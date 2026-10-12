# -*- coding: utf-8 -*-
"""Hoja de vida del Ing. Styp Bill Roy Canto Rondón, con el formato del curso.

Su PDF original pesa demasiado para enviarlo. El 12/10/2026 la Dra. Omidres pegó el texto
completo de esa hoja de vida y pidió armar una versión liviana con ese contenido.

Fuente única: ese texto. No se añadió nada de afuera, con una excepción marcada en rojo
para que él la confirme: su consultoría externa vigente (MEDDI hub a.s. entre otras), que
la Dra. Omidres confirmó el mismo día y que su hoja de vida solo registra hasta 12/2023.

Lo que se dejó fuera, a propósito:
  · La dirección de su domicilio: basta con la ciudad.
  · Las líneas repetidas «CIP. 131278» que llenan el final del PDF original.
  · Los cursos técnicos anteriores a 2017 y los 17 cursos de Platzi se agrupan en una
    línea, sin fechas: en el texto pegado varias columnas venían entrelazadas.

APROBADA=False pone el aviso de revisión y la nota del pie. Cuando él la apruebe, se
cambia a True y se regenera.
"""
APROBADA = False

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, Table, TableStyle)

TEAL=colors.HexColor('#0D5A62'); GOLD=colors.HexColor('#B8852B')
MINT=colors.HexColor('#C8E1DF'); PALE=colors.HexColor('#EDF5F4')
WARM=colors.HexColor('#FBF1DC'); INK=colors.HexColor('#1A2325')
MUTED=colors.HexColor('#5F7073')

st=lambda **k: ParagraphStyle(**k)
S_nom  = st(name='nom', fontName='Helvetica-Bold', fontSize=16.5, leading=19, textColor=TEAL)
S_esp  = st(name='esp', fontName='Helvetica', fontSize=8.8, leading=12, textColor=GOLD)
S_sec  = st(name='sec', fontName='Helvetica-Bold', fontSize=9.6, leading=12, textColor=colors.white)
S_txt  = st(name='txt', fontName='Helvetica', fontSize=8.5, leading=12.2, textColor=INK, alignment=TA_JUSTIFY)
S_item = st(name='item',fontName='Helvetica', fontSize=8.4, leading=11.6, textColor=INK,
            leftIndent=9, firstLineIndent=-9, spaceAfter=2.2)
S_sub  = st(name='sub', fontName='Helvetica-BoldOblique', fontSize=8.4, leading=11, textColor=TEAL,
            spaceBefore=2, spaceAfter=2)
S_aviso= st(name='aviso', fontName='Helvetica', fontSize=7.8, leading=10.8, textColor=INK)

PC='<font color="#A4161A"><b>[POR CONFIRMAR]</b></font>'
PIE=('Hoja de vida · Curso virtual SEDA' if APROBADA else
     'Hoja de vida · versión preparada por la coordinación el 12/10/2026 · pendiente de aprobación del docente')

def marco(canv, doc):
    canv.saveState()
    canv.setFillColor(TEAL); canv.rect(0, A4[1]-9*mm, A4[0], 9*mm, stroke=0, fill=1)
    canv.setFillColor(GOLD); canv.rect(0, A4[1]-10.2*mm, A4[0], 1.2*mm, stroke=0, fill=1)
    canv.setFillColor(colors.white); canv.setFont('Helvetica-Bold', 7.4)
    canv.drawString(15*mm, A4[1]-6.2*mm, 'ING. STYP BILL ROY CANTO RONDÓN')
    canv.setFont('Helvetica', 7.4)
    canv.drawRightString(A4[0]-15*mm, A4[1]-6.2*mm, 'Tecnologías de la información en salud · CIP 131278')
    canv.setStrokeColor(MINT); canv.setLineWidth(.5)
    canv.line(15*mm, 11*mm, A4[0]-15*mm, 11*mm)
    canv.setFillColor(MUTED); canv.setFont('Helvetica', 6.8)
    canv.drawString(15*mm, 7.4*mm, PIE)
    canv.drawRightString(A4[0]-15*mm, 7.4*mm, 'Página %d' % canv.getPageNumber())
    canv.restoreState()

SALIDA='SEDA_HojaVida_Canto' + ('' if APROBADA else '_REVISION')
doc=BaseDocTemplate(SALIDA+'.pdf', pagesize=A4,
    leftMargin=15*mm, rightMargin=15*mm, topMargin=15*mm, bottomMargin=14*mm,
    title='Hoja de vida — Ing. Styp Bill Roy Canto Rondón',
    author='Coordinación académica · Curso virtual SEDA')
doc.addPageTemplates([PageTemplate(id='n',
    frames=[Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='f')],
    onPage=marco)])
W=doc.width

def seccion(titulo):
    t=Table([[Paragraph(titulo, S_sec)]], colWidths=[W])
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),TEAL),
        ('LEFTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),3.4),
        ('BOTTOMPADDING',(0,0),(-1,-1),3.4)]))
    return [Spacer(1,4*mm), t, Spacer(1,2.4*mm)]

def vinetas(items):
    return [Paragraph('•&nbsp; '+i, S_item) for i in items]

def cargo(titulo, lugar, fechas):
    return Paragraph('<b>%s</b> — %s · <font color="#5F7073">%s</font>' % (titulo, lugar, fechas), S_sub)

F=[]

if not APROBADA:
    aviso=Table([[Paragraph(
        '<b>Para Styp.</b> Como tu PDF pesa demasiado para el expediente, la coordinación armó esta versión '
        'con el contenido de tu hoja de vida. Revísala, corrige lo que haga falta y confírmanos que podemos '
        'presentarla a la Universidad de Cuenca. Lo marcado en <font color="#A4161A"><b>rojo</b></font> lo '
        'añadimos nosotros y necesita tu confirmación.', S_aviso)]], colWidths=[W])
    aviso.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),WARM),('LINEBEFORE',(0,0),(0,-1),2.2,GOLD),
        ('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),
        ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
    F += [aviso, Spacer(1,5*mm)]

F += [Paragraph('Ing. Styp Bill Roy Canto Rondón', S_nom), Spacer(1,1.5*mm),
      Paragraph('Ingeniero de Telecomunicaciones · CIP 131278 · Coordinador de Tecnologías de la Información, '
                'Centro Nacional de Telemedicina (CENATE) – EsSalud · Lima, Perú', S_esp), Spacer(1,1.2*mm),
      Paragraph('<font color="#5F7073">styp611@outlook.com · (+51) 956 194 180 · www.stypcanto.com · '
                'linkedin.com/in/stypcanto · github.com/stypcanto</font>', S_txt)]

F += seccion('PERFIL PROFESIONAL')
F += [Paragraph(
    'Ingeniero con más de 13 años de experiencia, de los cuales 8 dedicados específicamente a las tecnologías '
    'de la información aplicadas a la salud. Especialista en análisis, integración y gestión de sistemas de '
    'software en entornos sanitarios, con una trayectoria liderando proyectos de tecnologías de información y '
    'comunicaciones, telemedicina, salud móvil y servicios digitales en salud, en coordinación con equipos '
    'multidisciplinarios de médicos, gestores y personal técnico. Experiencia en el ciclo completo de desarrollo '
    'de software y en la gestión de motores de bases de datos. Conocimiento de las regulaciones del sector salud '
    'y de los principios de seguridad y privacidad de la información clínica.', S_txt)]

F += seccion('FORMACIÓN PROFESIONAL')
F += vinetas(['<b>Ingeniero de Telecomunicaciones</b> — Universidad Inca Garcilaso de la Vega, Lima, Perú · 2005 – 2010',
              '<b>Colegio de Ingenieros del Perú</b> — registro CIP 131278'])

F += seccion('EXPERIENCIA PROFESIONAL')
F += [cargo('Coordinador de Equipo de Tecnologías de la Información',
            'Centro Nacional de Telemedicina (CENATE), EsSalud', '02/05/2024 – actualidad')]
F += vinetas([
    'Gestión y desarrollo de proyectos de software para servicios de telemedicina y salud digital: análisis de '
    'requerimientos, diseño, implementación, validación y despliegue.',
    'Desarrollo con Java y Spring Boot; diseño de APIs RESTful para integrar sistemas, servicios back-end y '
    'aplicaciones en React.',
    'Integración de inteligencia artificial generativa con modelos de lenguaje ejecutados en entornos locales, '
    'e integraciones mediante Model Context Protocol (MCP), evaluando los modelos según los requerimientos '
    'técnicos y de privacidad de cada solución.',
    'Modelado de sistemas con UML; bases de datos PostgreSQL, MySQL y Oracle; ciclo de desarrollo en ambientes '
    'de desarrollo, QA y producción; coordinación y supervisión del equipo técnico.',
])
if not APROBADA:
    F += [cargo('Consultor externo', 'empresas de tecnología en salud, entre ellas MEDDI hub a.s.',
                'actualidad ' + PC)]
F += [cargo('Jefe de Prácticas – Informática Biomédica',
            'Universidad Científica del Sur, Carrera de Medicina Humana', '22/08/2022 – 13/08/2023')]
F += vinetas([
    'Sesiones prácticas del curso de Informática Biomédica para estudiantes de Medicina Humana, presenciales y '
    'virtuales, con metodologías participativas y evaluación formativa.',
    'Orientación en el uso de herramientas informáticas para procesar, organizar y gestionar información en '
    'ciencias de la salud.',
])
F += [cargo('Consultor Especialista en Proyectos TI', 'MEDDI hub a.s.', '01/02/2022 – 30/12/2023')]
F += vinetas([
    'Gestión de proyectos de software para telemedicina y salud digital, en el ciclo completo, y desarrollo de '
    'una plataforma SaaS de telemedicina (Node.js, TypeScript, React, React Native).',
    'Despliegue de soluciones en instituciones de salud de Ecuador, Colombia y México, con capacitación a equipos '
    'técnicos y usuarios.',
])
F += [cargo('Especialista en Telecomunicaciones',
            'Ministerio de Salud del Perú (MINSA) — Oficina General de Tecnologías de la Información y '
            'Dirección de Telemedicina', '01/09/2014 – 31/01/2022')]
F += vinetas([
    'Liderazgo de proyectos de salud digital y telemedicina: historia clínica electrónica, conectividad '
    'hospitalaria y normativas de TI en salud.',
    'Supervisión de infraestructura tecnológica (data center, redes LAN/WAN, servidores) en hospitales nuevos a '
    'nivel nacional.',
    'Soporte y optimización de plataformas nacionales: eQhali, SIHCE, Wawared, HIS, SISGALEN Plus, Teleatiendo, '
    'Certificado de Nacido Vivo Electrónico, SINADEF, PACS/RIS y Openclinic.',
    'Participación en la formulación, actualización y difusión de normas técnicas de tecnologías de la '
    'información en salud.',
])
F += [cargo('Ingeniero en redes de telecomunicaciones', 'CGTEL · AENOR Perú · Constructel (servicios para Telefónica)',
            '09/2010 – 05/2014')]
F += vinetas(['Redes móviles 2G/3G, redes WAN y LAN, banda ancha corporativa y migraciones en entornos MPLS.'])

F += seccion('ESPECIALIZACIONES')
F += vinetas([
    '<b>Programa de Capacitación en Inteligencia de Datos para preparación ante Pandemias y Epidemias</b> — '
    'Universidad Continental, Lima, Perú · 2021',
    '<b>Diplomado en Tecnologías de la Información y Telecomunicaciones</b>, mención en Planificación, Gestión de '
    'Redes y Regulación de Telecomunicaciones — Instituto Nacional de Investigación y Capacitación de '
    'Telecomunicaciones, Lima, Perú · 2021',
    '<b>Diplomado en Telecomunicaciones y Tecnologías de la Información</b>, mención en Sistemas de Comunicaciones '
    'Móviles de Última Generación 4G LTE – 5G — Instituto Nacional de Investigación y Capacitación de '
    'Telecomunicaciones, Lima, Perú · 2019',
    '<b>Curso de Formação em Telessaúde para América Latina</b> — Universidade Federal de Minas Gerais, '
    'Belo Horizonte, Brasil · 2019',
    '<b>Curso Modelos operativos para la Teleconsulta en Telemedicina</b> — Centro Nacional de Excelencia '
    'Tecnológica, México · 2018',
    '<b>Programa de Capacitación en Telemedicina</b> — Gachon University Gil Medical Center, Incheon, '
    'Corea del Sur · 2017',
])

F += seccion('FORMACIÓN CONTINUA EN SALUD DIGITAL')
F += vinetas([
    'Transformación Digital para el Personal de Salud — OPS · 24/10/2025 (20 horas)',
    'Integración de la telesalud en el primer nivel de atención con la aplicación de modelos de simulación — '
    'OPS · 22/09/2025 (40 horas)',
    'Introducción a la Interoperabilidad y al estándar FHIR — Campus Virtual de Salud Pública, OPS · '
    '18/03/2024 (20 horas)',
    'Especialización en Salud Digital: Planificación de Sistemas Nacionales — CENS, Chile · 25/05/2023 (33 horas)',
    'Introducción a la Telemedicina y Telesalud — Organización Internacional de Telemedicina y Telesalud · '
    '14/10/2022 (36 horas)',
    'Curso Especializado en TIC en Salud — Telemedicina Perú · 01/06/2022 (32 horas)',
    'Reunión Técnica Nacional de Telemedicina – Telesalud — Dirección de Telemedicina de la Dirección General de '
    'Telesalud, Referencia y Urgencia, Lima · 14–15/12/2017 (16 horas)',
])

F += seccion('FORMACIÓN CONTINUA EN TECNOLOGÍA Y GESTIÓN')
F += vinetas([
    'Angular Frontend Developer — TecyLab · 18/08/2026 (37 horas)',
    'Desarrollo de Soluciones Azure — Ingenium · 15/07/2026 (57 horas)',
    'JAVA 17 Desarrollo Backend — CIBERTEC · 03/10/2025 – 14/11/2025 (82,7 horas)',
    'JAVA 17 Web Developer — CIBERTEC · 30/06/2025 – 15/08/2025 (80 horas)',
    'Especialista en Base de Datos SQL Server &amp; MySQL — Cámara de Comercio de Lima · 05/01/2025 – 28/03/2025 (150 horas)',
    'Desarrollo Web Fullstack con Java (Spring Boot y React) — CodiGO TECSUP · 30/08/2024 – 17/02/2025 (240 horas)',
    'Scrum Master — ADIESTRA (18 horas) · Scrum Foundation Professional Certificate — CertiProf · '
    'Scrum Fundamental Certified — SCRUMstudy · 2021',
    'Transformación Digital en las Organizaciones — Centro de Informática, Universidad Nacional Mayor de '
    'San Marcos · 2019 (40 horas)',
    'Curso de Especialización en Gestión de Políticas Públicas — Universidad Tecnológica del Perú · 2018 (90 horas)',
    'Programación Multianual y Formulación de Proyectos de Inversión Pública – Invierte.pe — Universidad San '
    'Martín de Porres · 2018 (64 horas)',
    'Project Management for Professionals, 5th Edition — New Horizons · 2016 (48 horas)',
    'Otros: ITIL Foundations (ISIL TECH), Cisco Certified Network Associate (CCNA), Linux Essentials y Linux '
    'Administrador LPIC-1 (Centro Nacional de Seguridad Digital), 17 cursos de desarrollo de software en Platzi '
    '(2023) y cursos de redes, telefonía IP y seguridad perimetral.',
])

F += seccion('COMPETENCIAS TÉCNICAS')
F += vinetas([
    '<b>Interoperabilidad en salud:</b> HL7 FHIR.',
    '<b>Lenguajes y frameworks:</b> Java 17, Spring Boot, JavaScript, TypeScript, Python, PHP, Node.js '
    '(Express, NestJS), FastAPI, React, Angular.',
    '<b>Bases de datos y nube:</b> PostgreSQL, MySQL, Oracle, SQL Server, Redis · Docker, Azure Functions, '
    'AWS Lambda, GitHub Actions.',
    '<b>Seguridad:</b> autenticación y autorización con JWT, Spring Security.',
    '<b>Inteligencia artificial:</b> integración de modelos de lenguaje en productos, agentes, RAG y diseño de '
    'prompts.',
    '<b>Metodologías:</b> Scrum, Kanban, Design Thinking.',
])

F += seccion('DISTINCIONES Y MEMBRESÍAS')
F += vinetas([
    '<b>Presidente y fundador</b> — HL7 Perú',
    '<b>Miembro vocal y fundador</b> — Organización Internacional de Telemedicina y Telesalud (Ecuador)',
    '<b>Miembro del Comité Especializado en Tecnologías para la Salud</b> — Colegio de Ingenieros del Perú',
    '<b>Miembro de la Comisión de Sociedad Digital</b> — Colegio de Ingenieros del Perú',
    '<b>Miembro asociado</b> — Asociación Iberoamericana de Telesalud y Telemedicina',
])

F += seccion('DOCENCIA EN ESTE CURSO')
F += vinetas([
    '<b>Curso virtual de actualización en obesidad, diabetes, nutrición clínica y salud digital</b> — '
    'Sociedad de Endocrinología y Diabetes del Austro (SEDA), Ecuador. Módulo 7 · Clase 4: '
    '<i>Implementación, ética y seguridad de datos</i>.',
])

F_word=list(F)   # doc.build vacía la lista
doc.build(F)

# ---------- versión Word, editable, con el mismo contenido ----------
import re
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def _rgb(h): h=h.lstrip('#'); return RGBColor(int(h[:2],16), int(h[2:4],16), int(h[4:],16))

def _sombra(par, color):
    pPr=par._p.get_or_add_pPr(); shd=OxmlElement('w:shd')
    shd.set(qn('w:val'),'clear'); shd.set(qn('w:color'),'auto'); shd.set(qn('w:fill'),color)
    pPr.append(shd)

def _runs(par, marca, size, color='1A2325', negrita=False):
    """Convierte el marcado de reportlab (<b>, <i>, <font color>) en runs de Word."""
    marca=marca.replace('&nbsp;',' ').replace('•  ','').replace('&amp;','&')
    estado={'b':negrita,'i':False,'c':[color]}
    for trozo in re.split(r'(<[^>]+>)', marca):
        if not trozo: continue
        t=trozo.lower()
        if t=='<b>': estado['b']=True; continue
        if t=='</b>': estado['b']=negrita; continue
        if t=='<i>': estado['i']=True; continue
        if t=='</i>': estado['i']=False; continue
        m=re.match(r'<(?:font|link)[^>]*color="#?([0-9A-Fa-f]{6})"', trozo)
        if m: estado['c'].append(m.group(1)); continue
        if t.startswith('<font') or t.startswith('<link'): estado['c'].append(estado['c'][-1]); continue
        if t in ('</font>','</link>'): estado['c'].pop(); continue
        if trozo.startswith('<'): continue
        r=par.add_run(trozo); r.bold=estado['b']; r.italic=estado['i']
        r.font.size=Pt(size); r.font.color.rgb=_rgb(estado['c'][-1]); r.font.name='Arial'

wd=Document()
for sec in wd.sections:
    sec.top_margin=sec.bottom_margin=Cm(1.6); sec.left_margin=sec.right_margin=Cm(1.8)
    _runs(sec.header.paragraphs[0], '<b>ING. STYP BILL ROY CANTO RONDÓN</b>   ·   CIP 131278', 8, '0D5A62')
    _runs(sec.footer.paragraphs[0], PIE, 7.5, '5F7073')

def _par(antes=0, despues=3):
    q=wd.add_paragraph(); q.paragraph_format.space_before=Pt(antes)
    q.paragraph_format.space_after=Pt(despues); return q

for fl in F_word:
    if isinstance(fl, Table):
        par_rl=fl._cellvalues[0][0]
        if not isinstance(par_rl, Paragraph): par_rl=par_rl[0]
        if par_rl.style.name=='sec':
            q=_par(9,4); q.paragraph_format.keep_with_next=True; _sombra(q,'0D5A62'); _runs(q, ' '+par_rl.text, 10, 'FFFFFF', True)
        else:
            q=_par(0,8); _sombra(q,'FBF1DC'); _runs(q, par_rl.text, 8.5)
    elif isinstance(fl, Paragraph):
        n=fl.style.name
        if n=='nom': _runs(_par(0,1), fl.text, 18, '0D5A62', True)
        elif n=='esp': _runs(_par(0,4), fl.text, 9.5, 'B8852B')
        elif n=='sub':
            q=_par(4,2); q.paragraph_format.keep_with_next=True; _runs(q, fl.text, 9, '0D5A62')
        elif n=='item':
            q=wd.add_paragraph(style='List Bullet'); q.paragraph_format.space_after=Pt(3)
            _runs(q, fl.text, 9)
        else:
            q=_par(0,4); q.alignment=WD_ALIGN_PARAGRAPH.JUSTIFY; _runs(q, fl.text, 9)
wd.core_properties.title='Hoja de vida — Ing. Styp Bill Roy Canto Rondón'
wd.core_properties.author='Coordinación académica · Curso virtual SEDA'
wd.save(SALIDA+'.docx')
print(SALIDA, 'generado')
