const pptxgen = require("pptxgenjs");
const p = new pptxgen();
p.layout = "LAYOUT_16x9";              // 10" x 5.625"
p.author = "Sociedad de Endocrinologia y Diabetes del Austro (SEDA)";
p.company = "SEDA";
p.title = "Plantilla institucional para ponentes";

const TEAL="0D5A62", TEAL2="094247", GOLD="B8852B", MINT="C8E1DF",
      PALE="EDF5F4", INK="212121", GREY="6B6B6B", W="FFFFFF", CREAM="FBF6EC";
const F="Arial";
const W10=10, H=5.625;

// ---------- helpers ----------
function fondoClaro(s){ s.background={color:W}; }
function fondoOscuro(s){ s.background={color:TEAL2}; }

function titulo(s,txt,sub){
  s.addText(txt,{x:0.6,y:0.42,w:8.8,h:0.62,fontFace:F,fontSize:30,bold:true,
    color:TEAL,isTextBox:true,margin:0});
  if(sub) s.addText(sub,{x:0.6,y:1.04,w:8.8,h:0.34,fontFace:F,fontSize:12,
    color:GREY,italic:true,isTextBox:true,margin:0});
}
function pie(s,n){
  s.addText("Curso virtual de actualización en obesidad, diabetes, nutrición clínica y salud digital  ·  SEDA",
    {x:0.6,y:5.15,w:7.6,h:0.26,fontFace:F,fontSize:8,color:GREY,isTextBox:true,margin:0});
  s.addText(String(n),{x:9.0,y:5.15,w:0.45,h:0.26,fontFace:F,fontSize:9,
    color:GOLD,bold:true,align:"right",isTextBox:true,margin:0});
}
function cajaNum(s,n,x,y,w,h,tit,cuerpo){
  s.addShape(p.ShapeType.roundRect,{x,y,w,h,fill:{color:PALE},
    rectRadius:0.08,line:{color:MINT,width:1}});
  s.addShape(p.ShapeType.ellipse,{x:x+0.22,y:y+0.22,w:0.42,h:0.42,fill:{color:GOLD}});
  s.addText(String(n),{x:x+0.22,y:y+0.22,w:0.42,h:0.42,fontFace:F,fontSize:15,bold:true,
    color:W,align:"center",valign:"middle",isTextBox:true,margin:0});
  s.addText(tit,{x:x+0.78,y:y+0.24,w:w-1.0,h:0.34,fontFace:F,fontSize:14,bold:true,
    color:TEAL2,isTextBox:true,margin:0});
  s.addText(cuerpo,{x:x+0.78,y:y+0.62,w:w-1.0,h:h-0.82,fontFace:F,fontSize:11,
    color:INK,isTextBox:true,margin:0});
}

// =========== 1. INSTRUCCIONES (se elimina antes de grabar) ===========
let s = p.addSlide(); s.background={color:CREAM};
s.addShape(p.ShapeType.roundRect,{x:0.6,y:0.4,w:8.8,h:0.62,fill:{color:"9C0006"},rectRadius:0.08});
s.addText("ELIMINE ESTA DIAPOSITIVA ANTES DE GRABAR",
  {x:0.6,y:0.4,w:8.8,h:0.62,fontFace:F,fontSize:17,bold:true,color:W,
   align:"center",valign:"middle",isTextBox:true,margin:0});
s.addText("Cómo usar esta plantilla",{x:0.6,y:1.22,w:8.8,h:0.44,fontFace:F,fontSize:23,
  bold:true,color:TEAL,isTextBox:true,margin:0});
cajaNum(s,1,0.6,1.82,4.25,1.42,"Duración: 30 minutos",
  "Cada clase dura 30 minutos grabados. Como referencia, entre 18 y 22 diapositivas de contenido.");
cajaNum(s,2,5.15,1.82,4.25,1.42,"Diapositivas obligatorias",
  "Portada, datos del ponente y declaración de conflicto de interés. Las tres van siempre.");
cajaNum(s,3,0.6,3.38,4.25,1.42,"Bibliografía en Vancouver",
  "Solo fuentes reales e indexadas, con volumen, páginas y DOI. Se revisan una a una.");
cajaNum(s,4,5.15,3.38,4.25,1.42,"Entrega",
  "Respete la fecha que se le indicó. Las clases se publican por módulos, una semana después.");
s.addNotes("Diapositiva de instrucciones internas. El ponente debe eliminarla antes de grabar.");

// =========== 2. PORTADA ===========
s = p.addSlide(); fondoOscuro(s);
s.addShape(p.ShapeType.ellipse,{x:8.05,y:-1.25,w:3.6,h:3.6,fill:{color:TEAL},transparency:55});
s.addShape(p.ShapeType.ellipse,{x:-1.1,y:3.5,w:2.9,h:2.9,fill:{color:TEAL},transparency:65});
s.addText("SOCIEDAD DE ENDOCRINOLOGÍA Y DIABETES DEL AUSTRO",
  {x:0.75,y:0.62,w:8.5,h:0.3,fontFace:F,fontSize:10,bold:true,color:MINT,
   charSpacing:1.6,isTextBox:true,margin:0});
s.addText("Título de la charla",
  {x:0.75,y:1.55,w:8.2,h:1.3,fontFace:F,fontSize:38,bold:true,color:W,isTextBox:true,margin:0});
s.addShape(p.ShapeType.roundRect,{x:0.75,y:3.05,w:2.05,h:0.4,fill:{color:GOLD},rectRadius:0.06});
s.addText("MÓDULO 0 · CLASE 0",{x:0.75,y:3.05,w:2.05,h:0.4,fontFace:F,fontSize:10,bold:true,
  color:W,align:"center",valign:"middle",isTextBox:true,margin:0});
s.addText("Nombre completo del ponente, con títulos",
  {x:0.75,y:3.72,w:8.2,h:0.36,fontFace:F,fontSize:17,bold:true,color:W,isTextBox:true,margin:0});
s.addText("Especialidad · Institución · Ciudad, País",
  {x:0.75,y:4.12,w:8.2,h:0.32,fontFace:F,fontSize:12,color:MINT,isTextBox:true,margin:0});
s.addText("Programa de educación continua  ·  Noviembre – diciembre 2026",
  {x:0.75,y:4.82,w:8.5,h:0.3,fontFace:F,fontSize:10,color:MINT,isTextBox:true,margin:0});
s.addNotes("Sustituya el título, el módulo, la clase y sus datos. No añada logotipos institucionales hasta que el aval esté resuelto.");

// =========== 3. DATOS DEL PONENTE ===========
s = p.addSlide(); fondoClaro(s);
titulo(s,"Datos del ponente","Diapositiva obligatoria");
s.addShape(p.ShapeType.roundRect,{x:0.6,y:1.6,w:2.65,h:2.9,fill:{color:PALE},
  rectRadius:0.1,line:{color:MINT,width:1}});
s.addText("Fotografía\nprofesional",{x:0.6,y:1.6,w:2.65,h:2.9,fontFace:F,fontSize:12,
  color:GREY,align:"center",valign:"middle",italic:true,isTextBox:true,margin:0});
const datos=[["Nombre completo","con títulos académicos"],
             ["Especialidad","y subespecialidad"],
             ["Institución","hospital, universidad o consulta"],
             ["Ciudad y país",""],
             ["Afiliaciones","sociedades científicas"]];
let yy=1.66;
datos.forEach(([k,v])=>{
  s.addText(k,{x:3.55,y:yy,w:5.85,h:0.26,fontFace:F,fontSize:13,bold:true,color:TEAL2,
    isTextBox:true,margin:0});
  s.addText(v||"—",{x:3.55,y:yy+0.26,w:5.85,h:0.24,fontFace:F,fontSize:11,color:GREY,
    italic:true,isTextBox:true,margin:0});
  yy+=0.58;
});
pie(s,1);
s.addNotes("Complete sus datos tal como deben aparecer en el certificado y en el expediente del aval.");

// =========== 4. CONFLICTO DE INTERÉS ===========
s = p.addSlide(); fondoClaro(s);
titulo(s,"Declaración de conflicto de interés","Diapositiva obligatoria · no puede omitirse");
s.addShape(p.ShapeType.roundRect,{x:0.6,y:1.62,w:8.8,h:1.18,fill:{color:PALE},
  rectRadius:0.1,line:{color:MINT,width:1}});
s.addText("Marque la opción que corresponda",{x:0.95,y:1.78,w:8.1,h:0.28,fontFace:F,
  fontSize:12,bold:true,color:TEAL2,isTextBox:true,margin:0});
s.addText([
 {text:"Declaro no tener conflictos de interés relacionados con el contenido de esta charla.",
  options:{bullet:true,breakLine:true}},
 {text:"Declaro los siguientes vínculos: ____________________________________________",
  options:{bullet:true}}],
 {x:0.95,y:2.08,w:8.1,h:0.64,fontFace:F,fontSize:11,color:INK,
  paraSpaceAfter:5,isTextBox:true,margin:0});
cajaNum(s,1,0.6,2.92,4.25,1.52,"Qué se declara",
  "Honorarios, consultorías, apoyo a investigación, participación en ensayos clínicos y patrocinio de viajes o eventos.");
cajaNum(s,2,5.15,2.92,4.25,1.52,"Por qué importa",
  "El programa aborda agonistas de GLP-1, tirzepatida e iSGLT2. La transparencia protege al docente y a SEDA.");
s.addText("Esta diapositiva debe mostrarse en pantalla y mencionarse en voz alta al inicio de la grabación.",
  {x:0.6,y:4.58,w:8.8,h:0.3,fontFace:F,fontSize:10,bold:true,color:"9C0006",
   isTextBox:true,margin:0});
pie(s,2);
s.addNotes("Obligatoria. Debe verse en pantalla y enunciarse en voz alta.");

// =========== 5. OBJETIVOS ===========
s = p.addSlide(); fondoClaro(s);
titulo(s,"Objetivos de aprendizaje","Qué sabrá hacer el participante al terminar su clase");
["Primer objetivo: comience con un verbo de acción — identificar, aplicar, interpretar, seleccionar.",
 "Segundo objetivo: concreto y evaluable, no genérico.",
 "Tercer objetivo: vinculado al caso clínico que presentará más adelante."]
 .forEach((t,i)=>{
  const y=1.68+i*1.02;
  s.addShape(p.ShapeType.roundRect,{x:0.6,y:y,w:8.8,h:0.86,fill:{color:PALE},
    rectRadius:0.08,line:{color:MINT,width:1}});
  s.addShape(p.ShapeType.ellipse,{x:0.86,y:y+0.21,w:0.44,h:0.44,fill:{color:TEAL}});
  s.addText(String(i+1),{x:0.86,y:y+0.21,w:0.44,h:0.44,fontFace:F,fontSize:16,bold:true,
    color:W,align:"center",valign:"middle",isTextBox:true,margin:0});
  s.addText(t,{x:1.48,y:y+0.2,w:7.7,h:0.48,fontFace:F,fontSize:13,color:INK,
    valign:"middle",isTextBox:true,margin:0});
 });
pie(s,3);
s.addNotes("Tres objetivos bastan para 30 minutos.");

// =========== 6. CONTENIDO — dos columnas ===========
s = p.addSlide(); fondoClaro(s);
titulo(s,"Título del apartado","Modelo de diapositiva de contenido · dos columnas");
s.addText([
 {text:"Idea principal del apartado",options:{bullet:true,breakLine:true}},
 {text:"Evidencia que la respalda, con la cita entre paréntesis",options:{bullet:true,breakLine:true}},
 {text:"Matiz o excepción relevante en la práctica",options:{bullet:true,breakLine:true}},
 {text:"Aplicación concreta al paciente",options:{bullet:true}}],
 {x:0.6,y:1.68,w:4.35,h:2.6,fontFace:F,fontSize:13,color:INK,
  paraSpaceAfter:9,isTextBox:true,margin:0});
s.addShape(p.ShapeType.roundRect,{x:5.25,y:1.68,w:4.15,h:2.6,fill:{color:PALE},
  rectRadius:0.1,line:{color:MINT,width:1}});
s.addText("Figura, tabla, gráfico\no algoritmo",{x:5.25,y:1.68,w:4.15,h:2.6,fontFace:F,
  fontSize:13,color:GREY,align:"center",valign:"middle",italic:true,isTextBox:true,margin:0});
s.addText("Fuente: Autor A, et al. Título. Revista. Año;vol(núm):págs. doi:…",
  {x:5.25,y:4.34,w:4.15,h:0.26,fontFace:F,fontSize:8,color:GREY,isTextBox:true,margin:0});
pie(s,4);
s.addNotes("Toda figura tomada de otra publicación debe llevar su fuente al pie.");

// =========== 7. CONTENIDO — tarjetas ===========
s = p.addSlide(); fondoClaro(s);
titulo(s,"Título del apartado","Modelo alterno · conceptos en bloques");
const cards=[["Concepto","Definición breve en una o dos líneas."],
             ["Evidencia","Estudio o guía que lo sustenta."],
             ["Práctica","Cómo se traduce a la consulta."]];
cards.forEach(([t,c],i)=>{
  const x=0.6+i*3.0;
  s.addShape(p.ShapeType.roundRect,{x:x,y:1.72,w:2.8,h:2.15,fill:{color:PALE},
    rectRadius:0.1,line:{color:MINT,width:1}});
  s.addShape(p.ShapeType.ellipse,{x:x+1.18,y:1.95,w:0.46,h:0.46,fill:{color:GOLD}});
  s.addText(String(i+1),{x:x+1.18,y:1.95,w:0.46,h:0.46,fontFace:F,fontSize:16,bold:true,
    color:W,align:"center",valign:"middle",isTextBox:true,margin:0});
  s.addText(t,{x:x+0.2,y:2.55,w:2.4,h:0.3,fontFace:F,fontSize:15,bold:true,color:TEAL2,
    align:"center",isTextBox:true,margin:0});
  s.addText(c,{x:x+0.2,y:2.9,w:2.4,h:0.85,fontFace:F,fontSize:11,color:INK,
    align:"center",isTextBox:true,margin:0});
});
s.addText("Dato o cifra destacada del apartado",{x:0.6,y:4.12,w:8.8,h:0.42,fontFace:F,
  fontSize:17,bold:true,italic:true,color:GOLD,isTextBox:true,margin:0});
pie(s,5);

// =========== 8. CASO CLÍNICO ===========
s = p.addSlide(); fondoClaro(s);
titulo(s,"Caso clínico","Un caso por clase, articulado con los objetivos");
const caso=[["Presentación","Edad, sexo, motivo de consulta y antecedentes relevantes."],
            ["Hallazgos","Examen físico, laboratorio e imagen."],
            ["Decisión","Qué se hizo y por qué, con la evidencia que lo sustenta."],
            ["Desenlace","Evolución y aprendizaje que deja el caso."]];
caso.forEach(([t,c],i)=>{
  const col=i%2, row=Math.floor(i/2);
  const x=0.6+col*4.55, y=1.7+row*1.42;
  s.addShape(p.ShapeType.roundRect,{x:x,y:y,w:4.25,h:1.22,fill:{color:PALE},
    rectRadius:0.08,line:{color:MINT,width:1}});
  s.addText(t,{x:x+0.26,y:y+0.16,w:3.75,h:0.3,fontFace:F,fontSize:14,bold:true,
    color:TEAL2,isTextBox:true,margin:0});
  s.addText(c,{x:x+0.26,y:y+0.5,w:3.75,h:0.58,fontFace:F,fontSize:11,color:INK,
    isTextBox:true,margin:0});
});
s.addText("No incluya datos que permitan identificar al paciente.",
  {x:0.6,y:4.62,w:8.8,h:0.28,fontFace:F,fontSize:10,bold:true,color:"9C0006",
   isTextBox:true,margin:0});
pie(s,6);
s.addNotes("Anonimice el caso: sin nombres, iniciales, fechas exactas ni números de historia clínica.");

// =========== 9. MENSAJES CLAVE ===========
s = p.addSlide(); fondoClaro(s);
titulo(s,"Mensajes para llevar a casa","Tres ideas que el participante debe recordar");
["Primer mensaje clave, redactado como una afirmación clínica accionable.",
 "Segundo mensaje clave.",
 "Tercer mensaje clave."].forEach((t,i)=>{
  const y=1.7+i*1.04;
  s.addShape(p.ShapeType.roundRect,{x:0.6,y:y,w:8.8,h:0.88,fill:{color:TEAL},rectRadius:0.08});
  s.addShape(p.ShapeType.ellipse,{x:0.88,y:y+0.22,w:0.44,h:0.44,fill:{color:GOLD}});
  s.addText(String(i+1),{x:0.88,y:y+0.22,w:0.44,h:0.44,fontFace:F,fontSize:16,bold:true,
    color:W,align:"center",valign:"middle",isTextBox:true,margin:0});
  s.addText(t,{x:1.5,y:y+0.2,w:7.65,h:0.48,fontFace:F,fontSize:13,bold:true,color:W,
    valign:"middle",isTextBox:true,margin:0});
});
pie(s,7);

// =========== 10. BIBLIOGRAFÍA ===========
s = p.addSlide(); fondoClaro(s);
titulo(s,"Bibliografía","Formato Vancouver · solo fuentes reales e indexadas");
s.addText([
 {text:"Apellido AA, Apellido BB, Apellido CC. Título del artículo. Abreviatura de la revista. Año;volumen(número):páginas. doi:10.xxxx/xxxxx",options:{bullet:true,breakLine:true}},
 {text:"Institución u organismo. Título del documento. Ciudad: Editorial; año.",options:{bullet:true,breakLine:true}},
 {text:"Apellido AA, et al. Título. Revista. Año;vol(núm):págs. doi:…",options:{bullet:true,breakLine:true}},
 {text:"Apellido AA, et al. Título. Revista. Año;vol(núm):págs. doi:…",options:{bullet:true}}],
 {x:0.6,y:1.68,w:8.8,h:2.0,fontFace:F,fontSize:11,color:INK,
  paraSpaceAfter:9,isTextBox:true,margin:0});
s.addShape(p.ShapeType.roundRect,{x:0.6,y:3.82,w:8.8,h:0.92,fill:{color:PALE},
  rectRadius:0.08,line:{color:MINT,width:1}});
s.addText("Cada referencia se verifica en PubMed antes de presentar el expediente. No incluya fuentes sin volumen, páginas ni DOI, ni citas de las que no tenga el artículo a la vista.",
  {x:0.92,y:3.98,w:8.2,h:0.62,fontFace:F,fontSize:11,color:TEAL2,isTextBox:true,margin:0});
pie(s,8);
s.addNotes("Las referencias se comprueban una a una. Prefiera la edición vigente de guías y consensos.");

// =========== 11. CIERRE ===========
s = p.addSlide(); fondoOscuro(s);
s.addShape(p.ShapeType.ellipse,{x:-1.3,y:-1.3,w:3.4,h:3.4,fill:{color:TEAL},transparency:60});
s.addShape(p.ShapeType.ellipse,{x:7.9,y:3.3,w:3.3,h:3.3,fill:{color:TEAL},transparency:60});
s.addText("Gracias",{x:0.75,y:1.85,w:8.5,h:0.95,fontFace:F,fontSize:44,bold:true,
  color:W,isTextBox:true,margin:0});
s.addText("Nombre del ponente  ·  correo de contacto",
  {x:0.75,y:2.92,w:8.5,h:0.34,fontFace:F,fontSize:14,color:MINT,isTextBox:true,margin:0});
s.addText("Sociedad de Endocrinología y Diabetes del Austro",
  {x:0.75,y:4.76,w:8.5,h:0.3,fontFace:F,fontSize:10,bold:true,color:MINT,
   charSpacing:1.2,isTextBox:true,margin:0});

p.writeFile({fileName:"SEDA_Plantilla_Ponentes.pptx"}).then(f=>console.log("Generado:",f));
