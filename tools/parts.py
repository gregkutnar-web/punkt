"""Skupna pomoč za build.py in razhroščevanje: razdeli artboarde na dele z id-ji.
id dela: a<osnutek>_<artboard>_<pot>, pot = indeksi (0-based) po vseh nivojih, ločeni z _ ."""
import json, re, pathlib, xml.etree.ElementTree as ET

ET.register_namespace('', 'http://www.w3.org/2000/svg')
R = pathlib.Path(__file__).parent.parent
A = R / 'assets'
BOARDS = json.loads((A / 'boards.json').read_text())
STYLE = (A / 'style.css').read_text()


def class_fills():
    """razred -> (fill ali None, ima_stroke)"""
    out = {}
    for sel, body in re.findall(r'([^{}]+)\{([^}]*)\}', STYLE):
        fill = re.search(r'fill:\s*([^;]+)', body)
        stroke = 'stroke' in body or 'filter' in body or 'clip-path' in body
        for c in re.findall(r'\.(k\d+)', sel):
            f, s = out.get(c, (None, False))
            out[c] = (fill.group(1).strip() if fill else f, s or stroke)
    return out


CF = class_fills()


def anim_board(idea, b):
    """Markup artboarda z id-ji delov; listi imajo fill=currentColor + data-c (razen obrisov/oznak)."""
    board = BOARDS['boards'][str(idea)][b]
    wrapped = '<svg xmlns="http://www.w3.org/2000/svg">' + ''.join(board['items']) + '</svg>'
    root = ET.fromstring(wrapped)

    def walk(e, ident):
        tag = e.tag.split('}')[1]
        attrs = dict(e.attrib)
        cls = attrs.get('class')
        if tag == 'g':
            attrs['id'] = ident
            kids = ''.join(walk(c, f'{ident}_{i}') for i, c in enumerate(e))
            a = ' '.join(f'{n}="{v}"' for n, v in attrs.items())
            return f'<g {a}>{kids}</g>'
        if tag == 'text' and idea == 2 and b == 9:
            # živo besedilo (pisava ni vdelana) zamenjam z orisanimi črkami BOSCAROL iz artboarda 6
            src = ET.fromstring('<svg xmlns="http://www.w3.org/2000/svg">' + BOARDS['boards']['2'][5]['items'][2] + '</svg>')[0]
            rep = walk(src, ident).replace('data-c="#25525f"', 'data-c="#e4edef"')
            sc = 147.0 / 181.0
            tx, ty = 5250.5 - sc * 2996.5, 1256.0 - sc * 1248.0
            # transformacijo vpišem v vsako črko (use ne upošteva transformacij prednikov)
            return rep.replace('<path ', f'<path transform="translate({tx:.2f} {ty:.2f}) scale({sc:.4f})" ')
        if tag == 'text':
            attrs['id'] = ident
            a = ' '.join(f'{n}="{v}"' for n, v in attrs.items())
            return f'<text {a}>{"".join(ET.tostring(c, encoding="unicode") for c in e).replace(" xmlns=" + chr(34) + "http://www.w3.org/2000/svg" + chr(34), "")}</text>'
        fill, special = CF.get(cls, (None, False)) if cls else (None, False)
        attrs['id'] = ident
        if cls and fill and fill != 'none' and not special:
            attrs.pop('class')
            attrs['fill'] = 'currentColor'
            attrs['data-c'] = fill
        a = ' '.join(f'{n}="{v}"' for n, v in attrs.items())
        return f'<{tag} {a}/>'

    return ''.join(walk(c, f'a{idea}_{b}_{i}') for i, c in enumerate(root))
