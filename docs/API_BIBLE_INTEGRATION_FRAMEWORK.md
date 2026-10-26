# API.Bible integration framework — permission-gated planning

Status: **design contract only; no API key, licensed text, server, or APK integration**. This is source-free planning in the public future-phases branch, not authorization to fetch or distribute copyrighted editions.

## Purpose and allowed paths

Flip the Tables must remain useful with **zero API requests** for approved, locally distributable editions (initially the verified WEB corpus, subject to its final provenance/attribution review). Licensed NIV, NLT and other copyrighted editions are **optional online capabilities** until the applicable rights and API plan are confirmed.

Architecture proposal:
```
Android app / WebView
  ├─ Offline edition repository -> only fully redistributable, approved packages
  └─ Licensed online passage reader
        -> optional bounded on-device cache (only where licensed)
        -> first-party backend gateway (key kept server-side)
             -> compliant bounded shared cache (never an unrestricted Bible mirror)
             -> API.Bible on permitted cache misses / refreshes
```

- No copyrighted translation text, publisher-only documents, token, API key, or original private application source in this public repository.
- Cache keys require edition ID, canonical requested passage, source/translation revision, formatting parameters, rights policy and locale where applicable; avoid cross-edition collisions.
- Fetch **only content actually required** for allowed viewing. Fetch a chapter/passage rather than a verse per swipe when it is appropriate and licensed. The passage endpoint currently supports up to **200 verses/request**; do not confuse this with unlimited bulk download rights.
- Never scrape or harvest entire copyrighted translations to create a replacement Bible source. A whole-Bible local installation or permanent multi-user corpus requires separately verified, written distribution/offline rights.
- Prefer on-demand shared caching: thousands of users viewing the **same permitted passage** can reuse a single response; distinct uncached passages and required refreshes still use the upstream quota.
- Do not exceed per-translation/territory/device limits, display/reuse restrictions, or anti-redistribution obligations; involve API.Bible before implementing server-to-client licensed delivery at scale.

## Compliance constraints before integrating

- Check the **current** Terms and Conditions and translation-specific addenda at registration; these can change.
- API.Bible 2026 support documents permit caching but require refreshing cached content at least once per **30 days** and recommend 14 days; use a stricter tested age policy as appropriate. Do not serve content beyond authorized age.
- API.Bible's documentation also says cache fewer than **500 consecutive verses**. Treat it as a constraint pending written clarification of scope/format, not an invitation to cache a complete copyrighted Bible in many fragments.
- Do not permit unrestricted export, redistribution, copying, full Bible download or indefinite offline use of copyrighted material absent separate written permission. Implement rights-revocation and stale-data deletion gates before enabling online licenses.
- API key is **backend-only**, never stored in Android resources, JavaScript, build artifacts, or browser logs.
- API.Bible requires visible copyright/translation attribution, and Starter-plan attribution linking to API.Bible. Preserve text integrity and citations.
- This Android experience uses WebView, so confirm applicability and implement required API.Bible FUMS fair-use reporting for rendered licensed text; re-evaluate the no-data-collection promise and publish accurate disclosures before activation. Fully native mobile exemptions do **not** automatically apply to an embedded web interface.
- No ad revenue, subscriptions, in-app purchases, or upsells under Starter. No creating additional free accounts/projects to pool quotas.
- Confirm user-count, geography, publisher-specific addenda and DRM obligations before selecting or activating versions.

## Configuration without credentials

Define edition capability metadata, not translation text:

```text
editionId, displayName, sourceKind (offline-approved | api-licensed),
rightsStatus (unverified | approved | expired | revoked),
territories, attributionRequired, providerBibleId (optional),
canCache, maxCacheAge, maxContiguousVerses, offlineRedistributionAllowed
```

Integrations stay disabled unless a rights record and approved live configuration exist. Build tests against invented references and placeholder passages (never copyrighted text).

## Failure and privacy acceptance criteria

1. Fully offline: approved WEB reading, Saved Scripture, navigation, artwork and settings work without account/network/API gateway.
2. Unregistered/no-key: API.Bible editions say "Not available yet" without broken loading loops; no unlicensed sample text bundled.
3. Single permitted passage, 1,000 simulated requests: one upstream miss then shared hits while fresh; no user identifiers stored by default. Demonstrate cache scope, access checks and territorial eligibility, not just cache hit rate.
4. Different editions/references never return each other's cached content.
5. Simulate 30-day expiry, revoked license, 72-hour termination deletion and urgent IP-holder removal: disallow stale/unauthorized content and remove it from caches/clients, including offline paths, within the required deadline.
6. Simulate 401/403, 429/quota exceeded and upstream downtime: degrade gracefully to approved offline editions without deceptive verse substitution; clearly label chosen translation.
7. Enforce a configurable shared monthly request budget (Starter: 5,000), alerts at 50/75/90% usage and bounded abuse protection. No billable overage without owner approval.
8. Preserve passage attribution, text fidelity and applicable FUMS delivery/reporting when rendering permitted content, including cache hits where required.
9. Separate Saved Scripture user data from remote translation cache. Cache expiry/revocation must not silently erase Saved verse references or modify native Saved backup. Handle copyright-sensitive Saved verse text separately under the actual license.
10. No stable provider key or publisher text in code, logs, APK, CI artifacts, browser cache beyond authorized scope, or public Git history.

## Questions requiring API.Bible/publisher written confirmation

1. May one first-party gateway serve bounded, cached copyrighted passages to many app installations, and what counts as permitted vs forbidden redistribution?
2. Is app WebView rendering subject to FUMS, and how can the app meet mandatory reporting with minimum device/session data?
3. What are per-edition maximum offline cached verses and permitted on-device retention, simultaneous devices and territories?
4. Are proactive prefetching, chapter caching, and shared server caching permitted for NIV/NLT under Starter and/or Enterprise?
5. Is there a separate grant for locally distributing complete editions and supporting offline reading without provider calls?
6. What special noncommercial/ministry volumes or waivers are possible for 25,000–100,000 monthly users?
7. What notice, copyright, DRM and attribution features are required for each licensed edition?

## Dependencies and responsibility

- **No registration needed to keep designing and testing mocks.** Owner completes account setup, chooses three eligible licenses, and adds secret configuration through a secure deployment procedure later.
- Public Development owns app integration only after approved source migration and license checks; Future Phases owns synthetic interface contracts and non-sensitive planning here. Do not merge, publish, activate network access or trigger private signing automatically.

References checked 2026-10-26:
- https://api.bible/terms-and-conditions
- https://care.api.bible/article/401-caching-content
- https://care.api.bible/article/411-common-integration-patterns
- https://care.api.bible/article/396-licensing-policies-quick-reference
- https://care.api.bible/article/417-understanding-fums
- https://docs.api.bible/common-questions/
