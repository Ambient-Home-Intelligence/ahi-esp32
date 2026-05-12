from flask import Flask, request, jsonify
import hashlib
import hmac
import json
import time

app = Flask(__name__)

# Load node registry
with open('node_registry.json', 'r') as f:
    REGISTRY = json.load(f)

# Active sessions
SESSIONS = {}

def verify_signature(node_id, timestamp, signature):
    """Verify node signature against registry"""

    if node_id not in REGISTRY:
        return False, "Node not registered"

    node = REGISTRY[node_id]
    secret = bytes.fromhex(node['secret'])

    # Verify TTL
    issued_at = int(node['issued_at'])
    if time.time() - issued_at > node['ttl']:
        return False, "Node TTL expired"

    # Verify timestamp freshness (replay attack prevention)
    if abs(time.time() - float(timestamp)) > 60:
        return False, "Timestamp too old - possible replay attack"

    # Verify signature
    message = f"{node_id}:{timestamp}"
    expected = hmac.new(
        secret,
        message.encode(),
        hashlib.sha256
    ).hexdigest()

    if signature == expected:
        return True, "Verified"
    return False, "Invalid signature"

@app.route('/register', methods=['POST'])
def register_node():
    data = request.json
    node_id = data.get('node_id')
    timestamp = data.get('timestamp')
    signature = data.get('signature')

    verified, message = verify_signature(node_id, timestamp, signature)

    if verified:
        # Create active session
        SESSIONS[node_id] = {
            "ip": request.remote_addr,
            "connected_at": time.time(),
            "ttl": 86400
        }
        print(f"[REGISTERED] Node {node_id} from {request.remote_addr}")
        return jsonify({"status": "registered", "message": message})
    else:
        print(f"[REJECTED] Node {node_id} - {message}")
        return jsonify({"status": "rejected", "message": message}), 401

@app.route('/sessions', methods=['GET'])
def get_sessions():
    return jsonify(SESSIONS)

@app.route('/registry', methods=['GET'])
def get_registry():
    safe = {k: {"node_id": v["node_id"], "mac": v["mac"]}
            for k, v in REGISTRY.items()}
    return jsonify(safe)

if __name__ == '__main__':
    print("AHI Hub Server starting...")
    print(f"Loaded {len(REGISTRY)} nodes from registry")
    app.run(host='0.0.0.0', port=5000, debug=True)
