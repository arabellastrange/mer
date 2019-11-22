import pandas as pd

PATH_LABELLED = 'I:\Science\CIS\wyb15135\datasets_created\labelled_data.csv'


def load_labelled_data():
    return pd.read_csv(PATH_LABELLED)


def main():
    data = load_labelled_data()
    print(data)


if __name__ == '__main__':
    main()
