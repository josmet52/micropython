# project ttgo_tdisp_temp
# 05.04.2021
# J. Metrailler

# 1.14 inch color display test
#
# Tutorial
# https://www.instructables.com/id/TTGO-color-Display-With-Micropython-TTGO-T-display/
#
#
# Loboris Wiki
# https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo/wiki

import machine, display, network, time

# https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo/wiki/display
tft = display.TFT()

# If you want to turn off the display,
# simply run the tft.init again with backl_on=0
tft.init(
    tft.ST7789,
    bgr=False,
    rot=tft.LANDSCAPE,
    miso=17,
    backl_pin=4,
    backl_on=1,
    mosi=19,
    clk=18,
    cs=5,
    dc=16,
)

# Sets the display border.
# The area you can use is (0,0,135,240)
tft.setwin(40, 52, 320, 240)

# RGB are inverted ???
# 0x000000 is white, 0x00FFFF is red...
# The wiki says other thing:
# https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo/wiki/display#colors

# The hue color gradient
for i in range(0, 241):
    color = 0xFFFFFF - tft.hsb2rgb(i/241*360, 1, 1)
    tft.line(i, 0, i, 135, color)

tft.set_fg(0xFFFFFF)
tft.ellipse(120, 67, 120, 67)
tft.line(0, 0, 240, 135)

txt = "ESP32 with Micropython!"
tft.set_bg(0xFFFFFF)
tft.text(
    120-int(tft.textWidth(txt)/2),
    43-int(tft.fontSize()[1]/2),
    txt,
    0x000000,
)

wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect("jmb-guest", "pravidondaz")
while not wifi.isconnected():
    pass
ip = wifi.ifconfig()[0]
txt = 'connected to WIFI "jmb_guest"\n on ip:' + str(ip)
tft.text(
    120-int(tft.textWidth(txt)/2),
    86-int(tft.fontSize()[1]/2),
    txt,
    0x000000,
)
print('connected to "jmb_guest" on ip:', ip)
time.sleep(2)
# https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo/wiki/telnetserver
# network.telnet.start(user="m", password="m")

tft.clear()
tft.font(tft.FONT_Comic)
# tft.attrib7seg(2, 2, tft.RED, tft.RED)
# for i in range(0, 240):
#     color=0xFFFFFF-tft.hsb2rgb(i/241*360, 1, 1)
#     print(color, tft.hsb2rgb(i/241*360, 1, 1))

while True:
    for i in range(-200, 0):
        tft.clear()
        txt = 'Congelo. ' + str(i/10) + ' °C' 
        tft.text(
            120-int(tft.textWidth(txt)/2),
            23-int(tft.fontSize()[1]/2),
            txt,
            0x0F0000
        )
        txt = 'Ambiance ' + str((i+200)/10) + ' °C'  
        tft.text(
            120-int(tft.textWidth(txt)/2),
            66-int(tft.fontSize()[1]/2),
            txt,
            0x0F0000
        )
        txt = 'Humidite ' + str((i+200)/2) + ' %'  
        tft.text(
            120-int(tft.textWidth(txt)/2),
            109-int(tft.fontSize()[1]/2),
            txt,
            0x0F0000
        )
        print(str(i))
        time.sleep(5)

