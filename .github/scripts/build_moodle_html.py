"""
Génère des fichiers HTML autonomes pour Moodle à partir du HTML JupyterBook.

Stratégie :
- Garde la structure complète du <body> (pour que tous les sélecteurs CSS
  fonctionnent, ex : .bd-page-width .highlight, body.pst-... etc.)
- Supprime du DOM les éléments de navigation (header, sidebar, footer, scripts)
- Inline tous les CSS locaux avec leurs polices/images converties en base64
  (gère les URLs avec query strings : fa-solid.woff2?v=6.4 → fichier réel)
- Garde les CSS CDN externes comme <link> tags (icônes Font Awesome, etc.)
- Embarque les images du contenu en base64
- MathJax conditionnel (CDN)
"""
import pathlib, base64, sys, re
from bs4 import BeautifulSoup

build_dir = pathlib.Path('_build/html')
moodle_dir = pathlib.Path('dist/moodle')

# ── MathJax conditionnel ─────────────────────────────────────────────────────
MATHJAX = """<script>
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
/* Masque navigation et sidebar — le contenu article reste visible */
body { overflow-x: hidden !important; }
.bd-header, header.bd-header,
.bd-sidebar-primary, .bd-sidebar-secondary,
#pst-primary-sidebar-modal, #pst-secondary-sidebar-modal,
.prev-next, .bd-footer, footer,
nav.bd-links, #navbar-icon-links,
[aria-label="previous page"], [aria-label="next page"],
.topbar, #main-nav,
a.headerlink, .copybtn, .cell_tag,
.sd-badge { display: none !important; }

.bd-main { padding-left: 0 !important; margin-left: 0 !important; }
.bd-content { max-width: 100% !important; }
.bd-article-container { max-width: 900px !important; margin: 0 auto; }
article.bd-article { padding: 1rem 1.5rem 2rem !important; }
</style>"""

# ── Types MIME pour fichiers locaux ──────────────────────────────────────────
MIME = {
    'woff':  'font/woff',
    'woff2': 'font/woff2',
    'ttf':   'font/ttf',
    'otf':   'font/otf',
    'eot':   'application/vnd.ms-fontobject',
    'svg':   'image/svg+xml',
    'png':   'image/png',
    'jpg':   'image/jpeg',
    'jpeg':  'image/jpeg',
    'gif':   'image/gif',
    'ico':   'image/x-icon',
}

MAX_EMBED_BYTES = 2 * 1024 * 1024  # 2 Mo max par fichier embarqué


def to_data_uri(path: pathlib.Path) -> str | None:
    """Convertit un fichier local en data URI base64 si son type est connu."""
    ext = path.suffix.lstrip('.').lower()
    mime = MIME.get(ext)
    if not mime:
        return None
    size = path.stat().st_size
    if size > MAX_EMBED_BYTES:
        print(f'    Trop grand pour embarquer ({size//1024} Ko): {path}', file=sys.stderr)
        return None
    b64 = base64.b64encode(path.read_bytes()).decode()
    return f'data:{mime};base64,{b64}'


def fix_css_urls(css_text: str, css_file: pathlib.Path) -> str:
    """
    Remplace url(<chemin relatif>) → url("data:...")
    Gère les URLs avec query string et fragment (ex: fa.woff2?v=6.4#iefix).
    """
    def replacer(m):
        raw = m.group(1).strip().strip("'\"")
        # Ignore les URLs déjà absolues ou vides
        if not raw or raw.startswith(('data:', 'http', '//', '#')):
            return m.group(0)
        # Supprime query string et fragment pour trouver le vrai fichier
        clean = re.sub(r'[?#].*$', '', raw)
        resolved = (css_file.parent / clean).resolve()
        if resolved.exists():
            uri = to_data_uri(resolved)
            if uri:
                return f'url("{uri}")'
        return m.group(0)

    return re.sub(r'url\(\s*(["\']?[^"\'()]*["\']?)\s*\)', replacer, css_text)


def resolve_imports(css_text: str, css_file: pathlib.Path, depth: int = 0) -> str:
    """Remplace les @import par le contenu réel du fichier importé (récursif)."""
    if depth > 5:
        return css_text

    def replacer(m):
        raw = m.group(1).strip().strip("'\"")
        clean = re.sub(r'[?#].*$', '', raw)
        if clean.startswith(('http', '//')):
            return m.group(0)
        resolved = (css_file.parent / clean).resolve()
        if resolved.exists():
            txt = resolved.read_text('utf-8', errors='replace')
            txt = resolve_imports(txt, resolved, depth + 1)
            txt = fix_css_urls(txt, resolved)
            return txt + '\n'
        return ''

    return re.sub(
        r'@import\s+(?:url\()?["\']?([^"\'();\s]+)["\']?\)?;?',
        replacer, css_text
    )


def resolve_css_path(href: str, page_path: pathlib.Path) -> pathlib.Path | None:
    """Résout un href relatif (sans query string) depuis la page HTML."""
    clean = re.sub(r'[?#].*$', '', href)
    resolved = (page_path.parent / clean).resolve()
    return resolved if resolved.exists() else None


def collect_css(soup: BeautifulSoup, page_path: pathlib.Path):
    """
    Retourne (css_inline: str, external_links: list[str]).
    Les CSS locaux sont lus, leurs imports et url() résolus, polices embarquées.
    Les CSS CDN restent comme <link> tags (pour les icônes Font Awesome, etc.).
    """
    parts = []
    external = []

    # Blocs <style> existants dans la page
    for style in soup.find_all('style'):
        txt = style.get_text()
        if txt.strip():
            txt = resolve_imports(txt, page_path)
            txt = fix_css_urls(txt, page_path)
            parts.append(txt)

    # <link rel="stylesheet">
    for link in soup.find_all('link', rel='stylesheet'):
        href = link.get('href', '')
        if not href:
            continue
        if href.startswith(('http', '//')):
            # CDN externe : garder comme <link> (icônes, polices CDN, etc.)
            external.append(
                f'<link rel="stylesheet" href="{href}" crossorigin="anonymous">'
            )
            continue
        css_path = resolve_css_path(href, page_path)
        if css_path:
            txt = css_path.read_text('utf-8', errors='replace')
            txt = resolve_imports(txt, css_path)
            txt = fix_css_urls(txt, css_path)
            parts.append(txt)
            print(f'    CSS inline: {css_path.name} ({css_path.stat().st_size//1024} Ko)')
        else:
            print(f'    CSS manquant: {href}', file=sys.stderr)

    return '<style>\n' + '\n\n'.join(parts) + '\n</style>', external


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
    print(f'  Traitement: {nb_path}')

    # ── CSS ──────────────────────────────────────────────────────────────────
    all_css, ext_links = collect_css(soup, jb_html)

    # ── Structure body : on garde tout mais on retire les scripts et
    #    les éléments de navigation lourds (sidebar, header, footer)
    #    Le CSS MOODLE_OVERRIDE masquera le reste.
    body = soup.find('body')
    if not body:
        print(f'  <body> introuvable: {jb_html}', file=sys.stderr)
        errors.append(str(nb_path))
        continue

    # Supprimer : scripts (dépendances ext.), éléments nav explicites
    for sel in [
        'script',
        'header.bd-header',
        '.bd-sidebar-primary',
        '.bd-sidebar-secondary',
        'footer.bd-footer',
        'footer',
        '.prev-next',
        'a.headerlink',
        '.copybtn',
        '.cell_tag',
    ]:
        for el in body.select(sel):
            el.decompose()

    # ── Images dans le contenu : embarquer en base64 ─────────────────────────
    article = (body.find('article', class_='bd-article')
               or body.find('div', role='main')
               or body)
    for img in article.find_all('img'):
        src = img.get('src', '')
        if src.startswith(('data:', 'http')):
            continue
        img_path = (jb_html.parent / src).resolve()
        if img_path.exists():
            ext = img_path.suffix.lstrip('.').lower()
            mime = MIME.get(ext, f'image/{ext}')
            b64 = base64.b64encode(img_path.read_bytes()).decode()
            img['src'] = f'data:{mime};base64,{b64}'
        else:
            print(f'    Image manquante: {img_path}', file=sys.stderr)

    # ── Attributs data-* du <html> (nécessaires pour le thème) ───────────────
    # data-theme est normalement injecté par JS au runtime ; on le fixe à "light"
    # pour que les sélecteurs Pygments html[data-theme="light"] .highlight soient actifs.
    html_tag = soup.find('html')
    data_attrs_dict = {'data-theme': 'light'}  # valeur par défaut forcée
    if html_tag:
        for k, v in html_tag.attrs.items():
            if k.startswith('data-'):
                data_attrs_dict[k] = v  # les attrs statiques écrasent si présents
    data_attrs = ''.join(f' {k}="{v}"' for k, v in data_attrs_dict.items())

    # ── Attributs / classes du <body> (sélecteurs CSS dépendent du body) ─────
    body_attrs = ''
    for k, v in body.attrs.items():
        if isinstance(v, list):
            body_attrs += f' {k}="{" ".join(v)}"'
        else:
            body_attrs += f' {k}="{v}"'

    # ── HTML final ────────────────────────────────────────────────────────────
    title = nb_path.stem.replace('_', ' ')
    html_out = f"""<!DOCTYPE html>
<html lang="fr"{data_attrs}>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
{chr(10).join(ext_links)}
{all_css}
{MOODLE_OVERRIDE}
{MATHJAX}
</head>
<body{body_attrs}>
{body.decode_contents()}
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
