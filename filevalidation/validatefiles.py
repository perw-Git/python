#!/usr/bin/python
# encoding: utf-8
import sys
import os

if (len(sys.argv) < 3):
    sys.stderr.write("Usage: validatefiles.py  <dir_existance_check>  <xml_or_properties_files>")
    sys.exit(2)
    
# read property keys (stripped) and make sure they are unique
def validateUniqueKeys(propertyFile):
    uniqueFlag = True
    separator = "="
    keys = {}
    with open(propertyFile, 'r') as file:
        for line in file:
            line = line.rstrip('\r\n')
            if (line[0] != '#') and (separator in line):
                # Find the name and value by splitting the string by first occurrence
                name, value = line.split(separator, 1)
                name = name.strip()
                if (keys.__contains__(name)):
                    sys.stderr.write("Property file '" +propertyFile+ "' key '" + name + "' is not unique.\r\n")
                    uniqueFlag = False
                else:
                    # Assign key value pair to dict
                    keys[name] = value
#     print(keys)
    return uniqueFlag

# main...
def main():
    count = 0
    hasError = False
    for filename in sys.argv:
        count += 1
        if (count == 1):
            continue
        elif (count == 2) and (not os.path.isdir(filename)):
            print("Directory '" + filename + "' does not exist, so no environment substitutions are performed.")
            sys.exit(0)
#         print (filename)
        if (not os.access(filename, os.R_OK)):
            sys.stderr.write("File not readable: " + filename + "\r\n")
            hasError = True
        if (filename.endswith('.properties') and not validateUniqueKeys(filename)):
            hasError = True
    if (hasError):
        sys.exit(2)


main()