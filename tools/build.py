#!/usr/bin/env python3
"""Build the BRAQON profile: every SVG in assets/ plus README.md and README.es.md.

Edit the content in this file, then run:  python3 tools/build.py
Nothing here needs third-party packages; the output is plain SVG and Markdown.
"""

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

# ── Content ──────────────────────────────────────────────────────────────────

T = {
    "en": dict(
        tagline="Braian Quintian · CTO @ 88Pay",
        sub="full-stack · payments · cloud & security · Colombia",
        prompt="building one API for every way LATAM pays",
        now_1="Leading engineering at 88Pay: one API for the ways Latin America pays.",
        now_2="shipping → payment APIs · infrastructure as code · security engineering",
        sections=[
            ("whoami", "// who's behind the keyboard"),
            ("payment rails", "// one contract on top, many edge cases below"),
            ("stack", "// tools I reach for"),
            ("projects", "// open source"),
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
        project_desc=["Middleware for versioning routes and APIs in Express.js,",
                      "so /v1 and /v2 can live together in peace."],
        project_cta="view repo →",
        footer_1="thanks for scrolling, see you in the next commit",
    ),
    "es": dict(
        tagline="Braian Quintian · CTO @ 88Pay",
        sub="full-stack · pagos · cloud y seguridad · Colombia",
        prompt="construyendo una API para cada forma de pagar en LATAM",
        now_1="Lidero ingeniería en 88Pay: una API para las formas de pagar en Latinoamérica.",
        now_2="enviando → APIs de pago · infraestructura como código · ingeniería de seguridad",
        sections=[
            ("whoami", "// quién está detrás del teclado"),
            ("rieles de pago", "// un contrato arriba, muchos casos borde abajo"),
            ("stack", "// las herramientas que uso"),
            ("proyectos", "// open source"),
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
        project_desc=["Middleware para versionar rutas y APIs en Express.js,",
                      "para que /v1 y /v2 convivan en paz."],
        project_cta="ver repo →",
        footer_1="gracias por llegar hasta aquí, nos vemos en el próximo commit",
    ),
}

# ── SVG helpers ──────────────────────────────────────────────────────────────

def e(text):
    return escape(text, {'"': "&quot;"})


def svg(height, body, c, css=""):
    style = (
        "<style>"
        ".blink{animation:blink 1.1s steps(1) infinite}"
        "@keyframes blink{50%{opacity:0}}"
        f"{css}"
        "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"
        "</style>"
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{height}" '
        f'viewBox="0 0 {W} {height}" fill="none" role="img">{style}{body}</svg>\n'
    )


def panel(x, y, w, h, c, rx=14, fill=None, dashed=False, stroke=None):
    dash = ' stroke-dasharray="6 6"' if dashed else ""
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
            f'fill="{fill or c["panel"]}" stroke="{stroke or c["border"]}"{dash}/>')


def text(x, y, s, c, size=16, color=None, font=SANS, weight=400, anchor="start", extra=""):
    return (f'<text x="{x}" y="{y}" font-family="{e(font)}" font-size="{size}" '
            f'font-weight="{weight}" fill="{color or c["fg"]}" text-anchor="{anchor}"{extra}>'
            f"{s}</text>")


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


def wordmark(word, c, x, y, scale):
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
    return (f'<g transform="translate({x},{y}) scale({scale})" stroke="{c["fg"]}" '
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


def project(t, c):
    chips, x = [], 32
    for label in ["TypeScript", "Express.js", "middleware", "API versioning"]:
        w = len(label) * 8.6 + 26
        chips.append(f'<rect x="{x}" y="124" width="{w:.0f}" height="28" rx="14" fill="none" stroke="{c["border"]}"/>'
                     + text(x + w / 2, 143, e(label), c, size=13, color=c["muted"], font=MONO, anchor="middle"))
        x += w + 10
    body = (
        panel(1, 1, W - 2, 176, c)
        + text(32, 50, "📦", c, size=24)
        + text(70, 50, "express-version-api", c, size=24, color=c["accent"], font=MONO, weight=700)
        + text(32, 84, e(t["project_desc"][0]), c, size=17)
        + text(32, 108, e(t["project_desc"][1]), c, size=17, color=c["muted"])
        + "".join(chips)
        + text(W - 32, 50, e(t["project_cta"]), c, size=15, color=c["muted"], font=MONO, anchor="end")
    )
    return svg(178, body, c)


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
        for lang, t in T.items():
            files = {
                f"hero-{lang}.svg": hero(t, c),
                f"now-{lang}.svg": now(t, c),
                f"rails-{lang}.svg": rails(t, c),
                f"project-{lang}.svg": project(t, c),
                f"footer-{lang}.svg": footer(t, c),
            }
            for n, (title, comment) in enumerate(t["sections"], 1):
                files[f"s{n:02d}-{lang}.svg"] = section(n, title, comment, c)
            for name, content in files.items():
                (out / name).write_text(content, encoding="utf-8")

# ── READMEs ──────────────────────────────────────────────────────────────────

def pic(name, alt, width="100%"):
    return (f'<picture><source media="(prefers-color-scheme: dark)" srcset="{name.format(t="dark")}"/>'
            f'<img src="{name.format(t="light")}" width="{width}" alt="{e(alt)}"/></picture>')


def asset(name, lang, alt):
    return pic(f"assets/{{t}}/{name}-{lang}.svg", alt)


def badge(label, color, logo, href):
    return (f'<a href="{href}"><img src="https://img.shields.io/badge/{label}-{color}'
            f'?style=for-the-badge&logo={logo}&logoColor=white" alt="{label}"/></a>')


def card(url_dark, url_light, alt, height):
    return (f'<picture><source media="(prefers-color-scheme: dark)" srcset="{url_dark}"/>'
            f'<img src="{url_light}" height="{height}" alt="{e(alt)}"/></picture>')


SUMMARY = "https://github-profile-summary-cards.vercel.app/api/cards/{kind}?username=" + USER + "&theme={theme}{extra}"


def summary(kind, alt, height, extra=""):
    return card(SUMMARY.format(kind=kind, theme="github_dark", extra=extra),
                SUMMARY.format(kind=kind, theme="default", extra=extra), alt, height)


COPY = {
    "en": dict(
        other=("Español", "README.es.md"), here="English",
        nav=["whoami", "rails", "stack", "projects", "telemetry", "off-keyboard"],
        code="""const braqon = {
  name:     "Braian Quintian",
  role:     "CTO @ 88Pay",
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
        rails_note="The kinds of payment rails I build integrations for. Same contract on top, wildly different edge cases underneath.",
        stack=[("🎨 Frontend", "html,css,js,ts,react,nextjs,angular,tailwind"),
               ("⚙️ Backend", "nodejs,nestjs,express,bun,python"),
               ("🗄️ Data", "postgres,mysql,mongodb,sqlite"),
               ("☁️ Cloud & tools", "aws,terraform,docker,linux,git,github,postman,vscode"),
               ("📚 Learning", "java,spring,graphql")],
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
        other=("English", "README.md"), here="Español",
        nav=["whoami", "rieles", "stack", "proyectos", "telemetría", "fuera del teclado"],
        code="""const braqon = {
  nombre:     "Braian Quintian",
  rol:        "CTO @ 88Pay",
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
        rails_note="Los tipos de rieles de pago para los que construyo integraciones. El mismo contrato arriba, casos borde muy distintos abajo.",
        stack=[("🎨 Frontend", "html,css,js,ts,react,nextjs,angular,tailwind"),
               ("⚙️ Backend", "nodejs,nestjs,express,bun,python"),
               ("🗄️ Datos", "postgres,mysql,mongodb,sqlite"),
               ("☁️ Cloud y herramientas", "aws,terraform,docker,linux,git,github,postman,vscode"),
               ("📚 Aprendiendo", "java,spring,graphql")],
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
    other_label, other_file = k["other"]
    anchors = ["whoami", "rails", "stack", "projects", "telemetry", "off-keyboard"]
    nav = " · ".join(f'<a href="#{a}">{label}</a>' for label, a in zip(k["nav"], anchors))
    stack_rows = "\n".join(
        f'  <tr><td align="center" width="170"><b>{label}</b></td>'
        f'<td><img src="https://skillicons.dev/icons?i={icons}&perline=8" alt="{e(label)}"/></td></tr>'
        for label, icons in k["stack"]
    )
    snake_base = f"https://raw.githubusercontent.com/{USER}/{USER}/output/github-snake"
    streak = "https://streak-stats.demolab.com?user=" + USER + "&hide_border=true&theme={}"

    def sec(n, anchor):
        return f'<a name="{anchor}"></a>\n{asset(f"s{n:02d}", lang, t["sections"][n - 1][0])}\n'

    return f"""<!-- Generated by tools/build.py. Edit that file and run `python3 tools/build.py`. -->
<a name="top"></a>

<p align="center">
  {asset("hero", lang, "BRAQON · " + t["tagline"])}
</p>

<p align="center">
  {badge("LinkedIn", "0A66C2", "linkedin", "https://linkedin.com/in/braian-quintian")}
  {badge("Email", "D14836", "gmail", "mailto:" + EMAIL)}
  {badge("Instagram", "E4405F", "instagram", "https://www.instagram.com/braian.qloq/")}
  {badge("GitHub", "181717", "github", "https://github.com/" + USER)}
</p>

<p align="center">
  <a href="https://github.com/braqon-dev"><img src="https://img.shields.io/badge/BRAQON-braqon--dev-0d1117?style=flat-square&logo=github&logoColor=white" alt="BRAQON on GitHub"/></a>
  <a href="https://x.com/braqondev"><img src="https://img.shields.io/badge/@braqondev-000000?style=flat-square&logo=x&logoColor=white" alt="X @braqondev"/></a>
  <a href="https://www.linkedin.com/company/braqon/"><img src="https://img.shields.io/badge/LinkedIn-BRAQON-0A66C2?style=flat-square&logo=linkedin&logoColor=white" alt="LinkedIn BRAQON"/></a>
  <a href="https://www.youtube.com/@braqon"><img src="https://img.shields.io/badge/YouTube-@braqon-FF0000?style=flat-square&logo=youtube&logoColor=white" alt="YouTube @braqon"/></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/{k['here']}-00b4d8?style=flat-square" alt="{k['here']}"/>
  <a href="{other_file}"><img src="https://img.shields.io/badge/{other_label}-30363d?style=flat-square" alt="{other_label}"/></a>
  <img src="https://komarev.com/ghpvc/?username={USER}&base=273&label=views&color=00b4d8&style=flat-square" alt="views"/>
</p>

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

{sec(4, "projects")}
<a href="https://github.com/braqon-dev/express-version-api">{asset("project", lang, "express-version-api")}</a>

{sec(5, "telemetry")}
<p align="center">
  {summary("profile-details", "profile details", 200).replace('height="200"', 'width="100%"')}
</p>
<p align="center">
  {summary("stats", "stats", 165)}
  {summary("most-commit-language", "top languages", 165)}
</p>
<p align="center">
  {card(streak.format("github-dark-blue"), streak.format("default"), "streak", 165)}
  {summary("productive-time", "productive time", 165, "&utcOffset=-5")}
</p>
<p align="center">
  {card(snake_base + "-dark.svg", snake_base + ".svg", "contribution snake", 170)}
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
