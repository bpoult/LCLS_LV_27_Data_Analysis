# Written by Ben Poulter (Khalil Group, University of Washington), May 2021
# For LV27 LCLS Beamtime.

import numpy as np
import os
import matplotlib.pyplot as plt
import pickle


class processed_data_class:
    _defaults = ('eventIDs',
                'high_diode_us',
                'low_diode_us',
                'xrt_intensity',
                'epix_intensity',
                'scan_name',
                'epix_motor',
                'save_dir',
                'calibration_info',
                'previous_cal',
                'epix_energy_windowed',
                'epix_windowed',
                'xrt_energy_windowed',
                'xrt_windowed',
                'xrt_red_res',
                'filters')

    _default_value = None

    def __init__(self, **kwargs):
        self.__dict__.update(dict.fromkeys(self._defaults, self._default_value))
        self.__dict__.update(kwargs)

    def changeValue(self, **kwargs):
        self.__dict__.update(kwargs)

    def getKeys(self):
        return self.__dict__.keys()


    def scale_spectrometers(self,probe_run):
        processed_data = self
        if np.logical_and(processed_data.scan_name == 'run_' + str(probe_run[0]),probe_run[1]):
            print(processed_data.scan_name)
            probe_run = [probe_run[0],False]
            epix_sum = np.mean(processed_data.epix_windowed, 0)
            xrt_sum = np.mean(processed_data.xrt_red_res, 0)

            scaling1 = np.max(xrt_sum) / np.max(epix_sum)
            scaling2 = epix_sum / xrt_sum
            scaling3 = scaling2 / np.max(scaling2)
            spec_scale = scaling2
            with open(processed_data.calibration_info[5][0] + 'spec_scaled_'+str(probe_run[0])+'_'+processed_data.calibration_info[5][1] + '.pkl', 'wb') as f:
                pickle.dump(spec_scale, f)
            return probe_run


        if not os.path.exists(processed_data.calibration_info[5][0] + 'spec_scaled_'+str(probe_run[0])+'_'+processed_data.calibration_info[5][1] + '.pkl'):
            print('There is no spec_scaling file saved for run ' + str(processed_data.scan_name))
            return
        with open(processed_data.calibration_info[5][0] + 'spec_scaled_'+str(probe_run[0])+'_'+processed_data.calibration_info[5][1] + '.pkl','rb') as f:
            spec_scale = pickle.load(f)
        xrt_based = np.asarray([spec_scale*processed_data.xrt_red_res[i] for i in range(0,len(processed_data.xrt_red_res))])
        xrt_intensity = np.sum(xrt_based,1)
        epix_intensity = np.sum(processed_data.epix_windowed,1)
        processed_data.changeValue(xrt_based=xrt_based,xrt_intensity=xrt_intensity,epix_intensity=epix_intensity)
        return






