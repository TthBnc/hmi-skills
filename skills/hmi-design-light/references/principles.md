# HMI principles and their sources

Use this to justify a decision or resolve a conflict between rules. Most
standards are paywalled; entries marked *(summary)* were distilled from
published summaries, and figures marked *(verify)* should be checked against
the primary text before being quoted as a requirement.

## Process-HMI standards

**ANSI/ISA-101.01-2015, HMIs for process automation** *(summary)*
- Write a style guide first (hierarchy, object library, colour, navigation,
  naming, alert presentation) and change it deliberately; consistency across
  screens is a requirement, not polish.
- Display hierarchy: Level 1 overview, Level 2 unit control, Level 3 detail and
  diagnostics, Level 4 help. Any detail should be one or two taps from the
  overview.
- Colour sparingly; saturated colour for abnormal states; never colour alone.

**ASM Consortium, Effective Operator Display Design (2008); Hollifield et al.,
The High Performance HMI Handbook (2008)** *(summary)*
- Neutral grey background, muted normal states, so abnormal states stand out.
- No 3D, gradients or decoration.
- Show values with context: units, target or expected value, normal range, and
  trend one tap away. A bare number forces the operator to remember the limit.

**ISA-18.2-2016 / IEC 62682 (alarm management); EEMUA 191 (2013)** *(summary)*
- An alarm requires an operator action; anything else is a status or log entry.
- At most three priority levels, each with consistent colour, shape and sound.
- Alert text says what happened and what to do.
- EEMUA 191 load guide: about 1 alert per 10 minutes is manageable; more than
  10 in 10 minutes during an upset overwhelms *(verify)*.

**NUREG-0700 Rev. 3 (2020), Human-System Interface Design Review Guidelines**
(free at nrc.gov) *(summary)*
- Consistent formats and units; labels adjacent to what they label; minimal
  clutter; limited, redundant colour coding; feedback for every control action.

**ISO 9241-110:2020 interaction principles** *(summary)*: suitability for the
task, self-descriptiveness, conformity with expectations, learnability,
controllability, use-error robustness, user engagement.
**ISO 9241-112:2017 presentation**: detectability, discriminability, legibility,
comprehensibility, consistency. **ISO 9241-11/-210**: define the context of use
and evaluate with real users in the real environment.

**IEC 62366-1 and FDA human factors guidance (2016, free at fda.gov)**
- Mitigate use errors in this order: design them out, then guard, then warn.
  Warnings and training are the weakest controls.
- Confirmations name the object and effect; prefer undo where possible.

## Cognitive foundations

- **Situation awareness (Endsley 1995):** perception, comprehension, projection.
  Organise screens around goals, not data sources; show what a value means
  (expected vs actual) and where it is heading (trend, time remaining); keep
  global state visible at all times.
- **Gulfs of execution and evaluation, mode errors (Norman 2013):** visible
  affordances, immediate feedback, constraints. Distinct modes (live, frozen,
  replay, test) must look different everywhere, not just in a label.
- **Error types (Reason 1990):** slips and lapses are prevented by spacing,
  constraints, defaults and undo; mistakes by clear information and feedback.
- **Multiple resources (Wickens 2002):** eyes are busy with the parts, so a
  critical event can use sound as well as the screen.
- **Fitts' law:** frequent actions large and near the resting hand; destructive
  actions small-er and far from frequent ones.
- **Hick-Hyman law:** decision time grows with the number of choices; keep about
  5-7 primary choices per screen and group the rest.
- **Pre-attentive features:** colour, size, motion and position pop out; only
  one or two things may pop out at once. Motion/blink only for urgent items.
- **Colour vision deficiency:** about 8% of men (red-green). Pair colour with
  text, icon or shape; prefer luminance contrast and blue/orange over red/green.
- **Ecological interface design (Vicente and Rasmussen 1992):** show why a value
  is what it is (detections behind a count), so operators can reason about the
  unexpected.

## Touch ergonomics

- Minimum targets: WCAG 2.2 SC 2.5.8 24x24 CSS px (AA), SC 2.5.5 44x44 (AAA);
  Apple 44 pt; Material 48 dp (about 9 mm).
- Industrial and gloved use: 15-20 mm for primary controls. A 15-inch kiosk
  study found 20 mm most efficient; a flight-deck study found 15 mm sufficient
  for non-critical targets *(industry practice, verify against our gloves)*.
  Capacitive panels often fail with gloves; test with the real panel and gloves.
- Spacing: at least 4 mm between targets (8 px+), more between safe and
  destructive actions.
- Act on release (click), so a wrong press can be cancelled by sliding off.
- Legibility: critical text at least about 20 arcminutes; at 600 mm that is
  about 3.5 mm *(verify)*. Contrast at least 4.5:1 for text, 3:1 for UI shapes
  (WCAG 2.2); aim for 7:1 on critical numbers.

## Automation and model output

- **Parasuraman and Riley (1997):** people both over- and under-rely on
  automation; complacency rises when it is usually right. Make the model's state
  and limits visible.
- **Lee and See (2004):** calibrate trust by making purpose, process and
  performance observable; show the reason for an output.
- **Amershi et al. (2019), Guidelines for Human-AI Interaction:** make clear what
  the system can do and how well, show why it did something, support efficient
  correction and undo, provide global controls.
- Show uncertainty only when it changes what the operator does: a few levels
  tied to rules (counted, check, unresolved), not raw probabilities.

## Real-world examples worth borrowing from

- High-performance HMI white papers (Emerson, ISA-101 material): grey screens,
  values shown as bars against limits, trends one tap away.
- Cognex VisionView / In-Sight: a pass/fail signal readable from a distance;
  pan/zoom on a held or failed image; export of failed images; job editing kept
  away from the run view.
- Siemens WinCC touch notes: desktop-default controls are too small for touch.
