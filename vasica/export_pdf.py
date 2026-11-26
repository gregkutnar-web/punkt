# Izvoz v večstranski PDF (vsak artboard = ena stran), živo besedilo z vdelano pisavo Inter (CFF, združljivo z Illustratorjem)
import re,cairosvg,io
from pypdf import PdfReader,PdfWriter
src=open('/home/user/punkt/vasica/vasica-artboards.svg',encoding='utf-8').read()
def fam(m):
    t=m.group(0)
    w=re.search(r'font-weight="(\d+)"',t); w=w.group(1) if w else '400'
    t=re.sub(r' font-weight="\d+"','',t)
    name,wt={'800':('Inter ExtraBold',None),'700':('Inter','bold')}.get(w,('Inter Regular',None))
    t=re.sub(r'font-family="[^"]*"',f'font-family="{name}"'+(f' font-weight="{wt}"' if wt else ''),t); return t
src=re.sub(r'<text [^>]*>',fam,src)
wr=PdfWriter()
for n,w,h,x in [('Feed',1080,1350,0),('Story',1080,1920,1200)]:
    s=src.replace('width="2280" height="1970" viewBox="0 0 2280 1970"',f'width="{w}" height="{h}" viewBox="{x} 50 {w} {h}"')
    wr.add_page(PdfReader(io.BytesIO(cairosvg.svg2pdf(bytestring=s.encode('utf-8')))).pages[0])
wr.add_metadata({'/Title':'Praznična vasica – Odiseja BTC City'})
wr.write('/home/user/punkt/vasica/vasica-artboards.pdf')
