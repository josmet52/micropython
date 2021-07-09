#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
project : ds18x20_lobo_ttgo.py.py
----------------------------
use the temperature sensor DS18B20 with examples
More details on : https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo/wiki/display

CLASS : tft_lobo_ttgo
PROCESSOR : ESP32
OS : loboris micropython
uC : TTGO T-DISPLAY ESP32
Display type : ST 7789V 135x240

22.05.2021
jmb52.dev@gmail.com
"""

import machine
import utime

class ds18x20_lobo_ttgo:
    
    def __init__(self, pin):
    
        self.ow = machine.Onewire(pin)  # Initialize onewire & DS18B20 temperature sensor
        self.roms = []
        for i, rom in enumerate (self.ow.scan()):
            if rom[-2:] == '10' or rom[-2:] == '28':
                sensor_id = rom[-2:] + '-' + rom[:-4]
                self.roms.append([sensor_id, machine.Onewire.ds18x20(self.ow, i)])

    def read_temps_lobo_ttgo(self): 
        
        v_ret = []
        for rom in self.roms:
            sensor_id = rom[0]
            sensor_temp = '{:.1f}'.format(rom[1].convert_read())
            v_ret.append([sensor_id, sensor_temp])
        return v_ret

if __name__ == '__main__':
    
    ds18x20 = ds18x20_lobo_ttgo(13)
    while True:
        temps = ds18x20.read_temps_lobo_ttgo()
        for m in temps:
            print('sensor: ' + m[0] + ' -> température: ' + m[1])
        print()
        utime.sleep(5)
