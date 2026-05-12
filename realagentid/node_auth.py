import network
import urequests
import hashlib
import hmac
import json
import time
import ubinascii

# Node credentials - will be unique per node
NODE_SECRET = "paste_node_secret_here"
NODE_ID = "paste_node_id_here"
HUB_IP = "192.168.1.124"
HUB_PORT = 5000

def sign_message(secret, message):
    """Sign a message using HMAC-SHA256"""
    key = bytes.fromhex(secret)
    msg = message.encode()
    h = hmac.new(key, msg, hashlib.sha256)
    return ubinascii.hexlify(h.digest()).decode()

def authenticate_with_hub():
    """Send signed authentication request to hub"""
    timestamp = str(time.time())
    message = f"{NODE_ID}:{timestamp}"
    signature = sign_message(NODE_SECRET, message)

    payload = {
        "node_id": NODE_ID,
        "timestamp": timestamp,
        "signature": signature
    }

    try:
        response = urequests.post(
            f"http://{HUB_IP}:{HUB_PORT}/register",
            json=payload
        )
        print("Auth response:", response.text)
        response.close()
    except Exception as e:
        print("Auth failed:", e)

# Connect to WiFi first
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('ATTuGTqV7i', 'fqmc5h=#dm3w')

timeout = 0
while not wlan.isconnected() and timeout < 30:
    time.sleep(1)
    timeout += 1

if wlan.isconnected():
    print("WiFi connected:", wlan.ifconfig())
    authenticate_with_hub()
else:
    print("WiFi failed")

