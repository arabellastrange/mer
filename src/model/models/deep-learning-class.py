import tensorflow as tf
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from tensorflow import feature_column
from tensorflow.keras import layers
from sklearn.model_selection import train_test_split

PATH_TRUTH = 'I:\Science\CIS\wyb15135\datasets_created\\formatted_high_lvl_ground_truth.csv'
PATH_PREDICTED_DEEP = 'I:\Science\CIS\wyb15135\datasets_created\high_lvl_predicted_deep_class.csv'
label_cols = ['abrupt', 'abundant', 'active', 'aged', 'airy', 'ambient', 'ancient', 'angry', 'annoyed', 'area', 'arena',
              'astonishing', 'awful', 'awkward', 'below', 'bitter', 'bizarre', 'black', 'breezy', 'bright', 'broad',
              'buoyant', 'buried', 'calm', 'cheerful', 'cheery', 'chorus', 'circling', 'cloudy', 'coma', 'comfortable',
              'comfy', 'contented', 'contrasting', 'cool', 'creepy', 'dark', 'deep', 'delicate', 'depressed',
              'different', 'dismal', 'disparate', 'earthy', 'eerie', 'fashionable', 'fast', 'flashy', 'funky', 'happy',
              'hard',
              'harmonious', 'heavy', 'jazzy', 'light', 'lively', 'loud', 'low', 'luminous', 'mellow', 'moving', 'muted',
              'old', 'opera', 'orchestra', 'peaceful', 'quick', 'quiet', 'rapture', 'relaxed', 'repetitive', 'sad',
              'savory', 'scary', 'slow', 'soft', 'solid', 'space', 'strange', 'strong', 'trance', 'upbeat', 'weird']


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

    model.fit(train,
              validation_data=val,
              epochs=5)

    return model


def main():
    data = load_file(PATH_TRUTH)
    data_id = data[['id', 'title', 'artist']]

    data = data.drop(
        columns=['metadata.tags.musicbrainz_recordingid', 'metadata.tags.artist', 'id', 'metadata.tags.title',
                 'metadata.tags.album'])

    # encode string data
    artist_encoder = LabelEncoder()
    data['artist'] = artist_encoder.fit_transform(data['artist'].astype(str))
    title_encoder = LabelEncoder()
    data['title'] = title_encoder.fit_transform(data['title'].astype(str))

    # Select training and testing subsets
    train, test = train_test_split(data, test_size=0.2)
    train, val = train_test_split(train, test_size=0.2)
    print(len(train), 'train examples')
    print(len(val), 'validation examples')
    print(len(test), 'test examples')

    # create input pipeline
    batch_size = 1000
    train_ds = df_to_dataset(train, batch_size=batch_size)
    val_ds = df_to_dataset(val, shuffle=False, batch_size=batch_size)
    test_ds = df_to_dataset(test, shuffle=False, batch_size=batch_size)

    # get feature cols
    feature_columns = []
    rest_cols = data[data.columns.difference(label_cols)].columns.values()
    for header in [rest_cols]:
        feature_columns.append(feature_column.numeric_column(header))

    feature_layer = tf.keras.layers.DenseFeatures(feature_columns)

    model = create_model()


if __name__ == '__main__':
    main()
