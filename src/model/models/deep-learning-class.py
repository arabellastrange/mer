import ast

import tensorflow as tf
import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.preprocessing import LabelEncoder
from tensorflow import feature_column
from tensorflow.keras import layers
from sklearn.model_selection import train_test_split
import tensorflow_docs as tfdocs
import tensorflow_docs.plots
import matplotlib as plt

PATH_MOOD = 'I:\Science\CIS\wyb15135\datasets_created\datasets_created_ground_truth.csv'

PATH_PREDICTED_H_DEEP = 'I:\Science\CIS\wyb15135\datasets_created\high_lvl_predicted_deep_class.csv'
PATH_PREDICTED_L_DEEP = 'I:\Science\CIS\wyb15135\datasets_created\low_lvl_predicted_deep_class.csv'

PATH_TRUTH_HIGH = 'I:\Science\CIS\wyb15135\datasets_created\ground_truth_classification_high.csv'
PATH_TRUTH_HIGH_CLASS = 'I:\Science\CIS\wyb15135\datasets_created\ground_truth_classification_high_min_class.csv'
PATH_TRUTH_LOW = 'I:\Science\CIS\wyb15135\datasets_created\ground_truth_classification_high_low.csv'

label_cols = ['airy', 'ambient', 'angry', 'animated', 'astonishing', 'big', 'bizarre', 'black', 'bleak', 'boisterous',
              'boring', 'breezy', 'bright', 'buoyant', 'calm', 'cheerful', 'cheery', 'choral', 'comfortable', 'complex',
              'constant', 'contented', 'contrasting', 'cool', 'curious', 'dark', 'daze', 'deafening', 'deep',
              'delicate', 'delighted', 'despondent', 'different', 'difficult', 'dim', 'distinctive',
              'dreamy', 'dull', 'earthy', 'easy', 'eccentric', 'ecstatic', 'ecstasy', 'eerie', 'elated', 'emphatic',
              'encouraging',
              'enveloping', 'extraordinary', 'fashionable', 'fast', 'fiery', 'flashy', 'fluid',
              'funky', 'happy', 'hard', 'harmonious', 'heated', 'heavy', 'hip', 'hopeful', 'jazzy', 'light',
              'lively', 'loud', 'low', 'luminous', 'melancholy', 'mellow', 'mild', 'modish', 'monotonous', 'mournful',
              'muted', 'odd', 'old', 'operatic', 'orchestral', 'passionate', 'peaceful', 'peculiar', 'profound',
              'quick',
              'quiet', 'rapture', 'relaxed', 'repeated', 'repetitive', 'rich', 'reticent', 'sad', 'scary', 'serene',
              'sexy', 'silent',
              'slow', 'soft', 'somber', 'soothing', 'space', 'storming', 'strange', 'sunny', 'sweet',
              'trance', 'unconventional', 'upbeat', 'weighty', 'weird', 'wistful', 'zippy']
l_cols = ['dejected', 'snappy', 'gray', 'traditional', 'energetic', 'familiar']


def load_file(path):
    return pd.read_csv(path)


def norm(x, train_stats):
    return (x - train_stats['mean']) / train_stats['std']


def df_to_dataset(data, shuffle=True, batch_size=512):
    data = data.copy()
    labels = data[label_cols].copy()
    data.drop(label_cols, axis=1, inplace=True)
    ds = tf.data.Dataset.from_tensor_slices((dict(data), labels))
    if shuffle:
        ds = ds.shuffle(buffer_size=len(data))
    ds = ds.batch(batch_size)
    return ds


def create_model(feature_layer, train, val):
    model = tf.keras.Sequential([
        feature_layer,
        layers.Dense(128, activation='relu'),
        layers.Dense(128, activation='relu'),
        layers.Dense(1, activation='sigmoid'),
        layers.Activation('relu')
    ])

    model.compile(optimizer='adam',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])

    return model


def custom_model_fn(features, labels, mode):
    my_head = tf.estimator.MultiLabelHead(n_classes=112)

    feature_columns = []
    for header in features:
        feature_columns.append(feature_column.numeric_column(header))
    feature_layer = layers.DenseFeatures(feature_columns)
    inputs = feature_layer(features)

    model = tf.keras.Sequential()
    model.add(layers.Dense(128, activation='relu'))
    model.add(layers.Dense(128, activation='relu'))
    model.add(layers.Dense(1, activation='sigmoid'))
    model.add(tf.keras.layers.Dense(units=my_head.logits_dimension, activation=None))
    logits = model(inputs)

    return my_head.create_estimator_spec(
        features=features,
        mode=mode,
        labels=labels,
        optimizer=tf.keras.optimizers.Adagrad(lr=0.1),
        logits=logits)


def create_estimator(features, labels, mode):
    custom_estimator = tf.estimator.Estimator(model_fn=custom_model_fn(features, labels, mode))
    return custom_estimator


def process_data(data, flag='high'):
    data = data.drop(columns=label_cols, errors='ignore')

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


def make_input_fn(data_df, label_df, num_epochs=25, shuffle=True, batch_size=512):
    def input_fn():
        dataset = tf.data.Dataset.from_tensor_slices((dict(data_df), label_df))
        if shuffle:
            dataset = dataset.shuffle(1000)
        dataset = dataset.batch(batch_size).repeat(num_epochs)
        return dataset

    return input_fn


def run_high_level_model():
    # data = load_file(PATH_TRUTH_HIGH)
    # data = process_data(data)

    mlb = MultiLabelBinarizer()
    data = load_file(PATH_TRUTH_HIGH_CLASS)
    data['mood'] = data['mood'].apply(ast.literal_eval)
    data_m = pd.DataFrame(mlb.fit_transform(data.pop('mood')), columns=mlb.classes_, index=data.index)
    data = data.join(data_m)
    dataset = data.drop(columns=['id'])

    train, test = train_test_split(dataset, test_size=0.3)
    train, val = train_test_split(train, test_size=0.3)
    print(len(train), 'train examples')
    print(len(val), 'validation examples')
    print(len(test), 'test examples')

    # Select training and testing subsets
    train_input_fn = make_input_fn(train, train[label_cols])
    eval_input_fn = make_input_fn(val, val[label_cols], num_epochs=15, shuffle=False)

    # create input pipeline
    # batch_size = 512
    # train_ds = df_to_dataset(train, batch_size=batch_size)
    # val_ds = df_to_dataset(val, shuffle=False, batch_size=batch_size)
    # test_ds = df_to_dataset(test, shuffle=False, batch_size=batch_size)

    # get feature cols
    # feature_columns = []
    rest_cols = dataset[dataset.columns.difference(label_cols)].columns.values
    # for header in rest_cols:
    #   feature_columns.append(feature_column.numeric_column(header))
    # feature_layer = tf.keras.layers.DenseFeatures(feature_columns)
    # model = create_model(feature_layer, train_ds, val_ds)
    estimator = create_estimator(rest_cols, label_cols, 'train')
    estimator.train(train_input_fn)
    results = estimator.evaluate(eval_input_fn)
    print(results)

    # history = model.fit(train_ds,
    #                    validation_data=val_ds,
    #                    epochs=25)
    # print(model.summary())
    # loss, acc = model.evaluate(test_ds)
    # print(loss)
    # print(acc)
    # test_predictions = model.predict(test_ds)
    # print(test_predictions[:5])
    # visualize(history)
    # output_predictions(test, test_predictions)


def run_low_level_model():
    pass


def output_predictions(x, y):
    pass


def visualize(history):
    plotter = tfdocs.plots.HistoryPlotter(smoothing_std=2)
    plotter.plot({'Basic': history}, metric="acc")
    # plt.show()

    plotter.plot({'Basic': history}, metric="loss")
    # plt.show()


def get_uncommon_tags(mood_array):
    mood_array = mood_array.apply(pd.Series).stack().value_counts()
    mood_array = mood_array[mood_array < 50]

    return mood_array.keys()


def main():
    run_high_level_model()
    # run_low_level_model()


if __name__ == '__main__':
    main()
