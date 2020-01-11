import pandas as pd
import musicbrainzngs as musicbrainz
import difflib as diff

import requests

PATH_ID = 'I:\Science\CIS\wyb15135\datasets_created\id_data.csv'
PATH_ID_RESET = 'I:\Science\CIS\wyb15135\datasets_created\id_data_reset.csv'


def load_data():
    return pd.read_csv(PATH_ID, encoding='latin1')


def search_musicbrainz(data):
    # identify self
    musicbrainz.set_useragent("mer-ml", "0.1")

    # search for artist
    for i, row in data.iterrows():
        print('Query: ')
        query = row['artist'] + ' ' + row['title']
        print(query)

        # artist = musicbrainz.search_artists(artist=row['artist'])
        recordings = musicbrainz.search_recordings(query=query)

        if not recordings['recording-list']:
            print("recording not found")
        else:
            song_titles = []
            for idx, recording in enumerate(recordings['recording-list']):
                if row['artist'].lower() in recording['artist-credit-phrase'].lower():
                    # get all recordings by artist
                    song_titles.append(recording['title'])
            # find closest match from list
            print(song_titles)
            # returns 'good enough' matches from list, sorted by similarity
            matches = diff.get_close_matches(row['title'], song_titles)

            print('Matches: ')
            print(matches)

            for recording in recordings['recording-list']:
                if matches:
                    if recording['title'] == matches[0]:
                        if row['artist'].lower() in recording['artist-credit-phrase'].lower():
                            print(recording)
                            url = "https://acousticbrainz.org/" + recording['id'] + "/high-level"
                            response = requests.get(url)
                            if response.status_code == 200:
                                # if acuosticbrainz has a corresponding data object for this id then store id
                                data.at[i, 'id'] = recording['id']

    return data


def main():
    data = load_data()

    # only fetch songs that dont already have an id
    # data_id = data.loc[data['id'] == '0-0']
    # reset
    data['id'] = '0-0'

    # finds song id in the musicbrainz database based on song title and artist
    data_id = search_musicbrainz(data)

    # drop empty cols
    # index_names = data[data['id'] == '0-0'].index
    # data.drop(index_names, inplace=True)

    # data = data.append(data_id, ignore_index=True)
    # print(data.head())

    # output
    data_id.to_csv(PATH_ID_RESET, index=False)


if __name__ == '__main__':
    main()
