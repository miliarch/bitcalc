import sys
from argparse import ArgumentParser, RawTextHelpFormatter
from .bits import DATA_LABEL_MAP, DataUnit
from .time import Duration

LABELS_B2 = list(DATA_LABEL_MAP['base-2'].keys())
LABELS_B10 = list(DATA_LABEL_MAP['base-10'].keys())


def parse_args():
    """ Parse input arguments provided by user

    Output: Namespace object containing validated argument values
    """

    # Define Parser class with custom error handler
    class Parser(ArgumentParser):
        def error(self, message):
            sys.stderr.write('error: {0}\n'.format(message))
            self.print_help()
            sys.exit(2)

    # Program title and description
    desc = 'Bitcalc - A command line utility for quick conversion and '
    desc += 'comparison of bit/byte values'
    parser = Parser(description=desc, formatter_class=RawTextHelpFormatter)

    # Argument: count (positional, required)
    help_str = 'specify bit/byte count (numeric)'
    parser.add_argument('count', help=help_str, type=float)

    # Argument: label (positional, required)
    help_str = "specify short unit label of count"
    parser.add_argument('label', help=help_str)

    # Argument: target_labels (positional, optional, multiple allowed)
    help_str = 'specify target short unit label conversion target(s)'
    help_str += '\n\n short unit labels:'
    help_str += '\n  ambiguous: [{}] '.format('|'.join(LABELS_B2[:2]))
    help_str += '(handled as base-2 by default)'
    help_str += '\n  base-2: [{}]'.format('|'.join(LABELS_B2[2:]))
    help_str += '\n  base-10: [{}]'.format('|'.join(LABELS_B10[2:]))
    parser.add_argument('target_labels', help=help_str, nargs='*')

    # Argument: -b --base (optional, only effective for b/B)
    help_str = 'specify base for ambiguous unit labels'
    parser.add_argument(
        '-b', '--base',
        help=help_str,
        type=int,
        choices=[2, 10])

    # Argument: -d --duration (optional)
    help_str = 'specify duration for rate conversion (y:w:d:h:m:s)'
    help_str += '\n format examples: [1:30:20|42|3:12:37:15]\n'
    parser.add_argument('-d', '--duration', help=help_str)

    # Argument: -a --alt (optional, only effective for b/B)
    help_str = 'print alternate table (both base-2 and base-10 units)'
    parser.add_argument('-a', '--alt', help=help_str, action='store_true')

    return validate_args(parser.parse_args())


def validate_args(args):
    """ Validate input arguments provided by user; exit conditionally

    Input:
        - args: Namespace object representing collection of arguments:

    Scrutinized arguments:
        - args.label: String containing short unit label of input count
        - args.target_labels: List containing short unit labels for conversion

    Output: The same args namespace object that was input
    """

    # Build list of all valid labels
    all_labels = []
    all_labels.extend(LABELS_B2)
    all_labels.extend(LABELS_B10)

    # Build list of all labels specified in input
    input_labels = []
    input_labels.append(args.label)
    input_labels.extend(args.target_labels)

    # Validate all input_labels exist in all_labels list
    for label in input_labels:
        if label not in all_labels:
            help_str = "Invalid label: {0}".format(label)
            print(help_str)
            sys.exit(2)

    return args


def format_decimal_value(value):
    """ Format number as string, limiting decimal length based on value

    Input:
        - value: Integer or float

    Output: String containing converted value
    """
    if value > 1:
        # Format as 3 point decimal for smaller amounts
        return "{:0.3f}".format(value).rstrip("0").rstrip(".")
    else:
        # Format as 15 point decimal for smaller amounts
        return "{:0.8f}".format(value).rstrip("0").rstrip(".")


def format_table(units, units2=None):
    """ Format table content for eventual command line output

    Input:
        - units: List of DataUnit objects containing values to represent in rows
        - units2: Optional list of units to be used in combination table
                  formatting; length must match len(units)

    Output: Table string used for command line tabular data output
    """
    if not units2:
        # Format table header and add to content string
        header = format_table_row_single('(lbl)', 'Unit Label', 'Value')
        divider = format_table_divider(header)
        content = ''
        content += '{}\n'.format(divider)
        content += '{}\n'.format(header)
        content += '{}\n'.format(divider)

        # Update content string with each target unit
        for unit in units:
            output_str = format_table_row_single(
                '({})'.format(unit.label_short),
                '{}s'.format(unit.label.title()),
                format_decimal_value(unit.value))
            content += '{}\n'.format(output_str)

        # Append divider to end of table
        content += '{}\n'.format(divider)
    else:
        # Format table header and add to content string
        header = format_table_row_combo('Value (base-2)', 'Value (base-10)')
        divider = format_table_divider(header)
        content = ''
        content += '{}\n'.format(divider)
        content += '{}\n'.format(header)
        content += '{}\n'.format(divider)

        # Identify which set of units is base-2 and save to convenience names
        if units[0].base == 'base-2':
            b2_units = units
            b10_units = units2
        else:
            b2_units = units2
            b10_units = units

        # Add each row of unit conversions to content string
        for idx, unit in enumerate(b2_units):
            b2_str = '{v} {ls: <3}'.format(
                v=format_decimal_value(b2_units[idx].value),
                ls=b2_units[idx].label_short)
            b10_str = '{v} {ls: <2}'.format(
                v=format_decimal_value(b10_units[idx].value),
                ls=b10_units[idx].label_short)
            output_str = format_table_row_combo(b2_str, b10_str)
            content += '{}\n'.format(output_str)

        # Append divider to end of table
        content += '{}\n'.format(divider)

    return content


def format_table_divider(scan_str, match_char='|', i_char='+', fill_char='-'):
    """ Format and return a divider for use in table printing

    Input:
        - scan_str: Full string to analyze for character matching
        - match_char: Character that indicates a match
        - i_char: Character to use in match positions
        - fill_char: Character to use in non-match positions

    Output: String to be used as a divider in tabular data output
    """
    i_positions = [idx for idx, c in enumerate(scan_str) if c == match_char]
    divider = ''
    for i in range(len(scan_str)):
        if i in i_positions:
            divider += i_char
        else:
            divider += fill_char
    return divider


def format_table_row_single(lbl, label, value):
    """ Format table row string representing a single value (two cells:
    label, value)

    Input:
        - lbl: Short/abbreviated label string
        - label: Full label string
        - value: Value at specified label (type agnostic)

    Output: String to be used as a row of tabular data output
    """
    return "| {lbl: >5} {label: <12}|{value: >23} |".format(
        lbl=lbl,
        label=label,
        value=value)


def format_table_row_combo(value1, value2):
    """ Format table row string representing multiple values

    Input:
        - value1: Value to use in cell 1 of table row
        - value2: Value to use in cell 2 of table row

    Output: String to be used as a row of tabular data output
    """
    return "| {value1: >23} | {value2: >23} |".format(
        value1=value1,
        value2=value2)


def generate_data_unit_list(base_unit, target_labels):
    """ Generate list of DataUnit objects based on base_unit against target_labels

    Input:
        - base_unit: DataUnit object instance representing input/base value
        - target_labels: Short target labels for building new DataUnit objects

    Output: List of DataUnit objects
    """
    units = []
    for short_label in target_labels:
        # Identify if target label represents bit or byte value
        if DataUnit.is_bit(short_label):
            new_value = base_unit.bits
        else:
            new_value = base_unit.bytes

        # Identify k_divisor based on short_label's base
        k_divisor = DataUnit.base_to_k_divisor(DataUnit.label_to_base(short_label))

        # Instantiate DataUnit object to represent target short_label
        unit = DataUnit(
            DataUnit.value_to_prefix(
                new_value,
                short_label[0].lower(),
                k_divisor),
            short_label)

        # Append DataUnit object to list of units
        units.append(unit)
    return units


def main():
    """ Main entry point for command line invocation """

    # Parse and validate arguments
    args = parse_args()

    # Instantiate input DataUnit object
    data_unit = DataUnit(args.count, args.label, base=args.base)

    # Echo information about input data_unit back to user
    input_value_str = '\nInput value ({base}): {value} {label} ({ls})'.format(
        base=data_unit.base,
        value=format_decimal_value(data_unit.value),
        label='{}s'.format(data_unit.label.title()),
        ls=data_unit.label_short)

    # Format and print conversion data
    output_str = ''
    if args.target_labels and not args.alt:
        data_units = generate_data_unit_list(data_unit, args.target_labels)
        if not args.duration:
            # Format and print table with target data_units based on target labels only
            output_str = '{}\n{}'.format(
                input_value_str,
                format_table(data_units))
        elif args.duration:
            # Select first listed data_unit
            data_unit = data_units[0]

            # Process data
            duration = Duration(timestamp=args.duration)
            rate = data_unit.value / duration.seconds

            # Format and print output
            input_duration_str = 'Input duration: {}'.format(duration.delta)
            rate_str = 'Average {lbl}s per second: {rate} {ls}/s'.format(
                lbl=data_unit.label.title(),
                rate=format_decimal_value(rate),
                ls=data_unit.label_short)
            output_str = '{v}\n{d}\n{r}'.format(
                v=input_value_str,
                d=input_duration_str,
                r=rate_str)
    else:
        if args.alt:
            # Format and print table with all base-2 and base-10 data_units
            b2_data_units = generate_data_unit_list(data_unit, LABELS_B2)
            b10_data_units = generate_data_unit_list(data_unit, LABELS_B10)
            output_str = '{}\n{}'.format(
                input_value_str,
                format_table(b2_data_units, b10_data_units))
        elif data_unit.base == 'base-2':
            # Format and print table with all base-2 data_units
            b2_data_units = generate_data_unit_list(data_unit, LABELS_B2)
            output_str = '{}\n{}'.format(
                input_value_str,
                format_table(b2_data_units))
        elif data_unit.base == 'base-10':
            # Format and print table with all base-10 data_units
            b10_data_units = generate_data_unit_list(data_unit, LABELS_B10)
            output_str = '{}\n{}'.format(
                input_value_str,
                format_table(b10_data_units))
    print(output_str)
