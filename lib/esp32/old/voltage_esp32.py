#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
project : voltage_esp32.py
----------------------------
voltage measurement with and without divider bridge 

CLASS : VoltageEsp32
PROCESSOR : ESP32 
OS : micropython
uC : WEMOS MINI D1
VERSION : 1.0.0
DATE : 12.06.2021
jmb52.dev@gmail.com
"""
import machine

class VoltageEsp32:
    
    def __init__(self):
        
        self.R1 = 0
        self.R2 = 1e12
        self.Rgpio = 1e12
        try:
            with open ('voltage_esp32_param.txt', 'r') as f:
                for line in f.readlines():
                    if line.strip() != '':
                        item = line.split('=')
                        if item[0] == 'Rgpio':
                            self.Rgpio = float(item[1].strip())
                        if item[0] == 'R1':
                            self.R1 = float(item[1].strip())
                        if item[0] == 'R2':
                            self.R2 = float(item[1].strip())
        except:
            with open ('voltage_esp32_param.txt', 'w') as f:
                f.write('R1=' + str(self.R1) + '\n')
                f.write('R2=' + str(self.R2) + '\n')
                f.write('Rgpio=' + str(self.Rgpio) + '\n')
                

    def calibrate_Rgpio(self, analog_pin):
        
        Uin = float(input('Entrez la tension appliquée aux bornes du diviseur: '))
        R1 = self.R1
        R2 = self.R2
        Rgpio = self.Rgpio
        
        ubat = machine.ADC(machine.Pin(analog_pin))
        ubat.atten(machine.ADC.WIDTH_12BIT)
        #Full range: 3.3v
        Umes = float(ubat.read() / 4095 * 3.3)
        if (Uin * R2 - Umes * R1 - Umes * R2) <= 0:
            Rgpio = 1e12
        else:
            Rgpio = (Umes * R1 * R2) / (Uin * R2 - Umes * R1 - Umes * R2)
        self.Rgpio = Rgpio
        
        with open ('voltage_esp32_param.txt', 'r') as f:
            result = ''
            for line in f:
                if line.startswith('Rgpio'):
                    list = line.split('=') 
                    list[1] = str(self.Rgpio) + '\n'
                    line = "=".join(list)
                if line[0].strip() != '':
                    result += line
        with open ('voltage_esp32_param.txt', 'w') as f:
            f.write(result)
            
        return self.Rgpio
    
    def get_voltage(self, analog_pin, R1=0, R2=1e12):

        ubat = machine.ADC(machine.Pin(analog_pin))
        ubat.atten(machine.ADC.WIDTH_12BIT)
        bin_measure = ubat.read()
        """ full range 12 bits = 3.3V
            conversion D/A : 12 bits ^ 0xFFF ^ 4095 ^ 3.3V
        """
        if R1 == 0:
            analog_in_voltage =  bin_measure / 0xFFF * 3.3 
        else:
            Rp = (self.R2 * self.Rgpio) / (self.R2 + self.Rgpio)  # Rp = R2 // Rgpio
            diviseur = Rp / (self.R1 + Rp)  # diviseur = diviseur de la tension Analog in / Tesion à mesurer
            analog_in_voltage =  bin_measure / 0xFFF * 3.3 / diviseur
        return analog_in_voltage


if __name__ == '__main__':

    ANALOG_IN_PIN_0 = 34
    R1 = 100e3
    R2 = 100e3
    
    print('-----------------------------------------------------------')
    print('With divider bridge')
    # measure with a divider bridge R1-R2
    my_voltage = VoltageEsp32() # Uin max = 3.3 * (R1+R2)/R2
    my_voltage.calibrate_Rgpio(ANALOG_IN_PIN_0)
    R1 = my_voltage.R1
    R2 = my_voltage.R2
    if R1 != 0:
        print('R1 = ' + str(R1))
        print('R2 = ' + str(R2))
    print('Voltage on divider (PIN ' + str(ANALOG_IN_PIN_0) + ') = ' + '{:.2f}V'.format(my_voltage.get_voltage(ANALOG_IN_PIN_0, R1, R2)))
    
    # undiveded voltage example
    # measure without divider bridge --> omit params R1 and R2
    ANALOG_IN_PIN_1 = 34
    print('-----------------------------------------------------------')
    print('Without divider bridge')
    print('Voltage on PIN ' + str(ANALOG_IN_PIN_0) + ' = ' + '{:.2f}V'.format(my_voltage.get_voltage(ANALOG_IN_PIN_0)))
    print('-----------------------------------------------------------')
