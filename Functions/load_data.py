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
    pulse_intensities = []
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
        pulse_intensities.append(fee_evt.f_11_ENRC())
        low_diode_us_events.append(low_diode_us_evt)
        high_diode_us_events.append(high_diode_us_evt)
        epix_events.append(np.sum(np.squeeze(epix_data), 0))
        xrt_events.append(xrt_evt.hproj()[XRTMin:XRTMax])
        i += 1
    elapsed_time = (time.time() - start)
    print('Data loaded in ' + str(np.round(elapsed_time, 1)) + ' seconds.')
    print(str(nevent - i) + ' out of ' + str(nevent) + ' shots had empty values.')
    eventIDs = np.asarray(eventIDs)
    photon_energies = np.asarray(photon_energies)
    pulse_intensities = np.asarray(pulse_intensities)
    low_diode_us_events = np.asarray(low_diode_us_events)
    high_diode_us_events = np.asarray(high_diode_us_events)
    epix_events = np.asarray(epix_events)
    xrt_events = np.asarray(xrt_events)

    RawData.changeValue(eventIDS = eventIDs, photon_energies=photon_energies,I0_fee = pulse_intensities,
                         low_diode_us=low_diode_us_events,high_diode_us=high_diode_us_events, epix_spectrum=epix_events,
                         xrt_spectrum=xrt_events,avg_epix_2d=np.asarray(epix_roiSum/i),xrt_intensity=np.sum(xrt_events,1),
                         epix_intensity=np.sum(epix_events,1),scan_name=scan_name,epix_roi=epix_roi,xrt_roi=xrt_roi,
                        save_dir=save_dir,ds_string=ds_string)

    if not os.path.isdir(save_dir + scan_name):
        try:
            os.mkdir(save_dir + scan_name)
        except:
            os.mkdir(save_dir)
            os.mkdir(save_dir + scan_name)

    with open(save_dir + scan_name + '/' + "rawdata.pkl", "wb") as f:
        pickle.dump(RawData, f)

    return RawData
