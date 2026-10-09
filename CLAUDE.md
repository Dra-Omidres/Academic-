# Academic- · Curso virtual SEDA

Repositorio de trabajo de la **Dra. Omidres Pérez de Carvelli** para coordinar el
*Curso virtual de actualización en obesidad, diabetes, nutrición clínica y salud digital*
de la **Sociedad de Endocrinología y Diabetes del Austro (SEDA)** y armar el expediente
con el que se solicita el **aval académico de la Universidad de Cuenca**.

No es un proyecto de software: es un expediente administrativo con herramientas en Python
que lo mantienen al día. Todo está en español y así debe seguir.

## Cómo funciona

```
SEDA_Matriz_Ponentes_Curso_Obesidad.xlsx     ← única fuente de verdad
          │
          ├── generador-directorio-pdf.py    → SEDA_Directorio_Ponentes.pdf
          ├── generador-programa-pdf.py      → SEDA_Programa_Academico.pdf
          ├── generador-grupo-whatsapp.py    → SEDA_Grupo_WhatsApp.html
          └── generador-*.py                 → el resto de entregables
```

La matriz manda. **Los PDF y HTML son productos: no se editan a mano, se regeneran.**
Si un dato cambia, se cambia en la matriz y se vuelve a correr el generador.

Sus cuatro hojas: `Instrucciones`, `Matriz 28 clases` (el programa: 7 módulos × 4 clases),
`Ponentes - datos aval` (los 23 docentes y el estado de sus documentos) y
`Vacantes por cubrir`.

## Estructura

| | |
|---|---|
| `curso-obesidad-seda/` | todo el proyecto |
| `├─ expediente/` | documentos recibidos de los docentes · **datos personales** |
| `│   ├─ hojas-de-vida/` · `fotografias/` · `documentos-identidad/` · `declaraciones-coi/` | |
| `├─ activos/` | imágenes que usan los generadores |
| `├─ generador-*.py` | los generadores |
| `├─ SEDA_*.pdf / .xlsx / .docx / .html` | entregables |
| `├─ whatsapp-*.md` · `correo-*.md` | mensajes redactados, listos para copiar |
| `└─ conflictos-de-interes-expediente.md` | **documento de registro de decisiones** |

## Instalar y ejecutar

```bash
pip install openpyxl reportlab python-docx pdfplumber pillow pypdfium2
cd curso-obesidad-seda
python3 generador-directorio-pdf.py      # regenera el PDF de seguimiento
```

Python 3.11 · openpyxl 3.1.5 · reportlab 5.0.1 · pdfplumber 0.11.10 · python-docx 1.2.0 ·
pillow 12.3.0.

No hay tests. **La verificación es leer el PDF generado**, con `pdfplumber` para el texto o
`pypdfium2` para renderizar una página y mirarla. Hacerlo siempre antes de dar algo por bueno:
los errores de este proyecto han sido de contenido, no de código.

`pdfplumber` entrelaza las columnas cuando una celda ocupa dos líneas, así que para
comprobar una tabla conviene verificar **la estructura de datos**, no el texto extraído.

## Reglas que hay que respetar

**Datos personales.** El `expediente/` tiene cédulas, pasaportes, teléfonos y domicilios
profesionales de 23 personas. No se publica, no se sube a ningún servicio y no sale de la
coordinación. Nunca escribir un número de documento en un archivo que no lo necesite.

**No inventar nada.** Si un dato no se puede leer —un escaneo borroso, una firma dudosa—
se escribe `ILEGIBLE` o `POR CONFIRMAR` y se pide. Ya pasó: una cédula manuscrita
ilegible se dejó sin transcribir en vez de adivinarla.

**Verificar el documento, no su nombre de archivo.** Una declaración llamada
`...-signed.pdf` llegó completamente en blanco. Hay que abrir cada archivo y comprobar que
esté lleno y firmado antes de contarlo.

**Convención de nombres** en `expediente/`: `TIPO_Apellido1-Apellido2_Nombre.ext`
(`COI_Bermeo-Cabrera_Janneth_firmada.pdf`).

**Paleta de la casa**, en todos los generadores:
`TEAL #0D5A62` · `GOLD #B8852B` · `MINT #C8E1DF` · `PALE #EDF5F4` · `WARM #FBF1DC` ·
`INK #1A2325` · `MUTED #5F7073`.

**Los mensajes se redactan, no se envían.** Van a un `.md` para que la Dra. Omidres los
revise y los mande. Nada sale a su nombre sin que lo haya leído.

## Decisiones y errores conocidos

**La Universidad exige solo la hoja de vida.** Su reglamento pide «expositoras o
expositores propuestos, con sus hojas de vida». La fotografía, la copia de la cédula y la
declaración de conflicto de interés **las añadió esta coordinación**. Durante diez días el
directorio afirmó lo contrario y se persiguió a 22 personas por documentos que nadie había
pedido. Al priorizar: primero hojas de vida, después declaraciones.

**La declaración de conflicto de interés se mantiene aunque no sea obligatoria.** El curso
tiene tres auspiciantes farmacéuticos y la plataforma pertenece a la compañía de la
coordinadora: es lo que sostiene el expediente si la Comisión pregunta. Todo esto, con sus
rutas de pago y los conflictos declarados, está en `conflictos-de-interes-expediente.md`,
que **hay que leer antes de tocar cualquier cosa de auspicios o de Omisalud**.

**Las celdas de estado tienen tres valores, no dos.** En `generador-directorio-pdf.py`:
empieza por `SÍ` (entregado, no se persigue) · contiene `YA PEDIDA` (no cuenta, pero
tampoco se vuelve a escribir) · cualquier marca de duda (`POSIBLE`, `EN BLANCO`,
`ILEGIBLE`, `PROVISIONAL`, `POR CONFIRMAR`) no cuenta y hay que pedirlo. La columna de
identidad guarda **el número**, no un `SÍ`: se evalúa con `tiene()`, no con `si()`.

**Los nombres no se emparejan por el último apellido.** Hay dos Molina, dos Cabrera y dos
González: hacerlo así cruzó clases entre personas. El emparejamiento compara los nombres
completos token a token con tolerancia a variantes de escritura (Janeth/Janneth,
Palacios/Palacio).

**Las cédulas ecuatorianas se validan** con el dígito verificador del Registro Civil
(módulo 10). Eso prueba que el número está bien transcrito, **no** que exista ni que sea de
esa persona. La regla del tercer dígito ≤ 5 no aplica a cédulas de extranjero residente.

**Las fotografías suelen venir dentro de las hojas de vida.** Se extraen con
`unzip word/media/*` en los `.docx` y leyendo el stream de la imagen en los `.pdf`. Hay que
mirar cada una: puede ser un logotipo o un membrete. Y comprobar el tamaño — una imagen de
perfil de WhatsApp (150 × 150 px) no sirve para el expediente.
