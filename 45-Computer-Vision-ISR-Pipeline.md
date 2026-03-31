# Computer Vision Pipeline for Drone ISR
*Research document for mpe-c2 team. Author: INTEROP agent. Date: 2026-03-31.*
*Covers: model selection (YOLOv8/v9 vs RT-DETR), training datasets, edge hardware, video ingest, integration with TrackManager.*
*Status: READ-ONLY reference for CORE to implement against. NO code in this document.*

---

## 1. The Gap This Fills

From the 2026-03-28 session notes:
> "Computer vision — YOLOv8 on drone video → Observation → TrackManager. The biggest capability gap vs Maven."

Currently MPE ingests ADS-B, AIS, and CoT. All three are network protocols carrying pre-processed position data from external sensors. The engine never touches raw video. Adding a CV pipeline means:

1. A drone's camera outputs a live H.264/H.265 video stream (RTSP or RTP)
2. An inference engine runs object detection on each frame
3. Detections (bounding boxes + class labels + confidence scores) are georegistered to lat/lon/alt coordinates
4. Each georeferenced detection becomes an `Observation` fed into `TrackManager`
5. `TrackManager` fuses these visual observations with AIS/ADS-B/CoT tracks from the same entity

This is the feature that makes MPE a genuine ISR platform rather than a track aggregator.

---

## 2. Model Selection: YOLOv8/v9 vs RT-DETR

### The Candidates

Three serious candidates exist for aerial object detection in 2025/2026:

| Model Family | Architecture | Maintained By | Primary Strength |
|---|---|---|---|
| YOLOv8 | CNN (CSPNet backbone) | Ultralytics | Speed, edge compatibility, community |
| YOLOv9 | CNN + PGI/GELAN | WongKinYiu | Accuracy over v8 at same speed |
| RT-DETR (v1/v2) | Transformer (ResNet backbone) | Baidu/Ultralytics | Accuracy on complex scenes, context |
| RF-DETR | Transformer (DINOv2) | Roboflow | SOTA accuracy 2025, larger model |

### Benchmark Data (COCO val2017)

| Model | mAP50-95 | Latency (T4 TRT FP16) | Params |
|---|---|---|---|
| YOLOv8s | 44.9% | 2.1ms | 11M |
| YOLOv8m | 50.2% | 5.1ms | 26M |
| YOLOv8x | 53.9% | 12.6ms | 68M |
| YOLOv9c | 53.0% | ~5ms | 25M |
| YOLOv9e | 55.6% | ~12ms | 58M |
| RT-DETR-R50 | 53.1% | 9.3ms (108 FPS) | 42M |
| RT-DETR-R101 | 54.3% | 13.5ms (74 FPS) | 76M |

### Aerial / Small Object Performance (VisDrone)

Standard COCO benchmarks are not aerial — the critical metric is VisDrone performance, where objects are tiny, dense, and seen from above.

| Approach | VisDrone mAP50 | Notes |
|---|---|---|
| Stock YOLOv8n | ~26% | Baseline; poor on tiny objects |
| Enhanced YOLOv8 (multi-scale) | 37.6% | Academic paper (Springer 2024) |
| CPDD-YOLOv8 | 41% | +6.9% over stock, +13% small obj |
| SL-YOLO | 46.9% | Lightweight, 132 FPS, 9.6M params |
| Drone-DETR (RT-DETR variant) | +4–6.5% vs YOLO-DCTI | Beats YOLO variants on aerial |

**Key insight:** Stock YOLOv8 underperforms on aerial imagery because the standard neck/head architecture is sized for objects occupying >1% of the image. Real-world aerial targets (vehicles, people at 200m altitude) can be 10–40px — less than 0.01% of a 1080p frame. All serious aerial deployments fine-tune with:
- Extra small-object detection head (P2 feature pyramid level added)
- SAHI (Slicing Aided Hyper Inference) — tiles the image into overlapping patches, runs inference on each, merges results
- Training on aerial-specific datasets (VisDrone, DOTA, xView)

### RT-DETR vs YOLOv8: The Trade-off

**Choose YOLOv8 (fine-tuned) when:**
- Deploying on Jetson Orin NX or edge hardware with TensorRT
- Latency budget is tight (sub-5ms per frame required)
- Model needs to run INT8 quantization on hardware without abundant memory
- Primary targets are vehicles and humans at medium altitude (100–300m AGL)
- Rapid iteration / community support matters (Ultralytics ecosystem)

**Choose RT-DETR when:**
- Server-side inference with GPU headroom (T4 or better)
- Targets are in dense, occluded, or complex backgrounds
- Global context matters (e.g., distinguishing boats in crowded harbours)
- Fine-grained classification beyond YOLO's typical 80 classes needed

**Recommendation for MPE (near-term):**
Use **YOLOv8m** fine-tuned on VisDrone + xView as the primary model. Reasons:
1. Best-supported model family for Jetson TensorRT deployment
2. 5ms inference at FP16 on Jetson Orin NX = 200 FPS theoretical → comfortable for 30 FPS drone video
3. SAHI tiling solves the small-object problem without model architecture changes
4. Ultralytics export pipeline handles TensorRT, ONNX, TFLite — reduces deployment friction
5. VisDrone fine-tuning examples are widely available

**RT-DETR is the upgrade path** when the platform targets server-side batch reprocessing of recorded ISR footage, where latency is less critical than accuracy.

---

## 3. Training Datasets

Three primary datasets, each with different properties. A real aerial CV pipeline will train on a combination of all three.

### VisDrone

**What it is:** Drone-captured video and images from real UAVs. The most relevant dataset for MPE's use case.

**Key specs:**
- 288 video clips (261,908 frames) + 10,209 static images
- Captured across 14 cities in China at varying altitudes and viewpoints
- 10 object categories: pedestrian, people, bicycle, car, van, truck, tricycle, awning-tricycle, bus, motor
- 6,471 training / 548 validation / 1,580 test images
- Annotations: horizontal bounding boxes

**Relevance to MPE:** Direct match for drone-mounted camera ISR at 50–300m AGL. Person and vehicle detection categories cover the majority of ground surveillance targets.

**Download:** GitHub — `VisDrone/VisDrone-Dataset`. Academic use; free.

**Ultralytics native support:** `data=VisDrone` in YOLOv8 training config; automatic download available.

**Limitation:** Primarily urban Chinese scenes. Performance on African, Middle Eastern, or maritime environments may degrade — domain adaptation (fine-tuning on target-environment images) is recommended before deployment.

### xView

**What it is:** Overhead satellite/aerial imagery from WorldView-3 satellites at 0.3m ground sample distance. Much higher resolution than VisDrone but from a vertical nadir viewpoint (straight down).

**Key specs:**
- 1,400 km² of imagery
- 1+ million annotated objects across 60 classes
- Image resolution: 0.3m GSD (each pixel = 30cm on the ground)
- 60 categories in parent-child hierarchy — includes: building, vehicle (cars, trucks, trailers), boat, plane, helicopter, cargo container, construction site, helipad, etc.
- Download: `xviewdataset.org` (requires registration; DIUx/NGA-funded dataset)

**Relevance to MPE:** Excellent for vehicle and vessel detection, port/harbour surveillance. The 60-class taxonomy is richer than VisDrone and covers maritime targets (boats, ships) that VisDrone lacks.

**Limitation:** Satellite imagery; objects are smaller and more nadir-oriented than drone footage. Transfer learning from xView to oblique drone imagery requires careful augmentation (rotation, perspective warp).

### DOTA-v2

**What it is:** Large-scale aerial imagery dataset specifically designed for Oriented Bounding Box (OBB) detection — bounding boxes that rotate to fit the object's actual orientation.

**Key specs:**
- 11,268 images, 1,793,658 instances, 18 categories
- Image sizes: 800×800 to 20,000×20,000 pixels
- 18 categories: plane, ship, storage tank, baseball diamond, tennis court, basketball court, ground track field, harbour, bridge, large vehicle, small vehicle, helicopter, roundabout, soccer ball field, swimming pool, container crane, airport, helipad
- Annotations: oriented bounding boxes (OBB) — 4 corner points + angle
- Subsets: train (1,830), val (593), test-dev (2,792), test-challenge (6,053)

**Relevance to MPE:**
- Ship and harbour detection is directly relevant to maritime surveillance missions
- Plane and helicopter categories complement ADS-B track correlation
- OBB annotations are important for vehicles/aircraft where orientation matters
- Large and small vehicle categories cover ground surveillance

**Ultralytics native support:** `data=DOTAv2` with OBB mode (YOLOv8-OBB variant).

**Limitation:** Large image sizes require tiling during training; computationally expensive. The 20,000×20,000 images need to be patched to 1,024×1,024 or similar during data preparation.

### Recommended Training Strategy for MPE

**Phase 1 — Pretrained baseline:** Start with YOLOv8m pretrained on COCO. This gives solid general detection capability.

**Phase 2 — Aerial fine-tuning:** Fine-tune on VisDrone (person/vehicle focus) + DOTA-v2 ships (maritime focus). 80 epochs, freeze backbone for first 20 epochs, unfreeze for remaining 60.

**Phase 3 — Domain adaptation:** Collect 500–1,000 images from the actual deployment region and environment (or use synthetic data via simulation). Fine-tune again. This closes the VisDrone-to-Africa gap.

**Phase 4 — SAHI inference:** Wrap the trained model in SAHI for deployment. SAHI tiles 1080p frames into 320×320 or 416×416 patches with 20% overlap, runs inference on each patch, merges via NMS. This recovers most of the small-object performance loss without model changes.

---

## 4. Edge Hardware Comparison

### The Candidates

Two viable edge platforms for drone-mounted inference:

| Platform | TOPS | Power | Weight | Price | Form Factor |
|---|---|---|---|---|---|
| NVIDIA Jetson Orin NX 16GB | 157 TOPS | 10–25W | ~45g module | ~$599 module | 69.6×45mm module |
| NVIDIA Jetson Orin NX 8GB | 100 TOPS | 10–20W | ~45g module | ~$399 module | 69.6×45mm module |
| Raspberry Pi 5 + Coral USB TPU | 4 TOPS (TPU) + CPU | 8.3W total | ~80g system | ~$90 + $60 = ~$150 | 85×56mm RPi + dongle |

### Jetson Orin NX: Detailed Assessment

**Strengths:**
- 157 TOPS (NX 16GB) — enough for real-time YOLOv8m at INT8 with TensorRT
- CUDA GPU + Deep Learning Accelerators (DLAs) + NVENC/NVDEC for hardware video decode
- Full PyTorch, TensorRT, ONNX Runtime support — no model conversion limitations
- NVMM (NVIDIA Memory Map) zero-copy pipeline: camera → ISP → GPU, no CPU copy overhead
- GStreamer hardware-accelerated H.264 decode: `nvv4l2decoder` element
- JetPack SDK: full toolchain for model optimization and deployment
- Temperature stability: 42–45°C under load with active cooling

**Specific benchmark (from peer-reviewed research, IEEE 2025):**
- YOLOv8 inference: ~41.8 FPS on Jetson Orin NX vs ~21.5 FPS on RPi5+Coral
- With INT8 TensorRT: up to 313 FPS for YOLOv8n; 60 FPS for YOLOv8m (simablt.ai benchmark)

**Weaknesses:**
- $400–600 for module alone; carrier board adds $150–500 depending on ruggedization
- Requires active cooling (fin + fan) — adds weight and acoustic signature
- Power: 25W max for NX at full load — significant on a battery-powered drone
- Export-controlled in some configurations (ECCN 4A994 — check before shipping to some destinations)

**Drone-optimised carrier boards:**
- **Neousys FLYC-300**: Purpose-built UAV/UGV mission computer. Orin NX inside, ruggedised, -40°C to +70°C, M.2 5G/4G slot, CAN bus, UART. Weight: ~380g. This is the professional choice.
- **Forecr DSBOARD-ORNXS**: Compact carrier, 128×80mm, good I/O
- **Generic dev kit**: NVIDIA Jetson Orin NX Developer Kit (~$849) — not for airborne use (too large/heavy)

### Raspberry Pi 5 + Coral USB TPU: Detailed Assessment

**Strengths:**
- Very low cost (~$150 total)
- 4 TOPS (Edge TPU) sufficient for MobileNet-class models at 400 FPS
- Small form factor
- Runs standard Linux; familiar Python ecosystem

**Weaknesses:**
- Coral TPU only runs **fully quantized TFLite INT8 models**. YOLOv8 requires conversion to TFLite Edge TPU format — many layers fall back to CPU if they are not supported by the Edge TPU compiler, nullifying the acceleration benefit. Observed real-world: only some layers run on TPU; CPU handles unsupported ops.
- Actual YOLOv8 performance: 18–75 FPS depending on model size and what fraction runs on TPU vs CPU
- RPi5 runs at 80°C without active cooling — thermal throttling likely under sustained load
- No NVDEC — H.264 decoding is CPU-only (or via V4L2 which is limited)
- Framework lock-in: Coral is TFLite-only; switching models requires full re-quantization

**The key issue:** Coral TPU is designed for MobileNet-class models (3–5M params, INT8). YOLOv8n (3M params) can work. YOLOv8s (11M) starts to see CPU fallback. YOLOv8m (26M) is impractical.

### Recommendation

| Scenario | Hardware | Justification |
|---|---|---|
| Primary drone ISR payload | Jetson Orin NX 16GB + FLYC-300 | Best inference performance, hardware video decode, industry-standard for UAV AI |
| Budget/prototype drone | RPi5 + Coral TPU | Adequate for YOLOv8n at 20–30 FPS; good for proof of concept |
| Ground station (server) | RTX 4060/4070 laptop GPU | Full model, no compromise; connects to drone via RTSP over RF link |
| Development and training | Cloud (A100/H100) | Train once, deploy to edge |

**Pragmatic path for MPE given current budget constraints:**
Mohammed's budget is limited. The right progression:
1. **Now**: Develop and validate the CV pipeline on a laptop GPU using pre-recorded drone footage
2. **Summer 2026**: Buy Jetson Orin NX developer kit (~$849) for hardware validation
3. **First demo**: Use Jetson Orin NX in a drone payload enclosure

---

## 5. Video Ingest Architecture

### RTSP as the Primary Protocol

All professional drone cameras output RTSP (Real Time Streaming Protocol). Typical stream parameters:
- Codec: H.264 (most common) or H.265 (newer drones, better compression)
- Resolution: 1080p (1920×1080) at 30 FPS — standard for ISR
- Bitrate: 4–20 Mbps depending on scene complexity
- Latency: 50–200ms from capture to stream start (glass-to-glass)

RTSP URL format: `rtsp://drone_ip:port/live/stream` (varies by drone manufacturer)

DJI drones: Use DJI Mobile SDK or DJI PSDK (Payload SDK) to expose video. On DJI Enterprise drones (Matrice series), RTSP is exposed on the drone's WiFi/LTE interface.

ArduPilot companion computer: If the drone runs ArduPilot with a companion computer (Raspberry Pi, Jetson), the companion computer runs a GStreamer sender that exposes RTSP.

### Two Ingest Approaches

#### Approach A: GStreamer Native (Recommended for Jetson)

GStreamer is a pipeline-based multimedia framework. On Jetson, it is the correct choice because:
- `nvv4l2decoder` uses Jetson's hardware NVDEC for H.264 decode — no CPU involvement in decode
- `NVMM` buffers keep decoded frames in GPU memory — no CPU-GPU copy before inference
- Eliminates the 200–500ms buffering latency of OpenCV's VideoCapture

**Jetson RTSP → inference pipeline (conceptual, not code):**
```
rtspsrc location=rtsp://drone_ip:port
  → rtph264depay
  → h264parse
  → nvv4l2decoder         ← hardware decode, outputs NVMM buffer
  → nvvidconv              ← convert to BGR/RGB for inference
  → appsink               ← Python app receives frames via callback
```

Latency achievable: **10–30ms** end-to-end (network latency excluded).

**Critical setting:** `max-latency=0` on `rtspsrc` and setting the pipeline to live mode eliminates the automatic GStreamer jitter buffer that adds 200ms+ of artificial delay.

#### Approach B: PyAV (Recommended for Non-Jetson / Development)

PyAV is a Python binding for FFmpeg/libav. It can connect to RTSP streams and extract frames as NumPy arrays.

**Why PyAV over OpenCV VideoCapture for RTSP:**
- OpenCV buffers multiple frames — by the time you read a frame it may be 300–500ms old
- PyAV's `container.decode(video=0)` reads the actual latest keyframe on demand
- Latency-critical flags: `nobuffer` + `low_delay` codec context flags reduce buffer to ~1–2 frames

**Documented latency issue with PyAV and drone streams:** 7–10 second lag has been reported when drone streams have variable bitrate or bad network. Solution: set `NOBUFFER` flag on the av container and skip frames if the queue is building up.

**Best practice:** Run PyAV stream reading in a dedicated thread; use `queue.Queue(maxsize=1)` to hold only the latest frame. The inference thread pulls from the queue — if a frame is already in the queue when a new one arrives, discard the old one. This trades completeness for latency.

### Frame Rate Strategy

The drone streams at 30 FPS. YOLOv8m on Jetson Orin NX runs at ~60 FPS with TensorRT. This means the system can process every frame at 30 FPS with headroom.

However, running inference on every frame at full resolution is wasteful if targets don't move much between frames. Recommended strategy:
- Run full YOLO inference at **5–10 FPS** (every 3rd–6th frame)
- Run a lightweight tracker (ByteTrack, built into Ultralytics) to maintain detections between YOLO frames at 30 FPS
- Feed confirmed tracks (not every detection) into TrackManager

This reduces compute load by 3–6x while maintaining 30 FPS apparent track update rate.

---

## 6. Georegistration: Bounding Box → Lat/Lon

This is the critical step that converts a detection (pixel coordinates in a frame) into a geographic position that `TrackManager` can use.

### The Math

The drone knows its own position (GPS: lat, lon, alt) and its camera's orientation (gimbal: pitch, roll, yaw). Given a detection's pixel coordinates (cx, cy) in a frame of size (W, H), the target's ground position can be estimated by:

1. **Pixel → camera ray**: Convert (cx, cy) to a unit vector in camera frame using the camera's focal length and principal point (intrinsic calibration)
2. **Camera ray → world ray**: Apply the camera-to-world rotation (from drone attitude + gimbal angles)
3. **Ray-ground intersection**: Trace the world ray down to the ground plane (using drone altitude and terrain altitude if known)
4. **Ground point → lat/lon**: Convert the intersection point offset from the drone's GPS position into lat/lon using a flat-Earth or WGS-84 approximation

**Required inputs per detection:**
- Drone GPS: lat, lon, alt MSL (from MAVLink GLOBAL_POSITION_INT message)
- Drone attitude: roll, pitch, yaw (from MAVLink ATTITUDE message)
- Camera intrinsics: focal length, sensor size, image dimensions (per-camera calibration, done once)
- Gimbal angles: roll, pitch, yaw relative to drone body (from MAVLink GIMBAL_DEVICE_ATTITUDE_STATUS)

**Accuracy:** At 100m AGL with a 1080p camera and 90° FOV, pixel accuracy of ±10px corresponds to ~2–3m ground position accuracy. Sufficient for track-level association.

**Reference implementation:** `roboflow/dji-aerial-georeferencing` on GitHub — open-source Python implementation of the full pipeline.

### The Observation Object

Once georegistered, each detection becomes an `Observation` with:
- `source = TrackSource.CAMERA` (new enum value to add to `c2_models.py`)
- `uid` = `CAMERA-{frame_id}-{detection_id}` (temporary; TrackManager will correlate)
- `lat, lon, alt` from georegistration
- `domain = Domain.AIR` for UAVs/aircraft, `Domain.GROUND` for vehicles, `Domain.SURFACE` for boats
- `affiliation = Affiliation.UNKNOWN` by default (Classifier will update)
- Custom detail: `confidence` (YOLO score), `class_label` (e.g., "car", "person", "helicopter"), `bounding_box` (pixel coords), `frame_id`

This Observation flows into `TrackManager.update()` exactly like an AIS or ADS-B observation. `TrackManager` will attempt to correlate it with existing tracks via spatial matching (haversine within 50m).

---

## 7. Integration Architecture: CV Pipeline → TrackManager

```
DRONE CAMERA
    │ H.264 RTSP
    ▼
VIDEO INGEST
  GStreamer pipeline (Jetson) or PyAV (dev/server)
  Frame queue (maxsize=1, drop old frames)
    │ numpy frame (BGR, 1080p, 30fps)
    ▼
PRE-PROCESSOR
  SAHI tiler: 1920×1080 → 12× 416×416 patches (20% overlap)
  OR: Direct resize to 640×640 if drone is low-altitude (targets large enough)
    │ batched tiles
    ▼
INFERENCE ENGINE
  YOLOv8m TensorRT INT8 (Jetson) / YOLOv8m ONNX (server)
  Output: list of (class_id, confidence, x1, y1, x2, y2) per tile
    │ raw detections
    ▼
POST-PROCESSOR
  SAHI NMS merge (combine detections across tiles)
  Confidence threshold: 0.4 (tune per deployment)
  ByteTrack: assign track_id to each detection across frames
    │ confirmed tracks with stable IDs
    ▼
GEOREGISTRATION
  Per-detection: pixel (cx,cy) → world ray → ground intersection → (lat, lon, alt)
  Requires: drone GPS + attitude + gimbal state from MAVLink (or companion computer)
    │ georeferenced detections
    ▼
OBSERVATION FACTORY
  Each georeferenced detection → Observation(source=CAMERA, lat, lon, ...)
    │ Observation objects
    ▼
TrackManager.update()  ← existing code, no changes needed
    │
    ▼
Classifier → AlertEngine → CoT output → TAK Server → ATAK
```

### New Modules CORE Must Build

| Module | Purpose | Priority |
|---|---|---|
| `video_receiver.py` | GStreamer/PyAV RTSP ingest; frame queue management | HIGH |
| `inference_engine.py` | YOLOv8 TensorRT/ONNX wrapper; SAHI integration | HIGH |
| `georegistration.py` | Pixel→lat/lon conversion; requires camera intrinsics + MAVLink state | HIGH |
| `camera_tracker.py` | ByteTrack wrapper; maintains detection-to-track association across frames | MEDIUM |
| `vision_cot_bridge.py` | Visual track → CoT XML (similar to ais_cot_bridge.py) | MEDIUM |

`TrackManager` does not need changes. The camera pipeline is just another data source that produces `Observation` objects.

### New Enum Value in `c2_models.py`

`TrackSource.CAMERA` must be added to the existing `TrackSource` enum. The stale threshold for camera tracks should be short (5–10 seconds) since visual tracks are only valid while the drone is overhead — much shorter than AIS (5 minutes) or ADS-B (2 minutes).

---

## 8. Model Deployment Workflow

### Training (Cloud or workstation GPU)

1. Start with YOLOv8m COCO pretrained weights
2. Fine-tune on VisDrone (80 epochs, batch 16, img 640, AdamW optimizer)
3. Further fine-tune on DOTA-v2 ships subset (for maritime)
4. Export to ONNX: `yolo export model=best.pt format=onnx`
5. Evaluate on VisDrone val set; target mAP50 > 35% on stock val

### Deployment (Jetson Orin NX)

1. Copy ONNX model to Jetson
2. Convert to TensorRT engine: `yolo export model=best.onnx format=engine device=0 int8=True`
3. Provide 500+ calibration images for INT8 calibration (ideally from target environment)
4. Test engine: `yolo predict model=best.engine source=rtsp://... stream=True`
5. Benchmark: measure actual FPS and confirm > 30 FPS on target resolution

### Development (laptop, no Jetson)

1. Use ONNX runtime with CPU/CUDA: `yolo predict model=best.onnx source=video.mp4`
2. Process pre-recorded drone footage from YouTube or open datasets
3. Validate georegistration math with synthetic test cases (known positions)

---

## 9. Key Open Questions for CORE

1. **Camera calibration data**: Does the drone have a known camera model (DJI Zenmuse, Sony, GoPro)? Intrinsic parameters (focal length, principal point, distortion) are needed for georegistration. Many drone cameras have published calibration data.

2. **MAVLink telemetry sync**: The georegistration requires GPS + attitude + gimbal at the exact timestamp of each frame. The video stream and MAVLink telemetry stream are separate — they need to be timestamped and aligned. This is a non-trivial engineering problem.

3. **Companion computer vs ground station inference**: Should the Jetson run on the drone (onboard inference, detections sent to MPE engine via CoT/network) or on the ground station (full video stream sent to ground, inference done there)? Onboard reduces bandwidth (detections are tiny compared to video); ground-side simplifies the drone payload and makes inference upgradeable without touching the drone.

4. **RF link bandwidth**: A 1080p H.264 stream at 4 Mbps requires a reliable 4+ Mbps RF link. At ISR ranges (1–5 km), a standard 2.4/5.8 GHz video link can sustain this; at 10+ km, you need a directional link (e.g., the ground mesh described in 12-Naval-Maritime-Applications.md) or onboard inference.

---

## 10. Key References

- YOLOv8/RT-DETR comparison: [Ultralytics compare docs](https://docs.ultralytics.com/compare/rtdetr-vs-yolov8/)
- RT-DETR paper (CVPR 2024): [openaccess.thecvf.com](https://openaccess.thecvf.com/content/CVPR2024/papers/Zhao_DETRs_Beat_YOLOs_on_Real-time_Object_Detection_CVPR_2024_paper.pdf)
- Drone-DETR (RT-DETR for aerial): [PMC article](https://pmc.ncbi.nlm.nih.gov/articles/PMC11397902/)
- SL-YOLO (VisDrone 46.9% mAP): [arxiv.org/abs/2411.11477](https://arxiv.org/html/2411.11477v3)
- CPDD-YOLOv8 (VisDrone 41%): [Scientific Reports](https://www.nature.com/articles/s41598-024-84938-4)
- VisDrone dataset: [github.com/VisDrone/VisDrone-Dataset](https://github.com/VisDrone/VisDrone-Dataset)
- VisDrone (Ultralytics docs): [docs.ultralytics.com/datasets/detect/visdrone](https://docs.ultralytics.com/datasets/detect/visdrone/)
- xView dataset: [xviewdataset.org](https://xviewdataset.org/)
- xView (Ultralytics docs): [docs.ultralytics.com/datasets/detect/xview](https://docs.ultralytics.com/datasets/detect/xview/)
- DOTA-v2 official: [captain-whu.github.io/DOTA](https://captain-whu.github.io/DOTA/dataset.html)
- DOTA-v2 (Ultralytics OBB): [docs.ultralytics.com/datasets/obb/dota-v2](https://docs.ultralytics.com/datasets/obb/dota-v2/)
- Jetson Orin NX benchmarks (IEEE 2025): [ieeexplore.ieee.org/document/10971592](https://ieeexplore.ieee.org/document/10971592/)
- INT8 quantization 60 FPS benchmark: [simalabs.ai](https://www.simalabs.ai/resources/60-fps-yolov8-jetson-orin-nx-int8-quantization-simabit)
- YOLOv8 TensorRT Jetson deploy: [Seeed Studio Wiki](https://wiki.seeedstudio.com/YOLOv8-TRT-Jetson/)
- Neousys FLYC-300 (UAV mission computer): [neousys-tech.com](https://www.neousys-tech.com/en/product/product-lines/edge-ai-gpu-computing/nvidia-jetson/flyc-300)
- Jetson vs Coral comparison: [thinkrobotics.com](https://thinkrobotics.com/blogs/learn/edge-ai-accelerators-jetson-vs-coral-tpu-a-detailed-comparison-for-developers)
- GStreamer Jetson real-time video: [roboticsknowledgebase.com](https://roboticsknowledgebase.com/wiki/networking/gstreamer-jetson-realtime-video/)
- PyAV RTSP low latency: [PyAV discussions](https://github.com/PyAV-Org/PyAV/discussions/957)
- YOLO + PyAV RTSP (GitHub): [Atomik31/POC-Real-Time-RTSP-Object-Detection](https://github.com/Atomik31/POC-Real-Time-RTSP-Object-Detection)
- Aerial georeferencing: [roboflow/dji-aerial-georeferencing](https://github.com/roboflow/dji-aerial-georeferencing)
- Georeferencing drone video (Roboflow): [blog.roboflow.com/georeferencing-drone-videos](https://blog.roboflow.com/georeferencing-drone-videos/)
- Edge AI platform comparison 2025: [promwad.com](https://promwad.com/news/choose-edge-ai-platform-jetson-kria-coral-2025)
- Video pipeline tuning (9 FPS → 650 FPS): [paulbridger.com](https://paulbridger.com/posts/video-analytics-pipeline-tuning/)
