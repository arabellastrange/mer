import pandas as pd
from sklearn.svm import SVR
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt

PATH_TRUTH = 'I:\Science\CIS\wyb15135\datasets_created\\formatted_high_lvl_ground_truth.csv'


def load_file(path):
    return pd.read_csv(path)


def main():
    # predict valence from arousal in ground truth - example regessor
    data = load_file(PATH_TRUTH)

    data = data.drop(
        columns=['mood', 'metadata.tags.musicbrainz_recordingid', 'metadata.tags.artist', 'title', 'id',
                 'metadata.tags.title', 'metadata.tags.album', 'metadata.audio_properties.length',
                 'metadata.audio_properties.replay_gain', 'metadata.audio_properties.equal_loudness',
                 'metadata.audio_properties.bit_rate', 'metadata.audio_properties.analysis_sample_rate'])

    Y_valence = data['valence']
    print('Y: ')
    print(Y_valence.head())

    Y_arousal = data['arousal']

    X = data.drop(columns=['valence', 'arousal'])
    print('X: ')
    print(X.head())

    # encode string labels as ints
    artist_encoder = LabelEncoder()
    X['artist'] = artist_encoder.fit_transform(X['artist'].astype(str))
    print('Encoded X: ')
    print(X.head())

    # split data set into train and test sets
    x_train_v, x_test_v, y_train_v, y_test_v = train_test_split(X, Y_valence, test_size=0.33, random_state=19)
    x_train_a, x_test_a, y_train_a, y_test_a = train_test_split(X, Y_arousal, test_size=0.33, random_state=19)

    # model - uses Radial Basis Function (RBF)
    # the gamma parameter defines how far the influence of a single training example reaches, with low values meaning
    # ‘far’ and high values meaning ‘close’.
    # For larger values of C, a smaller margin [of error] will be accepted if the decision function is better at
    # classifying all training points correctly.
    regressor_v = SVR(kernel='rbf', gamma=0.1, C=1.0)
    regressor_v = regressor_v.fit(x_train_v, y_train_v)

    regressor_a = SVR(kernel='rbf', gamma=0.1, C=1.0)
    regressor_a = regressor_a.fit(x_train_a, y_train_a)

    # predict
    prediction_v = regressor_v.predict(x_test_v)
    prediction_a = regressor_a.predict(x_test_a)

    print("Accuracy Valence: ")
    print(r2_score(y_test_v.values.reshape(-1, 1), prediction_v))

    print("Accuracy Arousal: ")
    print(r2_score(y_test_a.values.reshape(-1, 1), prediction_a))

    # output prediction to file

    # visualise data
    plt.scatter(x_test_v['highlevel.gender.all.female'], y_test_v, color='magenta')
    plt.scatter(x_test_v['highlevel.gender.all.female'], prediction_v, color='green')
    plt.title('Predicted Valence (Support Vector Regression Model)')
    plt.ylabel('Valence')
    plt.xlabel('Female Vocalist Probability')
    plt.show()

    plt.scatter(x_test_a['highlevel.danceability.all.danceable'], y_test_a, color='magenta')
    plt.scatter(x_test_a['highlevel.danceability.all.danceable'], prediction_a, color='green')
    plt.title('Predicted Arousal (Support Vector Regression Model)')
    plt.ylabel('Arousal')
    plt.xlabel('Danceability')
    plt.show()


if __name__ == '__main__':
    main()
