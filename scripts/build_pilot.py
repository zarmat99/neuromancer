#!/usr/bin/env python3
"""Build lettered sample pages, editorial storyboards and the chapter-one pilot PDF."""

from __future__ import annotations

import html
import math
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import portrait
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Image as RLImage,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
PAGES = ROOT / "chapters" / "ch01" / "pages"
BOARDS = ROOT / "chapters" / "ch01" / "storyboard"
EDITION = ROOT / "editions" / "neuromante-pilota-capitolo-01.pdf"
PDF_TMP = ROOT / "tmp" / "pdfs"

FONT_REG = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
FONT_BOLD = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
FONT_MONO = Path("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf")

TRIM_PX = (2008, 3071)  # 170 x 260 mm at approximately 300 dpi
TRIM_MM = (170 * mm, 260 * mm)


def normalize(text: str) -> str:
    return (
        text.replace("\u2013", "-")
        .replace("\u2014", "-")
        .replace("\u2011", "-")
        .replace("\u00a0", " ")
    )


def font(path: Path, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(path), size=size)


def wrap_for_pixels(draw: ImageDraw.ImageDraw, text: str, face, width: int) -> list[str]:
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


def fit_font(draw, text: str, width: int, height: int, bold: bool = False, start: int = 42):
    path = FONT_BOLD if bold else FONT_REG
    for size in range(start, 19, -1):
        face = font(path, size)
        lines = wrap_for_pixels(draw, text, face, width)
        line_h = int(size * 1.18)
        if len(lines) * line_h <= height:
            return face, lines, line_h
    face = font(path, 19)
    return face, wrap_for_pixels(draw, text, face, width), 23


def rounded_box(draw, rect, fill, outline, radius=28, stroke=5):
    draw.rounded_rectangle(rect, radius=radius, fill=fill, outline=outline, width=stroke)


def add_text_box(draw, rect, text: str, kind: str = "balloon", tail=None):
    x, y, w, h = rect
    if kind == "caption":
        fill = (10, 14, 18, 236)
        outline = (220, 235, 238, 255)
        ink = (244, 246, 240, 255)
        bold = False
        radius = 8
    elif kind == "cartiglio":
        fill = (25, 204, 207, 245)
        outline = (4, 24, 26, 255)
        ink = (4, 20, 22, 255)
        bold = True
        radius = 8
    elif kind == "sfx":
        face = font(FONT_BOLD, max(28, int(h * 0.58)))
        draw.text(
            (x + w / 2, y + h / 2),
            normalize(text),
            font=face,
            anchor="mm",
            fill=(245, 244, 230, 255),
            stroke_width=5,
            stroke_fill=(0, 0, 0, 255),
        )
        return
    else:
        fill = (249, 247, 235, 248)
        outline = (8, 10, 12, 255)
        ink = (10, 12, 14, 255)
        bold = False
        radius = min(40, h // 2)

    if kind == "balloon" and tail is not None:
        tx, ty = tail
        cx, cy = x + w / 2, y + h / 2
        if abs(tx - cx) > abs(ty - cy):
            bx = x if tx < cx else x + w
            by = max(y + 18, min(y + h - 18, ty))
            base = [(bx, by - 15), (bx, by + 15)]
        else:
            by = y if ty < cy else y + h
            bx = max(x + 18, min(x + w - 18, tx))
            base = [(bx - 15, by), (bx + 15, by)]
        draw.polygon([base[0], (tx, ty), base[1]], fill=fill)
        draw.line([base[0], (tx, ty), base[1]], fill=outline, width=5, joint="curve")

    rounded_box(draw, (x, y, x + w, y + h), fill, outline, radius=radius, stroke=5)
    pad_x, pad_y = 18, 12
    face, lines, line_h = fit_font(draw, text, w - 2 * pad_x, h - 2 * pad_y, bold=bold)
    total = len(lines) * line_h
    yy = y + (h - total) / 2
    for line in lines:
        tw = draw.textbbox((0, 0), line, font=face)[2]
        draw.text((x + (w - tw) / 2, yy), line, font=face, fill=ink)
        yy += line_h


def letter_page(src_name: str, out_name: str, boxes, page_no: int):
    src = Image.open(PAGES / src_name).convert("RGB")
    canvas = Image.new("RGB", TRIM_PX, (8, 10, 12))
    scale = TRIM_PX[1] / src.height
    art_w = int(round(src.width * scale))
    art = src.resize((art_w, TRIM_PX[1]), Image.Resampling.LANCZOS)
    x0 = (TRIM_PX[0] - art_w) // 2
    canvas.paste(art, (x0, 0))

    # Subtle vertical rails compensate for the generated page's extra-tall ratio.
    d = ImageDraw.Draw(canvas, "RGBA")
    d.rectangle((0, 0, x0, TRIM_PX[1]), fill=(8, 10, 12, 255))
    d.rectangle((x0 + art_w, 0, TRIM_PX[0], TRIM_PX[1]), fill=(8, 10, 12, 255))
    d.line((x0 - 4, 0, x0 - 4, TRIM_PX[1]), fill=(32, 205, 207, 210), width=3)
    d.line((x0 + art_w + 3, 0, x0 + art_w + 3, TRIM_PX[1]), fill=(157, 30, 55, 190), width=3)

    for entry in boxes:
        kind, (x, y, w, h), text = entry[:3]
        tail = entry[3] if len(entry) > 3 else None
        rect = (
            x0 + int(x * scale),
            int(y * scale),
            int(w * scale),
            int(h * scale),
        )
        scaled_tail = None
        if tail is not None:
            scaled_tail = (x0 + int(tail[0] * scale), int(tail[1] * scale))
        add_text_box(d, rect, normalize(text), kind, scaled_tail)

    pn = font(FONT_MONO, 28)
    d.text((TRIM_PX[0] - 55, TRIM_PX[1] - 42), f"{page_no:02}", font=pn, anchor="mm", fill=(210, 215, 210))
    canvas.save(PAGES / out_name, quality=95)


def crop_to_fill(src: Image.Image, size: tuple[int, int], crop=None) -> Image.Image:
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


def contain(src: Image.Image, size: tuple[int, int], background=(4, 6, 8)) -> Image.Image:
    target_w, target_h = size
    scale = min(target_w / src.width, target_h / src.height)
    resized = src.resize(
        (int(round(src.width * scale)), int(round(src.height * scale))),
        Image.Resampling.LANCZOS,
    )
    out = Image.new("RGB", size, background)
    out.paste(resized, ((target_w - resized.width) // 2, (target_h - resized.height) // 2))
    return out


def make_page14_art_v2() -> Path:
    """Compose page 14 from one spatial master so geometry cannot drift."""
    master = Image.open(ROOT / "assets" / "environments" / "capsule-92-scene-master-v2.png").convert("RGB")
    holster = Image.open(ROOT / "assets" / "environments" / "capsule-92-holster-v2.png").convert("RGB")
    old_page = Image.open(PAGES / "page-14-art-v1.png").convert("RGB")

    page = Image.new("RGB", TRIM_PX, (4, 6, 8))
    d = ImageDraw.Draw(page)
    margin, gutter = 20, 18
    inner_w = TRIM_PX[0] - 2 * margin

    # The black upper strips in panels A-C are reserved lettering zones. They
    # are part of the layout, not overlays found after the illustration exists.
    panels = [
        ((margin, 165, inner_w, 655), crop_to_fill(master, (inner_w, 655), (0, 110, 1536, 620))),
        ((margin, 1025, 975, 423), crop_to_fill(master, (975, 423), (0, 180, 900, 570))),
        ((margin + 975 + gutter, 1025, 975, 423), crop_to_fill(master, (975, 423), (560, 170, 1536, 593))),
        ((margin, 1466, inner_w, 500), crop_to_fill(holster, (inner_w, 500), (0, 140, 1536, 540))),
    ]

    final_crop = old_page.crop((0, 1050, old_page.width, old_page.height))
    panels.append(((margin, 1984, inner_w, 1067), contain(final_crop, (inner_w, 1067))))

    for (x, y, w, h), artwork in panels:
        page.paste(artwork, (x, y))
        d.rectangle((x, y, x + w - 1, y + h - 1), outline=(2, 3, 4), width=8)

    # Outline the complete A-C panels, including their protected text strips.
    for x, y, w, h in [
        (margin, 20, inner_w, 800),
        (margin, 838, 975, 610),
        (margin + 975 + gutter, 838, 975, 610),
    ]:
        d.rectangle((x, y, x + w - 1, y + h - 1), outline=(2, 3, 4), width=8)

    out = PAGES / "page-14-art-v2.png"
    page.save(out, quality=96)
    return out


LETTERING = {
    1: [
        ("caption", (20, 24, 370, 78), "Il cielo sopra il porto aveva il colore di un televisore sintonizzato su un canale morto."),
        ("cartiglio", (635, 28, 200, 44), "CHIBA CITY - 22:30"),
        ("balloon", (24, 350, 255, 76), "Non mi sto facendo. È il corpo che va in crisi da solo."),
        ("balloon", (650, 950, 185, 62), "Guarda chi arriva: l'artista.", (625, 1060)),
        ("balloon", (610, 1265, 225, 66), "Il virtuoso dell'affare storto.", (600, 1380)),
        ("balloon", (22, 1680, 250, 74), "Qualcuno dovrà pur tenerti allegro.", (330, 1645)),
        ("balloon", (420, 1660, 250, 82), "Wage è passato presto. Con due Joeboy.", (690, 1625)),
        ("balloon", (682, 1700, 150, 62), "Ti cercava?", (720, 1635)),
    ],
    10: [
        ("sfx", (625, 170, 185, 54), "TOK... TOK..."),
        ("caption", (25, 305, 260, 94), "Quella non era paranoia da dex. Era paura vera."),
        ("sfx", (650, 608, 175, 52), "KLIK-KLIK"),
        ("sfx", (650, 1020, 175, 60), "KRASH"),
        ("sfx", (650, 1330, 145, 55), "THUD"),
        ("balloon", (90, 1245, 145, 62), "Ngh--", (310, 1320)),
        ("balloon", (610, 1515, 175, 70), "Merda.", (650, 1470)),
    ],
    14: [
        ("balloon", (1030, 42, 360, 76), "Piano col portello.", (1510, 260)),
        ("balloon", (1410, 42, 540, 84), "Hai ancora la pistola di Shin?", (1580, 300)),
        ("balloon", (55, 858, 335, 72), "L'ho restituita.", (470, 1080)),
        ("balloon", (410, 858, 470, 72), "Eri tu, all'arcade?", (500, 1090)),
        ("balloon", (1040, 852, 410, 76), "Perché ti sei buttato?", (1660, 1080)),
        ("balloon", (1470, 852, 490, 86), "Linda ha detto che Wage voleva uccidermi.", (1015, 1010)),
        ("balloon", (1120, 935, 720, 76), "Linda? L'ho vista solo qui. È scappata col tuo Hitachi.", (1680, 1100)),
        ("balloon", (350, 1490, 500, 76), "Quindi non lavori per Wage.", (315, 1740)),
        ("balloon", (880, 1490, 330, 76), "No. Sono Molly.", (1260, 1660)),
        ("balloon", (330, 1600, 720, 92), "Il mio capo vuole parlarti. Ti vuole vivo.", (1260, 1710)),
        ("balloon", (550, 1720, 300, 68), "Che premura.", (315, 1800)),
        ("balloon", (45, 2070, 330, 118), "Ogni tanto faccio male alla gente.", (395, 2380)),
        ("balloon", (1628, 2110, 330, 108), "Sarà un difetto di fabbrica.", (1610, 2380)),
        ("sfx", (1650, 2880, 230, 78), "SNIK"),
    ],
}


BOARD_DATA = [
    ("Il cielo morto", ["Porto e cielo grigio", "Case nella folla", "Porta del Chat", "Ratz", "Protesi e birra", "Wage nominato"]),
    ("La caduta", ["Sarcasmo di Case", "Avvertimento di Ratz", "Matrice", "Punizione a Memphis", "Corpo-cella"]),
    ("Night City", ["Ninsei", "Capsule del porto", "Pillola rosa", "Jarre de Thé", "Iperfocus", "Linda appare"]),
    ("Linda", ["Primo incontro", "Harajuku", "Capsula condivisa", "Dipendenza", "Presente al Jarre", "Minaccia di Wage"]),
    ("Cinquanta", ["Case dubita", "Linda trema", "Banconota", "Tasca chiusa", "Occhi nel neon"]),
    ("Stelle di cromo", ["Folla come dati", "Innesto aziendale", "Shuriken", "Anticamera", "Deane", "Dubbio finale"]),
    ("La coda", ["Vetrina chirurgica", "Riflesso argento", "Case scatta", "Shin rifiuta", "Cobra"]),
    ("Campo di dati", ["Cobra nascosto", "Chat affollato", "Zone", "Coda riflessa", "Corsa all'arcade"]),
    ("La trappola", ["Ologramma", "Scale", "Sicurezza", "Prima porta", "Finestra", "Attesa col cobra"]),
    ("Paura reale", ["Passi", "Occhio", "Cobra chiuso", "Salto", "Impatto", "Molly alla finestra"]),
    ("Numero 92", ["Pistola di Shin", "Seconda dex", "Cheap Hotel", "Capsula", "Chiamata muta"]),
    ("Wage", ["Snake Man", "Linea morta", "Armi in tasca", "Chat vuoto", "Wage entra"]),
    ("Debito", ["Stallo", "Pistola scaricata", "Wage nega", "Fiasca ceduta", "Alba e arma resa", "Visita di Linda"]),
    ("Molly", ["Master shot fisso", "Arma già resa", "Errore su Linda", "Molly ripone la fletcher", "Dieci lame"]),
]


def layout_for(count: int):
    # Normalized within the board's drawing area.
    presets = {
        4: [(0.04, 0.05, 0.92, 0.27), (0.04, 0.35, 0.44, 0.25), (0.52, 0.35, 0.44, 0.25), (0.04, 0.63, 0.92, 0.32)],
        5: [(0.04, 0.05, 0.44, 0.24), (0.52, 0.05, 0.44, 0.24), (0.04, 0.32, 0.92, 0.25), (0.04, 0.60, 0.44, 0.35), (0.52, 0.60, 0.44, 0.35)],
        6: [(0.04, 0.05, 0.92, 0.25), (0.04, 0.33, 0.28, 0.25), (0.36, 0.33, 0.28, 0.25), (0.68, 0.33, 0.28, 0.25), (0.04, 0.61, 0.44, 0.34), (0.52, 0.61, 0.44, 0.34)],
    }
    return presets[count]


def make_storyboards():
    BOARDS.mkdir(parents=True, exist_ok=True)
    for page_no, (title, beats) in enumerate(BOARD_DATA, 1):
        canvas = Image.new("RGB", (1200, 1800), (236, 233, 220))
        d = ImageDraw.Draw(canvas)
        d.rectangle((0, 0, 1200, 150), fill=(10, 15, 19))
        d.text((55, 42), f"TAVOLA {page_no:02}", font=font(FONT_MONO, 34), fill=(48, 216, 215))
        d.text((320, 36), title.upper(), font=font(FONT_BOLD, 52), fill=(245, 242, 225))
        area = (35, 175, 1130, 1510)
        palette = [(51, 65, 70), (75, 76, 72), (48, 77, 82), (80, 60, 65), (60, 70, 62), (55, 61, 78)]
        for idx, (norm, beat) in enumerate(zip(layout_for(len(beats)), beats), 1):
            nx, ny, nw, nh = norm
            x = int(area[0] + nx * area[2])
            y = int(area[1] + ny * area[3])
            w = int(nw * area[2])
            h = int(nh * area[3])
            d.rectangle((x, y, x + w, y + h), fill=palette[(idx - 1) % len(palette)], outline=(8, 12, 14), width=8)
            d.text((x + 18, y + 14), f"{page_no}.{idx}", font=font(FONT_MONO, 28), fill=(48, 216, 215))
            face, lines, lh = fit_font(d, beat, w - 50, h - 90, bold=True, start=38)
            total = len(lines) * lh
            yy = y + (h - total) / 2
            for line in lines:
                tw = d.textbbox((0, 0), line, font=face)[2]
                d.text((x + (w - tw) / 2, yy), line, font=face, fill=(245, 242, 225))
                yy += lh
        d.line((55, 1715, 1145, 1715), fill=(18, 28, 32), width=3)
        d.text((55, 1730), "STORYBOARD EDITORIALE - CONTINUITÀ BLOCCATA v0.2", font=font(FONT_MONO, 22), fill=(20, 30, 34))
        canvas.save(BOARDS / f"page-{page_no:02}-board.png")


def make_cover():
    out = ROOT / "editions" / "cover-pilot.png"
    img = Image.new("RGB", TRIM_PX, (5, 8, 11))
    d = ImageDraw.Draw(img)
    # Abstract matrix lattice, drawn deterministically.
    for i in range(18):
        x = 90 + i * 108
        d.line((x, 0, x - 320, TRIM_PX[1]), fill=(8, 65 + i * 2, 72), width=3)
    for j in range(23):
        y = 340 + j * 108
        d.line((0, y, TRIM_PX[0], y - 260), fill=(72, 10, 40), width=2)
    d.rectangle((145, 410, 1865, 2530), outline=(42, 220, 216), width=8)
    d.rectangle((190, 455, 1820, 2485), outline=(155, 30, 72), width=3)
    d.text((170, 690), "NEUROMANTE", font=font(FONT_BOLD, 185), fill=(241, 238, 220))
    d.text((180, 930), "CAPITOLO 1", font=font(FONT_MONO, 78), fill=(52, 218, 216))
    d.text((180, 1060), "PILOTA A FUMETTI", font=font(FONT_BOLD, 80), fill=(194, 40, 84))
    d.line((180, 1240, 1530, 1240), fill=(240, 238, 220), width=5)
    d.text((180, 1310), "14 TAVOLE", font=font(FONT_MONO, 44), fill=(235, 232, 215))
    d.text((180, 1385), "77 VIGNETTE", font=font(FONT_MONO, 44), fill=(235, 232, 215))
    d.text((180, 1460), "3 TAVOLE CAMPIONE FINITE", font=font(FONT_MONO, 44), fill=(235, 232, 215))
    d.text((180, 2270), "BIBBIA COMPLETA DEL CAPITOLO 1", font=font(FONT_MONO, 34), fill=(170, 177, 172))
    d.text((180, 2340), "VERSIONE 0.2", font=font(FONT_MONO, 34), fill=(170, 177, 172))
    img.save(out)
    return out


def pdf_proxy(path: Path, quality: int = 90) -> Path:
    """Create a visually lossless-enough JPEG proxy for compact PDF embedding."""
    PDF_TMP.mkdir(parents=True, exist_ok=True)
    out = PDF_TMP / f"{path.stem}-q{quality}.jpg"
    src_mtime = path.stat().st_mtime
    if not out.exists() or out.stat().st_mtime < src_mtime:
        im = Image.open(path).convert("RGB")
        im.save(out, "JPEG", quality=quality, optimize=True, progressive=True, subsampling=0)
    return out


def rl_fit(path: Path, max_width=146 * mm, max_height=180 * mm, quality: int = 91):
    with Image.open(path) as im:
        ratio = im.width / im.height
    width = min(max_width, max_height * ratio)
    height = width / ratio
    if height > max_height:
        height = max_height
        width = height * ratio
    return RLImage(str(pdf_proxy(path, quality)), width=width, height=height)


def safe_para(text: str) -> str:
    text = normalize(text.strip())
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"`(.+?)`", r"<font name='DVMono'>\1</font>", text)
    return html.escape(text, quote=False).replace("&lt;b&gt;", "<b>").replace("&lt;/b&gt;", "</b>").replace("&lt;font name='DVMono'&gt;", "<font name='DVMono'>").replace("&lt;/font&gt;", "</font>")


def add_markdown_story(story, path: Path, styles):
    pending: list[str] = []
    table_pending: list[str] = []

    def flush():
        nonlocal pending
        if pending:
            story.append(Paragraph(safe_para(" ".join(pending)), styles["BodyPilot"]))
            story.append(Spacer(1, 2.2 * mm))
            pending = []

    def flush_table():
        nonlocal table_pending
        if not table_pending:
            return
        raw_rows = []
        for raw in table_pending:
            cells = [cell.strip() for cell in raw.strip().strip("|").split("|")]
            if cells and all(re.fullmatch(r":?-{3,}:?", cell.replace(" ", "")) for cell in cells):
                continue
            raw_rows.append(cells)
        table_pending = []
        if not raw_rows:
            return
        cols = max(len(row) for row in raw_rows)
        rows = []
        for ridx, row in enumerate(raw_rows):
            row = row + [""] * (cols - len(row))
            style = styles["TableHead"] if ridx == 0 else styles["TableBody"]
            rows.append([Paragraph(safe_para(cell), style) for cell in row])
        tbl = Table(rows, colWidths=[146 * mm / cols] * cols, repeatRows=1, hAlign="LEFT")
        tbl.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#d7eeee")),
            ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#172025")),
            ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#8b999c")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 3),
            ("RIGHTPADDING", (0, 0), (-1, -1), 3),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ]))
        story.append(tbl)
        story.append(Spacer(1, 2.5 * mm))

    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line.startswith("|"):
            flush()
            table_pending.append(line)
            continue
        flush_table()
        if line.startswith("## "):
            flush()
            if line.startswith("## TAVOLA") and story and not isinstance(story[-1], PageBreak):
                story.append(PageBreak())
            story.append(Paragraph(safe_para(line[3:]), styles["H1Pilot"]))
        elif line.startswith("#### "):
            flush()
            story.append(Paragraph(safe_para(line[5:]), styles["H3Pilot"]))
        elif line.startswith("### "):
            flush()
            story.append(Paragraph(safe_para(line[4:]), styles["H2Pilot"]))
        elif line.startswith("# "):
            flush()
            story.append(Paragraph(safe_para(line[2:]), styles["TitlePilot"]))
        elif line == "---":
            flush()
        elif line.startswith("-"):
            flush()
            story.append(Paragraph(safe_para(line[1:].strip()), styles["BulletPilot"], bulletText="•"))
        elif not line:
            flush()
        else:
            pending.append(line)
    flush()
    flush_table()


def build_pdf(cover_path: Path):
    pdfmetrics.registerFont(TTFont("DV", str(FONT_REG)))
    pdfmetrics.registerFont(TTFont("DVBold", str(FONT_BOLD)))
    pdfmetrics.registerFont(TTFont("DVMono", str(FONT_MONO)))

    doc = SimpleDocTemplate(
        str(EDITION),
        pagesize=portrait(TRIM_MM),
        leftMargin=12 * mm,
        rightMargin=12 * mm,
        topMargin=12 * mm,
        bottomMargin=12 * mm,
        title="Neuromante - Pilota a fumetti - Capitolo 1",
        author="Progetto Neuromante",
        subject="Bibbia completa del capitolo, storyboard, tavole campione e sceneggiatura tecnica",
    )
    ss = getSampleStyleSheet()
    styles = {
        "TitlePilot": ParagraphStyle("TitlePilot", parent=ss["Title"], fontName="DVBold", fontSize=24, leading=28, textColor=colors.HexColor("#10191d"), spaceAfter=8 * mm),
        "H1Pilot": ParagraphStyle("H1Pilot", parent=ss["Heading1"], fontName="DVBold", fontSize=17, leading=21, textColor=colors.HexColor("#0e6f75"), spaceAfter=5 * mm),
        "H2Pilot": ParagraphStyle("H2Pilot", parent=ss["Heading2"], fontName="DVBold", fontSize=10.5, leading=12.6, textColor=colors.HexColor("#9b2348"), spaceBefore=1.2 * mm, spaceAfter=1.3 * mm),
        "H3Pilot": ParagraphStyle("H3Pilot", parent=ss["Heading3"], fontName="DVBold", fontSize=8.8, leading=10.6, textColor=colors.HexColor("#253b42"), spaceBefore=1.1 * mm, spaceAfter=1.1 * mm),
        "BodyPilot": ParagraphStyle("BodyPilot", parent=ss["BodyText"], fontName="DV", fontSize=7.8, leading=10.1, textColor=colors.HexColor("#172025"), alignment=TA_LEFT),
        "BulletPilot": ParagraphStyle("BulletPilot", parent=ss["BodyText"], fontName="DV", fontSize=7.7, leading=9.9, leftIndent=5 * mm, firstLineIndent=-3 * mm, textColor=colors.HexColor("#172025"), spaceAfter=0.8 * mm),
        "Small": ParagraphStyle("Small", parent=ss["BodyText"], fontName="DVMono", fontSize=7, leading=9, textColor=colors.HexColor("#4b5a60")),
        "Center": ParagraphStyle("Center", parent=ss["BodyText"], fontName="DV", fontSize=8, leading=10, alignment=TA_CENTER, textColor=colors.HexColor("#24343a")),
        "TableHead": ParagraphStyle("TableHead", parent=ss["BodyText"], fontName="DVBold", fontSize=6.2, leading=7.5, textColor=colors.HexColor("#172025")),
        "TableBody": ParagraphStyle("TableBody", parent=ss["BodyText"], fontName="DV", fontSize=5.8, leading=7.1, textColor=colors.HexColor("#172025")),
    }

    story = []
    story.append(RLImage(str(pdf_proxy(cover_path, 94)), width=146 * mm, height=223.06 * mm))
    story.append(PageBreak())
    story.append(Paragraph("Pacchetto pilota", styles["TitlePilot"]))
    story.append(Paragraph(
        "Adattamento del capitolo 1, pagine PDF 3-29. Il pilota definisce la grammatica narrativa e visiva prima della produzione seriale, con un registro di continuità obbligatorio per personaggi, luoghi, oggetti, luce e danni fisici.",
        styles["BodyPilot"],
    ))
    story.append(Spacer(1, 6 * mm))
    data = [
        ["Formato", "170 x 260 mm, colore"],
        ["Sceneggiatura", "14 tavole / 77 vignette"],
        ["Tavole finite", "1, 10 e 14 — lettering v0.2"],
        ["Arco temporale", "Venerdì notte - sabato all'alba"],
        ["Continuità", "Bibbia incrementale completa del capitolo 1"],
        ["Lettering", "Italiano riscritto per intenzione; aree sicure"],
    ]
    table = Table(data, colWidths=[42 * mm, 96 * mm])
    table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "DV"),
        ("FONTNAME", (0, 0), (0, -1), "DVBold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#172025")),
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#d7eeee")),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#829397")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(table)
    story.append(Spacer(1, 8 * mm))
    story.append(Paragraph("Metodo di coerenza", styles["H1Pilot"]))
    for item in [
        "Una reference definitiva per ogni identità visibile prima delle scene.",
        "Outfit e oggetti tracciati tavola per tavola.",
        "Geometria e asse di ripresa bloccati per ogni ambiente ricorrente.",
        "Dialoghi riscritti per intenzione e voce, non tradotti parola per parola.",
        "Nessun testo generato nell'arte: balloon e didascalie usano zone riservate.",
        "Ogni immagine viene confrontata con bible/continuity-ledger.md.",
    ]:
        story.append(Paragraph(item, styles["BulletPilot"], bulletText="•"))

    story.append(PageBreak())
    add_markdown_story(story, ROOT / "bible" / "ch01-production-bible.md", styles)
    story.append(PageBreak())
    add_markdown_story(story, ROOT / "bible" / "ch01-reference-index.md", styles)

    refs = [
        ("CHAR_CASE_V1 - Case", ROOT / "assets" / "characters" / "case-v1.png"),
        ("CHAR_MOLLY_V1 - Molly", ROOT / "assets" / "characters" / "molly-v1.png"),
        ("Cast di supporto - Linda, Ratz, Wage", ROOT / "assets" / "characters" / "supporting-cast-v1.png"),
        ("Cast secondario A - Deane, Zone, Shin, Kurt", ROOT / "assets" / "characters" / "ch01-supporting-a-v2.png"),
        ("Cast secondario B - comparse funzionali", ROOT / "assets" / "characters" / "ch01-supporting-b-v2.png"),
        ("Ambienti primari - Chat, Ninsei, arcade, Cheap Hotel", ROOT / "assets" / "environments" / "ch01-locations-v1.png"),
        ("Ambienti secondari - Jarre, Deane, Shiga, armeria", ROOT / "assets" / "environments" / "ch01-locations-secondary-v2.png"),
        ("Ambienti di raccordo e flashback", ROOT / "assets" / "environments" / "ch01-locations-flashbacks-v2.png"),
        ("LOC_COFFIN_92_V2 - pianta e sezione", ROOT / "assets" / "environments" / "capsule-92-layout-v2.png"),
        ("LOC_COFFIN_92_V2 - master shot", ROOT / "assets" / "environments" / "capsule-92-scene-master-v2.png"),
        ("LOC_COFFIN_92_V2 - Molly ripone la fletcher", ROOT / "assets" / "environments" / "capsule-92-holster-v2.png"),
    ]
    for title, path in refs:
        story.append(PageBreak())
        story.append(Paragraph(title, styles["H1Pilot"]))
        story.append(Spacer(1, 3 * mm))
        story.append(rl_fit(path, max_width=146 * mm, max_height=178 * mm, quality=91))
        story.append(Spacer(1, 5 * mm))
        story.append(Paragraph(
            "Reference vincolante. Possono cambiare inquadratura e illuminazione, non identità, proporzioni, outfit, landmark o geometria stabilita.",
            styles["Center"],
        ))

    story.append(PageBreak())
    story.append(Paragraph("Storyboard completo", styles["TitlePilot"]))
    story.append(Paragraph(
        "Le quattordici pagine seguenti bloccano numero, ordine, funzione e geometria delle vignette. Sono una mappa editoriale: le descrizioni complete e il lettering sono nell'appendice di sceneggiatura.",
        styles["BodyPilot"],
    ))
    for page_no in range(1, 15):
        story.append(PageBreak())
        board = BOARDS / f"page-{page_no:02}-board.png"
        story.append(RLImage(str(pdf_proxy(board, 94)), width=146 * mm, height=219 * mm))

    story.append(PageBreak())
    story.append(Paragraph("Tavole campione finite", styles["TitlePilot"]))
    story.append(Paragraph(
        "Apertura, sequenza d'azione e cliffhanger verificano tre difficoltà differenti: atmosfera e dialogo, continuità fisica in movimento, identità di Molly e leggibilità delle mani.",
        styles["BodyPilot"],
    ))
    for no in (1, 10, 14):
        story.append(PageBreak())
        p = PAGES / f"page-{no:02}-lettered-v2.png"
        story.append(RLImage(str(pdf_proxy(p, 91)), width=146 * mm, height=223.06 * mm))

    story.append(PageBreak())
    add_markdown_story(story, ROOT / "bible" / "ch01-dialogue-pass.md", styles)

    story.append(PageBreak())
    story.append(Paragraph("Sceneggiatura tecnica integrale", styles["TitlePilot"]))
    story.append(Paragraph(
        "Il testo seguente specifica azione, regia, dialoghi, didascalie, suoni e vincoli di continuità per tutte le 77 vignette.",
        styles["BodyPilot"],
    ))
    add_markdown_story(story, ROOT / "chapters" / "ch01" / "script.md", styles)

    def footer(canvas, doc_obj):
        canvas.saveState()
        canvas.setFont("DVMono", 6.5)
        canvas.setFillColor(colors.HexColor("#6a777b"))
        canvas.drawString(12 * mm, 6.5 * mm, "NEUROMANTE - PILOTA CAPITOLO 1 - v0.2")
        canvas.drawRightString(158 * mm, 6.5 * mm, f"{doc_obj.page}")
        canvas.restoreState()

    doc.build(story, onFirstPage=footer, onLaterPages=footer)


def main():
    PAGES.mkdir(parents=True, exist_ok=True)
    ROOT.joinpath("editions").mkdir(parents=True, exist_ok=True)
    make_page14_art_v2()
    for no in (1, 10):
        letter_page(f"page-{no:02}-art-v1.png", f"page-{no:02}-lettered-v2.png", LETTERING[no], no)
    letter_page("page-14-art-v2.png", "page-14-lettered-v2.png", LETTERING[14], 14)
    make_storyboards()
    cover = make_cover()
    build_pdf(cover)
    print(f"built {EDITION}")


if __name__ == "__main__":
    main()
