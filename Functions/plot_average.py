# Averaging runs for plotting #### Turn on or off each plot [x1,x2,x3] where are all True/False

import matplotlib.pyplot as plt
import os
import sys
import numpy as np
import psana as ps
import pickle

def gather_shots(pro_datas,input_vars):
    scans_to_average= input_vars[0]
    runs= input_vars[2]
    if input_vars[1] is 0:
        idx = np.searchsorted(runs,scans_to_average) # runs
        all_epix_shots = np.asarray([pro_datas[i].epix_norm[j] for i in idx for j in range(0,len(pro_datas[i].epix_norm))])
        all_xrt_shots = np.asarray([pro_datas[i].xrt_norm[j] for i in idx for j in range(0,len(pro_datas[i].xrt_norm))])
        all_xrt_shots_based = np.asarray([pro_datas[i].xrt_based_norm[j] for i in idx for j in range(0,len(pro_datas[i].xrt_based_norm))])
        shot_id = [[pro_datas[i].scan_name,pro_datas[i].eventIDs[j]] for i in idx for j in range(0,len(pro_datas[i].xrt_norm))]
        return all_xrt_shots,all_epix_shots,all_xrt_shots_based,shot_id
    if input_vars[1] is 1:
        epix_shots_array = np.asarray([[pro_datas[runs.index(k)].epix_norm for k in j] for j in scans_to_average])
        all_epix_shots = np.asarray([np.concatenate(([epix_shots_array[j][i][:] for i in range(0,len(epix_shots_array[0]))]),0) for j in range(0,len(epix_shots_array))])
        
        xrt_shots_array = np.asarray([[pro_datas[runs.index(k)].xrt_norm for k in j] for j in scans_to_average])
        all_xrt_shots = np.asarray([np.concatenate(([xrt_shots_array[j][i][:] for i in range(0,len(xrt_shots_array[0]))]),0) for j in range(0,len(xrt_shots_array))])
        
        shot_id_arrays = np.asarray([[[pro_datas[runs.index(k)].scan_name,pro_datas[runs.index(k)].eventIDs] for k in j] for j in scans_to_average])
        shot_id = shot_id_arrays.flatten()
        return all_xrt_shots,all_epix_shots,shot_id

def plot_average(pro_datas,input_vars):
#     input_vars = [scans_to_average,all_shots,runs,boot,fraction,plot_type,plot_stacked,plot_residual,plot_deltaT_T, plot_bootstrap,check_dim,shot_by_shot]
    
    scans_to_average= input_vars[0]
    all_shots= input_vars[1]
    runs= input_vars[2]
    boot= input_vars[3]
    fraction= input_vars[4]
    plot_type= input_vars[5]
    plot_stacked= input_vars[6]
    plot_residual= input_vars[7]
    plot_deltaT_T= input_vars[8]
    plot_bootstrap= input_vars[9]
    check_dim= input_vars[10]
    shot_by_shot = input_vars[11]
    
    idx = np.searchsorted(runs,scans_to_average) # runs
    if all_shots:
        input_vars = [scans_to_average,0,runs]
        all_xrt_shots,all_epix_shots,all_xrt_shots_based,shot_id = gather_shots(pro_datas,input_vars)                
    # len(all_xrt_shots[:][:][:])
        if check_dim:
            print(len(all_epix_shots))
            print(len(all_xrt_shots))
            print(len(shot_id))
        
    


    energy = pro_datas[0].epix_energy_windowed
    average_epix_shots = np.mean(all_epix_shots,0)
    average_xrt_shots = np.mean(all_xrt_shots,0)
    average_xrt_shots_based = np.mean(all_xrt_shots_based,0)
    average_resid= average_epix_shots-average_xrt_shots_based
    average_deltaT_T = (average_resid)/average_xrt_shots_based
    if shot_by_shot:
        average_resid = all_epix_shots-all_xrt_shots_based
        average_deltaT_T = np.mean(average_resid/all_xrt_shots_based,0)
        average_resid = np.mean(average_resid,0)
    

    if plot_stacked:
        plt.figure()
        plt.plot(energy,average_epix_shots,label='Epix')
        plt.plot(energy,average_xrt_shots_based,label='XRT',alpha=0.6,linestyle='dashed')
        plt.legend()
        plt.title('Run(s) '+str(scans_to_average)+' | '+ str(len(all_epix_shots)) + ' shots in average.')
        plt.xlabel('energy, eV')
        plt.show()

    if plot_residual:
        plt.figure()
        plt.plot(energy,average_resid,label='xrt-epix')
        plt.legend()
        plt.title('Run(s) '+str(scans_to_average)+' Residual | '+ str(len(all_epix_shots)) + ' shots in average.')
        plt.xlabel('energy, eV')
        plt.show()

    if plot_deltaT_T:
        plt.figure()
        plt.plot(energy,average_deltaT_T,label='(xrt-epix)/xrt')
        plt.legend()
        plt.title('Run(s) '+str(scans_to_average)+' Delta T/T | '+ str(len(all_epix_shots)) + ' shots in average.')
        plt.xlabel('energy, eV')
        plt.show()


    if plot_bootstrap:
        if type(boot)==int:
            plt.figure()
            for i in range(0,boot):
                rand_=np.random.choice(len(all_epix_shots), np.int64(len(all_epix_shots)*fraction), replace=False)
                rand_shots_epix = np.mean(all_epix_shots[rand_],0)
                rand_shots_xrt = np.mean(average_xrt_shots_based[rand_],0)
                rand_shots_residual = rand_shots_xrt-rand_shots_epix
                rand_shots_DeltaT_T = rand_shots_residual/rand_shots_xrt
                if plot_type == 'stacked':
                    plt.plot(energy,rand_shots_epix)
                    plt.plot(energy,rand_shots_xrt,linestyle='dashed',alpha=0.6)
                if plot_type == 'residual':
                    plt.plot(energy,rand_shots_residual)
                if plot_type == 'DeltaT/T':
                    plt.plot(energy,rand_shots_DeltaT_T)
        if plot_type == 'stacked':
            plt.legend(('Epix','XRT'))
            plt.title('Runs '+str(scans_to_average)+' | '+ str(len(all_epix_shots)) + ' shots in average.')

        if plot_type == 'residual':
            plt.title('Run(s) '+str(scans_to_average)+' Residual | '+ str(len(all_epix_shots)) + ' shots in average.')
        if plot_type == 'DeltaT/T':
            plt.title('Run(s) '+str(scans_to_average)+' Delta T/T | '+ str(len(all_epix_shots)) + ' shots in average.')

        plt.legend(('Epix','XRT'))
        plt.xlabel('energy, eV')
        plt.title('Runs '+str(scans_to_average)+' | '+ str(len(all_epix_shots)) + ' shots in average.')
        # txt = 'Bootstrapped with ' + str(boot) + ' loops | ' + str(100*fraction)  + ' % of data | '+ str(np.int64(len(all_epix_shots)*fraction)) + ' of '+ str(len(all_epix_shots))+ ' shots'
        # fig.text(.5, .05, txt, ha='center')
        # fig.set_size_inches(7, 8, forward=True)
        plt.show()
        
    return

def plot_comparison(pro_datas,scans_to_plot,runs,energy,compare_resid,compare_deltaT_T):
    
    idx = np.searchsorted(runs,scans_to_plot)
    
    if compare_resid:
        plt.figure()
        for i in range(0,len(idx)):
            plt.plot(energy,np.mean(pro_datas[idx[i]].epix_norm,0)-np.mean(pro_datas[idx[i]].xrt_based_norm,0)
                     ,label=('run ' + str(scans_to_plot[i])),linewidth=2,alpha=0.5)
            plt.legend()
            plt.title('Residuals | xrt-epix')
            plt.xlabel('energy, eV')
            plt.show()

    if compare_deltaT_T:
        plt.figure()   
        for i in range(0,len(idx)):
            plt.plot(energy,(np.mean(pro_datas[idx[i]].epix_norm,0)-np.mean(pro_datas[idx[i]].xrt_based_norm,0))/np.mean(pro_datas[idx[i]].xrt_based_norm,0)
                     ,label=('run ' + str(scans_to_plot[i])),linewidth=2,alpha=0.5)
            plt.legend()
            plt.title('DeltaT/T | epix-xrt/xrt')
            plt.xlabel('energy, eV')
            plt.show()


        
        