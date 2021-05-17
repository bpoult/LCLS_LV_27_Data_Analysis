import sys, getopt
import psana as ps
import numpy as np
import h5py
from scipy.interpolate import interp1d
from mpi4py import MPI

def chunk_range(L,N,i):
    if i>=N:
        return range(0,0)
    if L>N:
        chunk_len = int(int(L)/int(N))
        if i==(N-1):
            return range(chunk_len*i,L)
        else:
            return range(chunk_len*(i),chunk_len*(i+1))
    elif L==N:
        return range(i,i+1)
    else:
        if i<L:
            return range(i,i+1)
        else:
            return range(0,0)
        
def data_source_string(loc="cxi", exp_str="x", exp_num="46119", **kwargs):
    exp_name = str(loc)+str(exp_str)+str(exp_num)
    ds = 'exp='+exp_name
    if ('run' in kwargs):
        ds += ':run='+str(kwargs['run'])
    if ('stream' in kwargs):
        ds += ":stream="+str(kwargs['stream'])
    if ('extra' in kwargs):
        ds += ":"+str(kwargs['extra'])
    return (ds,exp_name)


### HARD CODED SHIT FROM ANDY


ePixYMin = 192 + 40
ePixYMax = 293 + 40 #101 pixels
ePixXMin = 80
ePixXMax = 140
ePixSpec = np.zeros(ePixYMax-ePixYMin)
XRTMin = 725 #hard code
XRTMax = 1389
#data collected from runs 110 to 115
keV = [6.990,6.995,7.000,7.005, 7.010,7.015]
epix_loc = [12,25,38,51,64,77]
xrt_loc = [1306,1216,1132,1046,962,876]
m,b = np.polyfit(epix_loc, keV,1) #converts pixel to photon energy m*pixel+b = photon energy
epix_axis = np.arange(ePixYMax-ePixYMin)*m+b
m2,b2 = np.polyfit(xrt_loc, keV, 1)
xrt_axis = m2*np.arange(XRTMin,XRTMax)+b2
XRT_LEN = len(xrt_axis)
EPIX_LEN = len(epix_axis)


def process_xrt_img(img):
    XRTroi = img[XRTMin:XRTMax]
    XRTShotSpec = interp1d(xrt_axis, XRTroi, bounds_error=False, fill_value=0.)(epix_axis)
    return XRTShotSpec

def process_epix_img(img):
    data = np.rint(img/7.0) #convert to photons as ouput is in keV
    data[data<0.0] = 0.0 #remove negative photons (assume they are noise... note should test a bit)
    ePixRoi = data[0,ePixXMin:ePixXMax,ePixYMin:ePixYMax]
    ePixShotSpec = 	np.sum(ePixRoi, axis = 0)
    return ePixShotSpec

def get_epix_img(evt, det_obj):
    return det_obj.calib_data(evt)

def get_xrt_img(evt, det_obj):
    return det_obj.get(evt)



def main(argv):
    #parse args
    Length = None
    try:
        opts, args = getopt.getopt(argv,"hr:a:L:",["run=","angle=","Length="])
    except getopt.GetoptError:
        print('usage: ')
        print('<script> -r <run number> or <script> --run= <run number>')
        print('<script> -L <num shots> or <script> --Length= <num shots>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('Oops.  You entered a script argument wrong.  Usage: ')
            print('<script> -r <run number> or <script> --run= <run number>')
            print('<script> -L <num shots> or <script> --Length= <num shots>')
            sys.exit()
        elif opt in ("-r", "--run"):
            run_num = int(arg)
        elif opt in ("-L", "--Length"):
            Length = int(arg)

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    ds_string, exp_name = data_source_string(loc='cxi',exp_str='x',exp_num='46119',run=run_num,extra='idx')
    ds = ps.DataSource(ds_string)
    print(ds_string)

    EPIX = ps.Detector('epix10k135')
    XRT = ps.Detector('FEE-SPEC0')
    ZPOS = ps.Detector('CXI:BER:MCN:04.RBV')
    run = next(ds.runs())
    t = run.times()
    if Length is None:
        L = len(t)
    elif Length < len(t):
        L = Length
    else:
        L = len(t)
        
    local_chunk = chunk_range(L, size, rank)
    local_xrt = np.zeros((len(local_chunk),EPIX_LEN),dtype=np.float32)
    local_epix = np.zeros((len(local_chunk),EPIX_LEN),dtype=np.float32)
    local_zpos = np.zeros((len(local_chunk),4),dtype=np.float32)
    
    for i,k in enumerate(local_chunk):
        evt = run.event(t[k])
        epix_img = get_epix_img(evt, EPIX)
        if epix_img is None:
            continue
        xrt_img = get_xrt_img(evt, XRT)
        if xrt_img is None:
            continue
        evtId = evt.get(ps.EventId)
        second = float(evtId.time()[0])
        nanosec = float(evtId.time()[1])
        fiducial = float(evtId.fiducials())
        zpos = ZPOS()
        local_zpos[i,:] = np.array([zpos, second, nanosec, fiducial]).astype('float32')
        local_xrt[i,:] = process_xrt_img(xrt_img.hproj()).astype('float32')
        local_epix[i,:] = process_epix_img(epix_img).astype('float32')
        

    comm.Barrier() #block all threads until everyone crosses this line
    xrt_nelems = np.array(comm.gather(local_xrt.size))
    epix_nelems = np.array(comm.gather(local_epix.size))
    zpos_nelems = np.array(comm.gather(local_zpos.size))
    if rank==0:
        collected_xrt = np.empty((L,EPIX_LEN),dtype=np.float32)
        collected_epix = np.empty((L,EPIX_LEN),dtype=np.float32)
        collected_zpos = np.empty((L,4),dtype=np.float32)
    else:
        collected_xrt = None        
        collected_epix = None
        collected_zpos = None
    comm.Gatherv(sendbuf=local_xrt,recvbuf=[collected_xrt,xrt_nelems])
    comm.Gatherv(sendbuf=local_epix,recvbuf=[collected_epix,epix_nelems])
    comm.Gatherv(sendbuf=local_zpos,recvbuf=[collected_zpos,zpos_nelems])

    if rank==0:
        fname = '/reg/d/psdm/cxi/cxix46119/hdf5/smalldata/data/' + exp_name + '_r' + str(run_num) + '.h5'
        with h5py.File(fname,'w') as f:
            f['xrt_spectra'] = collected_xrt
            f['epix_spectra'] = collected_epix
            f['zpos_and_timestamps'] = collected_zpos
            f['epix_axis'] = epix_axis
            f['xrt_axis'] = xrt_axis
    MPI.Finalize()

if __name__ == "__main__":
    main(sys.argv[1:])
