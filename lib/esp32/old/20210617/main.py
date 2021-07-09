#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
project : lib_jo_demo.py
----------------------------
example of use DS18B20, DHT11, DHT22, seesaw i2c soil sensor with jo's lib

CLASS : lib_jo_demo
PROCESSOR : ESP32
OS : micropython
uC : WEMOS MINI D1

24.05.2021
jmb52.dev@gmail.com
"""
import dhtxx_esp32
import ds18x20_esp32
import rtc_esp32
import wifi_esp32
import voltage_esp32
import stemma_soil_sensor
import umqttsimple2_jo
import time
import machine
import ubinascii

# analog voltage measurement
R1 = 100e3 # first divider bridge resistor
R2 = 100e3 # second divider bridge resistor
ANALOG_PIN = 34 # Measure of analog voltage (ex: battery voltage following)
# temperature and humidity sensors
DS18B20_PIN = 13 # DS18B20 temperature sensors
DHT22_PIN_1 = 15 # DHT11 temperature ans humidity air sensor
DHT22_PIN_2 = 16 # DHT22 temperature and humidity air sensor (better precision and resolution)
# HW390soil sensor
HW390_PIN_1 = 35 # soil humidity sensor
HW390_PIN_2 = 36 # soil humidity sensor
# I2C initialisation
SDA_PIN = 21 # I2C SDA_PIN
SCL_PIN = 22 # I2C SCL_pin
i2c = machine.SoftI2C(sda=machine.Pin(SDA_PIN), scl=machine.Pin(SCL_PIN), freq=400000) 
# Mosquitto MQTT params
MQTT_BROKER = '192.168.1.108'
MQTT_TOPIC_PUB = 'lib_jo_demo'
MQTT_CLIENT_ID = ubinascii.hexlify(machine.unique_id())
# WIFI params
WIFI_SSID = 'jmb-home'
WIFI_PW = 'lu-mba01'
# LED settings
INTERNAL_LED = machine.Pin(2, machine.Pin.OUT)


def mqtt_connect(client_id, mqtt_broker):
    mqtt_client = umqttsimple2_jo.MQTTClient(client_id, mqtt_broker)
    mqtt_client.connect()
    return mqtt_client

if __name__ == '__main__':
    
    # WIFI and mosquitto MQTT connection
    print('-----------------------------------------------------------')
    my_wifi = wifi_esp32.WifiEsp32(WIFI_SSID, WIFI_PW)
    my_wifi.connect_wifi()
    mqtt_client = mqtt_connect(MQTT_CLIENT_ID, MQTT_BROKER)
    print('MQTT mqtt_client connected on ' + MQTT_BROKER + ' with the topic "' + MQTT_TOPIC_PUB + '"')
    print('-----------------------------------------------------------')

    # Real time clock (RTC) initialisation
    my_rtc = rtc_esp32.RtcEsp32()  # initialize the class
    my_rtc.rtc_init()  # initialize the rtc with local date and time
    
    # external classes initialisation
    my_ds18x20 = ds18x20_esp32.Ds18x20Esp32(DS18B20_PIN) # DS18B20 temperature sensors
    my_dhtxx = dhtxx_esp32.DhtxxEsp32() # DHT11 and DHT22 air temperature and humidity sensors
    my_seesaw = stemma_soil_sensor.StemmaSoilSensor(i2c) # seesaw soil humidity and temperature sensor
    my_HW390_soil_1 = voltage_esp32.VoltageEsp32(HW390_PIN_1) # HW390 soil humidity sensor 1
    my_HW390_soil_2 = voltage_esp32.VoltageEsp32(HW390_PIN_2) # HW390 soil humidity sensor 2
    my_divider_voltage = voltage_esp32.VoltageEsp32(ANALOG_PIN, R1, R2) # for battery voltage
    
    passe = 1
    while True:
        
        INTERNAL_LED.on() # blue led on
        # message initialisation with pass nr and datetime
        msg = 'Passe: ' + str(passe) + '\n'
        now = my_rtc.rtc_now()  # get date and time
        datetime_formated = my_rtc.format_datetime(now)
        txt = "now date and time :" + datetime_formated + '\n'
        msg += txt

        # DS18B20 temperature sensors
        temps = my_ds18x20.read_temp_esp32() # read all the sensors connected to the GPIO DS18B20_PIN
        for m in temps:
            txt = 'ds18b20 sensor: ' + m[0] + ' - temperature = ' + m[1] + ' C\n'
            msg += txt

        # DHT22_1 sensor
        t, h = my_dhtxx.read_dht22(DHT22_PIN_1)
        txt =  'DHT22_1 sensor pin:' + str(DHT22_PIN_1) + ' temperature = %3.1f C' %t + ' - humidity = %3.0f' %h + '\n'
        msg += txt
        
        # DHT22 sensor
        t, h = my_dhtxx.read_dht22(DHT22_PIN_2)
        txt ='DHT22_2 sensor pin:' + str(DHT22_PIN_2) + ' temperature = %3.1f C' %t + ' - humidity = %3.0f' %h + '\n'
        msg += txt

        # Seesaw soil humidity and temperature sensor
        moisture_abs_val = my_seesaw.get_moisture()
        moisture_rel_val = 0.1333 * moisture_abs_val - 40
        txt = 'Seesaw soil sensor: humidity abs = %3.0f' %moisture_abs_val + ' - humidity rel = %3.0f%%' %moisture_rel_val + '\n'
        msg += txt
        
        # HW-390 soil sensor 1
        soil_moist_abs_val = my_HW390_soil_1.get_voltage()
        soil_moist_rel_val = -49.5 * soil_moist_abs_val + 149.5
        txt ='HW-390 soil sensor: soil_1 humidity abs =' + ' %3.2f' %soil_moist_abs_val + ' humidity rel =' + ' %3.2f%%' %soil_moist_rel_val + '\n'
        msg += txt
        
        # HW-390 soil sensor 2
        soil_humid_abs_val = my_HW390_soil_2.get_voltage()
        soil_moist_rel_val = -49.5 * soil_moist_abs_val + 149.5
        txt ='HW-390 soil sensor: soil_2 humidity abs =' + ' %3.2f' %soil_moist_abs_val + ' humidity rel =' + ' %3.2f%%' %soil_moist_rel_val + '\n'
        msg += txt
        
        # read the tension applied to the divider
        analog_in_voltage = my_divider_voltage.get_voltage()
        txt ='Battery : voltage on divider = %3.2fV' %analog_in_voltage + '\n'
        msg += txt
        txt = '-----------------------------------------------------------'
        msg += txt

        # publish to MQTT
        mqtt_client.publish(MQTT_TOPIC_PUB, msg)
        print(msg)
        
        INTERNAL_LED.off()
        time.sleep(30)
        passe += 1



