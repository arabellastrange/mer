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
from sklearn.metrics import accuracy_score, r2_score

PATH_TRUTH = 'I:\Science\CIS\wyb15135\datasets_created\ground_truth.csv'
PATH_LABELLED = 'I:\Science\CIS\wyb15135\datasets_created\labelled_data.csv'


def load_labelled_data():
    return pd.read_csv(PATH_LABELLED)


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
    prediction = regressor.fit(data_train, target_train).predict(data_test)

    print("Accuracy: ")
    print(r2_score(target_test.values.reshape(-1, 1), prediction))

    # displaying the 3D graph
    # scalar_target = StandardScaler()
    # scalar = StandardScaler()
    # scalar_target.fit_transform(target_train.values.reshape(-1,1))
    # data_train = scalar.fit_transform(data_train)
    #
    # x = data_train[:, 0]
    # y = data_train[:, 1]
    # z = target
    # zp = scalar_target.inverse_transform(regressor.predict(scalar.transform(data_train))) #the predictions
    #
    # xi = np.linspace(min(x), max(x))
    # yi = np.linspace(min(y), max(y))
    # X, Y = np.meshgrid(xi, yi)
    # ZP = griddata(x, y, zp, xi, yi)
    #
    # fig = plt.figure()
    # ax = Axes3D(fig)
    # surf = ax.plot_surface(X, Y, ZP, rstride=1, cstride=1, facecolors=cm.jet(ZP/3200), linewidth=0, antialiased=True)
    # ax.scatter(x, y, z)
    # ax.set_zlim3d(np.min(z), np.max(z))
    # colorscale = cm.ScalarMappable(cmap=cm.jet)
    # colorscale.set_array(z)
    # fig.colorbar(colorscale)
    # plt.show()


if __name__ == '__main__':
    main()
