import numpy as np
import matplotlib.pyplot as plt
import random
from Ben.reduce_matrix_size import *

high_res = np.arange(-10,10,0.3)
low_res = np.arange(-10,10,0.35)

[X_high,Y_high] = np.meshgrid(high_res,high_res)
[X_low,Y_low] = np.meshgrid(low_res,low_res)

Z_high = np.asarray(X_high*np.exp(-X_high**2 - Y_high**2))
Z_low = np.asarray(X_low*np.exp(-X_low**2 - Y_low**2))

Z_reduced = compress_and_average(Z_high, Z_low.shape)

row_compressor = get_row_compressor(Z_high.shape[0],Z_low.shape[0])
column_compressor = get_column_compressor(Z_high.shape[1],Z_low.shape[1])
plt.figure()
plt.plot(high_res,np.sum(Z_high,0))
plt.plot(low_res,np.sum(Z_low,0))
plt.plot(low_res,np.transpose(np.sum(Z_reduced,0)))