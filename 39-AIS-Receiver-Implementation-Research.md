# AIS Receiver Implementation Research
## Practical Reference for a Python AIS Receiver Feeding a CoT-Based C2 Platform

**Purpose:** Practical implementation details for receiving, decoding, and converting AIS vessel tracks into Cursor-on-Target (CoT) events. Companion document to `38-CoT-Protocol-Deep-Dive.md` and `12-Naval-Maritime-Applications.md`.

---

## 1. What Is AIS?

Automatic Identification System (AIS) is a VHF broadcast system mandated by IMO (International Maritime Organization) under SOLAS for vessels over 300 GT on international voyages, cargo vessels over 500 GT on domestic voyages, and all passenger ships regardless of size. Smaller vessels and recreational craft use Class B transponders voluntarily.

AIS is a self-organizing TDMA (Time Division Multiple Access) system: every vessel claims time slots dynamically and broadcasts position data without any ground station infrastructure.

### Data Carried Per Vessel

Class A transponders (commercial mandatory) transmit:

| Field | Details |
|---|---|
| MMSI | 9-digit Maritime Mobile Service Identity — globally unique vessel ID, the primary tracking key |
| Vessel name | Up to 20 characters |
| Call sign | Up to 7 characters |
| IMO number | 7-digit unique ship number (stable across ownership changes) |
| Position (lat/lon) | WGS84 decimal degrees, accuracy to ~0.0001° (about 10 m) |
| Speed over ground (SOG) | 0 to 102.2 knots, 0.1 knot resolution |
| Course over ground (COG) | 0 to 359.9°, 0.1° resolution |
| True heading | 0 to 359°, 1° resolution; 511 when not available |
| Rate of turn | -127 to +127 (encoded; positive = turning right) |
| Navigational status | 0 = under way using engine, 1 = at anchor, 5 = moored, 15 = not defined — 16 values total |
| Type of ship/cargo | 2-digit code (see section 1.2) |
| Destination | Up to 20 characters |
| Estimated time of arrival (ETA) | Month, day, hour, minute in UTC |
| Draught | 0.1 m resolution, up to 25.5 m |
| Vessel dimensions | Length and beam in metres, with GPS antenna offset from bow/port |

Class B transponders (recreational/smaller vessels) transmit a reduced set: MMSI, name, call sign, ship type, dimensions, position, SOG, COG, heading. They omit IMO number, draught, destination, ETA, rate of turn, and navigational status.

### 1.2 Ship Type Codes (AIS Type of Ship Field)

The first digit of the 2-digit type code indicates the general category:

| First digit | Category |
|---|---|
| 2x | Wing In Ground (WIG) craft |
| 3x | Special category (fishing, tug, dredger, etc.) |
| 4x | High-Speed Craft (HSC) |
| 5x | Special — pilot vessel (50), search and rescue (51), tug (52), port tender (53), anti-pollution (54), law enforcement (55) |
| 6x | Passenger vessels |
| 7x | Cargo vessels |
| 8x | Tankers |
| 9x | Other — including fishing (30 is most common for fishing) |

The second digit gives sub-type (e.g., for tankers: 80 = tanker, 81 = hazardous A, 82 = hazardous B, 83 = hazardous C, 84 = hazardous D).

### 1.3 Broadcast Intervals

| Platform | Condition | Interval |
|---|---|---|
| Class A underway | Speed > 14 kn, changing course | 2 seconds |
| Class A underway | Speed 3–14 kn | 6 seconds |
| Class A underway | Speed < 3 kn | 10 seconds |
| Class A at anchor | — | 3 minutes |
| Class B | All | 30 seconds |
| Static data (type 5) | — | Every 6 minutes |

---

## 2. AIS Message Types

There are 27 defined AIS message types. The ones that matter for practical vessel tracking:

| Message Type | Name | Who Sends | Key Data |
|---|---|---|---|
| **1** | Position Report Class A | Class A underway | MMSI, status, turn, SOG, lat/lon, COG, heading, timestamp |
| **2** | Position Report Class A (Assigned) | Class A (assigned mode) | Same as type 1 |
| **3** | Position Report Class A (Response) | Class A (interrogated) | Same as type 1 |
| **4** | Base Station Report | AIS base stations | Position, time |
| **5** | Static and Voyage Related Data | Class A | MMSI, IMO, callsign, name, ship type, dimensions, destination, ETA, draught |
| **14** | Safety-Related Broadcast Message | Any station | Free text safety message |
| **18** | Standard Class B CS Position Report | Class B | MMSI, SOG, lat/lon, COG, heading |
| **21** | Aid-to-Navigation Report | Buoys, lighthouses | Position and nav aid name |
| **24** | Class B CS Static Data Report | Class B | Two parts: Part A = name; Part B = call sign, type, dimensions |
| **27** | Long Range AIS Broadcast | Satellites (S-AIS) | Compressed position; coarser precision (0.1°) |

For a coastal receiver, types 1, 2, 3, 18 will dominate by volume (~95%). Type 5 and 24 provide the identifying name/destination data. Type 21 marks nav aids (buoys, lights).

---

## 3. NMEA Sentence Format — Raw AIS Messages

AIS is delivered as NMEA 0183 sentences over serial/UDP/TCP. The relevant sentence identifiers are:

- `!AIVDM` — AIS data received from other vessels (the useful one for a receiver)
- `!AIVDO` — AIS data from your own transponder

### 3.1 Sentence Structure

```
!AIVDM,<count>,<fragment>,<seq>,<channel>,<payload>,<fill>*<checksum>
```

| Field | Position | Example | Meaning |
|---|---|---|---|
| Sentence ID | 1 | `!AIVDM` | AIS VDM sentence |
| Fragment count | 2 | `1` | Total fragments in this message (1 for most, 2 for type 5) |
| Fragment number | 3 | `1` | This fragment's sequence number |
| Sequential ID | 4 | `` (empty) | Used for multi-fragment reassembly; empty for single-fragment |
| Channel | 5 | `A` | VHF channel — `A` = 161.975 MHz, `B` = 162.025 MHz |
| Payload | 6 | `177KQJ5000G?tO\`K>RA1wUbN0TKH` | 6-bit ASCII encoded AIS bitfield |
| Fill bits | 7 | `0` | Pad bits added to complete the last 6-bit boundary (0–5) |
| Checksum | 8 | `*5C` | NMEA XOR checksum |

### 3.2 Real Examples

**Single-fragment Type 1 (Class A position report):**
```
!AIVDM,1,1,,B,177KQJ5000G?tO`K>RA1wUbN0TKH,0*5C
```

**Two-fragment Type 5 (static data — splits across two sentences):**
```
!AIVDM,2,1,3,B,55?MbV02Ah;ac<D4eK@Dh4j0Xt4iN22222220l1@D634ov0EPEp0000,0*32
!AIVDM,2,2,3,B,00000000000,2*25
```

**Type 18 Class B position report:**
```
!AIVDM,1,1,,B,B52KlJh00Fc>jpUk9HhdqonV06Cd,0*16
```

### 3.3 Payload Encoding

The payload is a 6-bit ASCII encoding of the raw AIS bit stream. To decode a character: subtract 48 from the ASCII value; if the result is greater than 40, subtract 8 more. This gives a 6-bit value (0–63). Concatenate all 6-bit values to get the full message bitfield. Message type (bits 0–5), repeat indicator (bits 6–7), and MMSI (bits 8–37) are always in the same location regardless of message type.

This decoding is handled entirely by libraries — do not implement it manually.

---

## 4. Python Libraries for AIS Decoding

### 4.1 pyais (Recommended)

**GitHub:** `M0r13n/pyais` | **PyPI:** `pyais` | **Status: Actively maintained**

pyais is the clear choice for new Python projects. As of 2025–2026 it is at version 2.15+ with regular releases, 20+ contributors, and active issue resolution.

**Capabilities:**
- Pure Python (no C dependencies), installs cleanly via pip
- Decodes all 27 AIS message types
- Accepts: single NMEA strings, file streams, TCP sockets, UDP sockets
- Handles multi-fragment message reassembly automatically
- Output via `.asdict()` returns a flat Python dict with all decoded fields
- `AISTracker` class maintains per-vessel state over time (merges type 1 position updates with type 5 static data)
- CLI tool for quick file decoding and socket connection
- Can encode AIS messages (for testing/simulation)

**Input sources:**
- `decode()` — single raw NMEA string
- `FileReaderStream` — reads NMEA log files
- `TCPConnection` — connects to TCP server outputting NMEA (e.g., AIS-catcher TCP output)
- `UDPReceiver` — listens on UDP port for incoming NMEA sentences

**Output dict keys for Type 1 example:** `msg_type`, `mmsi`, `status`, `turn`, `speed`, `accuracy`, `lon`, `lat`, `course`, `heading`, `second`, `maneuver`, `raim`

**Output dict keys for Type 5 example:** `msg_type`, `mmsi`, `imo`, `callsign`, `shipname`, `ship_type`, `to_bow`, `to_stern`, `to_port`, `to_starboard`, `eta`, `draught`, `destination`

### 4.2 libais

**PyPI:** `libais` | **Status: Largely unmaintained, last updated ~2018**

C-based library with Python bindings. Was widely used pre-pyais but the binding layer is fragile and it breaks on newer Python versions. Only consider if pyais cannot decode an edge-case message type.

### 4.3 ais-decoder (C++ with Python bindings)

**GitHub:** `aduvenhage/ais-decoder` | **Status: Niche, not widely used**

C++ core with Python wrappers. Faster than pure Python but the Python interface is minimal. Not worth the integration complexity over pyais for this use case.

### 4.4 AIS-catcher's Built-in JSON Decoder

AIS-catcher can output `JSON_FULL` directly — a fully decoded JSON object per vessel update — which means you can bypass NMEA parsing entirely if AIS-catcher is your SDR frontend. This is a valid architecture: AIS-catcher → UDP JSON → Python consumer. However, pyais remains useful if you also want to process NMEA feeds from AISHub or a hardware AIS receiver (e.g., dAISy).

### Recommendation

Use **pyais** via `TCPConnection` or `UDPReceiver` pointing at AIS-catcher's TCP/UDP NMEA output. This gives you the cleanest separation: AIS-catcher handles SDR + demodulation, pyais handles NMEA parsing and decoding, your Python code handles CoT conversion and forwarding.

---

## 5. Hardware for Receiving AIS

### 5.1 RTL-SDR + AIS-catcher (Software Path)

The RTL-SDR dongle is a USB DVB-T TV tuner chip (RTL2832U) repurposed as a general-purpose SDR. It covers roughly 500 kHz – 1.7 GHz, making it trivially capable of receiving 161–162 MHz AIS.

**Recommended hardware:**

| Component | Recommended Model | Approx. Cost (2025) |
|---|---|---|
| SDR dongle | RTL-SDR Blog V4 (R828D tuner, 1PPM TCXO, SMA connector) | ~$30–35 USD / ~£28–32 |
| Antenna | Included dipole kit (basic, works at short range) | Included |
| Marine-grade antenna | Shakespeare AIS antenna or homemade coax collinear | £15–£60 |
| LNA (optional) | Nooelec LaNA or RTL-SDR Blog LNA4ALL | £20–£35 |
| SMA coax cable | RG58 or LMR-200, 5–10 m | £5–£15 |
| **Total basic kit** | Dongle + included dipole | **~£30** |
| **Total optimised kit** | Dongle + marine antenna + LNA + coax | **~£85–£100** |

**RTL-SDR V4 vs V3:** The V4 introduced direct sampling for HF, a better TCXO, and improved USB noise shielding. Both work for AIS. V4 is preferred for a new build.

**Antenna notes:** A collinear coax antenna (DIY from RG-58, multiple quarter-wave sections) significantly outperforms the included dipole. Mount as high as possible — antenna elevation is the dominant factor in AIS range. A marine VHF whip antenna (e.g., Shakespeare 5400-S) screws directly to an SMA adapter and is the easiest high-quality option.

### 5.2 Dedicated AIS Hardware Receivers

If SDR complexity is not desired, dedicated AIS receiver modules exist and output NMEA sentences directly:

| Device | Interface | Output | Cost |
|---|---|---|---|
| **dAISy 2+** (Wegmatt) | USB or Serial | NMEA 0183 (serial stream) | ~$80 USD |
| **dAISy HAT** (Raspberry Pi HAT) | GPIO/UART | NMEA 0183 | ~$50 USD |
| **Vesper Cortex M1** | Ethernet, USB, NMEA | NMEA 0183 + JSON | ~$500 USD |
| **NASA Marine AIS Engine** | USB | NMEA 0183 | ~£150 |

The dAISy 2+ is widely used by hobbyists and professionals. It receives both AIS channels simultaneously (true dual-channel hardware demodulation), outputs standard NMEA, and works with pyais directly via serial port.

### 5.3 AIS Range

| Antenna height | Typical range | Exceptional (elevated site) |
|---|---|---|
| 2 m (ground level) | 5–10 NM | — |
| 15 m (typical shore station) | 15–20 NM | — |
| 50–100 m elevated | 30–40 NM | — |
| 700 m hilltop | Up to 200 NM | Proven by MarineTraffic |

The dominant factor is antenna height, not receiver quality. For a UAV-mounted AIS receiver at 300–1000 m altitude, range would be 40–80 NM — comparable to a professional shore station. This is why airborne AIS is so valuable for maritime patrol.

---

## 6. Software: AIS-catcher on macOS

AIS-catcher (`jvde-github/AIS-catcher`) is the recommended SDR demodulator for AIS. It simultaneously demodulates both AIS channels (161.975 MHz and 162.025 MHz) in a single RTL-SDR capture, outperforms older `rtl_ais`, and supports multiple output formats.

### 6.1 macOS Installation

macOS (Sonoma/Sequoia) does not have a Homebrew AIS-catcher formula, so compilation from source is required. Recent macOS is described by the AIS-catcher maintainer as "extremely Homebrew adverse" — some library path issues arise, particularly with RTL-SDR V4.

**Dependency chain via Homebrew:**
```
xcode-select --install
brew install git make gcc cmake pkg-config sqlite3
brew install librtlsdr       # RTL-SDR library + drivers
```

Then clone and build AIS-catcher:
```
git clone https://github.com/jvde-github/AIS-catcher.git --depth 1
cd AIS-catcher && mkdir build && cd build
cmake ..
make -j4
sudo make install
```

Known macOS-specific issue: "no LC_RPATH's found" errors during rtl-sdr compilation — requires passing `-DCMAKE_INSTALL_RPATH_USE_LINK_PATH=ON` to cmake when building rtl-sdr from source.

### 6.2 AIS-catcher Output Modes (Relevant to Python Integration)

| Output flag | What it sends | Use case |
|---|---|---|
| `-o <file>` | NMEA sentences to file | Logging |
| `-u <host> <port>` | NMEA sentences via UDP | Feed pyais UDPReceiver |
| `-P <port>` | TCP server, NMEA sentences | Feed pyais TCPConnection |
| `-H <url>` | HTTP POST of JSON | Web dashboard |
| `JSON_FULL` modifier | Fully decoded JSON per message | Direct JSON consumer |
| `JSON_NMEA` modifier | JSON wrapper around raw NMEA | Preserves NMEA + metadata |

**Recommended pipeline:**
```
AIS-catcher → UDP port 10110 (NMEA) → pyais UDPReceiver → CoT converter → TAK Server UDP/TCP
```

### 6.3 Alternative: rtl_ais

`rtl_ais` (`dgiardini/rtl-ais`) is an older single-tool option. It installs via Homebrew (`brew install rtl-ais` on some systems) and outputs NMEA directly to stdout. It is simpler but has weaker decoding performance than AIS-catcher. Use AIS-catcher.

---

## 7. AIS Web APIs (No Hardware Path)

If local SDR reception is not immediately available, web APIs provide AIS data for testing and development:

### 7.1 AISHub

**URL:** `aishub.net` | **Cost:** Free (requires membership + data sharing agreement)

AISHub is a cooperative network: you share your station's received AIS data and get access to the aggregated feed. API returns XML, JSON, or CSV. Filter by geographic bounding box, MMSI, or IMO. Rate limited (typically 1 request per minute on free tier). Good for development and testing. No continuous streaming on free tier.

### 7.2 MarineTraffic

**URL:** `marinetraffic.com` | **Cost:** Paid API, no free tier for developers

Comprehensive commercial service. APIs cover live positions, port calls, vessel particulars, voyage history. Pricing is per-credit or subscription. For a development/research project, cost is prohibitive. Web scraping their map is against ToS.

### 7.3 VesselFinder / VesselTracker / Spire Maritime

All commercial paid APIs. Spire Maritime (`spire.com`) is notable for satellite AIS (S-AIS) coverage of vessels beyond coastal reception range — useful for open-ocean tracking but expensive.

### 7.4 NOAA AIS Data (Historical, USA waters)

The NOAA Marine Cadastre project (`hub.marinecadastre.gov/pages/vesseltraffic`) provides free downloadable historical AIS data in CSV format. Useful for training ML models or testing CoT pipelines without a live feed.

### 7.5 OpenCPN + GPSd (Local Network)

If you have a hardware AIS receiver (dAISy, Vesper), OpenCPN can relay NMEA over TCP/UDP on a local network. pyais can connect directly.

---

## 8. AIS to CoT Mapping

### 8.1 Existing Tool: aiscot

**GitHub:** `snstac/aiscot` | **PyPI:** `aiscot` | **Status: Actively maintained (v7.x as of 2025)**

`aiscot` (by Greg Albrecht / SNSTAC) is a production-ready AIS-to-CoT gateway. It is worth studying its source code to understand the mapping logic, and it can be used directly rather than reinventing the wheel:

- Accepts AIS from: AISHub (internet), NMEA UDP/TCP, serial port (dAISy)
- Outputs CoT to: TAK Server UDP/TCP, ATAK multicast
- Supports hints files (CSV) to override CoT type, callsign, or icon per MMSI
- Written in Python using pyais + pytak

### 8.2 CoT Type Codes for Surface Vessels

The CoT type string structure is: `<atom>-<affiliation>-<battle-dimension>[-<function-codes>]`

From `38-CoT-Protocol-Deep-Dive.md`, the battle dimension for surface vessels is `S` (Sea Surface). For vessels of unknown identity/affiliation (the default for all AIS contacts), use:

| CoT Type | Meaning | ATAK Display |
|---|---|---|
| `a-u-S` | Unknown Sea Surface (generic) | Yellow diamond |
| `a-u-S-X-M` | Unknown Surface Maritime | Yellow diamond |
| `a-f-S` | Friendly Sea Surface | Cyan/blue |
| `a-n-S` | Neutral Sea Surface | Green |
| `a-h-S` | Hostile Sea Surface | Red |
| `a-f-S-X-M` | Friendly Surface Maritime | Cyan diamond |
| `a-n-S-X-M` | Neutral Surface Maritime | Green diamond |

**Practical default:** Use `a-n-S` (neutral surface) for all unidentified commercial vessels. This is what aiscot uses by default — civilian vessels are not hostile and not allied, so neutral is the correct affiliation. Reserve `a-u-S` for contacts where vessel type is genuinely unknown (e.g., a receiver picking up a Class B MMSI with no name). Use `a-f-S` only for vessels positively identified as friendly (e.g., coalition naval vessels with known MMSIs in a whitelist).

### 8.3 AIS Field to CoT Field Mapping

| AIS Field | CoT Destination | Notes |
|---|---|---|
| `lat`, `lon` | `<point lat lon>` | Direct; AIS is already WGS84 |
| `heading` / `COG` | `<track course>` | Use true heading if available, COG otherwise |
| `SOG` (knots) | `<track speed>` | Convert: m/s = knots × 0.514444 |
| `MMSI` | `uid` | Format: `AIS-<MMSI>` (stable across updates) |
| `shipname` | `callsign` in `<contact>` | Displayed as label in ATAK |
| `callsign` | `<contact callsign>` | Radio callsign |
| `ship_type` | CoT type modifier or custom icon | Map AIS type code to CoT function code |
| `navigational_status` | Remarks or `<status>` | "At anchor", "Moored", etc. |
| `destination` | `<remarks>` | Free text in ATAK popup |
| `draught` | `<remarks>` | Useful context |
| `stale` time | AIS update interval × 2–3 | Class A: 30–60s stale; Class B: 90s stale |

### 8.4 UID Convention

CoT `uid` must be stable (ATAK uses it to update the existing icon rather than create a duplicate). The correct convention used by aiscot is:

```
uid = f"AIS-{mmsi}"
```

This means every position update from MMSI 123456789 always updates the same ATAK icon, regardless of which AIS message fragment it came from.

### 8.5 how Attribute

AIS position data is GPS-derived, machine-generated: use `how="m-g"`.

### 8.6 stale Time

AIS contacts should go stale if no update is received within a reasonable window:
- Class A vessels: 60–120 seconds (they transmit every 2–30s, so >60s without update is meaningful)
- Class B vessels: 90–180 seconds (they transmit every 30s)
- Set `stale = time_of_message + timedelta(seconds=120)` as a safe default

### 8.7 CoT Detail Block for Vessels

```xml
<detail>
  <track course="247.5" speed="5.14"/>       <!-- speed in m/s, course in degrees -->
  <contact callsign="VESSEL_NAME"/>
  <remarks>MMSI: 123456789 | Type: Cargo | Dest: ROTTERDAM | Draught: 6.5m | Status: Underway</remarks>
  <color argb="-1"/>                          <!-- optional: white icon outline -->
</detail>
```

---

## 9. Legal Considerations (UK)

### 9.1 Receiving AIS

**Receiving AIS is legal in the UK without any licence.** AIS is a broadcast system — ITU Radio Regulations and UK/Ofcom rules require vessels to transmit AIS for safety purposes, and reception by shore stations, other vessels, and monitoring services is not only permitted but explicitly the intended design.

The UK Wireless Telegraphy Act 2006 restricts *transmitting* without a licence, not receiving. Passive reception of AIS (or any VHF maritime radio) requires no Ofcom licence. This is the same legal basis that allows amateur radio operators to listen to shortwave broadcasts, aircraft ADS-B, and NOAA weather satellites without restriction.

### 9.2 AISHub Data Sharing

AISHub's free tier requires you to share your received data back to their network. This is a cooperative model — your shore station's coverage contributes to the global picture. Technically straightforward: AIS-catcher has a built-in AISHub feed mode.

### 9.3 Transmitting AIS

Transmitting AIS (operating a transponder) requires a Ship Radio Licence from Ofcom (costs ~£25/year for small vessels) and a VHF marine radio operator certificate (Short Range Certificate, SRC). A drone-mounted AIS transponder that transmits would need to be covered under a ship licence for the vessel operating it. An AIS receiver payload on a drone does **not** require any licence.

### 9.4 Data Privacy

MMSI numbers and vessel positions are publicly broadcast. There is no privacy expectation for AIS-transmitted data. MarineTraffic, VesselFinder, and dozens of other services legally display this data commercially. Using it for a C2 display is entirely lawful.

---

## 10. Integration Architecture for the Drone C2 Platform

### 10.1 Shore-Based Reception Pipeline

```
VHF Antenna (marine collinear, elevated)
    ↓ coax (SMA)
RTL-SDR Blog V4 (USB)
    ↓ USB
AIS-catcher (macOS/RPi)
    ↓ UDP NMEA port 10110
pyais UDPReceiver (Python process)
    ↓ decoded AIS dicts
CoT Converter (Python)
    ↓ CoT XML
PyTAK / UDP/TCP
    ↓
TAK Server → ATAK / WinTAK clients
```

### 10.2 UAV-Mounted AIS Reception

For the drone platform itself, a dAISy 2+ or dAISy HAT on a Raspberry Pi CM4 provides dual-channel AIS reception from altitude. Output: NMEA serial → pyais → CoT → downlinked over Doodle Labs datalink to ground station → forwarded to TAK Server. At 300–1000 m altitude the drone's AIS receiver will detect vessels at 40–80 NM range, dramatically extending coverage beyond any shore station.

Integration with ArduPilot: the NMEA stream from dAISy can be parsed by the companion computer and correlated with the drone's own GPS to calculate range/bearing to each AIS contact, enabling the mission engine to autonomously cue the camera or trigger a loiter-orbit around a vessel of interest.

### 10.3 AISHub as Development Feed (No Hardware Needed)

During development, connect pyais to AISHub's data feed over TCP to get live real-world AIS data without SDR hardware. When hardware is available, switch the TCPConnection target to your local AIS-catcher instance. The pyais interface is identical.

---

## 11. Key References and Source Libraries

| Resource | URL | Purpose |
|---|---|---|
| pyais GitHub | `github.com/M0r13n/pyais` | Primary Python AIS decoder |
| pyais docs | `pyais.readthedocs.io` | API documentation |
| aiscot GitHub | `github.com/snstac/aiscot` | AIS-to-CoT gateway (study source) |
| aiscot docs | `aiscot.readthedocs.io` | Configuration reference |
| AIS-catcher GitHub | `github.com/jvde-github/AIS-catcher` | SDR demodulator |
| AIS-catcher docs | `docs.aiscatcher.org` | Full configuration reference |
| GPSD AIVDM reference | `gpsd.gitlab.io/gpsd/AIVDM.html` | Definitive bit-level field reference for all 27 message types |
| USCG NavCen AIS | `navcen.uscg.gov/ais-messages` | Official US Coast Guard message specs |
| USCG AIS Class A report | `navcen.uscg.gov/ais-class-a-reports` | Type 1/2/3 field definitions |
| USCG AIS Class B report | `navcen.uscg.gov/ais-class-b-reports` | Type 18 field definitions |
| USCG Type 5 | `navcen.uscg.gov/ais-class-a-static-voyage-message-5` | Static data message |
| AISHub API | `aishub.net/api` | Free tier data API |
| RTL-SDR AIS tutorial | `rtl-sdr.com/rtl-sdr-tutorial-cheap-ais-ship-tracking` | Hardware setup walkthrough |
| MarineTraffic range FAQ | `support.marinetraffic.com` | AIS reception range reference |

---

*Companion documents: `38-CoT-Protocol-Deep-Dive.md`, `12-Naval-Maritime-Applications.md`, `24-Ground-Station-Software-Architecture.md`*
