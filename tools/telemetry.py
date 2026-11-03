#!/usr/bin/env python3
"""Generate the telemetry card (stats + contribution heatmap) from the GitHub GraphQL API.

Runs in the profile-assets workflow every 12 hours and is published to the `output` branch:
    GITHUB_TOKEN=... python3 tools/telemetry.py --out dist
Writes telemetry-<lang>-<theme>.svg for every language and theme in build.py.
"""

import argparse
import json
import os
import sys
import urllib.request
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build import MONO, THEMES, USER, W, e, panel, svg, text  # noqa: E402

QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      totalPullRequestContributions
      totalPullRequestReviewContributions
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount } }
      }
    }
  }
}
"""

LABELS = {
    "en": dict(total="contributions · last 12 months", current="current streak · days",
               longest="longest streak · days", best="best day", updated="updated",
               less="less", more="more", months="Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec",
               days=("Mon", "Wed", "Fri")),
    "es": dict(total="contribuciones · últimos 12 meses", current="racha actual · días",
               longest="racha más larga · días", best="mejor día", updated="actualizado",
               less="menos", more="más", months="ene feb mar abr may jun jul ago sep oct nov dic",
               days=("lun", "mié", "vie")),
}


def fetch(token):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": USER}}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        payload = json.load(resp)
    if "errors" in payload:
        raise SystemExit(f"GraphQL error: {payload['errors']}")
    return payload["data"]["user"]["contributionsCollection"]


def summarize(collection):
    weeks = collection["contributionCalendar"]["weeks"]
    days = [d for w in weeks for d in w["contributionDays"]]
    counts = [d["contributionCount"] for d in days]

    longest = run = 0
    for n in counts:
        run = run + 1 if n else 0
        longest = max(longest, run)

    # The current streak may end yesterday if nothing was pushed today yet.
    current, i = 0, len(counts) - 1
    if i >= 0 and counts[i] == 0:
        i -= 1
    while i >= 0 and counts[i]:
        current += 1
        i -= 1

    best = max(days, key=lambda d: d["contributionCount"]) if days else {"date": "", "contributionCount": 0}
    return dict(
        weeks=weeks,
        total=collection["contributionCalendar"]["totalContributions"],
        current=current,
        longest=longest,
        best=best,
        cuts=thresholds(counts),
    )


def thresholds(counts):
    """Quartiles of the non-zero days, like GitHub, so one huge day doesn't flatten the scale."""
    nz = sorted(n for n in counts if n)
    if not nz:
        return (1, 1, 1)
    q = lambda f: nz[min(len(nz) - 1, int(len(nz) * f))]
    return (q(0.25), q(0.5), q(0.75))


def level(count, cuts):
    if count == 0:
        return 0
    return 1 if count <= cuts[0] else 2 if count <= cuts[1] else 3 if count <= cuts[2] else 4


def render(stats, lang, c):
    lb = LABELS[lang]
    height, pad, gap = 380, 24, 16
    tile_w = (W - 2 * pad - 3 * gap) / 4
    best = stats["best"]
    best_label = f'{best["contributionCount"]} · {best["date"][5:]}' if best["date"] else "0"
    tiles = [
        (f'{stats["total"]:,}', lb["total"]),
        (str(stats["current"]), lb["current"]),
        (str(stats["longest"]), lb["longest"]),
        (best_label, lb["best"]),
    ]
    parts = [panel(1, 1, W - 2, height - 2, c)]
    for i, (value, label) in enumerate(tiles):
        x = pad + i * (tile_w + gap)
        parts.append(panel(x, pad, tile_w, 96, c, rx=12, fill=c["bg"]))
        parts.append(text(x + 20, pad + 50, e(value), c, size=32, weight=700, color=c["accent"] if i == 0 else None))
        parts.append(text(x + 20, pad + 76, e(label), c, size=12, color=c["muted"], font=MONO))

    weeks = stats["weeks"][-53:]
    cell, step = 15, 19
    grid_w = len(weeks) * step - (step - cell)
    x0, y0 = (W - grid_w) / 2 + 16, 178
    months = lb["months"].split()
    last_month = None
    for wi, week in enumerate(weeks):
        x = x0 + wi * step
        first = week["contributionDays"][0]["date"]
        m = int(first[5:7])
        if m != last_month and wi < len(weeks) - 2:
            parts.append(text(x, y0 - 10, months[m - 1], c, size=11, color=c["muted"], font=MONO))
            last_month = m
        for day in week["contributionDays"]:
            wd = (date.fromisoformat(day["date"]).weekday() + 1) % 7  # Sunday = 0, like GitHub
            lv = level(day["contributionCount"], stats["cuts"])
            fill = c["border"] if lv == 0 else c["accent"]
            opacity = (0.45, 0.25, 0.45, 0.7, 1)[lv]
            parts.append(f'<rect x="{x:.1f}" y="{y0 + wd * step}" width="{cell}" height="{cell}" rx="3" '
                         f'fill="{fill}" fill-opacity="{opacity}"><title>{day["date"]}: {day["contributionCount"]}</title></rect>')
    for label, wd in zip(lb["days"], (1, 3, 5)):
        parts.append(text(x0 - 10, y0 + wd * step + 12, label, c, size=11, color=c["muted"], font=MONO, anchor="end"))

    footer_y = height - 26
    today = date.today().isoformat()
    parts.append(text(pad + 6, footer_y, f'{lb["updated"]} {today} · github.com/{USER}', c, size=12,
                      color=c["muted"], font=MONO))
    lx = W - pad - 6 - 5 * 19 - 40
    parts.append(text(lx - 10, footer_y, lb["less"], c, size=12, color=c["muted"], font=MONO, anchor="end"))
    for i in range(5):
        fill = c["border"] if i == 0 else c["accent"]
        opacity = (0.45, 0.25, 0.45, 0.7, 1)[i]
        parts.append(f'<rect x="{lx + i * 19}" y="{footer_y - 12}" width="{cell}" height="{cell}" rx="3" '
                     f'fill="{fill}" fill-opacity="{opacity}"/>')
    parts.append(text(lx + 5 * 19 + 6, footer_y, lb["more"], c, size=12, color=c["muted"], font=MONO))
    return svg(height, "".join(parts), c)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="dist")
    args = parser.parse_args()
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise SystemExit("GITHUB_TOKEN is required")
    stats = summarize(fetch(token))
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    for lang in LABELS:
        for theme, c in THEMES.items():
            (out / f"telemetry-{lang}-{theme}.svg").write_text(render(stats, lang, c), encoding="utf-8")
    print(f"telemetry: {stats['total']} contributions, streak {stats['current']}/{stats['longest']}")


if __name__ == "__main__":
    main()
