from json import JSONEncoder

from sklearn.cluster import KMeans
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
import json

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
    # allow repetition for the moment using replace true
    return data.sample(n=8, replace=True)


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
    playlists_ds = []
    for i in range(19):
        playlists_ds.append(select_songs(data.loc[data['Cluster'] == i]))

    playlists = []
    for playlist in playlists_ds:
        songs = []
        for i, row in playlist.iterrows():
            tags = []
            for l in label_cols:
                if row[l] == 1:
                    tags.append(l)

            song = Song(artist=row['artist'], id=row['id'], title=row['title'], tags=tags)
            songs.append(song)
        p = Playlist(songs)
        playlists.append(p)

    with open("C:/Users/User/PycharmProjects/merml/src/ui/playlists/playlists.json", 'w') as outfile:
        json.dump(playlists, outfile, cls=MusicEncoder)


class Playlist:
    songs = []
    song_ids = []

    def __init__(self, songs):
        self.songs = songs


class Song:
    artist = ''
    title = ''
    id = ''
    tags = []

    def __init__(self, artist, title, id, tags):
        self.artist = artist
        self.title = title
        self.id = id
        self.tags = tags


class MusicEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


if __name__ == '__main__':
    main()
