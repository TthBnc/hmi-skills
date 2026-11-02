# Tokens and taste

Clarity and ease of use always win. Taste means the screen looks deliberately
designed for its machine instead of assembled from defaults. The target
signature is a **calm, precise instrument**: restraint and craft, not
decoration.

Concepts here were taken from popular design-taste skills (Anthropic
frontend-design, Hallmark, Taste Skill, Impeccable, Vercel Web Interface
Guidelines, Rauno Freiberg, Emil Kowalski, Refactoring UI) and kept only where
they fit an operator HMI.

## Commit to a direction before writing components

Write a token sheet first and review it against the brief, removing every
default nobody chose:

```css
:root {
  /* neutrals: slightly cool-tinted, high contrast */
  --ink: #1b2027; --ink-muted: #5a6472; --canvas: #e9ecef; --surface: #f6f7f8; --line: #c9cfd6;
  /* meaning, never decoration */
  --live: #1f4e8c; --ok: #2f7d4f; --warn: #b26a00; --fault: #b3261e; --held: #5b3fa0;
  /* type: one bundled family */
  --font: "Your Chosen Sans", system-ui, sans-serif;
  --text-value: 64px; --text-status: 20px; --text-body: 18px; --text-small: 16px;
  /* size and rhythm */
  --tap: 56px; --tap-primary: 80px; --space-1: 4px; --space-2: 8px; --space-3: 12px;
  --space-4: 16px; --space-6: 24px; --space-8: 32px;
  --radius-control: 10px; --radius-panel: 2px;
  --dur-press: 80ms; --dur-state: 150ms;
}
```

The values are a starting point; contrast must be checked (text 4.5:1, key
values and status 7:1 target, shapes 3:1).

## Rules that add character

1. **Spend boldness in one place.** Each screen has one loud element: the main
   live value, the run state or the next action. Everything else is quieter by
   size and weight, not by colour.
2. **A chosen typeface, not the default.** One legible, slightly technical sans
   with distinct 0/O and 1/l/I and good tabular figures, bundled locally. Use
   weight and size for hierarchy within that one family.
3. **Numbers are the hero.** `font-variant-numeric: tabular-nums`, right or
   optically aligned, large, never truncated; units in `--ink-muted`.
4. **Tinted, high-contrast greys** instead of pure black, white or grey; the
   tint must never read as a state colour.
5. **Structure encodes information.** Every panel, border and divider answers
   "what belongs together?". Group with spacing on the 4/8 px scale first;
   borders only where spacing is not enough. Numbering only for real sequences.
6. **One radius rule.** Tappable controls use `--radius-control`; read-only
   panels and readouts use `--radius-panel`. Shape tells what can be touched.
7. **Functional motion only.** `--dur-press` for pressed feedback, `--dur-state`
   for state changes, `transform`/`opacity` only, no entrance animations. One
   deliberate moment is allowed where it carries meaning, such as the running
   band appearing when a run starts.
8. **Hit areas bigger than the shape**, so controls look precise and stay easy
   to hit with gloves.
9. **One vocabulary.** The button verb is the word in the status and the log:
   "Start run" -> "Running" -> "Run saved". Errors state the fix; empty states
   give the next action.
10. **Real content only.** Real values or an explicit "No data yet"; never
    placeholder numbers, fake success or decorative sample images.

## Adapted, with limits

- ALL CAPS only for short state words (REC, HELD, FAULT); never for labels or
  eyebrows above headings.
- Fixed aesthetic dials for HMIs: motion minimal, layout variance low, density
  low to medium.

## Rejected for HMIs

- Gradients, glows, glassmorphism, soft drop shadows, decorative texture,
  illustrations: they read as state, lose contrast under glare and cost frames
  on embedded webviews.
- Colouring a single word for emphasis or adding brand accent colour: colour is
  reserved for state.
- Card soup: grids of identical rounded cards, cards inside cards.
- Template chrome: eyebrows on every heading, middle-dot meta strings, arrows on
  buttons, monospace decoration labels.
- Serif or display typefaces, entrance animations, bounce or elastic easing.

## Taste review
- [ ] Exactly one loud element per screen, and it is the right one.
- [ ] Every colour on screen carries meaning; remove any that does not.
- [ ] Nothing is a default nobody chose (system font, stock radius, stock
      shadow, generic card).
- [ ] Numbers look precise: tabular, aligned, sized for distance.
- [ ] The same action uses the same word everywhere.
- [ ] All values come from tokens; no raw hex or ad hoc sizes in components.
