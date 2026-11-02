# Alarms, alerts, warnings and events

Reference for designing and reviewing the alarm side of an operator HMI. Domain-neutral: machine, robot, process or field equipment.

Number tags: `[V: source, page]` = supporting text was read. `(summary)` = from secondary sources (trade article, vendor, manufacturer manual); cite the standard, not this file. `(verify)` = unresolved or from memory; never present it as a requirement. Paywalled standards (ISA-18.2, IEC 62682, EEMUA 191, IEC 60601-1-8) were not read in normative text.

## Contents

1. Vocabulary
2. Lifecycle
3. Prioritisation
4. Alarm states
5. Latching, first-out, acknowledge vs silence
6. Banner, summary, in-context, sorting
7. Shelving and suppression
8. Floods, rates, chattering, deadband, delays
9. Audible design and the flash conflict
10. Message content
11. Comms-loss and device-offline alarms
12. Audit trail
13. Cross-domain lessons
14. Case lessons
15. Alarm philosophy outline
16. Common mistakes
17. Sources

## 1. Vocabulary

Use these six words with these meanings, everywhere in the UI, code and docs. Most floods start by calling everything an alarm.

| Term | Meaning | Operator must act? | Example |
|---|---|---|---|
| Alarm | Abnormal condition that needs a timely operator response; ignoring it has a defined consequence | Yes, within a defined time | Tank level high-high, cable tension out of range |
| Alert / warning | Needs attention but no mandated response time | Maybe, later | Filter due in 3 days |
| Event | Recorded occurrence, logged, not annunciated | No | "Pump 2 started", setpoint changed |
| Prompt | Request inside normal workflow | Yes, but not abnormal | "Insert next cassette" |
| Status | Continuous display of state | No | Run/Stop indicator |
| Trip / interlock | Automatic protective action; the alarm only reports it | No, already acted | "Emergency stop activated" |

**Rule: an alarm requires a defined operator action within a defined time.** If no action is possible, or none is needed within a time you can state, it is not an alarm; make it an event, status or message. An "alarm" whose only response is "press OK" is an event. (summary: ISA-18.2 / IEC 62682 sense)

Word usage: "Alarm" only for items that pass the rule. "Warning" is acceptable for the middle tier only if the philosophy says so (aviation uses warning/caution/advisory, see section 13). Pick one set and define it once.

## 2. Lifecycle (ISA-18.2 / IEC 62682)

Alarm design is a continuous process, not a screen task. ISA-18.2 first issued 2009, revised 2016; IEC 62682 is the international adoption, first 2014, with a newer edition 2023 per the release note (summary; the EEMUA release note names the 2023 edition). EEMUA 191 is on its 4th edition, published November 2024 [V: operationsengineer.org.uk release note, EEMUA contents PDF]; the benchmarks below are the long-standing ones from earlier editions, not re-checked against the 4th. Stage names A to J follow a Yokogawa/Control Engineering summary (stages E to J verified; A to D from general knowledge).

| Stage | What happens |
|---|---|
| A Philosophy | Write the product alarm philosophy (section 15) |
| B Identification | Collect candidate alarms from hazard analysis, incidents, field experience |
| C Rationalization | Justify each candidate; set limit, priority, consequence, action, response time; delete those that fail the section 1 rule |
| D Detailed design | Presentation, deadband, delays, suppression, guidance text |
| E Implementation | Configure, test, train |
| F Operation | Operators respond; ack, shelve |
| G Maintenance | Test alarms and instruments; out-of-service handling |
| H Monitoring | Measure rates, floods, standing, bad actors; feed back to C and A |
| I Management of change | No alarm added, changed or deleted without authorisation |
| J Audit | Compare running configuration to the master alarm database |

HMI implication: the screen must expose the data the process needs (logs, counts, shelved list, config version). Keep a master alarm database (one row per alarm: id, type, limit, priority, class, consequence, cause, action, response time, deadband, delays, suppression conditions, shelving allowed).

Machine builders: ISA-TR18.2.6 (batch and discrete processes) and ISA-TR18.2.7 (packaged systems) are the closest technical reports [V: isa.org InTech 2019, ANSI webstore]. TR8 title not found (verify).

## 3. Prioritisation

Priority = consequence of not responding x time available to respond. It is not the importance of the equipment.

Default matrix (template; the band edges are a product decision, document them):

| Time to respond \ Consequence | Minor | Major | Severe (injury, large loss) |
|---|---|---|---|
| > 30 min | Not an alarm (alert) | Low | Medium |
| 10 to 30 min | Low | Medium | High |
| < 10 min | Medium | High | High |

Rules:
- Use 3 priorities. A 4th is allowed only as "journal" (logged, not annunciated) or as an immediate-safety top tier. HSE says "use about three priorities" [V: HSE CHIS6 p.2]. More levels than 4 are not reliably told apart.
- Target distribution of configured alarms about 5 % high / 15 % medium / 80 % low [V: HSE CHIS6 p.2, citing EEMUA p.65]. Whether it applies to definitions or to activations is not settled (verify). Use it as a sanity check: a product where most alarms are top priority has no priority scheme (own inference, verify).
- Reserve the top priority. If a top-priority alarm is routinely active it will be ignored.
- Safety-class alarms get extra rigour: periodic test, no shelving without approval.
- Priority is shown redundantly: colour + shape or number + list position. Colour-vision deficiency affects about 8 % of men and about 0.4 to 0.5 % of women [V: README, Birch 2012; 04 file], so never colour alone.

Colour, shape and sound exclusive to alarm priorities:
- Colours used for alarm priority are reserved for alarms. Do not reuse red for a Stop label, a closed valve, a brand accent or a decoration; do not use amber for "selected". (ISA-101 and ASM guidance, secondary.)
- Same for shapes (e.g. triangle and octagon icons) and for sounds: no tone that sounds like an alarm tone may be used for button feedback or notifications.
- Default scheme: red = high, amber/yellow = medium, cyan or white = low, magenta = diagnostics/bad data (vendor practice, summary). Red high and yellow medium match IEC 60601-1-8 and aviation. Low priority colour varies by domain (cyan or yellow in medical); consistency inside the product and with the domain standard matters more than the exact hue.
- Keep the normal state quiet: grey or neutral, nothing flashing at rest. Any colour on screen then means something.
- Colours coded together must be well separated: NUREG-0700 Rev 4 asks at least 40 delta E (CIE 1976 L*u*v*) between colours in a coding set, giving about 7 to 10 simultaneous colours [V: NUREG-0700 Rev 4 1.3.8-7, p. 1-51]. Use 3 to 4.

## 4. Alarm states

Every alarm is in exactly one state, and each state must look different without relying on colour alone. (State model: ISA-18.2, summary.)

| State | Meaning | How it must look and sound |
|---|---|---|
| Normal | Inactive, acknowledged | No indication |
| Active, unacknowledged | Condition present, operator not yet aware | Priority colour + icon + text; attention cue (slow flash of a marker symbol or a highlighted row); audible per priority |
| Active, acknowledged | Condition present, operator aware | Same colour and icon, steady, no flash, audible stopped; stays in the list |
| Returned to normal, unacknowledged | Cleared before the operator saw it | Distinct mark (hollow icon or "cleared" tag), no loud audible; stays until acknowledged so the event is not lost |
| Shelved | Operator hid one alarm temporarily | Out of the main list; counted and listed in a Shelved view with reason, who, expiry |
| Suppressed by design | Logic hides it because the equipment state makes it meaningless | Out of the main list; counted and listed in a Suppressed view with the suppression condition |
| Out of service | Removed for maintenance under a work order | Listed with approver and work reference; the affected equipment shows a persistent "out of service" tag on its graphic |

Rules:
- Flash only what needs attention now, i.e. unacknowledged. Flashing acknowledged alarms is noise. Flash a marker symbol, not the text (NUREG-0700 Rev 4 1.3.10-10 [V: p. 1-55]).
- Hidden is never invisible: shelved, suppressed and out-of-service counts are always on screen.
- A failed flasher must stay lit steadily, not go dark [V: FAA HFDS 6.2.1.1.6, ch. 6].

## 5. Latching, first-out, acknowledge vs silence

- Latching: an alarm stays active after the condition clears until reset. Use it for trips and events whose evidence would otherwise vanish. Process deviations that recover are non-latching.
- Reset is separate from acknowledge and is possible only when the condition is clear. Resetting a stop must permit a restart, never cause one.
- Acknowledge = "I am aware"; it changes state. Silence = stops the sound only; it changes nothing else. Provide both. Silence is time-limited and its state is visible (medical practice: pause up to about 2 min, indicator visible) (summary, section 9).
- Acknowledge per alarm or per visible page. No "acknowledge all" over alarms the operator has not seen (summary: widely recommended, banned at some sites, so treat as a hard default).
- Re-annunciate an unacknowledged high-priority alarm after a stated interval; the interval is a philosophy decision (verify, no sourced value).
- Record who acknowledged, when, and from where (section 12).
- First-out: on a trip many alarms follow a root cause within seconds. Mark the first one by source-device timestamp (ms resolution, from the controller, not HMI arrival time) with a "first-out" marker, and keep a sequence-of-events record for analysis (summary).

## 6. Banner, summary, in-context, sorting

| Surface | Job | Rules |
|---|---|---|
| Banner (fixed strip) | Always shows the newest or highest-priority active alarms, 1 to 3 lines, plus counts per priority and counts of shelved/suppressed | Fixed place, never covered by pop-ups, one tap goes to detail |
| Summary (list) | All active alarms | Columns: time, equipment, description, value, limit, priority, state, time since onset. Filters by area and priority |
| In-context indication | Icon on the process graphic beside the equipment | Same colour and shape as the list; tap goes to the alarm |
| Shelved / suppressed / out-of-service lists | What is hidden right now | Reason, who, when, expiry |
| History / log | All alarm transitions and operator actions | Append-only, searchable (section 12) |

Sorting: default priority first, then time (pick newest-first or oldest-first once and keep it). Offer time-only and by-area views. Banner text names the condition ("Tank 3 level high"), not the tag ("LAH-0302").

Alarms never use modal pop-ups: a modal blocks the screen needed to fix the problem. Reserve modals for irreversible confirmations (summary: ISA-101/ASM guidance).

## 7. Shelving and suppression

Shelving = operator-initiated, temporary hiding of one alarm.
- Requires a reason (pick list plus optional text) and a maximum duration; it auto-unshelves at expiry. A default of one shift or less is common practice; sourced values do not exist (verify), so choose and document one.
- Access controlled by priority and role. Top-priority and safety alarms: not shelvable, or supervisor approval.
- Visible shelved list and count on the main screen; reviewed at handover.
- Logged: shelve, unshelve, reason, who. Events continue to be recorded while shelved.
- Shelving counts per alarm are a monitoring signal: a frequently shelved alarm needs rationalising.
- Different from out-of-service (maintenance, work order, long) and suppression by design (automatic).

Suppression types (design them in rationalization, not ad hoc in code):

| Type | Example |
|---|---|
| State-based | Pump stopped: no low-pressure alarm; start-up: hold alarms until stable |
| Cascade / consequential | Power lost: suppress every "motor not running" |
| Flood | During a flood show only high and medium priority |
| Mode-based | Equipment in maintenance mode is muted, with expiry |

Rules: suppression is visible (count and list), logged, and fail-safe (if the suppressing logic fails, alarms reappear). Instrument-bad-quality: raise one diagnostic alarm and mark or suppress derived process alarms.

## 8. Floods, rates, chattering, deadband, delays

Numbers and status:

| Item | Value | Status |
|---|---|---|
| Steady-state target | Long-term average at most 1 alarm per 10 min per operator (about 150 per day by arithmetic) | [V: HSE CHIS6 p.1, citing EEMUA p.37; Honeywell/ASM deck slide 18] |
| Manageable maximum | Up to about 2 per 10 min (12 per hour) | (summary: chemengonline.com trade article) |
| Upset target | At most 10 alarms displayed in the first 10 min after a major upset | [V: HSE CHIS6 p.1] |
| Flood start | More than 10 alarms in 10 min | (summary: ISA-18.2 / EEMUA, several secondary sources) |
| Flood end | Fewer than 5 new alarms in a 10 min interval | (summary: one trade article attributing to EEMUA 191) |
| Time in flood | Less than 1 % of time | (verify: not found in a source) |
| Standing (stale) alarm | Active more than 24 h; target fewer than 10 standing at once | stale: (summary, study guide); target: (verify) |
| Top-10 bad actors | If the top ten sources produce over 20 % of alarms, suspect nuisance alarms | (summary: trade article); the older "<1 % / <5 %" figures are (verify), do not use |
| Rate bands "over-demanding" above 2 or 5 per 10 min, "unacceptable" above 10 | Sources disagree on edges | (verify) |

Use the table values as monitoring targets for the product, not as certified requirements. Rate per operator per 10 min is the unit; compute it from the log monthly.

Milford Haven (1994): 275 alarms in the last 11 minutes before the explosion, for two operators [V: HSE CHIS6 p.1].

Chattering and nuisance:
- Chatter = a signal toggling around a limit. Practical test: 3 or more activations in 1 min (verify: definitions differ, one source says more than 2 per second). Detect it, auto-shelve or latch with a flag, and fix the cause.
- Fleeting = activates and clears quickly. Nuisance = annunciates excessively or does not clear after the right response.

Deadband (hysteresis), apply first. Alarm clears only after the value moves back past the limit by a margin, as percent of range:

| Signal | Deadband | Status |
|---|---|---|
| Flow | 5 % | (summary: exida vendor blog labelled "EEMUA 191 recommended") |
| Temperature | 1 % | same |
| Pressure | 2 % | same |
| Composition | 1 % | same |
| Level | 2 % or 5 % | UNRESOLVED: exida gives 2 %; Naghoosi et al., ACC 2011, Table 1 p.3627 gives 5 %. Default to 5 % for a first design and tune from the log (verify) |

On-delay (alarm only after the condition persists T) and off-delay (alarm clears only after stable normal T): no sourced default table exists. Do not copy "flow 5 to 30 s, pressure 1 to 15 s" figures seen elsewhere (verify, unsupported). The method that is sourced: use an on-delay when the operator action is not needed every time the limit is touched, set it to about the time a normal transient takes to clear (example in the source: 1 min for a filter alarm), and apply deadband first, delays second [V: Emerson blog, Cahill 2010]. Measure the transient in the real machine and write the number into the rationalization row. Other techniques: filtering noisy signals, rate-of-change alarms for early warning, and placing the limit early enough that the operator has the allowed response time.

## 9. Audible design

- One distinct sound per priority, at most 3 to 4 sounds, none used for anything else. Faster repetition, higher pitch and more pulses = more urgent (Edworthy research, summary).
- Loud enough to be heard over ambient noise; a common rule is about 15 dB above masked threshold (verify). Provide a volume setting with a safe minimum, and an audible test at start-up and on demand.
- Silence is time-limited and its state is visible; "alarm off" is a separate, deliberate, logged setting.
- Voice only for very few cases: slow, language-dependent. Aviation uses it for terrain and stall warnings.
- Use sound for what the eyes cannot cover (eyes on video or on the work); keep tones non-startling.
- Gate by operating phase where it helps (inhibit non-critical sounds during a critical manoeuvre), visibly and logged; see aviation inhibits in section 13.

IEC 60601-1-8 (medical alarm systems) as a transferable reference. The standard was not read; sources are a manufacturer manual, a patent summary, a clause-excerpt site and vendor articles.

| Priority | Visual | Audible burst |
|---|---|---|
| High | Red flashing 1.4 to 2.8 Hz, duty cycle 20 to 60 % | 10-pulse burst (two groups of 5), fast pulses |
| Medium | Yellow flashing 0.4 to 0.8 Hz, duty cycle 20 to 60 % | 3 pulses, slower |
| Low | Cyan steady, 100 % on (manual); yellow option (verify) | 1 or 2 pulses, slowest |

Status: flash rates and duty cycle come only from a manufacturer's operator manual (Mindray BeneVision N, PDF p.5), not the standard (summary). Pulse counts per priority are (summary: patent summary, clause excerpt site). Inter-pulse pause, burst repeat interval and the 2020 amendment changes are not obtained (verify). Pulse duration figures from a vendor article (high 25 to 75 ms, medium 90 to 200 ms, low 400 to 600 ms) are (verify) for design use. Pulse fundamental 150 to 1000 Hz and envelope rise/fall 7.5 to 100 ms are (summary: TI application note SSZT261 p.1-2). The transferable ideas: pulse count signals urgency, and a pause is time-limited, never indefinite.

The flash conflict (photosensitivity vs alarm flash). Sources disagree and the conflict is real:
- Alarm flash guidance: emergency flash 3 to 5 Hz at 50 % duty; at most two flash rates, at least 2 Hz apart, slow not under 0.8 Hz, fast not over 5 Hz; flash only for urgent items [V: MIL-STD-1472H 5.7.3.5.1, 5.17.27; NUREG-0700 Rev 4 1.3.10-12, p. 1-55].
- Photosensitive risk: MIL-STD-1472H 5.12.1.4.2 says avoid flicker or bright pulsing in the 1 to 30 Hz range [V]; FAA HFDS cites seizure risk between 10 and 25 Hz, peak 15 to 20 Hz (older edition). A 3 to 5 Hz flash sits inside the 1 to 30 Hz avoid band of the same standard.
- Medical standard flash is 0.4 to 2.8 Hz, below the 3 Hz level commonly used in web accessibility rules (WCAG 2.3.1 "no more than three flashes per second", not read here, verify).
- Default resolution: do not flash large areas. Flash a small marker symbol only, at or below about 2 Hz, with a 50 % duty cycle, limited to unacknowledged high-priority alarms; stop flashing on acknowledge; carry urgency through position, shape, sound and a steady colour. Provide a "no flash" setting where policy allows, because high-performance HMI guidance recommends minimising flashing entirely (summary). Run a review against the local accessibility and safety rules before shipping a flash.

## 10. Message content

An alarm message answers four questions: what happened, what it means (consequence), what to do, where. Codes sit behind a "technical details" fold. Headline under about 8 words.

| Element | Rule |
|---|---|
| What happened | Condition in operator words: "Cable tension too low", not "Err 0x4F12" |
| Where | Unit, axis or channel |
| Value and limit | "78 C, limit 75 C" |
| Consequence | What the machine did or will do: "Motion stopped" |
| What to do | 1 to 3 imperative steps: "Check cable; press Reset when clear" |
| Time to respond | "within 10 min" for alarms that have one |
| Code, timestamp | Small, copyable, stable across versions, unique, never renumbered |
| Help link | Cause, consequence, action shown in-line, not in a separate manual |

If you cannot write the action in one or two lines, the item is not a well-defined alarm or it is a maintenance diagnostic (summary).

| Bad | Good |
|---|---|
| "Error: failed" | "Camera disconnected during the run. The first 42 s were saved. Reconnect it and start a new run." |
| "LAH-0302" | "Tank 3 level high: 92 %, limit 90 %. Stop filling." |
| "Out of range" | "Pressure 2.4 bar, limit 2.0 bar. Motion held; open the vent." |
| "FATAL ERROR!!!" | "Drive overheated. Motion stopped. Let it cool 10 min, then press Reset." |
| One text reused for several causes | One text per cause: same text always means the same thing |
| "Invalid input by operator" | "Speed must be 0 to 5 m/min" |
| Modal dialog with only an OK | Non-modal banner row with a link to the fix |

Style: operator vocabulary, sentence case, no exclamation marks, no "please", "sorry" or jokes in safety messages, no blame, and say what the system is doing now rather than leaving the state unknown.

## 11. Comms-loss and device-offline alarms

| Rule | Detail |
|---|---|
| Stale is not normal | Show a frozen value as stale (dashes, hatch, grey, "last good 14:02:11"); never as live. Mark bad quality |
| One root alarm | A lost device raises one alarm; alarms derived from its points are suppressed or marked bad quality |
| Priority | By what the device protects. Loss of the only monitor of a hazard outranks loss of a convenience sensor |
| Heartbeat | Peer sends a counter at a fixed rate; typical timeout about 3 missed beats (verify: industry practice, no source). Timeout above worst-case jitter and below the time the process becomes unsafe |
| Safe state | The machine itself goes to a safe state on comms loss, independent of the screen. The HMI alarm is a notification, not the safety function |
| Recovery | Resync and require explicit confirmation before resuming motion if safety-relevant; no auto-restart |
| HMI-to-controller loss | Whole screen shows "No connection", controls disabled and visibly inactive |
| Cause | Distinguish powered off, cable fault and protocol error where diagnosable |
| Flapping | Debounce (stable 2 to 5 s before declaring restored, verify) and count flaps; escalate if frequent |
| Log | Each loss and restore as an event with duration |

## 12. Audit trail

Log, append-only and tamper-evident: alarm activation, return to normal, acknowledge, silence, shelve/unshelve with reason, suppression, out-of-service and return, limit/priority/deadband changes with old and new values and approver, operator login, operator actions, comms loss and restore.

Per record: timestamp (UTC plus local, ms resolution for sequence analysis), source device, alarm id, priority, value and limit, user, workstation. One synchronised clock; stamp at the source where possible. Retention period is a site rule (verify). Regulated sectors need who/what/when/why (21 CFR Part 11 for pharma, summary). Uses: incident analysis, monthly rate/flood/bad-actor KPIs, shelving review, comparing running configuration to the master alarm database.

## 13. Cross-domain lessons

Aviation (14 CFR 25.1322, AC 25.1322-1 [V: law.cornell.edu, faa.gov]):

| Level | Colour | Meaning | Aural |
|---|---|---|---|
| Warning | Red | Immediate awareness and immediate action | Continuous or repeating, may be voice |
| Caution | Amber | Immediate awareness, subsequent action | Single chime or tone |
| Advisory | White, cyan or green | Awareness | None or low |

The rule requires attention-getting cues through at least two senses for warnings and cautions, and prioritisation [V: 14 CFR 25.1322]. The colour assignment itself was not extracted from the AC (verify). Transferable:
- Dark (quiet) cockpit: in normal operation nothing lit, so any light is abnormal. Same as the grey, quiet normal state.
- Master warning/caution: one large attention-getter that is cancelled by pressing it, with the detail in a message list.
- Messages list "what is wrong" and "what to do" together, ordered by priority.
- Phase-of-flight inhibits: suppress non-critical alerts during critical phases. Applied to machines: inhibit by operating phase, visibly.
- False alerts are heavily penalised because they destroy trust; keep the number of aural alerts small and unambiguous.

Automotive tell-tales: red = danger to persons or serious damage immediate or imminent; yellow = outside normal limits, malfunction, damage likely; green = safety/normal [V: EU Reg. 3/2014 Annex VIII 2.1.8, 2.1.10]. ISO 2575 supplies symbols (colour table not read, verify). Transferable: standard symbols, few colours, and a start-up bulb check where every indicator lights at power-on to prove it works.

Medical: three priorities with standardised visual and audible signals (section 9); alarm fatigue is the failure mode (section 14).

## 14. Case lessons

| Case | Lesson (corrected facts) |
|---|---|
| Texas City, BP, 2005 | 15 killed, 180 injured. A level transmitter alarm at 72 % fired; a redundant hardwired high-level switch at about 78 % never sounded, though the tower had filled to about 13 ft. The blowdown-drum alarm failed from a holed float that the six-monthly rodding test could not detect. A repair on the level transmitter was deferred (work order of 10 March), and the pre-start-up alarm check was not completed. Test safety alarms by a method that can detect the failure; deferring an alarm repair is a hazard; show defect and bypass status [V: CSB final report, PDF pp. 17, 48, 50]. |
| Milford Haven, Texaco, 1994 | 275 alarms in the last 11 minutes for two operators; 26 injured, no deaths. Too many, poorly prioritised alarms; displays gave no overview; a control valve was shut while shown open [V: HSE CHIS6 p.1; HSE casetexaco94]. |
| Three Mile Island, 1979 | A relief valve stuck open while control-room instruments indicated it closed; operators did not recognise the loss of coolant [V: NRC fact sheet]. Show actual, not commanded, state (that the light showed the command is the standard reading but not in the NRC text, verify). Alarm count and printer lag are (verify). |
| Buncefield, 2005 | The independent high-level switch needed a padlock to hold its lever in the working position; the padlock was not fitted, so the switch was effectively inoperable, and no alarm reached the control room; the main gauge had stuck. A protection that a test can leave disabled gives false security; make test and override state visible [V: HSE/EA competent authority report pp. 4, 14]. |
| Air France 447, 2009 | Airspeeds became invalid after icing and the stall warning stopped while the aircraft was deeply stalled. Alert logic must not go silent in the worst case; design alerts for degraded sensors [V: flyingmag.com, atc-network.com summary of the BEA interim report; BEA final report not read]. |
| Medical alarm fatigue | Joint Commission SEA 50: 98 alarm-related events Jan 2009 to Jun 2012, 80 deaths, 13 permanent loss of function, 5 extra care [V: SEA 50 p.1]. Drew et al. 2014: 2,558,760 alarms in 31 days over 461 adult ICU patients; 88.8 % of the 1,154,201 arrhythmia alarms were false positives (not of all alarms) [V: UCSF news, study summary]. FDA logged 566 alarm-related deaths Jan 2005 to Jun 2010, likely an undercount [V: SEA 50 p.2]. Fewer, meaningful alarms; patient-specific limits; time-limited, visible off state. |
| Deepwater Horizon, 2010 (contested) | Testimony said the general alarm was set to inhibited; the company disputed it. Inhibit state must be prominent. Use only as an illustration, not a finding [summary: NBC, Fox]. |

## 15. Alarm philosophy outline (template)

One document per product. Short beats complete: fill each section in a few lines.

1. Purpose, scope, operator profile, what is out of scope
2. Definitions: alarm, alert, event, prompt, status, classes (safety, environmental, quality, asset, diagnostic)
3. Principles: every alarm has an action, a consequence and a response time; quiet normal state; eight attributes (relevant, unique, timely, prioritised, understandable, diagnostic, advisory, focused) (summary: EEMUA)
4. Roles: who can acknowledge, shelve, change limits
5. Prioritisation: the matrix, the number of levels, the target distribution
6. Presentation: colours, shapes, banner, summary, graphics, flash rules, sounds per priority, silence rules
7. Behaviour: ack, reset, latch, re-alarm, return to normal, first-out
8. Attribute guidelines: deadband, on/off delay, filtering, rate-of-change, bad-quality handling
9. Suppression, shelving, out-of-service: who, why, how long, approval, review
10. Operator guidance: cause, consequence, action, time, where stored and shown
11. Comms-loss and instrument-failure handling
12. KPIs: rate per 10 min, floods, standing, top 10, shelved count, targets from section 8, monthly review
13. Training, management of change, audit schedule, logging and retention

## 16. Common mistakes
- Calling everything an alarm: no action, or no time pressure, means it is an event or status.
- Priority by equipment importance, or top priority for most alarms.
- Reusing alarm red or amber for decoration, selection or a Stop label.
- Colour as the only priority cue; flashing acknowledged alarms; flashing large areas at 3 to 5 Hz.
- Modal alarm pop-ups that cover the screen needed to fix the fault.
- "Acknowledge all" on unseen alarms; silence that is indefinite or invisible; ack and silence merged.
- Analogue alarms without deadband or delay; copying delay values from a blog.
- Shelving without reason, expiry or a visible list; suppression that is invisible or not fail-safe.
- One alarm per signal on a comms loss instead of one root alarm.
- Showing the last value as live; showing commanded state as actual.
- Message text that is a tag, a code or "Error: failed"; one text for several causes.
- Alarm that depends on an untested sensor; deferred alarm repair with no visible flag.
- Treating the HMI alarm as the safety function instead of a controller safe state.
- No monitoring: nobody measures rate, standing alarms or shelved counts, so the list rots.
- Presenting a (verify) number as a requirement.

## 17. Sources
- HSE Chemicals Sheet 6 "Better alarm handling": https://www.hse.gov.uk/pubns/chis6.pdf ; HSE Texaco Milford Haven: https://www.hse.gov.uk/comah/sragtech/casetexaco94.htm
- EEMUA 191 4th edition news: https://operationsengineer.org.uk/plant-engineer-news/eemua-releases-guidance-on-industrial-alarm-systems/254082 ; EEMUA 191 4th edition contents: https://eemua.org/getattachment/9d3f8071-55c3-49bf-a74a-3bf6ad4a2e0f/Contents-EEMUA-Publication-191-Edition4-November-2024.pdf
- Honeywell/ASM benchmarking deck: https://process.honeywell.com/content/dam/process/en/documents/document-lists/doc_asm-consortium/presentations/August%2023%202009%20-%20Best%20Practices%20in%20Alarm%20Management%20Presentation.pdf ; Alarm numbers (trade article): https://www.chemengonline.com/alarm-management-numbers/
- ISA-18.2 study guide: https://open-exam-prep.com/study-guides/isa-cap/system-design-hmi-alarms-enterprise/alarm-management-isa182 ; Yokogawa lifecycle article: https://www.yokogawa.com/uk/library/resources/media-publications/implementing-alarm-management-per-the-ansi-isa-182-standard-control-engineering
- ISA InTech technical reports: https://www.isa.org/intech-home/2019/january-february/features/applying-alarm-management ; exida deadband: https://www.exida.com/Blog/why-should-i-use-an-alarm-deadband
- Naghoosi et al., ACC 2011: https://skoge.folk.ntnu.no/prost/proceedings/acc11/data/papers/1100.pdf ; Emerson on-delay blog: https://www.emersonautomationexperts.com/?p=44751
- Mindray monitor manual (flash rates): https://storage.mtender.gov.md/get/cff3d95a-bb6b-4669-a0f2-c53158b07de1-1664865640535 ; 60601-1-8 patent summary: https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11082786
- 60601-1-8 clause excerpt: https://standards.har-el.com/Projects/181701/60601-1-8/html/A2SubCl-6-3-3-1-a-priority-encoded.htm ; TI SSZT261: https://www.ti.com/lit/pdf/sszt261
- PUI Audio on 60601-1-8: https://puiaudio.com/news/key-updates-to-iec-60601-1-8-what-engineers-need-to-know ; 14 CFR 25.1322: https://www.law.cornell.edu/cfr/text/14/25.1322 ; FAA AC 25.1322-1: https://www.faa.gov/documentLibrary/media/Advisory_Circular/AC_25.1322-1.pdf
- EU Reg. 3/2014 Annex VIII: https://legislation.gov.uk/eur/2014/3/annex/1/annex/VIII/adopted ; CSB Texas City final report: https://www.csb.gov/assets/1/20/CSBFinalReportBP.pdf?13841
- Buncefield "Why did it happen?": https://www.icheme.org/media/10706/buncefield-report.pdf ; NRC TMI fact sheet: https://www.nrc.gov/reading-rm/doc-collections/fact-sheets/3mile-isle.html
- AF447: https://www.flyingmag.com/?p=10688 ; https://www.atc-network.com/atc-news/initial-accident-investigation-report-on-the-airbus-a330-203-flight-af-447-on-1st-june-2009 ; Joint Commission SEA 50: https://digitalassets.jointcommission.org/api/public/content/f65e5c9df2b94000a99445e0a7877007
- Drew et al. 2014: https://www.ucsf.edu/news/2014/10/119601/hospital-logs-staggering-25-million-alarms-just-month ; Deepwater Horizon testimony: https://www.nbcnews.com/news/amp/wbna38385494
- NUREG-0700 Rev 4: https://www.nrc.gov/docs/ML2602/ML26022A094.pdf ; MIL-STD-1472H: https://everyspec.com/MIL-STD/MIL-STD-1400-1499/MIL-STD-1472H_57041/
- FAA HFDS ch. 6: https://hf.tc.faa.gov/hfds/download-hfds/hfds_pdfs/Ch6_Controls_and_visual_indicators.pdf
