import pandas as pd
import musicbrainzngs as musicbrainz

PATH_TRUTH = 'C:\\Users\\User\Downloads\ground_truth.csv'
PATH_ID = 'C:\\Users\\User\Downloads\id_data.csv'


def load_ground_truth():
    return pd.read_csv(PATH_TRUTH)


def main():
    data = load_ground_truth()
    data['id'] = '0-0'

    # identify self
    musicbrainz.set_useragent("mer-ml", "0.1")

    # search
    for i, row in data.iterrows():
        results = musicbrainz.search_releases(artist=row['artist'], release=row['title'])
        if not results['release-list']:
            print("no release found")
        for idx, release in enumerate(results['release-list']):
            if release['artist-credit-phrase'] == row['artist'] and release['title'] == row['title']:
                data.at[i, 'id'] = release['id']

    # output
    data.to_csv(PATH_ID, encoding='utf-8')


if __name__ == '__main__':
    main()
