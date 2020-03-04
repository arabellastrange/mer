import ast

import tensorflow as tf
import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

PATH_MOOD = 'I:\Science\CIS\wyb15135\datasets_created\datasets_created_ground_truth.csv'

PATH_PREDICTED_H_DEEP = 'I:\Science\CIS\wyb15135\datasets_created\high_lvl_predicted_deep_class.csv'
PATH_PREDICTED_L_DEEP = 'I:\Science\CIS\wyb15135\datasets_created\low_lvl_predicted_deep_class.csv'

PATH_TRUTH_HIGH = 'I:\Science\CIS\wyb15135\datasets_created\ground_truth_classification_high.csv'
PATH_TRUTH_HIGH_CLASS = 'I:\Science\CIS\wyb15135\datasets_created\ground_truth_classification_high_min_class.csv'
PATH_TRUTH_LOW = 'I:\Science\CIS\wyb15135\datasets_created\ground_truth_classification_high_low.csv'
PATH_TRUTH_LOW_CLASS = 'I:\Science\CIS\wyb15135\datasets_created\ground_truth_classification_low_min_class.csv'

label_cols_min = ['ambient', 'angry', 'breezy', 'calm', 'cheerful', 'contented', 'dark',
                  'delighted', 'ecstatic', 'elated', 'fast', 'fiery', 'funky', 'happy',
                  'heated', 'heavy', 'jazzy', 'loud', 'melancholy', 'mellow', 'mournful',
                  'passionate', 'quiet', 'relaxed', 'sad', 'serene', 'slow', 'soft',
                  'space', 'storming', 'upbeat', 'weird', 'wistful']


def load_file(path):
    return pd.read_csv(path)


def df_to_dataset(data, shuffle=True, batch_size=512):
    data = data.copy()
    labels = data[label_cols_min].copy()
    data.drop(label_cols_min, axis=1, inplace=True)
    ds = tf.data.Dataset.from_tensor_slices((dict(data), labels))
    if shuffle:
        ds = ds.shuffle(buffer_size=len(data))
    ds = ds.batch(batch_size)
    return ds


def process_data(data, flag='high'):
    data = data.drop(columns=label_cols_min, errors='ignore')

    data_mood = load_file(PATH_MOOD)
    data_mood['mood'] = data_mood['mood'].apply(ast.literal_eval)
    data = pd.merge(data, data_mood[['mood', 'title', 'artist']], on=['title', 'artist'])

    data = data.drop(
        columns=['metadata.tags.musicbrainz_recordingid', 'metadata.tags.artist', 'metadata.tags.title',
                 'metadata.tags.album', 'artist', 'title', 'fallback-id'])

    for i, row in data.iterrows():
        for m_tag in get_uncommon_tags(data['mood']):
            if m_tag in row['mood']:
                row['mood'].remove(m_tag)
        print('updating row: {:d}'.format(i))
        data.at[i, 'mood'] = row['mood']

    if flag == 'high':
        data = process_high_data(data)
    if flag == 'low':
        data = process_low_data(data)

    return data


def process_high_data(data):
    # get rid of empty row after dropping sparse classes
    for i, row in data.iterrows():
        if row['mood'] == '' or row['mood'] == 'fast' or row['mood'] == 'slow':
            data.drop(i)

    return data


def process_low_data(data):
    lb_scale = LabelEncoder()
    lb_scale.fit(['major', 'minor'])
    lb_key = LabelEncoder()
    lb_key.fit(['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#'])

    data['tonal.key_scale'] = data['tonal.key_scale'].astype(str)
    data['tonal.chords_scale'] = data['tonal.chords_scale'].astype(str)
    data['tonal.chords_key'] = data['tonal.chords_key'].astype(str)
    data['tonal.key_key'] = data['tonal.key_key'].astype(str)

    data['tonal.key_scale'] = lb_scale.transform(data['tonal.key_scale'])
    data['tonal.chords_scale'] = lb_scale.transform(data['tonal.chords_scale'])
    data['tonal.key_key'] = lb_key.transform(data['tonal.key_key'])
    data['tonal.chords_key'] = lb_key.transform(data['tonal.chords_key'])

    return data


def run_model(data):
    mlb = MultiLabelBinarizer()
    data['mood'] = data['mood'].apply(ast.literal_eval)
    data_m = pd.DataFrame(mlb.fit_transform(data.pop('mood')), columns=mlb.classes_, index=data.index)
    data = data.join(data_m)
    print(data_m.columns)
    dataset = data.drop(columns=['id'])

    train, test = train_test_split(dataset, test_size=0.3)
    train, val = train_test_split(train, test_size=0.3)
    print(len(train), 'train examples')
    print(len(val), 'validation examples')
    print(len(test), 'test examples')

    ytrain = train[label_cols_min]
    yval = val[label_cols_min]
    train = train.drop(columns=label_cols_min)
    val = val.drop(columns=label_cols_min)
    ytest = test[label_cols_min]
    test = test.drop(columns=label_cols_min)

    feature_columns = []
    for feature in train.keys():
        feature_columns.append(tf.feature_column.numeric_column(key=feature))

    predictions = run_dnn_estimator(feature_columns, train, ytrain, val, yval, test)

    for pred_dict, expec in zip(predictions, ytest):
        for i in range(0, 5):
            probability = pred_dict['probabilities'][i]
            print('Prediction is "{}" ({:.1f}%), expected "{}"'.format(
                label_cols_min[i], 100 * probability, expec))


def run_dnn_estimator(feature_columns, train, ytrain, val, yval, test):
    estimator = multi_label_estimator(feature_columns=feature_columns)
    estimator.train(input_fn=lambda: input_fn(train, ytrain), steps=2000)
    metrics = estimator.evaluate(input_fn=lambda: input_fn(val, yval, training=False))
    print(metrics)

    f1 = 2 * (metrics['precision/positive_threshold_0.5'] * metrics['recall/positive_threshold_0.5']) / (
                metrics['precision/positive_threshold_0.5'] + metrics['recall/positive_threshold_0.5'])
    print('F1 Score DNN: ')
    print(f1)

    predictions = estimator.predict(input_fn=lambda: input_predict_fn(test))
    return predictions


def run_custom_estimator(train, ytrain, val, yval, test):
    multi_estimator = tf.estimator.Estimator(model_fn=multi_label_model_fn)
    multi_estimator.train(input_fn=lambda: input_fn(train, ytrain))
    metrics = multi_estimator.evaluate(input_fn=lambda: input_fn(val, yval, training=False))
    print(metrics)

    f1 = 2 * (metrics['precision/positive_threshold_0.5'] * metrics['recall/positive_threshold_0.5']) / (
            metrics['precision/positive_threshold_0.5'] + metrics['recall/positive_threshold_0.5'])
    print('F1 Score DNN: ')
    print(f1)

    predictions = multi_estimator.predict(input_fn=lambda: input_predict_fn(test))
    return predictions


def output_predictions(x, y):
    pass


def visualize():
    pass


def get_uncommon_tags(mood_array):
    mood_array = mood_array.apply(pd.Series).stack().value_counts()
    mood_array = mood_array[mood_array < 50]

    return mood_array.keys()


def input_fn(data_df, label_df, training=True, batch_size=512):
    dataset = tf.data.Dataset.from_tensor_slices((dict(data_df), label_df))
    if training:
        dataset = dataset.shuffle(1000).repeat()
    return dataset.batch(batch_size)


def input_predict_fn(features, batch_size=256):
    """An input function for prediction."""
    return tf.data.Dataset.from_tensor_slices(dict(features)).batch(batch_size)


def multi_label_model_fn(features, labels, mode, config=None):
    head = tf.estimator.MultiLabelHead(n_classes=33, thresholds=[0.4, 0.5, 0.6])
    feature_columns = []
    for f in features:
        feature_columns.append(tf.feature_column.numeric_column(f))
        print(f)
    print(feature_columns)
    feature_layer = tf.keras.layers.DenseFeatures(feature_columns)
    inputs = feature_layer(features)
    print(inputs)

    # comp logits
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.Dense(128, activation='relu'))
    model.add(tf.keras.layers.Dense(128, activation='relu'))
    model.add(tf.keras.layers.Dense(1, activation='sigmoid'))
    model.add(tf.keras.layers.Dense(units=head.logits_dimension, activation=None))
    logits = model(inputs)
    return head.create_estimator_spec(
        features=features,
        labels=labels,
        mode=mode,
        logits=logits,
        optimizer=tf.keras.optimizers.Adagrad(lr=0.1))


def multi_label_estimator(feature_columns):
    multi_head = tf.estimator.MultiLabelHead(n_classes=33, thresholds=[0.4, 0.5, 0.6])
    estimator = tf.estimator.DNNEstimator(
        head=multi_head,
        hidden_units=[1024, 512, 256],
        feature_columns=feature_columns,
        optimizer=tf.keras.optimizers.Adagrad(lr=0.1))
    return estimator


def main():
    data = load_file(PATH_TRUTH_HIGH_CLASS)
    run_model(data)


if __name__ == '__main__':
    main()