# -*- coding: utf-8 -*-
import openpyxl, html, io

wb = openpyxl.load_workbook('SEDA_Matriz_Ponentes_Curso_Obesidad.xlsx')
p, m = wb['Ponentes - datos aval'], wb['Matriz 28 clases']

MOD = {'M1':'Fundamentos de obesidad','M2':'Nutrición en obesidad','M3':'Farmacoterapia y cirugía',
       'M4':'Diabetes','M5':'Nutrición en diabetes','M6':'Complicaciones','M7':'Salud digital'}
PAIS = {'+51':'🇵🇪 Perú','+52':'🇲🇽 México','+54':'🇦🇷 Argentina','+57':'🇨🇴 Colombia',
        '+506':'🇨🇷 Costa Rica','+593':'🇪🇨 Ecuador'}

def pais(t):
    for pre in sorted(PAIS, key=len, reverse=True):
        if t.startswith(pre): return PAIS[pre]
    return ''

gente, sin_tel = [], []
for r in range(4, 26):
    n = p.cell(r,2).value
    if not n: continue
    tel = p.cell(r,6).value
    fila = dict(n=n, tel=tel or '', esp=p.cell(r,3).value or '',
                cl=p.cell(r,9).value or '', esta=str(p.cell(r,14).value or ''))
    (gente if tel else sin_tel).append(fila)

# ordenar por módulo y clase
def clave(f):
    c = f['cl']
    return (c[:2] if c[:1]=='M' else 'Z9', c)
gente.sort(key=clave)

DESC = """Curso virtual de actualización en obesidad, diabetes, nutrición clínica y salud digital · Sociedad de Endocrinología y Diabetes del Austro (SEDA).

7 módulos · 28 clases grabadas de 30 minutos · inicio 5 de noviembre de 2026 · aval académico de la Universidad de Cuenca en trámite.

Coordinación: Dra. Lizbet Ruilova y Dr. Pablo Vanegas.
Organización del cuerpo docente: Dra. Omidres Pérez de Carvelli.

Documentos y consultas: info@draomidresperez.com"""

BIENVENIDA = """¡Bienvenidos y bienvenidas!

Este grupo es para coordinar el curso virtual de SEDA. Somos docentes de Ecuador, México, Costa Rica, Perú, Argentina y Colombia, y aquí vamos a resolver lo práctico sin llenarnos de correos.

*Lo esencial:*

• Cada clase es una grabación de 30 minutos
• Se graba por Zoom; les paso el enlace y coordinamos día y hora uno por uno
• Cada módulo entrega su grabación 7 días antes de publicarse, así que cada quien tiene una fecha distinta. La suya ya se la envié por privado
• El curso arranca el 5 de noviembre y cierra el 17 de diciembre

*Lo que necesito de cada uno, si aún no me lo ha enviado:*

  1. Hoja de vida resumida
  2. Cédula o pasaporte
  3. Fotografía profesional
  4. Declaración de conflicto de interés firmada

A info@draomidresperez.com. Es lo que exige el expediente del aval ante la Universidad de Cuenca, y sin eso no puedo presentarlo.

*Dos cosas más:*

La participación docente es ad honorem, la mía incluida.

A cada quien le envié por privado qué cubre su clase y qué cubren las demás, para que no se pisen los temas. Si al preparar la suya ve que algo se cruza, dígamelo y lo acomodamos — mejor ahora que cuando ya esté grabado.

Cualquier duda, por aquí o por privado. ¡Gracias por sumarse!"""

e = lambda s: html.escape(str(s), quote=True)

filas = []
for i, f in enumerate(gente):
    mod = f['cl'][:2] if f['cl'][:1]=='M' else ''
    filas.append(f"""
<li class="p" id="m{i}">
  <label class="chk"><input type="checkbox" data-k="m{i}"><span></span></label>
  <div class="who">
    <b>{e(f['n'])}</b>
    <span class="meta">{e(f['cl'])}{' · '+e(MOD.get(mod,'')) if mod in MOD else ''}{' · '+e(f['esp']) if f['esp'] else ''}</span>
  </div>
  <div class="num"><code id="t{i}">{e(f['tel'])}</code><span class="pais">{pais(f['tel'])}</span></div>
  <button class="btn copy" type="button" data-t="t{i}">Copiar</button>
</li>""")

pend = "".join(f"<li><b>{e(f['n'])}</b> — {e(f['cl']) or 'sin tema asignado'}</li>" for f in sin_tel)

doc = """<!DOCTYPE html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Grupo de ponentes SEDA</title>
<style>
:root{--teal:#0D5A62;--gold:#B8852B;--mint:#C8E1DF;--pale:#EDF5F4;--bg:#F7FAFA;
  --surface:#FFF;--ink:#1A2325;--muted:#5F7073;--line:#DCE8E7;--wa:#128C7E}
@media(prefers-color-scheme:dark){:root:not([data-theme="light"]){--teal:#7FC5C4;--gold:#E0AE5C;
  --mint:#123A3D;--pale:#0F2A2D;--bg:#0B1718;--surface:#122224;--ink:#E8F1F0;--muted:#94A9AB;
  --line:#1E3538;--wa:#25D366}}
:root[data-theme="dark"]{--teal:#7FC5C4;--gold:#E0AE5C;--mint:#123A3D;--pale:#0F2A2D;--bg:#0B1718;
  --surface:#122224;--ink:#E8F1F0;--muted:#94A9AB;--line:#1E3538;--wa:#25D366}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
  font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
.wrap{max-width:840px;margin:0 auto;padding:30px 16px 70px}
h1{font-size:clamp(21px,4vw,28px);margin:0 0 6px;color:var(--teal)}
.sub{margin:0;color:var(--muted);font-size:14px}
h2{font-size:15px;letter-spacing:.04em;text-transform:uppercase;color:var(--muted);
  margin:34px 0 12px;padding-bottom:7px;border-bottom:1px solid var(--line)}
.paso{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:16px 18px;margin:0 0 14px}
.paso ol{margin:0;padding-left:20px} .paso li{margin:6px 0;font-size:14.5px}
.campo{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:15px 17px;margin:0 0 12px}
.campo h3{margin:0 0 8px;font-size:13px;letter-spacing:.03em;text-transform:uppercase;color:var(--muted)}
.campo pre{white-space:pre-wrap;margin:0 0 11px;font:13.5px/1.55 inherit;background:var(--pale);
  border-radius:8px;padding:12px 14px;max-height:230px;overflow:auto}
.campo .nom{font:600 17px/1.3 inherit;color:var(--teal);background:var(--pale);
  border-radius:8px;padding:11px 14px;margin:0 0 11px}
.prog{display:flex;align-items:center;gap:12px;background:var(--surface);border:1px solid var(--line);
  border-radius:12px;padding:13px 17px;margin:0 0 14px;position:sticky;top:8px;z-index:5}
.prog b{font-size:21px;color:var(--teal);font-variant-numeric:tabular-nums}
.bar{flex:1;height:7px;background:var(--pale);border-radius:9px;overflow:hidden}
.bar i{display:block;height:100%;background:var(--wa);width:0;transition:width .25s}
ul.lista{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:8px}
li.p{background:var(--surface);border:1px solid var(--line);border-radius:11px;
  padding:12px 14px;display:flex;align-items:center;gap:13px;flex-wrap:wrap}
li.p.ok{opacity:.45}
.chk input{position:absolute;opacity:0;width:0;height:0}
.chk span{display:block;width:23px;height:23px;border:2px solid var(--line);border-radius:6px;cursor:pointer}
.chk input:checked+span{background:var(--wa);border-color:var(--wa)}
.chk input:checked+span::after{content:"";display:block;width:6px;height:11px;margin:2px auto;
  border:solid #fff;border-width:0 2.5px 2.5px 0;transform:rotate(45deg)}
.who{flex:1;min-width:190px;display:flex;flex-direction:column}
.who b{font-size:15px;color:var(--teal);line-height:1.3}
.meta{font-size:12px;color:var(--muted)}
.num{display:flex;flex-direction:column;align-items:flex-end}
.num code{font:600 14.5px/1.4 ui-monospace,SFMono-Regular,Menlo,monospace;
  font-variant-numeric:tabular-nums;color:var(--ink)}
.pais{font-size:11px;color:var(--muted)}
.btn{font:600 13px/1 inherit;font-family:inherit;border-radius:8px;padding:9px 13px;cursor:pointer;
  border:1px solid var(--line);background:transparent;color:var(--teal)}
.btn.full{background:var(--teal);color:var(--bg);border-color:var(--teal)}
.aviso{background:var(--pale);border-left:4px solid var(--gold);border-radius:0 9px 9px 0;
  padding:13px 16px;margin:0 0 12px;font-size:14px}
.aviso b{color:var(--gold)}
.aviso ul{margin:7px 0 0;padding-left:19px}
footer{margin-top:40px;padding-top:16px;border-top:1px solid var(--line);font-size:12.5px;color:var(--muted)}
@media(max-width:520px){.num{align-items:flex-start;width:100%}.btn{width:100%}}
</style></head><body><div class="wrap">

<h1>Armar el grupo de ponentes</h1>
<p class="sub">SEDA · Curso de obesidad, diabetes, nutrición clínica y salud digital · __N__ integrantes</p>

<h2>Cómo se crea</h2>
<div class="paso"><ol>
<li>WhatsApp → <b>Nuevo grupo</b></li>
<li>Añadir a las __N__ personas de la lista, marcando cada una aquí según las agregue</li>
<li>Poner el nombre y la descripción de abajo</li>
<li><b>Ajustes del grupo → Enviar mensajes → Solo administradores</b>, mientras lo arma</li>
<li>Enviar el mensaje de bienvenida y <b>fijarlo</b></li>
<li>Abrir los mensajes para todos</li>
</ol></div>

<h2>Nombre y descripción</h2>
<div class="campo"><h3>Nombre del grupo</h3>
<div class="nom" id="nom">SEDA · Curso obesidad y diabetes 2026</div>
<button class="btn copy" type="button" data-t="nom">Copiar nombre</button></div>
<div class="campo"><h3>Descripción</h3>
<pre id="desc">__DESC__</pre>
<button class="btn copy" type="button" data-t="desc">Copiar descripción</button></div>

<h2>A quién añadir</h2>
<div class="prog"><b><span id="hechos">0</span>/__N__</b><div class="bar"><i id="barra"></i></div>
<button class="btn" type="button" id="reset">Reiniciar</button></div>
<ul class="lista">__FILAS__</ul>

<h2>Mensaje de bienvenida</h2>
<div class="campo"><h3>Enviar y fijar</h3>
<pre id="bien">__BIEN__</pre>
<button class="btn full copy" type="button" data-t="bien">Copiar mensaje</button></div>

<h2>Antes de crearlo</h2>
<div class="aviso"><b>Falta resolver:</b><ul>__PEND__</ul>
Sin número no puede entrar al grupo. Conviene decidir qué se hace antes de crearlo, para no dejar a nadie fuera sin explicación.</div>
<div class="aviso"><b>No tratar en el grupo:</b><ul>
<li>El precio de la inscripción y el tema de los honorarios. Hay una conversación abierta con la Dra. Ruilova que no está cerrada. En el grupo, ad honorem y nada más.</li>
<li>Las fechas de entrega de los demás. Cada quien ya tiene la suya por privado; verlas juntas invita a comparar y a pedir prórrogas.</li>
<li>Una fecha estimada del aval. Mientras la comisión no responda, «en trámite» y punto: en un grupo, una estimación se vuelve promesa.</li>
</ul></div>

<footer>
<p>Las casillas se guardan solo en este navegador y en este equipo. No se comparten ni quedan en la matriz.</p>
<p>Generado desde <b>SEDA_Matriz_Ponentes_Curso_Obesidad.xlsx</b>. Si cambia la matriz, se regenera y la lista se actualiza sola.</p>
</footer>
</div>
<script>
(function(){
 var K='seda-grupo',st={};try{st=JSON.parse(localStorage.getItem(K)||'{}')||{}}catch(e){st={}}
 var cajas=[].slice.call(document.querySelectorAll('input[type=checkbox]'));
 function pinta(){
   var n=0;
   cajas.forEach(function(b){
     b.checked=!!st[b.dataset.k];
     b.closest('li').classList.toggle('ok',b.checked);
     if(b.checked)n++;
   });
   document.getElementById('hechos').textContent=n;
   document.getElementById('barra').style.width=(cajas.length?n/cajas.length*100:0)+'%';
 }
 cajas.forEach(function(b){b.addEventListener('change',function(){
   st[b.dataset.k]=b.checked;try{localStorage.setItem(K,JSON.stringify(st))}catch(e){}pinta();});});
 document.getElementById('reset').addEventListener('click',function(){
   st={};try{localStorage.removeItem(K)}catch(e){}pinta();});
 document.querySelectorAll('.copy').forEach(function(btn){
   btn.addEventListener('click',function(){
     var el=document.getElementById(btn.dataset.t),txt=el.textContent;
     function ok(){var o=btn.textContent;btn.textContent='Copiado';setTimeout(function(){btn.textContent=o},1300)}
     function manual(){
       var ta=document.createElement('textarea');ta.value=txt;ta.style.position='fixed';ta.style.left='-9999px';
       document.body.appendChild(ta);ta.select();
       try{document.execCommand('copy');ok()}catch(e){alert('Seleccione el texto y cópielo a mano.')}
       document.body.removeChild(ta);
     }
     if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(txt).then(ok,manual)}else{manual()}
   });
 });
 pinta();
})();
</script></body></html>"""

doc = (doc.replace('__FILAS__', "".join(filas))
          .replace('__DESC__', e(DESC))
          .replace('__BIEN__', e(BIENVENIDA))
          .replace('__PEND__', pend or '<li>Nada pendiente.</li>')
          .replace('__N__', str(len(gente))))
io.open('SEDA_Grupo_WhatsApp.html','w',encoding='utf-8').write(doc)
print('integrantes:', len(gente), '| pendientes sin teléfono:', len(sin_tel), '| bytes:', len(doc))
