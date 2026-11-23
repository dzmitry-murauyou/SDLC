#!/usr/bin/env python3
"""Render the four Guardian UML views to accessible SVG and PNG assets."""
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1] / "diagrams"
ROOT.mkdir(parents=True, exist_ok=True)


def svg_start(w, h):
    return [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<defs>
  <marker id="arrow" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 z" fill="#26364a"/></marker>
  <marker id="openArrow" markerWidth="12" markerHeight="10" refX="11" refY="5" orient="auto"><path d="M1,1 L11,5 L1,9" fill="none" stroke="#48576a" stroke-width="1.5"/></marker>
  <style>
    text {{ font-family: Arial, 'DejaVu Sans', sans-serif; fill: #182230; }}
    .subtitle {{ font-size: 17px; fill: #566579; }}
    .lane {{ font-size: 20px; font-weight: 700; fill: #26364a; }}
    .label {{ font-size: 18px; }}
    .small {{ font-size: 15px; }}
    .tiny {{ font-size: 13px; }}
  </style>
</defs>
<rect width="100%" height="100%" fill="#ffffff"/>
''']


def text(x, y, value, size=18, anchor="middle", weight="400", fill="#182230", cls=None):
    c = f' class="{cls}"' if cls else ""
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" font-weight="{weight}" fill="{fill}"{c}>{escape(value)}</text>'


def lines_text(x, y, lines, size=17, line=22, anchor="middle", weight="400", fill="#182230"):
    out = [f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" font-weight="{weight}" fill="{fill}">']
    for i, val in enumerate(lines):
        out.append(f'<tspan x="{x}" dy="{0 if i == 0 else line}">{escape(val)}</tspan>')
    out.append('</text>')
    return ''.join(out)


def actor(cx, cy, label, lines=()):
    out = [f'<circle cx="{cx}" cy="{cy-35}" r="18" fill="#fff" stroke="#26364a" stroke-width="3"/>',
           f'<line x1="{cx}" y1="{cy-17}" x2="{cx}" y2="{cy+35}" stroke="#26364a" stroke-width="3"/>',
           f'<line x1="{cx-30}" y1="{cy+3}" x2="{cx+30}" y2="{cy+3}" stroke="#26364a" stroke-width="3"/>',
           f'<line x1="{cx}" y1="{cy+35}" x2="{cx-25}" y2="{cy+70}" stroke="#26364a" stroke-width="3"/>',
           f'<line x1="{cx}" y1="{cy+35}" x2="{cx+25}" y2="{cy+70}" stroke="#26364a" stroke-width="3"/>']
    label_lines = list(lines) if lines else [label]
    out.append(lines_text(cx, cy+98, label_lines, 16, 19, weight="700"))
    return ''.join(out)


def usecase_ellipse(cx, cy, rx, ry, label, optional=False):
    dash = ' stroke-dasharray="9 7"' if optional else ''
    stroke = '#b56a12' if optional else '#315f8e'
    fill = '#ffffff'
    return (f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{stroke}" stroke-width="2.4"{dash}/>' +
            lines_text(cx, cy-10, label, 16, 20, weight="600", fill="#17283b"))


def diagram_usecase():
    w,h=1800,1210; a=svg_start(w,h)
    a.append('<rect x="300" y="120" width="1120" height="1050" rx="18" fill="#fff" stroke="#26364a" stroke-width="3"/>')
    a.append(text(860,155,"Guardian 1.0 — локальное настольное приложение",21,weight="700"))
    centers=[200+i*100 for i in range(10)]
    # User associations use an outside trunk and one horizontal association per use case.
    a.append('<path d="M 185 653 L 270 653 L 270 200 L 270 1100" fill="none" stroke="#8995a5" stroke-width="1.6"/>')
    for cy in centers:
        a.append(f'<path d="M 270 {cy} L 580 {cy}" fill="none" stroke="#8995a5" stroke-width="1.6"/>')
    # External actors connect only to the use cases they participate in.
    for cy in (200,300):
        a.append(f'<path d="M 1590 243 L 1450 243 L 1450 {cy} L 1120 {cy}" fill="none" stroke="#8995a5" stroke-width="1.6"/>')
    a.append('<path d="M 1590 503 L 1450 503 L 1450 800 L 1120 800" fill="none" stroke="#8995a5" stroke-width="1.6"/>')
    a.append('<path d="M 1590 803 L 1450 803 L 1450 1100 L 1120 1100" fill="none" stroke="#8995a5" stroke-width="1.6"/>')
    for cy in (900,1000):
        a.append(f'<path d="M 1590 1033 L 1450 1033 L 1450 {cy} L 1120 {cy}" fill="none" stroke="#8995a5" stroke-width="1.6"/>')
    cases=[
      (200,["UC-01 Создать хранилище и", "зарегистрировать первичный ключ"]),
      (300,["UC-02 Разблокировать хранилище"]),
      (400,["UC-03 Управлять обычными записями", "и защищёнными заметками"]),
      (500,["UC-04 Сгенерировать пароль"]),
      (600,["UC-05 Просмотреть TOTP-код"]),
      (700,["UC-06 Хранить / явно раскрыть", "wallet-secret"]),
      (800,["UC-07 Безопасно заполнить запись", "в браузере"]),
      (900,["UC-08 Создать зашифрованную копию"]),
      (1000,["UC-09 Восстановить резервную копию"]),
      (1100,["UC-10 Заблокировать хранилище"]),
    ]
    for cy,lab in cases:a.append(usecase_ellipse(850,cy,270,34,lab))
    a.append(actor(150,650,"Пользователь"))
    a.append(actor(1620,240,"USB-ключ",["USB-ключ","FIDO2/WebAuthn"]))
    a.append(actor(1620,500,"Браузер",["Утверждённый","браузер Windows"]))
    a.append(actor(1620,800,"Windows"))
    a.append(actor(1620,1030,"Файловая система",["Файловая система /","внешний накопитель"]))
    a.append('</svg>')
    return ''.join(a)


def node(x,y,w,h,label,kind='action',fill='#f4f8fc'):
    if kind=='decision':
        pts=f'{x+w/2},{y} {x+w},{y+h/2} {x+w/2},{y+h} {x},{y+h/2}'
        return f'<polygon points="{pts}" fill="#ffffff" stroke="#40536a" stroke-width="2.2"/>'+lines_text(x+w/2,y+h/2-4,label,16,19)
    if kind=='start':
        return f'<circle cx="{x+w/2}" cy="{y+h/2}" r="14" fill="#26364a"/>'
    if kind=='end':
        return f'<circle cx="{x+w/2}" cy="{y+h/2}" r="17" fill="#fff" stroke="#26364a" stroke-width="3"/><circle cx="{x+w/2}" cy="{y+h/2}" r="11" fill="#26364a"/>'
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="#ffffff" stroke="#315f8e" stroke-width="2.2"/>'+lines_text(x+w/2,y+h/2-7,label,16,19)


def arrow(x1,y1,x2,y2,label=None,lx=None,ly=None,dashed=False):
    dash=' stroke-dasharray="7 5"' if dashed else ''
    out=f'<path d="M {x1} {y1} L {x2} {y2}" fill="none" stroke="#26364a" stroke-width="2" marker-end="url(#arrow)"{dash}/>'
    if label:
        tx=lx if lx is not None else (x1+x2)/2
        ty=ly if ly is not None else (y1+y2)/2-8
        out+=f'<text x="{tx}" y="{ty}" text-anchor="middle" font-size="15px" font-weight="600" fill="#40536a" style="paint-order:stroke;stroke:#ffffff;stroke-width:6px;stroke-linejoin:round">{escape(label)}</text>'
    return out


def orth_arrow(points,label=None,lx=None,ly=None,dashed=False):
    d=' '.join((('M' if i==0 else 'L')+f' {x} {y}') for i,(x,y) in enumerate(points))
    dash=' stroke-dasharray="7 5"' if dashed else ''
    out=f'<path d="{d}" fill="none" stroke="#26364a" stroke-width="2" marker-end="url(#arrow)"{dash}/>'
    if label: out+=text(lx if lx is not None else points[len(points)//2][0],ly if ly is not None else points[len(points)//2][1]-8,label,15,weight="600",fill="#40536a")
    return out


def diagram_activity():
    w,h=1500,1940; a=svg_start(w,h)
    top,bottom=125,1885
    lanes=[(0,420,"Пользователь"),(420,1040,"Guardian"),(1040,1500,"USB-ключ FIDO2")]
    for x1,x2,label in lanes:
        a.append(f'<rect x="{x1}" y="{top}" width="{x2-x1}" height="{bottom-top}" fill="#ffffff" stroke="#b7c2cf" stroke-width="1.4"/>')
        a.append(text((x1+x2)/2,118,label,18,weight="700",fill="#26364a"))
    nodes=[
      ('start',185,150,50,30,[]),
      ('action',85,220,250,70,['Запустить Guardian']),
      ('action',85,335,250,82,['Ввести мастер-пароль']),
      ('action',585,455,310,82,['Проверить мастер-пароль']),
      ('action',585,575,310,82,['Запросить ответ FIDO2']),
      ('action',1105,700,330,82,['Подтвердить запрос','на USB-ключе']),
      ('action',585,825,310,82,['Проверить ответ ключа']),
      ('decision',630,945,220,115,['Оба фактора','корректны?']),
      ('action',585,1100,310,82,['Открыть локальное','хранилище']),
      ('action',85,1270,250,82,['Выбрать wallet-запись']),
      ('action',85,1380,250,82,['Явно запросить','просмотр / копирование']),
      ('action',585,1380,310,82,['Временно показать','или скопировать секрет']),
      ('action',85,1540,250,82,['Запросить блокировку','или заблокировать Windows']),
      ('action',585,1540,310,82,['Скрыть секреты; очистить','clipboard, если возможно']),
      ('end',715,1830,50,35,[]),
      ('action',85,1080,250,82,['Оставить Locked;','нейтральная ошибка'],'#fff3f0'),
      ('end',185,1200,50,35,[]),
    ]
    for nd in nodes:
        typ,x,y,ww,hh,lab,*rest=nd
        fill=rest[0] if rest else '#f4f8fc'
        a.append(node(x,y,ww,hh,lab,typ,fill))
    # Orthogonal connectors keep the paths aligned with the activity lanes.
    a.append(orth_arrow([(210,180),(210,220)]))
    a.append(orth_arrow([(210,290),(210,335)]))
    a.append(orth_arrow([(335,376),(450,376),(450,496),(585,496)]))
    a.append(orth_arrow([(740,537),(740,575)]))
    a.append(orth_arrow([(895,616),(1000,616),(1000,741),(1105,741)]))
    a.append(orth_arrow([(1105,741),(1000,741),(1000,866),(895,866)]))
    a.append(orth_arrow([(740,907),(740,945)]))
    a.append(orth_arrow([(740,1060),(740,1100)],'да',780,1080))
    a.append(orth_arrow([(630,1002),(500,1002),(500,1121),(335,1121)],'нет',460,1035))
    a.append(orth_arrow([(210,1162),(210,1200)]))
    a.append(orth_arrow([(585,1141),(450,1141),(450,1311),(335,1311)]))
    a.append(orth_arrow([(210,1352),(210,1380)]))
    a.append(orth_arrow([(335,1421),(585,1421)]))
    a.append(orth_arrow([(585,1421),(450,1421),(450,1581),(335,1581)]))
    a.append(orth_arrow([(335,1581),(585,1581)]))
    a.append(orth_arrow([(740,1622),(740,1830)]))
    a.append('</svg>')
    return ''.join(a)


def state_box(x,y,w,h,label,fill='#f4f8fc'):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="20" fill="#ffffff" stroke="#315f8e" stroke-width="2.4"/>'+lines_text(x+w/2,y+h/2-7,label,18,22,weight="600")


def diagram_state():
    w,h=1500,900; a=svg_start(w,h)
    # Edges behind states
    a.append(arrow(100,425,205,425))
    a.append(arrow(410,425,515,425,label="создать Vault",lx=465,ly=360))
    a.append(arrow(720,425,835,425,label="инициализация + ключ",lx=780,ly=360))
    a.append(arrow(1040,425,1135,425,label="запрос разблокировки",lx=1090,ly=360))
    a.append(arrow(1245,475,1245,635,label="оба фактора верны",lx=1350,ly=560))
    a.append(arrow(1135,450,1040,450,label="ошибка / отмена",lx=1090,ly=510))
    a.append(arrow(1135,675,840,675,label="ручная / Windows-блокировка",lx=985,ly=750))
    a.append(arrow(835,650,835,475,label="завершить блокировку",lx=725,ly=560))
    # states
    a.append('<circle cx="70" cy="425" r="16" fill="#26364a"/>')
    a.append(state_box(205,385,205,80,["NotCreated"]))
    a.append(state_box(515,385,205,80,["SetupPending"]))
    a.append(state_box(835,385,205,90,["Locked"], '#eef4fa'))
    a.append(state_box(1135,385,220,90,["Authenticating"], '#fff8ed'))
    a.append(state_box(1135,635,220,90,["Unlocked"], '#eef8f0'))
    a.append(state_box(625,635,215,90,["Locking"], '#f4f8fc'))
    # setup cancellation link
    a.append('<path d="M 610 385 L 610 280 L 300 280 L 300 385" fill="none" stroke="#68778a" stroke-width="1.8" stroke-dasharray="7 5" marker-end="url(#openArrow)"/>')
    a.append(text(455,238,"отмена / ошибка настройки",15,fill="#566579"))
    # terminal marker
    a.append('<path d="M 835 475 L 835 810 L 730 810" fill="none" stroke="#26364a" stroke-width="1.8" marker-end="url(#arrow)"/>')
    a.append('<circle cx="700" cy="810" r="17" fill="#fff" stroke="#26364a" stroke-width="3"/><circle cx="700" cy="810" r="11" fill="#26364a"/>')
    a.append(text(860,835,"выход приложения",15,fill="#566579"))
    a.append('</svg>')
    return ''.join(a)


def participant(cx, name_lines, y=160, bottom=1125):
    out=[f'<rect x="{cx-115}" y="{y}" width="230" height="72" rx="8" fill="#ffffff" stroke="#315f8e" stroke-width="2"/>',
         lines_text(cx,y+29,name_lines,16,20,weight="700"),
         f'<line x1="{cx}" y1="{y+72}" x2="{cx}" y2="{bottom}" stroke="#8995a5" stroke-width="1.5" stroke-dasharray="7 6"/>']
    return ''.join(out)


def msg(x1,x2,y,label,reply=False):
    dash=' stroke-dasharray="7 5"' if reply else ''
    marker='openArrow' if reply else 'arrow'
    return f'<path d="M {x1} {y} L {x2} {y}" fill="none" stroke="#26364a" stroke-width="1.8" marker-end="url(#{marker})"{dash}/>'+text((x1+x2)/2,y-9,label,15,weight="500")


def diagram_sequence():
    w,h=1800,1240; a=svg_start(w,h)
    xs=[145,430,715,1000,1285,1570]
    names=[['Пользователь'],['Guardian UI'],['VaultService'],['FIDO2Adapter'],['USB-ключ'],['CryptoProvider /','VaultStore']]
    for x,n in zip(xs,names):a.append(participant(x,n,bottom=1095))
    for x,y1,y2 in [(430,270,1060),(715,300,1040),(1000,410,755),(1285,490,680),(1570,790,875)]:
        a.append(f'<rect x="{x-7}" y="{y1}" width="14" height="{y2-y1}" fill="#ffffff" stroke="#315f8e" stroke-width="1.2"/>')
    messages=[
      (145,430,285,'1. Ввести мастер-пароль и нажать «Открыть»',False),
      (430,715,345,'2. unlock(masterPassword)',False),
      (715,715,390,'3. verifyMaster(password)',False),
      (715,1000,465,'4. requestAssertion(challenge)',False),
      (1000,1285,520,'5. challenge',False),
      (145,1285,575,'6. Подтвердить касанием (если запрошено)',False),
      (1285,1000,630,'7. signedAssertion',True),
      (1000,715,685,'8. assertionValid',True),
    ]
    for x1,x2,y,label,reply in messages:
        if x1==x2:
            a.append(f'<path d="M {x1} {y} h 55 v 22 h -45" fill="none" stroke="#26364a" stroke-width="1.7" marker-end="url(#arrow)"/>'+text(x1+34,y-8,label,14))
        else:a.append(msg(x1,x2,y,label,reply))
    a.append('<rect x="650" y="735" width="1020" height="340" rx="12" fill="#ffffff" stroke="#68778a" stroke-width="1.6"/>')
    a.append('<path d="M 650 775 L 1670 775" stroke="#68778a" stroke-width="1.2"/>')
    a.append(text(700,763,"alt",16,anchor="start",weight="700",fill="#40536a"))
    a.append(text(810,763,"оба фактора корректны",15,anchor="start",fill="#40536a"))
    a.append(msg(715,1570,820,'9. openEncryptedVault()',False))
    a.append(msg(1570,715,860,'10. vaultReady',True))
    a.append(msg(715,430,900,'11. state = Unlocked',True))
    a.append(msg(430,145,935,'Показать список без раскрытия секретов',True))
    a.append('<path d="M 650 965 L 1670 965" stroke="#68778a" stroke-width="1.2"/>')
    a.append(text(810,987,"else: неверный фактор / отмена / ошибка",15,anchor="start",fill="#8b3a31"))
    a.append(msg(715,430,1015,'genericFailure; state = Locked',True))
    a.append(msg(430,145,1045,'Показать нейтральную ошибку',True))
    a.append('</svg>')
    return ''.join(a)


DIAGRAMS={
  'use-case': diagram_usecase(),
  'activity': diagram_activity(),
  'state': diagram_state(),
  'sequence': diagram_sequence(),
}
for name, content in DIAGRAMS.items():
    svg=ROOT/f'{name}.svg'
    svg.write_text(content, encoding='utf-8')
    print(svg)
