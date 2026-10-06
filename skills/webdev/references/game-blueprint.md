# Game Blueprint

Read for online choices, concepts, reopening, session-owned coverage, planning-unavailable setup or recovery;
[setup](game-setup.md) owns routine refresh/close. Writes use `expectedRevision` from the latest canonical read.
Errors, transport failures and missing state grant no approval.

## Three.js Blueprint

When the saved `gameEngine` is `threejs`, the Blueprint has two pages: summary, game type and
editable gameplay; then optional online features. The 3D model generation preference page is temporarily hidden;
do not recreate it as a chat question. Preserve recorded model choices, narrower restrictions and the same initialized Three.js project and starter.
Only `genre`, `gameplay`, `assetProduction` and `onlineFeatures` are accepted choices. There are no effort, coverage or
Godot concept-review steps. Approval continues directly to implementation; do not submit concepts or refresh coverage.
Saving, cancellation, reopening and history use the existing revision-based lifecycle below. A missing engine
on an older Blueprint means Godot. On a structured planning-unavailable handoff, settle gameplay and online
requirements only. For online features follow the Three.js sections of the selected guides; use the existing
Web build, Preview, checkpoint and deployment flow. Do not run a Godot installer or prepare a Godot release.

The approved `assetProduction` applies to 3D game models only:

- `catalog_procedural` (current default): reuse suitable Manus game assets catalog models as they are, or adapt them to the game. Read the installed catalog Skill before searching. A catalog gap grants no generation permission.
- `hybrid`: combine catalog models with custom-generated models from text using the built-in `generate_3d_model` tool. Do not create concept design references.
- `ai_generated`: write custom descriptions for the game's models and use the built-in `generate_3d_model` tool to generate them from text. Do not create image or concept design references.
- `ai_generated_max`: generate image references first, then use them to guide 3D model generation with the built-in `generate_3d_model` tool. This has the highest fidelity and token usage. These are model-production references, not the Godot three-concept review flow; do not submit them to `game/blueprint/concepts`.

For max, supply the finished reference in `image` and omit `prompt`. Including both edits the reference again, adding image credits and latency; use both only for an intentional edit. Keep generated references in tool-owned outputs or an existing ignored scratch location excluded from the Web build and checkpoint. Commit final models/runtime textures.

Tool names are implementation guidance; do not expose them in the model-choice card or require the user to choose a tool.

Wait for canonical approval before catalog sourcing or generation. Default/countdown and non-interactive confirmation use catalog assets; the default alone is not approval. Preserve supplied-only, no-AI and other narrower restrictions from the complete brief. This choice does not expand audio or other media permissions. Historical approved Blueprints without a saved model choice retain their recorded permissions; do not infer Hybrid consent. Reopening an unanswered historical draft upgrades its model default; save/reopen retains recorded choices.

In Cloud and Local, discover the active `generate_3d_model` schema before generation. If it lacks the selected method, continue gameplay with existing models and report deferred models; do not change provider/method, reinitialize or use paid calls to probe availability.

Follow the starter's Web convention: keep self-contained GLBs in `public/assets/`; preload with `Assets.gltf('assets/model.glb')` before `game.start()` in `main.ts` or its existing equivalent, then include models in the Web checkpoint. Catalog retrieval/adaptation applies; its Godot sync/release commands do not. Asset-library registration separately requires a Three.js-capable runtime.

## Card lifecycle and approvals

The initialized Blueprint owns the editable one-item-per-line plan and unresolved choices; there is no genre picker. For Godot, Development Effort offers Fast prototype and Standard effort (`max_effort`, the default).
Delegation settles only its fields; delegated mockups default to none unless images are authorized. Keep other
unresolved choices on the card, without parallel questions or unsolicited mockups.

The setup countdown accepts untouched defaults after 60 seconds; interaction cancels it, and saving never restarts
it. Concept review has no timer and requires explicit approval (Godot only). Non-interactive sessions preserve supplied
choices and otherwise use recommended gameplay; for Godot, use Hybrid within restrictions and no mockups.
Disclose conflicts with requested mockups; never skip them to bypass approval.

Reuse blueprintId through stages/retries, updating existing cards; never re-prepare/tool-poll. Each new run, including
background continuations, closes older unanswered Blueprints in this session; follow the saved receipt.

## Online features

`choices.onlineFeatures` records Manus login (`manus_oauth`), shared leaderboard (`leaderboard`) and Stripe
payments (`stripe`); no selection adds no online scope. Card edits record requirements, and saved selections override
superseded online requests in the original brief. Game init leaves server and database off even for online requests.
Do not provision while the card is pending, including preselected options. If all options are cleared before first
approval, keep the new project static. After approval, read `webdev.config`, enable missing `server` and `database`
for selected persistent integrations, verify provisioning, and follow the selected [login](game-authentication.md),
[leaderboard](game-leaderboards.md) or [payments](payments.md) guide. Stripe setup is separate. Configure and verify
hybrid deployment/routes before the first checkpoint with these features. Deselection does not disable provisioned
infrastructure; never reinitialize. Fast prototype preserves explicit online requirements. Pending/cancelled choices
grant no approval.

## Blueprint text

Use the stored Blueprint content language and you/your, 你／你的 (or 您／您的), not third-person 用户 or "the user".
Neutral text needs no pronoun; retain quotations and player references. Mention only unresolved questions.
Describe visual roles/content in titles, plans, options and captions; exclude filenames, directories, catalog/template
paths and tool details from that text. Required imagePath or assetRef fields keep exact identities. Quoted titles,
game-content language and the current viewer's UI locale do not rewrite saved Blueprint content. Fixed card UI follows
the current viewer's UI locale.
Chat follow-ups use the main session's own language rules.

## Planning unavailable

Only a structured `game_blueprint_planning` receipt with `planning_unavailable` transfers setup to this agent;
matching brief text, missing cards and transport errors do not. Continue the initialized project with its full brief,
language and known choices. Settle only unresolved choices through native questions, honoring no-questions safe
defaults. For Three.js, settle gameplay and online requirements only; preserve the original asset permissions without a separate model-preference question. For Godot, use the production wording below
and, if concepts were requested without a card, the Godot concept submission below. Settle online choices before enabling services
through config; init left server/database off. Do not reinitialize, poll or retry the planner. Canonical state wins.

## Submit concepts

Godot only; Three.js has no concept stage.

### Concept work by request
Concepts are conditional, not a routine production step. Follow the Blueprint's recorded mockup choice and do not
offer a second concept workflow when the direction is already clear. For an explicit request, produce distinct,
coherent interpretations of the brief and keep the selected identity through revisions. The Game Concept Design flow
needs exactly three separate mockups generated under the recorded image consent, presented through the existing card
and explicitly approved; never label mockups as screenshots. Outside that flow, honor the requested count and
approval method. Mockup consent is not consent for production assets.

For Godot authorized concepts, POST `game/blueprint/concepts` with `{expectedRevision, concepts}`: exactly three distinct entries,
each with id, name, description and exactly one absolute local PNG `imagePath` or saved `assetRef`. The runtime uploads
images. For requested shorter captions, rewrite once and resubmit all three at the same revision with existing images.
Present only through Game Concept Design unless asked for chat copies; wait for explicit approval. On generation
failure, POST `{expectedRevision, error:"generation_failed"}` to the same path. After a lost reply, read canonical state before retrying;
accepted images are not regenerated or reuploaded. Revision consent covers only that revision.

## Session-owned coverage

For Godot only, canonical `author_coverage` with saved `visualCoveragePlanning: "session_owned"` delegates coverage to this agent.
From the full brief and choices, POST `game/blueprint/refresh` at the handoff revision with
`{expectedRevision, question: {question, options:[{id,label,description}], recommendedOptionIds}}`: 1–12 roles,
≤8192 UTF-8 bytes; recommended IDs must come from options. An empty list permits no optional enrichment. No planner
retry, sourcing or implementation until the next action allows it. On stale revision, reassess returned state.

Otherwise the init planner owns visual roles; coverage is agent-only scope with no coverage page/questions.
Preserve explicit empty optional lists, inclusions/exclusions, source permissions and deliberate procedural design,
and check the integrated game against that scope.

## Reopen after cancellation

Closing/cancelling retains decisions without accepting defaults or authorizing implementation, sourcing or generation;
the current message may supply new direction. If another Blueprint helps, POST `game/blueprint/reopen` from the cancelled
receipt with `{blueprintId, expectedRevision, description?, title?, choices?}`: send the full revised brief and only
explicitly changed choices. Omitted choices retain saved decisions; unanswered ones remain unanswered. For genre changes,
include matching gameplay only if known; omitting it returns genre-only setup. Never initialize another project or regenerate the starter.

## Setup recovery

Recover the same project according to the cause: wait for an active operation, fix authorization or repair the
selected engine/toolchain (Godot engine/templates where applicable). Missing host capabilities need host support.
An unknown outcome requires one saved-state read, never automatic replay.
Before recovery that repeats inference/generation, downloads a toolchain, wakes paid compute or rebuilds heavily,
explain the action and possible credit/token cost and obtain explicit approval for that attempt; setup countdowns
and earlier consent do not cover it.

For existing games, failed Blueprint retrieval is non-blocking: log once and continue the same project from the current
request, `recorded_game_scope` and source, preserving known pending/cancelled approvals and source limits.
That failure grants no consent and needs no retries, reinitialization or new setup; for new games,
failed reads do not approve pending setup. Run start selects the current installed runtime for unchanged Addon
launchers; customized commands use returned GAME_RUNTIME. Never replace game files, patch release fingerprints or
invent an upgrade endpoint.

## Legacy setup

Only for supported legacy preparation, follow the live schema/receipt and reuse clientRequestId and arguments on retries.
`visualCoverageMode: "delegate"` delegates authoring; supplied choices.visualCoverage holds
`{roles:[{id,label,description}],customRequest?}`. When the receipt requests session-authored coverage, prepare
`visualCoverageQuestion:{question,options,recommendedOptionIds}` or use advertised submit_visual_coverage with
blueprintId, expectedRevision and question: group relevant roles (usually 4–8, at most 12) under stable lowercase IDs.
Existing pre-init Blueprints initialize with `gameEngine: "godot"` and approved ID/revision; never omit them to bypass pending/cancelled state.
Older init tools retain their supported flow, with non_interactive only where supported and never with mockups:true.
Do not discover retired operations from old messages.

## Production choices for cards and native questions

Godot only; Three.js has no production-choice page.

### Asset-production choice wording
Fast prototype follows its bounded workflow. New managed games call `webdev.init_project` once direction is clear,
with the complete brief; the canonical card settles unresolved choices, not parallel chat questions or a separate
Blueprint. Session-agent catalog search, access, downloads and delegation wait for successful initialization plus a
settled Blueprint, required plan and requested concept approval; in-flight or failed init is not success. Only
initialization's bounded metadata assessment may precede the card, never production downloads, generation or
integration. Standalone search or retrieval needs no project but does not justify speculative new-build sourcing.
Use the conversation language and call the catalog 游戏素材库 in Chinese. Recommend Hybrid mode for 2D, 3D and
unknown games. Card options for 2D/unknown: Manus game assets catalog, Hybrid mode, AI generation; Hybrid means
catalog plus AI art/audio, not scratch visuals. Known 3D: Game asset library and procedural generation, Hybrid mode,
AI generation. Only initialization's evidence-backed insufficient core-visual fit changes the first 3D label to
Procedural generation (Faster, lightweight, minimal token consumption); Unknown/sufficient fit or missing decoration
does not. Preserve historical accepted permissions; never infer them from option names or recommendations.
Only missing card support or a structured `planning_unavailable` receipt moves unresolved setup to one native
single-choice question; canonical state wins. For 2D/unknown: Manus game assets catalog, Hybrid (Recommended), AI
generated. Known 3D: Curated asset catalog and procedural (lowest token cost; catalog first, permitted gaps),
Hybrid (Recommended), AI generated (highest token cost). Keep these labels and this order, and record the answers.
No-questions sessions use
the recommended option within existing permission, which is not new consent. Additions to an existing game ask only
an unresolved production choice; delegation inherits constraints.
Accepted `choices.visualAssetSource: procedural` needs no repeated visual search/gap proof; audio follows its own
source restrictions and optional-production workflow. Catalog and Hybrid sourcing, including required-gap handling,
follows the game-asset-catalog Skill. Procedural permission never implies music composition.
