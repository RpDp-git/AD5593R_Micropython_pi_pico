# MicroPython Library for AD5593R 

This is a MicroPython library for the AD5593R Analog/Digital Converter (ADC) on the Raspberry Pi Pico (RP2040).

## Introduction
The AD5593R is a flexible, highly configurable 8-channel ADC with an integrated programmable analog-to-digital converter (ADC), digital-to-analog converter (DAC), and GPIO (general-purpose input/output) functionality. This library provides a convenient way to interface with the AD5593R using the Raspberry Pi Pico.

## Installation
To use this library, you must first have MicroPython installed on your Raspberry Pi Pico. If you have not yet installed MicroPython on your Pico, follow these RaspberryPi foundation website.

Once you have MicroPython installed on your Pico, you can copy the AD5593R.py file to the lib directory on your Pico. This will make the library available for use in your MicroPython scripts.

## Usage

```
import utime
import AD5593Rlib
from machine import I2C, Pin
import urandom

i2c = I2C(1,freq=400000, scl=Pin(15),sda = Pin(14))

#Assuming address is 0x10 or 16
ad5593r = AD5593Rlib.AD5593R(i2c,address=0x10,IO_config = ['ADC','ADC','ADC','ADC','DAC','DAC','DAC','DAC'])

#Write 4 different values into the DAC channels
ad5593r.write_dac(4,100)
ad5593r.write_dac(5,1000)
ad5593r.write_dac(6,2000)
ad5593r.write_dac(7,3000)

#Read from ADC channel 3
while True:       
    print(ad5593r.read_adc(3))
    print('\n')
    utime.sleep(1)
```
