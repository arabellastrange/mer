import pandas as pd
import musicbrainzngs as musicbrainz

PATH_TRUTH = 'C:\\Users\\User\Downloads\ground_truth.csv'
PATH_ID = 'I:\Science\CIS\wyb15135\datasets_created\id_data.csv'


def load_ground_truth():
    return pd.read_csv(PATH_TRUTH)


def main():
    data = load_ground_truth()

    # identify self
    musicbrainz.set_useragent("mer-ml", "0.1")

    # search
    for i, row in data.iterrows():
        results = musicbrainz.search_releases(artist=row['artist'], release=row['title'])
        if not results['release-list']:
            print("no release found")
        for release in enumerate(results['release-list']):
            print(release)

if __name__ == '__main__':
    main()