# project mqtt_temp
# 05.04.2021
# J. Metrailler

import utime
import machine
import onewire
import ds18x20
import ubinascii
from umqttsimple import MQTTClient

DS18X20_PIN = const(13) 
DS18X20_READ_TIME = 750

BLUE_LED_PIN = const(2)
LED = machine.Pin(BLUE_LED_PIN, machine.Pin.OUT)

MQTT_SERVER = '192.168.1.108'
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
TOPIC_PUB = 'reduit_'

T_SAVE_SECONDS = const(5)
T_MEASURE_INTERVAL_SECONDS = const(30)
T_MEASURE_INTERVAL_MINUTES = const(0)
T_MEASURE_INTERVAL_HOURS = const(0)
T_MEASURE_INTERVAL_DAYS = const(0)
T_DEEPSLEEP_MILLISECONDS = (max(T_MEASURE_INTERVAL_SECONDS \
                                + T_MEASURE_INTERVAL_MINUTES*60 \
                                + T_MEASURE_INTERVAL_HOURS*3600 \
                                + T_MEASURE_INTERVAL_DAYS*86400, 0) - T_SAVE_SECONDS) * 1000

def restart_and_reconnect(i, err_msg):
    msg = str(i) + ' - restart and reconnect: ' + err_msg
    print(msg)
    with open('error.txt' , 'a') as f:
        f.write(msg+'\n')
    utime.sleep(10)
    machine.reset()

def connect_and_subscribe(i):
    try:
        client = MQTTClient(CLIENT_ID, MQTT_SERVER)
        client.connect()
        print('Connected to %s MQTT broker, published to "%s" topic' % (MQTT_SERVER, TOPIC_PUB))
        return client
    except:
        err_msg = 'MQTT broker connection error'
        restart_and_reconnect(i, err_msg)

def read_many_ds18x20(i):
    try:
        ds_pin = machine.Pin(DS18X20_PIN)
        ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))
        roms = ds_sensor.scan()
        ds_sensor.convert_temp()
        utime.sleep_ms(DS18X20_READ_TIME)
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
    except:
        err_msg = 'ds18b20 sensor error'
        restart_and_reconnect(i, err_msg)
        
def publish_to_domoticz(client, idx, value):
    
    DOMOTICZ_TOPIC = "domoticz/in"
    msg = '{ "idx" : '+ str(idx) + ', "nvalue" : 0, "svalue" : "' + value + '" }'
    client.publish(DOMOTICZ_TOPIC, msg)
    print(DOMOTICZ_TOPIC, msg)


def main():

    # blink the blue led
    LED.on()
    if machine.reset_cause() == machine.DEEPSLEEP_RESET:
        print('woke from a deep sleep')
    else:
        print('power on or hard reset')
    # pass counter
    try:
        with open ('index.txt', 'r') as f:
            i = int(f.readline()) + 1
    except:
        i = 1
    with open ('index.txt', 'w') as f:
        f.write(str(i))
    # connect to MQTT
    client = connect_and_subscribe(i)
    # read temperatures
    l_temp = read_many_ds18x20(i)
    for j, t in enumerate(l_temp):
        topic = TOPIC_PUB  + '{:02x}'.format(j)
        msg = '"' + t[1] + '"'
        print(topic, msg)
        #publish the message 
        client.publish(topic, msg)
    # disconnect
    
    # DOMOTICZ
#     topic = "domoticz/in"
    for j, t in enumerate(l_temp):
        idx = j + 1
        value = t[1]
        publish_to_domoticz(client, idx, value)

    print('-----------------------------------------------------------------------------------')
    
    client.disconnect()
    # enter in sleeping mode
    LED.off()
    utime.sleep(T_SAVE_SECONDS)
    machine.deepsleep(T_DEEPSLEEP_MILLISECONDS)

main()


