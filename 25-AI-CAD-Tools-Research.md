# AI-Powered CAD Tools Research for Drone Component Design

> Research date: March 2026 | Current workflow: CadQuery (Python) on macOS
> Budget constraint: Student / limited budget

---

## Table of Contents

1. [Current Workflow Assessment](#1-current-workflow-assessment)
2. [AI-Powered Commercial CAD Tools](#2-ai-powered-commercial-cad-tools)
3. [Free / Student-Accessible Tools](#3-free--student-accessible-tools)
4. [AI Text-to-CAD and Code Generation](#4-ai-text-to-cad-and-code-generation)
5. [Topology Optimization Tools](#5-topology-optimization-tools)
6. [FEA / Stress Analysis Tools](#6-fea--stress-analysis-tools)
7. [Tool Comparison Matrix](#7-tool-comparison-matrix)
8. [Recommended Workflow](#8-recommended-workflow)

---

## 1. Current Workflow Assessment

### CadQuery Strengths (keep using)

The existing `payload-cad/` setup using CadQuery is a strong foundation:

- **Fully parametric** — dimensions defined in `config.py`, changed once, propagated everywhere
- **Version-controlled** — Python scripts live in git alongside the rest of the project
- **STEP + STL export** — already producing industry-standard interchange files
- **Reproducible** — anyone with Python + CadQuery can regenerate the exact same parts
- **AI-friendly** — LLMs can read, write, and debug CadQuery code directly (more on this below)

### CadQuery Gaps (needs complementary tools)

- No topology optimization (cannot remove material from low-stress regions)
- No FEA/stress analysis (cannot verify parts before printing)
- No generative design (cannot explore novel geometries AI might suggest)
- No visual CAD GUI for quick iteration (code-only workflow)
- No rendering/visualisation for documentation

**Verdict: Keep CadQuery as the parametric design backbone. Add complementary tools for optimisation, analysis, and visualisation.**

---

## 2. AI-Powered Commercial CAD Tools

### 2.1 Autodesk Fusion (formerly Fusion 360)

| Attribute | Detail |
|---|---|
| **Company** | Autodesk |
| **What it does** | Full parametric CAD + CAM + CAE with generative design and simulation |
| **AI features** | Generative design (define loads, constraints, manufacturing method; AI explores thousands of shapes). Neural CAD (2025-2026): text-to-BREP geometry generation inside Fusion |
| **Student pricing** | **Free** for students/educators (1-year renewable educational licence) |
| **Generative design access** | Included with educational licence; uses cloud credits per study |
| **STEP import/export** | Full STEP support (import and export) |
| **macOS** | Yes, native macOS app |
| **Drone relevance** | High. Generative design excels at lightweight structural parts (motor mounts, arms, frame joints). Integrated FEA verifies parts. CAM module can generate toolpaths for CNC if needed |
| **Compared to CadQuery** | GUI-based, much easier visualisation, but designs are not code-based or git-tracked. Best used alongside CadQuery, not as a replacement |

**Key limitation:** Generative design consumes cloud credits. Educational licences include credits, but heavy use may exhaust them. Each generative study can take hours of cloud compute.

### 2.2 nTopology (nTop)

| Attribute | Detail |
|---|---|
| **Company** | nTopology |
| **What it does** | Implicit modelling + lattice structures + topology optimisation. Specialises in designs for additive manufacturing |
| **AI features** | Field-driven design using simulation data to vary wall thickness, lattice density, and geometry. Not traditional "AI" but computationally sophisticated optimisation |
| **Student pricing** | **Free** non-commercial licence for students, educators, and researchers via nTop Ed programme |
| **STEP import/export** | STEP import supported; exports to STL, 3MF, and other mesh formats. STEP export limited (implicit geometry does not always convert cleanly to BREP) |
| **macOS** | Windows only (would need a VM, Boot Camp, or remote access) |
| **Drone relevance** | Very high. A high school intern designed and 3D-printed a tricopter drone using nTop in six weeks. Lattice structures can reduce drone component mass by 30-50% while maintaining strength |
| **Compared to CadQuery** | Complementary. Design base geometry in CadQuery, export STEP, import into nTop for lattice infill and optimisation |

**Key limitation:** Windows-only. Requires Boot Camp, Parallels, or a Windows machine.

### 2.3 PTC Creo Generative Design

| Attribute | Detail |
|---|---|
| **What it does** | Generative design with thermal + mechanical + weight constraints |
| **Student pricing** | PTC Creo Student edition available free; generative design module included in some educational packages |
| **STEP support** | Full STEP import/export |
| **macOS** | Windows only |
| **Drone relevance** | Moderate — better suited to complex assemblies in larger organisations |

### 2.4 Siemens NX

| Attribute | Detail |
|---|---|
| **What it does** | Enterprise-grade CAD with AI-driven design automation |
| **Student pricing** | Siemens offers academic licences through universities, not generally available to individual students |
| **macOS** | Windows/Linux only |
| **Drone relevance** | Overkill for this project. Aimed at automotive/aerospace enterprises |

### 2.5 Shapr3D

| Attribute | Detail |
|---|---|
| **Company** | Shapr3D (Siemens Parasolid kernel) |
| **What it does** | Direct + parametric modelling with AI rendering. Designed for macOS/iPad |
| **AI features** | AI-powered visualisation renders, adaptive UI. No generative design yet |
| **Student pricing** | Free tier available with limited features; full plans from ~$25/month |
| **STEP support** | Full STEP import/export |
| **macOS** | Native macOS + iPad (its primary platform) |
| **Drone relevance** | Good for quick visual modelling and presentations. Not a replacement for CadQuery's parametric power or Fusion's analysis tools |

---

## 3. Free / Student-Accessible Tools

### 3.1 FreeCAD 1.0 (Open Source)

| Attribute | Detail |
|---|---|
| **Cost** | Free, open source |
| **What it does** | Full parametric CAD with FEM workbench for analysis |
| **AI/optimisation addons** | **FEMbyGEN** workbench (generative design for additive manufacturing, topology optimisation). **ToOptix** addon (topology optimisation via FEM). **BESO** script (bidirectional evolutionary structural optimisation) |
| **STEP support** | Full STEP import/export |
| **macOS** | Yes |
| **Drone relevance** | High. FreeCAD 1.0 (released late 2024) fixed the infamous topological naming problem. FEM workbench with CalculiX solver handles stress analysis. Topology optimisation addons (FEMbyGEN) can optimise drone structural parts |
| **Compared to CadQuery** | GUI-based parametric design. Can import CadQuery STEP files for FEA and optimisation |

### 3.2 Onshape (Free Education Plan)

| Attribute | Detail |
|---|---|
| **Cost** | Free for students and educators |
| **What it does** | Cloud-based parametric CAD with real-time collaboration |
| **STEP support** | Full STEP import/export |
| **macOS** | Browser-based (works on any OS) |
| **Drone relevance** | Good for collaborative design and assemblies. No built-in generative design or topology optimisation |

### 3.3 OpenSCAD

| Attribute | Detail |
|---|---|
| **Cost** | Free, open source |
| **What it does** | Programmatic CAD using its own scripting language |
| **macOS** | Yes |
| **Drone relevance** | Similar philosophy to CadQuery but less powerful. CadQuery is the better choice. OpenSCAD uses CSG (mesh-based) while CadQuery uses BREP (solid modelling) |

---

## 4. AI Text-to-CAD and Code Generation

### 4.1 Zoo.dev Text-to-CAD (formerly KittyCAD)

| Attribute | Detail |
|---|---|
| **Company** | Zoo (backed by Sequoia Capital, GitHub co-founders) |
| **What it does** | Generates real B-Rep CAD models from text prompts. Not artistic meshes — actual engineering geometry with feature trees |
| **Pricing** | Free tier: 40 minutes/month. Additional: $0.50/minute |
| **Output formats** | STEP, STL, PLY, OBJ, glTF, GLB, FBX |
| **Quality** | Produces editable STEP files that can be imported into any CAD tool. Full feature tree, editable parameters. Best for single components with explicit geometric descriptions |
| **macOS** | Browser-based + API + Blender addon |
| **Drone relevance** | Useful for rapidly prototyping individual components (motor mounts, sensor brackets, antenna housings). Not suitable for complex assemblies or parts requiring precise tolerances |
| **Limitations** | Single objects only. Requires very explicit geometric descriptions. Vague prompts produce poor results |

**Best use case:** Quick prototyping of brackets, housings, and simple structural parts. Then refine in CadQuery for parametric control.

### 4.2 LLM-Generated CadQuery Code (Claude / GPT)

| Attribute | Detail |
|---|---|
| **What it does** | LLMs generate CadQuery Python scripts from natural language descriptions |
| **Cost** | Already available through Claude Code (this tool) |
| **Quality** | Recent research (Text-to-CadQuery, 2025) shows fine-tuned LLMs achieving 69.3% exact match on CAD generation. With error feedback loops, code execution success rises from 53% to 85% |
| **Drone relevance** | **Very high.** This is already the project's workflow. Claude can generate, debug, and refine CadQuery scripts directly. The parametric nature means dimensions can be adjusted after generation |

**This is the most cost-effective AI CAD approach for this project.** The existing CadQuery + Claude Code workflow is essentially a text-to-CAD pipeline that produces version-controlled, parametric, editable STEP files.

### 4.3 Hyperganic

| Attribute | Detail |
|---|---|
| **Company** | Hyperganic |
| **What it does** | Algorithmic engineering software for additive manufacturing. Creates lattice structures and complex geometries |
| **Pricing** | Hyperganic Core is free for non-commercial/open-source use. HyDesign (lattice tool) has a 14-day free trial |
| **Drone relevance** | Interesting for lattice-based lightweight structures, but niche and less mature than nTop |

### 4.4 Autodesk Neural CAD (Coming 2026)

Autodesk is developing "Neural CAD for geometry" within Fusion. This will allow text-to-BREP generation directly inside Fusion, creating geometry that can then be edited with standard Fusion tools. Worth monitoring, but not yet released for general use.

---

## 5. Topology Optimization Tools

### 5.1 Altair Inspire

| Attribute | Detail |
|---|---|
| **Company** | Altair |
| **What it does** | Industry-leading topology optimisation and generative design. Define loads, constraints, and manufacturing methods; the solver removes material from low-stress regions |
| **Student pricing** | Altair offers student licences through universities. Free Altair Student Edition available for enrolled students |
| **STEP import** | Yes, imports STEP files |
| **macOS** | Windows only |
| **Drone relevance** | Very high. Achieves 30-40% mass reduction on drone frames while maintaining structural integrity. Optimised designs ready for 3D printing |
| **Research evidence** | Studies show topology-optimised drone frames cut mass by 37.3% with FDM printing |

### 5.2 FreeCAD + FEMbyGEN (Open Source)

| Attribute | Detail |
|---|---|
| **Cost** | Free, open source |
| **What it does** | Topology optimisation integrated into FreeCAD's FEM workbench. Uses CalculiX solver |
| **STEP support** | Full import/export |
| **macOS** | Yes |
| **Drone relevance** | Good entry-level topology optimisation. Less powerful than Altair Inspire but free and runs on macOS |

### 5.3 Python Topology Optimization Libraries

| Library | Description | Maturity |
|---|---|---|
| **TopOpt** | Python library with MMA solver, minimum compliance problems | Active, documented |
| **FEniTop** | Built on FEniCSx. 2D and 3D topology optimisation with parallel computing | Academic, 2024 paper |
| **fenics-topopt** | Lightweight SIMP-based optimisation in FEniCS | Educational/research |
| **BESO (beso)** | Bidirectional evolutionary structural optimisation for FreeCAD + CalculiX | Maintained on GitHub |

**Python topology optimisation fits naturally into the CadQuery workflow** — design in CadQuery, export mesh, optimise in Python, re-import the optimised shape.

### 5.4 Fusion 360 Shape Optimization

Built into Fusion's Simulation workspace. Available with educational licence. Less powerful than dedicated tools like Altair Inspire but integrated into the same environment as generative design.

---

## 6. FEA / Stress Analysis Tools

### 6.1 SimScale (Cloud-Based)

| Attribute | Detail |
|---|---|
| **Cost** | Free Community Plan (3,000 core-hours, projects are public) |
| **What it does** | Cloud FEA + CFD. Structural analysis, thermal simulation, and aerodynamics |
| **Solvers** | Code_Aster, CalculiX (both open source, industrial-grade) |
| **STEP import** | Yes |
| **macOS** | Browser-based |
| **Drone relevance** | Very high. Can simulate drone airframes, landing gear, rotor blade stress, and even aerodynamic performance. Specific drone simulation templates available |

### 6.2 FreeCAD FEM Workbench

| Attribute | Detail |
|---|---|
| **Cost** | Free, open source |
| **Solver** | CalculiX (integrated) |
| **macOS** | Yes |
| **Drone relevance** | Good for basic structural analysis of individual parts. Import STEP from CadQuery, apply loads, check stress concentrations |

### 6.3 ANSYS Student Edition

| Attribute | Detail |
|---|---|
| **Cost** | Free for students |
| **Limitation** | 32,000 node limit (sufficient for individual drone parts, not full assemblies) |
| **macOS** | Windows only |
| **Drone relevance** | Industry-standard FEA. Good for validating critical structural parts |

### 6.4 Fusion 360 Simulation

| Attribute | Detail |
|---|---|
| **Cost** | Included with educational licence (limited cloud credits) |
| **macOS** | Yes |
| **Drone relevance** | Integrated with the CAD environment. Static stress, modal, and thermal analysis |

---

## 7. Tool Comparison Matrix

### For a student on macOS with limited budget:

| Tool | Cost | macOS | STEP | AI/GenDesign | TopOpt | FEA | Drone Score |
|---|---|---|---|---|---|---|---|
| **CadQuery** (current) | Free | Yes | Yes | Via LLMs | No | No | 7/10 |
| **Fusion 360** (edu) | Free | Yes | Yes | Yes (credits) | Shape opt | Yes | 9/10 |
| **FreeCAD 1.0** | Free | Yes | Yes | FEMbyGEN | FEMbyGEN | Yes (CalculiX) | 7/10 |
| **Onshape** (edu) | Free | Browser | Yes | No | No | No | 5/10 |
| **SimScale** (community) | Free | Browser | Yes | No | No | Yes (cloud) | 7/10 |
| **Zoo.dev Text-to-CAD** | Freemium | Browser | Yes | Text-to-CAD | No | No | 6/10 |
| **nTopology** (nTop Ed) | Free | Windows only | Import | Lattice/field | Yes | No | 8/10* |
| **Altair Inspire** (student) | Free/Uni | Windows only | Yes | Yes | Yes | Yes | 9/10* |
| **Shapr3D** | Freemium | Yes | Yes | Rendering | No | No | 5/10 |
| **Hyperganic Core** | Free (OSS) | Browser | Limited | Algorithmic | Lattice | No | 4/10 |

*Asterisk: Windows-only penalty. Would need Boot Camp/VM.

---

## 8. Recommended Workflow

### Tier 1: Immediate Setup (All Free, All macOS)

```
CadQuery (parametric design)
    |
    ├── Export STEP ──> Fusion 360 (generative design + FEA + rendering)
    |
    ├── Export STEP ──> FreeCAD (FEMbyGEN topology optimisation + CalculiX FEA)
    |
    └── Export STEP ──> SimScale (cloud FEA + CFD for aerodynamics)
```

**Primary parametric design:** CadQuery + Claude Code (LLM-assisted code generation)
- Keep the current Python-based workflow
- Use Claude to generate/refine CadQuery scripts from natural language
- All designs version-controlled in git
- Export STEP files as the interchange format

**Generative design + visual modelling:** Autodesk Fusion (free educational licence)
- Import STEP files from CadQuery
- Run generative design studies on structural parts (motor mounts, frame joints, arm cross-sections)
- Use built-in simulation for quick stress checks
- Use rendering tools for documentation

**Topology optimisation (free, macOS):** FreeCAD 1.0 + FEMbyGEN
- Import STEP from CadQuery
- Run topology optimisation to remove material from low-stress regions
- Export optimised geometry back to STL for 3D printing

**Serious FEA/CFD:** SimScale (free community tier)
- Upload STEP files for cloud-based structural + aerodynamic analysis
- Verify drone frame stress, propeller loads, landing impact forces

### Tier 2: When Budget Allows or Windows Available

**Advanced topology optimisation + lattice structures:** nTopology (free student licence, Windows required)
- The gold standard for drone lightweighting
- Import CadQuery STEP, apply lattice infill, variable wall thickness
- Export optimised STL for 3D printing

**Enterprise-grade FEA:** ANSYS Student Edition (free, Windows required)
- When SimScale's 3,000 core-hours run out or for more complex analyses

### Tier 3: Experimental / Monitoring

**Zoo.dev Text-to-CAD:** Use the free 40 min/month for rapid prototyping of brackets and housings. Good for generating starting geometries that you then refine in CadQuery.

**Autodesk Neural CAD:** Monitor for general availability in Fusion. When released, this will bring text-to-BREP directly inside Fusion.

**Python topology optimisation (TopOpt, FEniTop):** For advanced users comfortable with FEA mathematics. Can be integrated directly into the CadQuery Python pipeline.

### Design-to-Print Pipeline

```
1. CONCEPT ──────────> Claude + CadQuery (text-to-code-to-STEP)
2. OPTIMISE ─────────> Fusion generative design OR FreeCAD FEMbyGEN
3. ANALYSE ──────────> SimScale (cloud FEA) or Fusion simulation
4. ITERATE ──────────> Back to CadQuery (adjust parameters)
5. VERIFY ───────────> Final FEA pass with refined geometry
6. MANUFACTURE ──────> Export STL, slice for 3D printer (PrusaSlicer/Cura)
```

### Priority Actions

1. **Now:** Sign up for [Autodesk Fusion educational licence](https://www.autodesk.com/education/edu-software/fusion) (free, instant access)
2. **Now:** Install [FreeCAD 1.0](https://www.freecad.org/) and the FEMbyGEN addon
3. **Now:** Create a [SimScale](https://www.simscale.com/) community account
4. **Now:** Try [Zoo.dev Text-to-CAD](https://text-to-cad.zoo.dev/) for a quick component
5. **Summer 2026 (build start):** Apply for [nTop Ed](https://www.ntop.com/education/) student licence if Windows access is available
6. **Ongoing:** Continue using Claude + CadQuery as the primary parametric design pipeline

---

## Sources

- [AI in CAD: How 2025 is Reshaping Mechanical Design Workflows](https://mecagent.com/blog/ai-in-cad-how-2025-is-reshaping-mechanical-design-workflows)
- [3 AI Features Coming to Every CAD Program in 2026](https://www.engineering.com/3-ai-features-coming-to-every-cad-program-in-2026/)
- [Autodesk Neural CAD](https://www.engineering.com/is-autodesks-neural-cad-worth-getting-excited-about/)
- [Zoo.dev Text-to-CAD](https://zoo.dev/text-to-cad)
- [Zoo.dev Pricing](https://zoo.dev/zoo-pricing)
- [Open-Source AI Text-to-CAD by Zoo](https://3dprintingindustry.com/news/open-source-ai-text-to-cad-software-by-zoo-unlocks-accessible-3d-design-236964/)
- [Text-to-CadQuery: A New Paradigm for CAD Generation](https://arxiv.org/abs/2505.06507)
- [nTopology Education Programme](https://www.ntop.com/education/)
- [nTop Topology Optimization with Data Fields](https://www.ntop.com/resources/webinars/topology-optimization-using-data-fields-and-implicit-modeling/)
- [Autodesk Fusion Free for Students](https://www.autodesk.com/education/edu-software/fusion)
- [Fusion 360 Generative Design Access](https://www.autodesk.com/support/technical/article/caas/sfdcarticles/sfdcarticles/How-to-get-access-to-Generative-Design.html)
- [FreeCAD Addons](https://www.freecad.org/addons.php)
- [FEMbyGEN Workbench for FreeCAD](https://wiki.freecad.org/FEMbyGEN_Workbench/en)
- [ToOptix FreeCAD Addon](https://github.com/Foxelmanian/ToOptixFreeCADAddon)
- [TopOpt Python Library](https://pytopopt.readthedocs.io/en/latest/)
- [FEniTop: FEniCSx Topology Optimization](https://link.springer.com/article/10.1007/s00158-024-03818-7)
- [SimScale Drone Simulation](https://www.simscale.com/simulations/drone/)
- [Altair Inspire](https://altair.com/inspire)
- [Drone Frame Optimization via Simulation and 3D Printing (2025)](https://www.mdpi.com/2073-431X/14/8/328)
- [Topology Optimization of Drone Frames (AIAA)](https://arc.aiaa.org/doi/abs/10.2514/6.2023-0964)
- [Hyperganic](https://www.hyperganic.com/)
- [Shapr3D](https://www.shapr3d.com/)
- [Best Free CAD Software 2026 (Beebom)](https://beebom.com/free-cad-software/)
- [9 Free CAD Tools to Explore in 2025](https://www.genense.com/blog/9-free-cad-tools-to-explore-in-2025/)
- [Generative Design Software (Dassault)](https://www.3ds.com/store/cad/generative-design)
