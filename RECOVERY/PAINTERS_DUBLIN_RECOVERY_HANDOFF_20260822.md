# painters-dublin.ie — RECOVERY / RECONSTRUCTION HANDOFF — 2026-08-22

**Status:** DURABLE RECONSTRUCTION HANDOFF / CURRENT EXPORT NOT VERIFIED  
**Deletion consequence:** this file preserves the known project intent and recovery boundary, but does **not** prove that an exact WordPress/Elementor site export has been recovered.

## Known project identity

- Domain/project: `painters-dublin.ie`.
- Purpose: Dublin local painting / decorating / external-insulation service acquisition site.
- Known implementation direction: WordPress + Elementor / Elementor Pro.
- Known commercial/content modules from project planning:
  - service pages;
  - portfolio / completed-work evidence;
  - customer reviews / trust evidence;
  - direct contact / WhatsApp;
  - Google Business Profile integration/direction;
  - payment/deposit capability such as Stripe where commercially appropriate;
  - later expansion from a narrow painting site toward broader service coverage only when evidence supports it.

## Fresh recovery searches performed

Google Drive searches on 2026-08-22:
- `painters-dublin.ie` / `painters dublin`;
- `WordPress`;
- `Elementor`.

File Library searches on 2026-08-22:
- exact domain/name;
- WordPress + Elementor + Dublin painters;
- site backup/export/config terminology.

GitHub search/repository inventory was also checked.

### Result

No authoritative current site export/backup/config artifact was located in accessible GitHub, Google Drive, or File Library evidence during this audit.

A Drive search can surface unrelated business/CV/recovery documents mentioning painting or Dublin; these are **not** a website backup.

## What is NOT durably proven

- current WordPress database/export;
- current Elementor kit/templates/export;
- theme/plugin versions;
- active page inventory and exact current copy;
- menus/header/footer state;
- form configuration;
- SEO plugin state;
- analytics/tag configuration;
- redirects/permalinks;
- media-library completeness;
- hosting/DNS state;
- current GBP/Stripe/WhatsApp technical bindings.

## Security boundary

Never place the following into GitHub recovery files or ordinary Drive handoffs:

- passwords;
- WordPress admin credentials;
- hosting credentials;
- API secret keys;
- Stripe secret keys;
- private cookies/session tokens;
- recovery codes;
- DNS registrar secrets.

Use a password manager / provider-native secret store for secrets. A durable handoff may record only that a credential exists and which service owns it.

## Two legitimate closure paths

### Path A — exact-state recovery

If the site still matters as an existing build, obtain and persist a current non-secret recovery pack:

1. WordPress full export or hosting backup reference;
2. Elementor kit/template export where available;
3. plugin/theme/version inventory;
4. page/URL inventory;
5. media manifest;
6. redirects/permalinks/SEO settings export where available;
7. integrations manifest with secret values removed;
8. stable Drive pointer + readback receipt;
9. GitHub handoff/current pointer to that Drive recovery pack.

Then set:
`PAINTERS_DUBLIN_CURRENT_EXPORT_HANDOFF_VERIFIED = TRUE`.

### Path B — explicit reconstruction authority

If preserving the exact old build is no longer valuable, Founder may explicitly retire it and authorize reconstruction from this handoff + current business evidence. In that case, the old source chat is not treated as authoritative site state and the deletion blocker can close by explicit retirement, not by pretending an export exists.

## Current decision

`PAINTERS_DUBLIN_CURRENT_EXPORT_HANDOFF_VERIFIED = FALSE`

`PAINTERS_DUBLIN_RECONSTRUCTION_HANDOFF_EXISTS = TRUE`

`PAINTERS_DUBLIN_DELETE_GATE = BLOCKED_UNTIL_EXACT_EXPORT_RECOVERED_OR_FOUNDER_EXPLICITLY_RETIRES_OLD_SITE_STATE`

`PAINTERS-DUBLIN-RECOVERY-20260822-NONSECRET-HANDOFF-PERSISTED-EXACT-EXPORT-NOT-FOUND`
