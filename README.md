# HMI Skills

Three agent skills for designing and building operator interfaces for machines,
industrial processes, and field equipment.

Free to use, modify, and redistribute under the [MIT License](LICENSE).

## Skills

| Skill | What it does |
| --- | --- |
| [hmi-design-full](skills/hmi-design-full/SKILL.md) | Detailed HMI design and review: states, commands, alarms, safety boundaries, legibility, and operator testing. |
| [hmi-design-light](skills/hmi-design-light/SKILL.md) | Compact guidance for layout, navigation, visual hierarchy, and operator wording. |
| [leptos-hmi](skills/leptos-hmi/SKILL.md) | Leptos/Tauri implementation guidance. Use alongside one of the HMI design skills. |

Each folder contains its instructions and supporting references. The full skill
also includes its original Python helpers for contrast, physical sizing, and
finding hardcoded styling values. They are optional and use Python's standard
library; reading the skills requires no dependencies.

## Install

Copy the desired folders from `skills/` into your agent's skill directory, or use
the [Skills CLI](https://github.com/vercel-labs/skills):

```sh
npx skills add TthBnc/hmi-skills
```

## Use

```text
$hmi-design-full Review this machine's operator interface.
$hmi-design-light Simplify this station screen's layout and wording.
$leptos-hmi Build this operator screen using our existing Leptos components.
```

References distinguish source-backed guidance from summaries and unverified
starting points. These skills do not certify machine safety or replace testing
on the actual equipment. External standards remain their owners' material.

## License

[MIT](LICENSE). Each skill includes a license copy for independent redistribution.
