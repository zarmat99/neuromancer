#!/usr/bin/env python3
"""Build the fully lettered 14-page chapter-one comic and its comic-only PDF."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import portrait
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas as pdfcanvas


ROOT = Path(__file__).resolve().parents[1]
PAGES = ROOT / "chapters" / "ch01" / "pages"
EDITION = ROOT / "editions" / "neuromante-capitolo-01-completo.pdf"
PDF_TMP = ROOT / "tmp" / "pdfs-complete"

TRIM_PX = (2008, 3071)
TRIM_MM = (170 * mm, 260 * mm)

FONT_REG = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
FONT_BOLD = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
FONT_MONO = Path("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf")


def face(path: Path, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(path), size=size)


def normalize(text: str) -> str:
    return (
        text.replace("\u2013", "-")
        .replace("\u2014", "-")
        .replace("\u2011", "-")
        .replace("\u00a0", " ")
    )


def wrap(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, width: int) -> list[str]:
    words = normalize(text).split()
    lines: list[str] = []
    current = ""
    for word in words:
        trial = word if not current else f"{current} {word}"
        if draw.textbbox((0, 0), trial, font=font)[2] <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def fit_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    width: int,
    height: int,
    *,
    bold: bool = False,
    start: int = 44,
    minimum: int = 24,
) -> tuple[ImageFont.FreeTypeFont, list[str], int]:
    path = FONT_BOLD if bold else FONT_REG
    for size in range(start, minimum - 1, -1):
        font = face(path, size)
        lines = wrap(draw, text, font, width)
        line_height = int(size * 1.14)
        if lines and len(lines) * line_height <= height:
            return font, lines, line_height
    font = face(path, minimum)
    return font, wrap(draw, text, font, width), int(minimum * 1.14)


def add_box(
    draw: ImageDraw.ImageDraw,
    rect: tuple[int, int, int, int],
    text: str,
    kind: str,
    tail: tuple[int, int] | None = None,
) -> None:
    x, y, w, h = rect
    if kind == "sfx":
        font, lines, line_height = fit_text(draw, text, w, h, bold=True, start=66, minimum=30)
        yy = y + (h - len(lines) * line_height) / 2
        for line in lines:
            tw = draw.textbbox((0, 0), line, font=font)[2]
            draw.text(
                (x + (w - tw) / 2, yy),
                line,
                font=font,
                fill=(245, 243, 228, 255),
                stroke_width=max(3, font.size // 10),
                stroke_fill=(3, 5, 7, 255),
            )
            yy += line_height
        return

    if kind == "caption":
        fill = (8, 13, 18, 235)
        outline = (49, 214, 213, 255)
        ink = (246, 245, 232, 255)
        bold = False
        radius = 10
    elif kind == "thought":
        fill = (16, 19, 26, 238)
        outline = (196, 43, 91, 255)
        ink = (248, 244, 231, 255)
        bold = False
        radius = 20
    elif kind == "cartiglio":
        fill = (42, 211, 209, 244)
        outline = (4, 20, 24, 255)
        ink = (4, 18, 21, 255)
        bold = True
        radius = 9
    else:
        fill = (250, 248, 237, 250)
        outline = (5, 7, 9, 255)
        ink = (8, 10, 12, 255)
        bold = False
        radius = min(42, h // 2)

    if kind == "balloon" and tail is not None:
        tx, ty = tail
        cx, cy = x + w / 2, y + h / 2
        if abs(tx - cx) > abs(ty - cy):
            bx = x if tx < cx else x + w
            by = max(y + 20, min(y + h - 20, ty))
            base = [(bx, by - 18), (bx, by + 18)]
        else:
            by = y if ty < cy else y + h
            bx = max(x + 22, min(x + w - 22, tx))
            base = [(bx - 18, by), (bx + 18, by)]
        draw.polygon([base[0], (tx, ty), base[1]], fill=fill)
        draw.line([base[0], (tx, ty), base[1]], fill=outline, width=5, joint="curve")

    draw.rounded_rectangle(
        (x, y, x + w, y + h),
        radius=radius,
        fill=fill,
        outline=outline,
        width=5,
    )
    pad_x, pad_y = 20, 12
    font, lines, line_height = fit_text(
        draw,
        text,
        w - 2 * pad_x,
        h - 2 * pad_y,
        bold=bold,
        start=44 if kind == "balloon" else 40,
        minimum=23,
    )
    yy = y + (h - len(lines) * line_height) / 2
    for line in lines:
        tw = draw.textbbox((0, 0), line, font=font)[2]
        draw.text((x + (w - tw) / 2, yy), line, font=font, fill=ink)
        yy += line_height


def crop_to_fill(
    src: Image.Image,
    size: tuple[int, int],
    crop: tuple[int, int, int, int] | None = None,
) -> Image.Image:
    if crop is not None:
        src = src.crop(crop)
    target_w, target_h = size
    scale = max(target_w / src.width, target_h / src.height)
    resized = src.resize(
        (int(round(src.width * scale)), int(round(src.height * scale))),
        Image.Resampling.LANCZOS,
    )
    left = (resized.width - target_w) // 2
    top = (resized.height - target_h) // 2
    return resized.crop((left, top, left + target_w, top + target_h))


def compose_page14_art() -> Path:
    """Build six panels from a fixed spatial master; Case and Molly never swap axes."""
    master = Image.open(ROOT / "assets/environments/capsule-92-scene-master-v2.png").convert("RGB")
    holster = Image.open(ROOT / "assets/environments/capsule-92-holster-v2.png").convert("RGB")
    old = Image.open(PAGES / "page-14-art-v1.png").convert("RGB")

    page = Image.new("RGB", TRIM_PX, (3, 5, 7))
    draw = ImageDraw.Draw(page)
    margin, gutter = 20, 14
    panel_w = TRIM_PX[0] - 2 * margin
    heights = [560, 330, 360, 450, 450, 811]
    bands = [190, 100, 125, 240, 200, 195]
    sources = [master, master, master, master, holster, old]
    crops = [
        (0, 165, 1536, 515),
        (0, 185, 1536, 415),
        (0, 230, 1536, 465),
        (0, 175, 1536, 445),
        (0, 185, 1536, 460),
        (0, 1230, 864, 1506),
    ]

    y = margin
    for index, (height, band, src, crop) in enumerate(zip(heights, bands, sources, crops), 1):
        art_h = height - band
        art = crop_to_fill(src, (panel_w, art_h), crop)
        page.paste(art, (margin, y + band))
        draw.rectangle((margin, y, margin + panel_w - 1, y + height - 1), outline=(0, 0, 0), width=9)
        draw.line((margin, y + band, margin + panel_w, y + band), fill=(0, 0, 0), width=8)
        label = face(FONT_MONO, 22)
        draw.text((margin + 12, y + 9), f"14.{index}", font=label, fill=(75, 112, 116))
        y += height + gutter

    out = PAGES / "page-14-art-final.png"
    tmp = out.with_suffix(".tmp.png")
    page.save(tmp, "PNG")
    with Image.open(tmp) as check:
        check.load()
    tmp.replace(out)
    return out


# Coordinates are expressed in each source art file's pixel space. Every spoken
# balloon has a tail; captions and thoughts use a distinct, consistent frame.
LETTERING: dict[int, list[tuple]] = {
    1: [
        ("caption", (24, 24, 510, 92), "Il cielo sopra il porto aveva il colore di un televisore sintonizzato su un canale morto."),
        ("cartiglio", (590, 28, 240, 54), "CHIBA CITY - 22:30"),
        ("balloon", (-145, 350, 285, 130), "Io non mi drogo. È il mio corpo che soffre di una grave carenza di stupefacenti.", (220, 440)),
        ("sfx", (680, 390, 120, 58), "HA!"),
        ("sfx", (690, 760, 120, 58), "TCHK"),
        ("balloon", (745, 915, 190, 82), "Ecco l'artista.", (470, 1040)),
        ("balloon", (-135, 1205, 300, 105), "L'artista dei traffici un po' sporchi.", (440, 1355)),
        ("sfx", (650, 1360, 180, 62), "ZZZT-KLIK"),
        ("balloon", (-145, 1520, 270, 130), "Qui qualcuno deve pur far ridere. Di certo non tu.", (235, 1660)),
        ("balloon", (740, 1510, 250, 132), "Wage è passato presto. Aveva con sé due Joeboy.", (650, 1660)),
        ("balloon", (760, 1660, 210, 82), "Affari con te?", (650, 1690)),
    ],
    2: [
        ("balloon", (45, 25, 300, 65), "Non che io sappia.", (350, 220)),
        ("balloon", (20, 570, 600, 110), "Ieri ho visto Linda Lee. Con lei ridevi di più. Continua così e finirai in una vasca clinica. A pezzi.", (760, 500)),
        ("balloon", (640, 590, 350, 82), "Non ho una ragazza. Mi spezzi il cuore, Ratz.", (320, 500)),
        ("caption", (22, 720, 410, 72), "A ventidue anni Case era tra i migliori cowboy dello Sprawl."),
        ("caption", (22, 800, 440, 80), "Nella matrice la coscienza correva libera. Il corpo restava indietro."),
        ("caption", (20, 1030, 395, 70), "Poi rubò ai suoi datori di lavoro."),
        ("caption", (20, 1405, 405, 92), "Non lo uccisero. Gli avvelenarono il sistema nervoso."),
        ("caption", (540, 1030, 420, 72), "La matrice sparì. Rimase la carne."),
        ("caption", (585, 1405, 390, 92), "E il suo corpo diventò una cella."),
    ],
    3: [
        ("caption", (22, 22, 425, 76), "Un anno a Chiba. Tutto speso in cliniche che dicevano no."),
        ("caption", (565, 22, 420, 76), "Ora dormiva vicino al porto e rivendeva merce altrui."),
        ("sfx", (230, 750, 130, 60), "TIK"),
        ("caption", (600, 535, 390, 76), "Night City pretendeva movimento."),
        ("caption", (600, 620, 390, 88), "Fermarsi era sparire. Correre troppo, farsi notare."),
        ("caption", (650, 925, 335, 76), "Il dex gli accese ogni nervo."),
        ("balloon", (30, 1130, 385, 82), "Ehi, Case. Ti cercavo.", (230, 1335)),
    ],
    4: [
        ("caption", (20, 20, 455, 76), "L'aveva vista lì, una notte di pioggia."),
        ("caption", (20, 105, 455, 88), "In mezzo al rumore, quel volto era diventato un segnale."),
        ("caption", (20, 575, 430, 76), "Per qualche settimana aveva ricominciato a ridere."),
        ("caption", (555, 575, 420, 86), "Poi il bisogno aveva iniziato a portarsela via."),
        ("balloon", (20, 1035, 285, 92), "Vuoi una sigaretta? Riesci a dormire?", (190, 1300)),
        ("balloon", (250, 1400, 245, 100), "Non quando mi ricordo di prendere le pillole.", (385, 1325)),
        ("balloon", (550, 1035, 360, 76), "Wage vuole farti fuori.", (960, 1260)),
        ("balloon", (535, 1375, 215, 66), "Chi te l'ha detto?", (520, 1310)),
        ("balloon", (755, 1370, 240, 92), "Mona. Sta con uno dei suoi.", (900, 1500)),
    ],
    5: [
        ("balloon", (30, 25, 400, 78), "Non gli devo abbastanza. Se mi ammazza, perde i soldi.", (250, 245)),
        ("balloon", (555, 25, 430, 78), "Troppi gli devono soldi.", (710, 240)),
        ("balloon", (630, 110, 340, 70), "Potresti servire da esempio.", (710, 240)),
        ("balloon", (20, 475, 275, 64), "Hai dove dormire?", (490, 650)),
        ("balloon", (310, 475, 155, 58), "Certo.", (260, 650)),
        ("balloon", (520, 475, 165, 58), "Tieni.", (650, 665)),
        ("balloon", (690, 475, 305, 82), "Servono più a te. Dalli a Wage.", (800, 675)),
        ("balloon", (545, 740, 420, 76), "Gli devo molto di più. Prendili.", (680, 690)),
        ("balloon", (20, 865, 440, 82), "Quando incassi, vai da Wage. Subito.", (255, 985)),
        ("balloon", (35, 1135, 350, 72), "Ci vediamo, Linda.", (270, 1370)),
        ("balloon", (650, 1135, 330, 82), "Sicuro. Guardati le spalle.", (805, 1360)),
    ],
    6: [
        ("caption", (25, 20, 455, 76), "Compratore. Venditore. Intermediario."),
        ("caption", (535, 20, 460, 76), "Il trucco era convincerli che avessero bisogno di te."),
        ("thought", (25, 600, 395, 70), "CASE - Julie saprà qualcosa."),
        ("balloon", (575, 600, 405, 72), "Sei pulito, ragazzo mio. Entra.", (865, 760)),
        ("balloon", (25, 1000, 360, 72), "Ho sentito che Wage vuole ammazzarmi.", (190, 1210)),
        ("balloon", (245, 1080, 245, 64), "E chi l'avrebbe detto?", (400, 1190)),
        ("balloon", (25, 1160, 190, 58), "Amici.", (190, 1210)),
        ("balloon", (550, 1000, 430, 112), "Non che io sappia. Ma non è sempre facile capire chi sia davvero tuo amico.", (865, 1200)),
        ("sfx", (810, 1295, 175, 60), "THUNK"),
    ],
    7: [
        ("caption", (20, 20, 440, 76), "Un po' di paranoia poteva tenerti vivo."),
        ("caption", (540, 20, 445, 76), "Purché restasse al guinzaglio."),
        ("sfx", (790, 650, 155, 60), "SKRT"),
        ("balloon", (600, 775, 380, 62), "Mi affitti una pistola?", (700, 915)),
        ("balloon", (25, 950, 435, 80), "Due ore. Prima posso darti solo un taser.", (250, 900)),
        ("balloon", (535, 1020, 420, 76), "No. Voglio qualcosa che spari.", (700, 920)),
        ("balloon", (25, 1135, 310, 72), "Voglio un'arma. Niente coltelli.", (240, 1310)),
        ("balloon", (675, 1135, 280, 64), "Cobra.", (780, 1300)),
        ("sfx", (650, 1430, 340, 64), "KLAK-KLAK-KLAK"),
    ],
    8: [
        ("balloon", (385, 25, 275, 62), "Hai visto Wage?", (500, 270)),
        ("balloon", (675, 25, 315, 72), "Forse al Namban. Due ore fa.", (735, 270)),
        ("balloon", (20, 790, 520, 82), "Wage era con una donna? Capelli scuri, giacca nera?", (200, 700)),
        ("balloon", (180, 875, 470, 98), "No. Due uomini grossi e innestati. E quello è un cobra? Vuoi fare a pezzi qualcuno?", (425, 700)),
        ("caption", (605, 525, 365, 72), "La coda era di nuovo lì."),
        ("caption", (20, 1000, 330, 72), "Troppo dex. Troppi guai."),
        ("caption", (665, 1000, 330, 94), "Per un istante Ninsei tornò a essere una corsa nella matrice."),
        ("thought", (700, 1430, 270, 68), "CASE - Avanti. Seguimi."),
    ],
    9: [
        ("sfx", (175, 30, 290, 66), "WHUMMMMM"),
        ("balloon", (25, 455, 400, 84), "Chiama la sicurezza. Qualcuno mi sta seguendo.", (330, 635)),
        ("sfx", (760, 640, 210, 62), "KRAK"),
        ("sfx", (230, 880, 310, 66), "TAK - TAK - KRSSH"),
        ("caption", (565, 1135, 420, 82), "La porta sbagliata era aperta. Quella giusta, chiusa."),
        ("caption", (565, 1225, 420, 72), "Adesso doveva aspettare."),
        ("sfx", (650, 1390, 340, 72), "WAA-OOO / WAA-OOO"),
    ],
    10: [
        ("sfx", (610, 110, 225, 62), "TOK... TOK..."),
        ("caption", (-155, 285, 175, 118), "La paranoia da dex era sparita."),
        ("caption", (-155, 415, 175, 105), "Questa era paura animale."),
        ("sfx", (640, 580, 185, 58), "KLIK-KLIK"),
        ("sfx", (630, 850, 190, 66), "KRASH"),
        ("sfx", (635, 1190, 170, 60), "THUD"),
        ("balloon", (-90, 1205, 145, 70), "Ngh--", (260, 1270)),
        ("balloon", (825, 1510, 170, 78), "Merda.", (470, 1580)),
    ],
    11: [
        ("caption", (20, 20, 425, 80), "Due ore dopo, Shin gli consegnò la pistola."),
        ("sfx", (790, 385, 180, 62), "KLANG"),
        ("cartiglio", (30, 525, 300, 56), "01:10 - CHEAP HOTEL"),
        ("thought", (555, 1010, 420, 98), "CASE - Tre mega di RAM rubata. E il compratore non risponde."),
        ("sfx", (670, 1200, 300, 66), "DRR... DRR... DRR..."),
    ],
    12: [
        ("balloon", (20, 20, 240, 96), "Ho la merce che volevi.", (235, 230)),
        ("balloon", (275, 20, 220, 116), "Sono a corto di contanti. Puoi farmi credito?", (430, 105)),
        ("balloon", (20, 315, 320, 66), "Mi servono quei soldi.", (235, 235)),
        ("sfx", (810, 25, 170, 58), "TUUU--"),
        ("thought", (600, 310, 380, 92), "CASE - Stronzo. Stasera si mette male."),
        ("balloon", (20, 760, 360, 66), "Hai una faccia orribile, artista.", (540, 900)),
        ("balloon", (700, 760, 300, 76), "Sto benissimo. Mai stato meglio.", (855, 900)),
        ("balloon", (20, 930, 650, 92), "Alcol e stimolanti: una bella corazza contro la paura e la solitudine.", (540, 900)),
        ("balloon", (700, 930, 300, 76), "Lasciami stare. Hai visto Wage?", (855, 900)),
        ("balloon", (25, 1060, 420, 74), "Credo che tu stia per vederlo.", (135, 1280)),
    ],
    13: [
        ("balloon", (25, 20, 410, 72), "Niente guai, qui. Chiaro?", (260, 220)),
        ("balloon", (650, 20, 330, 66), "Vogliamo solo parlare.", (855, 230)),
        ("balloon", (500, 370, 345, 72), "Ho sentito che vuoi farmi fuori.", (650, 565)),
        ("balloon", (660, 445, 320, 66), "Ma che cazzo ti prende?", (855, 565)),
        ("balloon", (25, 520, 305, 64), "Non nel mio locale.", (250, 555)),
        ("sfx", (245, 690, 220, 60), "KLAK - TIK"),
        ("balloon", (550, 680, 430, 88), "Chi te l'ha detto? Qualcuno ti sta usando, Case.", (790, 790)),
        ("thought", (610, 790, 250, 62), "CASE - Linda."),
        ("balloon", (20, 900, 455, 92), "È tutto quello che ho. Estratto ipofisario. Vale cinquecento, se lo vendi in fretta.", (250, 1010)),
        ("balloon", (550, 900, 430, 86), "Così siamo pari. Ma fai schifo, Case. Vai a dormire.", (790, 1015)),
        ("caption", (20, 1120, 315, 66), "La minaccia era falsa."),
        ("thought", (20, 1192, 430, 82), "CASE - Linda, invece, se n'era andata con tutto."),
        ("balloon", (550, 1120, 300, 64), "Le cartucce? Metà prezzo.", (780, 1240)),
        ("balloon", (780, 1195, 200, 62), "Prendile.", (600, 1240)),
        ("balloon", (20, 1330, 500, 86), "È salita una ragazza? Capelli scuri. Una fascia di seta qui.", (280, 1470)),
        ("balloon", (620, 1330, 350, 72), "Aveva la tua chiave.", (780, 1460)),
    ],
    14: [
        ("balloon", (900, 35, 320, 72), "Chiudi piano.", (1510, 350)),
        ("balloon", (1230, 35, 730, 78), "Hai ancora la pistola che hai preso da Shin?", (1510, 350)),
        ("balloon", (45, 120, 500, 70), "Eri tu, all'arcade?", (430, 350)),
        ("balloon", (50, 608, 450, 72), "Dov'è Linda?", (430, 810)),
        ("balloon", (1110, 608, 820, 72), "Prima blocca il portello.", (1510, 810)),
        ("balloon", (780, 945, 1120, 62), "È scappata col tuo Hitachi. E la pistola?", (1510, 1160)),
        ("balloon", (50, 1010, 750, 70), "Restituita. Vuoi i soldi?", (430, 1160)),
        ("balloon", (1660, 1010, 230, 65), "No.", (1510, 1160)),
        ("balloon", (1050, 1320, 850, 56), "Che ti è preso all'arcade?", (1510, 1640)),
        ("balloon", (50, 1378, 1000, 58), "Linda ha detto che volevi uccidermi.", (430, 1640)),
        ("balloon", (800, 1438, 1100, 58), "Prima di salire qui non l'avevo mai vista.", (1510, 1640)),
        ("balloon", (50, 1498, 850, 54), "Allora non sei con Wage.", (430, 1640)),
        ("balloon", (50, 1790, 450, 70), "Che cosa vuoi?", (430, 2100)),
        ("balloon", (650, 1785, 1280, 115), "Te. Mi chiamo Molly. L'uomo per cui lavoro vuole parlarti. Nessuno vuole farti del male.", (1510, 2090)),
        ("balloon", (100, 1910, 280, 66), "Bene.", (430, 2100)),
        ("balloon", (650, 2254, 1280, 105), "Io, però, ogni tanto faccio male alla gente. Sono fatta così. Se la metto via, resti tranquillo?", (1540, 2680)),
        ("balloon", (50, 2365, 420, 68), "Tranquillissimo.", (20, 2640)),
        ("balloon", (500, 2365, 1350, 68), "Bene. Perché se provi qualcosa, te ne pentirai."),
        ("sfx", (1640, 2870, 300, 82), "SNIK"),
    ],
}


ART_FILES = {
    1: "page-01-art-v1.png",
    2: "page-02-art-final.png",
    3: "page-03-art-final.png",
    4: "page-04-art-final.png",
    5: "page-05-art-final.png",
    6: "page-06-art-final.png",
    7: "page-07-art-final.png",
    8: "page-08-art-final.png",
    9: "page-09-art-final.png",
    10: "page-10-art-v1.png",
    11: "page-11-art-final.png",
    12: "page-12-art-final.png",
    13: "page-13-art-final.png",
    14: "page-14-art-final.png",
}


def letter_page(page_no: int) -> Path:
    src = Image.open(PAGES / ART_FILES[page_no]).convert("RGB")
    canvas = Image.new("RGB", TRIM_PX, (4, 6, 8))

    if page_no in (1, 10):
        scale = min(TRIM_PX[0] / src.width, TRIM_PX[1] / src.height)
    else:
        scale = max(TRIM_PX[0] / src.width, TRIM_PX[1] / src.height)
    art_size = (int(round(src.width * scale)), int(round(src.height * scale)))
    art = src.resize(art_size, Image.Resampling.LANCZOS)
    x0 = (TRIM_PX[0] - art.width) // 2
    y0 = (TRIM_PX[1] - art.height) // 2
    canvas.paste(art, (x0, y0))

    draw = ImageDraw.Draw(canvas, "RGBA")
    if x0 > 0:
        draw.line((x0 - 4, 0, x0 - 4, TRIM_PX[1]), fill=(43, 210, 210, 200), width=3)
        draw.line((x0 + art.width + 3, 0, x0 + art.width + 3, TRIM_PX[1]), fill=(190, 40, 86, 190), width=3)

    for entry in LETTERING[page_no]:
        kind, (x, y, w, h), text = entry[:3]
        tail = entry[3] if len(entry) > 3 else None
        rect = (
            int(round(x0 + x * scale)),
            int(round(y0 + y * scale)),
            int(round(w * scale)),
            int(round(h * scale)),
        )
        mapped_tail = None
        if tail is not None:
            mapped_tail = (
                int(round(x0 + tail[0] * scale)),
                int(round(y0 + tail[1] * scale)),
            )
        add_box(draw, rect, text, kind, mapped_tail)

    # Quiet page marker, kept in the trim corner and outside the narrative focus.
    draw.ellipse((TRIM_PX[0] - 76, TRIM_PX[1] - 76, TRIM_PX[0] - 20, TRIM_PX[1] - 20), fill=(5, 8, 10, 220))
    draw.text(
        (TRIM_PX[0] - 48, TRIM_PX[1] - 48),
        str(page_no),
        font=face(FONT_MONO, 24),
        anchor="mm",
        fill=(224, 226, 216, 255),
    )

    out = PAGES / f"page-{page_no:02}-lettered-final.png"
    tmp = out.with_suffix(".tmp.png")
    canvas.save(tmp, "PNG")
    with Image.open(tmp) as check:
        check.load()
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
    draw.text((170, 675), "NEUROMANTE", font=face(FONT_BOLD, 182), fill=(243, 240, 223))
    draw.text((180, 930), "CAPITOLO 1", font=face(FONT_MONO, 82), fill=(52, 218, 216))
    draw.text((180, 1060), "FUMETTO COMPLETO", font=face(FONT_BOLD, 71), fill=(202, 43, 88))
    draw.line((180, 1240, 1530, 1240), fill=(240, 238, 220), width=5)
    draw.text((180, 1320), "14 TAVOLE FINITE", font=face(FONT_MONO, 48), fill=(236, 233, 216))
    draw.text((180, 1410), "DIALOGHI ITALIANI REVISIONATI", font=face(FONT_MONO, 34), fill=(236, 233, 216))
    draw.text((180, 2280), "VERSIONE 1.0", font=face(FONT_MONO, 36), fill=(171, 180, 174))
    tmp = out.with_suffix(".tmp.png")
    img.save(tmp, "PNG")
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
        proxy.save(
            out,
            "JPEG",
            quality=quality,
            optimize=True,
            progressive=True,
            subsampling=1,
        )
    return out


def build_pdf(cover: Path, pages: list[Path]) -> None:
    EDITION.parent.mkdir(parents=True, exist_ok=True)
    pdf = pdfcanvas.Canvas(str(EDITION), pagesize=portrait(TRIM_MM), pageCompression=1)
    pdf.setTitle("Neuromante - Capitolo 1 - Fumetto completo")
    pdf.setAuthor("Progetto Neuromante")
    pdf.setSubject("Adattamento italiano a fumetti - capitolo 1 completo")
    width, height = portrait(TRIM_MM)
    for path in [cover, *pages]:
        proxy = pdf_proxy(path)
        pdf.drawImage(str(proxy), 0, 0, width=width, height=height, preserveAspectRatio=False, mask="auto")
        pdf.showPage()
    pdf.save()


def main() -> None:
    PAGES.mkdir(parents=True, exist_ok=True)
    compose_page14_art()
    lettered = [letter_page(number) for number in range(1, 15)]
    cover = make_cover()
    build_pdf(cover, lettered)
    print(f"built {EDITION}")


if __name__ == "__main__":
    main()
