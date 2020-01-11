import requests
import pandas as pd
import pickle
from pandas.io.json import json_normalize

PATH_ID = 'I:\Science\CIS\wyb15135\datasets_created\id_data.csv'
PATH_HIGH = 'I:\Science\CIS\wyb15135\datasets_created\high_lvl_audio.csv'
PATH_LOW = 'I:\Science\CIS\wyb15135\datasets_created\low_lvl_audio.csv'


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
    highlvl_dataframe = pd.DataFrame()
    lowlvl_dataframe = pd.DataFrame()

    data = pd.read_csv(PATH_ID, encoding='latin1')

    # drop unidentified entries
    index_names = data[data['id'] == '0-0'].index
    data.drop(index_names, inplace=True)

    for i, row in data.iterrows():
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
