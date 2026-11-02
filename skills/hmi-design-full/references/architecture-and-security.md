# HMI software architecture, operations and security

Tags: `[V: source]` = checked against a read source; `(summary)` = secondary or vendor summary, primary not read; `(verify)` = recalled, synthesised or an engineering heuristic. Domain-neutral. Safety boundary details live in safety-boundary.md.

## Contents
1. Layering and the safety boundary
2. State machine and command protocol
3. Single source of truth, staleness, reconnection
4. Update rates, throttling, frame age, rendering
5. Multi-client control and remote access
6. Logging and audit trail
7. Recipes, config, versions, updates and rollback
8. Localisation, units, time
9. Diagnostics, help, training, simulation
10. Technology choices
11. Security (IEC 62443, auth, RBAC, kiosk, CISA, GDPR, safety-rated parts)
12. Testing
13. Common mistakes
14. Sources

## 1. Layering and the safety boundary

The HMI is not the safety layer. A PC, browser or touchscreen app can crash, freeze, lag, mis-render or be hacked. See safety-boundary.md for the full rules; the architecture consequences are:
- Safety functions (e-stop, interlocks, safe speed, light curtains) live in dedicated safety hardware or logic, verified per ISO 13849 / IEC 62061 / IEC 61508 (verify).
- Loss of the HMI must leave the machine in a safe, defined state. Hardwired stop paths never route through the HMI.
- Interlock logic lives in the controller; the HMI displays interlock status and cause.
- The controller validates every command (range, mode, interlock); UI checks (limits, confirmations) are usability aids only.
- Never draw a software button that looks like an e-stop; an HMI-resident stop is worded "pause" or "hold" (verify).

Layers (top to bottom); each talks only to its neighbour:

```
Operator UI (render, input)          no machine logic
HMI app logic (view-models, session, permission UI)
State/data service                   single source of truth inside the HMI
Communication adapter                OPC UA, MQTT, Modbus, serial, WebSocket, REST
Controller / firmware                modes, interlocks, motion (authoritative)
Safety layer, hardwired              independent
```
Rules: UI components never touch the protocol directly (so staleness, quality and rate limiting happen once); no duplicated machine logic in the UI, and display-only derived values are marked; all messages follow a typed, versioned schema shared by firmware, backend and frontend; keep presentation separate from semantics (verify).

## 2. State machine and command protocol

- The controller owns an explicit state machine; the HMI renders it and requests transitions. Use one state enum, not many booleans (isRunning, isPaused, isError allow impossible combinations).
- Reference model: ISA-88 / PackML has 17 states: Stopped, Resetting, Idle, Starting, Execute, Completing, Complete, Aborting, Aborted, Stopping, Clearing, Suspending, Suspended, Unsuspending, Holding, Held, Unholding [V: OPC UA PackML StateEnumeration, reference.opcfoundation.org/specs/OPC-30060/11.9]. Adopt the idea (small documented set of states, acting vs wait states, legal transitions), not necessarily the names.
- Display: current mode and state always visible; show which commands are legal and, for disabled ones, the blocking condition; show transient states with progress and timeout; faults carry cause, time and recovery steps; mode changes need explicit action and are logged.
- Transition table per machine: from-state, command or event, guard, to-state, side effects, who may request, HMI feedback.

Command lifecycle (verify; engineering practice):
1. Operator intent; UI-side checks for fast feedback.
2. Send with command ID (UUID), type, parameters, target, issuer, timestamp, expected state or revision.
3. Controller validates independently and answers ACCEPTED or REJECTED(reason) quickly (budget such as 200 ms).
4. Controller executes and reports progress and COMPLETED or FAILED(reason) keyed by the ID.
5. UI shows pending, accepted, done or failed; on timeout shows "outcome unknown, verify machine state". Never assume success.
6. Log every step with the ID.

Properties: idempotent (duplicate IDs ignored); absolute commands ("set to X", "open") over relative ("toggle", "+1"); stale commands discarded after a validity period or if the expected-state precondition fails; per-client sequence numbers; disable repeat until result; hold-to-run (jog) needs a continuous keep-alive and the controller stops when it ceases; error taxonomy: rejected, failed, timeout, refused-by-interlock (name the interlock).

Heartbeats (verify): bidirectional counters between HMI and controller to catch a frozen UI over a live socket; controller goes to defined safe behaviour when an HMI-originated enable or hold-to-run loses heartbeat (a process measure, not a certified safety function; ask the safety engineer); HMI marks all data stale and blocks commands when the controller heartbeat stops; example 5 Hz send, dead after 3 misses (600 ms); a supervisor restarts a frozen UI and state is rehydrated from the controller; each hop (sensor, controller, backend, UI) publishes its own freshness.

## 3. Single source of truth, staleness, reconnection

- The controller holds authoritative state; the HMI keeps a timestamped cache and never "optimistically" assumes a command worked. One store per process; screens subscribe; no second copies. Optimistic UI is allowed only for pure view feedback such as a pressed animation; show "pending" until confirmed.
- Every displayed value carries value, source timestamp, receive timestamp and quality. Age is derived from timestamps and the expected update period: older than about 3x the period means stale; link lost means unknown (verify). Never show a number that looks live when it is not.
- OPC UA status codes have severity Good, Uncertain, Bad; examples: Uncertain_LastUsableValue, Uncertain_NoCommunicationLastUsable, Bad_NoCommunication, BadWaitingForInitialData [V: OPC UA Part 8, reference.opcfoundation.org]. Ignition adds Bad_Stale = 516, "out-of-date based upon the requested refresh interval" [V: Ignition 8.3 quality codes docs].
- Map to a small display set (verify): Good; Stale/Uncertain; Bad/Unknown; Not yet received; Simulated/Overridden/Disabled. Stale keeps the value but de-emphasised with age and icon; Bad replaces the number with dashes and a symbol; global comms loss gets a banner with duration. Colour is never the only cue.
- Distinguish "link to controller lost", "controller reports sensor bad" and "value implausible"; they need different messages.
- On disconnect: disable controls that need the machine and say why; never queue dangerous commands to fire on reconnect. On reconnect: full snapshot resync before enabling controls, reconcile pending commands, re-check mode and state, backoff with jitter. Use revision numbers on snapshots and deltas to detect gaps.
- Clocks: monotonic clock for age and durations, wall clock for display; sync with NTP/PTP and warn on large skew.

## 4. Update rates, throttling, frame age, rendering

Perception anchors: about 0.1 s feels instantaneous, 1 s keeps flow of thought, 10 s keeps attention [V: Nielsen, Response Times: The 3 Important Limits, nngroup.com]. These are general UI numbers. All of the following are engineering defaults (verify), not standards:

| Item | Default |
|---|---|
| Touch feedback (pressed state) | under 100 ms |
| Command "received" | under 200 to 300 ms; show progress if completion exceeds 1 s |
| Live numeric values | 1 to 10 Hz; 10 to 20 Hz for smooth gauges; above 30 Hz is unreadable for numbers |
| Screen call-up | under 300 ms to first meaningful render |
| Alarm to display | about 1 to 2 s |
| Video | separate pipeline; drop frames rather than queue; always latest; show frame age |

Budget method: list each hop with worst-case latency (sensor sample, scan, bus, backend, network, render), sum, add jitter and retries.

Throttling: report by exception with deadband plus a periodic keepalive (so staleness detection still works); batch UI updates per animation frame; subscribe only to data on visible screens; prioritise alarms and state over bulk telemetry on one channel; downsample trends to pixel width.

Rendering: update only what changed (fine-grained reactivity); avoid layout thrash; animate with transforms; limit animation; test frame time and input latency on the target hardware, not the dev laptop (weak GPUs on embedded boards); soak for memory leaks over days; bound buffers; a scheduled restart is a mitigation only if state recovers cleanly; budget startup time and never block it on the network.

## 5. Multi-client control and remote access

Arbitration (verify):
- One controlling client per control scope; others observe. Controls on observers show "controlled by X".
- Explicit take and release; an indicator everywhere shows who has control. The device enforces; clients cannot self-grant. Control is a lease renewed by heartbeat.
- Local operator outranks remote; stop, hold and pause from any client are always allowed (stopping is safe, starting is not).
- Handover by request-offer-accept, or override with reason; notify the previous controller; log every change; on boot nobody controls.
- Test: two clients race; client drops mid-command; stale lease.
- Concurrency: recipes use revision numbers (optimistic concurrency) and show conflicts; commands carry the revision they were based on.

Local vs remote:
- The local HMI must run fully without internet or cloud; cloud is additive. Buffer events locally with store-and-forward and idempotent IDs; device wins for machine state, cloud wins for fleet configuration, with versioning (verify).
- Remote view is lower risk but still exposes data. Remote control needs authentication, MFA, time-limited sessions, local consent or presence, lockout by the local operator, extra audit, and a restricted command set (no motion; never hold-to-run over high-latency links).
- Show locally when a remote user is connected and what they may do; show data age on remote views.
- Connect via VPN or an outbound-only broker; no inbound port forwarding.

## 6. Logging and audit trail

Keep separate logs by purpose, with different retention and integrity (verify): operational events; operator actions (audit trail); alarm/event history (raise, acknowledge, return, shelve, suppress, out-of-service); process history; system diagnostics; security events; configuration changes.

Record fields: UTC timestamp with time source, sequence ID, severity, component, user or system, session/client ID, stable machine-readable event code plus text, before/after values with units, command ID, software and firmware version.

Rules (verify): carry command IDs end to end; no secrets, personal data only as needed; bounded storage with rotation and priority retention (audit and alarm outlive debug); detect disk full; tamper-evident (append-only, hash chain or external collector) where blame or regulation matters; viewable on the HMI with filters and exportable as CSV/JSON; one-click support bundle with sensitive data scrubbed; store codes plus parameters and render in the viewer's language.

21 CFR Part 11 as a reference model (not a requirement for most machines):
- 11.10(e) requires secure, computer-generated, time-stamped audit trails that record the date and time of operator entries and actions that create, modify or delete records; changes must not obscure earlier entries; retained as long as the records; available for agency review [V: eCFR 11.10, ecfr.gov, version 2026-10-01]. 11.10(d) limits access to authorised individuals [V: same].
- Non-biometric signatures need at least two distinct identification components; the first signing in a session uses all, later ones at least one owner-only component [V: 11.200(a)].
- FDA's 2003 scope-and-application guidance applies narrow interpretation and enforcement discretion for validation, audit trails, retention and copying; predicate rules still apply [V: fda.gov Part 11 scope guidance].
- HMI features implied: per-user login, credential re-entry on signing with a meaning ("Approved recipe v7"), reason-for-change, before/after display, immutable history, session timeout.

## 7. Recipes, config, versions, updates and rollback

Recipes and configuration (verify):
- Separate machine configuration, recipes/jobs, operator preferences and runtime state. Each has schema version, hash, author, timestamp, status (draft, approved, active, retired).
- Validate on load against schema and against controller limits. Gate approval of recipes and safety-relevant parameters by role or two persons.
- Always show "active recipe, version, modified?". Offer diff, backup, export/import with compatibility check. Factory reset needs elevated rights and is logged.
- Parameter metadata: unit, min, max, default, step, who may change, effect, restart needed.
- Never silently change setpoints on update; show migration notes. (A pre-release product may skip migrations; a fielded one cannot.)

Versioning:
- Semantic versions per component and a compatibility matrix (HMI x backend x firmware) checked at connect time.
- Handshake reports version, protocol version, capabilities; on mismatch refuse or degrade with a clear message ("Firmware too old for this software") rather than show wrong data.
- Additive fields are compatible; clients ignore unknown fields; removals or meaning changes bump major; enums carry an unknown fallback.
- Generate the shared schema for both sides. Show versions in About/Diagnostics, logs and support bundles. Release notes in operator language, tied to MOC.

Updates on field devices (checklist):
- [ ] Signed packages, signature checked on device.
- [ ] Compatibility check before applying.
- [ ] Only in a safe idle state; refuse during production; operator confirmation; progress shown.
- [ ] A/B partition or atomic swap with automatic rollback if the health check fails within N boots or minutes; keep last known good.
- [ ] Back up and preserve config, recipes, logs; power-loss-safe writes.
- [ ] Staged rollout (dev, hardware validation, fleet), canaries, ability to hold a site back.
- [ ] Post-update self-test and version report.
- [ ] Offline signed path (USB or technician tool).
- [ ] Controller firmware ordered by the compatibility matrix; never leave a fleet mixed and incompatible.
- [ ] Rollback documented and routinely tested; every update in the audit trail.

## 8. Localisation, units, time

Localisation (verify):
- All text in keyed resource files; no concatenated sentences; no text in images; ICU MessageFormat or equivalent for plurals and gender.
- Allow for text expansion (German, Finnish, Hungarian often 30 to 40% longer, approximate); test longest and shortest language and pseudo-localisation.
- Fallback chain; language switch reachable everywhere (login and error screens too), each language in its own name.
- Fonts for required scripts (CJK, Cyrillic, Arabic); right-to-left layout if needed.
- Native-speaking operators validate wording; alarm texts, codes and help share one system; codes stay language-neutral; spoken alerts localised too.
- Locale formats for separators, but consider a fixed unambiguous operator format (ISO 8601 dates).

Units:
- Store and transmit one canonical unit (SI); convert only at the UI edge; carry the unit in the data contract.
- Show the unit beside every number; entry uses the displayed unit and echoes the converted value on confirm; controller limit checks use canonical units.
- Avoid round-trip drift (convert for display only), handle offset units (temperature) and derived units, never reinterpret stored numbers on a unit change, handle a unit change while an edit field is open. Golden-value tests.

Time:
- Store UTC (ISO 8601 with offset); display in a configured zone and label the zone for remote or exported views.
- Device clock from NTP or local source plus RTC; handle jumps (monotonic for durations); log sync events; warn when unsynced.
- Handle DST ambiguity; schedule in UTC or explicitly. Keep source and server timestamps for event ordering across controller, backend and HMI.

## 9. Diagnostics, help, training, simulation

Diagnostics and maintenance screens (verify):
- Content: versions, uptime, IDs, time sync; link status, latency, loss, last message age, reconnect counts; raw and scaled I/O with quality, forced and simulated flags; health (temperature, voltage, storage, CPU); calibration and wear counters; log viewer, support bundle, self-test; fault history with recovery steps.
- Manual operation (jog, test outputs) gated by role, maintenance mode and interlocks; visible banner; auto-exit.
- Overrides and simulation are flagged, auto-expire, listed on an "active overrides" page and in handover reports.
- Separate from operator screens, role-protected; plain language first, detail expandable; never mix test and production controls.

Help and training:
- Per-screen help; inline hint text (what, units, limits) because tooltips fail on touch; messages carry cause, action and a help link; guided checklists for rare tasks (part change, post-e-stop recovery, calibration); help works offline, localised, versioned with the software; first-run guide and role-based tours; quick-reference cards and QR links to current manuals.
- Training/demo mode: unmistakable persistent banner and distinct look; cannot command real hardware (separate data path by build or process isolation, not just a UI flag); scripted fault injection (comms loss, sensor fail, alarm flood); records tagged or segregated.

Simulation/mock architecture (verify): define the controller interface so a simulator can implement it (ports and adapters); the mock must show realistic timing, noise, delay, dropped messages and faults; use declarative scenario scripts ("at t=10 s sensor X goes bad"); the same mock serves development, automated tests, demos, training and usability tests; mock mode is explicit in UI and logs.

## 10. Technology choices

| Option | Pros | Cons and cautions |
|---|---|---|
| Browser/HTML served locally | Fast iteration, ecosystem, same UI local and remote, easy localisation, web test tools | Hardened kiosk browser needed; CPU/RAM on embedded; exposed server risk; browser update churn (verify) |
| Electron | Desktop shell, offline package, native integration | Heavy; you own Chromium patching; only the three latest stable majors are supported, majors follow Chromium on an 8-week cycle (summary: electronjs.org timelines, page not fetched) |
| Tauri / webview wrapper | Small footprint, Rust backend | System webview differs across OS versions; fewer plugins (verify) |
| Ignition Perspective | Web-native, responsive, quality overlays, scripting | Licensing and gateway-centred; runs in the browser, no Java client, responsive, iOS/Android app [V: Inductive Automation Perspective docs 8.3]; session and licensing claims unverified |
| WinCC Unified | Web runtime integrated with TIA Portal | Vendor lock-in; HTML5/SVG/JavaScript runtime in standard browsers (summary: Siemens 2019 press release; no official docs page found) |
| Qt (QML/Widgets) | Native performance on embedded Linux, deterministic rendering | C++/QML skills; GPL/LGPL/commercial and a Device Creation distribution licence (summary: qt.io FAQ); LGPL duties need legal review |
| Vendor panel HMIs | Integrated, proven | Limited UX freedom, cost, specialised skills (verify) |
| Custom native (C#, Flutter, Rust) | Total control | You build widgets, accessibility and test tooling (verify) |

Choose by lifecycle (industrial gear lasts 10 to 20 years: check framework and OS support horizon), update path, hardware, team skills, remote needs, certification demands (verify). Pin dependency versions and plan security patches. No vendor comparison was hands-on tested.

## 11. Security

### 11.1 IEC 62443 in brief
- Zones and conduits: group assets of similar security need into zones, control traffic between them via conduits, each with a target security level from risk assessment (summary).
- Security levels: SL1 casual or coincidental violation; SL2 intentional, simple means, low resources; SL3 sophisticated means, moderate resources, IACS-specific skills; SL4 sophisticated, extended resources (summary: secondary overviews; wording not verified in the standard).
- Seven foundational requirements [V: ISA-62443-3-3 preview PDF, scope]: identification and authentication control (IAC); use control (UC); system integrity (SI); data confidentiality (DC); restricted data flow (RDF); timely response to events (TRE); resource availability (RA). About 51 system requirements (SRs) with per-SL enhancements (summary; count unconfirmed).
- Parts: 3-2 risk assessment and zoning; 3-3 system requirements; 4-1 secure development lifecycle; 4-2 component requirements (embedded, host, network devices, applications; an HMI is a host or embedded device plus application, my reading); 2-1 and 2-4 programme and service-provider requirements (verify).
- Relevant SRs (from blog and secondary lists, numbering (verify) against the standard): SR 1.1 human user identification and authentication on all interfaces including the HMI, with unique IDs at SL2 and multifactor over untrusted networks at SL3; SR 1.3 account management; SR 1.5 authenticator management (change default credentials); SR 1.11 unsuccessful login attempts; SR 1.13 access via untrusted networks; SR 2.1 authorisation enforcement (role-based); SR 2.8 auditable events, SR 2.9 audit storage, SR 2.11 timestamps.
- Mapping to an HMI (synthesis, verify): IAC unique accounts, lockout, no hard-coded or default passwords; UC server-side role enforcement, least privilege, session lock; SI signed updates, input validation, safe parsing; DC TLS in transit and protected secrets; RDF segmentation, only needed ports; TRE security logging and time sync; RA rate limits, backups, safe behaviour on loss of HMI.
- Supplier deliverables (verify): zone diagram, port and service list, SBOM, vulnerability disclosure and patch policy, hardening guide, default-credential policy.

### 11.2 Authentication on shared terminals
Never ship shared or hard-coded PINs or passwords (a fixed admin PIN in the source is a vulnerability, not a feature). Rules (verify):
- Safe actions (view, pause, stop) need no login; risky ones require identity. Emergency access must never depend on login.
- Options: individual user plus password (best audit, slow on touch); per-user PIN with lockout and rate limit; RFID/NFC badge (fast, glove-friendly, shareable); badge plus PIN for elevated roles; central identity (directory or SSO) with a local cache or break-glass for outages; fingerprint (glove problems, special-category data under GDPR). Shared generic accounts only as a last resort, logging station and shift.
- Short idle timeout with re-auth for elevated roles; visible "logged in as"; fast user switch without losing machine state; elevated sessions time-boxed and visibly distinct.
- No default credentials; force change at first use; per-device unique secrets; local secrets hashed with a slow KDF (argon2, bcrypt, scrypt, PBKDF2).
- Break-glass access is documented, logged, alarmed and reviewed.

### 11.3 RBAC
Roles come from the persona table: Viewer, Operator, Supervisor, Maintenance, Service engineer, Admin, Auditor. Build a permission matrix (rows: start, pause, change setpoint in limits, change limits, acknowledge, shelve alarm, edit and approve recipe, maintenance mode, manual jog, network change, firmware update, user management, export logs, view audit; columns: roles; cells: allowed, with signature, with second person). Enforce in the backend and controller, not by hiding buttons; show disabled controls with the reason; separate duty (who changes safety parameters is not who approves); periodic access review and joiner/leaver process; scope per site or machine; negative tests (operator token calling an admin API) (verify).

### 11.4 Kiosk hardening checklist (verify)
- [ ] Minimal OS, controlled update windows, boot straight to the app as an unprivileged user, supervisor restarts on crash.
- [ ] Read-only root or overlay, separate writable data partition.
- [ ] Disable OS shortcuts, devtools, address bar, right-click, new windows, file dialogs, print, virtual terminals.
- [ ] USB mass storage off or allow-listed; external boot disabled; BIOS/UEFI password; disk encryption where theft matters.
- [ ] Webview with CSP, navigation allow-list to local origin, no remote content or extensions.
- [ ] Default-deny local firewall; documented listening ports.
- [ ] No default accounts; SSH off or key-only, for maintenance.
- [ ] On-screen keyboard only for text fields; OS popups cannot cover the HMI.
- [ ] Lockable enclosure and port covers where justified.
- [ ] A documented authenticated service mode, so staff do not invent insecure ones.

### 11.5 CISA exposure lessons
- CISA/EPA fact sheet (December 2024) on internet-exposed HMIs in water systems: attackers could view the GUI, system maps and event logs, and in some cases changed administrative passwords to lock operators out. Advice: inventory exposed devices, disconnect from the public internet where possible, otherwise strong passwords, change defaults, MFA for all HMI and OT access, segment via DMZ or bastion host [V: EPA-hosted joint fact sheet PDF].
- CISA et al. (published 2024-05-01) on pro-Russia hacktivists: HMIs manipulated through VNC, including port 5900, using default and weak passwords with no MFA; activity since 2022 and as recently as April 2024; pumps and blowers pushed beyond normal parameters; some compromised HMIs were unsupported legacy rebranded devices [V: cisa.gov PDF].
- Censys research reported about 400 exposed web HMIs in US water facilities, roughly 40 fully unauthenticated and controllable from any browser (summary: press coverage of Censys).
- Product rules (derived, verify): remote services off by default; never bind to 0.0.0.0 unless configured; authenticate every connection, read-only included; no VNC passwords as the control and no security by obscure port; outbound-initiated broker or VPN; MFA for remote sessions; separate view and control rights; session recording and time limits; source allow-lists and rate limits; local indication of active remote sessions and an easy local off switch; hardening guide, SBOM, CVE tracking and a patch SLA for Chromium, Node, Electron, OS and libraries.
- The controller must not trust any client merely because it is on the LAN; use authenticated clients (OPC UA security policies with certificates, MQTT with TLS and per-client credentials) (verify).
- Secrets shipped inside binaries can be extracted; if unavoidable, scope them narrowly, make them rotatable, and record the risk in the threat model (verify).
- Secure development: STRIDE threat model per zone, assume a hostile LAN; validate every message and import with schema and size limits; no shell execution from inputs; lockfiles, SBOM and CI vulnerability scanning; fuzz protocol parsers; run without root; state a support and end-of-life period (verify).

### 11.6 GDPR for operator activity data
Not legal advice; involve a DPO or lawyer. Login, audit trails and telemetry are personal data when they identify a person.
- Design to Art. 5(1): lawfulness and transparency, purpose limitation, minimisation, accuracy, storage limitation, integrity and confidentiality [V: gdpr-info.eu Art. 5]. Practical mapping (verify): log what safety, quality and traceability need; set retention per log type; restrict per-person logs; do not use safety audit logs for performance ranking unless declared and lawful.
- Art. 88 lets Member States set employment-specific rules and safeguards for monitoring at work [V: gdpr-info.eu Art. 88]; national rules and works-council co-determination vary (verify).
- Employee consent is unlikely to be valid; employees must be told of monitoring (summary: WP29 Opinion 2/2017 law-firm summaries).
- Prefer badge plus PIN to fingerprints (special-category data, Art. 9) (verify); pseudonymise operator IDs in cloud sync and document transfers outside the EEA (verify).

### 11.7 Safety-rated HMI components
Display and touch layers are not safety devices. E-stops and three-position enabling switches are separate certified components wired into safety logic. A three-position enabling switch permits operation in the middle position and a stop when released; IEC 60947-5-8 covers them (summary: standards catalogue entries). Whether a handheld or wireless terminal reaches a given performance level depends on the vendor's certified safety function and your own calculation: ask for the PL/SIL certificate and PFHd and test link-loss behaviour (verify). The display shows safety state read from the safety controller as information only. ISO 13849-1 PL a to e map to PFHd bands from 1e-5..1e-4 (a) up to 1e-8..1e-7 (e) (summary: Schneider and Reer via search).

## 12. Testing

Pyramid (verify): (1) unit tests of pure logic (unit conversion, state mapping, quality-to-display, permissions); (2) component tests of each toolkit element in every state (normal, stale, bad, disabled, pending, fault) with long localised strings; (3) contract tests of schemas and version compatibility; (4) integration against a simulator including faults; (5) end-to-end UI automation of key journeys; (6) hardware-in-the-loop; (7) FAT and SAT; (8) soak, performance and security; (9) usability validation (process.md section 8).

UI automation:
- Web or Electron: Playwright, Cypress, Selenium, WebdriverIO; Qt: Qt Test or Squish; image-based tools last (verify).
- Stable test IDs, not text or CSS paths; mock backend over the real protocol; fake timers for staleness.
- Automate: boot with no backend (shows disconnected), connect, normal run, command accept/reject/timeout, comms drop and resync, role limits, every locale (no overflow), unit switch, illegal commands per mode, alarm raise/ack/clear, control races.
- State-machine property tests: random event sequences with invariants ("Start is never enabled in Faulted"; "no value appears live when older than its threshold").
- Fault injection: dropped, delayed, duplicated, reordered messages; malformed data; bursts; clock jumps.

Visual regression: screenshot every toolkit state and key screen per language and theme at target resolution; perceptual diff with tolerance; reviewed in code review; pin fonts and the rendering image; sample on real hardware; stress with worst-case data (longest strings, max digits, negatives, all alarms active).

HIL and simulation: plant simulation or recorded replay into the real controller; include scan time, jitter, bus errors; cases: power loss, controller reboot with HMI running, HMI reboot with machine running, cable pulled, partial sensor failure, firmware mismatch; replay field logs as regressions; multi-day soak on target hardware.

HMI test plan outline (verify): scope and versions; traceability matrix (requirement, test, evidence); environment and baseline; roles, entry/exit, defect severity; levels and strategy; functional; abnormal situations (comms loss, stale, controller restart, HMI crash, power cycle, firmware mismatch, disk full, clock jump); safety checks (pull HMI power and confirm the machine reaches a defined state; e-stop works with HMI dead; controller rejects invalid commands sent directly); security (auth, RBAC negatives, port scan, default credentials, bad signature, kiosk escape, remote settings); localisation and units; performance (latency, rates, frame time, soak, startup); usability; compatibility and rollback; documentation; FAT/SAT scripts; regression schedule tied to MOC class; reporting. Test case fields: ID, objective, preconditions, steps, expected, actual, result, evidence, tester, date, versions.

## 13. Common mistakes
- Treating the HMI as a safety function, or letting its loss leave motion running.
- UI-only validation; trusting any LAN client.
- Showing the last number as if live; no comms-loss banner; controls left enabled when disconnected.
- Toggle commands, no command IDs, assuming success when the send returns.
- Two stores holding the same value.
- Shared or hard-coded PINs; default passwords; VNC or web server exposed to the internet.
- Hiding buttons instead of enforcing roles server-side.
- Text in images, concatenated translations, unit conversion on stored values.
- Mock or training mode that is just a UI flag and can reach real hardware.
- Updates without signatures, compatibility checks or rollback; mixed fleets.
- Tests only on the dev laptop; no fault injection.

## 14. Sources
- OPC UA PackML states: https://reference.opcfoundation.org/specs/OPC-30060/11.9 ; Part 8 status codes: https://reference.opcfoundation.org/specs/OPC-10000-8/7.3
- Ignition: https://docs.inductiveautomation.com/docs/8.3/ignition-modules/perspective ; quality codes: https://docs.inductiveautomation.com/docs/8.3/platform/tags/quality-codes-and-overlays
- Nielsen response times: https://www.nngroup.com/articles/response-times-3-important-limits/
- 21 CFR 11.10: https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11/subpart-B/section-11.10 ; FDA Part 11 scope guidance: https://www.fda.gov/regulatory-information/search-fda-guidance-documents/part-11-electronic-records-electronic-signatures-scope-and-application
- ISA-62443-3-3 preview: https://www.isa.org/getmedia/d73509e9-b626-4709-a406-be6fc7616b79/ISA-62443-3-3_Preview.pdf
- CISA/EPA internet-exposed HMIs (Dec 2024): https://www.epa.gov/system/files/documents/2024-12/joint-factsheet-epa-cisa-internet-exposed-human-machine-interfaces-508c.pdf
- CISA et al. pro-Russia hacktivists (May 2024): https://www.cisa.gov/sites/default/files/2024-05/defending-ot-operations-against-ongoing-pro-russia-hacktivist-activity-508c.pdf
- GDPR Art. 5 and 88: https://gdpr-info.eu/art-5-gdpr/ , https://gdpr-info.eu/art-88-gdpr/
- Not read: IEC 62443 parts, ISO 13849, ISA-88, IEC 60947-5-8 normative text; Electron, Siemens, Qt pages are summaries.
