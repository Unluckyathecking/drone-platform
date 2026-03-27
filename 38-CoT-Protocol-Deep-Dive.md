# 38 — Cursor on Target (CoT) Protocol: Implementation Reference

**Purpose**: Complete technical reference for building a CoT output module in Python to feed drone telemetry into ATAK, WinTAK, and TAK Server.

---

## 1. What CoT Actually Is

Cursor on Target (CoT) is a lightweight publish/subscribe XML schema developed by MITRE Corporation for the US Air Force (~2002). It is not a full protocol — it is a data format. The transport is separate. ATAK, WinTAK, iTAK, and TAK Server all speak CoT natively. NATO C2 systems (NFFI, Link 16 gateways) can bridge to/from CoT.

CoT has two wire formats:
- **TAK Protocol v0**: Raw UTF-8 XML (what you will use)
- **TAK Protocol v1**: Protobuf framed binary (used on mesh/multicast links for bandwidth efficiency)

PyTAK recommends staying on v0 XML unless you have a specific reason — iTAK in particular has had compatibility issues with v1.

---

## 2. The CoT XML Schema — Every Field

### 2.1 The `<event>` Root Element

Every CoT message is a single `<event>` element. All attributes on `<event>` are **required**.

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
<event
  version="2.0"
  type="a-f-A-M-F-Q"
  uid="DRONE-001-ALPHA"
  how="m-g"
  time="2026-03-27T14:30:00.000Z"
  start="2026-03-27T14:30:00.000Z"
  stale="2026-03-27T14:32:00.000Z"
>
  <point
    lat="51.3721"
    lon="-0.1740"
    hae="120.5"
    ce="10.0"
    le="15.0"
  />
  <detail>
    <!-- optional sub-elements -->
  </detail>
</event>
```

### 2.2 `<event>` Attribute Reference

| Attribute | Type | Required | Notes |
|-----------|------|----------|-------|
| `version` | string | YES | Always `"2.0"` |
| `type` | string | YES | CoT type code — see Section 3 |
| `uid` | string | YES | Globally unique identifier. Must be stable across updates for the same entity. Use `DRONE-<serial>` or a UUID. |
| `how` | string | YES | How the position was derived — see Section 2.4 |
| `time` | datetime | YES | Time message was generated. W3C XML format: `YYYY-MM-DDTHH:MM:SS.sssZ` |
| `start` | datetime | YES | When the event becomes valid. Usually same as `time`. |
| `stale` | datetime | YES | When ATAK should remove the icon. `time + 120s` is a safe default. For fast-moving assets set 30–60s. |
| `access` | string | NO | MIL-STD-6090 classification. `"UNCLASSIFIED"` is the default. |
| `qos` | string | NO | Quality of service string. Rarely used. |
| `opex` | string | NO | Operational exercise flag. `"e-"` prefix for exercise. |

### 2.3 `<point>` Element Attributes

`<point>` is a **required child** of `<event>`. It carries the geospatial position.

| Attribute | Type | Required | Notes |
|-----------|------|----------|-------|
| `lat` | float | YES | WGS84 decimal degrees. Range: -90 to 90. |
| `lon` | float | YES | WGS84 decimal degrees. Range: -180 to 180. |
| `hae` | float | YES | Height above ellipsoid (WGS84), in metres. Use `9999999.0` if unknown. NOT altitude above sea level — convert if needed. |
| `ce` | float | YES | Circular error (horizontal accuracy), metres, 1-sigma. Use `9999999.0` if unknown. |
| `le` | float | YES | Linear error (vertical accuracy), metres, 1-sigma. Use `9999999.0` if unknown. |

**Important**: HAE (height above ellipsoid) differs from MSL by the geoid undulation at that location — typically 0–100m depending on region. If your drone gives MSL, you need to add the geoid offset. For quick work, `hae = msl_altitude + geoid_offset`. EGM96 tables give the offset; for UK it is approximately +45m to +55m.

### 2.4 `how` Attribute Values

The `how` attribute encodes the source of the data using a dotted hierarchy:

| Value | Meaning |
|-------|---------|
| `m-g` | Machine generated (GPS) — **use this for autonomous drone position** |
| `m-p` | Machine generated (predicted/dead-reckoning) |
| `h-g-i-g-o` | Human entered GPS observation |
| `h-e` | Human estimated |
| `a-f` | Assumed-friend (used in type, not how) |

For a drone reporting its own position via GPS: use `how="m-g"`.

### 2.5 `<detail>` Element

`<detail>` is optional but ATAK uses its sub-elements extensively for display. All sub-elements of `<detail>` are optional unless stated. Their attributes are shown as XML in the examples below.

---

## 3. CoT Event Type System

The `type` attribute uses a dotted atom hierarchy: `<affiliation>-<battle-dimension>-<function>-<modifier1>-<modifier2>...`

### 3.1 Atom 1: Affiliation

| Code | Meaning |
|------|---------|
| `a` | Atoms (real-world objects) |
| `b` | Bits (digital information) |
| `t` | Tasking |
| `r` | Reply |
| `c` | Capability |
| `u` | Unknown |

For real physical entities (drone, person, vehicle), use `a`.

### 3.2 Atom 2: Affiliation / Hostility

| Code | Meaning | ATAK Color |
|------|---------|-----------|
| `f` | Friendly | Cyan/Blue |
| `h` | Hostile | Red |
| `n` | Neutral | Green |
| `u` | Unknown | Yellow |
| `j` | Joker (friendly acting hostile) | Red |
| `k` | Faker (hostile acting friendly) | Red |
| `s` | Suspect | Orange |
| `p` | Pending | Yellow |

### 3.3 Atom 3: Battle Dimension

| Code | Meaning |
|------|---------|
| `A` | Air |
| `G` | Ground |
| `S` | Sea Surface |
| `U` | Subsurface |
| `F` | SOF (Special Operations Forces) |
| `X` | Other |

### 3.4 Complete CoT Types for UAV/Drone Operations

These are the practically relevant type strings:

```
# Friendly UAV / own drone position report
a-f-A-M-F-Q        # Friendly Air Military Fixed-wing UAV (Quadrotor)
a-f-A-M-H-Q        # Friendly Air Military Rotary-wing (Helicopter style)
a-f-A-C-F          # Friendly Air Civilian Fixed-wing

# Hostile / enemy air track
a-h-A              # Hostile Air (generic track)
a-h-A-M-F-Q        # Hostile Air Military Fixed-wing UAV
a-h-A-M-H-Q        # Hostile Rotary UAV

# Unknown air track (sensor return, unclassified)
a-u-A              # Unknown Air

# Ground entities
a-f-G-U-C          # Friendly Ground Unit (Command Post)
a-f-G-E-V          # Friendly Ground Vehicle
a-h-G-E-V          # Hostile Ground Vehicle
a-n-G              # Neutral Ground

# Waypoints / mission planning
b-m-p-w            # Waypoint (Map marker, basic)
b-m-p-w-GOTO       # Goto Waypoint
b-m-p-w-Chkpt      # Checkpoint
b-m-p-s-p-i        # IP (Initial Point)
b-m-r              # Route

# Sensor tracks and points of interest
b-m-p-s-p-op       # Observation Post
b-m-p-s-p-tgt      # Target
b-m-p-s-p-arp      # Air Reference Point
a-u-S-X-M          # Unknown Surface Maritime

# Alerts and emergency
b-a-o-tbl          # Area alert
b-a-o-can          # Cancel alert
b-a-g              # Alert (generic)

# System / heartbeat
t-x-d-d            # Hello / Ping (used for keepalive to TAK Server)
t-x-c-t            # Chat message

# Ground control / loitering zone
b-m-p-s-p-loc      # Location marker
b-m-p-s-p-POI      # Point of Interest
```

**Common UAV type breakdown example**: `a-f-A-M-F-Q`
- `a` = real-world atom
- `f` = friendly
- `A` = air battle dimension
- `M` = military
- `F` = fixed-wing
- `Q` = UAV/drone modifier

---

## 4. Transport Mechanisms

### 4.1 UDP Multicast (Mesh SA — standard ATAK-to-ATAK direct)

```
Address : 239.2.3.1
Port    : 6969
Protocol: UDP
Format  : TAK Protocol v0 (XML) or v1 Mesh (Protobuf)
TTL     : 1 (stays within local network segment)
```

This is what ATAK uses for local situational awareness without a server. Every ATAK device on the same network receives all multicast messages. Range is limited to the local LAN segment (TTL=1).

PyTAK default URL: `udp+wo://239.2.3.1:6969`

### 4.2 TCP Unicast to TAK Server

```
Port 8087  : Unencrypted TCP (legacy/insecure, avoid in production)
Port 8089  : TLS-encrypted TCP (PKCS#12 certificate required)
Port 8443  : HTTPS REST API
Port 8446  : Certificate enrollment (HTTPS)
```

PyTAK URL examples:
- `tcp://takserver.example.com:8087` (unencrypted)
- `tls://takserver.example.com:8089` (TLS with client cert)

### 4.3 UDP Broadcast (LAN-only fallback)

```
Port: 6969
URL : udp+broadcast://255.255.255.255:6969
```

### 4.4 UDP Unicast (direct to specific ATAK device)

```
URL: udp://192.168.1.50:4242
```

Default ATAK listener port is 4242 for unicast, 6969 for multicast.

### 4.5 Message Framing

- **UDP (multicast/broadcast/unicast)**: Each UDP datagram contains exactly one CoT XML message. No length prefix, no delimiter. Max UDP payload is 65507 bytes — well within any CoT message.
- **TCP**: Messages are newline or `</event>` delimited. PyTAK's `readcot()` reads until `</event>`.
- **TAK Protocol v1 Stream (TCP Protobuf)**: Prefixed with a varint length delimiter (`0xBF` magic byte + length + protobuf bytes).
- **TAK Protocol v1 Mesh (UDP Protobuf)**: 3-byte header `0xBF 0x01 0xBF` + raw protobuf bytes.

---

## 5. TAK Server Architecture and CoT Relay

TAK Server (commercial, from TAK.gov) and FreeTAK Server (open-source) act as **CoT brokers**:

```
[Drone/GCS] --CoT--> [TAK Server] --CoT--> [All connected ATAK clients]
                           |
                      [Persistence]
                      [Replay]
                      [Federation to other servers]
                      [REST API]
                      [Video streaming integration]
```

Key TAK Server roles:
1. **Relay**: Receives CoT from any connected client and re-broadcasts to all others — so you only need one TCP connection, not multicast
2. **Persistence**: Stores last-known position of all entities; new clients get full COP on connect
3. **Federation**: Multiple TAK Servers can peer and share selected CoT streams
4. **Data Packages**: Distributes mission files, imagery, KML over HTTPS
5. **Video**: Integrates with RTSP/RTMP streams via TAK Video Server

FreeTAK Server (open source, Python): github.com/FreeTAKTeam/FreeTAKServer — compatible with pytak, runs on TCP 8087, REST on 19023.

For a drone GCS you typically:
1. Connect to TAK Server on port 8087 (plain) or 8089 (TLS)
2. Send CoT position updates every 5–30 seconds
3. Send a `t-x-d-d` hello/ping on connect and periodically for keepalive

---

## 6. Open-Source Python Libraries

### 6.1 PyTAK (primary library)

```
pip install pytak
```

**Version**: 7.3.0 (March 2026)
**Source**: github.com/snstac/pytak (Apache 2.0)
**Author**: Greg Albrecht / Sensors & Signals LLC

Core functions (from installed source):

```python
import pytak

# Generate W3C XML datetime string (current UTC)
pytak.cot_time()            # "2026-03-27T14:30:00.000Z"
pytak.cot_time(120)         # current UTC + 120 seconds (for stale)

# Generate a minimal CoT XML bytes object
pytak.gen_cot(
    lat=51.3721,
    lon=-0.1740,
    hae=120.5,
    ce=10.0,
    le=15.0,
    uid="DRONE-001",
    stale=120,               # seconds from now
    cot_type="a-f-A-M-F-Q",
    callsign="ALPHA-1"
)

# Transport URL constant
pytak.DEFAULT_COT_URL        # "udp+wo://239.2.3.1:6969"
pytak.DEFAULT_COT_PORT       # "8087"
pytak.DEFAULT_BROADCAST_PORT # "6969"
```

Key classes:
- `pytak.QueueWorker` — subclass this, override `run()` to push CoT to `tx_queue`
- `pytak.TXWorker` — handles actual network write (created by `CLITool`)
- `pytak.RXWorker` — handles incoming CoT
- `pytak.CLITool` — orchestrates workers, queues, and asyncio event loop
- `pytak.COTEvent` — dataclass with all position fields

### 6.2 takproto (protobuf support)

```
pip install takproto
```

**Version**: 3.0.1
**Source**: github.com/snstac/takproto (MIT)

Used for converting CoT XML to TAK Protocol v1 Protobuf when transmitting over mesh links:

```python
from takproto import xml2proto, parse_proto, TAKProtoVer

# Convert XML CoT bytes to TAK Mesh protobuf (for UDP multicast)
proto_bytes = xml2proto(xml_bytes, TAKProtoVer.MESH)

# Convert XML CoT bytes to TAK Stream protobuf (for TCP)
proto_bytes = xml2proto(xml_bytes, TAKProtoVer.STREAM)

# Parse incoming protobuf message back to TakMessage object
tak_msg = parse_proto(raw_bytes)
```

Wire format headers:
- Mesh (UDP): `b"\xbf\x01\xbf"` + raw protobuf bytes
- Stream (TCP): `b"\xbf"` + varint length + protobuf bytes

### 6.3 FreeTAK Server (if running your own server)

```
pip install FreeTAKServer
```

Open-source TAK Server compatible. TCP port 8087, REST API port 19023.

---

## 7. Minimum Viable CoT Message

The absolute minimum that ATAK will display as an icon on the map:

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
<event version="2.0"
       type="a-f-A-M-F-Q"
       uid="DRONE-001"
       how="m-g"
       time="2026-03-27T14:30:00.000Z"
       start="2026-03-27T14:30:00.000Z"
       stale="2026-03-27T14:32:00.000Z">
  <point lat="51.3721" lon="-0.1740" hae="120.5" ce="10.0" le="15.0"/>
</event>
```

That is it. No `<detail>` required. ATAK will render a blue (friendly) air UAV icon at the given coordinates. The icon disappears when `stale` time passes.

---

## 8. Entity Types — Full Detail XML Examples

### 8.1 Friendly UAV — Own Drone Position Report

```xml
<event version="2.0" type="a-f-A-M-F-Q" uid="DRONE-ALPHA-001"
       how="m-g"
       time="2026-03-27T14:30:00.000Z"
       start="2026-03-27T14:30:00.000Z"
       stale="2026-03-27T14:31:00.000Z">
  <point lat="51.3721" lon="-0.1740" hae="120.5" ce="5.0" le="8.0"/>
  <detail>
    <contact callsign="ALPHA-1" endpoint="*:-1:stcp"/>
    <track speed="15.3" course="045.0"/>
    <status battery="87"/>
    <precisionlocation geopointsrc="GPS" altsrc="GPS"/>
    <takv device="ArduPilot" platform="DroneGCS" os="Linux" version="1.0.0"/>
    <remarks>Altitude: 120m AGL. Mission: Recon Alpha</remarks>
    <uid Droid="ALPHA-1"/>
  </detail>
</event>
```

Key `<detail>` sub-elements for a drone:
- `<contact callsign="..." endpoint="..."/>` — callsign is the display label in ATAK. endpoint is the network address for direct messaging; use `"*:-1:stcp"` if no direct contact.
- `<track speed="..." course="..."/>` — speed in m/s, course in degrees true (0–360). ATAK uses this to draw a velocity vector.
- `<status battery="87"/>` — battery percentage (0–100).
- `<precisionlocation geopointsrc="GPS" altsrc="GPS"/>` — tells ATAK the source of position data.
- `<takv device="..." platform="..." os="..." version="..."/>` — identifies the client software. ATAK shows this in the contact card.
- `<uid Droid="ALPHA-1"/>` — sets the display name shown under the icon.
- `<remarks>...</remarks>` — free text, shown in ATAK contact card.

### 8.2 Hostile Air Track (sensor-derived)

```xml
<event version="2.0" type="a-h-A-M-F-Q" uid="TRACK-H-00247"
       how="m-p"
       time="2026-03-27T14:30:00.000Z"
       start="2026-03-27T14:30:00.000Z"
       stale="2026-03-27T14:30:30.000Z">
  <point lat="51.4100" lon="-0.1200" hae="85.0" ce="25.0" le="30.0"/>
  <detail>
    <track speed="22.0" course="270.0"/>
    <remarks>Radar track. Classification: UAS. Confidence: HIGH</remarks>
  </detail>
</event>
```

Notes:
- `how="m-p"` — machine predicted (interpolated from sensor track)
- Short stale (30s) because sensor tracks go cold fast
- Higher CE/LE values reflecting radar accuracy limits
- No `<contact>` or `<takv>` since this is a track, not a known friendly

### 8.3 Mission Waypoint

```xml
<event version="2.0" type="b-m-p-w" uid="WPT-MISSION-001-003"
       how="h-g-i-g-o"
       time="2026-03-27T14:00:00.000Z"
       start="2026-03-27T14:00:00.000Z"
       stale="2026-03-27T23:59:59.000Z">
  <point lat="51.3850" lon="-0.1650" hae="0.0" ce="9999999.0" le="9999999.0"/>
  <detail>
    <remarks>WP3 — Loiter point. Hold 90s at 150m AGL.</remarks>
    <uid Droid="WP3-LOITER"/>
    <color argb="-256"/>
  </detail>
</event>
```

Notes:
- `type="b-m-p-w"` — map waypoint / planning item
- `how="h-g-i-g-o"` — human entered GPS observation
- Long stale for persistent mission markers
- `hae="0.0"` is fine for surface waypoints; ATAK treats this as ground level
- `<color argb="-256"/>` sets the icon colour; -256 = 0xFFFFFF00 = yellow

### 8.4 Sensor Point of Interest / Target

```xml
<event version="2.0" type="b-m-p-s-p-tgt" uid="TGT-EO-20260327-001"
       how="m-g"
       time="2026-03-27T14:30:00.000Z"
       start="2026-03-27T14:30:00.000Z"
       stale="2026-03-27T15:30:00.000Z">
  <point lat="51.3600" lon="-0.1800" hae="12.0" ce="3.0" le="5.0"/>
  <detail>
    <remarks>EO target acquired. DRONE-ALPHA-001 slant range: 320m. Bearing: 225 true.</remarks>
    <uid Droid="TGT-001"/>
    <color argb="-65536"/>
    <link uid="DRONE-ALPHA-001" type="a-f-A-M-F-Q" relation="p-p" remarks="Observing"/>
  </detail>
</event>
```

Notes:
- `type="b-m-p-s-p-tgt"` — target marker
- `<link .../>` — creates a relationship line in ATAK between this point and the drone icon
- `<color argb="-65536"/>` = 0xFFFF0000 = red
- High positional accuracy (CE=3m, LE=5m) appropriate for EO-derived coordinates

### 8.5 Alert / Emergency

```xml
<event version="2.0" type="b-a-o-tbl" uid="ALERT-GCS-001"
       how="m-g"
       time="2026-03-27T14:30:00.000Z"
       start="2026-03-27T14:30:00.000Z"
       stale="2026-03-27T14:35:00.000Z">
  <point lat="51.3721" lon="-0.1740" hae="0.0" ce="9999999.0" le="9999999.0"/>
  <detail>
    <remarks>LOST LINK — DRONE-ALPHA-001 last position. RTH initiated.</remarks>
    <uid Droid="ALERT-LOSTLINK"/>
  </detail>
</event>
```

---

## 9. Colour Encoding in CoT

ATAK `<color argb="..."/>` uses a signed 32-bit integer in ARGB order:

```python
def rgba_to_argb_int(r, g, b, a=255):
    """Convert RGBA to ATAK's signed ARGB integer."""
    argb = (a << 24) | (r << 16) | (g << 8) | b
    # Convert to signed 32-bit
    if argb >= 2**31:
        argb -= 2**32
    return argb

# Common colours
YELLOW  = rgba_to_argb_int(255, 255, 0)    # -256
RED     = rgba_to_argb_int(255, 0, 0)      # -65536
GREEN   = rgba_to_argb_int(0, 255, 0)      # 16711935 (note: positive)
BLUE    = rgba_to_argb_int(0, 0, 255)      # 4294901760 (wraps)
WHITE   = rgba_to_argb_int(255, 255, 255)  # -1
ORANGE  = rgba_to_argb_int(255, 165, 0)    # -23296
```

---

## 10. Complete Python Implementation

### 10.1 Minimal Send-Only (no PyTAK dependency)

```python
"""
cot_sender.py — Minimal CoT UDP multicast sender, no external dependencies.
Suitable for embedding directly in a drone GCS.
"""
import socket
import struct
import datetime
import uuid


MULTICAST_GROUP = "239.2.3.1"
MULTICAST_PORT  = 6969
TAK_SERVER_HOST = "192.168.1.100"
TAK_SERVER_PORT = 8087


def cot_time(offset_seconds: int = 0) -> str:
    """Return current UTC time as W3C XML datetime string."""
    t = datetime.datetime.now(datetime.timezone.utc)
    if offset_seconds:
        t += datetime.timedelta(seconds=offset_seconds)
    return t.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def build_drone_cot(
    uid: str,
    callsign: str,
    lat: float,
    lon: float,
    hae: float,
    ce: float = 10.0,
    le: float = 15.0,
    speed_ms: float = 0.0,
    course_deg: float = 0.0,
    battery_pct: int = -1,
    stale_seconds: int = 60,
    cot_type: str = "a-f-A-M-F-Q",
) -> bytes:
    """
    Build a CoT XML event for a drone position report.

    Returns UTF-8 encoded XML bytes ready to send over UDP or TCP.
    """
    t = cot_time()
    stale = cot_time(stale_seconds)

    track_xml = f'<track speed="{speed_ms:.2f}" course="{course_deg:.1f}"/>'
    battery_xml = f'<status battery="{battery_pct}"/>' if battery_pct >= 0 else ""

    xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>'
        f'<event version="2.0" type="{cot_type}" uid="{uid}" how="m-g" '
        f'time="{t}" start="{t}" stale="{stale}">'
        f'<point lat="{lat:.7f}" lon="{lon:.7f}" hae="{hae:.2f}" '
        f'ce="{ce:.1f}" le="{le:.1f}"/>'
        f'<detail>'
        f'<contact callsign="{callsign}" endpoint="*:-1:stcp"/>'
        f'{track_xml}'
        f'{battery_xml}'
        f'<precisionlocation geopointsrc="GPS" altsrc="GPS"/>'
        f'<uid Droid="{callsign}"/>'
        f'<remarks>lat={lat:.5f} lon={lon:.5f} hae={hae:.1f}m</remarks>'
        f'</detail>'
        f'</event>'
    )
    return xml.encode("utf-8")


def send_udp_multicast(data: bytes) -> None:
    """Send CoT bytes to ATAK multicast group."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, struct.pack("b", 1))
    sock.sendto(data, (MULTICAST_GROUP, MULTICAST_PORT))
    sock.close()


def send_tcp(data: bytes, host: str = TAK_SERVER_HOST, port: int = TAK_SERVER_PORT) -> None:
    """Send CoT bytes to a TAK Server over TCP."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5.0)
    sock.connect((host, port))
    sock.sendall(data)
    sock.close()


# --- Example usage ---
if __name__ == "__main__":
    import time

    drone_uid = f"DRONE-{uuid.uuid4().hex[:8].upper()}"

    while True:
        cot = build_drone_cot(
            uid=drone_uid,
            callsign="ALPHA-1",
            lat=51.37210,
            lon=-0.17400,
            hae=120.5,
            ce=5.0,
            le=8.0,
            speed_ms=15.3,
            course_deg=45.0,
            battery_pct=87,
            stale_seconds=30,
        )
        send_udp_multicast(cot)
        print(f"Sent CoT: {len(cot)} bytes")
        time.sleep(5)
```

### 10.2 Full PyTAK Integration (async, production-grade)

```python
"""
drone_cot_pytak.py — Production CoT sender using PyTAK.
Supports TCP, TLS, UDP multicast with proper async queue management.
"""
import asyncio
import datetime
import os
import uuid
import xml.etree.ElementTree as ET
from configparser import ConfigParser

import pytak


DRONE_UID      = os.getenv("DRONE_UID", f"DRONE-{uuid.uuid4().hex[:8].upper()}")
DRONE_CALLSIGN = os.getenv("DRONE_CALLSIGN", "ALPHA-1")
COT_URL        = os.getenv("COT_URL", "udp+wo://239.2.3.1:6969")
UPDATE_INTERVAL = int(os.getenv("UPDATE_INTERVAL", "10"))  # seconds


class DroneTelemetryWorker(pytak.QueueWorker):
    """
    Reads telemetry from your drone and sends CoT position reports.

    Override get_telemetry() to pull from MAVLink, serial port, etc.
    """

    async def get_telemetry(self) -> dict:
        """
        Replace this with real MAVLink / serial / REST telemetry.
        Returns dict with keys: lat, lon, hae, ce, le, speed_ms,
                                course_deg, battery_pct
        """
        # Stub — replace with real source
        return {
            "lat": 51.37210,
            "lon": -0.17400,
            "hae": 120.5,
            "ce": 5.0,
            "le": 8.0,
            "speed_ms": 15.3,
            "course_deg": 45.0,
            "battery_pct": 87,
        }

    def build_cot(self, tel: dict) -> bytes:
        """Construct CoT XML from telemetry dict."""
        t = pytak.cot_time()
        stale = pytak.cot_time(30)  # 30s stale for fast-moving asset

        event = ET.Element("event")
        event.set("version", "2.0")
        event.set("type", "a-f-A-M-F-Q")
        event.set("uid", DRONE_UID)
        event.set("how", "m-g")
        event.set("time", t)
        event.set("start", t)
        event.set("stale", stale)

        point = ET.SubElement(event, "point")
        point.set("lat", f"{tel['lat']:.7f}")
        point.set("lon", f"{tel['lon']:.7f}")
        point.set("hae", f"{tel['hae']:.2f}")
        point.set("ce", f"{tel['ce']:.1f}")
        point.set("le", f"{tel['le']:.1f}")

        detail = ET.SubElement(event, "detail")

        contact = ET.SubElement(detail, "contact")
        contact.set("callsign", DRONE_CALLSIGN)
        contact.set("endpoint", "*:-1:stcp")

        track = ET.SubElement(detail, "track")
        track.set("speed", f"{tel['speed_ms']:.2f}")
        track.set("course", f"{tel['course_deg']:.1f}")

        if tel.get("battery_pct", -1) >= 0:
            status = ET.SubElement(detail, "status")
            status.set("battery", str(tel["battery_pct"]))

        prec = ET.SubElement(detail, "precisionlocation")
        prec.set("geopointsrc", "GPS")
        prec.set("altsrc", "GPS")

        uid_el = ET.SubElement(detail, "uid")
        uid_el.set("Droid", DRONE_CALLSIGN)

        return pytak.DEFAULT_XML_DECLARATION + b"\n" + ET.tostring(event)

    async def run(self, _=-1) -> None:
        """Main loop — polls telemetry and queues CoT messages."""
        self._logger.info("DroneTelemetryWorker started. UID=%s", DRONE_UID)
        while True:
            tel = await self.get_telemetry()
            cot = self.build_cot(tel)
            await self.put_queue(cot)
            self._logger.debug("Queued CoT: %d bytes", len(cot))
            await asyncio.sleep(UPDATE_INTERVAL)

    async def handle_data(self, data: bytes) -> None:
        """Required override — not used for TX-only worker."""
        pass


async def main():
    config = ConfigParser()
    config["drone"] = {"COT_URL": COT_URL}

    clitool = pytak.CLITool(config["drone"])
    await clitool.setup()

    worker = DroneTelemetryWorker(clitool.tx_queue, config["drone"])
    clitool.add_task(worker)
    await clitool.run()


if __name__ == "__main__":
    asyncio.run(main())
```

### 10.3 Receiving Incoming CoT (for GCS situational awareness)

```python
class IncomingCoTHandler(pytak.RXWorker):
    """Parse incoming CoT events from ATAK users / other drones."""

    async def handle_data(self, data: bytes) -> None:
        try:
            root = ET.fromstring(data)
            uid = root.get("uid", "unknown")
            cot_type = root.get("type", "unknown")
            point = root.find("point")
            if point is not None:
                lat = point.get("lat")
                lon = point.get("lon")
                self._logger.info("RX CoT: uid=%s type=%s lat=%s lon=%s",
                                  uid, cot_type, lat, lon)
        except ET.ParseError as exc:
            self._logger.warning("Failed to parse incoming CoT: %s", exc)
```

---

## 11. Sending Waypoints / Mission Routes to ATAK

ATAK can receive mission waypoints as CoT events. For a multi-waypoint route:

```python
def build_waypoint(wp_num: int, lat: float, lon: float,
                   label: str, remarks: str = "") -> bytes:
    t = pytak.cot_time()
    stale = pytak.cot_time(86400)  # 24-hour persistence for mission markers

    event = ET.Element("event")
    event.set("version", "2.0")
    event.set("type", "b-m-p-w")          # waypoint type
    event.set("uid", f"MISSION-WP-{wp_num:03d}")
    event.set("how", "h-g-i-g-o")         # human/GCS planned
    event.set("time", t)
    event.set("start", t)
    event.set("stale", stale)

    point = ET.SubElement(event, "point")
    point.set("lat", f"{lat:.7f}")
    point.set("lon", f"{lon:.7f}")
    point.set("hae", "9999999.0")   # surface waypoint, unknown altitude
    point.set("ce", "9999999.0")
    point.set("le", "9999999.0")

    detail = ET.SubElement(event, "detail")
    uid_el = ET.SubElement(detail, "uid")
    uid_el.set("Droid", label)
    remarks_el = ET.SubElement(detail, "remarks")
    remarks_el.text = remarks

    return pytak.DEFAULT_XML_DECLARATION + b"\n" + ET.tostring(event)
```

To delete a waypoint from ATAK, send a CoT with `type="t-x-d-d"` targeting the waypoint's UID and include `<link uid="MISSION-WP-001" .../>` with a delete relation. More reliably: send the waypoint CoT with `stale` set to a past timestamp — ATAK will immediately remove it.

---

## 12. MAVLink to CoT Field Mapping

For ArduPilot / PX4 MAVLink integration:

| MAVLink Message | Field | CoT Field | Conversion |
|-----------------|-------|-----------|------------|
| `GLOBAL_POSITION_INT` | `lat / 1e7` | `point.lat` | direct |
| `GLOBAL_POSITION_INT` | `lon / 1e7` | `point.lon` | direct |
| `GLOBAL_POSITION_INT` | `alt / 1000.0` | `point.hae` | mm → m, then add geoid offset |
| `GLOBAL_POSITION_INT` | `relative_alt / 1000.0` | `<remarks>` | AGL altitude for display |
| `VFR_HUD` | `groundspeed` | `track.speed` | m/s direct |
| `VFR_HUD` | `heading` | `track.course` | degrees 0–360 |
| `SYS_STATUS` | `battery_remaining` | `status.battery` | direct (0–100) |
| `GPS_RAW_INT` | `eph / 100.0` | `point.ce` | hdop × 5 is a rough CE estimate |
| `GPS_RAW_INT` | `epv / 100.0` | `point.le` | vdop × 5 is a rough LE estimate |

---

## 13. Important Implementation Notes

### UID Stability
The `uid` attribute is the identity of an entity in ATAK. If you send two CoT messages with different UIDs for the same drone, ATAK creates two icons. If you update the same UID, ATAK updates the existing icon in place. Generate the UID once at startup and reuse it across all position reports.

### Stale Time Tuning
- Fast-moving asset (drone in flight): 30–60 seconds
- Slow asset (vehicle): 60–120 seconds
- Static marker (waypoint): 24+ hours
- If you miss a transmission cycle, the icon stays until stale expires, then disappears. Short stale = stale UI on packet loss. Long stale = ghost tracks linger.

### Update Rate
- ATAK multicast: 1 Hz is excessive and will flood small networks. 0.1–0.2 Hz (every 5–10s) is typical for position reports.
- TAK Server TCP: slightly higher rates are acceptable since it is unicast, but 0.2 Hz is still a good default.
- Track objects (hostile radar tracks): may need 1 Hz for smooth extrapolation.

### TCP Keepalive to TAK Server
Send a `t-x-d-d` (hello/ping) event every 30–60 seconds to keep the TCP connection alive. TAK Server disconnects idle clients. PyTAK sends this automatically on connect; you need to repeat it.

```python
# Hello event bytes
hello = pytak.hello_event("DRONE-001")   # produces t-x-d-d type event
```

### HAE vs AGL vs MSL
- CoT `hae` = height above WGS84 ellipsoid
- Most consumer GPS gives MSL (mean sea level)
- ArduPilot `GLOBAL_POSITION_INT.alt` is MSL
- ArduPilot `GLOBAL_POSITION_INT.relative_alt` is AGL (above home)
- For ATAK display: `hae = msl + geoid_undulation` (EGM96 table lookup, ~+45m to +55m in UK)
- For tactical use you can pass `msl` as `hae` and accept a small offset error — ATAK users understand this

### Classification / MIL-STD-6090
If operating in a military or sensitive context set:
```python
event.set("access", "UNCLASSIFIED")  # or SECRET, etc.
```
This attribute is passed through by TAK Server and visible in ATAK contact cards.

---

## 14. Quick Reference: Configuration for Common Scenarios

```ini
# config.ini

[drone]
# Scenario A: Local LAN (no TAK Server, ATAK devices on same WiFi)
COT_URL = udp+wo://239.2.3.1:6969

# Scenario B: Dedicated TAK Server (no TLS)
COT_URL = tcp://192.168.1.100:8087

# Scenario C: TAK Server with TLS (production)
COT_URL = tls://takserver.example.com:8089
PYTAK_TLS_CLIENT_CERT = /etc/tak/client.p12
PYTAK_TLS_CLIENT_PASSWORD = yourpassword

# Scenario D: FreeTAK Server
COT_URL = tcp://137.184.101.250:8087

# TAK Protocol: 0=XML (recommended), 1=Mesh Protobuf, 2=Stream Protobuf
TAK_PROTO = 0

# Stale time in seconds
COT_STALE = 60

# Disable hello event (if server doesn't want it)
PYTAK_NO_HELLO = False
```

---

## 15. Protobuf Wire Format (TAK Protocol v1) Reference

Only needed if using `TAK_PROTO=1` or `TAK_PROTO=2`. The protobuf schema (from ATAK-CIV source):

```
TakMessage {
  TakControl takControl = 1    # optional
  CotEvent   cotEvent   = 2    # optional
}

CotEvent {
  string type       = 1   # event type code
  string access     = 2   # optional classification
  string qos        = 3   # optional QoS
  string opex       = 4   # optional exercise flag
  string uid        = 5   # unique ID
  uint64 sendTime   = 6   # ms since epoch (= time attribute)
  uint64 startTime  = 7   # ms since epoch (= start attribute)
  uint64 staleTime  = 8   # ms since epoch (= stale attribute)
  string how        = 9
  double lat        = 10
  double lon        = 11
  double hae        = 12  # 999999 = unknown
  double ce         = 13  # 999999 = unknown
  double le         = 14  # 999999 = unknown
  Detail detail     = 15  # optional
}

Detail {
  string            xmlDetail         = 1  # remaining XML not in typed fields
  Contact           contact           = 2
  Group             group             = 3
  PrecisionLocation precisionLocation = 4
  Status            status            = 5
  Takv              takv              = 6
  Track             track             = 7
}

Contact { string endpoint=1; string callsign=2; }
Group   { string name=1;     string role=2; }
PrecisionLocation { string geopointsrc=1; string altsrc=2; }
Status  { uint32 battery=1; }
Takv    { string device=1; string platform=2; string os=3; string version=4; }
Track   { double speed=1; double course=2; }
```

TAKProto handles all of this automatically — just pass your XML to `xml2proto()`.

---

## 16. Integration Checklist

Before shipping a CoT module:

- [ ] UID is stable across reboots (store in config/NVRAM, not generated fresh each run)
- [ ] Stale time is appropriate for update rate (at least 2x the update interval)
- [ ] HAE source is documented (is it MSL, AGL, or true HAE?)
- [ ] CE and LE values reflect actual GPS accuracy, not defaults
- [ ] Callsign is unique and human-readable
- [ ] Battery percentage included when available
- [ ] Speed and course included in `<track>`
- [ ] Hello/ping sent to TAK Server on connect and every 30–60s
- [ ] Reconnection logic for TCP drops (use PyTAK's backoff or implement exponential retry)
- [ ] CoT validated by test-receiving on ATAK device or ATAK-X before deployment
- [ ] Classification field set correctly for operating environment
