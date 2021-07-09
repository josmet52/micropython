import machine, display, time, math, network, utime
led = machine.Pin(15, machine.Pin.OUT)


tft = display.TFT()
tft.init(tft.ST7789,bgr=False,rot=tft.LANDSCAPE, miso=17,backl_pin=4,backl_on=1, mosi=19, clk=18, cs=5, dc=16)
tft.setwin(40,52,320,240)

for i in range(0,241):
    color=0xFFFFFF-tft.hsb2rgb(i/241*360, 1, 1)
    tft.line(i,0,i,135,color)

tft.set_fg(0x000000)
tft.ellipse(120,67,120,67)
tft.line(0,0,240,135)
text="ST7789 with micropython!"
tft.text(120-int(tft.textWidth(text)/2),67-int(tft.fontSize()[1]/2),text,0xFFFFFF)

wifi=network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect("jmb-guest","pravidondaz")
while wifi.isconnected() == False:
    pass
print('connected to ' + 'jmb-guest')

i = 0
led = machine.Pin(15, machine.Pin.OUT)
while True:
	led.value(1)
	time.sleep(1)
	led.value(0)
	time.sleep(1)
	print(i)
	i += 1
# 	print(i)
#     i += 1

# utime.sleep_ms(3000)
# network.telnet.start(user="m",password="m")

