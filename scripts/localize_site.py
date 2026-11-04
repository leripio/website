"""Add static, page-matched language links and localize shared Quarto navigation.

Runs automatically after `quarto render`; uses only Python's standard library.
The translated content lives in the *-pt.qmd source pages.
"""
import os
import re
from pathlib import Path

OUTPUT = Path(os.environ.get("QUARTO_PROJECT_OUTPUT_DIR", "_site"))
PAGES = ("index", "services", "talks", "resume", "thank-you")
LABELS = {"About": "Sobre", "Work with me": "Trabalhe comigo", "Book": "Livro",
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
                    anchor = anchor.replace('nav-link active', 'nav-link')
                    anchor = re.sub(r'\s+aria-current="page"', '', anchor)
                    if name == page:
                        anchor = anchor.replace('class="nav-link"', 'class="nav-link active" aria-current="page"')
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
        label = "Mudar para inglês" if portuguese else "Switch to Portuguese"
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
        text = text[:header_match.start()] + header + text[header_match.end():]
        if portuguese:
            text = text.replace('Built with <a href="https://quarto.org">Quarto</a>', 'Criado com <a href="https://quarto.org">Quarto</a>')
        alternates = ''.join(f'<link data-language-alternate="true" rel="alternate" hreflang="{lang}" href="./{page}{ext}.html">\n'
                             for lang, ext in (("en", ""), ("pt-BR", "-pt"), ("x-default", "")))
        text = re.sub(r'\s*</head>', lambda _: '\n' + STYLE + '\n' + alternates + '</head>', text, count=1)
        path.write_text(text)
print("Localized navigation and language buttons for English and Portuguese pages.")
