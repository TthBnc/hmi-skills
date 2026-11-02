# States, modes, commands, data quality, comms and latency

Contents
1. Machine state model (PackML template) and mode model
2. Mode visibility and mode-confusion prevention
3. Command lifecycle, idempotency, no optimistic UI
4. Data quality, age and timestamps
5. Comms loss: watchdogs, screen, machine behaviour
6. Multi-client control arbitration
7. Latency budgets, teleoperation, video freeze
8. Common mistakes, sources

Tags: `[V: source, clause]` read in the research; `(summary)` secondary only;
`(verify)` unverified, check before relying on it. Numbers marked (verify) are
starting defaults to tune on the real machine, not requirements.

## 1. Machine state model and mode model

**Rule:** Model the machine as one state enumeration with a documented table of
legal transitions. Do not use loose booleans (isRunning, isPaused, isError); they
allow impossible combinations.

**Why:** The screen's only job here is to show the true state and the commands
legal in it. A single enum makes "what can I press now" computable.

**How to check:** Every state on the machine appears in the model; every command
is listed against the states where it is legal; no screen invents a state.

### 1.1 PackML as a reusable template

PackML (ISA-TR88.00.02) defines 17 states [V: ISA-TR88.00.02-2015 and the same
list in OPC UA StateEnumeration, https://reference.opcfoundation.org/specs/OPC-30060/11.9].
Names are a vocabulary, not a requirement to use PackML wording. Adopt the
concept: acting states (transient, doing something) vs wait states (stable).

Wait states (stable): Stopped, Idle, Complete, Held, Suspended, Aborted. Acting
states (transient): Resetting, Starting, Completing, Holding, Unholding,
Suspending, Unsuspending, Stopping, Aborting, Clearing. Execute is dual. Power-on
is Stopped; Reset leads through Resetting to Idle. Held = paused for an external
or planned reason; Suspended = the process cannot continue (e.g. input starved);
Aborted = faulted, needs Clear.

Transition template (one row per legal transition, kept with the code):

Columns: from-state, command, guard, to-state, side effects, who may request, screen feedback.

### 1.2 Mapping to simpler machines

Collapse states, never invent new ones silently. Keep these distinctions because
the operator acts differently in each:

| Simple state | PackML equivalent | Operator meaning | Offer |
|---|---|---|---|
| Stopped / Not ready | Stopped, Aborted, Clearing | Safe; cause listed | Reset or Clear (after physical reset if safety) |
| Ready | Idle, Complete | Can start | Start |
| Starting / Stopping | Starting, Stopping, Resetting, Completing | Transition in progress | Wait; Stop stays available |
| Running | Execute | Doing the work | Pause, Stop |
| Paused | Held, Suspended | Not working, can resume | Resume, Stop; reason shown |
| Fault | Aborting, Aborted | Needs attention | Cause, steps, acknowledge |

- A machine with only on/off still has Starting, Stopping and Fault; show them.
- Held (planned or operator pause) and Suspended (the process cannot continue)
  are shown differently, with the reason.
- The state shown is the controller's reported state, not the last command sent.

### 1.3 Mode model

Modes say who or what is in charge. Default set:

| Mode | Meaning | Rules |
|---|---|---|
| Auto / Production | Machine runs the programme | Manual motion disabled; parameters locked |
| Manual | Operator drives axes, hold-to-run | Hazardous motion needs an enabling device or hold control; speed limited |
| Maintenance | Authorised technician, guards may be defeated | Access control (key or login); restricted functions; always conspicuous |
| Simulation / Demo | No real actuation, or fake inputs | Whole screen marked; real outputs blocked |
| Replay / Frozen view | Recorded data shown instead of live | Distinct label and colour on every view |

- Mode change is a command with guards: only from safe states, with a visible
  result. Entering a hazardous mode (maintenance) needs physical or credentialed
  access (see safety-boundary.md).
- Mode is orthogonal to state: Manual + Held is legal; show both.

## 2. Mode visibility and mode-confusion prevention

**Rule:** The active mode and state are always visible in a fixed status area,
redundantly (text, position, colour) and again at the point of action.

**Why:** Mode errors are actions right for the mode the operator believes is
active. Triggers: automatic mode changes the operator did not command, the same
control meaning different things per mode, weak annunciation, and showing the
commanded mode instead of the actual one (Sarter and Woods 1995, summarised in
the research notes). Asiana 214 (NTSB AAR-14/01) is the cited aviation case: an
autothrottle HOLD mode went unnoticed by the whole crew [V: NTSB AAR-14/01,
Executive Summary].

How:
- Show commanded and actual mode separately when they can differ; highlight
  the difference.
- Announce automatic changes with a salient cue that does not need dismissal and
  does not block the screen: say what changed, why, and what happens next. The
  operator's three questions: what is it doing, why, what next.
- Same control, same meaning in every mode; if it must change, change its look.
- Simulation, maintenance, replay and "forced" states get a persistent banner or
  tinted frame on every screen, not just the settings page.
- After a fallback (for example automatic to manual on a sensor failure), keep the
  reason on screen until acknowledged by an action, not a timer.

Check: ask a person who just walked up to name the mode and state within 2 seconds
from 2 m away, without touching the screen.

## 3. Command lifecycle

**Rule:** Every command goes through visible stages. The state indicator changes
only when the controller or a sensor confirms.

| Stage | Meaning | Screen treatment | Time |
|---|---|---|---|
| 1 Input | Touch/press seen | Pressed state | <= 100 ms [V: NUREG-0700 Rev 3 11.3.2.3.6-7; Nielsen] |
| 2 Sent | Handed to controller | Pending badge on the control | show if no ack after about 300 ms (verify) |
| 3 Acknowledged | Controller accepted, or rejected with reason | "Accepted" or "Rejected: reason" | 100-500 ms on a local network (verify) |
| 4 Executing | Actuator moving, transition running | Transition appearance, progress | stroke time + margin (verify) |
| 5 Target reached | Measured feedback matches | Final state from feedback | - |
| 6 Failed / timed out | No ack, no feedback, or feedback disagrees | Explicit message, safe state, next step, alarm if needed | - |

Rules:
1. **Display confirmed state, not commanded state.** Show demand and actual
   separately where they differ ("Set 12.0 / Now 9.4").
2. **No optimistic UI for machine commands.** A button may show pending at once;
   the state indicator waits. Consumer toggles that flip immediately and
   reconcile later mislead: "Pump ON" while the pump never started.
3. **Time out every expected transition** (valve stroke, ramp) with a margin and
   show "Did not reach OPEN". Without a timeout, the screen waits forever.
4. **Idempotency.** Give each command a unique id and sequence number; the
   controller treats a repeat of the same id as the same command (acknowledges
   it, does not run it twice). Prefer absolute commands ("set speed 5") over
   relative ones ("increase speed").
5. **Prevent double-submit.** Disable the control and show pending on send;
   re-enable on response or timeout. Also debounce taps (ignore repeats within
   about 300-500 ms (verify)). UI disabling alone is not enough: retries and
   queues can replay a command, so the controller enforces idempotency.
6. **Reject stale commands.** Attach a timestamp or time-to-live; the controller
   drops motion commands older than about 1-2 s (verify). Never queue a dangerous
   command to fire on reconnect.
8. **Stop is exempt from confirmation and from state guards** that could block it;
   stop and hold are accepted from any client.

## 4. Data quality

**Rule:** Every displayed value carries value, timestamp(s) and quality. The
screen shows only what the quality allows. Unknown is never shown as zero.

OPC UA status codes have a top-level severity Good, Uncertain or Bad. Examples:
Uncertain_LastUsableValue (updating stopped), Uncertain_NoCommunicationLastUsable
(comms failed, last good value kept), Bad_NoCommunication (no value),
BadWaitingForInitialData (nothing received yet) [V: OPC UA Part 8 as summarised in
the research]. Ignition adds Bad_Stale (516) for data older than the requested
refresh interval [V: Ignition docs]. You do not need OPC UA to use the idea.

Display set (map any source into it):

| Quality | Meaning | Treatment |
|---|---|---|
| Good | Trusted live value | Normal |
| Stale | Older than N x expected period (3x is a start (verify)) | Keep value, de-emphasise, show age ("12 s ago"), icon |
| Uncertain | Probably usable, not guaranteed (last usable value, sensor at limit) | Marker overlay; do not drive decisions |
| Bad / Unknown | Invalid, comms or sensor failure, never received | Replace number with dashes ("--.-") and a quality symbol |
| Pending write | Command sent, not confirmed | Pending overlay |
| Simulated / Forced / Overridden / Substituted | Replaced or inhibited by a person or test | Persistent symbol (S / F / M) with who and when |
| Disabled / Not applicable | Intentionally off | Neutral "off" look, distinct from fault |

Rules:
- **Unknown is never zero.** Dashes, "No data", or a hatched gauge with no needle.
  A value of 0 means a measured zero. NUREG-0700 requires an indication when data
  are invalid or unvalidated [V: NUREG-0700 Rev 3, 14.3-3 and 14.3-4]; the hatched
  and timestamped look is practice (summary).
- Do not freeze a last value without marking it; a frozen number looks live.
  If the last value helps, keep it greyed and labelled "last known 14:03".
- Carry source and receive timestamps; derive age from them, not draw time.
- Separate messages for link lost, sensor bad and value implausible.
- A controller output in last-value state must not look commandable; disable
  controls that depend on it.
- Forced, simulated or bypassed values are marked persistently, not in an alarm
  colour (summary).

## 5. Comms loss

**Rule:** Safety of the machine must never depend on the screen being connected.
The machine reaches a safe state on its own; the screen tells the truth about it.

### 5.1 Heartbeats and watchdogs

- Both ends watch the link. For a hold or jog command the sender repeats it at a
  fixed rate (for example 10-20 Hz) and the receiver stops motion if no message
  arrives within about 100-300 ms (verify). Tune both numbers to the stopping
  distance and speed of the machine.
- A **watchdog in the controller** (not the screen) triggers the fail-safe action.
  Screen-side timeouts only drive display.
- The heartbeat carries a counter so duplicated or replayed messages are noticed;
  state updates carry sequence numbers so gaps force a full resync.

### 5.2 What the machine does by itself

Define one fail-safe response to link loss per machine in its risk assessment
(stop, hold, ramp to a safe state, or continue a self-contained programme) and
show which. Hazardous manual motion stops at once (verify per machine). After
reconnect the machine does not resume by itself unless designed to; the operator
confirms.

### 5.3 What the screen shows

1. A global connection banner in the status area, with duration ("Connection lost
   00:42").
2. All dependent live values go to Stale then Unknown (section 4).
3. Controls that need the machine are disabled with the reason; none queue.
4. State: "Last known: Running (14:03)" muted, never as current.
5. The message says what the machine is doing by itself ("Machine has stopped")
   only when the machine has reported it; otherwise say "state unknown".
6. On reconnect: snapshot, reconcile pending commands as failed, re-check mode
   and state, then enable controls; back off with jitter.

## 6. Multi-client control arbitration

**Rule:** One controlling client per control scope at a time; all others view.
The controller enforces this; clients cannot grant themselves control.

- Show everywhere who has control (name or station) and who is viewing. View-only
  controls are disabled with the reason "Controlled by X".
- Explicit take / release actions; the previous controller is told when control
  moves. Optional request / offer / accept flow; an authority override needs a
  reason and a log entry.
- Priority: the local operator at the machine outranks remote clients. Stop, hold
  and pause are accepted from any client, because stopping is safe; starts and
  mode changes need control.
- Control is a lease that needs a heartbeat; a lost client releases control after a
  timeout. At boot nobody controls; the local panel gets control on login or first
  touch.
- All clients render the same authoritative state; a stale client must not send.

## 7. Latency budgets

### 7.1 The three limits

| Limit | Meaning for a machine screen | Source |
|---|---|---|
| 0.1 s | Feels instant; the result itself is the feedback. Use for touch feedback and local UI. | [V: Nielsen 1993, nngroup.com] |
| 1 s | Flow of thought holds; show a busy/pending cue after about 1 s. | [V: Nielsen] |
| 10 s | Attention limit; for longer waits show determinate progress or an ETA and allow cancel when safe. | [V: Nielsen] |

- Touch feedback: at most 100 ms, preferably about 55 ms [V: NUREG-0700 Rev 3,
  11.3.2.3.6-7]. MIL-STD-1472H has a 100 ms latency limit (5.1.3.1.4) [V:
  research notes, 1472H].
- The 0.25 s figure: older FAA HFDS 9.4.2, citing MIL-STD-1472D, says display
  feedback of a user action within 0.25 s [V: FAA HFDS 9.4.2 via the research
  notes]; the research marks it superseded for sizes and not present in 1472H.
  Treat 0.25 s as a historical outer bound and design to 0.1 s.
- Commanded effect to visible result (controller round trip) is a separate budget:
  show pending after about 300 ms, accept 100-500 ms on a local network (verify).
- Budget the whole chain (touch scan, render at 16.7 ms per frame, network,
  controller scan, actuator, sensor); slow displays can exceed 100 ms (verify).

### 7.2 Teleoperation

Figures from ARL-TR-3834 (Chen et al., 2006), which cites studies second-hand
Evidence [V: ARL-TR-3834 sections 2.1.1.5, 2.1.2.3]:
- People can detect delay of 10-20 ms in virtual environments.
- Vehicle control degraded at 170 ms in a simulated driving study; operators begin
  to decouple commands from the response at about 300 ms.
- Positioning tasks took longer above 500 ms; above about 1 s operators switch to
  move-and-wait (command, stop, look, command).
- Jitter can hurt more than a longer constant delay: performance degraded when the
  standard deviation of latency exceeded 82 ms; unpredictable delay causes
  over-actuation (repeated commands, over-steer).
- Frame rate: 10 Hz is recommended as a minimum to avoid degradation; no fewer than
  8 fps for ground-vehicle teleoperation; performance is significantly affected at
  5-6 fps and nearly impossible below 3 fps [V: ARL-TR-3834 2.1.1.4, 2.1.2.2].
  Default: aim for at least 10 Hz and treat below 8 Hz as degraded.

Design responses (practice, mostly (verify)): show measured latency and link
quality; scale speed limits with latency and cap step size so one command cannot
overshoot; show video age and avoid frame buffering; above about 1 s design for
supervisory control (send a target, verify, use predictive overlays); use
low-latency video for driving and full-quality stills for inspection, labelled.

### 7.3 Video freeze and frame age

**Rule:** Detect a frozen or old video frame yourself; a frozen last frame looks
like a valid image.

- Stamp every frame with a source timestamp or counter at the camera side. Compute
  frame age at display time; show it when it exceeds a threshold (for example
  twice the frame period, or 250 ms (verify)).
- If frames stop for longer than a short threshold (for example 1 s (verify)),
  overlay "VIDEO LOST" at once, grey the image, and disable motion that depends on
  it. A watchdog on the machine side halts motion when the video, not only the
  control link, is lost, if the task depends on the video.

## Common mistakes

- Optimistic UI: the indicator flips to "ON" before feedback confirms.
- Boolean flags instead of one state enumeration, so impossible states render.
- Mode shown only on a settings page, or only the commanded mode shown.
- Unknown or failed sensor shown as 0, or last value shown unmarked as live.
- Disabling a button on send but not making the controller idempotent, so a
  retried command runs twice.
- Queueing commands during a disconnect and firing them on reconnect.
- Relying on a socket "connected" flag instead of data age to detect a silent link.
- Hold-to-run on a screen with no controller watchdog.
- Letting any client start the machine or change mode; no visible owner of control.
- Video that freezes on the last frame without any overlay, and motion allowed
  while it does.

## Sources

- OPC UA StateEnumeration (PackML 17 states): https://reference.opcfoundation.org/specs/OPC-30060/11.9
- Nielsen, response times, the 3 important limits: https://www.nngroup.com/articles/response-times-3-important-limits/
- Chen, Haas, Pillalamarri, Jacobson, ARL-TR-3834 (teleoperation latency, frame rate): https://www.govinfo.gov/content/pkg/GOVPUB-D101-PURL-gpo9710/pdf/GOVPUB-D101-PURL-gpo9710.pdf
- NTSB Asiana 214, AAR-14/01 (mode confusion case): https://www.ntsb.gov/investigations/AccidentReports/Reports/AAR1401.pdf
- Ignition quality codes and Perspective (Bad_Stale, overlays): https://docs.inductiveautomation.com/docs/8.3/ignition-modules/perspective
- NUREG-0700 Rev 3 (11.3.2.3.6, 14.3) and MIL-STD-1472H, FAA HFDS 9.4.2, as read in the research notes.
