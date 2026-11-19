# -*- coding: utf-8 -*-
"""Pogoji uporabe blagovne znamke Odiseja (SL in EN) – besedilo naročnika, brez sprememb vsebine."""

TERMS = {
    'sl': {
        'title': 'UPORABA BLAGOVNE ZNAMKE ODISEJA',
        'sub': 'Logotip, grafični elementi in celostna grafična podoba (CGP)',
        'sections': [
            {'h': '1. Dovoljenje za uporabo',
             'p': ['Odiseja omogoča svojim partnerjem, sodelavcem in drugim pooblaščenim uporabnikom uporabo uradnega logotipa, grafičnih elementov in drugih gradiv celostne grafične podobe (CGP) za namene promocije, komunikacije in predstavitve skupnih aktivnosti, dogodkov, projektov ali sodelovanj, povezanih z blagovno znamko Odiseja.']},
            {'h': '2. Smernice uporabe',
             'p': ['Pri uporabi elementov blagovne znamke je treba dosledno upoštevati priložena navodila in smernice celostne grafične podobe.'],
             'ul': ['Logotip in grafični elementi se uporabljajo v skladu z uradnimi grafičnimi predlogami.',
                    'Spreminjanje, popačenje, prebarvanje ali drugačno samovoljno prilagajanje logotipa ni dovoljeno.',
                    'Zagotoviti je treba ustrezno velikost, berljivost, razmerja in zaščitni prostor logotipa.',
                    'Uporaba blagovnih elementov ne sme škodovati ugledu, prepoznavnosti ali identiteti blagovne znamke Odiseja.',
                    'Vsaka uporaba zunaj predvidenih smernic oziroma večje odstopanje od njih zahteva predhodno pisno odobritev.']},
            {'h': '3. Lastništvo in pravice',
             'p': ['Vsi logotipi, grafični elementi in drugi materiali celostne grafične podobe Odiseja so zaščiteni z ustreznimi pravicami intelektualne lastnine. Njihovo lastništvo ostaja pri zakonitih imetnikih.',
                   'Prenos ali uporaba gradiv ne pomeni prenosa lastništva ali drugih pravic intelektualne lastnine.']},
            {'h': '4. Potrjevanje uporabe',
             'p': ['Za vprašanja, povezana z uporabo blagovne znamke, odobritvijo grafičnih rešitev ali morebitnimi odstopanji od smernic celostne grafične podobe, se obrnite na:'],
             'contact': ['Denis Kjostarov', 'Vodja Marketinga', 'denis.kjostarov@odiseja.si']},
            {'h': '5. Veljavnost in odgovornost',
             'p': ['Odiseja si pridržuje pravico do spremembe smernic uporabe ter do zahtevka za popravek ali odstranitev gradiv, ki niso skladna z opredeljenimi pravili uporabe blagovne znamke.',
                   'Z uporabo in prenosom gradiv uporabnik potrjuje, da je seznanjen s pogoji in smernicami uporabe ter se zavezuje k njihovemu spoštovanju.']},
        ],
        'ui': {
            'terms_head': 'Pogoji uporabe', 'terms_open': 'Preberi pogoje uporabe',
            'terms_accept': 'Prebral/a sem pogoje in smernice uporabe ter se zavezujem k njihovemu spoštovanju.',
            'terms_ok': 'Sprejmem in prenesem', 'terms_cancel': 'Prekliči', 'terms_close': 'Zapri',
            'terms_note': 'Za prenos gradiv je potrebno sprejeti pogoje uporabe.',
            'perm_short': 'Pred prenosom je treba sprejeti pogoje uporabe blagovne znamke.',
            'terms_file': 'pogoji-uporabe.txt',
            'pdf_perm': 'Vsa gradiva, ki vključujejo logotip ali druge elemente blagovne znamke Odiseja, morajo biti pred objavo ali distribucijo predložena v predhodno potrditev Denisu Kjostarovu (Marketing Odiseje).',
        },
    },
    'en': {
        'title': 'USE OF THE ODISEJA BRAND',
        'sub': 'Logo, Graphic Elements & Corporate Visual Identity (CVI)',
        'sections': [
            {'h': '1. Permission to Use',
             'p': ['Odiseja grants its partners, collaborators and other authorised users permission to use its official logo, graphic elements and other corporate visual identity (CVI) assets for the purposes of promoting, communicating and presenting joint activities, events, projects or collaborations associated with the Odiseja brand.']},
            {'h': '2. Brand Usage Guidelines',
             'p': ['The use of Odiseja brand elements must strictly comply with the accompanying instructions and corporate visual identity guidelines.'],
             'ul': ['The logo and graphic elements must be used in accordance with the officially provided artwork.',
                    'Altering, distorting, recolouring or otherwise modifying the logo without prior authorisation is not permitted.',
                    'The appropriate size, legibility, proportions and clear space around the logo must be maintained.',
                    'Brand elements must not be used in any way that could damage the reputation, recognition or identity of the Odiseja brand.',
                    'Any use outside the prescribed guidelines or significant deviations from them require prior written approval.']},
            {'h': '3. Ownership & Intellectual Property',
             'p': ['All Odiseja logos, graphic elements and other corporate visual identity materials are protected by applicable intellectual property rights. Ownership remains with their respective legal rights holders.',
                   'Downloading or using these materials does not constitute a transfer of ownership or any other intellectual property rights.']},
            {'h': '4. Usage Approval',
             'p': ['For questions regarding the use of the Odiseja brand, approval of graphic materials or any deviations from the corporate visual identity guidelines, please contact:'],
             'contact': ['Denis Kjostarov', 'Head of Marketing', 'denis.kjostarov@odiseja.si']},
            {'h': '5. Validity & Responsibility',
             'p': ['Odiseja reserves the right to amend its brand usage guidelines and request corrections or removal of any materials that do not comply with the established brand usage requirements.',
                   'By downloading and using these materials, users acknowledge that they have read and understood the applicable terms and guidelines and agree to comply with them.']},
        ],
        'ui': {
            'terms_head': 'Terms of use', 'terms_open': 'Read the terms of use',
            'terms_accept': 'I have read the terms and guidelines and agree to comply with them.',
            'terms_ok': 'Accept and download', 'terms_cancel': 'Cancel', 'terms_close': 'Close',
            'terms_note': 'You must accept the terms of use to download the materials.',
            'perm_short': 'The brand terms of use must be accepted before downloading.',
            'terms_file': 'terms-of-use.txt',
            'pdf_perm': 'All materials featuring the Odiseja logo or other brand elements must be submitted to Denis Kjostarov (Marketing Odiseje) for prior approval before publication or distribution.',
        },
    },
}


def terms_html(lg, cls='tm'):
    t = TERMS[lg]
    out = f'<h3 class="{cls}-t">{t["title"]}</h3><p class="{cls}-s">{t["sub"]}</p>'
    for s in t['sections']:
        out += f'<h4>{s["h"]}</h4>' + ''.join(f'<p>{p}</p>' for p in s.get('p', []))
        if s.get('ul'):
            out += '<ul>' + ''.join(f'<li>{x}</li>' for x in s['ul']) + '</ul>'
        if s.get('contact'):
            n, r, e = s['contact']
            out += f'<p class="ct"><b>{n}</b><br>{r}<br><a href="mailto:{e}">{e}</a></p>'
    return out


def terms_txt(lg):
    t = TERMS[lg]
    o = t['title'] + '\n' + t['sub'] + '\n\n'
    for s in t['sections']:
        o += s['h'] + '\n' + '\n'.join(s.get('p', [])) + '\n'
        for x in s.get('ul', []):
            o += '- ' + x + '\n'
        if s.get('contact'):
            o += '\n' + '\n'.join(s['contact']) + '\n'
        o += '\n'
    return o
