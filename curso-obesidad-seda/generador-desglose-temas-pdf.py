# -*- coding: utf-8 -*-
"""Desglose de las 28 clases para todos los docentes: tema, docente, fecha tope de entrega,
lo que le toca y lo que no, con quién lo cubre.

Lo pidió la Dra. Omidres el 13/10/2026, después de que la Dra. Bermeo preguntara qué tenía
que cubrir: que cada docente sepa cuándo, cómo y qué puntos tocar, y que no choquen.

Fuentes:
  · El tema, los contenidos declarados y el docente salen de la hoja «Matriz 28 clases».
  · El nombre completo de cada docente sale de «Ponentes - datos aval».
  · Lo que sí y lo que no toca cada clase sale del diccionario D de generador-delimitacion.py,
    que es lo que ya se acordó con cada docente. Ese diccionario traía nombres fijos que
    quedaron viejos (por ejemplo, M4 · C1 a nombre de la Dra. Astudillo): aquí el nombre se
    reemplaza por el que la matriz tiene hoy para esa clase.

Es un documento para repartir: no lleva teléfonos, correos ni ningún otro dato personal.

Salida: SEDA_Desglose_Temas_Docentes.pdf
"""
import re, unicodedata, datetime, openpyxl
from difflib import SequenceMatcher
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
                                Table, TableStyle, KeepTogether, Image, PageBreak)

TEAL=colors.HexColor('#0D5A62'); GOLD=colors.HexColor('#B8852B')
MINT=colors.HexColor('#C8E1DF'); PALE=colors.HexColor('#EDF5F4')
WARM=colors.HexColor('#FBF1DC'); INK=colors.HexColor('#1A2325'); MUTED=colors.HexColor('#5F7073')
ROJO=colors.HexColor('#A3342B')

FECHAS={'M1':'jueves 29 de octubre de 2026','M2':'jueves 29 de octubre de 2026',
        'M3':'jueves 5 de noviembre de 2026','M4':'jueves 12 de noviembre de 2026',
        'M5':'jueves 19 de noviembre de 2026','M6':'jueves 26 de noviembre de 2026',
        'M7':'jueves 3 de diciembre de 2026'}

# ---------- lo acordado con cada docente ----------
_src=open('generador-delimitacion.py', encoding='utf-8').read()
_ns={}; exec(_src[_src.index('D = {'):_src.index('# ---------- generación')], _ns)
D=_ns['D']

# ---------- matriz ----------
wb=openpyxl.load_workbook('SEDA_Matriz_Ponentes_Curso_Obesidad.xlsx')
m=wb['Matriz 28 clases']; p=wb['Ponentes - datos aval']

TITULOS={'dr','dra','lcda','lcdo','ing','msc','m','sc','mg','mgtr','de','del','la','y'}
def tokens(s):
    s=unicodedata.normalize('NFKD', str(s)).encode('ascii','ignore').decode().lower()
    return {t for t in re.findall(r'[a-z]+', s) if t not in TITULOS and len(t)>1}
def puntaje(ta,tb):
    return sum(1 for a in ta if any(a==b or SequenceMatcher(None,a,b).ratio()>=0.85 for b in tb))

completos=[]
r=4
while p.cell(r,2).value:
    completos.append(re.sub(r',\s*M\.?\s*Sc\.?$','',str(p.cell(r,2).value).strip())); r+=1
def nombre_completo(corto):
    if not corto: return None
    tc=tokens(corto)
    mejor=max(completos, key=lambda n: puntaje(tc, tokens(n)))
    return mejor if puntaje(tc, tokens(mejor))>=2 else corto

CL={}; modulos=[]
i=0
for r in range(3,31):
    if not m.cell(r,3).value: continue
    mod='M%d' % (i//4+1); cod='%s · C%d' % (mod, i%4+1); i+=1
    if m.cell(r,1).value: modulos.append((mod, str(m.cell(r,1).value).split('. ',1)[-1]))
    CL[cod]={'tema':str(m.cell(r,3).value).strip(), 'cont':str(m.cell(r,4).value or '').strip(),
             'doc':nombre_completo(m.cell(r,5).value), 'estado':str(m.cell(r,6).value or '')}
assert len(CL)==28 and set(CL)==set(D), 'la matriz y la delimitación no coinciden'

def docente(cod):
    d=CL[cod]['doc']
    return d if d else 'por confirmar'

def quien(txt):
    """«M4 · C1, Dra. X. nota» -> «M4 · C1 · <docente de hoy>» y la nota aparte.
    Entiende rangos («M3 · C1 a C3») y pares («M4 · C3 y C4», «M6 · C1 y M6 · C2»)."""
    cods=[]
    for mo, c1, c2 in re.findall(r'M(\d) · C(\d)(?: a C(\d))?', txt):
        for k in range(int(c1), int(c2 or c1)+1): cods.append('M%s · C%d' % (mo, k))
    for mo, c in re.findall(r'M(\d) · C\d y C(\d)', txt):
        cods.append('M%s · C%s' % (mo, c))
    if not cods:
        return txt, ''
    corte=re.search(r'(?<!Dr)(?<!Dra)(?<!Lcda)(?<!Lcdo)(?<!Ing)\. | — ', txt)
    nota=txt[corte.end():].strip() if corte else ''
    vistos=[]
    for c in cods:
        if c not in vistos: vistos.append(c)
    return '<br/>› '.join('%s · %s' % (c, docente(c)) for c in vistos), nota

# ---------- estilos ----------
S=lambda **k: ParagraphStyle(**k)
st_tit=S(name='tit', fontName='Helvetica-Bold', fontSize=19, leading=23, textColor=TEAL)
st_sub=S(name='sub', fontName='Helvetica', fontSize=10, leading=14, textColor=MUTED)
st_txt=S(name='txt', fontName='Helvetica', fontSize=9, leading=12.6, textColor=INK)
st_sec=S(name='sec', fontName='Helvetica-Bold', fontSize=10.5, leading=13, textColor=colors.white)
st_cod=S(name='cod', fontName='Helvetica-Bold', fontSize=8.6, leading=11, textColor=GOLD)
st_tem=S(name='tem', fontName='Helvetica-Bold', fontSize=11.2, leading=14, textColor=TEAL)
st_dat=S(name='dat', fontName='Helvetica', fontSize=8.6, leading=11.5, textColor=INK)
st_lab=S(name='lab', fontName='Helvetica-Bold', fontSize=7.6, leading=10, textColor=MUTED)
st_it =S(name='it',  fontName='Helvetica', fontSize=8.5, leading=11.4, textColor=INK, leftIndent=8, firstLineIndent=-8)
st_nota=S(name='nota', fontName='Helvetica-Oblique', fontSize=7.8, leading=10.2, textColor=MUTED, leftIndent=8)
st_th=S(name='th', fontName='Helvetica-Bold', fontSize=8, leading=10, textColor=colors.white)
st_td=S(name='td', fontName='Helvetica', fontSize=8, leading=10.4, textColor=INK)

_h=datetime.date.today()
MESES=['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre']
HOY='%d de %s de %d' % (_h.day, MESES[_h.month-1], _h.year)

def marco(canv, doc):
    canv.saveState()
    canv.setFillColor(TEAL); canv.rect(0, A4[1]-9*mm, A4[0], 9*mm, stroke=0, fill=1)
    canv.setFillColor(GOLD); canv.rect(0, A4[1]-10.2*mm, A4[0], 1.2*mm, stroke=0, fill=1)
    canv.setFillColor(colors.white); canv.setFont('Helvetica-Bold', 7.4)
    canv.drawString(15*mm, A4[1]-6.2*mm, 'CURSO VIRTUAL SEDA · DESGLOSE DE TEMAS PARA DOCENTES')
    canv.setFont('Helvetica', 7.4)
    canv.drawRightString(A4[0]-15*mm, A4[1]-6.2*mm, 'Página %d' % doc.page)
    canv.setStrokeColor(MINT); canv.setLineWidth(.5); canv.line(15*mm, 11*mm, A4[0]-15*mm, 11*mm)
    canv.setFillColor(MUTED); canv.setFont('Helvetica', 6.8)
    canv.drawString(15*mm, 7.4*mm, 'Coordinación académica · Sociedad de Endocrinología y Diabetes del Austro')
    canv.drawRightString(A4[0]-15*mm, 7.4*mm, 'Versión del %s' % HOY)
    canv.restoreState()

doc=BaseDocTemplate('SEDA_Desglose_Temas_Docentes.pdf', pagesize=A4,
    leftMargin=15*mm, rightMargin=15*mm, topMargin=16*mm, bottomMargin=15*mm,
    title='Desglose de temas para docentes — Curso virtual SEDA',
    author='Coordinación académica · Curso virtual SEDA')
doc.addPageTemplates([PageTemplate(id='n',
    frames=[Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='f')], onPage=marco)])
W=doc.width

def banda(texto, color=TEAL):
    t=Table([[Paragraph(texto, st_sec)]], colWidths=[W])
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),color),('LEFTPADDING',(0,0),(-1,-1),7),
        ('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4)]))
    return t

def caja(texto):
    t=Table([[Paragraph(texto, st_txt)]], colWidths=[W])
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),WARM),('LINEBEFORE',(0,0),(0,-1),2.4,GOLD),
        ('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),
        ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
    return t

def tabla(filas, anchos):
    data=[[Paragraph(c, st_th) for c in filas[0]]]+[[Paragraph(c, st_td) for c in f] for f in filas[1:]]
    t=Table(data, colWidths=anchos, repeatRows=1)
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),TEAL),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white, PALE]),('GRID',(0,0),(-1,-1),.4,MINT),
        ('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),
        ('TOPPADDING',(0,0),(-1,-1),3.5),('BOTTOMPADDING',(0,0),(-1,-1),3.5)]))
    return t

F=[]
# ---------- portada ----------
try:
    F += [Image('activos/logo/logo-curso-seda.png', width=34*mm, height=34*mm, kind='proportional'), Spacer(1,4*mm)]
except Exception:
    pass
F += [Paragraph('Desglose de temas para docentes', st_tit), Spacer(1,1.5*mm),
      Paragraph('Curso virtual de actualización en obesidad, diabetes, nutrición clínica y salud digital · '
                'Sociedad de Endocrinología y Diabetes del Austro (SEDA)', st_sub), Spacer(1,5*mm),
      caja('<b>Para qué sirve este documento.</b> Son 28 clases grabadas por separado que los participantes '
           'verán seguidas. Aquí cada docente encuentra <b>su tema, su fecha tope de entrega, los puntos que le '
           'tocan y los que no</b>, con el nombre de quien los cubre. Así nadie repite lo que dicta otro colega '
           'y el curso se ve como un solo programa.'),
      Spacer(1,5*mm)]

F += [banda('CÓMO SE GRABA'), Spacer(1,2.5*mm)]
for x in ['<b>Duración:</b> 30 minutos por clase, grabada, no en vivo.',
          '<b>Dónde:</b> en la sala de Zoom del curso, con el fondo y la plantilla del curso. La coordinación '
          'envía el enlace y la guía de grabación.',
          '<b>Cuándo:</b> el día y la hora que le queden mejor, <b>antes de la fecha tope de su módulo</b>.',
          '<b>Si algo no le cuadra:</b> escriba a la coordinación antes de grabar. Es más fácil ajustarlo ahora '
          'que cuando la clase ya está grabada.']:
    F.append(Paragraph('•&nbsp; '+x, st_it))
F.append(Spacer(1,5*mm))

F += [banda('FECHAS TOPE DE ENTREGA POR MÓDULO'), Spacer(1,2.5*mm)]
filas=[['Módulo','Tema del módulo','Entrega de la grabación']]
for mod, nom in modulos:
    filas.append(['<b>%s</b>' % mod, nom, '<b>%s</b>' % FECHAS[mod]])
F += [tabla(filas, [16*mm, W-16*mm-52*mm, 52*mm]), Spacer(1,5*mm)]

F += [banda('LOS TEMAS QUE SE REPITEN Y CÓMO SE REPARTEN'), Spacer(1,2.5*mm),
      Paragraph('El programa declara algunos contenidos en más de una clase. Se reparten por enfoque:', st_txt),
      Spacer(1,2*mm)]
F.append(tabla([['Contenido que se repite','Clases','Cómo se reparte'],
    ['Dieta mediterránea, restricción de carbohidratos, ayuno intermitente','M2 · C2 y M5 · C2',
     'M2 lo enfoca en <b>obesidad</b>; M5, en <b>diabetes</b>'],
    ['Agonistas de GLP-1 y tirzepatida','M3 · C2, M3 · C3 y M4 · C3',
     'El módulo 3, como tratamiento de la <b>obesidad</b>; el 4, como <b>control glucémico</b>'],
    ['Monitoreo continuo de glucosa y AGP','M4 · C2 y M7 · C2',
     'M4 da la <b>interpretación clínica</b>; M7, la <b>implementación digital</b>'],
    ['Bioimpedancia y sarcopenia','M1 · C4, M5 · C4 y M6 · C4',
     'M1 da el <b>método</b>; M5 lo aplica a <b>diabetes</b>; M6 lo trata como <b>complicación</b>'],
    ['Beneficios renales de las nuevas terapias','M6 · C1 y M6 · C3',
     'M6 · C1 se queda con <b>tamizaje y diagnóstico</b>; M6 · C3, con los beneficios de las terapias'],
    ['Fenotipos metabólicos','M1 · C3 y M5 · C1',
     'M1 para <b>clasificar</b> al paciente; M5 para decidir el <b>plan nutricional</b>']],
    [W*0.34, W*0.22, W*0.44]))

# ---------- enfoque sugerido a algunos docentes ----------
# Cuando un docente pregunta cómo encarar su clase y la coordinación le responde, el enfoque
# acordado entra aquí. Es una propuesta: el docente puede repartir los minutos a su manera.
ENFOQUE = {
"M2 · C3": ("Una clase práctica para la consulta, no de fisiología ni de psiquiatría. Que quien escucha "
            "sepa reconocer qué tipo de hambre tiene su paciente y qué herramientas conductuales usar para "
            "que sostenga el tratamiento.",
            # propuesto por la coordinación a la Dra. Bermeo el 13/10/2026, a raíz de su consulta
            [("Hambre fisiológica y hambre emocional", "8 min",
              "La vía del hambre de forma breve: lo justo para distinguir el hambre homeostática de la "
              "hedónica o emocional, y cómo diferenciarlas en la consulta."),
             ("Conducta alimentaria en la consulta", "12 min",
              "Qué preguntar y cómo detectar el comer emocional; cuándo sospechar un trastorno de la conducta "
              "alimentaria (por ejemplo, el trastorno por atracón) y derivar; herramientas sencillas: registro "
              "alimentario, escala de hambre, control de estímulos, alimentación consciente, entrevista motivacional."),
             ("Adherencia terapéutica", "8 min",
              "Por qué los pacientes abandonan y qué hacer: metas realistas, seguimiento frecuente, prevención "
              "de recaídas y lenguaje sin estigma.")],
            "Cierre con un mensaje práctico para la consulta."),
}

def caja_enfoque(cod):
    obj, bloques, cierre = ENFOQUE[cod]
    filas=[[Paragraph('ENFOQUE SUGERIDO · los minutos son orientativos', S(name='ea', parent=st_lab, textColor=GOLD)), '', ''],
           [Paragraph(obj, st_dat), '', '']]
    for i,(t,mins,d) in enumerate(bloques, 1):
        filas.append([Paragraph('<b>%d</b>' % i, st_dat), Paragraph('<b>%s</b><br/>%s' % (t, d), st_dat),
                      Paragraph('<b>%s</b>' % mins, st_dat)])
    filas.append([Paragraph(cierre, st_nota), '', ''])
    t=Table(filas, colWidths=[8*mm, W-8*mm-18*mm, 18*mm])
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),WARM),('LINEBEFORE',(0,0),(0,-1),2.4,GOLD),
        ('SPAN',(0,0),(-1,0)),('SPAN',(0,1),(-1,1)),('SPAN',(0,-1),(-1,-1)),
        ('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),
        ('TOPPADDING',(0,0),(-1,-1),2.5),('BOTTOMPADDING',(0,0),(-1,-1),2.5),
        ('LINEABOVE',(0,2),(-1,-2),.4,colors.HexColor('#EBD9B4'))]))
    return t

# ---------- clase por clase ----------
def bloque_clase(cod):
    c=CL[cod]; si,no=D[cod]; mod=cod.split(' · ')[0]
    vac = not c['doc']
    cab=Table([[Paragraph(cod.replace('M','MÓDULO ',1).replace(' · C',' · CLASE '), st_cod)],
               [Paragraph(c['tema'], st_tem)]], colWidths=[W])
    cab.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),PALE),('LINEBEFORE',(0,0),(0,-1),3,TEAL),
        ('LEFTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(0,0),5),('BOTTOMPADDING',(0,-1),(-1,-1),5),
        ('TOPPADDING',(0,1),(-1,1),0)]))
    doc_txt=('<font color="#A3342B"><b>Por confirmar</b></font>' if vac else '<b>%s</b>' % c['doc'])
    datos=Table([[Paragraph('DOCENTE', st_lab), Paragraph('ENTREGA', st_lab), Paragraph('DURACIÓN', st_lab)],
                 [Paragraph(doc_txt, st_dat), Paragraph('<b>%s</b>' % FECHAS[mod], st_dat),
                  Paragraph('30 minutos', st_dat)]],
                colWidths=[W*0.48, W*0.36, W*0.16])
    datos.setStyle(TableStyle([('LEFTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),1.5),
        ('BOTTOMPADDING',(0,0),(-1,-1),1.5),('VALIGN',(0,0),(-1,-1),'TOP')]))
    izq=[Paragraph('LO QUE SÍ LE TOCA', S(name='l1', parent=st_lab, textColor=TEAL))]
    for x in si:
        x=x.replace('ALCANCE ACORDADO:', '<b>Alcance acordado:</b>')
        izq.append(Paragraph('•&nbsp; '+x, st_it))
    der=[Paragraph('LO QUE NO LE TOCA · QUIÉN LO CUBRE', S(name='l2', parent=st_lab, textColor=ROJO))]
    for q,w in no:
        q=q.replace('ATENCIÓN — ', '<b>Atención:</b> ')
        quien_txt, nota = quien(w)
        der.append(Paragraph('•&nbsp; %s<br/><font color="#5F7073">› %s</font>' % (q, quien_txt), st_it))
        if nota: der.append(Paragraph(nota[0].upper()+nota[1:], st_nota))
    cuerpo=Table([[izq, der]], colWidths=[W*0.48, W*0.52])
    cuerpo.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),8),
        ('RIGHTPADDING',(0,0),(-1,-1),6),('LINEAFTER',(0,0),(0,-1),.5,MINT)]))
    partes=[cab, Spacer(1,2*mm), datos,
            Paragraph('<font color="#5F7073"><b>Contenidos declarados en el programa:</b> %s</font>' % c['cont'],
                      S(name='cd', parent=st_dat, leftIndent=8, spaceBefore=2, spaceAfter=3)),
            cuerpo]
    if cod in ENFOQUE:
        partes += [Spacer(1,2.5*mm), caja_enfoque(cod)]
    if vac:
        partes.append(Paragraph('Esta clase todavía no tiene docente confirmado. La coordinación avisará cuando '
                                'se asigne.', S(name='v', parent=st_nota, textColor=ROJO)))
    return KeepTogether(partes+[Spacer(1,6*mm)])

for mod, nom in modulos:
    F += [PageBreak(), banda('MÓDULO %s · %s' % (mod[1], nom.upper())),
          Paragraph('Entrega de todas las clases de este módulo: <b>%s</b>' % FECHAS[mod],
                    S(name='em', parent=st_dat, spaceBefore=3, spaceAfter=5, leftIndent=2)),
          ]
    for k in range(1,5):
        F.append(bloque_clase('%s · C%d' % (mod, k)))

doc.build(F)
print('generado ·', len(CL), 'clases')
