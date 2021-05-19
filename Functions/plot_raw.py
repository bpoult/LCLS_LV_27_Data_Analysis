import matplotlib.pyplot as plt
import os
import sys
import numpy as np
import psana as ps


def plot_raw(datas, plot_one, x_axis, on_off):
    if not on_off:
        print('Raw Data plotting is turned off.')
        return

    runs = [datas[i].scan_name for i in range(0, len(datas))]
    epix_array = np.asarray([np.mean(datas[i].epix_spectrum, 0) for i in range(0, len(datas))], dtype=object)
    xrt_array = np.asarray([np.mean(datas[i].xrt_spectrum,0) for i in range(0, len(datas))], dtype=object)
    epix_rois = [datas[i].epix_roi for i in range(0, len(datas))]
    xrt_rois = [datas[i].xrt_roi for i in range(0, len(datas))]

    if not any(x == 'run_' + str(plot_one) for x in runs):
        print('The run you want to plot individually is not in the input runs')
        return

    idx = runs.index('run_' + str(plot_one))
    if x_axis == 'pixels':

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

        if not all(x == epix_rois[0] for x in epix_rois):
            print('You are trying to average epix spectra with different ROIs.')
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
        check_calib = [hasattr(datas[i], 'calibration') for i in range(0, len(datas))]

        if not any(check_calib):
            non_calib = [str(runs[i]) for i in range(0, len(runs)) if check_calib[i] is False]
            print('The following do not have calibrations: ' + str(non_calib))
            return
        calib_arrays = [datas[i].calibration for i in range(0, len(datas))]

        plt.figure()
        plt.plot(datas.calibration[4], xrt_array[idx])
        plt.title('xrt spectrum of run_' + str(plot_one))
        plt.xlabel('Energy, keV')
        plt.show()

        plt.figure()
        plt.plot(datas.calibration[5], epix_array[idx])
        plt.title('epix spectrum of run_' + str(plot_one))
        plt.xlabel('Energy, keV')
        plt.show()

        if not all(calib_arrays[0][5] == x for x in [calib_arrays[i][5] for i in range(0, len(calib_arrays))]):
            print('You are trying to average epix spectra with different energy ranges.')
            plt.figure()
            plt.plot(datas.calibration[4], np.mean(xrt_array, 0))
            plt.title('xrt spectrum of averaged runs')
            plt.xlabel('Energy, keV')
            return

        if not all(calib_arrays[0][4] == x for x in [calib_arrays[i][4] for i in range(0, len(calib_arrays))]):
            print('You are trying to average xrt spectra with different energy ranges.')
            plt.figure()
            plt.plot(datas.calibration[5], np.mean(epix_array, 0))
            plt.title('epix spectrum of averaged runs')
            plt.xlabel('Energy, keV')
            return

        plt.figure()
        plt.plot(datas.calibration[4], np.mean(xrt_array, 0))
        plt.title('xrt spectrum of averaged runs')
        plt.xlabel('Energy, keV')

        plt.figure()
        plt.plot(datas.calibration[5], np.mean(epix_array, 0))
        plt.title('epix spectrum of averaged runs')
        plt.xlabel('Energy, keV')
        return
