import matplotlib.pyplot as plt
import os
import sys
import numpy as np
import psana as ps
import pickle
from .plot_average import gather_shots
                    
                    
def plot_lots_comp(pro_datas,input_vars,txt2):
#     input_vars = [scans_to_plot_comp,spec_cal_runs_comp,runs_comp,scans_to_plot_comp2,spec_cal_runs_comp2
#               ,runs_comp2,scans_to_plot,spec_cal_runs,plot_conds,plot_shotwise,plot_meanwise,runs,bootstrap]
#     pro_datas = [pro_datas0,pro_datas1,pro_datas2]

    pro_datas1 = pro_datas[1]
    scans_to_plot_comp = input_vars1[0]
    spec_cal_runs_comp = input_vars1[1]
    runs_comp = input_vars1[2]
    energy = pro_datas[1][0].epix_energy_windowed

#     spec_cal_runs_comp = spec_cal_runs
#     scans_to_plot_comp = scans_to_plot
#     runs_comp = runs

    shots_in_scale_comp = gather_shots(pro_datas1,[spec_cal_runs_comp,1,runs_comp])
    scale_comp = np.mean(np.mean(shots_in_scale_comp[1],0),0)/np.mean(np.mean(shots_in_scale_comp[0],0),0)
    compare_comp = np.asarray(gather_shots(pro_datas1,[scans_to_plot_comp,1,runs_comp]))
#     print(compare_comp.shape)

    epix_means_comp = [np.mean(compare_comp[1][i],0) for i in range(0,compare_comp[0].shape[0])]
    xrt_means_comp = [np.mean(scale_comp*compare_comp[0][i],0) for i in range(0,compare_comp[0].shape[0])]

    resid_means_comp =[epix_means_comp[i]-xrt_means_comp[i] for i in range(0,compare_comp[0].shape[0])]
    deltaT_T_means_comp =[(resid_means_comp[i]/xrt_means_comp[i]) for i in range(0,compare_comp[0].shape[0])]

    resid_sbs_comp = [compare_comp[1][i]-(scale_comp*compare_comp[0][i]) for i in range(0,compare_comp[0].shape[0])]
    deltaT_T_sbs_comp = [(resid_sbs_comp[i])/(scale_comp*compare_comp[0][i]) for i in range(0,compare_comp[0].shape[0])]
    
    
    
#     make another set of variables
    pro_datas2 = pro_datas[
    scans_to_plot_comp2 = input_vars2[0]
    spec_cal_runs_comp2 = input_vars2[1]
    runs_comp2 = input_vars2[5]
    energy = pro_datas2[0].epix_energy_windowed

    shots_in_scale_comp2 = gather_shots(pro_datas2,[spec_cal_runs_comp2,1,runs_comp2])
    scale_comp2 = np.mean(np.mean(shots_in_scale_comp2[1],0),0)/np.mean(np.mean(shots_in_scale_comp2[0],0),0)
    compare_comp2 = np.asarray(gather_shots(pro_datas2,[scans_to_plot_comp2,1,runs_comp2]))
#     print(compare_comp.shape)

    epix_means_comp2 = [np.mean(compare_comp2[1][i],0) for i in range(0,compare_comp2[0].shape[0])]
    xrt_means_comp2 = [np.mean(scale_comp2*compare_comp2[0][i],0) for i in range(0,compare_comp2[0].shape[0])]

    resid_means_comp2 =[epix_means_comp2[i]-xrt_means_comp2[i] for i in range(0,compare_comp2[0].shape[0])]
    deltaT_T_means_comp2 =[(resid_means_comp2[i]/xrt_means_comp2[i]) for i in range(0,compare_comp2[0].shape[0])]

    resid_sbs_comp2 = [compare_comp2[1][i]-(scale_comp*compare_comp2[0][i]) for i in range(0,compare_comp2[0].shape[0])]
    deltaT_T_sbs_comp2 = [(resid_sbs_comp2[i])/(scale_comp*compare_comp2[0][i]) for i in range(0,compare_comp2[0].shape[0])]



    
#     make another set of variables and plot things
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
    
    padding = 3
    txt = 'cal '+str(spec_cal_runs[0])+' on ',[str(scans_to_plot[i]) for i in range(0,len(epix_means))],' AND cal ' + str(spec_cal_runs_comp[0])+' on ',[str(scans_to_plot_comp[i]) for i in range(0,len(epix_means_comp))]

#     txt2 = input('Type optional notes or hit enter')


    if epix_plot:
        plt.figure()
        [plt.plot(energy,epix_means[i],label = scans_to_plot[i]) for i in range(0,len(epix_means))]
        [plt.plot(energy,epix_means_comp[i],label = scans_to_plot_comp[i]) for i in range(0,len(epix_means_comp))]
        [plt.plot(energy,epix_means_comp2[i],label = scans_to_plot_comp2[i]) for i in range(0,len(epix_means_comp2))]
        plt.legend()
        plt.title('Epix Spectra Stacked')
        plt.xlabel('energy, keV')
        plt.figtext(0.5, 0.04, txt, wrap=True, horizontalalignment='center', fontsize=8)
        plt.figtext(0.5, 0.01, txt2, wrap=True, horizontalalignment='center', fontsize=8)
        plt.tight_layout(pad=padding)    
        plt.show()
    if xrt_plot:
        plt.figure()
        [plt.plot(energy,xrt_means[i],label = scans_to_plot[i]) for i in range(0,len(xrt_means))]
        [plt.plot(energy,xrt_means_comp[i],label = scans_to_plot_comp[i]) for i in range(0,len(xrt_means_comp))]
        [plt.plot(energy,xrt_means_comp2[i],label = scans_to_plot_comp2[i]) for i in range(0,len(xrt_means_comp2))]
        plt.legend()    
        plt.title('XRT Spectra Stacked')
        plt.xlabel('energy, keV')
        plt.figtext(0.5, 0.04, txt, wrap=True, horizontalalignment='center', fontsize=8)
        plt.figtext(0.5, 0.01, txt2, wrap=True, horizontalalignment='center', fontsize=8)
        plt.tight_layout(pad=padding)    
        plt.show()

    if plot_meanwise:
        resid_means =[epix_means[i]-xrt_means[i] for i in range(0,compare[0].shape[0])]
        deltaT_T_means =[(resid_means[i]/xrt_means[i]) for i in range(0,compare[0].shape[0])]

        if resid_plot:
            plt.figure()
            [plt.plot(energy,resid_means[i],label = scans_to_plot[i]) for i in range(0,len(resid_means))]
            [plt.plot(energy,resid_means_comp[i],label = scans_to_plot_comp[i]) for i in range(0,len(resid_means_comp))]
            [plt.plot(energy,resid_means_comp2[i],label = scans_to_plot_comp2[i]) for i in range(0,len(resid_means_comp2))]
            plt.legend()    
            plt.title('Residual | avg(epix)-avg(xrt)')
            plt.xlabel('energy, keV')
            plt.figtext(0.5, 0.04, txt, wrap=True, horizontalalignment='center', fontsize=8)
            plt.figtext(0.5, 0.01, txt2, wrap=True, horizontalalignment='center', fontsize=8)
            plt.tight_layout(pad=padding)               
            plt.show()

        if deltaT_T_plot:
            plt.figure()
            [plt.plot(energy,deltaT_T_means[i],label = scans_to_plot[i]) for i in range(0,len(deltaT_T_means))]
            [plt.plot(energy,deltaT_T_means_comp[i],label = scans_to_plot_comp[i]) for i in range(0,len(deltaT_T_means_comp))]
            [plt.plot(energy,deltaT_T_means_comp2[i],label = scans_to_plot_comp2[i]) for i in range(0,len(deltaT_T_means_comp2))]
            plt.legend()    
            plt.title('Delta T / T | (avg(epix)-avg(xrt))/avg(xrt)')
            plt.xlabel('energy, keV')
            plt.figtext(0.5, 0.04, txt, wrap=True, horizontalalignment='center', fontsize=8)
            plt.figtext(0.5, 0.01, txt2, wrap=True, horizontalalignment='center', fontsize=8)
            plt.tight_layout(pad=padding)    
            plt.show()


    if plot_shotwise:
        resid_sbs = [compare[1][i]-(scale*compare[0][i]) for i in range(0,compare[0].shape[0])]
        deltaT_T_sbs = [(resid_sbs[i])/(scale*compare[0][i]) for i in range(0,compare[0].shape[0])]        

        if resid_plot:
            plt.figure()
            [plt.plot(energy,np.mean(resid_sbs[i],0),label = scans_to_plot[i]) for i in range(0,len(resid_sbs))]
            [plt.plot(energy,np.mean(resid_sbs_comp[i],0),label = scans_to_plot_comp[i]) for i in range(0,len(resid_sbs_comp))]
            [plt.plot(energy,np.mean(resid_sbs_comp2[i],0),label = scans_to_plot_comp2[i]) for i in range(0,len(resid_sbs_comp2))]
            plt.legend()    
            plt.title('Residual | avg(epix-xrt) shotwise')
            plt.xlabel('energy, keV')
            plt.figtext(0.5, 0.04, txt, wrap=True, horizontalalignment='center', fontsize=8)
            plt.figtext(0.5, 0.01, txt2, wrap=True, horizontalalignment='center', fontsize=8)
            plt.tight_layout(pad=padding)    
            plt.show()

        if deltaT_T_plot:
            plt.figure()
            [plt.plot(energy,np.mean(deltaT_T_sbs[i],0),label = scans_to_plot[i]) for i in range(0,len(deltaT_T_sbs))]
            [plt.plot(energy,np.mean(deltaT_T_sbs_comp[i],0),label = scans_to_plot_comp[i]) for i in range(0,len(deltaT_T_sbs_comp))]
            [plt.plot(energy,np.mean(deltaT_T_sbs_comp2[i],0),label = scans_to_plot_comp2[i]) for i in range(0,len(deltaT_T_sbs_comp2))]
            plt.legend()    
            plt.title('Delta T / T | avg[(epix-xrt)/xrt] shotwise')
            plt.xlabel('energy, keV')
            plt.figtext(0.5, 0.04, txt, wrap=True, horizontalalignment='center', fontsize=8)
            plt.figtext(0.5, 0.01, txt2, wrap=True, horizontalalignment='center', fontsize=8)
            plt.tight_layout(pad=padding)    
            plt.show()

    if bootstrapped[0]:
        colors = ['b','k','r','g','c','m','y']
        boot = bootstrapped[1]
        fraction = bootstrapped[2]

        if epix_plot:
            fig_1, ax_1 = plt.subplots()
            plt.xlabel('energy, keV')
            plt.figtext(0.5, 0.04, txt, wrap=True, horizontalalignment='center', fontsize=8)
            plt.figtext(0.5, 0.01, txt2, wrap=True, horizontalalignment='center', fontsize=8)
            plt.tight_layout(pad=padding)    
            plt.title('Epix Spectrum | ' +str(boot)+ ' loops | ' + str(round(fraction,2)) + ' of data per' )
        if xrt_plot:
            fig_2, ax_2 = plt.subplots()
            plt.xlabel('energy, keV')
            plt.figtext(0.5, 0.04, txt, wrap=True, horizontalalignment='center', fontsize=8)
            plt.figtext(0.5, 0.01, txt2, wrap=True, horizontalalignment='center', fontsize=8)
            plt.tight_layout(pad=padding)    
            plt.title('XRT Spectrum | ' +str(boot)+ ' loops | random ' + str(round(fraction,2)) + ' of data per' )

        if plot_meanwise:

            if resid_plot:
                fig_3, ax_3 = plt.subplots()
                plt.xlabel('energy, keV')
                plt.figtext(0.5, 0.04, txt, wrap=True, horizontalalignment='center', fontsize=8)
                plt.figtext(0.5, 0.01, txt2, wrap=True, horizontalalignment='center', fontsize=8)
                plt.tight_layout(pad=padding)    
                plt.title('avg(epix)- avg(xrt) | ' +str(boot)+ ' loops | random ' + str(round(fraction,2)) + ' of data per' )

            if deltaT_T_plot:
                fig_4, ax_4 = plt.subplots()
                plt.xlabel('energy, keV')
                plt.figtext(0.5, 0.04, txt, wrap=True, horizontalalignment='center', fontsize=8)
                plt.figtext(0.5, 0.01, txt2, wrap=True, horizontalalignment='center', fontsize=8)
                plt.tight_layout(pad=padding)    
                plt.title('[avg(epix)-avg(xrt)]/avg(xrt) | ' +str(boot)+ ' loops | random ' + str(round(fraction,2)) + ' of data per' )

        if plot_shotwise:
            if resid_plot:
                fig_5, ax_5 = plt.subplots()
                plt.xlabel('energy, keV')
                plt.figtext(0.5, 0.04, txt, wrap=True, horizontalalignment='center', fontsize=8)
                plt.figtext(0.5, 0.01, txt2, wrap=True, horizontalalignment='center', fontsize=8)
                plt.tight_layout(pad=padding)    
                plt.title('avg(epix-xrt) | ' +str(boot)+ ' loops | random ' + str(round(fraction,2)) + ' of data per' )

            if deltaT_T_plot:
                fig_6, ax_6 = plt.subplots()
                plt.xlabel('energy, keV')
                plt.figtext(0.5, 0.04, txt, wrap=True, horizontalalignment='center', fontsize=8)
                plt.figtext(0.5, 0.01, txt2, wrap=True, horizontalalignment='center', fontsize=8)
                plt.tight_layout(pad=padding)    
                plt.title('avg[(epix-xrt)/xrt] | ' +str(boot)+ ' loops | random ' + str(round(fraction,2)) + ' of data per' )

                
                
                
        for j in range(0,compare[0].shape[0]):
            for i in range(0,boot):
                rand_=np.random.choice(len(compare[1][j]), np.int64(len(compare[1][j])*fraction), replace=False)
                rand_shots_epix = compare[1][j][rand_]
                rand_shots_xrt = scale*compare[0][j][rand_]
                rand_shots_residual = rand_shots_epix-rand_shots_xrt
                rand_shots_DeltaT_T = rand_shots_residual/(scale*rand_shots_xrt)
                
                rand_comp_=np.random.choice(len(compare_comp[1][j]), np.int64(len(compare_comp[1][j])*fraction), replace=False)
                rand_shots_epix_comp = compare_comp[1][j][rand_comp_]
                rand_shots_xrt_comp = scale*compare_comp[0][j][rand_comp_]
                rand_shots_residual_comp = rand_shots_epix_comp-rand_shots_xrt_comp
                rand_shots_DeltaT_T_comp = rand_shots_residual_comp/(scale_comp*rand_shots_xrt_comp)

                if epix_plot:
                    ax_1.plot(energy,np.mean(rand_shots_epix,0),color=colors[j])
                    ax_1.plot(energy,np.mean(rand_shots_epix_comp,0),color='m')

                if xrt_plot:
                    ax_2.plot(energy,np.mean(rand_shots_xrt,0),color=colors[j])
                    ax_2.plot(energy,np.mean(rand_shots_xrt_comp,0),color='m')

                if plot_meanwise:

                    if resid_plot:
                        ax_3.plot(energy,np.mean(rand_shots_epix,0)-np.mean(rand_shots_xrt,0),color=colors[j])
                        ax_3.plot(energy,np.mean(rand_shots_epix_comp,0)-np.mean(rand_shots_xrt_comp,0),color='m')
                    if deltaT_T_plot:
                        ax_4.plot(energy,(np.mean(rand_shots_epix,0)-np.mean(rand_shots_xrt,0))/np.mean(rand_shots_xrt,0),color=colors[j])
                        ax_4.plot(energy,(np.mean(rand_shots_epix_comp,0)-np.mean(rand_shots_xrt_comp,0))/np.mean(rand_shots_xrt_comp,0),color='m')

                if plot_shotwise:

                    if resid_plot:
                        ax_5.plot(energy,np.mean(rand_shots_epix-rand_shots_xrt,0),color=colors[j])
                        ax_5.plot(energy,np.mean(rand_shots_epix_comp-rand_shots_xrt_comp,0),color='m')
                    if deltaT_T_plot:
                        ax_6.plot(energy,np.mean((rand_shots_epix-rand_shots_xrt)/rand_shots_xrt,0),color=colors[j])
                        ax_6.plot(energy,np.mean((rand_shots_epix_comp-rand_shots_xrt_comp)/rand_shots_xrt_comp,0),color='m')


        if epix_plot:
            ax_1.legend((scans_to_plot[0],scans_to_plot_comp[0]),labelcolor=colors)
        if xrt_plot:
            ax_2.legend((scans_to_plot,scans_to_plot_comp[0]),labelcolor=colors)
        if plot_meanwise:
            if resid_plot:
                ax_3.legend((scans_to_plot[0],scans_to_plot_comp[0]),labelcolor=colors)
            if deltaT_T_plot:
                ax_4.legend((scans_to_plot[0],scans_to_plot_comp[0]),labelcolor=colors)
        if plot_shotwise:
            if resid_plot:
                ax_5.legend((scans_to_plot[0],scans_to_plot_comp[0]),labelcolor=colors)
            if deltaT_T_plot:
                ax_6.legend((scans_to_plot[0],scans_to_plot_comp[0]),labelcolor=colors)