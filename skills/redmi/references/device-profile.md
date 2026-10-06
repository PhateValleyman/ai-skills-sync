# Device and Termux reference

## Baseline

- Device: Redmi Note 11
- Model: `2201117TG`
- Codename: `spes`
- Architecture: `ARM64 / aarch64`
- Root: Magisk
- Terminal: Termux
- Shell: Bash
- Language preference: Bash, then Go, then Python
- Editor: `nano`

Verify the baseline instead of trusting it when the task may involve another device or a changed ROM.

```bash
# Display the complete Android build fingerprint.
getprop ro.build.fingerprint

# Display the Android product device and hardware name.
printf '%s %s\n' "$(getprop ro.product.device)" "$(getprop ro.product.board)"

# Display the current machine architecture.
uname -m
```

## Termux rules

Termux-specific scripts should use `#!/data/data/com.termux/files/usr/bin/bash`, not `/bin/bash`. Prefer `$HOME` for builds and temporary files; move final artifacts to shared storage only when needed. Run `termux-setup-storage` only when shared-storage access is required.

Use `pkg update`, `pkg upgrade`, and `pkg install PACKAGE`; do not use `apt` assumptions from desktop distributions unless verified in the current Termux installation.

## Android command availability

Check tools before relying on them:

```bash
# Check whether an Android-native command exists.
command -v COMMAND

# Display command-specific help when supported.
COMMAND --help
```

Common Android-native tools are `getprop`, `setprop`, `pm`, `cmd`, `am`, `settings`, `dumpsys`, `logcat`, `toybox`, `svc`, `input`, and `content`. Their options vary by Android version.

## Termux:API

Use Termux:API for battery, Wi-Fi, notifications, infrared, location, sensors, clipboard, media, and volume only after checking that the add-on and command are installed. Example:

```bash
# Check whether the Termux battery API command exists.
command -v termux-battery-status

# Display supported infrared carrier-frequency ranges when available.
termux-infrared-frequencies
```

Do not assume every Android API is available or permitted.
