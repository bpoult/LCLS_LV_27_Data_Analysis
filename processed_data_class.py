


class processed_data_class:
    _defaults = ("RIXS_map_pumped", "RIXS_map_unpumped",
                 "FilterParameters", "Energy", "TFY_on", "TFY_off")

    _default_value = None

    def __init__(self, **kwargs):
        self.__dict__.update(dict.fromkeys(self._defaults, self._default_value))
        self.__dict__.update(kwargs)

    def changeValue(self, **kwargs):
        self.__dict__.update(kwargs)

    def getKeys(self):
        return self.__dict__.keys()







