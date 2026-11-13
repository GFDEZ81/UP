#!/usr/bin/env python3
"""Genera el proyecto HyperFrames del reel Zoho (AGF Conecta)."""
import json, os

P = "/tmp/claude-0/-home-user-UP/28e7ed4e-ff55-5b09-b431-2b6a74c02655/scratchpad/zoho-reel"
W = json.load(open(os.path.join(os.path.dirname(__file__), "words2.json")))
WT = {w["id"]: w["start"] for w in W}
def ws(i): return W[i]["start"]
def we(i): return W[i]["end"]

FPS = 30
TOTAL = 29.7

# ---- escenas: (id, start, end, kind) kind: avatar | full
SC = [
    ("hook",      0.00,  4.15, "avatar"),
    ("campaigns", 4.15,  6.45, "full"),
    ("channels",  6.45, 10.10, "full"),
    ("crm",      10.10, 13.75, "avatar"),
    ("flow",     13.75, 16.60, "full"),
    ("three",    16.60, 19.75, "full"),
    ("price",    19.75, 21.45, "avatar"),
    ("remate",   21.45, 23.85, "full"),
    ("cta",      23.85, 26.70, "avatar"),
    ("cierre",   26.70, TOTAL, "full"),
]
OVERLAP = 0.4  # una escena completa que va seguida de otra completa se queda debajo durante el barrido

COMMON_CSS = """
#root{position:absolute;inset:0;overflow:hidden;font-family:'Outfit',sans-serif;color:#f8fafc}
.bg{position:absolute;inset:0}
.bg.azul{background:#1d4ed8}.bg.oscuro{background:#0d1b2a}.bg.claro{background:#eef2f7}
.stage{position:absolute;inset:0}
.h{font-family:'Outfit';font-weight:700;line-height:1.0;letter-spacing:-0.03em}
.it{font-family:'Playfair Display';font-style:italic;font-weight:500;letter-spacing:-0.01em}
.sup{font-family:'Inter';font-weight:600;font-size:32px;letter-spacing:0}
.card{position:absolute;background:#ffffff;color:#0d1b2a;border-radius:44px;box-shadow:0 24px 60px rgba(13,27,42,.35)}
.ico{display:flex;align-items:center;justify-content:center;background:#1d4ed8;border-radius:24px}
.ico svg{stroke:#fff;fill:none;stroke-width:2.4;stroke-linecap:round;stroke-linejoin:round}
.pill{position:absolute;border-radius:999px;font-family:'Outfit';font-weight:700;white-space:nowrap}
"""

ICON = {
 "mail": '<rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
 "sms": '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>',
 "wa": '<path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/>',
 "check": '<path d="M20 6 9 17l-5-5"/>',
 "sync": '<path d="M8 3 4 7l4 4"/><path d="M4 7h16"/><path d="m16 21 4-4-4-4"/><path d="M20 17H4"/>',
 "userplus": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><line x1="19" x2="19" y1="8" y2="14"/><line x1="22" x2="16" y1="11" y2="11"/>',
 "spark": '<path d="M9.937 15.5A2 2 0 0 0 8.5 14.063l-6.135-1.582a.5.5 0 0 1 0-.962L8.5 9.936A2 2 0 0 0 9.937 8.5l1.582-6.135a.5.5 0 0 1 .963 0L14.063 8.5A2 2 0 0 0 15.5 9.937l6.135 1.581a.5.5 0 0 1 0 .964L15.5 14.063a2 2 0 0 0-1.437 1.437l-1.582 6.135a.5.5 0 0 1-.963 0z"/>',
 "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
}
def icon(name, box=96, size=52, cls="ico", extra=""):
    return (f'<div class="{cls}" style="width:{box}px;height:{box}px;{extra}">'
            f'<svg viewBox="0 0 24 24" width="{size}" height="{size}">{ICON[name]}</svg></div>')

def scene_file(sid, dur, body, js, css="", transparent=False):
    return f"""<template>
  <style>{COMMON_CSS}{css}</style>
  <div id="root" data-composition-id="{sid}" data-width="1080" data-height="1920" data-layout-allow-overlap>
{body}
  </div>
  <script>
    (function(){{
    const tl = gsap.timeline({{ paused: true }});
    const S = (t) => t; // tiempos locales de la escena
{js}
    window.__timelines["{sid}"] = tl;
    }})();
  </script>
</template>
"""

def full_in(sid, color_from="bottom"):
    """Barrido de color 0,4 s + acercamiento 1,07→1,0 + glitch de 3 fotogramas."""
    clip_from = "inset(100% 0% 0% 0%)" if color_from == "bottom" else "inset(0% 100% 0% 0%)"
    return f"""
    tl.fromTo("#{sid}-bg", {{clipPath:"{clip_from}"}}, {{clipPath:"inset(0% 0% 0% 0%)", duration:0.4, ease:"power2.inOut"}}, 0);
    tl.fromTo("#{sid}-stage", {{scale:1.07, opacity:0}}, {{scale:1.0, opacity:1, duration:0.5, ease:"expo.out"}}, 0.18);
    tl.to("#{sid}-stage", {{scale:1.03, duration:2.6, ease:"none"}}, 0.68);
    tl.fromTo("#{sid}-stage", {{x:0, skewX:0}}, {{x:18, skewX:-6, duration:0.034, ease:"none", immediateRender:false}}, 0.40);
    tl.to("#{sid}-stage", {{x:-12, skewX:4, duration:0.034, ease:"none"}}, 0.434);
    tl.to("#{sid}-stage", {{x:0, skewX:0, duration:0.034, ease:"none"}}, 0.468);
"""

def full_out(sid, dur):
    """Salida hacia el avatar: la escena se recoge hacia arriba en 0,35 s."""
    return f"""
    tl.fromTo("#{sid}-wrap", {{clipPath:"inset(0% 0% 0% 0%)"}}, {{clipPath:"inset(0% 0% 100% 0%)", duration:0.35, ease:"power3.in"}}, {dur-0.36:.3f});
"""

def shake(sel, t, amp=14):
    return f"""
    tl.fromTo("{sel}", {{x:0,y:0}}, {{x:{amp},y:{-amp*0.6}, duration:0.05, ease:"none", immediateRender:false}}, {t:.3f});
    tl.to("{sel}", {{x:{-amp*0.7},y:{amp*0.4}, duration:0.05, ease:"none"}}, {t+0.05:.3f});
    tl.to("{sel}", {{x:{amp*0.35},y:{-amp*0.2}, duration:0.06, ease:"none"}}, {t+0.10:.3f});
    tl.to("{sel}", {{x:0,y:0, duration:0.12, ease:"power2.out"}}, {t+0.16:.3f});
"""

files = {}
start = {s[0]: s[1] for s in SC}
def L(sid, t): return round(t - start[sid], 3)

# ---------------------------------------------------------------- 1 HOOK (avatar)
sid = "hook"; d = 4.15
body = f"""
    <div id="hook-pill" class="pill" style="left:84px;top:268px;height:70px;line-height:70px;padding:0 30px;background:#1d4ed8;color:#f8fafc;font-size:28px;letter-spacing:.12em">ZOHO · NOVEDAD</div>
    <div id="hook-card" class="card" style="left:84px;top:842px;width:912px;height:380px;padding:44px 48px">
      <div style="display:flex;align-items:center;gap:24px">
        {icon("wa", 88, 48)}
        <div>
          <div class="sup" style="font-size:30px;color:#1d4ed8">Zoho Campaigns</div>
          <div style="font-family:Inter;font-weight:500;font-size:28px;color:#475569">Nuevo canal disponible</div>
        </div>
      </div>
      <div class="h" style="font-size:74px;margin-top:40px;white-space:nowrap">
        <span id="hook-w1" style="display:inline-block">ZOHO</span>
        <span id="hook-w2" style="display:inline-block">+ WHATSAPP</span>
        <span id="hook-w3" style="display:inline-block;color:#1d4ed8">+ IA</span>
      </div>
    </div>
"""
js = f"""
    tl.fromTo("#hook-pill", {{opacity:0, rotation:-14, scale:0.8}}, {{opacity:1, rotation:0, scale:1, duration:0.5, ease:"back.out(1.8)"}}, 0.10);
    tl.fromTo("#hook-card", {{opacity:0, y:120, scale:0.92}}, {{opacity:1, y:0, scale:1, duration:0.5, ease:"expo.out"}}, 0.25);
    tl.fromTo("#hook-w1", {{opacity:0.25}}, {{opacity:1, duration:0.15}}, {L(sid, ws(2)):.3f});
    tl.fromTo("#hook-w2", {{opacity:0.25, scale:1.4}}, {{opacity:1, scale:1, duration:0.3, ease:"power4.out"}}, {L(sid, ws(6)):.3f});
    tl.fromTo("#hook-w3", {{opacity:0.25}}, {{opacity:1, duration:0.25}}, {L(sid, ws(8)):.3f});
    {shake("#hook-card", L(sid, ws(6)), 10)}
    tl.to(["#hook-card","#hook-pill"], {{opacity:0, y:-40, duration:0.25, ease:"power3.in"}}, {d-0.3:.3f});
"""
files[sid] = scene_file(sid, d, body, js)

# ---------------------------------------------------------------- 2 CAMPAIGNS (azul)
sid = "campaigns"; d = 6.45 - 4.15
body = f"""
    <div id="campaigns-wrap" class="stage">
      <div id="campaigns-bg" class="bg azul"></div>
      <div id="campaigns-stage" class="stage">
        <div id="campaigns-pill" class="pill" style="left:84px;top:520px;height:84px;line-height:84px;padding:0 38px;background:#00f2fe;color:#0d1b2a;font-size:44px;transform-origin:left center">NOVEDAD</div>
        <div class="h" style="position:absolute;left:84px;right:84px;top:660px;font-size:150px">
          <div id="campaigns-l1">Zoho</div>
          <div id="campaigns-l2">Campaigns,</div>
          <div id="campaigns-l3" class="it" style="font-size:150px">renovado.</div>
        </div>
      </div>
    </div>
"""
js = full_in(sid) + f"""
    tl.fromTo("#campaigns-pill", {{opacity:0, rotation:-18}}, {{opacity:1, rotation:-4, duration:0.5, ease:"back.out(2)"}}, 0.35);
    tl.fromTo("#campaigns-l1", {{opacity:0, filter:"blur(8px)"}}, {{opacity:1, filter:"blur(0px)", duration:0.18}}, {L(sid, ws(11)):.3f});
    tl.fromTo("#campaigns-l3", {{opacity:0, filter:"blur(8px)"}}, {{opacity:1, filter:"blur(0px)", duration:0.18}}, {L(sid, ws(13)):.3f});
    tl.fromTo("#campaigns-l2", {{opacity:0, scale:1.4, transformOrigin:"left center"}}, {{opacity:1, scale:1, duration:0.3, ease:"power4.out"}}, {L(sid, ws(14)):.3f});
"""
files[sid] = scene_file(sid, d, body, js)

# ---------------------------------------------------------------- 3 CHANNELS (oscuro)
sid = "channels"; d = 10.10 - 6.45
tiles = [("mail", "Email", 15), ("sms", "SMS", 16), ("wa", "WhatsApp", 18)]
tiles_html = ""
for k, (ic, lab, wi) in enumerate(tiles):
    x = 84 + k * 312
    tiles_html += f"""
        <div id="channels-t{k}" style="position:absolute;left:{x}px;top:470px;width:288px;height:300px;border-radius:40px;background:#16283d;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:28px">
          {icon(ic, 128, 64)}
          <div class="h" style="font-size:48px">{lab}</div>
        </div>"""
body = f"""
    <div id="channels-wrap" class="stage">
      <div id="channels-bg" class="bg oscuro"></div>
      <div id="channels-stage" class="stage">{tiles_html}
        <div class="h" style="position:absolute;left:84px;right:84px;top:880px;font-size:112px">
          <div id="channels-l1">Desde el</div>
          <div id="channels-l2"><span class="it">mismo sitio.</span></div>
        </div>
        <svg id="channels-ul" viewBox="0 0 600 40" width="600" height="40" style="position:absolute;left:84px;top:1112px;overflow:visible">
          <path d="M6 26 C 150 6, 330 8, 594 20" stroke="#00f2fe" stroke-width="9" fill="none" stroke-linecap="round" pathLength="1" stroke-dasharray="1 1.2" stroke-dashoffset="1.1"/>
        </svg>
      </div>
    </div>
"""
js = full_in(sid, "left")
for k, (ic, lab, wi) in enumerate(tiles):
    js += f"""
    tl.fromTo("#channels-t{k}", {{opacity:0, y:90, scale:0.8}}, {{opacity:1, y:0, scale:1, duration:0.45, ease:"back.out(1.7)"}}, {max(0.2, L(sid, ws(wi))-0.05):.3f});"""
js += f"""
    tl.fromTo("#channels-l1", {{opacity:0, filter:"blur(8px)"}}, {{opacity:1, filter:"blur(0px)", duration:0.18}}, {L(sid, ws(19)):.3f});
    tl.fromTo("#channels-l2", {{opacity:0, scale:1.35, transformOrigin:"left center"}}, {{opacity:1, scale:1, duration:0.3, ease:"power4.out"}}, {L(sid, ws(21)):.3f});
    tl.to("#channels-ul path", {{strokeDashoffset:0, duration:0.4, ease:"power2.out"}}, {L(sid, ws(22)):.3f});
    tl.to(["#channels-t0","#channels-t2"], {{x:(i)=> i===0 ? 40 : -40, duration:0.5, ease:"power2.inOut"}}, {L(sid, ws(21)):.3f});
""" + full_out(sid, d)
files[sid] = scene_file(sid, d, body, js)

# ---------------------------------------------------------------- 4 CRM (avatar, plano cerrado)
sid = "crm"; d = 13.75 - 10.10
body = f"""
    <div id="crm-card" class="card" style="left:84px;top:820px;width:912px;height:420px;padding:44px 48px">
      <div style="display:flex;align-items:center;justify-content:space-between">
        <div class="sup" style="color:#475569;font-size:30px">Audiencias sincronizadas</div>
        <div id="crm-live" class="pill" style="position:relative;height:56px;line-height:56px;padding:0 24px 0 50px;background:#0d1b2a;color:#00f2fe;font-size:28px;letter-spacing:.12em">
          <span id="crm-dot" style="position:absolute;left:22px;top:19px;width:18px;height:18px;border-radius:50%;background:#00f2fe"></span>EN VIVO</div>
      </div>
      <div style="display:flex;align-items:center;gap:26px;margin-top:44px">
        {icon("mail", 100, 52)}
        <div class="h" style="font-size:56px">Campaigns</div>
        <div id="crm-sync" style="margin-left:auto">{icon("sync", 84, 48, extra="background:#eef2f7").replace('stroke:#fff','')}</div>
      </div>
      <div id="crm-row2" style="display:flex;align-items:center;gap:26px;margin-top:30px">
        {icon("users", 100, 52)}
        <div class="h" style="font-size:56px">CRM <span style="font-family:Inter;font-weight:600;font-size:34px;color:#475569;letter-spacing:0">(gestión de clientes)</span></div>
      </div>
    </div>
"""
css = "#crm-sync svg{stroke:#1d4ed8}"
js = f"""
    tl.fromTo("#crm-card", {{opacity:0, y:120, scale:0.92}}, {{opacity:1, y:0, scale:1, duration:0.5, ease:"expo.out"}}, 0.25);
    tl.fromTo("#crm-live", {{opacity:0, rotation:-14, scale:0.7}}, {{opacity:1, rotation:0, scale:1, duration:0.5, ease:"back.out(2)"}}, {L(sid, ws(25))-0.1:.3f});
    tl.fromTo("#crm-dot", {{scale:1}}, {{scale:1.5, duration:0.3, yoyo:true, repeat:5, ease:"sine.inOut"}}, {L(sid, ws(25)):.3f});
    tl.fromTo("#crm-row2", {{opacity:0, x:-40}}, {{opacity:1, x:0, duration:0.4, ease:"expo.out"}}, {L(sid, ws(28))-0.05:.3f});
    tl.fromTo("#crm-sync", {{rotation:0}}, {{rotation:180, duration:0.6, ease:"power2.inOut"}}, {L(sid, ws(28)):.3f});
    tl.to("#crm-card", {{opacity:0, y:-40, duration:0.25, ease:"power3.in"}}, {d-0.3:.3f});
"""
files[sid] = scene_file(sid, d, body, js, css)

# ---------------------------------------------------------------- 5 FLOW (claro)
sid = "flow"; d = 16.60 - 13.75
nodes = [("userplus", "Entra un contacto", 34), ("spark", "Un agente de IA decide", 37), ("wa", "Le escribe por WhatsApp", 39)]
nodes_html = ""
for k, (ic, lab, wi) in enumerate(nodes):
    y = 720 + k * 170
    hl = "background:#1d4ed8;color:#f8fafc" if k == 1 else "background:#ffffff;color:#0d1b2a"
    nodes_html += f"""
        <div id="flow-n{k}" style="position:absolute;left:84px;right:84px;top:{y}px;height:132px;border-radius:36px;{hl};display:flex;align-items:center;gap:28px;padding:0 30px;box-shadow:0 14px 40px rgba(13,27,42,.10)">
          {icon(ic, 84, 46, extra=("background:#0d1b2a" if k == 1 else ""))}
          <div class="h" style="font-size:52px;letter-spacing:-0.02em">{lab}</div>
        </div>"""
body = f"""
    <div id="flow-wrap" class="stage">
      <div id="flow-bg" class="bg claro"></div>
      <div id="flow-stage" class="stage" style="color:#0d1b2a">
        <div class="h" style="position:absolute;left:84px;right:84px;top:400px;font-size:112px">
          <div id="flow-l1">Flujos que mueve</div>
          <div id="flow-l2" style="color:#1d4ed8">un <span class="it">agente.</span></div>
        </div>
        <div id="flow-line" style="position:absolute;left:125px;top:780px;width:6px;height:340px;background:#1d4ed8;border-radius:3px;transform-origin:top center"></div>{nodes_html}
      </div>
    </div>
"""
js = full_in(sid) + f"""
    tl.fromTo("#flow-l1", {{opacity:0, filter:"blur(8px)"}}, {{opacity:1, filter:"blur(0px)", duration:0.18}}, {L(sid, ws(35)):.3f});
    tl.fromTo("#flow-l2", {{opacity:0, scale:1.35, transformOrigin:"left center"}}, {{opacity:1, scale:1, duration:0.3, ease:"power4.out"}}, {L(sid, ws(39)):.3f});
    tl.fromTo("#flow-line", {{scaleY:0}}, {{scaleY:1, duration:1.4, ease:"power2.inOut"}}, {L(sid, ws(35)):.3f});
"""
for k, (ic, lab, wi) in enumerate(nodes):
    js += f"""
    tl.fromTo("#flow-n{k}", {{opacity:0, x:-60}}, {{opacity:1, x:0, duration:0.4, ease:"expo.out"}}, {L(sid, ws(wi))-0.05:.3f});"""
files[sid] = scene_file(sid, d, body, js)

# ---------------------------------------------------------------- 6 THREE (oscuro): 3 herramientas -> 1
sid = "three"; d = 19.75 - 16.60
body = f"""
    <div id="three-wrap" class="stage">
      <div id="three-bg" class="bg oscuro"></div>
      <div id="three-stage" class="stage">
        <div class="h sup" style="position:absolute;left:84px;right:84px;top:400px;font-family:Inter;font-weight:600;font-size:40px;color:#cbd5e1;text-align:center">Lo que antes eran</div>
        <div id="three-num" class="h" style="position:absolute;left:0;right:0;top:470px;height:560px;text-align:center;font-size:540px;line-height:560px;color:#00f2fe"><span id="three-n">0</span></div>
        <div id="three-lab" class="h" style="position:absolute;left:84px;right:84px;top:1060px;text-align:center;font-size:96px">herramientas</div>
        <div id="three-lab2" class="h" style="position:absolute;left:84px;right:84px;top:1060px;text-align:center;font-size:96px;opacity:0">ahora es <span class="it">una.</span></div>
      </div>
    </div>
"""
t_tres = L(sid, ws(46)); t_una = L(sid, ws(50))
js = full_in(sid, "left") + f"""
    const n = {{v:0}};
    tl.fromTo(n, {{v:0}}, {{v:3, duration:{max(0.3, t_tres-0.45):.3f}, ease:"power1.in", onUpdate:()=>{{document.querySelector("#three-n").textContent = Math.round(n.v);}}}}, 0.45);
    tl.fromTo("#three-num", {{scale:1.5}}, {{scale:1, duration:0.3, ease:"power4.out"}}, {t_tres:.3f});
    tl.set("#three-n", {{textContent:"3"}}, {t_tres:.3f});
    {shake("#three-stage", t_tres, 16)}
    tl.fromTo("#three-num", {{x:0, skewX:0}}, {{x:26, skewX:-10, duration:0.034, immediateRender:false}}, {t_una-0.1:.3f});
    tl.to("#three-num", {{x:-18, skewX:6, duration:0.034}}, {t_una-0.066:.3f});
    tl.set("#three-n", {{textContent:"1"}}, {t_una-0.033:.3f});
    tl.to("#three-num", {{x:0, skewX:0, duration:0.034}}, {t_una-0.033:.3f});
    tl.fromTo("#three-num", {{scale:1.6}}, {{scale:1, duration:0.3, ease:"power4.out", immediateRender:false}}, {t_una:.3f});
    tl.to("#three-lab", {{opacity:0, duration:0.15}}, {L(sid, ws(48)):.3f});
    tl.fromTo("#three-lab2", {{opacity:0}}, {{opacity:1, duration:0.18}}, {L(sid, ws(48))+0.1:.3f});
    {shake("#three-stage", t_una, 18)}
""" + full_out(sid, d)
files[sid] = scene_file(sid, d, body, js)

# ---------------------------------------------------------------- 7 PRICE (avatar, plano normal)
sid = "price"; d = 21.45 - 19.75
body = f"""
    <div id="price-card" class="card" style="left:84px;top:900px;width:912px;height:300px;padding:40px 48px;display:flex;flex-direction:column;justify-content:center">
      <div class="sup" style="color:#475569;font-size:32px">Email + SMS + WhatsApp</div>
      <div class="h" style="font-size:96px;margin-top:14px">Mismo <span class="it" style="color:#1d4ed8">precio.</span></div>
    </div>
    <div id="price-pill" class="pill" style="left:640px;top:850px;height:84px;line-height:84px;padding:0 36px;background:#00f2fe;color:#0d1b2a;font-size:44px">+0 €</div>
"""
js = f"""
    tl.fromTo("#price-card", {{opacity:0, y:120, scale:0.92}}, {{opacity:1, y:0, scale:1, duration:0.5, ease:"expo.out"}}, 0.15);
    tl.fromTo("#price-pill", {{opacity:0, rotation:-20, scale:0.6}}, {{opacity:1, rotation:-6, scale:1, duration:0.5, ease:"back.out(2.2)"}}, {L(sid, ws(53)):.3f});
    tl.to(["#price-card","#price-pill"], {{opacity:0, y:-40, duration:0.25, ease:"power3.in"}}, {d-0.3:.3f});
"""
files[sid] = scene_file(sid, d, body, js)

# ---------------------------------------------------------------- 8 REMATE (azul)
sid = "remate"; d = 23.85 - 21.45
body = f"""
    <div id="remate-wrap" class="stage">
      <div id="remate-bg" class="bg azul"></div>
      <div id="remate-stage" class="stage">
        <div class="h" style="position:absolute;left:84px;right:84px;top:520px;font-size:120px">
          <div id="remate-l1">La mayoría</div>
          <div id="remate-l2">no lo va a</div>
          <div id="remate-l3">activar</div>
          <div id="remate-l4"><span class="it" style="font-size:150px">nunca.</span></div>
        </div>
        <svg id="remate-ul" viewBox="0 0 420 40" width="420" height="40" style="position:absolute;left:84px;top:1130px;overflow:visible">
          <path d="M6 22 C 120 8, 260 6, 414 18" stroke="#00f2fe" stroke-width="9" fill="none" stroke-linecap="round" pathLength="1" stroke-dasharray="1 1.2" stroke-dashoffset="1.1"/>
        </svg>
      </div>
    </div>
"""
js = full_in(sid) + f"""
    tl.fromTo("#remate-l1", {{opacity:0, filter:"blur(8px)"}}, {{opacity:1, filter:"blur(0px)", duration:0.15}}, {max(0.3, L(sid, ws(56))):.3f});
    tl.fromTo("#remate-l2", {{opacity:0, filter:"blur(8px)"}}, {{opacity:1, filter:"blur(0px)", duration:0.15}}, {L(sid, ws(58)):.3f});
    tl.fromTo("#remate-l3", {{opacity:0, filter:"blur(8px)"}}, {{opacity:1, filter:"blur(0px)", duration:0.15}}, {L(sid, ws(62)):.3f});
    tl.fromTo("#remate-l4", {{opacity:0, scale:1.5, transformOrigin:"left center"}}, {{opacity:1, scale:1, duration:0.3, ease:"power4.out"}}, {L(sid, ws(63)):.3f});
    tl.to("#remate-ul path", {{strokeDashoffset:0, duration:0.35, ease:"power2.out"}}, {L(sid, ws(63))+0.15:.3f});
    {shake("#remate-stage", L(sid, ws(63)), 16)}
""" + full_out(sid, d)
files[sid] = scene_file(sid, d, body, js)

# ---------------------------------------------------------------- 9 CTA (avatar, plano cerrado)
sid = "cta"; d = 26.70 - 23.85
letters = "ZOHO"
t_kw = L(sid, ws(65))
letters_html = "".join(f'<span id="cta-c{i}" style="display:inline-block">{c}</span>' for i, c in enumerate(letters))
checks = ["Email", "SMS", "WhatsApp"]
chk_html = ""
for k, c in enumerate(checks):
    chk_html += f"""
          <div style="display:flex;align-items:center;gap:18px;margin-top:14px">
            <div style="width:52px;height:52px;border-radius:14px;border:3px solid #1d4ed8;display:flex;align-items:center;justify-content:center">
              <svg id="cta-k{k}" viewBox="0 0 24 24" width="38" height="38" style="stroke:#1d4ed8;fill:none;stroke-width:3;stroke-linecap:round;stroke-linejoin:round">{ICON['check']}</svg>
            </div>
            <div style="font-family:Inter;font-weight:600;font-size:34px">{c}</div>
          </div>"""
body = f"""
    <div id="cta-say" class="h" style="position:absolute;left:84px;top:800px;font-size:64px;text-shadow:0 4px 20px rgba(13,27,42,.6)">Escríbeme</div>
    <div id="cta-bubble" style="position:absolute;left:84px;top:885px;height:130px;min-width:120px;padding:0 48px;background:#1d4ed8;border-radius:40px 40px 40px 10px;display:flex;align-items:center;box-shadow:0 18px 40px rgba(13,27,42,.4)">
      <div class="h" style="font-size:84px;letter-spacing:.04em">{letters_html}<span id="cta-caret" style="display:inline-block;width:6px;height:70px;background:#f8fafc;margin-left:8px;vertical-align:-6px"></span></div>
    </div>
    <div id="cta-card" class="card" style="left:500px;top:1000px;width:496px;height:270px;padding:28px 34px;border-radius:36px">
      <div class="sup" style="font-size:28px;color:#475569">Te enseño a montar</div>{chk_html}
    </div>
"""
js = f"""
    tl.fromTo("#cta-say", {{opacity:0, filter:"blur(8px)"}}, {{opacity:1, filter:"blur(0px)", duration:0.2}}, {max(0.2, L(sid, ws(64))):.3f});
    tl.fromTo("#cta-bubble", {{opacity:0, scale:0.6, transformOrigin:"left bottom"}}, {{opacity:1, scale:1, duration:0.4, ease:"back.out(1.8)"}}, {L(sid, ws(64))+0.25:.3f});
"""
for i in range(4):
    js += f"""
    tl.fromTo("#cta-c{i}", {{opacity:0}}, {{opacity:1, duration:0.01}}, {t_kw - 0.05 + i*0.09:.3f});"""
js += f"""
    tl.fromTo("#cta-caret", {{opacity:1}}, {{opacity:0, duration:0.01}}, {t_kw+0.5:.3f});
    tl.fromTo("#cta-card", {{opacity:0, y:80, scale:0.9}}, {{opacity:1, y:0, scale:1, duration:0.45, ease:"expo.out"}}, {L(sid, ws(65))+0.3:.3f});
"""
for k in range(3):
    js += f"""
    tl.fromTo("#cta-k{k}", {{opacity:0, scale:0}}, {{opacity:1, scale:1, duration:0.35, ease:"back.out(2.2)"}}, {L(sid, ws(65)) + 0.55 + k*0.24:.3f});"""
js += f"""
    tl.to(["#cta-say","#cta-bubble","#cta-card"], {{opacity:0, duration:0.2}}, {d-0.22:.3f});
"""
files[sid] = scene_file(sid, d, body, js)

# ---------------------------------------------------------------- 10 CIERRE (azul)
sid = "cierre"; d = TOTAL - 26.70
body = f"""
    <div id="cierre-wrap" class="stage">
      <div id="cierre-bg" class="bg azul"></div>
      <div id="cierre-stage" class="stage">
        <div id="cierre-card" class="card" style="left:84px;top:360px;width:912px;height:820px;border-radius:60px;padding:64px 60px">
          <div class="sup" style="color:#475569;font-size:34px">¿Tienes Zoho?</div>
          <div class="h" style="font-size:96px;margin-top:22px">Email, SMS y WhatsApp en <span class="it" style="color:#1d4ed8">un sitio.</span></div>
          <div id="cierre-btn" style="margin-top:56px;height:120px;border-radius:999px;background:#1d4ed8;color:#f8fafc;display:flex;align-items:center;justify-content:center" class="h">
            <span style="font-size:56px">Escríbeme&nbsp;</span><span style="font-size:56px;color:#00f2fe">ZOHO</span>
          </div>
          <div style="font-family:Inter;font-weight:500;font-size:32px;color:#475569;margin-top:26px;text-align:center">y te enseño cómo montarlo</div>
          <div class="h" style="font-size:40px;margin-top:40px;text-align:center;letter-spacing:-0.01em">agfconecta.com</div>
        </div>
        <div id="cierre-logo" style="position:absolute;left:290px;top:1215px;width:500px;height:230px;border-radius:28px;background:#0d1b2a;display:flex;align-items:center;justify-content:center">
          <img src="assets/logo-agf-completo.png" alt="AGF Conecta" style="width:400px;height:auto;display:block"/>
        </div>
      </div>
    </div>
"""
js = full_in(sid) + f"""
    tl.fromTo("#cierre-card", {{opacity:0, y:140, scale:0.92}}, {{opacity:1, y:0, scale:1, duration:0.55, ease:"expo.out"}}, 0.3);
    tl.fromTo("#cierre-btn", {{scale:1.25}}, {{scale:1, duration:0.4, ease:"back.out(1.8)"}}, 0.75);
    tl.fromTo("#cierre-logo", {{opacity:0, y:60}}, {{opacity:1, y:0, duration:0.5, ease:"expo.out"}}, 0.85);
"""
files[sid] = scene_file(sid, d, body, js)

# ---------------------------------------------------------------- SUBTÍTULOS
GROUPS = [
    ([0,1,2], 2), ([3,4,5,6], 6), ([7,8,9,10], 10),
    ([11,12,13,14], 14), ([15,16,17,18], 18), ([19,20,21,22], 22),
    ([23,24,25], 25), ([26,27,28], 28), ([29,30,31,32], 32),
    ([33,34,35,36,37], 35), ([38,39,40,41], 41),
    ([42,43,44,45,46], 46), ([47,48,49,50], 50),
    ([51,52,53,54,55], 53), ([56,57,58,59], 57), ([60,61,62,63], 63),
    ([64,65], 65), ([66,67,68,69,70], 70),
]
light_scenes = []  # todas las frases llevan placa, el acento es siempre cian
cap_html = ""; cap_js = ""; groups_meta = []
for gi, (idx, kw) in enumerate(GROUPS):
    g_start = round(ws(idx[0]) - 0.08, 3)
    nxt = ws(GROUPS[gi+1][0][0]) - 0.08 if gi + 1 < len(GROUPS) else we(idx[-1]) + 0.4
    g_end = round(min(nxt, we(idx[-1]) + 0.6), 3)
    spans = ""
    for i in idx:
        txt = W[i]["text"]
        col = "color:#00f2fe;" if i == kw else ""
        spans += f'<span id="cw{i}" class="cw" style="{col}">{txt}</span> '
    text = " ".join(W[i]["text"] for i in idx)
    cap_html += f"""
    <div id="cg{gi}" class="cg" style="opacity:0"><div class="plate"><span class="ct" data-text="{text}">{spans.strip()}</span></div></div>"""
    cap_js += f"""
    tl.fromTo("#cg{gi}", {{opacity:0, y:14}}, {{opacity:1, y:0, duration:0.12, ease:"power2.out"}}, {g_start:.3f});"""
    for i in idx:
        cap_js += f"""
    tl.fromTo("#cw{i}", {{opacity:0.3}}, {{opacity:1, duration:0.06}}, {ws(i):.3f});"""
    cap_js += f"""
    tl.to("#cg{gi}", {{opacity:0, duration:0.12, ease:"power2.in"}}, {g_end-0.12:.3f});
    tl.set("#cg{gi}", {{opacity:0, visibility:"hidden"}}, {g_end:.3f});"""

cap_css = """
#root{position:absolute;inset:0;pointer-events:none}
.cg{position:absolute;left:84px;right:84px;top:1290px;text-align:center;overflow:visible}
.plate{display:inline-block;background:rgba(13,27,42,0.62);border-radius:26px;padding:10px 26px}
.ct{font-family:'Outfit';font-weight:700;font-size:70px;line-height:1.06;letter-spacing:-0.02em;color:#f8fafc;text-shadow:0 2px 12px rgba(0,0,0,.35)}
.cw{opacity:.3}
"""
files["captions"] = f"""<template>
  <style>{cap_css}</style>
  <div id="root" data-composition-id="captions" data-width="1080" data-height="1920">{cap_html}
  </div>
  <script>
    (function(){{
    document.querySelectorAll("#root .ct").forEach((el)=>{{
      if (window.__hyperframes && window.__hyperframes.fitTextFontSize) {{
        const r = window.__hyperframes.fitTextFontSize(el.dataset.text, {{fontFamily:"Outfit", fontWeight:700, maxWidth:860, baseFontSize:70, minFontSize:52, step:2}});
        if (r && r.fontSize) el.style.fontSize = Math.min(70, r.fontSize) + "px";
      }}
    }});
    const tl = gsap.timeline({{ paused: true }});
{cap_js}
    window.__timelines["captions"] = tl;
    }})();
  </script>
</template>
"""

# ---------------------------------------------------------------- AUDIO
def at_peak(t_visual, peak):  # el pico cae un fotograma después de la imagen
    return round(max(0, t_visual + 1/FPS - peak), 3)
SFX = []
SFX.append(("notif", at_peak(0.30, 0.045), 0.32))
whooshes = []
for k, (s_id, s0, s1, kind) in enumerate(SC[1:], start=1):
    f, pk = ("whoosh1", 0.53) if k % 2 else ("whoosh2", 0.345)
    SFX.append((f, at_peak(s0 + 0.2, pk), 0.28))
for wi in (15, 16, 18):
    SFX.append(("notif", at_peak(ws(wi), 0.045), 0.17))
SFX.append(("notif", at_peak(10.10 + 0.3, 0.045), 0.32))
SFX.append(("impact", at_peak(ws(46), 0.35), 0.5))
SFX.append(("glitch", at_peak(ws(50) - 0.1, 0.67), 0.34))
SFX.append(("notif", at_peak(19.75 + 0.15, 0.045), 0.32))
SFX.append(("impact", at_peak(ws(63), 0.35), 0.5))
SFX.append(("notif", at_peak(ws(64) + 0.3, 0.045), 0.32))
for k in range(3):
    SFX.append(("notif", at_peak(ws(65) + 0.55 + k*0.24, 0.045), 0.17))
SFX.append(("notif", at_peak(26.70 + 0.35, 0.045), 0.32))
SFX.sort(key=lambda x: x[1])
# separación mínima 0,22 s entre efectos del mismo tipo
last = {}
clean = []
for f, t, v in SFX:
    if f in last and t - last[f] < 0.22:
        t = round(last[f] + 0.22, 3)
    last[f] = t; clean.append((f, t, v))
SFX = clean
DUR = {"notif":0.72, "whoosh1":1.58, "whoosh2":1.285, "impact":3.454, "glitch":1.372}
audio_html = ""
for k, (f, t, v) in enumerate(SFX):
    dd = min(DUR[f], TOTAL - t - 0.01)
    audio_html += f"""
      <audio id="sfx{k}" class="clip" src="assets/{f}.wav" data-start="{t}" data-duration="{dd:.3f}" data-volume="{v}" data-track-index="{20+k}"></audio>"""

# ---------------------------------------------------------------- INDEX
hosts = ""
for k, (s_id, s0, s1, kind) in enumerate(SC):
    e = s1
    if kind == "full" and k + 1 < len(SC) and SC[k+1][3] == "full":
        e = s1 + OVERLAP
    e = min(e, TOTAL)
    hosts += f"""
      <div id="{s_id}" data-composition-id="{s_id}" data-composition-src="compositions/{s_id}.html" data-start="{s0}" data-duration="{e-s0:.3f}" data-track-index="{3+k}" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index:{10+k}"></div>"""

index = f"""<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin:0; padding:0; box-sizing:border-box; }}
      html, body {{ margin:0; width:1080px; height:1920px; overflow:hidden; background:#0d1b2a; }}
      #root {{ position:relative; width:1080px; height:1920px; overflow:hidden; font-family:'Outfit',sans-serif; }}
      #ground {{ position:absolute; inset:0; background:#0d1b2a; }}
      #cam {{ position:absolute; inset:0; transform-origin:50% 28%; }}
      #avatar {{ position:absolute; left:0; top:0; width:1080px; height:1920px; object-fit:cover; }}
      #shade {{ position:absolute; left:0; right:0; bottom:0; height:960px; background:linear-gradient(to top, rgba(13,27,42,.55) 0%, rgba(13,27,42,0) 100%); z-index:2; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-fps="{FPS}" data-width="1080" data-height="1920">
      <div id="ground"></div>
      <div id="cam">
        <video id="avatar" class="clip" src="assets/avatar.mp4" muted playsinline data-start="0" data-duration="26.8" data-track-index="0"></video>
      </div>
      <div id="shade"></div>{hosts}
      <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{TOTAL}" data-track-index="2" data-track-kind="captions" data-width="1080" data-height="1920" style="z-index:40"></div>
      <audio id="voice" class="clip" src="assets/voice.wav" data-start="0" data-duration="26.8" data-volume="1" data-track-index="1"></audio>
      <audio id="music" class="clip" src="assets/music.wav" data-start="0" data-duration="{TOTAL}" data-volume="0.15" data-fade-in="0.4" data-fade-out="1.4" data-track-index="19"></audio>{audio_html}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      // cortes de cámara simulados en cada vuelta a Germán
      tl.set("#cam", {{scale:1.0}}, 0);
      tl.set("#cam", {{scale:1.14}}, 10.10);
      tl.set("#cam", {{scale:1.0}}, 19.75);
      tl.set("#cam", {{scale:1.14}}, 23.85);
      tl.fromTo("#ground", {{opacity:1}}, {{opacity:1, duration:{TOTAL-0.01}}}, 0);
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""

open(os.path.join(P, "index.html"), "w").write(index)
for k, v in files.items():
    open(os.path.join(P, "compositions", f"{k}.html"), "w").write(v)
print("ok", len(files), "compositions;", len(SFX), "sfx")
