# reads in a the outputs of the regression model i.e. arousal valence, title, artists, mood tags, and clusters by
# arousal valence
# selects songs from cluster
# produced playlists and averages arousal valence values for a playlist arousal valence value
# selects tag with similar arousal valence values

from sklearn.cluster import KMeans
import pandas as pd
import matplotlib.pyplot as plt

PATH_PREDICTED_SVM = 'I:\Science\CIS\wyb15135\datasets_created\high_lvl_predicted_SVM.csv'
PATH_PREDICTED_DEEP = 'I:\Science\CIS\wyb15135\datasets_created\high_lvl_predicted_DEEP.csv'
PATH_CLUSTERED = 'I:\Science\CIS\wyb15135\datasets_created\high_lvl_clustered.csv'


def load_file(path):
    return pd.read_csv(path)


def cluster(data):
    kmeans = KMeans(n_clusters=5, random_state=0).fit(data)
    y = kmeans.fit_predict(data[['arousal', 'valence']])

    data['Cluster'] = y

    # visualise
    plt.scatter(data[:, 0], data[:, 1], c=y, s=50, cmap='viridis')

    centers = kmeans.cluster_centers_
    plt.scatter(centers[:, 0], centers[:, 1], c='black', s=200, alpha=0.5);
    plt.show()

    return data

def select_songs(data):
    return data.sample(n = 8, replace=True)

def main():
    # predict valence from arousal in ground truth - example regessor
    data = load_file(PATH_PREDICTED_DEEP)
    data = cluster(data)
    print(data.head())

    data.to_csv(PATH_CLUSTERED)


if __name__ == '__main__':
    main()
