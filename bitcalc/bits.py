# Label mappings
LABEL_MAP = {
    'base-2': {
        'b': 'bit',
        'B': 'byte',
        'Kib': 'kibibit',
        'KiB': 'kibibyte',
        'Mib': 'mebibit',
        'MiB': 'mebibyte',
        'Gib': 'gibibit',
        'GiB': 'gibibyte',
        'Tib': 'tebibit',
        'TiB': 'tebibyte',
        'Pib': 'pebibit',
        'PiB': 'pebibyte',
    },
    'base-10': {
        'b': 'bit',
        'B': 'byte',
        'kb': 'kilobit',
        'kB': 'kilobyte',
        'Mb': 'megabit',
        'MB': 'megabyte',
        'Gb': 'gigabit',
        'GB': 'gigabyte',
        'Tb': 'terabit',
        'TB': 'terabyte',
        'Pb': 'petabit',
        'PB': 'petabyte'
    }
}

PREFIX_TO_POWER = {
    'b': 0,
    'k': 1,
    'm': 2,
    'g': 3,
    't': 4,
    'p': 5
}


class Unit:
    """ Parent class for units """
    value = float()
    label = str()
    label_short = str()
    base = str()
    k_divisor = int()

    def __init__(self):
        self.prefix = self._get_prefix(self.label)
        self.suffix = self._get_suffix(self.label)
        self.is_bit = self.is_bit(self.label_short)
        self.bits = self._get_bit_value()
        self.bytes = self.bits_to_bytes(self.bits)

    def _get_bit_value(self):
        if self.prefix is None and self.is_bit:
            # Value is bits already
            return self.value
        elif self.prefix is None and not self.is_bit:
            # Value is bytes
            return Unit.bytes_to_bits(self.value)
        elif not self.is_bit:
            # Value is bytes, but not plain; convert to bits and save
            value = Unit.bytes_to_bits(self.value)
        else:
            # value is bits, set it and move on
            value = self.value
        return Unit.prefix_to_value(value, self.prefix, self.k_divisor)

    @staticmethod
    def _get_prefix(label):
        if len(label) <= 4:
            return None
        else:
            return label[:label.rfind('b')]

    @staticmethod
    def _get_suffix(label):
        return label[label.rfind('b'):]

    @staticmethod
    def value_to_prefix(value, prefix, k_divisor):
        return value / pow(k_divisor, PREFIX_TO_POWER[prefix[0]])

    @staticmethod
    def prefix_to_value(value, prefix, k_divisor):
        return value * pow(k_divisor, PREFIX_TO_POWER[prefix[0]])

    @staticmethod
    def bits_to_bytes(value):
        return value / 8

    @staticmethod
    def bytes_to_bits(value):
        return value * 8

    @staticmethod
    def is_bit(label_short):
        return True if label_short[-1] == 'b' else False


class UnitBase2(Unit):
    def __init__(self, value, label_short):
        self.base = 'base-2'
        self.value = value
        self.label = LABEL_MAP[self.base][label_short]
        self.label_short = label_short
        self.k_divisor = 2**10
        super().__init__()


class UnitBase10(Unit):
    def __init__(self, value, label_short):
        self.base = 'base-10'
        self.value = value
        self.label = LABEL_MAP[self.base][label_short]
        self.label_short = label_short
        self.k_divisor = 10**3
        super().__init__()
