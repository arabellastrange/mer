import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MultiLabelBinarizer, LabelEncoder
from sklearn.metrics import f1_score, classification_report
from sklearn.svm import LinearSVC

PATH_MOOD = 'I:\Science\CIS\wyb15135\datasets_created\datasets_created_ground_truth.csv'

PATH_TRUTH_HIGH = 'I:\Science\CIS\wyb15135\datasets_created\high_lvl_more_clustered_label_truth.csv'
PATH_TRUTH_LOW = 'I:\Science\CIS\wyb15135\datasets_created\low_lvl_more_clustered_label_truth.csv'

PATH_PREDICTED_H_SVM = 'I:\Science\CIS\wyb15135\datasets_created\high_lvl_predicted_svm_multiclass.csv'
PATH_PREDICTED_L_SVM = 'I:\Science\CIS\wyb15135\datasets_created\low_lvl_predicted_svm_multiclass.csv'
PATH_PREDICTED_H_RFOR = 'I:\Science\CIS\wyb15135\datasets_created\high_lvl_predicted_forest_multiclass.csv'
PATH_PREDICTED_L_RFOR = 'I:\Science\CIS\wyb15135\datasets_created\low_lvl_predicted_forest_multiclass.csv'

label_cols_all = ['airy', 'ambient', 'angry', 'animated', 'astonishing', 'big', 'bizarre', 'black', 'bleak', 'boisterous',
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
              'quiet', 'rapture', 'relaxed', 'repeated', 'repetitive', 'rich', 'reticent', 'sad', 'scary', 'serene',
              'sexy', 'silent',
              'slow', 'snappy', 'soft', 'somber', 'soothing', 'space', 'storming', 'strange', 'sunny', 'sweet',
              'traditional', 'trance', 'unconventional', 'upbeat', 'weighty', 'weird', 'wistful', 'zippy']
label_cols_min = ['ambient', 'angry', 'breezy', 'calm', 'cheerful', 'contented', 'dark',
       'delighted', 'ecstatic', 'elated', 'fast', 'fiery', 'funky', 'happy',
       'heated', 'heavy', 'jazzy', 'loud', 'melancholy', 'mellow', 'mournful',
       'passionate', 'quiet', 'relaxed', 'sad', 'serene', 'slow', 'soft',
       'space', 'storming', 'upbeat', 'weird', 'wistful']


def load_file(path):
    return pd.read_csv(path)


def process_data(data, flag='high'):
    data.drop(
        columns=['metadata.tags.musicbrainz_recordingid', 'metadata.tags.artist', 'metadata.tags.title',
                 'metadata.tags.album', 'title', 'artist', 'mood'], inplace=True, errors='ignore')

    if flag == 'high':
        data = process_high_data(data)
    if flag == 'low':
        data = process_low_data(data)

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
    return data


def model_low_high_features():
    data = load_file(PATH_TRUTH_LOW)
    data = process_data(data, flag='low')
    run_model(data)


def model_high_features():
    data = load_file(PATH_TRUTH_HIGH)
    data = process_data(data)
    run_model(data)


def run_model(data):
    # one-hot encoding mood classes

    Y = pd.get_dummies(data.pop('Cluster').astype(str))
    X = data.drop(columns=['id'])

    # scale x
    # X = StandardScaler().fit_transform(X)

    # split dataset
    x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.40, random_state=19)

    # data is scaled for SVM but not rand forest!
    sc_x = StandardScaler()
    s_x_train = sc_x.fit_transform(x_train)
    s_x_test = sc_x.fit_transform(x_test)

    rand_forest_model(data, x_train, y_train, x_test, y_test)
    svm_model(data, s_x_train, y_train, s_x_test, y_test)


def rand_forest_model(data, x_train, y_train, x_test, y_test):
    classifier = RandomForestClassifier(max_depth=32, n_estimators=100, class_weight='balanced')
    classifier.fit(x_train, y_train)
    y_pred = classifier.predict(x_test)

    y_pred_frame = pd.DataFrame(y_pred, columns=y_test.columns, index=y_test.index.copy())

    score = f1_score(y_test.values.argmax(axis=1), y_pred_frame.values.argmax(axis=1), average='micro')
    print('Score Forest: ')
    print(score)
    report = classification_report(y_test.values.argmax(axis=1), y_pred_frame.values.argmax(axis=1))
    print(report)

    # output
    df_out = pd.merge(data, y_pred_frame, left_index=True, right_index=True)

    # TODO CHANGE FILE FOR HIGH/LOW MODELS
    output_predictions_to_file(df_out, PATH_PREDICTED_H_RFOR)


def svm_model(data, x_train, y_train, x_test, y_test):
    # linear kernel for multi-class classification
    classifier = LinearSVC(C=1, multi_class='ovr', class_weight='balanced')
    classifier.fit(x_train, y_train)
    y_pred = classifier.predict(x_test)

    y_pred_frame = pd.DataFrame(y_pred, columns=y_test.columns, index=y_test.index.copy())

    score = f1_score(y_test.values.argmax(axis=1), y_pred_frame.values.argmax(axis=1), average='micro')
    print('Score SVM: ')
    print(score)
    report = classification_report(y_test.values.argmax(axis=1), y_pred_frame.values.argmax(axis=1))
    print(report)

    # merge on how='left' for all data, default for test data only
    df_out = pd.merge(data, y_pred, left_index=True, right_index=True)

    # TODO PATH CHANGES
    output_predictions_to_file(df_out, PATH_PREDICTED_H_SVM)


def output_predictions_to_file(data, file):
    data.to_csv(file, index=False)


def main():
    model_high_features()
    # model_low_high_features()


if __name__ == '__main__':
    main()
