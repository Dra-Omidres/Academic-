# -*- coding: utf-8 -*-
"""Solicitud de aval académico a la Universidad de Cuenca y expediente del curso, en Word.

Lo que pide la Universidad, según la Comisión de Avales (29/09/2026, ver
aval-requisitos-ucuenca.md): la solicitud se dirige a la Decana de la Facultad de Ciencias
Médicas y se entrega en el Decanato; rige el artículo 7 del Reglamento Interno (objetivos,
contenidos, población, expositores con sus hojas de vida, cronograma, financiamiento) y
once puntos de evaluación.

Decisiones de la Dra. Omidres (13/10/2026): firma la Dra. Lizbet Ruilova como Presidenta de
SEDA; M5 · C2 la dicta la Lcda. Isabel Reinoso; expediente nuevo y completo.

El cuerpo docente, las clases y los contenidos salen de la matriz. Lo que falta decidir va
resaltado en amarillo dentro del documento, para que nadie lo entregue sin completarlo.

Salida: SEDA_Solicitud_Aval_UCuenca.docx
"""
import re, openpyxl, unicodedata
from difflib import SequenceMatcher
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_COLOR_INDEX, WD_BREAK
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

TEAL='0D5A62'; GOLD='B8852B'; PALE='EDF5F4'; INK='1A2325'; MUTED='5F7073'
def rgb(h): return RGBColor(int(h[:2],16), int(h[2:4],16), int(h[4:],16))

PUBLICA={'M1':'jueves 5 de noviembre','M2':'jueves 5 de noviembre','M3':'jueves 12 de noviembre',
         'M4':'jueves 19 de noviembre','M5':'jueves 26 de noviembre','M6':'jueves 3 de diciembre',
         'M7':'jueves 10 de diciembre'}

# ---------- datos de la matriz ----------
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

docentes=[]
r=4
while p.cell(r,2).value:
    docentes.append({'nombre':limpio(p.cell(r,2).value), 'esp':limpio(p.cell(r,3).value) or '—',
                     'inst':limpio(p.cell(r,4).value) or '—',
                     'cv':str(p.cell(r,10).value or '').strip().upper().startswith('SÍ'),
                     'clases':[]})
    r+=1
def docente_de(corto):
    tc=tokens(corto)
    return max(docentes, key=lambda d: puntaje(tc, tokens(d['nombre'])))

modulos=[]; clases=[]; i=0
for r in range(3,31):
    if not m.cell(r,3).value: continue
    mod='M%d' % (i//4+1); cod='%s · C%d' % (mod, i%4+1); i+=1
    if m.cell(r,1).value: modulos.append((mod, str(m.cell(r,1).value).split('. ',1)[-1]))
    d=docente_de(m.cell(r,5).value) if m.cell(r,5).value else None
    if d: d['clases'].append(cod)
    clases.append({'cod':cod,'mod':mod,'tema':str(m.cell(r,3).value).strip(),
                   'cont':str(m.cell(r,4).value or '').strip(), 'doc':d['nombre'] if d else None})
assert len(clases)==28
vacantes=[c['cod'] for c in clases if not c['doc']]
for c in clases:
    if not c['doc']: c['doc']='Por confirmar'
docentes=[d for d in docentes if d['clases']]
docentes.sort(key=lambda d: sorted(d['clases'])[0])
sin_cv=[d['nombre'] for d in docentes if not d['cv']]

# ---------- documento ----------
doc=Document()
for s in doc.sections:
    s.top_margin=Cm(2.2); s.bottom_margin=Cm(2); s.left_margin=Cm(2.5); s.right_margin=Cm(2.3)
st=doc.styles['Normal']; st.font.name='Arial'; st.font.size=Pt(10.5)
st.element.rPr.rFonts.set(qn('w:eastAsia'),'Arial')

def run(par, txt, b=False, i=False, color=INK, size=None, resaltar=False):
    r=par.add_run(txt); r.bold=b; r.italic=i; r.font.color.rgb=rgb(color)
    if size: r.font.size=Pt(size)
    if resaltar: r.font.highlight_color=WD_COLOR_INDEX.YELLOW
    return r

def par(txt='', b=False, i=False, color=INK, size=None, align=None, antes=0, despues=6, resaltar=False):
    q=doc.add_paragraph(); q.paragraph_format.space_before=Pt(antes); q.paragraph_format.space_after=Pt(despues)
    if align: q.alignment=align
    if txt: _mixto(q, txt, b, i, color, size, resaltar)
    return q

def _mixto(q, txt, b=False, i=False, color=INK, size=None, resaltar=False):
    """**negrita** y [[resaltado]] dentro del texto."""
    for trozo in re.split(r'(\*\*.+?\*\*|\[\[.+?\]\])', txt):
        if not trozo: continue
        if trozo.startswith('**'): run(q, trozo[2:-2], True, i, color, size, resaltar)
        elif trozo.startswith('[['): run(q, trozo[2:-2], True, i, INK, size, True)
        else: run(q, trozo, b, i, color, size, resaltar)

def titulo(txt):
    q=par(txt, b=True, color=TEAL, size=12.5, antes=12, despues=6)
    q.paragraph_format.keep_with_next=True
    return q

def vineta(txt):
    q=doc.add_paragraph(style='List Bullet'); q.paragraph_format.space_after=Pt(3)
    _mixto(q, txt); return q

def sombra(celda, color):
    tcPr=celda._tc.get_or_add_tcPr(); shd=OxmlElement('w:shd')
    shd.set(qn('w:val'),'clear'); shd.set(qn('w:color'),'auto'); shd.set(qn('w:fill'),color); tcPr.append(shd)

def tabla(filas, anchos, cab=True, size=9):
    t=doc.add_table(rows=len(filas), cols=len(filas[0])); t.style='Table Grid'
    t.alignment=WD_TABLE_ALIGNMENT.CENTER
    t.autofit=False
    for ci,w in enumerate(anchos):
        t.columns[ci].width=Cm(w)
        gc=t._tbl.tblGrid.findall(qn('w:gridCol'))
        if ci<len(gc): gc[ci].set(qn('w:w'), str(int(Cm(w).twips)))
    for ri,f in enumerate(filas):
        for ci,v in enumerate(f):
            c=t.cell(ri,ci); c.width=Cm(anchos[ci]); c.paragraphs[0].paragraph_format.space_after=Pt(0)
            if cab and ri==0:
                sombra(c, TEAL); run(c.paragraphs[0], v, True, color='FFFFFF', size=size)
            else:
                if ci==0 and not cab: sombra(c, PALE)
                _mixto(c.paragraphs[0], v, b=(ci==0 and not cab), size=size)
    doc.add_paragraph().paragraph_format.space_after=Pt(2)
    return t

# ===== 1 · Carta de solicitud =====
par('Cuenca, ____ de octubre de 2026', align=WD_ALIGN_PARAGRAPH.RIGHT, despues=14)
for l in ['Doctora','Nancy Auquilla Díaz','Decana (e) de la Facultad de Ciencias Médicas','Universidad de Cuenca']:
    par(l, b=(l=='Nancy Auquilla Díaz'), despues=0)
par('Presente.', despues=12)
par('**Asunto:** Solicitud de aval académico para el «Curso virtual de actualización en obesidad, diabetes, '
    'nutrición clínica y salud digital»', despues=12)
par('De mi consideración:', despues=8)
cuerpo=[
 'Reciba un cordial saludo. En mi calidad de Presidenta de la **Sociedad de Endocrinología y Diabetes del Austro '
 '(SEDA)**, me permito solicitar a usted, y por su intermedio a la Comisión de Avales y al Consejo Directivo de la '
 'Facultad, el **aval académico de la Universidad de Cuenca** para el **Curso virtual de actualización en obesidad, '
 'diabetes, nutrición clínica y salud digital**, que nuestra Sociedad dictará del **5 de noviembre al 17 de diciembre '
 'de 2026**.',
 'La obesidad y la diabetes tipo 2 son hoy dos de los principales problemas de salud pública de la región, y su '
 'abordaje ha cambiado de forma sustancial en los últimos años con la llegada de nuevas terapias farmacológicas, de la '
 'nutrición basada en evidencia y de las herramientas de salud digital. El curso busca que los profesionales de la '
 'salud que atienden a estas personas incorporen esos avances a su práctica diaria, con un enfoque integral y '
 'aplicable a la consulta.',
 'El programa consta de **siete módulos y veintiocho clases grabadas**, con un valor curricular de **20 horas**, en '
 'modalidad virtual en la plataforma **saludelearning.com**. Está dirigido a médicos generales y especialistas, '
 'nutricionistas y otros profesionales de la salud, con un cupo de **200 participantes**, y lo dicta un cuerpo '
 'docente de especialistas del Ecuador, México, Costa Rica, Perú, Argentina, Colombia y España.',
 'Adjunto el expediente con la información que establece el artículo 7 del Reglamento Interno y los puntos de '
 'evaluación que nos indicó la Comisión de Avales, junto con las hojas de vida del cuerpo docente.',
 'Para cualquier aclaración, la coordinación académica del curso está a cargo de la **Dra. Omidres Pérez de '
 'Carvelli** (info@draomidresperez.com), quien atenderá con gusto cualquier requerimiento de la Comisión.',
 'Agradezco de antemano la atención que brinde a la presente.',
]
for c in cuerpo:
    q=par(c, align=WD_ALIGN_PARAGRAPH.JUSTIFY, despues=8)
par('Atentamente,', antes=6, despues=46)
par('**Dra. Lizbet Yolanda Ruilova González**', despues=0)
par('Presidenta', despues=0)
par('Sociedad de Endocrinología y Diabetes del Austro (SEDA)', despues=0)
doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)

# ===== 2 · Expediente =====
par('EXPEDIENTE PARA EL AVAL ACADÉMICO', b=True, color=GOLD, size=10, despues=2)
par('Curso virtual de actualización en obesidad, diabetes, nutrición clínica y salud digital', b=True, color=TEAL, size=15, despues=2)
par('Sociedad de Endocrinología y Diabetes del Austro (SEDA) · Cuenca, Ecuador', color=MUTED, despues=10)

titulo('1. Datos generales')
tabla([
 ['Entidad organizadora','Sociedad de Endocrinología y Diabetes del Austro (SEDA)'],
 ['Fecha','Del jueves 5 de noviembre al jueves 17 de diciembre de 2026 (siete semanas)'],
 ['Lugar','Curso virtual. La entidad organizadora tiene su sede en Cuenca, Ecuador'],
 ['Modalidad y plataforma','Virtual asincrónica, en la plataforma saludelearning.com'],
 ['Población objetivo','Médicos generales y especialistas, nutricionistas y otros profesionales de la salud'],
 ['Cupos disponibles','200 participantes'],
 ['Valor curricular','20 horas: 14 horas de clases grabadas (28 clases de 30 minutos) y 6 horas de estudio autónomo con lecturas y material complementario por módulo'],
 ['Tipo de certificado','De participación, emitido por SEDA con el aval académico de la Universidad de Cuenca'],
 ['Entidades auspiciantes','Boehringer Ingelheim, Laboratorios Elea y Laboratorio Saval (ver sección 7)'],
 ['Costo de inscripción','El curso contempla un costo de inscripción, cuyo valor fija la directiva de SEDA. Se comunicará a la Comisión antes de abrir las inscripciones'],
 ['Coordinación académica','Dra. Omidres Pérez de Carvelli'],
], [5, 11.2], cab=False, size=9.5)

titulo('2. Objetivos')
par('**Objetivo general**', despues=3)
par('Actualizar a los profesionales de la salud en el abordaje integral y basado en evidencia de la obesidad y la '
    'diabetes, integrando la evaluación clínica, la nutrición, el tratamiento farmacológico y quirúrgico, la prevención '
    'de complicaciones y las herramientas de salud digital.', align=WD_ALIGN_PARAGRAPH.JUSTIFY)
par('**Objetivos específicos.** Al finalizar el curso, el participante estará en capacidad de:', despues=3)
for o in [
 'Reconocer la obesidad como enfermedad crónica, comprender su fisiopatología y evaluar de forma integral al paciente, incluida la composición corporal.',
 'Aplicar los principios de la terapia nutricional, los patrones alimentarios con evidencia, el abordaje conductual y la prescripción de actividad física en el manejo de la obesidad.',
 'Indicar y dar seguimiento al tratamiento farmacológico de la obesidad y reconocer las indicaciones de la cirugía bariátrica y metabólica.',
 'Diagnosticar y clasificar la diabetes, establecer metas terapéuticas con las herramientas actuales de monitoreo glucémico e individualizar el tratamiento farmacológico y la insulinoterapia.',
 'Diseñar estrategias de terapia nutricional para las personas con diabetes y obesidad, incluidas las que reciben nuevas terapias farmacológicas.',
 'Identificar y abordar las complicaciones cardiorrenometabólicas asociadas a la obesidad y la diabetes.',
 'Incorporar a la práctica clínica las herramientas de salud digital y telemedicina, con criterios de ética y protección de datos.',
]: vineta(o)

titulo('3. Contenidos y programación detallada')
par('Cada clase es un video de 30 minutos. Los módulos se publican en la plataforma los jueves, en las fechas indicadas, '
    'y permanecen disponibles hasta el cierre del curso.', align=WD_ALIGN_PARAGRAPH.JUSTIFY)
for mod, nom in modulos:
    q=par('Módulo %s · %s' % (mod[1], nom), b=True, color=TEAL, antes=6, despues=2)
    q.paragraph_format.keep_with_next=True
    par('Publicación: %s de 2026' % PUBLICA[mod], i=True, color=MUTED, size=9, despues=3).paragraph_format.keep_with_next=True
    filas=[['Clase','Tema y contenidos','Expositor','Duración']]
    for c in [c for c in clases if c['mod']==mod]:
        filas.append([c['cod'], '**%s**\n%s' % (c['tema'], c['cont']), c['doc'], '30 min'])
    tabla(filas, [1.6, 8.6, 4.4, 1.6], size=8.5)

titulo('4. Cronograma')
filas=[['Semana','Fecha de publicación','Contenido']]
sem=[('1','jueves 5 de noviembre','Módulos 1 y 2'),('2','jueves 12 de noviembre','Módulo 3'),
     ('3','jueves 19 de noviembre','Módulo 4'),('4','jueves 26 de noviembre','Módulo 5'),
     ('5','jueves 3 de diciembre','Módulo 6'),('6','jueves 10 de diciembre','Módulo 7'),
     ('7','jueves 17 de diciembre','Cierre del curso y emisión de certificados')]
for s in sem: filas.append(list(s))
tabla(filas, [2, 5, 9.2], size=9)

titulo('5. Cuerpo docente')
par('Las hojas de vida se adjuntan como anexo, en el formato propio de cada docente. La participación del cuerpo '
    'docente es ad honorem.', align=WD_ALIGN_PARAGRAPH.JUSTIFY)
filas=[['Docente','Especialidad','Institución · ciudad y país','Clases']]
for d in docentes:
    filas.append([d['nombre'], d['esp'], d['inst'], ' / '.join(sorted(d['clases']))])
tabla(filas, [4.4, 4.6, 5, 2.2], size=8.5)
if vacantes:
    par('**Docente por confirmar:** %s. La Sociedad comunicará a la Comisión el nombre y la hoja de vida en cuanto se confirme.' % ', '.join(vacantes), size=9)
if sin_cv:
    par('**Hojas de vida en trámite:** %s. Se remitirán a la Comisión en cuanto se reciban.' % '; '.join(sin_cv), size=9)

titulo('6. Financiamiento')
par('El curso se financia con el auspicio de la industria farmacéutica y con el costo de inscripción que fije la directiva de la Sociedad. '
    'El auspicio ingresa a la Sociedad de Endocrinología y Diabetes del Austro, que con esos recursos contrata la '
    'plataforma y su gestión operativa.', align=WD_ALIGN_PARAGRAPH.JUSTIFY)

titulo('7. Auspicio y transparencia')
for t in [
 'El curso cuenta con el auspicio de **Boehringer Ingelheim, Laboratorios Elea y Laboratorio Saval**. Los auspiciantes '
 'no intervienen en la selección de docentes, en la definición de los contenidos ni en la elaboración del material, y no '
 'revisan las clases antes de su publicación. Los docentes se comprometen a emplear denominaciones genéricas y a no '
 'promover marcas comerciales ni productos específicos.',
 'El curso se dicta en la plataforma saludelearning.com, operada por **Omisalud Cía. Ltda.** (RUC 0190491641001), '
 'compañía de la cual la coordinadora académica, Dra. Omidres Pérez de Carvelli, es socia con el 50 % del capital social '
 'y ejerce la Presidencia. La Sociedad contrata el uso de la plataforma y su gestión operativa (montaje del curso, '
 'soporte a los participantes, matrículas y certificados) mediante factura emitida por Omisalud Cía. Ltda. y cancelada '
 'en su cuenta corporativa nacional. Los auspiciantes no realizan pago alguno a la compañía. La coordinadora académica '
 'no participó en la decisión de contratación, que corresponde a la Sociedad.',
 'La participación de todo el cuerpo docente es ad honorem, incluida la de la coordinadora académica, quien no percibe '
 'remuneración alguna por la coordinación ni por la docencia. Tiene a su cargo dos clases: «Agonistas del receptor de '
 'GLP-1» y «Fundamentos de salud digital y telemedicina en enfermedades crónicas». En la primera, como en todo el curso, '
 'se emplean exclusivamente denominaciones genéricas y no se promueve ningún producto comercial.',
 'Los docentes declaran sus posibles conflictos de interés. Las declaraciones firmadas recibidas a la fecha se '
 'adjuntan como anexo.',
]: par(t, align=WD_ALIGN_PARAGRAPH.JUSTIFY, despues=7)

titulo('8. Anexos')
vineta('**Anexo 1.** Hojas de vida del cuerpo docente (%d de %d).' % (len(docentes)-len(sin_cv), len(docentes)))
vineta('**Anexo 2.** Declaraciones de conflicto de interés recibidas a la fecha.')

doc.core_properties.title='Solicitud de aval académico — Curso virtual SEDA'
doc.core_properties.author='Sociedad de Endocrinología y Diabetes del Austro'
doc.save('SEDA_Solicitud_Aval_UCuenca.docx')
print('generado ·', len(docentes), 'docentes ·', len(clases), 'clases · sin hoja de vida:', sin_cv)
