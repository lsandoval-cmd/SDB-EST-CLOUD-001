# -*- coding: utf-8 -*-
"""Genera pdt.html — Plan de Trabajo vivo de SUDBAU · SDB-EST-CLOUD-001."""
import json, re, sys, html, pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from contenido_1 import BLOQUE_1
from contenido_2 import BLOQUE_2
from contenido_3 import BLOQUE_3

REPO = pathlib.Path(__file__).resolve().parents[2]  # raíz del repositorio
CONTENIDO = {**BLOQUE_1, **BLOQUE_2, **BLOQUE_3}

# ---------------------------------------------------------------- datos base
src = (REPO / 'index.html').read_text(encoding='utf-8')
m = re.search(r'<script[^>]*id="guide-data"[^>]*>(.*?)</script>', src, re.S)
GUIDE = json.loads(m.group(1))
TASKS = GUIDE['tasks']

faltan = [t['id'] for t in TASKS if t['id'] not in CONTENIDO]
sobran = [k for k in CONTENIDO if k not in {t['id'] for t in TASKS}]
if faltan or sobran:
    raise SystemExit(f'Desalineado. Faltan: {faltan} | Sobran: {sobran}')

FASES = {
 'F0': ('Fundaciones', 'Accesos, ambientes y reglas para trabajar con confianza.'),
 'F1': ('APIs y maestros', 'Unir Field, Microtrack y reloj con identificadores confiables.'),
 'F2': ('Operación y costos', 'Una OT trazable; luego flota y costo por pozo.'),
 'F3': ('IA supervisada', 'A01 primero: respuestas con fuentes. A02 después: borradores revisados.'),
 'F4': ('ERP y novedades', 'Conectar Administración y preparar novedades aprobadas.'),
 'F5': ('Escala con control', 'Evaluar acciones asistidas después de aceptar el piloto.'),
}

PREAMBULO = """CONTEXTO FIJO · SUDBAU S.A. — proyecto SDB-EST-CLOUD-001
Estamos construyendo el piloto del ERP Operativo de SUDBAU (servicios industriales y Oil & Gas, Argentina).
Meta del piloto: seguir una orden de trabajo desde el parte de campo hasta los indicadores y las novedades revisadas, conservando siempre la trazabilidad hasta la fuente.

Repositorio: [completar]
Rama: [completar]
Ambiente: TEST, salvo indicación expresa.
Fuentes y muestras autorizadas para esta sesión: [completar]

REGLAS QUE VALEN PARA TODAS LAS TAREAS
- No inventes endpoints, credenciales, permisos, archivos ni decisiones. Si falta información, decilo y avanzá con lo verificable.
- Distinguí siempre decisión documentada, propuesta, implementación comprobada y pendiente.
- Leé AGENTS.md, CLAUDE.md y las reglas locales del repositorio antes de escribir código. Reutilizá lo que ya existe.
- Conservá los originales. Un derivado nunca se escribe encima de su fuente.
- Identificadores: ID_Persona en los intercambios técnicos; el CUIL sólo en entornos autorizados; ID_OT e ID_Pozo + cliente para imputar costos.
- Fechas: zona operativa America/Argentina/Buenos_Aires para los cortes; timestamps técnicos en UTC. Declaralo siempre.
- Importes: moneda explícita, precisión y redondeo definidos. Si hay conversión ARS/USD, guardá tasa, fuente y fecha.
- Dato ausente no es cero. Salida del modelo no es corrección humana, y ninguna de las dos es dato validado.
- Los permisos se verifican en el backend. Un filtro de pantalla o el dominio del correo no son autorización.
- Las reglas de negocio y los cálculos van fuera del modelo de IA.
- Nunca declares como ejecutado un comando, un test, un recurso creado o un despliegue sin evidencia real.
- Nada de secretos ni datos personales en el sitio público de planificación.

CÓMO CERRAR LA SESIÓN — entregá siempre:
1. Archivos o cambios concretos, con ruta y versión.
2. Resultado por criterio: cumple, no cumple, no probado o pendiente de decisión, con su evidencia.
3. Comandos y pruebas realmente ejecutados, con su salida.
4. Defectos, límites y datos faltantes, con próxima acción y responsable.
5. Cómo reproducir el resultado y cómo revertirlo.
6. Resumen para el tablero: ID, cambio, evidencia, próximo paso y estado sugerido."""


def prompt_text(t, c, herramienta):
    cuerpo = c['claude'] if herramienta == 'claude' else c['codex']
    dep = ', '.join(t['dependencies']) or 'sin predecesoras declaradas'
    crit = '\n'.join(f'{i+1}. {x}' for i, x in enumerate(t['criteria']))
    entre = '\n'.join(f'- {x}' for x in c['entregables'])
    return f"""{PREAMBULO}

════════════════════════════════════════
TAREA {t['id']} · {c['titulo']}
Responsable propuesto: {t['owner']} · Fase {t['phase']} · Sprint {t['sprint']} · Tipo: {t['kind']}
Dependencias: {dep}. Verificá su resultado, ambiente y evidencia antes de apoyarte en ellas.
════════════════════════════════════════

POR QUÉ LO HACEMOS
{c['proposito']}

LO QUE TE PIDO
{cuerpo}

ENTREGABLES ESPERADOS
{entre}

CRITERIOS DE ACEPTACIÓN (vienen del tablero, no los reescribas por tu cuenta)
{crit}

DEFINICIÓN DE LISTO
{c['listo']}

PASOS DE REFERENCIA DEL PLAN (son una guía, no una obligación)
""" + '\n'.join(f"{s['id']} · {s['action']}" for s in t['steps'])


e = lambda x: html.escape(str(x if x is not None else ''), quote=True)

def marcar(txt):
    """Resalta los marcadores [Ajustar según necesidad] y similares."""
    out = e(txt)
    return re.sub(r'\[([^\]\[]{3,60})\]', r'<span class="chip-ajuste">[\1]</span>', out)


# ---------------------------------------------------------------- secciones
def bloque_tarea(t):
    c = CONTENIDO[t['id']]
    dep = (', '.join(f'<a href="#{e(d)}">{e(d)}</a>' for d in t['dependencies'])
           or '<span class="muted">sin predecesoras declaradas</span>')
    ent = ''.join(f'<li>{e(x)}</li>' for x in c['entregables'])
    cri = ''.join(f'<li>{e(x)}</li>' for x in t['criteria'])
    pasos = ''.join(
        f'<li><b>{e(s["id"])}</b> · {e(s["title"])} — {e(s["action"])}</li>' for s in t['steps'])
    rev = f' · revisa {e(t["reviewer"])}' if t.get('reviewer') else ''

    def caja(tag, titulo, texto):
        return (f'<details class="prompt" data-prompt="{tag}">'
                f'<summary>{titulo}</summary><div class="prompt-body">'
                f'<div class="actions"><button type="button" data-copy>Copiar prompt</button>'
                f'<button type="button" class="secondary" data-download>Descargar .md</button>'
                f'<span class="copied" hidden>¡Copiado!</span></div>'
                f'<textarea readonly rows="16" aria-label="Prompt {tag}">{e(texto)}</textarea>'
                f'</div></details>')

    return f"""
<article class="task" id="{e(t['id'])}" data-id="{e(t['id'])}" data-owner="{e(t['owner'])}"
         data-sprint="{e(t['sprint'])}" data-phase="{e(t['phase'])}"
         data-search="{e((t['id'] + ' ' + c['titulo'] + ' ' + t['owner'] + ' ' + c['proposito']).lower())}">
  <header class="task-head">
    <div>
      <span class="eyebrow">{e(t['id'])} · Fase {e(t['phase'])} · {e(t['sprint'])}</span>
      <h3>{e(c['titulo'])}</h3>
      <p class="meta">Responsable propuesto: {e(t['owner'])}{rev} · Tipo: {e(t['kind'])} · Depende de: {dep}</p>
    </div>
    <div class="task-links">
      <a class="button secondary" href="index.html#{e(t['id'])}">Checklist ↗</a>
      <a class="button secondary" href="tablero_scrumban.html#{e(t['id'])}">Tarjeta ↗</a>
      <button class="secondary" type="button" data-link="{e(t['id'])}">Copiar enlace</button>
    </div>
  </header>

  <h4>Por qué lo hacemos</h4>
  <p>{e(c['proposito'])}</p>

  <h4>Qué vamos a tener al terminar</h4>
  <ul class="entregables">{ent}</ul>
  <p class="listo"><b>Sabemos que está listo</b> cuando… {e(c['listo'])}</p>

  <h4>Prompts listos para usar</h4>
  {caja(t['id'] + '-claude', 'Prompt para <b>Claude Code</b> — trabaja dentro del repositorio, explora, ejecuta y reporta', prompt_text(t, c, 'claude'))}
  {caja(t['id'] + '-codex', 'Prompt para <b>Codex</b> — cambio acotado, con diff y tests', prompt_text(t, c, 'codex'))}

  <details class="pasos"><summary>Pasos de referencia y criterios de aceptación del plan original</summary>
    <ol class="pasos-lista">{pasos}</ol>
    <h5>Criterios de aceptación (fuente: tablero)</h5>
    <ul>{cri}</ul>
  </details>

  <div class="flex-box">
    <h4>Espacio de flexibilidad</h4>
    <p>{marcar(c['flex'])}</p>
  </div>
</article>"""


def indice():
    out = []
    for fase, (nombre, desc) in FASES.items():
        ts = [t for t in TASKS if t['phase'] == fase]
        if not ts:
            continue
        items = ''.join(
            f'<li><a href="#{e(t["id"])}"><b>{e(t["id"])}</b> {e(CONTENIDO[t["id"]]["titulo"])}</a>'
            f'<small>{e(t["owner"])} · {e(t["sprint"])}</small></li>' for t in ts)
        out.append(f'<section class="fase"><h3>{e(fase)} · {e(nombre)}</h3>'
                   f'<p class="muted">{e(desc)}</p><ul class="indice">{items}</ul></section>')
    return ''.join(out)


CSS = """
:root{--navy:#05145a;--blue:#0055aa;--ink:#192345;--muted:#58657d;--line:#dce3ef;--bg:#f3f5fa;
--warm:#8a5a12;--warmbg:#fff6e4;--warmline:#f0d9a8;--good:#2f6a4a;--goodbg:#eef7f1}
*{box-sizing:border-box}html{scroll-padding-top:96px}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.65 system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
a{color:var(--blue)}button,input,select,textarea{font:inherit}
button,.button{display:inline-block;border:1px solid var(--blue);border-radius:8px;background:var(--blue);
color:#fff;padding:8px 13px;cursor:pointer;font-weight:600;text-decoration:none;font-size:13px}
button:hover,.button:hover{filter:brightness(.94)}
button.secondary,.button.secondary{color:var(--blue);background:#fff;border-color:var(--line)}
button:focus-visible,a:focus-visible,input:focus-visible,select:focus-visible,summary:focus-visible{outline:3px solid #008fa5;outline-offset:3px}
header.top{background:#fff;border-bottom:1px solid var(--line);padding:26px max(20px,calc((100vw - 1140px)/2))}
h1{font-size:30px;line-height:1.15;margin:6px 0 10px;color:var(--navy)}
h2{font-size:22px;margin:28px 0 10px;color:var(--navy)}
h3{font-size:19px;margin:0 0 6px}
h4{font-size:15px;margin:20px 0 6px;color:var(--navy);letter-spacing:.2px}
h5{font-size:14px;margin:16px 0 6px}
.eyebrow{font-size:11px;letter-spacing:1.6px;font-weight:750;color:var(--blue);text-transform:uppercase}
main{max-width:1140px;padding:20px 20px 60px;margin:auto}
p{margin:10px 0}.muted,.meta,small{color:var(--muted);font-size:13.5px}
.card{background:#fff;border:1px solid var(--line);border-radius:14px;padding:20px 22px;margin-bottom:16px}
.card.vivo{background:var(--warmbg);border-color:var(--warmline)}
.card.vivo h2,.card.vivo h3{color:var(--warm)}
.grid3{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px;margin:14px 0}
.grid3>div{background:#fff;border:1px solid var(--line);border-radius:11px;padding:14px 16px}
.filters{display:grid;grid-template-columns:2fr 1fr 1fr 1fr auto;gap:9px;align-items:end;
position:sticky;top:0;z-index:5;background:var(--bg);padding:12px 0;border-bottom:1px solid var(--line);margin-bottom:14px}
.filters label{font-size:12px;font-weight:650;display:block;margin-bottom:3px}
.filters input,.filters select{width:100%;border:1px solid var(--line);border-radius:8px;padding:9px;background:#fff;color:var(--ink)}
.fase{margin-bottom:18px}
ul.indice{list-style:none;padding:0;margin:8px 0 0;display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:6px}
ul.indice li{background:#fff;border:1px solid var(--line);border-radius:9px;padding:9px 12px;font-size:14px}
ul.indice small{display:block}
article.task{background:#fff;border:1px solid var(--line);border-radius:14px;padding:20px 22px;margin-bottom:18px;scroll-margin-top:96px}
article.task:target{outline:3px solid #008fa5;outline-offset:2px}
.task-head{display:flex;justify-content:space-between;gap:18px;align-items:flex-start;flex-wrap:wrap;
border-bottom:1px solid var(--line);padding-bottom:12px;margin-bottom:4px}
.task-links{display:flex;gap:7px;flex-wrap:wrap}
ul.entregables{margin:6px 0;padding-left:20px}
ul.entregables li{margin:5px 0}
.listo{background:var(--goodbg);border-left:3px solid var(--good);padding:9px 13px;border-radius:0 8px 8px 0;font-size:14.5px}
details.prompt{margin:9px 0;border:1px solid #c8d9ec;background:#edf5ff;border-radius:9px}
details.prompt>summary{padding:11px 14px;color:var(--blue);font-weight:650;font-size:14.5px;cursor:pointer}
.prompt-body{padding:0 14px 14px}
.prompt-body textarea{width:100%;border:1px solid #c8d9ec;border-radius:8px;padding:11px;
font:13px/1.55 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;background:#fff;color:var(--ink);resize:vertical}
.actions{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-bottom:9px}
.copied{color:var(--good);font-size:13px;font-weight:650}
details.pasos{margin:14px 0;border:1px solid var(--line);border-radius:9px;background:#f8fafd}
details.pasos>summary{padding:10px 14px;font-size:14px;font-weight:600;cursor:pointer;color:var(--muted)}
details.pasos ol,details.pasos ul{margin:0 0 12px;padding-left:34px;font-size:14px}
.pasos-lista li{margin:5px 0}
.flex-box{background:var(--warmbg);border:1px solid var(--warmline);border-radius:10px;padding:12px 16px;margin-top:16px}
.flex-box h4{margin-top:0;color:var(--warm)}
.chip-ajuste{background:#fff;border:1px dashed var(--warm);color:var(--warm);border-radius:6px;padding:1px 6px;font-weight:650;font-size:13px;white-space:nowrap}
summary::-webkit-details-marker{display:none}
summary{list-style:none}
details>summary:before{content:"▸ ";color:var(--blue)}
details[open]>summary:before{content:"▾ "}
.count{font-size:13px;color:var(--muted);margin:0 0 10px}
footer{max-width:1140px;margin:auto;padding:0 20px 50px;color:var(--muted);font-size:13.5px}
@media(max-width:760px){html{scroll-padding-top:12px}article.task{scroll-margin-top:12px}.filters{grid-template-columns:1fr 1fr;position:static}
 .task-head{flex-direction:column}h1{font-size:24px}body{font-size:15px}}
@media print{.filters,.task-links,.actions{display:none}details{open:true}}
"""

JS = """
'use strict';
const $=s=>document.querySelector(s), $$=s=>Array.from(document.querySelectorAll(s));
function filtrar(){
  const q=$('#q').value.trim().toLowerCase(), o=$('#owner').value, s=$('#sprint').value, f=$('#phase').value;
  let n=0;
  $$('article.task').forEach(el=>{
    const ok=(!q||el.dataset.search.includes(q))&&(!o||el.dataset.owner===o)&&
             (!s||el.dataset.sprint===s)&&(!f||el.dataset.phase===f);
    el.hidden=!ok; if(ok)n++;
  });
  $('#count').textContent=n+' de '+$$('article.task').length+' tareas visibles';
}
['q','owner','sprint','phase'].forEach(id=>{
  const el=document.getElementById(id);
  el.addEventListener('input',filtrar); el.addEventListener('change',filtrar);
});
$('#limpiar').addEventListener('click',()=>{['q','owner','sprint','phase'].forEach(id=>document.getElementById(id).value='');filtrar();});

async function copiar(texto,aviso){
  try{ await navigator.clipboard.writeText(texto); }
  catch(e){ const t=document.createElement('textarea'); t.value=texto; document.body.append(t);
            t.select(); try{document.execCommand('copy');}catch(_){ } t.remove(); }
  if(aviso){ aviso.hidden=false; setTimeout(()=>aviso.hidden=true,1600); }
}
document.addEventListener('click',ev=>{
  const c=ev.target.closest('[data-copy]');
  if(c){ const box=c.closest('.prompt'); copiar(box.querySelector('textarea').value,box.querySelector('.copied')); return; }
  const d=ev.target.closest('[data-download]');
  if(d){ const box=d.closest('.prompt'), nom=box.dataset.prompt+'.md';
         const u=URL.createObjectURL(new Blob([box.querySelector('textarea').value],{type:'text/markdown'}));
         const a=document.createElement('a'); a.href=u; a.download=nom; document.body.append(a); a.click(); a.remove();
         setTimeout(()=>URL.revokeObjectURL(u),2000); return; }
  const l=ev.target.closest('[data-link]');
  if(l){ copiar(location.origin+location.pathname+'#'+l.dataset.link,null); l.textContent='Enlace copiado'; setTimeout(()=>l.textContent='Copiar enlace',1600); }
});
$('#abrir-todo').addEventListener('click',()=>$$('details').forEach(d=>d.open=true));
$('#cerrar-todo').addEventListener('click',()=>$$('details').forEach(d=>d.open=false));
if(location.hash){const el=document.getElementById(decodeURIComponent(location.hash.slice(1)));if(el)el.scrollIntoView();}
filtrar();
"""

owners = sorted({t['owner'] for t in TASKS})
sprints = sorted({t['sprint'] for t in TASKS}, key=lambda s: (len(s), s))
phases = [p for p in FASES if any(t['phase'] == p for t in TASKS)]

opt = lambda vals: ''.join(f'<option value="{e(v)}">{e(v)}</option>' for v in vals)

HTML = f"""<!DOCTYPE html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#05145a">
<meta name="description" content="Plan de Trabajo vivo del piloto SUDBAU SDB-EST-CLOUD-001: propósito, entregables y prompts para Claude Code y Codex por cada tarea SDB-001 a SDB-040.">
<title>SUDBAU · PDT · Plan de Trabajo vivo</title>
<style>{CSS}</style></head>
<body>
<header class="top">
  <span class="eyebrow">SUDBAU S.A. · SDB-EST-CLOUD-001</span>
  <h1>Plan de Trabajo (PDT) — nuestro manual de a bordo</h1>
  <p class="muted">Documento vivo · Revisión {e(GUIDE['revision'])} · Derivado del tablero {e(GUIDE['sourceCommit'][:8])} ·
  {len(TASKS)} tareas, de SDB-001 a SDB-040 (más el ajuste SDB-003.1)</p>
</header>

<main>

<div class="card vivo">
  <h2>Antes que nada: esto es un punto de partida, no un examen</h2>
  <p>Acá vas a encontrar, tarea por tarea, para qué sirve, qué tenemos que tener al terminar y un prompt listo para
  copiar y pegar en <b>Claude Code</b> o en <b>Codex</b>. La idea es simple: que nadie arranque desde una hoja en blanco
  y que nadie tenga que adivinar qué se espera.</p>
  <p><b>Ahora lo importante.</b> Los prompts de este documento son una propuesta. Vos conocés el código, los datos y el
  cliente mejor que el prompt. Si algo no encaja, cambialo. Si un paso sobra, saltealo. Si encontrás una forma mejor,
  usala y contala. El control del código y del proceso es del equipo, siempre.</p>
  <p>Cada tarea termina con un bloque <b>Espacio de flexibilidad</b> donde te decimos qué partes conviene cuestionar.
  Y donde veas un marcador como <span class="chip-ajuste">[Ajustar según necesidad]</span>, tomalo como una invitación
  explícita a decidir vos.</p>
  <p class="muted">Una sola cosa pedimos no negociar: que lo que digamos que está hecho, esté hecho de verdad, con
  evidencia. El resto se conversa.</p>
</div>

<div class="grid3">
  <div><h3>El tablero</h3><p class="muted">Coordinación y estado. Dónde está cada tarjeta, quién la tiene, qué la bloquea.
  <br><a href="tablero_scrumban.html">Abrir el tablero ↗</a></p></div>
  <div><h3>Este PDT</h3><p class="muted">Instrucciones, entregables y prompts. Lo que hay que hacer y cómo empezar.
  Las tarjetas enlazan acá para no llenarse de texto.</p></div>
  <div><h3>El checklist</h3><p class="muted">Progreso personal con casillas, notas y evidencia, guardado en tu navegador.
  <br><a href="index.html">Abrir el checklist ↗</a></p></div>
</div>

<div class="card">
  <h2>Cómo usamos esto, en cuatro pasos</h2>
  <ol>
    <li><b>Agarrás una tarjeta</b> del tablero y hacés clic en su enlace al PDT. Caés justo en la tarea, no en el índice.</li>
    <li><b>Leés el propósito y los entregables.</b> Si algo no te cierra, ese es el momento de decirlo — no después.</li>
    <li><b>Copiás el prompt</b> que prefieras, completás las tres líneas del contexto (repositorio, rama, fuentes) y arrancás.
    Ajustá el prompt todo lo que necesites antes de enviarlo.</li>
    <li><b>Cerrás con evidencia</b>: qué cambió, qué probaste de verdad, qué quedó pendiente. Eso vuelve al tablero y al checklist.</li>
  </ol>
  <p class="muted">Los dos prompts de cada tarea no son el mismo texto con otro nombre. El de <b>Claude Code</b> asume que
  la herramienta puede recorrer el repositorio, ejecutar comandos y volver con hallazgos: por eso arranca explorando y
  pide reportar lo que encontró. El de <b>Codex</b> apunta a un cambio acotado y revisable: archivos concretos, diff y
  tests. Usá el que te sirva, o mezclalos.</p>
</div>

<div class="card">
  <h2>Contexto fijo que viaja en todos los prompts</h2>
  <p>Para no repetir lo mismo 41 veces, cada prompt ya trae este preámbulo adelante. Si el equipo decide cambiar una de
  estas reglas, se cambia acá y vale para todos. <span class="chip-ajuste">[Ajustar según necesidad]</span></p>
  <details class="prompt" data-prompt="preambulo"><summary>Ver el contexto fijo</summary>
    <div class="prompt-body">
      <div class="actions"><button type="button" data-copy>Copiar</button>
      <button type="button" class="secondary" data-download>Descargar .md</button>
      <span class="copied" hidden>¡Copiado!</span></div>
      <textarea readonly rows="14" aria-label="Contexto fijo">{e(PREAMBULO)}</textarea>
    </div>
  </details>
</div>

<div class="card vivo">
  <h2>Cómo proponer un cambio a este PDT</h2>
  <p>El PDT es código como cualquier otro: vive en el repositorio y se mejora con un cambio propuesto y revisado.</p>
  <ol>
    <li>Rama <code>pdt/&lt;lo-que-cambias&gt;</code>.</li>
    <li>Editá el contenido y regenerá la página (el generador y el contenido viven junto al archivo).</li>
    <li>En la descripción del cambio contá <b>por qué</b>: qué pasó al usar el prompt que te hizo querer cambiarlo. Ese
    "por qué" es lo más valioso que podés dejarle al que venga después.</li>
    <li>Una revisión de otra persona y listo.</li>
  </ol>
  <p class="muted">Si un prompt te funcionó mucho mejor con un ajuste, traelo. Este documento mejora con el uso, no con
  la prolijidad.</p>
</div>

<h2>Índice por fase</h2>
{indice()}

<h2 id="tareas">Las tareas, una por una</h2>

<div class="filters">
  <div><label for="q">Buscar</label><input id="q" type="search" placeholder="ID, título, responsable…"></div>
  <div><label for="owner">Responsable</label><select id="owner"><option value="">Todos</option>{opt(owners)}</select></div>
  <div><label for="sprint">Sprint</label><select id="sprint"><option value="">Todos</option>{opt(sprints)}</select></div>
  <div><label for="phase">Fase</label><select id="phase"><option value="">Todas</option>{opt(phases)}</select></div>
  <div><button id="limpiar" class="secondary" type="button">Limpiar</button></div>
</div>
<p class="count"><span id="count"></span> ·
  <button id="abrir-todo" class="secondary" type="button">Abrir todo</button>
  <button id="cerrar-todo" class="secondary" type="button">Cerrar todo</button></p>

{''.join(bloque_tarea(t) for t in TASKS)}

</main>
<footer>
  <p><b>Recordatorio final.</b> Los responsables, los sprints y los prompts de este documento son propuestas del plan,
  no asignaciones cerradas. Un prompt no aprueba nada, no despliega nada y no reemplaza una revisión humana. Lo que
  vale es el resultado con evidencia.</p>
  <p class="muted">Generado a partir del tablero {e(GUIDE['sourceCommit'][:8])} y del checklist revisión {e(GUIDE['revision'])}.
  Si encontrás una contradicción entre este documento y el tablero, el tablero manda para el estado y este documento manda
  para las instrucciones — y avisá, que algo hay que arreglar.</p>
</footer>
<script>{JS}</script>
</body></html>
"""

out = REPO / 'pdt.html'
out.write_text(HTML, encoding='utf-8')
print('OK', out, len(HTML), 'bytes,', len(TASKS), 'tareas')
