import ast

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import ListedColormap
from sklearn.model_selection import train_test_split
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler, MultiLabelBinarizer
from sklearn.metrics import confusion_matrix, f1_score
from sklearn.svm import SVC

PATH_MOOD = 'I:\Science\CIS\wyb15135\datasets_created\datasets_created_ground_truth.csv'
PATH_TRUTH = 'I:\Science\CIS\wyb15135\datasets_created\ground_truth_classification_high.csv'
PATH_PREDICTED_SVM = 'I:\Science\CIS\wyb15135\datasets_created\high_lvl_predicted_svm_class.csv'

# dropped: 'ecstasy', 'repeated', 'reticent'
label_cols = ['airy', 'ambient', 'angry', 'animated', 'astonishing', 'big', 'bizarre', 'black', 'bleak', 'boisterous',
              'boring', 'breezy', 'bright', 'buoyant', 'calm', 'cheerful', 'cheery', 'choral', 'comfortable', 'complex',
              'constant', 'contented', 'contrasting', 'cool', 'curious', 'dark', 'daze', 'deafening', 'deep',
              'dejected','delicate', 'delighted', 'despondent', 'different', 'difficult', 'dim', 'distinctive',
              'dreamy', 'dull', 'earthy','easy', 'eccentric', 'ecstatic', 'eerie', 'elated', 'emphatic', 'encouraging',
              'energetic', 'enveloping', 'extraordinary', 'familiar', 'fashionable', 'fast', 'fiery', 'flashy', 'fluid',
              'funky', 'gray', 'happy', 'hard', 'harmonious', 'heated', 'heavy', 'hip', 'hopeful', 'jazzy', 'light',
              'lively','loud', 'low', 'luminous', 'melancholy', 'mellow', 'mild', 'modish', 'monotonous', 'mournful',
              'muted','odd','old', 'operatic', 'orchestral', 'passionate', 'peaceful', 'peculiar', 'profound', 'quick',
              'quiet','rapture', 'relaxed', 'repetitive', 'rich', 'sad', 'scary', 'serene', 'sexy', 'silent',
              'slow', 'snappy','soft', 'somber', 'soothing', 'space', 'storming', 'strange', 'sunny', 'sweet',
              'traditional', 'trance', 'unconventional', 'upbeat', 'weighty', 'weird', 'wistful', 'zippy']
h = .02  # step size in the mesh


def load_file(path):
    return pd.read_csv(path)


def process_data(data):
    data = data.drop(columns=label_cols)
    data_mood = load_file(PATH_MOOD)
    data_mood['mood'] = data_mood['mood'].apply(ast.literal_eval)

    data = pd.merge(data, data_mood[['mood', 'title', 'artist']], on=['title', 'artist'])

    data.drop(
        columns=['metadata.tags.musicbrainz_recordingid', 'metadata.tags.artist', 'id', 'metadata.tags.title',
                 'metadata.tags.album', 'title', 'artist'], inplace=True)

    # encode string data
    # artist_encoder = LabelEncoder()
    # data['artist'] = artist_encoder.fit_transform(data['artist'].astype(str))
    # title_encoder = LabelEncoder()
    # data['title'] = title_encoder.fit_transform(data['title'].astype(str))

    return data


# modify prediction function to offset issues with sparse labels
# assign only the tags with the highest confidence
def get_best_tags(clf, X, lb, n_tags=3):
    decfun = clf.decision_function(X)
    best_tags = np.argsort(decfun)[:, :-(n_tags+1): -1]
    return lb.classes_[best_tags]


def main():
    data = load_file(PATH_TRUTH)
    data = process_data(data)

    # one-hot encoding mood classes
    mlb = MultiLabelBinarizer()
    Y = pd.DataFrame(mlb.fit_transform(data.pop('mood')),  columns=mlb.classes_, index=data.index)
    X = data

    # scale x
    X = StandardScaler().fit_transform(X)

    # split dataset
    x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.33, random_state=19)

    # plotting for decision functions
    # x_min, x_max = x_train[:, 0].min() - .5, x_train[:, 0].max() + .5
    # y_min, y_max = x_train[:, 1].min() - .5, x_train[:, 1].max() + .5
    # xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
    #                     np.arange(y_min, y_max, h))

    # plot input
    # cm = plt.cm.RdBu
    # cm_bright = ListedColormap(['#FF0000', '#0000FF'])
    # plt.scatter(x_train[:, 0], x_train[:, 1], c='y', cmap=cm_bright,
    #            edgecolors='k')
    # plt.scatter(x_test[:, 0], x_test[:, 1], c='m', cmap=cm_bright, alpha=0.6,
    #            edgecolors='k')

    # plt.show()

    # model "RBF SVM"
    classifier = OneVsRestClassifier(SVC(kernel='rbf', gamma=0.1, C=1))
    classifier.fit(x_train, y_train)

    # Plot the decision boundary.
    # if hasattr(classifier, "decision_function"):
        # Z = classifier.decision_function(x_test)
    #    Z = classifier.decision_function(np.c_[xx.ravel(), yy.ravel()])

    # Z = Z.reshape(xx.shape)
    # plt.contourf(xx, yy, Z, cmap=cm, alpha=.8)
    # Plot the training points
    # plt.scatter(x_train[:, 0], x_train[:, 1], c='g', cmap=cm_bright,
    #            edgecolors='k')
    # Plot the testing points
    # plt.scatter(x_test[:, 0], x_test[:, 1], c='r', cmap=cm_bright,
    #            edgecolors='k', alpha=0.6)
    # plt.show()

    # predict, make Confusion Matrix and score
    mlb.inverse_transform(classifier.predict(x_test))
    y_pred = get_best_tags(classifier, x_test, mlb)
    print(y_pred)

    c_matrix = confusion_matrix(y_test.argmax(axis=1), classifier.predict(x_test).argmax(axis=1))
    print(c_matrix)

    score = f1_score(y_test, classifier.predict(x_test))
    print('Score: ')
    print(score)

    # predictions = classifier.predict(x_test).flatten()
    # predictions_frame = DataFrame(predictions, columns='mood')
    # predictions_frame = x_test.join(predictions_frame)
    # predictions['artist'] = artist_encoder.inverse_transform(predictions['artist'])
    # predictions['title'] = title_encoder.inverse_transform(predictions['title'])

    # predictions = pd.merge(data, predictions, on=['title', 'artist'])
    # predictions.to_csv(PATH_PREDICTED_SVM, index=False)


if __name__ == '__main__':
    main()
