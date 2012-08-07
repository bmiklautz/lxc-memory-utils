#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import lxc
import sys

def getRunningContainers():
	lxcdir=os.listdir(lxc.basepath)
	ret = []
	for entry in lxcdir:
		if os.path.isdir(os.path.join(lxc.basepath, entry)):
			ret.append(entry)
	return ret

def byte2MiByte(val):
	        return val/1024/1024

def ContainerMemUsage(name):
	inst = lxc.cgroup(name)

	memlimit = int(inst.getValue("memory.limit_in_bytes"))
	memswlimit = int(inst.getValue("memory.memsw.limit_in_bytes"))
	memused = int(inst.getValue("memory.usage_in_bytes"))
	memswused = int(inst.getValue("memory.memsw.usage_in_bytes"))

	print "         %12s	%12s	%12s	%12s" % ("total","used","free", "percent used")
	print "Mem  :	%12i	%12i	%12i	%12i" % (byte2MiByte(memlimit),byte2MiByte(memused),byte2MiByte(memlimit-memused), memused/float(memlimit)*100)
	print "Swap :	%12i	%12i	%12i	%12i" % (byte2MiByte(memswlimit-memlimit),byte2MiByte(memswused-memused),byte2MiByte(memswlimit-memlimit-(memswused-memused)), (memswused-memused)/float(memswlimit-memlimit)*100)
	print "Total:	%12i	%12i	%12i	%12i" % (byte2MiByte(memswlimit),byte2MiByte(memswused),byte2MiByte(memswlimit-memswused), memswused/float(memswlimit)*100)
