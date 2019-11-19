# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 21:28:52 2019

@author: Shatha
"""
import pandas as pd


# process the tagatun dataset
# compine clips of the same songs into one song value -> add up every instance of a mmod tag 
PATH_TAGS = 'I:\Science\CIS\wyb15135\datasets_unmodified\\annotations_final.csv'
PATH_META = 'I:\Science\CIS\wyb15135\datasets_unmodified\clip_info_final.csv'
PATH_LAST = 'I:\Science\CIS\wyb15135\datasets_unmodified\MoodyLyrics4Q\MoodyLyrics4Q.csv'

genre_columns = ['hard rock', 'jazz', 'soft rock', 'electric', 'folk', 'synth', 'funk', 
                 'new age', 'not classical', 'not rock', 'opera', 'country', 'electro', 'reggae', 'tribal',
                 'irish', 'electronica', 'arabic', 'instrumental', 'heavy metal', 'modern', 'disco', 'industrial',
                 'pop','celtic', 'punk', 'spanish', 'blues', 'indian', 'rock', 'dance', 'techno', 'house', 'not opera',
                 'not english', 'oriental', 'metal', 'hip hop', 'rap', 'baroque', 'english', 'world', 'clasical',
                 'foreign', 'middle eastern', 'medieval', 'acoustic', 'not rock', 'jungle', 'india', 'eastern', 
                 'classical', 'classic', 'electronic', 'lol']
instrument_columns = ['no voice', 'singer', 'duet', 'plucking', 'bongos', 'harpsichord', 'female singing', 'sitar', 'chorus', 
                      'female opera', 'male vocal', 'vocals' , 'clarinet', 'silence', 'beats', 'men', 'woodwind', 
                      'no strings','chimes', 'no piano', 'horns', 'female', 'no voices', 'guitar', 'no beat', 'beat', 
                      'banjo', 'solo', 'violins', 'female voice', 'wind', 'no singing', 'trumpet', 'percussion', 'drum',
                      'voice', 'birds', 'strings', 'bass', 'harpsicord', 'male voice', 'girl', 'keyboard', 'string',
                      'drums', 'chanting', 'no violin', 'no guitar', 'organ', 'no vocal', 'talking', 'soprano', 
                      'acoustic guitar', 'electric guitar', 'male singer', 'man singing', 'classical guitar', 'violin',
                      'male opera', 'no vocals', 'horn', 'chant', 'drone', 'synthesizer' , 'bells', 'man', 'fast beat',
                      'harp', 'no flute', 'lute', 'female vocal', 'oboe', 'viola', 'echo', 'piano', 'male vocals', 'flutes',
                      'sax', 'male', 'vocal', 'no singer', 'woman', 'woman singing', 'piano solo', 'guitars', 'no drums',
                      'singing', 'cello', 'female vocals', 'voices', 'clapping', 'monks', 'flute', 'noise', 'choir', 
                      'female singer', 'water', 'women', 'fiddle', 'orchestra']
meta_columns = ['url', 'track_number', 'segmentStart', 'segmentEnd', 'original_url', 'clip_id', 'mp3_path_x', 
                'mp3_path_y', 'album']

# linked by clip id 
def load_tagatune_data():
    tag_data = pd.read_csv(PATH_TAGS)
    meta_data =  pd.read_csv(PATH_META)
    data = pd.merge(tag_data, meta_data, on="clip_id")
    return data

def load_lastfm_data():
    return pd.read_csv(PATH_LAST)

def drop_non_mood_tags(data):
    data = data.drop(columns=genre_columns)
    data = data.drop(columns=instrument_columns)
    data = data.drop(columns=meta_columns)
    return data 

# for clips of the same song, aggregate tags into one entry
def compress_song_clips(data):
    ## TODO need to combine 'space' and 'spacey' cols
    return data.groupby(['title', 'artist'], as_index=False).max()


def concat_dataframes(last_data, tag_data):
    l_data = format_last_data(last_data)
    t_data = format_tag_data(tag_data)
    t_data.append(l_data, ignore_index=True, sort=True)
    print(t_data.head())
    return t_data

    
def format_tag_data(data):
    data['angry'] = 0
    data['relaxed'] = 0
    data = drop_non_mood_tags(data)
    data = compress_song_clips(data)
    return data    


# match formattign of last_fm mood database to tagatune database    
def format_last_data(data):
    data['angry'] = 0; data['relaxed'] = 0; data['happy'] = 0; data['sad'] = 0; data['heavy'] = 0 
    data['funky'] = 0; data['eerie'] = 0; data['spacey'] = 0; data['quiet'] = 0; data['ambient'] = 0
    data['airy'] = 0; data['repetitive'] = 0; data['space'] = 0; data['loud'] = 0; data['choral'] = 0
    data['weird'] = 0; data['fast'] = 0; data['dark'] = 0; data['operatic'] = 0; data['low'] = 0
    data['trance'] = 0; data['strange'] = 0; data['deep'] = 0; data['hard'] = 0; data['mellow'] = 0
    data['orchestral'] = 0; data['light'] = 0; data['old'] = 0; data['sad'] = 0; data['slow'] = 0
    data['scary'] = 0; data['jazzy'] = 0; data['calm'] = 0; data['different'] = 0 
    data['upbeat'] = 0; data['soft'] = 0; data['quick'] = 0
    data = data.drop(columns='index')
    
    for i, row in data.iterrows():
        if row['mood'] == 'happy':
            data.at[i,'happy'] = 1
        elif row['mood'] == 'sad':
            data.at[i,'sad'] = 1
        elif row['mood'] == 'relaxed':
            data.at[i,'relaxed'] = 1
        else: 
            data.at[i,'angry'] = 1
    
    data = data.drop(columns='mood')
    return data
    

def main():
    # this file creates and process the gorud truth dataset from 3 datasets - Last.fm MoodyLyrics, TagATune, 
    # Norms Of Valence for English words
    
    tag_data = load_tagatune_data()
    last_data = load_lastfm_data()
    tag_data = concat_dataframes(last_data, tag_data)
    
    # print('Example: ')
    # print(processed_data.loc[0,:])
    

if __name__ == '__main__':
    main()

