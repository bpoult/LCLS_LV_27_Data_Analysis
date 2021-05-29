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


    def scale_spectrometers(self,probe_run,scaling):
        processed_data = self
        if np.logical_and(processed_data.scan_name == 'run_' + str(probe_run[0]),probe_run[1]):
            print('New spec scaling made from' + processed_data.scan_name)
            print('')
            probe_run = [probe_run[0],False]
            epix_mean = np.mean(processed_data.epix_norm, 0)
            xrt_mean = np.mean(processed_data.xrt_norm, 0)

            scaling1 = np.mean(np.divide(processed_data.epix_norm,processed_data.xrt_norm),0)
            scaling2 = epix_mean / xrt_mean
            if scaling:
                spec_scale = scaling2
            if not scaling:
                spec_scale = scaling1
            with open(processed_data.calibration_info[5][0] + 'spec_scaled_'+str(probe_run[0])+'_'+processed_data.calibration_info[5][1] + '.pkl', 'wb') as f:
                pickle.dump(spec_scale, f)
            return probe_run,spec_scale


        if not os.path.exists(processed_data.calibration_info[5][0] + 'spec_scaled_'+str(probe_run[0])+'_'+processed_data.calibration_info[5][1] + '.pkl'):
            print('There is no spec_scaling file saved for run ' + str(processed_data.scan_name))
            return
        with open(processed_data.calibration_info[5][0] + 'spec_scaled_'+str(probe_run[0])+'_'+processed_data.calibration_info[5][1] + '.pkl','rb') as f:
            spec_scale = pickle.load(f)
        xrt_based_norm = np.asarray([spec_scale*processed_data.xrt_norm[i] for i in range(0,len(processed_data.xrt_norm))])
#         xrt_based = np.asarray([spec_scale*processed_data.xrt_red_res[i] for i in range(0,len(processed_data.xrt_red_res))])
        processed_data.changeValue(xrt_based_norm=xrt_based_norm)
        return






