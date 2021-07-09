#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
project : hw390_esp32.py
----------------------------
voltage measurement with and without divider bridge 

CLASS : Hw390Esp32
PROCESSOR : ESP32 
OS : micropython
uC : WEMOS MINI D1
VERSION : 1.0.0
DATE : 12.06.2021
jmb52.dev@gmail.com
"""
import machine

class Hw390Esp32:

    def __init__(self):
        self.HW390_U100 = 1 # tension mesuree sur la sonde quand l'umidite de la terre est de 100%
        self.HW390_U000 = 3 # tension mesuree sur la sonde quand l'umidite de la terre est de 100%
        
    def get_soil_moisture(self, pin):
        # measure the voltage on the sensor
        hw390 = machine.ADC(machine.Pin(pin))
        hw390.atten(machine.ADC.WIDTH_12BIT)
        v_sensor = hw390.read()
        u_moist =  v_sensor / 0xFFF * 3.3
        if u_moist < self.HW390_U100:
            u_moist = -1
            moist_rel = -1
        else:
            # convert the voltage in %
            moist_rel = (u_moist - self.HW390_U000) / (self.HW390_U100 - self.HW390_U000) * 100
        return moist_rel

if __name__ == '__main__':
    
    HW390_PIN_1 = 35 # soil humidity sensor
    HW390_PIN_2 = 36 # soil humidity sensor
    
    hw390_esp32 = Hw390Esp32()
    moist_rel_1 = hw390_esp32.get_soil_moisture(HW390_PIN_1)
    moist_rel_2 = hw390_esp32.get_soil_moisture(HW390_PIN_2)
    
    print('-----------------------------------------------------------')
    print('HW-390 soil sensor: sensor_1 humidity rel =' + ' %3.0f%%' %moist_rel_1)
    print('HW-390 soil sensor: sensor_2 humidity rel =' + ' %3.0f%%' %moist_rel_2)
    print('-----------------------------------------------------------')
    

        
