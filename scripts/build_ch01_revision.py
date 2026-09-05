#!/usr/bin/env python3
"""Rebuild chapter 1 with panel-safe lettering and locked visual continuity.

The source illustrations stay text-free.  Each source panel is re-composed into
the trim page with its own dedicated dialogue rail, so no line of text can cover
a face, hand, weapon, prop, or action.  The capsule sequence deliberately uses
one geometry master and two controlled derivatives.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageDraw, ImageFont, ImageOps
from reportlab.lib.pagesizes import portrait
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas as pdfcanvas


ROOT = Path(__file__).resolve().parents[1]
PAGE_DIR = ROOT / "chapters" / "ch01" / "pages"
ASSET_DIR = ROOT / "assets"
EDITION = ROOT / "editions" / "neuromante-capitolo-01-completo.pdf"
PDF_TMP = ROOT / "tmp" / "pdfs-revision"

TRIM_PX = (2008, 3071)
TRIM_MM = (170 * mm, 260 * mm)
MARGIN = 18

FONT_REG = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
FONT_BOLD = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
FONT_OBLIQUE = FONT_REG
FONT_MONO = Path("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf")

INK = (241, 240, 229)
PAPER = (6, 9, 11)
RAIL = (12, 17, 20)
GUTTER = (2, 4, 5)

SPEAKER_COLORS = {
    "CASE": (49, 211, 211),
    "RATZ": (222, 163, 80),
    "LINDA": (211, 58, 111),
    "DEANE": (174, 127, 215),
    "SHIN": (100, 180, 232),
    "ZONE": (115, 193, 131),
    "MOLLY": (211, 225, 229),
    "WAGE": (207, 177, 94),
    "SNAKE": (179, 118, 204),
    "CUSTODE": (164, 176, 181),
    "VENDITRICE": (185, 157, 118),
    "VOCE": (168, 181, 184),
}


def font(path: Path, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(path), size=size)


def normalize(text: str) -> str:
    return (
        text.replace("\u2013", "-")
        .replace("\u2014", "-")
        .replace("\u2011", "-")
        .replace("\u00a0", " ")
    )


def wrap(draw: ImageDraw.ImageDraw, text: str, face: ImageFont.FreeTypeFont, width: int) -> list[str]:
    words = normalize(text).split()
    lines: list[str] = []
    current = ""
    for word in words:
        trial = word if not current else f"{current} {word}"
        if draw.textbbox((0, 0), trial, font=face)[2] <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def fit_lines(
    draw: ImageDraw.ImageDraw,
    text: str,
    width: int,
    height: int,
    *,
    bold: bool = False,
    italic: bool = False,
    start: int = 38,
    minimum: int = 22,
) -> tuple[ImageFont.FreeTypeFont, list[str], int]:
    path = FONT_BOLD if bold else FONT_OBLIQUE if italic else FONT_REG
    for size in range(start, minimum - 1, -1):
        face = font(path, size)
        lines = wrap(draw, text, face, width)
        leading = int(size * 1.15)
        if lines and len(lines) * leading <= height:
            return face, lines, leading
    face = font(path, minimum)
    return face, wrap(draw, text, face, width), int(minimum * 1.15)


@dataclass(frozen=True)
class Entry:
    kind: str
    text: str
    speaker: str = ""


@dataclass(frozen=True)
class Panel:
    crop: tuple[int, int, int, int]
    entries: tuple[Entry, ...] = ()
    rail: float = 0.0
    source: str = ""
    dest_ref: tuple[int, int, int, int] | None = None
    sounds: tuple[tuple[str, str], ...] = ()
    focus_y: float = 0.36


@dataclass(frozen=True)
class PageSpec:
    source: str
    bounds: tuple[int, int, int, int]
    panels: tuple[Panel, ...] = field(default_factory=tuple)


def C(text: str) -> Entry:
    return Entry("caption", text)


def D(speaker: str, text: str) -> Entry:
    return Entry("dialogue", text, speaker)


def T(text: str) -> Entry:
    return Entry("thought", text, "CASE")


def M(text: str) -> Entry:
    return Entry("meta", text)


def V(text: str) -> Entry:
    return Entry("voice", text, "VOCE")


PAGE_SPECS: dict[int, PageSpec] = {
    1: PageSpec("chapters/ch01/pages/page-01-art-v1.png", (0, 7, 864, 1813), (
        Panel((10, 7, 854, 314), (C("Il cielo sopra il porto aveva il colore di un televisore sintonizzato su un canale morto."), M("CHIBA CITY - VENERDÌ, 22:30")), .30, focus_y=.50),
        Panel((10, 326, 853, 631), (V("Non mi sto facendo. È il corpo che va in crisi senza roba."),), .25, sounds=(("HA!", "br"),)),
        Panel((10, 643, 854, 903), sounds=(("TCHK", "br"),), focus_y=.50),
        Panel((10, 916, 854, 1219), (D("RATZ", "Ecco l'artista."),), .22, focus_y=.28),
        Panel((10, 1230, 854, 1473), (D("RATZ", "Il virtuoso dell'affare storto."),), .28, sounds=(("ZZZT-KLIK", "br"),), focus_y=.50),
        Panel((10, 1486, 854, 1813), (D("CASE", "Qualcuno deve pur far ridere. Tu non ci riesci."), D("RATZ", "Wage è passato con due Joeboy. Cercava te?")), .34, focus_y=.28),
    )),
    2: PageSpec("chapters/ch01/pages/page-02-art-final.png", (0, 78, 1024, 1527), (
        Panel((10, 78, 1014, 394), (D("CASE", "Non che io sappia."),), .20),
        Panel((10, 406, 1014, 695), (D("RATZ", "Ho visto Linda. Con lei ridevi."), D("RATZ", "Continua così e finirai in una vasca, venduto a pezzi."), D("CASE", "Mi commuovi, Ratz.")), .38),
        Panel((10, 705, 1014, 1007), (C("A ventidue anni Case era uno dei migliori cowboy dello Sprawl. Nella matrice, la coscienza correva libera."),), .30),
        Panel((10, 1017, 386, 1527), (C("Poi rubò ai suoi datori di lavoro. Non lo uccisero: gli bruciarono il sistema nervoso."),), .34),
        Panel((395, 1017, 1015, 1527), (C("La matrice sparì. Rimase la carne: il corpo diventò una cella."),), .27),
    )),
    3: PageSpec("chapters/ch01/pages/page-03-art-final.png", (0, 13, 1024, 1523), (
        Panel((13, 13, 614, 506), (C("Un anno a Chiba. Tutto speso in cliniche che continuavano a dirgli di no."),), .25),
        Panel((624, 13, 1009, 506), (C("Ora viveva vicino al porto e rivendeva merce altrui."),), .28),
        Panel((13, 516, 365, 892), sounds=(("TIK", "br"),)),
        Panel((376, 516, 1010, 892), (C("A Night City dovevi muoverti. Fermarti significava sparire; correre troppo, farti notare."),), .30),
        Panel((13, 902, 348, 1099)),
        Panel((357, 902, 648, 1099)),
        Panel((658, 902, 1010, 1099), (C("Il dex gli accese ogni nervo."),), .42),
        Panel((13, 1109, 1010, 1523), (D("LINDA", "Ehi, Case. Ti cercavo."),), .20),
    )),
    4: PageSpec("chapters/ch01/pages/page-04-art-final.png", (0, 72, 1024, 1527), (
        Panel((9, 72, 509, 557), (C("L'aveva vista in quell'arcade, una notte di pioggia. In mezzo al rumore, il suo volto era diventato un segnale."),), .31),
        Panel((516, 72, 1015, 557)),
        Panel((9, 563, 509, 1014), (C("Per qualche settimana aveva ricominciato a ridere."),), .24),
        Panel((516, 563, 1015, 1014), (C("Poi il bisogno aveva cominciato a portarsela via."),), .25),
        Panel((9, 1021, 509, 1527), (D("LINDA", "Fumi? Dormi almeno?"), D("CASE", "Solo quando dimentico le pillole.")), .29),
        Panel((516, 1021, 1015, 1527), (D("LINDA", "Wage vuole farti ammazzare."), D("CASE", "Chi te l'ha detto?"), D("LINDA", "Mona. Il suo tipo lavora per lui.")), .38),
    )),
    5: PageSpec("chapters/ch01/pages/page-05-art-final.png", (0, 28, 1024, 1509), (
        Panel((19, 28, 1006, 448), (D("CASE", "Se mi ammazza, perde i suoi soldi."), D("LINDA", "Ne ha troppi in giro. Potrebbe scegliere te come esempio.")), .30),
        Panel((19, 460, 479, 843), (D("CASE", "Hai un posto per dormire?"), D("LINDA", "Certo.")), .29),
        Panel((491, 460, 1006, 843), (D("CASE", "Tieni."), D("LINDA", "Servono a te. Paga Wage."), D("CASE", "Gli devo molto più di così. Prendili.")), .40),
        Panel((19, 855, 479, 1102), (D("LINDA", "Appena incassi, vai da Wage."),), .32),
        Panel((19, 1112, 479, 1509), (D("CASE", "Ci vediamo, Linda."),), .24),
        Panel((491, 855, 1006, 1509), (D("LINDA", "Certo. Guardati le spalle."),), .20),
    )),
    6: PageSpec("chapters/ch01/pages/page-06-art-final.png", (0, 125, 1024, 1411), (
        Panel((14, 125, 513, 571), (C("Compratore, venditore, intermediario. Il trucco era rendersi indispensabile."),), .28),
        Panel((524, 125, 1010, 571)),
        Panel((14, 581, 513, 978), (T("Julie saprà qualcosa."),), .22),
        Panel((524, 581, 1010, 978), (D("DEANE", "Pulito. Entra, ragazzo mio."),), .25),
        Panel((14, 989, 513, 1411), (D("CASE", "Dicono che Wage voglia ammazzarmi."), D("DEANE", "Davvero? Chi lo dice?"), D("CASE", "Amici.")), .38),
        Panel((524, 989, 1010, 1411), (D("DEANE", "Non che io sappia. Però non è sempre facile capire chi ti è davvero amico."),), .30, sounds=(("THUNK", "br"),)),
    )),
    7: PageSpec("chapters/ch01/pages/page-07-art-final.png", (0, 11, 1024, 1526), (
        Panel((13, 11, 1011, 436), (C("Un po' di paranoia poteva tenerti vivo. Purché restasse al guinzaglio."),), .25),
        Panel((13, 442, 518, 763)),
        Panel((524, 442, 1011, 763), sounds=(("SKRT", "br"),)),
        Panel((13, 770, 1012, 1115), (D("CASE", "Mi serve una pistola."), D("SHIN", "Tra due ore. Adesso ho solo un taser."), D("CASE", "No. Mi serve qualcosa che spari.")), .38),
        Panel((13, 1122, 1011, 1526), (D("CASE", "Un'arma. Niente coltelli."), D("VENDITRICE", "Cobra.")), .27, sounds=(("KLAK-KLAK", "br"),)),
    )),
    8: PageSpec("chapters/ch01/pages/page-08-art-final.png", (0, 27, 1024, 1512), (
        Panel((10, 27, 355, 505)),
        Panel((365, 27, 1012, 505), (D("CASE", "Hai visto Wage?"), D("ZONE", "Forse al Namban. Due ore fa.")), .26),
        Panel((10, 517, 542, 972), (D("CASE", "Era con una donna? Capelli scuri, giacca nera?"), D("ZONE", "No. Due grossi, pieni d'innesti. Quello è un cobra? Vuoi spaccare qualcuno?")), .36),
        Panel((551, 517, 1013, 972), (C("La coda era di nuovo lì."),), .22),
        Panel((10, 985, 1013, 1512), (C("Troppo dex, troppi guai. Per un istante Ninsei tornò a essere una corsa nella matrice."), T("Forza. Seguimi.")), .28),
    )),
    9: PageSpec("chapters/ch01/pages/page-09-art-final.png", (0, 14, 1024, 1523), (
        Panel((14, 14, 678, 426), sounds=(("WHUMMMMM", "tr"),)),
        Panel((689, 14, 1010, 426)),
        Panel((14, 438, 480, 766), (D("CASE", "Chiama la sicurezza. Ho qualcuno alle spalle."),), .30),
        Panel((491, 438, 1010, 766), sounds=(("KRAK", "br"),)),
        Panel((14, 777, 541, 1089), sounds=(("TAK - TAK - KRSSH", "br"),)),
        Panel((551, 777, 1010, 1089)),
        Panel((14, 1103, 1010, 1523), (C("La porta sbagliata era aperta. Quella giusta, chiusa. Ora doveva aspettare."),), .28, sounds=(("WAA-OOO", "br"),)),
    )),
    10: PageSpec("chapters/ch01/pages/page-10-art-v1.png", (0, 7, 864, 1813), (
        Panel((8, 7, 856, 264), sounds=(("TOK... TOK...", "br"),)),
        Panel((8, 272, 856, 492), (C("La paranoia da dex era sparita. Questa era paura animale."),), .32),
        Panel((8, 499, 778, 698), sounds=(("KLIK-KLIK", "br"),)),
        Panel((8, 707, 856, 1123), sounds=(("KRASH", "br"),)),
        Panel((8, 1131, 856, 1448), (D("CASE", "Ngh..."),), .20, sounds=(("THUD", "br"),)),
        Panel((8, 1457, 856, 1813), (D("MOLLY", "Merda."),), .20),
    )),
    11: PageSpec("chapters/ch01/pages/page-11-art-final.png", (0, 15, 1024, 1522), (
        Panel((14, 15, 514, 490), (C("Due ore dopo, Shin gli consegnò la pistola."),), .24),
        Panel((528, 15, 1010, 490), sounds=(("KLANG", "br"),)),
        Panel((14, 503, 1010, 957), (M("01:10 - CHEAP HOTEL"),), .18),
        Panel((0, 0, 1536, 1024), (), 0.0, "assets/environments/capsule-92-case-alone-v3.png", (14, 971, 495, 1522), focus_y=.54),
        Panel((420, 40, 1450, 1024), (T("Tre mega di RAM rubata. E il compratore non risponde."),), .25, "assets/environments/capsule-92-phone-v3.png", (507, 971, 1010, 1522), sounds=(("DRR... DRR...", "br"),), focus_y=.54),
    )),
    12: PageSpec("chapters/ch01/pages/page-12-art-final.png", (0, 15, 1022, 1532), (
        Panel((350, 20, 1500, 1024), (D("CASE", "Ho la merce."), D("SNAKE", "Ottimo. Ma sono a corto. Mi fai credito?"), D("CASE", "No. Mi servono i soldi adesso.")), .40, "assets/environments/capsule-92-phone-v3.png", (13, 15, 507, 445), focus_y=.52),
        Panel((650, 150, 1450, 950), (T("Stronzo. Serata perfetta."),), .25, "assets/environments/capsule-92-phone-v3.png", (517, 15, 1017, 445), sounds=(("TUUU...", "tr"),), focus_y=.52),
        Panel((13, 456, 340, 742)),
        Panel((350, 456, 633, 742)),
        Panel((643, 456, 1017, 742)),
        Panel((13, 754, 1016, 1029), (D("RATZ", "Hai una faccia orribile, artista."), D("CASE", "Sto da dio."), D("RATZ", "Alcol e stimolanti: un'armatura contro paura e solitudine."), D("CASE", "Risparmiami la predica. Hai visto Wage?")), .48),
        Panel((13, 1040, 1017, 1532), (D("RATZ", "Sta entrando."),), .20),
    )),
    13: PageSpec("chapters/ch01/pages/page-13-art-final.png", (0, 11, 1024, 1526), (
        Panel((12, 11, 1011, 357), (D("RATZ", "Qui non si ammazza nessuno."), D("WAGE", "Vogliamo parlare.")), .28),
        Panel((12, 366, 1010, 642), (D("CASE", "Mi hanno detto che vuoi farmi fuori."), D("WAGE", "Che cazzo dici?")), .32),
        Panel((12, 650, 509, 869), sounds=(("KLAK - TIK", "br"),)),
        Panel((518, 650, 1010, 869), (D("WAGE", "Chi te l'ha detto? Ti stanno usando."), T("Linda.")), .40),
        Panel((12, 877, 585, 1085), (D("CASE", "È tutto. Estratto ipofisario: cinquecento, se fai presto."),), .42),
        Panel((594, 877, 1011, 1085), (D("WAGE", "Siamo pari. Ora vai a dormire."),), .40),
        Panel((12, 1093, 509, 1298), (C("La minaccia era falsa. Linda, invece, era sparita col resto."),), .42),
        Panel((518, 1093, 1011, 1298), (D("SHIN", "Le cartucce? Metà prezzo."), D("CASE", "Tieni.")), .44),
        Panel((15, 1307, 1001, 1526), (D("CASE", "È salita una ragazza? Capelli scuri, fascia di seta."), D("CUSTODE", "Aveva la tua chiave.")), .42),
    )),
    14: PageSpec("assets/environments/capsule-92-scene-master-v2.png", (0, 0, 2008, 3071), (
        Panel((0, 0, 1536, 1024), (D("MOLLY", "Chiudi piano. Hai ancora la pistola di Shin?"), D("CASE", "Eri tu all'arcade?")), .30, dest_ref=(18, 18, 1990, 620), focus_y=.31),
        Panel((0, 0, 1536, 1024), (D("CASE", "Dov'è Linda?"), D("MOLLY", "Prima chiudi il fermo.")), .30, "assets/environments/capsule-92-latch-v3.png", (18, 634, 996, 1250), focus_y=.39),
        Panel((650, 80, 1536, 940), (D("MOLLY", "È scappata col tuo Hitachi. La pistola?"), D("CASE", "Restituita. Vuoi i soldi?"), D("MOLLY", "No.")), .38, dest_ref=(1010, 634, 1990, 1250), focus_y=.31),
        Panel((0, 80, 1536, 860), (D("MOLLY", "Perché quel casino all'arcade?"), D("CASE", "Linda ha detto che Wage voleva uccidermi."), D("MOLLY", "Non l'avevo mai vista."), D("CASE", "Quindi non sei con Wage.")), .43, dest_ref=(18, 1264, 1990, 1775), focus_y=.31),
        Panel((500, 80, 1536, 950), (D("CASE", "Che cosa vuoi?"), D("MOLLY", "Portarti dal mio capo. Mi chiamo Molly. Vuole solo parlare."), D("CASE", "Che premura.")), .32, "assets/environments/capsule-92-holster-v2.png", (18, 1789, 996, 3053), focus_y=.43),
        Panel((0, 1065, 864, 1813), (D("MOLLY", "La pistola è via. Adesso te ne stai buono?"), D("CASE", "Un agnellino."), D("MOLLY", "Perfetto. Perché a volte faccio male alla gente.")), .30, "chapters/ch01/pages/page-14-art-v1.png", (1010, 1789, 1990, 3053), sounds=(("SNIK", "br"),), focus_y=.50),
    )),
}


def source_image(path: str, cache: dict[str, Image.Image]) -> Image.Image:
    if path not in cache:
        cache[path] = Image.open(ROOT / path).convert("RGB")
    return cache[path]


def map_dest(
    ref: tuple[int, int, int, int],
    bounds: tuple[int, int, int, int],
) -> tuple[int, int, int, int]:
    bx0, by0, bx1, by1 = bounds
    x0, y0, x1, y1 = ref
    inner_w = TRIM_PX[0] - 2 * MARGIN
    inner_h = TRIM_PX[1] - 2 * MARGIN
    dx0 = MARGIN + round((x0 - bx0) / (bx1 - bx0) * inner_w)
    dy0 = MARGIN + round((y0 - by0) / (by1 - by0) * inner_h)
    dx1 = MARGIN + round((x1 - bx0) / (bx1 - bx0) * inner_w)
    dy1 = MARGIN + round((y1 - by0) / (by1 - by0) * inner_h)
    return dx0, dy0, dx1, dy1


def paste_contained(
    canvas: Image.Image,
    crop: Image.Image,
    rect: tuple[int, int, int, int],
    focus_y: float,
) -> None:
    x0, y0, x1, y1 = rect
    width, height = max(1, x1 - x0), max(1, y1 - y0)
    # The source pages were generated in mixed aspect ratios.  Filling each
    # panel prevents the large dead side bars that made the previous edition
    # feel like a contact sheet.  Only the outer edges are cropped; text still
    # has its own rail and never competes with the illustration.
    fitted = ImageOps.fit(
        crop,
        (width, height),
        Image.Resampling.LANCZOS,
        centering=(0.5, focus_y),
    )
    canvas.paste(fitted, (x0, y0))


def entry_grid(count: int, width: int) -> tuple[int, int]:
    if count <= 1:
        return 1, 1
    if count == 2:
        return (2, 1) if width >= 560 else (1, 2)
    if count == 3:
        return (3, 1) if width >= 1050 else (2, 2)
    return 2, 2


def draw_entry(
    draw: ImageDraw.ImageDraw,
    rect: tuple[int, int, int, int],
    entry: Entry,
) -> None:
    x0, y0, x1, y1 = rect
    pad = 12
    if entry.kind == "caption":
        color = (46, 210, 210)
        label = "NARRAZIONE"
        italic = True
    elif entry.kind == "thought":
        color = (204, 48, 101)
        label = "CASE - PENSIERO"
        italic = True
    elif entry.kind == "meta":
        color = (44, 211, 209)
        label = ""
        italic = False
    else:
        color = SPEAKER_COLORS.get(entry.speaker, (190, 199, 201))
        label = entry.speaker
        italic = entry.kind == "voice"

    draw.rounded_rectangle((x0 + 4, y0 + 4, x1 - 4, y1 - 4), 12, fill=(15, 21, 24), outline=color, width=3)
    draw.rectangle((x0 + 4, y0 + 4, x0 + 12, y1 - 4), fill=color)
    label_h = 26 if label else 0
    if label:
        label_face = font(FONT_BOLD, 18)
        draw.text((x0 + pad + 8, y0 + 8), label, font=label_face, fill=color)
    tx0 = x0 + pad + 8
    ty0 = y0 + 8 + label_h
    tx1 = x1 - pad
    ty1 = y1 - 8
    start = 35 if x1 - x0 > 500 else 31
    face, lines, leading = fit_lines(
        draw,
        entry.text,
        tx1 - tx0,
        ty1 - ty0,
        italic=italic,
        bold=entry.kind == "meta",
        start=start,
        minimum=20,
    )
    total = len(lines) * leading
    yy = ty0 + max(0, (ty1 - ty0 - total) // 2)
    for line in lines:
        draw.text((tx0, yy), line, font=face, fill=INK)
        yy += leading


def draw_rail(
    draw: ImageDraw.ImageDraw,
    rect: tuple[int, int, int, int],
    entries: tuple[Entry, ...],
) -> None:
    x0, y0, x1, y1 = rect
    draw.rectangle(rect, fill=RAIL)
    cols, rows = entry_grid(len(entries), x1 - x0)
    gap = 8
    cell_w = (x1 - x0 - gap * (cols + 1)) // cols
    cell_h = (y1 - y0 - gap * (rows + 1)) // rows
    for index, entry in enumerate(entries):
        row, col = divmod(index, cols)
        cx0 = x0 + gap + col * (cell_w + gap)
        cy0 = y0 + gap + row * (cell_h + gap)
        draw_entry(draw, (cx0, cy0, cx0 + cell_w, cy0 + cell_h), entry)


def draw_sounds(
    draw: ImageDraw.ImageDraw,
    rect: tuple[int, int, int, int],
    sounds: Iterable[tuple[str, str]],
) -> None:
    x0, y0, x1, y1 = rect
    for index, (text, anchor) in enumerate(sounds):
        face = font(FONT_BOLD, max(30, min(56, (y1 - y0) // 5)))
        bbox = draw.textbbox((0, 0), text, font=face, stroke_width=5)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        if anchor == "tr":
            px, py = x1 - tw - 20, y0 + 18 + index * (th + 8)
        elif anchor == "tl":
            px, py = x0 + 20, y0 + 18 + index * (th + 8)
        elif anchor == "bl":
            px, py = x0 + 20, y1 - th - 22 - index * (th + 8)
        else:
            px, py = x1 - tw - 20, y1 - th - 22 - index * (th + 8)
        draw.text((px, py), text, font=face, fill=INK, stroke_width=5, stroke_fill=(1, 2, 3))


def render_page(number: int, spec: PageSpec) -> Path:
    canvas = Image.new("RGB", TRIM_PX, PAPER)
    draw = ImageDraw.Draw(canvas)
    cache: dict[str, Image.Image] = {}

    for panel in spec.panels:
        source_path = panel.source or spec.source
        src = source_image(source_path, cache)
        crop = src.crop(panel.crop)
        ref = panel.dest_ref or panel.crop
        dx0, dy0, dx1, dy1 = map_dest(ref, spec.bounds)
        # Leave a clean gutter between panels regardless of source gutter width.
        dx0 += 4
        dy0 += 4
        dx1 -= 4
        dy1 -= 4
        draw.rectangle((dx0, dy0, dx1, dy1), fill=GUTTER, outline=(58, 78, 82), width=2)

        rail_h = 0
        if panel.entries:
            rail_h = max(86, round((dy1 - dy0) * panel.rail))
            rail_h = min(rail_h, max(86, (dy1 - dy0) - 100))
        art_rect = (dx0 + 4, dy0 + rail_h + 4, dx1 - 4, dy1 - 4)
        if art_rect[3] <= art_rect[1]:
            raise ValueError(f"invalid art rect on page {number}: {art_rect}")
        paste_contained(canvas, crop, art_rect, panel.focus_y)
        if panel.entries:
            draw_rail(draw, (dx0 + 4, dy0 + 4, dx1 - 4, dy0 + rail_h), panel.entries)
        if panel.sounds:
            draw_sounds(draw, art_rect, panel.sounds)

    # Quiet folio outside all narrative panels.
    folio = font(FONT_MONO, 22)
    draw.text((TRIM_PX[0] - 34, TRIM_PX[1] - 22), str(number), font=folio, anchor="rs", fill=(166, 177, 178))

    out = PAGE_DIR / f"page-{number:02}-lettered-final.png"
    tmp = out.with_suffix(".tmp.png")
    canvas.save(tmp, "PNG", optimize=True)
    with Image.open(tmp) as check:
        check.load()
        if check.size != TRIM_PX:
            raise ValueError(f"wrong page size: {out}")
    tmp.replace(out)
    return out


def make_cover() -> Path:
    out = ROOT / "editions" / "cover-capitolo-01-completo.png"
    img = Image.new("RGB", TRIM_PX, (4, 7, 10))
    draw = ImageDraw.Draw(img)
    for i in range(20):
        x = 55 + i * 105
        draw.line((x, 0, x - 360, TRIM_PX[1]), fill=(8, 60 + i * 2, 70), width=3)
    for j in range(24):
        y = 300 + j * 110
        draw.line((0, y, TRIM_PX[0], y - 280), fill=(72, 9, 38), width=2)
    draw.rectangle((145, 410, 1865, 2530), outline=(46, 219, 216), width=8)
    draw.rectangle((190, 455, 1820, 2485), outline=(188, 38, 82), width=3)
    draw.text((170, 675), "NEUROMANTE", font=font(FONT_BOLD, 182), fill=(243, 240, 223))
    draw.text((180, 930), "CAPITOLO 1", font=font(FONT_MONO, 82), fill=(52, 218, 216))
    draw.text((180, 1060), "EDIZIONE RIVISTA", font=font(FONT_BOLD, 76), fill=(202, 43, 88))
    draw.line((180, 1240, 1530, 1240), fill=(240, 238, 220), width=5)
    draw.text((180, 1320), "14 TAVOLE FINITE", font=font(FONT_MONO, 48), fill=(236, 233, 216))
    draw.text((180, 1410), "LETTERING IN AREE RISERVATE", font=font(FONT_MONO, 35), fill=(236, 233, 216))
    draw.text((180, 2280), "VERSIONE 2.0", font=font(FONT_MONO, 36), fill=(171, 180, 174))
    tmp = out.with_suffix(".tmp.png")
    img.save(tmp, "PNG", optimize=True)
    with Image.open(tmp) as check:
        check.load()
    tmp.replace(out)
    return out


def pdf_proxy(path: Path, quality: int = 76) -> Path:
    PDF_TMP.mkdir(parents=True, exist_ok=True)
    out = PDF_TMP / f"{path.stem}-q{quality}.jpg"
    with Image.open(path) as image:
        proxy = image.convert("RGB")
        proxy.thumbnail((1600, 2447), Image.Resampling.LANCZOS)
        proxy.save(out, "JPEG", quality=quality, optimize=True, progressive=True, subsampling=1)
    return out


def build_pdf(cover: Path, pages: list[Path]) -> None:
    EDITION.parent.mkdir(parents=True, exist_ok=True)
    tmp = EDITION.with_suffix(".tmp.pdf")
    pdf = pdfcanvas.Canvas(str(tmp), pagesize=portrait(TRIM_MM), pageCompression=1)
    pdf.setTitle("Neuromante - Capitolo 1 - Edizione rivista")
    pdf.setAuthor("Progetto Neuromante")
    pdf.setSubject("Adattamento italiano a fumetti - lettering e continuità v2")
    width, height = portrait(TRIM_MM)
    for path in [cover, *pages]:
        proxy = pdf_proxy(path)
        pdf.drawImage(str(proxy), 0, 0, width=width, height=height, preserveAspectRatio=False, mask="auto")
        pdf.showPage()
    pdf.save()
    tmp.replace(EDITION)


def main() -> None:
    PAGE_DIR.mkdir(parents=True, exist_ok=True)
    pages = [render_page(number, PAGE_SPECS[number]) for number in range(1, 15)]
    cover = make_cover()
    build_pdf(cover, pages)
    print(f"built {EDITION}")


if __name__ == "__main__":
    main()
