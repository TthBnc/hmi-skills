# Example: cable-driven UV-CIPP liner curing machine (generic class)

A sketch of how the skill's rules apply to a machine class: a drum plus a
motor-driven cable that pulls a UV light head, with camera, through a resin
liner while air pressure holds the liner against the pipe. This is a generic
class built from vendor and specification material, not any one product, and
it does not judge any existing implementation. Tags: `[V: source]`,
`(summary)`, `(verify)`. Patterns: `../patterns.md`.

## Context of use

- Truck or trailer at a manhole, outdoors, in sun, rain or dark. Crew of 2-3.
  Rugged touch panel (about 10 in) in a cab or under a canopy; wet, gloved
  hands (verify per site). Screen size and glove use are never assumed.
- Task: set up the project, check the machine, load the liner, run the cure,
  save the record. The cure takes minutes to hours; the record goes to an
  engineer or owner for acceptance.
- Process facts the UI must reflect: municipal specs require recording of
  project name, date and time, curing speed, light source and wattage, inner
  air pressure, inner temperatures and liner length (verify: source attribution from unpublished research; independently check the named source). The curing record is the deliverable.
- Light is a hazard: UV exposure and heat. Controller may sit away from the
  source (verify: source attribution from unpublished research; independently check the named source).

## States

| State | Meaning | Primary action |
| --- | --- | --- |
| Not ready | check failed or device missing | fix the listed item |
| Ready | all permissives met | Start step |
| Loading / Inverting | liner moves, air in | Stop |
| Curing | light on, head moving at set speed | Hold / Stop |
| Held (automatic or operator) | motion or light paused | Resume |
| Cooling / Complete | light off, pressure bleed-down | Finish and save |
| Fault / Emergency | machine safe state | Clear after cause removed |

Modes: Project (guided), Manual (test and maintenance), Service. Mode is in
the strip. Manual is gated and shows a banner (patterns §13). One enumerated
state; PackML-like acting vs wait states apply (patterns §18).

## Status strip

Connection to control unit and to head, project name, state with elapsed time,
mode, recording indicator, storage left, highest-priority fault, "UV ON" when
light is on, "motion enabled" when the drive can move. Fixed top.

## Main screen (curing)

```
+----------------------------------------------------------------------+
| Link OK | CURING 00:18:40 | Project: Main St 12 | REC | UV ON | !0     |
+----------------------------------------------------------------------+
| ALARM BANNER (empty when quiet)                                      |
+-------------------------------+--------------------------------------+
| FRONT CAMERA   [rear] [full]  | Position  46.2 of 120 m  [####-----] |
|  (live, age 0.1 s)            | Speed     0.80 m/min  (target 0.80)  |
|  overlay: m, speed, time      | Lamp      80 %  (520 W)  limit 650 W |
|                               | Liner temp  72 C  band 55-80 C   ^   |
|                               | Pressure  0.35 bar (hold 0.30-0.40)  |
|                               | ETA 13:42 at current speed           |
+-------------------------------+--------------------------------------+
| [ STOP ALL ]  [ Hold ]  Speed [-][+]  Lamp [-][+]   Log | Alarms | ..  |
+----------------------------------------------------------------------+
```

- Video stays visible; parameters sit in a strip beside it, never in a modal
  (verify: source attribution from unpublished research; independently check the named source).
- Each value shows target, limit band, unit and a sparkline on tap
  (patterns §6). Temperature is read as trend: a rise that levels off is a
  normal exotherm, a sudden spike means too slow or too hot (summary: NuFlow
  guide, vendor).
- Actual vs target speed is shown, with a "drag" or stall flag when the
  pulled distance and the commanded speed diverge (summary).
- Stop controls: a screen Stop plus separate physical stops for lamps and for
  the cable drum; the screen shows their state (verify: source attribution from unpublished research; independently check the named source).

## Alarms (priorities; rules in `../alarms.md`)

| Priority | Examples | Automatic response |
| --- | --- | --- |
| High (red) | emergency stop, hatch or guard open, drum overpressure, light-head over-temperature, loss of control link | outputs to safe state; light off; motion stop |
| Medium (amber) | pressure drifting out of band, lamp output low, temperature near limit, storage low, camera lost | operator ack; automatic pause at a threshold with stated resume |
| Info | speed trim logged, recording segment saved | message line |

Show automatic actions with reason and planned resume: "Paused: head 82 C
above 80 C. Resumes below 70 C at lower lamp power" (summary: patent US
12439493, vendor behaviour). Show degraded mode with an updated duration
("one lamp chain off, half speed, finish 15:10") (summary: Vortex split
chain). Alarm causes seen in vendor guidance: high temperature, lamp faults,
winch problems (verify: source attribution from unpublished research; independently check the named source).

## Critical actions

| Action | Treatment |
| --- | --- |
| Light on | explicit arm then act, warning and short visual countdown, interlocks (cooling, pressure) listed |
| Stop / emergency | physical, independent; screen Stop never confirmed |
| Speed trim during cure | small steps, limited range, logged; larger changes need supervisor (summary: NuFlow) |
| Change cure parameters | only after Hold; Apply shows before/after; locked while curing |
| Override an interlock | role, reason, visible marker, auto-expiry (patterns §4) |
| End and save | "Saving..." until the record is confirmed, then "Saved" |
| Delete a project | names it and what is removed; export first |

## Data quality

- Temperature, pressure and position each carry quality; a lost sensor shows
  dashes, never a plausible number [V: 02 §9].
- Untrusted telemetry (for example a head variant without a temperature
  channel) is hidden or marked "not available", not zero.
- Camera: frame age and "No signal" state; the cure may continue only if the
  spec allows it (verify with the spec).
- Pre-flight checks start as "Not checked", not "passed".
- Startup: wait for the first real board frame before judging pressure.
- Link loss: strip shows time since loss; values greyed; do not assume the
  outputs stopped. Plan for a force-off on loss of communication in the
  firmware, not only the screen (verify on the actual machine).

## Records

One data model for the live screen and the report. Log at least 1 s for speed,
position, lamp power, temperatures, pressure, plus state changes, alarms,
operator actions and notes, with video; tamper-evident; export as PDF and by
USB (verify: source attribution from unpublished research; independently check the named source). History plays the cure against its video
on one timeline (verify: source attribution from unpublished research; independently check the named source). Lamp hours and wear appear in the
next pre-flight check (summary, IBG RFID).

## Top pitfalls

1. Record optional or hidden; recording failure unannounced.
2. No always-visible status strip: connection, mode and fault in toasts only.
3. Socket or link loss replaces the whole UI.
4. Stale values or camera frames that look live.
5. Pre-flight items pre-marked as passed.
6. Disabled buttons with no reason.
7. Parameter edits mid-cure that apply instantly.
8. Colour as the only difference; several reds; text too small outdoors.
9. Client-side PIN or admin mode treated as security.
10. A hold-to-run or enabling input missing for motion, or stop not
    independent of the touch computer.
11. Labels clipped in other languages on fixed-size buttons.
12. No units or limits next to temperature, pressure and lamp power.
