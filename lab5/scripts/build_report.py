#!/usr/bin/env python3
"""Build a formatted Russian DOCX report from report.md and embedded UML PNGs."""
from pathlib import Path
import re
from docx import Document
from docx.shared import Cm, Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "report.md"
OUT = ROOT / "report.docx"

def set_run_font(run, name="Times New Roman", size=14, bold=None, italic=None):
    run.font.name = name
    run._element.rPr.rFonts.set(qn('w:eastAsia'), name)
    run.font.size = Pt(size)
    if bold is not None: run.bold = bold
    if italic is not None: run.italic = italic

def add_inline(paragraph, content, size=14, base_bold=False):
    # Minimal Markdown inline support for bold, code and links.
    token_re = re.compile(r'(\*\*.+?\*\*|`[^`]+`|\[[^\]]+\]\([^)]+\))')
    pos = 0
    for m in token_re.finditer(content):
        if m.start() > pos:
            r = paragraph.add_run(content[pos:m.start()]); set_run_font(r, size=size, bold=base_bold)
        token = m.group(0)
        if token.startswith('**'):
            r = paragraph.add_run(token[2:-2]); set_run_font(r, size=size, bold=True)
        elif token.startswith('`'):
            r = paragraph.add_run(token[1:-1]); set_run_font(r, name='Consolas', size=size-1)
        else:
            label = re.match(r'\[([^\]]+)\]', token).group(1)
            r = paragraph.add_run(label); set_run_font(r, size=size, bold=base_bold)
        pos = m.end()
    if pos < len(content):
        r = paragraph.add_run(content[pos:]); set_run_font(r, size=size, bold=base_bold)

def style_para(p, align=WD_ALIGN_PARAGRAPH.JUSTIFY, indent=True, spacing=1.5):
    p.alignment = align
    fmt = p.paragraph_format
    fmt.line_spacing = spacing
    fmt.space_after = Pt(6)
    if indent: fmt.first_line_indent = Cm(1.25)


doc = Document()
sec = doc.sections[0]
sec.page_width = Cm(21.0); sec.page_height = Cm(29.7)
sec.top_margin = Cm(2.0); sec.bottom_margin = Cm(2.0)
sec.left_margin = Cm(2.7); sec.right_margin = Cm(1.5)

normal = doc.styles['Normal']
normal.font.name = 'Times New Roman'; normal._element.rPr.rFonts.set(qn('w:eastAsia'), 'Times New Roman'); normal.font.size = Pt(14)
normal.paragraph_format.line_spacing = 1.5
for name, size in [('Heading 1',16),('Heading 2',14),('Heading 3',14)]:
    st=doc.styles[name]; st.font.name='Times New Roman'; st._element.rPr.rFonts.set(qn('w:eastAsia'),'Times New Roman'); st.font.size=Pt(size); st.font.bold=True
    st.paragraph_format.keep_with_next=True; st.paragraph_format.space_before=Pt(10); st.paragraph_format.space_after=Pt(6)

# Footer with an automatic page number field.
footer = sec.footer.paragraphs[0]
footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
r=footer.add_run('Лабораторная работа №5 — Guardian — '); set_run_font(r,size=10)
fld=OxmlElement('w:fldSimple'); fld.set(qn('w:instr'),'PAGE'); footer._p.append(fld)

# Title page.
for val, size, bold in [
    ('Министерство образования Республики Беларусь',14,False),
    ('Учреждение образования',14,False),
    ('«БЕЛОРУССКИЙ ГОСУДАРСТВЕННЫЙ УНИВЕРСИТЕТ',14,True),
    ('ИНФОРМАТИКИ И РАДИОЭЛЕКТРОНИКИ»',14,True),
]:
    p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER; p.paragraph_format.space_after=Pt(2)
    set_run_font(p.add_run(val),size=size,bold=bold)
for _ in range(2): doc.add_paragraph()
for val in ['Факультет компьютерных систем и сетей','Кафедра электронных вычислительных машин','Дисциплина: «Жизненный цикл разработки программного обеспечения»']:
    p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER; p.paragraph_format.space_after=Pt(4); set_run_font(p.add_run(val),size=14)
for _ in range(3): doc.add_paragraph()
p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER; set_run_font(p.add_run('ОТЧЁТ'),size=18,bold=True)
p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER; set_run_font(p.add_run('по лабораторной работе № 5'),size=16,bold=True)
p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER; set_run_font(p.add_run('на тему'),size=14)
for val in ['«МОДЕЛИРОВАНИЕ ДИНАМИЧЕСКОГО ПОВЕДЕНИЯ','СИСТЕМЫ НА ЯЗЫКЕ UML»']:
    p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER; p.paragraph_format.space_after=Pt(1); set_run_font(p.add_run(val),size=15,bold=True)
for _ in range(3): doc.add_paragraph()
p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.RIGHT; p.paragraph_format.right_indent=Cm(1)
set_run_font(p.add_run('Студент: Д.А. Муравьёв'),size=14)
p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.RIGHT; p.paragraph_format.right_indent=Cm(1)
set_run_font(p.add_run('Преподаватель: Д.В. Куприянова'),size=14)
for _ in range(5): doc.add_paragraph()
p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER; set_run_font(p.add_run('Минск 2026'),size=14)
doc.add_page_break()

lines = SRC.read_text(encoding='utf-8').splitlines()
start = next(i for i,line in enumerate(lines) if line.startswith('# 1 ЦЕЛЬ'))
for i,line in enumerate(lines[start:], start=start):
    s=line.strip()
    if not s or s == '---': continue
    img=re.match(r'!\[([^\]]*)\]\(([^)]+)\)', s)
    if img:
        image_path=(ROOT/img.group(2)).resolve()
        # Place each diagram on a clean page and preserve its aspect ratio.
        doc.add_page_break()
        p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER
        with Image.open(image_path) as im:
            wpx,hpx=im.size
        max_w,max_h=6.55,7.4
        ratio=min(max_w/wpx,max_h/hpx)
        p.add_run().add_picture(str(image_path),width=Inches(wpx*ratio),height=Inches(hpx*ratio))
        continue
    if s.startswith('# '):
        p=doc.add_paragraph(style='Heading 1'); p.alignment=WD_ALIGN_PARAGRAPH.CENTER; add_inline(p,s[2:],16,True)
    elif s.startswith('## '):
        p=doc.add_paragraph(style='Heading 2'); p.alignment=WD_ALIGN_PARAGRAPH.LEFT; add_inline(p,s[3:],14,True)
    elif s.startswith('### '):
        p=doc.add_paragraph(style='Heading 3'); p.alignment=WD_ALIGN_PARAGRAPH.LEFT; add_inline(p,s[4:],14,True)
    elif s.startswith('**') and s.endswith('**'):
        p=doc.add_paragraph(); style_para(p,WD_ALIGN_PARAGRAPH.CENTER,False,1.0); add_inline(p,s,12,True)
    elif re.match(r'^\d+\.\s+',s):
        p=doc.add_paragraph(style='List Number'); style_para(p,WD_ALIGN_PARAGRAPH.JUSTIFY,False,1.5); add_inline(p,re.sub(r'^\d+\.\s+','',s),14)
    elif s.startswith('- '):
        p=doc.add_paragraph(style='List Bullet'); style_para(p,WD_ALIGN_PARAGRAPH.JUSTIFY,False,1.5); add_inline(p,s[2:],14)
    else:
        p=doc.add_paragraph(); style_para(p,WD_ALIGN_PARAGRAPH.JUSTIFY,True,1.5); add_inline(p,s,14)

# Keep the report's metadata informative without asserting an implementation not present in the repository.
doc.core_properties.title = 'Лабораторная работа №5 — UML-моделирование Guardian'
doc.core_properties.subject = 'Моделирование динамического поведения системы на языке UML'
doc.core_properties.author = 'Д.А. Муравьёв'
doc.save(OUT)
print(OUT)
