# Written by Ben Poulter for LCLS run 19, LV 27.

import matplotlib.pyplot as plt
import numpy as np
import psana as ps
import pickle
import os
from processed_data_class import processed_data_class as PDC


class RawData:
    _defaults = ['eventIDs',
                'photon_energies',
                'pulse_energies_fee',
                'high_diode_us',
                'low_diode_us',
                'epix_roi',
                'xrt_roi',
                'epix_spectrum',
                'xrt_spectrum',
                'avg_epix_2d',
                'xrt_intensity',
                'epix_intensity',
                'scan_name',
                'epix_motor',
                'save_dir',
                'ds_string',
                'previous_cal',
                'epix_energy_windowed',
                'epix_windowed',
                'xrt_energy_windowed',
                'xrt_windowed']

    _default_value = None

    def __init__(self, **kwargs):
        self.__dict__.update(dict.fromkeys(self._defaults, self._default_value))
        self.__dict__.update(kwargs)

    def changeValue(self, **kwargs):
        self.__dict__.update(kwargs)

    def getKeys(self):
        return self.__dict__.keys()
    
    def make_pro_data(self,conditions,filters):
        processed_data = PDC()
        raw=self
        
        combined_conditions = np.asarray(conditions).all(axis=0)
        
        processed_data.changeValue(eventIDs=raw.eventIDs[combined_conditions],
                                   high_diode_us=raw.high_diode_us[combined_conditions],
                                   low_diode_us=raw.low_diode_us[combined_conditions],
                                   xrt_intensity=raw.xrt_intensity[combined_conditions],
                                   epix_intensity=raw.epix_intensity[combined_conditions],
                                   scan_name=raw.scan_name,
                                   epix_motor=raw.epix_motor,
                                   save_dir=raw.save_dir,
                                   calibration_info=raw.calibration_info,
                                   previous_cal=raw.previous_cal,
                                   epix_energy_windowed=raw.epix_energy_windowed,
                                   epix_windowed=raw.epix_windowed[combined_conditions],
                                   xrt_energy_windowed=raw.xrt_energy_windowed,
                                   xrt_windowed=raw.xrt_windowed[combined_conditions],
                                   xrt_red_res=raw.xrt_red_res[combined_conditions],
                                   filters=filters)
        
        if not os.path.isdir(processed_data.save_dir + processed_data.scan_name):
            try:
                os.mkdir(processed_data.save_dir + processed_data.scan_name)
            except:
                os.mkdir(processed_data.save_dir)
                os.mkdir(processed_data.save_dir + processed_data.scan_name)

        with open(processed_data.save_dir + processed_data.scan_name + '/' + "pro_data.pkl", "wb") as f:
            pickle.dump(processed_data, f)
        
        return processed_data
        

    
    
    