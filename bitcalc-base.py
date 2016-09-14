#!/usr/bin/env python3
import sys
from getopt import getopt, GetoptError

# Lists of prefixes (long and short)
prefixes = ["kilo", "mega", "giga", "tera", "peta"]
prefixes_s = ["K", "M", "G", "T", "P"]

# Lists of units (long and short)
units = ["bit", "byte"]
units_s = ["b", "B"]

# Dictionary for short to long unit mapping
unit_table = {}

# Populate long form unit list
for prefix in prefixes:
    units.append(prefix + units[0])
    units.append(prefix + units[1])

# Populate short form unit list
for prefix_s in prefixes_s:
    units_s.append(prefix_s + units_s[0])
    units_s.append(prefix_s + units_s[1])

# Populate unit_table (eg. "Kb": "kilobit")
for idx,unit in enumerate(units):
    unit_table[units_s[idx]] = unit

# Modify Similar - Number of bytes in kilobyte (SI = 1000, Binary = 1024)
mod_s = 1024 

# Modify Disparate - Number of bits in a byte
mod_d = 8

def convert_to_bits(input_type, input_value):
    # Check if value is a bit or byte value
    is_bit = True if units[0] in input_type else False

    # If value is byte, convert to bit
    if not is_bit:
        input_value *= mod_d

    # Check prefix and convert to bits accordingly    
    for prefix in prefixes:
        # Do nothing unless prefix is found in input_type string
        if prefix in input_type:
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
    argv = sys.argv[1:]

    try:
        opts, args = getopt(argv, "b:ht:", ["help", "type="])
    except GetoptError:
        usage()

    arg_dict = {}

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit(2)
        elif opt == "-b":
            try:
                arg_dict['input_value'] = float(arg)
            except(TypeError):
                print("Value must be a number, try again.")
                usage()
        elif opt == "-t":
            arg_dict['input_type'] = arg

    return arg_dict


def print_table(bit_value, type_index):
    table_values = []
    
    # Define and print header string
    header = " Unit Type\t\tValue"
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
        
        # Format float value as 15 point decimal, drop 0s after decimal
        pretty_val = "{:0.15f}".format(table_values[idx]).rstrip("0").rstrip(".")
        
        # Set unit labes for long and short labels
        unit_long = unit.title()
        unit_short = " " + units_s[idx] if len(units_s[idx]) == 1 else units_s[idx]

        # Define and print output string
        output_str = (" {short} - {unit}s\t\t{val}".format(
                unit=unit_long, short=unit_short, val=pretty_val
                )
            )
        print(output_str)
        
    print()

def usage():
    print("-t for type, -b for value")
    sys.exit(2)


def validate_args(arg_dict):
    type_exists = True if 'input_type' in arg_dict else False

    if type_exists:
        if arg_dict['input_type'] in unit_table:
            input_type = unit_table[arg_dict['input_type']]
        else:
            print("Invalid type, check usage.")
            usage()
    else:
        print("No type provided, check usage.")
        usage()


def main():
    arg_dict = get_args()

    # Validate provided arguments
    validate_args(arg_dict)

    input_value = arg_dict['input_value']
    input_type = unit_table[arg_dict['input_type']]
    input_type_index = units.index(input_type)

    # Convert input value to bits
    bit_value = convert_to_bits(input_type, input_value)

    # Print conversion table
    print_table(bit_value, input_type_index)


if __name__ == "__main__":
    main()
