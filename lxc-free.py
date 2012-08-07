#!/usr/bin/env python
# -*- coding: utf8 -*- 

import sys
import lxc
from lxc.utils import byte2MiByte

if (len(sys.argv) != 2):
	print "Usage %s container" % (sys.argv[0]) 
	sys.exit(1)

try:
	lxc.ContainerMemUsage(sys.argv[1])
except lxc.CGroupNotFound:
	print "Container name invalid"
	sys.exit(1)

