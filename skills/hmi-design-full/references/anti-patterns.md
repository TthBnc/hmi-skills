# HMI anti-patterns

Each entry: what it looks like, why it harms (incident or study where one
exists), and what to do instead. Tags: `[V: source]` = text was read;
`(summary)` = secondary source; `(verify)` = unconfirmed, do not quote.
Facts follow the verification logs, including corrected retellings.

## Contents

Data truth and comms (1-4); colour and coding (5-7); control, confirmation and
error (8-15); state, mode and command (16-19); alarms and messages (20-22);
automation (23-25); text, language, trends and looks (26-30); safety boundary
and security (31-32); Sources.

## Data truth and comms

### 1. Loading screen replaces the whole UI on comms loss
- What it looks like: when the link to the controller or backend drops, the
  entire screen becomes a spinner or "loading" page. Everything vanishes,
  including the last known values and the stop control.
- Why harmful: the operator loses the overview, cannot tell whether the machine
  still moves, and a spinner implies a brief wait, not a lost link. Information
  vanishes exactly when it matters (Endsley Level 1).
- Do instead: keep the screen, grey the values, show a persistent
  "No link, last data HH:MM:SS" strip with the age ticking, state what the
  machine does on link loss (stops, holds, retracts), and keep every available
  safe action. Fail visible, not blank.

### 2. Stale values shown as live
- What it looks like: a number that stopped updating looks like a fresh one.
- Why harmful: operators act on the old picture. A frozen frame looks like a
  valid image, and a live command on a stale frame leads to overshoot
  [V: ARL-TR-3834 §2.1.2.3]. OPC defines Bad_Stale and
  Uncertain_LastUsableValue precisely for this (summary).
- Do instead: stamp every live value with a quality state (good, stale, lost,
  estimated, conflicting) driven by data age against a timeout. Stale values are
  visibly different (hollow, dashed, struck through, "?" suffix) and age is
  readable. Overlay frozen video immediately and limit motion.

### 3. Unknown shown as zero
- What it looks like: before the first frame or after a sensor fails, the
  display shows 0, "OK" or a default that passes checks.
- Why harmful: 0 is a legitimate reading and a passing one for many limits, so
  a missing value looks healthy. Texas City: the level indicator read a falling,
  in-range level while the tower overfilled and the independent high-level alarm
  silently failed [V: CSB final report, PDF p.23, 50, 106].
- Do instead: model "no value" as a distinct state (null, not 0); render it as
  "--" with a quality flag; make startup and safety checks fail closed until a
  real, fresh value arrives; show instrument range limits.

### 4. Video freeze looks like a still scene
- What it looks like: the picture stops during link degradation, unmarked.
- Why harmful: operators judge motion from video; a stale frame hides motion.
  Below about 8-10 Hz teleoperation degrades [V: ARL-TR-3834 §2.1.1.4].
- Do instead: detect missing frames within a second or two, overlay
  "VIDEO LOST" with frame age, show a link-quality indicator, and halt or limit
  commanded motion automatically.

## Colour and coding

### 5. Colour-only status
- What it looks like: a green or red dot with no text, icon or shape.
- Why harmful: about 8% of men and 0.4-0.5% of women have colour vision
  deficiency [V: Birch 2012, via research notes]; sunlight and cheap panels
  wash colours out; colour alone also fails ISO 9241-125 style redundancy.
- Do instead: pair every colour with a word or icon and a shape or position;
  keep luminance contrast; test greyscale and a colour-blind simulation.

### 6. Rainbow "normal" screens
- What it looks like: bright colours on equipment, pipes and bars in normal
  state; reds and greens used decoratively.
- Why harmful: when everything is coloured, abnormal does not stand out, and
  the colour budget for alarms is spent. High-performance (grey-based) displays
  improved early abnormal detection from 10% to 48% in one vendor-affiliated
  simulator study with 21 operators; many factors changed at once, no
  independent replication [V: ASM/Nova study notes]. Treat as direction, not
  magnitude.
- Do instead: neutral background, muted normal states, saturated colour
  reserved for abnormal or alarm; one colour, one meaning; colour sets of
  about 5-7 categories with at least 40 delta E separation [V: NUREG-0700 Rev 4].

### 7. Alarm colours reused for normal or decoration
- What it looks like: red for a "stop" label, a closed valve or a brand accent
  on a screen that also uses red for alarms.
- Why harmful: operators cannot tell a state from an alarm at a glance, and a
  red-on-yellow control can be mistaken for the emergency stop device.
- Do instead: reserve the alarm colours for alarms; use neutral or shape-coded
  stop labels; never make a screen control resemble the physical e-stop.

## Control, confirmation and error

### 8. Confirmation on stop
- What it looks like: "Stop motor? Are you sure?" with OK and Cancel.
- Why harmful: stopping is the safe direction and must be immediate; a dialog
  adds seconds when seconds matter.
- Do instead: one-tap stop, always visible, in a fixed position, acting
  immediately; use undo or a "resume" action if the stop was a mistake.
  Confirmations belong on irreversible or costly acts, not on safe ones.

### 9. "Are you sure?" habituation
- What it looks like: the same generic dialog before many actions.
- Why harmful: confirmations decay into reflex. Warning click-through ranged
  from about 10% to 70% depending on design [V: Akhawe and Felt 2013];
  clinicians override 49-96% of drug alerts [V: van der Sijs 2006], mostly
  because specificity is low.
- Do instead: confirm rarely; state consequence and scope ("Delete 3 videos,
  2.1 GB, cannot be undone"); verb button labels; safe default; a different
  gesture (hold, type the name, second person) for the highest risk; prefer
  undo for reversible acts; log acceptance rates and remove dialogs that
  nobody reads.

### 10. Confirmation that was too generic: Hawaii 2018
- What it looks like: a test option and a live option sit next to each other
  with similar labels; a generic second prompt follows.
- Why harmful: on 13 Jan 2018 an employee selected the live ballistic-missile
  alert instead of the test; a confirmation was clicked through; the
  correction reached the public about 38 minutes after the alert (Wikipedia
  summary; FCC report not read) (verify the menu labels and sign-off details).
- Do instead: separate test and live structurally (different screen, colour,
  banner, login), consequence-specific confirmation, two-person integrity for
  high-consequence sends, and a pre-built, rehearsed cancellation path.

### 11. Cheap "proceed" on a safety fault: Therac-25
- What it looks like: a cryptic fault code and a single key to resume.
- Why harmful: Therac-25 radiotherapy accidents, six known overdoses 1985-87.
  Faults showed as "Malfunction 54", unexplained in the manual; the operator
  could press P to proceed up to five times; some clinics saw about 40 dose-rate
  malfunctions on some days, so resuming became routine. In overdose events the
  console showed "no dose" while the beam had delivered one [V: Leveson and
  Turner 1993, IEEE Computer 26(7), PDF p.1, 7]. Hardware interlocks had been
  replaced by software.
- Do instead: faults carry plain-language cause, severity and required action
  (not codes like "Malfunction 54"); no one-key bypass of a safety fault; show what actually happened (delivered,
  measured) rather than what was commanded; keep hardware protection.

### 12. Form shows fields, not the outcome: Citibank/Revlon
- What it looks like: an approval screen of checkboxes and amounts whose
  semantics are cryptic; approvers check the form, not its effect.
- Why harmful: in Aug 2020 a bank intended to pay about USD 7.8M in interest
  and wired about USD 900M after choosing the wrong options in a loan system;
  a three-step maker/checker/approver chain missed it (web search; district
  court Feb 2021; the appeal outcome and exact checkbox labels are (verify)).
- Do instead: before the final approve, show the plain-language result
  ("This will pay USD 893,000,000 to 3 lenders") and a diff against the intent;
  give rare high-consequence operations a distinct flow.

### 13. Control transfer on a touchscreen: USS McCain
- What it looks like: steering and thrust moved between stations by on-screen
  taps; throttles on a touchscreen whose split or ganged state is not obvious.
- Why harmful: on 21 Aug 2017 a watchstander unintentionally transferred
  steering control while thrust control was being moved; the helmsman believed
  the ship had lost steering. The lee helmsman slowed only one throttle, shaft
  speeds reached 44 vs 87 rpm; 10 sailors died. NTSB: mechanical throttles give
  tactile confirmation of ganging and are preferred [V: NTSB MAR-19/01, PDF
  p.36-37, 43].
- Do instead: show unmistakably who has what control; confirm every transfer
  explicitly at both ends; keep critical eyes-free controls physical; make
  split controls look split.

### 14. Disabled button with no reason
- What it looks like: a grey control that does nothing when tapped, with no
  explanation of which condition is unmet.
- Why harmful: the operator cannot tell if the machine is broken, the task is
  forbidden or a prerequisite is missing; this invites repeated taps and
  workarounds (routine violations, Reason).
- Do instead: show the reason next to the control ("Locked: head is moving"),
  or show permissives as a checklist (guards closed, pressure OK, mode = auto)
  with live OK/NOT OK per condition; make a tap on the disabled control
  explain, not ignore.

### 15. Hover-only affordances
- What it looks like: a control or tooltip that appears only on mouse hover, a
  hover state as the only sign of pressability.
- Why harmful: touch screens have no hover; the cue is unreachable, and gloves
  and glare reduce the remaining cues (gulf of execution).
- Do instead: permanent signifiers (button shape, label, state); show help
  inline or on long-press only as a secondary route; design for touch first.

## State, mode and command

### 16. Mode shown only in the page body (Asiana 214)
- What it looks like: mode in a small label inside the content area, changing
  silently on automatic transitions.
- Why harmful: on 6 Jul 2013 the autothrottle went to HOLD, which does not
  control speed. The HOLD annunciation was displayed, boxed green for 10 s,
  but none of three crew noticed; 3 of 291 died. NTSB contributing factors:
  complexity of automation under-documented, and increased likelihood of mode
  error [V: NTSB AAR-14/01, exec. summary, PDF p.18, 45]. The lesson is that
  a transient, text-only, unexpected change is easy to miss.
- Do instead: put mode in a persistent header or strip plus near the control;
  code it redundantly (text, shape, position); show the consequence ("Speed
  not controlled"); annunciate automatic changes with a persistent,
  non-modal cue; alert on the absence of an expected automatic function.

### 17. Indicator shows the command, not the state (TMI PORV)
- What it looks like: a lamp lit when the controller sent "close" rather than
  when the valve is measured closed.
- Why harmful: at Three Mile Island (1979) a stuck-open relief valve leaked
  coolant while instruments indicated it closed and operators did not
  recognise a loss-of-coolant accident [V: NRC fact sheet]. That the lamp
  showed the commanded (solenoid) state is the standard reading but is
  (verify) in the primary report.
- Do instead: show commanded and actual separately ("Cmd: close / Pos: open"),
  highlight any disagreement, and derive the indicator from a measured signal.

### 18. Optimistic success before confirmation
- What it looks like: the UI shows "done" or the new value as soon as the tap
  is sent; blocks incoming updates for a moment to avoid flicker.
- Why harmful: when the command fails or is clamped the operator believes a
  false state; suppressing incoming data hides the truth. Gulf of evaluation
  (Norman).
- Do instead: three visible stages: pressed, sent/pending, confirmed by the
  actual state. Pending looks different from done; time out visibly; on
  disagreement show the real value.

### 19. Latched speed steps with no hold-to-run or link-loss stop
- What it looks like: tapping a step button changes commanded speed, and the
  machine keeps going if the operator, screen or link disappears.
- Why harmful: loss of signal does not stop motion; a dead or frozen screen
  leaves the machine moving. Hold-to-run or enabling devices exist for this
  (summary: IEC 60204-1, robot pendants).
- Do instead: hold-to-run or an enabling device for hazardous motion; heartbeat
  watchdog that stops on loss; show "stopped by watchdog" afterwards; keep the
  decision in hardware, not in the screen.

## Alarms and messages

### 20. Toasts for faults
- What it looks like: a banner announces a lost board, then vanishes.
- Why harmful: an alert needs to persist until acted on. Change blindness and
  attention narrowing mean a 4-6 s banner is easily missed, and nothing marks
  the state afterwards.
- Do instead: faults become persistent, prioritised alarms with a visible
  state (active, acknowledged, cleared), a history list and a persistent strip;
  toasts only for transient confirmations ("Saved").

### 21. Alarm flood
- What it looks like: every abnormality raises an alarm; an upset triggers
  dozens in a minute.
- Why harmful: Milford Haven (1994): 275 alarms in the last 11 minutes for
  two operators [V: HSE CHIS6 p.1]. Targets: long-term average at most 1 per
  10 min and at most 10 in the first 10 min of a major upset [V: HSE CHIS6
  citing EEMUA 191]. TMI: more than 100 alarms in the first minutes
  (verify).
- Do instead: an alarm requires a defined operator action; everything else is
  status or log. Use at most three priorities (about 5/15/80 percent split), a
  first-out marker, deadband, on-delay, and state-based suppression; review
  monthly.

### 22. Silenceable alarms and acknowledge-all
- What it looks like: a siren silenced without action; acknowledge-all.
- Why harmful: Bhopal: the plant alarm was silenced soon after sounding and
  instruments were distrusted (secondary; sources not read) (verify). In
  general, acknowledgement becomes reflex and hides new alarms.
- Do instead: acknowledge only what is displayed; silencing the sound never
  clears the condition; the visual alert persists until the state clears.

### 23. Single-sensor automation without disagreement display (737 MAX)
- What it looks like: automation with authority reads one sensor; a
  second sensor disagrees and nothing says so.
- Why harmful: MCAS could act on a single angle-of-attack sensor. The AOA
  DISAGREE alert was certified standard but inoperable on more than 80% of the
  MAX fleet because it was tied to an optional display; MCAS was not disclosed
  to pilots. 346 died in two accidents. Federal guidelines assume a 4 s
  response; a Boeing test pilot took more than 10 s in a simulator [V: House
  T&I report, PDF p.20-21, 27, 130; NTSB ASR 2019].
- Do instead: redundant sensing, visible disagreement and the source in use,
  standard (not optional) safety alerts, disclosed authority, an obvious way to
  disable the automation, and response-time assumptions tested with several
  simultaneous alerts and startle.

### 24. Silent automation handover (AF447, Uber)
- What it looks like: automation disengages, degrades or hands back with a
  brief or silent cue, or asks one operator to supervise for hours.
- Why harmful: AF447 (2009): pitot icing, autopilot disconnect and degraded
  control law; side-sticks not visibly linked; stall warning ceased with invalid
  data (BEA final report not read: (verify) specifics; secondary sources only).
  Uber ATG (2018): the system detected the pedestrian 5.6 s before impact but
  never classified her, dropped tracking history on reclassification, had
  emergency braking disabled, and a one-second action suppression with no alert;
  the sole operator was looking at a phone [V: NTSB HAR-19/03, PDF p.8, 13, 25].
  The human monitor was not a safety layer.
- Do instead: announce handover early, with reason and time budget; say
  explicitly who has control; show a "what happened" summary and current values;
  never make passive monitoring the only safety layer; do not disable
  automation safeguards and rely on an inattentive human.

### 25. Machine output presented as fact
- What it looks like: a classification, count or "defect found" appears with the
  same style as measured values; accepting is one tap, correcting is five.
- Why harmful: explanations did not reduce overreliance and could raise
  acceptance of wrong advice [V: Bansal et al. 2021]; satisfaction of search
  and automation bias reduce independent checking.
- Do instead: label as machine-generated, show the evidence (frame, crop,
  time), show a few categorical confidence levels tied to actions, one-gesture
  correction, log overrides, and require independent human judgement first for
  high-stakes items [V: Bucinca et al. 2021 for forcing functions].

## Text, language, trends and looks

### 26. Internal IDs and engineering names in operator text
- What it looks like: "Board 3 fault", hex codes, variable names, database
  IDs, or "head 0x2F" where the operator thinks in pipe, cable and lamp.
- Why harmful: the operator must translate, and translation fails under stress
  (gulf of evaluation). Different vocabulary between screen and manual causes
  mistakes.
- Do instead: operator vocabulary, one name per thing across screens and
  manual; show IDs only in an admin or detail view.

### 27. Auto-scaled trends hiding change
- What it looks like: a trend whose axis rescales to fit the data, so a drift
  and a flat line look the same, or a limit that moves.
- Why harmful: slope and distance-to-limit are the cue; auto-scaling erases
  them and makes noise look like events.
- Do instead: fixed axes tied to limits, normal band shaded, limit lines drawn,
  current value as the end point; time window stated; mark data gaps; use the
  same scale for comparable channels.

### 28. Missing right-to-left support in a translated UI
- What it looks like: Arabic or Hebrew text shipped in a left-to-right layout;
  icons, progress bars and arrows not mirrored; numbers misplaced.
- Why harmful: reading order and progress direction break; values get misread.
- Do instead: use direction-aware layout (logical properties, `dir`), mirror
  layout, progress and navigation but not clocks, media icons or physical
  direction symbols (joystick directions refer to machine reality); numbers stay
  left-to-right; test with the real language and fonts.

### 29. Truncated or shrunk labels after translation
- What it looks like: ellipses on machine commands, text auto-shrunk to fit,
  button label changed in layout.
- Why harmful: a clipped command can hide the difference between "Retract" and
  "Retract all"; localisation lengthens strings.
- Do instead: fixed-size controls with wrapping label areas; test the longest
  language on every screen state; never ellipsise or shrink safety or machine
  commands; size the container to the text.

### 30. Decorative 3D, gradients and animation
- What it looks like: shaded 3D equipment icons, gradient buttons, animated
  backgrounds, flashing logos.
- Why harmful: decoration spends salience and reduces contrast. One 2016 study
  found interactive 3D helped problem detection (verify), so the rule is "no
  decorative 3D", not "never 3D".
- Do instead: flat shapes, neutral background, motion only for urgency; use 3D
  only when it carries information a 2D view cannot, and test it.

## Safety boundary and security

### 31. Touchscreen as the only stop or the safety reset
- What it looks like: an on-screen emergency stop or a software reset of a
  safety function.
- Why harmful: the screen can freeze, reboot or crack. An ordinary
  touchscreen plus standard controller only reaches PL b / Category B; e-stops
  need at least PL c, are latching and work in all modes (summary:
  ISO 13850, ISO 13849-1; verify against licensed text).
- Do instead: hardwired, monitored emergency stop and enabling device; safety
  reset on a physical device; the screen shows status and guidance only; the
  machine must be safe with the screen dead.

### 32. Hard-coded shared admin PIN
- What it looks like: a fixed PIN in client code, shared by every technician
  and every machine.
- Why harmful: WARNING (security): anyone with the application package can read
  it; there is no individual accountability or revocation. IEC 62443 expects
  authentication on every interface including the HMI, unique accounts from
  SL2, role-based access and audit of changes (summary).
- Do instead: per-user or per-role credentials issued and revocable centrally
  (or a hardware key), no secrets in client code, lockout and audit of
  setpoint, mode and limit changes, and a login-independent path for emergency
  actions.

## Sources

- Leveson and Turner 1993 (Therac-25), IEEE Computer 26(7).
- NTSB MAR-19/01 (McCain), AAR-14/01 (Asiana), ASR-19/01 (737 MAX), HAR-19/03
  (Uber); US House T&I 737 MAX report 2020; CSB BP Texas City report 2007; HSE
  CHIS6; NRC Three Mile Island fact sheet; ARL-TR-3834.
- Akhawe and Felt 2013; van der Sijs 2006; Bansal 2021; Bucinca 2021; Sarter and
  Woods 1995; Norman 2013; Reason 1990.
- Not read, so (verify): BEA AF447, FCC Hawaii, Kemeny, Bhopal, Citibank/Revlon.
