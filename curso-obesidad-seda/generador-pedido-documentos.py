# -*- coding: utf-8 -*-
import html, urllib.parse, json, openpyxl

_wb = openpyxl.load_workbook('/home/user/Academic-/curso-obesidad-seda/SEDA_Matriz_Ponentes_Curso_Obesidad.xlsx')
_p = _wb['Ponentes - datos aval']
_v = _wb['Vacantes por cubrir']
GESTION = {}
for _r in range(4, 15):
    _c = _v.cell(_r, 2).value
    if _c and _v.cell(_r, 5).value:
        GESTION[_c] = (_v.cell(_r, 5).value, _v.cell(_r, 7).value or "")
def _tel(v):
    return "".join(ch for ch in str(v or "") if ch.isdigit())

ESPECIALIDAD = {}
for _r in range(4, 19):
    _k = _tel(_p.cell(_r, 6).value)
    if _k:
        ESPECIALIDAD[_k] = (_p.cell(_r, 3).value or "").strip()

FECHAS = {"M1":"jueves 29 de octubre","M2":"jueves 29 de octubre","M3":"jueves 5 de noviembre",
          "M4":"jueves 12 de noviembre","M5":"jueves 19 de noviembre","M6":"jueves 26 de noviembre",
          "M7":"jueves 3 de diciembre"}
TEMAS = {
 "M1 · C1":"Epidemiología y nuevos conceptos de obesidad","M1 · C2":"Fisiopatología moderna de la obesidad",
 "M1 · C3":"Evaluación integral del paciente con obesidad","M1 · C4":"Composición corporal y sarcopenia",
 "M2 · C1":"Principios de terapia nutricional","M2 · C2":"Patrones alimentarios basados en evidencia",
 "M2 · C3":"Nutrición conductual","M3 · C1":"Farmacoterapia para obesidad",
 "M3 · C2":"Agonistas del receptor de GLP-1","M3 · C3":"Tirzepatida y nuevas terapias",
 "M4 · C1":"Fisiopatología y clasificación de la diabetes","M4 · C2":"Monitoreo glucémico y metas terapéuticas",
 "M4 · C3":"Terapia farmacológica moderna","M4 · C4":"Insulinoterapia avanzada",
 "M5 · C4":"Composición corporal y sarcopenia en pacientes con diabetes",
 "M6 · C1":"Enfermedad renal asociada a obesidad y diabetes","M6 · C2":"Riesgo cardiovascular en obesidad y diabetes",
 "M6 · C3":"Síndrome cardiorrenometabólico","M6 · C4":"MASLD, sarcopenia y complicaciones metabólicas",
}

# nombre, trato, wa, clases, estado, faltan, nota
P = [
 ("Lcda. Isabel Reinoso","Isabel","+593 98 736 8816",["M2 · C1"],"CONFIRMADO",
  ["hoja de vida","número de cédula","fotografía","declaración de conflicto de interés firmada"],None),
 ("Dra. Johanna Piedra Bravo","Johanna","+593 98 765 4330",["M2 · C2"],"CONFIRMADO",
  ["número de cédula","fotografía","declaración de conflicto de interés firmada"],
  "Su hoja de vida ya llegó."),
 ("Dra. Janeth Bermeo","Janeth","+593 96 198 1203",["M2 · C3"],"CONFIRMADO",
  ["hoja de vida","número de cédula","fotografía","declaración de conflicto de interés firmada"],
  "Aceptó el 22/09. Es la fecha más apretada del curso: su módulo abre el programa."),
 ("Dr. Frank Espinoza","doctor","+51 936 260 715",["M3 · C2"],"CONFIRMADO",
  ["hoja de vida","número de cédula o pasaporte","fotografía","declaración de conflicto de interés firmada"],
  "Número de Perú. Si ejerce fuera de Ecuador, pídale pasaporte en lugar de cédula."),
 ("Dra. Teresa Cuatecontzi","doctora","+52 1 55 5405 6619",["M3 · C3"],"CONFIRMADO",
  ["hoja de vida","número de pasaporte","fotografía","declaración de conflicto de interés firmada"],
  "México. El «1» del número es el prefijo antiguo de móviles; si el enlace no abre, use el alterno."),
 ("Dra. Josefa Palacio Riofrío","doctora","+593 96 816 1654",["M4 · C2"],"CONFIRMADO",
  ["fotografía","declaración de conflicto de interés firmada"],
  "Ya envió hoja de vida y cédula. Es la más completa del grupo."),
 ("Dr. Chih Hao Chen Ku","doctor","+506 8392 7083",["M6 · C2","M6 · C3"],"CONFIRMADO",
  ["número de pasaporte","fotografía"],
  "Ya se le pidió por correo el 23/09. Use este mensaje solo si no responde."),
 ("Dra. Adriana Alvarez","doctora","+54 9 11 6708-1708",["M6 · C4"],"CONFIRMADO",
  ["hoja de vida","número de pasaporte","fotografía","declaración de conflicto de interés firmada"],
  "Número de Argentina. Confirmar dónde ejerce."),
 ("Dra. Lizbet Ruilova","Liz","+593 99 907 3471",["M1 · C1","M5 · C4"],"POR CONFIRMAR",
  ["número de cédula","fotografía","declaración de conflicto de interés firmada"],
  "Presidenta de SEDA. Su hoja de vida ya llegó. Falta su aceptación por escrito de sus dos clases."),
 ("Dr. Pablo Vanegas","Pablo","+593 98 765 3136",["M1 · C2","M3 · C1"],"POR CONFIRMAR",
  ["hoja de vida","número de cédula","fotografía","declaración de conflicto de interés firmada"],
  "Coordinador académico."),
 ("Dra. María Augusta Astudillo","doctora","+593 99 811 1635",["M1 · C3","M4 · C1"],"POR CONFIRMAR",
  ["hoja de vida","número de cédula","fotografía","declaración de conflicto de interés firmada"],None),
 ("Dra. Gabriela Jiménez","doctora","+593 99 807 8964",["M1 · C4","M4 · C3"],"POR CONFIRMAR",
  ["hoja de vida","número de cédula","fotografía","declaración de conflicto de interés firmada"],None),
 ("Dr. Juan Molina","doctor","+593 99 862 5711",["M4 · C4"],"POR CONFIRMAR",
  ["hoja de vida","número de cédula","fotografía","declaración de conflicto de interés firmada"],None),
 ("Dra. Valeria Andrade","doctora","+593 98 335 5686",["M6 · C1"],"POR CONFIRMAR",
  ["hoja de vida","número de cédula","fotografía","declaración de conflicto de interés firmada"],None),
]

VAC = [
 ("M2 · C4","Actividad física en obesidad",
  "Ejercicio aeróbico · entrenamiento de fuerza · prescripción de ejercicio",
  "Medicina del deporte, fisiatría o fisioterapia","M2","urgente",
  "Su módulo abre el curso. Es la única vacante con fecha de octubre."),
 ("M3 · C4","Cirugía bariátrica",
  "Indicaciones · técnicas quirúrgicas · seguimiento metabólico",
  "Cirujano bariátrico y metabólico acreditado","M3","",
  "La gestiona la Dra. Lizbet Ruilova. Es la única que le queda a ella."),
 ("M5 · C1","Nutrición de precisión en diabetes y obesidad",
  "Fenotipos metabólicos · individualización nutricional",
  "Nutricionista clínico o endocrinólogo con línea en nutrición de precisión","M5","",
  "El módulo 5 está entero sin ponente: se le puede ofrecer completo a una sola persona."),
 ("M5 · C2","Estrategias nutricionales basadas en evidencia",
  "Dieta mediterránea · restricción de carbohidratos · ayuno intermitente",
  "Nutricionista clínico con experiencia en diabetes","M5","",None),
 ("M5 · C3","Nutrición durante las terapias para obesidad",
  "Agonistas de GLP-1 · tirzepatida · preservación de la masa muscular",
  "Nutricionista clínico o endocrinólogo","M5","",
  "Tema de alta demanda: es el mejor gancho para reclutar."),
 ("M7 · C2","Monitoreo digital y tecnologías en diabetes y obesidad",
  "MCG y AGP en entornos digitales · monitoreo remoto, apps y wearables · salud conectada",
  "Endocrinólogo con experiencia en MCG o tecnología en diabetes","M7","",None),
 ("M7 · C3","Terapéutica digital, IA y educación del paciente",
  "Terapias digitales (DTx) · IA en tamizaje y apoyo a la decisión · educación digital y adherencia",
  "Informática médica o IA aplicada a salud","M7","",
  "Perfil difícil de encontrar en Cuenca: conviene sondear ya aunque la entrega sea en diciembre."),
]

AD_HON = ("Una cosa antes de que prepare nada, para que no haya malentendidos: la participación docente es "
          "ad honorem, la mía incluida. El curso va a cobrar inscripción, pero eso se destina a la plataforma, "
          "la certificación y el trámite del aval ante la Universidad de Cuenca.")

def lista(items):
    if len(items)==1: return items[0]
    return ", ".join(items[:-1]) + " y " + items[-1]

def saludo(trato):
    return trato if trato in ("Isabel","Johanna","Janeth","Liz","Pablo") else ("doctor" if trato=="doctor" else "doctora")

def bloque_clases(clases):
    out=[]
    for c in clases:
        mod=c.split(" · ")[0]
        out.append("%s\n%s · 30 minutos grabados\nEntrega de la grabación: %s" % (TEMAS[c], c.replace(" · C",", Clase ").replace("M","Módulo "), FECHAS[mod]))
    return "\n\n".join(out)

COORD = ("Liz","Pablo")

def mensaje(nombre,trato,clases,estado,faltan):
    s = saludo(trato)
    coord = trato in COORD
    if coord:
        cab = "%s, ¿cómo estás? Te escribe Omidres." % s
    elif s in ("Isabel","Johanna","Janeth"):
        cab = "Hola %s, ¿cómo está? Le escribe Omidres Pérez." % s
    else:
        cab = "Hola, %s, ¿cómo está? Le escribe Omidres Pérez, endocrinóloga." % s
    if estado=="CONFIRMADO":
        return "\n\n".join([
          cab,
          "Le confirmo su participación en el curso virtual de la Sociedad de Endocrinología y Diabetes del Austro:",
          bloque_clases(clases),
          AD_HON,
          "Y le pido un favor: estamos armando el expediente del aval y me faltan de usted %s." % lista(faltan),
          "¿Me los puede enviar a info@draomidresperez.com? Si me llegan antes del 2 de octubre, quedamos al día.",
          "Le paso por aquí la plantilla de diapositivas del curso y el formato de la declaración. La primera lámina de la plantilla trae las instrucciones y hay que borrarla antes de grabar.",
          "¡Mil gracias y un abrazo!"])
    else:
        n = "esta clase" if len(clases)==1 else "estas dos clases"
        return "\n\n".join([p for p in [
          cab + ("" if coord else " Estoy apoyando a Liz Ruilova y a Pablo Vanegas con el curso virtual de la Sociedad de Endocrinología y Diabetes del Austro."),
          ("Te escribo por algo de trámite, no de fondo. En el programa figuras con %s:" % n) if coord
            else ("Usted figura en el programa con %s:" % n),
          bloque_clases(clases),
          ("Para el expediente del aval necesito tu aceptación por escrito, aunque suene absurdo pidiéndotela a ti. La Universidad pide constancia de cada docente y la tuya es la única que no tengo en papel. Con que me respondas este mensaje diciendo que sí, me sirve." if coord
            else "Antes de seguir necesito confirmarlo con usted directamente: ¿contamos con su participación? Se lo pregunto porque el expediente del aval ante la Universidad de Cuenca lleva el nombre de cada docente y no quiero poner el suyo sin que usted me lo diga."),
          ("Y dejo dicho, para que quede parejo: estoy manejando el curso como participación ad honorem para todo el cuerpo docente, yo incluida. Así se lo dije a los demás ponentes y así quedó en el correo al Dr. Ojeda." if coord else AD_HON),
          ("Y me faltarían de ti %s. A info@draomidresperez.com cuando puedas." % lista(faltan)) if coord
            else ("Si me dice que sí, le paso enseguida la plantilla de diapositivas y le pediría %s para el expediente, a info@draomidresperez.com." % lista(faltan)),
          "¡Un abrazo!" if coord else "Y si no le calza, dígame con toda confianza: preferimos saberlo ahora.",
          "" if coord else "¡Un abrazo!"] if p])

GANCHO = {
 "M2 · C4": "y pensé en ti de una vez. Nadie mejor para esto:",
 "M3 · C4": "y me falta justo lo tuyo:",
 "M5 · C1": "y hay un tema que tiene tu nombre escrito:",
 "M5 · C2": "y hay un tema que es exactamente tu área:",
 "M5 · C3": "y hay un tema que es puro tú:",
 "M7 · C2": "y hay un tema para el que pensé en ti de inmediato:",
 "M7 · C3": "y me falta alguien para un tema que es tuyo:",
}
EXTRA = {
 "M2 · C4": "Lo único apretado es la fecha: la grabación tendría que estar el jueves 29 de octubre, porque ese módulo abre el curso. Si te resulta muy justo, dime y vemos.",
 "M5 · C1": "Y si te provoca, en ese mismo módulo tengo dos temas más de nutrición con la misma fecha. Puedes quedarte con uno o con los que quieras.",
 "M5 · C2": "Y si te provoca, en ese mismo módulo tengo dos temas más de nutrición con la misma fecha. Puedes quedarte con uno o con los que quieras.",
 "M5 · C3": "Te confieso que es el tema que más me están preguntando. Por eso quiero que lo dé alguien que lo maneje de verdad.",
 "M7 · C3": "Ese módulo lo coordino yo, así que trabajaríamos juntos de cerca.",
 "M7 · C2": "Ese módulo lo coordino yo, así que trabajaríamos juntos de cerca.",
}

FORMAL = {
 "M5 · C1": True,
}

def invitacion_formal(cod, tema, cont, fecha):
    return "\n\n".join([
      "Estimado/a Dr./Dra. [NOMBRE]:",
      "Reciba un cordial saludo.",
      "Le escribo en nombre de la Sociedad de Endocrinología y Diabetes del Austro (SEDA). "
      "Estamos organizando el *Curso virtual de actualización en obesidad, diabetes, "
      "nutrición clínica y salud digital*, cuyo aval académico se encuentra en trámite ante "
      "la Universidad de Cuenca.",
      "Me dirijo a usted para invitarle a integrar el cuerpo docente con el siguiente tema:",
      "*%s*\n%s" % (tema, cont),
      "Se trata de una clase grabada de treinta minutos, que usted prepara y graba cuando le "
      "resulte conveniente. Le haríamos llegar la plantilla institucional del curso y el "
      "formato de declaración de conflicto de interés. La grabación debería estar entregada "
      "el %s." % fecha,
      "El mismo módulo contempla otros dos temas de nutrición con idéntica fecha de entrega, "
      "por si fueran de su interés.",
      "Le señalo desde ahora, con toda transparencia, que la participación del cuerpo docente "
      "es ad honorem, la mía incluida. El curso tendrá un costo de inscripción destinado a la "
      "plataforma, la certificación y el trámite del aval universitario.",
      "Quedo atenta a su respuesta y con gusto le amplío cualquier detalle del programa. "
      "Si su agenda no se lo permitiera, le agradezco igualmente que me lo haga saber.",
      "Cordialmente,\n\nDra. Omidres Pérez de Carvelli\nEndocrinología · Medicina Interna"])

def invitacion(cod, tema, cont, fecha):
    if FORMAL.get(cod):
        return invitacion_formal(cod, tema, cont, fecha)
    return invitacion_cercana(cod, tema, cont, fecha)

def invitacion_cercana(cod, tema, cont, fecha):
    p = ["[NOMBRE], ¿cómo estás?",
         "Te escribo porque estoy metida de lleno con el curso virtual de SEDA "
         "—obesidad, diabetes, nutrición clínica y salud digital, con el aval de la "
         "Universidad de Cuenca en trámite— %s" % GANCHO[cod],
         "*%s*\n%s" % (tema, cont),
         "Es una clase grabada de 30 minutos, tú a tu ritmo. Te paso la plantilla del "
         "curso y listo. La grabación tendría que estar el %s." % fecha]
    if cod in EXTRA and cod != "M2 · C4":
        p.append(EXTRA[cod])
    elif cod == "M2 · C4":
        p[-1] = ("Es una clase grabada de 30 minutos, tú a tu ritmo. Te paso la plantilla "
                 "del curso y listo. " + EXTRA[cod])
    p += ["Te aviso de una vez, para que no haya sorpresas: es ad honorem, yo también. "
          "El curso va a cobrar inscripción, pero eso se va completo en la plataforma, "
          "los certificados y el trámite del aval.",
          "¿Te animas? Y si no te da la agenda, me lo dices con toda confianza, que no pasa nada.",
          "¡Un abrazo grande!"]
    return "\n\n".join(p)

def wa_digits(n): return "".join(ch for ch in n if ch.isdigit())

cards=[]
for i,(nombre,trato,wa,clases,estado,faltan,nota) in enumerate(P):
    msg = mensaje(nombre,trato,clases,estado,faltan)
    d = wa_digits(wa)
    alt = None
    if d.startswith("521"): alt = "52"+d[3:]
    link = "https://wa.me/%s?text=%s" % (d, urllib.parse.quote(msg))
    altlink = "https://wa.me/%s?text=%s" % (alt, urllib.parse.quote(msg)) if alt else None
    mods = sorted({c.split(" · ")[0] for c in clases})
    fecha_min = FECHAS[mods[0]]
    esp = ESPECIALIDAD.get(wa_digits(wa), "") or "especialidad no registrada"
    cards.append(dict(id="p%d"%i, nombre=nombre, esp=esp, wa=wa, estado=estado, clases=clases,
                      temas=[TEMAS[c] for c in clases], fecha=fecha_min, faltan=faltan,
                      nota=nota, msg=msg, link=link, altlink=altlink))

def esc(s): return html.escape(s, quote=True)

cards_html=[]
for c in cards:
    badge = "ok" if c["estado"]=="CONFIRMADO" else "pend"
    clases_html = "".join(
        '<li><span class="cod">%s</span> %s</li>' % (esc(cl), esc(t))
        for cl,t in zip(c["clases"], c["temas"]))
    faltan_html = "".join('<li>%s</li>' % esc(f) for f in c["faltan"])
    nota = '<p class="nota">%s</p>' % esc(c["nota"]) if c["nota"] else ""
    alt = ('<a class="btn ghost" href="%s" target="_blank" rel="noopener">Nº alterno</a>' % esc(c["altlink"])) if c["altlink"] else ""
    cards_html.append(f"""
<article class="card" data-estado="{badge}" id="{c['id']}">
  <header>
    <label class="done"><input type="checkbox" data-k="{c['id']}"><span>enviado</span></label>
    <h2>{esc(c['nombre'])}</h2>
    <p class="esp">{esc(c['esp'])}</p>
    <p class="tel">{esc(c['wa'])}</p>
    <span class="badge {badge}">{esc(c['estado'])}</span>
  </header>
  <ul class="clases">{clases_html}</ul>
  <p class="fecha">Entrega de la grabación: <strong>{esc(c['fecha'])}</strong></p>
  <div class="falta"><h3>Le falta enviar</h3><ul>{faltan_html}</ul></div>
  {nota}
  <details><summary>Ver el mensaje</summary><pre class="msg">{esc(c['msg'])}</pre></details>
  <div class="acciones">
    <a class="btn primary" href="{esc(c['link'])}" target="_blank" rel="noopener">Abrir en WhatsApp</a>
    {alt}
    <button class="btn ghost copy" type="button" data-id="{c['id']}">Copiar texto</button>
  </div>
  <textarea class="src" id="src-{c['id']}" readonly hidden>{esc(c['msg'])}</textarea>
</article>""")

vac_html=[]
for j,(cod,tema,cont,perfil,mod,urg,nota) in enumerate(VAC):
    msg = invitacion(cod, tema, cont, FECHAS[mod])
    nota_h = '<p class="nota">%s</p>' % esc(nota) if nota else ""
    ges = GESTION.get(cod)
    ges_h = ('<p class="ges"><strong>%s</strong><br>%s</p>' % (esc(ges[0]), esc(ges[1]))) if ges else ""
    urg_h = '<span class="badge urg">urgente</span>' if urg else ""
    vac_html.append(f"""
<article class="card vac" id="v{j}">
  <header>
    <span class="cod">{esc(cod)}</span>{urg_h}
    <h2>{esc(tema)}</h2>
  </header>
  <p class="cont">{esc(cont)}</p>
  <div class="falta"><h3>Perfil que se busca</h3><p>{esc(perfil)}</p></div>
  <p class="fecha">Entrega de la grabación: <strong>{esc(FECHAS[mod])}</strong></p>
  {ges_h}{nota_h}
  <details><summary>Ver la invitación</summary><pre class="msg">{esc(msg)}</pre></details>
  <div class="envio">
    <input class="inp nom" type="text" placeholder="Nombre de pila" autocomplete="off">
    <input class="inp tel" type="tel" placeholder="WhatsApp con código de país" autocomplete="off" inputmode="tel">
  </div>
  <div class="acciones">
    <button class="btn primary abrir" type="button" data-id="v{j}">Abrir en WhatsApp</button>
    <button class="btn ghost copy" type="button" data-id="v{j}">Copiar texto</button>
  </div>
  <textarea class="src" id="src-v{j}" readonly hidden>{esc(msg)}</textarea>
</article>""")

doc = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Pedido de documentos SEDA</title>
<style>
:root{
  --teal:#0D5A62; --teal2:#094247; --gold:#B8852B; --mint:#C8E1DF; --pale:#EDF5F4;
  --bg:#F7FAFA; --surface:#FFFFFF; --ink:#1A2325; --muted:#5F7073; --line:#DCE8E7;
  --ok:#0D5A62; --pend:#B8852B;
}
@media (prefers-color-scheme: dark){ :root:not([data-theme="light"]){
  --teal:#7FC5C4; --teal2:#A8DCDA; --gold:#E0AE5C; --mint:#123A3D; --pale:#0F2A2D;
  --bg:#0B1718; --surface:#122224; --ink:#E8F1F0; --muted:#94A9AB; --line:#1E3538;
  --ok:#7FC5C4; --pend:#E0AE5C;
}}
:root[data-theme="dark"]{
  --teal:#7FC5C4; --teal2:#A8DCDA; --gold:#E0AE5C; --mint:#123A3D; --pale:#0F2A2D;
  --bg:#0B1718; --surface:#122224; --ink:#E8F1F0; --muted:#94A9AB; --line:#1E3538;
  --ok:#7FC5C4; --pend:#E0AE5C;
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
  font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;}
.wrap{max-width:1140px;margin:0 auto;padding:32px 16px 72px}
header.top{border-bottom:2px solid var(--mint);padding-bottom:20px;margin-bottom:26px}
h1{font-size:clamp(22px,4vw,30px);margin:0 0 6px;color:var(--teal);letter-spacing:-.01em}
.sub{margin:0;color:var(--muted);font-size:14px}
.stats{display:flex;flex-wrap:wrap;gap:10px;margin:18px 0 0}
.stat{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:10px 14px;min-width:96px}
.stat b{display:block;font-size:20px;color:var(--teal);line-height:1.2}
.stat span{font-size:12px;color:var(--muted)}
.filtros{display:flex;gap:8px;flex-wrap:wrap;margin:22px 0 6px}
.f{background:var(--surface);border:1px solid var(--line);color:var(--muted);border-radius:999px;
   padding:7px 15px;font-size:13px;cursor:pointer;font-family:inherit}
.f[aria-pressed="true"]{background:var(--teal);border-color:var(--teal);color:var(--bg);font-weight:600}
.stat.ok b{color:var(--ok)} .stat.urg b{color:var(--pend)}
.secs{display:flex;gap:8px;margin:22px 0 4px;border-bottom:1px solid var(--line);flex-wrap:wrap}
.sec{background:none;border:none;border-bottom:3px solid transparent;color:var(--muted);
     font:600 15px/1 inherit;font-family:inherit;padding:11px 4px;margin-right:14px;cursor:pointer}
.sec em{font-style:normal;font-size:11px;background:var(--pale);color:var(--muted);
        border-radius:20px;padding:2px 7px;margin-left:6px;vertical-align:2px}
.sec[aria-selected="true"]{color:var(--teal);border-bottom-color:var(--teal)}
.sec[aria-selected="true"] em{background:var(--mint);color:var(--teal)}
.intro{margin:20px 0 0;font-size:14px;color:var(--muted);max-width:62ch}
.card.vac header{padding-right:0}
.card.vac h2{margin-top:9px}
.badge.urg{position:static;background:var(--pend);color:var(--bg);margin-left:7px}
.ges{margin:0;background:var(--mint);color:var(--teal);border-radius:9px;
     padding:10px 13px;font-size:12.5px;line-height:1.45}
.cont{margin:0;font-size:13.5px;color:var(--muted);line-height:1.5}
.falta p{margin:0;font-size:13px}
.envio{display:flex;flex-direction:column;gap:7px;margin-top:auto}
.inp{font:14px/1 inherit;font-family:inherit;padding:10px 12px;border-radius:8px;
     border:1px solid var(--line);background:var(--bg);color:var(--ink);width:100%}
.inp:focus{outline:2px solid var(--teal);outline-offset:1px}
.card.vac .acciones{margin-top:0}
.grid{display:grid;gap:16px;grid-template-columns:repeat(auto-fill,minmax(330px,1fr));margin-top:18px}
.card{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:18px;
      display:flex;flex-direction:column;gap:12px}
.card.hecho{opacity:.5}
.card header{position:relative;padding-right:92px}
.card h2{font-size:17px;margin:0;color:var(--teal);line-height:1.3}
.esp{margin:4px 0 0;font-size:12.5px;color:var(--gold);font-weight:600}
.tel{margin:2px 0 0;font-size:13px;color:var(--muted);font-variant-numeric:tabular-nums}
.badge{position:absolute;top:0;right:0;font-size:10px;letter-spacing:.06em;font-weight:700;
       padding:4px 8px;border-radius:5px;text-transform:uppercase}
.badge.ok{background:var(--mint);color:var(--ok)}
.badge.pend{background:transparent;border:1px solid var(--pend);color:var(--pend)}
.done{position:absolute;top:26px;right:0;display:flex;align-items:center;gap:5px;font-size:11px;color:var(--muted);cursor:pointer}
.clases{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:6px}
.clases li{font-size:14px;line-height:1.4}
.cod{display:inline-block;background:var(--pale);color:var(--teal);font-size:11px;font-weight:700;
     padding:2px 6px;border-radius:4px;margin-right:6px;white-space:nowrap}
.fecha{margin:0;font-size:13px;color:var(--muted)}
.fecha strong{color:var(--gold)}
.falta{background:var(--pale);border-radius:9px;padding:11px 13px}
.falta h3{margin:0 0 5px;font-size:11px;letter-spacing:.05em;text-transform:uppercase;color:var(--muted)}
.falta ul{margin:0;padding-left:17px;font-size:13px}
.falta li{margin:2px 0}
.nota{margin:0;font-size:12.5px;color:var(--muted);border-left:3px solid var(--gold);padding-left:10px}
details summary{cursor:pointer;font-size:13px;color:var(--teal);font-weight:600}
.msg{white-space:pre-wrap;font:13px/1.55 ui-monospace,SFMono-Regular,Menlo,monospace;
     background:var(--pale);border-radius:8px;padding:12px;margin:9px 0 0;overflow-x:auto}
.acciones{display:flex;gap:8px;flex-wrap:wrap;margin-top:auto;padding-top:4px}
.btn{font:600 13px/1 inherit;font-family:inherit;border-radius:8px;padding:10px 14px;cursor:pointer;
     text-decoration:none;display:inline-flex;align-items:center;border:1px solid transparent}
.primary{background:var(--teal);color:var(--bg)}
.ghost{background:transparent;border-color:var(--line);color:var(--teal)}
.src{position:absolute;left:-9999px}
footer{margin-top:44px;padding-top:18px;border-top:1px solid var(--line);font-size:12.5px;color:var(--muted)}
footer b{color:var(--teal)}
@media (max-width:480px){.grid{grid-template-columns:1fr}}
</style>
</head>
<body>
<div class="wrap">
<header class="top">
  <h1>Cuerpo docente del curso SEDA</h1>
  <p class="sub">Obesidad, diabetes, nutrición clínica y salud digital · inicio 5 de noviembre de 2026 · plazo de documentación 2 de octubre</p>
  <div class="stats">
    <div class="stat"><b>28</b><span>clases</span></div>
    <div class="stat ok"><b>11</b><span>confirmadas</span></div>
    <div class="stat"><b>10</b><span>por confirmar</span></div>
    <div class="stat urg"><b>7</b><span>vacantes</span></div>
    <div class="stat"><b>4/15</b><span>hojas de vida</span></div>
    <div class="stat"><b>1/15</b><span>declaración COI</span></div>
  </div>
</header>

<nav class="secs" role="tablist">
  <button class="sec" data-s="docs" aria-selected="true">Pedir documentos <em>14</em></button>
  <button class="sec" data-s="vac" aria-selected="false">Cubrir vacantes <em>7</em></button>
</nav>

<section id="s-docs">
<div class="filtros" role="group" aria-label="Filtros">
  <button class="f" data-f="todos" aria-pressed="true">Todos</button>
  <button class="f" data-f="ok" aria-pressed="false">Confirmados</button>
  <button class="f" data-f="pend" aria-pressed="false">Por confirmar</button>
  <button class="f" data-f="pendientes" aria-pressed="false">Sin enviar</button>
</div>

<div class="grid" id="grid">
__CARDS__
</div>
</section>

<section id="s-vac" hidden>
<p class="intro">Siete clases sin ponente. Escriba el nombre de pila y el WhatsApp de la persona a la que quiere invitar, y el botón abre la conversación con la invitación ya escrita.</p>
<div class="grid">
__VACANTES__
</div>
</section>

<footer>
<p><b>Cómo usarlo.</b> «Abrir en WhatsApp» abre la conversación con el mensaje ya escrito: usted solo revisa y pulsa enviar. No se envía nada solo. «Copiar texto» sirve si prefiere pegarlo a mano.</p>
<p><b>Adjunte los dos archivos.</b> El mensaje anuncia la plantilla de diapositivas y el formato de declaración de conflicto de interés. WhatsApp no permite adjuntarlos desde un enlace: adjúntelos usted en la misma conversación, después de enviar el texto.</p>
<p><b>La casilla «enviado»</b> se guarda solo en este navegador, en este equipo. No se comparte con nadie y no queda registrada en la matriz.</p>
<p><b>Dra. Cuatecontzi:</b> su número trae el prefijo «1» que México usaba para móviles. Si el enlace principal no abre la conversación, pruebe el botón «Nº alterno». No puedo confirmarle cuál de los dos formatos está vigente hoy.</p>
<p><b>Las vacantes.</b> El mensaje de invitación dice «[NOMBRE]» hasta que usted escriba el nombre de pila en la tarjeta. Si va a mandar la misma vacante a varias personas, hágalo de dos en dos y espere respuesta, o terminará con dos personas preparando la misma clase.</p>
<p>La Dra. Omidres no aparece en la lista de documentos porque es ella quien envía; sí dicta M7 · C1 y M7 · C4. Generado el 23 de septiembre de 2026 a partir de <b>SEDA_Matriz_Ponentes_Curso_Obesidad.xlsx</b>.</p>
</footer>
</div>

<script>
(function(){
  var K='seda-docs-enviados';
  var st={};
  try{ st=JSON.parse(localStorage.getItem(K)||'{}')||{}; }catch(e){ st={}; }
  function pinta(){
    document.querySelectorAll('.card').forEach(function(c){
      var b=c.querySelector('input[type=checkbox]');
      if(!b) return;
      b.checked=!!st[b.dataset.k];
      c.classList.toggle('hecho', b.checked);
    });
  }
  document.querySelectorAll('input[type=checkbox]').forEach(function(b){
    b.addEventListener('change',function(){
      st[b.dataset.k]=b.checked;
      try{ localStorage.setItem(K,JSON.stringify(st)); }catch(e){}
      pinta(); aplica();
    });
  });
  var filtro='todos';
  function aplica(){
    document.querySelectorAll('.card').forEach(function(c){
      var b=c.querySelector('input[type=checkbox]');
      var hecho=b&&b.checked;
      var ok = filtro==='todos' ? true
             : filtro==='pendientes' ? !hecho
             : c.dataset.estado===filtro;
      c.style.display = ok ? '' : 'none';
    });
  }
  document.querySelectorAll('.f').forEach(function(f){
    f.addEventListener('click',function(){
      filtro=f.dataset.f;
      document.querySelectorAll('.f').forEach(function(o){ o.setAttribute('aria-pressed', o===f ? 'true':'false'); });
      aplica();
    });
  });
  document.querySelectorAll('.copy').forEach(function(btn){
    btn.addEventListener('click',function(){
      var t=document.getElementById('src-'+btn.dataset.id);
      var txt=t.value;
      function fin(){ var o=btn.textContent; btn.textContent='Copiado'; setTimeout(function(){btn.textContent=o;},1400); }
      if(navigator.clipboard&&navigator.clipboard.writeText){
        navigator.clipboard.writeText(txt).then(fin,manual);
      } else { manual(); }
      function manual(){
        t.hidden=false; t.select(); t.setSelectionRange(0,999999);
        try{ document.execCommand('copy'); fin(); }catch(e){ alert('Seleccione el texto y cópielo a mano.'); }
        t.hidden=true;
      }
    });
  });
  pinta(); aplica();

  // secciones
  document.querySelectorAll('.sec').forEach(function(b){
    b.addEventListener('click',function(){
      document.querySelectorAll('.sec').forEach(function(o){ o.setAttribute('aria-selected', o===b ? 'true':'false'); });
      document.getElementById('s-docs').hidden = b.dataset.s!=='docs';
      document.getElementById('s-vac').hidden  = b.dataset.s!=='vac';
      window.scrollTo(0,0);
    });
  });

  // vacantes: arma el enlace con el nombre y el numero escritos
  document.querySelectorAll('.abrir').forEach(function(btn){
    btn.addEventListener('click',function(){
      var card=document.getElementById(btn.dataset.id);
      var nom=(card.querySelector('.nom').value||'').trim();
      var tel=(card.querySelector('.tel').value||'').replace(/\D/g,'');
      if(tel.length<8){ alert('Escriba el número de WhatsApp con código de país, por ejemplo +593 99 123 4567.'); card.querySelector('.tel').focus(); return; }
      var txt=document.getElementById('src-'+btn.dataset.id).value;
      if(nom) txt=txt.replace('[NOMBRE]',nom);
      window.open('https://wa.me/'+tel+'?text='+encodeURIComponent(txt),'_blank','noopener');
    });
  });
  // el boton copiar de una vacante tambien sustituye el nombre
  document.querySelectorAll('.vac .copy').forEach(function(btn){
    btn.addEventListener('click',function(){
      var card=document.getElementById(btn.dataset.id);
      var nom=(card.querySelector('.nom').value||'').trim();
      var t=document.getElementById('src-'+btn.dataset.id);
      if(nom && t.value.indexOf('[NOMBRE]')>-1) t.value=t.value.replace('[NOMBRE]',nom);
    }, true);
  });
})();
</script>
</body>
</html>
"""
doc = doc.replace("__CARDS__", "\n".join(cards_html)).replace("__VACANTES__", "\n".join(vac_html))
open('/home/user/Academic-/curso-obesidad-seda/SEDA_Pedido_Documentos_Ponentes.html','w',encoding='utf-8').write(doc)
print("cards:", len(cards), "| vacantes:", len(vac_html))
print("bytes:", len(doc))
