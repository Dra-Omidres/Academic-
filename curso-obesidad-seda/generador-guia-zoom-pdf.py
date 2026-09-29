# -*- coding: utf-8 -*-
"""Guía rápida de grabación en Zoom, en PDF, para anclar en el grupo de ponentes.

Acompaña al video tutorial. Es el documento que abre quien no vio el video, o quien lo
vio hace tres semanas y hoy le toca grabar.
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, Table, TableStyle, KeepTogether, PageBreak)

TEAL  = colors.HexColor('#0D5A62')
GOLD  = colors.HexColor('#B8852B')
MINT  = colors.HexColor('#C8E1DF')
PALE  = colors.HexColor('#EDF5F4')
WARM  = colors.HexColor('#FBF1DC')
INK   = colors.HexColor('#1A2325')
MUTED = colors.HexColor('#5F7073')

S = lambda **k: ParagraphStyle(**k)
st_tit  = S(name='t',  fontName='Helvetica-Bold', fontSize=19, leading=23, textColor=TEAL)
st_sub  = S(name='s',  fontName='Helvetica', fontSize=10, leading=14, textColor=MUTED)
st_sec  = S(name='se', fontName='Helvetica-Bold', fontSize=11.5, leading=14, textColor=colors.white)
st_num  = S(name='nu', fontName='Helvetica-Bold', fontSize=13, leading=15, textColor=GOLD)
st_txt  = S(name='x',  fontName='Helvetica', fontSize=9.3, leading=12.2, textColor=INK)
st_li   = S(name='li', fontName='Helvetica', fontSize=9.3, leading=12.2, textColor=INK,
            leftIndent=9, bulletIndent=1, spaceAfter=1.2)
st_avi  = S(name='av', fontName='Helvetica', fontSize=9.3, leading=12.2, textColor=INK)
st_pie  = S(name='pi', fontName='Helvetica', fontSize=7.5, leading=10, textColor=MUTED)

def marco(canv, doc):
    canv.saveState()
    if doc.page > 1:
        canv.setFillColor(PALE); canv.rect(0, A4[1]-13*mm, A4[0], 13*mm, stroke=0, fill=1)
        canv.setFillColor(MUTED); canv.setFont('Helvetica', 7.5)
        canv.drawString(18*mm, A4[1]-8.6*mm, 'Cómo grabar su clase · Curso virtual SEDA')
        canv.drawRightString(A4[0]-18*mm, A4[1]-8.6*mm, 'Página %d' % doc.page)
    canv.setStrokeColor(MINT); canv.setLineWidth(.6)
    canv.line(18*mm, 13*mm, A4[0]-18*mm, 13*mm)
    canv.setFillColor(MUTED); canv.setFont('Helvetica', 7)
    canv.drawString(18*mm, 9*mm, 'Sociedad de Endocrinología y Diabetes del Austro · SEDA')
    canv.drawRightString(A4[0]-18*mm, 9*mm, 'Dudas: escriba al grupo de ponentes')
    canv.restoreState()

doc = BaseDocTemplate('SEDA_Guia_Grabacion_Zoom.pdf', pagesize=A4,
                      leftMargin=18*mm, rightMargin=18*mm, topMargin=18*mm, bottomMargin=17*mm,
                      title='Cómo grabar su clase en Zoom · Curso virtual SEDA',
                      author='Sociedad de Endocrinología y Diabetes del Austro')
doc.addPageTemplates([PageTemplate(id='n',
    frames=[Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='f')],
    onPage=marco)])

W = doc.width

def seccion(txt):
    t = Table([[Paragraph(txt, st_sec)]], colWidths=[W])
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),TEAL),
                           ('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),
                           ('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4)]))
    return [Spacer(1, 2.8*mm), t, Spacer(1, 2*mm)]

def aviso(txt, fondo=WARM, borde=GOLD):
    t = Table([[Paragraph(txt, st_avi)]], colWidths=[W])
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),fondo),
                           ('LINEBEFORE',(0,0),(0,-1),2.2,borde),
                           ('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),
                           ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
    return t

def pasos(items):
    """Lista numerada con el número en dorado, alineado a la izquierda."""
    filas = [[Paragraph('%d' % i, st_num), Paragraph(txt, st_txt)]
             for i, txt in enumerate(items, 1)]
    t = Table(filas, colWidths=[9*mm, W-9*mm])
    t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),
                           ('TOPPADDING',(0,0),(-1,-1),2.6),('BOTTOMPADDING',(0,0),(-1,-1),2.6),
                           ('LEFTPADDING',(0,0),(0,-1),0),
                           ('LINEBELOW',(0,0),(-1,-2),.35,MINT)]))
    return t

def bullets(items, estilo=st_li):
    return [Paragraph(x, estilo, bulletText='·') for x in items]

F = []

# ---------------- página 1 ----------------
F += [Paragraph('Cómo grabar su clase', st_tit),
      Spacer(1, 3*mm),
      Paragraph('Curso virtual de actualización en obesidad, diabetes, nutrición clínica y salud '
                'digital · SEDA<br/>Guía rápida de dos páginas. Acompaña al video tutorial.',
                st_sub),
      Spacer(1, 4*mm),
      aviso('<b>Lo esencial en tres líneas.</b> Grabe desde una <b>computadora</b>, nunca desde el '
            'celular. Use <b>audífonos con micrófono</b>: el audio importa más que la imagen. Y '
            'cuando termine, <b>no cierre la computadora</b> hasta que Zoom acabe de convertir el '
            'video.')]

F += seccion('1 · Antes de sentarse a grabar')
F += [pasos([
    'Una <b>computadora</b> con Zoom instalado y sesión iniciada. Desde el celular no se puede '
    'grabar en el equipo.',
    'El <b>fondo virtual del curso</b> descargado. Se lo enviamos por el grupo; es el mismo para '
    'todos.',
    'Su <b>presentación abierta</b>, en la primera diapositiva.',
    'Sus <b>audífonos con micrófono</b> conectados. Los de cualquier celular sirven.',
])]

F += seccion('2 · La luz')
F += bullets([
    '<b>La luz va delante de usted, nunca detrás.</b> Si hay una ventana, siéntese mirándola. Con '
    'la ventana a la espalda, la cámara la deja en sombra.',
    'De noche: una <b>lámpara detrás de la pantalla</b>, apuntando a su cara, un poco por encima '
    'de los ojos.',
    '<b>La luz del techo sola no sirve</b>: cae desde arriba y marca ojeras. Súmele siempre una '
    'luz de frente.',
    'Si puede elegir, <b>grabe de día</b> con luz de ventana. Es la mejor luz y es gratis.',
])

F += seccion('3 · La cámara')
F += bullets([
    '<b>Altura:</b> la cámara a la altura de sus ojos. Si la computadora está en la mesa, la está '
    'mirando desde abajo. <b>Póngala sobre unos libros</b> hasta que la camarita quede a la altura '
    'de su mirada.',
    '<b>Inclinación:</b> con la computadora ya levantada, incline la pantalla un poco hacia atrás, '
    'hasta que la cámara le quede de frente y no apuntando al techo.',
    '<b>Distancia:</b> más o menos un brazo extendido de la pantalla.',
    '<b>Encuadre:</b> cabeza y hombros, con un dedo de espacio por encima de la cabeza. Ni la cara '
    'llenando la pantalla, ni usted pequeña y lejos.',
    '<b>Mire a la camarita</b>, no a su propia imagen. Ayuda pegar un papelito de color al lado de '
    'la cámara y hablarle a él.',
])

F += [PageBreak()]

# ---------------- página 2 ----------------
F += seccion('4 · El fondo y la ropa')
F += bullets([
    '<b>Sepárese de la pared</b> medio metro o más. Pegada a la pared, el fondo virtual le recorta '
    'los hombros y el pelo.',
    '<b>Evite rayas finas y cuadros pequeños:</b> la cámara los convierte en un temblor que marea.',
    '<b>Evite el blanco puro y el negro puro.</b> Un color sólido de tono medio siempre sale bien.',
])

F += seccion('5 · El sonido — lo más importante')
F += [Paragraph('Una imagen regular se perdona; un audio malo, no. Antes de empezar:', st_txt),
      Spacer(1, 2*mm)]
F += bullets([
    '<b>Audífonos con micrófono</b>, no el micrófono de la computadora, que recoge todo el eco.',
    'Cierre la ventana si hay ruido de calle.',
    'Apague el <b>ventilador o el aire acondicionado</b>: zumban más de lo que uno cree.',
    'Celular <b>en silencio de verdad</b>, no en vibrador.',
    'Avise en casa que va a estar grabando media hora.',
])

F += seccion('6 · Grabar en Zoom, paso a paso')
F += [pasos([
    'Abra Zoom y haga clic en <b>Nueva reunión</b>. Va a entrar usted sola: es su estudio de '
    'grabación.',
    'Cuando pregunte por el audio, <b>Entrar con el audio del computador</b>. Si no, graba sin '
    'sonido y no tiene arreglo.',
    '<b>Pruebe el micrófono:</b> flechita junto al ícono del micrófono → <i>Configuración de '
    'audio</i> → <i>Probar micrófono</i>. Confirme que el micrófono elegido es el de sus audífonos.',
    '<b>Ponga el fondo:</b> flechita junto al ícono de la cámara → <i>Elegir fondo virtual</i> → '
    'el signo <b>+</b> → busque la imagen del curso. Queda guardado para la próxima vez.',
    '<b>Comparta su presentación:</b> botón verde <i>Compartir pantalla</i> → elija la ventana de '
    'su presentación, no toda la pantalla → <i>Compartir</i>.',
    '<b>Grabe:</b> botón <i>Grabar</i> → si le da opciones, <b>Grabar en este computador</b>.',
    '<b>Verifique:</b> arriba a la izquierda tiene que decir <i>Grabando</i>. Si no lo dice, no '
    'está grabando.',
    '<b>Espere cinco segundos en silencio</b> antes de empezar a hablar. Nos deja margen limpio '
    'para cortar.',
    'Dé su clase. <b>Si se equivoca, no empiece de nuevo:</b> quédese callada tres segundos y '
    'repita la frase desde el principio. Eso se corta.',
])]

F += seccion('7 · Al terminar — donde más gente pierde su trabajo')
F += [pasos([
    'Tres segundos en silencio antes de tocar nada.',
    '<b>Detener grabación</b> → <b>Finalizar</b> → <b>Finalizar la reunión para todos</b>.',
    'Zoom empieza a <b>convertir</b> el video y le muestra una barrita. <b>No cierre la '
    'computadora, no la apague, no cierre esa ventana.</b> Déjela terminar sola; puede tardar '
    'unos minutos.',
    'Al terminar <b>se abre una carpeta</b>. Su clase es el archivo <b>zoom_0.mp4</b> o de nombre '
    'parecido. Si cerró la carpeta: está en <i>Documentos → Zoom →</i> carpeta con la fecha de hoy.',
    'Envíelo por el enlace que le pasamos en el grupo. <b>Pesa demasiado para mandarlo por '
    'correo.</b>',
])]

F += [Spacer(1, 3.5*mm),
      aviso('<b>El consejo que ahorra una grabación entera: haga una prueba de un minuto.</b><br/>'
            'Antes de grabar los treinta minutos, grabe uno solo, deténgalo y <b>ábralo y véalo</b>. '
            'En ese minuto descubre si el micrófono era el correcto, si la luz le da de frente, si '
            'la cámara está a buena altura y si el fondo le recorta los hombros. Todo eso se '
            'arregla en dos minutos ahora, y no se arregla nunca si lo descubre al final de la '
            'clase.', PALE, TEAL),
      Spacer(1, 4*mm),
      Paragraph('¿Algo no le sale? Escriba al grupo de ponentes. Preguntar no le quita seriedad a '
                'nadie: ninguno de nosotros estudió medicina para esto.', st_pie)]

doc.build(F)
print('SEDA_Guia_Grabacion_Zoom.pdf generado')
