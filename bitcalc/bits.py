from datetime import timedelta
from .time import Duration, scale_rate_to_seconds, SHORT_TO_LONG_TIME_LABELS

# Label mappings
DATA_LABEL_MAP = {
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


class DataUnit:
    """ Parent class for data units """
    value = float()
    label = str()
    label_short = str()
    base = str()
    k_divisor = int()

    def __init__(self, value, label_short, base=None):
        self.base = self.label_to_base(label_short, base=base)
        self.value = value
        self.label = DATA_LABEL_MAP[self.base][label_short]
        self.label_short = label_short
        self.k_divisor = self.base_to_k_divisor(self.base)
        self.prefix = self._get_prefix(self.label)
        self.suffix = self._get_suffix(self.label)
        self.is_bit = self.is_bit(self.label_short)
        self.bits = self._reduce_to_bits()
        self.bytes = self.bits_to_bytes(self.bits)

    def _reduce_to_bits(self):
        if self.prefix is None and self.is_bit:
            # Value is bits already
            return self.value
        elif self.prefix is None and not self.is_bit:
            # Value is bytes, convert to bits and return
            return DataUnit.bytes_to_bits(self.value)
        elif not self.is_bit:
            # Value is bytes, but not plain; convert to bits for processing
            value = DataUnit.bytes_to_bits(self.value)
        else:
            # value is bits, but not plain; save for processing
            value = self.value
        return DataUnit.prefix_to_value(value, self.prefix, self.k_divisor)

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

    @staticmethod
    def label_to_base(label_short, base=None):
        # Handle base for bits and bytes as they're ambiguous
        if base and (label_short == 'b' or label_short == 'B'):
            # base argument may be integer or long-form value
            if base == 2 or base == 'base-2':
                return 'base-2'
            elif base == 10 or base == 'base-10':
                return 'base-10'

        # Value isn't b/B, or base wasn't specified; normal logic
        if label_short in DATA_LABEL_MAP['base-2']:
            return 'base-2'
        elif label_short in DATA_LABEL_MAP['base-10']:
            return 'base-10'

    @staticmethod
    def base_to_k_divisor(base):
        return 2**10 if base == 'base-2' else 10**3


class DataRate(DataUnit):
    """ Representation of data rate """
    def __init__(self, unit, rate=None, timestamp=None, time_label_short='s'):
        super().__init__(unit.value, unit.label_short, base=unit.base)
        self.time_label = SHORT_TO_LONG_TIME_LABELS[time_label_short]
        self.time_label_short = time_label_short
        if rate:
            rate_seconds = scale_rate_to_seconds(
                rate,
                self.time_label_short)
            seconds = self.value / rate_seconds
            delta = timedelta(seconds=seconds)
            self.duration = Duration(delta=delta)
        elif timestamp:
            self.duration = Duration(timestamp=timestamp)
        self.rate = self.value / getattr(self.duration, self.time_label)
