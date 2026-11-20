(function(){
const $=(s,r=document)=>r.querySelector(s), stage=$('#stage'), RM=matchMedia('(prefers-reduced-motion:reduce)').matches;
const COL=['#e2445c','#784bd1','#0086c0','#00c875','#fdab3d','#a25ddc','#00854d'];
const av=(a)=>'<div class="avs">'+a.map((x,i)=>`<div class="av" style="background:${COL[(x.charCodeAt(0)+i)%7]}">${x}</div>`).join('')+'</div>';
const top=`<div class="top"><div class="logo">${LOGO}</div><div class="search"><span class="ic" style="width:26px;height:26px"></span>Search for anything…</div><span class="ic"></span><span class="ic"></span><div class="avs"><div class="av" style="background:#5559df;width:64px;height:64px">G</div></div></div>`;
const fab='<div class="fab">Ask, create, analyze</div>';
const D=[ // [ime, ura, kat-razred, kat, nivo, status-razred, status, ljudje, kanban-bar]
['Sprejem z napitkom','19:00','gs','Gostinstvo','C','run','Teče','AM'],
['Večerja','19:45','gs','Gostinstvo','C','wait','Čaka','TK'],
['Monday leta','21:00','live','Live','A','prep','V pripravi','GL'],
['DJ & glasba','22:00','live','Live','B','wait','Čaka','MR'],
['Foto kotiček','22:30','film','Film','C','run','Teče','NP'],
['Odštevanje','23:59','k','Kampanja','B','run','Teče','AM'],
['Dress code: modra','–','ex','Extra','C','ok','POTRJENO','TK'],
['Odiseja BTC City','19:00','rad','Radio Odiseja','C','ok','POTRJENO','GL'],
['RSVP do 3. 12.','Ti','ot','Otroški','C','wait','Čaka nate','Ti']];
const STAT={wait:'Čaka',run:'Teče',prep:'V pripravi',ok:'POTRJENO'};
const head='<div class="row h"><div><span class="cb"></span></div><div>Projekt</div><div>Start</div><div>Kategorija</div><div>Nivo</div><div>Status</div><div>People</div></div>';
const row=(r,i)=>`<div class="row" data-i="${i}"><div><span class="cb"></span></div><div><span class="chev"></span>${r[0]}</div><div class="dt">${r[1]}</div><div><div class="c ${r[2]}">${r[3]}</div></div><div><div class="c n-${r[4].toLowerCase()}">${r[4]}</div></div><div><div class="c s-${r[5]}">${r[6]}</div></div><div>${av([r[7]])}</div></div>`;
const hd=(sub)=>`<div class="hd"><h1>MONDAY PARTY <i></i></h1><div class="tabs"><span class="on">Main table</span><span>Ponedeljek, 7. 12. 2026</span><span>19:00</span><span>Odiseja BTC City</span></div></div><div class="tool"><div class="btn">RSVP <b>▾</b></div><span>Search</span><span>Person</span><span>Filter</span><span>Sort</span><span>Hide</span></div>`;
const table=(rows,n)=>`<div class="grp"><div class="gt"><i></i>Ponedeljek, 7. 12. 2026</div>${head}${rows.slice(0,n).map(row).join('')}</div>`;
const days=()=>{const t=new Date(2026,11,7,19,0)-new Date();const m=Math.max(0,Math.floor(t/6e4));return [Math.floor(m/1440),Math.floor(m%1440/60),m%60]};
const V={
a1(){const [d,h,m]=days();
 return `<div class="scr">${top}${hd()}<div class="big"><div class="word">MON<em>DAY</em><br>PARTY</div>
 <div class="cd"><div style="background:#e2445c"><b>${d}</b><small>dni</small></div><div style="background:#fdab3d"><b>${h}</b><small>ur</small></div><div style="background:#00c875"><b>${m}</b><small>min</small></div><div style="background:#784bd1"><b>NY</b><small>2027</small></div></div>
 <div class="info">${[['Kdaj','7. 12. 2026, 19:00','POTRJENO','ok'],['Kje','Odiseja BTC City','POTRJENO','ok'],['Dress code','Monday modra','V pripravi','prep'],['RSVP','do 3. 12. 2026','Čaka','wait']].map(r=>`<div class="row"><div class="dt">${r[0]}</div><div>${r[1]}</div><div><div class="c s-${r[3]}">${r[2]}</div></div></div>`).join('')}</div></div>${fab}</div>`},
a2(){const [d]=days();
 return `<div class="scr">${top}<div class="cols"><div class="rail">${['Workspace','Sidekick','Agents','Vibe','Workflows','Notetaker','Favorites'].map((x,i)=>`<div class="${i?'':'on'}"><i></i>${x}</div>`).join('')}</div>
 <div class="panel"><div class="mk"><i>M</i>Marketing</div><h4>Content</h4><div class="it">Manage workspace</div><div class="it on">MONDAY PARTY</div><div class="it">Program</div><div class="it">Lokacija</div><div class="it">Dress code</div><div class="it">RSVP</div></div>
 <div class="side"><h1>MONDAY<br>PARTY</h1><div class="tabs" style="margin-top:0"><span class="on">Main table</span><span>Kanban</span></div>
 <div class="card" style="background:#e2445c"><b>7. 12.</b><span>ponedeljek, 2026</span></div><div class="card" style="background:#0086c0"><b>19:00</b><span>Odiseja BTC City</span></div><div class="card" style="background:#00c875"><b>${d} dni</b><span>do začetka</span></div><div class="card" style="background:#784bd1"><b>RSVP</b><span>do 3. 12.</span></div><div class="card" style="background:#fdab3d"><b>Modra</b><span>dress code</span></div></div></div>${fab}</div>`},
b1(){return `<div class="scr">${top}${hd()}${table(D,9)}${fab}</div>`},
b2(){const rows=D.map(r=>r.slice());
 const el=document.createElement('div');el.className='scr';el.innerHTML=top+hd()+`<div class="grp"><div class="gt"><i></i>Ponedeljek, 7. 12. 2026</div>${head}<div id="rws"></div></div>`+fab;
 const w=$('#rws',el);
 if(RM){w.innerHTML=D.map((r,i)=>r[7]=='Ti'?row(r,i):row(r.slice(0,5).concat('ok','POTRJENO',r[7]),i)).join('');return el}
 D.forEach((r,i)=>{T(()=>{const x=document.createElement('div');x.innerHTML=row(r,i);const n=x.firstChild;n.style.opacity=0;n.style.transition='opacity .6s';w.appendChild(n);requestAnimationFrame(()=>n.style.opacity=1);
  if(r[7]=='Ti')return;T(()=>{const c=n.querySelectorAll('.c')[2];c.className='c s-run';c.textContent='Teče'},700);
  T(()=>{const c=n.querySelectorAll('.c')[2];c.className='c s-ok';c.textContent='POTRJENO'},1500)},i*600)});
 return el},
b3(){const cols=[['Čaka','#fdab3d',D.filter(r=>r[5]=='wait')],['Teče','#00c875',D.filter(r=>r[5]=='run'||r[5]=='prep')],['POTRJENO','#00854d',D.filter(r=>r[5]=='ok')]];
 return `<div class="scr">${top}${hd()}<div class="kb">${cols.map(c=>`<div class="kcol"><h3 style="background:${c[1]}">${c[0]}<span>${c[2].length}</span></h3>${c[2].map(r=>`<div class="kcard" style="--bar:${c[1]}"><b>${r[0]}</b><span>${r[1]}</span><span class="tag" style="background:${{k:'#784bd1',live:'#e2445c',gs:'#0086c0',film:'#00c875',rad:'#00854d',ex:'#a25ddc',ot:'#ff9bf0'}[r[2]]}">${r[3]}</span></div>`).join('')}</div>`).join('')}</div>${fab}</div>`}
};
let timers=[];function T(f,ms){timers.push(setTimeout(f,ms))}
function show(v){timers.forEach(clearTimeout);timers=[];stage.innerHTML='';const s=V[v]();if(typeof s=='string')stage.innerHTML=s;else stage.appendChild(s);
 stage.querySelectorAll('.kcard').forEach((k,i)=>setTimeout(()=>k.classList.add('show'),RM?0:150+i*110));
 document.querySelectorAll('#nav button').forEach(b=>b.classList.toggle('on',b.dataset.v==v));pill();history.replaceState(0,'','#'+v)}
function pill(){const b=$('#nav button.on'),p=$('#nav .pill');if(b){p.style.left=b.offsetLeft+'px';p.style.width=b.offsetWidth+'px'}}
function fit(){const v=$('#view'),k=Math.min(v.clientWidth/1080,v.clientHeight/1920);stage.style.transform=`scale(${k})`;stage.style.margin=`${-(1920*(1-k))/2}px ${-(1080*(1-k))/2}px`;pill()}
document.querySelectorAll('#nav button').forEach(b=>b.onclick=()=>show(b.dataset.v));
addEventListener('resize',fit);
addEventListener('keydown',e=>{const k=Object.keys(V),i=k.indexOf(location.hash.slice(1));if(e.key=='ArrowRight')show(k[Math.min(i+1,k.length-1)]);if(e.key=='ArrowLeft')show(k[Math.max(i-1,0)])});
fit();show(V[location.hash.slice(1)]?location.hash.slice(1):'a1');
})();
