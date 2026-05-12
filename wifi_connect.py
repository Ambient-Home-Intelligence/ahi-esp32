import network
import time

wlan = network.WLAN(network.STA_IF)
wlan.active(False)
time.sleep(2)
wlan.active(True)
time.sleep(2)
wlan.connect("ATTuGTqV7i_Guest", "test1234")

timeout = 0
while not wlan.isconnected() and timeout < 30:
    print("Connecting...")
    time.sleep(1)
    timeout += 1

print("Connected:", wlan.isconnected())
print("Config:", wlan.ifconfig())
