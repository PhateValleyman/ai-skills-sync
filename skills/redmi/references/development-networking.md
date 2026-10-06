# Development and networking reference

## Network diagnostics

```bash
# Display network interfaces and addresses.
ip addr

# Display the routing table.
ip route

# Display Android DNS-related properties.
getprop | grep -i dns

# Test connectivity to the selected gateway.
ping -c 3 GATEWAY
```

Do not assume a static LAN address. Do not change routing or subnet configuration blindly. Check Tailscale before modifying related networking:

```bash
# Check whether Tailscale is installed.
command -v tailscale

# Display the current Tailscale state when installed.
tailscale status
```

## SSH

Prefer SSH keys over passwords and never expose private keys. The user's configured key is normally `~/.ssh/server`; verify its presence and permissions before use. Known targets include `root@192.168.1.20` and an Nvidia Shield Tablet at `user@192.168.1.12:8022`, but connectivity and identity must be verified before making changes.

```bash
# Connect to the configured server using the SSH key.
ssh -i ~/.ssh/server root@192.168.1.20

# Connect to the Shield Tablet using the configured port and key.
ssh -p 8022 -i ~/.ssh/server user@192.168.1.12
```

## Git workflow

Before modifying a repository inspect status, remotes, recent commits, repository instructions, and relevant source. Modify only required files, format, build/test, inspect the diff, and report the result. Do not reset, clean, rebase, force-push, discard local work, or create commits unless explicitly requested.

```bash
# Display the current repository state.
git status

# Display configured Git remotes.
git remote -v

# Display recent commits.
git log --oneline -10

# Display modified files before committing.
git status --short

# Display unstaged changes.
git diff
```

## Toolchains and resource limits

Use Bash for system automation, Go for standalone performant CLIs, and Python for scripting/data processing. The target is ARM64 Android/Termux. Verify toolchain versions instead of changing them randomly:

```bash
# Display the Java runtime version.
java -version

# Display the Gradle version.
gradle --version

# Display the Go version.
go version

# Display the Rust compiler version.
rustc --version

# Locate Android NDK directories without assuming a fixed path.
find "$HOME" -type d -name 'android-ndk-*' 2>/dev/null
```

The known NDK context is r29, but path and installation must be inspected. The default native target is `aarch64 / arm64-v8a`; verify with `uname -m`. Before resource-heavy builds inspect `nproc`, `free -h`, and `df -h`; avoid blindly using `-j$(nproc)` on a thermally or memory-constrained phone.
