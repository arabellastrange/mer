import ast
import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer
import requests
from bs4 import BeautifulSoup

PATH_TRUTH = 'I:\Science\CIS\wyb15135\datasets_created\datasets_created_ground_truth.csv'
PATH_CLASS = 'I:\Science\CIS\wyb15135\datasets_created\ground_truth_classification.csv'


def load_file(path):
    return pd.read_csv(path)


def get_synonym(word):
    response = requests.get('http://www.thesaurus.com/browse/{}'.format(word))
    soup = BeautifulSoup(response.text, 'html')
    section = soup.find('section', {'class': 'e1991neq0'})
    return [span.text for span in section.findAll('span')]


def main():
    # input
    data = load_file(PATH_TRUTH)
    # read string rep of lists as lists
    data['mood'] = data['mood'].apply(ast.literal_eval)
    print(data.head())

    # drop arousal and valence
    # drop only fast and slow tags
    # split mood tags to separate columns for one-hot encoding
    # merge with id'd songs
    data = data.drop(columns=['arousal', 'valence'])
    for i, row in data.iterrows():
        if row['mood'] == ['slow'] or row['mood'] == ['fast'] or row['mood'] == ['chorus'] or row['mood'] == ['opera']:
            data = data.drop(i)
        else:
            # expand singleton lists with synonyms
            if len(row['mood']) == 1:
                similar = get_synonym(row['mood'][0])
                print(similar)
                if similar:
                    row['mood'] = row['mood'] + similar[0:2]

    # use sci-learn for one hot encoding
    mlb = MultiLabelBinarizer()
    data = data.join(pd.DataFrame(mlb.fit_transform(data.pop('mood')),
                                  columns=mlb.classes_,
                                  index=data.index))

    # output
    data.to_csv(PATH_CLASS, index=False)


if __name__ == '__main__':
    main()
