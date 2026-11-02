---
name: hmi-design-full
description: Design, specify, and review operator HMIs for machines and industrial processes. Use for safety boundaries, machine states, command feedback, data quality, alarms, glove use, legibility, or operator testing. Framework independent; excludes consumer apps and ordinary business dashboards.
license: MIT
---

# HMI Design (full)

An HMI exists so an operator, often standing, gloved, under time pressure and
watching the work rather than the screen, can answer at a glance: **what state
is the machine in, is anything wrong, what do I do next.** Every decision is
judged against those three questions, in this priority order when rules
conflict: **safety > situation awareness > error prevention > efficiency >
aesthetics.**

For review or planning requests, inspect and recommend; do not implement
without a request. In a repository, follow its own agent instructions.

## Evidence tags used in the references

`[V: source]` records a source check made during original authoring; it is not
a fresh verification of the current edition or a claim of compliance. `(summary)` from
secondary sources. `(verify)` unconfirmed: never present it as a requirement;
say it is a starting value and recommend testing on the real device.
For normative or safety-critical decisions, check the applicable current primary
source and the machine risk assessment. Domain-specific guidance is not a
universal requirement. External standards are not redistributed or relicensed
by this skill; source annotations do not establish machine compliance.

## Non-negotiables

1. **The HMI is never the safety layer.** E-stop and safety functions are
   hardwired/safety-rated; a screen may show them but never implement or reset
   them. → [safety-boundary](references/safety-boundary.md)
2. **State, mode and connection are always visible** in a fixed status strip
   on every screen, together with the highest-priority active alarm.
3. **Every value carries its quality.** Stale, bad, simulated or unknown values
   never look live; unknown is never shown as 0.
   → [states-and-commands](references/states-and-commands.md)
4. **Commands show their real lifecycle**: pressed (≤100 ms feedback) → sent →
   acknowledged → target state reached, or a plain-language failure with the
   next step. Never claim success before the machine confirms it.
5. **An alarm requires an operator action.** Everything else is status or log.
   Few priorities, exclusive colours and sounds, and every alarm says what to
   do. → [alarms](references/alarms.md)
6. **Neutral is normal; colour means attention.** Saturated colour only for
   abnormal states and modes; never colour alone.
   → [visual-language](references/visual-language.md)
7. **Size for the real hand, eye and environment**: gloved primary targets
   about 20 mm or more, text at least 16 arcmin (20-22 preferred) at the real
   viewing distance. → [physical-and-environment](references/physical-and-environment.md)
8. **Confirm only irreversible actions**, naming object and effect. Never
   confirm stop. Physical or held actions for motion.
9. **Operator language only**: no internal IDs, enum names, codes or stack
   traces outside "Technical details".
10. **Automation output is evidence, not truth**: show why, show limits, make
    correction fast, never switch automation level silently.
11. **Configuration is separate from operation**, and access is per person and
    role. No shared hard-coded PINs.

## Workflow

1. **Context of use**: operators (roles, skill), tasks, environment (distance,
   gloves, light, noise, vibration, where eyes and hands are), safety functions
   that exist outside the HMI. → [process](references/process.md)
2. **State model**: list machine states and modes, every screen state (idle,
   pending, running, held, stale, disconnected, failed, empty, no permission),
   and the command lifecycle. A missing state is a defect.
3. **Alarm list**: rationalise each alarm (cause, consequence, action, time to
   respond, priority) before drawing any screen.
4. **Information ranking and hierarchy**: what must be read from 2 m, at arm's
   length, on demand; levels 1-4. → [patterns](references/patterns.md)
5. **Style guide and tokens** written once and reused everywhere; run
   `scripts/contrast.py` on token pairs and `scripts/sizing.py` for the panel.
6. **Design screens** from the patterns; check [anti-patterns](references/anti-patterns.md).
7. **Evaluate on the real device**, at the real distance, with real gloves and
   real operators, including abnormal scenarios; then the
   [review checklist](references/review-checklist.md).

## Which reference to read

| Question | File |
|---|---|
| Why a rule exists, which standard, rule conflicts, cognitive basis | [principles](references/principles.md) |
| What the screen may do vs the safety system, e-stop, interlocks | [safety-boundary](references/safety-boundary.md) |
| Machine states/modes, command feedback, data quality, comms loss, latency | [states-and-commands](references/states-and-commands.md) |
| Alarms, alerts, priorities, sound, messages, floods | [alarms](references/alarms.md) |
| Colour, type, numbers, trends, indicators, tokens, blink | [visual-language](references/visual-language.md) |
| Touch sizes, gloves, physical controls, environment, localisation, kiosk | [physical-and-environment](references/physical-and-environment.md) |
| Screen and workflow patterns, wording, setpoint entry, history | [patterns](references/patterns.md) |
| Design process, documents, task analysis, usability testing, KPIs | [process](references/process.md) |
| Software architecture, logging, updates, security, testing | [architecture-and-security](references/architecture-and-security.md) |
| What goes wrong (with real incidents) | [anti-patterns](references/anti-patterns.md) |
| Worked examples by machine type | [Packaging](references/examples/packaging-line-packml.md), [vision inspection](references/examples/vision-inspection-station.md), [pipe rehabilitation](references/examples/cable-driven-pipe-rehab-machine.md) |
| Reviewing a screen or codebase | [review-checklist](references/review-checklist.md) |

Read only the files the task needs. For a full review, read the checklist first
and open the other files as items come up.

## Tools

- `python3 scripts/contrast.py FG BG [...]`: WCAG 2.x contrast ratio for hex colour pairs.
- `python3 scripts/sizing.py --ppi P --distance-mm D`: converts mm, px and arcminutes
  for a panel; prints minimum target and text sizes.
- `python3 scripts/lint_tokens.py PATH`: lists hard-coded colours and px sizes in
  CSS/TSX/RS files that bypass design tokens.

## Review output format

Rank findings by severity: **Safety** (could hurt someone or damage
equipment) → **Operator error** (likely wrong action or missed state) →
**Efficiency** → **Consistency/cosmetic**. Each finding: what and where
(file:line or screen), the rule it breaks (reference file), the consequence,
and the fix. Mark items not checkable from code (legibility, glove use) as
"not verified: needs device test", never as passed.
