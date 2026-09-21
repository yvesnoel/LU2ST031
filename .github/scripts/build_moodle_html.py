"""
Génère des fichiers HTML autonomes pour Moodle à partir du HTML JupyterBook.
- Admonitions MyST déjà rendues par Sphinx
- Images embarquées en base64
- CSS minimal autonome (Pygments + admonitions + typographie)
- MathJax conditionnel (CDN, ne se charge pas si Moodle l'a déjà)
"""
import pathlib, base64, sys
from bs4 import BeautifulSoup

build_dir = pathlib.Path('_build/html')
moodle_dir = pathlib.Path('dist/moodle')

# CSS Pygments (coloration syntaxique) généré par JupyterBook
pygments_css = ''
for css_path in sorted((build_dir / '_static').glob('pygments*.css')):
    pygments_css = css_path.read_text('utf-8')
    break

STYLE = f"""<style>
{pygments_css}
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
     font-size:16px;line-height:1.6;color:#333;max-width:900px;margin:0 auto;padding:1.5em}}
h1,h2,h3,h4{{color:#2c3e50;margin-top:1.4em}}
p{{margin:.6em 0}}
pre{{background:#f8f8f8;padding:1em;border-radius:4px;overflow-x:auto;font-size:.9em}}
code{{background:#f0f0f0;padding:.15em .4em;border-radius:3px;font-size:.9em}}
pre code{{background:none;padding:0}}
img{{max-width:100%;height:auto}}
table{{border-collapse:collapse;width:100%;margin:1em 0}}
th,td{{border:1px solid #ddd;padding:8px;text-align:left}}
th{{background:#f2f2f2;font-weight:bold}}
blockquote{{border-left:4px solid #ccc;margin:1em 0;padding:.5em 1em;color:#555}}
/* Admonitions MyST / Sphinx */
.admonition{{padding:.8em 1em;border-left:4px solid;border-radius:0 4px 4px 0;margin:1.2em 0}}
.admonition-title{{font-weight:bold;margin:0 0 .4em;text-transform:capitalize}}
.admonition.note,.admonition.seealso{{background:#e8f4fd;border-color:#3498db}}
.admonition.note .admonition-title,.admonition.seealso .admonition-title{{color:#1a5276}}
.admonition.tip,.admonition.hint{{background:#e9f7ef;border-color:#27ae60}}
.admonition.tip .admonition-title,.admonition.hint .admonition-title{{color:#1e8449}}
.admonition.warning,.admonition.attention,.admonition.caution{{background:#fef9e7;border-color:#f39c12}}
.admonition.warning .admonition-title{{color:#9a6e00}}
.admonition.danger,.admonition.error{{background:#fdecea;border-color:#e74c3c}}
.admonition.danger .admonition-title,.admonition.error .admonition-title{{color:#922b21}}
.admonition.important{{background:#f4ecff;border-color:#8e44ad}}
.admonition.important .admonition-title{{color:#6c3483}}
.prompt{{display:none}}
</style>"""

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

    # Contenu principal (JupyterBook / Sphinx Book Theme)
    main = (soup.find('div', role='main')
            or soup.find('article')
            or soup.find('div', class_='bd-article')
            or soup.find('section'))

    if not main:
        print(f'  Contenu principal introuvable: {jb_html}', file=sys.stderr)
        errors.append(str(nb_path))
        continue

    # Supprimer liens de navigation prev/next, ancres "#", badges
    for sel in ['.prev-next', '.footer-item', 'a.headerlink',
                '.sd-badge', '.cell_tag']:
        for el in main.select(sel):
            el.decompose()

    # Embarquer les images locales en base64
    for img in main.find_all('img'):
        src = img.get('src', '')
        if src.startswith('data:') or src.startswith('http'):
            continue
        img_path = (jb_html.parent / src).resolve()
        if img_path.exists():
            ext = img_path.suffix.lstrip('.').lower()
            if ext == 'jpg':
                ext = 'jpeg'
            b64 = base64.b64encode(img_path.read_bytes()).decode()
            img['src'] = f'data:image/{ext};base64,{b64}'
        else:
            print(f'    Image manquante: {img_path}', file=sys.stderr)

    title = nb_path.stem.replace('_', ' ')
    html_out = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
{STYLE}
{MATHJAX}
</head>
<body>
{main.decode_contents()}
</body>
</html>"""

    out_file = out_dir / (nb_path.stem + '.html')
    out_file.write_text(html_out, encoding='utf-8')
    print(f'  OK: {out_file}')
    ok += 1

print(f'Terminé : {ok} OK, {len(errors)} erreurs')
if errors:
    print('Erreurs :', errors, file=sys.stderr)
