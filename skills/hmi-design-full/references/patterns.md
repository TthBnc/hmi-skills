# HMI screen and workflow patterns

Domain-neutral patterns for operator screens on machines, robots, process and
field equipment. Adapt names and pages to the machine; keep the structure.
Evidence tags: `[V: source]` verified in a read source, `(summary)` secondary
or paraphrased, `(verify)` unconfirmed: check before quoting or relying on it.
Worked examples live in `examples/`. Alarm rules live in `alarms.md`.

## Contents

1. Screen frame
2. Display hierarchy and navigation depth
3. Overview (home) screen
4. Setup as a checklist; pre-start checks and permissives
5. Running a task
6. Live values with context
7. The operator's camera or video view
8. Parameter and setpoint entry
9. Recipes and profiles
10. Automation and model output
11. Hold, review and playback as modes
12. History, records and reports
13. Maintenance and diagnostics; settings vs operation; roles
14. Notifications vs alarms
15. Confirmations
16. Wording and microcopy
17. Empty, loading and error states
18. Cross-domain patterns worth copying
19. Common mistakes
20. Sources

## 1. Screen frame

Every operator screen shares one frame. Fixed positions are learned by the
hand and the peripheral eye; never reflow the frame between modes.

| Area | Position | Contents | Rule |
| --- | --- | --- | --- |
| Status strip | fixed, top | link/connection, machine state with elapsed time, mode, resource warnings (storage, battery, consumables), highest-priority active fault | Always visible, never covered by a dialog. Tapping the fault opens its detail. |
| Alarm banner | directly under the strip, same width | top 1-3 unacknowledged alarms: priority shape + colour + text, time, acknowledge | Empty when nothing is wrong (quiet = normal). See `alarms.md`. |
| Navigation | fixed edge (left or bottom) | 3-6 large labelled destinations | Current one unmistakable. Guarded or disabled while it would lose work, with the reason shown. |
| Work area | centre | the task: video, values, controls | Dominant. Overlays show only what this task needs. |
| Action area | fixed, bottom or dominant-hand side | the one primary action, plus Stop | Same place on every screen so the hand learns it. |
| Message line | footer | command feedback ("Sent", "Rejected: door open") | One line; details behind "More". |


## 2. Display hierarchy and navigation depth

ISA-101 style levels (summary), mapped to machine HMIs:

| Level | Purpose | Typical screen |
| --- | --- | --- |
| 1 | overview of the whole operation | home / run screen |
| 2 | control of one unit or task | task screen with its primary action |
| 3 | detail and diagnostics | history, logs, item detail, I/O view |
| 4 | support and technical help | versions, manuals, service tools |

- Any detail is at most 2 touches from the overview. The "3 clicks" figure is
  a heuristic, not a tested law (summary). Prefer fewer, richer screens to deep
  menus on small machines.

## 3. Overview (home) screen

- Purpose: answer "is everything OK, what is the machine doing, what next?" in
  one glance.
- Contents: state and mode, the 3-8 values that decide the task (with targets
  and limits), the active alarm summary, the primary action, and a way to the
  last/current record.

## 4. Setup as a checklist; pre-start checks and permissives

Setup collects what the task needs; pre-start checks prove the machine and
site are ready. Keep them separate screens or sections.

**Checklist rules**

- One row per prerequisite with a state word: Ready, Needs attention, Checking,
  Not needed for this task. Each row has one button for the next thing to do.

**Permissives (start conditions)**

| Part | Rule |
| --- | --- |
| Definition | A permissive is a condition that must be true to allow an action (door closed, pressure in range, device connected). |
| Display | Beside the disabled Start, list each unmet permissive with its live value: "Pressure 0.9 bar, needs below 0.05". |
| Enforcement | The controller enforces them. The HMI shows them; it is never the only gate. |
| Bypass | If a bypass exists, it needs a role, a reason, a visible persistent "bypassed" marker, auto-expiry and a log entry. Show the risk text once, plainly. |
| Interlock vs check | An interlock blocks automatically and is not operator-overridable. A check informs; the operator may proceed only if policy allows. Label which is which. |

A "safe to start" interlock input that blocks cycle start is standard on cure
and UV controllers (summary). Hard-gate the dangerous step, not the whole setup.

## 5. Running a task

State model first. Use one enumerated state, not a set of flags. A minimal
default: Idle, Starting, Running, Pausing/Held, Stopping, Stopped, Fault.
PackML defines 17 states with wait vs acting classes (section 18) [V: 06
domain-examples §4.1; OPC UA StateEnumeration]. Reuse its vocabulary if the
machine is in packaging or discrete manufacturing.

- The main value or live view dominates. Start/Stop is the largest control.
- While running: the primary button becomes Stop (danger styling), the strip
  shows state and elapsed time, and the work area has a distinct running
  treatment (border or band).
- Transitional states are visible: "Starting...", "Stopping...", "Saving...",
  each with a timeout and a result. Never leave the operator guessing whether a
  command took.
- Stop and emergency actions are never confirmed. A physical emergency stop
  exists independent of the screen (section 18).
- Pause/Hold keeps the record open and recording; the strip says "Held". Resume
  is a separate, deliberate action with the same size as Pause.
- **Progress and ETA**: show elapsed time, a progress bar against a known total
  (length, volume, steps), and ETA only when it is computable. Label the basis
  ("at current speed"). Recompute when conditions change and flag a degraded
  mode: "Reduced speed, finish moves to 14:35". If progress is unknown, show
  elapsed time only, not a fake bar.
- **Automatic actions** (auto pause, auto power reduction, auto stop) show the
  reason and the planned resume: "Paused: temperature 78 C above 75 C. Resumes
  below 70 C." (summary: UV controllers pause and resume at lower power on a
  temperature threshold.)
- **Recording**: if the run is recorded (video, data, log), say so in the
  strip with a distinct indicator. Recording is automatic and never optional or
  hidden when a record is a deliverable. Stopping shows "Saving..." until the
  record is confirmed, then "Saved" with a link. Never claim success early.
  Warn before storage runs out, with time left at current rate.

## 6. Live values with context

- Each value shows: number, unit, target or setpoint, normal range or limits,
  and a trend one tap away. A bare number is data; value + range + trend is
  information [V: 02 HP-HMI §1] (summary).
- **Data quality** (full rules in `states-and-commands.md`). Minimum displayable
  states: Good, Stale (kept, de-emphasised, with age), Bad/Unknown (dashes, no
  plausible number), Not yet received, Simulated/Forced/Overridden. Unknown is
  never shown as 0 [V: 02 §9].

## 7. The operator's camera or video view

Video is often the main sense of the operator. Treat it as a measured, stateful
instrument, not a decoration.

| Element | Rule |
| --- | --- |
| Layout | Video dominates the centre; telemetry in a strip around it; controls in drawers or fly-outs. Modals must not cover it. |
| Overlays | Only task-needed fields (distance, speed, time, labels). Configurable per customer or spec, saved as a profile. If the overlay is burned into the recording it is a deliverable: it needs the same care as a report (verify: source attribution from unpublished research; independently check the named source). |
| Labels | Name each camera ("Front", "Drum"). Show which one is recorded. |
| Frame age | Show a small "live" indicator tied to real frame arrival. If no new frame for about 1-2 s, mark it stale ("No new image for 3 s"), do not leave a frozen picture that looks live. |
| No signal | A black or frozen image is not a state. Show an explicit "No camera signal" panel with the cause if known and the fix ("Check the cable"), plus time since last frame. Retry silently, but make the state visible. |
| Placeholder frames | If the system sends placeholder frames during mode switches, label them ("Switching camera...") so they cannot be mistaken for the scene. |
| Fullscreen | One tap in, a large Exit control out, same position every time. |
| Presets | One-tap views (forward, side) beat free PTZ for repeatable work (summary: IBAK, RapidView). |
| Horizon | If the image can roll, offer upright/horizon lock and a roll indicator (summary). |
| Second viewer | A read-only mirror for a helper is cheap value (summary). |
| Environment | Glare, vibration and dim cabs: allow brightness and day/night palettes; keep overlay text high-contrast. |

Frame age and no-signal are among the most often missing states in field HMIs.

## 8. Parameter and setpoint entry

Number entry is the classic hazard: infusion-pump incident analyses name
ten-times and wrong-rate errors as central, caused by design not by users
(verify: source attribution from unpublished research; independently check the named source).

- Show metadata with the field: unit, allowed min and max, default, step,
  current value, and what the parameter does (summary: 07 §4.3).
- Validate as typed. Reject out-of-range values with the range in the message:
  "Speed must be 0.2-2.0 m/min." The controller validates again; the HMI never
  is the only check.
- Warn on plausible-but-unusual values (10x the previous) and ask to confirm
  them; do not accept implausible ones.
- Use steppers for small changes and a keypad for large ones. Do not use
  free-running sliders for values that need precision.
- Show before and after: "Speed 0.8 -> 1.0 m/min". Echo the final value with
  its unit before applying.
- **Apply vs Cancel**: edits are drafts until Apply. Cancel restores the old
  values and says so. The dirty state is visible ("Unsaved changes"). Leaving
  the screen with a dirty draft is guarded.
- Apply is a command: show pending, then confirmed by the controller's actual
  value, never by the local copy. If rejected, show why and keep the old value.
- Parameter changes during a run are logged with old value, new value, time
  and who.

## 9. Recipes and profiles

- A recipe is a named, versioned set of parameters for a product or job. A
  profile is a named set of display or site preferences (overlay, units,
  standards). Both reduce typing and errors (verify: source attribution from unpublished research; independently check the named source).
- Show the active recipe always: "Recipe: Liner 400 / v7" and whether values
  were edited from it ("modified").
- At least two stored user configurations plus a reset-to-defaults, recalled
  with confirmation, is the maritime minimum (S-Mode, section 18) (verify: source attribution from unpublished research; independently check the named source).

## 10. Automation and model output

Automation output is evidence, not truth.

- Show the result with its evidence: the image with overlays, the per-class
  breakdown, the reading behind the decision.
- Use a few states with rules behind them, not raw probabilities. Default four:

| State | Rule (example, tune per domain) | Operator action |
| --- | --- | --- |
| Confirmed | stable for N consecutive readings and above the reference | none, or accept |
| Settling | changing within a window | wait |
| Check | disagrees with an independent signal, or below threshold | look and decide |
| Not running | input missing or automation off | say what is needed |

- State the rule in help text ("Confirmed after 5 s without change").
- Correction must be fast: large labelled choices per item and one tap for
  "the whole result is correct". Show original and corrected side by side;
  every correction is undoable until saved.
- Automation may propose and advance steps only if the operator can see why and
  override. Show the planned next action and a countdown where it is
  time-triggered.

## 11. Hold, review and playback as modes

- Hold/freeze, review and playback are modes. Each has a distinct label and
  colour on the view and in the status strip. Norman's mode-error principle:
  distinct modes must look different (summary).
- While in a non-live mode, hide live values or mark them "not live". A frozen
  picture must never be mistakable for live. Show an explicit "FROZEN" or
  "REVIEW" label and time.
- Playback of recorded data has its own transport: play/pause/seek, with
  touch-sized targets and a time readout. Synchronise video with the data
  trace on one timeline (verify: source attribution from unpublished research; independently check the named source).
- Saving a correction returns to live with a confirmation. Unsaved edits are
  guarded when leaving.

## 12. History, records and reports

- Lists have plain columns: when, duration, who, outcome, size, notes. IDs
  only in a technical section of the detail view.
- Deleting names the record, says what is removed (record, or video only) and
  that it cannot be undone. Offer export first when a record is a deliverable.
- **Records as deliverables.** Where a log is evidence (cure logs, batch
  records), it must be complete, timestamped, tamper-evident and exportable.
  The record fields should be fixed by spec before the screen is designed.
  Spec-driven fields for a curing log are in
  `examples/cable-driven-pipe-rehab-machine.md`.
- Reports are generated on the device from templates, preview before save, and
  export to USB or network. Missing data shows as missing, not blank or zero.

## 13. Maintenance and diagnostics; settings vs operation; roles

- **Separate setup, settings and diagnostics from operation.** Operating
  screens stay clean; calibration lives elsewhere (Cockpit leaves it to the
  vehicle software; CNC has a separate start-up area) (verify: source attribution from unpublished research; independently check the named source).
- Diagnostics screen content (summary: 07 §4.9): versions, uptime, link
  health and last message age, raw and scaled I/O with quality and forced
  flags, subsystem health (temperatures, voltages, storage), counters (lamp
  hours, wear, calibration due), log viewer and support bundle, self-test.
- **Roles.** Define at least Operator, Supervisor/Technician, Admin. Show only
  what the role needs. A visible indicator when an elevated mode is on (a
  frame colour or strip label), automatic return to operator after a timeout.
- Permission lives on the controller. A client-side PIN or role flag is
  cosmetic (WARNING: a secret in client code is readable by anyone with the
  program) (summary: 07 §5.2-5.3).

## 14. Notifications vs alarms

| | Alarm | Notification |
| --- | --- | --- |
| Needs operator action now | yes | no |
| Persistence | stays until resolved and acknowledged | auto-dismisses or lives in a log |
| Colour | red/amber, reserved | neutral or blue |
| Sound | by priority | none |
| Location | alarm banner, status strip | transient message line, log |

- Only interrupt for conditions that need action. Everything else is status
  or log (ISA-18.2) (summary).
- At most three alarm priorities. Group repeats; suppress consequences of an
  already-shown cause. Full rules in `alarms.md`.
- Format: what happened, why if known, what to do. "Camera disconnected during
  the run. The first 42 s were saved. Reconnect it and start a new run." Codes
  and IDs go in technical details.
- Queue modal dialogs: one at a time, with a stated priority order, and the
  emergency screen above all of them (summary: local ADR pattern).

## 15. Confirmations

- Confirm only irreversible actions: delete, discard unsaved work, reset, mode
  changes with consequences. Prefer undo for everything else.
- The title names the object. The destructive button names the verb ("Delete
  run from 10:42"), not "OK". The safe choice is the default and is placed
  further from the hand.
- Never confirm Stop, Hold or emergency actions.
- Hold-to-confirm or slide-to-confirm works for rare dangerous actions when
  it shows progress and cancels on release (QGroundControl uses a confirmation
  slider) (verify: source attribution from unpublished research; independently check the named source).

## 16. Wording and microcopy

- One sentence of help per panel; details behind "More".
- Operator's words, not system words. Same verb everywhere: "Start run" ->
  "Running" -> "Run saved". Disabled controls say why. Errors state the fix
  without apologising. Give units. Do not use ALL CAPS sentences.

| Bad | Good |
| --- | --- |
| Error 0x2F | Pressure sensor not responding. Check the hose, then press Retry. |
| Operation failed | Could not save. Disk is full (0.4 GB free). Delete old runs in Records. |
| Invalid input | Speed must be 0.2-2.0 m/min. |
| Are you sure? | Delete run from 10:42? This cannot be undone. |
| OK / Cancel | Delete run / Keep run |
| Payload rejected | The job file is for a different machine. Choose another file. |
| State: epoch 3 | Curing, 62% |
| Disabled button, no text | Connect the camera first |
| Comms timeout | Lost contact with the control unit 12 s ago. Outputs stay as they were; check the cable. |
| Warning | Lamp temperature 78 C, above 75 C. Light pauses and resumes below 70 C. |
| Calibration needed | Pressure sensor not zeroed. Vent the line, then press Zero. |
| Success | Run saved (42 min, 2.1 GB). Open |

## 17. Empty, loading and error states

Design every async state for every screen: empty, loading, pending, success,
failure, stale, disconnected, partial.

- **Empty**: say what belongs here and the next action. "No runs yet. Start a
  run to see it here." Never a blank panel.
- **Loading**: show a skeleton or "Loading..." with a timeout. After the
  timeout, switch to an error with Retry. Keep already-loaded content visible
  while refreshing.
- **Pending**: the control shows pending and ignores a second tap until the
  result arrives. Pending times out into "Unknown outcome - check the machine",
  never into silent success.
- **Error**: cause in operator terms, effect on the task, fix. Keep unsaved
  work. Offer Retry in place.
- **Disconnected**: strip message, values greyed with age, controls disabled
  with a reason. On reconnect, resync before enabling controls and show
  "Reconnected" (summary: 07 §3.5).
- **Partial / degraded**: name what still works and what does not ("Rear
  camera offline. Recording continues from the front camera").
- **Startup**: never let a default 0 pass as a measurement. Show "Waiting for
  first reading".

## 18. Cross-domain patterns worth copying

| Pattern | What it does | Copy as | Source |
| --- | --- | --- | --- |
| ETCS DMI fixed areas | Distance, speed, supplementary, planning and message areas keep fixed positions; speed colours grey, yellow, orange, red map to supervision status | A fixed layout map that never changes between modes; a small coded set of colours for supervision level | (verify: source attribution from unpublished research; independently check the named source) |
| Airbus ECAM | Three alert levels, checklist actions shown inline with the alert, system page auto-shown for the failing system | Alert plus "what to do" text and the relevant detail one tap away | (verify: source attribution from unpublished research; independently check the named source) (verify) for inline actions |
| S-Mode / always-on standardisation | Standard terminology, icons and grouping; critical functions reachable by a single action; at least two stored configs | Common words and icons; single-action access to critical controls | (verify: source attribution from unpublished research; independently check the named source) |
| PackML | One shared state vocabulary: wait vs acting states, Held vs Suspended, Abort and Clear; modes Production, Maintenance, Manual | State and mode always visible; only valid commands shown | [V: ISA-TR88.00.02, OPC UA StateEnumeration] |
| Teach-pendant enabling switch | Three-position device: released stops, middle enables, hard squeeze stops; hold-to-run in manual mode | Motion enabled only while a deliberate physical input is held; stop physical and independent of the touch screen | (verify: source attribution from unpublished research; independently check the named source) (verify standards list) |
| Drag-and-drop overlay builder | Operators place static text, entries and live variables on the video, and save and recall profiles | Overlay profile per customer; overlay is a deliverable | (verify: source attribution from unpublished research; independently check the named source) |
| Tamper-proof cure logs | Process data logged each second, tamper-proof, sent live to the cloud; RFID tracks lamp wear | Log by default, tamper-evident, with maintenance counters in pre-start checks | (verify: source attribution from unpublished research; independently check the named source) |

Physical controls: stops, enabling devices and mode keys are physical and
independent of the touch computer (teach pendants, EOD robots, UV drum e-stops
separate for lamps and drive) (verify: source attribution from unpublished research; independently check the named source).

## 19. Common mistakes

- Toasts for lasting conditions; no persistent status strip.
- Connection loss hides the whole UI, or the last value stays on screen looking
  live.
- Camera black or frozen with no "no signal" or frame-age state.
- A check pre-marked as passed; a default 0 treated as a measurement.
- Disabled controls with no reason.
- Confirmations on Stop; no confirmation on delete; OK/Cancel labels.
- Number entry with no range, no unit, no before/after.
- Live parameter edits that apply immediately with no Apply and no log.
- Automation shown as a bare percentage with no evidence or rule.
- Recording success claimed before it is saved; recording hidden or optional
  when it is the deliverable.
- Client-side PIN treated as security.

## 20. Sources

- ISA-101.01-2015; ISA-18.2 / EEMUA 191; ISA-TR88.00.02 and OPC UA PackML
  StateEnumeration; ERA ETCS driver manual (via Emery, STRC 2016); IMO
  MSC.1/Circ.1609; CHI+MED infusion-pump work; NUREG-0700 Rev. 3 (draft).
- Vendor material: Envirosight VC500, Trelleborg UV doc, Vortex, IMS, IBG
  smartcure 5.0, NuFlow; QGroundControl, Cockpit and dVRK docs.
