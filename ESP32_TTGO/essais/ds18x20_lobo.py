from machine import Onewire
from time import sleep

ds=[]
ow = Onewire(13)  # Initialize onewire & DS18B20 temperature sensor
print(ow)

ds0 = Onewire.ds18x20(ow, 0)
ds1 = Onewire.ds18x20(ow, 1)

print('OW', ow)
print('DS', ds)
print('ow.scan()', ow.scan())

def get_temp_lobo():
    try:
        while True:
            temp0 = ds0.convert_read()
            print("Temperature0: {0:.1f}°C".format(temp0))
            temp1 = ds1.convert_read()
            print("Temperature1: {0:.1f}°C".format(temp1))
            print('\n')
            sleep(4)
    except KeyboardInterrupt:
        print('\nCtrl-C pressed.  Cleaning up and exiting...')
    finally:
        ds0.deinit()
        ds1.deinit()
        ow.deinit()

get_temp_lobo()

