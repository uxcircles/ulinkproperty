"""Build the ULINK Property Services concept site (no dependencies).

    python3 _build/pages.py && python3 _build/fonts.py

Traditional Chinese (Hong Kong wording) at /, English at /en/.
Every string is written as L(english, chinese).
"""
import json
import os

BUILD = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BUILD)
V = "1"  # cache-bust: bump on every CSS/JS change

LANG = "zh"


def L(en, zh):
    return zh if LANG == "zh" else en


# ------------------------------------------------------------------ facts (sources in README)
EMAIL = "info@ulinkproperty.co.uk"
FB = "https://www.facebook.com/ulinkps"
MSG = "https://m.me/ulinkps"
OFFICIAL = "https://www.ulinkproperty.co.uk/"
UXC = "https://ux-circles.com/professionals"
BASE = "https://uxcircles.github.io/ulinkproperty/"
COMPANY = "12359766"
HOME = [-2.9553686, 53.4245782]  # L5 6PU postcode centroid (OpenStreetMap Nominatim)
ANFIELD = [-2.9608, 53.4308]     # Anfield stadium (OpenStreetMap)

LANGS = [("zh", "", "中文", "zh-Hant-HK"), ("en", "en/", "EN", "en-GB")]
HTML_LANG = {"zh": "zh-Hant-HK", "en": "en-GB"}


def tagmark(cls="tagmark", label=None):
    """The signature: a Hong Kong market price tag, hole punched, on a string."""
    aria = f'role="img" aria-label="{label}"' if label else 'aria-hidden="true"'
    return (f'<svg class="{cls}" viewBox="0 0 64 64" {aria}>'
            '<path class="tm-card" d="M14 6h36a4 4 0 0 1 4 4v44a4 4 0 0 1-4 4H14a4 4 0 0 1-4-4V10a4 4 0 0 1 4-4Z"/>'
            '<circle class="tm-hole" cx="32" cy="15" r="4"/>'
            '<path class="tm-u" d="M22 26v14a10 10 0 0 0 20 0V26"/></svg>')


def tag(label, price, note="", body="", cls=""):
    n = f'<span class="tag-note">{note}</span>' if note else ""
    b = f'<p class="tag-body">{body}</p>' if body else ""
    return (f'<div class="tag {cls}"><span class="tag-hole" aria-hidden="true"></span>'
            f'<span class="tag-label">{label}</span><b class="tag-price">{price}</b>{n}{b}</div>')


def img(src, alt, w, h, cls="", lazy=True, prefix=""):
    lz = ' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high"'
    c = f' class="{cls}"' if cls else ""
    return f'<img{c} src="{prefix}assets/img/{src}" alt="{alt}" width="{w}" height="{h}"{lz}>'


# ------------------------------------------------------------------ shared pieces
def head(prefix, slug, title, desc):
    target = "" if slug == "index.html" else slug
    alts = "".join(f'<link rel="alternate" hreflang="{h}" href="{BASE}{d}{target}">\n' for _, d, _, h in LANGS)
    zh_pre = ""
    if LANG == "zh":
        zh_pre = f'<link rel="preload" href="{prefix}assets/fonts/wenkai-tc-700.woff2" as="font" type="font/woff2" crossorigin>\n'
    return f'''<!doctype html>
<html lang="{HTML_LANG[LANG]}" class="l-{LANG}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{title}</title>
<meta name="description" content="{desc}">
{alts}<link rel="alternate" hreflang="x-default" href="{BASE}{target}">
<link rel="icon" href="{prefix}assets/img/favicon.svg" type="image/svg+xml">
<meta name="theme-color" content="#0e5a45">
<link rel="preload" href="{prefix}assets/fonts/big-shoulders.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{prefix}assets/fonts/atkinson-400.woff2" as="font" type="font/woff2" crossorigin>
{zh_pre}<link rel="stylesheet" href="{prefix}assets/site.css?v={V}">
<script defer src="{prefix}assets/site.js?v={V}"></script>
</head>
'''


def concept_bar():
    # Copied from uxcircles-concept-site/templates/concept-bar.html. Do not reword.
    arrow = ('<svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2" '
             'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17 17 7M9 7h8v8"/></svg>')
    if LANG == "zh":
        return f'''<div class="concept-bar" role="note">
  <div class="concept-inner">
    <p class="concept-text"><span class="concept-tag">概念</span><span class="concept-long">概念設計展示，並非<a href="{OFFICIAL}" target="_blank" rel="noopener">英聯物業管理官方網站</a>。</span></p>
    <a class="concept-credit" href="{UXC}" target="_blank" rel="noopener"><span class="concept-by">設計：</span><strong>UX CIRCLES</strong>{arrow}</a>
  </div>
</div>
'''
    return f'''<div class="concept-bar" role="note">
  <div class="concept-inner">
    <p class="concept-text"><span class="concept-tag">Concept</span><span class="concept-long">Redesign concept. Not the <a href="{OFFICIAL}" target="_blank" rel="noopener">official ULINK Property Services website</a>.</span></p>
    <a class="concept-credit" href="{UXC}" target="_blank" rel="noopener"><span class="concept-by">Designed by </span><strong>UX CIRCLES</strong>{arrow}</a>
  </div>
</div>
'''


def concept_note():
    if LANG == "zh":
        return f'<p class="concept-note">非官方概念設計：<a href="{UXC}" target="_blank" rel="noopener">UX CIRCLES</a></p>'
    return f'<p class="concept-note">Unofficial redesign concept by <a href="{UXC}" target="_blank" rel="noopener">UX CIRCLES</a></p>'


def nav_items():
    return [
        ("services.html", L("Services &amp; fees", "服務及收費")),
        ("airbnb.html", L("Airbnb", "Airbnb 管家")),
        ("team.html", L("Team", "團隊")),
        ("contact.html", L("Contact", "聯絡")),
    ]


def lang_links(prefix, slug, cls):
    target = "" if slug in ("index.html", "404.html") else slug
    out = []
    for code, d, label, h in LANGS:
        cur = ' aria-current="true"' if code == LANG else ""
        out.append(f'<a href="{prefix}{d}{target}" lang="{h}" hreflang="{h}"{cur}>{label}</a>')
    return f'<div class="{cls}">' + "".join(out) + "</div>"


def header(prefix, pg, slug):
    links = "".join(f'<a href="{pg}{h}"{" aria-current=page" if h == slug else ""}>{t}</a>' for h, t in nav_items())
    mlinks = "".join(f'<a href="{pg}{h}">{t}</a>' for h, t in nav_items())
    return f'''<body>
<a class="skip" href="#main">{L("Skip to content", "跳至內容")}</a>
{concept_bar()}<header class="site-head">
  <div class="wrap head-in">
    <a class="brand" href="{pg}index.html">
      {tagmark("brand-mark")}
      <span class="brand-zh" lang="zh-Hant-HK">英聯物業管理</span>
      <span class="brand-en" lang="en">ULINK Property Services</span>
    </a>
    <nav class="nav" aria-label="{L('Main', '主選單')}">{links}</nav>
    {lang_links(prefix, slug, "langs")}
    <a class="head-cta" href="{pg}contact.html">{L("Ask a question", "查詢")}</a>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="menu">{L("Menu", "選單")}</button>
  </div>
  <div class="menu" id="menu" hidden>
    <nav class="wrap menu-in" aria-label="{L('Menu', '選單')}">{mlinks}{lang_links(prefix, slug, "menu-langs")}</nav>
  </div>
</header>
'''


def footer(prefix, pg, slug):
    return f'''<footer class="site-foot">
  <div class="wrap foot-in">
    <div class="foot-brand">
      {tagmark("foot-mark")}
      <p><strong lang="zh-Hant-HK">英聯物業管理</strong><br><span lang="en">ULINK Property Services Limited</span></p>
    </div>
    <div class="foot-col">
      <p>299 Breck Road, Liverpool L5 6PU<br><a href="mailto:{EMAIL}">{EMAIL}</a><br><a href="{FB}" target="_blank" rel="noopener">Facebook @ULINKPS</a></p>
    </div>
    <div class="foot-col">
      <p>{L("Registered in England, company no. ", "英格蘭註冊公司，公司號碼 ")}{COMPANY}<br>
      {L("Member of the Property Redress Scheme. Registered with the ICO.", "Property Redress Scheme 會員，已於 ICO 登記。")}</p>
      <p><a href="{pg}privacy.html">{L("Privacy", "私隱政策")}</a> · {lang_links(prefix, slug, "foot-langs")}</p>
    </div>
  </div>
  <div class="wrap">{concept_note()}</div>
</footer>
<nav class="mbar" aria-label="{L('Quick actions', '快捷操作')}">
  <a href="mailto:{EMAIL}">{L("Email", "電郵")}</a>
  <a href="{MSG}" target="_blank" rel="noopener">{L("Messenger", "Facebook 訊息")}</a>
  <a class="mbar-main" href="{pg}index.html#calc">{L("Fees", "計收費")}</a>
</nav>
</body>
</html>
'''


def page(slug, title, desc, body, extra=""):
    prefix = "" if LANG == "zh" else "../"
    pg = ""
    if slug == "404.html":
        pg = BASE + ("" if LANG == "zh" else "en/")
        prefix = BASE
    return head(prefix, slug, title, desc) + header(prefix, pg, slug) + f'<main id="main">\n{body}\n</main>\n{extra}' + footer(prefix, pg, slug)


# ------------------------------------------------------------------ home
def calculator(p):
    return f'''<section class="hero" aria-labelledby="h1">
  <div class="wrap hero-top">
    <h1 id="h1">{L("Every fee, written on the tag", "<span class=nb>每項收費，</span><span class=nb>寫明喺價錢牌上</span>")}</h1>
    <p class="lede">{L("Type your rent or price: see what we charge and what you keep.",
                       "輸入數字，即刻睇我哋收幾多、你袋幾多。")}</p>
  </div>
  <div class="hero-stage">
    {img("house.webp", L("Brick semi-detached house with a for-sale sign", "掛住「出售」牌的紅磚半獨立屋"), 1600, 1200, "hero-photo", lazy=False, prefix=p)}
    <div class="wrap">
      <form class="board" id="calc" aria-label="{L('Fee calculator', '收費計算機')}" onsubmit="return false">
        <div class="board-in">
          <fieldset class="modes">
            <legend class="sr">{L("Service", "服務")}</legend>
            <label><input type="radio" name="mode" value="let" checked><span>{L("Letting", "長租")}</span></label>
            <label><input type="radio" name="mode" value="bnb"><span>Airbnb</span></label>
            <label><input type="radio" name="mode" value="buy"><span>{L("Buying", "買樓")}</span></label>
          </fieldset>
          <div class="fields">
            <label class="f" data-for="let"><span>{L("Monthly rent", "每月租金")}</span><span class="money"><i>£</i><input id="c-rent" type="number" inputmode="numeric" min="0" step="10" value="750"></span></label>
            <label class="f" data-for="bnb" hidden><span>{L("Per night", "每晚租金")}</span><span class="money"><i>£</i><input id="c-night" type="number" inputmode="numeric" min="0" step="5" value="85"></span></label>
            <label class="f" data-for="bnb" hidden><span>{L("Nights a month", "每月入住晚數")}</span><span class="money"><input id="c-nights" type="number" inputmode="numeric" min="0" max="31" step="1" value="18"></span></label>
            <label class="f" data-for="buy" hidden><span>{L("Property price", "樓價")}</span><span class="money"><i>£</i><input id="c-price" type="number" inputmode="numeric" min="0" step="1000" value="120000"></span></label>
            <label class="f f-rate"><span>£1 = HK$</span><span class="money"><input id="c-rate" type="number" inputmode="decimal" min="1" step="0.1" value="10.4"></span></label>
          </div>
          <div class="string" aria-live="polite" id="c-out"></div>
        </div>
        <p class="board-note">{L("An estimate from our published fees.", "按公佈收費估算，以報價為準。")}</p>
      </form>
    </div>
  </div>
</section>
'''


def home():
    pg = ""
    p = "" if LANG == "zh" else "../"
    s = calculator(p)
    s += f'''<section class="strip" aria-label="{L('Liverpool', '利物浦')}">
  <div class="wrap strip-in">
    <figure>{img("anfield-street.webp", L("Terraced street in Liverpool with a football mural", "利物浦一條有足球壁畫的排屋街"), 1200, 799, prefix=p)}<figcaption>{L("Our office is on Breck Road, near Anfield", "辦公室喺 Breck Road，近 Anfield 球場")}</figcaption></figure>
    <figure>{img("keys.webp", L("House keys passed from one hand to another", "交收鎖匙"), 900, 1125, prefix=p)}<figcaption>{L("From the offer to the keys", "由出價到拎鎖匙")}</figcaption></figure>
    <figure>{img("liver-building.webp", L("The clock towers of the Royal Liver Building", "利物浦皇家利物大廈鐘樓"), 900, 1125, prefix=p)}<figcaption>{L("Liverpool, 9,600 km from Hong Kong", "利物浦，離香港 9,600 公里")}</figcaption></figure>
  </div>
</section>

<section class="sec tags-sec" aria-labelledby="h-fees">
  <div class="wrap">
    <h2 id="h-fees">{L("Five services, five prices", "五項服務，五個價錢")}</h2>
    <p class="intro">{L("No hard sell, and nothing added later. Pay after the work is done where shown.", "唔 hard sell，唔會事後加錢。註明「後付」嘅，做完先收。")}</p>
    <div class="rack">
      {tag(L("Viewing report", "睇樓報告"), "HK$450", L("pay after the viewing", "睇完先俾"), L("Street, every room, meters and pipes on video, plus our view on the price.", "街道、每間房、電錶水錶煤氣錶全部拍片，附價錢意見。"))}
      {tag(L("Buying service", "買樓一條龍"), "1%", L("of the price, on completion", "樓價，成交後付"), L("Offer, agent, solicitor and paperwork, all the way to the keys.", "出價、地產代理、律師、文件，直到拎鎖匙。"))}
      {tag(L("Tenant find", "搵租客"), L("1 month", "一個月租"), L("of rent", "租金"), L("Rent advice, photos, listing, viewings, tenancy agreement, deposit registration.", "建議租金、影相、放盤、帶睇、租約、按金登記。"))}
      {tag(L("Full management", "全方位管理"), "12%", L("of the rent", "租金"), L("Tenants, repairs and the deposit claim when they leave.", "聯絡租客、安排維修，退租時處理按金索償。"))}
      {tag("Airbnb", "15% <small>+ VAT</small>", L("of bookings", "訂房收入"), L("Listing, pricing, cleaning, check-in and replies around the clock.", "上架、定價、清潔、check-in，24 小時回覆。"), "tag-red")}
    </div>
    <p class="more"><a class="btn" href="{pg}services.html">{L("What each fee includes", "每項收費包括乜嘢")}</a></p>
  </div>
</section>

<section class="sec viewing" aria-labelledby="h-view">
  <div class="wrap view-in">
    <figure class="view-photo">{img("hallway.webp", L("Bright hallway of a house, front door at the end", "屋內走廊，盡頭係大門"), 1200, 1500, prefix=p)}</figure>
    <div>
      <h2 id="h-view">{L("We view it for you, for HK$450", "HK$450，我哋代你去睇樓")}</h2>
      <p class="intro">{L("Send us the listing link. We book the viewing with the agent and film:", "將放盤連結發俾我哋，我哋約地產代理，現場拍片：")}</p>
      <ol class="report">
        <li>{L("The street, and whether houses nearby stand empty", "街道環境，附近有冇空置屋")}</li>
        <li>{L("Every room and the back garden", "全屋每間房同後花園")}</li>
        <li>{L("Electricity, water and gas meters, and the pipes", "電錶、水錶、煤氣錶同喉管")}</li>
        <li>{L("Signs of leaks, with a repair estimate", "有冇漏水，附維修預算")}</li>
        <li>{L("Parking, garage or driveway", "泊車位或車房")}</li>
        <li>{L("Our view: is the price right, is it worth buying", "結論：價錢合唔合理，值唔值得買")}</li>
      </ol>
    </div>
  </div>
</section>

<section class="band" aria-labelledby="h-band">
  {img("terrace.webp", L("Row of red-brick terraced houses with parked cars", "一排紅磚排屋"), 1600, 1066, "band-photo", prefix=p)}
  <div class="wrap band-in">
    <h2 id="h-band">{L("Found one? We take it to the keys", "睇中咗？我哋跟到拎鎖匙")}</h2>
    <p>{L("Offer, agent, solicitor, paperwork and completion, for 1% of the price, paid when the sale completes.", "出價、同地產代理傾、搵律師、跟文件到收樓，收樓價 1%，成交後先付。")}</p>
  </div>
</section>

<section class="sec bnb" aria-labelledby="h-bnb">
  <div class="wrap bnb-in">
    <div>
      {img("superhost.webp", "Airbnb Superhost", 600, 408, "badge", prefix=p)}
      <h2 id="h-bnb">{L("Airbnb, from renovation to check-in", "Airbnb，由裝修到接客")}</h2>
      <blockquote lang="en"><p>“Fast communication! … The home was very clean and had clear listed instructions on how to operate everything.”</p>
        <cite>{L("Michael, from FL, USA, guest review", "住客評價：Michael，美國佛羅里達")}</cite></blockquote>
      <p><a class="btn" href="{pg}airbnb.html">{L("How Airbnb management works", "Airbnb 管家點運作")}</a></p>
    </div>
    <figure>{img("airbnb-room.webp", L("Hotel-style room with a dark quilted wall and brass lamp", "深色牆身、銅燈的客房"), 1600, 1066, prefix=p)}</figure>
  </div>
</section>

<section class="sec team-sec" aria-labelledby="h-team">
  <div class="wrap team-in">
    <figure>{img("hong-kong.webp", L("Hong Kong skyline and Victoria Harbour at dusk", "黃昏的維多利亞港"), 1600, 1066, prefix=p)}</figure>
    <div>
      <h2 id="h-team">{L("Buying in Liverpool since 2016", "2016 年起喺利物浦買樓")}</h2>
      <p class="intro">{L("We started as Hong Kong investors here ourselves, so we know which questions you will have.", "我哋自己都係香港投資者，知道人喺香港買英國樓會遇到乜嘢問題。")}</p>
      <ul class="names">
        <li><b>Bryan Wong</b> {L("buying and conversions", "買樓改建")}</li>
        <li><b>Evan Wong</b> {L("lettings, rules and tenants", "出租法規同租客")}</li>
        <li><b>Hugo Wong</b> {L("repairs and renovation team", "維修同本地裝修團隊")}</li>
      </ul>
      <p><a class="btn btn-line" href="{pg}team.html">{L("Meet the team", "認識團隊")}</a></p>
    </div>
  </div>
</section>
''' + location(p)
    return page("index.html",
                L("ULINK Property Services | Liverpool property management for Hong Kong owners", "英聯物業管理 ULINK | 利物浦睇樓、買樓、收租、Airbnb 管家"),
                L("Liverpool viewings, buying, letting and Airbnb management with fees on the page.", "利物浦睇樓、買樓、收租同 Airbnb 管家，收費全部寫明。"), s, map_data())


def map_data():
    d = {"home": HOME, "mark": BASE + "assets/img/favicon.svg",
         "label": L("ULINK, 299 Breck Road", "英聯物業 299 Breck Road"),
         "places": [{"at": ANFIELD, "name": L("Anfield", "Anfield 球場")}]}
    return f'<script type="application/json" id="map-data">{json.dumps(d, ensure_ascii=False)}</script>\n'


def location(p):
    return f'''<section class="sec where" aria-labelledby="h-where">
  <div class="wrap where-in">
    <div class="mapcard" data-map>
      <svg class="map-fallback" viewBox="0 0 600 420" role="img" aria-label="{L('Sketch map: 299 Breck Road, near Anfield', '示意圖：299 Breck Road，近 Anfield 球場')}">
        <rect width="600" height="420" fill="#eef0ea"/>
        <path d="M-10 300 C150 270 330 250 610 140" stroke="#fff" stroke-width="22" fill="none"/>
        <path d="M200 -10 L260 430" stroke="#fff" stroke-width="12" fill="none"/>
        <rect x="330" y="40" width="150" height="110" rx="16" fill="#d9e4d4"/>
        <text x="405" y="102" text-anchor="middle" font-size="18" fill="#3c4a40">Anfield</text>
        <text x="80" y="268" font-size="16" fill="#3c4a40" transform="rotate(-8 80 268)">Breck Road</text>
        <circle cx="300" cy="248" r="12" fill="#c8102e"/>
      </svg>
    </div>
    <div class="where-text">
      <h2 id="h-where">299 Breck Road, Liverpool</h2>
      <p>{L("Our office is in Liverpool, so someone local can be at your property the same week.", "辦公室喺利物浦本地，有事同一個星期就可以上門。")}</p>
      <p class="addr">299 Breck Road<br>Liverpool L5 6PU<br><a href="mailto:{EMAIL}">{EMAIL}</a><br><a href="{FB}" target="_blank" rel="noopener">Facebook @ULINKPS</a></p>
      {img("anfield-gates.webp", L("The gates of Anfield stadium", "Anfield 球場大閘"), 1200, 799, "where-photo", prefix=p)}
    </div>
  </div>
</section>
'''


# ------------------------------------------------------------------ inner pages
def page_head(h1, lede, photo, alt, p):
    return f'''<section class="phead">
  <div class="wrap phead-in">
    <div><h1>{h1}</h1><p class="lede">{lede}</p></div>
    <figure>{img(photo, alt, 1600, 1066, lazy=False, prefix=p)}</figure>
  </div>
</section>
'''


def services():
    p = "" if LANG == "zh" else "../"
    s = page_head(L("Services and fees", "服務及收費"),
                  L("Four services, priced as they are on our current website.", "四項服務，收費同我哋現有網站一致。"),
                  "terrace.webp", L("Row of red-brick terraced houses", "一排紅磚排屋"), p)
    s += f'''<section class="sec svc" aria-labelledby="s1">
  <div class="wrap svc-in">
    <div class="svc-side">{tag(L("Viewing report", "睇樓報告"), "HK$450", L("no deposit, pay after the viewing", "無需預繳，睇完先俾"))}{img("hallway.webp", L("Hallway of a house", "屋內走廊"), 1200, 1500, prefix=p)}</div>
    <div>
      <h2 id="s1">{L("Viewing service", "代客睇樓")}</h2>
      <p>{L("Send us the link to a property you like. We book the viewing with the agent, film it and send you a written report.", "揀好心儀物業，將連結發俾我哋。我哋同地產代理約時間睇樓，拍片影相，再寫睇樓報告。")}</p>
      <h3>{L("Outside", "第一部分：屋外")}</h3>
      <ul><li>{L("The house front and the street", "屋外環境同街道")}</li><li>{L("The area around the property", "物業所在地區環境")}</li><li>{L("Anything that affects buying or letting, such as empty houses or how lived-in the street is", "有冇影響買賣或出租嘅問題，例如空置屋、條街多唔多人住")}</li></ul>
      <h3>{L("Inside", "第二部分：屋內")}</h3>
      <ul><li>{L("Video of every room and the back garden", "全屋拍片，連內部房間同後花園")}</li><li>{L("Electricity, water and gas meters, and the pipes", "電錶、水錶、煤氣錶、喉管")}</li><li>{L("Visible leaks or structural problems, photographed close up, with a repair estimate", "表面結構或漏水問題 close up 影相，附維修報價預算")}</li><li>{L("Parking: garage or space outside", "泊車位、車房或屋外泊車位")}</li><li>{L("Our conclusion: is the price fair, is it worth buying", "總結：價錢合唔合理，值唔值得購入")}</li></ul>
    </div>
  </div>
</section>
<section class="sec svc alt" aria-labelledby="s2">
  <div class="wrap svc-in">
    <div class="svc-side">{tag(L("Buying service", "買樓諮詢"), "1%", L("of the price, paid on completion", "樓價，無需預繳，成交後付"))}{img("keys.webp", L("House keys handed over", "交收鎖匙"), 900, 1125, prefix=p)}</div>
    <div>
      <h2 id="s2">{L("Buying, start to finish", "物業購買一條龍")}</h2>
      <p>{L("We learn what you need, then recommend and analyse properties, pros and cons both.", "了解你嘅需要，為你分析同推介物業，優點缺點都講。")}</p>
      <ol class="steps"><li>{L("Viewing", "睇樓")}</li><li>{L("Offer", "出價")}</li><li>{L("Talking to the agent", "同地產代理溝通")}</li><li>{L("Instructing a solicitor", "安排律師")}</li><li>{L("Paperwork and completion", "文件交收")}</li><li>{L("Collecting the keys", "收樓拎鎖匙")}</li></ol>
    </div>
  </div>
</section>
<section class="sec svc" aria-labelledby="s3">
  <div class="wrap svc-in">
    <div class="svc-side tag-pair">{tag(L("Tenant find", "搵租客"), L("1 month", "一個月租"), L("of rent", "租金"))}{tag(L("Management", "管理費"), "12%", L("of the rent", "租金"), cls="tag-red")}{img("anfield-street.webp", L("Terraced street in Liverpool", "利物浦排屋街"), 1200, 799, prefix=p)}</div>
    <div>
      <h2 id="s3">{L("Letting and management", "放租及全方位管理")}</h2>
      <h3>{L("Tenant find includes", "搵租客包括")}</h3>
      <ul><li>{L("Rental assessment: what rent the market will pay", "租金評估：分析市場，建議合理租金")}</li><li>{L("Photos inside and out, edited", "上門全屋內外影相，包後期執相")}</li><li>{L("Description, online listing and advertising", "撰寫描述、上網放盤、廣告宣傳")}</li><li>{L("Viewings with interested tenants", "帶有意租客睇樓")}</li><li>{L("Tenancy agreement", "準備租約文件")}</li><li>{L("Deposit registered with a government-approved scheme", "將租客按金存入政府指定機構")}</li></ul>
      <p class="small">{L("Tenant credit and background checks are charged per check by the referencing company.", "租客信貸及背景審查按次收費，由 referencing 公司收取。")}</p>
      <h3>{L("Management includes", "管理包括")}</h3>
      <ul><li>{L("Handling the tenancy and contact with tenants", "處理租務，聯絡租客")}</li><li>{L("Arranging repairs and renovation", "安排維修及裝修")}</li><li>{L("Claiming from the deposit for any damage when the tenant leaves", "退租時如有損毀，代你由按金申索賠償")}</li></ul>
    </div>
  </div>
</section>
<section class="sec svc alt" aria-labelledby="s4">
  <div class="wrap svc-in">
    <div class="svc-side">{tag("Airbnb", "15% <small>+ VAT</small>", L("of bookings, plus a cleaning fee", "訂房收入，另加清潔費"))}{img("airbnb-room.webp", L("Hotel-style guest room", "客房"), 1600, 1066, prefix=p)}</div>
    <div>
      <h2 id="s4">{L("Airbnb management", "Airbnb 管家")}</h2>
      <p>{L("Listing, pricing, cleaning, check-in, guest vetting and 24/7 replies. The cleaning fee depends on how many guests stayed; guests pay most of it.", "上架、定價、清潔、check-in、審核住客，24 小時回覆。清潔費按入住人數計，大部分由住客支付。")}</p>
      <p><a class="btn" href="airbnb.html">{L("Airbnb in detail", "Airbnb 管家詳情")}</a></p>
    </div>
  </div>
</section>
'''
    return page("services.html", L("Services and fees | ULINK Property Services", "服務及收費 | 英聯物業管理 ULINK"),
                L("Viewing HK$450, buying 1%, tenant find one month’s rent, management 12%, Airbnb 15% + VAT.", "睇樓 HK$450、買樓 1%、搵租客一個月租、管理 12%、Airbnb 15% + VAT。"), s)


def airbnb():
    p = "" if LANG == "zh" else "../"
    items = [
        (L("Online listing", "網上放盤"), L("We create the listing and adjust the price.", "由建立 listing 到調整價錢，全部包辦。")),
        (L("Maintenance and cleaning", "維修及清潔"), L("Repairs arranged; toiletries, bed linen and towels supplied if needed.", "安排維修，有需要可提供洗漱用品、床單同毛巾。")),
        (L("Guest check-in", "住客入住"), L("A smooth check-in, with house details explained.", "安排順利 check-in，講解屋內設施。")),
        (L("Guest vetting", "審核住客"), L("We review each guest against criteria you choose.", "按你訂嘅條件審核每位住客。")),
        (L("Communication", "溝通"), L("24/7 support for you and your guests.", "24 小時回覆業主同住客。")),
        (L("Utilities", "水電煤"), L("We organise utilities and look for a competitive deal.", "代辦水電煤，搵合理價錢。")),
        (L("Clear earnings", "收入清楚"), L("From 15% + VAT of bookings plus a small cleaning fee.", "訂房收入 15% + VAT 起，另加少量清潔費。")),
        (L("We do everything", "一條龍"), L("Buy, renovate, list and manage for the best return.", "買樓、翻新、上架到管理，爭取最大回報。")),
    ]
    grid = "".join(f'<li><h3>{t}</h3><p>{d}</p></li>' for t, d in items)
    s = page_head(L("Airbnb management in Liverpool", "利物浦 Airbnb 管家"),
                  L("We are Airbnb Superhosts, with a team on standby 24 hours.", "我哋係 Airbnb Superhost，團隊 24 小時 standby。"),
                  "airbnb-room.webp", L("Hotel-style room with a quilted wall", "深色牆身的客房"), p)
    s += f'''<section class="sec" aria-labelledby="a1">
  <div class="wrap">
    <h2 id="a1">{L("What we look after", "我哋負責乜嘢")}</h2>
    <ul class="grid8">{grid}</ul>
  </div>
</section>
<section class="sec alt" aria-labelledby="a2">
  <div class="wrap reviews">
    <h2 id="a2">{L("What guests wrote", "住客評價")}</h2>
    <blockquote lang="en"><p>“Bryan and Evan were great host. Fast communication! They even provided us with tips of things to do and places to eat. 10/10, A+, just wonderful!”</p><cite>Michael, from FL, USA</cite></blockquote>
    <blockquote lang="en"><p>“Evan was incredibly accommodating to a very last minute booking from me … Evan provides all the relevant information on a web link which made life very easy and the accommodation itself was perfect.”</p><cite>Jodie, from France</cite></blockquote>
    {img("pier-head.webp", L("Liverpool waterfront at sunset", "日落時的利物浦海濱"), 1600, 700, "wide", prefix=p)}
  </div>
</section>
'''
    return page("airbnb.html", L("Airbnb management | ULINK Property Services", "Airbnb 管家 | 英聯物業管理 ULINK"),
                L("Airbnb Superhost management in Liverpool from 15% + VAT.", "利物浦 Airbnb 管家，15% + VAT 起。"), s)


def team():
    p = "" if LANG == "zh" else "../"
    people = [
        ("Bryan Wong", L("Years of UK property investment; specialises in buying and converting. Interviewed by Hong Kong Economic Times iMoney about UK property.", "多年英國物業投資經驗，擅長買樓改建。曾接受經濟日報 iMoney 訪問，分享英國物業資訊。")),
        ("Evan Wong", L("Owns property across different parts of Liverpool and knows local letting rules. Runs the page 「利物浦物業投資經驗分享」.", "喺利物浦唔同地區投資物業多年，熟悉當地出租法規同處理租客。投資專頁「利物浦物業投資經驗分享」版主。")),
        ("Hugo Wong", L("A Hong Kong investor living in Liverpool, with a local renovation team for realistic repair advice and budgets before you buy.", "居於利物浦的香港投資者，有本地裝修團隊，買樓前提供實際裝修建議同預算。")),
    ]
    cards = "".join(f'<li>{tagmark("person-mark")}<h2>{n}</h2><p>{d}</p></li>' for n, d in people)
    s = page_head(L("The team", "團隊"),
                  L("Hong Kong investors who have been buying in Liverpool since 2016.", "2016 年起喺利物浦買樓嘅香港投資者。"),
                  "hong-kong.webp", L("Hong Kong skyline at dusk", "黃昏的香港"), p)
    s += f'''<section class="sec" aria-label="{L('People', '成員')}">
  <div class="wrap"><ul class="people">{cards}</ul>
  <p class="intro">{L("Honest, transparent quotes from the client’s side. We won’t exaggerate or overcharge.", "高透明度，誠實，以客人角度出發，如實報價，不會誇大和濫收費用。")}</p></div>
</section>
<section class="sec alt" aria-label="Liverpool">
  <div class="wrap">{img("liver-building.webp", L("Royal Liver Building clock towers", "皇家利物大廈鐘樓"), 900, 1125, "tall", prefix=p)}</div>
</section>
'''
    return page("team.html", L("Team | ULINK Property Services", "團隊 | 英聯物業管理 ULINK"),
                L("Bryan, Evan and Hugo Wong: Hong Kong investors in Liverpool since 2016.", "Bryan、Evan、Hugo：2016 年起喺利物浦投資的香港人。"), s)


def contact():
    p = "" if LANG == "zh" else "../"
    s = f'''<section class="sec contact" aria-labelledby="h1">
  <div class="wrap contact-in">
    <div>
      <h1 id="h1">{L("Ask us anything", "有問題，問我哋")}</h1>
      <p class="lede">{L("Tell us which service and the property, and we’ll reply by email or WhatsApp.", "話俾我哋知想用邊項服務、邊間物業，我哋會用電郵或 WhatsApp 回覆。")}</p>
      <form id="ask" class="ask" novalidate>
        <label>{L("Your name", "姓名")}<input name="name" autocomplete="name" required></label>
        <label>{L("Email or WhatsApp number", "電郵或 WhatsApp 號碼")}<input name="reach" required></label>
        <label>{L("Service", "服務")}<select name="svc">
          <option>{L("Viewing report (HK$450)", "睇樓報告（HK$450）")}</option>
          <option>{L("Buying service (1%)", "買樓一條龍（1%）")}</option>
          <option>{L("Letting and management", "放租及管理")}</option>
          <option>Airbnb</option>
          <option>{L("Something else", "其他")}</option></select></label>
        <label>{L("Property link or message", "物業連結或訊息")}<textarea name="msg" rows="4"></textarea></label>
        <p class="err" id="f-err" hidden>{L("Please add your name and how to reach you.", "請填寫姓名同聯絡方法。")}</p>
        <button class="btn" type="submit">{L("Open in my email", "用電郵發送")}</button>
        <p class="small">{L("Nothing is stored on this website; your email app opens with the message filled in.", "本網站不會儲存任何資料，按下後會開啟你的電郵程式並填好內容。")}</p>
      </form>
    </div>
    <aside class="contact-side">
      {tag(L("Email", "電郵"), "info@", "ulinkproperty.co.uk")}
      <p class="addr">299 Breck Road<br>Liverpool L5 6PU<br>United Kingdom<br><a href="mailto:{EMAIL}">{EMAIL}</a><br><a href="{FB}" target="_blank" rel="noopener">Facebook @ULINKPS</a></p>
    </aside>
  </div>
</section>
''' + location(p)
    return page("contact.html", L("Contact | ULINK Property Services", "聯絡 | 英聯物業管理 ULINK"),
                L("Email ULINK Property Services, 299 Breck Road, Liverpool L5 6PU.", "聯絡英聯物業管理：利物浦 299 Breck Road。"), s, map_data())


def privacy():
    s = f'''<section class="sec prose">
  <div class="wrap narrow">
    <h1>{L("Privacy notice", "私隱政策")}</h1>
    <p class="small">{L("Draft for ULINK to review. The current website has no privacy notice.", "草稿，待英聯審閱。現有網站並無私隱政策。")}</p>
    <h2>{L("Who we are", "我哋係邊個")}</h2>
    <p>{L(f"ULINK Property Services Limited (company no. {COMPANY}), 299 Breck Road, Liverpool L5 6PU, is the controller of your personal data and is registered with the Information Commissioner’s Office.", f"ULINK Property Services Limited（公司號碼 {COMPANY}），地址利物浦 299 Breck Road L5 6PU，為你個人資料的控制者，已於英國資訊專員辦公室（ICO）登記。")}</p>
    <h2>{L("What we collect and why", "收集乜嘢資料、點解")}</h2>
    <p>{L("Your name, contact details and property details, to answer enquiries and provide the services you ask for. For lettings we also hold tenant details needed for the tenancy and deposit protection.", "姓名、聯絡方法同物業資料，用嚟回覆查詢及提供你要求的服務。出租方面亦會保存租約及按金保障所需的租客資料。")}</p>
    <h2>{L("How long we keep it", "保存幾耐")}</h2>
    <p>{L("Only as long as needed for the service and for legal and tax records, normally six years after the service ends.", "只按服務、法律及稅務紀錄所需保存，一般為服務結束後六年。")}</p>
    <h2>{L("Your rights", "你的權利")}</h2>
    <p>{L(f"You can ask to see, correct or delete your data by emailing {EMAIL}. You can also complain to the ICO at ico.org.uk.", f"你可以電郵 {EMAIL} 要求查閱、更正或刪除資料，亦可向 ICO（ico.org.uk）投訴。")}</p>
    <h2>{L("This website", "本網站")}</h2>
    <p>{L("This concept website sets no cookies and stores nothing you type. The map loads tiles from OpenFreeMap.", "本概念網站不設 cookies，亦不會儲存你輸入的內容。地圖由 OpenFreeMap 載入。")}</p>
  </div>
</section>
'''
    return page("privacy.html", L("Privacy | ULINK Property Services", "私隱政策 | 英聯物業管理 ULINK"), L("Privacy notice.", "私隱政策。"), s)


def notfound():
    s = f'''<section class="sec nf">
  <div class="wrap nf-in">
    {tag("404", L("Sold out", "賣晒"), L("this page isn’t on the shelf", "呢版唔喺架上"), cls="tag-red tag-big")}
    <div><h1>{L("This page isn’t here", "搵唔到呢一頁")}</h1>
    <p><a class="btn" href="{BASE}{'' if LANG == 'zh' else 'en/'}index.html">{L("Back to the fees", "返去睇收費")}</a></p></div>
  </div>
</section>
'''
    return page("404.html", "404 | ULINK", "404", s)


def write(rel, text):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8").write(text)


if __name__ == "__main__":
    for code, d, _, _ in LANGS:
        LANG = code
        for slug, fn in (("index.html", home), ("services.html", services), ("airbnb.html", airbnb),
                         ("team.html", team), ("contact.html", contact), ("privacy.html", privacy)):
            write(d + slug, fn())
    LANG = "zh"
    write("404.html", notfound())
    write("robots.txt", "User-agent: *\nDisallow: /\n")
    write(".nojekyll", "")
    print("built")
