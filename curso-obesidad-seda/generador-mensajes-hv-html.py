# -*- coding: utf-8 -*-
"""Página HTML con los seis mensajes que piden solo la hoja de vida.

Lee los textos de whatsapp-seis-hojas-de-vida.md (la fuente: si un mensaje cambia, se cambia
allí y se vuelve a correr esto) y arma una tarjeta por docente con dos botones: abrir el
chat de WhatsApp con el mensaje ya escrito, o copiarlo. Nada se envía solo: WhatsApp abre el
chat y la Dra. Omidres pulsa «Enviar».

Salida: SEDA_Mensajes_Hojas_de_Vida.html
"""
import html, re, urllib.parse

FUENTE = 'whatsapp-seis-hojas-de-vida.md'
SALIDA = 'SEDA_Mensajes_Hojas_de_Vida.html'

# nombre visible, clase, teléfono, aviso que bloquea el envío (o None)
DOCENTES = [
    ('Dr. Frank Espinoza', 'M3 · C2 · Agonistas del receptor de GLP-1', '+51 936 260 715', None),
    ('Dra. María Paz Castillo Cabrera', 'M4 · C1 · Fisiopatología y clasificación de la diabetes',
     '+52 1 56 2489 0698',
     'No enviar hasta aclarar si es la misma persona que interviene en el trámite del aval de la '
     'Universidad de Cuenca. Si lo es, dictar una clase de un curso que evalúa puede ser un conflicto '
     'de interés para el aval.'),
    ('Dra. Gabriela Jiménez', 'M4 · C3 · Terapia farmacológica moderna', '+593 99 807 8964', None),
    ('Dra. Gabriela Machado', 'M5 · C3 · Nutrición durante las terapias para obesidad', '+593 99 502 5774',
     'Confirmar antes que sigue en el curso: estaba pendiente de confirmar.'),
    ('Dra. Valeria Andrade', 'M6 · C1 · Enfermedad renal asociada a obesidad y diabetes', '+593 98 335 5686', None),
    ('Dra. Ana María Gómez', 'M7 · C2 · Monitoreo digital y tecnologías en diabetes y obesidad',
     '+57 310 488 4626', None),
]

textos = re.findall(r'^```\n(.*?)\n```', open(FUENTE, encoding='utf-8').read(), flags=re.S | re.M)
if len(textos) != len(DOCENTES):
    raise SystemExit('Se esperaban %d mensajes en %s y hay %d' % (len(DOCENTES), FUENTE, len(textos)))

e = lambda s: html.escape(s, quote=True)
tarjetas = []
for i, ((nombre, clase, tel, aviso), msg) in enumerate(zip(DOCENTES, textos)):
    digitos = ''.join(ch for ch in tel if ch.isdigit())
    enlace = 'https://wa.me/%s?text=%s' % (digitos, urllib.parse.quote(msg, safe=''))
    aviso_h = ('<p class="aviso"><strong>⚠️ Antes de enviar:</strong> %s</p>' % e(aviso)) if aviso else ''
    tarjetas.append(f'''
<article class="card{' bloq' if aviso else ''}" id="m{i}">
  <header><span class="num">{i+1}</span><div><h2>{e(nombre)}</h2><p class="clase">{e(clase)}</p></div></header>
  <p class="tel">WhatsApp: <strong>{e(tel)}</strong></p>
  {aviso_h}
  <pre class="msg" id="t{i}">{e(msg)}</pre>
  <div class="acciones">
    <a class="btn primary" href="{e(enlace)}" target="_blank" rel="noopener">Abrir en WhatsApp</a>
    <button class="btn ghost" type="button" data-t="t{i}">Copiar texto</button>
    <label class="hecho"><input type="checkbox" data-k="hv-{i}"> Enviado</label>
  </div>
</article>''')

doc = f'''<!DOCTYPE html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Hojas de vida pendientes · Curso SEDA</title>
<style>
:root{{--teal:#0D5A62;--gold:#B8852B;--mint:#C8E1DF;--pale:#EDF5F4;--warm:#FBF1DC;--ink:#1A2325;--muted:#5F7073}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--pale);color:var(--ink);font:16px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif}}
.wrap{{max-width:760px;margin:0 auto;padding:24px 16px 48px}}
.top{{display:flex;align-items:center;gap:14px;margin-bottom:6px}}
.top img{{height:46px}}
h1{{color:var(--teal);font-size:24px;margin:6px 0 2px}}
.sub{{color:var(--muted);margin:0 0 18px}}
.intro{{background:var(--warm);border-left:4px solid var(--gold);border-radius:10px;padding:12px 16px;margin-bottom:18px;font-size:15px}}
.card{{background:#fff;border-radius:14px;padding:16px 18px;margin-bottom:16px;border-left:5px solid var(--teal);box-shadow:0 1px 2px rgba(0,0,0,.05)}}
.card.bloq{{border-left-color:var(--gold)}}
.card header{{display:flex;gap:12px;align-items:flex-start}}
.num{{flex:none;width:30px;height:30px;border-radius:50%;background:var(--teal);color:#fff;display:grid;place-items:center;font-weight:700}}
.card.bloq .num{{background:var(--gold)}}
h2{{margin:0;font-size:18px;color:var(--teal)}}
.clase,.tel{{margin:2px 0 0;color:var(--muted);font-size:14px}}
.tel{{margin:10px 0}}
.aviso{{background:var(--warm);border-radius:8px;padding:10px 12px;font-size:14px;margin:8px 0}}
.msg{{white-space:pre-wrap;font:14.5px/1.5 inherit;font-family:inherit;background:var(--pale);border-radius:10px;padding:12px 14px;margin:8px 0 12px;max-height:260px;overflow:auto}}
.acciones{{display:flex;flex-wrap:wrap;gap:10px;align-items:center}}
.btn{{border:0;border-radius:999px;padding:10px 18px;font:600 15px/1 inherit;font-family:inherit;cursor:pointer;text-decoration:none;display:inline-block}}
.primary{{background:var(--teal);color:#fff}}
.ghost{{background:#fff;color:var(--teal);border:1.5px solid var(--teal)}}
.hecho{{margin-left:auto;color:var(--muted);font-size:14px;display:flex;gap:6px;align-items:center}}
.card.enviado{{opacity:.55}}
footer{{color:var(--muted);font-size:13px;text-align:center;margin-top:26px}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--pale:#14201f;--ink:#e7efee;--muted:#9fb3b5;--warm:#3a3220}}
 :root:not([data-theme="light"]) .card{{background:#1b2a2a}} :root:not([data-theme="light"]) .ghost{{background:transparent;color:var(--mint);border-color:var(--mint)}}
 :root:not([data-theme="light"]) h1,:root:not([data-theme="light"]) h2{{color:var(--mint)}}}}
</style></head>
<body><div class="wrap">
<div class="top"><img src="activos/logo/logo-curso-seda.png" alt="Curso SEDA" onerror="this.remove()"></div>
<h1>Hojas de vida pendientes</h1>
<p class="sub">Seis mensajes individuales · solo se pide la hoja de vida · 12 de octubre de 2026</p>
<div class="intro"><strong>Cómo usarlo:</strong> «Abrir en WhatsApp» abre el chat de cada docente con el mensaje ya escrito; usted lo revisa y pulsa enviar. Nada se envía solo. Marque «Enviado» para llevar la cuenta en este equipo.</div>
{''.join(tarjetas)}
<footer>Curso virtual SEDA · Coordinación académica · uso interno, contiene teléfonos de los docentes</footer>
</div>
<script>
document.querySelectorAll('button[data-t]').forEach(b=>b.addEventListener('click',async()=>{{
  const t=document.getElementById(b.dataset.t).innerText;
  try{{await navigator.clipboard.writeText(t)}}catch(e){{const a=document.createElement('textarea');a.value=t;document.body.appendChild(a);a.select();document.execCommand('copy');a.remove()}}
  const o=b.textContent;b.textContent='¡Copiado!';setTimeout(()=>b.textContent=o,1500);
}}));
document.querySelectorAll('input[data-k]').forEach(c=>{{
  const card=c.closest('.card');
  try{{c.checked=localStorage.getItem(c.dataset.k)==='1'}}catch(e){{}}
  card.classList.toggle('enviado',c.checked);
  c.addEventListener('change',()=>{{card.classList.toggle('enviado',c.checked);try{{localStorage.setItem(c.dataset.k,c.checked?'1':'0')}}catch(e){{}}}});
}});
</script>
</body></html>'''
open(SALIDA, 'w', encoding='utf-8').write(doc)
print(SALIDA, 'generado ·', len(tarjetas), 'mensajes')
