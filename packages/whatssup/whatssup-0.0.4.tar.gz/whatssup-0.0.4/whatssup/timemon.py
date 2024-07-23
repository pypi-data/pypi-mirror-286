#!/usr/bin/env python

import getopt
import os
import sys
import xmlrpc.client as xmlrpcclient

from supervisor import childutils


class Timeout:
    def __init__(self, arguments):
        self.args = arguments
        self.stdin = sys.stdin
        self.stdout = sys.stdout
        self.stderr = sys.stderr
        self.rpc = None

    def run(self):
        while 1:
            headers, payload = childutils.listener.wait(self.stdin, self.stdout)

            if not headers['eventname'].startswith('TICK'):
                # do nothing with non-TICK events
                childutils.listener.ok(self.stdout)
                continue

            process_infos = self.rpc.supervisor.getAllProcessInfo()

            for process_info in process_infos:
                name = process_info['name']
                uptime = process_info['now'] - process_info['start']

                if name in self.args['programs'] and uptime > self.args['programs'][name]:
                    self.restart(name)

            self.stderr.flush()

            childutils.listener.ok(self.stdout)

    def stop(self, name):
        try:
            self.rpc.supervisor.stopProcess(name)
        except xmlrpcclient.Fault as e:
            msg = ('Failed to stop process %s, exiting: %s' %
                   (name, e))
            self.stderr.write(str(msg))
            raise

    def start(self, name):
        try:
            self.rpc.supervisor.startProcess(name)
        except xmlrpcclient.Fault as e:
            msg = ('Failed to start process %s, exiting: %s' %
                   (name, e))
            self.stderr.write(str(msg))
            raise

    def restart(self, name):
        self.stderr.write('Restarting %s\n' % name)

        self.stop(name)
        self.start(name)

        self.stderr.write('Restarted %s\n' % name)


def parse_program_arg(option, value):
    try:
        name, timeout = value.split('=')
        timeout = int(timeout)
    except ValueError:
        print('Invalid value %r for %r' % (value, option))
        name = None
        timeout = None
    return name, timeout


def parse_args(arguments):
    short_args = 'p:'
    long_args = [
        'program=',
    ]
    parsed_args = {}

    if not arguments:
        return parsed_args
    try:
        opts, args = getopt.getopt(arguments, short_args, long_args)
    except:
        return parsed_args

    parsed_args['programs'] = {}

    for option, value in opts:

        if option in ('-p', '--program'):
            name, timeout = parse_program_arg(option, value)
            parsed_args['programs'][name] = timeout

    return parsed_args


def main():
    parsed_args = parse_args(sys.argv[1:])
    timeout = Timeout(parsed_args)
    timeout.rpc = childutils.getRPCInterface(os.environ)
    timeout.run()


if __name__ == '__main__':
    main()
