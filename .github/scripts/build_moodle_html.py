"""
Génère des fichiers HTML autonomes pour Moodle à partir du HTML JupyterBook.

Stratégie :
- Inline TOUS les CSS locaux (link rel=stylesheet) avec leurs polices/images
  embarquées en base64 (url() relatifs → data URI)
- Garde les CSS externes CDN comme <link> tags (icônes FontAwesome, etc.)
- Embarque les images du contenu en base64
- MathJax conditionnel (CDN, ne se charge pas si Moodle l'a déjà)
- Navigation / sidebar supprimées
"""
import pathlib, base64, sys, re, urllib.request, urllib.error
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
      inlineMath: [["\\(","\\)"]],
      displayMath: [["\\[","\\]"]]
    },
    options: { skipHtmlTags: ["script","noscript","style","textarea","pre"] }
  };
  var s = document.createElement("script");
  s.src = "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js";
  s.async = true;
  document.head.appendChild(s);
}
</script>"""

# ── CSS de recadrage Moodle ───────────────────────────────────────────────────
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

# ── Mime types pour les fichiers référencés en url() ─────────────────────────
FONT_MIME = {
    'woff':  'font/woff',
    'woff2': 'font/woff2',
    'ttf':   'font/ttf',
    'otf':   'font/otf',
    'eot':   'application/vnd.ms-fontobject',
}
IMG_MIME = {
    'png':  'image/png',
    'jpg':  'image/jpeg',
    'jpeg': 'image/jpeg',
    'gif':  'image/gif',
    'svg':  'image/svg+xml',
    'ico':  'image/x-icon',
}


def file_to_data_uri(path: pathlib.Path) -> str | None:
    """Convertit un fichier local en data URI base64."""
    ext = path.suffix.lstrip('.').lower()
    mime = FONT_MIME.get(ext) or IMG_MIME.get(ext)
    if mime is None:
        return None
    b64 = base64.b64encode(path.read_bytes()).decode()
    return f'data:{mime};base64,{b64}'


def fix_css_urls(css_text: str, css_file_path: pathlib.Path) -> str:
    """
    Remplace les url() relatifs dans un bloc CSS par des data URIs base64.
    Laisse intacts les url() déjà absolus (http, data:, //).
    """
    def replacer(m):
        raw = m.group(1).strip()
        # Enlève les quotes éventuelles
        url = raw.strip("'\"")
        if url.startswith(('data:', 'http', '//', '#', '')):
            return m.group(0)
        # Résout par rapport au fichier CSS
        resolved = (css_file_path.parent / url).resolve()
        if resolved.exists():
            data_uri = file_to_data_uri(resolved)
            if data_uri:
                return f'url("{data_uri}")'
        return m.group(0)

    return re.sub(r'url\(([^)]+)\)', replacer, css_text)


def resolve_css_path(href: str, page_path: pathlib.Path) -> pathlib.Path | None:
    """Résout le chemin d'un CSS relatif depuis la page HTML."""
    clean_href = re.sub(r'\?.*$', '', href)
    resolved = (page_path.parent / clean_href).resolve()
    return resolved if resolved.exists() else None


def inline_css_file(css_path: pathlib.Path) -> str:
    """Lit un fichier CSS et fixe ses url() relatifs."""
    text = css_path.read_text('utf-8', errors='replace')
    return fix_css_urls(text, css_path)


def resolve_css_imports(css_text: str, css_file_path: pathlib.Path) -> str:
    """Résout les @import url(...) / @import "..." dans un bloc CSS."""
    def replacer(m):
        raw = m.group(1).strip().strip("'\"")
        # Supprime query string
        raw = re.sub(r'\?.*$', '', raw)
        if raw.startswith(('http', '//', 'data:')):
            return m.group(0)
        resolved = (css_file_path.parent / raw).resolve()
        if resolved.exists():
            imported = resolved.read_text('utf-8', errors='replace')
            imported = fix_css_urls(imported, resolved)
            imported = resolve_css_imports(imported, resolved)
            return imported + '\n'
        return m.group(0)

    # Gère : @import "foo.css"; et @import url("foo.css");
    pattern = r'@import\s+(?:url\()?["\']?([^"\')\s;]+)["\']?\)?;?'
    return re.sub(pattern, replacer, css_text)


def collect_css(soup: BeautifulSoup, page_path: pathlib.Path):
    """
    Retourne (inline_css: str, external_link_tags: list[str]).
    - inline_css : CSS local combiné, url() convertis en base64
    - external_link_tags : <link> CDN à conserver tels quels dans le <head>
    """
    css_parts = []
    external_links = []

    # 1. Blocs <style> existants dans la page
    for style in soup.find_all('style'):
        txt = style.get_text()
        if not txt.strip():
            continue
        txt = resolve_css_imports(txt, page_path)
        txt = fix_css_urls(txt, page_path)
        css_parts.append(txt)

    # 2. <link rel="stylesheet">
    for link in soup.find_all('link', rel='stylesheet'):
        href = link.get('href', '')
        if not href:
            continue

        if href.startswith('http') or href.startswith('//'):
            # CSS externe (CDN) : garder comme <link> pour les icônes, etc.
            external_links.append(f'<link rel="stylesheet" href="{href}" crossorigin="anonymous">')
            continue

        css_path = resolve_css_path(href, page_path)
        if css_path and css_path.exists():
            css_text = inline_css_file(css_path)
            css_text = resolve_css_imports(css_text, css_path)
            css_parts.append(css_text)
        else:
            print(f'    CSS local manquant: {href}', file=sys.stderr)

    inline_block = '<style>\n' + '\n\n'.join(css_parts) + '\n</style>'
    return inline_block, external_links


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

    # ── CSS inline + liens CDN externes ──────────────────────────────────────
    all_css, external_link_tags = collect_css(soup, jb_html)

    # ── Extrait le contenu principal ─────────────────────────────────────────
    main = (soup.find('article', class_='bd-article')
            or soup.find('div', role='main')
            or soup.find('div', class_='bd-article')
            or soup.find('article')
            or soup.find('div', class_='bd-content'))

    if not main:
        print(f'  Contenu principal introuvable: {jb_html}', file=sys.stderr)
        errors.append(str(nb_path))
        continue

    # ── Supprime navigation et éléments inutiles ──────────────────────────────
    for sel in [
        '.prev-next', '.footer-item', 'a.headerlink',
        '.sd-badge', '.cell_tag', '.copybtn',
        '[aria-label="previous page"]', '[aria-label="next page"]',
        '.bd-sidebar', 'nav',
    ]:
        for el in main.select(sel):
            el.decompose()

    # ── Embarque les images du contenu en base64 ──────────────────────────────
    for img in main.find_all('img'):
        src = img.get('src', '')
        if src.startswith('data:') or src.startswith('http'):
            continue
        img_path = (jb_html.parent / src).resolve()
        if img_path.exists():
            ext = img_path.suffix.lstrip('.').lower()
            mime = IMG_MIME.get(ext, f'image/{ext}')
            b64 = base64.b64encode(img_path.read_bytes()).decode()
            img['src'] = f'data:{mime};base64,{b64}'
        else:
            print(f'    Image manquante: {img_path}', file=sys.stderr)

    # ── Attributs data-* du tag <html> (nécessaires pour le thème) ───────────
    html_tag = soup.find('html')
    data_attrs = ''
    if html_tag:
        for k, v in html_tag.attrs.items():
            if k.startswith('data-'):
                data_attrs += f' {k}="{v}"'

    # ── Assemble le HTML final ────────────────────────────────────────────────
    title = nb_path.stem.replace('_', ' ')
    external_links_html = '\n'.join(external_link_tags)
    html_out = f"""<!DOCTYPE html>
<html lang="fr"{data_attrs}>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
{external_links_html}
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
