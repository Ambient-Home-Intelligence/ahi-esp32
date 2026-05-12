import hashlib
import hmac
import json
import os
import time

def generate_node_credentials(mac_address):
    """Generate unique credentials for an ESP32 node"""

    # Generate a unique secret key for this node
    node_secret = os.urandom(32)

    # Create node identity
    node_id = hashlib.sha256(mac_address.encode()).hexdigest()[:16]

    # Create registration token
    timestamp = str(int(time.time()))
    message = f"{node_id}:{mac_address}:{timestamp}"
    signature = hmac.new(
        node_secret,
        message.encode(),
        hashlib.sha256
    ).hexdigest()

    credentials = {
        "node_id": node_id,
        "mac": mac_address,
        "secret": node_secret.hex(),
        "signature": signature,
        "issued_at": timestamp,
        "ttl": 86400  # 24 hour TTL
    }

    return credentials

# Provision all three nodes
macs = macs = [
    "1c:c3:ab:fa:ce:64",  # Node 1
    "1c:c3:ab:fa:ce:6c",  # Node 2
    "1c:c3:ab:f9:58:18"   # Node 3
]

registry = {}
for mac in macs:
    creds = generate_node_credentials(mac)
    registry[creds["node_id"]] = creds
    print(f"Provisioned node: {creds['node_id']} ({mac})")

# Save registry
with open("node_registry.json", "w") as f:
    json.dump(registry, f, indent=2)

print("\nRegistry saved to node_registry.json")
