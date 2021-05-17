import psana as ps
import numpy as np
import matplotlib.pyplot as plt
import sys
import h5py

if len(sys.argv) < 2:
	sys.exit('Please supply a run number')
else:
	run = sys.argv[1]


ds = ps.DataSource('exp=cxix46119:run='+run+':smd')
epix = ps.Detector('epix10k135')
wave8 = ps.Detector('CXI-DG3-BMMON')
electronBeam = ps.Detector('EBeam')
fee = ps.Detector('FEEGasDetEnergy')

roiYMin = 170
roiYMax = 330
roiXMin = 80
roiXMax = 140
imageSum = np.zeros([352,384]) # data for summed image
roiSum = np.zeros([roiXMax-roiXMin, roiYMax-roiYMin])
roiSpec = np.zeros(roiYMax-roiYMin)
spec = np.zeros(384)
i = 0
for nevent, evt in enumerate(ds.events()):
	ebeam = electronBeam.get(evt)
	if ebeam is None: continue #skip if no ebeam data
	photonEnergy = ebeam.ebeamPhotonEnergy()

	PulseEnergy = fee.get(evt)
	if PulseEnergy is None: continue
	pulse = PulseEnergy.f_11_ENRC()

	d = wave8.get(evt)
	if d is None: continue
	
	image = epix.calib_data(evt)
	if image is None: continue
	
	keV = photonEnergy/1000.0 #scale photon energy
	data = np.rint(image/keV) #convert to photons
	data[data<0.0] = 0.0 #remove negative photons (assume they are noise... note should test)

	imageSum += data[0,:,:]
	roiSum += data[0,roiXMin:roiXMax,roiYMin:roiYMax]

	diodes = d.peakA()
	lowDiode = -1.0 * diodes[8] * 13.0 #/0.12230 #scale by 50 micron Fe foil transmission at 7 keV
	highDiode = (-1.0* diodes[12]) - lowDiode #sees both pulses

	roiSpec += np.sum(roiSum, axis = 0)#/(-1.0 * diodes[12])
	spec += np.sum(imageSum, axis = 0)#/(-1.0 * diodes[12])
	i += 1
	print(nevent, i)
plt.imshow(roiSum)
plt.show()
plt.plot(roiSpec/i)
plt.show()
np.save('run_'+run+'.npy', roiSpec/i)
