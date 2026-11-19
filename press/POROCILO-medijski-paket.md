# Odiseja – medijski paket: poročilo o vsebini

**Namen:** logotipi, barve, pravila uporabe in prepovedane uporabe blagovne znamke Odiseja za medije in partnerje, v slovenščini in angleščini.
**Obseg:** samo prizorišče Odiseja (brez družbe Odisejada d.o.o.), brez podnapisov (brez »Boscarol Group« in »BTC City«).
**Vir:** priročnika CGP (decembra 2024 in oglaševanje), dokument `Varne_cone_odiseja_logo.ai` in ozadje `CGP-background.svg`.

## 1. Kaj je v paketu

Datoteka `odiseja-press-package.zip` vsebuje štiri datoteke, ki morajo ostati v isti mapi:

| Datoteka | Opis |
|---|---|
| `press-sl.html` | Slovenska predstavitvena stran (ena samostojna datoteka, deluje brez omrežja) |
| `press-en.html` | Angleška predstavitvena stran (enaka vsebina) |
| `odiseja-medijski-paket.zip` | Slovenski paket za prenos (40 datotek) |
| `odiseja-press-kit.zip` | Angleški paket za prenos (40 datotek) |

Gumb za prenos na strani odpre ZIP iz iste mape.

## 2. Predstavitvena stran (HTML)

1. **Uvod:** veliki beli logotip na gradientu CGP.
2. **Logotip:** vodoravni, navpični in samostojni znak; ozadje bela, črna ali turkizna; barva logotipa turkizna, črna ali bela (nedovoljene kombinacije so onemogočene). Prenos SVG in PNG. Ob izbiri samostojnega znaka se pokaže opozorilo (»Use the symbol alone only as a decorative element.« / »Znak samostojno uporabljamo le kot okrasni element.«).
3. **Pravila:**
   - *Varni prostor:* višina črke O na vseh straneh; vodoravni in navpični logotip, narisana po dokumentu `Varne_cone_odiseja_logo.ai`.
   - *Najmanjša velikost:* interaktivno ravnilo v pravih mm; vodoravni logotip 40 mm, navpični 23 mm; drsnik z označenim minimumom in stanjem »Dovolj velik« / »Premajhen«.
4. **Barve:** turkizna `#00B1BC` (RGB 0 177 188, CMYK 75 / 5 / 28 / 0), črna `#000000`, bela `#FFFFFF`; kopiranje vrednosti; matrika dovoljenih barv logotipa na ozadju.
5. **Prepovedano:** osem prepovedanih uporab, prikazanih z resničnim logotipom (napis brez znaka, spreminjanje razmerij, nagib, zrcaljenje, druge barve, okvir ali podlaga, vzorci iz logotipa, znak na glavo).
6. **Prenos:** gumb za ZIP in povezava na pogoje uporabe.

**Pogoji uporabe:** ob prenosu SVG, PNG ali ZIP se prikaže okno s celotnim besedilom pogojev (SL ali EN). Prenos se začne šele, ko uporabnik označi potrditev in klikne »Sprejmem in prenesem«. Po sprejemu v isti seji nadaljnji prenosi niso ovirani.

Stran je odzivna (namizje in telefon), brez vodoravnega drsenja, z upoštevanjem `prefers-reduced-motion`.

## 3. Paket za prenos (ZIP, 40 datotek)

| Vsebina | Podrobnosti |
|---|---|
| `logo/` (36 datotek) | 3 različice (vodoravno, navpično, znak) × 3 barve (turkizna, črna, bela) × 4 oblike: SVG (vektor), PDF (vektor), PNG 1200 px in PNG 3600 px (prosojno ozadje) |
| `pravila-uporabe.pdf` / `usage-rules.pdf` | 7 strani A4 ležeče (opis spodaj) |
| `barve.txt` / `colours.txt` | Vrednosti HEX, RGB in CMYK |
| `pogoji-uporabe.txt` / `terms-of-use.txt` | Celotno besedilo pogojev uporabe |
| `README.txt` | Kratek opis paketa |

### PDF s pravili uporabe (7 strani)
1. Naslovnica z gradientom CGP in belim logotipom
2. Logotip: vseh 9 različic in opozorilo za samostojni znak
3. Pravila: varni prostor in najmanjša velikost (logotipa v pravih 40 mm in 23 mm)
4. Barve in matrika barv logotipa na ozadju
5. Prepovedane uporabe
6. Pogoji uporabe (celotno besedilo)
7. Zadnja stran z gradientom: gradiva z logotipom ali elementi blagovne znamke je treba pred objavo ali distribucijo predložiti v predhodno potrditev; kontakt Denis Kjostarov, Vodja Marketinga (denis.kjostarov@odiseja.si)

## 4. Pravila uporabe v povzetku

- **Varni prostor:** višina črke O okoli napisa (levo, zgoraj, spodaj) in znaka (desno); pri navpičnem logotipu okoli celotnega logotipa.
- **Najmanjša velikost:** vodoravni 40 mm, navpični 23 mm (veljajo za A4 in manjše).
- **Barve:** samo turkizna, črna ali bela; turkizna ali črna na svetlem ozadju, turkizna ali bela na temnem; na turkiznem ozadju samo bela.
- **Znak** samostojno samo kot okrasni element.
- **Prepovedano:** vse, kar spreminja logotip (glej točko 2.5).

## 5. Odprta vprašanja in opombe

- **Najmanjša velikost znaka:** priročniki je ne določajo, zato je paket ne navaja.
- **Navpični logotip:** v priročnikih obstaja samo s podnapisom; brez podnapisa je izdelan po pravilih iz priročnika (znak nad napisom). Varni prostor za navpični logotip priročnik ne določa; uporabljeno je enako pravilo (višina črke O okoli celotnega logotipa).
- **Natančnost prikaza mm na zaslonu:** približna (1 mm ≈ 3,78 px).
- **Pogoji uporabe:** besedilo je v obeh jezikih vneseno po predlogi naročnika. Popup se po sprejemu v isti seji ne ponavlja.
- **Angleški PDF:** zadnja stran še omenja Denisa Kjostarova v stavku o potrditvi, slovenski ne; uskladitev je mogoča po želji.

## 6. Tehnični podatki

- Barve v vseh datotekah logotipov so samo `#00B1BC`, `#000000` in `#FFFFFF` (brez sivin).
- Napis je orisan (brez vdelanih pisav).
- Izvorna koda sestavljanja je v repozitoriju (`build_press.py`, `tools/extract_odiseja.py`, `tools/press_raster.js`, `src/press*`); veja `claude/upbeat-cray-cb5g5e`.
