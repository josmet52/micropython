# connect to WIFI
ssid = 'jmb-guest'
password = 'pravidondaz'
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass
print('connected')




