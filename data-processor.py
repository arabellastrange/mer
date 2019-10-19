# Install TensorFlow
import tensorflow as tf
import pandas as pd
import sqlite3

# .db file from additional files of dataset
metadata = sqlite3.connect("/resources/subset_track_metadata.db")
metaDataFrame = pd.read_sql_query("select * from songs", metadata)
# a single track information from dataset
song = pd.read_hdf("/resources/TRABBKX128F4285205.h5")

# load into tensorflow
dataset = tf.data.Dataset.from_tensor_slices(metaDataFrame.values)
