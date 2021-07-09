# project ttgo_tdisp_temp
# 05.04.2021
# J. Metrailler

import machine
import display
import time

DS18X20_PIN = const(13) 
ow = machine.Onewire(DS18X20_PIN)  # Initialize onewire & DS18B20 temperature sensor
ow.init()

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

# If you want to turn off the display,
# simply run the tft.init again with backl_on=0
tft = display.TFT()
tft.init(tft.ST7789, bgr=False, rot=tft.LANDSCAPE, miso=17, backl_pin=4, backl_on=1, mosi=19, clk=18, cs=5, dc=16,)
tft.setwin(40, 52, 320, 240)
# for i in range(0, 241):
#     color = 0xFFFFFF - tft.hsb2rgb(i/241*360, 1, 1)
#     tft.line(i, 0, i, 135, color)

# tft.set_fg(0xFFFFFF)
# tft.ellipse(120, 67, 120, 67)
# tft.line(0, 0, 240, 135)

txt = "ESP32 with Micropython!"
tft.set_bg(0xFFFFFF)
tft.text(
    120-int(tft.textWidth(txt)/2),
    43-int(tft.fontSize()[1]/2),
    txt,
    0x000000,
)
time.sleep(2)

tft.clear()
tft.set_bg(0xFFFFFF)
tft.set_fg(0xFFFFFF)
tft.font(tft.FONT_Comic)

# initialize the ds18x20 sensors
roms = []
for i, rom in enumerate (ow.scan()):
    if rom[-2:] == '10' or rom[-2:] == '28':
        r2 = rom[-2:] + '-' + rom[:-4]
        roms.append([r2, machine.Onewire.ds18x20(ow, i)])

while True:
    
    temp = get_temp_lobo()
    top_pos = 25
    for i, t in enumerate(temp):
        sensor_id = t[0][:3] + '...' + t[0][-4:] + ' ='
        sensor_val = t[1]
        txt = sensor_id + ' ' + sensor_val
        tft.text(
            120 - int(tft.textWidth(txt)/2),
            (top_pos * (i + 1)) - int(tft.fontSize()[1]/2),
            txt,
            0x0F0000
        )
        print(txt)
    print()

    time.sleep(5)

