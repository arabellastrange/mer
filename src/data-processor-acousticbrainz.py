import json
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from keras import layers
from keras.models import Sequential
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

mood_columns_stats = ['highlevel.mood_acoustic.all.acoustic', 'highlevel.mood_acoustic.all.not_acoustic',
                      'highlevel.mood_acoustic.probability', 'highlevel.mood_aggressive.all.aggressive',
                      'highlevel.mood_aggressive.all.not_aggressive',
                      'highlevel.mood_aggressive.probability', 'highlevel.mood_electronic.all.electronic',
                      'highlevel.mood_electronic.all.not_electronic',
                      'highlevel.mood_electronic.probability', 'highlevel.mood_happy.all.happy',
                      'highlevel.mood_happy.all.not_happy',
                      'highlevel.mood_happy.probability', 'highlevel.mood_party.all.not_party',
                      'highlevel.mood_party.all.party',
                      'highlevel.mood_party.probability', 'highlevel.mood_relaxed.all.not_relaxed',
                      'highlevel.mood_relaxed.all.relaxed',
                      'highlevel.mood_relaxed.probability', 'highlevel.mood_sad.all.not_sad',
                      'highlevel.mood_sad.all.sad',
                      'highlevel.mood_sad.probability', 'highlevel.moods_mirex.all.Cluster1',
                      'highlevel.moods_mirex.all.Cluster2',
                      'highlevel.moods_mirex.all.Cluster3', 'highlevel.moods_mirex.all.Cluster4',
                      'highlevel.moods_mirex.all.Cluster5', 'highlevel.moods_mirex.probability']


def read_json_directory(path):
    data = pd.DataFrame()
    files = []

    # r=root, d=directories, f = files
    # read the first 100 files
    for r, d, f in os.walk(path):
        for file in f:
            if '.json' in file:
                files.append(os.path.join(r, file))
            if len(files) > 100:
                break

    for f in files:
        print("reading: " + f)
        with open(f) as json_file:
            j = json_normalize(json.load(json_file))
            data = data.append(j, sort=True)

    return data


def split_train_data(data):
    train_data = data.sample(frac=0.8, random_state=0)
    return train_data


def split_test_data(data):
    train_data = split_train_data(data)
    test_data = data.drop(train_data.index)
    return test_data


def extract_mood_information(data):
    mood_data = data[mood_columns]
    return mood_data


def drop_mood_information(data):
    data = data.drop(columns=mood_columns)
    return data


def drop_mood_stats_information(data):
    data = data.drop(columns=mood_columns_stats)
    return data


def calc_feature_standards(data):
    train_stats = data.describe()
    train_stats = drop_mood_stats_information(train_stats)
    train_stats = train_stats.transpose()
    print('train_stats: ')
    print(train_stats)
    return train_stats


def norm(train_data, train_stats):
    # do not need to normalize string data
    train_data = train_data.select_dtypes(exclude=['object'])
    return (train_data - train_stats['mean']) / train_stats['std']


def build_model(data):
    model = Sequential([
        layers.Dense(64, activation='relu', input_shape=[len(data.keys())]),
        layers.Dense(64, activation='relu'),
        layers.Dense(1)
    ])

    optimizer = keras.optimizers.RMSprop(0.001)

    model.compile(loss='mse',
                  optimizer=optimizer,
                  metrics=['mae', 'mse'])

    return model


def model_data(data, norm_data):
    # investigate data
    sns.pairplot(
        data[['highlevel.danceability.value', 'highlevel.gender.all.female', 'highlevel.gender.all.male']],
        diag_kind="kde")
    plt.show()
    print(data.describe())

    model = build_model(data)
    model.summary()
    example_batch = norm_data[:10]
    example_result = model.predict(example_batch)
    print(example_result)


def main():
    # read files into pandas DataFrame
    highlvl_data = read_json_directory(
        'I:\Science\CIS\wyb15135\datasets_unmodified\\acousticbrainz-highlevel-json-20150130\highlevel\\0\\00')

    # Split data into training and testing data
    train_highlvl_data = split_train_data(highlvl_data)
    test_highlvl_data = split_test_data(highlvl_data)

    # normalize data
    train_stats = calc_feature_standards(train_highlvl_data)
    norm_train_highlvl_data = norm(train_highlvl_data, train_stats)
    norm_test_highlvl_data = norm(test_highlvl_data, train_stats)

    # extract labels, in this case mood
    train_mood_labels = extract_mood_information(train_highlvl_data)
    test_mood_labels = extract_mood_information(test_highlvl_data)

    # build and run model
    model_data(train_highlvl_data, norm_train_highlvl_data)


if __name__ == '__main__':
    main()
