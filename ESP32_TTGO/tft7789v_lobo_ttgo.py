# project ttgo_tdisp_temp
# 05.04.2021
# J. Metrailler

import machine
import display
import time

DS18X20_PIN = const(13) 
ow = machine.Onewire(DS18X20_PIN)  # Initialize onewire & DS18B20 temperature sensor

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
    # If you want to turn off the display,
    # simply run the tft.init again with backl_on=0
    tft = display.TFT()
    tft.init(tft.ST7789, bgr=False, rot=tft.LANDSCAPE, miso=17, backl_pin=4, backl_on=1, mosi=19, clk=18, cs=5, dc=16,)

    # corrections des erreurs de loboris micropython
    tft.tft_writecmd(0x21) # correct the colors
    tft.setwin(40, 52, 279, 186) # adjust the size of the windows for the display 135x240
    # get the real size of the tft
    tft_width, tft_height = tft.winsize()
    # draw a rectangle 
    margin = 0
    tft.rect(margin, margin, tft_width-margin, tft_height-margin, tft.RED)

    txt = "ESP32 with Micropython!\n"
    tft.text(int(tft_width/2)-int(tft.textWidth(txt)/2), int(tft_height/4)-int(tft.fontSize()[1]/2), txt, 0xFFFFFF,)
    time.sleep(3)

    tft.clear()
    tft.font(tft.FONT_Comic)

    txt_height = int(tft.fontSize()[1])
    top_pos = int(txt_height/2)

    # displax text for sensors
    temp = get_temp_lobo()
    nbre_sensors = str(len(temp))
    # read the temperatures
    k = 0
    while True:
        tft.clear()
        txt = nbre_sensors + ' ds18b20 actif(s)'
        tft.text(0, top_pos + txt_height * 0 - int(tft.fontSize()[1]/2), txt, 0xFFFFFF)
        txt = 'passe : ' + str(k)
        tft.text(0, top_pos + txt_height * 1 - int(tft.fontSize()[1]/2), txt, 0xFFFFFF)
        k += 1
        temp = get_temp_lobo()
        
        for i, t in enumerate(temp):
            sensor_id = t[0][:5] + '..' + t[0][-4:] + ' ='
            sensor_val = t[1]
            txt = sensor_id + ' ' + sensor_val
            tft.text(0, top_pos + txt_height * (i + 2) - int(tft.fontSize()[1]/2), txt, 0xFFFFFF)
            print(txt)
        print()

        time.sleep(60)

# initialize the ds18x20 sensors
roms = []
for i, rom in enumerate (ow.scan()):
    if rom[-2:] == '10' or rom[-2:] == '28':
        r2 = rom[-2:] + '-' + rom[:-4]
        roms.append([r2, machine.Onewire.ds18x20(ow, i)])
# run the programm
main()