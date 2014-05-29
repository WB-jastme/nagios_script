#!/usr/bin/env python

"""

    Nagios plugin to report Memory usage by parsing /proc/meminfo
    by L.S. Keijser <keijser@stone-it.com>
    This script takes Cached memory into consideration by adding that
    to the total MemFree value.
    by boge modified,can used by pnp4nagios

"""

from optparse import OptionParser
import sys

checkmemver = '0.1'

# Parse commandline options:
parser = OptionParser(usage="%prog -w <warning threshold> -c <critical threshold> [ -h ]",version="%prog " + checkmemver)
parser.add_option("-w", "--warning",
    action="store", type="string", dest="warn_threshold", help="Warning threshold in percentage")
parser.add_option("-c", "--critical",
    action="store", type="string", dest="crit_threshold", help="Critical threshold in percentage")
(options, args) = parser.parse_args()


def readLines(filename):
    f = open(filename, "r")
    lines = f.readlines()
    return lines

def readMemValues():
    global memTotal, memCached, memFree
    for line in readLines('/proc/meminfo'):
        if line.split()[0] == 'MemTotal:':
            memTotal = line.split()[1]
        if line.split()[0] == 'MemFree:':
            memFree = line.split()[1]
        if line.split()[0] == 'Cached:':
            memCached = line.split()[1]

def percMem():
    readMemValues()
    return (((int(memFree) + int(memCached)) * 100) / int(memTotal))

def realMem():
    readMemValues()
    return (int(memFree) + int(memCached)) / 1024

def go():
    if not options.crit_threshold:
        print "UNKNOWN: Missing critical threshold value."
        sys.exit(3)
    if not options.warn_threshold:
        print "UNKNOWN: Missing warning threshold value."
        sys.exit(3)
    if int(options.crit_threshold) >= int(options.warn_threshold):
        print "UNKNOWN: Critical percentage can't be equal to or bigger than warning percentage."
        sys.exit(3)
    trueFree = percMem()
    trueMemFree = realMem()
    if int(trueFree) <= int(options.crit_threshold):
        print "CRITICAL: Free memory percentage is less than or equal to %s%% %s %sMB | mem = %sMB;6546;3273;0;32732"  %(str(options.crit_threshold),str(trueFree),str(trueMemFree),str(trueMemFree))
        sys.exit(2)
    if int(trueFree) <= int(options.warn_threshold):
        print "WARNING: Free memory percentage is less than or equal to %s%% %s %sMB | mem = %sMB;6546;3273;0;32732"  %(str(options.warn_threshold),str(trueFree),str(trueMemFree),str(trueMemFree))
        sys.exit(1)
    else:
        print "OK: Free memory percentage is %s%% %sMB | mem = %sMB;6546;3273;0;32732"  %(str(trueFree),str(trueMemFree),str(trueMemFree))
        sys.exit(0)

if __name__ == '__main__':
    go()



