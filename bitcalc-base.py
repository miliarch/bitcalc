#!/usr/bin/env python3
import getopt, math, os, sys, decimal

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

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def convert_to_bits(input_type, input_value):
    is_bit = True if units[0] in input_type else False
    
    for prefix in prefixes:
        if prefix in input_type:
            if prefix == prefixes[0]:
                input_value *= mod_s
            elif prefix == prefixes[1]:
                input_value *= math.pow(mod_s, 2)
            elif prefix == prefixes[2]:
                input_value *= math.pow(mod_s, 3)
            elif prefix == prefixes[3]:
                input_value *= math.pow(mod_s, 4)
            elif prefix == prefixes[4]:
                input_value *= math.pow(mod_s, 5)
    
    if not is_bit:
        input_value *= mod_d    

    return input_value
   

def get_args():
    argv = sys.argv[1:]

    try:
        opts, args = getopt.getopt(argv, "b:ht:", ["help", "type="])
    except getopt.GetoptError:
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

    header = (" {c}Unit Type\t\tValue{endc}".format(
            c=bcolors.WARNING + bcolors.BOLD + bcolors.UNDERLINE,
            endc=bcolors.ENDC,
            )
        )
    print(header)

    max_range = type_index + 3 if type_index % 2 == 0 else type_index + 2

    table_range = range(0, max_range)

    for idx,unit in enumerate(units):
        j = idx - 2

        if idx == 0:
            table_values.append(bit_value);
        elif idx == 1:
            table_values.append(bit_value / mod_d)
        else:
            table_values.append(table_values[j] / mod_s)
        
        #prettyVal = "{:f}".format(table_values[i]).rstrip(".0") # format float, drop empty 0s from decimal value

        unit_long = unit.title()
        unit_short = " " + units_s[idx] if len(units_s[idx]) == 1 else units_s[idx]

        value_str = (" {c}{short} - {unit}s\t{endc}\t{val}".format(
                c=bcolors.OKGREEN,
                endc=bcolors.ENDC,
                unit=unit_long,
                short=unit_short,
                val=table_values[idx]
                )
            )
        
        print(value_str)
        
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
