#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
render_mockups.py — рендерер GUI-мокапов из SysML v2-модели в PNG.

Идея лабораторной работы №3: прототипы интерфейса описываются на языке SysML v2
(пакеты `Larets::UI` и `Larets::UI::Mockups`), а PNG-изображения получаются
автоматической отрисовкой этой модели. Модель — единственный источник истины:
координаты, подписи и состояния элементов хранятся в .sysml-файле.

Использование:
    python3 render_mockups.py                 # все экраны из ui-mockups.sysml
    python3 render_mockups.py --out .           # каталог для PNG (по умолчанию — рядом с моделями)
    python3 render_mockups.py --only UnlockScreen

Зависимости: Python 3.10+, Pillow, шрифты DejaVu (пакет fonts-dejavu-core).
"""

from __future__ import annotations

import argparse
import hashlib
import math
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:  # pragma: no cover
    sys.exit("Требуется Pillow: pip install pillow")

HERE = Path(__file__).resolve().parent

FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
FONT_MONO_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

SCALE = 2  # рендер с удвоением и последующим уменьшением — сглаживание текста

# ----------------------------------------------------------------------------
# Палитра
# ----------------------------------------------------------------------------
PALETTE = {
    "bg": "#EEF1F7",
    "surface": "#FFFFFF",
    "surface-alt": "#F7F9FC",
    "dark": "#1F2A44",
    "dark-alt": "#273353",
    "dark-text": "#FFFFFF",
    "dark-muted": "#A9B4CC",
    "sidebar-text": "#C9D3E8",
    "text": "#1B2333",
    "muted": "#6B7488",
    "faint": "#98A1B3",
    "border": "#D5DBE6",
    "border-soft": "#E8ECF3",
    "primary": "#2F5BEA",
    "primary-dark": "#1E3FA8",
    "primary-soft": "#E8EEFF",
    "success": "#2AA876",
    "warn": "#E39A1D",
    "danger": "#D9534F",
    "white": "#FFFFFF",
    "transparent": None,
}


def color(value: str | None, default: str = "#000000") -> str | None:
    if value is None:
        return default
    if value.startswith("#"):
        return value
    return PALETTE.get(value, default)


# ----------------------------------------------------------------------------
# Парсер SysML v2 (подмножество, нужное для мокапов)
# ----------------------------------------------------------------------------
@dataclass
class Node:
    """Элемент модели: определение (part def) или экземпляр (part)."""

    kind: str                    # "def" | "instance"
    name: str
    type: str | None = None
    attrs: dict[str, object] = field(default_factory=dict)
    parts: list["Node"] = field(default_factory=list)


ATTR_RE = re.compile(r"^attribute\s+([A-Za-z_]\w*)\s*(?::\s*[\w:\[\]<>]+)?\s*=\s*(.+?);?$")
PART_DEF_RE = re.compile(r"^(?:abstract\s+)?part\s+def\s+([A-Za-z_]\w*)\b")
PART_RE = re.compile(r"^part\s+([A-Za-z_]\w*)\s*:\s*([A-Za-z_]\w*)\b")


def strip_comment(line: str) -> str:
    """Удаляет // комментарий, не затрагивая содержимое строковых литералов."""
    out: list[str] = []
    in_str = False
    i = 0
    while i < len(line):
        ch = line[i]
        if ch == '"':
            in_str = not in_str
            out.append(ch)
        elif not in_str and line.startswith("//", i):
            break
        else:
            out.append(ch)
        i += 1
    return "".join(out).strip()


def split_statements(line: str) -> list[str]:
    """Разбивает строку на несколько `attribute ...;` вне строковых литералов."""
    parts, current = [], []
    in_str = False
    for ch in line:
        if ch == '"':
            in_str = not in_str
        if ch == ";" and not in_str:
            parts.append("".join(current))
            current = []
        else:
            current.append(ch)
    if "".join(current).strip():
        parts.append("".join(current))
    return [p for p in parts if p.strip()]


def parse_value(raw: str):
    raw = raw.strip().rstrip(";").strip()
    if raw.startswith('"') and raw.endswith('"'):
        return raw[1:-1].replace("\\n", "\n").replace('\\"', '"')
    if raw in ("true", "false"):
        return raw == "true"
    try:
        number = float(raw)
        return int(number) if number == int(number) else number
    except ValueError:
        return raw


def parse_sysml(text: str) -> list[Node]:
    """Возвращает плоский список определений верхнего уровня."""
    defs: list[Node] = []
    stack: list[Node | None] = []
    for raw in text.splitlines():
        line = strip_comment(raw)
        if not line:
            continue
        if line.startswith(("package ", "private import", "import ", "public import")):
            continue
        if line in ("}", "};"):
            if stack:
                stack.pop()
            continue
        m = PART_DEF_RE.match(line)
        if m:
            node = Node("def", m.group(1))
            (stack[-1].parts if stack and stack[-1] else defs).append(node)
            if "{" in line:
                stack.append(node)
            continue
        m = PART_RE.match(line)
        if m:
            node = Node("instance", m.group(1), m.group(2))
            if stack:
                stack[-1].parts.append(node)
            if "{" in line:
                stack.append(node)
            continue
        if line.startswith("attribute") and stack and stack[-1] is not None:
            for statement in split_statements(line):
                m = ATTR_RE.match(statement.strip())
                if m:
                    stack[-1].attrs[m.group(1)] = parse_value(m.group(2))
            continue
    return defs


# ----------------------------------------------------------------------------
# Отрисовка
# ----------------------------------------------------------------------------
class Painter:
    def __init__(self, width: int, height: int):
        self.w, self.h = width, height
        self.img = Image.new("RGB", (width * SCALE, height * SCALE), color("bg"))
        self.d = ImageDraw.Draw(self.img)
        self._fonts: dict[tuple[int, str], ImageFont.FreeTypeFont] = {}

    # -- утилиты ------------------------------------------------------------
    def s(self, value: float) -> int:
        return int(round(value * SCALE))

    def font(self, size: int = 14, style: str = "regular") -> ImageFont.FreeTypeFont:
        key = (size, style)
        if key not in self._fonts:
            path = {
                "regular": FONT_REG,
                "bold": FONT_BOLD,
                "mono": FONT_MONO,
                "mono-bold": FONT_MONO_BOLD,
            }[style]
            self._fonts[key] = ImageFont.truetype(path, self.s(size))
        return self._fonts[key]

    def rect(self, x, y, w, h, r=0, fill=None, outline=None, width=1):
        if w <= 0 or h <= 0:
            return
        self.d.rounded_rectangle(
            [self.s(x), self.s(y), self.s(x + w), self.s(y + h)],
            radius=self.s(r),
            fill=fill,
            outline=outline,
            width=max(1, self.s(width)) if outline else 0,
        )

    def line(self, x1, y1, x2, y2, fill="#D5DBE6", width=1):
        self.d.line([self.s(x1), self.s(y1), self.s(x2), self.s(y2)],
                    fill=fill, width=max(1, self.s(width)))

    def text(self, x, y, value, size=14, style="regular", fill="#1B2333",
             anchor="la", width=None):
        f = self.font(size, style)
        if width is not None and width > 0:
            value = self._wrap(value, f, width)
        self.d.multiline_text((self.s(x), self.s(y)), value, font=f, fill=fill,
                              anchor=anchor, spacing=self.s(4))

    def _wrap(self, value: str, font, width: float) -> str:
        words = str(value).replace("\n", " \n ").split(" ")
        lines, current = [], ""
        for word in words:
            if word == "\n":
                lines.append(current)
                current = ""
                continue
            probe = f"{current} {word}".strip()
            if font.getlength(probe) <= self.s(width) or not current:
                current = probe
            else:
                lines.append(current)
                current = word
        if current:
            lines.append(current)
        return "\n".join(lines)

    def length(self, value: str, size=14, style="regular") -> float:
        return self.font(size, style).getlength(str(value)) / SCALE

    # -- виджеты ------------------------------------------------------------
    def w_titlebar(self, a):
        x, y, w, h = self.box_of(a)
        self.rect(x, y, w, h, 0, fill=color(a.get("fill", "dark")))
        cx = x + 18
        for i, c in enumerate(("#FF5F57", "#FEBC2E", "#28C840")):
            self.d.ellipse([self.s(cx + i * 18), self.s(y + h / 2 - 6),
                            self.s(cx + i * 18 + 12), self.s(y + h / 2 + 6)], fill=c)
        self.text(x + 84, y + h / 2, a.get("text", ""), 13, "regular",
                  fill=color(a.get("color", "dark-text")), anchor="lm")
        trailing = a.get("trailing")
        if trailing:
            f = self.font(12)
            tw = f.getlength(str(trailing)) / SCALE
            self.d.text((self.s(x + w - 18 - tw), self.s(y + h / 2)), str(trailing),
                        font=f, fill=color("dark-muted"), anchor="lm")

    def w_panel(self, a):
        x, y, w, h = self.box_of(a)
        self.rect(x, y, w, h, a.get("r", 0), fill=color(a.get("fill", "surface"),
                  PALETTE["surface"]), outline=color(a.get("stroke"), None) if a.get("stroke") else None)

    def w_card(self, a):
        x, y, w, h = self.box_of(a)
        self.rect(x + 1, y + 2, w, h, a.get("r", 14), fill="#E3E7F0")
        self.rect(x, y, w, h, a.get("r", 14), fill=color(a.get("fill", "surface")),
                  outline=color(a.get("stroke", "border-soft")))

    def w_label(self, a):
        x, y, w, h = self.box_of(a)
        anchor = {"left": "la", "center": "ma", "right": "ra"}.get(
            str(a.get("align", "left")), "la")
        style = str(a.get("style", "regular"))
        fill = color(a.get("color", "text"))
        size = int(a.get("size", 14))
        if anchor == "ma":
            tx = x + w / 2
        elif anchor == "ra":
            tx = x + w
        else:
            tx = x
        self.text(tx, y + (h / 2 if h else 0), a.get("text", ""), size, style,
                  fill=fill, anchor=anchor if h else "la", width=w if a.get("wrap") else None)

    def w_field(self, a):
        x, y, w, h = self.box_of(a)
        disabled = bool(a.get("disabled"))
        self.rect(x, y, w, h, 9, fill=color(a.get("fill", "surface-alt" if disabled else "surface")),
                  outline=color(a.get("stroke", "border")))
        value = str(a.get("value", ""))
        placeholder = str(a.get("placeholder", ""))
        if a.get("mask"):
            value = "•" * int(a.get("dots", 14))
        f = self.font(int(a.get("size", 15)), "mono" if a.get("mono") else "regular")
        if not value and placeholder:
            value = placeholder
        fill = color("text") if (a.get("value") or (a.get("mask") and not placeholder)) else color("faint")
        pad = 14
        inner_w = w - 2 * pad - (a.get("trailing") and 30 or 0)
        shown = value
        while shown and f.getlength(shown) > self.s(inner_w):
            shown = shown[:-1]
        self.d.text((self.s(x + pad), self.s(y + h / 2)), shown, font=f,
                    fill=fill, anchor="lm")
        if a.get("trailing"):
            self.d.text((self.s(x + w - 14), self.s(y + h / 2)), str(a["trailing"]),
                        font=self.font(12), fill=color("muted"), anchor="rm")

    def w_textarea(self, a):
        x, y, w, h = self.box_of(a)
        self.rect(x, y, w, h, 9, fill=color(a.get("fill", "surface")),
                  outline=color(a.get("stroke", "border")))
        value = str(a.get("value") or a.get("placeholder") or "")
        fill = color("text") if a.get("value") else color("faint")
        self.text(x + 14, y + 12, value, int(a.get("size", 14)),
                  fill=fill, width=w - 28)

    def w_button(self, a):
        x, y, w, h = self.box_of(a)
        style = str(a.get("style", "primary"))
        fill, outline, txt = {
            "primary": (color("primary"), None, color("white")),
            "primary-dark": (color("primary-dark"), None, color("white")),
            "secondary": (color("surface"), color("border"), color("text")),
            "ghost": (None, None, color("primary")),
            "danger": (None, None, color("danger")),
            "danger-solid": (color("danger"), None, color("white")),
            "on-dark": (color("dark-alt"), "#3B4A6B", color("dark-text")),
        }.get(style, (color("primary"), None, color("white")))
        self.rect(x, y, w, h, int(a.get("r", 9)), fill=fill, outline=outline)
        self.text(x + w / 2, y + h / 2, a.get("text", ""), int(a.get("size", 14)),
                  "bold", fill=txt, anchor="mm")

    def w_iconbutton(self, a):
        x, y, w, h = self.box_of(a)
        style = str(a.get("style", "secondary"))
        fill = {
            "secondary": color("surface"),
            "ghost": None,
            "primary": color("primary"),
            "dark": color("dark-alt"),
        }.get(style, color("surface"))
        outline = color("border") if style == "secondary" else None
        self.rect(x, y, w, h, 9, fill=fill, outline=outline)
        txt_fill = color("white") if style == "primary" else color(a.get("color", "text"))
        self.text(x + w / 2, y + h / 2, a.get("glyph", "…"), int(a.get("size", 15)),
                  "regular", fill=txt_fill, anchor="mm")

    def w_checkbox(self, a):
        x, y, w, h = self.box_of(a)
        size = 18
        top = y + h / 2 - size / 2
        checked = bool(a.get("checked"))
        self.rect(x, top, size, size, 4,
                  fill=color("primary") if checked else color("surface"),
                  outline=color("primary") if checked else color("border"))
        if checked:
            self.d.line([self.s(x + 4), self.s(top + 9), self.s(x + 8), self.s(top + 13),
                         self.s(x + 14), self.s(top + 5)], fill=color("white"),
                        width=self.s(2), joint="curve")
        self.text(x + size + 10, y + h / 2, a.get("text", ""), int(a.get("size", 14)),
                  fill=color(a.get("color", "text")), anchor="lm")

    def w_toggle(self, a):
        x, y, w, h = self.box_of(a)
        on = bool(a.get("on", True))
        self.rect(x, y, w, h, h / 2, fill=color("primary") if on else "#C3CAD8")
        knob = h - 6
        kx = x + w - knob - 3 if on else x + 3
        self.d.ellipse([self.s(kx), self.s(y + 3), self.s(kx + knob), self.s(y + 3 + knob)],
                       fill=color("white"))

    def w_divider(self, a):
        x, y, w, h = self.box_of(a)
        self.line(x, y + max(h / 2, 0), x + w, y + max(h / 2, 0),
                  fill=color(a.get("fill", "border-soft")))

    def w_bar(self, a):
        x, y, w, h = self.box_of(a)
        value = max(0.0, min(1.0, float(a.get("value", 0.5))))
        self.rect(x, y, w, h, h / 2, fill=color(a.get("background", "border-soft")))
        self.rect(x, y, max(h, w * value), h, h / 2,
                  fill=color(a.get("fill", "success")))
        if a.get("caption"):
            self.text(x + w + 10, y + h / 2, a["caption"], 12, fill=color("muted"), anchor="lm")

    def w_slider(self, a):
        x, y, w, h = self.box_of(a)
        value = max(0.0, min(1.0, float(a.get("value", 0.5))))
        cy = y + h / 2
        self.line(x, cy, x + w, cy, fill=color("border"), width=4)
        self.line(x, cy, x + w * value, cy, fill=color("primary"), width=4)
        kx = x + w * value
        self.d.ellipse([self.s(kx - 9), self.s(cy - 9), self.s(kx + 9), self.s(cy + 9)],
                       fill=color("white"), outline=color("primary"), width=self.s(2))

    def w_listrow(self, a):
        x, y, w, h = self.box_of(a)
        selected = bool(a.get("selected"))
        if selected:
            self.rect(x, y, w, h, 0, fill=color("primary-soft"))
            self.rect(x, y, 4, h, 0, fill=color("primary"))
        self.rect(x + 14, y + h / 2 - 14, 28, 28, 8, fill=color(a.get("icon", "border-soft")))
        self.text(x + 54, y + h / 2 - 9, a.get("text", ""), int(a.get("size", 14)),
                  "bold" if selected else "regular", fill=color("text"), anchor="lm")
        if a.get("subtitle"):
            self.text(x + 54, y + h / 2 + 11, a["subtitle"], 12, fill=color("muted"), anchor="lm")
        if a.get("badge"):
            self._badge(x + w - 16, y + h / 2, a["badge"])
        self.line(x + 14, y + h, x + w, y + h, fill=color("border-soft"))

    def _badge(self, right_x, center_y, text):
        f = self.font(11, "bold")
        tw = f.getlength(str(text)) / SCALE
        bw = tw + 20
        self.rect(right_x - bw, center_y - 10, bw, 20, 10, fill=color("primary-soft"))
        self.d.text((self.s(right_x - bw / 2), self.s(center_y)), str(text), font=f,
                    fill=color("primary-dark"), anchor="mm")

    def w_sidebarrow(self, a):
        x, y, w, h = self.box_of(a)
        active = bool(a.get("active"))
        if active:
            self.rect(x, y, w, h, 9, fill=color("primary"))
        self.rect(x + 12, y + h / 2 - 8, 16, 16, 4,
                  fill=color("primary") if not active else "#7C9BFF")
        txt_col = color("white") if active else color("sidebar-text")
        self.text(x + 40, y + h / 2, a.get("text", ""), int(a.get("size", 14)),
                  "bold" if active else "regular", fill=txt_col, anchor="lm")
        if a.get("badge"):
            f = self.font(11, "bold")
            tw = f.getlength(str(a["badge"])) / SCALE
            self.d.text((self.s(x + w - 16), self.s(y + h / 2)), str(a["badge"]),
                        font=f, fill=color("dark-muted"), anchor="rm")

    def w_tab(self, a):
        x, y, w, h = self.box_of(a)
        active = bool(a.get("active"))
        col = color("primary") if active else color("muted")
        self.text(x + w / 2, y + h / 2 - 4, a.get("text", ""), int(a.get("size", 14)),
                  "bold" if active else "regular", fill=col, anchor="mm")
        if active:
            self.line(x + 12, y + h - 2, x + w - 12, y + h - 2, fill=color("primary"), width=3)

    def w_statusbar(self, a):
        x, y, w, h = self.box_of(a)
        self.rect(x, y, w, h, 0, fill=color("surface-alt"))
        self.line(x, y, x + w, y, fill=color("border-soft"))
        self.text(x + 18, y + h / 2, a.get("text", ""), 12, fill=color("muted"), anchor="lm")
        if a.get("trailing"):
            self.d.text((self.s(x + w - 18), self.s(y + h / 2)), str(a["trailing"]),
                        font=self.font(12), fill=color("muted"), anchor="rm")

    def w_step(self, a):
        x, y, w, h = self.box_of(a)
        r = h / 2
        active = bool(a.get("active", True))
        fill = color("primary") if active else color("border-soft")
        self.d.ellipse([self.s(x), self.s(y), self.s(x + h), self.s(y + h)],
                       fill=fill)
        self.text(x + r, y + r, a.get("number", ""), 14, "bold",
                  fill=color("white") if active else color("muted"), anchor="mm")
        self.text(x + h + 10, y + r, a.get("text", ""), 13,
                  fill=color("text") if active else color("muted"), anchor="lm")

    def w_codecell(self, a):
        x, y, w, h = self.box_of(a)
        self.rect(x, y, w, h, 9, fill=color("surface"), outline=color("border"))
        self.text(x + w / 2, y + h / 2, a.get("text", ""), 20, "mono-bold",
                  fill=color("text"), anchor="mm")

    def w_qr(self, a):
        x, y, w, h = self.box_of(a)
        self.rect(x, y, w, h, 6, fill=color("white"), outline=color("border"))
        pad = 12
        side = min(w, h) - 2 * pad
        cell = side / 21
        seed = hashlib.sha256(str(a.get("text", "larets")).encode()).digest()
        bits = "".join(f"{b:08b}" for b in seed) * 3

        def finder(ox, oy):
            self.rect(x + pad + ox * cell, y + pad + oy * cell, cell * 7, cell * 7, 0,
                      fill=color("dark"))
            self.rect(x + pad + (ox + 1) * cell, y + pad + (oy + 1) * cell, cell * 5, cell * 5,
                      0, fill=color("white"))
            self.rect(x + pad + (ox + 2) * cell, y + pad + (oy + 2) * cell, cell * 3, cell * 3,
                      0, fill=color("dark"))

        idx = 0
        for row in range(21):
            for col in range(21):
                if (row < 7 and col < 7) or (row < 7 and col > 13) or (row > 13 and col < 7):
                    continue
                if bits[idx % len(bits)] == "1":
                    self.rect(x + pad + col * cell, y + pad + row * cell, cell, cell, 0,
                              fill=color("dark"))
                idx += 1
        finder(0, 0)
        finder(14, 0)
        finder(0, 14)

    def w_logo(self, a):
        x, y, w, h = self.box_of(a)
        self.rect(x, y, w, h, int(a.get("r", w * 0.28)), fill=color(a.get("fill", "primary")))
        cx, cy = x + w / 2, y + h / 2
        bw, bh = w * 0.42, h * 0.30
        self.rect(cx - bw / 2, cy - bh / 2 + h * 0.06, bw, bh, w * 0.06,
                  fill=color("white"))
        self.d.arc([self.s(cx - bw * 0.36), self.s(cy - bh * 0.95),
                    self.s(cx + bw * 0.36), self.s(cy + bh * 0.05)],
                   start=180, end=360, fill=color("white"), width=self.s(max(3, w * 0.055)))
        self.d.ellipse([self.s(cx - w * 0.035), self.s(cy + h * 0.02),
                        self.s(cx + w * 0.035), self.s(cy + h * 0.09)],
                       fill=color("primary"))

    def w_actor(self, a):
        x, y, w, h = self.box_of(a)
        cx = x + w / 2
        r = 9
        self.d.ellipse([self.s(cx - r), self.s(y), self.s(cx + r), self.s(y + 2 * r)],
                       outline=color("text"), width=self.s(1.5))
        self.line(cx, y + 2 * r, cx, y + 2 * r + 22, fill=color("text"), width=1.5)
        self.line(cx - 14, y + 2 * r + 8, cx + 14, y + 2 * r + 8, fill=color("text"), width=1.5)
        self.line(cx, y + 2 * r + 22, cx - 12, y + 2 * r + 40, fill=color("text"), width=1.5)
        self.line(cx, y + 2 * r + 22, cx + 12, y + 2 * r + 40, fill=color("text"), width=1.5)
        self.text(cx, y + 2 * r + 48, a.get("text", ""), 13, "bold",
                  fill=color("text"), anchor="ma", width=w)

    def w_usecase(self, a):
        x, y, w, h = self.box_of(a)
        self.d.ellipse([self.s(x), self.s(y), self.s(x + w), self.s(y + h)],
                       fill=color("primary-soft"), outline=color("primary"),
                       width=self.s(1.5))
        self.text(x + w / 2, y + h / 2 - 8, a.get("text", ""), int(a.get("size", 12)),
                  fill=color("text"), anchor="ma", width=w - 28)

    def w_boundary(self, a):
        x, y, w, h = self.box_of(a)
        self.rect(x, y, w, h, 12, fill=color("surface"), outline=color("border"), width=1.5)
        if a.get("text"):
            self.text(x + w / 2, y + 16, a["text"], 13, "bold", fill=color("muted"),
                      anchor="ma")

    def w_connector(self, a):
        x, y = self.box_of(a)[:2]
        x2, y2 = float(a.get("x2", x + 40)), float(a.get("y2", y))
        dashed = bool(a.get("dashed"))
        if dashed:
            self._dashed_line(x, y, x2, y2, color(a.get("fill", "muted")))
        else:
            self.line(x, y, x2, y2, fill=color(a.get("fill", "muted")), width=1.5)
        if a.get("text"):
            frac = float(a.get("labelAt", 0.5))
            lx, ly = x + (x2 - x) * frac, y + (y2 - y) * frac
            label = str(a["text"])
            width = self.length(label, 11) + 12
            self.rect(lx - width / 2, ly - 9, width, 18, 4, fill=color("bg"))
            self.text(lx, ly, label, 11, fill=color("muted"), anchor="mm")

    def _dashed_line(self, x1, y1, x2, y2, fill):
        dist = math.hypot(x2 - x1, y2 - y1)
        if dist == 0:
            return
        steps = max(2, int(dist // 10))
        for i in range(steps):
            t0, t1 = i / steps, (i + 0.55) / steps
            self.line(x1 + (x2 - x1) * t0, y1 + (y2 - y1) * t0,
                      x1 + (x2 - x1) * t1, y1 + (y2 - y1) * t1,
                      fill=fill, width=1.2)

    # -- общее --------------------------------------------------------------
    @staticmethod
    def box_of(a) -> tuple[float, float, float, float]:
        return (float(a.get("x", 0)), float(a.get("y", 0)),
                float(a.get("w", 0)), float(a.get("h", 0)))

    def render(self, screen: Node) -> Image.Image:
        for part in screen.parts:
            handler = getattr(self, f"w_{part.type.lower()}" if part.type else "", None)
            if handler is None:
                print(f"  ! неизвестный тип виджета: {part.type} ({part.name})")
                continue
            handler(part.attrs)
        return self.img.resize((self.w, self.h), Image.LANCZOS)


# ----------------------------------------------------------------------------
def main() -> int:
    parser = argparse.ArgumentParser(description="SysML v2 → PNG mockup renderer")
    parser.add_argument("--model", default=str(HERE / "ui-mockups.sysml"))
    parser.add_argument("--extra", action="append", default=[],
                        help="дополнительные .sysml-файлы (например use-case-diagram.sysml)")
    parser.add_argument("--out", default=str(HERE))
    parser.add_argument("--only", default=None, help="отрисовать только указанный экран")
    args = parser.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    files = [Path(args.model)] + [Path(p) for p in args.extra]
    screens: list[Node] = []
    for path in files:
        if not path.exists():
            sys.exit(f"Модель не найдена: {path}")
        screens.extend(parse_sysml(path.read_text(encoding="utf-8")))

    targets = [s for s in screens if s.attrs.get("kind") == "screen"]
    if args.only:
        targets = [s for s in targets if s.name == args.only]
    if not targets:
        sys.exit("В модели не найдено ни одного part def с attribute kind = \"screen\"")

    for screen in targets:
        width = int(screen.attrs.get("canvasWidth", 1000))
        height = int(screen.attrs.get("canvasHeight", 640))
        painter = Painter(width, height)
        image = painter.render(screen)
        filename = str(screen.attrs.get("file", f"{screen.name}.png"))
        image.save(out_dir / filename)
        print(f"  ✓ {screen.name:24s} → {out_dir / filename}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
