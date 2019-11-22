import pylast
import pandas as pd

# possibly useful compiled dataset:
# https://www.researchgate.net/publication/317382609_Music_Mood_Dataset_Creation_Based_on_Last_FM_Tags
PATH = 'I:/Science/CIS/wyb15135/datasets_created/tags-dataset.csv'

client_id = "28f491a22753592dfe63a6a08b11a39a"
client_secret = "960c32508b94014652dffed90991e6cf"

username = "balqeesrose"
pass_hash = pylast.md5("GRV6$VjgfgGKG/j")

network = pylast.LastFMNetwork(api_key=client_id, api_secret=client_secret,
                               username=username, password_hash=pass_hash)


def example_song(): 
    # TODO fetch a song - iterate over all songs next
    artist = 'Arctic Monkeys'
    title = 'Do I Wanna Know'
    track = network.get_track(artist, title)
    tags = track.get_top_tags()

    # possibly useful for lyrics and sentiment analysis
    wiki = track.get_wiki_content()
    
    # make dataframe put tags, title, artist
    data = [[artist, title, tags]]
    dataFrame = pd.DataFrame(data, columns=['artist', 'title', 'tags'])
    print(dataFrame)

    # output
    dataFrame.to_csv(PATH)
    

def find_song_tags(song_name, artist_name):
    track = network.get_track(song_name, artist_name)
    tags = track.get_top_tags()
    data = [[song_name, artist_name, tags]]
    dataFrame = pd.DataFrame(data, columns=['artist', 'title', 'tags'])
    return dataFrame


def append_song_to_file(data):
    with open(PATH, 'a') as f:
        data.to_csv(f, header=False)
        

def drop_empty_tags(data):
    data.dropna()
    

def main():
    example_song()
    
    
if __name__ == '__main__':
    main()


