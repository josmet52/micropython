#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
project : analog_esp32.py
----------------------------
sync analog in with calibration for a divider

CLASS : AnalogEsp
PROCESSOR : ESP32 
OS : micropython
uC : WEMOS MINI D1
VERSION 1.0.0

12.06.2021
jmb52.dev@gmail.com
"""
import machine

class AnalogInEsp32:
    
    def __init__(self, analog_pin, R1=0, R2=1e9):
        
        self.ANALOG_PIN = analog_pin
        self.R1 = R1
        self.R2 = R2
    
    def get_voltage(self):

        ubat = machine.ADC(machine.Pin(self.ANALOG_PIN))
        ubat.atten(machine.ADC.WIDTH_12BIT)       #Full range: 3.3v
        bin_pin_measure = ubat.read()
        """ conversion D/A :
            4095 ^ 3.3V
        """
        analog_in_voltage =  3.3 * bin_pin_measure / 4095 / self.R2 * (self.R1 + self.R2)
        return analog_in_voltage

if __name__ == '__main__':

    my_analog_esp = AnalogInEsp32(34, 100e3, 100e3)
    
    print('-----------------------------------------------------------')
    if my_analog_esp.R1 != 0:
        print('R1 = ' + str(my_analog_esp.R1))
        print('R2 = ' + str(my_analog_esp.R2))
#     print('gpio analog input impedance:', my_analog_esp.Rgpio)
    print('Voltage on PIN ' + str(my_analog_esp.ANALOG_PIN) + ' = ' + '{:.2f}[V]'.format(my_analog_esp.get_voltage()))
    print('-----------------------------------------------------------')
