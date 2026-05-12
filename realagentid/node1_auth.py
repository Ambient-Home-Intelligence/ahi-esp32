import network
import urequests
import hashlib
import json
import time
import ubinascii

NODE_SECRET = "25fc5f9ba080b64898f516d94283e3b2e27da15371b59581e08326106f4f9aa3"
NODE_ID = "dfcd3aa6382f1eba"
HUB_IP = "192.168.1.124"
HUB_PORT = 5000

def sign_message(secret, message):
    key = bytes.fromhex(secret)
    msg = message.encode()

    # HMAC-SHA256 manual implementation
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

wlan = network.WLAN(network.STA_IF)
wlan.active(False)
time.sleep(2)
wlan.active(True)
time.sleep(2)
wlan.connect("ATTuGTqV7i", "fqmc5h=#dm3w")

timeout = 0
while not wlan.isconnected() and timeout < 60:
    time.sleep(1)
    timeout += 1

if wlan.isconnected():
    print("WiFi connected:", wlan.ifconfig())
    authenticate_with_hub()
else:
    print("WiFi failed")
