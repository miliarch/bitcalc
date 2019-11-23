import sys
from argparse import ArgumentParser, RawTextHelpFormatter
from .bits import LABEL_MAP, UnitBase2, UnitBase10, Unit

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

    help_str = 'specify target short unit label to convert to'
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

    help_str = 'print alternate table (base-2 and base-10 tables)'
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
    else:
        # Check label, if bit/byte, notify user binary/base-2 will be used
        if label == 'bit' or label == 'byte':
            usage_str = ('{0}s specified with no base, using base-2'.format(
                label.title()))
            print(usage_str)

    return args


def format_decimal_value(value):
    if value > 1:
        # Format as 3 point decimal for smaller amounts
        return "{:0.3f}".format(value).rstrip("0").rstrip(".")
    else:
        # Format as 15 point decimal for smaller amounts
        return "{:0.8f}".format(value).rstrip("0").rstrip(".")


def format_table(units):
    """ Print conversion table based on bit_value to console """
    header = format_table_line('lbl', 'Unit Label', 'Value ({})'.format(
        units[0].base))
    divider = format_table_divider(header)
    content = ''
    content += '{}\n'.format(divider)
    content += '{}\n'.format(header)
    content += '{}\n'.format(divider)

    for unit in units:
        output_str = format_table_line(
            unit.label_short,
            unit.label,
            format_decimal_value(unit.value))
        content += '{}\n'.format(output_str)
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


def format_table_line(lbl, label, value):
    return "| {lbl: >5} {label: <12}|{value: >23} |".format(
        lbl='({})'.format(lbl),
        label=label,
        value=value)


def generate_unit_list(base_unit, target_labels):
    units = []
    if target_labels:
        for short_label in target_labels:
            if Unit.is_bit(short_label):
                new_value = base_unit.bits
            else:
                new_value = base_unit.bytes
            unit = UnitBase2(
                base_unit.value_to_prefix(
                    new_value,
                    short_label[0].lower(),
                    base_unit.k_divisor),
                short_label)
            units.append(unit)
    return units


def main():
    # Parse and validate arguments
    args = parse_args()

    # Instantiate input unit object
    if args.base == 2 or (args.base is None and args.label in LABELS_B2):
        # Base 2
        unit = UnitBase2(args.count, args.label)
    else:
        # Base 10
        unit = UnitBase10(args.count, args.label)

    if args.target_labels:
        presentation_units = generate_unit_list(unit, args.target_labels)
    else:
        presentation_units = generate_unit_list(unit, LABELS_B2)

    print(format_table(presentation_units))
