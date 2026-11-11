# Sestavi kombi-odiseja-osnutki.html: predstavitev petih končnih mockupov kombija (slike vdelane).
import base64, io, sys
from PIL import Image
SRC = sys.argv[1] if len(sys.argv) > 1 else '/tmp/claude-0/-home-user-punkt/48b3d78d-1599-5d3a-acc8-93dab4d65a91/images'
def b64(n):
    im = Image.open(f'{SRC}/{n}.jpg').convert('RGB')
    if im.width > 1600: im = im.resize((1600, round(im.height*1600/im.width)), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, 'JPEG', quality=84, optimize=True)
    return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
HTML = r'''<!doctype html>
<html lang="sl"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Odiseja – poslikava kombija</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
:root{--sans:"Helvetica Neue","Inter","Segoe UI",system-ui,-apple-system,Arial,sans-serif;--ease:cubic-bezier(.2,.8,.2,1);--teal:#0097a7;--ink:#0b1416}
html{background:var(--ink)}
body{font-family:var(--sans);color:#eef6f7;background:var(--ink);-webkit-font-smoothing:antialiased;overflow-x:hidden}
button{font:inherit;color:inherit;background:none;border:0;cursor:pointer}
.hero{min-height:100vh;min-height:100svh;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:24px;background:radial-gradient(120% 80% at 50% 110%,#0a3a40 0,var(--ink) 60%)}
.hero h1{font-weight:800;letter-spacing:-.03em;line-height:.9;font-size:clamp(56px,15vw,230px);text-transform:uppercase}
.hero h1 span{display:block;font-size:.32em;letter-spacing:.38em;font-weight:600;color:#4fd0db;margin-bottom:.35em}
.hero p{margin-top:36px;font-size:clamp(14px,1.4vw,18px);color:#9db7ba;letter-spacing:.04em}
.hero i{position:absolute;bottom:90px;font-style:normal;color:#5b7d82;font-size:13px;letter-spacing:.2em;text-transform:uppercase;animation:b 2.4s var(--ease) infinite}
@keyframes b{50%{transform:translateY(8px)}}
section.s{min-height:100vh;min-height:100svh;padding:7vh 4vw 14vh;display:flex;flex-direction:column;justify-content:center;gap:22px}
.t{display:flex;align-items:baseline;gap:16px;max-width:1500px;width:100%;margin:0 auto}
.t b{font-size:clamp(26px,3.4vw,48px);letter-spacing:-.02em}.t em,.xx{font-style:normal;color:#7fa3a7;font-size:15px}
.stage{position:relative;width:min(100%,calc(76vh*var(--ar)));max-width:1500px;margin:0 auto;aspect-ratio:var(--ar);border-radius:26px;overflow:hidden;box-shadow:0 40px 90px -30px rgba(0,151,167,.45),0 10px 30px rgba(0,0,0,.5);background:#111;opacity:0;transform:translateY(40px) scale(.98);transition:opacity .9s var(--ease),transform .9s var(--ease)}
.stage.in{opacity:1;transform:none}
.stage img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;transition:transform 1.3s var(--ease),opacity .6s var(--ease);transform-origin:var(--ox) var(--oy)}
.stage img.on{opacity:1}
.stage.z img{transform:scale(var(--zs))}
.tabs{display:flex;gap:6px;flex-wrap:wrap}.tabs button{padding:8px 16px;border-radius:99px;font-size:14px;color:#9db7ba;border:1px solid rgba(255,255,255,.18);transition:all .3s var(--ease)}.tabs button.on{background:var(--teal);border-color:var(--teal);color:#fff}
.zoom{position:absolute;right:16px;bottom:16px;padding:11px 18px;border-radius:99px;font-size:14px;background:rgba(255,255,255,.18);backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);border:1px solid rgba(255,255,255,.3);color:#fff;transition:background .3s}
.zoom:hover{background:rgba(255,255,255,.3)}
.duo{display:grid;grid-template-columns:1fr 1fr;gap:20px;max-width:1500px;width:100%;margin:0 auto}
.duo .stage{aspect-ratio:16/10}
.duo figcaption{position:absolute;left:14px;top:14px;padding:7px 14px;border-radius:99px;font-size:13px;background:rgba(0,0,0,.5);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px)}
nav{position:fixed;left:50%;bottom:calc(18px + env(safe-area-inset-bottom));transform:translateX(-50%);display:flex;gap:4px;padding:6px;border-radius:99px;background:rgba(20,32,34,.55);backdrop-filter:blur(22px) saturate(1.4);-webkit-backdrop-filter:blur(22px) saturate(1.4);border:1px solid rgba(255,255,255,.18);box-shadow:0 12px 40px rgba(0,0,0,.4);z-index:9}
nav a{padding:10px 18px;border-radius:99px;font-size:14px;color:#c4d8da;text-decoration:none;transition:background .4s var(--ease),color .3s}
nav a.on{background:var(--teal);color:#fff}
nav .m{display:none}
@media(max-width:700px){section.s{padding:5vh 14px 14vh}.stage{border-radius:18px}.duo{grid-template-columns:1fr}nav .d{display:none}nav .m{display:inline}nav a{padding:10px 14px}.t{flex-direction:column;gap:4px}.zoom{padding:9px 14px;font-size:13px}}
@media(prefers-reduced-motion:reduce){*{transition-duration:.01ms!important;animation:none!important}.stage{opacity:1;transform:none}}
</style></head><body>
<header class="hero" id="hero"><h1>Odiseja</h1><p>Poslikava kombija</p><i>Drsi navzdol</i></header>

<section class="s" id="bok"><div class="t"><b>Bok vozila</b><div class="tabs"><button class="on">Osnutek 1</button><button class="">Osnutek 2</button><button class="">Osnutek 3</button><button class="">Osnutek 4</button></div></div>
<div class="stage" style="--ar:2"><img class="on" src="@12" alt="Osnutek 1" style="--ox:96%;--oy:36%;--zs:2"><img class="" src="@14" alt="Osnutek 2" style="--ox:96%;--oy:36%;--zs:2"><img class="" src="@13" alt="Osnutek 3" style="--ox:60%;--oy:33%;--zs:2"><img class="" src="@15" alt="Osnutek 4" style="--ox:85%;--oy:40%;--zs:1.5"><button class="zoom">Približaj napis</button></div></section>

<section class="s" id="zadaj"><div class="t"><b>Zadnja vrata</b><div class="tabs"><button class="on">Osnutek 1</button><button class="">Osnutek 2</button><button class="">Osnutek 3</button></div></div>
<div class="stage" style="--ar:1.77"><img class="on" src="@17" alt="Osnutek 1" style="--ox:47%;--oy:36%;--zs:2.8"><img class="" src="@19" alt="Osnutek 2" style="--ox:51%;--oy:31%;--zs:2.4"><img class="" src="@18" alt="Osnutek 3" style="--ox:70%;--oy:33%;--zs:3"><button class="zoom">Približaj napis</button></div></section>

<nav id="nav"><a href="#bok"><span class="d">Bok</span><span class="m">Bok</span></a><a href="#zadaj"><span class="d">Zadnja vrata</span><span class="m">Zadaj</span></a></nav>
<script>
const rm=matchMedia('(prefers-reduced-motion:reduce)').matches;
const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{threshold:.15});
document.querySelectorAll('.stage').forEach(s=>io.observe(s));
document.querySelectorAll('.tabs').forEach(t=>{const st=t.closest('section').querySelector('.stage'),im=[...st.querySelectorAll('img')],bs=[...t.children];bs.forEach((b,i)=>b.onclick=()=>{bs.forEach((x,j)=>x.classList.toggle('on',i===j));im.forEach((x,j)=>x.classList.toggle('on',i===j))})});
document.querySelectorAll('.zoom').forEach(b=>b.onclick=()=>{const s=b.closest('.stage');s.classList.toggle('z');b.textContent=s.classList.contains('z')?'Celotno vozilo':'Približaj napis'});
const links=[...document.querySelectorAll('nav a')],secs=links.map(a=>document.querySelector(a.hash));
links.forEach(a=>a.onclick=e=>{e.preventDefault();document.querySelector(a.hash).scrollIntoView({behavior:rm?'auto':'smooth'})});
function spy(){const y=innerHeight*.5;let c=-1;secs.forEach((s,i)=>{const r=s.getBoundingClientRect();if(r.top<y&&r.bottom>y)c=i});links.forEach((a,i)=>a.classList.toggle('on',i===c))}
addEventListener('scroll',spy,{passive:true});spy();
</script></body></html>'''
for n in (12, 13, 14, 15, 17, 18, 19):
    HTML = HTML.replace(f'"@{n}"', f'"{b64(n)}"')
open('kombi-odiseja-osnutki.html', 'w', encoding='utf-8').write(HTML)
