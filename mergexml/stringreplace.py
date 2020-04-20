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
read environment specific envKeys (stripped) and values (not stripped)

@var 3. resulting file (optional), otherwise print to stdout
'''
import sys

if (len(sys.argv) < 3) or (len(sys.argv) > 4):
    sys.stderr.write("Usage: stringreplace.py <template.properties_file> <environment_file> [<resulting_file>]")
    sys.exit(2)

separator = "="

# read environment specific keys (stripped) and values (not stripped)
def readEnvironmentKeys(envfile):
    keys = {}
    try:
        with open(envfile, 'r') as file:
            for line in file:
                line = line.rstrip('\r\n')
                if (line[0] != '#') and (separator in line):
                    # Find the name and value by splitting the string by first occurrence
                    name, value = line.split(separator, 1)
                    # Assign key value pair to dict
                    keys[name.strip()] = value
    except IOError:
        sys.stderr.write("File not accessible: " + envfile)
        sys.exit(2)
    # print(envKeys)
    return keys

envKeys = readEnvironmentKeys(sys.argv[2])

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
                if nameStrip in envKeys.keys():
                    resFile.write(name + '=' + envKeys[nameStrip] + '\n')
                else:
                    resFile.write(line + '\n')
            else:
                resFile.write(line + '\n')
except IOError:
    resFile.close()
    sys.stderr.write("File not accessible: " + defaultfile)
    sys.exit(2)

resFile.close()