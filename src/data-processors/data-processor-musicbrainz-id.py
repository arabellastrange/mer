import pandas as pd
import musicbrainzngs as musicbrainz

PATH_TRUTH = 'I:\Science\CIS\wyb15135\datasets_created\ground_truth.csv'
PATH_ID = 'I:\Science\CIS\wyb15135\datasets_created\id_data.csv'

def load_ground_truth():
    return pd.read_csv(PATH_TRUTH)


def main():
    data = load_ground_truth()
    data['id'] = '0-0'

    # identify self
    musicbrainz.set_useragent("mer-ml", "0.1")

    # search
    for i, row in data.iterrows():
        query = row['artist'] + ' ' + row['title']
        results = musicbrainz.search_recordings(query=query)
        if not results['recording-list']:
            print("no recording found")
        for idx, release in enumerate(results['recording-list']):
            if release['artist-credit-phrase'] == row['artist'] and release['title'] == row['title']:
                data.at[i, 'id'] = release['id']

    # output
    data.to_csv(PATH_ID)


if __name__ == '__main__':
    main()
