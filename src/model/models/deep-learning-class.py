import ast

import tensorflow as tf
import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer
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
              'dejected', 'delicate', 'delighted', 'despondent', 'different', 'difficult', 'dim', 'distinctive',
              'dreamy', 'dull', 'earthy', 'easy', 'eccentric', 'ecstatic', 'ecstasy', 'eerie', 'elated', 'emphatic',
              'encouraging',
              'energetic', 'enveloping', 'extraordinary', 'familiar', 'fashionable', 'fast', 'fiery', 'flashy', 'fluid',
              'funky', 'gray', 'happy', 'hard', 'harmonious', 'heated', 'heavy', 'hip', 'hopeful', 'jazzy', 'light',
              'lively', 'loud', 'low', 'luminous', 'melancholy', 'mellow', 'mild', 'modish', 'monotonous', 'mournful',
              'muted', 'odd', 'old', 'operatic', 'orchestral', 'passionate', 'peaceful', 'peculiar', 'profound',
              'quick',
              'quiet', 'rapture', 'relaxed', 'repeated' ,'repetitive', 'rich', 'reticent', 'sad', 'scary', 'serene',
              'sexy','silent',
              'slow', 'snappy', 'soft', 'somber', 'soothing', 'space', 'storming', 'strange', 'sunny', 'sweet',
              'traditional', 'trance', 'unconventional', 'upbeat', 'weighty', 'weird', 'wistful', 'zippy']


def load_file(path):
    return pd.read_csv(path)


def norm(x, train_stats):
    return (x - train_stats['mean']) / train_stats['std']


def df_to_dataset(data, shuffle=True, batch_size=32):
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
        layers.Dense(1, activation='sigmoid')
    ])

    model.compile(optimizer='adam',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])
    print(model.summary())

    return model


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
    mlb_scale = MultiLabelBinarizer()
    mlb_key = MultiLabelBinarizer()
    mlb_chord = MultiLabelBinarizer()

    data = data.join(
        pd.DataFrame(mlb_scale.fit_transform(data.pop('tonal.key_scale').astype(str)), columns=mlb_scale.classes_,
                     index=data.index))
    data = data.join(
        pd.DataFrame(mlb_chord.fit_transform(data.pop('tonal.chords_scale').astype(str)), columns=mlb_chord.classes_,
                     index=data.index))
    data = data.join(
        pd.DataFrame(mlb_key.fit_transform(data.pop('tonal.key_key').astype(str)), columns=mlb_key.classes_,
                     index=data.index))

    return data


def run_high_level_model():
    data = load_file(PATH_TRUTH_HIGH)
    data = process_data(data)

    # Select training and testing subsets
    train, test = train_test_split(data, test_size=0.2)
    train, val = train_test_split(train.drop(column='id'), test_size=0.2)
    print(len(train), 'train examples')
    print(len(val), 'validation examples')
    print(len(test), 'test examples')

    # create input pipeline
    batch_size = 512

    train_ds = df_to_dataset(train, batch_size=batch_size)
    val_ds = df_to_dataset(val, shuffle=False, batch_size=batch_size)
    test_ds = df_to_dataset(test, shuffle=False, batch_size=batch_size)

    # get feature cols
    feature_columns = []
    rest_cols = data[data.columns.difference(label_cols)].columns.values
    for header in rest_cols:
        feature_columns.append(feature_column.numeric_column(header))

    feature_layer = tf.keras.layers.DenseFeatures(feature_columns)

    model = create_model(feature_layer, train_ds, val_ds)

    history = model.fit(train_ds,
                        validation_data=val_ds,
                        epochs=25)

    loss, acc = model.evaluate(test_ds)
    print(loss)
    print(acc)

    test_predictions = model.predict(test_ds).flatten()
    print(test_predictions)

    visualize(history)
    output_predictions(test, test_predictions)


def output_predictions(x, y):
    pass


def visualize(history):
    plotter = tfdocs.plots.HistoryPlotter(smoothing_std=2)
    plotter.plot({'Basic': history}, metric="acc")
    plt.show()

    plotter.plot({'Basic': history}, metric="loss")
    plt.show()


def run_low_level_model():
    pass


def get_uncommon_tags(mood_array):
    mood_array = mood_array.apply(pd.Series).stack().value_counts()
    mood_array = mood_array[mood_array < 50]

    return mood_array.keys()


def main():
    run_high_level_model()
    run_low_level_model()


if __name__ == '__main__':
    main()
