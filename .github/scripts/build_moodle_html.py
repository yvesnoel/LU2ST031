"""
Génère des fichiers HTML autonomes pour Moodle à partir du HTML JupyterBook.

Stratégie : inline TOUS les fichiers CSS référencés par <link rel="stylesheet">
pour un rendu identique au site JupyterBook, sans aucune dépendance externe.

- Admonitions MyST déjà rendues par Sphinx
- Images embarquées en base64
- Tous les CSS lus depuis _build/html/_static/ et inlinés
- MathJax conditionnel (CDN, ne se charge pas si Moodle l'a déjà)
- Navigation / sidebar supprimées
"""
import pathlib, base64, sys, re
from bs4 import BeautifulSoup

build_dir = pathlib.Path('_build/html')
moodle_dir = pathlib.Path('dist/moodle')
static_dir = build_dir / '_static'

# ── MathJax conditionnel ─────────────────────────────────────────────────────
MATHJAX = """<script>
/* Charge MathJax uniquement si pas déjà présent (Moodle l'a souvent) */
if (typeof MathJax === "undefined") {
  window.MathJax = {
    tex: {
      inlineMath: [["\\\\(","\\\\)"]],
      displayMath: [["\\\\[","\\\\]"]]
    },
    options: { skipHtmlTags: ["script","noscript","style","textarea","pre"] }
  };
  var s = document.createElement("script");
  s.src = "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js";
  s.async = true;
  document.head.appendChild(s);
}
</script>"""

# ── CSS minimal de recadrage pour intégration Moodle ─────────────────────────
MOODLE_OVERRIDE = """<style>
/* Recadrage pour intégration Moodle - masque navigation et sidebar */
body { overflow-x: hidden !important; }
.bd-sidebar-primary, .bd-sidebar-secondary,
.prev-next, .bd-footer, nav.bd-links,
#navbar-icon-links, .topbar, #main-nav,
.bd-header, header.bd-header,
#pst-primary-sidebar-modal, #pst-secondary-sidebar-modal,
[aria-label="previous page"], [aria-label="next page"],
.footer, footer { display: none !important; }
.bd-main { padding-left: 0 !important; margin-left: 0 !important; }
.bd-content { max-width: 100% !important; padding: 0 !important; }
.bd-article-container { max-width: 900px !important; margin: 0 auto; }
article.bd-article { padding: 1rem 1.5rem 2rem !important; }
a.headerlink { display: none !important; }
.copybtn { display: none !important; }
</style>"""


def resolve_css_path(href: str, page_path: pathlib.Path) -> pathlib.Path | None:
    """
    Résout le chemin d'un fichier CSS (href relatif) par rapport à la page HTML.
    Ex : href="../_static/styles/theme.css" depuis CM1/page.html
         → _build/html/_static/styles/theme.css
    """
    # Supprime les query strings (?v=..., ?digest=...)
    clean_href = re.sub(r'\?.*$', '', href)
    # Chemin absolu depuis la page
    resolved = (page_path.parent / clean_href).resolve()
    return resolved if resolved.exists() else None


def inline_all_css(soup: BeautifulSoup, page_path: pathlib.Path) -> str:
    """Lit tous les <link rel=stylesheet> et retourne le CSS combiné."""
    css_parts = []

    # 1. Blocs <style> inline existants (ex: .pst-js-only)
    for style in soup.find_all('style'):
        txt = style.get_text()
        if txt.strip():
            # Remplace @import "basic.css" par le contenu réel si trouvé
            if '@import' in txt and 'basic.css' in txt:
                basic = (page_path.parent / '../basic.css').resolve()
                if not basic.exists():
                    basic = page_path.parent.parent / '_static' / 'basic.css'
                if basic.exists():
                    txt = re.sub(
                        r'@import\s+["\'][^"\']*basic\.css["\'];?\s*',
                        basic.read_text('utf-8') + '\n',
                        txt
                    )
            css_parts.append(txt)

    # 2. <link rel="stylesheet" href="..."> → lit le fichier et inline
    for link in soup.find_all('link', rel='stylesheet'):
        href = link.get('href', '')
        if not href or href.startswith('http'):
            continue
        css_path = resolve_css_path(href, page_path)
        if css_path and css_path.exists():
            css_parts.append(css_path.read_text('utf-8', errors='replace'))
        else:
            print(f'    CSS manquant: {href}', file=sys.stderr)

    return '<style>\n' + '\n\n'.join(css_parts) + '\n</style>'


# ── Traitement de chaque notebook ─────────────────────────────────────────────
notebooks = sorted(pathlib.Path('.').glob('CM*/*.ipynb'))
print(f'Notebooks trouvés : {len(notebooks)}')
ok, errors = 0, []

for nb_path in notebooks:
    jb_html = build_dir / nb_path.with_suffix('.html')
    if not jb_html.exists():
        print(f'  Manquant: {jb_html} — skipping', file=sys.stderr)
        errors.append(str(nb_path))
        continue

    out_dir = moodle_dir / nb_path.parent
    out_dir.mkdir(parents=True, exist_ok=True)

    soup = BeautifulSoup(jb_html.read_text('utf-8'), 'lxml')

    # ── Inline tout le CSS ───────────────────────────────────────────────────
    all_css = inline_all_css(soup, jb_html)

    # ── Extrait le contenu principal ─────────────────────────────────────────
    # JupyterBook / Sphinx Book Theme : <article class="bd-article">
    main = (soup.find('article', class_='bd-article')
            or soup.find('div', role='main')
            or soup.find('div', class_='bd-article')
            or soup.find('article')
            or soup.find('div', class_='bd-content'))

    if not main:
        print(f'  Contenu principal introuvable: {jb_html}', file=sys.stderr)
        errors.append(str(nb_path))
        continue

    # ── Supprime les éléments de navigation dans le contenu ─────────────────
    for sel in [
        '.prev-next', '.footer-item', 'a.headerlink',
        '.sd-badge', '.cell_tag', '.copybtn',
        '[aria-label="previous page"]', '[aria-label="next page"]',
        '.bd-sidebar', 'nav',
    ]:
        for el in main.select(sel):
            el.decompose()

    # ── Embarque les images locales en base64 ────────────────────────────────
    for img in main.find_all('img'):
        src = img.get('src', '')
        if src.startswith('data:') or src.startswith('http'):
            continue
        img_path = (jb_html.parent / src).resolve()
        if img_path.exists():
            ext = img_path.suffix.lstrip('.').lower()
            mime_map = {'jpg': 'jpeg', 'svg': 'svg+xml'}
            ext = mime_map.get(ext, ext)
            b64 = base64.b64encode(img_path.read_bytes()).decode()
            img['src'] = f'data:image/{ext};base64,{b64}'
        else:
            print(f'    Image manquante: {img_path}', file=sys.stderr)

    # ── Attributs data-* du tag <html> (nécessaires pour le thème) ───────────
    html_tag = soup.find('html')
    data_attrs = ''
    if html_tag:
        for k, v in html_tag.attrs.items():
            if k.startswith('data-'):
                data_attrs += f' {k}="{v}"'

    # ── Assemble le HTML final ───────────────────────────────────────────────
    title = nb_path.stem.replace('_', ' ')
    html_out = f"""<!DOCTYPE html>
<html lang="fr"{data_attrs}>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
{all_css}
{MOODLE_OVERRIDE}
{MATHJAX}
</head>
<body>
{str(main)}
</body>
</html>"""

    out_file = out_dir / (nb_path.stem + '.html')
    out_file.write_text(html_out, encoding='utf-8')
    size_kb = out_file.stat().st_size / 1024
    print(f'  OK: {out_file}  ({size_kb:.0f} Ko)')
    ok += 1

print(f'\nTerminé : {ok} OK, {len(errors)} erreurs')
if errors:
    print('Erreurs :', errors, file=sys.stderr)
    sys.exit(1)
