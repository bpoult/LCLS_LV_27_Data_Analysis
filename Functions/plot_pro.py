# Written by Ben Poulter (Khalil Group, University of Washington), May 2021
# For LV27 LCLS Beamtime.

import matplotlib.pyplot as plt
import os
import sys
import numpy as np
import psana as ps
import pickle
from .plot_average import gather_shots



def check_SN(pro_data,plot_on):

    epix = pro_data.epix_norm
    xrt = pro_data.xrt_based_norm
    resid = np.subtract(epix,xrt)
    if plot_on:
        resid_rand = resid[np.random.choice(resid.shape[0], np.int64(epix.shape[0]), replace=False)]
        loop_over = np.append(np.arange(100,len(resid),100,dtype=int),len(resid))
        plt.figure()
        for i in loop_over:
            plt.scatter(i,np.std(np.mean(resid_rand[0:i],0)),1.5,c='k')
        plt.xlabel('# shots in avg')
        plt.ylabel('STD of residual')
        plt.title('Shot Noise for ' +str(epix.shape[0])+' total shots')
        plt.show()
    return resid

def plot_one_run(processed_data,plot_on):
    energy = processed_data.epix_energy_windowed
    epix = processed_data.epix_norm
    xrt = processed_data.xrt_based_norm
    resid = np.subtract(epix,xrt)
    deltaT_T = np.divide(resid,xrt)


    if plot_on:
        plt.figure()
        plt.errorbar(energy,np.mean(epix,0),label='epix')#,np.std(epix,0)/epix_I,label='epix')
        plt.errorbar(energy,np.mean(xrt,0),label='xrt')#,np.std(xrt,0)/xrt_I,label='xrt')
        plt.xlabel('energy, keV')
        plt.legend()
        plt.title('Epix and XRT spectra | error bars = std')

        plt.figure()
        plt.plot(energy,np.mean(resid,0))#,np.std(resid,0)/(epix_I-xrt_I))
        plt.xlabel('energy, keV')
        plt.title('Epix - XRT | error bars = std')

        plt.figure()
        plt.plot(energy,np.mean(deltaT_T,0))
        plt.xlabel('energy, keV')
        plt.ylabel('% difference')
        plt.title('\u0394 T / T')
        
        
def plot_average(pro_datas,plot_on):
    
    shots_array = [pro_datas[i].eventIDs.shape[0] for i in range(0,len(pro_datas))]
    total_shots = np.sum(shots_array)
    energy = pro_datas[0].epix_energy_windowed
    epix_I_array = [np.mean(pro_datas[i].epix_intensity,0) for i in range(0,len(pro_datas))]
    xrt_I_array = [np.mean(pro_datas[i].xrt_intensity,0) for i in range(0,len(pro_datas))]
    epix_array = [np.mean(pro_datas[i].epix_windowed,0)/epix_I_array[i] for i in range(0,len(pro_datas))]
    xrt_array = [np.mean(pro_datas[i].xrt_based,0)/xrt_I_array[i] for i in range(0,len(pro_datas))]


    weighted_epix_avg = np.mean([epix_array[i]*shots_array[i]/total_shots for i in range(0,len(pro_datas))])
    weighted_xrt_avg = np.mean([xrt_array[i]*shots_array[i]/total_shots for i in range(0,len(pro_datas))])
    resid = weighted_epix_avg - weighted_xrt_avg
    DeltaT_T = resid/weighted_xrt_avg
                                                                 
                                                                 
    if plot_on:
        plt.figure()
        plt.plot(energy,weighted_epix_avg,label='epix')#,np.std(epix,0)/epix_I,label='epix')
        plt.plot(energy,weighted_xrt_avg,label='xrt')#,np.std(xrt,0)/xrt_I,label='xrt')
        plt.xlabel('energy, keV')
        plt.legend()
        plt.title('Epix and XRT spectra | error bars = std')

        plt.figure()
        plt.plot(energy,resid)#,np.std(resid,0)/(epix_I-xrt_I))
        plt.xlabel('energy, keV')
        plt.title('Epix - XRT | error bars = std')

        plt.figure()
        plt.plot(energy,DeltaT_T)
        plt.xlabel('energy, keV')
        plt.ylabel('% difference')
        plt.title('\u0394 T / T')

def plot_lots(pro_datas,input_vars):
    #input_vars = [scans_to_plot,spec_cal_runs,plot_conds,plot_shotwise,plot_meanwise]
    # Plot Conds : epix, xrt, resid, deltaT_T
    scans_to_plot = input_vars[0]
    spec_cal_runs = input_vars[1]
    xrt_plot = input_vars[2][0]
    epix_plot = input_vars[2][1]
    resid_plot = input_vars[2][2]
    deltaT_T_plot = input_vars[2][3]
    plot_shotwise = input_vars[3]
    plot_meanwise = input_vars[4]
    runs = input_vars[5]
    bootstrapped = input_vars[6]
    energy = pro_datas[0].epix_energy_windowed
        
    scale_shots_xrt,scale_shots_epix,scale_shots_ids = gather_shots(pro_datas,[spec_cal_runs,1,runs])
    scale = np.mean(scale_shots_epix,0)/np.mean(scale_shots_xrt,0)
    
    compare = [gather_shots(pro_datas,[scans_to_plot[i],1,runs]) for i in range(0,len(scans_to_plot))]
    
    epix_means = [np.mean(compare[i][1],0) for i in range(0,len(compare))]
    xrt_means = [np.mean(scale*compare[i][0],0) for i in range(0,len(compare))]


    if epix_plot:
        plt.figure()
        [plt.plot(energy,epix_means[i]) for i in range(0,len(epix_means))]
        plt.legend((scans_to_plot))
        plt.title('Epix Spectra Stacked')
        plt.xlabel('energy, keV')
        plt.show()
        
    if xrt_plot:
        plt.figure()
        [plt.plot(energy,xrt_means[i]) for i in range(0,len(xrt_means))]
        plt.legend((scans_to_plot))
        plt.title('XRT Spectra Stacked')
        plt.xlabel('energy, keV')
        plt.show()

    if plot_meanwise:
        resid_means =[epix_means[i]-xrt_means[i] for i in range(0,len(compare))]
        deltaT_T_means =[(resid_means[i]/xrt_means[i]) for i in range(0,len(compare))]

        if resid_plot:
            plt.figure()
            [plt.plot(energy,resid_means[i]) for i in range(0,len(resid_means))]
            plt.legend((scans_to_plot))
            plt.title('Residual | avg(epix)-avg(xrt)')
            plt.xlabel('energy, keV')
            plt.show()

        if deltaT_T_plot:
            plt.figure()
            [plt.plot(energy,deltaT_T_means[i]) for i in range(0,len(deltaT_T_means))]
            plt.legend((scans_to_plot))
            plt.title('Delta T / T | (avg(epix)-avg(xrt))/avg(xrt)')
            plt.xlabel('energy, keV')
            plt.show()
    
    
    if plot_shotwise:
        resid_sbs = [compare[i][1]-compare[i][0]*scale for i in range(0,len(compare))]
        deltaT_T_sbs = [(resid_sbs[i])/(compare[i][0]*scale) for i in range(0,len(compare))]        
            
        if resid_plot:
            plt.figure()
            [plt.plot(energy,np.mean(resid_sbs[i],0)) for i in range(0,len(resid_sbs))]
            plt.legend((scans_to_plot))
            plt.title('Residual | avg(epix-xrt) shotwise')
            plt.xlabel('energy, keV')
            plt.show()

        if deltaT_T_plot:
            plt.figure()
            [plt.plot(energy,np.mean(deltaT_T_sbs[i],0)) for i in range(0,len(deltaT_T_sbs))]
            plt.legend((scans_to_plot))
            plt.title('Delta T / T | avg[(epix-xrt)/xrt] shotwise')
            plt.xlabel('energy, keV')
            plt.show()








                                                                 
                                                                 
                                                                 
