import matplotlib.pyplot as plt
import os
import sys
import numpy as np
import psana as ps
import processed_data_class as PDC


def filtering(raw_data, filters):
    pro_data = PDC
    all_events = raw_data.eventIDs
    conditions = []
    good_events = []
    good_indicies = []
    
    for i in range(0,len(filters)):
        if not filters[i][0]:
            conditions.append(True)
        if filters[i][1] is 'bounds':
            conditions.append(bounds_filter(raw_data,filters[i][2]))
        if filters[i][1] is 'linearity':
            conditions.append(lin_filter(raw_data,filters[i][2]))
        if filters[i][1] is 'rms':
            conditions.append(lin_filter(raw_data,filters[i][2]))
        good_events.append(raw_data.eventIDs[conditions[i]])
        
        
        
        #good_indicies.append(all_events.searchsorted(good_events[i]))

            
    
    



    return good_events,conditions


def bounds_filter(raw_data,filt_param):
    var = getattr(raw_data,filt_param[0])
    lower_bound = filt_param[1]
    upper_bound = filt_param[2]
    num_stds = filt_param[3]

    cond_low = var > np.median(var) - np.std(var)*num_stds
    cond_high = var < np.median(var) + np.std(var)*num_stds
    cond_abs_min = var > lower_bound
    if not upper_bound is 'None':
        cond_abs_max = var < upper_bound
    else:
        cond_abs_max = True
    condition = cond_low & cond_high & cond_abs_min & cond_abs_max

    return condition

def lin_filter(raw_data,filt_param):
    var_x = getattr(raw_data,filt_param[0])
    var_y = getattr(raw_data,filt_param[1])

    lin_fit = np.polyfit(var_x, var_y, 1)

    cond_lin_high = var_y < var_x * lin_fit[0] + lin_fit[1] + filt_param[2]
    cond_lin_low = var_y > var_x * lin_fit[0] + lin_fit[1] - filt_param[2]
    
    condition = cond_lin_high & cond_lin_low

    return condition

def rms_filter(raw_data,filt_param):

    parameters = filt_param

    condition = 'tbd'
    return condition

def plot_filters(raw_data,conditions,plot_on):


    return

