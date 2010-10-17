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
import Image
import array

##################
TheImage = None

def getimageprops(imgfile):
    x = 0
    y = 0


##################

version = '1.0'

if len(sys.argv) < 3:
    print 'Usage: %s brotherfile image.bmp' % sys.argv[0]
    sys.exit()

imgfile = sys.argv[2]

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

# ok got a bank, now lets figure out how big this thing we want to insert is
TheImage = Image.open(imgfile)
TheImage.load()

im_size = TheImage.size
width = im_size[0]
print "width:",width
height = im_size[1]
print "height:", height

# debugging stuff here
x = 0
y = 0

x = width - 1
while x > 0:
    value = TheImage.getpixel((x,y))
    if value:
        sys.stdout.write('* ')
    else:
        sys.stdout.write('  ')
    #sys.stdout.write(str(value))
    x = x-1
    if x == 0: #did we hit the end of the line?
        y = y+1
        x = width - 1
        print " "
        if y == height:
            break
# debugging stuff done

# create the program entry
progentry = []
progentry.append(0x1)  # is used
progentry.append(0x0)  # no idea what this is
progentry.append( (int(width / 100) << 4) | (int((width%100) / 10) & 0xF) )
progentry.append( (int(width % 10) << 4) | (int(height / 100) & 0xF) )
progentry.append( (int((height % 100)/10) << 4) | (int(height % 10) & 0xF) )

# now we have to pick out a 'program name'
patternnum = 901 # start with 901? i dunno
for pat in pats:
    if (pat["number"] >= patternnum):
        patternnum = pat["number"] + 1

#print patternnum
progentry.append(int(patternnum / 100) & 0xF)
progentry.append( (int((patternnum % 100)/10) << 4) | (int(patternnum % 10) & 0xF) )

print "Program entry: ",map(hex, progentry)
