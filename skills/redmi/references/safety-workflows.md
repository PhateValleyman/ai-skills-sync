# Safety and troubleshooting reference

## Backup and destructive operations

Before root changes or application-data modifications, create a timestamped backup when practical.

```bash
# Create a compressed backup of the selected directory.
tar -czf "backup-$(date +%Y%m%d-%H%M%S).tar.gz" DIRECTORY
```

For destructive deletion, print and validate the target first:

```bash
# Display the target before deleting anything.
printf 'Target: %s\n' "$TARGET"

# Abort if the target variable is empty.
[ -n "$TARGET" ] || exit 1
```

Explicitly confirm high-impact operations: partition or filesystem destruction, `/data` or `/data/adb` deletion, boot-image flashing, partition-table changes, SELinux disabling, mass package removal, recursive changes on critical paths, broad `rm -rf`, destructive Git history operations, and release-key replacement. Never generate a replacement Android release key without authorization; losing the existing key can prevent application updates.

## Diagnostic layers

For a non-trivial issue follow:

`REPRODUCE → CAPTURE ERROR → INSPECT ENVIRONMENT → IDENTIFY FAILURE LAYER → MAKE SMALLEST CHANGE → TEST → VERIFY → DOCUMENT`

Use the lowest layer that explains the failure. Typical layers are Android framework, Magisk/root, Termux, shell, toolchain, application, and project. Do not solve a higher-level issue by unnecessarily changing a lower-level component.

Useful diagnostics:

```bash
# Display running processes.
ps -A

# Display Android logs.
logcat

# Filter logs for an application or keyword.
logcat | grep -i PACKAGE

# Display kernel messages when the production kernel permits access.
su -p -s bash -c 'dmesg'
```

Prefer `am force-stop PACKAGE` for Android applications over killing arbitrary PIDs. Never kill system processes blindly.

## Verification and reporting

For each significant change report: observed before-state, exact modification, verification output or result, persistence level, reboot requirements, rollback path, and any assumptions that remain unverified. A suggested command is not an executed command.

For repository work use: inspect status and instructions → inspect relevant source → targeted edit → format → build/test → inspect diff → report. Keep commits focused and descriptive, but do not commit automatically unless requested.
