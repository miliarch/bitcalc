from collections import OrderedDict

UNITS_TO_SECONDS_MULTIPLIER = OrderedDict([
    ('seconds', 1),
    ('minutes', 60),
    ('hours', 60**2),
    ('days', 24 * 60**2),
    ('weeks', 7 * 24 * 60**2),
    ('years', 52 * 7 * 24 * 60**2)
])


def timestamp_to_time_units(timestamp):
    """ Split timestamp to list

    Input:
        - timestamp: String of colon delimited time values (y:w:d:h:m:s)

    Output: List of ints representing input timestamp
    """
    try:
        return [int(t) for t in timestamp.split(sep=':')]
    except ValueError:
        raise


def time_units_to_dict(time_units):
    """ Generate dictionary of labeled time time_units

    Input:
        - time_units: List of ints representing timestamp ([y, w, d, h, m, s])

    Output: List of integers representing input timestamp
    """
    time_units_dict = {}
    for label in UNITS_TO_SECONDS_MULTIPLIER:
        if time_units:
            # Save last value in list with current label as key
            time_units_dict[label] = time_units.pop()

    return time_units_dict


def reduce_to_seconds(time_units_dict):
    """ Reduce time unit dict values to seconds and return summed value

    Input:
        - time_units_dict: Dictionary of time unit labels to values

    Output: Sum of seconds (int)
    """
    seconds_list = []
    for key in time_units_dict:
        seconds_list.append(
            time_units_dict[key] * UNITS_TO_SECONDS_MULTIPLIER[key])
    return sum(seconds_list)


def timestamp_to_seconds(timestamp):
    """ Process timestamp string to get sum of seconds

    Input:
        - timestamp: String of colon delimited time values (y:w:d:h:m:s)

    Output: Sum of seconds (int)
    """
    time_units = timestamp_to_time_units(timestamp)
    time_units_dict = time_units_to_dict(time_units)
    return reduce_to_seconds(time_units_dict)
