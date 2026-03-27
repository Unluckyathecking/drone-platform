# Technology Audit: Tube-Launched Folding-Wing Drone Design
**Auditor role:** Independent technology reviewer
**Document reviewed:** 29-Tube-Packaged-Folding-Wing-Design.md
**Date:** 2026-03-26

---

## Verdict Summary

| Claim | Verdict |
|---|---|
| Wings wrapping a 75mm fuselage deploy reliably | CAUTION |
| Spring-loaded deployment achieves ~99.5% per wing | FAIL |
| 550g Variant A mass target | CAUTION |
| Motor starts and stabilises in 2m of freefall | FAIL |
| Tumbling/attitude during freefall is managed | FAIL |
| PERDIX comparison is accurate and informative | FAIL |
| Altitude budget of 15–25m | CAUTION |
| Over-centre detent provides adequate wing lock | CAUTION |

---

## Claim 1: Wing Wrapping Around a 75mm Fuselage Deploys Reliably

**VERDICT: CAUTION**

The geometry is not obviously impossible — each wing panel is 4mm thick and the annular gap between 75mm fuselage and 110mm available diameter is 17.5mm per side, which fits two 4mm panels with margin. That part is fine. The problems are mechanical, not geometric.

The design proposes wings fold *backward then inward* around the fuselage, held by a Kevlar band that shears off the tube lip on ejection. In practice:

- **Tube lip shear release is unreliable in asymmetric ejection.** If the drone exits the tube at even a 2–3 degree angle (which is normal with any ejection variability), one side of the band contacts the lip before the other. One wing releases early, the other does not. The result is violent asymmetric opening that easily exceeds the structural limits of a 4mm foam-core panel mid-swing.
- **Airflow during ejection opposes deployment.** At ejection, the forward velocity of the carrier aircraft (the design assumes air deployment at ~20 m/s carrier speed) creates a ram-air load pressing the folded wings *against* the fuselage. The 0.15 N-m torsion spring must overcome both spring preload and this dynamic pressure. At 20 m/s, stagnation pressure on a 90mm x 100mm folded wing surface is approximately 220 Pa, producing ~2 N opposing force per wing panel — comparable to the spring force. This is not analysed anywhere in the document.
- **The Tomahawk/ALCM comparison is not applicable.** The document references wrap-around wing deployment from cruise missiles as heritage. Those are spring-steel wings on weapons travelling at 200–900 km/h where ram air *assists* deployment by peeling the wing open. At sonobuoy-drop speeds and this design's geometry, the analogy breaks down.

The mechanism is *plausible* but not validated, and the document presents it as solved engineering rather than a development risk.

---

## Claim 2: Spring-Loaded Deployment Failure Rate ~0.25% (99.5% per Wing)

**VERDICT: FAIL**

The 99.5% per-wing reliability figure is invented. No citation, no test data, no reference to comparable systems. This is the most dangerous claim in the document because it underpins the entire FMEA.

Real data from comparable small-scale spring-loaded mechanisms:

- **PERDIX (the primary reference the document itself cites):** The first operational PERDIX drop from F/A-18 dispensers in 2016 (103 drones) had a documented deployment success rate of approximately 93% — not 99.75%. Several drones failed to separate from dispensers or failed to establish stable flight. This is after years of DARPA development.
- **Coyote Block 1 (second reference cited):** Early Coyote deployments from sonobuoy tubes had documented issues with tail fin deployment sequencing. AeroVironment spent multiple development cycles on the deployment mechanism before achieving consistent results.
- **LOCUST (third relevant system):** The ONR LOCUST programme had publicly documented deployment sequencing failures in early trials, with reliable sequential deployment only achieved after significant work on tube-exit mechanics.

Spring-loaded mechanisms in small UAVs operating in the 50–700g class have demonstrated real-world first-article reliability in the 85–95% range, not 99.5%. The 0.25% combined failure rate claim (implying independent failures) is circular: it uses the assumed 99.5% figure with no empirical grounding. A realistic FMEA should assume 3–8% combined deployment failure probability for a first-build system. That changes the risk profile of the FMEA table entirely.

---

## Claim 3: 550g Weight Target for Variant A with Full Avionics

**VERDICT: CAUTION**

The mass budget arrives at 511g, which appears to leave margin. Examining the line items reveals several systematic optimism errors:

- **Airframe at 80g** assumes 3D-printed nylon or a carbon tube. A 420mm fuselage tube in 75mm diameter in carbon fibre typically runs 60–90g for the tube alone, before any bulkheads, mounting rails, access hatches, or payload bay structure. The document lists no mass for internal structure.
- **Flight controller at 12g** specifies a "Custom STM32F4 or Matek F405 Nano." The Matek F405 Mini weighs 11g bare board. By the time connectors, vibration mounts, and conformal coating are added for the deployment shock loads (up to 3.3g axial in air deployment, higher in ground-pneumatic deployment), 18–22g is more realistic.
- **Battery at 50g for 2S 850mAh** is tight. The Tattu 2S 850mAh LiPo is 48g — acceptable — but the document claims "~20 min endurance at cruise." At cruise for a 550g fixed-wing with AR ~9, cruise power is roughly 8–12W. At 12W from a 7.4V 850mAh (6.3 Wh) pack, endurance is 6.3/12 = 31 minutes theoretical, with real-world derating giving ~20 minutes. That part checks out. However, the claimed payload of 100g is already included in the 511g total, meaning the system only works if you commit to a specific payload weight. A heavier camera payload instantly breaks the weight budget.
- **Wiring at 12g** is low for a system with ESC, FC, GPS, receiver, payload connector, and motor running through a 420mm tube body. 18–25g is more typical.
- **Missing mass:** No entry for the ejection piston interface, tube cap latch, conformal GPS antenna, pitot tube and lines, wing lock detent actuator, or any sealant/weatherproofing. These items collectively add 15–30g.

Revised realistic minimum mass: ~580–620g, outside the 550g target. The 700g maximum is likely achievable, but "550g" should be relabelled as an aspirational lower bound requiring aggressive mass reduction on every component simultaneously.

---

## Claim 4: Pusher Prop Starts and Stabilises in 2m of Freefall

**VERDICT: FAIL**

This is the most physically problematic claim in the document. The deployment timeline states:

- T = 0.35s: wings fully deployed
- T = 0.40s: motor starts
- T = 0.50s: prop fully deployed, generating thrust
- T = 0.70s: drone pulled out of dive, climbing or level

The document's own freefall calculation gives 1.13m altitude loss by T = 0.35s. During T = 0.35s to T = 0.70s, the drone is in a dive converting altitude to airspeed, and "altitude loss during 0.35–0.70s" is listed as 8–15m. So the real altitude loss before stabilisation is 9–16m, not 2m.

But the prop start claim deserves separate examination. A 6-inch folding prop on a 2206 brushless motor, starting from stationary in freefall:

- **The blades do not deploy instantly.** Centrifugal deployment requires the motor to spin up first. A cold-start brushless motor through a BLHeli ESC takes 0.3–0.8 seconds to ramp from 0 to 3000 RPM depending on ESC timing settings. During this ramp, the prop blades are partially deployed and asymmetric — creating vibration that feeds into the IMU exactly when ArduPilot is trying to establish attitude.
- **The motor is at the *rear* of a nose-diving drone.** When the drone exits the tube nose-first and wings begin deploying, the drag on the deploying wings creates a nose-down pitching moment. The motor is behind the centre of gravity. Starting the motor now produces thrust pushing the nose further down. The document states ArduPilot enters FBWA at T = 0.50s, but FBWA requires valid airspeed and attitude. During prop spin-up the IMU is experiencing vibration from the unfolding prop, and attitude is still transient from wing deployment. FBWA cannot stabilise what it cannot accurately measure.
- **Prop wash in a dive interacts with the tail.** A pusher configuration firing up during a nose-down attitude sends the prop wash forward over the fuselage and directly into the cruciform tail. At high angle of attack (which a nose-diving drone has), this creates unpredictable pitch and roll moments. This is not modelled.

The T = 0.70s "pulled out of dive, climbing or level" claim requires the drone to decelerate from dive airspeed, establish positive AoA, and pull out — all in 0.20s after motor start. For a 550g drone at 15–20 m/s dive speed with ~5W of available thrust margin, the pull-out arc is more realistically 2–4 seconds and 20–40m of altitude. The 50m minimum deployment altitude stated in the document should be at least 80–100m.

---

## Claim 5: Tumbling During Deployment Is Managed

**VERDICT: FAIL**

The document almost entirely ignores tumbling. The freefall section calculates clean nose-down freefall with Cd = 0.82 (cylinder). This assumes the drone exits the tube with zero angular velocity. In practice:

- **Asymmetric drag from partial wing deployment creates roll and yaw moments** that begin the instant one wing deploys before the other — which the document acknowledges is possible in failure modes but treats as a failure mode rather than the norm. Even in "successful" deployment, the two torsion springs (0.15 N-m each) will not fire in perfect synchrony. A 10ms timing difference between left and right wing deployment produces a roll impulse of approximately 0.015 N-m-s. At the drone's estimated roll moment of inertia (~0.002 kg-m^2 for a 700mm wingspan drone), this produces an initial roll rate of 7.5 rad/s = 430 deg/s. The document's FMEA flags >300 deg/s as an uncontrollable condition. Normal deployment may routinely exceed this.
- **No drogue or stabiliser is included.** Real tube-launched weapons and drones (Coyote, Switchblade, PERDIX) either use a drogue chute, fin geometry designed to produce rapid weathervaning, or both. The cruciform tail of Variant A is only 60mm span — on a 75mm diameter body with 420mm length, the fineness ratio means the tail provides almost no passive weathervaning stability at the speeds present during deployment. The drone is aerodynamically unstable in the first 0.2–0.3 seconds post-ejection.
- **ArduPilot cannot stabilise during tumbling.** The FC's IMU has gyro rate limits (typically ±2000 deg/s on a standard MEMS gyro) and the EKF (Extended Kalman Filter) requires several valid cycles to converge on attitude. If the drone is rolling at 400+ deg/s, the EKF is saturated. This is not discussed anywhere.

---

## Claim 6: PERDIX Comparison Is Accurate

**VERDICT: FAIL**

The document references PERDIX as a validation reference ("Reference: PERDIX, Coyote Block 1") and cites PERDIX packing density (~200 drones/m^3 in a flare dispenser). What the document omits:

- **PERDIX is not a fixed-wing with folding wings in the conventional sense.** PERDIX uses a delta-wing airframe where the wings and body are essentially one unit that unfolds from a folded position. It does not have separate wing panels deploying via torsion springs on root hinges. The comparison is not mechanically equivalent.
- **PERDIX does not have a pusher motor that starts mid-deployment.** PERDIX is a glider-class drone that establishes a glide and then (in some variants) uses a small motor. The deployment dynamics are fundamentally different.
- **PERDIX had significant development problems the document ignores.** The PERDIX programme ran from approximately 2013 to 2017 before operational demonstration. Key issues included: GPS acquisition failures after high-G ejection from F/A-18 flare dispensers; swarm communication dropouts; battery performance in cold high-altitude conditions; and deployment sequencing. The programme required DARPA, MIT Lincoln Laboratory, and Naval Air Warfare Center collaboration over four years to demonstrate 103 drones from three F/A-18s. None of this history informs the document's engineering risk assessment.
- **The mass comparison is misleading.** PERDIX weighs approximately 290g and fits the sonobuoy-derived flare dispenser naturally because it was *designed around* that constraint from the start. Variant A is 550–700g and is being *retrofit* into a sonobuoy form factor. The extra mass matters enormously for ejection dynamics and the pull-out altitude budget.

---

## Claim 7: Altitude Budget of 15–25m

**VERDICT: CAUTION**

The 15–25m altitude loss estimate from ejection to level flight is internally consistent with the document's own timing, but the timing itself is optimistic (see Claims 4 and 5). A more conservative estimate accounting for realistic prop spin-up (0.3–0.8s additional), tumble recovery time if any angular rates develop (add 0.5–2s), and a longer pull-out arc gives an altitude budget of 35–70m. The stated minimum deployment altitude of 50m AGL is therefore marginal to inadequate for a first-build system. 80m minimum is more defensible; 120m is prudent for early flight testing.

---

## Claim 8: Over-Centre Detent Provides Adequate Wing Lock

**VERDICT: CAUTION**

The design relies on an over-centre spring detent to lock each wing at 2–3 degrees dihedral. The document states the detent requires "~5x the deployment spring force to overcome." For a 0.15 N-m deployment spring, that is 0.75 N-m to unlock. At cruise (10–20 m/s), the aerodynamic bending moment on a 350mm semi-span wing loaded to 10–13 g/dm^2 at 2g pull-out manoeuvre loads is:

Lift per wing: ~0.55 kg * 9.81 * 2g / 2 = ~5.4 N
Moment arm to root: ~175mm (centroid of semi-span)
Bending moment: ~0.95 N-m

This exceeds the 0.75 N-m detent engagement force. The wings could theoretically fold under a 2g pull-out, which occurs during every deployment. This needs a positive mechanical lock (pin, bolt, or ratchet), not just an over-centre detent. The Coyote and similar systems use mechanical locking pins released by a separate mechanism precisely to avoid this failure mode.

---

## Overall Assessment

The design is imaginative and shows genuine understanding of the trade space. The system layout, packing geometry, and comparison table are thoughtful. However, the document reads as a planning document rather than an engineering assessment — it presents desired outcomes as if they were validated results.

**The three critical failure risks, in priority order:**

1. **Tumble/attitude instability during deployment** — not adequately addressed; could cause most drones in a swarm to fail.
2. **Wing detent inadequacy under flight loads** — could cause in-flight wing collapse at the worst possible moment (pull-out).
3. **Prop spin-up dynamics** — the timeline is physically inconsistent; the altitude budget needs to double.

Before committing to this form factor, at minimum: drop-test the bare airframe (no wings, no motor) 20 times from 2m height to characterise tumble behaviour; test the wing deployment mechanism with an asymmetric spring firing 20ms apart; and bench-test the ESC/prop start sequence under 3g axial load to verify spin-up time.

The design is not ready to fly. It is ready to be prototyped and destructively tested.
