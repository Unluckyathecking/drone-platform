# Palantir AIP Military Architecture: Technical Deep-Dive

*Compiled from Palantir official documentation, public GitHub (osdk-ts), defence press, SEC filings references, and programme reporting. Last updated: March 2026.*

---

## Executive Summary

Palantir's military AI platform is not a single product but a stack of layered technologies:

1. **Foundry** — the data integration, transformation, and storage substrate
2. **The Ontology** — a semantic property-graph sitting above raw data, representing real-world entities
3. **AIP (AI Platform)** — LLM integration and agent orchestration sitting above the Ontology
4. **Gotham** — the defence/intelligence-specific application layer built on Foundry/Ontology
5. **Apollo** — the software delivery engine that pushes all of the above to edge/air-gapped environments
6. **TITAN** — a specific hardware+software ground station contract the Army awarded Palantir in April 2023

The architecture is designed around one key insight: LLMs should never touch raw data directly. Every AI interaction is mediated through the Ontology, which enforces access controls, provides semantic grounding, and converts natural-language intent into typed, validated operations.

---

## 1. The Ontology — Technical Architecture

### What It Is

The Ontology is Palantir's core abstraction. It sits "on top of the digital assets integrated into the platform (datasets, virtual tables, and models) and connects them to real-world entities." It is best understood as a **typed property graph** with mandatory access-control metadata — not RDF/OWL (no inference engine), not a pure graph database, but a schema-enforced, access-controlled knowledge graph integrated into a distributed data platform.

### Object Types

An object type is defined by the `ObjectTypeDefinition` interface (from the open-source `osdk-ts` repo):

```typescript
interface ObjectTypeDefinition {
  type: "object";
  apiName: string;           // e.g. "MilitaryVehicle", "Person", "AircraftTrack"
  primaryKeyApiName?: string;
  primaryKeyType?: PrimaryKeyTypes;  // string | integer | long | boolean | double
  __DefinitionMetadata?: ObjectMetadata & ObjectInterfaceCompileDefinition;
}
```

The `ObjectMetadata` includes:
- `apiName`, `displayName`, `description`, `rid` (resource identifier)
- `properties`: Record of property names → `Property` objects
- `links`: Record of link names → typed relationships to other ObjectTypes
- `primaryKeyApiName`, `primaryKeyType`
- `titleProperty`: which property is the human-readable label
- `status`: ACTIVE | EXPERIMENTAL | DEPRECATED | ENDORSED
- `interfaceMap`, `inverseInterfaceMap`: bidirectional maps for polymorphism via Interfaces

**Military object types** (inferred from documentation and use-case descriptions) would include: `Vehicle`, `Person`, `Location`, `Incident`, `Track`, `Signal`, `Sensor`, `Target`, `Mission`, `Unit`, `Asset`, `Alert`, `IntelligenceReport`.

### Property Types

The complete set of supported wire property types (from `WirePropertyTypes.ts`):

| Category | Types |
|---|---|
| Primitive | `string`, `boolean`, `integer`, `long`, `short`, `double`, `float`, `decimal`, `byte` |
| Temporal | `datetime`, `timestamp` |
| Specialised | `marking`, `mediaReference`, `attachment` |
| Time-series | `numericTimeseries`, `stringTimeseries`, `sensorTimeseries` |
| Geospatial | `geopoint`, `geoshape`, `geotimeSeriesReference` |
| ML | `vector` (embedding vector) |
| Complex | `Record<string, BaseWirePropertyTypes>` (nested structs) |

The `geopoint` and `geoshape` types are central to military use: a `Vehicle` object has a `geopoint` property representing its last known position, and a `geotimeSeriesReference` property pointing to its full movement history as a time-series.

The `marking` type is Palantir's mandatory-access-control label — it carries classification markings (SECRET, TOP SECRET, NOFORN, etc.) as a property on individual objects, not just on datasets.

The `vector` type enables semantic search: objects can have embedding vectors attached, allowing the retrieval system to find semantically similar objects using cosine similarity.

### Link Types

Links connect objects with typed, directional, cardinality-aware edges:

```typescript
// From LinkDefinitions.ts
type SingleLinkAccessor<T> = {
  fetchOne(args?: SelectArg): Promise<T>;
  fetchOneWithErrors(args?: SelectArg): Promise<Result<T>>;
};

// Multi-link: returns an ObjectSet (queryable collection)
type MultiLinkAccessor<T> = ObjectSet<T>;
```

Cardinality is encoded in the link definition: `M extends false` = single link (many-to-one), `M extends true` = multi-link (one-to-many or many-to-many).

**Military link examples:**
- `Vehicle → LINKED_TO → Track` (many-to-one: a vehicle's current track)
- `Track → HAS_WAYPOINTS → TrackPoint[]` (one-to-many)
- `Person → AFFILIATED_WITH → Organization` (many-to-one)
- `Target → COVERED_BY → Sensor[]` (many-to-many)
- `MilitaryUnit → COMMANDS → MilitaryUnit[]` (hierarchical, self-referential)

### Interfaces (Polymorphism)

Interfaces allow multiple concrete object types to satisfy a common contract:

```
Interface: MovingObject
  properties: geopoint, heading, speed, lastSeen
  implemented by: Vehicle, Aircraft, Vessel, Person, Drone
```

This is how a query like "show me all fast-moving objects within 5km of grid reference X" can work across object types without knowing the specific type at query time.

### How Sensors Feed the Ontology

The data pipeline is: **Sensor → Data Connection → Stream/Dataset → Transform Pipeline → Ontology Object**

1. **Data Connection layer**: 200+ connectors including Kafka, Kinesis, Pub/Sub for streaming sensor data; REST APIs for tactical systems; CDC for database feeds.

2. **Streams**: Real-time data flows from sensor hardware (via Kafka topics, typically) into Foundry "Streams" — similar to datasets but designed for continuous data. Streams support Flink-based stream processing (Palantir calls this "streaming compute") for windowing, aggregation, and enrichment.

3. **Pipeline Builder / Transforms**: Python (PySpark), SQL, or Java transforms normalise and enrich raw sensor data. For FMV (full-motion video), frames are processed through ML models (computer vision) in container transforms that output structured detections.

4. **Ontology Writeback**: Processed data is written to ontology objects through **Actions** (the write API). A transform can call an action to create or update a `Track` object with new position data.

5. **Time Series**: Sensor readings (radar cross-section, signal strength, temperature, coordinates over time) attach to objects as time-series properties. The `sensorTimeseries` wire type stores sequences of timestamped numeric values. These are queryable through the Ontology API with time-range filters.

### How Analysts Query the Ontology

Three primary interfaces:

**1. Workshop (no-code application layer)**: Drag-and-drop application builder. Applications read all data from the "Object Data Layer". An analyst opens a Workshop app that shows an Object Table (a filterable list of Track objects), an Object View (detail panel), and a Map widget (geospatial view). Clicking on a vehicle shows all its linked objects — signals, persons, incidents.

**2. Quiver (analytical)**: Point-and-click analytics for "object and time series data from the Ontology." Supports time series anomaly detection, forecasting, movement track visualisation, map views, and geospatial joins. Analysts can write back analysis results to the ontology ("writeback capabilities").

**3. OSDK (programmatic)**: TypeScript/Python/Java SDK for building custom applications. Query pattern from the open-source SDK:

```typescript
// Filtering objects by property
const client = createClient("https://stack.palantir.com", "ri.foundry.main...", auth);

// Fetch all active military vehicles within a geo area
const vehicles = await client(MilitaryVehicle)
  .where({
    status: { $eq: "ACTIVE" },
    position: { $withinGeoShape: operationalArea }
  })
  .fetchPage({ pageSize: 100 });

// Traverse links
const tracks = await vehicle.$link.CURRENT_TRACKS.fetchPage();
```

The `WhereClause` supports: `$eq`, `$ne`, `$gt`, `$gte`, `$lt`, `$lte`, `$isNull`, `$containsAnyTerm` (full-text), `$intersectsGeoShape`, `$withinGeoShape`, `$containsPoint`, `$doesNotIntersectGeoShape`, `$withinBoundingBox`, and boolean combinators `$and`, `$or`, `$not`.

Geospatial filters are first-class: `GeoFilter_Intersects` and `GeoFilter_Within` are exported API types, enabling sub-5km queries, corridor queries, and perimeter queries directly against ontology objects.

---

## 2. Data Pipelines — Sensor to Decision

### Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│  SENSORS / SOURCES                                       │
│  FMV cameras │ SAR satellite │ SIGINT receivers │ HUMINT │
│  OSINT feeds │ Link 16 feeds │ AIS receivers    │ ATAK   │
└────────────────────────┬────────────────────────────────┘
                         │ raw data
                         ▼
┌─────────────────────────────────────────────────────────┐
│  DATA CONNECTION LAYER (Foundry)                        │
│  Kafka consumers │ REST listeners │ JDBC syncs          │
│  Webhook listeners │ Push APIs │ CDC connectors         │
└────────────────────────┬────────────────────────────────┘
                         │ raw datasets / streams
                         ▼
┌─────────────────────────────────────────────────────────┐
│  TRANSFORM PIPELINE (Foundry)                           │
│  Python (PySpark) transforms │ SQL transforms           │
│  Container transforms (for CV models)                   │
│  Streaming compute (Flink) for real-time processing     │
│  Geospatial transforms (H3 indexing, spatial joins)     │
└────────────────────────┬────────────────────────────────┘
                         │ normalised, enriched datasets
                         ▼
┌─────────────────────────────────────────────────────────┐
│  ENTITY RESOLUTION                                      │
│  Deduplication functions                                │
│  Same-vehicle multi-sensor fusion                       │
│  Primary key consolidation                              │
└────────────────────────┬────────────────────────────────┘
                         │ resolved entities
                         ▼
┌─────────────────────────────────────────────────────────┐
│  ONTOLOGY (Foundry)                                     │
│  Object types with typed properties and links           │
│  Classification markings on individual objects          │
│  Time-series properties for sensor readings             │
│  Geotemporal series for position histories              │
└────────────────────────┬────────────────────────────────┘
                         │ semantic data layer
                         ▼
┌─────────────────────────────────────────────────────────┐
│  AIP / GOTHAM APPLICATIONS                              │
│  Workshop operational apps │ Quiver analytics           │
│  AIP Logic functions │ AIP Agents                       │
│  Gotham investigation tools                             │
└────────────────────────┬────────────────────────────────┘
                         │ decisions / actions
                         ▼
┌─────────────────────────────────────────────────────────┐
│  ACTION LAYER                                           │
│  Ontology edits │ Webhook calls to external systems     │
│  Notifications │ Fire control data products             │
│  ATAK pushes │ Mission planning updates                 │
└─────────────────────────────────────────────────────────┘
```

### Sensor Ingestion: Specific Types

**Full-Motion Video (FMV)**: Video frames processed through container-based CV models (YOLO-class architectures or custom models) that output bounding boxes, object classifications, and confidence scores. These detections write to ontology object types (e.g., `DetectedObject`, `Track`). Palantir's `mediaReference` and `MediaSet` infrastructure stores the raw video while the metadata (detections, timestamps, coordinates) lives in the ontology.

**Satellite Imagery**: TITAN is specifically designed to ingest imagery from commercial satellites (Maxar WorldView 1/2, BlackSky 14-satellite constellation were confirmed in Project Convergence testing) plus DoD overhead ISR. The imagery goes through ML pipelines (change detection, object detection) with results written to the ontology as `Target` or `Activity` objects.

**SIGINT**: Signal intercepts arrive as structured data (frequency, time, geo, signal type). Transform pipelines normalise to ontology `Signal` objects with classification markings. Entity resolution links signals to known entities (e.g., `Signal → ATTRIBUTED_TO → Person`).

**HUMINT/Intelligence Reports**: NLP pipelines process text reports. Named entity recognition extracts persons, locations, organisations, and events. These populate `Person`, `Location`, `Incident`, and `Organisation` ontology objects.

**OSINT**: Web scraping, social media, news feeds processed through NLP. Geolocation extracted from text and images.

**Link 16 / SADL**: These tactical data link messages (track messages in J-series message format) would be parsed into structured data by custom parsers and written to `Track` objects in the ontology. Palantir's broad connector ecosystem supports custom parsers via Python transforms.

**AIS / Ship Tracking**: AIS messages (NMEA format over UDP/TCP) decode to vessel identity, position, speed, course. AIS connectors are well-documented — the open-source osdk-ts examples include AIS as a use case. Each vessel becomes a `Vessel` ontology object with a `geotimeSeriesReference` for position history.

### Entity Resolution

Palantir calls this the "Multi-datasource Object (MDO)" capability. When the same physical entity (e.g., a truck) is observed by a UAV camera AND a SIGINT receiver AND an infantry report, three separate data records exist. Entity resolution functions (TypeScript or Python, running as Foundry Functions) consolidate these into a single ontology object with links to all contributing data sources.

The resolution process uses configurable fuzzy matching rules:
- **Geo-temporal proximity**: Two detections within X metres and Y seconds are likely the same entity
- **Attribute matching**: Same vehicle registration, same signal characteristics, same named person
- **Analyst confirmation**: Ambiguous merges can be staged for human review via the Action approval workflow

The resolved entity's primary key becomes canonical, and all historical detections link to it via `OBSERVED_AS` or `CONTRIBUTED_TO` links.

### Classification and Enrichment

After entity resolution, enrichment functions:
- Look up the entity against watch lists and databases
- Score threat level based on rules or ML models
- Apply STANAG classification labels using the `marking` property type
- Add temporal context: last seen, first seen, pattern-of-life baseline
- Generate predictive properties: estimated next position, predicted behaviour

---

## 3. AI/ML Components

### Computer Vision

Palantir's platform supports container-based model deployment: "Container models" are Docker containers deployed as inference services. CV models (likely YOLO-family architectures based on industry norms and the inference latency requirements for FMV processing) run as containerised transforms in the pipeline.

The `mediaReference` and `MediaSet` types in the Ontology are specifically designed for unstructured media. A `MediaSet` contains the raw imagery/video, and transforms output structured detections that write to typed ontology objects.

For satellite imagery analysis, Palantir's Project Convergence demos showed the system processing imagery from WorldView satellites in near-real-time. The processing chain is: imagery downlink → Foundry ingestion → CV model (container transform) → change detection / object detection output → ontology `Target` or `ChangeEvent` object.

### Natural Language Processing

For intelligence reports (HUMINT, OSINT), NLP pipeline:
- Foundry Python transforms using standard NLP libraries (spaCy, transformers)
- Named entity recognition → populate ontology objects
- Relationship extraction → populate ontology links
- Sentiment / threat scoring as derived properties
- Document storage in `mediaReference` with extracted metadata in ontology properties

The `vector` property type supports embedding-based retrieval: documents and ontology objects can have embedding vectors attached, enabling semantic search across all intelligence products.

### LLM Integration: The k-LLM Philosophy

Palantir uses what the documentation calls a **"k-LLM philosophy"**: the platform abstracts over multiple LLM providers so operators are not locked into one model. From the AIP Logic documentation: "any available LLM in the platform, in keeping with Palantir's k-LLM philosophy."

**Supported LLM Providers** (from Model Integration documentation listing externally-hosted model providers): OpenAI, SageMaker (which hosts custom models including government-tailored versions), Vertex AI (Google), Databricks. The platform also supports self-hosted models via Container Models, meaning Llama 3, Falcon, or US government-approved models can run entirely on-premises.

For classified deployments (IL5/IL6), LLMs run locally — no data leaves the classification boundary. Palantir's FedRAMP Moderate and DoD IL5 SRG certifications are listed explicitly on the Gotham platform page, and Apollo's air-gapped deployment capability means LLM inference runs on hardware physically present in the classified enclave.

**LLM Configuration Parameters** (from AIP Logic FAQ):
- Temperature: configurable, default = 0 (fully deterministic)
- Model selection: dropdown per Use LLM block; can switch between model sizes (e.g., "32k" context window variant)
- Token limits: reset per-block (not per-function); each block has its own token budget
- Execution timeout: 5 minutes when called from Workshop or API; no limit in Debugger mode

### Anomaly Detection and Prediction

Quiver's built-in capabilities include:
- Time series anomaly detection (statistical models)
- Forecasting and regression on time series data
- Reference profile comparison (baseline vs. current behaviour)

More sophisticated models deploy through Foundry's Modeling Objectives framework: scikit-learn, TensorFlow, or Spark ML models trained in-platform or imported from container registries. These models register against ontology object types and run as live inference services. A patrol pattern prediction model, for example, would take a `Track` object's position history and output predicted future waypoints as a derived property.

---

## 4. The LLM Interface — Technical Mechanics

### AIP Logic: How Natural Language Executes Against Military Data

AIP Logic is "a no-code development environment for building, testing, and releasing functions powered by LLMs." It is the mechanism that converts a query like "Show me all military vehicles within 5km of [location]" into a typed ontology query with structured results.

**Block-Based Execution Model**

A Logic function is a directed graph of blocks:

| Block Type | What It Does |
|---|---|
| **Use LLM** | Calls an LLM with a prompt + tools. The LLM reasons and calls tools to answer. |
| **Apply Action** | Executes a typed Action on the ontology deterministically (no LLM involved) |
| **Execute Function** | Calls a TypeScript/Python function or another Logic function |
| **Conditional** | Routes execution based on a condition |
| **Loop** | Iterates over a list, running blocks per element |
| **Create Variable** | Declares a typed variable (string, integer, object, array, etc.) |

**Tools Available to the LLM Within a Use LLM Block**

The LLM does not have direct database access. It can only interact with the ontology through these four tools:

1. **Query Objects**: "Access specified object types" with configured properties. The LLM specifies filter criteria (which the tool translates into a typed `WhereClause` query), and receives back typed objects. Supports filtering, aggregation, link traversal. The object types and properties the LLM can access are **configured by the developer, not chosen by the LLM at runtime** — this is the hallucination boundary.

2. **Apply Actions**: Execute ontology edits via pre-defined Action types. Again, the action types and their parameter schemas are configured in advance. The LLM fills in parameter values from context; it cannot invent new action types.

3. **Call Function**: Invoke a named TypeScript/Python function. Functions are pre-registered; the LLM cannot call arbitrary code.

4. **Calculator Tool**: Perform mathematical operations accurately (offloads arithmetic from the LLM to prevent calculation hallucination).

**The Natural Language → Military Action Pipeline**

For the viral demo scenario — "Show me all military vehicles within 5km of grid reference 42SXC..." — the execution flow is:

```
1. User input → AIP Logic function is invoked with the text query as input

2. Use LLM block receives the query + system prompt context
   System prompt includes: what object types exist, what properties they have,
   what the user is allowed to access (enforced by Ontology permissions)

3. LLM reasons: "I need to find Vehicle objects near a location"
   LLM calls Query Objects tool with:
     objectType: "MilitaryVehicle"
     filter: { position: { $withinGeoShape: { radius: 5000, center: [lat, lon] } } }
     properties: ["vehicleId", "classification", "lastSeen", "speed", "heading"]

4. Query Objects tool executes typed Ontology query → returns array of Vehicle objects

5. LLM receives structured query results (typed, not raw data strings)
   LLM formats a response: "3 vehicles found: [T-80 tank at grid..., ...]"

6. Logic function returns the formatted response + the underlying object references

7. The Workshop/Gotham application displays results on a map (using the geopoint properties)
   and as structured cards (using Object View widgets)
```

**Critical Security Property**: The LLM never receives data it is not authorised to see. The Query Objects tool respects the user's classification markings. If the calling user lacks a marking required to see a specific `MilitaryVehicle` object, that object is silently excluded from tool results — the LLM cannot ask for it because it does not know it exists.

**Hallucination Prevention**

Multiple defence layers:
1. **Typed tools only**: The LLM cannot query data structures that haven't been pre-defined. Hallucinated object types return empty results, not fabricated data.
2. **Temperature = 0 by default**: Fully deterministic outputs.
3. **Chain-of-thought logging**: Every LLM step is logged ("AIP Logic Metrics"). Developers can inspect the full reasoning chain for audit.
4. **Evaluations framework**: Developers configure test sets with expected outputs. The platform measures variance across multiple runs. Palantir recommends "5–10 input/output pairs as unit tests."
5. **Few-shot examples**: System prompts include examples of correct query → result mappings.
6. **Human review staging**: Ontology edits (write operations) can be set to "staged" mode — the LLM generates a proposal, which is shown in the Proposals tab with the full decision log. A human approves or rejects before execution.

**The 24-Hour Proposal Window**: Staged proposals are visible for only 24 hours and only to the user who created the automation. This is a key military-relevant safety constraint: there is no persistent queue of un-reviewed AI-generated targeting proposals.

### AIP Agent Studio: Multi-Turn Agents

AIP Agents are multi-turn assistants that combine an LLM with six tool types, retrieval-augmented generation, and stateful application variables.

**Tool Types for Agents**:
1. **Action Tool**: Execute an ontology edit. Can be configured for automatic execution OR require user confirmation (the default). The confirmation modal shows the proposed change before execution.
2. **Object Query Tool**: "Supports filtering, aggregation, inspection, and traversal of links for configured objects." This is the primary intelligence data access mechanism.
3. **Function Tool**: Invoke any Foundry function, including published AIP Logic workflows.
4. **Update Application Variable Tool**: Update a UI state variable (e.g., pan the map to a new location).
5. **Command Tool**: Trigger operations in other Palantir applications — specifically mentioned: Gaia map commands including "Draw polygon," "Render ephemeral feature," "Remove all features." This means an agent can directly manipulate the operational map display.
6. **Request Clarification Tool**: Pause execution and ask the user for more information.

**Native Tool Calling** (parallel): For the four non-UI tool types (actions, object queries, functions, variable updates), agents support parallel tool execution — multiple database queries run simultaneously rather than sequentially.

**Retrieval Context Types** (RAG for agents):
1. **Ontology Context**: Semantic search across ontology objects with vector embeddings
2. **Document Context**: Full-text or chunk-based semantic search across intelligence documents
3. **Function-backed Context**: Custom retrieval logic in TypeScript

**Application State**: Agents can maintain stateful variables between turns. This enables persistent operational context — the agent "knows" the current area of operations, the current task, and the history of the conversation.

---

## 5. Edge Deployment (Apollo + Disconnected Operations)

### Apollo Architecture

Apollo is described as a "continuous deployment engine" that supports multi-cloud, hybrid-cloud, private SaaS, air-gapped, and ruggedized environments. It runs on Kubernetes (implied by the "autoscaling compute mesh" description and the 300+ microservices architecture).

**Core Apollo Capabilities**:
- **Auto-discovery**: Inventory of all software running across a fleet of installations
- **Autonomous deployment**: Palantir claims "tens of thousands of releases per week" across their customer fleet
- **Disconnected operation**: Software updates can be pre-staged and applied when connectivity is available; operations continue during disconnected periods with locally cached data
- **Compliance-as-code**: Security and access standards are baked into the deployment pipeline, not applied after the fact

### Edge Footprint

The Foundry/AIP platform is built on 300+ microservices. For a tactical edge deployment, Palantir offers tiered configurations — the TITAN programme explicitly describes "dual configuration tiers":

- **Advanced (Tier 1)**: Connects to space assets and fuses multi-domain data; likely requires a vehicle-mounted server rack (joint light tactical vehicle or similar)
- **Basic (Tier 2)**: Operates at tactical echelon from lower units; lighter footprint

For the TITAN programme specifically, "the key component is the software" and the hardware is provided by partners (Northrop Grumman, Anduril, L3Harris, Sierra Nevada Corporation). This means the software footprint is designed to be platform-agnostic — deployable on whatever server hardware the hardware integrators bring.

The emphasis on "rapid startup and shutdown" for TITAN suggests the software boots quickly (minutes, not hours) and can be cleanly shut down without data loss — important for "shoot and scoot" operations.

### LLMs at the Edge

For disconnected/air-gapped deployments, LLMs must run locally. The Container Models capability means any Hugging Face model or custom-trained model packaged as a Docker container can be deployed via Apollo to edge nodes. The `vector` property type for embeddings means RAG pipelines also run locally — no cloud dependency.

Palantir's DoD IL5 and FedRAMP certifications mean the same platform that runs in AWS GovCloud can also run on-premises in a SCIF or on a vehicle-mounted server.

---

## 6. TITAN Ground Station — Technical Architecture

### What TITAN Is

**TITAN (Tactical Intelligence Targeting Access Node)** is the Army's programme-of-record ground station for multi-domain ISR data fusion and AI-assisted targeting. The Army awarded Palantir a contract (with Raytheon as the hardware integrator) in April 2023 after a competitive prototype programme.

TITAN's job: connect Army tactical units to space-based and high-altitude ISR sensors, fuse the data using AI, and distribute targeting solutions to long-range precision fires.

### Hardware Platform

TITAN is hosted on a ground vehicle — specifically referenced as a **Joint Light Tactical Vehicle (JLTV)** class platform. The system must accommodate soldiers moving through the vehicle "with helmets, boots, and backpacks" — a real ergonomic constraint that shapes the hardware form factor.

Hardware integrators confirmed to be involved:
- **Northrop Grumman**: Space segment connectivity (was the pre-prototype vendor)
- **L3Harris**: Communications systems
- **Sierra Nevada Corporation**: Platform integration
- **Anduril**: Contributing sensors/payload elements

The server hardware inside the vehicle is not publicly specified but would be a ruggedised rack system (likely based on VITA 48 VPX standards or commercial equivalents) running Kubernetes for the Palantir software stack.

### Software Stack

Palantir's contribution is the software that runs on the TITAN hardware. Based on their public statements and the contracts' scope:

- **Core**: Palantir Foundry + Ontology (the data fabric)
- **Sensor ingestion**: Data Connection agents subscribing to downlinked satellite imagery, UAV feeds, SIGINT streams, and ground-based sensor networks
- **AI processing**: CV models for imagery exploitation, NLP for report processing, anomaly detection for pattern-of-life analysis
- **Human interface**: Gotham application layer for analysts; AIP Logic/Agent for natural language querying
- **Distribution**: Generates targeting messages in standard DoD formats (ATAK, AFATDS-compatible data products, Link 16 message formats)
- **Delivery**: Apollo manages software updates and ensures software consistency across the fleet of TITAN vehicles

### Sensor Inputs

Confirmed sensor categories for TITAN (from Army programme documentation):

| Sensor Type | Source |
|---|---|
| **Space-based EO/IR** | Commercial (Maxar WorldView 1/2, BlackSky) + DoD NRO assets |
| **Space-based SAR** | Emerging commercial SAR constellations |
| **High-altitude ISR** | U-2, Global Hawk, multi-domain sensing systems |
| **Aerial ISR** | Manned ISR aircraft, Grey Eagle UAS, MQ-9 |
| **Ground ISR** | Terrestrial Layer System (TLS), EW sensors |
| **Space Development Agency** | National Defense Space Architecture (NDSA) LEO satellite data |

Project Convergence (Sep-Nov 2022) demonstrated TITAN ingesting real-time data from BlackSky's 14-satellite constellation and distributing targeting messages to multiple mission command applications.

### Outputs and Kill Chain

TITAN's output is "targeting data to the right shooter — such as the new Army long-range precision fires missiles." The targeting workflow:

```
Space/air/ground sensors detect activity
        ↓
TITAN ingests multi-source data (near-real-time)
        ↓
AI/ML fuses data: entity resolution, classification, geo-location
        ↓
Analyst reviews AI-generated target nomination in Gotham/AIP interface
        ↓
Analyst approves and assigns to shooter
        ↓
Targeting message distributed to: AFATDS (fire control), IBCS, ATAK
        ↓
Long-range precision fires execute
```

The Army's stated goal is to "decrease complexity" while "greatly increasing capability" — meaning the AI compression of multi-source data into a single actionable picture is the core value proposition. Specific sensor-to-targeting timelines are not publicly disclosed but the programme emphasises "operationally relevant speeds."

### JADC2 Integration

TITAN is explicitly described as "one of the foundational elements from the intelligence modernisation efforts" and "the core concept for the Pentagon's Joint All-Domain Command and Control initiative." It participates in:

- **Combined JADC2 (CJADC2)**: Army-Air Force joint framework
- **Space Development Agency's NDSA**: LEO satellite constellation access
- **Multi-Domain Task Force**: TITAN was deployed to the 1st MDTF in the Philippines for live operational testing

---

## 7. Integration with Military Systems

### ATAK (Android Tactical Assault Kit)

ATAK is the primary tactical situational awareness platform used by US special operations and increasingly conventional forces. Palantir integrates at two levels:

1. **Data output**: TITAN and Gotham can generate CoT (Cursor-on-Target) XML messages that ATAK consumes. A targeting object in the Palantir Ontology can trigger a webhook action that posts a CoT message to an ATAK server.
2. **AIP Agents**: The "Command Tool" in AIP Agent Studio can trigger operations in Palantir applications. Workshop applications can embed ATAK-format map data. The bidirectional data flow means ATAK position reports can flow into Foundry and update ontology objects.

### Fire Control (AFATDS / IBCS)

AFATDS (Advanced Field Artillery Tactical Data System) is the Army's fire control software. TITAN's stated purpose is to feed "targeting messages to a variety of mission command applications/weapons systems" — AFATDS is the primary target.

The integration likely uses standard Army data formats (STANAG 4586 for UAS data, tactical XML, or fire mission request formats) sent via webhook actions from the Palantir Ontology when an analyst approves a target nomination.

IBCS (Integrated Battle Command System) for air and missile defence would receive similar data feeds for air track correlation and engagement coordination.

### Link 16 / SADL

Link 16 track messages (J3.0, J3.2, J3.5) carry position, identity, and status for air, surface, and land tracks. A Link 16 gateway (hardware) decodes these messages and exposes them as a data stream. Palantir would consume this via a Data Connection connector (custom parser in a Foundry agent or a streaming sync from a UDP/TCP endpoint) and write decoded track data to ontology `Track` objects.

The bidirectional capability (publishing back to Link 16) would require a hardware interface that Palantir's software would drive via Action webhooks.

### MetaConstellation / Satellite Tasking

Palantir built "MetaConstellation" — a satellite tasking management system that wraps access to multiple commercial satellite operators. In the TITAN context, this means the ground station can not only receive satellite data passively but also task satellites: an analyst identifies a coverage gap, requests a revisit of a specific area, and the tasking request goes to the appropriate satellite operator via MetaConstellation. The tasked imagery comes back into the TITAN pipeline automatically.

### Drone Control

Palantir's software does not directly fly drones but serves as the C2 software layer that ingests drone sensor feeds and coordinates mission assignments. Integration patterns:
- **FMV from UAVs**: Video feeds ingested into MediaSets, processed by CV models, detections written to ontology
- **Drone tasking**: Action types that webhook to drone ground control software (e.g., a STANAG 4586-compatible GCS)
- **ATAK/CoT**: UAV position reports via CoT format flow into the ontology

---

## 8. Maven Smart System (US Air Force / SOCOM)

Maven Smart System (MSS) is the US government's AI-enabled computer vision system originally started by Project Maven (DoD). Palantir won the MSS contract from the Defense Innovation Unit (DIU).

While specific technical details are less public than TITAN, the architecture follows the same Palantir pattern:

- **Input**: FMV from ISR platforms (Predator, Reaper, Global Hawk feeds)
- **CV pipeline**: Object detection and classification on video frames (detecting vehicles, people, weapons, activities)
- **Ontology**: Detections write to typed object types with confidence scores, timestamps, and geolocations
- **Analyst interface**: Gotham application for reviewing detections, confirming identifications, and generating intelligence products
- **Distribution**: Intelligence products distributed to JWICS consumers

The computer vision models are almost certainly YOLO-family or transformer-based architectures (e.g., ViT-based detection models), running as containerised transforms in the Foundry pipeline. Specific architectures are not publicly disclosed.

---

## 9. Security Architecture for Military Deployments

### Markings (Mandatory Access Control)

Palantir's Markings system implements Bell-LaPadula-style mandatory access control:

- **Binary, all-or-nothing**: A user either has a Marking or they don't. There is no partial access.
- **Conjunctive logic (AND)**: A resource with markings A AND B requires the user to hold both.
- **Inheritance propagation**: Markings travel downstream through data lineage — a classified dataset propagates its markings to all derived datasets automatically.
- **Centralised administration**: Only users with "Expand Access" permission on the Marking itself can remove it from a resource.

### Classification-Based Access Controls (CBAC)

CBAC is specifically described as "mandatory controls used to protect sensitive government information" — it is not enabled by default and "requires Palantir involvement to configure."

CBAC adds hierarchical classification levels (UNCLASSIFIED, SECRET, TOP SECRET) and caveat handling (NOFORN, REL TO...) as a separate dimension from binary Markings. Key properties:
- **Hierarchical access**: Users with higher clearance can see lower-classified data
- **Disjunctive logic for caveats**: "REL TO USA, GBR" uses OR logic (users from either country satisfy the requirement)
- **Project maximum classification**: Resources cannot be moved to a project at a lower classification level than the resource's classification

### Organisations (Silos)

Organisations create "strict silos between groups of users and resources." In a military context, this maps to compartmentalisation — an analyst in one intelligence programme cannot see data in another programme even if they hold the same classification level.

### Zero-Trust Infrastructure

The Foundry platform runs on "zero-trust security infrastructure with aggressive node cycling to guard against advanced persistent threats." This means:
- No implicit trust between microservices
- All inter-service communication authenticated
- Regular node rotation to prevent persistence
- Certificate-based mutual TLS throughout

---

## 10. Key Technical Gaps and Unknowns

The following were not findable in public sources:

1. **Specific CV model architectures**: Whether Palantir uses YOLO-v8, RT-DETR, custom architectures, or third-party CV APIs for FMV exploitation is not publicly disclosed.

2. **Specific LLM models in classified deployments**: The commercial demos use OpenAI GPT-4 variants. For classified deployments, the models are not named. Likely candidates: Llama 3 (self-hosted), government-specific fine-tuned models, or commercially contracted models running in government-controlled infrastructure.

3. **Entity resolution algorithm specifics**: The specific fuzzy matching thresholds, similarity scores, and ML models used for multi-source entity fusion are proprietary.

4. **TITAN processing latency**: The sensor-to-targeting timeline. The Army's aspiration is "operationally relevant speed" but specific numbers (e.g., time from satellite tasking request to targeting quality coordinates) are not public.

5. **Kill chain automation depth**: It is publicly stated that the AI generates targeting *nominations* that humans review. Whether the system can, in principle, be configured for fully automated engagement (without human review) in specific rule-sets-of-engagement scenarios is not publicly disclosed.

6. **TITAN hardware specifics**: The server hardware inside the JLTV, CPU/GPU specifications, RAM, storage, power draw.

7. **Ontology schema for Gotham military deployments**: While the property type system is open-source and the general ontology architecture is documented, the specific object types, properties, and links that Palantir ships in their Gotham military templates are proprietary.

---

## Summary: The Architectural Answer to Each Technical Question

| Question | Answer |
|---|---|
| Is the Ontology a knowledge graph? | Yes — a typed property graph (not RDF/OWL) with mandatory access control metadata and time-series extensions |
| What graph structure? | Property graph with typed nodes (object types), typed edges (link types), typed properties (22 wire property types including geopoint, vector, sensorTimeseries) |
| How do sensors feed the ontology? | Kafka/Kinesis → Data Connection → Foundry Streams → Flink processing → Python/Spark transforms → Action writeback to ontology objects |
| How do analysts query? | Workshop (no-code apps), Quiver (analytics), OSDK (programmatic with WhereClause + geospatial filters) |
| What LLMs are used? | k-LLM model (any provider): GPT-4 for commercial, self-hosted Llama/custom for classified |
| How does NL → military action work? | AIP Logic blocks: LLM uses Query Objects / Apply Action / Call Function tools, all pre-defined, with ontology security enforced at tool layer |
| Does LLM control systems directly? | No. LLM proposes actions via typed Action parameters. Human approval required for writes (configurable). Execution via pre-defined Action types only. |
| How is hallucination prevented? | Temperature=0 default, typed tools only, pre-configured object types the LLM can access, CoT logging, evaluations framework, human-review staging |
| Edge deployment? | Apollo deploys 300+ microservice Kubernetes stack to air-gapped environments. Container models mean LLMs run locally. Tiered hardware (JLTV for advanced, lighter footprint for basic) |
| TITAN hardware? | JLTV-mounted server rack (vendor unspecified), software from Palantir, hardware integration by Northrop/L3Harris/Sierra Nevada |
| TITAN sensor inputs? | Commercial EO/SAR (Maxar, BlackSky), DoD overhead ISR, high-altitude (U-2, Global Hawk), aerial UAV (Grey Eagle, MQ-9), ground sensors (TLS), LEO satellites (SDA NDSA) |
| TITAN outputs? | Targeting messages to AFATDS, IBCS, ATAK; intelligence products to mission command applications |
| ATAK integration? | CoT XML webhook outputs from Palantir Actions; bidirectional via Data Connection |
| Fire control integration? | AFATDS: targeting message webhooks from approved ontology actions; IBCS: air track data feeds |
| Link 16? | Custom parser consuming Link 16 gateway output → Foundry stream → ontology Track objects |
| Drone control? | Ingest (FMV + CoT position reports) into ontology; task via Action webhooks to GCS; no direct flight control |

---

*Sources: Palantir official documentation at palantir.com/docs (March 2026 snapshot), open-source osdk-ts GitHub repository (Apache 2.0 licensed), Breaking Defense programme reporting (2020–2024), US Army Project Convergence exercise reporting (2022), Army Acquisition portfolio documentation, TITAN programme competition reporting.*
