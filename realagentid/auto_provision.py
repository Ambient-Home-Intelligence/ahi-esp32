import json

# Load registry
with open('node_registry.json', 'r') as f:
    registry = json.load(f)

# Template for node auth script
template = '''import network
import urequests
import hashlib
import hmac
import json
import time
import ubinascii

NODE_SECRET = "{secret}"
NODE_ID = "{node_id}"
HUB_IP = "192.168.1.124"
HUB_PORT = 5000

def sign_message(secret, message):
    key = bytes.fromhex(secret)
    msg = message.encode()
    h = hmac.new(key, msg, hashlib.sha256)
    return ubinascii.hexlify(h.digest()).decode()

def authenticate_with_hub():
    timestamp = str(time.time())
    message = NODE_ID + ":" + timestamp
    signature = sign_message(NODE_SECRET, message)
    payload = {{
        "node_id": NODE_ID,
        "timestamp": timestamp,
        "signature": signature
    }}
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
wlan.active(True)
wlan.connect("ATTuGTqV7i", "fqmc5h=#dm3w")

timeout = 0
while not wlan.isconnected() and timeout < 30:
    time.sleep(1)
    timeout += 1

if wlan.isconnected():
    print("WiFi connected:", wlan.ifconfig())
    authenticate_with_hub()
else:
    print("WiFi failed")
'''

# Generate a script for each node
for i, (node_id, node) in enumerate(registry.items(), 1):
    filename = f"node{i}_auth.py"
    script = template.format(
        secret=node['secret'],
        node_id=node['node_id']
    )
    with open(filename, 'w') as f:
        f.write(script)
    print(f"Generated {filename} for node {node_id} ({node['mac']})")

print("\nDone! Flash each nodeX_auth.py to its corresponding board.")
