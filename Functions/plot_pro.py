# Written by Ben Poulter (Khalil Group, University of Washington), May 2021
# For LV27 LCLS Beamtime.

import matplotlib.pyplot as plt
import os
import sys
import numpy as np
import psana as ps
import pickle
import random


def check_SN(pro_data,plot_on,fraction):
    if plot_on:
        number_shots = pro_data.eventIDs.shape[0]
        random_xrt = random.sample(pro_data.xrt_based,number_shots/fraction)
        random_epix = random.sample(pro_data.epix_windowed,number_shots/fraction)

        resid_array = []
        scatter_val =[]
        for i in range(0,len(random_epix)):
            resid = abs(random_epix[i]-random_xrt[i])
            resid_array.append(resid)
            scatter_val.append(np.sum(np.mean(resid_array[0:i+1],0)))
        plt.figure()
        plt.scatter(range(0,len(random_epix)),scatter_val)
        plt.xlabel('# shots in avg')
        plt.ylabel('Sum of averaged residuals')
        plt.title('S/N estimation')
        plt.show()
    return