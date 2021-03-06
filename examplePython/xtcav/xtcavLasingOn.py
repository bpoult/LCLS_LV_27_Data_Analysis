from psana import *

from xtcav.ShotToShotCharacterization import *
ds=DataSource('exp=xpptut15:run=302:smd')
XTCAVRetrieval=ShotToShotCharacterization();
XTCAVRetrieval.SetEnv(ds.env())

import matplotlib.pyplot as plt

ngood = 0
for evt in ds.events():
    if not XTCAVRetrieval.SetCurrentEvent(evt): continue
    time,power,ok=XTCAVRetrieval.XRayPower()  
    if not ok: continue
    agreement,ok=XTCAVRetrieval.ReconstructionAgreement()
    if not ok: continue
    ngood += 1
    # time and power are lists, with each entry corresponding to
    # a bunch number.  The number of bunches is set by the GLOC.nb
    # parameter in the lasing-off analysis.  In general, one should
    # also cut on the "agreement" value, which measures the agreement
    # between the first and second moment analysis (larger is better).
    plt.plot(time[0],power[0])
    plt.xlabel('Time (fs)')
    plt.ylabel('Lasing Power (GW)')
    plt.title('Agreement %4.2f'%agreement)
    plt.show()
    if ngood>1: break
