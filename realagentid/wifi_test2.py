import network
import time

wlan = network.WLAN(network.STA_IF)
wlan.active(False)
time.sleep(3)
wlan.active(True)
time.sleep(3)
wlan.connect("ATTuGTqV7i_Guest", "test1234")

timeout = 0
while not wlan.isconnected() and timeout < 60:
    print(timeout, wlan.status())
    time.sleep(1)
    timeout += 1

print("Result:", wlan.isconnected())
print("IP:", wlan.ifconfig())
