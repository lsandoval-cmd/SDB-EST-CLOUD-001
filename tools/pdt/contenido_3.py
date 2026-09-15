# -*- coding: utf-8 -*-
"""Contenido redactado del PDT — bloque 3 (SDB-027 a SDB-040)."""

BLOQUE_3 = {

"SDB-027": {
 "titulo": "La pantalla donde se revisan y corrigen las novedades",
 "proposito": "Es la pantalla que va a usar Administración todos los meses. Tiene que mostrar las excepciones entre lo que se cargó en campo y lo que hay en el sistema, y permitir corregir dejando rastro de quién cambió qué.",
 "entregables": [
   "Vista de novedades por persona y período, con la procedencia de cada dato.",
   "Excepciones campo vs. base visibles y accionables.",
   "Corrección y aprobación limitadas a revisores habilitados, verificado en el backend.",
   "Trazabilidad completa de cada cambio: valor anterior, valor nuevo, autor y fecha.",
   "Pruebas de usuario sin permiso, novedad ya corregida y períodos solapados.",
 ],
 "listo": "Cuando alguien de Administración puede corregir una novedad y otra persona puede ver exactamente qué cambió y quién lo hizo.",
 "claude": """Construyamos la pantalla de revisión de novedades. Esta la va a usar Administración de verdad, así que la usabilidad importa tanto como la lógica.

1. Definí en `docs/SDB-027/contrato-novedades.md` qué es una novedad en nuestro modelo: por persona y por período, con su procedencia (de dónde salió cada valor) y su estado (`propuesta`, `corregida`, `aprobada`).
2. Implementá la vista:
   - Agrupada por persona y período, con las excepciones campo vs. base destacadas arriba.
   - Cada valor muestra su origen. Un valor corregido a mano se ve distinto de uno que vino del sistema.
   - Acciones de corregir y aprobar, habilitadas sólo para revisores autorizados. La verificación va en el backend; el ocultamiento en la UI es cortesía, no seguridad.
3. Implementá la trazabilidad: cada cambio guarda valor anterior, valor nuevo, autor, fecha y motivo opcional. Esa historia se puede consultar desde la misma pantalla.
4. Probá:
   - Un usuario sin permiso intenta corregir → denegado por el backend y registrado.
   - Una novedad ya corregida que recibe una corrección nueva → la historia conserva las dos.
   - Dos períodos solapados para la misma persona → se detecta y se muestra.

Pensá la pantalla para alguien que tiene que revisar cuarenta personas en una tarde: que se pueda avanzar rápido y que los casos normales no pidan atención.""",
 "codex": """Implementar la pantalla de revisión de novedades del piloto SUDBAU.

Modelo: `novedad { ID_Persona, periodo, campo, valor_propuesto, valor_corregido, origen, estado ∈ {propuesta, corregida, aprobada} }` más `historial { valor_anterior, valor_nuevo, autor, fecha, motivo }`.

Requisitos:
- Excepciones campo vs. base priorizadas en el render.
- Corrección y aprobación autorizadas en el backend por rol; la UI no es la barrera.
- Todo cambio escribe una entrada de historial inmutable.
- Detección y visualización de períodos solapados para una misma persona.

Tests: usuario sin rol de revisor recibe 403 del backend al corregir y al aprobar; doble corrección conserva ambas entradas de historial; solapamiento de períodos detectado.

Entregá diff y salida real de tests.""",
 "flex": "El flujo de estados (`propuesta → corregida → aprobada`) es una propuesta; si Administración trabaja con dos estados, simplifíquenlo. El historial inmutable es lo que yo no sacaría: es lo que permite responder «¿quién cambió esto?» sin adivinar, y en temas de nómina esa pregunta aparece. [Ajustar según necesidad]",
},

"SDB-028": {
 "titulo": "Congelar el lote aprobado y exportarlo sin riesgo de mandarlo dos veces",
 "proposito": "Una vez que las novedades están aprobadas, el lote se congela: esa versión no cambia más. Preparar el lote y enviarlo afuera son dos cosas separadas, porque un envío duplicado al prestador es un problema real.",
 "entregables": [
   "Versión inmutable del lote aprobado, vinculada a persona, período y revisión.",
   "Generación y exportación con control de acceso e idempotencia.",
   "Separación explícita entre preparar el lote y enviarlo afuera.",
   "Prueba de repetición: exportar dos veces no produce dos lotes ni dos efectos.",
   "Conciliación de la devolución de prueba del prestador.",
 ],
 "listo": "Cuando repetís la exportación por error y no pasa nada malo.",
 "claude": """Implementemos la generación del lote aprobado.

1. Definí en `docs/SDB-028/contrato-lote.md`: qué identifica a un lote (persona, período, revisión), qué lo congela, y por qué una vez congelado no se modifica — si hay que corregir, se genera un lote nuevo que referencia al anterior.
2. Implementá:
   - Generación del lote a partir de novedades en estado `aprobada`, con hash del contenido y versión.
   - Inmutabilidad: intentar modificar un lote congelado falla de forma explícita.
   - Control de acceso: quién puede generar y quién puede exportar son permisos distintos.
   - Idempotencia: exportar el mismo lote dos veces no produce dos efectos externos. Usá una clave de idempotencia por lote.
3. Separá claramente dos operaciones en el código: `preparar_lote` (interna, reversible) y `enviar_lote` (externa, con efecto). El paso de una a otra requiere una acción humana explícita.
4. Probá: doble exportación del mismo lote; exportación por un usuario sin permiso; intento de modificar un lote congelado; conciliación de la devolución de prueba.

El caso de doble exportación es el que hay que probar mejor. Un lote de novedades enviado dos veces al prestador es un problema que después se arregla con llamadas telefónicas.""",
 "codex": """Implementar la generación y exportación de lotes aprobados del piloto SUDBAU.

Modelo: `lote { lote_id, periodo, personas[], revision_id, contenido_hash, estado ∈ {preparado, exportado}, creado_por, exportado_por, idempotency_key }`.

Requisitos:
- El lote se construye sólo con novedades en estado `aprobada` y queda inmutable tras su creación; toda modificación posterior exige un lote nuevo que referencie al anterior.
- Permisos separados para `preparar_lote` y `enviar_lote`.
- `enviar_lote` es idempotente por `idempotency_key`; una segunda invocación devuelve el resultado original sin repetir el efecto externo.

Tests: doble envío no duplica el efecto; modificación de lote congelado rechazada; usuario sin permiso de envío recibe 403; conciliación de la devolución contra el contenido del lote.

Entregá diff y salida real de tests.""",
 "flex": "Si el prestador acepta reenvíos sin problema, la idempotencia baja de crítica a deseable — pero confírmenlo con ellos antes de relajarla, no lo supongan. La separación preparar/enviar podría parecer burocracia; es lo que permite que alguien revise antes de que algo salga de la empresa. [Ajustar según necesidad]",
},

"SDB-029": {
 "titulo": "Juntar los documentos con los que vamos a probar A02 y saber qué dice cada uno",
 "proposito": "Para evaluar una extracción automática hace falta saber primero cuál es la respuesta correcta. Armamos un conjunto de 20 documentos variados, con su verdad de referencia hecha por una persona y el tiempo que lleva revisarlos a mano.",
 "entregables": [
   "20 documentos autorizados, con diversidad real de calidad: buenos, escaneados, torcidos, con manuscritos.",
   "Originales identificados y conservados.",
   "Verdad de referencia validada por una persona, distinguiendo campo presente, ausente y ambiguo.",
   "Medición de la revisión manual: cuánto tarda hoy una persona por documento.",
   "Registro separado de salida bruta de OCR, corrección humana y resultado final.",
 ],
 "listo": "Cuando tenemos 20 documentos con su respuesta correcta validada y sabemos cuántos minutos cuesta hoy hacerlo a mano.",
 "claude": """Preparemos el conjunto de evaluación de A02.

1. Definí en `docs/SDB-029/criterio-seleccion.md` qué diversidad queremos en los 20 documentos: tipo de documento, calidad de imagen, presencia de manuscritos, orientación, idioma. La tentación es elegir los 20 más lindos; hay que resistirla.
2. Preparame la estructura de trabajo: dónde van los originales (sin modificar), dónde la verdad de referencia, y cómo se vinculan.
3. Diseñá la plantilla de verdad de referencia en `docs/SDB-029/verdad-referencia.md`: por documento y por campo, el valor correcto, y un estado que distinga `presente`, `ausente` y `ambiguo`. El estado `ambiguo` es importante: hay campos que un humano tampoco puede leer con certeza, y A02 no debería ser penalizado por eso ni premiado por inventar.
4. Diseñá el protocolo de medición manual: quién revisa, cómo se cronometra, y cómo se registra.
5. Definí el registro de tres columnas que vamos a mantener siempre separadas: salida bruta del OCR/modelo, corrección humana, resultado final. No se pueden mezclar: un valor que completó una persona no es un acierto del modelo.

Si no tenés acceso a los documentos reales, preparame toda la estructura y el procedimiento, y dejá marcado qué tengo que cargar yo.""",
 "codex": """Generar la estructura de evaluación de A02 del piloto SUDBAU.

- `docs/SDB-029/criterio-seleccion.md`: dimensiones de diversidad requeridas en los 20 documentos (tipo, calidad, manuscritos, orientación).
- `data/a02/originals/` (sólo estructura y `.gitkeep`): originales sin modificar.
- `docs/SDB-029/verdad-referencia.schema.json` y `verdad-referencia.md`: por documento y campo, `{ valor, estado ∈ {presente, ausente, ambiguo}, validado_por }`.
- `docs/SDB-029/linea-base-manual.md`: plantilla de medición con `documento_id`, `revisor`, `minutos`, `campos_corregidos`.
- `docs/SDB-029/registro-tres-columnas.md`: definición del registro separado de salida bruta, corrección humana y resultado final, con la regla de que un valor completado por una persona nunca se contabiliza como acierto del modelo.

No implementes extracción en este cambio ni cargues documentos.""",
 "flex": "Veinte documentos puede ser mucho para arrancar: con doce bien elegidos y variados se aprende casi lo mismo. Lo que no reduciría es la diversidad de calidad — un corpus de documentos prolijos da una métrica que después se rompe en el primer mes de uso real. [Ajustar según necesidad]",
},

"SDB-030": {
 "titulo": "Que A02 proponga campos, siempre como borrador y siempre atado al original",
 "proposito": "Extraer datos de documentos para ahorrarle tipeo a una persona. Nunca para aprobar nada solo. Cada campo propuesto trae de dónde salió y cuánta confianza tiene, y el original queda intacto al lado.",
 "entregables": [
   "Esquema de A02 con procedencia por campo: página, ubicación, y confianza útil.",
   "Extracción implementada como borrador, vinculada al documento original.",
   "Salida bruta conservada antes de cualquier edición humana.",
   "Errores y ausencias visibles, no rellenados.",
   "Cotejo contra la OT correspondiente, mostrando discrepancias sin resolverlas automáticamente.",
   "Ninguna aprobación de certificados ni de facturación.",
 ],
 "listo": "Cuando A02 propone diez campos, se equivoca en dos, y las dos equivocaciones se ven a simple vista.",
 "claude": """Implementemos el extractor de A02.

1. Definí el esquema en `docs/SDB-030/esquema-a02.md`: por cada campo extraído, `{ valor, pagina, ubicacion, confianza, estado }`. La confianza tiene que ser útil: si siempre devuelve 0.99, no sirve para nada. Calibrala contra la verdad de referencia de SDB-029 y decime qué umbral separa lo que conviene revisar de lo que conviene aceptar.
2. Implementá la extracción:
   - Todo lo que sale es un borrador. El estado inicial de cada campo es `propuesto`, nunca `confirmado`.
   - La salida bruta se guarda tal cual, antes de que nadie la toque. Esa copia no se modifica nunca.
   - Un campo que no se pudo leer se devuelve como `ausente`, no como cadena vacía ni como valor plausible.
   - Cada campo referencia al documento original y a la ubicación dentro de él.
3. Implementá el cotejo contra la OT correspondiente: mostrar las discrepancias entre lo que dice el documento y lo que dice el sistema. Mostrarlas, no resolverlas.
4. Límite duro, escribilo en el código y en el documento: A02 no aprueba certificados ni genera facturación. Propone campos para que una persona revise.

Evaluá el resultado contra la verdad de referencia y traeme la tabla: por campo, aciertos, errores y ausencias mal resueltas.""",
 "codex": """Implementar el extractor de documentos A02 del piloto SUDBAU.

Salida por campo: `{ valor, pagina, ubicacion, confianza, estado ∈ {propuesto, ausente, ilegible} }`, vinculada a `documento_id`.

Requisitos:
- La salida bruta se persiste antes de cualquier edición y es inmutable.
- Ningún campo se completa con un valor inferido cuando no se pudo leer: se devuelve `ausente` o `ilegible`.
- Cotejo automático contra la OT correspondiente que emite discrepancias, sin aplicarlas.
- Prohibido exponer cualquier operación de aprobación de certificado o facturación desde este módulo.

Evaluación: script que compare la salida contra `docs/SDB-029/verdad-referencia.*` y emita precisión por campo, separando `presente`, `ausente` y `ambiguo`.

Tests: campo ilegible no se rellena; salida bruta inmutable tras corrección; discrepancia con la OT reportada y no aplicada.

Entregá diff, salida real de tests y la tabla de precisión por campo.""",
 "flex": "Si el proveedor de OCR que usen no devuelve confianza por campo, es válido derivarla de otra señal o directamente no tenerla — pero díganlo, en vez de inventar un número. La ubicación dentro del documento es opcional si complica mucho; lo que hace la diferencia en la revisión es poder ver el original al lado. [Ajustar según necesidad]",
},

"SDB-031": {
 "titulo": "La pantalla de revisión de A02: el original a la izquierda, la propuesta a la derecha",
 "proposito": "Hacer que revisar un documento sea rápido y verificable. La persona ve el documento y los campos propuestos al mismo tiempo, corrige lo que haga falta, y todo queda registrado como corrección humana, no como acierto del modelo.",
 "entregables": [
   "Vista lado a lado: documento original y campos propuestos.",
   "Corrección humana claramente diferenciada del valor propuesto.",
   "Conservación de valor propuesto, valor corregido, autor y fuente.",
   "Guardar la revisión no envía ni aprueba nada automáticamente.",
   "Pruebas con campos ausentes, campos erróneos y documentos ilegibles.",
 ],
 "listo": "Cuando revisar un documento con la pantalla lleva menos tiempo que hacerlo a mano — medido, no supuesto.",
 "claude": """Construyamos la pantalla de revisión de A02.

1. Implementá la vista lado a lado: el documento original renderizado (con la página correcta) y los campos propuestos editables al costado. Si tenés la ubicación del campo dentro del documento, resaltala al enfocar el campo — eso solo acelera muchísimo la revisión.
2. Diferenciá visualmente y en el modelo: valor propuesto por el modelo, valor corregido por la persona, y campo sin resolver. Guardá siempre los tres datos: propuesto, corregido, autor.
3. Regla de comportamiento, importante: guardar la revisión **no** envía, no aprueba y no dispara ningún efecto externo. Si más adelante existe un envío, será una acción aparte y explícita. Probalo.
4. Probá los casos que importan: campo ausente, campo con valor erróneo, documento ilegible completo, y una revisión guardada a medias que se retoma después.
5. Medí: cronometrá la revisión de cinco documentos con la pantalla y compará contra la línea base manual de SDB-029. Si no mejora, es un dato valioso, no un fracaso — decímelo.

Pensala para alguien que revisa treinta documentos seguidos: teclado antes que mouse, y que se pueda pasar al siguiente sin levantar las manos.""",
 "codex": """Implementar la pantalla de revisión de A02 del piloto SUDBAU.

Requisitos:
- Render lado a lado del documento original (página correspondiente) y los campos propuestos editables.
- Modelo por campo: `{ valor_propuesto, valor_corregido, autor_correccion, fuente, estado }`. Los tres primeros se conservan siempre.
- Diferenciación visual entre propuesto, corregido y sin resolver.
- `guardar_revision` no produce envío ni aprobación ni ningún efecto externo.
- Navegación por teclado entre campos y entre documentos.

Tests: campo ausente editable sin valor precargado; corrección conserva el valor propuesto original; guardar revisión no dispara efectos externos (verificado con espía sobre las salidas); revisión parcial persistida y retomada.

Entregá diff, salida real de tests y la medición de tiempo de revisión sobre cinco documentos.""",
 "flex": "El render del documento original puede ser caro de implementar según el formato; si al principio muestran sólo la imagen de la página sin resaltado, ya es suficiente para probar el concepto. La medición de tiempo contra la línea base es lo que después justifica (o desestima) seguir invirtiendo en A02. [Ajustar según necesidad]",
},

"SDB-032": {
 "titulo": "Saber cuánto nos cuesta la IA y poder apagarla",
 "proposito": "Medir consumo real por agente y por ejecución, poner límites que funcionen, y ensayar qué pasa cuando el proveedor se cae o cuando hay que suspender todo. Sin esto, la conversación sobre costos de IA es adivinanza.",
 "entregables": [
   "Métricas de consumo por agente y ejecución, con versión del modelo.",
   "Límites configurados de contexto, salida y reintentos.",
   "Mecanismo de suspensión probado del lado del servidor.",
   "Ensayo de fallas: proveedor caído, límite agotado, respuesta inválida.",
   "Minimización de datos sensibles enviados al modelo, verificada.",
   "Supuestos de costo documentados: tarifa, fecha, volumen asumido y exclusiones.",
 ],
 "listo": "Cuando podés decir, con números, cuánto costó A01 el mes pasado y cuánto costaría con el triple de uso.",
 "claude": """Instrumentemos el costo y la protección de la capa de IA.

1. Instrumentá el consumo por ejecución: agente (A01 / A02), tokens de entrada, tokens de salida, versión del modelo, latencia, usuario, y resultado. Guardalo de forma consultable.
2. Revisá y ajustá los límites de SDB-022 con los datos reales que estés viendo: contexto, salida, reintentos, pasos. Documentá por qué cada valor.
3. Minimización de datos: revisá exactamente qué se le envía al modelo y recortá todo lo que no haga falta. En particular, ningún CUIL, ningún dato personal que no sea necesario para la respuesta, ningún secreto. Contame qué encontraste y qué sacaste.
4. Ensayá fallas, con evidencia de cada una:
   - Proveedor no disponible → la app sigue funcionando sin IA, con mensaje claro.
   - Límite de tokens agotado a mitad de una respuesta.
   - Respuesta del modelo con formato inválido.
   - Suspensión activada durante una ejecución en curso.
5. Escribí `docs/SDB-032/costos-ia.md` con: tarifa vigente y su fecha, volumen asumido para el piloto, costo mensual estimado, y qué queda explícitamente excluido del cálculo. Marcá la tarifa como verificada sólo si la verificaste contra la documentación oficial vigente.

La alternativa manual tiene que seguir existiendo. Verificá que si la IA está caída, el trabajo se puede hacer igual.""",
 "codex": """Instrumentar consumo, límites y resiliencia de la capa de IA del piloto SUDBAU.

Métricas por ejecución: `{ agente, modelo_version, tokens_entrada, tokens_salida, latencia_ms, usuario, resultado, costo_estimado }`, consultables por período y por agente.

Requisitos:
- Límites configurables de contexto, salida, reintentos y pasos, con valores por defecto documentados.
- Sanitización del payload enviado al modelo: test que verifique que no viajan CUIL, credenciales ni campos personales no requeridos.
- Degradación: con el proveedor no disponible, la aplicación responde sin IA y ofrece la ruta manual.
- Suspensión efectiva en ejecuciones en curso y nuevas.

Tests: proveedor caído → degradación sin error al usuario; límite de salida agotado → corte controlado y registro; respuesta con formato inválido → manejada sin exponer traza; suspensión durante ejecución.

Entregá diff, salida real de tests y `docs/SDB-032/costos-ia.md` con tarifa, fecha de verificación, volumen asumido y exclusiones.""",
 "flex": "El costo estimado va a estar mal: siempre lo está al principio. Lo importante es que quede escrito con qué supuestos, para poder corregirlo cuando lleguen los números reales. La prueba de degradación sin IA es la que yo pondría primero — es la que protege la operación. [Ajustar según necesidad]",
},

"SDB-033": {
 "titulo": "Mostrar el piloto completo y escuchar el veredicto",
 "proposito": "Poner todo junto frente a los dueños funcionales: la OT trazable, A01, el lote administrativo. Y escuchar con honestidad qué sirve, qué falta y qué riesgos se aceptan.",
 "entregables": [
   "Demo integral preparada: de parte de campo a indicadores y a lote de novedades.",
   "Brechas conocidas listadas de antemano, no escondidas.",
   "Validación de los dueños funcionales sobre alcance, utilidad y pendientes.",
   "Riesgos aceptados registrados, con la autoridad que los acepta identificada.",
   "Acta del piloto con decisiones, condiciones y próximos pasos.",
   "Sin declaraciones de certificación ISO ni de cumplimiento normativo que no existan.",
 ],
 "listo": "Cuando hay un acta firmada que dice qué se acepta, con qué condiciones y qué queda pendiente.",
 "claude": """Preparemos la aceptación del piloto.

1. Armá el guion de la demo integral en `docs/SDB-033/guion-demo-integral.md`: el recorrido completo desde un parte de campo hasta los indicadores y el lote de novedades revisadas. Máximo 30 minutos. Cada paso con lo que se espera ver.
2. Antes de la demo, escribí la lista de brechas conocidas en `docs/SDB-033/brechas.md`. Se muestran al principio, no se esconden: que aparezcan durante la demo es mucho peor que anunciarlas.
3. Preparame la plantilla de acta `docs/SDB-033/acta-piloto.md`: qué se demostró (con versión y ambiente), quién validó y en qué rol, qué se acepta, con qué condiciones, qué riesgos se aceptan y quién tiene autoridad para aceptarlos, y los próximos pasos con responsable.
4. Revisá el estado real del repositorio y decime con franqueza qué partes del recorrido están y cuáles no. Prefiero una demo de tres cuartos honesta que una completa con humo.

Nada en el acta puede decir que el sistema está certificado, ni que cumple una norma. Podemos decir que está alineado con un criterio; alineación, implementación y certificación son tres cosas distintas.""",
 "codex": """Generar el paquete de aceptación del piloto SUDBAU en `docs/SDB-033/`.

- `guion-demo-integral.md`: recorrido de parte de campo → normalización → indicadores → A01 → novedades → lote, con versión y ambiente por paso, en 30 minutos.
- `brechas.md`: brechas conocidas con impacto y responsable, para presentar al inicio de la demo.
- `acta-piloto.md`: plantilla con qué se demostró (versión, ambiente, fecha), validadores y su rol, aceptación, condiciones, riesgos aceptados con autoridad que los acepta, próximos pasos.
- `estado-real.md`: verificación contra el repositorio de qué componentes del recorrido existen y cuáles no, sin suponer.

No incluyas afirmaciones de certificación ni de cumplimiento normativo. Los campos de validación quedan en `PENDIENTE`.""",
 "flex": "Si el piloto llega con menos de lo previsto, esta tarea sigue siendo valiosa: el acta de «esto sirve, esto no, esto falta» es el entregable. La demo de 30 minutos puede ser de 15. Lo que no cambiaría es anunciar las brechas antes de mostrarlas. [Ajustar según necesidad]",
},

"SDB-034": {
 "titulo": "Cerrar un período completo junto a Administración y al prestador",
 "proposito": "Probar el circuito de novedades de punta a punta en un período real, viendo qué diferencias aparecen contra lo que hoy se hace. La liquidación sigue siendo del prestador: nosotros conciliamos.",
 "entregables": [
   "Período de prueba elegido y acordado.",
   "Lote, novedades, correcciones y devolución relacionados entre sí.",
   "Conciliación con Administración y con el prestador, conservando IDs y versiones.",
   "Diferencias documentadas: resueltas y pendientes, con responsable.",
   "Confirmación explícita de que el cálculo salarial sigue tercerizado.",
 ],
 "listo": "Cuando las diferencias del período están explicadas una por una, sin promedios ni redondeos.",
 "claude": """Conciliemos un período completo.

1. Elegí con Administración un período de prueba y documentá por qué ese: volumen manejable, sin eventos raros, con datos disponibles.
2. Armá la trazabilidad del período en `docs/SDB-034/trazabilidad-periodo.md`: el lote generado, las novedades que lo componen, las correcciones aplicadas y la devolución recibida, todo relacionado por ID y versión.
3. Conciliá contra lo que hace Administración hoy. Para cada diferencia:
   - Qué muestra nuestro circuito y qué muestra el proceso actual.
   - Por qué difieren (regla distinta, dato faltante, corrección no propagada, error nuestro).
   - Si se resolvió o queda pendiente, y quién es el responsable.
   Una diferencia sin explicación queda abierta. No la cierres por ser chica.
4. Escribí explícitamente en el informe que el cálculo de liquidación lo sigue haciendo el prestador y que nuestro circuito prepara y concilia novedades.

Si aparecen muchas diferencias, eso es información útil sobre dónde están las reglas mal entendidas, no un fracaso del circuito. Traémelas ordenadas por frecuencia.""",
 "codex": """Generar la conciliación del período de prueba del piloto SUDBAU en `docs/SDB-034/`.

- `trazabilidad-periodo.md`: relación `lote_id → novedades → correcciones → devolución`, con IDs y versiones.
- `conciliacion.md`: tabla de diferencias `{ concepto, valor_circuito, valor_proceso_actual, causa, estado ∈ {resuelta, pendiente}, responsable }`.
- `informe-periodo.md`: resumen, diferencias por frecuencia de causa, y declaración explícita de que el cálculo de liquidación permanece tercerizado.

Si existe un script de conciliación, agregalo en `tools/sdb-034/` con sus tests. No cierres diferencias por magnitud; toda diferencia sin causa identificada queda `pendiente`.""",
 "flex": "Si Administración prefiere conciliar en su propia planilla, úsenla: el entregable es la lista de diferencias explicadas, no el formato. Lo único que evitaría es el impulso de cerrar diferencias chicas por ser chicas — suelen ser la punta de una regla mal entendida. [Ajustar según necesidad]",
},

"SDB-035": {
 "titulo": "Escribir la guía y comprobar que alguien la puede seguir sin ayuda",
 "proposito": "Una guía que sólo entiende quien la escribió no sirve. La prueba es simple: alguien que no participó completa el caso mirando la guía, sin que nadie lo ayude.",
 "entregables": [
   "Guía de uso para campo y para novedades, con capturas de la versión real que se está usando.",
   "Procedimiento de operación normal, pérdida de conexión, corrección y contingencia.",
   "Indicación clara de cuándo pedir ayuda y a quién.",
   "Prueba de adopción observada: un usuario completa el caso sin asistencia del autor.",
   "Registro de dudas, tiempo y mejoras sugeridas.",
 ],
 "listo": "Cuando alguien completó el caso mirando sólo la guía y anotamos dónde se trabó.",
 "claude": """Escribamos la guía de uso y probémosla de verdad.

1. Escribí la guía en `docs/SDB-035/guia-uso.md`, en dos partes: campo y novedades. Con capturas de la versión real que está desplegada, no de un prototipo. Lenguaje directo y frases cortas: la va a leer alguien con poco tiempo.
2. Incluí sí o sí:
   - Operación normal, paso a paso.
   - Qué hacer si se corta la conexión.
   - Cómo corregir algo que se cargó mal.
   - Contingencia: qué hacer si el sistema no está disponible (el procedimiento manual de respaldo).
   - Cuándo pedir ayuda, a quién, y qué información tener a mano al pedirla.
3. Diseñá la prueba de adopción en `docs/SDB-035/prueba-adopcion.md`: qué caso completa el usuario, qué se observa, y cómo se registra. La regla es que el autor de la guía observa en silencio y no ayuda.
4. Después de la prueba, actualizá la guía con lo que se aprendió. Registrá dudas, tiempo total y mejoras sugeridas.

La primera versión de la guía siempre tiene un paso obvio para el autor e invisible para el usuario. La prueba existe para encontrar ese paso.""",
 "codex": """Generar la guía de uso del piloto SUDBAU en `docs/SDB-035/`.

- `guia-uso.md`: secciones de campo y de novedades; operación normal, pérdida de conexión, corrección de carga, contingencia sin sistema, y a quién escalar con qué información. Referencias a capturas en `docs/SDB-035/img/` (creá la carpeta con `.gitkeep`; las capturas las carga el equipo desde la versión desplegada).
- `prueba-adopcion.md`: protocolo de observación con campos `usuario`, `caso`, `minutos`, `puntos_de_traba[]`, `dudas[]`, `mejoras[]`, y la regla explícita de que el autor no interviene.
- `contingencia.md`: procedimiento manual de respaldo.

No inventes capturas ni describas pantallas que no puedas verificar en el repositorio.""",
 "flex": "Si la guía puede ser un video de cinco minutos en vez de un documento, probablemente se use más. La prueba de adopción es la parte irremplazable: sin ella, la guía es una suposición sobre lo que el otro entiende. [Ajustar según necesidad]",
},

"SDB-036": {
 "titulo": "La puerta de producción: nada pasa sin que otro pueda reproducirlo",
 "proposito": "El último control antes de producción. Que el paquete esté completo, que otro integrante pueda desplegar y restaurar siguiendo el runbook, y que la decisión de publicar la tome quien tiene autoridad — no el calendario.",
 "entregables": [
   "Paquete de release completo: artefacto versionado, pruebas, revisión independiente, aceptación funcional, plan de reversión y runbook operativo.",
   "Despliegue y restauración reproducidos por un segundo integrante en ambiente autorizado, con evidencia.",
   "Verificación de que las dependencias están realmente satisfechas, con su resultado aceptado.",
   "Autoridad de release identificada y decisión registrada.",
   "Release registrada con versión, ambiente, fecha y resultado.",
 ],
 "listo": "Cuando otra persona desplegó y restauró siguiendo el runbook, y quien tiene autoridad dijo que sí por escrito.",
 "claude": """Preparemos la puerta de producción.

1. Armá la lista de verificación del release en `docs/SDB-036/checklist-release.md` y completala contra el repositorio real:
   - Artefacto versionado e identificable.
   - Pruebas ejecutadas, con su salida.
   - Revisión independiente hecha (por alguien que no escribió el código).
   - Aceptación funcional registrada (SDB-033).
   - Plan de reversión probado (SDB-020).
   - Runbook operativo (SDB-035).
   Marcá cada ítem como presente, ausente o parcial, con la referencia concreta.
2. Verificá las dependencias: cada tarea de la que depende este release, ¿tiene resultado aceptado en el ambiente requerido? Recordá el criterio de SDB-003.1: aceptado en TEST con evidencia satisface la dependencia; no hace falta inventar un PROD.
3. Preparame el procedimiento para que un segundo integrante reproduzca despliegue y restauración en el ambiente autorizado, y el formato de evidencia que tiene que dejar.
4. Registrá quién tiene autoridad para decidir la publicación y dejá el campo de decisión en PENDIENTE.

No ejecutes una publicación. Si todo está listo, decímelo y la decisión la toma una persona. Publicar no es un paso técnico más.""",
 "codex": """Generar el paquete de release del piloto SUDBAU en `docs/SDB-036/`.

- `checklist-release.md`: verificación contra el repositorio de artefacto versionado, pruebas con salida, revisión independiente, aceptación funcional, plan de reversión y runbook; estado `presente | ausente | parcial` con referencia concreta por ítem.
- `verificacion-dependencias.md`: por cada dependencia, resultado aceptado y ambiente; una dependencia aceptada en TEST con evidencia se considera satisfecha.
- `procedimiento-reproduccion.md`: pasos para que un segundo integrante despliegue y restaure, y formato de evidencia a registrar.
- `registro-release.md`: versión, ambiente, fecha, autoridad de release y decisión (`PENDIENTE`).

No ejecutes despliegues ni publicaciones desde este entorno.""",
 "flex": "Si el piloto no llega a producción y se queda en TEST, esta tarea igual vale: es el momento de ordenar el paquete. La regla que sí defendería es que el despliegue lo reproduzca otro — si sólo una persona sabe desplegar, eso es un riesgo operativo, no una eficiencia. [Ajustar según necesidad]",
},

"SDB-037": {
 "titulo": "Evaluar si conviene dejar que la IA haga una acción chiquita",
 "proposito": "Recién acá, después de todo lo anterior, miramos si vale la pena que un agente ejecute algo y no sólo responda. Una acción concreta, de bajo impacto y reversible. Y se evalúa antes de construir nada.",
 "entregables": [
   "Una acción N2 candidata identificada con precisión: recurso, parámetros, efecto exacto y reversibilidad.",
   "Beneficio esperado y riesgo evaluados, con números o con escenarios concretos.",
   "Definición de quién aprueba esa acción y con qué vigencia.",
   "Decisión registrada, con límites explícitos.",
   "N3 (acción autónoma sin aprobación) fuera de alcance, escrito.",
   "Criterios preliminares para el ejecutor y la interfaz de aprobación.",
 ],
 "listo": "Cuando hay una decisión escrita sobre una acción concreta, con su autoridad y sus límites.",
 "claude": """Evaluemos una primera acción asistida, sin construir todavía.

1. Proponeme tres candidatas a acción N2 de bajo impacto en el contexto de SUDBAU. Para cada una: qué recurso toca, con qué parámetros, qué efecto exacto produce, si es reversible y cómo, y a quién afecta si sale mal. Ordenalas de menor a mayor riesgo. Después esperá mi elección.
2. Con la elegida, escribí `docs/SDB-037/ficha-n2.md`:
   - Descripción exacta de la acción: no "actualizar el estado", sino "cambiar el estado de la OT X de A a B".
   - Beneficio esperado, con una estimación de cuántas veces por mes ocurre y cuánto tiempo ahorra.
   - Riesgos: qué pasa si se ejecuta con parámetros equivocados, si se ejecuta dos veces, si se ejecuta sobre el recurso equivocado.
   - Quién tiene autoridad para aprobarla y por cuánto tiempo vale esa aprobación.
   - Qué la invalida: cambio de parámetros, cambio de versión del recurso, cambio de permisos.
3. Dejá escrito que N3 no está habilitado por esta historia y qué haría falta para siquiera considerarlo.
4. Esbozá los criterios que después van a guiar SDB-038 (ejecutor) y SDB-039 (interfaz de aprobación).

Si tu conclusión honesta es que ninguna acción justifica el riesgo todavía, decímelo. Es una respuesta perfectamente válida para esta tarea.""",
 "codex": """Generar la evaluación de una acción N2 del piloto SUDBAU en `docs/SDB-037/`.

- `candidatas-n2.md`: tres acciones candidatas con `{ recurso, parametros, efecto_exacto, reversible, impacto_si_falla }`, ordenadas por riesgo.
- `ficha-n2.md`: para la acción seleccionada, descripción exacta, frecuencia estimada, beneficio, riesgos (parámetros erróneos, doble ejecución, recurso equivocado), autoridad de aprobación, vigencia de la aprobación y condiciones de invalidación.
- `limites.md`: N3 explícitamente fuera de alcance y qué requisitos habría que cumplir para considerarlo.
- `criterios-ejecutor-interfaz.md`: criterios preliminares para SDB-038 y SDB-039.

Sin implementación de código en este cambio. La selección de la acción queda en `PENDIENTE` hasta decisión humana.""",
 "flex": "Esta tarea puede terminar en «todavía no». Sería un buen resultado, no una tarea fallida. Si el equipo ya tiene clarísima cuál es la acción, saltense el paso de las tres candidatas. La vigencia de la aprobación es el detalle que más se olvida y el que más problemas trae. [Ajustar según necesidad]",
},

"SDB-038": {
 "titulo": "El ejecutor: que sólo haga lo aprobado, una sola vez y sólo si sigue valiendo",
 "proposito": "Construir la pieza que efectivamente ejecuta una acción aprobada, con la disciplina puesta en el código: sólo la herramienta permitida, revalidación en el momento de ejecutar, idempotencia y un freno que funcione.",
 "entregables": [
   "Contrato del ejecutor: herramienta permitida, identidad, recurso, parámetros, versión y clave de idempotencia.",
   "Revalidación de permisos y de versión en el momento de ejecutar, no sólo al aprobar.",
   "Aprobación expirada no ejecuta. Probado.",
   "Suspensión que impide nuevos efectos, incluso con aprobaciones vigentes.",
   "Pruebas de repetición, expiración y suspensión, sin efectos fuera del contrato.",
 ],
 "listo": "Cuando una aprobación de ayer, sobre un recurso que cambió hoy, no ejecuta nada.",
 "claude": """Implementemos el ejecutor de acciones N2. Acá la disciplina va en el código, no en el procedimiento.

1. Definí el contrato en `docs/SDB-038/contrato-ejecutor.md`: `{ herramienta, identidad_solicitante, recurso, recurso_version, parametros, aprobacion_id, vigencia, idempotency_key }`. Sólo se acepta una herramienta de una lista blanca explícita.
2. Implementá, con estas reglas duras:
   - **Revalidación al ejecutar**: los permisos y la versión del recurso se verifican en el momento de la ejecución, no en el de la aprobación. Si el recurso cambió desde que se aprobó, no se ejecuta.
   - **Vigencia**: una aprobación vencida no ejecuta, y el rechazo queda auditado.
   - **Idempotencia**: la misma `idempotency_key` no produce dos efectos. La segunda vez devuelve el resultado de la primera.
   - **Suspensión**: un interruptor del lado del servidor impide cualquier efecto nuevo, aunque haya aprobaciones vigentes.
   - Auditoría completa: qué se pidió, qué se aprobó, qué se ejecutó y qué devolvió el sistema externo.
3. Probá con casos explícitos: repetición del mismo pedido; aprobación expirada; permiso retirado entre la aprobación y la ejecución; versión del recurso cambiada; suspensión activa; error del sistema externo a mitad de la ejecución.
4. Verificá que no exista ninguna ruta de código que produzca un efecto fuera del contrato. Contame cómo lo verificaste.

Si en algún momento el diseño te obliga a confiar en que la aprobación previa sigue siendo válida, eso es un defecto de diseño: decímelo en vez de resolverlo con un comentario.""",
 "codex": """Implementar el ejecutor de acciones N2 del piloto SUDBAU.

Contrato: `{ herramienta, identidad_solicitante, recurso, recurso_version, parametros, aprobacion_id, vigencia, idempotency_key }`. Lista blanca explícita de herramientas.

Reglas obligatorias:
- Revalidación de permisos y `recurso_version` en el momento de la ejecución; discrepancia → rechazo auditado.
- Aprobación fuera de vigencia → rechazo auditado, sin efecto.
- Idempotencia por `idempotency_key`: segunda invocación devuelve el resultado original sin repetir el efecto externo.
- Interruptor de suspensión consultado en servidor antes de cualquier efecto.
- Auditoría de solicitud, aprobación, ejecución y respuesta externa.

Tests: doble envío; aprobación expirada; permiso retirado entre aprobación y ejecución; `recurso_version` cambiada; suspensión activa; fallo del sistema externo a mitad de la ejecución (sin efecto parcial no registrado).

Entregá diff, salida real de tests y la lista blanca de herramientas con su esquema.""",
 "flex": "Si la acción elegida es trivialmente reversible, parte de esta maquinaria puede parecer excesiva. Mi consejo: construyan igual la revalidación al ejecutar y la idempotencia; el resto pueden simplificarlo. Son las dos que evitan los incidentes que después cuestan explicar. [Ajustar según necesidad]",
},

"SDB-039": {
 "titulo": "La pantalla donde se aprueba: que se vea exactamente qué se está autorizando",
 "proposito": "Que la persona que aprueba vea el recurso concreto, los parámetros exactos, el impacto y hasta cuándo vale su aprobación. Y que cualquier cambio invalide lo aprobado antes.",
 "entregables": [
   "Interfaz de confirmación que muestra recurso, parámetros, impacto y vencimiento.",
   "Aprobación vinculada a la versión exacta del recurso y a la identidad habilitada.",
   "Invalidación automática ante cambios relevantes.",
   "Registro de lo aprobado y de lo efectivamente ejecutado, comparables.",
   "Pruebas de parámetros modificados, expiración y falta de permiso.",
 ],
 "listo": "Cuando quien aprueba puede explicar, con la pantalla a la vista, exactamente qué va a pasar.",
 "claude": """Construyamos la interfaz de aprobación de acciones.

1. Diseñá la pantalla de confirmación mostrando, sin tecnicismos y sin ambigüedad:
   - Qué recurso concreto se va a tocar (con su identificador legible, no un UUID).
   - Los parámetros exactos, en lenguaje entendible.
   - El efecto esperado y si es reversible.
   - Hasta cuándo vale esta aprobación.
   Nada de "¿Confirmar acción?" sin decir cuál.
2. Implementá el vínculo de la aprobación con: la versión exacta del recurso, la identidad del aprobador y su habilitación. Guardá los tres.
3. Implementá la invalidación: si cambian los parámetros, la versión del recurso o los permisos del aprobador, la aprobación anterior deja de valer y hay que aprobar de nuevo. La pantalla tiene que explicar por qué se invalidó.
4. Mostrá, después de la ejecución, la comparación entre lo aprobado y lo efectivamente ejecutado. Si difieren en algo, es un incidente.
5. Probá: parámetros modificados después de aprobar; aprobación expirada; usuario sin permiso de aprobación.

La prueba de fuego de esta pantalla: que quien aprueba pueda explicarle a otra persona qué va a pasar, leyendo sólo lo que ve.""",
 "codex": """Implementar la interfaz de aprobación de acciones N2 del piloto SUDBAU.

Requisitos de la confirmación: identificador legible del recurso, parámetros en lenguaje natural, efecto esperado, reversibilidad y vencimiento de la aprobación. Prohibido un diálogo genérico sin detalle de la acción.

Modelo: `aprobacion { aprobacion_id, accion, recurso, recurso_version, parametros_hash, aprobador, vigencia_hasta, estado ∈ {vigente, invalidada, consumida} }`.

Reglas:
- Cambio de `parametros_hash`, de `recurso_version` o de los permisos del aprobador → `invalidada`, con motivo mostrado en la UI.
- Tras la ejecución, vista comparativa entre lo aprobado y lo ejecutado.

Tests: parámetros modificados tras aprobar → invalidación; aprobación expirada → no ejecutable; usuario sin permiso → no puede aprobar; comparación aprobado vs. ejecutado detecta divergencia.

Entregá diff y salida real de tests.""",
 "flex": "Si la acción es muy simple, la pantalla puede ser un diálogo de tres líneas — lo que importa es que esas tres líneas digan el recurso y los parámetros reales. La vista comparativa de aprobado vs. ejecutado es opcional al principio, pero es lo que da tranquilidad cuando el volumen crece. [Ajustar según necesidad]",
},

"SDB-040": {
 "titulo": "Romper la acción N2 a propósito antes de confiar en ella",
 "proposito": "El cierre de la etapa de agentes: probar los escenarios feos (doble envío, cambio concurrente, permiso retirado, error externo) y ensayar la reversión. Recién con esto se puede decidir si N2 se queda.",
 "entregables": [
   "Casos preparados: doble envío, cambio concurrente, permiso retirado y error del sistema externo.",
   "Ejecución en entorno controlado, con los efectos reales cotejados contra lo solicitado y lo aprobado.",
   "Prueba de reversión o compensación, con evidencia.",
   "Verificación de ausencia de doble efecto en todos los casos.",
   "Informe con fallos, límites conocidos y recomendación sobre continuar con N2.",
 ],
 "listo": "Cuando intentaste romperlo de cuatro formas distintas y podés mostrar qué pasó en cada una.",
 "claude": """Probemos la acción N2 con intención de romperla.

1. Preparate los cuatro escenarios en `docs/SDB-040/casos.md`, cada uno con su resultado esperado definido antes de ejecutar:
   - **Doble envío**: el mismo pedido aprobado se ejecuta dos veces, casi simultáneamente.
   - **Cambio concurrente**: el recurso cambia entre la aprobación y la ejecución.
   - **Permiso retirado**: el aprobador pierde su habilitación después de aprobar y antes de que se ejecute.
   - **Error externo**: el sistema destino falla a mitad de la operación, o responde con un error ambiguo (no se sabe si aplicó o no). Este es el peor y el más realista.
2. Ejecutá los casos en un entorno controlado y cotejá, en cada uno, tres cosas: lo que se solicitó, lo que se aprobó y el efecto real que quedó en el sistema destino. Las tres tienen que coincidir o el caso falla.
3. Ensayá la reversión o compensación: deshacer el efecto de una acción ejecutada. Documentá cuánto tarda y qué queda como rastro.
4. Escribí `docs/SDB-040/informe-n2.md` con: resultados por caso, fallos encontrados, límites conocidos, y una recomendación explícita sobre si N2 se mantiene, se mantiene con restricciones o se suspende.

El caso del error ambiguo del sistema externo es el que separa un ejecutor serio de uno optimista. Dedicale tiempo y contame cómo lo resolviste.""",
 "codex": """Ejecutar y documentar la prueba adversarial de la acción N2 del piloto SUDBAU.

Casos, con resultado esperado declarado previamente:
1. Doble envío concurrente del mismo pedido aprobado → un solo efecto.
2. Cambio del recurso entre aprobación y ejecución → rechazo, sin efecto.
3. Permiso del aprobador retirado tras aprobar → rechazo, sin efecto.
4. Error del sistema externo a mitad de la operación, incluida una respuesta ambigua → estado resuelto sin doble efecto y sin efecto silencioso.

Por cada caso, cotejar solicitado vs. aprobado vs. efecto real observado en el destino.

Además: prueba de reversión o compensación de una acción ya ejecutada, con medición de tiempo y rastro resultante.

Entregables: suite en `tests/n2/`, salida real de ejecución, y `docs/SDB-040/informe-n2.md` con fallos, límites y recomendación (mantener / mantener con restricciones / suspender).""",
 "flex": "Si el sistema externo no tiene un entorno de prueba, esta tarea se hace con un doble controlado y hay que decirlo en el informe: probado contra doble, no contra el sistema real. Es honesto y sigue siendo útil. El caso de la respuesta ambigua es el que yo no dejaría afuera en ninguna variante. [Ajustar según necesidad]",
},

}
