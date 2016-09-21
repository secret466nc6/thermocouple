#!/usr/bin/python
# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# Can enable debug output by uncommenting:
#import logging
#logging.basicConfig(level=logging.DEBUG)

import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_MAX31855.MAX31855 as MAX31855
import xlsxwriter

# Define a function to convert celsius to fahrenheit.
def c_to_f(c):
        return c * 9.0 / 5.0 + 32.0


# Uncomment one of the blocks of code below to configure your Pi or BBB to use
# software or hardware SPI.

# Raspberry Pi software SPI configuration.


DO  = 14
CLK = 15
CS0  = 12
CS1  = 16
CS2  = 20
CS3  = 21
sensor0 = MAX31855.MAX31855(CLK, CS0, DO)
sensor1 = MAX31855.MAX31855(CLK, CS1, DO)
sensor2 = MAX31855.MAX31855(CLK, CS2, DO)
sensor3 = MAX31855.MAX31855(CLK, CS3, DO)
# Raspberry Pi hardware SPI configuration.
#SPI_PORT   = 0
#SPI_DEVICE = 0
#sensor = MAX31855.MAX31855(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

# BeagleBone Black software SPI configuration.
#CLK = 'P9_12'
#CS  = 'P9_15'
#DO  = 'P9_23'
#sensor = MAX31855.MAX31855(CLK, CS, DO)

# BeagleBone Black hardware SPI configuration.
#SPI_PORT   = 1
#SPI_DEVICE = 0
#sensor = MAX31855.MAX31855(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
with xlsxwriter.Workbook('hello_world.xlsx') as workbook:
    worksheet = workbook.add_worksheet()
# Loop printing measurements every second.
print('Press Ctrl-C to quit.')
i = 0
while True:
    temp0 = sensor0.readTempC()
    temp1 = sensor1.readTempC()
    temp2 = sensor2.readTempC()
    temp3 = sensor3.readTempC()
    
    #internal = sensor.readInternalC()
    print('(0)Thermocouple Temperature: {0:0.3F}*C / {1:0.3F}*F'.format(temp0, c_to_f(temp0)))
    print('(1)Thermocouple Temperature: {0:0.3F}*C / {1:0.3F}*F'.format(temp1, c_to_f(temp1)))
    print('(2)Thermocouple Temperature: {0:0.3F}*C / {1:0.3F}*F'.format(temp2, c_to_f(temp2)))
    print('(3)Thermocouple Temperature: {0:0.3F}*C / {1:0.3F}*F'.format(temp3, c_to_f(temp3)))
    #print('    Internal Temperature: {0:0.3F}*C / {1:0.3F}*F'.format(internal, c_to_f(internal)))
    worksheet.write(i,0, 'Hello world')
    i = i + 1
    time.sleep(1.0)

