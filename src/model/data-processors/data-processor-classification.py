import ast
import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer
import requests
from bs4 import BeautifulSoup

PATH_TRUTH = 'I:\Science\CIS\wyb15135\datasets_created\datasets_created_ground_truth.csv'
PATH_CLASS = 'I:\Science\CIS\wyb15135\datasets_created\ground_truth_classification.csv'
PATH_ID = 'I:\Science\CIS\wyb15135\datasets_created\ground_truth_classification_id.csv'

Synonyms = {'weird': ['curious', 'eccentric', 'eerie'], 'ambient': ['fluid', 'enveloping'],
            'quiet': ['muted', 'peaceful', 'reticent', 'silent', 'soft'],
            'old': ['familiar', 'traditional', 'gray'],
            'happy': ['cheerful', 'contented', 'delighted', 'ecstatic', 'elated'],
            'trance': ['rapture', 'daze', 'dreamy', 'ecstasy'],
            'jazzy': ['flashy', 'lively', 'sexy', 'zippy', 'animated'],
            'soft': ['comfortable', 'delicate', 'easy'],
            'heavy': ['dark', 'melancholy', 'weighty', 'despondent'],
            'funky': ['earthy', 'fashionable', 'hip', 'modish', 'unconventional'],
            'strange': ['astonishing', 'bizarre', 'curious', 'different', 'extraordinary'],
            'upbeat': ['buoyant', 'cheery', 'encouraging', 'happy', 'hopeful'],
            'different': ['contrasting', 'distinctive', 'peculiar', 'weird'],
            'light': ['bright', 'luminous', 'rich', 'sunny'],
            'space': ['eccentric', 'strange', 'odd'],
            'dark': ['black', 'dim', 'bleak', 'somber'],
            'deep': ['profound', 'complex', 'heavy', 'rich'],
            'calm': ['cool', 'harmonious', 'relaxed', 'mild'],
            'mellow': ['delicate', 'relaxed', 'soft', 'soothing', 'sweet'],
            'hard': ['difficult', 'heavy', 'complex'],
            'low': ['dejected', 'melancholy', 'despondent'],
            'quick': ['energetic', 'upbeat', 'snappy'],
            'angry': ['heated', 'passionate','storming','fiery'],
            'sad': ['melancholy', 'mournful', 'heavy', 'wistful'],
            'relaxed': ['breezy', 'calm', 'mellow', 'serene']}


def load_file(path):
    return pd.read_csv(path)


def get_synonym(word):
    if word not in Synonyms:
        response = requests.get('http://www.thesaurus.com/browse/{}'.format(word))
        soup = BeautifulSoup(response.text, 'html')
        section = soup.find('section', {'class': 'e1991neq0'})
        synonyms = [span.text for span in section.findAll('span')]

        if 'Synonyms' in synonyms[0]:
            synonyms.pop(0)

        Synonyms[word] = synonyms[0:5]

    return Synonyms[word]


def format_class_data(data):
    # drop arousal and valence
    # drop only fast and slow tags
    # split mood tags to separate columns for one-hot encoding
    # merge with id'd songs
    for i, row in data.iterrows():
        if row['mood'] == ['slow'] or row['mood'] == ['fast'] or row['mood'] == ['chorus'] or row['mood'] == ['opera'] \
                or row['mood'] == ['orchestra']:
            data = data.drop(i)
        elif 'slow' in row['mood'] and 'fast' in row['mood']:
            # if song is tagged with both slow and fast then drop both tags
            row['mood'].remove('fast')
            row['mood'].remove('slow')
            data.at[i, 'mood'] = row['mood']
        elif 'orchestra' in row['mood']:
            row['mood'].remove('orchestra')
            row['mood'].append('orchestral')
            data.at[i, 'mood'] = row['mood']
        elif 'chorus' in row['mood']:
            row['mood'].remove('chorus')
            row['mood'].append('choral')
            data.at[i, 'mood'] = row['mood']
        elif 'opera' in row['mood']:
            row['mood'].remove('opera')
            row['mood'].append('operatic')
            data.at[i, 'mood'] = row['mood']
        else:
            # expand singleton lists with synonyms
            if len(row['mood']) == 1:
                similar = get_synonym(row['mood'][0])
                if similar:
                    data.at[i, 'mood'] = row['mood'] + similar
            if len(row['mood']) == 0:
                # drop rows with empty tags
                data = data.drop(i)

    print(data.head())
    return data


def encode_moods(data):
    # use sci-learn for one hot encoding
    mlb = MultiLabelBinarizer()
    data = data.join(pd.DataFrame(mlb.fit_transform(data.pop('mood')), columns=mlb.classes_, index=data.index))
    return data


def merge_w_id(d_class, d_id):
    d_class = d_class.merge(d_id[['artist', 'title', 'id', 'fallback-id']], left_on=['artist', 'title'], right_on=['artist', 'title'],
                            how='left')
    return d_class


def main():
    # input
    # d_truth = load_file(PATH_TRUTH)
    d_class = load_file(PATH_CLASS)
    d_id = load_file(PATH_ID)

    # read string rep of lists as lists
    # d_truth['mood'] = d_truth['mood'].apply(ast.literal_eval)
    # d_truth = format_class_data(d_truth)
    d_class = merge_w_id(d_class, d_id)

    # output with mood list
    # d_truth.to_csv(PATH_TRUTH, index=False)

    # output encoded moods
    # d_truth = d_truth.drop(columns=['arousal', 'valence'])
    # d_truth = encode_moods(d_truth)
    # d_truth.to_csv(PATH_CLASS, index=False)

    d_class.to_csv(PATH_ID, index=False)


if __name__ == '__main__':
    main()
