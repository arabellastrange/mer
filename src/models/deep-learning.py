import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import seaborn as sns

PATH_TRUTH = 'I:\Science\CIS\wyb15135\datasets_created\\formatted_high_lvl_ground_truth.csv'


def load_file(path):
    return pd.read_csv(path)


def main():
    data = load_file(PATH_TRUTH)

    train_dataset = data.sample(frac=0.8, random_state=0)
    test_dataset = data.drop(train_dataset.index)
    sns.pairplot(train_dataset[["valence", "arousal", "Displacement", "Weight"]], diag_kind="kde")

    print(data)


if __name__ == '__main__':
    main()
