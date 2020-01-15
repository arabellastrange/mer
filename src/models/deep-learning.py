import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import tensorflow_docs as tfdocs
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt

PATH_TRUTH = 'I:\Science\CIS\wyb15135\datasets_created\\formatted_high_lvl_ground_truth.csv'


def load_file(path):
    return pd.read_csv(path)


def norm(x, train_stats):
    return (x - train_stats['mean']) / train_stats['std']


def build_model(train_dataset):
    model = keras.Sequential([
        layers.Dense(64, activation='relu', input_shape=[len(train_dataset.keys())]),
        layers.Dense(64, activation='relu'),
        layers.Dense(1)
    ])

    optimizer = tf.keras.optimizers.RMSprop(0.001)

    model.compile(loss='mse',
                  optimizer=optimizer,
                  metrics=['mae', 'mse'])
    return model


def main():
    # Pre-process data
    data = load_file(PATH_TRUTH)
    data = data.drop(
        columns=['mood', 'metadata.tags.musicbrainz_recordingid', 'metadata.tags.artist', 'title', 'id',
                 'metadata.tags.title', 'metadata.tags.album', 'metadata.audio_properties.length',
                 'metadata.audio_properties.replay_gain', 'metadata.audio_properties.equal_loudness',
                 'metadata.audio_properties.bit_rate', 'metadata.audio_properties.analysis_sample_rate'])
    artist_encoder = LabelEncoder()
    data['artist'] = artist_encoder.fit_transform(data['artist'].astype(str))

    # Select training and testing subsets
    train_dataset = data.sample(frac=0.8, random_state=0)
    test_dataset = data.drop(train_dataset.index)

    sns.pairplot(
        train_dataset[["valence", "arousal", "highlevel.danceability.all.danceable", "highlevel.timbre.all.bright"]],
        diag_kind="kde")
    plt.show()

    # Stats
    train_stats = train_dataset.describe()
    train_stats = train_stats.pop("valence")
    train_stats = train_stats.pop("arousal")
    train_stats = train_stats.transpose()
    print(train_stats)

    # Drop labels
    train_labels_v = train_dataset.pop('valence')
    train_labels_a = train_dataset.pop('arousal')
    test_labels_v = test_dataset.pop('valence')
    test_labels_a = test_dataset.pop('arousal')

    # Normalise
    normed_train_data = norm(train_dataset)
    normed_test_data = norm(test_dataset)

    # Build model
    model = build_model()
    model.summary()

    # Train
    EPOCHS = 1000
    history = model.fit(
        normed_train_data, train_labels_v,
        epochs=EPOCHS, validation_split=0.2, verbose=0,
        callbacks=[tfdocs.modeling.EpochDots()])

    # Predict
    example_batch = normed_train_data[:10]
    example_result = model.predict(example_batch)
    print(example_result)


if __name__ == '__main__':
    main()
