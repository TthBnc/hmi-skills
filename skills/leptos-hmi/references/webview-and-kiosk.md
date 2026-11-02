# Webview, touch and kiosk

## Touch CSS baseline

```css
button, [role="button"], a { touch-action: manipulation; -webkit-tap-highlight-color: transparent; }
.app-root { user-select: none; -webkit-user-select: none; overscroll-behavior: none; -webkit-touch-callout: none; }
input, textarea, [contenteditable] { user-select: text; -webkit-user-select: text; }
button:active:not(:disabled) { transform: scale(0.97); filter: brightness(0.92); }
@media (hover: hover) { /* hover styles only here, as an enhancement */ }
@media (prefers-reduced-motion: reduce) { * { animation: none !important; transition: none !important; } }
```

- Hit areas larger than the visible shape: pad with invisible padding or a
  `::before` with negative inset rather than shrinking spacing.
- Act on click (release), so a wrong press can be cancelled by sliding off.

## Embedded webview performance

Profile the actual Linux webview (often WebKitGTK with Tauri/wry) on the
actual ARM board; desktop-browser performance is not a reliable proxy.
- Animate only `transform` and `opacity`; never `transition: all`.
- Avoid large `box-shadow`, `filter`, `backdrop-filter`, blur and
  `scroll-behavior: smooth`.
- Keep the DOM small; lazy-mount pages; do not re-render high-rate values more
  than needed.
- If the surface flickers or stays blank on Linux, test
  `WEBKIT_DISABLE_DMABUF_RENDERER=1` and `WEBKIT_DISABLE_COMPOSITING_MODE=1`.
- Release builds keep `wasm-opt` enabled.

## Kiosk

- Fullscreen and no window decorations (Tauri: `fullscreen: true`,
  `decorations: false`).
- Restrict browser chrome only for a dedicated, tested kiosk deployment. Keep
  zoom available by default; do not disable accessibility features merely for
  appearance. Any fixed-scale mode needs verified physical sizing and an
  accessible service path.
- Hide the cursor on touch-only devices (`cursor: none` under
  `@media (pointer: coarse)`), but keep it for service use with a mouse.
- No hover-only affordances anywhere.

## Offline deployment

- Bundle fonts, icons and every asset locally; no CDN or web-font requests.
- Verify font rendering (hinting, tabular figures) in the target webview, not
  only in a desktop browser.
