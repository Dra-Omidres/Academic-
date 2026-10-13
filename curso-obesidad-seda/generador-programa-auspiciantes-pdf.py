# -*- coding: utf-8 -*-
"""Programa académico del curso para los auspiciantes.

Lo pidió Boehringer Ingelheim (12/10/2026): un programa con fechas de inicio y fin para su
proceso interno. Lleva solo lo público del curso: datos generales y, por módulo, la fecha
de publicación, las clases y quién las dicta. Nada de contactos ni de datos personales.

La charla del auspiciante NO va aquí: es material complementario, fuera de las 28 clases
con aval, y se le explica en el correo.

Salida: SEDA_Programa_Academico_Auspiciantes.pdf
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

PUBLICA={'M1':'jueves 5 de noviembre','M2':'jueves 5 de noviembre','M3':'jueves 12 de noviembre',
         'M4':'jueves 19 de noviembre','M5':'jueves 26 de noviembre','M6':'jueves 3 de diciembre',
         'M7':'jueves 10 de diciembre'}

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
    modulos[-1]['clases'].append((str(m.cell(r,3).value).strip(), doc))
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

out='SEDA_Programa_Academico_Auspiciantes.pdf'
pdf=SimpleDocTemplate(out, pagesize=A4, leftMargin=2*cm, rightMargin=2*cm, topMargin=1.8*cm, bottomMargin=1.8*cm,
                      title='Programa académico · Curso virtual SEDA', author='SEDA')
E=[Paragraph('PROGRAMA ACADÉMICO', st_sup), Spacer(1,3),
   Paragraph('Curso virtual de actualización en obesidad, diabetes, nutrición clínica y salud digital', st_tit),
   Spacer(1,4), Paragraph('Sociedad de Endocrinología y Diabetes del Austro (SEDA) · Cuenca, Ecuador', st_sub), Spacer(1,12)]

gen=[['Inicio','Jueves 5 de noviembre de 2026'],
     ['Cierre','Jueves 17 de diciembre de 2026'],
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
    for k,(tema,doc) in enumerate(md['clases'],1):
        filas.append([Paragraph('<font color="#B8852B"><b>Clase %d</b></font>&nbsp;&nbsp;%s' % (k, tema), st_cel),
                      Paragraph(doc, st_doc)])
    t=Table(filas, colWidths=[11.2*cm, 5.8*cm])
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),TEAL),('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                           ('LINEBELOW',(0,1),(-1,-1),0.4,MINT),('TOPPADDING',(0,0),(-1,-1),4),
                           ('BOTTOMPADDING',(0,0),(-1,-1),4)]))
    E+=[KeepTogether([t, Spacer(1,9)])]

E+=[Spacer(1,4), Paragraph('Programa sujeto a cambios menores en el cuerpo docente. Versión del 13 de octubre de 2026.', st_nota)]
pdf.build(E)
print('generado', out)
