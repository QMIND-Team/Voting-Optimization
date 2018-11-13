# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 18:36:18 2018

@author: Caelum Kamps, Skato, Dan, Denis, Ali
"""

import json
import pandas as pd

def get_data():
    # Inputing and formatting voting location data
    with open('municipal-voting-locations-2018.geojson') as f:
        voting_data = json.load(f)
        
    vloc_info = pd.DataFrame()
    longitudes = []
    latitudes = []
    addresses = []
    location_number = []
    for i in range(len(voting_data['features'])):
        longitudes.append(voting_data['features'][i]['geometry']['coordinates'][0])
        latitudes.append(voting_data['features'][i]['geometry']['coordinates'][1])
        addresses.append(voting_data['features'][i]['properties']['votinglocationaddress']+', Kingston, ON')
        location_number.append(voting_data['features'][i]['properties']['votinglocationnumber'])
        
    vloc_info['num'] = location_number
    vloc_info['addy'] = addresses
    vloc_info['lat'] = latitudes
    vloc_info['long'] = longitudes
    
    # Inputting and formatting civic address data
    with open('civic-addresses.geojson') as f:
        civic_data = json.load(f)
    
    cloc_info = pd.DataFrame()
    longitudes = []
    latitudes = []
    addresses = []
    for i in range(len(civic_data['features'])):
        longitudes.append(civic_data['features'][i]['geometry']['coordinates'][0])
        latitudes.append(civic_data['features'][i]['geometry']['coordinates'][1])
        address = (civic_data['features'][i]['properties']['address_number']+
                 ' '+civic_data['features'][i]['properties']['street']+' Kingston, ON')
        addresses.append(address)
     
    cloc_info['addy'] = addresses
    cloc_info['lat'] = latitudes
    cloc_info['long'] = longitudes       
    return vloc_info, cloc_info
