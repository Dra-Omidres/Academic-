# -*- coding: utf-8 -*-
"""Delimitación tema por tema de las 28 clases.
   'no' = (qué no debe tocar, quién lo cubre)"""
import json, io, html, urllib.parse, openpyxl

CL = {c['cod']: c for c in json.load(open('/tmp/clases.json'))}
FECHAS = {"M1":"jueves 29 de octubre","M2":"jueves 29 de octubre","M3":"jueves 5 de noviembre",
          "M4":"jueves 12 de noviembre","M5":"jueves 19 de noviembre","M6":"jueves 26 de noviembre",
          "M7":"jueves 3 de diciembre"}

D = {
"M1 · C1": (["La magnitud del problema: cifras mundiales, de la región y del Ecuador",
             "El impacto sanitario y económico de la obesidad",
             "El cambio de paradigma diagnóstico: de la obesidad como IMC a la obesidad como enfermedad crónica"],
            [("Los mecanismos biológicos de la obesidad","M1 · C2, Dr. Pablo Vanegas"),
             ("Cómo se clasifica y evalúa al paciente en consulta","M1 · C3, Dra. María Augusta Astudillo"),
             ("IMC, circunferencia abdominal y bioimpedancia en detalle","M1 · C4, Dra. Gabriela Jiménez")]),
"M1 · C2": (["Adiposopatía y lipotoxicidad",
             "Inflamación crónica de bajo grado",
             "Cronobiología y su papel en la ganancia de peso"],
            [("Epidemiología y cifras","M1 · C1, Dra. Lizbet Ruilova"),
             ("Fisiopatología de la diabetes tipo 2","M4 · C1, Dra. María Augusta Astudillo"),
             ("Mecanismos de acción de los fármacos","M3 · C1 a C3")]),
"M1 · C3": (["Clasificación clínica del paciente con obesidad",
             "Fenotipos metabólicos como herramienta de consulta",
             "Estratificación del riesgo y decisión terapéutica"],
            [("Antropometría, bioimpedancia y sarcopenia","M1 · C4, Dra. Gabriela Jiménez"),
             ("El uso de los fenotipos para individualizar el plan nutricional","M5 · C1, módulo 5"),
             ("Estratificación del riesgo cardiovascular","M6 · C2, Dr. Chih Hao Chen Ku")]),
"M1 · C4": (["Las limitaciones del IMC",
             "Circunferencia abdominal y otras medidas antropométricas",
             "Bioimpedancia: qué mide y cómo se lee",
             "Obesidad sarcopénica: concepto y diagnóstico"],
            [("La misma evaluación en el paciente con diabetes","M5 · C4, Dra. Lizbet Ruilova — coordínenlo entre ustedes"),
             ("Sarcopenia como complicación metabólica","M6 · C4, Dra. Adriana Alvarez"),
             ("Estrategias nutricionales para preservar masa muscular","M5 · C3, módulo 5")]),
"M2 · C1": (["Requerimientos de energía y cómo se estiman",
             "Distribución de macronutrientes y criterios para decidirla",
             "Calidad nutricional: densidad de nutrientes, ultraprocesados, fibra",
             "Los principios para individualizar un plan"],
            [("Patrones alimentarios concretos: mediterránea, DASH, baja en carbohidratos, ayuno","M2 · C2, Dra. Johanna Piedra Bravo — es la clase siguiente a la suya"),
             ("Conducta alimentaria, hambre emocional y adherencia","M2 · C3, Dra. Janneth Bermeo"),
             ("Antropometría y bioimpedancia","M1 · C4, Dra. Gabriela Jiménez"),
             ("Nutrición durante el tratamiento con GLP-1 o tirzepatida","M5 · C3, módulo 5")]),
"M2 · C2": (["Dieta mediterránea: evidencia y aplicación en obesidad",
             "Dieta DASH",
             "Dietas bajas en carbohidratos",
             "Ayuno intermitente: qué dice la evidencia"],
            [("Cálculo de requerimientos y macronutrientes","M2 · C1, Lcda. Isabel Reinoso — es la clase anterior a la suya"),
             ("Adherencia y conducta alimentaria","M2 · C3, Dra. Janneth Bermeo"),
             ("ATENCIÓN — los mismos patrones aplicados a diabetes","M5 · C2, módulo 5. Ese módulo repite mediterránea, restricción de carbohidratos y ayuno: enfoque usted la obesidad y deje la diabetes al módulo 5")]),
"M2 · C3": (["Hambre fisiológica y hambre emocional",
             "Conducta alimentaria y su abordaje en consulta",
             "Adherencia terapéutica y cómo sostenerla"],
            [("Cálculo de requerimientos y macronutrientes","M2 · C1, Lcda. Isabel Reinoso"),
             ("Patrones alimentarios concretos","M2 · C2, Dra. Johanna Piedra Bravo"),
             ("Educación digital del paciente y adherencia por medios digitales","M7 · C3, módulo 7")]),
"M2 · C4": (["Ejercicio aeróbico: prescripción en obesidad",
             "Entrenamiento de fuerza",
             "Cómo se prescribe ejercicio en la consulta, con dosis y progresión"],
            [("Sarcopenia y composición corporal","M1 · C4, Dra. Gabriela Jiménez"),
             ("Preservación de masa muscular durante el tratamiento farmacológico","M5 · C3, módulo 5"),
             ("Enfermedad osteomuscular asociada a la obesidad","M6 · C4, Dra. Adriana Alvarez")]),
"M3 · C1": (["Cuándo indicar farmacoterapia y a quién",
             "Orlistat",
             "Fentermina y fentermina/topiramato",
             "Bupropión/naltrexona"],
            [("Semaglutida y los agonistas de GLP-1","M3 · C2, Dr. Frank Espinoza"),
             ("Tirzepatida y las terapias nuevas","M3 · C3, Dra. Teresa Cuatecontzi"),
             ("Cirugía bariátrica","M3 · C4, Dr. Cristian Castillo"),
             ("Los mismos fármacos aplicados a la diabetes","M4 · C3, Dra. Gabriela Jiménez")]),
"M3 · C2": (["Semaglutida: mecanismo, dosificación y manejo práctico",
             "La evidencia clínica de los agonistas de GLP-1 en obesidad",
             "Efectos adversos y cómo manejarlos"],
            [("Tirzepatida","M3 · C3, Dra. Teresa Cuatecontzi"),
             ("ATENCIÓN — los agonistas de GLP-1 en diabetes","M4 · C3, Dra. Gabriela Jiménez. Céntrese en obesidad y deje el uso en diabetes a ese módulo"),
             ("Los beneficios cardiovasculares y renales de estos fármacos","M6 · C3, Dr. Chih Hao Chen Ku"),
             ("El manejo nutricional durante el tratamiento","M5 · C3, módulo 5")]),
"M3 · C3": (["Tirzepatida: mecanismo dual GIP/GLP-1",
             "Evidencia clínica en obesidad",
             "Perfil de seguridad y manejo de efectos adversos",
             "Terapias en desarrollo"],
            [("Semaglutida y los agonistas de GLP-1","M3 · C2, Dr. Frank Espinoza — es la clase anterior a la suya"),
             ("Tirzepatida en el tratamiento de la diabetes","M4 · C3, Dra. Gabriela Jiménez"),
             ("Nutrición y masa muscular durante el tratamiento","M5 · C3, módulo 5")]),
"M3 · C4": (["Indicaciones y criterios de selección del paciente",
             "Las técnicas quirúrgicas y cómo se elige entre ellas",
             "Seguimiento metabólico y nutricional del posoperatorio",
             "Complicaciones y reganancia de peso"],
            [("Farmacoterapia previa a la cirugía","M3 · C1 a C3"),
             ("Composición corporal y sarcopenia","M1 · C4, Dra. Gabriela Jiménez"),
             ("El plan nutricional general","módulo 2")]),
"M4 · C1": (["Los defectos fisiopatológicos de la diabetes tipo 2",
             "La clasificación actual de la diabetes",
             "Diagnóstico temprano y tamizaje"],
            [("Fisiopatología de la obesidad","M1 · C2, Dr. Pablo Vanegas"),
             ("Metas terapéuticas y monitoreo","M4 · C2, Dra. Josefa Palacio"),
             ("Tratamiento farmacológico","M4 · C3 y C4")]),
"M4 · C2": (["HbA1c: alcances y limitaciones",
             "Tiempo en rango y las métricas del monitoreo continuo",
             "Lectura e interpretación del AGP",
             "Cómo se fijan las metas y se individualizan"],
            [("ATENCIÓN — MCG y AGP en entornos digitales, apps y monitoreo remoto","M7 · C2, módulo 7. Usted da la interpretación clínica; ese módulo da la implementación digital"),
             ("Los fármacos para alcanzar las metas","M4 · C3, Dra. Gabriela Jiménez"),
             ("Insulinoterapia","M4 · C4, Dr. Juan Molina")]),
"M4 · C3": (["iSGLT2 e iDPP-4 en diabetes",
             "Agonistas de GLP-1 y tirzepatida aplicados a la diabetes",
             "Individualización del tratamiento y algoritmos de decisión"],
            [("ATENCIÓN — los mismos fármacos en obesidad","M3 · C2 (Dr. Frank Espinoza) y M3 · C3 (Dra. Teresa Cuatecontzi). Céntrese en el control glucémico y deje el tratamiento de la obesidad al módulo 3"),
             ("Los beneficios cardiovasculares y renales de estos fármacos","M6 · C3, Dr. Chih Hao Chen Ku"),
             ("Insulinoterapia","M4 · C4, Dr. Juan Molina"),
             ("Fármacos para obesidad sin indicación en diabetes","M3 · C1, Dr. Pablo Vanegas")]),
"M4 · C4": (["Inicio de insulina: cuándo y con qué esquema",
             "Intensificación y ajuste",
             "Combinación de insulina con agonistas de GLP-1",
             "Prevención y manejo de la hipoglucemia"],
            [("Los antidiabéticos orales y los inyectables no insulínicos","M4 · C3, Dra. Gabriela Jiménez"),
             ("Metas de control y tiempo en rango","M4 · C2, Dra. Josefa Palacio"),
             ("Tecnología de infusión y monitoreo digital","M7 · C2, módulo 7")]),
"M5 · C1": (["Fenotipos metabólicos aplicados a la decisión nutricional",
             "Cómo se individualiza un plan según el fenotipo",
             "Qué aporta y qué no aporta hoy la nutrición de precisión"],
            [("La clasificación clínica y la estratificación de riesgo","M1 · C3, Dra. María Augusta Astudillo"),
             ("Los principios generales de la terapia nutricional","M2 · C1, Lcda. Isabel Reinoso"),
             ("Los patrones alimentarios concretos","M5 · C2, su mismo módulo")]),
"M5 · C2": (["Dieta mediterránea en el paciente con diabetes",
             "Restricción de carbohidratos y control glucémico",
             "Ayuno intermitente: evidencia en diabetes"],
            [("ATENCIÓN — los mismos patrones en obesidad","M2 · C2, Dra. Johanna Piedra Bravo. Ese módulo cubre mediterránea, DASH, bajas en carbohidratos y ayuno aplicados a obesidad: enfoque usted la diabetes"),
             ("Individualización por fenotipos","M5 · C1, su mismo módulo"),
             ("Nutrición durante el tratamiento farmacológico","M5 · C3, su mismo módulo")]),
"M5 · C3": (["Manejo nutricional durante el tratamiento con agonistas de GLP-1",
             "Manejo nutricional con tirzepatida",
             "Preservación de la masa muscular durante la pérdida de peso",
             "Manejo nutricional de los efectos adversos gastrointestinales"],
            [("Farmacología, dosificación y evidencia de esos fármacos","M3 · C2 y M3 · C3"),
             ("Prescripción de ejercicio para preservar masa muscular","M2 · C4, Dra. Julia Castro"),
             ("Diagnóstico de la sarcopenia","M1 · C4 y M5 · C4")]),
"M5 · C4": (["Evaluación clínica de la composición corporal en el paciente con diabetes",
             "Interpretación de la bioimpedancia",
             "Estrategias nutricionales frente a la pérdida de masa magra"],
            [("ATENCIÓN — IMC, circunferencia, bioimpedancia y obesidad sarcopénica","M1 · C4, Dra. Gabriela Jiménez. Ella da los fundamentos del método: céntrese usted en el paciente con diabetes"),
             ("Sarcopenia como complicación metabólica","M6 · C4, Dra. Adriana Alvarez"),
             ("Nutrición durante el tratamiento farmacológico","M5 · C3, su mismo módulo")]),
"M6 · C1": (["Tamizaje de la enfermedad renal y diagnóstico temprano",
             "Estratificación del riesgo renal",
             "Estrategias terapéuticas de protección renal"],
            [("ATENCIÓN — los beneficios renales de las nuevas terapias","M6 · C3, Dr. Chih Hao Chen Ku. Él los cubre dentro del síndrome cardiorrenometabólico: céntrese usted en el tamizaje, el diagnóstico y la estratificación"),
             ("Riesgo cardiovascular y dislipidemias","M6 · C2, Dr. Chih Hao Chen Ku"),
             ("Los fármacos y su dosificación en diabetes","M4 · C3, Dra. Gabriela Jiménez")]),
"M6 · C2": (["Estratificación del riesgo cardiovascular",
             "Aterosclerosis en obesidad y diabetes",
             "Dislipidemias y su tratamiento",
             "Riesgo residual: colesterol no-HDL, ApoB, hipertrigliceridemia"],
            [("Enfermedad renal","M6 · C1, Dra. Valeria Andrade"),
             ("Insuficiencia cardíaca y síndrome cardiorrenometabólico","M6 · C3, su propia clase siguiente")]),
"M6 · C3": (["Concepto actual de síndrome cardiorrenometabólico",
             "Insuficiencia cardíaca en el paciente con obesidad y diabetes",
             "Beneficios cardiovasculares y renales de las nuevas terapias"],
            [("Estratificación del riesgo cardiovascular y dislipidemias","M6 · C2, su propia clase anterior"),
             ("Tamizaje y diagnóstico de la enfermedad renal","M6 · C1, Dra. Valeria Andrade"),
             ("Dosificación y evidencia de los fármacos en diabetes","M4 · C3, Dra. Gabriela Jiménez")]),
"M6 · C4": (["MASLD: diagnóstico, estratificación y manejo",
             "Obesidad sarcopénica como complicación",
             "Enfermedad osteomuscular asociada a la obesidad",
             "Abordaje integral de estas complicaciones"],
            [("ATENCIÓN — diagnóstico de sarcopenia y bioimpedancia","M1 · C4 (Dra. Gabriela Jiménez) y M5 · C4 (Dra. Lizbet Ruilova). Ellas dan el método diagnóstico: céntrese usted en la sarcopenia como complicación y su manejo"),
             ("Riesgo cardiovascular y renal","M6 · C1 y M6 · C2"),
             ("Prescripción de ejercicio","M2 · C4, Dra. Julia Castro")]),
"M7 · C1": (["Marco conceptual de la salud digital",
             "Marco normativo de la telesalud en el Ecuador",
             "Modelos sincrónico, asincrónico e híbrido"],
            [("Tecnologías de monitoreo","M7 · C2, su mismo módulo"),
             ("IA y terapias digitales","M7 · C3, su mismo módulo"),
             ("Protección de datos e implementación","M7 · C4, su propia clase")]),
"M7 · C2": (["MCG y AGP en entornos digitales",
             "Monitoreo remoto de pacientes, apps y dispositivos vestibles",
             "Salud conectada e integración de datos"],
            [("ATENCIÓN — interpretación clínica del AGP y del tiempo en rango","M4 · C2, Dra. Josefa Palacio. Ella da la lectura clínica: céntrese usted en la implementación digital y el monitoreo a distancia"),
             ("Marco normativo de telesalud","M7 · C1, Dra. Omidres Pérez"),
             ("IA aplicada al tamizaje","M7 · C3, su mismo módulo")]),
"M7 · C3": (["Terapias digitales (DTx): qué son y qué evidencia tienen",
             "IA en tamizaje y apoyo a la decisión clínica",
             "Educación digital del paciente y adherencia"],
            [("Monitoreo continuo, apps y wearables","M7 · C2, su mismo módulo"),
             ("Conducta alimentaria y adherencia en consulta presencial","M2 · C3, Dra. Janneth Bermeo"),
             ("Protección de datos y ética","M7 · C4, Dra. Omidres Pérez")]),
"M7 · C4": (["Programas híbridos de teleconsulta y telenutrición",
             "Protección de datos en salud",
             "Interoperabilidad y calidad"],
            [("Marco normativo general de telesalud","M7 · C1, su propia clase anterior"),
             ("Tecnologías de monitoreo","M7 · C2, su mismo módulo"),
             ("IA y terapias digitales","M7 · C3, su mismo módulo")]),
}

# ---------- generación de los mensajes ----------
def msg(cod):
    c = CL[cod]; si, no = D[cod]
    mod = cod.split(' · ')[0]
    p = []
    p.append("*Su clase: %s*\n%s · 30 minutos grabados" % (c['tema'], cod.replace('M','Módulo ').replace(' · C',', Clase ')))
    p.append("El programa declara estos contenidos para su clase:\n%s" % c['cont'])
    p.append("*Lo que sí es suyo, con toda libertad:*\n" + "\n".join("• "+x for x in si))
    p.append("*Lo que le pido que no toque, porque lo dicta otra persona:*\n" +
             "\n".join("• %s\n  → %s" % (q, quien) for q, quien in no))
    p.append("*La grabación:* por Zoom. Le paso el enlace y coordinamos día y hora.\n"
             "*La fecha de entrega:* %s." % FECHAS[mod])
    p.append("Si algo de esto le aprieta o cree que falta, dígame con toda confianza y lo ajustamos. "
             "Prefiero acomodarlo ahora y no cuando ya esté grabado.")
    return "\n\n".join(p)

doc = ["""# Delimitación de las 28 clases — qué cubre cada ponente

**Generado el 24 de septiembre de 2026.** Nace de la pregunta de la Lcda. Isabel
Reinoso: «¿qué otros temas hay, por si se chocan?». Ninguna otra persona lo había
preguntado, y el riesgo era real.

Cada bloque trae el mensaje listo para enviar por WhatsApp a esa persona. Lo único que
cambia es el nombre del saludo, que va aparte.

## Los nueve choques reales del programa

No son suposiciones: son contenidos declarados por duplicado en el programa original.

| Se repite | Entre | Cómo se reparte |
|---|---|---|
| Dieta mediterránea, restricción de carbohidratos, ayuno intermitente | M2 · C2 y M5 · C2 | M2 lo enfoca en obesidad; M5, en diabetes |
| Agonistas de GLP-1 y tirzepatida | M3 · C2, M3 · C3 y M4 · C3 | El módulo 3 los ve como tratamiento de la obesidad; el 4, como control glucémico |
| MCG y AGP | M4 · C2 y M7 · C2 | M4 da la interpretación clínica; M7, la implementación digital |
| Bioimpedancia y sarcopenia | M1 · C4, M5 · C4 y M6 · C4 | M1 da el método; M5 lo aplica a diabetes; M6 la trata como complicación |
| Beneficios renales de las nuevas terapias | M6 · C1 y M6 · C3 | M6 · C1 se queda con tamizaje y diagnóstico |
| Fenotipos metabólicos | M1 · C3 y M5 · C1 | M1 para clasificar al paciente; M5 para decidir el plan nutricional |

## Por qué importa

Son 28 clases grabadas que el participante ve seguidas. Si dos ponentes desarrollan lo
mismo, el que va segundo queda mal sin haber hecho nada mal. Y como se graban por
separado y sin verse entre ellos, nadie puede darse cuenta solo.

---
"""]
for cod in sorted(D, key=lambda k: (k.split(' · ')[0], k)):
    c = CL[cod]
    doc.append("## %s — %s\n" % (cod, c['tema']))
    doc.append("**Ponente:** %s · **Entrega:** %s\n" % (c['ponente'] or '— sin ponente —', FECHAS[cod.split(' · ')[0]]))
    doc.append("```\n%s\n```\n" % msg(cod))
    doc.append("---\n")
io.open('/home/user/Academic-/curso-obesidad-seda/brief-delimitacion-28-clases.md','w',encoding='utf-8').write("\n".join(doc))
print("clases documentadas:", len(D))
