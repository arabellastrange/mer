# reads in a the outputs of the regression model i.e. arousal valence, title, artists, mood tags, and clusters by
# arousal valence
# selects songs from cluster
# produced playlists and averages arousal valence values for a playlist arousal valence value
# selects tag with similar arousal valence values

from sklearn.cluster import KMeans
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder

PATH_PREDICTED_SVM = 'I:\Science\CIS\wyb15135\datasets_created\high_lvl_predicted_SVM.csv'
PATH_PREDICTED_DEEP = 'I:\Science\CIS\wyb15135\datasets_created\high_lvl_predicted_DEEP.csv'
PATH_CLUSTERED = 'I:\Science\CIS\wyb15135\datasets_created\high_lvl_clustered.csv'


def load_file(path):
    return pd.read_csv(path)


def cluster(data):
    print(data.head())
    kmeans = KMeans(n_clusters=5)
    y = kmeans.fit_predict(data[['arousal', 'valence']])

    data['Cluster'] = y

    # visualise
    plt.scatter(data['arousal'], data['valence'], c=y, s=50, cmap='viridis')

    centers = kmeans.cluster_centers_
    print(centers)
    plt.scatter(centers[:, 0], centers[:, 1], c='black', s=200, alpha=0.5);
    plt.show()

    return data


def select_songs(data):
    return data.sample(n=8, replace=True)


def main():
    # predict valence from arousal in ground truth - example regessor
    data = load_file(PATH_PREDICTED_DEEP)
    
    artist_encoder = LabelEncoder()
    data['artist'] = artist_encoder.fit_transform(data['artist'].astype(str))
    title_encoder = LabelEncoder()
    data['title'] = title_encoder.fit_transform(data['title'].astype(str))
    
    data = data.dropna()
    
    data = cluster(data)
    
    data['artist'] = artist_encoder.inverse_transform(data['artist'])
    data['title'] = title_encoder.inverse_transform(data['title'])
    print(data.head())

    data.to_csv(PATH_CLUSTERED, index=False)

    print(select_songs(data.loc[data['Cluster'] == 2]))


if __name__ == '__main__':
    main()
