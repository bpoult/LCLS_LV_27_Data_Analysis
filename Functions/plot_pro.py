# Written by Ben Poulter (Khalil Group, University of Washington), May 2021
# For LV27 LCLS Beamtime.

import matplotlib.pyplot as plt
import os
import sys
import numpy as np
import psana as ps
import pickle


def check_SN(pro_data,plot_on):

    epix = pro_data.epix_windowed
    xrt = pro_data.xrt_based
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
    epix_I = np.mean(processed_data.epix_intensity)
    xrt_I = np.mean(processed_data.xrt_intensity)
    epix = processed_data.epix_windowed/epix_I
    xrt = processed_data.xrt_based/xrt_I
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
    
    shots_array = [pro_datas[i].eventIDs.shape[0] for i in range(0,len(pro_datas)]
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










                                                                 
                                                                 
                                                                 
