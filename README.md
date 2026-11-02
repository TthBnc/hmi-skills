# HMI Skills

Agent skills for designing and implementing operator interfaces for machines,
industrial processes, inspection stations, and field equipment.

| Skill | Use it for |
| --- | --- |
| [hmi-design-full](skills/hmi-design-full/SKILL.md) | Detailed design and review: safety boundaries, state and command feedback, alarms, data quality, physical ergonomics, and operator testing. |
| [hmi-design-light](skills/hmi-design-light/SKILL.md) | A compact pass on layout, navigation, wording, and visual hierarchy. Escalate to the full skill for safety or detailed behavior. |
| [leptos-hmi](skills/leptos-hmi/SKILL.md) | Leptos 0.7/0.8 CSR components, live data, tokens, touch interaction, and Tauri/kiosk implementation. Pair with a design skill. |

## Install

Using the [Skills CLI](https://github.com/vercel-labs/skills):

```sh
npx skills add TthBnc/hmi-skills
```

Choose individual skills and supported agents interactively, or select explicitly:

```sh
npx skills add TthBnc/hmi-skills --skill hmi-design-full --skill leptos-hmi
```

For a reproducible source revision, clone a release tag and install from that
local directory. You can also copy complete skill directories into the skill
location documented by your agent. Keep each folder's `references`, `scripts`,
`agents`, and `LICENSE` files together. Do not overwrite existing local edits.

## Use

Example prompts (explicit `$skill-name` syntax depends on the agent):

- “Use $hmi-design-full to review this machine's operator screens. Separate
  findings from items that need a real-device test.”
- “Use $hmi-design-light to simplify the navigation and operator wording.”
- “Use $leptos-hmi with $hmi-design-full to implement a gloved-operator screen
  using our existing Leptos components.”

The skills use the open [Agent Skills format](https://agentskills.io/specification):
short YAML frontmatter, focused entry points, and on-demand references. Optional
`agents/openai.yaml` files provide Codex discovery metadata. They are not needed
by other compatible clients. There is no MCP server, credential, runtime daemon,
or required network connection to read the installed skills. Verify current
primary documentation when the task depends on changing APIs or standards.

## Helpers

The full skill includes Python 3.11+ utilities with no third-party runtime dependencies:

```sh
python3 skills/hmi-design-full/scripts/contrast.py '#111111' '#ffffff'
python3 skills/hmi-design-full/scripts/sizing.py --ppi 150 --distance-mm 700
python3 skills/hmi-design-full/scripts/lint_tokens.py path/to/ui
```

Contrast computes an sRGB color ratio, not measured panel contrast under glare.
Sizing calculations distinguish physical/device pixels from CSS pixels; measure
on the actual panel. The token scanner is advisory and may report false positives.

## Scope and evidence

These are design and implementation aids, **not a safety-certified controller,
conformity assessment, or substitute for a machine risk assessment**. They grant
no permission to operate equipment or modify a live installation. Physical
legibility, glove use, stopping behavior and interlocks require appropriate
real-device validation.

References preserve research annotations and distinguish direct-source notes,
secondary summaries and unverified heuristics. An annotation is not a current
certification claim. See [source provenance](skills/hmi-design-full/references/source-provenance.md).
External standards and linked publications are not redistributed or relicensed.

## Validation and contributing

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python scripts/validate.py
.venv/bin/python -m unittest discover -s tests -v
```

CI checks all three skills using the official `skills-ref` validator, local
references and metadata, and helper behavior. It does not prove model quality or
machine safety. [Evaluation cases](docs/evaluations.md) cover realistic activation
and behavior; model-based evaluations are manual and must be reported separately.
See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE). Each skill includes its own license so it remains licensed when
installed independently.
