import re, json, html, pathlib
R = pathlib.Path(__file__).parent
css = (R / 'base.css').read_text(encoding='utf8')
units = []
for f in sorted((R / 'src').glob('u*.txt')):
    s = f.read_text(encoding='utf8')
    uid = re.search(r'id:"(u\d+)"', s).group(1)
    sj = int(re.search(r'\bs:(\d)', s).group(1))
    t = re.search(r'\bt:"([^"]*)"', s).group(1)
    p = re.search(r'\bp:"([^"]*)"', s).group(1)
    frag = (R / 'u' / f'{uid}.html').read_text(encoding='utf8')
    h1 = re.search(r'<h1>(.*?)</h1>', frag, re.S)
    h1 = re.sub(r'<[^>]+>', '', h1.group(1)).strip() if h1 else ''
    eps = len(re.findall(r'<section class="ep" id="e\d+"', frag))
    units.append(dict(id=uid, s=sj, t=t, p=p, h=h1, n=eps, frag=frag))

tpls = '\n'.join(f'<template id="t-{u["id"]}">\n{u["frag"]}</template>' for u in units)
meta = json.dumps([{k: u[k] for k in ('id', 's', 't', 'p', 'h', 'n')} for u in units], ensure_ascii=False)

shell = (R / 'shell.html').read_text(encoding='utf8')
out = shell.replace('/*BASE_CSS*/', css).replace('/*UNITS*/', meta).replace('<!--TEMPLATES-->', tpls)
(R / 'index.html').write_text(out, encoding='utf8')
import hashlib
sw = (R / 'sw.js').read_text(encoding='utf8')
ver = 'adsp-story-' + hashlib.sha1(out.encode('utf8')).hexdigest()[:8]
sw = re.sub(r'const VERSION = "[^"]*";', f'const VERSION = "{ver}";', sw)
(R / 'sw.js').write_text(sw, encoding='utf8')
print(len(units), 'units', len(out) // 1024, 'KB', 'emdash', out.count('—'))
