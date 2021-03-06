import machine
from onewire import OneWire

class DS18X20(object):
    
    def __init__(self, pin):
        self.ow = OneWire(pin)
        # Scan the 1-wire devices, but only keep those which have the
        # correct # first byte in their rom for a DS18x20 device.
        self.roms = [rom for rom in self.ow.scan() if rom[0] == 0x10 or rom[0] == 0x28]

    def read_temp(self, rom=None):
        """
        Read and return the temperature of one DS18x20 device.
        Pass the 8-byte bytes object with the ROM of the specific device you want to read.
        If only one DS18x20 device is attached to the bus you may omit the rom parameter.
        """
        rom = rom or self.roms[0]
        ow = self.ow
        ow.reset()
        ow.select_rom(rom)
        ow.write_byte(0x44)  # Convert Temp
        while True:
            if ow.read_bit():
                break
        ow.reset()
        ow.select_rom(rom)
        ow.write_byte(0xbe)  # Read scratch
        data = ow.read_bytes(9)
        return self.convert_temp(rom[0], data)

    def read_temps(self):
        """
        Read and return the temperatures of all attached DS18x20 devices.
        """
        temps = []
        for rom in self.roms:
            temps.append(self.read_temp(rom))
        return temps

    def convert_temp(self, rom0, data):
        """
        Convert the raw temperature data into degrees celsius and return as a float.
        """
        temp_lsb = data[0]
        temp_msb = data[1]
        if rom0 == 0x10:
            if temp_msb != 0:
                # convert negative number
                temp_read = temp_lsb >> 1 | 0x80  # truncate bit 0 by shifting, fill high bit with 1.
                temp_read = -((~temp_read + 1) & 0xff) # now convert from two's complement
            else:
                temp_read = temp_lsb >> 1  # truncate bit 0 by shifting
            count_remain = data[6]
            count_per_c = data[7]
            temp = temp_read - 0.25 + (count_per_c - count_remain) / count_per_c
            return temp
        elif rom0 == 0x28:
            return (temp_msb << 8 | temp_lsb) / 16
        else:
            assert False

DS18X20_PIN = const(13) 
DS18X20_READ_TIME = 750

# Lhelp()ED = machine.Pin(BLUE_LED_PIN, machine.Pin.OUT)
ds_pin = machine.Pin(DS18X20_PIN, machine.Pin.OUT)
ds18x20 = DS18X20(ds_pin)
print(ds18x20.read_temps())



