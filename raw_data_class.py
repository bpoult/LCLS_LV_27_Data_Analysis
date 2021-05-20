# Written by Ben Poulter for LCLS run 19, LV 27.

import matplotlib.pyplot as plt
import numpy as np
import psana as ps


class RawData:
    _defaults = ['eventIDs',
                 'photon_energies',
                 'I0_fee',
                 'high_diode_us',
                 'low_diode_us',
                 'epix_roi',
                 'xrt_roi',
                 'epix_spectrum',
                 'xrt_spectrum',
                 'avg_epix_2d',
                 'xrt_intensity',
                 'epix_intensity',
                 'scan_name']

    _default_value = None

    def __init__(self, **kwargs):
        self.__dict__.update(dict.fromkeys(self._defaults, self._default_value))
        self.__dict__.update(kwargs)

    def changeValue(self, **kwargs):
        self.__dict__.update(kwargs)

    def getKeys(self):
        return self.__dict__.keys()

    # labels = ['notch_energies', 'xrt_pixels', 'epix_pixels']
    # notch_energies = [7.06, 7.065, 7.07, 7.075, 7.08, 7.085, 7.09]  # keV
    # xrt_pixels = [0, 1, 2, 3, 4, 5, 0]  # enter 0 if you can't see the notch
    # epix_pixels = [1, 2, 3, 4, 5, 6]  # enter 0 if you can't see the notch
    # calib = [labels, notch_energies, xrt_pixels, epix_pixels]

    def energy_calib(self, calib):
        raw_data = self
        xrt_pix = np.asarray([calib[2][x] for x in range(0,len(calib[2])) if calib[2][x] != 0])
        keV_xrt = np.asarray([calib[1][x] for x in range(0, len(calib[2])) if calib[2][x] != 0])
        epix_pix = np.asarray([calib[3][x] for x in range(0,len(calib[3])) if calib[3][x] != 0])
        keV_epix = np.asarray([calib[1][x] for x in range(0, len(calib[3])) if calib[3][x] != 0])

        m_xrt, b_xrt = np.polyfit(xrt_pix, keV_xrt, 1)
        m_epix, b_epix = np.polyfit(epix_pix, keV_epix, 1)

        xrt_energy = m_xrt*np.arange(raw_data.xrt_roi[0],raw_data.xrt_roi[1])+b_xrt
        epix_energy = m_epix * np.arange(raw_data.epix_roi[2], raw_data.epix_roi[3]) + b_epix

        calib[0].append(['xrt_energy','epix_energy'])
        calib.append([xrt_energy,epix_energy])

        raw_data.changeValue(calibration=calib)
        return raw_data
