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


def convert_bytes_to_bits(byte_value):
    """ Convert input bytes to bits """
    return byte_value * 8


def convert_bits_to_bytes(bit_value):
    """ Convert input bits to bytes """
    return bit_value / 8


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
        self.bits = self._get_bit_value(
            self.value,
            self.prefix,
            self.suffix,
            self.k_divisor)

    @staticmethod
    def _get_bit_value(value, prefix, suffix, k_divisor):
        if prefix is None and suffix == 'bit':
            # Value is bits already
            return value
        elif prefix is None and suffix == 'byte':
            # Value is bytes
            return value * 8
        elif suffix == 'byte':
            # Value is bytes, but not plain; convert to bit for processing
            value *= 8

        prefix_to_power = {
            'kibi': 1, 'kilo': 1,
            'mebi': 2, 'mega': 2,
            'gibi': 3, 'giga': 3,
            'tebi': 4, 'tera': 4,
            'pebi': 5, 'peta': 5
        }

        return int(value * pow(k_divisor, prefix_to_power[prefix]))

    @staticmethod
    def _get_prefix(label):
        if len(label) <= 4:
            return None
        else:
            return label[:label.rfind('b')]

    @staticmethod
    def _get_suffix(label):
        return label[label.rfind('b'):]


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
