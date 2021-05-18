# Written by Ben Poulter for LCLS run 19, LV 27.


class RawData:
    _defaults = ['eventIDs',
                 'photon_energies',
                 'I0_fee',
                 'high_diode_us',
                 'low_diode_us',
                 'epix_spectrum',
                 'xrt_spectrum',
                 'avg_epix_2d',
                 'xrt_intensity',
                 'epix_intensity']

    _default_value = None

    def __init__(self, **kwargs):
        self.__dict__.update(dict.fromkeys(self._defaults, self._default_value))
        self.__dict__.update(kwargs)

    def changeValue(self, **kwargs):
        self.__dict__.update(kwargs)

    def getKeys(self):
        return self.__dict__.keys()