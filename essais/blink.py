import utime
import machine
INTERNAL_LED = machine.Pin(15, machine.Pin.OUT)
 
while True:
    INTERNAL_LED.on()
    time.sleep(0.5)
    INTERNAL_LED.off()
    time.sleep(0.5)

