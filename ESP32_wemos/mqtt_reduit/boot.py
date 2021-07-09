# project mqtt_temp
# 05.04.2021
# J. Metrailler

#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()

import network
import esp
esp.osdebug(None)
import gc
gc.collect()

# connect to WIFI
ssid = 'jmb-home'
password = 'lu-mba01'
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)
while station.isconnected() == False:
    pass
