# Physical interaction and operating environment

How operators touch, press, see and hear an HMI in real conditions: gloves,
water, vibration, sun, noise, shared terminals, vehicles. Domain-neutral.

Evidence tags: `[V: source, location]` = read in source text; `(summary)` =
secondary summary; `(verify)` = practice or recall; check before quoting as a
requirement. Synthesis tables are design judgement, not standards.

## Contents
1 Touch targets; 2 Gloves, water, touch technology; 3 Touch behaviour and
gestures; 4 Numeric entry; 5 Physical vs on-screen controls; 6 Direction mapping,
joysticks, pendants; 7 Critical actions; 8 Feedback and double activation;
9 Viewing, sun, dimming; 10 Vibration, PPE, noise, audio; 11 Accessibility;
12 Localisation; 13 Kiosk; 14 Vehicle and mobile standards; 15 Common mistakes;
16 Sources

## 1. Touch targets and spacing

Specify in millimetres, then derive pixels: `px = mm x ppi / 25.4`. Example: a
20 mm target on a 160 ppi panel = 20 x 160 / 25.4 = 126 px; on 96 ppi = 76 px.
10 mm = 63 px at 160 ppi.

| Source | Target | Separation | Note |
|---|---|---|---|
| MIL-STD-1472H 5.1.3.1.17 | 15-38 mm | 3-6 mm; at least 5 mm for "first contact" actuation | bare finger; add 5 mm per dimension for gloves; force 250 mN-1.5 N [V: 1472H via 01 notes; FAA report Table 1, p. 9] |
| NUREG-0700 Rev 4 11.3.2.3.6-2 | 10-40 mm | 3-6 mm | above 22 mm square gives no further gain [V: Rev 4, pp. 11-46/47] |
| BSR/HFES 100-2026 draft | 9 x 9 mm (7 where accuracy matters less) | 3.2 mm | office desk floor [V: draft, p. 33-34] |
| Microsoft Windows guidance | 7.5 mm | n/a | enlarge for frequent or high-consequence targets [V: Microsoft Learn] |
| Material 3 | 48 dp, 8 dp apart | | about 9 mm at typical density (arithmetic) [V: m3.material.io] |
| WCAG 2.2 SC 2.5.8 / 2.5.5 | 24 / 44 CSS px | | web floors, not industrial sizes [V: W3C] |
| Rockwell (desktop touch) | command button 40 x 40 px; object touch 30 x 30 min; 10 px gap | | [V: PROCES-WP023] |

Default tiers (synthesis):

| Context | Target | Gap | px at 96 / 160 ppi |
|---|---|---|---|
| Fixed station, bare finger | 15 mm (1472H minimum) | 4 mm | 57 / 94 |
| Thin nitrile or lab gloves | 20 mm | 5 mm | 76 / 126 |
| Work gloves, field, vibration | 20 mm minimum, 25 preferred | 6 mm | 76-95 / 126-157 |
| Safety-relevant or hard-to-undo | 20-25 mm plus a confirm step | 8 mm or more | 76-95 / 126-157 |

The rule: gloved primary controls are at least 20 mm. 15 mm bare plus the
+5 mm glove allowance gives 20 mm; NUREG's 10 mm minimum is a bare-finger
floor, not a glove size. Do not use the 12 mm tier seen in older notes.

- Hit area may exceed the visible shape; never overlap neighbours' hit areas.
- Gap matters as much as size; destructive and constructive actions never
  adjacent, never identically styled.
- Keep primary controls inset from the bezel; users must reach all corners
  without full arm extension or upward reach [V: NUREG Rev 3 11.3.2.3.6-10].
  The 5-8 mm edge inset is convention (verify).
- Parallax from thick cover glass shifts touches; use bonded glass (verify
  offset size) [V: NUREG 11.3.2.3.6-2 acknowledges parallax].
- Panel keytops, if present: at least 12 mm, 18 mm preferred for gloves [V:
  NUREG Rev 3 11.3.2.2.2-1].

## 2. Gloves, wet screens, touch technology

| Technology | Bare | Gloves | Wet | Notes |
|---|---|---|---|---|
| Resistive | works (pressure) | any glove or tool | immune to drops | lower clarity, no multi-touch, wears (verify) |
| PCAP, standard | excellent | fails with thick/non-conductive | ghost touches | consumer default |
| PCAP glove/water mode | good | thin to medium (claims 2-5 mm) | needs rejection firmware | mode switching, less precision |
| Infrared | good | any | dirt, sun can trigger | large formats |
| SAW | good | soft gloves only | contamination | mostly legacy |
(technology facts: (verify), vendor claims vary widely.)

- Choose by the real glove, wet and dry; test, do not trust "glove mode".
- If gloves are required and PCAP is chosen, add hardware keys for essential
  functions.
- Provide a clean mode that freezes input while the screen is wiped (duration
  15-30 s is practice, verify). NUREG-0700 lists "deactivate controls for
  cleaning" and glove incompatibility as touchscreen disadvantages [V: Rev 3
  Table 11.7].

## 3. Touch behaviour and gestures

- Act on release inside the target; show the pressed state on touch-down; sliding
  off cancels. (standard practice, verify)
- Ignore touches shorter than about 30-50 ms and contacts larger than a finger
  (palms); ignore touches for 200-300 ms after a screen change (all verify).
- Latency: touch response at most 100 ms, 55 ms preferred [V: NUREG Rev 3
  11.3.2.3.6-7; 1472H 5.1.3.1.4 at most 100 ms]. Provide a positive indication
  of actuation [V: 1472H 5.1.3.1.3; NUREG 11.3.2.3.6-6].
- Auto-repeat initial delay 500-750 ms with a visible cue [V: NUREG
  11.3.2.3.6-9]. Double-click is two clicks within 700 ms [V: NUREG glossary].
- No hover: nothing may depend on tooltips or hover. State it in text.
- Reject multi-touch where the function is single-touch; interlocked pairs
  (forward/reverse) must not both fire.

| Gesture | Verdict |
|---|---|
| Tap | use |
| Double-tap | avoid; timing fails with gloves and vibration |
| Long press | only as visible hold-to-confirm |
| Swipe between pages | avoid for primary navigation |
| Pinch, rotate | only for maps, trends, camera images where errors are harmless |
| Drag and drop | avoid for commands |
| OS edge swipes | disable in kiosk |
| Pull-to-refresh | never |
| Multi-finger control | never |
| Scroll lists | acceptable with visible scrollbar and page buttons |

## 4. Numeric entry

- Tapping a numeric field opens an in-app keypad, not the OS keyboard. Keys meet
  the glove tier (15-20 mm). Pick one layout (phone or calculator) and keep it.
- Show allowed range and units on the keypad, the old value and the typed value.
- Validate while typing; say why a value is rejected ("maximum 250").
- Offer +/- only where negatives are legal, decimal point only where decimals are.
- Value applies only on OK; OK and Cancel apart; dangerous parameters get a
  further confirmation after OK. Entry errors by orders of magnitude must be
  caught [V: ASM cat. 9, priority 1].
- Sliders: only for coarse, reversible settings. A finger covers 10-15 mm of
  track, so a 100 mm slider resolves roughly 30-50 values (arithmetic). Pair
  with +/- steps and a numeric readout; thumb at least target size; value shown
  offset from the thumb. Not for exact safety setpoints.
- Free text: avoid; use pick lists, scan codes, presets. Prefer PIN or badge for
  login. No auto-correct in IDs; scroll the edited field above the keyboard.
- Spinner wheels or tiny steppers never as the only method.

## 5. Physical vs on-screen controls

| Function | Physical and independent of the screen? |
|---|---|
| Emergency stop | Yes: red mushroom on yellow, latching, hardwired to the safety circuit (ISO 13850, IEC 60204-1) (summary); never only on screen |
| Enabling device (3-position) | Yes for manual motion in hazardous zones: released = stop, mid = enable, hard squeeze = stop [V: UR 3PE guide 8.1] |
| Hold-to-run, jog | hardwired, or held input with stop on signal or comms loss (summary) |
| Mode selector (auto/manual) | key or access-controlled switch (summary) |
| Safety reset | separate deliberate action, never combined with start (summary) |
| Beacon/horn for safety | independent of the HMI (summary) |

- The touchscreen is a convenience layer: safety functions work with the screen
  dead, frozen, rebooting or cracked. Show the hardware chain (e-stop engaged,
  guards, enabling device) but never be its actuator.
- Rule of thumb: if it is needed within 1 s, with gloves, without looking, or in
  an emergency, make it physical (synthesis).
- Hardware keys for Home, Alarm, Acknowledge stay reachable when the screen
  hangs. Soft keys beside the screen tolerate gloves; keep labels stable.
- Rotary encoder with push: one-handed, glove-friendly; detents match steps;
  apply dangerous values on push, not on turn.
- Key force: keyboard keys 0.25-1.5 N to snap (0.5-0.6 N preferred); legend
  pushbuttons 2.8-16.7 N [V: NUREG Rev 3 11.3.2.2.2-10, 3.1.2.3-9]. The old
  "2-5 N" figure is withdrawn. Touch actuation force 250 mN-1.5 N [V: 1472H].
- Physical lamp and button colours: red emergency/stop, yellow abnormal, green
  normal, blue mandatory action (IEC 60073 / 60204-1, summary). Mirror them on
  screen with shape and text redundancy. Whether START is green or white is
  unresolved (IEC 60204-1 text unread).

## 6. Direction mapping, joysticks, pendants

- Spatial compatibility: control layout mirrors the layout of what it controls.
- Movement compatibility: up, right, clockwise, push or forward means
  increase, on or start; the display pointer moves in the same direction as the
  control. IEC 60447 defines actuating directions for switches and pushbuttons
  (summary; check clause text before citing). Stimulus-response compatibility
  (Wickens; Proctor and Vu) explains why violations raise errors even for
  experts (summary).
- Frame of reference: through a camera view, "left" turns the view left; for an
  overhead map, controls map to map axes. Say which frame is active ("Camera
  view" / "Machine frame") and remap when a camera is rotated.
- Joysticks: spring return to centre for velocity; dead band about 5-10%; exponential
  curve for fine speed; rate limiting (verify). Enable (deadman) button: no
  motion unless held. On link loss, stick fault or sleep, demand falls to zero
  and the HMI shows link status. Industrial remotes carry IP rating and e-stop;
  consumer pads are not rugged.
- Show demand, actual state and control source (which pad, who has control);
  explicit take/release of control when several controllers exist.
- Not a safety or irreversible function on a single trigger.

## 7. Critical-action patterns

| Pattern | How | Use when | Weakness |
|---|---|---|---|
| Single tap with undo | acts, shows Undo for N s | reversible, no physical effect | not for physical actions |
| Select-then-operate | arm target (auto-disarm 5-30 s, verify), then distinct EXECUTE | switching equipment, medium risk | slower; needs clear armed state |
| Hold-to-confirm | press and hold about 1-2 s (verify) with filling ring; release cancels | frequent semi-dangerous actions | vibration breaks the hold; not accessible to all |
| Slide-to-confirm | drag handle across track | rare; consumer-style | poor with gloves, water, vibration, PPE; avoid in the field |
| Confirm dialog | modal OK/Cancel | rare, moderate-risk | habituation; ASM says no modals for routine work [V: ASM cat. 9] |
| Typed confirmation | type asset name or word | irreversible data or config, admin | slow; keyboard needed; not for time-critical |
| Key/role gate | badge, key, PIN | config and maintenance | shared credentials |
| Two-hand or two-person | hardware (ISO 13851) | hazardous machine start (summary) | hardware level |

Choose by consequence and reversibility: low and reversible = tap (+ undo);
medium = select-then-operate or hold; high or physical hazard = hardware
enabling + two-step + interlocks (+ role gate); destructive data = typed
confirmation naming the object. NUREG-0700 asks for an additional confirmatory
action on important touch tasks and separate select and activate steps for
serious-consequence inputs [V: Rev 3 11.3.2.3.6-8, 7.3.7-1]; a soft control must
not activate when its display is not working [V: 7.3.7-1].

Dialog rules: lead with object and effect ("Stop pump 2? Flow to tank A
ceases"), verb buttons, Cancel as default focus, one dialog per decision, no
stacked confirmations, never appearing under the expected tap spot.

Never confirm stop. Stop, abort and pause act on first touch with no dialog;
a confirmation delays the safe action. Confirm the risky direction (start,
resume, override), not the safe one.

## 8. Feedback and double activation

Command lifecycle: input registered (<100 ms) -> sent (pending) -> accepted or
rejected with reason -> executing -> state reached (from measured feedback) ->
timeout or failure (explicit message, safe state, alarm if needed). Show the
confirmed state from feedback, not the commanded one. Optimistic UI is
forbidden for machine state (a button may show pending; the state indicator
waits). Time out expected transitions (stroke time plus margin).

Double activation:
- Disable and show pending the instant a command is sent; re-enable on response
  or timeout.
- Debounce taps (about 300-500 ms, verify) and tag commands with IDs or sequence
  numbers so a retry is idempotent.
- Reject stale commands (time-to-live, 1-2 s for motion, verify).
- Jog or hold: heartbeat repeats the command (10-20 Hz) and the receiver stops
  on 100-300 ms silence (verify).
- Show permissives (guard closed, e-stop released, mode) as a checklist near the
  control; Ready, Running, Not ready (why), Fault are separate states.

## 9. Viewing distance, angle, sunlight, dimming

- Size text by visual angle (visual-language.md section 5): 16 arcmin minimum, 20-22
  preferred [V: NUREG Rev 4 1.3.1-4].
- Minimum viewing distance 330 mm [V: 1472H 5.2.2.11.4]. Display and its control
  within 635 mm of a seated eye point (older HFDS, verify).
- Viewing angle: IPS/ADS/MVA panels for off-axis wall or pedestal mounts; TN
  shifts at 30-40 degrees (verify). Large shared displays: group viewers within 30
  degrees of centreline (HFDS, 1472F, verify). Touch-desk viewing near 400 mm with
  centre 35-45 degrees below horizontal [V: BSR/HFES 100-2026 draft].

| Condition | Luminance guide | Source |
|---|---|---|
| Control room | at least 35 cd/m2, preferably 100+; preferred 80-160 | [V: NUREG Rev 3 11.3.1.4.3-1] |
| Indoor industrial panel | 300-500 nits | (verify) vendor practice |
| Sunlight-readable | 1000+ nits plus optical bonding and AR coating | (verify) vendor practice |
| Illuminance | overcast 1,000-10,000 lux; direct sun 50,000-100,000+ | (verify) |

- Effective contrast under glare is (L_display + L_reflected) / (L_black +
  L_reflected), with L_reflected = lux x reflectance / pi (arithmetic). Uncoated
  glass reflects about 4%, AR under 1% (verify).
- Outdoors: higher contrast than indoor minima, bold weights, no mid-tone pairs
  (orange on red), polarised sunglasses can black out an LCD (verify). Test in
  real sun; dark vs light is a hardware-dependent call.
- Brightness: day / standard / night levels, manual control one tap away,
  auto sensor with hysteresis; night target about 1-5 nits (verify); alarms stay
  distinguishable when dimmed; dim red accents help keep dark adaptation.

## 10. Vibration, PPE, noise, audio

| Factor | Effect | Response |
|---|---|---|
| Vibration | mis-touches; blur near seated body resonance (about 4-8 Hz, verify) | 20 mm+ targets, text up about 25-50% (verify), no sliders, hardware keys, hand rest, debounce; ISO 2631 for whole-body exposure |
| Cold | LCD slows, touch less sensitive | heated or low-temp LCD, larger targets, no animation |
| Heat | black LCD, shorter life | rated display, thermal dimming |
| Wet | false touches | water rejection, sealed front |
| PPE (gloves, visors, tinted lenses) | dexterity; visors dim or polarise display | larger targets; test through the visor; avoid blue-only information under yellow lenses |
| Hearing protection and noise (over 85 dB(A)) | masks audio | visual and vibrotactile redundancy |

Audio:
- Alarm sound about 15 dB above background across the reception area per ISO 7731
  as summarised by a vendor; criteria vary by edition (verify). Main spectrum
  500-1500 Hz (vendor summary).
- Distinct patterns per priority (rate, pitch, beep count); critical repeats until
  acknowledged. Never audio only. Silence is timed, never a permanent mute of
  safety audio.

## 11. Accessibility

- Never colour alone (WCAG 1.4.1 [V: W3C]); see visual-language.md for colour
  vision (about 8% of men, about 0.4% of women [V: Birch 2012]).
- Hearing: visual duplicate of every audio alert. Vision: scalable text, a
  high-contrast theme. Motor: large targets, no timing-dependent gestures.
  Cognitive: consistent layout, no surprise changes, undo, plain language
  (reading grade 6-8 aim, verify). Left- and right-handed use; reachable for seated
  and standing operators.
- Short language switch reachable without login; use the language's own name, not
  a flag.

## 12. Localisation

| Item | Rule |
|---|---|
| Text expansion | allow 30-50% spare space; short strings (10 chars or fewer) can grow 200-300% of English length, 11-20 chars 180-200%, over 70 chars about 130% (IBM table via W3C) [V: W3C i18n]; per-language percentages (German +30%) (verify) |
| Layout | wrap to two lines, no text in images, strings in resource files, pseudo-localisation tests |
| CJK | shorter text but needs legible stroke size and taller line height (verify) |
| RTL | mirror layout, progress bars, back/forward; do not mirror clocks, media controls, or direction of real machine motion (joystick directions); numbers stay LTR (verify) |
| Numbers | locale decimal and thousands separators; make entry accept both; store one format |
| Dates and time | ISO 8601 and 24 h in logs; unambiguous on screen |
| Units | unit beside every value; user choice, SI stored; never convert silently in alarms; both units on limits for mixed workforces |
| Symbols | prefer ISO 7000/7010/3864 symbols; check cultural meaning of tick and cross; icon plus label |

## 13. Kiosk concerns

| Concern | Rule |
|---|---|
| Lockdown | full-screen single app; disable OS gestures, menus, notifications, update prompts, task switching, context menus, text selection, devtools, file drag, pinch-zoom, shortcuts; admin escape by key, PIN or hardware |
| Boot-to-app | straight to the application; target under 30-60 s (verify); splash with an error state; watchdog restarts a crash and returns to the last safe screen; never show a desktop or OS error |
| Updates | never mid-operation; admin-only prompts; survive power loss (read-only root, journaling) |
| Burn-in | OLED, and LCD retention: pixel shifting, dim idle, avoid static bright logos; prefer LCD for always-on static HMIs (verify) |
| Idle | dim to 20-30% while keeping alarm and state readable (verify); never blank where status must stay visible; alarms wake at full brightness; wake touch is swallowed |
| Shared-terminal auth | badge, RFID or 4-6 digit PIN; read-only status without login; role and user always visible; quick user switch; log changes with user ID |
| Roles | viewer, operator, supervisor, maintenance, engineer, admin; least privilege; show locked functions as "Requires supervisor" |
| Idle logout | 5-30 min, 2-5 for privileged (practice, verify); countdown 10-30 s; never during active control or a pending alarm; logout never stops the machine |
| Security | disable USB mass storage and debug interfaces; no default passwords; WARNING: hard-coded PINs in shipped code are a vulnerability |

## 14. Vehicle and mobile standards

| Standard | Content | Status |
|---|---|---|
| NHTSA Visual-Manual Guidelines, 78 FR 24818 (2013) | task completable with glances of 2 s or less and 12 s or less total eyes-off-road; occlusion alternative 1.5 s intervals, TSOT 12 s; per se lockouts: manual text entry over 6 presses, reading over 30 characters | [V: 78 FR 24818, PDF pp. 4, 10, 11] |
| Alliance (AAM) | 15 s static task time, 20 s occlusion TSOT | [V: same, p. 17] |
| JAMA | TEORT 8.0 s, TSOT 7.5 s; no single-glance limit | [V: same, pp. 46, 47, 51] |
| ISO 15005 | dialogue management for in-vehicle information systems while moving | scope [V: iso.org]; numbers unread |
| ISO 15008 | visual presentation of in-vehicle displays (passenger cars, excludes HUD, rear camera, maps) | scope [V]; contrast and size numbers unverified |
| ISO 17287 | procedure to assess suitability for use while driving | scope [V] |
| ISO 15077:2020 | agricultural tractors and self-propelled machinery: operator controls (forces, direction, location); NOT earthmoving or forestry | scope [V] |

Glance metrics (2 s / 12 s vs 15 s vs 8 s) differ in kind and are not
interchangeable. Translation for work machines and remote vehicles (synthesis):
- Each interaction completes in a glance of 2 s or less with 1-2 touches; use
  hardware for continuous tasks.
- Gate text entry, long menus and settings to "stopped"; show "Available when
  stopped".
- Constant-position, shallow menus (2-3 levels while operating); no auto-scrolling
  lists, no time-limited prompts except safety.
- Show wireless link quality; failsafe stop on loss.

## 15. Common mistakes
- Using WCAG's 24 px or a phone's 44 pt as an industrial glove size.
- Sizing for the bare finger, then issuing gloves.
- Confirming stop, or confirming everything with "Are you sure? OK/Cancel".
- Slide-to-confirm, double-tap or pinch on a vibrating, wet, gloved screen.
- Slider for an exact safety setpoint.
- Optimistic toggles; showing commanded state as actual.
- Only on-screen e-stop; enabling or hold-to-run in software alone.
- Greyed-out button with no reason; hover tooltips.
- Colour-only coding; audio-only alarms; permanent mute.
- Blanking the screen where status must stay visible; logout that stops control.
- ISO 15077 applied to cars or earthmoving machines.

## 16. Sources
- MIL-STD-1472H (via FAA/Honeywell touch report, rosap.ntl.bts.gov dot_61043).
- NUREG-0700 Rev 3 (ML20162A214) and Rev 4 (ML26022A094), nrc.gov.
- BSR/HFES 100-2026 draft; Microsoft Learn targeting; Material 3; WCAG 2.2.
- UR 3PE teach pendant guide; ISO 13850, 13851, 10218, IEC 60204-1/60073/60447
  (summary only).
- NHTSA 78 FR 24818 (govinfo); ISO catalogue pages for 15005, 15077.
- Nielsen response times; APCA in a Nutshell; W3C i18n text-expansion note.
