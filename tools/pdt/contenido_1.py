# -*- coding: utf-8 -*-
"""Contenido redactado del PDT — bloque 1 (SDB-001 a SDB-012, incluye SDB-003.1)."""

BLOQUE_1 = {

"SDB-001": {
 "titulo": "Ponernos de acuerdo: a dónde vamos, cuánto tiempo tenemos y con qué OT arrancamos",
 "proposito": "Antes de escribir una línea de código necesitamos tres cosas claras: qué queremos mostrar al final del sprint, cuántas horas reales tiene cada uno, y una orden de trabajo concreta que nos sirva de hilo conductor. Sin esto, todo lo demás se discute en abstracto y no termina nunca.",
 "entregables": [
   "Ficha de la OT de referencia: identificador, cliente, pozo, período, sistema de origen y quién es el dueño funcional que puede decir «esto está bien».",
   "Matriz de disponibilidad de los cuatro, en horas por semana, escrita y confirmada por cada uno (no estimada por otro).",
   "Acuerdo de S1 en una página: meta demostrable, qué queda explícitamente afuera, y la lista de tarjetas que entran en la capacidad acordada.",
   "Registro separado de lo confirmado y lo que todavía está pendiente de respuesta.",
 ],
 "listo": "Cuando los cuatro pueden decir de memoria cuál es la meta de S1 y cuál es la OT que vamos a seguir de punta a punta.",
 "claude": """Ayudame a preparar y documentar el acuerdo de arranque del piloto.

Lo que necesito de vos, en este orden:

1. Explorá el repositorio y decime qué hay realmente disponible hoy sobre la OT de referencia: archivos, muestras, exportaciones de Field, documentación previa. No supongas que existe algo que no puedas abrir.
2. Proponeme una plantilla de "Ficha de OT de referencia" en Markdown con estos campos: ID_OT, cliente, ID_Pozo, período, sistema de origen, ruta del archivo o endpoint, dueño funcional, y una columna de estado por campo (confirmado / pendiente / no disponible).
3. Proponeme una plantilla de matriz de disponibilidad para cuatro personas (Luis Fernando, Irma, Cata, María) con horas por semana y una nota de "confirmado por la persona: sí/no".
4. Redactá un borrador de acuerdo de S1 de una página con: meta demostrable en una frase, alcance incluido, alcance excluido, y una tabla de tarjetas candidatas con esfuerzo estimado.

Reglas que no quiero que rompas:
- Todo lo que yo no te haya confirmado va marcado como PENDIENTE DE CONFIRMACIÓN. No lo completes con un valor plausible.
- No inventes nombres de archivos, IDs de OT ni pozos.
- Entregame los archivos creados con su ruta, y al final un resumen de qué preguntas me quedan por responder para cerrar la tarea.""",
 "codex": """Generá los tres documentos de arranque del piloto SUDBAU en el repositorio, en `docs/SDB-001/`.

Archivos a crear:
- `ficha-ot-referencia.md` — tabla con campos ID_OT, cliente, ID_Pozo, período, sistema de origen, ruta o endpoint, dueño funcional, y estado por campo (confirmado / pendiente / no disponible). Dejá los valores vacíos con el literal `PENDIENTE`.
- `disponibilidad-s1.md` — matriz de 4 personas × horas semanales, con columna "confirmado por la persona".
- `acuerdo-s1.md` — meta demostrable, alcance incluido, alcance excluido, tabla de tarjetas candidatas.

Restricciones:
- No completes ningún dato de negocio que no esté en el repositorio; usá `PENDIENTE` y listalo al final.
- Una sola entrega, con el diff completo y una descripción de PR que explique qué decisiones quedan abiertas.
- No toques `index.html` ni `tablero_scrumban.html`.""",
 "flex": "Si el equipo ya tiene la OT elegida y la disponibilidad hablada, saltate las plantillas y usá el prompt sólo para redactar el acuerdo de S1. Si les resulta más natural acordar esto en una llamada de 40 minutos y escribir tres párrafos después, háganlo así: esta tarea existe para que el acuerdo quede escrito, no para que exista un documento bonito. [Ajustar según necesidad]",
},

"SDB-002": {
 "titulo": "Mirar qué ya tenemos hecho de Field y armar una muestra que podamos usar sin miedo",
 "proposito": "Muy probablemente ya hay código que extrae datos de Field y del reloj de asistencia. Antes de escribir otro extractor, lo inventariamos. Y necesitamos una muestra chica, autorizada y sin datos sensibles de más para poder trabajar tranquilos.",
 "entregables": [
   "Inventario de extractores existentes: qué hace cada uno, dónde vive, en qué lenguaje, qué formato devuelve, última vez que corrió.",
   "Muestra mínima autorizada de Field y del reloj, guardada con su archivo original intacto.",
   "Manifiesto de procedencia: fuente, fecha de corte, cantidad de registros y hash SHA-256 calculado sobre el archivo real.",
   "Diccionario de campos de la muestra, con tipo, ejemplo y si el campo puede venir vacío.",
   "Confirmación explícita de que no hay credenciales ni datos personales innecesarios en lo que quedó versionado.",
 ],
 "listo": "Cuando cualquiera del equipo puede clonar el repo, correr el extractor sobre la muestra y obtener el mismo resultado.",
 "claude": """Necesito inventariar lo que ya tenemos y preparar una muestra de trabajo segura.

Paso 1 — Inventario. Recorré el repositorio y cualquier carpeta que te indique, y armá `docs/SDB-002/inventario-extractores.md` con una fila por extractor: nombre, ruta, lenguaje, fuente (Field / CrossChex / otro), formato de salida, dependencias, y si pudiste ejecutarlo o no. Marcá claramente lo que NO pudiste verificar.

Paso 2 — Muestra. Proponeme un procedimiento reproducible para generar una muestra mínima: qué registros incluir, cómo anonimizar o reducir campos personales, y dónde guardarla. Escribí el script en `tools/sdb-002/make_sample.py` y que además emita `manifest.json` con: fuente, fecha de corte, cantidad de registros, lista de campos y hash SHA-256 del archivo de muestra real.

Paso 3 — Diccionario. Generá `docs/SDB-002/diccionario-campos.md` a partir de la muestra real, no de lo que suponés que trae Field: tipo inferido, ejemplo, porcentaje de vacíos.

Paso 4 — Higiene. Revisá que no quede ningún secreto ni token en lo que se versiona, y decime exactamente qué buscaste y cómo.

Importante: si no tenés acceso a datos reales, generá la muestra como sintética y etiquetala como SINTÉTICA en el manifiesto y en el nombre del archivo. No la presentes como dato de producción.""",
 "codex": """Escribí `tools/sdb-002/make_sample.py` para el repositorio SUDBAU.

Comportamiento:
- Entrada: ruta a una exportación de Field (CSV o JSON) y ruta a una exportación del reloj de asistencia.
- Salida: muestra reducida en `data/samples/`, más `manifest.json` con `source`, `cutoff_date`, `record_count`, `fields[]` y `sha256` calculado sobre el archivo de muestra realmente escrito.
- Parámetros: `--limit`, `--drop-fields` (lista de campos personales a excluir), `--synthetic` (genera datos ficticios con el mismo esquema y marca `"synthetic": true` en el manifiesto).
- El script debe fallar con un mensaje claro si el archivo de entrada no existe. No inventes un esquema por defecto.

Además, generá `tests/test_make_sample.py` con al menos: hash reproducible sobre la misma entrada, exclusión efectiva de campos, y modo sintético marcado en el manifiesto.

Entregá el diff y el resultado real de correr los tests.""",
 "flex": "Si el inventario da cero extractores reutilizables, esta tarea se achica muchísimo y conviene decirlo en voz alta en vez de forzar un documento. El hash y el manifiesto sí los mantendría siempre: son baratos y nos salvan discusiones de «¿esta muestra de cuándo era?». El paso de anonimización dependerá de qué permita Administración. [Ajustar según necesidad]",
},

"SDB-003": {
 "titulo": "Dejar el repositorio y el tablero de GitHub listos para trabajar los cuatro",
 "proposito": "Que nadie se quede afuera por un permiso, y que el lugar donde vive el código esté claramente separado del sitio público de planificación. Suena aburrido; es lo que evita el caos en la semana tres.",
 "entregables": [
   "Referencia del repositorio institucional privado: URL, quién lo administra y para qué sirve.",
   "Matriz de acceso comprobada: los cuatro entran, con el nivel que corresponde. Comprobada entrando, no asumida.",
   "Campos del proyecto de GitHub creados: responsable, sprint, fase, tipo de entrega.",
   "Convenciones escritas de ramas, revisión y dónde se guarda la evidencia.",
   "Lista de protecciones que el plan contratado permite y cuáles no, con la restricción documentada.",
 ],
 "listo": "Cuando los cuatro confirman por escrito que entraron y vieron el tablero, y sabemos qué protecciones podemos y no podemos activar.",
 "claude": """Ayudame a dejar documentado y verificado el entorno de trabajo en GitHub.

1. Revisá el repositorio actual y decime qué hay: ramas existentes, archivos en la raíz, si hay `AGENTS.md`, `CLAUDE.md`, `README.md`, `.github/`. Si falta alguno de los primeros tres, proponé un borrador.
2. Escribí `CONTRIBUTING.md` con nuestras convenciones: nombres de rama (`sdb-<id>/<descripcion-corta>`), qué lleva un commit, quién revisa qué, y dónde se guarda la evidencia de cada tarea.
3. Escribí `docs/SDB-003/acceso-y-protecciones.md` con: tabla de acceso por persona (dejá el resultado en PENDIENTE hasta que alguien lo verifique entrando), campos del proyecto a crear, y una sección sobre qué protecciones de rama permite el plan contratado.
4. Dejá muy explícita la separación entre el repositorio privado de código y el sitio público de planificación (GitHub Pages). Escribí qué NO puede publicarse en el sitio público.

No afirmes que un permiso está configurado si no lo viste. Si no podés verificar algo desde acá, escribilo como comprobación manual pendiente y decime el paso exacto que tengo que hacer yo.""",
 "codex": """Creá la documentación base del repositorio SUDBAU SDB-EST-CLOUD-001.

Archivos:
- `CONTRIBUTING.md`: convención de ramas `sdb-<id>/<slug>`, formato de commit, política de revisión cruzada, ubicación de evidencia por tarea.
- `docs/SDB-003/acceso-y-protecciones.md`: tabla de acceso por persona con estado `PENDIENTE`, campos del proyecto (responsable, sprint, fase, tipo), y una sección que distinga el repositorio privado del sitio público de GitHub Pages.
- `.github/PULL_REQUEST_TEMPLATE.md`: checklist corto con ID SDB, ambiente probado, evidencia, y revisor.

Restricciones: no modifiques `index.html` ni `tablero_scrumban.html`. No declares configuraciones de GitHub como aplicadas; son documentación de lo que hay que aplicar a mano.""",
 "flex": "Si el repo institucional todavía no existe y están trabajando sobre el personal, no bloqueen el sprint por eso: documenten la restricción y sigan. Lo único que no conviene saltarse es la separación entre lo privado y lo publicado en Pages. La plantilla de PR es opcional si les resulta burocrática. [Ajustar según necesidad]",
},

"SDB-003.1": {
 "titulo": "Arreglar el tablero: en qué estado está el trabajo NO es lo mismo que en qué ambiente está entregado",
 "proposito": "Hoy el tablero mezcla dos cosas distintas: cómo viene una tarea y dónde quedó publicado su resultado. Eso obliga a inventar un PROD que no existe para poder cerrar una tarjeta. Lo separamos, sin perder nada de lo que ya cargamos.",
 "entregables": [
   "Respaldo del JSON y del HTML vigentes, guardado antes de tocar nada.",
   "Contrato de datos nuevo, versionado, con campos separados: estado del trabajo, ambiente de entrega, resultado aceptado, versión y evidencia.",
   "Copia nueva del tablero migrada sin pérdida: IDs, notas, evidencias, revisores, bloqueos e historial intactos.",
   "Las siete columnas conservadas y los tipos de tarea conservados (una tarea de software no se convierte en documento).",
   "Evidencia de regresión: exportación/importación, dependencias, documentos, TEST, PROD, WIP y respaldo probados.",
 ],
 "listo": "Cuando una tarea de software puede cerrarse con su resultado aceptado en TEST, sin que nadie tenga que mentirle al tablero.",
 "claude": """Esta es una migración delicada. Trabajá con cuidado y con respaldo.

Contexto real del repositorio: `tablero_scrumban.html` contiene el tablero, con su estado en un `<script id="seed" type="application/json">` y persistencia en localStorage bajo la clave `sudbau-scrumban-v1-<copyId>`. `index.html` es el checklist, con su propio `<script id="guide-data">` y su clave `sudbau_checklist_v2`. Confirmá esto leyendo los archivos antes de proponer nada.

Lo que necesito:

1. Primero, un script `tools/sdb-003-1/backup.md` (o instrucciones claras) para que exportemos el JSON y el HTML vigentes antes de cualquier cambio. Nada se toca antes de esto.
2. Proponeme el contrato nuevo `schema: 2` del tablero, separando explícitamente:
   - `status`: dónde está el trabajo (las siete columnas actuales se conservan).
   - `delivery`: `{ environment, acceptedResult, version, evidence }` — dónde quedó entregado el resultado y con qué evidencia.
   Una dependencia debe poder darse por satisfecha por su resultado aceptado en el ambiente requerido, sin exigir PROD.
3. Escribí la función de migración `schema 1 → schema 2` que conserve IDs, notas, bloqueos, revisores, evidencias, historial y tipo de tarea. Ninguna tarea de software puede quedar convertida en documento.
4. Aplicá el cambio en una copia nueva del archivo, no sobre el original.
5. Definí y ejecutá las pruebas de regresión: exportar/importar, dependencias satisfechas en TEST, cierre de documento, cierre de software en TEST, límite de WIP, recuperación desde respaldo, y qué pasa al reabrir una tarea (debe invalidar las validaciones afectadas).

Reglas: no deduzcas el ambiente real desde una casilla marcada. Una casilla es una declaración, no un despliegue. Decime al final qué probaste de verdad y qué quedó sin probar.""",
 "codex": """Migración del esquema del tablero Scrumban de SUDBAU, en una copia nueva del archivo.

Entrada: `tablero_scrumban.html`, con estado en `<script id="seed" type="application/json">` (schema 1) y persistencia en localStorage.

Tarea:
1. Definir `schema: 2` separando `status` (columna de trabajo) de `delivery: { environment, acceptedResult, version, evidence }`.
2. Implementar `migrate(v1) -> v2` preservando `id`, `notes`, `blocker`, `blockedFrom`, `reviewer`, `evidence`, `trail`, `kind`, `dependencies`.
3. La resolución de dependencias debe aceptar el resultado aceptado en el ambiente requerido; no debe exigir `status === 'done'` en PROD.
4. Escribir la salida en `tablero_scrumban_v2.html`. No sobrescribas el archivo original en este cambio.
5. Agregar `tests/` con casos: migración sin pérdida de campos, cierre de tarea `kind: delivery` aceptada en TEST, cierre de `kind: document`, invalidación de validaciones al reabrir, export→import idempotente, tope de WIP.

Entregá el diff, la salida real de los tests y una lista explícita de los campos que la migración toca.""",
 "flex": "Esta es la tarea donde más vale discutir antes de codear. Si al equipo le parece que `delivery` debería ser una lista (una tarea puede estar aceptada en TEST y después en PROD), cámbienlo: es una mejora, no una desviación. Lo que sí pediría no negociar es el respaldo previo y la prueba de reapertura. El nombre de los campos es totalmente suyo. [Ajustar según necesidad]",
},

"SDB-004": {
 "titulo": "Levantar un TEST de verdad, con acceso controlado y sin miedo a romper nada",
 "proposito": "Necesitamos un lugar donde probar cosas que no sea la máquina de nadie ni producción. Y antes de provisionar, cerrar de una vez la pregunta de plataforma: el tablero dice Cloudflare Workers + D1/R2, el Blueprint propone GCP. No se decide con el mouse en la consola.",
 "entregables": [
   "Decisión de plataforma escrita y fechada, con quién la tomó y qué queda fuera de alcance.",
   "Entorno TEST desplegado y separado: recursos, identidades y secretos propios, distintos de producción.",
   "Secretos fuera del repositorio, con el mecanismo de inyección documentado.",
   "Procedimiento de despliegue reproducible: alguien que no lo escribió puede ejecutarlo.",
   "Prueba de acceso: un usuario habilitado entra, uno no habilitado recibe denegación. Con evidencia de ambas.",
   "URL de prueba, versión desplegada y fecha registradas.",
 ],
 "listo": "Cuando otro integrante despliega TEST siguiendo el procedimiento y obtiene la misma URL funcionando.",
 "claude": """Antes de provisionar nada, necesito que resuelvas una contradicción documentada.

Paso 0 — Decisión de plataforma. El tablero y el checklist de este repositorio asumen Cloudflare Workers + D1 + R2. El Blueprint GCP v3 propone Google Cloud. No son equivalentes. Leé lo que haya en el repositorio sobre ambos, armá `docs/SDB-004/decision-plataforma.md` con: qué dice cada fuente (citando archivo y sección), qué implica cada opción para este piloto en costo, runtime y tiempo de puesta en marcha, y una recomendación tuya con fundamento. Dejá el campo "decidido por" y "fecha" en PENDIENTE hasta que yo lo confirme.

Paso 1 — Sólo cuando la decisión esté tomada, preparás TEST sobre la plataforma acordada:
- Configuración de recursos separados de producción, con nombres que hagan obvio el ambiente.
- Manejo de secretos fuera del repositorio. Documentá el mecanismo concreto, no "usar variables de entorno" en abstracto.
- Script o comando de despliegue reproducible, en `tools/deploy/`.

Paso 2 — Pruebas de acceso: un caso con usuario habilitado y uno con usuario no habilitado. Quiero ver la respuesta real de cada uno, no una afirmación.

Paso 3 — Registro: URL de TEST, versión, fecha, y una nota explícita de que TEST no tiene permiso de escritura hacia producción.

No ejecutes comandos que creen recursos facturables sin avisarme primero qué vas a crear y qué costo aproximado tiene.""",
 "codex": """Preparar el entorno TEST del piloto SUDBAU sobre la plataforma ya decidida en `docs/SDB-004/decision-plataforma.md`. Si ese archivo no existe o no tiene decisión tomada, detenete y reportalo en vez de elegir por tu cuenta.

Entregables de código:
- Configuración de despliegue del entorno TEST con recursos nombrados con sufijo `-test`.
- `tools/deploy/deploy-test.sh` idempotente, que falle con mensaje claro si falta una variable requerida.
- `docs/SDB-004/runbook-test.md`: pasos para desplegar, para verificar y para revertir.
- Un test de acceso automatizado: usuario habilitado → 200; usuario no habilitado → 403. Sin credenciales embebidas en el repo.

No crees recursos en la nube desde este entorno. Entregá la configuración, los scripts y el diff; la ejecución real la hace el equipo con sus credenciales.""",
 "flex": "Si la decisión de plataforma ya está cerrada por escrito en otro lado, saltate el paso 0 y linkéalo. Si el equipo prefiere arrancar TEST con algo más simple (un único Worker con D1, sin R2) y crecer después, es una decisión razonable: anótenla como alcance reducido, no como deuda. La prueba de acceso denegado es la que yo no dejaría afuera. [Ajustar según necesidad]",
},

"SDB-005": {
 "titulo": "Convertir una OT real en datos limpios, sin perder nunca el original",
 "proposito": "Este es el corazón del piloto. Tomamos una OT como viene de Field y la dejamos en una forma estable, con identificadores confiables, siempre unida a su original. Si después alguien pregunta «¿de dónde salió este número?», tiene que haber respuesta.",
 "entregables": [
   "Contrato de OT escrito: ID_OT, ID_Persona, fechas con zona horaria explícita, fuente, y vínculo al archivo original.",
   "Normalizador implementado, que escribe el derivado con número de versión de reglas.",
   "Regla clara y probada que distingue dato ausente de cero.",
   "Bandeja de excepciones: IDs no conciliados y correcciones aisladas, no silenciadas.",
   "Prueba de reproceso: correr dos veces la misma muestra no duplica registros.",
   "Nota explícita: las horas normalizadas no son liquidación salarial.",
 ],
 "listo": "Cuando reprocesás la muestra dos veces y una corrección tardía, y el resultado sigue siendo correcto y rastreable al original.",
 "claude": """Construyamos el normalizador de OT. Es la pieza de la que dependen casi todas las tarjetas que siguen, así que vale hacerla bien.

1. Leé la muestra y el diccionario de campos generados en SDB-002. Si no existen, decímelo y frená.
2. Escribí `docs/SDB-005/contrato-ot.md` con el esquema del derivado: `ID_OT`, `ID_Persona`, `fecha_inicio`, `fecha_fin`, `timezone`, `fuente`, `archivo_original`, `version_reglas`, y el criterio explícito para distinguir `null` (ausente) de `0` (cero real). Usá `ID_Persona` en los intercambios técnicos; el CUIL queda restringido a los entornos autorizados.
3. Implementá el normalizador en `src/normalizers/ot.py` (o el lenguaje que ya use el repo — revisalo antes de elegir):
   - Nunca modifica el original; lo referencia.
   - Escribe el derivado con `version_reglas` y `procesado_en` (UTC + zona operativa America/Argentina/Buenos_Aires).
   - Es idempotente: reprocesar la misma entrada no duplica ni altera lo ya escrito.
   - Los IDs que no concilian van a una bandeja de excepciones, no se descartan.
4. Escribí tests reales en `tests/test_ot_normalizer.py`: reproceso idempotente, corrección tardía de un registro ya normalizado, campo ausente vs. cero, ID huérfano.
5. Corré los tests y mostrame la salida real.

Límite duro: no calcules ni insinúes liquidación salarial. Las horas acá son horas trabajadas registradas, nada más. Dejalo escrito en el módulo.""",
 "codex": """Implementar el normalizador de órdenes de trabajo del piloto SUDBAU.

Entrada: muestra de Field en `data/samples/` con su `manifest.json`.
Salida: registros derivados con esquema `{ ID_OT, ID_Persona, fecha_inicio, fecha_fin, timezone, fuente, archivo_original, version_reglas, procesado_en }`.

Requisitos:
- Idempotencia por clave natural `(ID_OT, ID_Persona, fecha_inicio)`; un segundo run sobre la misma entrada no debe producir filas nuevas.
- Distinguir ausente (`null`) de cero (`0`) en todos los campos numéricos.
- Registros cuyo `ID_Persona` o `ID_OT` no concilie contra maestros van a una tabla/archivo de excepciones con el motivo.
- Zona horaria operativa `America/Argentina/Buenos_Aires`, timestamps técnicos en UTC.
- Prohibido derivar importes salariales.

Tests obligatorios: doble ejecución idempotente, corrección tardía, null vs cero, excepción por ID huérfano.

Entregá el diff, la salida de los tests y la lista de supuestos que tuviste que hacer sobre el esquema de entrada.""",
 "flex": "El lenguaje y la ubicación de los archivos los define el equipo según lo que ya exista: no adopten Python porque el prompt lo mencione. La clave natural para idempotencia es una hipótesis mía; si la realidad de Field es otra (por ejemplo, un ID de parte propio), cámbienla y anoten por qué. La bandeja de excepciones puede ser una tabla, un CSV o un log estructurado. [Ajustar según necesidad]",
},

"SDB-006": {
 "titulo": "Primera pantalla: ver una OT completa y poder creerle",
 "proposito": "Es el primer momento en que el piloto se vuelve visible. Una pantalla en TEST que muestre la OT, quiénes trabajaron, los intervalos y lo que falta — diciendo siempre de dónde salió cada cosa.",
 "entregables": [
   "Contrato de datos del resumen de OT, acordado con quien va a construir el backend.",
   "Vista desplegada en TEST que muestra OT, personas, intervalos y pendientes.",
   "En pantalla: fuente, fecha de corte y cobertura. Sin eso, un número es una opinión.",
   "Declaración escrita de si la entrada es muestra, archivo o API real.",
   "Cotejo de la pantalla contra la consulta y contra el original, documentado.",
   "Ninguna cifra de costo total mostrada mientras la cobertura sea incompleta.",
 ],
 "listo": "Cuando alguien que no construyó la pantalla mira un número, hace clic y llega al dato original.",
 "claude": """Construyamos la primera vista del piloto: el resumen de una OT.

1. Revisá el derivado de SDB-005 y acordá conmigo el contrato de la pantalla. Escribilo en `docs/SDB-006/contrato-resumen-ot.md`: request, response, tipos, y qué significa cada campo. Incluí siempre `fuente`, `fecha_corte` y `cobertura`.
2. Implementá el endpoint y la vista en TEST. Requisitos de producto, no negociables:
   - Se ve la OT, las personas, los intervalos y lo que está pendiente.
   - "Sin dato" y "cero" se muestran distinto y se leen distinto.
   - La pantalla declara si está mirando una muestra, un archivo o una API real.
   - No se muestra un costo total si la cobertura no está completa: en su lugar, "cobertura parcial: N de M".
3. Hacé el cotejo: misma OT por pantalla, por consulta directa y contra el archivo original. Documentá los tres resultados en `docs/SDB-006/cotejo.md`.
4. Probá el caso de datos ausentes y el de período incompleto.

Pensala para un teléfono en el campo, no para un monitor de escritorio: pocos elementos, tipografía grande, y que se entienda con conexión mala.""",
 "codex": """Implementar el endpoint y la vista de "resumen de OT" del piloto SUDBAU, en el entorno TEST.

Backend: endpoint que reciba `ID_OT` y devuelva `{ ot, personas[], intervalos[], pendientes[], fuente, fecha_corte, cobertura: { presentes, esperados } }`.

Frontend: vista mobile-first que rinda ese contrato. Reglas:
- `null` se rinde como "sin dato", `0` como "0". Nunca se colapsan.
- Mostrar `fuente` y `fecha_corte` de forma visible, no en un tooltip.
- Si `cobertura.presentes < cobertura.esperados`, no renderizar ningún total de costo; mostrar el estado de cobertura.
- Declarar en la UI si el origen es muestra, archivo o API.

Tests: contrato del endpoint, render con datos ausentes, render con cobertura parcial (verificar que no aparece total).

Entregá diff, tests ejecutados y una captura o descripción del render en ancho de teléfono.""",
 "flex": "El diseño visual es enteramente de Cata: el prompt fija el comportamiento, no la estética. Si en la práctica el equipo necesita ver un total aunque la cobertura sea parcial, propongan una forma honesta de mostrarlo (por ejemplo, total parcial claramente etiquetado) en vez de esconder la regla. El cotejo triple puede parecer exagerado la primera vez; es justamente la primera vez cuando sirve. [Ajustar según necesidad]",
},

"SDB-007": {
 "titulo": "Buscarle las cosquillas: permisos, duplicados y correcciones",
 "proposito": "Probar lo que funciona es fácil. Acá probamos lo que puede salir mal, que es donde se pierde la confianza de un usuario. Y lo hacemos cruzado: cada uno revisa el trabajo del otro.",
 "entregables": [
   "Matriz de casos con resultado esperado: acceso permitido, acceso denegado, registro duplicado, corrección tardía, ID no conciliado.",
   "Ejecución de los casos sobre el normalizador y sobre la UI, en una versión de TEST identificada.",
   "Resultado real por caso, con evidencia y defectos reproducibles.",
   "Revisión cruzada registrada: María revisa las pruebas de UI, Cata revisa las del normalizador.",
   "Lista de correcciones hechas y de pendientes con responsable.",
 ],
 "listo": "Cuando los cinco casos tienen resultado documentado y los defectos encontrados tienen dueño y fecha.",
 "claude": """Armemos la matriz de pruebas de borde del piloto y ejecutémosla.

1. Escribí `docs/SDB-007/matriz-casos.md` con una fila por caso: ID de caso, qué se prueba, precondición, pasos, resultado esperado, componente (normalizador / UI), y quién lo revisa. Los cinco casos mínimos son: acceso permitido, acceso denegado, registro duplicado, corrección posterior de un registro ya procesado, ID no conciliado.
2. Para cada caso, implementá la prueba automatizada donde tenga sentido y describí el procedimiento manual donde no.
3. Ejecutá lo automatizable y traeme la salida real. Para lo manual, dejá el resultado en PENDIENTE con el paso exacto a seguir.
4. Los defectos que encuentres van a `docs/SDB-007/defectos.md`: cómo reproducirlo, qué esperábamos, qué pasó, severidad, y una propuesta de corrección. No los arregles todos de una; primero listámelos.

Advertencia importante: el caso de acceso denegado tiene que probarse contra la verificación del backend. Un filtro de pantalla o un dominio de correo no son autorización. Si encontrás que el permiso se resuelve sólo en el front, eso es un defecto de severidad alta.""",
 "codex": """Escribir la suite de pruebas de borde del piloto SUDBAU.

Casos obligatorios, sobre normalizador y UI:
1. Acceso permitido: usuario habilitado obtiene el recurso.
2. Acceso denegado: usuario no habilitado recibe 403 **desde el backend**, no por ocultamiento en el front.
3. Duplicado: el mismo registro ingresado dos veces produce una sola fila.
4. Corrección tardía: una corrección de un registro ya procesado actualiza el derivado y conserva el valor anterior en el rastro.
5. ID no conciliado: el registro va a excepciones con motivo, sin romper el lote.

Entregá: los tests, su salida real de ejecución, y un archivo `docs/SDB-007/defectos.md` con los fallos encontrados (reproducción, esperado, obtenido, severidad). No corrijas los defectos en este mismo cambio.""",
 "flex": "Cinco casos es el piso, no el techo: si al equipo se le ocurren otros tres que les dan miedo de verdad, esos valen más que los del prompt. Lo que pediría sostener es la revisión cruzada — es barata y encuentra cosas que uno solo no ve — y la verificación de permisos en el backend. [Ajustar según necesidad]",
},

"SDB-008": {
 "titulo": "Mostrarlo funcionando y anotar honestamente qué falta",
 "proposito": "Cerrar el primer sprint con algo demostrable. No una presentación: alguien que no lo construyó abre la pantalla, sigue el caso y el dueño funcional dice si le sirve o no.",
 "entregables": [
   "Guion de demo: qué se muestra, en qué orden, con qué OT y desde qué URL de TEST.",
   "Demo ejecutada por un segundo integrante, no por quien construyó la funcionalidad.",
   "Cotejo en vivo contra la fuente original.",
   "Acta corta: qué aceptó el dueño funcional, qué brechas quedaron, con responsable y próximo paso.",
   "Resultado registrado en TEST. Nada se publica en producción por calendario.",
 ],
 "listo": "Cuando el dueño funcional dijo con sus palabras qué le sirve y qué le falta, y quedó escrito.",
 "claude": """Preparemos la demo de cierre de S1 y su acta.

1. Escribí `docs/SDB-008/guion-demo.md`: duración objetivo 15 minutos, pasos numerados, qué OT se usa, qué URL de TEST, qué se espera ver en cada paso, y en qué momento se abre el archivo original para cotejar. El guion tiene que poder ejecutarlo alguien que no construyó la funcionalidad.
2. Preparame una lista de "cosas que pueden salir mal en la demo" con su plan B (datos que no cargan, acceso que falla, período sin registros).
3. Escribí la plantilla de acta `docs/SDB-008/acta-aceptacion.md`: qué se mostró, quién validó, qué aceptó, qué brechas se registraron, riesgos, responsables y próximo paso por cada brecha.
4. Revisá el estado real de SDB-006 y SDB-007 en el repositorio y decime con franqueza si estamos en condiciones de demostrar. Si falta algo, prefiero saberlo hoy.

No escribas en el acta ninguna aceptación que no haya ocurrido, y no marques la tarea como cerrada: eso lo decide una persona.""",
 "codex": """Generar el paquete de demo del sprint 1 en `docs/SDB-008/`:

- `guion-demo.md`: pasos numerados, OT de referencia, URL de TEST, resultado esperado por paso, y momento de cotejo contra el original.
- `plan-b.md`: fallos probables y alternativa para cada uno.
- `acta-aceptacion.md`: plantilla con campos vacíos marcados `PENDIENTE` (validador, aceptación, brechas, riesgos, responsable, próximo paso).

Además, verificá en el repositorio si existen los artefactos de SDB-006 y SDB-007 y generá `docs/SDB-008/preparacion.md` listando qué está presente y qué falta, sin suponer. No completes resultados de aceptación.""",
 "flex": "Si la demo la quieren hacer con pantalla compartida y sin guion, adelante — pero escriban el acta igual, aunque sean seis líneas. Esa acta es lo que van a mirar dentro de dos meses cuando alguien pregunte qué se aprobó. El plan B es opcional si el equipo ya tiene confianza con el entorno. [Ajustar según necesidad]",
},

"SDB-009": {
 "titulo": "Traer datos de Field de forma incremental, sin perder correcciones ni bajas",
 "proposito": "Dejar de trabajar con una muestra congelada y empezar a traer datos de verdad, de a poco, entendiendo cómo Field maneja páginas, cuotas, estados y registros dados de baja.",
 "entregables": [
   "Verificación real de la API de Field: paginación, cursor o ventana, cuotas, estados posibles y tratamiento de bajas. Verificada, no supuesta.",
   "Conector incremental con corte explícito y esquema etiquetado con versión y fecha.",
   "Contrato de estados: qué significa cada estado de Field en nuestro modelo.",
   "Tratamiento de correcciones y bajas: una baja no es un registro que desaparece en silencio.",
   "Muestra de conciliación contra la fuente, con diferencias explicadas.",
   "Pruebas de página repetida, actualización tardía y reinicio del proceso.",
 ],
 "listo": "Cuando podés apagar el proceso a la mitad, volver a prenderlo, y el resultado sigue siendo correcto.",
 "claude": """Construyamos el conector incremental de Field.

Paso 1 — Verificación, antes de codear. Revisá la documentación real de Field by Voolks a la que tengamos acceso y el código de SDB-002, y escribí `docs/SDB-009/capacidades-field.md` con: método de paginación disponible, existencia o no de cursor, límites de cuota, catálogo de estados, y cómo se representa una baja. Marcá cada ítem como VERIFICADO (con la fuente) o NO VERIFICADO. No inventes endpoints ni parámetros.

Paso 2 — Diseño. Escribí el contrato de estados en `docs/SDB-009/contrato-estados.md`: estado en Field → estado en nuestro modelo → qué implica para el derivado.

Paso 3 — Implementación del conector incremental:
- Corte explícito por ventana temporal o cursor, según lo verificado.
- Cada lote etiquetado con `schema_version` y `fecha_corte`.
- Correcciones: actualizan el derivado y conservan el valor anterior en el rastro.
- Bajas: se marcan, no se borran.
- Respeto de cuota con espera controlada.

Paso 4 — Pruebas: página repetida (no duplica), actualización tardía (gana la corrección y queda el rastro), reinicio del proceso desde el último corte (no salta registros).

Paso 5 — Conciliación: corré el conector sobre un período acotado y compará el conteo y los importes contra la fuente. Las diferencias se explican una por una, no se promedian.""",
 "codex": """Implementar el conector incremental hacia Field by Voolks para el piloto SUDBAU.

Prerrequisito: `docs/SDB-009/capacidades-field.md` con la paginación, cuota y estados VERIFICADOS. Si no existe, detenete y reportalo; no asumas un contrato de API.

Requisitos:
- Extracción incremental con cursor o ventana temporal persistida.
- Cada lote lleva `schema_version` y `fecha_corte`.
- Correcciones actualizan el derivado y conservan el valor previo en un rastro auditable.
- Bajas se marcan con `estado = baja`, nunca se eliminan filas.
- Backoff ante 429 y 5xx, con tope de reintentos.

Tests con la API mockeada: página repetida no duplica; corrección posterior sobrescribe y deja rastro; reinicio desde el cursor no omite registros; cuota agotada activa backoff y no pierde el cursor.

Aclará explícitamente en el PR qué se probó contra mock y qué falta probar contra la API real.""",
 "flex": "Si Field no ofrece cursor, la ventana temporal con solapamiento es una alternativa válida y más simple: elíjanla sin culpa y documenten el solapamiento elegido. El contrato de estados es el punto donde más conviene sentarse con alguien de operaciones antes que con el código. [Ajustar según necesidad]",
},

"SDB-010": {
 "titulo": "Que un fallo a mitad de camino no nos duplique ni nos borre nada",
 "proposito": "Las integraciones fallan: se corta internet, la API devuelve 500, alguien apaga el proceso. Lo que no puede pasar es que después de un fallo tengamos horas duplicadas o un lote perdido en silencio.",
 "entregables": [
   "Definición escrita de lote y de checkpoint: el checkpoint avanza sólo después de persistir bien.",
   "Reintentos acotados ante 429 y 5xx, con tope y espera creciente.",
   "Registro de fallos consultable: qué lote, qué error, cuándo, y si se reprocesó.",
   "Reproceso por lote que no produce doble efecto.",
   "Evidencia de recuperación: fallo inducido entre lectura, persistencia y checkpoint, y resultado verificado.",
 ],
 "listo": "Cuando inducís un corte en el peor momento posible y el sistema se recupera sin perder ni duplicar.",
 "claude": """Trabajemos la resiliencia del pipeline de ingesta.

1. Escribí `docs/SDB-010/contrato-lotes.md` definiendo: qué es un lote, qué lo identifica, cuál es su checkpoint, y la regla de oro — el checkpoint avanza **después** de persistir, nunca antes.
2. Implementá en el conector:
   - Control de lotes con estado (`pendiente`, `en_proceso`, `persistido`, `fallido`).
   - Reintentos acotados para 429 y 5xx con espera creciente y tope. Los 4xx que no sean 429 no se reintentan: se registran.
   - Registro de fallos con lote, error, timestamp y si fue reprocesado.
   - Reproceso por lote idempotente.
3. Escribí las pruebas de fallo inducido, que son el corazón de esta tarea. Necesito tres específicamente:
   - Fallo entre la lectura y la persistencia.
   - Fallo entre la persistencia y el avance del checkpoint.
   - Fallo durante el reproceso de un lote ya parcialmente aplicado.
   En los tres casos verificá que al reanudar no haya omisiones ni doble efecto.
4. Corré las pruebas y mostrame la salida real.

Si encontrás que el diseño actual no permite garantizar esto, decímelo antes de parchear: prefiero cambiar el diseño que acumular remiendos.""",
 "codex": """Agregar control de lotes, reintentos y reproceso al conector de ingesta del piloto SUDBAU.

Modelo de lote: `{ batch_id, ventana, estado, checkpoint, intentos, ultimo_error }`, con estados `pendiente | en_proceso | persistido | fallido`.

Reglas:
- El checkpoint sólo avanza después de una persistencia confirmada.
- Backoff exponencial con tope para 429 y 5xx; los demás 4xx no se reintentan.
- `reprocess(batch_id)` es idempotente: aplicar dos veces el mismo lote no cambia el resultado.

Tests obligatorios, con fallos inyectados:
1. Excepción entre lectura y persistencia → al reanudar, no faltan registros.
2. Excepción entre persistencia y avance de checkpoint → al reanudar, no se duplican registros.
3. Reproceso de un lote parcialmente aplicado → resultado final idéntico a una aplicación única.

Entregá el diff y la salida real de la suite.""",
 "flex": "Si el volumen del piloto es chico, puede que un reproceso completo por período sea más simple y suficiente que el control fino por lote. Es una decisión legítima: elíjanla y anoten el límite de volumen a partir del cual habría que revisarla. Las tres pruebas de fallo inducido son lo que yo sostendría en cualquier variante. [Ajustar según necesidad]",
},

"SDB-011": {
 "titulo": "Que se vean las jornadas y, sobre todo, las excepciones",
 "proposito": "Pasar del dato a algo que una persona puede mirar y entender: quién trabajó, cuándo, cuánto, y qué casos raros aparecieron. Las excepciones son la parte valiosa: son las que hoy alguien busca a mano.",
 "entregables": [
   "Consulta validada por OT, persona y período, con zona horaria y cobertura explícitas.",
   "Vista de jornadas, intervalos y excepciones, con dato ausente y cero claramente distintos.",
   "Cotejo reproducible: los números de la pantalla coinciden con los de la consulta.",
   "Pruebas de período incompleto, intervalos solapados y cambios de fecha.",
 ],
 "listo": "Cuando alguien de operaciones mira la pantalla y encuentra solo una excepción que antes buscaba en una planilla.",
 "claude": """Construyamos la vista de jornadas y excepciones.

1. Definí y validá la consulta base en `docs/SDB-011/consulta-jornadas.md`: parámetros (OT, persona, período), zona horaria operativa, criterio de corte del período, y cómo se calcula la cobertura. Validala contra los datos reales antes de construir la pantalla.
2. Implementá la vista:
   - Agrupación por OT, por persona y por período, con intervalos visibles.
   - Excepciones destacadas, no escondidas en un tab: solapamientos, jornadas sin cierre, personas sin OT, OT sin personas.
   - "Sin dato" y "0" se ven distinto.
   - Fecha de corte y cobertura siempre a la vista.
3. Hacé el cotejo: mismos parámetros por pantalla y por consulta directa. Guardá el resultado en `docs/SDB-011/cotejo.md`.
4. Probá explícitamente: período incompleto, dos intervalos solapados de la misma persona, y un registro que cambia de fecha por zona horaria (una jornada que cruza la medianoche).

El caso de la medianoche es el que más veces rompe este tipo de pantalla. Probalo con un ejemplo concreto y mostrame el resultado.""",
 "codex": """Implementar la vista de jornadas y excepciones del piloto SUDBAU.

Consulta: agregación por `ID_OT`, `ID_Persona` y período, con zona horaria `America/Argentina/Buenos_Aires` para el corte operativo y UTC para los timestamps técnicos.

Excepciones a detectar y mostrar: intervalos solapados de la misma persona, jornada sin cierre, persona sin OT asociada, OT sin personas.

Reglas de render: `null` ≠ `0`; `fecha_corte` y cobertura siempre visibles.

Tests: período incompleto; solapamiento de dos intervalos; jornada que cruza la medianoche local (verificar que no se duplica ni se pierde); igualdad entre el resultado de la vista y el de la consulta directa.

Entregá diff, salida de tests y el caso de medianoche documentado con datos concretos.""",
 "flex": "La lista de excepciones que propongo es un punto de partida basado en lo que suele romperse; operaciones seguro conoce otras dos que importan más. Reemplácenlas. La agrupación (por OT primero o por persona primero) es una decisión de uso real: prueben con alguien que hoy hace esta tarea a mano. [Ajustar según necesidad]",
},

"SDB-012": {
 "titulo": "Definir qué le vamos a preguntar a A01 y cuánto cuesta hoy responderlo a mano",
 "proposito": "Antes de sumar un modelo, medir. Elegimos una pregunta que importe, la respondemos manualmente cinco veces y cronometramos. Sin esa línea base, después no vamos a poder decir si la IA sirvió o si nos gustó.",
 "entregables": [
   "Ficha de A01: una pregunta prioritaria, qué métricas puede usar, y qué queda explícitamente excluido.",
   "Cinco casos resueltos a mano, identificados, con entrada, respuesta verificada y tiempo medido.",
   "Métricas de evaluación definidas antes de construir: precisión, calidad de citas, utilidad.",
   "Brechas de datos señaladas: qué no se puede responder bien hoy y por qué.",
   "Condición de entrada escrita: qué tiene que estar confiable antes de incorporar un modelo.",
 ],
 "listo": "Cuando tenemos un número: «hoy responder esto nos lleva X minutos y acertamos en Y de 5».",
 "claude": """Preparemos la línea base de A01, sin incorporar todavía ningún modelo.

1. A partir de lo que ya está construido (SDB-006, SDB-011) y de lo que sabés del negocio de SUDBAU, proponeme cinco candidatas a "pregunta prioritaria" que A01 podría responder sobre métricas autorizadas. Para cada una: qué datos necesita, si esos datos hoy son confiables, y qué valor tendría responderla rápido. Después esperá mi elección.
2. Con la pregunta elegida, escribí `docs/SDB-012/ficha-a01.md`: enunciado, métricas autorizadas que puede usar, fuentes, y una lista explícita de exclusiones (qué no debe responder aunque se lo pidan: nada de liquidación, nada de datos personales, nada de decisiones laborales).
3. Diseñá el protocolo de medición manual: cinco casos identificados, quién los resuelve, cómo se cronometra, y cómo se verifica que la respuesta es correcta. Plantilla en `docs/SDB-012/linea-base-manual.md`.
4. Definí las métricas de evaluación **antes** de que exista el modelo: precisión (respuesta correcta sí/no), citas (¿señala la fuente y el corte?), utilidad (¿le sirvió a quien preguntó?). Escribí cómo se puntúa cada una.
5. Señalá las brechas: qué parte de la pregunta hoy no se puede responder con confianza y qué haría falta.

No incorpores un modelo en esta tarea. Si te parece que ya estamos listos para hacerlo, decímelo y lo discutimos, pero no lo hagas.""",
 "codex": """Generar el paquete de línea base de A01 en `docs/SDB-012/`, sin integrar ningún modelo.

Archivos:
- `ficha-a01.md`: pregunta prioritaria, métricas autorizadas, fuentes, exclusiones explícitas (liquidación salarial, datos personales, decisiones laborales).
- `linea-base-manual.md`: plantilla para cinco casos con campos `caso_id`, `entrada`, `respuesta_verificada`, `verificado_por`, `minutos`, `fuentes_consultadas`.
- `metricas-evaluacion.md`: definición y escala de precisión, citas y utilidad, fijadas antes de construir.
- `brechas-datos.md`: qué no se puede responder hoy y qué falta.

Restricción: no agregues dependencias de modelos ni llamadas a APIs de IA en este cambio.""",
 "flex": "Medir cinco casos a mano suena tedioso y es tentador saltarlo. Es lo único que después permite decir si A01 vale la pena. Si cinco es mucho, hagan tres — pero háganlos. La pregunta prioritaria puede cambiar cuando vean los datos reales: cambiarla es aprendizaje, no retroceso. [Ajustar según necesidad]",
},

}
