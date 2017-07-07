#!/usr/bin/python

from __future__ import print_function

import sys
import os
import argparse
import traceback
import json
import re


error_detected = False
macro_variable = re.compile('^([^$]*)(\$\{([a-zA-Z_][a-zA-Z_0-9]*)(-([^}]+))?\})?(.*)$')
macro_name = re.compile('^([a-zA-Z_][a-zA-Z_0-9]*)$')
macro_definition = re.compile('^([a-zA-Z_][a-zA-Z_0-9]*)(=(.+))?$')


def error(message):

    global error_detected

    print('%s: %s' % (sys.argv[0], message), file=sys.stderr)
    error_detected = True


def expand(source, number, debug, macros):

    input = source
    output = ''
    while input != '':
        m = macro_variable.match(input)
        if debug:
            print(m.groups())
        input = m.group(6) if m.group(6) else ''
        output += m.group(1)
        if m.group(3):
            if m.group(3) in macros:
                output += macros[m.group(3)]
            elif m.group(5):
                output += m.group(5)
            else:
                message = 'No macro found for "{}" in line {:d}'.format(m.group(3), number)
                error(message)
                input = ''
                output = '<<<<<<<   {}\n{}\n>>>>>>>'.format(message, source)

    return output

def main():

    parser = argparse.ArgumentParser(description='Simple Pre-Processor for configuration files')
    parser.add_argument('-m', '--macros', action='store', help='JSON formatted macro definitions file')
    parser.add_argument('-D', action='append', help='Individual macro definitions')
    parser.add_argument('-n', '--dry-run', action='store_true')
    parser.add_argument('-d', '--debug', action='store_true')
    parser.add_argument('file', nargs='?')
    arguments = parser.parse_args()
    if arguments.debug:
        print(arguments, file=sys.stderr)

    if arguments.macros:
        with open(arguments.macros, 'r') as file:
            macros = json.load(file)
        for name in macros:
            m = macro_name.match(name)
            if not m:
                error('Invalid macro name: "{}"'.format(name))

    if arguments.D:
        for option in arguments.D:
            m = macro_definition.match(option)
            if m:
                name = m.groups(1)
                definition = m.groups(3) if m.groups(3) else ''
                macros[name] = definition
            else:
                error('Invalid command line macro definition: "{}"'.format(option))

    if arguments.debug:
        print(macros, file=sys.stderr)

    if not error_detected:

        if not arguments.file or (arguments.file == '-'):
            contents = sys.stdin.readlines()
        else:
            with open(arguments.file, 'r') as file:
                contents = file.read().splitlines()
        if arguments.debug:
            print(contents, file=sys.stderr)

        number = 0
        output = []
        for line in contents:
            number += 1
            output.append(expand(line, number, arguments.debug, macros))

        if not arguments.dry_run:
            for line in output:
                print(line)

    return 1 if error_detected else 0


if __name__ == '__main__':
    try:
        status = main()
        sys.exit(status)
    except Exception, e:
        print(str(e))
        traceback.print_exc()
        os._exit(1)
