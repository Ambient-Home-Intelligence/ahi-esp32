import network
import time

wlan = network.WLAN(network.STA_IF)
wlan.active(False)
time.sleep(2)
wlan.active(True)
time.sleep(2)
wlan.connect('ATTuGTqV7i', 'fqmc.5h=dm3w')

timeout = 0
while timeout < 30:
    status = wlan.status()
    print('Status:', status)
    if wlan.isconnected():
        print('Connected!')
        print(wlan.ifconfig())
        break
    time.sleep(1)
    timeout += 1
