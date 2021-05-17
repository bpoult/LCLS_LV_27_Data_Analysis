import psana as ps
import sys 
if len(sys.argv) < 2:
    sys.exit('Please supply a run number')
else:
    run = sys.argv[1]

ds = ps.DataSource('exp=cxix46119:run='+run+':smd')
zMotor = ps.Detector('CXI:BER:MCN:04.RBV')

for nevent, evt in enumerate(ds.events()):
    evtId = evt.get(ps.EventId)
    second = evtId.time()[0]
    nanosec = evtId.time()[1]
    fiducial = evtId.fiducials()
    
    z = zMotor()
    print('seconds: ',second, 'nanoseconds: ',nanosec, 'fiducial: ', fiducial, 'z positions: ' , z)
