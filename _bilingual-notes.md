# English and Brazilian Portuguese

English remains at the original URLs. Portuguese source pages use a `-pt`
suffix: `index-pt.qmd`, `services-pt.qmd`, `talks-pt.qmd`, and `resume-pt.qmd`.
Both versions share the same styles, images, and presentation data.

Edit the corresponding source page in each language when changing content.
The translations are authored content, not automatic browser translations.
Presentation titles and book titles remain in their original language.

Run `quarto render` from this directory to build the complete site. Python 3
is required for the post-render script; no additional Python packages are needed.
`scripts/localize_site.py` adds page-matched PT/EN links, translates the shared
navigation and footer, and adds alternate-language metadata. The links work
without JavaScript; a small click handler also carries the current section hash.
Navigation within the site stays in the chosen language. External book and
presentation links keep their original destinations.

The language link is placed next to the theme control, outside the collapsible
navigation, so it remains available on mobile. It names the destination language:
PT on English pages, EN on Portuguese pages.

When adding a new translated page, add its base name to `PAGES` in the
post-render script and add its Portuguese navigation label to `LABELS` if needed.
