# -*- coding: utf-8 -*-
"""Directorio de ponentes: nombre, correo, celular y tema. Documento interno de trabajo."""
import openpyxl, unicodedata
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, Table, TableStyle, KeepTogether)

TEAL=colors.HexColor('#0D5A62'); GOLD=colors.HexColor('#B8852B')
MINT=colors.HexColor('#C8E1DF'); PALE=colors.HexColor('#EDF5F4')
WARM=colors.HexColor('#FBF1DC'); INK=colors.HexColor('#1A2325'); MUTED=colors.HexColor('#5F7073')
RED =colors.HexColor('#A3342B')

S=lambda **k: ParagraphStyle(**k)
st_tit=S(name='t', fontName='Helvetica-Bold', fontSize=18, leading=22, textColor=TEAL)
st_sub=S(name='s', fontName='Helvetica', fontSize=9.5, leading=13, textColor=MUTED)
st_mod=S(name='m', fontName='Helvetica-Bold', fontSize=10.5, leading=13, textColor=colors.white)
st_nom=S(name='n', fontName='Helvetica-Bold', fontSize=9.2, leading=11.5, textColor=INK)
st_dat=S(name='d', fontName='Helvetica', fontSize=8.3, leading=10.5, textColor=MUTED)
st_fal=S(name='f', fontName='Helvetica-Oblique', fontSize=8.3, leading=10.5, textColor=RED)
st_tem=S(name='te',fontName='Helvetica', fontSize=8.6, leading=11, textColor=INK)
st_cod=S(name='c', fontName='Helvetica-Bold', fontSize=8, leading=10, textColor=GOLD)
st_av =S(name='a', fontName='Helvetica', fontSize=8.6, leading=11.5, textColor=INK)
st_hd =S(name='h', fontName='Helvetica-Bold', fontSize=7.2, leading=9, textColor=MUTED)

def marco(canv, doc):
    canv.saveState()
    canv.setFillColor(PALE); canv.rect(0, A4[1]-12*mm, A4[0], 12*mm, stroke=0, fill=1)
    canv.setFillColor(MUTED); canv.setFont('Helvetica', 7)
    canv.drawString(15*mm, A4[1]-8*mm, 'Directorio de ponentes · Curso virtual SEDA · DOCUMENTO INTERNO')
    canv.drawRightString(A4[0]-15*mm, A4[1]-8*mm, 'Página %d' % doc.page)
    canv.setStrokeColor(MINT); canv.setLineWidth(.6); canv.line(15*mm, 12*mm, A4[0]-15*mm, 12*mm)
    canv.setFillColor(MUTED); canv.setFont('Helvetica', 6.5)
    canv.drawString(15*mm, 8.5*mm, 'Contiene datos personales. No distribuir.')
    canv.drawRightString(A4[0]-15*mm, 8.5*mm, 'Actualizado el 5 de octubre de 2026')
    canv.restoreState()

doc=BaseDocTemplate('SEDA_Directorio_Ponentes.pdf', pagesize=A4,
    leftMargin=15*mm, rightMargin=15*mm, topMargin=17*mm, bottomMargin=15*mm,
    title='Directorio de ponentes · Curso virtual SEDA', author='SEDA')
doc.addPageTemplates([PageTemplate(id='n',
    frames=[Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='f')], onPage=marco)])
W=doc.width

w=openpyxl.load_workbook('SEDA_Matriz_Ponentes_Curso_Obesidad.xlsx')
m=w['Matriz 28 clases']; p=w['Ponentes - datos aval']
def norm(s):
    return unicodedata.normalize('NFKD',str(s)).encode('ascii','ignore').decode().lower()
pon=[]
r=4
while p.cell(r,2).value:
    pon.append({'n':str(p.cell(r,2).value),'esp':p.cell(r,3).value,'inst':p.cell(r,4).value,
                'mail':p.cell(r,5).value,'tel':p.cell(r,6).value}); r+=1
def datos(nombre):
    a=set(norm(nombre).replace('.','').split())-{'dr','dra','lcda','msc','de','m'}
    best,sc=None,0
    for d in pon:
        b=set(norm(d['n']).replace('.','').split())-{'dr','dra','lcda','msc','de','m'}
        s=len(a&b)
        if s>sc: sc,best=s,d
    return best

mods=['M1']*4+['M2']*4+['M3']*4+['M4']*4+['M5']*4+['M6']*4+['M7']*4
MOD={'M1':'MÓDULO 1 · Obesidad: concepto y evaluación','M2':'MÓDULO 2 · Nutrición y actividad física',
     'M3':'MÓDULO 3 · Farmacoterapia y cirugía','M4':'MÓDULO 4 · Diabetes',
     'M5':'MÓDULO 5 · Nutrición clínica aplicada','M6':'MÓDULO 6 · Complicaciones',
     'M7':'MÓDULO 7 · Salud digital'}
ENT={'M1':'entrega 29 oct','M2':'entrega 29 oct','M3':'entrega 5 nov','M4':'entrega 12 nov',
     'M5':'entrega 19 nov','M6':'entrega 26 nov','M7':'entrega 3 dic'}

F=[Paragraph('Directorio de ponentes', st_tit), Spacer(1,2.5*mm),
   Paragraph('Curso virtual de actualización en obesidad, diabetes, nutrición clínica y salud digital<br/>'
             'Sociedad de Endocrinología y Diabetes del Austro · SEDA', st_sub), Spacer(1,4*mm)]
sin_mail=sum(1 for d in pon if not d['mail'])
av=Table([[Paragraph('<b>Documento interno de trabajo.</b> Reúne los datos de contacto de los 23 docentes '
  'junto a la clase que dicta cada uno. Contiene datos personales: no circula fuera de la coordinación.<br/><br/>'
  '<b>Atención:</b> faltan <b>%d de 23 correos electrónicos</b>. La comunicación con la mayoría ha sido por '
  'WhatsApp, de modo que el teléfono es el canal fiable. Los correos que faltan hay que pedirlos: el '
  'expediente del aval y el envío de certificados los van a necesitar.' % sin_mail, st_av)]], colWidths=[W])
av.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),WARM),('LINEBEFORE',(0,0),(0,-1),2.2,GOLD),
    ('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),
    ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
F += [av, Spacer(1,4*mm)]

i=0; last=None; bloque=[]
def cerrar(b):
    if b: F.append(KeepTogether(b))
for r in range(3,31):
    if not m.cell(r,3).value: continue
    md=mods[i]; cod='%s · C%d'%(md,i%4+1); i+=1
    tema=m.cell(r,3).value; nombre=str(m.cell(r,5).value); est=str(m.cell(r,6).value)
    if md!=last:
        cerrar(bloque); bloque=[]
        h=Table([[Paragraph(MOD[md], st_mod), Paragraph(
            '<para align="right">%s</para>'%ENT[md],
            S(name='x',fontName='Helvetica',fontSize=8,leading=10,textColor=MINT))]],
            colWidths=[W*0.74, W*0.26])
        h.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),TEAL),('VALIGN',(0,0),(-1,-1),'MIDDLE'),
            ('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),
            ('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4)]))
        bloque += [Spacer(1,3*mm), h, Spacer(1,1.5*mm)]
        last=md
    if est=='VACANTE':
        t=Table([[Paragraph(cod,st_cod), Paragraph('<b>%s</b>'%tema, st_tem),
                  Paragraph('SIN PONENTE ASIGNADO', st_fal)]], colWidths=[17*mm, W*0.44, W-17*mm-W*0.44])
        t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(-1,-1),colors.HexColor('#FBEEEC')),
            ('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),
            ('LEFTPADDING',(0,0),(0,-1),4)]))
        bloque.append(t); continue
    d=datos(nombre) or {}
    mail=d.get('mail') or '— falta correo —'
    tel =d.get('tel')  or '— falta teléfono —'
    esp =d.get('esp'); inst=d.get('inst')
    linea2=' · '.join([x for x in [esp, inst] if x])
    cont='%s<br/>%s'%(tel, mail)
    izq=[Paragraph(nombre, st_nom)]
    if linea2: izq.append(Paragraph(linea2, st_dat))
    t=Table([[Paragraph(cod,st_cod), izq, Paragraph(tema, st_tem),
              Paragraph(cont, st_fal if not d.get('mail') else st_dat)]],
            colWidths=[17*mm, W*0.28, W*0.31, W-17*mm-W*0.59])
    t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),
        ('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),
        ('LEFTPADDING',(0,0),(0,-1),4),('LINEBELOW',(0,0),(-1,-1),.35,MINT)]))
    bloque.append(t)
cerrar(bloque)
doc.build(F)
print('SEDA_Directorio_Ponentes.pdf generado')
