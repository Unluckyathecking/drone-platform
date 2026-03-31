# Cambridge Engineering Personal Statement — Draft Framework

**Document:** 45-Cambridge-Engineering-Personal-Statement.md
**Date:** 2026-03-31
**Author:** GTM research — Mohammed Ali Bhai project
**Purpose:** Draft the strongest possible Cambridge Engineering personal statement angle using the MPE project
**Target:** Cambridge Engineering (General, leading to Information Engineering or Electrical & Information Sciences), 2027 entry

---

## WHAT CAMBRIDGE ENGINEERING ADMISSIONS WANTS

Cambridge Engineering interviews are split into two parts:
1. **Technical interview:** Maths and physics problems at A-level and beyond. They test whether you can think, adapt, and reason under pressure — not just recall.
2. **General interview:** Your genuine interest in engineering, independent reading, and what you want to do with the degree. Specific projects are asked about in detail. "Tell me about a project and what you found hard" is a near-universal Cambridge question.

The personal statement is not the primary selection tool at Cambridge (unlike most universities). It serves three purposes:
1. **To pass the threshold** — confirm you have done something real beyond school
2. **To generate interview questions** — anything you write will be probed in interview
3. **To signal intellectual curiosity beyond the syllabus**

The worst personal statement is a list of achievements. The best personal statement is a specific intellectual problem you encountered, how you thought about it, what you still don't understand, and what you want to learn.

**Critical rule:** Only write what you can defend in a 30-minute technical grilling.

---

## THE MPE ANGLE: WHAT MAKES IT GENUINELY STRONG

Mohammed has built something that almost no A-level applicant has built: a working multi-sensor data fusion engine with real-time AI classification, deployed against live global data. This is not a school project. It is objectively impressive to an engineering academic.

However, the personal statement should not be a capabilities list. The Cambridge angle is: **what were the hardest engineering decisions, and why did you make them the way you did?**

### Five intellectually defensible moments from MPE that Cambridge will love:

**1. The Kalman filter decision**
MPE uses haversine spatial correlation for track fusion, not a Kalman filter. Why? Was this right? Kalman filtering would give optimal state estimation under Gaussian noise — but AIS/ADS-B data has non-Gaussian errors (spoofing, dropouts, protocol delays). This is a genuine engineering trade-off a Cambridge interviewer will explore with pleasure.

**2. The classifier architecture choice**
MPE uses rule-based classification (9 rules, threat 0–10) rather than a trained ML model. Why? Because you need explainability for military applications: an operator needs to know *why* a vessel is flagged hostile, not just that it is. This is a deep problem in AI ethics for autonomous systems — a hot research area at the Cambridge Engineering Department (Professor Hatice Gunes, AI and Ethics; Professor Roberto Cipolla, computer vision and autonomous systems).

**3. The CoT protocol choice**
MPE outputs Cursor on Target (CoT) XML rather than building a proprietary display. This is the "sit on top of existing architecture" principle — understood from visiting an Oxford Science Innovation summit. The engineering insight: interoperability as a design constraint. This connects directly to Cambridge's Information Engineering track, which emphasises signal processing, communications, and systems integration.

**4. The headless daemon architecture**
The product is `python -m mpe`, not a web app. The UI is ATAK (existing military standard). This is a systems engineering decision: separate the intelligence layer from the presentation layer, with a well-defined interface (CoT protocol). Cambridge loves systems thinking.

**5. The AIS spoofing detection problem**
Position jump detection (haversine distance between consecutive AIS reports) is the current implementation. But this has false positives (legitimate vessels near land with signal reflection) and misses sophisticated spoofing (gradual position drift). This is an open research problem. Acknowledging what you don't know is the most powerful thing you can write in a Cambridge personal statement.

---

## DRAFT PERSONAL STATEMENT

*(~4,000 characters / 650 words — UCAS limit is 4,000 characters)*

---

In the spring of 2026, I built a piece of software that made a decision I still disagree with. The system was a multi-domain command and control intelligence engine: it ingests live ADS-B aircraft positions from across Europe, AIS ship tracks from maritime receivers, and combines them into a unified picture with anomaly detection and alert generation. The decision was architectural: I used a rule-based classifier rather than a trained machine learning model. Every paper I read told me ML was more capable. I chose the dumber system deliberately.

The reason was explainability. For a military operator responding to an alert — "hostile vessel detected, Strait of Gibraltar, MMSI 123456789, confidence 8/10" — "the neural network said so" is not an acceptable answer. They need a reasoning chain: elevated speed for vessel class, entering restricted zone, AIS signal consistent with spoofing pattern. The intelligence is only useful if the operator can verify it, challenge it, and make a decision. I found myself unexpectedly in the middle of one of the central arguments in machine learning research: the trade-off between capability and interpretability.

The spoofing detection problem is where my own understanding reached its limit. My implementation flags a vessel as potentially spoofing AIS if its consecutive position reports imply an impossible speed — a haversine distance check. This works for crude spoofing. It fails for gradual drift. It produces false positives near coastlines where signal reflection causes apparent position jumps. I know the literature suggests Kalman filtering for track smoothing, but the measurement noise on AIS is non-Gaussian — the Kalman model's assumptions break. I do not yet know the correct solution. I suspect it involves a mixture model that distinguishes sensor noise from intentional deception, but I haven't implemented it. This is the question I most want to study.

The project started differently. I was designing a drone platform — propulsion, airframe, payload integration — when I realised the limiting factor wasn't the hardware. It was the intelligence layer. What matters in autonomous systems is not whether the drone can fly; it is whether the system knows where the drone is, what everything else around it is, and what it should do next. I pivoted the project to focus entirely on the C2 (command and control) problem: how does a system with imperfect, partial, multi-source sensor data build a coherent picture and make confident decisions?

This question connects directly to what I want to study. Cambridge's Information Engineering track addresses exactly the problems I've been building towards: Kalman filtering and state estimation, sensor fusion under uncertainty, decision theory for autonomous systems. I have built a working system with known limitations; I want to understand the mathematics that would fix those limitations.

Beyond the technical, the project taught me something about engineering judgement. Early on I made the dashboard beautiful and the underlying engine broken. A mentor told me: the demo that works is worth more than the demo that looks good. That observation reshaped how I approach problems — start with function, add form. The 692 passing tests in the system are more valuable than any visual output.

I read Judea Pearl's *The Book of Why* last year, which gave me a framework for thinking about the difference between correlation and causation in classifier decisions. I've been working through Kalman's original 1960 paper on optimal linear filtering — the mathematics is tractable, the insight is profound. I'm currently trying to understand whether particle filters are applicable to the AIS spoofing problem given the non-Gaussian noise characteristics.

I want to study engineering at Cambridge because the problems I've encountered in building this system require mathematics I don't yet have: stochastic estimation, information theory, control theory. The project showed me what I don't know. The degree is how I find out.

---

## INTERVIEW PREP — QUESTIONS CAMBRIDGE WILL ASK

These are the questions a Cambridge interviewer will ask based on the personal statement above. Mohammed should be able to answer all of them.

| Question | What the interviewer is testing | Preparation needed |
|----------|--------------------------------|-------------------|
| "Explain how Kalman filtering works and why you didn't use it" | Whether you understand the maths, not just the name | Read Kalman (1960). Understand state transition matrix, measurement model, update equations. Know what Gaussian noise assumption means. |
| "What's the difference between haversine distance and the formula for great-circle distance?" | Basic maths under pressure | Know both formulas. Note they're the same thing — haversine *is* the great-circle formula. This is a trick question. |
| "You said the ML trade-off is capability vs. interpretability. Give me an example where you'd choose the ML model" | Whether you can reason about engineering trade-offs honestly | Correct answer: computer vision, where rule-based systems fail completely and operators only need to know "probably an aircraft". Wrong answer: "I'd always use rules". |
| "What is a mixture model? Why might it apply to your spoofing detection problem?" | Whether you've read the references you cited | A mixture model assigns data points to one of K distributions. Here: legitimate noise ~ narrow Gaussian, spoofing ~ different distribution (e.g. fat-tailed). The EM algorithm fits it. |
| "What does the Kullback-Leibler divergence measure and how is it relevant to information theory?" | General knowledge from reading, not curriculum | KL divergence measures how different one probability distribution is from another. Relevant here: comparing a vessel's reported position distribution against its historical baseline. |
| "Walk me through the architecture of your system" | Technical depth and clarity of thought | Practice the 3-minute version: ingest → fuse → classify → alert → output. Then drill into any layer they ask about. |
| "If you had three months and unlimited compute, what would you build next?" | Intellectual ambition and direction | Answer: particle filter for non-Gaussian AIS track smoothing, plus a computer vision module to correlate SAR satellite imagery with AIS track anomalies. |

---

## BOOKS TO READ BEFORE APPLICATION

These should be genuinely read, not listed in the PS:
- Kalman, R.E. (1960). "A New Approach to Linear Filtering and Prediction Problems" — the original paper. 12 pages. Read it.
- Pearl, J. & Mackenzie, D. (2018). *The Book of Why* — causation and inference in AI. Already cited.
- Bishop, C.M. (2006). *Pattern Recognition and Machine Learning* — Chapter 9 (EM algorithm, mixture models)
- Stone, L.D., Streit, R.L., Corwin, T.L. & Bell, K.L. (2013). *Bayesian Multiple Target Tracking* — the professional reference for the problem MPE is solving
- Thrun, S., Burgard, W. & Fox, D. (2005). *Probabilistic Robotics* — Chapters 2–4 (Bayes filter, Kalman filter, particle filter)

---

## TIMING NOTES

- UCAS application opens: September 2026
- Cambridge Engineering deadline: 15 October 2026 (one year earlier than most courses — Cambridge has its own deadline)
- Written Assessment (ENGAA or Engineering Admissions Assessment): October/November 2026
- Interview: December 2026
- Decision: January 2027
- Entry: October 2027
