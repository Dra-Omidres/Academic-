# -*- coding: utf-8 -*-
"""BORRADOR de hoja de vida de la Dra. Adriana Mabel Álvarez para el expediente del aval.

La docente no envió su hoja de vida. La Dra. Omidres pidió armarla con lo que ella
mandó y con lo que se encontrara en línea (10/10/2026). Fuentes:

  · Cargos en sociedades: los envió la Dra. Omidres el 10/10/2026, transcritos de la
    docente. No se encontraron en línea, así que no están verificados de forma externa.
  · Publicaciones: PubMed, consultado el 10/10/2026. Se separan en dos grupos:
      CONFIRMADAS  — firma «Adriana» o «Adriana Mabel» Álvarez con afiliación al
                     Hospital Italiano de Buenos Aires (HIBA).
      PROBABLES    — firma solo «Alvarez A» con afiliación al HIBA. Muy posiblemente
                     son suyas, pero el nombre no lo demuestra: se le preguntan a ella.
  · Formación académica: no se encontró nada verificable. Queda POR CONFIRMAR.

Este documento NO va al expediente hasta que la Dra. Álvarez lo revise y lo apruebe:
es su hoja de vida y la firma de la Universidad se la atribuye a ella.
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, Table, TableStyle, KeepTogether)

TEAL=colors.HexColor('#0D5A62'); GOLD=colors.HexColor('#B8852B')
MINT=colors.HexColor('#C8E1DF'); PALE=colors.HexColor('#EDF5F4')
WARM=colors.HexColor('#FBF1DC'); INK=colors.HexColor('#1A2325')
MUTED=colors.HexColor('#5F7073'); ROJO=colors.HexColor('#A4161A')

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
S_pc   = st(name='pc', fontName='Helvetica-Bold', fontSize=8.4, leading=11.6, textColor=ROJO,
            leftIndent=9, firstLineIndent=-9)

PC='<font color="#A4161A"><b>[POR CONFIRMAR]</b></font>'

def marco(canv, doc):
    canv.saveState()
    canv.setFillColor(TEAL); canv.rect(0, A4[1]-9*mm, A4[0], 9*mm, stroke=0, fill=1)
    canv.setFillColor(GOLD); canv.rect(0, A4[1]-10.2*mm, A4[0], 1.2*mm, stroke=0, fill=1)
    canv.setFillColor(colors.white); canv.setFont('Helvetica-Bold', 7.4)
    canv.drawString(15*mm, A4[1]-6.2*mm, 'DRA. ADRIANA MABEL ÁLVAREZ')
    canv.setFont('Helvetica', 7.4)
    canv.drawRightString(A4[0]-15*mm, A4[1]-6.2*mm, 'Endocrinología · Diabetes · Obesidad · MASLD')
    # marca de agua de borrador
    canv.setFillColor(colors.Color(.64,.09,.10,alpha=.07)); canv.setFont('Helvetica-Bold', 82)
    canv.translate(A4[0]/2, A4[1]/2); canv.rotate(35)
    canv.drawCentredString(0, 0, 'BORRADOR')
    canv.restoreState(); canv.saveState()
    canv.setStrokeColor(MINT); canv.setLineWidth(.5)
    canv.line(15*mm, 11*mm, A4[0]-15*mm, 11*mm)
    canv.setFillColor(MUTED); canv.setFont('Helvetica', 6.8)
    canv.drawString(15*mm, 7.4*mm, 'Hoja de vida · BORRADOR del 10 de octubre de 2026 · pendiente de aprobación por la docente')
    canv.drawRightString(A4[0]-15*mm, 7.4*mm, 'Página %d' % canv.getPageNumber())
    canv.restoreState()

doc=BaseDocTemplate('SEDA_HojaVida_Alvarez_BORRADOR.pdf', pagesize=A4,
    leftMargin=15*mm, rightMargin=15*mm, topMargin=15*mm, bottomMargin=14*mm,
    title='Hoja de vida (borrador) — Dra. Adriana Mabel Álvarez',
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

def vinetas(items, estilo=S_item):
    return [Paragraph('•&nbsp; '+i, estilo) for i in items]

def doi(d):
    return 'doi: <link href="https://doi.org/%s" color="#0D5A62">%s</link>' % (d, d)

F=[]

# ---------- aviso para la docente ----------
aviso=Table([[Paragraph(
    '<b>Para la Dra. Álvarez.</b> Este borrador lo preparó la coordinación académica del curso '
    'con los datos que usted nos hizo llegar y con sus publicaciones indexadas en PubMed. '
    'Le pedimos que lo revise: corrija lo que haga falta, complete lo marcado como '
    '<font color="#A4161A"><b>POR CONFIRMAR</b></font> y confírmenos que podemos presentarlo '
    'en su nombre a la Universidad de Cuenca.', S_aviso)]], colWidths=[W])
aviso.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),WARM),('LINEBEFORE',(0,0),(0,-1),2.2,GOLD),
    ('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),
    ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
F += [aviso, Spacer(1,5*mm)]

# ---------- portada ----------
F += [Paragraph('Dra. Adriana Mabel Álvarez', S_nom), Spacer(1,1.5*mm),
      Paragraph('Médica endocrinóloga · Hospital Italiano de Buenos Aires · Buenos Aires, Argentina', S_esp)]

F += seccion('PERFIL PROFESIONAL')
F += [Paragraph(
    'Médica endocrinóloga con actividad asistencial y de investigación en el Hospital Italiano de '
    'Buenos Aires. Su trabajo publicado abarca la diabetes tipo 1 y tipo 2, la relación entre '
    'diabetes y depresión, el sueño en la diabetes tipo 1 y, en los últimos años, la enfermedad '
    'hepática esteatósica asociada a disfunción metabólica (MASLD) en personas con diabetes tipo 2. '
    'Participa en los grupos de trabajo sobre obesidad y esteatosis hepática de la Asociación '
    'Latinoamericana de Diabetes (ALAD) y de la Sociedad Argentina de Diabetes (SAD).', S_txt)]

F += seccion('CARGO ACTUAL')
F += vinetas([
    '<b>Médica endocrinóloga</b> — Unidad de Endocrinología, Departamento de Medicina General, '
    'Hospital Italiano de Buenos Aires (HIBA), Buenos Aires, Argentina.',
])

F += seccion('SOCIEDADES CIENTÍFICAS Y CARGOS')
F += vinetas([
    '<b>Coordinadora del Grupo de Trabajo Obesidad-MASH</b> — Asociación Latinoamericana de Diabetes (ALAD).',
    '<b>Vocal de la Región Sur</b> — Asociación Latinoamericana de Diabetes (ALAD).',
    '<b>Miembro del Comité de Esteatosis Hepática Metabólica</b> — Sociedad Argentina de Diabetes (SAD).',
])

F += seccion('FORMACIÓN ACADÉMICA')
F += [Paragraph('•&nbsp; Título de médica — universidad y año ' + PC, S_item),
      Paragraph('•&nbsp; Especialidad en Endocrinología — institución y año ' + PC, S_item),
      Paragraph('•&nbsp; Otros posgrados, maestrías o certificaciones ' + PC, S_item)]

F += seccion('PUBLICACIONES INDEXADAS (PubMed)')
F += [Paragraph('Confirmadas', S_sub)]
F += vinetas([
    'Suarez B, Álvarez AM, Mascardi MF, Ramos ALM, Woo DH, Gutiérrez MM, et al. Interactions between '
    'the gut microbiome and genetic and clinical risk factors for metabolic dysfunction-associated '
    'steatotic liver disease (MASLD) in patients with type 2 diabetes mellitus from different '
    'geographical regions of Argentina. <i>Life (Basel)</i>. 2026;16(2):283. ' + doi('10.3390/life16020283'),
    'Valiensi SM, Folgueira AL, Diez JJ, Gonzalez-Cardozo A, Vera VA, Camji JM, Alvarez AM. Is being a '
    'lark healthier for patients with type 1 diabetes mellitus? <i>Sleep Sci</i>. 2023;16(1):75-83. '
    + doi('10.1055/s-0043-1767749'),
    'Alvarez A, Faccioli J, Guinzbourg M, Castex MM, Bayón C, Masson W, et al. Endocrine and '
    'inflammatory profiles in type 2 diabetic patients with and without major depressive disorder. '
    '<i>BMC Res Notes</i>. 2013;6:61. ' + doi('10.1186/1756-0500-6-61'),
])
F += [Spacer(1,1.5*mm),
      Paragraph('Probables — firmadas como «Alvarez A», Hospital Italiano de Buenos Aires ' + PC, S_sub)]
F += vinetas([
    'Lloyd CE, Sartorius N, Ahmed HU, Alvarez A, Bahendeka S, Bobrov AE, et al. Factors associated with '
    'the onset of major depressive disorder in adults with type 2 diabetes living in 12 different '
    'countries: results from the INTERPRET-DD prospective study. <i>Epidemiol Psychiatr Sci</i>. '
    '2020;29:e134. ' + doi('10.1017/S2045796020000438'),
    'Lloyd CE, Nouwen A, Sartorius N, Ahmed HU, Alvarez A, Bahendeka S, et al. Prevalence and correlates '
    'of depressive disorders in people with type 2 diabetes: results from the International Prevalence '
    'and Treatment of Diabetes and Depression (INTERPRET-DD) study, a collaborative study carried out '
    'in 14 countries. <i>Diabet Med</i>. 2018;35(6):760-9. ' + doi('10.1111/dme.13611'),
    'Lloyd CE, Sartorius N, Cimino LC, Alvarez A, Guinzbourg de Braude M, Rabbani G, et al. The '
    'INTERPRET-DD study of diabetes and depression: a protocol. <i>Diabet Med</i>. 2015;32(7):925-34. '
    + doi('10.1111/dme.12719'),
    'Litwak LE, Mileo Vaglio R, Alvarez A, Gutman RA. [Self monitoring of capillary blood glucose. '
    'Evaluation of long-term results (3 to 7 years)]. <i>Medicina (B Aires)</i>. 1999;59(1):71-8. '
    'Spanish.',
    'Litwak LE, Mileo Vaglio R, Fried T, De Sancho H, Alvarez A, Althabe O, et al. [Intensified insulin '
    'therapy in the management of gestational diabetes]. <i>Medicina (B Aires)</i>. 1992;52(6):523-33. '
    'Spanish.',
])

F += seccion('DOCENCIA EN ESTE CURSO')
F += vinetas([
    '<b>Curso virtual de actualización en obesidad, diabetes, nutrición clínica y salud digital</b> — '
    'Sociedad de Endocrinología y Diabetes del Austro (SEDA), Ecuador. Módulo 6 · Clase 4: '
    '<i>MASLD y complicaciones metabólicas</i>.',
])

F += [Spacer(1,4*mm),
      Paragraph('<font color="#5F7073" size="7.2">Fuentes de este borrador: datos aportados por la '
                'docente a la coordinación académica (cargo y sociedades) y registros de PubMed '
                'consultados el 10/10/2026 (publicaciones).</font>', S_txt)]

doc.build(F)
print('generado')
