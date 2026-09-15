# SDB-EST-CLOUD-001 · SUDBAU S.A.

Planificación del piloto del ERP Operativo de SUDBAU: seguir una orden de trabajo desde el
parte de campo hasta los indicadores y las novedades revisadas, conservando la trazabilidad
hasta la fuente.

Este repositorio contiene **material de planificación publicado en GitHub Pages**. No es el
repositorio de código del piloto y no debe contener secretos, credenciales ni datos personales.

## Qué es cada archivo

| Archivo | Qué es | Para qué se usa |
|---|---|---|
| `tablero_scrumban.html` | **El tablero.** Siete columnas, tarjetas SDB-001 a SDB-040. | Coordinación y estado: quién tiene qué, qué está bloqueado, qué entró al sprint. |
| `pdt.html` | **El PDT (Plan de Trabajo).** Documento vivo con propósito, entregables y prompts por tarea. | Saber cómo encarar cada tarea. Las tarjetas del tablero enlazan acá. |
| `index.html` | **El checklist.** Casillas de avance, notas y evidencia por tarea. | Registrar el avance propio. Es la página de inicio del sitio publicado. |

> Nota histórica: `index.html` es el checklist renombrado para GitHub Pages, **no** el tablero.
> Identificá siempre un archivo por su contenido antes de editarlo.

## Cómo se enlazan

- Tarjeta del tablero → `pdt.html#SDB-012` (instrucciones y prompts de esa tarea).
- Tarea del PDT → `index.html#SDB-012` (checklist) y `tablero_scrumban.html#SDB-012` (tarjeta).
- El tablero abre la tarjeta correspondiente al llegar con `#SDB-012` en la URL.

## Persistencia real, y sus límites

Las tres páginas guardan su estado en el `localStorage` **del navegador de cada persona**.

- No hay sincronización entre personas ni entre dispositivos.
- Publicar en GitHub Pages no comparte avances: comparte la página, no los datos.
- Exportar a HTML o JSON produce una copia; dos copias editadas en paralelo no se combinan solas.
- Para trabajar en equipo hay que exportar, compartir la copia y acordar quién la mantiene.

Esto es una limitación conocida y aceptada de la herramienta actual, no un error.

## Regenerar el PDT

El contenido del PDT vive en `tools/pdt/` y la página se genera desde ahí:

```bash
python3 tools/pdt/build_pdt.py
```

- `tools/pdt/contenido_1.py`, `contenido_2.py`, `contenido_3.py` — propósito, entregables,
  prompts y espacio de flexibilidad de cada tarea. **Acá se edita el contenido.**
- `tools/pdt/build_pdt.py` — arma `pdt.html`. Los IDs, responsables, sprints, dependencias y
  criterios de aceptación se leen del `guide-data` de `index.html`, que a su vez proviene del
  tablero: no se duplican a mano.
- El generador falla si un ID del tablero no tiene contenido en el PDT, o al revés.

## Cómo proponer un cambio

1. Rama `pdt/<lo-que-cambias>` o `sdb-<id>/<slug>`.
2. Editá el contenido, regenerá `pdt.html` y revisá el diff.
3. En la descripción del cambio contá **por qué**: qué pasó al usar el prompt que te hizo
   querer cambiarlo.
4. Una revisión de otra persona.

## Alcance y advertencias

- Responsables, sprints y prompts son **propuestas del plan**, no asignaciones confirmadas.
- Un prompt no aprueba nada, no despliega nada y no reemplaza una revisión humana.
- Una tarjeta cerrada o una casilla marcada **no acreditan** una integración funcionando.
- El cálculo de liquidación salarial sigue tercerizado durante el piloto.
