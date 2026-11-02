# Visual language for operator HMIs

Defaults for how an operator screen looks: colour, type, values, trends,
hierarchy, icons, motion, data quality and control states. Domain-neutral.
Define everything once as named design tokens; screens use tokens only.

Evidence tags: `[V: source, location]` = read in the source text;
`(summary)` = from a secondary summary; `(verify)` = practice or memory, check
before quoting as a requirement. Never present `(verify)` numbers as rules of a
standard.

## Contents
1 Tokens and colour roles; 2 Colour count, coding, CVD; 3 Contrast; 4 Themes; 5 Typography; 6 Numbers; 7 Analog indicators; 8 Trends; 9 Hierarchy and layout; 10 Icons and labels; 11 Blink and animation; 12 2D vs 3D; 13 Data quality; 14 Control states; 15 Vendors; 16 Common mistakes; 17 Sources

## 1. Design tokens and colour roles

Philosophy (High Performance HMI, ASM Consortium): normal is visually quiet;
saturated colour is reserved for abnormal states, so a deviation pops out
without reading. Colour is one facet only; layout, hierarchy, shapes and
context matter as much. [V: 02 notes s3, Hollifield/GE Vernova]

| Token role | Use | Default rule |
|---|---|---|
| canvas | page background | unsaturated grey, never pure white or black; Rockwell uses #E0E0E0 for a light theme [V: Rockwell PROCES-WP023] |
| surface | panels, cards | one step from canvas; flat, no gradient or shadow |
| ink | values, titles | dark grey rather than black (Rockwell #3F3F3F) [V: Rockwell] |
| ink-muted | labels, units | clearly lighter than ink but still passing contrast (section 3) |
| line | borders, process lines | mid grey; thicker line, not colour, for emphasis [V: Rockwell] |
| live | data that updates | one calm non-alarm colour, or plain ink; same everywhere |
| setpoint / reference | targets, demand values | one cool colour (often blue) used only for this |
| normal-state | running, open, healthy | neutral (grey or off-white); do not use bright green [V: Rockwell, ASM] |
| idle / off | stopped, disabled, scheduled | darker grey, quieter than normal |
| advisory | non-urgent info | one low-saturation hue, distinct from the alarm hues |
| alarm-low/med/high/urgent | priority colours | 3-4 fixed colours, each with its own shape and number (section 2) |
| quality-bad / stale | data not trustworthy | grey hatch or dashes plus a symbol, not an alarm colour |
| mode / held | review, replay, simulated, forced | one distinct non-alarm colour plus a persistent word |

Rules:
- One colour, one meaning, on every screen. No per-screen palettes.
- Only alarm icons use the red-to-yellow range; navigation icons stay
  uncoloured. [V: Rockwell]
- One spacing scale (4/8/12/16/24/32 px) and one type scale; no one-off values.
- There is no common alarm palette across vendors (Rockwell, Ignition and ASM
  examples disagree on which hue is "high"). Pick yours, document it, keep it
  fixed. [V: 02 notes s15b]

## 2. How many colours; redundant coding; colour vision

| Question | Default | Source |
|---|---|---|
| Object-category colours | 7 or fewer, ideally 3-6 semantic | [V: ASM guideline 6, 2009 slides] |
| Alarm priorities shown | 3 (4 with advisory), each with colour + shape + number | (summary: EEMUA 191, ISA-18.2); [V: Ignition docs] |
| Colours in one coding set | at least 40 delta E apart (CIE 1976 L*u*v*), giving about 7-10 usable colours | [V: NUREG-0700 Rev 4, 1.3.8-7, p. 1-51] |
| Coloured symbol vs background | at least 100 delta E (CIE Yu'v' units) | [V: NUREG-0700 Rev 4, 1.3.8-8, p. 1-52] |
| Acknowledged vs unacknowledged | same hue, different saturation/brightness or blink vs steady | [V: ASM; Rockwell] |

Redundant coding: every state is carried by at least two of colour, shape,
text, position. Colour alone is never enough (WCAG SC 1.4.1, level A)
[V: W3C WCAG 2.2].

| State | Colour | Shape | Text | Other |
|---|---|---|---|---|
| Normal | neutral | none or small dot | none, or state word | quiet |
| Advisory | advisory hue | circle | short label | steady |
| Warning | amber | triangle | WARNING + cause | steady |
| Alarm | red | diamond/rectangle with priority number | cause + action | blink only until acknowledged |
| Stale / comms lost | grey | hatch or "?" | NO DATA + age | no number shown |

Colour vision deficiency: about 8% of men of European descent and about 0.4%
of women; 4-6.5% of Chinese and Japanese men [V: Birch 2012, JOSA A 29(3):313,
abstract]. Another source rounds the female figure to 0.5% [V: Colour Blind
Awareness]. Do not use the popular "10% / 1%" figures; they have no primary
support.
- Never red vs green, or blue vs purple, as the only difference.
- Separate hues by luminance too; blue + orange and dark blue + yellow are safer
  pairs (verify with a simulator: Color Oracle, Coblis, browser devtools).
- Reserve red and yellow for alarms only. [V: ASM 6.2]

Conflict: machine standards (IEC 60073/60204-1) use green for normal; HP-HMI uses grey. Use IEC colours on physical lamps/buttons, grey normal on screen with redundant coding; document the choice. (summary)

## 3. Contrast

| Target | Minimum | Source |
|---|---|---|
| Text (normal) | 4.5:1 | [V: WCAG 2.2 SC 1.4.3] |
| Large text (18 pt, or 14 pt bold) | 3:1 | [V: WCAG 2.2 SC 1.4.3] |
| UI components, graphics | 3:1 against neighbours | [V: WCAG 2.2 SC 1.4.11] |
| Operational text, enhanced | 7:1 (4.5:1 large) | [V: WCAG 2.2 SC 1.4.6] |
| Display screen, including glare and ambient | at least 6:1, 10:1 preferred | [V: NUREG-0700 Rev 3, 11.3.1.4.1-2, p. 337] |
| Display under 1,000 lux or specular 1,000 cd/m2 source | at least 3:1 | [V: NUREG-0700 Rev 3, 11.3.1.3-2/-3] |

APCA (draft WCAG 3 method, polarity-aware, not normative) [V: APCA in a
Nutshell]:

| Lc | Use |
|---|---|
| 90 | preferred for fluent body text |
| 75 | minimum for columns of body text |
| 60 | minimum for other content text |
| 45 | larger or heavier text; detailed pictograms |
| 30 | absolute minimum for any other text and solid icons |
| 15 | absolute minimum for non-semantic non-text (dividers, focus outlines) |

Defaults: WCAG numbers as floor; 7:1 on operational text, 10:1 on alarms outdoors (verify); cross-check APCA (WCAG 2 mis-rates some dark and orange pairs); measure grey-on-grey secondary text; test on the real panel in real light.

## 4. Dark vs light themes by environment

No controlled study of dark vs light control-room themes was found. Decide by
measured environment and test on the hardware. (verify) throughout.

| Environment | Default | Why |
|---|---|---|
| 24/7 dim control room or cabin, night use | dark or mid-grey, dimmable | less glare and dazzle |
| Daylit room, controlled lighting | light-mid grey | classic HP-HMI; matches paper-era practice |
| Outdoor, direct sun, non-bonded LCD | test both; start with high-luminance, bold, high-contrast | sunlight lifts black levels; thin light text washes out |
| Mixed indoor/outdoor or day/night | both themes plus auto (ambient sensor, hysteresis) and manual override | one tap away |

- Alarm colours keep their meaning and pass contrast on both themes.
- At night use a dim dark-grey canvas, muted accents, no large white areas;
  alarms stay distinguishable at low luminance.
- NUREG-0700 Rev 3 control-room luminance: character or background at least
  35 cd/m2, preferably at least 100; preferred range 80-160 cd/m2
  [V: 11.3.1.4.3-1]. Far lower than sunlight displays; see
  physical-and-environment.md.

## 5. Typography and visual angle

Legibility is set by visual angle, not pixels.

| Rule | Value | Source |
|---|---|---|
| Character height, minimum | 16 arcmin | [V: NUREG-0700 Rev 4, 1.3.1-4, p. 1-39] |
| Preferred for reading | 20-22 arcmin | [V: same]; ISO 9241-303 same range (summary, secondary) |
| Not larger than | 24 arcmin for text (Rev 3); 45 arcmin for character groups | [V: NUREG-0700 Rev 3, 1.3.1-4, p. 37] |
| Labels, MIL-STD-1472H | at least 15 arcmin, 20 preferred | [V: 5.4.7.1] |
| Information-system text floor | 10 arcmin, 15 recommended | [V: MIL-STD-1472H 5.17.18.2] |
| Minimum viewing distance | 330 mm | [V: MIL-STD-1472H 5.2.2.11.4] |

Formula: height_mm = distance_mm x arcmin x 0.000291. Capital height at 20
arcmin: 2.9 mm at 0.5 m, 4.1 mm at 0.7 m, 5.8 mm at 1 m, 11.6 mm at 2 m.
Font em size is about cap height / 0.7, so 4.1 mm caps means about 5.9 mm em
(about 22 px at 96 ppi, 37 px at 160 ppi). Size scales linearly with distance.
[V: derived from NUREG formula, 02 notes s11]

Defaults:
- Sans-serif with distinct 0/O and 1/l/I. No serif, italic or condensed faces.
- 2-3 sizes: key value, body/label, small unit. Values larger and bolder than
  labels; labels and units in muted ink.
- Sentence case; all caps only for short state words.
- Weight 500+ on small text; thin faces fail in sun and under vibration (verify).
- Text size checked on the real panel at the real distance.
- Rockwell example sizes (desktop monitor, Arial): live value 11 pt bold,
  labels 8 pt, titles 24 pt bold; bigger for wall displays [V: Rockwell].
  These suit a seated desk viewer, not a standing gloved operator.

## 6. Numbers: precision, formatting, units

| Rule | Detail |
|---|---|
| Tabular numerals | `font-variant-numeric: tabular-nums` (or a monospaced-digit face) on everything that updates |
| Alignment | right-align, or align the decimal point; labels left; units left of nothing, right of the number [V: Rockwell] |
| Decimals | fixed per tag; never show more than the sensor resolves (2 needed, do not show 3); integers get no decimal point [V: Rockwell] |
| Significant figures | typically 3-4; match accuracy and noise, not the data type (verify) |
| Filtering | smooth or round the display, never the control signal (verify) |
| Units | beside every value, smaller and muted; one unit system per screen; SI stored internally (verify) |
| Unknown | dashes or "?" , never 0 |
| Separators | locale decimal and thousands; ISO 8601, 24 h time for logs |
| Update rate | a value that jumps faster than it can be read is noise: slow the display refresh (verify) |
| Magnitude | entry fields reject order-of-magnitude slips; show allowed range [V: ASM cat. 9] |

Do not use the unsourced "4-10 updates per second" figure. Display refresh of 1-2 s suits most process values; alarm banner under 1 s (verify).

## 7. Analog indicators, bars, sparklines

Show a value in context, not as a bare number: range, normal band, limits,
setpoint, trend. [V: Ignition docs; ASM]

Moving analog indicator (the signature HP-HMI object):
- A small scale with a pointer: instrument range, shaded normal band, limit
  ticks, setpoint marker (reference colour), value shown as text.
- Pointer and band change colour only when a limit is crossed.
- Variants: vertical bar (levels), horizontal bar (tables), dual bar (actual
  vs target), centred deviation bar (zero in the middle), bullet graph.
- Bar graph shows high/low, alarm limits and setpoint. [V: Rockwell]
- Use numbers for precision and bars for state; combine, do not choose.
  Some operators prefer numbers; the evidence is mixed.

Sparklines:
- Tiny axis-free trend beside the value, endpoint dot, normal band shaded.
- Same time scale for every sparkline on a screen so shapes compare.
- Window: minutes for fast machines, 1-2 h for slow processes (verify).
- Show direction and rate; an operator can then project, not just perceive.

Radar/fan charts only for parallel measurements of one type. KPI tile = value + unit + target + delta + sparkline; colour only off target (verify).

Evidence: ASM/Nova simulator study (n = 21, vendor-led, many changes at once): early detection 10% to 48%, success 70% to 96%, time 18.1 to 10.6 min [V: Chemical Processing 2006]; it cannot isolate colour. Controlled grey-vs-colour evidence is thin; one 2007 study found layered colour coding faster than monochrome (abstract only, summary).

## 8. Trends

| Topic | Default |
|---|---|
| Time ranges | 4-5 presets matched to the task, e.g. 10 min / 1 h / 8 h / 24 h; default per variable group (verify) |
| Scale | fixed to engineering range or normal band; auto-scale only as an explicit, labelled mode |
| Auto-scale danger | magnifies noise so a flat line looks like an excursion, and squashes real deviations; if used, show min/max and a lock |
| Setpoint and limits | draw setpoint (dashed, reference colour), alarm limits (thin lines), normal band |
| Control loops | actual and output in separate stacked panes, not overlapped |
| Pens | about 4-6 per chart (verify); colour plus line style; same variable, same colour everywhere |
| Cursor | "now" marker, time cursor readout, shared time axis, events as markers |
| Bad data | draw a gap; never interpolate silently |
| Presets | pre-configured trends per unit or problem beat blank ad-hoc trending [V: ASM cat. 2] |
| When | use trends where operators decide on change over time [V: ASM 2.x, priority 1] |

## 9. Display hierarchy and layout zones

| Level | Name | Purpose | Content |
|---|---|---|---|
| 1 | Overview | "is everything OK?" | key indicators, alarm summary, critical trends; no control detail |
| 2 | Unit/area control | daily operation | simplified schematic, loop access, analog indicators, mini trends |
| 3 | Detail | start-up, abnormal handling | equipment groups, interlocks, detailed control |
| 4 | Support | diagnosis, maintenance | faceplates, diagnostics, help, logs |

(summary: ASM, ISA-101, Rockwell). Rockwell designs Level 2 first and Level 1
second [V: Rockwell]. Operators live in levels 1-2; 3-4 are for upsets and
diagnosis (verify). Small machines may need only 2-3 levels.

Layout zones, identical on every screen: header/status (mode, user, comms),
alarm banner (always visible, highest priority first), navigation (fixed),
work area, feedback/footer. Spatial memory beats reading, so keep things in
place. Safety-relevant status (alarm, stop state, mode) is visible regardless of
screen or login. (verify: pixel heights)

Navigation: flat and simple; primary displays reachable without menus; all Level 2 displays reachable from anywhere [V: ASM cat. 5]. "Three clicks" is a heuristic, not a proven limit. Highlight the current screen; no swipe-only navigation on kiosks; structure by operator task, not by P&ID or software module; no modal dialogs for routine work [V: ASM cat. 9, priority 1].

Schematics: simplified ISA-5.1/5.5 symbols, two line weights (Rockwell 3 px / 1 px) [V: Rockwell], flow left to right, importance by size.

## 10. Iconography and labels
- Icon plus text label; icon-only only for universal, non-critical controls.
- Use standard symbols (ISO 7000, IEC 60417, ISO 7010); avoid hands, animals, tick/cross as sole meaning.
- Icon size: Rockwell 32 px buttons, 16 px info icons (desktop) [V: Rockwell]; on touch 24 px minimum, 32-48 preferred (verify).
- Labels name the function in operator words, tag secondary; buttons say what they do ("Stop pump 2"), not "OK".
- Alarm text: what happened, why it matters, what to do. Mixed case [V: ASM cat. 8]. Same name on screen, panel and manual.

## 11. Blink, flash and animation

| Rule | Value | Source |
|---|---|---|
| Alarm flash rate | 3-5 flashes/s, roughly equal on/off | [V: NUREG-0700 Rev 3, 4.2.6.2-3, p. 203]; MIL-STD-1472H emergency 3-5 Hz at 50% duty [V: 5.7.3.5.1] |
| Coded flash rates | at most two rates, at least 2 Hz apart, slow at least 0.8 Hz, fast at most 5 Hz, 50% duty preferred | [V: NUREG 1.3.10-12; 1472H 5.17.27] |
| Single rate | about 2-3 per second, on-time at least 50 ms | [V: NUREG Rev 3, p. 52] |
| Faster = more critical | yes | [V: NUREG 1.3.10-15] |
| Caution text flash | at most 2 Hz | [V: MIL-STD-1472H 5.7.3.5.2] |
| Flicker to avoid | 1-30 Hz bright pulsing | [V: MIL-STD-1472H 5.12.1.4.2] |

- Flash only urgent items; never routine data or text meant to be read. Flash
  the marker or border, not the text. [V: NUREG 1.3.10-9/-10; Rockwell]
- Give the operator acknowledge or flash suppression. [V: NUREG 1.3.10-13]
- One blink style system-wide; unacknowledged blinks, acknowledged is steady.
- Conflict: WCAG 2.3.1 allows no more than three flashes per second (seizure
  safety), while NUREG alarm guidance says 3-5 per second, and MIL-STD-1472H
  itself says to avoid bright pulsing at 1-30 Hz. Default (same as alarms.md):
  flash only a small marker, at about 2 Hz or below, only for unacknowledged
  high-priority alarms, and offer a steady alternative; decide per product and
  risk and document it. [V: 02 notes s8]
- No decorative animation. Spinning fans and flowing pipes keep moving after
  comms loss and give false assurance; stop state animation when quality is bad.
- State-change transitions under 200 ms; honour `prefers-reduced-motion`.
- Animation only for process-critical or safety activity. [V: ASM 3.2]

## 12. 2D vs 3D
Default flat 2D: no gradients, shadows or glossy realism; 3D adds no state information and competes with colour. ASM allows 3D "if depicted effectively" (3.6, priority 2), not a ban [V: ASM slides].
Counterpoint: an IEEE 2016 paper (abstract only) found interactive 3D plant-model visualisation improved problem detection, workload and accuracy over 2D (summary: ieeexplore 7560613). It concerns interactive exploration, not decorative symbols. Use 3D for spatial tasks (where is the head, collisions), 2D for status and control.

## 13. Showing data quality visually

Every live widget supports these states automatically; screens do not add them
by hand. (OPC/Ignition practice) [V: Ignition quality docs]

| State | Display |
|---|---|
| Good | normal rendering |
| Uncertain | value shown with a marker or changed style |
| Bad / error | dashes or "?", no pointer, no plausible number |
| Stale | age shown ("last 14:03"), hatched or greyed; no frozen "healthy" look |
| Pending write | pending badge on the control, state indicator unchanged |
| Simulated / forced / manual / bypassed | persistent symbol and word, not an alarm colour |
| Comms lost | one zone- or screen-level "NO DATA since HH:MM" banner, not hundreds of icons |

- Never show 0 or the last value as if good. A value from a dead link looks
  identical to a live one unless you design it not to.
- Disable controls on stale or lost data.
- Forced or bypassed values stay visible until cleared; a bypass left on is a
  classic accident precursor (verify).
- NUREG-0700 Rev 3 14.3-3/-4 require an indication when data are invalid or
  unvalidated [V]. The hatch-and-timestamp treatment is design synthesis.

## 14. Control states

Every control has: default, pressed (visible within 100 ms [V: Nielsen;
NUREG 11.3.2.3.6-7 max 100 ms, 55 ms preferred]), disabled, pending, failed.

| State | Treatment |
|---|---|
| Default | clear affordance, label with verb |
| Pressed | shown on touch-down; action fires on release |
| Disabled | greyed, still legible, never hidden; reason in the operator's words beside it or on tap [V: Rockwell] |
| Pending | on the control, same size, blocks re-entry; elapsed time or timeout, not an endless spinner |
| Failed | inline message with next step, not just a toast; no "Error 17" |
| Selected / armed | distinct, with auto-disarm timeout (see physical-and-environment.md) |

The process state indicator changes only on measured feedback; the control may
show pending at once. Show demand and actual separately where they differ.
Response feedback thresholds: 0.1 s instant, 1 s keep flow (show an indicator
beyond), 10 s attention limit (show progress and a way to interrupt) [V:
Nielsen]. Show a processing message beyond 1 s and a progress indicator beyond
10 s [V: MIL-STD-1472H 5.17.9.5.3, 5.17.9.9].

## 15. Vendor reference points
| Vendor | Known | Status |
|---|---|---|
| Rockwell PlantPAx PROCES-WP023 | RGB table, fonts, px sizes, levels, alarm-only bright colours | [V: full text] |
| ASM Consortium | 2009 guideline catalogue; 81 guidelines (2008), 64 (2013) | [V: slides]; full text unread |
| Ignition | grey base, alarm indicator by equipment, quality overlays | [V: docs] |
| Siemens WinCC Unified Template Suite | flat, one accent (0,161,209), greys; no ISA-101 or alarm colours; no HP-HMI guide | [V: entry 91174767 V3.1] |
| Emerson DeltaV Live | ISA-101 hierarchy, HP graphic elements | [V: product page] |
| AVEVA SA Library | reusable symbols, colour only for critical metrics; ISA-101 not claimed | [V: product page], vendor claims |
| ABB 800xA, B&R mapp View | classic/HP styles; web themes | (summary) search only |
| Beckhoff TwinCAT HMI | JSON `.theme` files; no guideline found | [V: Infosys] |

ISA-101, ISA-18.2, EEMUA 191, IEC 60073 and ISO 9241-303 were not read in normative text.

## 16. Common mistakes
- Colourful screens at rest, so colour no longer means anything.
- Red for running and green for stopped, or any hue with two meanings.
- Colour as the only carrier; red/green pairs.
- Light-grey secondary text under 4.5:1.
- Bare numbers with no unit, range or trend.
- Auto-scaled trends hiding a real excursion.
- Showing 0 or the last value after a dead link.
- Optimistic toggles that flip before the machine confirms.
- Blinking text, blinking everything, or several blink styles.
- Unsourced numbers ("5-7 choices (Hick)", "4-10 updates/s") quoted as rules.
- Sizing text in px on a desktop window instead of by visual angle on the panel.
- 10%/1% colour-blindness figures.

## 17. Sources
- NUREG-0700 Rev 3 draft (ML18158A333), Rev 3 (ML20162A214), Rev 4 2026 (ML26022A094), nrc.gov.
- MIL-STD-1472H (via FAA/Honeywell touch report); WCAG 2.2; APCA in a Nutshell.
- Birch 2012, JOSA A 29(3):313; Colour Blind Awareness; Nielsen response-time limits.
- Rockwell PROCES-WP023; ASM Display Guidelines slides (2009); Opto 22 white paper 2061.
- Ignition docs; Siemens 91174767; Emerson, AVEVA, Beckhoff pages.
