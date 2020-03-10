from json import JSONEncoder

from sklearn.cluster import KMeans
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
import json

PATH_PREDICTED_SVM = 'I:\Science\CIS\wyb15135\datasets_created\predicted_svm_class.csv'
PATH_PREDICTED_FOREST = 'I:\Science\CIS\wyb15135\datasets_created\predicted_forest_class.csv'
PATH_PREDICTED_DEEP = 'I:\Science\CIS\wyb15135\datasets_created\predicted_deep.csv'

PATH_PREDICTED_LSVM = 'I:\Science\CIS\wyb15135\datasets_created\predicted_lsvm_class.csv'
PATH_PREDICTED_LFOREST = 'I:\Science\CIS\wyb15135\datasets_created\predicted_lforest_class.csv'
PATH_PREDICTED_LDEEP = 'I:\Science\CIS\wyb15135\datasets_created\predicted_ldeep.csv'

PATH_ID = 'I:\Science\CIS\wyb15135\datasets_created\ground_truth_classification_id.csv'

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
              'quiet', 'rapture', 'relaxed', 'repeated', 'repetitive', 'rich', 'reticent', 'sad', 'scary', 'serene',
              'sexy', 'silent',
              'slow', 'soft', 'somber', 'soothing', 'space', 'storming', 'strange', 'sunny', 'sweet',
              'trance', 'unconventional', 'upbeat', 'weighty', 'weird', 'wistful', 'zippy']
label_cols_min = ['ambient', 'angry', 'breezy', 'calm', 'cheerful', 'contented', 'dark',
                  'delighted', 'ecstatic', 'elated', 'fast', 'fiery', 'funky', 'happy',
                  'heated', 'heavy', 'jazzy', 'loud', 'melancholy', 'mellow', 'mournful',
                  'passionate', 'quiet', 'relaxed', 'sad', 'serene', 'slow', 'soft',
                  'space', 'storming', 'upbeat', 'weird', 'wistful']


def load_file(path):
    return pd.read_csv(path)


def cluster(data):
    print(data.head())
    kmeans = KMeans(n_clusters=20)
    y = kmeans.fit_predict(data[label_cols_min])

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
    for file in [PATH_PREDICTED_FOREST, PATH_PREDICTED_SVM, PATH_PREDICTED_DEEP, PATH_PREDICTED_LDEEP,
                 PATH_PREDICTED_LFOREST, PATH_PREDICTED_LSVM]:
        data = load_file(file)
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

        PATH_CLUSTERED = file[:file.index('.')] + '_clustered.csv'

        data.to_csv(PATH_CLUSTERED, index=False)

        # Playlists
        playlists_ds = []
        for i in range(20):
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

            # get model type from file name: file name format path/predicted_{model}.csv
            model = file[51: file.index('.')]
            p = Playlist(songs, model, False)
            playlists.append(p)

            # Random Playlist
            rand_playlist = (data.sample(n=8, replace=False))
            rand_songs = []
            for n, row in rand_playlist.iterrows():
                tags = []
                for l in label_cols:
                    if row[l] == 1:
                        tags.append(l)
                r_song = Song(artist=row['artist'], id=row['id'], title=row['title'], tags=tags)
                rand_songs.append(r_song)
            r_p = Playlist(rand_songs, 'none', True)
            playlists.append(r_p)

        PLAYLIST_PATH = "/ui/playlists_" + file[:file.index('.')] + '.json'
        with open(PLAYLIST_PATH, 'w') as outfile:
            json.dump(playlists, outfile, cls=MusicEncoder)


class Playlist:
    songs = []
    model = ''  # what model is this playlist generated by
    random = False

    def __init__(self, songs, model, random):
        self.songs = songs
        self.model = model
        self.random = random


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
