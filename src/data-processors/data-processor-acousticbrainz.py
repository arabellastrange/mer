import pandas as pd

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
                'highlevel.moods_mirex.value', 'metadata.tags.mood']
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
                 'metadata.tags.acoustid_id', 'metadata.tags.album artist', 'metadata.tags.albumartist',
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
                 'metadata.tags.originaldate', 'metadata.tags.owner',
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
drop_cols = ['highlevel.danceability.version.essentia', 'highlevel.danceability.version.essentia_build_sha',
             'highlevel.danceability.version.essentia_git_sha', 'highlevel.danceability.version.extractor',
             'highlevel.danceability.version.gaia', 'highlevel.danceability.version.gaia_git_sha',
             'highlevel.danceability.version.models_essentia_git_sha', 'highlevel.gender.version.essentia',
             'highlevel.gender.version.essentia_build_sha', 'highlevel.gender.version.essentia_git_sha',
             'highlevel.gender.version.extractor', 'highlevel.gender.version.gaia',
             'highlevel.gender.version.gaia_git_sha', 'highlevel.gender.version.models_essentia_git_sha',
             'highlevel.genre_dortmund.version.essentia', 'highlevel.genre_dortmund.version.essentia_build_sha',
             'highlevel.genre_dortmund.version.essentia_git_sha', 'highlevel.genre_dortmund.version.extractor',
             'highlevel.genre_dortmund.version.gaia', 'highlevel.genre_dortmund.version.gaia_git_sha',
             'highlevel.genre_dortmund.version.models_essentia_git_sha', 'highlevel.genre_electronic.version.essentia',
             'highlevel.genre_electronic.version.essentia_build_sha',
             'highlevel.genre_electronic.version.essentia_git_sha',
             'highlevel.genre_electronic.version.extractor', 'highlevel.genre_electronic.version.gaia',
             'highlevel.genre_electronic.version.gaia_git_sha',
             'highlevel.genre_electronic.version.models_essentia_git_sha',
             'highlevel.genre_rosamerica.version.essentia', 'highlevel.genre_rosamerica.version.essentia_build_sha',
             'highlevel.genre_rosamerica.version.essentia_git_sha', 'highlevel.genre_rosamerica.version.extractor',
             'highlevel.genre_rosamerica.version.gaia', 'highlevel.genre_rosamerica.version.gaia_git_sha',
             'highlevel.genre_rosamerica.version.models_essentia_git_sha',
             'highlevel.genre_tzanetakis.version.essentia', 'highlevel.genre_tzanetakis.version.essentia_build_sha',
             'highlevel.genre_tzanetakis.version.essentia_git_sha',
             'highlevel.genre_tzanetakis.version.extractor', 'highlevel.genre_tzanetakis.version.gaia',
             'highlevel.genre_tzanetakis.version.gaia_git_sha',
             'highlevel.genre_tzanetakis.version.models_essentia_git_sha',
             'highlevel.ismir04_rhythm.version.essentia', 'highlevel.ismir04_rhythm.version.essentia_build_sha',
             'highlevel.ismir04_rhythm.version.essentia_git_sha', 'highlevel.ismir04_rhythm.version.extractor',
             'highlevel.ismir04_rhythm.version.gaia', 'highlevel.ismir04_rhythm.version.gaia_git_sha',
             'highlevel.ismir04_rhythm.version.models_essentia_git_sha', 'highlevel.mood_acoustic.version.essentia',
             'highlevel.mood_acoustic.version.essentia_build_sha', 'highlevel.mood_acoustic.version.essentia_git_sha',
             'highlevel.mood_acoustic.version.extractor', 'highlevel.mood_acoustic.version.gaia',
             'highlevel.mood_acoustic.version.gaia_git_sha', 'highlevel.mood_acoustic.version.models_essentia_git_sha',
             'highlevel.mood_aggressive.version.essentia', 'highlevel.mood_aggressive.version.essentia_build_sha',
             'highlevel.mood_aggressive.version.essentia_git_sha', 'highlevel.mood_aggressive.version.extractor',
             'highlevel.mood_aggressive.version.gaia', 'highlevel.mood_aggressive.version.gaia_git_sha',
             'highlevel.mood_aggressive.version.models_essentia_git_sha', 'highlevel.mood_electronic.version.essentia',
             'highlevel.mood_electronic.version.essentia_build_sha',
             'highlevel.mood_electronic.version.essentia_git_sha',
             'highlevel.mood_electronic.version.extractor', 'highlevel.mood_electronic.version.gaia',
             'highlevel.mood_electronic.version.gaia_git_sha',
             'highlevel.mood_electronic.version.models_essentia_git_sha',
             'highlevel.mood_happy.version.essentia', 'highlevel.mood_happy.version.essentia_build_sha',
             'highlevel.mood_happy.version.essentia_git_sha',
             'highlevel.mood_happy.version.extractor', 'highlevel.mood_happy.version.gaia',
             'highlevel.mood_happy.version.gaia_git_sha', 'highlevel.mood_happy.version.models_essentia_git_sha',
             'highlevel.mood_party.version.essentia', 'highlevel.mood_party.version.essentia_build_sha',
             'highlevel.mood_party.version.essentia_git_sha', 'highlevel.mood_party.version.extractor',
             'highlevel.mood_party.version.gaia', 'highlevel.mood_party.version.gaia_git_sha',
             'highlevel.mood_party.version.models_essentia_git_sha', 'highlevel.mood_relaxed.version.essentia',
             'highlevel.mood_relaxed.version.essentia_build_sha', 'highlevel.mood_relaxed.version.essentia_git_sha',
             'highlevel.mood_relaxed.version.extractor', 'highlevel.mood_relaxed.version.gaia',
             'highlevel.mood_relaxed.version.gaia_git_sha', 'highlevel.mood_relaxed.version.models_essentia_git_sha',
             'highlevel.mood_sad.version.essentia', 'highlevel.mood_sad.version.essentia_build_sha',
             'highlevel.mood_sad.version.essentia_git_sha', 'highlevel.mood_sad.version.extractor',
             'highlevel.mood_sad.version.gaia', 'highlevel.mood_sad.version.gaia_git_sha',
             'highlevel.mood_sad.version.models_essentia_git_sha', 'highlevel.moods_mirex.version.essentia',
             'highlevel.moods_mirex.version.essentia_build_sha', 'highlevel.moods_mirex.version.essentia_git_sha',
             'highlevel.moods_mirex.version.extractor', 'highlevel.moods_mirex.version.gaia',
             'highlevel.moods_mirex.version.gaia_git_sha', 'highlevel.moods_mirex.version.models_essentia_git_sha',
             'highlevel.timbre.version.essentia', 'highlevel.timbre.version.essentia_build_sha',
             'highlevel.timbre.version.essentia_git_sha', 'highlevel.timbre.version.extractor',
             'highlevel.timbre.version.gaia', 'highlevel.timbre.version.gaia_git_sha',
             'highlevel.timbre.version.models_essentia_git_sha', 'highlevel.tonal_atonal.version.essentia',
             'highlevel.tonal_atonal.version.essentia_build_sha', 'highlevel.tonal_atonal.version.essentia_git_sha',
             'highlevel.tonal_atonal.version.extractor', 'highlevel.tonal_atonal.version.gaia',
             'highlevel.tonal_atonal.version.gaia_git_sha', 'highlevel.tonal_atonal.version.models_essentia_git_sha',
             'highlevel.voice_instrumental.version.essentia',
             'highlevel.voice_instrumental.version.essentia_build_sha',
             'highlevel.voice_instrumental.version.essentia_git_sha',
             'highlevel.voice_instrumental.version.extractor', 'highlevel.voice_instrumental.version.gaia',
             'highlevel.voice_instrumental.version.gaia_git_sha',
             'highlevel.voice_instrumental.version.models_essentia_git_sha',
             'metadata.tags.album artist credit', 'metadata.tags.albumartist_credit', 'metadata.tags.analysis',
             'metadata.tags.arranger', 'metadata.tags.artistwebpage', 'metadata.tags.composer',
             'metadata.tags.composersort', 'metadata.tags.conductor', 'metadata.tags.content group',
             'metadata.tags.contentgroup', 'metadata.tags.copyright', 'metadata.tags.copyrighturl',
             'metadata.tags.country', 'metadata.tags.date', 'metadata.tags.description',
             'metadata.tags.discc', 'metadata.tags.discid', 'metadata.tags.djmixer',
             'metadata.tags.encodersettings', 'metadata.tags.encoding', 'metadata.tags.encodingtime',
             'metadata.tags.engineer', 'metadata.tags.filetype',
             'metadata.tags.filewebpage', 'metadata.tags.fingerprint', 'metadata.tags.fmps_playcount',
             'metadata.tags.fmps_rating_amarok_score', 'metadata.tags.format', 'metadata.tags.grouping',
             'metadata.tags.initialkey', 'metadata.tags.itunes_cddb_1', 'metadata.tags.length',
             'metadata.tags.license', 'metadata.tags.lyricist', 'metadata.tags.mixer',
             'metadata.tags.mp3gain_album_minmax', 'metadata.tags.mp3gain_minmax', 'metadata.tags.mp3gain_undo',
             'metadata.tags.musicbrainz album artist', 'metadata.tags.musicbrainz album artist sortname',
             'metadata.tags.musicbrainz disc id', 'metadata.tags.musicbrainz non-album',
             'metadata.tags.musicbrainz original album id', 'metadata.tags.musicbrainz release track id',
             'metadata.tags.musicbrainz trm id', 'metadata.tags.musicbrainz_albumstatus',
             'metadata.tags.musicbrainz_albumtype', 'metadata.tags.musicbrainz_discid',
             'metadata.tags.musicbrainz_sortname', 'metadata.tags.musicbrainz_trmid',
             'metadata.tags.musicbrainz_workid', 'metadata.tags.musicmagic data',
             'metadata.tags.musicmagic fingerprint', 'metadata.tags.originalalbum',
             'metadata.tags.originalartist', 'metadata.tags.originalyear', 'metadata.tags.performer',
             'metadata.tags.producer', 'metadata.tags.publisher',
             'metadata.tags.quodlibet::labelid', 'metadata.tags.rating', 'metadata.tags.release type',
             'metadata.tags.releasedate', 'metadata.tags.remixer',
             'metadata.tags.replaygain_reference_loudness', 'metadata.tags.rip date',
             'metadata.tags.ripping tool', 'metadata.tags.source', 'metadata.tags.tagging time',
             'metadata.tags.taggingdate', 'metadata.tags.the cavalera conspiracy', 'metadata.tags.titlesort',
             'metadata.tags.tool name', 'metadata.tags.tool version', 'metadata.tags.track', 'metadata.tags.trackc',
             'metadata.tags.url', 'metadata.tags.url:discogs_release', 'metadata.tags.website',
             'metadata.tags.work', 'metadata.tags.writer', 'metadata.tags.year', 'metadata.tags.artist credit',
             'metadata.tags.genre', 'metadata.audio_properties.sample_rate', 'metadata.tags.bpm']

PATH_DATA = 'I:\Science\CIS\wyb15135\datasets_created\id_data_reset.csv'
PATH_HIGH = 'I:\Science\CIS\wyb15135\datasets_created\high_lvl_audio_reset.csv'
PATH_LOW = 'I:\Science\CIS\wyb15135\datasets_created\low_lvl_audio_reset.csv'
PATH_TRUTH = 'I:\Science\CIS\wyb15135\datasets_created\ground_truth_high_reset.csv'


def load_file(path):
    return pd.read_csv(path)


def fetch_audio_data_for_truth(ground_truth, audio_data):
    data = format_audio_data(audio_data)
    labelled = pd.merge(ground_truth.astype(str), data.astype(str), left_on=['id'],
                        right_on=['metadata.tags.musicbrainz_recordingid'])
    return labelled


def format_audio_data(data):
    data = data.drop_duplicates()
    data = drop_mood_information(data)
    data = drop_extra_information(data)
    data = data.drop(columns=drop_cols)

    performer_cols = [c for c in data.columns if 'metadata.tags.performer:' in c]
    data = data.drop(columns=performer_cols)

    data['metadata.tags.musicbrainz_recordingid'] = data['metadata.tags.musicbrainz_recordingid'].astype(str).apply(
        lambda x: x.strip("[]'"))
    data['metadata.tags.artist'] = data['metadata.tags.artist'].astype(str).apply(
        lambda x: x.strip("[]'"))
    data['metadata.tags.title'] = data['metadata.tags.title'].astype(str).apply(
        lambda x: x.strip("[]'"))
    data['metadata.tags.album'] = data['metadata.tags.title'].astype(str).apply(
        lambda x: x.strip("[]'"))

    data = data.reset_index(drop=True)

    return data


def drop_mood_information(data):
    data = data.drop(columns=mood_columns)
    return data


def drop_extra_information(data):
    data = data.drop(columns=extra_columns)
    return data


def main():
    # input
    # id_data = load_file(PATH_DATA)
    # id_data = id_data.drop_duplicates()
    #
    # highlvl_data = load_file(PATH_HIGH)
    # lowlvl_data = load_file(PATH_LOW)

    # ground_truth = fetch_audio_data_for_truth(id_data, highlvl_data)
    # print("Ground truth: ")
    # print(ground_truth.head())

    ground_truth = pd.read_csv(PATH_TRUTH)
    for i, row in ground_truth.iterrows():
        if row['artist'] != row['metadata.tags.artist']:
            if row['title'] != row['metadata.tags.title']:
                print(row)
    # output
    # ground_truth.to_csv(PATH_TRUTH, index=False)


if __name__ == '__main__':
    main()
