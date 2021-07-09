#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
project : voltage_esp32.py
----------------------------
voltage measurement with and without divider bridge 

CLASS : VoltageEsp32
PROCESSOR : ESP32 
OS : micropython
uC : WEMOS MINI D1
VERSION : 1.0.0
DATE : 12.06.2021
jmb52.dev@gmail.com
"""
import machine

class VoltageEsp32:
    
    def __init__(self, analog_pin, R1=0, R2=1e12):
        
        self.ANALOG_PIN = analog_pin
        self.R1 = R1
        self.R2 = R2
    
    def get_voltage(self):

        ubat = machine.ADC(machine.Pin(self.ANALOG_PIN))
        ubat.atten(machine.ADC.WIDTH_12BIT)
        bin_measure = ubat.read()
        """ full range 12 bits = 3.3V
            conversion D/A : 12 bits ^ 0xFFF ^ 4095 ^ 3.3V
        """
        analog_in_voltage =  bin_measure / 0xFFF * 3.3 / self.R2 * (self.R1 + self.R2)
        return analog_in_voltage

if __name__ == '__main__':

    ANALOG_IN_PIN_0 = 35
    ANALOG_IN_PIN_1 = 35
    R1 = 100e3
    R2 = 33e3
    
    print('-----------------------------------------------------------')
    print('With divider bridge')
    # measure with a divider bridge R1-R2
    my_divided_voltage = VoltageEsp32(ANALOG_IN_PIN_0, R1, R2) # Uin max = 3.3 * (R1+R2)/R2 
    if my_divided_voltage.R1 != 0:
        print('R1 = ' + str(my_divided_voltage.R1))
        print('R2 = ' + str(my_divided_voltage.R2))
    print('Voltage on divider (PIN ' + str(my_divided_voltage.ANALOG_PIN) + ') = ' + '{:.2f}V'.format(my_divided_voltage.get_voltage()))
    
    # undiveded voltage example
    # measure witout dividr bridge --> omit params R1 and R2
    print('-----------------------------------------------------------')
    print('Without divider bridge')
    my_voltage = VoltageEsp32(ANALOG_IN_PIN_1) # Uin max = 3.3V
    print('Voltage on PIN ' + str(my_voltage.ANALOG_PIN) + ' = ' + '{:.2f}V'.format(my_voltage.get_voltage()))
    print('-----------------------------------------------------------')
