# Saved Scripture recovery — public acceptance contract

**Status:** source-free specification only; no app implementation or APK is included.
**Scope:** public app Saved Scripture, device-local persistence, normal native recovery, and manual `.fttbackup` recovery. This is **not** a Bible-edition import specification.

## Non-negotiable invariants

1. **No silent data loss.** A pending, unreadable, invalid, or unavailable native store must never be overwritten by a default empty web state. Preserve the last verified data and report uncertain durability.
2. **Quiet routine success.** Normal verified native recovery must not show a repeated “Saved Scripture restored” toast, banner, dialog, or notification. The saved items simply appear.
3. **Visible failure.** Corruption, write failure, failed verification, rejected backup, and unresolved conflicts must produce an actionable warning; never claim a successful save or restore in those states.
4. **Explicit manual restore.** Opening a `.fttbackup` file is not consent to replace Saved Scripture. Show a preview of the impact and require an affirmative confirmation before applying changes. Only a completed, verified *user-initiated* restore may show a success message.
5. **Backup is not an edition.** A `.fttbackup` contains Saved Scripture state only. It cannot add or replace a Bible edition, and the public app must not offer user-submitted Bible-edition imports.
6. **Offline and private by default.** Recovery and manual backup processing work without network access, sign-in, telemetry, or uploading saved text. Errors must not leak user content into logs.
7. **Upgrade integrity.** Persistence across APK upgrades must be demonstrated with the **same permanent signer** and increasing Android `versionCode` on a real device. Public debug builds have a different signer and are **not** in-place upgrade-safe.

## State and transition contract

- **Not checked:** native storage availability has not been established. Do not mirror the web's empty state into native storage.
- **Pending:** native read/recovery is in flight or delayed. Display the existing verified Saved view if available; do not treat “no response yet” as “no saved items.”
- **Verified:** native payload passes format/integrity checks and reconciliation completes without dropping entries or metadata. Routine recovery completes silently.
- **Failed:** native read, parse, write, or read-back verification fails. Keep all previously verified items, block destructive writes, and show a warning with a retry path.
- **Manual preview:** a selected `.fttbackup` has passed type, size, schema, and integrity validation. Show additions/replacements and await explicit confirmation.
- **Manual committed:** the confirmed change has been durably written and read back. Only now may the UI show “restore complete.”
- **Rejected:** a malformed, oversized, untrusted, wrong-format, or edition-import file is not applied. Keep Saved unchanged and explain the rejection.

If two stores disagree, never silently prefer an empty, stale, or partially parsed snapshot. Reconciliation must preserve every verified Saved entry and its associated metadata; unresolved collisions block destructive replacement until a safe resolution is implemented.

## Synthetic acceptance scenarios

All identifiers below are invented test tokens, **not** Scripture text, references, personal data, or artwork. Each scenario must later be translated into executable browser/native tests against reviewed public source.

| ID | Given | When | Required outcome |
| --- | --- | --- | --- |
| SR-01 | Native has `synthetic-A`; web initially empty | App launches | `synthetic-A` appears after verification; no success toast; no empty-state native write |
| SR-02 | Native read is delayed; web initially empty | Web initialization finishes first | Native is not cleared; state remains pending until read resolves |
| SR-03 | Verified web has `synthetic-A`; native data is corrupt | Recovery runs | Keep `synthetic-A`; show warning; do not overwrite native with an unverified snapshot |
| SR-04 | Verified Saved has `synthetic-A` | Native write or read-back verification fails for `synthetic-B` | No success claim; retain `synthetic-A`; warn that `synthetic-B` is not confirmed durable |
| SR-05 | Saved has `synthetic-A`; valid `.fttbackup` proposes `synthetic-B` | File selected but not confirmed | Show preview; no Saved changes and no “restored” message |
| SR-06 | Same setup as SR-05 | User explicitly confirms, durable write and read-back pass | Apply the previewed change without silently discarding `synthetic-A`; show one manual-restore success message |
| SR-07 | Saved has `synthetic-A` | Malformed or oversized `.fttbackup` is selected | Reject with warning; preserve `synthetic-A`; no success message |
| SR-08 | Saved has `synthetic-A` | A file purporting to install a Bible edition is selected | Reject as an unsupported edition import; preserve Saved and edition catalog |
| SR-09 | Native and web have differing verified entries | Routine recovery reconciles | No verified entry or metadata is lost; no routine success toast; unresolved conflicts warn instead of destructive replacement |
| SR-10 | Same-signer installed app has `synthetic-A` | Owner installs higher-`versionCode` permanent-signed APK over it | `synthetic-A` survives; verify on Samsung, not by browser simulation alone |
| SR-11 | Installed app is permanently signed | User attempts to install a public debug APK over it | Do **not** recommend the attempt as an upgrade; signer mismatch is a release blocker |
| SR-12 | App data is cleared without a separately retained backup | App reopens | Do not promise automatic recovery of erased local data; explain that only a valid retained manual backup may restore it |

## Acceptance evidence required

- **Automated browser tests:** exercise SR-01–SR-09 with injected delays, corruption, rejected files, failed writes, and read-back checks; record each assertion and its result. A test of a mock alone is not proof of Android behavior.
- **Native Android/Samsung tests:** exercise actual app lifecycle, delayed native bridge initialization, interruption/restart, low-storage write failure where reproducible, SR-10 upgrade, and backup chooser/confirmation. Preserve device test notes without uploading Saved content.
- **Privacy review:** confirm backup/recovery never sends content over the network and that error logging is redacted.
- **Release gate:** fail if a routine restore toast reappears, any verified item disappears, failed persistence is reported as success, or an unconfirmed backup replaces existing Saved data.

## Dependencies and ownership

This contract can be reviewed without private source. Implementation and app-facing tests wait for legally reviewed public Android source and the separate public-development workstream; this branch must not edit that workstream's migration/build files or launch CI. Private permanent signing and device upgrade receipts remain owner-controlled. The public repository is not presently evidence of a buildable or upgrade-safe APK.
