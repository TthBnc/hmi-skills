# Visual language

Prototype defaults for operator HMIs, not normative limits. Define them once as named design tokens
and use only the tokens on every screen; no one-off colours or sizes.

## Colour roles

| Role | Use | Rule |
| --- | --- | --- |
| Canvas | page background | light neutral grey, not pure white; low glare |
| Surface | panels, cards | slightly lighter or darker than canvas; flat, no gradient or heavy shadow |
| Ink / muted ink | text, labels | ink for values, muted for labels and units |
| Live value | numbers that update | one consistent non-alarm colour (dark blue) so live data reads as live |
| Positive | completed, saved, healthy | used sparingly; healthy is mostly just grey |
| Warning | needs a look, not urgent | amber with an icon |
| Danger / fault | requires action, failed, data lost | red with an icon and text |
| Running / recording | a run or recording in progress | its own colour and icon (for example a dot plus "REC" and elapsed time) |
| Held / review / playback | not live data | a distinct non-alarm colour (violet or blue) and "FROZEN" label |

- Normal operation shows almost no saturated colour. If a screen is colourful
  when nothing is wrong, the colours have lost their meaning.
- One colour, one meaning, on every page.
- Never colour alone: pair it with text and an icon or shape. Check with a
  colour-blindness simulator.
- Contrast: text at least 4.5:1; key numbers and status labels aim for 7:1;
  UI shapes at least 3:1.

## Type

| Use | Size (CSS px at 1x) | Notes |
| --- | --- | --- |
| Key value (count, timer, state word) | 48-96 | tabular figures, the largest thing on the screen |
| Status strip text | 18-20, semibold | always visible |
| Body, labels, buttons | 18-20 | never below 16 on the target panel |
| Secondary detail | 16 | only in Level 3-4 views |

- Use `font-variant-numeric: tabular-nums` for anything that updates, so digits
  do not jitter.
- Units sit next to the value in muted ink.
- Sentence case. Avoid all caps except short state words (REC, FROZEN).
- Text sizes must be checked on the real panel at the operator's distance; the
  desktop window is not evidence of legibility.

## Size and spacing

| Element | Minimum | Preferred |
| --- | --- | --- |
| Primary action (start/stop, the main task action) | 56 px high | 72-88 px high, full width of its panel |
| Secondary action | 48 px | 56 px |
| Any touch target | 44x44 px | 56x56 px |
| Gap between targets | 8 px | 12-16 px; 24 px+ between a destructive and a frequent action |
| Panel padding | 16 px | 24 px |

- Convert physical size using device pixels = mm x panel PPI / 25.4, then
  account for device-pixel ratio, OS scaling and webview zoom. CSS pixels are
  not necessarily device pixels. For gloves, start around 20 mm or larger,
  consult the full skill, and verify with the actual panel and operators.
- One spacing scale (4/8/12/16/24/32) across all pages.

## States every control must have

Default, pressed (`:active`, visible within 100 ms), disabled (with the reason
nearby), pending (spinner or progress text, still the same size), and failed
(inline message, not just a toast). Focus rings stay for keyboard use; hover is
only an enhancement under `@media (hover: hover)`.

## Motion and decoration

- No gradients, 3D, glassmorphism, large blurs or box-shadows; they cost frames
  on embedded hardware and add no meaning.
- Animation only to show a state change (under 200 ms) or for the single most
  urgent alert. Respect `prefers-reduced-motion`.
- Blinking only for an unacknowledged, urgent fault.
