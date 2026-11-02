# Evaluating skill behavior

Static validation and Python helper tests run in CI. They do not execute an LLM.
The cases below are evaluation inputs and rubrics, not recorded passing results.

1. Use the skill's `evals/triggers.json` prompts to check selection, including
   near-misses. Record the selected skills, agent/model version and prompt.
2. Run behavior cases with and without the skill, using identical task evidence
   and an isolated workspace. Do not contact machinery or live systems.
3. Grade against the expected decisions, not wording or formatting. Record missing
   evidence and refusals to make unsupported claims. Inspect generated artifacts.
4. Repeat after substantive changes. Report limitations; a self-review or static
   check is not an independent model evaluation.

- [Full-skill activation cases](../skills/hmi-design-full/evals/triggers.json)
- [Full-skill behavior cases](../skills/hmi-design-full/evals/cases/README.md)
- [Light-skill activation cases](../skills/hmi-design-light/evals/triggers.json)
- [Light-skill behavior cases](../skills/hmi-design-light/evals/cases.md)
- [Leptos activation cases](../skills/leptos-hmi/evals/triggers.json)
- [Leptos behavior cases](../skills/leptos-hmi/evals/cases.md)
