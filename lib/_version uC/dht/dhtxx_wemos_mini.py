#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
project : dhtxx_wemos_mini.py
----------------------------
use the temperature and humidity sensors DHT11 or DHT22 with examples

CLASS : dhtxx_wemos_mini
PROCESSOR : ESP32
OS : micropython
uC : WEMOS MINI D1

22.05.2021
jmb52.dev@gmail.com
"""

import machine
import utime
import dht 

class dhtxx_wemos_mini:

    def read_dht11(self, pin):
        sensor = dht.DHT11(machine.Pin(pin))
        while True:
            utime.sleep(2)
            sensor.measure()
            t = sensor.temperature()
            h = sensor.humidity()
            return t, h

    def read_dht22(self, pin):
        sensor = dht.DHT22(machine.Pin(pin))
        while True:
            utime.sleep(2)
            sensor.measure()
            t = sensor.temperature()
            h = sensor.humidity()
            return t, h

if __name__ == '__main__':
    
    my_dhtxx = dhtxx_wemos_mini()
    while True:
        dht11_pin = 15
        t, h = my_dhtxx.read_dht11(dht11_pin)
        print( 'DHT11 pin:' + str(dht11_pin), 'Temperature: %3.1f°C' %t, 'Humidity: %3.0f%%' %h)
        
        dht22_pin = 16
        t, h = my_dhtxx.read_dht22(dht22_pin)
        print( 'DHT22 pin:' + str(dht22_pin), 'Temperature: %3.1f°C' %t, 'Humidity: %3.0f%%' %h)
        print()
        utime.sleep(5)
