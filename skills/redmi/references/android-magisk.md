# Android, root, and Magisk reference

## Privilege model

Start from the Termux user. Use root only for `/data`, Magisk, privileged Android inspection, application-private data, or privileged networking.

```bash
# Start a root Bash shell only when the operation requires it.
su -p -s bash

# Check the effective identity without opening an interactive shell.
su -p -s bash -c 'id'
```

Prefer Magisk modules, overlays, property overrides, `/data/adb/service.d`, and `/data/adb/post-fs-data.d` over direct modification of Android partitions. Before a critical modification: inspect current state, determine persistence, assess bootloop risk, back up when practical, and implement the smallest change.

## Properties and SELinux

Before changing a property, determine whether it is read-only, whether Magisk can override it, whether it survives reboot, and what security services or applications depend on it.

```bash
# Display the current Android properties.
getprop

# Display the current SELinux enforcement mode.
getenforce

# Display the security context of a file.
ls -Z FILE
```

Do not disable SELinux as the first troubleshooting step. Prefer correcting ownership, permissions, contexts, Magisk policy, or application configuration.

## Application data

For application changes use this sequence: identify package and UID, stop application, back up data, modify only the required file, restore ownership/permissions/context if needed, start application, inspect logs, and verify behavior.

```bash
# Display installed packages and their UIDs.
pm list packages -U

# Display detailed package information.
dumpsys package PACKAGE

# Force-stop the selected application before touching its data.
am force-stop PACKAGE

# Verify that the package is installed.
pm path PACKAGE
```

Never blindly apply recursive world-writable permissions or root ownership. Preserve UID, GID, permissions, and SELinux context.

## Boot scripts and services

Use the earliest Magisk boot phase that is actually necessary. Never block boot-critical processes with long-running scripts. For Termux services account for Android process killing, wake locks, boot integration, noninteractive execution, persistent logs, and clean start/stop operations. Do not assume a Termux background process survives indefinitely.

Every change must state its persistence level and whether reboot is required.
