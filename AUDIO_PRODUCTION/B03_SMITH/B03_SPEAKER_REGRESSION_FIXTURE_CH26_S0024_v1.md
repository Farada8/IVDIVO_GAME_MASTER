# B03 speaker regression — CH26 S0024

Expected acoustic speaker: `NETWORK_TECHNICIAN_CH26`.

Failure pattern: pronoun coreference chose the nearest named male (`Smith`) even though the local grammatical/action subject is the technician.

Immutable local anchor: the technician connects his maintenance terminal, waits for the local controller to answer, then the quote is followed by `he said`.

Mandatory regression: a resolver must not promote `SMITH` for `B03_CH26_S0024`.
