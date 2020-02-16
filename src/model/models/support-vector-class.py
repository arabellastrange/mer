import ast
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import StandardScaler, MultiLabelBinarizer
from sklearn.metrics import f1_score, classification_report
from sklearn.svm import SVC

PATH_MOOD = 'I:\Science\CIS\wyb15135\datasets_created\datasets_created_ground_truth.csv'

PATH_TRUTH_HIGH = 'I:\Science\CIS\wyb15135\datasets_created\ground_truth_classification_high.csv'
PATH_TRUTH_HIGH_CLASS = 'I:\Science\CIS\wyb15135\datasets_created\ground_truth_classification_high_min_class.csv'
PATH_TRUTH_LOW = 'I:\Science\CIS\wyb15135\datasets_created\ground_truth_classification_high_low.csv'

PATH_PREDICTED_H_SVM = 'I:\Science\CIS\wyb15135\datasets_created\high_lvl_predicted_svm_class.csv'
PATH_PREDICTED_L_SVM = 'I:\Science\CIS\wyb15135\datasets_created\low_lvl_predicted_svm_class.csv'
PATH_PREDICTED_H_RFOR = 'I:\Science\CIS\wyb15135\datasets_created\high_lvl_predicted_forest_class.csv'

label_cols = ['airy', 'ambient', 'angry', 'animated', 'astonishing', 'big', 'bizarre', 'black', 'bleak', 'boisterous',
              'boring', 'breezy', 'bright', 'buoyant', 'calm', 'cheerful', 'cheery', 'choral', 'comfortable', 'complex',
              'constant', 'contented', 'contrasting', 'cool', 'curious', 'dark', 'daze', 'deafening', 'deep',
              'dejected', 'delicate', 'delighted', 'despondent', 'different', 'difficult', 'dim', 'distinctive',
              'dreamy', 'dull', 'earthy', 'easy', 'eccentric', 'ecstatic', 'ecstasy', 'eerie', 'elated', 'emphatic',
              'encouraging',
              'energetic', 'enveloping', 'extraordinary', 'familiar', 'fashionable', 'fast', 'fiery', 'flashy', 'fluid',
              'funky', 'gray', 'happy', 'hard', 'harmonious', 'heated', 'heavy', 'hip', 'hopeful', 'jazzy', 'light',
              'lively', 'loud', 'low', 'luminous', 'melancholy', 'mellow', 'mild', 'modish', 'monotonous', 'mournful',
              'muted', 'odd', 'old', 'operatic', 'orchestral', 'passionate', 'peaceful', 'peculiar', 'profound',
              'quick',
              'quiet', 'rapture', 'relaxed', 'repeated' ,'repetitive', 'rich', 'reticent', 'sad', 'scary', 'serene',
              'sexy','silent',
              'slow', 'snappy', 'soft', 'somber', 'soothing', 'space', 'storming', 'strange', 'sunny', 'sweet',
              'traditional', 'trance', 'unconventional', 'upbeat', 'weighty', 'weird', 'wistful', 'zippy']


def load_file(path):
    return pd.read_csv(path)


def process_data(data, flag='high'):
    data = data.drop(columns=label_cols, errors='ignore')

    data_mood = load_file(PATH_MOOD)
    data_mood['mood'] = data_mood['mood'].apply(ast.literal_eval)
    data = pd.merge(data, data_mood[['mood', 'title', 'artist']], on=['title', 'artist'])

    data.drop(
        columns=['metadata.tags.musicbrainz_recordingid', 'metadata.tags.artist', 'metadata.tags.title',
                 'metadata.tags.album', 'title', 'artist', 'fallback-id'], inplace=True)

    # drop uncommon mood tags
    for i, row in data.iterrows():
        for m_tag in get_uncommon_tags(data['mood']):
            if m_tag in row['mood']:
                row['mood'].remove(m_tag)
        print('updating row: {:d}'.format(i))
        data.at[i, 'mood'] = row['mood']

    if flag == 'high':
        data = process_high_data(data)
    if flag == 'low':
        data = process_low_data(data)

    data.to_csv(PATH_TRUTH_HIGH_CLASS, index=False)
    return data


def process_low_data(data):
    mlb_scale = MultiLabelBinarizer()
    mlb_key = MultiLabelBinarizer()
    mlb_chord = MultiLabelBinarizer()

    data = data.join(
        pd.DataFrame(mlb_scale.fit_transform(data.pop('tonal.key_scale').astype(str)), columns=mlb_scale.classes_,
                     index=data.index))
    data = data.join(
        pd.DataFrame(mlb_chord.fit_transform(data.pop('tonal.chords_scale').astype(str)), columns=mlb_chord.classes_,
                     index=data.index))
    data = data.join(
        pd.DataFrame(mlb_key.fit_transform(data.pop('tonal.key_key').astype(str)), columns=mlb_key.classes_,
                     index=data.index))

    return data


def process_high_data(data):
    # get rid of empty row after dropping sparse classes
    for i, row in data.iterrows():
        if row['mood'] == '' or row['mood'] == 'fast' or row['mood'] == 'slow':
            data.drop(i)

    return data


# modify prediction function to offset issues with sparse labels
# assign only the tags with the highest confidence
def get_best_tags(clf, X, lb, n_tags=3):
    decfun = clf.decision_function(X)
    best_tags = np.argsort(decfun)[:, :-(n_tags + 1): -1]
    return lb.classes_[best_tags]


def get_uncommon_tags(mood_array):
    mood_array = mood_array.apply(pd.Series).stack().value_counts()
    mood_array = mood_array[mood_array < 50]

    return mood_array.keys()


def model_low_high_features():
    data = load_file(PATH_TRUTH_LOW)
    data = process_data(data, flag='low')
    run_model(data)


def model_high_features():
    data = load_file(PATH_TRUTH_HIGH)
    data = process_data(data)
    data['mood'] = data['mood'].apply(ast.literal_eval)
    run_model(data)


def run_model(data):
    h = .02  # step size in the mesh

    # one-hot encoding mood classes
    mlb = MultiLabelBinarizer()
    Y = pd.DataFrame(mlb.fit_transform(data.pop('mood')), columns=mlb.classes_, index=data.index)
    X = data.drop(columns=['id'])

    # scale x
    X = StandardScaler().fit_transform(X)

    # split dataset
    x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.40, random_state=19)
    svm_model(x_train, y_train, x_test, y_test, mlb)
    rand_forest_model(x_train,y_train,x_test,y_test, mlb)


def rand_forest_model(x_train, y_train, x_test, y_test, mlb):
    classifier = RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1)
    classifier.fit(x_train, y_train)

    y_pred = mlb.inverse_transform(classifier.predict(x_test))
    print(y_pred[:5])

    output_predictions_to_file(x_test, y_pred, PATH_PREDICTED_H_RFOR)
    y_pred_frame = pd.DataFrame(mlb.transform(y_pred), columns=mlb.classes_)

    score = f1_score(y_test.values.argmax(axis=1), y_pred_frame.values.argmax(axis=1), average='micro')
    print('Score Forest: ')
    print(score)
    report = classification_report(y_test.values.argmax(axis=1), y_pred_frame.values.argmax(axis=1))
    print(report)


def svm_model(x_train, y_train, x_test, y_test, mlb):
    # model "RBF SVM"
    classifier = OneVsRestClassifier(SVC(kernel='rbf', gamma=0.1, C=1))
    classifier.fit(x_train, y_train)

    # predict, make Confusion Matrix and score
    y_pred = mlb.inverse_transform(classifier.predict(x_test))
    print(y_pred[:5])

    output_predictions_to_file(x_test, y_pred, PATH_PREDICTED_H_SVM)
    y_pred_frame = pd.DataFrame(mlb.transform(y_pred), columns=mlb.classes_)

    # flatten y predicted data frames to array
    # c_matrix = multilabel_confusion_matrix(y_test.values, y_pred_frame.values)
    # print(c_matrix)

    score = f1_score(y_test.values.argmax(axis=1), y_pred_frame.values.argmax(axis=1), average='micro')
    print('Score SVM: ')
    print(score)
    report = classification_report(y_test.values.argmax(axis=1), y_pred_frame.values.argmax(axis=1))
    print(report)


def output_predictions_to_file(x , y, file):
    predictions_frame = pd.DataFrame(y, columns='mood')
    predictions = x.join(predictions_frame)
    predictions.to_csv(file, index=False)


def main():
    model_high_features()
    # model_low_high_features()


if __name__ == '__main__':
    main()
