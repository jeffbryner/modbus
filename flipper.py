#!/usr/bin/python2
import os
import sys
from pymodbus.client.sync import ModbusTcpClient
from random import randint
from optparse import OptionParser

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-s", dest='start' , default=0, type="int", help="starting row")
    parser.add_option("-e", dest='end' , default=4095, type="int", help="starting row")
    parser.add_option("-i", dest='ipaddress', default="",help="ipaddress to target")
    
    (options,args) = parser.parse_args()
    
    client = ModbusTcpClient(options.ipaddress)
    #for x in range(4090,4095):
    
    #check for stupidity
    if len(options.ipaddress.strip())==0:
        print('invalid target ip')
        sys.exit(1)
    if options.start<0 or (options.start>options.end):
        print('invalid start (0-4095)')
        sys.exit(1)
    if options.end>4095 or (options.end<options.start):
        print('invalid end (0-4095)')
        sys.exit(1)

    #client reads at least 8 bits at a time, no matter what you ask for..so get 16
    #and flip bits rows at a time bits 0-65535, rows 0-4095, 16bits each time.
    for x in range(options.start,options.end):
        row=min(x*16,65520)
        result = client.read_coils(row,16)
        print("flipping bits from %d,%d"%(row,min(row+16,65535)))
        print("was %r"%result.bits)
        for y in range(len(result.bits)-1):
            if result.bits[y]:
                client.write_coil((row)+y, False)
            else:
                client.write_coil((row)+y,True)
    
    client.close()
