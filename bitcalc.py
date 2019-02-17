#!/usr/bin/env python3
''' Python Bit Calculator (pybitcalc)
Inspired by Matisse's Bit Calculator - http://www.matisse.net/bitcalc
Units conform to Ubuntu Units Policy - https://wiki.ubuntu.com/UnitsPolicy

License: MIT License, Copyright (c) 2016-2019 Marcus Bowman
Version: 1.1
'''
import sys
from argparse import ArgumentParser, RawTextHelpFormatter

# Set IEC (base-2) and SI (base-10) values - should be considered constant
b2 = 1024
b10 = 1000

# Type prefixes, used for conversion to base bits/bytes
prefixes = ['ki', 'me', 'gi', 'te', 'pe']

# List of base-2 unit labels
b2_units = [
    'bit', 'byte',
    'kibibit', 'kibibyte',
    'mebibit', 'mebibyte',
    'gibibit', 'gibibyte',
    'tebibit', 'tebibyte',
    'pebibit', 'pebibyte',
]

# List of short base_2 unit labels
b2_units_s = [
    'b', 'B',
    'Kib', 'KiB',
    'Mib', 'MiB',
    'Gib', 'GiB',
    'Tib', 'TiB',
    'Pib', 'PiB',
]

# List of base-10 unit labels
b10_units = [
    'bit', 'byte',
    'kilobit', 'kilobyte',
    'megabit', 'megabyte',
    'gigabit', 'gigabyte',
    'terabit', 'terabyte',
    'petabit', 'petabyte',
]

# List of short base_10 unit labels
b10_units_s = [
    'b', 'B',
    'kb', 'kB',
    'Mb', 'MB',
    'Gb', 'GB',
    'Tb', 'TB',
    'Pb', 'PB',
]

# Create and populate dictionary for short to long unit mapping (all bases)
unit_table = {}

for idx, unit in enumerate(b2_units):
    unit_table[b2_units_s[idx]] = unit

for idx, unit in enumerate(b10_units):
    unit_table[b10_units_s[idx]] = unit

# Modify Similar - Number of bytes in kilobyte, b2 (1024) by default
mod_s = b2

# Modify Disparate - Number of bits in byte
mod_d = 8


def convert_to_bits(input_type, input_value):
    """ Import type and value of input, return value in bits """
    # Check if value is a bit or byte value
    is_bit = True if units[0] in input_type else False

    # If value is byte, convert to bit
    if not is_bit:
        input_value *= mod_d

    # Check prefix and convert to bits accordingly
    for prefix in prefixes:
        # Do nothing unless prefix is found in input_type string
        if prefix in input_type[:2]:
            # Convert from kilo
            if prefix == prefixes[0]:
                input_value *= mod_s
            # Convert from mega
            elif prefix == prefixes[1]:
                input_value *= pow(mod_s, 2)
            # Convert from giga
            elif prefix == prefixes[2]:
                input_value *= pow(mod_s, 3)
            # Convert from tera
            elif prefix == prefixes[3]:
                input_value *= pow(mod_s, 4)
            # Convert from peta
            elif prefix == prefixes[4]:
                input_value *= pow(mod_s, 5)

    return input_value


def format_divider(scan_str, match_char='|', i_char='+', fill_char='-'):
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


def format_output(lbl, label, value):
    return "| {lbl: >5} {label: <12}|{value: >23} |".format(
        lbl='({})'.format(lbl),
        label=label,
        value=value)


def parse_args():
    """ Parse passed arguments and return as Namespace object """
    # Found this bit posted by unutbu here: http://stackoverflow.com/a/4042861
    class Parser(ArgumentParser):
        def error(self, message):
            sys.stderr.write('error: {0}\n'.format(message))
            self.print_help()
            sys.exit(2)

    # Set and define description
    desc = 'A simple program for printing a conversion '
    desc += 'table of bit and byte values for a given input value'
    parser = Parser(description=desc, formatter_class=RawTextHelpFormatter)

    help_str = 'specify bit/byte amount'
    parser.add_argument('amount', help=help_str)

    help_str = 'specify bit/byte type as short unit label - valid options:'
    help_str += '\n  ambiguous: [{}] (handled as base-2 by default)'.format(
        '|'.join(b2_units_s[:2]))
    help_str += '\n  base-2: [{}]'.format('|'.join(b2_units_s[2:]))
    help_str += '\n  base-10: [{}]'.format('|'.join(b10_units_s[2:]))
    help_str += '\n'
    parser.add_argument('type', help=help_str)

    help_str = 'specify base for ambiguous unit labels - valid options: [2|10]'
    help_str += ''
    parser.add_argument('-b', '--base', help=help_str)

    return parser.parse_args()


def print_table(bit_value):
    """ Print conversion table based on bit_value to console """
    table_values = []
    if mod_s == b2:
        base = 'base-2'
    else:
        base = 'base-10'
    header = format_output('lbl', 'Unit Label', 'Value ({})'.format(base))
    divider = format_divider(header)
    print(divider)
    print(header)
    print(divider)

    for idx, unit in enumerate(units):
        if idx == 0:
            # Append base bit value to table_values list
            table_values.append(bit_value)
        elif idx == 1:
            # Append base byte value to table_values list
            table_values.append(bit_value / mod_d)
        else:
            # Modify value for previous like type (bit/byte), append to list
            table_values.append(table_values[idx - 2] / mod_s)

        if table_values[idx] > 1:
            # Format float as 3 point decimal for larger amounts
            pretty_val = "{:0.3f}".format(
                table_values[idx]).rstrip("0").rstrip(".")
        else:
            # Format float as 15 point decimal for smaller amounts
            pretty_val = "{:0.15f}".format(
                table_values[idx]).rstrip("0").rstrip(".")

        # Set unit labels for long and short labels
        unit_long = unit.title()
        unit_short = units_s[idx]

        # Define and print output string
        output_str = format_output(unit_short, unit_long + 's', pretty_val)
        print(output_str)
    print(divider)


def update_mod_s(value):
    """ Update mod_s global to specified value """
    global mod_s
    mod_s = value


def validate_args(args):
    # Cast amount and base (if present) as integer
    try:
        args.amount = float(args.amount)
    except ValueError:
        help_str = 'Amount must be a number'
        print(help_str)
        sys.exit(2)

    if args.base:
        try:
            args.base = int(args.base)
        except ValueError:
            help_str = 'Base must be a number'
            print(help_str)
            sys.exit(2)

    # Validate specified type exists in the unit_table
    if args.type not in unit_table:
        help_str = "Invalid type: {0}".format(args.type)
        print(help_str)
        sys.exit(2)

    # Set input_type for simplified use in later logic
    input_type = unit_table[args.type]

    # Check if base passed as arg, continue only if true and type is bit/byte
    if args.base and (input_type == 'bit' or input_type == 'byte'):
        # Validate base specification, only 2 and 10 are valid
        if args.base != 2 and args.base != 10:
            usage_str = 'Base specification must be 2 or 10'
            print(usage_str)
            sys.exit(2)
        # Update mod_s to binary/base-2 if specified
        elif args.base == 2:
            update_mod_s(b2)
        # Update mod_s to decimal/base-10 if specified
        elif args.base == 10:
            update_mod_s(b10)
    else:
        # Check input_type, if bit/byte, notify user binary/base-2 will be used
        if input_type == 'bit' or input_type == 'byte':
            usage_str = ('{0}s selected, no base specified, using base-2.'
                         '\nRun again with -b 10 or --base 10 for base-10.\n'
                         ''.format(input_type.title()))
            print(usage_str)
        # Check input_type, update mod_s to decimal/base-10 if not "bi" type
        elif 'bib' not in input_type:
            update_mod_s(b10)

    return args


def main():
    # Import and validate arguments
    args = parse_args()
    args = validate_args(args)

    # Create global vars to hold selected units
    global units, units_s

    # Set units based on current mod_s value
    units = b2_units if mod_s == b2 else b10_units
    units_s = b2_units_s if mod_s == b2 else b10_units_s

    # Convert input value to bits
    bit_value = convert_to_bits(unit_table[args.type], args.amount)

    # Print input value
    input_value_str = 'Input value: {value} {lbl}'.format(
        value=args.amount,
        lbl=args.type)
    print(input_value_str)

    # Print conversion table
    print_table(bit_value)


if __name__ == "__main__":
    main()
