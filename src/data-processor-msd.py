import sqlite3
import h5py
import tensorflow as tf
import pandas as pd
import os
import sys
import glob
import time
import datetime

# Paths
msd_subset_path = '/home/user/PycharmProjects/MillionSongSubset'
msd_subset_data_path = os.path.join(msd_subset_path, 'data')
msd_subset_addf_path = os.path.join(msd_subset_path, 'AdditionalFiles')
msd_code_path = "/home/user/PycharmProjects/MSongsDB-master"
sys.path.append(os.path.join(msd_code_path, 'PythonSrc'))

# MSD imports
import hdf5_getters as GETTERS

# the following function simply gives us a nice string for
# a time lag in seconds
def strtimedelta(starttime,stoptime):
    return str(datetime.timedelta(seconds=stoptime-starttime))

# we define this very useful function to iterate the files
def apply_to_all_files(basedir, func=lambda x: x, ext='.h5'):
    """
    From a base directory, go through all subdirectories,
    find all files with the given extension, apply the
    given function 'func' to all of them.
    If no 'func' is passed, we do nothing except counting.
    INPUT
       basedir  - base directory of the dataset
       func     - function to apply to all filenames
       ext      - extension, .h5 by default
    RETURN
       number of files
    """
    cnt = 0
    # iterate over all files in all subdirectories
    for root, dirs, files in os.walk(basedir):
        files = glob.glob(os.path.join(root, '*' + ext))
        # count files
        cnt += len(files)
        # apply function to all files
        for f in files:
            func(f)
    return cnt


# we can now easily count the number of files in the dataset
print('number of song files:', apply_to_all_files(msd_subset_data_path))
# let's now get all artist names in a set(). One nice property:
# if we enter many times the same artist, only one will be kept.
all_artist_names = set()


# we define the function to apply to all files
def func_to_get_artist_name(filename):
    """
    This function does 3 simple things:
    - open the song file
    - get artist ID and put it
    - close the file
    """
    h5 = GETTERS.open_h5_file_read(filename)
    artist_name = GETTERS.get_artist_name(h5)
    all_artist_names.add(artist_name)
    h5.close()


# let's apply the previous function to all files
# we'll also measure how long it takes
t1 = time.time()
apply_to_all_files(msd_subset_data_path, func=func_to_get_artist_name)
t2 = time.time()
print('all artist names extracted in:', strtimedelta(t1, t2))

#############################################################################

# .db file from additional files of dataset
metadata = sqlite3.connect("/resources/subset_track_metadata.db")

# a single track information from dataset
# TODO convert file to panda dataframe
song = h5py.File("/resources/TRABBKX128F4285205.h5", 'r')

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
