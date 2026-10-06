const videos=[...document.querySelectorAll('video')];
const reduced=window.matchMedia('(prefers-reduced-motion: reduce)');
let globalPause=reduced.matches;
const motion=document.querySelector('#motion');
const sync=()=>{motion.textContent=globalPause?'Lire les boucles':'Mettre les boucles en pause';motion.setAttribute('aria-pressed',String(globalPause))};
const setButton=v=>{const b=v.parentElement.querySelector('button');if(b){b.textContent=v.paused?'▶':'Ⅱ';b.setAttribute('aria-label',v.paused?'Lire cet extrait':'Mettre cet extrait en pause')}};
videos.forEach(v=>{v.muted=true;if(globalPause){v.removeAttribute('autoplay');v.pause()}v.addEventListener('play',()=>setButton(v));v.addEventListener('pause',()=>setButton(v));const b=v.parentElement.querySelector('button');if(b)b.addEventListener('click',()=>{if(v.paused){v.dataset.paused='';v.play().catch(()=>{})}else{v.dataset.paused='true';v.pause()}})});
const observer=new IntersectionObserver(entries=>entries.forEach(({target:v,isIntersecting})=>{v.dataset.visible=String(isIntersecting);if(isIntersecting&&!globalPause&&v.dataset.paused!=='true')v.play().catch(()=>{});else v.pause()}),{threshold:.12});videos.forEach(v=>observer.observe(v));
motion.addEventListener('click',()=>{globalPause=!globalPause;sync();videos.forEach(v=>{if(globalPause)v.pause();else if(v.dataset.visible==='true'){v.dataset.paused='';v.play().catch(()=>{})}})});sync();
