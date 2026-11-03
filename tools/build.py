#!/usr/bin/env python3
"""Build the BRAQON profile: every SVG in assets/ plus README.md and README.es.md.

Edit the content in this file, then run:  python3 tools/build.py
Nothing here needs third-party packages; the output is plain SVG and Markdown.
"""

import json
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
USER = "braqon"
EMAIL = "bquintianromero@gmail.com"
W = 1200

MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"

THEMES = {
    "dark": dict(bg="#0d1117", panel="#161b22", border="#30363d", fg="#e6edf3",
                 muted="#8b949e", accent="#00b4d8", soft="#90e0ef"),
    "light": dict(bg="#ffffff", panel="#f6f8fa", border="#d0d7de", fg="#1f2328",
                  muted="#59636e", accent="#0077b6", soft="#00b4d8"),
}

# Official brand icons (24x24 paths) from Simple Icons 13.0.0, CC0: https://simpleicons.org
ICONS = json.loads((Path(__file__).resolve().parent / "icons.json").read_text())
# Brand colors; None means "use the theme's text color" (GitHub and X are black/white marks).
ICON_COLORS = {"github": None, "linkedin": "#0A66C2", "gmail": "#EA4335",
               "instagram": "#E4405F", "x": None, "youtube": "#FF0000"}

# Contact buttons: (file, label, url, icon). Drawn as our own SVG pills so they match the theme.
LINKS = [
    ("github", "GITHUB", f"https://github.com/{USER}", "github"),
    ("linkedin", "LINKEDIN", "https://linkedin.com/in/braian-quintian", "linkedin"),
    ("email", "EMAIL", f"mailto:{EMAIL}", "gmail"),
    ("instagram", "INSTAGRAM", "https://www.instagram.com/braian.qloq/", "instagram"),
]
BRAND_LINKS = [
    ("b-github", "BRAQON-DEV", "https://github.com/braqon-dev", "github"),
    ("b-x", "@BRAQONDEV", "https://x.com/braqondev", "x"),
    ("b-linkedin", "BRAQON", "https://www.linkedin.com/company/braqon/", "linkedin"),
    ("b-youtube", "@BRAQON", "https://www.youtube.com/@braqon", "youtube"),
    ("b-instagram", "@BRAQONDEV", "https://www.instagram.com/braqondev/", "instagram"),
]

# ── Content ──────────────────────────────────────────────────────────────────

T = {
    "en": dict(
        tagline="Braian Quintian · Founder @ BRAQON · CTO @ 88Pay",
        sub="full-stack · payments · cloud & security · Colombia",
        prompt="building one API for every way LATAM pays",
        now_1="Leading engineering at 88Pay: one API for the ways Latin America pays.",
        now_2="shipping → payment APIs · infrastructure as code · security engineering",
        sections=[
            ("whoami", "// who's behind the keyboard"),
            ("payment rails", "// one contract on top, many edge cases below"),
            ("stack", "// tools I reach for"),
            ("building", "// open source under BRAQON"),
            ("telemetry", "// numbers, because engineers love numbers"),
            ("off-keyboard", "// the human part"),
        ],
        hub="one API",
        hub_sub="REST · webhooks",
        rails=[
            ("Bank transfers", "account to account"),
            ("Instant payments", "real-time rails"),
            ("Digital wallets", "mobile-first"),
            ("Mobile payments", "pay with a phone number"),
            ("Cash", "pay in person"),
            ("Cards", "debit · credit"),
            ("Crypto", "stablecoins"),
            ("Your rail next?", "let's talk →"),
        ],
        express_desc=["Versioned routes and APIs for Express.js,", "so /v1 and /v2 live together in peace."],
        express_meta="npm · JSR · GitHub Packages",
        braqon_desc=["Open-source payments, POS and", "developer tools from Latin America."],
        braqon_meta="POS · coming soon",
        view="view →",
        footer_1="thanks for scrolling, see you in the next commit",
    ),
    "es": dict(
        tagline="Braian Quintian · Founder @ BRAQON · CTO @ 88Pay",
        sub="full-stack · pagos · cloud y seguridad · Colombia",
        prompt="construyendo una API para cada forma de pagar en LATAM",
        now_1="Lidero ingeniería en 88Pay: una API para las formas de pagar en Latinoamérica.",
        now_2="enviando → APIs de pago · infraestructura como código · ingeniería de seguridad",
        sections=[
            ("whoami", "// quién está detrás del teclado"),
            ("rieles de pago", "// un contrato arriba, muchos casos borde abajo"),
            ("stack", "// las herramientas que uso"),
            ("construyendo", "// open source bajo BRAQON"),
            ("telemetría", "// números, porque a los ingenieros nos encantan"),
            ("fuera del teclado", "// la parte humana"),
        ],
        hub="una API",
        hub_sub="REST · webhooks",
        rails=[
            ("Transferencias", "cuenta a cuenta"),
            ("Pagos inmediatos", "en tiempo real"),
            ("Billeteras digitales", "mobile-first"),
            ("Pagos móviles", "con número de celular"),
            ("Efectivo", "pago presencial"),
            ("Tarjetas", "débito · crédito"),
            ("Cripto", "stablecoins"),
            ("¿Tu riel sigue?", "hablemos →"),
        ],
        express_desc=["Rutas y APIs versionadas para Express.js,", "para que /v1 y /v2 convivan en paz."],
        express_meta="npm · JSR · GitHub Packages",
        braqon_desc=["Pagos, POS y herramientas para", "devs, open source y hechas en LATAM."],
        braqon_meta="POS · muy pronto",
        view="ver →",
        footer_1="gracias por llegar hasta aquí, nos vemos en el próximo commit",
    ),
}

# ── SVG helpers ──────────────────────────────────────────────────────────────

def e(text):
    return escape(text, {'"': "&quot;"})


def svg(height, body, c, css="", width=W):
    style = (
        "<style>"
        ".blink{animation:blink 1.1s steps(1) infinite}"
        "@keyframes blink{50%{opacity:0}}"
        f"{css}"
        "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"
        "</style>"
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" fill="none" role="img">{style}{body}</svg>\n'
    )


def panel(x, y, w, h, c, rx=14, fill=None, dashed=False, stroke=None):
    dash = ' stroke-dasharray="6 6"' if dashed else ""
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
            f'fill="{fill or c["panel"]}" stroke="{stroke or c["border"]}"{dash}/>')


def text(x, y, s, c, size=16, color=None, font=SANS, weight=400, anchor="start", extra=""):
    return (f'<text x="{x}" y="{y}" font-family="{e(font)}" font-size="{size}" '
            f'font-weight="{weight}" fill="{color or c["fg"]}" text-anchor="{anchor}"{extra}>'
            f"{s}</text>")


def chip(x, y, label, c, dashed=False, size=14):
    w = len(label) * size * 0.61 + 28
    dash = ' stroke-dasharray="4 4"' if dashed else ""
    return (f'<rect x="{x}" y="{y}" width="{w:.0f}" height="32" rx="16" fill="{c["bg"]}" '
            f'stroke="{c["border"]}"{dash}/>'
            + text(x + w / 2, y + 21, e(label), c, size=size, color=c["muted"] if dashed else c["fg"],
                   font=MONO, anchor="middle")), w


# Geometric stroke glyphs for the BRAQON wordmark (cap height 100, stroke 13).
S = 13
h = S / 2
GLYPHS = {
    # One continuous stroke so every corner is a join (no notch where strokes meet).
    "B": (73, [f"M{h},50H44A21.75,21.75 0 0 1 44,{100-h}H{h}V{h}H40A21.75,21.75 0 0 1 40,50H{h}"]),
    "R": (74, [f"M{h},{100-h}V{h}H40A21.75,21.75 0 0 1 40,50H{h}", f"M36,50L70,{100-h}"]),
    "A": (84, [f"M3,{100-h}L42,{h}L81,{100-h}", "M21,68H63"]),
    "Q": (100, ["circle", "M62,66L93,97"]),
    "O": (100, ["circle"]),
    "N": (78, [f"M{h},{100-h}V{h}L{78-h},{100-h}V{h}"]),
}


def wordmark(word, c, x, y, scale, color=None):
    parts, cursor, i = [], 0, 0
    for ch in word:
        width, strokes = GLYPHS[ch]
        for stroke in strokes:
            delay = f'style="animation-delay:{0.12 * i:.2f}s"'
            if stroke == "circle":
                parts.append(f'<circle class="g" {delay} cx="{cursor + 50}" cy="50" r="{50 - h}" pathLength="1"/>')
            else:
                parts.append(f'<path class="g" {delay} transform="translate({cursor},0)" d="{stroke}" pathLength="1"/>')
            i += 1
        cursor += width + 14
    return (f'<g transform="translate({x},{y}) scale({scale})" stroke="{color or c["fg"]}" '
            f'stroke-width="{S}" stroke-linejoin="round" fill="none">{"".join(parts)}</g>'), cursor - 14


# Drawn by default; the animation only hides strokes while it runs, so a viewer
# without CSS animation still sees the full wordmark.
DRAW_CSS = (".g{stroke-dasharray:1;stroke-dashoffset:0;animation:draw 1.1s cubic-bezier(.6,0,.2,1) backwards}"
            "@keyframes draw{from{stroke-dashoffset:1}to{stroke-dashoffset:0}}")

# ── Assets ───────────────────────────────────────────────────────────────────

def hero(t, c):
    height = 340
    scale = 0.9
    _, width = wordmark("BRAQON", c, 0, 0, 1)
    mark, _ = wordmark("BRAQON", c, (W - width * scale) / 2, 58, scale)
    body = (
        '<defs><pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse">'
        f'<circle cx="2" cy="2" r="1" fill="{c["border"]}"/></pattern>'
        f'<radialGradient id="glow" cx="50%" cy="0%" r="70%"><stop offset="0" stop-color="{c["accent"]}" stop-opacity=".22"/>'
        f'<stop offset="1" stop-color="{c["accent"]}" stop-opacity="0"/></radialGradient></defs>'
        + panel(1, 1, W - 2, height - 2, c, rx=18, fill=c["bg"])
        + f'<rect x="1" y="1" width="{W-2}" height="{height-2}" rx="18" fill="url(#dots)" opacity=".6"/>'
        + f'<rect x="1" y="1" width="{W-2}" height="{height-2}" rx="18" fill="url(#glow)"/>'
        + mark
        + text(W / 2, 212, e(t["tagline"]), c, size=26, weight=600, anchor="middle")
        + text(W / 2, 244, e(t["sub"]), c, size=16, color=c["muted"], font=MONO, anchor="middle")
        + f'<text x="{W/2}" y="296" font-family="{e(MONO)}" font-size="17" text-anchor="middle">'
          f'<tspan fill="{c["accent"]}">{USER}@github</tspan><tspan fill="{c["muted"]}">:~$ </tspan>'
          f'<tspan fill="{c["fg"]}">{e(t["prompt"])}</tspan><tspan class="blink" fill="{c["accent"]}"> ▋</tspan></text>'
    )
    return svg(height, body, c, DRAW_CSS)


def button(label, c, active=False, icon=None):
    """A pill-shaped link button (height 44) with the brand's official icon when given."""
    start = 48 if icon else 36
    width = round(start + len(label) * 9.4 + 22)
    fill = c["accent"] if active else c["panel"]
    fg = c["bg"] if active else c["fg"]
    body = f'<rect x="1" y="1" width="{width-2}" height="42" rx="21" fill="{fill}" stroke="{c["accent"] if active else c["border"]}"/>'
    if icon:
        color = ICON_COLORS[icon] or c["fg"]
        body += f'<path transform="translate(16,12) scale(0.8333)" fill="{color}" d="{ICONS[icon]}"/>'
    else:
        body += f'<circle cx="22" cy="22" r="4" fill="{c["bg"] if active else c["accent"]}"/>'
    body += text(start, 27, e(label), c, size=14, color=fg, font=MONO, weight=700, extra=' letter-spacing="1.5"')
    return svg(44, body, c, width=width)


def now(t, c):
    body = (
        panel(1, 1, W - 2, 126, c)
        + f'<circle cx="40" cy="38" r="6" fill="{c["accent"]}"/>'
        + f'<circle cx="40" cy="38" r="6" fill="none" stroke="{c["accent"]}" stroke-width="2">'
          '<animate attributeName="r" values="6;16" dur="1.8s" repeatCount="indefinite"/>'
          '<animate attributeName="opacity" values="1;0" dur="1.8s" repeatCount="indefinite"/></circle>'
        + text(60, 43, "NOW", c, size=14, color=c["accent"], font=MONO, weight=700, extra=' letter-spacing="3"')
        + text(32, 80, e(t["now_1"]), c, size=21, weight=600)
        + text(32, 108, e(t["now_2"]), c, size=15, color=c["muted"], font=MONO)
    )
    return svg(128, body, c)


def section(n, title, comment, c):
    body = (
        f'<defs><linearGradient id="rule" x1="0" x2="1"><stop offset="0" stop-color="{c["accent"]}"/>'
        f'<stop offset="1" stop-color="{c["accent"]}" stop-opacity="0"/></linearGradient></defs>'
        + text(0, 50, f"{n:02d}", c, size=30, color=c["accent"], font=MONO, weight=700)
        + text(62, 50, e(title), c, size=30, weight=700)
        + text(W, 50, e(comment), c, size=15, color=c["muted"], font=MONO, anchor="end")
        + f'<rect x="0" y="70" width="{W}" height="2" fill="url(#rule)"/>'
    )
    return svg(84, body, c)


def rails(t, c):
    height = 460
    hx, hy, hr = W / 2, 232, 78
    ys = [40, 145, 250, 355]
    parts = []
    for i, (title, sub) in enumerate(t["rails"]):
        left = i < 4
        y = ys[i % 4]
        cy = y + 35
        x = 60 if left else 840
        last = i == len(t["rails"]) - 1
        if left:
            path = f"M360,{cy} C480,{cy} 470,{hy} {hx - hr},{hy}"
        else:
            path = f"M840,{cy} C720,{cy} 730,{hy} {hx + hr},{hy}"
        parts.append(f'<path d="{path}" stroke="{c["border"]}" stroke-width="2"'
                     f'{" stroke-dasharray=\"5 6\"" if last else ""}/>')
        if not last:
            parts.append(f'<circle r="4" fill="{c["accent"]}"><animateMotion dur="2.8s" '
                         f'begin="-{i * 0.35:.2f}s" repeatCount="indefinite" path="{path}"/></circle>')
        parts.append(panel(x, y, 300, 70, c, rx=12, dashed=last,
                           stroke=c["accent"] if last else None,
                           fill=c["bg"] if last else None))
        parts.append(text(x + 20, y + 30, e(title), c, size=18, weight=700,
                          color=c["accent"] if last else None))
        parts.append(text(x + 20, y + 54, e(sub), c, size=14, color=c["muted"], font=MONO))
    hub = (
        f'<circle cx="{hx}" cy="{hy}" r="{hr}" fill="none" stroke="{c["accent"]}" stroke-width="2">'
        f'<animate attributeName="r" values="{hr};{hr + 26}" dur="2.4s" repeatCount="indefinite"/>'
        '<animate attributeName="opacity" values=".7;0" dur="2.4s" repeatCount="indefinite"/></circle>'
        f'<circle cx="{hx}" cy="{hy}" r="{hr}" fill="{c["panel"]}" stroke="{c["accent"]}" stroke-width="2"/>'
        + text(hx, hy - 2, e(t["hub"]), c, size=24, weight=700, anchor="middle")
        + text(hx, hy + 24, e(t["hub_sub"]), c, size=13, color=c["muted"], font=MONO, anchor="middle")
    )
    return svg(height, "".join(parts) + hub, c)



def project_card(title, desc, meta, c, view, mark=False, live=True):
    width, height = 588, 220
    parts = [panel(1, 1, width - 2, height - 2, c, stroke=c["accent"] if live else None)]
    if mark:
        logo, _ = wordmark("BRAQON", c, 30, 34, 0.3)
        parts.append(logo)
    else:
        parts.append(text(30, 62, e(title), c, size=24, color=c["accent"], font=MONO, weight=700))
    parts.append(text(width - 30, 60, e(view), c, size=14, color=c["muted"], font=MONO, anchor="end"))
    parts.append(text(30, 112, e(desc[0]), c, size=17))
    parts.append(text(30, 138, e(desc[1]), c, size=17, color=c["muted"]))
    dot = c["accent"] if live else c["muted"]
    parts.append(f'<circle cx="36" cy="182" r="5" fill="{dot}"/>')
    parts.append(text(50, 187, e(meta), c, size=14, color=dot, font=MONO))
    return svg(height, "".join(parts), c, width=width)


# macOS-style terminal: commands type themselves, outputs appear, then it loops.
# SMIL keeps it working inside GitHub's <img>; without animation it shows the final screen.
TERM_SCRIPT = {
    "en": [
        ("whoami", [("Braian Quintian · Founder @ ", "fg"), ("BRAQON", "accent"), (" · CTO @ 88Pay · Colombia", "fg")]),
        ("ls ~/braqon-dev", [("express-version-api", "accent"), ("    braqon-pos ", "fg"), ("(soon)", "muted"),
                             ("    payments-toolkit ", "fg"), ("(lab)", "muted")]),
        ("cat stack.txt", [("TypeScript · NestJS · Next.js · Angular · AWS · Terraform · Docker", "fg")]),
        ("npx braqon", [("→ ", "green"), ("my business card, right in your terminal. go on, run it.", "fg")]),
    ],
    "es": [
        ("whoami", [("Braian Quintian · Founder @ ", "fg"), ("BRAQON", "accent"), (" · CTO @ 88Pay · Colombia", "fg")]),
        ("ls ~/braqon-dev", [("express-version-api", "accent"), ("    braqon-pos ", "fg"), ("(pronto)", "muted"),
                             ("    payments-toolkit ", "fg"), ("(lab)", "muted")]),
        ("cat stack.txt", [("TypeScript · NestJS · Next.js · Angular · AWS · Terraform · Docker", "fg")]),
        ("npx braqon", [("→ ", "green"), ("mi tarjeta de presentación en tu terminal. dale, córrelo.", "fg")]),
    ],
}


def terminal(lang, c):
    script = TERM_SCRIPT[lang]
    size, lh, cw = 17, 30, 17 * 0.602        # font size, line height, monospace char width
    top, left = 44, 28                        # title bar height, text inset
    prompt = f"{USER}@mac ~ % "
    height = top + 24 + lh * (2 + 2 * len(script)) + 14
    think, enter, respond, settle, hold = 1.0, 0.5, 0.18, 0.3, 5.0

    def keystrokes(cmd, i):
        """Human-ish rhythm: uneven per-key delays, a beat after spaces and symbols."""
        delays = []
        for k, ch in enumerate(cmd):
            d = 0.06 + ((k * 37 + i * 11 + ord(ch)) % 7) * 0.017
            if k and cmd[k - 1] in " ~/.-":
                d += 0.09
            delays.append(d)
        return delays

    # Build the timeline first so every animation shares one loop length.
    t, events = 0.9, []
    for i, (cmd, _) in enumerate(script):
        prompt_at = t
        start = prompt_at + (think + 0.3 if i == 0 else think)
        times, s = [], start
        for d in keystrokes(cmd, i):
            s += d
            times.append(s)
        out_at = s + enter + respond
        events.append(dict(prompt=prompt_at, start=start, keys=times, enter=s + enter, out=out_at))
        t = out_at + settle
    total = t + hold

    def kt(s):
        return f"{s / total:.4f}"

    def anim(attr, values, times):
        return (f'<animate attributeName="{attr}" calcMode="discrete" values="{";".join(values)}" '
                f'keyTimes="{";".join(times)}" dur="{total:.2f}s" repeatCount="indefinite"/>')

    def appear(s):
        return anim("opacity", ["0", "1"], ["0", kt(s)])

    def cursor_anim(ev, x0):
        # Blinks while "thinking" at the prompt, stays solid while typing, gone after Enter.
        vals, times, s, on = ["0"], ["0"], ev["prompt"], True
        while s < ev["start"]:
            vals.append("1" if on else "0"); times.append(kt(s)); s += 0.5; on = not on
        vals += ["1", "0"]; times += [kt(ev["start"]), kt(ev["enter"])]
        xs = [f"{x0:.1f}"] + [f"{x0 + (k + 1) * cw:.1f}" for k in range(len(ev["keys"]))]
        xt = ["0"] + [kt(s) for s in ev["keys"]]
        return anim("opacity", vals, times) + anim("x", xs, xt)

    def tspans(parts):
        colors = {"fg": c["fg"], "muted": c["muted"], "accent": c["accent"], "green": "#28c840"}
        return "".join(f'<tspan fill="{colors[k]}">{e(s)}</tspan>' for s, k in parts)

    def line(y, inner, extra=""):
        return (f'<text x="{left}" y="{y}" font-family="{e(MONO)}" font-size="{size}" '
                f'xml:space="preserve"{extra}>{inner}</text>')

    def prompt_spans():
        return (f'<tspan fill="{c["accent"]}">{USER}@mac</tspan>'
                f'<tspan fill="{c["fg"]}"> ~ </tspan><tspan fill="{c["muted"]}">% </tspan>')

    login = "Last login: Mon Nov  2 09:41:07 on ttys001" if lang == "en" else "Último acceso: lun 2 nov 09:41:07 en ttys001"
    y = top + 24 + lh * 0.7
    body = [line(y, f'<tspan fill="{c["muted"]}">{e(login)}</tspan>')]
    x0 = left + len(prompt) * cw
    block = (cw - 1, size + 3)
    for i, ((cmd, out), ev) in enumerate(zip(script, events)):
        y += lh
        n = len(cmd)
        widths = ["0"] + [f"{(k + 1) * cw:.1f}" for k in range(n)]
        times = ["0"] + [kt(s) for s in ev["keys"]]
        body.append(
            f'<clipPath id="type{i}"><rect x="{x0 - 1:.1f}" y="{y - size - 4:.0f}" height="{lh}" width="{n * cw + 2:.1f}">'
            f'{anim("width", widths, times)}</rect></clipPath>'
            f'<g>{appear(ev["prompt"])}{line(y, prompt_spans())}'
            f'<text x="{x0:.1f}" y="{y}" font-family="{e(MONO)}" font-size="{size}" fill="{c["fg"]}" '
            f'clip-path="url(#type{i})">{e(cmd)}</text></g>'
            f'<rect x="{x0 + n * cw:.1f}" y="{y - size + 1:.0f}" width="{block[0]:.1f}" height="{block[1]}" '
            f'fill="{c["accent"]}" opacity="0">{cursor_anim(ev, x0)}</rect>')
        y += lh
        body.append(f'<g>{appear(ev["out"])}{line(y, tspans(out))}</g>')
    y += lh
    body.append(
        f'<g>{appear(t)}{line(y, prompt_spans())}'
        f'<rect class="blink" x="{x0:.1f}" y="{y - size + 1:.0f}" width="{block[0]:.1f}" height="{block[1]}" '
        f'fill="{c["accent"]}"/></g>')

    title = f"{USER} — -zsh — 80×24"
    chrome = (
        f'<rect x="1" y="1" width="{W - 2}" height="{height - 2}" rx="12" fill="{c["bg"]}" stroke="{c["border"]}"/>'
        f'<path d="M1,13A12,12 0 0 1 13,1H{W - 13}A12,12 0 0 1 {W - 1},13V{top}H1Z" fill="{c["panel"]}"/>'
        f'<rect x="1" y="{top}" width="{W - 2}" height="1" fill="{c["border"]}"/>'
        '<circle cx="24" cy="22" r="7" fill="#ff5f57"/><circle cx="46" cy="22" r="7" fill="#febc2e"/>'
        '<circle cx="68" cy="22" r="7" fill="#28c840"/>'
        + text(W / 2, 27, e(title), c, size=14, color=c["muted"], weight=600, anchor="middle")
    )
    return svg(height, chrome + "".join(body), c)


def footer(t, c):
    body = (
        f'<text x="{W/2}" y="40" font-family="{e(MONO)}" font-size="17" text-anchor="middle">'
        f'<tspan fill="{c["accent"]}">{USER}@github</tspan><tspan fill="{c["muted"]}">:~$ </tspan>'
        f'<tspan fill="{c["fg"]}">exit</tspan><tspan class="blink" fill="{c["accent"]}"> ▋</tspan></text>'
        + text(W / 2, 76, e(t["footer_1"]), c, size=15, color=c["muted"], font=MONO, anchor="middle")
    )
    return svg(96, body, c)


def build_assets():
    for theme, c in THEMES.items():
        out = ROOT / "assets" / theme
        out.mkdir(parents=True, exist_ok=True)
        files = {f"l-{name}.svg": button(label, c, icon=icon) for name, label, _, icon in LINKS + BRAND_LINKS}
        files["lang-en-on.svg"] = button("EN", c, active=True)
        files["lang-en-off.svg"] = button("EN", c)
        files["lang-es-on.svg"] = button("ES", c, active=True)
        files["lang-es-off.svg"] = button("ES", c)
        for lang, t in T.items():
            files[f"hero-{lang}.svg"] = hero(t, c)
            files[f"now-{lang}.svg"] = now(t, c)
            files[f"terminal-{lang}.svg"] = terminal(lang, c)
            files[f"rails-{lang}.svg"] = rails(t, c)
            files[f"p-express-{lang}.svg"] = project_card(
                "express-version-api", t["express_desc"], t["express_meta"], c, t["view"])
            files[f"p-braqon-{lang}.svg"] = project_card(
                "BRAQON", t["braqon_desc"], t["braqon_meta"], c, t["view"], mark=True, live=False)
            files[f"footer-{lang}.svg"] = footer(t, c)
            for n, (title, comment) in enumerate(t["sections"], 1):
                files[f"s{n:02d}-{lang}.svg"] = section(n, title, comment, c)
        for name, content in files.items():
            (out / name).write_text(content, encoding="utf-8")
        # Assets from earlier versions that the READMEs no longer use.
        for pattern in ("project-*.svg", "stack-*.svg"):
            for old in out.glob(pattern):
                old.unlink()

# ── READMEs ──────────────────────────────────────────────────────────────────

def pic(src, alt, width="100%", height=None):
    size = f'height="{height}"' if height else f'width="{width}"'
    return (f'<picture><source media="(prefers-color-scheme: dark)" srcset="{src.format(t="dark")}"/>'
            f'<img src="{src.format(t="light")}" {size} alt="{e(alt)}"/></picture>')


def asset(name, lang, alt, width="100%"):
    return pic(f"assets/{{t}}/{name}-{lang}.svg", alt, width)


def link_button(name, label, url, height=34):
    return f'<a href="{url}">{pic(f"assets/{{t}}/l-{name}.svg", label, height=height)}</a>'


OUTPUT = f"https://raw.githubusercontent.com/{USER}/{USER}/output"
SUMMARY = "https://github-profile-summary-cards.vercel.app/api/cards/{kind}?username=" + USER + "&theme={theme}{extra}"
STREAK = "https://streak-stats.demolab.com?user=" + USER + "&hide_border=true&theme={}"


def card(url_dark, url_light, alt, height):
    return (f'<picture><source media="(prefers-color-scheme: dark)" srcset="{url_dark}"/>'
            f'<img src="{url_light}" height="{height}" alt="{e(alt)}"/></picture>')


def summary(kind, alt, height, extra=""):
    return card(SUMMARY.format(kind=kind, theme="github_dark", extra=extra),
                SUMMARY.format(kind=kind, theme="default", extra=extra), alt, height)

COPY = {
    "en": dict(
        other="es", other_file="README.es.md",
        nav=["whoami", "rails", "stack", "building", "telemetry", "off-keyboard"],
        code="""const braqon = {
  name:     "Braian Quintian",
  role:     ["Founder @ BRAQON", "CTO @ 88Pay"],
  based:    "Colombia 🇨🇴",
  builds:   ["payment APIs", "fintech platforms"],
  stack:    ["NestJS", "Next.js", "Angular", "TS"],
  infra:    ["AWS", "Terraform", "Docker"],
  learning: ["Java", "Spring Boot", "GraphQL"],
  hobbies:  ["🏀", "🎵", "📚"],
  fuel:     "☕".repeat(Infinity), // RangeError 💥
};""",
        bullets=[
            "💳 By day I wire up the ways Latin America pays (bank transfers, wallets, cards, cash and crypto) behind **one API**.",
            "🔐 I care about the boring stuff that keeps money safe: secure-by-default code, least privilege and reviews that actually happen.",
            "🎓 Systems Engineering student. Learning out loud.",
            f"📫 Reach me at **{EMAIL}**",
        ],
        stack=[("🎨 Frontend", "html,css,js,ts,react,nextjs,angular,tailwind"),
               ("⚙️ Backend", "nodejs,nestjs,express,bun,python"),
               ("🗄️ Data", "postgres,mysql,mongodb,sqlite"),
               ("☁️ Cloud & tools", "aws,terraform,docker,linux,git,github,postman,vscode"),
               ("📚 Learning", "java,spring,graphql")],
        rails_note="The kinds of payment rails I build integrations for. Same contract on top, wildly different edge cases underneath.",
        brand="BRAQON on the internet",
        snake="🐍 a snake eating my contributions, refreshed every 12 hours",
        facts_title="🎲 Random facts (click me)",
        facts=[
            "🏷️ **BRAQON** = **BRA**ian + **Q**uintian + **ON**. Yes, I did the math.",
            "🐛 My favorite bug is the one that only happens in production. (Kidding. Please don't.)",
            "🎮 In games I'm *baxtom* or *braxtom*, whichever isn't taken.",
            "🏀 If I'm not coding, I'm probably arguing about basketball.",
        ],
        coding_to="🎧 Coding to",
        back="back to top ↑",
    ),
    "es": dict(
        other="en", other_file="README.md",
        nav=["whoami", "rieles", "stack", "construyendo", "telemetría", "fuera del teclado"],
        code="""const braqon = {
  nombre:     "Braian Quintian",
  rol:        ["Founder @ BRAQON", "CTO @ 88Pay"],
  desde:      "Colombia 🇨🇴",
  construye:  ["APIs de pago", "plataformas fintech"],
  stack:      ["NestJS", "Next.js", "Angular", "TS"],
  infra:      ["AWS", "Terraform", "Docker"],
  aprendiendo:["Java", "Spring Boot", "GraphQL"],
  hobbies:    ["🏀", "🎵", "📚"],
  gasolina:   "☕".repeat(Infinity), // RangeError 💥
};""",
        bullets=[
            "💳 De día conecto las formas de pagar en Latinoamérica (transferencias, billeteras, tarjetas, efectivo y cripto) detrás de **una sola API**.",
            "🔐 Me importa lo aburrido que mantiene el dinero seguro: código seguro por defecto, mínimo privilegio y revisiones que de verdad se hacen.",
            "🎓 Estudiante de Ingeniería de Sistemas. Aprendiendo en voz alta.",
            f"📫 Escríbeme a **{EMAIL}**",
        ],
        stack=[("🎨 Frontend", "html,css,js,ts,react,nextjs,angular,tailwind"),
               ("⚙️ Backend", "nodejs,nestjs,express,bun,python"),
               ("🗄️ Datos", "postgres,mysql,mongodb,sqlite"),
               ("☁️ Cloud y herramientas", "aws,terraform,docker,linux,git,github,postman,vscode"),
               ("📚 Aprendiendo", "java,spring,graphql")],
        rails_note="Los tipos de rieles de pago para los que construyo integraciones. El mismo contrato arriba, casos borde muy distintos abajo.",
        brand="BRAQON en internet",
        snake="🐍 una serpiente comiéndose mis contribuciones, se actualiza cada 12 horas",
        facts_title="🎲 Datos random (dale clic)",
        facts=[
            "🏷️ **BRAQON** = **BRA**ian + **Q**uintian + **ON**. Sí, hice la cuenta.",
            "🐛 Mi bug favorito es el que solo pasa en producción. (Es broma. Por favor no.)",
            "🎮 En los juegos soy *baxtom* o *braxtom*, el que esté libre.",
            "🏀 Si no estoy programando, probablemente estoy discutiendo de basket.",
        ],
        coding_to="🎧 Programando con",
        back="volver arriba ↑",
    ),
}


def readme(lang):
    t, k = T[lang], COPY[lang]
    anchors = ["whoami", "rails", "stack", "building", "telemetry", "off-keyboard"]
    nav = " · ".join(f'<a href="#{a}">{label}</a>' for label, a in zip(k["nav"], anchors))
    personal = "\n  ".join(link_button(n, label, url) for n, label, url, _ in LINKS)
    brand = "\n  ".join(link_button(n, label, url, height=30) for n, label, url, _ in BRAND_LINKS)
    here = pic(f"assets/{{t}}/lang-{lang}-on.svg", lang.upper(), height=30)
    other = f'<a href="{k["other_file"]}">{pic(f"assets/{{t}}/lang-{k["other"]}-off.svg", k["other"].upper(), height=30)}</a>'
    langs = (here + "\n  " + other) if lang == "en" else (other + "\n  " + here)

    stack_rows = "\n".join(
        f'  <tr><td align="center" width="200"><b>{label}</b></td>'
        f'<td><img src="https://skillicons.dev/icons?i={icons}&perline=8" alt="{e(label)}"/></td></tr>'
        for label, icons in k["stack"]
    )

    def sec(n, anchor):
        return f'<a name="{anchor}"></a>\n{asset(f"s{n:02d}", lang, t["sections"][n - 1][0])}\n'

    return f"""<!-- Generated by tools/build.py. Edit that file and run `python3 tools/build.py`. -->
<a name="top"></a>

<p align="center">
  {asset("hero", lang, "BRAQON · " + t["tagline"])}
</p>

<p align="center">
  {personal}
</p>

<p align="center">
  {langs}
  <img src="https://komarev.com/ghpvc/?username={USER}&base=273&label=views&color=00b4d8&style=flat-square" alt="views" height="22"/>
</p>

<a href="https://www.npmjs.com/package/braqon">{asset("terminal", lang, "terminal: whoami, ls ~/braqon-dev, cat stack.txt, npx braqon")}</a>

<p align="center"><code>{USER}@github:~$ cat README.md</code><br/><sub>{nav}</sub></p>

{asset("now", lang, t["now_1"])}

{sec(1, "whoami")}
```ts
{k["code"]}
```

{chr(10).join("- " + b for b in k["bullets"])}

{sec(2, "rails")}
{asset("rails", lang, t["sections"][1][0])}

<p align="center"><sub>{k["rails_note"]}</sub></p>

{sec(3, "stack")}
<table align="center">
{stack_rows}
</table>

{sec(4, "building")}
<p align="center">
  <a href="https://github.com/braqon-dev/express-version-api">{asset("p-express", lang, "express-version-api", "49%")}</a>
  <a href="https://github.com/braqon-dev">{asset("p-braqon", lang, "BRAQON", "49%")}</a>
</p>

<p align="center"><sub><b>{k["brand"]}</b></sub><br/>
  {brand}
</p>

{sec(5, "telemetry")}
<p align="center">
  {summary("profile-details", "profile details", 200).replace('height="200"', 'width="100%"')}
</p>
<p align="center">
  {summary("stats", "stats", 165)}
  {summary("most-commit-language", "top languages", 165)}
</p>
<p align="center">
  {card(STREAK.format("github-dark-blue"), STREAK.format("default"), "streak", 165)}
  {summary("productive-time", "productive time", 165, "&utcOffset=-5")}
</p>
<p align="center">
  <picture><source media="(prefers-color-scheme: dark)" srcset="{OUTPUT}/github-snake-dark.svg"/><img src="{OUTPUT}/github-snake.svg" width="100%" alt="contribution snake"/></picture>
  <br/><sub>{k["snake"]}</sub>
</p>

{sec(6, "off-keyboard")}
<details>
  <summary><b>{k["facts_title"]}</b></summary>
  <br/>

{chr(10).join("  - " + f for f in k["facts"])}
</details>

<p align="center"><b>{k["coding_to"]}</b><br/>
  <a href="https://spotify-github-profile.kittinanx.com/api/view?uid=31s5hjyn255z2to7qh4jy7f3lsve&redirect=true"><img src="https://spotify-github-profile.kittinanx.com/api/view?uid=31s5hjyn255z2to7qh4jy7f3lsve&cover_image=true&theme=default&show_offline=true&background_color=121212&interchange=true&profanity=true&hide_remaster=true&bar_color_cover=true" alt="Spotify"/></a>
</p>

<p align="center">
  <img src="https://quotes-github-readme.vercel.app/api?type=horizontal&theme=tokyonight" alt="dev quote"/>
</p>

{asset("footer", lang, "exit")}

<p align="center"><sub><a href="#top">{k["back"]}</a></sub></p>
"""


def main():
    build_assets()
    (ROOT / "README.md").write_text(readme("en"), encoding="utf-8")
    (ROOT / "README.es.md").write_text(readme("es"), encoding="utf-8")
    print("built assets/, README.md, README.es.md")


if __name__ == "__main__":
    main()
