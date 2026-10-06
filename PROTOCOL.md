# AI Skills Sync Protocol v1

## Purpose

AI Skills Sync is a GitHub-native profile distribution protocol. A compatible AI agent can discover a profile, select components, and mirror them locally without requiring a server, daemon, CI/CD pipeline, Docker, or GitHub Actions.

## Discovery contract

A compatible consumer starts with `registry.json`, then `profile.json`, then the component paths referenced by the registry.

The registry is authoritative for component discovery. Component files are authoritative for their own content and instructions.

## Canonical layout

Repository paths map directly below the consumer profile root:

```text
~/.agents/
├── skills/
├── agents/
├── plugins/
├── knowledge/
├── manifests/
└── config.toml
```

For example, `skills/redmi/SKILL.md` maps to `~/.agents/skills/redmi/SKILL.md`.

## Synchronization model

The protocol is pull-based:

- GitHub repository = source of truth.
- Consumer = reader and optional local mirror.
- Synchronization is explicit or scheduled by the consumer.
- No remote service is required.
- Empty component categories are valid.

Recommended sequence:

1. Fetch `registry.json`.
2. Validate the protocol identifier.
3. Fetch `profile.json`.
4. Validate the repository identity.
5. Select components from `components`.
6. Fetch each referenced path.
7. Verify optional checksums when present.
8. Write files below the canonical local root.
9. Preserve unmanaged local files unless pruning was explicitly requested.
10. Record installed profile state when supported.

## Security model

The repository contains portable instructions and metadata, not credentials.

Never synchronize API keys, OAuth tokens, GitHub/GitLab personal access tokens, private SSH keys, passwords, session cookies, browser profiles, or other authentication material.

A consuming agent may use its own credential store to access a private repository. The profile itself must not contain credentials.

## Compatibility

The protocol identifier is `ai-skills-sync/v1`.

Consumers should ignore unknown optional fields to preserve forward compatibility. Breaking protocol changes require a new protocol identifier.

## Partial synchronization

Consumers may install only selected categories or components. A partial profile remains valid.

If a component path is unavailable, the consumer should report the failed path and continue only when its policy permits partial synchronization.

## GitHub access

For a public repository, registry and component reads require no GitHub credential. For a private repository, the consumer supplies its own read credential through its normal credential mechanism.

The protocol does not mandate a GitHub API implementation. Raw repository content, GitHub APIs, or a Git client are acceptable if they provide equivalent read access.
