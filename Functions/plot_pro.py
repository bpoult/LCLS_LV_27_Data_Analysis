# Written by Ben Poulter (Khalil Group, University of Washington), May 2021
# For LV27 LCLS Beamtime.

import matplotlib.pyplot as plt
import os
import sys
import numpy as np
import psana as ps
import pickle


def check_SN(pro_data,plot_on):

    epix = pro_data.epix_windowed
    xrt = pro_data.xrt_based
    resid = np.subtract(epix,xrt)
    if plot_on:
        resid_rand = resid[np.random.choice(resid.shape[0], np.int64(epix.shape[0]), replace=False)]
        loop_over = np.append(np.arange(100,len(resid),100,dtype=int),len(resid))
        plt.figure()
        for i in loop_over:
            plt.scatter(i,np.std(np.mean(resid_rand[0:i],0)),1.5,c='k')
        plt.xlabel('# shots in avg')
        plt.ylabel('STD of residual')
        plt.title('Shot Noise for ' +str(epix.shape[0])+' total shots')
        plt.show()
    return resid