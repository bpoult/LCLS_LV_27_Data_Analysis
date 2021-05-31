import numpy as np
import psana as ps
import sys
import os
from raw_data_class import RawData as RDC
from processed_data_class import processed_data_class as PDC
import pickle


def load_pro(scans_to_plot):
    pro_datas = []
    save_dir = '/reg/d/psdm/cxi/cxilv2718/results/data/'
    for i in range(0,len(scans_to_plot)):
        scan_name = 'run_' + str(scans_to_plot[i])
        if os.path.exists(save_dir+ scan_name + "/" + "pro_data.pkl"):
            with open(save_dir+ scan_name + "/" + "pro_data.pkl", "rb") as f:
                processed_data = pickle.load(f)
                pro_datas = pro_datas + [processed_data]
                print('Loaded processed_data for run ' + processed_data.scan_name)
        else:
            print('You are trying to load a file that does not exist.')
            return
    return pro_datas


