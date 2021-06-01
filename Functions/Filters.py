# Written by Ben Poulter (Khalil Group, University of Washington), May 2021
# For LV27 LCLS Beamtime.

import matplotlib.pyplot as plt
import os
import sys
import numpy as np
import psana as ps

def filtering(raw_data, filters,suspress_output):
    all_events = raw_data.eventIDs
    conditions = []
    bounds_cond = []
    lin_conds = []
    good_shots = []
    really_good_shots = []
    if not suspress_output:
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
                if suspress_output:
                    print('Filter info for ' + raw_data.scan_name + ':')
                    
                print('Filter' + str(i) + ' removed ' + str(len(all_events)-len(really_good_shots[i])) + ' unique shots out of ' +str(len(all_events)) + ' total shots.')
                
            else:
                print('Filter' + str(i) + ' removed ' + str(len(really_good_shots[i-1])-len(really_good_shots[i])) + ' unique shots out of ' +str(len(all_events)) + ' total shots.')
            if np.logical_and(i is len(filters) -1,not suspress_output):
                print('The combined filters removed ' + str(len(all_events)-len(really_good_shots[-1])) + ' shots out of ' +str(len(all_events)) +' total shots | '+ str(np.round(100*(len(all_events)-len(really_good_shots[-1]))/len(all_events),3))+' %')
#                 print('')
    rm_by_bounds = len(all_events)-len(really_good_shots[len(bounds_cond)-1])
    rm_by_lin = len(really_good_shots[len(bounds_cond)-1])-len(really_good_shots[len(bounds_cond)+len(lin_conds)-1])
    if not suspress_output:
        print('')
        print('Bounds filters removed ' + str(rm_by_bounds) + ' shots out of ' + str(len(all_events))+' total shots.')
        print('Linearity filters removed ' + str(rm_by_lin) + ' shots out of ' + str(len(all_events))+' total shots.')
        print('The combined filters removed ' + str(len(all_events)-len(really_good_shots[-1])) + ' shots out of ' +str(len(all_events)) +' total shots | '+ str(np.round(100*(len(all_events)-len(really_good_shots[-1]))/len(all_events),3))+' %')
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
    scale = np.max([var_x,var_y])
    if type(bounds_conds)==type(np.bool_(True)):
        bounds_conds = np.full(len(var_x),True)
    if filt_param[2][3]:
        m, _, _, _ = np.linalg.lstsq(var_x[bounds_conds][:,np.newaxis],var_y[bounds_conds])
        cond_lin_high = var_y < var_x * m + filt_param[2][2]*scale
        cond_lin_low = var_y > var_x * m - filt_param[2][2]*scale
        condition = cond_lin_high & cond_lin_low
    else:
        var_x = var_x
        var_y = var_y
        lin_fit = np.polyfit(var_x[bounds_conds], var_y[bounds_conds], 1)
        cond_lin_high = var_y < var_x * lin_fit[0] + lin_fit[1] + filt_param[2][2]*scale
        cond_lin_low = var_y > var_x * lin_fit[0] + lin_fit[1] - filt_param[2][2]*scale
        condition = cond_lin_high & cond_lin_low
    if np.logical_and(filt_param[3][0],'run_'+str(filt_param[3][1])==getattr(raw_data,'scan_name')):
        plt.figure()
        plt.scatter(var_x,var_y,alpha=0.95)
        plt.scatter(var_x[condition],var_y[condition],alpha=0.05)
        plt.title(filt_param[1]+' '+filt_param[2][0] +' vs '+ filt_param[2][1])
        plt.show()
    return condition

def rms_filter(processed_data,filt_param,suppress_output):
    total_I_epix = processed_data.epix_intensity
    total_I_xrt = processed_data.xrt_intensity
    energy = processed_data.epix_energy_windowed
    events = processed_data.eventIDs
    epix = processed_data.epix_windowed
    xrt = processed_data.xrt_based_norm
    epix_avg = np.mean(epix,0)
    xrt_avg = np.mean(xrt,0)

    epix_norm = epix/np.max(epix_avg)
    xrt_norm = xrt/np.max(xrt_avg)
    epix_avg_norm = epix_avg/np.max(epix_avg)
    xrt_avg_norm = xrt_avg/np.max(xrt_avg)


    epix_rms = np.sqrt(np.mean(np.subtract(epix_avg_norm,epix_norm)**2,1))
    xrt_rms = np.sqrt(np.mean(np.subtract(xrt_avg_norm,xrt_norm)**2,1))

    max_rms_epix = filt_param[0][0]
    max_rms_xrt = filt_param[0][1]
    rms_cond_epix = epix_rms < max_rms_epix
    rms_cond_xrt = xrt_rms < max_rms_xrt
    rms_cond_combined = np.logical_and(rms_cond_epix,rms_cond_xrt)
    conditions = [rms_cond_epix,rms_cond_xrt,rms_cond_combined]
    
    if not suppress_output:
        print('RMSE filter information for ' + str(processed_data.scan_name))
        print('The epix rmse condition removed ' + str(rms_cond_epix.shape[0] - rms_cond_epix.sum()) +' out of ' + str(events.shape[0]) + ' shots.')
        print('The xrt rmse condition removed ' + str(rms_cond_xrt.shape[0] - rms_cond_xrt.sum()) +' out of ' + str(events.shape[0]) + ' shots.')
        print('Both rmse conditions removed ' + str(rms_cond_combined.shape[0] - rms_cond_combined.sum()) +' out of ' + str(events.shape[0]) + ' shots.')
        print('')
        return conditions

    if np.logical_and(filt_param[2] is False, processed_data.scan_name == 'run_'+str(filt_param[1])):
        print('RMSE filter information for run ' + str(processed_data.scan_name))
        print('The epix rmse condition removed ' + str(rms_cond_epix.shape[0] - rms_cond_epix.sum()) +' out of ' + str(events.shape[0]) + ' shots.')
        print('The xrt rmse condition removed ' + str(rms_cond_xrt.shape[0] - rms_cond_xrt.sum()) +' out of ' + str(events.shape[0]) + ' shots.')
        print('Both rmse conditions removed ' + str(rms_cond_combined.shape[0] - rms_cond_combined.sum()) +' out of ' + str(events.shape[0]) + ' shots.')
        print('')
        plt.figure()
        _, bins, _ = plt.hist(epix_rms, 100, label='xrt')
        _ = plt.hist(xrt_rms, bins, rwidth=.5, label='epix')
        plt.legend()
        plt.title('RMSE distribution for each spectrometer | ' + str(processed_data.scan_name))
        plt.xlabel('RMSE')
        plt.ylabel('# shots')
        plt.show()
        
        return conditions
    if filt_param[2]:
        plt.figure()
        _, bins, _ = plt.hist(epix_rms, 100, label='epix')
        _ = plt.hist(xrt_rms, bins, rwidth=.5, label='xrt')
        plt.legend()
        plt.title('RMSE distribution for each spectrometer | ' + str(processed_data.scan_name))
        plt.xlabel('RMSE')
        plt.ylabel('# shots')
        plt.show()     
        return conditions
    if np.logical_and(filt_param[2] is False,suppress_output):
        return conditions
def apply_rms_filter(processed_data,condition):
    
    processed_data.changeValue(eventIDs=processed_data.eventIDs[condition],
                    high_diode_us=processed_data.high_diode_us[condition],
                    low_diode_us=processed_data.low_diode_us[condition],
                    xrt_intensity=processed_data.xrt_intensity[condition],
                    epix_intensity=processed_data.epix_intensity[condition],
                    epix_windowed=processed_data.epix_windowed[condition],
                    xrt_windowed=processed_data.xrt_windowed[condition],
                    xrt_red_res=processed_data.xrt_red_res[condition],
                    xrt_based=processed_data.xrt_based[condition])
    
    return processed_data




