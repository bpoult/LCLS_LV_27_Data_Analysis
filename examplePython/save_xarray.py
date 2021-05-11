"""
import h5py
import xarray as xr
import numpy as np

# Open h5 file created with
# 
# mpirun -n 8 python mpiDataSource_xarray.py
#

f = h5py.File("/reg/d/psdm/xpp/xpptut15/scratch/xarray/run0261.h5")

# Make xarray Dataset from h5 file
x = xr.Dataset()

d = f.get("XCS_IPM_05_channel")
value = np.array(d.value, np.float32)
x['XCS_IPM_05_channel'] = (('time', 'XCS_IPM_05_channel_x'), value)
x["XCS_IPM_05_channel"].attrs["alias"] = "XCS_IPM_05"

d = f.get("XCS_IPM_05_sum")
value = np.array(d.value, np.float32)
x['XCS_IPM_05_sum'] = (('time'), value)
x["XCS_IPM_05_sum"].attrs["alias"] = "XCS_IPM_05"

d = f.get("XCS_IPM_05_xpos")
value = np.array(d.value, np.float32)
x['XCS_IPM_05_xpos'] = (('time'), value)
x["XCS_IPM_05_xpos"].attrs["alias"] = "XCS_IPM_05"

d = f.get("XCS_IPM_05_ypos")
value = np.array(d.value, np.float32)
x['XCS_IPM_05_ypos'] = (('time'), value)
x["XCS_IPM_05_ypos"].attrs["alias"] = "XCS_IPM_05"

d = f.get("XCS_IPM_gon_channel")
value = np.array(d.value, np.float32)
x['XCS_IPM_gon_channel'] = (('time', 'XCS_IPM_gon_channel_x'), value)
x["XCS_IPM_gon_channel"].attrs["alias"] = "XCS_IPM_gon"

d = f.get("cspad2x2_diff_calib")
value = np.array(d.value, np.float32)
x['cspad2x2_diff_calib'] = (('time', 'cspad2x2_diff_calib+_sensor', 'cspad2x2_diff_calib_row', 'cspad2x2_diff_calib_column'), value)
x["cspad2x2_diff_calib"].attrs["alias"] = "cspad2x2_diff"

d = f.get("ebeam")
value = np.array(d.get("L3_energy").value, np.float32)
x['ebeam_L3_energy'] = (('time'), value)
x["ebeam_L3_energy".attrs["alias"] = "ebeam"
value = np.array(d.get("charge").value, np.float32)
x['ebeam_charge'] = (('time'), value)
x["ebeam_charge".attrs["alias"] = "ebeam"
value = np.array(d.get("dump_charge").value, np.float32)
x['ebeam_dump_charge'] = (('time'), value)
x["ebeam_dump_charge".attrs["alias"] = "ebeam"
value = np.array(d.get("photon_energy").value, np.float32)
x['ebeam_photon_energy'] = (('time'), value)
x["ebeam_photon_energy".attrs["alias"] = "ebeam"
value = np.array(d.get("pk_curr_bc2").value, np.float32)
x['ebeam_pk_curr_bc2'] = (('time'), value)
x["ebeam_pk_curr_bc2".attrs["alias"] = "ebeam"

d = f.get("epix100a_diff_calib")
value = np.array(d.value, np.float32)
x['epix100a_diff_calib'] = (('time', 'epix100a_diff_calib_y', 'epix100a_diff_calib_x'), value)
x["epix100a_diff_calib"].attrs["alias"] = "epix100a_diff"

d = f.get("event_time")
value = d.value
x['event_time'] = (('time'), value)
x["event_time"].attrs["alias"] = "event"

d = f.get("evr")
value = np.array(d.get("code_140").value, np.bool)
x['evr_code_140'] = (('time'), value)
x["evr_code_140".attrs["alias"] = "evr"
value = np.array(d.get("code_141").value, np.bool)
x['evr_code_141'] = (('time'), value)
x["evr_code_141".attrs["alias"] = "evr"
value = np.array(d.get("code_142").value, np.bool)
x['evr_code_142'] = (('time'), value)
x["evr_code_142".attrs["alias"] = "evr"
value = np.array(d.get("code_143").value, np.bool)
x['evr_code_143'] = (('time'), value)
x["evr_code_143".attrs["alias"] = "evr"
value = np.array(d.get("code_144").value, np.bool)
x['evr_code_144'] = (('time'), value)
x["evr_code_144".attrs["alias"] = "evr"
value = np.array(d.get("code_145").value, np.bool)
x['evr_code_145'] = (('time'), value)
x["evr_code_145".attrs["alias"] = "evr"
value = np.array(d.get("code_146").value, np.bool)
x['evr_code_146'] = (('time'), value)
x["evr_code_146".attrs["alias"] = "evr"
value = np.array(d.get("code_150").value, np.bool)
x['evr_code_150'] = (('time'), value)
x["evr_code_150".attrs["alias"] = "evr"
value = np.array(d.get("code_162").value, np.bool)
x['evr_code_162'] = (('time'), value)
x["evr_code_162".attrs["alias"] = "evr"
value = np.array(d.get("code_164").value, np.bool)
x['evr_code_164'] = (('time'), value)
x["evr_code_164".attrs["alias"] = "evr"
value = np.array(d.get("code_40").value, np.bool)
x['evr_code_40'] = (('time'), value)
x["evr_code_40".attrs["alias"] = "evr"
value = np.array(d.get("code_41").value, np.bool)
x['evr_code_41'] = (('time'), value)
x["evr_code_41".attrs["alias"] = "evr"
value = np.array(d.get("code_42").value, np.bool)
x['evr_code_42'] = (('time'), value)
x["evr_code_42".attrs["alias"] = "evr"
value = np.array(d.get("code_43").value, np.bool)
x['evr_code_43'] = (('time'), value)
x["evr_code_43".attrs["alias"] = "evr"
value = np.array(d.get("code_44").value, np.bool)
x['evr_code_44'] = (('time'), value)
x["evr_code_44".attrs["alias"] = "evr"
value = np.array(d.get("code_45").value, np.bool)
x['evr_code_45'] = (('time'), value)
x["evr_code_45".attrs["alias"] = "evr"
value = np.array(d.get("code_46").value, np.bool)
x['evr_code_46'] = (('time'), value)
x["evr_code_46".attrs["alias"] = "evr"
value = np.array(d.get("code_83").value, np.bool)
x['evr_code_83'] = (('time'), value)
x["evr_code_83".attrs["alias"] = "evr"
value = np.array(d.get("code_84").value, np.bool)
x['evr_code_84'] = (('time'), value)
x["evr_code_84".attrs["alias"] = "evr"
value = np.array(d.get("code_85").value, np.bool)
x['evr_code_85'] = (('time'), value)
x["evr_code_85".attrs["alias"] = "evr"
value = np.array(d.get("code_86").value, np.bool)
x['evr_code_86'] = (('time'), value)
x["evr_code_86".attrs["alias"] = "evr"
value = np.array(d.get("code_87").value, np.bool)
x['evr_code_87'] = (('time'), value)
x["evr_code_87".attrs["alias"] = "evr"
value = np.array(d.get("code_88").value, np.bool)
x['evr_code_88'] = (('time'), value)
x["evr_code_88".attrs["alias"] = "evr"
value = np.array(d.get("code_89").value, np.bool)
x['evr_code_89'] = (('time'), value)
x["evr_code_89".attrs["alias"] = "evr"

d = f.get("fiducials")
value = d.value
x['fiducials'] = (('time'), value)
x["fiducials"].attrs["alias"] = ""

d = f.get("gas_detector")
value = np.array(d.get("f_11_ENRC").value, np.float32)
x['gas_detector_f_11_ENRC'] = (('time'), value)
x["gas_detector_f_11_ENRC".attrs["alias"] = "gas_detector"
value = np.array(d.get("f_12_ENRC").value, np.float32)
x['gas_detector_f_12_ENRC'] = (('time'), value)
x["gas_detector_f_12_ENRC".attrs["alias"] = "gas_detector"
value = np.array(d.get("f_21_ENRC").value, np.float32)
x['gas_detector_f_21_ENRC'] = (('time'), value)
x["gas_detector_f_21_ENRC".attrs["alias"] = "gas_detector"
value = np.array(d.get("f_22_ENRC").value, np.float32)
x['gas_detector_f_22_ENRC'] = (('time'), value)
x["gas_detector_f_22_ENRC".attrs["alias"] = "gas_detector"
value = np.array(d.get("f_63_ENRC").value, np.float32)
x['gas_detector_f_63_ENRC'] = (('time'), value)
x["gas_detector_f_63_ENRC".attrs["alias"] = "gas_detector"
value = np.array(d.get("f_64_ENRC").value, np.float32)
x['gas_detector_f_64_ENRC'] = (('time'), value)
x["gas_detector_f_64_ENRC".attrs["alias"] = "gas_detector"

d = f.get("phase_cav")
value = np.array(d.get("charge1").value, np.float32)
x['phase_cav_charge1'] = (('time'), value)
x["phase_cav_charge1".attrs["alias"] = "phase_cav"
value = np.array(d.get("charge2").value, np.float32)
x['phase_cav_charge2'] = (('time'), value)
x["phase_cav_charge2".attrs["alias"] = "phase_cav"
value = np.array(d.get("fit_time_1").value, np.float32)
x['phase_cav_fit_time_1'] = (('time'), value)
x["phase_cav_fit_time_1".attrs["alias"] = "phase_cav"
value = np.array(d.get("fit_time_2").value, np.float32)
x['phase_cav_fit_time_2'] = (('time'), value)
x["phase_cav_fit_time_2".attrs["alias"] = "phase_cav"
x.coords['ievent'] = x.time
x['time'] = (x.event_time - x.event_time.values[0])/1.e9
x.coords['step'] = (x.time.diff(dim='time') > 0.1).cumsum(dim='time')
x.step[0] = 0
x['cspad2x2_diff_count'] = x.cspad2x2_diff_calib.astype(np.float64).mean(axis=(1,2,3))
x['cspad2x2_diff_count'].attrs = x.cspad2x2_diff_calib.attrs
x['cspad2x2_diff_count'].attrs['doc'] = 'Count of x.cspad2x2_diff_calib'
x['epix100a_diff_count'] = x.epix100a_diff_calib.astype(np.float64).mean(axis=(1,2))
x['epix100a_diff_count'].attrs = x.epix100a_diff_calib.attrs
x['epix100a_diff_count'].attrs['doc'] = 'Count of epix100a_diff_calib'

# set xarray coordinates
x = x.set_coords(['evr_code_140', 'evr_code_141', 'evr_code_142', 'evr_code_143', 'evr_code_144', 'evr_code_145', 'evr_code_146', 'evr_code_150', 'evr_code_162', 'evr_code_164', 'evr_code_40', 'evr_code_41', 'evr_code_42', 'evr_code_43', 'evr_code_44', 'evr_code_45', 'evr_code_46', 'evr_code_83', 'evr_code_84', 'evr_code_85', 'evr_code_86', 'evr_code_87', 'evr_code_88', 'evr_code_89', 'fiducials', 'event_time'])


# Add attributes
x.attrs['run'] = run
x.attrs['exp'] = exp
x.attrs['h5file'] = file_name
x.ebeam_photon_energy.attrs['unit'] = 'eV'
x.ebeam_charge.attrs['unit'] = 'nC'
x.ebeam_dump_charge.attrs['unit'] = '-e'
x.ebeam_L3_energy.attrs['unit'] = 'MeV'


# Save xarray Dataset to file with netcdf4 convention
x.to_netcdf('/reg/d/psdm/xpp/xpptut15/scratch/xarray/run0261.nc', engine='h5netcdf')

f.close()

"""

import os
import h5py
import xarray as xr
import numpy as np
exp='xpptut15'
run=261
#user=os.getlogin() 
user='xarray'

def convert(exp=exp, run=run, user=user):
    print 'import h5py'
    print 'import xarray as xr'
    print 'import numpy as np'
    print '''
# Open h5 file created with
# 
# mpirun -n 8 python mpiDataSource_xarray.py
#
'''
    
    instrument=exp[0:3]
    path='/reg/d/psdm/{:}/{:}/scratch/{:}'.format(instrument, exp, user)
    file_name = '{:}/run{:04}.h5'.format(path,run)
    f = h5py.File(file_name)
    x = xr.Dataset()
    print 'f = h5py.File("{:}")'.format(file_name)
    print ''
    print '# Make xarray Dataset from h5 file' 
    print 'x = xr.Dataset()'
    for key in f.keys():
        print ''
        d = f.get(key)
        print 'd = f.get("{:}")'.format(key)
        typ = d.__class__.__module__.split('.')[2]
        if typ == 'dataset':
            ndims = len(d.shape)
            attr = key
            value = d.value
            if ndims > 1:
                value = np.array(value, np.float32)
                print 'value = np.array(d.value, np.float32)'
            elif value.dtype == np.float64:
                value = np.array(value, np.float32)
                print 'value = np.array(d.value, np.float32)'
            else:
                print 'value = d.value'

            add_attr(x, attr, value)
            alias = '_'.join(key.split('_')[:-1])
            x[attr].attrs['alias'] = alias
            print 'x["{:}"].attrs["alias"] = "{:}"'.format(attr, alias)
       
        elif typ == 'group':
            for name in d.keys():
                item = d.get(name)
                ndims = len(item.shape)
                attr = '_'.join(item.name.split('/')[1:])
                value = item.value
                if ndims > 1:
                    value = np.array(value, np.float32)
                    print 'value = np.array(d.get("{:}").value, np.float32)'.format(name)
                elif attr.startswith('evr_code'):
                    value = np.array(value, np.bool)
                    print 'value = np.array(d.get("{:}").value, np.bool)'.format(name)
                elif value.dtype == np.float64:
                    value = np.array(value, np.float32)
                    print 'value = np.array(d.get("{:}").value, np.float32)'.format(name)
                else:
                    print 'value = d.get("{:}").value'.format(name)

                add_attr(x, attr, value)
                x[attr].attrs['alias'] = key
                print 'x["{:}".attrs["alias"] = "{:}"'.format(attr, key)

    x.coords['ievent'] = x.time
    x['time'] = (x.event_time - x.event_time.values[0])/1.e9
    x.coords['step'] = (x.time.diff(dim='time') > 0.1).cumsum(dim='time')
    x.step[0] = 0
    print "x.coords['ievent'] = x.time"
    print "x['time'] = (x.event_time - x.event_time.values[0])/1.e9"
    print "x.coords['step'] = (x.time.diff(dim='time') > 0.1).cumsum(dim='time')"
    print "x.step[0] = 0"
    
    if 'cspad2x2_diff_calib' in x:
        x['cspad2x2_diff_count'] = x.cspad2x2_diff_calib.astype(np.float64).mean(axis=(1,2,3))
        x['cspad2x2_diff_count'].attrs = x.cspad2x2_diff_calib.attrs
        x['cspad2x2_diff_count'].attrs['doc'] = 'Count of x.cspad2x2_diff_calib'
        print "x['cspad2x2_diff_count'] = x.cspad2x2_diff_calib.astype(np.float64).mean(axis=(1,2,3))"
        print "x['cspad2x2_diff_count'].attrs = x.cspad2x2_diff_calib.attrs"
        print "x['cspad2x2_diff_count'].attrs['doc'] = 'Count of x.cspad2x2_diff_calib'"

    if 'epix100a_diff_calib' in x: 
        x['epix100a_diff_count'] = x.epix100a_diff_calib.astype(np.float64).mean(axis=(1,2))
        x['epix100a_diff_count'].attrs = x.epix100a_diff_calib.attrs
        x['epix100a_diff_count'].attrs['doc'] = 'Count of epix100a_diff_calib'
        print "x['epix100a_diff_count'] = x.epix100a_diff_calib.astype(np.float64).mean(axis=(1,2))"
        print "x['epix100a_diff_count'].attrs = x.epix100a_diff_calib.attrs"
        print "x['epix100a_diff_count'].attrs['doc'] = 'Count of epix100a_diff_calib'"

    attrs = [str(a) for a in x if a.startswith('evr_code') and x[a].dims == ('time',)]
    attrs += ['fiducials', 'event_time']
    x = x.set_coords(attrs)
    print ''
    print "# set xarray coordinates"
    print "x = x.set_coords({:})".format(attrs)

    print ''
    print """
# Add attributes
x.attrs['run'] = run
x.attrs['exp'] = exp
x.attrs['h5file'] = file_name
x.ebeam_photon_energy.attrs['unit'] = 'eV'
x.ebeam_charge.attrs['unit'] = 'nC'
x.ebeam_dump_charge.attrs['unit'] = '-e'
x.ebeam_L3_energy.attrs['unit'] = 'MeV'
"""

    x.attrs['run'] = run
    x.attrs['exp'] = exp
    x.attrs['h5file'] = file_name
    x.ebeam_photon_energy.attrs['unit'] = 'eV'
    x.ebeam_charge.attrs['unit'] = 'nC'
    x.ebeam_dump_charge.attrs['unit'] = '-e'
    x.ebeam_L3_energy.attrs['unit'] = 'MeV'

    file_out = '{:}/run{:04}.nc'.format(path,run)
    x.to_netcdf(file_out, engine='h5netcdf')
    print ''
    print '# Save xarray Dataset to file with netcdf4 convention' 
    print "x.to_netcdf('{:}', engine='h5netcdf')".format(file_out)

    f.close()
    print ''
    print 'f.close()'

    return x

def add_attr(x, attr, value):
        ndims = len(value.shape)
        if ndims == 1:
            print "x['{:}'] = (('time'), value)".format(attr)
            x[attr] = (('time'), value)
        
        elif ndims == 2:
            print "x['{:}'] = (('time', '{:}_x'), value)".format(attr, attr)
            x[attr] = (('time', attr+'_item'), value)
        
        elif ndims == 3:
            print "x['{:}'] = (('time', '{:}_y', '{:}_x'), value)".format(attr, attr, attr)
            x[attr] = (('time', attr+'_y', attr+'_x'), value)
        
        elif ndims == 4:
            print "x['{:}'] = (('time', '{:}+_sensor', '{:}_row', '{:}_column'), value)".format(attr, attr, attr, attr)
            x[attr] = (('time', attr+'_sensor', attr+'_row', attr+'_column'), value)


