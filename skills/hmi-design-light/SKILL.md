---
name: hmi-design-light
description: Apply a compact HMI usability checklist to machine and station screens. Use for routine layout, operator wording, navigation, and visual hierarchy. Use hmi-design-full for safety, alarms, command/data-quality behavior, quantitative standards, or detailed reviews.
license: MIT
metadata:
  author: TthBnc
  version: "1.0.0"
---

# HMI Design (light)

The compact version. For full depth (safety boundary, alarm lifecycle, data
quality, physical environment, process, anti-patterns) use `hmi-design-full`.

An HMI exists so an operator, often standing, gloved, under time pressure and
looking at the work rather than the screen, can answer three questions at a
glance: **what state is the machine in, is anything wrong, what do I do next.**
Judge every decision against those questions, not against how much fits.
Clarity and ease of use always come first.

For review or planning requests, inspect and recommend; do not implement
without a request. In a repository, follow its own agent instructions for
scope and validation.

## Read what changes the decision

- Why a rule exists, or a trade-off between rules: [principles](references/principles.md).
- Colour, type, sizes, spacing and control states: [visual language](references/visual-language.md).
- Screen structure, modes, live values, automation output, alerts,
  confirmations and wording: [patterns](references/patterns.md).
- Before handing off a screen, and for HMI reviews: [review checklist](references/review-checklist.md).

## Non-negotiables

1. **State and mode are always visible** in a fixed status area: connection,
   run state, active mode and the highest-priority fault. Never only in a page body.
2. **Neutral is normal, colour means attention.** Saturated colour is reserved
   for states the operator must notice; every colour is paired with text or an icon.
3. **One primary action per screen**, always visible and in a fixed place,
   sized on the real panel for the operator and gloves. CSS pixel defaults
   are starting points, not proof of adequate physical size.
4. **Operator language only.** No internal IDs, raw enum names, versions, paths
   or error codes in the main view; put them behind "Technical details".
5. **Every touch gets feedback within 100 ms**, and every command shows pending,
   success, or a plain-language failure with the next step.
6. **Confirm only irreversible actions**, naming the object and the effect;
   prefer undo for reversible ones. Never put a confirmation on a stop or
   emergency action.
7. **Automation output is evidence, not truth.** Show results with their
   evidence and a few rule-based confidence levels; make correction fast.
8. **Configuration is separate from operation.** Setup and settings live away
   from the screens used during a run.

## Workflow

1. Name the operator, the task, the physical context (distance, gloves,
   lighting, noise, where hands and eyes are) and what success looks like.
2. List every state the screen can be in (idle, pending, running, paused,
   held, stale, disconnected, failed, empty) and design each one; a missing
   state is a defect.
3. Rank the information: what must be seen from 2 m, what is read at arm's
   length, what is on demand. Lay out in that order.
4. Write the style decisions once (colours, type scale, sizes, wording) and
   reuse them on every screen; consistency is a requirement.
5. Evaluate on the real device at the real distance, ideally with real
   operators and their gloves; a desktop window is not evidence of legibility
   or touch accuracy.
