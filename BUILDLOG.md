# BUILDLOG.md — AHI ESP32 Phase 1

> The story of how a zero trust IoT mesh came to life.

---

## May 11, 2026 — Hardware Arrives

Three ELEGOO ESP32-D0WD-V3 boards. Out of the box, flashed MicroPython
v1.24.1 on all three via esptool. Verified WiFi radio active on each
node through the MicroPython REPL.

Development hub: crossroad_code iMac running Ubuntu.

All three nodes alive. Phase 1 begins.

---

## Challenge 1: WiFi Credential Encoding

**Problem:** Nodes refusing WiFi connection despite correct credentials.

**Discovery:** MicroPython's `network.WLAN` requires credentials passed
as byte strings, not plain strings. A password with special characters
was being silently misread.

**Fix:**
```python
sta.connect(b"SSID", b"password")

The b"" prefix forces byte string encoding. Connection established
on all three nodes immediately after.
Lesson: MicroPython is not Python. Assumptions about type handling
will cost you time.

Challenge 2: MicroPython Epoch Offset
Problem: Timestamps from the ESP32 nodes were off by decades.
Discovery: MicroPython’s internal clock epoch starts at
January 1, 2000 — not January 1, 1970 like Unix. Every timestamp
was offset by exactly 946,684,800 seconds.
Fix:

import time
unix_time = time.time() + 946684800

Why it matters: RealAgentID uses timestamps for TTL nonce
enforcement. An incorrect epoch would break replay attack prevention.
Accurate time is not optional in a zero trust system.

Challenge 3: Network Isolation
Problem: ESP32 nodes on the main network represented an unacceptable
attack surface. Any compromised node could reach every device on the LAN.
Decision: Move all ESP32 nodes to an isolated guest VLAN.
Implementation:
        •       Nodes assigned to guest network (isolated from main LAN)
        •       UFW rules configured on the hub to control inbound node traffic
        •       Hub sits on both networks as the controlled bridge point
Result: Nodes can reach the hub. Nodes cannot reach each other’s
management interfaces or any other LAN device. Blast radius of a
compromised node is contained.

Architecture Decision: RealAgentID as the Trust Layer
The question: How do you know the node sending presence data is
actually your node and not a spoofed device?
The answer: You don’t — unless every node has a cryptographic identity.
Decision: Integrate RealAgentID as the identity and verification
layer for all ESP32 nodes and hub agents.
What this means in practice:
        •       Every node registers an Ed25519 keypair
        •       All mesh communications are signed
        •       The hub verifies signatures before processing any data
        •       Replay attacks blocked via Redis TTL nonces
        •       Full tamper-evident audit trail of all node activity
This is the architectural decision that transforms AHI from a presence
detection project into a zero trust IoT mesh.

End State — Phase 1 Complete

ESP32 nodes flashed 3/3
WiFi authentication 3/3
Epoch offset resolved
Network isolation | Guest VLAN + UFW
RealAgentID integrated
Zero-trust posture

Three ESP32 nodes.
One hub.
Cryptographic identity on every layer.
No cameras.
No implicit trust.

Phase 2: CSI data collection begins.
