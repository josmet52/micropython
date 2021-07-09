#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
project : dhtxx_lobo_ttgo.py
----------------------------
use the temperature and humidity sensors DHT11 or DHT22 with examples

CLASS : dhtxx_lobo_ttgo
PROCESSOR : ESP32
OS : loboris micropython
uC : WEMOS MINI D1

22.05.2021
jmb52.dev@gmail.com
"""

import machine
import utime

class dhtxx_wemos_mini:

    def read_dht11_lobo(self, pin11):
        dht = machine.DHT(machine.Pin(pin11), machine.DHT.DHT11)
        result, temperature, humidity = dht.read()
        return temperature, humidity

    def read_dht22_lobo(self, pin22):
        dht = machine.DHT(machine.Pin(pin22), machine.DHT.DHT2X)
        result, temperature, humidity = dht.read()
        return temperature, humidity

if __name__ == '__main__':
    
    my_dhtxx = dhtxx_wemos_mini()
    
    while True:
        dht11_pin = 13
        t, h = my_dhtxx.read_dht11_lobo(dht11_pin)
        print( 'DHT11 pin:' + str(dht11_pin), 'Temperature: %3.1f°C' %t, 'Humidity: %3.0f%%' %h)
        
        dht22_pin = 17
        t, h = my_dhtxx.read_dht22_lobo(dht22_pin)
        print( 'DHT22 pin:' + str(dht22_pin), 'Temperature: %3.1f°C' %t, 'Humidity: %3.0f%%' %h)
        print()
        utime.sleep(5)
