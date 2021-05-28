#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 26 13:41:16 2021

@author: Caroline
"""

#import time
import os
import pickle
#import psana as ps

path = '/Users/Caroline/PycharmProjects/LCLS_LV_27_Data_Analysis/sample_data/'
#ds = ps.DataSource(dir)

try:
    with open('savedSet.txt','rb') as f:
        savedSet = pickle.load(f) #open pickle file if it exists
except:
    savedSet = set()
    print('except')

nameSet = set()

for file in os.listdir(path):
    fullpath = os.path.join(path, file)
    if os.path.isfile(fullpath):
        nameSet.add(file) #add all run names to nameSet
    else:
        print('error: file not found in path')

newSet = nameSet - savedSet
savedSet = nameSet

f = open('savedSet.txt','wb')
pickle.dump(savedSet,f)
f.close #save new run names in a pickle file
    
if newSet:
    newruns = []
    process_raw = True
    newList = list(newSet)
    newList.sort()
    for i in range(0,len(newList)):
        newruns.append(newList[i].replace('run_',''))
        print(newruns[i])
    print('new files: ',newList)
    runs = list(range(newruns[0],int(newruns[len(newruns)-1]) + 1))
    x_axis = 'pixels'
else:
    print('No new runs')

#else : 
#    time.sleep(60) #checks again in n seconds
