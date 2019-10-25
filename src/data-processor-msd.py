import sqlite3
import h5py
import tensorflow as tf
import pandas as pd
import numpy as np


# .db file from additional files of dataset
metadata = sqlite3.connect("C:/Users/User/PycharmProjects/mer-ml/resources/subset_track_metadata.db")

# a single track information from dataset
# TODO convert file to panda dataframe
song = h5py.File("C:/Users/User/PycharmProjects/mer-ml/resources/TRABBKX128F4285205.h5", 'r')

# create panda dataframe from data
metaDataFrame = pd.read_sql("select * from songs", metadata)

# investigate loaded files
print("Keys of metadata table: " + metaDataFrame.keys())
print(metaDataFrame.head(5).get("title"))

keys = list(song.keys())
print("Keys of song dataset: ")
print(*keys)
print("Song metadata keys: ")
print(song.get("metadata").keys())
print("Song analysis keys: ")
print(song.get("analysis").keys())
print("Song musicbrainz keys: ")
print(song.get("musicbrainz").keys())

# load into tensorflow
# dataset = tf.data.Dataset.from_tensor_slices(metaDataFrame.values)
# for feat in dataset:
#     print('Features: {}'.format(feat))
