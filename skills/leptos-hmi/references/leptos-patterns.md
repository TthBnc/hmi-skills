# Leptos patterns for HMIs

Written for Leptos 0.8 with client-side rendering (`features = ["csr"]`); most
apply to 0.7. Book: https://book.leptos.dev, API: https://docs.rs/leptos.

## Reactivity

- Components run once; only signal reads inside closures re-run. Read signals
  inside `move ||` in the view; a `.get()` in the component body never updates.
- One signal per live metric, not one struct signal for everything; a struct
  signal re-notifies every reader on every change. For large state trees use
  `reactive_stores` (`#[derive(Store)]`) for per-field tracking.
- Set only on change: `if count.get_untracked() != v { count.set(v) }`.
- Gate expensive or visual work with `Memo`, which only notifies when its value
  changes: `let over = Memo::new(move |_| count.get() > limit.get());`
- Use `get_untracked` inside event handlers and callbacks.

## High-rate live data

- For high-rate numeric displays, buffer samples and select a display cadence
  from the process and operator task. A 100-250 ms interval is an example to
  test, not a standard. Do not delay alarm, machine-state or quality updates.
- If smoothing is useful, label it and retain unsmoothed values for limit checks.
- Bind numbers as text (`<span class="value">{move || count.get()}</span>`), not
  through `<For>` over a replaced `Vec`.
- Track last-update time in a signal and derive a `stale` flag from it.

## Components and props

- `#[prop(into)]` for ergonomic inputs; `Signal<T>` for reactive inputs;
  `MaybeProp<T>` for optional reactive props (`MaybeSignal` is gone in 0.7+).
- `Callback<T>` for events, `Children`/`ChildrenFn` (use `ChildrenFn` when
  rendered inside `<Show>`).
- Enums for variants (`ButtonVariant::Primary`, `Tone::Danger`) with `const fn`
  class mapping, so styling logic is unit-testable without a browser.
- App-wide state (connection, run state, active fault) through
  `provide_context` / `expect_context` of a `Copy` struct of signals, instead of
  threading many props.

```rust
#[derive(Clone, Copy, PartialEq)]
pub enum RunState { Idle, Starting, Running, Stopping, Failed }

impl RunState {
    pub const fn label(self) -> &'static str {
        match self {
            Self::Idle => "Ready", Self::Starting => "Starting...",
            Self::Running => "Running", Self::Stopping => "Stopping...",
            Self::Failed => "Stopped with a fault",
        }
    }
    pub const fn tone(self) -> Tone {
        match self { Self::Running => Tone::Accent, Self::Failed => Tone::Danger, _ => Tone::Neutral }
    }
}
```

## Async

- Commands: `Action::new_local(|input: &T| async move { ... })`; wire
  `action.pending()` to the button's `pending`; read `action.value()` for the
  result and show failure inline with the next step.
- Reads: `LocalResource::new(|| async { ... })` inside `<Transition>` so the
  previous data stays on screen during a refresh instead of a flashing spinner.
- Where several in-flight responses can overwrite each other (reconnects,
  rapid source changes), guard with a request id or epoch and drop stale replies.
- `<ErrorBoundary>` fallback is plain-language with a Retry button; never render
  an error's Debug text.

## Conditionals and lists

- `<Show>` unmounts and rebuilds. For a status banner, mode band or overlay
  that toggles often, keep it mounted: `class:is-held=move || held.get()`.
- Multi-state widgets: `move || match state.get() { ... }.into_any()`.
- `<For each=... key=|row| row.id>` with a stable key, never the index.
- Lazy-mount inactive pages; keep the DOM small on embedded webviews.

## Buttons and input

```rust
let start = Action::new_local(|_: &()| async { api::start_run().await });
view! {
    <Button size=ButtonSize::Primary pending=start.pending().into()
            disabled=Signal::derive(move || !ready.get())
            on_click=move |_| { start.dispatch(()); }>
        "Start run"
    </Button>
}
```

- The button checks its own pending flag synchronously on click, so a double
  tap cannot submit twice.
- Long-press or hold-to-confirm: `pointerdown` starts a timer with visible
  progress; `pointerup`, `pointercancel` and `pointerleave` cancel it.
- Keyboard: real `<button>` elements, visible focus, `on:keydown` for Escape;
  `window_event_listener` for global shortcuts.

## Live video

- Show an MJPEG or similar stream as a plain `<img src=url>`; the browser
  decodes it with zero WASM work per frame. Avoid canvas blitting through WASM.
- Add a "No signal" overlay, automatic retry after `on:error` with a
  cache-busting URL, and a frame-age indicator so a frozen stream is visible.
- Draw overlays (boxes, regions) as an absolutely positioned SVG with a
  `viewBox` in source pixels, so they scale with the image.

## Testing

- Keep labels, tones, state derivation and validation in plain functions with
  unit tests.
- Walk every state in the running app (pending, failed, stale, disconnected,
  empty), not only the happy path.
