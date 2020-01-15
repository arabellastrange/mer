import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import tensorflow_docs as tfdocs
import tensorflow_docs.plots
import tensorflow_docs.modeling
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
    train_stats.pop("valence")
    train_stats.pop("arousal")
    train_stats = train_stats.transpose()
    print(train_stats)

    # Drop labels
    train_labels_v = train_dataset.pop('valence')
    train_labels_a = train_dataset.pop('arousal')
    test_labels_v = test_dataset.pop('valence')
    test_labels_a = test_dataset.pop('arousal')

    # Normalise
    normed_train_data = norm(train_dataset, train_stats)
    normed_test_data = norm(test_dataset, train_stats)

    # Build model
    model = build_model(train_dataset)
    model.summary()

    # Train
    EPOCHS = 1000
    history = model.fit(
        normed_train_data, train_labels_v,
        epochs=EPOCHS, validation_split=0.2, verbose=0,
        callbacks=[tfdocs.modeling.EpochDots()])

    
    # History 
    hist = pd.DataFrame(history.history)
    hist['epoch'] = history.epoch
    print(hist.tail())
    
    plotter = tfdocs.plots.HistoryPlotter(smoothing_std=2)
    plotter.plot({'Basic': history}, metric = "mean_absolute_error")
    plt.ylim([0, 10])
    plt.ylabel('MAE [Valence]')
    plt.show()
    
    plotter.plot({'Basic': history}, metric = "mean_squared_error")
    plt.ylim([0, 20])
    plt.ylabel('MSE [Valence^2]')
    plt.show()
    
    # Predict
    loss, mae, mse = model.evaluate(normed_test_data, test_labels_v, verbose=2)
    print("Testing set Mean Abs Error: {:5.2f} Valence".format(mae))
    
    test_predictions = model.predict(normed_test_data).flatten()

    a = plt.axes(aspect='equal')
    plt.scatter(test_labels_v, test_predictions)
    plt.xlabel('True Values [Valence]')
    plt.ylabel('Predictions [Valence]')
    lims = [0, 15]
    plt.xlim(lims)
    plt.ylim(lims)
    _ = plt.plot(lims, lims)
    
    plt.show()
    
    error = test_predictions - test_labels_v
    plt.hist(error, bins = 25)
    plt.xlabel("Prediction Error [MPG]")
    _ = plt.ylabel("Count")
    
    plt.show()

if __name__ == '__main__':
    main()
