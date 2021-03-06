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

# import convenience functions from brother module
from brother import roundeven, roundfour, roundeight, nibblesPerRow, bytesPerPattern, bytesForMemo

TheImage = None

version = '1.0'

if len(sys.argv) < 5:
    print 'Usage: %s oldbrotherfile pattern# image.bmp newbrotherfile' % sys.argv[0]
    sys.exit()


bf = brother.brotherFile(sys.argv[1])
pattnum = sys.argv[2]
imgfile = sys.argv[3]


pats = bf.getPatterns()

# ok got a bank, now lets figure out how big this thing we want to insert is
TheImage = Image.open(imgfile)
TheImage.load()

im_size = TheImage.size
width = im_size[0]
print "width:",width
height = im_size[1]
print "height:", height



# find the program entry
thePattern = None

for pat in pats:
    if (int(pat["number"]) == int(pattnum)):
        #print "found it!"
        thePattern = pat
if (thePattern == None):
    print "Pattern #",pattnum,"not found!"
    exit(0)

if (height != thePattern["rows"] or width != thePattern["stitches"]):
    print "Pattern is the wrong size, the BMP is ",height,"x",width,"and the pattern is ",thePattern["rows"], "x", thePattern["stitches"]
    exit(0)

# debugging stuff here
x = 0
y = 0

x = width - 1
while x >= 0:
    value = TheImage.getpixel((x,y))
    if value:
        sys.stdout.write('* ')
    else:
        sys.stdout.write('  ')
    #sys.stdout.write(str(value))
    x = x-1
    if x < 0: #did we hit the end of the line?
        y = y+1
        x = width - 1
        print " "
        if y == height:
            break
# debugging stuff done

# now to make the actual, yknow memo+pattern data

# the memo seems to be always blank. i have no idea really
memoentry = []
for i in range(bytesForMemo(height)):
    memoentry.append(0x0)

# now for actual real live pattern data!
pattmem = brother.image2nibblestream(TheImage)

#print map(hex, pattmem)
# whew. 


# now to insert this data into the file 

# now we have to figure out the -end- of the last pattern is
endaddr = 0x6df

beginaddr = thePattern["pattend"]
endaddr = beginaddr + bytesForMemo(height) + len(pattmem)
print "beginning will be at ", hex(beginaddr), "end at", hex(endaddr)

# Note - It's note certain that in all cases this collision test is needed. What's happening
# when you write below this address (as the pattern grows downward in memory) in that you begin
# to overwrite the pattern index data that starts at low memory. Since you overwrite the info
# for highest memory numbers first, you may be able to get away with it as long as you don't
# attempt to use higher memories.
# Steve

if beginaddr <= 0x2B8:
    print "sorry, this will collide with the pattern entry data since %s is <= 0x2B8!" % hex(beginaddr)
    #exit

# write the memo and pattern entry from the -end- to the -beginning- (up!)
for i in range(len(memoentry)):
    bf.setIndexedByte(endaddr, 0)
    endaddr -= 1

for i in range(len(pattmem)):
    bf.setIndexedByte(endaddr, pattmem[i])
    endaddr -= 1

# push the data to a file
outfile = open(sys.argv[4], 'wb')

d = bf.getFullData()
outfile.write(d)
outfile.close()
