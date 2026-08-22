# B03 speaker regression — CH27 S0136

Expected acoustic speaker: `SMITH`.
Source author: `TAREN_SOR`.
Delivery mode: `READ_ALOUD`.

Failure pattern: message/source authorship was treated as acoustic speaker identity.

Immutable narrative anchor establishes that Smith reads Taren's reply aloud. A later `Taren’s message continued` describes the message content/source; it does not establish a live Taren audio channel.

Mandatory regression: when narration establishes that character A reads character B's message aloud, TTS/acoustic speaker is A unless the text separately establishes playback or a live channel from B.
