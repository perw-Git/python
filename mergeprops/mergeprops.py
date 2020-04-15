#!/usr/bin/python
# encoding: utf-8
'''
@author: Per Wadmark

Merge properties from default property file and environment property file.
Result is printed to resultingfile or standard out.
@note: values with multiple lines are not handles.

@var 1. default properties file
default properties, where the values (only) may be substituted from env file above

@var 2. environment properties file
read environment specific keys (stripped) and values (not stripped)

@var 3. resulting file (optional), otherwise print to stdout
'''
import sys

if (len(sys.argv) < 3) or (len(sys.argv) > 4):
    print("Usage: mergeProps.py <default.properties_file> <env.properties_file> [<resulting.properties_file>]", file=sys.stderr)
    sys.exit(2)

separator = "="
keys = {}

# read environment specific keys (stripped) and values (not stripped)
envfile = sys.argv[2]
try:
    with open(envfile, 'r') as file:
        for line in file:
            line = line.rstrip('\r\n')
            if (separator in line) and (line[0] != '#'):

                # Find the name and value by splitting the string by first occurrence
                name, value = line.split(separator, 1)
                # Assign key value pair to dict
                keys[name.strip()] = value
except IOError:
    print("File not accessible: " + envfile, file=sys.stderr)
    sys.exit(2)
# print(keys)

# resulting file or stdout
if len(sys.argv) == 4:
    resFile = open(sys.argv[3], 'w')
else:
    resFile = sys.stdout

# default properties, where the values (only) may be substituted from env file above
defaultfile = sys.argv[1]
try:
    with open(defaultfile, 'r') as file:
        for line in file:
            line = line.rstrip('\r\n')
            if (separator in line) and (line[0] != '#'):
                # Find the name and value by splitting the string by first occurrence
                name, value = line.split(separator, 1)
                nameStrip = name.strip()
                if nameStrip in keys.keys():
                    resFile.write(name + '=' + keys[nameStrip] + '\n')
                else:
                    resFile.write(line + '\n')
            else:
                resFile.write(line + '\n')
except IOError:
    resFile.close()
    print("File not accessible: " + defaultfile, file=sys.stderr)
    sys.exit(2)

resFile.close()