# Safety boundary: what a screen may and may not do

Contents
1. The core rule and the regulatory frame
2. Emergency stop
3. Reset, enabling devices, hold-to-run
4. Showing interlocks and permissives
5. Wireless and remote control
6. Physical vs on-screen (table)
7. Use-error risk ordering
8. Review procedure, common mistakes, sources

Tags: `[V: source, clause]` read in the research; `(summary)` secondary source
only; `(verify)` unverified, check before relying on it. Nothing here is legal
advice. The required performance level for any function comes from the machine's
own risk assessment, never from this file.

## 1. The core rule and the regulatory frame

**Rule:** The HMI is never the safety layer. Every safety function must work with
the screen dead, frozen, rebooting, cracked or wiped by a cleaning cloth.

**Why:** Touch panels, operating systems and web stacks are standard,
non-certified components. One author's analysis (summary) is that an ordinary HMI
plus a standard PLC reaches Category B / PL b at best, while an e-stop needs at
least PL c. A screen also fails silently: a frozen frame looks like a live one.

**How to check:** Pull the screen's power and kill its process while the machine
runs. Every stop, guard and enable function must still work, and the machine must
reach a safe state without the screen.

What the screen does with safety:
- **Display** the status of the safety chain (e-stop pressed, guard open, enabling
  device held, safe torque off active). This is read-only.
- **Request** non-safety functions (start a programme, change a setpoint).
- **Never** perform, release, bypass, reset or be relied upon for a safety
  function. The only exception: certified safety touch hardware, treated as part of
  the safety-related control system with a documented PL (summary: such hardware
  exists, e.g. PL d marketed). That is a machine-builder decision, not a UI choice.

### Standards map (what each is for)

| Standard / law | Concern | Binding? | Confidence |
|---|---|---|---|
| ISO 12100 | Risk assessment; three-step risk reduction | Harmonised in EU | (summary) |
| ISO 13849-1 | Safety-related control parts; PL a-e, categories B,1,2,3,4 | Harmonised in EU | (summary) |
| IEC 62061 | SIL-based functional safety of electrical control systems | Harmonised in EU | (summary) |
| ISO 13850 | Emergency stop function, design principles | Harmonised in EU | scope [V: catalogue abstract]; details (summary) |
| IEC 60204-1 | Electrical equipment of machines; stop categories, colours, e-stop devices | Harmonised in EU | (summary) |
| Regulation (EU) 2023/1230 | Machinery law for EU market | Yes | applies from 2027-01-20 (summary); verify on EUR-Lex |

- ISO 13849-1 and IEC 62061 are alternative routes to the same goal; which one a
  machine uses follows its product standard or sector habit (summary). A designer
  of screens does not choose; the safety engineer does.
- The Regulation replaces Directive 2006/42/EC and binds the machine builder. The
  HMI is part of the control system and the instructions, not a separate object
  (summary). Annex III clauses that touch screens: ergonomics (1.1.6),
  protection against corruption of safety software and data (1.1.9), control
  system safety including resistance to malicious attempts (1.2.1) (summary).
  Exact wording and one source's alternative date for some parts: (verify).
- If you do not know the market or the harmonised standards that apply, say so in
  the review and ask for the risk assessment. Do not invent a PL.

## 2. Emergency stop

**Rule:** The e-stop is a physical, latching, hard-wired device. A software
e-stop button may exist only as an additional, non-safety "stop" shortcut and must
never be labelled or styled as the emergency stop.

Facts (all (summary) unless marked; the standards are paywalled):
- Red actuator on a yellow background where a background exists; the red-on-yellow
  pairing is reserved for emergency devices. Symbol IEC 60417-5638.
- Direct physical action (press or pull), easily reachable, available and
  effective in all operating modes, overriding other functions.
- Latching; reset is manual and only permits a restart, never causes one.
- Fail-safe: a component failure results in a stop.
- Minimum PL c or SIL 1, more if the risk assessment says so. The PL is risk-based,
  so never treat "c" as a ceiling.
- Stop category 0 = uncontrolled stop, power removed at once. Category 1 =
  controlled stop with power kept for braking, then removed. Category 2 =
  controlled stop with power kept. Emergency stop uses 0 or 1, chosen by risk
  assessment.
- The e-stop complements guarding and safe design; it does not replace them
  (ISO 13850 clause 4.1.1.3, as cited in the research (summary)).
- An enabling device is not an e-stop; if wired into the e-stop circuit, e-stop
  requirements apply (vendor document, summary).
- An area-stop button must not look like an e-stop (summary).

Screen consequences:
1. Show e-stop state on every screen in the fixed status area: "Emergency stop
   pressed: release at the machine, then reset". Redundant with the physical lamp.
2. Never place a confirmation on stop actions. Stop is always one touch.
3. Do not use red-on-yellow or a mushroom shape for any on-screen control.
4. A screen "Stop" or "Hold" is allowed and useful (a stop request is safe), but
   its state must come from the controller, and the label must not imply it is the
   emergency stop.
5. If the screen cannot be seen or reached, the physical device must still be
   within reach at every operator position, including remote or teleoperation
   stations.

## 3. Reset, enabling devices, hold-to-run

### 3.1 Safety reset

**Rule:** A screen must not reset a safety stop (e-stop, guard interlock, safe
torque off). Reset is a separate, deliberate physical action at a place with a
view of the danger zone, never combined with start.

**Why:** A manual reset must be its own control device connected to the safety
system and must not weaken its PL (one author's reasoning, summary). An e-stop
reset only permits restart (summary). A commenter cited vendor guidance allowing
screen reset under conditions; the same author still advised a physical device.
Treat this as a risk-assessment decision, default to physical.

**How the screen helps:** Show the stop as "reset required at machine" with the
cause. After the physical reset, the machine goes to a stopped/idle state and
waits for a separate, ordinary start (see states-and-commands.md). Reset signals
are best evaluated on release (falling edge) so a stuck button cannot reset
(summary).

### 3.2 Enabling device (three-position)

For manual motion in a hazard zone (pendants, jogging):
- Released = motion stopped. Middle (light press) = motion allowed. Full squeeze
  = motion stopped. [V: Universal Robots 3PE Teach Pendant guide, section 8.1].
- Motion buttons are active only in manual mode (same source).
- After release or full squeeze, the system needs a deliberate re-enable; a
  held-over press must not resume motion (ABB behaviour via search summaries; the
  research flags the mapping to a "motors off" state as (verify) for other brands).
- An enabling device may be a pendant feature or a separate belt/bar; either way it
  is hardware, not a touch zone.

### 3.3 Hold-to-run and jog

**Rule:** Motion that can injure or damage (jog, cable feed, boom) runs only while
a control is held and stops on release, on loss of signal and on loss of comms.
Preferably the held control is hard-wired; if it is on a screen, the machine must
stop by itself when the heartbeat stops (see states-and-commands.md, comms loss)
and the machine side must also bound speed and travel.

- A touch hold is weak: a wet screen, a glove or a dropped tablet can leave a
  phantom or lost touch. Do not use a touch hold as the only enabling action for
  hazardous motion.
- Hold-to-confirm for non-motion actions (about 1 s) is a different pattern; it
  guards against taps, not against hazards. Duration 0.7-2 s is practice
  (verify).
- Two-hand control for hazardous starts is hardware-level (ISO 13851 named in the
  research; clause text not read) (verify).

## 4. Displaying interlocks and permissives

**Rule:** Every blocked control tells the operator why, in operator words, at the
point of use.

**Why:** A grey button with no reason is the classic frustration and drives
bypassing. Touch has no hover, so the reason must be visible or one tap away.

**How to check:** For each disabled control, name the blocking condition on
screen. Walk every interlock in the machine's list and verify each one appears.

Pattern:
- Show permissives as a short checklist beside the control: guards closed, e-stop
  released, pressure in range, mode = Auto, link good. Each row is OK / NOT OK
  with the live value, and the first blocking one is highlighted ("first-out").
- Distinguish four states: Ready (all met), Running, Not ready (list why), Fault.
- Keep the disabled control legible; allow tap-to-explain ("Cannot start: guard
  open") rather than ignoring the touch.
- Role-based blocks say so: "Requires supervisor".
- The screen shows the interlock; it never evaluates it. The controller
  or safety relay decides. A permissive that is calculated only in the UI is a
  display, not a protection.
- Bypassed, forced or simulated interlocks stay visible while active: persistent
  symbol, not an alarm colour, plus who set it and when. A safety bypass left on
  is a classic accident precursor (summary).
- Do not show "safe" from the absence of a signal. A missing or stale status is
  "unknown", never "OK" (see states-and-commands.md, data quality).

## 5. Wireless and remote control

- Whether a handheld or wireless terminal with e-stop or enabling device reaches a
  required PL (e.g. PL d) and satisfies ISO 13850 depends on the manufacturer's
  certified safety function and your own calculation. The research could not
  confirm any generic claim. (verify with the supplier)
- Wireless e-stop and enabling functions need a monitored link: on loss, stop
  (category 0 or 1 by risk assessment), not freeze. Display link quality and a
  clear "control link lost: machine stopped" state.
- Consumer tablets and gamepads are not safety devices. A rugged radio remote
  with built-in e-stop is a product with a certificate; a tablet app is not.
- A remote operator cannot see the hazard zone. Add independent presence or
  camera confirmation, speed limits, and local priority: whoever stands at the
  machine outranks the remote station (see control arbitration).
- On link loss, controller sleep or stick fault, the command must fall to zero by
  design (fail-safe default), and the screen must show link status. [Source: 05,
  section 2.3, practice] (summary)
- Remote start is more dangerous than remote stop. Allow stop/hold from any
  client; require control and local confirmation for start and mode change.

## 6. Physical vs on-screen

| Function | Physical (hard-wired / certified)? | On-screen allowed? | Confidence |
|---|---|---|---|
| Emergency stop | Yes, latching, red on yellow, cuts power independently of software | Status only; no software e-stop | ISO 13850 scope [V: catalogue abstract]; rest (summary) |
| Enabling device (3-position) | Yes, for manual hazardous motion | Status only (held / not held) | behaviour [V: UR 3PE guide s8.1] |
| Safety reset (e-stop, guard, STO) | Yes, separate deliberate action with view of the danger zone | Status and instruction only | (summary, one author) |
| Hold-to-run / jog of hazardous motion | Preferably yes; else continuous hold plus controller-side watchdog | Allowed only with watchdog and bounded speed/travel | (verify) |
| Mode selector for hazardous modes | Key switch or equivalent access control | Show mode; changing to maintenance needs physical access control | (verify) |
| Two-hand start of hazardous cycle | Yes | No | (verify) |
| Guard interlock | Yes | Status only | (summary) |
| Safety beacon / horn | Independent of screen if safety-relevant | Mirror only | (verify) |
| Start of ordinary cycle | Not required | Yes, after permissives are met | practice |
| Setpoints, recipes, parameters inside safe limits | No | Yes, with limits enforced by the controller | practice |
| Pause, hold, stop request | No | Yes, from any client | practice |
| Alarm display, acknowledge | No | Yes (acknowledge never clears a safety stop) | practice |
| Diagnostics, logs, trends, help | No | Yes | practice |

Default when unsure: put it on the physical side and show its status on screen.

## 7. Use-error risk ordering

Use-error means an operator action that differs from what the designer intended,
including foreseeable mistakes. Risk reduction follows the ISO 12100 order
(three-step method, summary):

1. **Design out.** Make the dangerous mistake impossible. Examples: motion limits
   and speed caps in the controller; a command that is simply not offered in this
   state; separate physical placement of start and reset; one-way sequences; an
   interlock the screen cannot override.
2. **Guard.** Add a barrier the operator must deliberately pass: physical guards,
   key switches, hold-to-confirm, select-then-operate with auto-disarm timeout,
   role gating, spacing and shielding of touch targets. Confirmation dialogs belong
   here and are weak (habituation: operators tap OK reflexively); use them only for
   rare, irreversible, non-urgent actions and name the object and effect.
3. **Warn.** Messages, colour, wording, training, manuals. Information for use is
   the weakest step and must not replace steps 1 and 2.

**Rule:** When a review finds a dangerous use-error, fix it at the highest step
that is feasible. A warning label on a screen that allows the error is not a fix.

Also list hazards the HMI itself creates: confusing mode display, ambiguous
labels, stale values, a touch that moves a machine. They belong in the machine's
risk assessment. For medical devices the equivalent is IEC 62366-1 and
critical-task testing (summary).

## 8. Review procedure

1. List every function that can hurt a person or damage the machine. For each,
   find the physical device or controller logic that protects it.
2. Remove any case where the screen is the only protection.
3. Confirm e-stop, enable, reset and guard status are shown from controller
   feedback, on every screen, and nothing is simulated by the UI.
4. Confirm every blocked control states its reason.
5. Confirm link-loss behaviour: machine stops by itself; screen says so.
6. Record gaps for the safety engineer rather than deciding a PL.

## Common mistakes

- A touchscreen "emergency stop" button, or any red-on-yellow control on screen.
- A "Reset" or "Clear fault" button that also releases a safety stop.
- Start and reset combined in one control, or reset that restarts the machine.
- Hold-to-run on touch with no watchdog, so a lost link keeps motion going.
- Showing a safety input as OK when the value is stale or missing.
- Disabling controls with no reason, which teaches operators to bypass them.
- Using a confirmation dialog as the only barrier to a dangerous action.
- Bypass or force flags that leave no persistent on-screen mark.
- Using a consumer tablet or gamepad for enabling or e-stop functions.
- Quoting a performance level as a UI requirement instead of asking for the
  risk assessment.

## Sources

- machinerysafety101, manual reset using an HMI: https://machinerysafety101.com/2021/06/02/manual-reset-using-an-hmi/
- machinerysafety101, ISO 13850 requirements: https://machinerysafety101.com/2026/05/18/iso-13850-emergency-stop-requirements/
- Universal Robots 3PE teach pendant guide (enabling device behaviour): https://www.universal-robots.com/manuals/latest/en/pdf/polyx/3petp/
- Regulation (EU) 2023/1230 (primary text; not retrievable in the research): https://eur-lex.europa.eu/eli/reg/2023/1230/oj/eng
- TUV SUD, ISO 13849 / IEC 62061: https://www.tuvsud.com/en-us/services/functional-safety/iso-13849-iec-62061
- Pilz, functional safety standards: https://www.pilz.com/en-CZ/support/law-standards-norms/functional-safety
- RAFI SAFETY TOUCH (certified safety touch example): https://www.rafi-group.com/en/safetytouch/
