# Game online leaderboards

Read this only when the requested game needs a shared online leaderboard. Keep local scores by default;
adding a board does not add a Blueprint category. This page owns the optional network integration.
Read the shared sections with the recorded `gameEngine`'s integration section only.
Three.js uses [Web checkpoints](git-checkpoints.md) and [Web deployment](deployment.md);
Godot uses [Game delivery](game-delivery.md). Player data belongs to this game's project database
and API, never the Addon Server database or a Manus chat session.

## Shared setup

Read [configuration](configuration.md), [features](features.md), [database](database.md),
[publish container](build-contracts.md#container-build) and [routes](routing-and-responses.md#published-routes)
together in one parallel tool call before configuring infrastructure.
GET the existing config first; preserve other declared fields. Through the existing registered config
tool, verify `features.server` and `features.database` are enabled for the requested online capability.
New Games initialize with both capabilities off. After leaderboard selection is approved in the
[Blueprint](game-blueprint.md#online-features), enable missing capabilities through config; existing games use the
same config flow when adding leaderboards. Enablement provisions infrastructure, not the leaderboard API or tables.
These capabilities cannot be assumed reversible and can incur hosting costs.

## Three.js

Use the installed runtime's `install-leaderboard.mjs` and `leaderboard-reference/`; no Godot download or
starter upgrade is needed. These are opt-in project additions: an Addon update does not update existing
games. Keep `pnpm build` → `dist`, the project database and Web hybrid `/api/*` server routes.

1. If Manus login is selected, first follow [Game authentication](game-authentication.md)'s Three.js
   installation, then choose `identity: "account"`. Otherwise choose `identity: "guest"`.
2. Author a project-owned configuration file with the game's immutable board identifiers, for example:
   `{"identity":"account","boards":[{"id":"score-v1","rulesVersion":"v1"}]}`.
   From the project root run `node <game_dev_runtime_dir>/install-leaderboard.mjs <config-file>`.
   Merge the returned `configurationPatch` through the existing config API and read it back: server and
   database enabled, `server/Dockerfile`, startup health `/api/health`, `/api/*` → server followed
   by `/*` → static. The installer does not apply config or execute migrations.
3. Review `server/leaderboard/migrations/`, add the next numbered migration defining the game's board,
   score limits and duration rules, then run `npm --prefix server run db:migrate:leaderboard` only through
   the authorized project database workflow. Account mode also needs the canonical users migration from
   auth setup. Never edit applied migrations. Install server/frontend dependencies and commit lockfiles.
4. Import `createLeaderboardClient` from `../leaderboard.js` in `src/main.ts`. Configure the same
   `identity`, `boardId` and `rulesVersion`; in account mode pass the imported `ManusAuth` as `auth`.
   Guest mode calls `ensureGuest(displayName)` explicitly before ranked play and preserves its token.
   A custom guest client sends the token as both `Authorization: Bearer` and `X-Guest-Token`: Preview can
   strip `Authorization`, and older copied backends read only `Authorization`.
   Call `beginRun()` when gameplay starts, `submitRun(ticket, score, durationMs)` at settlement, and
   `retryRun(ticket)` after a failed submission. Results are `{ok:true,value}` or `{ok:false,error}`;
   display real errors while local gameplay continues independently. Do not invent a run or global rank.
   The client keeps the original payload for retry and refreshes the board after submission; a failed
   refresh is returned separately from an accepted receipt. `list()` refreshes without a write.

Account mode calls `game.leaderboard.list`, `beginRun`, `submitRun` through canonical Webdev tRPC/session.
Writes are protected and derive identity only from `ctx.user.id`. Public ranking remains readable without
login; personal rank requires a session. `game_lb_accounts` permanently maps the integer Webdev user key
inside the project database, independent of guest expiry. Authentication failure never falls back to a
guest. Account mode permits only health and GET through REST; all REST writes return 403
`account_session_required`, even with an existing guest token. Guest mode retains the original REST write
flow. Existing guest scores remain readable, but are not automatically merged into account scores.
Client-selected user/player IDs are rejected. Scores remain client-reported casual rankings.

The installer preserves customized backends. For an existing service, integrate the exported
`createLeaderboardRuntime` and `createLeaderboardRouter` using the existing Webdev `router`,
`publicProcedure` and `protectedProcedure`; mount `leaderboard.middleware` in that same app before
body parsing, then add `leaderboard` under the existing `game` router. See the packaged reference README
for wiring. Do not start a second listener or duplicate scoring logic. Reconcile old project files and
migration history explicitly; rerunning the installer is not an upgrade command.

Leaderboard readiness at `/api/leaderboards/v1/health` checks the declared boards and required account
columns. Apply additive migrations before the checkpoint so its checkpoint database branch includes
them. Use the normal Web checkpoint and hybrid
publish flow; verify the selected Preview's login, ranked run, result refresh, cross-device continuity
and database isolation before claiming online acceptance. Local protocol/build tests are separate from
CI, deployment and live acceptance. Preserve the published Origin policy and injected environment.

## Shared schema and scoring

Use the selected engine's finite migration command: Three.js uses `npm --prefix server run db:migrate:leaderboard`;
Godot uses `npm --prefix server run db:migrate`. Run it against this game's managed project database only,
under the normal database-change rules. The runner applies
ordered SQL files once and records each filename and content hash in `game_lb_schema_migrations`; changing
an applied migration is an error. Add a numbered migration for later schema changes and for the game's
reviewed, immutable board definition. Provisioning, process startup and publishing do not run migrations
or seed boards. Apply required additive migrations before saving the checkpoint that first uses them, so
the existing Webdev checkpoint database branch contains the matching schema. Retain existing rows and use
a new board ID when scoring rules change. Do not seed example scores.

In guest mode, server-issued opaque tokens establish identity. Preserve the token locally; losing local storage or
switching device can create a new guest. Cross-device continuity requires account mode with the game's authenticated account
system and a server-side identity adapter; do not present a guest token as cross-device account support.
Nicknames are display text, not identity. Never accept a client-selected player ID or namespace.

Set the client's rules version to the immutable board definition (`rulesVersion` for Three.js, `rules_version` for Godot). Protocol v1 run issuance requires
`protocolVersion:1` and that `rulesVersion`; show 426 `client_upgrade_required` as a refresh/upgrade
state without interrupting local play. The server pins both values in the run.
Request a run when gameplay actually starts; submit that run once after completion. Retries reuse its run
ID and exact payload. Show pending/success/failure from the API response; never invent a global rank from
local scores. The reference bounds scores and durations and serializes best-score updates, but scores are
explicitly client-reported. These are casual rankings, not verified anti-cheat. Competitive/reward-bearing
games require gameplay-specific server validation or verified replay before accepting ranked results.
Keep local play working offline; do not automatically import old local scores into the online board.

On `client_upgrade_required`, retain the guest identity and offline results, show the game's existing
refresh/upgrade message, and stop ranked writes from that loaded client. The reference adapter latches
this state until reloaded. Board reads remain available. Do not silently change the rules version, clear
player data, refresh the page mid-game, or retry by creating a new run. A `run_rules_changed` response
does not authorize resubmitting the old result under new rules.

## Shared publication, rollback and retention

The managed development connection points at the project database. Use it only for the reviewed finite
migration step, never for local leaderboard gameplay tests. Once a checkpoint is saved, the existing
Webdev version flow owns Preview database isolation; publishing that checkpoint selects the live project
database. Both environments keep the application namespace `production` because isolation comes from
the physical database branch, not from a client-selectable namespace. Rules/protocol mismatches remain
errors; do not rewrite old scoring rules to make an old client submit.

Git rollback restores code and assets, not live scores or DB schema. Use additive, backward-compatible
migrations and keep old board rules available for older releases. Retention/backup and guest-expiry policies
are game-owned maintenance tasks; record them before launching a public board.


Candidate frontend upload is not publication success. Use the managed Host's combined frontend/container
result and previous successful pair. Configure `deploy.healthPath` as `/api/health` only after verifying
that the project's actual backend provides this handler: it verifies HTTP startup without acquiring a
database connection or waiting for leaderboard request admission. The current installer/reference
provides it, but existing games are not upgraded automatically. Before changing config for an older
guest/Godot backend, add the lightweight handler; for Godot, also align `server.mjs`'s expected health
path and the project-root backend declaration. Preserve custom backend code; follow the existing-game
update instructions under "Shared database and deployment contract" in `leaderboard-reference/README.md`.
Keep `/api/leaderboards/v1/health` for business readiness; it verifies database identity, migration
columns and declared boards. Verify that endpoint and a ranked run in the selected checkpoint Preview
and published API before claiming the online leaderboard works. A successful startup probe or deployment
does not establish database readiness. Apply additive schema before deploying, retain it after
failures/rollback, and keep rollback targets within
this protocol-compatible window. Detailed SQL, grants and supported client/run behavior belong to the
packaged `leaderboard-reference/README.md`. These checks do not prove actual hosting or SQL isolation;
record manual acceptance before claiming the public online feature is ready.

## Godot

The following integration, Preview and publication steps apply only to Godot.

### Enable and install

Keep the Godot build
`{"command":"true","outputDirectory":"site"}`. Add a deploy declaration pointing at the project's
Dockerfile and health endpoint. Never change applicationKind to web.

The Addon runtime directory from init/attach contains `leaderboard-reference/`. It is an editable
reference, not a provisioned service. Copy its `server/` directory once into the project and its Godot client into the game's scripts;
never overwrite an existing backend. Install that directory's dependencies and commit its lockfile.
Adapt its SQL boards, score limits, duration rules and Godot client to the game. Commit the backend,
Dockerfile, migrations and client together with the game; do not edit installed Addon files. The reference
Dockerfile uses `server/` COPY paths from the project repository root.

A matching deploy domain fragment is:

```json
{"deploy":{"dockerfilePath":"server/Dockerfile","healthPath":"/api/health"}}
```

Use the current config workflow to preserve/merge unrelated routes. Game hybrid requires an `/api/*`
server rule and a final static fallback; server rules stay under `/api`:

```json
{"routes":[{"path":"/api/*","target":"server"},{"path":"/*","target":"static"}]}
```

Do not set `cache` on server rules (the API sends `Cache-Control: no-store`), do not add `deploy.port`,
and do not route WASM/PCK or the platform storage prefix to the API. The backend listens on injected
`PORT`; in Studio, declare the preview port for this Session through webdev.config runtime.port.

`DATABASE_URL` is supplied by managed infrastructure, stays server-only and is never written to
GDScript, a shell command argument, Git or a client build. Do not declare or request another database
URL for Game Preview. The browser client uses same-origin `/api` routes; the backend rejects browser
requests identified as cross-site without depending on a guessed production or Preview hostname.

### Local and checkpoint Preview

The resident local Game Preview validates Godot gameplay and the exported browser bundle. It does not
start or proxy the project backend, and `/api/*` returns `online_preview_requires_checkpoint`. Keep local
play and local scores working, and show the online leaderboard as unavailable there. Do not ask for a
database URL or connect a local preview process to the managed project database to bypass this boundary.

For online leaderboard delivery, finish the backend and client as one coherent version, run the finite
migration command, prepare the Game release, and save/push it through the normal checkpoint workflow.
Hand that saved checkpoint to the user for online acceptance through the existing Webdev Preview.
The platform deploys the checkpoint's
container and static output together, injects the checkpoint database branch as `DATABASE_URL`, and
routes `/api/*` to the container. Preview writes remain in that branch and do not modify the live project
database. Do not replace this with a Game-specific database, URL input card, local supervisor or relay.

The Godot reference client derives an ingress-preserving relative API path from the actual page URL.
Do not replace it with `/api` at the host root on Cloud preview or with an author-machine URL. Native
Godot execution has no managed browser origin. Prioritize deterministic Godot API/client-state tests,
native-renderer screenshots and existing backend/protocol checks; these do not establish that the managed
online adapter works end to end. Do not configure another endpoint or proactively open/drive a browser
to test the leaderboard. The [Game validation policy](game-delivery.md#develop-and-validate) applies to
all Godot game features, including leaderboard UI and API integration.

Deliver promptly after the relevant checks pass. Ask the user to try the saved checkpoint: start and
finish a ranked run, confirm the submission result and board refresh, then reload to check guest identity
and score retention. Offline/API failure should leave local play usable and show an honest online status.
Report this online acceptance as pending until observed; diagnose reported failures from available logs
and affected native/protocol checks without adding a default Agent browser test.

### Publish, history and persistence

When adding an online leaderboard backend, create project-root `game-backend-contract.json` before
its first checkpoint, even if provisioning is blocked, from the packaged
`leaderboard-reference/game-backend-contract.example.json`. Declare the backend's actual Dockerfile/health
paths and required ordered routes, including optional cache or spaFallback values; do not guess or persist
secrets. Read back applied config through the existing config tool and verify it matches before online
deployment. Set the protocol/schema versions and immutable board
IDs/rules versions for this game's backend. The reference runs from the project root and its Dockerfile
copies this declaration; custom backends must implement equivalent readiness checks.

The declaration is a bounded, strictly parsed release input, not a second editable Webdev config owner.
Prepare-release validates and hashes it with the frozen source. Hybrid publication requires its bound
hash and compares the selected checkpoint's deployment requirements with the actual current binding.
A mismatch, static-only publication of a declared backend, or a hybrid release without a declaration is rejected. Restore compatible current
configuration, or prepare and save a new checkpoint; never edit an old checkpoint or bypass by changing
applicationKind. Static Game releases and history reads do not require the declaration.

Leaderboard readiness checks verify actual database identity/schema, required columns and the declared
board rules. The declaration alone does not prove the live database is compatible. Addon does not connect
to the game database during preflight, does not migrate it, and does not change Webdev's deploy/switch
workflow. Existing generated games need an explicit backend update to obtain these checks.

Prepare the game release after all backend/client/source changes, then checkpoint normally. Hybrid Publish
verifies that exact checkpoint's `site/` and manifest before deploying its static bytes and API container.
It runs no Godot build remotely. Confirm the actual deployment result before claiming the online board is
available. Published hosting continues independently of the author's computer and production requests
use the production namespace.
