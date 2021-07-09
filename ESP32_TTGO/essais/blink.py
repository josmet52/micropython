import utime
from machine import Pin
led=Pin(15,Pin.OUT)
led = machine.Pin(15, machine.Pin.OUT)
 
i = 0
while True:
  led.on()
  utime.sleep(0.5)
  led.off()
  utime.sleep(0.5)
  print(i)
  i += 1
  


