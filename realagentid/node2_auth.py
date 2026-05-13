import network
import urequests
import hashlib
import ubinascii
import time
import ntptime

NODE_SECRET = "d0a4f1d06413a26e0ae2a4efa901ebd402f471e836818c28162aa11ada278cc0"
NODE_ID = "50a6b5714718a857"
HUB_IP = "192.168.1.124"
HUB_PORT = 5000

wlan = network.WLAN(network.STA_IF)
wlan.active(False)
time.sleep(2)
wlan.active(True)
time.sleep(1)
try:
    wlan.disconnect()
    time.sleep(2)
except:
    pass
wlan.connect("ATTuGTqV7i_5G", b"fqmc5h=#dm3w")

timeout = 0
while not wlan.isconnected() and timeout < 60:
    time.sleep(1)
    timeout += 1

if not wlan.isconnected():
    print("WiFi failed")
    raise SystemExit

print("WiFi connected:", wlan.ifconfig())
try:
    ntptime.settime()
    print("Time synced:", time.time())
except:
    print("NTP failed")

def sign_message(secret, message):
    key = bytes.fromhex(secret)
    msg = message.encode()
    block_size = 64
    if len(key) > block_size:
        key = hashlib.sha256(key).digest()
    key = key + b'\x00' * (block_size - len(key))
    o_key = bytes(b ^ 0x5C for b in key)
    i_key = bytes(b ^ 0x36 for b in key)
    inner = hashlib.sha256(i_key + msg).digest()
    outer = hashlib.sha256(o_key + inner).digest()
    return ubinascii.hexlify(outer).decode()

def authenticate_with_hub():
    timestamp = str(time.time())
    message = NODE_ID + ":" + timestamp
    signature = sign_message(NODE_SECRET, message)
    payload = {
        "node_id": NODE_ID,
        "timestamp": timestamp,
        "signature": signature
    }
    try:
        response = urequests.post(
            "http://" + HUB_IP + ":" + str(HUB_PORT) + "/register",
            json=payload
        )
        print("Auth response:", response.text)
        response.close()
    except Exception as e:
        print("Auth failed:", e)

authenticate_with_hub()
