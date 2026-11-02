# Example: packaging line (PackML states)

A sketch of how the skill's rules apply to one machine type. Illustrative, not
a spec. Tags: `[V: source]`, `(summary)`, `(verify)`. Patterns: `../patterns.md`.

## Context of use

- A filler-capper-labeller-packer line with 4-8 machines under one line
  controller. Panel on each machine plus a line overview at a supervisor
  station. Noisy hall, gloved hands, mixed lighting (verify).
- Operators start, stop, clear jams, change over products, refill materials.
  Technicians handle recipes, I/O and faults. Shifts run hours; stops cost
  money, so every minute of downtime is categorised.

## States and modes (PackML)

PackML has 17 states: wait states Idle, Stopped, Suspended, Held, Complete,
Aborted; acting states Resetting, Starting, Stopping, Aborting, Clearing,
Holding, Unholding, Suspending, Unsuspending, Completing; and Execute as the
dual state. Power-up lands in Stopped; Reset goes to Idle; Start to Execute
[V: ISA-TR88.00.02; OPC UA StateEnumeration].

| State | Operator meaning | Show |
| --- | --- | --- |
| Stopped | safe, nothing running | grey; primary action Reset |
| Idle | ready | "Ready", Start |
| Execute | producing | green only if the site style guide says so; else neutral with a running band |
| Held | operator paused | "Held by operator", Unhold |
| Suspended | external cause (starved, blocked) | amber, cause named ("No caps") |
| Aborted | e-stop or door | red, cause, Clear |

Modes: Production, Maintenance, Manual (names from PackML) (summary). Mode is
always in the strip; state availability depends on mode. Only the commands
valid now are enabled; disabled ones say why.

## Status strip

Machine name, mode, state with time-in-state, active recipe, good and reject
counts, speed vs target, highest alarm. Fixed top. State and mode are never
covered.

## Main screen

```
+----------------------------------------------------------------------+
| Labeller 3 | PRODUCTION | EXECUTE 00:42:10 | Recipe: 500ml / v12 | !1 |
+----------------------------------------------------------------------+
| ALARM: Label roll low (Medium)  14:02   [Ack]                        |
+---------------------------------+------------------------------------+
|  Line speed   180 / 200 ppm     |  Good 12,480   Reject 31 (0.25 %)  |
|  [=========-] target 200        |  Order 14,000   ETA 14:35          |
|  Infeed  OK  Outfeed  OK        |  OEE  81 %   (A 92 P 90 Q 98)      |
|  Material: labels 14 min left   |  Downtime today 22 min             |
+---------------------------------+------------------------------------+
| [ STOP ]   [ Hold ]   [ Reset ]  [ Start ]      Alarms | Recipe | Diag |
+----------------------------------------------------------------------+
```

- Large Start/Stop/Reset/Hold in a fixed row; Stop never confirmed.
- Material levels show time left, not a bare percentage, with warning limits.
- Line overview: each machine a tile with state colour plus word, so a
  starved or blocked machine stands out (summary).

## Alarms (priorities; rules in `../alarms.md`)

| Priority | Examples | Behaviour |
| --- | --- | --- |
| High | e-stop, guard open, overpressure, safety relay fault | red banner, sound, stays; causes Aborting |
| Medium | label roll low, reject rate above limit, motor load high | amber, acknowledge, cause and action text |
| Low/Info | recipe changed, changeover complete | log or message line |

Cause first: a starved infeed suppresses the downstream "no product" alarms.
Target: fewer than 1 new alarm per 10 minutes in steady state; 10 or more in 10
minutes is a flood (summary, EEMUA 191 via secondary sources).

## Critical actions

| Action | Treatment |
| --- | --- |
| Stop / Hold | immediate, no confirm; physical e-stop independent |
| Start after Aborted/Stopped | requires Clear then Reset, then Start; guards shown |
| Recipe change | only in Idle/Stopped; diff; role; reason logged |
| Bypass a guard or sensor | maintenance mode, key or role, visible "bypassed" marker, auto-expiry |
| Jog or manual outputs | Manual mode only, hold-to-run, interlocks apply |
| Reset counters | confirmation naming the counter |

## Data quality

- Counters from a lost PLC link are "last known 14:02", not live.
- Rates are averaged over a stated window; show it.
- Sensor "not yet received" is a dash, never 0 ppm.
- Forced or simulated I/O flagged; listed on an overrides page.

## Records

Order, recipe, start/end, good, reject, downtime reasons with cause category,
alarms with time and acknowledgement, operator or role. Downtime reason is
asked at the next Start, not mid-incident; "unknown" is allowed.

## Top pitfalls

1. Hiding state and mode behind a menu.
2. Showing Start while it is not legal and failing silently.
3. Free-form state names that differ between machines (use one vocabulary).
4. Held and Suspended shown identically (operator vs external cause).
5. Alarm floods from one starved sensor; no consequence suppression.
6. Recipes changeable while running.
7. Bypass left on with no marker.
8. OEE as a lone big number with no breakdown or cause.
9. Colour-only state tiles.
10. Counters showing 0 on comms loss.
