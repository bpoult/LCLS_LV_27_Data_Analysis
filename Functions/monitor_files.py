#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 26 13:41:16 2021

@author: Caroline
"""
#         raw_data = load_data.load_data(save_dir,scan_name,ds_string,epix_roi,xrt_roi)

import time
import os
import pickle
import psana as ps
import numpy as np
from .load_data import load_data
def monitor_and_process(save_dir,xtc_smd_dir,load_data_input):
#ds = ps.DataSource(dir)
    ignore_runs = set([1,2])

#     if os.path.exists(save_dir + 'savedSet.pkl'):
#         with open(save_dir + 'savedSet.pkl','rb') as f:
#             savedSet = pickle.load(f) #open pickle file if it exists
#     else:
#         savedSet = set(ignore_runs)
#         print('except')

    x = os.listdir(xtc_smd_dir)
    run_files = [int(x[i][11:15]) for i in range(0,len(x)) if '-r' in x[i]]
    unique_runs = np.unique(run_files)
    nameSet = set([unique_runs[i] for i in range(0,len(unique_runs)) if run_files.count(unique_runs[i]) == 4])
    nameSet = nameSet - ignore_runs
#     newSet = nameSet - savedSet
#     savedSet = nameSet
    
#     with open(save_dir + 'savedSet.pkl','wb') as f:
#         pickle.dump(savedSet,f)
#     f.close #save new run names in a pickle file
    if nameSet:
        newList = list(nameSet)
        newList.sort()
        for i in range(0,len(newList)):
            scan_name = 'run_' + str(newList[i])
            if not os.path.exists(load_data_input[0] + scan_name + "/" + "rawdata.pkl"):
                ds_string = 'exp=cxix46119:run='+str(newList[i])+':smd'
                raw_data = load_data(load_data_input[0],scan_name,ds_string,load_data_input[1],load_data_input[2])
            else: 
                print('No new runs')

    
    #else : 
    #    time.sleep(60) #checks again in n seconds
