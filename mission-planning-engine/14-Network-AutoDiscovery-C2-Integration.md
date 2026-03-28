# Network Auto-Discovery and Device Integration Architecture
## C2 Platform — Passive Network Scanner and Adapter Framework

**Document type:** Architecture Design
**Status:** Research / Pre-implementation
**Scope:** Passive network discovery, device fingerprinting, adapter hot-loading
**Relates to:** `src/mpe/c2_models.py`, `src/mpe/classifier.py`, existing AIS/ADS-B receivers

---

## 1. Problem Statement

When this C2 platform is deployed onto a customer's network — whether a military forward operating base, a coastguard operations centre, or a civilian disaster-response network — it will encounter dozens of devices broadcasting data in different proprietary and standard protocols. An operator should not need to manually configure each device. The system should:

1. Observe network traffic and identify what protocols are present
2. Classify each source as a specific device type with high confidence
3. Automatically install the correct adapter to bring that device into the common operating picture
4. Do this on minimal hardware, without disrupting network operations

This document designs that system.

---

## 2. System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          DEPLOYMENT NETWORK                                  │
│  [Drone GCS] [AIS Receiver] [Radar] [ATAK Server] [Camera] [Tracker] ...    │
└──────────────────────────────┬──────────────────────────────────────────────┘
                               │ Raw packets (promiscuous mode or SPAN port)
                               ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                        PASSIVE NETWORK SCANNER                                │
│                                                                               │
│  ┌──────────────┐  ┌─────────────────────┐  ┌──────────────────────────┐    │
│  │  Packet      │  │  Service Discovery  │  │  Traffic Pattern         │    │
│  │  Sniffer     │  │  Listener           │  │  Analyser                │    │
│  │  (libpcap/   │  │  (mDNS/SSDP/UPnP)  │  │  (packet size, freq,     │    │
│  │   scapy)     │  │                     │  │   directionality)        │    │
│  └──────┬───────┘  └──────────┬──────────┘  └────────────┬─────────────┘   │
│         └───────────────────┬─┘─────────────────────────-┘                  │
│                             ▼                                                 │
│                    ┌─────────────────┐                                       │
│                    │ Protocol        │                                        │
│                    │ Signature DB    │                                        │
│                    │ (rules engine)  │                                        │
│                    └────────┬────────┘                                       │
└─────────────────────────────┼────────────────────────────────────────────────┘
                              │ Candidate fingerprint
                              ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         DEVICE CLASSIFIER                                     │
│                                                                               │
│  Input: {src_ip, src_port, dst_port, protocol_hint, traffic_pattern,         │
│           service_name, banner}                                               │
│                                                                               │
│  Stage 1: Rule-based triage (deterministic, zero-cost)                       │
│    ├── Port lookup → known protocol                                           │
│    ├── Byte-sequence match → protocol signature                               │
│    └── Service name match → device type                                       │
│                                                                               │
│  Stage 2: ML classifier (only if rule-based inconclusive)                    │
│    ├── TinyML ONNX model (<10MB, <50MB RAM)                                  │
│    └── Features: packet length distribution, inter-arrival time,             │
│        port entropy, first-N-bytes fingerprint                                │
│                                                                               │
│  Output: {device_type, protocol, confidence, protocol_version}               │
└─────────────────────────────┬───────────────────────────────────────────────┘
                              │ Classification result
                              ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                        OPERATOR APPROVAL GATE                                 │
│                                                                               │
│  [NEW DEVICE DETECTED]                                                        │
│  Type: MAVLink drone GCS  |  IP: 192.168.1.47:14550                          │
│  Confidence: 97%          |  Protocol: MAVLink v2                             │
│  Suggested adapter: mavlink-ardupilot-v2                                      │
│                                                                               │
│  [ Connect ]  [ Skip ]  [ Classify manually ]  [ Block ]                     │
└─────────────────────────────┬───────────────────────────────────────────────┘
                              │ Approved
                              ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                         ADAPTER MANAGER                                       │
│                                                                               │
│  ┌────────────────────┐    ┌──────────────────────┐                          │
│  │  Adapter Registry  │    │  Local Adapter Cache  │                         │
│  │  (manifest.json)   │◄──►│  ~/.mpe/adapters/     │                        │
│  │  device_type →     │    │                       │                         │
│  │  adapter_id        │    └──────────────────────┘                          │
│  └────────────────────┘                                                      │
│           │                                                                   │
│           ▼                                                                   │
│  ┌─────────────────────────────────────────────────────────────┐             │
│  │  Adapter Loader                                              │             │
│  │  1. Check local cache                                        │             │
│  │  2. Fetch from signed adapter repository (if not cached)     │             │
│  │  3. Verify signature                                         │             │
│  │  4. Load into isolated sandbox (subprocess / importlib)      │             │
│  │  5. Register adapter with broker                             │             │
│  └─────────────────────────────────────────────────────────────┘             │
└─────────────────────────────┬───────────────────────────────────────────────┘
                              │ Adapter running
                              ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                         PROTOCOL ADAPTER                                      │
│  (one per connected device, runs in isolated thread or subprocess)            │
│                                                                               │
│  Device-specific protocol                                                     │
│  (MAVLink, CoT, AIS, ADS-B, ASTERIX, RTSP, etc.)                            │
│         │                                                                     │
│         ▼                                                                     │
│  translate() → C2 Entity / Track  (c2_models.Entity / c2_models.Track)       │
│                                                                               │
│  Adapter publishes updates via internal message bus (asyncio Queue)           │
└─────────────────────────────┬───────────────────────────────────────────────┘
                              │ Normalised C2 entities
                              ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                   C2 COMMON OPERATING PICTURE                                 │
│            Entity Registry  /  Track Store  /  Map Display                   │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Component Descriptions

### 3.1 Passive Network Scanner

The scanner is the ears of the system. It never transmits; it only observes.

**Three sub-components run in parallel:**

**A. Packet Sniffer**

Captures raw packets from a network interface in promiscuous mode. On Linux this requires a raw socket or `libpcap`. On deployment hardware with a SPAN/mirror port, it captures a copy of all switch traffic.

Key library: `scapy` (Python) or `pyshark` (wraps tshark). For minimal-overhead production use, `dpkt` + raw sockets is lighter than scapy.

What it extracts per flow:
- Source IP, destination IP
- Transport protocol (UDP/TCP)
- Source port, destination port
- First 64 bytes of payload (for signature matching)
- Packet inter-arrival time distribution
- Packet size distribution over a 30-second window

**B. Service Discovery Listener**

Listens on multicast groups for:
- mDNS (224.0.0.251 : 5353) — Apple/Bonjour/Avahi device names and service types
- SSDP (239.255.255.250 : 1900) — UPnP device descriptions
- WS-Discovery (239.255.255.250 : 3702) — ONVIF IP cameras

These are passive — the scanner never sends a query packet. It only receives announcements that devices broadcast on their own. Service names from mDNS/SSDP frequently contain manufacturer names, device models, or service types (e.g., `_rtsp._tcp`, `_mavlink._udp`) that directly identify the device type.

**C. Traffic Pattern Analyser**

For flows that do not match a known protocol signature, the analyser computes statistical features:
- Mean and variance of packet length
- Inter-arrival time coefficient of variation (bursty vs. periodic)
- Directionality ratio (one-way broadcast vs. bidirectional command/response)
- Port entropy (does the source randomise ports, indicating a response protocol?)
- Flow duration and total bytes in first 60 seconds

These features are the input to the Stage 2 ML classifier.

### 3.2 Protocol Signature Database

A rule database structured as a priority-ordered list of matchers. Each entry specifies:

```
ProtocolSignature:
  id:            "mavlink_v2"
  priority:      10           # higher = checked first
  ports:         [14550, 14551, 5760]   # UDP/TCP ports
  transport:     "udp"
  byte_match:    {offset: 0, bytes: "fd"}  # MAVLink v2 magic byte
  min_packet_len: 10
  device_type:   "drone_gcs"
  protocol:      "mavlink_v2"
  confidence:    0.95
```

The database is a YAML/JSON file — no compiled code — so operators can add custom signatures without redeploying. This is the same model used by Nmap's `nmap-service-probes` file, which has proven robust for 25+ years.

**Known military/operational protocol signatures (see Section 5 for full list):**

| Protocol | Magic Bytes / Port | Transport | Device Type |
|---|---|---|---|
| MAVLink v1 | 0xFE @ byte 0 | UDP 14550 | Drone GCS |
| MAVLink v2 | 0xFD @ byte 0 | UDP 14550/14551 | Drone GCS |
| CoT / TAK | XML `<event` prefix | UDP 6969, TCP 8087/8089 | Situational awareness node |
| NMEA 0183 (AIS) | `!AIVDM` / `!AIVDO` | UDP 10110, TCP 10110 | AIS receiver |
| NMEA 0183 (GPS) | `$GP` / `$GN` prefix | UDP/TCP various | GPS tracker |
| ADS-B Beast | 0x1A @ byte 0 | TCP 30005 | ADS-B receiver |
| ADS-B SBS-1 | `MSG,` ASCII | TCP 30003 | ADS-B receiver |
| ADS-B JSON | `{"icao":` | TCP/HTTP 8080 | ADS-B receiver |
| RTSP | `RTSP/1.0` | TCP 554 | IP camera |
| ONVIF | SOAP/XML | TCP 80/443 | IP camera |
| ASTERIX | Binary category field | UDP 8600 | Radar |
| JREAP-C | Defined header | TCP 4000 | Joint range extension |
| VMF | Military binary | UDP/TCP 3000 | Tactical messaging |
| STANAG 4586 | XML/binary | TCP 4586 | UAV control station |
| DJI SDK v2 | 0x55 0xAA header | UDP 8080 | DJI drone/controller |

### 3.3 Device Classifier

Classification is a two-stage pipeline. Stage 1 is always attempted first; Stage 2 is only invoked when Stage 1 confidence is below a configurable threshold (default: 0.80).

**Stage 1: Rule-Based Triage**

Decision tree, evaluated in priority order:

1. Port lookup: check source/destination ports against the signature DB
2. Byte-sequence match: compare first N bytes of payload against known magic bytes
3. Service name match: if mDNS/SSDP returned a service name, check against device type table
4. Banner match: for TCP connections, check the server banner (HTTP Server header, FTP banner, etc.)

This covers ~85% of cases with zero computational cost. The remaining ~15% are either encrypted protocols, non-standard port configurations, or novel devices.

**Stage 2: Tiny ML Classifier**

Input feature vector (fixed-length, computed from flow statistics):
- Normalised mean packet length [0,1]
- Normalised packet length variance [0,1]
- Log-scaled inter-arrival time mean
- Directionality ratio (outbound bytes / total bytes)
- Protocol family hint (1-hot: UDP=0, TCP=1, multicast=2)
- First 8 bytes of first payload packet (raw bytes, hex-encoded as 16 floats)

Total feature vector: ~22 floats.

**Model options evaluated for this use case:**

| Option | Size | RAM | Latency | Accuracy estimate | Notes |
|---|---|---|---|---|---|
| Decision tree (scikit-learn) | <1 KB | <1 MB | <0.1 ms | ~88% | Fully explainable, no GPU |
| Random forest (100 trees) | ~2 MB | ~5 MB | ~1 ms | ~93% | Good baseline |
| Gradient-boosted tree (XGBoost) | ~5 MB | ~10 MB | ~2 ms | ~95% | Best accuracy per byte |
| MobileNetV3 feature extractor | ~4 MB | ~30 MB | ~10 ms | N/A | Overkill, wrong modality |
| ONNX Runtime + RF/GBDT export | same as above | +5 MB runtime | +1 ms | same | Portable across platforms |
| BitNet / 1-bit LLM | 100MB+ (smallest) | 200MB+ | 100ms+ | Higher | Wrong tool for this task |

**Recommendation: Random forest or gradient-boosted tree, exported to ONNX.**

BitNet and other 1-bit LLMs are designed for natural language tasks. Protocol classification is a structured, low-dimensional classification problem (22 features, ~30 classes). A gradient-boosted tree trained on labelled flow data will outperform a tiny LLM on this task while using 1/20th the memory. The classifier should be replaceable — the interface is fixed regardless of what sits behind it.

For the training dataset: Zeek/Bro or Suricata can label network flows in a lab environment. Record traffic from each device type, run the feature extractor, label with the ground truth device type, train offline, export ONNX.

**Classifier output:**
```python
@dataclass
class DeviceFingerprint:
    src_ip: str
    src_port: int
    dst_port: int
    device_type: str          # e.g. "drone_gcs", "ais_receiver"
    protocol: str             # e.g. "mavlink_v2"
    protocol_version: str     # e.g. "2.0"
    confidence: float         # 0.0 - 1.0
    classification_method: str  # "rule_port", "rule_bytes", "ml_rf", etc.
    raw_features: dict        # for audit/explainability
    detected_at: datetime
```

### 3.4 Operator Approval Gate

No device is connected without operator confirmation. This is non-negotiable for security and safety. The gate:

- Queues pending fingerprints
- Displays each to the operator with: IP, port, detected type, confidence, suggested adapter, timestamp
- Operator actions: Connect, Skip (keep monitoring), Block (add to deny list), Override type
- For high-confidence matches (>0.95) from signed protocols, operators may configure auto-approve for specific device types (e.g., "auto-connect all MAVLink drones")
- All decisions are logged with operator ID and timestamp

### 3.5 Adapter Manager

Manages the lifecycle of device adapters.

**Adapter Registry** is a `manifest.json` file structured as:

```json
{
  "version": "1.0",
  "adapters": {
    "mavlink_v2": {
      "id": "mavlink-ardupilot-v2",
      "version": "1.2.0",
      "device_types": ["drone_gcs"],
      "protocols": ["mavlink_v2"],
      "entry_point": "adapters.mavlink.ardupilot:MAVLinkArduPilotAdapter",
      "sha256": "abc123...",
      "signed_by": "mpe-official"
    },
    "cot_tak": {
      "id": "cot-tak-server",
      "version": "2.1.0",
      ...
    }
  }
}
```

**Adapter discovery hierarchy (checked in order):**
1. Built-in adapters (shipped with the platform, for MAVLink, CoT, AIS, ADS-B)
2. Local cache directory (`~/.mpe/adapters/`)
3. Signed adapter repository (authenticated HTTPS, GPG-signed packages)

**Adapter loading sequence:**
1. Look up `device_type` in registry → get `adapter_id`
2. Check local cache for version match
3. If not cached: fetch from repository, verify SHA-256 and GPG signature, cache
4. Load adapter module via `importlib.import_module` into an isolated subprocess (not the main process)
5. Establish IPC channel (asyncio Queue, Unix socket, or ZMQ depending on throughput requirements)
6. Adapter begins translating device protocol → `c2_models.Entity` / `c2_models.Track`

**Adapter isolation model:**
- Each adapter runs in a separate Python subprocess (not a thread) — so a buggy adapter cannot corrupt the main process state
- The subprocess communicates over a typed IPC channel with a defined schema
- Adapters are granted read-only access to device network traffic and write-only access to the entity bus
- Future enhancement: run adapters in separate Linux namespaces (containers) for strong isolation

### 3.6 Protocol Adapter Interface

Every adapter implements the same abstract base class:

```python
class ProtocolAdapter(ABC):
    """Every device adapter implements this interface.

    The adapter translates device-specific protocol messages into
    c2_models.Entity and c2_models.Track objects, published to the
    entity bus.
    """

    @property
    @abstractmethod
    def adapter_id(self) -> str: ...

    @property
    @abstractmethod
    def supported_protocols(self) -> list[str]: ...

    @abstractmethod
    async def connect(self, host: str, port: int, config: dict) -> None: ...

    @abstractmethod
    async def disconnect(self) -> None: ...

    @abstractmethod
    async def run(self, entity_bus: asyncio.Queue) -> None:
        """Main loop: receive device data, translate, publish to bus."""
        ...

    @abstractmethod
    def status(self) -> AdapterStatus: ...
```

This interface is identical to what the existing `AISReceiver` and `ADSBReceiver` implement — they are already de facto adapters. The new framework formalises that pattern.

**Existing receivers as adapters (what already exists):**

| Existing module | Adapter role |
|---|---|
| `ais_receiver.py` | AIS NMEA → VesselTrack → CoT |
| `adsb_receiver.py` | ADS-B JSON/API → AircraftTrack → CoT |
| `cot_sender.py` | C2 Entity → CoT XML output |
| `ais_cot_bridge.py` | VesselTrack → CoT (translator) |
| `adsb_cot_bridge.py` | AircraftTrack → CoT (translator) |

These modules become the first registered adapters in the new framework with zero code changes — they just need to be wrapped in the `ProtocolAdapter` ABC.

---

## 4. Protocol Reference — Military and Operational Systems

### 4.1 Drone and UAV Protocols

**MAVLink (ArduPilot / PX4)**
- Version 1: magic byte `0xFE`, UDP 14550 (GCS listening), UDP 14551 (second GCS), TCP 5760 (SITL)
- Version 2: magic byte `0xFD`, same ports
- Heartbeat message ID 0 sent every 1 second — highly distinctive
- Fingerprint: byte 0 = `0xFE`/`0xFD`, byte 5 = system ID, byte 6 = component ID
- Detection reliability: very high (protocol is well-documented and distinctive)

**STANAG 4586 (NATO UAV control)**
- ISO 15628, XML over TCP
- Port: typically TCP 4586 (not standardised, varies by implementation)
- Some implementations use UDP with a proprietary wrapper
- Binary + XML hybrid in some versions
- Key discriminator: XML root element `<UCSRequest>` or `<CDLC_Message>`

**DJI proprietary**
- OcuSync/Lightbridge: encrypted, use 2.4GHz/5.8GHz RF — not normally visible as raw network packets
- DJI SDK v2 (when a GCS app is connected via SDK): uses custom binary protocol, UDP/TCP 8080 or 8889
- DJI devices on local WiFi: mDNS service `_dji._tcp` — very distinctive
- Fingerprint: `0x55 0xAA` header magic bytes in SDK protocol

### 4.2 Situational Awareness

**Cursor on Target (CoT) / TAK**
- Protocol: XML over UDP (multicast) or TCP (unicast to TAK server)
- Ports: UDP 6969 (legacy broadcast), TCP 8087 (TAK server unencrypted), TCP 8089 (TAK server TLS)
- XML structure: `<event version="2.0" uid="..." type="a-f-G-U-C" ...>`
- Type field encodes MIL-STD-2525 symbology: `a-f-G-U-C` = friendly ground unit
- Detection: XML starting with `<event` + CoT type field pattern

**Link 16 / SADL / JTIDS**
- Link 16 is a TDMA radio protocol — not carried natively over IP
- However, Link 16 gateways (J-series message processors) do forward Link 16 data to IP networks
- Typically encapsulated in: JREAP-C (Joint Range Extension Application Protocol - Common)
- JREAP-C: TCP 4000 (default), message structure defined in MIL-STD-3011
- Not publicly documented enough for open-source signature development

**NFFI (NATO Friendly Force Information)**
- STANAG 5527, XML schema
- Transported over HTTPS or as data within NATO messaging systems
- Not passively discoverable on open LAN — requires authorised network access

**Blue Force Tracker (BFT)**
- Primarily satellite-based (Inmarsat / MUOS) — not an IP LAN protocol
- BFT-1 gateways that bridge to IP exist but are highly proprietary
- On IP networks: typically appears as HTTPS traffic to specific government servers
- Not practical to fingerprint passively

### 4.3 Aviation and Air Surveillance

**ADS-B (network-forwarded formats)**
- Beast binary: TCP 30005, magic byte `0x1A` followed by message type byte
- AVR/hex: TCP 30002, ASCII hex strings starting with `*`
- SBS-1 (BaseStation): TCP 30003, comma-separated ASCII starting with `MSG,`
- JSON (dump1090-fa / readsb): HTTP/TCP 8080, path `/data/aircraft.json`
- Detection: port + format is highly specific

**ASTERIX (EUROCONTROL radar data exchange)**
- Binary, category-based message format
- UDP 8600 (common) but varies — many implementations use UDP broadcast or multicast
- Each message starts with: 1-byte category ID + 2-byte length
- Categories relevant here: CAT 21 (ADS-B reports), CAT 48 (monoradar), CAT 62 (system track)
- Detection: byte 0 = valid ASTERIX category (1-255), bytes 1-2 = plausible length

### 4.4 Maritime

**AIS (NMEA 0183)**
- Sentences: `!AIVDM` (received from others), `!AIVDO` (own vessel)
- UDP 10110, UDP 5050 (AIS-catcher default), TCP 10110
- Distinctive ASCII prefix — extremely easy to detect
- Already implemented in `ais_receiver.py`

**NMEA (GPS/Navigation)**
- Sentences start with `$`: `$GPGGA`, `$GPRMC`, `$GNRMC` etc.
- UDP/TCP 10110 (same as AIS), TCP 4001, various
- Shared port with AIS requires byte inspection to distinguish

### 4.5 Surveillance and Sensors

**RTSP (camera streams)**
- TCP 554 (standard), TCP 8554 (alternate)
- Connection starts with `OPTIONS rtsp://` or `DESCRIBE rtsp://`
- Response: `RTSP/1.0 200 OK`
- mDNS: `_rtsp._tcp` service type

**ONVIF (IP camera management)**
- WS-Discovery on UDP 3702 (multicast 239.255.255.250)
- HTTP/SOAP on TCP 80 or 443
- Discovery probe: `<Probe><Types>dn:NetworkVideoTransmitter</Types></Probe>`
- Response contains device URI and service capabilities

**Radar (proprietary)**
- No universal standard — each radar manufacturer uses a proprietary protocol
- Common patterns: binary UDP broadcast on high ports (>10000), periodic fixed-size packets
- Furuno, Garmin: NMEA-based radar overlay messages
- Military radar: ASTERIX (see above) or classified protocols

### 4.6 VMF and Tactical Messaging

**VMF (Variable Message Format)**
- MIL-STD-47001
- Binary, compact encoding optimised for low-bandwidth radio
- When gateway-bridged to IP: typically UDP, port varies by implementation
- Fingerprint: first byte = application header, fixed bit patterns in first 4 bytes

**OTH-Gold (Over-The-Horizon targeting)**
- Classified protocol — not available for open-source signature development
- Network forwarding typically over classified networks (SIPRNET) — not present on unclassified LANs

---

## 5. Tiny AI Models — Detailed Evaluation

### 5.1 Why Rule-Based First?

For network protocol classification, the signal is high-dimensional in data-science terms but the decision surface is clean. Most protocols have:
- Fixed magic bytes (MAVLink, Beast ADS-B)
- Fixed port assignments (CoT, RTSP)
- Distinctive ASCII prefixes (NMEA, CoT XML, HTTP)

A lookup table resolves ~85% of cases. Rule-based classification for this problem is not a limitation — it is the correct engineering choice for deterministic, explainable, auditable operation in a safety-critical context.

### 5.2 When is ML Actually Needed?

ML is needed for:
1. Protocols on non-standard ports (someone moved MAVLink to port 9999)
2. Encrypted protocols (DJI OcuSync when tunnelled, VPN-wrapped military protocols)
3. Novel devices not in the signature database
4. Distinguishing between protocols that share ports (AIS vs. NMEA GPS on 10110)

For cases 1, 2, 3, 4: a random forest on traffic-pattern features is the right tool. It operates on statistical properties of the flow rather than the content.

### 5.3 BitNet / 1-bit LLMs Assessment

Meta's BitNet b1.58 (2024) demonstrated that weights can be represented as {-1, 0, +1}, reducing model size dramatically. The smallest deployable BitNet models are ~100MB. Microsoft's phi-2 (2.7B parameters) runs on a Raspberry Pi 5 but requires ~2GB RAM.

**Why BitNet is the wrong tool here:**
- Designed for text generation and comprehension — not tabular/numerical classification
- Minimum viable model size (~100MB) is 10-50x larger than a comparable GBDT
- Latency is 100-1000x higher per inference
- Explainability is near-zero (black box)
- Training requires labelled text — the feature space here is numerical

**When BitNet/LLM would be appropriate in this system:**
- Natural language description of device from mDNS/SSDP service records
- Parsing free-text device names or model strings to infer device type
- Generating human-readable explanations of classification decisions for the operator

### 5.4 Recommended ML Stack

| Component | Library | Size | Target Hardware |
|---|---|---|---|
| Feature extraction | dpkt or scapy | — | Any |
| Rule engine | Pure Python dict lookup | — | Any |
| ML classifier | scikit-learn RF or XGBoost | 2-10 MB model | Raspberry Pi 4 / Jetson Nano |
| Model runtime | ONNX Runtime (onnxruntime) | ~30 MB runtime | Any |
| TinyML alternative | micromlgen (Arduino/bare metal) | <100 KB | ESP32 / bare metal |

**Target inference budget:**
- Raspberry Pi 4: <5 ms per classification
- Jetson Nano: <1 ms per classification
- x86 laptop/server: <0.1 ms per classification

ONNX Runtime is the right portability layer — train in scikit-learn or XGBoost, export once to `.onnx`, run everywhere with identical results.

---

## 6. Adapter Architecture — Detailed Design

### 6.1 Plugin Pattern

The adapter system uses Python's `importlib` for dynamic loading. This is the same mechanism used by pytest plugins, Django apps, and Flask extensions — well-understood, stable, and zero external dependencies.

```
adapters/
├── __init__.py
├── base.py              # ProtocolAdapter ABC + AdapterStatus
├── registry.py          # AdapterRegistry + manifest loader
├── loader.py            # AdapterLoader (importlib + subprocess wrapper)
├── builtin/
│   ├── mavlink.py       # MAVLink v1/v2 → c2_models.Entity
│   ├── cot.py           # CoT/TAK → c2_models.Entity
│   ├── ais.py           # AIS NMEA → c2_models.Track (wraps ais_receiver.py)
│   ├── adsb.py          # ADS-B → c2_models.Track (wraps adsb_receiver.py)
│   ├── asterix.py       # ASTERIX CAT 21/48 → c2_models.Track
│   └── rtsp.py          # RTSP camera → c2_models.Entity (sensor type)
└── community/           # Downloaded adapters (verified signatures)
```

### 6.2 Adapter Versioning and Compatibility

Each adapter declares:
```python
ADAPTER_API_VERSION = "1.0"   # must match loader expectation
MIN_MPE_VERSION = "0.5.0"     # minimum platform version
MAX_MPE_VERSION = "2.x"       # maximum platform version (semver range)
```

The loader rejects adapters with incompatible API versions before execution.

### 6.3 Adapter Sandboxing

Three tiers of isolation, chosen based on trust level:

| Tier | Mechanism | Use for |
|---|---|---|
| Thread (no isolation) | `threading.Thread` | Built-in adapters (trusted, same codebase) |
| Subprocess | `multiprocessing.Process` | Community adapters (verified signature) |
| Container | Docker/Podman subprocess | Unverified adapters / high-risk devices |

For the MPE's target deployment (Raspberry Pi / embedded), subprocess isolation is the practical default.

### 6.4 Entity Bus

All adapters write to a single internal message bus:

```
Adapter A (MAVLink) ─────────────────────┐
Adapter B (CoT)     ─────────────────────┤──► asyncio.Queue ──► Entity Registry
Adapter C (AIS)     ─────────────────────┘                       (Track Store)
```

Bus messages are typed:
```python
@dataclass
class EntityUpdate:
    adapter_id: str
    update_type: Literal["create", "update", "delete"]
    entity: Entity | Track
    raw_source: bytes | None = None  # for audit log
    received_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
```

---

## 7. Security Architecture

### 7.1 Passive Scanning Guarantees

The scanner must never transmit. Technical controls:
- Open packet capture socket in read-only mode (`BPF_SOCK_RAW` with no send capability)
- Service discovery: listen-only on multicast groups, never send probe packets
- No ARP requests, no ICMP pings, no TCP SYN packets from the scanner
- Process runs under a dedicated user account with `CAP_NET_RAW` only (no `CAP_NET_ADMIN`)

Active scanning (Nmap-style) is an explicitly out-of-scope feature. If active probing is needed in future, it must be:
1. Operator-initiated, not automatic
2. Logged as a significant event
3. Performed against a specific IP only (no subnet sweeps)

### 7.2 Adapter Repository Security

```
Developer signs adapter package:
  gpg --sign adapter-mavlink-v2-1.2.0.tar.gz

Repository stores:
  adapter-mavlink-v2-1.2.0.tar.gz
  adapter-mavlink-v2-1.2.0.tar.gz.sig
  manifest.json (registry index, also signed)

Loader verifies:
  1. Download manifest.json, verify signature against trusted public key
  2. Download adapter package
  3. Verify SHA-256 of package matches manifest entry
  4. Verify GPG signature of package
  5. Only then import/execute adapter code
```

Trusted public keys are bundled with the platform and cannot be modified at runtime.

### 7.3 Audit Logging

Every event is logged to an append-only audit log:

```
[2026-03-28T14:32:01Z] SCANNER  device_detected   192.168.1.47:14550  mavlink_v2  confidence=0.97
[2026-03-28T14:32:05Z] OPERATOR approved          192.168.1.47:14550  adapter=mavlink-ardupilot-v2  operator=operator-01
[2026-03-28T14:32:06Z] LOADER   adapter_loaded    mavlink-ardupilot-v2 v1.2.0  sha256=abc123
[2026-03-28T14:32:06Z] ADAPTER  connected         192.168.1.47:14550  sysid=1  component=autopilot
[2026-03-28T14:32:07Z] ENTITY   created           uid=TRK-a4f3b2e1  type=uav  source=mavlink_v2
```

Log is structured JSON, written to an append-only file descriptor, optionally forwarded to a syslog server.

### 7.4 Classification Review for High-Stakes Devices

For device types with elevated security implications (radar, BFT gateway, STANAG 4586 UAV control station), the confidence threshold for auto-suggest should be set higher (>0.99) and auto-approve should be disabled regardless of operator configuration.

---

## 8. Minimum Viable Implementation Plan

### Phase 1 — Core Framework (buildable now, no special hardware)

**What it does:** Formalises the existing AIS/ADS-B receivers as adapters, creates the adapter ABC, registry, and entity bus. No network scanning yet.

**Deliverables:**
- `adapters/base.py` — ProtocolAdapter ABC, AdapterStatus, EntityUpdate
- `adapters/registry.py` — AdapterRegistry with JSON manifest
- `adapters/loader.py` — importlib-based adapter loader (thread tier)
- `adapters/builtin/ais.py` — wraps existing `ais_receiver.py`
- `adapters/builtin/adsb.py` — wraps existing `adsb_receiver.py`
- `adapters/builtin/cot.py` — wraps existing `cot_sender.py`
- Entity bus (asyncio.Queue)
- Adapter lifecycle tests

**Libraries needed:** None beyond existing stack. Zero new dependencies.

**Time estimate:** 2-3 days of focused implementation.

### Phase 2 — Protocol Signature Database and Rule-Based Classifier (buildable now)

**What it does:** Implements the signature database, the rule-based Stage 1 classifier, and the `DeviceFingerprint` output model. Can be tested against recorded pcap files.

**Deliverables:**
- `discovery/signatures.yaml` — protocol signature database (start with 15 protocols)
- `discovery/classifier.py` — Stage 1 rule engine
- `discovery/fingerprint.py` — DeviceFingerprint model
- Tests using sample pcap files (can be generated in SITL environment)

**Libraries needed:** `pyyaml` (already in most Python environments). Optionally `dpkt` for pcap reading in tests.

**Time estimate:** 3-4 days.

### Phase 3 — Passive Network Scanner (requires Linux with promiscuous mode access)

**What it does:** The actual packet capture, mDNS/SSDP listener, and traffic pattern analyser. Requires a network interface and appropriate permissions.

**Deliverables:**
- `discovery/scanner.py` — PacketSniffer, ServiceDiscoveryListener, TrafficPatternAnalyser
- Integration between scanner → classifier → fingerprint queue
- Operator approval gate (CLI first, then GUI integration)
- Audit logger

**Libraries needed:** `scapy` (for packet capture) or `dpkt` + raw sockets. `zeroconf` library for mDNS passive listening.

**Time estimate:** 1 week. Needs testing on a real network or a simulated LAN (can use `mininet` or Docker bridge network).

### Phase 4 — ML Classifier Stage 2 (requires training data)

**What it does:** The traffic-pattern ML classifier for ambiguous protocols.

**Deliverables:**
- `discovery/feature_extractor.py` — extracts 22-feature vector from flow stats
- `discovery/ml_classifier.py` — ONNX Runtime inference wrapper
- Training pipeline (offline, separate notebook or script)
- Trained model file (`protocol_classifier.onnx`)

**Libraries needed:** `onnxruntime`, `scikit-learn` (training only), `numpy`.

**Key dependency:** Labelled training data. Generate by running the platform against known device setups in a lab.

**Time estimate:** 1 week (plus data collection time).

### Phase 5 — Community Adapter Repository (requires infrastructure)

**What it does:** Signed remote adapter repository with download, verify, and install.

**Deliverables:**
- Repository server (static file hosting + manifest)
- GPG signing workflow for adapter packages
- `adapters/loader.py` extended for remote fetch + subprocess isolation

**Libraries needed:** `requests` or `httpx`, `python-gnupg`.

**Time estimate:** 3-4 days.

### Phase 6 — Container Isolation (requires Docker on target)

**What it does:** Third isolation tier for untrusted adapters.

**Deliverables:**
- Docker-based adapter runner
- IPC over Unix socket to container

**Time estimate:** 3-4 days. Lower priority than Phases 1-4.

---

## 9. Technology Choices — Summary

| Component | Technology | Rationale |
|---|---|---|
| Packet capture | `scapy` or `dpkt` + raw socket | scapy for development, dpkt for production (lower overhead) |
| mDNS passive listen | `zeroconf` library (read-only mode) | Well-maintained, pure Python, passive mode supported |
| Protocol signature DB | YAML file | Human-readable, operator-editable, no compilation |
| Stage 1 classifier | Pure Python dict/rule engine | Zero dependencies, deterministic, explainable |
| Stage 2 classifier | scikit-learn GBDT → ONNX | Best accuracy/size ratio for tabular data |
| ONNX runtime | `onnxruntime` | Portable, CPU-only, 30MB, runs on Pi 4 |
| Adapter ABC | `abc.ABC` + `asyncio` | Zero dependencies, idiomatic Python |
| Adapter loading | `importlib.import_module` | Standard library, stable, auditable |
| Adapter IPC | `asyncio.Queue` (thread), `multiprocessing.Queue` (subprocess) | Standard library |
| Adapter signing | GPG / `python-gnupg` | Established standard, widely understood |
| Audit logging | Structured JSON, append-only fd | Simple, tamper-evident, parseable |
| C2 data models | Existing `c2_models.py` | Already designed for this exact purpose |

---

## 10. What Can Be Built Now vs. What Needs Hardware

### Can Build Now (laptop/desktop, no special hardware)

- Adapter ABC and registry framework
- Protocol signature YAML database
- Rule-based Stage 1 classifier
- DeviceFingerprint model
- Entity bus and adapter lifecycle
- Wrapping existing AIS/ADS-B receivers as adapters
- Tests using recorded pcap files or simulated traffic (scapy can generate packets)
- Audit logging
- Operator approval gate (CLI)
- MAVLink adapter (testable against SITL)
- CoT adapter (testable with ATAK simulator or FreeTAKServer)

### Needs Hardware / Network Access

| Feature | Hardware required |
|---|---|
| Live promiscuous packet capture | Linux host with NIC, `CAP_NET_RAW` |
| SPAN/mirror port capture | Managed switch with port mirroring |
| mDNS/SSDP passive discovery | LAN with multicast-enabled switch |
| DJI device detection | DJI controller + drone on WiFi |
| STANAG 4586 adapter | NATO-compatible UCS simulator (e.g., UCS Emulator) |
| ASTERIX adapter | Radar simulator or ASTERIX test stream |
| ML classifier training | Collection of labelled pcap from real devices |
| AIS adapter testing | RTL-SDR + antenna, or AIS-catcher with live feed |
| Link 16 / JREAP testing | Classified network access — not available |

### What Cannot Be Built (open-source only)

- Link 16 / SADL adapters (classified specification)
- BFT-1 adapters (proprietary, government-controlled)
- OTH-Gold adapters (classified)
- DJI decryption (OcuSync/Lightbridge are encrypted — DJI SDK is needed)
- NFFI in full (STANAG 5527 is NATO-restricted)

For these, the architecture supports them via the community adapter pathway — a defence contractor with access to the relevant specifications can write a compliant adapter.

---

## 11. Relationship to Existing MPE Architecture

The network auto-discovery system integrates cleanly with what already exists:

```
Existing:
  AISReceiver → VesselTracker → ais_cot_bridge → CoT XML out
  ADSBReceiver → AircraftTracker → adsb_cot_bridge → CoT XML out

New (wraps existing):
  NetworkScanner → DeviceClassifier → AdapterManager
                                           ├── AISAdapter (wraps AISReceiver)
                                           ├── ADSBAdapter (wraps ADSBReceiver)
                                           ├── MAVLinkAdapter (new)
                                           ├── CoTAdapter (wraps cot_sender)
                                           └── [more adapters]
                                                     │
                                                     ▼
                                           Entity Bus (asyncio.Queue)
                                                     │
                                                     ▼
                                           c2_models.Entity / c2_models.Track
                                           (shared data model, already defined)
```

The `c2_models.py` `Entity`, `Track`, `TrackSource`, and `EntityType` enumerations are already designed for this multi-source scenario. The `TrackSource` enum (`AIS`, `ADSB`, `RADAR`, `SIGINT`, `COT`) maps directly onto adapter output types.

The `EntityClassifier` in `classifier.py` already implements the rule-based + ML upgrade path pattern that the network classifier should follow. The new `DeviceClassifier` (for classifying network protocols) should be structured identically to `EntityClassifier` — a rule engine with a documented ML upgrade path and identical output contract regardless of what classification method is used.

---

## 12. Precedents and Prior Art

| Tool | Relevance |
|---|---|
| Nmap service detection (`nmap-service-probes`) | Direct precedent for protocol signature DB format. The probes file uses similar port + byte-match + probability structure |
| p0f | Passive OS fingerprinting from TCP/IP stack characteristics. Same passive-only philosophy |
| Zeek/Bro | Network protocol analysis framework. Can generate labelled flow data for ML training |
| Suricata | Protocol identification in IDS mode. Signature format similar to proposed DB |
| NetworkMiner | Passive network forensics. GUI tool showing similar device discovery concept |
| nzyme | Open-source WiFi defence sensor. Shows passive discovery architecture for security context |
| OpenTAK / FreeTAKServer | Open CoT/TAK implementation. Good reference for CoT protocol details |
| pymavlink | Python MAVLink library — the foundation for the MAVLink adapter |
| pyais | Python AIS library — already used in `ais_receiver.py` |
| dump1090 / readsb | ADS-B decoders — multiple output formats documented in source |
| python-asterix | Open-source ASTERIX decoder — foundation for radar adapter |

---

## 13. Key Design Decisions and Rationale

**Decision 1: Rule-based first, ML second**
Rationale: Deterministic, zero-cost, explainable. ML adds value only at the margin where rules are insufficient. For an operator safety context, explainability matters — "I detected MAVLink magic byte 0xFD on port 14550" is a more trustworthy justification than "the neural network said 97%".

**Decision 2: Operator approval before connection**
Rationale: The system can discover and classify without operator input, but it cannot connect. This is the critical safety boundary between an auto-discovery tool and a botnet. No exceptions.

**Decision 3: Adapter isolation via subprocess**
Rationale: A buggy or compromised adapter must not be able to crash the main C2 process or access its memory. The subprocess boundary provides this guarantee at minimal performance cost for low-throughput adapters.

**Decision 4: Signature database as human-readable YAML**
Rationale: Field operators and integrators should be able to add signatures for custom devices without modifying code. YAML is readable, versionable, and well-understood.

**Decision 5: ONNX for the ML classifier**
Rationale: Train once, deploy everywhere. An ONNX model trained on a development machine runs identically on a Raspberry Pi, a Jetson Nano, or a server. Avoids scikit-learn and numpy version pinning on embedded targets.

**Decision 6: No active probing**
Rationale: Active probing (SYN scans, ICMP pings, banner grabbing) reveals the presence of the C2 platform to network observers, may disturb sensitive military equipment with unexpected packets, and creates legal/rules of engagement issues. Passive only is the correct operational posture.
