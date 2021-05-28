# Written by Ben Poulter (Khalil Group, University of Washington), May 2021
# For LV27 LCLS Beamtime.

import numpy as np
import os
import pickle
import matplotlib.pyplot as plt
from raw_data_class import RawData as RDC
from .reduce_matrix_size import get_column_compressor

def reduce_res(raw_data):
    dir_to_matrix = raw_data.calibration_info[5][0] + 'reduction_matrix_' + str(raw_data.calibration_info[5][1]) + '.pkl'
    if os.path.exists(dir_to_matrix):
        with open(dir_to_matrix, "rb") as f:
            reduction_matrix = pickle.load(f)
        if not np.logical_or(reduction_matrix.shape[0]==raw_data.xrt_energy_windowed.shape[0],reduction_matrix.shape[1]==raw_data.epix_energy_windowed.shape[0]):
            reduction_matrix = get_column_compressor(raw_data.xrt_energy_windowed.shape[0],raw_data.epix_energy_windowed.shape[0])
            with open(dir_to_matrix, "wb") as f:
                pickle.dump(reduction_matrix, f)     
                
    else:
        reduction_matrix = get_column_compressor(raw_data.xrt_energy_windowed.shape[0],raw_data.epix_energy_windowed.shape[0])
        with open(dir_to_matrix, "wb") as f:
            pickle.dump(reduction_matrix, f)
            
    input_xrt = np.asarray([raw_data.xrt_windowed[i][np.newaxis, :] for i in range(0, len(raw_data.xrt_windowed))])
    xrt_red_res = np.asarray([np.flip(np.squeeze(input_xrt[i] @ reduction_matrix)) for i in range(0, len(input_xrt))])

    raw_data.changeValue(xrt_red_res=xrt_red_res)
    with open(raw_data.save_dir + raw_data.scan_name + "/" + "rawdata.pkl", "wb") as f:
        pickle.dump(raw_data,f)
            
    return

def apply_window(raw_data,energy_window):
    epix_window = np.logical_and(raw_data.calibration_info[8] > energy_window[0], raw_data.calibration_info[8] < energy_window[1])
    epix_energy_windowed = raw_data.calibration_info[8][epix_window]
    
    xrt_window = [np.abs(raw_data.calibration_info[7]-epix_energy_windowed[-1]).argmin(),np.abs(raw_data.calibration_info[7]-epix_energy_windowed[0]).argmin()]
    xrt_energy_windowed=raw_data.calibration_info[7][xrt_window[0]:xrt_window[-1]]


    epix_windowed = np.asarray([raw_data.epix_spectrum[i][epix_window] for i in range(0,len(raw_data.epix_spectrum))])
    xrt_windowed = np.asarray([raw_data.xrt_spectrum[i][xrt_window[0]:xrt_window[-1]] for i in range(0,len(raw_data.xrt_spectrum))])

    raw_data.changeValue(epix_energy_windowed=epix_energy_windowed,
                         epix_windowed=epix_windowed,
                         xrt_energy_windowed=xrt_energy_windowed,
                         xrt_windowed=xrt_windowed)
    return
