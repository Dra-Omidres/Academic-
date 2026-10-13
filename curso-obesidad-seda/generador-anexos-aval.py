# -*- coding: utf-8 -*-
"""Anexos del expediente del aval: un PDF con las hojas de vida, en el orden del cuerpo docente
del expediente, y otro con las declaraciones de conflicto de interés firmadas.

Las hojas de vida en Word se convierten con LibreOffice. Las que pesan más de 3 MB se
rasterizan a unos 115 ppp para que el anexo se pueda enviar por correo; los originales no se
tocan.

Salidas: expediente/entrega-ucuenca/SEDA_Anexo1_Hojas_de_Vida.pdf y SEDA_Anexo2_Declaraciones_COI.pdf
"""
import os, re, glob, subprocess, tempfile, unicodedata, docx, pypdf, pypdfium2

HV='expediente/hojas-de-vida'; OUT='expediente/entrega-ucuenca'
tmp=tempfile.mkdtemp(); os.makedirs(OUT, exist_ok=True)
src={}
for f in sorted(glob.glob(HV+'/*.pdf')): src[os.path.basename(f)[:-4]]=f
for f in sorted(glob.glob(HV+'/*.docx')):
    k=os.path.basename(f)[:-5]
    if k not in src:
        subprocess.run(['soffice','--headless','--convert-to','pdf','--outdir',tmp,f], capture_output=True)
        src[k]=os.path.join(tmp,k+'.pdf')
for k,f in list(src.items()):
    if os.path.getsize(f)>3e6:
        d=pypdfium2.PdfDocument(f); ims=[d[i].render(scale=1.6).to_pil().convert('RGB') for i in range(len(d))]
        out=os.path.join(tmp,k+'_liviano.pdf'); ims[0].save(out, save_all=True, append_images=ims[1:], resolution=115, quality=70)
        src[k]=out

def norm(s): return unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower()
d=docx.Document('SEDA_Solicitud_Aval_UCuenca.docx')
tb=[t for t in d.tables if t.rows[0].cells[0].text=='Docente'][0]
w=pypdf.PdfWriter(); n=0; faltan=[]
for r in tb.rows[1:]:
    nombre=r.cells[0].text
    toks=[t for t in re.findall(r'[a-z]+',norm(nombre)) if len(t)>2 and t not in ('dra','lcda','ing','consolacion','del')]
    best=max(src, key=lambda k: sum(1 for t in toks if t in norm(k)))
    if sum(1 for t in toks if t in norm(best))>=2: w.append(src[best], outline_item=nombre); n+=1
    else: faltan.append(nombre)
w.compress_identical_objects(); a1=OUT+'/SEDA_Anexo1_Hojas_de_Vida.pdf'; w.write(a1)
w=pypdf.PdfWriter()
for f in sorted(glob.glob('expediente/declaraciones-coi/*_firmada.pdf')): w.append(f)
a2=OUT+'/SEDA_Anexo2_Declaraciones_COI.pdf'; w.write(a2)
print('Anexo 1: %d hojas de vida, %.1f MB · faltan: %s' % (n, os.path.getsize(a1)/1e6, faltan))
print('Anexo 2: %.1f MB' % (os.path.getsize(a2)/1e6))
