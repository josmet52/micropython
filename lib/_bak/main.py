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
import umqttsimple2
import time
import machine
import ubinascii

# analog voltage measurement
R1 = 100e3 # first divider bridge resistor
R2 = 100e3 # second divider bridge resistor
ANALOG_PIN = 34 # Measure of analog voltage (ex: battery voltage following)
# temperature and humidity sensors
DS18B20_PIN = 13 # DS18B20 temperature sensors
DHT11_PIN = 15 # DHT11 temperature ans humidity air sensor
DHT22_PIN = 16 # DHT22 temperature and humidity air sensor (better precision and resolution)
HW390_PIN = 35 # soil humidity sensor
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
    mqtt_client = umqttsimple2.MQTTClient(client_id, mqtt_broker)
    mqtt_client.connect()
    return mqtt_client

if __name__ == '__main__':
    
    
    print('-----------------------------------------------------------')
    my_wifi = wifi_esp32.WifiEsp32(WIFI_SSID, WIFI_PW)
    my_wifi.connect_wifi()
    mqtt_client = mqtt_connect(MQTT_CLIENT_ID, MQTT_BROKER)
    print('MQTT mqtt_client connected on ' + MQTT_BROKER + ' with the topic "' + MQTT_TOPIC_PUB + '"')
    print('-----------------------------------------------------------')

    my_rtc = rtc_esp32.RtcEsp32()  # initialize the class
    my_rtc.rtc_init()  # initialize the rtc with local date and time
    
    my_ds18x20 = ds18x20_esp32.Ds18x20Esp32(DS18B20_PIN)
    my_dhtxx = dhtxx_esp32.DhtxxEsp32()
    my_seesaw = stemma_soil_sensor.StemmaSoilSensor(i2c)
    my_HW390_soil = voltage_esp32.VoltageEsp32(HW390_PIN)
    my_voltage = voltage_esp32.VoltageEsp32(ANALOG_PIN, R1, R2)
    
    passe = 1
    while True:
        
        msg = 'Passe: ' + str(passe) + '\n'
        INTERNAL_LED.on()
        now = my_rtc.rtc_now()  # get date and time
        datetime_formated = my_rtc.format_datetime(now)
        txt = "now date and time :" + datetime_formated + '\n'
        msg += txt

        temps = my_ds18x20.read_temp_esp32()
        for m in temps:
            txt = 'ds18b20 sensor: ' + m[0] + ' -> température = ' + m[1] + '\n'
            msg += txt

        t, h = my_dhtxx.read_dht11(DHT11_PIN)
        txt =  'DHT11 sensor pin:' + str(DHT11_PIN) + ' température = %3.1f°C' %t + ' humidity = %3.0f%%' %h + '\n'
        msg += txt
        
        t, h = my_dhtxx.read_dht22(DHT22_PIN)
        txt ='DHT22 sensor pin:' + str(DHT22_PIN) + ' température = %3.1f°C' %t + 'humidity = %3.0f%%' %h + '\n'
        msg += txt

        # get sensor data
        txt = 'Seesaw soil sensor:' + ' température = %3.1f°C' %my_seesaw.get_temp() + ' humidity = %3.0f' %my_seesaw.get_moisture() + '\n'
        msg += txt
        
        # HW-390 soil sensor
        soil_humid_val = my_HW390_soil.get_voltage()
        txt ='HW-390 soil humidity:' + ' %3.2f' %soil_humid_val + '\n'
        msg += txt
        
#         analog_input_impedance = my_analog.calibrate_Rgpio()
        analog_in_voltage = my_voltage.get_voltage()
        txt ='Analog in:' + ' tension = %3.2fV' %analog_in_voltage + '\n'
        msg += txt
        txt = '-----------------------------------------------------------'
        msg += txt

        mqtt_client.publish(ubinascii.hexlify(MQTT_TOPIC_PUB).decode('ascii'), ubinascii.hexlify(msg).decode('ascii'))
        print(msg)
        INTERNAL_LED.off()
        time.sleep(30)
        passe += 1
    mqtt_client.disconnect()



