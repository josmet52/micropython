#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
project : lib_rtc_lobo_ttgo.py
----------------------------
sync rtc with internet

CLASS : rtc_ttgo_esp32
PROCESSOR : ESP32
OS : loboris micropython
uC : TTGO T-DISPLAY ESP32
Display type : ST 7789V 135x240

21.05.2021
jmb52.dev@gmail.com
"""
import network
import machine
import utime
from wifi_esp32 import wifi

class rtc_ttgo_esp32:
    
    def __init__(self):
        self.TIMEZONE_CORRECTION = '-1'  # 3600 secondes par heure de décalage

    def rtc_init(self): 
        rtc = machine.RTC()
        rtc.ntp_sync(server='pool.ntp.org', tz='<UTC' + self.TIMEZONE_CORRECTION + '>')
        self.rtc = rtc
        
        # check the connection
        tmo = 100
        while not rtc.synced():
           utime.sleep_ms(100)
           tmo -= 1
           if tmo == 0:
               print('rtc sync breaked')
               break
        print('RTC synced -> ' + str(rtc.synced()))
    
    def rtc_now(self):
        return self.rtc.now()
        
    def connect_wifi(self):
        ssid = self.WIFI_SSID 
        password = self.WIFI_PW 
        station = network.WLAN(network.STA_IF)
        station.active(True)
        station.connect(ssid, password)

        # check connection
        tmo = 100
        while not station.isconnected():
           utime.sleep_ms(100)
           tmo -= 1
           if tmo == 0:
               print('wifi connection breaked')
               break
        print('wifi connected on ' + self.WIFI_SSID + ' -> ' + str(station.isconnected()))
        
    def format_datetime(self, dt):
        year = "{:04d}".format(dt[0])
        month = "{:02d}".format(dt[1])  
        day = "{:02d}".format(dt[2])   
        hour = "{:02d}".format(dt[3])
        minute = "{:02d}".format(dt[4])
        second = "{:02d}".format(dt[5])
        return day + '.' + month + '.' + year + ' ' + hour + ':' + minute + ':' + second 
       
    
# demo prg for this class
if __name__ == '__main__':
    
    print('---------------------------------------------------------')
    my_rtc = rtc_ttgo_esp32()  # initialize the class
    my_wifi = wifi('jmb-guest', 'pravidondaz')
    my_wifi.connect_wifi()
#     my_rtc.connect_wifi()  # connect to the wifi network
    my_rtc.rtc_init()  # initialize the rtc with local date and time
    print('---------------------------------------------------------')
        
    while True:
        # extract the date and time values in str format and print it
        now = my_rtc.rtc_now()  # get date and time
        datetime_formated = my_rtc.format_datetime(now)
        print("now date and time :", datetime_formated)
        utime.sleep(10)

