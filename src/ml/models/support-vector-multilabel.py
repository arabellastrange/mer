import ast
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import StandardScaler, MultiLabelBinarizer, LabelEncoder
from sklearn.metrics import f1_score, classification_report
from sklearn.svm import SVC

PATH_MOOD = 'I:\Science\CIS\wyb15135\datasets_created\datasets_created_ground_truth.csv'

PATH_TRUTH_HIGH = 'I:\Science\CIS\wyb15135\datasets_created\ground_truth_classification_high.csv'
PATH_TRUTH_HIGH_CLASS = 'I:\Science\CIS\wyb15135\datasets_created\ground_truth_classification_high_min_class.csv'
PATH_TRUTH_LOW = 'I:\Science\CIS\wyb15135\datasets_created\ground_truth_classification_high_low.csv'
PATH_TRUTH_LOW_CLASS = 'I:\Science\CIS\wyb15135\datasets_created\ground_truth_classification_low_min_class.csv'

PATH_PREDICTED_H_SVM = 'I:\Science\CIS\wyb15135\datasets_created\high_lvl_predicted_svm_class.csv'
PATH_PREDICTED_L_SVM = 'I:\Science\CIS\wyb15135\datasets_created\low_lvl_predicted_svm_class.csv'
PATH_PREDICTED_H_RFOR = 'I:\Science\CIS\wyb15135\datasets_created\high_lvl_predicted_forest_class.csv'
PATH_PREDICTED_L_RFOR = 'I:\Science\CIS\wyb15135\datasets_created\low_lvl_predicted_forest_class.csv'

PATH_HTRUTH = 'I:\Science\CIS\wyb15135\datasets_created\high_lvl_test_data'
PATH_LTRUTH = 'I:\Science\CIS\wyb15135\datasets_created\low_lvl_test_data'

label_cols_min = ['ambient', 'angry', 'breezy', 'calm', 'cheerful', 'contented', 'dark',
       'delighted', 'ecstatic', 'elated', 'fast', 'fiery', 'funky', 'happy',
       'heated', 'heavy', 'jazzy', 'loud', 'melancholy', 'mellow', 'mournful',
       'passionate', 'quiet', 'relaxed', 'sad', 'serene', 'slow', 'soft',
       'space', 'storming', 'upbeat', 'weird', 'wistful']


def load_file(path):
    return pd.read_csv(path)


def process_data(data, flag='high'):
    data = data.drop(columns=label_cols_min, errors='ignore')
    data_mood = load_file(PATH_MOOD)
    data_mood['mood'] = data_mood['mood'].apply(ast.literal_eval)

    data = pd.merge(data, data_mood[['mood', 'title', 'artist']], on=['title', 'artist'])
    data.drop(
        columns=['metadata.tags.musicbrainz_recordingid', 'metadata.tags.artist', 'metadata.tags.title',
                 'metadata.tags.album', 'title', 'artist', 'fallback-id'], inplace=True, errors='ignore')

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
        data = data.dropna(axis=0, how='any')
        data = process_low_data(data)

    # TODO CHANGE PATH
    data.to_csv(PATH_TRUTH_LOW_CLASS, index=False)
    return data


def process_low_data(data):
    lb_scale = LabelEncoder()
    lb_scale.fit(['major', 'minor'])
    lb_key = LabelEncoder()
    lb_key.fit(['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#'])

    data['tonal.key_scale'] = data['tonal.key_scale'].astype(str)
    data['tonal.chords_scale'] = data['tonal.chords_scale'].astype(str)
    data['tonal.chords_key'] = data['tonal.chords_key'].astype(str)
    data['tonal.key_key'] = data['tonal.key_key'].astype(str)

    data['tonal.key_scale'] = lb_scale.transform(data['tonal.key_scale'])
    data['tonal.chords_scale'] = lb_scale.transform(data['tonal.chords_scale'])
    data['tonal.key_key'] = lb_key.transform(data['tonal.key_key'])
    data['tonal.chords_key'] = lb_key.transform(data['tonal.chords_key'])

    return data


def process_high_data(data):
    # get rid of empty row after dropping sparse classes
    for i, row in data.iterrows():
        if row['mood'] == '' or row['mood'] == 'fast' or row['mood'] == 'slow':
            data = data.drop(i)
    return data


def get_uncommon_tags(mood_array):
    mood_array = mood_array.apply(pd.Series).stack().value_counts()
    mood_array = mood_array[mood_array < 50]
    return mood_array.keys()


def model_low_high_features():
    data = load_file(PATH_TRUTH_LOW_CLASS)
    data['mood'] = data['mood'].apply(ast.literal_eval)
    run_model(data)


def model_high_features():
    data = load_file(PATH_TRUTH_HIGH_CLASS)
    data['mood'] = data['mood'].apply(ast.literal_eval)
    run_model(data)


def run_model(data):
    # one-hot encoding mood classes
    mlb = MultiLabelBinarizer()
    Y = pd.DataFrame(mlb.fit_transform(data.pop('mood')), columns=mlb.classes_, index=data.index)
    X = data.drop(columns=['id'])

    # scale x
    # X = StandardScaler().fit_transform(X)

    # split dataset
    x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.40, random_state=19)

    # data is scaled for SVM but not rand forest!
    sc_x = StandardScaler()
    s_x_train = sc_x.fit_transform(x_train)
    s_x_test = sc_x.fit_transform(x_test)

    svm_model(data, s_x_train, y_train, s_x_test, y_test, x_test, mlb)
    rand_forest_model(data, x_train, y_train, x_test, y_test, x_test, mlb)


def rand_forest_model(data, x_train, y_train, x_test, y_test, d_test, mlb):
    classifier = RandomForestClassifier(max_depth=32, n_estimators=100, class_weight='balanced')
    classifier.fit(x_train, y_train)
    y_pred = classifier.predict(x_test)

    y_pred_frame = pd.DataFrame(y_pred, columns=mlb.classes_, index=d_test.index.copy())

    score = f1_score(y_test.values.argmax(axis=1), y_pred_frame.values.argmax(axis=1), average='micro')
    print('Score Forest: ')
    print(score)
    report = classification_report(y_test.values.argmax(axis=1), y_pred_frame.values.argmax(axis=1))
    print(report)

    # Random control playlists
    random_predictions = []
    for i in range(0, 1068):
        # gen 33 rand bin ints
        bin_array = np.random.randint(0, 1, 33)
        random_predictions.append(bin_array)

    y_rand_frame = pd.DataFrame(random_predictions, columns=mlb.classes_, index=d_test.index.copy())
    rand_score = f1_score(y_test.values.argmax(axis=1), y_rand_frame.values.argmax(axis=1), average='micro')
    print('Rand Score Forest: ')
    print(rand_score)
    rand_report = classification_report(y_test.values.argmax(axis=1), y_rand_frame.values.argmax(axis=1))
    print(rand_report)

    # output
    df_out = pd.merge(data, y_pred_frame, left_index=True, right_index=True)

    # TODO CHANGE FILE FOR HIGH/LOW MODELS
    # output_predictions_to_file(df_out, PATH_PREDICTED_L_RFOR)


def svm_model(data, x_train, y_train, x_test, y_test, d_test, mlb):
    # ml "RBF SVM"
    classifier = OneVsRestClassifier(SVC(kernel='poly', gamma=0.1, C=1, degree=4, class_weight='balanced'))
    classifier.fit(x_train, y_train)
    y_pred = classifier.predict(x_test)

    y_pred_frame = pd.DataFrame(y_pred, columns=mlb.classes_, index=d_test.index.copy())
    score = f1_score(y_test.values.argmax(axis=1), y_pred_frame.values.argmax(axis=1), average='micro')
    print('Score SVM: ')
    print(score)
    report = classification_report(y_test.values.argmax(axis=1), y_pred_frame.values.argmax(axis=1))
    print(report)

    # Random control playlists
    random_predictions = []
    for i in range(0, 1068):
        # gen 33 rand bin ints
        bin_array = np.random.randint(0, 1, 33)
        random_predictions.append(bin_array)

    y_rand_frame = pd.DataFrame(random_predictions, columns=mlb.classes_, index=d_test.index.copy())
    rand_score = f1_score(y_test.values.argmax(axis=1), y_rand_frame.values.argmax(axis=1), average='micro')
    print('Rand Score SVM: ')
    print(rand_score)
    rand_report = classification_report(y_test.values.argmax(axis=1), y_rand_frame.values.argmax(axis=1))
    print(rand_report)

    # merge on how='left' for all data, default for test data only
    df_out = pd.merge(data, y_pred_frame, left_index=True, right_index=True)

    # TODO PATH CHANGES
    # output_predictions_to_file(df_out, PATH_PREDICTED_L_SVM)


def output_predictions_to_file(data, file):
    data.to_csv(file, index=False)


def main():
    # model_high_features()
    model_low_high_features()


if __name__ == '__main__':
    main()
