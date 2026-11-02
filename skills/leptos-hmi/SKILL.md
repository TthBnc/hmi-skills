---
name: leptos-hmi
description: Build or review operator HMIs in Leptos 0.7/0.8 with client-side rendering, including Tauri or kiosk webviews. Use for reactive components, live data, command state, design tokens, and touch interaction. Pair with an HMI design skill; excludes unrelated Rust backend work.
license: MIT
metadata:
  author: TthBnc
  version: "1.0.0"
---

# Leptos HMI

Turn HMI principles into Leptos code that is clear first and distinctive
second: a calm, precise instrument, not a default web app and not a decorated
one. Read the `hmi-design-full` (or `hmi-design-light`) skill first; it decides what the screen must do. This
skill decides how to build it well in Leptos. Install a companion design skill
from this repository. If it is unavailable, disclose the missing guidance and
ask for it when required for safety-sensitive work; do not invent its contents.

In a repository, follow its own agent instructions, and read the project's
existing component library and tokens before writing new ones. Extend a shared
component with a variant instead of restyling it locally.

## Read what changes the decision

- Components, reactivity, async, live data, lists, video: [Leptos patterns](references/leptos-patterns.md).
- Design tokens, typeface, colour, radius, motion and the anti-bland rules:
  [tokens and taste](references/tokens-and-taste.md). Read it for every new or
  redesigned screen.
- Touch CSS, webview performance, kiosk and offline deployment:
  [webview and kiosk](references/webview-and-kiosk.md).

## Rules

1. **One `Button` component for every action**: real `<button>`, a synchronous
   double-tap guard, `pending` and `disabled` as `Signal<bool>`, `aria-busy`,
   size variants that meet the HMI minimums. No hand-rolled clickable elements.
2. **Tokens only.** Colours, type sizes, spacing, radii and durations are CSS
   custom properties defined once; components never contain raw hex values or
   ad hoc sizes.
3. **Label functions, never Debug.** Every enum shown to an operator has
   `fn label(&self) -> &'static str` and `fn tone(&self) -> Tone`, with unit
   tests. `format!("{:?}", ...)` in a view is a defect.
4. **Fine-grained, throttled live data.** One signal per live metric, set only
   on change, derived flags via `Memo`, display cadence chosen for the process and target device. Never throttle away
   alarms, state transitions, or data-quality changes.
5. **State banners stay mounted.** Toggle classes for frequently changing
   modes; reserve `<Show>` for content that is rarely swapped.
6. **Design every async state**: pending, success, failure with the next step,
   stale. Prefer `Action` for commands and `LocalResource` with `<Transition>`
   for reads so old data stays visible while refreshing.
7. **Verify on the target**: run the real app, walk every state, and check
   sizes, legibility and frame rate on the target panel and webview.
