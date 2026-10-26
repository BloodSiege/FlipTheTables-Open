# Phase 0 — public-source and asset clearance acceptance

**Status:** source-free review contract only. No reviewed Android source, licensed Scripture corpus, build, or publication is authorized by this document.

This acceptance gate supplements the public future-phase framework and the separate migration workstream's *technical* file/checksum gate. A checksum proves integrity of reviewed bytes, **not** originality, copyright ownership, or permission to distribute. No third-party APK material, private code, artwork, credentials, correspondence, private Git history, or personal Saved content belongs in this planning branch.

## Decision states and stop rule

For each criterion record **PASS**, **BLOCKED**, or **UNKNOWN**, plus reviewer, date, scope/version, evidence reference, and any remaining limitation. An undocumented claim is **UNKNOWN**. Any BLOCKED or UNKNOWN criterion prevents an **approved-for-public-export** decision; passing a different criterion never overrides it. Retain sensitive evidence only in owner-controlled private records. Public evidence uses synthetic identifiers, path categories, rights-status summaries, and non-sensitive digests when appropriate.

## Required acceptance criteria

| ID | Gate | Evidence required for PASS |
| --- | --- | --- |
| PC-01 | Independent application implementation | Review the actual planned export's Android and web implementation against available third-party baselines for copied or translated proprietary code, distinctive algorithms, identifiers, resources and generated code. Document scope and limitations; zero literal-name or byte-hash matches alone is **not** clearance. |
| PC-02 | Complete source inventory | A deterministic, path-by-path export manifest records every intended source and generated file; no unpublished code or unreviewed path is silently included. Each nontrivial file has a known origin and redistribution basis. |
| PC-03 | Dependencies and notices | Inventory runtime/build dependencies, font licenses, notice files, embedded SDKs and required attribution; verify the **specific versions** permit the contemplated redistribution. |
| PC-04 | Image and audio provenance | Review every bundled illustration, icon, photo, font, audio file and derivative: original/authorized source, generator or artist record, transformation, required credits, and any embedded third-party elements. Similarity searches support—but cannot substitute for—rights review. |
| PC-05 | Exact Bible edition rights | For **each** included edition, record original source, exact revision, territory, offline/distribution permission, attribution/trademark requirements, coverage and corpus-integrity result. An acknowledgment, API key, free access, or ownership of a personal copy is **not** permission. |
| PC-06 | Content and import boundary | Public distribution contains only approved licensed/public-domain editions. No user-submitted Bible-edition imports. Manual user-confirmed `.fttbackup` Saved recovery stays distinct from edition installation. |
| PC-07 | No private material or history | The public export starts with fresh history and contains no private Git commits, personal screenshots, owner identifiers, correspondence, signing material, secret values, or private Bible documents. Review bytes, metadata and repository history, not only filenames. |
| PC-08 | Local privacy and Saved safety | Document device-local Saved behavior, quiet routine native recovery, warnings on uncertain durability, explicit confirmation before manual backup restore, offline behavior and no unconsented transmission of user content. |
| PC-09 | Debug-only build separation | Public source and GitHub workflows include no private signer or owner-only flavor. Public CI artifacts, once possible, are clearly **debug-only and NOT upgrade-safe**. Same-signer permanent upgrades belong to the separate private release process. |
| PC-10 | Executed technical source gate | Against the **actual approved export**, run the public allowlist, checksum, path/symlink, secret, edition and packaging checks. Record exact source revision, command, outputs, checksums and failures. A synthetic fixture pass alone does not satisfy this gate. |
| PC-11 | Executed app acceptance | Only after lawful Android source is present, record actual browser/offline and Android debug packaging tests, followed by device checks. Clearly distinguish simulated results, compiled APK verification and physical handset results. |
| PC-12 | Final human approval | A named authorized reviewer signs off on the *exact export manifest and rights matrix* before migration/publishing. Changes to code, media, Scripture revisions or dependencies invalidate the affected approvals and require re-review. |

## Evidence receipt (template; synthetic values only)

- **Candidate source revision:** `synthetic-source-001`
- **Export manifest digest:** `synthetic-digest-not-a-real-hash`
- **Code review:** `UNKNOWN` — scope, comparison method and exclusions
- **Assets and fonts:** `UNKNOWN` — itemized provenance and any outstanding rights
- **Bible editions:** `UNKNOWN` — edition-specific permissions, territory and integrity
- **Privacy/Saved:** `UNKNOWN` — privacy, backup and recovery regression evidence
- **Technical source gate:** `NOT RUN` — actual export required
- **Android/browser/device tests:** `NOT RUN` — app implementation required
- **Authorized reviewer/date:** `NOT APPROVED`
- **Decision:** `BLOCKED` until all criteria pass

## Handoff boundary

The separate public migration/build workstream owns the source exporter, checksum gate, GitHub Actions debug APK workflow and eventual reviewed-source integration. This planning branch defines review criteria **only**; it must never copy private implementation, modify the migration/build files, automatically merge, dispatch private Actions, or publish artifacts. Do not claim a public APK can build until reviewed Android source actually exists and passes CI. Publication or permanent signing requires separate explicit owner approval.
