# Pravila za predstavitve logotipov in CGP-jev

## Kdaj velja
Vsaka predstavitev osnutkov logotipa ali CGP-ja (celostne grafične podobe), tudi za druge stranke, se dela **v obliki in s designom landing predstavitve PUNKT** (`index.html`, referenčna implementacija v tem repozitoriju). Ne delaj PPTX ali zaslonskih slides, razen če uporabnik to izrecno zahteva.

## Oblika
- Ena samostojna `index.html`: vse vdelano (SVG, slike, JS, CSS), deluje brez omrežja.
- Slovenščina, besedila minimalno, jasen ton brez dvoumnih ali nepomembnih pripomb.
- Osnutkov **ne poimenuješ** (samo »Osnutek 1/2/3«).
- **Wow na koncu**: hero je nevtralen (velika beseda imena, brez logotipov). Noben logotip in nikoli vsi trije skupaj se ne pokažejo na začetku; skupaj šele v primerjavah.

## Struktura
Hero → Osnutek 1…N → Primerjava mockupov → Primerjava logotipov.
- **Lebdeča navigacija**: steklena pilula spodaj na sredini, scroll-spy, gladek skok; na telefonu skrajšane oznake (1, 2, 3, Mockupi, Logotipi).
- **Vsak osnutek**: (1) animacija razvoja skozi **vse artboarde**: scroll-scrub v sticky odru, filmski trak klikljivih minijatur, gumb Predvajaj/Pavza; če sta artboarda največ dva, naredi 2D animacijo logotipa; (2) končni osnutek na ploščici s preklopom Svetlo/Temno; (3) mockup čez cel zaslon s približkom na napis.
- **Primerjava mockupov**: harmonika (hover/klik razširi enega).
- **Primerjava logotipov**: enaki pogoji za vse: drsnik velikosti, Svetlo/Temno, Barvno/Enobarvno, megla.
- **CGP**: ista oblika; razdelki so poglavja (logotip, barve, tipografija, uporabe …) namesto osnutkov. Vsako poglavje ima animacijo ali sestavljanje, končni prikaz in uporabo/mockup. Isti hero, navigacija in primerjave, kjer so smiselne.

## Design
- Oder 16:9, kartica z zaobljenostjo 26 px in mehko senco; vsak razdelek ima svojo paleto, izpeljano iz osnutka.
- Sistemska sans pisava (Helvetica Neue / Inter), hero z veliko besedo imena.
- Gladke animacije `cubic-bezier(.2,.8,.2,1)`; upoštevaj `prefers-reduced-motion`.

## Tehnika (ne piši od nič, kopiraj in prilagodi)
- `tools/extract.js`: Playwright izlušči artboarde iz glavne SVG datoteke v `assets/boards.json` in makete v JPEG. `tools/extract_compare.js`: končni logotipi iz primerjalne SVG datoteke.
- `tools/parts.py` + `build.py`: razdelita artboarde na dele z id-ji `a<osnutek>_<artboard>_<pot>` in sestavita `index.html`.
- `src/stage.js`: motor delov (FLIP): ista oblika se premakne/poveča/zrcali, druga se prelije, nova se pojavi, manjkajoča ugasne; kamera obkroži vsako ploščo; krožni razkritek vzorca.
- `src/scen.js`: scenariji delov po osnutkih. `src/page.js`, `src/landing.html`, `src/landing.css`: stran.
- Gradnja: `python3 build.py`. Izlušči: `NODE_PATH=$(npm root -g) node tools/extract.js <IDEJA.svg>`.

## Pasti iz izkušnje
- `clipPath` in `filter` defs ne smejo biti v `visibility:hidden` svg (izrez izprazni vse).
- `use` ne upošteva transformacij prednikov: transformacijo vpiši na sam list.
- Živo besedilo brez vdelane pisave zamenjaj z orisanimi črkami.
- Artboardi imajo lahko nepravilen razmak: vzemi dejanske `<rect>`, ne mreže 550 px.
- Rdeče oznake in komentarji v artboardih: vprašaj uporabnika, kaj z njimi.
- Blagovne znamke strank nimajo zveze z drugimi projekti; ne omenjaj drugih blagovnih znamk.

## Dostava in preverjanje
- Playwright posnetki 1440×900 in 390×844 vsakega razdelka; scroll-scrub na več položajih; vsak artboard primerjaj s PDF-jem.
- Test navigacije in vseh kontrol; brez napak v konzoli; brez vodoravnega drsenja.
- Commit + push na določeno vejo; datoteko pošlji z `SendUserFile` (`render`; `attach`, če uporabnik reče »daj html«).

## Izbrani logotip (ena sama izbira, brez primerjave osnutkov)
Ko stranka izbere en logotip, ista oblika v skrajšani različici (primer: `pravi-punkt.html`, `build_pravi.py`): nevtralen hero → **Ideja** (scroll-scrub animacija ikone, ki razloži pomen znaka) → **Logotip** (oblike) → **Ikona** (z drsnikom velikosti) → **Različice** (preklop ozadij). Brez mockupov, če jih stranka izrecno ne želi. Vir: PDF z vektorji → `tools/extract_pdf.py` (pdftocairo) → `assets/pravi.json`; animacije z `src/timeline.js` + `src/pravi_scen.js`.
