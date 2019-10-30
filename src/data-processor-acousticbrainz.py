import pandas as pd
import requests

# the song Bohemian Rhapsody by Queen has a MBID of: b1a9c0e9-d987-4042-ae91-78d6a3267d69
highlvl_response = requests.get("https://acousticbrainz.org/b1a9c0e9-d987-4042-ae91-78d6a3267d69/high-level")
lowlvl_response = requests.get("https://acousticbrainz.org/b1a9c0e9-d987-4042-ae91-78d6a3267d69/low-level")


def fetch_song_data(response):
    if response.status_code != 200:
        # This means something went wrong.
        print('GET /api/mbid/high-level/ {}'.format(response.status_code))

    json = response.json()
    print(json)
    return json


def json_to_dataframe(json):
    # json to dataframe
    dataframe = pd.read_json(json)
    print(dataframe)


def main():
    json_to_dataframe(fetch_song_data(highlvl_response))
    json_to_dataframe(fetch_song_data(lowlvl_response))


if __name__ == '__main__':
    main()
