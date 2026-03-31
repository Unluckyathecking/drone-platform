# CoT / TAK Ecosystem Integration Requirements
*Research document for mpe-c2 team. Author: INTEROP agent. Date: 2026-03-31.*
*Covers: FreeTAK Server vs official TAK Server, ATAK plugin development, certificate management.*
*Status: READ-ONLY reference for CORE and COP to implement against.*

---

## 1. The TAK Ecosystem: Overview

TAK (Team Awareness Kit) is the US military situational awareness platform, originally built by ATAK Systems (now TAK.gov). It consists of:

- **ATAK**: Android Tactical Assault Kit — Android app, the primary client
- **WinTAK**: Windows client (laptop/desktop use)
- **iTAK**: iOS client (limited features)
- **TAK Server**: The central broker — routes CoT events between clients, manages users/groups, stores tracks
- **CoT Protocol**: The XML/Protobuf message format everything speaks

In 2020, the US DoD open-sourced the ATAK civilian variant (**ATAK-CIV / CivTAK**) on GitHub at `github.com/deptofdefense/AndroidTacticalAssaultKit-CIV`. This is the basis for all non-military ATAK development.

The TAK ecosystem is the de facto UI layer for MPE. The engine outputs CoT; ATAK consumes it. This is the architecture decision from the 2026-03-28 session.

---

## 2. TAK Server Options Compared

There are three viable server options:

### A. Official TAK Server (tak.gov)

**What it is:** The production TAK Server software, maintained by the US government (TAKY/TAK Server). Available from tak.gov after agreeing to US government terms and conditions.

**Capability:**
- Full federation support (server-to-server CoT routing)
- Certificate enrollment (ATAK auto-downloads client certs from server)
- Data Package Server (maps, overlays, mission packages)
- Missions/Tasks API (server-managed collaborative tasks)
- Video streaming integration
- Plugin distribution
- Advanced access control (group-based visibility)
- Latest version as of 2024: TAK Server 5.2

**Limitations for MPE:**
- US government T&Cs apply — restricts redistribution
- Java/Spring-based — heavier than alternatives
- Requires proper configuration; not trivial to deploy
- Some plugins only available after signing US government agreements

**Use case for MPE:** Integration testing against official TAK Server is important for validation. Any customer with an existing TAK deployment will be running official TAK Server. MPE must be compatible.

**TAK Server 5.2 Configuration Guide:** Available at the URL in the references section — covers TLS setup, certificate generation, federation configuration.

### B. FreeTAK Server (FTS)

**What it is:** Open-source Python TAK Server, maintained by the FreeTAKTeam community. GitHub: `github.com/FreeTAKTeam/FreeTakServer`. Eclipse Public License.

**Architecture:**
- Python 3 + Flask/asyncio
- Runs on Linux, macOS, Windows, Raspberry Pi
- Optional: Node-RED integration for workflow automation
- Optional: FTS UI (web dashboard)
- Zero-touch installer available

**Capability:**
- CoT event routing between ATAK clients
- Chat relay
- File/data package sharing
- Basic user management
- API for external integration (this is what MPE uses)
- Automated SSL certificate generation (self-signed CA)

**Key limitation vs official TAK Server:**
- No certificate enrollment (ATAK clients must manually import certs)
- No missions API
- No video streaming
- Less mature federation support
- Community-supported only

**Use case for MPE:** Development and testing. FreeTAK Server is what you stand up in Docker to verify the engine's CoT output appears on ATAK. It's also the right recommendation for resource-constrained customers (African coast guards, small peacekeeping units) who cannot afford official TAK Server infrastructure.

**FTS Feature comparison page:** `freetakteam.github.io/FreeTAKServer-User-Docs/About/FeaturesCompared/`

### C. OpenTAK Server

**What it is:** Another open-source TAK server alternative, distinct from FreeTAK. Lighter weight. Certificate enrollment support. Documentation at `docs.opentakserver.io`.

**Use case:** Worth evaluating as an alternative to FreeTAK for self-hosted deployments. Has certificate enrollment which FreeTAK lacks.

### Recommendation for MPE

| Purpose | Server |
|---------|--------|
| Development/CI testing | FreeTAK Server (Docker, easiest to stand up) |
| Demo to potential customers | FreeTAK Server + FTS UI dashboard |
| Integration testing (final validation) | Official TAK Server 5.2 |
| Customer deployment (large military) | Customer's own TAK Server — MPE connects to it |
| Customer deployment (small/budget) | Recommend FreeTAK Server or OpenTAK Server |

---

## 3. Certificate Management

This is the single most important operational detail. Every TAK connection — client to server, server to server, MPE to TAK Server — requires TLS certificates. Without correct certs, ATAK will refuse to connect.

### Architecture

TAK Server operates as its own Certificate Authority (CA). It issues:
1. **Server certificate**: presented by TAK Server to clients connecting via TLS
2. **Client certificates**: issued to each ATAK device — proves the device identity to the server
3. **Truststore**: the CA's public certificate — both server and clients need this to validate each other

This is mutual TLS (mTLS). Both parties authenticate.

### Certificate Flow for MPE → TAK Server Connection

```
1. TAK Server generates its CA (one-time setup)
2. TAK Server issues a client certificate for MPE (via admin UI or API)
3. MPE loads: ca-cert.pem + client-cert.p12 + client-key.pem
4. MPE connects to TAK Server with mTLS
5. TAK Server validates MPE's cert against its CA
6. MPE validates TAK Server cert against the CA it trusts
```

For MPE's `cot_sender.py` and `cot_output.py`, this means adding SSL context support:

```python
# What CORE needs to add to cot_output.py / cot_sender.py:
import ssl
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
ssl_context.load_cert_chain('client-cert.pem', 'client-key.pem')
ssl_context.load_verify_locations('ca-cert.pem')
# Then use ssl_context when opening TCP socket
```

### FreeTAK Server Certificate Setup

FTS has automated SSL generation. The relevant commands (from FTS documentation):

```bash
# FTS generates a CA and server cert on first run
# Admin then downloads client certs from FTS web interface
# Or uses the automated SSL generation endpoint:
curl http://FTS_IP:19023/api/SystemUser/Certificate \
     -H "Authorization: Bearer TOKEN" \
     --output atak_client_cert.zip
```

The cert zip contains:
- `truststore-root.p12` — the CA cert, imported into ATAK truststore
- `user.p12` — the client cert, imported into ATAK as user cert

Password for both is typically `atakatak` by default (must be changed in production).

### ATAK Certificate Import Process

On the ATAK device:
1. Transfer both `.p12` files to the Android device
2. ATAK → Settings → Network → Manage Server Connections → Add Server
3. Enter server address, port (typically 8089 for SSL, 8087 for TCP)
4. Import Truststore: select `truststore-root.p12`, password
5. Import Client Cert: select `user.p12`, password
6. Connect

Alternatively: bundle both certs into a `.zip` data package, which ATAK imports via the Import Manager.

### Certificate Gotchas

Based on research into common issues:

1. **SAN (Subject Alternative Name) required**: ATAK checks the certificate's SAN field, not just CN. If the server cert doesn't have a SAN matching the server's IP or hostname, ATAK will reject it. OpenSSL default self-signed certs often lack SAN — FTS's automated generation handles this; manual OpenSSL commands must explicitly add `-ext SAN=IP:x.x.x.x`.

2. **ATAK truststore validation**: ATAK validates the server cert against the loaded truststore. The CA cert in the truststore must be the issuer of the server cert. If you rotate the server cert with a different CA, all clients must re-import the new truststore.

3. **pytak and TLS**: The `cot_sender.py` in MPE uses pytak. pytak supports TLS via the URL scheme: `tcps://server:8089` (SSL) vs `tcp://server:8087` (plaintext). The SSL cert paths are passed as pytak configuration.

4. **External CA option**: Let's Encrypt certificates work with TAK Server — useful for publicly accessible servers. Requires a domain name. Guide at: `mytecknet.com/lets-sign-our-tak-server/`

---

## 4. ATAK Plugin Development

### Architecture

ATAK is an Android app. Plugins are companion APKs that extend ATAK via the ATAK SDK. A plugin:
- Runs in the same process as ATAK (not a separate app)
- Has access to the ATAK map, CoT event bus, tools API
- Can add map overlays, UI panels, hardware integrations
- Built with Android Studio + ATAK CIV SDK

### Why MPE Should Build an ATAK Plugin (Eventually)

The current MPE architecture: engine → CoT → TAK Server → ATAK. ATAK shows tracks as icons on the map. This is the minimum viable integration and it's what the next session should validate.

However, a plugin would allow:
- Custom UI panels (SITREP text, alert list, entity details)
- Direct connection to the MPE Operator API (REST)
- Custom map overlays (geofences, pattern-of-life zones, predicted tracks)
- Push classification data into the ATAK track detail view
- Receive operator commands and forward to MPE

This is a **medium-term** milestone. The plugin is the product's UI layer once the engine is validated.

### Development Setup

**Requirements:**
- Android Studio (Hedgehog or later recommended)
- ATAK CIV SDK — available at `tak.gov` (requires account) or from `github.com/deptofdefense/AndroidTacticalAssaultKit-CIV` (CIV version)
- JDK 17
- Android SDK API 33+
- A physical Android device or emulator running ATAK CIV

**Project structure:**
```
atak-plugin/
├── app/                   # Plugin APK module
│   ├── src/main/
│   │   ├── java/          # Plugin Java/Kotlin code
│   │   └── res/           # Plugin resources
│   └── build.gradle
├── local.properties       # Keystore paths (DO NOT COMMIT)
└── build.gradle
```

**Key local.properties entries:**
```properties
takDebugKeyFile=../debug.keystore
takDebugKeyFilePassword=android
takDebugKeyAlias=androiddebugkey
takDebugKeyPassword=android
takReleaseKeyFile=../release.keystore
takReleaseKeyFilePassword=<release_password>
takReleaseKeyAlias=release
takReleaseKeyPassword=<release_password>
```

**Generate debug keystore:**
```bash
keytool -genkey -v -keystore debug.keystore \
        -alias androiddebugkey -keyalg RSA -keysize 2048 \
        -validity 10000 -storepass android -keypass android \
        -dname "CN=Android Debug,O=Android,C=US"
```

### ATAK Plugin API — Relevant Hooks

The plugin connects to ATAK via the `ATAKActivity` lifecycle. Key APIs for MPE:

```java
// Register to receive all CoT events
ATAKPlugin.registerCotListener(cotListener);

// Add a map item (track, geofence polygon, etc.)
MapGroup rootGroup = mapView.getRootGroup();
CotMapAdapter.addEntityToMap(cotEvent, rootGroup);

// Add custom detail view for a track
MapItem item = mapView.findItem(uid);
item.setMetaString("mpe_threat_level", "8");
item.setMetaString("mpe_classification", "HOSTILE");

// Open a custom side panel
AtakBroadcast.getInstance().sendBroadcast(
    new Intent("com.atakmap.app.SHOW_SIDE_PANE")
        .putExtra("component", MPESidePane.class.getName())
);
```

### Open Source Plugin Examples

Useful reference implementations on GitHub:
- `github.com/deptofdefense/AndroidTacticalAssaultKit-CIV` — the full ATAK CIV source
- `github.com/9M2PJU/ATAK-Civ-Plugins` — compiled list of CIV plugins
- `github.com/FreeTAKTeam/openTAKpickList` — comprehensive TAK tools list
- `github.com/kdudkov/goatak` — Go-based ATAK server + client (useful for understanding the protocol)
- CotMaker plugin (from CivTAK resources) — minimal example of creating CoT from coordinates

### Plugin Signing for Distribution

To distribute a plugin to ATAK users:
1. Sign APK with a release keystore
2. For official TAK (not CIV), the plugin must be listed on tak.gov — requires US DoD agreement
3. For CivTAK, sideloading is permitted — distribute the APK directly
4. For customer deployments, the APK goes in a TAK Server Data Package and is pushed to all clients automatically

**For MPE:** Sideload the APK during demos. Once the platform matures, evaluate tak.gov listing. Non-US customers (target market) will sideload anyway.

---

## 5. Integration Test Plan: FreeTAK Server + MPE

This is the "demo-or-die" test from the 2026-03-28 session next steps list.

### Step 1: Stand Up FreeTAK Server

```bash
docker run -d \
  --name fts \
  -p 8087:8087 \   # TCP CoT (plaintext)
  -p 8089:8089 \   # TCP CoT (TLS)
  -p 8080:8080 \   # FTS web UI
  -p 19023:19023 \ # FTS API
  freetakteam/freetakserver:latest
```

Default admin credentials: check FTS docs (typically admin/password).

### Step 2: Configure ATAK Client

1. Install ATAK CIV on Android device
2. Add server: Settings → Network → Add Server → `tcp://FTS_IP:8087` (plaintext first, then switch to TLS)
3. Verify ATAK connects and shows green status

### Step 3: Run MPE Engine Pointing at FTS

```bash
cd /Users/mohammedalibhai/Documents/Drone\ project/mission-planning-engine
source .venv/bin/activate
PYTHONPATH=src python -m mpe \
  --adsb-center 51.3632,-0.2652 \
  --cot-url udp://FTS_IP:8087 \
  --callsign MPE-ENGINE \
  --log-level INFO
```

### Step 4: Verify Tracks Appear on ATAK

- Open ATAK on device
- Should see aircraft tracks appearing as CoT icons on map
- Hostile classifications should appear as red icons
- Alerts should generate CoT alert events

### Step 5: Switch to TLS

1. Download client certs from FTS admin UI
2. Import into ATAK
3. Change engine `--cot-url` to `tcps://FTS_IP:8089`
4. Add cert paths to engine config
5. Re-verify all tracks appear

---

## 6. Key References

- FreeTAK Server GitHub: [github.com/FreeTAKTeam/FreeTakServer](https://github.com/FreeTAKTeam/FreeTakServer)
- FreeTAK Server docs: [freetakteam.github.io/FreeTAKServer-User-Docs](https://freetakteam.github.io/FreeTAKServer-User-Docs/)
- FreeTAK vs official comparison: [FeaturesCompared](https://freetakteam.github.io/FreeTAKServer-User-Docs/About/FeaturesCompared/)
- OpenTAK Server cert enrollment: [docs.opentakserver.io](https://docs.opentakserver.io/certificate_enrollment.html)
- TAK Server 5.2 Configuration Guide: [squarespace link](https://static1.squarespace.com/static/5404b7d2e4b0feb6e5d9636b/t/6756e17b053bbe305668a08f/1733747077204/TAK_Server_Configuration_Guide_5.2.pdf)
- ATAK CIV source: [github.com/deptofdefense/AndroidTacticalAssaultKit-CIV](https://github.com/deptofdefense/AndroidTacticalAssaultKit-CIV)
- ATAK plugin development guide: [toyon.github.io/LearnATAK](https://toyon.github.io/LearnATAK/docs/setup/atak_plugin/)
- ATAK plugin tutorial (Ballantyne): [ballantyne.online](https://www.ballantyne.online/developing-atak-plugin-101/)
- Certificate SAN issue: [goatak truststore issue](https://github.com/kdudkov/goatak/issues/18)
- External CA for TAK Server: [mytecknet.com](https://mytecknet.com/lets-sign-our-tak-server/)
- TAK ecosystem overview: [Hackaday article](https://hackaday.com/2022/09/08/the-tak-ecosystem-military-coordination-goes-open-source/)
- FreeTAK SSL generation: [freetakteam.github.io SSL docs](https://freetakteam.github.io/FreeTAKServer-User-Docs/administration/SSL/)
- ATAK-Certs tool: [github.com/lennisthemenace/ATAK-Certs](https://github.com/lennisthemenace/ATAK-Certs)
