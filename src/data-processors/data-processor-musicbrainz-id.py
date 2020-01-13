import pandas as pd
import musicbrainzngs as musicbrainz
import difflib as diff

import requests

PATH_ID = 'I:\Science\CIS\wyb15135\datasets_created\datasets_created_ground_truth.csv'
PATH_ID_RESET = 'I:\Science\CIS\wyb15135\datasets_created\id_data_reset.csv'


def load_data():
    return pd.read_csv(PATH_ID, encoding='latin1')


def search_musicbrainz(data):
    # identify self
    musicbrainz.set_useragent("mer-ml", "0.1")

    for i, row in data.iterrows():
        query = row['title'] + ' ' + row['artist']
        print('Query: ')
        print(query)
        # artist = musicbrainz.search_artists(artist=row['artist'])
        recordings = musicbrainz.search_recordings(query=query)

        if not recordings['recording-list']:
            print("recording not found")
        else:
            # find closest artist and title matches
            query_match = find_closest_recording(recordings, query)
            if query_match:
                for recording in recordings['recording-list']:
                    if query_match == recording['title'] + ' ' + recording['artist-credit-phrase']:
                        print('Found: ')
                        print(recording)
                        if has_audio_data(recording['id']):
                            data.at[i, 'id'] = recording['id']
                        else:
                            print('no audio data')
    return data


def find_closest_artist(recordings, target):
    possibilities = []
    for idx, recording in enumerate(recordings['recording-list']):
        possibilities.append(recording['artist-credit-phrase'])
    # returns 'good enough' matches from list, sorted by similarity
    matches = diff.get_close_matches(target, possibilities)

    if matches:
        return matches[0]


def find_closest_title(recordings, target, artist):
    possibilities = []
    for idx, recording in enumerate(recordings['recording-list']):
        if artist == recording['artist-credit-phrase']:
            possibilities.append(recording['title'])
    # returns 'good enough' matches from list, sorted by similarity
    matches = diff.get_close_matches(target, possibilities)

    if matches:
        return matches[0]


def find_closest_recording(recordings, target):
    possibilities = []
    for idx, recording in enumerate(recordings['recording-list']):
        possibilities.append(recording['title'] + ' ' + recording['artist-credit-phrase'])
    # returns 'good enough' matches from list, sorted by similarity
    matches = diff.get_close_matches(target, possibilities)
    print(matches)
    if matches:
        return matches[0]


def has_audio_data(id):
    # if acousticbrainz has a corresponding data object for this id then store id
    url = "https://acousticbrainz.org/" + id + "/high-level"
    response = requests.get(url)
    if response.status_code == 200:
        return True
    else:
        return False


def main():
    data = load_data()
    # only fetch songs that dont already have an id
    # data_id = data.loc[data['id'] == '0-0']
    data['id'] = '0-0'

    # finds song id in the musicbrainz database based on song title and artist
    data_id = search_musicbrainz(data)

    # drop empty cols
    index_names = data[data['id'] == '0-0'].index
    data.drop(index_names, inplace=True)

    data = data.append(data_id, ignore_index=True)
    # print(data.head())

    # output
    data.to_csv(PATH_ID_RESET, index=False)


if __name__ == '__main__':
    main()
