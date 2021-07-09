#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
project : ds18x20_esp32.py
----------------------------
use the temperature sensor DS18B20 with examples

CLASS : ds18x20_esp32
PROCESSOR : ESP32
OS : micropython
uC : WEMOS MINI D1

22.05.2021
jmb52.dev@gmail.com
"""

import machine
import utime
import onewire
import ds18x20
import ubinascii

class Ds18x20Esp32:
    
    def __init__(self, pin):
        self.DS18B20_pin = pin
        self.DS18X20_READ_TIME = 750

    def read_temp_esp32(self):
        
        ds_pin = machine.Pin(self.DS18B20_pin)
        ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))
        roms = ds_sensor.scan()
        ds_sensor.convert_temp()
        utime.sleep_ms(self.DS18X20_READ_TIME)
        v_ret = []
        for rom in roms:
            sx = []
            s_id = ubinascii.hexlify(rom).decode("utf-8")
            sensor_id = s_id[:2] + '-' + s_id[4:]
            sensor_temp = '{:.1f}'.format(ds_sensor.read_temp(rom))
            sx.append(sensor_id)
            sx.append(sensor_temp)
            v_ret.append(sx)
        return v_ret

if __name__ == '__main__':
    
    my_ds18x20 = Ds18x20Esp32(13)
    temps = my_ds18x20.read_temp_esp32()
    print('-----------------------------------------------------------')
    for m in temps:
        print('sensor: ' + m[0] + ' -> température: ' + m[1])
    print('-----------------------------------------------------------')
