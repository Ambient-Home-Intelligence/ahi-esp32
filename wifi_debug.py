import network
import time

wlan = network.WLAN(network.STA_IF)
wlan.active(False)
time.sleep(2)
wlan.active(True)
time.sleep(2)
wlan.connect('ATTuGTqV7i', 'fqmc.5h=dm3w')
time.sleep(20)
print('Status:', wlan.status())
print('Connected:', wlan.isconnected())
print('Config:', wlan.ifconfig())
