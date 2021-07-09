#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
project : rtc_esp32.py
----------------------------
measure the temperature and humidity of ground of rhododendrons

PROCESSOR : ESP32 
OS : micropython
uC : WEMOS MINI D1

v1.0.0 -- 27.05.2021
v1.0.1 -- 10.06.2021 -- integration of analog_esp32 class
V1.1.0 -- 16.06.2021 -- integration of class for the sensors, created class Rhodo
jmb52.dev@gmail.com
"""
# import machine
# import esp32
# import onewire
# import ds18x20
# import ubinascii
# from umqttsimple import MQTTClient
# from analog_esp32 import analog_esp

import ds18x20_esp32
import rtc_esp32
import wifi_esp32
import voltage_esp32
import umqttsimple2_jo
import utime
import machine
import ubinascii
import esp32

# analog voltage measurement
R1 = 100e3 # first divider bridge resistor
R2 = 100e3 # second divider bridge resistor
BATTERY_VOLTAGE_MEASUREMENT_PIN = 33 # Measure of analog voltage (ex: battery voltage following)
# temperature and humidity sensors
DS18B20_PIN = 13 # DS18B20 temperature sensors
DHT22_PIN_1 = 15 # DHT11 temperature ans humidity air sensor
DHT22_PIN_2 = 16 # DHT22 temperature and humidity air sensor (better precision and resolution)
# HW390soil sensor
HW390_PIN_1 = 35 # soil humidity sensor
HW390_PIN_2 = 36 # soil humidity sensor
HW390_U100 = 0.88 # tension mesuree sur la sonde quand l'umidite de la terre est de 100%
HW390_U000 = 3 # tension mesuree sur la sonde quand l'umidite de la terre est de 100%
# HW390_PENTE = (HW390_100 - HW390_000) / 100
# I2C initialisation
SDA_PIN = 21 # I2C SDA_PIN
SCL_PIN = 22 # I2C SCL_pin
i2c = machine.SoftI2C(sda=machine.Pin(SDA_PIN), scl=machine.Pin(SCL_PIN), freq=400000) 
# Mosquitto MQTT params
MQTT_BROKER = '192.168.1.108'
MQTT_CLIENT_ID = ubinascii.hexlify(machine.unique_id())
MQTT_TOPIC_PUB = 'rhodo_'
# WIFI params
WIFI_SSID = 'jmb-home'
WIFI_PW = 'lu-mba01'
# LED settings
INTERNAL_BLUE_LED_PIN = 2
INTERNAL_BLUE_LED = machine.Pin(INTERNAL_BLUE_LED_PIN, machine.Pin.OUT)
SENSOR_ON_PIN = const(26) # activate sensors
WAKE_UP_PIN = const(27)

# deepsleep time
T_SAVE_SECONDS = const(5)
T_MEASURE_INTERVAL_SECONDS = const(20)
T_MEASURE_INTERVAL_MINUTES = const(0)
T_MEASURE_INTERVAL_HOURS = const(0)
T_MEASURE_INTERVAL_DAYS = const(0)
T_DEEPSLEEP_MILLISECONDS = (max(T_MEASURE_INTERVAL_SECONDS \
                                + T_MEASURE_INTERVAL_MINUTES*60 \
                                + T_MEASURE_INTERVAL_HOURS*3600 \
                                + T_MEASURE_INTERVAL_DAYS*86400, 0) - T_SAVE_SECONDS) * 1000

class Rhodo:
    
    def __init__(self):
        self.R1 = 100e3
        self.R2 = 33e3
        with open ('param.txt', 'r') as f:
            for line in f.readlines():
                if line.strip() != '':
                    items = line.split('=')
                    for item in items:
                        if item[0] == 'R1':
                            self.R1 = float(item[1].strip())
                        if item[0] == 'R2':
                            self.R2 = float(item[1].strip())
    
    def mqtt_connect(self, client_id, mqtt_broker):
        mqtt_client = umqttsimple2_jo.MQTTClient(client_id, mqtt_broker)
        mqtt_client.connect()
        return mqtt_client
    
    def restart_and_reconnect(self, err_msg):
        my_rtc = rtc_esp32.RtcEsp32()  # initialize the class
        msg = my_rtc.format_datetime(my_rtc.rtc_now()) + ' -> ' + err_msg
        print(msg)
        with open('error.txt' , 'a') as f:
            f.write(msg+'\n')
        utime.sleep(10)
        machine.reset()

    def connect_and_subscribe(self):
#         try:
            print('-----------------------------------------------------------')
            my_wifi = wifi_esp32.WifiEsp32(WIFI_SSID, WIFI_PW)
            my_wifi.connect_wifi()
            mqtt_client = rhodo.mqtt_connect(MQTT_CLIENT_ID, MQTT_BROKER)
            print('MQTT mqtt_client connected on ' + MQTT_BROKER + ' with the topic "' + MQTT_TOPIC_PUB + '"')
            # Real time clock (RTC) initialisation
            my_rtc = rtc_esp32.RtcEsp32()  # initialize the class
            my_rtc.rtc_init()  # initialize the rtc with local date and time
            txt = "now date and time :" + my_rtc.format_datetime(my_rtc.rtc_now()) + '\n'
            print('-----------------------------------------------------------')
            return mqtt_client
#         except:
#             err_msg = 'Mosquitto MQTT connect problem'
#             self.restart_and_reconnect(err_msg)
    
    def blink_internal_blue_led(self, t_on, t_off, n_repeat, t_pause):
        for n in range(n_repeat):
            INTERNAL_BLUE_LED.on()
            utime.sleep(t_on)
            INTERNAL_BLUE_LED.off()
            utime.sleep(t_off)
        utime.sleep(t_pause)


if __name__ == '__main__':
    
    # initialisation classe rhodo
    rhodo = Rhodo()
    # imported classes initialisation
    my_ds18x20 = ds18x20_esp32.Ds18x20Esp32(DS18B20_PIN) # DS18B20 temperature sensors
    my_HW390_soil_1 = voltage_esp32.VoltageEsp32(HW390_PIN_1) # HW390 soil humidity sensor 1
    my_divider_voltage = voltage_esp32.VoltageEsp32(BATTERY_VOLTAGE_MEASUREMENT_PIN, rhodo.R1, rhodo.R2) # for battery voltage
    
    # initialise wake-up by external gpio signal (push button)
    wake1 = machine.Pin(WAKE_UP_PIN, mode = machine.Pin.IN)
    esp32.wake_on_ext0(wake1, level = esp32.WAKEUP_ANY_HIGH)
    
    # sensors are deactivated during deep sleep so activate it before the measures
    sensor_onoff = machine.Pin(SENSOR_ON_PIN, machine.Pin.OUT)
    sensor_onoff.on()
    utime.sleep(2)
    
    # connect to mosquitto server
    rhodo.blink_internal_blue_led(t_on=0.2, t_off=0.2, n_repeat=3, t_pause=1)
    client = rhodo.connect_and_subscribe()
    INTERNAL_BLUE_LED.on() # blue led on
    
    # HW-390 soil moisture sensor 1
    soil_moist_abs_volt = my_HW390_soil_1.get_voltage()
    soil_moisture = (soil_moist_abs_volt - HW390_U000) / (HW390_U100 - HW390_U000) * 100
    topic = MQTT_TOPIC_PUB + 'sol_moist'
    value =  '{:.0f}'.format(soil_moisture)
    client.publish(topic, value)
    msg_all = value 
    print(topic, value)
    
    # SOIL AND AIR TEMPERATURE (DS18B20)
    # 28-4875d0013c27 = YELLOW = AIR
    # 28-4b75d0013cf5 = GREEN = GROUND
    ds18x20_temperatures = my_ds18x20.read_temp_esp32() # read all the sensors connected to the GPIO DS18B20_PIN
    for sensor in ds18x20_temperatures:
        s_id = sensor[0]
        s_val = sensor[1]
        if s_id == '28-4875d0013c27':
            topic = MQTT_TOPIC_PUB + 'air_temp'
            value = s_val
        elif s_id == '28-4b75d0013cf5':
            topic = MQTT_TOPIC_PUB + 'sol_temp'
            value = s_val
        msg_all += "," + value 
        client.publish(topic, value)
        print(topic, value)

    # BAT VOLTAGE
    # read the battery charge status
    bat_voltage = my_divider_voltage.get_voltage()
    topic = MQTT_TOPIC_PUB + 'bat'
    value = '{:.2f}'.format(bat_voltage)
    msg_all += "," + value 
#     client.publish(topic, value)
    print(topic, value)
    
    # ALL TOPICS
    topic = MQTT_TOPIC_PUB + 'all'
    value = msg_all
#     client.publish(topic, value)
    INTERNAL_BLUE_LED.off() # blue led off

    # enter in sleeping mode
    # disconnect the ground of the sensors
    sensor_onoff.off()
    utime.sleep(T_SAVE_SECONDS)
    if T_DEEPSLEEP_MILLISECONDS / 1000 < 60:
        msg = '{:.0f}'.format(T_DEEPSLEEP_MILLISECONDS / 1000) + ' sec'
    else:
        msg = '{:.0f}'.format(T_DEEPSLEEP_MILLISECONDS / 1000 / 60) + ' min'
        
    print('going to deep sleep '+ msg)
    print('-------------------------')
    rhodo.blink_internal_blue_led(t_on=0.2, t_off=0.2, n_repeat=3, t_pause=1)
    machine.deepsleep(T_DEEPSLEEP_MILLISECONDS)




