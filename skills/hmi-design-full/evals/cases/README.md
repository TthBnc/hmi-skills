# Behaviour eval cases

Run each case twice (with and without the skill) and grade the answer against
its expected findings. A case passes when every **must** item is present and no
**must not** item appears. Compare pass rates; the skill earns its place only
if it clearly beats the baseline.

## Case 1: comms loss

Prompt: "Our machine UI replaces the whole screen with a spinner when the
websocket to the controller drops, then restores it on reconnect. Review this."

- must: last known values stay visible but marked stale with their age;
  a status strip shows "Connection lost" with time since; the screen states
  what the machine does by itself (failsafe), not only that the UI is waiting.
- must: say that the machine-side failsafe must not depend on the HMI.
- must not: recommend keeping the spinner as the main fix.

## Case 2: e-stop on a tablet

Prompt: "Add an emergency stop button to our wireless tablet app that controls
a winch."

- must: state that a screen button is not an emergency stop. E-stop is a
  hardwired, safety-rated control (ISO 13850 / IEC 60204-1). The tablet may
  offer a normal stop and show e-stop status.
- must: mention wireless-specific behaviour (loss of link must stop or hold
  the machine safely).
- must not: design a confirmation dialog on any stop.

## Case 3: alarm flood

Prompt: "Startup produces about 60 alarms in two minutes on our curing unit.
Operators just acknowledge them all."

- must: rationalise alarms (each needs an operator action, consequence and
  time to respond); suppress alarms that are expected for the startup state;
  give a priority distribution target (cited, with its verification status);
  add first-out or grouping.
- must: identify the habituation risk.

## Case 4: setpoint entry

Prompt: "Design the screen where the operator sets UV lamp power and travel
speed before a cure."

- must: show units, allowed range and current versus new values; validate
  before apply; Apply/Cancel; log the change with the user; confirm only if
  the change is irreversible or outside the recommended range.
- must: size the targets for gloves (about 20 mm) and use tabular numerals.

## Case 5: full review (repository)

Prompt: "Review the operator frontend in this repo against HMI best
practice." (Use a real repository.)

- must: findings ranked Safety → Operator error → Efficiency → Cosmetic, each
  with file:line, the rule broken and the fix.
- must: mark legibility and glove use as "needs device test", not as passed.
- must: flag shared or hard-coded credentials as a security finding if present.
