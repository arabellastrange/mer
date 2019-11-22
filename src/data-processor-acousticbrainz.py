import json
import os
import pandas as pd
from pandas.io.json import json_normalize

mood_columns = ['highlevel.mood_acoustic.all.acoustic', 'highlevel.mood_acoustic.all.not_acoustic',
                'highlevel.mood_acoustic.probability', 'highlevel.mood_acoustic.value',
                'highlevel.mood_aggressive.all.aggressive', 'highlevel.mood_aggressive.all.not_aggressive',
                'highlevel.mood_aggressive.probability', 'highlevel.mood_aggressive.value',
                'highlevel.mood_electronic.all.electronic', 'highlevel.mood_electronic.all.not_electronic',
                'highlevel.mood_electronic.probability', 'highlevel.mood_electronic.value',
                'highlevel.mood_happy.all.happy', 'highlevel.mood_happy.all.not_happy',
                'highlevel.mood_happy.probability', 'highlevel.mood_happy.value',
                'highlevel.mood_party.all.not_party', 'highlevel.mood_party.all.party',
                'highlevel.mood_party.probability', 'highlevel.mood_party.value',
                'highlevel.mood_relaxed.all.not_relaxed', 'highlevel.mood_relaxed.all.relaxed',
                'highlevel.mood_relaxed.probability', 'highlevel.mood_relaxed.value',
                'highlevel.mood_sad.all.not_sad', 'highlevel.mood_sad.all.sad',
                'highlevel.mood_sad.probability', 'highlevel.mood_sad.value',
                'highlevel.moods_mirex.all.Cluster1', 'highlevel.moods_mirex.all.Cluster2',
                'highlevel.moods_mirex.all.Cluster3', 'highlevel.moods_mirex.all.Cluster4',
                'highlevel.moods_mirex.all.Cluster5', 'highlevel.moods_mirex.probability',
                'highlevel.moods_mirex.value']

extra_columns = ['highlevel.danceability.probability', 'highlevel.danceability.value', 'highlevel.gender.probability',
                 'highlevel.gender.value', 'highlevel.genre_dortmund.probability', 'highlevel.genre_dortmund.value',
                 'highlevel.genre_electronic.probability', 'highlevel.genre_electronic.value',
                 'highlevel.genre_rosamerica.probability',
                 'highlevel.genre_rosamerica.value', 'highlevel.genre_tzanetakis.probability',
                 'highlevel.genre_tzanetakis.value',
                 'highlevel.ismir04_rhythm.probability', 'highlevel.ismir04_rhythm.value',
                 'highlevel.timbre.probability',
                 'highlevel.timbre.value', 'highlevel.tonal_atonal.probability', 'highlevel.tonal_atonal.value',
                 'highlevel.voice_instrumental.probability', 'highlevel.voice_instrumental.value',
                 'metadata.audio_properties.lossless',
                 'metadata.audio_properties.md5_encoded', 'metadata.tags.acoustid_fingerprint',
                 'metadata.tags.acoustid_id',
                 'metadata.tags.album', 'metadata.tags.album artist', 'metadata.tags.albumartist',
                 'metadata.tags.albumartistsort',
                 'metadata.tags.albumsort', 'metadata.tags.artistsort', 'metadata.tags.asin',
                 'metadata.tags.catalognumber',
                 'metadata.tags.compilation', 'metadata.tags.disc', 'metadata.tags.discnumber',
                 'metadata.tags.discsubtitle',
                 'metadata.tags.disctotal', 'metadata.tags.encodedby', 'metadata.tags.encoder',
                 'metadata.tags.ensemble',
                 'metadata.tags.file_name', 'metadata.tags.isrc', 'metadata.tags.label', 'metadata.tags.media',
                 'metadata.tags.musicbrainz album release country', 'metadata.tags.musicbrainz album status',
                 'metadata.tags.musicbrainz album type', 'metadata.tags.musicbrainz_albumartistid',
                 'metadata.tags.musicbrainz_albumid',
                 'metadata.tags.musicbrainz_artistid', 'metadata.tags.musicbrainz_releasegroupid',
                 'metadata.tags.musicip_puid',
                 'metadata.tags.notes', 'metadata.tags.originaldate', 'metadata.tags.owner',
                 'metadata.tags.releasecountry',
                 'metadata.tags.releasestatus', 'metadata.tags.releasetype', 'metadata.tags.replaygain_album_gain',
                 'metadata.tags.replaygain_album_peak', 'metadata.tags.script', 'metadata.tags.totaldiscs',
                 'metadata.tags.totaltracks',
                 'metadata.tags.tracknumber', 'metadata.tags.tracktotal', 'metadata.version.highlevel.essentia',
                 'metadata.version.highlevel.essentia_build_sha', 'metadata.version.highlevel.essentia_git_sha',
                 'metadata.version.highlevel.extractor', 'metadata.version.highlevel.gaia',
                 'metadata.version.highlevel.gaia_git_sha',
                 'metadata.version.highlevel.models_essentia_git_sha',
                 'metadata.version.lowlevel.essentia_build_sha', 'metadata.version.lowlevel.essentia_git_sha',
                 'metadata.version.lowlevel.extractor', 'metadata.audio_properties.codec',
                 'metadata.audio_properties.downmix', 'metadata.tags.language', 'metadata.version.lowlevel.essentia',
                 'metadata.tags.artists', 'metadata.tags.barcode', 'metadata.tags.musicbrainz_releasetrackid',
                 'metadata.tags.replaygain_track_gain', 'metadata.tags.replaygain_track_peak']

PATH_TRUTH = 'I:\Science\CIS\wyb15135\datasets_created\ground_truth.csv'
PATH_LABELLED = 'I:\Science\CIS\wyb15135\datasets_created\labelled_data.csv'
PATH_AUDIO = 'I:\Science\CIS\wyb15135\datasets_unmodified\\acousticbrainz-highlevel-json-20150130\highlevel'


def load_ground_truth():
    return pd.read_csv(PATH_TRUTH)


def read_json_directory():
    data = pd.DataFrame()
    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(PATH_AUDIO):
        print('opened directory')
        for file in f:
            if '.json' in file:
                files.append(os.path.join(r, file))
            # if len(files) > 10:
            #     break

    for f in files:
        print("reading: " + f)
        with open(f) as json_file:
            j = json_normalize(json.load(json_file))
            data = data.append(j, sort=True)

    return data


def fetch_audio_data_for_truth(ground_truth, audio_data):
    labelled = pd.merge(ground_truth.astype(str), audio_data.astype(str), left_on=['artist', 'title'],
                        right_on=['metadata.tags.artist', 'metadata.tags.title'])
    labelled.drop(columns=['metadata.tags.artist', 'metadata.tags.title'])
    return labelled


def format_audio_data(data):
    data = drop_mood_information(data)
    data = drop_extra_information(data)

    # one entry per song - handling lists as strings so that dataframe can be hashed
    data = data.astype(str).drop_duplicates(['metadata.tags.title', 'metadata.tags.artist'], keep='first')

    # formatting singleton lists into strings to match ground truth dataset
    data['metadata.tags.title'] = data['metadata.tags.title'].apply(lambda x: x.strip("[]'"))
    data['metadata.tags.artist'] = data['metadata.tags.artist'].apply(lambda x: x.strip("[]'"))

    data = data.reset_index(drop=True)

    return data


def drop_mood_information(data):
    data = data.drop(columns=mood_columns)
    return data


def drop_extra_information(data):
    data = data.drop(columns=extra_columns)
    return data


def main():
    # read files into pandas DataFrame
    ground_truth = load_ground_truth()
    highlvl_data = read_json_directory()
    audio_data = format_audio_data(highlvl_data)

    labelled_data = fetch_audio_data_for_truth(ground_truth, audio_data)
    print("Labelled data: ")
    print(labelled_data)

    labelled_data.to_csv(PATH_LABELLED, encoding='utf-8')


if __name__ == '__main__':
    main()
