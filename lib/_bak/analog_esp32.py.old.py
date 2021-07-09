#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
project : analog_esp32.py
----------------------------
sync analog in with calibration for a divider

CLASS : AnalogEsp
PROCESSOR : ESP32 
OS : micropython
uC : WEMOS MINI D1
VERSION: 0.0.1

27.05.2021
jmb52.dev@gmail.com
"""
import machine

class AnalogEsp32:
    
    def __init__(self, analog_pin):
        
        self.ANALOG_PIN = analog_pin
        self.R1 = 100e3
        self.R2 = 100e3
        self.Rgpio = 700
        with open ('param.txt', 'r') as f:
            for line in f.readlines():
                if line.strip() != '':
                    item = line.split('=')
                    if item[0] == 'Rgpio':
                        self.Rgpio = float(item[1].strip())
                    if item[0] == 'R1':
                        self.R1 = float(item[1].strip())
                    if item[0] == 'R2':
                        self.R2 = float(item[1].strip())
    
    def get_analog_voltage(self):

        ubat = machine.ADC(machine.Pin(self.ANALOG_PIN))
        ubat.atten(machine.ADC.WIDTH_12BIT)       #Full range: 3.3v
        bin_pin_measure = ubat.read()
        """ conversion D/A :
            4095 ^ 3.3V
        """
        analog_in_voltage =  3.3 * bin_pin_measure / 4095
        return analog_in_voltage
    
    def get_battery_voltage(self):

        ubat = machine.ADC(machine.Pin(self.ANALOG_PIN))
        ubat.atten(machine.ADC.WIDTH_12BIT)       #Full range: 3.3v
        bin_pin_measure = ubat.read()
        """ conversion D/A :
            4095 ^ 3.3V
        """
        R1 = self.R1  # R1 = 100k
        R2 = self.R2  # R1 = 100k
        Rgpio = self.Rgpio  # Rgpio = ~700k 
        Rp = (R2 * Rgpio) / (R2 + Rgpio)  # Rp = R2 // Rgpio
        diviseur = Rp / (R1 + Rp)  # diviseur = diviseur de la tension Analog in / Tesion à mesurer 
        analog_in_voltage =  3.3 * bin_pin_measure / 4095 / diviseur
#         return analog_in_voltage
        return bin_pin_measure / 4095 * 3.3 / R2 * (R1 + R2)
    
    def calibrate_Rgpio(self):
        
#         Uin = input('Entrez la tension appliquée aux bornes du diviseur: ')
        Uin = 4.64 #float(Uin)
        R1 = self.R1
        R2 = self.R2
        Rgpio = self.Rgpio
        
        ubat = machine.ADC(machine.Pin(self.ANALOG_PIN))
        ubat.atten(machine.ADC.WIDTH_12BIT)
        #Full range: 3.3v
        Umes = float(ubat.read() / 4095 * 3.3)
        numerateur = Umes * R1 * R2
        d1 = Uin * R2
        d2 = Umes * R1
        d3 = Umes * R2
        d23 = Umes * (R1 + R2)
        
        d = d1-d2-d3
        print(Uin, Umes, d1, d23, d)
        fraction = numerateur / d
        print('num:', numerateur, 'denom:', d, 'fract:', fraction)
        Rgpio = (Umes * R1 * R2) / (Uin * R2 - Umes * R1 - Umes * R2)
        Rgpio = (Umes * R1 * R2) / (Uin * R2 - Umes * R1 - Umes * R2)
#         self.Rgpio = (Umes * self.R1 * self.R2) / (Uin * self.R2 - Umes * self.R1 - Umes * self.R2)
#         self.Rgpio = (Umes * self.R1 * self.R2) / ((Uin * self.R2) - (Umes * (self.R1 + self.R2)))
        print('Ubat:', ubat.read(), 'Umes:', Umes, 'R1:', R1, 'R2:', R2, 'Rgpio:', Rgpio)
        self.Rgpio = Rgpio
        
        with open ('param.txt', 'r') as f:
            result = ''
            for line in f:
                if line.startswith('Rgpio'):
                    list = line.split('=') 
                    list[1] = str(self.Rgpio) + '\n'
                    line = "=".join(list)
                if line[0].strip() != '':
                    result += line
        with open ('param.txt', 'w') as f:
            f.write(result)
            
        return self.Rgpio

if __name__ == '__main__':

    my_analog_esp = AnalogEsp32(34)
    
#     choice = input("voulez-vous calibrer l'impédance de l'entrée analogique YN ?")
#     if choice.strip().upper() == 'Y':
    my_analog_esp.calibrate_Rgpio()
    
    print('-----------------------------------------------------------')
    print('R1 = ' + str(my_analog_esp.R1))
    print('R2 = ' + str(my_analog_esp.R2))
    print('gpio analog input impedance:', my_analog_esp.Rgpio)
    print('analog tension after calibration:', my_analog_esp.get_battery_voltage())
    print('-----------------------------------------------------------')
