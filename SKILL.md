# AI Skills Sync

## Purpose

This repository is the portable, GitHub-native source of truth for the user's AI profile: skills, agents, plugins, knowledge, manifests, and compatibility metadata.

## Architecture

- GitHub is the primary backend and source of truth.
- The repository must work without CI/CD, GitHub Actions, a VPS, Docker, or a continuously running service.
- GitLab and local `~/.agents` installations are mirrors/adapters, not required infrastructure.
- Third-party agents should be able to discover the profile from `registry.json` and load only the components they need.
- Credentials and secrets must never be stored in this repository.

## Canonical local layout

```
~/.agents/
├── skills/
├── agents/
├── plugins/
├── knowledge/
├── manifests/
└── config.toml
```

## Repository mapping

- `~/.agents/skills/` -> `skills/`
- `~/.agents/agents/` -> `agents/`
- `~/.agents/plugins/` -> `plugins/`
- `~/.agents/knowledge/` -> `knowledge/`
- `~/.agents/manifests/` -> `manifests/`

## Rules

1. Preserve existing reusable guidance unless disproven.
2. Never commit passwords, API keys, private keys, access tokens, session cookies, or other secrets.
3. Keep the registry machine-readable and stable.
4. Prefer portable Markdown, JSON, TOML, and plain-text formats.
5. Changes to this architecture must be reflected in this SKILL.md.
6. Validate Markdown and JSON before publishing changes.
7. Keep the core usable by an arbitrary third-party agent that can read GitHub content.
