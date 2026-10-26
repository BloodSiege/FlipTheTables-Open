# Public future-phase framework

Status: planning and source-free groundwork only. This branch contains no exported private app code and is **not** an Android build.

## Separate workstreams

- **Hourly public migration/build workstream:** owns reviewed source export, public Actions debug pipeline, import/privacy verification and APK artifact publishing. Do not edit its files or trigger private CI from this branch.
- **Future-phase framework workstream:** owns this planning branch and new source-free test contracts, fixtures, design notes and safe infrastructure. Reconcile with private ROADMAP before changing implementations. Never merge to main automatically.

## Phase 0 — security and test readiness (first)

- Prepare public-only test contracts and synthetic fixtures that contain no copyrighted Scripture or private information.
- Check that source, artwork, repository history and Bible editions are approved before any public export.
- Keep the public app flavor, debug signing and public GitHub-hosted CI separate from private signing and Justin Only releases.
- Define deterministic test pass/fail output and a low-storage policy for generated artifacts.
- **Done when:** a public CI run executes meaningful checks against reviewed public source, proves APK package/assets/signature are debug-only, and retains artifacts briefly. A hygiene-only success does not count as an app build.

## Phase 1 — foundational user experience

- Define interfaces for Scripture cards and For You feed queue: swipe, previous/next navigation, local preferences, chapter-aware diversity, loading/error/empty states.
- Plan reading modes, font/spacing controls, brightness, background rotation, and Settings-based edition selection.
- Provide deterministic, **synthetic** fixtures for navigation/persistence regression tests.
- **Done when:** relevant UI behaviors pass actual browser tests and are confirmed on device before release; source-only assertions are separately labeled.

## Phase 2 — Saved Scripture resilience

- Test silent, verified normal native recovery; retain explicit success messaging only for user-initiated Saved backup restore.
- Protect Saved verses during delayed native recovery, write failures, oversized backups, interruptions, and Clear Data. Fail closed on uncertain durability.
- Keep Saved `.fttbackup` separate from forbidden user-supplied Bible-edition imports.
- **Done when:** simulated browser/native tests pass and owner Samsung testing confirms data retained across same-signer, increasing-versionCode APK upgrades.

## Phase 3 — future content modules

- Specify a user-controlled media queue for official, approved videos and audio, including inaccessible embed behavior, external-link safety, and an opt-in experience.
- Plan Scripture-first mixed-media feed without weakening existing Scripture navigation or silently launching network media.
- Document privacy-first, device-local community/discussion concepts until moderation, safety and data handling are designed.
- **Done when:** implementation and third-party rights are reviewed, real browser/player checks pass, and phone acceptance is recorded.

## Phase 4 — access and broader reach

- Track rights-holder-approved Bible versions and public-domain editions separately, with provenance, attribution, jurisdiction and verse-integrity checks.
- Scope localization, RTL handling, accessibility, dynamic font scaling, screen readers, offline behavior and low-data mode.
- Never equate an acknowledgment, API access, free-to-read or personal ownership with redistribution permission.
- **Done when:** each edition passes a documented rights check and content integrity review before inclusion.

## Phase 5 — release readiness

- Keep permanent signing exclusively in the private owner-controlled workflow; no key material or stable signatures on public CI.
- Produce a clear private release receipt identifying source commit, package ID, versionCode, signer fingerprint, APK checksum and Samsung checklist.
- Never recommend a public debug APK for an in-place upgrade.
- **Done when:** all necessary gates pass and the owner authorizes a real signed release; device-specific outcomes are reported separately.

## Working agreement for scheduled framework changes

1. Start each run by checking the owner's latest instructions and any pause; inspect the public planning branch, public main and the relevant private roadmap before selecting a task.
2. Work only on independently useful source-free framework or tests, on `planning/public-future-phases`. Do not alter the main public migration branch, GitHub settings, secrets or private repository.
3. Prefer one small reviewable change per run. Include a runnable test when implementing code; distinguish executed tests from source inspection.
4. Re-check compliance: no private data, publisher correspondence, credentials, copyrighted translations, private artwork or source copied without review.
5. Do not merge automatically, launch paid/private Actions, authorize permissions, or create an upgrade-safe APK.
6. Report verified commit SHA/URL, checks actually executed, dependency on approved source, and blockers. Avoid duplicate commits and repeated status messages when nothing changed.
