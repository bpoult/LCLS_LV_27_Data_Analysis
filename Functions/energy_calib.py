import numpy as np
import pickle
import datetime
def energy_calib(raw_data, calibration,save_cal):
    calib = calibration.copy()
    xrt_pix = np.asarray([calib[2][x] for x in range(0, len(calib[2])) if calib[2][x] != 0])
    keV_xrt = np.asarray([calib[1][x] for x in range(0, len(calib[2])) if calib[2][x] != 0])
    epix_pix = np.asarray([calib[3][x] for x in range(0, len(calib[3])) if calib[3][x] != 0])
    keV_epix = np.asarray([calib[1][x] for x in range(0, len(calib[3])) if calib[3][x] != 0])

    m_xrt, b_xrt = np.polyfit(xrt_pix, keV_xrt, 1)
    m_epix, b_epix = np.polyfit(epix_pix, keV_epix, 1)

    xrt_energy = m_xrt * np.arange(raw_data.xrt_roi[0], raw_data.xrt_roi[1]) + b_xrt
    epix_energy = m_epix * np.arange(raw_data.epix_roi[2], raw_data.epix_roi[3]) + b_epix


    calib[0] = calib[0] + list(['xrt_energy', 'epix_energy','time_calibrated'])
    calib.append(xrt_energy)
    calib.append(epix_energy)
    calib.append(datetime.datetime.now())
    
    raw_data.changeValue(calibration=calib)
    
    if save_cal == True:
        with open(raw_data.save_dir + raw_data.scan_name + '/' + "rawdata.pkl", "wb") as f:
            pickle.dump(raw_data, f)
    return raw_data