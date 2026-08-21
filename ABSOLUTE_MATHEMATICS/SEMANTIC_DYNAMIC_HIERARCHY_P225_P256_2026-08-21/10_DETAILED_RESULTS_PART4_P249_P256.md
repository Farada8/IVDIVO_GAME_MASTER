# DETAILED RESULTS P249–P256

## P249 — LOCALITY DEPTH ON GRAPHS

**STATUS:** DERIVED

### Strongest supported claim
Locality yields graph-dependent lower bounds on construction depth proportional to graph distance/communication radius.

### Evidence
Fresh graph diameters/local lower bounds: {'path32': {'diameter': 31, 'local_r1_lower_bound': 31, 'local_r2_lower_bound': 16, 'unrestricted': 1}, 'grid6x6': {'diameter': 10, 'local_r1_lower_bound': 10, 'local_r2_lower_bound': 5, 'unrestricted': 1}, 'binary_tree_depth4': {'diameter': 8, 'local_r1_lower_bound': 8, 'local_r2_lower_bound': 4, 'unrestricted': 1}, 'complete32': {'diameter': 1, 'local_r1_lower_bound': 1, 'local_r2_lower_bound': 1, 'unrestricted': 1}}.

### Limitations / Red Team
These are signal-propagation lower bounds for the declared local model, not universal upper-order counts.

### Decision
Add graph metric and radius to locality-admissibility metadata.

### Formal anchor
`depth >= ceil(distance/r)`

## P250 — ARITY-LOCALITY COMBINED DEPTH

**STATUS:** DERIVED

### Strongest supported claim
When bounded arity and locality both apply, construction depth is at least the maximum of the separate arity and locality lower bounds.

### Evidence
Fresh combined controls record max(ceil(log_b N), distance/r): examples [{'N': 16, 'arity': 2, 'distance': 8, 'arity_lb': 4, 'locality_r1_lb': 8, 'combined_lb_max': 8}, {'N': 16, 'arity': 2, 'distance': 32, 'arity_lb': 4, 'locality_r1_lb': 32, 'combined_lb_max': 32}, {'N': 16, 'arity': 4, 'distance': 8, 'arity_lb': 2, 'locality_r1_lb': 8, 'combined_lb_max': 8}, {'N': 16, 'arity': 4, 'distance': 32, 'arity_lb': 2, 'locality_r1_lb': 32, 'combined_lb_max': 32}].

### Limitations / Red Team
Achievability of the maximum is architecture-dependent; it is only a lower bound in general.

### Decision
Use combined admissibility bounds, not additive heuristics unless proved.

## P251 — COMMUNICATION-COMPLEXITY ORDER

**STATUS:** KNOWN

### Strongest supported claim
Communication complexity supplies an established resource axis showing that a tiny final macro output can require large distributed information exchange.

### Evidence
For deterministic Equality, the standard lower bound is n communicated bits although the answer is one bit; the benchmark registry records n=8…128: [{'n': 8, 'macro_output_bits': 1, 'deterministic_comm_lower_bound_bits': 8, 'ratio': 8}, {'n': 16, 'macro_output_bits': 1, 'deterministic_comm_lower_bound_bits': 16, 'ratio': 16}, {'n': 32, 'macro_output_bits': 1, 'deterministic_comm_lower_bound_bits': 32, 'ratio': 32}, {'n': 64, 'macro_output_bits': 1, 'deterministic_comm_lower_bound_bits': 64, 'ratio': 64}, {'n': 128, 'macro_output_bits': 1, 'deterministic_comm_lower_bound_bits': 128, 'ratio': 128}].

### Limitations / Red Team
Randomized communication can be much cheaper for Equality with error, so the communication model must be declared.

### Decision
Add deterministic/randomized communication budget as an admissibility coordinate.

## P252 — MEMORY-BUDGET ORDER

**STATUS:** DERIVED

### Strongest supported claim
Working-memory constraints can create a separate resource hierarchy even when the final output is tiny.

### Evidence
Benchmark examples record parity with 1-bit streaming state versus exact fixed-length palindrome requiring distinction among 2^(n/2) first-half prefixes, i.e. at least n/2 bits: [{'n': 8, 'parity_memory_bits': 1, 'palindrome_exact_lower_bound_bits': 4}, {'n': 16, 'parity_memory_bits': 1, 'palindrome_exact_lower_bound_bits': 8}, {'n': 32, 'parity_memory_bits': 1, 'palindrome_exact_lower_bound_bits': 16}, {'n': 64, 'parity_memory_bits': 1, 'palindrome_exact_lower_bound_bits': 32}].

### Limitations / Red Team
The exact bound depends on streaming model, input length assumptions and error allowance.

### Decision
Add memory budget to Order Spectrum only with a declared computational model.

## P253 — TYPE-SAFE NONFLATTENABILITY

**STATUS:** DERIVED

### Strongest supported claim
Typed staged depth can be nontrivial when admissibility counts primitive typed transformations rather than their composites.

### Evidence
Fresh toy: {'types': ['A', 'B', 'C'], 'primitive_maps': ['f:A→B', 'g:B→C'], 'composite_function_exists': 'g∘f:A→C', 'primitive_A_to_C_allowed': False, 'relative_depth': 2, 'red_team': 'Depth exists only because admissibility counts primitive maps and is not composition-closed.'}.

### Limitations / Red Team
This is easy to manufacture artificially; if the admissibility class is closed under well-typed composition, the direct composite exists and flattening returns.

### Decision
Typing-based depth is valid only when type constraints are externally grounded and composition closure is explicitly restricted.

## P254 — ADMISSIBILITY NATURALNESS SCORE

**STATUS:** NOVELTY_UNVERIFIED

### Strongest supported claim
A useful admissibility-naturalness audit can combine external grounding, invariance, resource interpretation and non-ad-hocness, but a scalar 'naturalness score' is heuristic rather than mathematics.

### Evidence
Fresh rubric sharply separates locality/bounded arity from contrived 'forbid only the direct target map': {'locality': {'external_grounding': 1, 'symmetry_invariance': 1, 'resource_interpretation': 1, 'non_ad_hoc': 1, 'score': 1.0}, 'bounded_arity': {'external_grounding': 1, 'symmetry_invariance': 1, 'resource_interpretation': 1, 'non_ad_hoc': 1, 'score': 1.0}, 'forbid_only_direct_target_map': {'external_grounding': 0, 'symmetry_invariance': 0, 'resource_interpretation': 0, 'non_ad_hoc': 0, 'score': 0.0}, 'chosen_coordinate_threshold': {'external_grounding': 0, 'symmetry_invariance': 0, 'resource_interpretation': 1, 'non_ad_hoc': 0, 'score': 0.25}}.

### Limitations / Red Team
Weights and criteria are normative; no theorem makes this score canonical.

### Decision
Keep the rubric as Red-Team metadata, not as an order invariant.

## P255 — ORDER SPECTRUM PARETO DOMINANCE

**STATUS:** DERIVED

### Strongest supported claim
Order spectra are generally partially ordered: different tasks/hierarchies can trade locality, arity and communication costs so neither dominates.

### Evidence
Fresh example: {'tasks': {'TaskA': {'unrestricted': 1, 'arity2': 6, 'locality': 10, 'communication': 32}, 'TaskB': {'unrestricted': 1, 'arity2': 4, 'locality': 20, 'communication': 16}}, 'pareto': {'A_dominates_B': False, 'B_dominates_A': False}}.

### Limitations / Red Team
The spectrum depends on the chosen admissibility coordinates.

### Decision
Use Pareto dominance/incomparability rather than forcing a total scalar ranking.

## P256 — HIERARCHY GRAND RED TEAM

**STATUS:** DERIVED

### Strongest supported claim
The Hierarchy module survives Red Team only as an application-relative resource/construction object; no evidence supports a context-free intrinsic scalar order.

### Evidence
P249–P255 show graph-locality, arity, communication, memory and typing produce legitimate but model-relative depths, while naturalness and flattening audits prevent ad-hoc hierarchy rescue.

### Limitations / Red Team
The choice of admissibility axes remains partly application/normative.

### Decision
Formal Core v5 should explicitly call this Construction Complexity Spectrum rather than universal Order where possible.
