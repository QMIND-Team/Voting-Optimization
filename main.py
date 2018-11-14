# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 18:36:18 2018

@author: Caelum Kamps, Skato, Dan, Denis, Ali
"""


import pandas as pd
import getData
from matplotlib import pyplot as plt
import googlemaps
gmaps = googlemaps.Client(key='AIzaSyDpDRMQ-jmQ0wNpPt3BGyBmgPb8UmsJOEw')


voting_loc, civic_loc = getData.get_data()
num = len(voting_loc)


clusters = [[] for i in range(num)] # holds civic 
distances = pd.DataFrame(columns=['civic_addy','v_loc1','v_loc2','v_loc3'])

civic_loc['v_loc1'] = [0]*len(civic_loc)
civic_loc['v_loc2'] = [0]*len(civic_loc)
civic_loc['v_loc3'] = [0]*len(civic_loc)

#for i in range(len(civic_loc)):
for i in range(len(civic_loc)):
    # Find the distance between house and each voting location using gmaps api
    dist = gmaps.distance_matrix(voting_loc['addy'],civic_loc.loc[i,'addy'])
    for j in range(len(voting_loc)):
        voting_loc.loc[j,'sort_val'] = dist['rows'][j]['elements'][0]['distance']['text'].partition(' ')[0]
  
    
    # Sort the voting locations based on distance to house 
    voting_loc = voting_loc.sort_values('sort_val')
    
    
    # Store the top three closest voting locations to each civic address
    civic_loc['v_loc1'].iloc[i] = (voting_loc.loc[0,'num'],voting_loc['sort_val'].iloc[0])
    civic_loc['v_loc2'].iloc[i] = (voting_loc.loc[1,'num'],voting_loc['sort_val'].iloc[1])
    civic_loc['v_loc3'].iloc[i] = (voting_loc.loc[2,'num'],voting_loc['sort_val'].iloc[2])
    
  