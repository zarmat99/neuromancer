# Prompt visivi bloccati - pilota capitolo 1 — v0.2

Questi prompt vanno usati insieme alle reference approvate. Ogni generazione
successiva deve ripetere gli invarianti di identità e outfit.

## Stile comune

```text
Use case: illustration-story
Asset type: Italian graphic-novel production art
Style/medium: original retro-future industrial cyberpunk noir; precise expressive
ink linework; deep blacks; restrained painterly color; tactile worn plastics,
wet pavement and analog technology; mature editorial graphic novel, not anime,
not photorealistic
Lighting/mood: oppressive night, practical neon and fluorescent sources
Constraints: adult characters; anatomically coherent hands; no text, letters,
captions, logos or watermark; no redesign of referenced characters; no elements
from later chapters
```

## Reference `CHAR_CASE_V1`

```text
Primary request: definitive model sheet for Case, the same adult male character
shown full-body front, full-body side, three-quarter standing and two facial
expressions
Subject: 24-year-old tall very lean pale man, narrow angular face, defined
cheekbones, hollow cheeks, tired gray-brown eyes, short uneven very dark brown
hair, narrow high shoulders; rain-stained khaki nylon windbreaker, dark shirt,
faded black jeans, nylon running shoes
Composition/framing: clean production turnaround on neutral warm-gray background;
views separated and fully visible
Color palette: khaki, faded black, pale skin, small cyan rim light
Constraints: identical facial structure, proportions and outfit in every view;
not muscular, not glamorous; no weapons; no text or labels
```

## Reference `CHAR_MOLLY_V1`

```text
Primary request: definitive model sheet for Molly, the same adult woman shown
full-body front, full-body side, three-quarter defensive stance and close-up
Subject: 25-30-year-old slender athletic pale woman, oval-angular face, high
cheekbones, short rough black shag; surgically inset seamless silver mirrored
lenses growing from the skin with no arms; bulky matte-black jacket, tight black
glove-leather jeans, black boots; burgundy artificial nails
Composition/framing: clean production turnaround on neutral cool-gray background
Constraints: same identity and proportions in every view; mirrored lenses never
become removable sunglasses; no visible eyes; no sexualized pose; no text;
show one small separate hand study with four-centimeter retractable blades
```

## Supporting cast reference

```text
Primary request: production lineup of three distinct adult supporting characters:
Linda Lee, Ratz and Wage, each front three-quarter and one portrait
Subject: Linda is 20, small and tense, gray eyes with smudged black makeup, pale
under-eyes, dark hair tied with a silk circuit-map headband, faded blue sleeveless
orbital fatigues and white sneakers; Ratz is a huge 120-kg bald sweaty bartender
with steel-and-decay teeth, white shirt and a grubby pink Russian military
prosthesis as his right arm; Wage is 35-45, uniformly tanned, anonymous face,
vat-grown sea-green eyes, gunmetal silk suit and one platinum bracelet per wrist
Constraints: three clearly separate character blocks; adult anatomy; no glamour;
Ratz's prosthesis always right; no text or labels
```

## Environment reference

```text
Primary request: production environment board with four separate empty location
views: Chatsubo bar, Ninsei street, arcade back corridor and Cheap Hotel rooftop
Scene/backdrop: use the exact descriptions in bible/visual-bible.md
Composition/framing: four clearly separated cinematic establishing frames with
consistent architecture suitable for reuse
Constraints: no people; no readable text; no pristine generic sci-fi; retain
landmarks and spatial logic; no watermark
```

## Tavola campione 1

```text
Primary request: finished six-panel portrait comic page following storyboard
page 1; establish the dead gray port sky, crowded wet Ninsei, Case entering the
Chatsubo, Ratz behind the bar, pink prosthetic arm pouring beer, ending on a
two-shot of Case and Ratz
Input images: Case reference, supporting-cast reference and environment reference
Composition/framing: panel 1 wide across top; three middle panels; two bottom
panels; clean gutters and intentional cinematic flow
Constraints: preserve CHAR_CASE_V1, CHAR_RATZ_V1 and LOC_CHAT_V1 exactly; leave
natural negative space for later captions and balloons but draw no balloons and
no text
```

## Tavola campione 10

```text
Primary request: finished six-panel portrait action page following storyboard
page 10; bootsteps at a cheap office door, Case's fear, collapsing cobra, Case
diving diagonally through a broken plastic window, painful landing among wet
junk, final view of Molly's silver-lensed head framed in the high window
Input images: Case reference, Molly reference and environment reference
Composition/framing: narrow suspense panel on top, two close panels, large
diagonal action panel, two low aftermath panels
Constraints: preserve CHAR_CASE_V1 and CHAR_MOLLY_V1; Case still has khaki
windbreaker and cobra, no .22 pistol; Molly appears only as head/silhouette in
final panel; no text or balloons
```

## Tavola 14 — metodo bloccato v2.0

```text
Do not generate the finished page as one image. First create one spatial master
shot using CHAR_CASE_V1, CHAR_MOLLY_V1 and the dimensional drawing
assets/environments/capsule-92-layout-v2.svg.

LOC_COFFIN_92_V2 is exactly 3.00 m long, 1.00 m maximum width and 1.45 m maximum
height. Case remains within 0.75 m of the near hatch. Molly remains seated against
the far end at x=2.65 m in panels 14.1-14.4. Terminal is on the left wall looking
in; rules panel on the right; brown foam spans the floor. Never cross the
longitudinal axis.

Panels 14.1-14.4 must use the same master geometry. Crops come directly from the
master; action inserts such as the latch are controlled derivatives that preserve
all landmarks, scale, distance, light and camera axis. Generate only the later
holstering beat separately, using the master as reference. Composite the page
deterministically with a dedicated lettering rail above each associated image.

Constraints: surgically inset lenses without arms and no visible eyes; exactly
one fletcher until it is holstered; Case has no weapon; ten blades only in the
final panel; no text, balloons or labels inside generated art.
```
