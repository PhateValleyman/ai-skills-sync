# AI Skills Sync

## Purpose

This repository is the portable, GitHub-native source of truth for the user's AI profile: skills, agents, plugins, knowledge, manifests, and compatibility metadata.

## Architecture

- GitHub is the primary backend and source of truth.
- The repository must work without CI/CD, GitHub Actions, a VPS, Docker, or a continuously running service.
- GitLab and local `~/.agents` installations are mirrors/adapters, not required infrastructure.
- Third-party agents should be able to discover the profile from `registry.json` and load only the components they need.
- Credentials and secrets must never be stored in this repository.
- `tools/ai-skills-sync.py` is a dependency-free reference consumer; it is a bootstrap utility, not a managed profile component.

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
8. `registry.json` is the machine-readable discovery index; update it whenever registered components are added, removed, renamed, or structurally changed.
9. Registry entries should point to canonical repository paths and must not require a running service or generated cache.
10. The reference synchronizer must validate the v1 protocol and repository identity before installing components.
11. The reference synchronizer must verify declared `sha256` values when present and must reject unsafe component paths.
12. Synchronization must preserve unmanaged local files; pruning is never implicit.
13. Synchronizer state belongs under `~/.agents/manifests/.ai-skills-sync-state.json` and must never contain credentials.
