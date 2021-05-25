import matplotlib.pyplot as plt
import os
import sys
import numpy as np
import psana as ps

def filtering(raw_data, filters):
    all_events = raw_data.eventIDs
    conditions = []
    for i in range(0,len(filters)):
        if not filters[i][0]:
            conditions.append('None')
            continue
        if filters[i][1] is 'bounds':
            conditions.append(bounds_filter(raw_data,filters[i]))
        if filters[i][1] is 'linearity':
            conditions.append(lin_filter(raw_data,filters[i]))
        if filters[i][1] is 'rms':
            conditions.append(lin_filter(raw_data,filters[i]))
            
        cond_combined = np.asarray(conditions[i:i+1]).all(axis=0)
        print('Filter' + str(i) + ' removed ' + str(len(all_events)-len(all_events[cond_combined])) + ' unique shots.')
        
    print('All filters combined removed ' + str(len(all_events)-len(all_events[np.asarray(conditions).all(axis=0)])) + ' shots out of ' + str(len(all_events))+'.')
    print('')
    
    return conditions


def bounds_filter(raw_data,filt_param):
    var = getattr(raw_data,filt_param[2][0])
    if filt_param[2][0] is 'pulse_energies_fee':
        var=var[:,2] # 0 = 12; 1 = 21; 2 = 63
    var = var/np.max(var)
    lower_bound = filt_param[2][1]
    upper_bound = filt_param[2][2]
    num_stds = filt_param[2][3]

    cond_low = var > np.median(var) - np.std(var)*num_stds
    cond_high = var < np.median(var) + np.std(var)*num_stds
    cond_abs_min = var > lower_bound
    if not upper_bound is 'None':
        cond_abs_max = var < upper_bound
    else:
        cond_abs_max = True
    condition = cond_low & cond_high & cond_abs_min & cond_abs_max
    if filt_param[3]:
        plt.figure()
        plt.scatter(raw_data.eventIDs,var)
        plt.scatter(raw_data.eventIDs[condition],var[condition])
        plt.title(filt_param[1]+' '+filt_param[2][0])
        plt.show()
    return condition

def lin_filter(raw_data,filt_param):
    var_x = getattr(raw_data,filt_param[2][0])
    var_y = getattr(raw_data,filt_param[2][1])
    var_x = var_x/np.max(var_x)
    var_y = var_y/np.max(var_y)
    lin_fit = np.polyfit(var_x, var_y, 1)

    cond_lin_high = var_y < var_x * lin_fit[0] + lin_fit[1] + filt_param[2][2]
    cond_lin_low = var_y > var_x * lin_fit[0] + lin_fit[1] - filt_param[2][2]
    
    condition = cond_lin_high & cond_lin_low
    if filt_param[3]:
        plt.figure()
        plt.scatter(var_x,var_y)
        plt.scatter(var_x[condition],var_y[condition])
        plt.title(filt_param[1]+' '+filt_param[2][0])
        plt.show()
    return condition

def rms_filter(raw_data,filt_param):

    parameters = filt_param

    condition = 'tbd'
    return condition
