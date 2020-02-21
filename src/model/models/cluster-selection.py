# reads in a the outputs of the regression model i.e. arousal valence, title, artists, mood tags, and clusters by
# arousal valence
# selects songs from cluster
# produced playlists and averages arousal valence values for a playlist arousal valence value
# selects tag with similar arousal valence values

from sklearn.cluster import KMeans
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder

PATH_PREDICTED_SVM = 'I:\Science\CIS\wyb15135\datasets_created\high_lvl_predicted_svm_class.csv'
PATH_PREDICTED_FOREST = 'I:\Science\CIS\wyb15135\datasets_created\high_lvl_predicted_forest_class.csv'
PATH_PREDICTED_DEEP = 'I:\Science\CIS\wyb15135\datasets_created\high_lvl_predicted_deep.csv'
PATH_ID = 'I:\Science\CIS\wyb15135\datasets_created\ground_truth_classification_id.csv'
PATH_CLUSTERED = 'I:\Science\CIS\wyb15135\datasets_created\high_lvl_clustered.csv'

label_cols = ['airy', 'ambient', 'angry', 'animated', 'astonishing', 'big', 'bizarre', 'black', 'bleak', 'boisterous',
              'boring', 'breezy', 'bright', 'buoyant', 'calm', 'cheerful', 'cheery', 'choral', 'comfortable', 'complex',
              'constant', 'contented', 'contrasting', 'cool', 'curious', 'dark', 'daze', 'deafening', 'deep',
              'delicate', 'delighted', 'despondent', 'different', 'difficult', 'dim', 'distinctive',
              'dreamy', 'dull', 'earthy', 'easy', 'eccentric', 'ecstatic', 'ecstasy', 'eerie', 'elated', 'emphatic',
              'encouraging',
              'enveloping', 'extraordinary', 'fashionable', 'fast', 'fiery', 'flashy', 'fluid',
              'funky', 'happy', 'hard', 'harmonious', 'heated', 'heavy', 'hip', 'hopeful', 'jazzy', 'light',
              'lively', 'loud', 'low', 'luminous', 'melancholy', 'mellow', 'mild', 'modish', 'monotonous', 'mournful',
              'muted', 'odd', 'old', 'operatic', 'orchestral', 'passionate', 'peaceful', 'peculiar', 'profound',
              'quick',
              'quiet', 'rapture', 'relaxed', 'repeated' ,'repetitive', 'rich', 'reticent', 'sad', 'scary', 'serene',
              'sexy','silent',
              'slow', 'soft', 'somber', 'soothing', 'space', 'storming', 'strange', 'sunny', 'sweet',
              'trance', 'unconventional', 'upbeat', 'weighty', 'weird', 'wistful', 'zippy']

def load_file(path):
    return pd.read_csv(path)


def cluster(data):
    print(data.head())
    kmeans = KMeans(n_clusters=20)
    y = kmeans.fit_predict(data[label_cols])

    data['Cluster'] = y

    # visualise
    centers = kmeans.cluster_centers_
    print(centers)
    plt.scatter(centers[:, 0], centers[:, 1], c='red', s=200, alpha=0.5)
    plt.show()

    return data


def select_songs(data):
    return data.sample(n=8, replace=False)


def main():
    # predict valence from arousal in ground truth - example regessor
    data = load_file(PATH_PREDICTED_FOREST)
    data_id = load_file(PATH_ID)
    data = pd.merge(data, data_id[['artist', 'title', 'id']], on=['id'])

    artist_encoder = LabelEncoder()
    data['artist'] = artist_encoder.fit_transform(data['artist'].astype(str))
    title_encoder = LabelEncoder()
    data['title'] = title_encoder.fit_transform(data['title'].astype(str))

    data = cluster(data)
    
    data['artist'] = artist_encoder.inverse_transform(data['artist'])
    data['title'] = title_encoder.inverse_transform(data['title'])

    print(data.head())

    data.to_csv(PATH_CLUSTERED, index=False)

    # Playlists
    songs_1 = select_songs(data.loc[data['Cluster'] == 1])
    songs_10 = select_songs(data.loc[data['Cluster'] == 10])
    
    print(songs_1)
    print('--------------')
    print(songs_10)


if __name__ == '__main__':
    main()
