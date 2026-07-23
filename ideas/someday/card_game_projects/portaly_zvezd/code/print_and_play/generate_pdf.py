"""
Print-and-play генератор: CSV -> PDF, карты 63x88мм, сетка 3x3 на A4,
метки реза, отступ под bleed 3мм. Меняем CSV -> новый PDF за секунды.

Использование: python3 generate_pdf.py <путь_к_csv> <путь_к_pdf> [тип_карты]
тип_карты: portal | adventure  (влияет на то, какие поля показывать)
"""
import csv
import sys
import textwrap
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

CARD_W = 63 * mm
CARD_H = 88 * mm
BLEED = 3 * mm
COLS, ROWS = 3, 3

ELNAME = {"earth": "Земля", "water": "Вода", "fire": "Огонь", "star": "Звезда", "synth": "Синтез"}

ELEMENT_COLOR = {
    "earth": (0.85, 0.93, 0.80),
    "water": (0.82, 0.90, 0.97),
    "fire": (0.97, 0.86, 0.80),
    "star": (0.90, 0.85, 0.98),
    "synth": (0.98, 0.92, 0.78),
}


def wrap(text, width_chars):
    return textwrap.wrap(text, width=width_chars) if text else []


def cost_string(row):
    parts = []
    for el in ["earth", "water", "fire", "star", "synth"]:
        key = f"cost_{el}"
        if key in row and row[key] and int(row[key]) > 0:
            parts.append(f"{ELNAME[el]}x{row[key]}")
    return ", ".join(parts) if parts else "—"


def draw_crop_marks(c, x, y, w, h):
    m = BLEED
    ln = 3 * mm
    corners = [(x, y), (x + w, y), (x, y + h), (x + w, y + h)]
    for cx, cy in corners:
        sx = 1 if cx == x else -1
        sy = 1 if cy == y else -1
        c.setLineWidth(0.3)
        c.line(cx - sx * m, cy, cx - sx * (m + ln), cy)
        c.line(cx, cy - sy * m, cx, cy - sy * (m + ln))


def draw_card(c, x, y, row, card_type):
    element = row.get("element", "")
    color = ELEMENT_COLOR.get(element, (0.93, 0.93, 0.93))
    c.setFillColorRGB(*color)
    c.rect(x, y, CARD_W, CARD_H, fill=1, stroke=0)
    c.setStrokeColorRGB(0.2, 0.2, 0.2)
    c.setLineWidth(0.75)
    c.rect(x, y, CARD_W, CARD_H, fill=0, stroke=1)
    draw_crop_marks(c, x, y, CARD_W, CARD_H)

    pad = 3 * mm
    c.setFillColorRGB(0.1, 0.1, 0.1)
    c.setFont("Helvetica-Bold", 9)
    name = row.get("name", "")
    c.drawString(x + pad, y + CARD_H - pad - 8, name)

    c.setFont("Helvetica", 6.5)
    if card_type == "portal":
        tier = row.get("tier", "")
        vp = row.get("vp", "0")
        c.drawString(x + pad, y + CARD_H - pad - 18, f"Тир {tier} · {ELNAME.get(element,'')}")
        c.setFont("Helvetica-Bold", 11)
        c.drawRightString(x + CARD_W - pad, y + CARD_H - pad - 4, str(vp))
        c.setFont("Helvetica", 6.5)
        c.drawString(x + pad, y + CARD_H - pad - 28, "Цена: " + cost_string(row))
        effect = row.get("effect", "")
        if effect:
            for i, line in enumerate(wrap("Эффект: " + effect.replace("_", " "), 34)):
                c.drawString(x + pad, y + CARD_H - pad - 40 - i * 8, line)
    elif card_type == "adventure":
        safe_el = row.get("safe_element", "")
        c.drawString(x + pad, y + CARD_H - pad - 18, "Приключение")
        c.setFont("Helvetica", 6.5)
        c.drawString(x + pad, y + CARD_H - pad - 30, f"Надёжно: +1 {ELNAME.get(safe_el,'')}")
        c.drawString(x + pad, y + CARD_H - pad - 40, f"Риск: тяни из мешка (до {row.get('risk_draws_allowed','1')} раз)")

    flavor = row.get("flavor", "")
    if flavor:
        c.setFont("Helvetica-Oblique", 6)
        c.setFillColorRGB(0.35, 0.35, 0.35)
        lines = wrap(flavor, 36)
        for i, line in enumerate(lines[-3:]):
            c.drawString(x + pad, y + pad + (len(lines[-3:]) - i - 1) * 7, line)


def generate(csv_path, pdf_path, card_type="portal"):
    with open(csv_path, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    c = canvas.Canvas(str(pdf_path), pagesize=A4)
    page_w, page_h = A4
    margin_x = (page_w - COLS * CARD_W) / 2
    margin_y = (page_h - ROWS * CARD_H) / 2

    for i, row in enumerate(rows):
        pos = i % (COLS * ROWS)
        if pos == 0 and i != 0:
            c.showPage()
        col = pos % COLS
        grid_row = pos // COLS
        x = margin_x + col * CARD_W
        y = page_h - margin_y - (grid_row + 1) * CARD_H
        draw_card(c, x, y, row, card_type)

    c.save()
    return len(rows)


if __name__ == "__main__":
    csv_path = sys.argv[1] if len(sys.argv) > 1 else "portal_cards.csv"
    pdf_path = sys.argv[2] if len(sys.argv) > 2 else "output.pdf"
    card_type = sys.argv[3] if len(sys.argv) > 3 else "portal"
    n = generate(csv_path, pdf_path, card_type)
    print(f"Сгенерировано {n} карт -> {pdf_path}")
