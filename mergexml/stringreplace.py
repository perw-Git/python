#!/usr/bin/python3
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
    sys.stderr.write("Usage: python3 stringreplace.py <template.properties_file> <environment_file> [<resulting_file>]")
    sys.exit(2)

separator = "="

def replaceAll(text, dic):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text

# read environment specific keys (stripped) and values (not stripped)
def readEnvironmentKeys(envfile):
    keys = {}
    try:
        with open(envfile, 'r') as file:
            for line in file:
                line = line.rstrip('\r\n')
                if (separator in line) and (line[0] != '#'):
                    # Find the name and value by splitting the string by first occurrence
                    name, value = line.split(separator, 1)
                    # Assign key value pair to dict
                    keys['{' +name.strip()+ '}'] = value
    except IOError:
        sys.stderr.write("File not accessible: " + envfile)
        sys.exit(2)
    return keys

def main():
    envKeys = readEnvironmentKeys(sys.argv[1])
    
    # resulting file or stdout
    if len(sys.argv) == 4:
        resFile = open(sys.argv[3], 'w')
    else:
        resFile = sys.stdout
    
    # default properties, where the values (only) may be substituted from env file above
    templatefile = sys.argv[2]
    try:
        with open(templatefile, 'r') as file:
            text = file.read() #.replace('\n', '')
            text = replaceAll(text, envKeys)
            resFile.write(text)
    except IOError:
        resFile.close()
        sys.stderr.write("File not accessible: " + templatefile)
        sys.exit(2)
    
    resFile.close()
    
main()