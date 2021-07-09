import display
tft = display.TFT()
tft.init(tft.ST7789,width=135,height=240,mosi=19,clk=18,cs=5,dc=16,miso=19,rst_pin=23,backl_pin=4,backl_on=1)
tft.rect(10,10,100,100,tft.RED,tft.BLUE)

i = 0
tft.init(tft.ST7789, width=320, height=240, rot=tft.LANDSCAPE, miso=17, mosi=19, clk=18, cs=5, dc=16, rst_pin=23, backl_pin=4, backl_on=1)
tft.setwin(40,52,279,186)
while True:
  print(str(i) + '\n')
  i += 1


tft.rect(0,0,20,20)
tft.rect(221,116,20,20,0xFF0000,0xFF0000)

print('end')
