# HMI review checklist

Walk the real screen in each state. Mark each item as pass, fail (with a
file:line or screenshot) or not checked (with the reason). Do not mark sizing or
legibility as passed from a desktop window alone.

## Glance test (from 2 m, 3 seconds)
- [ ] The run state (idle, running, held, playback, fault) is obvious.
- [ ] It is obvious whether anything is wrong.
- [ ] The next action is obvious and is the largest control.

## State coverage
- [ ] Idle, pending, success, failed, disconnected/stale, empty and permission-
      denied states are all designed and reachable.
- [ ] The status strip is visible on every page and matches the page body.
- [ ] Modes (frozen, replay) look different from live everywhere they appear.
- [ ] Disabled controls state why.

## Colour and type
- [ ] Normal operation is mostly grey; colour only marks attention or mode.
- [ ] Every colour has a text or icon partner; one meaning per colour.
- [ ] Contrast: text 4.5:1+, key values 7:1 target, shapes 3:1+.
- [ ] Key value 48 px+; body 18 px+; nothing operator-facing below 16 px.
- [ ] Updating numbers use tabular figures and do not flicker.

## Touch
- [ ] Every target 44x44 px+, primary 56 px+ (72 px+ for start/stop and the main task action).
- [ ] 8 px+ between targets; destructive actions 24 px+ from frequent ones.
- [ ] Visible pressed state; no hover-only affordance; no double-submit.

## Content
- [ ] No internal IDs, raw enum names, versions, paths or codes outside technical details.
- [ ] At most one sentence of help per panel in the main view.
- [ ] Messages say what happened, why if known, and what to do.
- [ ] Confirmations only for irreversible actions, naming the object and verb.

## Model output
- [ ] Count shown with expected value and evidence (overlay, breakdown).
- [ ] Confidence as rule-based levels, not raw probabilities.
- [ ] Correction is fast, reversible until saved, and shows original vs
      corrected.

## Implementation
- [ ] Style values come from one set of design tokens; no one-off colours or sizes.
- [ ] High-rate values are throttled and do not flicker.
- [ ] Live video has no-signal, retry and frame-age handling.
- [ ] Label and state logic is unit-tested.
- [ ] If built in Leptos, the leptos-hmi taste review passes.
