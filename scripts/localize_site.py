"""Add static, page-matched language links and localize shared Quarto navigation.

Runs automatically after `quarto render`; uses only Python's standard library.
The translated content lives in the *-pt.qmd source pages.
"""
import os
import re
import hashlib
from pathlib import Path

OUTPUT = Path(os.environ.get("QUARTO_PROJECT_OUTPUT_DIR", "_site"))
PAGES = ("index", "services", "talks", "resume", "thank-you")
LABELS = {"About": "Sobre", "How I can help": "Como posso ajudar", "Book": "Livro",
          "Talks": "Palestras", "Resume": "Currículo"}
STYLE = """<style id="language-switch-style">
.language-switch { display:inline-flex; align-items:center; gap:.35rem; margin-right:.65rem;
 padding:.25rem .65rem; border:1px solid var(--border); border-radius:100px;
 font-size:.75rem; font-weight:600; color:var(--text-muted); text-decoration:none; white-space:nowrap; }
.language-switch:hover { color:var(--accent); border-color:var(--accent); }
.language-switch:focus-visible { outline:3px solid var(--accent); outline-offset:3px; }
.language-switch .language-flag { font-size:1rem; line-height:1; }
@media(max-width:400px) { .language-switch { margin-right:.25rem; padding:.25rem .45rem; } }
</style>"""

for page in PAGES:
    for portuguese in (False, True):
        suffix = "-pt" if portuguese else ""
        path = OUTPUT / f"{page}{suffix}.html"
        if not path.exists():
            continue
        text = path.read_text()
        # Refresh page-specific CSS after edits, including in local browser previews.
        def version_style(match):
            asset = OUTPUT / match[2]
            digest = hashlib.sha256(asset.read_bytes()).hexdigest()[:10]
            return match[1] + match[2] + '?v=' + digest + match[3]
        text = re.sub(r'(href=")(about-page\.css|services-page\.css|resume-page\.css)(?:\?v=[a-f0-9]+)?(")', version_style, text)
        # Remove generated additions before processing an existing output again.
        text = re.sub(r'<style id="language-switch-style">.*?</style>', '', text, flags=re.S)
        text = re.sub(r'<link data-language-alternate="true"[^>]*>\s*', '', text)
        text = re.sub(r'<a\b[^>]*\bclass="language-switch"[^>]*>.*?</a>', '', text, flags=re.S)
        header_match = re.search(r'<header id="quarto-header".*?</header>', text, re.S)
        if not header_match:
            raise RuntimeError(f"Missing Quarto navigation in {path}")
        header = header_match.group()

        def localize_link(match):
            anchor = match.group()
            target = re.search(r'href="(?:\./)?(index|services|talks|resume)(?:-pt)?\.html"', anchor)
            if target:
                name = target[1]
                anchor = anchor[:target.start()] + f'href="./{name}{suffix}.html"' + anchor[target.end():]
                if 'class="nav-link' in anchor:
                    anchor = anchor.replace('class="nav-link services-nav-link', 'class="nav-link', 1)
                    anchor = anchor.replace('nav-link active', 'nav-link')
                    anchor = re.sub(r'\s+aria-current="page"', '', anchor)
                    if name == page:
                        anchor = anchor.replace('class="nav-link"', 'class="nav-link active" aria-current="page"')
                    if name == "services":
                        anchor = anchor.replace('class="nav-link', 'class="nav-link services-nav-link', 1)
            if portuguese:
                for en, pt in LABELS.items():
                    anchor = anchor.replace(f'<span class="menu-text">{en}</span>', f'<span class="menu-text">{pt}</span>')
            return anchor

        header = re.sub(r'<a\b[^>]*>.*?</a>', localize_link, header, flags=re.S)
        if portuguese:
            header = header.replace('aria-label="Toggle navigation"', 'aria-label="Abrir navegação"')
            header = header.replace('title="Toggle dark mode"', 'title="Alternar tema claro e escuro"')
            header = header.replace('title="Search"', 'title="Pesquisar"')
        other_suffix = "" if portuguese else "-pt"
        label = "Read in English" if portuguese else "Ver em português"
        other_language = "en" if portuguese else "pt-BR"
        button_text = "EN" if portuguese else "PT"
        flag = "🇬🇧" if portuguese else "🇧🇷"
        switch = (f'<a class="language-switch" href="./{page}{other_suffix}.html" '
                  f'lang="{other_language}" hreflang="{other_language}" aria-label="{label}" '
                  f'title="{label}" onclick="this.hash=window.location.hash">'
                  f'<span class="language-flag" aria-hidden="true">{flag}</span> {button_text}</a>')
        marker = '<div class="quarto-navbar-tools">'
        if marker not in header:
            raise RuntimeError(f"Missing navbar tools in {path}")
        header = header.replace(marker, marker + switch, 1)
        header = re.sub(r'\s+target="_blank"', '', header)
        header = header.replace(
            'href="https://r4er.rleripio.com"',
            'href="https://r4er.rleripio.com" target="_blank" rel="noopener"',
        )
        text = text[:header_match.start()] + header + text[header_match.end():]
        if portuguese:
            text = text.replace('Built with <a href="https://quarto.org">Quarto</a>', 'Criado com <a href="https://quarto.org">Quarto</a>')
        alternates = ''.join(f'<link data-language-alternate="true" rel="alternate" hreflang="{lang}" href="./{page}{ext}.html">\n'
                             for lang, ext in (("en", ""), ("pt-BR", "-pt"), ("x-default", "")))
        text = re.sub(r'\s*</head>', lambda _: '\n' + STYLE + '\n' + alternates + '</head>', text, count=1)
        if page == "resume":
            # Leave fragment links, interactive controls, and email actions in place.
            header_end = text.index("</header>", header_match.start()) + len("</header>")
            text = text[:header_end] + re.sub(
                r'<a\b(?=[^>]*\bhref="(?!(?:#|mailto:|javascript:))[^"]+")(?![^>]*\btarget=)',
                '<a target="_blank" rel="noopener"',
                text[header_end:],
            )
        path.write_text(text)
print("Localized navigation and language buttons for English and Portuguese pages.")


# Publish explicit language paths while retaining Quarto's root outputs for
# partial renders and legacy URLs. All assets remain shared at the site root.
from urllib.parse import urlsplit

def language_url(page, language):
    return f"/{language}/" + ("" if page == "index" else f"{page}.html")

def route_attribute(match, language):
    attribute, value = match[1], match[2]
    url = urlsplit(value)
    if url.scheme or url.netloc or not url.path or url.path.startswith("/"):
        return match[0]
    relative = url.path.removeprefix("./")
    page_match = re.fullmatch(r"(index|services|talks|resume|thank-you)(-pt)?\.html", relative)
    if page_match:
        target_language = "pt" if page_match[2] else language
        target = language_url(page_match[1], target_language)
    else:
        target = "/" + relative
    if url.query:
        target += "?" + url.query
    if url.fragment:
        target += "#" + url.fragment
    return f'{attribute}="{target}"'

redirects = []
for page in PAGES:
    for language, suffix in (("en", ""), ("pt", "-pt")):
        source = OUTPUT / f"{page}{suffix}.html"
        if not source.exists():
            continue
        text = source.read_text()
        text = re.sub(r'<script src="/language.js"></script>\s*', "", text)
        text = re.sub(r'<link rel="canonical"[^>]*>\s*', "", text)
        text = text.replace("<head>", '<head>\n<script src="/language.js"></script>', 1)
        source.write_text(text)
        localized = re.sub(r'(href|src|action)="([^"]+)"',
                           lambda m: route_attribute(m, language), text)
        # The language switch always points to the equivalent page.
        other = "en" if language == "pt" else "pt"
        localized = re.sub(r'(<a class="language-switch" href=")[^"]+',
                           lambda m: m[1] + language_url(page, other), localized)
        localized = re.sub(r'<link data-language-alternate="true"[^>]*>\s*', "", localized)
        links = "".join(
            f'<link data-language-alternate="true" rel="alternate" hreflang="{tag}" href="{language_url(page, lang)}">\n'
            for tag, lang in (("en", "en"), ("pt-BR", "pt"), ("x-default", "en"))
        )
        localized = localized.replace("</head>",
            f'<link rel="canonical" href="https://www.rleripio.com{language_url(page, language)}">\n' + links + "</head>", 1)
        destination = OUTPUT / language / f"{page}.html"
        destination.parent.mkdir(exist_ok=True)
        destination.write_text(localized)
        if page != "index" or suffix:
            for extension in (".html", ""):
                redirects.append(f"/{page}{suffix}{extension} {language_url(page, language)} 301")
(OUTPUT / "_redirects").write_text("\n".join(redirects) + "\n")
