


class processed_data_class:
    _defaults = ('eventIDs',
                'high_diode_us',
                'low_diode_us',
                'xrt_intensity',
                'epix_intensity',
                'scan_name',
                'epix_motor',
                'save_dir',
                'calibration_info',
                'previous_cal',
                'epix_energy_windowed',
                'epix_windowed',
                'xrt_energy_windowed',
                'xrt_windowed',
                'xrt_red_res',
                'filters')

    _default_value = None

    def __init__(self, **kwargs):
        self.__dict__.update(dict.fromkeys(self._defaults, self._default_value))
        self.__dict__.update(kwargs)

    def changeValue(self, **kwargs):
        self.__dict__.update(kwargs)

    def getKeys(self):
        return self.__dict__.keys()







