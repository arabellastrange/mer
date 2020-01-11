import pandas as pd
from sklearn.svm import SVR
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt

PATH_TRUTH = 'I:\Science\CIS\wyb15135\datasets_created\ground_truth_high.csv'


def load_file(path):
    return pd.read_csv(path)


def main():
    # predict valence from arousal in ground truth - example regessor
    data = load_file(PATH_TRUTH)

    data = data.drop(
        columns=['mood', 'metadata.tags.musicbrainz_recordingid', 'artist', 'title', 'id', 'metadata.tags.genre',
                 'metadata.tags.artist credit', 'metadata.audio_properties.sample_rate', 'metadata.tags.bpm'])

    Y = data[['valence', 'arousal']]
    X = data.drop(columns=['valence', 'arousal'])

    # encode string labels as ints
    title_encoder = LabelEncoder()
    artist_encoder = LabelEncoder()
    X['metadata.tags.artist'] = artist_encoder.fit_transform(X['metadata.tags.artist'].astype(str))
    X['metadata.tags.title'] = title_encoder.fit_transform(X['metadata.tags.title'].astype(str))

    # split data set into train and test sets
    x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.30, random_state=10)

    sc_X = StandardScaler()
    sc_Y = StandardScaler()

    X = sc_X.fit_transform(x_train)
    Y= sc_Y.fit_transform(y_train)

    # model
    regressor = SVR(kernel='rbf')
    regressor.fit(X, Y)

    # predict
    prediction = regressor.predict(x_test)

    print("Accuracy: ")
    print(r2_score(y_test.values.reshape(-1, 1), prediction))

    # output prediction to file

    # visualise data
    plt.scatter(x_train, y_train, color='magenta')
    plt.plot(x_test, regressor.predict(x_test), color='green')
    plt.title('Predicted Arousal Valence (Support Vector Regression Model)')
    plt.ylabel('Arousal - Valence')
    plt.show()


if __name__ == '__main__':
    main()
