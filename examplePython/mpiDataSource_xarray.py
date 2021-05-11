from psana import *
import sys, os

"""
example of creating hdf5 data set that will be convered to xarray compatable h5 convention

For 8 core mpi processing:

mpirun -n 8 python mpiDataSource_xarray.py
"""

exp='xpptut15'
instrument=exp[0:3]
run=261
user=os.getlogin() 
if user == 'koglin':
    user = 'xarray'
gather_interval=100
path='/reg/d/psdm/{:}/{:}/scratch/{:}'.format(instrument, exp, user)
if not os.path.isdir(path):
    os.mkdir(path)

data_source = 'exp={:}:run={:}:smd'.format(exp,run)
print 'Opening {:}'.format(data_source)
dsource = MPIDataSource(data_source)

nmax=200

# Dictionary of detector attributes to save
dattrs   = {'cspad2x2_diff':   ['calib'],
            'epix100a_diff':   ['calib'], 
            'XCS-IPM-gon':     ['channel'],
            'XCS-IPM-05':      ['channel', 'sum', 'xpos', 'ypos'],
            }

# Dictionary of psana Detector objects
adets = {}
for alias in dattrs:
    try: 
        adets[alias] = Detector(alias)
    except:
        print alias, 'Not Valid'

file_name = '{:}/run{:04}.h5'.format(path,run)
print 'Opening {:}'.format(file_name)
smldata = dsource.small_data(file_name, gather_interval=gather_interval)

for nevt,evt in enumerate(dsource.events()):

    adata = {}
    for alias, det in adets.items():
        for attr in dattrs[alias]:
            try:
                if hasattr(det, attr):
                    data = getattr(det, attr)(evt)
                else:
                    data = getattr(det.get(evt), attr)()
                
                if data is not None:
                    name = alias.replace('-','_')+'_'+attr
                    adata[name] = data
            
            except:
                print 'Error getting', nevt, alias, attr    
    
    smldata.event(**adata)

    if nevt % 100 == 0:
        print 'Event', nevt 
 
    if nevt>nmax: 
        break

# save HDF5 file
print 'Saving {:}'.format(file_name)
smldata.save()


