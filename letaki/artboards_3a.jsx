// Illustrator: za vsako stran letaka (skupina »stran_…« z ozadjem »ozadje«) ustvari artboard.
// Uporaba: odprite zimski_letaki_3a.svg, nato File > Scripts > Other Script… in izberite to datoteko.
#target illustrator
(function () {
    if (app.documents.length === 0) { alert("Najprej odprite zimski_letaki_3a.svg."); return; }
    var doc = app.activeDocument;
    var pages = [];
    for (var i = 0; i < doc.groupItems.length; i++) {
        var g = doc.groupItems[i];
        if (g.name.indexOf("stran_") === 0) pages.push(g);
    }
    if (pages.length === 0) { alert("Skupin »stran_…« ni najdenih."); return; }
    var added = 0, missing = [];
    for (var p = 0; p < pages.length; p++) {
        var bg = null;
        for (var k = 0; k < pages[p].pageItems.length; k++) {
            if (pages[p].pageItems[k].name === "ozadje") { bg = pages[p].pageItems[k]; break; }
        }
        if (!bg) { missing.push(pages[p].name); continue; }
        var ab = doc.artboards.add(bg.geometricBounds);
        ab.name = pages[p].name.replace("stran_", "").replace(/_/g, " ").toUpperCase();
        added++;
    }
    if (added > 0 && doc.artboards.length > added) doc.artboards.remove(0);
    alert("Artboardov: " + added + (missing.length ? "\nBrez ozadja: " + missing.join(", ") : ""));
})();
