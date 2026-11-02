# HMI patterns

General patterns for operator screens. Adapt names and pages to the machine;
keep the structure.

## Screen frame

- **Status strip (fixed, top):** connection, run state with elapsed time where
  it matters, active mode, resource warnings (storage, battery, consumables) and
  the highest-priority active fault. Tapping a fault opens its detail.
- **Navigation:** few, large, labelled destinations; the current one is
  unmistakable. Navigation that would lose work (an active run, unsaved edits)
  is guarded or disabled, with the reason shown.
- **Action area:** the screen's primary action in a fixed position (bottom or
  the side of the dominant hand) so the hand learns where it is.

## Display hierarchy (ISA-101 levels)

| Level | Purpose | Typical screen |
| --- | --- | --- |
| 1 | overview of the whole operation | the run/operate screen |
| 2 | control of one unit or task | a task screen with its primary action |
| 3 | detail and diagnostics | history, logs, item detail |
| 4 | help and technical support | technical details, manuals |

Any detail is reachable in one or two taps from the overview.

## Setup as a checklist

- Show each prerequisite with a state word (Ready, Needs attention, Not needed
  for this task) and one button for the next thing to do. Say which tasks need
  which steps.
- Device selection offers only usable devices and only modes they support,
  with a picker; a failure says why in operator terms and offers the fix on the
  same screen.

## Running a task (start/stop)

- The live view or main value dominates; overlays show only what the operator
  needs for the task.
- Start/stop is the largest control. While running, the button changes to Stop
  (danger styling), the status strip shows the run state and elapsed time, and
  the main view has a distinct running treatment (a border or band).
- Show "Stopping..." until the controller confirms stopped. Record saving is
  a separate state: "Saving...", then "Saved" after persistence is confirmed.
- Optional metadata is pre-filled from the last run and never required to start.
- Notes during a run are one tap plus a short form, timestamped automatically.

## Live values

- Show each value with its context: unit, expected or target value, normal
  range, and a trend one tap away ("7 of 8 expected", a bar against limits).
- Choose numeric display cadence for the task and process. Label any smoothing;
  do not delay alarm, machine-state or data-quality updates.
- Stale data is marked as stale (greyed, "last updated 12 s ago"), never shown
  as if live.

## Automation and model output

- Show the result with its evidence (the image with overlays, the per-type
  breakdown, the reading behind the decision).
- Use a few states with rules behind them (for example: Confirmed, Settling,
  Check, Not running), not raw probabilities.
- When automation is unavailable, say so and what is needed, instead of empty
  panels.

## Hold, review and correct

- A held/frozen/review state is a mode: distinct colour and label on the view
  and in the status strip; live values are hidden or marked as not live.
- Corrections are large, labelled choices per item plus a fastest path for
  "the whole result is correct".
- Show original vs corrected side by side; every correction is undoable until
  saved; saving returns to live with a confirmation.
- Playback of recorded data is also a mode, with its own label and touch-sized
  play/pause/seek.

## History and records

- Lists with plain columns: when, duration, who, outcome, size, notes. IDs only
  in a technical section of the detail view.
- Deleting names the record and says it cannot be undone.

## Alerts

- Only interrupt for conditions that need operator action; everything else is
  status or log (ISA-18.2).
- At most three priorities: Fault (red, remains visible while active, even after acknowledgement),
  Warning (amber), Info (neutral, auto-dismisses). Critical faults while the
  operator is looking at the work may also use sound.
- Acknowledged and unacknowledged alerts look different. Avoid floods: group
  repeats and suppress consequences of an already-shown cause.
- Format: what happened, why if known, what to do. "Camera disconnected during
  the run. The first 42 s were saved. Reconnect it and start a new run." Codes
  go in technical details.

## Confirmations

- Only for irreversible actions (delete, discard unsaved work, reset).
- The title names the object; the destructive button names the verb ("Delete
  run from 10:42"); the safe choice is the default and further from the hand.
- Hold-to-confirm is an alternative when it shows progress and cancels on
  release. Stop and emergency actions are never confirmed.

## Wording

- One sentence of help per panel at most; details behind "More".
- The operator's words, not the system's (no "epoch", "manifest", "payload",
  "bundle", "generation").
- The same verb everywhere: "Start run" -> "Running" -> "Run saved".
- Disabled controls say why ("Connect the camera first"). Empty states give the
  next action. Errors state the fix without apologising.
