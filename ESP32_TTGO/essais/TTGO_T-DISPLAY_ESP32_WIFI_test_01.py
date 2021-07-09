# 1.14 inch color display test
#
# Tutorial
# https://www.instructables.com/id/TTGO-color-Display-With-Micropython-TTGO-T-display/
#
#
# Loboris Wiki
# https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo/wiki

import machine, display, network

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

text = "ESP32 with Micropython!"
tft.set_bg(0xFFFFFF)
tft.text(
    120-int(tft.textWidth(text)/2),
    20-int(tft.fontSize()[1]/2),
    text,
    0x000000,
)

wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect("jmb-guest", "pravidondaz")
while not wifi.isconnected():
    pass
ip = wifi.ifconfig()[0]
print('connected to WIFI jmb_guest on ip: ', ip)

tft.text(
    120-int(tft.textWidth(ip)/2),
    40-int(tft.fontSize()[1]/2),
    ip,
    0x000000,
)
print('ip displayed')

tft.text(
    120-int(tft.textWidth(ip)/2),
    60-int(tft.fontSize()[1]/2),
    str(tft.fontSize()),
    0x000000,
)
print('font-size displayed', str(tft.fontSize()))

# https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo/wiki/telnetserver
network.telnet.start(user="m", password="m")

tft.clear()
tft.font(tft.FONT_7seg)
# tft.attrib7seg(2, 2, tft.RED, tft.RED)
tft.text(tft.CENTER, tft.CENTER, '32.8 °C', tft.YELLOW)
print('7seg displayed: 32.8 °C')

