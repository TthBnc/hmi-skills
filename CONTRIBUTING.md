# Contributing

Keep each skill independently installable. Use the Agent Skills frontmatter
fields; keep descriptions specific and entry points short. Add detailed guidance
under references only when it changes a decision. Do not add permissions or
assume a particular agent's tools. Declare companion skills in the instructions.

Preserve source attribution and distinguish requirements from conventions.
For a standard-related correction, cite the edition and primary source where
available; do not paste licensed standards. No private paths, factory mappings,
credentials, operator records, or proprietary project material belong here.

Run both README validation commands. Add helper regression tests for meaningful
behavior changes and evaluation prompts for changes to skill routing or advice.
Never report an evaluation as executed unless it actually ran; record the agent,
model/version, prompt, artifacts and limitations when reporting results.

Changes to safety-related guidance need review against the specific safety
architecture. A contribution or passing CI does not authorize live equipment
operations. Describe any uncertainty directly in the reference.
