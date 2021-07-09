# import ntptime
import stemma_soil_sensor 
import utime
import machine, onewire, ds18x20, dht


SDA_PIN = const(21) # update this
SCL_PIN = const(22) # update this

def connect_and_subscribe():
    global client_id, mqtt_server 
    client = MQTTClient(client_id, mqtt_server)
    client.connect()
    print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic_pub))
    return client

def restart_and_reconnect():
    print('Failed to connect to MQTT broker. Reconnecting...')
    utime.sleep(10)
    machine.reset()

def read_soil():
    try:
        # connect I2C and read the moisture and temperature
        i2c = machine.SoftI2C(sda=machine.Pin(SDA_PIN), scl=machine.Pin(SCL_PIN), freq=400000)
        seesaw = stemma_soil_sensor.StemmaSoilSensor(i2c)
        # get sensor data
        moisture = seesaw.get_moisture()
        temperature = seesaw.get_temp()
        return 0, moisture, temperature
    except:
        print ('soil error')
        restart_and_reconnect()
        return 1, 0

def read_temp_ds18b20(ds_pin):
    try:
        ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))
        roms = ds_sensor.scan()
        print(roms)
        ds_sensor.convert_temp()
        utime.sleep_ms(750)
        return 0, '{:.1f}'.format(ds_sensor.read_temp(roms[0]))
    except:
        print('DS18B20 error')
        restart_and_reconnect()
        return 1, 0

def read_air_humidity(dh_pin):
    try:
        dht11_sensor = dht.DHT11(dh_pin)
        dht11_sensor.measure()
        dht11_temperature = '{:.1f}'.format(dht11_sensor.temperature())
        dht11_humidity = '{:.0f}'.format(dht11_sensor.humidity())
        return 0, dht11_temperature, dht11_humidity
    except:
        print('DHT11 error')
        restart_and_reconnect()
        return 1, 0, 0

def read_analog_voltage(analog_pin):
    try:
        ubat = machine.ADC(machine.Pin(analog_pin))
        ubat.atten(machine.ADC.WIDTH_12BIT)       #Full range: 3.3v
        bin_pin_measure = ubat.read()
        analog_pin_voltage = bin_pin_measure / 4096 * 3.3
        return 1, analog_pin_voltage
    except:
        print('Analog1 error')
        restart_and_reconnect()
        return 0, 1
        


if __name__ == '__main__':

    i = 0
    while True:
        i+= 1
        
        try:
            print('try connect')
            client = connect_and_subscribe()
        except:
            restart_and_reconnect()

    #     blink the blue led
        print('led on')
        led = machine.Pin(2, machine.Pin.OUT)
        led.on()

        t_pre_pause = const(10)
        t_pause_minute = const(1)
        t_pause = const((t_pause_minute * 60 - t_pre_pause) * 1000)

        # read the battery charge status
        print('analog read')
        analog_pin = 35
        bat_voltage = read_analog_voltage(analog_pin)
        str_bat =  ' bat:' +  '{:.2f}'.format((bat_voltage[1]*133/33)+0.6)
        
        # get soil moisture
        print('moisture read')
        error, soil_moisture, soil_temperature = read_soil()
        
        if error == 0:
            # prepare the message
            str_soil_temperature = 'soil temp:' + '{:.1f}'.format(soil_temperature)
            str_soil_moisture = 'soil moist:' + '{:.0f}'.format(soil_moisture)
        else:
            restart_and_reconnect()
            
        # get temperature DS18B20
        print('ds18b20 read')
        ds_pin = machine.Pin(13)
        error, ds18b20_temperature = read_temp_ds18b20(ds_pin)
        if error == 0:
            str_ds18b20_temperature = 'ds18b20 temp:' + ds18b20_temperature
        else:
            restart_and_reconnect()
            
            
        # get DHT11 air humidity and temperature
        print('dht11 read')
        ds_pin = machine.Pin(14)
        error, dht11_temperature, dht11_humidity = read_air_humidity(ds_pin)
        if error == 0:
            str_dht11_temperature = 'DHT1 temp:' + dht11_temperature
            str_dht11_humidity = 'air humidity:' + dht11_humidity
        else:
            restart_and_reconnect()
        
            
        msg = ''.join([str(i) +' -> msg from garden ->, ', str_soil_moisture, ', ', str_dht11_humidity, ", ", \
                       str_soil_temperature, ", " , str_dht11_temperature, ", " , str_ds18b20_temperature, ", ", str_bat])
        print(msg)
        #publish the message
        client.publish(topic_pub, msg)

        # enter in sleeping mode
        led.off()
        print('going to sleep', str(t_pre_pause), 's')
        utime.sleep(t_pre_pause)
    #     print('going to deep sleep', str(t_pause_minute) , 'min')
        print('-------------------------\n')
    #     machine.deepsleep(t_pause)


