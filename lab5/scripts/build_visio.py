#!/usr/bin/env python3
"""Build editable A3 Visio sheets from the four Guardian SVG diagrams.

The diagram symbols/text are translated to native Visio shapes. The page frame
and title block follow the A3/ESKD sheet conventions (GOST 2.301 and 2.104);
UML notation remains UML, not an electrical E3 schematic.
"""
from __future__ import annotations

import math
import re
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path

import vsdx
from vsdx import VisioFile

ROOT = Path(__file__).resolve().parents[1]
DIAGRAM_DIR = ROOT / "diagrams"
OUT = ROOT / "visio"
OUT.mkdir(parents=True, exist_ok=True)
MEDIA_TEMPLATE = Path(vsdx.__file__).parent / "media" / "media.vsdx"
NS = vsdx.namespace
MM_PER_IN = 25.4
PAGE_A3_MM = {"landscape": (420.0, 297.0), "portrait": (297.0, 420.0)}

DIAGRAMS = [
    ("use-case", "Диаграмма вариантов использования", "landscape", "GDN-ЛР5-01"),
    ("activity", "Диаграмма активности", "portrait", "GDN-ЛР5-02"),
    ("state", "Диаграмма состояний", "landscape", "GDN-ЛР5-03"),
    ("sequence", "Диаграмма последовательности", "landscape", "GDN-ЛР5-04"),
]


def get_cell(shape, name):
    return shape.xml.find(f'{NS}Cell[@N="{name}"]')


def set_text_style(shape, size_in, bold=False, align="center", color="#000000"):
    """Set explicit Visio character/paragraph styling in inches and alignment."""
    char = shape.xml.find(f'{NS}Section[@N="Character"]')
    if char is None:
        char = ET.SubElement(shape.xml, f'{NS}Section', {"N": "Character"})
    for row in list(char):
        char.remove(row)
    crow = ET.SubElement(char, f'{NS}Row', {"IX": "0"})
    for name, value in (("Size", size_in), ("Color", color), ("Style", 1 if bold else 0)):
        ET.SubElement(crow, f'{NS}Cell', {"N": name, "V": str(value)})

    para = shape.xml.find(f'{NS}Section[@N="Paragraph"]')
    if para is None:
        para = ET.SubElement(shape.xml, f'{NS}Section', {"N": "Paragraph"})
    for row in list(para):
        para.remove(row)
    prow = ET.SubElement(para, f'{NS}Row', {"IX": "0"})
    h_align = {"left": 0, "center": 1, "right": 2}[align]
    ET.SubElement(prow, f'{NS}Cell', {"N": "HorzAlign", "V": str(h_align)})
    for name in ("TextMarginLeft", "TextMarginRight", "TextMarginTop", "TextMarginBottom"):
        shape.set_cell_value(name, "0.02")


def place(shape, x0, y0, x1, y1):
    width = max(abs(x1 - x0), 0.001)
    height = max(abs(y1 - y0), 0.001)
    shape.width = width
    shape.height = height
    shape.loc_x = width / 2
    shape.loc_y = height / 2
    shape.x = (x0 + x1) / 2
    shape.y = (y0 + y1) / 2


def style_shape(shape, stroke="#000000", fill="#FFFFFF", weight=0.012, no_fill=False, no_line=False):
    shape.line_color = stroke
    shape.fill_color = fill
    shape.line_weight = weight
    geo = shape.xml.find(f'{NS}Section[@N="Geometry"]')
    if geo is not None:
        for name, value in (("NoFill", "1" if no_fill else "0"), ("NoLine", "1" if no_line else "0")):
            cell = geo.find(f'{NS}Cell[@N="{name}"]')
            if cell is None:
                cell = ET.SubElement(geo, f'{NS}Cell', {"N": name})
            cell.attrib["V"] = value


def add_rect(page, templates, x0, y0, x1, y1, text="", *, weight=0.012,
             fill="#FFFFFF", stroke="#000000", font_in=None, bold=False,
             align="center", no_fill=False, no_line=False):
    shape = templates["rect"].copy(page)
    place(shape, x0, y0, x1, y1)
    shape.text = text
    style_shape(shape, stroke=stroke, fill=fill, weight=weight,
                no_fill=no_fill, no_line=no_line)
    if font_in is not None:
        set_text_style(shape, font_in, bold=bold, align=align)
    return shape


def add_ellipse(page, templates, x0, y0, x1, y1, *, fill="#FFFFFF", stroke="#000000", weight=0.012):
    shape = templates["circle"].copy(page)
    place(shape, x0, y0, x1, y1)
    shape.text = ""
    style_shape(shape, stroke=stroke, fill=fill, weight=weight)
    return shape


def add_line(page, templates, x1, y1, x2, y2, *, weight=0.009, arrow=None, dashed=False, color="#000000"):
    """Add an editable freeform segment with correctly oriented endpoints.

    The package's line helper flattens every segment to a horizontal geometry,
    which detaches vertical and reversed arrow segments in Visio. A 2-D freeform
    path avoids that limitation and keeps positive shape dimensions in all cases.
    """
    epsilon = 0.001
    left, right = sorted((x1, x2))
    bottom, top = sorted((y1, y2))
    if right - left < epsilon:
        left, right = (x1 - epsilon/2, x1 + epsilon/2)
    if top - bottom < epsilon:
        bottom, top = (y1 - epsilon/2, y1 + epsilon/2)

    shape = templates["rect"].copy(page)
    place(shape, left, bottom, right, top)
    shape.text = ""
    style_shape(shape, stroke=color, fill="#FFFFFF", weight=weight,
                no_fill=True, no_line=False)
    shape.set_cell_value("LinePattern", "2" if dashed else "1")

    geometry = shape.xml.find(f'{NS}Section[@N="Geometry"]')
    for row in list(geometry.findall(f'{NS}Row')):
        geometry.remove(row)
    for index, (kind, px, py) in enumerate((
        ("MoveTo", x1-left, y1-bottom),
        ("LineTo", x2-left, y2-bottom),
    ), 1):
        row = ET.SubElement(geometry, f'{NS}Row', {"T": kind, "IX": str(index)})
        ET.SubElement(row, f'{NS}Cell', {"N": "X", "V": str(px)})
        ET.SubElement(row, f'{NS}Cell', {"N": "Y", "V": str(py)})

    if arrow == "open":
        shape.end_arrow = "1"
    elif arrow:
        shape.end_arrow = True
    else:
        shape.end_arrow = False
    return shape


def add_diamond(page, templates, x0, y0, x1, y1, *, weight=0.012):
    shape = templates["rect"].copy(page)
    place(shape, x0, y0, x1, y1)
    shape.text = ""
    style_shape(shape, stroke="#000000", fill="#FFFFFF", weight=weight)
    geo = shape.xml.find(f'{NS}Section[@N="Geometry"]')
    for row in list(geo.findall(f'{NS}Row')):
        geo.remove(row)
    points = [(0.5, 0), (1, 0.5), (0.5, 1), (0, 0.5), (0.5, 0)]
    for i, (px, py) in enumerate(points, 1):
        typ = "RelMoveTo" if i == 1 else "RelLineTo"
        row = ET.SubElement(geo, f'{NS}Row', {"T": typ, "IX": str(i)})
        ET.SubElement(row, f'{NS}Cell', {"N": "X", "V": str(px)})
        ET.SubElement(row, f'{NS}Cell', {"N": "Y", "V": str(py)})
    return shape


def parse_path(d):
    """Parse the simple M/L/H/V paths emitted by render_diagrams.py."""
    tokens = re.findall(r'[A-Za-z]|[-+]?(?:\d*\.\d+|\d+\.?\d*)(?:[eE][-+]?\d+)?', d)
    out, i, cmd, current, substart = [], 0, None, (0.0, 0.0), None
    while i < len(tokens):
        if tokens[i].isalpha():
            cmd = tokens[i]
            i += 1
            if cmd in "Zz":
                if substart and current != substart:
                    out.append(substart)
                    current = substart
                continue
        if cmd in "MmLl":
            x, y = float(tokens[i]), float(tokens[i + 1]); i += 2
            if cmd.islower(): x, y = current[0] + x, current[1] + y
            current = (x, y)
            if cmd in "Mm":
                substart = current
                out.append(current)
                cmd = "l" if cmd == "m" else "L"
            else:
                out.append(current)
        elif cmd in "Hh":
            x = float(tokens[i]); i += 1
            if cmd == "h": x += current[0]
            current = (x, current[1]); out.append(current)
        elif cmd in "Vv":
            y = float(tokens[i]); i += 1
            if cmd == "v": y += current[1]
            current = (current[0], y); out.append(current)
        else:
            raise ValueError(f"Unsupported SVG path command {cmd!r} in {d!r}")
    return out


def local_name(tag):
    return tag.rsplit("}", 1)[-1]


def parse_text(element):
    lines = []
    for child in list(element):
        if local_name(child.tag) == "tspan":
            lines.append("".join(child.itertext()))
    if not lines:
        return ["".join(element.itertext())]
    return lines


def read_float(element, name, default=0.0):
    try:
        return float(element.attrib.get(name, default))
    except (TypeError, ValueError):
        return default


def map_point(x, y, scale, origin_x, top_y):
    return origin_x + x * scale, top_y - y * scale


def add_svg_text(page, templates, element, scale, origin_x, top_y):
    lines = parse_text(element)
    if not lines or not any(lines):
        return
    x, y = read_float(element, "x"), read_float(element, "y")
    font_px = read_float(element, "font-size", 16)
    size = max(font_px * scale, 0.055)
    anchor = element.attrib.get("text-anchor", "start")
    weight = element.attrib.get("font-weight", "400")
    bold = weight in ("600", "700", "bold")
    line_height = font_px * 1.18 * scale
    max_chars = max(len(line) for line in lines)
    width = max(max_chars * size * 0.62 + size * 0.8, size * 2)
    height = max(len(lines) * line_height + size * 0.55, size * 1.45)
    px, py = map_point(x, y, scale, origin_x, top_y)
    if anchor == "middle":
        cx = px
        align = "center"
    elif anchor == "end":
        cx = px - width / 2
        align = "right"
    else:
        cx = px + width / 2
        align = "left"
    # SVG y is the first baseline; Visio text box center is slightly above that baseline.
    cy = py + (len(lines) - 1) * line_height / 2 + size * 0.25
    shape = add_rect(page, templates, cx-width/2, cy-height/2, cx+width/2, cy+height/2,
                     "\n".join(lines), weight=0, font_in=size, bold=bold,
                     align=align, no_fill=True, no_line=True)
    # Transparent text shapes must not carry a visible border or fill.
    return shape


def add_svg_path(page, templates, element, scale, origin_x, top_y):
    pts = parse_path(element.attrib.get("d", ""))
    if len(pts) < 2:
        return
    stroke_width = read_float(element, "stroke-width", 1.5)
    line_weight = max(stroke_width * scale, 0.006)
    dashed = bool(element.attrib.get("stroke-dasharray"))
    marker = element.attrib.get("marker-end", "")
    arrow = "open" if "openArrow" in marker else ("filled" if "arrow" in marker else None)
    # Native Visio line segments keep the orthogonal routing editable.
    for index, ((ax, ay), (bx, by)) in enumerate(zip(pts, pts[1:])):
        p1 = map_point(ax, ay, scale, origin_x, top_y)
        p2 = map_point(bx, by, scale, origin_x, top_y)
        add_line(page, templates, *p1, *p2, weight=line_weight,
                 arrow=arrow if index == len(pts)-2 else None, dashed=dashed)


def add_svg_element(page, templates, element, scale, origin_x, top_y, view_w, view_h):
    tag = local_name(element.tag)
    if tag == "rect":
        x, y = read_float(element, "x"), read_float(element, "y")
        w, h = read_float(element, "width"), read_float(element, "height")
        if x == 0 and y == 0 and w >= view_w and h >= view_h:
            return  # the white SVG page background is the Visio page itself
        a = map_point(x, y, scale, origin_x, top_y)
        b = map_point(x+w, y+h, scale, origin_x, top_y)
        line_weight = max(read_float(element, "stroke-width", 1.2) * scale, 0.005)
        add_rect(page, templates, a[0], b[1], b[0], a[1], weight=line_weight,
                 fill="#FFFFFF", stroke="#000000")
    elif tag == "ellipse":
        cx, cy = read_float(element, "cx"), read_float(element, "cy")
        rx, ry = read_float(element, "rx"), read_float(element, "ry")
        a = map_point(cx-rx, cy-ry, scale, origin_x, top_y)
        b = map_point(cx+rx, cy+ry, scale, origin_x, top_y)
        add_ellipse(page, templates, a[0], b[1], b[0], a[1],
                    weight=max(read_float(element, "stroke-width", 1.5)*scale, .005))
    elif tag == "circle":
        cx, cy, r = read_float(element, "cx"), read_float(element, "cy"), read_float(element, "r")
        a = map_point(cx-r, cy-r, scale, origin_x, top_y)
        b = map_point(cx+r, cy+r, scale, origin_x, top_y)
        circle_fill = "#000000" if element.attrib.get("fill", "#fff").lower() not in ("#fff", "#ffffff", "white", "none") else "#FFFFFF"
        add_ellipse(page, templates, a[0], b[1], b[0], a[1], fill=circle_fill, weight=.010)
    elif tag == "line":
        x1, y1 = read_float(element, "x1"), read_float(element, "y1")
        x2, y2 = read_float(element, "x2"), read_float(element, "y2")
        p1, p2 = map_point(x1,y1,scale,origin_x,top_y), map_point(x2,y2,scale,origin_x,top_y)
        add_line(page, templates, *p1, *p2,
                 weight=max(read_float(element,"stroke-width",1.5)*scale,.004),
                 dashed=bool(element.attrib.get("stroke-dasharray")))
    elif tag == "path":
        add_svg_path(page, templates, element, scale, origin_x, top_y)
    elif tag == "polygon":
        pts = [tuple(map(float, pair.split(','))) for pair in element.attrib.get("points", "").split()]
        if not pts:
            return
        xs, ys = zip(*pts)
        a = map_point(min(xs), max(ys), scale, origin_x, top_y)
        b = map_point(max(xs), min(ys), scale, origin_x, top_y)
        shape = add_diamond(page, templates, a[0], a[1], b[0], b[1], weight=.012)
    elif tag == "text":
        add_svg_text(page, templates, element, scale, origin_x, top_y)


def mm(value):
    return value / MM_PER_IN


def add_sheet_frame_and_title(page, templates, page_w_mm, page_h_mm, title, code):
    # GOST/ESKD sheet frame: 20 mm binding margin, 5 mm other margins.
    x0, y0 = mm(20), mm(5)
    x1, y1 = mm(page_w_mm-5), mm(page_h_mm-5)
    add_rect(page, templates, x0, y0, x1, y1, weight=mm(.5), no_fill=True)

    # A3 first-sheet title block (185 x 55 mm), bottom-right inside the frame.
    bx, by, bw, bh = mm(page_w_mm-5-185), mm(5), mm(185), mm(55)
    add_rect(page, templates, bx, by, bx+bw, by+bh, weight=mm(.5), no_fill=True)
    # Internal grid: change row, drawing title, author/reviewer, sheet data.
    for yy in (by+mm(10), by+mm(20), by+mm(40), by+mm(48)):
        add_line(page, templates, bx, yy, bx+bw, yy, weight=mm(.35))
    # Column dividers are scoped to their title-block bands.
    for offset in (20, 40, 95, 140):
        xx = bx + mm(offset)
        add_line(page, templates, xx, by+mm(48), xx, by+bh, weight=mm(.35))
    for offset in (45, 90, 135):
        xx = bx + mm(offset)
        add_line(page, templates, xx, by, xx, by+mm(10), weight=mm(.35))
    add_line(page, templates, bx+mm(90), by+mm(10), bx+mm(90), by+mm(20), weight=mm(.35))
    add_line(page, templates, bx+mm(110), by+mm(20), bx+mm(110), by+mm(40), weight=mm(.35))
    # Change table labels, title/designation, author, and sheet data.
    change_labels = ["Изм.", "Лист", "№ докум.", "Подп.", "Дата"]
    change_widths = [20, 20, 55, 45, 45]
    cx = bx
    for label, width in zip(change_labels, change_widths):
        add_rect(page, templates, cx, by+mm(48), cx+mm(width), by+bh, label,
                 weight=0, font_in=mm(2.5), align="center", no_fill=True, no_line=True)
        cx += mm(width)
    add_rect(page, templates, bx+mm(2), by+mm(41), bx+bw-mm(2), by+mm(47), "БГУИР  |  Жизненный цикл разработки ПО  |  ЛР №5",
             weight=0, font_in=mm(2.4), align="left", no_fill=True, no_line=True)
    add_rect(page, templates, bx+mm(2), by+mm(23), bx+mm(108), by+mm(38), title,
             weight=0, font_in=mm(3.5), bold=True, align="left", no_fill=True, no_line=True)
    add_rect(page, templates, bx+mm(112), by+mm(23), bx+bw-mm(2), by+mm(38), f"Обозначение\n{code}",
             weight=0, font_in=mm(2.6), align="left", no_fill=True, no_line=True)
    add_rect(page, templates, bx+mm(2), by+mm(12), bx+mm(90), by+mm(19), "Разраб.  Д.А. Муравьёв",
             weight=0, font_in=mm(2.6), align="left", no_fill=True, no_line=True)
    add_rect(page, templates, bx+mm(92), by+mm(12), bx+bw-mm(2), by+mm(19), "Преподаватель  Д.В. Куприянова",
             weight=0, font_in=mm(2.6), align="left", no_fill=True, no_line=True)
    bottom_fields = [(bx, bx+mm(45), "Лист 1/1"),
                     (bx+mm(45), bx+mm(90), "Формат A3"),
                     (bx+mm(90), bx+mm(135), "Масштаб б/м"),
                     (bx+mm(135), bx+bw, "2026")]
    for left, right, text in bottom_fields:
        add_rect(page, templates, left, by+mm(1), right, by+mm(9), text,
                 weight=0, font_in=mm(2.5), align="center", no_fill=True, no_line=True)


def build_one(name, title, orientation, code):
    page_w_mm, page_h_mm = PAGE_A3_MM[orientation]
    output = OUT / f"{name}-A3.vsdx"
    svg_path = DIAGRAM_DIR / f"{name}.svg"
    root = ET.parse(svg_path).getroot()
    view_w, view_h = (float(v) for v in root.attrib["viewBox"].split()[2:])

    with VisioFile(str(MEDIA_TEMPLATE)) as vis:
        page = vis.pages[0]
        page.name = f"{name} A3"
        page.width, page.height = mm(page_w_mm), mm(page_h_mm)
        # Set explicit paper page values so Visio opens in the chosen A3 orientation.
        for cell_name, value in (("PageWidth", mm(page_w_mm)), ("PageHeight", mm(page_h_mm))):
            cell = page._pagesheet_xml.find(f'{NS}Cell[@N="{cell_name}"]')
            cell.attrib["V"] = str(value)
        templates = {
            "rect": page.find_shape_by_id("1"),
            "circle": page.find_shape_by_id("7"),
            "line": page.find_shape_by_id("8"),
        }
        # Keep template XML as cloning sources, but remove its demonstration shapes.
        for shape in list(page.child_shapes):
            shape.remove()

        add_sheet_frame_and_title(page, templates, page_w_mm, page_h_mm, title, code)

        left_mm, right_mm = 25.0, page_w_mm-10.0
        bottom_mm, top_mm = 65.0, page_h_mm-10.0
        area_w, area_h = right_mm-left_mm, top_mm-bottom_mm
        scale_mm = min(area_w/view_w, area_h/view_h)
        content_w, content_h = view_w*scale_mm, view_h*scale_mm
        origin_x = mm(left_mm + (area_w-content_w)/2)
        top_y = mm(top_mm - (area_h-content_h)/2)
        scale = mm(scale_mm)
        for element in list(root):
            add_svg_element(page, templates, element, scale, origin_x, top_y, view_w, view_h)

        vis.save_vsdx(str(output))
    print(output)


if __name__ == "__main__":
    for spec in DIAGRAMS:
        build_one(*spec)
