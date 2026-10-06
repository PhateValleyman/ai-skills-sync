# ai-skills-sync

Portable, GitHub-native AI profile for sharing and synchronizing skills, agents, plugins, knowledge, and manifests across AI agents and devices.

## Design goals

- GitHub-only operation for the core profile.
- No CI/CD or GitHub Actions required.
- No server, database, Docker, or daemon required.
- Third-party agents can discover the profile from `registry.json`.
- Local installations can mirror the profile into `~/.agents/`.
- GitLab can be added later as a mirror.
- Secrets stay outside the repository.

## Repository layout

| Path | Purpose |
|---|---|
| `registry.json` | Machine-readable discovery index |
| `profile.json` | Profile identity and protocol metadata |
| `skills/` | Reusable agent skills |
| `agents/` | Agent definitions |
| `plugins/` | Plugin definitions and metadata |
| `knowledge/` | Portable shared knowledge |
| `manifests/` | Installation and synchronization manifests |
| `schemas/` | JSON schemas for validation |

## Third-party agent integration

A compatible agent only needs read access to this repository.

1. Read `registry.json`.
2. Read `profile.json`.
3. Select the required component from the registry.
4. Fetch the referenced file.
5. Follow the component's own instructions.

For a public repository, read-only discovery requires no credential.

## Security

Never store credentials in this repository. GitHub/GitLab/API credentials belong in the consuming agent's credential store or environment.

## Status

Initial protocol/profile skeleton. The format is intentionally small and extensible.
