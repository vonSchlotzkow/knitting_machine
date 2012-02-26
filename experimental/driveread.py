#!/usr/bin/env python

# Copyright 2012  Steve Conklin 
# steve at conklinhouse dot com
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

import sys
#import os
#import os.path
#import string
import time
import serial

from FDif import PDD1, dump

# meat and potatos here

if len(sys.argv) < 2:
    print 'Usage: %s serialdevice' % sys.argv[0]
    sys.exit()

#print 'Preparing . . . Please Wait'
drive = PDD1()

#print 'open'
drive.open(cport=sys.argv[1], tmout = None)

drive.EnterFDCMode()
#stat = drive.FDCformat() # FDC Mode
#stat = drive.FDCcheckDeviceCondition() # FDC Mode
#stat = drive.FDCsendS()
for sector in range(2):
    sid = drive.FDCreadIdSection(psn = '%d' % sector)
    print "Sector ID: "
    print dump(sid)
    data = drive.FDCreadSector(psn = '%d' % sector)
    print "Sector Data: "
    print dump(data)

drive.close()
