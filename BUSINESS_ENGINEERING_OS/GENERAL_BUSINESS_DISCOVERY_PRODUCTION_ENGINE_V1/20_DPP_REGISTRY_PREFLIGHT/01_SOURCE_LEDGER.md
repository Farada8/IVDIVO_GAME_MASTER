# P-EW04 SOURCE LEDGER — CURRENT FIRST-PARTY BASELINE

**Date checked:** 2026-08-22  
**Evidence class:** first-party European Commission public implementation material.  
**Rule:** these sources support architecture/timing/test design only; they do not prove our customer demand or legal applicability for an arbitrary product.

## S1 — DPP Registry now live
European Commission, 20 July 2026:
https://single-market-economy.ec.europa.eu/news/digital-product-passport-registry-now-live-2026-07-20_en

Supports: Registry + testing environment operational; Registry stores identifiers/registration metadata while detailed DPP data is decentralised; registration available via UI or API; secure proof of registration can be requested; semantic repository/machine-readable models and documented APIs; current testing phase ahead of first battery implementation deadline.

## S2 — DPP Registry architecture
European Commission:
https://single-market-economy.ec.europa.eu/single-market/digital-product-passport/dpp-registry_en

Supports: Registry is an indexing service; stores unique identifiers, registration data and high-level metadata rather than the full detailed payload; economic operator registers in accordance with applicable legislation; product data remains with operator/service provider; testing environment is separate from live processes; customs use includes registered DPP and commodity-code verification.

## S3 — DPP overview / timeline / workflow
European Commission:
https://single-market-economy.ec.europa.eu/single-market/digital-product-passport_en

Supports: product-specific requirements arise through ESPR delegated acts or separate Union legislation; Registry operational 20 July 2026; certain battery DPPs mandatory from 18 February 2027; textile/steel/construction and other groups phase later; operator gathers applicable information, creates/registers DPP, detailed data stays decentralised, a data carrier links product to DPP, and Registry then generates a unique registration identifier.

## S4 — Batteries sector page
European Commission:
https://single-market-economy.ec.europa.eu/single-market/digital-product-passport/batteries_en

Supports: batteries are the first DPP product group; certain battery categories become mandatory 18 February 2027; responsible economic operator is the one placing the finished battery on the market; sector information may include identification, operator, performance/durability, repair/reuse/recycling and sustainability/circularity data.

## Engineering restrictions derived from source quality
- Do not invent a universal mandatory DPP field list.
- Do not label textile/furniture preparation as a current legal obligation solely because they are priority groups.
- Do not model a Registry-generated identifier as an input available before registration.
- Do not equate test-environment preflight with live acceptance.
