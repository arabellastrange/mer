import json
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import tensorflow as tf
from keras import layers
from tensorflow import keras
from pandas.io.json import json_normalize

mood_columns = ['highlevel.mood_acoustic.all.acoustic', 'highlevel.mood_acoustic.all.not_acoustic',
                'highlevel.mood_acoustic.probability', 'highlevel.mood_acoustic.value',
                'highlevel.mood_aggressive.all.aggressive', 'highlevel.mood_aggressive.all.not_aggressive',
                'highlevel.mood_aggressive.probability', 'highlevel.mood_aggressive.value',
                'highlevel.mood_electronic.all.electronic', 'highlevel.mood_electronic.all.not_electronic',
                'highlevel.mood_electronic.probability', 'highlevel.mood_electronic.value',
                'highlevel.mood_happy.all.happy', 'highlevel.mood_happy.all.not_happy',
                'highlevel.mood_happy.probability', 'highlevel.mood_happy.value',
                'highlevel.mood_party.all.not_party', 'highlevel.mood_party.all.party',
                'highlevel.mood_party.probability', 'highlevel.mood_party.value',
                'highlevel.mood_relaxed.all.not_relaxed', 'highlevel.mood_relaxed.all.relaxed',
                'highlevel.mood_relaxed.probability', 'highlevel.mood_relaxed.value',
                'highlevel.mood_sad.all.not_sad', 'highlevel.mood_sad.all.sad',
                'highlevel.mood_sad.probability', 'highlevel.mood_sad.value',
                'highlevel.moods_mirex.all.Cluster1', 'highlevel.moods_mirex.all.Cluster2',
                'highlevel.moods_mirex.all.Cluster3', 'highlevel.moods_mirex.all.Cluster4',
                'highlevel.moods_mirex.all.Cluster5', 'highlevel.moods_mirex.probability',
                'highlevel.moods_mirex.value']


def read_json_directory(path):
    dataframe = pd.DataFrame()
    files = []

    # r=root, d=directories, f = files
    # read the first 10 files
    for r, d, f in os.walk(path):
        for file in f:
            if '.json' in file:
                files.append(os.path.join(r, file))
            if len(files) > 10:
                break

    for f in files:
        print("reading: " + f)
        with open(f) as json_file:
            j = json_normalize(json.load(json_file))
            dataframe = dataframe.append(j, sort=True)

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
    # investigate data
    sns.pairplot(dataframe[['highlevel.danceability.value', 'highlevel.gender.all.female', 'highlevel.gender.all.male']],
                 diag_kind="kde")
    # plt.show()
    print(dataframe.describe())

    model = build_model(dataframe)

    example_result = model.predict(dataframe)
    print(example_result)


def main():
    highlvl_dataframe = read_json_directory(
        'I:\Science\CIS\wyb15135\datasets_unmodified\\acousticbrainz-highlevel-json-20150130\highlevel\\0\\00')

    print("output: ")
    print(highlvl_dataframe.head())

    mood_dataframe = extract_mood_information(highlvl_dataframe)
    highlvl_datafrme = drop_mood_information(highlvl_dataframe)

    print("output: ")
    print(highlvl_datafrme.head())
    print("mood: ")
    print(mood_dataframe.head())

    model_data(highlvl_datafrme, mood_dataframe)


if __name__ == '__main__':
    main()
