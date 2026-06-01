#!/usr/bin/env python3
"""
Build script for 3607 Pacific Avenue Offering Memorandum.
Buyer-facing OM. 3-agent footer (Erster + Glen + Filip — co-listing).
Source of truth: 3607 Pacific Ave - OM Model.pdf (June 2026).
Coordinates: U.S. Census Bureau geocoder (Public_AR_Current).
"""

import base64, os, io, sys
from PIL import Image

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ── Paths ────────────────────────────────────────────────────────────────
BTS = r"C:\Users\gscher\OneDrive - Marcus & Millichap\Niculete, Filip's files - LAAA Team\Marketing Packages\3607 Pacific Ave\BTS Docs"
PRO = os.path.join(BTS, 'Pictures', 'Professional Pictures')   # new professional shoot (drone + DSLR)
SELLER = os.path.join(BTS, 'Seller Pictures')                  # staged interiors + common areas
ERSTER_PICS = r"C:\Users\gscher\OneDrive - Marcus & Millichap\Niculete, Filip's files - LAAA Team\Proposals\Old Team Member Proposals\Erster's Proposals\2024\3607 Pacific Ave\Pics"
BRAND = r"C:\Users\gscher\LAAA-AI-Prompts\branding"
HEADSHOTS_SQ = r"C:\Users\gscher\OneDrive - Marcus & Millichap\Niculete, Filip's files - LAAA Team\LAAA\Team Headshots\SQ"
OUT = r"C:\Users\gscher\3607-pacific-ave-om\index.html"

def img_b64(path, max_w=1600, q=80):
    im = Image.open(path)
    if im.mode in ('RGBA','P','LA'): im = im.convert('RGB')
    if im.width > max_w:
        r = max_w/im.width; im = im.resize((max_w, int(im.height*r)), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, format='JPEG', quality=q, optimize=True)
    return f'data:image/jpeg;base64,{base64.b64encode(buf.getvalue()).decode()}'

def png_b64(path, max_w=600):
    im = Image.open(path)
    if im.width > max_w:
        r = max_w/im.width; im = im.resize((max_w, int(im.height*r)), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, format='PNG', optimize=True)
    return f'data:image/png;base64,{base64.b64encode(buf.getvalue()).decode()}'

print("Encoding images ...")
# Cover — hero twilight drone aerial (building centered, beach + ocean + sunset)
cover_bg  = img_b64(os.path.join(PRO, 'DJI_20260529063433_0274_D.JPG'), 1800, 82)
# Executive Summary — ocean-facing aerial (Venice Pier + Pacific in frame)
exec_aerial = img_b64(os.path.join(PRO, 'DJI_20260529062131_0265_D.jpg'), 1700, 82)
# Location Overview hero — wide neighborhood + Marina harbor context
context   = img_b64(os.path.join(PRO, 'DJI_20260529061949_0262_D.jpg'), 1700, 82)
# Investment Overview photo grid (4)
g_main    = img_b64(os.path.join(PRO, 'DJI_20260529064304_0284_D.JPG'), 1400, 78)  # twilight street elevation
g_kitchen = img_b64(os.path.join(SELLER, '8.jpg'), 1400, 78)   # open living/dining, wall-to-wall glass
g_patio   = img_b64(os.path.join(SELLER, '9.jpg'), 1400, 78)   # double-height living, architecture
g_sunset  = img_b64(os.path.join(SELLER, '6.jpg'), 1400, 78)   # ground-floor beach patio
# Investment Highlights — paired feature-row images
feat_unit_a = img_b64(os.path.join(SELLER, '7.jpg'), 1400, 78)   # renovated kitchen (waterfall quartz island)
feat_unit_b = img_b64(os.path.join(SELLER, '5.jpg'), 1400, 78)   # private roof terrace
feat_common = img_b64(os.path.join(PRO, 'DSC02705.jpg'), 1400, 78)  # gated entry + Gelman architecture
feat_invest = img_b64(os.path.join(PRO, 'DJI_20260529063815_0277_D.JPG'), 1400, 78)  # aerial: asset + pier + ocean
feat_loc    = img_b64(os.path.join(SELLER, '2.jpg'), 1400, 78)   # beach-access walk street
# Brand
logo      = png_b64(os.path.join(BRAND, 'logos', 'LAAA_Team_White.png'), 400)
hs_glen   = png_b64(os.path.join(BRAND, 'headshots', 'Glen_Scher.png'), 200)
hs_filip  = png_b64(os.path.join(BRAND, 'headshots', 'Filip_Niculete.png'), 200)
hs_yoni   = png_b64(os.path.join(HEADSHOTS_SQ, 'Jonathan SQ.png'), 200)
print("Done encoding.")

# ── Social-share (Open Graph) card ──────────────────────────────────────────
# Link unfurls (iMessage, email, Slack, WhatsApp, LinkedIn) need a REAL hosted
# image file + og:image meta tags — base64-inlined images can't be scraped.
# Domain is read from CNAME so this block is reusable for any BOV/OM build.
REPO = os.path.dirname(OUT)
try:
    with open(os.path.join(REPO, 'CNAME'), encoding='utf-8') as _f: DOMAIN = _f.read().strip()
except Exception: DOMAIN = ''
SITE_URL = f'https://{DOMAIN}' if DOMAIN else ''
OG_IMG_URL = f'{SITE_URL}/og.jpg'

def make_og(src, dst, w=1200, h=630, q=86):
    """Cover-crop a hero photo to a 1200x630 social-share card."""
    im = Image.open(src)
    if im.mode != 'RGB': im = im.convert('RGB')
    sr, ir = w/h, im.width/im.height
    if ir > sr:
        nw = int(im.height*sr); x = (im.width-nw)//2; im = im.crop((x, 0, x+nw, im.height))
    else:
        nh = int(im.width/sr); y = (im.height-nh)//2; im = im.crop((0, y, im.width, y+nh))
    im.resize((w, h), Image.LANCZOS).save(dst, format='JPEG', quality=q, optimize=True)

make_og(os.path.join(PRO, 'DJI_20260529063433_0274_D.JPG'), os.path.join(REPO, 'og.jpg'))
print(f"Wrote og.jpg ({OG_IMG_URL})")

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Eastwind Apartments | 3607 Pacific Avenue | Investment Offering | Marcus &amp; Millichap</title>
<meta name="description" content="Eastwind Apartments — 3607 Pacific Avenue, a renovated six-unit beach-front offering on the Marina Peninsula in Marina del Rey, steps from the sand. $5,395,000.">
<link rel="canonical" href="{SITE_URL}/">
<!-- Open Graph / Twitter share card (link preview thumbnail) -->
<meta property="og:type" content="website">
<meta property="og:site_name" content="LAAA Team">
<meta property="og:title" content="Eastwind Apartments | 3607 Pacific Avenue | Investment Offering">
<meta property="og:description" content="A renovated six-unit beach-front offering on the Marina Peninsula in Marina del Rey, steps from the sand. $5,395,000.">
<meta property="og:url" content="{SITE_URL}/">
<meta property="og:image" content="{OG_IMG_URL}">
<meta property="og:image:secure_url" content="{OG_IMG_URL}">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Eastwind Apartments, 3607 Pacific Avenue, Marina del Rey">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Eastwind Apartments | 3607 Pacific Avenue">
<meta name="twitter:description" content="A renovated six-unit beach-front offering on the Marina Peninsula, steps from the sand. $5,395,000.">
<meta name="twitter:image" content="{OG_IMG_URL}">
<!-- Define the Maps callback BEFORE the API loads so it can never race; API still starts fetching from <head> in parallel. Real drawing runs whenever both the API and the page body are ready (either order). -->
<script>function initMaps(){{window.__mapsReady=true;if(window.__drawMaps)window.__drawMaps();}}</script>
<script async defer src="https://maps.googleapis.com/maps/api/js?key=AIzaSyB1FbBfb4q0FVpiMSHBhjERp_R2lP3wDE8&callback=initMaps&loading=async&v=weekly"></script>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'Inter',sans-serif;color:#333;line-height:1.6;background:#fff}}
html{{scroll-behavior:smooth;scroll-padding-top:50px}}

/* ════ COVER (single full viewport, photo bg + overlaid text) ════ */
.cover{{position:relative;min-height:100vh;min-height:100svh;display:flex;align-items:center;justify-content:center;text-align:center;color:#fff;overflow:hidden}}
.cover-bg{{position:absolute;inset:0;background:url('{cover_bg}') center/cover no-repeat;filter:brightness(.42);z-index:0}}
.cover-scrim{{position:absolute;inset:0;background:linear-gradient(180deg, rgba(13,34,56,0.35) 0%, rgba(13,34,56,0.15) 35%, rgba(13,34,56,0.55) 100%);z-index:1}}
.cover-content{{position:relative;z-index:2;padding:60px 40px;max-width:900px}}
.cover-logo{{width:260px;margin:0 auto 28px;display:block}}
.cover-label{{font-size:12px;font-weight:500;letter-spacing:3px;text-transform:uppercase;color:#C5A258;margin-bottom:14px}}
.cover-title{{font-size:46px;font-weight:700;letter-spacing:1px;margin-bottom:6px;line-height:1.1;text-shadow:0 2px 12px rgba(0,0,0,.6)}}
.cover-sub{{font-size:16px;font-weight:300;color:rgba(255,255,255,.85);margin-bottom:30px;letter-spacing:.5px;text-shadow:0 1px 6px rgba(0,0,0,.6)}}
.cover-price{{font-size:54px;font-weight:700;color:#C5A258;margin-bottom:28px;letter-spacing:1px;text-shadow:0 2px 16px rgba(0,0,0,.6)}}
.cover-stats{{display:flex;justify-content:center;gap:36px;flex-wrap:wrap;margin-bottom:34px}}
.cv{{font-size:22px;font-weight:600;display:block;color:#fff;text-shadow:0 1px 6px rgba(0,0,0,.5)}}
.cl{{font-size:10px;font-weight:500;text-transform:uppercase;letter-spacing:1.5px;color:rgba(255,255,255,.7);display:block;margin-top:2px}}
.client-greeting{{font-size:15px;font-weight:400;font-style:italic;color:rgba(255,255,255,.92);margin-bottom:4px}}
.coop-line{{font-size:12px;font-weight:600;color:#C5A258;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:18px}}
.cover-agent{{font-size:13px;color:rgba(255,255,255,.78);margin-top:10px;line-height:1.6}}
.cover-date{{font-size:12px;color:rgba(255,255,255,.55);margin-top:6px}}
.cover-nyse{{font-size:11px;letter-spacing:2px;color:rgba(255,255,255,.45);margin-top:8px;text-transform:uppercase}}

/* ════ TOC NAV ════ */
.toc-nav{{background:#1B3A5C;position:sticky;top:0;z-index:100;box-shadow:0 2px 8px rgba(0,0,0,.15)}}
.toc-links{{display:flex;flex-wrap:nowrap;justify-content:center;align-items:stretch;padding:0 20px;overflow-x:auto;-webkit-overflow-scrolling:touch}}
.toc-links a{{color:rgba(255,255,255,.7);text-decoration:none;font-size:11px;font-weight:500;letter-spacing:.5px;text-transform:uppercase;padding:14px 12px;border-bottom:2px solid transparent;transition:all .2s ease;white-space:nowrap;display:flex;align-items:center;min-height:44px}}
.toc-links a:hover{{color:#fff;background:rgba(197,162,88,.12);border-bottom-color:rgba(197,162,88,.4)}}
.toc-links a.toc-active{{color:#C5A258;font-weight:600;border-bottom-color:#C5A258}}
/* Hamburger toggle — hidden on desktop, shown when the row can't fit */
.nav-toggle{{display:none}}
@media(max-width:960px){{
  .nav-toggle{{display:flex;align-items:center;gap:10px;width:100%;background:#1B3A5C;color:#fff;border:none;cursor:pointer;padding:14px 18px;min-height:50px;font-family:'Inter',sans-serif;font-size:12px;font-weight:600;letter-spacing:1.5px;text-transform:uppercase}}
  .nav-toggle .nav-burger{{font-size:16px;line-height:1}}
  .nav-toggle .nav-label{{flex:1;text-align:left}}
  .nav-toggle .nav-caret{{transition:transform .2s ease}}
  .toc-nav.open .nav-toggle .nav-caret{{transform:rotate(180deg)}}
  .toc-links{{display:none;flex-direction:column;padding:0;max-height:72vh;overflow-y:auto;overflow-x:hidden;border-top:1px solid rgba(255,255,255,.12)}}
  .toc-nav.open .toc-links{{display:flex}}
  .toc-links a{{width:100%;padding:15px 18px;min-height:50px;font-size:13px;border-bottom:1px solid rgba(255,255,255,.08)}}
  .toc-links a.toc-active{{background:rgba(197,162,88,.14)}}
}}

/* ════ SECTIONS ════ */
.section{{padding:50px 40px;max-width:1100px;margin:0 auto}}
.section-alt{{background:#f8f9fa}}
.section-title{{font-size:28px;font-weight:700;color:#1B3A5C;text-align:center;margin-bottom:6px}}
.section-subtitle{{font-size:13px;color:#C5A258;text-align:center;font-weight:500;letter-spacing:1px;text-transform:uppercase;margin-bottom:16px}}
.section-divider{{width:60px;height:3px;background:#C5A258;margin:0 auto 30px;border-radius:2px}}
.sub-heading{{font-size:18px;font-weight:600;color:#1B3A5C;margin:30px 0 14px;border-bottom:2px solid #C5A258;padding-bottom:6px;display:inline-block}}

/* ════ EXECUTIVE SUMMARY METRIC CARDS ════ */
.mg4{{display:grid;grid-template-columns:repeat(5,1fr);gap:14px;margin-bottom:30px}}
.mc{{background:#1B3A5C;color:#fff;border-radius:8px;padding:22px 16px;text-align:center;box-shadow:0 2px 8px rgba(27,58,92,.12)}}
.mv{{font-size:23px;font-weight:700;color:#C5A258;display:block;line-height:1.1;white-space:nowrap;font-variant-numeric:tabular-nums}}
.ml{{font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:1px;margin-top:6px;display:block;color:rgba(255,255,255,.85)}}
@media(max-width:1024px){{.mg4{{grid-template-columns:repeat(2,1fr);gap:14px}}.mv{{font-size:24px}}}}

/* ════ EXEC SUMMARY LAYOUT ════ */
.exec-intro{{font-size:15px;line-height:1.75;color:#333;text-align:center;max-width:880px;margin:0 auto 36px}}
.exec-aerial{{margin:0 0 30px;border-radius:8px;overflow:hidden;box-shadow:0 4px 18px rgba(0,0,0,.18)}}
.exec-aerial img{{width:100%;height:auto;display:block}}
.exec-aerial .caption{{padding:10px 18px;background:#f5f5f5;color:#555;font-size:12.5px;font-style:italic;text-align:center;border-top:1px solid #e5e5e5}}
.exec-aerial .caption strong{{color:#1B3A5C;font-style:normal}}
.exec-facts{{display:grid;grid-template-columns:repeat(2,1fr);gap:0 30px;margin-top:6px}}
.exec-facts table{{margin-bottom:0}}

/* ════ PHOTOS ════ */
.photo-grid{{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;margin:6px 0 24px;border-radius:8px;overflow:hidden}}
.photo-grid img{{width:100%;height:260px;object-fit:cover;display:block}}

/* ════ TABLES ════ */
table{{width:100%;border-collapse:collapse;margin-bottom:24px;font-size:13px}}
thead th{{background:#1B3A5C;color:#fff;padding:10px 8px;text-align:left;font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:.5px}}
tbody td{{padding:9px 8px;border-bottom:1px solid #e0e0e0}}
/* Numeric tables — right-align everything after the first 2 cols + tabular nums */
.fin-num td,.fin-num th{{font-variant-numeric:tabular-nums}}
.fin-num td:not(:first-child),.fin-num th:not(:first-child){{text-align:right}}
.fin-num td:first-child{{text-align:left}}
/* For Rent Roll which has unit + type as first 2 cols */
.fin-num-2 td,.fin-num-2 th{{font-variant-numeric:tabular-nums}}
.fin-num-2 td:not(:first-child):not(:nth-child(2)),.fin-num-2 th:not(:first-child):not(:nth-child(2)){{text-align:right}}
/* Comps tables: label cols 1-4 left, numbers right-aligned from col 5 on */
.fin-r5 td,.fin-r5 th{{font-variant-numeric:tabular-nums}}
.fin-r5 td:nth-child(n+5),.fin-r5 th:nth-child(n+5){{text-align:right}}
tbody tr:nth-child(even){{background:#f5f5f5}}
tbody tr.hl{{background:#FFF8E7;border-left:3px solid #C5A258;border-right:3px solid #C5A258;font-weight:600}}
tbody tr.hl td{{border-bottom-color:#C5A258}}
.it{{margin-bottom:24px}}
.it td{{padding:8px 12px;border-bottom:1px solid #eee}}
.it td:first-child{{font-weight:600;color:#1B3A5C;width:42%}}
.ts{{overflow-x:auto;-webkit-overflow-scrolling:touch;margin-bottom:24px}}
.ts table{{min-width:560px;margin-bottom:0}}
.ts-wide table{{min-width:720px}}
.ts-wider table{{min-width:920px}}
.ts-wide tbody td,.ts-wider tbody td{{vertical-align:top}}
.two-col{{display:grid;grid-template-columns:1fr 1fr;gap:30px;margin-bottom:24px}}
.narrative{{font-size:14px;line-height:1.75;color:#444;margin-bottom:20px}}
.narrative p{{margin-bottom:14px}}
.narrative ul{{margin:8px 0 18px 24px;font-size:14px;line-height:1.85;color:#444}}
.narrative ul li{{margin-bottom:4px}}

/* ════ CALLOUTS ════ */
.cn{{background:#FFF8E7;border-left:4px solid #C5A258;padding:16px 20px;margin:20px 0;border-radius:0 4px 4px 0;font-size:13px;color:#555;line-height:1.65}}
.cn strong{{color:#1B3A5C}}

/* ════ HIGHLIGHT BOXES (compact) ════ */
.hb-grid{{display:grid;grid-template-columns:repeat(2,1fr);gap:18px;margin:24px 0}}
.hb{{background:#1B3A5C;color:#fff;border-radius:8px;padding:22px 24px}}
.hb h4{{color:#C5A258;font-size:13px;text-transform:uppercase;letter-spacing:1px;margin-bottom:10px}}
.hb p{{font-size:13px;line-height:1.6;color:rgba(255,255,255,.92);margin:0}}
.hb ul{{margin:6px 0 0 18px;padding:0}}
.hb li{{font-size:13px;line-height:1.6;color:rgba(255,255,255,.92);margin-bottom:7px}}
.hb li:last-child{{margin-bottom:0}}

/* ════ PAIRED IMAGE + TEXT FEATURE ROWS (Investment Highlights) ════ */
.feat{{margin:18px 0 8px}}
.feat-row{{display:flex;gap:30px;align-items:center;margin-bottom:30px}}
.feat-row:last-child{{margin-bottom:0}}
.feat-row.rev{{flex-direction:row-reverse}}
.feat-imgs{{flex:1 1 50%;display:grid;grid-template-columns:1fr;gap:10px}}
.feat-imgs.two{{grid-template-columns:1fr 1fr}}
.feat-imgs img{{width:100%;height:280px;object-fit:cover;display:block;border-radius:8px;box-shadow:0 4px 16px rgba(0,0,0,.15)}}
.feat-text{{flex:1 1 50%}}
.feat-text h4{{color:#1B3A5C;font-size:16px;font-weight:600;text-transform:uppercase;letter-spacing:1px;margin-bottom:12px;border-bottom:2px solid #C5A258;padding-bottom:6px;display:inline-block}}
.feat-text ul{{margin:0 0 0 18px;padding:0}}
.feat-text li{{font-size:14px;line-height:1.65;color:#444;margin-bottom:8px}}
.feat-text li:last-child{{margin-bottom:0}}

/* ════ LOCATION HERO ════ */
.loc-hero{{width:100%;display:block;border-radius:8px;overflow:hidden;box-shadow:0 4px 18px rgba(0,0,0,.18);margin-bottom:24px}}
.loc-hero img{{width:100%;height:auto;display:block}}

/* ════ GOOGLE MAPS ════ */
.gmap{{height:460px;border-radius:8px;overflow:hidden;border:1px solid #ddd;margin-bottom:30px;box-shadow:0 2px 10px rgba(0,0,0,.08);background:#f0f4f8}}
.map-fallback{{display:none;font-size:12px;color:#666;font-style:italic;margin-bottom:30px}}
.gm-iw{{font-family:'Inter',sans-serif;font-size:12.5px;line-height:1.5;padding:4px 4px 2px;min-width:200px}}
.gm-iw strong{{color:#1B3A5C}}
.gm-iw a.gm-link{{display:inline-block;margin-top:8px;padding:5px 10px;background:#C5A258;color:#fff;border-radius:3px;font-size:11px;font-weight:600;text-decoration:none;letter-spacing:.3px}}
.gm-iw a.gm-link:hover{{background:#b3924f}}

/* ════ STATUS BADGES ════ */
.badge-done{{background:#e8f5e9;color:#2e7d32;padding:3px 9px;border-radius:3px;font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:.3px}}
.badge-opp{{background:#fff3e0;color:#e65100;padding:3px 9px;border-radius:3px;font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:.3px}}

/* ════ FOOTER (3-agent) ════ */
.footer{{background:#1B3A5C;color:#fff;padding:50px 40px;text-align:center}}
.footer-logo{{width:220px;margin:0 auto 28px;display:block}}
.footer-coop{{font-size:12px;color:#C5A258;text-transform:uppercase;letter-spacing:1.2px;margin-bottom:24px}}
.footer-team{{display:flex;justify-content:center;gap:28px;flex-wrap:wrap;margin-bottom:30px}}
.fp{{text-align:center;flex:1;min-width:240px;max-width:320px}}
.fp img{{width:64px;height:64px;border-radius:50%;object-fit:cover;border:2px solid #C5A258;margin-bottom:10px}}
/* Mobile: stack M&M (Glen, Filip) first; co-broker (Erster) last */
@media(max-width:768px){{
.fp.fp-yoni{{order:3}}
.fp.fp-glen{{order:1}}
.fp.fp-filip{{order:2}}
.fp img{{width:80px;height:80px}}
}}
.fp .fpn{{font-size:15px;font-weight:600;display:block}}
.fp .fpt{{font-size:11px;color:#C5A258;text-transform:uppercase;letter-spacing:.5px;display:block;margin-bottom:6px}}
.fp .fpfirm{{font-size:11px;color:rgba(255,255,255,.55);display:block;margin-bottom:6px;font-style:italic}}
.fp .fpd{{font-size:12px;color:rgba(255,255,255,.75);display:block;line-height:1.6}}
.fp .fpd a{{color:rgba(255,255,255,.75);text-decoration:none}}
.fo{{font-size:12px;color:rgba(255,255,255,.6);margin-bottom:18px}}
.fo a{{color:#C5A258;text-decoration:none}}
.fd{{font-size:10px;color:rgba(255,255,255,.4);max-width:820px;margin:0 auto;line-height:1.6}}

/* ════ DOWNLOAD PDF BUTTON ════ */
.download-btn{{position:fixed;bottom:24px;right:24px;z-index:200;background:#1B3A5C;color:#fff;border:2px solid #C5A258;border-radius:8px;padding:12px 20px;cursor:pointer;font-family:'Inter',sans-serif;font-size:13px;font-weight:600;display:flex;align-items:center;gap:8px;box-shadow:0 4px 16px rgba(0,0,0,.2);transition:all .2s ease}}
.download-btn:hover{{background:#244a6e;transform:translateY(-2px);box-shadow:0 6px 20px rgba(0,0,0,.25)}}
.download-btn svg{{color:#C5A258}}
.download-btn.is-hidden{{opacity:0;transform:translateY(20px);pointer-events:none}}

/* ════ RESPONSIVE 768 ════ */
@media(max-width:768px){{
.cover-content{{padding:40px 22px}}
.cover-title{{font-size:32px}}.cover-price{{font-size:38px}}
.cover-logo{{width:200px}}.cover-stats{{gap:20px}}
.cv{{white-space:nowrap}}
.section{{padding:36px 18px}}
.photo-grid{{grid-template-columns:1fr}}.photo-grid img{{height:240px}}
.two-col{{grid-template-columns:1fr;gap:20px}}
.hb-grid{{grid-template-columns:1fr}}
.feat-row,.feat-row.rev{{flex-direction:column;gap:16px}}
.feat-imgs img{{height:240px}}
.mg4{{grid-template-columns:repeat(2,1fr);gap:12px}}.mc{{padding:16px 10px}}.mv{{font-size:22px}}
.exec-facts{{grid-template-columns:1fr;gap:0}}
.footer-team{{flex-direction:column;align-items:center;gap:24px}}
table{{font-size:12px}}thead th{{font-size:10px;padding:8px 6px}}tbody td{{padding:7px 6px}}
.gmap{{height:340px}}
.toc-nav{{padding:0 8px}}.toc-nav a{{font-size:10.5px;padding:14px 10px;letter-spacing:.4px;min-height:44px}}
}}

/* ════ RESPONSIVE 420 ════ */
@media(max-width:420px){{
.cover-content{{padding:32px 16px}}
.cover-title{{font-size:26px}}.cover-sub{{font-size:13px}}
.cover-price{{font-size:32px}}
.cover-stats{{display:grid;grid-template-columns:1fr 1fr;gap:14px 18px;max-width:300px;margin:0 auto 26px}}
.cv{{font-size:17px;white-space:nowrap}}.cl{{font-size:9px}}.cover-label{{font-size:11px}}
.mg4{{grid-template-columns:1fr}}.mc{{padding:14px 10px}}.mv{{font-size:22px}}
.section{{padding:24px 12px}}.section-title{{font-size:22px}}
.footer{{padding:28px 14px}}.footer-team{{gap:18px}}
.toc-nav{{padding:0 4px}}.toc-nav a{{font-size:10px;padding:14px 8px;letter-spacing:.3px;min-height:44px}}
.gmap{{height:280px}}.ts table{{min-width:520px}}
.download-btn{{padding:10px 14px;font-size:11px;bottom:18px;right:14px}}
}}

/* ════ PRINT / PDF — Letter LANDSCAPE (rendered by LAAA-AI-Prompts/reporting/build_pdf.py) ════ */
@media print{{
/* build_pdf.py (Playwright) is authoritative for page size/margins/footer; this @page is only a
   fallback for browser window.print(). ALL pages landscape — never mixed portrait/landscape. */
@page{{size:Letter landscape;margin:0.45in 0.5in 0.65in}}
html,body{{background:#fff!important;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.toc-nav{{display:none!important}}
.download-btn{{display:none!important}}
/* Interactive Google maps hide; build_pdf injects a static-map <img> (.pdf-static-map) into each
   .gmap container. The text fallback shows ONLY when static-map generation fails. */
.gmap{{display:none!important}}
.pdf-static-map{{display:block!important;margin:0 auto 16px;text-align:center}}
.pdf-static-map img{{height:3.3in;width:auto;max-width:100%;display:inline-block;border:1px solid #d8dee6;border-radius:6px}}
.map-fallback{{display:block;color:#666;font-style:italic;margin-bottom:18px}}
.map-fallback.is-replaced{{display:none!important}}
/* Cover = exactly ONE landscape page (fixed height + clip beats the screen 100svh rule) */
.cover{{min-height:0!important;height:7in!important;max-height:7in!important;overflow:hidden;page-break-after:always}}
.cover-bg{{filter:brightness(.5)}}
.cover-content{{padding:24px 40px}}
/* One section per page; first section follows the cover break (no blank page between) */
.section{{page-break-before:always;padding:16px 0;max-width:none}}
.section:first-of-type{{page-break-before:avoid}}
.section-title{{font-size:23px;margin-bottom:4px}}
.section-subtitle{{margin-bottom:8px}}
.section-divider{{margin:0 auto 14px}}
/* Tables: repeat headers, keep rows whole, let the body flow across pages */
thead{{display:table-header-group}}
tfoot{{display:table-footer-group}}
tr{{page-break-inside:avoid}}
table{{page-break-inside:auto;font-size:11px}}
thead th{{font-size:9.5px;padding:7px 6px}}
tbody td{{padding:6px 6px}}
h2,h3,.section-title,.sub-heading{{page-break-after:avoid}}
p{{orphans:3;widows:3}}
.narrative{{margin-bottom:14px}}
.narrative p{{margin-bottom:10px}}
/* Scroll-wrapped tables must reveal full width in print (no clip), fit the landscape page */
.ts,.ts-wide,.ts-wider{{overflow:visible!important}}
.ts table,.ts-wide table,.ts-wider table{{min-width:0!important;width:100%!important}}
.ts-wider table{{font-size:9.5px}}
.ts-wider thead th{{font-size:8.5px;padding:6px 4px}}
.ts-wider tbody td{{padding:5px 4px}}
/* Wide detail tables (Building Systems, Rent Roll) flow naturally; the repeating header
   (thead display:table-header-group) makes a multi-page table read as one continuous table. */
.ts-wide table{{font-size:9.5px}}
.ts-wide thead th{{font-size:8.5px;padding:5px 4px}}
.ts-wide tbody td{{padding:4px 4px}}
/* Regulatory table: compact so the full ~18-row table + LARSO callout fit one page (no orphan tail) */
.reg table{{font-size:9px}}
.reg thead th{{font-size:8px;padding:4px 6px}}
.reg tbody td{{padding:3px 6px}}
/* Metric cards + photos: keep landscape multi-column, never split a block across a page break */
.mg4{{grid-template-columns:repeat(5,1fr);gap:8px;page-break-inside:avoid}}
.mc{{padding:12px 8px}}.mv{{font-size:17px}}.ml{{font-size:9px}}
.photo-grid{{grid-template-columns:repeat(2,1fr);gap:8px;page-break-inside:avoid;margin-bottom:16px}}
.photo-grid img{{height:2.3in}}
.exec-aerial,.loc-hero{{page-break-inside:avoid;margin-bottom:16px}}
.exec-aerial img{{height:4in;object-fit:cover}}
.loc-hero img{{height:4in;object-fit:cover}}
.cn{{page-break-inside:avoid;margin:10px 0;padding:12px 16px}}
/* Keep the contact/footer block whole on one page (logo + agents + disclaimer cohesive) */
.footer{{page-break-inside:avoid}}
/* Keep the "Property at a Glance" heading with its facts table (no orphaned heading), and give the
   fact rows more presence so the page reads as an intentional fact sheet rather than a sparse top strip */
.exec-glance{{page-break-inside:avoid}}
.exec-glance .it{{font-size:13px}}
.exec-glance .it td{{padding:13px 14px}}
/* exec-facts + returns/financing two-col stay side-by-side (fit landscape), just don't split */
.exec-facts,.two-col{{page-break-inside:avoid}}
/* Investment Highlights: PRESERVE the website's alternating side-by-side image+text rows in the PDF.
   Each row stays a flex pair with fixed image heights and break-inside:avoid so it never splits across
   a page boundary - selective layout, NOT a global flatten. */
.feat{{display:block}}
.feat-row,.feat-row.rev{{display:flex;gap:22px;align-items:center;page-break-inside:avoid;margin-bottom:20px}}
.feat-row.rev{{flex-direction:row-reverse}}
.feat-imgs{{flex:0 0 45%;display:grid;grid-template-columns:1fr;gap:8px;margin:0}}
.feat-imgs.two{{grid-template-columns:1fr 1fr}}
.feat-imgs img{{height:2.6in;width:100%;object-fit:cover}}
.feat-imgs.two img{{height:2.4in}}
.feat-text{{flex:1}}
.feat-text h4{{margin-bottom:8px}}
.feat-text li{{margin-bottom:5px;line-height:1.5}}
.hb-grid{{display:block}}
.hb{{page-break-inside:avoid;margin-bottom:12px}}
}}
</style>
</head>
<body>

<!-- ════ COVER ════ -->
<div class="cover">
<div class="cover-bg"></div>
<div class="cover-scrim"></div>
<div class="cover-content">
<img src="{logo}" alt="LAAA Team" class="cover-logo">
<div class="cover-label">Investment Offering</div>
<h1 class="cover-title">Eastwind Apartments</h1>
<p class="cover-sub">3607 Pacific Avenue &nbsp;&bull;&nbsp; Marina del Rey, CA 90292 &nbsp;&bull;&nbsp; Marina Peninsula</p>
<div class="cover-price">$5,395,000</div>
<div class="cover-stats">
<div><span class="cv">6</span><span class="cl">Units</span></div>
<div><span class="cv">5,634 SF</span><span class="cl">Building Area</span></div>
<div><span class="cv">1964 / 2025</span><span class="cl">Built / Renovated</span></div>
<div><span class="cv">0.15 Ac</span><span class="cl">Lot Size</span></div>
</div>
<p class="client-greeting" id="client-greeting">Exclusively Offered by Marcus &amp; Millichap</p>
<p class="coop-line">In Cooperation with The Erster Group</p>
<p class="cover-agent">Jonathan Erster &nbsp;|&nbsp; Glen Scher &nbsp;|&nbsp; Filip Niculete</p>
<p class="cover-date">June 2026</p>
<p class="cover-nyse">NYSE: MMI</p>
</div>
</div>

<!-- ════ TOC NAV ════ -->
<nav class="toc-nav" id="toc-nav">
<button class="nav-toggle" id="navToggle" aria-expanded="false" aria-controls="toc-links"><span class="nav-burger" aria-hidden="true">&#9776;</span><span class="nav-label">Sections</span><span class="nav-caret" aria-hidden="true">&#9662;</span></button>
<div class="toc-links" id="toc-links">
<a href="#summary">Summary</a>
<a href="#overview">Overview</a>
<a href="#highlights">Highlights</a>
<a href="#location">Location</a>
<a href="#systems">Systems</a>
<a href="#regulatory">Regulatory</a>
<a href="#financials">Financials</a>
<a href="#sale-comps">Sale Comps</a>
<a href="#rent-comps">Rent Comps</a>
<a href="#contact">Contact</a>
</div>
</nav>

<!-- ════ EXECUTIVE SUMMARY ════ -->
<div class="section" id="summary">
<div class="section-title">Executive Summary</div>
<div class="section-subtitle">Investment Offering &bull; Eastwind Apartments, Marina del Rey</div>
<div class="section-divider"></div>

<div class="mg4">
<div class="mc"><span class="mv">$5,395,000</span><span class="ml">Offering Price</span></div>
<div class="mc"><span class="mv">$899,167</span><span class="ml">Price Per Unit</span></div>
<div class="mc"><span class="mv">$957.58</span><span class="ml">Price / SF</span></div>
<div class="mc"><span class="mv">4.75% / 5.60%</span><span class="ml">Cap Rate &mdash; Yr 1 / Pro Forma</span></div>
<div class="mc"><span class="mv">14.28x / 13.34x</span><span class="ml">GRM &mdash; Yr 1 / Pro Forma</span></div>
</div>

<div class="exec-aerial">
<img src="{exec_aerial}" alt="3607 Pacific Avenue — aerial steps from the sand beside the Venice Fishing Pier and the Pacific Ocean">
<div class="caption"><strong>3607 Pacific Avenue</strong> &nbsp;&bull;&nbsp; Marina Peninsula &nbsp;&bull;&nbsp; Steps to Venice Fishing Pier &amp; the Pacific Ocean</div>
</div>

<div class="exec-glance">
<h3 class="sub-heading">Property at a Glance</h3>
<div class="exec-facts two-col">
<table class="it">
<tr><td>Address</td><td>3607 Pacific Avenue, Marina del Rey, CA 90292</td></tr>
<tr><td>Submarket</td><td>Marina Peninsula / Venice Coastal Zone</td></tr>
<tr><td>Units</td><td>6 &mdash; All 2BR/1BA</td></tr>
<tr><td>Building SF</td><td>5,634 SF (avg ~925 SF/unit)</td></tr>
<tr><td>Lot Size</td><td>0.15 Acres (6,401 SF)</td></tr>
<tr><td>Year Built / Renovated</td><td>1964 / 2025</td></tr>
</table>
<table class="it">
<tr><td>Price / SF</td><td>$957.58</td></tr>
<tr><td>Cap Rate (Yr 1 / Pro Forma)</td><td>4.75% / 5.60%</td></tr>
<tr><td>GRM (Yr 1 / Pro Forma)</td><td>14.28 / 13.34</td></tr>
<tr><td>NOI (Yr 1 / Pro Forma)</td><td>$256,355 / $301,898</td></tr>
<tr><td>Zoning</td><td>R3-1 &mdash; LARSO + AB 1482</td></tr>
<tr><td>Offering Type</td><td>Standard / Stabilized</td></tr>
</table>
</div>
</div>
</div>

<!-- ════ INVESTMENT OVERVIEW ════ -->
<div class="section section-alt" id="overview">
<div class="section-title">Investment Overview</div>
<div class="section-subtitle">Architecture by Ellis Gelman &bull; Steps from the Sand</div>
<div class="section-divider"></div>

<div class="photo-grid">
<img src="{g_main}" alt="3607 Pacific Avenue — twilight street elevation">
<img src="{g_kitchen}" alt="Open living and dining with floor-to-ceiling, wall-to-wall glass">
<img src="{g_patio}" alt="Double-height living space — Ellis Gelman architecture">
<img src="{g_sunset}" alt="Ground-floor private patio with beach-walk access">
</div>

<div class="narrative">
<p>The LAAA Team at Marcus &amp; Millichap is proud to present <strong>Eastwind Apartments</strong>, a rare architectural six-unit beach-front offering located in the heart of Marina del Rey, California, on the highly coveted <strong>Marina Peninsula</strong>, one of the most supply-constrained and sought-after coastal rental submarkets in Los Angeles. Designed by renowned Los Angeles architect Ellis Gelman, Eastwind showcases a timeless contemporary aesthetic that sets it apart from typical coastal multifamily inventory, sitting just steps from the sand on what is widely regarded as the most private and pristine stretch of beach in Los Angeles. Set within a unique beach community, the property is within walking distance of restaurants and shops, the Marina del Rey boat harbor, the Venice Fishing Pier, and the iconic Venice Canals. This is a generational opportunity to acquire a true pride-of-ownership coastal asset that simply cannot be replicated in today&rsquo;s market.</p>

<p>Built in 1964 and improved through an extensive capital-improvement program, Eastwind is comprised of six spacious 2 bed / 1 bath units averaging 925 square feet each, configured as two ground-level residences with extraordinarily large private patios offering direct, private access to the beach walk, and four upstairs residences each with its own large private roof terrace. All units have bright, open floor plans framed by floor-to-ceiling, wall-to-wall glass and appointed with modern European-style kitchens featuring stainless steel appliances and quartz countertops, along with wood flooring throughout. The property also benefits from a completed soft-story seismic retrofit, gated entry, one private parking space per unit, and in-unit laundry in four of the six units, with laundry being added to the remaining two on move-out. Eastwind is delivered in excellent condition.</p>

<p>Eastwind&rsquo;s location is what makes it truly irreplaceable. Residents enjoy a quiet, intimate beach-community setting within walking distance of the Marina del Rey boat harbor, the Venice Fishing Pier, the iconic Venice Canals, and the restaurants and shops of Washington Boulevard and Abbot Kinney. For investors, the offering pairs a Gelman architectural pedigree and rare beach-walk frontage with a clear path to additional upside: continued mark-to-market on unit turnover and the lease-up of recently renovated units. Positioned on the Marina Peninsula in one of Southern California&rsquo;s most rent-stable coastal submarkets, Eastwind offers sustained tenant demand, durable long-term value, and a quality of asset that properties on this beach simply do not bring to market.</p>
</div>
</div>

<!-- ════ INVESTMENT HIGHLIGHTS ════ -->
<div class="section" id="highlights">
<div class="section-title">Investment Highlights</div>
<div class="section-subtitle">Key Opportunity Drivers</div>
<div class="section-divider"></div>

<div class="feat">

<div class="feat-row">
<div class="feat-imgs two">
<img src="{feat_unit_a}" alt="Renovated unit kitchen — European-style cabinetry, stainless steel appliances, quartz countertops">
<img src="{feat_unit_b}" alt="Private roof terrace — one of four upstairs units">
</div>
<div class="feat-text"><h4>Unit Amenities</h4>
<ul>
<li>Bright units with floor-to-ceiling, wall-to-wall glass throughout</li>
<li>European-style kitchens with stainless steel appliances and quartz countertops</li>
<li>Wood flooring throughout</li>
<li>Spacious 2 bed / 1 bath floor plans; ground-level units feature extraordinarily large private patios with direct, private access to the beach walk</li>
<li>Upstairs units feature large private roof terraces (one per unit, four total)</li>
<li>Four units have in-unit laundry; laundry being added to the remaining two upon move-out</li>
</ul></div>
</div>

<div class="feat-row rev">
<div class="feat-imgs">
<img src="{feat_common}" alt="Gated entry and Ellis Gelman contemporary architecture at 3607 Pacific Avenue">
</div>
<div class="feat-text"><h4>Common-Area Amenities</h4>
<ul>
<li>Outstanding contemporary architecture by renowned Los Angeles architect Ellis Gelman</li>
<li>Gated entry with secured access</li>
<li>One private parking space per unit</li>
<li>Building well-maintained and delivered in excellent condition</li>
</ul></div>
</div>

<div class="feat-row">
<div class="feat-imgs">
<img src="{feat_invest}" alt="Aerial view — the subject asset steps from the sand beside the Venice Fishing Pier and Pacific Ocean">
</div>
<div class="feat-text"><h4>Investor Highlights</h4>
<ul>
<li>Soft-story (earthquake) retrofit completed; buyer inherits a structurally upgraded asset</li>
<li>Additional upside through mark-to-market rents on unit turnover</li>
<li>Subject to required jurisdictional approvals, the office and laundry space can be converted into an ADU for additional income; a seventh parking space is available to serve the ADU</li>
<li>Steps-from-sand Marina Peninsula location with exceptionally low inventory turnover</li>
</ul></div>
</div>

<div class="feat-row rev">
<div class="feat-imgs">
<img src="{feat_loc}" alt="Beach-access walk street steps from the sand on the Marina Peninsula">
</div>
<div class="feat-text"><h4>Location Highlights</h4>
<ul>
<li>Located in Marina del Rey on the exclusive Marina Peninsula, one of LA&rsquo;s most supply-constrained coastal rental submarkets</li>
<li>Steps from the sand on the most private, pristine beach in Los Angeles</li>
<li>Walking distance to the Marina del Rey boat harbor</li>
<li>Walking distance to the Venice Fishing Pier</li>
<li>Walking distance to the iconic Venice Canals</li>
<li>Walking distance to the restaurants, shops, and nightlife of Washington Boulevard, and minutes to the restaurants, shops, and nightlife of Abbot Kinney Boulevard</li>
</ul></div>
</div>

</div>
</div>

<!-- ════ LOCATION OVERVIEW ════ -->
<div class="section section-alt" id="location">
<div class="section-title">Location Overview</div>
<div class="section-subtitle">A Beachfront Walk Street Within Steps of Marina del Rey&rsquo;s Premier Amenities</div>
<div class="section-divider"></div>

<div class="loc-hero"><img src="{context}" alt="3607 Pacific Avenue — Marina Del Rey context aerial showing Marina del Rey Harbor, Burton Chace Park, Fisherman's Village, Mothers Beach, and beach access"></div>

<div class="narrative">
<h3 class="sub-heading">Marina del Rey &amp; the Marina Peninsula</h3>
<p>Eastwind Apartments occupies one of the most coveted pieces of coastal Los Angeles real estate: the <strong>Marina Peninsula</strong> in Marina del Rey, a narrow strip of beachfront residential community wedged between the open Pacific Ocean and North America&rsquo;s largest man-made small-craft harbor. Marina del Rey is renowned as a premier destination for waterfront living and recreation, home to more than 5,000 boats and a vibrant collection of resort-style hotels, dockside dining, and outdoor recreation that includes sailing, kayaking, paddleboarding, and dining cruises. Located just four miles north of LAX and approximately twelve miles from downtown Los Angeles, the area pairs small-town coastal charm with immediate access to one of the nation&rsquo;s largest metropolitan economies. Land-based amenities include the 22-mile Marvin Braude Coastal Bike Trail, Burton Chace Park (a 10-acre harborfront park hosting free summer concerts), Mother&rsquo;s Beach, Fisherman&rsquo;s Village, and the Villa Marina and Waterside shopping and dining centers.</p>

<p>The Marina Peninsula itself is defined by quiet, low-traffic walk streets, a powerful sense of neighborhood, and an architectural fabric dominated by single-family homes, small luxury condominiums, and a tightly held inventory of intimately scaled apartment buildings. Inventory turnover is exceptionally low; the combination of geographic constraint, restrictive zoning, and pride-of-ownership stewardship has made the Peninsula a true rarity among Westside rental submarkets.</p>

<h3 class="sub-heading">Adjacent Venice</h3>
<p>Immediately to the north, the Marina Peninsula flows into the iconic neighborhood of Venice. Founded in 1905 by Abbot Kinney as a coastal resort town and annexed by Los Angeles in 1926, Venice is one of the most culturally distinctive and economically vital neighborhoods in the Los Angeles metro. Known for its bohemian spirit, its world-famous Ocean Front Walk, its iconic canals, and its modernist residential architecture, Venice draws an estimated 28,000 to 30,000 visitors daily and more than ten million annually, a tourism engine that supports a deep, year-round demand base within walking distance of Eastwind. Abbot Kinney Boulevard, ranked among the most influential retail streets in the country, anchors the area&rsquo;s upscale lifestyle layer with stylish boutiques, artisanal coffee shops, and destination dining, while the Venice Canals, the Venice Fishing Pier, Muscle Beach, and the Venice Beach Recreation Center round out a recreational footprint few residential submarkets can match.</p>
</div>
</div>

<!-- ════ BUILDING SYSTEMS ════ -->
<div class="section" id="systems">
<div class="section-title">Building Systems &amp; Renovations</div>
<div class="section-subtitle">Stabilized Property &bull; Capital Improvements Complete</div>
<div class="section-divider"></div>

<div class="narrative">
<p>Eastwind Apartments has been comprehensively renovated and brought into full compliance with Los Angeles seismic, building, and rent stabilization requirements. The largest single capital item for a 1964-era multifamily property, the soft-story retrofit, was completed in March 2024 with a Certificate of Compliance issued by LADBS. The units have been renovated with modern European-style kitchens, quartz countertops, stainless steel appliances, and wood flooring; in-unit laundry is in place in four of the six units and is being added to the remaining two on move-out.</p>
</div>

<div class="ts ts-wide"><table>
<thead><tr><th>System / Improvement</th><th>Status</th><th>Detail</th></tr></thead>
<tbody>
<tr><td>Soft-Story Seismic Retrofit</td><td><span class="badge-done">Completed</span></td><td>Certificate of Compliance issued 3/26/2024 (LADBS Permit 23016-10000-30898) &mdash; LABC Ch. 93 wood shear wall</td></tr>
<tr><td>Unit Renovations</td><td><span class="badge-done">Completed</span></td><td>European-style kitchens, quartz countertops, stainless steel appliances, wood flooring throughout</td></tr>
<tr><td>Roof / Reroof</td><td><span class="badge-done">Completed</span></td><td>Reroof + hot-mop work; permit finalized 1/22/2004</td></tr>
<tr><td>Windows &amp; Doors</td><td><span class="badge-done">Completed</span></td><td>Window and door replacement; permit finalized 1/22/2004</td></tr>
<tr><td>Perimeter Block Wall</td><td><span class="badge-done">Completed</span></td><td>6-foot concrete block wall, 69 linear feet (8/13/2002)</td></tr>
<tr><td>Electrical &mdash; Intercom</td><td><span class="badge-done">Completed</span></td><td>Low-voltage intercom conduits (4/3/2002)</td></tr>
<tr><td>Gated Entry</td><td><span class="badge-done">In Place</span></td><td>Secured access controls common areas</td></tr>
<tr><td>In-Unit Laundry</td><td><span class="badge-done">4 of 6 In Place</span></td><td>Four units have in-unit laundry; laundry being added to the remaining two upon move-out</td></tr>
<tr><td>Parking</td><td><span class="badge-done">In Place</span></td><td>1 private space per unit</td></tr>
<tr><td>Private Roof Terraces</td><td><span class="badge-done">In Place</span></td><td>Four upstairs units, one large private roof terrace each</td></tr>
<tr><td>Ground-Floor Patios</td><td><span class="badge-done">In Place</span></td><td>Two ground-level units, extraordinarily large private patios with direct beach-walk access</td></tr>
<tr><td>Office-to-ADU Conversion</td><td><span class="badge-opp">Future Opportunity</span></td><td>Subject to required jurisdictional approvals, the office and laundry space can be converted into an ADU for additional income; a seventh parking space is available to serve the ADU. Buyer to investigate post-close</td></tr>
</tbody></table></div>
</div>

<!-- ════ REGULATORY ════ -->
<div class="section section-alt" id="regulatory">
<div class="section-title">Regulatory &amp; Zoning Profile</div>
<div class="section-subtitle">Los Angeles &bull; Venice Coastal Zone &bull; Marina Peninsula Subarea</div>
<div class="section-divider"></div>

<div class="ts reg"><table>
<thead><tr><th>Item</th><th>Status / Detail</th></tr></thead>
<tbody>
<tr><td>Zoning</td><td>R3-1 (Multifamily Residential)</td></tr>
<tr><td>General Plan Land Use</td><td>Medium Residential</td></tr>
<tr><td>Community Plan</td><td>Venice</td></tr>
<tr><td>Council District</td><td>CD 11</td></tr>
<tr><td>Specific Plan</td><td>Venice Coastal Zone &mdash; Marina Peninsula subarea + LA Coastal Transportation Corridor</td></tr>
<tr><td>Coastal Zone Designation</td><td><strong>Calvo Exclusion Area</strong> (simplified coastal development permitting)</td></tr>
<tr><td>Rent Stabilization (LARSO)</td><td>Yes &mdash; subject property is subject to the LA Rent Stabilization Ordinance</td></tr>
<tr><td>State Rent Cap (AB 1482)</td><td>Applicable as backstop to LARSO</td></tr>
<tr><td>Soft-Story Retrofit</td><td>Completed &mdash; CofC issued 3/26/2024</td></tr>
<tr><td>Flood Zone</td><td>Outside Flood Zone</td></tr>
<tr><td>Very High Fire Hazard Severity Zone</td><td>No</td></tr>
<tr><td>Hillside</td><td>No</td></tr>
<tr><td>Methane Zone</td><td>Yes (standard for Marina Peninsula)</td></tr>
<tr><td>Liquefaction Zone</td><td>Yes (standard for low-lying coastal Marina Peninsula parcels)</td></tr>
<tr><td>Tsunami Hazard Area</td><td>Yes (standard for Marina Peninsula coastal parcels)</td></tr>
<tr><td>Nearest Active Fault</td><td>Santa Monica Fault &mdash; approximately 4.1 miles (6.6 km)</td></tr>
<tr><td>Oil Well Adjacency</td><td>Plugged well within 100 ft (per LA City records)</td></tr>
<tr><td>TCAC Opportunity Area</td><td>Highest</td></tr>
<tr><td>Police / Fire</td><td>LAPD Pacific Division / LAFD Battalion 4, Station 63</td></tr>
</tbody></table></div>

<div class="cn">
<strong>LARSO Note:</strong> 3607 Pacific Avenue is subject to the Los Angeles Rent Stabilization Ordinance (LARSO), which limits annual rent increases on existing tenancies in accordance with the LA Housing Department&rsquo;s annual allowable adjustment. New tenancies may be set at market rent upon vacancy. AB 1482 (California Tenant Protection Act) applies as a state-level backstop. Buyer should conduct an independent review of LARSO compliance during due diligence.
</div>
</div>

<!-- ════ FINANCIAL ANALYSIS ════ -->
<div class="section" id="financials">
<div class="section-title">Financial Analysis</div>
<div class="section-subtitle">Operating Performance &amp; Returns at $5,395,000</div>
<div class="section-divider"></div>

<h3 class="sub-heading">Rent Roll</h3>
<div class="ts ts-wide"><table class="fin-num-2">
<thead><tr><th>Unit</th><th>Unit Type</th><th>Size SF</th><th>Current Rent</th><th>Current $/SF</th><th>Pro Forma Rent</th><th>PF $/SF</th></tr></thead>
<tbody>
<tr><td>1</td><td>2 Bed / 1 Bath</td><td>900</td><td>$5,850</td><td>$6.50</td><td>$6,000</td><td>$6.67</td></tr>
<tr><td>2</td><td>2 Bed / 1 Bath</td><td>900</td><td>$5,450</td><td>$6.06</td><td>$5,800</td><td>$6.44</td></tr>
<tr><td>3</td><td>2 Bed / 1 Bath</td><td>900</td><td>$5,245</td><td>$5.83</td><td>$5,600</td><td>$6.22</td></tr>
<tr><td>4</td><td>2 Bed / 1 Bath</td><td>900</td><td>$5,145</td><td>$5.72</td><td>$5,500</td><td>$6.11</td></tr>
<tr><td>5</td><td>2 Bed / 1 Bath</td><td>900</td><td>$4,945</td><td>$5.49</td><td>$5,400</td><td>$6.00</td></tr>
<tr><td>6</td><td>2 Bed / 1 Bath</td><td>900</td><td>$4,845</td><td>$5.38</td><td>$5,400</td><td>$6.00</td></tr>
<tr style="font-weight:700;background:#e8edf3"><td colspan="2">Total / Wtd Avg</td><td style="text-align:right">5,634</td><td style="text-align:right">$31,480</td><td style="text-align:right">$5.59</td><td style="text-align:right">$33,700</td><td style="text-align:right">$5.98</td></tr>
<tr style="font-weight:700;background:#e8edf3"><td colspan="3">Gross Annualized Rents</td><td style="text-align:right">$377,760</td><td></td><td style="text-align:right">$404,400</td><td></td></tr>
</tbody></table></div>

<h3 class="sub-heading">Operating Statement</h3>
<div class="ts"><table class="fin-num">
<thead><tr><th>Income</th><th>Current</th><th>Pro Forma</th><th>Per Unit</th><th>Per SF</th></tr></thead>
<tbody>
<tr><td>Gross Scheduled Rent</td><td>$377,760</td><td>$404,400</td><td>$67,400</td><td>$71.78</td></tr>
<tr><td>Physical Vacancy (3.0%)</td><td>($11,333)</td><td>($12,132)</td><td>($2,022)</td><td>($2.15)</td></tr>
<tr style="font-weight:600"><td>Effective Rental Income</td><td>$366,427</td><td>$392,268</td><td>$65,378</td><td>$69.63</td></tr>
<tr><td>ADU Income (Pro Forma)</td><td>$0</td><td>$21,600</td><td>$3,600</td><td>$3.83</td></tr>
<tr style="font-weight:700;background:#e8edf3"><td>Effective Gross Income</td><td>$366,427</td><td>$413,868</td><td>$68,978</td><td>$73.46</td></tr>
</tbody></table></div>

<div class="ts"><table class="fin-num">
<thead><tr><th>Expenses</th><th>Current</th><th>Pro Forma</th><th>Per Unit</th><th>Per SF</th></tr></thead>
<tbody>
<tr><td>Real Estate Taxes</td><td>$65,819</td><td>$65,819</td><td>$10,970</td><td>$11.68</td></tr>
<tr><td>Insurance</td><td>$5,000</td><td>$5,000</td><td>$833</td><td>$0.89</td></tr>
<tr><td>Utilities &mdash; LADWP</td><td>$6,783</td><td>$6,783</td><td>$1,131</td><td>$1.20</td></tr>
<tr><td>Trash Removal</td><td>$4,393</td><td>$4,393</td><td>$732</td><td>$0.78</td></tr>
<tr><td>Repairs &amp; Maintenance</td><td>$5,200</td><td>$5,200</td><td>$867</td><td>$0.92</td></tr>
<tr><td>Weekly Landscape &amp; Maintenance</td><td>$4,800</td><td>$4,800</td><td>$800</td><td>$0.85</td></tr>
<tr><td>Pest Control</td><td>$330</td><td>$330</td><td>$55</td><td>$0.06</td></tr>
<tr><td>LA City Fees</td><td>$1,590</td><td>$1,590</td><td>$265</td><td>$0.28</td></tr>
<tr><td>Misc. Expenses</td><td>$1,500</td><td>$1,500</td><td>$250</td><td>$0.27</td></tr>
<tr><td>Management Fee (4% of GSR)</td><td>$14,657</td><td>$16,555</td><td>$2,759</td><td>$2.94</td></tr>
<tr style="font-weight:700;background:#e8edf3"><td>Total Expenses</td><td>$110,072</td><td>$111,970</td><td>$18,662</td><td>$19.87</td></tr>
<tr><td>Expenses as % of EGI</td><td>30.0%</td><td>27.1%</td><td>&mdash;</td><td>&mdash;</td></tr>
<tr style="font-weight:700;font-size:15px;background:#e8edf3"><td>Net Operating Income</td><td style="color:#1B3A5C">$256,355</td><td style="color:#2E7D32">$301,898</td><td>$50,316</td><td>$53.59</td></tr>
</tbody></table></div>

<div class="two-col" style="margin-top:30px">
<div>
<h3 class="sub-heading">Returns at $5,395,000</h3>
<table class="fin-num">
<thead><tr><th>Metric</th><th>Year 1</th><th>Pro Forma</th></tr></thead>
<tbody>
<tr><td>Cap Rate</td><td>4.75%</td><td style="color:#2E7D32;font-weight:600">5.60%</td></tr>
<tr><td>GRM</td><td>14.28x</td><td>13.34x</td></tr>
<tr><td>Cash-on-Cash</td><td>3.50%</td><td style="color:#2E7D32;font-weight:600">5.19%</td></tr>
<tr><td>Debt Coverage Ratio</td><td>1.58</td><td>1.87</td></tr>
<tr><td>Net Cash Flow After DS</td><td>$94,505</td><td>$140,048</td></tr>
<tr><td>Total Return</td><td>3.50%</td><td>5.19%</td></tr>
</tbody></table>
</div>
<div>
<h3 class="sub-heading">Financing Assumption</h3>
<table>
<thead><tr><th style="width:50%">Term</th><th>Detail</th></tr></thead>
<tbody>
<tr><td style="font-weight:600;color:#1B3A5C;width:50%">Loan Amount</td><td>$2,697,500 (50% LTV)</td></tr>
<tr><td style="font-weight:600;color:#1B3A5C">Loan Type</td><td><strong>Interest Only</strong></td></tr>
<tr><td style="font-weight:600;color:#1B3A5C">Interest Rate</td><td>6.00%</td></tr>
<tr><td style="font-weight:600;color:#1B3A5C">Year Due</td><td>2029 (5-Year Term)</td></tr>
<tr><td style="font-weight:600;color:#1B3A5C">Annual Debt Service</td><td>$161,850</td></tr>
<tr><td style="font-weight:600;color:#1B3A5C">Principal Reduction</td><td>$0</td></tr>
</tbody></table>
</div>
</div>

<div class="cn">
<strong>Financing:</strong> Loan terms shown reflect a representative interest-only assumption. Loan information is subject to change. Contact your Marcus &amp; Millichap Capital Corporation representative for current financing options tailored to your acquisition strategy.
</div>
</div>

<!-- ════ SALE COMPARABLES ════ -->
<div class="section section-alt" id="sale-comps">
<div class="section-title">Comparable Sales</div>
<div class="section-subtitle">Recent Closed Transactions &bull; Marina Peninsula &amp; Venice</div>
<div class="section-divider"></div>

<div id="saleMap" class="gmap"></div>
<p class="map-fallback">Map image unavailable &mdash; view the interactive map at the live listing URL.</p>

<div class="ts ts-wider"><table class="fin-r5">
<thead><tr><th>#</th><th>Property</th><th>City</th><th>Date</th><th>Price</th><th>Units</th><th>$/Unit</th><th>$/SF</th><th>Cap</th><th>GRM</th><th>Yr Built</th></tr></thead>
<tbody>
<tr class="hl"><td>&star;</td><td><strong>3607 Pacific Avenue</strong></td><td><strong>Marina Del Rey</strong></td><td>On Market</td><td><strong>$5,395,000</strong></td><td><strong>6</strong></td><td><strong>$899,167</strong></td><td><strong>$957.58</strong></td><td><strong>4.75%</strong></td><td><strong>14.28</strong></td><td><strong>1964/2025</strong></td></tr>
<tr><td>A</td><td>440 Howland Canal</td><td>Venice</td><td>05/13/2024</td><td>$2,135,000</td><td>5</td><td>$427,000</td><td>$1,108.52</td><td>4.38%</td><td>15.52</td><td>1924</td></tr>
<tr><td>B</td><td>124 Catamaran St</td><td>Marina Del Rey</td><td>05/16/2023</td><td>$2,775,000</td><td>7</td><td>$396,428</td><td>$436.73</td><td>5.05%</td><td>13.36</td><td>1970</td></tr>
<tr><td>C</td><td>101 Catamaran St</td><td>Marina Del Rey</td><td>04/29/2025</td><td>$3,000,000</td><td>6</td><td>$500,000</td><td>$529.94</td><td>5.71%</td><td>12.25</td><td>1964</td></tr>
<tr><td>D</td><td>16 Fleet St</td><td>Marina Del Rey</td><td>08/30/2023</td><td>$4,825,000</td><td>10</td><td>$482,500</td><td>$600.12</td><td>3.90%</td><td>17.31</td><td>1971</td></tr>
<tr><td>E</td><td>1426 Main St</td><td>Venice</td><td>06/26/2025</td><td>$4,565,000</td><td>7</td><td>$652,142</td><td>$693.03</td><td>6.72%</td><td>10.12</td><td>1962</td></tr>
<tr><td>F</td><td>2201 Ocean Ave</td><td>Venice</td><td>07/29/2025</td><td>$4,750,000</td><td>10</td><td>$475,000</td><td>$338.68</td><td>5.68%</td><td>11.44</td><td>1975</td></tr>
<tr><td>G</td><td>315 Vernon Ave</td><td>Venice</td><td>05/02/2025</td><td>$5,050,000</td><td>6</td><td>$841,666</td><td>$1,046.42</td><td>5.04%</td><td>13.89</td><td>1922</td></tr>
<tr style="font-weight:700;background:#e8edf3"><td colspan="6">Average &mdash; 7 closed comps</td><td style="text-align:right">$539,248</td><td style="text-align:right">$679.06</td><td style="text-align:right">5.21%</td><td style="text-align:right">13.41</td><td></td></tr>
<tr style="font-weight:700;background:#e8edf3"><td colspan="6">Median</td><td style="text-align:right">$482,500</td><td style="text-align:right">$600.12</td><td style="text-align:right">5.05%</td><td style="text-align:right">13.36</td><td></td></tr>
</tbody></table></div>

<div class="narrative">
<p>The closest pricing anchor is <strong>315 Vernon Avenue</strong> in Venice, a 6-unit property that closed for $5,050,000 on May 2, 2025 at a 5.04% cap rate and 13.89 GRM &mdash; identical unit count, comparable submarket, and a nearly identical $/SF profile ($1,046 vs. subject $958). Both 315 Vernon and 3607 Pacific occupy the premium tier of small-balance coastal multifamily inventory.</p>

<p><strong>101 Catamaran Street</strong> sold for $3,000,000 in April 2025 at a 5.71% cap rate &mdash; a same-vintage (1964), same-unit-count Marina Del Rey property providing a direct comparability anchor on building characteristics. The subject&rsquo;s superior renovation status, soft-story retrofit completion, and architectural pedigree support the pricing premium reflected in the offering.</p>

<p>The surrounding Venice and Marina Peninsula transactions confirm a market range of $338 to $1,108 per square foot, with cap rates predominantly in the 4.4% to 5.7% range. At $957.58/SF and a 4.75% cap rate (5.60% pro forma), the subject is positioned within the premium-tier coastal anchor range supported by the most directly comparable transactions.</p>
</div>
</div>

<!-- ════ RENT COMPARABLES ════ -->
<div class="section" id="rent-comps">
<div class="section-title">Rent Comparables</div>
<div class="section-subtitle">2BR Rental Market &bull; Marina Peninsula &amp; Venice</div>
<div class="section-divider"></div>

<div id="rentMap" class="gmap"></div>
<p class="map-fallback">Map image unavailable &mdash; view the interactive map at the live listing URL.</p>

<div class="ts"><table class="fin-r5">
<thead><tr><th>#</th><th>Property</th><th>City / ZIP</th><th>Unit Type</th><th>Size SF</th><th>Rent</th><th>Rent/SF</th></tr></thead>
<tbody>
<tr class="hl"><td>&star;</td><td><strong>3607 Pacific Avenue (Subject)</strong></td><td><strong>Marina Del Rey 90292</strong></td><td><strong>2BR/1BA</strong></td><td><strong>900</strong></td><td><strong>$5,617 PF Avg</strong></td><td><strong>$6.24</strong></td></tr>
<tr><td>1</td><td>3900 Pacific Avenue</td><td>Marina Del Rey 90292</td><td>2BR/1BA</td><td>1,000</td><td>$5,500</td><td>$5.50</td></tr>
<tr><td>2</td><td>3512 Pacific Avenue</td><td>Marina Del Rey 90292</td><td>2BR/2BA</td><td>917</td><td>$5,500</td><td>$6.00</td></tr>
<tr><td>3</td><td>3003 Ocean Front Walk</td><td>Venice 90291</td><td>2BR/1BA</td><td>700</td><td>$5,500</td><td>$7.86</td></tr>
<tr style="font-weight:700;background:#e8edf3"><td colspan="4">Average &mdash; 3 comps</td><td style="text-align:right">872</td><td style="text-align:right">$5,500</td><td style="text-align:right">$6.45</td></tr>
<tr style="font-weight:700;background:#e8edf3"><td colspan="4">Median</td><td style="text-align:right">917</td><td style="text-align:right">$5,500</td><td style="text-align:right">$6.00</td></tr>
</tbody></table></div>

<div class="narrative">
<p>The three closest comparable 2BR rentals on the Marina Peninsula and adjacent Venice corridors all achieve <strong>$5,500/month</strong>. The subject&rsquo;s pro forma rents (averaging $5,617/month, $6.24/SF) reflect modest upside above the immediate market &mdash; supported by the property&rsquo;s renovated interiors, architectural pedigree, private roof terrace, gated entry, and one private parking space per unit. The closest direct comparable, <strong>3003 Ocean Front Walk</strong>, achieves $7.86/SF &mdash; demonstrating the rent premium achievable for ocean-proximate 2BR product in this submarket.</p>
<p>Current in-place rents at the subject average $5,247/month ($5.83/SF), with the highest in-place unit at $5,850/month ($6.50/SF). Per-unit rents range from $4,845 to $5,850 reflecting unit-level finish variations and tenancy duration.</p>
</div>
<div class="cn">
Additional rent comparables and current LARSO compliance documentation are available through the broker team upon request and during due diligence.
</div>
</div>

<!-- ════ FOOTER (3-AGENT) ════ -->
<div class="footer" id="contact">
<img src="{logo}" alt="LAAA Team" class="footer-logo">
<div class="footer-coop">Exclusively Offered by Marcus &amp; Millichap in Cooperation with The Erster Group</div>
<div class="footer-team">

<div class="fp fp-yoni">
<img src="{hs_yoni}" alt="Jonathan Erster">
<span class="fpn">Jonathan Erster</span>
<span class="fpt">Co-Listing Broker</span>
<span class="fpfirm">The Erster Group</span>
<span class="fpd">(818) 943-8002<br><a href="mailto:Jonathan@TheErsterGroup.com">Jonathan@TheErsterGroup.com</a><br>License: CA 01906424</span>
</div>

<div class="fp fp-glen">
<img src="{hs_glen}" alt="Glen Scher">
<span class="fpn">Glen Scher</span>
<span class="fpt">Senior Managing Director Investments</span>
<span class="fpfirm">Marcus &amp; Millichap</span>
<span class="fpd">(818) 212-2808<br><a href="mailto:Glen.Scher@marcusmillichap.com">Glen.Scher@marcusmillichap.com</a><br>License: CA 01962976</span>
</div>

<div class="fp fp-filip">
<img src="{hs_filip}" alt="Filip Niculete">
<span class="fpn">Filip Niculete</span>
<span class="fpt">Senior Managing Director Investments</span>
<span class="fpfirm">Marcus &amp; Millichap</span>
<span class="fpd">(818) 212-2748<br><a href="mailto:Filip.Niculete@marcusmillichap.com">Filip.Niculete@marcusmillichap.com</a><br>License: CA 01905352</span>
</div>

</div>
<div class="fo">16830 Ventura Blvd, Ste. 100, Encino, CA 91436 &nbsp;|&nbsp; <a href="https://laaa.com">laaa.com</a></div>
<div class="fd">This information has been secured from sources we believe to be reliable, but we make no representations or warranties, expressed or implied, as to the accuracy of the information. Buyer must verify the information and bears all risk for any inaccuracies. Any rent or income information in this offering memorandum, with the exception of actual historical rent collections, represents good-faith projections of potential future rent only, and Marcus &amp; Millichap makes no representations as to whether such rent may actually be attainable. Marcus &amp; Millichap Real Estate Investment Services, Inc. | License: CA 01930580.</div>
</div>

<!-- Download PDF button removed 2026-06-01 — print/PDF output (page breaks, maps) needs a proper print stylesheet first; re-add when fixed. -->

<!-- ════ JAVASCRIPT ════ -->
<script>
// Optional client param
var params=new URLSearchParams(window.location.search);
var client=params.get('client');
if(client){{
  var el=document.getElementById('client-greeting');
  if(el)el.textContent='Prepared Exclusively for '+client;
}}

// Mobile nav: tap-to-open menu (collapsed hamburger on narrow screens)
var navWrap=document.getElementById('toc-nav'), navToggle=document.getElementById('navToggle');
if(navToggle){{navToggle.addEventListener('click',function(){{
  var open=navWrap.classList.toggle('open');
  navToggle.setAttribute('aria-expanded', open?'true':'false');
}});}}

// Smooth scroll for TOC (closes the mobile menu first so the offset is correct)
document.querySelectorAll('.toc-links a').forEach(function(link){{
  link.addEventListener('click',function(e){{
    e.preventDefault();
    navWrap.classList.remove('open');
    if(navToggle)navToggle.setAttribute('aria-expanded','false');
    var t=document.querySelector(this.getAttribute('href'));
    if(t){{
      var h=document.getElementById('toc-nav').offsetHeight;
      window.scrollTo({{top:t.getBoundingClientRect().top+window.pageYOffset-h-4,behavior:'smooth'}});
    }}
  }});
}});

// Active TOC link highlighting
var tocLinks=document.querySelectorAll('.toc-links a'),tocSections=[];
tocLinks.forEach(function(l){{
  var id=l.getAttribute('href').substring(1);
  var s=document.getElementById(id);
  if(s)tocSections.push({{link:l,section:s}});
}});
function updateToc(){{
  var h=document.getElementById('toc-nav').offsetHeight+20;
  var sp=window.pageYOffset+h, cur=null;
  tocSections.forEach(function(i){{if(i.section.offsetTop<=sp)cur=i.link;}});
  tocLinks.forEach(function(l){{l.classList.remove('toc-active');}});
  if(cur)cur.classList.add('toc-active');
}}
window.addEventListener('scroll',updateToc);
updateToc();

// Hide Download PDF button when footer is in view
(function(){{
  var btn=document.querySelector('.download-btn');
  var footer=document.getElementById('contact');
  if(!btn||!footer||!('IntersectionObserver' in window))return;
  var io=new IntersectionObserver(function(entries){{
    entries.forEach(function(e){{
      btn.classList.toggle('is-hidden', e.isIntersecting);
    }});
  }},{{rootMargin:'0px 0px -20% 0px'}});
  io.observe(footer);
}})();

// SVG marker icon helper for Google Maps (subject = gold star, comps = navy circles w/ label)
function gmIcon(color, label, sz){{
  sz = sz || 30;
  var svg;
  if(label === '★'){{
    svg = '<svg xmlns="http://www.w3.org/2000/svg" width="'+sz+'" height="'+sz+'" viewBox="0 0 '+sz+' '+sz+'"><circle cx="'+(sz/2)+'" cy="'+(sz/2)+'" r="'+(sz/2-2)+'" fill="'+color+'" stroke="#fff" stroke-width="2"/><text x="50%" y="56%" text-anchor="middle" dy=".25em" fill="#fff" font-size="'+(sz*.5)+'" font-family="sans-serif">★</text></svg>';
  }} else {{
    svg = '<svg xmlns="http://www.w3.org/2000/svg" width="'+sz+'" height="'+sz+'" viewBox="0 0 '+sz+' '+sz+'"><circle cx="'+(sz/2)+'" cy="'+(sz/2)+'" r="'+(sz/2-2)+'" fill="'+color+'" stroke="#fff" stroke-width="2"/><text x="50%" y="56%" text-anchor="middle" dy=".25em" fill="#fff" font-size="'+(sz*.45)+'" font-weight="700" font-family="sans-serif">'+label+'</text></svg>';
  }}
  return {{
    url: 'data:image/svg+xml;charset=UTF-8,' + encodeURIComponent(svg),
    scaledSize: new google.maps.Size(sz, sz),
    anchor: new google.maps.Point(sz/2, sz/2)
  }};
}}

// InfoWindow content builder
function gmIWHtml(title, body, address){{
  var gmap = 'https://www.google.com/maps/search/?api=1&query=' + encodeURIComponent(address);
  return '<div class="gm-iw"><strong>' + title + '</strong><br>' + body + '<br><a class="gm-link" href="' + gmap + '" target="_blank" rel="noopener">View in Google Maps</a></div>';
}}

// ── Map data: single source for the interactive Google maps AND the static-map PDF specs ──
var __SUBJECT = {{ lat: 33.976940, lng: -118.463554, addr: '3607 Pacific Ave, Marina Del Rey, CA 90292' }};
var __SALE_VIEW = {{ center: {{ lat: 33.983, lng: -118.467 }}, zoom: 14 }};
var __RENT_VIEW = {{ center: {{ lat: 33.978, lng: -118.465 }}, zoom: 15 }};
var __SALE_COMPS = [
    [33.984375, -118.465351, 'A', '440 Howland Canal (Venice)', '5 Units &bull; $2.135M &bull; 4.38% Cap &bull; 1924', '440 Howland Canal, Venice, CA 90291'],
    [33.978540, -118.463526, 'B', '124 Catamaran St (Marina Del Rey)', '7 Units &bull; $2.775M &bull; 5.05% Cap &bull; 1970', '124 Catamaran St, Marina Del Rey, CA 90292'],
    [33.978198, -118.464361, 'C', '101 Catamaran St (Marina Del Rey)', '6 Units &bull; $3.0M &bull; 5.71% Cap &bull; 1964', '101 Catamaran St, Marina Del Rey, CA 90292'],
    [33.976375, -118.463222, 'D', '16 Fleet St (Marina Del Rey)', '10 Units &bull; $4.825M &bull; 3.90% Cap &bull; 1971', '16 Fleet St, Marina Del Rey, CA 90292'],
    [33.989251, -118.471904, 'E', '1426 Main St (Venice)', '7 Units &bull; $4.565M &bull; 6.72% Cap &bull; 1962', '1426 Main St, Venice, CA 90291'],
    [33.986827, -118.464876, 'F', '2201 Ocean Ave (Venice)', '10 Units &bull; $4.75M &bull; 5.68% Cap &bull; 1975', '2201 Ocean Ave, Venice, CA 90291'],
    [33.994493, -118.474506, 'G', '315 Vernon Ave (Venice)', '6 Units &bull; $5.05M &bull; 5.04% Cap &bull; 1922', '315 Vernon Ave, Venice, CA 90291']
  ];
var __RENT_COMPS = [
    [33.975401, -118.462194, '1', '3900 Pacific Avenue', '2BR/1BA &bull; 1,000 SF &bull; $5,500', '3900 Pacific Ave, Marina Del Rey, CA 90292'],
    [33.977516, -118.463835, '2', '3512 Pacific Avenue', '2BR/2BA &bull; 917 SF &bull; $5,500', '3512 Pacific Ave, Marina Del Rey, CA 90292'],
    [33.979560, -118.467177, '3', '3003 Ocean Front Walk', '2BR/1BA &bull; 700 SF &bull; $5,500', '3003 Ocean Front Walk, Venice, CA 90291']
  ];
// Static-map contract consumed by build_pdf.py (LAAA-AI-Prompts/reporting/build_pdf.py). Any BOV/OM
// page that wants static maps in its PDF publishes:
//   window.__STATIC_MAP_SPECS = [{{targetId, center, zoom, markers:[{{lat,lng,color,label,subject}}]}}]
function __compMarker(c){{ return {{ lat: c[0], lng: c[1], color: '0x1B3A5C', label: c[2] }}; }}
window.__STATIC_MAP_SPECS = [
  {{ targetId: 'saleMap', center: __SALE_VIEW.center, zoom: __SALE_VIEW.zoom,
     markers: [{{ lat: __SUBJECT.lat, lng: __SUBJECT.lng, color: '0xC5A258', subject: true }}].concat(__SALE_COMPS.map(__compMarker)) }},
  {{ targetId: 'rentMap', center: __RENT_VIEW.center, zoom: __RENT_VIEW.zoom,
     markers: [{{ lat: __SUBJECT.lat, lng: __SUBJECT.lng, color: '0xC5A258', subject: true }}].concat(__RENT_COMPS.map(__compMarker)) }}
];

// Builds both maps; runs when API + body are both ready (see head stub)
function __drawMaps(){{
  var subjectPos = {{ lat: __SUBJECT.lat, lng: __SUBJECT.lng }};
  var subjectAddr = __SUBJECT.addr;

  // ── Sale Comps Map ──
  var saleMap = new google.maps.Map(document.getElementById('saleMap'), {{
    center: __SALE_VIEW.center,
    zoom: __SALE_VIEW.zoom,
    mapTypeId: 'roadmap',
    mapTypeControl: true,
    mapTypeControlOptions: {{ style: google.maps.MapTypeControlStyle.HORIZONTAL_BAR, position: google.maps.ControlPosition.TOP_LEFT }},
    streetViewControl: true,
    fullscreenControl: true,
    zoomControl: true
  }});
  var saleIW = new google.maps.InfoWindow();

  new google.maps.Marker({{
    position: subjectPos,
    map: saleMap,
    icon: gmIcon('#C5A258', '★', 36),
    title: '3607 Pacific Avenue (Subject)',
    zIndex: 1000
  }}).addListener('click', function(){{
    saleIW.setContent(gmIWHtml('Subject: 3607 Pacific Ave', '6 Units &bull; $5,395,000 &bull; 4.75% Cap', subjectAddr));
    saleIW.open(saleMap, this);
  }});

  var saleComps = __SALE_COMPS;
  saleComps.forEach(function(c){{
    var marker = new google.maps.Marker({{
      position: {{ lat: c[0], lng: c[1] }},
      map: saleMap,
      icon: gmIcon('#1B3A5C', c[2], 28),
      title: c[3]
    }});
    marker.addListener('click', function(){{
      saleIW.setContent(gmIWHtml(c[3], c[4], c[5]));
      saleIW.open(saleMap, marker);
    }});
  }});

  // ── Rent Comps Map ──
  var rentMap = new google.maps.Map(document.getElementById('rentMap'), {{
    center: __RENT_VIEW.center,
    zoom: __RENT_VIEW.zoom,
    mapTypeId: 'roadmap',
    mapTypeControl: true,
    mapTypeControlOptions: {{ style: google.maps.MapTypeControlStyle.HORIZONTAL_BAR, position: google.maps.ControlPosition.TOP_LEFT }},
    streetViewControl: true,
    fullscreenControl: true,
    zoomControl: true
  }});
  var rentIW = new google.maps.InfoWindow();

  new google.maps.Marker({{
    position: subjectPos,
    map: rentMap,
    icon: gmIcon('#C5A258', '★', 36),
    title: '3607 Pacific Avenue (Subject)',
    zIndex: 1000
  }}).addListener('click', function(){{
    rentIW.setContent(gmIWHtml('Subject: 3607 Pacific Ave', '2BR/1BA &bull; $5,617 PF avg &bull; $6.24/SF', subjectAddr));
    rentIW.open(rentMap, this);
  }});

  var rentComps = __RENT_COMPS;
  rentComps.forEach(function(c){{
    var marker = new google.maps.Marker({{
      position: {{ lat: c[0], lng: c[1] }},
      map: rentMap,
      icon: gmIcon('#1B3A5C', c[2], 28),
      title: c[3]
    }});
    marker.addListener('click', function(){{
      rentIW.setContent(gmIWHtml(c[3], c[4], c[5]));
      rentIW.open(rentMap, marker);
    }});
  }});
}}
window.__drawMaps = __drawMaps;
if (window.__mapsReady) __drawMaps();  // API already fired its callback before this script ran

// PDF readiness flag — build_pdf.py waits for this (if present) before printing.
(function(){{ function r(){{ window.__PDF_READY = true; }} if (document.readyState === 'complete') r(); else window.addEventListener('load', r); }})();
</script>
</body></html>'''

with open(OUT, 'w', encoding='utf-8') as f:
    f.write(html)

sz = os.path.getsize(OUT)/1024
print(f"Wrote {OUT} ({sz:.0f} KB)")
