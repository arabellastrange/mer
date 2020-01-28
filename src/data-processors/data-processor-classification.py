import ast
import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer
import requests
from bs4 import BeautifulSoup

PATH_TRUTH = 'I:\Science\CIS\wyb15135\datasets_created\datasets_created_ground_truth.csv'
PATH_CLASS = 'I:\Science\CIS\wyb15135\datasets_created\ground_truth_classification.csv'
PATH_ID = 'I:\Science\CIS\wyb15135\datasets_created\\formatted_high_lvl_ground_truth.csv'
Synonyms = {}


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
    data = data.drop(columns=['arousal', 'valence'])
    for i, row in data.iterrows():
        if row['mood'] == ['slow'] or row['mood'] == ['fast'] or row['mood'] == ['chorus'] or row['mood'] == ['opera']:
            data = data.drop(i)
        elif 'slow' in row['mood'] and 'fast' in row['mood']:
            # if song is tagged with both slow and fast then drop both tags
            row['mood'].remove('fast')
            row['mood'].remove('slow')
            data.at[i, 'mood'] = row['mood']
        else:
            # expand singleton lists with synonyms
            if len(row['mood']) == 1:
                similar = get_synonym(row['mood'][0])
                if similar:
                    data.at[i, 'mood'] = row['mood'] + similar[0:2]

    print(data.head())

    # use sci-learn for one hot encoding
    mlb = MultiLabelBinarizer()
    data = data.join(pd.DataFrame(mlb.fit_transform(data.pop('mood')),
                                  columns=mlb.classes_,
                                  index=data.index))
    return data


def merge_w_id(d_class, d_id):
    d_class = d_class.merge(d_id[['artist', 'title', 'id']], on=['artist', 'title'], )
    return d_class


def main():
    # input
    d_truth = load_file(PATH_TRUTH)
    d_class = load_file(PATH_CLASS)
    d_id = load_file(PATH_ID)

    # read string rep of lists as lists
    d_truth['mood'] = d_truth['mood'].apply(ast.literal_eval)
    d_truth = format_class_data(d_truth)
    # d_class = merge_w_id(d_class, d_id)

    # output
    d_truth.to_csv(PATH_CLASS, index=False)
    # d_class.to_csv(PATH_CLASS, index=False)


if __name__ == '__main__':
    main()
