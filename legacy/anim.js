/* ===== A: animacija nastanka – motor delov (ideja 1, Sinergija) =====
   Vsaka sličica je razdeljena na dele (id e<sličica>_<pot>). Del, ki ima sličico tudi v naslednjem
   kadru, se premakne/poveča/zrcali; del z drugačno obliko se prelije; novi se pojavijo, manjkajoči ugasnejo. */
var anim=(function(){
  var ORDER=__ORDER__;                       // prikazni vrstni red -> sličica
  var N=ORDER.length, HOLD=.55, FD=2400;     // zadržek (delež) in ms na sličico
  var CS=[3.6,3.7,3.6,3.6,5.0,5.0,5.2,5.2,5.0,1.65,3.9,3.4,1.9,3.9];   // povečava kamere
  var CY=[0,0,0,0,0,0,0,0,0,0,0,0,79,0];                                 // navpični zamik kamere
  var SVGNS='http://www.w3.org/2000/svg';
  var cam=$('#cam'), layer=$('#actors'), patc=$('#patc'), anim_svg=$('#anim');
  var el={play:$('#play'),scrub:$('#scrub'),fc:$('#fc'),spd:$('#spd'),ths:$$('#film .th'),chap:$$('.chap span')};

  function cl(x){return x<0?0:x>1?1:x}
  function lerp(a,b,t){return a+(b-a)*t}
  function ease(t){return t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2}
  var TILEX=__TILEX__;
  function TX(k){return TILEX[k]+252.025}
  var TY=272.98;
  function sid(d,p){return 'e'+ORDER[d]+'_'+p.replace(/\./g,'_')}
  function hex(c){return [parseInt(c.substr(1,2),16),parseInt(c.substr(3,2),16),parseInt(c.substr(5,2),16)]}
  function mix(a,b,t){var x=hex(a),y=hex(b);return 'rgb('+Math.round(lerp(x[0],y[0],t))+','+Math.round(lerp(x[1],y[1],t))+','+Math.round(lerp(x[2],y[2],t))+')'}

  var actors=[];
  function mk(tag,attrs){var e=document.createElementNS(SVGNS,tag);for(var k in attrs)e.setAttribute(k,attrs[k]);return e}
  function actor(name,list){
    var a={name:name,kf:[]};
    list.forEach(function(it){
      var d=it[0], src=document.getElementById(sid(d,it[1]));
      if(!src){console.warn('manjka del',d,it[1]);return}
      var bb=src.getBBox(), tk=ORDER[d];
      a.kf[d]={id:src.id,o:it[2]||{},ncx:bb.x+bb.width/2,ncy:bb.y+bb.height/2,w:bb.width,h:bb.height,
               cx:bb.x+bb.width/2-TX(tk),cy:bb.y+bb.height/2-TY,color:src.getAttribute('data-c')};
      if(it[2]&&it[2].wipe&&!a.clip){
        var cp=mk('clipPath',{id:'wp_'+name,clipPathUnits:'objectBoundingBox'});
        a.rect=mk('rect',{x:0,y:0,width:0,height:1});cp.appendChild(a.rect);$('#anim defs').appendChild(cp);a.clip=cp.id;
      }
    });
    a.g=mk('g',{});a.under=mk('use',{});a.over=mk('use',{});a.g.appendChild(a.under);a.g.appendChild(a.over);
    layer.appendChild(a.g);actors.push(a);return a;
  }

  /* ---- scenarij: [prikazni kader, pot, možnosti] ----
     x: prelitje (druga oblika) · flip: zrcaljenje · from: od kod pride · d: zakasnitev · out: kam odide · wipe: se nariše */
  var FL={flip:1}, SP={from:[110,0],d:.1};
  actor('P',[[0,'1.0'],[1,'1.0'],[2,'1.0'],[3,'1',{out:[-170,0]}]]);
  actor('K',[[0,'1.3'],[1,'1.2'],[2,'1.1'],[3,'2',{out:[170,0]}]]);
  actor('T',[[0,'1.4'],[1,'1.3'],[2,'1.2'],[3,'3',{out:[190,0]}]]);
  actor('N',[[0,'1.2'],[1,'1.1.1',{x:1}],[2,'1.3.2'],[3,'4.2'],[4,'1.2'],[5,'1.2']]);
  // leva enota znaka: ukrivljen U (od besede do logotipa)
  actor('Lb',[[0,'1.1'],[1,'1.1.0',{x:1}],[2,'1.3.1'],[3,'4.1'],[4,'1.1'],[5,'1.1'],[6,'1.3.0'],[7,'1.3.0'],[8,'1.1.0'],
              [9,'3.0.1.0'],[10,'1.0.0.1.0'],[11,'1.1.0',FL],[12,'2.0'],[13,'1.0.0.1.0',FL]]);
  actor('Lc',[[1,'1.1.2',{d:.15}],[2,'1.3.3'],[3,'4.3'],[4,'1.3'],[5,'1.3'],[6,'1.3.1'],[7,'1.3.1'],[8,'1.1.2'],
              [9,'3.0.1.2'],[10,'1.0.0.1.2'],[11,'1.1.2',FL],[12,'2.2'],[13,'1.0.0.1.2',FL]]);
  actor('Lh',[[8,'1.1.1',{d:.3}],[9,'3.0.1.1'],[10,'1.0.0.1.1'],[11,'1.1.1',FL],[12,'2.1'],[13,'1.0.0.1.1',FL]]);
  // desna enota znaka
  actor('Rs',[[6,'1.0',SP],[7,'1.0'],[8,'1.0.1'],[9,'3.0.0.1'],[10,'1.0.0.0.1'],[11,'1.0.1',FL],[12,'1.1'],[13,'1.0.0.0.1',FL]]);
  actor('Rc',[[6,'1.2',{from:[110,0],d:.2}],[7,'1.2'],[8,'1.0.2'],[9,'3.0.0.2'],[10,'1.0.0.0.2'],[11,'1.0.2',FL],[12,'1.2'],[13,'1.0.0.0.2',FL]]);
  actor('Rh',[[8,'1.0.0',{d:.3}],[9,'3.0.0.0'],[10,'1.0.0.0.0'],[11,'1.0.0',FL],[12,'1.0'],[13,'1.0.0.0.0',FL]]);
  actor('M1',[[6,'1.1',{d:.15}],[7,'1.1']]);
  // zlata črta (nariše se)
  actor('gU',[[3,'5.0',{wipe:1}],[4,'2.0']]);
  actor('gN',[[3,'5.1',{wipe:1,d:.25}],[4,'2.1']]);
  actor('gA',[[6,'2',{wipe:1}]]);
  actor('gB',[[6,'3',{wipe:1,d:.3}]]);
  // sličica 10: tri različice
  var UP={from:[0,16]};
  [['1.0',0],['1.1.0',1],['1.1.1',2],['1.1.2',3],['1.2',4],['1.3',5]].forEach(function(r){actor('w1'+r[1],[[9,r[0],{from:[0,16],d:.05*r[1]}]])});
  ['2.0.0','2.0.1','2.0.2','2.0.3.0','2.0.3.1'].forEach(function(p,i){actor('m2'+i,[[9,p,{d:.04*i}]])});
  [['2.1.0',0],['2.1.1.0',1],['2.1.1.1',2],['2.1.1.2',3],['2.1.2',4],['2.1.3',5]].forEach(function(r){actor('w2'+r[1],[[9,r[0],{from:[0,16],d:.05*r[1]}]])});
  ['3.1.1.0','3.1.1.1','3.1.1.2'].forEach(function(p,i){actor('w3'+i,[[9,p,{from:[0,16],d:.1}]])});
  actor('Wp',[[9,'3.1.0',{from:[0,16]}],[10,'1.0.1.0'],[11,'2.0'],[13,'1.0.1.0',{from:[-110,0]}]]);
  actor('Wk',[[9,'3.1.2',{from:[0,16]}],[10,'1.0.1.3'],[11,'2.3'],[13,'1.0.1.3',{from:[-110,0],d:.2}]]);
  actor('Wt',[[9,'3.1.3',{from:[0,16]}],[10,'1.0.1.4'],[11,'2.4'],[13,'1.0.1.4',{from:[-110,0],d:.25}]]);
  actor('Wu',[[10,'1.0.1.1',{d:.1}],[11,'2.1'],[13,'1.0.1.1',{from:[-110,0],d:.1}]]);
  actor('Wn',[[10,'1.0.1.2',{d:.15}],[11,'2.2'],[13,'1.0.1.2',{from:[-110,0],d:.15}]]);
  for(var i=0;i<13;i++){actor('B'+i,[[10,'1.1.'+i,{from:[0,10],d:.25+i*.04}],[13,'1.1.'+i,{from:[0,10],d:.3+i*.03}]])}
  for(var j=0;j<4;j++){actor('D'+j,[[12,'3.'+j,{from:[0,40],d:.2+j*.14,s0:.4}]])}

  function place(u,kf,x,y,sx,sy,color,op,clip){
    u.setAttribute('href','#'+kf.id);
    u.setAttribute('transform','translate('+x.toFixed(2)+' '+y.toFixed(2)+') scale('+sx.toFixed(4)+' '+sy.toFixed(4)+') translate('+(-kf.ncx).toFixed(2)+' '+(-kf.ncy).toFixed(2)+')');
    u.style.color=color;u.style.opacity=op<=0?0:op;
    if(clip)u.setAttribute('clip-path','url(#'+clip+')');else u.removeAttribute('clip-path');
    u.style.display='';
  }
  function draw(a,k,t){
    a.under.style.display='none';a.over.style.display='none';
    var A=a.kf[k], B=k<N-1?a.kf[k+1]:null;
    if(A&&B){
      var o=B.o,d=o.d||0,tt=ease(cl((t-d)/(1-d)));
      var cx=lerp(A.cx,B.cx,tt),cy=lerp(A.cy,B.cy,tt);
      if(!o.x){                                  // ista oblika: premik + povečava (+ zrcaljenje)
        var sg=Math.max(B.w,B.h)/Math.max(A.w,A.h), s=lerp(1,sg,tt), fx=o.flip?1-2*tt:1;
        place(a.over,A,cx,cy,s*fx,s,mix(A.color,B.color,tt),1);
      }else{                                     // druga oblika: prelitje (nova pod staro)
        place(a.under,B,cx,cy,1,1,B.color,cl(tt*3));
        place(a.over,A,cx,cy,1,1,A.color,1-cl((tt-.3)/.7));
      }
    }else if(A){                                 // ugasne
      var out=A.o.out||[0,0],te=ease(t);
      place(a.over,A,A.cx+out[0]*te,A.cy+out[1]*te,1,1,A.color,1-cl(t*1.6));
    }else if(B){                                 // se pojavi
      var ob=B.o,db=ob.d||0,tb=ease(cl((t-db)/(1-db))),fr=ob.from||[0,0],s0=ob.s0||.94,sc=lerp(s0,1,tb);
      if(ob.wipe&&a.rect){a.rect.setAttribute('width',tb.toFixed(4));place(a.under,B,B.cx,B.cy,1,1,B.color,tb>0?1:0,a.clip)}
      else place(a.under,B,B.cx+fr[0]*(1-tb),B.cy+fr[1]*(1-tb),sc,sc,B.color,tb);
    }
  }

  var pos=0, playing=false, raf=0, last=0, speed=1, twRaf=0;
  function render(){
    var k=Math.min(N-1,Math.floor(pos+1e-9)), u=pos-k, t=0;
    if(k<N-1&&u>HOLD)t=ease((u-HOLD)/(1-HOLD));
    var k1=Math.min(N-1,k+1);
    var cs=lerp(CS[k],CS[k1],t), cy=lerp(CY[k],CY[k1],t);
    cam.setAttribute('transform','translate(840 300) scale('+cs.toFixed(4)+') translate(0 '+(-cy).toFixed(2)+')');
    // pri zunanjem ease je t že zglajen; actorji ga ponovno gladijo samo za zakasnitve
    var tl=(k<N-1&&u>HOLD)?(u-HOLD)/(1-HOLD):0;
    actors.forEach(function(a){draw(a,k,tl)});
    patc.setAttribute('r',k===12?(2000*ease(tl)).toFixed(1):(k>=13?2000:0));
    var act=Math.min(N-1,Math.round(pos));
    el.ths.forEach(function(b,i){b.classList.toggle('on',i===act)});
    var ch=act<3?0:act<6?1:act<9?2:3;
    el.chap.forEach(function(s,i){s.classList.toggle('on',i===ch)});
    el.fc.textContent=(act<9?'0':'')+(act+1)+' / '+N;
    el.scrub.value=Math.round(pos*100);
    el.scrub.style.setProperty('--p',(pos/(N-1)*100)+'%');
    el.play.textContent=playing?'Pavza':(pos>=N-1-1e-6?'Ponovi':'Predvajaj');
  }
  function stopAll(){playing=false;cancelAnimationFrame(raf);cancelAnimationFrame(twRaf)}
  function tick(now){
    if(!playing)return;
    pos=Math.max(0,Math.min(N-1,pos+Math.max(0,now-last)*speed/FD));last=now;render();
    if(pos>=N-1){playing=false;render();return}
    raf=requestAnimationFrame(tick);
  }
  function play(from){stopAll();pos=from;playing=true;last=performance.now();raf=requestAnimationFrame(tick)}
  function tween(target){                        // animiran skok (korak ali klik na sličico)
    stopAll();var from=pos,dur=650+160*Math.abs(target-from),t0=performance.now();
    if(Math.abs(target-from)<1.001&&target>from)from=Math.max(from,Math.floor(target)-1+HOLD);
    if(Math.abs(target-from)<1.001&&target<from)from=Math.min(from,Math.ceil(target)+1-0);
    pos=from;
    (function f(now){var p=cl((now-t0)/dur);pos=lerp(from,target,p<.5?2*p*p:1-Math.pow(-2*p+2,2)/2);render();if(p<1)twRaf=requestAnimationFrame(f);else{pos=target;render()}})(t0);
  }
  el.play.onclick=function(){if(playing){stopAll();render()}else play(pos>=N-1-1e-6?0:pos)};
  el.scrub.oninput=function(){stopAll();pos=el.scrub.value/100;render()};
  el.ths.forEach(function(b){b.onclick=function(){tween(+b.dataset.k)}});
  function step(dir){var r=Math.round(pos),near=Math.abs(pos-r)<.02;var tgt=dir>0?(near?r+1:Math.ceil(pos)):(near?r-1:Math.floor(pos));tween(Math.max(0,Math.min(N-1,tgt)))}
  $('#stepf').onclick=function(){step(1)};$('#stepb').onclick=function(){step(-1)};
  el.spd.onclick=function(){speed=speed===1?2:1;el.spd.textContent=speed+'×'};
  addEventListener('keydown',function(e){if(!slides[cur]||!slides[cur].hasAttribute('data-anim'))return;if(e.key==='.')step(1);else if(e.key===',')step(-1)});
  render();
  return {restart:function(){stopAll();pos=0;render();setTimeout(function(){if(slides[cur]&&slides[cur].hasAttribute('data-anim'))play(0)},600)},
          stop:stopAll,seek:function(v){stopAll();pos=v;render()},actors:actors};
})();
