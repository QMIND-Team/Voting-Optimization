# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 18:36:18 2018

@author: Caelum Kamps, Sean Kato, Dan, Denis, Ali
"""


import pandas as pd
import getData

#%% Preliminary initializations and imports
data = pd.read_pickle('OurSortedData') # Pickled data
voting_loc, _ = getData.get_data() # Voting locations
voting_loc = voting_loc.sort_values('num') # Sorted voting locations

# Column for each voting location
model_output = pd.DataFrame(columns = ['location '+str(i) for i in range(54)])

# Model statistics
model_statistics = pd.DataFrame(columns = ['num of addys', 'mean', 'std', 'median', 'max'])
placeholder_column = [None for i in range(54)]
for column in model_statistics.columns:
    model_statistics[column] = placeholder_column

# Placeholder to get voting locations
columns = [[] for i in range(54)]

#%% Actual function to map civic addresses to voting locations
for i in range(len(data)):
    try:
        columns[int(data['v_loc1'].iloc[i][0]) - 1].append(float(data['v_loc1'].iloc[i][1]))
    
    # This except statement is to handle any shitty or missing data
    except:
        # No bueno
        continue

#%% Storing function output in a pandas dataframe
        
# Calculate the max column length so pandas doesnt get mad
length = max([len(columns[i]) for i in range(54)])

# Making all of the columns the same length so pandas doesnt get mad
for column in columns:
    for i in range(length):
        try:
            a = column[i]
        except:
            column.append(None)


for i in range(54):
    model_output['location '+str(i)] = columns[i]   
    
    
#%% Calculating Model Statistics for each voting location

for i in range(54):
    model_statistics.loc[i,'num of addys'] = model_output['location '+str(i)].count()
    model_statistics.loc[i,'mean'] = model_output['location '+str(i)].mean()
    model_statistics.loc[i,'std'] = model_output['location '+str(i)].std()
    model_statistics.loc[i,'max'] = model_output['location '+str(i)].max()
    model_statistics.loc[i,'std'] = model_output['location '+str(i)].std()
    model_statistics.loc[i,'max'] = model_output['location '+str(i)].max()
    model_statistics.loc[i,'median'] = model_output['location '+str(i)].median()    
 
# Some examples of things we might care about
print('Std # of ppl per voting location = ', model_statistics['num of addys'].std())
print('Mean mean per voting location = ', model_statistics['mean'].mean())     
print('Worst std per voting location = ', model_statistics['std'].max())      
    
      
      
      
      
      
      