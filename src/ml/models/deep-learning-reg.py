import pandas as pd
import tensorflow as tf
from pandas import DataFrame
from tensorflow import keras
from tensorflow.keras import layers
import tensorflow_docs as tfdocs
import tensorflow_docs.plots
import tensorflow_docs.modeling
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt

PATH_TRUTH = 'I:\Science\CIS\wyb15135\datasets_created\\formatted_high_lvl_ground_truth.csv'
PATH_PREDICTED_DEEP = 'I:\Science\CIS\wyb15135\datasets_created\high_lvl_predicted_DEEP.csv'


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
    data_id = data[['id', 'title', 'artist']]
    data = data.drop(
        columns=['mood', 'metadata.tags.musicbrainz_recordingid', 'metadata.tags.artist', 'id',
                 'metadata.tags.title', 'metadata.tags.album', 'metadata.audio_properties.length',
                 'metadata.audio_properties.replay_gain', 'metadata.audio_properties.equal_loudness',
                 'metadata.audio_properties.bit_rate', 'metadata.audio_properties.analysis_sample_rate'])
    artist_encoder = LabelEncoder()
    data['artist'] = artist_encoder.fit_transform(data['artist'].astype(str))
    title_encoder = LabelEncoder()
    data['title'] = title_encoder.fit_transform(data['title'].astype(str))

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

    # Build ml
    model_v = build_model(train_dataset)
    print(model_v.summary())

    model_a = build_model(train_dataset)
    print(model_a.summary())

    # Train
    EPOCHS = 1000
    history_v = model_v.fit(
        normed_train_data, train_labels_v,
        epochs=EPOCHS, validation_split=0.2, verbose=0,
        callbacks=[tfdocs.modeling.EpochDots()])

    history_a = model_a.fit(
        normed_train_data, train_labels_a,
        epochs=EPOCHS, validation_split=0.2, verbose=0,
        callbacks=[tfdocs.modeling.EpochDots()])

    # History
    hist_v = pd.DataFrame(history_v.history)
    hist_v['epoch'] = history_v.epoch
    print(hist_v.tail())

    hist_a = pd.DataFrame(history_a.history)
    hist_a['epoch'] = history_a.epoch
    print(hist_a.tail())

    # Predict and write to file
    loss_v, mae_v, mse_v = model_v.evaluate(normed_test_data, test_labels_v, verbose=2)
    print("Testing set Mean Abs Error: {:5.2f} Valence".format(mae_v))

    test_predictions_v = model_v.predict(normed_test_data).flatten()
    valence_data = DataFrame(test_predictions_v, columns=['valence'])

    loss_a, mae_a, mse_a = model_a.evaluate(normed_test_data, test_labels_a, verbose=2)
    print("Testing set Mean Abs Error: {:5.2f} Arousal".format(mae_a))
    test_predictions_a = model_a.predict(normed_test_data).flatten()
    arousal_data = DataFrame(test_predictions_a, columns=['arousal'])
    
    print(test_dataset.head())
    print(valence_data.head())
    print(arousal_data.head())
    
    predictions = test_dataset.join(valence_data.join(arousal_data))
    print(predictions.head())
    predictions['artist'] = artist_encoder.inverse_transform(predictions['artist'])
    predictions['title'] = title_encoder.inverse_transform(predictions['title'])

    predictions = pd.merge(data_id, predictions, on=['title', 'artist'])
    predictions.to_csv(PATH_PREDICTED_DEEP, index=False)

    # Visualize
    plotter = tfdocs.plots.HistoryPlotter(smoothing_std=2)
    plotter.plot({'Basic': history_v}, metric="mean_absolute_error")
    plt.ylim([0, 10])
    plt.ylabel('MAE [Valence]')
    plt.show()

    plotter.plot({'Basic': history_v}, metric="mean_squared_error")
    plt.ylim([0, 20])
    plt.ylabel('MSE [Valence^2]')
    plt.show()

    plotter.plot({'Basic': history_a}, metric="mean_absolute_error")
    plt.ylim([0, 10])
    plt.ylabel('MAE [Arousal]')
    plt.show()

    a = plt.axes(aspect='equal')
    plt.scatter(test_labels_v, test_predictions_v)
    plt.xlabel('True Values [Valence]')
    plt.ylabel('Predictions [Valence]')
    lims = [0, 15]
    plt.xlim(lims)
    plt.ylim(lims)
    _ = plt.plot(lims, lims)

    plt.show()

    error = test_predictions_v - test_labels_v
    plt.hist(error, bins=25)
    plt.xlabel("Prediction Error [Valence]")
    _ = plt.ylabel("Count")

    plt.show()


if __name__ == '__main__':
    main()
