import pandas as pd
import os
import json
from pandas.io.json import json_normalize

PATH_HAUDIO = 'I:\Science\CIS\wyb15135\datasets_unmodified\\acousticbrainz-highlevel-json-20150130\highlevel\\0\\00'
PATH_LAUDIO = 'I:\Science\CIS\wyb15135\datasets_unmodified\\acousticbrainz-lowlevel-json-20150129\lowlevel\\0\\00'

PATH_HTRUTH = 'I:\Science\CIS\wyb15135\datasets_created\high_lvl_test_data.csv'
PATH_LTRUTH = 'I:\Science\CIS\wyb15135\datasets_created\low_lvl_test_data.csv'


def read_json_directory(path):
    data = pd.DataFrame()
    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        print('opened directory')
        for file in f:
            if '.json' in file:
                files.append(os.path.join(r, file))

    for f in files:
        print("reading: " + f)
        with open(f) as json_file:
            j = json_normalize(json.load(json_file))
            data = data.append(j, sort=True)

    return data


def main():
    # read files into pandas DataFrame
    high_audio = read_json_directory(PATH_HAUDIO)
    low_audio = read_json_directory(PATH_LAUDIO)

    high_audio.to_csv(PATH_HTRUTH, index=False)
    low_audio.to_csv(PATH_LTRUTH, index=False)


if __name__ == '__main__':
    main()
