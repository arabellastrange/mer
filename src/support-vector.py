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
    #predict valence from arousal in ground truth - example regessor
    data = load_ground_truth()
    data = data.drop(columns='mood')
    
    s = data.drop(columns='valence')
    target = data['valence']
    
    encoder = LabelEncoder()
    s['artist'] = encoder.fit_transform(s['artist'])
    s['title'] = encoder.fit_transform(s['title'])
    
    #split data set into train and test sets
    data_train, data_test, target_train, target_test = train_test_split(data,target, test_size = 0.30, random_state = 10)
    
    # model 
    scalar = StandardScaler()
    scalar_target = StandardScaler()
    
    data_2 = scalar.fit_transform(s)
    target_2 = scalar_target.fit_transform(target)
    
    regressor = SVR(kernel = 'rbf')
    
    # predict 
    prediction = regressor.fit(data_2, target_2).predict(data_test)
    print("Accuracy: " + accuracy_score(target_test, prediction, normalize = True))
    
    #displaying the 3D graph
    x = s[:, 0]
    y = s[:, 1]
    z = target
    zp = scalar_target.inverse_transform(regressor.predict(scalar.transform(s))) #the predictions
    
    xi = np.linspace(min(x), max(x))
    yi = np.linspace(min(y), max(y))
    X, Y = np.meshgrid(xi, yi)
    ZP = griddata(x, y, zp, xi, yi)
    
    fig = plt.figure()
    ax = Axes3D(fig)
    surf = ax.plot_surface(X, Y, ZP, rstride=1, cstride=1, facecolors=cm.jet(ZP/3200), linewidth=0, antialiased=True)
    ax.scatter(x, y, z)
    ax.set_zlim3d(np.min(z), np.max(z))
    colorscale = cm.ScalarMappable(cmap=cm.jet)
    colorscale.set_array(z)
    fig.colorbar(colorscale)
    plt.show()



if __name__ == '__main__':
    main()
