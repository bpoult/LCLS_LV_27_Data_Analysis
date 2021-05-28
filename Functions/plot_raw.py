# Written by Ben Poulter (Khalil Group, University of Washington), May 2021
# For LV27 LCLS Beamtime.
import matplotlib.pyplot as plt
import os
import sys
import numpy as np
import psana as ps
import pickle
from raw_data_class import RawData as RDC

def plot_raw(datas, plot_one, x_axis, on_off,calibration_file):
    if not on_off:
        print('Raw Data plotting is turned off.')
        return
    
    runs = [datas[i].scan_name for i in range(0, len(datas))]
    events_array = []
    epix_array = []
    xrt_array = []
    epix_rois = []
    xrt_rois = []
    for i in range(0,len(datas)):
        if not datas[i].eventIDs:
            continue
        events_array.append(datas[i].eventIDs)
        epix_array.append(np.mean(datas[i].epix_spectrum, 0))
        xrt_array.append(np.mean(datas[i].xrt_spectrum,0))
        epix_rois.append(datas[i].epix_roi)
        xrt_rois.append(datas[i].xrt_roi)
    
    events_array = np.asarray(events_array)
    epix_array = np.asarray(epix_array)
    xrt_array = np.asarray(xrt_array)
    epix_rois = np.asarray(epix_rois)
    xrt_rois = np.asarray(xrt_rois)
    
    if not any(x == 'run_' + str(plot_one) for x in runs) and plot_one is not False:
        print('The run you want to plot individually is not in the input runs')
        return

        
    idx = runs.index('run_' + str(plot_one))
    if x_axis == 'pixels':
        if plot_one:
            plt.figure()
            plt.plot(range(xrt_rois[idx][0], xrt_rois[idx][1]), xrt_array[idx])
            plt.title('xrt spectrum of run_' + str(plot_one))
            plt.xlabel('Pixels')
            plt.show()

            plt.figure()
            plt.plot(range(epix_rois[idx][2], epix_rois[idx][3]), epix_array[idx])
            plt.title('epix spectrum of run_' + str(plot_one))
            plt.xlabel('Pixels')
            plt.show()
            
            
            fig, ax = plt.subplots()
            plt.title('average epix image from run_' + str(plot_one))
            x_y = [epix_rois[idx][2], epix_rois[idx][3],epix_rois[idx][0],epix_rois[idx][1]]
            plt.xlabel('Pixels')
            ax.imshow(datas[idx].avg_epix_2d, extent=x_y)
            
        if not all(datas[0].epix_motor == datas[x].epix_motor for x in range(0,len(datas))) and all(x == xrt_rois[0] for x in xrt_rois):
            print('You are trying to average epix spectra with different epix motor positions.')
            print('You are trying to average xrt spectra with different ROIs.')
            return
        
        if not all(datas[0].epix_motor == datas[x].epix_motor for x in range(0,len(datas))):
            print('You are trying to average epix spectra with different epix motor positions.')
            plt.figure()
            plt.plot(range(xrt_rois[idx][0], xrt_rois[idx][1]), np.mean(xrt_array, 0))
            plt.title('xrt spectrum of averaged runs')
            plt.xlabel('Pixels')
            return
        
        if not all(x == xrt_rois[0] for x in xrt_rois):
            print('You are trying to average xrt spectra with different ROIs.')
            plt.figure()
            plt.plot(range(epix_rois[idx][2], epix_rois[idx][3]), np.mean(epix_array, 0))
            plt.title('epix spectrum of averaged runs')
            plt.xlabel('Pixels')
            return

        plt.figure()
        plt.plot(range(xrt_rois[idx][0], xrt_rois[idx][1]), np.mean(xrt_array, 0))
        plt.title('xrt spectrum of averaged runs')
        plt.xlabel('Pixels')

        plt.figure()
        plt.plot(range(epix_rois[idx][2], epix_rois[idx][3]), np.mean(epix_array, 0))
        plt.title('epix spectrum of averaged runs')
        plt.xlabel('Pixels')
        
        
        
        
        return

    if x_axis == 'energy':
        
        if not os.path.exists(calibration_file[0]+calibration_file[1]+'.pkl'):
            print('The calibration file does not exist.')
            return
        
        with open(calibration_file[0]+calibration_file[1]+'.pkl', "rb") as f: 
            calibration = pickle.load(f)
            check_matching = [datas[i].epix_motor == calibration[9] for i in range(0,len(datas))]
            
        if not all(check_matching):
            print('The calibration and the following runs have different epix motor positions: ')
            print([runs[i] for i in range(0,len(runs)) if check_matching[i] is False])
            return
        
        if plot_one:

            plt.figure()
            plt.plot(calibration[7], xrt_array[idx])
            plt.title('xrt spectrum of run_' + str(plot_one))
            plt.xlabel('Energy, keV')
            plt.show()

            plt.figure()
            plt.plot(calibration[8], epix_array[idx])
            plt.title('epix spectrum of run_' + str(plot_one))
            plt.xlabel('Energy, keV')
            plt.show()
            
            fig, ax = plt.subplots()
            plt.title('average epix image from run_' + str(plot_one))
            x_y = [calibration[8][0],calibration[8][-1],0,0.05]
            plt.xlabel('energy, keV')
            ax.imshow(datas[idx].avg_epix_2d,extent=x_y)

        plt.figure()
        plt.plot(calibration[7], np.mean(xrt_array, 0))
        plt.title('xrt spectrum of averaged runs')
        plt.xlabel('Energy, keV')

        plt.figure()
        plt.plot(calibration[8], np.mean(epix_array, 0))
        plt.title('epix spectrum of averaged runs')
        plt.xlabel('Energy, keV')
        
        return
