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


def print_table(bits):
    table_values = []
    bar = "--------------------------------------"

    print(bar)
    print(bcolors.WARNING + bcolors.BOLD + bcolors.UNDERLINE + "Type" + bcolors.ENDC + bcolors.BOLD + "\t\t" + bcolors.WARNING +
        bcolors.UNDERLINE + "Value" + bcolors.ENDC)
    print(bar)
    for i,unit in enumerate(units):
        j = i - 2

        if i == 0:
            table_values.append(bits);
        elif i == 1:
            table_values.append(bits / mod_d)
        else:
            table_values.append(table_values[j] / mod_s)
        
        #prettyVal = "{:f}".format(table_values[i]).rstrip(".0") # format float, drop empty 0s from decimal value

        #print(bar)
        print(bcolors.OKGREEN + unit + "s:    \t" + bcolors.ENDC + bcolors.BOLD + str(table_values[i]) +
            bcolors.ENDC)
        
    print(bar)

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

    # Convert input value to bits
    bit_value = convert_to_bits(input_type, input_value)

    # Print conversion table
    print_table(bit_value)


if __name__ == "__main__":
    main()
