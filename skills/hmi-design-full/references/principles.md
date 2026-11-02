# HMI principles: the "why" layer

Use this file to justify a decision or to resolve a conflict between rules.
It is not a screen recipe. Evidence tags: `[V: source]` = supporting text was
read; `(summary)` = from secondary summaries, check the primary before quoting;
`(verify)` = unconfirmed number or attribution, do not quote as a requirement.

## Contents

1. How to use this file
2. Standards map (table)
3. Reading standards correctly (hard numbers worth knowing)
4. Situation awareness
5. Skill-rule-knowledge and ecological interface design
6. Norman: gulfs, signifiers, mapping, feedback, constraints, modes
7. Reason: error types, Swiss cheese, error-control hierarchy
8. Automation, trust and AI output
9. Workload and attention
10. Teleoperation
11. When rules conflict
12. Sources

## 1. How to use this file

- Rules say what to do; this file says why, so edge cases can be judged.
- When a standard and a convention disagree, the order of authority is: law and
  safety standards, then the site/product style guide, then published
  guidelines, then taste. Record the choice and the reason.
- Treat paywalled standards as leads unless you hold the licensed text. Few
  give a finished screen: run the process, document decisions, apply hard rules
  to physical devices and safety, justify the rest by testing with operators.

## 2. Standards map

| Standard | Purpose | Consult when | Access |
|---|---|---|---|
| ANSI/ISA-101.01-2015 | Lifecycle for process HMIs: philosophy, style guide, toolkit documents; display levels 1-4; change management. Colour rules are site convention, not normative. | Setting up a design process or an audit trail; naming display levels | Paywalled; TOC and vendor summaries free |
| ISA-18.2-2016 / IEC 62682:2014 | Alarm management lifecycle: philosophy, rationalisation, KPIs, shelving | Any alert or alarm design; defining what is an alarm | Paywalled |
| EEMUA 191 (4th ed., 2024) | Alarm-system benchmarks: loads, priority split, deadbands | Sizing alarm load, priority distribution | Paywalled; HSE sheet CHIS6 free |
| ISO 9241-110:2020 | Seven interaction principles (task suitability, self-descriptiveness, expectation conformity, learnability, controllability, use-error robustness, user engagement) | Design reviews as a checklist [V: free ISO preview] | Paywalled; preview free |
| ISO 9241-112 (2nd ed., 2025) | Presenting information (visual, auditory, tactile) | Detectability, discriminability, consistency of presentation (principle list: verify) | Paywalled |
| ISO 9241-11:2018 | Usability = effectiveness, efficiency, satisfaction in a specified context of use [V: quoted in the -110 preview] | Writing measurable acceptance criteria | Paywalled |
| ISO 9241-210:2019 | Human-centred design process (understand context, specify requirements, design, evaluate; iterate) | Planning user involvement and evaluation | Paywalled |
| ISO 11064 (parts 1-7) | Ergonomic design of control centres: layout, workstations, displays, environment | Fixed control rooms; background for a single station | Paywalled |
| IEC 60073 / 61310 / 60447 | Colour, signal and actuation coding for machine indicators and actuators; actuating directions | Physical buttons, lamps, tower lights; keep screen colours consistent with them | Paywalled |
| IEC 60204-1:2016 (+A1:2021) | Electrical equipment of machines: button colours, stop categories 0/1/2, e-stop reset rule | Any machine with physical controls | Paywalled; sources conflict on preferred START colour (white vs green), check licensed text |
| ISO 13850:2015 | Emergency stop function: latching, manual reset that only permits restart, available in all modes | Anything that touches stopping | Paywalled |
| ISO 12100 / ISO 13849-1 / IEC 62061 | Risk assessment; performance levels and SIL for safety functions | Deciding whether a screen may take part in a safety function | Paywalled |
| NUREG-0700 Rev 4 (Jan 2026) | Numbered HSI review guidelines: displays, alarms, soft controls, automation, workstations [V: nrc.gov PDF] | Looking for a defensible number or checklist (colour delta E, flash rates, touch size) | Free |
| MIL-STD-1472H (2020) | Human engineering numbers: touch size, character height, flash, colour meanings [V: OCR text] | Same; touch and glove allowances | Free |
| FAA HFDS (2003) | Free digest citing MIL-STD-1472 with rationale | Reading the rationale behind a number; older-edition values | Free |
| ANSI/HFES 100 (2007; 2026 draft) | Office workstation ergonomics; draft gives 9 mm soft keys, 3.2 mm dead space [V] | Floor values for bare-finger desk use only | Paywalled; draft free |
| IEC 62366-1:2015+A1:2020 and FDA human factors guidance (2016) | Usability engineering: use-related risk, critical tasks, formative then summative testing | Transferable validation model for any high-consequence HMI | IEC paywalled; FDA free |
| IEC 62443 (esp. 3-3) | Industrial cybersecurity: authentication, roles, audit on every interface including the HMI (summary) | Login, roles, audit logs, shared accounts | Paywalled |
| Regulation (EU) 2023/1230 | Machinery law, applies from 20 Jan 2027 (summary; EUR-Lex not read): ergonomics, control-system safety, protection against corruption, autonomy | Machines placed on the EU market | Free (law) |
| EU AI Act Art. 14 | Human oversight of high-risk AI: understand limits, stay aware of automation bias, override, stop [V: artificialintelligenceact.eu] | Any model output that drives operator decisions | Free |
| WCAG 2.2 | 4.5:1 text contrast, 3:1 large text and UI; 24 px minimum target (AA) | Web-technology HMIs; accessibility floor | Free |

## 3. Reading standards correctly

Verified numbers (primary text read) that settle common disputes:

- Touch target: MIL-STD-1472H 15-38 mm square, separation 3-6 mm, add 5 mm per
  dimension for gloves, force 0.25-1.5 N [V: 5.1.3.1.17]. NUREG-0700 Rev 4
  10-40 mm [V: 11.3.2.3.6-2]. Office floor 9 mm [V: HFES 100-2026 draft]. The
  older 19 mm figure belonged to 1472D.
- Latency: feedback within 100 ms; message if over 1 s; progress if over 10 s
  [V: MIL-STD-1472H 5.1.3.1.4, 5.17.9.5.3; Nielsen thresholds].
- Colour sets: members differ by at least 40 delta E, giving about 7-10
  simultaneous colours [V: NUREG-0700 Rev 4 1.3.8-7].
- Flash: urgent items only; at most two rates, at least 2 Hz apart, between
  0.8 and 5 Hz, 50% duty [V: MIL-STD-1472H 5.17.27; NUREG-0700 1.3.10-12].
  Emergency flash 3-5 Hz. A failed flasher must stay lit [V: FAA HFDS 6.2.2.1.28].
- Alarm load: long-term average at most 1 per 10 min; at most 10 in the first
  10 min after a major upset; priorities about 5/15/80 percent [V: HSE CHIS6
  citing EEMUA 191]. A flood starts above 10 alarms in 10 min (common
  definition; ISA-18.2 text not read).

## 4. Situation awareness (Endsley)

Definition [V: Endsley 1995, via bibliographic records]: perception of elements
in a volume of time and space, comprehension of their meaning, projection of
their status. Design for all three levels:

- Level 1, perceive: is the item shown, legible and not masked? Most
  situation-awareness errors in aviation were Level 1 (commonly cited 76/20/4
  split; the exact split is (verify)). Fix perception before sophistication.
- Level 2, comprehend: show meaning, not raw data. Value with unit, limit,
  normal band, comparison with expected.
- Level 3, project: trend, rate, time to limit, what happens if nothing is done.

SA demons (Endsley and Jones 2012): attentional tunnelling; requisite memory
trap; stress, fatigue and workload; data overload; misplaced salience;
complexity creep; errant mental models; out-of-the-loop syndrome.

Derived rules:
- Keep a permanent overview whose silence is informative; never replace it with
  a modal screen during operation.
- For each key value show current value, acceptable band, trend, and time to
  limit when a limit exists.
- Show derived decision quantities (remaining length, minutes of margin) rather
  than only raw channels.
- Show age and validity of every live value: fresh, stale, lost, estimated,
  conflicting.
- Never require remembering a value from another screen.
- Spend salience (flash, sound, saturated colour) only on importance; count
  simultaneous attention-grabbers and keep the count very small.
- Show the mode and what the machine will do next, not only its state.

## 5. Skill-rule-knowledge and ecological interface design

Rasmussen (1983): behaviour is skill-based (automatic, sensorimotor), rule-based
(if state X, do Y) or knowledge-based (novel reasoning). Errors: slips, misapplied
rules, and mistakes from wrong models; knowledge-based work is slowest and most
error-prone.

Ecological interface design (Vicente and Rasmussen 1992) applies this: let the
operator act directly on a display that mirrors the controlled item (skill);
give a consistent one-to-one mapping from domain constraints to cues (rule); and
expose goals, functions and constraints via an abstraction hierarchy so the
operator can reason (knowledge). Effect sizes in the classic microworld studies
are (verify); cite direction only.

Derived rules:
- Classify each task before designing it. Skill tasks get fixed positions,
  direct controls and no menu depth. Rule tasks get unambiguous cues tied to the
  rule. Knowledge tasks get an explanatory and diagnostic view.
- Draw limits, forbidden zones and constraints on the display so operators see
  boundaries, not only position.

## 6. Norman: gulfs, signifiers, mapping, feedback, constraints, modes

- Gulf of execution: gap between intent and available actions. Bridge it with
  signifiers (visible cues of what is pressable and where), mapping and
  constraints. Flat styling that removes the look of a button widens the gulf.
- Gulf of evaluation: gap between system state and what the user can perceive
  and interpret. Bridge with feedback and a truthful system image.
- Designer's model, user's model, system image: operators learn only from what
  the interface shows. If it does not convey the real model, wrong ones form,
  and wrong models are sticky.
- Mapping: control layout and direction should match the effect (push-forward
  moves forward; on-screen direction matches the video frame of reference).
- Feedback: every action gets an immediate, informative response; no feedback
  leads to repeated presses and double actions.
- Constraints: physical, logical, semantic limits that make wrong actions
  impossible or visibly unavailable.
- Mode errors: an action right for the believed mode, wrong for the real one.
  Same control meaning different things in different modes is the trigger.

Derived rules:
- Every control shows a pressable look, a pressed or busy state within 100 ms,
  and the real outcome as soon as it is known (acknowledged vs done).
- Say why an action is unavailable ("Locked: head is moving"), not just grey it.
- Use the operators' domain words; never firmware identifiers.
- Distinct modes (live, frozen, replay, test, manual, automatic) look different
  everywhere, not only in one label; keep the mode near the point of action.

## 7. Reason: error types, Swiss cheese, error-control hierarchy

Types (Reason 1990): slips (right intention, wrong execution), lapses (omitted
step), mistakes (wrong intention: rule-based or knowledge-based), violations
(deliberate deviations; routine ones are often caused by designs that make the
safe path slow). Latent conditions (design, scheduling, training) precede the
active failure. Swiss-cheese model: each defence (alarm, confirmation,
interlock, procedure, training) has holes; accidents happen when they align. A
bad HMI opens holes in several layers at once. Treat error as a consequence of
design, not a cause (Dekker).

Order of controls, strongest first (Norman; Reason; hierarchy of controls):
1. eliminate the hazardous function from the screen;
2. prevent by interlock, sequence enforcement, physical key;
3. make it hard (spacing, guards, hold-to-confirm, separate dangerous from
   frequent controls);
4. make it visible (preview of effect, immediate feedback);
5. make it reversible (undo, return to previous setting);
6. make it recoverable (safe state, clear recovery path);
7. warn, train, write a procedure (weakest).

Confirmation facts: click-through of browser warnings varied from about 10% to
70% depending on design [V: Akhawe and Felt 2013]; clinicians override 49-96% of
drug alerts, mostly because specificity is low [V: van der Sijs 2006]. So
habituation is design-dependent, not inevitable.

Derived rules:
- Document the control tier used for each hazardous function.
- Undo for reversible actions; confirmation only for irreversible, costly ones;
  never both for trivial ones.
- A confirmation names the consequence and scope, uses verb button labels, has
  a safe default, and for the highest risk uses a gesture that cannot be done on
  reflex (hold, type the name, physical key, second person).
- Never use confirmation to compensate for a missing interlock.
- Log confirmation acceptance in the field; near-100% instant acceptance means
  the dialog is not working.
- If the safe procedure is slow, expect routine violations: fix the design.

## 8. Automation, trust and AI output

Bainbridge, "Ironies of Automation" [V: Automatica 19(6) 775-779]:
- Designers automate because humans are unreliable, then leave the human the
  hardest cases.
- Skills decay without practice, yet takeover needs more skill, at the worst
  moment, with degraded contact with the process.
- Humans cannot sustain effective attention on a source where little happens
  beyond about half an hour (citing Mackworth); alarms must do the monitoring,
  and those need an operator who understands the process.
- Training and simulators only cover faults the designer already imagined.

Levels of automation (Sheridan and Verplank 1978, 10 levels; Parasuraman,
Sheridan and Wickens 2000): apply levels separately to acquisition, analysis,
decision selection and action. Higher automation is easier to justify for
acquisition and analysis than for decisions and irreversible actions, and where
reliability is high and consequence low. (Four classes confirmed from secondary
summaries only.)

Complacency and bias: complacency is under-monitoring because automation seems
reliable; automation bias is using its cue in place of vigilant checking, giving
omission and commission errors (Parasuraman and Manzey 2010; Skitka et al.).
Training alone does not cure it.

Mode awareness: Sarter and Woods's three questions: what is it doing, why, what
will it do next. Surprises come from automatic mode changes, one control with
several meanings, and displays that show commanded rather than actual state.

Transparency: show what the agent is doing and why, and what it projects and how
uncertain it is (Chen et al. SAT model). Trust calibration (Lee and See 2004):
trust should match capability; overtrust gives misuse, undertrust gives disuse;
make performance, process and purpose observable, including when the system is
not competent. The "70% reliability crossover" is (verify; second-hand).

AI output: explanations did not reduce overreliance and could raise acceptance
of wrong advice [V: Bansal et al. 2021]; cognitive forcing designs cut
overreliance but were rated least favourably [V: Bucinca et al. 2021]. Amershi et
al. (CHI 2019, 18 guidelines [V: count]): make clear what the system can do and
how well; show why; support efficient dismissal, correction and global controls.
EU AI Act Art. 14(4) [V]: overseers must understand limits, monitor anomalies,
stay aware of automation bias, interpret output, disregard or reverse it, and
stop it. Awareness text in a manual is not an HMI control; the screen itself
must carry the mitigations.

Derived rules:
- Write down the automation level per function; default high for acquisition and
  analysis, human decision for irreversible acts.
- Always display what automation is doing, why, what next, and how to override
  or stop it. Show degraded, out-of-domain and handed-back states.
- Keep the operator active; passive monitoring is never the only safety layer.
- Takeover requests: early, reasoned, with a time budget, with explicit "you
  have control / system has control" confirmation, and a "what happened" summary.
- Show redundant-sensor disagreement and which source is in use; never silently
  choose one.
- Machine-generated content is labelled, shows the evidence beside it, uses a
  few categorical confidence levels, is correctable in one gesture, and the
  correction is logged. The corrective path is never longer than accepting.
- Do not anchor on the recommendation for high-stakes items; offer it after the
  human's own assessment where feasible.

## 9. Workload and attention

- Multiple resources (Wickens 2002): conflicts rise when tasks share a stage,
  modality, channel or code. Eyes on video: put a critical alert in sound or
  touch as well. Spatial control interferes with spatial displays.
- SEEV: attention follows salience, expectancy, value and low effort. Place
  high-value, frequently changing items where looking is cheap.
- Change blindness: changes coinciding with a transient (page switch, redraw,
  flicker) go unseen. Use persistent change flags and event logs; do not redraw
  whole screens.
- Inattentional blindness: unexpected rare events are missed when attention is
  elsewhere (about half missed the gorilla in Simons and Chabris). Rare critical
  events need salient multimodal cues.
- Vigilance decrement: detection of rare signals drops after roughly 15-30 min;
  monitoring is hard work, not just boring.
- Tunnelling and stress: narrow attention; familiar responses win. Emergency
  screens must work "with a pounding heart".
- Hick-Hyman: choice time rises with log2(alternatives); about 5-7 grouped
  choices; broad-shallow beats narrow-deep.
- Fitts: time rises with distance and falls with target size; touch has no
  infinite edge targets. Frequent actions large and near the resting hand,
  destructive ones separated.
- Colour vision deficiency: about 8% of men, 0.4-0.5% of women (Birch 2012).
Derived rules:
- Cut extraneous load: nothing on the main screen that does not support a
  current decision.
- Response budget: under 100 ms feedback, busy cue past 1 s, progress with
  cancel past 10 s.
- Code nothing in colour alone; about 5-7 categories at most.
- Targets: at least about 9-10 mm in general; 15 mm or more for primary field
  controls; gloves add 5 mm; spacing at least 3-4 mm.

## 10. Teleoperation

Evidence from ARL-TR-3834 (2006, precursor of Chen, Haas and Barnes 2007)
Evidence [V: read]: latency detectable at 10-20 ms in virtual environments; simulated
driving degraded at 170 ms; operators begin decoupling commands from responses
near 300 ms; move-and-wait behaviour above about 1 s; jitter (standard
deviation above about 82 ms) can hurt more than a longer constant delay;
video at 8-10 Hz is the evidence floor for indirect driving (more is an
engineering margin). Restricted field of view degrades self-location and depth
perception (the "keyhole" effect). A frozen last frame looks like a valid image.

Derived rules:
- Measure and show control-loop latency, frame age and link quality; scale
  permitted speed to latency; stop on a stale link and say so.
- Make frozen video unmistakable (overlay, frame-age counter) and halt or limit
  motion; warn below roughly 8-10 fps.
- Keep a persistent cluster of vehicle-state facts (pose, position along the
  path, load, tension, power) near the video, plus an overview map or linear
  schematic with event markers. Provide egocentric and exocentric views, linked.
- Keep drive and camera frames consistent; warn or remap; label rear views.
- Separate drive quality (low latency) from inspect quality (high resolution).
- Announce autonomous interventions with the reason and make them overridable.
- Define link-loss behaviour; tell the operator before and after it happens.

## 11. When rules conflict

Default order: safety > situation awareness > operator efficiency > consistency
with convention > aesthetics. Resolve a conflict by moving up that list, then
record the decision in the style guide.

| Conflict | Resolution |
|---|---|
| Safety vs convenience (fewer taps) | Safety wins; move the hazardous act off the screen or add prevention, not another dialog |
| SA vs decluttering | Remove only what no decision uses; keep overview, mode and fault status always visible |
| Blink rate vs photosensitivity | Flash only urgent items, 0.8-5 Hz as the coding limit; avoid 1-30 Hz flicker over large areas [V: MIL-STD-1472H 5.12.1.4.2] and keep flashing elements small; WCAG's three-flashes-per-second limit is the web floor (verify); prefer static change of shape or colour plus sound; never make the entire screen flash |
| Colour minimalism vs recognisability | Grey normal, colour only for abnormal (ISA-101 practice), but never at the cost of recognition: add shape, text and position; colour-blind safe pairs |
| ISA-101 grey/green-avoidance vs machine convention (green = normal) | Keep screen colours separate from physical-device meanings; never make an on-screen control resemble the red-on-yellow emergency stop |
| Many confirmations vs habituation | Fewer, consequence-specific ones; prefer undo; hold gestures for the severe |
| Transparency vs workload | Show one line of reason by default; detail on demand; never hide authority or mode |
| Automation convenience vs skill retention | Keep manual practice paths and meaningful operator decisions |
| Localisation vs fixed layout | Fixed-size controls, wrapping labels, test the longest language; never shrink or truncate machine commands |
| Standards disagree (numbers) | Use the stricter or larger value for the environment; cite the clause and edition |

Tie-breaker: prefer reversible over irreversible, visible failure over quiet
failure, and measured field behaviour over opinion.

## 12. Sources

- Endsley 1995, Human Factors 37(1); Endsley, Bolte and Jones 2003; Endsley and
  Jones 2012.
- Rasmussen 1983; Vicente and Rasmussen 1992; Norman 2013, The Design of Everyday Things; Hutchins, Hollan and Norman 1985.
- Reason 1990 and 2000 (BMJ 320); Dekker, Field Guide to Understanding "Human Error".
- Akhawe and Felt 2013, USENIX Security; van der Sijs et al. 2006, JAMIA 13(2).
- Bainbridge 1983, Automatica 19(6); Parasuraman, Sheridan and Wickens 2000;
  Parasuraman and Manzey 2010; Sarter and Woods 1995; Lee and See 2004;
  Chen et al. SAT model; Wickens and Dixon 2007.
- Bansal et al. 2021 (arXiv 2006.14779); Bucinca, Malaya and Gajos 2021 (arXiv
  2102.09692); Amershi et al. 2019 (CHI); Laux and Ruschemeier 2025 (arXiv 2502.10036).
- Wickens 2002; Simons and Chabris 1999; Cowan 2001; Nielsen response-time limits;
  MacKenzie 1992. Chen, Haas, Pillalamarri and Jacobson 2006, ARL-TR-3834 (govinfo.gov).
- Standards: NUREG-0700 Rev 4 (nrc.gov, ML26022A094); MIL-STD-1472H
  (everyspec.com); ISO 9241-110:2020 free preview; BSR/HFES 100-2026 draft;
  FAA HFDS Ch. 5, 6, 9; HSE CHIS6 (hse.gov.uk/pubns/chis6.pdf); EU AI Act Art. 14.
