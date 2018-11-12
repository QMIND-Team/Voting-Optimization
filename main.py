# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 18:36:18 2018

@author: Caelum Kamps, Skato, Dan, Denis, Ali
"""


import pandas as pd
import getData
from matplotlib import pyplot as plt


voting_loc, civic_loc = getData.get_data()
num = len(voting_loc)


clusters = [[] for i in range(num)] # holds civic 
distances = [[] for i in range(len(civic_loc))]


for i in range(len(civic_loc)):
    
    # Find the absolute distance between house and each voting location
    voting_loc['sort_val'] = (
        (civic_loc['lat'][i] - voting_loc['lat'])**2
         + abs(civic_loc['long'][i] - voting_loc['long'])**2)**0.5
    
    # Sort the voting locations based on distance to house then drop the sort column
    voting_loc = voting_loc.sort_values('sort_val').drop('sort_val', 1)
    
    # Store the top ten closest voting locations to each civic address
    distances[i] = voting_loc['num'][0:9]
     