# CYCLE 4 — ENGINEERING SPEC
## Design / Public Art / Hospitality Business Engine

## 1. Runtime object model

### DesignProjectObject v1
Required fields:
- `project_id`
- `project_type`: mural | sculpture | monument | installation | small_architecture | hospitality_interior | office | visitor_centre | route | mixed
- `country`, `county`, `place`, `site_id`
- `site_evidence[]`: photos, dimensions, maps, drawings, owner/public context
- `site_constraints[]`
- `heritage_state`
- `stakeholders[]`
- `buyer_class_candidates[]`
- `programme[]`
- `user_groups[]`
- `user_journeys[]`
- `story_or_interpretive_thesis`
- `design_intent`
- `composition_or_spatial_system`
- `style_genome`
- `art_components[]`
- `material_system[]`
- `lighting_system`
- `acoustic_system`
- `accessibility_state`
- `safety_state`
- `maintenance_model`
- `technical_unknowns[]`
- `cost_band`
- `commission_routes[]`
- `K_grade`, `D_grade`, `T_grade`, `E_grade`
- `red_team_findings[]`
- `next_decisive_action`

Missing factual fields remain null/TBD. The engine must not synthesize site dimensions, permissions, structural capacities, fire strategy, accessibility compliance or buyer commitments.

## 2. Modules B81–B112

### B81 — DesignSourceRegistryAdapter
Maps the existing Business Source Registry and the new Design Raw Inbox into a single canonical work graph without mixing evidence weights.

### B82 — DesignBookJurisdictionRouter
Routes each design source to stages it can legitimately inform: composition, figure, perspective, hospitality planning, lighting, acoustics, materials, public art, conservation, etc.

### B83 — StyleMechanismExtractor
Converts style references into mechanisms rather than adjectives. Example dimensions: spatial depth, edge logic, figure grouping, chromatic structure, light model, drapery rhythm, architecture/figure relationship, symbolic density.

### B84 — SpatialReferencePassportCompiler
Creates reference passports for built projects and precedents: what worked, under which constraints, at what scale, for which user journey, and what must not be copied blindly.

### B85 — SiteContextObjectCompiler
Compiles physical, cultural, visual, climatic, access, circulation, heritage and stakeholder context into a typed site object.

### B86 — HeritageSensitivityGate
Separates documented history from invention, flags contested narratives, protected fabric, sacred context, archaeological risk and community-sensitive interpretation.

### B87 — ProgrammeAndUserJourneyCompiler
Transforms a vague request into functions, capacities, adjacencies, user groups, arrival/departure, dwell points, service routes and peak-load scenarios.

### B88 — DesignBriefContractCompiler
Produces the authoritative brief with goals, non-goals, constraints, success criteria, evidence state and unresolved decisions.

### B89 — CompositionHierarchyEngine
For 2D/3D/spatial work, compiles primary/secondary/tertiary hierarchy, masses, axes, focal sequence, figure groups, negative space and light hierarchy before detail.

### B90 — DistanceReadabilityGate
Requires explicit viewing distances and evaluates silhouette, dominant mass, narrative legibility, text/graphic scale and close-detail discovery.

### B91 — StyleGenomeCompiler
Represents style as a vector of compositional/spatial/material mechanisms, not artist-name imitation. Can combine historical mechanisms into an original project language.

### B92 — GenerativePromptCompiler
Compiles prompts from the structured brief. Prompt layers are emitted separately: geometry/composition, figures, materials, light, atmosphere, exclusions, continuity and camera/viewpoint.

### B93 — PromptImageDiagnosisLoop
Classifies generation failure: composition, anatomy, perspective, style drift, architectural logic, object identity, continuity, material error, lighting conflict or over-detail. Repair targets the cause rather than requesting random regeneration.

### B94 — MuralSurfaceEngineeringGate
Tracks substrate, moisture, cracks, preparation, paint/mineral system, UV exposure, drainage, access equipment, edge conditions and maintenance/repaint strategy.

### B95 — SculptureObjectEngineeringGate
Tracks scale, centre of gravity assumptions, anchoring dependency, climbability, sharp edges, drainage, corrosion, fabrication path, lifting/installation and inspection requirements. Structural calculations remain professional-TBD unless provided.

### B96 — SmallArchitectureSystemEngine
Handles pavilion, shelter, lookout, seating, gate, pergola, kiosk, marker, street-furniture and route-element systems as repeatable kits of parts.

### B97 — HospitalityFlowEngine
Models guest, staff, food, beverage, waste, housekeeping, delivery and emergency/service paths separately. Optimizes service and guest experience without collapsing them into one circulation diagram.

### B98 — FOHBOHConflictRouter
Detects front-of-house/back-of-house conflicts: cross-traffic, bottlenecks, dirty/clean conflicts, long service paths, delivery conflicts and visible back-of-house exposure.

### B99 — InteriorArtIntegrationEngine
Determines whether mural, mosaic, stained glass, sculpture, ceiling, floor, joinery or lighting is structural to the experience or merely applied decoration; integrates art at the brief/space stage.

### B100 — LightingAcousticExperienceEngine
Compiles day/night layers, task/accent/ambient light, face/food/art lighting, glare risk, acoustic zones, reverberation risk, privacy and soundscape intent.

### B101 — MaterialDurabilityLifecycleEngine
Routes material by interior/exterior, coastal exposure, moisture, UV, impact, cleaning, repairability, patina, replacement cycle and embodied/lifecycle considerations.

### B102 — BuildabilityAndMaintenanceGate
Requires fabrication route, access, sequencing, tolerances, cleaning, replacement, inspection and maintenance ownership before project is called commission-ready.

### B103 — CostBandEstimator
Outputs assumption-banded cost classes rather than fake precision. Unknown quantities and specialist scopes remain explicit. Cost estimate maturity is tied to design maturity.

### B104 — CommissionRouteCompiler
Maps project to likely commissioning route classes: council/public art, developer, hotel/restaurant operator, tourism/visitor attraction, private owner, grant-supported culture, competition, partnership or self-funded prototype. No live buyer claim without E-proof.

### B105 — StakeholderAndConsentMap
Maps owner, operator, public authority, heritage stakeholders, neighbours/community, fabricator, design team, maintenance owner and end users. Records disagreement rather than smoothing it away.

### B106 — TourismExperienceValueEngine
Compiles visit trigger, arrival, orientation, story discovery, interaction, dwell, photo moment, night mode, accessibility, repeatability and local-business spillover hypotheses.

### B107 — OfferPackagingEngine
Packages the same creative capability into scoped commercial offers: concept-only, mural package, public-art feasibility, hospitality art integration, visitor-route concept, full concept+visualization, or design/fabrication coordination.

### B108 — ProposalProofPackCompiler
Builds a proposal pack with site evidence, concept, design rationale, before/after, programme, visitor journey, materials, preliminary technical risks, cost band assumptions, maintenance, project stages and proof grades.

### B109 — NoOutreachMarketEvidenceBridge
Uses public signals, procurement notices, strategies, capital plans, tourism/heritage programmes and comparable commissions only to E2/E2+ ceilings. It cannot create buyer intent.

### B110 — DesignRedTeam
Runs independent fatal/major/minor review across story, site, composition, operations, technical, maintenance, accessibility, safety, heritage, budget and commissioning route.

### B111 — CrossAIReviewAdapter
Allows Claude/Grok/other AI or parallel ChatGPT dialogues to contribute findings with source/provenance and authority labels. Unpersisted neighbouring-chat memory is DISCOVERY_ONLY.

### B112 — DesignSelfImprovementBridge
Logs failure taxonomy, repaired rule, affected module, regression fixture and pilot outcome. Candidate improvements do not become authority until they demonstrate gain on a real project without cross-domain regression.

## 3. Engineering contracts C97–C128
C97 `RAW_COPYRIGHTED_DESIGN_SOURCES_PRIVATE_DRIVE_ONLY`  
C98 `DESIGN_SOURCE_REQUIRES_JURISDICTION`  
C99 `STYLE_NAME_NEQ_STYLE_MECHANISM`  
C100 `SITE_BEFORE_STYLE`  
C101 `PROGRAMME_BEFORE_DECORATION`  
C102 `USER_JOURNEY_BEFORE_HERO_RENDER`  
C103 `COMPOSITION_BEFORE_DETAIL`  
C104 `VIEW_DISTANCE_REQUIRED`  
C105 `RENDER_NEQ_DESIGN_PROOF`  
C106 `DESIGN_PROOF_NEQ_TECHNICAL_PROOF`  
C107 `TECHNICAL_PROOF_NEQ_MARKET_PROOF`  
C108 `K_NEQ_D_NEQ_T_NEQ_E`  
C109 `UNKNOWN_DIMENSIONS_NULL`  
C110 `UNKNOWN_STRUCTURE_NULL`  
C111 `UNKNOWN_CODE_COMPLIANCE_NULL`  
C112 `HISTORICAL_CLAIM_REQUIRES_SOURCE`  
C113 `CONTESTED_HERITAGE_PRESERVE_DISSENT`  
C114 `FOH_NEQ_BOH_FLOW`  
C115 `ACCESSIBILITY_IS_GATE`  
C116 `PUBLIC_SAFETY_IS_GATE`  
C117 `MATERIAL_REQUIRES_EXPOSURE_CONTEXT`  
C118 `OUTDOOR_IRELAND_REQUIRES_WEATHER_MAINTENANCE_CHECK`  
C119 `ART_INTEGRATION_DECLARED_ARCHITECTURAL_OR_DECORATIVE`  
C120 `COST_ESTIMATE_MATCHES_DESIGN_MATURITY`  
C121 `COST_UNKNOWN_NEQ_ZERO`  
C122 `COMMISSION_ROUTE_NEQ_BUYER_COMMITMENT`  
C123 `ONE_MAGIC_PROJECT_SCORE_FORBIDDEN`  
C124 `PROMPT_IS_COMPILED_ARTIFACT_NOT_AUTHORITY`  
C125 `REPEATED_GENERATION_FAILURE_TRIGGERS_DECOMPOSITION`  
C126 `RED_TEAM_FATAL_BLOCKS_COMMISSION_READY`  
C127 `CROSS_AI_FINDING_REQUIRES_PROVENANCE_AND_AUTHORITY_LABEL`  
C128 `SELF_IMPROVEMENT_PROMOTION_REQUIRES_REAL_PILOT_GAIN`

## 4. Proof planes

### Knowledge proof K0–K5 — inherited
K0 present -> K1 integrity -> K2 canonical identity -> K3 mechanism+provenance -> K4 cross-source/conflict -> K5 executable fixture/regression.

### Design proof D0–D6
- **D0 Hypothesis:** idea only.
- **D1 Briefed:** explicit site/project goal and constraints exist.
- **D2 Coherent:** programme/user journey/composition or spatial system is internally coherent.
- **D3 Site-fit:** design is tested against actual site evidence and viewing/use conditions.
- **D4 Cross-discipline reviewed:** red-team review covers art, operations, heritage/accessibility and major technical interfaces.
- **D5 Prototype evidence:** scaled mock-up, test panel, spatial prototype, verified render set or equivalent evidence demonstrates key design behaviours.
- **D6 Built/post-use evidence:** as-built or real installation plus observed use/maintenance learning.

### Technical proof T0–T6
- **T0 Unknown:** technical feasibility not assessed.
- **T1 Constraint inventory:** substrate/structure/services/climate/access risks listed.
- **T2 Preliminary feasibility:** dimensions/material/fabrication route checked at concept level.
- **T3 Specialist interfaces defined:** structural, fire, accessibility, MEP, conservation or other required professional dependencies explicitly assigned.
- **T4 Coordinated design:** major interfaces resolved in drawings/specs or verified specialist inputs.
- **T5 Fabrication/installation ready:** fabrication package, sequencing, access and maintenance requirements defined.
- **T6 As-built verified:** installed condition and critical performance evidence recorded.

### Market proof E0–E7 — inherited
No Cycle4 design artifact may upgrade E-grade without the required external buyer/commitment evidence.

## 5. Proof objects
### DesignProof
`project_id, site_evidence_ids[], brief_version, user_journey_fixture, composition_fixture, distance_readability_fixture, heritage_review, accessibility_review, red_team_state, prototype_artifacts[], D_grade`.

### TechnicalProof
`project_id, dimension_source, substrate_or_structure_state, material_exposure_match, services_dependencies[], specialist_dependencies[], fabrication_route, installation_route, maintenance_owner, unresolved_risks[], T_grade`.

### CommercialDesignProof
`project_id, offer_id, commission_route_class, public_signal_ids[], comparable_commissions[], buyer_evidence_artifact, cost_band_assumptions, E_grade`.

Missing proof fields are never synthesized.

## 6. Protocols
P-DES-01 **Library Ingest:** raw -> integrity -> canonical identity -> passport -> mechanism -> limit -> fixture -> K-grade -> readback.  
P-DES-02 **Site Intake:** location -> ownership/context -> photos/dimensions -> movement/views -> weather -> heritage -> constraints -> unknown ledger.  
P-DES-03 **Brief Compile:** objectives -> users -> programme -> narrative -> non-goals -> success criteria -> constraints -> evidence state -> lock.  
P-DES-04 **Concept Divergence:** generate at least three materially different mechanisms, not three cosmetic variants -> compare by brief fit -> preserve dissent -> select or hybridize.  
P-DES-05 **Composition/Spatial Compile:** hierarchy -> masses/zones -> axes -> journey -> viewpoints -> light -> detail budget -> distance checks.  
P-DES-06 **Prompt Compile:** brief fields -> composition geometry -> subject -> style mechanisms -> materials -> lighting -> exclusions -> camera -> continuity -> generation.  
P-DES-07 **Image Diagnosis:** inspect output -> classify failure -> determine root layer -> repair smallest upstream object -> regenerate -> compare.  
P-DES-08 **Technical Gate:** dimensions -> substrate/structure -> services -> materials -> climate -> accessibility -> safety -> fabrication -> installation -> maintenance -> T-grade.  
P-DES-09 **Hospitality Flow:** guest/staff/product/waste/delivery/housekeeping flows -> conflict map -> adjacency repair -> capacity assumptions -> experience layer.  
P-DES-10 **Commercial Package:** project type -> commission route -> offer scope -> deliverables -> exclusions -> cost band -> schedule assumptions -> proof pack -> E ceiling.  
P-DES-11 **Red Team:** fatal -> major -> minor -> fix -> regression fixture -> re-run affected gates.  
P-DES-12 **Self-Improvement:** failure -> causal hypothesis -> rule/module mutation -> bounded pilot -> before/after metrics -> regression -> promote/hold/rollback.

## 7. Acceptance gates
A project may be labelled **CONCEPT READY** only if D2+ and site unknowns are explicit.  
A project may be labelled **SITE PROPOSAL READY** only if D3+ and T1+ with real site evidence.  
A project may be labelled **COMMISSION PROPOSAL READY** only if D4+ and T2+, cost assumptions and maintenance are visible, and all FATAL red-team findings are closed.  
A project may be labelled **FABRICATION READY** only after T5 with required professional approvals/evidence supplied by the appropriate parties.  
No label upgrades E-grade automatically.

## 8. Self-improvement instrumentation
For every pilot record:
- time to authoritative brief;
- number of unresolved site unknowns;
- number of image-generation retries by failure class;
- red-team FATAL/MAJOR count before and after repair;
- number of design decisions with source/mechanism provenance;
- number of technical claims left correctly null rather than guessed;
- cost-band assumption count and sensitivity;
- commissioning evidence grade;
- change requests after stakeholder review;
- post-installation failures/maintenance issues when available.

The engine optimizes decision quality and rework reduction, not prompt volume or image count.

## 9. Current real gate after Cycle4
`INGEST FIRST DESIGN SOURCES -> SELECT ONE REAL IRISH SITE -> BUILD DesignProjectObject -> D/T RED TEAM -> PROTOTYPE/RENDER FIXTURES -> COMMISSION PROOF PACK`.

Do not create another abstract top-level engine until at least one real design pilot exercises B81–B112 end to end.