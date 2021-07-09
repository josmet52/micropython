#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
project : rtc_wemos_mini.py
----------------------------
sync rtc with internet

CLASS : rtc_wemos_mini
PROCESSOR : ESP32
OS : micropython
uC : WEMOS MINI D1

21.05.2021
jmb52.dev@gmail.com
"""
import network
import machine
import utime
import ntptime
from wifi_esp32 import wifi

class rtc_wemos_mini:
    
    def __init__(self):
        self.TIMEZONE_CORRECTION = 7200  # 3600 secondes par heure de décalage

    def rtc_init(self, year=0, month=0, day=0, hour=0, minute=0, second=0):
        rtc = machine.RTC()
        ntptime.settime()
        (year, month, mday, hour, minute, second, weekday, yearday)=utime.localtime(utime.time() + self.TIMEZONE_CORRECTION)
        rtc.datetime((year, month, mday, 0, hour, minute, second, 0))
    
    def rtc_now(self):
        return utime.localtime(utime.time())
        
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
    
    print('-----------------------------------------------------------')
    
    my_wifi = wifi('jmb-guest', 'pravidondaz')
    my_wifi.connect_wifi()
    
    my_rtc = rtc_wemos_mini()  # initialize the class
    my_rtc.rtc_init()  # initialize the rtc with local date and time
    print('-----------------------------------------------------------')
    while True:
        # extract the date and time values in str format and print it
        now = my_rtc.rtc_now()  # get date and time
        datetime_formated = my_rtc.format_datetime(now)
        print("now date and time :", datetime_formated)
        utime.sleep(10)

