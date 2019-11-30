from collections import OrderedDict
from datetime import timedelta

TIME_UNITS_TO_SECONDS = OrderedDict([
    ('seconds', 1),
    ('minutes', 60),
    ('hours', 60**2),
    ('days', 24 * 60**2),
    ('weeks', 7 * 24 * 60**2),
    ('years', 52 * 7 * 24 * 60**2)
])


class Duration:
    def __init__(self, timestamp=None, delta=None):
        if delta:
            timestamp = '{d}:0:0:{s}'.format(d=delta.days, s=delta.seconds)

        self.seconds = self.timestamp_to_seconds(timestamp)
        self.minutes = self.seconds / TIME_UNITS_TO_SECONDS['minutes']
        self.hours = self.seconds / TIME_UNITS_TO_SECONDS['hours']
        self.days = self.seconds / TIME_UNITS_TO_SECONDS['days']
        self.weeks = self.seconds / TIME_UNITS_TO_SECONDS['weeks']
        self.years = self.seconds / TIME_UNITS_TO_SECONDS['years']
        self.delta = timedelta(seconds=self.seconds)

    @staticmethod
    def timestamp_to_units_list(timestamp):
        """ Split timestamp to list

        Input:
            - timestamp: String of colon delimited time values (y:w:d:h:m:s)

        Output: List of ints representing input timestamp
        """
        try:
            return [int(t) for t in timestamp.split(sep=':')]
        except ValueError:
            raise

    @staticmethod
    def units_to_dict(time_units):
        """ Generate dictionary of labeled time_units

        Input:
            - time_units: List of ints representing timestamp ([y, w, d, h, m, s])

        Output: Dictionary of unit: value representing input timestamp
        """
        time_units_dict = {}
        for label in TIME_UNITS_TO_SECONDS:
            if time_units:
                # Save last value in list with current label as key
                time_units_dict[label] = time_units.pop()

        return time_units_dict

    @staticmethod
    def units_to_seconds(time_units_dict):
        """ Reduce time unit dict values to seconds and return summed value

        Input:
            - time_units_dict: Dictionary of time unit labels to values

        Output: Sum of seconds (int)
        """
        seconds_list = []
        for key in time_units_dict:
            seconds_list.append(
                time_units_dict[key] * TIME_UNITS_TO_SECONDS[key])
        return sum(seconds_list)

    @staticmethod
    def timestamp_to_seconds(timestamp):
        """ Process timestamp string to get sum of seconds

        Input:
            - timestamp: String of colon delimited time values (y:w:d:h:m:s)

        Output: Sum of seconds (int)
        """
        units_list = Duration.timestamp_to_units_list(timestamp)
        units_dict = Duration.units_to_dict(units_list)
        return Duration.units_to_seconds(units_dict)
