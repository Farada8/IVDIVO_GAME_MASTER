# IVDIVO HUMAN MICROTEXTURE + SPATIAL SOUND LIBRARY v1.0

**Status:** CANON / UNIVERSAL REFERENCE LIBRARY  
**Purpose:** reusable vocabulary and planning rules for believable body, food/drink, clothing, object, intimacy, ambience and spatial sound.

## 1. Naturalism profiles

`MINIMAL` — only story-critical physical sounds.  
`NATURAL` — selected ordinary body/object texture.  
`CINEMATIC` — stronger contrast and foregrounding, still believable.  
`INTIMATE` — closer breath/clothing/touch/proximity, carefully dosed.  
`COMEDIC` — timing may foreground selected object/body events.  
`DOCUMENTARY` — physically plausible, minimally stylized.  
`ASMR` — only when explicitly authorized; never default.

Microtexture intensity: `0 NONE / 1 TRACE / 2 AUDIBLE / 3 FOREGROUND`.

## 2. Mouth / speech-adjacent texture

Possible low-level events:
- lips parting before first word;
- small lip closure after phrase;
- saliva click;
- tongue reposition;
- dry-mouth swallow;
- throat clear;
- suppressed cough;
- nasal inhale;
- breath through nose;
- mouth breath after exertion;
- jaw movement before difficult speech.

Default: intensity 0–1. Repetition is a defect unless character/condition requires it.

## 3. Food textures

### Hard/crisp
apple, toast, crisp/chip, cracker, raw vegetable, crust.
Possible: initial bite transient, fracture/crunch, restrained chew, swallow.

### Soft/moist
cake, bread, pasta, rice, soft fruit.
Possible: soft bite, low chew texture, utensil movement, swallow.

### Hot food
steam/container movement, cautious breath, delayed sip/bite, mouth cooling reaction only when story-earned.

### Messy/sticky
sauce, jam, melting food. Avoid exaggerated wet mouth sounds unless plot/comedy/ASMR explicitly needs them.

### Eating behavior as character
- rushed bite = impatience/pressure;
- tiny controlled bite = restraint/status;
- eating while talking = casual intimacy or bad manners;
- stopping mid-bite = shock/attention shift;
- chewing to avoid answering = avoidance;
- plate/cutlery in silence = social discomfort.

## 4. Drink textures

Possible chain:
`container pickup → liquid movement → sip → swallow → breath → container return`.

Assets:
- cup ceramic contact;
- glass resonance;
- bottle cap;
- can open;
- pour;
- ice movement;
- straw;
- small sip;
- gulp;
- throat swallow;
- carbonation response;
- coffee/tea cooling breath.

Do not make every sip a loud gulp.

## 5. Body Foley

- weight shift;
- sit/stand effort;
- knee/foot reposition;
- chair cushion compression;
- mattress/sofa compression;
- leaning on table/wall;
- hand rub;
- finger tap;
- hand over face;
- palm on chest/neck only if action exists;
- stretch;
- physical exertion breath;
- fatigue posture movement.

## 6. Clothing / skin / hair

- sleeve brush;
- coat movement;
- leather jacket creak;
- shirt/blouse fabric;
- denim;
- silk/satin trace;
- wool coat;
- zipper;
- button;
- belt;
- pocket;
- handbag/backpack;
- scarf/hood;
- hair against collar;
- wet clothing cling/release;
- fabric during embrace or near-touch.

Never imply undressing or sexual action unless source supports it.

## 7. Touch and intimacy textures

Preferred order:
`approach → near-contact → hesitation → contact → reaction → continuation/withdrawal`.

Possible sounds:
- step stops close;
- clothing proximity;
- hand brushing sleeve;
- fingers on fabric;
- chair/bed shift;
- hand on table near another hand;
- subtle body turn;
- breath-distance change.

Avoid generic kissing sound libraries. If a kiss is story-authorized, prioritize breath, fabric, movement and aftermath over exaggerated lip sounds.

## 8. Footsteps and locomotion

Track:
`character / footwear / surface / pace / weight / direction / distance / room response`.

Surfaces: carpet, wood, stone, tile, gravel, wet pavement, metal stairs, grass, snow, sand.

Footsteps are character/action information, not constant metronome.

## 9. Object texture families

### Paper
page turn, envelope, folded letter, receipt, newspaper, cardboard.

### Metal
key ring, latch, cutlery, railing, tool, switch, coin.

### Glass/ceramic
cup, wine glass, bottle, plate, window touch.

### Wood
door, drawer, table, chair, old floorboard.

### Plastic/composite
phone case, packaging, appliance controls.

### Electronics
button, vibration, charger, laptop hinge, keyboard, old recorder, radio, intercom.

Each recurring story object should receive a stable `OBJECT_AUDIO_ID`.

## 10. Emotional physicality examples

Emotion is inferred from physical behavior, not labelled SFX.

### Anxiety
smaller breath, repeated object handling, aborted movement, faster reply latency or delayed answer depending character.

### Attraction
reduced distance, quieter voice, less Foley density, audible but restrained breath, delayed reply, fabric movement, no need for music.

### Shame
head turn/off-axis voice, smaller volume, object avoidance, delayed answer.

### Anger
harder consonants/shorter latency/controlled object handling or abrupt movement depending character; do not automatically slam doors.

### Grief
instability in breath/voice, effort to continue action, long aftermath; avoid canned sobs.

### Shock
sound subtraction, held breath, stopped object action, delayed response.

### Relief
released breath, body settling, room returning, optional restrained music after change.

## 11. Ambience palette

### Interior domestic
HVAC/fridge, distant traffic, plumbing, neighbors, floor/building movement, clock only if physically present.

### Restaurant/cafe
room murmur, cutlery, cup/plate, espresso machine, door, distant kitchen; keep dialogue clear.

### Car
engine/road bed, tire texture, indicators, rain, ventilation, door/window perspective, seat/seatbelt.

### Hotel
HVAC/radiator, corridor air, distant lift, doors, lobby activity, rain/wind leakage, service sounds.

### Hospital
ventilation, distant trolley, soft monitor only where plausible, doors, fabric/bed movement, footsteps.

### Street
traffic bed, footsteps, wind, crossings, distant voices, bicycles/vehicles according to place.

Ambience must be geographically and temporally plausible for the specific scene.

## 12. Spatial vocabulary

`EAR_BIAS`: CENTER / LEFT_15 / LEFT_30 / LEFT_60 / RIGHT_15 / RIGHT_30 / RIGHT_60 / EXTREME_LEFT / EXTREME_RIGHT.  
`DEPTH`: VERY_CLOSE / CLOSE / CONVERSATIONAL / ROOM / FAR / DISTANT.  
`ORIENTATION`: ON_AXIS / OFF_AXIS / TURNING / FACING_AWAY.  
`OCCLUSION`: NONE / PARTIAL / DOOR / WALL / VEHICLE / OBJECT.

Ear-biased speech is not simple pan: combine position with direct/reverb ratio, HF detail, head orientation and room response.

## 13. Binaural examples

### Intimate two-person scene
A close but not extreme left bias for one speaker, right bias for the other, with common room coherence. Use only if POV and blocking justify it.

### Whisper near one ear
Very close, low room contribution, breath/detail increased, high mono-risk. Keep words duplicated enough in fold-down to remain intelligible.

### Person walking behind listener
Use movement path + changing direct/reverb ratio + spectral cues. Do not rely on pan-only motion.

### Crowded scene
Keep principals spatially stable; move background around them. Listener must always know who matters.

## 14. Negative rules

Reject:
- random mouth smacks;
- constant loud breathing;
- every chew rendered;
- generic heartbeat for every anxiety beat;
- whoosh/boom for every reveal;
- sexy whispering where relationship has not earned it;
- wet body sounds without source justification;
- hard-panned essential dialogue;
- room tone that changes identity every cut;
- decorative off-screen footsteps/knocks that sound like clues;
- continuous music that flattens scene dynamics.

## 15. SFX prompt template

`[physical source] + [material] + [action] + [distance] + [space] + [duration] + [foreground/background] + [realism profile] + [must be distinct from] + [negative implications]`.

Example:
`One restrained ceramic coffee cup set onto a small wooden cafe table at close conversational distance, natural room perspective, short one-shot, no exaggerated clink, no dramatic sting, no glass resonance.`

## 16. Human microtexture decision test

Before adding any human texture ask:
1. Did the action happen?
2. Would it naturally produce an audible sound at this distance?
3. Does hearing it improve embodiment, character, intimacy, comedy, discomfort or causality?
4. Will it distract from the line/clue?
5. Could it imply an unsupported action?

If 1–3 are not clearly yes, omit it.