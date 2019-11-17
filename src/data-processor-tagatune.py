# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 21:28:52 2019

@author: Shatha
"""
import pandas as pd


# process the tagatun dataset
# compine clips of the same songs into one song value -> add up every instance of a mmod tag 
PATH = 'I:\Science\CIS\wyb15135\datasets_unmodified\annotations_final.csv'

data = pd.read_csv(PATH)

