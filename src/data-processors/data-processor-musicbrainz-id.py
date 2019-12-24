import pandas as pd
import musicbrainzngs as musicbrainz
import difflib as diff

PATH_ID_REM = 'I:\Science\CIS\wyb15135\datasets_created\id_data_rem.csv'


def load_data():
    return pd.read_csv(PATH_ID_REM, encoding='latin1')


def search_musicbrainz(data):
    # identify self
    musicbrainz.set_useragent("mer-ml", "0.1")

    # search for artist
    for i, row in data.iterrows():
        print('Query: ')
        print(row['artist'] + ' ' + row['title'])

        artist = musicbrainz.search_artists(artist=row['artist'])
        if not artist['artist-list']:
            print("artist not found")
        else:
            for idx, art in enumerate(artist['artist-list']):
                if row['artist'].lower() in art['name'].lower():
                    # get all recordings by artist
                    song_titles = []
                    # limit is an integer value defining how many entries should be returned.
                    # Only values between 1 and 100 (both inclusive) are allowed. If not given, this defaults to 25
                    recordings = musicbrainz.browse_recordings(artist=art['id'], limit=100)
                    print(recordings)
                    for recording in recordings['recording-list']:
                        # create a list of all recording titles by artist
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
                                print(recording)
                                data.at[i, 'id'] = recording['id']

    return data


def main():
    data = load_data()

    # only fetch songs that dont already have an id
    data_id = data.loc[data['id'] == '0-0']

    # finds song id in the musicbrainz database based on song title and artist
    data_id = search_musicbrainz(data_id)

    # drop empty cols
    index_names = data[data['id'] == '0-0'].index
    data.drop(index_names, inplace=True)

    data = data.append(data_id)

    # output
    data.to_csv(PATH_ID_REM, encoding='latin1')


if __name__ == '__main__':
    main()
