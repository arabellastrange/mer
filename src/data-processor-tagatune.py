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
                'mp3_path_y']

# linked by clip id 
def load_tagatune_data():
    tag_data = pd.read_csv(PATH_TAGS)
    meta_data =  pd.read_csv(PATH_META)
    data = pd.merge(tag_data, meta_data, on="clip_id")
    return data

def drop_non_mood_tags(data):
    data = data.drop(columns=genre_columns)
    data = data.drop(columns=instrument_columns)
    data = data.drop(columns=meta_columns)
    return data 


# for clips of the same song, aggregate tags into one entry
def compress_song_clips(data):  
    return data.groupby(['title', 'artist'], as_index=False).max()


def append_moody_cols(data):
    data['angry'] = 0
    data['relaxed'] = 0
    return data


def load_lastfm_data():
    return pd.read_csv(PATH_LAST)
    
    
def concat_dataframes(last_data, tag_data):
    print()
    

def main():
    tag_data = load_tagatune_data()
    processed_data = drop_non_mood_tags(tag_data)
    processed_data = compress_song_clips(processed_data)
    processed_data = append_moody_cols(processed_data)
    
    last_data = load_lastfm_data()
    processed_data = concat_dataframes(last_data, processed_data)
    
    print('Example: ')
    print(processed_data.loc[0,:])
    

if __name__ == '__main__':
    main()

