import matplotlib.pyplot as plt
import os
import sys
import numpy as np
import psana as ps

def filtering(raw_data, filters):
    all_events = raw_data.eventIDs
    conditions = []
    bounds_cond = []
    lin_conds = []
    good_shots = []
    really_good_shots = []
    print('Filter info for ' + raw_data.scan_name + ':')
    for i in range(0,len(filters)):
        if not filters[i][0]:
            conditions.append('None')
            continue
        if filters[i][1] is 'bounds':
            conditions.append(bounds_filter(raw_data,filters[i]))
            bounds_cond.append(conditions[i])
            good_shots.append(all_events[conditions[i]])
        if filters[i][1] is 'linearity':
            bounds_conds = np.asarray(bounds_cond).all(axis=0)
            conditions.append(lin_filter(raw_data,filters[i],bounds_conds))
            lin_conds.append(conditions[i])
            good_shots.append((all_events)[conditions[i]])
        if filters[i][1] is 'rms':
            conditions.append(rms_filter(raw_data,filters[i]))
        really_good_shots.append(list(set.intersection(*[set(x) for x in good_shots])))
        if raw_data.scan_name == 'run_'+str(filters[i][3][1]):
            if i is 0:
                print('Filter' + str(i) + ' removed ' + str(len(all_events)-len(really_good_shots[i])) + ' unique shots out of ' +str(len(all_events)) + ' total shots.')
            else:
                print('Filter' + str(i) + ' removed ' + str(len(really_good_shots[i-1])-len(really_good_shots[i])) + ' unique shots out of ' +str(len(all_events)) + ' total shots.')        
    rm_by_bounds = len(all_events)-len(really_good_shots[len(bounds_cond)-1])
    rm_by_lin = len(really_good_shots[len(bounds_cond)-1])-len(really_good_shots[len(bounds_cond)+len(lin_conds)-1])
    
    print('Bounds filters removed ' + str(rm_by_bounds) + ' shots out of ' + str(len(all_events))+' total shots.')
    print('Linearity filters removed ' + str(rm_by_lin) + ' shots out of ' + str(len(all_events))+' total shots.')
    print('The combined filters removed ' + str(len(all_events)-len(really_good_shots[-1])) + ' shots out of ' +str(len(all_events)) +' total shots.')
    print('')

    return conditions


def bounds_filter(raw_data,filt_param):
    var = getattr(raw_data,filt_param[2][0])
    if filt_param[2][0] is 'pulse_energies_fee':
        var=var[:,1] # 0 = 12; 1 = 21; 2 = 63
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
    if np.logical_and(filt_param[3][0],'run_'+str(filt_param[3][1])==getattr(raw_data,'scan_name')):
        plt.figure()
        _, bins, _ = plt.hist(var, 100, label='unfiltered')
        _ = plt.hist(var[condition], bins, rwidth=.5, label='filtered')
        plt.title(filt_param[1]+' '+filt_param[2][0])
        plt.legend()
        plt.show()
    return condition

def lin_filter(raw_data,filt_param,bounds_conds):
    var_x = getattr(raw_data,filt_param[2][0])
    var_y = getattr(raw_data,filt_param[2][1])
    var_x = var_x/np.max(var_x)
    var_y = var_y/np.max(var_y)
    lin_fit = np.polyfit(var_x[bounds_conds], var_y[bounds_conds], 1)
    cond_lin_high = var_y < var_x * lin_fit[0] + lin_fit[1] + filt_param[2][2]
    cond_lin_low = var_y > var_x * lin_fit[0] + lin_fit[1] - filt_param[2][2]
    condition = cond_lin_high & cond_lin_low
    if np.logical_and(filt_param[3][0],'run_'+str(filt_param[3][1])==getattr(raw_data,'scan_name')):
        plt.figure()
        plt.scatter(var_x,var_y,alpha=0.95)
        plt.scatter(var_x[condition],var_y[condition],alpha=0.05)
        plt.title(filt_param[1]+' '+filt_param[2][0] +' vs '+ filt_param[2][1])
        plt.show()
    return condition

def rms_filter(raw_data,filt_param):

    parameters = filt_param

    condition = 'tbd'
    return condition
