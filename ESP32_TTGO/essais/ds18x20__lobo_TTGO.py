from machine import Onewire
from time import sleep
import ubinascii
import machine

DS18X20_PIN = const(13) 
ow = Onewire(DS18X20_PIN)  # Initialize onewire & DS18B20 temperature sensor
roms = []

def get_temp_lobo():
    
    v_ret = []
    for rom in roms:
        sx = []
        sensor_id = rom[0]
        sensor_temp = '{:.1f}'.format(rom[1].convert_read())
        sx.append(sensor_id)
        sx.append(sensor_temp)
        v_ret.append(sx)
    return v_ret
        
def main():

    for i, rom in enumerate (ow.scan()):
        if rom[-2:] == '10' or rom[-2:] == '28':
            r2 = rom[-2:] + '-' + rom[:-4]
            roms.append([r2, Onewire.ds18x20(ow, i)])
            
    while True:
        temp = get_temp_lobo()
        for t in temp:
            print('sensor: ' + t[0] + ' température: ' + t[1])
        print()
        sleep(5)
        
    for r in roms:
        r[1].deinit()
    ow.deinit()

main()
