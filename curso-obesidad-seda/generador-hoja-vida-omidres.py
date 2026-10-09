# -*- coding: utf-8 -*-
"""Hoja de vida de la Dra. Omidres Pérez de Carvelli para el expediente del aval.

Se rehace desde el contenido del PDF de junio de 2026, con una corrección: el
Proyecto TED2 LATAM figuraba como «Jun 2025 – Jul 2026» bajo «cargos actuales»,
y sigue vigente.
"""
import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, Table, TableStyle, Image, KeepTogether)

TEAL=colors.HexColor('#0D5A62'); GOLD=colors.HexColor('#B8852B')
MINT=colors.HexColor('#C8E1DF'); PALE=colors.HexColor('#EDF5F4')
WARM=colors.HexColor('#FBF1DC'); INK=colors.HexColor('#1A2325')
MUTED=colors.HexColor('#5F7073')

MESES=['enero','febrero','marzo','abril','mayo','junio','julio','agosto',
       'septiembre','octubre','noviembre','diciembre']
_h=datetime.date.today()
HOY='%s de %d' % (MESES[_h.month-1], _h.year)

FOTO='activos/foto-omidres-hoja-vida.jpg'

st=lambda **k: ParagraphStyle(**k)
S_nom  = st(name='nom', fontName='Helvetica-Bold', fontSize=16.5, leading=19, textColor=TEAL)
S_esp  = st(name='esp', fontName='Helvetica', fontSize=8.6, leading=12, textColor=GOLD)
S_con  = st(name='con', fontName='Helvetica', fontSize=8, leading=11.5, textColor=MUTED)
S_sec  = st(name='sec', fontName='Helvetica-Bold', fontSize=9.6, leading=12, textColor=colors.white)
S_txt  = st(name='txt', fontName='Helvetica', fontSize=8.5, leading=12.2, textColor=INK, alignment=TA_JUSTIFY)
S_item = st(name='item',fontName='Helvetica', fontSize=8.4, leading=11.6, textColor=INK,
            leftIndent=7, firstLineIndent=-7)
S_dato = st(name='dato',fontName='Helvetica', fontSize=8.3, leading=11.4, textColor=INK)
S_sub  = st(name='sub', fontName='Helvetica-BoldOblique', fontSize=8.4, leading=11, textColor=TEAL)

def marco(canv, doc):
    canv.saveState()
    canv.setFillColor(TEAL); canv.rect(0, A4[1]-9*mm, A4[0], 9*mm, stroke=0, fill=1)
    canv.setFillColor(GOLD); canv.rect(0, A4[1]-10.2*mm, A4[0], 1.2*mm, stroke=0, fill=1)
    canv.setFillColor(colors.white); canv.setFont('Helvetica-Bold', 7.4)
    canv.drawString(15*mm, A4[1]-6.2*mm, 'DRA. OMIDRES PÉREZ DE CARVELLI')
    canv.setFont('Helvetica', 7.4)
    canv.drawRightString(A4[0]-15*mm, A4[1]-6.2*mm,
                         'Medicina Interna · Endocrinología · Telemedicina')
    canv.setStrokeColor(MINT); canv.setLineWidth(.5)
    canv.line(15*mm, 11*mm, A4[0]-15*mm, 11*mm)
    canv.setFillColor(MUTED); canv.setFont('Helvetica', 6.8)
    canv.drawString(15*mm, 7.4*mm, 'Hoja de vida · actualizada en %s' % HOY)
    canv.drawRightString(A4[0]-15*mm, 7.4*mm, 'Página %d' % canv.getPageNumber())
    canv.restoreState()

doc=BaseDocTemplate('SEDA_HojaVida_Omidres_Perez.pdf', pagesize=A4,
    leftMargin=15*mm, rightMargin=15*mm, topMargin=15*mm, bottomMargin=14*mm,
    title='Hoja de vida — Dra. Omidres Pérez de Carvelli',
    author='Dra. Omidres Pérez de Carvelli')
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

def entrada(cargo, resto):
    return Paragraph('<b>%s</b>&nbsp; <font color="#5F7073">%s</font>' % (cargo, resto), S_item)

def vinetas(items, estilo=S_item):
    return [Paragraph('•&nbsp; '+i, estilo) for i in items]

F=[]

# ---------- portada ----------
izq=[Paragraph('Dra. Omidres de la Consolación<br/>Pérez de Carvelli', S_nom), Spacer(1,1.6*mm),
     Paragraph('Medicina Interna · Endocrinología y Metabolismo · Diabetología · '
               'Telemedicina y salud digital', S_esp), Spacer(1,2.2*mm),
     Paragraph('info@draomidresperez.com &nbsp;·&nbsp; www.draomidresperez.com '
               '&nbsp;·&nbsp; @draomidres', S_con)]
port=Table([[izq, Image(FOTO, width=27*mm, height=33.9*mm)]],
           colWidths=[W-31*mm, 31*mm])
port.setStyle(TableStyle([('VALIGN',(0,0),(0,0),'MIDDLE'),('VALIGN',(1,0),(1,0),'TOP'),
    ('ALIGN',(1,0),(1,0),'RIGHT'),('LEFTPADDING',(0,0),(-1,-1),0),
    ('RIGHTPADDING',(0,0),(-1,-1),0),('TOPPADDING',(0,0),(-1,-1),0),
    ('BOTTOMPADDING',(0,0),(-1,-1),0),('LINEBELOW',(0,0),(-1,-1),1.4,GOLD)]))
F += [port, Spacer(1,4*mm)]

# ---------- perfil ----------
perfil=Table([[Paragraph(
 'Médico internista endocrinóloga venezolana con más de 25 años de trayectoria clínica, '
 'científica e institucional en América Latina. Pionera en telemedicina especializada en '
 'diabetes en la región, autora del método PCP para consulta en línea —publicado en su '
 'libro <i>Controlando la Diabetes en un Click</i> (2020)— y coordinadora del Proyecto '
 'TED2 LATAM, programa híbrido de atención especializada en diabetes con resultados '
 'clínicos demostrables (HbA1c −0,51 %; n=200; Veracruz, México). Fundadora y presidenta '
 'de la Organización Internacional de Telemedicina y Telesalud (OITT), co-autora de las '
 'Guías de Buenas Prácticas en Telemedicina y Diabetes ALAD–OITT 2025, Chief Medical '
 'Officer LATAM de MEDDI Hub a.s. (Praga) e investigadora acreditada del Sistema Nacional '
 'de Ciencia y Tecnología del Ecuador.', S_txt)]], colWidths=[W])
perfil.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),WARM),
    ('LINEBEFORE',(0,0),(0,-1),2.2,GOLD),('LEFTPADDING',(0,0),(-1,-1),8),
    ('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),6),
    ('BOTTOMPADDING',(0,0),(-1,-1),6)]))
F.append(perfil)

# ---------- información personal ----------
F += seccion('INFORMACIÓN PERSONAL')
datos=[('Nacionalidad','Venezolana'),
       ('Fecha de nacimiento','7 de octubre de 1971'),
       ('Cédula ecuatoriana','096127908-0'),
       ('Cédula venezolana','V-11.007.782'),
       ('Registro MSP Ecuador','116694452'),
       ('Investigadora acreditada SENESCYT','INV-25-08756')]
celdas=[[Paragraph('<b>%s</b><br/>%s'%(k,v), S_dato) for k,v in datos[i:i+3]]
        for i in (0,3)]
ti=Table(celdas, colWidths=[W/3.0]*3)
ti.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),6),
    ('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),
    ('BACKGROUND',(0,0),(-1,-1),PALE),('LINEBELOW',(0,0),(-1,0),.5,colors.white)]))
F.append(ti)

# ---------- formación ----------
F += seccion('FORMACIÓN ACADÉMICA')
F += [entrada(c,r) for c,r in [
 ('Médico Cirujano','Universidad de Oriente, Núcleo Anzoátegui, Venezuela · 1988–1998'),
 ('Especialista en Medicina Interna','Universidad Central de Venezuela — Hospital Vargas, Caracas · 2000–2003'),
 ('Especialista en Endocrinología y Metabolismo','RAP Hospital Vargas de Caracas, UCV · 2003–2006'),
 ('Fellow en Patología Tiroidea','Hospital Vargas de Caracas · 2006–2007'),
 ('MBA en Transformación Digital','IEBS Business School, España · 2025'),
 ('Diplomado Internacional en Telemedicina','Universidad Tecnológica del Centro (UNITEC) · 2020'),
 ('Diplomado Internacional en Teleodontología','Universidad Tecnológica del Centro (UNITEC) · 2020'),
 ('Diplomado Universitario en Formación Docente para Educación Superior','FundaUDO Sucre, 216 horas · 2009'),
 ('Coach Former en Salud y Bienestar','Instituto Latinoamericano de Coaching y Terapia (ILACOT) · 2014–2015'),
]]

F += seccion('TÍTULOS Y DISTINCIONES')
F += vinetas([
 'Doctorado <i>Honoris Causa</i> en Ciencias de la Salud — SIISDET, con aval de la Universidad Autónoma de Chiriquí (UNACHI), Panamá · enero de 2025',
 'Investigadora Acreditada — SENESCYT Ecuador, en Endocrinología, Telemedicina y Salud Digital · mayo de 2025 · credencial INV-25-08756',
 'Premio al Líder en Investigación y Ciencias de la Salud para el Beneficio de la Humanidad 2021–2022 — SIISDET',
 'Premio Dr. Moros Ghersi a la mejor tesis del año 2003 — Sociedad Venezolana de Medicina Interna',
 'Certificado al Mérito — American College of Physicians, capítulo Venezuela · 2004',
])

# ---------- cargos ----------
F += seccion('CARGOS INSTITUCIONALES ACTUALES')
F += [entrada(c,r) for c,r in [
 ('Médico especialista en Medicina Interna y Endocrinología','Hospital Universitario del Río, Cuenca, Ecuador · desde septiembre de 2018'),
 ('Presidenta y miembro fundadora','Organización Internacional de Telemedicina y Telesalud (OITT) · desde 2022'),
 ('Coordinadora — Proyecto TED2 LATAM','Telemedicina Especializada en Diabetes tipo 2, Veracruz, México (n=200) · desde junio de 2025'),
 ('Chief Medical Officer LATAM','MEDDI Hub a.s., Praga, República Checa · desde 2022 · representante Ecuador–LATAM desde 2021'),
 ('Directora del Diplomado Internacional de Telemedicina','Salud eLearning — Universidad Tecnológica del Centro · desde 2020'),
 ('Presidenta y CEO','Omisalud Cía. Ltda. · desde mayo de 2020'),
 ('Revisora técnica','Revista INSPILIP — MSP Ecuador · desde 2022'),
 ('Coordinadora general','Guías de Buenas Prácticas en Telemedicina y Diabetes en LATAM y el Caribe — ALAD/OITT · 2025'),
 ('Colaboradora técnica','Norma Técnica de Telesalud del MSP Ecuador, Acuerdo Ministerial 00044-2025, como representante de la OITT · 2025'),
 ('Terapeuta fundadora','Programa MeTTAS® de peso saludable y cambio de estilo de vida · desde 2015'),
]]

F += seccion('CARGOS ANTERIORES RELEVANTES')
F += [entrada(c,r) for c,r in [
 ('Presidenta','Asociación Iberoamericana de Telesalud y Telemedicina · 2021–2022'),
 ('Especialista en Endocrinología','CCQA Hospital del Día IESS Azogues — comité de ética e investigación · 2017–2019'),
 ('Especialista en Endocrinología','Hospital General IESS Quevedo · 2016–2017'),
 ('Directora y especialista en Endocrinología','Unidad Endocrino Metabólica de Oriente (UNEMOR), Cumaná, Venezuela · 2009–2016'),
 ('Coordinadora Región Andina · Secretaria del Comité de Ética','Asociación Latinoamericana de Diabetes (ALAD) · 2016–2019'),
 ('Delegada por Venezuela','Asociación Latinoamericana de Diabetes (ALAD) · 2011–2013'),
 ('Vicepresidenta y vocal directiva','Federación Nacional de Diabetes de Venezuela (Fenadiabetes) · 2008–2015'),
 ('Adjunta del Servicio de Medicina Interna','Hospital Carlos J. Bello — Cruz Roja, Caracas · 2005–2008'),
 ('Adjunta del Servicio de Endocrinología','Hospital Vargas de Caracas · 2007'),
]]

# ---------- publicaciones ----------
F += seccion('PUBLICACIONES EN REVISTAS INDEXADAS')
pubs=[
 'Pérez de Carvelli O. Validación del método PCP en telemedicina: evaluación de la satisfacción y adherencia del paciente. <i>INSPILIP — Rev. Ecuatoriana de Ciencia, Tecnología e Innovación en Salud Pública.</i> 2025;9(30). inspilip.gob.ec/index.php/inspi/article/view/822',
 'Pérez de Carvelli O. Optimizing diabetes management with personalized telemedicine. <i>Diabetes Technology &amp; Therapeutics</i> (ATTD). 2019. doi:10.1089/dia.2019.2525.abstracts',
 'Pérez de Carvelli O. Niveles de 25-OH vitamina D en la población del CCQA Hospital del Día de Azogues — IESS, 2017. <i>Rev. méd. Hosp. José Carrasco Arteaga.</i> 2017;10(2):133-138',
 'Pérez de Carvelli O, et al. Incidencia de hipertensión arterial en DM2 del Hospital Vargas de Caracas. <i>Archivos del Hospital Vargas.</i> 2004;46(1-4):61-66',
 'Pérez de Carvelli O, et al. Parámetros antropométricos en DM2 del Hospital Vargas de Caracas. <i>Archivos del Hospital Vargas.</i> 2004;46(1-4):67-73',
 'Pérez de Carvelli O, et al. Incidencia de microalbuminuria en pacientes diabéticos del Hospital Vargas. <i>Archivos del Hospital Vargas.</i> 2003;45(3-4):20-25',
 'Pérez de Carvelli O, et al. Neuropatía diabética periférica: correlación entre la escala de Toronto y la bioestesiometría. <i>Rev. Soc. Venezolana de Medicina Interna.</i> 2003',
 'Pérez de Carvelli O, et al. Human herpesvirus 8 variants in Venezuelan patients with AIDS-related Kaposi sarcoma. <i>Clinical Infectious Diseases.</i> 2003;36:385-386',
 'Pérez de Carvelli O, et al. Asociación de tuberculosis ganglionar y ocular en paciente no-VIH. <i>Archivos del Hospital Vargas.</i> 2002;44:223-227',
 'Pérez de Carvelli O, et al. Sífilis terciaria en pacientes con infección por VIH. <i>Archivos del Hospital Vargas.</i> 2001;43:223-228',
]
F += [Paragraph('%d.&nbsp; %s'%(i+1,p), S_item) for i,p in enumerate(pubs)]
F += [Spacer(1,2*mm), Paragraph('En proceso de publicación', S_sub),
      Paragraph('Pérez de Carvelli O, Zuzuarregui Benítez DC, Hernández Mendoza J. '
        '«Bridging the diabetes care gap through specialised telemedicine: implementation '
        'and early outcomes of the TED2 LATAM programme in Veracruz, Mexico». '
        '<i>Salud Pública de México</i> (destino primario) · <i>Revista Venezolana de '
        'Endocrinología y Metabolismo</i> (destino secundario).', S_item)]

F += seccion('LIBROS Y CAPÍTULOS')
F += vinetas([
 '<b>Autora.</b> <i>Controlando la Diabetes en un Click: cómo ayudar efectivamente a los pacientes a través de consultas en línea vía telemedicina.</i> ISBN 9798586160003. 1.ª ed., diciembre de 2020. Prólogo del Dr. Juan Rosas, expresidente de ALAD',
 '<b>Autora.</b> <i>Diabetes: guía de consejos médicos para pacientes y sus familiares.</i> ISBN 9798587050143. Amazon, 2020 (reedición); 1.ª ed. Magenta Ediciones, 2010',
 '<b>Coautora.</b> <i>Transforma tu consulta al mundo digital.</i> Amazon, 2020',
 '<b>Coautora.</b> <i>Autismo, ¿por dónde comenzar?</i> Amazon, 2021',
 '<b>Coautora del capítulo</b> «Microalbuminuria: significado clínico en la nefropatía diabética y tratamiento», en <i>Diez años de avances en diabetes mellitus</i>, Chacín L. Litografía Normacolor, 2004, pp. 99-126',
 '<b>Revisora y redactora de la introducción</b> de <i>Taller de manejo práctico de la diabetes 2008.</i> Fenadiabetes',
])

F += seccion('NORMAS Y DOCUMENTOS TÉCNICOS OFICIALES')
F += vinetas([
 '<b>Colaboradora técnica</b> — Norma Técnica de Telesalud del Ministerio de Salud Pública del Ecuador, Acuerdo Ministerial 00044-2025, como representante de la OITT. Quito, 2025 · salud.gob.ec',
 '<b>Coordinadora general</b> — Guías de Buenas Prácticas en Telemedicina y Diabetes en LATAM y el Caribe 2025. ALAD–OITT, 2025',
])

# ---------- conferencias ----------
F += seccion('ACTIVIDAD COMO CONFERENCISTA (SELECCIÓN)')
F += [Paragraph('Internacional', S_sub)]
F += vinetas([
 'II Encuentro Científico NUTRIANDFARM — ponente invitada. Loja, Ecuador (2026)',
 'XIX Congreso ALAD. Cusco, Perú (noviembre de 2025)',
 'Conferencia de Consenso sobre Disglucemia en Perú, DBCD 2025 — UPCH (noviembre de 2025)',
 '1.er Congreso Latinoamericano de Autocuidado ILAR/OITT — ponente. São Paulo, Brasil (2023)',
 '3.er Congreso Internacional de Atención Domiciliaria — ponente. ACISD, Colombia (septiembre de 2023)',
 'Foro del Día Mundial de la Diabetes — ponente. Federación Mexicana de Diabetes (noviembre de 2023)',
 'XXXII Congreso Nacional de Diabetes — ponente invitada. FMD, México (septiembre de 2022)',
 'XIX Congreso Internacional de la Sociedad Ecuatoriana de Endocrinología — ponencia «Control glicémico a partir de un click». Guayaquil (julio de 2022)',
 'ATTD — Advanced Technologies &amp; Treatments for Diabetes, resumen publicado (2019)',
 'American Diabetes Association, 67.ª y 68.ª Scientific Sessions. Chicago y San Francisco (2007 y 2008)',
 'XII Congreso ALAD. La Habana, Cuba (2007)',
])
F += [Spacer(1,1.6*mm), Paragraph('Ecuador', S_sub)]
F += vinetas([
 'Evento NEUROBION, mes de la diabetes — Procter &amp; Gamble Ecuador (noviembre de 2025)',
 'XX Congreso de la Sociedad Ecuatoriana de Endocrinología de Manabí — ponente. Manta (septiembre de 2024)',
 'Conferencia «Optimizando el metabolismo celular» (octubre de 2024)',
 'Evento de telemedicina en Cuenca — conferencista. Medicamenta Ecuador (septiembre de 2022)',
 'Congreso Internacional de Endocrinología y Diabetes AECE (2022)',
 'XVII Congreso Ecuatoriano de Endocrinología. Quito (octubre de 2018)',
])

F += seccion('MEMBRESÍAS Y ASOCIACIONES CIENTÍFICAS')
F += vinetas([
 'Presidenta fundadora — Organización Internacional de Telemedicina y Telesalud (OITT), 2022–2026',
 'Presidenta — Asociación Iberoamericana de Telesalud y Telemedicina, 2021–2022',
 'Miembro de la Asociación Latinoamericana de Diabetes (ALAD) desde 2007 · coordinadora de la Región Andina y secretaria del Comité de Ética, 2016–2019',
 'Miembro del American College of Physicians desde 2006',
 'Miembro titular de la Sociedad Venezolana de Medicina Interna y de la Sociedad Venezolana de Endocrinología y Metabolismo',
 'Miembro de la Sociedad de Endocrinología y Diabetes del Austro desde 2018',
 'Integrante de los grupos redactores de guías nacionales y latinoamericanas: nefropatía diabética (ALAD), tratamiento de la diabetes, patología tiroidea, síndrome metabólico, diabetes y embarazo (SVEM) y enfermedad cardiovascular en la mujer',
])

F += seccion('DOCENCIA Y ASESORÍA')
F += vinetas([
 'Directora del Diplomado Internacional de Telemedicina — Salud eLearning / UNITEC, desde 2020',
 'Docente colaboradora del Curso ALAD de prevención, diagnóstico y tratamiento de la diabetes, <b>avalado por la Universidad de Cuenca</b> y el MSP del Ecuador (2018)',
 'Facilitadora de cursos de Coach en Salud y Bienestar — ILACOT, 2015–2024',
 'Asesora de tesis de pregrado — Universidad de Oriente, Venezuela (2005, 2015 y 2016)',
 'Medical advisor — Roche Farmacéutica y Sanofi Aventis, Venezuela',
 'Conferencista para la industria farmacéutica: Merck, MSD, Novartis, Roche, Sanofi Aventis, Lilly y Pfizer',
 'Columnista científica — <i>El Nacional</i> (Caracas), <i>El Comercio</i> (Cuenca), <i>Región</i> (Sucre) y <i>La Prensa de Monagas</i>',
])

F += seccion('FORMACIÓN COMPLEMENTARIA E IDIOMAS')
F += vinetas([
 'Curso Intensivo de Diabetes, Endocrinología y Enfermedades Metabólicas — Escuela de Medicina Keck, USC. Miami (2007 y 2008)',
 'Capacitación de la American Diabetes Association para el programa Unidos contra la Diabetes. São Paulo (2008)',
 'Curso de diagnóstico de osteoporosis con certificación en densitometría — IOF. Venezuela (2007)',
 'Curso básico del Grupo Latinoamericano de Epidemiología de la Diabetes (GLED). Venezuela (2006)',
 'Programa EMPRENDE — IESA, Venezuela, 80 horas (2016)',
 'Instituto Scharovsky de Hipnosis Clínica Reparadora. Buenos Aires (2015)',
 'Formaciones en neuromarketing y marketing digital desde 2015',
 '<b>Idiomas:</b> español nativo · inglés profesional (comunicación científica, ponencias internacionales y publicaciones)',
])

doc.build(F)
print('generado')
