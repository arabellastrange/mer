import requests
import pandas as pd
import pickle
from pandas.io.json import json_normalize

PATH_ID = 'I:\Science\CIS\wyb15135\datasets_created\ground_truth_classification_id.csv'
PATH_HIGH = 'I:\Science\CIS\wyb15135\datasets_created\high_lvl_audio_class.csv'
PATH_LOW = 'I:\Science\CIS\wyb15135\datasets_created\low_lvl_audio_class.csv'


def request_song_data(url):
    response = requests.get(url)
    return fetch_song_data(response)


def fetch_song_data(response):
    if response.status_code != 200:
        # This means something went wrong.
        print('GET /api/mbid/level/{}'.format(response.status_code))

    return response.json()


def json_to_dataframe(json):
    return json_normalize(json)


def main():
    highlvl_dataframe = pd.read_csv(PATH_HIGH)
    highlvl_dataframe['metadata.tags.musicbrainz_recordingid'] = highlvl_dataframe[
        'metadata.tags.musicbrainz_recordingid'].apply(lambda s: s.strip())
    lowlvl_dataframe = pd.read_csv(PATH_LOW)
    data = pd.read_csv(PATH_ID)

    # drop unidentified entries
    index_names = data[data['id'].isnull()].index
    data.drop(index_names, inplace=True)

    for i, row in data.iterrows():
        if row['id'] == 'x' or row['id'] in highlvl_dataframe['metadata.tags.musicbrainz_recordingid'].values:
            pass
        else:
            high_url = "https://acousticbrainz.org/" + row['id'] + "/high-level"
            low_url = "https://acousticbrainz.org/" + row['id'] + "/low-level"
            print(high_url)

            highlvl_dataframe = highlvl_dataframe.append(json_to_dataframe(request_song_data(high_url)), sort=True)
            lowlvl_dataframe = lowlvl_dataframe.append(json_to_dataframe(request_song_data(low_url)), sort=True)

    print("output: ")
    print(highlvl_dataframe.head())

    # serialize and write object to file in case csv write fails
    with open('high_lvl.pkl', 'wb') as output:
        pickle.dump(highlvl_dataframe, output, pickle.HIGHEST_PROTOCOL)
    with open('low_lvl.pkl', 'wb') as output:
        pickle.dump(lowlvl_dataframe, output, pickle.HIGHEST_PROTOCOL)

    highlvl_dataframe.to_csv(PATH_HIGH)
    lowlvl_dataframe.to_csv(PATH_LOW)


if __name__ == '__main__':
    main()
