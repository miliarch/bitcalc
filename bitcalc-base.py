#!/usr/bin/env python3
import getopt, math, os, sys, decimal

prefixes = ["kilo", "mega", "giga", "tera", "peta"]
units = ["bit", "byte"]

for prefix in prefixes:
   units.append(prefix + ''.join(units[0]))
   units.append(prefix + ''.join(units[1]))

mod_s = 1024
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

def check_value(input_type):
    for unit in units:
        if input_type == unit:
            return True

    return False


def convert_to_bits(input_type, input_value):
    if not check_value(input_type):
        return False

    is_bit = True if units[0] in input_type else False
    
    for mod in prefixes:
        if mod in input_type:
            if mod == prefixes[0]:
                input_value *= mod_s
            elif mod == prefixes[1]:
                input_value *= math.pow(mod_s, 2)
            elif mod == prefixes[2]:
                input_value *= math.pow(mod_s, 3)
            elif mod == prefixes[3]:
                input_value *= math.pow(mod_s, 4)
            elif mod == prefixes[4]:
                input_value *= math.pow(mod_s, 5)
            
            isValid = True
    
    if not is_bit:
        input_value *= mod_d    
        
    return input_value
   

def print_table(bits):
    table_values = []
    bar = "--------------------------------------"

    print(bar)
    print(bcolors.WARNING + bcolors.BOLD + bcolors.UNDERLINE + "Type" + bcolors.ENDC + bcolors.BOLD + "\t\t" + bcolors.WARNING +
        bcolors.UNDERLINE + "Value" + bcolors.ENDC)
    print(bar)
    for i,type in enumerate(units):
        j = i - 2

        if i == 0:
            table_values.append(bits);
        elif i == 1:
            table_values.append(bits / mod_d)
        else:
            table_values.append(table_values[j] / mod_s)
        
        prettyVal = "{:f}".format(table_values[i]).rstrip(".0") # format float, drop empty 0s from decimal value

        #print(bar)
        print(bcolors.OKGREEN + type + "s:    \t" + bcolors.ENDC + bcolors.BOLD + str(table_values[i]) +
            bcolors.ENDC)
        
    print(bar)

def usage():
    print("help coming maybe.  -t for type")

def main(argv):
    input_type = "byte"
    
    try:
        opts, args = getopt.getopt(argv, "b:ht:", ["help", "type="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    count = 0

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt == "-b":
            input_value = float(arg)
        elif opt == "-t":
            input_type = arg

    bit_value = convert_to_bits(input_type, input_value)

    print_table(bit_value)

if __name__ == "__main__":
    main(sys.argv[1:])
