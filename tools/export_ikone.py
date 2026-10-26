import re, importlib.util, sys
src = open('build_ikone.py').read().split("page = f'''")[0]
ns = {}; exec(src, ns)
defs = re.search(r'<defs>.*</defs>', ns['defs'], re.S).group(0)
for n in (1, 2):
    ic = ns['icon'](n).replace('<svg ', '<svg xmlns="http://www.w3.org/2000/svg" ', 1)
    ic = ic.replace('>', '>' + defs, 1)
    open(f'export/ikona-predlog-{n}.svg', 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n' + ic)
