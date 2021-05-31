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
    #input_vars = [scans_to_plot,spec_cal_runs,plot_conds,plot_shotwise,plot_meanwise,runs,bootstrap]
    # Plot Conds : epix, xrt, resid, deltaT_T
    scans_to_plot = input_vars[0]
    spec_cal_runs = input_vars[1]
    xrt_plot = input_vars[2][1]
    epix_plot = input_vars[2][0]
    resid_plot = input_vars[2][2]
    deltaT_T_plot = input_vars[2][3]
    plot_shotwise = input_vars[3]
    plot_meanwise = input_vars[4]
    runs = input_vars[5]
    bootstrapped = input_vars[6]
    energy = pro_datas[0].epix_energy_windowed
        
    shots_in_scale = gather_shots(pro_datas,[spec_cal_runs,1,runs])
    scale = np.mean(np.mean(shots_in_scale[1],0),0)/np.mean(np.mean(shots_in_scale[0],0),0)
    
    compare = np.asarray(gather_shots(pro_datas,[scans_to_plot,1,runs]))
    epix_means = [np.mean(compare[1][i],0) for i in range(0,compare[0].shape[0])]
    xrt_means = [np.mean(scale*compare[0][i],0) for i in range(0,compare[0].shape[0])]


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
        resid_means =[epix_means[i]-xrt_means[i] for i in range(0,compare[0].shape[0])]
        deltaT_T_means =[(resid_means[i]/xrt_means[i]) for i in range(0,compare[0].shape[0])]

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
        resid_sbs = [compare[1][i]-(scale*compare[0][i]) for i in range(0,compare[0].shape[0])]
        deltaT_T_sbs = [(resid_sbs[i])/(scale*compare[0][i]) for i in range(0,compare[0].shape[0])]        
            
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

    if bootstrapped[0]:
        colors = ['b','k','r','g','c','m','y']
        boot = bootstrapped[1]
        fraction = bootstrapped[2]
        
        if epix_plot:
            fig_1, ax_1 = plt.subplots()
            plt.xlabel('energy, keV')
            plt.title('Epix Spectrum | ' +str(boot)+ ' loops | ' + str(round(fraction,2)) + ' of data per' )
        if xrt_plot:
            fig_2, ax_2 = plt.subplots()
            plt.xlabel('energy, keV')
            plt.title('XRT Spectrum | ' +str(boot)+ ' loops | random ' + str(round(fraction,2)) + ' of data per' )

        if plot_meanwise:
            
            if resid_plot:
                fig_3, ax_3 = plt.subplots()
                plt.xlabel('energy, keV')
                plt.title('avg(epix)- avg(xrt) | ' +str(boot)+ ' loops | random ' + str(round(fraction,2)) + ' of data per' )

            if deltaT_T_plot:
                fig_4, ax_4 = plt.subplots()
                plt.xlabel('energy, keV')
                plt.title('[avg(epix)-avg(xrt)]/avg(xrt) | ' +str(boot)+ ' loops | random ' + str(round(fraction,2)) + ' of data per' )

        if plot_shotwise:
            if resid_plot:
                fig_5, ax_5 = plt.subplots()
                plt.xlabel('energy, keV')
                plt.title('avg(epix-xrt) | ' +str(boot)+ ' loops | random ' + str(round(fraction,2)) + ' of data per' )

            if deltaT_T_plot:
                fig_6, ax_6 = plt.subplots()
                plt.xlabel('energy, keV')
                plt.title('avg[(epix-xrt)/xrt] | ' +str(boot)+ ' loops | random ' + str(round(fraction,2)) + ' of data per' )


        for j in range(0,compare[0].shape[0]):
            for i in range(0,boot):
                rand_=np.random.choice(len(compare[1][j]), np.int64(len(compare[1][j])*fraction), replace=False)
                rand_shots_epix = compare[1][j][rand_]
                rand_shots_xrt = scale*compare[0][j][rand_]
                rand_shots_residual = rand_shots_epix-rand_shots_xrt
                rand_shots_DeltaT_T = rand_shots_residual/(scale*rand_shots_xrt)

                if epix_plot:
                    ax_1.plot(energy,np.mean(rand_shots_epix,0),color=colors[j])

                if xrt_plot:
                    ax_2.plot(energy,np.mean(rand_shots_xrt,0),color=colors[j])

                if plot_meanwise:

                    if resid_plot:
                        ax_3.plot(energy,np.mean(rand_shots_epix,0)-np.mean(rand_shots_xrt,0),color=colors[j])
                    if deltaT_T_plot:
                        ax_4.plot(energy,(np.mean(rand_shots_epix,0)-np.mean(rand_shots_xrt,0))/np.mean(rand_shots_xrt,0),color=colors[j])

                if plot_shotwise:

                    if resid_plot:
                        ax_5.plot(energy,np.mean(rand_shots_epix-rand_shots_xrt,0),color=colors[j])
                    if deltaT_T_plot:
                        ax_6.plot(energy,np.mean((rand_shots_epix-rand_shots_xrt)/rand_shots_xrt,0),color=colors[j])


        if epix_plot:
            ax_1.legend((scans_to_plot),labelcolor=colors)
        if xrt_plot:
            ax_2.legend((scans_to_plot),labelcolor=colors)
        if plot_meanwise:
            if resid_plot:
                ax_3.legend((scans_to_plot),labelcolor=colors)
            if deltaT_T_plot:
                ax_4.legend((scans_to_plot),labelcolor=colors)
        if plot_shotwise:
            if resid_plot:
                ax_5.legend((scans_to_plot),labelcolor=colors)
            if deltaT_T_plot:
                ax_6.legend((scans_to_plot),labelcolor=colors)
                           
