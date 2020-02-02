import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.datasets import make_multilabel_classification
from sklearn.multiclass import OneVsRestClassifier
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC

PATH_TRUTH = 'I:\Science\CIS\wyb15135\datasets_created\\formatted_high_lvl_ground_truth.csv'
PATH_PREDICTED_SVM = 'I:\Science\CIS\wyb15135\datasets_created\high_lvl_predicted_svm_class.csv'
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


def main():
    data = load_file(PATH_TRUTH)
    data = data.drop(
        columns=['metadata.tags.musicbrainz_recordingid', 'metadata.tags.artist', 'id', 'metadata.tags.title',
                 'metadata.tags.album'])

    # encode string data
    artist_encoder = LabelEncoder()
    data['artist'] = artist_encoder.fit_transform(data['artist'].astype(str))
    title_encoder = LabelEncoder()
    data['title'] = title_encoder.fit_transform(data['title'].astype(str))

    Y = data[label_cols]
    X = data.drop(columns=label_cols)

    # split dataset
    x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.33, random_state=19)

    # model
    mlb = MultiLabelBinarizer()
    mlb_fitted = mlb.fit_transform(y_train)

    classifier = OneVsRestClassifier(SVC(kernel='rbf'))
    classifier.fit(x_train,y_train)

    # predict
    predictions = classifier.predict(x_test)
    all_labels = mlb.inverse_transform(predictions)


if __name__ == '__main__':
    main()

