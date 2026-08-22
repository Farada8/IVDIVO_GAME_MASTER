from __future__ import annotations

DEFAULT_BENCHMARKS=[
    {"id":"B01_POINT_SEPARATING_NO_GO","domain":"finite_context","expected":"NO_PROMOTION"},
    {"id":"B02_EXACT_LUMPABLE","domain":"markov","expected":"EXACT"},
    {"id":"B03_PERTURBED_LUMPABLE","domain":"markov","expected":"TOLERANCE_TRANSITION"},
    {"id":"B04_NONCONTRACTIVE_SMALL_ERROR","domain":"markov","expected":"LONG_HORIZON_FAIL"},
    {"id":"B05_HISTORY_CMI","domain":"symbolic","expected":"MISSING_HISTORY_DETECTED"},
    {"id":"B06_MICRO_CMI","domain":"symbolic","expected":"MISSING_MICRO_DETECTED"},
    {"id":"B07_NONREGULAR_GROWTH","domain":"language","expected":"NO_FINITE_STATE"},
    {"id":"B08_FLATTENABLE_HIERARCHY","domain":"construction","expected":"REJECT_INTRINSIC_DEPTH"},
]

def registry(): return list(DEFAULT_BENCHMARKS)
