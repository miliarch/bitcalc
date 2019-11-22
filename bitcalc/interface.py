import sys
from argparse import ArgumentParser, RawTextHelpFormatter
from .bits import LABEL_MAP, UnitBase2, UnitBase10

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
    help_str += '\n  ambiguous: [{}] (handled as base-2 by default)'.format(
        '|'.join(LABELS_B2[:2]))
    help_str += '\n  base-2: [{}]'.format(
        '|'.join(LABELS_B2[2:]))
    help_str += '\n  base-10: [{}]'.format(
        '|'.join(LABELS_B10[2:]))
    parser.add_argument('label', help=help_str)

    help_str = 'specify base for ambiguous unit labels'
    help_str += '\n options: [2|10]'
    parser.add_argument('-b', '--base', help=help_str)

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

    # Validate specified label exists in the LABEL_MAP
    all_labels = []
    all_labels.extend(LABELS_B2)
    all_labels.extend(LABELS_B10)
    if args.label not in all_labels:
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

    print(unit.bits)