import pandas as pd
from sklearn.svm import SVR
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
import numpy as np

PATH_TRUTH = 'I:\Science\CIS\wyb15135\datasets_created\\formatted_high_lvl_ground_truth.csv'


def load_file(path):
    return pd.read_csv(path)


def main():
    # predict valence from arousal in ground truth - example regessor
    data = load_file(PATH_TRUTH)

    data = data.drop(
        columns=['mood', 'metadata.tags.musicbrainz_recordingid', 'metadata.tags.artist', 'title', 'id',
                 'metadata.tags.title', 'metadata.tags.album'])

    Y_valence = data['valence']
    print(Y_valence.head())
    Y_arousal = data['arousal']
    X = data.drop(columns=['valence', 'arousal'])
    print(X.head())

    # encode string labels as ints
    artist_encoder = LabelEncoder()
    X['artist'] = artist_encoder.fit_transform(X['artist'].astype(str))

    # split data set into train and test sets
    x_train_v, x_test_v, y_train_v, y_test_v = train_test_split(X, Y_valence, test_size=0.33, random_state=19)
    x_train_a, x_test_a, y_train_a, y_test_a = train_test_split(X, Y_arousal, test_size=0.33, random_state=19)

    sc_XV = StandardScaler()
    sc_XA = StandardScaler()
    sc_YV = StandardScaler()
    sc_YA = StandardScaler()

    X_valence = sc_XV.fit_transform(x_train_v)
    X_arousal = sc_XA.fit_transform(x_train_a)
    Y_valence = np.array(y_train_v).reshape(-1,1)
    Y_arousal = np.array(y_train_a).reshape(-1,1)

    Y_valence = sc_YV.fit_transform(Y_valence)
    Y_arousal = sc_YA.fit_transform(Y_arousal)

    # model
    regressor_v = SVR(kernel='rbf')
    regressor_v.fit(X_valence, Y_valence)

    regressor_a = SVR(kernel='rbf')
    regressor_a.fit(X_arousal, Y_arousal)

    # predict
    prediction_v = regressor_v.predict(x_test_v)
    prediction_a = regressor_a.predict(x_test_a)

    print("Accuracy Valence: ")
    print(r2_score(y_test_v.values.reshape(-1, 1), prediction_v))

    print("Accuracy Arousal: ")
    print(r2_score(y_test_a.values.reshape(-1, 1), prediction_a))

    # output prediction to file

    # visualise data
    plt.scatter(x_train_v['highlevel.danceability.all.danceable'], y_train_v, color='magenta')
    plt.plot(x_test_v['highlevel.danceability.all.danceable'], regressor_v.predict(x_test_v), color='green')
    plt.title('Predicted Valence (Support Vector Regression Model)')
    plt.ylabel('Valence')
    plt.xlabel('Danceability')
    plt.show()


if __name__ == '__main__':
    main()
