#!/usr/bin/env python

# Copyright 2009  Steve Conklin 
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
import brother

version = '1.0'

if len(sys.argv) < 2:
    print 'Usage: %s file [patternnum]' % sys.argv[0]
    print 'Dumps user programs (901-999) from brother data files'
    sys.exit()

if len(sys.argv) == 3:
    patt = int(sys.argv[2])
else:
    patt = 0

bf = brother.brotherFile(sys.argv[1])

pats = bf.getPatterns()

# find first unused pattern bank
patternbank = 100
for i in range(99):
    bytenum = i*7
    if (bf.getIndexedByte(bytenum) != 0x1):
        print "first unused pattern bank #", i
        patternbank = i
        break

if (patternbank == 100):
    print "sorry, no free banks!"
    exit
