# Written by Ben Poulter (Khalil Group, University of Washington), May 2021
# For LV27 LCLS Beamtime.

import sys
import os
import numpy as np
import psana as ps
import pickle
import matplotlib.pyplot as plt
import time
from raw_data_class import RawData as RDC

def load_data(save_dir,scan_name,ds_string, epix_roi, xrt_roi):
    RawData = RDC()

    ds = ps.DataSource(ds_string)
    epix = ps.Detector('epix10k135')
    XRT = ps.Detector('FEE-SPEC0')
    wave8 = ps.Detector('CXI-DG3-BMMON')
    electronBeam = ps.Detector('EBeam')
    fee = ps.Detector('FEEGasDetEnergy')

    eventIDs = []
    epix_events = []
    xrt_events = []
    low_diode_us_events = []
    high_diode_us_events = []
    photon_energies = []
    pulse_energies = []
    i = 0

    epix_roiYMin = epix_roi[2]
    epix_roiYMax = epix_roi[3]
    epix_roiXMin = epix_roi[0]
    epix_roiXMax = epix_roi[1]
    epix_roiSum = np.zeros([epix_roiXMax - epix_roiXMin, epix_roiYMax - epix_roiYMin])

    XRTMin = xrt_roi[0]
    XRTMax = xrt_roi[1]
    start = time.time()

    for nevent, evt in enumerate(ds.events()):
        epix_evt = epix.calib_data(evt)
        xrt_evt = XRT.get(evt)
        wave8_evt = wave8.get(evt)
        ebeam_evt = electronBeam.get(evt)
        fee_evt = fee.get(evt)
        condition = epix_evt is None or xrt_evt is None or wave8_evt is None or ebeam_evt is None or fee_evt is None

        if condition:
            continue
        diodes = wave8_evt.peakA()
        photonEnergy = ebeam_evt.ebeamPhotonEnergy()
        keV = photonEnergy / 1000.0  # scale photon energy
        epix_data = np.rint(epix_evt[0, epix_roiXMin:epix_roiXMax, epix_roiYMin:epix_roiYMax] / keV)
        epix_data[epix_data < 0.0] = 0.0
        epix_roiSum += epix_data
        low_diode_us_evt = -1.0 * diodes[8] * 13.0  # /0.12230 #scale by 50 micron Fe foil transmission at 7 keV
        high_diode_us_evt = (-1.0 * diodes[12]) - low_diode_us_evt

        eventIDs.append(nevent)
        photon_energies.append(photonEnergy)
        pulse_energies.append([fee_evt.f_11_ENRC(),fee_evt.f_21_ENRC(),fee_evt.f_63_ENRC()])
        low_diode_us_events.append(low_diode_us_evt)
        high_diode_us_events.append(high_diode_us_evt)
        epix_events.append(np.sum(np.squeeze(epix_data), 0))
        xrt_events.append(xrt_evt.hproj()[XRTMin:XRTMax])
        i += 1
        print('Loading: ...  Currently on shot: ' + str(i), end="\r", flush=True)

    elapsed_time = (time.time() - start)
    print('Data loaded in ' + str(np.round(elapsed_time, 1)) + ' seconds.')
    print(str(nevent - i) + ' out of ' + str(nevent) + ' shots had empty values.')
    eventIDs = np.asarray(eventIDs)
    photon_energies = np.asarray(photon_energies)
    pulse_energies = np.asarray(pulse_energies)
    low_diode_us_events = np.asarray(low_diode_us_events)
    high_diode_us_events = np.asarray(high_diode_us_events)
    epix_events = np.asarray(epix_events)
    xrt_events = np.asarray(xrt_events)
    epix_motor = ps.Detector('CXI:DG2:MMS:10.RBV').__call__()
    RawData.changeValue(eventIDs = eventIDs,
                        photon_energies=photon_energies,
                        pulse_energies_fee = pulse_energies,
                        low_diode_us=low_diode_us_events,
                        high_diode_us=high_diode_us_events,
                        epix_spectrum=epix_events,
                        xrt_spectrum=xrt_events,
                        avg_epix_2d=np.asarray(epix_roiSum/i),
                        xrt_intensity=np.sum(xrt_events,1),
                        epix_intensity=np.sum(epix_events,1),
                        scan_name=scan_name,
                        epix_roi=epix_roi,xrt_roi=xrt_roi,
                        save_dir=save_dir,
                        ds_string=ds_string,
                        epix_motor=round(epix_motor,5))
    if not os.path.isdir(save_dir + scan_name):
        try:
            os.mkdir(save_dir + scan_name)
        except:
            os.mkdir(save_dir)
            os.mkdir(save_dir + scan_name)

    with open(save_dir + scan_name + '/' + "rawdata.pkl", "wb") as f:
        pickle.dump(RawData, f)

    return RawData

def add_cal_info(raw_data,to_cal_file):
    if not os.path.exists(to_cal_file[0]+to_cal_file[1]+'.pkl'):
        return
    else:
        with open(to_cal_file[0] + to_cal_file[1] +'.pkl', "rb") as f:
            calibration = pickle.load(f)
        if not calibration[9] == raw_data.epix_motor:
            return
        if hasattr(raw_data,'calibration_info'):
            previous_cal = raw_data.calibration_info[5][1]
            raw_data.changeValue(calibration_info=calibration,previous_cal=previous_cal)   
        else: 
            raw_data.changeValue(calibration_info=calibration)
    with open(raw_data.save_dir + raw_data.scan_name + '/' + "rawdata.pkl", "wb") as f:
        pickle.dump(raw_data, f)
        