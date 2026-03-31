# NATO Interoperability Standards: Implementation Requirements
*Research document for mpe-c2 team. Author: INTEROP agent. Date: 2026-03-31.*
*Covers: STANAG 4586 (UAV interop), STANAG 4677 / NFFI (friendly force tracking), Link 16 / JREAP gateways.*
*Status: READ-ONLY reference for CORE and COP to implement against.*

---

## 1. STANAG 4586 — Standard Interfaces of UAV Control System (UCS)

### What It Is

STANAG 4586 is the NATO standard that defines the architecture, interfaces, communication protocols, data elements, and message formats required for NATO UAV interoperability. Its purpose is to allow any STANAG-4586-compliant Ground Control Station (GCS) to control any STANAG-4586-compliant UAV regardless of manufacturer.

The current edition is Edition 4 (ratified; Edition 5 was in draft as of 2024).

### Architecture

The standard defines seven elements and the interfaces between them:

```
┌─────────────────────────────────────────────────────────────────┐
│                    CORE UCS (CUCS)                              │
│  ┌──────────────────┐         ┌────────────────────────────┐   │
│  │  HCI             │         │  CCISM                     │   │
│  │  Human Computer  │         │  Command & Control          │   │
│  │  Interface       │         │  Interface Specific Module  │   │
│  └──────────────────┘         └──────────────┬─────────────┘   │
│                                              │ CCI              │
└──────────────────────────────────────────────┼─────────────────┘
                                               │
                                    ┌──────────▼──────────┐
                                    │     VSM             │
                                    │  Vehicle Specific   │
                                    │  Module             │
                                    │  (the translator)   │
                                    └──────────┬──────────┘
                                               │ DLI
                                    ┌──────────▼──────────┐
                                    │    Data Link        │
                                    └──────────┬──────────┘
                                               │
                                    ┌──────────▼──────────┐
                                    │    Air Vehicle (AV) │
                                    └─────────────────────┘
```

**Key interfaces:**
- **DLI (Data Link Interface)**: Between the data link and the VSM
- **VSM (Vehicle Specific Module)**: The crucial translator — converts STANAG 4586 messages to/from the UAV's native protocol (MAVLink, custom, etc.)
- **CCI (Command and Control Interface)**: Between VSM and Core UCS — this is where the standard message set lives
- **HCI (Human Computer Interface)**: Between Core UCS and the human operator

### Levels of Interoperability (LOI)

STANAG 4586 defines five LOIs. A GCS/platform declares which LOIs it supports:

| LOI | Capability |
|-----|-----------|
| 1 | Indirect receipt/transmission of data via separate C2 system |
| 2 | Direct receipt of ISR and other data (receive-only) |
| 3 | Control of UAV payload (camera, sensors) — no flight control |
| 4 | Control of UAV flight path (waypoint commands, return-to-home) |
| 5 | Full control including launch and recovery |

**For the MPE platform:** Initial target is LOI 3 (payload/sensor data receipt) and LOI 4 (flight path commands via the MAVLink bridge). LOI 5 requires hardware integration (catapult, landing system) — not relevant for initial release.

### VSM: The MAVLink Bridge

This is the most actionable part for CORE. A VSM is a software module that sits between the STANAG 4586 message bus and the UAV's native protocol. There are existing open-source implementations:

- **SkyView VSM for MAVLink**: A commercial VSM from UAS Europe that translates STANAG 4586 ↔ MAVLink. Allows any STANAG 4586 GCS to control ArduPilot/PX4 drones. Architecture: Raspberry Pi running the bridge software, connected to the drone via MAVLink serial/UDP and to the GCS via the STANAG 4586 DLI.

- **python-stanag-4586-vsm** (GitHub: `faisalthaheem/python-stanag-4586-vsm`): Open-source Python VSM. Proof-of-concept quality — useful for understanding the message structure, not production-ready.

- **IEEE paper** "Unmanned systems interoperability in military maritime operations: MAVLink to STANAG 4586 bridge" (IEEE Xplore, DOI: 10.1109/8084866) — academic implementation reference.

**Implementation requirement for CORE:** The `task_translator.py` module already converts TaskPlan → MAVLink MissionItems. A STANAG 4586 VSM layer would sit above this, accepting STANAG 4586 CCI messages and converting them into the internal TaskPlan format. This is a **future milestone** (post-MVP), but the architecture should not preclude it.

### Message Format (Relevant Subset)

STANAG 4586 messages are binary, not XML. They use fixed-length fields. The relevant message categories:

| Message Category | Content |
|-----------------|---------|
| VSM Capabilities | What the drone supports (LOIs, payload types) |
| Vehicle State | Position, attitude, speed, fuel, payload status |
| Mission Upload | Waypoints, loiter patterns, survey grids |
| Payload Control | Camera gimbal, zoom, IR/EO switch |
| Emergency | Abort, return-to-home, controlled crash |

### Gap Assessment for MPE

| STANAG 4586 Requirement | MPE Current State | Gap |
|------------------------|------------------|-----|
| VSM for MAVLink bridge | Not implemented | Must build or integrate SkyView VSM |
| CCI message parser | Not implemented | Binary protocol parser required |
| LOI declaration | Not implemented | Static capability advertisement needed |
| Multi-UAV coordination | Not implemented | Track manager handles entities but not command routing |

**Recommendation for CORE:** Do not implement full STANAG 4586 from scratch. Evaluate licensing SkyView VSM (commercial) or contributing to/forking `python-stanag-4586-vsm` as the bridge layer. The internal TaskPlan model is close enough to map to STANAG 4586 mission messages.

---

## 2. STANAG 4677 / NFFI — NATO Friendly Force Information

### What NFFI Is

NATO Friendly Force Information (NFFI), defined under STANAG 4677 and technically specified in STANAG 5527, is an XML-based message format for exchanging friendly force tracks between NATO and national Force Tracking Systems (FTS). It is the NATO standard for the "blue picture" — where your own forces are.

STANAG 4677 covers dismounted soldier C4 interoperability. STANAG 5527 carries the actual NFFI XML schema (version 1.4 is current in operational use).

### NFFI Message Structure

An NFFI message is XML, rooted at `<NFFI>`, containing zero or more `<track>` elements of type `trackType`.

```xml
<NFFI>
  <track>
    <positionalData>
      <trackSource>GBR-001</trackSource>       <!-- Unique source ID -->
      <dateTime>2026-03-31T12:00:00Z</dateTime> <!-- ISO 8601, UTC -->
      <latitude>51.3632</latitude>              <!-- Decimal degrees WGS-84 -->
      <longitude>-0.2652</longitude>
      <altitude>50</altitude>                   <!-- Metres MSL -->
      <speed>5.2</speed>                        <!-- m/s -->
      <heading>245</heading>                    <!-- Degrees true -->
      <positionalAccuracy>10</positionalAccuracy><!-- Metres -->
    </positionalData>
    <identificationData>
      <unitID>GBR-A-1-1</unitID>               <!-- NATO unit designation -->
      <unitName>1 PARA A Coy</unitName>
      <nationalIdentification>GBR</nationalIdentification>
      <affiliation>FRIEND</affiliation>         <!-- FRIEND / NEUTRAL / HOSTILE / UNKNOWN -->
      <category>GROUND</category>              <!-- AIR / SURFACE / SUB / GROUND / SPACE -->
      <unitType>INFANTRY</unitType>
    </identificationData>
    <operStatusData>
      <operationalStatus>OPERATIONAL</operationalStatus>
      <missionStatus>IN_PROGRESS</missionStatus>
    </operStatusData>
    <deviceSpecificData>
      <!-- Optional: device manufacturer extensions -->
    </deviceSpecificData>
    <detailData>
      <!-- Optional: non-standard extensions -->
    </detailData>
  </track>
</NFFI>
```

**Key technical constraints:**
- Track uniqueness is by `(trackSource, dateTime)` — same source, same timestamp = same track (idempotent update)
- Each `<track>` has exactly one `<positionalData>` element
- The schema is at: `http://community.rti.com/sites/default/files/STANAG5527_NFFI14_original.xsd`
- Coordinates: WGS-84 decimal degrees, altitude in metres MSL
- Datetime: ISO 8601 UTC

### Transport

NFFI is typically transported over:
- **Web Services** (SOAP/XML over HTTPS) — used for tactical-level integration
- **DDS (Data Distribution Service)** — RTI Connext, used for high-frequency track updates (pub-sub)
- **Multicast UDP** — for low-bandwidth environments

For the MPE platform, the pragmatic approach is NFFI-over-HTTPS as a REST-compatible XML endpoint. This is what most modern coalition interoperability connectors expect.

### Relationship to CoT

NFFI and CoT carry similar data — both represent entity position tracks with identification and status. The mapping is:

| NFFI Field | CoT Equivalent |
|-----------|---------------|
| `trackSource` | `<uid>` attribute on `<event>` |
| `dateTime` | `time` + `stale` attributes |
| `latitude/longitude` | `<point lat="..." lon="...">` |
| `altitude` | `<point hae="...">` (HAE = height above ellipsoid) |
| `affiliation` | 2nd character of CoT type (e.g., `a-f-` = air-friendly) |
| `category` | 3rd character of CoT type (a = air, g = ground, s = surface) |
| `unitID` | `<contact callsign="...">` in `<detail>` |

**Implementation requirement for COP:** The COP dashboard should be able to ingest NFFI XML from allied systems in addition to CoT. An NFFI→CoT converter would be a thin XML transformation layer that maps fields per the table above.

### Implementation Requirement for CORE

CORE should add an `NFFIReceiver` that:
1. Accepts NFFI XML messages via HTTP POST endpoint (or multicast UDP)
2. Parses `<track>` elements using the field mapping above
3. Creates `Observation` objects for each track
4. Feeds observations into `TrackManager` like any other source

The existing `cot_receiver.py` pattern is directly applicable — same structure, different XML format.

---

## 3. Link 16 / JREAP Gateways

### What Link 16 Is

Link 16 is the primary NATO tactical data link. It runs over JTIDS/MIDS radio waveforms in the L-band (960–1215 MHz), uses TDMA (time-division multiple access) time slots, and carries J-series messages defined by MIL-STD-6016 (US) / STANAG 5516 (NATO).

**It is not directly accessible to non-military systems.** The radios require cryptographic keys (TRANSEC), are export-controlled under ITAR (US) / UK military list, and access requires specific NATO approvals. This is a long-term integration milestone, not an MVP requirement.

### JREAP — The IP Bridge

JREAP (Joint Range Extension Applications Protocol), defined in MIL-STD-3011 and STANAG 5518, is the mechanism for carrying Link 16 J-series messages over IP networks. This is how Link 16 data gets from the radios to software systems.

**JREAP-C is the relevant variant:**
- Uses UDP or TCP over standard IP
- Supports both IPv4 and IPv6
- Carries J-series messages (the same binary 75-bit message words as Link 16)
- Low-latency (UDP preferred for real-time tracks)
- Used by military C2 systems to receive Link 16 data via LAN/WAN rather than directly via JTIDS radio

```
JTIDS/MIDS Radio ──→ Link 16 Crypto Gateway ──→ JREAP-C UDP/IP ──→ MPE
       (RF layer)         (MIL hardware)              (IP network)
```

### J-Series Message Format (Relevant Subset)

J-series messages are binary. Each message word is 75 bits (padded to 80 bits for transmission). A message consists of a header word plus variable-length data words.

Key J-series message categories relevant to MPE:

| Message Series | Content | Example |
|---------------|---------|---------|
| J2.x | Air track data | Aircraft position, heading, speed, IFF |
| J3.x | Surface/subsurface tracks | Ship tracks |
| J7.x | Land point/track | Ground force positions |
| J12.x | Mission assignment | Tasking messages |
| J14.x | Weapon coordination | Weapons free/safe, engagement status |

**For MPE:** J2 (air) and J3 (surface) are directly relevant — they carry the same information as ADS-B and AIS but from military sensor networks. J7 adds ground force picture.

### Commercial Gateway Products

Two commercial products translate between Link 16 / JREAP-C and CoT/TAK:

**Curtiss-Wright HUNTR:**
- Translates: Link 16 ↔ VMF ↔ CoT ↔ JREAP ↔ SADL ↔ CESMO
- Architecture: Dedicated hardware appliance or VMware VM
- Can automatically forward J2/J3 tracks as CoT to a TAK Server
- Market: US/NATO militaries; export-controlled

**SAIC JRE Gateway:**
- Translates JREAP-C to CoT and other formats
- Provides a graphical UI for monitoring J-series traffic
- Used in US military C2 networks

### What This Means for MPE

MPE does **not** need to implement Link 16 or JREAP natively. The practical integration path is:

1. A military customer already has a JREAP-C gateway (Curtiss-Wright HUNTR or equivalent)
2. That gateway outputs CoT to a TAK Server
3. MPE's existing `cot_receiver.py` ingests those CoT events
4. MPE enriches them (classification, alerting, pattern-of-life) and outputs back to TAK

**This means full Link 16 integration is available today via the CoT receiver — as long as the customer has a JREAP↔CoT gateway.** MPE doesn't need to speak JREAP directly.

**Longer-term (if direct JREAP-C integration is required):**

The JREAP-C protocol is an IP protocol — JREAP messages are structured binary packets over UDP/TCP. The binary format is specified in MIL-STD-3011 (US DoD document, not freely available but accessible through DTIC). An open-source JREAP-C decoder does not appear to exist. This would require:
1. Obtaining MIL-STD-3011 via DTIC
2. Implementing a binary parser for J-series message words
3. Mapping J2/J3 message fields to MPE's `Observation` model

**Implementation recommendation for CORE:** Document the CoT-via-gateway path as the standard integration. Add a note in the operator manual that JREAP-C direct integration requires MIL-STD-3011 and appropriate authorisation. Do not invest engineering time here until a specific customer demands it.

---

## 4. Summary: Implementation Requirements for CORE and COP

### CORE (mission-planning-engine/src/mpe/)

| Requirement | Priority | Module | Notes |
|------------|----------|--------|-------|
| NFFI XML receiver | HIGH | `nffi_receiver.py` (new) | HTTP POST endpoint + field mapping to Observation |
| NFFI→CoT converter | HIGH | `nffi_cot_bridge.py` (new) | XML transform using field mapping table above |
| STANAG 4586 VSM interface | MEDIUM | `stanag4586_vsm.py` (new) | Integrate SkyView VSM or fork python-stanag-4586-vsm |
| Link 16 via CoT gateway | LOW/NOW | Already works | cot_receiver.py handles CoT from HUNTR gateway |
| JREAP-C native parser | FUTURE | `jreap_receiver.py` | Only if direct integration required by customer |

### COP (dashboard)

| Requirement | Priority | Notes |
|------------|----------|-------|
| NFFI track display | HIGH | Parse NFFI XML; display tracks using same MIL-STD-2525D renderer as CoT tracks |
| LOI indicator on drone entities | MEDIUM | Show which STANAG 4586 LOI level the drone supports |
| J-series track origin badge | LOW | Tag tracks that arrived via JREAP gateway with "LINK 16" source label |

---

## 5. Key References

- STANAG 4586: [NATO STO Educational Note STO-EN-SCI-271-03](https://publications.sto.nato.int/publications/STO%20Educational%20Notes/STO-EN-SCI-271/EN-SCI-271-03.pdf)
- STANAG 4586 overview: [Wikipedia](https://en.wikipedia.org/wiki/STANAG_4586)
- VSM/MAVLink bridge: [UAS Europe SkyView VSM](https://www.uas-europe.se/index.php/component/content/article/skyview-vsm-mavlink-uavs)
- Python VSM: [github.com/faisalthaheem/python-stanag-4586-vsm](https://github.com/faisalthaheem/python-stanag-4586-vsm)
- NFFI XSD schema (STANAG 5527 v1.4): [community.rti.com](http://community.rti.com/sites/default/files/STANAG5527_NFFI14_original.xsd)
- NFFI web services paper: [ICCRTS 2008](http://www.dodccrp.org/events/13th_iccrts_2008/presentations/052.pdf)
- JREAP Wikipedia: [Wikipedia](https://en.wikipedia.org/wiki/JREAP)
- Link 16 Wikipedia: [Wikipedia](https://en.wikipedia.org/wiki/Link_16)
- Curtiss-Wright HUNTR: [Aviation Defence Universe](https://www.aviation-defence-universe.com/curtiss-wright-intelligent-tactical-data-link-translation-gateway-improves-and-simplifies-real-time-warfighter-communications/)
- NISP Catalogue (NATO interoperability profiles): [nhqc3s.hq.nato.int](https://nhqc3s.hq.nato.int/apps/nisp/NISP_Baseline_16_Catalogue_5SEP2024_enclosure_only.pdf)
