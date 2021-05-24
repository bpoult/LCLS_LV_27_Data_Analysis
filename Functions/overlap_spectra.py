import numpy as np
import os
import pickle
from reduce_matrix_size import get_row_compressor
from raw_data_class import RawData as RDC

def overlap_spectra(raw_data,energy_window):
    raw1 = apply_window(raw_data,energy_window)
    raw2 = reduce_res(raw1)
    scaling_factor =create_scaling_factor(raw2)

    overlapped_xrt = np.asarray([scaling_factor*raw2.xrt_red_res[i] for i in range(0,len(raw2.xrt_red_res))])
    raw2.changeValue(overlapped_xrt=overlapped_xrt)

    return raw2

def create_scaling_factor(raw_data):
    dir_to_scaling = raw_data.calibration_info[5][0] + 'spec_scaling_factor_' +str(raw_data.calibration_info[5][1])+ '.pkl'
    if not os.path.exists(dir_to_scaling):
        xrt_sum = np.sum(raw_data.xrt_windowed_red,0)
        epix_sum = np.sum(raw_data.epix_windowed,0)

        part1 = np.max(xrt_sum)/np.max(epix_sum)
        part2 = part1*epix_sum/xrt_sum
        part3 = part2/np.max(part2)
        scaling_factor = part3

        with open(dir_to_scaling, "wb") as f:
            pickle.dump(scaling_factor, f)
    else:
        with open(dir_to_scaling, "rb") as f:
            scaling_factor = pickle.load(f)
    return scaling_factor

def reduce_res(raw_data):
    dir_to_matrix = raw_data.calibration_info[5][0] + 'reduction_matrix_' + str(raw_data.calibration_info[5][1]) + '.pkl'
    if not os.path.exists(dir_to_matrix):
        reduction_matrix = get_row_compressor(raw_data.xrt_energy_windowed.shape[0],raw_data.epix_energy_windowed.shape[0])
        with open(dir_to_matrix, "wb") as f:
            pickle.dump(reduction_matrix, f)

    else:
        with open(dir_to_matrix, "rb") as f:
            reduction_matrix = pickle.load(f)
    input_xrt = [raw_data.xrt_windowed_red[i][np.newaxis, :] for i in range(0, len(raw_data.xrt_windowed))]
    xrt_red_res = np.asarray([np.squeeze(input_xrt[i] @ reduction_matrix) for i in range(0, len(input_xrt))])
    raw_data.changeValue(xrt_red_res=xrt_red_res)

    return raw_data

def apply_window(raw_data,energy_window):
    epix_window = np.logical_and(raw_data.calibration_info[8] > energy_window[0], raw_data.calibration_info[8] < energy_window[1])
    xrt_window = np.logical_and(raw_data.calibration_info[7] > energy_window[0], raw_data.calibration_info[7] < energy_window[1])
    epix_energy_windowed = raw_data.calibration_info[8][epix_window]
    xrt_energy_windowed = raw_data.calibration_info[7][xrt_window]

    epix_windowed = [raw_data.epix_spectrum[i][epix_window] for i in range(0,len(raw_data.epix_spectrum))]
    xrt_windowed = [raw_data.xrt_spectrum[i][xrt_window] for i in range(0,len(raw_data.xrt_spectrum))]

    raw_data.changeValue(epix_energy_windowed=epix_energy_windowed, epix_windowed=epix_windowed,
                         xrt_windowed_red=xrt_windowed_red,xrt_energy_windowed=xrt_energy_windowed,
                         xrt_windowed=xrt_windowed)
    return raw_data
