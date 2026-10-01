"""Gera o ícone da Zicão Store (simulador de maquininha) em SVG + PNGs.
Uso: python3 icons/gen.py  (precisa do playwright com chromium)"""
import os, asyncio
from playwright.async_api import async_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# Z geométrico (240x240), centralizado em 0,0
Z = "-120,-120 120,-120 120,-58 -28,58 120,58 120,120 -120,120 -120,58 28,-58 -120,-58"


def svg(mode="full", detail=True):
    """mode: full (quadrado cheio), rounded (cantos arredondados, fundo transparente fora),
    maskable (desenho menor dentro da área segura de 80%)."""
    scale = {"full": 1.0, "rounded": 1.06, "maskable": 0.72}[mode]
    rx = 230 if mode == "rounded" else 0
    chip = (
        '<rect x="-262" y="-118" width="104" height="80" rx="20" fill="url(#chip)"/>'
        '<path d="M-262 -78h104M-210 -118v80" stroke="#8a7420" stroke-opacity=".45" stroke-width="7"/>'
        if detail else ""
    )
    zx, zy, zs = (110, 30, 1.0) if detail else (0, 0, 1.25)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024">
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#262626"/><stop offset="1" stop-color="#070707"/>
  </linearGradient>
  <radialGradient id="glow" cx=".5" cy=".55" r=".5">
    <stop offset="0" stop-color="#FFE566" stop-opacity=".28"/><stop offset="1" stop-color="#FFE566" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="am" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#FFF3A8"/><stop offset=".45" stop-color="#FFE566"/><stop offset="1" stop-color="#F4C430"/>
  </linearGradient>
  <linearGradient id="vd" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#5BEA97"/><stop offset=".5" stop-color="#21C25E"/><stop offset="1" stop-color="#128A40"/>
  </linearGradient>
  <linearGradient id="gloss" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#fff" stop-opacity=".55"/><stop offset=".5" stop-color="#fff" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="chip" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#F1DC7A"/><stop offset="1" stop-color="#B8952A"/>
  </linearGradient>
  <linearGradient id="zg" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#2a2a2a"/><stop offset="1" stop-color="#0b0b0b"/>
  </linearGradient>
  <filter id="sh" x="-30%" y="-30%" width="160%" height="170%">
    <feDropShadow dx="0" dy="26" stdDeviation="26" flood-color="#000" flood-opacity=".55"/>
  </filter>
  <clipPath id="cardclip"><rect x="-320" y="-205" width="640" height="410" rx="72"/></clipPath>
  <clipPath id="tile"><rect width="1024" height="1024" rx="{rx}"/></clipPath>
</defs>
<g clip-path="url(#tile)">
  <rect width="1024" height="1024" fill="url(#bg)"/>
  <rect width="1024" height="1024" fill="url(#glow)"/>
  <g transform="translate(512 520) scale({scale})">
    <!-- cartão verde (PicPay) atrás -->
    <g transform="translate(-40 -70) rotate(-20)" filter="url(#sh)">
      <rect x="-320" y="-205" width="640" height="410" rx="72" fill="url(#vd)"/>
      <rect x="-320" y="-205" width="640" height="410" rx="72" fill="url(#gloss)" opacity=".6"/>
    </g>
    <!-- cartão amarelo (PagBank / marca) na frente -->
    <g transform="translate(30 60) rotate(-6)" filter="url(#sh)">
      <rect x="-320" y="-205" width="640" height="410" rx="72" fill="url(#am)"/>
      <g clip-path="url(#cardclip)">
        <rect x="-320" y="-205" width="640" height="210" fill="url(#gloss)"/>
      </g>
      <rect x="-317" y="-202" width="634" height="404" rx="69" fill="none" stroke="#fff" stroke-opacity=".5" stroke-width="5"/>
      {chip}
      <g transform="translate({zx} {zy}) scale({zs})">
        <polygon points="{Z}" fill="url(#zg)" stroke="#111" stroke-width="18" stroke-linejoin="round"/>
      </g>
    </g>
  </g>
</g>
</svg>'''


async def render(page, svg_txt, size, out, transparent=False):
    bg = "transparent" if transparent else "#070707"
    await page.set_viewport_size({"width": size, "height": size})
    await page.set_content(
        f'<html><body style="margin:0;background:{bg}">'
        f'<div style="width:{size}px;height:{size}px">{svg_txt.replace("<svg ", f"<svg width={size} height={size} ", 1)}</div>'
        '</body></html>')
    await page.screenshot(path=out, omit_background=transparent, clip={"x": 0, "y": 0, "width": size, "height": size})


async def main():
    full, rounded, mask = svg("full"), svg("rounded"), svg("maskable")
    fav = svg("rounded", detail=False)  # favicon: sem chip, Z maior
    open(os.path.join(HERE, "icon.svg"), "w").write(full)
    open(os.path.join(ROOT, "favicon.svg"), "w").write(fav)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page()
        jobs = [
            (full, 180, "apple-touch-icon.png", False),
            (full, 192, "icon-192.png", False),
            (full, 512, "icon-512.png", False),
            (mask, 512, "icon-maskable-512.png", False),
            (full, 1024, "icon-only.png", False),
            (fav, 32, "favicon-32.png", True),
        ]
        for s, size, name, tr in jobs:
            await render(pg, s, size, os.path.join(ROOT, "icons", name), tr)
        # testes de legibilidade
        for size in (120, 60, 32):
            await render(pg, rounded, size, os.path.join(HERE, f"_teste-{size}.png"), True)
        await render(pg, fav, 64, os.path.join(HERE, "_teste-fav64.png"), True)
        await b.close()

asyncio.run(main())
