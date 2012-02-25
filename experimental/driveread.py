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

FILTER=''.join([(len(repr(chr(x)))==3) and chr(x) or '.' for x in range(256)])

def dump(src, length=16):
    result=[]
    for i in xrange(0, len(src), length):
       s = src[i:i+length]
       hexa = ' '.join(["%02X"%ord(x) for x in s])
       printable = s.translate(FILTER)
       result.append("%04X   %-*s   %s\n" % (i, length*3, hexa, printable))
    return ''.join(result)

class PDD1():

    def __init__(self):
        self.verbose = True
        self.commport = ''
        self.ser = None
        return

    def __del__(self):
        return

    def open(self, cport='/dev/ttyUSB0', rate = 9600, par = 'N', stpbts=1, tmout=1, xx=0):
        print "Open enter"
        #self.ser = serial.Serial(port = cport, baudrate = rate, parity = par, stopbits = stpbts, timeout = tmout, xonxoff=0)
        self.ser = serial.Serial(port = cport, baudrate = rate, parity = par, stopbits = stpbts, timeout = tmout, xonxoff=0, rtscts=1, dsrdtr=0)
        if self.ser == None:
            print 'Unable to open serial device %s' % cport
            raise IOError
        self.commtimeout = tmout
        # Sometimes on powerup there are some characters in the buffer, purge them
        self.dumpchars()
        #foo = 0
        #while self.ser.inWaiting():
        #    bar = self.ser.read(1)
        #    foo = foo+1
        #if self.verbose and foo:
        #    print 'During open %d characters were read from the serial port and discarded' % foo
        print "Open Exit"
        return

    def close(self):
        if self.ser is not None:
            self.ser.close()
            self.ser = None
        return

    def dumpchars(self):
        num = 1
        while self.ser.inWaiting():
            inc = self.ser.read()
            if len(inc) != 0:
                print 'flushed 0x%02X (%d)' % (ord(inc), num)
                num = num + 1
            else:
                break
        return

    def readsomechars(self):
        if True:
            waiting = self.ser.inWaiting()
            print "readsomechars - waiting chars: ", waiting
            print "CTS = ", self.ser.getCTS()
            #time.sleep(1)
            #waiting = 1
            while  waiting == 0:
                print "CTS = ", self.ser.getCTS()
                if self.verbose:
                    print 'waiting'
                time.sleep(.1)
                waiting = self.ser.inWaiting()

            if self.verbose:
                print "readsomechars: waiting = ", waiting

        sch = self.ser.read(waiting)
        return sch

    def readchar(self):
        inc = ''
        while len(inc) == 0:
            inc = self.ser.read()
        return inc
            
    def writebytes(self, bytes):
        print "CTS = ", self.ser.getCTS()
        self.ser.write(bytes)
        return

    def calcChecksum(self, string):
        sum = 0
        for schr in string:
            sum = sum + ord(schr)
        sum = sum % 0x100
        sum = sum ^ 0xFF
        return chr(sum)

    def __commandResponse(self, command):
        if self.verbose:
            pcmd = command.strip()
            print 'writing command ===> <%s>' % pcmd
        self.dumpchars()
        ds_string = command
        cs = self.calcChecksum(ds_string)
        ds_string = ds_string + cs
        print "cR sending . . ."
        print dump(ds_string)
        self.writebytes(ds_string)
        response = self.readsomechars()
        print 'Command got a response of ', response
        return response

    def __FDCcommandResponse(self, command):
        if self.verbose:
            pcmd = command.strip()
            print 'writing FDC command ===> <%s>' % pcmd
        self.dumpchars()
        print "FDC Sending . . ."
        print dump(command)
        self.writebytes(command)
        response = self.readsomechars()
        print 'FDC Command got a response of ', response
        return response
    #
    # Begin commands
    #

    def EnterOpMode(self):
        if False:
            command = "ZZ" + chr(0x08) + chr(0)
            cs = self.calcChecksum(command)
            command = command + cs + "\r"
        else:
            command = "ZZ" + chr(0x08) + chr(0) + chr(0xF7) + "\r"
        print "Sending: . . ."
        print dump(command)
        self.writebytes(command)
        # There's no response to this command, so allow time to complete
        time.sleep(.010)

    def getDriveStatus(self):
        command = "ZZ" + chr(0x07) + chr(0)
        print "Sending request for Drive status: . . ."
        print dump(command)
        result = self.__commandResponse(command)
        return result

    def checkDeviceCondition(self):
        command = "D\r"
        return self.__FDCcommandResponse(command)

    def format(self):
        command = "F5\r"
        return self.__FDCcommandResponse(command)

    def sendS(self):
        command = "S\r"
        return self.__FDCcommandResponse(command)


# meat and potatos here

if len(sys.argv) < 2:
    print 'Usage: %s serialdevice' % sys.argv[0]
    sys.exit()

#print 'Preparing . . . Please Wait'
drive = PDD1()

#print 'open'
drive.open(cport=sys.argv[1], tmout = None)

drive.EnterOpMode()
#stat = drive.format() # FDC Mode
stat = drive.checkDeviceCondition() # FDC Mode
stat = drive.sendS()

# OR
#stat = drive.getDriveStatus() # NOT FDC mode

print 'Status = '
print dump(stat)


drive.close()
