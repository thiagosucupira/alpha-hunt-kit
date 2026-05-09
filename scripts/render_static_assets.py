#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets"
OUT.mkdir(parents=True, exist_ok=True)

BG = (5, 10, 16)
PANEL = (12, 22, 32)
TEXT = (226, 232, 240)
MUTED = (148, 163, 184)
TEAL = (45, 212, 191)
GREEN = (52, 211, 153)
AMBER = (245, 158, 11)
RED = (251, 113, 133)
BLUE = (96, 165, 250)
FONT_DIRS = [Path("/usr/share/fonts/truetype/dejavu"), Path("/usr/share/fonts/truetype/liberation2")]


def font(name: str, size: int):
    for d in FONT_DIRS:
        p = d / name
        if p.exists():
            return ImageFont.truetype(str(p), size)
    return ImageFont.load_default()

FB = font("DejaVuSans-Bold.ttf", 34)
FH = font("DejaVuSans-Bold.ttf", 26)
FM = font("DejaVuSansMono.ttf", 20)
FS = font("DejaVuSans.ttf", 18)
FT = font("DejaVuSans-Bold.ttf", 56)


def base(w=1400, h=860):
    img = Image.new("RGB", (w, h), BG)
    d = ImageDraw.Draw(img)
    for y in range(h):
        t = y / h
        d.line((0, y, w, y), fill=(int(5 + 8*t), int(10 + 22*t), int(16 + 34*t)))
    glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse((-180, -160, 520, 430), fill=(45, 212, 191, 45))
    gd.ellipse((880, 500, 1650, 1050), fill=(52, 211, 153, 28))
    gd.ellipse((420, 180, 1050, 720), fill=(245, 158, 11, 16))
    glow = glow.filter(ImageFilter.GaussianBlur(48))
    return Image.alpha_composite(img.convert("RGBA"), glow)


def text_box(d, xy, title, body, color, width=300, height=140):
    x, y = xy
    d.rounded_rectangle((x, y, x+width, y+height), radius=20, fill=PANEL+(245,), outline=color+(170,), width=2)
    d.text((x+20, y+18), title, font=FH, fill=color)
    d.multiline_text((x+20, y+58), body, font=FS, fill=TEXT, spacing=6)


def arrow(d, start, end, color=(180, 200, 210), width=4):
    x1, y1 = start
    x2, y2 = end
    d.line((x1, y1, x2, y2), fill=color+(190,), width=width)
    if x2 >= x1:
        pts = [(x2, y2), (x2-16, y2-9), (x2-16, y2+9)]
    else:
        pts = [(x2, y2), (x2+16, y2-9), (x2+16, y2+9)]
    d.polygon(pts, fill=color+(210,))


def boundary():
    img = base(1400, 860)
    d = ImageDraw.Draw(img)
    d.text((70, 54), "Package the hunt, not the agent", font=FT, fill=TEXT)
    d.text((74, 120), "Portable research contract: sources, prompts, state, tests, examples — no secrets.", font=FM, fill=MUTED)
    # host chips: keep them below the subtitle so the hero title owns the top line.
    x = 74
    y = 156
    for chip in ["Hermes", "OpenClaw", "cron", "GitHub Actions", "any agent"]:
        bbox = d.textbbox((0, 0), chip, font=FS)
        w = bbox[2] - bbox[0] + 28
        d.rounded_rectangle((x, y, x+w, y+34), radius=17, fill=(10, 28, 38, 230), outline=TEAL+(120,), width=1)
        d.text((x+14, y+8), chip, font=FS, fill=TEAL)
        x += w + 12
    d.text((745, 164), "hosts schedule; package owns the contract", font=FS, fill=MUTED)
    # center package
    d.rounded_rectangle((420, 210, 980, 645), radius=34, fill=(9, 20, 30, 245), outline=TEAL+(210,), width=3)
    d.text((470, 245), "daily-alpha-hunt/", font=FB, fill=TEAL)
    items = ["manifest.yaml", "docs/agent_prompt.md", "alpha_hunt/*.py", "experiments/*.json", "state templates", "tests + fixtures", "examples + visuals"]
    for j, item in enumerate(items):
        y = 310 + j*42
        d.rounded_rectangle((470, y, 890, y+30), radius=9, fill=(18, 36, 48, 240), outline=(80, 110, 125, 120), width=1)
        d.text((488, y+5), item, font=FM, fill=TEXT)
    # inputs
    text_box(d, (70, 230), "READS", "OpenAlex / Crossref / arXiv\nboard, ledger, graveyard\nfixtures or user bars", TEAL, 300, 165)
    text_box(d, (70, 470), "NEVER READS", ".env / API keys\nbroker account ids\nprivate memory stores", RED, 300, 145)
    # outputs
    text_box(d, (1030, 230), "WRITES", "metrics.json / report.md\nexperiments.tsv\nleaderboard / graveyard", GREEN, 300, 165)
    text_box(d, (1030, 470), "NEVER WRITES", "live orders\npublic posts\nmessages as the user", RED, 300, 145)
    arrow(d, (370, 315), (420, 315), TEAL)
    arrow(d, (980, 315), (1030, 315), GREEN)
    d.rounded_rectangle((90, 710, 1310, 775), radius=24, fill=(45, 15, 24, 220), outline=RED+(180,), width=2)
    d.text((125, 731), "Quarantine: credentials, live permissions, private paths, delivery targets, and toy-data alpha claims.", font=FM, fill=(255, 205, 210))
    img.convert('RGB').save(OUT/'alpha-hunt-package-boundary.png', quality=95)


def loop():
    img = base(1400, 860)
    d = ImageDraw.Draw(img)
    d.text((70, 54), "Alpha Hunt loop", font=FT, fill=TEXT)
    d.text((74, 120), "Seed -> Score -> Falsify -> Cheap test -> Distill -> Ship or kill", font=FM, fill=MUTED)
    nodes = [
        (160, 260, "1 SOURCES", "papers\nnotes\nprior runs", TEAL),
        (440, 260, "2 BOARD", "ranked\nfrontier", AMBER),
        (720, 260, "3 TEST", "one fixed\ncheap assay", GREEN),
        (1000, 260, "4 VERDICT", "promote\nblock\nkill", RED),
        (585, 555, "MEMORY", "ledger JSONL\ngraveyard.md\ncurrent.json", BLUE),
    ]
    for x, y, title, body, color in nodes:
        text_box(d, (x, y), title, body, color, 240, 150)
    arrow(d, (400, 335), (440, 335), TEAL)
    arrow(d, (680, 335), (720, 335), AMBER)
    arrow(d, (960, 335), (1000, 335), GREEN)
    arrow(d, (1120, 410), (760, 555), RED)
    arrow(d, (585, 630), (280, 410), BLUE)
    d.text((120, 735), "The package worked if one visible verdict became sharper. More ideas are noise until they survive a gate.", font=FM, fill=TEXT)
    img.convert('RGB').save(OUT/'alpha-hunt-loop.png', quality=95)


def ladder():
    img = base(1400, 860)
    d = ImageDraw.Draw(img)
    d.text((70, 54), "Data access ladder", font=FT, fill=TEXT)
    d.text((74, 120), "First run should be open. Serious validation must be canonical.", font=FM, fill=MUTED)
    tiers = [
        ("Tier 0", "Bundled fixture", "Runs everywhere. Plumbing only.", TEAL),
        ("Tier 1", "Public smoke/reference", "Yahoo daily, ECB reference. Demo only.", TEAL),
        ("Tier 2", "Public/manual history", "Dukascopy, HistData. Normalize carefully.", AMBER),
        ("Tier 3", "API-key providers", "Alpha Vantage, Twelve Data, Tiingo, Polygon.", AMBER),
        ("Tier 4", "Broker/account adapters", "Darwinex, OANDA, FXCM, IBKR. Optional.", RED),
        ("Tier 5", "Host canonical bars", "Required for promoted alpha claims.", GREEN),
    ]
    for i, (tier, title, body, color) in enumerate(tiers):
        x = 110 + i*190
        y = 630 - i*78
        d.rounded_rectangle((x, y, x+310, y+62), radius=16, fill=PANEL+(245,), outline=color+(180,), width=2)
        d.text((x+16, y+8), f"{tier} — {title}", font=FS, fill=color)
        d.text((x+16, y+34), body, font=font("DejaVuSans.ttf", 14), fill=TEXT)
    d.rounded_rectangle((90, 710, 1310, 795), radius=24, fill=(42, 32, 12, 230), outline=AMBER+(190,), width=2)
    d.text((125, 728), "Smoke tests prove the loop runs; they do not prove edge.", font=FM, fill=(255, 229, 180))
    d.text((125, 758), "Broker data is optional. Canonical validation is not.", font=FM, fill=(255, 229, 180))
    img.convert('RGB').save(OUT/'alpha-hunt-data-access-ladder.png', quality=95)

if __name__ == '__main__':
    boundary()
    loop()
    ladder()
    print('\n'.join(str(p) for p in sorted(OUT.glob('alpha-hunt*.png'))))
