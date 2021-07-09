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
import hw390_esp32
import umqttsimple2_jo
import utime
import machine
import ubinascii
import adc1_cal

# analog voltage measurement
R1 = 100e3 # first divider bridge resistor
R2 = 33e3 # second divider bridge resistor
ADC1_PIN = 35 # Measure of analog voltage (ex: battery voltage following)
DIV       = R2 / (R1 + R2) # (R2 / R1 + R2) -> V_meas = V(R1 + R2); V_adc = V(R2)  
AVERAGING = 10                # no. of samples for averaging
ubatt = adc1_cal.ADC1Cal(machine.Pin(ADC1_PIN, machine.Pin.IN), DIV, None, AVERAGING, "ADC1 eFuse Calibrated")
# set ADC result width
ubatt.width(machine.ADC.WIDTH_12BIT)
# set attenuation
ubatt.atten(machine.ADC.ATTN_6DB)
# temperature and humidity sensors
DS18B20_PIN = 13 # DS18B20 temperature sensors
DHT22_PIN_1 = 15 # DHT11 temperature ans humidity air sensor
DHT22_PIN_2 = 16 # DHT22 temperature and humidity air sensor (better precision and resolution)
# HW390soil sensor
HW390_PIN_1 = 34 # soil humidity sensor
HW390_PIN_2 = 36 # soil humidity sensor
HW390_U100 = 1 # tension mesuree sur la sonde quand l'umidite de la terre est de 100%
HW390_U000 = 3 # tension mesuree sur la sonde quand l'umidite de la terre est de 100%
# HW390_PENTE = (HW390_100 - HW390_000) / 100
# I2C initialisation
SDA_PIN = 21 # I2C SDA_PIN
SCL_PIN = 22 # I2C SCL_pin
i2c = machine.SoftI2C(sda=machine.Pin(SDA_PIN), scl=machine.Pin(SCL_PIN), freq=400000) 
# Mosquitto MQTT params
MQTT_BROKER = '192.168.1.108'
MQTT_TOPIC_PUB = 'lib_jo_demo'
MQTT_RHODO_PUB = 'rhodo'
MQTT_CLIENT_ID = ubinascii.hexlify(machine.unique_id())
# WIFI params
WIFI_SSID = 'jmb-home'
WIFI_PW = 'lu-mba01'
# LED settings
INTERNAL_BLUE_LED = machine.Pin(2, machine.Pin.OUT)


def mqtt_connect(client_id, mqtt_broker):
    mqtt_client = umqttsimple2_jo.MQTTClient(client_id, mqtt_broker)
    mqtt_client.connect()
    return mqtt_client
    
def blink_internal_blue_led(self, ton, toff, nrepeat, tpause):
    led = machine.Pin(INTERNAL_BLUE_LED, machine.Pin.OUT)
    for n in range(nrepeat):
        led.on()
        utime.sleep(ton)
        led.off()
        utime.sleep(toff)
    time.sleep(tpause)

if __name__ == '__main__':
    
    # WIFI, mosquitto MQTT connection and RTC sync
    print('-----------------------------------------------------------')
    my_wifi = wifi_esp32.WifiEsp32(WIFI_SSID, WIFI_PW)
    my_wifi.connect_wifi()
    mqtt_client = mqtt_connect(MQTT_CLIENT_ID, MQTT_BROKER)
    print('MQTT mqtt_client connected on ' + MQTT_BROKER + ' with the topic "' + MQTT_TOPIC_PUB + '"')
    # Real time clock (RTC) initialisation
    my_rtc = rtc_esp32.RtcEsp32()  # initialize the class
    my_rtc.rtc_init()  # initialize the rtc with local date and time
    txt = "now date and time :" + my_rtc.format_datetime(my_rtc.rtc_now()) + '\n'
    print('-----------------------------------------------------------')
    
    # imported classes initialisation
    my_ds18x20 = ds18x20_esp32.Ds18x20Esp32() # DS18B20 temperature sensors
    my_dhtxx = dhtxx_esp32.DhtxxEsp32() # DHT11 and DHT22 air temperature and humidity sensors
    my_hw390_soil = hw390_esp32.Hw390Esp32() # HW390 soil humidity sensor 1
    
    passe = 1
    while True:
        
        INTERNAL_BLUE_LED.on() # blue led on
        # message initialisation with pass nr and datetime
        msg = 'Passe: ' + str(passe) + '\n'
#         now = my_rtc.rtc_now()  # get date and time
        datetime_formated = my_rtc.format_datetime(my_rtc.rtc_now())
        txt = "now date and time :" + datetime_formated + '\n'
        msg += txt

        # DS18B20 temperature sensors
        temps = my_ds18x20.read_temp_esp32(DS18B20_PIN) # read all the sensors connected to the GPIO DS18B20_PIN
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
        
        # HW-390 soil sensor 1
        soil_moist_rel_val_1 = my_hw390_soil.get_soil_moisture(HW390_PIN_1)
        if soil_moist_rel_val_1 != -1:
            txt ='HW-390 soil sensor 1: moisture rel = ' + '%3.2f%%' %soil_moist_rel_val_1 + '\n'
        else:
            txt ='HW-390 soil sensor 1: moisture rel = NA\n'
        msg += txt
        
        # HW-390 soil sensor 2
        soil_moist_rel_val_2 = my_hw390_soil.get_soil_moisture(HW390_PIN_2)
        if soil_moist_rel_val_2 != -1:
            txt ='HW-390 soil sensor 2: moisture rel = ' + '%3.2f%%' %soil_moist_rel_val_2 + '\n'
        else:
            txt ='HW-390 soil sensor 2: moisture rel = NA\n'
        msg += txt
        
        # read the tension applied to the divider
        u = ubatt.voltage / 1000
        txt ='Battery : voltage on divider = %3.2fV' %u + '\n'
        msg += txt

        # publish to MQTT
        mqtt_client.publish(MQTT_TOPIC_PUB, msg)
        print(msg)
        
        msg_rhodo = str(int(soil_moist_rel_val_2)) + ',' + temps[0][1] + ',' + temps[1][1] + ',' + '{:.1f}'.format(u)
        print(MQTT_RHODO_PUB + ' - soil moist=' + str(int(soil_moist_rel_val_2)) + '% air temp=' + temps[0][1] + ' sol temp=' + temps[1][1] + ' bat=' + '{:.1f}'.format(u) + 'V')
        mqtt_client.publish(MQTT_RHODO_PUB, msg_rhodo)
        print('-----------------------------------------------------------')
        
        INTERNAL_BLUE_LED.off()
        utime.sleep(60)
        passe += 1



