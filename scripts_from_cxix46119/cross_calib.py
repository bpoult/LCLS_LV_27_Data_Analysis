import psana as ps
import numpy as np
import matplotlib.pyplot as plt
import sys


def minimal_rms_difference(x,y):
	"""
	args: x and y are vectors with shape (N,) and (N,), where N is the number of pixels per shot
	"""
	xaug = np.stack([x,np.ones_like(x)],-1)
	z = np.linalg.lstsq(xaug,y[:,None],rcond=None)[0]
	xScaled = xaug @ z 
	diff = np.squeeze(xaug @ z - y[:,None],-1)
	return xScaled, np.sqrt(np.mean(diff**2))



if len(sys.argv) < 2:
	sys.exit('Please supply a run number')
else:
	run = sys.argv[1]


ePixYMin = 192
ePixYMax = 293 #100 pixels
ePixXMin = 80
ePixXMax = 140
#ePixSum = np.zeros([ePixXMax-ePixXMin, ePixYMax-ePixYMin])
ePixSpec = np.zeros(ePixYMax-ePixYMin)
XRTMin = 725 #hard code
XRTMax = 1389
#data collected from runs 110 to 115
keV = [6.990,6.995,7.000,7.005, 7.010,7.015]
epix_loc = [12,25,38,51,64,77]
xrt_loc = [1306,1216,1132,1046,962,876]
m,b = np.polyfit(epix_loc, keV,1) #converts pixel to photon energy m*pixel+b = photon energy
specBins = np.arange(101)*m+b
m2,b2 = np.polyfit(xrt_loc, keV, 1)
XRTBinMap = np.digitize(m2*np.arange(XRTMin,XRTMax)+b2, m*np.arange(100)+b)
XRTSpecSum = np.zeros(101)

saclingFactor= np.array([0.61267234, 0.61192014, 0.52556952, 0.62836552, 0.51506395,
       0.56560294, 0.61779851, 0.47910407, 0.53389795, 0.48886262,
       0.57916102, 0.56955877, 0.67836004, 0.8402622 , 0.71570191,
       0.80473815, 0.73448521, 0.72574981, 0.85374149, 0.78548235,
       0.82916105, 0.73123882, 0.77133502, 0.93017954, 0.76877141,
       0.94227047, 0.84980386, 0.85232781, 0.96989022, 0.83950811,
       0.99347067, 0.86278467, 0.94161836, 0.8401351 , 0.85981156,
       0.99383003, 0.84630155, 1.        , 0.80821647, 0.7994699 ,
       0.94927662, 0.7985246 , 0.89549207, 0.76751772, 0.7840017 ,
       0.915676  , 0.73807643, 0.86960072, 0.77942932, 0.91795256,
       0.73699036, 0.75140738, 0.89992646, 0.75817684, 0.8347983 ,
       0.70427961, 0.64994903, 0.78217784, 0.69916102, 0.81742916,
       0.67450447, 0.67634881, 0.78851408, 0.66438318, 0.77599554,
       0.65830784, 0.66893555, 0.74220471, 0.6279756 , 0.77663808,
       0.62343641, 0.75592951, 0.61417982, 0.62966456, 0.68717199,
       0.61442937, 0.65402111, 0.64730217, 0.75025975, 0.79664558,
       0.64207048, 0.73153138, 0.61899056, 0.6073008 , 0.68303569,
       0.55992355, 0.6215416 , 0.53165928, 0.51104229, 0.48048335,
       0.52648141, 0.60638083, 0.50890528, 0.60623351, 0.48748342,
       0.49460639, 0.56049269, 0.47743731, 0.56588401, 0.51817187,
       0.60472137])

# scale factor found by running 
# scale = XRTSpecSum.max()/ePixSpec.max()
#s = ePixSpec*scale/XRTSpecSum
# s = s/s.max() 
# on run 116 (2000 events)

#xrt 17 pixels/eV
#epix 2.6 pixels/eV
xrtSum = np.zeros(2048)

ds = ps.DataSource('exp=cxix46119:run='+run+':smd')
epix = ps.Detector('epix10k135')

XRT = ps.Detector('FEE-SPEC0')

z = ps.Detector('CXI:BER:MCN:04.RBV')

i = 0
for nevent, evt in enumerate(ds.events()):
	
	image = epix.calib_data(evt)
	if image is None: continue

	x = XRT.get(evt)
	if x is None: continue
	xrtSpec = x.hproj()

	data = np.rint(image/7.0) #convert to photons as ouput is in keV
	data[data<0.0] = 0.0 #remove negative photons (assume they are noise... note should test a bit)

	
	ePixRoi = data[0,ePixXMin:ePixXMax,ePixYMin:ePixYMax]
	ePixShotSpec = 	np.sum(ePixRoi, axis = 0)
	ePixSpec += ePixShotSpec

	XRTroi = xrtSpec[XRTMin:XRTMax]
	XRTShotSpec = np.zeros(101)
	for idx, val in enumerate(XRTroi):
		XRTSpecSum[XRTBinMap[idx]] += val 
		XRTShotSpec[XRTBinMap[idx]] += val 


	XRTShotSpec = XRTShotSpec * saclingFactor
	XRTShotSpec, RMS = minimal_rms_difference(XRTShotSpec,ePixShotSpec)
#	scale =XRTShotSpec[25:75].sum()/ePixShotSpec[25:75].sum()
#	XRTShotSpec = XRTShotSpec/scale
#	plt.plot(specBins,ePixShotSpec)
#	plt.plot(specBins,XRTShotSpec)
#	RMS = np.sqrt(np.sum((XRTShotSpec - ePixShotSpec)**2)/101)
	print(nevent, RMS)
#	plt.show()
	i +=1
#	if nevent > 10000: break


XRTSpecSum = XRTSpecSum * saclingFactor
#scale = XRTSpecSum.sum()/ePixSpec.sum()
XRTSpecSum, RMS = minimal_rms_difference(XRTSpecSum,ePixSpec)
plt.plot(specBins,XRTSpecSum )
plt.plot(specBins,ePixSpec )
plt.show()
	
