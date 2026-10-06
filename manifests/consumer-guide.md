# AI Skills Sync Consumer Guide

## Minimal implementation

A third-party agent does not need a dedicated plugin to consume this profile.

### Discovery

Fetch:

1. `registry.json`
2. `profile.json`
3. `PROTOCOL.md`

Require:

- `protocol == ai-skills-sync/v1`
- `registry.repository == profile.repository`
- `registry.canonical_root == ~/.agents`

### Loading

Each registry entry supplies:

- `id`: stable component identifier
- `path`: repository-relative source path
- `format`: content format
- `scope`: intended installation scope
- optional `version`
- optional `sha256`

A consumer may load all components or only selected entries.

### Local mirror

When a consumer supports a local profile directory, map repository paths directly below:

```text
~/.agents/
```

Do not remove files that are not registered by this profile unless the user explicitly requests pruning.

### Integrity

When `sha256` is present, calculate SHA-256 over the downloaded bytes and compare it with the registry value before installing the component.

When no checksum is present, the component remains valid but integrity verification is unavailable.

### Credentials

Public repositories require no credential for read-only discovery.

Private repositories must be accessed with credentials owned by the consuming agent. Never copy those credentials into this profile.

### Compatibility

Unknown optional fields must be ignored. A consumer must reject an unsupported protocol identifier rather than guessing its semantics.
