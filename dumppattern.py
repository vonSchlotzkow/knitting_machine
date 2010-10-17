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

if patt == 0:
    pats = bf.getPatterns()
    print 'Pattern   Stitches   Rows'
    for pat in pats:
        print '  %3d       %3d      %3d' % (pat["number"], pat["stitches"], pat["rows"])
    print "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+"
    print "Data file"
    print "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+"

    # first dump the 99 'pattern id' blocks
    for i in range(100):
        print "pattern bank",i
        # each block is 7 bytes
        bytenum = i*7

        pattused = bf.getIndexedByte(bytenum)
        print "\t",hex(bytenum),": ",hex(pattused),
        if (pattused == 1):
            print "\t(used)"
        else:
            print "\t(unused)"
            print "\t-skipped-"
            continue
        bytenum += 1
        
        unk1 = bf.getIndexedByte(bytenum)
        print "\t",hex(bytenum),": ",hex(unk1),"\t(unknown)"
        bytenum += 1

        rows100 =  bf.getIndexedByte(bytenum)
        print "\t",hex(bytenum),": ",hex(rows100),"\t(rows = ", (rows100 >> 4)*100, " + ", (rows100 & 0xF)*10
        bytenum += 1

        rows1 =  bf.getIndexedByte(bytenum)
        print "\t",hex(bytenum),": ",hex(rows1),"\t\t+ ", (rows1 >> 4), " stiches = ", (rows1 & 0xF)*100,"+"
        bytenum += 1

        stitches10 =  bf.getIndexedByte(bytenum)
        print "\t",hex(bytenum),": ",hex(stitches10),"\t\t+ ", (stitches10 >> 4)*10, " +", (stitches10 & 0xF),")"
        bytenum += 1

        prog100 = bf.getIndexedByte(bytenum)
        print "\t",hex(bytenum),": ",hex(prog100),"\t(unknown , prog# = ", (prog100&0xF) * 100,"+"
        bytenum += 1

        prog10 = bf.getIndexedByte(bytenum)
        print "\t",hex(bytenum),": ",hex(prog10),"\t\t + ", (prog10>>4) * 10,"+",(prog10&0xF),")"
        bytenum += 1

else:
    print 'Searching for pattern number %d' % patt
    pats = bf.getPatterns(patt)
    if len(pats) == 0:
        print 'pattern %d not found' % patt
    else:
        stitches = pats[0]["stitches"]
        rows = pats[0]["rows"]
        print '%3d Stitches, %3d Rows' % (stitches, rows)
        pattern = bf.getPattern(patt)
        for row in range(rows):
            for stitch in range(stitches):
                if(pattern[row][stitch]) == 0:
                    print ' ',
                else:
                    print '*',
            print

