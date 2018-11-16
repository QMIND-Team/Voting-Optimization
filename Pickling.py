# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 15:16:12 2017

@author: Caelum.Kamps
"""

import pickle

def pickleIt(Object,Filename):
    pickle.dump(Object,open(Filename,'wb'))

def unPickleIt(Filename):    
   data =pickle.load(open(Filename,'rb'))
   return(data)
