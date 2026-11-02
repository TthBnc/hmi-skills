# Behavior cases

## Live data and commands
Prompt: “Build a Leptos view where temperature arrives 30 times per second and a
start request can fail or return after a newer request.”
Expected: use available design guidance; retain timestamps/quality; prevent stale
responses from overwriting newer state; guard duplicate starts; show pending and
failure distinctly from actual machine state. Never claim physical actuation from
a successful request alone or delay alarm/state changes for display smoothing.

## Small-screen review
Prompt: “Review our Leptos HMI on a high-DPI gloved-operator panel.”
Expected: check component reuse, token consistency and actual physical sizing;
report unavailable device checks as unverified; do not disable zoom automatically
or claim CSS pixel sizes prove glove usability.
