#!/usr/bin/env python
# -*- coding: utf8 -*- 

import argparse
import lxc
import sys

def percent(given, total):
	return (given/float(total))*100.0

def addState(host, which, state):
	if (not host in state[which]):
		state[which].append(host)

def checkValues(host, val, warn, crit, state):
	if (val >= crit):
		addState(host, 'critical', state)
	elif (val >= warn):
		addState(host, 'warn', state)
	else:
		addState(host, 'ok', state)

parser = argparse.ArgumentParser(description='Nagios check for lxc memory', epilog='Thats pretty much all')
parser.add_argument('--version', action='version', version='%(prog)s 0.1')

parser._optionals.title = "flags"
parser.add_argument('-w', '--warn', help='warn level (percent used default 95)', default=95, action='store', type=int)
parser.add_argument('-c', '--critical', help='critical level (percent used default 98)', default=98, action='store', type=int)

group =  parser.add_argument_group('check specs')
group.add_argument('-m', '--disable-mem', help='disable memory check', action='store_true')
group.add_argument('-s', '--disable-memsw', help='disable memorysw check', action='store_true')
group.add_argument('-f', '--failcount', help="also check failcount (memory only)", action='store_true')

group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-a', '--all', help='check all running containers', action='store_true')
group.add_argument('container', nargs='?', help='name of the continer', action='store', type=str)


args = parser.parse_args()
if ((args.disable_mem and args.disable_memsw) and not args.failcount):
	parser.error('some check needs to be performed (either add -f or remove -m or -s)')

if (args.critical < args.warn):
	parser.error('critical must be higher than warning')

hosts = []
if (args.all):
	hosts = lxc.getRunningContainers()
else:
	hosts.append(args.container)

state = {}
state['critical'] = []
state['warn'] = []
state['ok'] = []
state['notrunning'] = []

for host in hosts:
	inst = None
	try:
		inst = lxc.cgroup(host)
	except lxc.CGroupNotFound:
		addState(host, 'notrunning', state)
		continue

	if (not args.disable_mem):
		memused = int(inst.getValue("memory.usage_in_bytes"))
		memlimit = int(inst.getValue("memory.limit_in_bytes"))
		checkValues(host, percent(memused, memlimit), args.warn, args.critical, state)
	if (not args.disable_memsw):
		memswused = int(inst.getValue("memory.memsw.usage_in_bytes"))
        	memswlimit = int(inst.getValue("memory.memsw.limit_in_bytes"))
		checkValues(host, percent(memswused, memswlimit), args.warn, args.critical, state)
	if (args.failcount):
        	memfailcnt = int(inst.getValue("memory.failcnt"))
		if (memfailcnt > 0):
			addState(host, 'critical', state)
		else:
			addState(host, 'ok', state)

if len(state['critical']):
	print "CRITICAL - host(s) %s" % state['critical']
	sys.exit(2)

if len(state['warn']):
	print "WARNING - host(s) %s" % state['warn']
	sys.exit(1)

print "OK - All limits are fine"
sys.exit(0)
