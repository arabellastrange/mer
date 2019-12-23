import pandas as pd
import musicbrainzngs as musicbrainz
import difflib as diff

PATH_ID = 'I:\Science\CIS\wyb15135\datasets_created\id_data_rem.csv'
PATH_ID_REM = 'I:\Science\CIS\wyb15135\datasets_created\id_data_rem.csv'


def load_data():
    return pd.read_csv(PATH_ID_REM, encoding='latin1')


def search_musicbrainz(data):
    # identify self
    musicbrainz.set_useragent("mer-ml", "0.1")

    # search for artist
    for i, row in data.iterrows():
        artist = musicbrainz.search_artists(artist=row['artist'])
        if not artist['artist-list']:
            print("artist not found")
        else:
            for idx, art in enumerate(artist['artist-list']):
                if row['artist'].lower() in art['name'].lower():
                    # get all recording by artist
                    song_titles = []
                    recordings = musicbrainz.browse_recordings(artist=art['id'])
                    print(recordings)
                    for recording in recordings['recording-list']:
                        # create a list of all recording titles by artist
                        song_titles.append(recording['title'])
                    # find closest match from list
                    print(song_titles)
                    matches = diff.get_close_matches(row['title'], song_titles)

                    print('Query: ')
                    print(row['artist'] + row['title'])
                    print('Matches: ')
                    print(matches)
                    # data.at[i, 'id'] = recording['id']

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
    # data.to_csv(PATH_ID_REM, encoding='latin1')


if __name__ == '__main__':
    main()
