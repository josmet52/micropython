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
import adc1_cal_jo

if __name__ == '__main__':

   
    ADC1_PIN = 35
    R1 = 100e3
    R2 = 33e3
    DIV       = R2 / (R1 + R2) # (R2 / R1 + R2) -> V_meas = V(R1 + R2); V_adc = V(R2)  
    AVERAGING = 10                # no. of samples for averaging
    ubatt = adc1_cal_jo.ADC1Cal(machine.Pin(ADC1_PIN, machine.Pin.IN), DIV, None, AVERAGING, "ADC1 eFuse Calibrated")

    # set ADC result width
    ubatt.width(machine.ADC.WIDTH_12BIT)
    # set attenuation
    ubatt.atten(machine.ADC.ATTN_11DB)

    print('-----------------------------------------------------------')
    print('With divider bridge')
    # measure with a divider bridge R1-R2
    print('Voltage on divider (PIN ' + str(ADC1_PIN) + ') = ' + '{:.0f}mV'.format(ubatt.voltage))
    
