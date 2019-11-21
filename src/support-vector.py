import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from matplotlib import cm
from scipy.interpolate import griddata
from mpl_toolkits.mplot3d import Axes3D
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

PATH_TRUTH = 'I:\Science\CIS\wyb15135\datasets_created\ground_truth.csv'


def load_ground_truth():
    return pd.read_csv(PATH_TRUTH)


def main():
    # predict valence from arousal in ground truth - example regessor
    data = load_ground_truth()
    data = data.drop(columns='mood')

    s = data.drop(columns='valence')
    target = data['valence']

    # encode string labels as ints
    encoder = LabelEncoder()
    s['artist'] = encoder.fit_transform(s['artist'])
    s['title'] = encoder.fit_transform(s['title'])

    # split data set into train and test sets
    data_train, data_test, target_train, target_test = train_test_split(s, target, test_size=0.30, random_state=10)

    # model
    regressor = SVR(kernel='rbf')

    # predict 
    regressor.fit(data_train, target_train)
    prediction = regressor.predict(data_test)
    # print('prediction: ')
    # print(prediction)
    # print('target: ')
    # print(target_test)
    print("Accuracy: " + accuracy_score(target_test.values, prediction, normalize=True))


if __name__ == '__main__':
    main()
