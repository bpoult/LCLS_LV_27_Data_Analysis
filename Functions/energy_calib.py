import numpy as np
import pickle
import datetime
import os
import psana as ps
def energy_calib(calibration,save_cal):
    calib = calibration.copy()
    xrt_pix = np.asarray([calib[2][x] for x in range(0, len(calib[2])) if calib[2][x] != 0])
    keV_xrt = np.asarray([calib[1][x] for x in range(0, len(calib[2])) if calib[2][x] != 0])
    epix_pix = np.asarray([calib[3][x] for x in range(0, len(calib[3])) if calib[3][x] != 0])
    keV_epix = np.asarray([calib[1][x] for x in range(0, len(calib[3])) if calib[3][x] != 0])

    m_xrt, b_xrt = np.polyfit(xrt_pix, keV_xrt, 1)
    m_epix, b_epix = np.polyfit(epix_pix, keV_epix, 1)
    
    epix_motor = []
    ds_list = [ps.DataSource('exp=cxix46119:run='+str(calib[6][i])+':smd') for i in range(0,len(calib[6]))]
    for i in range(0,len(ds_list)):
        ds = ps.DataSource('exp=cxix46119:run='+str(calib[6][i])+':smd')
        det = ps.Detector('CXI:DG2:MMS:10.RBV')
        ds.events().__next__()
        epix_motor.append(det())

    if not all(x == epix_motor[0] for x in epix_motor):
        print('Your calibration scans have different epix motor positions.')
        x = [print('run_' + str(calib[6][i])+ ': ' + str(round(epix_motor[i],4)) + ' mm') for i in range(0,len(epix_motor))]
        return
    
    if all(x == epix_motor[0] for x in epix_motor):
        xrt_energy = m_xrt * np.arange(calib[4][0][0],calib[4][0][1]) + b_xrt
        epix_energy = m_epix * np.arange(calib[4][1][2],calib[4][1][3]) + b_epix

        calib[0] = calib[0] + list(['xrt_energy', 'epix_energy','epix_motor','time_calibrated'])
        calib.append(xrt_energy)
        calib.append(epix_energy)
        calib.append(epix_motor[0])
        calib.append(datetime.datetime.now())
    
        if save_cal == True:
            if not os.path.isdir(calib[5][0]):
                os.mkdir(calib[5][0])
            if not os.path.isdir(calib[5][0]+calib[5][1]):
                with open(calib[5][0] + calib[5][1] + '.pkl', "wb") as f:
                    pickle.dump(calib, f)
                    print(calib[5][1] + '.pkl has been saved.')
            if os.path.exists(calib[5][0] + calib[5][1] + '.pkl') and input('Overwrite ' + calib[5][1]+ '.pkl? (y/n)') is 'y':
                with open(calib[5][0] + calib[5][1] + '.pkl', "wb") as f:
                    pickle.dump(calib, f)
                    print(calib[5][1] + '.pkl has been saved.')
        return calib
