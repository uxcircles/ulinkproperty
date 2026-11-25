"""Self-hosted web fonts. Run after editing Chinese text (no dependencies):

    python3 _build/pages.py && python3 _build/fonts.py

- Big Shoulders Display 600-900 (prices, headings): Google's Latin subset
- Atkinson Hyperlegible 400/700 (English body): Latin subset
- LXGW WenKai TC 700 (Chinese headings, marker-pen price tags) and Noto Sans TC 400/700:
  only the characters used on the site
"""
import glob, html, os, re, urllib.parse, urllib.request

BUILD = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BUILD)
OUT = os.path.join(ROOT, "assets", "fonts")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
API = "https://fonts.googleapis.com/css2?"


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA})).read()


def latin_src(css):
    for comment, block in re.findall(r"/\* ([\w-]+) \*/\s*@font-face \{(.*?)\}", css, re.S):
        if comment == "latin":
            return re.search(r"url\((.*?)\)", block).group(1)
    raise SystemExit("latin block not found")


def save(name, data):
    os.makedirs(OUT, exist_ok=True)
    open(os.path.join(OUT, name + ".woff2"), "wb").write(data)
    print(f"{name}.woff2  {len(data) // 1024} KB")


def cjk():
    chars = set()
    files = glob.glob(os.path.join(ROOT, "*.html")) + glob.glob(os.path.join(ROOT, "en", "*.html")) + [os.path.join(ROOT, "assets", "site.js")]
    for f in files:
        chars.update(ch for ch in html.unescape(open(f, encoding="utf-8").read()) if ord(ch) > 0x2E7F)
    chars.update("，。：；！？（）「」、·…０１２３４５６７８９")
    return "".join(sorted(chars))


def subset(family, w, text, name):
    css = get(API + f"family={family}:wght@{w}&display=swap&text=" + urllib.parse.quote(text)).decode()
    save(name, get(re.search(r"url\((.*?)\)", css).group(1)))


if __name__ == "__main__":
    save("big-shoulders", get(latin_src(get(API + "family=Big+Shoulders+Display:wght@600..900&display=swap").decode())))
    for w in (400, 700):
        save(f"atkinson-{w}", get(latin_src(get(API + f"family=Atkinson+Hyperlegible:wght@{w}&display=swap").decode())))
    text = cjk()
    subset("LXGW+WenKai+TC", 700, text, "wenkai-tc-700")
    for w in (400, 700):
        subset("Noto+Sans+TC", w, text, f"noto-sans-tc-{w}")
    print(len(text), "characters")
