# Example: vision inspection station (counting / presence check)

A sketch of how the skill's rules apply to one machine type. Illustrative, not
a spec. Tags: `[V: source]`, `(summary)`, `(verify)`. Patterns: `../patterns.md`.

## Context of use

- Fixed station on a line or bench. Operator stands 0.5-1 m from a 10-15 in
  touch screen, often gloved, under variable shop lighting (verify on site).
- Task: place a part or tray, the camera counts or checks items against an
  expected set, operator accepts, corrects or rejects, next part. Cycle time
  seconds; hundreds of cycles per shift.
- Operators are trained on the product, not on vision software. Supervisor
  sets recipes; operator never edits thresholds.

## States

| State | Meaning | Strip text |
| --- | --- | --- |
| Not ready | camera, light or model missing | "Camera not connected" |
| Ready | waiting for a part | "Ready" |
| Inspecting | frame captured, model running | "Inspecting..." |
| Result | decision shown with evidence | "Pass" / "Check" |
| Held | image frozen for correction | "FROZEN - correcting" |
| Fault | machine problem, not a part problem | fault text |

Use one enumeration. Held is a mode: distinct colour, "FROZEN" label on the
image and in the strip, live values hidden (patterns §11).

## Status strip

Left to right: connection (camera, light, PLC/line), state, recipe and
version ("Tray 8 / v3"), counts for the shift (good, check, rejected), storage
or queue warning, highest-priority fault. Fixed top, always visible.

## Main screen

```
+----------------------------------------------------------------------+
| Camera OK | Ready | Tray 8 v3 | Shift: 412 good 9 check | Fault: --  |
+----------------------------------------------------------------------+
| ALARM BANNER (empty when quiet)                                      |
+----------------------------------+-----------------------------------+
|                                  |  FOUND  7 of 8 expected   CHECK   |
|   LIVE IMAGE with overlays       |  [########-]  missing: slot 5     |
|   boxes on found items,          |  by type:  A 4/4   B 3/4          |
|   dashed box where missing       |  stable for 2.1 s (needs 3 s)     |
|                                  |                                   |
|   frame age: live 0.2 s         |  Image age 0.2 s   Model v1.4     |
+----------------------------------+-----------------------------------+
| [Freeze & correct]   [ Accept ]   [ Reject ]          [Records]  [..]|
+----------------------------------------------------------------------+
```

- Result panel states: Confirmed (stable N s and equals expected), Settling
  (count changing), Check (differs from expected or low agreement), Not
  running (patterns §10). Never a raw probability.
- Count is shown against the expected number and per type, with a bar and the
  missing positions marked on the image, not only a number.
- Accept sits in the fixed primary position; it is disabled in Settling with
  the reason "Wait 3 s for a stable count".
- Correction screen: large per-item choices, one tap for "whole result is
  correct", original vs corrected side by side, undo until saved.

## Alarms (priorities; rules in `../alarms.md`)

| Priority | Examples | Behaviour |
| --- | --- | --- |
| High (red) | camera lost during a cycle, light failed, model failed to load | banner, sound, blocks Accept, stays until resolved |
| Medium (amber) | image too dark, lens dirty, reject rate above limit, queue nearly full | banner, acknowledge, no sound |
| Info | recipe changed, report exported | message line, no alarm |

Reject rate and drift are process alarms for a supervisor. Each message says
what happened and what to do ("Image too dark. Check the lamp or the cover.").

## Critical actions

| Action | Treatment |
| --- | --- |
| Accept / Reject | one tap, large, fixed position, no confirmation; undo window of a few seconds |
| Discard a held correction | confirmation naming the part |
| Change recipe | blocked while a part is in progress; diff shown; supervisor role |
| Stop line | physical stop wired to the line, not the screen (verify with safety engineer) |
| Delete records | names the date range, cannot be undone |

## Data quality

- Image: show age; after about 1-2 s without a new frame mark "No new image"
  and disable Accept.
- Camera disconnected: "No camera signal", last frame greyed, retry visible.
- Counts from a stale or settling image are never counted as good.
- Placeholder or test images are labelled; a default 0 is never "0 found".
- Model version and recipe version recorded with every result.

## Records

Per part: time, recipe version, expected vs found, per-type counts, decision,
who corrected what, image path. Corrections are logged. CSV export with a
visible progress.

## Top pitfalls

1. A frozen image that looks live (no FROZEN label).
2. Confidence percentages instead of rule-based states.
3. Accept enabled while the count is still changing.
4. Missing items shown only as a smaller number, not located on the image.
5. Lost correction history when the part is rejected afterwards.
6. Operator can edit thresholds on the production screen.
7. Alarm for every dark frame (floods); group and suppress.
8. Colour-only pass/fail with no word or icon.
9. Camera loss handled by a spinner over the entire UI.
10. Result counted before the operator saw it, with no undo.
