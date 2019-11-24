import sys
from argparse import ArgumentParser, RawTextHelpFormatter
from .bits import LABEL_MAP, Unit

LABELS_B2 = list(LABEL_MAP['base-2'].keys())
LABELS_B10 = list(LABEL_MAP['base-10'].keys())


def parse_args():
    """ Parse passed arguments and return as Namespace object """
    # Found this bit posted by unutbu here: http://stackoverflow.com/a/4042861
    class Parser(ArgumentParser):
        def error(self, message):
            sys.stderr.write('error: {0}\n'.format(message))
            self.print_help()
            sys.exit(2)

    # Set and define description
    desc = 'Bitcalc - The future'
    parser = Parser(description=desc, formatter_class=RawTextHelpFormatter)

    help_str = 'specify bit/byte count'
    parser.add_argument('count', help=help_str)

    help_str = 'specify short unit label'
    parser.add_argument('label', help=help_str)

    help_str = 'specify target short unit conversion label(s)'
    help_str += '\n\n short unit labels:'
    help_str += '\n  ambiguous: [{}] (handled as base-2 by default)'.format(
        '|'.join(LABELS_B2[:2]))
    help_str += '\n  base-2: [{}]'.format(
        '|'.join(LABELS_B2[2:]))
    help_str += '\n  base-10: [{}]'.format(
        '|'.join(LABELS_B10[2:]))
    parser.add_argument('target_labels', help=help_str, nargs='*')

    help_str = 'specify base for ambiguous unit labels'
    help_str += '\n options: [2|10]'
    parser.add_argument('-b', '--base', help=help_str)

    help_str = 'print alternate table (combo base-2 and base-10 values)'
    parser.add_argument('-a', '--alt', help=help_str, action='store_true')

    return validate_args(parser.parse_args())


def validate_args(args):
    # Check if count and base are castable as numbers
    try:
        args.count = float(args.count)
    except ValueError:
        help_str = 'Count must be a number'
        print(help_str)
        sys.exit(2)

    if args.base:
        try:
            args.base = int(args.base)
        except ValueError:
            help_str = 'Base must be an integer'
            print(help_str)
            sys.exit(2)

    # Validate specified labels exist in the LABEL_MAP
    all_labels = []
    all_labels.extend(LABELS_B2)
    all_labels.extend(LABELS_B10)
    input_labels = []
    input_labels.append(args.label)
    input_labels.extend(args.target_labels)
    for label in input_labels:
        if label not in all_labels:
            help_str = "Invalid label: {0}".format(args.label)
            print(help_str)
            sys.exit(2)

    # Set input_type for simplified use in later logic
    if args.label in LABELS_B2:
        label = LABEL_MAP['base-2'][args.label]
    else:
        label = LABEL_MAP['base-10'][args.label]

    # Check if base passed as arg, continue only if true and type is bit/byte
    if args.base and (label == 'bit' or label == 'byte'):
        # Validate base specification, only 2 and 10 are valid
        if args.base != 2 and args.base != 10:
            usage_str = 'Base specification must be 2 or 10'
            print(usage_str)
            sys.exit(2)

    return args


def format_decimal_value(value):
    if value > 1:
        # Format as 3 point decimal for smaller amounts
        return "{:0.3f}".format(value).rstrip("0").rstrip(".")
    else:
        # Format as 15 point decimal for smaller amounts
        return "{:0.8f}".format(value).rstrip("0").rstrip(".")


def format_table(units, units2=None):
    """ Print conversion table based on bit_value to console """
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
    """ Format and return a divider for use in table printing - check the
    scan_str for all instances of the match_char, log the positions, generate
    divider with i_char in match positions, fill_char in non-match positions
    """
    i_positions = [idx for idx, s in enumerate(scan_str) if s == match_char]
    divider = ''
    for i in range(len(scan_str)):
        if i in i_positions:
            divider += i_char
        else:
            divider += fill_char
    return divider


def format_table_row_single(lbl, label, value):
    return "| {lbl: >5} {label: <12}|{value: >23} |".format(
        lbl=lbl,
        label=label,
        value=value)


def format_table_row_combo(value1, value2):
    return "| {value1: >23} | {value2: >23} |".format(
        value1=value1,
        value2=value2)


def generate_unit_list(base_unit, target_labels):
    units = []
    if target_labels:
        for short_label in target_labels:
            if Unit.is_bit(short_label):
                new_value = base_unit.bits
            else:
                new_value = base_unit.bytes
            k_divisor = Unit.base_to_k_divisor(Unit.label_to_base(short_label))
            unit = Unit(
                base_unit.value_to_prefix(
                    new_value,
                    short_label[0].lower(),
                    k_divisor),
                short_label)
            units.append(unit)
    return units


def main():
    # Parse and validate arguments
    args = parse_args()

    # Instantiate input unit object
    unit = Unit(args.count, args.label, base=args.base)

    # Print input data
    input_value_str = '\nInput value ({base}): {value} {label} ({ls})'.format(
        base=unit.base,
        value=format_decimal_value(unit.value),
        label='{}s'.format(unit.label.title()),
        ls=unit.label_short)
    print(input_value_str)

    # Print conversion data
    if args.target_labels and not args.alt:
        units = generate_unit_list(unit, args.target_labels)
        print(format_table(units))
    else:
        if args.alt:
            b2_units = generate_unit_list(unit, LABELS_B2)
            b10_units = generate_unit_list(unit, LABELS_B10)
            print(format_table(b2_units, b10_units))
        elif unit.base == 'base-2':
            b2_units = generate_unit_list(unit, LABELS_B2)
            print(format_table(b2_units))
        elif unit.base == 'base-10':
            b10_units = generate_unit_list(unit, LABELS_B10)
            print(format_table(b10_units))
