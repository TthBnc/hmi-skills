# HMI review checklist

Contents: how to review · S safety · A state & mode · D data & commands ·
L alarms · V visual · T touch & physical · C content · P patterns ·
X architecture & security · R process · reporting.

## How to review

- Walk every screen in every state, not just the happy path: idle, starting,
  running, held, stopping, faulted, disconnected, stale, empty, no permission.
- Mark each item **pass**, **fail** (with file:line or screenshot), or
  **not verified** (with the reason, e.g. "needs device test").
- Never pass sizing, legibility, glove use, sunlight or sound from code or a
  desktop window alone.
- Severity of a fail: **S1 Safety** (could injure or damage), **S2 Operator
  error** (wrong action or missed state likely), **S3 Efficiency**, **S4
  Consistency/cosmetic**. Items marked ★ are S1/S2 by default.

## S. Safety boundary → safety-boundary.md

- [ ] ★ No safety function (e-stop, guard, safety stop reset) is implemented
      only in HMI software.
- [ ] ★ E-stop is a physical, red-on-yellow control; the screen shows its
      state but cannot reset a safety stop.
- [ ] ★ Motion that can hurt someone needs a held control or enabling device.
      A single tap that starts motion with no hold is justified in writing.
- [ ] ★ Loss of the HMI or link brings the machine to a defined safe state by
      itself; the screen says which.
- [ ] Interlocks and permissives are shown with the reason a control is blocked.
- [ ] Stop is never behind a confirmation, menu or scroll.

## A. State and mode → states-and-commands.md

- [ ] ★ A fixed status strip on every screen shows connection, machine state,
      active mode and the highest-priority active alarm.
- [ ] ★ Modes (manual/auto/maintenance/simulation/playback) look different
      everywhere, not just in a label; simulated data can never be mistaken
      for live data.
- [ ] Every state in the machine state model has a designed screen state.
- [ ] Mode changes are announced; automation never changes level silently.

## D. Data quality and commands → states-and-commands.md

- [ ] ★ Stale, bad, uncertain, forced and simulated values are visually marked
      and show their age; unknown is never shown as 0 or blank-as-normal.
- [ ] ★ Indicators show the measured state, not the command sent.
- [ ] ★ Commands show pressed (≤100 ms), pending, confirmed-by-machine, or a
      failure/timeout with the next step; no optimistic success.
- [ ] Double-submit is impossible (debounce, idempotent command IDs).
- [ ] When several clients connect, it is clear who has control; view-only
      clients cannot command.
- [ ] Live video shows frame age or freeze, and has a no-signal state.
- [ ] Update rates are throttled to readable values; numbers do not flicker.

## L. Alarms → alarms.md

- [ ] ★ Every alarm has a defined operator action and time to respond; the
      rest are status or log entries.
- [ ] ★ 3-4 priorities at most, each with an exclusive colour, shape and sound.
- [ ] Alarm states (unacknowledged, acknowledged, cleared-unacknowledged,
      shelved, suppressed) look different; shelving is time-limited and logged.
- [ ] Messages say what happened, the consequence, what to do and where.
      Codes sit in technical details.
- [ ] Flood handling: startup/state-based suppression, grouping, first-out.
- [ ] Faults are not shown only as toasts that disappear.
- [ ] Alarms and operator actions go to an audit log with time and user.

## V. Visual language → visual-language.md

- [ ] Normal operation is mostly neutral; saturated colour only for
      abnormal states and modes; one meaning per colour.
- [ ] ★ No information carried by colour alone (check with a CVD simulator).
- [ ] Contrast: text 4.5:1+ (aim 6-7:1 for key values), UI shapes 3:1+.
      Run `scripts/contrast.py`.
- [ ] Key values show unit, range or target, and trend access; precision
      matches what the measurement supports.
- [ ] Updating numbers use tabular figures.
- [ ] Trends do not silently auto-scale away meaningful change; setpoints and
      limits are drawn.
- [ ] Blinking only for unacknowledged urgent alarms.
- [ ] No decorative 3D, gradients or heavy shadows.
- [ ] Styles come from tokens. Run `scripts/lint_tokens.py`.

## T. Touch, physical and environment → physical-and-environment.md

- [ ] Targets meet the size table for the real panel and gloves (about 20 mm+
      gloved primary). Run `scripts/sizing.py`. ⚠ device test.
- [ ] Separation 3-6 mm+, more between destructive and frequent actions.
- [ ] Act on release; visible pressed state; no hover-only affordance.
- [ ] Text at least 16 arcmin (20-22 preferred) at the real distance.
      ⚠ device test.
- [ ] On-screen and physical direction of motion match the machine.
- [ ] Sunlight, night/dimming, vibration and audible-alarm loudness are
      considered for the real environment. ⚠ field test.
- [ ] Localisation: no truncation at about 30% text expansion; RTL layout if
      RTL languages ship; locale number, date and unit formats.

## C. Content → patterns.md

- [ ] No internal IDs, enum names, versions, paths, stack traces or codes in
      the main view.
- [ ] Disabled controls say why; empty states give the next action.
- [ ] Confirmations only for irreversible actions, naming object and verb;
      the safe choice is the default.
- [ ] The same verb is used through the flow (Start cure → Curing → Cure saved).

## P. Patterns → patterns.md

- [ ] Display hierarchy: any detail within one or two taps of the overview.
- [ ] Primary action is in a fixed place and is the largest control.
- [ ] Setpoint entry shows range, units and current vs new; validated before
      apply.
- [ ] Setup and settings are separate from run screens and role-gated.
- [ ] Automation output shows its evidence, rule-based confidence and a fast
      correction path.

## X. Architecture and security → architecture-and-security.md

- [ ] ★ No shared or hard-coded passwords or PINs; per-user roles; admin
      functions are logged.
- [ ] Remote access is view-only by default; remote control is explicit and
      visible on the local screen.
- [ ] HMI and firmware versions are checked for compatibility; updates can be
      rolled back.
- [ ] Kiosk lockdown: no OS chrome or escape paths for operators.
- [ ] A simulation/mock mode exists and is visibly marked.
- [ ] State and label logic have unit tests; critical flows have UI or HIL
      tests.

## R. Process → process.md

- [ ] Context of use is written down (operators, tasks, environment).
- [ ] An HMI philosophy and style guide exist and match the implementation.
- [ ] A use-error risk analysis covers the critical tasks.
- [ ] Tested with real operators on the real device, including abnormal
      scenarios.

## Reporting

List fails by severity (S1 first), then the "not verified" items with the test
that would settle each. Close with the 3-5 changes that would most reduce
risk.
