# Ambient Home Intelligence (AHI)

> Your home knows. No cameras required.

AHI is a zero trust IoT presence detection mesh built on ESP32 nodes using RF/CSI sensing. Every node and agent in the system is cryptographically verified by [RealAgentID](https://github.com/RealAgentID/RealAgentID) — no device is trusted by default.

---

## What It Is

AHI detects human presence and activity patterns through radio frequency and channel state information (CSI) sensing — without cameras, microphones, or invasive data collection. Three ESP32 nodes form a mesh that covers a space, and a hub aggregates and interprets the signal.

Privacy is not a feature. It's the architecture.

---

## Zero Trust IoT

Most smart home systems assume devices on the local network are trusted. AHI doesn't.

Every ESP32 node registers a cryptographic identity via RealAgentID before it can participate in the mesh. Commands are signed. Identities are verified at sub-millisecond latency. Replay attacks are blocked via Redis TTL nonces. Nothing operates anonymously.

This is the same trust model used in enterprise agent networks — applied to embedded IoT hardware.

---

## Hardware

- 3x ELEGOO ESP32-D0WD-V3 boards
- MicroPython v1.24.1
- Development hub: Ubuntu (crossroad_code iMac)
- Network: Isolated guest VLAN, UFW hardened

---

## Architecture

ESP32 Node 1] ─┐
[ESP32 Node 2] ─┼──► [Hub: Ubuntu] ──► [RealAgentID Registry]
[ESP32 Node 3] ─┘         │
└──► [Presence Engine] ──► [Intelligence Layer]


Each node:
- Connects to the network with verified identity
- Transmits RF/CSI presence data to the hub
- Is governed by RealAgentID cryptographic protocol

---

## Build Log Highlights

| Challenge | Resolution |
|---|---|
| WiFi credential encoding | MicroPython `b""` byte string fix |
| Time sync failure | MicroPython epoch offset (+946684800 vs Unix) |
| Node isolation | Guest network VLAN + UFW rules |
| Agent trust | RealAgentID integrated as identity layer |

See [BUILDLOG.md](./BUILDLOG.md) for the full technical narrative.

---

## Roadmap

- **Phase 1** ✅ — ESP32 nodes flashed, WiFi authenticated, RealAgentID integrated
- **Phase 2** — CSI data collection and presence detection algorithms
- **Phase 3** — Hub intelligence layer and pattern recognition
- **Phase 4** — Multi-zone mesh coordination
- **Phase 5** — Geo-fencing handoff (home ↔ mobile mode)
- **Phase 6** — Grant submission and production hardening

---

## Related

- [RealAgentID](https://github.com/RealAgentID/RealAgentID) — Cryptographic identity for AI and IoT agents
- [multi_agent_lab](https://github.com/RealAgentID/multi_agent_lab) — Governed multi-agent platform built on RealAgentID

---

## Organization

[Ambient Home Intelligence](https://github.com/Ambient-Home-Intelligence) is building privacy-first presence intelligence for homes and buildings — no cameras, no microphones, cryptographic trust at every layer.
