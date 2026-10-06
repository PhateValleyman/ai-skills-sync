---
name: zyxel
description: Safely operate, maintain, debug, build software for, and modify a ZyXEL NSA320 NAS running Fonz Fun Plug (FFP) — legacy ARMv5/uClibc production infrastructure at root@192.168.1.20. Use this skill whenever the user mentions the NSA320, "Server" (hostname SERVER), FFP, /ffp, ffp packages, or asks to SSH into, configure, build for, debug, or administer that specific NAS device, even if they only say "the server" or "my NAS" in context that matches. Always consult this skill before running any command against that host — it defines the legacy ARMv5/soft-float/uClibc constraints, backup-before-change workflow, and safety rules required to avoid breaking the device.
---

# ZyXEL NSA320 / FFP Administration

## 1. Purpose

This skill defines how to safely operate, maintain, debug, build software for, and modify the ZyXEL NSA320 running Fonz Fun Plug (FFP).

The NSA320 must be treated as **legacy ARM/uClibc production infrastructure**, not as a modern Linux workstation.

---

## 2. Server Profile

| Property | Value |
|---|---|
| Hostname | `SERVER` |
| IP | `192.168.1.20` |
| Architecture | ARMv5 / Feroceon |
| ABI | soft-float |
| OS environment | Fonz Fun Plug 0.7.0 |
| Kernel | `2.6.31.8` |
| libc | `uClibc 0.9.33.3` |
| FFP root | `/ffp` |
| FFP Bash | `/ffp/bin/bash` |
| FFP home | `/ffp/home/root` |
| Toolchain | `arm-ffp-linux-uclibcgnueabi` |
| Native compiler target | `-march=armv5te -mfloat-abi=soft` |
| Go target | `GOARM=5` |

Assume limited CPU, RAM, storage I/O, and old kernel/userspace behavior.

---

## 3. Operating Principles

Default workflow:

```
OBSERVE → UNDERSTAND → BACKUP → CHANGE → VALIDATE → TEST → VERIFY → DOCUMENT
```

Never:

```
GUESS → MODIFY → HOPE
```

Rules:

- Inspect the actual system before making assumptions.
- Prefer the smallest possible change.
- Preserve compatibility with ARMv5, soft-float, uClibc, and the old kernel.
- Prefer reversible changes.
- Do not replace working system components unnecessarily.
- Never discard existing local work without explicit authorization.
- Treat storage, boot, firmware, and system-library changes as high risk.

---

## 4. Shell and Command Conventions

Generated shell commands must have an English comment immediately above each command.

Example:

```bash
# Check the running kernel version.
uname -a
```

Use:

- `/ffp/bin/bash` for FFP scripts.
- `#!/ffp/bin/bash` as the FFP Bash shebang.
- Absolute paths in scripts where practical.
- POSIX-compatible shell syntax unless Bash features are required.
- Traditional utilities when they are the available compatible option.

Do not assume the presence of:

- systemd
- journalctl
- modern GNU utilities
- modern iproute2
- modern Bash
- glibc
- modern OpenSSL
- modern kernel APIs

Check availability first.

---

## 5. Environment Discovery

Before any non-trivial operation, inspect the relevant environment.

Typical checks:

```bash
# Identify the running kernel and architecture.
uname -a

# Identify the current shell and executable location.
echo "$SHELL"
command -v bash

# Inspect available memory and storage.
free
df -h
```

For software operations also inspect:

```bash
# Check whether the required program exists.
command -v PROGRAM

# Check the installed program version when supported.
PROGRAM --version
```

Never guess:

- device names
- mountpoints
- filesystem types
- RAID layout
- service paths
- configuration locations
- installed packages
- library versions

---

## 6. SSH

Preferred authentication is SSH public-key authentication.

Typical connection:

```bash
# Connect to the NSA320 using the dedicated SSH key.
ssh -i ~/.ssh/server root@192.168.1.20
```

Verify before depending on SSH:

- host/IP
- username
- key
- port
- network reachability

Do not weaken SSH security merely to make a connection work.

---

## 7. FFP Environment and Packages

FFP software normally lives below `/ffp`.

Inspect package tooling before using it:

```bash
# Check which FFP package managers are installed.
command -v slacker
command -v funpkg
```

Do not assume modern package-management behavior.

When changing packages:

1. Identify the currently installed version.
2. Check dependencies.
3. Preserve configuration.
4. Avoid replacing core libraries without understanding the impact.
5. Verify the resulting binaries and services.

---

## 8. Legacy Compatibility and Native Builds

Native binaries must match the NSA320 ABI and runtime.

Expected native target:

- ARMv5
- soft-float
- uClibc

Toolchain:

```
arm-ffp-linux-uclibcgnueabi
```

Typical compiler flags:

```
-march=armv5te -mfloat-abi=soft
```

Inspect binaries before deployment:

```bash
# Identify the binary architecture and ABI.
file ./program

# Inspect ELF architecture information.
readelf -h ./program

# Inspect runtime library dependencies when ldd is available.
ldd ./program
```

Common causes of failure:

- wrong architecture
- ARM hard-float vs soft-float mismatch
- glibc vs uClibc mismatch
- missing shared libraries
- incompatible dynamic linker
- unsupported newer kernel features
- compiler-generated instructions unavailable on ARMv5

---

## 9. Go Builds

Prefer static Go binaries for deployment where practical.

Typical target:

```bash
# Build a statically linked Linux ARMv5 binary.
CGO_ENABLED=0 GOOS=linux GOARCH=arm GOARM=5 go build
```

Verify the result:

```bash
# Verify the resulting executable architecture and linkage.
file ./program
```

Avoid CGO unless there is a specific requirement and the target toolchain/runtime is known to be compatible.

---

## 10. Storage and Filesystems

Storage operations are high risk.

Inspect before changing anything:

```bash
# Inspect mounted filesystems.
mount

# Inspect filesystem capacity.
df -h

# Inspect kernel-visible block devices.
cat /proc/partitions
```

Never assume:

- `/dev/sda`
- partition numbering
- RAID devices
- mountpoints
- filesystem type
- disk ownership

Explicit authorization is required before destructive operations such as:

- `mkfs`
- `fsck -y`
- `fdisk`
- `parted`
- `dd`
- partition changes
- RAID changes

---

## 11. File Deletion and Cleanup

Verify the exact target before destructive deletion.

Never blindly execute:

```
rm -rf /
rm -rf /ffp
rm -rf /etc
rm -rf /var
rm -rf /mnt
rm -rf /storage
```

Large files are not automatically unnecessary.

For cleanup:

1. Identify the exact path.
2. Determine ownership and purpose.
3. Check whether a service depends on it.
4. Back up important data.
5. Delete only the confirmed target.
6. Verify the resulting state.

---

## 12. Backup and Recovery

Back up important configuration before modification.

Important locations may include:

```
/ffp/etc
/ffp/start
/ffp/stop
/ffp/etc/init.d
/etc
service/application configuration
scripts
databases
```

Example:

```bash
# Create a timestamped backup of an important configuration directory.
cp -a /ffp/etc /ffp/etc.backup.$(date +%Y%m%d-%H%M%S)
```

Backups must be usable, not merely created.

---

## 13. Startup and Services

FFP startup is normally handled through:

```
/ffp/start
/ffp/stop
/ffp/etc/init.d
```

Do not assume systemd.

For service changes identify:

1. executable
2. configuration
3. startup mechanism
4. running process
5. logs
6. dependencies
7. listening ports
8. required mounts

After modification, verify both startup configuration and runtime state.

---

## 14. Networking

Primary server address: `192.168.1.20`

Legacy systems may provide:

```bash
# Inspect network interfaces when ifconfig is available.
ifconfig

# Inspect the routing table when route is available.
route -n

# Test basic network reachability.
ping HOST
```

Use `ip` only when it is actually installed and functional.

---

## 15. Network Services and Ports

For network services determine:

- process
- listening address
- listening port
- protocol
- configuration
- startup mechanism
- required firewall/network access

When available:

```bash
# Inspect listening TCP and UDP sockets.
netstat -lntup
```

Prefer LAN-only exposure when public access is unnecessary.

---

## 16. Logs and Diagnostics

Expect traditional logging.

Common locations: `/var/log`

Useful tools:

```bash
# Search logs recursively for a relevant term.
grep -Ri "TERM" /var/log

# Inspect recent kernel messages.
dmesg
```

Do not assume `journalctl` exists.

---

## 17. Kernel and System Resources

Check resource state before expensive operations:

```bash
# Inspect available memory.
free

# Inspect filesystem capacity.
df -h

# Inspect system load and uptime.
uptime
```

Avoid:

- aggressive parallel builds
- memory-heavy operations
- unbounded loops
- unnecessary background processes

Do not blindly use `-j$(nproc)`.

---

## 18. OpenSSL and Shared Libraries

Inspect the installed OpenSSL version before making TLS-related changes:

```bash
# Display the installed OpenSSL version.
openssl version
```

Never replace system libraries blindly.

When diagnosing a binary, inspect:

- architecture
- ABI
- dynamic linker
- shared libraries
- library versions

A library upgrade can break unrelated legacy software.

---

## 19. Scheduled Tasks and Locks

Inspect cron before adding scheduled jobs:

```bash
# Check whether the cron daemon is running.
ps | grep crond

# Display the current root user's cron jobs.
crontab -l
```

Scheduled scripts should:

- use absolute paths
- be idempotent
- log failures
- avoid overlapping executions
- fail safely

Use an appropriate locking mechanism such as:

- PID file
- lock file
- `flock`, if available
- atomic `mkdir`, when appropriate

---

## 20. MeshFS / SSHFS

The NSA320 participates in the MeshFS environment.

Before changing mounts inspect:

```bash
# Inspect current filesystem mounts.
mount

# Check whether sshfs is installed.
command -v sshfs
```

Verify:

1. SSH connectivity
2. target availability
3. mountpoint existence
4. existing mounts
5. duplicate mounts
6. `allow_other` requirements
7. boot behavior
8. failure/retry behavior

Do not create infinite boot-blocking retry loops.

---

## 21. Git and Repository Changes

Before modifying a repository:

```bash
# Inspect the current Git working tree.
git status

# Inspect configured remotes.
git remote -v

# Inspect recent commits.
git log --oneline -10
```

Never discard local work without authorization.

Do not use:

- `git reset --hard`
- `git clean`
- destructive rebases
- force-pushes

unless explicitly authorized.

---

## 22. Configuration Changes

Use this workflow:

```
LOCATE ACTIVE CONFIG → BACKUP → MINIMAL CHANGE → VALIDATE → TEST SERVICE → VERIFY RUNTIME
```

Do not edit an apparently relevant configuration file until you know that the running service actually uses it.

---

## 23. Verification

Every meaningful change must have an observable verification step.

Examples:

```bash
# Verify that the expected executable is available.
command -v PROGRAM

# Verify the installed program version.
PROGRAM --version

# Verify that the expected process is running.
ps | grep SERVICE

# Verify that the expected mount exists.
mount | grep MOUNTPOINT

# Verify that the expected configuration value is present.
grep -n EXPECTED_VALUE CONFIG

# Verify that the expected file exists.
ls -la FILE
```

Prefer verifying the actual runtime result over verifying only that a command completed successfully.

---

## 24. SSH / Service / Reboot Safety

Before restarting or rebooting:

1. Save configuration changes.
2. Verify syntax.
3. Verify required mounts.
4. Check running services.
5. Check active transfers/jobs.
6. Ensure SSH should return after reboot.
7. Confirm the change is recoverable.

After reboot verify remotely:

```bash
# Verify the server identity and running kernel after reboot.
hostname
uname -a

# Verify required mounts after reboot.
mount
```

---

## 25. Firmware Protection

Do not modify:

- bootloader
- kernel
- firmware partitions
- unknown flash/system partitions

unless the task explicitly requires it and the exact recovery procedure is understood.

Prefer making changes under `/ffp`.

---

## 26. Security

Default security posture:

- SSH keys instead of passwords
- encrypted protocols
- least privilege
- minimal exposed ports
- LAN-only services where possible
- no credentials in Git
- never copy private SSH keys unnecessarily
- avoid `chmod 777`
- avoid unnecessary root services

---

## 27. PC Independence

Routine administration should work from:

- Android/Termux
- SSH
- server-side scripts
- Git
- FFP tools

A PC should not be required unless a task genuinely depends on hardware/software unavailable through the existing environment.

---

## 28. Completion Standard

For software:

```
EDIT → SYNTAX CHECK → BUILD → TEST → INSPECT → DEPLOY → VERIFY
```

For configuration:

```
BACKUP → EDIT → VALIDATE → RESTART/RELOAD → TEST → VERIFY
```

A task is not complete merely because a command returned exit code `0`. The actual resulting state must be checked.

---

## 29. Compact Decision Tree

Use this before acting:

```
START
 │
 ├─ What kind of change?
 │   │
 │   ├─ Read-only / diagnostic
 │   │    └─ Inspect → diagnose → report
 │   │
 │   ├─ Software / binary
 │   │    └─ Identify arch/ABI/libs
 │   │         ├─ compatible → build/test → deploy → verify
 │   │         └─ incompatible → fix target/toolchain first
 │   │
 │   ├─ Configuration / service
 │   │    └─ Locate active config → backup → minimal edit
 │   │         → validate → reload/restart → runtime verify
 │   │
 │   ├─ Storage / filesystem
 │   │    └─ Inspect devices/mounts/FS
 │   │         ├─ read-only → proceed cautiously
 │   │         └─ destructive → explicit authorization required
 │   │
 │   ├─ Network / SSH / mount
 │   │    └─ Check connectivity → config → process → port/mount
 │   │         → test failure/recovery path
 │   │
 │   └─ Reboot / firmware / system-level
 │        └─ Backup → dependency/recovery check
 │             → explicit authorization → change → remote verify
 │
 └─ Any uncertainty?
      └─ STOP → inspect more → do not guess
```

---

## 30. Quick Reference

| Item | Value |
|---|---|
| Host | SERVER / `192.168.1.20` |
| FFP root | `/ffp` |
| FFP Bash | `/ffp/bin/bash` |
| Architecture | ARMv5 |
| ABI | soft-float |
| libc | uClibc 0.9.33.3 |
| Kernel | 2.6.31.8 |
| Toolchain | arm-ffp-linux-uclibcgnueabi |
| Go | `GOOS=linux GOARCH=arm GOARM=5` |
| SSH key | `~/.ssh/server` |

---

## 31. Final Rule

Treat the NSA320 as legacy production infrastructure: inspect first, preserve compatibility, make the smallest reversible change, and verify the actual result.
