import sqlite3
import h5py
import pandas as pd
import tensorflow as tf

# .db file from additional files of dataset
metadata = sqlite3.connect("C:/Users/User/PycharmProjects/mer-ml/resources/subset_track_metadata.db")
metaDataFrame = pd.read_sql_query("select * from songs", metadata)

# a single track information from dataset
# throws a conversion error
# song = pd.read_hdf("C:/Users/User/PycharmProjects/mer-ml/resources/TRABBKX128F4285205.h5")
song = h5py.File("C:/Users/User/PycharmProjects/mer-ml/resources/TRABBKX128F4285205.h5", 'r')

# load into tensorflow
id = metaDataFrame.pop('track_id')
# dataset = tf.data.Dataset.from_tensor_slices(metaDataFrame.values)
# for feat, targ in dataset.take(5):
#     print('Features and Target: {}'.format(feat, targ))

print("Keys of metadata table: " + metaDataFrame.keys())

keys = list(song.keys())
print("Keys of song dataset: ")
print(*keys)
