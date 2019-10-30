# use python lyrcis librabry to fetch lyrics by song name
from PyLyrics import *
import pandas as pd

#fetch song - next step iterate over all songs from the DataFrame
artist = 'Foster The People'
title = 'SHC'
lyrics = PyLyrics.getLyrics(artist, title)

#make dataframe put lyrics, title, artist
data = [[artist, title, lyrics]]
dataFrame = pd.DataFrame(data, columns=['artist', 'title', 'lyrics'])

#output
print(dataFrame)