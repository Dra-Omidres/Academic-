# -*- coding: utf-8 -*-
"""Programa del curso para montarlo en saludelearning.com (módulos, clases, contenidos, docente).

Derivado de generador-programa-auspiciantes-pdf.py; además de tema y docente lleva los
contenidos declarados de cada clase (columna D de la matriz), para la ficha de cada video.

Lo pidió Boehringer Ingelheim (12/10/2026): un programa con fechas de inicio y fin para su
proceso interno. Lleva solo lo público del curso: datos generales y, por módulo, la fecha
de publicación, las clases y quién las dicta. Nada de contactos ni de datos personales.

La charla del auspiciante NO va aquí: es material complementario, fuera de las 28 clases
con aval, y se le explica en el correo.

Salida: SEDA_Programa_Plataforma_saludelearning.pdf
"""
import re, unicodedata, openpyxl
from difflib import SequenceMatcher
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether

TEAL=colors.HexColor('#0D5A62'); GOLD=colors.HexColor('#B8852B'); MINT=colors.HexColor('#C8E1DF')
PALE=colors.HexColor('#EDF5F4'); INK=colors.HexColor('#1A2325'); MUTED=colors.HexColor('#5F7073')

# Calendario del correo a la Comisión del 26/10/2026 (ver generador-expediente-aval-docx.py)
PUBLICA={'M1':'jueves 26 de noviembre de 2026','M2':'jueves 26 de noviembre de 2026','M3':'jueves 3 de diciembre de 2026',
         'M4':'jueves 10 de diciembre de 2026','M5':'jueves 17 de diciembre de 2026','M6':'jueves 7 de enero de 2027',
         'M7':'jueves 14 de enero de 2027'}

# ---------- datos de la matriz (mismo emparejamiento que el expediente) ----------
wb=openpyxl.load_workbook('SEDA_Matriz_Ponentes_Curso_Obesidad.xlsx')
m=wb['Matriz 28 clases']; p=wb['Ponentes - datos aval']
TITULOS={'dr','dra','lcda','lcdo','ing','msc','m','sc','mg','mgt','mgtr','de','del','la','y'}
def tokens(s):
    s=unicodedata.normalize('NFKD', str(s)).encode('ascii','ignore').decode().lower()
    return {t for t in re.findall(r'[a-z]+', s) if t not in TITULOS and len(t)>1}
def puntaje(a,b):
    return sum(1 for x in a if any(x==y or SequenceMatcher(None,x,y).ratio()>=0.85 for y in b))
def limpio(s):
    s=re.sub(r'\s*\([^)]*\)', '', str(s or '')).strip()
    return re.sub(r',\s*M\.?\s*Sc\.?$', '', s)
docentes=[]; r=4
while p.cell(r,2).value:
    docentes.append(limpio(p.cell(r,2).value)); r+=1
def docente_de(corto):
    tc=tokens(corto); return max(docentes, key=lambda d: puntaje(tc, tokens(d)))

modulos=[]; i=0
for r in range(3,31):
    if not m.cell(r,3).value: continue
    mod='M%d' % (i//4+1); i+=1
    if m.cell(r,1).value: modulos.append({'mod':mod,'nombre':str(m.cell(r,1).value).split('. ',1)[-1],'clases':[]})
    doc=docente_de(m.cell(r,5).value) if m.cell(r,5).value else 'Por confirmar'
    modulos[-1]['clases'].append((str(m.cell(r,3).value).strip(), doc, str(m.cell(r,4).value or '').strip()))
assert i==28 and len(modulos)==7

# ---------- PDF ----------
def S(**k):
    base=dict(fontName='Helvetica', fontSize=9.5, leading=12.5, textColor=INK); base.update(k)
    return ParagraphStyle('x', **base)
st_tit=S(fontName='Helvetica-Bold', fontSize=16, leading=20, textColor=TEAL)
st_sup=S(fontName='Helvetica-Bold', fontSize=8.5, textColor=GOLD)
st_sub=S(textColor=MUTED, fontSize=10)
st_mod=S(fontName='Helvetica-Bold', fontSize=10.5, textColor=colors.white)
st_fecha=S(fontSize=8.5, textColor=colors.white)
st_cel=S(); st_doc=S(textColor=MUTED, fontSize=9)
st_nota=S(fontSize=8.5, textColor=MUTED)

out='SEDA_Programa_Plataforma_saludelearning.pdf'
pdf=SimpleDocTemplate(out, pagesize=A4, leftMargin=2*cm, rightMargin=2*cm, topMargin=1.8*cm, bottomMargin=1.8*cm,
                      title='Programa para la plataforma · Curso virtual SEDA', author='SEDA')
E=[Paragraph('PROGRAMA PARA LA PLATAFORMA · saludelearning.com', st_sup), Spacer(1,3),
   Paragraph('Curso virtual de actualización en obesidad, diabetes, nutrición clínica y salud digital', st_tit),
   Spacer(1,4), Paragraph('Sociedad de Endocrinología y Diabetes del Austro (SEDA) · Cuenca, Ecuador', st_sub), Spacer(1,12)]

gen=[['Inicio','Jueves 26 de noviembre de 2026'],
     ['Cierre','Jueves 21 de enero de 2027 · receso entre el 17 de diciembre y el 7 de enero'],
     ['Modalidad','Virtual y asincrónica, en la plataforma saludelearning.com'],
     ['Estructura','7 módulos · 28 clases grabadas de 30 minutos · un módulo nuevo cada jueves'],
     ['Valor curricular','20 horas'],
     ['Dirigido a','Médicos generales y especialistas, nutricionistas y otros profesionales de la salud'],
     ['Aval académico','Universidad de Cuenca, en trámite']]
t=Table([[Paragraph('<b>%s</b>' % a, S(textColor=TEAL)), Paragraph(b, st_cel)] for a,b in gen], colWidths=[3.6*cm, 13.4*cm])
t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),PALE),('LINEBELOW',(0,0),(-1,-2),0.4,colors.white),
                       ('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4)]))
E+=[t, Spacer(1,14)]

for md in modulos:
    filas=[[Paragraph('%s · %s' % (md['mod'], md['nombre']), st_mod),
            Paragraph('Se publica el %s' % PUBLICA[md['mod']], st_fecha)]]
    for k,(tema,doc,cont) in enumerate(md['clases'],1):
        filas.append([Paragraph('<font color="#B8852B"><b>Clase %d</b></font>&nbsp;&nbsp;<b>%s</b><br/><font size="8.3" color="#5F7073">%s</font>' % (k, tema, cont), st_cel),
                      Paragraph(doc, st_doc)])
    t=Table(filas, colWidths=[11.2*cm, 5.8*cm])
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),TEAL),('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                           ('LINEBELOW',(0,1),(-1,-1),0.4,MINT),('TOPPADDING',(0,0),(-1,-1),4),
                           ('BOTTOMPADDING',(0,0),(-1,-1),4)]))
    E+=[KeepTogether([t, Spacer(1,9)])]

E+=[KeepTogether([Table([[Paragraph('<b>Módulo de anexos · material complementario</b>', st_mod), Paragraph('Abierto desde el inicio del curso', st_fecha)],
       [Paragraph('Temas complementarios y charlas de la industria, identificados como tales. No forman parte de las 28 clases ni de las horas del certificado. Contenidos: <b>por confirmar</b>.', st_cel), Paragraph('', st_doc)]],
       colWidths=[11.2*cm, 5.8*cm], style=TableStyle([('BACKGROUND',(0,0),(-1,0),GOLD),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),('SPAN',(0,1),(1,1))])), Spacer(1,9)])]
E+=[Spacer(1,4), Paragraph('Programa sujeto a cambios menores en el cuerpo docente. Versión del 7 de noviembre de 2026.', st_nota)]
pdf.build(E)
print('generado', out)
