#!/usr/bin/env python3
''' Python Bit Calculator (bitcalc.py)
Inspired by Matisse's Bit Calculator - http://www.matisse.net/bitcalc
Units conform to Ubuntu Units Policy - https://wiki.ubuntu.com/UnitsPolicy
'''
import sys
from getopt import getopt, GetoptError

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

for idx,unit in enumerate(b2_units):
    unit_table[b2_units_s[idx]] = unit

for idx,unit in enumerate(b10_units):
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


def get_args():
    """ Import command line arguments, return dictionary of passed args """
    argv = sys.argv[1:]

    try:
        opts, args = getopt(argv, "a:b:ht:", ["amount=", "base=", "help", "type="])
    except GetoptError:
        usage()

    arg_dict = {}

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit(2)
        elif opt in ("-a", "--amount"):
            try:
                arg_dict['value'] = float(arg)
            except(TypeError, ValueError):
                print("Amount (-a, --amount) must be a number, try again.")
                usage()
        elif opt in ("-b", "--base"):
            try:
                arg_dict['base'] = int(arg)
            except(TypeError, ValueError):
                print("Base (-b, --base) must be a number, try again.")
                usage()
        elif opt in ("-t", "--type"):
            arg_dict['type'] = arg

    return arg_dict


def print_table(bit_value):
    """ Print conversion table based on bit_value to console """
    table_values = []
    base_2 = True if mod_s == b2 else False

    # Define and print header string
    header = "Unit Type\t\tValue"
    print(header)

    for idx,unit in enumerate(units):
        if idx == 0:
            # Append base bit value to table_values list
            table_values.append(bit_value);
        elif idx == 1:
            # Append base byte value to table_values list
            table_values.append(bit_value / mod_d)
        else:
            # Modify value for previous like type (bit/byte), append to list
            table_values.append(table_values[idx - 2] / mod_s)
        
        if table_values[idx] > 1:
            # Format float as 3 point decimal for larger amounts
            pretty_val = "{:0.3f}".format(table_values[idx]).rstrip("0").rstrip(".")
        else:
            # Format float as 15 point decimal for smaller amounts
            pretty_val = "{:0.15f}".format(table_values[idx]).rstrip("0").rstrip(".")
        
        # Set unit labels for long and short labels
        unit_long = unit.title()

        if len(units_s[idx]) == 1:
            # Adjust short unit label alignment if b or B (insert spaces)
            unit_short = "  " + units_s[idx] if base_2 else " " + units_s[idx]
        else:
            unit_short = units_s[idx]

        # Define and print output string
        output_str = ("{short} - {unit}s\t\t{val}".format(
                unit=unit_long, short=unit_short, val=pretty_val
                )
            )
        print(output_str)
        
    print()

def usage():
    """ Print usage information to console """
    print("-t for type, -b for value")
    sys.exit(2)


def update_mod_s(value):
    """ Update mod_s global to specified value """
    global mod_s
    mod_s = value

def validate_args(arg_dict):
    # Check if arguments have been passed
    type_exists = True if 'type' in arg_dict else False
    base_exists = True if 'base' in arg_dict else False

    # Check if type passed as arg, continue if true
    if type_exists:
        # Validate specified type exists in the unit_table
        if arg_dict['type'] not in unit_table:
            print("Invalid type {0}, check usage.".format(arg_dict['type']))
            usage()
    else:
        # TODO: Establish default type if no type present
        # Provide usage if type is not present
        print("No type provided, check usage.")
        usage()

    # Set input_type for simplified use in later logic
    input_type = unit_table[arg_dict['type']]

    # Check if base passed as arg, continue only if true and type is bit/byte
    if base_exists and (input_type == 'bit' or input_type == 'byte'):
        # Validate base specification, only 2 and 10 are valid
        if arg_dict['base'] != 2 and arg_dict['base'] != 10:
            print('Base specification must be 2 or 10, check usage.')
            usage()
        # Update mod_s to binary/base-2 if specified
        elif arg_dict['base'] == 2:
            update_mod_s(b2)
        # Update mod_s to decimal/base-10 if specified
        elif arg_dict['base'] == 10:
            update_mod_s(b10)
    else:
        # Check input_type, if bit/byte, notify user binary/base-2 will be used 
        if input_type == 'bit' or input_type == 'byte':
            usage_str = ('{0}s selected, no base specified, using binary mode (base-2).'
                '\nRun again and specify -b 10 or --base 10 for base-10.\n'
                ''.format(input_type.title()))
            print(usage_str)
        # Check input_type, update mod_s to decimal/base-10 if not "bi" type
        elif 'bib' not in input_type:
            update_mod_s(b10)


def main():
    # Import arguments
    arg_dict = get_args()

    # Validate arguments
    validate_args(arg_dict)

    # Create global vars to hold selected units
    global units, units_s

    # Set units based on current mod_s value
    units = b2_units if mod_s == b2 else b10_units
    units_s = b2_units_s if mod_s == b2 else b10_units_s

    # Store arguments for further use
    input_value = arg_dict['value']
    input_type = unit_table[arg_dict['type']]

    # Convert input value to bits
    bit_value = convert_to_bits(input_type, input_value)

    # Print conversion table
    print_table(bit_value)


if __name__ == "__main__":
    main()
