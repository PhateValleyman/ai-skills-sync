# Game asset operations

Read only for deletion, restoration, grouping, animation, models/textures or user-attached asset edits; do not audit unchanged assets.
Catalog sourcing uses the enrolled `game-asset-catalog` Skill from `webdev-mcp`, including
its helpers and recovery. Respect recorded methods and published facts without publisher/licensing re-review. Use
the project's layout and local runtime media that survives grant expiry. The [delivery](game-delivery.md)
save/prepare path reconciles receipts and syncs assets automatically; do not add a separate sync before it.

## Deletion and restoration

For a requested deletion run `node "$GAME_RUNTIME/scripts/delete-asset.mjs" "assets/<exact-media-path>"` from the
project; disk-only deletion is restored by sync, and lock storage facts are never hand-edited. For missing files,
reuse verified copies and restore known managed assets first, then diagnose actual path, import or config errors.
Search only unresolved roles within source permission, and get agreement before changing restrictions; an access
failure is not a catalog gap. Keep originals until replacements work, and verify integration before claiming
recovery.

From the project, `node "$GAME_RUNTIME/scripts/hydrate-assets.mjs"` restores genuinely missing managed assets, and
`node "$GAME_RUNTIME/sync-assets.mjs"` registers a coherent changed batch when early registration is needed. Keep
existing `asset-provenance.json`, supplied license notices, lock entries, groups and sidecars; never fake preloads or
delete dependencies because they are marked `used:false`.

## Groups and animation

Keep group IDs, names, membership and order. New groups serve browsing (characters, UI, audio, fonts), not wrapper
directories; reserved `assets/template` stays template. The Godot Assets tab always displays Animations → Images →
Audio → Others. `groups[groupId].order` only controls group order within a media category; it cannot override this
category priority. Mixed groups are split by media category for display only; preserve their manifest membership.
Animation frames share size/anchor and consecutive names in one
clip directory or prefix. Authored `<prefix>.animation.json` needs `type:"frame-animation"`, `name`, `fps`,
`loop` and project-relative `coverFrame`, without `managed:true`. Mixed-directory clips need descriptors rather
than moves. Sync builds ordered bundles; loose images are not an Animation entry and generated bundles are not
hand-edited.

## Models and textures

Preserve case, relative URIs and GLB/glTF dependencies; move dependencies together and update model URIs, material
bindings and consumers. New layouts use assets/models/<asset>, materials/<material> and textures/<material>, keeping
existing model-relative Textures directories. The lock covers images, audio, video, fonts and GLB/glTF/OBJ/FBX/Blend/
DAE models; loose textures register separately and embedded ones stay in models. Buffers, material resources and
unsupported HDR/EXR/TGA stay versioned source; only GLB/glTF dependencies are automatic. Keep the runtime-managed
.gitignore rules so hydrated media stays out of Git.
`node "$GAME_RUNTIME/check-textures.mjs" --strict` is read-only: a nonzero exit includes oversized *or uninspected*
resources and resizes nothing. It covers GLB/glTF images and identifiable Godot material or scene bindings; other
formats, binary resources and dynamic or default shader textures need explicit inspection, so never claim strict
coverage for them. Optional versioned `game-texture-budgets.json` (excluded from player export) is
`{version:1,textures:{"assets/models/hero.glb":{maxSize:2048,reason:"Closest camera fills face"}}}`, keyed by exact
image, model, material or scene path or `model.glb#image/0`. Allowed sizes are 256/512/1024/2048/4096, and above
1024 needs a concrete reason.

## Apply asset edits without overwriting newer work

Preserve the attachment's baseDigest, resource URI and path; resized thumbnails never establish original hashes, and
missing bases require inspecting the actual targets. Generate candidates under dist/asset-edit-candidates, keeping
originals, and prepare the matching candidate lock with the changed bytes and hash. Batch originals, derivatives and
the lock with `node "$GAME_RUNTIME/asset-edit.mjs" --prepare request.json`, then `--apply ID`:
```json
{"resourceId":"wdp_PROJECT_ID","changes":[{"path":"assets/hero.png","baseDigest":"sha256:ORIGINAL_HASH","candidate":"dist/asset-edit-candidates/hero.png"},{"path":"assets.lock.json","baseDigest":"sha256:LOCK_HASH","candidate":"dist/asset-edit-candidates/assets.lock.json"}]}
```
Derive identity from the attachment URI, current runtime or Local declaration, never a fabricated init marker; attach
on mismatch. Use a null base only for explicitly new targets. Prepare freezes candidates; apply rechecks bases and
backs up originals, and only phase:complete succeeds. A conflict keeps candidates and newer files: report it and ask
which to keep, never silently refresh the base. Interrupted edits use `--recover ID`; remove an exact stale lock only
after confirming its owner PID exited. Bundle frame edits keep timing, groups and annotation coordinates.
Keep `.manus-asset-history/` in source checkpoints and outside the player export. To restore, read its ID.json,
choose before or after, capture the current digest, run `--restore request.json` with
`{resourceId,id,path,side,baseDigest}`, then `--apply` the NEW returned ID; restore related animation sets together.
Before-creation means deletion, not image restoration. Keep the last successful Preview if rebuilding fails.

## Textures, animation and parallax

### 3D texture budgets
Budget the project's stored textures, including bytes embedded in GLB/glTF, not catalog masters or import limits.
Longest edge: 256–512 for small or distant props, 1024 by default, 2048 for close main actors or shared atlases,
4096 only for a justified visible difference. Never upscale, and keep UVs, channel packing and material bindings
intact. Remove replaced embedded bytes, keep ancestry and sync the changed files. If suitable tools are missing,
report it rather than replacing working assets. Claim only measured savings.

### Continuous animation and alignment
Use the approved animation method. AI continuous motion goes from approved static references to a guided
fixed-camera, in-place video to fixed-FPS extracted loops; independent poses need an approved stepped style. Keep a
shared canvas, scale, pivot and contact anchor across states and facings instead of per-state placement patches, and
keep raw masters outside the game. Check representative movement, reversal and ground contact with the native
renderer.

### Seamless parallax backgrounds
Repeating layers must tile left and right without mirroring; check the joins between adjacent copies at the intended
scale after any crop, import or scale change. Side-scrollers keep a low scenic foreground above world actors and
below the HUD without hiding combat.
