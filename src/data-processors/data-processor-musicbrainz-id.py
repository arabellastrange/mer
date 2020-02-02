import pandas as pd
import musicbrainzngs as musicbrainz
import difflib as diff
import requests

PATH_ID = 'I:\Science\CIS\wyb15135\datasets_created\ground_truth_classification_id.csv'


def load_file(path):
    return pd.read_csv(path)


def search_musicbrainz_by_recording(data):
    musicbrainz.set_useragent("mer-ml", "0.1")

    for i, row in data.iterrows():
        query = row['title'] + ' ' + row['artist']
        print('Query: ')
        print(query)

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
                            data.at[i, 'fallback-id'] = recording['id']
                            print('no audio data')
    return data


def search_musicbrainz_by_artist(data):
    # identify self
    musicbrainz.set_useragent("mer-ml", "0.1")

    for i, row in data.iterrows():
        artists = musicbrainz.search_artists(artist=row['artist'])
        if not artists['artist-list']:
            print('artist not found')
        else:
            for idx, artist in enumerate(artists['artist-list']):
                if row['artist'].lower() in artist['name'].lower():
                    recordings = fetch_all_recordings(artist['id'])
                    match = find_closest_title(recordings, row['title'])
                    if match:
                        for recording in recordings:
                            if match == recording['title']:
                                print('Query: ')
                                print(row['artist'] + ' ' + row['title'])
                                print('Matches: ')
                                print(recording)

                                if has_audio_data(recording['id']):
                                    data.at[i, 'id'] = recording['id']
                                    print('found')
                                else:
                                    data.at[i, 'fallback-id'] = recording['id']
                                    print('no audio data')
    return data


def find_closest_artist(recordings, target):
    possibilities = []
    for recording in recordings:
        possibilities.append(recording['artist-credit-phrase'])
    # returns 'good enough' matches from list, sorted by similarity
    matches = diff.get_close_matches(target, possibilities)

    if matches:
        return matches[0]


def find_closest_title(recordings, target):
    possibilities = []
    for recording in recordings:
        possibilities.append(recording['title'])
    # returns 'good enough' matches from list, sorted by similarity
    matches = diff.get_close_matches(target, possibilities)

    if matches:
        return matches[0]


def find_closest_title_with_artist(recordings, target, artist):
    possibilities = []
    for recording in recordings:
        if artist == recording['artist-credit-phrase']:
            possibilities.append(recording['title'])
    # returns 'good enough' matches from list, sorted by similarity
    matches = diff.get_close_matches(target, possibilities)

    if matches:
        return matches[0]


def find_closest_recording(recordings, target):
    possibilities = []
    for recording in recordings:
        possibilities.append(recording['title'] + ' ' + recording['artist-credit-phrase'])
    # returns 'good enough' matches from list, sorted by similarity
    matches = diff.get_close_matches(target, possibilities)
    print(matches)
    if matches:
        return matches[0]


def fetch_all_recordings(artist_id):
    # When you want to fetch a list of entities greater than 25, you have to use one of the browse
    # functions. Not only can you specify a limit as high as 100, but you can also specify an offset
    # to get the complete list in multiple requests.
    offset = 0
    limit = 100
    recordings = []
    page = 1
    result = musicbrainz.browse_recordings(artist=artist_id, limit=limit)
    page_recs = result['recording-list']
    recordings += page_recs

    if "release-count" in result:
        count = result['release-count']
    while len(page_recs) >= limit:
        offset += limit
        page += 1
        result = musicbrainz.browse_recordings(artist=artist_id, limit=limit, offset=offset)
        page_recs = result['recording-list']
        recordings += page_recs

    return recordings


def has_audio_data(id):
    # if acousticbrainz has a corresponding data object for this id then store id
    url = "https://acousticbrainz.org/" + id + "/high-level"
    response = requests.get(url)
    if response.status_code == 200:
        return True
    else:
        return False


def main():
    data = load_file(PATH_ID)

    # only fetch songs that dont already have an id
    data_id = data[data['id'].isnull()]

    # finds song id in the musicbrainz database based on song title and artist
    data_id = search_musicbrainz_by_artist(data_id)

    # drop empty id rows
    index_names = data[data['id'].isnull()].index
    data.drop(index_names, inplace=True)

    data = data.append(data_id, ignore_index=True)
    print(data.head())

    # output
    data.to_csv(PATH_ID, index=False)


if __name__ == '__main__':
    main()
