# ssh daq-cxi-mon08
# source /reg/g/psdm/sw/conda1/manage/bin/psconda.sh -py3

import psana as ps
import numpy as np
import time
from psmon import publish
from psmon.plots import Image
from epics import caget, caput

ps.setOption('psana.calib-dir', '/reg/d/psdm/cxi/cxix46119/calib')
#ps.setOption('psana.calib-dir', '/cds/home/opr/cxiopr/calib')
ds = ps.DataSource('shmem=psana.0:stop=no')
epix = ps.Detector('epix10k135')
wave8 = ps.Detector('CXI-DG3-BMMON')
electronBeam = ps.Detector('EBeam')

imageSum = np.zeros([1,352,384])

publish.local = True
publish.plot_opts.aspect = 1

lastupdate = 0
for nevent, evt in enumerate(ds.events()):
    evtId = evt.get(ps.EventId)
    second = evtId.time()[0]
    nanosec = evtId.time()[1]
    fiducial = evtId.fiducials()
    
    d = wave8.get(evt)
    if d is None:
        print ('*** no wave8')
        continue

    diodes = d.peakA()
    lowDiode = -1.0 * diodes[8] * 13.0 #/0.12230 #scale by 50 micron Fe foil transmission at 7 keV
    highDiode = (-1.0* diodes[12]) - lowDiode #sees both pulses    
    #print([second,nanosec,fiducial,lowDiode,highDiode])
    caput('CXI:ACR:HIST:BERGMANN', [second,nanosec,fiducial,lowDiode,highDiode])

    ebeam = electronBeam.get(evt)
    if ebeam is None: continue #skip if no ebeam data
    photonEnergy = ebeam.ebeamPhotonEnergy()

    image = epix.calib_data(evt)
    keV = photonEnergy/1000.0 #scale photon energy
    data = np.rint(image/keV) #convert to photons
    data[data<0.0] = 0.0 #remove negative photons (assume they are noise... note should test)
    imageSum += data
    if nevent % 10 == 0:
        print ('event', nevent)
    if image is None:
        print ('*** no detector image')
        continue

    
    if time.time() - lastupdate >= 1:
        lastupdate = time.time()
        imgsend = Image(nevent, "epix10k135", imageSum)
        publish.send('sum', imgsend)
        print(diodes[8], diodes[12], lowDiode, highDiode)
