import xarray as xr
import seaborn as sns
import pandas as pd
import bottleneck as bn
from pylab import *
plt.ion()
user='xarray'
#user=os.getlogin() 

"""
# http://xarray.pydata.org
# https://seaborn.pydata.org/
# http://pandas.pydata.org/
#
# see also PyDataSource package
# http://pswww.slac.stanford.edu/swdoc/ana/PyDataSource/
# can be used to create xarray compatable hdf5 datasets with complete metadata
# from these run summaries can be created with the python code necessary to make the plots
# e.g.,
# file:///reg/d/psdm/xpp/xpptut15/stats/summary/run0261/report.html
#

% pylab 

import xarray as xr
import seaborn as sns
import pandas as pd
import bottleneck as bn
user='xarray'

import xarray_examples

x = xarray_examples.open_xarray()
print x

attrs = [a for a in x.data_vars if a.startswith('ebeam') and x[a].dims == ('time',)] + ['gas_detector_f_21_ENRC']
print attrs

df = xarray_examples.describe(x, attrs)
print df

df = xarray_examples.heatmap(x,attrs)
print df

df = xarray_examples.groupby_stats(x, 'ebeam_charge')
print df

plt.figure()
xarray_examples.plot_rolling(x)

# make a scatter plot to show correlation of data  
plt.figure()
attrs = ['gas_detector_f_21_ENRC', 'ebeam_photon_energy', 'ebeam_charge']
xarray_examples.scatter_plot(x, attrs)

# make cuts to ignore outliers and make scatter plot again
xarray_examples.make_cuts(x, attrs)
plt.figure()
xarray_examples.scatter_plot(x, attrs, cut=x.valid_cut)

# plot sum of all epix detector events
plt.figure()
x.epix100a_diff_calib.mean(dim='time').plot()

# use robust keyword to make plot range nic
plt.figure()
x.epix100a_diff_calib.mean(dim='time').plot(robust=True)

# Plot projection vs time specifying axis as alternative to dim
plt.figure()
x.epix100a_diff_calib.mean(axis=1).plot(robust=True)

# Group epix data by event code 141 present and plot.
plt.figure()
da = x.epix100a_diff_calib.groupby('evr_code_141').mean(dim='time')
da.plot(col='evr_code_141', robust=True)

"""

def open_xarray(exp='xpptut15', run=261, user=user):
    """
    Open xarray dataset
    """
    instrument=exp[0:3]
    path='/reg/d/psdm/{:}/{:}/scratch/{:}'.format(instrument, exp, user)
    h5file = '{:}/run{:04}.nc'.format(path,run)
    return xr.open_dataset(h5file, engine='h5netcdf')

def groupby_stats(x, attr='ebeam_photon_energy', drop=False, 
            groupby='evr_code_141', stats=['mean','std','min','max'], dataframe=False):
    """
    Compare stats of attr after groupby another attribute. 
    """
    if drop:
        dag = x[attr].dropna(dim='time').groupby(groupby)
        print "dag = x['{:}'].dropna(dim='time').groupby('{:}')".format(attr, groupby)
    else:
        dag = x[attr].groupby(groupby)
        print "dag = x['{:}'].groupby('{:}')".format(attr, groupby)
    
    if dataframe:
        df = pd.DataFrame({stat: getattr(dag, stat)() for stat in ['mean', 'std', 'min', 'max']})
        print "df = pd.DataFrame({stat: getattr(dag, stat)() for stat in ['mean', 'std', 'min', 'max']})"
        return df
    else:
        da = xr.Dataset({stat: getattr(dag, stat)() for stat in ['mean', 'std', 'min', 'max']})
        print "da = xr.Dataset({stat: getattr(dag, stat)() for stat in ['mean', 'std', 'min', 'max']})"
        return da

def plot_groupby(x, attr='ebeam_photon_energy', groupby='step'):
    """
    Groupby step and plot.
    """
    dag = x[attr].dropna(dim='time').groupby(groupby)
    dag.mean().to_pandas().plot(yerr=dag.std())
    print "dag = x['{:}'].dropna(dim='time').groupby('{:}')".format(attr, groupby)
    print "dag.mean().to_pandas().plot(yerr=dag.std())"


def plot_rolling(x, attr='gas_detector_f_22_ENRC', ntime=100, cut=None):
    """
    Plot gas detector data points with time 
    Then over plot rolling mean with thick grean line
    Rolling method uses bottlneck to speed up calculation
    """
    if cut:
        da = x[attr].where(x[cut]).dropna(dim='time')
        print "da = x['{:}'].where(x['{:}']).dropna(dim='time')".format(attr, cut)
    else:
        da = x[attr]
        print "da = x['{:}']".format(attr)
    print "fig = da.plot(marker='.',linestyle='')"
    print "da.rolling(time={:}).mean().plot(color='g',linewidth=5)".format(ntime)
    fig = da.plot(marker='.',linestyle='')
    da.rolling(time=ntime).mean().plot(color='g',linewidth=5)

def describe(x, attrs, percentiles=[0.05,0.5,0.95]):
    """
    Use pandas describe method to build stats summary table
    """
    return x[attrs].to_dataframe().describe(percentiles=percentiles).T

def make_cuts(x, attrs, name='valid_cut', percentiles=[0.05, 0.95], sigma=2):
    """
    Make cuts on data
    """
    df = x.reset_coords()[attrs].to_dataframe()
    df_tbl = df.describe(percentiles=percentiles).T
    minp = int(min(percentiles)*100)
    maxp = int(max(percentiles)*100)
    dfcut = (df > df_tbl['{:}%'.format(minp)]-sigma*df_tbl['std']).all(axis=1) \
          & (df < df_tbl['{:}%'.format(maxp)]+sigma*df_tbl['std']).all(axis=1)
    x[name] = dfcut
    print "attrs = {:}".format(attrs)
    print "percentiles = {:}".format(percentiles)
    print "sigma = {:}".format(sigma)
    print "df = x.reset_coords()[attrs].to_dataframe()"
    print "df_tbl = df.describe(percentiles=percentiles).T"
    print "minp = int(min(percentiles)*100)"
    print "maxp = int(max(percentiles)*100)"
    print "dfcut = (df > df_tbl['{:}%']-sigma*df_tbl['std']).all(axis=1) & (df < df_tbl['{:}%']+sigma*df_tbl['std']).all(axis=1)".format(minp, maxp)
    print "x['{:}'] = dfcut".format(name)
 
    return dfcut

def heatmap(x, attrs):
    """
    Use pandas and seaborn to make heatmap of correlations.
    """
    corr = x.reset_coords()[attrs].to_dataframe().corr(method='pearson')
    sns.heatmap(corr,annot=True)
    print "corr = x.reset_coords()[attrs].to_dataframe().corr(method='pearson')"
    print "sns.heatmap(corr,annot=True)"
    return corr

def scatter_plot(x, attrs, cut=None):
    """
    Use pandas and seaborn to make a scatter plot.
    """
    if cut is None:
        dfscat = x.reset_coords()[attrs].to_dataframe()
        print "dfscat = x.reset_coords()[attrs].to_dataframe()"
    else:
        dfscat = x[attrs].where(cut, drop=True).reset_coords()[attrs].to_dataframe()
        print "dfscat = x[attrs].where(cut, drop=True).reset_coords()[attrs].to_dataframe()"

    print """
g = sns.PairGrid(dfscat, diag_sharey=False)
g.map_lower(sns.kdeplot, cmap="Blues_d")
g.map_upper(plt.scatter)
g.map_diag(sns.kdeplot, lw=3)
"""
    g = sns.PairGrid(dfscat, diag_sharey=False)
    g.map_lower(sns.kdeplot, cmap="Blues_d")
    g.map_upper(plt.scatter)
    g.map_diag(sns.kdeplot, lw=3)

def get_attrs(x, det=None):
    """
    Helper function to get scalar attributes for an optionally provided detector
    """
    if det:
       attrs = [a for a in x.data_vars if a.startswith(det) and x[a].dims == ('time',)]
    else:
       attrs = [a for a in x.data_vars if x[a].dims == ('time',)]

    return attrs


