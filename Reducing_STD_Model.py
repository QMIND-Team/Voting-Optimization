# -*- coding: utf-8 -*-
"""
Created on Sat, Nov  17, 2018

@author: Caelum Kamps, Sean Kato, Dan, Denis, Ali
"""


import pandas as pd
import getData

#%% Preliminary initializations and imports
data = pd.read_pickle('OurSortedData') # Pickled data
data = data.drop(5219) #This was the row giving us trouble
data = data.drop(13988)
civic_addy = getData.get_data()[1]['addy']
del civic_addy[5219]
del civic_addy[13988]
#data.dropna(inplace=True)
#data.reset_index(drop=True, inplace=True)
voting_loc, _ = getData.get_data() # Voting locations
voting_loc = voting_loc.sort_values('num') # Sorted voting locations
ideal_num = (len(data))/(len(voting_loc)) #Ideal number of addresses per location
ratio_tolerance = 1.1 #Arbitrary distance ratio tolerance (voting_loc_n+1/voting_loc_n)
quot = pd.DataFrame(columns = ['civic addy', 'quot1', 'quot2'])
quot['civic addy'] = civic_addy
too_many = []    
quot1 = [0]*len(data) #array for first difference, initialize to zero
quot2 = [0]*len(data) #array for second difference, initialize to zero

# Column for each voting location
model_output = pd.DataFrame(columns = ['location '+str(i) for i in range(54)])

# Model statistics
model_statistics = pd.DataFrame(columns = ['num of addys', 'mean', 'std', 'median', 'max'])
placeholder_column = [None for i in range(54)]
for column in model_statistics.columns:
    model_statistics[column] = placeholder_column

# Placeholder to get voting locations
columns = [[] for i in range(54)]

#%% Basic function to map civic addresses to voting locations
for i in range(len(data)):
    try:
        columns[int(data['v_loc1'].iloc[i][0]) - 1].append(float(data['v_loc1'].iloc[i][1]))
    
    # This except statement is to handle any shitty or missing data
    except:
        # No bueno
        continue

#%%Expanded function to seek equal distribution (reduce standard deviation)
for i in range(len(voting_loc)):
    if (len(columns[i]) > ideal_num):
        too_many.append(i) #which locations have too many people
        


#calculating ratio between civic addy's first&second voting locations, and second&third voting locations
for i in range(len(data)):
    try:
        quot1[i] = float(float(data['v_loc2'].iloc[i][1])/float(data['v_loc1'].iloc[i][1]))
        quot2[i] = float(float(data['v_loc3'].iloc[i][1])/float(data['v_loc2'].iloc[i][1]))
    # This except statement is to handle any shitty or missing data 
    except:
        #No bueno
        continue
    
quot['quot1'] = quot1
quot['quot2'] = quot2

#now we must find the associated civic addies with the voting locations that have too many people
#v_loc1_dict = dict(data['v_loc1']) #for easy searching of values in column
too_many_vloc_with_civic_addies = pd.DataFrame(columns = ['voting loc', 'civic addies'])
too_many_vloc_with_civic_addies['voting loc'] = too_many
#i = 0
##instantiate the civic addty list of "too many" vlocs
#addy_list_big = [[] for j in range(len(too_many))]  
#
#
#for j in range(len(too_many)):
#    i = 0
#    while (i < 5219):
#        if data['v_loc1'].iloc[i][0] == too_many[j]:
#           addy_list_big[j].append(data['addy'][i])
#            #add all associated civic addies to too_many_vloc_with_civic_addies['civic addies']          
#        i += 1
#    i += 1
#    while (i < 13988):
#        if data['v_loc1'].iloc[i][0] == too_many[j]:
#            addy_list_big[j].append(data['addy'][i])
#        i += 1
#    i += 1
#    while (i < 38407):
#        if data['v_loc1'].iloc[i][0] == too_many[j]:
#            addy_list_big[j].append(data['addy'][i])
#        i += 1
#    i = 38410
#    while (i < 59160):
#        if data['v_loc1'].iloc[i][0] == too_many[j]:
#            addy_list_big[j].append(data['addy'][i])
#        i += 1
#    i = 59174
#    while (i < len(data)):
#        if data['v_loc1'].iloc[i][0] == too_many[j]:
#            addy_list_big[j].append(data['addy'][i])
#        i += 1 
#for j in range(len(too_many)):
#    too_many_vloc_with_civic_addies['civic addies'].iloc[j] = addy_list_big[j]
too_many_vloc_with_civic_addies = pd.read_pickle('too_many_vloc_with_civic_addies')

#Now we have everything we need: quot (which has the ratioss of each civic addy's top choices),
#and too_many_vloc_with_civic_addies (which has the voting locations that have too 
#many addresses, with the corresponding civic address to that location). We now must iterate 
#through these civic addies and see which ones have a quot less than the "threshold". If quot
#is less than threshold, then send that civic addy to its next best choice. 
for j in range(len(too_many)):
    for i in range(len(too_many_vloc_with_civic_addies['civic addies'][j])):
        for k in range(len(quot)):
            if too_many_vloc_with_civic_addies['civic addies'][j][i] == quot['civic addy'][k]:
                if quot['quot1'][k] < ratio_tolerance:
                    row = data[data.addy == too_many_vloc_with_civic_addies['civic addies'][j][i]]
                    row['vloc1'] = row['vloc2']
                    
        


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
