# -*- coding: utf-8 -*-
"""Programa académico del curso, en PDF, para anclar en el grupo de ponentes."""
import io, json, re
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, Table, TableStyle, KeepTogether, PageBreak)

TEAL   = colors.HexColor('#0D5A62')
TEAL2  = colors.HexColor('#094247')
GOLD   = colors.HexColor('#B8852B')
MINT   = colors.HexColor('#C8E1DF')
PALE   = colors.HexColor('#EDF5F4')
INK    = colors.HexColor('#1A2325')
MUTED  = colors.HexColor('#5F7073')

ENTREGA = {'M1':'jueves 29 de octubre','M2':'jueves 29 de octubre','M3':'jueves 5 de noviembre',
           'M4':'jueves 12 de noviembre','M5':'jueves 19 de noviembre','M6':'jueves 26 de noviembre',
           'M7':'jueves 3 de diciembre'}
PUBLICA = {'M1':'5 de noviembre','M2':'5 de noviembre','M3':'12 de noviembre','M4':'19 de noviembre',
           'M5':'26 de noviembre','M6':'3 de diciembre','M7':'10 de diciembre'}

CL = {c['cod']: c for c in json.load(open('/tmp/clases.json'))}
ns = {}
exec(io.open('generador-delimitacion.py', encoding='utf-8').read().split('# ---------- generación')[0], ns)
D = ns['D']


NOM = re.compile(r'\s*\(?\b(?:Dr\.|Dra\.|Lcda\.|Lcdo\.)\s+[A-ZÁÉÍÓÚÑ][^,.;:—()]*\)?')
def sin_nombres(t):
    """El programa se publica sin nombres: deja solo el código de la clase."""
    t = re.sub(r'^ATENCIÓN\s*—\s*', '', t)        # marca interna, no va en el programa
    t = re.sub(r',' + NOM.pattern, '', t)          # «M1 · C2, Dr. Pablo Vanegas»
    t = NOM.sub('', t)                              # «(Dra. Lizbet Ruilova)»
    t = (t.replace('Él los cubre', 'Esa clase los cubre')
           .replace('Ella da los fundamentos del método', 'Esa clase da los fundamentos del método')
           .replace('Ella da la lectura clínica', 'Esa clase da la lectura clínica')
           .replace('Ellas dan el método diagnóstico', 'Esas clases dan el método diagnóstico'))
    t = re.sub(r'\s{2,}', ' ', t)
    t = re.sub(r'\s+([,.;:])', r'\1', t)
    t = re.sub(r'\(\s*\)', '', t)
    t = re.sub(r'\s*y\s*$', '', t.strip())
    return t.strip(' ,;')

S = lambda **k: ParagraphStyle(**k)
st_tit   = S(name='t',  fontName='Helvetica-Bold', fontSize=21, leading=25, textColor=TEAL)
st_sub   = S(name='s',  fontName='Helvetica', fontSize=11.5, leading=16, textColor=MUTED)
st_mod   = S(name='m',  fontName='Helvetica-Bold', fontSize=13, leading=16, textColor=colors.white)
st_modd  = S(name='md', fontName='Helvetica', fontSize=9, leading=12, textColor=MINT)
st_cod   = S(name='c',  fontName='Helvetica-Bold', fontSize=8.5, leading=11, textColor=GOLD)
st_tema  = S(name='te', fontName='Helvetica-Bold', fontSize=12, leading=14.5, textColor=TEAL)
st_pon   = S(name='p',  fontName='Helvetica-Oblique', fontSize=9, leading=12, textColor=MUTED)
st_lab   = S(name='l',  fontName='Helvetica-Bold', fontSize=7.5, leading=10, textColor=MUTED)
st_txt   = S(name='x',  fontName='Helvetica', fontSize=9.3, leading=13, textColor=INK, alignment=TA_JUSTIFY)
st_li    = S(name='li', fontName='Helvetica', fontSize=9.3, leading=13, textColor=INK,
             leftIndent=9, bulletIndent=1, spaceAfter=1.5)
st_no    = S(name='n',  fontName='Helvetica', fontSize=8.8, leading=12, textColor=MUTED,
             leftIndent=9, bulletIndent=1, spaceAfter=1.5)
st_pie   = S(name='pi', fontName='Helvetica', fontSize=7.5, leading=10, textColor=MUTED)

def encabezado(canv, doc):
    canv.saveState()
    if doc.page > 1:
        canv.setFillColor(PALE); canv.rect(0, A4[1]-13*mm, A4[0], 13*mm, stroke=0, fill=1)
        canv.setFillColor(MUTED); canv.setFont('Helvetica', 7.5)
        canv.drawString(18*mm, A4[1]-8.6*mm,
                        'Curso virtual SEDA · Obesidad, diabetes, nutrición clínica y salud digital')
        canv.drawRightString(A4[0]-18*mm, A4[1]-8.6*mm, 'Página %d' % doc.page)
    canv.setStrokeColor(MINT); canv.setLineWidth(.6)
    canv.line(18*mm, 13*mm, A4[0]-18*mm, 13*mm)
    canv.setFillColor(MUTED); canv.setFont('Helvetica', 7)
    canv.drawString(18*mm, 9*mm, 'Sociedad de Endocrinología y Diabetes del Austro · SEDA')
    canv.drawRightString(A4[0]-18*mm, 9*mm, 'Versión del 29 de septiembre de 2026')
    canv.restoreState()

doc = BaseDocTemplate('SEDA_Programa_Academico.pdf', pagesize=A4,
                      leftMargin=18*mm, rightMargin=18*mm, topMargin=19*mm, bottomMargin=17*mm,
                      title='Programa académico · Curso virtual SEDA',
                      author='Sociedad de Endocrinología y Diabetes del Austro')
doc.addPageTemplates([PageTemplate(id='n',
    frames=[Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='f')],
    onPage=encabezado)])

F = []
# ---------- portada ----------
F += [Spacer(1, 22*mm),
      Paragraph('Curso virtual de actualización en<br/>obesidad, diabetes, nutrición clínica<br/>y salud digital', st_tit),
      Spacer(1, 6*mm),
      Paragraph('Sociedad de Endocrinología y Diabetes del Austro · SEDA<br/>'
                'Aval académico de la Universidad de Cuenca, en trámite', st_sub),
      Spacer(1, 9*mm)]
datos = [['Modalidad', 'Virtual, en saludelearning.com'],
         ['Duración', 'Del 5 de noviembre al 17 de diciembre de 2026'],
         ['Estructura', '7 módulos · 28 clases grabadas de 30 minutos'],
         ['Dirigido a', 'Médicos generales y especialistas, nutricionistas y otros\nprofesionales de la salud'],
         ['Cuerpo docente', 'Especialistas de Ecuador, México, Costa Rica, Perú,\nArgentina y Colombia'],
         ['Coordinación', 'Dra. Lizbet Ruilova y Dr. Pablo Vanegas'],
         ['Organización docente', 'Dra. Omidres Pérez de Carvelli']]
t = Table([[Paragraph(a, st_lab), Paragraph(b.replace('\n','<br/>'), st_txt)] for a, b in datos],
          colWidths=[35*mm, doc.width-35*mm])
t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),
                       ('BOTTOMPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),6),
                       ('LINEBELOW',(0,0),(-1,-2),.4,MINT)]))
F += [t, Spacer(1, 10*mm)]

nota = ('<b>Para qué sirve este documento.</b> Cada ponente encuentra aquí su clase, los contenidos '
        'que el programa declara y, sobre todo, qué temas cubren las clases vecinas. Son 28 clases '
        'que se graban por separado y que el participante ve seguidas: si dos ponentes desarrollan '
        'lo mismo, quien se ve en segundo lugar queda repetido sin haber hecho nada mal. '
        'Por eso cada clase lleva un apartado con lo que no le corresponde y con quién lo cubre.<br/><br/>'
        'Si al preparar su clase cree que un límite está mal puesto, escriba a la coordinación y se ajusta. '
        'Es mejor acomodarlo ahora que cuando la clase ya esté grabada.')
t2 = Table([[Paragraph(nota, st_txt)]], colWidths=[doc.width])
t2.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),PALE),
                        ('LEFTPADDING',(0,0),(-1,-1),11),('RIGHTPADDING',(0,0),(-1,-1),11),
                        ('TOPPADDING',(0,0),(-1,-1),10),('BOTTOMPADDING',(0,0),(-1,-1),10),
                        ('LINEBEFORE',(0,0),(0,-1),2.5,GOLD)]))
F += [t2, PageBreak()]

# ---------- módulos y clases ----------
mod_actual = None
for cod, c in CL.items():
    m = cod.split(' · ')[0]
    if c['modulo'] != mod_actual:
        mod_actual = c['modulo']
        cab = Table([[Paragraph(mod_actual, st_mod)],
                     [Paragraph('Entrega de las grabaciones: %s&nbsp;&nbsp;·&nbsp;&nbsp;se publica el %s'
                                % (ENTREGA[m], PUBLICA[m]), st_modd)]], colWidths=[doc.width])
        cab.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),TEAL2),
                                 ('LEFTPADDING',(0,0),(-1,-1),12),('RIGHTPADDING',(0,0),(-1,-1),12),
                                 ('TOPPADDING',(0,0),(0,0),9),('BOTTOMPADDING',(0,-1),(-1,-1),9),
                                 ('TOPPADDING',(0,1),(-1,1),1),('BOTTOMPADDING',(0,0),(-1,0),2)]))
        F += [Spacer(1, 3*mm), cab, Spacer(1, 4*mm)]

    si, no = D[cod]
    bloque = [Paragraph(cod.replace(' · C', ' · CLASE '), st_cod),
              Paragraph(c['tema'], st_tema),
              Paragraph('30 minutos grabados&nbsp;&nbsp;·&nbsp;&nbsp;entrega de la grabación: %s'
                        % ENTREGA[m], st_pon),
              Spacer(1, 2.5*mm),
              Paragraph('CONTENIDOS DECLARADOS EN EL PROGRAMA', st_lab),
              Paragraph(c['cont'], st_txt),
              Spacer(1, 2.5*mm),
              Paragraph('CÓMO ENFOCARLA', st_lab)]
    bloque += [Paragraph(x, st_li, bulletText='•') for x in si]
    bloque += [Spacer(1, 2.5*mm), Paragraph('QUÉ NO ABORDAR, Y DÓNDE SE CUBRE', st_lab)]
    bloque += [Paragraph('<b>%s</b> — %s' % (sin_nombres(q), sin_nombres(quien)), st_no, bulletText='–')
               for q, quien in no]
    caja = Table([[bloque]], colWidths=[doc.width])
    caja.setStyle(TableStyle([('LEFTPADDING',(0,0),(-1,-1),11),('RIGHTPADDING',(0,0),(-1,-1),11),
                              ('TOPPADDING',(0,0),(-1,-1),9),('BOTTOMPADDING',(0,0),(-1,-1),9),
                              ('BOX',(0,0),(-1,-1),.5,MINT),('VALIGN',(0,0),(-1,-1),'TOP')]))
    F += [KeepTogether([caja, Spacer(1, 3.5*mm)])]

# ---------- cierre ----------
F += [PageBreak(), Paragraph('Lo que necesitamos de cada ponente', st_tit), Spacer(1, 5*mm)]
req = [('La grabación','30 minutos, en la plantilla institucional del curso. Se graba por Zoom: la '
        'coordinación envía el enlace y se acuerda día y hora con cada quien.'),
       ('Para el expediente del aval','Hoja de vida resumida, cédula o pasaporte, una fotografía '
        'profesional y la declaración de conflicto de interés firmada. A info@draomidresperez.com.'),
       ('En la presentación','Tres diapositivas obligatorias: portada, datos del ponente y declaración '
        'de conflicto de interés. Denominación genérica de los medicamentos, sin marcas comerciales. '
        'Un caso clínico anonimizado. Bibliografía en formato Vancouver, con fuentes reales e indexadas.'),
       ('La participación','Es ad honorem para todo el cuerpo docente. Cada ponente recibe certificado '
        'de docente.')]
t3 = Table([[Paragraph(a, st_lab), Paragraph(b, st_txt)] for a, b in req],
           colWidths=[38*mm, doc.width-38*mm])
t3.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),
                        ('BOTTOMPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),8),
                        ('LINEBELOW',(0,0),(-1,-2),.4,MINT)]))
F += [t3, Spacer(1, 10*mm),
      Paragraph('Coordinación académica: Dra. Lizbet Ruilova y Dr. Pablo Vanegas<br/>'
                'Organización del cuerpo docente: Dra. Omidres Pérez de Carvelli · '
                'info@draomidresperez.com', st_pie)]

doc.build(F)
print('PDF generado · clases:', len(CL))
