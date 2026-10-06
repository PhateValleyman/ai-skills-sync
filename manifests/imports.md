# Import manifest

This file records reusable profile components that have been imported into this repository.

## Imported

- `Global_project_workflow.md` -> `skills/global-project-workflow/SKILL.md`
  - Scope: global
  - Version: 1.0.0
  - Secrets: none

## Pending discovery

The previously supplied `skill.zip` is referenced by the profile history, but its archive contents are not currently exposed as a directly readable Library file in this session. Do not invent or reconstruct missing SKILL.md content. Import each skill only after its actual source content is available.

## Import rules

- Preserve source language and semantics.
- Do not silently rewrite an existing skill.
- Normalize only repository metadata/front matter when required by the protocol.
- Never import credentials or other secrets.
- Add every imported component to `registry.json`.
