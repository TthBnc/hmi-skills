# HMI design process (end to end)

Evidence tags: `[V: source]` = checked against a read source; `(summary)` = secondary or vendor summary, primary not read; `(verify)` = recalled or synthesised, check before relying on it. Domain-neutral: "machine" means any equipment an operator runs.

## Contents
1. The lifecycle in one page
2. Context of use: personas, environment, tasks
3. Field research methods
4. Task analysis (HTA, CTA) with worked example
5. Use-error risk analysis (FMEA worksheet)
6. ISA-101 document set: philosophy, style guide, toolkit
7. Prototyping, design reviews, gates, operator involvement
8. Evaluation: heuristics, walkthrough, usability tests, metrics
9. Field trials, FAT/SAT, MOC
10. Alarm and display KPIs
11. Common mistakes
12. Sources

## 1. The lifecycle in one page

ISA-101 frames HMI work as Design, Implement, Operate, with management of change (MOC), audit and validation running through all stages [V: Yokogawa and ARC summaries of ISA-101]. A non-process product can use the same loop:

1. Research users, tasks, environment.
2. Write the philosophy (principles, goals, responsibilities).
3. Write the style guide; build the toolkit (tested reusable widgets).
4. Design screens, prototype, review with operators.
5. Implement and test (FAT).
6. Commission (SAT), train, operate.
7. Monitor KPIs, audit, change only through MOC, loop back.

Entry rule (verify): do not draw a screen until you can write on one page who uses the machine, the 5 to 10 most frequent tasks, and the 3 worst mistakes possible.

Pick the regime first: process plant (ISA-101 is the lifecycle), machine on the EU market (Machinery Regulation and machine standards bind; ISA-101 and ISO 9241 are good practice), medical (IEC 62366 and FDA are mandatory) (summary). ISO 9241-210 is the generic human-centred loop behind all of them: understand context, specify requirements, produce designs, evaluate, iterate (verify).

## 2. Context of use

### 2.1 Roles (define by skill, frequency, authority; not demographics)

| Role | Needs | Typical failure |
|---|---|---|
| Novice / occasional operator | Guided flows, plain words, safe default, undo | Misses mode, hesitates, over-trusts defaults |
| Expert / daily operator | Speed, density, predictability, no extra confirms on routine acts | Habit capture: clicks through confirmations |
| Supervisor / shift lead | Overview, history, handover notes | Needs data the operator screen hides |
| Maintenance technician | Diagnostics, I/O, manual jog, calibration, logs | Powerful functions reachable by operators |
| Commissioning / service engineer | Config, tuning, simulation, overrides | Leaves test overrides active |
| Administrator / IT | Users, backups, updates, network | Change breaks operations unannounced |
| Remote observer / support | Read-only view, same terminology | Mistaken for local operator; unintended control |
| Auditor | Audit trail, exports | Records not traceable |

(All rows: verify; standard human-factors practice.)

Rule: design the default operator screen for the novice under stress; give experts speed through consistency, not hidden features (verify).

Persona card fields: role; goals; top tasks (frequency x criticality); environment; devices; skill and training; information needs; typical errors; research quotes; permissions required.

### 2.2 Environment checklist
Lighting (lux, direct sun, glare); noise; temperature and rain; gloves; vibration; viewing distance and angle; mounting height; hands busy or one-handed use; interruptions; shift pattern; language(s); connectivity.

### 2.3 Task inventory
List tasks by frequency x criticality: start-up, routine run, shift handover, pause/resume, recovery after fault, recipe change, calibration, maintenance, shutdown. Mark critical tasks (wrong action causes harm, damage or loss). This list drives scenarios later.

## 3. Field research methods (cheapest first)

- Stakeholder interviews: operators, supervisors, maintenance, safety officer, trainers, support. Ask for the last time something went wrong, workarounds, what they ignore.
- Contextual inquiry (verify): watch real work in the real place, ask questions while it happens; principles: go to the place, user is the expert, confirm interpretations, keep a research question.
- Shadow across shifts; night and weekend crews differ.
- Artifact collection: photos of sticky notes, paper checklists, hand-made cheat sheets. Each is a missing HMI feature.
- Log and alarm analysis: what operators press, which alarms are acknowledged without action.
- Incident and near-miss review.
- Surveys only after interviews; they confirm, they rarely discover.
- Environment survey (2.2).

Per observation record: who, task, trigger, tools, information needed, decision, consequence, pain point.

## 4. Task analysis

### 4.1 Hierarchical task analysis (HTA) (verify)
Steps: state the goal; list 4 to 8 sub-goals; decompose until leaves are observable actions or decisions; write a plan per node (order or condition); stop when further detail has no design consequence. Use the tree to find information needed per step, controls needed, memory-dependent steps, irreversible steps, and points where the operator must leave the screen.

### 4.2 Cognitive task analysis (CTA) (verify)
Capture what operators must know and decide. Techniques: critical decision method (interview on one non-routine incident: cues noticed, options, what experts knew that novices miss), think-aloud, simulation walk-throughs, knowledge audit, decision ladders. Output: cues and thresholds that must be on screen, novice traps, ambiguity points. Optionally map workload on a timeline to find overload moments; use work-domain analysis only for complex systems.

### 4.3 Worked example (generic: "replace a worn consumable during a run")

```
0. Replace consumable during run
   Plan 0: do 1, 2, 3 in order; if 3 fails return to 2
 1. Hold machine safely
    Plan 1: 1.1 then 1.2; 1.3 only if access needed
    1.1 Press Pause        1.2 Verify state = Held       1.3 Verify guard open
 2. Exchange part
    2.1 Remove old  2.2 Fit new  2.3 Enter part ID / reset wear counter
 3. Resume and verify
    3.1 Check no fault  3.2 Press Resume  3.3 Watch first cycle, confirm value in range
```
CTA overlay for step 1.2: cue = state label says Held (not just a dimmed button); novice trap = Paused vs Held look alike; expert shortcut = glance at state colour. Design consequences: state word large and always visible; Resume disabled with reason until 2.3 done; wear counter reset prompts before, not after, Resume; step 3.3 needs a live value with an age indicator.

## 5. Use-error risk analysis

Use error means an action or omission giving a result other than intended; it is not "operator error", it assumes the design allowed it (verify). IEC 62366-1 ties usability to ISO 14971 risk management; FDA's guidance cites 62366-1:2015+AMD1:2020 and covers use-related risk analysis, formative evaluation and validation [V: FDA human factors guidance, fda.gov/media/80481/download]. The method is useful for any machine HMI.

Process outline (verify; standard paywalled): (1) use specification; (2) safety-related UI characteristics; (3) hazards and hazardous situations; (4) hazard-related use scenarios; (5) select scenarios for summative test; (6) UI specification and evaluation plan; (7) formative evaluations, iterate; (8) summative evaluation; (9) usability engineering file.

### 5.1 Use-error FMEA worksheet

| Column | Content |
|---|---|
| ID | Row key |
| Task step | From the HTA |
| Possible use error | Omission, commission, wrong order, wrong object, wrong timing, wrong value |
| Cause | Design-induced and situational (glare, gloves, stale data) |
| Effect | On people, machine, product |
| Severity S | Scale defined in the project (for example 1 to 5) |
| Occurrence O | Likelihood scale |
| Detectability D | Chance the operator or system notices before harm |
| Existing controls | Interlock, confirmation, range limit |
| Risk | Combined per project rule (matrix or S x O x D) |
| Mitigation | Hierarchy below |
| Residual risk | After mitigation |
| Verified by | Test ID |

Mitigation hierarchy (verify): (1) eliminate by design (make the wrong action impossible); (2) guard in the interface (interlock, consequence confirmation, range limit, undo); (3) inform (warning, label, state display); (4) train. Training alone is the weakest control.

Error prompts: adjacent or similar buttons; wrong mode; unit confusion or decimal slip; stale display; delayed feedback leading to repeated commands; forgotten step; sequence error; mistaking remote for local; changing another operator's setpoint.

## 6. ISA-101 document set

Per secondary sources: philosophy is platform-independent (principles, goals, lifecycle, responsibilities); style guide applies it to one platform; toolkit is the library of pre-engineered, tested graphic elements [V: Yokogawa and ARC summaries]. One vendor cites 75+ pages for a plant philosophy; another blog estimates 20 to 50 (summary). A short one is fine for a small product if every item below is answered somewhere. ISA-101 sets colour rules per site, not globally; do not cite colour lists as "required by ISA-101" (summary).

### 6.1 HMI philosophy: outline
1. Purpose and scope (products, users, screens; out of scope: safety layer)
2. Reference documents (ISA-101, ISA-18.2, ISO 9241-210, IEC 62366-1 if relevant, company safety docs)
3. Definitions (mode, state, alarm vs alert vs message)
4. Roles and responsibilities (owner, design authority, safety reviewer, operator reps, change approver)
5. Design principles (state always visible; never lie about staleness; one way per task; consequence-aware confirmation; calm by default)
6. Operator environment and ergonomics
7. Display hierarchy and navigation (levels, maximum depth to any control)
8. Information content rules (always visible; per level; units; trends)
9. Colour, symbol, typography philosophy (colour scarce, redundant coding)
10. Alarm philosophy interface (link to a separate ISA-18.2-style document)
11. Control interaction (select-before-operate, confirmation by consequence, setpoints, interlock feedback, acknowledgement)
12. Access, authentication, authority, remote vs local
13. Mode, state and fault presentation; degraded modes; comms loss
14. Data quality and staleness
15. Language, units, time
16. Help, training, simulation
17. Logging and audit
18. Lifecycle: FAT/SAT, KPIs, MOC, audit, retirement
19. Performance targets (response, update rate, startup, availability)
20. Appendices: glossary, personas, task inventory, risk register link

### 6.2 Style guide: outline
1. Platform: framework, screen sizes, touch or mouse, kiosk limits
2. Grid and layout templates (header, status bar, navigation, work area, alarm banner, margins)
3. Colour tokens, meanings, contrast, theme variants, forbidden uses
4. Typography: sizes by role, minimum at viewing distance, tabular digits
5. Symbols and icons, with labels where meaning is not universal
6. Live values: digits, units, range, setpoint vs actual, out-of-range and bad-quality styling
7. Controls: sizes, spacing, states (enabled, disabled with reason, pending, active, failed), numeric entry
8. Confirmation, undo, message wording (what happened, meaning, what to do)
9. Navigation and naming conventions
10. Alarm and notification styling
11. Trend and chart rules
12. Popup and faceplate behaviour
13. Animation and sound rules (usually only alarms move)
14. Localisation rules (text expansion, no text in images)
15. Accessibility (contrast, colour-blind safe, sound alternatives)
16. Object naming, versioning, project structure
17. Do/don't gallery
18. Design-review compliance checklist

### 6.3 Toolkit: catalog entry per element
Name, purpose, version, owner; visual spec with a screenshot per state (normal, abnormal, unknown/stale, disabled, selected, pending, fault); data interface (signals, units, quality handling); behaviour (command flow, confirmation, feedback, timeouts); permissions; automated tests and last run; limits, deprecation, change log.

Rule (verify): a widget that cannot render a defined unknown/stale state is not finished.

## 7. Prototyping, reviews, gates, operators

Fidelity ladder: paper and card sorting, clickable wireframe, coded prototype on a simulator, pilot on a real machine. Prefer a simulated backend with faults and data loss; static mockups hide the hard problems. Use Wizard-of-Oz if no backend exists (verify). See architecture-and-security.md for mock mode.

| Gate | Evidence |
|---|---|
| G0 Concept | Personas, task list, philosophy approved |
| G1 Low-fi | Navigation, content, labels reviewed |
| G2 Interactive prototype | Operators complete tasks |
| G3 Pre-FAT | Screens checked against style guide and risk register |
| G4 After 1 to 3 months in service | Field feedback and KPI review |

(Gates: verify; project convention.)

Reviewers: operators from each shift, maintenance, safety, controls and software engineers, a human-factors person, and someone who has never seen the design.

Per-screen review questions:
- Can a new operator say within 5 seconds the machine state, mode, whether attention is needed, whether data is live?
- Is every action within the navigation depth target?
- Is each control's effect predictable from label and state?
- Are irreversible or hazardous consequences explicit?
- Are units, scale, range shown? Is stale/unknown designed?
- Is colour reserved for meaning; is the screen readable in grayscale?
- Is wording the operators' own, from research?
- Does it match style guide and toolkit?

Operator involvement: operators asked "do you like it" say yes; have them do tasks. Include sceptics. Study their workarounds (verify).

## 8. Evaluation

### 8.1 Formative vs summative
- Formative: during design, small samples (5 to 8 per group is a common heuristic (verify)); the "5 users find 85%" claim is a model with caveats, and FDA Appendix A notes there is no statistically correct sample-size formula [V: FDA 2016 guidance].
- Summative: near-final, representative users, predefined pass/fail on critical tasks, no coaching. FDA says in general at least 15 participants, and at least 15 from each distinct user population [V: FDA 2016 guidance, validation testing section]. Attribute it to FDA, not to IEC 62366.
- Verification = built as specified; validation = works for real users in real use (verify).

### 8.2 Heuristic evaluation
Nielsen's 10 (titles and order confirmed [V: nngroup.com/articles/ten-usability-heuristics, reviewed 2024-01-30]):
1. Visibility of system status. 2. Match with the real world. 3. User control and freedom. 4. Consistency and standards. 5. Error prevention. 6. Recognition rather than recall. 7. Flexibility and efficiency. 8. Aesthetic and minimalist design. 9. Help recognise, diagnose, recover from errors. 10. Help and documentation.

Industrial additions (synthesis, verify): 11 Truthfulness about data (quality, age, source). 12 Mode awareness. 13 Consequence awareness before commit and feedback after. 14 Calm by default. 15 Graceful degradation (comms loss, sensor failure). 16 Environment fit (gloves, glare, distance, noise). 17 Authority clarity (who controls now).

Procedure: 3 to 5 evaluators work independently; severity 0 to 4; record location, heuristic, evidence, fix; merge; rank by frequency x impact x persistence. It finds many issues fast but also false alarms; combine with testing.

### 8.3 Cognitive walkthrough (verify)
Per step ask: will the user try the right effect; will they notice the action is available; will they connect control to effect; will they see progress afterwards. Best for novice and rare flows (setup, recovery, part change). Record failure stories with causes.

### 8.4 Usability test with abnormal situations
Scenarios: normal (start, run, handover, stop); frequent edge (pause/resume, retry after jam, recipe change); abnormal (sensor failure, comms loss, e-stop recovery, conflicting alarms, wrong-mode command, low battery, remote link lost); rare critical (rows from the FMEA).

Method: simulator with injectable faults; think-aloud for formative, silent observation for timing; "freeze probe" (stop, ask what the machine is doing and what happens next); post-task interview. Use real operators or close substitutes, trained only as the product would train them; include novices, experts, maintenance. Roles: facilitator, note-taker, simulator operator; consent; no-blame framing; record screen and audio.

Example pass criterion (verify): every participant completes each critical task without critical use error, or each failure has a root cause and a retested design change.

Test plan skeleton: purpose and critical tasks; participants; environment; task cards; injected faults and timing; data (success, time, errors, SUS, TLX, SA probes); procedure (brief, consent, practice, tasks, debrief); success criteria; analysis; privacy.

### 8.5 Metrics
Performance: task success (binary, partial), time on task, steps vs minimum, errors by type (slip, mistake, omission), recoveries, help requests, time to detect and respond to an abnormal event.

SUS: 10 items, 5-point agreement; odd items score (response - 1), even items (5 - response); sum x 2.5 gives 0 to 100. Benchmark: mean 68 from about 500 evaluations and over 5,000 users; above 80.3 is top 10% (grade A); below 51 is bottom 15% (F) [V: measuringu.com/sus]. Use as a relative benchmark, not a diagnosis. The usual original citation (Brooke 1996) was not confirmed.

NASA-TLX: six subscales (mental, physical, temporal demand; own performance; effort; frustration); overall score is a weighted average, weights from 15 pairwise comparisons per task [V: NASA TM, NTRS 20000021487]. The 0 to 100 range and the unweighted "raw TLX" variant are (verify). Compare designs on identical tasks.

Situation awareness (Endsley): level 1 perceive, 2 comprehend, 3 project (summary). SAGAT freezes the simulation, blanks displays, asks queries on all three levels and compares to ground truth: objective, intrusive, needs a simulator (summary). SART (Taylor 1990) is a post-hoc self-rating of 10 constructs (instability, variability, complexity, arousal, spare mental capacity, concentration, division of attention, information quantity, information quality, familiarity) grouped into 3 dimensions (attentional demand, attentional supply, understanding), 7-point scales; validity evidence is contested (summary: skybrary SART article). Do not describe it as "10 dimensions". Lighter option: probe questions at natural pauses (verify).

Also: Single Ease Question per task, 7-point (verify); trust-in-automation questions (verify).

Report outline: objective; participants; method; scenarios; findings by severity; metrics; critical-task results; root causes; design changes; retest evidence; limits.

## 9. Field trials, FAT/SAT, MOC

Field trial: pilot on 1 to 3 machines or sites; instrument HMI telemetry (screens, presses, error dialogs, alarm counts, time in mode) with consent; in-app "report issue" with log snapshot; site visits comparing real work to the HTA; periodic review of use errors and near-misses feeding the risk register; periodic audit against philosophy and style guide (ISA-101 lifecycle calls for audit [V: ARC summary]).

FAT: at supplier, on bench or simulator, against contractual spec, customer-witnessed, punch list. SAT: on site with real process, network, operators; checks integration, performance, security configuration, training. Both need traceable criteria, scripts with expected results, recorded evidence, deviation handling, sign-off (verify). Full test-plan outline is in architecture-and-security.md section 12.

### MOC for HMI changes
Small edits (moved button, changed unit, new colour) can cause incidents; treat the HMI as safety-relevant (principle in ISA-101 lifecycle [V: Yokogawa/ARC]; specific incident cases not verified).

1. Change request: what, why, who, affected screens, tags, roles.
2. Impact: operator tasks, training, alarms, procedures, firmware/protocol compatibility, safety analysis.
3. Classify: trivial (typo), minor (layout), major (new control, mode logic, alarm). Approval depth grows with class.
4. Design to style guide and toolkit; update risk register.
5. Test: regression plus targeted; operator walkthrough for major.
6. Approve by named roles.
7. Deploy with rollback plan.
8. Tell operators first, in operator language.
9. Update docs.
10. Post-implementation review; keep records.

MOC record: ID, date, requester, description, screens/objects, risk impact, test evidence, approver, deployed version, rollback version, training done.

## 10. Alarm and display KPIs

Alarm numbers come from two different scale families; do not mix them.
- Average alarm rate per operator: IEC 62682 acceptable about 1 per 10 min; EEMUA 191 under 1 per 10 min [V: ABB/IChemE slides 2021-05-06, slide 14]. A ChemEng example uses 12 per hour as long-term maximum and 18 per hour as an example action limit, site-specific [V: chemengonline.com/alarm-management-numbers].
- Peak: fewer than 10 alarms in the first 10 minutes of an upset [V: ABB/IChemE slide 14].
- Share of 10-minute periods with more than 10 alarms per console: under 1% [V: same slide]. A ">5% action limit" was not found (verify). Flood (EEMUA): more than 10 new alarms in 10 min until an interval below 5; simple form: any 10-minute period above 10 [V: ChemEng]. ISA-18.2 wording unchecked (verify).
- Stale (standing) alarms, active about 24 h: IEC under 5, EEMUA under 10 [V: ChemEng; ABB/IChemE].
- Chattering: 3 or more activations in 1 min [V: ChemEng]. Top-10 sources' share: above 20% signals a problem [V: ChemEng]; IEC column lists 1 to 5% [V: ABB/IChemE]; sources differ.
- Priority split about 80% low, 15% medium, 5% high [V: ChemEng; ABB/IChemE slide 24].
- Also track time to acknowledge and resolve; shelved/suppressed count and duration.
- Display KPIs (verify): navigation depth per task, screens per task, unused screens, popups, time on trend vs overview, reported confusion events.
- Operational (verify): unplanned stops from use error, mean time to recover, rework, training time to competence, support calls.

Make every KPI reproducible from the logs.

## 11. Common mistakes
- Drawing screens before research; designing for engineers' vocabulary.
- Asking operators for opinions instead of observing tasks.
- Testing only the happy path; no comms-loss or fault scenarios.
- Treating training or a warning as the fix for a design-induced error.
- Citing the FDA 15-participant figure as an IEC rule, or SART as "10 dimensions".
- Mixing IEC 62682 and ChemEng alarm-rate scales.
- Documents written once, never versioned or tied to MOC.
- "Minor" HMI edits shipped without MOC or operator notice.
- Heuristic evaluation alone, with no user test.
- Leaving test overrides or simulation active after commissioning.

## 12. Sources
- FDA, Applying Human Factors and Usability Engineering to Medical Devices: https://www.fda.gov/media/80481/download
- Nielsen heuristics: https://www.nngroup.com/articles/ten-usability-heuristics/
- MeasuringU SUS: https://measuringu.com/sus/
- NASA-TLX TM: https://ntrs.nasa.gov/citations/20000021487
- SART: https://skybrary.aero/articles/situation-awareness-rating-technique-sart
- ABB/IChemE alarm slides: https://www.icheme.org/media/16019/icheme-alarm-management-practical-guide-06_05_2021.pdf
- ChemEng alarm numbers: https://www.chemengonline.com/alarm-management-numbers/
- Yokogawa ISA-101 summary: https://www.yokogawa.com/us/library/resources/media-publications/isa-101-toward-a-more-effective-hmi-strategy/ ; ARC: https://www.arcweb.com/node/109226
- Primary standards not read: ISA-101.01-2015, IEC 62366-1, ISO 9241-210, ISA-18.2, EEMUA 191.
