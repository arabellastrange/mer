# Install TensorFlow
import sqlite3

import pandas as pd
import tensorflow as tf

# .db file from additional files of dataset
metadata = sqlite3.connect("C:/Users/User/PycharmProjects/mer-ml/resources/subset_track_metadata.db")
metaDataFrame = pd.read_sql_query("select * from songs", metadata)
# a single track information from dataset
song = pd.read_hdf("C:/Users/User/PycharmProjects/mer-ml/resources/TRABBKX128F4285205.h5")

# load into tensorflow
dataset = tf.data.Dataset.from_tensor_slices(metaDataFrame.values)

for feat in dataset.take(5):
    print('Features: {}'.format(feat))
