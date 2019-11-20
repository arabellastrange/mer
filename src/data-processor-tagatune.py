import pandas as pd
import numpy as np

# process the tagatun dataset
# combine clips of the same songs into one song value -> add up every instance of a mmod tag
PATH_TAGS = 'I:\Science\CIS\wyb15135\datasets_unmodified\\annotations_final.csv'
PATH_META = 'I:\Science\CIS\wyb15135\datasets_unmodified\clip_info_final.csv'
PATH_LAST = 'I:\Science\CIS\wyb15135\datasets_unmodified\MoodyLyrics4Q\MoodyLyrics4Q.csv'
PATH_WORDS = 'I:\Science\CIS\wyb15135\datasets_unmodified\\13428_2012_314_MOESM1_ESM\BRM-emot-submit.csv'
PATH_TRUTH = 'I:\Science\CIS\wyb15135\datasets_created\ground_truth.csv'

genre_columns = ['hard rock', 'jazz', 'soft rock', 'electric', 'folk', 'synth', 'funk',
                 'new age', 'not classical', 'not rock', 'opera', 'country', 'electro', 'reggae', 'tribal',
                 'irish', 'electronica', 'arabic', 'instrumental', 'heavy metal', 'modern', 'disco', 'industrial',
                 'pop', 'celtic', 'punk', 'spanish', 'blues', 'indian', 'rock', 'dance', 'techno', 'house', 'not opera',
                 'not english', 'oriental', 'metal', 'hip hop', 'rap', 'baroque', 'english', 'world', 'clasical',
                 'foreign', 'middle eastern', 'medieval', 'acoustic', 'not rock', 'jungle', 'india', 'eastern',
                 'classical', 'classic', 'electronic', 'lol']
instrument_columns = ['no voice', 'singer', 'duet', 'plucking', 'bongos', 'harpsichord', 'female singing', 'sitar',
                      'chorus',
                      'female opera', 'male vocal', 'vocals', 'clarinet', 'silence', 'beats', 'men', 'woodwind',
                      'no strings', 'chimes', 'no piano', 'horns', 'female', 'no voices', 'guitar', 'no beat', 'beat',
                      'banjo', 'solo', 'violins', 'female voice', 'wind', 'no singing', 'trumpet', 'percussion', 'drum',
                      'voice', 'birds', 'strings', 'bass', 'harpsicord', 'male voice', 'girl', 'keyboard', 'string',
                      'drums', 'chanting', 'no violin', 'no guitar', 'organ', 'no vocal', 'talking', 'soprano',
                      'acoustic guitar', 'electric guitar', 'male singer', 'man singing', 'classical guitar', 'violin',
                      'male opera', 'no vocals', 'horn', 'chant', 'drone', 'synthesizer', 'bells', 'man', 'fast beat',
                      'harp', 'no flute', 'lute', 'female vocal', 'oboe', 'viola', 'echo', 'piano', 'male vocals',
                      'flutes',
                      'sax', 'male', 'vocal', 'no singer', 'woman', 'woman singing', 'piano solo', 'guitars',
                      'no drums',
                      'singing', 'cello', 'female vocals', 'voices', 'clapping', 'monks', 'flute', 'noise', 'choir',
                      'female singer', 'water', 'women', 'fiddle', 'orchestra']
meta_columns = ['url', 'track_number', 'segmentStart', 'segmentEnd', 'original_url', 'clip_id', 'mp3_path_x',
                'mp3_path_y', 'album']
mood_tags = ['angry', 'relaxed', 'happy', 'sad', 'heavy', 'funky', 'eerie', 'spacey', 'quiet', 'ambient', 'airy',
             'repetitive', 'space', 'loud', 'choral', 'weird', 'fast', 'dark', 'operatic', 'low', 'trance', 'strange',
             'deep', 'hard', 'mellow', 'orchestral', 'light', 'old', 'sad', 'slow', 'scary', 'jazzy', 'calm',
             'different', 'upbeat', 'soft', 'quick']


# linked by clip id
def load_tagatune_data():
    tag_data = pd.read_csv(PATH_TAGS)
    meta_data = pd.read_csv(PATH_META)
    data = pd.merge(tag_data, meta_data, on="clip_id")
    return data


def load_lastfm_data():
    return pd.read_csv(PATH_LAST)


def load_words_data():
    return pd.read_csv(PATH_WORDS)


def drop_non_mood_tags(data):
    data = data.drop(columns=genre_columns)
    data = data.drop(columns=instrument_columns)
    data = data.drop(columns=meta_columns)
    return data


# for clips of the same song, aggregate tags into one entry
def compress_song_clips(data):
    return data.groupby(['title', 'artist'], as_index=False).max()


def concat_dataframes(last_data, tag_data):
    l_data = format_last_data(last_data)
    t_data = format_tag_data(tag_data)
    t_data = t_data.append(l_data, ignore_index=True, sort=True)
    return t_data


# match formatting of tagatune mood database to last.fm database
def format_tag_data(data):
    data = drop_non_mood_tags(data)
    data = compress_song_clips(data)

    data['mood'] = np.empty((len(data), 0)).tolist()
    data['angry'] = 0
    data['relaxed'] = 0

    # modifying mood tags as some tags don't have values in the arousal-valence dataset
    for i, row in data.iterrows():
        for m_tag in mood_tags:
            if row[m_tag] == 1:
                if m_tag == 'operatic':
                    data.at[i, 'mood'] = data.loc[i, 'mood'] + ['opera']
                elif m_tag == 'choral':
                    data.at[i, 'mood'] = data.loc[i, 'mood'] + ['chorus']
                elif m_tag == 'orchestral':
                    data.at[i, 'mood'] = data.loc[i, 'mood'] + ['orchestra']
                elif m_tag == 'spacey':
                    data.at[i, 'mood'] = data.loc[i, 'mood'] + ['space']
                else:
                    data.at[i, 'mood'] = data.loc[i, 'mood'] + [m_tag]

    data = data.drop(columns=mood_tags)
    # drop data with no mood information
    data = data[data['mood'].map(lambda d: len(d)) > 0]
    return data


# format all moods as a list of moods
def format_last_data(data):
    data = data.drop(columns='index')
    for i, row in data.iterrows():
        data.at[i, 'mood'] = [row['mood']]
    return data


# search words database for the arousal-valence values associated with mood tag
def annotate_tags_arousal_valence(words_data, tag_data):
    annotated_data = tag_data
    annotated_data['arousal'] = 0.0
    annotated_data['valence'] = 0.0
    # find the arousal and valence emotion values associated with every tag, if song has multiple tags
    # then average values
    for i, row in tag_data.iterrows():
        arousal_vals = []
        valence_vals = []
        for tag in row['mood']:
            word_entry = words_data.loc[words_data['Word'] == tag]
            if not word_entry.empty:
                arousal_vals.append(find_avg_arousal(word_entry))
                valence_vals.append(find_avg_valence(word_entry))
        if len(arousal_vals) > 0 and len(valence_vals) > 0:
            annotated_data.at[i, 'valence'] = (sum(valence_vals) / len(valence_vals))
            annotated_data.at[i, 'arousal'] = (sum(arousal_vals) / len(arousal_vals))

    return annotated_data


def find_avg_arousal(entry):
    # dataset stores arousal values for males, females, old, young, highly-educated and lowly-educated participants
    # we are averaging all values for an avg arousal
    arousal = entry['A.Mean.M'].values[0]
    arousal += entry['A.Mean.F'].values[0]
    arousal += entry['A.Mean.O'].values[0]
    arousal += entry['A.Mean.Y'].values[0]
    arousal += entry['A.Mean.H'].values[0]
    arousal += entry['A.Mean.L'].values[0]
    arousal = arousal / 6
    return arousal


def find_avg_valence(entry):
    # dataset stores arousal values for males, females, old, young, highly-educated and lowly-educated participants
    # we are averaging all values for an avg valence
    valence = entry['V.Mean.M'].values[0]
    valence += entry['V.Mean.F'].values[0]
    valence += entry['V.Mean.O'].values[0]
    valence += entry['V.Mean.Y'].values[0]
    valence += entry['V.Mean.H'].values[0]
    valence += entry['V.Mean.L'].values[0]
    valence = valence / 6
    return valence


def drop_data_points_withno_av(data):
    return data[(data['arousal'] != 0) & (data['valence'] != 0)]


def main():
    # this file creates and process the gorud truth dataset from 3 datasets - Last.fm MoodyLyrics, TagATune, 
    # Norms Of Valence for English words

    tag_data = load_tagatune_data()
    last_data = load_lastfm_data()
    combined_data = concat_dataframes(last_data, tag_data)
    words_data = load_words_data()

    ground_truth = annotate_tags_arousal_valence(words_data, combined_data)
    ground_truth = drop_data_points_withno_av(ground_truth)

    print('Example: ')
    print(ground_truth.loc[500, :])
    print(ground_truth)

    ground_truth.to_csv(PATH_TRUTH, encoding='utf-8', index=False)


if __name__ == '__main__':
    main()
