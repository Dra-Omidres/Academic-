# -*- coding: utf-8 -*-
"""Guion detallado de la clase M3 · C2 · Agonistas del receptor de GLP-1 (Dra. Omidres).

Cronograma minuto a minuto de los 30 minutos, temas y subtemas, cifras clave y referencias.
Cada referencia se verificó en PubMed el 14/10/2026 (título, revista, volumen, páginas, DOI)
y cada cifra se copió del resumen publicado. Lo que viene de ficha técnica y no de un artículo
va marcado así, para verificarlo con la ficha aprobada en Ecuador.

Alcance según generador-delimitacion.py: semaglutida (mecanismo, dosis, manejo práctico),
evidencia de los agonistas de GLP-1 en OBESIDAD y efectos adversos. Fuera: tirzepatida
(M3 · C3), uso en diabetes (M4 · C3), beneficio cardiovascular y renal (M6 · C3) y manejo
nutricional (M5 · C3). Solo denominaciones genéricas: Elea, auspiciante, vende un agonista
de GLP-1 (conflictos-de-interes-expediente.md).

Salida: SEDA_Clase_M3C2_GLP1_Cronograma.pdf
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
                                KeepTogether, PageBreak)

TEAL=colors.HexColor('#0D5A62'); GOLD=colors.HexColor('#B8852B'); MINT=colors.HexColor('#C8E1DF')
PALE=colors.HexColor('#EDF5F4'); WARM=colors.HexColor('#FBF1DC'); INK=colors.HexColor('#1A2325')
MUTED=colors.HexColor('#5F7073')

def S(**k):
    b=dict(fontName='Helvetica', fontSize=9.3, leading=12.3, textColor=INK); b.update(k)
    return ParagraphStyle('x', **b)
st_sup=S(fontName='Helvetica-Bold', fontSize=8.5, textColor=GOLD)
st_tit=S(fontName='Helvetica-Bold', fontSize=17, leading=21, textColor=TEAL)
st_sub=S(fontSize=10, textColor=MUTED)
st_h=S(fontName='Helvetica-Bold', fontSize=12, leading=15, textColor=TEAL, spaceBefore=6, spaceAfter=4)
st=S(); st_b=S(fontName='Helvetica-Bold'); st_m=S(textColor=MUTED, fontSize=8.5, leading=11)
st_w=S(fontName='Helvetica-Bold', textColor=colors.white, fontSize=9.5)
st_ref=S(fontSize=8.3, leading=10.8)

def P(t, s=st): return Paragraph(t, s)
def caja(texto, fondo=WARM):
    t=Table([[P(texto)]], colWidths=[17*cm])
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),fondo),('LEFTPADDING',(0,0),(-1,-1),8),
                           ('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
    return t

E=[P('CURSO VIRTUAL SEDA · MÓDULO 3 · CLASE 2 · GUION DE LA DOCENTE', st_sup), Spacer(1,3),
   P('Agonistas del receptor de GLP-1 en el tratamiento de la obesidad', st_tit), Spacer(1,3),
   P('Dra. Omidres Pérez de Carvelli · 30 minutos grabados · entrega de la grabación: jueves 5 de noviembre · se publica el jueves 12 de noviembre', st_sub),
   Spacer(1,10)]

# ---------- alcance ----------
E.append(P('Qué cubre la clase y qué deja a otras', st_h))
t=Table([[P('<b>Sí entra</b>', st_w), P('<b>No entra · dónde se cubre</b>', st_w)],
         [P('• Mecanismo de acción de los agonistas de GLP-1 y por qué reducen el peso<br/>'
            '• Semaglutida y liraglutida: dosis, escalada y manejo práctico<br/>'
            '• Evidencia en obesidad: programas SCALE, STEP y OASIS<br/>'
            '• Qué pasa al suspender el fármaco<br/>'
            '• Efectos adversos y cómo manejarlos'),
          P('• Tirzepatida y terapias nuevas → M3 · C3, Dra. Cuatecontzi<br/>'
            '• Agonistas de GLP-1 en diabetes → M4 · C3, Dra. Jiménez<br/>'
            '• Beneficio cardiovascular y renal → M6 · C3, Dr. Chen Ku<br/>'
            '• Alimentación durante el tratamiento → M5 · C3, Dra. Machado<br/>'
            '• Fármacos clásicos para obesidad → M3 · C1, Dr. Vanegas')]],
       colWidths=[8.5*cm, 8.5*cm])
t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),TEAL),('BACKGROUND',(0,1),(0,1),PALE),('BACKGROUND',(1,1),(1,1),colors.white),
                       ('BOX',(0,0),(-1,-1),0.5,MINT),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
E+=[t, Spacer(1,6),
    caja('<b>Dos reglas de esta clase.</b> Solo <b>denominaciones genéricas</b> (semaglutida, liraglutida), nunca marcas: '
         'uno de los auspiciantes del curso comercializa un agonista de GLP-1. Y la primera diapositiva después de la '
         'portada es la <b>declaración de conflictos de interés</b>.'), Spacer(1,8)]

# ---------- cronograma ----------
E.append(P('Cronograma minuto a minuto', st_h))
B=[
('00:00 – 02:00','Apertura',
 '• Presentación y título de la clase<br/>• Declaración de conflictos de interés<br/>'
 '• Tres objetivos: entender cómo actúan, conocer la evidencia en obesidad y saber manejar los efectos adversos',
 '—'),
('02:00 – 07:00','1 · Mecanismo de acción',
 '• GLP-1 endógeno: hormona intestinal, vida media de minutos<br/>'
 '• El agonista farmacológico: resistente a la degradación, vida media prolongada<br/>'
 '• Acción central: hipotálamo y tronco encefálico → más saciedad, menos apetito<br/>'
 '• Retraso del vaciamiento gástrico<br/>'
 '• Secreción de insulina dependiente de glucosa e inhibición del glucagón (solo mencionarlo: el detalle glucémico es de M4 · C3)<br/>'
 '• Mensaje: el peso baja porque el paciente come menos, no por pérdida de calorías por el intestino',
 'Drucker 2018 [1]'),
('07:00 – 10:00','2 · Moléculas y dosificación',
 '• <b>Liraglutida 3,0 mg</b> subcutánea, una vez al día<br/>'
 '• <b>Semaglutida 2,4 mg</b> subcutánea, una vez por semana; escalada de 16 semanas hasta la dosis de mantenimiento<br/>'
 '• Si no tolera 2,4 mg: STEP 8 permitió quedarse en 1,7 mg<br/>'
 '• <b>Semaglutida oral 50 mg</b> diaria: evidencia de fase 3 (OASIS 1)<br/>'
 '• Diapositiva práctica: la tabla de escalada y qué hacer si se olvida una dosis',
 'STEP 4 [5] · STEP 8 [7] · OASIS 1 [10] · ficha técnica (FT)'),
('10:00 – 18:00','3 · La evidencia en obesidad',
 '• <b>SCALE</b>, liraglutida 3,0 mg, 56 semanas: −8,4 kg frente a −2,8 kg con placebo; 63,2 % perdió ≥5 % del peso<br/>'
 '• <b>STEP 1</b>, semaglutida 2,4 mg, 68 semanas: −14,9 % frente a −2,4 %; la mitad perdió ≥15 %<br/>'
 '• <b>STEP 3</b>, con terapia conductual intensiva: −16,0 % frente a −5,7 %<br/>'
 '• <b>STEP 5</b>, dos años: −15,2 % frente a −2,6 %; el efecto se sostiene<br/>'
 '• <b>STEP 8</b>, comparación directa: semaglutida −15,8 % frente a liraglutida −6,4 %<br/>'
 '• <b>STEP 2</b>, persona con obesidad y diabetes tipo 2: −9,6 % frente a −3,4 % (la pérdida es menor; el resto, en M4 · C3)<br/>'
 '• <b>STEP TEENS</b>, adolescentes: IMC −16,1 % frente a +0,6 %<br/>'
 '• <b>OASIS 1</b>, vía oral 50 mg: −15,1 % frente a −2,4 %<br/>'
 '• Una sola línea sobre <b>SELECT</b> (eventos cardiovasculares) y remitir a M6 · C3',
 '[2] [3] [4] [6] [7] [8] [9] [10] · SELECT [14]'),
('18:00 – 21:00','4 · Al suspender el tratamiento',
 '• <b>STEP 4</b>: tras 20 semanas con semaglutida, quien siguió perdió otro 7,9 %; quien pasó a placebo recuperó 6,9 %<br/>'
 '• <b>Extensión de STEP 1</b>: un año después de suspender, se recuperaron dos tercios del peso perdido y los factores cardiometabólicos volvieron hacia el inicio<br/>'
 '• Mensaje: la obesidad es una enfermedad crónica; el tratamiento también lo es. Hay que hablarlo con el paciente antes de empezar',
 'STEP 4 [5] · STEP 1 ext. [11]'),
('21:00 – 27:00','5 · Efectos adversos y su manejo',
 '• <b>Gastrointestinales</b> (STEP 1 a 3): náuseas 43,9 % frente a 16,1 %; diarrea 29,7 %; vómitos 24,5 %; estreñimiento 24,2 %. '
 'Casi todos leves o moderados, transitorios y concentrados en la escalada; solo 4,3 % suspendió por ellos. '
 'La pérdida de peso <b>no</b> depende de tener náuseas<br/>'
 '• Manejo: escalar despacio, no subir la dosis si persisten los síntomas, porciones pequeñas (el detalle nutricional va en M5 · C3)<br/>'
 '• <b>Vesícula y vías biliares</b>: metaanálisis de 76 ensayos, RR 1,37; mayor en ensayos de pérdida de peso (RR 2,29), con dosis altas y uso prolongado<br/>'
 '• <b>Neuropatía óptica isquémica (NAION)</b>: una cohorte retrospectiva de un solo centro encontró asociación; es una señal, no una causalidad demostrada<br/>'
 '• <b>Cirugía y endoscopia</b>: riesgo de contenido gástrico retenido; la guía multisocietaria de 2024 recomienda estratificar el riesgo y decidir en conjunto si se suspende<br/>'
 '• Contraindicaciones y precauciones de la ficha técnica: antecedente personal o familiar de carcinoma medular de tiroides o MEN 2, pancreatitis, embarazo (FT)',
 'Wharton 2022 [12] · He 2022 [13] · Hathaway 2024 [15] · Kindel 2024 [16] · ficha técnica (FT)'),
('27:00 – 30:00','Cierre',
 '• Tres mensajes:<br/>'
 '&nbsp;&nbsp;1. Actúan sobre el apetito y la saciedad; la pérdida de peso es clínicamente relevante y se sostiene a dos años<br/>'
 '&nbsp;&nbsp;2. Al suspenderlos, el peso vuelve: se plantean como tratamiento crónico<br/>'
 '&nbsp;&nbsp;3. Los efectos gastrointestinales se previenen con una escalada lenta<br/>'
 '• Puente a la clase siguiente: tirzepatida y terapias nuevas (M3 · C3)',
 '—'),
]
filas=[[P('<b>Minuto</b>',st_w),P('<b>Bloque</b>',st_w),P('<b>Temas y subtemas</b>',st_w),P('<b>Referencias</b>',st_w)]]
for m,b,c,r in B:
    filas.append([P('<b>%s</b>'%m, S(fontSize=8.8, textColor=TEAL)), P('<b>%s</b>'%b), P(c), P(r, st_m)])
t=Table(filas, colWidths=[2.2*cm, 2.9*cm, 9.0*cm, 2.9*cm], repeatRows=1)
t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),TEAL),('VALIGN',(0,0),(-1,-1),'TOP'),
                       ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white, PALE]),
                       ('LINEBELOW',(0,0),(-1,-1),0.4,MINT),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
E+=[t, Spacer(1,6),
    P('(FT) = dato de ficha técnica, no de un artículo. Verificarlo con la ficha aprobada por ARCSA antes de grabar. '
      'Qué presentaciones están disponibles hoy en Ecuador: <b>POR CONFIRMAR</b>.', st_m)]

# ---------- calendario de preparación ----------
E+=[Spacer(1,8), P('Tu calendario hasta la entrega', st_h)]
cal=[['Hasta el miércoles 22 de octubre','Diapositivas armadas con este guion'],
     ['Jueves 23 – lunes 27 de octubre','Ensayo cronometrado: cada bloque dentro de su tiempo'],
     ['Hasta el lunes 2 de noviembre','Grabación en la sala de Zoom del curso'],
     ['Jueves 5 de noviembre','Fecha límite de entrega'],
     ['Jueves 12 de noviembre','Se publica con el módulo 3']]
t=Table([[P('<b>%s</b>'%a),P(b)] for a,b in cal], colWidths=[5.5*cm, 11.5*cm])
t.setStyle(TableStyle([('BACKGROUND',(0,0),(0,-1),PALE),('LINEBELOW',(0,0),(-1,-1),0.4,MINT),
                       ('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4)]))
E+=[t, Spacer(1,3), P('Fechas intermedias propuestas para dejar margen; solo la del 5 de noviembre es fija.', st_m)]

# ---------- referencias ----------
E+=[Spacer(1,10), P('Referencias', st_h),
    P('Verificadas en PubMed el 14 de octubre de 2026. Las cifras del cronograma están tomadas del resumen publicado de cada artículo.', st_m), Spacer(1,6)]
R=[
 'Drucker DJ. Mechanisms of action and therapeutic application of glucagon-like peptide-1. Cell Metab. 2018;27(4):740-56. doi:10.1016/j.cmet.2018.03.001',
 'Pi-Sunyer X, Astrup A, Fujioka K, et al. A randomized, controlled trial of 3.0 mg of liraglutide in weight management. N Engl J Med. 2015;373(1):11-22. doi:10.1056/NEJMoa1411892',
 'Wilding JPH, Batterham RL, Calanna S, et al. Once-weekly semaglutide in adults with overweight or obesity. N Engl J Med. 2021;384(11):989-1002. doi:10.1056/NEJMoa2032183',
 'Wadden TA, Bailey TS, Billings LK, et al. Effect of subcutaneous semaglutide vs placebo as an adjunct to intensive behavioral therapy on body weight in adults with overweight or obesity: the STEP 3 randomized clinical trial. JAMA. 2021;325(14):1403-13. doi:10.1001/jama.2021.1831',
 'Rubino D, Abrahamsson N, Davies M, et al. Effect of continued weekly subcutaneous semaglutide vs placebo on weight loss maintenance in adults with overweight or obesity: the STEP 4 randomized clinical trial. JAMA. 2021;325(14):1414-25. doi:10.1001/jama.2021.3224',
 'Garvey WT, Batterham RL, Bhatta M, et al. Two-year effects of semaglutide in adults with overweight or obesity: the STEP 5 trial. Nat Med. 2022;28(10):2083-91. doi:10.1038/s41591-022-02026-4',
 'Rubino DM, Greenway FL, Khalid U, et al. Effect of weekly subcutaneous semaglutide vs daily liraglutide on body weight in adults with overweight or obesity without diabetes: the STEP 8 randomized clinical trial. JAMA. 2022;327(2):138-50. doi:10.1001/jama.2021.23619',
 'Davies M, Færch L, Jeppesen OK, et al. Semaglutide 2·4 mg once a week in adults with overweight or obesity, and type 2 diabetes (STEP 2): a randomised, double-blind, double-dummy, placebo-controlled, phase 3 trial. Lancet. 2021;397(10278):971-84. doi:10.1016/S0140-6736(21)00213-0',
 'Weghuber D, Barrett T, Barrientos-Pérez M, et al. Once-weekly semaglutide in adolescents with obesity. N Engl J Med. 2022;387(24):2245-57. doi:10.1056/NEJMoa2208601',
 'Knop FK, Aroda VR, do Vale RD, et al. Oral semaglutide 50 mg taken once per day in adults with overweight or obesity (OASIS 1): a randomised, double-blind, placebo-controlled, phase 3 trial. Lancet. 2023;402(10403):705-19. doi:10.1016/S0140-6736(23)01185-6',
 'Wilding JPH, Batterham RL, Davies M, et al. Weight regain and cardiometabolic effects after withdrawal of semaglutide: the STEP 1 trial extension. Diabetes Obes Metab. 2022;24(8):1553-64. doi:10.1111/dom.14725',
 'Wharton S, Calanna S, Davies M, et al. Gastrointestinal tolerability of once-weekly semaglutide 2.4 mg in adults with overweight or obesity, and the relationship between gastrointestinal adverse events and weight loss. Diabetes Obes Metab. 2022;24(1):94-105. doi:10.1111/dom.14551',
 'He L, Wang J, Ping F, et al. Association of glucagon-like peptide-1 receptor agonist use with risk of gallbladder and biliary diseases: a systematic review and meta-analysis of randomized clinical trials. JAMA Intern Med. 2022;182(5):513-9. doi:10.1001/jamainternmed.2022.0338',
 'Lincoff AM, Brown-Frandsen K, Colhoun HM, et al. Semaglutide and cardiovascular outcomes in obesity without diabetes. N Engl J Med. 2023;389(24):2221-32. doi:10.1056/NEJMoa2307563',
 'Hathaway JT, Shah MP, Hathaway DB, et al. Risk of nonarteritic anterior ischemic optic neuropathy in patients prescribed semaglutide. JAMA Ophthalmol. 2024;142(8):732-9. doi:10.1001/jamaophthalmol.2024.2296',
 'Kindel TL, Wang AY, Wadhwa A, et al. Multisociety clinical practice guidance for the safe use of glucagon-like peptide-1 receptor agonists in the perioperative period. Surg Obes Relat Dis. 2024;20(12):1183-6. doi:10.1016/j.soard.2024.08.033',
]
for i,r in enumerate(R,1):
    E.append(P('%d. %s' % (i,r), st_ref)); E.append(Spacer(1,3))

def pie(c, d):
    c.saveState(); c.setFont('Helvetica',7.5); c.setFillColor(MUTED)
    c.drawString(2*cm, 1.1*cm, 'Curso virtual SEDA · M3 · C2 · Guion de uso interno · 14 de octubre de 2026')
    c.drawRightString(19*cm, 1.1*cm, 'Página %d' % d.page); c.restoreState()

out='SEDA_Clase_M3C2_GLP1_Cronograma.pdf'
SimpleDocTemplate(out, pagesize=A4, leftMargin=2*cm, rightMargin=2*cm, topMargin=1.7*cm, bottomMargin=1.7*cm,
                  title='M3 · C2 · Agonistas de GLP-1 · Cronograma', author='Dra. Omidres Pérez de Carvelli'
                  ).build(E, onFirstPage=pie, onLaterPages=pie)
print('generado', out)
