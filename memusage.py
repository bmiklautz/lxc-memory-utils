#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lxc.utils import *

cts=getRunningContainers()
for i in cts:
	print "%s" % i
	ContainerMemUsage(i)
	print ""
