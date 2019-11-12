from pandas.io.json import json_normalize
import requests
import tensorflow as tf
import seaborn as sns
from tensorflow import keras
from tensorflow.keras import layers

# the song Bohemian Rhapsody by Queen has a MBID of: b1a9c0e9-d987-4042-ae91-78d6a3267d69
highlvl_response = requests.get("https://acousticbrainz.org/b1a9c0e9-d987-4042-ae91-78d6a3267d69/high-level")
lowlvl_response = requests.get("https://acousticbrainz.org/b1a9c0e9-d987-4042-ae91-78d6a3267d69/low-level")

mood_columns = ['highlevel.mood_aggressive.all.aggressive', 'highlevel.mood_aggressive.all.not_aggressive',
                'highlevel.mood_aggressive.probability', 'highlevel.mood_aggressive.value',
                'highlevel.mood_aggressive.version.essentia',
                'highlevel.mood_aggressive.version.essentia_build_sha',
                'highlevel.mood_aggressive.version.essentia_git_sha', 'highlevel.mood_aggressive.version.extractor',
                'highlevel.mood_aggressive.version.gaia', 'highlevel.mood_aggressive.version.gaia_git_sha',
                'highlevel.mood_aggressive.version.models_essentia_git_sha',
                'highlevel.mood_electronic.all.electronic', 'highlevel.mood_electronic.all.not_electronic',
                'highlevel.mood_electronic.probability', 'highlevel.mood_electronic.value',
                'highlevel.mood_electronic.version.essentia',
                'highlevel.mood_electronic.version.essentia_build_sha',
                'highlevel.mood_electronic.version.essentia_git_sha', 'highlevel.mood_electronic.version.extractor',
                'highlevel.mood_electronic.version.gaia', 'highlevel.mood_electronic.version.gaia_git_sha',
                'highlevel.mood_electronic.version.models_essentia_git_sha', 'highlevel.mood_party.all.party',
                'highlevel.mood_party.all.not_party',
                'highlevel.mood_party.probability', 'highlevel.mood_party.value',
                'highlevel.mood_party.version.essentia', 'highlevel.mood_party.version.essentia_build_sha',
                'highlevel.mood_party.version.essentia_git_sha', 'highlevel.mood_party.version.extractor',
                'highlevel.mood_party.version.gaia', 'highlevel.mood_party.version.gaia_git_sha',
                'highlevel.mood_party.version.models_essentia_git_sha', 'highlevel.mood_acoustic.all.acoustic',
                'highlevel.mood_acoustic.all.not_acoustic', 'highlevel.mood_acoustic.probability',
                'highlevel.mood_acoustic.value', 'highlevel.mood_acoustic.version.essentia',
                'highlevel.mood_acoustic.version.essentia_build_sha',
                'highlevel.mood_acoustic.version.essentia_git_sha',
                'highlevel.mood_acoustic.version.extractor', 'highlevel.mood_acoustic.version.gaia',
                'highlevel.mood_acoustic.version.gaia_git_sha',
                'highlevel.mood_acoustic.version.models_essentia_git_sha',
                'highlevel.mood_happy.all.happy', 'highlevel.mood_happy.all.not_happy',
                'highlevel.mood_happy.probability',
                'highlevel.mood_happy.value', 'highlevel.mood_happy.version.essentia',
                'highlevel.mood_happy.version.essentia_build_sha',
                'highlevel.mood_happy.version.essentia_git_sha', 'highlevel.mood_happy.version.extractor',
                'highlevel.mood_happy.version.gaia', 'highlevel.mood_happy.version.gaia_git_sha',
                'highlevel.mood_happy.version.models_essentia_git_sha',
                'highlevel.mood_sad.all.sad', 'highlevel.mood_sad.all.not_sad',
                'highlevel.mood_sad.probability',
                'highlevel.mood_sad.value', 'highlevel.mood_sad.version.essentia',
                'highlevel.mood_sad.version.essentia_build_sha',
                'highlevel.mood_sad.version.essentia_git_sha', 'highlevel.mood_sad.version.extractor',
                'highlevel.mood_sad.version.gaia', 'highlevel.mood_sad.version.gaia_git_sha',
                'highlevel.mood_sad.version.models_essentia_git_sha',
                'highlevel.mood_relaxed.all.relaxed', 'highlevel.mood_relaxed.all.not_relaxed',
                'highlevel.mood_relaxed.probability',
                'highlevel.mood_relaxed.value', 'highlevel.mood_relaxed.version.essentia',
                'highlevel.mood_relaxed.version.essentia_build_sha',
                'highlevel.mood_relaxed.version.essentia_git_sha', 'highlevel.mood_relaxed.version.extractor',
                'highlevel.mood_relaxed.version.gaia', 'highlevel.mood_relaxed.version.gaia_git_sha',
                'highlevel.mood_relaxed.version.models_essentia_git_sha',
                'highlevel.moods_mirex.all.Cluster1', 'highlevel.moods_mirex.all.Cluster2',
                'highlevel.moods_mirex.all.Cluster3', 'highlevel.moods_mirex.all.Cluster4',
                'highlevel.moods_mirex.all.Cluster5', 'highlevel.moods_mirex.probability',
                'highlevel.moods_mirex.value', 'highlevel.moods_mirex.version.essentia',
                'highlevel.moods_mirex.version.essentia_build_sha',
                'highlevel.moods_mirex.version.essentia_git_sha', 'highlevel.moods_mirex.version.extractor',
                'highlevel.moods_mirex.version.gaia', 'highlevel.moods_mirex.version.gaia_git_sha',
                'highlevel.moods_mirex.version.models_essentia_git_sha']

# Path to high level dataset
PATH = 'I:/Science/CIS/wyb15135/datasets_unmodified/acousticbrainz-highlevel-json-20150130'


def read_json_directory():
    print()


def fetch_song_data(response):
    if response.status_code != 200:
        # This means something went wrong.
        print('GET /api/mbid/level/ {}'.format(response.status_code))

    return response.json()


def json_to_dataframe(json):
    dataframe = json_normalize(json)
    return dataframe


def extract_mood_information(dataframe):
    mood_dataframe = dataframe[mood_columns]
    return mood_dataframe


def drop_mood_information(dataframe):
    dataframe = dataframe.drop(columns=mood_columns)
    return dataframe


def build_model(dataframe):
    model = keras.Sequential([
        layers.Dense(64, activation='relu', input_shape=[len(dataframe.keys())]),
        layers.Dense(64, activation='relu'),
        layers.Dense(1)
    ])

    optimizer = tf.keras.optimizers.RMSprop(0.001)

    model.compile(loss='mse',
                  optimizer=optimizer,
                  metrics=['mae', 'mse'])
    return model


def model_data(dataframe, labels):
    sns.pairplot(dataframe['highlevel.danceability.value', 'metadata.version.highlevel.essentia_git_sha'],
                 diag_kind="kde")
    print(dataframe.describe())

    mood_label = labels.pop('highlevel.moods_mirex.version.gaia')
    model = build_model()

    example_result = model.predict(dataframe)
    print(example_result)

def main():
    highlvl_datafrme = json_to_dataframe(fetch_song_data(highlvl_response))
    lowlvl_dataframe = json_to_dataframe(fetch_song_data(lowlvl_response))

    mood_dataframe = extract_mood_information(highlvl_datafrme)
    highlvl_datafrme = drop_mood_information(highlvl_datafrme)

    print("output: ")
    print(highlvl_datafrme)
    print(highlvl_datafrme.keys())
    print(lowlvl_dataframe)
    print(mood_dataframe)


if __name__ == '__main__':
    main()
