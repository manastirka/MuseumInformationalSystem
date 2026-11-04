const al={ucitavanjeUdzbenika:"Учитавање уџбеника…",ucitavanjeLekcije:"Учитавање лекције…",ucitavanjeScene:"Учитавање 3D приказа…",greskaUcitavanja:"Грешка при учитавању — покушај поново",pokusajPonovo:"Покушај поново",nemaSecureFetch:"Безбедно слање (secureFetch) није доступно на овој страници.",greskaCuvanjaNapretka:"Чување напретка није успело.",sadrzajDugme:"Садржај уџбеника",navigacijaAria:"Поглавља и лекције",napredakOznaka:"Завршено лекција",zavrsenaLekcijaOznaka:"Завршено",nezavrsenaLekcijaOznaka:"Није завршено",zavrsiLekciju:"Заврши лекцију",cuvanjeNapretka:"Чување…",lekcijaZavrsenaPoruka:"Лекција је означена као завршена.",sacuvajPonovo:"Сачувај напредак поново",prethodnaLekcija:"Претходна лекција",sledecaLekcija:"Следећа лекција",navigacijaLekcijeAria:"Навигација између лекција",tabelaAria:"Табела података",porekloFotografija:"Фотографија",porekloCrtez:"Цртеж",porekloAiIlustracija:"АИ илустрација",porekloDijagram:"Дијаграм",autorOznaka:"Аутор",primerakNedostupan:"Примерак тренутно није доступан",primerakNedostupanPodrazumevano:"Подаци о примерку се не могу приказати.",inventarniBroj:"Инв. бр.",lokalitet:"Локалитет",otvoriKarticuPrimerka:"Отвори картицу примерка у МИС-у",napomenaInfo:"Напомена",napomenaPazi:"Пажња",napomenaZanimljivost:"Занимљивост",proveriOdgovor:"Провери одговор",izaberiOdgovorUpozorenje:"Изаберите бар један одговор пре провере.",odgovorTacan:"Тачно!",odgovorNetacan:"Није тачно — погледајте објашњење.",oznakaTacnogOdgovora:"тачан одговор",oznakaViseTacnih:"Могуће је више тачних одговора.",kvizRezime:"Квиз у лекцији",scenaResetuj:"Ресетуј",scenaResetujAria:"Ресетуј камеру и стање сцене",scenaPauza:"Пауза",scenaPauzaAria:"Паузирај анимацију сцене",scenaNastavi:"Настави",scenaNastaviAria:"Настави анимацију сцене",scenaKorak:"Корак",scenaKorakAria:"Помери анимацију за један корак",scenaPrikaziObjasnjenje:"Прикажи објашњење",scenaSakrijObjasnjenje:"Сакриј објашњење",scenaObjasnjenjeAria:"Прикажи текстуално објашњење сцене",scenaZumPlusAria:"Увећај приказ",scenaZumMinusAria:"Умањи приказ",scenaDodirSavet:"Додирните приказ за ротацију једним прстом (или ротирајте са два прста)",scenaDodirAktivan:"3D ротација активна — заврши за скрол стране",scenaRezervaOznaka:"Статични приказ (3D WebGL није доступан)",strukturaNedostupna:"Структура није доступна за овај минерал",legendaElemenata:"Легенда хемијских елемената (CPK боје и полупречници)",poluprecniciJonskiOznaka:"Полупречници сфера: јонски",poluprecniciKovalentniOznaka:"Полупречници сфера: ковалентни",kovalentnaRezervaOznaka:"ковалентни за елементе ван јонске табеле",detekcijaVezaKovalentniOznaka:"детекција веза: ковалентни ×",faktorVeza:"Праг дужине веза",sledeciAtom:"Следећи атом",atomKoordinate:"Фракционе координате",izaberiKristalniSistem:"Кристални системи",apsolutnaTvrdocaPreklopnik:"Апсолутна тврдоћа (Knoop)",ordinalnaTvrdocaOznaka:"Мосова ординална скала (1–10)",terenskeProbeOznaka:"Теренске пробе",probaGrebanja:"Проба гребања",zameniMinerale:"Обрни смер гребања",izvorPodataka:"Извор",brojPravacaCepljivosti:"Број праваца",ugloviCepljivosti:"Углови",primerMinerala:"Пример",prelazFormi:"Однос форми (прелаз хабитуса)",aktivnaForma:"Кристална форма"},sl={А:"A",Б:"B",В:"V",Г:"G",Д:"D",Ђ:"Đ",Е:"E",Ж:"Ž",З:"Z",И:"I",Ј:"J",К:"K",Л:"L",Љ:"Lj",М:"M",Н:"N",Њ:"Nj",О:"O",П:"P",Р:"R",С:"S",Т:"T",Ћ:"Ć",У:"U",Ф:"F",Х:"H",Ц:"C",Ч:"Č",Џ:"Dž",Ш:"Š",а:"a",б:"b",в:"v",г:"g",д:"d",ђ:"đ",е:"e",ж:"ž",з:"z",и:"i",ј:"j",к:"k",л:"l",љ:"lj",м:"m",н:"n",њ:"nj",о:"o",п:"p",р:"r",с:"s",т:"t",ћ:"ć",у:"u",ф:"f",х:"h",ц:"c",ч:"č",џ:"dž",ш:"š"};function ol(n){let e="";for(const t of n)e+=sl[t]??t;return e}let mc="cyrl";function v0(n){mc=n}function Ge(n){const e=al[n];return mc==="latn"?ol(e):e}class At extends Error{status;constructor(e,t=0){super(e),this.name="ApiGreska",this.status=t}}function cl(n,e){const t=n.replace(/\/+$/,""),i=`/${e}`;if(e&&t.endsWith(i))return t.slice(0,t.length-i.length)||"/api/udzbenik";const r=t.lastIndexOf("/");return r>0?t.slice(0,r):t}function x0(n){const e=(n.dataset.api??"").trim(),t=(n.dataset.zbirka??"minerali").trim();if(!e)throw new At("Недостаје обавезан атрибут data-api на #udzbenik-app.");const i=(n.dataset.apiKoren??"").trim()||cl(e,t),a=(n.dataset.pismo??"cyrl").trim().toLowerCase()==="latn"?"latn":"cyrl";return{api:e.replace(/\/+$/,""),apiKoren:i.replace(/\/+$/,""),zbirka:t,pocetnoPoglavlje:(n.dataset.poglavlje??"").trim(),pocetnaLekcija:(n.dataset.lekcija??"").trim(),pismo:a,mozeUredjuje:n.dataset.mozeUredjuje==="true"}}async function Kr(n,e){try{const t=await n.text();if(!t)return e;const i=JSON.parse(t);if(typeof i.greska=="string"&&i.greska.trim())return i.greska.trim()}catch{}return e}class M0{konfig;kesStruktura=new Map;constructor(e){this.konfig=e}get konfiguracija(){return this.konfig}ocistiKes(){this.kesStruktura.clear()}async ucitajUdzbenik(){let e;try{e=await fetch(this.konfig.api,{method:"GET",headers:{Accept:"application/json"}})}catch{throw new At(Ge("greskaUcitavanja"),0)}if(!e.ok){const t=await Kr(e,Ge("greskaUcitavanja"));throw new At(t,e.status)}try{return await e.json()}catch{throw new At(Ge("greskaUcitavanja"),e.status)}}async ucitajLekciju(e,t){const i=`${this.konfig.api}/lekcija/${encodeURIComponent(e)}/${encodeURIComponent(t)}`;let r;try{r=await fetch(i,{method:"GET",headers:{Accept:"application/json"}})}catch{throw new At(Ge("greskaUcitavanja"),0)}if(!r.ok){const a=await Kr(r,Ge("greskaUcitavanja"));throw new At(a,r.status)}try{return await r.json()}catch{throw new At(Ge("greskaUcitavanja"),r.status)}}async posaljiNapredak(e){if(typeof window>"u"||typeof window.secureFetch!="function")throw new At(Ge("nemaSecureFetch"),0);const t=`${this.konfig.apiKoren}/napredak`;let i;try{i=await window.secureFetch(t,{method:"POST",headers:{"Content-Type":"application/json",Accept:"application/json"},body:JSON.stringify(e)})}catch{throw new At(Ge("greskaCuvanjaNapretka"),0)}let r=null;try{r=await i.json()}catch{r=null}if(!i.ok||!r?.ok){const a=typeof r?.greska=="string"&&r.greska.trim()?r.greska.trim():Ge("greskaCuvanjaNapretka");throw new At(a,i.status)}return r}async ucitajStrukturuCif(e){const t=e.trim().toLowerCase(),i=this.kesStruktura.get(t);if(i)return i;const r=`${this.konfig.apiKoren}/struktura/${encodeURIComponent(e.trim())}`,a=(async()=>{let s;try{s=await fetch(r,{method:"GET",headers:{Accept:"text/plain, */*"}})}catch{throw this.kesStruktura.delete(t),new At(Ge("greskaUcitavanja"),0)}if(s.status===404)throw new At(Ge("strukturaNedostupna"),404);if(!s.ok){this.kesStruktura.delete(t);const o=await Kr(s,Ge("greskaUcitavanja"));throw new At(o,s.status)}return s.text()})();return a.catch(s=>{s instanceof At&&s.status===404||this.kesStruktura.delete(t)}),this.kesStruktura.set(t,a),a}}const ll=["--bg-body","--bg-card","--bg-elevated","--bg-hover","--text-primary","--text-secondary","--text-muted","--primary","--primary-light","--primary-dark","--accent","--accent-light","--accent-strong","--on-accent","--border-color","--border-strong","--focus-ring","--success","--success-soft","--warning","--warning-soft","--danger","--danger-soft","--info","--info-soft","--font-family","--font-display","--font-size-sm","--font-size-base","--font-size-lg","--lh-base","--radius-sm","--radius-md","--radius-card","--radius-btn","--shadow-sm","--shadow-card","--space-1","--space-2","--space-3","--space-4","--space-6","--space-8","--transition-fast","--transition-base"],gc={"--font-family":'system-ui, -apple-system, "Segoe UI", Roboto, sans-serif',"--font-display":'system-ui, -apple-system, "Segoe UI", Roboto, sans-serif',"--font-size-sm":"0.875rem","--font-size-base":"1rem","--font-size-lg":"1.25rem","--lh-base":"1.6","--radius-sm":"4px","--radius-md":"8px","--radius-card":"12px","--radius-btn":"8px","--space-1":"0.25rem","--space-2":"0.5rem","--space-3":"0.75rem","--space-4":"1rem","--space-6":"1.5rem","--space-8":"2rem","--transition-fast":"150ms ease","--transition-base":"240ms ease"},Qs={...gc,"--bg-body":"#f5f6f8","--bg-card":"#ffffff","--bg-elevated":"#eef1f5","--bg-hover":"#e3e8ef","--text-primary":"#161b22","--text-secondary":"#424d5c","--text-muted":"#596577","--primary":"#1b5e4a","--primary-light":"#e4f2ed","--primary-dark":"#124234","--accent":"#0f5c8c","--accent-light":"#e3f0f9","--accent-strong":"#0a4368","--on-accent":"#ffffff","--border-color":"#768396","--border-strong":"#4f5b6b","--focus-ring":"#0f5c8c","--success":"#166534","--success-soft":"#e6f5ec","--warning":"#854d0e","--warning-soft":"#fef3db","--danger":"#991b1b","--danger-soft":"#fdeaea","--info":"#1e4e8c","--info-soft":"#e8f0fb","--shadow-sm":"0 1px 2px rgba(15, 20, 26, 0.08)","--shadow-card":"0 2px 8px rgba(15, 20, 26, 0.10)"},eo={...gc,"--bg-body":"#0f141a","--bg-card":"#18202a","--bg-elevated":"#212b38","--bg-hover":"#2b3848","--text-primary":"#f0f4f8","--text-secondary":"#c2cdd9","--text-muted":"#9aa8b8","--primary":"#56c7a3","--primary-light":"#1c3b33","--primary-dark":"#7adbb9","--accent":"#63b3ed","--accent-light":"#1b3247","--accent-strong":"#90cdf4","--on-accent":"#0f141a","--border-color":"#68788c","--border-strong":"#8fa0b5","--focus-ring":"#63b3ed","--success":"#5fd38d","--success-soft":"#163324","--warning":"#f6c453","--warning-soft":"#362a12","--danger":"#f88080","--danger-soft":"#3b1c20","--info":"#76b9f5","--info-soft":"#192e45","--shadow-sm":"0 1px 3px rgba(0, 0, 0, 0.35)","--shadow-card":"0 4px 12px rgba(0, 0, 0, 0.45)"},ul=["data-theme","data-palette","data-accent","data-style","data-density","data-bs-theme"];function dl(n=document.documentElement){const e=(n.getAttribute("data-theme")??"").toLowerCase(),t=(n.getAttribute("data-bs-theme")??"").toLowerCase();return e==="dark"||t==="dark"?!0:e==="light"||t==="light"?!1:typeof window<"u"&&typeof window.matchMedia=="function"?window.matchMedia("(prefers-color-scheme: dark)").matches:!1}class hl{slusaoci=new Set;posmatrac=null;medijaUpit=null;medijaSlusalac=null;kesiraniTokeni=new Map;ciljniKontejner=null;povezi(e){this.ciljniKontejner=e??null,this.osvezi(),typeof MutationObserver<"u"&&typeof document<"u"&&(this.posmatrac?.disconnect(),this.posmatrac=new MutationObserver(()=>{this.osvezi()}),this.posmatrac.observe(document.documentElement,{attributes:!0,attributeFilter:ul})),typeof window<"u"&&typeof window.matchMedia=="function"&&(this.medijaUpit=window.matchMedia("(prefers-color-scheme: dark)"),this.medijaSlusalac=()=>this.osvezi(),this.medijaUpit.addEventListener("change",this.medijaSlusalac))}odspoji(){this.posmatrac?.disconnect(),this.posmatrac=null,this.medijaUpit&&this.medijaSlusalac&&this.medijaUpit.removeEventListener("change",this.medijaSlusalac),this.medijaUpit=null,this.medijaSlusalac=null,this.slusaoci.clear()}pretplati(e){return this.slusaoci.add(e),()=>{this.slusaoci.delete(e)}}jeTamna(){return typeof document>"u"?!1:dl(document.documentElement)}osvezi(){this.kesiraniTokeni.clear();const t=this.jeTamna()?eo:Qs,i=typeof window<"u"&&typeof document<"u"?window.getComputedStyle(document.documentElement):null;for(const r of ll){const a=i?i.getPropertyValue(r).trim():"",s=a||t[r];this.kesiraniTokeni.set(r,s),this.ciljniKontejner&&(a?this.ciljniKontejner.style.removeProperty(r):this.ciljniKontejner.style.setProperty(r,t[r]))}for(const r of this.slusaoci)r(this)}token(e){const t=this.kesiraniTokeni.get(e);if(t)return t;const i=this.jeTamna()?eo:Qs;if(typeof window<"u"&&typeof document<"u"){const r=window.getComputedStyle(document.documentElement).getPropertyValue(e).trim();if(r)return r}return i[e]}}const qr=new hl;/**
 * @license
 * Copyright 2010-2025 Three.js Authors
 * SPDX-License-Identifier: MIT
 */const Rs="174",fl=0,to=1,pl=2,_c=1,ml=2,hn=3,Ln=0,Lt=1,St=2,Pn=0,Si=1,no=2,io=3,ro=4,gl=5,Kn=100,_l=101,vl=102,xl=103,Ml=104,Sl=200,El=201,bl=202,yl=203,Ia=204,Ua=205,Tl=206,wl=207,Al=208,Rl=209,Cl=210,Pl=211,Dl=212,Ll=213,Il=214,za=0,Na=1,ka=2,yi=3,Fa=4,Oa=5,Ba=6,ja=7,vc=0,Ul=1,zl=2,Dn=0,Nl=1,kl=2,Fl=3,Ol=4,Bl=5,jl=6,Vl=7,xc=300,Ti=301,wi=302,Va=303,Ha=304,Vr=306,Ga=1e3,$n=1001,Wa=1002,Jt=1003,Hl=1004,tr=1005,tn=1006,$r=1007,Yn=1008,vn=1009,Mc=1010,Sc=1011,Xi=1012,Cs=1013,Qn=1014,pn=1015,$i=1016,Ps=1017,Ds=1018,Ai=1020,Ec=35902,bc=1021,yc=1022,Zt=1023,Tc=1024,wc=1025,Ei=1026,Ri=1027,Ac=1028,Ls=1029,Rc=1030,Is=1031,Us=1033,Rr=33776,Cr=33777,Pr=33778,Dr=33779,Xa=35840,Ka=35841,qa=35842,$a=35843,Ya=36196,Za=37492,Ja=37496,Qa=37808,es=37809,ts=37810,ns=37811,is=37812,rs=37813,as=37814,ss=37815,os=37816,cs=37817,ls=37818,us=37819,ds=37820,hs=37821,Lr=36492,fs=36494,ps=36495,Cc=36283,ms=36284,gs=36285,_s=36286,Gl=3200,Wl=3201,Pc=0,Xl=1,Rn="",Ft="srgb",Ci="srgb-linear",Nr="linear",rt="srgb",ni=7680,ao=519,Kl=512,ql=513,$l=514,Dc=515,Yl=516,Zl=517,Jl=518,Ql=519,so=35044,oo="300 es",mn=2e3,kr=2001;class Di{addEventListener(e,t){this._listeners===void 0&&(this._listeners={});const i=this._listeners;i[e]===void 0&&(i[e]=[]),i[e].indexOf(t)===-1&&i[e].push(t)}hasEventListener(e,t){const i=this._listeners;return i===void 0?!1:i[e]!==void 0&&i[e].indexOf(t)!==-1}removeEventListener(e,t){const i=this._listeners;if(i===void 0)return;const r=i[e];if(r!==void 0){const a=r.indexOf(t);a!==-1&&r.splice(a,1)}}dispatchEvent(e){const t=this._listeners;if(t===void 0)return;const i=t[e.type];if(i!==void 0){e.target=this;const r=i.slice(0);for(let a=0,s=r.length;a<s;a++)r[a].call(this,e);e.target=null}}}const yt=["00","01","02","03","04","05","06","07","08","09","0a","0b","0c","0d","0e","0f","10","11","12","13","14","15","16","17","18","19","1a","1b","1c","1d","1e","1f","20","21","22","23","24","25","26","27","28","29","2a","2b","2c","2d","2e","2f","30","31","32","33","34","35","36","37","38","39","3a","3b","3c","3d","3e","3f","40","41","42","43","44","45","46","47","48","49","4a","4b","4c","4d","4e","4f","50","51","52","53","54","55","56","57","58","59","5a","5b","5c","5d","5e","5f","60","61","62","63","64","65","66","67","68","69","6a","6b","6c","6d","6e","6f","70","71","72","73","74","75","76","77","78","79","7a","7b","7c","7d","7e","7f","80","81","82","83","84","85","86","87","88","89","8a","8b","8c","8d","8e","8f","90","91","92","93","94","95","96","97","98","99","9a","9b","9c","9d","9e","9f","a0","a1","a2","a3","a4","a5","a6","a7","a8","a9","aa","ab","ac","ad","ae","af","b0","b1","b2","b3","b4","b5","b6","b7","b8","b9","ba","bb","bc","bd","be","bf","c0","c1","c2","c3","c4","c5","c6","c7","c8","c9","ca","cb","cc","cd","ce","cf","d0","d1","d2","d3","d4","d5","d6","d7","d8","d9","da","db","dc","dd","de","df","e0","e1","e2","e3","e4","e5","e6","e7","e8","e9","ea","eb","ec","ed","ee","ef","f0","f1","f2","f3","f4","f5","f6","f7","f8","f9","fa","fb","fc","fd","fe","ff"],Ir=Math.PI/180,vs=180/Math.PI;function Yi(){const n=Math.random()*4294967295|0,e=Math.random()*4294967295|0,t=Math.random()*4294967295|0,i=Math.random()*4294967295|0;return(yt[n&255]+yt[n>>8&255]+yt[n>>16&255]+yt[n>>24&255]+"-"+yt[e&255]+yt[e>>8&255]+"-"+yt[e>>16&15|64]+yt[e>>24&255]+"-"+yt[t&63|128]+yt[t>>8&255]+"-"+yt[t>>16&255]+yt[t>>24&255]+yt[i&255]+yt[i>>8&255]+yt[i>>16&255]+yt[i>>24&255]).toLowerCase()}function Xe(n,e,t){return Math.max(e,Math.min(t,n))}function eu(n,e){return(n%e+e)%e}function Yr(n,e,t){return(1-t)*n+t*e}function Fi(n,e){switch(e.constructor){case Float32Array:return n;case Uint32Array:return n/4294967295;case Uint16Array:return n/65535;case Uint8Array:return n/255;case Int32Array:return Math.max(n/2147483647,-1);case Int16Array:return Math.max(n/32767,-1);case Int8Array:return Math.max(n/127,-1);default:throw new Error("Invalid component type.")}}function Dt(n,e){switch(e.constructor){case Float32Array:return n;case Uint32Array:return Math.round(n*4294967295);case Uint16Array:return Math.round(n*65535);case Uint8Array:return Math.round(n*255);case Int32Array:return Math.round(n*2147483647);case Int16Array:return Math.round(n*32767);case Int8Array:return Math.round(n*127);default:throw new Error("Invalid component type.")}}class Ke{constructor(e=0,t=0){Ke.prototype.isVector2=!0,this.x=e,this.y=t}get width(){return this.x}set width(e){this.x=e}get height(){return this.y}set height(e){this.y=e}set(e,t){return this.x=e,this.y=t,this}setScalar(e){return this.x=e,this.y=e,this}setX(e){return this.x=e,this}setY(e){return this.y=e,this}setComponent(e,t){switch(e){case 0:this.x=t;break;case 1:this.y=t;break;default:throw new Error("index is out of range: "+e)}return this}getComponent(e){switch(e){case 0:return this.x;case 1:return this.y;default:throw new Error("index is out of range: "+e)}}clone(){return new this.constructor(this.x,this.y)}copy(e){return this.x=e.x,this.y=e.y,this}add(e){return this.x+=e.x,this.y+=e.y,this}addScalar(e){return this.x+=e,this.y+=e,this}addVectors(e,t){return this.x=e.x+t.x,this.y=e.y+t.y,this}addScaledVector(e,t){return this.x+=e.x*t,this.y+=e.y*t,this}sub(e){return this.x-=e.x,this.y-=e.y,this}subScalar(e){return this.x-=e,this.y-=e,this}subVectors(e,t){return this.x=e.x-t.x,this.y=e.y-t.y,this}multiply(e){return this.x*=e.x,this.y*=e.y,this}multiplyScalar(e){return this.x*=e,this.y*=e,this}divide(e){return this.x/=e.x,this.y/=e.y,this}divideScalar(e){return this.multiplyScalar(1/e)}applyMatrix3(e){const t=this.x,i=this.y,r=e.elements;return this.x=r[0]*t+r[3]*i+r[6],this.y=r[1]*t+r[4]*i+r[7],this}min(e){return this.x=Math.min(this.x,e.x),this.y=Math.min(this.y,e.y),this}max(e){return this.x=Math.max(this.x,e.x),this.y=Math.max(this.y,e.y),this}clamp(e,t){return this.x=Xe(this.x,e.x,t.x),this.y=Xe(this.y,e.y,t.y),this}clampScalar(e,t){return this.x=Xe(this.x,e,t),this.y=Xe(this.y,e,t),this}clampLength(e,t){const i=this.length();return this.divideScalar(i||1).multiplyScalar(Xe(i,e,t))}floor(){return this.x=Math.floor(this.x),this.y=Math.floor(this.y),this}ceil(){return this.x=Math.ceil(this.x),this.y=Math.ceil(this.y),this}round(){return this.x=Math.round(this.x),this.y=Math.round(this.y),this}roundToZero(){return this.x=Math.trunc(this.x),this.y=Math.trunc(this.y),this}negate(){return this.x=-this.x,this.y=-this.y,this}dot(e){return this.x*e.x+this.y*e.y}cross(e){return this.x*e.y-this.y*e.x}lengthSq(){return this.x*this.x+this.y*this.y}length(){return Math.sqrt(this.x*this.x+this.y*this.y)}manhattanLength(){return Math.abs(this.x)+Math.abs(this.y)}normalize(){return this.divideScalar(this.length()||1)}angle(){return Math.atan2(-this.y,-this.x)+Math.PI}angleTo(e){const t=Math.sqrt(this.lengthSq()*e.lengthSq());if(t===0)return Math.PI/2;const i=this.dot(e)/t;return Math.acos(Xe(i,-1,1))}distanceTo(e){return Math.sqrt(this.distanceToSquared(e))}distanceToSquared(e){const t=this.x-e.x,i=this.y-e.y;return t*t+i*i}manhattanDistanceTo(e){return Math.abs(this.x-e.x)+Math.abs(this.y-e.y)}setLength(e){return this.normalize().multiplyScalar(e)}lerp(e,t){return this.x+=(e.x-this.x)*t,this.y+=(e.y-this.y)*t,this}lerpVectors(e,t,i){return this.x=e.x+(t.x-e.x)*i,this.y=e.y+(t.y-e.y)*i,this}equals(e){return e.x===this.x&&e.y===this.y}fromArray(e,t=0){return this.x=e[t],this.y=e[t+1],this}toArray(e=[],t=0){return e[t]=this.x,e[t+1]=this.y,e}fromBufferAttribute(e,t){return this.x=e.getX(t),this.y=e.getY(t),this}rotateAround(e,t){const i=Math.cos(t),r=Math.sin(t),a=this.x-e.x,s=this.y-e.y;return this.x=a*i-s*r+e.x,this.y=a*r+s*i+e.y,this}random(){return this.x=Math.random(),this.y=Math.random(),this}*[Symbol.iterator](){yield this.x,yield this.y}}class Be{constructor(e,t,i,r,a,s,o,c,l){Be.prototype.isMatrix3=!0,this.elements=[1,0,0,0,1,0,0,0,1],e!==void 0&&this.set(e,t,i,r,a,s,o,c,l)}set(e,t,i,r,a,s,o,c,l){const d=this.elements;return d[0]=e,d[1]=r,d[2]=o,d[3]=t,d[4]=a,d[5]=c,d[6]=i,d[7]=s,d[8]=l,this}identity(){return this.set(1,0,0,0,1,0,0,0,1),this}copy(e){const t=this.elements,i=e.elements;return t[0]=i[0],t[1]=i[1],t[2]=i[2],t[3]=i[3],t[4]=i[4],t[5]=i[5],t[6]=i[6],t[7]=i[7],t[8]=i[8],this}extractBasis(e,t,i){return e.setFromMatrix3Column(this,0),t.setFromMatrix3Column(this,1),i.setFromMatrix3Column(this,2),this}setFromMatrix4(e){const t=e.elements;return this.set(t[0],t[4],t[8],t[1],t[5],t[9],t[2],t[6],t[10]),this}multiply(e){return this.multiplyMatrices(this,e)}premultiply(e){return this.multiplyMatrices(e,this)}multiplyMatrices(e,t){const i=e.elements,r=t.elements,a=this.elements,s=i[0],o=i[3],c=i[6],l=i[1],d=i[4],h=i[7],f=i[2],m=i[5],g=i[8],_=r[0],p=r[3],u=r[6],b=r[1],S=r[4],M=r[7],w=r[2],T=r[5],A=r[8];return a[0]=s*_+o*b+c*w,a[3]=s*p+o*S+c*T,a[6]=s*u+o*M+c*A,a[1]=l*_+d*b+h*w,a[4]=l*p+d*S+h*T,a[7]=l*u+d*M+h*A,a[2]=f*_+m*b+g*w,a[5]=f*p+m*S+g*T,a[8]=f*u+m*M+g*A,this}multiplyScalar(e){const t=this.elements;return t[0]*=e,t[3]*=e,t[6]*=e,t[1]*=e,t[4]*=e,t[7]*=e,t[2]*=e,t[5]*=e,t[8]*=e,this}determinant(){const e=this.elements,t=e[0],i=e[1],r=e[2],a=e[3],s=e[4],o=e[5],c=e[6],l=e[7],d=e[8];return t*s*d-t*o*l-i*a*d+i*o*c+r*a*l-r*s*c}invert(){const e=this.elements,t=e[0],i=e[1],r=e[2],a=e[3],s=e[4],o=e[5],c=e[6],l=e[7],d=e[8],h=d*s-o*l,f=o*c-d*a,m=l*a-s*c,g=t*h+i*f+r*m;if(g===0)return this.set(0,0,0,0,0,0,0,0,0);const _=1/g;return e[0]=h*_,e[1]=(r*l-d*i)*_,e[2]=(o*i-r*s)*_,e[3]=f*_,e[4]=(d*t-r*c)*_,e[5]=(r*a-o*t)*_,e[6]=m*_,e[7]=(i*c-l*t)*_,e[8]=(s*t-i*a)*_,this}transpose(){let e;const t=this.elements;return e=t[1],t[1]=t[3],t[3]=e,e=t[2],t[2]=t[6],t[6]=e,e=t[5],t[5]=t[7],t[7]=e,this}getNormalMatrix(e){return this.setFromMatrix4(e).invert().transpose()}transposeIntoArray(e){const t=this.elements;return e[0]=t[0],e[1]=t[3],e[2]=t[6],e[3]=t[1],e[4]=t[4],e[5]=t[7],e[6]=t[2],e[7]=t[5],e[8]=t[8],this}setUvTransform(e,t,i,r,a,s,o){const c=Math.cos(a),l=Math.sin(a);return this.set(i*c,i*l,-i*(c*s+l*o)+s+e,-r*l,r*c,-r*(-l*s+c*o)+o+t,0,0,1),this}scale(e,t){return this.premultiply(Zr.makeScale(e,t)),this}rotate(e){return this.premultiply(Zr.makeRotation(-e)),this}translate(e,t){return this.premultiply(Zr.makeTranslation(e,t)),this}makeTranslation(e,t){return e.isVector2?this.set(1,0,e.x,0,1,e.y,0,0,1):this.set(1,0,e,0,1,t,0,0,1),this}makeRotation(e){const t=Math.cos(e),i=Math.sin(e);return this.set(t,-i,0,i,t,0,0,0,1),this}makeScale(e,t){return this.set(e,0,0,0,t,0,0,0,1),this}equals(e){const t=this.elements,i=e.elements;for(let r=0;r<9;r++)if(t[r]!==i[r])return!1;return!0}fromArray(e,t=0){for(let i=0;i<9;i++)this.elements[i]=e[i+t];return this}toArray(e=[],t=0){const i=this.elements;return e[t]=i[0],e[t+1]=i[1],e[t+2]=i[2],e[t+3]=i[3],e[t+4]=i[4],e[t+5]=i[5],e[t+6]=i[6],e[t+7]=i[7],e[t+8]=i[8],e}clone(){return new this.constructor().fromArray(this.elements)}}const Zr=new Be;function Lc(n){for(let e=n.length-1;e>=0;--e)if(n[e]>=65535)return!0;return!1}function Fr(n){return document.createElementNS("http://www.w3.org/1999/xhtml",n)}function tu(){const n=Fr("canvas");return n.style.display="block",n}const co={};function Vn(n){n in co||(co[n]=!0,console.warn(n))}function nu(n,e,t){return new Promise(function(i,r){function a(){switch(n.clientWaitSync(e,n.SYNC_FLUSH_COMMANDS_BIT,0)){case n.WAIT_FAILED:r();break;case n.TIMEOUT_EXPIRED:setTimeout(a,t);break;default:i()}}setTimeout(a,t)})}function iu(n){const e=n.elements;e[2]=.5*e[2]+.5*e[3],e[6]=.5*e[6]+.5*e[7],e[10]=.5*e[10]+.5*e[11],e[14]=.5*e[14]+.5*e[15]}function ru(n){const e=n.elements;e[11]===-1?(e[10]=-e[10]-1,e[14]=-e[14]):(e[10]=-e[10],e[14]=-e[14]+1)}const lo=new Be().set(.4123908,.3575843,.1804808,.212639,.7151687,.0721923,.0193308,.1191948,.9505322),uo=new Be().set(3.2409699,-1.5373832,-.4986108,-.9692436,1.8759675,.0415551,.0556301,-.203977,1.0569715);function au(){const n={enabled:!0,workingColorSpace:Ci,spaces:{},convert:function(r,a,s){return this.enabled===!1||a===s||!a||!s||(this.spaces[a].transfer===rt&&(r.r=_n(r.r),r.g=_n(r.g),r.b=_n(r.b)),this.spaces[a].primaries!==this.spaces[s].primaries&&(r.applyMatrix3(this.spaces[a].toXYZ),r.applyMatrix3(this.spaces[s].fromXYZ)),this.spaces[s].transfer===rt&&(r.r=bi(r.r),r.g=bi(r.g),r.b=bi(r.b))),r},fromWorkingColorSpace:function(r,a){return this.convert(r,this.workingColorSpace,a)},toWorkingColorSpace:function(r,a){return this.convert(r,a,this.workingColorSpace)},getPrimaries:function(r){return this.spaces[r].primaries},getTransfer:function(r){return r===Rn?Nr:this.spaces[r].transfer},getLuminanceCoefficients:function(r,a=this.workingColorSpace){return r.fromArray(this.spaces[a].luminanceCoefficients)},define:function(r){Object.assign(this.spaces,r)},_getMatrix:function(r,a,s){return r.copy(this.spaces[a].toXYZ).multiply(this.spaces[s].fromXYZ)},_getDrawingBufferColorSpace:function(r){return this.spaces[r].outputColorSpaceConfig.drawingBufferColorSpace},_getUnpackColorSpace:function(r=this.workingColorSpace){return this.spaces[r].workingColorSpaceConfig.unpackColorSpace}},e=[.64,.33,.3,.6,.15,.06],t=[.2126,.7152,.0722],i=[.3127,.329];return n.define({[Ci]:{primaries:e,whitePoint:i,transfer:Nr,toXYZ:lo,fromXYZ:uo,luminanceCoefficients:t,workingColorSpaceConfig:{unpackColorSpace:Ft},outputColorSpaceConfig:{drawingBufferColorSpace:Ft}},[Ft]:{primaries:e,whitePoint:i,transfer:rt,toXYZ:lo,fromXYZ:uo,luminanceCoefficients:t,outputColorSpaceConfig:{drawingBufferColorSpace:Ft}}}),n}const Qe=au();function _n(n){return n<.04045?n*.0773993808:Math.pow(n*.9478672986+.0521327014,2.4)}function bi(n){return n<.0031308?n*12.92:1.055*Math.pow(n,.41666)-.055}let ii;class su{static getDataURL(e){if(/^data:/i.test(e.src)||typeof HTMLCanvasElement>"u")return e.src;let t;if(e instanceof HTMLCanvasElement)t=e;else{ii===void 0&&(ii=Fr("canvas")),ii.width=e.width,ii.height=e.height;const i=ii.getContext("2d");e instanceof ImageData?i.putImageData(e,0,0):i.drawImage(e,0,0,e.width,e.height),t=ii}return t.toDataURL("image/png")}static sRGBToLinear(e){if(typeof HTMLImageElement<"u"&&e instanceof HTMLImageElement||typeof HTMLCanvasElement<"u"&&e instanceof HTMLCanvasElement||typeof ImageBitmap<"u"&&e instanceof ImageBitmap){const t=Fr("canvas");t.width=e.width,t.height=e.height;const i=t.getContext("2d");i.drawImage(e,0,0,e.width,e.height);const r=i.getImageData(0,0,e.width,e.height),a=r.data;for(let s=0;s<a.length;s++)a[s]=_n(a[s]/255)*255;return i.putImageData(r,0,0),t}else if(e.data){const t=e.data.slice(0);for(let i=0;i<t.length;i++)t instanceof Uint8Array||t instanceof Uint8ClampedArray?t[i]=Math.floor(_n(t[i]/255)*255):t[i]=_n(t[i]);return{data:t,width:e.width,height:e.height}}else return console.warn("THREE.ImageUtils.sRGBToLinear(): Unsupported image type. No color space conversion applied."),e}}let ou=0;class zs{constructor(e=null){this.isSource=!0,Object.defineProperty(this,"id",{value:ou++}),this.uuid=Yi(),this.data=e,this.dataReady=!0,this.version=0}set needsUpdate(e){e===!0&&this.version++}toJSON(e){const t=e===void 0||typeof e=="string";if(!t&&e.images[this.uuid]!==void 0)return e.images[this.uuid];const i={uuid:this.uuid,url:""},r=this.data;if(r!==null){let a;if(Array.isArray(r)){a=[];for(let s=0,o=r.length;s<o;s++)r[s].isDataTexture?a.push(Jr(r[s].image)):a.push(Jr(r[s]))}else a=Jr(r);i.url=a}return t||(e.images[this.uuid]=i),i}}function Jr(n){return typeof HTMLImageElement<"u"&&n instanceof HTMLImageElement||typeof HTMLCanvasElement<"u"&&n instanceof HTMLCanvasElement||typeof ImageBitmap<"u"&&n instanceof ImageBitmap?su.getDataURL(n):n.data?{data:Array.from(n.data),width:n.width,height:n.height,type:n.data.constructor.name}:(console.warn("THREE.Texture: Unable to serialize Texture."),{})}let cu=0;class Ct extends Di{constructor(e=Ct.DEFAULT_IMAGE,t=Ct.DEFAULT_MAPPING,i=$n,r=$n,a=tn,s=Yn,o=Zt,c=vn,l=Ct.DEFAULT_ANISOTROPY,d=Rn){super(),this.isTexture=!0,Object.defineProperty(this,"id",{value:cu++}),this.uuid=Yi(),this.name="",this.source=new zs(e),this.mipmaps=[],this.mapping=t,this.channel=0,this.wrapS=i,this.wrapT=r,this.magFilter=a,this.minFilter=s,this.anisotropy=l,this.format=o,this.internalFormat=null,this.type=c,this.offset=new Ke(0,0),this.repeat=new Ke(1,1),this.center=new Ke(0,0),this.rotation=0,this.matrixAutoUpdate=!0,this.matrix=new Be,this.generateMipmaps=!0,this.premultiplyAlpha=!1,this.flipY=!0,this.unpackAlignment=4,this.colorSpace=d,this.userData={},this.version=0,this.onUpdate=null,this.renderTarget=null,this.isRenderTargetTexture=!1,this.pmremVersion=0}get image(){return this.source.data}set image(e=null){this.source.data=e}updateMatrix(){this.matrix.setUvTransform(this.offset.x,this.offset.y,this.repeat.x,this.repeat.y,this.rotation,this.center.x,this.center.y)}clone(){return new this.constructor().copy(this)}copy(e){return this.name=e.name,this.source=e.source,this.mipmaps=e.mipmaps.slice(0),this.mapping=e.mapping,this.channel=e.channel,this.wrapS=e.wrapS,this.wrapT=e.wrapT,this.magFilter=e.magFilter,this.minFilter=e.minFilter,this.anisotropy=e.anisotropy,this.format=e.format,this.internalFormat=e.internalFormat,this.type=e.type,this.offset.copy(e.offset),this.repeat.copy(e.repeat),this.center.copy(e.center),this.rotation=e.rotation,this.matrixAutoUpdate=e.matrixAutoUpdate,this.matrix.copy(e.matrix),this.generateMipmaps=e.generateMipmaps,this.premultiplyAlpha=e.premultiplyAlpha,this.flipY=e.flipY,this.unpackAlignment=e.unpackAlignment,this.colorSpace=e.colorSpace,this.renderTarget=e.renderTarget,this.isRenderTargetTexture=e.isRenderTargetTexture,this.userData=JSON.parse(JSON.stringify(e.userData)),this.needsUpdate=!0,this}toJSON(e){const t=e===void 0||typeof e=="string";if(!t&&e.textures[this.uuid]!==void 0)return e.textures[this.uuid];const i={metadata:{version:4.6,type:"Texture",generator:"Texture.toJSON"},uuid:this.uuid,name:this.name,image:this.source.toJSON(e).uuid,mapping:this.mapping,channel:this.channel,repeat:[this.repeat.x,this.repeat.y],offset:[this.offset.x,this.offset.y],center:[this.center.x,this.center.y],rotation:this.rotation,wrap:[this.wrapS,this.wrapT],format:this.format,internalFormat:this.internalFormat,type:this.type,colorSpace:this.colorSpace,minFilter:this.minFilter,magFilter:this.magFilter,anisotropy:this.anisotropy,flipY:this.flipY,generateMipmaps:this.generateMipmaps,premultiplyAlpha:this.premultiplyAlpha,unpackAlignment:this.unpackAlignment};return Object.keys(this.userData).length>0&&(i.userData=this.userData),t||(e.textures[this.uuid]=i),i}dispose(){this.dispatchEvent({type:"dispose"})}transformUv(e){if(this.mapping!==xc)return e;if(e.applyMatrix3(this.matrix),e.x<0||e.x>1)switch(this.wrapS){case Ga:e.x=e.x-Math.floor(e.x);break;case $n:e.x=e.x<0?0:1;break;case Wa:Math.abs(Math.floor(e.x)%2)===1?e.x=Math.ceil(e.x)-e.x:e.x=e.x-Math.floor(e.x);break}if(e.y<0||e.y>1)switch(this.wrapT){case Ga:e.y=e.y-Math.floor(e.y);break;case $n:e.y=e.y<0?0:1;break;case Wa:Math.abs(Math.floor(e.y)%2)===1?e.y=Math.ceil(e.y)-e.y:e.y=e.y-Math.floor(e.y);break}return this.flipY&&(e.y=1-e.y),e}set needsUpdate(e){e===!0&&(this.version++,this.source.needsUpdate=!0)}set needsPMREMUpdate(e){e===!0&&this.pmremVersion++}}Ct.DEFAULT_IMAGE=null;Ct.DEFAULT_MAPPING=xc;Ct.DEFAULT_ANISOTROPY=1;class dt{constructor(e=0,t=0,i=0,r=1){dt.prototype.isVector4=!0,this.x=e,this.y=t,this.z=i,this.w=r}get width(){return this.z}set width(e){this.z=e}get height(){return this.w}set height(e){this.w=e}set(e,t,i,r){return this.x=e,this.y=t,this.z=i,this.w=r,this}setScalar(e){return this.x=e,this.y=e,this.z=e,this.w=e,this}setX(e){return this.x=e,this}setY(e){return this.y=e,this}setZ(e){return this.z=e,this}setW(e){return this.w=e,this}setComponent(e,t){switch(e){case 0:this.x=t;break;case 1:this.y=t;break;case 2:this.z=t;break;case 3:this.w=t;break;default:throw new Error("index is out of range: "+e)}return this}getComponent(e){switch(e){case 0:return this.x;case 1:return this.y;case 2:return this.z;case 3:return this.w;default:throw new Error("index is out of range: "+e)}}clone(){return new this.constructor(this.x,this.y,this.z,this.w)}copy(e){return this.x=e.x,this.y=e.y,this.z=e.z,this.w=e.w!==void 0?e.w:1,this}add(e){return this.x+=e.x,this.y+=e.y,this.z+=e.z,this.w+=e.w,this}addScalar(e){return this.x+=e,this.y+=e,this.z+=e,this.w+=e,this}addVectors(e,t){return this.x=e.x+t.x,this.y=e.y+t.y,this.z=e.z+t.z,this.w=e.w+t.w,this}addScaledVector(e,t){return this.x+=e.x*t,this.y+=e.y*t,this.z+=e.z*t,this.w+=e.w*t,this}sub(e){return this.x-=e.x,this.y-=e.y,this.z-=e.z,this.w-=e.w,this}subScalar(e){return this.x-=e,this.y-=e,this.z-=e,this.w-=e,this}subVectors(e,t){return this.x=e.x-t.x,this.y=e.y-t.y,this.z=e.z-t.z,this.w=e.w-t.w,this}multiply(e){return this.x*=e.x,this.y*=e.y,this.z*=e.z,this.w*=e.w,this}multiplyScalar(e){return this.x*=e,this.y*=e,this.z*=e,this.w*=e,this}applyMatrix4(e){const t=this.x,i=this.y,r=this.z,a=this.w,s=e.elements;return this.x=s[0]*t+s[4]*i+s[8]*r+s[12]*a,this.y=s[1]*t+s[5]*i+s[9]*r+s[13]*a,this.z=s[2]*t+s[6]*i+s[10]*r+s[14]*a,this.w=s[3]*t+s[7]*i+s[11]*r+s[15]*a,this}divide(e){return this.x/=e.x,this.y/=e.y,this.z/=e.z,this.w/=e.w,this}divideScalar(e){return this.multiplyScalar(1/e)}setAxisAngleFromQuaternion(e){this.w=2*Math.acos(e.w);const t=Math.sqrt(1-e.w*e.w);return t<1e-4?(this.x=1,this.y=0,this.z=0):(this.x=e.x/t,this.y=e.y/t,this.z=e.z/t),this}setAxisAngleFromRotationMatrix(e){let t,i,r,a;const c=e.elements,l=c[0],d=c[4],h=c[8],f=c[1],m=c[5],g=c[9],_=c[2],p=c[6],u=c[10];if(Math.abs(d-f)<.01&&Math.abs(h-_)<.01&&Math.abs(g-p)<.01){if(Math.abs(d+f)<.1&&Math.abs(h+_)<.1&&Math.abs(g+p)<.1&&Math.abs(l+m+u-3)<.1)return this.set(1,0,0,0),this;t=Math.PI;const S=(l+1)/2,M=(m+1)/2,w=(u+1)/2,T=(d+f)/4,A=(h+_)/4,L=(g+p)/4;return S>M&&S>w?S<.01?(i=0,r=.707106781,a=.707106781):(i=Math.sqrt(S),r=T/i,a=A/i):M>w?M<.01?(i=.707106781,r=0,a=.707106781):(r=Math.sqrt(M),i=T/r,a=L/r):w<.01?(i=.707106781,r=.707106781,a=0):(a=Math.sqrt(w),i=A/a,r=L/a),this.set(i,r,a,t),this}let b=Math.sqrt((p-g)*(p-g)+(h-_)*(h-_)+(f-d)*(f-d));return Math.abs(b)<.001&&(b=1),this.x=(p-g)/b,this.y=(h-_)/b,this.z=(f-d)/b,this.w=Math.acos((l+m+u-1)/2),this}setFromMatrixPosition(e){const t=e.elements;return this.x=t[12],this.y=t[13],this.z=t[14],this.w=t[15],this}min(e){return this.x=Math.min(this.x,e.x),this.y=Math.min(this.y,e.y),this.z=Math.min(this.z,e.z),this.w=Math.min(this.w,e.w),this}max(e){return this.x=Math.max(this.x,e.x),this.y=Math.max(this.y,e.y),this.z=Math.max(this.z,e.z),this.w=Math.max(this.w,e.w),this}clamp(e,t){return this.x=Xe(this.x,e.x,t.x),this.y=Xe(this.y,e.y,t.y),this.z=Xe(this.z,e.z,t.z),this.w=Xe(this.w,e.w,t.w),this}clampScalar(e,t){return this.x=Xe(this.x,e,t),this.y=Xe(this.y,e,t),this.z=Xe(this.z,e,t),this.w=Xe(this.w,e,t),this}clampLength(e,t){const i=this.length();return this.divideScalar(i||1).multiplyScalar(Xe(i,e,t))}floor(){return this.x=Math.floor(this.x),this.y=Math.floor(this.y),this.z=Math.floor(this.z),this.w=Math.floor(this.w),this}ceil(){return this.x=Math.ceil(this.x),this.y=Math.ceil(this.y),this.z=Math.ceil(this.z),this.w=Math.ceil(this.w),this}round(){return this.x=Math.round(this.x),this.y=Math.round(this.y),this.z=Math.round(this.z),this.w=Math.round(this.w),this}roundToZero(){return this.x=Math.trunc(this.x),this.y=Math.trunc(this.y),this.z=Math.trunc(this.z),this.w=Math.trunc(this.w),this}negate(){return this.x=-this.x,this.y=-this.y,this.z=-this.z,this.w=-this.w,this}dot(e){return this.x*e.x+this.y*e.y+this.z*e.z+this.w*e.w}lengthSq(){return this.x*this.x+this.y*this.y+this.z*this.z+this.w*this.w}length(){return Math.sqrt(this.x*this.x+this.y*this.y+this.z*this.z+this.w*this.w)}manhattanLength(){return Math.abs(this.x)+Math.abs(this.y)+Math.abs(this.z)+Math.abs(this.w)}normalize(){return this.divideScalar(this.length()||1)}setLength(e){return this.normalize().multiplyScalar(e)}lerp(e,t){return this.x+=(e.x-this.x)*t,this.y+=(e.y-this.y)*t,this.z+=(e.z-this.z)*t,this.w+=(e.w-this.w)*t,this}lerpVectors(e,t,i){return this.x=e.x+(t.x-e.x)*i,this.y=e.y+(t.y-e.y)*i,this.z=e.z+(t.z-e.z)*i,this.w=e.w+(t.w-e.w)*i,this}equals(e){return e.x===this.x&&e.y===this.y&&e.z===this.z&&e.w===this.w}fromArray(e,t=0){return this.x=e[t],this.y=e[t+1],this.z=e[t+2],this.w=e[t+3],this}toArray(e=[],t=0){return e[t]=this.x,e[t+1]=this.y,e[t+2]=this.z,e[t+3]=this.w,e}fromBufferAttribute(e,t){return this.x=e.getX(t),this.y=e.getY(t),this.z=e.getZ(t),this.w=e.getW(t),this}random(){return this.x=Math.random(),this.y=Math.random(),this.z=Math.random(),this.w=Math.random(),this}*[Symbol.iterator](){yield this.x,yield this.y,yield this.z,yield this.w}}class lu extends Di{constructor(e=1,t=1,i={}){super(),this.isRenderTarget=!0,this.width=e,this.height=t,this.depth=1,this.scissor=new dt(0,0,e,t),this.scissorTest=!1,this.viewport=new dt(0,0,e,t);const r={width:e,height:t,depth:1};i=Object.assign({generateMipmaps:!1,internalFormat:null,minFilter:tn,depthBuffer:!0,stencilBuffer:!1,resolveDepthBuffer:!0,resolveStencilBuffer:!0,depthTexture:null,samples:0,count:1},i);const a=new Ct(r,i.mapping,i.wrapS,i.wrapT,i.magFilter,i.minFilter,i.format,i.type,i.anisotropy,i.colorSpace);a.flipY=!1,a.generateMipmaps=i.generateMipmaps,a.internalFormat=i.internalFormat,this.textures=[];const s=i.count;for(let o=0;o<s;o++)this.textures[o]=a.clone(),this.textures[o].isRenderTargetTexture=!0,this.textures[o].renderTarget=this;this.depthBuffer=i.depthBuffer,this.stencilBuffer=i.stencilBuffer,this.resolveDepthBuffer=i.resolveDepthBuffer,this.resolveStencilBuffer=i.resolveStencilBuffer,this._depthTexture=null,this.depthTexture=i.depthTexture,this.samples=i.samples}get texture(){return this.textures[0]}set texture(e){this.textures[0]=e}set depthTexture(e){this._depthTexture!==null&&(this._depthTexture.renderTarget=null),e!==null&&(e.renderTarget=this),this._depthTexture=e}get depthTexture(){return this._depthTexture}setSize(e,t,i=1){if(this.width!==e||this.height!==t||this.depth!==i){this.width=e,this.height=t,this.depth=i;for(let r=0,a=this.textures.length;r<a;r++)this.textures[r].image.width=e,this.textures[r].image.height=t,this.textures[r].image.depth=i;this.dispose()}this.viewport.set(0,0,e,t),this.scissor.set(0,0,e,t)}clone(){return new this.constructor().copy(this)}copy(e){this.width=e.width,this.height=e.height,this.depth=e.depth,this.scissor.copy(e.scissor),this.scissorTest=e.scissorTest,this.viewport.copy(e.viewport),this.textures.length=0;for(let t=0,i=e.textures.length;t<i;t++){this.textures[t]=e.textures[t].clone(),this.textures[t].isRenderTargetTexture=!0,this.textures[t].renderTarget=this;const r=Object.assign({},e.textures[t].image);this.textures[t].source=new zs(r)}return this.depthBuffer=e.depthBuffer,this.stencilBuffer=e.stencilBuffer,this.resolveDepthBuffer=e.resolveDepthBuffer,this.resolveStencilBuffer=e.resolveStencilBuffer,e.depthTexture!==null&&(this.depthTexture=e.depthTexture.clone()),this.samples=e.samples,this}dispose(){this.dispatchEvent({type:"dispose"})}}class ei extends lu{constructor(e=1,t=1,i={}){super(e,t,i),this.isWebGLRenderTarget=!0}}class Ic extends Ct{constructor(e=null,t=1,i=1,r=1){super(null),this.isDataArrayTexture=!0,this.image={data:e,width:t,height:i,depth:r},this.magFilter=Jt,this.minFilter=Jt,this.wrapR=$n,this.generateMipmaps=!1,this.flipY=!1,this.unpackAlignment=1,this.layerUpdates=new Set}addLayerUpdate(e){this.layerUpdates.add(e)}clearLayerUpdates(){this.layerUpdates.clear()}}class uu extends Ct{constructor(e=null,t=1,i=1,r=1){super(null),this.isData3DTexture=!0,this.image={data:e,width:t,height:i,depth:r},this.magFilter=Jt,this.minFilter=Jt,this.wrapR=$n,this.generateMipmaps=!1,this.flipY=!1,this.unpackAlignment=1}}class Li{constructor(e=0,t=0,i=0,r=1){this.isQuaternion=!0,this._x=e,this._y=t,this._z=i,this._w=r}static slerpFlat(e,t,i,r,a,s,o){let c=i[r+0],l=i[r+1],d=i[r+2],h=i[r+3];const f=a[s+0],m=a[s+1],g=a[s+2],_=a[s+3];if(o===0){e[t+0]=c,e[t+1]=l,e[t+2]=d,e[t+3]=h;return}if(o===1){e[t+0]=f,e[t+1]=m,e[t+2]=g,e[t+3]=_;return}if(h!==_||c!==f||l!==m||d!==g){let p=1-o;const u=c*f+l*m+d*g+h*_,b=u>=0?1:-1,S=1-u*u;if(S>Number.EPSILON){const w=Math.sqrt(S),T=Math.atan2(w,u*b);p=Math.sin(p*T)/w,o=Math.sin(o*T)/w}const M=o*b;if(c=c*p+f*M,l=l*p+m*M,d=d*p+g*M,h=h*p+_*M,p===1-o){const w=1/Math.sqrt(c*c+l*l+d*d+h*h);c*=w,l*=w,d*=w,h*=w}}e[t]=c,e[t+1]=l,e[t+2]=d,e[t+3]=h}static multiplyQuaternionsFlat(e,t,i,r,a,s){const o=i[r],c=i[r+1],l=i[r+2],d=i[r+3],h=a[s],f=a[s+1],m=a[s+2],g=a[s+3];return e[t]=o*g+d*h+c*m-l*f,e[t+1]=c*g+d*f+l*h-o*m,e[t+2]=l*g+d*m+o*f-c*h,e[t+3]=d*g-o*h-c*f-l*m,e}get x(){return this._x}set x(e){this._x=e,this._onChangeCallback()}get y(){return this._y}set y(e){this._y=e,this._onChangeCallback()}get z(){return this._z}set z(e){this._z=e,this._onChangeCallback()}get w(){return this._w}set w(e){this._w=e,this._onChangeCallback()}set(e,t,i,r){return this._x=e,this._y=t,this._z=i,this._w=r,this._onChangeCallback(),this}clone(){return new this.constructor(this._x,this._y,this._z,this._w)}copy(e){return this._x=e.x,this._y=e.y,this._z=e.z,this._w=e.w,this._onChangeCallback(),this}setFromEuler(e,t=!0){const i=e._x,r=e._y,a=e._z,s=e._order,o=Math.cos,c=Math.sin,l=o(i/2),d=o(r/2),h=o(a/2),f=c(i/2),m=c(r/2),g=c(a/2);switch(s){case"XYZ":this._x=f*d*h+l*m*g,this._y=l*m*h-f*d*g,this._z=l*d*g+f*m*h,this._w=l*d*h-f*m*g;break;case"YXZ":this._x=f*d*h+l*m*g,this._y=l*m*h-f*d*g,this._z=l*d*g-f*m*h,this._w=l*d*h+f*m*g;break;case"ZXY":this._x=f*d*h-l*m*g,this._y=l*m*h+f*d*g,this._z=l*d*g+f*m*h,this._w=l*d*h-f*m*g;break;case"ZYX":this._x=f*d*h-l*m*g,this._y=l*m*h+f*d*g,this._z=l*d*g-f*m*h,this._w=l*d*h+f*m*g;break;case"YZX":this._x=f*d*h+l*m*g,this._y=l*m*h+f*d*g,this._z=l*d*g-f*m*h,this._w=l*d*h-f*m*g;break;case"XZY":this._x=f*d*h-l*m*g,this._y=l*m*h-f*d*g,this._z=l*d*g+f*m*h,this._w=l*d*h+f*m*g;break;default:console.warn("THREE.Quaternion: .setFromEuler() encountered an unknown order: "+s)}return t===!0&&this._onChangeCallback(),this}setFromAxisAngle(e,t){const i=t/2,r=Math.sin(i);return this._x=e.x*r,this._y=e.y*r,this._z=e.z*r,this._w=Math.cos(i),this._onChangeCallback(),this}setFromRotationMatrix(e){const t=e.elements,i=t[0],r=t[4],a=t[8],s=t[1],o=t[5],c=t[9],l=t[2],d=t[6],h=t[10],f=i+o+h;if(f>0){const m=.5/Math.sqrt(f+1);this._w=.25/m,this._x=(d-c)*m,this._y=(a-l)*m,this._z=(s-r)*m}else if(i>o&&i>h){const m=2*Math.sqrt(1+i-o-h);this._w=(d-c)/m,this._x=.25*m,this._y=(r+s)/m,this._z=(a+l)/m}else if(o>h){const m=2*Math.sqrt(1+o-i-h);this._w=(a-l)/m,this._x=(r+s)/m,this._y=.25*m,this._z=(c+d)/m}else{const m=2*Math.sqrt(1+h-i-o);this._w=(s-r)/m,this._x=(a+l)/m,this._y=(c+d)/m,this._z=.25*m}return this._onChangeCallback(),this}setFromUnitVectors(e,t){let i=e.dot(t)+1;return i<Number.EPSILON?(i=0,Math.abs(e.x)>Math.abs(e.z)?(this._x=-e.y,this._y=e.x,this._z=0,this._w=i):(this._x=0,this._y=-e.z,this._z=e.y,this._w=i)):(this._x=e.y*t.z-e.z*t.y,this._y=e.z*t.x-e.x*t.z,this._z=e.x*t.y-e.y*t.x,this._w=i),this.normalize()}angleTo(e){return 2*Math.acos(Math.abs(Xe(this.dot(e),-1,1)))}rotateTowards(e,t){const i=this.angleTo(e);if(i===0)return this;const r=Math.min(1,t/i);return this.slerp(e,r),this}identity(){return this.set(0,0,0,1)}invert(){return this.conjugate()}conjugate(){return this._x*=-1,this._y*=-1,this._z*=-1,this._onChangeCallback(),this}dot(e){return this._x*e._x+this._y*e._y+this._z*e._z+this._w*e._w}lengthSq(){return this._x*this._x+this._y*this._y+this._z*this._z+this._w*this._w}length(){return Math.sqrt(this._x*this._x+this._y*this._y+this._z*this._z+this._w*this._w)}normalize(){let e=this.length();return e===0?(this._x=0,this._y=0,this._z=0,this._w=1):(e=1/e,this._x=this._x*e,this._y=this._y*e,this._z=this._z*e,this._w=this._w*e),this._onChangeCallback(),this}multiply(e){return this.multiplyQuaternions(this,e)}premultiply(e){return this.multiplyQuaternions(e,this)}multiplyQuaternions(e,t){const i=e._x,r=e._y,a=e._z,s=e._w,o=t._x,c=t._y,l=t._z,d=t._w;return this._x=i*d+s*o+r*l-a*c,this._y=r*d+s*c+a*o-i*l,this._z=a*d+s*l+i*c-r*o,this._w=s*d-i*o-r*c-a*l,this._onChangeCallback(),this}slerp(e,t){if(t===0)return this;if(t===1)return this.copy(e);const i=this._x,r=this._y,a=this._z,s=this._w;let o=s*e._w+i*e._x+r*e._y+a*e._z;if(o<0?(this._w=-e._w,this._x=-e._x,this._y=-e._y,this._z=-e._z,o=-o):this.copy(e),o>=1)return this._w=s,this._x=i,this._y=r,this._z=a,this;const c=1-o*o;if(c<=Number.EPSILON){const m=1-t;return this._w=m*s+t*this._w,this._x=m*i+t*this._x,this._y=m*r+t*this._y,this._z=m*a+t*this._z,this.normalize(),this}const l=Math.sqrt(c),d=Math.atan2(l,o),h=Math.sin((1-t)*d)/l,f=Math.sin(t*d)/l;return this._w=s*h+this._w*f,this._x=i*h+this._x*f,this._y=r*h+this._y*f,this._z=a*h+this._z*f,this._onChangeCallback(),this}slerpQuaternions(e,t,i){return this.copy(e).slerp(t,i)}random(){const e=2*Math.PI*Math.random(),t=2*Math.PI*Math.random(),i=Math.random(),r=Math.sqrt(1-i),a=Math.sqrt(i);return this.set(r*Math.sin(e),r*Math.cos(e),a*Math.sin(t),a*Math.cos(t))}equals(e){return e._x===this._x&&e._y===this._y&&e._z===this._z&&e._w===this._w}fromArray(e,t=0){return this._x=e[t],this._y=e[t+1],this._z=e[t+2],this._w=e[t+3],this._onChangeCallback(),this}toArray(e=[],t=0){return e[t]=this._x,e[t+1]=this._y,e[t+2]=this._z,e[t+3]=this._w,e}fromBufferAttribute(e,t){return this._x=e.getX(t),this._y=e.getY(t),this._z=e.getZ(t),this._w=e.getW(t),this._onChangeCallback(),this}toJSON(){return this.toArray()}_onChange(e){return this._onChangeCallback=e,this}_onChangeCallback(){}*[Symbol.iterator](){yield this._x,yield this._y,yield this._z,yield this._w}}class F{constructor(e=0,t=0,i=0){F.prototype.isVector3=!0,this.x=e,this.y=t,this.z=i}set(e,t,i){return i===void 0&&(i=this.z),this.x=e,this.y=t,this.z=i,this}setScalar(e){return this.x=e,this.y=e,this.z=e,this}setX(e){return this.x=e,this}setY(e){return this.y=e,this}setZ(e){return this.z=e,this}setComponent(e,t){switch(e){case 0:this.x=t;break;case 1:this.y=t;break;case 2:this.z=t;break;default:throw new Error("index is out of range: "+e)}return this}getComponent(e){switch(e){case 0:return this.x;case 1:return this.y;case 2:return this.z;default:throw new Error("index is out of range: "+e)}}clone(){return new this.constructor(this.x,this.y,this.z)}copy(e){return this.x=e.x,this.y=e.y,this.z=e.z,this}add(e){return this.x+=e.x,this.y+=e.y,this.z+=e.z,this}addScalar(e){return this.x+=e,this.y+=e,this.z+=e,this}addVectors(e,t){return this.x=e.x+t.x,this.y=e.y+t.y,this.z=e.z+t.z,this}addScaledVector(e,t){return this.x+=e.x*t,this.y+=e.y*t,this.z+=e.z*t,this}sub(e){return this.x-=e.x,this.y-=e.y,this.z-=e.z,this}subScalar(e){return this.x-=e,this.y-=e,this.z-=e,this}subVectors(e,t){return this.x=e.x-t.x,this.y=e.y-t.y,this.z=e.z-t.z,this}multiply(e){return this.x*=e.x,this.y*=e.y,this.z*=e.z,this}multiplyScalar(e){return this.x*=e,this.y*=e,this.z*=e,this}multiplyVectors(e,t){return this.x=e.x*t.x,this.y=e.y*t.y,this.z=e.z*t.z,this}applyEuler(e){return this.applyQuaternion(ho.setFromEuler(e))}applyAxisAngle(e,t){return this.applyQuaternion(ho.setFromAxisAngle(e,t))}applyMatrix3(e){const t=this.x,i=this.y,r=this.z,a=e.elements;return this.x=a[0]*t+a[3]*i+a[6]*r,this.y=a[1]*t+a[4]*i+a[7]*r,this.z=a[2]*t+a[5]*i+a[8]*r,this}applyNormalMatrix(e){return this.applyMatrix3(e).normalize()}applyMatrix4(e){const t=this.x,i=this.y,r=this.z,a=e.elements,s=1/(a[3]*t+a[7]*i+a[11]*r+a[15]);return this.x=(a[0]*t+a[4]*i+a[8]*r+a[12])*s,this.y=(a[1]*t+a[5]*i+a[9]*r+a[13])*s,this.z=(a[2]*t+a[6]*i+a[10]*r+a[14])*s,this}applyQuaternion(e){const t=this.x,i=this.y,r=this.z,a=e.x,s=e.y,o=e.z,c=e.w,l=2*(s*r-o*i),d=2*(o*t-a*r),h=2*(a*i-s*t);return this.x=t+c*l+s*h-o*d,this.y=i+c*d+o*l-a*h,this.z=r+c*h+a*d-s*l,this}project(e){return this.applyMatrix4(e.matrixWorldInverse).applyMatrix4(e.projectionMatrix)}unproject(e){return this.applyMatrix4(e.projectionMatrixInverse).applyMatrix4(e.matrixWorld)}transformDirection(e){const t=this.x,i=this.y,r=this.z,a=e.elements;return this.x=a[0]*t+a[4]*i+a[8]*r,this.y=a[1]*t+a[5]*i+a[9]*r,this.z=a[2]*t+a[6]*i+a[10]*r,this.normalize()}divide(e){return this.x/=e.x,this.y/=e.y,this.z/=e.z,this}divideScalar(e){return this.multiplyScalar(1/e)}min(e){return this.x=Math.min(this.x,e.x),this.y=Math.min(this.y,e.y),this.z=Math.min(this.z,e.z),this}max(e){return this.x=Math.max(this.x,e.x),this.y=Math.max(this.y,e.y),this.z=Math.max(this.z,e.z),this}clamp(e,t){return this.x=Xe(this.x,e.x,t.x),this.y=Xe(this.y,e.y,t.y),this.z=Xe(this.z,e.z,t.z),this}clampScalar(e,t){return this.x=Xe(this.x,e,t),this.y=Xe(this.y,e,t),this.z=Xe(this.z,e,t),this}clampLength(e,t){const i=this.length();return this.divideScalar(i||1).multiplyScalar(Xe(i,e,t))}floor(){return this.x=Math.floor(this.x),this.y=Math.floor(this.y),this.z=Math.floor(this.z),this}ceil(){return this.x=Math.ceil(this.x),this.y=Math.ceil(this.y),this.z=Math.ceil(this.z),this}round(){return this.x=Math.round(this.x),this.y=Math.round(this.y),this.z=Math.round(this.z),this}roundToZero(){return this.x=Math.trunc(this.x),this.y=Math.trunc(this.y),this.z=Math.trunc(this.z),this}negate(){return this.x=-this.x,this.y=-this.y,this.z=-this.z,this}dot(e){return this.x*e.x+this.y*e.y+this.z*e.z}lengthSq(){return this.x*this.x+this.y*this.y+this.z*this.z}length(){return Math.sqrt(this.x*this.x+this.y*this.y+this.z*this.z)}manhattanLength(){return Math.abs(this.x)+Math.abs(this.y)+Math.abs(this.z)}normalize(){return this.divideScalar(this.length()||1)}setLength(e){return this.normalize().multiplyScalar(e)}lerp(e,t){return this.x+=(e.x-this.x)*t,this.y+=(e.y-this.y)*t,this.z+=(e.z-this.z)*t,this}lerpVectors(e,t,i){return this.x=e.x+(t.x-e.x)*i,this.y=e.y+(t.y-e.y)*i,this.z=e.z+(t.z-e.z)*i,this}cross(e){return this.crossVectors(this,e)}crossVectors(e,t){const i=e.x,r=e.y,a=e.z,s=t.x,o=t.y,c=t.z;return this.x=r*c-a*o,this.y=a*s-i*c,this.z=i*o-r*s,this}projectOnVector(e){const t=e.lengthSq();if(t===0)return this.set(0,0,0);const i=e.dot(this)/t;return this.copy(e).multiplyScalar(i)}projectOnPlane(e){return Qr.copy(this).projectOnVector(e),this.sub(Qr)}reflect(e){return this.sub(Qr.copy(e).multiplyScalar(2*this.dot(e)))}angleTo(e){const t=Math.sqrt(this.lengthSq()*e.lengthSq());if(t===0)return Math.PI/2;const i=this.dot(e)/t;return Math.acos(Xe(i,-1,1))}distanceTo(e){return Math.sqrt(this.distanceToSquared(e))}distanceToSquared(e){const t=this.x-e.x,i=this.y-e.y,r=this.z-e.z;return t*t+i*i+r*r}manhattanDistanceTo(e){return Math.abs(this.x-e.x)+Math.abs(this.y-e.y)+Math.abs(this.z-e.z)}setFromSpherical(e){return this.setFromSphericalCoords(e.radius,e.phi,e.theta)}setFromSphericalCoords(e,t,i){const r=Math.sin(t)*e;return this.x=r*Math.sin(i),this.y=Math.cos(t)*e,this.z=r*Math.cos(i),this}setFromCylindrical(e){return this.setFromCylindricalCoords(e.radius,e.theta,e.y)}setFromCylindricalCoords(e,t,i){return this.x=e*Math.sin(t),this.y=i,this.z=e*Math.cos(t),this}setFromMatrixPosition(e){const t=e.elements;return this.x=t[12],this.y=t[13],this.z=t[14],this}setFromMatrixScale(e){const t=this.setFromMatrixColumn(e,0).length(),i=this.setFromMatrixColumn(e,1).length(),r=this.setFromMatrixColumn(e,2).length();return this.x=t,this.y=i,this.z=r,this}setFromMatrixColumn(e,t){return this.fromArray(e.elements,t*4)}setFromMatrix3Column(e,t){return this.fromArray(e.elements,t*3)}setFromEuler(e){return this.x=e._x,this.y=e._y,this.z=e._z,this}setFromColor(e){return this.x=e.r,this.y=e.g,this.z=e.b,this}equals(e){return e.x===this.x&&e.y===this.y&&e.z===this.z}fromArray(e,t=0){return this.x=e[t],this.y=e[t+1],this.z=e[t+2],this}toArray(e=[],t=0){return e[t]=this.x,e[t+1]=this.y,e[t+2]=this.z,e}fromBufferAttribute(e,t){return this.x=e.getX(t),this.y=e.getY(t),this.z=e.getZ(t),this}random(){return this.x=Math.random(),this.y=Math.random(),this.z=Math.random(),this}randomDirection(){const e=Math.random()*Math.PI*2,t=Math.random()*2-1,i=Math.sqrt(1-t*t);return this.x=i*Math.cos(e),this.y=t,this.z=i*Math.sin(e),this}*[Symbol.iterator](){yield this.x,yield this.y,yield this.z}}const Qr=new F,ho=new Li;class Zi{constructor(e=new F(1/0,1/0,1/0),t=new F(-1/0,-1/0,-1/0)){this.isBox3=!0,this.min=e,this.max=t}set(e,t){return this.min.copy(e),this.max.copy(t),this}setFromArray(e){this.makeEmpty();for(let t=0,i=e.length;t<i;t+=3)this.expandByPoint(Kt.fromArray(e,t));return this}setFromBufferAttribute(e){this.makeEmpty();for(let t=0,i=e.count;t<i;t++)this.expandByPoint(Kt.fromBufferAttribute(e,t));return this}setFromPoints(e){this.makeEmpty();for(let t=0,i=e.length;t<i;t++)this.expandByPoint(e[t]);return this}setFromCenterAndSize(e,t){const i=Kt.copy(t).multiplyScalar(.5);return this.min.copy(e).sub(i),this.max.copy(e).add(i),this}setFromObject(e,t=!1){return this.makeEmpty(),this.expandByObject(e,t)}clone(){return new this.constructor().copy(this)}copy(e){return this.min.copy(e.min),this.max.copy(e.max),this}makeEmpty(){return this.min.x=this.min.y=this.min.z=1/0,this.max.x=this.max.y=this.max.z=-1/0,this}isEmpty(){return this.max.x<this.min.x||this.max.y<this.min.y||this.max.z<this.min.z}getCenter(e){return this.isEmpty()?e.set(0,0,0):e.addVectors(this.min,this.max).multiplyScalar(.5)}getSize(e){return this.isEmpty()?e.set(0,0,0):e.subVectors(this.max,this.min)}expandByPoint(e){return this.min.min(e),this.max.max(e),this}expandByVector(e){return this.min.sub(e),this.max.add(e),this}expandByScalar(e){return this.min.addScalar(-e),this.max.addScalar(e),this}expandByObject(e,t=!1){e.updateWorldMatrix(!1,!1);const i=e.geometry;if(i!==void 0){const a=i.getAttribute("position");if(t===!0&&a!==void 0&&e.isInstancedMesh!==!0)for(let s=0,o=a.count;s<o;s++)e.isMesh===!0?e.getVertexPosition(s,Kt):Kt.fromBufferAttribute(a,s),Kt.applyMatrix4(e.matrixWorld),this.expandByPoint(Kt);else e.boundingBox!==void 0?(e.boundingBox===null&&e.computeBoundingBox(),nr.copy(e.boundingBox)):(i.boundingBox===null&&i.computeBoundingBox(),nr.copy(i.boundingBox)),nr.applyMatrix4(e.matrixWorld),this.union(nr)}const r=e.children;for(let a=0,s=r.length;a<s;a++)this.expandByObject(r[a],t);return this}containsPoint(e){return e.x>=this.min.x&&e.x<=this.max.x&&e.y>=this.min.y&&e.y<=this.max.y&&e.z>=this.min.z&&e.z<=this.max.z}containsBox(e){return this.min.x<=e.min.x&&e.max.x<=this.max.x&&this.min.y<=e.min.y&&e.max.y<=this.max.y&&this.min.z<=e.min.z&&e.max.z<=this.max.z}getParameter(e,t){return t.set((e.x-this.min.x)/(this.max.x-this.min.x),(e.y-this.min.y)/(this.max.y-this.min.y),(e.z-this.min.z)/(this.max.z-this.min.z))}intersectsBox(e){return e.max.x>=this.min.x&&e.min.x<=this.max.x&&e.max.y>=this.min.y&&e.min.y<=this.max.y&&e.max.z>=this.min.z&&e.min.z<=this.max.z}intersectsSphere(e){return this.clampPoint(e.center,Kt),Kt.distanceToSquared(e.center)<=e.radius*e.radius}intersectsPlane(e){let t,i;return e.normal.x>0?(t=e.normal.x*this.min.x,i=e.normal.x*this.max.x):(t=e.normal.x*this.max.x,i=e.normal.x*this.min.x),e.normal.y>0?(t+=e.normal.y*this.min.y,i+=e.normal.y*this.max.y):(t+=e.normal.y*this.max.y,i+=e.normal.y*this.min.y),e.normal.z>0?(t+=e.normal.z*this.min.z,i+=e.normal.z*this.max.z):(t+=e.normal.z*this.max.z,i+=e.normal.z*this.min.z),t<=-e.constant&&i>=-e.constant}intersectsTriangle(e){if(this.isEmpty())return!1;this.getCenter(Oi),ir.subVectors(this.max,Oi),ri.subVectors(e.a,Oi),ai.subVectors(e.b,Oi),si.subVectors(e.c,Oi),Mn.subVectors(ai,ri),Sn.subVectors(si,ai),Nn.subVectors(ri,si);let t=[0,-Mn.z,Mn.y,0,-Sn.z,Sn.y,0,-Nn.z,Nn.y,Mn.z,0,-Mn.x,Sn.z,0,-Sn.x,Nn.z,0,-Nn.x,-Mn.y,Mn.x,0,-Sn.y,Sn.x,0,-Nn.y,Nn.x,0];return!ea(t,ri,ai,si,ir)||(t=[1,0,0,0,1,0,0,0,1],!ea(t,ri,ai,si,ir))?!1:(rr.crossVectors(Mn,Sn),t=[rr.x,rr.y,rr.z],ea(t,ri,ai,si,ir))}clampPoint(e,t){return t.copy(e).clamp(this.min,this.max)}distanceToPoint(e){return this.clampPoint(e,Kt).distanceTo(e)}getBoundingSphere(e){return this.isEmpty()?e.makeEmpty():(this.getCenter(e.center),e.radius=this.getSize(Kt).length()*.5),e}intersect(e){return this.min.max(e.min),this.max.min(e.max),this.isEmpty()&&this.makeEmpty(),this}union(e){return this.min.min(e.min),this.max.max(e.max),this}applyMatrix4(e){return this.isEmpty()?this:(an[0].set(this.min.x,this.min.y,this.min.z).applyMatrix4(e),an[1].set(this.min.x,this.min.y,this.max.z).applyMatrix4(e),an[2].set(this.min.x,this.max.y,this.min.z).applyMatrix4(e),an[3].set(this.min.x,this.max.y,this.max.z).applyMatrix4(e),an[4].set(this.max.x,this.min.y,this.min.z).applyMatrix4(e),an[5].set(this.max.x,this.min.y,this.max.z).applyMatrix4(e),an[6].set(this.max.x,this.max.y,this.min.z).applyMatrix4(e),an[7].set(this.max.x,this.max.y,this.max.z).applyMatrix4(e),this.setFromPoints(an),this)}translate(e){return this.min.add(e),this.max.add(e),this}equals(e){return e.min.equals(this.min)&&e.max.equals(this.max)}}const an=[new F,new F,new F,new F,new F,new F,new F,new F],Kt=new F,nr=new Zi,ri=new F,ai=new F,si=new F,Mn=new F,Sn=new F,Nn=new F,Oi=new F,ir=new F,rr=new F,kn=new F;function ea(n,e,t,i,r){for(let a=0,s=n.length-3;a<=s;a+=3){kn.fromArray(n,a);const o=r.x*Math.abs(kn.x)+r.y*Math.abs(kn.y)+r.z*Math.abs(kn.z),c=e.dot(kn),l=t.dot(kn),d=i.dot(kn);if(Math.max(-Math.max(c,l,d),Math.min(c,l,d))>o)return!1}return!0}const du=new Zi,Bi=new F,ta=new F;class Hr{constructor(e=new F,t=-1){this.isSphere=!0,this.center=e,this.radius=t}set(e,t){return this.center.copy(e),this.radius=t,this}setFromPoints(e,t){const i=this.center;t!==void 0?i.copy(t):du.setFromPoints(e).getCenter(i);let r=0;for(let a=0,s=e.length;a<s;a++)r=Math.max(r,i.distanceToSquared(e[a]));return this.radius=Math.sqrt(r),this}copy(e){return this.center.copy(e.center),this.radius=e.radius,this}isEmpty(){return this.radius<0}makeEmpty(){return this.center.set(0,0,0),this.radius=-1,this}containsPoint(e){return e.distanceToSquared(this.center)<=this.radius*this.radius}distanceToPoint(e){return e.distanceTo(this.center)-this.radius}intersectsSphere(e){const t=this.radius+e.radius;return e.center.distanceToSquared(this.center)<=t*t}intersectsBox(e){return e.intersectsSphere(this)}intersectsPlane(e){return Math.abs(e.distanceToPoint(this.center))<=this.radius}clampPoint(e,t){const i=this.center.distanceToSquared(e);return t.copy(e),i>this.radius*this.radius&&(t.sub(this.center).normalize(),t.multiplyScalar(this.radius).add(this.center)),t}getBoundingBox(e){return this.isEmpty()?(e.makeEmpty(),e):(e.set(this.center,this.center),e.expandByScalar(this.radius),e)}applyMatrix4(e){return this.center.applyMatrix4(e),this.radius=this.radius*e.getMaxScaleOnAxis(),this}translate(e){return this.center.add(e),this}expandByPoint(e){if(this.isEmpty())return this.center.copy(e),this.radius=0,this;Bi.subVectors(e,this.center);const t=Bi.lengthSq();if(t>this.radius*this.radius){const i=Math.sqrt(t),r=(i-this.radius)*.5;this.center.addScaledVector(Bi,r/i),this.radius+=r}return this}union(e){return e.isEmpty()?this:this.isEmpty()?(this.copy(e),this):(this.center.equals(e.center)===!0?this.radius=Math.max(this.radius,e.radius):(ta.subVectors(e.center,this.center).setLength(e.radius),this.expandByPoint(Bi.copy(e.center).add(ta)),this.expandByPoint(Bi.copy(e.center).sub(ta))),this)}equals(e){return e.center.equals(this.center)&&e.radius===this.radius}clone(){return new this.constructor().copy(this)}}const sn=new F,na=new F,ar=new F,En=new F,ia=new F,sr=new F,ra=new F;class Ns{constructor(e=new F,t=new F(0,0,-1)){this.origin=e,this.direction=t}set(e,t){return this.origin.copy(e),this.direction.copy(t),this}copy(e){return this.origin.copy(e.origin),this.direction.copy(e.direction),this}at(e,t){return t.copy(this.origin).addScaledVector(this.direction,e)}lookAt(e){return this.direction.copy(e).sub(this.origin).normalize(),this}recast(e){return this.origin.copy(this.at(e,sn)),this}closestPointToPoint(e,t){t.subVectors(e,this.origin);const i=t.dot(this.direction);return i<0?t.copy(this.origin):t.copy(this.origin).addScaledVector(this.direction,i)}distanceToPoint(e){return Math.sqrt(this.distanceSqToPoint(e))}distanceSqToPoint(e){const t=sn.subVectors(e,this.origin).dot(this.direction);return t<0?this.origin.distanceToSquared(e):(sn.copy(this.origin).addScaledVector(this.direction,t),sn.distanceToSquared(e))}distanceSqToSegment(e,t,i,r){na.copy(e).add(t).multiplyScalar(.5),ar.copy(t).sub(e).normalize(),En.copy(this.origin).sub(na);const a=e.distanceTo(t)*.5,s=-this.direction.dot(ar),o=En.dot(this.direction),c=-En.dot(ar),l=En.lengthSq(),d=Math.abs(1-s*s);let h,f,m,g;if(d>0)if(h=s*c-o,f=s*o-c,g=a*d,h>=0)if(f>=-g)if(f<=g){const _=1/d;h*=_,f*=_,m=h*(h+s*f+2*o)+f*(s*h+f+2*c)+l}else f=a,h=Math.max(0,-(s*f+o)),m=-h*h+f*(f+2*c)+l;else f=-a,h=Math.max(0,-(s*f+o)),m=-h*h+f*(f+2*c)+l;else f<=-g?(h=Math.max(0,-(-s*a+o)),f=h>0?-a:Math.min(Math.max(-a,-c),a),m=-h*h+f*(f+2*c)+l):f<=g?(h=0,f=Math.min(Math.max(-a,-c),a),m=f*(f+2*c)+l):(h=Math.max(0,-(s*a+o)),f=h>0?a:Math.min(Math.max(-a,-c),a),m=-h*h+f*(f+2*c)+l);else f=s>0?-a:a,h=Math.max(0,-(s*f+o)),m=-h*h+f*(f+2*c)+l;return i&&i.copy(this.origin).addScaledVector(this.direction,h),r&&r.copy(na).addScaledVector(ar,f),m}intersectSphere(e,t){sn.subVectors(e.center,this.origin);const i=sn.dot(this.direction),r=sn.dot(sn)-i*i,a=e.radius*e.radius;if(r>a)return null;const s=Math.sqrt(a-r),o=i-s,c=i+s;return c<0?null:o<0?this.at(c,t):this.at(o,t)}intersectsSphere(e){return this.distanceSqToPoint(e.center)<=e.radius*e.radius}distanceToPlane(e){const t=e.normal.dot(this.direction);if(t===0)return e.distanceToPoint(this.origin)===0?0:null;const i=-(this.origin.dot(e.normal)+e.constant)/t;return i>=0?i:null}intersectPlane(e,t){const i=this.distanceToPlane(e);return i===null?null:this.at(i,t)}intersectsPlane(e){const t=e.distanceToPoint(this.origin);return t===0||e.normal.dot(this.direction)*t<0}intersectBox(e,t){let i,r,a,s,o,c;const l=1/this.direction.x,d=1/this.direction.y,h=1/this.direction.z,f=this.origin;return l>=0?(i=(e.min.x-f.x)*l,r=(e.max.x-f.x)*l):(i=(e.max.x-f.x)*l,r=(e.min.x-f.x)*l),d>=0?(a=(e.min.y-f.y)*d,s=(e.max.y-f.y)*d):(a=(e.max.y-f.y)*d,s=(e.min.y-f.y)*d),i>s||a>r||((a>i||isNaN(i))&&(i=a),(s<r||isNaN(r))&&(r=s),h>=0?(o=(e.min.z-f.z)*h,c=(e.max.z-f.z)*h):(o=(e.max.z-f.z)*h,c=(e.min.z-f.z)*h),i>c||o>r)||((o>i||i!==i)&&(i=o),(c<r||r!==r)&&(r=c),r<0)?null:this.at(i>=0?i:r,t)}intersectsBox(e){return this.intersectBox(e,sn)!==null}intersectTriangle(e,t,i,r,a){ia.subVectors(t,e),sr.subVectors(i,e),ra.crossVectors(ia,sr);let s=this.direction.dot(ra),o;if(s>0){if(r)return null;o=1}else if(s<0)o=-1,s=-s;else return null;En.subVectors(this.origin,e);const c=o*this.direction.dot(sr.crossVectors(En,sr));if(c<0)return null;const l=o*this.direction.dot(ia.cross(En));if(l<0||c+l>s)return null;const d=-o*En.dot(ra);return d<0?null:this.at(d/s,a)}applyMatrix4(e){return this.origin.applyMatrix4(e),this.direction.transformDirection(e),this}equals(e){return e.origin.equals(this.origin)&&e.direction.equals(this.direction)}clone(){return new this.constructor().copy(this)}}class ct{constructor(e,t,i,r,a,s,o,c,l,d,h,f,m,g,_,p){ct.prototype.isMatrix4=!0,this.elements=[1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1],e!==void 0&&this.set(e,t,i,r,a,s,o,c,l,d,h,f,m,g,_,p)}set(e,t,i,r,a,s,o,c,l,d,h,f,m,g,_,p){const u=this.elements;return u[0]=e,u[4]=t,u[8]=i,u[12]=r,u[1]=a,u[5]=s,u[9]=o,u[13]=c,u[2]=l,u[6]=d,u[10]=h,u[14]=f,u[3]=m,u[7]=g,u[11]=_,u[15]=p,this}identity(){return this.set(1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1),this}clone(){return new ct().fromArray(this.elements)}copy(e){const t=this.elements,i=e.elements;return t[0]=i[0],t[1]=i[1],t[2]=i[2],t[3]=i[3],t[4]=i[4],t[5]=i[5],t[6]=i[6],t[7]=i[7],t[8]=i[8],t[9]=i[9],t[10]=i[10],t[11]=i[11],t[12]=i[12],t[13]=i[13],t[14]=i[14],t[15]=i[15],this}copyPosition(e){const t=this.elements,i=e.elements;return t[12]=i[12],t[13]=i[13],t[14]=i[14],this}setFromMatrix3(e){const t=e.elements;return this.set(t[0],t[3],t[6],0,t[1],t[4],t[7],0,t[2],t[5],t[8],0,0,0,0,1),this}extractBasis(e,t,i){return e.setFromMatrixColumn(this,0),t.setFromMatrixColumn(this,1),i.setFromMatrixColumn(this,2),this}makeBasis(e,t,i){return this.set(e.x,t.x,i.x,0,e.y,t.y,i.y,0,e.z,t.z,i.z,0,0,0,0,1),this}extractRotation(e){const t=this.elements,i=e.elements,r=1/oi.setFromMatrixColumn(e,0).length(),a=1/oi.setFromMatrixColumn(e,1).length(),s=1/oi.setFromMatrixColumn(e,2).length();return t[0]=i[0]*r,t[1]=i[1]*r,t[2]=i[2]*r,t[3]=0,t[4]=i[4]*a,t[5]=i[5]*a,t[6]=i[6]*a,t[7]=0,t[8]=i[8]*s,t[9]=i[9]*s,t[10]=i[10]*s,t[11]=0,t[12]=0,t[13]=0,t[14]=0,t[15]=1,this}makeRotationFromEuler(e){const t=this.elements,i=e.x,r=e.y,a=e.z,s=Math.cos(i),o=Math.sin(i),c=Math.cos(r),l=Math.sin(r),d=Math.cos(a),h=Math.sin(a);if(e.order==="XYZ"){const f=s*d,m=s*h,g=o*d,_=o*h;t[0]=c*d,t[4]=-c*h,t[8]=l,t[1]=m+g*l,t[5]=f-_*l,t[9]=-o*c,t[2]=_-f*l,t[6]=g+m*l,t[10]=s*c}else if(e.order==="YXZ"){const f=c*d,m=c*h,g=l*d,_=l*h;t[0]=f+_*o,t[4]=g*o-m,t[8]=s*l,t[1]=s*h,t[5]=s*d,t[9]=-o,t[2]=m*o-g,t[6]=_+f*o,t[10]=s*c}else if(e.order==="ZXY"){const f=c*d,m=c*h,g=l*d,_=l*h;t[0]=f-_*o,t[4]=-s*h,t[8]=g+m*o,t[1]=m+g*o,t[5]=s*d,t[9]=_-f*o,t[2]=-s*l,t[6]=o,t[10]=s*c}else if(e.order==="ZYX"){const f=s*d,m=s*h,g=o*d,_=o*h;t[0]=c*d,t[4]=g*l-m,t[8]=f*l+_,t[1]=c*h,t[5]=_*l+f,t[9]=m*l-g,t[2]=-l,t[6]=o*c,t[10]=s*c}else if(e.order==="YZX"){const f=s*c,m=s*l,g=o*c,_=o*l;t[0]=c*d,t[4]=_-f*h,t[8]=g*h+m,t[1]=h,t[5]=s*d,t[9]=-o*d,t[2]=-l*d,t[6]=m*h+g,t[10]=f-_*h}else if(e.order==="XZY"){const f=s*c,m=s*l,g=o*c,_=o*l;t[0]=c*d,t[4]=-h,t[8]=l*d,t[1]=f*h+_,t[5]=s*d,t[9]=m*h-g,t[2]=g*h-m,t[6]=o*d,t[10]=_*h+f}return t[3]=0,t[7]=0,t[11]=0,t[12]=0,t[13]=0,t[14]=0,t[15]=1,this}makeRotationFromQuaternion(e){return this.compose(hu,e,fu)}lookAt(e,t,i){const r=this.elements;return zt.subVectors(e,t),zt.lengthSq()===0&&(zt.z=1),zt.normalize(),bn.crossVectors(i,zt),bn.lengthSq()===0&&(Math.abs(i.z)===1?zt.x+=1e-4:zt.z+=1e-4,zt.normalize(),bn.crossVectors(i,zt)),bn.normalize(),or.crossVectors(zt,bn),r[0]=bn.x,r[4]=or.x,r[8]=zt.x,r[1]=bn.y,r[5]=or.y,r[9]=zt.y,r[2]=bn.z,r[6]=or.z,r[10]=zt.z,this}multiply(e){return this.multiplyMatrices(this,e)}premultiply(e){return this.multiplyMatrices(e,this)}multiplyMatrices(e,t){const i=e.elements,r=t.elements,a=this.elements,s=i[0],o=i[4],c=i[8],l=i[12],d=i[1],h=i[5],f=i[9],m=i[13],g=i[2],_=i[6],p=i[10],u=i[14],b=i[3],S=i[7],M=i[11],w=i[15],T=r[0],A=r[4],L=r[8],x=r[12],v=r[1],R=r[5],U=r[9],C=r[13],D=r[2],k=r[6],N=r[10],O=r[14],z=r[3],H=r[7],q=r[11],J=r[15];return a[0]=s*T+o*v+c*D+l*z,a[4]=s*A+o*R+c*k+l*H,a[8]=s*L+o*U+c*N+l*q,a[12]=s*x+o*C+c*O+l*J,a[1]=d*T+h*v+f*D+m*z,a[5]=d*A+h*R+f*k+m*H,a[9]=d*L+h*U+f*N+m*q,a[13]=d*x+h*C+f*O+m*J,a[2]=g*T+_*v+p*D+u*z,a[6]=g*A+_*R+p*k+u*H,a[10]=g*L+_*U+p*N+u*q,a[14]=g*x+_*C+p*O+u*J,a[3]=b*T+S*v+M*D+w*z,a[7]=b*A+S*R+M*k+w*H,a[11]=b*L+S*U+M*N+w*q,a[15]=b*x+S*C+M*O+w*J,this}multiplyScalar(e){const t=this.elements;return t[0]*=e,t[4]*=e,t[8]*=e,t[12]*=e,t[1]*=e,t[5]*=e,t[9]*=e,t[13]*=e,t[2]*=e,t[6]*=e,t[10]*=e,t[14]*=e,t[3]*=e,t[7]*=e,t[11]*=e,t[15]*=e,this}determinant(){const e=this.elements,t=e[0],i=e[4],r=e[8],a=e[12],s=e[1],o=e[5],c=e[9],l=e[13],d=e[2],h=e[6],f=e[10],m=e[14],g=e[3],_=e[7],p=e[11],u=e[15];return g*(+a*c*h-r*l*h-a*o*f+i*l*f+r*o*m-i*c*m)+_*(+t*c*m-t*l*f+a*s*f-r*s*m+r*l*d-a*c*d)+p*(+t*l*h-t*o*m-a*s*h+i*s*m+a*o*d-i*l*d)+u*(-r*o*d-t*c*h+t*o*f+r*s*h-i*s*f+i*c*d)}transpose(){const e=this.elements;let t;return t=e[1],e[1]=e[4],e[4]=t,t=e[2],e[2]=e[8],e[8]=t,t=e[6],e[6]=e[9],e[9]=t,t=e[3],e[3]=e[12],e[12]=t,t=e[7],e[7]=e[13],e[13]=t,t=e[11],e[11]=e[14],e[14]=t,this}setPosition(e,t,i){const r=this.elements;return e.isVector3?(r[12]=e.x,r[13]=e.y,r[14]=e.z):(r[12]=e,r[13]=t,r[14]=i),this}invert(){const e=this.elements,t=e[0],i=e[1],r=e[2],a=e[3],s=e[4],o=e[5],c=e[6],l=e[7],d=e[8],h=e[9],f=e[10],m=e[11],g=e[12],_=e[13],p=e[14],u=e[15],b=h*p*l-_*f*l+_*c*m-o*p*m-h*c*u+o*f*u,S=g*f*l-d*p*l-g*c*m+s*p*m+d*c*u-s*f*u,M=d*_*l-g*h*l+g*o*m-s*_*m-d*o*u+s*h*u,w=g*h*c-d*_*c-g*o*f+s*_*f+d*o*p-s*h*p,T=t*b+i*S+r*M+a*w;if(T===0)return this.set(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);const A=1/T;return e[0]=b*A,e[1]=(_*f*a-h*p*a-_*r*m+i*p*m+h*r*u-i*f*u)*A,e[2]=(o*p*a-_*c*a+_*r*l-i*p*l-o*r*u+i*c*u)*A,e[3]=(h*c*a-o*f*a-h*r*l+i*f*l+o*r*m-i*c*m)*A,e[4]=S*A,e[5]=(d*p*a-g*f*a+g*r*m-t*p*m-d*r*u+t*f*u)*A,e[6]=(g*c*a-s*p*a-g*r*l+t*p*l+s*r*u-t*c*u)*A,e[7]=(s*f*a-d*c*a+d*r*l-t*f*l-s*r*m+t*c*m)*A,e[8]=M*A,e[9]=(g*h*a-d*_*a-g*i*m+t*_*m+d*i*u-t*h*u)*A,e[10]=(s*_*a-g*o*a+g*i*l-t*_*l-s*i*u+t*o*u)*A,e[11]=(d*o*a-s*h*a-d*i*l+t*h*l+s*i*m-t*o*m)*A,e[12]=w*A,e[13]=(d*_*r-g*h*r+g*i*f-t*_*f-d*i*p+t*h*p)*A,e[14]=(g*o*r-s*_*r-g*i*c+t*_*c+s*i*p-t*o*p)*A,e[15]=(s*h*r-d*o*r+d*i*c-t*h*c-s*i*f+t*o*f)*A,this}scale(e){const t=this.elements,i=e.x,r=e.y,a=e.z;return t[0]*=i,t[4]*=r,t[8]*=a,t[1]*=i,t[5]*=r,t[9]*=a,t[2]*=i,t[6]*=r,t[10]*=a,t[3]*=i,t[7]*=r,t[11]*=a,this}getMaxScaleOnAxis(){const e=this.elements,t=e[0]*e[0]+e[1]*e[1]+e[2]*e[2],i=e[4]*e[4]+e[5]*e[5]+e[6]*e[6],r=e[8]*e[8]+e[9]*e[9]+e[10]*e[10];return Math.sqrt(Math.max(t,i,r))}makeTranslation(e,t,i){return e.isVector3?this.set(1,0,0,e.x,0,1,0,e.y,0,0,1,e.z,0,0,0,1):this.set(1,0,0,e,0,1,0,t,0,0,1,i,0,0,0,1),this}makeRotationX(e){const t=Math.cos(e),i=Math.sin(e);return this.set(1,0,0,0,0,t,-i,0,0,i,t,0,0,0,0,1),this}makeRotationY(e){const t=Math.cos(e),i=Math.sin(e);return this.set(t,0,i,0,0,1,0,0,-i,0,t,0,0,0,0,1),this}makeRotationZ(e){const t=Math.cos(e),i=Math.sin(e);return this.set(t,-i,0,0,i,t,0,0,0,0,1,0,0,0,0,1),this}makeRotationAxis(e,t){const i=Math.cos(t),r=Math.sin(t),a=1-i,s=e.x,o=e.y,c=e.z,l=a*s,d=a*o;return this.set(l*s+i,l*o-r*c,l*c+r*o,0,l*o+r*c,d*o+i,d*c-r*s,0,l*c-r*o,d*c+r*s,a*c*c+i,0,0,0,0,1),this}makeScale(e,t,i){return this.set(e,0,0,0,0,t,0,0,0,0,i,0,0,0,0,1),this}makeShear(e,t,i,r,a,s){return this.set(1,i,a,0,e,1,s,0,t,r,1,0,0,0,0,1),this}compose(e,t,i){const r=this.elements,a=t._x,s=t._y,o=t._z,c=t._w,l=a+a,d=s+s,h=o+o,f=a*l,m=a*d,g=a*h,_=s*d,p=s*h,u=o*h,b=c*l,S=c*d,M=c*h,w=i.x,T=i.y,A=i.z;return r[0]=(1-(_+u))*w,r[1]=(m+M)*w,r[2]=(g-S)*w,r[3]=0,r[4]=(m-M)*T,r[5]=(1-(f+u))*T,r[6]=(p+b)*T,r[7]=0,r[8]=(g+S)*A,r[9]=(p-b)*A,r[10]=(1-(f+_))*A,r[11]=0,r[12]=e.x,r[13]=e.y,r[14]=e.z,r[15]=1,this}decompose(e,t,i){const r=this.elements;let a=oi.set(r[0],r[1],r[2]).length();const s=oi.set(r[4],r[5],r[6]).length(),o=oi.set(r[8],r[9],r[10]).length();this.determinant()<0&&(a=-a),e.x=r[12],e.y=r[13],e.z=r[14],qt.copy(this);const l=1/a,d=1/s,h=1/o;return qt.elements[0]*=l,qt.elements[1]*=l,qt.elements[2]*=l,qt.elements[4]*=d,qt.elements[5]*=d,qt.elements[6]*=d,qt.elements[8]*=h,qt.elements[9]*=h,qt.elements[10]*=h,t.setFromRotationMatrix(qt),i.x=a,i.y=s,i.z=o,this}makePerspective(e,t,i,r,a,s,o=mn){const c=this.elements,l=2*a/(t-e),d=2*a/(i-r),h=(t+e)/(t-e),f=(i+r)/(i-r);let m,g;if(o===mn)m=-(s+a)/(s-a),g=-2*s*a/(s-a);else if(o===kr)m=-s/(s-a),g=-s*a/(s-a);else throw new Error("THREE.Matrix4.makePerspective(): Invalid coordinate system: "+o);return c[0]=l,c[4]=0,c[8]=h,c[12]=0,c[1]=0,c[5]=d,c[9]=f,c[13]=0,c[2]=0,c[6]=0,c[10]=m,c[14]=g,c[3]=0,c[7]=0,c[11]=-1,c[15]=0,this}makeOrthographic(e,t,i,r,a,s,o=mn){const c=this.elements,l=1/(t-e),d=1/(i-r),h=1/(s-a),f=(t+e)*l,m=(i+r)*d;let g,_;if(o===mn)g=(s+a)*h,_=-2*h;else if(o===kr)g=a*h,_=-1*h;else throw new Error("THREE.Matrix4.makeOrthographic(): Invalid coordinate system: "+o);return c[0]=2*l,c[4]=0,c[8]=0,c[12]=-f,c[1]=0,c[5]=2*d,c[9]=0,c[13]=-m,c[2]=0,c[6]=0,c[10]=_,c[14]=-g,c[3]=0,c[7]=0,c[11]=0,c[15]=1,this}equals(e){const t=this.elements,i=e.elements;for(let r=0;r<16;r++)if(t[r]!==i[r])return!1;return!0}fromArray(e,t=0){for(let i=0;i<16;i++)this.elements[i]=e[i+t];return this}toArray(e=[],t=0){const i=this.elements;return e[t]=i[0],e[t+1]=i[1],e[t+2]=i[2],e[t+3]=i[3],e[t+4]=i[4],e[t+5]=i[5],e[t+6]=i[6],e[t+7]=i[7],e[t+8]=i[8],e[t+9]=i[9],e[t+10]=i[10],e[t+11]=i[11],e[t+12]=i[12],e[t+13]=i[13],e[t+14]=i[14],e[t+15]=i[15],e}}const oi=new F,qt=new ct,hu=new F(0,0,0),fu=new F(1,1,1),bn=new F,or=new F,zt=new F,fo=new ct,po=new Li;class mt{constructor(e=0,t=0,i=0,r=mt.DEFAULT_ORDER){this.isEuler=!0,this._x=e,this._y=t,this._z=i,this._order=r}get x(){return this._x}set x(e){this._x=e,this._onChangeCallback()}get y(){return this._y}set y(e){this._y=e,this._onChangeCallback()}get z(){return this._z}set z(e){this._z=e,this._onChangeCallback()}get order(){return this._order}set order(e){this._order=e,this._onChangeCallback()}set(e,t,i,r=this._order){return this._x=e,this._y=t,this._z=i,this._order=r,this._onChangeCallback(),this}clone(){return new this.constructor(this._x,this._y,this._z,this._order)}copy(e){return this._x=e._x,this._y=e._y,this._z=e._z,this._order=e._order,this._onChangeCallback(),this}setFromRotationMatrix(e,t=this._order,i=!0){const r=e.elements,a=r[0],s=r[4],o=r[8],c=r[1],l=r[5],d=r[9],h=r[2],f=r[6],m=r[10];switch(t){case"XYZ":this._y=Math.asin(Xe(o,-1,1)),Math.abs(o)<.9999999?(this._x=Math.atan2(-d,m),this._z=Math.atan2(-s,a)):(this._x=Math.atan2(f,l),this._z=0);break;case"YXZ":this._x=Math.asin(-Xe(d,-1,1)),Math.abs(d)<.9999999?(this._y=Math.atan2(o,m),this._z=Math.atan2(c,l)):(this._y=Math.atan2(-h,a),this._z=0);break;case"ZXY":this._x=Math.asin(Xe(f,-1,1)),Math.abs(f)<.9999999?(this._y=Math.atan2(-h,m),this._z=Math.atan2(-s,l)):(this._y=0,this._z=Math.atan2(c,a));break;case"ZYX":this._y=Math.asin(-Xe(h,-1,1)),Math.abs(h)<.9999999?(this._x=Math.atan2(f,m),this._z=Math.atan2(c,a)):(this._x=0,this._z=Math.atan2(-s,l));break;case"YZX":this._z=Math.asin(Xe(c,-1,1)),Math.abs(c)<.9999999?(this._x=Math.atan2(-d,l),this._y=Math.atan2(-h,a)):(this._x=0,this._y=Math.atan2(o,m));break;case"XZY":this._z=Math.asin(-Xe(s,-1,1)),Math.abs(s)<.9999999?(this._x=Math.atan2(f,l),this._y=Math.atan2(o,a)):(this._x=Math.atan2(-d,m),this._y=0);break;default:console.warn("THREE.Euler: .setFromRotationMatrix() encountered an unknown order: "+t)}return this._order=t,i===!0&&this._onChangeCallback(),this}setFromQuaternion(e,t,i){return fo.makeRotationFromQuaternion(e),this.setFromRotationMatrix(fo,t,i)}setFromVector3(e,t=this._order){return this.set(e.x,e.y,e.z,t)}reorder(e){return po.setFromEuler(this),this.setFromQuaternion(po,e)}equals(e){return e._x===this._x&&e._y===this._y&&e._z===this._z&&e._order===this._order}fromArray(e){return this._x=e[0],this._y=e[1],this._z=e[2],e[3]!==void 0&&(this._order=e[3]),this._onChangeCallback(),this}toArray(e=[],t=0){return e[t]=this._x,e[t+1]=this._y,e[t+2]=this._z,e[t+3]=this._order,e}_onChange(e){return this._onChangeCallback=e,this}_onChangeCallback(){}*[Symbol.iterator](){yield this._x,yield this._y,yield this._z,yield this._order}}mt.DEFAULT_ORDER="XYZ";class ks{constructor(){this.mask=1}set(e){this.mask=(1<<e|0)>>>0}enable(e){this.mask|=1<<e|0}enableAll(){this.mask=-1}toggle(e){this.mask^=1<<e|0}disable(e){this.mask&=~(1<<e|0)}disableAll(){this.mask=0}test(e){return(this.mask&e.mask)!==0}isEnabled(e){return(this.mask&(1<<e|0))!==0}}let pu=0;const mo=new F,ci=new Li,on=new ct,cr=new F,ji=new F,mu=new F,gu=new Li,go=new F(1,0,0),_o=new F(0,1,0),vo=new F(0,0,1),xo={type:"added"},_u={type:"removed"},li={type:"childadded",child:null},aa={type:"childremoved",child:null};class Et extends Di{constructor(){super(),this.isObject3D=!0,Object.defineProperty(this,"id",{value:pu++}),this.uuid=Yi(),this.name="",this.type="Object3D",this.parent=null,this.children=[],this.up=Et.DEFAULT_UP.clone();const e=new F,t=new mt,i=new Li,r=new F(1,1,1);function a(){i.setFromEuler(t,!1)}function s(){t.setFromQuaternion(i,void 0,!1)}t._onChange(a),i._onChange(s),Object.defineProperties(this,{position:{configurable:!0,enumerable:!0,value:e},rotation:{configurable:!0,enumerable:!0,value:t},quaternion:{configurable:!0,enumerable:!0,value:i},scale:{configurable:!0,enumerable:!0,value:r},modelViewMatrix:{value:new ct},normalMatrix:{value:new Be}}),this.matrix=new ct,this.matrixWorld=new ct,this.matrixAutoUpdate=Et.DEFAULT_MATRIX_AUTO_UPDATE,this.matrixWorldAutoUpdate=Et.DEFAULT_MATRIX_WORLD_AUTO_UPDATE,this.matrixWorldNeedsUpdate=!1,this.layers=new ks,this.visible=!0,this.castShadow=!1,this.receiveShadow=!1,this.frustumCulled=!0,this.renderOrder=0,this.animations=[],this.userData={}}onBeforeShadow(){}onAfterShadow(){}onBeforeRender(){}onAfterRender(){}applyMatrix4(e){this.matrixAutoUpdate&&this.updateMatrix(),this.matrix.premultiply(e),this.matrix.decompose(this.position,this.quaternion,this.scale)}applyQuaternion(e){return this.quaternion.premultiply(e),this}setRotationFromAxisAngle(e,t){this.quaternion.setFromAxisAngle(e,t)}setRotationFromEuler(e){this.quaternion.setFromEuler(e,!0)}setRotationFromMatrix(e){this.quaternion.setFromRotationMatrix(e)}setRotationFromQuaternion(e){this.quaternion.copy(e)}rotateOnAxis(e,t){return ci.setFromAxisAngle(e,t),this.quaternion.multiply(ci),this}rotateOnWorldAxis(e,t){return ci.setFromAxisAngle(e,t),this.quaternion.premultiply(ci),this}rotateX(e){return this.rotateOnAxis(go,e)}rotateY(e){return this.rotateOnAxis(_o,e)}rotateZ(e){return this.rotateOnAxis(vo,e)}translateOnAxis(e,t){return mo.copy(e).applyQuaternion(this.quaternion),this.position.add(mo.multiplyScalar(t)),this}translateX(e){return this.translateOnAxis(go,e)}translateY(e){return this.translateOnAxis(_o,e)}translateZ(e){return this.translateOnAxis(vo,e)}localToWorld(e){return this.updateWorldMatrix(!0,!1),e.applyMatrix4(this.matrixWorld)}worldToLocal(e){return this.updateWorldMatrix(!0,!1),e.applyMatrix4(on.copy(this.matrixWorld).invert())}lookAt(e,t,i){e.isVector3?cr.copy(e):cr.set(e,t,i);const r=this.parent;this.updateWorldMatrix(!0,!1),ji.setFromMatrixPosition(this.matrixWorld),this.isCamera||this.isLight?on.lookAt(ji,cr,this.up):on.lookAt(cr,ji,this.up),this.quaternion.setFromRotationMatrix(on),r&&(on.extractRotation(r.matrixWorld),ci.setFromRotationMatrix(on),this.quaternion.premultiply(ci.invert()))}add(e){if(arguments.length>1){for(let t=0;t<arguments.length;t++)this.add(arguments[t]);return this}return e===this?(console.error("THREE.Object3D.add: object can't be added as a child of itself.",e),this):(e&&e.isObject3D?(e.removeFromParent(),e.parent=this,this.children.push(e),e.dispatchEvent(xo),li.child=e,this.dispatchEvent(li),li.child=null):console.error("THREE.Object3D.add: object not an instance of THREE.Object3D.",e),this)}remove(e){if(arguments.length>1){for(let i=0;i<arguments.length;i++)this.remove(arguments[i]);return this}const t=this.children.indexOf(e);return t!==-1&&(e.parent=null,this.children.splice(t,1),e.dispatchEvent(_u),aa.child=e,this.dispatchEvent(aa),aa.child=null),this}removeFromParent(){const e=this.parent;return e!==null&&e.remove(this),this}clear(){return this.remove(...this.children)}attach(e){return this.updateWorldMatrix(!0,!1),on.copy(this.matrixWorld).invert(),e.parent!==null&&(e.parent.updateWorldMatrix(!0,!1),on.multiply(e.parent.matrixWorld)),e.applyMatrix4(on),e.removeFromParent(),e.parent=this,this.children.push(e),e.updateWorldMatrix(!1,!0),e.dispatchEvent(xo),li.child=e,this.dispatchEvent(li),li.child=null,this}getObjectById(e){return this.getObjectByProperty("id",e)}getObjectByName(e){return this.getObjectByProperty("name",e)}getObjectByProperty(e,t){if(this[e]===t)return this;for(let i=0,r=this.children.length;i<r;i++){const s=this.children[i].getObjectByProperty(e,t);if(s!==void 0)return s}}getObjectsByProperty(e,t,i=[]){this[e]===t&&i.push(this);const r=this.children;for(let a=0,s=r.length;a<s;a++)r[a].getObjectsByProperty(e,t,i);return i}getWorldPosition(e){return this.updateWorldMatrix(!0,!1),e.setFromMatrixPosition(this.matrixWorld)}getWorldQuaternion(e){return this.updateWorldMatrix(!0,!1),this.matrixWorld.decompose(ji,e,mu),e}getWorldScale(e){return this.updateWorldMatrix(!0,!1),this.matrixWorld.decompose(ji,gu,e),e}getWorldDirection(e){this.updateWorldMatrix(!0,!1);const t=this.matrixWorld.elements;return e.set(t[8],t[9],t[10]).normalize()}raycast(){}traverse(e){e(this);const t=this.children;for(let i=0,r=t.length;i<r;i++)t[i].traverse(e)}traverseVisible(e){if(this.visible===!1)return;e(this);const t=this.children;for(let i=0,r=t.length;i<r;i++)t[i].traverseVisible(e)}traverseAncestors(e){const t=this.parent;t!==null&&(e(t),t.traverseAncestors(e))}updateMatrix(){this.matrix.compose(this.position,this.quaternion,this.scale),this.matrixWorldNeedsUpdate=!0}updateMatrixWorld(e){this.matrixAutoUpdate&&this.updateMatrix(),(this.matrixWorldNeedsUpdate||e)&&(this.matrixWorldAutoUpdate===!0&&(this.parent===null?this.matrixWorld.copy(this.matrix):this.matrixWorld.multiplyMatrices(this.parent.matrixWorld,this.matrix)),this.matrixWorldNeedsUpdate=!1,e=!0);const t=this.children;for(let i=0,r=t.length;i<r;i++)t[i].updateMatrixWorld(e)}updateWorldMatrix(e,t){const i=this.parent;if(e===!0&&i!==null&&i.updateWorldMatrix(!0,!1),this.matrixAutoUpdate&&this.updateMatrix(),this.matrixWorldAutoUpdate===!0&&(this.parent===null?this.matrixWorld.copy(this.matrix):this.matrixWorld.multiplyMatrices(this.parent.matrixWorld,this.matrix)),t===!0){const r=this.children;for(let a=0,s=r.length;a<s;a++)r[a].updateWorldMatrix(!1,!0)}}toJSON(e){const t=e===void 0||typeof e=="string",i={};t&&(e={geometries:{},materials:{},textures:{},images:{},shapes:{},skeletons:{},animations:{},nodes:{}},i.metadata={version:4.6,type:"Object",generator:"Object3D.toJSON"});const r={};r.uuid=this.uuid,r.type=this.type,this.name!==""&&(r.name=this.name),this.castShadow===!0&&(r.castShadow=!0),this.receiveShadow===!0&&(r.receiveShadow=!0),this.visible===!1&&(r.visible=!1),this.frustumCulled===!1&&(r.frustumCulled=!1),this.renderOrder!==0&&(r.renderOrder=this.renderOrder),Object.keys(this.userData).length>0&&(r.userData=this.userData),r.layers=this.layers.mask,r.matrix=this.matrix.toArray(),r.up=this.up.toArray(),this.matrixAutoUpdate===!1&&(r.matrixAutoUpdate=!1),this.isInstancedMesh&&(r.type="InstancedMesh",r.count=this.count,r.instanceMatrix=this.instanceMatrix.toJSON(),this.instanceColor!==null&&(r.instanceColor=this.instanceColor.toJSON())),this.isBatchedMesh&&(r.type="BatchedMesh",r.perObjectFrustumCulled=this.perObjectFrustumCulled,r.sortObjects=this.sortObjects,r.drawRanges=this._drawRanges,r.reservedRanges=this._reservedRanges,r.visibility=this._visibility,r.active=this._active,r.bounds=this._bounds.map(o=>({boxInitialized:o.boxInitialized,boxMin:o.box.min.toArray(),boxMax:o.box.max.toArray(),sphereInitialized:o.sphereInitialized,sphereRadius:o.sphere.radius,sphereCenter:o.sphere.center.toArray()})),r.maxInstanceCount=this._maxInstanceCount,r.maxVertexCount=this._maxVertexCount,r.maxIndexCount=this._maxIndexCount,r.geometryInitialized=this._geometryInitialized,r.geometryCount=this._geometryCount,r.matricesTexture=this._matricesTexture.toJSON(e),this._colorsTexture!==null&&(r.colorsTexture=this._colorsTexture.toJSON(e)),this.boundingSphere!==null&&(r.boundingSphere={center:r.boundingSphere.center.toArray(),radius:r.boundingSphere.radius}),this.boundingBox!==null&&(r.boundingBox={min:r.boundingBox.min.toArray(),max:r.boundingBox.max.toArray()}));function a(o,c){return o[c.uuid]===void 0&&(o[c.uuid]=c.toJSON(e)),c.uuid}if(this.isScene)this.background&&(this.background.isColor?r.background=this.background.toJSON():this.background.isTexture&&(r.background=this.background.toJSON(e).uuid)),this.environment&&this.environment.isTexture&&this.environment.isRenderTargetTexture!==!0&&(r.environment=this.environment.toJSON(e).uuid);else if(this.isMesh||this.isLine||this.isPoints){r.geometry=a(e.geometries,this.geometry);const o=this.geometry.parameters;if(o!==void 0&&o.shapes!==void 0){const c=o.shapes;if(Array.isArray(c))for(let l=0,d=c.length;l<d;l++){const h=c[l];a(e.shapes,h)}else a(e.shapes,c)}}if(this.isSkinnedMesh&&(r.bindMode=this.bindMode,r.bindMatrix=this.bindMatrix.toArray(),this.skeleton!==void 0&&(a(e.skeletons,this.skeleton),r.skeleton=this.skeleton.uuid)),this.material!==void 0)if(Array.isArray(this.material)){const o=[];for(let c=0,l=this.material.length;c<l;c++)o.push(a(e.materials,this.material[c]));r.material=o}else r.material=a(e.materials,this.material);if(this.children.length>0){r.children=[];for(let o=0;o<this.children.length;o++)r.children.push(this.children[o].toJSON(e).object)}if(this.animations.length>0){r.animations=[];for(let o=0;o<this.animations.length;o++){const c=this.animations[o];r.animations.push(a(e.animations,c))}}if(t){const o=s(e.geometries),c=s(e.materials),l=s(e.textures),d=s(e.images),h=s(e.shapes),f=s(e.skeletons),m=s(e.animations),g=s(e.nodes);o.length>0&&(i.geometries=o),c.length>0&&(i.materials=c),l.length>0&&(i.textures=l),d.length>0&&(i.images=d),h.length>0&&(i.shapes=h),f.length>0&&(i.skeletons=f),m.length>0&&(i.animations=m),g.length>0&&(i.nodes=g)}return i.object=r,i;function s(o){const c=[];for(const l in o){const d=o[l];delete d.metadata,c.push(d)}return c}}clone(e){return new this.constructor().copy(this,e)}copy(e,t=!0){if(this.name=e.name,this.up.copy(e.up),this.position.copy(e.position),this.rotation.order=e.rotation.order,this.quaternion.copy(e.quaternion),this.scale.copy(e.scale),this.matrix.copy(e.matrix),this.matrixWorld.copy(e.matrixWorld),this.matrixAutoUpdate=e.matrixAutoUpdate,this.matrixWorldAutoUpdate=e.matrixWorldAutoUpdate,this.matrixWorldNeedsUpdate=e.matrixWorldNeedsUpdate,this.layers.mask=e.layers.mask,this.visible=e.visible,this.castShadow=e.castShadow,this.receiveShadow=e.receiveShadow,this.frustumCulled=e.frustumCulled,this.renderOrder=e.renderOrder,this.animations=e.animations.slice(),this.userData=JSON.parse(JSON.stringify(e.userData)),t===!0)for(let i=0;i<e.children.length;i++){const r=e.children[i];this.add(r.clone())}return this}}Et.DEFAULT_UP=new F(0,1,0);Et.DEFAULT_MATRIX_AUTO_UPDATE=!0;Et.DEFAULT_MATRIX_WORLD_AUTO_UPDATE=!0;const $t=new F,cn=new F,sa=new F,ln=new F,ui=new F,di=new F,Mo=new F,oa=new F,ca=new F,la=new F,ua=new dt,da=new dt,ha=new dt;class Gt{constructor(e=new F,t=new F,i=new F){this.a=e,this.b=t,this.c=i}static getNormal(e,t,i,r){r.subVectors(i,t),$t.subVectors(e,t),r.cross($t);const a=r.lengthSq();return a>0?r.multiplyScalar(1/Math.sqrt(a)):r.set(0,0,0)}static getBarycoord(e,t,i,r,a){$t.subVectors(r,t),cn.subVectors(i,t),sa.subVectors(e,t);const s=$t.dot($t),o=$t.dot(cn),c=$t.dot(sa),l=cn.dot(cn),d=cn.dot(sa),h=s*l-o*o;if(h===0)return a.set(0,0,0),null;const f=1/h,m=(l*c-o*d)*f,g=(s*d-o*c)*f;return a.set(1-m-g,g,m)}static containsPoint(e,t,i,r){return this.getBarycoord(e,t,i,r,ln)===null?!1:ln.x>=0&&ln.y>=0&&ln.x+ln.y<=1}static getInterpolation(e,t,i,r,a,s,o,c){return this.getBarycoord(e,t,i,r,ln)===null?(c.x=0,c.y=0,"z"in c&&(c.z=0),"w"in c&&(c.w=0),null):(c.setScalar(0),c.addScaledVector(a,ln.x),c.addScaledVector(s,ln.y),c.addScaledVector(o,ln.z),c)}static getInterpolatedAttribute(e,t,i,r,a,s){return ua.setScalar(0),da.setScalar(0),ha.setScalar(0),ua.fromBufferAttribute(e,t),da.fromBufferAttribute(e,i),ha.fromBufferAttribute(e,r),s.setScalar(0),s.addScaledVector(ua,a.x),s.addScaledVector(da,a.y),s.addScaledVector(ha,a.z),s}static isFrontFacing(e,t,i,r){return $t.subVectors(i,t),cn.subVectors(e,t),$t.cross(cn).dot(r)<0}set(e,t,i){return this.a.copy(e),this.b.copy(t),this.c.copy(i),this}setFromPointsAndIndices(e,t,i,r){return this.a.copy(e[t]),this.b.copy(e[i]),this.c.copy(e[r]),this}setFromAttributeAndIndices(e,t,i,r){return this.a.fromBufferAttribute(e,t),this.b.fromBufferAttribute(e,i),this.c.fromBufferAttribute(e,r),this}clone(){return new this.constructor().copy(this)}copy(e){return this.a.copy(e.a),this.b.copy(e.b),this.c.copy(e.c),this}getArea(){return $t.subVectors(this.c,this.b),cn.subVectors(this.a,this.b),$t.cross(cn).length()*.5}getMidpoint(e){return e.addVectors(this.a,this.b).add(this.c).multiplyScalar(1/3)}getNormal(e){return Gt.getNormal(this.a,this.b,this.c,e)}getPlane(e){return e.setFromCoplanarPoints(this.a,this.b,this.c)}getBarycoord(e,t){return Gt.getBarycoord(e,this.a,this.b,this.c,t)}getInterpolation(e,t,i,r,a){return Gt.getInterpolation(e,this.a,this.b,this.c,t,i,r,a)}containsPoint(e){return Gt.containsPoint(e,this.a,this.b,this.c)}isFrontFacing(e){return Gt.isFrontFacing(this.a,this.b,this.c,e)}intersectsBox(e){return e.intersectsTriangle(this)}closestPointToPoint(e,t){const i=this.a,r=this.b,a=this.c;let s,o;ui.subVectors(r,i),di.subVectors(a,i),oa.subVectors(e,i);const c=ui.dot(oa),l=di.dot(oa);if(c<=0&&l<=0)return t.copy(i);ca.subVectors(e,r);const d=ui.dot(ca),h=di.dot(ca);if(d>=0&&h<=d)return t.copy(r);const f=c*h-d*l;if(f<=0&&c>=0&&d<=0)return s=c/(c-d),t.copy(i).addScaledVector(ui,s);la.subVectors(e,a);const m=ui.dot(la),g=di.dot(la);if(g>=0&&m<=g)return t.copy(a);const _=m*l-c*g;if(_<=0&&l>=0&&g<=0)return o=l/(l-g),t.copy(i).addScaledVector(di,o);const p=d*g-m*h;if(p<=0&&h-d>=0&&m-g>=0)return Mo.subVectors(a,r),o=(h-d)/(h-d+(m-g)),t.copy(r).addScaledVector(Mo,o);const u=1/(p+_+f);return s=_*u,o=f*u,t.copy(i).addScaledVector(ui,s).addScaledVector(di,o)}equals(e){return e.a.equals(this.a)&&e.b.equals(this.b)&&e.c.equals(this.c)}}const Uc={aliceblue:15792383,antiquewhite:16444375,aqua:65535,aquamarine:8388564,azure:15794175,beige:16119260,bisque:16770244,black:0,blanchedalmond:16772045,blue:255,blueviolet:9055202,brown:10824234,burlywood:14596231,cadetblue:6266528,chartreuse:8388352,chocolate:13789470,coral:16744272,cornflowerblue:6591981,cornsilk:16775388,crimson:14423100,cyan:65535,darkblue:139,darkcyan:35723,darkgoldenrod:12092939,darkgray:11119017,darkgreen:25600,darkgrey:11119017,darkkhaki:12433259,darkmagenta:9109643,darkolivegreen:5597999,darkorange:16747520,darkorchid:10040012,darkred:9109504,darksalmon:15308410,darkseagreen:9419919,darkslateblue:4734347,darkslategray:3100495,darkslategrey:3100495,darkturquoise:52945,darkviolet:9699539,deeppink:16716947,deepskyblue:49151,dimgray:6908265,dimgrey:6908265,dodgerblue:2003199,firebrick:11674146,floralwhite:16775920,forestgreen:2263842,fuchsia:16711935,gainsboro:14474460,ghostwhite:16316671,gold:16766720,goldenrod:14329120,gray:8421504,green:32768,greenyellow:11403055,grey:8421504,honeydew:15794160,hotpink:16738740,indianred:13458524,indigo:4915330,ivory:16777200,khaki:15787660,lavender:15132410,lavenderblush:16773365,lawngreen:8190976,lemonchiffon:16775885,lightblue:11393254,lightcoral:15761536,lightcyan:14745599,lightgoldenrodyellow:16448210,lightgray:13882323,lightgreen:9498256,lightgrey:13882323,lightpink:16758465,lightsalmon:16752762,lightseagreen:2142890,lightskyblue:8900346,lightslategray:7833753,lightslategrey:7833753,lightsteelblue:11584734,lightyellow:16777184,lime:65280,limegreen:3329330,linen:16445670,magenta:16711935,maroon:8388608,mediumaquamarine:6737322,mediumblue:205,mediumorchid:12211667,mediumpurple:9662683,mediumseagreen:3978097,mediumslateblue:8087790,mediumspringgreen:64154,mediumturquoise:4772300,mediumvioletred:13047173,midnightblue:1644912,mintcream:16121850,mistyrose:16770273,moccasin:16770229,navajowhite:16768685,navy:128,oldlace:16643558,olive:8421376,olivedrab:7048739,orange:16753920,orangered:16729344,orchid:14315734,palegoldenrod:15657130,palegreen:10025880,paleturquoise:11529966,palevioletred:14381203,papayawhip:16773077,peachpuff:16767673,peru:13468991,pink:16761035,plum:14524637,powderblue:11591910,purple:8388736,rebeccapurple:6697881,red:16711680,rosybrown:12357519,royalblue:4286945,saddlebrown:9127187,salmon:16416882,sandybrown:16032864,seagreen:3050327,seashell:16774638,sienna:10506797,silver:12632256,skyblue:8900331,slateblue:6970061,slategray:7372944,slategrey:7372944,snow:16775930,springgreen:65407,steelblue:4620980,tan:13808780,teal:32896,thistle:14204888,tomato:16737095,turquoise:4251856,violet:15631086,wheat:16113331,white:16777215,whitesmoke:16119285,yellow:16776960,yellowgreen:10145074},yn={h:0,s:0,l:0},lr={h:0,s:0,l:0};function fa(n,e,t){return t<0&&(t+=1),t>1&&(t-=1),t<1/6?n+(e-n)*6*t:t<1/2?e:t<2/3?n+(e-n)*6*(2/3-t):n}class ce{constructor(e,t,i){return this.isColor=!0,this.r=1,this.g=1,this.b=1,this.set(e,t,i)}set(e,t,i){if(t===void 0&&i===void 0){const r=e;r&&r.isColor?this.copy(r):typeof r=="number"?this.setHex(r):typeof r=="string"&&this.setStyle(r)}else this.setRGB(e,t,i);return this}setScalar(e){return this.r=e,this.g=e,this.b=e,this}setHex(e,t=Ft){return e=Math.floor(e),this.r=(e>>16&255)/255,this.g=(e>>8&255)/255,this.b=(e&255)/255,Qe.toWorkingColorSpace(this,t),this}setRGB(e,t,i,r=Qe.workingColorSpace){return this.r=e,this.g=t,this.b=i,Qe.toWorkingColorSpace(this,r),this}setHSL(e,t,i,r=Qe.workingColorSpace){if(e=eu(e,1),t=Xe(t,0,1),i=Xe(i,0,1),t===0)this.r=this.g=this.b=i;else{const a=i<=.5?i*(1+t):i+t-i*t,s=2*i-a;this.r=fa(s,a,e+1/3),this.g=fa(s,a,e),this.b=fa(s,a,e-1/3)}return Qe.toWorkingColorSpace(this,r),this}setStyle(e,t=Ft){function i(a){a!==void 0&&parseFloat(a)<1&&console.warn("THREE.Color: Alpha component of "+e+" will be ignored.")}let r;if(r=/^(\w+)\(([^\)]*)\)/.exec(e)){let a;const s=r[1],o=r[2];switch(s){case"rgb":case"rgba":if(a=/^\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*(?:,\s*(\d*\.?\d+)\s*)?$/.exec(o))return i(a[4]),this.setRGB(Math.min(255,parseInt(a[1],10))/255,Math.min(255,parseInt(a[2],10))/255,Math.min(255,parseInt(a[3],10))/255,t);if(a=/^\s*(\d+)\%\s*,\s*(\d+)\%\s*,\s*(\d+)\%\s*(?:,\s*(\d*\.?\d+)\s*)?$/.exec(o))return i(a[4]),this.setRGB(Math.min(100,parseInt(a[1],10))/100,Math.min(100,parseInt(a[2],10))/100,Math.min(100,parseInt(a[3],10))/100,t);break;case"hsl":case"hsla":if(a=/^\s*(\d*\.?\d+)\s*,\s*(\d*\.?\d+)\%\s*,\s*(\d*\.?\d+)\%\s*(?:,\s*(\d*\.?\d+)\s*)?$/.exec(o))return i(a[4]),this.setHSL(parseFloat(a[1])/360,parseFloat(a[2])/100,parseFloat(a[3])/100,t);break;default:console.warn("THREE.Color: Unknown color model "+e)}}else if(r=/^\#([A-Fa-f\d]+)$/.exec(e)){const a=r[1],s=a.length;if(s===3)return this.setRGB(parseInt(a.charAt(0),16)/15,parseInt(a.charAt(1),16)/15,parseInt(a.charAt(2),16)/15,t);if(s===6)return this.setHex(parseInt(a,16),t);console.warn("THREE.Color: Invalid hex color "+e)}else if(e&&e.length>0)return this.setColorName(e,t);return this}setColorName(e,t=Ft){const i=Uc[e.toLowerCase()];return i!==void 0?this.setHex(i,t):console.warn("THREE.Color: Unknown color "+e),this}clone(){return new this.constructor(this.r,this.g,this.b)}copy(e){return this.r=e.r,this.g=e.g,this.b=e.b,this}copySRGBToLinear(e){return this.r=_n(e.r),this.g=_n(e.g),this.b=_n(e.b),this}copyLinearToSRGB(e){return this.r=bi(e.r),this.g=bi(e.g),this.b=bi(e.b),this}convertSRGBToLinear(){return this.copySRGBToLinear(this),this}convertLinearToSRGB(){return this.copyLinearToSRGB(this),this}getHex(e=Ft){return Qe.fromWorkingColorSpace(Tt.copy(this),e),Math.round(Xe(Tt.r*255,0,255))*65536+Math.round(Xe(Tt.g*255,0,255))*256+Math.round(Xe(Tt.b*255,0,255))}getHexString(e=Ft){return("000000"+this.getHex(e).toString(16)).slice(-6)}getHSL(e,t=Qe.workingColorSpace){Qe.fromWorkingColorSpace(Tt.copy(this),t);const i=Tt.r,r=Tt.g,a=Tt.b,s=Math.max(i,r,a),o=Math.min(i,r,a);let c,l;const d=(o+s)/2;if(o===s)c=0,l=0;else{const h=s-o;switch(l=d<=.5?h/(s+o):h/(2-s-o),s){case i:c=(r-a)/h+(r<a?6:0);break;case r:c=(a-i)/h+2;break;case a:c=(i-r)/h+4;break}c/=6}return e.h=c,e.s=l,e.l=d,e}getRGB(e,t=Qe.workingColorSpace){return Qe.fromWorkingColorSpace(Tt.copy(this),t),e.r=Tt.r,e.g=Tt.g,e.b=Tt.b,e}getStyle(e=Ft){Qe.fromWorkingColorSpace(Tt.copy(this),e);const t=Tt.r,i=Tt.g,r=Tt.b;return e!==Ft?`color(${e} ${t.toFixed(3)} ${i.toFixed(3)} ${r.toFixed(3)})`:`rgb(${Math.round(t*255)},${Math.round(i*255)},${Math.round(r*255)})`}offsetHSL(e,t,i){return this.getHSL(yn),this.setHSL(yn.h+e,yn.s+t,yn.l+i)}add(e){return this.r+=e.r,this.g+=e.g,this.b+=e.b,this}addColors(e,t){return this.r=e.r+t.r,this.g=e.g+t.g,this.b=e.b+t.b,this}addScalar(e){return this.r+=e,this.g+=e,this.b+=e,this}sub(e){return this.r=Math.max(0,this.r-e.r),this.g=Math.max(0,this.g-e.g),this.b=Math.max(0,this.b-e.b),this}multiply(e){return this.r*=e.r,this.g*=e.g,this.b*=e.b,this}multiplyScalar(e){return this.r*=e,this.g*=e,this.b*=e,this}lerp(e,t){return this.r+=(e.r-this.r)*t,this.g+=(e.g-this.g)*t,this.b+=(e.b-this.b)*t,this}lerpColors(e,t,i){return this.r=e.r+(t.r-e.r)*i,this.g=e.g+(t.g-e.g)*i,this.b=e.b+(t.b-e.b)*i,this}lerpHSL(e,t){this.getHSL(yn),e.getHSL(lr);const i=Yr(yn.h,lr.h,t),r=Yr(yn.s,lr.s,t),a=Yr(yn.l,lr.l,t);return this.setHSL(i,r,a),this}setFromVector3(e){return this.r=e.x,this.g=e.y,this.b=e.z,this}applyMatrix3(e){const t=this.r,i=this.g,r=this.b,a=e.elements;return this.r=a[0]*t+a[3]*i+a[6]*r,this.g=a[1]*t+a[4]*i+a[7]*r,this.b=a[2]*t+a[5]*i+a[8]*r,this}equals(e){return e.r===this.r&&e.g===this.g&&e.b===this.b}fromArray(e,t=0){return this.r=e[t],this.g=e[t+1],this.b=e[t+2],this}toArray(e=[],t=0){return e[t]=this.r,e[t+1]=this.g,e[t+2]=this.b,e}fromBufferAttribute(e,t){return this.r=e.getX(t),this.g=e.getY(t),this.b=e.getZ(t),this}toJSON(){return this.getHex()}*[Symbol.iterator](){yield this.r,yield this.g,yield this.b}}const Tt=new ce;ce.NAMES=Uc;let vu=0;class Ii extends Di{constructor(){super(),this.isMaterial=!0,Object.defineProperty(this,"id",{value:vu++}),this.uuid=Yi(),this.name="",this.type="Material",this.blending=Si,this.side=Ln,this.vertexColors=!1,this.opacity=1,this.transparent=!1,this.alphaHash=!1,this.blendSrc=Ia,this.blendDst=Ua,this.blendEquation=Kn,this.blendSrcAlpha=null,this.blendDstAlpha=null,this.blendEquationAlpha=null,this.blendColor=new ce(0,0,0),this.blendAlpha=0,this.depthFunc=yi,this.depthTest=!0,this.depthWrite=!0,this.stencilWriteMask=255,this.stencilFunc=ao,this.stencilRef=0,this.stencilFuncMask=255,this.stencilFail=ni,this.stencilZFail=ni,this.stencilZPass=ni,this.stencilWrite=!1,this.clippingPlanes=null,this.clipIntersection=!1,this.clipShadows=!1,this.shadowSide=null,this.colorWrite=!0,this.precision=null,this.polygonOffset=!1,this.polygonOffsetFactor=0,this.polygonOffsetUnits=0,this.dithering=!1,this.alphaToCoverage=!1,this.premultipliedAlpha=!1,this.forceSinglePass=!1,this.visible=!0,this.toneMapped=!0,this.userData={},this.version=0,this._alphaTest=0}get alphaTest(){return this._alphaTest}set alphaTest(e){this._alphaTest>0!=e>0&&this.version++,this._alphaTest=e}onBeforeRender(){}onBeforeCompile(){}customProgramCacheKey(){return this.onBeforeCompile.toString()}setValues(e){if(e!==void 0)for(const t in e){const i=e[t];if(i===void 0){console.warn(`THREE.Material: parameter '${t}' has value of undefined.`);continue}const r=this[t];if(r===void 0){console.warn(`THREE.Material: '${t}' is not a property of THREE.${this.type}.`);continue}r&&r.isColor?r.set(i):r&&r.isVector3&&i&&i.isVector3?r.copy(i):this[t]=i}}toJSON(e){const t=e===void 0||typeof e=="string";t&&(e={textures:{},images:{}});const i={metadata:{version:4.6,type:"Material",generator:"Material.toJSON"}};i.uuid=this.uuid,i.type=this.type,this.name!==""&&(i.name=this.name),this.color&&this.color.isColor&&(i.color=this.color.getHex()),this.roughness!==void 0&&(i.roughness=this.roughness),this.metalness!==void 0&&(i.metalness=this.metalness),this.sheen!==void 0&&(i.sheen=this.sheen),this.sheenColor&&this.sheenColor.isColor&&(i.sheenColor=this.sheenColor.getHex()),this.sheenRoughness!==void 0&&(i.sheenRoughness=this.sheenRoughness),this.emissive&&this.emissive.isColor&&(i.emissive=this.emissive.getHex()),this.emissiveIntensity!==void 0&&this.emissiveIntensity!==1&&(i.emissiveIntensity=this.emissiveIntensity),this.specular&&this.specular.isColor&&(i.specular=this.specular.getHex()),this.specularIntensity!==void 0&&(i.specularIntensity=this.specularIntensity),this.specularColor&&this.specularColor.isColor&&(i.specularColor=this.specularColor.getHex()),this.shininess!==void 0&&(i.shininess=this.shininess),this.clearcoat!==void 0&&(i.clearcoat=this.clearcoat),this.clearcoatRoughness!==void 0&&(i.clearcoatRoughness=this.clearcoatRoughness),this.clearcoatMap&&this.clearcoatMap.isTexture&&(i.clearcoatMap=this.clearcoatMap.toJSON(e).uuid),this.clearcoatRoughnessMap&&this.clearcoatRoughnessMap.isTexture&&(i.clearcoatRoughnessMap=this.clearcoatRoughnessMap.toJSON(e).uuid),this.clearcoatNormalMap&&this.clearcoatNormalMap.isTexture&&(i.clearcoatNormalMap=this.clearcoatNormalMap.toJSON(e).uuid,i.clearcoatNormalScale=this.clearcoatNormalScale.toArray()),this.dispersion!==void 0&&(i.dispersion=this.dispersion),this.iridescence!==void 0&&(i.iridescence=this.iridescence),this.iridescenceIOR!==void 0&&(i.iridescenceIOR=this.iridescenceIOR),this.iridescenceThicknessRange!==void 0&&(i.iridescenceThicknessRange=this.iridescenceThicknessRange),this.iridescenceMap&&this.iridescenceMap.isTexture&&(i.iridescenceMap=this.iridescenceMap.toJSON(e).uuid),this.iridescenceThicknessMap&&this.iridescenceThicknessMap.isTexture&&(i.iridescenceThicknessMap=this.iridescenceThicknessMap.toJSON(e).uuid),this.anisotropy!==void 0&&(i.anisotropy=this.anisotropy),this.anisotropyRotation!==void 0&&(i.anisotropyRotation=this.anisotropyRotation),this.anisotropyMap&&this.anisotropyMap.isTexture&&(i.anisotropyMap=this.anisotropyMap.toJSON(e).uuid),this.map&&this.map.isTexture&&(i.map=this.map.toJSON(e).uuid),this.matcap&&this.matcap.isTexture&&(i.matcap=this.matcap.toJSON(e).uuid),this.alphaMap&&this.alphaMap.isTexture&&(i.alphaMap=this.alphaMap.toJSON(e).uuid),this.lightMap&&this.lightMap.isTexture&&(i.lightMap=this.lightMap.toJSON(e).uuid,i.lightMapIntensity=this.lightMapIntensity),this.aoMap&&this.aoMap.isTexture&&(i.aoMap=this.aoMap.toJSON(e).uuid,i.aoMapIntensity=this.aoMapIntensity),this.bumpMap&&this.bumpMap.isTexture&&(i.bumpMap=this.bumpMap.toJSON(e).uuid,i.bumpScale=this.bumpScale),this.normalMap&&this.normalMap.isTexture&&(i.normalMap=this.normalMap.toJSON(e).uuid,i.normalMapType=this.normalMapType,i.normalScale=this.normalScale.toArray()),this.displacementMap&&this.displacementMap.isTexture&&(i.displacementMap=this.displacementMap.toJSON(e).uuid,i.displacementScale=this.displacementScale,i.displacementBias=this.displacementBias),this.roughnessMap&&this.roughnessMap.isTexture&&(i.roughnessMap=this.roughnessMap.toJSON(e).uuid),this.metalnessMap&&this.metalnessMap.isTexture&&(i.metalnessMap=this.metalnessMap.toJSON(e).uuid),this.emissiveMap&&this.emissiveMap.isTexture&&(i.emissiveMap=this.emissiveMap.toJSON(e).uuid),this.specularMap&&this.specularMap.isTexture&&(i.specularMap=this.specularMap.toJSON(e).uuid),this.specularIntensityMap&&this.specularIntensityMap.isTexture&&(i.specularIntensityMap=this.specularIntensityMap.toJSON(e).uuid),this.specularColorMap&&this.specularColorMap.isTexture&&(i.specularColorMap=this.specularColorMap.toJSON(e).uuid),this.envMap&&this.envMap.isTexture&&(i.envMap=this.envMap.toJSON(e).uuid,this.combine!==void 0&&(i.combine=this.combine)),this.envMapRotation!==void 0&&(i.envMapRotation=this.envMapRotation.toArray()),this.envMapIntensity!==void 0&&(i.envMapIntensity=this.envMapIntensity),this.reflectivity!==void 0&&(i.reflectivity=this.reflectivity),this.refractionRatio!==void 0&&(i.refractionRatio=this.refractionRatio),this.gradientMap&&this.gradientMap.isTexture&&(i.gradientMap=this.gradientMap.toJSON(e).uuid),this.transmission!==void 0&&(i.transmission=this.transmission),this.transmissionMap&&this.transmissionMap.isTexture&&(i.transmissionMap=this.transmissionMap.toJSON(e).uuid),this.thickness!==void 0&&(i.thickness=this.thickness),this.thicknessMap&&this.thicknessMap.isTexture&&(i.thicknessMap=this.thicknessMap.toJSON(e).uuid),this.attenuationDistance!==void 0&&this.attenuationDistance!==1/0&&(i.attenuationDistance=this.attenuationDistance),this.attenuationColor!==void 0&&(i.attenuationColor=this.attenuationColor.getHex()),this.size!==void 0&&(i.size=this.size),this.shadowSide!==null&&(i.shadowSide=this.shadowSide),this.sizeAttenuation!==void 0&&(i.sizeAttenuation=this.sizeAttenuation),this.blending!==Si&&(i.blending=this.blending),this.side!==Ln&&(i.side=this.side),this.vertexColors===!0&&(i.vertexColors=!0),this.opacity<1&&(i.opacity=this.opacity),this.transparent===!0&&(i.transparent=!0),this.blendSrc!==Ia&&(i.blendSrc=this.blendSrc),this.blendDst!==Ua&&(i.blendDst=this.blendDst),this.blendEquation!==Kn&&(i.blendEquation=this.blendEquation),this.blendSrcAlpha!==null&&(i.blendSrcAlpha=this.blendSrcAlpha),this.blendDstAlpha!==null&&(i.blendDstAlpha=this.blendDstAlpha),this.blendEquationAlpha!==null&&(i.blendEquationAlpha=this.blendEquationAlpha),this.blendColor&&this.blendColor.isColor&&(i.blendColor=this.blendColor.getHex()),this.blendAlpha!==0&&(i.blendAlpha=this.blendAlpha),this.depthFunc!==yi&&(i.depthFunc=this.depthFunc),this.depthTest===!1&&(i.depthTest=this.depthTest),this.depthWrite===!1&&(i.depthWrite=this.depthWrite),this.colorWrite===!1&&(i.colorWrite=this.colorWrite),this.stencilWriteMask!==255&&(i.stencilWriteMask=this.stencilWriteMask),this.stencilFunc!==ao&&(i.stencilFunc=this.stencilFunc),this.stencilRef!==0&&(i.stencilRef=this.stencilRef),this.stencilFuncMask!==255&&(i.stencilFuncMask=this.stencilFuncMask),this.stencilFail!==ni&&(i.stencilFail=this.stencilFail),this.stencilZFail!==ni&&(i.stencilZFail=this.stencilZFail),this.stencilZPass!==ni&&(i.stencilZPass=this.stencilZPass),this.stencilWrite===!0&&(i.stencilWrite=this.stencilWrite),this.rotation!==void 0&&this.rotation!==0&&(i.rotation=this.rotation),this.polygonOffset===!0&&(i.polygonOffset=!0),this.polygonOffsetFactor!==0&&(i.polygonOffsetFactor=this.polygonOffsetFactor),this.polygonOffsetUnits!==0&&(i.polygonOffsetUnits=this.polygonOffsetUnits),this.linewidth!==void 0&&this.linewidth!==1&&(i.linewidth=this.linewidth),this.dashSize!==void 0&&(i.dashSize=this.dashSize),this.gapSize!==void 0&&(i.gapSize=this.gapSize),this.scale!==void 0&&(i.scale=this.scale),this.dithering===!0&&(i.dithering=!0),this.alphaTest>0&&(i.alphaTest=this.alphaTest),this.alphaHash===!0&&(i.alphaHash=!0),this.alphaToCoverage===!0&&(i.alphaToCoverage=!0),this.premultipliedAlpha===!0&&(i.premultipliedAlpha=!0),this.forceSinglePass===!0&&(i.forceSinglePass=!0),this.wireframe===!0&&(i.wireframe=!0),this.wireframeLinewidth>1&&(i.wireframeLinewidth=this.wireframeLinewidth),this.wireframeLinecap!=="round"&&(i.wireframeLinecap=this.wireframeLinecap),this.wireframeLinejoin!=="round"&&(i.wireframeLinejoin=this.wireframeLinejoin),this.flatShading===!0&&(i.flatShading=!0),this.visible===!1&&(i.visible=!1),this.toneMapped===!1&&(i.toneMapped=!1),this.fog===!1&&(i.fog=!1),Object.keys(this.userData).length>0&&(i.userData=this.userData);function r(a){const s=[];for(const o in a){const c=a[o];delete c.metadata,s.push(c)}return s}if(t){const a=r(e.textures),s=r(e.images);a.length>0&&(i.textures=a),s.length>0&&(i.images=s)}return i}clone(){return new this.constructor().copy(this)}copy(e){this.name=e.name,this.blending=e.blending,this.side=e.side,this.vertexColors=e.vertexColors,this.opacity=e.opacity,this.transparent=e.transparent,this.blendSrc=e.blendSrc,this.blendDst=e.blendDst,this.blendEquation=e.blendEquation,this.blendSrcAlpha=e.blendSrcAlpha,this.blendDstAlpha=e.blendDstAlpha,this.blendEquationAlpha=e.blendEquationAlpha,this.blendColor.copy(e.blendColor),this.blendAlpha=e.blendAlpha,this.depthFunc=e.depthFunc,this.depthTest=e.depthTest,this.depthWrite=e.depthWrite,this.stencilWriteMask=e.stencilWriteMask,this.stencilFunc=e.stencilFunc,this.stencilRef=e.stencilRef,this.stencilFuncMask=e.stencilFuncMask,this.stencilFail=e.stencilFail,this.stencilZFail=e.stencilZFail,this.stencilZPass=e.stencilZPass,this.stencilWrite=e.stencilWrite;const t=e.clippingPlanes;let i=null;if(t!==null){const r=t.length;i=new Array(r);for(let a=0;a!==r;++a)i[a]=t[a].clone()}return this.clippingPlanes=i,this.clipIntersection=e.clipIntersection,this.clipShadows=e.clipShadows,this.shadowSide=e.shadowSide,this.colorWrite=e.colorWrite,this.precision=e.precision,this.polygonOffset=e.polygonOffset,this.polygonOffsetFactor=e.polygonOffsetFactor,this.polygonOffsetUnits=e.polygonOffsetUnits,this.dithering=e.dithering,this.alphaTest=e.alphaTest,this.alphaHash=e.alphaHash,this.alphaToCoverage=e.alphaToCoverage,this.premultipliedAlpha=e.premultipliedAlpha,this.forceSinglePass=e.forceSinglePass,this.visible=e.visible,this.toneMapped=e.toneMapped,this.userData=JSON.parse(JSON.stringify(e.userData)),this}dispose(){this.dispatchEvent({type:"dispose"})}set needsUpdate(e){e===!0&&this.version++}onBuild(){console.warn("Material: onBuild() has been removed.")}}class Ui extends Ii{constructor(e){super(),this.isMeshBasicMaterial=!0,this.type="MeshBasicMaterial",this.color=new ce(16777215),this.map=null,this.lightMap=null,this.lightMapIntensity=1,this.aoMap=null,this.aoMapIntensity=1,this.specularMap=null,this.alphaMap=null,this.envMap=null,this.envMapRotation=new mt,this.combine=vc,this.reflectivity=1,this.refractionRatio=.98,this.wireframe=!1,this.wireframeLinewidth=1,this.wireframeLinecap="round",this.wireframeLinejoin="round",this.fog=!0,this.setValues(e)}copy(e){return super.copy(e),this.color.copy(e.color),this.map=e.map,this.lightMap=e.lightMap,this.lightMapIntensity=e.lightMapIntensity,this.aoMap=e.aoMap,this.aoMapIntensity=e.aoMapIntensity,this.specularMap=e.specularMap,this.alphaMap=e.alphaMap,this.envMap=e.envMap,this.envMapRotation.copy(e.envMapRotation),this.combine=e.combine,this.reflectivity=e.reflectivity,this.refractionRatio=e.refractionRatio,this.wireframe=e.wireframe,this.wireframeLinewidth=e.wireframeLinewidth,this.wireframeLinecap=e.wireframeLinecap,this.wireframeLinejoin=e.wireframeLinejoin,this.fog=e.fog,this}}const pt=new F,ur=new Ke;let xu=0;class nn{constructor(e,t,i=!1){if(Array.isArray(e))throw new TypeError("THREE.BufferAttribute: array should be a Typed Array.");this.isBufferAttribute=!0,Object.defineProperty(this,"id",{value:xu++}),this.name="",this.array=e,this.itemSize=t,this.count=e!==void 0?e.length/t:0,this.normalized=i,this.usage=so,this.updateRanges=[],this.gpuType=pn,this.version=0}onUploadCallback(){}set needsUpdate(e){e===!0&&this.version++}setUsage(e){return this.usage=e,this}addUpdateRange(e,t){this.updateRanges.push({start:e,count:t})}clearUpdateRanges(){this.updateRanges.length=0}copy(e){return this.name=e.name,this.array=new e.array.constructor(e.array),this.itemSize=e.itemSize,this.count=e.count,this.normalized=e.normalized,this.usage=e.usage,this.gpuType=e.gpuType,this}copyAt(e,t,i){e*=this.itemSize,i*=t.itemSize;for(let r=0,a=this.itemSize;r<a;r++)this.array[e+r]=t.array[i+r];return this}copyArray(e){return this.array.set(e),this}applyMatrix3(e){if(this.itemSize===2)for(let t=0,i=this.count;t<i;t++)ur.fromBufferAttribute(this,t),ur.applyMatrix3(e),this.setXY(t,ur.x,ur.y);else if(this.itemSize===3)for(let t=0,i=this.count;t<i;t++)pt.fromBufferAttribute(this,t),pt.applyMatrix3(e),this.setXYZ(t,pt.x,pt.y,pt.z);return this}applyMatrix4(e){for(let t=0,i=this.count;t<i;t++)pt.fromBufferAttribute(this,t),pt.applyMatrix4(e),this.setXYZ(t,pt.x,pt.y,pt.z);return this}applyNormalMatrix(e){for(let t=0,i=this.count;t<i;t++)pt.fromBufferAttribute(this,t),pt.applyNormalMatrix(e),this.setXYZ(t,pt.x,pt.y,pt.z);return this}transformDirection(e){for(let t=0,i=this.count;t<i;t++)pt.fromBufferAttribute(this,t),pt.transformDirection(e),this.setXYZ(t,pt.x,pt.y,pt.z);return this}set(e,t=0){return this.array.set(e,t),this}getComponent(e,t){let i=this.array[e*this.itemSize+t];return this.normalized&&(i=Fi(i,this.array)),i}setComponent(e,t,i){return this.normalized&&(i=Dt(i,this.array)),this.array[e*this.itemSize+t]=i,this}getX(e){let t=this.array[e*this.itemSize];return this.normalized&&(t=Fi(t,this.array)),t}setX(e,t){return this.normalized&&(t=Dt(t,this.array)),this.array[e*this.itemSize]=t,this}getY(e){let t=this.array[e*this.itemSize+1];return this.normalized&&(t=Fi(t,this.array)),t}setY(e,t){return this.normalized&&(t=Dt(t,this.array)),this.array[e*this.itemSize+1]=t,this}getZ(e){let t=this.array[e*this.itemSize+2];return this.normalized&&(t=Fi(t,this.array)),t}setZ(e,t){return this.normalized&&(t=Dt(t,this.array)),this.array[e*this.itemSize+2]=t,this}getW(e){let t=this.array[e*this.itemSize+3];return this.normalized&&(t=Fi(t,this.array)),t}setW(e,t){return this.normalized&&(t=Dt(t,this.array)),this.array[e*this.itemSize+3]=t,this}setXY(e,t,i){return e*=this.itemSize,this.normalized&&(t=Dt(t,this.array),i=Dt(i,this.array)),this.array[e+0]=t,this.array[e+1]=i,this}setXYZ(e,t,i,r){return e*=this.itemSize,this.normalized&&(t=Dt(t,this.array),i=Dt(i,this.array),r=Dt(r,this.array)),this.array[e+0]=t,this.array[e+1]=i,this.array[e+2]=r,this}setXYZW(e,t,i,r,a){return e*=this.itemSize,this.normalized&&(t=Dt(t,this.array),i=Dt(i,this.array),r=Dt(r,this.array),a=Dt(a,this.array)),this.array[e+0]=t,this.array[e+1]=i,this.array[e+2]=r,this.array[e+3]=a,this}onUpload(e){return this.onUploadCallback=e,this}clone(){return new this.constructor(this.array,this.itemSize).copy(this)}toJSON(){const e={itemSize:this.itemSize,type:this.array.constructor.name,array:Array.from(this.array),normalized:this.normalized};return this.name!==""&&(e.name=this.name),this.usage!==so&&(e.usage=this.usage),e}}class zc extends nn{constructor(e,t,i){super(new Uint16Array(e),t,i)}}class Nc extends nn{constructor(e,t,i){super(new Uint32Array(e),t,i)}}class He extends nn{constructor(e,t,i){super(new Float32Array(e),t,i)}}let Mu=0;const Vt=new ct,pa=new Et,hi=new F,Nt=new Zi,Vi=new Zi,xt=new F;class Ze extends Di{constructor(){super(),this.isBufferGeometry=!0,Object.defineProperty(this,"id",{value:Mu++}),this.uuid=Yi(),this.name="",this.type="BufferGeometry",this.index=null,this.indirect=null,this.attributes={},this.morphAttributes={},this.morphTargetsRelative=!1,this.groups=[],this.boundingBox=null,this.boundingSphere=null,this.drawRange={start:0,count:1/0},this.userData={}}getIndex(){return this.index}setIndex(e){return Array.isArray(e)?this.index=new(Lc(e)?Nc:zc)(e,1):this.index=e,this}setIndirect(e){return this.indirect=e,this}getIndirect(){return this.indirect}getAttribute(e){return this.attributes[e]}setAttribute(e,t){return this.attributes[e]=t,this}deleteAttribute(e){return delete this.attributes[e],this}hasAttribute(e){return this.attributes[e]!==void 0}addGroup(e,t,i=0){this.groups.push({start:e,count:t,materialIndex:i})}clearGroups(){this.groups=[]}setDrawRange(e,t){this.drawRange.start=e,this.drawRange.count=t}applyMatrix4(e){const t=this.attributes.position;t!==void 0&&(t.applyMatrix4(e),t.needsUpdate=!0);const i=this.attributes.normal;if(i!==void 0){const a=new Be().getNormalMatrix(e);i.applyNormalMatrix(a),i.needsUpdate=!0}const r=this.attributes.tangent;return r!==void 0&&(r.transformDirection(e),r.needsUpdate=!0),this.boundingBox!==null&&this.computeBoundingBox(),this.boundingSphere!==null&&this.computeBoundingSphere(),this}applyQuaternion(e){return Vt.makeRotationFromQuaternion(e),this.applyMatrix4(Vt),this}rotateX(e){return Vt.makeRotationX(e),this.applyMatrix4(Vt),this}rotateY(e){return Vt.makeRotationY(e),this.applyMatrix4(Vt),this}rotateZ(e){return Vt.makeRotationZ(e),this.applyMatrix4(Vt),this}translate(e,t,i){return Vt.makeTranslation(e,t,i),this.applyMatrix4(Vt),this}scale(e,t,i){return Vt.makeScale(e,t,i),this.applyMatrix4(Vt),this}lookAt(e){return pa.lookAt(e),pa.updateMatrix(),this.applyMatrix4(pa.matrix),this}center(){return this.computeBoundingBox(),this.boundingBox.getCenter(hi).negate(),this.translate(hi.x,hi.y,hi.z),this}setFromPoints(e){const t=this.getAttribute("position");if(t===void 0){const i=[];for(let r=0,a=e.length;r<a;r++){const s=e[r];i.push(s.x,s.y,s.z||0)}this.setAttribute("position",new He(i,3))}else{const i=Math.min(e.length,t.count);for(let r=0;r<i;r++){const a=e[r];t.setXYZ(r,a.x,a.y,a.z||0)}e.length>t.count&&console.warn("THREE.BufferGeometry: Buffer size too small for points data. Use .dispose() and create a new geometry."),t.needsUpdate=!0}return this}computeBoundingBox(){this.boundingBox===null&&(this.boundingBox=new Zi);const e=this.attributes.position,t=this.morphAttributes.position;if(e&&e.isGLBufferAttribute){console.error("THREE.BufferGeometry.computeBoundingBox(): GLBufferAttribute requires a manual bounding box.",this),this.boundingBox.set(new F(-1/0,-1/0,-1/0),new F(1/0,1/0,1/0));return}if(e!==void 0){if(this.boundingBox.setFromBufferAttribute(e),t)for(let i=0,r=t.length;i<r;i++){const a=t[i];Nt.setFromBufferAttribute(a),this.morphTargetsRelative?(xt.addVectors(this.boundingBox.min,Nt.min),this.boundingBox.expandByPoint(xt),xt.addVectors(this.boundingBox.max,Nt.max),this.boundingBox.expandByPoint(xt)):(this.boundingBox.expandByPoint(Nt.min),this.boundingBox.expandByPoint(Nt.max))}}else this.boundingBox.makeEmpty();(isNaN(this.boundingBox.min.x)||isNaN(this.boundingBox.min.y)||isNaN(this.boundingBox.min.z))&&console.error('THREE.BufferGeometry.computeBoundingBox(): Computed min/max have NaN values. The "position" attribute is likely to have NaN values.',this)}computeBoundingSphere(){this.boundingSphere===null&&(this.boundingSphere=new Hr);const e=this.attributes.position,t=this.morphAttributes.position;if(e&&e.isGLBufferAttribute){console.error("THREE.BufferGeometry.computeBoundingSphere(): GLBufferAttribute requires a manual bounding sphere.",this),this.boundingSphere.set(new F,1/0);return}if(e){const i=this.boundingSphere.center;if(Nt.setFromBufferAttribute(e),t)for(let a=0,s=t.length;a<s;a++){const o=t[a];Vi.setFromBufferAttribute(o),this.morphTargetsRelative?(xt.addVectors(Nt.min,Vi.min),Nt.expandByPoint(xt),xt.addVectors(Nt.max,Vi.max),Nt.expandByPoint(xt)):(Nt.expandByPoint(Vi.min),Nt.expandByPoint(Vi.max))}Nt.getCenter(i);let r=0;for(let a=0,s=e.count;a<s;a++)xt.fromBufferAttribute(e,a),r=Math.max(r,i.distanceToSquared(xt));if(t)for(let a=0,s=t.length;a<s;a++){const o=t[a],c=this.morphTargetsRelative;for(let l=0,d=o.count;l<d;l++)xt.fromBufferAttribute(o,l),c&&(hi.fromBufferAttribute(e,l),xt.add(hi)),r=Math.max(r,i.distanceToSquared(xt))}this.boundingSphere.radius=Math.sqrt(r),isNaN(this.boundingSphere.radius)&&console.error('THREE.BufferGeometry.computeBoundingSphere(): Computed radius is NaN. The "position" attribute is likely to have NaN values.',this)}}computeTangents(){const e=this.index,t=this.attributes;if(e===null||t.position===void 0||t.normal===void 0||t.uv===void 0){console.error("THREE.BufferGeometry: .computeTangents() failed. Missing required attributes (index, position, normal or uv)");return}const i=t.position,r=t.normal,a=t.uv;this.hasAttribute("tangent")===!1&&this.setAttribute("tangent",new nn(new Float32Array(4*i.count),4));const s=this.getAttribute("tangent"),o=[],c=[];for(let L=0;L<i.count;L++)o[L]=new F,c[L]=new F;const l=new F,d=new F,h=new F,f=new Ke,m=new Ke,g=new Ke,_=new F,p=new F;function u(L,x,v){l.fromBufferAttribute(i,L),d.fromBufferAttribute(i,x),h.fromBufferAttribute(i,v),f.fromBufferAttribute(a,L),m.fromBufferAttribute(a,x),g.fromBufferAttribute(a,v),d.sub(l),h.sub(l),m.sub(f),g.sub(f);const R=1/(m.x*g.y-g.x*m.y);isFinite(R)&&(_.copy(d).multiplyScalar(g.y).addScaledVector(h,-m.y).multiplyScalar(R),p.copy(h).multiplyScalar(m.x).addScaledVector(d,-g.x).multiplyScalar(R),o[L].add(_),o[x].add(_),o[v].add(_),c[L].add(p),c[x].add(p),c[v].add(p))}let b=this.groups;b.length===0&&(b=[{start:0,count:e.count}]);for(let L=0,x=b.length;L<x;++L){const v=b[L],R=v.start,U=v.count;for(let C=R,D=R+U;C<D;C+=3)u(e.getX(C+0),e.getX(C+1),e.getX(C+2))}const S=new F,M=new F,w=new F,T=new F;function A(L){w.fromBufferAttribute(r,L),T.copy(w);const x=o[L];S.copy(x),S.sub(w.multiplyScalar(w.dot(x))).normalize(),M.crossVectors(T,x);const R=M.dot(c[L])<0?-1:1;s.setXYZW(L,S.x,S.y,S.z,R)}for(let L=0,x=b.length;L<x;++L){const v=b[L],R=v.start,U=v.count;for(let C=R,D=R+U;C<D;C+=3)A(e.getX(C+0)),A(e.getX(C+1)),A(e.getX(C+2))}}computeVertexNormals(){const e=this.index,t=this.getAttribute("position");if(t!==void 0){let i=this.getAttribute("normal");if(i===void 0)i=new nn(new Float32Array(t.count*3),3),this.setAttribute("normal",i);else for(let f=0,m=i.count;f<m;f++)i.setXYZ(f,0,0,0);const r=new F,a=new F,s=new F,o=new F,c=new F,l=new F,d=new F,h=new F;if(e)for(let f=0,m=e.count;f<m;f+=3){const g=e.getX(f+0),_=e.getX(f+1),p=e.getX(f+2);r.fromBufferAttribute(t,g),a.fromBufferAttribute(t,_),s.fromBufferAttribute(t,p),d.subVectors(s,a),h.subVectors(r,a),d.cross(h),o.fromBufferAttribute(i,g),c.fromBufferAttribute(i,_),l.fromBufferAttribute(i,p),o.add(d),c.add(d),l.add(d),i.setXYZ(g,o.x,o.y,o.z),i.setXYZ(_,c.x,c.y,c.z),i.setXYZ(p,l.x,l.y,l.z)}else for(let f=0,m=t.count;f<m;f+=3)r.fromBufferAttribute(t,f+0),a.fromBufferAttribute(t,f+1),s.fromBufferAttribute(t,f+2),d.subVectors(s,a),h.subVectors(r,a),d.cross(h),i.setXYZ(f+0,d.x,d.y,d.z),i.setXYZ(f+1,d.x,d.y,d.z),i.setXYZ(f+2,d.x,d.y,d.z);this.normalizeNormals(),i.needsUpdate=!0}}normalizeNormals(){const e=this.attributes.normal;for(let t=0,i=e.count;t<i;t++)xt.fromBufferAttribute(e,t),xt.normalize(),e.setXYZ(t,xt.x,xt.y,xt.z)}toNonIndexed(){function e(o,c){const l=o.array,d=o.itemSize,h=o.normalized,f=new l.constructor(c.length*d);let m=0,g=0;for(let _=0,p=c.length;_<p;_++){o.isInterleavedBufferAttribute?m=c[_]*o.data.stride+o.offset:m=c[_]*d;for(let u=0;u<d;u++)f[g++]=l[m++]}return new nn(f,d,h)}if(this.index===null)return console.warn("THREE.BufferGeometry.toNonIndexed(): BufferGeometry is already non-indexed."),this;const t=new Ze,i=this.index.array,r=this.attributes;for(const o in r){const c=r[o],l=e(c,i);t.setAttribute(o,l)}const a=this.morphAttributes;for(const o in a){const c=[],l=a[o];for(let d=0,h=l.length;d<h;d++){const f=l[d],m=e(f,i);c.push(m)}t.morphAttributes[o]=c}t.morphTargetsRelative=this.morphTargetsRelative;const s=this.groups;for(let o=0,c=s.length;o<c;o++){const l=s[o];t.addGroup(l.start,l.count,l.materialIndex)}return t}toJSON(){const e={metadata:{version:4.6,type:"BufferGeometry",generator:"BufferGeometry.toJSON"}};if(e.uuid=this.uuid,e.type=this.type,this.name!==""&&(e.name=this.name),Object.keys(this.userData).length>0&&(e.userData=this.userData),this.parameters!==void 0){const c=this.parameters;for(const l in c)c[l]!==void 0&&(e[l]=c[l]);return e}e.data={attributes:{}};const t=this.index;t!==null&&(e.data.index={type:t.array.constructor.name,array:Array.prototype.slice.call(t.array)});const i=this.attributes;for(const c in i){const l=i[c];e.data.attributes[c]=l.toJSON(e.data)}const r={};let a=!1;for(const c in this.morphAttributes){const l=this.morphAttributes[c],d=[];for(let h=0,f=l.length;h<f;h++){const m=l[h];d.push(m.toJSON(e.data))}d.length>0&&(r[c]=d,a=!0)}a&&(e.data.morphAttributes=r,e.data.morphTargetsRelative=this.morphTargetsRelative);const s=this.groups;s.length>0&&(e.data.groups=JSON.parse(JSON.stringify(s)));const o=this.boundingSphere;return o!==null&&(e.data.boundingSphere={center:o.center.toArray(),radius:o.radius}),e}clone(){return new this.constructor().copy(this)}copy(e){this.index=null,this.attributes={},this.morphAttributes={},this.groups=[],this.boundingBox=null,this.boundingSphere=null;const t={};this.name=e.name;const i=e.index;i!==null&&this.setIndex(i.clone(t));const r=e.attributes;for(const l in r){const d=r[l];this.setAttribute(l,d.clone(t))}const a=e.morphAttributes;for(const l in a){const d=[],h=a[l];for(let f=0,m=h.length;f<m;f++)d.push(h[f].clone(t));this.morphAttributes[l]=d}this.morphTargetsRelative=e.morphTargetsRelative;const s=e.groups;for(let l=0,d=s.length;l<d;l++){const h=s[l];this.addGroup(h.start,h.count,h.materialIndex)}const o=e.boundingBox;o!==null&&(this.boundingBox=o.clone());const c=e.boundingSphere;return c!==null&&(this.boundingSphere=c.clone()),this.drawRange.start=e.drawRange.start,this.drawRange.count=e.drawRange.count,this.userData=e.userData,this}dispose(){this.dispatchEvent({type:"dispose"})}}const So=new ct,Fn=new Ns,dr=new Hr,Eo=new F,hr=new F,fr=new F,pr=new F,ma=new F,mr=new F,bo=new F,gr=new F;class We extends Et{constructor(e=new Ze,t=new Ui){super(),this.isMesh=!0,this.type="Mesh",this.geometry=e,this.material=t,this.morphTargetDictionary=void 0,this.morphTargetInfluences=void 0,this.updateMorphTargets()}copy(e,t){return super.copy(e,t),e.morphTargetInfluences!==void 0&&(this.morphTargetInfluences=e.morphTargetInfluences.slice()),e.morphTargetDictionary!==void 0&&(this.morphTargetDictionary=Object.assign({},e.morphTargetDictionary)),this.material=Array.isArray(e.material)?e.material.slice():e.material,this.geometry=e.geometry,this}updateMorphTargets(){const t=this.geometry.morphAttributes,i=Object.keys(t);if(i.length>0){const r=t[i[0]];if(r!==void 0){this.morphTargetInfluences=[],this.morphTargetDictionary={};for(let a=0,s=r.length;a<s;a++){const o=r[a].name||String(a);this.morphTargetInfluences.push(0),this.morphTargetDictionary[o]=a}}}}getVertexPosition(e,t){const i=this.geometry,r=i.attributes.position,a=i.morphAttributes.position,s=i.morphTargetsRelative;t.fromBufferAttribute(r,e);const o=this.morphTargetInfluences;if(a&&o){mr.set(0,0,0);for(let c=0,l=a.length;c<l;c++){const d=o[c],h=a[c];d!==0&&(ma.fromBufferAttribute(h,e),s?mr.addScaledVector(ma,d):mr.addScaledVector(ma.sub(t),d))}t.add(mr)}return t}raycast(e,t){const i=this.geometry,r=this.material,a=this.matrixWorld;r!==void 0&&(i.boundingSphere===null&&i.computeBoundingSphere(),dr.copy(i.boundingSphere),dr.applyMatrix4(a),Fn.copy(e.ray).recast(e.near),!(dr.containsPoint(Fn.origin)===!1&&(Fn.intersectSphere(dr,Eo)===null||Fn.origin.distanceToSquared(Eo)>(e.far-e.near)**2))&&(So.copy(a).invert(),Fn.copy(e.ray).applyMatrix4(So),!(i.boundingBox!==null&&Fn.intersectsBox(i.boundingBox)===!1)&&this._computeIntersections(e,t,Fn)))}_computeIntersections(e,t,i){let r;const a=this.geometry,s=this.material,o=a.index,c=a.attributes.position,l=a.attributes.uv,d=a.attributes.uv1,h=a.attributes.normal,f=a.groups,m=a.drawRange;if(o!==null)if(Array.isArray(s))for(let g=0,_=f.length;g<_;g++){const p=f[g],u=s[p.materialIndex],b=Math.max(p.start,m.start),S=Math.min(o.count,Math.min(p.start+p.count,m.start+m.count));for(let M=b,w=S;M<w;M+=3){const T=o.getX(M),A=o.getX(M+1),L=o.getX(M+2);r=_r(this,u,e,i,l,d,h,T,A,L),r&&(r.faceIndex=Math.floor(M/3),r.face.materialIndex=p.materialIndex,t.push(r))}}else{const g=Math.max(0,m.start),_=Math.min(o.count,m.start+m.count);for(let p=g,u=_;p<u;p+=3){const b=o.getX(p),S=o.getX(p+1),M=o.getX(p+2);r=_r(this,s,e,i,l,d,h,b,S,M),r&&(r.faceIndex=Math.floor(p/3),t.push(r))}}else if(c!==void 0)if(Array.isArray(s))for(let g=0,_=f.length;g<_;g++){const p=f[g],u=s[p.materialIndex],b=Math.max(p.start,m.start),S=Math.min(c.count,Math.min(p.start+p.count,m.start+m.count));for(let M=b,w=S;M<w;M+=3){const T=M,A=M+1,L=M+2;r=_r(this,u,e,i,l,d,h,T,A,L),r&&(r.faceIndex=Math.floor(M/3),r.face.materialIndex=p.materialIndex,t.push(r))}}else{const g=Math.max(0,m.start),_=Math.min(c.count,m.start+m.count);for(let p=g,u=_;p<u;p+=3){const b=p,S=p+1,M=p+2;r=_r(this,s,e,i,l,d,h,b,S,M),r&&(r.faceIndex=Math.floor(p/3),t.push(r))}}}}function Su(n,e,t,i,r,a,s,o){let c;if(e.side===Lt?c=i.intersectTriangle(s,a,r,!0,o):c=i.intersectTriangle(r,a,s,e.side===Ln,o),c===null)return null;gr.copy(o),gr.applyMatrix4(n.matrixWorld);const l=t.ray.origin.distanceTo(gr);return l<t.near||l>t.far?null:{distance:l,point:gr.clone(),object:n}}function _r(n,e,t,i,r,a,s,o,c,l){n.getVertexPosition(o,hr),n.getVertexPosition(c,fr),n.getVertexPosition(l,pr);const d=Su(n,e,t,i,hr,fr,pr,bo);if(d){const h=new F;Gt.getBarycoord(bo,hr,fr,pr,h),r&&(d.uv=Gt.getInterpolatedAttribute(r,o,c,l,h,new Ke)),a&&(d.uv1=Gt.getInterpolatedAttribute(a,o,c,l,h,new Ke)),s&&(d.normal=Gt.getInterpolatedAttribute(s,o,c,l,h,new F),d.normal.dot(i.direction)>0&&d.normal.multiplyScalar(-1));const f={a:o,b:c,c:l,normal:new F,materialIndex:0};Gt.getNormal(hr,fr,pr,f.normal),d.face=f,d.barycoord=h}return d}class gn extends Ze{constructor(e=1,t=1,i=1,r=1,a=1,s=1){super(),this.type="BoxGeometry",this.parameters={width:e,height:t,depth:i,widthSegments:r,heightSegments:a,depthSegments:s};const o=this;r=Math.floor(r),a=Math.floor(a),s=Math.floor(s);const c=[],l=[],d=[],h=[];let f=0,m=0;g("z","y","x",-1,-1,i,t,e,s,a,0),g("z","y","x",1,-1,i,t,-e,s,a,1),g("x","z","y",1,1,e,i,t,r,s,2),g("x","z","y",1,-1,e,i,-t,r,s,3),g("x","y","z",1,-1,e,t,i,r,a,4),g("x","y","z",-1,-1,e,t,-i,r,a,5),this.setIndex(c),this.setAttribute("position",new He(l,3)),this.setAttribute("normal",new He(d,3)),this.setAttribute("uv",new He(h,2));function g(_,p,u,b,S,M,w,T,A,L,x){const v=M/A,R=w/L,U=M/2,C=w/2,D=T/2,k=A+1,N=L+1;let O=0,z=0;const H=new F;for(let q=0;q<N;q++){const J=q*R-C;for(let fe=0;fe<k;fe++){const Ae=fe*v-U;H[_]=Ae*b,H[p]=J*S,H[u]=D,l.push(H.x,H.y,H.z),H[_]=0,H[p]=0,H[u]=T>0?1:-1,d.push(H.x,H.y,H.z),h.push(fe/A),h.push(1-q/L),O+=1}}for(let q=0;q<L;q++)for(let J=0;J<A;J++){const fe=f+J+k*q,Ae=f+J+k*(q+1),K=f+(J+1)+k*(q+1),ne=f+(J+1)+k*q;c.push(fe,Ae,ne),c.push(Ae,K,ne),z+=6}o.addGroup(m,z,x),m+=z,f+=O}}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}static fromJSON(e){return new gn(e.width,e.height,e.depth,e.widthSegments,e.heightSegments,e.depthSegments)}}function Pi(n){const e={};for(const t in n){e[t]={};for(const i in n[t]){const r=n[t][i];r&&(r.isColor||r.isMatrix3||r.isMatrix4||r.isVector2||r.isVector3||r.isVector4||r.isTexture||r.isQuaternion)?r.isRenderTargetTexture?(console.warn("UniformsUtils: Textures of render targets cannot be cloned via cloneUniforms() or mergeUniforms()."),e[t][i]=null):e[t][i]=r.clone():Array.isArray(r)?e[t][i]=r.slice():e[t][i]=r}}return e}function Rt(n){const e={};for(let t=0;t<n.length;t++){const i=Pi(n[t]);for(const r in i)e[r]=i[r]}return e}function Eu(n){const e=[];for(let t=0;t<n.length;t++)e.push(n[t].clone());return e}function kc(n){const e=n.getRenderTarget();return e===null?n.outputColorSpace:e.isXRRenderTarget===!0?e.texture.colorSpace:Qe.workingColorSpace}const bu={clone:Pi,merge:Rt};var yu=`void main() {
	gl_Position = projectionMatrix * modelViewMatrix * vec4( position, 1.0 );
}`,Tu=`void main() {
	gl_FragColor = vec4( 1.0, 0.0, 0.0, 1.0 );
}`;class In extends Ii{constructor(e){super(),this.isShaderMaterial=!0,this.type="ShaderMaterial",this.defines={},this.uniforms={},this.uniformsGroups=[],this.vertexShader=yu,this.fragmentShader=Tu,this.linewidth=1,this.wireframe=!1,this.wireframeLinewidth=1,this.fog=!1,this.lights=!1,this.clipping=!1,this.forceSinglePass=!0,this.extensions={clipCullDistance:!1,multiDraw:!1},this.defaultAttributeValues={color:[1,1,1],uv:[0,0],uv1:[0,0]},this.index0AttributeName=void 0,this.uniformsNeedUpdate=!1,this.glslVersion=null,e!==void 0&&this.setValues(e)}copy(e){return super.copy(e),this.fragmentShader=e.fragmentShader,this.vertexShader=e.vertexShader,this.uniforms=Pi(e.uniforms),this.uniformsGroups=Eu(e.uniformsGroups),this.defines=Object.assign({},e.defines),this.wireframe=e.wireframe,this.wireframeLinewidth=e.wireframeLinewidth,this.fog=e.fog,this.lights=e.lights,this.clipping=e.clipping,this.extensions=Object.assign({},e.extensions),this.glslVersion=e.glslVersion,this}toJSON(e){const t=super.toJSON(e);t.glslVersion=this.glslVersion,t.uniforms={};for(const r in this.uniforms){const s=this.uniforms[r].value;s&&s.isTexture?t.uniforms[r]={type:"t",value:s.toJSON(e).uuid}:s&&s.isColor?t.uniforms[r]={type:"c",value:s.getHex()}:s&&s.isVector2?t.uniforms[r]={type:"v2",value:s.toArray()}:s&&s.isVector3?t.uniforms[r]={type:"v3",value:s.toArray()}:s&&s.isVector4?t.uniforms[r]={type:"v4",value:s.toArray()}:s&&s.isMatrix3?t.uniforms[r]={type:"m3",value:s.toArray()}:s&&s.isMatrix4?t.uniforms[r]={type:"m4",value:s.toArray()}:t.uniforms[r]={value:s}}Object.keys(this.defines).length>0&&(t.defines=this.defines),t.vertexShader=this.vertexShader,t.fragmentShader=this.fragmentShader,t.lights=this.lights,t.clipping=this.clipping;const i={};for(const r in this.extensions)this.extensions[r]===!0&&(i[r]=!0);return Object.keys(i).length>0&&(t.extensions=i),t}}class Fc extends Et{constructor(){super(),this.isCamera=!0,this.type="Camera",this.matrixWorldInverse=new ct,this.projectionMatrix=new ct,this.projectionMatrixInverse=new ct,this.coordinateSystem=mn}copy(e,t){return super.copy(e,t),this.matrixWorldInverse.copy(e.matrixWorldInverse),this.projectionMatrix.copy(e.projectionMatrix),this.projectionMatrixInverse.copy(e.projectionMatrixInverse),this.coordinateSystem=e.coordinateSystem,this}getWorldDirection(e){return super.getWorldDirection(e).negate()}updateMatrixWorld(e){super.updateMatrixWorld(e),this.matrixWorldInverse.copy(this.matrixWorld).invert()}updateWorldMatrix(e,t){super.updateWorldMatrix(e,t),this.matrixWorldInverse.copy(this.matrixWorld).invert()}clone(){return new this.constructor().copy(this)}}const Tn=new F,yo=new Ke,To=new Ke;class Ht extends Fc{constructor(e=50,t=1,i=.1,r=2e3){super(),this.isPerspectiveCamera=!0,this.type="PerspectiveCamera",this.fov=e,this.zoom=1,this.near=i,this.far=r,this.focus=10,this.aspect=t,this.view=null,this.filmGauge=35,this.filmOffset=0,this.updateProjectionMatrix()}copy(e,t){return super.copy(e,t),this.fov=e.fov,this.zoom=e.zoom,this.near=e.near,this.far=e.far,this.focus=e.focus,this.aspect=e.aspect,this.view=e.view===null?null:Object.assign({},e.view),this.filmGauge=e.filmGauge,this.filmOffset=e.filmOffset,this}setFocalLength(e){const t=.5*this.getFilmHeight()/e;this.fov=vs*2*Math.atan(t),this.updateProjectionMatrix()}getFocalLength(){const e=Math.tan(Ir*.5*this.fov);return .5*this.getFilmHeight()/e}getEffectiveFOV(){return vs*2*Math.atan(Math.tan(Ir*.5*this.fov)/this.zoom)}getFilmWidth(){return this.filmGauge*Math.min(this.aspect,1)}getFilmHeight(){return this.filmGauge/Math.max(this.aspect,1)}getViewBounds(e,t,i){Tn.set(-1,-1,.5).applyMatrix4(this.projectionMatrixInverse),t.set(Tn.x,Tn.y).multiplyScalar(-e/Tn.z),Tn.set(1,1,.5).applyMatrix4(this.projectionMatrixInverse),i.set(Tn.x,Tn.y).multiplyScalar(-e/Tn.z)}getViewSize(e,t){return this.getViewBounds(e,yo,To),t.subVectors(To,yo)}setViewOffset(e,t,i,r,a,s){this.aspect=e/t,this.view===null&&(this.view={enabled:!0,fullWidth:1,fullHeight:1,offsetX:0,offsetY:0,width:1,height:1}),this.view.enabled=!0,this.view.fullWidth=e,this.view.fullHeight=t,this.view.offsetX=i,this.view.offsetY=r,this.view.width=a,this.view.height=s,this.updateProjectionMatrix()}clearViewOffset(){this.view!==null&&(this.view.enabled=!1),this.updateProjectionMatrix()}updateProjectionMatrix(){const e=this.near;let t=e*Math.tan(Ir*.5*this.fov)/this.zoom,i=2*t,r=this.aspect*i,a=-.5*r;const s=this.view;if(this.view!==null&&this.view.enabled){const c=s.fullWidth,l=s.fullHeight;a+=s.offsetX*r/c,t-=s.offsetY*i/l,r*=s.width/c,i*=s.height/l}const o=this.filmOffset;o!==0&&(a+=e*o/this.getFilmWidth()),this.projectionMatrix.makePerspective(a,a+r,t,t-i,e,this.far,this.coordinateSystem),this.projectionMatrixInverse.copy(this.projectionMatrix).invert()}toJSON(e){const t=super.toJSON(e);return t.object.fov=this.fov,t.object.zoom=this.zoom,t.object.near=this.near,t.object.far=this.far,t.object.focus=this.focus,t.object.aspect=this.aspect,this.view!==null&&(t.object.view=Object.assign({},this.view)),t.object.filmGauge=this.filmGauge,t.object.filmOffset=this.filmOffset,t}}const fi=-90,pi=1;class wu extends Et{constructor(e,t,i){super(),this.type="CubeCamera",this.renderTarget=i,this.coordinateSystem=null,this.activeMipmapLevel=0;const r=new Ht(fi,pi,e,t);r.layers=this.layers,this.add(r);const a=new Ht(fi,pi,e,t);a.layers=this.layers,this.add(a);const s=new Ht(fi,pi,e,t);s.layers=this.layers,this.add(s);const o=new Ht(fi,pi,e,t);o.layers=this.layers,this.add(o);const c=new Ht(fi,pi,e,t);c.layers=this.layers,this.add(c);const l=new Ht(fi,pi,e,t);l.layers=this.layers,this.add(l)}updateCoordinateSystem(){const e=this.coordinateSystem,t=this.children.concat(),[i,r,a,s,o,c]=t;for(const l of t)this.remove(l);if(e===mn)i.up.set(0,1,0),i.lookAt(1,0,0),r.up.set(0,1,0),r.lookAt(-1,0,0),a.up.set(0,0,-1),a.lookAt(0,1,0),s.up.set(0,0,1),s.lookAt(0,-1,0),o.up.set(0,1,0),o.lookAt(0,0,1),c.up.set(0,1,0),c.lookAt(0,0,-1);else if(e===kr)i.up.set(0,-1,0),i.lookAt(-1,0,0),r.up.set(0,-1,0),r.lookAt(1,0,0),a.up.set(0,0,1),a.lookAt(0,1,0),s.up.set(0,0,-1),s.lookAt(0,-1,0),o.up.set(0,-1,0),o.lookAt(0,0,1),c.up.set(0,-1,0),c.lookAt(0,0,-1);else throw new Error("THREE.CubeCamera.updateCoordinateSystem(): Invalid coordinate system: "+e);for(const l of t)this.add(l),l.updateMatrixWorld()}update(e,t){this.parent===null&&this.updateMatrixWorld();const{renderTarget:i,activeMipmapLevel:r}=this;this.coordinateSystem!==e.coordinateSystem&&(this.coordinateSystem=e.coordinateSystem,this.updateCoordinateSystem());const[a,s,o,c,l,d]=this.children,h=e.getRenderTarget(),f=e.getActiveCubeFace(),m=e.getActiveMipmapLevel(),g=e.xr.enabled;e.xr.enabled=!1;const _=i.texture.generateMipmaps;i.texture.generateMipmaps=!1,e.setRenderTarget(i,0,r),e.render(t,a),e.setRenderTarget(i,1,r),e.render(t,s),e.setRenderTarget(i,2,r),e.render(t,o),e.setRenderTarget(i,3,r),e.render(t,c),e.setRenderTarget(i,4,r),e.render(t,l),i.texture.generateMipmaps=_,e.setRenderTarget(i,5,r),e.render(t,d),e.setRenderTarget(h,f,m),e.xr.enabled=g,i.texture.needsPMREMUpdate=!0}}class Oc extends Ct{constructor(e,t,i,r,a,s,o,c,l,d){e=e!==void 0?e:[],t=t!==void 0?t:Ti,super(e,t,i,r,a,s,o,c,l,d),this.isCubeTexture=!0,this.flipY=!1}get images(){return this.image}set images(e){this.image=e}}class Au extends ei{constructor(e=1,t={}){super(e,e,t),this.isWebGLCubeRenderTarget=!0;const i={width:e,height:e,depth:1},r=[i,i,i,i,i,i];this.texture=new Oc(r,t.mapping,t.wrapS,t.wrapT,t.magFilter,t.minFilter,t.format,t.type,t.anisotropy,t.colorSpace),this.texture.isRenderTargetTexture=!0,this.texture.generateMipmaps=t.generateMipmaps!==void 0?t.generateMipmaps:!1,this.texture.minFilter=t.minFilter!==void 0?t.minFilter:tn}fromEquirectangularTexture(e,t){this.texture.type=t.type,this.texture.colorSpace=t.colorSpace,this.texture.generateMipmaps=t.generateMipmaps,this.texture.minFilter=t.minFilter,this.texture.magFilter=t.magFilter;const i={uniforms:{tEquirect:{value:null}},vertexShader:`

				varying vec3 vWorldDirection;

				vec3 transformDirection( in vec3 dir, in mat4 matrix ) {

					return normalize( ( matrix * vec4( dir, 0.0 ) ).xyz );

				}

				void main() {

					vWorldDirection = transformDirection( position, modelMatrix );

					#include <begin_vertex>
					#include <project_vertex>

				}
			`,fragmentShader:`

				uniform sampler2D tEquirect;

				varying vec3 vWorldDirection;

				#include <common>

				void main() {

					vec3 direction = normalize( vWorldDirection );

					vec2 sampleUV = equirectUv( direction );

					gl_FragColor = texture2D( tEquirect, sampleUV );

				}
			`},r=new gn(5,5,5),a=new In({name:"CubemapFromEquirect",uniforms:Pi(i.uniforms),vertexShader:i.vertexShader,fragmentShader:i.fragmentShader,side:Lt,blending:Pn});a.uniforms.tEquirect.value=t;const s=new We(r,a),o=t.minFilter;return t.minFilter===Yn&&(t.minFilter=tn),new wu(1,10,this).update(e,s),t.minFilter=o,s.geometry.dispose(),s.material.dispose(),this}clear(e,t,i,r){const a=e.getRenderTarget();for(let s=0;s<6;s++)e.setRenderTarget(this,s),e.clear(t,i,r);e.setRenderTarget(a)}}class it extends Et{constructor(){super(),this.isGroup=!0,this.type="Group"}}const Ru={type:"move"};class ga{constructor(){this._targetRay=null,this._grip=null,this._hand=null}getHandSpace(){return this._hand===null&&(this._hand=new it,this._hand.matrixAutoUpdate=!1,this._hand.visible=!1,this._hand.joints={},this._hand.inputState={pinching:!1}),this._hand}getTargetRaySpace(){return this._targetRay===null&&(this._targetRay=new it,this._targetRay.matrixAutoUpdate=!1,this._targetRay.visible=!1,this._targetRay.hasLinearVelocity=!1,this._targetRay.linearVelocity=new F,this._targetRay.hasAngularVelocity=!1,this._targetRay.angularVelocity=new F),this._targetRay}getGripSpace(){return this._grip===null&&(this._grip=new it,this._grip.matrixAutoUpdate=!1,this._grip.visible=!1,this._grip.hasLinearVelocity=!1,this._grip.linearVelocity=new F,this._grip.hasAngularVelocity=!1,this._grip.angularVelocity=new F),this._grip}dispatchEvent(e){return this._targetRay!==null&&this._targetRay.dispatchEvent(e),this._grip!==null&&this._grip.dispatchEvent(e),this._hand!==null&&this._hand.dispatchEvent(e),this}connect(e){if(e&&e.hand){const t=this._hand;if(t)for(const i of e.hand.values())this._getHandJoint(t,i)}return this.dispatchEvent({type:"connected",data:e}),this}disconnect(e){return this.dispatchEvent({type:"disconnected",data:e}),this._targetRay!==null&&(this._targetRay.visible=!1),this._grip!==null&&(this._grip.visible=!1),this._hand!==null&&(this._hand.visible=!1),this}update(e,t,i){let r=null,a=null,s=null;const o=this._targetRay,c=this._grip,l=this._hand;if(e&&t.session.visibilityState!=="visible-blurred"){if(l&&e.hand){s=!0;for(const _ of e.hand.values()){const p=t.getJointPose(_,i),u=this._getHandJoint(l,_);p!==null&&(u.matrix.fromArray(p.transform.matrix),u.matrix.decompose(u.position,u.rotation,u.scale),u.matrixWorldNeedsUpdate=!0,u.jointRadius=p.radius),u.visible=p!==null}const d=l.joints["index-finger-tip"],h=l.joints["thumb-tip"],f=d.position.distanceTo(h.position),m=.02,g=.005;l.inputState.pinching&&f>m+g?(l.inputState.pinching=!1,this.dispatchEvent({type:"pinchend",handedness:e.handedness,target:this})):!l.inputState.pinching&&f<=m-g&&(l.inputState.pinching=!0,this.dispatchEvent({type:"pinchstart",handedness:e.handedness,target:this}))}else c!==null&&e.gripSpace&&(a=t.getPose(e.gripSpace,i),a!==null&&(c.matrix.fromArray(a.transform.matrix),c.matrix.decompose(c.position,c.rotation,c.scale),c.matrixWorldNeedsUpdate=!0,a.linearVelocity?(c.hasLinearVelocity=!0,c.linearVelocity.copy(a.linearVelocity)):c.hasLinearVelocity=!1,a.angularVelocity?(c.hasAngularVelocity=!0,c.angularVelocity.copy(a.angularVelocity)):c.hasAngularVelocity=!1));o!==null&&(r=t.getPose(e.targetRaySpace,i),r===null&&a!==null&&(r=a),r!==null&&(o.matrix.fromArray(r.transform.matrix),o.matrix.decompose(o.position,o.rotation,o.scale),o.matrixWorldNeedsUpdate=!0,r.linearVelocity?(o.hasLinearVelocity=!0,o.linearVelocity.copy(r.linearVelocity)):o.hasLinearVelocity=!1,r.angularVelocity?(o.hasAngularVelocity=!0,o.angularVelocity.copy(r.angularVelocity)):o.hasAngularVelocity=!1,this.dispatchEvent(Ru)))}return o!==null&&(o.visible=r!==null),c!==null&&(c.visible=a!==null),l!==null&&(l.visible=s!==null),this}_getHandJoint(e,t){if(e.joints[t.jointName]===void 0){const i=new it;i.matrixAutoUpdate=!1,i.visible=!1,e.joints[t.jointName]=i,e.add(i)}return e.joints[t.jointName]}}class Cu extends Et{constructor(){super(),this.isScene=!0,this.type="Scene",this.background=null,this.environment=null,this.fog=null,this.backgroundBlurriness=0,this.backgroundIntensity=1,this.backgroundRotation=new mt,this.environmentIntensity=1,this.environmentRotation=new mt,this.overrideMaterial=null,typeof __THREE_DEVTOOLS__<"u"&&__THREE_DEVTOOLS__.dispatchEvent(new CustomEvent("observe",{detail:this}))}copy(e,t){return super.copy(e,t),e.background!==null&&(this.background=e.background.clone()),e.environment!==null&&(this.environment=e.environment.clone()),e.fog!==null&&(this.fog=e.fog.clone()),this.backgroundBlurriness=e.backgroundBlurriness,this.backgroundIntensity=e.backgroundIntensity,this.backgroundRotation.copy(e.backgroundRotation),this.environmentIntensity=e.environmentIntensity,this.environmentRotation.copy(e.environmentRotation),e.overrideMaterial!==null&&(this.overrideMaterial=e.overrideMaterial.clone()),this.matrixAutoUpdate=e.matrixAutoUpdate,this}toJSON(e){const t=super.toJSON(e);return this.fog!==null&&(t.object.fog=this.fog.toJSON()),this.backgroundBlurriness>0&&(t.object.backgroundBlurriness=this.backgroundBlurriness),this.backgroundIntensity!==1&&(t.object.backgroundIntensity=this.backgroundIntensity),t.object.backgroundRotation=this.backgroundRotation.toArray(),this.environmentIntensity!==1&&(t.object.environmentIntensity=this.environmentIntensity),t.object.environmentRotation=this.environmentRotation.toArray(),t}}const _a=new F,Pu=new F,Du=new Be;class Hn{constructor(e=new F(1,0,0),t=0){this.isPlane=!0,this.normal=e,this.constant=t}set(e,t){return this.normal.copy(e),this.constant=t,this}setComponents(e,t,i,r){return this.normal.set(e,t,i),this.constant=r,this}setFromNormalAndCoplanarPoint(e,t){return this.normal.copy(e),this.constant=-t.dot(this.normal),this}setFromCoplanarPoints(e,t,i){const r=_a.subVectors(i,t).cross(Pu.subVectors(e,t)).normalize();return this.setFromNormalAndCoplanarPoint(r,e),this}copy(e){return this.normal.copy(e.normal),this.constant=e.constant,this}normalize(){const e=1/this.normal.length();return this.normal.multiplyScalar(e),this.constant*=e,this}negate(){return this.constant*=-1,this.normal.negate(),this}distanceToPoint(e){return this.normal.dot(e)+this.constant}distanceToSphere(e){return this.distanceToPoint(e.center)-e.radius}projectPoint(e,t){return t.copy(e).addScaledVector(this.normal,-this.distanceToPoint(e))}intersectLine(e,t){const i=e.delta(_a),r=this.normal.dot(i);if(r===0)return this.distanceToPoint(e.start)===0?t.copy(e.start):null;const a=-(e.start.dot(this.normal)+this.constant)/r;return a<0||a>1?null:t.copy(e.start).addScaledVector(i,a)}intersectsLine(e){const t=this.distanceToPoint(e.start),i=this.distanceToPoint(e.end);return t<0&&i>0||i<0&&t>0}intersectsBox(e){return e.intersectsPlane(this)}intersectsSphere(e){return e.intersectsPlane(this)}coplanarPoint(e){return e.copy(this.normal).multiplyScalar(-this.constant)}applyMatrix4(e,t){const i=t||Du.getNormalMatrix(e),r=this.coplanarPoint(_a).applyMatrix4(e),a=this.normal.applyMatrix3(i).normalize();return this.constant=-r.dot(a),this}translate(e){return this.constant-=e.dot(this.normal),this}equals(e){return e.normal.equals(this.normal)&&e.constant===this.constant}clone(){return new this.constructor().copy(this)}}const On=new Hr,vr=new F;class Fs{constructor(e=new Hn,t=new Hn,i=new Hn,r=new Hn,a=new Hn,s=new Hn){this.planes=[e,t,i,r,a,s]}set(e,t,i,r,a,s){const o=this.planes;return o[0].copy(e),o[1].copy(t),o[2].copy(i),o[3].copy(r),o[4].copy(a),o[5].copy(s),this}copy(e){const t=this.planes;for(let i=0;i<6;i++)t[i].copy(e.planes[i]);return this}setFromProjectionMatrix(e,t=mn){const i=this.planes,r=e.elements,a=r[0],s=r[1],o=r[2],c=r[3],l=r[4],d=r[5],h=r[6],f=r[7],m=r[8],g=r[9],_=r[10],p=r[11],u=r[12],b=r[13],S=r[14],M=r[15];if(i[0].setComponents(c-a,f-l,p-m,M-u).normalize(),i[1].setComponents(c+a,f+l,p+m,M+u).normalize(),i[2].setComponents(c+s,f+d,p+g,M+b).normalize(),i[3].setComponents(c-s,f-d,p-g,M-b).normalize(),i[4].setComponents(c-o,f-h,p-_,M-S).normalize(),t===mn)i[5].setComponents(c+o,f+h,p+_,M+S).normalize();else if(t===kr)i[5].setComponents(o,h,_,S).normalize();else throw new Error("THREE.Frustum.setFromProjectionMatrix(): Invalid coordinate system: "+t);return this}intersectsObject(e){if(e.boundingSphere!==void 0)e.boundingSphere===null&&e.computeBoundingSphere(),On.copy(e.boundingSphere).applyMatrix4(e.matrixWorld);else{const t=e.geometry;t.boundingSphere===null&&t.computeBoundingSphere(),On.copy(t.boundingSphere).applyMatrix4(e.matrixWorld)}return this.intersectsSphere(On)}intersectsSprite(e){return On.center.set(0,0,0),On.radius=.7071067811865476,On.applyMatrix4(e.matrixWorld),this.intersectsSphere(On)}intersectsSphere(e){const t=this.planes,i=e.center,r=-e.radius;for(let a=0;a<6;a++)if(t[a].distanceToPoint(i)<r)return!1;return!0}intersectsBox(e){const t=this.planes;for(let i=0;i<6;i++){const r=t[i];if(vr.x=r.normal.x>0?e.max.x:e.min.x,vr.y=r.normal.y>0?e.max.y:e.min.y,vr.z=r.normal.z>0?e.max.z:e.min.z,r.distanceToPoint(vr)<0)return!1}return!0}containsPoint(e){const t=this.planes;for(let i=0;i<6;i++)if(t[i].distanceToPoint(e)<0)return!1;return!0}clone(){return new this.constructor().copy(this)}}class ht extends Ii{constructor(e){super(),this.isLineBasicMaterial=!0,this.type="LineBasicMaterial",this.color=new ce(16777215),this.map=null,this.linewidth=1,this.linecap="round",this.linejoin="round",this.fog=!0,this.setValues(e)}copy(e){return super.copy(e),this.color.copy(e.color),this.map=e.map,this.linewidth=e.linewidth,this.linecap=e.linecap,this.linejoin=e.linejoin,this.fog=e.fog,this}}const Or=new F,Br=new F,wo=new ct,Hi=new Ns,xr=new Hr,va=new F,Ao=new F;class Wi extends Et{constructor(e=new Ze,t=new ht){super(),this.isLine=!0,this.type="Line",this.geometry=e,this.material=t,this.morphTargetDictionary=void 0,this.morphTargetInfluences=void 0,this.updateMorphTargets()}copy(e,t){return super.copy(e,t),this.material=Array.isArray(e.material)?e.material.slice():e.material,this.geometry=e.geometry,this}computeLineDistances(){const e=this.geometry;if(e.index===null){const t=e.attributes.position,i=[0];for(let r=1,a=t.count;r<a;r++)Or.fromBufferAttribute(t,r-1),Br.fromBufferAttribute(t,r),i[r]=i[r-1],i[r]+=Or.distanceTo(Br);e.setAttribute("lineDistance",new He(i,1))}else console.warn("THREE.Line.computeLineDistances(): Computation only possible with non-indexed BufferGeometry.");return this}raycast(e,t){const i=this.geometry,r=this.matrixWorld,a=e.params.Line.threshold,s=i.drawRange;if(i.boundingSphere===null&&i.computeBoundingSphere(),xr.copy(i.boundingSphere),xr.applyMatrix4(r),xr.radius+=a,e.ray.intersectsSphere(xr)===!1)return;wo.copy(r).invert(),Hi.copy(e.ray).applyMatrix4(wo);const o=a/((this.scale.x+this.scale.y+this.scale.z)/3),c=o*o,l=this.isLineSegments?2:1,d=i.index,f=i.attributes.position;if(d!==null){const m=Math.max(0,s.start),g=Math.min(d.count,s.start+s.count);for(let _=m,p=g-1;_<p;_+=l){const u=d.getX(_),b=d.getX(_+1),S=Mr(this,e,Hi,c,u,b,_);S&&t.push(S)}if(this.isLineLoop){const _=d.getX(g-1),p=d.getX(m),u=Mr(this,e,Hi,c,_,p,g-1);u&&t.push(u)}}else{const m=Math.max(0,s.start),g=Math.min(f.count,s.start+s.count);for(let _=m,p=g-1;_<p;_+=l){const u=Mr(this,e,Hi,c,_,_+1,_);u&&t.push(u)}if(this.isLineLoop){const _=Mr(this,e,Hi,c,g-1,m,g-1);_&&t.push(_)}}}updateMorphTargets(){const t=this.geometry.morphAttributes,i=Object.keys(t);if(i.length>0){const r=t[i[0]];if(r!==void 0){this.morphTargetInfluences=[],this.morphTargetDictionary={};for(let a=0,s=r.length;a<s;a++){const o=r[a].name||String(a);this.morphTargetInfluences.push(0),this.morphTargetDictionary[o]=a}}}}}function Mr(n,e,t,i,r,a,s){const o=n.geometry.attributes.position;if(Or.fromBufferAttribute(o,r),Br.fromBufferAttribute(o,a),t.distanceSqToSegment(Or,Br,va,Ao)>i)return;va.applyMatrix4(n.matrixWorld);const l=e.ray.origin.distanceTo(va);if(!(l<e.near||l>e.far))return{distance:l,point:Ao.clone().applyMatrix4(n.matrixWorld),index:s,face:null,faceIndex:null,barycoord:null,object:n}}const Ro=new F,Co=new F;class gt extends Wi{constructor(e,t){super(e,t),this.isLineSegments=!0,this.type="LineSegments"}computeLineDistances(){const e=this.geometry;if(e.index===null){const t=e.attributes.position,i=[];for(let r=0,a=t.count;r<a;r+=2)Ro.fromBufferAttribute(t,r),Co.fromBufferAttribute(t,r+1),i[r]=r===0?0:i[r-1],i[r+1]=i[r]+Ro.distanceTo(Co);e.setAttribute("lineDistance",new He(i,1))}else console.warn("THREE.LineSegments.computeLineDistances(): Computation only possible with non-indexed BufferGeometry.");return this}}class Bc extends Ct{constructor(e,t,i,r,a,s,o,c,l,d=Ei){if(d!==Ei&&d!==Ri)throw new Error("DepthTexture format must be either THREE.DepthFormat or THREE.DepthStencilFormat");i===void 0&&d===Ei&&(i=Qn),i===void 0&&d===Ri&&(i=Ai),super(null,r,a,s,o,c,d,i,l),this.isDepthTexture=!0,this.image={width:e,height:t},this.magFilter=o!==void 0?o:Jt,this.minFilter=c!==void 0?c:Jt,this.flipY=!1,this.generateMipmaps=!1,this.compareFunction=null}copy(e){return super.copy(e),this.source=new zs(Object.assign({},e.image)),this.compareFunction=e.compareFunction,this}toJSON(e){const t=super.toJSON(e);return this.compareFunction!==null&&(t.compareFunction=this.compareFunction),t}}class Ji extends Ze{constructor(e=1,t=1,i=1,r=32,a=1,s=!1,o=0,c=Math.PI*2){super(),this.type="CylinderGeometry",this.parameters={radiusTop:e,radiusBottom:t,height:i,radialSegments:r,heightSegments:a,openEnded:s,thetaStart:o,thetaLength:c};const l=this;r=Math.floor(r),a=Math.floor(a);const d=[],h=[],f=[],m=[];let g=0;const _=[],p=i/2;let u=0;b(),s===!1&&(e>0&&S(!0),t>0&&S(!1)),this.setIndex(d),this.setAttribute("position",new He(h,3)),this.setAttribute("normal",new He(f,3)),this.setAttribute("uv",new He(m,2));function b(){const M=new F,w=new F;let T=0;const A=(t-e)/i;for(let L=0;L<=a;L++){const x=[],v=L/a,R=v*(t-e)+e;for(let U=0;U<=r;U++){const C=U/r,D=C*c+o,k=Math.sin(D),N=Math.cos(D);w.x=R*k,w.y=-v*i+p,w.z=R*N,h.push(w.x,w.y,w.z),M.set(k,A,N).normalize(),f.push(M.x,M.y,M.z),m.push(C,1-v),x.push(g++)}_.push(x)}for(let L=0;L<r;L++)for(let x=0;x<a;x++){const v=_[x][L],R=_[x+1][L],U=_[x+1][L+1],C=_[x][L+1];(e>0||x!==0)&&(d.push(v,R,C),T+=3),(t>0||x!==a-1)&&(d.push(R,U,C),T+=3)}l.addGroup(u,T,0),u+=T}function S(M){const w=g,T=new Ke,A=new F;let L=0;const x=M===!0?e:t,v=M===!0?1:-1;for(let U=1;U<=r;U++)h.push(0,p*v,0),f.push(0,v,0),m.push(.5,.5),g++;const R=g;for(let U=0;U<=r;U++){const D=U/r*c+o,k=Math.cos(D),N=Math.sin(D);A.x=x*N,A.y=p*v,A.z=x*k,h.push(A.x,A.y,A.z),f.push(0,v,0),T.x=k*.5+.5,T.y=N*.5*v+.5,m.push(T.x,T.y),g++}for(let U=0;U<r;U++){const C=w+U,D=R+U;M===!0?d.push(D,D+1,C):d.push(D+1,D,C),L+=3}l.addGroup(u,L,M===!0?1:2),u+=L}}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}static fromJSON(e){return new Ji(e.radiusTop,e.radiusBottom,e.height,e.radialSegments,e.heightSegments,e.openEnded,e.thetaStart,e.thetaLength)}}class Os extends Ji{constructor(e=1,t=1,i=32,r=1,a=!1,s=0,o=Math.PI*2){super(0,e,t,i,r,a,s,o),this.type="ConeGeometry",this.parameters={radius:e,height:t,radialSegments:i,heightSegments:r,openEnded:a,thetaStart:s,thetaLength:o}}static fromJSON(e){return new Os(e.radius,e.height,e.radialSegments,e.heightSegments,e.openEnded,e.thetaStart,e.thetaLength)}}const Sr=new F,Er=new F,xa=new F,br=new Gt;class jr extends Ze{constructor(e=null,t=1){if(super(),this.type="EdgesGeometry",this.parameters={geometry:e,thresholdAngle:t},e!==null){const r=Math.pow(10,4),a=Math.cos(Ir*t),s=e.getIndex(),o=e.getAttribute("position"),c=s?s.count:o.count,l=[0,0,0],d=["a","b","c"],h=new Array(3),f={},m=[];for(let g=0;g<c;g+=3){s?(l[0]=s.getX(g),l[1]=s.getX(g+1),l[2]=s.getX(g+2)):(l[0]=g,l[1]=g+1,l[2]=g+2);const{a:_,b:p,c:u}=br;if(_.fromBufferAttribute(o,l[0]),p.fromBufferAttribute(o,l[1]),u.fromBufferAttribute(o,l[2]),br.getNormal(xa),h[0]=`${Math.round(_.x*r)},${Math.round(_.y*r)},${Math.round(_.z*r)}`,h[1]=`${Math.round(p.x*r)},${Math.round(p.y*r)},${Math.round(p.z*r)}`,h[2]=`${Math.round(u.x*r)},${Math.round(u.y*r)},${Math.round(u.z*r)}`,!(h[0]===h[1]||h[1]===h[2]||h[2]===h[0]))for(let b=0;b<3;b++){const S=(b+1)%3,M=h[b],w=h[S],T=br[d[b]],A=br[d[S]],L=`${M}_${w}`,x=`${w}_${M}`;x in f&&f[x]?(xa.dot(f[x].normal)<=a&&(m.push(T.x,T.y,T.z),m.push(A.x,A.y,A.z)),f[x]=null):L in f||(f[L]={index0:l[b],index1:l[S],normal:xa.clone()})}}for(const g in f)if(f[g]){const{index0:_,index1:p}=f[g];Sr.fromBufferAttribute(o,_),Er.fromBufferAttribute(o,p),m.push(Sr.x,Sr.y,Sr.z),m.push(Er.x,Er.y,Er.z)}this.setAttribute("position",new He(m,3))}}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}}class zi extends Ze{constructor(e=1,t=1,i=1,r=1){super(),this.type="PlaneGeometry",this.parameters={width:e,height:t,widthSegments:i,heightSegments:r};const a=e/2,s=t/2,o=Math.floor(i),c=Math.floor(r),l=o+1,d=c+1,h=e/o,f=t/c,m=[],g=[],_=[],p=[];for(let u=0;u<d;u++){const b=u*f-s;for(let S=0;S<l;S++){const M=S*h-a;g.push(M,-b,0),_.push(0,0,1),p.push(S/o),p.push(1-u/c)}}for(let u=0;u<c;u++)for(let b=0;b<o;b++){const S=b+l*u,M=b+l*(u+1),w=b+1+l*(u+1),T=b+1+l*u;m.push(S,M,T),m.push(M,w,T)}this.setIndex(m),this.setAttribute("position",new He(g,3)),this.setAttribute("normal",new He(_,3)),this.setAttribute("uv",new He(p,2))}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}static fromJSON(e){return new zi(e.width,e.height,e.widthSegments,e.heightSegments)}}class Bs extends Ze{constructor(e=.5,t=1,i=32,r=1,a=0,s=Math.PI*2){super(),this.type="RingGeometry",this.parameters={innerRadius:e,outerRadius:t,thetaSegments:i,phiSegments:r,thetaStart:a,thetaLength:s},i=Math.max(3,i),r=Math.max(1,r);const o=[],c=[],l=[],d=[];let h=e;const f=(t-e)/r,m=new F,g=new Ke;for(let _=0;_<=r;_++){for(let p=0;p<=i;p++){const u=a+p/i*s;m.x=h*Math.cos(u),m.y=h*Math.sin(u),c.push(m.x,m.y,m.z),l.push(0,0,1),g.x=(m.x/t+1)/2,g.y=(m.y/t+1)/2,d.push(g.x,g.y)}h+=f}for(let _=0;_<r;_++){const p=_*(i+1);for(let u=0;u<i;u++){const b=u+p,S=b,M=b+i+1,w=b+i+2,T=b+1;o.push(S,M,T),o.push(M,w,T)}}this.setIndex(o),this.setAttribute("position",new He(c,3)),this.setAttribute("normal",new He(l,3)),this.setAttribute("uv",new He(d,2))}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}static fromJSON(e){return new Bs(e.innerRadius,e.outerRadius,e.thetaSegments,e.phiSegments,e.thetaStart,e.thetaLength)}}class xn extends Ze{constructor(e=1,t=32,i=16,r=0,a=Math.PI*2,s=0,o=Math.PI){super(),this.type="SphereGeometry",this.parameters={radius:e,widthSegments:t,heightSegments:i,phiStart:r,phiLength:a,thetaStart:s,thetaLength:o},t=Math.max(3,Math.floor(t)),i=Math.max(2,Math.floor(i));const c=Math.min(s+o,Math.PI);let l=0;const d=[],h=new F,f=new F,m=[],g=[],_=[],p=[];for(let u=0;u<=i;u++){const b=[],S=u/i;let M=0;u===0&&s===0?M=.5/t:u===i&&c===Math.PI&&(M=-.5/t);for(let w=0;w<=t;w++){const T=w/t;h.x=-e*Math.cos(r+T*a)*Math.sin(s+S*o),h.y=e*Math.cos(s+S*o),h.z=e*Math.sin(r+T*a)*Math.sin(s+S*o),g.push(h.x,h.y,h.z),f.copy(h).normalize(),_.push(f.x,f.y,f.z),p.push(T+M,1-S),b.push(l++)}d.push(b)}for(let u=0;u<i;u++)for(let b=0;b<t;b++){const S=d[u][b+1],M=d[u][b],w=d[u+1][b],T=d[u+1][b+1];(u!==0||s>0)&&m.push(S,M,T),(u!==i-1||c<Math.PI)&&m.push(M,w,T)}this.setIndex(m),this.setAttribute("position",new He(g,3)),this.setAttribute("normal",new He(_,3)),this.setAttribute("uv",new He(p,2))}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}static fromJSON(e){return new xn(e.radius,e.widthSegments,e.heightSegments,e.phiStart,e.phiLength,e.thetaStart,e.thetaLength)}}class ot extends Ii{constructor(e){super(),this.isMeshStandardMaterial=!0,this.type="MeshStandardMaterial",this.defines={STANDARD:""},this.color=new ce(16777215),this.roughness=1,this.metalness=0,this.map=null,this.lightMap=null,this.lightMapIntensity=1,this.aoMap=null,this.aoMapIntensity=1,this.emissive=new ce(0),this.emissiveIntensity=1,this.emissiveMap=null,this.bumpMap=null,this.bumpScale=1,this.normalMap=null,this.normalMapType=Pc,this.normalScale=new Ke(1,1),this.displacementMap=null,this.displacementScale=1,this.displacementBias=0,this.roughnessMap=null,this.metalnessMap=null,this.alphaMap=null,this.envMap=null,this.envMapRotation=new mt,this.envMapIntensity=1,this.wireframe=!1,this.wireframeLinewidth=1,this.wireframeLinecap="round",this.wireframeLinejoin="round",this.flatShading=!1,this.fog=!0,this.setValues(e)}copy(e){return super.copy(e),this.defines={STANDARD:""},this.color.copy(e.color),this.roughness=e.roughness,this.metalness=e.metalness,this.map=e.map,this.lightMap=e.lightMap,this.lightMapIntensity=e.lightMapIntensity,this.aoMap=e.aoMap,this.aoMapIntensity=e.aoMapIntensity,this.emissive.copy(e.emissive),this.emissiveMap=e.emissiveMap,this.emissiveIntensity=e.emissiveIntensity,this.bumpMap=e.bumpMap,this.bumpScale=e.bumpScale,this.normalMap=e.normalMap,this.normalMapType=e.normalMapType,this.normalScale.copy(e.normalScale),this.displacementMap=e.displacementMap,this.displacementScale=e.displacementScale,this.displacementBias=e.displacementBias,this.roughnessMap=e.roughnessMap,this.metalnessMap=e.metalnessMap,this.alphaMap=e.alphaMap,this.envMap=e.envMap,this.envMapRotation.copy(e.envMapRotation),this.envMapIntensity=e.envMapIntensity,this.wireframe=e.wireframe,this.wireframeLinewidth=e.wireframeLinewidth,this.wireframeLinecap=e.wireframeLinecap,this.wireframeLinejoin=e.wireframeLinejoin,this.flatShading=e.flatShading,this.fog=e.fog,this}}class Lu extends Ii{constructor(e){super(),this.isMeshDepthMaterial=!0,this.type="MeshDepthMaterial",this.depthPacking=Gl,this.map=null,this.alphaMap=null,this.displacementMap=null,this.displacementScale=1,this.displacementBias=0,this.wireframe=!1,this.wireframeLinewidth=1,this.setValues(e)}copy(e){return super.copy(e),this.depthPacking=e.depthPacking,this.map=e.map,this.alphaMap=e.alphaMap,this.displacementMap=e.displacementMap,this.displacementScale=e.displacementScale,this.displacementBias=e.displacementBias,this.wireframe=e.wireframe,this.wireframeLinewidth=e.wireframeLinewidth,this}}class Iu extends Ii{constructor(e){super(),this.isMeshDistanceMaterial=!0,this.type="MeshDistanceMaterial",this.map=null,this.alphaMap=null,this.displacementMap=null,this.displacementScale=1,this.displacementBias=0,this.setValues(e)}copy(e){return super.copy(e),this.map=e.map,this.alphaMap=e.alphaMap,this.displacementMap=e.displacementMap,this.displacementScale=e.displacementScale,this.displacementBias=e.displacementBias,this}}class Uu extends ht{constructor(e){super(),this.isLineDashedMaterial=!0,this.type="LineDashedMaterial",this.scale=1,this.dashSize=3,this.gapSize=1,this.setValues(e)}copy(e){return super.copy(e),this.scale=e.scale,this.dashSize=e.dashSize,this.gapSize=e.gapSize,this}}class jc extends Et{constructor(e,t=1){super(),this.isLight=!0,this.type="Light",this.color=new ce(e),this.intensity=t}dispose(){}copy(e,t){return super.copy(e,t),this.color.copy(e.color),this.intensity=e.intensity,this}toJSON(e){const t=super.toJSON(e);return t.object.color=this.color.getHex(),t.object.intensity=this.intensity,this.groundColor!==void 0&&(t.object.groundColor=this.groundColor.getHex()),this.distance!==void 0&&(t.object.distance=this.distance),this.angle!==void 0&&(t.object.angle=this.angle),this.decay!==void 0&&(t.object.decay=this.decay),this.penumbra!==void 0&&(t.object.penumbra=this.penumbra),this.shadow!==void 0&&(t.object.shadow=this.shadow.toJSON()),this.target!==void 0&&(t.object.target=this.target.uuid),t}}const Ma=new ct,Po=new F,Do=new F;class zu{constructor(e){this.camera=e,this.intensity=1,this.bias=0,this.normalBias=0,this.radius=1,this.blurSamples=8,this.mapSize=new Ke(512,512),this.map=null,this.mapPass=null,this.matrix=new ct,this.autoUpdate=!0,this.needsUpdate=!1,this._frustum=new Fs,this._frameExtents=new Ke(1,1),this._viewportCount=1,this._viewports=[new dt(0,0,1,1)]}getViewportCount(){return this._viewportCount}getFrustum(){return this._frustum}updateMatrices(e){const t=this.camera,i=this.matrix;Po.setFromMatrixPosition(e.matrixWorld),t.position.copy(Po),Do.setFromMatrixPosition(e.target.matrixWorld),t.lookAt(Do),t.updateMatrixWorld(),Ma.multiplyMatrices(t.projectionMatrix,t.matrixWorldInverse),this._frustum.setFromProjectionMatrix(Ma),i.set(.5,0,0,.5,0,.5,0,.5,0,0,.5,.5,0,0,0,1),i.multiply(Ma)}getViewport(e){return this._viewports[e]}getFrameExtents(){return this._frameExtents}dispose(){this.map&&this.map.dispose(),this.mapPass&&this.mapPass.dispose()}copy(e){return this.camera=e.camera.clone(),this.intensity=e.intensity,this.bias=e.bias,this.radius=e.radius,this.mapSize.copy(e.mapSize),this}clone(){return new this.constructor().copy(this)}toJSON(){const e={};return this.intensity!==1&&(e.intensity=this.intensity),this.bias!==0&&(e.bias=this.bias),this.normalBias!==0&&(e.normalBias=this.normalBias),this.radius!==1&&(e.radius=this.radius),(this.mapSize.x!==512||this.mapSize.y!==512)&&(e.mapSize=this.mapSize.toArray()),e.camera=this.camera.toJSON(!1).object,delete e.camera.matrix,e}}class Vc extends Fc{constructor(e=-1,t=1,i=1,r=-1,a=.1,s=2e3){super(),this.isOrthographicCamera=!0,this.type="OrthographicCamera",this.zoom=1,this.view=null,this.left=e,this.right=t,this.top=i,this.bottom=r,this.near=a,this.far=s,this.updateProjectionMatrix()}copy(e,t){return super.copy(e,t),this.left=e.left,this.right=e.right,this.top=e.top,this.bottom=e.bottom,this.near=e.near,this.far=e.far,this.zoom=e.zoom,this.view=e.view===null?null:Object.assign({},e.view),this}setViewOffset(e,t,i,r,a,s){this.view===null&&(this.view={enabled:!0,fullWidth:1,fullHeight:1,offsetX:0,offsetY:0,width:1,height:1}),this.view.enabled=!0,this.view.fullWidth=e,this.view.fullHeight=t,this.view.offsetX=i,this.view.offsetY=r,this.view.width=a,this.view.height=s,this.updateProjectionMatrix()}clearViewOffset(){this.view!==null&&(this.view.enabled=!1),this.updateProjectionMatrix()}updateProjectionMatrix(){const e=(this.right-this.left)/(2*this.zoom),t=(this.top-this.bottom)/(2*this.zoom),i=(this.right+this.left)/2,r=(this.top+this.bottom)/2;let a=i-e,s=i+e,o=r+t,c=r-t;if(this.view!==null&&this.view.enabled){const l=(this.right-this.left)/this.view.fullWidth/this.zoom,d=(this.top-this.bottom)/this.view.fullHeight/this.zoom;a+=l*this.view.offsetX,s=a+l*this.view.width,o-=d*this.view.offsetY,c=o-d*this.view.height}this.projectionMatrix.makeOrthographic(a,s,o,c,this.near,this.far,this.coordinateSystem),this.projectionMatrixInverse.copy(this.projectionMatrix).invert()}toJSON(e){const t=super.toJSON(e);return t.object.zoom=this.zoom,t.object.left=this.left,t.object.right=this.right,t.object.top=this.top,t.object.bottom=this.bottom,t.object.near=this.near,t.object.far=this.far,this.view!==null&&(t.object.view=Object.assign({},this.view)),t}}class Nu extends zu{constructor(){super(new Vc(-5,5,5,-5,.5,500)),this.isDirectionalLightShadow=!0}}class Lo extends jc{constructor(e,t){super(e,t),this.isDirectionalLight=!0,this.type="DirectionalLight",this.position.copy(Et.DEFAULT_UP),this.updateMatrix(),this.target=new Et,this.shadow=new Nu}dispose(){this.shadow.dispose()}copy(e){return super.copy(e),this.target=e.target.clone(),this.shadow=e.shadow.clone(),this}}class ku extends jc{constructor(e,t){super(e,t),this.isAmbientLight=!0,this.type="AmbientLight"}}class Fu extends Ht{constructor(e=[]){super(),this.isArrayCamera=!0,this.cameras=e,this.index=0}}const Io=new ct;class js{constructor(e,t,i=0,r=1/0){this.ray=new Ns(e,t),this.near=i,this.far=r,this.camera=null,this.layers=new ks,this.params={Mesh:{},Line:{threshold:1},LOD:{},Points:{threshold:1},Sprite:{}}}set(e,t){this.ray.set(e,t)}setFromCamera(e,t){t.isPerspectiveCamera?(this.ray.origin.setFromMatrixPosition(t.matrixWorld),this.ray.direction.set(e.x,e.y,.5).unproject(t).sub(this.ray.origin).normalize(),this.camera=t):t.isOrthographicCamera?(this.ray.origin.set(e.x,e.y,(t.near+t.far)/(t.near-t.far)).unproject(t),this.ray.direction.set(0,0,-1).transformDirection(t.matrixWorld),this.camera=t):console.error("THREE.Raycaster: Unsupported camera type: "+t.type)}setFromXRController(e){return Io.identity().extractRotation(e.matrixWorld),this.ray.origin.setFromMatrixPosition(e.matrixWorld),this.ray.direction.set(0,0,-1).applyMatrix4(Io),this}intersectObject(e,t=!0,i=[]){return xs(e,this,i,t),i.sort(Uo),i}intersectObjects(e,t=!0,i=[]){for(let r=0,a=e.length;r<a;r++)xs(e[r],this,i,t);return i.sort(Uo),i}}function Uo(n,e){return n.distance-e.distance}function xs(n,e,t,i){let r=!0;if(n.layers.test(e.layers)&&n.raycast(e,t)===!1&&(r=!1),r===!0&&i===!0){const a=n.children;for(let s=0,o=a.length;s<o;s++)xs(a[s],e,t,!0)}}function zo(n,e,t,i){const r=Ou(i);switch(t){case bc:return n*e;case Tc:return n*e;case wc:return n*e*2;case Ac:return n*e/r.components*r.byteLength;case Ls:return n*e/r.components*r.byteLength;case Rc:return n*e*2/r.components*r.byteLength;case Is:return n*e*2/r.components*r.byteLength;case yc:return n*e*3/r.components*r.byteLength;case Zt:return n*e*4/r.components*r.byteLength;case Us:return n*e*4/r.components*r.byteLength;case Rr:case Cr:return Math.floor((n+3)/4)*Math.floor((e+3)/4)*8;case Pr:case Dr:return Math.floor((n+3)/4)*Math.floor((e+3)/4)*16;case Ka:case $a:return Math.max(n,16)*Math.max(e,8)/4;case Xa:case qa:return Math.max(n,8)*Math.max(e,8)/2;case Ya:case Za:return Math.floor((n+3)/4)*Math.floor((e+3)/4)*8;case Ja:return Math.floor((n+3)/4)*Math.floor((e+3)/4)*16;case Qa:return Math.floor((n+3)/4)*Math.floor((e+3)/4)*16;case es:return Math.floor((n+4)/5)*Math.floor((e+3)/4)*16;case ts:return Math.floor((n+4)/5)*Math.floor((e+4)/5)*16;case ns:return Math.floor((n+5)/6)*Math.floor((e+4)/5)*16;case is:return Math.floor((n+5)/6)*Math.floor((e+5)/6)*16;case rs:return Math.floor((n+7)/8)*Math.floor((e+4)/5)*16;case as:return Math.floor((n+7)/8)*Math.floor((e+5)/6)*16;case ss:return Math.floor((n+7)/8)*Math.floor((e+7)/8)*16;case os:return Math.floor((n+9)/10)*Math.floor((e+4)/5)*16;case cs:return Math.floor((n+9)/10)*Math.floor((e+5)/6)*16;case ls:return Math.floor((n+9)/10)*Math.floor((e+7)/8)*16;case us:return Math.floor((n+9)/10)*Math.floor((e+9)/10)*16;case ds:return Math.floor((n+11)/12)*Math.floor((e+9)/10)*16;case hs:return Math.floor((n+11)/12)*Math.floor((e+11)/12)*16;case Lr:case fs:case ps:return Math.ceil(n/4)*Math.ceil(e/4)*16;case Cc:case ms:return Math.ceil(n/4)*Math.ceil(e/4)*8;case gs:case _s:return Math.ceil(n/4)*Math.ceil(e/4)*16}throw new Error(`Unable to determine texture byte length for ${t} format.`)}function Ou(n){switch(n){case vn:case Mc:return{byteLength:1,components:1};case Xi:case Sc:case $i:return{byteLength:2,components:1};case Ps:case Ds:return{byteLength:2,components:4};case Qn:case Cs:case pn:return{byteLength:4,components:1};case Ec:return{byteLength:4,components:3}}throw new Error(`Unknown texture type ${n}.`)}typeof __THREE_DEVTOOLS__<"u"&&__THREE_DEVTOOLS__.dispatchEvent(new CustomEvent("register",{detail:{revision:Rs}}));typeof window<"u"&&(window.__THREE__?console.warn("WARNING: Multiple instances of Three.js being imported."):window.__THREE__=Rs);/**
 * @license
 * Copyright 2010-2025 Three.js Authors
 * SPDX-License-Identifier: MIT
 */function Hc(){let n=null,e=!1,t=null,i=null;function r(a,s){t(a,s),i=n.requestAnimationFrame(r)}return{start:function(){e!==!0&&t!==null&&(i=n.requestAnimationFrame(r),e=!0)},stop:function(){n.cancelAnimationFrame(i),e=!1},setAnimationLoop:function(a){t=a},setContext:function(a){n=a}}}function Bu(n){const e=new WeakMap;function t(o,c){const l=o.array,d=o.usage,h=l.byteLength,f=n.createBuffer();n.bindBuffer(c,f),n.bufferData(c,l,d),o.onUploadCallback();let m;if(l instanceof Float32Array)m=n.FLOAT;else if(l instanceof Uint16Array)o.isFloat16BufferAttribute?m=n.HALF_FLOAT:m=n.UNSIGNED_SHORT;else if(l instanceof Int16Array)m=n.SHORT;else if(l instanceof Uint32Array)m=n.UNSIGNED_INT;else if(l instanceof Int32Array)m=n.INT;else if(l instanceof Int8Array)m=n.BYTE;else if(l instanceof Uint8Array)m=n.UNSIGNED_BYTE;else if(l instanceof Uint8ClampedArray)m=n.UNSIGNED_BYTE;else throw new Error("THREE.WebGLAttributes: Unsupported buffer data format: "+l);return{buffer:f,type:m,bytesPerElement:l.BYTES_PER_ELEMENT,version:o.version,size:h}}function i(o,c,l){const d=c.array,h=c.updateRanges;if(n.bindBuffer(l,o),h.length===0)n.bufferSubData(l,0,d);else{h.sort((m,g)=>m.start-g.start);let f=0;for(let m=1;m<h.length;m++){const g=h[f],_=h[m];_.start<=g.start+g.count+1?g.count=Math.max(g.count,_.start+_.count-g.start):(++f,h[f]=_)}h.length=f+1;for(let m=0,g=h.length;m<g;m++){const _=h[m];n.bufferSubData(l,_.start*d.BYTES_PER_ELEMENT,d,_.start,_.count)}c.clearUpdateRanges()}c.onUploadCallback()}function r(o){return o.isInterleavedBufferAttribute&&(o=o.data),e.get(o)}function a(o){o.isInterleavedBufferAttribute&&(o=o.data);const c=e.get(o);c&&(n.deleteBuffer(c.buffer),e.delete(o))}function s(o,c){if(o.isInterleavedBufferAttribute&&(o=o.data),o.isGLBufferAttribute){const d=e.get(o);(!d||d.version<o.version)&&e.set(o,{buffer:o.buffer,type:o.type,bytesPerElement:o.elementSize,version:o.version});return}const l=e.get(o);if(l===void 0)e.set(o,t(o,c));else if(l.version<o.version){if(l.size!==o.array.byteLength)throw new Error("THREE.WebGLAttributes: The size of the buffer attribute's array buffer does not match the original size. Resizing buffer attributes is not supported.");i(l.buffer,o,c),l.version=o.version}}return{get:r,remove:a,update:s}}var ju=`#ifdef USE_ALPHAHASH
	if ( diffuseColor.a < getAlphaHashThreshold( vPosition ) ) discard;
#endif`,Vu=`#ifdef USE_ALPHAHASH
	const float ALPHA_HASH_SCALE = 0.05;
	float hash2D( vec2 value ) {
		return fract( 1.0e4 * sin( 17.0 * value.x + 0.1 * value.y ) * ( 0.1 + abs( sin( 13.0 * value.y + value.x ) ) ) );
	}
	float hash3D( vec3 value ) {
		return hash2D( vec2( hash2D( value.xy ), value.z ) );
	}
	float getAlphaHashThreshold( vec3 position ) {
		float maxDeriv = max(
			length( dFdx( position.xyz ) ),
			length( dFdy( position.xyz ) )
		);
		float pixScale = 1.0 / ( ALPHA_HASH_SCALE * maxDeriv );
		vec2 pixScales = vec2(
			exp2( floor( log2( pixScale ) ) ),
			exp2( ceil( log2( pixScale ) ) )
		);
		vec2 alpha = vec2(
			hash3D( floor( pixScales.x * position.xyz ) ),
			hash3D( floor( pixScales.y * position.xyz ) )
		);
		float lerpFactor = fract( log2( pixScale ) );
		float x = ( 1.0 - lerpFactor ) * alpha.x + lerpFactor * alpha.y;
		float a = min( lerpFactor, 1.0 - lerpFactor );
		vec3 cases = vec3(
			x * x / ( 2.0 * a * ( 1.0 - a ) ),
			( x - 0.5 * a ) / ( 1.0 - a ),
			1.0 - ( ( 1.0 - x ) * ( 1.0 - x ) / ( 2.0 * a * ( 1.0 - a ) ) )
		);
		float threshold = ( x < ( 1.0 - a ) )
			? ( ( x < a ) ? cases.x : cases.y )
			: cases.z;
		return clamp( threshold , 1.0e-6, 1.0 );
	}
#endif`,Hu=`#ifdef USE_ALPHAMAP
	diffuseColor.a *= texture2D( alphaMap, vAlphaMapUv ).g;
#endif`,Gu=`#ifdef USE_ALPHAMAP
	uniform sampler2D alphaMap;
#endif`,Wu=`#ifdef USE_ALPHATEST
	#ifdef ALPHA_TO_COVERAGE
	diffuseColor.a = smoothstep( alphaTest, alphaTest + fwidth( diffuseColor.a ), diffuseColor.a );
	if ( diffuseColor.a == 0.0 ) discard;
	#else
	if ( diffuseColor.a < alphaTest ) discard;
	#endif
#endif`,Xu=`#ifdef USE_ALPHATEST
	uniform float alphaTest;
#endif`,Ku=`#ifdef USE_AOMAP
	float ambientOcclusion = ( texture2D( aoMap, vAoMapUv ).r - 1.0 ) * aoMapIntensity + 1.0;
	reflectedLight.indirectDiffuse *= ambientOcclusion;
	#if defined( USE_CLEARCOAT ) 
		clearcoatSpecularIndirect *= ambientOcclusion;
	#endif
	#if defined( USE_SHEEN ) 
		sheenSpecularIndirect *= ambientOcclusion;
	#endif
	#if defined( USE_ENVMAP ) && defined( STANDARD )
		float dotNV = saturate( dot( geometryNormal, geometryViewDir ) );
		reflectedLight.indirectSpecular *= computeSpecularOcclusion( dotNV, ambientOcclusion, material.roughness );
	#endif
#endif`,qu=`#ifdef USE_AOMAP
	uniform sampler2D aoMap;
	uniform float aoMapIntensity;
#endif`,$u=`#ifdef USE_BATCHING
	#if ! defined( GL_ANGLE_multi_draw )
	#define gl_DrawID _gl_DrawID
	uniform int _gl_DrawID;
	#endif
	uniform highp sampler2D batchingTexture;
	uniform highp usampler2D batchingIdTexture;
	mat4 getBatchingMatrix( const in float i ) {
		int size = textureSize( batchingTexture, 0 ).x;
		int j = int( i ) * 4;
		int x = j % size;
		int y = j / size;
		vec4 v1 = texelFetch( batchingTexture, ivec2( x, y ), 0 );
		vec4 v2 = texelFetch( batchingTexture, ivec2( x + 1, y ), 0 );
		vec4 v3 = texelFetch( batchingTexture, ivec2( x + 2, y ), 0 );
		vec4 v4 = texelFetch( batchingTexture, ivec2( x + 3, y ), 0 );
		return mat4( v1, v2, v3, v4 );
	}
	float getIndirectIndex( const in int i ) {
		int size = textureSize( batchingIdTexture, 0 ).x;
		int x = i % size;
		int y = i / size;
		return float( texelFetch( batchingIdTexture, ivec2( x, y ), 0 ).r );
	}
#endif
#ifdef USE_BATCHING_COLOR
	uniform sampler2D batchingColorTexture;
	vec3 getBatchingColor( const in float i ) {
		int size = textureSize( batchingColorTexture, 0 ).x;
		int j = int( i );
		int x = j % size;
		int y = j / size;
		return texelFetch( batchingColorTexture, ivec2( x, y ), 0 ).rgb;
	}
#endif`,Yu=`#ifdef USE_BATCHING
	mat4 batchingMatrix = getBatchingMatrix( getIndirectIndex( gl_DrawID ) );
#endif`,Zu=`vec3 transformed = vec3( position );
#ifdef USE_ALPHAHASH
	vPosition = vec3( position );
#endif`,Ju=`vec3 objectNormal = vec3( normal );
#ifdef USE_TANGENT
	vec3 objectTangent = vec3( tangent.xyz );
#endif`,Qu=`float G_BlinnPhong_Implicit( ) {
	return 0.25;
}
float D_BlinnPhong( const in float shininess, const in float dotNH ) {
	return RECIPROCAL_PI * ( shininess * 0.5 + 1.0 ) * pow( dotNH, shininess );
}
vec3 BRDF_BlinnPhong( const in vec3 lightDir, const in vec3 viewDir, const in vec3 normal, const in vec3 specularColor, const in float shininess ) {
	vec3 halfDir = normalize( lightDir + viewDir );
	float dotNH = saturate( dot( normal, halfDir ) );
	float dotVH = saturate( dot( viewDir, halfDir ) );
	vec3 F = F_Schlick( specularColor, 1.0, dotVH );
	float G = G_BlinnPhong_Implicit( );
	float D = D_BlinnPhong( shininess, dotNH );
	return F * ( G * D );
} // validated`,ed=`#ifdef USE_IRIDESCENCE
	const mat3 XYZ_TO_REC709 = mat3(
		 3.2404542, -0.9692660,  0.0556434,
		-1.5371385,  1.8760108, -0.2040259,
		-0.4985314,  0.0415560,  1.0572252
	);
	vec3 Fresnel0ToIor( vec3 fresnel0 ) {
		vec3 sqrtF0 = sqrt( fresnel0 );
		return ( vec3( 1.0 ) + sqrtF0 ) / ( vec3( 1.0 ) - sqrtF0 );
	}
	vec3 IorToFresnel0( vec3 transmittedIor, float incidentIor ) {
		return pow2( ( transmittedIor - vec3( incidentIor ) ) / ( transmittedIor + vec3( incidentIor ) ) );
	}
	float IorToFresnel0( float transmittedIor, float incidentIor ) {
		return pow2( ( transmittedIor - incidentIor ) / ( transmittedIor + incidentIor ));
	}
	vec3 evalSensitivity( float OPD, vec3 shift ) {
		float phase = 2.0 * PI * OPD * 1.0e-9;
		vec3 val = vec3( 5.4856e-13, 4.4201e-13, 5.2481e-13 );
		vec3 pos = vec3( 1.6810e+06, 1.7953e+06, 2.2084e+06 );
		vec3 var = vec3( 4.3278e+09, 9.3046e+09, 6.6121e+09 );
		vec3 xyz = val * sqrt( 2.0 * PI * var ) * cos( pos * phase + shift ) * exp( - pow2( phase ) * var );
		xyz.x += 9.7470e-14 * sqrt( 2.0 * PI * 4.5282e+09 ) * cos( 2.2399e+06 * phase + shift[ 0 ] ) * exp( - 4.5282e+09 * pow2( phase ) );
		xyz /= 1.0685e-7;
		vec3 rgb = XYZ_TO_REC709 * xyz;
		return rgb;
	}
	vec3 evalIridescence( float outsideIOR, float eta2, float cosTheta1, float thinFilmThickness, vec3 baseF0 ) {
		vec3 I;
		float iridescenceIOR = mix( outsideIOR, eta2, smoothstep( 0.0, 0.03, thinFilmThickness ) );
		float sinTheta2Sq = pow2( outsideIOR / iridescenceIOR ) * ( 1.0 - pow2( cosTheta1 ) );
		float cosTheta2Sq = 1.0 - sinTheta2Sq;
		if ( cosTheta2Sq < 0.0 ) {
			return vec3( 1.0 );
		}
		float cosTheta2 = sqrt( cosTheta2Sq );
		float R0 = IorToFresnel0( iridescenceIOR, outsideIOR );
		float R12 = F_Schlick( R0, 1.0, cosTheta1 );
		float T121 = 1.0 - R12;
		float phi12 = 0.0;
		if ( iridescenceIOR < outsideIOR ) phi12 = PI;
		float phi21 = PI - phi12;
		vec3 baseIOR = Fresnel0ToIor( clamp( baseF0, 0.0, 0.9999 ) );		vec3 R1 = IorToFresnel0( baseIOR, iridescenceIOR );
		vec3 R23 = F_Schlick( R1, 1.0, cosTheta2 );
		vec3 phi23 = vec3( 0.0 );
		if ( baseIOR[ 0 ] < iridescenceIOR ) phi23[ 0 ] = PI;
		if ( baseIOR[ 1 ] < iridescenceIOR ) phi23[ 1 ] = PI;
		if ( baseIOR[ 2 ] < iridescenceIOR ) phi23[ 2 ] = PI;
		float OPD = 2.0 * iridescenceIOR * thinFilmThickness * cosTheta2;
		vec3 phi = vec3( phi21 ) + phi23;
		vec3 R123 = clamp( R12 * R23, 1e-5, 0.9999 );
		vec3 r123 = sqrt( R123 );
		vec3 Rs = pow2( T121 ) * R23 / ( vec3( 1.0 ) - R123 );
		vec3 C0 = R12 + Rs;
		I = C0;
		vec3 Cm = Rs - T121;
		for ( int m = 1; m <= 2; ++ m ) {
			Cm *= r123;
			vec3 Sm = 2.0 * evalSensitivity( float( m ) * OPD, float( m ) * phi );
			I += Cm * Sm;
		}
		return max( I, vec3( 0.0 ) );
	}
#endif`,td=`#ifdef USE_BUMPMAP
	uniform sampler2D bumpMap;
	uniform float bumpScale;
	vec2 dHdxy_fwd() {
		vec2 dSTdx = dFdx( vBumpMapUv );
		vec2 dSTdy = dFdy( vBumpMapUv );
		float Hll = bumpScale * texture2D( bumpMap, vBumpMapUv ).x;
		float dBx = bumpScale * texture2D( bumpMap, vBumpMapUv + dSTdx ).x - Hll;
		float dBy = bumpScale * texture2D( bumpMap, vBumpMapUv + dSTdy ).x - Hll;
		return vec2( dBx, dBy );
	}
	vec3 perturbNormalArb( vec3 surf_pos, vec3 surf_norm, vec2 dHdxy, float faceDirection ) {
		vec3 vSigmaX = normalize( dFdx( surf_pos.xyz ) );
		vec3 vSigmaY = normalize( dFdy( surf_pos.xyz ) );
		vec3 vN = surf_norm;
		vec3 R1 = cross( vSigmaY, vN );
		vec3 R2 = cross( vN, vSigmaX );
		float fDet = dot( vSigmaX, R1 ) * faceDirection;
		vec3 vGrad = sign( fDet ) * ( dHdxy.x * R1 + dHdxy.y * R2 );
		return normalize( abs( fDet ) * surf_norm - vGrad );
	}
#endif`,nd=`#if NUM_CLIPPING_PLANES > 0
	vec4 plane;
	#ifdef ALPHA_TO_COVERAGE
		float distanceToPlane, distanceGradient;
		float clipOpacity = 1.0;
		#pragma unroll_loop_start
		for ( int i = 0; i < UNION_CLIPPING_PLANES; i ++ ) {
			plane = clippingPlanes[ i ];
			distanceToPlane = - dot( vClipPosition, plane.xyz ) + plane.w;
			distanceGradient = fwidth( distanceToPlane ) / 2.0;
			clipOpacity *= smoothstep( - distanceGradient, distanceGradient, distanceToPlane );
			if ( clipOpacity == 0.0 ) discard;
		}
		#pragma unroll_loop_end
		#if UNION_CLIPPING_PLANES < NUM_CLIPPING_PLANES
			float unionClipOpacity = 1.0;
			#pragma unroll_loop_start
			for ( int i = UNION_CLIPPING_PLANES; i < NUM_CLIPPING_PLANES; i ++ ) {
				plane = clippingPlanes[ i ];
				distanceToPlane = - dot( vClipPosition, plane.xyz ) + plane.w;
				distanceGradient = fwidth( distanceToPlane ) / 2.0;
				unionClipOpacity *= 1.0 - smoothstep( - distanceGradient, distanceGradient, distanceToPlane );
			}
			#pragma unroll_loop_end
			clipOpacity *= 1.0 - unionClipOpacity;
		#endif
		diffuseColor.a *= clipOpacity;
		if ( diffuseColor.a == 0.0 ) discard;
	#else
		#pragma unroll_loop_start
		for ( int i = 0; i < UNION_CLIPPING_PLANES; i ++ ) {
			plane = clippingPlanes[ i ];
			if ( dot( vClipPosition, plane.xyz ) > plane.w ) discard;
		}
		#pragma unroll_loop_end
		#if UNION_CLIPPING_PLANES < NUM_CLIPPING_PLANES
			bool clipped = true;
			#pragma unroll_loop_start
			for ( int i = UNION_CLIPPING_PLANES; i < NUM_CLIPPING_PLANES; i ++ ) {
				plane = clippingPlanes[ i ];
				clipped = ( dot( vClipPosition, plane.xyz ) > plane.w ) && clipped;
			}
			#pragma unroll_loop_end
			if ( clipped ) discard;
		#endif
	#endif
#endif`,id=`#if NUM_CLIPPING_PLANES > 0
	varying vec3 vClipPosition;
	uniform vec4 clippingPlanes[ NUM_CLIPPING_PLANES ];
#endif`,rd=`#if NUM_CLIPPING_PLANES > 0
	varying vec3 vClipPosition;
#endif`,ad=`#if NUM_CLIPPING_PLANES > 0
	vClipPosition = - mvPosition.xyz;
#endif`,sd=`#if defined( USE_COLOR_ALPHA )
	diffuseColor *= vColor;
#elif defined( USE_COLOR )
	diffuseColor.rgb *= vColor;
#endif`,od=`#if defined( USE_COLOR_ALPHA )
	varying vec4 vColor;
#elif defined( USE_COLOR )
	varying vec3 vColor;
#endif`,cd=`#if defined( USE_COLOR_ALPHA )
	varying vec4 vColor;
#elif defined( USE_COLOR ) || defined( USE_INSTANCING_COLOR ) || defined( USE_BATCHING_COLOR )
	varying vec3 vColor;
#endif`,ld=`#if defined( USE_COLOR_ALPHA )
	vColor = vec4( 1.0 );
#elif defined( USE_COLOR ) || defined( USE_INSTANCING_COLOR ) || defined( USE_BATCHING_COLOR )
	vColor = vec3( 1.0 );
#endif
#ifdef USE_COLOR
	vColor *= color;
#endif
#ifdef USE_INSTANCING_COLOR
	vColor.xyz *= instanceColor.xyz;
#endif
#ifdef USE_BATCHING_COLOR
	vec3 batchingColor = getBatchingColor( getIndirectIndex( gl_DrawID ) );
	vColor.xyz *= batchingColor.xyz;
#endif`,ud=`#define PI 3.141592653589793
#define PI2 6.283185307179586
#define PI_HALF 1.5707963267948966
#define RECIPROCAL_PI 0.3183098861837907
#define RECIPROCAL_PI2 0.15915494309189535
#define EPSILON 1e-6
#ifndef saturate
#define saturate( a ) clamp( a, 0.0, 1.0 )
#endif
#define whiteComplement( a ) ( 1.0 - saturate( a ) )
float pow2( const in float x ) { return x*x; }
vec3 pow2( const in vec3 x ) { return x*x; }
float pow3( const in float x ) { return x*x*x; }
float pow4( const in float x ) { float x2 = x*x; return x2*x2; }
float max3( const in vec3 v ) { return max( max( v.x, v.y ), v.z ); }
float average( const in vec3 v ) { return dot( v, vec3( 0.3333333 ) ); }
highp float rand( const in vec2 uv ) {
	const highp float a = 12.9898, b = 78.233, c = 43758.5453;
	highp float dt = dot( uv.xy, vec2( a,b ) ), sn = mod( dt, PI );
	return fract( sin( sn ) * c );
}
#ifdef HIGH_PRECISION
	float precisionSafeLength( vec3 v ) { return length( v ); }
#else
	float precisionSafeLength( vec3 v ) {
		float maxComponent = max3( abs( v ) );
		return length( v / maxComponent ) * maxComponent;
	}
#endif
struct IncidentLight {
	vec3 color;
	vec3 direction;
	bool visible;
};
struct ReflectedLight {
	vec3 directDiffuse;
	vec3 directSpecular;
	vec3 indirectDiffuse;
	vec3 indirectSpecular;
};
#ifdef USE_ALPHAHASH
	varying vec3 vPosition;
#endif
vec3 transformDirection( in vec3 dir, in mat4 matrix ) {
	return normalize( ( matrix * vec4( dir, 0.0 ) ).xyz );
}
vec3 inverseTransformDirection( in vec3 dir, in mat4 matrix ) {
	return normalize( ( vec4( dir, 0.0 ) * matrix ).xyz );
}
mat3 transposeMat3( const in mat3 m ) {
	mat3 tmp;
	tmp[ 0 ] = vec3( m[ 0 ].x, m[ 1 ].x, m[ 2 ].x );
	tmp[ 1 ] = vec3( m[ 0 ].y, m[ 1 ].y, m[ 2 ].y );
	tmp[ 2 ] = vec3( m[ 0 ].z, m[ 1 ].z, m[ 2 ].z );
	return tmp;
}
bool isPerspectiveMatrix( mat4 m ) {
	return m[ 2 ][ 3 ] == - 1.0;
}
vec2 equirectUv( in vec3 dir ) {
	float u = atan( dir.z, dir.x ) * RECIPROCAL_PI2 + 0.5;
	float v = asin( clamp( dir.y, - 1.0, 1.0 ) ) * RECIPROCAL_PI + 0.5;
	return vec2( u, v );
}
vec3 BRDF_Lambert( const in vec3 diffuseColor ) {
	return RECIPROCAL_PI * diffuseColor;
}
vec3 F_Schlick( const in vec3 f0, const in float f90, const in float dotVH ) {
	float fresnel = exp2( ( - 5.55473 * dotVH - 6.98316 ) * dotVH );
	return f0 * ( 1.0 - fresnel ) + ( f90 * fresnel );
}
float F_Schlick( const in float f0, const in float f90, const in float dotVH ) {
	float fresnel = exp2( ( - 5.55473 * dotVH - 6.98316 ) * dotVH );
	return f0 * ( 1.0 - fresnel ) + ( f90 * fresnel );
} // validated`,dd=`#ifdef ENVMAP_TYPE_CUBE_UV
	#define cubeUV_minMipLevel 4.0
	#define cubeUV_minTileSize 16.0
	float getFace( vec3 direction ) {
		vec3 absDirection = abs( direction );
		float face = - 1.0;
		if ( absDirection.x > absDirection.z ) {
			if ( absDirection.x > absDirection.y )
				face = direction.x > 0.0 ? 0.0 : 3.0;
			else
				face = direction.y > 0.0 ? 1.0 : 4.0;
		} else {
			if ( absDirection.z > absDirection.y )
				face = direction.z > 0.0 ? 2.0 : 5.0;
			else
				face = direction.y > 0.0 ? 1.0 : 4.0;
		}
		return face;
	}
	vec2 getUV( vec3 direction, float face ) {
		vec2 uv;
		if ( face == 0.0 ) {
			uv = vec2( direction.z, direction.y ) / abs( direction.x );
		} else if ( face == 1.0 ) {
			uv = vec2( - direction.x, - direction.z ) / abs( direction.y );
		} else if ( face == 2.0 ) {
			uv = vec2( - direction.x, direction.y ) / abs( direction.z );
		} else if ( face == 3.0 ) {
			uv = vec2( - direction.z, direction.y ) / abs( direction.x );
		} else if ( face == 4.0 ) {
			uv = vec2( - direction.x, direction.z ) / abs( direction.y );
		} else {
			uv = vec2( direction.x, direction.y ) / abs( direction.z );
		}
		return 0.5 * ( uv + 1.0 );
	}
	vec3 bilinearCubeUV( sampler2D envMap, vec3 direction, float mipInt ) {
		float face = getFace( direction );
		float filterInt = max( cubeUV_minMipLevel - mipInt, 0.0 );
		mipInt = max( mipInt, cubeUV_minMipLevel );
		float faceSize = exp2( mipInt );
		highp vec2 uv = getUV( direction, face ) * ( faceSize - 2.0 ) + 1.0;
		if ( face > 2.0 ) {
			uv.y += faceSize;
			face -= 3.0;
		}
		uv.x += face * faceSize;
		uv.x += filterInt * 3.0 * cubeUV_minTileSize;
		uv.y += 4.0 * ( exp2( CUBEUV_MAX_MIP ) - faceSize );
		uv.x *= CUBEUV_TEXEL_WIDTH;
		uv.y *= CUBEUV_TEXEL_HEIGHT;
		#ifdef texture2DGradEXT
			return texture2DGradEXT( envMap, uv, vec2( 0.0 ), vec2( 0.0 ) ).rgb;
		#else
			return texture2D( envMap, uv ).rgb;
		#endif
	}
	#define cubeUV_r0 1.0
	#define cubeUV_m0 - 2.0
	#define cubeUV_r1 0.8
	#define cubeUV_m1 - 1.0
	#define cubeUV_r4 0.4
	#define cubeUV_m4 2.0
	#define cubeUV_r5 0.305
	#define cubeUV_m5 3.0
	#define cubeUV_r6 0.21
	#define cubeUV_m6 4.0
	float roughnessToMip( float roughness ) {
		float mip = 0.0;
		if ( roughness >= cubeUV_r1 ) {
			mip = ( cubeUV_r0 - roughness ) * ( cubeUV_m1 - cubeUV_m0 ) / ( cubeUV_r0 - cubeUV_r1 ) + cubeUV_m0;
		} else if ( roughness >= cubeUV_r4 ) {
			mip = ( cubeUV_r1 - roughness ) * ( cubeUV_m4 - cubeUV_m1 ) / ( cubeUV_r1 - cubeUV_r4 ) + cubeUV_m1;
		} else if ( roughness >= cubeUV_r5 ) {
			mip = ( cubeUV_r4 - roughness ) * ( cubeUV_m5 - cubeUV_m4 ) / ( cubeUV_r4 - cubeUV_r5 ) + cubeUV_m4;
		} else if ( roughness >= cubeUV_r6 ) {
			mip = ( cubeUV_r5 - roughness ) * ( cubeUV_m6 - cubeUV_m5 ) / ( cubeUV_r5 - cubeUV_r6 ) + cubeUV_m5;
		} else {
			mip = - 2.0 * log2( 1.16 * roughness );		}
		return mip;
	}
	vec4 textureCubeUV( sampler2D envMap, vec3 sampleDir, float roughness ) {
		float mip = clamp( roughnessToMip( roughness ), cubeUV_m0, CUBEUV_MAX_MIP );
		float mipF = fract( mip );
		float mipInt = floor( mip );
		vec3 color0 = bilinearCubeUV( envMap, sampleDir, mipInt );
		if ( mipF == 0.0 ) {
			return vec4( color0, 1.0 );
		} else {
			vec3 color1 = bilinearCubeUV( envMap, sampleDir, mipInt + 1.0 );
			return vec4( mix( color0, color1, mipF ), 1.0 );
		}
	}
#endif`,hd=`vec3 transformedNormal = objectNormal;
#ifdef USE_TANGENT
	vec3 transformedTangent = objectTangent;
#endif
#ifdef USE_BATCHING
	mat3 bm = mat3( batchingMatrix );
	transformedNormal /= vec3( dot( bm[ 0 ], bm[ 0 ] ), dot( bm[ 1 ], bm[ 1 ] ), dot( bm[ 2 ], bm[ 2 ] ) );
	transformedNormal = bm * transformedNormal;
	#ifdef USE_TANGENT
		transformedTangent = bm * transformedTangent;
	#endif
#endif
#ifdef USE_INSTANCING
	mat3 im = mat3( instanceMatrix );
	transformedNormal /= vec3( dot( im[ 0 ], im[ 0 ] ), dot( im[ 1 ], im[ 1 ] ), dot( im[ 2 ], im[ 2 ] ) );
	transformedNormal = im * transformedNormal;
	#ifdef USE_TANGENT
		transformedTangent = im * transformedTangent;
	#endif
#endif
transformedNormal = normalMatrix * transformedNormal;
#ifdef FLIP_SIDED
	transformedNormal = - transformedNormal;
#endif
#ifdef USE_TANGENT
	transformedTangent = ( modelViewMatrix * vec4( transformedTangent, 0.0 ) ).xyz;
	#ifdef FLIP_SIDED
		transformedTangent = - transformedTangent;
	#endif
#endif`,fd=`#ifdef USE_DISPLACEMENTMAP
	uniform sampler2D displacementMap;
	uniform float displacementScale;
	uniform float displacementBias;
#endif`,pd=`#ifdef USE_DISPLACEMENTMAP
	transformed += normalize( objectNormal ) * ( texture2D( displacementMap, vDisplacementMapUv ).x * displacementScale + displacementBias );
#endif`,md=`#ifdef USE_EMISSIVEMAP
	vec4 emissiveColor = texture2D( emissiveMap, vEmissiveMapUv );
	#ifdef DECODE_VIDEO_TEXTURE_EMISSIVE
		emissiveColor = sRGBTransferEOTF( emissiveColor );
	#endif
	totalEmissiveRadiance *= emissiveColor.rgb;
#endif`,gd=`#ifdef USE_EMISSIVEMAP
	uniform sampler2D emissiveMap;
#endif`,_d="gl_FragColor = linearToOutputTexel( gl_FragColor );",vd=`vec4 LinearTransferOETF( in vec4 value ) {
	return value;
}
vec4 sRGBTransferEOTF( in vec4 value ) {
	return vec4( mix( pow( value.rgb * 0.9478672986 + vec3( 0.0521327014 ), vec3( 2.4 ) ), value.rgb * 0.0773993808, vec3( lessThanEqual( value.rgb, vec3( 0.04045 ) ) ) ), value.a );
}
vec4 sRGBTransferOETF( in vec4 value ) {
	return vec4( mix( pow( value.rgb, vec3( 0.41666 ) ) * 1.055 - vec3( 0.055 ), value.rgb * 12.92, vec3( lessThanEqual( value.rgb, vec3( 0.0031308 ) ) ) ), value.a );
}`,xd=`#ifdef USE_ENVMAP
	#ifdef ENV_WORLDPOS
		vec3 cameraToFrag;
		if ( isOrthographic ) {
			cameraToFrag = normalize( vec3( - viewMatrix[ 0 ][ 2 ], - viewMatrix[ 1 ][ 2 ], - viewMatrix[ 2 ][ 2 ] ) );
		} else {
			cameraToFrag = normalize( vWorldPosition - cameraPosition );
		}
		vec3 worldNormal = inverseTransformDirection( normal, viewMatrix );
		#ifdef ENVMAP_MODE_REFLECTION
			vec3 reflectVec = reflect( cameraToFrag, worldNormal );
		#else
			vec3 reflectVec = refract( cameraToFrag, worldNormal, refractionRatio );
		#endif
	#else
		vec3 reflectVec = vReflect;
	#endif
	#ifdef ENVMAP_TYPE_CUBE
		vec4 envColor = textureCube( envMap, envMapRotation * vec3( flipEnvMap * reflectVec.x, reflectVec.yz ) );
	#else
		vec4 envColor = vec4( 0.0 );
	#endif
	#ifdef ENVMAP_BLENDING_MULTIPLY
		outgoingLight = mix( outgoingLight, outgoingLight * envColor.xyz, specularStrength * reflectivity );
	#elif defined( ENVMAP_BLENDING_MIX )
		outgoingLight = mix( outgoingLight, envColor.xyz, specularStrength * reflectivity );
	#elif defined( ENVMAP_BLENDING_ADD )
		outgoingLight += envColor.xyz * specularStrength * reflectivity;
	#endif
#endif`,Md=`#ifdef USE_ENVMAP
	uniform float envMapIntensity;
	uniform float flipEnvMap;
	uniform mat3 envMapRotation;
	#ifdef ENVMAP_TYPE_CUBE
		uniform samplerCube envMap;
	#else
		uniform sampler2D envMap;
	#endif
	
#endif`,Sd=`#ifdef USE_ENVMAP
	uniform float reflectivity;
	#if defined( USE_BUMPMAP ) || defined( USE_NORMALMAP ) || defined( PHONG ) || defined( LAMBERT )
		#define ENV_WORLDPOS
	#endif
	#ifdef ENV_WORLDPOS
		varying vec3 vWorldPosition;
		uniform float refractionRatio;
	#else
		varying vec3 vReflect;
	#endif
#endif`,Ed=`#ifdef USE_ENVMAP
	#if defined( USE_BUMPMAP ) || defined( USE_NORMALMAP ) || defined( PHONG ) || defined( LAMBERT )
		#define ENV_WORLDPOS
	#endif
	#ifdef ENV_WORLDPOS
		
		varying vec3 vWorldPosition;
	#else
		varying vec3 vReflect;
		uniform float refractionRatio;
	#endif
#endif`,bd=`#ifdef USE_ENVMAP
	#ifdef ENV_WORLDPOS
		vWorldPosition = worldPosition.xyz;
	#else
		vec3 cameraToVertex;
		if ( isOrthographic ) {
			cameraToVertex = normalize( vec3( - viewMatrix[ 0 ][ 2 ], - viewMatrix[ 1 ][ 2 ], - viewMatrix[ 2 ][ 2 ] ) );
		} else {
			cameraToVertex = normalize( worldPosition.xyz - cameraPosition );
		}
		vec3 worldNormal = inverseTransformDirection( transformedNormal, viewMatrix );
		#ifdef ENVMAP_MODE_REFLECTION
			vReflect = reflect( cameraToVertex, worldNormal );
		#else
			vReflect = refract( cameraToVertex, worldNormal, refractionRatio );
		#endif
	#endif
#endif`,yd=`#ifdef USE_FOG
	vFogDepth = - mvPosition.z;
#endif`,Td=`#ifdef USE_FOG
	varying float vFogDepth;
#endif`,wd=`#ifdef USE_FOG
	#ifdef FOG_EXP2
		float fogFactor = 1.0 - exp( - fogDensity * fogDensity * vFogDepth * vFogDepth );
	#else
		float fogFactor = smoothstep( fogNear, fogFar, vFogDepth );
	#endif
	gl_FragColor.rgb = mix( gl_FragColor.rgb, fogColor, fogFactor );
#endif`,Ad=`#ifdef USE_FOG
	uniform vec3 fogColor;
	varying float vFogDepth;
	#ifdef FOG_EXP2
		uniform float fogDensity;
	#else
		uniform float fogNear;
		uniform float fogFar;
	#endif
#endif`,Rd=`#ifdef USE_GRADIENTMAP
	uniform sampler2D gradientMap;
#endif
vec3 getGradientIrradiance( vec3 normal, vec3 lightDirection ) {
	float dotNL = dot( normal, lightDirection );
	vec2 coord = vec2( dotNL * 0.5 + 0.5, 0.0 );
	#ifdef USE_GRADIENTMAP
		return vec3( texture2D( gradientMap, coord ).r );
	#else
		vec2 fw = fwidth( coord ) * 0.5;
		return mix( vec3( 0.7 ), vec3( 1.0 ), smoothstep( 0.7 - fw.x, 0.7 + fw.x, coord.x ) );
	#endif
}`,Cd=`#ifdef USE_LIGHTMAP
	uniform sampler2D lightMap;
	uniform float lightMapIntensity;
#endif`,Pd=`LambertMaterial material;
material.diffuseColor = diffuseColor.rgb;
material.specularStrength = specularStrength;`,Dd=`varying vec3 vViewPosition;
struct LambertMaterial {
	vec3 diffuseColor;
	float specularStrength;
};
void RE_Direct_Lambert( const in IncidentLight directLight, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in LambertMaterial material, inout ReflectedLight reflectedLight ) {
	float dotNL = saturate( dot( geometryNormal, directLight.direction ) );
	vec3 irradiance = dotNL * directLight.color;
	reflectedLight.directDiffuse += irradiance * BRDF_Lambert( material.diffuseColor );
}
void RE_IndirectDiffuse_Lambert( const in vec3 irradiance, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in LambertMaterial material, inout ReflectedLight reflectedLight ) {
	reflectedLight.indirectDiffuse += irradiance * BRDF_Lambert( material.diffuseColor );
}
#define RE_Direct				RE_Direct_Lambert
#define RE_IndirectDiffuse		RE_IndirectDiffuse_Lambert`,Ld=`uniform bool receiveShadow;
uniform vec3 ambientLightColor;
#if defined( USE_LIGHT_PROBES )
	uniform vec3 lightProbe[ 9 ];
#endif
vec3 shGetIrradianceAt( in vec3 normal, in vec3 shCoefficients[ 9 ] ) {
	float x = normal.x, y = normal.y, z = normal.z;
	vec3 result = shCoefficients[ 0 ] * 0.886227;
	result += shCoefficients[ 1 ] * 2.0 * 0.511664 * y;
	result += shCoefficients[ 2 ] * 2.0 * 0.511664 * z;
	result += shCoefficients[ 3 ] * 2.0 * 0.511664 * x;
	result += shCoefficients[ 4 ] * 2.0 * 0.429043 * x * y;
	result += shCoefficients[ 5 ] * 2.0 * 0.429043 * y * z;
	result += shCoefficients[ 6 ] * ( 0.743125 * z * z - 0.247708 );
	result += shCoefficients[ 7 ] * 2.0 * 0.429043 * x * z;
	result += shCoefficients[ 8 ] * 0.429043 * ( x * x - y * y );
	return result;
}
vec3 getLightProbeIrradiance( const in vec3 lightProbe[ 9 ], const in vec3 normal ) {
	vec3 worldNormal = inverseTransformDirection( normal, viewMatrix );
	vec3 irradiance = shGetIrradianceAt( worldNormal, lightProbe );
	return irradiance;
}
vec3 getAmbientLightIrradiance( const in vec3 ambientLightColor ) {
	vec3 irradiance = ambientLightColor;
	return irradiance;
}
float getDistanceAttenuation( const in float lightDistance, const in float cutoffDistance, const in float decayExponent ) {
	float distanceFalloff = 1.0 / max( pow( lightDistance, decayExponent ), 0.01 );
	if ( cutoffDistance > 0.0 ) {
		distanceFalloff *= pow2( saturate( 1.0 - pow4( lightDistance / cutoffDistance ) ) );
	}
	return distanceFalloff;
}
float getSpotAttenuation( const in float coneCosine, const in float penumbraCosine, const in float angleCosine ) {
	return smoothstep( coneCosine, penumbraCosine, angleCosine );
}
#if NUM_DIR_LIGHTS > 0
	struct DirectionalLight {
		vec3 direction;
		vec3 color;
	};
	uniform DirectionalLight directionalLights[ NUM_DIR_LIGHTS ];
	void getDirectionalLightInfo( const in DirectionalLight directionalLight, out IncidentLight light ) {
		light.color = directionalLight.color;
		light.direction = directionalLight.direction;
		light.visible = true;
	}
#endif
#if NUM_POINT_LIGHTS > 0
	struct PointLight {
		vec3 position;
		vec3 color;
		float distance;
		float decay;
	};
	uniform PointLight pointLights[ NUM_POINT_LIGHTS ];
	void getPointLightInfo( const in PointLight pointLight, const in vec3 geometryPosition, out IncidentLight light ) {
		vec3 lVector = pointLight.position - geometryPosition;
		light.direction = normalize( lVector );
		float lightDistance = length( lVector );
		light.color = pointLight.color;
		light.color *= getDistanceAttenuation( lightDistance, pointLight.distance, pointLight.decay );
		light.visible = ( light.color != vec3( 0.0 ) );
	}
#endif
#if NUM_SPOT_LIGHTS > 0
	struct SpotLight {
		vec3 position;
		vec3 direction;
		vec3 color;
		float distance;
		float decay;
		float coneCos;
		float penumbraCos;
	};
	uniform SpotLight spotLights[ NUM_SPOT_LIGHTS ];
	void getSpotLightInfo( const in SpotLight spotLight, const in vec3 geometryPosition, out IncidentLight light ) {
		vec3 lVector = spotLight.position - geometryPosition;
		light.direction = normalize( lVector );
		float angleCos = dot( light.direction, spotLight.direction );
		float spotAttenuation = getSpotAttenuation( spotLight.coneCos, spotLight.penumbraCos, angleCos );
		if ( spotAttenuation > 0.0 ) {
			float lightDistance = length( lVector );
			light.color = spotLight.color * spotAttenuation;
			light.color *= getDistanceAttenuation( lightDistance, spotLight.distance, spotLight.decay );
			light.visible = ( light.color != vec3( 0.0 ) );
		} else {
			light.color = vec3( 0.0 );
			light.visible = false;
		}
	}
#endif
#if NUM_RECT_AREA_LIGHTS > 0
	struct RectAreaLight {
		vec3 color;
		vec3 position;
		vec3 halfWidth;
		vec3 halfHeight;
	};
	uniform sampler2D ltc_1;	uniform sampler2D ltc_2;
	uniform RectAreaLight rectAreaLights[ NUM_RECT_AREA_LIGHTS ];
#endif
#if NUM_HEMI_LIGHTS > 0
	struct HemisphereLight {
		vec3 direction;
		vec3 skyColor;
		vec3 groundColor;
	};
	uniform HemisphereLight hemisphereLights[ NUM_HEMI_LIGHTS ];
	vec3 getHemisphereLightIrradiance( const in HemisphereLight hemiLight, const in vec3 normal ) {
		float dotNL = dot( normal, hemiLight.direction );
		float hemiDiffuseWeight = 0.5 * dotNL + 0.5;
		vec3 irradiance = mix( hemiLight.groundColor, hemiLight.skyColor, hemiDiffuseWeight );
		return irradiance;
	}
#endif`,Id=`#ifdef USE_ENVMAP
	vec3 getIBLIrradiance( const in vec3 normal ) {
		#ifdef ENVMAP_TYPE_CUBE_UV
			vec3 worldNormal = inverseTransformDirection( normal, viewMatrix );
			vec4 envMapColor = textureCubeUV( envMap, envMapRotation * worldNormal, 1.0 );
			return PI * envMapColor.rgb * envMapIntensity;
		#else
			return vec3( 0.0 );
		#endif
	}
	vec3 getIBLRadiance( const in vec3 viewDir, const in vec3 normal, const in float roughness ) {
		#ifdef ENVMAP_TYPE_CUBE_UV
			vec3 reflectVec = reflect( - viewDir, normal );
			reflectVec = normalize( mix( reflectVec, normal, roughness * roughness) );
			reflectVec = inverseTransformDirection( reflectVec, viewMatrix );
			vec4 envMapColor = textureCubeUV( envMap, envMapRotation * reflectVec, roughness );
			return envMapColor.rgb * envMapIntensity;
		#else
			return vec3( 0.0 );
		#endif
	}
	#ifdef USE_ANISOTROPY
		vec3 getIBLAnisotropyRadiance( const in vec3 viewDir, const in vec3 normal, const in float roughness, const in vec3 bitangent, const in float anisotropy ) {
			#ifdef ENVMAP_TYPE_CUBE_UV
				vec3 bentNormal = cross( bitangent, viewDir );
				bentNormal = normalize( cross( bentNormal, bitangent ) );
				bentNormal = normalize( mix( bentNormal, normal, pow2( pow2( 1.0 - anisotropy * ( 1.0 - roughness ) ) ) ) );
				return getIBLRadiance( viewDir, bentNormal, roughness );
			#else
				return vec3( 0.0 );
			#endif
		}
	#endif
#endif`,Ud=`ToonMaterial material;
material.diffuseColor = diffuseColor.rgb;`,zd=`varying vec3 vViewPosition;
struct ToonMaterial {
	vec3 diffuseColor;
};
void RE_Direct_Toon( const in IncidentLight directLight, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in ToonMaterial material, inout ReflectedLight reflectedLight ) {
	vec3 irradiance = getGradientIrradiance( geometryNormal, directLight.direction ) * directLight.color;
	reflectedLight.directDiffuse += irradiance * BRDF_Lambert( material.diffuseColor );
}
void RE_IndirectDiffuse_Toon( const in vec3 irradiance, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in ToonMaterial material, inout ReflectedLight reflectedLight ) {
	reflectedLight.indirectDiffuse += irradiance * BRDF_Lambert( material.diffuseColor );
}
#define RE_Direct				RE_Direct_Toon
#define RE_IndirectDiffuse		RE_IndirectDiffuse_Toon`,Nd=`BlinnPhongMaterial material;
material.diffuseColor = diffuseColor.rgb;
material.specularColor = specular;
material.specularShininess = shininess;
material.specularStrength = specularStrength;`,kd=`varying vec3 vViewPosition;
struct BlinnPhongMaterial {
	vec3 diffuseColor;
	vec3 specularColor;
	float specularShininess;
	float specularStrength;
};
void RE_Direct_BlinnPhong( const in IncidentLight directLight, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in BlinnPhongMaterial material, inout ReflectedLight reflectedLight ) {
	float dotNL = saturate( dot( geometryNormal, directLight.direction ) );
	vec3 irradiance = dotNL * directLight.color;
	reflectedLight.directDiffuse += irradiance * BRDF_Lambert( material.diffuseColor );
	reflectedLight.directSpecular += irradiance * BRDF_BlinnPhong( directLight.direction, geometryViewDir, geometryNormal, material.specularColor, material.specularShininess ) * material.specularStrength;
}
void RE_IndirectDiffuse_BlinnPhong( const in vec3 irradiance, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in BlinnPhongMaterial material, inout ReflectedLight reflectedLight ) {
	reflectedLight.indirectDiffuse += irradiance * BRDF_Lambert( material.diffuseColor );
}
#define RE_Direct				RE_Direct_BlinnPhong
#define RE_IndirectDiffuse		RE_IndirectDiffuse_BlinnPhong`,Fd=`PhysicalMaterial material;
material.diffuseColor = diffuseColor.rgb * ( 1.0 - metalnessFactor );
vec3 dxy = max( abs( dFdx( nonPerturbedNormal ) ), abs( dFdy( nonPerturbedNormal ) ) );
float geometryRoughness = max( max( dxy.x, dxy.y ), dxy.z );
material.roughness = max( roughnessFactor, 0.0525 );material.roughness += geometryRoughness;
material.roughness = min( material.roughness, 1.0 );
#ifdef IOR
	material.ior = ior;
	#ifdef USE_SPECULAR
		float specularIntensityFactor = specularIntensity;
		vec3 specularColorFactor = specularColor;
		#ifdef USE_SPECULAR_COLORMAP
			specularColorFactor *= texture2D( specularColorMap, vSpecularColorMapUv ).rgb;
		#endif
		#ifdef USE_SPECULAR_INTENSITYMAP
			specularIntensityFactor *= texture2D( specularIntensityMap, vSpecularIntensityMapUv ).a;
		#endif
		material.specularF90 = mix( specularIntensityFactor, 1.0, metalnessFactor );
	#else
		float specularIntensityFactor = 1.0;
		vec3 specularColorFactor = vec3( 1.0 );
		material.specularF90 = 1.0;
	#endif
	material.specularColor = mix( min( pow2( ( material.ior - 1.0 ) / ( material.ior + 1.0 ) ) * specularColorFactor, vec3( 1.0 ) ) * specularIntensityFactor, diffuseColor.rgb, metalnessFactor );
#else
	material.specularColor = mix( vec3( 0.04 ), diffuseColor.rgb, metalnessFactor );
	material.specularF90 = 1.0;
#endif
#ifdef USE_CLEARCOAT
	material.clearcoat = clearcoat;
	material.clearcoatRoughness = clearcoatRoughness;
	material.clearcoatF0 = vec3( 0.04 );
	material.clearcoatF90 = 1.0;
	#ifdef USE_CLEARCOATMAP
		material.clearcoat *= texture2D( clearcoatMap, vClearcoatMapUv ).x;
	#endif
	#ifdef USE_CLEARCOAT_ROUGHNESSMAP
		material.clearcoatRoughness *= texture2D( clearcoatRoughnessMap, vClearcoatRoughnessMapUv ).y;
	#endif
	material.clearcoat = saturate( material.clearcoat );	material.clearcoatRoughness = max( material.clearcoatRoughness, 0.0525 );
	material.clearcoatRoughness += geometryRoughness;
	material.clearcoatRoughness = min( material.clearcoatRoughness, 1.0 );
#endif
#ifdef USE_DISPERSION
	material.dispersion = dispersion;
#endif
#ifdef USE_IRIDESCENCE
	material.iridescence = iridescence;
	material.iridescenceIOR = iridescenceIOR;
	#ifdef USE_IRIDESCENCEMAP
		material.iridescence *= texture2D( iridescenceMap, vIridescenceMapUv ).r;
	#endif
	#ifdef USE_IRIDESCENCE_THICKNESSMAP
		material.iridescenceThickness = (iridescenceThicknessMaximum - iridescenceThicknessMinimum) * texture2D( iridescenceThicknessMap, vIridescenceThicknessMapUv ).g + iridescenceThicknessMinimum;
	#else
		material.iridescenceThickness = iridescenceThicknessMaximum;
	#endif
#endif
#ifdef USE_SHEEN
	material.sheenColor = sheenColor;
	#ifdef USE_SHEEN_COLORMAP
		material.sheenColor *= texture2D( sheenColorMap, vSheenColorMapUv ).rgb;
	#endif
	material.sheenRoughness = clamp( sheenRoughness, 0.07, 1.0 );
	#ifdef USE_SHEEN_ROUGHNESSMAP
		material.sheenRoughness *= texture2D( sheenRoughnessMap, vSheenRoughnessMapUv ).a;
	#endif
#endif
#ifdef USE_ANISOTROPY
	#ifdef USE_ANISOTROPYMAP
		mat2 anisotropyMat = mat2( anisotropyVector.x, anisotropyVector.y, - anisotropyVector.y, anisotropyVector.x );
		vec3 anisotropyPolar = texture2D( anisotropyMap, vAnisotropyMapUv ).rgb;
		vec2 anisotropyV = anisotropyMat * normalize( 2.0 * anisotropyPolar.rg - vec2( 1.0 ) ) * anisotropyPolar.b;
	#else
		vec2 anisotropyV = anisotropyVector;
	#endif
	material.anisotropy = length( anisotropyV );
	if( material.anisotropy == 0.0 ) {
		anisotropyV = vec2( 1.0, 0.0 );
	} else {
		anisotropyV /= material.anisotropy;
		material.anisotropy = saturate( material.anisotropy );
	}
	material.alphaT = mix( pow2( material.roughness ), 1.0, pow2( material.anisotropy ) );
	material.anisotropyT = tbn[ 0 ] * anisotropyV.x + tbn[ 1 ] * anisotropyV.y;
	material.anisotropyB = tbn[ 1 ] * anisotropyV.x - tbn[ 0 ] * anisotropyV.y;
#endif`,Od=`struct PhysicalMaterial {
	vec3 diffuseColor;
	float roughness;
	vec3 specularColor;
	float specularF90;
	float dispersion;
	#ifdef USE_CLEARCOAT
		float clearcoat;
		float clearcoatRoughness;
		vec3 clearcoatF0;
		float clearcoatF90;
	#endif
	#ifdef USE_IRIDESCENCE
		float iridescence;
		float iridescenceIOR;
		float iridescenceThickness;
		vec3 iridescenceFresnel;
		vec3 iridescenceF0;
	#endif
	#ifdef USE_SHEEN
		vec3 sheenColor;
		float sheenRoughness;
	#endif
	#ifdef IOR
		float ior;
	#endif
	#ifdef USE_TRANSMISSION
		float transmission;
		float transmissionAlpha;
		float thickness;
		float attenuationDistance;
		vec3 attenuationColor;
	#endif
	#ifdef USE_ANISOTROPY
		float anisotropy;
		float alphaT;
		vec3 anisotropyT;
		vec3 anisotropyB;
	#endif
};
vec3 clearcoatSpecularDirect = vec3( 0.0 );
vec3 clearcoatSpecularIndirect = vec3( 0.0 );
vec3 sheenSpecularDirect = vec3( 0.0 );
vec3 sheenSpecularIndirect = vec3(0.0 );
vec3 Schlick_to_F0( const in vec3 f, const in float f90, const in float dotVH ) {
    float x = clamp( 1.0 - dotVH, 0.0, 1.0 );
    float x2 = x * x;
    float x5 = clamp( x * x2 * x2, 0.0, 0.9999 );
    return ( f - vec3( f90 ) * x5 ) / ( 1.0 - x5 );
}
float V_GGX_SmithCorrelated( const in float alpha, const in float dotNL, const in float dotNV ) {
	float a2 = pow2( alpha );
	float gv = dotNL * sqrt( a2 + ( 1.0 - a2 ) * pow2( dotNV ) );
	float gl = dotNV * sqrt( a2 + ( 1.0 - a2 ) * pow2( dotNL ) );
	return 0.5 / max( gv + gl, EPSILON );
}
float D_GGX( const in float alpha, const in float dotNH ) {
	float a2 = pow2( alpha );
	float denom = pow2( dotNH ) * ( a2 - 1.0 ) + 1.0;
	return RECIPROCAL_PI * a2 / pow2( denom );
}
#ifdef USE_ANISOTROPY
	float V_GGX_SmithCorrelated_Anisotropic( const in float alphaT, const in float alphaB, const in float dotTV, const in float dotBV, const in float dotTL, const in float dotBL, const in float dotNV, const in float dotNL ) {
		float gv = dotNL * length( vec3( alphaT * dotTV, alphaB * dotBV, dotNV ) );
		float gl = dotNV * length( vec3( alphaT * dotTL, alphaB * dotBL, dotNL ) );
		float v = 0.5 / ( gv + gl );
		return saturate(v);
	}
	float D_GGX_Anisotropic( const in float alphaT, const in float alphaB, const in float dotNH, const in float dotTH, const in float dotBH ) {
		float a2 = alphaT * alphaB;
		highp vec3 v = vec3( alphaB * dotTH, alphaT * dotBH, a2 * dotNH );
		highp float v2 = dot( v, v );
		float w2 = a2 / v2;
		return RECIPROCAL_PI * a2 * pow2 ( w2 );
	}
#endif
#ifdef USE_CLEARCOAT
	vec3 BRDF_GGX_Clearcoat( const in vec3 lightDir, const in vec3 viewDir, const in vec3 normal, const in PhysicalMaterial material) {
		vec3 f0 = material.clearcoatF0;
		float f90 = material.clearcoatF90;
		float roughness = material.clearcoatRoughness;
		float alpha = pow2( roughness );
		vec3 halfDir = normalize( lightDir + viewDir );
		float dotNL = saturate( dot( normal, lightDir ) );
		float dotNV = saturate( dot( normal, viewDir ) );
		float dotNH = saturate( dot( normal, halfDir ) );
		float dotVH = saturate( dot( viewDir, halfDir ) );
		vec3 F = F_Schlick( f0, f90, dotVH );
		float V = V_GGX_SmithCorrelated( alpha, dotNL, dotNV );
		float D = D_GGX( alpha, dotNH );
		return F * ( V * D );
	}
#endif
vec3 BRDF_GGX( const in vec3 lightDir, const in vec3 viewDir, const in vec3 normal, const in PhysicalMaterial material ) {
	vec3 f0 = material.specularColor;
	float f90 = material.specularF90;
	float roughness = material.roughness;
	float alpha = pow2( roughness );
	vec3 halfDir = normalize( lightDir + viewDir );
	float dotNL = saturate( dot( normal, lightDir ) );
	float dotNV = saturate( dot( normal, viewDir ) );
	float dotNH = saturate( dot( normal, halfDir ) );
	float dotVH = saturate( dot( viewDir, halfDir ) );
	vec3 F = F_Schlick( f0, f90, dotVH );
	#ifdef USE_IRIDESCENCE
		F = mix( F, material.iridescenceFresnel, material.iridescence );
	#endif
	#ifdef USE_ANISOTROPY
		float dotTL = dot( material.anisotropyT, lightDir );
		float dotTV = dot( material.anisotropyT, viewDir );
		float dotTH = dot( material.anisotropyT, halfDir );
		float dotBL = dot( material.anisotropyB, lightDir );
		float dotBV = dot( material.anisotropyB, viewDir );
		float dotBH = dot( material.anisotropyB, halfDir );
		float V = V_GGX_SmithCorrelated_Anisotropic( material.alphaT, alpha, dotTV, dotBV, dotTL, dotBL, dotNV, dotNL );
		float D = D_GGX_Anisotropic( material.alphaT, alpha, dotNH, dotTH, dotBH );
	#else
		float V = V_GGX_SmithCorrelated( alpha, dotNL, dotNV );
		float D = D_GGX( alpha, dotNH );
	#endif
	return F * ( V * D );
}
vec2 LTC_Uv( const in vec3 N, const in vec3 V, const in float roughness ) {
	const float LUT_SIZE = 64.0;
	const float LUT_SCALE = ( LUT_SIZE - 1.0 ) / LUT_SIZE;
	const float LUT_BIAS = 0.5 / LUT_SIZE;
	float dotNV = saturate( dot( N, V ) );
	vec2 uv = vec2( roughness, sqrt( 1.0 - dotNV ) );
	uv = uv * LUT_SCALE + LUT_BIAS;
	return uv;
}
float LTC_ClippedSphereFormFactor( const in vec3 f ) {
	float l = length( f );
	return max( ( l * l + f.z ) / ( l + 1.0 ), 0.0 );
}
vec3 LTC_EdgeVectorFormFactor( const in vec3 v1, const in vec3 v2 ) {
	float x = dot( v1, v2 );
	float y = abs( x );
	float a = 0.8543985 + ( 0.4965155 + 0.0145206 * y ) * y;
	float b = 3.4175940 + ( 4.1616724 + y ) * y;
	float v = a / b;
	float theta_sintheta = ( x > 0.0 ) ? v : 0.5 * inversesqrt( max( 1.0 - x * x, 1e-7 ) ) - v;
	return cross( v1, v2 ) * theta_sintheta;
}
vec3 LTC_Evaluate( const in vec3 N, const in vec3 V, const in vec3 P, const in mat3 mInv, const in vec3 rectCoords[ 4 ] ) {
	vec3 v1 = rectCoords[ 1 ] - rectCoords[ 0 ];
	vec3 v2 = rectCoords[ 3 ] - rectCoords[ 0 ];
	vec3 lightNormal = cross( v1, v2 );
	if( dot( lightNormal, P - rectCoords[ 0 ] ) < 0.0 ) return vec3( 0.0 );
	vec3 T1, T2;
	T1 = normalize( V - N * dot( V, N ) );
	T2 = - cross( N, T1 );
	mat3 mat = mInv * transposeMat3( mat3( T1, T2, N ) );
	vec3 coords[ 4 ];
	coords[ 0 ] = mat * ( rectCoords[ 0 ] - P );
	coords[ 1 ] = mat * ( rectCoords[ 1 ] - P );
	coords[ 2 ] = mat * ( rectCoords[ 2 ] - P );
	coords[ 3 ] = mat * ( rectCoords[ 3 ] - P );
	coords[ 0 ] = normalize( coords[ 0 ] );
	coords[ 1 ] = normalize( coords[ 1 ] );
	coords[ 2 ] = normalize( coords[ 2 ] );
	coords[ 3 ] = normalize( coords[ 3 ] );
	vec3 vectorFormFactor = vec3( 0.0 );
	vectorFormFactor += LTC_EdgeVectorFormFactor( coords[ 0 ], coords[ 1 ] );
	vectorFormFactor += LTC_EdgeVectorFormFactor( coords[ 1 ], coords[ 2 ] );
	vectorFormFactor += LTC_EdgeVectorFormFactor( coords[ 2 ], coords[ 3 ] );
	vectorFormFactor += LTC_EdgeVectorFormFactor( coords[ 3 ], coords[ 0 ] );
	float result = LTC_ClippedSphereFormFactor( vectorFormFactor );
	return vec3( result );
}
#if defined( USE_SHEEN )
float D_Charlie( float roughness, float dotNH ) {
	float alpha = pow2( roughness );
	float invAlpha = 1.0 / alpha;
	float cos2h = dotNH * dotNH;
	float sin2h = max( 1.0 - cos2h, 0.0078125 );
	return ( 2.0 + invAlpha ) * pow( sin2h, invAlpha * 0.5 ) / ( 2.0 * PI );
}
float V_Neubelt( float dotNV, float dotNL ) {
	return saturate( 1.0 / ( 4.0 * ( dotNL + dotNV - dotNL * dotNV ) ) );
}
vec3 BRDF_Sheen( const in vec3 lightDir, const in vec3 viewDir, const in vec3 normal, vec3 sheenColor, const in float sheenRoughness ) {
	vec3 halfDir = normalize( lightDir + viewDir );
	float dotNL = saturate( dot( normal, lightDir ) );
	float dotNV = saturate( dot( normal, viewDir ) );
	float dotNH = saturate( dot( normal, halfDir ) );
	float D = D_Charlie( sheenRoughness, dotNH );
	float V = V_Neubelt( dotNV, dotNL );
	return sheenColor * ( D * V );
}
#endif
float IBLSheenBRDF( const in vec3 normal, const in vec3 viewDir, const in float roughness ) {
	float dotNV = saturate( dot( normal, viewDir ) );
	float r2 = roughness * roughness;
	float a = roughness < 0.25 ? -339.2 * r2 + 161.4 * roughness - 25.9 : -8.48 * r2 + 14.3 * roughness - 9.95;
	float b = roughness < 0.25 ? 44.0 * r2 - 23.7 * roughness + 3.26 : 1.97 * r2 - 3.27 * roughness + 0.72;
	float DG = exp( a * dotNV + b ) + ( roughness < 0.25 ? 0.0 : 0.1 * ( roughness - 0.25 ) );
	return saturate( DG * RECIPROCAL_PI );
}
vec2 DFGApprox( const in vec3 normal, const in vec3 viewDir, const in float roughness ) {
	float dotNV = saturate( dot( normal, viewDir ) );
	const vec4 c0 = vec4( - 1, - 0.0275, - 0.572, 0.022 );
	const vec4 c1 = vec4( 1, 0.0425, 1.04, - 0.04 );
	vec4 r = roughness * c0 + c1;
	float a004 = min( r.x * r.x, exp2( - 9.28 * dotNV ) ) * r.x + r.y;
	vec2 fab = vec2( - 1.04, 1.04 ) * a004 + r.zw;
	return fab;
}
vec3 EnvironmentBRDF( const in vec3 normal, const in vec3 viewDir, const in vec3 specularColor, const in float specularF90, const in float roughness ) {
	vec2 fab = DFGApprox( normal, viewDir, roughness );
	return specularColor * fab.x + specularF90 * fab.y;
}
#ifdef USE_IRIDESCENCE
void computeMultiscatteringIridescence( const in vec3 normal, const in vec3 viewDir, const in vec3 specularColor, const in float specularF90, const in float iridescence, const in vec3 iridescenceF0, const in float roughness, inout vec3 singleScatter, inout vec3 multiScatter ) {
#else
void computeMultiscattering( const in vec3 normal, const in vec3 viewDir, const in vec3 specularColor, const in float specularF90, const in float roughness, inout vec3 singleScatter, inout vec3 multiScatter ) {
#endif
	vec2 fab = DFGApprox( normal, viewDir, roughness );
	#ifdef USE_IRIDESCENCE
		vec3 Fr = mix( specularColor, iridescenceF0, iridescence );
	#else
		vec3 Fr = specularColor;
	#endif
	vec3 FssEss = Fr * fab.x + specularF90 * fab.y;
	float Ess = fab.x + fab.y;
	float Ems = 1.0 - Ess;
	vec3 Favg = Fr + ( 1.0 - Fr ) * 0.047619;	vec3 Fms = FssEss * Favg / ( 1.0 - Ems * Favg );
	singleScatter += FssEss;
	multiScatter += Fms * Ems;
}
#if NUM_RECT_AREA_LIGHTS > 0
	void RE_Direct_RectArea_Physical( const in RectAreaLight rectAreaLight, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in PhysicalMaterial material, inout ReflectedLight reflectedLight ) {
		vec3 normal = geometryNormal;
		vec3 viewDir = geometryViewDir;
		vec3 position = geometryPosition;
		vec3 lightPos = rectAreaLight.position;
		vec3 halfWidth = rectAreaLight.halfWidth;
		vec3 halfHeight = rectAreaLight.halfHeight;
		vec3 lightColor = rectAreaLight.color;
		float roughness = material.roughness;
		vec3 rectCoords[ 4 ];
		rectCoords[ 0 ] = lightPos + halfWidth - halfHeight;		rectCoords[ 1 ] = lightPos - halfWidth - halfHeight;
		rectCoords[ 2 ] = lightPos - halfWidth + halfHeight;
		rectCoords[ 3 ] = lightPos + halfWidth + halfHeight;
		vec2 uv = LTC_Uv( normal, viewDir, roughness );
		vec4 t1 = texture2D( ltc_1, uv );
		vec4 t2 = texture2D( ltc_2, uv );
		mat3 mInv = mat3(
			vec3( t1.x, 0, t1.y ),
			vec3(    0, 1,    0 ),
			vec3( t1.z, 0, t1.w )
		);
		vec3 fresnel = ( material.specularColor * t2.x + ( vec3( 1.0 ) - material.specularColor ) * t2.y );
		reflectedLight.directSpecular += lightColor * fresnel * LTC_Evaluate( normal, viewDir, position, mInv, rectCoords );
		reflectedLight.directDiffuse += lightColor * material.diffuseColor * LTC_Evaluate( normal, viewDir, position, mat3( 1.0 ), rectCoords );
	}
#endif
void RE_Direct_Physical( const in IncidentLight directLight, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in PhysicalMaterial material, inout ReflectedLight reflectedLight ) {
	float dotNL = saturate( dot( geometryNormal, directLight.direction ) );
	vec3 irradiance = dotNL * directLight.color;
	#ifdef USE_CLEARCOAT
		float dotNLcc = saturate( dot( geometryClearcoatNormal, directLight.direction ) );
		vec3 ccIrradiance = dotNLcc * directLight.color;
		clearcoatSpecularDirect += ccIrradiance * BRDF_GGX_Clearcoat( directLight.direction, geometryViewDir, geometryClearcoatNormal, material );
	#endif
	#ifdef USE_SHEEN
		sheenSpecularDirect += irradiance * BRDF_Sheen( directLight.direction, geometryViewDir, geometryNormal, material.sheenColor, material.sheenRoughness );
	#endif
	reflectedLight.directSpecular += irradiance * BRDF_GGX( directLight.direction, geometryViewDir, geometryNormal, material );
	reflectedLight.directDiffuse += irradiance * BRDF_Lambert( material.diffuseColor );
}
void RE_IndirectDiffuse_Physical( const in vec3 irradiance, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in PhysicalMaterial material, inout ReflectedLight reflectedLight ) {
	reflectedLight.indirectDiffuse += irradiance * BRDF_Lambert( material.diffuseColor );
}
void RE_IndirectSpecular_Physical( const in vec3 radiance, const in vec3 irradiance, const in vec3 clearcoatRadiance, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in PhysicalMaterial material, inout ReflectedLight reflectedLight) {
	#ifdef USE_CLEARCOAT
		clearcoatSpecularIndirect += clearcoatRadiance * EnvironmentBRDF( geometryClearcoatNormal, geometryViewDir, material.clearcoatF0, material.clearcoatF90, material.clearcoatRoughness );
	#endif
	#ifdef USE_SHEEN
		sheenSpecularIndirect += irradiance * material.sheenColor * IBLSheenBRDF( geometryNormal, geometryViewDir, material.sheenRoughness );
	#endif
	vec3 singleScattering = vec3( 0.0 );
	vec3 multiScattering = vec3( 0.0 );
	vec3 cosineWeightedIrradiance = irradiance * RECIPROCAL_PI;
	#ifdef USE_IRIDESCENCE
		computeMultiscatteringIridescence( geometryNormal, geometryViewDir, material.specularColor, material.specularF90, material.iridescence, material.iridescenceFresnel, material.roughness, singleScattering, multiScattering );
	#else
		computeMultiscattering( geometryNormal, geometryViewDir, material.specularColor, material.specularF90, material.roughness, singleScattering, multiScattering );
	#endif
	vec3 totalScattering = singleScattering + multiScattering;
	vec3 diffuse = material.diffuseColor * ( 1.0 - max( max( totalScattering.r, totalScattering.g ), totalScattering.b ) );
	reflectedLight.indirectSpecular += radiance * singleScattering;
	reflectedLight.indirectSpecular += multiScattering * cosineWeightedIrradiance;
	reflectedLight.indirectDiffuse += diffuse * cosineWeightedIrradiance;
}
#define RE_Direct				RE_Direct_Physical
#define RE_Direct_RectArea		RE_Direct_RectArea_Physical
#define RE_IndirectDiffuse		RE_IndirectDiffuse_Physical
#define RE_IndirectSpecular		RE_IndirectSpecular_Physical
float computeSpecularOcclusion( const in float dotNV, const in float ambientOcclusion, const in float roughness ) {
	return saturate( pow( dotNV + ambientOcclusion, exp2( - 16.0 * roughness - 1.0 ) ) - 1.0 + ambientOcclusion );
}`,Bd=`
vec3 geometryPosition = - vViewPosition;
vec3 geometryNormal = normal;
vec3 geometryViewDir = ( isOrthographic ) ? vec3( 0, 0, 1 ) : normalize( vViewPosition );
vec3 geometryClearcoatNormal = vec3( 0.0 );
#ifdef USE_CLEARCOAT
	geometryClearcoatNormal = clearcoatNormal;
#endif
#ifdef USE_IRIDESCENCE
	float dotNVi = saturate( dot( normal, geometryViewDir ) );
	if ( material.iridescenceThickness == 0.0 ) {
		material.iridescence = 0.0;
	} else {
		material.iridescence = saturate( material.iridescence );
	}
	if ( material.iridescence > 0.0 ) {
		material.iridescenceFresnel = evalIridescence( 1.0, material.iridescenceIOR, dotNVi, material.iridescenceThickness, material.specularColor );
		material.iridescenceF0 = Schlick_to_F0( material.iridescenceFresnel, 1.0, dotNVi );
	}
#endif
IncidentLight directLight;
#if ( NUM_POINT_LIGHTS > 0 ) && defined( RE_Direct )
	PointLight pointLight;
	#if defined( USE_SHADOWMAP ) && NUM_POINT_LIGHT_SHADOWS > 0
	PointLightShadow pointLightShadow;
	#endif
	#pragma unroll_loop_start
	for ( int i = 0; i < NUM_POINT_LIGHTS; i ++ ) {
		pointLight = pointLights[ i ];
		getPointLightInfo( pointLight, geometryPosition, directLight );
		#if defined( USE_SHADOWMAP ) && ( UNROLLED_LOOP_INDEX < NUM_POINT_LIGHT_SHADOWS )
		pointLightShadow = pointLightShadows[ i ];
		directLight.color *= ( directLight.visible && receiveShadow ) ? getPointShadow( pointShadowMap[ i ], pointLightShadow.shadowMapSize, pointLightShadow.shadowIntensity, pointLightShadow.shadowBias, pointLightShadow.shadowRadius, vPointShadowCoord[ i ], pointLightShadow.shadowCameraNear, pointLightShadow.shadowCameraFar ) : 1.0;
		#endif
		RE_Direct( directLight, geometryPosition, geometryNormal, geometryViewDir, geometryClearcoatNormal, material, reflectedLight );
	}
	#pragma unroll_loop_end
#endif
#if ( NUM_SPOT_LIGHTS > 0 ) && defined( RE_Direct )
	SpotLight spotLight;
	vec4 spotColor;
	vec3 spotLightCoord;
	bool inSpotLightMap;
	#if defined( USE_SHADOWMAP ) && NUM_SPOT_LIGHT_SHADOWS > 0
	SpotLightShadow spotLightShadow;
	#endif
	#pragma unroll_loop_start
	for ( int i = 0; i < NUM_SPOT_LIGHTS; i ++ ) {
		spotLight = spotLights[ i ];
		getSpotLightInfo( spotLight, geometryPosition, directLight );
		#if ( UNROLLED_LOOP_INDEX < NUM_SPOT_LIGHT_SHADOWS_WITH_MAPS )
		#define SPOT_LIGHT_MAP_INDEX UNROLLED_LOOP_INDEX
		#elif ( UNROLLED_LOOP_INDEX < NUM_SPOT_LIGHT_SHADOWS )
		#define SPOT_LIGHT_MAP_INDEX NUM_SPOT_LIGHT_MAPS
		#else
		#define SPOT_LIGHT_MAP_INDEX ( UNROLLED_LOOP_INDEX - NUM_SPOT_LIGHT_SHADOWS + NUM_SPOT_LIGHT_SHADOWS_WITH_MAPS )
		#endif
		#if ( SPOT_LIGHT_MAP_INDEX < NUM_SPOT_LIGHT_MAPS )
			spotLightCoord = vSpotLightCoord[ i ].xyz / vSpotLightCoord[ i ].w;
			inSpotLightMap = all( lessThan( abs( spotLightCoord * 2. - 1. ), vec3( 1.0 ) ) );
			spotColor = texture2D( spotLightMap[ SPOT_LIGHT_MAP_INDEX ], spotLightCoord.xy );
			directLight.color = inSpotLightMap ? directLight.color * spotColor.rgb : directLight.color;
		#endif
		#undef SPOT_LIGHT_MAP_INDEX
		#if defined( USE_SHADOWMAP ) && ( UNROLLED_LOOP_INDEX < NUM_SPOT_LIGHT_SHADOWS )
		spotLightShadow = spotLightShadows[ i ];
		directLight.color *= ( directLight.visible && receiveShadow ) ? getShadow( spotShadowMap[ i ], spotLightShadow.shadowMapSize, spotLightShadow.shadowIntensity, spotLightShadow.shadowBias, spotLightShadow.shadowRadius, vSpotLightCoord[ i ] ) : 1.0;
		#endif
		RE_Direct( directLight, geometryPosition, geometryNormal, geometryViewDir, geometryClearcoatNormal, material, reflectedLight );
	}
	#pragma unroll_loop_end
#endif
#if ( NUM_DIR_LIGHTS > 0 ) && defined( RE_Direct )
	DirectionalLight directionalLight;
	#if defined( USE_SHADOWMAP ) && NUM_DIR_LIGHT_SHADOWS > 0
	DirectionalLightShadow directionalLightShadow;
	#endif
	#pragma unroll_loop_start
	for ( int i = 0; i < NUM_DIR_LIGHTS; i ++ ) {
		directionalLight = directionalLights[ i ];
		getDirectionalLightInfo( directionalLight, directLight );
		#if defined( USE_SHADOWMAP ) && ( UNROLLED_LOOP_INDEX < NUM_DIR_LIGHT_SHADOWS )
		directionalLightShadow = directionalLightShadows[ i ];
		directLight.color *= ( directLight.visible && receiveShadow ) ? getShadow( directionalShadowMap[ i ], directionalLightShadow.shadowMapSize, directionalLightShadow.shadowIntensity, directionalLightShadow.shadowBias, directionalLightShadow.shadowRadius, vDirectionalShadowCoord[ i ] ) : 1.0;
		#endif
		RE_Direct( directLight, geometryPosition, geometryNormal, geometryViewDir, geometryClearcoatNormal, material, reflectedLight );
	}
	#pragma unroll_loop_end
#endif
#if ( NUM_RECT_AREA_LIGHTS > 0 ) && defined( RE_Direct_RectArea )
	RectAreaLight rectAreaLight;
	#pragma unroll_loop_start
	for ( int i = 0; i < NUM_RECT_AREA_LIGHTS; i ++ ) {
		rectAreaLight = rectAreaLights[ i ];
		RE_Direct_RectArea( rectAreaLight, geometryPosition, geometryNormal, geometryViewDir, geometryClearcoatNormal, material, reflectedLight );
	}
	#pragma unroll_loop_end
#endif
#if defined( RE_IndirectDiffuse )
	vec3 iblIrradiance = vec3( 0.0 );
	vec3 irradiance = getAmbientLightIrradiance( ambientLightColor );
	#if defined( USE_LIGHT_PROBES )
		irradiance += getLightProbeIrradiance( lightProbe, geometryNormal );
	#endif
	#if ( NUM_HEMI_LIGHTS > 0 )
		#pragma unroll_loop_start
		for ( int i = 0; i < NUM_HEMI_LIGHTS; i ++ ) {
			irradiance += getHemisphereLightIrradiance( hemisphereLights[ i ], geometryNormal );
		}
		#pragma unroll_loop_end
	#endif
#endif
#if defined( RE_IndirectSpecular )
	vec3 radiance = vec3( 0.0 );
	vec3 clearcoatRadiance = vec3( 0.0 );
#endif`,jd=`#if defined( RE_IndirectDiffuse )
	#ifdef USE_LIGHTMAP
		vec4 lightMapTexel = texture2D( lightMap, vLightMapUv );
		vec3 lightMapIrradiance = lightMapTexel.rgb * lightMapIntensity;
		irradiance += lightMapIrradiance;
	#endif
	#if defined( USE_ENVMAP ) && defined( STANDARD ) && defined( ENVMAP_TYPE_CUBE_UV )
		iblIrradiance += getIBLIrradiance( geometryNormal );
	#endif
#endif
#if defined( USE_ENVMAP ) && defined( RE_IndirectSpecular )
	#ifdef USE_ANISOTROPY
		radiance += getIBLAnisotropyRadiance( geometryViewDir, geometryNormal, material.roughness, material.anisotropyB, material.anisotropy );
	#else
		radiance += getIBLRadiance( geometryViewDir, geometryNormal, material.roughness );
	#endif
	#ifdef USE_CLEARCOAT
		clearcoatRadiance += getIBLRadiance( geometryViewDir, geometryClearcoatNormal, material.clearcoatRoughness );
	#endif
#endif`,Vd=`#if defined( RE_IndirectDiffuse )
	RE_IndirectDiffuse( irradiance, geometryPosition, geometryNormal, geometryViewDir, geometryClearcoatNormal, material, reflectedLight );
#endif
#if defined( RE_IndirectSpecular )
	RE_IndirectSpecular( radiance, iblIrradiance, clearcoatRadiance, geometryPosition, geometryNormal, geometryViewDir, geometryClearcoatNormal, material, reflectedLight );
#endif`,Hd=`#if defined( USE_LOGDEPTHBUF )
	gl_FragDepth = vIsPerspective == 0.0 ? gl_FragCoord.z : log2( vFragDepth ) * logDepthBufFC * 0.5;
#endif`,Gd=`#if defined( USE_LOGDEPTHBUF )
	uniform float logDepthBufFC;
	varying float vFragDepth;
	varying float vIsPerspective;
#endif`,Wd=`#ifdef USE_LOGDEPTHBUF
	varying float vFragDepth;
	varying float vIsPerspective;
#endif`,Xd=`#ifdef USE_LOGDEPTHBUF
	vFragDepth = 1.0 + gl_Position.w;
	vIsPerspective = float( isPerspectiveMatrix( projectionMatrix ) );
#endif`,Kd=`#ifdef USE_MAP
	vec4 sampledDiffuseColor = texture2D( map, vMapUv );
	#ifdef DECODE_VIDEO_TEXTURE
		sampledDiffuseColor = sRGBTransferEOTF( sampledDiffuseColor );
	#endif
	diffuseColor *= sampledDiffuseColor;
#endif`,qd=`#ifdef USE_MAP
	uniform sampler2D map;
#endif`,$d=`#if defined( USE_MAP ) || defined( USE_ALPHAMAP )
	#if defined( USE_POINTS_UV )
		vec2 uv = vUv;
	#else
		vec2 uv = ( uvTransform * vec3( gl_PointCoord.x, 1.0 - gl_PointCoord.y, 1 ) ).xy;
	#endif
#endif
#ifdef USE_MAP
	diffuseColor *= texture2D( map, uv );
#endif
#ifdef USE_ALPHAMAP
	diffuseColor.a *= texture2D( alphaMap, uv ).g;
#endif`,Yd=`#if defined( USE_POINTS_UV )
	varying vec2 vUv;
#else
	#if defined( USE_MAP ) || defined( USE_ALPHAMAP )
		uniform mat3 uvTransform;
	#endif
#endif
#ifdef USE_MAP
	uniform sampler2D map;
#endif
#ifdef USE_ALPHAMAP
	uniform sampler2D alphaMap;
#endif`,Zd=`float metalnessFactor = metalness;
#ifdef USE_METALNESSMAP
	vec4 texelMetalness = texture2D( metalnessMap, vMetalnessMapUv );
	metalnessFactor *= texelMetalness.b;
#endif`,Jd=`#ifdef USE_METALNESSMAP
	uniform sampler2D metalnessMap;
#endif`,Qd=`#ifdef USE_INSTANCING_MORPH
	float morphTargetInfluences[ MORPHTARGETS_COUNT ];
	float morphTargetBaseInfluence = texelFetch( morphTexture, ivec2( 0, gl_InstanceID ), 0 ).r;
	for ( int i = 0; i < MORPHTARGETS_COUNT; i ++ ) {
		morphTargetInfluences[i] =  texelFetch( morphTexture, ivec2( i + 1, gl_InstanceID ), 0 ).r;
	}
#endif`,eh=`#if defined( USE_MORPHCOLORS )
	vColor *= morphTargetBaseInfluence;
	for ( int i = 0; i < MORPHTARGETS_COUNT; i ++ ) {
		#if defined( USE_COLOR_ALPHA )
			if ( morphTargetInfluences[ i ] != 0.0 ) vColor += getMorph( gl_VertexID, i, 2 ) * morphTargetInfluences[ i ];
		#elif defined( USE_COLOR )
			if ( morphTargetInfluences[ i ] != 0.0 ) vColor += getMorph( gl_VertexID, i, 2 ).rgb * morphTargetInfluences[ i ];
		#endif
	}
#endif`,th=`#ifdef USE_MORPHNORMALS
	objectNormal *= morphTargetBaseInfluence;
	for ( int i = 0; i < MORPHTARGETS_COUNT; i ++ ) {
		if ( morphTargetInfluences[ i ] != 0.0 ) objectNormal += getMorph( gl_VertexID, i, 1 ).xyz * morphTargetInfluences[ i ];
	}
#endif`,nh=`#ifdef USE_MORPHTARGETS
	#ifndef USE_INSTANCING_MORPH
		uniform float morphTargetBaseInfluence;
		uniform float morphTargetInfluences[ MORPHTARGETS_COUNT ];
	#endif
	uniform sampler2DArray morphTargetsTexture;
	uniform ivec2 morphTargetsTextureSize;
	vec4 getMorph( const in int vertexIndex, const in int morphTargetIndex, const in int offset ) {
		int texelIndex = vertexIndex * MORPHTARGETS_TEXTURE_STRIDE + offset;
		int y = texelIndex / morphTargetsTextureSize.x;
		int x = texelIndex - y * morphTargetsTextureSize.x;
		ivec3 morphUV = ivec3( x, y, morphTargetIndex );
		return texelFetch( morphTargetsTexture, morphUV, 0 );
	}
#endif`,ih=`#ifdef USE_MORPHTARGETS
	transformed *= morphTargetBaseInfluence;
	for ( int i = 0; i < MORPHTARGETS_COUNT; i ++ ) {
		if ( morphTargetInfluences[ i ] != 0.0 ) transformed += getMorph( gl_VertexID, i, 0 ).xyz * morphTargetInfluences[ i ];
	}
#endif`,rh=`float faceDirection = gl_FrontFacing ? 1.0 : - 1.0;
#ifdef FLAT_SHADED
	vec3 fdx = dFdx( vViewPosition );
	vec3 fdy = dFdy( vViewPosition );
	vec3 normal = normalize( cross( fdx, fdy ) );
#else
	vec3 normal = normalize( vNormal );
	#ifdef DOUBLE_SIDED
		normal *= faceDirection;
	#endif
#endif
#if defined( USE_NORMALMAP_TANGENTSPACE ) || defined( USE_CLEARCOAT_NORMALMAP ) || defined( USE_ANISOTROPY )
	#ifdef USE_TANGENT
		mat3 tbn = mat3( normalize( vTangent ), normalize( vBitangent ), normal );
	#else
		mat3 tbn = getTangentFrame( - vViewPosition, normal,
		#if defined( USE_NORMALMAP )
			vNormalMapUv
		#elif defined( USE_CLEARCOAT_NORMALMAP )
			vClearcoatNormalMapUv
		#else
			vUv
		#endif
		);
	#endif
	#if defined( DOUBLE_SIDED ) && ! defined( FLAT_SHADED )
		tbn[0] *= faceDirection;
		tbn[1] *= faceDirection;
	#endif
#endif
#ifdef USE_CLEARCOAT_NORMALMAP
	#ifdef USE_TANGENT
		mat3 tbn2 = mat3( normalize( vTangent ), normalize( vBitangent ), normal );
	#else
		mat3 tbn2 = getTangentFrame( - vViewPosition, normal, vClearcoatNormalMapUv );
	#endif
	#if defined( DOUBLE_SIDED ) && ! defined( FLAT_SHADED )
		tbn2[0] *= faceDirection;
		tbn2[1] *= faceDirection;
	#endif
#endif
vec3 nonPerturbedNormal = normal;`,ah=`#ifdef USE_NORMALMAP_OBJECTSPACE
	normal = texture2D( normalMap, vNormalMapUv ).xyz * 2.0 - 1.0;
	#ifdef FLIP_SIDED
		normal = - normal;
	#endif
	#ifdef DOUBLE_SIDED
		normal = normal * faceDirection;
	#endif
	normal = normalize( normalMatrix * normal );
#elif defined( USE_NORMALMAP_TANGENTSPACE )
	vec3 mapN = texture2D( normalMap, vNormalMapUv ).xyz * 2.0 - 1.0;
	mapN.xy *= normalScale;
	normal = normalize( tbn * mapN );
#elif defined( USE_BUMPMAP )
	normal = perturbNormalArb( - vViewPosition, normal, dHdxy_fwd(), faceDirection );
#endif`,sh=`#ifndef FLAT_SHADED
	varying vec3 vNormal;
	#ifdef USE_TANGENT
		varying vec3 vTangent;
		varying vec3 vBitangent;
	#endif
#endif`,oh=`#ifndef FLAT_SHADED
	varying vec3 vNormal;
	#ifdef USE_TANGENT
		varying vec3 vTangent;
		varying vec3 vBitangent;
	#endif
#endif`,ch=`#ifndef FLAT_SHADED
	vNormal = normalize( transformedNormal );
	#ifdef USE_TANGENT
		vTangent = normalize( transformedTangent );
		vBitangent = normalize( cross( vNormal, vTangent ) * tangent.w );
	#endif
#endif`,lh=`#ifdef USE_NORMALMAP
	uniform sampler2D normalMap;
	uniform vec2 normalScale;
#endif
#ifdef USE_NORMALMAP_OBJECTSPACE
	uniform mat3 normalMatrix;
#endif
#if ! defined ( USE_TANGENT ) && ( defined ( USE_NORMALMAP_TANGENTSPACE ) || defined ( USE_CLEARCOAT_NORMALMAP ) || defined( USE_ANISOTROPY ) )
	mat3 getTangentFrame( vec3 eye_pos, vec3 surf_norm, vec2 uv ) {
		vec3 q0 = dFdx( eye_pos.xyz );
		vec3 q1 = dFdy( eye_pos.xyz );
		vec2 st0 = dFdx( uv.st );
		vec2 st1 = dFdy( uv.st );
		vec3 N = surf_norm;
		vec3 q1perp = cross( q1, N );
		vec3 q0perp = cross( N, q0 );
		vec3 T = q1perp * st0.x + q0perp * st1.x;
		vec3 B = q1perp * st0.y + q0perp * st1.y;
		float det = max( dot( T, T ), dot( B, B ) );
		float scale = ( det == 0.0 ) ? 0.0 : inversesqrt( det );
		return mat3( T * scale, B * scale, N );
	}
#endif`,uh=`#ifdef USE_CLEARCOAT
	vec3 clearcoatNormal = nonPerturbedNormal;
#endif`,dh=`#ifdef USE_CLEARCOAT_NORMALMAP
	vec3 clearcoatMapN = texture2D( clearcoatNormalMap, vClearcoatNormalMapUv ).xyz * 2.0 - 1.0;
	clearcoatMapN.xy *= clearcoatNormalScale;
	clearcoatNormal = normalize( tbn2 * clearcoatMapN );
#endif`,hh=`#ifdef USE_CLEARCOATMAP
	uniform sampler2D clearcoatMap;
#endif
#ifdef USE_CLEARCOAT_NORMALMAP
	uniform sampler2D clearcoatNormalMap;
	uniform vec2 clearcoatNormalScale;
#endif
#ifdef USE_CLEARCOAT_ROUGHNESSMAP
	uniform sampler2D clearcoatRoughnessMap;
#endif`,fh=`#ifdef USE_IRIDESCENCEMAP
	uniform sampler2D iridescenceMap;
#endif
#ifdef USE_IRIDESCENCE_THICKNESSMAP
	uniform sampler2D iridescenceThicknessMap;
#endif`,ph=`#ifdef OPAQUE
diffuseColor.a = 1.0;
#endif
#ifdef USE_TRANSMISSION
diffuseColor.a *= material.transmissionAlpha;
#endif
gl_FragColor = vec4( outgoingLight, diffuseColor.a );`,mh=`vec3 packNormalToRGB( const in vec3 normal ) {
	return normalize( normal ) * 0.5 + 0.5;
}
vec3 unpackRGBToNormal( const in vec3 rgb ) {
	return 2.0 * rgb.xyz - 1.0;
}
const float PackUpscale = 256. / 255.;const float UnpackDownscale = 255. / 256.;const float ShiftRight8 = 1. / 256.;
const float Inv255 = 1. / 255.;
const vec4 PackFactors = vec4( 1.0, 256.0, 256.0 * 256.0, 256.0 * 256.0 * 256.0 );
const vec2 UnpackFactors2 = vec2( UnpackDownscale, 1.0 / PackFactors.g );
const vec3 UnpackFactors3 = vec3( UnpackDownscale / PackFactors.rg, 1.0 / PackFactors.b );
const vec4 UnpackFactors4 = vec4( UnpackDownscale / PackFactors.rgb, 1.0 / PackFactors.a );
vec4 packDepthToRGBA( const in float v ) {
	if( v <= 0.0 )
		return vec4( 0., 0., 0., 0. );
	if( v >= 1.0 )
		return vec4( 1., 1., 1., 1. );
	float vuf;
	float af = modf( v * PackFactors.a, vuf );
	float bf = modf( vuf * ShiftRight8, vuf );
	float gf = modf( vuf * ShiftRight8, vuf );
	return vec4( vuf * Inv255, gf * PackUpscale, bf * PackUpscale, af );
}
vec3 packDepthToRGB( const in float v ) {
	if( v <= 0.0 )
		return vec3( 0., 0., 0. );
	if( v >= 1.0 )
		return vec3( 1., 1., 1. );
	float vuf;
	float bf = modf( v * PackFactors.b, vuf );
	float gf = modf( vuf * ShiftRight8, vuf );
	return vec3( vuf * Inv255, gf * PackUpscale, bf );
}
vec2 packDepthToRG( const in float v ) {
	if( v <= 0.0 )
		return vec2( 0., 0. );
	if( v >= 1.0 )
		return vec2( 1., 1. );
	float vuf;
	float gf = modf( v * 256., vuf );
	return vec2( vuf * Inv255, gf );
}
float unpackRGBAToDepth( const in vec4 v ) {
	return dot( v, UnpackFactors4 );
}
float unpackRGBToDepth( const in vec3 v ) {
	return dot( v, UnpackFactors3 );
}
float unpackRGToDepth( const in vec2 v ) {
	return v.r * UnpackFactors2.r + v.g * UnpackFactors2.g;
}
vec4 pack2HalfToRGBA( const in vec2 v ) {
	vec4 r = vec4( v.x, fract( v.x * 255.0 ), v.y, fract( v.y * 255.0 ) );
	return vec4( r.x - r.y / 255.0, r.y, r.z - r.w / 255.0, r.w );
}
vec2 unpackRGBATo2Half( const in vec4 v ) {
	return vec2( v.x + ( v.y / 255.0 ), v.z + ( v.w / 255.0 ) );
}
float viewZToOrthographicDepth( const in float viewZ, const in float near, const in float far ) {
	return ( viewZ + near ) / ( near - far );
}
float orthographicDepthToViewZ( const in float depth, const in float near, const in float far ) {
	return depth * ( near - far ) - near;
}
float viewZToPerspectiveDepth( const in float viewZ, const in float near, const in float far ) {
	return ( ( near + viewZ ) * far ) / ( ( far - near ) * viewZ );
}
float perspectiveDepthToViewZ( const in float depth, const in float near, const in float far ) {
	return ( near * far ) / ( ( far - near ) * depth - far );
}`,gh=`#ifdef PREMULTIPLIED_ALPHA
	gl_FragColor.rgb *= gl_FragColor.a;
#endif`,_h=`vec4 mvPosition = vec4( transformed, 1.0 );
#ifdef USE_BATCHING
	mvPosition = batchingMatrix * mvPosition;
#endif
#ifdef USE_INSTANCING
	mvPosition = instanceMatrix * mvPosition;
#endif
mvPosition = modelViewMatrix * mvPosition;
gl_Position = projectionMatrix * mvPosition;`,vh=`#ifdef DITHERING
	gl_FragColor.rgb = dithering( gl_FragColor.rgb );
#endif`,xh=`#ifdef DITHERING
	vec3 dithering( vec3 color ) {
		float grid_position = rand( gl_FragCoord.xy );
		vec3 dither_shift_RGB = vec3( 0.25 / 255.0, -0.25 / 255.0, 0.25 / 255.0 );
		dither_shift_RGB = mix( 2.0 * dither_shift_RGB, -2.0 * dither_shift_RGB, grid_position );
		return color + dither_shift_RGB;
	}
#endif`,Mh=`float roughnessFactor = roughness;
#ifdef USE_ROUGHNESSMAP
	vec4 texelRoughness = texture2D( roughnessMap, vRoughnessMapUv );
	roughnessFactor *= texelRoughness.g;
#endif`,Sh=`#ifdef USE_ROUGHNESSMAP
	uniform sampler2D roughnessMap;
#endif`,Eh=`#if NUM_SPOT_LIGHT_COORDS > 0
	varying vec4 vSpotLightCoord[ NUM_SPOT_LIGHT_COORDS ];
#endif
#if NUM_SPOT_LIGHT_MAPS > 0
	uniform sampler2D spotLightMap[ NUM_SPOT_LIGHT_MAPS ];
#endif
#ifdef USE_SHADOWMAP
	#if NUM_DIR_LIGHT_SHADOWS > 0
		uniform sampler2D directionalShadowMap[ NUM_DIR_LIGHT_SHADOWS ];
		varying vec4 vDirectionalShadowCoord[ NUM_DIR_LIGHT_SHADOWS ];
		struct DirectionalLightShadow {
			float shadowIntensity;
			float shadowBias;
			float shadowNormalBias;
			float shadowRadius;
			vec2 shadowMapSize;
		};
		uniform DirectionalLightShadow directionalLightShadows[ NUM_DIR_LIGHT_SHADOWS ];
	#endif
	#if NUM_SPOT_LIGHT_SHADOWS > 0
		uniform sampler2D spotShadowMap[ NUM_SPOT_LIGHT_SHADOWS ];
		struct SpotLightShadow {
			float shadowIntensity;
			float shadowBias;
			float shadowNormalBias;
			float shadowRadius;
			vec2 shadowMapSize;
		};
		uniform SpotLightShadow spotLightShadows[ NUM_SPOT_LIGHT_SHADOWS ];
	#endif
	#if NUM_POINT_LIGHT_SHADOWS > 0
		uniform sampler2D pointShadowMap[ NUM_POINT_LIGHT_SHADOWS ];
		varying vec4 vPointShadowCoord[ NUM_POINT_LIGHT_SHADOWS ];
		struct PointLightShadow {
			float shadowIntensity;
			float shadowBias;
			float shadowNormalBias;
			float shadowRadius;
			vec2 shadowMapSize;
			float shadowCameraNear;
			float shadowCameraFar;
		};
		uniform PointLightShadow pointLightShadows[ NUM_POINT_LIGHT_SHADOWS ];
	#endif
	float texture2DCompare( sampler2D depths, vec2 uv, float compare ) {
		return step( compare, unpackRGBAToDepth( texture2D( depths, uv ) ) );
	}
	vec2 texture2DDistribution( sampler2D shadow, vec2 uv ) {
		return unpackRGBATo2Half( texture2D( shadow, uv ) );
	}
	float VSMShadow (sampler2D shadow, vec2 uv, float compare ){
		float occlusion = 1.0;
		vec2 distribution = texture2DDistribution( shadow, uv );
		float hard_shadow = step( compare , distribution.x );
		if (hard_shadow != 1.0 ) {
			float distance = compare - distribution.x ;
			float variance = max( 0.00000, distribution.y * distribution.y );
			float softness_probability = variance / (variance + distance * distance );			softness_probability = clamp( ( softness_probability - 0.3 ) / ( 0.95 - 0.3 ), 0.0, 1.0 );			occlusion = clamp( max( hard_shadow, softness_probability ), 0.0, 1.0 );
		}
		return occlusion;
	}
	float getShadow( sampler2D shadowMap, vec2 shadowMapSize, float shadowIntensity, float shadowBias, float shadowRadius, vec4 shadowCoord ) {
		float shadow = 1.0;
		shadowCoord.xyz /= shadowCoord.w;
		shadowCoord.z += shadowBias;
		bool inFrustum = shadowCoord.x >= 0.0 && shadowCoord.x <= 1.0 && shadowCoord.y >= 0.0 && shadowCoord.y <= 1.0;
		bool frustumTest = inFrustum && shadowCoord.z <= 1.0;
		if ( frustumTest ) {
		#if defined( SHADOWMAP_TYPE_PCF )
			vec2 texelSize = vec2( 1.0 ) / shadowMapSize;
			float dx0 = - texelSize.x * shadowRadius;
			float dy0 = - texelSize.y * shadowRadius;
			float dx1 = + texelSize.x * shadowRadius;
			float dy1 = + texelSize.y * shadowRadius;
			float dx2 = dx0 / 2.0;
			float dy2 = dy0 / 2.0;
			float dx3 = dx1 / 2.0;
			float dy3 = dy1 / 2.0;
			shadow = (
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( dx0, dy0 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( 0.0, dy0 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( dx1, dy0 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( dx2, dy2 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( 0.0, dy2 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( dx3, dy2 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( dx0, 0.0 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( dx2, 0.0 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy, shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( dx3, 0.0 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( dx1, 0.0 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( dx2, dy3 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( 0.0, dy3 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( dx3, dy3 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( dx0, dy1 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( 0.0, dy1 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( dx1, dy1 ), shadowCoord.z )
			) * ( 1.0 / 17.0 );
		#elif defined( SHADOWMAP_TYPE_PCF_SOFT )
			vec2 texelSize = vec2( 1.0 ) / shadowMapSize;
			float dx = texelSize.x;
			float dy = texelSize.y;
			vec2 uv = shadowCoord.xy;
			vec2 f = fract( uv * shadowMapSize + 0.5 );
			uv -= f * texelSize;
			shadow = (
				texture2DCompare( shadowMap, uv, shadowCoord.z ) +
				texture2DCompare( shadowMap, uv + vec2( dx, 0.0 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, uv + vec2( 0.0, dy ), shadowCoord.z ) +
				texture2DCompare( shadowMap, uv + texelSize, shadowCoord.z ) +
				mix( texture2DCompare( shadowMap, uv + vec2( -dx, 0.0 ), shadowCoord.z ),
					 texture2DCompare( shadowMap, uv + vec2( 2.0 * dx, 0.0 ), shadowCoord.z ),
					 f.x ) +
				mix( texture2DCompare( shadowMap, uv + vec2( -dx, dy ), shadowCoord.z ),
					 texture2DCompare( shadowMap, uv + vec2( 2.0 * dx, dy ), shadowCoord.z ),
					 f.x ) +
				mix( texture2DCompare( shadowMap, uv + vec2( 0.0, -dy ), shadowCoord.z ),
					 texture2DCompare( shadowMap, uv + vec2( 0.0, 2.0 * dy ), shadowCoord.z ),
					 f.y ) +
				mix( texture2DCompare( shadowMap, uv + vec2( dx, -dy ), shadowCoord.z ),
					 texture2DCompare( shadowMap, uv + vec2( dx, 2.0 * dy ), shadowCoord.z ),
					 f.y ) +
				mix( mix( texture2DCompare( shadowMap, uv + vec2( -dx, -dy ), shadowCoord.z ),
						  texture2DCompare( shadowMap, uv + vec2( 2.0 * dx, -dy ), shadowCoord.z ),
						  f.x ),
					 mix( texture2DCompare( shadowMap, uv + vec2( -dx, 2.0 * dy ), shadowCoord.z ),
						  texture2DCompare( shadowMap, uv + vec2( 2.0 * dx, 2.0 * dy ), shadowCoord.z ),
						  f.x ),
					 f.y )
			) * ( 1.0 / 9.0 );
		#elif defined( SHADOWMAP_TYPE_VSM )
			shadow = VSMShadow( shadowMap, shadowCoord.xy, shadowCoord.z );
		#else
			shadow = texture2DCompare( shadowMap, shadowCoord.xy, shadowCoord.z );
		#endif
		}
		return mix( 1.0, shadow, shadowIntensity );
	}
	vec2 cubeToUV( vec3 v, float texelSizeY ) {
		vec3 absV = abs( v );
		float scaleToCube = 1.0 / max( absV.x, max( absV.y, absV.z ) );
		absV *= scaleToCube;
		v *= scaleToCube * ( 1.0 - 2.0 * texelSizeY );
		vec2 planar = v.xy;
		float almostATexel = 1.5 * texelSizeY;
		float almostOne = 1.0 - almostATexel;
		if ( absV.z >= almostOne ) {
			if ( v.z > 0.0 )
				planar.x = 4.0 - v.x;
		} else if ( absV.x >= almostOne ) {
			float signX = sign( v.x );
			planar.x = v.z * signX + 2.0 * signX;
		} else if ( absV.y >= almostOne ) {
			float signY = sign( v.y );
			planar.x = v.x + 2.0 * signY + 2.0;
			planar.y = v.z * signY - 2.0;
		}
		return vec2( 0.125, 0.25 ) * planar + vec2( 0.375, 0.75 );
	}
	float getPointShadow( sampler2D shadowMap, vec2 shadowMapSize, float shadowIntensity, float shadowBias, float shadowRadius, vec4 shadowCoord, float shadowCameraNear, float shadowCameraFar ) {
		float shadow = 1.0;
		vec3 lightToPosition = shadowCoord.xyz;
		
		float lightToPositionLength = length( lightToPosition );
		if ( lightToPositionLength - shadowCameraFar <= 0.0 && lightToPositionLength - shadowCameraNear >= 0.0 ) {
			float dp = ( lightToPositionLength - shadowCameraNear ) / ( shadowCameraFar - shadowCameraNear );			dp += shadowBias;
			vec3 bd3D = normalize( lightToPosition );
			vec2 texelSize = vec2( 1.0 ) / ( shadowMapSize * vec2( 4.0, 2.0 ) );
			#if defined( SHADOWMAP_TYPE_PCF ) || defined( SHADOWMAP_TYPE_PCF_SOFT ) || defined( SHADOWMAP_TYPE_VSM )
				vec2 offset = vec2( - 1, 1 ) * shadowRadius * texelSize.y;
				shadow = (
					texture2DCompare( shadowMap, cubeToUV( bd3D + offset.xyy, texelSize.y ), dp ) +
					texture2DCompare( shadowMap, cubeToUV( bd3D + offset.yyy, texelSize.y ), dp ) +
					texture2DCompare( shadowMap, cubeToUV( bd3D + offset.xyx, texelSize.y ), dp ) +
					texture2DCompare( shadowMap, cubeToUV( bd3D + offset.yyx, texelSize.y ), dp ) +
					texture2DCompare( shadowMap, cubeToUV( bd3D, texelSize.y ), dp ) +
					texture2DCompare( shadowMap, cubeToUV( bd3D + offset.xxy, texelSize.y ), dp ) +
					texture2DCompare( shadowMap, cubeToUV( bd3D + offset.yxy, texelSize.y ), dp ) +
					texture2DCompare( shadowMap, cubeToUV( bd3D + offset.xxx, texelSize.y ), dp ) +
					texture2DCompare( shadowMap, cubeToUV( bd3D + offset.yxx, texelSize.y ), dp )
				) * ( 1.0 / 9.0 );
			#else
				shadow = texture2DCompare( shadowMap, cubeToUV( bd3D, texelSize.y ), dp );
			#endif
		}
		return mix( 1.0, shadow, shadowIntensity );
	}
#endif`,bh=`#if NUM_SPOT_LIGHT_COORDS > 0
	uniform mat4 spotLightMatrix[ NUM_SPOT_LIGHT_COORDS ];
	varying vec4 vSpotLightCoord[ NUM_SPOT_LIGHT_COORDS ];
#endif
#ifdef USE_SHADOWMAP
	#if NUM_DIR_LIGHT_SHADOWS > 0
		uniform mat4 directionalShadowMatrix[ NUM_DIR_LIGHT_SHADOWS ];
		varying vec4 vDirectionalShadowCoord[ NUM_DIR_LIGHT_SHADOWS ];
		struct DirectionalLightShadow {
			float shadowIntensity;
			float shadowBias;
			float shadowNormalBias;
			float shadowRadius;
			vec2 shadowMapSize;
		};
		uniform DirectionalLightShadow directionalLightShadows[ NUM_DIR_LIGHT_SHADOWS ];
	#endif
	#if NUM_SPOT_LIGHT_SHADOWS > 0
		struct SpotLightShadow {
			float shadowIntensity;
			float shadowBias;
			float shadowNormalBias;
			float shadowRadius;
			vec2 shadowMapSize;
		};
		uniform SpotLightShadow spotLightShadows[ NUM_SPOT_LIGHT_SHADOWS ];
	#endif
	#if NUM_POINT_LIGHT_SHADOWS > 0
		uniform mat4 pointShadowMatrix[ NUM_POINT_LIGHT_SHADOWS ];
		varying vec4 vPointShadowCoord[ NUM_POINT_LIGHT_SHADOWS ];
		struct PointLightShadow {
			float shadowIntensity;
			float shadowBias;
			float shadowNormalBias;
			float shadowRadius;
			vec2 shadowMapSize;
			float shadowCameraNear;
			float shadowCameraFar;
		};
		uniform PointLightShadow pointLightShadows[ NUM_POINT_LIGHT_SHADOWS ];
	#endif
#endif`,yh=`#if ( defined( USE_SHADOWMAP ) && ( NUM_DIR_LIGHT_SHADOWS > 0 || NUM_POINT_LIGHT_SHADOWS > 0 ) ) || ( NUM_SPOT_LIGHT_COORDS > 0 )
	vec3 shadowWorldNormal = inverseTransformDirection( transformedNormal, viewMatrix );
	vec4 shadowWorldPosition;
#endif
#if defined( USE_SHADOWMAP )
	#if NUM_DIR_LIGHT_SHADOWS > 0
		#pragma unroll_loop_start
		for ( int i = 0; i < NUM_DIR_LIGHT_SHADOWS; i ++ ) {
			shadowWorldPosition = worldPosition + vec4( shadowWorldNormal * directionalLightShadows[ i ].shadowNormalBias, 0 );
			vDirectionalShadowCoord[ i ] = directionalShadowMatrix[ i ] * shadowWorldPosition;
		}
		#pragma unroll_loop_end
	#endif
	#if NUM_POINT_LIGHT_SHADOWS > 0
		#pragma unroll_loop_start
		for ( int i = 0; i < NUM_POINT_LIGHT_SHADOWS; i ++ ) {
			shadowWorldPosition = worldPosition + vec4( shadowWorldNormal * pointLightShadows[ i ].shadowNormalBias, 0 );
			vPointShadowCoord[ i ] = pointShadowMatrix[ i ] * shadowWorldPosition;
		}
		#pragma unroll_loop_end
	#endif
#endif
#if NUM_SPOT_LIGHT_COORDS > 0
	#pragma unroll_loop_start
	for ( int i = 0; i < NUM_SPOT_LIGHT_COORDS; i ++ ) {
		shadowWorldPosition = worldPosition;
		#if ( defined( USE_SHADOWMAP ) && UNROLLED_LOOP_INDEX < NUM_SPOT_LIGHT_SHADOWS )
			shadowWorldPosition.xyz += shadowWorldNormal * spotLightShadows[ i ].shadowNormalBias;
		#endif
		vSpotLightCoord[ i ] = spotLightMatrix[ i ] * shadowWorldPosition;
	}
	#pragma unroll_loop_end
#endif`,Th=`float getShadowMask() {
	float shadow = 1.0;
	#ifdef USE_SHADOWMAP
	#if NUM_DIR_LIGHT_SHADOWS > 0
	DirectionalLightShadow directionalLight;
	#pragma unroll_loop_start
	for ( int i = 0; i < NUM_DIR_LIGHT_SHADOWS; i ++ ) {
		directionalLight = directionalLightShadows[ i ];
		shadow *= receiveShadow ? getShadow( directionalShadowMap[ i ], directionalLight.shadowMapSize, directionalLight.shadowIntensity, directionalLight.shadowBias, directionalLight.shadowRadius, vDirectionalShadowCoord[ i ] ) : 1.0;
	}
	#pragma unroll_loop_end
	#endif
	#if NUM_SPOT_LIGHT_SHADOWS > 0
	SpotLightShadow spotLight;
	#pragma unroll_loop_start
	for ( int i = 0; i < NUM_SPOT_LIGHT_SHADOWS; i ++ ) {
		spotLight = spotLightShadows[ i ];
		shadow *= receiveShadow ? getShadow( spotShadowMap[ i ], spotLight.shadowMapSize, spotLight.shadowIntensity, spotLight.shadowBias, spotLight.shadowRadius, vSpotLightCoord[ i ] ) : 1.0;
	}
	#pragma unroll_loop_end
	#endif
	#if NUM_POINT_LIGHT_SHADOWS > 0
	PointLightShadow pointLight;
	#pragma unroll_loop_start
	for ( int i = 0; i < NUM_POINT_LIGHT_SHADOWS; i ++ ) {
		pointLight = pointLightShadows[ i ];
		shadow *= receiveShadow ? getPointShadow( pointShadowMap[ i ], pointLight.shadowMapSize, pointLight.shadowIntensity, pointLight.shadowBias, pointLight.shadowRadius, vPointShadowCoord[ i ], pointLight.shadowCameraNear, pointLight.shadowCameraFar ) : 1.0;
	}
	#pragma unroll_loop_end
	#endif
	#endif
	return shadow;
}`,wh=`#ifdef USE_SKINNING
	mat4 boneMatX = getBoneMatrix( skinIndex.x );
	mat4 boneMatY = getBoneMatrix( skinIndex.y );
	mat4 boneMatZ = getBoneMatrix( skinIndex.z );
	mat4 boneMatW = getBoneMatrix( skinIndex.w );
#endif`,Ah=`#ifdef USE_SKINNING
	uniform mat4 bindMatrix;
	uniform mat4 bindMatrixInverse;
	uniform highp sampler2D boneTexture;
	mat4 getBoneMatrix( const in float i ) {
		int size = textureSize( boneTexture, 0 ).x;
		int j = int( i ) * 4;
		int x = j % size;
		int y = j / size;
		vec4 v1 = texelFetch( boneTexture, ivec2( x, y ), 0 );
		vec4 v2 = texelFetch( boneTexture, ivec2( x + 1, y ), 0 );
		vec4 v3 = texelFetch( boneTexture, ivec2( x + 2, y ), 0 );
		vec4 v4 = texelFetch( boneTexture, ivec2( x + 3, y ), 0 );
		return mat4( v1, v2, v3, v4 );
	}
#endif`,Rh=`#ifdef USE_SKINNING
	vec4 skinVertex = bindMatrix * vec4( transformed, 1.0 );
	vec4 skinned = vec4( 0.0 );
	skinned += boneMatX * skinVertex * skinWeight.x;
	skinned += boneMatY * skinVertex * skinWeight.y;
	skinned += boneMatZ * skinVertex * skinWeight.z;
	skinned += boneMatW * skinVertex * skinWeight.w;
	transformed = ( bindMatrixInverse * skinned ).xyz;
#endif`,Ch=`#ifdef USE_SKINNING
	mat4 skinMatrix = mat4( 0.0 );
	skinMatrix += skinWeight.x * boneMatX;
	skinMatrix += skinWeight.y * boneMatY;
	skinMatrix += skinWeight.z * boneMatZ;
	skinMatrix += skinWeight.w * boneMatW;
	skinMatrix = bindMatrixInverse * skinMatrix * bindMatrix;
	objectNormal = vec4( skinMatrix * vec4( objectNormal, 0.0 ) ).xyz;
	#ifdef USE_TANGENT
		objectTangent = vec4( skinMatrix * vec4( objectTangent, 0.0 ) ).xyz;
	#endif
#endif`,Ph=`float specularStrength;
#ifdef USE_SPECULARMAP
	vec4 texelSpecular = texture2D( specularMap, vSpecularMapUv );
	specularStrength = texelSpecular.r;
#else
	specularStrength = 1.0;
#endif`,Dh=`#ifdef USE_SPECULARMAP
	uniform sampler2D specularMap;
#endif`,Lh=`#if defined( TONE_MAPPING )
	gl_FragColor.rgb = toneMapping( gl_FragColor.rgb );
#endif`,Ih=`#ifndef saturate
#define saturate( a ) clamp( a, 0.0, 1.0 )
#endif
uniform float toneMappingExposure;
vec3 LinearToneMapping( vec3 color ) {
	return saturate( toneMappingExposure * color );
}
vec3 ReinhardToneMapping( vec3 color ) {
	color *= toneMappingExposure;
	return saturate( color / ( vec3( 1.0 ) + color ) );
}
vec3 CineonToneMapping( vec3 color ) {
	color *= toneMappingExposure;
	color = max( vec3( 0.0 ), color - 0.004 );
	return pow( ( color * ( 6.2 * color + 0.5 ) ) / ( color * ( 6.2 * color + 1.7 ) + 0.06 ), vec3( 2.2 ) );
}
vec3 RRTAndODTFit( vec3 v ) {
	vec3 a = v * ( v + 0.0245786 ) - 0.000090537;
	vec3 b = v * ( 0.983729 * v + 0.4329510 ) + 0.238081;
	return a / b;
}
vec3 ACESFilmicToneMapping( vec3 color ) {
	const mat3 ACESInputMat = mat3(
		vec3( 0.59719, 0.07600, 0.02840 ),		vec3( 0.35458, 0.90834, 0.13383 ),
		vec3( 0.04823, 0.01566, 0.83777 )
	);
	const mat3 ACESOutputMat = mat3(
		vec3(  1.60475, -0.10208, -0.00327 ),		vec3( -0.53108,  1.10813, -0.07276 ),
		vec3( -0.07367, -0.00605,  1.07602 )
	);
	color *= toneMappingExposure / 0.6;
	color = ACESInputMat * color;
	color = RRTAndODTFit( color );
	color = ACESOutputMat * color;
	return saturate( color );
}
const mat3 LINEAR_REC2020_TO_LINEAR_SRGB = mat3(
	vec3( 1.6605, - 0.1246, - 0.0182 ),
	vec3( - 0.5876, 1.1329, - 0.1006 ),
	vec3( - 0.0728, - 0.0083, 1.1187 )
);
const mat3 LINEAR_SRGB_TO_LINEAR_REC2020 = mat3(
	vec3( 0.6274, 0.0691, 0.0164 ),
	vec3( 0.3293, 0.9195, 0.0880 ),
	vec3( 0.0433, 0.0113, 0.8956 )
);
vec3 agxDefaultContrastApprox( vec3 x ) {
	vec3 x2 = x * x;
	vec3 x4 = x2 * x2;
	return + 15.5 * x4 * x2
		- 40.14 * x4 * x
		+ 31.96 * x4
		- 6.868 * x2 * x
		+ 0.4298 * x2
		+ 0.1191 * x
		- 0.00232;
}
vec3 AgXToneMapping( vec3 color ) {
	const mat3 AgXInsetMatrix = mat3(
		vec3( 0.856627153315983, 0.137318972929847, 0.11189821299995 ),
		vec3( 0.0951212405381588, 0.761241990602591, 0.0767994186031903 ),
		vec3( 0.0482516061458583, 0.101439036467562, 0.811302368396859 )
	);
	const mat3 AgXOutsetMatrix = mat3(
		vec3( 1.1271005818144368, - 0.1413297634984383, - 0.14132976349843826 ),
		vec3( - 0.11060664309660323, 1.157823702216272, - 0.11060664309660294 ),
		vec3( - 0.016493938717834573, - 0.016493938717834257, 1.2519364065950405 )
	);
	const float AgxMinEv = - 12.47393;	const float AgxMaxEv = 4.026069;
	color *= toneMappingExposure;
	color = LINEAR_SRGB_TO_LINEAR_REC2020 * color;
	color = AgXInsetMatrix * color;
	color = max( color, 1e-10 );	color = log2( color );
	color = ( color - AgxMinEv ) / ( AgxMaxEv - AgxMinEv );
	color = clamp( color, 0.0, 1.0 );
	color = agxDefaultContrastApprox( color );
	color = AgXOutsetMatrix * color;
	color = pow( max( vec3( 0.0 ), color ), vec3( 2.2 ) );
	color = LINEAR_REC2020_TO_LINEAR_SRGB * color;
	color = clamp( color, 0.0, 1.0 );
	return color;
}
vec3 NeutralToneMapping( vec3 color ) {
	const float StartCompression = 0.8 - 0.04;
	const float Desaturation = 0.15;
	color *= toneMappingExposure;
	float x = min( color.r, min( color.g, color.b ) );
	float offset = x < 0.08 ? x - 6.25 * x * x : 0.04;
	color -= offset;
	float peak = max( color.r, max( color.g, color.b ) );
	if ( peak < StartCompression ) return color;
	float d = 1. - StartCompression;
	float newPeak = 1. - d * d / ( peak + d - StartCompression );
	color *= newPeak / peak;
	float g = 1. - 1. / ( Desaturation * ( peak - newPeak ) + 1. );
	return mix( color, vec3( newPeak ), g );
}
vec3 CustomToneMapping( vec3 color ) { return color; }`,Uh=`#ifdef USE_TRANSMISSION
	material.transmission = transmission;
	material.transmissionAlpha = 1.0;
	material.thickness = thickness;
	material.attenuationDistance = attenuationDistance;
	material.attenuationColor = attenuationColor;
	#ifdef USE_TRANSMISSIONMAP
		material.transmission *= texture2D( transmissionMap, vTransmissionMapUv ).r;
	#endif
	#ifdef USE_THICKNESSMAP
		material.thickness *= texture2D( thicknessMap, vThicknessMapUv ).g;
	#endif
	vec3 pos = vWorldPosition;
	vec3 v = normalize( cameraPosition - pos );
	vec3 n = inverseTransformDirection( normal, viewMatrix );
	vec4 transmitted = getIBLVolumeRefraction(
		n, v, material.roughness, material.diffuseColor, material.specularColor, material.specularF90,
		pos, modelMatrix, viewMatrix, projectionMatrix, material.dispersion, material.ior, material.thickness,
		material.attenuationColor, material.attenuationDistance );
	material.transmissionAlpha = mix( material.transmissionAlpha, transmitted.a, material.transmission );
	totalDiffuse = mix( totalDiffuse, transmitted.rgb, material.transmission );
#endif`,zh=`#ifdef USE_TRANSMISSION
	uniform float transmission;
	uniform float thickness;
	uniform float attenuationDistance;
	uniform vec3 attenuationColor;
	#ifdef USE_TRANSMISSIONMAP
		uniform sampler2D transmissionMap;
	#endif
	#ifdef USE_THICKNESSMAP
		uniform sampler2D thicknessMap;
	#endif
	uniform vec2 transmissionSamplerSize;
	uniform sampler2D transmissionSamplerMap;
	uniform mat4 modelMatrix;
	uniform mat4 projectionMatrix;
	varying vec3 vWorldPosition;
	float w0( float a ) {
		return ( 1.0 / 6.0 ) * ( a * ( a * ( - a + 3.0 ) - 3.0 ) + 1.0 );
	}
	float w1( float a ) {
		return ( 1.0 / 6.0 ) * ( a *  a * ( 3.0 * a - 6.0 ) + 4.0 );
	}
	float w2( float a ){
		return ( 1.0 / 6.0 ) * ( a * ( a * ( - 3.0 * a + 3.0 ) + 3.0 ) + 1.0 );
	}
	float w3( float a ) {
		return ( 1.0 / 6.0 ) * ( a * a * a );
	}
	float g0( float a ) {
		return w0( a ) + w1( a );
	}
	float g1( float a ) {
		return w2( a ) + w3( a );
	}
	float h0( float a ) {
		return - 1.0 + w1( a ) / ( w0( a ) + w1( a ) );
	}
	float h1( float a ) {
		return 1.0 + w3( a ) / ( w2( a ) + w3( a ) );
	}
	vec4 bicubic( sampler2D tex, vec2 uv, vec4 texelSize, float lod ) {
		uv = uv * texelSize.zw + 0.5;
		vec2 iuv = floor( uv );
		vec2 fuv = fract( uv );
		float g0x = g0( fuv.x );
		float g1x = g1( fuv.x );
		float h0x = h0( fuv.x );
		float h1x = h1( fuv.x );
		float h0y = h0( fuv.y );
		float h1y = h1( fuv.y );
		vec2 p0 = ( vec2( iuv.x + h0x, iuv.y + h0y ) - 0.5 ) * texelSize.xy;
		vec2 p1 = ( vec2( iuv.x + h1x, iuv.y + h0y ) - 0.5 ) * texelSize.xy;
		vec2 p2 = ( vec2( iuv.x + h0x, iuv.y + h1y ) - 0.5 ) * texelSize.xy;
		vec2 p3 = ( vec2( iuv.x + h1x, iuv.y + h1y ) - 0.5 ) * texelSize.xy;
		return g0( fuv.y ) * ( g0x * textureLod( tex, p0, lod ) + g1x * textureLod( tex, p1, lod ) ) +
			g1( fuv.y ) * ( g0x * textureLod( tex, p2, lod ) + g1x * textureLod( tex, p3, lod ) );
	}
	vec4 textureBicubic( sampler2D sampler, vec2 uv, float lod ) {
		vec2 fLodSize = vec2( textureSize( sampler, int( lod ) ) );
		vec2 cLodSize = vec2( textureSize( sampler, int( lod + 1.0 ) ) );
		vec2 fLodSizeInv = 1.0 / fLodSize;
		vec2 cLodSizeInv = 1.0 / cLodSize;
		vec4 fSample = bicubic( sampler, uv, vec4( fLodSizeInv, fLodSize ), floor( lod ) );
		vec4 cSample = bicubic( sampler, uv, vec4( cLodSizeInv, cLodSize ), ceil( lod ) );
		return mix( fSample, cSample, fract( lod ) );
	}
	vec3 getVolumeTransmissionRay( const in vec3 n, const in vec3 v, const in float thickness, const in float ior, const in mat4 modelMatrix ) {
		vec3 refractionVector = refract( - v, normalize( n ), 1.0 / ior );
		vec3 modelScale;
		modelScale.x = length( vec3( modelMatrix[ 0 ].xyz ) );
		modelScale.y = length( vec3( modelMatrix[ 1 ].xyz ) );
		modelScale.z = length( vec3( modelMatrix[ 2 ].xyz ) );
		return normalize( refractionVector ) * thickness * modelScale;
	}
	float applyIorToRoughness( const in float roughness, const in float ior ) {
		return roughness * clamp( ior * 2.0 - 2.0, 0.0, 1.0 );
	}
	vec4 getTransmissionSample( const in vec2 fragCoord, const in float roughness, const in float ior ) {
		float lod = log2( transmissionSamplerSize.x ) * applyIorToRoughness( roughness, ior );
		return textureBicubic( transmissionSamplerMap, fragCoord.xy, lod );
	}
	vec3 volumeAttenuation( const in float transmissionDistance, const in vec3 attenuationColor, const in float attenuationDistance ) {
		if ( isinf( attenuationDistance ) ) {
			return vec3( 1.0 );
		} else {
			vec3 attenuationCoefficient = -log( attenuationColor ) / attenuationDistance;
			vec3 transmittance = exp( - attenuationCoefficient * transmissionDistance );			return transmittance;
		}
	}
	vec4 getIBLVolumeRefraction( const in vec3 n, const in vec3 v, const in float roughness, const in vec3 diffuseColor,
		const in vec3 specularColor, const in float specularF90, const in vec3 position, const in mat4 modelMatrix,
		const in mat4 viewMatrix, const in mat4 projMatrix, const in float dispersion, const in float ior, const in float thickness,
		const in vec3 attenuationColor, const in float attenuationDistance ) {
		vec4 transmittedLight;
		vec3 transmittance;
		#ifdef USE_DISPERSION
			float halfSpread = ( ior - 1.0 ) * 0.025 * dispersion;
			vec3 iors = vec3( ior - halfSpread, ior, ior + halfSpread );
			for ( int i = 0; i < 3; i ++ ) {
				vec3 transmissionRay = getVolumeTransmissionRay( n, v, thickness, iors[ i ], modelMatrix );
				vec3 refractedRayExit = position + transmissionRay;
				vec4 ndcPos = projMatrix * viewMatrix * vec4( refractedRayExit, 1.0 );
				vec2 refractionCoords = ndcPos.xy / ndcPos.w;
				refractionCoords += 1.0;
				refractionCoords /= 2.0;
				vec4 transmissionSample = getTransmissionSample( refractionCoords, roughness, iors[ i ] );
				transmittedLight[ i ] = transmissionSample[ i ];
				transmittedLight.a += transmissionSample.a;
				transmittance[ i ] = diffuseColor[ i ] * volumeAttenuation( length( transmissionRay ), attenuationColor, attenuationDistance )[ i ];
			}
			transmittedLight.a /= 3.0;
		#else
			vec3 transmissionRay = getVolumeTransmissionRay( n, v, thickness, ior, modelMatrix );
			vec3 refractedRayExit = position + transmissionRay;
			vec4 ndcPos = projMatrix * viewMatrix * vec4( refractedRayExit, 1.0 );
			vec2 refractionCoords = ndcPos.xy / ndcPos.w;
			refractionCoords += 1.0;
			refractionCoords /= 2.0;
			transmittedLight = getTransmissionSample( refractionCoords, roughness, ior );
			transmittance = diffuseColor * volumeAttenuation( length( transmissionRay ), attenuationColor, attenuationDistance );
		#endif
		vec3 attenuatedColor = transmittance * transmittedLight.rgb;
		vec3 F = EnvironmentBRDF( n, v, specularColor, specularF90, roughness );
		float transmittanceFactor = ( transmittance.r + transmittance.g + transmittance.b ) / 3.0;
		return vec4( ( 1.0 - F ) * attenuatedColor, 1.0 - ( 1.0 - transmittedLight.a ) * transmittanceFactor );
	}
#endif`,Nh=`#if defined( USE_UV ) || defined( USE_ANISOTROPY )
	varying vec2 vUv;
#endif
#ifdef USE_MAP
	varying vec2 vMapUv;
#endif
#ifdef USE_ALPHAMAP
	varying vec2 vAlphaMapUv;
#endif
#ifdef USE_LIGHTMAP
	varying vec2 vLightMapUv;
#endif
#ifdef USE_AOMAP
	varying vec2 vAoMapUv;
#endif
#ifdef USE_BUMPMAP
	varying vec2 vBumpMapUv;
#endif
#ifdef USE_NORMALMAP
	varying vec2 vNormalMapUv;
#endif
#ifdef USE_EMISSIVEMAP
	varying vec2 vEmissiveMapUv;
#endif
#ifdef USE_METALNESSMAP
	varying vec2 vMetalnessMapUv;
#endif
#ifdef USE_ROUGHNESSMAP
	varying vec2 vRoughnessMapUv;
#endif
#ifdef USE_ANISOTROPYMAP
	varying vec2 vAnisotropyMapUv;
#endif
#ifdef USE_CLEARCOATMAP
	varying vec2 vClearcoatMapUv;
#endif
#ifdef USE_CLEARCOAT_NORMALMAP
	varying vec2 vClearcoatNormalMapUv;
#endif
#ifdef USE_CLEARCOAT_ROUGHNESSMAP
	varying vec2 vClearcoatRoughnessMapUv;
#endif
#ifdef USE_IRIDESCENCEMAP
	varying vec2 vIridescenceMapUv;
#endif
#ifdef USE_IRIDESCENCE_THICKNESSMAP
	varying vec2 vIridescenceThicknessMapUv;
#endif
#ifdef USE_SHEEN_COLORMAP
	varying vec2 vSheenColorMapUv;
#endif
#ifdef USE_SHEEN_ROUGHNESSMAP
	varying vec2 vSheenRoughnessMapUv;
#endif
#ifdef USE_SPECULARMAP
	varying vec2 vSpecularMapUv;
#endif
#ifdef USE_SPECULAR_COLORMAP
	varying vec2 vSpecularColorMapUv;
#endif
#ifdef USE_SPECULAR_INTENSITYMAP
	varying vec2 vSpecularIntensityMapUv;
#endif
#ifdef USE_TRANSMISSIONMAP
	uniform mat3 transmissionMapTransform;
	varying vec2 vTransmissionMapUv;
#endif
#ifdef USE_THICKNESSMAP
	uniform mat3 thicknessMapTransform;
	varying vec2 vThicknessMapUv;
#endif`,kh=`#if defined( USE_UV ) || defined( USE_ANISOTROPY )
	varying vec2 vUv;
#endif
#ifdef USE_MAP
	uniform mat3 mapTransform;
	varying vec2 vMapUv;
#endif
#ifdef USE_ALPHAMAP
	uniform mat3 alphaMapTransform;
	varying vec2 vAlphaMapUv;
#endif
#ifdef USE_LIGHTMAP
	uniform mat3 lightMapTransform;
	varying vec2 vLightMapUv;
#endif
#ifdef USE_AOMAP
	uniform mat3 aoMapTransform;
	varying vec2 vAoMapUv;
#endif
#ifdef USE_BUMPMAP
	uniform mat3 bumpMapTransform;
	varying vec2 vBumpMapUv;
#endif
#ifdef USE_NORMALMAP
	uniform mat3 normalMapTransform;
	varying vec2 vNormalMapUv;
#endif
#ifdef USE_DISPLACEMENTMAP
	uniform mat3 displacementMapTransform;
	varying vec2 vDisplacementMapUv;
#endif
#ifdef USE_EMISSIVEMAP
	uniform mat3 emissiveMapTransform;
	varying vec2 vEmissiveMapUv;
#endif
#ifdef USE_METALNESSMAP
	uniform mat3 metalnessMapTransform;
	varying vec2 vMetalnessMapUv;
#endif
#ifdef USE_ROUGHNESSMAP
	uniform mat3 roughnessMapTransform;
	varying vec2 vRoughnessMapUv;
#endif
#ifdef USE_ANISOTROPYMAP
	uniform mat3 anisotropyMapTransform;
	varying vec2 vAnisotropyMapUv;
#endif
#ifdef USE_CLEARCOATMAP
	uniform mat3 clearcoatMapTransform;
	varying vec2 vClearcoatMapUv;
#endif
#ifdef USE_CLEARCOAT_NORMALMAP
	uniform mat3 clearcoatNormalMapTransform;
	varying vec2 vClearcoatNormalMapUv;
#endif
#ifdef USE_CLEARCOAT_ROUGHNESSMAP
	uniform mat3 clearcoatRoughnessMapTransform;
	varying vec2 vClearcoatRoughnessMapUv;
#endif
#ifdef USE_SHEEN_COLORMAP
	uniform mat3 sheenColorMapTransform;
	varying vec2 vSheenColorMapUv;
#endif
#ifdef USE_SHEEN_ROUGHNESSMAP
	uniform mat3 sheenRoughnessMapTransform;
	varying vec2 vSheenRoughnessMapUv;
#endif
#ifdef USE_IRIDESCENCEMAP
	uniform mat3 iridescenceMapTransform;
	varying vec2 vIridescenceMapUv;
#endif
#ifdef USE_IRIDESCENCE_THICKNESSMAP
	uniform mat3 iridescenceThicknessMapTransform;
	varying vec2 vIridescenceThicknessMapUv;
#endif
#ifdef USE_SPECULARMAP
	uniform mat3 specularMapTransform;
	varying vec2 vSpecularMapUv;
#endif
#ifdef USE_SPECULAR_COLORMAP
	uniform mat3 specularColorMapTransform;
	varying vec2 vSpecularColorMapUv;
#endif
#ifdef USE_SPECULAR_INTENSITYMAP
	uniform mat3 specularIntensityMapTransform;
	varying vec2 vSpecularIntensityMapUv;
#endif
#ifdef USE_TRANSMISSIONMAP
	uniform mat3 transmissionMapTransform;
	varying vec2 vTransmissionMapUv;
#endif
#ifdef USE_THICKNESSMAP
	uniform mat3 thicknessMapTransform;
	varying vec2 vThicknessMapUv;
#endif`,Fh=`#if defined( USE_UV ) || defined( USE_ANISOTROPY )
	vUv = vec3( uv, 1 ).xy;
#endif
#ifdef USE_MAP
	vMapUv = ( mapTransform * vec3( MAP_UV, 1 ) ).xy;
#endif
#ifdef USE_ALPHAMAP
	vAlphaMapUv = ( alphaMapTransform * vec3( ALPHAMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_LIGHTMAP
	vLightMapUv = ( lightMapTransform * vec3( LIGHTMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_AOMAP
	vAoMapUv = ( aoMapTransform * vec3( AOMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_BUMPMAP
	vBumpMapUv = ( bumpMapTransform * vec3( BUMPMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_NORMALMAP
	vNormalMapUv = ( normalMapTransform * vec3( NORMALMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_DISPLACEMENTMAP
	vDisplacementMapUv = ( displacementMapTransform * vec3( DISPLACEMENTMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_EMISSIVEMAP
	vEmissiveMapUv = ( emissiveMapTransform * vec3( EMISSIVEMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_METALNESSMAP
	vMetalnessMapUv = ( metalnessMapTransform * vec3( METALNESSMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_ROUGHNESSMAP
	vRoughnessMapUv = ( roughnessMapTransform * vec3( ROUGHNESSMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_ANISOTROPYMAP
	vAnisotropyMapUv = ( anisotropyMapTransform * vec3( ANISOTROPYMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_CLEARCOATMAP
	vClearcoatMapUv = ( clearcoatMapTransform * vec3( CLEARCOATMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_CLEARCOAT_NORMALMAP
	vClearcoatNormalMapUv = ( clearcoatNormalMapTransform * vec3( CLEARCOAT_NORMALMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_CLEARCOAT_ROUGHNESSMAP
	vClearcoatRoughnessMapUv = ( clearcoatRoughnessMapTransform * vec3( CLEARCOAT_ROUGHNESSMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_IRIDESCENCEMAP
	vIridescenceMapUv = ( iridescenceMapTransform * vec3( IRIDESCENCEMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_IRIDESCENCE_THICKNESSMAP
	vIridescenceThicknessMapUv = ( iridescenceThicknessMapTransform * vec3( IRIDESCENCE_THICKNESSMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_SHEEN_COLORMAP
	vSheenColorMapUv = ( sheenColorMapTransform * vec3( SHEEN_COLORMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_SHEEN_ROUGHNESSMAP
	vSheenRoughnessMapUv = ( sheenRoughnessMapTransform * vec3( SHEEN_ROUGHNESSMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_SPECULARMAP
	vSpecularMapUv = ( specularMapTransform * vec3( SPECULARMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_SPECULAR_COLORMAP
	vSpecularColorMapUv = ( specularColorMapTransform * vec3( SPECULAR_COLORMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_SPECULAR_INTENSITYMAP
	vSpecularIntensityMapUv = ( specularIntensityMapTransform * vec3( SPECULAR_INTENSITYMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_TRANSMISSIONMAP
	vTransmissionMapUv = ( transmissionMapTransform * vec3( TRANSMISSIONMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_THICKNESSMAP
	vThicknessMapUv = ( thicknessMapTransform * vec3( THICKNESSMAP_UV, 1 ) ).xy;
#endif`,Oh=`#if defined( USE_ENVMAP ) || defined( DISTANCE ) || defined ( USE_SHADOWMAP ) || defined ( USE_TRANSMISSION ) || NUM_SPOT_LIGHT_COORDS > 0
	vec4 worldPosition = vec4( transformed, 1.0 );
	#ifdef USE_BATCHING
		worldPosition = batchingMatrix * worldPosition;
	#endif
	#ifdef USE_INSTANCING
		worldPosition = instanceMatrix * worldPosition;
	#endif
	worldPosition = modelMatrix * worldPosition;
#endif`;const Bh=`varying vec2 vUv;
uniform mat3 uvTransform;
void main() {
	vUv = ( uvTransform * vec3( uv, 1 ) ).xy;
	gl_Position = vec4( position.xy, 1.0, 1.0 );
}`,jh=`uniform sampler2D t2D;
uniform float backgroundIntensity;
varying vec2 vUv;
void main() {
	vec4 texColor = texture2D( t2D, vUv );
	#ifdef DECODE_VIDEO_TEXTURE
		texColor = vec4( mix( pow( texColor.rgb * 0.9478672986 + vec3( 0.0521327014 ), vec3( 2.4 ) ), texColor.rgb * 0.0773993808, vec3( lessThanEqual( texColor.rgb, vec3( 0.04045 ) ) ) ), texColor.w );
	#endif
	texColor.rgb *= backgroundIntensity;
	gl_FragColor = texColor;
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
}`,Vh=`varying vec3 vWorldDirection;
#include <common>
void main() {
	vWorldDirection = transformDirection( position, modelMatrix );
	#include <begin_vertex>
	#include <project_vertex>
	gl_Position.z = gl_Position.w;
}`,Hh=`#ifdef ENVMAP_TYPE_CUBE
	uniform samplerCube envMap;
#elif defined( ENVMAP_TYPE_CUBE_UV )
	uniform sampler2D envMap;
#endif
uniform float flipEnvMap;
uniform float backgroundBlurriness;
uniform float backgroundIntensity;
uniform mat3 backgroundRotation;
varying vec3 vWorldDirection;
#include <cube_uv_reflection_fragment>
void main() {
	#ifdef ENVMAP_TYPE_CUBE
		vec4 texColor = textureCube( envMap, backgroundRotation * vec3( flipEnvMap * vWorldDirection.x, vWorldDirection.yz ) );
	#elif defined( ENVMAP_TYPE_CUBE_UV )
		vec4 texColor = textureCubeUV( envMap, backgroundRotation * vWorldDirection, backgroundBlurriness );
	#else
		vec4 texColor = vec4( 0.0, 0.0, 0.0, 1.0 );
	#endif
	texColor.rgb *= backgroundIntensity;
	gl_FragColor = texColor;
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
}`,Gh=`varying vec3 vWorldDirection;
#include <common>
void main() {
	vWorldDirection = transformDirection( position, modelMatrix );
	#include <begin_vertex>
	#include <project_vertex>
	gl_Position.z = gl_Position.w;
}`,Wh=`uniform samplerCube tCube;
uniform float tFlip;
uniform float opacity;
varying vec3 vWorldDirection;
void main() {
	vec4 texColor = textureCube( tCube, vec3( tFlip * vWorldDirection.x, vWorldDirection.yz ) );
	gl_FragColor = texColor;
	gl_FragColor.a *= opacity;
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
}`,Xh=`#include <common>
#include <batching_pars_vertex>
#include <uv_pars_vertex>
#include <displacementmap_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
varying vec2 vHighPrecisionZW;
void main() {
	#include <uv_vertex>
	#include <batching_vertex>
	#include <skinbase_vertex>
	#include <morphinstance_vertex>
	#ifdef USE_DISPLACEMENTMAP
		#include <beginnormal_vertex>
		#include <morphnormal_vertex>
		#include <skinnormal_vertex>
	#endif
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <displacementmap_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	vHighPrecisionZW = gl_Position.zw;
}`,Kh=`#if DEPTH_PACKING == 3200
	uniform float opacity;
#endif
#include <common>
#include <packing>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <alphamap_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
varying vec2 vHighPrecisionZW;
void main() {
	vec4 diffuseColor = vec4( 1.0 );
	#include <clipping_planes_fragment>
	#if DEPTH_PACKING == 3200
		diffuseColor.a = opacity;
	#endif
	#include <map_fragment>
	#include <alphamap_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	#include <logdepthbuf_fragment>
	float fragCoordZ = 0.5 * vHighPrecisionZW[0] / vHighPrecisionZW[1] + 0.5;
	#if DEPTH_PACKING == 3200
		gl_FragColor = vec4( vec3( 1.0 - fragCoordZ ), opacity );
	#elif DEPTH_PACKING == 3201
		gl_FragColor = packDepthToRGBA( fragCoordZ );
	#elif DEPTH_PACKING == 3202
		gl_FragColor = vec4( packDepthToRGB( fragCoordZ ), 1.0 );
	#elif DEPTH_PACKING == 3203
		gl_FragColor = vec4( packDepthToRG( fragCoordZ ), 0.0, 1.0 );
	#endif
}`,qh=`#define DISTANCE
varying vec3 vWorldPosition;
#include <common>
#include <batching_pars_vertex>
#include <uv_pars_vertex>
#include <displacementmap_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	#include <uv_vertex>
	#include <batching_vertex>
	#include <skinbase_vertex>
	#include <morphinstance_vertex>
	#ifdef USE_DISPLACEMENTMAP
		#include <beginnormal_vertex>
		#include <morphnormal_vertex>
		#include <skinnormal_vertex>
	#endif
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <displacementmap_vertex>
	#include <project_vertex>
	#include <worldpos_vertex>
	#include <clipping_planes_vertex>
	vWorldPosition = worldPosition.xyz;
}`,$h=`#define DISTANCE
uniform vec3 referencePosition;
uniform float nearDistance;
uniform float farDistance;
varying vec3 vWorldPosition;
#include <common>
#include <packing>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <alphamap_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <clipping_planes_pars_fragment>
void main () {
	vec4 diffuseColor = vec4( 1.0 );
	#include <clipping_planes_fragment>
	#include <map_fragment>
	#include <alphamap_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	float dist = length( vWorldPosition - referencePosition );
	dist = ( dist - nearDistance ) / ( farDistance - nearDistance );
	dist = saturate( dist );
	gl_FragColor = packDepthToRGBA( dist );
}`,Yh=`varying vec3 vWorldDirection;
#include <common>
void main() {
	vWorldDirection = transformDirection( position, modelMatrix );
	#include <begin_vertex>
	#include <project_vertex>
}`,Zh=`uniform sampler2D tEquirect;
varying vec3 vWorldDirection;
#include <common>
void main() {
	vec3 direction = normalize( vWorldDirection );
	vec2 sampleUV = equirectUv( direction );
	gl_FragColor = texture2D( tEquirect, sampleUV );
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
}`,Jh=`uniform float scale;
attribute float lineDistance;
varying float vLineDistance;
#include <common>
#include <uv_pars_vertex>
#include <color_pars_vertex>
#include <fog_pars_vertex>
#include <morphtarget_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	vLineDistance = scale * lineDistance;
	#include <uv_vertex>
	#include <color_vertex>
	#include <morphinstance_vertex>
	#include <morphcolor_vertex>
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	#include <fog_vertex>
}`,Qh=`uniform vec3 diffuse;
uniform float opacity;
uniform float dashSize;
uniform float totalSize;
varying float vLineDistance;
#include <common>
#include <color_pars_fragment>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <fog_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( diffuse, opacity );
	#include <clipping_planes_fragment>
	if ( mod( vLineDistance, totalSize ) > dashSize ) {
		discard;
	}
	vec3 outgoingLight = vec3( 0.0 );
	#include <logdepthbuf_fragment>
	#include <map_fragment>
	#include <color_fragment>
	outgoingLight = diffuseColor.rgb;
	#include <opaque_fragment>
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
	#include <premultiplied_alpha_fragment>
}`,ef=`#include <common>
#include <batching_pars_vertex>
#include <uv_pars_vertex>
#include <envmap_pars_vertex>
#include <color_pars_vertex>
#include <fog_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	#include <uv_vertex>
	#include <color_vertex>
	#include <morphinstance_vertex>
	#include <morphcolor_vertex>
	#include <batching_vertex>
	#if defined ( USE_ENVMAP ) || defined ( USE_SKINNING )
		#include <beginnormal_vertex>
		#include <morphnormal_vertex>
		#include <skinbase_vertex>
		#include <skinnormal_vertex>
		#include <defaultnormal_vertex>
	#endif
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	#include <worldpos_vertex>
	#include <envmap_vertex>
	#include <fog_vertex>
}`,tf=`uniform vec3 diffuse;
uniform float opacity;
#ifndef FLAT_SHADED
	varying vec3 vNormal;
#endif
#include <common>
#include <dithering_pars_fragment>
#include <color_pars_fragment>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <alphamap_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <aomap_pars_fragment>
#include <lightmap_pars_fragment>
#include <envmap_common_pars_fragment>
#include <envmap_pars_fragment>
#include <fog_pars_fragment>
#include <specularmap_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( diffuse, opacity );
	#include <clipping_planes_fragment>
	#include <logdepthbuf_fragment>
	#include <map_fragment>
	#include <color_fragment>
	#include <alphamap_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	#include <specularmap_fragment>
	ReflectedLight reflectedLight = ReflectedLight( vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ) );
	#ifdef USE_LIGHTMAP
		vec4 lightMapTexel = texture2D( lightMap, vLightMapUv );
		reflectedLight.indirectDiffuse += lightMapTexel.rgb * lightMapIntensity * RECIPROCAL_PI;
	#else
		reflectedLight.indirectDiffuse += vec3( 1.0 );
	#endif
	#include <aomap_fragment>
	reflectedLight.indirectDiffuse *= diffuseColor.rgb;
	vec3 outgoingLight = reflectedLight.indirectDiffuse;
	#include <envmap_fragment>
	#include <opaque_fragment>
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
	#include <premultiplied_alpha_fragment>
	#include <dithering_fragment>
}`,nf=`#define LAMBERT
varying vec3 vViewPosition;
#include <common>
#include <batching_pars_vertex>
#include <uv_pars_vertex>
#include <displacementmap_pars_vertex>
#include <envmap_pars_vertex>
#include <color_pars_vertex>
#include <fog_pars_vertex>
#include <normal_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <shadowmap_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	#include <uv_vertex>
	#include <color_vertex>
	#include <morphinstance_vertex>
	#include <morphcolor_vertex>
	#include <batching_vertex>
	#include <beginnormal_vertex>
	#include <morphnormal_vertex>
	#include <skinbase_vertex>
	#include <skinnormal_vertex>
	#include <defaultnormal_vertex>
	#include <normal_vertex>
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <displacementmap_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	vViewPosition = - mvPosition.xyz;
	#include <worldpos_vertex>
	#include <envmap_vertex>
	#include <shadowmap_vertex>
	#include <fog_vertex>
}`,rf=`#define LAMBERT
uniform vec3 diffuse;
uniform vec3 emissive;
uniform float opacity;
#include <common>
#include <packing>
#include <dithering_pars_fragment>
#include <color_pars_fragment>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <alphamap_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <aomap_pars_fragment>
#include <lightmap_pars_fragment>
#include <emissivemap_pars_fragment>
#include <envmap_common_pars_fragment>
#include <envmap_pars_fragment>
#include <fog_pars_fragment>
#include <bsdfs>
#include <lights_pars_begin>
#include <normal_pars_fragment>
#include <lights_lambert_pars_fragment>
#include <shadowmap_pars_fragment>
#include <bumpmap_pars_fragment>
#include <normalmap_pars_fragment>
#include <specularmap_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( diffuse, opacity );
	#include <clipping_planes_fragment>
	ReflectedLight reflectedLight = ReflectedLight( vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ) );
	vec3 totalEmissiveRadiance = emissive;
	#include <logdepthbuf_fragment>
	#include <map_fragment>
	#include <color_fragment>
	#include <alphamap_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	#include <specularmap_fragment>
	#include <normal_fragment_begin>
	#include <normal_fragment_maps>
	#include <emissivemap_fragment>
	#include <lights_lambert_fragment>
	#include <lights_fragment_begin>
	#include <lights_fragment_maps>
	#include <lights_fragment_end>
	#include <aomap_fragment>
	vec3 outgoingLight = reflectedLight.directDiffuse + reflectedLight.indirectDiffuse + totalEmissiveRadiance;
	#include <envmap_fragment>
	#include <opaque_fragment>
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
	#include <premultiplied_alpha_fragment>
	#include <dithering_fragment>
}`,af=`#define MATCAP
varying vec3 vViewPosition;
#include <common>
#include <batching_pars_vertex>
#include <uv_pars_vertex>
#include <color_pars_vertex>
#include <displacementmap_pars_vertex>
#include <fog_pars_vertex>
#include <normal_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	#include <uv_vertex>
	#include <color_vertex>
	#include <morphinstance_vertex>
	#include <morphcolor_vertex>
	#include <batching_vertex>
	#include <beginnormal_vertex>
	#include <morphnormal_vertex>
	#include <skinbase_vertex>
	#include <skinnormal_vertex>
	#include <defaultnormal_vertex>
	#include <normal_vertex>
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <displacementmap_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	#include <fog_vertex>
	vViewPosition = - mvPosition.xyz;
}`,sf=`#define MATCAP
uniform vec3 diffuse;
uniform float opacity;
uniform sampler2D matcap;
varying vec3 vViewPosition;
#include <common>
#include <dithering_pars_fragment>
#include <color_pars_fragment>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <alphamap_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <fog_pars_fragment>
#include <normal_pars_fragment>
#include <bumpmap_pars_fragment>
#include <normalmap_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( diffuse, opacity );
	#include <clipping_planes_fragment>
	#include <logdepthbuf_fragment>
	#include <map_fragment>
	#include <color_fragment>
	#include <alphamap_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	#include <normal_fragment_begin>
	#include <normal_fragment_maps>
	vec3 viewDir = normalize( vViewPosition );
	vec3 x = normalize( vec3( viewDir.z, 0.0, - viewDir.x ) );
	vec3 y = cross( viewDir, x );
	vec2 uv = vec2( dot( x, normal ), dot( y, normal ) ) * 0.495 + 0.5;
	#ifdef USE_MATCAP
		vec4 matcapColor = texture2D( matcap, uv );
	#else
		vec4 matcapColor = vec4( vec3( mix( 0.2, 0.8, uv.y ) ), 1.0 );
	#endif
	vec3 outgoingLight = diffuseColor.rgb * matcapColor.rgb;
	#include <opaque_fragment>
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
	#include <premultiplied_alpha_fragment>
	#include <dithering_fragment>
}`,of=`#define NORMAL
#if defined( FLAT_SHADED ) || defined( USE_BUMPMAP ) || defined( USE_NORMALMAP_TANGENTSPACE )
	varying vec3 vViewPosition;
#endif
#include <common>
#include <batching_pars_vertex>
#include <uv_pars_vertex>
#include <displacementmap_pars_vertex>
#include <normal_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	#include <uv_vertex>
	#include <batching_vertex>
	#include <beginnormal_vertex>
	#include <morphinstance_vertex>
	#include <morphnormal_vertex>
	#include <skinbase_vertex>
	#include <skinnormal_vertex>
	#include <defaultnormal_vertex>
	#include <normal_vertex>
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <displacementmap_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
#if defined( FLAT_SHADED ) || defined( USE_BUMPMAP ) || defined( USE_NORMALMAP_TANGENTSPACE )
	vViewPosition = - mvPosition.xyz;
#endif
}`,cf=`#define NORMAL
uniform float opacity;
#if defined( FLAT_SHADED ) || defined( USE_BUMPMAP ) || defined( USE_NORMALMAP_TANGENTSPACE )
	varying vec3 vViewPosition;
#endif
#include <packing>
#include <uv_pars_fragment>
#include <normal_pars_fragment>
#include <bumpmap_pars_fragment>
#include <normalmap_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( 0.0, 0.0, 0.0, opacity );
	#include <clipping_planes_fragment>
	#include <logdepthbuf_fragment>
	#include <normal_fragment_begin>
	#include <normal_fragment_maps>
	gl_FragColor = vec4( packNormalToRGB( normal ), diffuseColor.a );
	#ifdef OPAQUE
		gl_FragColor.a = 1.0;
	#endif
}`,lf=`#define PHONG
varying vec3 vViewPosition;
#include <common>
#include <batching_pars_vertex>
#include <uv_pars_vertex>
#include <displacementmap_pars_vertex>
#include <envmap_pars_vertex>
#include <color_pars_vertex>
#include <fog_pars_vertex>
#include <normal_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <shadowmap_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	#include <uv_vertex>
	#include <color_vertex>
	#include <morphcolor_vertex>
	#include <batching_vertex>
	#include <beginnormal_vertex>
	#include <morphinstance_vertex>
	#include <morphnormal_vertex>
	#include <skinbase_vertex>
	#include <skinnormal_vertex>
	#include <defaultnormal_vertex>
	#include <normal_vertex>
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <displacementmap_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	vViewPosition = - mvPosition.xyz;
	#include <worldpos_vertex>
	#include <envmap_vertex>
	#include <shadowmap_vertex>
	#include <fog_vertex>
}`,uf=`#define PHONG
uniform vec3 diffuse;
uniform vec3 emissive;
uniform vec3 specular;
uniform float shininess;
uniform float opacity;
#include <common>
#include <packing>
#include <dithering_pars_fragment>
#include <color_pars_fragment>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <alphamap_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <aomap_pars_fragment>
#include <lightmap_pars_fragment>
#include <emissivemap_pars_fragment>
#include <envmap_common_pars_fragment>
#include <envmap_pars_fragment>
#include <fog_pars_fragment>
#include <bsdfs>
#include <lights_pars_begin>
#include <normal_pars_fragment>
#include <lights_phong_pars_fragment>
#include <shadowmap_pars_fragment>
#include <bumpmap_pars_fragment>
#include <normalmap_pars_fragment>
#include <specularmap_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( diffuse, opacity );
	#include <clipping_planes_fragment>
	ReflectedLight reflectedLight = ReflectedLight( vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ) );
	vec3 totalEmissiveRadiance = emissive;
	#include <logdepthbuf_fragment>
	#include <map_fragment>
	#include <color_fragment>
	#include <alphamap_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	#include <specularmap_fragment>
	#include <normal_fragment_begin>
	#include <normal_fragment_maps>
	#include <emissivemap_fragment>
	#include <lights_phong_fragment>
	#include <lights_fragment_begin>
	#include <lights_fragment_maps>
	#include <lights_fragment_end>
	#include <aomap_fragment>
	vec3 outgoingLight = reflectedLight.directDiffuse + reflectedLight.indirectDiffuse + reflectedLight.directSpecular + reflectedLight.indirectSpecular + totalEmissiveRadiance;
	#include <envmap_fragment>
	#include <opaque_fragment>
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
	#include <premultiplied_alpha_fragment>
	#include <dithering_fragment>
}`,df=`#define STANDARD
varying vec3 vViewPosition;
#ifdef USE_TRANSMISSION
	varying vec3 vWorldPosition;
#endif
#include <common>
#include <batching_pars_vertex>
#include <uv_pars_vertex>
#include <displacementmap_pars_vertex>
#include <color_pars_vertex>
#include <fog_pars_vertex>
#include <normal_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <shadowmap_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	#include <uv_vertex>
	#include <color_vertex>
	#include <morphinstance_vertex>
	#include <morphcolor_vertex>
	#include <batching_vertex>
	#include <beginnormal_vertex>
	#include <morphnormal_vertex>
	#include <skinbase_vertex>
	#include <skinnormal_vertex>
	#include <defaultnormal_vertex>
	#include <normal_vertex>
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <displacementmap_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	vViewPosition = - mvPosition.xyz;
	#include <worldpos_vertex>
	#include <shadowmap_vertex>
	#include <fog_vertex>
#ifdef USE_TRANSMISSION
	vWorldPosition = worldPosition.xyz;
#endif
}`,hf=`#define STANDARD
#ifdef PHYSICAL
	#define IOR
	#define USE_SPECULAR
#endif
uniform vec3 diffuse;
uniform vec3 emissive;
uniform float roughness;
uniform float metalness;
uniform float opacity;
#ifdef IOR
	uniform float ior;
#endif
#ifdef USE_SPECULAR
	uniform float specularIntensity;
	uniform vec3 specularColor;
	#ifdef USE_SPECULAR_COLORMAP
		uniform sampler2D specularColorMap;
	#endif
	#ifdef USE_SPECULAR_INTENSITYMAP
		uniform sampler2D specularIntensityMap;
	#endif
#endif
#ifdef USE_CLEARCOAT
	uniform float clearcoat;
	uniform float clearcoatRoughness;
#endif
#ifdef USE_DISPERSION
	uniform float dispersion;
#endif
#ifdef USE_IRIDESCENCE
	uniform float iridescence;
	uniform float iridescenceIOR;
	uniform float iridescenceThicknessMinimum;
	uniform float iridescenceThicknessMaximum;
#endif
#ifdef USE_SHEEN
	uniform vec3 sheenColor;
	uniform float sheenRoughness;
	#ifdef USE_SHEEN_COLORMAP
		uniform sampler2D sheenColorMap;
	#endif
	#ifdef USE_SHEEN_ROUGHNESSMAP
		uniform sampler2D sheenRoughnessMap;
	#endif
#endif
#ifdef USE_ANISOTROPY
	uniform vec2 anisotropyVector;
	#ifdef USE_ANISOTROPYMAP
		uniform sampler2D anisotropyMap;
	#endif
#endif
varying vec3 vViewPosition;
#include <common>
#include <packing>
#include <dithering_pars_fragment>
#include <color_pars_fragment>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <alphamap_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <aomap_pars_fragment>
#include <lightmap_pars_fragment>
#include <emissivemap_pars_fragment>
#include <iridescence_fragment>
#include <cube_uv_reflection_fragment>
#include <envmap_common_pars_fragment>
#include <envmap_physical_pars_fragment>
#include <fog_pars_fragment>
#include <lights_pars_begin>
#include <normal_pars_fragment>
#include <lights_physical_pars_fragment>
#include <transmission_pars_fragment>
#include <shadowmap_pars_fragment>
#include <bumpmap_pars_fragment>
#include <normalmap_pars_fragment>
#include <clearcoat_pars_fragment>
#include <iridescence_pars_fragment>
#include <roughnessmap_pars_fragment>
#include <metalnessmap_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( diffuse, opacity );
	#include <clipping_planes_fragment>
	ReflectedLight reflectedLight = ReflectedLight( vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ) );
	vec3 totalEmissiveRadiance = emissive;
	#include <logdepthbuf_fragment>
	#include <map_fragment>
	#include <color_fragment>
	#include <alphamap_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	#include <roughnessmap_fragment>
	#include <metalnessmap_fragment>
	#include <normal_fragment_begin>
	#include <normal_fragment_maps>
	#include <clearcoat_normal_fragment_begin>
	#include <clearcoat_normal_fragment_maps>
	#include <emissivemap_fragment>
	#include <lights_physical_fragment>
	#include <lights_fragment_begin>
	#include <lights_fragment_maps>
	#include <lights_fragment_end>
	#include <aomap_fragment>
	vec3 totalDiffuse = reflectedLight.directDiffuse + reflectedLight.indirectDiffuse;
	vec3 totalSpecular = reflectedLight.directSpecular + reflectedLight.indirectSpecular;
	#include <transmission_fragment>
	vec3 outgoingLight = totalDiffuse + totalSpecular + totalEmissiveRadiance;
	#ifdef USE_SHEEN
		float sheenEnergyComp = 1.0 - 0.157 * max3( material.sheenColor );
		outgoingLight = outgoingLight * sheenEnergyComp + sheenSpecularDirect + sheenSpecularIndirect;
	#endif
	#ifdef USE_CLEARCOAT
		float dotNVcc = saturate( dot( geometryClearcoatNormal, geometryViewDir ) );
		vec3 Fcc = F_Schlick( material.clearcoatF0, material.clearcoatF90, dotNVcc );
		outgoingLight = outgoingLight * ( 1.0 - material.clearcoat * Fcc ) + ( clearcoatSpecularDirect + clearcoatSpecularIndirect ) * material.clearcoat;
	#endif
	#include <opaque_fragment>
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
	#include <premultiplied_alpha_fragment>
	#include <dithering_fragment>
}`,ff=`#define TOON
varying vec3 vViewPosition;
#include <common>
#include <batching_pars_vertex>
#include <uv_pars_vertex>
#include <displacementmap_pars_vertex>
#include <color_pars_vertex>
#include <fog_pars_vertex>
#include <normal_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <shadowmap_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	#include <uv_vertex>
	#include <color_vertex>
	#include <morphinstance_vertex>
	#include <morphcolor_vertex>
	#include <batching_vertex>
	#include <beginnormal_vertex>
	#include <morphnormal_vertex>
	#include <skinbase_vertex>
	#include <skinnormal_vertex>
	#include <defaultnormal_vertex>
	#include <normal_vertex>
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <displacementmap_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	vViewPosition = - mvPosition.xyz;
	#include <worldpos_vertex>
	#include <shadowmap_vertex>
	#include <fog_vertex>
}`,pf=`#define TOON
uniform vec3 diffuse;
uniform vec3 emissive;
uniform float opacity;
#include <common>
#include <packing>
#include <dithering_pars_fragment>
#include <color_pars_fragment>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <alphamap_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <aomap_pars_fragment>
#include <lightmap_pars_fragment>
#include <emissivemap_pars_fragment>
#include <gradientmap_pars_fragment>
#include <fog_pars_fragment>
#include <bsdfs>
#include <lights_pars_begin>
#include <normal_pars_fragment>
#include <lights_toon_pars_fragment>
#include <shadowmap_pars_fragment>
#include <bumpmap_pars_fragment>
#include <normalmap_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( diffuse, opacity );
	#include <clipping_planes_fragment>
	ReflectedLight reflectedLight = ReflectedLight( vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ) );
	vec3 totalEmissiveRadiance = emissive;
	#include <logdepthbuf_fragment>
	#include <map_fragment>
	#include <color_fragment>
	#include <alphamap_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	#include <normal_fragment_begin>
	#include <normal_fragment_maps>
	#include <emissivemap_fragment>
	#include <lights_toon_fragment>
	#include <lights_fragment_begin>
	#include <lights_fragment_maps>
	#include <lights_fragment_end>
	#include <aomap_fragment>
	vec3 outgoingLight = reflectedLight.directDiffuse + reflectedLight.indirectDiffuse + totalEmissiveRadiance;
	#include <opaque_fragment>
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
	#include <premultiplied_alpha_fragment>
	#include <dithering_fragment>
}`,mf=`uniform float size;
uniform float scale;
#include <common>
#include <color_pars_vertex>
#include <fog_pars_vertex>
#include <morphtarget_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
#ifdef USE_POINTS_UV
	varying vec2 vUv;
	uniform mat3 uvTransform;
#endif
void main() {
	#ifdef USE_POINTS_UV
		vUv = ( uvTransform * vec3( uv, 1 ) ).xy;
	#endif
	#include <color_vertex>
	#include <morphinstance_vertex>
	#include <morphcolor_vertex>
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <project_vertex>
	gl_PointSize = size;
	#ifdef USE_SIZEATTENUATION
		bool isPerspective = isPerspectiveMatrix( projectionMatrix );
		if ( isPerspective ) gl_PointSize *= ( scale / - mvPosition.z );
	#endif
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	#include <worldpos_vertex>
	#include <fog_vertex>
}`,gf=`uniform vec3 diffuse;
uniform float opacity;
#include <common>
#include <color_pars_fragment>
#include <map_particle_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <fog_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( diffuse, opacity );
	#include <clipping_planes_fragment>
	vec3 outgoingLight = vec3( 0.0 );
	#include <logdepthbuf_fragment>
	#include <map_particle_fragment>
	#include <color_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	outgoingLight = diffuseColor.rgb;
	#include <opaque_fragment>
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
	#include <premultiplied_alpha_fragment>
}`,_f=`#include <common>
#include <batching_pars_vertex>
#include <fog_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <shadowmap_pars_vertex>
void main() {
	#include <batching_vertex>
	#include <beginnormal_vertex>
	#include <morphinstance_vertex>
	#include <morphnormal_vertex>
	#include <skinbase_vertex>
	#include <skinnormal_vertex>
	#include <defaultnormal_vertex>
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <worldpos_vertex>
	#include <shadowmap_vertex>
	#include <fog_vertex>
}`,vf=`uniform vec3 color;
uniform float opacity;
#include <common>
#include <packing>
#include <fog_pars_fragment>
#include <bsdfs>
#include <lights_pars_begin>
#include <logdepthbuf_pars_fragment>
#include <shadowmap_pars_fragment>
#include <shadowmask_pars_fragment>
void main() {
	#include <logdepthbuf_fragment>
	gl_FragColor = vec4( color, opacity * ( 1.0 - getShadowMask() ) );
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
}`,xf=`uniform float rotation;
uniform vec2 center;
#include <common>
#include <uv_pars_vertex>
#include <fog_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	#include <uv_vertex>
	vec4 mvPosition = modelViewMatrix[ 3 ];
	vec2 scale = vec2( length( modelMatrix[ 0 ].xyz ), length( modelMatrix[ 1 ].xyz ) );
	#ifndef USE_SIZEATTENUATION
		bool isPerspective = isPerspectiveMatrix( projectionMatrix );
		if ( isPerspective ) scale *= - mvPosition.z;
	#endif
	vec2 alignedPosition = ( position.xy - ( center - vec2( 0.5 ) ) ) * scale;
	vec2 rotatedPosition;
	rotatedPosition.x = cos( rotation ) * alignedPosition.x - sin( rotation ) * alignedPosition.y;
	rotatedPosition.y = sin( rotation ) * alignedPosition.x + cos( rotation ) * alignedPosition.y;
	mvPosition.xy += rotatedPosition;
	gl_Position = projectionMatrix * mvPosition;
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	#include <fog_vertex>
}`,Mf=`uniform vec3 diffuse;
uniform float opacity;
#include <common>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <alphamap_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <fog_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( diffuse, opacity );
	#include <clipping_planes_fragment>
	vec3 outgoingLight = vec3( 0.0 );
	#include <logdepthbuf_fragment>
	#include <map_fragment>
	#include <alphamap_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	outgoingLight = diffuseColor.rgb;
	#include <opaque_fragment>
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
}`,Ve={alphahash_fragment:ju,alphahash_pars_fragment:Vu,alphamap_fragment:Hu,alphamap_pars_fragment:Gu,alphatest_fragment:Wu,alphatest_pars_fragment:Xu,aomap_fragment:Ku,aomap_pars_fragment:qu,batching_pars_vertex:$u,batching_vertex:Yu,begin_vertex:Zu,beginnormal_vertex:Ju,bsdfs:Qu,iridescence_fragment:ed,bumpmap_pars_fragment:td,clipping_planes_fragment:nd,clipping_planes_pars_fragment:id,clipping_planes_pars_vertex:rd,clipping_planes_vertex:ad,color_fragment:sd,color_pars_fragment:od,color_pars_vertex:cd,color_vertex:ld,common:ud,cube_uv_reflection_fragment:dd,defaultnormal_vertex:hd,displacementmap_pars_vertex:fd,displacementmap_vertex:pd,emissivemap_fragment:md,emissivemap_pars_fragment:gd,colorspace_fragment:_d,colorspace_pars_fragment:vd,envmap_fragment:xd,envmap_common_pars_fragment:Md,envmap_pars_fragment:Sd,envmap_pars_vertex:Ed,envmap_physical_pars_fragment:Id,envmap_vertex:bd,fog_vertex:yd,fog_pars_vertex:Td,fog_fragment:wd,fog_pars_fragment:Ad,gradientmap_pars_fragment:Rd,lightmap_pars_fragment:Cd,lights_lambert_fragment:Pd,lights_lambert_pars_fragment:Dd,lights_pars_begin:Ld,lights_toon_fragment:Ud,lights_toon_pars_fragment:zd,lights_phong_fragment:Nd,lights_phong_pars_fragment:kd,lights_physical_fragment:Fd,lights_physical_pars_fragment:Od,lights_fragment_begin:Bd,lights_fragment_maps:jd,lights_fragment_end:Vd,logdepthbuf_fragment:Hd,logdepthbuf_pars_fragment:Gd,logdepthbuf_pars_vertex:Wd,logdepthbuf_vertex:Xd,map_fragment:Kd,map_pars_fragment:qd,map_particle_fragment:$d,map_particle_pars_fragment:Yd,metalnessmap_fragment:Zd,metalnessmap_pars_fragment:Jd,morphinstance_vertex:Qd,morphcolor_vertex:eh,morphnormal_vertex:th,morphtarget_pars_vertex:nh,morphtarget_vertex:ih,normal_fragment_begin:rh,normal_fragment_maps:ah,normal_pars_fragment:sh,normal_pars_vertex:oh,normal_vertex:ch,normalmap_pars_fragment:lh,clearcoat_normal_fragment_begin:uh,clearcoat_normal_fragment_maps:dh,clearcoat_pars_fragment:hh,iridescence_pars_fragment:fh,opaque_fragment:ph,packing:mh,premultiplied_alpha_fragment:gh,project_vertex:_h,dithering_fragment:vh,dithering_pars_fragment:xh,roughnessmap_fragment:Mh,roughnessmap_pars_fragment:Sh,shadowmap_pars_fragment:Eh,shadowmap_pars_vertex:bh,shadowmap_vertex:yh,shadowmask_pars_fragment:Th,skinbase_vertex:wh,skinning_pars_vertex:Ah,skinning_vertex:Rh,skinnormal_vertex:Ch,specularmap_fragment:Ph,specularmap_pars_fragment:Dh,tonemapping_fragment:Lh,tonemapping_pars_fragment:Ih,transmission_fragment:Uh,transmission_pars_fragment:zh,uv_pars_fragment:Nh,uv_pars_vertex:kh,uv_vertex:Fh,worldpos_vertex:Oh,background_vert:Bh,background_frag:jh,backgroundCube_vert:Vh,backgroundCube_frag:Hh,cube_vert:Gh,cube_frag:Wh,depth_vert:Xh,depth_frag:Kh,distanceRGBA_vert:qh,distanceRGBA_frag:$h,equirect_vert:Yh,equirect_frag:Zh,linedashed_vert:Jh,linedashed_frag:Qh,meshbasic_vert:ef,meshbasic_frag:tf,meshlambert_vert:nf,meshlambert_frag:rf,meshmatcap_vert:af,meshmatcap_frag:sf,meshnormal_vert:of,meshnormal_frag:cf,meshphong_vert:lf,meshphong_frag:uf,meshphysical_vert:df,meshphysical_frag:hf,meshtoon_vert:ff,meshtoon_frag:pf,points_vert:mf,points_frag:gf,shadow_vert:_f,shadow_frag:vf,sprite_vert:xf,sprite_frag:Mf},he={common:{diffuse:{value:new ce(16777215)},opacity:{value:1},map:{value:null},mapTransform:{value:new Be},alphaMap:{value:null},alphaMapTransform:{value:new Be},alphaTest:{value:0}},specularmap:{specularMap:{value:null},specularMapTransform:{value:new Be}},envmap:{envMap:{value:null},envMapRotation:{value:new Be},flipEnvMap:{value:-1},reflectivity:{value:1},ior:{value:1.5},refractionRatio:{value:.98}},aomap:{aoMap:{value:null},aoMapIntensity:{value:1},aoMapTransform:{value:new Be}},lightmap:{lightMap:{value:null},lightMapIntensity:{value:1},lightMapTransform:{value:new Be}},bumpmap:{bumpMap:{value:null},bumpMapTransform:{value:new Be},bumpScale:{value:1}},normalmap:{normalMap:{value:null},normalMapTransform:{value:new Be},normalScale:{value:new Ke(1,1)}},displacementmap:{displacementMap:{value:null},displacementMapTransform:{value:new Be},displacementScale:{value:1},displacementBias:{value:0}},emissivemap:{emissiveMap:{value:null},emissiveMapTransform:{value:new Be}},metalnessmap:{metalnessMap:{value:null},metalnessMapTransform:{value:new Be}},roughnessmap:{roughnessMap:{value:null},roughnessMapTransform:{value:new Be}},gradientmap:{gradientMap:{value:null}},fog:{fogDensity:{value:25e-5},fogNear:{value:1},fogFar:{value:2e3},fogColor:{value:new ce(16777215)}},lights:{ambientLightColor:{value:[]},lightProbe:{value:[]},directionalLights:{value:[],properties:{direction:{},color:{}}},directionalLightShadows:{value:[],properties:{shadowIntensity:1,shadowBias:{},shadowNormalBias:{},shadowRadius:{},shadowMapSize:{}}},directionalShadowMap:{value:[]},directionalShadowMatrix:{value:[]},spotLights:{value:[],properties:{color:{},position:{},direction:{},distance:{},coneCos:{},penumbraCos:{},decay:{}}},spotLightShadows:{value:[],properties:{shadowIntensity:1,shadowBias:{},shadowNormalBias:{},shadowRadius:{},shadowMapSize:{}}},spotLightMap:{value:[]},spotShadowMap:{value:[]},spotLightMatrix:{value:[]},pointLights:{value:[],properties:{color:{},position:{},decay:{},distance:{}}},pointLightShadows:{value:[],properties:{shadowIntensity:1,shadowBias:{},shadowNormalBias:{},shadowRadius:{},shadowMapSize:{},shadowCameraNear:{},shadowCameraFar:{}}},pointShadowMap:{value:[]},pointShadowMatrix:{value:[]},hemisphereLights:{value:[],properties:{direction:{},skyColor:{},groundColor:{}}},rectAreaLights:{value:[],properties:{color:{},position:{},width:{},height:{}}},ltc_1:{value:null},ltc_2:{value:null}},points:{diffuse:{value:new ce(16777215)},opacity:{value:1},size:{value:1},scale:{value:1},map:{value:null},alphaMap:{value:null},alphaMapTransform:{value:new Be},alphaTest:{value:0},uvTransform:{value:new Be}},sprite:{diffuse:{value:new ce(16777215)},opacity:{value:1},center:{value:new Ke(.5,.5)},rotation:{value:0},map:{value:null},mapTransform:{value:new Be},alphaMap:{value:null},alphaMapTransform:{value:new Be},alphaTest:{value:0}}},en={basic:{uniforms:Rt([he.common,he.specularmap,he.envmap,he.aomap,he.lightmap,he.fog]),vertexShader:Ve.meshbasic_vert,fragmentShader:Ve.meshbasic_frag},lambert:{uniforms:Rt([he.common,he.specularmap,he.envmap,he.aomap,he.lightmap,he.emissivemap,he.bumpmap,he.normalmap,he.displacementmap,he.fog,he.lights,{emissive:{value:new ce(0)}}]),vertexShader:Ve.meshlambert_vert,fragmentShader:Ve.meshlambert_frag},phong:{uniforms:Rt([he.common,he.specularmap,he.envmap,he.aomap,he.lightmap,he.emissivemap,he.bumpmap,he.normalmap,he.displacementmap,he.fog,he.lights,{emissive:{value:new ce(0)},specular:{value:new ce(1118481)},shininess:{value:30}}]),vertexShader:Ve.meshphong_vert,fragmentShader:Ve.meshphong_frag},standard:{uniforms:Rt([he.common,he.envmap,he.aomap,he.lightmap,he.emissivemap,he.bumpmap,he.normalmap,he.displacementmap,he.roughnessmap,he.metalnessmap,he.fog,he.lights,{emissive:{value:new ce(0)},roughness:{value:1},metalness:{value:0},envMapIntensity:{value:1}}]),vertexShader:Ve.meshphysical_vert,fragmentShader:Ve.meshphysical_frag},toon:{uniforms:Rt([he.common,he.aomap,he.lightmap,he.emissivemap,he.bumpmap,he.normalmap,he.displacementmap,he.gradientmap,he.fog,he.lights,{emissive:{value:new ce(0)}}]),vertexShader:Ve.meshtoon_vert,fragmentShader:Ve.meshtoon_frag},matcap:{uniforms:Rt([he.common,he.bumpmap,he.normalmap,he.displacementmap,he.fog,{matcap:{value:null}}]),vertexShader:Ve.meshmatcap_vert,fragmentShader:Ve.meshmatcap_frag},points:{uniforms:Rt([he.points,he.fog]),vertexShader:Ve.points_vert,fragmentShader:Ve.points_frag},dashed:{uniforms:Rt([he.common,he.fog,{scale:{value:1},dashSize:{value:1},totalSize:{value:2}}]),vertexShader:Ve.linedashed_vert,fragmentShader:Ve.linedashed_frag},depth:{uniforms:Rt([he.common,he.displacementmap]),vertexShader:Ve.depth_vert,fragmentShader:Ve.depth_frag},normal:{uniforms:Rt([he.common,he.bumpmap,he.normalmap,he.displacementmap,{opacity:{value:1}}]),vertexShader:Ve.meshnormal_vert,fragmentShader:Ve.meshnormal_frag},sprite:{uniforms:Rt([he.sprite,he.fog]),vertexShader:Ve.sprite_vert,fragmentShader:Ve.sprite_frag},background:{uniforms:{uvTransform:{value:new Be},t2D:{value:null},backgroundIntensity:{value:1}},vertexShader:Ve.background_vert,fragmentShader:Ve.background_frag},backgroundCube:{uniforms:{envMap:{value:null},flipEnvMap:{value:-1},backgroundBlurriness:{value:0},backgroundIntensity:{value:1},backgroundRotation:{value:new Be}},vertexShader:Ve.backgroundCube_vert,fragmentShader:Ve.backgroundCube_frag},cube:{uniforms:{tCube:{value:null},tFlip:{value:-1},opacity:{value:1}},vertexShader:Ve.cube_vert,fragmentShader:Ve.cube_frag},equirect:{uniforms:{tEquirect:{value:null}},vertexShader:Ve.equirect_vert,fragmentShader:Ve.equirect_frag},distanceRGBA:{uniforms:Rt([he.common,he.displacementmap,{referencePosition:{value:new F},nearDistance:{value:1},farDistance:{value:1e3}}]),vertexShader:Ve.distanceRGBA_vert,fragmentShader:Ve.distanceRGBA_frag},shadow:{uniforms:Rt([he.lights,he.fog,{color:{value:new ce(0)},opacity:{value:1}}]),vertexShader:Ve.shadow_vert,fragmentShader:Ve.shadow_frag}};en.physical={uniforms:Rt([en.standard.uniforms,{clearcoat:{value:0},clearcoatMap:{value:null},clearcoatMapTransform:{value:new Be},clearcoatNormalMap:{value:null},clearcoatNormalMapTransform:{value:new Be},clearcoatNormalScale:{value:new Ke(1,1)},clearcoatRoughness:{value:0},clearcoatRoughnessMap:{value:null},clearcoatRoughnessMapTransform:{value:new Be},dispersion:{value:0},iridescence:{value:0},iridescenceMap:{value:null},iridescenceMapTransform:{value:new Be},iridescenceIOR:{value:1.3},iridescenceThicknessMinimum:{value:100},iridescenceThicknessMaximum:{value:400},iridescenceThicknessMap:{value:null},iridescenceThicknessMapTransform:{value:new Be},sheen:{value:0},sheenColor:{value:new ce(0)},sheenColorMap:{value:null},sheenColorMapTransform:{value:new Be},sheenRoughness:{value:1},sheenRoughnessMap:{value:null},sheenRoughnessMapTransform:{value:new Be},transmission:{value:0},transmissionMap:{value:null},transmissionMapTransform:{value:new Be},transmissionSamplerSize:{value:new Ke},transmissionSamplerMap:{value:null},thickness:{value:0},thicknessMap:{value:null},thicknessMapTransform:{value:new Be},attenuationDistance:{value:0},attenuationColor:{value:new ce(0)},specularColor:{value:new ce(1,1,1)},specularColorMap:{value:null},specularColorMapTransform:{value:new Be},specularIntensity:{value:1},specularIntensityMap:{value:null},specularIntensityMapTransform:{value:new Be},anisotropyVector:{value:new Ke},anisotropyMap:{value:null},anisotropyMapTransform:{value:new Be}}]),vertexShader:Ve.meshphysical_vert,fragmentShader:Ve.meshphysical_frag};const yr={r:0,b:0,g:0},Bn=new mt,Sf=new ct;function Ef(n,e,t,i,r,a,s){const o=new ce(0);let c=a===!0?0:1,l,d,h=null,f=0,m=null;function g(S){let M=S.isScene===!0?S.background:null;return M&&M.isTexture&&(M=(S.backgroundBlurriness>0?t:e).get(M)),M}function _(S){let M=!1;const w=g(S);w===null?u(o,c):w&&w.isColor&&(u(w,1),M=!0);const T=n.xr.getEnvironmentBlendMode();T==="additive"?i.buffers.color.setClear(0,0,0,1,s):T==="alpha-blend"&&i.buffers.color.setClear(0,0,0,0,s),(n.autoClear||M)&&(i.buffers.depth.setTest(!0),i.buffers.depth.setMask(!0),i.buffers.color.setMask(!0),n.clear(n.autoClearColor,n.autoClearDepth,n.autoClearStencil))}function p(S,M){const w=g(M);w&&(w.isCubeTexture||w.mapping===Vr)?(d===void 0&&(d=new We(new gn(1,1,1),new In({name:"BackgroundCubeMaterial",uniforms:Pi(en.backgroundCube.uniforms),vertexShader:en.backgroundCube.vertexShader,fragmentShader:en.backgroundCube.fragmentShader,side:Lt,depthTest:!1,depthWrite:!1,fog:!1})),d.geometry.deleteAttribute("normal"),d.geometry.deleteAttribute("uv"),d.onBeforeRender=function(T,A,L){this.matrixWorld.copyPosition(L.matrixWorld)},Object.defineProperty(d.material,"envMap",{get:function(){return this.uniforms.envMap.value}}),r.update(d)),Bn.copy(M.backgroundRotation),Bn.x*=-1,Bn.y*=-1,Bn.z*=-1,w.isCubeTexture&&w.isRenderTargetTexture===!1&&(Bn.y*=-1,Bn.z*=-1),d.material.uniforms.envMap.value=w,d.material.uniforms.flipEnvMap.value=w.isCubeTexture&&w.isRenderTargetTexture===!1?-1:1,d.material.uniforms.backgroundBlurriness.value=M.backgroundBlurriness,d.material.uniforms.backgroundIntensity.value=M.backgroundIntensity,d.material.uniforms.backgroundRotation.value.setFromMatrix4(Sf.makeRotationFromEuler(Bn)),d.material.toneMapped=Qe.getTransfer(w.colorSpace)!==rt,(h!==w||f!==w.version||m!==n.toneMapping)&&(d.material.needsUpdate=!0,h=w,f=w.version,m=n.toneMapping),d.layers.enableAll(),S.unshift(d,d.geometry,d.material,0,0,null)):w&&w.isTexture&&(l===void 0&&(l=new We(new zi(2,2),new In({name:"BackgroundMaterial",uniforms:Pi(en.background.uniforms),vertexShader:en.background.vertexShader,fragmentShader:en.background.fragmentShader,side:Ln,depthTest:!1,depthWrite:!1,fog:!1})),l.geometry.deleteAttribute("normal"),Object.defineProperty(l.material,"map",{get:function(){return this.uniforms.t2D.value}}),r.update(l)),l.material.uniforms.t2D.value=w,l.material.uniforms.backgroundIntensity.value=M.backgroundIntensity,l.material.toneMapped=Qe.getTransfer(w.colorSpace)!==rt,w.matrixAutoUpdate===!0&&w.updateMatrix(),l.material.uniforms.uvTransform.value.copy(w.matrix),(h!==w||f!==w.version||m!==n.toneMapping)&&(l.material.needsUpdate=!0,h=w,f=w.version,m=n.toneMapping),l.layers.enableAll(),S.unshift(l,l.geometry,l.material,0,0,null))}function u(S,M){S.getRGB(yr,kc(n)),i.buffers.color.setClear(yr.r,yr.g,yr.b,M,s)}function b(){d!==void 0&&(d.geometry.dispose(),d.material.dispose(),d=void 0),l!==void 0&&(l.geometry.dispose(),l.material.dispose(),l=void 0)}return{getClearColor:function(){return o},setClearColor:function(S,M=1){o.set(S),c=M,u(o,c)},getClearAlpha:function(){return c},setClearAlpha:function(S){c=S,u(o,c)},render:_,addToRenderList:p,dispose:b}}function bf(n,e){const t=n.getParameter(n.MAX_VERTEX_ATTRIBS),i={},r=f(null);let a=r,s=!1;function o(v,R,U,C,D){let k=!1;const N=h(C,U,R);a!==N&&(a=N,l(a.object)),k=m(v,C,U,D),k&&g(v,C,U,D),D!==null&&e.update(D,n.ELEMENT_ARRAY_BUFFER),(k||s)&&(s=!1,M(v,R,U,C),D!==null&&n.bindBuffer(n.ELEMENT_ARRAY_BUFFER,e.get(D).buffer))}function c(){return n.createVertexArray()}function l(v){return n.bindVertexArray(v)}function d(v){return n.deleteVertexArray(v)}function h(v,R,U){const C=U.wireframe===!0;let D=i[v.id];D===void 0&&(D={},i[v.id]=D);let k=D[R.id];k===void 0&&(k={},D[R.id]=k);let N=k[C];return N===void 0&&(N=f(c()),k[C]=N),N}function f(v){const R=[],U=[],C=[];for(let D=0;D<t;D++)R[D]=0,U[D]=0,C[D]=0;return{geometry:null,program:null,wireframe:!1,newAttributes:R,enabledAttributes:U,attributeDivisors:C,object:v,attributes:{},index:null}}function m(v,R,U,C){const D=a.attributes,k=R.attributes;let N=0;const O=U.getAttributes();for(const z in O)if(O[z].location>=0){const q=D[z];let J=k[z];if(J===void 0&&(z==="instanceMatrix"&&v.instanceMatrix&&(J=v.instanceMatrix),z==="instanceColor"&&v.instanceColor&&(J=v.instanceColor)),q===void 0||q.attribute!==J||J&&q.data!==J.data)return!0;N++}return a.attributesNum!==N||a.index!==C}function g(v,R,U,C){const D={},k=R.attributes;let N=0;const O=U.getAttributes();for(const z in O)if(O[z].location>=0){let q=k[z];q===void 0&&(z==="instanceMatrix"&&v.instanceMatrix&&(q=v.instanceMatrix),z==="instanceColor"&&v.instanceColor&&(q=v.instanceColor));const J={};J.attribute=q,q&&q.data&&(J.data=q.data),D[z]=J,N++}a.attributes=D,a.attributesNum=N,a.index=C}function _(){const v=a.newAttributes;for(let R=0,U=v.length;R<U;R++)v[R]=0}function p(v){u(v,0)}function u(v,R){const U=a.newAttributes,C=a.enabledAttributes,D=a.attributeDivisors;U[v]=1,C[v]===0&&(n.enableVertexAttribArray(v),C[v]=1),D[v]!==R&&(n.vertexAttribDivisor(v,R),D[v]=R)}function b(){const v=a.newAttributes,R=a.enabledAttributes;for(let U=0,C=R.length;U<C;U++)R[U]!==v[U]&&(n.disableVertexAttribArray(U),R[U]=0)}function S(v,R,U,C,D,k,N){N===!0?n.vertexAttribIPointer(v,R,U,D,k):n.vertexAttribPointer(v,R,U,C,D,k)}function M(v,R,U,C){_();const D=C.attributes,k=U.getAttributes(),N=R.defaultAttributeValues;for(const O in k){const z=k[O];if(z.location>=0){let H=D[O];if(H===void 0&&(O==="instanceMatrix"&&v.instanceMatrix&&(H=v.instanceMatrix),O==="instanceColor"&&v.instanceColor&&(H=v.instanceColor)),H!==void 0){const q=H.normalized,J=H.itemSize,fe=e.get(H);if(fe===void 0)continue;const Ae=fe.buffer,K=fe.type,ne=fe.bytesPerElement,ue=K===n.INT||K===n.UNSIGNED_INT||H.gpuType===Cs;if(H.isInterleavedBufferAttribute){const ae=H.data,ee=ae.stride,_e=H.offset;if(ae.isInstancedInterleavedBuffer){for(let de=0;de<z.locationSize;de++)u(z.location+de,ae.meshPerAttribute);v.isInstancedMesh!==!0&&C._maxInstanceCount===void 0&&(C._maxInstanceCount=ae.meshPerAttribute*ae.count)}else for(let de=0;de<z.locationSize;de++)p(z.location+de);n.bindBuffer(n.ARRAY_BUFFER,Ae);for(let de=0;de<z.locationSize;de++)S(z.location+de,J/z.locationSize,K,q,ee*ne,(_e+J/z.locationSize*de)*ne,ue)}else{if(H.isInstancedBufferAttribute){for(let ae=0;ae<z.locationSize;ae++)u(z.location+ae,H.meshPerAttribute);v.isInstancedMesh!==!0&&C._maxInstanceCount===void 0&&(C._maxInstanceCount=H.meshPerAttribute*H.count)}else for(let ae=0;ae<z.locationSize;ae++)p(z.location+ae);n.bindBuffer(n.ARRAY_BUFFER,Ae);for(let ae=0;ae<z.locationSize;ae++)S(z.location+ae,J/z.locationSize,K,q,J*ne,J/z.locationSize*ae*ne,ue)}}else if(N!==void 0){const q=N[O];if(q!==void 0)switch(q.length){case 2:n.vertexAttrib2fv(z.location,q);break;case 3:n.vertexAttrib3fv(z.location,q);break;case 4:n.vertexAttrib4fv(z.location,q);break;default:n.vertexAttrib1fv(z.location,q)}}}}b()}function w(){L();for(const v in i){const R=i[v];for(const U in R){const C=R[U];for(const D in C)d(C[D].object),delete C[D];delete R[U]}delete i[v]}}function T(v){if(i[v.id]===void 0)return;const R=i[v.id];for(const U in R){const C=R[U];for(const D in C)d(C[D].object),delete C[D];delete R[U]}delete i[v.id]}function A(v){for(const R in i){const U=i[R];if(U[v.id]===void 0)continue;const C=U[v.id];for(const D in C)d(C[D].object),delete C[D];delete U[v.id]}}function L(){x(),s=!0,a!==r&&(a=r,l(a.object))}function x(){r.geometry=null,r.program=null,r.wireframe=!1}return{setup:o,reset:L,resetDefaultState:x,dispose:w,releaseStatesOfGeometry:T,releaseStatesOfProgram:A,initAttributes:_,enableAttribute:p,disableUnusedAttributes:b}}function yf(n,e,t){let i;function r(l){i=l}function a(l,d){n.drawArrays(i,l,d),t.update(d,i,1)}function s(l,d,h){h!==0&&(n.drawArraysInstanced(i,l,d,h),t.update(d,i,h))}function o(l,d,h){if(h===0)return;e.get("WEBGL_multi_draw").multiDrawArraysWEBGL(i,l,0,d,0,h);let m=0;for(let g=0;g<h;g++)m+=d[g];t.update(m,i,1)}function c(l,d,h,f){if(h===0)return;const m=e.get("WEBGL_multi_draw");if(m===null)for(let g=0;g<l.length;g++)s(l[g],d[g],f[g]);else{m.multiDrawArraysInstancedWEBGL(i,l,0,d,0,f,0,h);let g=0;for(let _=0;_<h;_++)g+=d[_]*f[_];t.update(g,i,1)}}this.setMode=r,this.render=a,this.renderInstances=s,this.renderMultiDraw=o,this.renderMultiDrawInstances=c}function Tf(n,e,t,i){let r;function a(){if(r!==void 0)return r;if(e.has("EXT_texture_filter_anisotropic")===!0){const A=e.get("EXT_texture_filter_anisotropic");r=n.getParameter(A.MAX_TEXTURE_MAX_ANISOTROPY_EXT)}else r=0;return r}function s(A){return!(A!==Zt&&i.convert(A)!==n.getParameter(n.IMPLEMENTATION_COLOR_READ_FORMAT))}function o(A){const L=A===$i&&(e.has("EXT_color_buffer_half_float")||e.has("EXT_color_buffer_float"));return!(A!==vn&&i.convert(A)!==n.getParameter(n.IMPLEMENTATION_COLOR_READ_TYPE)&&A!==pn&&!L)}function c(A){if(A==="highp"){if(n.getShaderPrecisionFormat(n.VERTEX_SHADER,n.HIGH_FLOAT).precision>0&&n.getShaderPrecisionFormat(n.FRAGMENT_SHADER,n.HIGH_FLOAT).precision>0)return"highp";A="mediump"}return A==="mediump"&&n.getShaderPrecisionFormat(n.VERTEX_SHADER,n.MEDIUM_FLOAT).precision>0&&n.getShaderPrecisionFormat(n.FRAGMENT_SHADER,n.MEDIUM_FLOAT).precision>0?"mediump":"lowp"}let l=t.precision!==void 0?t.precision:"highp";const d=c(l);d!==l&&(console.warn("THREE.WebGLRenderer:",l,"not supported, using",d,"instead."),l=d);const h=t.logarithmicDepthBuffer===!0,f=t.reverseDepthBuffer===!0&&e.has("EXT_clip_control"),m=n.getParameter(n.MAX_TEXTURE_IMAGE_UNITS),g=n.getParameter(n.MAX_VERTEX_TEXTURE_IMAGE_UNITS),_=n.getParameter(n.MAX_TEXTURE_SIZE),p=n.getParameter(n.MAX_CUBE_MAP_TEXTURE_SIZE),u=n.getParameter(n.MAX_VERTEX_ATTRIBS),b=n.getParameter(n.MAX_VERTEX_UNIFORM_VECTORS),S=n.getParameter(n.MAX_VARYING_VECTORS),M=n.getParameter(n.MAX_FRAGMENT_UNIFORM_VECTORS),w=g>0,T=n.getParameter(n.MAX_SAMPLES);return{isWebGL2:!0,getMaxAnisotropy:a,getMaxPrecision:c,textureFormatReadable:s,textureTypeReadable:o,precision:l,logarithmicDepthBuffer:h,reverseDepthBuffer:f,maxTextures:m,maxVertexTextures:g,maxTextureSize:_,maxCubemapSize:p,maxAttributes:u,maxVertexUniforms:b,maxVaryings:S,maxFragmentUniforms:M,vertexTextures:w,maxSamples:T}}function wf(n){const e=this;let t=null,i=0,r=!1,a=!1;const s=new Hn,o=new Be,c={value:null,needsUpdate:!1};this.uniform=c,this.numPlanes=0,this.numIntersection=0,this.init=function(h,f){const m=h.length!==0||f||i!==0||r;return r=f,i=h.length,m},this.beginShadows=function(){a=!0,d(null)},this.endShadows=function(){a=!1},this.setGlobalState=function(h,f){t=d(h,f,0)},this.setState=function(h,f,m){const g=h.clippingPlanes,_=h.clipIntersection,p=h.clipShadows,u=n.get(h);if(!r||g===null||g.length===0||a&&!p)a?d(null):l();else{const b=a?0:i,S=b*4;let M=u.clippingState||null;c.value=M,M=d(g,f,S,m);for(let w=0;w!==S;++w)M[w]=t[w];u.clippingState=M,this.numIntersection=_?this.numPlanes:0,this.numPlanes+=b}};function l(){c.value!==t&&(c.value=t,c.needsUpdate=i>0),e.numPlanes=i,e.numIntersection=0}function d(h,f,m,g){const _=h!==null?h.length:0;let p=null;if(_!==0){if(p=c.value,g!==!0||p===null){const u=m+_*4,b=f.matrixWorldInverse;o.getNormalMatrix(b),(p===null||p.length<u)&&(p=new Float32Array(u));for(let S=0,M=m;S!==_;++S,M+=4)s.copy(h[S]).applyMatrix4(b,o),s.normal.toArray(p,M),p[M+3]=s.constant}c.value=p,c.needsUpdate=!0}return e.numPlanes=_,e.numIntersection=0,p}}function Af(n){let e=new WeakMap;function t(s,o){return o===Va?s.mapping=Ti:o===Ha&&(s.mapping=wi),s}function i(s){if(s&&s.isTexture){const o=s.mapping;if(o===Va||o===Ha)if(e.has(s)){const c=e.get(s).texture;return t(c,s.mapping)}else{const c=s.image;if(c&&c.height>0){const l=new Au(c.height);return l.fromEquirectangularTexture(n,s),e.set(s,l),s.addEventListener("dispose",r),t(l.texture,s.mapping)}else return null}}return s}function r(s){const o=s.target;o.removeEventListener("dispose",r);const c=e.get(o);c!==void 0&&(e.delete(o),c.dispose())}function a(){e=new WeakMap}return{get:i,dispose:a}}const vi=4,No=[.125,.215,.35,.446,.526,.582],qn=20,Sa=new Vc,ko=new ce;let Ea=null,ba=0,ya=0,Ta=!1;const Gn=(1+Math.sqrt(5))/2,mi=1/Gn,Fo=[new F(-Gn,mi,0),new F(Gn,mi,0),new F(-mi,0,Gn),new F(mi,0,Gn),new F(0,Gn,-mi),new F(0,Gn,mi),new F(-1,1,-1),new F(1,1,-1),new F(-1,1,1),new F(1,1,1)],Rf=new F;class Oo{constructor(e){this._renderer=e,this._pingPongRenderTarget=null,this._lodMax=0,this._cubeSize=0,this._lodPlanes=[],this._sizeLods=[],this._sigmas=[],this._blurMaterial=null,this._cubemapMaterial=null,this._equirectMaterial=null,this._compileMaterial(this._blurMaterial)}fromScene(e,t=0,i=.1,r=100,a={}){const{size:s=256,position:o=Rf}=a;Ea=this._renderer.getRenderTarget(),ba=this._renderer.getActiveCubeFace(),ya=this._renderer.getActiveMipmapLevel(),Ta=this._renderer.xr.enabled,this._renderer.xr.enabled=!1,this._setSize(s);const c=this._allocateTargets();return c.depthBuffer=!0,this._sceneToCubeUV(e,i,r,c,o),t>0&&this._blur(c,0,0,t),this._applyPMREM(c),this._cleanup(c),c}fromEquirectangular(e,t=null){return this._fromTexture(e,t)}fromCubemap(e,t=null){return this._fromTexture(e,t)}compileCubemapShader(){this._cubemapMaterial===null&&(this._cubemapMaterial=Vo(),this._compileMaterial(this._cubemapMaterial))}compileEquirectangularShader(){this._equirectMaterial===null&&(this._equirectMaterial=jo(),this._compileMaterial(this._equirectMaterial))}dispose(){this._dispose(),this._cubemapMaterial!==null&&this._cubemapMaterial.dispose(),this._equirectMaterial!==null&&this._equirectMaterial.dispose()}_setSize(e){this._lodMax=Math.floor(Math.log2(e)),this._cubeSize=Math.pow(2,this._lodMax)}_dispose(){this._blurMaterial!==null&&this._blurMaterial.dispose(),this._pingPongRenderTarget!==null&&this._pingPongRenderTarget.dispose();for(let e=0;e<this._lodPlanes.length;e++)this._lodPlanes[e].dispose()}_cleanup(e){this._renderer.setRenderTarget(Ea,ba,ya),this._renderer.xr.enabled=Ta,e.scissorTest=!1,Tr(e,0,0,e.width,e.height)}_fromTexture(e,t){e.mapping===Ti||e.mapping===wi?this._setSize(e.image.length===0?16:e.image[0].width||e.image[0].image.width):this._setSize(e.image.width/4),Ea=this._renderer.getRenderTarget(),ba=this._renderer.getActiveCubeFace(),ya=this._renderer.getActiveMipmapLevel(),Ta=this._renderer.xr.enabled,this._renderer.xr.enabled=!1;const i=t||this._allocateTargets();return this._textureToCubeUV(e,i),this._applyPMREM(i),this._cleanup(i),i}_allocateTargets(){const e=3*Math.max(this._cubeSize,112),t=4*this._cubeSize,i={magFilter:tn,minFilter:tn,generateMipmaps:!1,type:$i,format:Zt,colorSpace:Ci,depthBuffer:!1},r=Bo(e,t,i);if(this._pingPongRenderTarget===null||this._pingPongRenderTarget.width!==e||this._pingPongRenderTarget.height!==t){this._pingPongRenderTarget!==null&&this._dispose(),this._pingPongRenderTarget=Bo(e,t,i);const{_lodMax:a}=this;({sizeLods:this._sizeLods,lodPlanes:this._lodPlanes,sigmas:this._sigmas}=Cf(a)),this._blurMaterial=Pf(a,e,t)}return r}_compileMaterial(e){const t=new We(this._lodPlanes[0],e);this._renderer.compile(t,Sa)}_sceneToCubeUV(e,t,i,r,a){const c=new Ht(90,1,t,i),l=[1,-1,1,1,1,1],d=[1,1,1,-1,-1,-1],h=this._renderer,f=h.autoClear,m=h.toneMapping;h.getClearColor(ko),h.toneMapping=Dn,h.autoClear=!1;const g=new Ui({name:"PMREM.Background",side:Lt,depthWrite:!1,depthTest:!1}),_=new We(new gn,g);let p=!1;const u=e.background;u?u.isColor&&(g.color.copy(u),e.background=null,p=!0):(g.color.copy(ko),p=!0);for(let b=0;b<6;b++){const S=b%3;S===0?(c.up.set(0,l[b],0),c.position.set(a.x,a.y,a.z),c.lookAt(a.x+d[b],a.y,a.z)):S===1?(c.up.set(0,0,l[b]),c.position.set(a.x,a.y,a.z),c.lookAt(a.x,a.y+d[b],a.z)):(c.up.set(0,l[b],0),c.position.set(a.x,a.y,a.z),c.lookAt(a.x,a.y,a.z+d[b]));const M=this._cubeSize;Tr(r,S*M,b>2?M:0,M,M),h.setRenderTarget(r),p&&h.render(_,c),h.render(e,c)}_.geometry.dispose(),_.material.dispose(),h.toneMapping=m,h.autoClear=f,e.background=u}_textureToCubeUV(e,t){const i=this._renderer,r=e.mapping===Ti||e.mapping===wi;r?(this._cubemapMaterial===null&&(this._cubemapMaterial=Vo()),this._cubemapMaterial.uniforms.flipEnvMap.value=e.isRenderTargetTexture===!1?-1:1):this._equirectMaterial===null&&(this._equirectMaterial=jo());const a=r?this._cubemapMaterial:this._equirectMaterial,s=new We(this._lodPlanes[0],a),o=a.uniforms;o.envMap.value=e;const c=this._cubeSize;Tr(t,0,0,3*c,2*c),i.setRenderTarget(t),i.render(s,Sa)}_applyPMREM(e){const t=this._renderer,i=t.autoClear;t.autoClear=!1;const r=this._lodPlanes.length;for(let a=1;a<r;a++){const s=Math.sqrt(this._sigmas[a]*this._sigmas[a]-this._sigmas[a-1]*this._sigmas[a-1]),o=Fo[(r-a-1)%Fo.length];this._blur(e,a-1,a,s,o)}t.autoClear=i}_blur(e,t,i,r,a){const s=this._pingPongRenderTarget;this._halfBlur(e,s,t,i,r,"latitudinal",a),this._halfBlur(s,e,i,i,r,"longitudinal",a)}_halfBlur(e,t,i,r,a,s,o){const c=this._renderer,l=this._blurMaterial;s!=="latitudinal"&&s!=="longitudinal"&&console.error("blur direction must be either latitudinal or longitudinal!");const d=3,h=new We(this._lodPlanes[r],l),f=l.uniforms,m=this._sizeLods[i]-1,g=isFinite(a)?Math.PI/(2*m):2*Math.PI/(2*qn-1),_=a/g,p=isFinite(a)?1+Math.floor(d*_):qn;p>qn&&console.warn(`sigmaRadians, ${a}, is too large and will clip, as it requested ${p} samples when the maximum is set to ${qn}`);const u=[];let b=0;for(let A=0;A<qn;++A){const L=A/_,x=Math.exp(-L*L/2);u.push(x),A===0?b+=x:A<p&&(b+=2*x)}for(let A=0;A<u.length;A++)u[A]=u[A]/b;f.envMap.value=e.texture,f.samples.value=p,f.weights.value=u,f.latitudinal.value=s==="latitudinal",o&&(f.poleAxis.value=o);const{_lodMax:S}=this;f.dTheta.value=g,f.mipInt.value=S-i;const M=this._sizeLods[r],w=3*M*(r>S-vi?r-S+vi:0),T=4*(this._cubeSize-M);Tr(t,w,T,3*M,2*M),c.setRenderTarget(t),c.render(h,Sa)}}function Cf(n){const e=[],t=[],i=[];let r=n;const a=n-vi+1+No.length;for(let s=0;s<a;s++){const o=Math.pow(2,r);t.push(o);let c=1/o;s>n-vi?c=No[s-n+vi-1]:s===0&&(c=0),i.push(c);const l=1/(o-2),d=-l,h=1+l,f=[d,d,h,d,h,h,d,d,h,h,d,h],m=6,g=6,_=3,p=2,u=1,b=new Float32Array(_*g*m),S=new Float32Array(p*g*m),M=new Float32Array(u*g*m);for(let T=0;T<m;T++){const A=T%3*2/3-1,L=T>2?0:-1,x=[A,L,0,A+2/3,L,0,A+2/3,L+1,0,A,L,0,A+2/3,L+1,0,A,L+1,0];b.set(x,_*g*T),S.set(f,p*g*T);const v=[T,T,T,T,T,T];M.set(v,u*g*T)}const w=new Ze;w.setAttribute("position",new nn(b,_)),w.setAttribute("uv",new nn(S,p)),w.setAttribute("faceIndex",new nn(M,u)),e.push(w),r>vi&&r--}return{lodPlanes:e,sizeLods:t,sigmas:i}}function Bo(n,e,t){const i=new ei(n,e,t);return i.texture.mapping=Vr,i.texture.name="PMREM.cubeUv",i.scissorTest=!0,i}function Tr(n,e,t,i,r){n.viewport.set(e,t,i,r),n.scissor.set(e,t,i,r)}function Pf(n,e,t){const i=new Float32Array(qn),r=new F(0,1,0);return new In({name:"SphericalGaussianBlur",defines:{n:qn,CUBEUV_TEXEL_WIDTH:1/e,CUBEUV_TEXEL_HEIGHT:1/t,CUBEUV_MAX_MIP:`${n}.0`},uniforms:{envMap:{value:null},samples:{value:1},weights:{value:i},latitudinal:{value:!1},dTheta:{value:0},mipInt:{value:0},poleAxis:{value:r}},vertexShader:Vs(),fragmentShader:`

			precision mediump float;
			precision mediump int;

			varying vec3 vOutputDirection;

			uniform sampler2D envMap;
			uniform int samples;
			uniform float weights[ n ];
			uniform bool latitudinal;
			uniform float dTheta;
			uniform float mipInt;
			uniform vec3 poleAxis;

			#define ENVMAP_TYPE_CUBE_UV
			#include <cube_uv_reflection_fragment>

			vec3 getSample( float theta, vec3 axis ) {

				float cosTheta = cos( theta );
				// Rodrigues' axis-angle rotation
				vec3 sampleDirection = vOutputDirection * cosTheta
					+ cross( axis, vOutputDirection ) * sin( theta )
					+ axis * dot( axis, vOutputDirection ) * ( 1.0 - cosTheta );

				return bilinearCubeUV( envMap, sampleDirection, mipInt );

			}

			void main() {

				vec3 axis = latitudinal ? poleAxis : cross( poleAxis, vOutputDirection );

				if ( all( equal( axis, vec3( 0.0 ) ) ) ) {

					axis = vec3( vOutputDirection.z, 0.0, - vOutputDirection.x );

				}

				axis = normalize( axis );

				gl_FragColor = vec4( 0.0, 0.0, 0.0, 1.0 );
				gl_FragColor.rgb += weights[ 0 ] * getSample( 0.0, axis );

				for ( int i = 1; i < n; i++ ) {

					if ( i >= samples ) {

						break;

					}

					float theta = dTheta * float( i );
					gl_FragColor.rgb += weights[ i ] * getSample( -1.0 * theta, axis );
					gl_FragColor.rgb += weights[ i ] * getSample( theta, axis );

				}

			}
		`,blending:Pn,depthTest:!1,depthWrite:!1})}function jo(){return new In({name:"EquirectangularToCubeUV",uniforms:{envMap:{value:null}},vertexShader:Vs(),fragmentShader:`

			precision mediump float;
			precision mediump int;

			varying vec3 vOutputDirection;

			uniform sampler2D envMap;

			#include <common>

			void main() {

				vec3 outputDirection = normalize( vOutputDirection );
				vec2 uv = equirectUv( outputDirection );

				gl_FragColor = vec4( texture2D ( envMap, uv ).rgb, 1.0 );

			}
		`,blending:Pn,depthTest:!1,depthWrite:!1})}function Vo(){return new In({name:"CubemapToCubeUV",uniforms:{envMap:{value:null},flipEnvMap:{value:-1}},vertexShader:Vs(),fragmentShader:`

			precision mediump float;
			precision mediump int;

			uniform float flipEnvMap;

			varying vec3 vOutputDirection;

			uniform samplerCube envMap;

			void main() {

				gl_FragColor = textureCube( envMap, vec3( flipEnvMap * vOutputDirection.x, vOutputDirection.yz ) );

			}
		`,blending:Pn,depthTest:!1,depthWrite:!1})}function Vs(){return`

		precision mediump float;
		precision mediump int;

		attribute float faceIndex;

		varying vec3 vOutputDirection;

		// RH coordinate system; PMREM face-indexing convention
		vec3 getDirection( vec2 uv, float face ) {

			uv = 2.0 * uv - 1.0;

			vec3 direction = vec3( uv, 1.0 );

			if ( face == 0.0 ) {

				direction = direction.zyx; // ( 1, v, u ) pos x

			} else if ( face == 1.0 ) {

				direction = direction.xzy;
				direction.xz *= -1.0; // ( -u, 1, -v ) pos y

			} else if ( face == 2.0 ) {

				direction.x *= -1.0; // ( -u, v, 1 ) pos z

			} else if ( face == 3.0 ) {

				direction = direction.zyx;
				direction.xz *= -1.0; // ( -1, v, -u ) neg x

			} else if ( face == 4.0 ) {

				direction = direction.xzy;
				direction.xy *= -1.0; // ( -u, -1, v ) neg y

			} else if ( face == 5.0 ) {

				direction.z *= -1.0; // ( u, v, -1 ) neg z

			}

			return direction;

		}

		void main() {

			vOutputDirection = getDirection( uv, faceIndex );
			gl_Position = vec4( position, 1.0 );

		}
	`}function Df(n){let e=new WeakMap,t=null;function i(o){if(o&&o.isTexture){const c=o.mapping,l=c===Va||c===Ha,d=c===Ti||c===wi;if(l||d){let h=e.get(o);const f=h!==void 0?h.texture.pmremVersion:0;if(o.isRenderTargetTexture&&o.pmremVersion!==f)return t===null&&(t=new Oo(n)),h=l?t.fromEquirectangular(o,h):t.fromCubemap(o,h),h.texture.pmremVersion=o.pmremVersion,e.set(o,h),h.texture;if(h!==void 0)return h.texture;{const m=o.image;return l&&m&&m.height>0||d&&m&&r(m)?(t===null&&(t=new Oo(n)),h=l?t.fromEquirectangular(o):t.fromCubemap(o),h.texture.pmremVersion=o.pmremVersion,e.set(o,h),o.addEventListener("dispose",a),h.texture):null}}}return o}function r(o){let c=0;const l=6;for(let d=0;d<l;d++)o[d]!==void 0&&c++;return c===l}function a(o){const c=o.target;c.removeEventListener("dispose",a);const l=e.get(c);l!==void 0&&(e.delete(c),l.dispose())}function s(){e=new WeakMap,t!==null&&(t.dispose(),t=null)}return{get:i,dispose:s}}function Lf(n){const e={};function t(i){if(e[i]!==void 0)return e[i];let r;switch(i){case"WEBGL_depth_texture":r=n.getExtension("WEBGL_depth_texture")||n.getExtension("MOZ_WEBGL_depth_texture")||n.getExtension("WEBKIT_WEBGL_depth_texture");break;case"EXT_texture_filter_anisotropic":r=n.getExtension("EXT_texture_filter_anisotropic")||n.getExtension("MOZ_EXT_texture_filter_anisotropic")||n.getExtension("WEBKIT_EXT_texture_filter_anisotropic");break;case"WEBGL_compressed_texture_s3tc":r=n.getExtension("WEBGL_compressed_texture_s3tc")||n.getExtension("MOZ_WEBGL_compressed_texture_s3tc")||n.getExtension("WEBKIT_WEBGL_compressed_texture_s3tc");break;case"WEBGL_compressed_texture_pvrtc":r=n.getExtension("WEBGL_compressed_texture_pvrtc")||n.getExtension("WEBKIT_WEBGL_compressed_texture_pvrtc");break;default:r=n.getExtension(i)}return e[i]=r,r}return{has:function(i){return t(i)!==null},init:function(){t("EXT_color_buffer_float"),t("WEBGL_clip_cull_distance"),t("OES_texture_float_linear"),t("EXT_color_buffer_half_float"),t("WEBGL_multisampled_render_to_texture"),t("WEBGL_render_shared_exponent")},get:function(i){const r=t(i);return r===null&&Vn("THREE.WebGLRenderer: "+i+" extension not supported."),r}}}function If(n,e,t,i){const r={},a=new WeakMap;function s(h){const f=h.target;f.index!==null&&e.remove(f.index);for(const g in f.attributes)e.remove(f.attributes[g]);f.removeEventListener("dispose",s),delete r[f.id];const m=a.get(f);m&&(e.remove(m),a.delete(f)),i.releaseStatesOfGeometry(f),f.isInstancedBufferGeometry===!0&&delete f._maxInstanceCount,t.memory.geometries--}function o(h,f){return r[f.id]===!0||(f.addEventListener("dispose",s),r[f.id]=!0,t.memory.geometries++),f}function c(h){const f=h.attributes;for(const m in f)e.update(f[m],n.ARRAY_BUFFER)}function l(h){const f=[],m=h.index,g=h.attributes.position;let _=0;if(m!==null){const b=m.array;_=m.version;for(let S=0,M=b.length;S<M;S+=3){const w=b[S+0],T=b[S+1],A=b[S+2];f.push(w,T,T,A,A,w)}}else if(g!==void 0){const b=g.array;_=g.version;for(let S=0,M=b.length/3-1;S<M;S+=3){const w=S+0,T=S+1,A=S+2;f.push(w,T,T,A,A,w)}}else return;const p=new(Lc(f)?Nc:zc)(f,1);p.version=_;const u=a.get(h);u&&e.remove(u),a.set(h,p)}function d(h){const f=a.get(h);if(f){const m=h.index;m!==null&&f.version<m.version&&l(h)}else l(h);return a.get(h)}return{get:o,update:c,getWireframeAttribute:d}}function Uf(n,e,t){let i;function r(f){i=f}let a,s;function o(f){a=f.type,s=f.bytesPerElement}function c(f,m){n.drawElements(i,m,a,f*s),t.update(m,i,1)}function l(f,m,g){g!==0&&(n.drawElementsInstanced(i,m,a,f*s,g),t.update(m,i,g))}function d(f,m,g){if(g===0)return;e.get("WEBGL_multi_draw").multiDrawElementsWEBGL(i,m,0,a,f,0,g);let p=0;for(let u=0;u<g;u++)p+=m[u];t.update(p,i,1)}function h(f,m,g,_){if(g===0)return;const p=e.get("WEBGL_multi_draw");if(p===null)for(let u=0;u<f.length;u++)l(f[u]/s,m[u],_[u]);else{p.multiDrawElementsInstancedWEBGL(i,m,0,a,f,0,_,0,g);let u=0;for(let b=0;b<g;b++)u+=m[b]*_[b];t.update(u,i,1)}}this.setMode=r,this.setIndex=o,this.render=c,this.renderInstances=l,this.renderMultiDraw=d,this.renderMultiDrawInstances=h}function zf(n){const e={geometries:0,textures:0},t={frame:0,calls:0,triangles:0,points:0,lines:0};function i(a,s,o){switch(t.calls++,s){case n.TRIANGLES:t.triangles+=o*(a/3);break;case n.LINES:t.lines+=o*(a/2);break;case n.LINE_STRIP:t.lines+=o*(a-1);break;case n.LINE_LOOP:t.lines+=o*a;break;case n.POINTS:t.points+=o*a;break;default:console.error("THREE.WebGLInfo: Unknown draw mode:",s);break}}function r(){t.calls=0,t.triangles=0,t.points=0,t.lines=0}return{memory:e,render:t,programs:null,autoReset:!0,reset:r,update:i}}function Nf(n,e,t){const i=new WeakMap,r=new dt;function a(s,o,c){const l=s.morphTargetInfluences,d=o.morphAttributes.position||o.morphAttributes.normal||o.morphAttributes.color,h=d!==void 0?d.length:0;let f=i.get(o);if(f===void 0||f.count!==h){let x=function(){A.dispose(),i.delete(o),o.removeEventListener("dispose",x)};f!==void 0&&f.texture.dispose();const m=o.morphAttributes.position!==void 0,g=o.morphAttributes.normal!==void 0,_=o.morphAttributes.color!==void 0,p=o.morphAttributes.position||[],u=o.morphAttributes.normal||[],b=o.morphAttributes.color||[];let S=0;m===!0&&(S=1),g===!0&&(S=2),_===!0&&(S=3);let M=o.attributes.position.count*S,w=1;M>e.maxTextureSize&&(w=Math.ceil(M/e.maxTextureSize),M=e.maxTextureSize);const T=new Float32Array(M*w*4*h),A=new Ic(T,M,w,h);A.type=pn,A.needsUpdate=!0;const L=S*4;for(let v=0;v<h;v++){const R=p[v],U=u[v],C=b[v],D=M*w*4*v;for(let k=0;k<R.count;k++){const N=k*L;m===!0&&(r.fromBufferAttribute(R,k),T[D+N+0]=r.x,T[D+N+1]=r.y,T[D+N+2]=r.z,T[D+N+3]=0),g===!0&&(r.fromBufferAttribute(U,k),T[D+N+4]=r.x,T[D+N+5]=r.y,T[D+N+6]=r.z,T[D+N+7]=0),_===!0&&(r.fromBufferAttribute(C,k),T[D+N+8]=r.x,T[D+N+9]=r.y,T[D+N+10]=r.z,T[D+N+11]=C.itemSize===4?r.w:1)}}f={count:h,texture:A,size:new Ke(M,w)},i.set(o,f),o.addEventListener("dispose",x)}if(s.isInstancedMesh===!0&&s.morphTexture!==null)c.getUniforms().setValue(n,"morphTexture",s.morphTexture,t);else{let m=0;for(let _=0;_<l.length;_++)m+=l[_];const g=o.morphTargetsRelative?1:1-m;c.getUniforms().setValue(n,"morphTargetBaseInfluence",g),c.getUniforms().setValue(n,"morphTargetInfluences",l)}c.getUniforms().setValue(n,"morphTargetsTexture",f.texture,t),c.getUniforms().setValue(n,"morphTargetsTextureSize",f.size)}return{update:a}}function kf(n,e,t,i){let r=new WeakMap;function a(c){const l=i.render.frame,d=c.geometry,h=e.get(c,d);if(r.get(h)!==l&&(e.update(h),r.set(h,l)),c.isInstancedMesh&&(c.hasEventListener("dispose",o)===!1&&c.addEventListener("dispose",o),r.get(c)!==l&&(t.update(c.instanceMatrix,n.ARRAY_BUFFER),c.instanceColor!==null&&t.update(c.instanceColor,n.ARRAY_BUFFER),r.set(c,l))),c.isSkinnedMesh){const f=c.skeleton;r.get(f)!==l&&(f.update(),r.set(f,l))}return h}function s(){r=new WeakMap}function o(c){const l=c.target;l.removeEventListener("dispose",o),t.remove(l.instanceMatrix),l.instanceColor!==null&&t.remove(l.instanceColor)}return{update:a,dispose:s}}const Gc=new Ct,Ho=new Bc(1,1),Wc=new Ic,Xc=new uu,Kc=new Oc,Go=[],Wo=[],Xo=new Float32Array(16),Ko=new Float32Array(9),qo=new Float32Array(4);function Ni(n,e,t){const i=n[0];if(i<=0||i>0)return n;const r=e*t;let a=Go[r];if(a===void 0&&(a=new Float32Array(r),Go[r]=a),e!==0){i.toArray(a,0);for(let s=1,o=0;s!==e;++s)o+=t,n[s].toArray(a,o)}return a}function _t(n,e){if(n.length!==e.length)return!1;for(let t=0,i=n.length;t<i;t++)if(n[t]!==e[t])return!1;return!0}function vt(n,e){for(let t=0,i=e.length;t<i;t++)n[t]=e[t]}function Gr(n,e){let t=Wo[e];t===void 0&&(t=new Int32Array(e),Wo[e]=t);for(let i=0;i!==e;++i)t[i]=n.allocateTextureUnit();return t}function Ff(n,e){const t=this.cache;t[0]!==e&&(n.uniform1f(this.addr,e),t[0]=e)}function Of(n,e){const t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y)&&(n.uniform2f(this.addr,e.x,e.y),t[0]=e.x,t[1]=e.y);else{if(_t(t,e))return;n.uniform2fv(this.addr,e),vt(t,e)}}function Bf(n,e){const t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y||t[2]!==e.z)&&(n.uniform3f(this.addr,e.x,e.y,e.z),t[0]=e.x,t[1]=e.y,t[2]=e.z);else if(e.r!==void 0)(t[0]!==e.r||t[1]!==e.g||t[2]!==e.b)&&(n.uniform3f(this.addr,e.r,e.g,e.b),t[0]=e.r,t[1]=e.g,t[2]=e.b);else{if(_t(t,e))return;n.uniform3fv(this.addr,e),vt(t,e)}}function jf(n,e){const t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y||t[2]!==e.z||t[3]!==e.w)&&(n.uniform4f(this.addr,e.x,e.y,e.z,e.w),t[0]=e.x,t[1]=e.y,t[2]=e.z,t[3]=e.w);else{if(_t(t,e))return;n.uniform4fv(this.addr,e),vt(t,e)}}function Vf(n,e){const t=this.cache,i=e.elements;if(i===void 0){if(_t(t,e))return;n.uniformMatrix2fv(this.addr,!1,e),vt(t,e)}else{if(_t(t,i))return;qo.set(i),n.uniformMatrix2fv(this.addr,!1,qo),vt(t,i)}}function Hf(n,e){const t=this.cache,i=e.elements;if(i===void 0){if(_t(t,e))return;n.uniformMatrix3fv(this.addr,!1,e),vt(t,e)}else{if(_t(t,i))return;Ko.set(i),n.uniformMatrix3fv(this.addr,!1,Ko),vt(t,i)}}function Gf(n,e){const t=this.cache,i=e.elements;if(i===void 0){if(_t(t,e))return;n.uniformMatrix4fv(this.addr,!1,e),vt(t,e)}else{if(_t(t,i))return;Xo.set(i),n.uniformMatrix4fv(this.addr,!1,Xo),vt(t,i)}}function Wf(n,e){const t=this.cache;t[0]!==e&&(n.uniform1i(this.addr,e),t[0]=e)}function Xf(n,e){const t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y)&&(n.uniform2i(this.addr,e.x,e.y),t[0]=e.x,t[1]=e.y);else{if(_t(t,e))return;n.uniform2iv(this.addr,e),vt(t,e)}}function Kf(n,e){const t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y||t[2]!==e.z)&&(n.uniform3i(this.addr,e.x,e.y,e.z),t[0]=e.x,t[1]=e.y,t[2]=e.z);else{if(_t(t,e))return;n.uniform3iv(this.addr,e),vt(t,e)}}function qf(n,e){const t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y||t[2]!==e.z||t[3]!==e.w)&&(n.uniform4i(this.addr,e.x,e.y,e.z,e.w),t[0]=e.x,t[1]=e.y,t[2]=e.z,t[3]=e.w);else{if(_t(t,e))return;n.uniform4iv(this.addr,e),vt(t,e)}}function $f(n,e){const t=this.cache;t[0]!==e&&(n.uniform1ui(this.addr,e),t[0]=e)}function Yf(n,e){const t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y)&&(n.uniform2ui(this.addr,e.x,e.y),t[0]=e.x,t[1]=e.y);else{if(_t(t,e))return;n.uniform2uiv(this.addr,e),vt(t,e)}}function Zf(n,e){const t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y||t[2]!==e.z)&&(n.uniform3ui(this.addr,e.x,e.y,e.z),t[0]=e.x,t[1]=e.y,t[2]=e.z);else{if(_t(t,e))return;n.uniform3uiv(this.addr,e),vt(t,e)}}function Jf(n,e){const t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y||t[2]!==e.z||t[3]!==e.w)&&(n.uniform4ui(this.addr,e.x,e.y,e.z,e.w),t[0]=e.x,t[1]=e.y,t[2]=e.z,t[3]=e.w);else{if(_t(t,e))return;n.uniform4uiv(this.addr,e),vt(t,e)}}function Qf(n,e,t){const i=this.cache,r=t.allocateTextureUnit();i[0]!==r&&(n.uniform1i(this.addr,r),i[0]=r);let a;this.type===n.SAMPLER_2D_SHADOW?(Ho.compareFunction=Dc,a=Ho):a=Gc,t.setTexture2D(e||a,r)}function ep(n,e,t){const i=this.cache,r=t.allocateTextureUnit();i[0]!==r&&(n.uniform1i(this.addr,r),i[0]=r),t.setTexture3D(e||Xc,r)}function tp(n,e,t){const i=this.cache,r=t.allocateTextureUnit();i[0]!==r&&(n.uniform1i(this.addr,r),i[0]=r),t.setTextureCube(e||Kc,r)}function np(n,e,t){const i=this.cache,r=t.allocateTextureUnit();i[0]!==r&&(n.uniform1i(this.addr,r),i[0]=r),t.setTexture2DArray(e||Wc,r)}function ip(n){switch(n){case 5126:return Ff;case 35664:return Of;case 35665:return Bf;case 35666:return jf;case 35674:return Vf;case 35675:return Hf;case 35676:return Gf;case 5124:case 35670:return Wf;case 35667:case 35671:return Xf;case 35668:case 35672:return Kf;case 35669:case 35673:return qf;case 5125:return $f;case 36294:return Yf;case 36295:return Zf;case 36296:return Jf;case 35678:case 36198:case 36298:case 36306:case 35682:return Qf;case 35679:case 36299:case 36307:return ep;case 35680:case 36300:case 36308:case 36293:return tp;case 36289:case 36303:case 36311:case 36292:return np}}function rp(n,e){n.uniform1fv(this.addr,e)}function ap(n,e){const t=Ni(e,this.size,2);n.uniform2fv(this.addr,t)}function sp(n,e){const t=Ni(e,this.size,3);n.uniform3fv(this.addr,t)}function op(n,e){const t=Ni(e,this.size,4);n.uniform4fv(this.addr,t)}function cp(n,e){const t=Ni(e,this.size,4);n.uniformMatrix2fv(this.addr,!1,t)}function lp(n,e){const t=Ni(e,this.size,9);n.uniformMatrix3fv(this.addr,!1,t)}function up(n,e){const t=Ni(e,this.size,16);n.uniformMatrix4fv(this.addr,!1,t)}function dp(n,e){n.uniform1iv(this.addr,e)}function hp(n,e){n.uniform2iv(this.addr,e)}function fp(n,e){n.uniform3iv(this.addr,e)}function pp(n,e){n.uniform4iv(this.addr,e)}function mp(n,e){n.uniform1uiv(this.addr,e)}function gp(n,e){n.uniform2uiv(this.addr,e)}function _p(n,e){n.uniform3uiv(this.addr,e)}function vp(n,e){n.uniform4uiv(this.addr,e)}function xp(n,e,t){const i=this.cache,r=e.length,a=Gr(t,r);_t(i,a)||(n.uniform1iv(this.addr,a),vt(i,a));for(let s=0;s!==r;++s)t.setTexture2D(e[s]||Gc,a[s])}function Mp(n,e,t){const i=this.cache,r=e.length,a=Gr(t,r);_t(i,a)||(n.uniform1iv(this.addr,a),vt(i,a));for(let s=0;s!==r;++s)t.setTexture3D(e[s]||Xc,a[s])}function Sp(n,e,t){const i=this.cache,r=e.length,a=Gr(t,r);_t(i,a)||(n.uniform1iv(this.addr,a),vt(i,a));for(let s=0;s!==r;++s)t.setTextureCube(e[s]||Kc,a[s])}function Ep(n,e,t){const i=this.cache,r=e.length,a=Gr(t,r);_t(i,a)||(n.uniform1iv(this.addr,a),vt(i,a));for(let s=0;s!==r;++s)t.setTexture2DArray(e[s]||Wc,a[s])}function bp(n){switch(n){case 5126:return rp;case 35664:return ap;case 35665:return sp;case 35666:return op;case 35674:return cp;case 35675:return lp;case 35676:return up;case 5124:case 35670:return dp;case 35667:case 35671:return hp;case 35668:case 35672:return fp;case 35669:case 35673:return pp;case 5125:return mp;case 36294:return gp;case 36295:return _p;case 36296:return vp;case 35678:case 36198:case 36298:case 36306:case 35682:return xp;case 35679:case 36299:case 36307:return Mp;case 35680:case 36300:case 36308:case 36293:return Sp;case 36289:case 36303:case 36311:case 36292:return Ep}}class yp{constructor(e,t,i){this.id=e,this.addr=i,this.cache=[],this.type=t.type,this.setValue=ip(t.type)}}class Tp{constructor(e,t,i){this.id=e,this.addr=i,this.cache=[],this.type=t.type,this.size=t.size,this.setValue=bp(t.type)}}class wp{constructor(e){this.id=e,this.seq=[],this.map={}}setValue(e,t,i){const r=this.seq;for(let a=0,s=r.length;a!==s;++a){const o=r[a];o.setValue(e,t[o.id],i)}}}const wa=/(\w+)(\])?(\[|\.)?/g;function $o(n,e){n.seq.push(e),n.map[e.id]=e}function Ap(n,e,t){const i=n.name,r=i.length;for(wa.lastIndex=0;;){const a=wa.exec(i),s=wa.lastIndex;let o=a[1];const c=a[2]==="]",l=a[3];if(c&&(o=o|0),l===void 0||l==="["&&s+2===r){$o(t,l===void 0?new yp(o,n,e):new Tp(o,n,e));break}else{let h=t.map[o];h===void 0&&(h=new wp(o),$o(t,h)),t=h}}}class Ur{constructor(e,t){this.seq=[],this.map={};const i=e.getProgramParameter(t,e.ACTIVE_UNIFORMS);for(let r=0;r<i;++r){const a=e.getActiveUniform(t,r),s=e.getUniformLocation(t,a.name);Ap(a,s,this)}}setValue(e,t,i,r){const a=this.map[t];a!==void 0&&a.setValue(e,i,r)}setOptional(e,t,i){const r=t[i];r!==void 0&&this.setValue(e,i,r)}static upload(e,t,i,r){for(let a=0,s=t.length;a!==s;++a){const o=t[a],c=i[o.id];c.needsUpdate!==!1&&o.setValue(e,c.value,r)}}static seqWithValue(e,t){const i=[];for(let r=0,a=e.length;r!==a;++r){const s=e[r];s.id in t&&i.push(s)}return i}}function Yo(n,e,t){const i=n.createShader(e);return n.shaderSource(i,t),n.compileShader(i),i}const Rp=37297;let Cp=0;function Pp(n,e){const t=n.split(`
`),i=[],r=Math.max(e-6,0),a=Math.min(e+6,t.length);for(let s=r;s<a;s++){const o=s+1;i.push(`${o===e?">":" "} ${o}: ${t[s]}`)}return i.join(`
`)}const Zo=new Be;function Dp(n){Qe._getMatrix(Zo,Qe.workingColorSpace,n);const e=`mat3( ${Zo.elements.map(t=>t.toFixed(4))} )`;switch(Qe.getTransfer(n)){case Nr:return[e,"LinearTransferOETF"];case rt:return[e,"sRGBTransferOETF"];default:return console.warn("THREE.WebGLProgram: Unsupported color space: ",n),[e,"LinearTransferOETF"]}}function Jo(n,e,t){const i=n.getShaderParameter(e,n.COMPILE_STATUS),r=n.getShaderInfoLog(e).trim();if(i&&r==="")return"";const a=/ERROR: 0:(\d+)/.exec(r);if(a){const s=parseInt(a[1]);return t.toUpperCase()+`

`+r+`

`+Pp(n.getShaderSource(e),s)}else return r}function Lp(n,e){const t=Dp(e);return[`vec4 ${n}( vec4 value ) {`,`	return ${t[1]}( vec4( value.rgb * ${t[0]}, value.a ) );`,"}"].join(`
`)}function Ip(n,e){let t;switch(e){case Nl:t="Linear";break;case kl:t="Reinhard";break;case Fl:t="Cineon";break;case Ol:t="ACESFilmic";break;case jl:t="AgX";break;case Vl:t="Neutral";break;case Bl:t="Custom";break;default:console.warn("THREE.WebGLProgram: Unsupported toneMapping:",e),t="Linear"}return"vec3 "+n+"( vec3 color ) { return "+t+"ToneMapping( color ); }"}const wr=new F;function Up(){Qe.getLuminanceCoefficients(wr);const n=wr.x.toFixed(4),e=wr.y.toFixed(4),t=wr.z.toFixed(4);return["float luminance( const in vec3 rgb ) {",`	const vec3 weights = vec3( ${n}, ${e}, ${t} );`,"	return dot( weights, rgb );","}"].join(`
`)}function zp(n){return[n.extensionClipCullDistance?"#extension GL_ANGLE_clip_cull_distance : require":"",n.extensionMultiDraw?"#extension GL_ANGLE_multi_draw : require":""].filter(Gi).join(`
`)}function Np(n){const e=[];for(const t in n){const i=n[t];i!==!1&&e.push("#define "+t+" "+i)}return e.join(`
`)}function kp(n,e){const t={},i=n.getProgramParameter(e,n.ACTIVE_ATTRIBUTES);for(let r=0;r<i;r++){const a=n.getActiveAttrib(e,r),s=a.name;let o=1;a.type===n.FLOAT_MAT2&&(o=2),a.type===n.FLOAT_MAT3&&(o=3),a.type===n.FLOAT_MAT4&&(o=4),t[s]={type:a.type,location:n.getAttribLocation(e,s),locationSize:o}}return t}function Gi(n){return n!==""}function Qo(n,e){const t=e.numSpotLightShadows+e.numSpotLightMaps-e.numSpotLightShadowsWithMaps;return n.replace(/NUM_DIR_LIGHTS/g,e.numDirLights).replace(/NUM_SPOT_LIGHTS/g,e.numSpotLights).replace(/NUM_SPOT_LIGHT_MAPS/g,e.numSpotLightMaps).replace(/NUM_SPOT_LIGHT_COORDS/g,t).replace(/NUM_RECT_AREA_LIGHTS/g,e.numRectAreaLights).replace(/NUM_POINT_LIGHTS/g,e.numPointLights).replace(/NUM_HEMI_LIGHTS/g,e.numHemiLights).replace(/NUM_DIR_LIGHT_SHADOWS/g,e.numDirLightShadows).replace(/NUM_SPOT_LIGHT_SHADOWS_WITH_MAPS/g,e.numSpotLightShadowsWithMaps).replace(/NUM_SPOT_LIGHT_SHADOWS/g,e.numSpotLightShadows).replace(/NUM_POINT_LIGHT_SHADOWS/g,e.numPointLightShadows)}function ec(n,e){return n.replace(/NUM_CLIPPING_PLANES/g,e.numClippingPlanes).replace(/UNION_CLIPPING_PLANES/g,e.numClippingPlanes-e.numClipIntersection)}const Fp=/^[ \t]*#include +<([\w\d./]+)>/gm;function Ms(n){return n.replace(Fp,Bp)}const Op=new Map;function Bp(n,e){let t=Ve[e];if(t===void 0){const i=Op.get(e);if(i!==void 0)t=Ve[i],console.warn('THREE.WebGLRenderer: Shader chunk "%s" has been deprecated. Use "%s" instead.',e,i);else throw new Error("Can not resolve #include <"+e+">")}return Ms(t)}const jp=/#pragma unroll_loop_start\s+for\s*\(\s*int\s+i\s*=\s*(\d+)\s*;\s*i\s*<\s*(\d+)\s*;\s*i\s*\+\+\s*\)\s*{([\s\S]+?)}\s+#pragma unroll_loop_end/g;function tc(n){return n.replace(jp,Vp)}function Vp(n,e,t,i){let r="";for(let a=parseInt(e);a<parseInt(t);a++)r+=i.replace(/\[\s*i\s*\]/g,"[ "+a+" ]").replace(/UNROLLED_LOOP_INDEX/g,a);return r}function nc(n){let e=`precision ${n.precision} float;
	precision ${n.precision} int;
	precision ${n.precision} sampler2D;
	precision ${n.precision} samplerCube;
	precision ${n.precision} sampler3D;
	precision ${n.precision} sampler2DArray;
	precision ${n.precision} sampler2DShadow;
	precision ${n.precision} samplerCubeShadow;
	precision ${n.precision} sampler2DArrayShadow;
	precision ${n.precision} isampler2D;
	precision ${n.precision} isampler3D;
	precision ${n.precision} isamplerCube;
	precision ${n.precision} isampler2DArray;
	precision ${n.precision} usampler2D;
	precision ${n.precision} usampler3D;
	precision ${n.precision} usamplerCube;
	precision ${n.precision} usampler2DArray;
	`;return n.precision==="highp"?e+=`
#define HIGH_PRECISION`:n.precision==="mediump"?e+=`
#define MEDIUM_PRECISION`:n.precision==="lowp"&&(e+=`
#define LOW_PRECISION`),e}function Hp(n){let e="SHADOWMAP_TYPE_BASIC";return n.shadowMapType===_c?e="SHADOWMAP_TYPE_PCF":n.shadowMapType===ml?e="SHADOWMAP_TYPE_PCF_SOFT":n.shadowMapType===hn&&(e="SHADOWMAP_TYPE_VSM"),e}function Gp(n){let e="ENVMAP_TYPE_CUBE";if(n.envMap)switch(n.envMapMode){case Ti:case wi:e="ENVMAP_TYPE_CUBE";break;case Vr:e="ENVMAP_TYPE_CUBE_UV";break}return e}function Wp(n){let e="ENVMAP_MODE_REFLECTION";if(n.envMap)switch(n.envMapMode){case wi:e="ENVMAP_MODE_REFRACTION";break}return e}function Xp(n){let e="ENVMAP_BLENDING_NONE";if(n.envMap)switch(n.combine){case vc:e="ENVMAP_BLENDING_MULTIPLY";break;case Ul:e="ENVMAP_BLENDING_MIX";break;case zl:e="ENVMAP_BLENDING_ADD";break}return e}function Kp(n){const e=n.envMapCubeUVHeight;if(e===null)return null;const t=Math.log2(e)-2,i=1/e;return{texelWidth:1/(3*Math.max(Math.pow(2,t),112)),texelHeight:i,maxMip:t}}function qp(n,e,t,i){const r=n.getContext(),a=t.defines;let s=t.vertexShader,o=t.fragmentShader;const c=Hp(t),l=Gp(t),d=Wp(t),h=Xp(t),f=Kp(t),m=zp(t),g=Np(a),_=r.createProgram();let p,u,b=t.glslVersion?"#version "+t.glslVersion+`
`:"";t.isRawShaderMaterial?(p=["#define SHADER_TYPE "+t.shaderType,"#define SHADER_NAME "+t.shaderName,g].filter(Gi).join(`
`),p.length>0&&(p+=`
`),u=["#define SHADER_TYPE "+t.shaderType,"#define SHADER_NAME "+t.shaderName,g].filter(Gi).join(`
`),u.length>0&&(u+=`
`)):(p=[nc(t),"#define SHADER_TYPE "+t.shaderType,"#define SHADER_NAME "+t.shaderName,g,t.extensionClipCullDistance?"#define USE_CLIP_DISTANCE":"",t.batching?"#define USE_BATCHING":"",t.batchingColor?"#define USE_BATCHING_COLOR":"",t.instancing?"#define USE_INSTANCING":"",t.instancingColor?"#define USE_INSTANCING_COLOR":"",t.instancingMorph?"#define USE_INSTANCING_MORPH":"",t.useFog&&t.fog?"#define USE_FOG":"",t.useFog&&t.fogExp2?"#define FOG_EXP2":"",t.map?"#define USE_MAP":"",t.envMap?"#define USE_ENVMAP":"",t.envMap?"#define "+d:"",t.lightMap?"#define USE_LIGHTMAP":"",t.aoMap?"#define USE_AOMAP":"",t.bumpMap?"#define USE_BUMPMAP":"",t.normalMap?"#define USE_NORMALMAP":"",t.normalMapObjectSpace?"#define USE_NORMALMAP_OBJECTSPACE":"",t.normalMapTangentSpace?"#define USE_NORMALMAP_TANGENTSPACE":"",t.displacementMap?"#define USE_DISPLACEMENTMAP":"",t.emissiveMap?"#define USE_EMISSIVEMAP":"",t.anisotropy?"#define USE_ANISOTROPY":"",t.anisotropyMap?"#define USE_ANISOTROPYMAP":"",t.clearcoatMap?"#define USE_CLEARCOATMAP":"",t.clearcoatRoughnessMap?"#define USE_CLEARCOAT_ROUGHNESSMAP":"",t.clearcoatNormalMap?"#define USE_CLEARCOAT_NORMALMAP":"",t.iridescenceMap?"#define USE_IRIDESCENCEMAP":"",t.iridescenceThicknessMap?"#define USE_IRIDESCENCE_THICKNESSMAP":"",t.specularMap?"#define USE_SPECULARMAP":"",t.specularColorMap?"#define USE_SPECULAR_COLORMAP":"",t.specularIntensityMap?"#define USE_SPECULAR_INTENSITYMAP":"",t.roughnessMap?"#define USE_ROUGHNESSMAP":"",t.metalnessMap?"#define USE_METALNESSMAP":"",t.alphaMap?"#define USE_ALPHAMAP":"",t.alphaHash?"#define USE_ALPHAHASH":"",t.transmission?"#define USE_TRANSMISSION":"",t.transmissionMap?"#define USE_TRANSMISSIONMAP":"",t.thicknessMap?"#define USE_THICKNESSMAP":"",t.sheenColorMap?"#define USE_SHEEN_COLORMAP":"",t.sheenRoughnessMap?"#define USE_SHEEN_ROUGHNESSMAP":"",t.mapUv?"#define MAP_UV "+t.mapUv:"",t.alphaMapUv?"#define ALPHAMAP_UV "+t.alphaMapUv:"",t.lightMapUv?"#define LIGHTMAP_UV "+t.lightMapUv:"",t.aoMapUv?"#define AOMAP_UV "+t.aoMapUv:"",t.emissiveMapUv?"#define EMISSIVEMAP_UV "+t.emissiveMapUv:"",t.bumpMapUv?"#define BUMPMAP_UV "+t.bumpMapUv:"",t.normalMapUv?"#define NORMALMAP_UV "+t.normalMapUv:"",t.displacementMapUv?"#define DISPLACEMENTMAP_UV "+t.displacementMapUv:"",t.metalnessMapUv?"#define METALNESSMAP_UV "+t.metalnessMapUv:"",t.roughnessMapUv?"#define ROUGHNESSMAP_UV "+t.roughnessMapUv:"",t.anisotropyMapUv?"#define ANISOTROPYMAP_UV "+t.anisotropyMapUv:"",t.clearcoatMapUv?"#define CLEARCOATMAP_UV "+t.clearcoatMapUv:"",t.clearcoatNormalMapUv?"#define CLEARCOAT_NORMALMAP_UV "+t.clearcoatNormalMapUv:"",t.clearcoatRoughnessMapUv?"#define CLEARCOAT_ROUGHNESSMAP_UV "+t.clearcoatRoughnessMapUv:"",t.iridescenceMapUv?"#define IRIDESCENCEMAP_UV "+t.iridescenceMapUv:"",t.iridescenceThicknessMapUv?"#define IRIDESCENCE_THICKNESSMAP_UV "+t.iridescenceThicknessMapUv:"",t.sheenColorMapUv?"#define SHEEN_COLORMAP_UV "+t.sheenColorMapUv:"",t.sheenRoughnessMapUv?"#define SHEEN_ROUGHNESSMAP_UV "+t.sheenRoughnessMapUv:"",t.specularMapUv?"#define SPECULARMAP_UV "+t.specularMapUv:"",t.specularColorMapUv?"#define SPECULAR_COLORMAP_UV "+t.specularColorMapUv:"",t.specularIntensityMapUv?"#define SPECULAR_INTENSITYMAP_UV "+t.specularIntensityMapUv:"",t.transmissionMapUv?"#define TRANSMISSIONMAP_UV "+t.transmissionMapUv:"",t.thicknessMapUv?"#define THICKNESSMAP_UV "+t.thicknessMapUv:"",t.vertexTangents&&t.flatShading===!1?"#define USE_TANGENT":"",t.vertexColors?"#define USE_COLOR":"",t.vertexAlphas?"#define USE_COLOR_ALPHA":"",t.vertexUv1s?"#define USE_UV1":"",t.vertexUv2s?"#define USE_UV2":"",t.vertexUv3s?"#define USE_UV3":"",t.pointsUvs?"#define USE_POINTS_UV":"",t.flatShading?"#define FLAT_SHADED":"",t.skinning?"#define USE_SKINNING":"",t.morphTargets?"#define USE_MORPHTARGETS":"",t.morphNormals&&t.flatShading===!1?"#define USE_MORPHNORMALS":"",t.morphColors?"#define USE_MORPHCOLORS":"",t.morphTargetsCount>0?"#define MORPHTARGETS_TEXTURE_STRIDE "+t.morphTextureStride:"",t.morphTargetsCount>0?"#define MORPHTARGETS_COUNT "+t.morphTargetsCount:"",t.doubleSided?"#define DOUBLE_SIDED":"",t.flipSided?"#define FLIP_SIDED":"",t.shadowMapEnabled?"#define USE_SHADOWMAP":"",t.shadowMapEnabled?"#define "+c:"",t.sizeAttenuation?"#define USE_SIZEATTENUATION":"",t.numLightProbes>0?"#define USE_LIGHT_PROBES":"",t.logarithmicDepthBuffer?"#define USE_LOGDEPTHBUF":"",t.reverseDepthBuffer?"#define USE_REVERSEDEPTHBUF":"","uniform mat4 modelMatrix;","uniform mat4 modelViewMatrix;","uniform mat4 projectionMatrix;","uniform mat4 viewMatrix;","uniform mat3 normalMatrix;","uniform vec3 cameraPosition;","uniform bool isOrthographic;","#ifdef USE_INSTANCING","	attribute mat4 instanceMatrix;","#endif","#ifdef USE_INSTANCING_COLOR","	attribute vec3 instanceColor;","#endif","#ifdef USE_INSTANCING_MORPH","	uniform sampler2D morphTexture;","#endif","attribute vec3 position;","attribute vec3 normal;","attribute vec2 uv;","#ifdef USE_UV1","	attribute vec2 uv1;","#endif","#ifdef USE_UV2","	attribute vec2 uv2;","#endif","#ifdef USE_UV3","	attribute vec2 uv3;","#endif","#ifdef USE_TANGENT","	attribute vec4 tangent;","#endif","#if defined( USE_COLOR_ALPHA )","	attribute vec4 color;","#elif defined( USE_COLOR )","	attribute vec3 color;","#endif","#ifdef USE_SKINNING","	attribute vec4 skinIndex;","	attribute vec4 skinWeight;","#endif",`
`].filter(Gi).join(`
`),u=[nc(t),"#define SHADER_TYPE "+t.shaderType,"#define SHADER_NAME "+t.shaderName,g,t.useFog&&t.fog?"#define USE_FOG":"",t.useFog&&t.fogExp2?"#define FOG_EXP2":"",t.alphaToCoverage?"#define ALPHA_TO_COVERAGE":"",t.map?"#define USE_MAP":"",t.matcap?"#define USE_MATCAP":"",t.envMap?"#define USE_ENVMAP":"",t.envMap?"#define "+l:"",t.envMap?"#define "+d:"",t.envMap?"#define "+h:"",f?"#define CUBEUV_TEXEL_WIDTH "+f.texelWidth:"",f?"#define CUBEUV_TEXEL_HEIGHT "+f.texelHeight:"",f?"#define CUBEUV_MAX_MIP "+f.maxMip+".0":"",t.lightMap?"#define USE_LIGHTMAP":"",t.aoMap?"#define USE_AOMAP":"",t.bumpMap?"#define USE_BUMPMAP":"",t.normalMap?"#define USE_NORMALMAP":"",t.normalMapObjectSpace?"#define USE_NORMALMAP_OBJECTSPACE":"",t.normalMapTangentSpace?"#define USE_NORMALMAP_TANGENTSPACE":"",t.emissiveMap?"#define USE_EMISSIVEMAP":"",t.anisotropy?"#define USE_ANISOTROPY":"",t.anisotropyMap?"#define USE_ANISOTROPYMAP":"",t.clearcoat?"#define USE_CLEARCOAT":"",t.clearcoatMap?"#define USE_CLEARCOATMAP":"",t.clearcoatRoughnessMap?"#define USE_CLEARCOAT_ROUGHNESSMAP":"",t.clearcoatNormalMap?"#define USE_CLEARCOAT_NORMALMAP":"",t.dispersion?"#define USE_DISPERSION":"",t.iridescence?"#define USE_IRIDESCENCE":"",t.iridescenceMap?"#define USE_IRIDESCENCEMAP":"",t.iridescenceThicknessMap?"#define USE_IRIDESCENCE_THICKNESSMAP":"",t.specularMap?"#define USE_SPECULARMAP":"",t.specularColorMap?"#define USE_SPECULAR_COLORMAP":"",t.specularIntensityMap?"#define USE_SPECULAR_INTENSITYMAP":"",t.roughnessMap?"#define USE_ROUGHNESSMAP":"",t.metalnessMap?"#define USE_METALNESSMAP":"",t.alphaMap?"#define USE_ALPHAMAP":"",t.alphaTest?"#define USE_ALPHATEST":"",t.alphaHash?"#define USE_ALPHAHASH":"",t.sheen?"#define USE_SHEEN":"",t.sheenColorMap?"#define USE_SHEEN_COLORMAP":"",t.sheenRoughnessMap?"#define USE_SHEEN_ROUGHNESSMAP":"",t.transmission?"#define USE_TRANSMISSION":"",t.transmissionMap?"#define USE_TRANSMISSIONMAP":"",t.thicknessMap?"#define USE_THICKNESSMAP":"",t.vertexTangents&&t.flatShading===!1?"#define USE_TANGENT":"",t.vertexColors||t.instancingColor||t.batchingColor?"#define USE_COLOR":"",t.vertexAlphas?"#define USE_COLOR_ALPHA":"",t.vertexUv1s?"#define USE_UV1":"",t.vertexUv2s?"#define USE_UV2":"",t.vertexUv3s?"#define USE_UV3":"",t.pointsUvs?"#define USE_POINTS_UV":"",t.gradientMap?"#define USE_GRADIENTMAP":"",t.flatShading?"#define FLAT_SHADED":"",t.doubleSided?"#define DOUBLE_SIDED":"",t.flipSided?"#define FLIP_SIDED":"",t.shadowMapEnabled?"#define USE_SHADOWMAP":"",t.shadowMapEnabled?"#define "+c:"",t.premultipliedAlpha?"#define PREMULTIPLIED_ALPHA":"",t.numLightProbes>0?"#define USE_LIGHT_PROBES":"",t.decodeVideoTexture?"#define DECODE_VIDEO_TEXTURE":"",t.decodeVideoTextureEmissive?"#define DECODE_VIDEO_TEXTURE_EMISSIVE":"",t.logarithmicDepthBuffer?"#define USE_LOGDEPTHBUF":"",t.reverseDepthBuffer?"#define USE_REVERSEDEPTHBUF":"","uniform mat4 viewMatrix;","uniform vec3 cameraPosition;","uniform bool isOrthographic;",t.toneMapping!==Dn?"#define TONE_MAPPING":"",t.toneMapping!==Dn?Ve.tonemapping_pars_fragment:"",t.toneMapping!==Dn?Ip("toneMapping",t.toneMapping):"",t.dithering?"#define DITHERING":"",t.opaque?"#define OPAQUE":"",Ve.colorspace_pars_fragment,Lp("linearToOutputTexel",t.outputColorSpace),Up(),t.useDepthPacking?"#define DEPTH_PACKING "+t.depthPacking:"",`
`].filter(Gi).join(`
`)),s=Ms(s),s=Qo(s,t),s=ec(s,t),o=Ms(o),o=Qo(o,t),o=ec(o,t),s=tc(s),o=tc(o),t.isRawShaderMaterial!==!0&&(b=`#version 300 es
`,p=[m,"#define attribute in","#define varying out","#define texture2D texture"].join(`
`)+`
`+p,u=["#define varying in",t.glslVersion===oo?"":"layout(location = 0) out highp vec4 pc_fragColor;",t.glslVersion===oo?"":"#define gl_FragColor pc_fragColor","#define gl_FragDepthEXT gl_FragDepth","#define texture2D texture","#define textureCube texture","#define texture2DProj textureProj","#define texture2DLodEXT textureLod","#define texture2DProjLodEXT textureProjLod","#define textureCubeLodEXT textureLod","#define texture2DGradEXT textureGrad","#define texture2DProjGradEXT textureProjGrad","#define textureCubeGradEXT textureGrad"].join(`
`)+`
`+u);const S=b+p+s,M=b+u+o,w=Yo(r,r.VERTEX_SHADER,S),T=Yo(r,r.FRAGMENT_SHADER,M);r.attachShader(_,w),r.attachShader(_,T),t.index0AttributeName!==void 0?r.bindAttribLocation(_,0,t.index0AttributeName):t.morphTargets===!0&&r.bindAttribLocation(_,0,"position"),r.linkProgram(_);function A(R){if(n.debug.checkShaderErrors){const U=r.getProgramInfoLog(_).trim(),C=r.getShaderInfoLog(w).trim(),D=r.getShaderInfoLog(T).trim();let k=!0,N=!0;if(r.getProgramParameter(_,r.LINK_STATUS)===!1)if(k=!1,typeof n.debug.onShaderError=="function")n.debug.onShaderError(r,_,w,T);else{const O=Jo(r,w,"vertex"),z=Jo(r,T,"fragment");console.error("THREE.WebGLProgram: Shader Error "+r.getError()+" - VALIDATE_STATUS "+r.getProgramParameter(_,r.VALIDATE_STATUS)+`

Material Name: `+R.name+`
Material Type: `+R.type+`

Program Info Log: `+U+`
`+O+`
`+z)}else U!==""?console.warn("THREE.WebGLProgram: Program Info Log:",U):(C===""||D==="")&&(N=!1);N&&(R.diagnostics={runnable:k,programLog:U,vertexShader:{log:C,prefix:p},fragmentShader:{log:D,prefix:u}})}r.deleteShader(w),r.deleteShader(T),L=new Ur(r,_),x=kp(r,_)}let L;this.getUniforms=function(){return L===void 0&&A(this),L};let x;this.getAttributes=function(){return x===void 0&&A(this),x};let v=t.rendererExtensionParallelShaderCompile===!1;return this.isReady=function(){return v===!1&&(v=r.getProgramParameter(_,Rp)),v},this.destroy=function(){i.releaseStatesOfProgram(this),r.deleteProgram(_),this.program=void 0},this.type=t.shaderType,this.name=t.shaderName,this.id=Cp++,this.cacheKey=e,this.usedTimes=1,this.program=_,this.vertexShader=w,this.fragmentShader=T,this}let $p=0;class Yp{constructor(){this.shaderCache=new Map,this.materialCache=new Map}update(e){const t=e.vertexShader,i=e.fragmentShader,r=this._getShaderStage(t),a=this._getShaderStage(i),s=this._getShaderCacheForMaterial(e);return s.has(r)===!1&&(s.add(r),r.usedTimes++),s.has(a)===!1&&(s.add(a),a.usedTimes++),this}remove(e){const t=this.materialCache.get(e);for(const i of t)i.usedTimes--,i.usedTimes===0&&this.shaderCache.delete(i.code);return this.materialCache.delete(e),this}getVertexShaderID(e){return this._getShaderStage(e.vertexShader).id}getFragmentShaderID(e){return this._getShaderStage(e.fragmentShader).id}dispose(){this.shaderCache.clear(),this.materialCache.clear()}_getShaderCacheForMaterial(e){const t=this.materialCache;let i=t.get(e);return i===void 0&&(i=new Set,t.set(e,i)),i}_getShaderStage(e){const t=this.shaderCache;let i=t.get(e);return i===void 0&&(i=new Zp(e),t.set(e,i)),i}}class Zp{constructor(e){this.id=$p++,this.code=e,this.usedTimes=0}}function Jp(n,e,t,i,r,a,s){const o=new ks,c=new Yp,l=new Set,d=[],h=r.logarithmicDepthBuffer,f=r.vertexTextures;let m=r.precision;const g={MeshDepthMaterial:"depth",MeshDistanceMaterial:"distanceRGBA",MeshNormalMaterial:"normal",MeshBasicMaterial:"basic",MeshLambertMaterial:"lambert",MeshPhongMaterial:"phong",MeshToonMaterial:"toon",MeshStandardMaterial:"physical",MeshPhysicalMaterial:"physical",MeshMatcapMaterial:"matcap",LineBasicMaterial:"basic",LineDashedMaterial:"dashed",PointsMaterial:"points",ShadowMaterial:"shadow",SpriteMaterial:"sprite"};function _(x){return l.add(x),x===0?"uv":`uv${x}`}function p(x,v,R,U,C){const D=U.fog,k=C.geometry,N=x.isMeshStandardMaterial?U.environment:null,O=(x.isMeshStandardMaterial?t:e).get(x.envMap||N),z=O&&O.mapping===Vr?O.image.height:null,H=g[x.type];x.precision!==null&&(m=r.getMaxPrecision(x.precision),m!==x.precision&&console.warn("THREE.WebGLProgram.getParameters:",x.precision,"not supported, using",m,"instead."));const q=k.morphAttributes.position||k.morphAttributes.normal||k.morphAttributes.color,J=q!==void 0?q.length:0;let fe=0;k.morphAttributes.position!==void 0&&(fe=1),k.morphAttributes.normal!==void 0&&(fe=2),k.morphAttributes.color!==void 0&&(fe=3);let Ae,K,ne,ue;if(H){const nt=en[H];Ae=nt.vertexShader,K=nt.fragmentShader}else Ae=x.vertexShader,K=x.fragmentShader,c.update(x),ne=c.getVertexShaderID(x),ue=c.getFragmentShaderID(x);const ae=n.getRenderTarget(),ee=n.state.buffers.depth.getReversed(),_e=C.isInstancedMesh===!0,de=C.isBatchedMesh===!0,Y=!!x.map,re=!!x.matcap,oe=!!O,I=!!x.aoMap,Ie=!!x.lightMap,Pe=!!x.bumpMap,Ce=!!x.normalMap,Me=!!x.displacementMap,Fe=!!x.emissiveMap,Re=!!x.metalnessMap,P=!!x.roughnessMap,E=x.anisotropy>0,G=x.clearcoat>0,Q=x.dispersion>0,ie=x.iridescence>0,Z=x.sheen>0,we=x.transmission>0,ge=E&&!!x.anisotropyMap,Ee=G&&!!x.clearcoatMap,$e=G&&!!x.clearcoatNormalMap,le=G&&!!x.clearcoatRoughnessMap,be=ie&&!!x.iridescenceMap,Ue=ie&&!!x.iridescenceThicknessMap,ze=Z&&!!x.sheenColorMap,ye=Z&&!!x.sheenRoughnessMap,qe=!!x.specularMap,je=!!x.specularColorMap,at=!!x.specularIntensityMap,B=we&&!!x.transmissionMap,pe=we&&!!x.thicknessMap,$=!!x.gradientMap,te=!!x.alphaMap,xe=x.alphaTest>0,ve=!!x.alphaHash,Oe=!!x.extensions;let lt=Dn;x.toneMapped&&(ae===null||ae.isXRRenderTarget===!0)&&(lt=n.toneMapping);const bt={shaderID:H,shaderType:x.type,shaderName:x.name,vertexShader:Ae,fragmentShader:K,defines:x.defines,customVertexShaderID:ne,customFragmentShaderID:ue,isRawShaderMaterial:x.isRawShaderMaterial===!0,glslVersion:x.glslVersion,precision:m,batching:de,batchingColor:de&&C._colorsTexture!==null,instancing:_e,instancingColor:_e&&C.instanceColor!==null,instancingMorph:_e&&C.morphTexture!==null,supportsVertexTextures:f,outputColorSpace:ae===null?n.outputColorSpace:ae.isXRRenderTarget===!0?ae.texture.colorSpace:Ci,alphaToCoverage:!!x.alphaToCoverage,map:Y,matcap:re,envMap:oe,envMapMode:oe&&O.mapping,envMapCubeUVHeight:z,aoMap:I,lightMap:Ie,bumpMap:Pe,normalMap:Ce,displacementMap:f&&Me,emissiveMap:Fe,normalMapObjectSpace:Ce&&x.normalMapType===Xl,normalMapTangentSpace:Ce&&x.normalMapType===Pc,metalnessMap:Re,roughnessMap:P,anisotropy:E,anisotropyMap:ge,clearcoat:G,clearcoatMap:Ee,clearcoatNormalMap:$e,clearcoatRoughnessMap:le,dispersion:Q,iridescence:ie,iridescenceMap:be,iridescenceThicknessMap:Ue,sheen:Z,sheenColorMap:ze,sheenRoughnessMap:ye,specularMap:qe,specularColorMap:je,specularIntensityMap:at,transmission:we,transmissionMap:B,thicknessMap:pe,gradientMap:$,opaque:x.transparent===!1&&x.blending===Si&&x.alphaToCoverage===!1,alphaMap:te,alphaTest:xe,alphaHash:ve,combine:x.combine,mapUv:Y&&_(x.map.channel),aoMapUv:I&&_(x.aoMap.channel),lightMapUv:Ie&&_(x.lightMap.channel),bumpMapUv:Pe&&_(x.bumpMap.channel),normalMapUv:Ce&&_(x.normalMap.channel),displacementMapUv:Me&&_(x.displacementMap.channel),emissiveMapUv:Fe&&_(x.emissiveMap.channel),metalnessMapUv:Re&&_(x.metalnessMap.channel),roughnessMapUv:P&&_(x.roughnessMap.channel),anisotropyMapUv:ge&&_(x.anisotropyMap.channel),clearcoatMapUv:Ee&&_(x.clearcoatMap.channel),clearcoatNormalMapUv:$e&&_(x.clearcoatNormalMap.channel),clearcoatRoughnessMapUv:le&&_(x.clearcoatRoughnessMap.channel),iridescenceMapUv:be&&_(x.iridescenceMap.channel),iridescenceThicknessMapUv:Ue&&_(x.iridescenceThicknessMap.channel),sheenColorMapUv:ze&&_(x.sheenColorMap.channel),sheenRoughnessMapUv:ye&&_(x.sheenRoughnessMap.channel),specularMapUv:qe&&_(x.specularMap.channel),specularColorMapUv:je&&_(x.specularColorMap.channel),specularIntensityMapUv:at&&_(x.specularIntensityMap.channel),transmissionMapUv:B&&_(x.transmissionMap.channel),thicknessMapUv:pe&&_(x.thicknessMap.channel),alphaMapUv:te&&_(x.alphaMap.channel),vertexTangents:!!k.attributes.tangent&&(Ce||E),vertexColors:x.vertexColors,vertexAlphas:x.vertexColors===!0&&!!k.attributes.color&&k.attributes.color.itemSize===4,pointsUvs:C.isPoints===!0&&!!k.attributes.uv&&(Y||te),fog:!!D,useFog:x.fog===!0,fogExp2:!!D&&D.isFogExp2,flatShading:x.flatShading===!0,sizeAttenuation:x.sizeAttenuation===!0,logarithmicDepthBuffer:h,reverseDepthBuffer:ee,skinning:C.isSkinnedMesh===!0,morphTargets:k.morphAttributes.position!==void 0,morphNormals:k.morphAttributes.normal!==void 0,morphColors:k.morphAttributes.color!==void 0,morphTargetsCount:J,morphTextureStride:fe,numDirLights:v.directional.length,numPointLights:v.point.length,numSpotLights:v.spot.length,numSpotLightMaps:v.spotLightMap.length,numRectAreaLights:v.rectArea.length,numHemiLights:v.hemi.length,numDirLightShadows:v.directionalShadowMap.length,numPointLightShadows:v.pointShadowMap.length,numSpotLightShadows:v.spotShadowMap.length,numSpotLightShadowsWithMaps:v.numSpotLightShadowsWithMaps,numLightProbes:v.numLightProbes,numClippingPlanes:s.numPlanes,numClipIntersection:s.numIntersection,dithering:x.dithering,shadowMapEnabled:n.shadowMap.enabled&&R.length>0,shadowMapType:n.shadowMap.type,toneMapping:lt,decodeVideoTexture:Y&&x.map.isVideoTexture===!0&&Qe.getTransfer(x.map.colorSpace)===rt,decodeVideoTextureEmissive:Fe&&x.emissiveMap.isVideoTexture===!0&&Qe.getTransfer(x.emissiveMap.colorSpace)===rt,premultipliedAlpha:x.premultipliedAlpha,doubleSided:x.side===St,flipSided:x.side===Lt,useDepthPacking:x.depthPacking>=0,depthPacking:x.depthPacking||0,index0AttributeName:x.index0AttributeName,extensionClipCullDistance:Oe&&x.extensions.clipCullDistance===!0&&i.has("WEBGL_clip_cull_distance"),extensionMultiDraw:(Oe&&x.extensions.multiDraw===!0||de)&&i.has("WEBGL_multi_draw"),rendererExtensionParallelShaderCompile:i.has("KHR_parallel_shader_compile"),customProgramCacheKey:x.customProgramCacheKey()};return bt.vertexUv1s=l.has(1),bt.vertexUv2s=l.has(2),bt.vertexUv3s=l.has(3),l.clear(),bt}function u(x){const v=[];if(x.shaderID?v.push(x.shaderID):(v.push(x.customVertexShaderID),v.push(x.customFragmentShaderID)),x.defines!==void 0)for(const R in x.defines)v.push(R),v.push(x.defines[R]);return x.isRawShaderMaterial===!1&&(b(v,x),S(v,x),v.push(n.outputColorSpace)),v.push(x.customProgramCacheKey),v.join()}function b(x,v){x.push(v.precision),x.push(v.outputColorSpace),x.push(v.envMapMode),x.push(v.envMapCubeUVHeight),x.push(v.mapUv),x.push(v.alphaMapUv),x.push(v.lightMapUv),x.push(v.aoMapUv),x.push(v.bumpMapUv),x.push(v.normalMapUv),x.push(v.displacementMapUv),x.push(v.emissiveMapUv),x.push(v.metalnessMapUv),x.push(v.roughnessMapUv),x.push(v.anisotropyMapUv),x.push(v.clearcoatMapUv),x.push(v.clearcoatNormalMapUv),x.push(v.clearcoatRoughnessMapUv),x.push(v.iridescenceMapUv),x.push(v.iridescenceThicknessMapUv),x.push(v.sheenColorMapUv),x.push(v.sheenRoughnessMapUv),x.push(v.specularMapUv),x.push(v.specularColorMapUv),x.push(v.specularIntensityMapUv),x.push(v.transmissionMapUv),x.push(v.thicknessMapUv),x.push(v.combine),x.push(v.fogExp2),x.push(v.sizeAttenuation),x.push(v.morphTargetsCount),x.push(v.morphAttributeCount),x.push(v.numDirLights),x.push(v.numPointLights),x.push(v.numSpotLights),x.push(v.numSpotLightMaps),x.push(v.numHemiLights),x.push(v.numRectAreaLights),x.push(v.numDirLightShadows),x.push(v.numPointLightShadows),x.push(v.numSpotLightShadows),x.push(v.numSpotLightShadowsWithMaps),x.push(v.numLightProbes),x.push(v.shadowMapType),x.push(v.toneMapping),x.push(v.numClippingPlanes),x.push(v.numClipIntersection),x.push(v.depthPacking)}function S(x,v){o.disableAll(),v.supportsVertexTextures&&o.enable(0),v.instancing&&o.enable(1),v.instancingColor&&o.enable(2),v.instancingMorph&&o.enable(3),v.matcap&&o.enable(4),v.envMap&&o.enable(5),v.normalMapObjectSpace&&o.enable(6),v.normalMapTangentSpace&&o.enable(7),v.clearcoat&&o.enable(8),v.iridescence&&o.enable(9),v.alphaTest&&o.enable(10),v.vertexColors&&o.enable(11),v.vertexAlphas&&o.enable(12),v.vertexUv1s&&o.enable(13),v.vertexUv2s&&o.enable(14),v.vertexUv3s&&o.enable(15),v.vertexTangents&&o.enable(16),v.anisotropy&&o.enable(17),v.alphaHash&&o.enable(18),v.batching&&o.enable(19),v.dispersion&&o.enable(20),v.batchingColor&&o.enable(21),x.push(o.mask),o.disableAll(),v.fog&&o.enable(0),v.useFog&&o.enable(1),v.flatShading&&o.enable(2),v.logarithmicDepthBuffer&&o.enable(3),v.reverseDepthBuffer&&o.enable(4),v.skinning&&o.enable(5),v.morphTargets&&o.enable(6),v.morphNormals&&o.enable(7),v.morphColors&&o.enable(8),v.premultipliedAlpha&&o.enable(9),v.shadowMapEnabled&&o.enable(10),v.doubleSided&&o.enable(11),v.flipSided&&o.enable(12),v.useDepthPacking&&o.enable(13),v.dithering&&o.enable(14),v.transmission&&o.enable(15),v.sheen&&o.enable(16),v.opaque&&o.enable(17),v.pointsUvs&&o.enable(18),v.decodeVideoTexture&&o.enable(19),v.decodeVideoTextureEmissive&&o.enable(20),v.alphaToCoverage&&o.enable(21),x.push(o.mask)}function M(x){const v=g[x.type];let R;if(v){const U=en[v];R=bu.clone(U.uniforms)}else R=x.uniforms;return R}function w(x,v){let R;for(let U=0,C=d.length;U<C;U++){const D=d[U];if(D.cacheKey===v){R=D,++R.usedTimes;break}}return R===void 0&&(R=new qp(n,v,x,a),d.push(R)),R}function T(x){if(--x.usedTimes===0){const v=d.indexOf(x);d[v]=d[d.length-1],d.pop(),x.destroy()}}function A(x){c.remove(x)}function L(){c.dispose()}return{getParameters:p,getProgramCacheKey:u,getUniforms:M,acquireProgram:w,releaseProgram:T,releaseShaderCache:A,programs:d,dispose:L}}function Qp(){let n=new WeakMap;function e(s){return n.has(s)}function t(s){let o=n.get(s);return o===void 0&&(o={},n.set(s,o)),o}function i(s){n.delete(s)}function r(s,o,c){n.get(s)[o]=c}function a(){n=new WeakMap}return{has:e,get:t,remove:i,update:r,dispose:a}}function em(n,e){return n.groupOrder!==e.groupOrder?n.groupOrder-e.groupOrder:n.renderOrder!==e.renderOrder?n.renderOrder-e.renderOrder:n.material.id!==e.material.id?n.material.id-e.material.id:n.z!==e.z?n.z-e.z:n.id-e.id}function ic(n,e){return n.groupOrder!==e.groupOrder?n.groupOrder-e.groupOrder:n.renderOrder!==e.renderOrder?n.renderOrder-e.renderOrder:n.z!==e.z?e.z-n.z:n.id-e.id}function rc(){const n=[];let e=0;const t=[],i=[],r=[];function a(){e=0,t.length=0,i.length=0,r.length=0}function s(h,f,m,g,_,p){let u=n[e];return u===void 0?(u={id:h.id,object:h,geometry:f,material:m,groupOrder:g,renderOrder:h.renderOrder,z:_,group:p},n[e]=u):(u.id=h.id,u.object=h,u.geometry=f,u.material=m,u.groupOrder=g,u.renderOrder=h.renderOrder,u.z=_,u.group=p),e++,u}function o(h,f,m,g,_,p){const u=s(h,f,m,g,_,p);m.transmission>0?i.push(u):m.transparent===!0?r.push(u):t.push(u)}function c(h,f,m,g,_,p){const u=s(h,f,m,g,_,p);m.transmission>0?i.unshift(u):m.transparent===!0?r.unshift(u):t.unshift(u)}function l(h,f){t.length>1&&t.sort(h||em),i.length>1&&i.sort(f||ic),r.length>1&&r.sort(f||ic)}function d(){for(let h=e,f=n.length;h<f;h++){const m=n[h];if(m.id===null)break;m.id=null,m.object=null,m.geometry=null,m.material=null,m.group=null}}return{opaque:t,transmissive:i,transparent:r,init:a,push:o,unshift:c,finish:d,sort:l}}function tm(){let n=new WeakMap;function e(i,r){const a=n.get(i);let s;return a===void 0?(s=new rc,n.set(i,[s])):r>=a.length?(s=new rc,a.push(s)):s=a[r],s}function t(){n=new WeakMap}return{get:e,dispose:t}}function nm(){const n={};return{get:function(e){if(n[e.id]!==void 0)return n[e.id];let t;switch(e.type){case"DirectionalLight":t={direction:new F,color:new ce};break;case"SpotLight":t={position:new F,direction:new F,color:new ce,distance:0,coneCos:0,penumbraCos:0,decay:0};break;case"PointLight":t={position:new F,color:new ce,distance:0,decay:0};break;case"HemisphereLight":t={direction:new F,skyColor:new ce,groundColor:new ce};break;case"RectAreaLight":t={color:new ce,position:new F,halfWidth:new F,halfHeight:new F};break}return n[e.id]=t,t}}}function im(){const n={};return{get:function(e){if(n[e.id]!==void 0)return n[e.id];let t;switch(e.type){case"DirectionalLight":t={shadowIntensity:1,shadowBias:0,shadowNormalBias:0,shadowRadius:1,shadowMapSize:new Ke};break;case"SpotLight":t={shadowIntensity:1,shadowBias:0,shadowNormalBias:0,shadowRadius:1,shadowMapSize:new Ke};break;case"PointLight":t={shadowIntensity:1,shadowBias:0,shadowNormalBias:0,shadowRadius:1,shadowMapSize:new Ke,shadowCameraNear:1,shadowCameraFar:1e3};break}return n[e.id]=t,t}}}let rm=0;function am(n,e){return(e.castShadow?2:0)-(n.castShadow?2:0)+(e.map?1:0)-(n.map?1:0)}function sm(n){const e=new nm,t=im(),i={version:0,hash:{directionalLength:-1,pointLength:-1,spotLength:-1,rectAreaLength:-1,hemiLength:-1,numDirectionalShadows:-1,numPointShadows:-1,numSpotShadows:-1,numSpotMaps:-1,numLightProbes:-1},ambient:[0,0,0],probe:[],directional:[],directionalShadow:[],directionalShadowMap:[],directionalShadowMatrix:[],spot:[],spotLightMap:[],spotShadow:[],spotShadowMap:[],spotLightMatrix:[],rectArea:[],rectAreaLTC1:null,rectAreaLTC2:null,point:[],pointShadow:[],pointShadowMap:[],pointShadowMatrix:[],hemi:[],numSpotLightShadowsWithMaps:0,numLightProbes:0};for(let l=0;l<9;l++)i.probe.push(new F);const r=new F,a=new ct,s=new ct;function o(l){let d=0,h=0,f=0;for(let x=0;x<9;x++)i.probe[x].set(0,0,0);let m=0,g=0,_=0,p=0,u=0,b=0,S=0,M=0,w=0,T=0,A=0;l.sort(am);for(let x=0,v=l.length;x<v;x++){const R=l[x],U=R.color,C=R.intensity,D=R.distance,k=R.shadow&&R.shadow.map?R.shadow.map.texture:null;if(R.isAmbientLight)d+=U.r*C,h+=U.g*C,f+=U.b*C;else if(R.isLightProbe){for(let N=0;N<9;N++)i.probe[N].addScaledVector(R.sh.coefficients[N],C);A++}else if(R.isDirectionalLight){const N=e.get(R);if(N.color.copy(R.color).multiplyScalar(R.intensity),R.castShadow){const O=R.shadow,z=t.get(R);z.shadowIntensity=O.intensity,z.shadowBias=O.bias,z.shadowNormalBias=O.normalBias,z.shadowRadius=O.radius,z.shadowMapSize=O.mapSize,i.directionalShadow[m]=z,i.directionalShadowMap[m]=k,i.directionalShadowMatrix[m]=R.shadow.matrix,b++}i.directional[m]=N,m++}else if(R.isSpotLight){const N=e.get(R);N.position.setFromMatrixPosition(R.matrixWorld),N.color.copy(U).multiplyScalar(C),N.distance=D,N.coneCos=Math.cos(R.angle),N.penumbraCos=Math.cos(R.angle*(1-R.penumbra)),N.decay=R.decay,i.spot[_]=N;const O=R.shadow;if(R.map&&(i.spotLightMap[w]=R.map,w++,O.updateMatrices(R),R.castShadow&&T++),i.spotLightMatrix[_]=O.matrix,R.castShadow){const z=t.get(R);z.shadowIntensity=O.intensity,z.shadowBias=O.bias,z.shadowNormalBias=O.normalBias,z.shadowRadius=O.radius,z.shadowMapSize=O.mapSize,i.spotShadow[_]=z,i.spotShadowMap[_]=k,M++}_++}else if(R.isRectAreaLight){const N=e.get(R);N.color.copy(U).multiplyScalar(C),N.halfWidth.set(R.width*.5,0,0),N.halfHeight.set(0,R.height*.5,0),i.rectArea[p]=N,p++}else if(R.isPointLight){const N=e.get(R);if(N.color.copy(R.color).multiplyScalar(R.intensity),N.distance=R.distance,N.decay=R.decay,R.castShadow){const O=R.shadow,z=t.get(R);z.shadowIntensity=O.intensity,z.shadowBias=O.bias,z.shadowNormalBias=O.normalBias,z.shadowRadius=O.radius,z.shadowMapSize=O.mapSize,z.shadowCameraNear=O.camera.near,z.shadowCameraFar=O.camera.far,i.pointShadow[g]=z,i.pointShadowMap[g]=k,i.pointShadowMatrix[g]=R.shadow.matrix,S++}i.point[g]=N,g++}else if(R.isHemisphereLight){const N=e.get(R);N.skyColor.copy(R.color).multiplyScalar(C),N.groundColor.copy(R.groundColor).multiplyScalar(C),i.hemi[u]=N,u++}}p>0&&(n.has("OES_texture_float_linear")===!0?(i.rectAreaLTC1=he.LTC_FLOAT_1,i.rectAreaLTC2=he.LTC_FLOAT_2):(i.rectAreaLTC1=he.LTC_HALF_1,i.rectAreaLTC2=he.LTC_HALF_2)),i.ambient[0]=d,i.ambient[1]=h,i.ambient[2]=f;const L=i.hash;(L.directionalLength!==m||L.pointLength!==g||L.spotLength!==_||L.rectAreaLength!==p||L.hemiLength!==u||L.numDirectionalShadows!==b||L.numPointShadows!==S||L.numSpotShadows!==M||L.numSpotMaps!==w||L.numLightProbes!==A)&&(i.directional.length=m,i.spot.length=_,i.rectArea.length=p,i.point.length=g,i.hemi.length=u,i.directionalShadow.length=b,i.directionalShadowMap.length=b,i.pointShadow.length=S,i.pointShadowMap.length=S,i.spotShadow.length=M,i.spotShadowMap.length=M,i.directionalShadowMatrix.length=b,i.pointShadowMatrix.length=S,i.spotLightMatrix.length=M+w-T,i.spotLightMap.length=w,i.numSpotLightShadowsWithMaps=T,i.numLightProbes=A,L.directionalLength=m,L.pointLength=g,L.spotLength=_,L.rectAreaLength=p,L.hemiLength=u,L.numDirectionalShadows=b,L.numPointShadows=S,L.numSpotShadows=M,L.numSpotMaps=w,L.numLightProbes=A,i.version=rm++)}function c(l,d){let h=0,f=0,m=0,g=0,_=0;const p=d.matrixWorldInverse;for(let u=0,b=l.length;u<b;u++){const S=l[u];if(S.isDirectionalLight){const M=i.directional[h];M.direction.setFromMatrixPosition(S.matrixWorld),r.setFromMatrixPosition(S.target.matrixWorld),M.direction.sub(r),M.direction.transformDirection(p),h++}else if(S.isSpotLight){const M=i.spot[m];M.position.setFromMatrixPosition(S.matrixWorld),M.position.applyMatrix4(p),M.direction.setFromMatrixPosition(S.matrixWorld),r.setFromMatrixPosition(S.target.matrixWorld),M.direction.sub(r),M.direction.transformDirection(p),m++}else if(S.isRectAreaLight){const M=i.rectArea[g];M.position.setFromMatrixPosition(S.matrixWorld),M.position.applyMatrix4(p),s.identity(),a.copy(S.matrixWorld),a.premultiply(p),s.extractRotation(a),M.halfWidth.set(S.width*.5,0,0),M.halfHeight.set(0,S.height*.5,0),M.halfWidth.applyMatrix4(s),M.halfHeight.applyMatrix4(s),g++}else if(S.isPointLight){const M=i.point[f];M.position.setFromMatrixPosition(S.matrixWorld),M.position.applyMatrix4(p),f++}else if(S.isHemisphereLight){const M=i.hemi[_];M.direction.setFromMatrixPosition(S.matrixWorld),M.direction.transformDirection(p),_++}}}return{setup:o,setupView:c,state:i}}function ac(n){const e=new sm(n),t=[],i=[];function r(d){l.camera=d,t.length=0,i.length=0}function a(d){t.push(d)}function s(d){i.push(d)}function o(){e.setup(t)}function c(d){e.setupView(t,d)}const l={lightsArray:t,shadowsArray:i,camera:null,lights:e,transmissionRenderTarget:{}};return{init:r,state:l,setupLights:o,setupLightsView:c,pushLight:a,pushShadow:s}}function om(n){let e=new WeakMap;function t(r,a=0){const s=e.get(r);let o;return s===void 0?(o=new ac(n),e.set(r,[o])):a>=s.length?(o=new ac(n),s.push(o)):o=s[a],o}function i(){e=new WeakMap}return{get:t,dispose:i}}const cm=`void main() {
	gl_Position = vec4( position, 1.0 );
}`,lm=`uniform sampler2D shadow_pass;
uniform vec2 resolution;
uniform float radius;
#include <packing>
void main() {
	const float samples = float( VSM_SAMPLES );
	float mean = 0.0;
	float squared_mean = 0.0;
	float uvStride = samples <= 1.0 ? 0.0 : 2.0 / ( samples - 1.0 );
	float uvStart = samples <= 1.0 ? 0.0 : - 1.0;
	for ( float i = 0.0; i < samples; i ++ ) {
		float uvOffset = uvStart + i * uvStride;
		#ifdef HORIZONTAL_PASS
			vec2 distribution = unpackRGBATo2Half( texture2D( shadow_pass, ( gl_FragCoord.xy + vec2( uvOffset, 0.0 ) * radius ) / resolution ) );
			mean += distribution.x;
			squared_mean += distribution.y * distribution.y + distribution.x * distribution.x;
		#else
			float depth = unpackRGBAToDepth( texture2D( shadow_pass, ( gl_FragCoord.xy + vec2( 0.0, uvOffset ) * radius ) / resolution ) );
			mean += depth;
			squared_mean += depth * depth;
		#endif
	}
	mean = mean / samples;
	squared_mean = squared_mean / samples;
	float std_dev = sqrt( squared_mean - mean * mean );
	gl_FragColor = pack2HalfToRGBA( vec2( mean, std_dev ) );
}`;function um(n,e,t){let i=new Fs;const r=new Ke,a=new Ke,s=new dt,o=new Lu({depthPacking:Wl}),c=new Iu,l={},d=t.maxTextureSize,h={[Ln]:Lt,[Lt]:Ln,[St]:St},f=new In({defines:{VSM_SAMPLES:8},uniforms:{shadow_pass:{value:null},resolution:{value:new Ke},radius:{value:4}},vertexShader:cm,fragmentShader:lm}),m=f.clone();m.defines.HORIZONTAL_PASS=1;const g=new Ze;g.setAttribute("position",new nn(new Float32Array([-1,-1,.5,3,-1,.5,-1,3,.5]),3));const _=new We(g,f),p=this;this.enabled=!1,this.autoUpdate=!0,this.needsUpdate=!1,this.type=_c;let u=this.type;this.render=function(T,A,L){if(p.enabled===!1||p.autoUpdate===!1&&p.needsUpdate===!1||T.length===0)return;const x=n.getRenderTarget(),v=n.getActiveCubeFace(),R=n.getActiveMipmapLevel(),U=n.state;U.setBlending(Pn),U.buffers.color.setClear(1,1,1,1),U.buffers.depth.setTest(!0),U.setScissorTest(!1);const C=u!==hn&&this.type===hn,D=u===hn&&this.type!==hn;for(let k=0,N=T.length;k<N;k++){const O=T[k],z=O.shadow;if(z===void 0){console.warn("THREE.WebGLShadowMap:",O,"has no shadow.");continue}if(z.autoUpdate===!1&&z.needsUpdate===!1)continue;r.copy(z.mapSize);const H=z.getFrameExtents();if(r.multiply(H),a.copy(z.mapSize),(r.x>d||r.y>d)&&(r.x>d&&(a.x=Math.floor(d/H.x),r.x=a.x*H.x,z.mapSize.x=a.x),r.y>d&&(a.y=Math.floor(d/H.y),r.y=a.y*H.y,z.mapSize.y=a.y)),z.map===null||C===!0||D===!0){const J=this.type!==hn?{minFilter:Jt,magFilter:Jt}:{};z.map!==null&&z.map.dispose(),z.map=new ei(r.x,r.y,J),z.map.texture.name=O.name+".shadowMap",z.camera.updateProjectionMatrix()}n.setRenderTarget(z.map),n.clear();const q=z.getViewportCount();for(let J=0;J<q;J++){const fe=z.getViewport(J);s.set(a.x*fe.x,a.y*fe.y,a.x*fe.z,a.y*fe.w),U.viewport(s),z.updateMatrices(O,J),i=z.getFrustum(),M(A,L,z.camera,O,this.type)}z.isPointLightShadow!==!0&&this.type===hn&&b(z,L),z.needsUpdate=!1}u=this.type,p.needsUpdate=!1,n.setRenderTarget(x,v,R)};function b(T,A){const L=e.update(_);f.defines.VSM_SAMPLES!==T.blurSamples&&(f.defines.VSM_SAMPLES=T.blurSamples,m.defines.VSM_SAMPLES=T.blurSamples,f.needsUpdate=!0,m.needsUpdate=!0),T.mapPass===null&&(T.mapPass=new ei(r.x,r.y)),f.uniforms.shadow_pass.value=T.map.texture,f.uniforms.resolution.value=T.mapSize,f.uniforms.radius.value=T.radius,n.setRenderTarget(T.mapPass),n.clear(),n.renderBufferDirect(A,null,L,f,_,null),m.uniforms.shadow_pass.value=T.mapPass.texture,m.uniforms.resolution.value=T.mapSize,m.uniforms.radius.value=T.radius,n.setRenderTarget(T.map),n.clear(),n.renderBufferDirect(A,null,L,m,_,null)}function S(T,A,L,x){let v=null;const R=L.isPointLight===!0?T.customDistanceMaterial:T.customDepthMaterial;if(R!==void 0)v=R;else if(v=L.isPointLight===!0?c:o,n.localClippingEnabled&&A.clipShadows===!0&&Array.isArray(A.clippingPlanes)&&A.clippingPlanes.length!==0||A.displacementMap&&A.displacementScale!==0||A.alphaMap&&A.alphaTest>0||A.map&&A.alphaTest>0){const U=v.uuid,C=A.uuid;let D=l[U];D===void 0&&(D={},l[U]=D);let k=D[C];k===void 0&&(k=v.clone(),D[C]=k,A.addEventListener("dispose",w)),v=k}if(v.visible=A.visible,v.wireframe=A.wireframe,x===hn?v.side=A.shadowSide!==null?A.shadowSide:A.side:v.side=A.shadowSide!==null?A.shadowSide:h[A.side],v.alphaMap=A.alphaMap,v.alphaTest=A.alphaTest,v.map=A.map,v.clipShadows=A.clipShadows,v.clippingPlanes=A.clippingPlanes,v.clipIntersection=A.clipIntersection,v.displacementMap=A.displacementMap,v.displacementScale=A.displacementScale,v.displacementBias=A.displacementBias,v.wireframeLinewidth=A.wireframeLinewidth,v.linewidth=A.linewidth,L.isPointLight===!0&&v.isMeshDistanceMaterial===!0){const U=n.properties.get(v);U.light=L}return v}function M(T,A,L,x,v){if(T.visible===!1)return;if(T.layers.test(A.layers)&&(T.isMesh||T.isLine||T.isPoints)&&(T.castShadow||T.receiveShadow&&v===hn)&&(!T.frustumCulled||i.intersectsObject(T))){T.modelViewMatrix.multiplyMatrices(L.matrixWorldInverse,T.matrixWorld);const C=e.update(T),D=T.material;if(Array.isArray(D)){const k=C.groups;for(let N=0,O=k.length;N<O;N++){const z=k[N],H=D[z.materialIndex];if(H&&H.visible){const q=S(T,H,x,v);T.onBeforeShadow(n,T,A,L,C,q,z),n.renderBufferDirect(L,null,C,q,T,z),T.onAfterShadow(n,T,A,L,C,q,z)}}}else if(D.visible){const k=S(T,D,x,v);T.onBeforeShadow(n,T,A,L,C,k,null),n.renderBufferDirect(L,null,C,k,T,null),T.onAfterShadow(n,T,A,L,C,k,null)}}const U=T.children;for(let C=0,D=U.length;C<D;C++)M(U[C],A,L,x,v)}function w(T){T.target.removeEventListener("dispose",w);for(const L in l){const x=l[L],v=T.target.uuid;v in x&&(x[v].dispose(),delete x[v])}}}const dm={[za]:Na,[ka]:Ba,[Fa]:ja,[yi]:Oa,[Na]:za,[Ba]:ka,[ja]:Fa,[Oa]:yi};function hm(n,e){function t(){let B=!1;const pe=new dt;let $=null;const te=new dt(0,0,0,0);return{setMask:function(xe){$!==xe&&!B&&(n.colorMask(xe,xe,xe,xe),$=xe)},setLocked:function(xe){B=xe},setClear:function(xe,ve,Oe,lt,bt){bt===!0&&(xe*=lt,ve*=lt,Oe*=lt),pe.set(xe,ve,Oe,lt),te.equals(pe)===!1&&(n.clearColor(xe,ve,Oe,lt),te.copy(pe))},reset:function(){B=!1,$=null,te.set(-1,0,0,0)}}}function i(){let B=!1,pe=!1,$=null,te=null,xe=null;return{setReversed:function(ve){if(pe!==ve){const Oe=e.get("EXT_clip_control");pe?Oe.clipControlEXT(Oe.LOWER_LEFT_EXT,Oe.ZERO_TO_ONE_EXT):Oe.clipControlEXT(Oe.LOWER_LEFT_EXT,Oe.NEGATIVE_ONE_TO_ONE_EXT);const lt=xe;xe=null,this.setClear(lt)}pe=ve},getReversed:function(){return pe},setTest:function(ve){ve?ae(n.DEPTH_TEST):ee(n.DEPTH_TEST)},setMask:function(ve){$!==ve&&!B&&(n.depthMask(ve),$=ve)},setFunc:function(ve){if(pe&&(ve=dm[ve]),te!==ve){switch(ve){case za:n.depthFunc(n.NEVER);break;case Na:n.depthFunc(n.ALWAYS);break;case ka:n.depthFunc(n.LESS);break;case yi:n.depthFunc(n.LEQUAL);break;case Fa:n.depthFunc(n.EQUAL);break;case Oa:n.depthFunc(n.GEQUAL);break;case Ba:n.depthFunc(n.GREATER);break;case ja:n.depthFunc(n.NOTEQUAL);break;default:n.depthFunc(n.LEQUAL)}te=ve}},setLocked:function(ve){B=ve},setClear:function(ve){xe!==ve&&(pe&&(ve=1-ve),n.clearDepth(ve),xe=ve)},reset:function(){B=!1,$=null,te=null,xe=null,pe=!1}}}function r(){let B=!1,pe=null,$=null,te=null,xe=null,ve=null,Oe=null,lt=null,bt=null;return{setTest:function(nt){B||(nt?ae(n.STENCIL_TEST):ee(n.STENCIL_TEST))},setMask:function(nt){pe!==nt&&!B&&(n.stencilMask(nt),pe=nt)},setFunc:function(nt,Wt,rn){($!==nt||te!==Wt||xe!==rn)&&(n.stencilFunc(nt,Wt,rn),$=nt,te=Wt,xe=rn)},setOp:function(nt,Wt,rn){(ve!==nt||Oe!==Wt||lt!==rn)&&(n.stencilOp(nt,Wt,rn),ve=nt,Oe=Wt,lt=rn)},setLocked:function(nt){B=nt},setClear:function(nt){bt!==nt&&(n.clearStencil(nt),bt=nt)},reset:function(){B=!1,pe=null,$=null,te=null,xe=null,ve=null,Oe=null,lt=null,bt=null}}}const a=new t,s=new i,o=new r,c=new WeakMap,l=new WeakMap;let d={},h={},f=new WeakMap,m=[],g=null,_=!1,p=null,u=null,b=null,S=null,M=null,w=null,T=null,A=new ce(0,0,0),L=0,x=!1,v=null,R=null,U=null,C=null,D=null;const k=n.getParameter(n.MAX_COMBINED_TEXTURE_IMAGE_UNITS);let N=!1,O=0;const z=n.getParameter(n.VERSION);z.indexOf("WebGL")!==-1?(O=parseFloat(/^WebGL (\d)/.exec(z)[1]),N=O>=1):z.indexOf("OpenGL ES")!==-1&&(O=parseFloat(/^OpenGL ES (\d)/.exec(z)[1]),N=O>=2);let H=null,q={};const J=n.getParameter(n.SCISSOR_BOX),fe=n.getParameter(n.VIEWPORT),Ae=new dt().fromArray(J),K=new dt().fromArray(fe);function ne(B,pe,$,te){const xe=new Uint8Array(4),ve=n.createTexture();n.bindTexture(B,ve),n.texParameteri(B,n.TEXTURE_MIN_FILTER,n.NEAREST),n.texParameteri(B,n.TEXTURE_MAG_FILTER,n.NEAREST);for(let Oe=0;Oe<$;Oe++)B===n.TEXTURE_3D||B===n.TEXTURE_2D_ARRAY?n.texImage3D(pe,0,n.RGBA,1,1,te,0,n.RGBA,n.UNSIGNED_BYTE,xe):n.texImage2D(pe+Oe,0,n.RGBA,1,1,0,n.RGBA,n.UNSIGNED_BYTE,xe);return ve}const ue={};ue[n.TEXTURE_2D]=ne(n.TEXTURE_2D,n.TEXTURE_2D,1),ue[n.TEXTURE_CUBE_MAP]=ne(n.TEXTURE_CUBE_MAP,n.TEXTURE_CUBE_MAP_POSITIVE_X,6),ue[n.TEXTURE_2D_ARRAY]=ne(n.TEXTURE_2D_ARRAY,n.TEXTURE_2D_ARRAY,1,1),ue[n.TEXTURE_3D]=ne(n.TEXTURE_3D,n.TEXTURE_3D,1,1),a.setClear(0,0,0,1),s.setClear(1),o.setClear(0),ae(n.DEPTH_TEST),s.setFunc(yi),Pe(!1),Ce(to),ae(n.CULL_FACE),I(Pn);function ae(B){d[B]!==!0&&(n.enable(B),d[B]=!0)}function ee(B){d[B]!==!1&&(n.disable(B),d[B]=!1)}function _e(B,pe){return h[B]!==pe?(n.bindFramebuffer(B,pe),h[B]=pe,B===n.DRAW_FRAMEBUFFER&&(h[n.FRAMEBUFFER]=pe),B===n.FRAMEBUFFER&&(h[n.DRAW_FRAMEBUFFER]=pe),!0):!1}function de(B,pe){let $=m,te=!1;if(B){$=f.get(pe),$===void 0&&($=[],f.set(pe,$));const xe=B.textures;if($.length!==xe.length||$[0]!==n.COLOR_ATTACHMENT0){for(let ve=0,Oe=xe.length;ve<Oe;ve++)$[ve]=n.COLOR_ATTACHMENT0+ve;$.length=xe.length,te=!0}}else $[0]!==n.BACK&&($[0]=n.BACK,te=!0);te&&n.drawBuffers($)}function Y(B){return g!==B?(n.useProgram(B),g=B,!0):!1}const re={[Kn]:n.FUNC_ADD,[_l]:n.FUNC_SUBTRACT,[vl]:n.FUNC_REVERSE_SUBTRACT};re[xl]=n.MIN,re[Ml]=n.MAX;const oe={[Sl]:n.ZERO,[El]:n.ONE,[bl]:n.SRC_COLOR,[Ia]:n.SRC_ALPHA,[Cl]:n.SRC_ALPHA_SATURATE,[Al]:n.DST_COLOR,[Tl]:n.DST_ALPHA,[yl]:n.ONE_MINUS_SRC_COLOR,[Ua]:n.ONE_MINUS_SRC_ALPHA,[Rl]:n.ONE_MINUS_DST_COLOR,[wl]:n.ONE_MINUS_DST_ALPHA,[Pl]:n.CONSTANT_COLOR,[Dl]:n.ONE_MINUS_CONSTANT_COLOR,[Ll]:n.CONSTANT_ALPHA,[Il]:n.ONE_MINUS_CONSTANT_ALPHA};function I(B,pe,$,te,xe,ve,Oe,lt,bt,nt){if(B===Pn){_===!0&&(ee(n.BLEND),_=!1);return}if(_===!1&&(ae(n.BLEND),_=!0),B!==gl){if(B!==p||nt!==x){if((u!==Kn||M!==Kn)&&(n.blendEquation(n.FUNC_ADD),u=Kn,M=Kn),nt)switch(B){case Si:n.blendFuncSeparate(n.ONE,n.ONE_MINUS_SRC_ALPHA,n.ONE,n.ONE_MINUS_SRC_ALPHA);break;case no:n.blendFunc(n.ONE,n.ONE);break;case io:n.blendFuncSeparate(n.ZERO,n.ONE_MINUS_SRC_COLOR,n.ZERO,n.ONE);break;case ro:n.blendFuncSeparate(n.ZERO,n.SRC_COLOR,n.ZERO,n.SRC_ALPHA);break;default:console.error("THREE.WebGLState: Invalid blending: ",B);break}else switch(B){case Si:n.blendFuncSeparate(n.SRC_ALPHA,n.ONE_MINUS_SRC_ALPHA,n.ONE,n.ONE_MINUS_SRC_ALPHA);break;case no:n.blendFunc(n.SRC_ALPHA,n.ONE);break;case io:n.blendFuncSeparate(n.ZERO,n.ONE_MINUS_SRC_COLOR,n.ZERO,n.ONE);break;case ro:n.blendFunc(n.ZERO,n.SRC_COLOR);break;default:console.error("THREE.WebGLState: Invalid blending: ",B);break}b=null,S=null,w=null,T=null,A.set(0,0,0),L=0,p=B,x=nt}return}xe=xe||pe,ve=ve||$,Oe=Oe||te,(pe!==u||xe!==M)&&(n.blendEquationSeparate(re[pe],re[xe]),u=pe,M=xe),($!==b||te!==S||ve!==w||Oe!==T)&&(n.blendFuncSeparate(oe[$],oe[te],oe[ve],oe[Oe]),b=$,S=te,w=ve,T=Oe),(lt.equals(A)===!1||bt!==L)&&(n.blendColor(lt.r,lt.g,lt.b,bt),A.copy(lt),L=bt),p=B,x=!1}function Ie(B,pe){B.side===St?ee(n.CULL_FACE):ae(n.CULL_FACE);let $=B.side===Lt;pe&&($=!$),Pe($),B.blending===Si&&B.transparent===!1?I(Pn):I(B.blending,B.blendEquation,B.blendSrc,B.blendDst,B.blendEquationAlpha,B.blendSrcAlpha,B.blendDstAlpha,B.blendColor,B.blendAlpha,B.premultipliedAlpha),s.setFunc(B.depthFunc),s.setTest(B.depthTest),s.setMask(B.depthWrite),a.setMask(B.colorWrite);const te=B.stencilWrite;o.setTest(te),te&&(o.setMask(B.stencilWriteMask),o.setFunc(B.stencilFunc,B.stencilRef,B.stencilFuncMask),o.setOp(B.stencilFail,B.stencilZFail,B.stencilZPass)),Fe(B.polygonOffset,B.polygonOffsetFactor,B.polygonOffsetUnits),B.alphaToCoverage===!0?ae(n.SAMPLE_ALPHA_TO_COVERAGE):ee(n.SAMPLE_ALPHA_TO_COVERAGE)}function Pe(B){v!==B&&(B?n.frontFace(n.CW):n.frontFace(n.CCW),v=B)}function Ce(B){B!==fl?(ae(n.CULL_FACE),B!==R&&(B===to?n.cullFace(n.BACK):B===pl?n.cullFace(n.FRONT):n.cullFace(n.FRONT_AND_BACK))):ee(n.CULL_FACE),R=B}function Me(B){B!==U&&(N&&n.lineWidth(B),U=B)}function Fe(B,pe,$){B?(ae(n.POLYGON_OFFSET_FILL),(C!==pe||D!==$)&&(n.polygonOffset(pe,$),C=pe,D=$)):ee(n.POLYGON_OFFSET_FILL)}function Re(B){B?ae(n.SCISSOR_TEST):ee(n.SCISSOR_TEST)}function P(B){B===void 0&&(B=n.TEXTURE0+k-1),H!==B&&(n.activeTexture(B),H=B)}function E(B,pe,$){$===void 0&&(H===null?$=n.TEXTURE0+k-1:$=H);let te=q[$];te===void 0&&(te={type:void 0,texture:void 0},q[$]=te),(te.type!==B||te.texture!==pe)&&(H!==$&&(n.activeTexture($),H=$),n.bindTexture(B,pe||ue[B]),te.type=B,te.texture=pe)}function G(){const B=q[H];B!==void 0&&B.type!==void 0&&(n.bindTexture(B.type,null),B.type=void 0,B.texture=void 0)}function Q(){try{n.compressedTexImage2D(...arguments)}catch(B){console.error("THREE.WebGLState:",B)}}function ie(){try{n.compressedTexImage3D(...arguments)}catch(B){console.error("THREE.WebGLState:",B)}}function Z(){try{n.texSubImage2D(...arguments)}catch(B){console.error("THREE.WebGLState:",B)}}function we(){try{n.texSubImage3D(...arguments)}catch(B){console.error("THREE.WebGLState:",B)}}function ge(){try{n.compressedTexSubImage2D(...arguments)}catch(B){console.error("THREE.WebGLState:",B)}}function Ee(){try{n.compressedTexSubImage3D(...arguments)}catch(B){console.error("THREE.WebGLState:",B)}}function $e(){try{n.texStorage2D(...arguments)}catch(B){console.error("THREE.WebGLState:",B)}}function le(){try{n.texStorage3D(...arguments)}catch(B){console.error("THREE.WebGLState:",B)}}function be(){try{n.texImage2D(...arguments)}catch(B){console.error("THREE.WebGLState:",B)}}function Ue(){try{n.texImage3D(...arguments)}catch(B){console.error("THREE.WebGLState:",B)}}function ze(B){Ae.equals(B)===!1&&(n.scissor(B.x,B.y,B.z,B.w),Ae.copy(B))}function ye(B){K.equals(B)===!1&&(n.viewport(B.x,B.y,B.z,B.w),K.copy(B))}function qe(B,pe){let $=l.get(pe);$===void 0&&($=new WeakMap,l.set(pe,$));let te=$.get(B);te===void 0&&(te=n.getUniformBlockIndex(pe,B.name),$.set(B,te))}function je(B,pe){const te=l.get(pe).get(B);c.get(pe)!==te&&(n.uniformBlockBinding(pe,te,B.__bindingPointIndex),c.set(pe,te))}function at(){n.disable(n.BLEND),n.disable(n.CULL_FACE),n.disable(n.DEPTH_TEST),n.disable(n.POLYGON_OFFSET_FILL),n.disable(n.SCISSOR_TEST),n.disable(n.STENCIL_TEST),n.disable(n.SAMPLE_ALPHA_TO_COVERAGE),n.blendEquation(n.FUNC_ADD),n.blendFunc(n.ONE,n.ZERO),n.blendFuncSeparate(n.ONE,n.ZERO,n.ONE,n.ZERO),n.blendColor(0,0,0,0),n.colorMask(!0,!0,!0,!0),n.clearColor(0,0,0,0),n.depthMask(!0),n.depthFunc(n.LESS),s.setReversed(!1),n.clearDepth(1),n.stencilMask(4294967295),n.stencilFunc(n.ALWAYS,0,4294967295),n.stencilOp(n.KEEP,n.KEEP,n.KEEP),n.clearStencil(0),n.cullFace(n.BACK),n.frontFace(n.CCW),n.polygonOffset(0,0),n.activeTexture(n.TEXTURE0),n.bindFramebuffer(n.FRAMEBUFFER,null),n.bindFramebuffer(n.DRAW_FRAMEBUFFER,null),n.bindFramebuffer(n.READ_FRAMEBUFFER,null),n.useProgram(null),n.lineWidth(1),n.scissor(0,0,n.canvas.width,n.canvas.height),n.viewport(0,0,n.canvas.width,n.canvas.height),d={},H=null,q={},h={},f=new WeakMap,m=[],g=null,_=!1,p=null,u=null,b=null,S=null,M=null,w=null,T=null,A=new ce(0,0,0),L=0,x=!1,v=null,R=null,U=null,C=null,D=null,Ae.set(0,0,n.canvas.width,n.canvas.height),K.set(0,0,n.canvas.width,n.canvas.height),a.reset(),s.reset(),o.reset()}return{buffers:{color:a,depth:s,stencil:o},enable:ae,disable:ee,bindFramebuffer:_e,drawBuffers:de,useProgram:Y,setBlending:I,setMaterial:Ie,setFlipSided:Pe,setCullFace:Ce,setLineWidth:Me,setPolygonOffset:Fe,setScissorTest:Re,activeTexture:P,bindTexture:E,unbindTexture:G,compressedTexImage2D:Q,compressedTexImage3D:ie,texImage2D:be,texImage3D:Ue,updateUBOMapping:qe,uniformBlockBinding:je,texStorage2D:$e,texStorage3D:le,texSubImage2D:Z,texSubImage3D:we,compressedTexSubImage2D:ge,compressedTexSubImage3D:Ee,scissor:ze,viewport:ye,reset:at}}function fm(n,e,t,i,r,a,s){const o=e.has("WEBGL_multisampled_render_to_texture")?e.get("WEBGL_multisampled_render_to_texture"):null,c=typeof navigator>"u"?!1:/OculusBrowser/g.test(navigator.userAgent),l=new Ke,d=new WeakMap;let h;const f=new WeakMap;let m=!1;try{m=typeof OffscreenCanvas<"u"&&new OffscreenCanvas(1,1).getContext("2d")!==null}catch{}function g(P,E){return m?new OffscreenCanvas(P,E):Fr("canvas")}function _(P,E,G){let Q=1;const ie=Re(P);if((ie.width>G||ie.height>G)&&(Q=G/Math.max(ie.width,ie.height)),Q<1)if(typeof HTMLImageElement<"u"&&P instanceof HTMLImageElement||typeof HTMLCanvasElement<"u"&&P instanceof HTMLCanvasElement||typeof ImageBitmap<"u"&&P instanceof ImageBitmap||typeof VideoFrame<"u"&&P instanceof VideoFrame){const Z=Math.floor(Q*ie.width),we=Math.floor(Q*ie.height);h===void 0&&(h=g(Z,we));const ge=E?g(Z,we):h;return ge.width=Z,ge.height=we,ge.getContext("2d").drawImage(P,0,0,Z,we),console.warn("THREE.WebGLRenderer: Texture has been resized from ("+ie.width+"x"+ie.height+") to ("+Z+"x"+we+")."),ge}else return"data"in P&&console.warn("THREE.WebGLRenderer: Image in DataTexture is too big ("+ie.width+"x"+ie.height+")."),P;return P}function p(P){return P.generateMipmaps}function u(P){n.generateMipmap(P)}function b(P){return P.isWebGLCubeRenderTarget?n.TEXTURE_CUBE_MAP:P.isWebGL3DRenderTarget?n.TEXTURE_3D:P.isWebGLArrayRenderTarget||P.isCompressedArrayTexture?n.TEXTURE_2D_ARRAY:n.TEXTURE_2D}function S(P,E,G,Q,ie=!1){if(P!==null){if(n[P]!==void 0)return n[P];console.warn("THREE.WebGLRenderer: Attempt to use non-existing WebGL internal format '"+P+"'")}let Z=E;if(E===n.RED&&(G===n.FLOAT&&(Z=n.R32F),G===n.HALF_FLOAT&&(Z=n.R16F),G===n.UNSIGNED_BYTE&&(Z=n.R8)),E===n.RED_INTEGER&&(G===n.UNSIGNED_BYTE&&(Z=n.R8UI),G===n.UNSIGNED_SHORT&&(Z=n.R16UI),G===n.UNSIGNED_INT&&(Z=n.R32UI),G===n.BYTE&&(Z=n.R8I),G===n.SHORT&&(Z=n.R16I),G===n.INT&&(Z=n.R32I)),E===n.RG&&(G===n.FLOAT&&(Z=n.RG32F),G===n.HALF_FLOAT&&(Z=n.RG16F),G===n.UNSIGNED_BYTE&&(Z=n.RG8)),E===n.RG_INTEGER&&(G===n.UNSIGNED_BYTE&&(Z=n.RG8UI),G===n.UNSIGNED_SHORT&&(Z=n.RG16UI),G===n.UNSIGNED_INT&&(Z=n.RG32UI),G===n.BYTE&&(Z=n.RG8I),G===n.SHORT&&(Z=n.RG16I),G===n.INT&&(Z=n.RG32I)),E===n.RGB_INTEGER&&(G===n.UNSIGNED_BYTE&&(Z=n.RGB8UI),G===n.UNSIGNED_SHORT&&(Z=n.RGB16UI),G===n.UNSIGNED_INT&&(Z=n.RGB32UI),G===n.BYTE&&(Z=n.RGB8I),G===n.SHORT&&(Z=n.RGB16I),G===n.INT&&(Z=n.RGB32I)),E===n.RGBA_INTEGER&&(G===n.UNSIGNED_BYTE&&(Z=n.RGBA8UI),G===n.UNSIGNED_SHORT&&(Z=n.RGBA16UI),G===n.UNSIGNED_INT&&(Z=n.RGBA32UI),G===n.BYTE&&(Z=n.RGBA8I),G===n.SHORT&&(Z=n.RGBA16I),G===n.INT&&(Z=n.RGBA32I)),E===n.RGB&&G===n.UNSIGNED_INT_5_9_9_9_REV&&(Z=n.RGB9_E5),E===n.RGBA){const we=ie?Nr:Qe.getTransfer(Q);G===n.FLOAT&&(Z=n.RGBA32F),G===n.HALF_FLOAT&&(Z=n.RGBA16F),G===n.UNSIGNED_BYTE&&(Z=we===rt?n.SRGB8_ALPHA8:n.RGBA8),G===n.UNSIGNED_SHORT_4_4_4_4&&(Z=n.RGBA4),G===n.UNSIGNED_SHORT_5_5_5_1&&(Z=n.RGB5_A1)}return(Z===n.R16F||Z===n.R32F||Z===n.RG16F||Z===n.RG32F||Z===n.RGBA16F||Z===n.RGBA32F)&&e.get("EXT_color_buffer_float"),Z}function M(P,E){let G;return P?E===null||E===Qn||E===Ai?G=n.DEPTH24_STENCIL8:E===pn?G=n.DEPTH32F_STENCIL8:E===Xi&&(G=n.DEPTH24_STENCIL8,console.warn("DepthTexture: 16 bit depth attachment is not supported with stencil. Using 24-bit attachment.")):E===null||E===Qn||E===Ai?G=n.DEPTH_COMPONENT24:E===pn?G=n.DEPTH_COMPONENT32F:E===Xi&&(G=n.DEPTH_COMPONENT16),G}function w(P,E){return p(P)===!0||P.isFramebufferTexture&&P.minFilter!==Jt&&P.minFilter!==tn?Math.log2(Math.max(E.width,E.height))+1:P.mipmaps!==void 0&&P.mipmaps.length>0?P.mipmaps.length:P.isCompressedTexture&&Array.isArray(P.image)?E.mipmaps.length:1}function T(P){const E=P.target;E.removeEventListener("dispose",T),L(E),E.isVideoTexture&&d.delete(E)}function A(P){const E=P.target;E.removeEventListener("dispose",A),v(E)}function L(P){const E=i.get(P);if(E.__webglInit===void 0)return;const G=P.source,Q=f.get(G);if(Q){const ie=Q[E.__cacheKey];ie.usedTimes--,ie.usedTimes===0&&x(P),Object.keys(Q).length===0&&f.delete(G)}i.remove(P)}function x(P){const E=i.get(P);n.deleteTexture(E.__webglTexture);const G=P.source,Q=f.get(G);delete Q[E.__cacheKey],s.memory.textures--}function v(P){const E=i.get(P);if(P.depthTexture&&(P.depthTexture.dispose(),i.remove(P.depthTexture)),P.isWebGLCubeRenderTarget)for(let Q=0;Q<6;Q++){if(Array.isArray(E.__webglFramebuffer[Q]))for(let ie=0;ie<E.__webglFramebuffer[Q].length;ie++)n.deleteFramebuffer(E.__webglFramebuffer[Q][ie]);else n.deleteFramebuffer(E.__webglFramebuffer[Q]);E.__webglDepthbuffer&&n.deleteRenderbuffer(E.__webglDepthbuffer[Q])}else{if(Array.isArray(E.__webglFramebuffer))for(let Q=0;Q<E.__webglFramebuffer.length;Q++)n.deleteFramebuffer(E.__webglFramebuffer[Q]);else n.deleteFramebuffer(E.__webglFramebuffer);if(E.__webglDepthbuffer&&n.deleteRenderbuffer(E.__webglDepthbuffer),E.__webglMultisampledFramebuffer&&n.deleteFramebuffer(E.__webglMultisampledFramebuffer),E.__webglColorRenderbuffer)for(let Q=0;Q<E.__webglColorRenderbuffer.length;Q++)E.__webglColorRenderbuffer[Q]&&n.deleteRenderbuffer(E.__webglColorRenderbuffer[Q]);E.__webglDepthRenderbuffer&&n.deleteRenderbuffer(E.__webglDepthRenderbuffer)}const G=P.textures;for(let Q=0,ie=G.length;Q<ie;Q++){const Z=i.get(G[Q]);Z.__webglTexture&&(n.deleteTexture(Z.__webglTexture),s.memory.textures--),i.remove(G[Q])}i.remove(P)}let R=0;function U(){R=0}function C(){const P=R;return P>=r.maxTextures&&console.warn("THREE.WebGLTextures: Trying to use "+P+" texture units while this GPU supports only "+r.maxTextures),R+=1,P}function D(P){const E=[];return E.push(P.wrapS),E.push(P.wrapT),E.push(P.wrapR||0),E.push(P.magFilter),E.push(P.minFilter),E.push(P.anisotropy),E.push(P.internalFormat),E.push(P.format),E.push(P.type),E.push(P.generateMipmaps),E.push(P.premultiplyAlpha),E.push(P.flipY),E.push(P.unpackAlignment),E.push(P.colorSpace),E.join()}function k(P,E){const G=i.get(P);if(P.isVideoTexture&&Me(P),P.isRenderTargetTexture===!1&&P.version>0&&G.__version!==P.version){const Q=P.image;if(Q===null)console.warn("THREE.WebGLRenderer: Texture marked for update but no image data found.");else if(Q.complete===!1)console.warn("THREE.WebGLRenderer: Texture marked for update but image is incomplete");else{K(G,P,E);return}}t.bindTexture(n.TEXTURE_2D,G.__webglTexture,n.TEXTURE0+E)}function N(P,E){const G=i.get(P);if(P.version>0&&G.__version!==P.version){K(G,P,E);return}t.bindTexture(n.TEXTURE_2D_ARRAY,G.__webglTexture,n.TEXTURE0+E)}function O(P,E){const G=i.get(P);if(P.version>0&&G.__version!==P.version){K(G,P,E);return}t.bindTexture(n.TEXTURE_3D,G.__webglTexture,n.TEXTURE0+E)}function z(P,E){const G=i.get(P);if(P.version>0&&G.__version!==P.version){ne(G,P,E);return}t.bindTexture(n.TEXTURE_CUBE_MAP,G.__webglTexture,n.TEXTURE0+E)}const H={[Ga]:n.REPEAT,[$n]:n.CLAMP_TO_EDGE,[Wa]:n.MIRRORED_REPEAT},q={[Jt]:n.NEAREST,[Hl]:n.NEAREST_MIPMAP_NEAREST,[tr]:n.NEAREST_MIPMAP_LINEAR,[tn]:n.LINEAR,[$r]:n.LINEAR_MIPMAP_NEAREST,[Yn]:n.LINEAR_MIPMAP_LINEAR},J={[Kl]:n.NEVER,[Ql]:n.ALWAYS,[ql]:n.LESS,[Dc]:n.LEQUAL,[$l]:n.EQUAL,[Jl]:n.GEQUAL,[Yl]:n.GREATER,[Zl]:n.NOTEQUAL};function fe(P,E){if(E.type===pn&&e.has("OES_texture_float_linear")===!1&&(E.magFilter===tn||E.magFilter===$r||E.magFilter===tr||E.magFilter===Yn||E.minFilter===tn||E.minFilter===$r||E.minFilter===tr||E.minFilter===Yn)&&console.warn("THREE.WebGLRenderer: Unable to use linear filtering with floating point textures. OES_texture_float_linear not supported on this device."),n.texParameteri(P,n.TEXTURE_WRAP_S,H[E.wrapS]),n.texParameteri(P,n.TEXTURE_WRAP_T,H[E.wrapT]),(P===n.TEXTURE_3D||P===n.TEXTURE_2D_ARRAY)&&n.texParameteri(P,n.TEXTURE_WRAP_R,H[E.wrapR]),n.texParameteri(P,n.TEXTURE_MAG_FILTER,q[E.magFilter]),n.texParameteri(P,n.TEXTURE_MIN_FILTER,q[E.minFilter]),E.compareFunction&&(n.texParameteri(P,n.TEXTURE_COMPARE_MODE,n.COMPARE_REF_TO_TEXTURE),n.texParameteri(P,n.TEXTURE_COMPARE_FUNC,J[E.compareFunction])),e.has("EXT_texture_filter_anisotropic")===!0){if(E.magFilter===Jt||E.minFilter!==tr&&E.minFilter!==Yn||E.type===pn&&e.has("OES_texture_float_linear")===!1)return;if(E.anisotropy>1||i.get(E).__currentAnisotropy){const G=e.get("EXT_texture_filter_anisotropic");n.texParameterf(P,G.TEXTURE_MAX_ANISOTROPY_EXT,Math.min(E.anisotropy,r.getMaxAnisotropy())),i.get(E).__currentAnisotropy=E.anisotropy}}}function Ae(P,E){let G=!1;P.__webglInit===void 0&&(P.__webglInit=!0,E.addEventListener("dispose",T));const Q=E.source;let ie=f.get(Q);ie===void 0&&(ie={},f.set(Q,ie));const Z=D(E);if(Z!==P.__cacheKey){ie[Z]===void 0&&(ie[Z]={texture:n.createTexture(),usedTimes:0},s.memory.textures++,G=!0),ie[Z].usedTimes++;const we=ie[P.__cacheKey];we!==void 0&&(ie[P.__cacheKey].usedTimes--,we.usedTimes===0&&x(E)),P.__cacheKey=Z,P.__webglTexture=ie[Z].texture}return G}function K(P,E,G){let Q=n.TEXTURE_2D;(E.isDataArrayTexture||E.isCompressedArrayTexture)&&(Q=n.TEXTURE_2D_ARRAY),E.isData3DTexture&&(Q=n.TEXTURE_3D);const ie=Ae(P,E),Z=E.source;t.bindTexture(Q,P.__webglTexture,n.TEXTURE0+G);const we=i.get(Z);if(Z.version!==we.__version||ie===!0){t.activeTexture(n.TEXTURE0+G);const ge=Qe.getPrimaries(Qe.workingColorSpace),Ee=E.colorSpace===Rn?null:Qe.getPrimaries(E.colorSpace),$e=E.colorSpace===Rn||ge===Ee?n.NONE:n.BROWSER_DEFAULT_WEBGL;n.pixelStorei(n.UNPACK_FLIP_Y_WEBGL,E.flipY),n.pixelStorei(n.UNPACK_PREMULTIPLY_ALPHA_WEBGL,E.premultiplyAlpha),n.pixelStorei(n.UNPACK_ALIGNMENT,E.unpackAlignment),n.pixelStorei(n.UNPACK_COLORSPACE_CONVERSION_WEBGL,$e);let le=_(E.image,!1,r.maxTextureSize);le=Fe(E,le);const be=a.convert(E.format,E.colorSpace),Ue=a.convert(E.type);let ze=S(E.internalFormat,be,Ue,E.colorSpace,E.isVideoTexture);fe(Q,E);let ye;const qe=E.mipmaps,je=E.isVideoTexture!==!0,at=we.__version===void 0||ie===!0,B=Z.dataReady,pe=w(E,le);if(E.isDepthTexture)ze=M(E.format===Ri,E.type),at&&(je?t.texStorage2D(n.TEXTURE_2D,1,ze,le.width,le.height):t.texImage2D(n.TEXTURE_2D,0,ze,le.width,le.height,0,be,Ue,null));else if(E.isDataTexture)if(qe.length>0){je&&at&&t.texStorage2D(n.TEXTURE_2D,pe,ze,qe[0].width,qe[0].height);for(let $=0,te=qe.length;$<te;$++)ye=qe[$],je?B&&t.texSubImage2D(n.TEXTURE_2D,$,0,0,ye.width,ye.height,be,Ue,ye.data):t.texImage2D(n.TEXTURE_2D,$,ze,ye.width,ye.height,0,be,Ue,ye.data);E.generateMipmaps=!1}else je?(at&&t.texStorage2D(n.TEXTURE_2D,pe,ze,le.width,le.height),B&&t.texSubImage2D(n.TEXTURE_2D,0,0,0,le.width,le.height,be,Ue,le.data)):t.texImage2D(n.TEXTURE_2D,0,ze,le.width,le.height,0,be,Ue,le.data);else if(E.isCompressedTexture)if(E.isCompressedArrayTexture){je&&at&&t.texStorage3D(n.TEXTURE_2D_ARRAY,pe,ze,qe[0].width,qe[0].height,le.depth);for(let $=0,te=qe.length;$<te;$++)if(ye=qe[$],E.format!==Zt)if(be!==null)if(je){if(B)if(E.layerUpdates.size>0){const xe=zo(ye.width,ye.height,E.format,E.type);for(const ve of E.layerUpdates){const Oe=ye.data.subarray(ve*xe/ye.data.BYTES_PER_ELEMENT,(ve+1)*xe/ye.data.BYTES_PER_ELEMENT);t.compressedTexSubImage3D(n.TEXTURE_2D_ARRAY,$,0,0,ve,ye.width,ye.height,1,be,Oe)}E.clearLayerUpdates()}else t.compressedTexSubImage3D(n.TEXTURE_2D_ARRAY,$,0,0,0,ye.width,ye.height,le.depth,be,ye.data)}else t.compressedTexImage3D(n.TEXTURE_2D_ARRAY,$,ze,ye.width,ye.height,le.depth,0,ye.data,0,0);else console.warn("THREE.WebGLRenderer: Attempt to load unsupported compressed texture format in .uploadTexture()");else je?B&&t.texSubImage3D(n.TEXTURE_2D_ARRAY,$,0,0,0,ye.width,ye.height,le.depth,be,Ue,ye.data):t.texImage3D(n.TEXTURE_2D_ARRAY,$,ze,ye.width,ye.height,le.depth,0,be,Ue,ye.data)}else{je&&at&&t.texStorage2D(n.TEXTURE_2D,pe,ze,qe[0].width,qe[0].height);for(let $=0,te=qe.length;$<te;$++)ye=qe[$],E.format!==Zt?be!==null?je?B&&t.compressedTexSubImage2D(n.TEXTURE_2D,$,0,0,ye.width,ye.height,be,ye.data):t.compressedTexImage2D(n.TEXTURE_2D,$,ze,ye.width,ye.height,0,ye.data):console.warn("THREE.WebGLRenderer: Attempt to load unsupported compressed texture format in .uploadTexture()"):je?B&&t.texSubImage2D(n.TEXTURE_2D,$,0,0,ye.width,ye.height,be,Ue,ye.data):t.texImage2D(n.TEXTURE_2D,$,ze,ye.width,ye.height,0,be,Ue,ye.data)}else if(E.isDataArrayTexture)if(je){if(at&&t.texStorage3D(n.TEXTURE_2D_ARRAY,pe,ze,le.width,le.height,le.depth),B)if(E.layerUpdates.size>0){const $=zo(le.width,le.height,E.format,E.type);for(const te of E.layerUpdates){const xe=le.data.subarray(te*$/le.data.BYTES_PER_ELEMENT,(te+1)*$/le.data.BYTES_PER_ELEMENT);t.texSubImage3D(n.TEXTURE_2D_ARRAY,0,0,0,te,le.width,le.height,1,be,Ue,xe)}E.clearLayerUpdates()}else t.texSubImage3D(n.TEXTURE_2D_ARRAY,0,0,0,0,le.width,le.height,le.depth,be,Ue,le.data)}else t.texImage3D(n.TEXTURE_2D_ARRAY,0,ze,le.width,le.height,le.depth,0,be,Ue,le.data);else if(E.isData3DTexture)je?(at&&t.texStorage3D(n.TEXTURE_3D,pe,ze,le.width,le.height,le.depth),B&&t.texSubImage3D(n.TEXTURE_3D,0,0,0,0,le.width,le.height,le.depth,be,Ue,le.data)):t.texImage3D(n.TEXTURE_3D,0,ze,le.width,le.height,le.depth,0,be,Ue,le.data);else if(E.isFramebufferTexture){if(at)if(je)t.texStorage2D(n.TEXTURE_2D,pe,ze,le.width,le.height);else{let $=le.width,te=le.height;for(let xe=0;xe<pe;xe++)t.texImage2D(n.TEXTURE_2D,xe,ze,$,te,0,be,Ue,null),$>>=1,te>>=1}}else if(qe.length>0){if(je&&at){const $=Re(qe[0]);t.texStorage2D(n.TEXTURE_2D,pe,ze,$.width,$.height)}for(let $=0,te=qe.length;$<te;$++)ye=qe[$],je?B&&t.texSubImage2D(n.TEXTURE_2D,$,0,0,be,Ue,ye):t.texImage2D(n.TEXTURE_2D,$,ze,be,Ue,ye);E.generateMipmaps=!1}else if(je){if(at){const $=Re(le);t.texStorage2D(n.TEXTURE_2D,pe,ze,$.width,$.height)}B&&t.texSubImage2D(n.TEXTURE_2D,0,0,0,be,Ue,le)}else t.texImage2D(n.TEXTURE_2D,0,ze,be,Ue,le);p(E)&&u(Q),we.__version=Z.version,E.onUpdate&&E.onUpdate(E)}P.__version=E.version}function ne(P,E,G){if(E.image.length!==6)return;const Q=Ae(P,E),ie=E.source;t.bindTexture(n.TEXTURE_CUBE_MAP,P.__webglTexture,n.TEXTURE0+G);const Z=i.get(ie);if(ie.version!==Z.__version||Q===!0){t.activeTexture(n.TEXTURE0+G);const we=Qe.getPrimaries(Qe.workingColorSpace),ge=E.colorSpace===Rn?null:Qe.getPrimaries(E.colorSpace),Ee=E.colorSpace===Rn||we===ge?n.NONE:n.BROWSER_DEFAULT_WEBGL;n.pixelStorei(n.UNPACK_FLIP_Y_WEBGL,E.flipY),n.pixelStorei(n.UNPACK_PREMULTIPLY_ALPHA_WEBGL,E.premultiplyAlpha),n.pixelStorei(n.UNPACK_ALIGNMENT,E.unpackAlignment),n.pixelStorei(n.UNPACK_COLORSPACE_CONVERSION_WEBGL,Ee);const $e=E.isCompressedTexture||E.image[0].isCompressedTexture,le=E.image[0]&&E.image[0].isDataTexture,be=[];for(let te=0;te<6;te++)!$e&&!le?be[te]=_(E.image[te],!0,r.maxCubemapSize):be[te]=le?E.image[te].image:E.image[te],be[te]=Fe(E,be[te]);const Ue=be[0],ze=a.convert(E.format,E.colorSpace),ye=a.convert(E.type),qe=S(E.internalFormat,ze,ye,E.colorSpace),je=E.isVideoTexture!==!0,at=Z.__version===void 0||Q===!0,B=ie.dataReady;let pe=w(E,Ue);fe(n.TEXTURE_CUBE_MAP,E);let $;if($e){je&&at&&t.texStorage2D(n.TEXTURE_CUBE_MAP,pe,qe,Ue.width,Ue.height);for(let te=0;te<6;te++){$=be[te].mipmaps;for(let xe=0;xe<$.length;xe++){const ve=$[xe];E.format!==Zt?ze!==null?je?B&&t.compressedTexSubImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+te,xe,0,0,ve.width,ve.height,ze,ve.data):t.compressedTexImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+te,xe,qe,ve.width,ve.height,0,ve.data):console.warn("THREE.WebGLRenderer: Attempt to load unsupported compressed texture format in .setTextureCube()"):je?B&&t.texSubImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+te,xe,0,0,ve.width,ve.height,ze,ye,ve.data):t.texImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+te,xe,qe,ve.width,ve.height,0,ze,ye,ve.data)}}}else{if($=E.mipmaps,je&&at){$.length>0&&pe++;const te=Re(be[0]);t.texStorage2D(n.TEXTURE_CUBE_MAP,pe,qe,te.width,te.height)}for(let te=0;te<6;te++)if(le){je?B&&t.texSubImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+te,0,0,0,be[te].width,be[te].height,ze,ye,be[te].data):t.texImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+te,0,qe,be[te].width,be[te].height,0,ze,ye,be[te].data);for(let xe=0;xe<$.length;xe++){const Oe=$[xe].image[te].image;je?B&&t.texSubImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+te,xe+1,0,0,Oe.width,Oe.height,ze,ye,Oe.data):t.texImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+te,xe+1,qe,Oe.width,Oe.height,0,ze,ye,Oe.data)}}else{je?B&&t.texSubImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+te,0,0,0,ze,ye,be[te]):t.texImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+te,0,qe,ze,ye,be[te]);for(let xe=0;xe<$.length;xe++){const ve=$[xe];je?B&&t.texSubImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+te,xe+1,0,0,ze,ye,ve.image[te]):t.texImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+te,xe+1,qe,ze,ye,ve.image[te])}}}p(E)&&u(n.TEXTURE_CUBE_MAP),Z.__version=ie.version,E.onUpdate&&E.onUpdate(E)}P.__version=E.version}function ue(P,E,G,Q,ie,Z){const we=a.convert(G.format,G.colorSpace),ge=a.convert(G.type),Ee=S(G.internalFormat,we,ge,G.colorSpace),$e=i.get(E),le=i.get(G);if(le.__renderTarget=E,!$e.__hasExternalTextures){const be=Math.max(1,E.width>>Z),Ue=Math.max(1,E.height>>Z);ie===n.TEXTURE_3D||ie===n.TEXTURE_2D_ARRAY?t.texImage3D(ie,Z,Ee,be,Ue,E.depth,0,we,ge,null):t.texImage2D(ie,Z,Ee,be,Ue,0,we,ge,null)}t.bindFramebuffer(n.FRAMEBUFFER,P),Ce(E)?o.framebufferTexture2DMultisampleEXT(n.FRAMEBUFFER,Q,ie,le.__webglTexture,0,Pe(E)):(ie===n.TEXTURE_2D||ie>=n.TEXTURE_CUBE_MAP_POSITIVE_X&&ie<=n.TEXTURE_CUBE_MAP_NEGATIVE_Z)&&n.framebufferTexture2D(n.FRAMEBUFFER,Q,ie,le.__webglTexture,Z),t.bindFramebuffer(n.FRAMEBUFFER,null)}function ae(P,E,G){if(n.bindRenderbuffer(n.RENDERBUFFER,P),E.depthBuffer){const Q=E.depthTexture,ie=Q&&Q.isDepthTexture?Q.type:null,Z=M(E.stencilBuffer,ie),we=E.stencilBuffer?n.DEPTH_STENCIL_ATTACHMENT:n.DEPTH_ATTACHMENT,ge=Pe(E);Ce(E)?o.renderbufferStorageMultisampleEXT(n.RENDERBUFFER,ge,Z,E.width,E.height):G?n.renderbufferStorageMultisample(n.RENDERBUFFER,ge,Z,E.width,E.height):n.renderbufferStorage(n.RENDERBUFFER,Z,E.width,E.height),n.framebufferRenderbuffer(n.FRAMEBUFFER,we,n.RENDERBUFFER,P)}else{const Q=E.textures;for(let ie=0;ie<Q.length;ie++){const Z=Q[ie],we=a.convert(Z.format,Z.colorSpace),ge=a.convert(Z.type),Ee=S(Z.internalFormat,we,ge,Z.colorSpace),$e=Pe(E);G&&Ce(E)===!1?n.renderbufferStorageMultisample(n.RENDERBUFFER,$e,Ee,E.width,E.height):Ce(E)?o.renderbufferStorageMultisampleEXT(n.RENDERBUFFER,$e,Ee,E.width,E.height):n.renderbufferStorage(n.RENDERBUFFER,Ee,E.width,E.height)}}n.bindRenderbuffer(n.RENDERBUFFER,null)}function ee(P,E){if(E&&E.isWebGLCubeRenderTarget)throw new Error("Depth Texture with cube render targets is not supported");if(t.bindFramebuffer(n.FRAMEBUFFER,P),!(E.depthTexture&&E.depthTexture.isDepthTexture))throw new Error("renderTarget.depthTexture must be an instance of THREE.DepthTexture");const Q=i.get(E.depthTexture);Q.__renderTarget=E,(!Q.__webglTexture||E.depthTexture.image.width!==E.width||E.depthTexture.image.height!==E.height)&&(E.depthTexture.image.width=E.width,E.depthTexture.image.height=E.height,E.depthTexture.needsUpdate=!0),k(E.depthTexture,0);const ie=Q.__webglTexture,Z=Pe(E);if(E.depthTexture.format===Ei)Ce(E)?o.framebufferTexture2DMultisampleEXT(n.FRAMEBUFFER,n.DEPTH_ATTACHMENT,n.TEXTURE_2D,ie,0,Z):n.framebufferTexture2D(n.FRAMEBUFFER,n.DEPTH_ATTACHMENT,n.TEXTURE_2D,ie,0);else if(E.depthTexture.format===Ri)Ce(E)?o.framebufferTexture2DMultisampleEXT(n.FRAMEBUFFER,n.DEPTH_STENCIL_ATTACHMENT,n.TEXTURE_2D,ie,0,Z):n.framebufferTexture2D(n.FRAMEBUFFER,n.DEPTH_STENCIL_ATTACHMENT,n.TEXTURE_2D,ie,0);else throw new Error("Unknown depthTexture format")}function _e(P){const E=i.get(P),G=P.isWebGLCubeRenderTarget===!0;if(E.__boundDepthTexture!==P.depthTexture){const Q=P.depthTexture;if(E.__depthDisposeCallback&&E.__depthDisposeCallback(),Q){const ie=()=>{delete E.__boundDepthTexture,delete E.__depthDisposeCallback,Q.removeEventListener("dispose",ie)};Q.addEventListener("dispose",ie),E.__depthDisposeCallback=ie}E.__boundDepthTexture=Q}if(P.depthTexture&&!E.__autoAllocateDepthBuffer){if(G)throw new Error("target.depthTexture not supported in Cube render targets");ee(E.__webglFramebuffer,P)}else if(G){E.__webglDepthbuffer=[];for(let Q=0;Q<6;Q++)if(t.bindFramebuffer(n.FRAMEBUFFER,E.__webglFramebuffer[Q]),E.__webglDepthbuffer[Q]===void 0)E.__webglDepthbuffer[Q]=n.createRenderbuffer(),ae(E.__webglDepthbuffer[Q],P,!1);else{const ie=P.stencilBuffer?n.DEPTH_STENCIL_ATTACHMENT:n.DEPTH_ATTACHMENT,Z=E.__webglDepthbuffer[Q];n.bindRenderbuffer(n.RENDERBUFFER,Z),n.framebufferRenderbuffer(n.FRAMEBUFFER,ie,n.RENDERBUFFER,Z)}}else if(t.bindFramebuffer(n.FRAMEBUFFER,E.__webglFramebuffer),E.__webglDepthbuffer===void 0)E.__webglDepthbuffer=n.createRenderbuffer(),ae(E.__webglDepthbuffer,P,!1);else{const Q=P.stencilBuffer?n.DEPTH_STENCIL_ATTACHMENT:n.DEPTH_ATTACHMENT,ie=E.__webglDepthbuffer;n.bindRenderbuffer(n.RENDERBUFFER,ie),n.framebufferRenderbuffer(n.FRAMEBUFFER,Q,n.RENDERBUFFER,ie)}t.bindFramebuffer(n.FRAMEBUFFER,null)}function de(P,E,G){const Q=i.get(P);E!==void 0&&ue(Q.__webglFramebuffer,P,P.texture,n.COLOR_ATTACHMENT0,n.TEXTURE_2D,0),G!==void 0&&_e(P)}function Y(P){const E=P.texture,G=i.get(P),Q=i.get(E);P.addEventListener("dispose",A);const ie=P.textures,Z=P.isWebGLCubeRenderTarget===!0,we=ie.length>1;if(we||(Q.__webglTexture===void 0&&(Q.__webglTexture=n.createTexture()),Q.__version=E.version,s.memory.textures++),Z){G.__webglFramebuffer=[];for(let ge=0;ge<6;ge++)if(E.mipmaps&&E.mipmaps.length>0){G.__webglFramebuffer[ge]=[];for(let Ee=0;Ee<E.mipmaps.length;Ee++)G.__webglFramebuffer[ge][Ee]=n.createFramebuffer()}else G.__webglFramebuffer[ge]=n.createFramebuffer()}else{if(E.mipmaps&&E.mipmaps.length>0){G.__webglFramebuffer=[];for(let ge=0;ge<E.mipmaps.length;ge++)G.__webglFramebuffer[ge]=n.createFramebuffer()}else G.__webglFramebuffer=n.createFramebuffer();if(we)for(let ge=0,Ee=ie.length;ge<Ee;ge++){const $e=i.get(ie[ge]);$e.__webglTexture===void 0&&($e.__webglTexture=n.createTexture(),s.memory.textures++)}if(P.samples>0&&Ce(P)===!1){G.__webglMultisampledFramebuffer=n.createFramebuffer(),G.__webglColorRenderbuffer=[],t.bindFramebuffer(n.FRAMEBUFFER,G.__webglMultisampledFramebuffer);for(let ge=0;ge<ie.length;ge++){const Ee=ie[ge];G.__webglColorRenderbuffer[ge]=n.createRenderbuffer(),n.bindRenderbuffer(n.RENDERBUFFER,G.__webglColorRenderbuffer[ge]);const $e=a.convert(Ee.format,Ee.colorSpace),le=a.convert(Ee.type),be=S(Ee.internalFormat,$e,le,Ee.colorSpace,P.isXRRenderTarget===!0),Ue=Pe(P);n.renderbufferStorageMultisample(n.RENDERBUFFER,Ue,be,P.width,P.height),n.framebufferRenderbuffer(n.FRAMEBUFFER,n.COLOR_ATTACHMENT0+ge,n.RENDERBUFFER,G.__webglColorRenderbuffer[ge])}n.bindRenderbuffer(n.RENDERBUFFER,null),P.depthBuffer&&(G.__webglDepthRenderbuffer=n.createRenderbuffer(),ae(G.__webglDepthRenderbuffer,P,!0)),t.bindFramebuffer(n.FRAMEBUFFER,null)}}if(Z){t.bindTexture(n.TEXTURE_CUBE_MAP,Q.__webglTexture),fe(n.TEXTURE_CUBE_MAP,E);for(let ge=0;ge<6;ge++)if(E.mipmaps&&E.mipmaps.length>0)for(let Ee=0;Ee<E.mipmaps.length;Ee++)ue(G.__webglFramebuffer[ge][Ee],P,E,n.COLOR_ATTACHMENT0,n.TEXTURE_CUBE_MAP_POSITIVE_X+ge,Ee);else ue(G.__webglFramebuffer[ge],P,E,n.COLOR_ATTACHMENT0,n.TEXTURE_CUBE_MAP_POSITIVE_X+ge,0);p(E)&&u(n.TEXTURE_CUBE_MAP),t.unbindTexture()}else if(we){for(let ge=0,Ee=ie.length;ge<Ee;ge++){const $e=ie[ge],le=i.get($e);t.bindTexture(n.TEXTURE_2D,le.__webglTexture),fe(n.TEXTURE_2D,$e),ue(G.__webglFramebuffer,P,$e,n.COLOR_ATTACHMENT0+ge,n.TEXTURE_2D,0),p($e)&&u(n.TEXTURE_2D)}t.unbindTexture()}else{let ge=n.TEXTURE_2D;if((P.isWebGL3DRenderTarget||P.isWebGLArrayRenderTarget)&&(ge=P.isWebGL3DRenderTarget?n.TEXTURE_3D:n.TEXTURE_2D_ARRAY),t.bindTexture(ge,Q.__webglTexture),fe(ge,E),E.mipmaps&&E.mipmaps.length>0)for(let Ee=0;Ee<E.mipmaps.length;Ee++)ue(G.__webglFramebuffer[Ee],P,E,n.COLOR_ATTACHMENT0,ge,Ee);else ue(G.__webglFramebuffer,P,E,n.COLOR_ATTACHMENT0,ge,0);p(E)&&u(ge),t.unbindTexture()}P.depthBuffer&&_e(P)}function re(P){const E=P.textures;for(let G=0,Q=E.length;G<Q;G++){const ie=E[G];if(p(ie)){const Z=b(P),we=i.get(ie).__webglTexture;t.bindTexture(Z,we),u(Z),t.unbindTexture()}}}const oe=[],I=[];function Ie(P){if(P.samples>0){if(Ce(P)===!1){const E=P.textures,G=P.width,Q=P.height;let ie=n.COLOR_BUFFER_BIT;const Z=P.stencilBuffer?n.DEPTH_STENCIL_ATTACHMENT:n.DEPTH_ATTACHMENT,we=i.get(P),ge=E.length>1;if(ge)for(let Ee=0;Ee<E.length;Ee++)t.bindFramebuffer(n.FRAMEBUFFER,we.__webglMultisampledFramebuffer),n.framebufferRenderbuffer(n.FRAMEBUFFER,n.COLOR_ATTACHMENT0+Ee,n.RENDERBUFFER,null),t.bindFramebuffer(n.FRAMEBUFFER,we.__webglFramebuffer),n.framebufferTexture2D(n.DRAW_FRAMEBUFFER,n.COLOR_ATTACHMENT0+Ee,n.TEXTURE_2D,null,0);t.bindFramebuffer(n.READ_FRAMEBUFFER,we.__webglMultisampledFramebuffer),t.bindFramebuffer(n.DRAW_FRAMEBUFFER,we.__webglFramebuffer);for(let Ee=0;Ee<E.length;Ee++){if(P.resolveDepthBuffer&&(P.depthBuffer&&(ie|=n.DEPTH_BUFFER_BIT),P.stencilBuffer&&P.resolveStencilBuffer&&(ie|=n.STENCIL_BUFFER_BIT)),ge){n.framebufferRenderbuffer(n.READ_FRAMEBUFFER,n.COLOR_ATTACHMENT0,n.RENDERBUFFER,we.__webglColorRenderbuffer[Ee]);const $e=i.get(E[Ee]).__webglTexture;n.framebufferTexture2D(n.DRAW_FRAMEBUFFER,n.COLOR_ATTACHMENT0,n.TEXTURE_2D,$e,0)}n.blitFramebuffer(0,0,G,Q,0,0,G,Q,ie,n.NEAREST),c===!0&&(oe.length=0,I.length=0,oe.push(n.COLOR_ATTACHMENT0+Ee),P.depthBuffer&&P.resolveDepthBuffer===!1&&(oe.push(Z),I.push(Z),n.invalidateFramebuffer(n.DRAW_FRAMEBUFFER,I)),n.invalidateFramebuffer(n.READ_FRAMEBUFFER,oe))}if(t.bindFramebuffer(n.READ_FRAMEBUFFER,null),t.bindFramebuffer(n.DRAW_FRAMEBUFFER,null),ge)for(let Ee=0;Ee<E.length;Ee++){t.bindFramebuffer(n.FRAMEBUFFER,we.__webglMultisampledFramebuffer),n.framebufferRenderbuffer(n.FRAMEBUFFER,n.COLOR_ATTACHMENT0+Ee,n.RENDERBUFFER,we.__webglColorRenderbuffer[Ee]);const $e=i.get(E[Ee]).__webglTexture;t.bindFramebuffer(n.FRAMEBUFFER,we.__webglFramebuffer),n.framebufferTexture2D(n.DRAW_FRAMEBUFFER,n.COLOR_ATTACHMENT0+Ee,n.TEXTURE_2D,$e,0)}t.bindFramebuffer(n.DRAW_FRAMEBUFFER,we.__webglMultisampledFramebuffer)}else if(P.depthBuffer&&P.resolveDepthBuffer===!1&&c){const E=P.stencilBuffer?n.DEPTH_STENCIL_ATTACHMENT:n.DEPTH_ATTACHMENT;n.invalidateFramebuffer(n.DRAW_FRAMEBUFFER,[E])}}}function Pe(P){return Math.min(r.maxSamples,P.samples)}function Ce(P){const E=i.get(P);return P.samples>0&&e.has("WEBGL_multisampled_render_to_texture")===!0&&E.__useRenderToTexture!==!1}function Me(P){const E=s.render.frame;d.get(P)!==E&&(d.set(P,E),P.update())}function Fe(P,E){const G=P.colorSpace,Q=P.format,ie=P.type;return P.isCompressedTexture===!0||P.isVideoTexture===!0||G!==Ci&&G!==Rn&&(Qe.getTransfer(G)===rt?(Q!==Zt||ie!==vn)&&console.warn("THREE.WebGLTextures: sRGB encoded textures have to use RGBAFormat and UnsignedByteType."):console.error("THREE.WebGLTextures: Unsupported texture color space:",G)),E}function Re(P){return typeof HTMLImageElement<"u"&&P instanceof HTMLImageElement?(l.width=P.naturalWidth||P.width,l.height=P.naturalHeight||P.height):typeof VideoFrame<"u"&&P instanceof VideoFrame?(l.width=P.displayWidth,l.height=P.displayHeight):(l.width=P.width,l.height=P.height),l}this.allocateTextureUnit=C,this.resetTextureUnits=U,this.setTexture2D=k,this.setTexture2DArray=N,this.setTexture3D=O,this.setTextureCube=z,this.rebindTextures=de,this.setupRenderTarget=Y,this.updateRenderTargetMipmap=re,this.updateMultisampleRenderTarget=Ie,this.setupDepthRenderbuffer=_e,this.setupFrameBufferTexture=ue,this.useMultisampledRTT=Ce}function pm(n,e){function t(i,r=Rn){let a;const s=Qe.getTransfer(r);if(i===vn)return n.UNSIGNED_BYTE;if(i===Ps)return n.UNSIGNED_SHORT_4_4_4_4;if(i===Ds)return n.UNSIGNED_SHORT_5_5_5_1;if(i===Ec)return n.UNSIGNED_INT_5_9_9_9_REV;if(i===Mc)return n.BYTE;if(i===Sc)return n.SHORT;if(i===Xi)return n.UNSIGNED_SHORT;if(i===Cs)return n.INT;if(i===Qn)return n.UNSIGNED_INT;if(i===pn)return n.FLOAT;if(i===$i)return n.HALF_FLOAT;if(i===bc)return n.ALPHA;if(i===yc)return n.RGB;if(i===Zt)return n.RGBA;if(i===Tc)return n.LUMINANCE;if(i===wc)return n.LUMINANCE_ALPHA;if(i===Ei)return n.DEPTH_COMPONENT;if(i===Ri)return n.DEPTH_STENCIL;if(i===Ac)return n.RED;if(i===Ls)return n.RED_INTEGER;if(i===Rc)return n.RG;if(i===Is)return n.RG_INTEGER;if(i===Us)return n.RGBA_INTEGER;if(i===Rr||i===Cr||i===Pr||i===Dr)if(s===rt)if(a=e.get("WEBGL_compressed_texture_s3tc_srgb"),a!==null){if(i===Rr)return a.COMPRESSED_SRGB_S3TC_DXT1_EXT;if(i===Cr)return a.COMPRESSED_SRGB_ALPHA_S3TC_DXT1_EXT;if(i===Pr)return a.COMPRESSED_SRGB_ALPHA_S3TC_DXT3_EXT;if(i===Dr)return a.COMPRESSED_SRGB_ALPHA_S3TC_DXT5_EXT}else return null;else if(a=e.get("WEBGL_compressed_texture_s3tc"),a!==null){if(i===Rr)return a.COMPRESSED_RGB_S3TC_DXT1_EXT;if(i===Cr)return a.COMPRESSED_RGBA_S3TC_DXT1_EXT;if(i===Pr)return a.COMPRESSED_RGBA_S3TC_DXT3_EXT;if(i===Dr)return a.COMPRESSED_RGBA_S3TC_DXT5_EXT}else return null;if(i===Xa||i===Ka||i===qa||i===$a)if(a=e.get("WEBGL_compressed_texture_pvrtc"),a!==null){if(i===Xa)return a.COMPRESSED_RGB_PVRTC_4BPPV1_IMG;if(i===Ka)return a.COMPRESSED_RGB_PVRTC_2BPPV1_IMG;if(i===qa)return a.COMPRESSED_RGBA_PVRTC_4BPPV1_IMG;if(i===$a)return a.COMPRESSED_RGBA_PVRTC_2BPPV1_IMG}else return null;if(i===Ya||i===Za||i===Ja)if(a=e.get("WEBGL_compressed_texture_etc"),a!==null){if(i===Ya||i===Za)return s===rt?a.COMPRESSED_SRGB8_ETC2:a.COMPRESSED_RGB8_ETC2;if(i===Ja)return s===rt?a.COMPRESSED_SRGB8_ALPHA8_ETC2_EAC:a.COMPRESSED_RGBA8_ETC2_EAC}else return null;if(i===Qa||i===es||i===ts||i===ns||i===is||i===rs||i===as||i===ss||i===os||i===cs||i===ls||i===us||i===ds||i===hs)if(a=e.get("WEBGL_compressed_texture_astc"),a!==null){if(i===Qa)return s===rt?a.COMPRESSED_SRGB8_ALPHA8_ASTC_4x4_KHR:a.COMPRESSED_RGBA_ASTC_4x4_KHR;if(i===es)return s===rt?a.COMPRESSED_SRGB8_ALPHA8_ASTC_5x4_KHR:a.COMPRESSED_RGBA_ASTC_5x4_KHR;if(i===ts)return s===rt?a.COMPRESSED_SRGB8_ALPHA8_ASTC_5x5_KHR:a.COMPRESSED_RGBA_ASTC_5x5_KHR;if(i===ns)return s===rt?a.COMPRESSED_SRGB8_ALPHA8_ASTC_6x5_KHR:a.COMPRESSED_RGBA_ASTC_6x5_KHR;if(i===is)return s===rt?a.COMPRESSED_SRGB8_ALPHA8_ASTC_6x6_KHR:a.COMPRESSED_RGBA_ASTC_6x6_KHR;if(i===rs)return s===rt?a.COMPRESSED_SRGB8_ALPHA8_ASTC_8x5_KHR:a.COMPRESSED_RGBA_ASTC_8x5_KHR;if(i===as)return s===rt?a.COMPRESSED_SRGB8_ALPHA8_ASTC_8x6_KHR:a.COMPRESSED_RGBA_ASTC_8x6_KHR;if(i===ss)return s===rt?a.COMPRESSED_SRGB8_ALPHA8_ASTC_8x8_KHR:a.COMPRESSED_RGBA_ASTC_8x8_KHR;if(i===os)return s===rt?a.COMPRESSED_SRGB8_ALPHA8_ASTC_10x5_KHR:a.COMPRESSED_RGBA_ASTC_10x5_KHR;if(i===cs)return s===rt?a.COMPRESSED_SRGB8_ALPHA8_ASTC_10x6_KHR:a.COMPRESSED_RGBA_ASTC_10x6_KHR;if(i===ls)return s===rt?a.COMPRESSED_SRGB8_ALPHA8_ASTC_10x8_KHR:a.COMPRESSED_RGBA_ASTC_10x8_KHR;if(i===us)return s===rt?a.COMPRESSED_SRGB8_ALPHA8_ASTC_10x10_KHR:a.COMPRESSED_RGBA_ASTC_10x10_KHR;if(i===ds)return s===rt?a.COMPRESSED_SRGB8_ALPHA8_ASTC_12x10_KHR:a.COMPRESSED_RGBA_ASTC_12x10_KHR;if(i===hs)return s===rt?a.COMPRESSED_SRGB8_ALPHA8_ASTC_12x12_KHR:a.COMPRESSED_RGBA_ASTC_12x12_KHR}else return null;if(i===Lr||i===fs||i===ps)if(a=e.get("EXT_texture_compression_bptc"),a!==null){if(i===Lr)return s===rt?a.COMPRESSED_SRGB_ALPHA_BPTC_UNORM_EXT:a.COMPRESSED_RGBA_BPTC_UNORM_EXT;if(i===fs)return a.COMPRESSED_RGB_BPTC_SIGNED_FLOAT_EXT;if(i===ps)return a.COMPRESSED_RGB_BPTC_UNSIGNED_FLOAT_EXT}else return null;if(i===Cc||i===ms||i===gs||i===_s)if(a=e.get("EXT_texture_compression_rgtc"),a!==null){if(i===Lr)return a.COMPRESSED_RED_RGTC1_EXT;if(i===ms)return a.COMPRESSED_SIGNED_RED_RGTC1_EXT;if(i===gs)return a.COMPRESSED_RED_GREEN_RGTC2_EXT;if(i===_s)return a.COMPRESSED_SIGNED_RED_GREEN_RGTC2_EXT}else return null;return i===Ai?n.UNSIGNED_INT_24_8:n[i]!==void 0?n[i]:null}return{convert:t}}const mm=`
void main() {

	gl_Position = vec4( position, 1.0 );

}`,gm=`
uniform sampler2DArray depthColor;
uniform float depthWidth;
uniform float depthHeight;

void main() {

	vec2 coord = vec2( gl_FragCoord.x / depthWidth, gl_FragCoord.y / depthHeight );

	if ( coord.x >= 1.0 ) {

		gl_FragDepth = texture( depthColor, vec3( coord.x - 1.0, coord.y, 1 ) ).r;

	} else {

		gl_FragDepth = texture( depthColor, vec3( coord.x, coord.y, 0 ) ).r;

	}

}`;class _m{constructor(){this.texture=null,this.mesh=null,this.depthNear=0,this.depthFar=0}init(e,t,i){if(this.texture===null){const r=new Ct,a=e.properties.get(r);a.__webglTexture=t.texture,(t.depthNear!==i.depthNear||t.depthFar!==i.depthFar)&&(this.depthNear=t.depthNear,this.depthFar=t.depthFar),this.texture=r}}getMesh(e){if(this.texture!==null&&this.mesh===null){const t=e.cameras[0].viewport,i=new In({vertexShader:mm,fragmentShader:gm,uniforms:{depthColor:{value:this.texture},depthWidth:{value:t.z},depthHeight:{value:t.w}}});this.mesh=new We(new zi(20,20),i)}return this.mesh}reset(){this.texture=null,this.mesh=null}getDepthTexture(){return this.texture}}class vm extends Di{constructor(e,t){super();const i=this;let r=null,a=1,s=null,o="local-floor",c=1,l=null,d=null,h=null,f=null,m=null,g=null;const _=new _m,p=t.getContextAttributes();let u=null,b=null;const S=[],M=[],w=new Ke;let T=null;const A=new Ht;A.viewport=new dt;const L=new Ht;L.viewport=new dt;const x=[A,L],v=new Fu;let R=null,U=null;this.cameraAutoUpdate=!0,this.enabled=!1,this.isPresenting=!1,this.getController=function(K){let ne=S[K];return ne===void 0&&(ne=new ga,S[K]=ne),ne.getTargetRaySpace()},this.getControllerGrip=function(K){let ne=S[K];return ne===void 0&&(ne=new ga,S[K]=ne),ne.getGripSpace()},this.getHand=function(K){let ne=S[K];return ne===void 0&&(ne=new ga,S[K]=ne),ne.getHandSpace()};function C(K){const ne=M.indexOf(K.inputSource);if(ne===-1)return;const ue=S[ne];ue!==void 0&&(ue.update(K.inputSource,K.frame,l||s),ue.dispatchEvent({type:K.type,data:K.inputSource}))}function D(){r.removeEventListener("select",C),r.removeEventListener("selectstart",C),r.removeEventListener("selectend",C),r.removeEventListener("squeeze",C),r.removeEventListener("squeezestart",C),r.removeEventListener("squeezeend",C),r.removeEventListener("end",D),r.removeEventListener("inputsourceschange",k);for(let K=0;K<S.length;K++){const ne=M[K];ne!==null&&(M[K]=null,S[K].disconnect(ne))}R=null,U=null,_.reset(),e.setRenderTarget(u),m=null,f=null,h=null,r=null,b=null,Ae.stop(),i.isPresenting=!1,e.setPixelRatio(T),e.setSize(w.width,w.height,!1),i.dispatchEvent({type:"sessionend"})}this.setFramebufferScaleFactor=function(K){a=K,i.isPresenting===!0&&console.warn("THREE.WebXRManager: Cannot change framebuffer scale while presenting.")},this.setReferenceSpaceType=function(K){o=K,i.isPresenting===!0&&console.warn("THREE.WebXRManager: Cannot change reference space type while presenting.")},this.getReferenceSpace=function(){return l||s},this.setReferenceSpace=function(K){l=K},this.getBaseLayer=function(){return f!==null?f:m},this.getBinding=function(){return h},this.getFrame=function(){return g},this.getSession=function(){return r},this.setSession=async function(K){if(r=K,r!==null){if(u=e.getRenderTarget(),r.addEventListener("select",C),r.addEventListener("selectstart",C),r.addEventListener("selectend",C),r.addEventListener("squeeze",C),r.addEventListener("squeezestart",C),r.addEventListener("squeezeend",C),r.addEventListener("end",D),r.addEventListener("inputsourceschange",k),p.xrCompatible!==!0&&await t.makeXRCompatible(),T=e.getPixelRatio(),e.getSize(w),typeof XRWebGLBinding<"u"&&"createProjectionLayer"in XRWebGLBinding.prototype){let ue=null,ae=null,ee=null;p.depth&&(ee=p.stencil?t.DEPTH24_STENCIL8:t.DEPTH_COMPONENT24,ue=p.stencil?Ri:Ei,ae=p.stencil?Ai:Qn);const _e={colorFormat:t.RGBA8,depthFormat:ee,scaleFactor:a};h=new XRWebGLBinding(r,t),f=h.createProjectionLayer(_e),r.updateRenderState({layers:[f]}),e.setPixelRatio(1),e.setSize(f.textureWidth,f.textureHeight,!1),b=new ei(f.textureWidth,f.textureHeight,{format:Zt,type:vn,depthTexture:new Bc(f.textureWidth,f.textureHeight,ae,void 0,void 0,void 0,void 0,void 0,void 0,ue),stencilBuffer:p.stencil,colorSpace:e.outputColorSpace,samples:p.antialias?4:0,resolveDepthBuffer:f.ignoreDepthValues===!1,resolveStencilBuffer:f.ignoreDepthValues===!1})}else{const ue={antialias:p.antialias,alpha:!0,depth:p.depth,stencil:p.stencil,framebufferScaleFactor:a};m=new XRWebGLLayer(r,t,ue),r.updateRenderState({baseLayer:m}),e.setPixelRatio(1),e.setSize(m.framebufferWidth,m.framebufferHeight,!1),b=new ei(m.framebufferWidth,m.framebufferHeight,{format:Zt,type:vn,colorSpace:e.outputColorSpace,stencilBuffer:p.stencil,resolveDepthBuffer:m.ignoreDepthValues===!1,resolveStencilBuffer:m.ignoreDepthValues===!1})}b.isXRRenderTarget=!0,this.setFoveation(c),l=null,s=await r.requestReferenceSpace(o),Ae.setContext(r),Ae.start(),i.isPresenting=!0,i.dispatchEvent({type:"sessionstart"})}},this.getEnvironmentBlendMode=function(){if(r!==null)return r.environmentBlendMode},this.getDepthTexture=function(){return _.getDepthTexture()};function k(K){for(let ne=0;ne<K.removed.length;ne++){const ue=K.removed[ne],ae=M.indexOf(ue);ae>=0&&(M[ae]=null,S[ae].disconnect(ue))}for(let ne=0;ne<K.added.length;ne++){const ue=K.added[ne];let ae=M.indexOf(ue);if(ae===-1){for(let _e=0;_e<S.length;_e++)if(_e>=M.length){M.push(ue),ae=_e;break}else if(M[_e]===null){M[_e]=ue,ae=_e;break}if(ae===-1)break}const ee=S[ae];ee&&ee.connect(ue)}}const N=new F,O=new F;function z(K,ne,ue){N.setFromMatrixPosition(ne.matrixWorld),O.setFromMatrixPosition(ue.matrixWorld);const ae=N.distanceTo(O),ee=ne.projectionMatrix.elements,_e=ue.projectionMatrix.elements,de=ee[14]/(ee[10]-1),Y=ee[14]/(ee[10]+1),re=(ee[9]+1)/ee[5],oe=(ee[9]-1)/ee[5],I=(ee[8]-1)/ee[0],Ie=(_e[8]+1)/_e[0],Pe=de*I,Ce=de*Ie,Me=ae/(-I+Ie),Fe=Me*-I;if(ne.matrixWorld.decompose(K.position,K.quaternion,K.scale),K.translateX(Fe),K.translateZ(Me),K.matrixWorld.compose(K.position,K.quaternion,K.scale),K.matrixWorldInverse.copy(K.matrixWorld).invert(),ee[10]===-1)K.projectionMatrix.copy(ne.projectionMatrix),K.projectionMatrixInverse.copy(ne.projectionMatrixInverse);else{const Re=de+Me,P=Y+Me,E=Pe-Fe,G=Ce+(ae-Fe),Q=re*Y/P*Re,ie=oe*Y/P*Re;K.projectionMatrix.makePerspective(E,G,Q,ie,Re,P),K.projectionMatrixInverse.copy(K.projectionMatrix).invert()}}function H(K,ne){ne===null?K.matrixWorld.copy(K.matrix):K.matrixWorld.multiplyMatrices(ne.matrixWorld,K.matrix),K.matrixWorldInverse.copy(K.matrixWorld).invert()}this.updateCamera=function(K){if(r===null)return;let ne=K.near,ue=K.far;_.texture!==null&&(_.depthNear>0&&(ne=_.depthNear),_.depthFar>0&&(ue=_.depthFar)),v.near=L.near=A.near=ne,v.far=L.far=A.far=ue,(R!==v.near||U!==v.far)&&(r.updateRenderState({depthNear:v.near,depthFar:v.far}),R=v.near,U=v.far),A.layers.mask=K.layers.mask|2,L.layers.mask=K.layers.mask|4,v.layers.mask=A.layers.mask|L.layers.mask;const ae=K.parent,ee=v.cameras;H(v,ae);for(let _e=0;_e<ee.length;_e++)H(ee[_e],ae);ee.length===2?z(v,A,L):v.projectionMatrix.copy(A.projectionMatrix),q(K,v,ae)};function q(K,ne,ue){ue===null?K.matrix.copy(ne.matrixWorld):(K.matrix.copy(ue.matrixWorld),K.matrix.invert(),K.matrix.multiply(ne.matrixWorld)),K.matrix.decompose(K.position,K.quaternion,K.scale),K.updateMatrixWorld(!0),K.projectionMatrix.copy(ne.projectionMatrix),K.projectionMatrixInverse.copy(ne.projectionMatrixInverse),K.isPerspectiveCamera&&(K.fov=vs*2*Math.atan(1/K.projectionMatrix.elements[5]),K.zoom=1)}this.getCamera=function(){return v},this.getFoveation=function(){if(!(f===null&&m===null))return c},this.setFoveation=function(K){c=K,f!==null&&(f.fixedFoveation=K),m!==null&&m.fixedFoveation!==void 0&&(m.fixedFoveation=K)},this.hasDepthSensing=function(){return _.texture!==null},this.getDepthSensingMesh=function(){return _.getMesh(v)};let J=null;function fe(K,ne){if(d=ne.getViewerPose(l||s),g=ne,d!==null){const ue=d.views;m!==null&&(e.setRenderTargetFramebuffer(b,m.framebuffer),e.setRenderTarget(b));let ae=!1;ue.length!==v.cameras.length&&(v.cameras.length=0,ae=!0);for(let de=0;de<ue.length;de++){const Y=ue[de];let re=null;if(m!==null)re=m.getViewport(Y);else{const I=h.getViewSubImage(f,Y);re=I.viewport,de===0&&(e.setRenderTargetTextures(b,I.colorTexture,f.ignoreDepthValues?void 0:I.depthStencilTexture),e.setRenderTarget(b))}let oe=x[de];oe===void 0&&(oe=new Ht,oe.layers.enable(de),oe.viewport=new dt,x[de]=oe),oe.matrix.fromArray(Y.transform.matrix),oe.matrix.decompose(oe.position,oe.quaternion,oe.scale),oe.projectionMatrix.fromArray(Y.projectionMatrix),oe.projectionMatrixInverse.copy(oe.projectionMatrix).invert(),oe.viewport.set(re.x,re.y,re.width,re.height),de===0&&(v.matrix.copy(oe.matrix),v.matrix.decompose(v.position,v.quaternion,v.scale)),ae===!0&&v.cameras.push(oe)}const ee=r.enabledFeatures;if(ee&&ee.includes("depth-sensing")&&r.depthUsage=="gpu-optimized"&&h){const de=h.getDepthInformation(ue[0]);de&&de.isValid&&de.texture&&_.init(e,de,r.renderState)}}for(let ue=0;ue<S.length;ue++){const ae=M[ue],ee=S[ue];ae!==null&&ee!==void 0&&ee.update(ae,ne,l||s)}J&&J(K,ne),ne.detectedPlanes&&i.dispatchEvent({type:"planesdetected",data:ne}),g=null}const Ae=new Hc;Ae.setAnimationLoop(fe),this.setAnimationLoop=function(K){J=K},this.dispose=function(){}}}const jn=new mt,xm=new ct;function Mm(n,e){function t(p,u){p.matrixAutoUpdate===!0&&p.updateMatrix(),u.value.copy(p.matrix)}function i(p,u){u.color.getRGB(p.fogColor.value,kc(n)),u.isFog?(p.fogNear.value=u.near,p.fogFar.value=u.far):u.isFogExp2&&(p.fogDensity.value=u.density)}function r(p,u,b,S,M){u.isMeshBasicMaterial||u.isMeshLambertMaterial?a(p,u):u.isMeshToonMaterial?(a(p,u),h(p,u)):u.isMeshPhongMaterial?(a(p,u),d(p,u)):u.isMeshStandardMaterial?(a(p,u),f(p,u),u.isMeshPhysicalMaterial&&m(p,u,M)):u.isMeshMatcapMaterial?(a(p,u),g(p,u)):u.isMeshDepthMaterial?a(p,u):u.isMeshDistanceMaterial?(a(p,u),_(p,u)):u.isMeshNormalMaterial?a(p,u):u.isLineBasicMaterial?(s(p,u),u.isLineDashedMaterial&&o(p,u)):u.isPointsMaterial?c(p,u,b,S):u.isSpriteMaterial?l(p,u):u.isShadowMaterial?(p.color.value.copy(u.color),p.opacity.value=u.opacity):u.isShaderMaterial&&(u.uniformsNeedUpdate=!1)}function a(p,u){p.opacity.value=u.opacity,u.color&&p.diffuse.value.copy(u.color),u.emissive&&p.emissive.value.copy(u.emissive).multiplyScalar(u.emissiveIntensity),u.map&&(p.map.value=u.map,t(u.map,p.mapTransform)),u.alphaMap&&(p.alphaMap.value=u.alphaMap,t(u.alphaMap,p.alphaMapTransform)),u.bumpMap&&(p.bumpMap.value=u.bumpMap,t(u.bumpMap,p.bumpMapTransform),p.bumpScale.value=u.bumpScale,u.side===Lt&&(p.bumpScale.value*=-1)),u.normalMap&&(p.normalMap.value=u.normalMap,t(u.normalMap,p.normalMapTransform),p.normalScale.value.copy(u.normalScale),u.side===Lt&&p.normalScale.value.negate()),u.displacementMap&&(p.displacementMap.value=u.displacementMap,t(u.displacementMap,p.displacementMapTransform),p.displacementScale.value=u.displacementScale,p.displacementBias.value=u.displacementBias),u.emissiveMap&&(p.emissiveMap.value=u.emissiveMap,t(u.emissiveMap,p.emissiveMapTransform)),u.specularMap&&(p.specularMap.value=u.specularMap,t(u.specularMap,p.specularMapTransform)),u.alphaTest>0&&(p.alphaTest.value=u.alphaTest);const b=e.get(u),S=b.envMap,M=b.envMapRotation;S&&(p.envMap.value=S,jn.copy(M),jn.x*=-1,jn.y*=-1,jn.z*=-1,S.isCubeTexture&&S.isRenderTargetTexture===!1&&(jn.y*=-1,jn.z*=-1),p.envMapRotation.value.setFromMatrix4(xm.makeRotationFromEuler(jn)),p.flipEnvMap.value=S.isCubeTexture&&S.isRenderTargetTexture===!1?-1:1,p.reflectivity.value=u.reflectivity,p.ior.value=u.ior,p.refractionRatio.value=u.refractionRatio),u.lightMap&&(p.lightMap.value=u.lightMap,p.lightMapIntensity.value=u.lightMapIntensity,t(u.lightMap,p.lightMapTransform)),u.aoMap&&(p.aoMap.value=u.aoMap,p.aoMapIntensity.value=u.aoMapIntensity,t(u.aoMap,p.aoMapTransform))}function s(p,u){p.diffuse.value.copy(u.color),p.opacity.value=u.opacity,u.map&&(p.map.value=u.map,t(u.map,p.mapTransform))}function o(p,u){p.dashSize.value=u.dashSize,p.totalSize.value=u.dashSize+u.gapSize,p.scale.value=u.scale}function c(p,u,b,S){p.diffuse.value.copy(u.color),p.opacity.value=u.opacity,p.size.value=u.size*b,p.scale.value=S*.5,u.map&&(p.map.value=u.map,t(u.map,p.uvTransform)),u.alphaMap&&(p.alphaMap.value=u.alphaMap,t(u.alphaMap,p.alphaMapTransform)),u.alphaTest>0&&(p.alphaTest.value=u.alphaTest)}function l(p,u){p.diffuse.value.copy(u.color),p.opacity.value=u.opacity,p.rotation.value=u.rotation,u.map&&(p.map.value=u.map,t(u.map,p.mapTransform)),u.alphaMap&&(p.alphaMap.value=u.alphaMap,t(u.alphaMap,p.alphaMapTransform)),u.alphaTest>0&&(p.alphaTest.value=u.alphaTest)}function d(p,u){p.specular.value.copy(u.specular),p.shininess.value=Math.max(u.shininess,1e-4)}function h(p,u){u.gradientMap&&(p.gradientMap.value=u.gradientMap)}function f(p,u){p.metalness.value=u.metalness,u.metalnessMap&&(p.metalnessMap.value=u.metalnessMap,t(u.metalnessMap,p.metalnessMapTransform)),p.roughness.value=u.roughness,u.roughnessMap&&(p.roughnessMap.value=u.roughnessMap,t(u.roughnessMap,p.roughnessMapTransform)),u.envMap&&(p.envMapIntensity.value=u.envMapIntensity)}function m(p,u,b){p.ior.value=u.ior,u.sheen>0&&(p.sheenColor.value.copy(u.sheenColor).multiplyScalar(u.sheen),p.sheenRoughness.value=u.sheenRoughness,u.sheenColorMap&&(p.sheenColorMap.value=u.sheenColorMap,t(u.sheenColorMap,p.sheenColorMapTransform)),u.sheenRoughnessMap&&(p.sheenRoughnessMap.value=u.sheenRoughnessMap,t(u.sheenRoughnessMap,p.sheenRoughnessMapTransform))),u.clearcoat>0&&(p.clearcoat.value=u.clearcoat,p.clearcoatRoughness.value=u.clearcoatRoughness,u.clearcoatMap&&(p.clearcoatMap.value=u.clearcoatMap,t(u.clearcoatMap,p.clearcoatMapTransform)),u.clearcoatRoughnessMap&&(p.clearcoatRoughnessMap.value=u.clearcoatRoughnessMap,t(u.clearcoatRoughnessMap,p.clearcoatRoughnessMapTransform)),u.clearcoatNormalMap&&(p.clearcoatNormalMap.value=u.clearcoatNormalMap,t(u.clearcoatNormalMap,p.clearcoatNormalMapTransform),p.clearcoatNormalScale.value.copy(u.clearcoatNormalScale),u.side===Lt&&p.clearcoatNormalScale.value.negate())),u.dispersion>0&&(p.dispersion.value=u.dispersion),u.iridescence>0&&(p.iridescence.value=u.iridescence,p.iridescenceIOR.value=u.iridescenceIOR,p.iridescenceThicknessMinimum.value=u.iridescenceThicknessRange[0],p.iridescenceThicknessMaximum.value=u.iridescenceThicknessRange[1],u.iridescenceMap&&(p.iridescenceMap.value=u.iridescenceMap,t(u.iridescenceMap,p.iridescenceMapTransform)),u.iridescenceThicknessMap&&(p.iridescenceThicknessMap.value=u.iridescenceThicknessMap,t(u.iridescenceThicknessMap,p.iridescenceThicknessMapTransform))),u.transmission>0&&(p.transmission.value=u.transmission,p.transmissionSamplerMap.value=b.texture,p.transmissionSamplerSize.value.set(b.width,b.height),u.transmissionMap&&(p.transmissionMap.value=u.transmissionMap,t(u.transmissionMap,p.transmissionMapTransform)),p.thickness.value=u.thickness,u.thicknessMap&&(p.thicknessMap.value=u.thicknessMap,t(u.thicknessMap,p.thicknessMapTransform)),p.attenuationDistance.value=u.attenuationDistance,p.attenuationColor.value.copy(u.attenuationColor)),u.anisotropy>0&&(p.anisotropyVector.value.set(u.anisotropy*Math.cos(u.anisotropyRotation),u.anisotropy*Math.sin(u.anisotropyRotation)),u.anisotropyMap&&(p.anisotropyMap.value=u.anisotropyMap,t(u.anisotropyMap,p.anisotropyMapTransform))),p.specularIntensity.value=u.specularIntensity,p.specularColor.value.copy(u.specularColor),u.specularColorMap&&(p.specularColorMap.value=u.specularColorMap,t(u.specularColorMap,p.specularColorMapTransform)),u.specularIntensityMap&&(p.specularIntensityMap.value=u.specularIntensityMap,t(u.specularIntensityMap,p.specularIntensityMapTransform))}function g(p,u){u.matcap&&(p.matcap.value=u.matcap)}function _(p,u){const b=e.get(u).light;p.referencePosition.value.setFromMatrixPosition(b.matrixWorld),p.nearDistance.value=b.shadow.camera.near,p.farDistance.value=b.shadow.camera.far}return{refreshFogUniforms:i,refreshMaterialUniforms:r}}function Sm(n,e,t,i){let r={},a={},s=[];const o=n.getParameter(n.MAX_UNIFORM_BUFFER_BINDINGS);function c(b,S){const M=S.program;i.uniformBlockBinding(b,M)}function l(b,S){let M=r[b.id];M===void 0&&(g(b),M=d(b),r[b.id]=M,b.addEventListener("dispose",p));const w=S.program;i.updateUBOMapping(b,w);const T=e.render.frame;a[b.id]!==T&&(f(b),a[b.id]=T)}function d(b){const S=h();b.__bindingPointIndex=S;const M=n.createBuffer(),w=b.__size,T=b.usage;return n.bindBuffer(n.UNIFORM_BUFFER,M),n.bufferData(n.UNIFORM_BUFFER,w,T),n.bindBuffer(n.UNIFORM_BUFFER,null),n.bindBufferBase(n.UNIFORM_BUFFER,S,M),M}function h(){for(let b=0;b<o;b++)if(s.indexOf(b)===-1)return s.push(b),b;return console.error("THREE.WebGLRenderer: Maximum number of simultaneously usable uniforms groups reached."),0}function f(b){const S=r[b.id],M=b.uniforms,w=b.__cache;n.bindBuffer(n.UNIFORM_BUFFER,S);for(let T=0,A=M.length;T<A;T++){const L=Array.isArray(M[T])?M[T]:[M[T]];for(let x=0,v=L.length;x<v;x++){const R=L[x];if(m(R,T,x,w)===!0){const U=R.__offset,C=Array.isArray(R.value)?R.value:[R.value];let D=0;for(let k=0;k<C.length;k++){const N=C[k],O=_(N);typeof N=="number"||typeof N=="boolean"?(R.__data[0]=N,n.bufferSubData(n.UNIFORM_BUFFER,U+D,R.__data)):N.isMatrix3?(R.__data[0]=N.elements[0],R.__data[1]=N.elements[1],R.__data[2]=N.elements[2],R.__data[3]=0,R.__data[4]=N.elements[3],R.__data[5]=N.elements[4],R.__data[6]=N.elements[5],R.__data[7]=0,R.__data[8]=N.elements[6],R.__data[9]=N.elements[7],R.__data[10]=N.elements[8],R.__data[11]=0):(N.toArray(R.__data,D),D+=O.storage/Float32Array.BYTES_PER_ELEMENT)}n.bufferSubData(n.UNIFORM_BUFFER,U,R.__data)}}}n.bindBuffer(n.UNIFORM_BUFFER,null)}function m(b,S,M,w){const T=b.value,A=S+"_"+M;if(w[A]===void 0)return typeof T=="number"||typeof T=="boolean"?w[A]=T:w[A]=T.clone(),!0;{const L=w[A];if(typeof T=="number"||typeof T=="boolean"){if(L!==T)return w[A]=T,!0}else if(L.equals(T)===!1)return L.copy(T),!0}return!1}function g(b){const S=b.uniforms;let M=0;const w=16;for(let A=0,L=S.length;A<L;A++){const x=Array.isArray(S[A])?S[A]:[S[A]];for(let v=0,R=x.length;v<R;v++){const U=x[v],C=Array.isArray(U.value)?U.value:[U.value];for(let D=0,k=C.length;D<k;D++){const N=C[D],O=_(N),z=M%w,H=z%O.boundary,q=z+H;M+=H,q!==0&&w-q<O.storage&&(M+=w-q),U.__data=new Float32Array(O.storage/Float32Array.BYTES_PER_ELEMENT),U.__offset=M,M+=O.storage}}}const T=M%w;return T>0&&(M+=w-T),b.__size=M,b.__cache={},this}function _(b){const S={boundary:0,storage:0};return typeof b=="number"||typeof b=="boolean"?(S.boundary=4,S.storage=4):b.isVector2?(S.boundary=8,S.storage=8):b.isVector3||b.isColor?(S.boundary=16,S.storage=12):b.isVector4?(S.boundary=16,S.storage=16):b.isMatrix3?(S.boundary=48,S.storage=48):b.isMatrix4?(S.boundary=64,S.storage=64):b.isTexture?console.warn("THREE.WebGLRenderer: Texture samplers can not be part of an uniforms group."):console.warn("THREE.WebGLRenderer: Unsupported uniform value type.",b),S}function p(b){const S=b.target;S.removeEventListener("dispose",p);const M=s.indexOf(S.__bindingPointIndex);s.splice(M,1),n.deleteBuffer(r[S.id]),delete r[S.id],delete a[S.id]}function u(){for(const b in r)n.deleteBuffer(r[b]);s=[],r={},a={}}return{bind:c,update:l,dispose:u}}class Em{constructor(e={}){const{canvas:t=tu(),context:i=null,depth:r=!0,stencil:a=!1,alpha:s=!1,antialias:o=!1,premultipliedAlpha:c=!0,preserveDrawingBuffer:l=!1,powerPreference:d="default",failIfMajorPerformanceCaveat:h=!1,reverseDepthBuffer:f=!1}=e;this.isWebGLRenderer=!0;let m;if(i!==null){if(typeof WebGLRenderingContext<"u"&&i instanceof WebGLRenderingContext)throw new Error("THREE.WebGLRenderer: WebGL 1 is not supported since r163.");m=i.getContextAttributes().alpha}else m=s;const g=new Uint32Array(4),_=new Int32Array(4);let p=null,u=null;const b=[],S=[];this.domElement=t,this.debug={checkShaderErrors:!0,onShaderError:null},this.autoClear=!0,this.autoClearColor=!0,this.autoClearDepth=!0,this.autoClearStencil=!0,this.sortObjects=!0,this.clippingPlanes=[],this.localClippingEnabled=!1,this._outputColorSpace=Ft,this.toneMapping=Dn,this.toneMappingExposure=1;const M=this;let w=!1,T=0,A=0,L=null,x=-1,v=null;const R=new dt,U=new dt;let C=null;const D=new ce(0);let k=0,N=t.width,O=t.height,z=1,H=null,q=null;const J=new dt(0,0,N,O),fe=new dt(0,0,N,O);let Ae=!1;const K=new Fs;let ne=!1,ue=!1;this.transmissionResolutionScale=1;const ae=new ct,ee=new ct,_e=new F,de=new dt,Y={background:null,fog:null,environment:null,overrideMaterial:null,isScene:!0};let re=!1;function oe(){return L===null?z:1}let I=i;function Ie(y,j){return t.getContext(y,j)}try{const y={alpha:!0,depth:r,stencil:a,antialias:o,premultipliedAlpha:c,preserveDrawingBuffer:l,powerPreference:d,failIfMajorPerformanceCaveat:h};if("setAttribute"in t&&t.setAttribute("data-engine",`three.js r${Rs}`),t.addEventListener("webglcontextlost",te,!1),t.addEventListener("webglcontextrestored",xe,!1),t.addEventListener("webglcontextcreationerror",ve,!1),I===null){const j="webgl2";if(I=Ie(j,y),I===null)throw Ie(j)?new Error("Error creating WebGL context with your selected attributes."):new Error("Error creating WebGL context.")}}catch(y){throw console.error("THREE.WebGLRenderer: "+y.message),y}let Pe,Ce,Me,Fe,Re,P,E,G,Q,ie,Z,we,ge,Ee,$e,le,be,Ue,ze,ye,qe,je,at,B;function pe(){Pe=new Lf(I),Pe.init(),je=new pm(I,Pe),Ce=new Tf(I,Pe,e,je),Me=new hm(I,Pe),Ce.reverseDepthBuffer&&f&&Me.buffers.depth.setReversed(!0),Fe=new zf(I),Re=new Qp,P=new fm(I,Pe,Me,Re,Ce,je,Fe),E=new Af(M),G=new Df(M),Q=new Bu(I),at=new bf(I,Q),ie=new If(I,Q,Fe,at),Z=new kf(I,ie,Q,Fe),ze=new Nf(I,Ce,P),le=new wf(Re),we=new Jp(M,E,G,Pe,Ce,at,le),ge=new Mm(M,Re),Ee=new tm,$e=new om(Pe),Ue=new Ef(M,E,G,Me,Z,m,c),be=new um(M,Z,Ce),B=new Sm(I,Fe,Ce,Me),ye=new yf(I,Pe,Fe),qe=new Uf(I,Pe,Fe),Fe.programs=we.programs,M.capabilities=Ce,M.extensions=Pe,M.properties=Re,M.renderLists=Ee,M.shadowMap=be,M.state=Me,M.info=Fe}pe();const $=new vm(M,I);this.xr=$,this.getContext=function(){return I},this.getContextAttributes=function(){return I.getContextAttributes()},this.forceContextLoss=function(){const y=Pe.get("WEBGL_lose_context");y&&y.loseContext()},this.forceContextRestore=function(){const y=Pe.get("WEBGL_lose_context");y&&y.restoreContext()},this.getPixelRatio=function(){return z},this.setPixelRatio=function(y){y!==void 0&&(z=y,this.setSize(N,O,!1))},this.getSize=function(y){return y.set(N,O)},this.setSize=function(y,j,W=!0){if($.isPresenting){console.warn("THREE.WebGLRenderer: Can't change size while VR device is presenting.");return}N=y,O=j,t.width=Math.floor(y*z),t.height=Math.floor(j*z),W===!0&&(t.style.width=y+"px",t.style.height=j+"px"),this.setViewport(0,0,y,j)},this.getDrawingBufferSize=function(y){return y.set(N*z,O*z).floor()},this.setDrawingBufferSize=function(y,j,W){N=y,O=j,z=W,t.width=Math.floor(y*W),t.height=Math.floor(j*W),this.setViewport(0,0,y,j)},this.getCurrentViewport=function(y){return y.copy(R)},this.getViewport=function(y){return y.copy(J)},this.setViewport=function(y,j,W,X){y.isVector4?J.set(y.x,y.y,y.z,y.w):J.set(y,j,W,X),Me.viewport(R.copy(J).multiplyScalar(z).round())},this.getScissor=function(y){return y.copy(fe)},this.setScissor=function(y,j,W,X){y.isVector4?fe.set(y.x,y.y,y.z,y.w):fe.set(y,j,W,X),Me.scissor(U.copy(fe).multiplyScalar(z).round())},this.getScissorTest=function(){return Ae},this.setScissorTest=function(y){Me.setScissorTest(Ae=y)},this.setOpaqueSort=function(y){H=y},this.setTransparentSort=function(y){q=y},this.getClearColor=function(y){return y.copy(Ue.getClearColor())},this.setClearColor=function(){Ue.setClearColor(...arguments)},this.getClearAlpha=function(){return Ue.getClearAlpha()},this.setClearAlpha=function(){Ue.setClearAlpha(...arguments)},this.clear=function(y=!0,j=!0,W=!0){let X=0;if(y){let V=!1;if(L!==null){const se=L.texture.format;V=se===Us||se===Is||se===Ls}if(V){const se=L.texture.type,me=se===vn||se===Qn||se===Xi||se===Ai||se===Ps||se===Ds,Se=Ue.getClearColor(),Te=Ue.getClearAlpha(),Ne=Se.r,ke=Se.g,De=Se.b;me?(g[0]=Ne,g[1]=ke,g[2]=De,g[3]=Te,I.clearBufferuiv(I.COLOR,0,g)):(_[0]=Ne,_[1]=ke,_[2]=De,_[3]=Te,I.clearBufferiv(I.COLOR,0,_))}else X|=I.COLOR_BUFFER_BIT}j&&(X|=I.DEPTH_BUFFER_BIT),W&&(X|=I.STENCIL_BUFFER_BIT,this.state.buffers.stencil.setMask(4294967295)),I.clear(X)},this.clearColor=function(){this.clear(!0,!1,!1)},this.clearDepth=function(){this.clear(!1,!0,!1)},this.clearStencil=function(){this.clear(!1,!1,!0)},this.dispose=function(){t.removeEventListener("webglcontextlost",te,!1),t.removeEventListener("webglcontextrestored",xe,!1),t.removeEventListener("webglcontextcreationerror",ve,!1),Ue.dispose(),Ee.dispose(),$e.dispose(),Re.dispose(),E.dispose(),G.dispose(),Z.dispose(),at.dispose(),B.dispose(),we.dispose(),$.dispose(),$.removeEventListener("sessionstart",Xs),$.removeEventListener("sessionend",Ks),Un.stop()};function te(y){y.preventDefault(),console.log("THREE.WebGLRenderer: Context Lost."),w=!0}function xe(){console.log("THREE.WebGLRenderer: Context Restored."),w=!1;const y=Fe.autoReset,j=be.enabled,W=be.autoUpdate,X=be.needsUpdate,V=be.type;pe(),Fe.autoReset=y,be.enabled=j,be.autoUpdate=W,be.needsUpdate=X,be.type=V}function ve(y){console.error("THREE.WebGLRenderer: A WebGL context could not be created. Reason: ",y.statusMessage)}function Oe(y){const j=y.target;j.removeEventListener("dispose",Oe),lt(j)}function lt(y){bt(y),Re.remove(y)}function bt(y){const j=Re.get(y).programs;j!==void 0&&(j.forEach(function(W){we.releaseProgram(W)}),y.isShaderMaterial&&we.releaseShaderCache(y))}this.renderBufferDirect=function(y,j,W,X,V,se){j===null&&(j=Y);const me=V.isMesh&&V.matrixWorld.determinant()<0,Se=Qc(y,j,W,X,V);Me.setMaterial(X,me);let Te=W.index,Ne=1;if(X.wireframe===!0){if(Te=ie.getWireframeAttribute(W),Te===void 0)return;Ne=2}const ke=W.drawRange,De=W.attributes.position;let Ye=ke.start*Ne,et=(ke.start+ke.count)*Ne;se!==null&&(Ye=Math.max(Ye,se.start*Ne),et=Math.min(et,(se.start+se.count)*Ne)),Te!==null?(Ye=Math.max(Ye,0),et=Math.min(et,Te.count)):De!=null&&(Ye=Math.max(Ye,0),et=Math.min(et,De.count));const ft=et-Ye;if(ft<0||ft===1/0)return;at.setup(V,X,Se,W,Te);let ut,Je=ye;if(Te!==null&&(ut=Q.get(Te),Je=qe,Je.setIndex(ut)),V.isMesh)X.wireframe===!0?(Me.setLineWidth(X.wireframeLinewidth*oe()),Je.setMode(I.LINES)):Je.setMode(I.TRIANGLES);else if(V.isLine){let Le=X.linewidth;Le===void 0&&(Le=1),Me.setLineWidth(Le*oe()),V.isLineSegments?Je.setMode(I.LINES):V.isLineLoop?Je.setMode(I.LINE_LOOP):Je.setMode(I.LINE_STRIP)}else V.isPoints?Je.setMode(I.POINTS):V.isSprite&&Je.setMode(I.TRIANGLES);if(V.isBatchedMesh)if(V._multiDrawInstances!==null)Vn("THREE.WebGLRenderer: renderMultiDrawInstances has been deprecated and will be removed in r184. Append to renderMultiDraw arguments and use indirection."),Je.renderMultiDrawInstances(V._multiDrawStarts,V._multiDrawCounts,V._multiDrawCount,V._multiDrawInstances);else if(Pe.get("WEBGL_multi_draw"))Je.renderMultiDraw(V._multiDrawStarts,V._multiDrawCounts,V._multiDrawCount);else{const Le=V._multiDrawStarts,Mt=V._multiDrawCounts,tt=V._multiDrawCount,Xt=Te?Q.get(Te).bytesPerElement:1,ti=Re.get(X).currentProgram.getUniforms();for(let Ut=0;Ut<tt;Ut++)ti.setValue(I,"_gl_DrawID",Ut),Je.render(Le[Ut]/Xt,Mt[Ut])}else if(V.isInstancedMesh)Je.renderInstances(Ye,ft,V.count);else if(W.isInstancedBufferGeometry){const Le=W._maxInstanceCount!==void 0?W._maxInstanceCount:1/0,Mt=Math.min(W.instanceCount,Le);Je.renderInstances(Ye,ft,Mt)}else Je.render(Ye,ft)};function nt(y,j,W){y.transparent===!0&&y.side===St&&y.forceSinglePass===!1?(y.side=Lt,y.needsUpdate=!0,er(y,j,W),y.side=Ln,y.needsUpdate=!0,er(y,j,W),y.side=St):er(y,j,W)}this.compile=function(y,j,W=null){W===null&&(W=y),u=$e.get(W),u.init(j),S.push(u),W.traverseVisible(function(V){V.isLight&&V.layers.test(j.layers)&&(u.pushLight(V),V.castShadow&&u.pushShadow(V))}),y!==W&&y.traverseVisible(function(V){V.isLight&&V.layers.test(j.layers)&&(u.pushLight(V),V.castShadow&&u.pushShadow(V))}),u.setupLights();const X=new Set;return y.traverse(function(V){if(!(V.isMesh||V.isPoints||V.isLine||V.isSprite))return;const se=V.material;if(se)if(Array.isArray(se))for(let me=0;me<se.length;me++){const Se=se[me];nt(Se,W,V),X.add(Se)}else nt(se,W,V),X.add(se)}),u=S.pop(),X},this.compileAsync=function(y,j,W=null){const X=this.compile(y,j,W);return new Promise(V=>{function se(){if(X.forEach(function(me){Re.get(me).currentProgram.isReady()&&X.delete(me)}),X.size===0){V(y);return}setTimeout(se,10)}Pe.get("KHR_parallel_shader_compile")!==null?se():setTimeout(se,10)})};let Wt=null;function rn(y){Wt&&Wt(y)}function Xs(){Un.stop()}function Ks(){Un.start()}const Un=new Hc;Un.setAnimationLoop(rn),typeof self<"u"&&Un.setContext(self),this.setAnimationLoop=function(y){Wt=y,$.setAnimationLoop(y),y===null?Un.stop():Un.start()},$.addEventListener("sessionstart",Xs),$.addEventListener("sessionend",Ks),this.render=function(y,j){if(j!==void 0&&j.isCamera!==!0){console.error("THREE.WebGLRenderer.render: camera is not an instance of THREE.Camera.");return}if(w===!0)return;if(y.matrixWorldAutoUpdate===!0&&y.updateMatrixWorld(),j.parent===null&&j.matrixWorldAutoUpdate===!0&&j.updateMatrixWorld(),$.enabled===!0&&$.isPresenting===!0&&($.cameraAutoUpdate===!0&&$.updateCamera(j),j=$.getCamera()),y.isScene===!0&&y.onBeforeRender(M,y,j,L),u=$e.get(y,S.length),u.init(j),S.push(u),ee.multiplyMatrices(j.projectionMatrix,j.matrixWorldInverse),K.setFromProjectionMatrix(ee),ue=this.localClippingEnabled,ne=le.init(this.clippingPlanes,ue),p=Ee.get(y,b.length),p.init(),b.push(p),$.enabled===!0&&$.isPresenting===!0){const se=M.xr.getDepthSensingMesh();se!==null&&Wr(se,j,-1/0,M.sortObjects)}Wr(y,j,0,M.sortObjects),p.finish(),M.sortObjects===!0&&p.sort(H,q),re=$.enabled===!1||$.isPresenting===!1||$.hasDepthSensing()===!1,re&&Ue.addToRenderList(p,y),this.info.render.frame++,ne===!0&&le.beginShadows();const W=u.state.shadowsArray;be.render(W,y,j),ne===!0&&le.endShadows(),this.info.autoReset===!0&&this.info.reset();const X=p.opaque,V=p.transmissive;if(u.setupLights(),j.isArrayCamera){const se=j.cameras;if(V.length>0)for(let me=0,Se=se.length;me<Se;me++){const Te=se[me];$s(X,V,y,Te)}re&&Ue.render(y);for(let me=0,Se=se.length;me<Se;me++){const Te=se[me];qs(p,y,Te,Te.viewport)}}else V.length>0&&$s(X,V,y,j),re&&Ue.render(y),qs(p,y,j);L!==null&&A===0&&(P.updateMultisampleRenderTarget(L),P.updateRenderTargetMipmap(L)),y.isScene===!0&&y.onAfterRender(M,y,j),at.resetDefaultState(),x=-1,v=null,S.pop(),S.length>0?(u=S[S.length-1],ne===!0&&le.setGlobalState(M.clippingPlanes,u.state.camera)):u=null,b.pop(),b.length>0?p=b[b.length-1]:p=null};function Wr(y,j,W,X){if(y.visible===!1)return;if(y.layers.test(j.layers)){if(y.isGroup)W=y.renderOrder;else if(y.isLOD)y.autoUpdate===!0&&y.update(j);else if(y.isLight)u.pushLight(y),y.castShadow&&u.pushShadow(y);else if(y.isSprite){if(!y.frustumCulled||K.intersectsSprite(y)){X&&de.setFromMatrixPosition(y.matrixWorld).applyMatrix4(ee);const me=Z.update(y),Se=y.material;Se.visible&&p.push(y,me,Se,W,de.z,null)}}else if((y.isMesh||y.isLine||y.isPoints)&&(!y.frustumCulled||K.intersectsObject(y))){const me=Z.update(y),Se=y.material;if(X&&(y.boundingSphere!==void 0?(y.boundingSphere===null&&y.computeBoundingSphere(),de.copy(y.boundingSphere.center)):(me.boundingSphere===null&&me.computeBoundingSphere(),de.copy(me.boundingSphere.center)),de.applyMatrix4(y.matrixWorld).applyMatrix4(ee)),Array.isArray(Se)){const Te=me.groups;for(let Ne=0,ke=Te.length;Ne<ke;Ne++){const De=Te[Ne],Ye=Se[De.materialIndex];Ye&&Ye.visible&&p.push(y,me,Ye,W,de.z,De)}}else Se.visible&&p.push(y,me,Se,W,de.z,null)}}const se=y.children;for(let me=0,Se=se.length;me<Se;me++)Wr(se[me],j,W,X)}function qs(y,j,W,X){const V=y.opaque,se=y.transmissive,me=y.transparent;u.setupLightsView(W),ne===!0&&le.setGlobalState(M.clippingPlanes,W),X&&Me.viewport(R.copy(X)),V.length>0&&Qi(V,j,W),se.length>0&&Qi(se,j,W),me.length>0&&Qi(me,j,W),Me.buffers.depth.setTest(!0),Me.buffers.depth.setMask(!0),Me.buffers.color.setMask(!0),Me.setPolygonOffset(!1)}function $s(y,j,W,X){if((W.isScene===!0?W.overrideMaterial:null)!==null)return;u.state.transmissionRenderTarget[X.id]===void 0&&(u.state.transmissionRenderTarget[X.id]=new ei(1,1,{generateMipmaps:!0,type:Pe.has("EXT_color_buffer_half_float")||Pe.has("EXT_color_buffer_float")?$i:vn,minFilter:Yn,samples:4,stencilBuffer:a,resolveDepthBuffer:!1,resolveStencilBuffer:!1,colorSpace:Qe.workingColorSpace}));const se=u.state.transmissionRenderTarget[X.id],me=X.viewport||R;se.setSize(me.z*M.transmissionResolutionScale,me.w*M.transmissionResolutionScale);const Se=M.getRenderTarget();M.setRenderTarget(se),M.getClearColor(D),k=M.getClearAlpha(),k<1&&M.setClearColor(16777215,.5),M.clear(),re&&Ue.render(W);const Te=M.toneMapping;M.toneMapping=Dn;const Ne=X.viewport;if(X.viewport!==void 0&&(X.viewport=void 0),u.setupLightsView(X),ne===!0&&le.setGlobalState(M.clippingPlanes,X),Qi(y,W,X),P.updateMultisampleRenderTarget(se),P.updateRenderTargetMipmap(se),Pe.has("WEBGL_multisampled_render_to_texture")===!1){let ke=!1;for(let De=0,Ye=j.length;De<Ye;De++){const et=j[De],ft=et.object,ut=et.geometry,Je=et.material,Le=et.group;if(Je.side===St&&ft.layers.test(X.layers)){const Mt=Je.side;Je.side=Lt,Je.needsUpdate=!0,Ys(ft,W,X,ut,Je,Le),Je.side=Mt,Je.needsUpdate=!0,ke=!0}}ke===!0&&(P.updateMultisampleRenderTarget(se),P.updateRenderTargetMipmap(se))}M.setRenderTarget(Se),M.setClearColor(D,k),Ne!==void 0&&(X.viewport=Ne),M.toneMapping=Te}function Qi(y,j,W){const X=j.isScene===!0?j.overrideMaterial:null;for(let V=0,se=y.length;V<se;V++){const me=y[V],Se=me.object,Te=me.geometry,Ne=X===null?me.material:X,ke=me.group;Se.layers.test(W.layers)&&Ys(Se,j,W,Te,Ne,ke)}}function Ys(y,j,W,X,V,se){y.onBeforeRender(M,j,W,X,V,se),y.modelViewMatrix.multiplyMatrices(W.matrixWorldInverse,y.matrixWorld),y.normalMatrix.getNormalMatrix(y.modelViewMatrix),V.onBeforeRender(M,j,W,X,y,se),V.transparent===!0&&V.side===St&&V.forceSinglePass===!1?(V.side=Lt,V.needsUpdate=!0,M.renderBufferDirect(W,j,X,V,y,se),V.side=Ln,V.needsUpdate=!0,M.renderBufferDirect(W,j,X,V,y,se),V.side=St):M.renderBufferDirect(W,j,X,V,y,se),y.onAfterRender(M,j,W,X,V,se)}function er(y,j,W){j.isScene!==!0&&(j=Y);const X=Re.get(y),V=u.state.lights,se=u.state.shadowsArray,me=V.state.version,Se=we.getParameters(y,V.state,se,j,W),Te=we.getProgramCacheKey(Se);let Ne=X.programs;X.environment=y.isMeshStandardMaterial?j.environment:null,X.fog=j.fog,X.envMap=(y.isMeshStandardMaterial?G:E).get(y.envMap||X.environment),X.envMapRotation=X.environment!==null&&y.envMap===null?j.environmentRotation:y.envMapRotation,Ne===void 0&&(y.addEventListener("dispose",Oe),Ne=new Map,X.programs=Ne);let ke=Ne.get(Te);if(ke!==void 0){if(X.currentProgram===ke&&X.lightsStateVersion===me)return Js(y,Se),ke}else Se.uniforms=we.getUniforms(y),y.onBeforeCompile(Se,M),ke=we.acquireProgram(Se,Te),Ne.set(Te,ke),X.uniforms=Se.uniforms;const De=X.uniforms;return(!y.isShaderMaterial&&!y.isRawShaderMaterial||y.clipping===!0)&&(De.clippingPlanes=le.uniform),Js(y,Se),X.needsLights=tl(y),X.lightsStateVersion=me,X.needsLights&&(De.ambientLightColor.value=V.state.ambient,De.lightProbe.value=V.state.probe,De.directionalLights.value=V.state.directional,De.directionalLightShadows.value=V.state.directionalShadow,De.spotLights.value=V.state.spot,De.spotLightShadows.value=V.state.spotShadow,De.rectAreaLights.value=V.state.rectArea,De.ltc_1.value=V.state.rectAreaLTC1,De.ltc_2.value=V.state.rectAreaLTC2,De.pointLights.value=V.state.point,De.pointLightShadows.value=V.state.pointShadow,De.hemisphereLights.value=V.state.hemi,De.directionalShadowMap.value=V.state.directionalShadowMap,De.directionalShadowMatrix.value=V.state.directionalShadowMatrix,De.spotShadowMap.value=V.state.spotShadowMap,De.spotLightMatrix.value=V.state.spotLightMatrix,De.spotLightMap.value=V.state.spotLightMap,De.pointShadowMap.value=V.state.pointShadowMap,De.pointShadowMatrix.value=V.state.pointShadowMatrix),X.currentProgram=ke,X.uniformsList=null,ke}function Zs(y){if(y.uniformsList===null){const j=y.currentProgram.getUniforms();y.uniformsList=Ur.seqWithValue(j.seq,y.uniforms)}return y.uniformsList}function Js(y,j){const W=Re.get(y);W.outputColorSpace=j.outputColorSpace,W.batching=j.batching,W.batchingColor=j.batchingColor,W.instancing=j.instancing,W.instancingColor=j.instancingColor,W.instancingMorph=j.instancingMorph,W.skinning=j.skinning,W.morphTargets=j.morphTargets,W.morphNormals=j.morphNormals,W.morphColors=j.morphColors,W.morphTargetsCount=j.morphTargetsCount,W.numClippingPlanes=j.numClippingPlanes,W.numIntersection=j.numClipIntersection,W.vertexAlphas=j.vertexAlphas,W.vertexTangents=j.vertexTangents,W.toneMapping=j.toneMapping}function Qc(y,j,W,X,V){j.isScene!==!0&&(j=Y),P.resetTextureUnits();const se=j.fog,me=X.isMeshStandardMaterial?j.environment:null,Se=L===null?M.outputColorSpace:L.isXRRenderTarget===!0?L.texture.colorSpace:Ci,Te=(X.isMeshStandardMaterial?G:E).get(X.envMap||me),Ne=X.vertexColors===!0&&!!W.attributes.color&&W.attributes.color.itemSize===4,ke=!!W.attributes.tangent&&(!!X.normalMap||X.anisotropy>0),De=!!W.morphAttributes.position,Ye=!!W.morphAttributes.normal,et=!!W.morphAttributes.color;let ft=Dn;X.toneMapped&&(L===null||L.isXRRenderTarget===!0)&&(ft=M.toneMapping);const ut=W.morphAttributes.position||W.morphAttributes.normal||W.morphAttributes.color,Je=ut!==void 0?ut.length:0,Le=Re.get(X),Mt=u.state.lights;if(ne===!0&&(ue===!0||y!==v)){const wt=y===v&&X.id===x;le.setState(X,y,wt)}let tt=!1;X.version===Le.__version?(Le.needsLights&&Le.lightsStateVersion!==Mt.state.version||Le.outputColorSpace!==Se||V.isBatchedMesh&&Le.batching===!1||!V.isBatchedMesh&&Le.batching===!0||V.isBatchedMesh&&Le.batchingColor===!0&&V.colorTexture===null||V.isBatchedMesh&&Le.batchingColor===!1&&V.colorTexture!==null||V.isInstancedMesh&&Le.instancing===!1||!V.isInstancedMesh&&Le.instancing===!0||V.isSkinnedMesh&&Le.skinning===!1||!V.isSkinnedMesh&&Le.skinning===!0||V.isInstancedMesh&&Le.instancingColor===!0&&V.instanceColor===null||V.isInstancedMesh&&Le.instancingColor===!1&&V.instanceColor!==null||V.isInstancedMesh&&Le.instancingMorph===!0&&V.morphTexture===null||V.isInstancedMesh&&Le.instancingMorph===!1&&V.morphTexture!==null||Le.envMap!==Te||X.fog===!0&&Le.fog!==se||Le.numClippingPlanes!==void 0&&(Le.numClippingPlanes!==le.numPlanes||Le.numIntersection!==le.numIntersection)||Le.vertexAlphas!==Ne||Le.vertexTangents!==ke||Le.morphTargets!==De||Le.morphNormals!==Ye||Le.morphColors!==et||Le.toneMapping!==ft||Le.morphTargetsCount!==Je)&&(tt=!0):(tt=!0,Le.__version=X.version);let Xt=Le.currentProgram;tt===!0&&(Xt=er(X,j,V));let ti=!1,Ut=!1,ki=!1;const st=Xt.getUniforms(),Bt=Le.uniforms;if(Me.useProgram(Xt.program)&&(ti=!0,Ut=!0,ki=!0),X.id!==x&&(x=X.id,Ut=!0),ti||v!==y){Me.buffers.depth.getReversed()?(ae.copy(y.projectionMatrix),iu(ae),ru(ae),st.setValue(I,"projectionMatrix",ae)):st.setValue(I,"projectionMatrix",y.projectionMatrix),st.setValue(I,"viewMatrix",y.matrixWorldInverse);const Pt=st.map.cameraPosition;Pt!==void 0&&Pt.setValue(I,_e.setFromMatrixPosition(y.matrixWorld)),Ce.logarithmicDepthBuffer&&st.setValue(I,"logDepthBufFC",2/(Math.log(y.far+1)/Math.LN2)),(X.isMeshPhongMaterial||X.isMeshToonMaterial||X.isMeshLambertMaterial||X.isMeshBasicMaterial||X.isMeshStandardMaterial||X.isShaderMaterial)&&st.setValue(I,"isOrthographic",y.isOrthographicCamera===!0),v!==y&&(v=y,Ut=!0,ki=!0)}if(V.isSkinnedMesh){st.setOptional(I,V,"bindMatrix"),st.setOptional(I,V,"bindMatrixInverse");const wt=V.skeleton;wt&&(wt.boneTexture===null&&wt.computeBoneTexture(),st.setValue(I,"boneTexture",wt.boneTexture,P))}V.isBatchedMesh&&(st.setOptional(I,V,"batchingTexture"),st.setValue(I,"batchingTexture",V._matricesTexture,P),st.setOptional(I,V,"batchingIdTexture"),st.setValue(I,"batchingIdTexture",V._indirectTexture,P),st.setOptional(I,V,"batchingColorTexture"),V._colorsTexture!==null&&st.setValue(I,"batchingColorTexture",V._colorsTexture,P));const jt=W.morphAttributes;if((jt.position!==void 0||jt.normal!==void 0||jt.color!==void 0)&&ze.update(V,W,Xt),(Ut||Le.receiveShadow!==V.receiveShadow)&&(Le.receiveShadow=V.receiveShadow,st.setValue(I,"receiveShadow",V.receiveShadow)),X.isMeshGouraudMaterial&&X.envMap!==null&&(Bt.envMap.value=Te,Bt.flipEnvMap.value=Te.isCubeTexture&&Te.isRenderTargetTexture===!1?-1:1),X.isMeshStandardMaterial&&X.envMap===null&&j.environment!==null&&(Bt.envMapIntensity.value=j.environmentIntensity),Ut&&(st.setValue(I,"toneMappingExposure",M.toneMappingExposure),Le.needsLights&&el(Bt,ki),se&&X.fog===!0&&ge.refreshFogUniforms(Bt,se),ge.refreshMaterialUniforms(Bt,X,z,O,u.state.transmissionRenderTarget[y.id]),Ur.upload(I,Zs(Le),Bt,P)),X.isShaderMaterial&&X.uniformsNeedUpdate===!0&&(Ur.upload(I,Zs(Le),Bt,P),X.uniformsNeedUpdate=!1),X.isSpriteMaterial&&st.setValue(I,"center",V.center),st.setValue(I,"modelViewMatrix",V.modelViewMatrix),st.setValue(I,"normalMatrix",V.normalMatrix),st.setValue(I,"modelMatrix",V.matrixWorld),X.isShaderMaterial||X.isRawShaderMaterial){const wt=X.uniformsGroups;for(let Pt=0,Xr=wt.length;Pt<Xr;Pt++){const zn=wt[Pt];B.update(zn,Xt),B.bind(zn,Xt)}}return Xt}function el(y,j){y.ambientLightColor.needsUpdate=j,y.lightProbe.needsUpdate=j,y.directionalLights.needsUpdate=j,y.directionalLightShadows.needsUpdate=j,y.pointLights.needsUpdate=j,y.pointLightShadows.needsUpdate=j,y.spotLights.needsUpdate=j,y.spotLightShadows.needsUpdate=j,y.rectAreaLights.needsUpdate=j,y.hemisphereLights.needsUpdate=j}function tl(y){return y.isMeshLambertMaterial||y.isMeshToonMaterial||y.isMeshPhongMaterial||y.isMeshStandardMaterial||y.isShadowMaterial||y.isShaderMaterial&&y.lights===!0}this.getActiveCubeFace=function(){return T},this.getActiveMipmapLevel=function(){return A},this.getRenderTarget=function(){return L},this.setRenderTargetTextures=function(y,j,W){Re.get(y.texture).__webglTexture=j,Re.get(y.depthTexture).__webglTexture=W;const X=Re.get(y);X.__hasExternalTextures=!0,X.__autoAllocateDepthBuffer=W===void 0,X.__autoAllocateDepthBuffer||Pe.has("WEBGL_multisampled_render_to_texture")===!0&&(console.warn("THREE.WebGLRenderer: Render-to-texture extension was disabled because an external texture was provided"),X.__useRenderToTexture=!1)},this.setRenderTargetFramebuffer=function(y,j){const W=Re.get(y);W.__webglFramebuffer=j,W.__useDefaultFramebuffer=j===void 0};const nl=I.createFramebuffer();this.setRenderTarget=function(y,j=0,W=0){L=y,T=j,A=W;let X=!0,V=null,se=!1,me=!1;if(y){const Te=Re.get(y);if(Te.__useDefaultFramebuffer!==void 0)Me.bindFramebuffer(I.FRAMEBUFFER,null),X=!1;else if(Te.__webglFramebuffer===void 0)P.setupRenderTarget(y);else if(Te.__hasExternalTextures)P.rebindTextures(y,Re.get(y.texture).__webglTexture,Re.get(y.depthTexture).__webglTexture);else if(y.depthBuffer){const De=y.depthTexture;if(Te.__boundDepthTexture!==De){if(De!==null&&Re.has(De)&&(y.width!==De.image.width||y.height!==De.image.height))throw new Error("WebGLRenderTarget: Attached DepthTexture is initialized to the incorrect size.");P.setupDepthRenderbuffer(y)}}const Ne=y.texture;(Ne.isData3DTexture||Ne.isDataArrayTexture||Ne.isCompressedArrayTexture)&&(me=!0);const ke=Re.get(y).__webglFramebuffer;y.isWebGLCubeRenderTarget?(Array.isArray(ke[j])?V=ke[j][W]:V=ke[j],se=!0):y.samples>0&&P.useMultisampledRTT(y)===!1?V=Re.get(y).__webglMultisampledFramebuffer:Array.isArray(ke)?V=ke[W]:V=ke,R.copy(y.viewport),U.copy(y.scissor),C=y.scissorTest}else R.copy(J).multiplyScalar(z).floor(),U.copy(fe).multiplyScalar(z).floor(),C=Ae;if(W!==0&&(V=nl),Me.bindFramebuffer(I.FRAMEBUFFER,V)&&X&&Me.drawBuffers(y,V),Me.viewport(R),Me.scissor(U),Me.setScissorTest(C),se){const Te=Re.get(y.texture);I.framebufferTexture2D(I.FRAMEBUFFER,I.COLOR_ATTACHMENT0,I.TEXTURE_CUBE_MAP_POSITIVE_X+j,Te.__webglTexture,W)}else if(me){const Te=Re.get(y.texture),Ne=j;I.framebufferTextureLayer(I.FRAMEBUFFER,I.COLOR_ATTACHMENT0,Te.__webglTexture,W,Ne)}else if(y!==null&&W!==0){const Te=Re.get(y.texture);I.framebufferTexture2D(I.FRAMEBUFFER,I.COLOR_ATTACHMENT0,I.TEXTURE_2D,Te.__webglTexture,W)}x=-1},this.readRenderTargetPixels=function(y,j,W,X,V,se,me){if(!(y&&y.isWebGLRenderTarget)){console.error("THREE.WebGLRenderer.readRenderTargetPixels: renderTarget is not THREE.WebGLRenderTarget.");return}let Se=Re.get(y).__webglFramebuffer;if(y.isWebGLCubeRenderTarget&&me!==void 0&&(Se=Se[me]),Se){Me.bindFramebuffer(I.FRAMEBUFFER,Se);try{const Te=y.texture,Ne=Te.format,ke=Te.type;if(!Ce.textureFormatReadable(Ne)){console.error("THREE.WebGLRenderer.readRenderTargetPixels: renderTarget is not in RGBA or implementation defined format.");return}if(!Ce.textureTypeReadable(ke)){console.error("THREE.WebGLRenderer.readRenderTargetPixels: renderTarget is not in UnsignedByteType or implementation defined type.");return}j>=0&&j<=y.width-X&&W>=0&&W<=y.height-V&&I.readPixels(j,W,X,V,je.convert(Ne),je.convert(ke),se)}finally{const Te=L!==null?Re.get(L).__webglFramebuffer:null;Me.bindFramebuffer(I.FRAMEBUFFER,Te)}}},this.readRenderTargetPixelsAsync=async function(y,j,W,X,V,se,me){if(!(y&&y.isWebGLRenderTarget))throw new Error("THREE.WebGLRenderer.readRenderTargetPixels: renderTarget is not THREE.WebGLRenderTarget.");let Se=Re.get(y).__webglFramebuffer;if(y.isWebGLCubeRenderTarget&&me!==void 0&&(Se=Se[me]),Se){const Te=y.texture,Ne=Te.format,ke=Te.type;if(!Ce.textureFormatReadable(Ne))throw new Error("THREE.WebGLRenderer.readRenderTargetPixelsAsync: renderTarget is not in RGBA or implementation defined format.");if(!Ce.textureTypeReadable(ke))throw new Error("THREE.WebGLRenderer.readRenderTargetPixelsAsync: renderTarget is not in UnsignedByteType or implementation defined type.");if(j>=0&&j<=y.width-X&&W>=0&&W<=y.height-V){Me.bindFramebuffer(I.FRAMEBUFFER,Se);const De=I.createBuffer();I.bindBuffer(I.PIXEL_PACK_BUFFER,De),I.bufferData(I.PIXEL_PACK_BUFFER,se.byteLength,I.STREAM_READ),I.readPixels(j,W,X,V,je.convert(Ne),je.convert(ke),0);const Ye=L!==null?Re.get(L).__webglFramebuffer:null;Me.bindFramebuffer(I.FRAMEBUFFER,Ye);const et=I.fenceSync(I.SYNC_GPU_COMMANDS_COMPLETE,0);return I.flush(),await nu(I,et,4),I.bindBuffer(I.PIXEL_PACK_BUFFER,De),I.getBufferSubData(I.PIXEL_PACK_BUFFER,0,se),I.deleteBuffer(De),I.deleteSync(et),se}else throw new Error("THREE.WebGLRenderer.readRenderTargetPixelsAsync: requested read bounds are out of range.")}},this.copyFramebufferToTexture=function(y,j=null,W=0){y.isTexture!==!0&&(Vn("WebGLRenderer: copyFramebufferToTexture function signature has changed."),j=arguments[0]||null,y=arguments[1]);const X=Math.pow(2,-W),V=Math.floor(y.image.width*X),se=Math.floor(y.image.height*X),me=j!==null?j.x:0,Se=j!==null?j.y:0;P.setTexture2D(y,0),I.copyTexSubImage2D(I.TEXTURE_2D,W,0,0,me,Se,V,se),Me.unbindTexture()};const il=I.createFramebuffer(),rl=I.createFramebuffer();this.copyTextureToTexture=function(y,j,W=null,X=null,V=0,se=null){y.isTexture!==!0&&(Vn("WebGLRenderer: copyTextureToTexture function signature has changed."),X=arguments[0]||null,y=arguments[1],j=arguments[2],se=arguments[3]||0,W=null),se===null&&(V!==0?(Vn("WebGLRenderer: copyTextureToTexture function signature has changed to support src and dst mipmap levels."),se=V,V=0):se=0);let me,Se,Te,Ne,ke,De,Ye,et,ft;const ut=y.isCompressedTexture?y.mipmaps[se]:y.image;if(W!==null)me=W.max.x-W.min.x,Se=W.max.y-W.min.y,Te=W.isBox3?W.max.z-W.min.z:1,Ne=W.min.x,ke=W.min.y,De=W.isBox3?W.min.z:0;else{const jt=Math.pow(2,-V);me=Math.floor(ut.width*jt),Se=Math.floor(ut.height*jt),y.isDataArrayTexture?Te=ut.depth:y.isData3DTexture?Te=Math.floor(ut.depth*jt):Te=1,Ne=0,ke=0,De=0}X!==null?(Ye=X.x,et=X.y,ft=X.z):(Ye=0,et=0,ft=0);const Je=je.convert(j.format),Le=je.convert(j.type);let Mt;j.isData3DTexture?(P.setTexture3D(j,0),Mt=I.TEXTURE_3D):j.isDataArrayTexture||j.isCompressedArrayTexture?(P.setTexture2DArray(j,0),Mt=I.TEXTURE_2D_ARRAY):(P.setTexture2D(j,0),Mt=I.TEXTURE_2D),I.pixelStorei(I.UNPACK_FLIP_Y_WEBGL,j.flipY),I.pixelStorei(I.UNPACK_PREMULTIPLY_ALPHA_WEBGL,j.premultiplyAlpha),I.pixelStorei(I.UNPACK_ALIGNMENT,j.unpackAlignment);const tt=I.getParameter(I.UNPACK_ROW_LENGTH),Xt=I.getParameter(I.UNPACK_IMAGE_HEIGHT),ti=I.getParameter(I.UNPACK_SKIP_PIXELS),Ut=I.getParameter(I.UNPACK_SKIP_ROWS),ki=I.getParameter(I.UNPACK_SKIP_IMAGES);I.pixelStorei(I.UNPACK_ROW_LENGTH,ut.width),I.pixelStorei(I.UNPACK_IMAGE_HEIGHT,ut.height),I.pixelStorei(I.UNPACK_SKIP_PIXELS,Ne),I.pixelStorei(I.UNPACK_SKIP_ROWS,ke),I.pixelStorei(I.UNPACK_SKIP_IMAGES,De);const st=y.isDataArrayTexture||y.isData3DTexture,Bt=j.isDataArrayTexture||j.isData3DTexture;if(y.isDepthTexture){const jt=Re.get(y),wt=Re.get(j),Pt=Re.get(jt.__renderTarget),Xr=Re.get(wt.__renderTarget);Me.bindFramebuffer(I.READ_FRAMEBUFFER,Pt.__webglFramebuffer),Me.bindFramebuffer(I.DRAW_FRAMEBUFFER,Xr.__webglFramebuffer);for(let zn=0;zn<Te;zn++)st&&(I.framebufferTextureLayer(I.READ_FRAMEBUFFER,I.COLOR_ATTACHMENT0,Re.get(y).__webglTexture,V,De+zn),I.framebufferTextureLayer(I.DRAW_FRAMEBUFFER,I.COLOR_ATTACHMENT0,Re.get(j).__webglTexture,se,ft+zn)),I.blitFramebuffer(Ne,ke,me,Se,Ye,et,me,Se,I.DEPTH_BUFFER_BIT,I.NEAREST);Me.bindFramebuffer(I.READ_FRAMEBUFFER,null),Me.bindFramebuffer(I.DRAW_FRAMEBUFFER,null)}else if(V!==0||y.isRenderTargetTexture||Re.has(y)){const jt=Re.get(y),wt=Re.get(j);Me.bindFramebuffer(I.READ_FRAMEBUFFER,il),Me.bindFramebuffer(I.DRAW_FRAMEBUFFER,rl);for(let Pt=0;Pt<Te;Pt++)st?I.framebufferTextureLayer(I.READ_FRAMEBUFFER,I.COLOR_ATTACHMENT0,jt.__webglTexture,V,De+Pt):I.framebufferTexture2D(I.READ_FRAMEBUFFER,I.COLOR_ATTACHMENT0,I.TEXTURE_2D,jt.__webglTexture,V),Bt?I.framebufferTextureLayer(I.DRAW_FRAMEBUFFER,I.COLOR_ATTACHMENT0,wt.__webglTexture,se,ft+Pt):I.framebufferTexture2D(I.DRAW_FRAMEBUFFER,I.COLOR_ATTACHMENT0,I.TEXTURE_2D,wt.__webglTexture,se),V!==0?I.blitFramebuffer(Ne,ke,me,Se,Ye,et,me,Se,I.COLOR_BUFFER_BIT,I.NEAREST):Bt?I.copyTexSubImage3D(Mt,se,Ye,et,ft+Pt,Ne,ke,me,Se):I.copyTexSubImage2D(Mt,se,Ye,et,Ne,ke,me,Se);Me.bindFramebuffer(I.READ_FRAMEBUFFER,null),Me.bindFramebuffer(I.DRAW_FRAMEBUFFER,null)}else Bt?y.isDataTexture||y.isData3DTexture?I.texSubImage3D(Mt,se,Ye,et,ft,me,Se,Te,Je,Le,ut.data):j.isCompressedArrayTexture?I.compressedTexSubImage3D(Mt,se,Ye,et,ft,me,Se,Te,Je,ut.data):I.texSubImage3D(Mt,se,Ye,et,ft,me,Se,Te,Je,Le,ut):y.isDataTexture?I.texSubImage2D(I.TEXTURE_2D,se,Ye,et,me,Se,Je,Le,ut.data):y.isCompressedTexture?I.compressedTexSubImage2D(I.TEXTURE_2D,se,Ye,et,ut.width,ut.height,Je,ut.data):I.texSubImage2D(I.TEXTURE_2D,se,Ye,et,me,Se,Je,Le,ut);I.pixelStorei(I.UNPACK_ROW_LENGTH,tt),I.pixelStorei(I.UNPACK_IMAGE_HEIGHT,Xt),I.pixelStorei(I.UNPACK_SKIP_PIXELS,ti),I.pixelStorei(I.UNPACK_SKIP_ROWS,Ut),I.pixelStorei(I.UNPACK_SKIP_IMAGES,ki),se===0&&j.generateMipmaps&&I.generateMipmap(Mt),Me.unbindTexture()},this.copyTextureToTexture3D=function(y,j,W=null,X=null,V=0){return y.isTexture!==!0&&(Vn("WebGLRenderer: copyTextureToTexture3D function signature has changed."),W=arguments[0]||null,X=arguments[1]||null,y=arguments[2],j=arguments[3],V=arguments[4]||0),Vn('WebGLRenderer: copyTextureToTexture3D function has been deprecated. Use "copyTextureToTexture" instead.'),this.copyTextureToTexture(y,j,W,X,V)},this.initRenderTarget=function(y){Re.get(y).__webglFramebuffer===void 0&&P.setupRenderTarget(y)},this.initTexture=function(y){y.isCubeTexture?P.setTextureCube(y,0):y.isData3DTexture?P.setTexture3D(y,0):y.isDataArrayTexture||y.isCompressedArrayTexture?P.setTexture2DArray(y,0):P.setTexture2D(y,0),Me.unbindTexture()},this.resetState=function(){T=0,A=0,L=null,Me.reset(),at.reset()},typeof __THREE_DEVTOOLS__<"u"&&__THREE_DEVTOOLS__.dispatchEvent(new CustomEvent("observe",{detail:this}))}get coordinateSystem(){return mn}get outputColorSpace(){return this._outputColorSpace}set outputColorSpace(e){this._outputColorSpace=e;const t=this.getContext();t.drawingBufferColorspace=Qe._getDrawingBufferColorSpace(e),t.unpackColorSpace=Qe._getUnpackColorSpace()}}const wn=1e-6,xi=5e-5,Aa=1e-7;function Ss(n,e){return n[0]*e[0]+n[1]*e[1]+n[2]*e[2]}function Es(n,e){return[n[0]-e[0],n[1]-e[1],n[2]-e[2]]}function bs(n,e){return[n[1]*e[2]-n[2]*e[1],n[2]*e[0]-n[0]*e[2],n[0]*e[1]-n[1]*e[0]]}function bm(n){const e=Math.hypot(n[0],n[1],n[2]);return e<1e-12?null:[n[0]/e,n[1]/e,n[2]/e]}function zr(n,e){const t=n[0]-e[0],i=n[1]-e[1],r=n[2]-e[2];return t*t+i*i+r*r}function Ra(n){if(n.length<3)return 0;const e=n[0];let t=0,i=0,r=0;for(let a=1;a+1<n.length;a++){const s=Es(n[a],e),o=Es(n[a+1],e),c=bs(s,o);t+=c[0],i+=c[1],r+=c[2]}return .5*Math.hypot(t,i,r)}function ym(n,e){const t=[],i=xi*xi;for(const f of n)t.some(m=>zr(f,m)<=i)||t.push(f);if(t.length<3)return[];let r=0,a=0,s=0;for(const f of t)r+=f[0],a+=f[1],s+=f[2];r/=t.length,a/=t.length,s/=t.length;const o=[r,a,s],c=Math.abs(e[0])<.8?[1,0,0]:[0,1,0],l=bm(bs(c,e));if(!l)return[];const d=bs(e,l),h=t.map(f=>{const m=Es(f,o),g=Ss(m,l),_=Ss(m,d);return{tacka:f,ugao:Math.atan2(_,g)}});return h.sort((f,m)=>f.ugao-m.ugao),h.map(f=>f.tacka)}function Tm(n){return[{normala:[1,0,0],grupaId:"__okvir__",oznaka:"",temena:[[n,-n,-n],[n,n,-n],[n,n,n],[n,-n,n]]},{normala:[-1,0,0],grupaId:"__okvir__",oznaka:"",temena:[[-n,-n,n],[-n,n,n],[-n,n,-n],[-n,-n,-n]]},{normala:[0,1,0],grupaId:"__okvir__",oznaka:"",temena:[[-n,n,-n],[-n,n,n],[n,n,n],[n,n,-n]]},{normala:[0,-1,0],grupaId:"__okvir__",oznaka:"",temena:[[-n,-n,n],[-n,-n,-n],[n,-n,-n],[n,-n,n]]},{normala:[0,0,1],grupaId:"__okvir__",oznaka:"",temena:[[-n,-n,n],[n,-n,n],[n,n,n],[-n,n,n]]},{normala:[0,0,-1],grupaId:"__okvir__",oznaka:"",temena:[[n,-n,-n],[-n,-n,-n],[-n,n,-n],[n,n,-n]]}]}function Ki(n){if(n.length===0)return{temena:[],pljosni:[]};let e=1;const t=[];for(let c=0;c<n.length;c++){const l=n[c],d=Math.hypot(l.normala[0],l.normala[1],l.normala[2]);if(d<1e-12)continue;const h=[l.normala[0]/d,l.normala[1]/d,l.normala[2]/d],f=l.d;e=Math.max(e,Math.abs(f)),t.push({normala:h,d:f,grupaId:l.grupaId??`forma-${c}`,oznaka:l.oznaka??""})}let i=Tm(Math.max(12,e*6));for(const c of t){const l=[],d=[];for(const f of i){const m=f.temena.length;if(m<3)continue;const g=f.temena.map(b=>Ss(c.normala,b)-c.d),_=[];for(let b=0;b<m;b++){const S=(b+1)%m,M=f.temena[b],w=f.temena[S],T=g[b],A=g[S],L=T<=wn,x=A<=wn;if(Math.abs(T)<=wn*4&&d.push(M),L&&_.push(M),T<-wn&&A>wn||T>wn&&A<-wn){const v=T/(T-A),R=[M[0]+(w[0]-M[0])*v,M[1]+(w[1]-M[1])*v,M[2]+(w[2]-M[2])*v];_.push(R),d.push(R)}else!L&&x&&Math.abs(A)<=wn&&d.push(w)}const p=[],u=xi*xi;for(const b of _)(p.length===0||zr(b,p[p.length-1])>u)&&p.push(b);p.length>1&&zr(p[0],p[p.length-1])<=u&&p.pop(),p.length>=3&&Ra(p)>Aa&&l.push({temena:p,normala:f.normala,grupaId:f.grupaId,oznaka:f.oznaka})}const h=ym(d,c.normala);if(h.length>=3&&Ra(h)>Aa&&l.push({temena:h,normala:c.normala,grupaId:c.grupaId,oznaka:c.oznaka}),i=l,i.length===0)break}const r=[],a=[],s=xi*xi;function o(c){for(let l=0;l<r.length;l++)if(zr(r[l],c)<=s)return l;return r.push([Math.abs(c[0])<1e-10?0:c[0],Math.abs(c[1])<1e-10?0:c[1],Math.abs(c[2])<1e-10?0:c[2]]),r.length-1}for(const c of i){if(c.grupaId==="__okvir__")continue;const l=Ra(c.temena);if(l<=Aa)continue;const d=c.temena.map(p=>o(p)),h=[];for(const p of d)(h.length===0||h[h.length-1]!==p)&&h.push(p);if(h.length>1&&h[0]===h[h.length-1]&&h.pop(),h.length<3)continue;let f=0,m=0,g=0;for(const p of h){const u=r[p];f+=u[0],m+=u[1],g+=u[2]}const _=h.length;a.push({indeksiTemena:h,normala:c.normala,centar:[f/_,m/_,g/_],povrsina:l,grupaId:c.grupaId,oznaka:c.oznaka})}return{temena:r,pljosni:a}}function qi(n){const e=[];for(const d of n.pljosni)e.includes(d.grupaId)||e.push(d.grupaId);const t=[],i=[],r=[],a=[];for(let d=0;d<e.length;d++){const h=e[d],f=t.length/3;for(let g=0;g<n.pljosni.length;g++){const _=n.pljosni[g];if(_.grupaId!==h)continue;const p=_.indeksiTemena;if(p.length<3)continue;const u=n.temena[p[0]],[b,S,M]=_.normala;for(let w=1;w+1<p.length;w++){const T=n.temena[p[w]],A=n.temena[p[w+1]];t.push(u[0],u[1],u[2],T[0],T[1],T[2],A[0],A[1],A[2]),i.push(b,S,M,b,S,M,b,S,M),r.push(g)}}const m=t.length/3;m>f&&a.push({pocetak:f,broj:m-f,indeksMaterijala:d})}const s=new Ze;s.setAttribute("position",new He(t,3)),s.setAttribute("normal",new He(i,3));for(const d of a)s.addGroup(d.pocetak,d.broj,d.indeksMaterijala);const o=new Set,c=[];for(const d of n.pljosni){const h=d.indeksiTemena;for(let f=0;f<h.length;f++){const m=h[f],g=h[(f+1)%h.length],_=m<g?`${m}-${g}`:`${g}-${m}`;if(o.has(_))continue;o.add(_);const p=n.temena[m],u=n.temena[g];c.push(p[0],p[1],p[2],u[0],u[1],u[2])}}const l=new Ze;return l.setAttribute("position",new He(c,3)),{geometrijaMreze:s,geometrijaIvica:l,mapaTrougaoUPljosan:r,redosledGrupa:e}}function gi(n,e,t){return Math.max(e,Math.min(t,n))}class wm{stanje;pocetno;minUdaljenost;maksUdaljenost;opcije;vuceMisem=!1;prethodniX=0;prethodniY=0;dodirAktiviran=!1;prethodniDodirX=0;prethodniDodirY=0;prethodniRazmakPrstiju=0;pocetakDodiraX=0;pocetakDodiraY=0;dodirPomeren=!1;cistaci=[];constructor(e){this.opcije=e,this.pocetno={...e.pocetno},this.stanje={...e.pocetno},this.minUdaljenost=e.minUdaljenost??2,this.maksUdaljenost=e.maksUdaljenost??24,this.poveziDogadjaje()}trenutnoStanje(){return{...this.stanje}}rotirajAzimut(e){this.stanje.theta+=e,this.opcije.naPromenu(this.trenutnoStanje())}rotirajElevaciju(e){this.stanje.phi=gi(this.stanje.phi+e,.15,Math.PI-.15),this.opcije.naPromenu(this.trenutnoStanje())}zumiraj(e){this.stanje.udaljenost=gi(this.stanje.udaljenost*e,this.minUdaljenost,this.maksUdaljenost),this.opcije.naPromenu(this.trenutnoStanje())}resetuj(){this.stanje={...this.pocetno},this.opcije.naPromenu(this.trenutnoStanje())}postaviAktivacijuDodira(e){this.dodirAktiviran=e,this.opcije.platno.classList.toggle("udzbenik-scena-platno--dodir-aktivan",e),this.opcije.dugmeDodira.hidden=!e,this.opcije.priPromeniAktivacijeDodira?.(e)}poveziDogadjaje(){const{bina:e,platno:t,dugmeDodira:i}=this.opcije,r=g=>{if(g.pointerType!=="touch"&&g.button===0){this.vuceMisem=!0,this.prethodniX=g.clientX,this.prethodniY=g.clientY;try{t.setPointerCapture(g.pointerId)}catch{}}},a=g=>{if(g.pointerType==="touch"||!this.vuceMisem)return;const _=g.clientX-this.prethodniX,p=g.clientY-this.prethodniY;this.prethodniX=g.clientX,this.prethodniY=g.clientY,this.stanje.theta-=_*.008,this.stanje.phi=gi(this.stanje.phi-p*.008,.15,Math.PI-.15),this.opcije.naPromenu(this.trenutnoStanje())},s=g=>{if(g.pointerType!=="touch"){this.vuceMisem=!1;try{t.hasPointerCapture(g.pointerId)&&t.releasePointerCapture(g.pointerId)}catch{}}},o=g=>{if(!(document.activeElement===e||e.contains(document.activeElement))&&!g.ctrlKey&&!g.metaKey)return;g.preventDefault();const p=g.deltaY>0?1.09:.92;this.zumiraj(p)},c=g=>{if(g.touches.length===2){const _=g.touches[0],p=g.touches[1];this.prethodniDodirX=(_.clientX+p.clientX)/2,this.prethodniDodirY=(_.clientY+p.clientY)/2,this.prethodniRazmakPrstiju=Math.hypot(p.clientX-_.clientX,p.clientY-_.clientY)}else if(g.touches.length===1){const _=g.touches[0];this.pocetakDodiraX=_.clientX,this.pocetakDodiraY=_.clientY,this.prethodniDodirX=_.clientX,this.prethodniDodirY=_.clientY,this.dodirPomeren=!1}},l=g=>{if(g.touches.length===2){g.preventDefault();const _=g.touches[0],p=g.touches[1],u=(_.clientX+p.clientX)/2,b=(_.clientY+p.clientY)/2,S=Math.hypot(p.clientX-_.clientX,p.clientY-_.clientY),M=u-this.prethodniDodirX,w=b-this.prethodniDodirY;if(this.prethodniDodirX=u,this.prethodniDodirY=b,this.stanje.theta-=M*.008,this.stanje.phi=gi(this.stanje.phi-w*.008,.15,Math.PI-.15),this.prethodniRazmakPrstiju>8&&S>8){const T=this.prethodniRazmakPrstiju/S;this.stanje.udaljenost=gi(this.stanje.udaljenost*T,this.minUdaljenost,this.maksUdaljenost)}this.prethodniRazmakPrstiju=S,this.dodirPomeren=!0,this.opcije.naPromenu(this.trenutnoStanje())}else if(g.touches.length===1){const _=g.touches[0];if(Math.hypot(_.clientX-this.pocetakDodiraX,_.clientY-this.pocetakDodiraY)>8&&(this.dodirPomeren=!0),this.dodirAktiviran){g.preventDefault();const p=_.clientX-this.prethodniDodirX,u=_.clientY-this.prethodniDodirY;this.prethodniDodirX=_.clientX,this.prethodniDodirY=_.clientY,this.stanje.theta-=p*.009,this.stanje.phi=gi(this.stanje.phi-u*.009,.15,Math.PI-.15),this.opcije.naPromenu(this.trenutnoStanje())}}},d=g=>{g.touches.length===0&&!this.dodirPomeren&&g.changedTouches.length===1&&this.postaviAktivacijuDodira(!this.dodirAktiviran)},h=()=>{this.postaviAktivacijuDodira(!1)},f=g=>{this.dodirAktiviran&&g.target instanceof Node&&!e.contains(g.target)&&this.postaviAktivacijuDodira(!1)},m=g=>{if(!(g.target instanceof HTMLElement&&g.target!==e&&(g.target.tagName==="BUTTON"||g.target.tagName==="INPUT")))switch(g.key){case"ArrowLeft":g.preventDefault(),this.rotirajAzimut(-.12);break;case"ArrowRight":g.preventDefault(),this.rotirajAzimut(.12);break;case"ArrowUp":g.preventDefault(),this.rotirajElevaciju(-.12);break;case"ArrowDown":g.preventDefault(),this.rotirajElevaciju(.12);break;case"+":case"=":g.preventDefault(),this.zumiraj(.88);break;case"-":case"_":g.preventDefault(),this.zumiraj(1.14);break;case"r":case"R":case"р":case"Р":g.preventDefault(),this.opcije.naReset();break;case" ":g.preventDefault(),this.opcije.naPrekidacPauze();break;case"Escape":this.dodirAktiviran&&(g.preventDefault(),this.postaviAktivacijuDodira(!1));break}};t.addEventListener("pointerdown",r),t.addEventListener("pointermove",a),t.addEventListener("pointerup",s),t.addEventListener("pointercancel",s),t.addEventListener("wheel",o,{passive:!1}),t.addEventListener("touchstart",c,{passive:!0}),t.addEventListener("touchmove",l,{passive:!1}),t.addEventListener("touchend",d),i.addEventListener("click",h),document.addEventListener("touchstart",f,{passive:!0}),e.addEventListener("keydown",m),this.cistaci.push(()=>{t.removeEventListener("pointerdown",r),t.removeEventListener("pointermove",a),t.removeEventListener("pointerup",s),t.removeEventListener("pointercancel",s),t.removeEventListener("wheel",o),t.removeEventListener("touchstart",c),t.removeEventListener("touchmove",l),t.removeEventListener("touchend",d),i.removeEventListener("click",h),document.removeEventListener("touchstart",f),e.removeEventListener("keydown",m)})}raspolazi(){for(const e of this.cistaci)e();this.cistaci.length=0}}let fn=null,Mi=null,Zn=0,Jn=0;function Am(){if(fn)return fn;const n=document.createElement("canvas"),e=n.getContext("webgl2",{antialias:!0,alpha:!1,preserveDrawingBuffer:!1})??n.getContext("webgl",{antialias:!0,alpha:!1,preserveDrawingBuffer:!1});if(!e)throw new Error("WebGL контекст није доступан у овом прегледачу.");const t=new Em({canvas:n,context:e,antialias:!0,alpha:!1,powerPreference:"default"});return t.setPixelRatio(1),t.outputColorSpace=Ft,Mi=n,fn=t,Zn=320,Jn=240,fn.setSize(Zn,Jn,!1),fn}function Rm(){fn&&(fn.forceContextLoss(),fn.dispose(),fn=null,Mi=null,Zn=0,Jn=0)}function It(n){n.traverse(e=>{const t=e;t.geometry&&typeof t.geometry.dispose=="function"&&t.geometry.dispose();const i=t.material;if(Array.isArray(i))for(const r of i)sc(r);else i&&sc(i)})}function sc(n){for(const e of Object.values(n))e instanceof Ct&&e.dispose();n.dispose()}function Cm(n,e,t,i){const r=Am(),a=t.platno.getContext("2d");if(!a||!Mi)throw new Error("2D контекст платна није доступан.");const s=typeof window<"u"&&typeof window.matchMedia=="function"&&window.matchMedia("(prefers-reduced-motion: reduce)").matches,o=new Cu,c=new Ht(42,16/9,.1,100),l=new F(0,0,0),d=new ku(new ce(1,1,1),.72),h=new Lo(new ce(1,1,1),.95);h.position.set(5,8,6);const f=new Lo(new ce(1,1,1),.38);f.position.set(-5,-3,-4),o.add(d,h,f);const m=n.pocetnaKamera?.(e)??{theta:.62,phi:1.12,udaljenost:6.2};function g(ee){const _e=Math.sin(ee.phi);c.position.set(l.x+ee.udaljenost*_e*Math.sin(ee.theta),l.y+ee.udaljenost*Math.cos(ee.phi),l.z+ee.udaljenost*_e*Math.cos(ee.theta)),c.lookAt(l),c.updateMatrixWorld()}g(m);let _=!1,p=!1,u=!0,b=n.imaPodrazumevanuAnimaciju?n.imaPodrazumevanuAnimaciju(e):!0,S=s||!b,M=null,w=null,T=0,A=0,L=Math.max(240,t.bina.clientWidth||600),x=Math.max(180,t.bina.clientHeight||360),v=null;function R(){if(_||p||!Mi||!a)return;const ee=t.bina.clientWidth,_e=t.bina.clientHeight;ee>0&&_e>0&&(L=ee,x=_e);const de=Math.min(typeof window<"u"&&window.devicePixelRatio||1,2),Y=Math.max(1,Math.round(L*de)),re=Math.max(1,Math.round(x*de));(t.platno.width!==Y||t.platno.height!==re)&&(t.platno.width=Y,t.platno.height=re),c.aspect=L/Math.max(1,x),c.updateProjectionMatrix();const oe=Math.min(4096,Math.max(Zn,Y)),I=Math.min(4096,Math.max(Jn,re));(oe>Zn||I>Jn)&&(Zn=oe,Jn=I,r.setSize(Zn,Jn,!1));const Ie=new ce(qr.token("--bg-card"));r.setViewport(0,0,Y,re),r.setScissor(0,0,Y,re),r.setScissorTest(!0),r.setClearColor(Ie,1),r.clear(!0,!0,!0),r.render(o,c);const Pe=Math.max(0,Mi.height-re);a.drawImage(Mi,0,Pe,Y,re,0,0,Y,re),v?.posleRendera?.()}function U(){_||p||M!==null||w!==null||(w=requestAnimationFrame(()=>{w=null,R()}))}function C(){const ee=typeof document<"u"&&document.hidden;return!_&&!p&&b&&!S&&u&&!ee}function D(ee){if(M=null,!C())return;const _e=T>0?Math.min(.05,(ee-T)/1e3):.016;T=ee,A+=_e,v?.azuriraj?.(_e,A),R(),C()&&(M=requestAnimationFrame(D))}function k(){t.azurirajDugmePauze(S,b),C()?M===null&&(T=performance.now(),M=requestAnimationFrame(D)):M!==null&&(cancelAnimationFrame(M),M=null)}function N(ee){const _e=ee.clone().project(c),de=_e.z>=-1&&_e.z<=1;return{x:(_e.x*.5+.5)*L,y:(-_e.y*.5+.5)*x,vidljivo:de}}const O={scena3D:o,kamera:c,platno:t.platno,slojEtiketa:t.slojEtiketa,gornjeKontrole:t.gornjeKontrole,podnozje:t.podnozje,api:i,tema:qr,smanjenPokret:s,zatraziRender:U,postaviImaAnimaciju:ee=>{b=ee,ee||(S=!0),k()},prikaziRezervu:ee=>{p=!0,k(),t.prikaziRezervu(ee)},projektujU2D:N},z=new wm({bina:t.bina,platno:t.platno,dugmeDodira:t.dugmeDodira,pocetno:m,naPromenu:ee=>{g(ee),U()},naReset:()=>{z.resetuj(),v?.resetuj?.(),R()},naPrekidacPauze:()=>{b&&(S=!S,k())}});v=n.kreiraj(O,e);const H=()=>{z.resetuj(),v?.resetuj?.(),R()},q=()=>{b&&(S=!S,k())},J=()=>{S=!0,k(),v?.korak?v.korak():(A+=.45,v?.azuriraj?.(.45,A)),R()},fe=()=>z.zumiraj(.86),Ae=()=>z.zumiraj(1.16);t.dugmeReset.addEventListener("click",H),t.dugmePauza.addEventListener("click",q),t.dugmeKorak.addEventListener("click",J),t.dugmeZumPlus.addEventListener("click",fe),t.dugmeZumMinus.addEventListener("click",Ae);let K=null;typeof ResizeObserver<"u"&&(K=new ResizeObserver(ee=>{for(const _e of ee){const de=Math.round(_e.contentRect.width),Y=Math.round(_e.contentRect.height);de>0&&Y>0&&(de!==L||Y!==x)&&(L=de,x=Y,R())}}),K.observe(t.bina));let ne=null;typeof IntersectionObserver<"u"&&(ne=new IntersectionObserver(ee=>{for(const _e of ee)u=_e.isIntersecting,k()},{threshold:.05}),ne.observe(t.bina));const ue=()=>{k(),document.hidden||U()};document.addEventListener("visibilitychange",ue);const ae=qr.pretplati(ee=>{v?.osveziTemu?.(ee),R()});return R(),k(),()=>{_||(_=!0,M!==null&&(cancelAnimationFrame(M),M=null),w!==null&&(cancelAnimationFrame(w),w=null),K?.disconnect(),ne?.disconnect(),document.removeEventListener("visibilitychange",ue),ae(),t.dugmeReset.removeEventListener("click",H),t.dugmePauza.removeEventListener("click",q),t.dugmeKorak.removeEventListener("click",J),t.dugmeZumPlus.removeEventListener("click",fe),t.dugmeZumMinus.removeEventListener("click",Ae),z.raspolazi(),v?.raspolazi?.(),It(o),o.clear(),t.slojEtiketa.replaceChildren(),t.gornjeKontrole.replaceChildren(),t.podnozje.replaceChildren())}}const oc={karlsbadski:{zakon:"karlsbadski",naziv:"Карлсбадски близанац",mineral:"ортоклас",sistem:"моноклинични",tipElementa:"osa",opisElementa:"Оса близањења [001] (c-оса), раван срастања (010)",normalaRavniIliOsa:[0,0,1],ugaoRotacijeStepeni:180,izvor:"Klein & Dutrow 2007, str. 235"},spinelov:{zakon:"spinelov",naziv:"Спинелов закон",mineral:"спинел (октаедар)",sistem:"кубни",tipElementa:"ravan",opisElementa:"Раван близањења (111)",normalaRavniIliOsa:[1/Math.sqrt(3),1/Math.sqrt(3),1/Math.sqrt(3)],izvor:"Klein & Dutrow 2007, str. 233"},baveno:{zakon:"baveno",naziv:"Бавено близанац",mineral:"ортоклас",sistem:"моноклинични",tipElementa:"ravan",opisElementa:"Раван близањења (021)",normalaRavniIliOsa:[0,.894,.447],izvor:"Klein & Dutrow 2007, str. 235"},manebah:{zakon:"manebah",naziv:"Манебах близанац",mineral:"ортоклас",sistem:"моноклинични",tipElementa:"ravan",opisElementa:"Раван близањења (001)",normalaRavniIliOsa:[0,0,1],izvor:"Klein & Dutrow 2007, str. 235"},"albitski-polisintetski":{zakon:"albitski-polisintetski",naziv:"Албитски полисинтетски закон",mineral:"албит / плагиоклас",sistem:"триклинични",tipElementa:"ravan",opisElementa:"Раван близањења (010), вишеструке паралелне ламеле",normalaRavniIliOsa:[0,1,0],izvor:"Nesse 2012, str. 280"},japanski:{zakon:"japanski",naziv:"Јапански закон",mineral:"кварц",sistem:"тригонални",tipElementa:"ravan",opisElementa:"Раван близањења (11-22), угао међу c-осама 84°33′",normalaRavniIliOsa:[.707,0,.707],izvor:"Frondel 1962, Dana System of Mineralogy Vol. III",napomena:"Угао 84°33′ је теоријски угао контакта две јединке кварца по (11-22)."},dofinejski:{zakon:"dofinejski",naziv:"Дофинејски закон",mineral:"кварц",sistem:"тригонални",tipElementa:"osa",opisElementa:"Оса близањења [0001] (c-оса), ротација за 180°",normalaRavniIliOsa:[0,0,1],ugaoRotacijeStepeni:180,izvor:"Klein & Dutrow 2007, str. 236"},brazilski:{zakon:"brazilski",naziv:"Бразилски закон",mineral:"кварц",sistem:"тригонални",tipElementa:"ravan",opisElementa:"Раван близањења (11-20), прорастање левог и десног кварца",normalaRavniIliOsa:[1,0,0],izvor:"Klein & Dutrow 2007, str. 236"},"lastin-rep":{zakon:"lastin-rep",naziv:"Ластин реп (близанац гипса)",mineral:"гипс",sistem:"моноклинични",tipElementa:"ravan",opisElementa:"Раван близањења (100)",normalaRavniIliOsa:[1,0,0],izvor:"Klein & Dutrow 2007, str. 235"},"staurolit-90":{zakon:"staurolit-90",naziv:"Крстасти близанац стауролита (90°)",mineral:"стауролит",sistem:"моноклинични / псеудоорторомбични",tipElementa:"ravan",opisElementa:"Раван близањења (031), две јединке под ~90°",normalaRavniIliOsa:[0,.707,.707],izvor:"Klein & Dutrow 2007, str. 234"},"staurolit-60":{zakon:"staurolit-60",naziv:"Коси крстасти близанац стауролита (60°)",mineral:"стауролит",sistem:"моноклинични / псеудоорторомбични",tipElementa:"ravan",opisElementa:"Раван близањења (231), две јединке под ~60°",normalaRavniIliOsa:[.5,.866,0],izvor:"Klein & Dutrow 2007, str. 234"},"kolenasti-rutil":{zakon:"kolenasti-rutil",naziv:"Коленасти близанац рутила",mineral:"рутил",sistem:"тетрагонални",tipElementa:"ravan",opisElementa:"Раван близањења (011), прегиб под 114°30′",normalaRavniIliOsa:[0,.707,.707],izvor:"Klein & Dutrow 2007, str. 234"},"trilinga-aragonit":{zakon:"trilinga-aragonit",naziv:"Циклички трилинг арагонита",mineral:"арагонит",sistem:"орторомбични",tipElementa:"ravan",opisElementa:"Раван близањења (110), псеудохексагонални склоп",normalaRavniIliOsa:[.707,.707,0],izvor:"Klein & Dutrow 2007, str. 235"},"gvozdeni-krst-pirit":{zakon:"gvozdeni-krst-pirit",naziv:"Гвоздени крст (близанац пирита)",mineral:"пирит",sistem:"кубни (m-3)",tipElementa:"osa",opisElementa:"Оса близањења [001] са прорастањем два пиритоедра",normalaRavniIliOsa:[0,0,1],ugaoRotacijeStepeni:90,izvor:"Klein & Dutrow 2007, str. 234"}};function Pm(n){const e=[];if(n.includes("спинел")||n.includes("октаедар"))for(const r of[1,-1])for(const a of[1,-1])for(const s of[1,-1]){const o=1/Math.sqrt(3);e.push({normala:[r*o,a*o,s*o],d:1})}else if(n.includes("ортоклас"))e.push({normala:[.707,.707,0],d:.9},{normala:[-.707,.707,0],d:.9},{normala:[.707,-.707,0],d:.9},{normala:[-.707,-.707,0],d:.9},{normala:[0,1,0],d:1},{normala:[0,-1,0],d:1},{normala:[0,0,1],d:1.5},{normala:[0,0,-1],d:1.5},{normala:[.5,0,.866],d:1.1},{normala:[-.5,0,-.866],d:1.1});else if(n.includes("кварц")){const r=Math.sqrt(3),a=[[1,0,0],[-1,0,0],[.5,r/2,0],[-.5,r/2,0],[.5,-r/2,0],[-.5,-r/2,0]];for(const s of a)e.push({normala:s,d:.85});e.push({normala:[.707,0,.707],d:1.3},{normala:[-.353,.612,.707],d:1.3},{normala:[-.353,-.612,.707],d:1.3},{normala:[0,0,-1],d:1.4})}else if(n.includes("пирит")){const r=[[0,1,2],[1,2,0],[2,0,1]],a=[[1,1],[1,-1],[-1,1],[-1,-1]],s=Math.sqrt(5);for(const o of r)for(const c of a){const l=[0,0,0];l[o[0]]=2*c[0]/s,l[o[1]]=1*c[1]/s,l[o[2]]=0,e.push({normala:[l[0],l[1],l[2]],d:1})}}else e.push({normala:[1,0,0],d:.75},{normala:[-1,0,0],d:.75},{normala:[0,1,0],d:.85},{normala:[0,-1,0],d:.85},{normala:[0,0,1],d:1.6},{normala:[0,0,-1],d:1.6},{normala:[.707,0,.707],d:1.25},{normala:[-.707,0,.707],d:1.25},{normala:[.707,0,-.707],d:1.25},{normala:[-.707,0,-.707],d:1.25});const t=Ki(e);return qi(t).geometrijaMreze}const Dm={imaPodrazumevanuAnimaciju(n){return(n.animacija??"razdvoji-spoji")!=="nema"},pocetnaKamera(){return{theta:.65,phi:1.15,udaljenost:5.8}},kreiraj(n,e){const t=new it;n.scena3D.add(t);const i=oc[e.zakon]??oc.karlsbadski,r=Pm(i.mineral),a=new ot({color:new ce(n.tema.token("--primary")),roughness:.35,metalness:.1,flatShading:!0}),s=new ot({color:new ce(n.tema.token("--accent")),roughness:.35,metalness:.1,flatShading:!0}),o=new We(r,a),c=new We(r.clone(),s),l=new F(...i.normalaRavniIliOsa).normalize(),d=new it;if(d.add(c),i.tipElementa==="osa"){const S=(i.ugaoRotacijeStepeni??180)*Math.PI/180;c.rotateOnAxis(l,S)}else{const S=new Li().setFromUnitVectors(new F(0,1,0),l),M=S.clone().invert();c.applyQuaternion(M),c.scale.set(1,-1,1),c.applyQuaternion(S)}t.add(o),t.add(d);const h=new Ui({color:new ce(n.tema.token("--warning")),transparent:!0,opacity:.35,side:St}),f=new ht({color:new ce(n.tema.token("--warning")),linewidth:2});let m=null,g=null;if(e.prikazi_element!==!1)if(i.tipElementa==="ravan"){const S=new zi(3.5,3.5);m=new We(S,h),m.quaternion.setFromUnitVectors(new F(0,0,1),l),t.add(m)}else{const S=new Ze,M=l.clone().multiplyScalar(-2.8),w=l.clone().multiplyScalar(2.8);S.setAttribute("position",new He([M.x,M.y,M.z,w.x,w.y,w.z],3)),g=new Wi(S,f),t.add(g)}const _=document.createElement("div");_.className="udzbenik-scena-status",_.textContent=`${i.naziv} (${i.mineral}) • ${i.opisElementa}`,n.podnozje.append(_);const p=e.animacija??"razdvoji-spoji";let u=0;function b(){a.color.set(n.tema.token("--primary")),s.color.set(n.tema.token("--accent")),h.color.set(n.tema.token("--warning")),f.color.set(n.tema.token("--warning"))}return{azuriraj(S){if(u+=S,p==="razdvoji-spoji"){const M=(Math.sin(u*1.5)*.5+.5)*1.1;d.position.copy(l.clone().multiplyScalar(M)),t.rotation.y=u*.25}else p==="rotacija"&&(t.rotation.y=u*.45)},korak(){u+=.4;const S=(Math.sin(u*1.5)*.5+.5)*1.1;d.position.copy(l.clone().multiplyScalar(S)),t.rotation.y+=.2},resetuj(){u=0,d.position.set(0,0,0),t.rotation.set(0,0,0)},osveziTemu(){b()},raspolazi(){r.dispose(),c.geometry.dispose(),a.dispose(),s.dispose(),h.dispose(),f.dispose(),m&&m.geometry.dispose(),g&&g.geometry.dispose(),It(t),_.remove()}}}},cc="Cordero et al., Dalton Trans., 2008, 2832–2838 (DOI: 10.1039/B801115J)",ys={izvor:"Shannon 1976",vrednosti:{Na:{jon:"Na⁺",poluprecnik:1.02},K:{jon:"K⁺",poluprecnik:1.38},Ca:{jon:"Ca²⁺",poluprecnik:1},Mg:{jon:"Mg²⁺",poluprecnik:.72},Fe:{jon:"Fe²⁺",poluprecnik:.78},Al:{jon:"Al³⁺",poluprecnik:.54},Si:{jon:"Si⁴⁺",poluprecnik:.4},Ti:{jon:"Ti⁴⁺",poluprecnik:.61},Mn:{jon:"Mn²⁺",poluprecnik:.83},Cu:{jon:"Cu²⁺",poluprecnik:.73},Zn:{jon:"Zn²⁺",poluprecnik:.74},Pb:{jon:"Pb²⁺",poluprecnik:1.19},Ba:{jon:"Ba²⁺",poluprecnik:1.35},Cs:{jon:"Cs⁺",poluprecnik:1.67},O:{jon:"O²⁻",poluprecnik:1.4},F:{jon:"F⁻",poluprecnik:1.33},Cl:{jon:"Cl⁻",poluprecnik:1.81},S:{jon:"S²⁻",poluprecnik:1.84}}},Ts={H:{simbol:"H",naziv:"Водоник",bojaHex:"#ffffff",kovalentniPoluprecnik:.31},Li:{simbol:"Li",naziv:"Литијум",bojaHex:"#cc80ff",kovalentniPoluprecnik:1.28},Be:{simbol:"Be",naziv:"Берилијум",bojaHex:"#c2ff00",kovalentniPoluprecnik:.96},B:{simbol:"B",naziv:"Бор",bojaHex:"#ffb5b5",kovalentniPoluprecnik:.84},C:{simbol:"C",naziv:"Угљеник",bojaHex:"#505050",kovalentniPoluprecnik:.76},N:{simbol:"N",naziv:"Азот",bojaHex:"#3050f8",kovalentniPoluprecnik:.71},O:{simbol:"O",naziv:"Кисеоник",bojaHex:"#ff0d0d",kovalentniPoluprecnik:.66},F:{simbol:"F",naziv:"Флуор",bojaHex:"#90e050",kovalentniPoluprecnik:.57},Na:{simbol:"Na",naziv:"Натријум",bojaHex:"#ab5cf2",kovalentniPoluprecnik:1.66},Mg:{simbol:"Mg",naziv:"Магнезијум",bojaHex:"#8aff00",kovalentniPoluprecnik:1.41},Al:{simbol:"Al",naziv:"Алуминијум",bojaHex:"#bfa6a6",kovalentniPoluprecnik:1.21},Si:{simbol:"Si",naziv:"Силицијум",bojaHex:"#f0c8a0",kovalentniPoluprecnik:1.11},P:{simbol:"P",naziv:"Фосфор",bojaHex:"#ff8000",kovalentniPoluprecnik:1.07},S:{simbol:"S",naziv:"Сумпор",bojaHex:"#ffff30",kovalentniPoluprecnik:1.05},Cl:{simbol:"Cl",naziv:"Хлор",bojaHex:"#1ff01f",kovalentniPoluprecnik:1.02},K:{simbol:"K",naziv:"Калијум",bojaHex:"#8f40d4",kovalentniPoluprecnik:2.03},Ca:{simbol:"Ca",naziv:"Калцијум",bojaHex:"#3dff00",kovalentniPoluprecnik:1.76},Ti:{simbol:"Ti",naziv:"Титанијум",bojaHex:"#bfc2c7",kovalentniPoluprecnik:1.6},V:{simbol:"V",naziv:"Ванадијум",bojaHex:"#a6a6ab",kovalentniPoluprecnik:1.53},Cr:{simbol:"Cr",naziv:"Хром",bojaHex:"#8a99c7",kovalentniPoluprecnik:1.39},Mn:{simbol:"Mn",naziv:"Манган",bojaHex:"#9c7ac7",kovalentniPoluprecnik:1.39},Fe:{simbol:"Fe",naziv:"Гвожђе",bojaHex:"#e06633",kovalentniPoluprecnik:1.32},Co:{simbol:"Co",naziv:"Кобалт",bojaHex:"#f090a0",kovalentniPoluprecnik:1.26},Ni:{simbol:"Ni",naziv:"Никл",bojaHex:"#50d050",kovalentniPoluprecnik:1.24},Cu:{simbol:"Cu",naziv:"Бакар",bojaHex:"#c88033",kovalentniPoluprecnik:1.32},Zn:{simbol:"Zn",naziv:"Цинк",bojaHex:"#7d80b0",kovalentniPoluprecnik:1.22},As:{simbol:"As",naziv:"Арсен",bojaHex:"#bd80e3",kovalentniPoluprecnik:1.19},Sr:{simbol:"Sr",naziv:"Стронцијум",bojaHex:"#00ff00",kovalentniPoluprecnik:1.95},Zr:{simbol:"Zr",naziv:"Цирконијум",bojaHex:"#94e0e0",kovalentniPoluprecnik:1.75},Mo:{simbol:"Mo",naziv:"Молибден",bojaHex:"#54b5b5",kovalentniPoluprecnik:1.54},Ag:{simbol:"Ag",naziv:"Сребро",bojaHex:"#c0c0c0",kovalentniPoluprecnik:1.45},Sn:{simbol:"Sn",naziv:"Калај",bojaHex:"#668080",kovalentniPoluprecnik:1.39},Sb:{simbol:"Sb",naziv:"Антимон",bojaHex:"#9e63b5",kovalentniPoluprecnik:1.39},Ba:{simbol:"Ba",naziv:"Баријум",bojaHex:"#00c900",kovalentniPoluprecnik:2.15},W:{simbol:"W",naziv:"Волфрам",bojaHex:"#2194d6",kovalentniPoluprecnik:1.62},Pt:{simbol:"Pt",naziv:"Платина",bojaHex:"#d0d0e0",kovalentniPoluprecnik:1.36},Au:{simbol:"Au",naziv:"Злато",bojaHex:"#ffd123",kovalentniPoluprecnik:1.36},Hg:{simbol:"Hg",naziv:"Жива",bojaHex:"#b8b8d0",kovalentniPoluprecnik:1.32},Pb:{simbol:"Pb",naziv:"Олово",bojaHex:"#575961",kovalentniPoluprecnik:1.46},Bi:{simbol:"Bi",naziv:"Бизмут",bojaHex:"#9e4fb5",kovalentniPoluprecnik:1.48}},Lm={simbol:"?",naziv:"Непознат елемент",bojaHex:"#ff1493",kovalentniPoluprecnik:1.2};function Hs(n){const e=n.trim().replace(/[^A-Za-z]/g,"");if(!e)return"?";const t=e[0].toUpperCase(),i=e.length>1?e[1].toLowerCase():"",r=t+i;return r in Ts?r:t in Ts?t:r}function ws(n){const e=Hs(n);return Ts[e]??{...Lm,simbol:e}}function lc(n,e="jonski"){const t=Hs(n),i=ws(t);if(e==="jonski"){const r=ys.vrednosti[t];if(r)return{poluprecnik:r.poluprecnik,koriscenaVrsta:"jonski",jon:r.jon}}return{poluprecnik:i.kovalentniPoluprecnik,koriscenaVrsta:"kovalentni"}}class Wn extends Error{constructor(e){super(e),this.name="CifGreska"}}function un(n,e){const t=n.trim().replace(/\([0-9]+\)$/,""),i=Number(t);if(!Number.isFinite(i))throw new Wn(`Неисправна нумеричка вредност у CIF пољу ${e}: "${n}"`);return i}function Ar(n){const e=[];let t=0;const i=n.length;for(;t<i;){for(;t<i&&/\s/.test(n[t]);)t++;if(t>=i)break;const r=n[t];if(r==="#")break;if(r==="'"||r==='"'){const a=r;t++;let s=t;for(;t<i&&!(n[t]===a&&(t+1>=i||/\s/.test(n[t+1])));)t++;e.push(n.slice(s,t)),t<i&&n[t]===a&&t++}else{const a=t;for(;t<i&&!/\s/.test(n[t]);)t++;e.push(n.slice(a,t))}}return e}function Im(n){if(!n||!n.trim())throw new Wn("CIF садржај је празан.");const e=n.split(/\r?\n/);let t="struktura";const i=new Map,r=[];let a=0;for(;a<e.length;){const m=e[a].trim();if(!m||m.startsWith("#")){a++;continue}if(m.toLowerCase().startsWith("data_")){t=m.slice(5).trim()||t,a++;continue}if(m.toLowerCase()==="loop_"){a++;const g=[];for(;a<e.length;){const w=e[a].trim();if(!w||w.startsWith("#")){a++;continue}if(w.startsWith("_")){const T=Ar(w);T[0]&&g.push(T[0].toLowerCase()),a++}else break}const _=g.indexOf("_atom_site_label"),p=g.indexOf("_atom_site_type_symbol"),u=g.indexOf("_atom_site_fract_x"),b=g.indexOf("_atom_site_fract_y"),S=g.indexOf("_atom_site_fract_z"),M=_!==-1&&p!==-1&&u!==-1&&b!==-1&&S!==-1;for(;a<e.length;){const w=e[a].trim();if(!w||w.startsWith("#")){a++;continue}const T=w.toLowerCase();if(w.startsWith("_")||T==="loop_"||T.startsWith("data_")||w.startsWith(";"))break;if(M&&g.length>0){const A=Ar(w);if(A.length<g.length)throw new Wn("Непотпун ред у _atom_site табели CIF фајла.");const L=A[_],x=A[p],v=un(A[u],"_atom_site_fract_x"),R=un(A[b],"_atom_site_fract_y"),U=un(A[S],"_atom_site_fract_z");r.push({oznaka:L,simbol:Hs(x),fx:v,fy:R,fz:U})}a++}continue}if(m.startsWith("_")){const g=Ar(m);if(g.length>=2&&g[0]&&g[1]!==void 0)i.set(g[0].toLowerCase(),g[1]);else if(g.length===1&&g[0]&&a+1<e.length){const _=Ar(e[a+1].trim());_[0]&&!_[0].startsWith("_")&&_[0].toLowerCase()!=="loop_"&&(i.set(g[0].toLowerCase(),_[0]),a++)}}a++}const s=["_cell_length_a","_cell_length_b","_cell_length_c","_cell_angle_alpha","_cell_angle_beta","_cell_angle_gamma"];for(const m of s)if(!i.has(m))throw new Wn(`Недостаје обавезно CIF поље: ${m}`);const o=un(i.get("_cell_length_a"),"_cell_length_a"),c=un(i.get("_cell_length_b"),"_cell_length_b"),l=un(i.get("_cell_length_c"),"_cell_length_c"),d=un(i.get("_cell_angle_alpha"),"_cell_angle_alpha"),h=un(i.get("_cell_angle_beta"),"_cell_angle_beta"),f=un(i.get("_cell_angle_gamma"),"_cell_angle_gamma");if(o<=0||c<=0||l<=0)throw new Wn("Димензије јединичне ћелије a, b, c морају бити позитивне.");if(d<=0||d>=180||h<=0||h>=180||f<=0||f>=180||d+h+f>=360)throw new Wn("Углови јединичне ћелије α, β, γ нису физички валидни.");if(r.length===0)throw new Wn("CIF не садржи ниједан атом у loop_ _atom_site блоку.");return{nazivBloka:t,celija:{a:o,b:c,c:l,alpha:d,beta:h,gamma:f},atomi:r}}function Gs(n){const e=Math.PI/180,t=n.alpha*e,i=n.beta*e,r=n.gamma*e,a=Math.cos(t),s=Math.cos(i),o=Math.cos(r),c=Math.sin(r),l=n.a,d=0,h=n.b*o,f=n.b*c,m=0,g=n.c*s,_=n.c*(a-s*o)/c,p=Math.max(0,n.c*n.c-g*g-_*_),u=Math.sqrt(p);return{va:[l,d,-0],vb:[h,m,-f],vc:[g,u,-_]}}function Cn(n,e,t,i){return[n*i.va[0]+e*i.vb[0]+t*i.vc[0],n*i.va[1]+e*i.vb[1]+t*i.vc[1],n*i.va[2]+e*i.vb[2]+t*i.vc[2]]}const Ca=[{kljuc:"kubna-P",naziv:"Кубна примитивна (P)",sistem:"Кубни",centriranje:"P",brojCvorova:1,celija:{a:1.8,b:1.8,c:1.8,alpha:90,beta:90,gamma:90},cvoroviFrakcioni:[[0,0,0]]},{kljuc:"kubna-I",naziv:"Кубна просторно центрирана (I)",sistem:"Кубни",centriranje:"I",brojCvorova:2,celija:{a:1.8,b:1.8,c:1.8,alpha:90,beta:90,gamma:90},cvoroviFrakcioni:[[0,0,0],[.5,.5,.5]],primitivniVektori:[[-.5,.5,.5],[.5,-.5,.5],[.5,.5,-.5]]},{kljuc:"kubna-F",naziv:"Кубна површински центрирана (F)",sistem:"Кубни",centriranje:"F",brojCvorova:4,celija:{a:1.8,b:1.8,c:1.8,alpha:90,beta:90,gamma:90},cvoroviFrakcioni:[[0,0,0],[0,.5,.5],[.5,0,.5],[.5,.5,0]],primitivniVektori:[[0,.5,.5],[.5,0,.5],[.5,.5,0]]},{kljuc:"tetragonalna-P",naziv:"Тетрагонална примитивна (P)",sistem:"Тетрагонални",centriranje:"P",brojCvorova:1,celija:{a:1.6,b:1.6,c:2.3,alpha:90,beta:90,gamma:90},cvoroviFrakcioni:[[0,0,0]]},{kljuc:"tetragonalna-I",naziv:"Тетрагонална просторно центрирана (I)",sistem:"Тетрагонални",centriranje:"I",brojCvorova:2,celija:{a:1.6,b:1.6,c:2.3,alpha:90,beta:90,gamma:90},cvoroviFrakcioni:[[0,0,0],[.5,.5,.5]],primitivniVektori:[[-.5,.5,.5],[.5,-.5,.5],[.5,.5,-.5]]},{kljuc:"ortorombicna-P",naziv:"Орторомбична примитивна (P)",sistem:"Орторомбични",centriranje:"P",brojCvorova:1,celija:{a:1.4,b:1.9,c:2.4,alpha:90,beta:90,gamma:90},cvoroviFrakcioni:[[0,0,0]]},{kljuc:"ortorombicna-C",naziv:"Орторомбична базно центрирана (C)",sistem:"Орторомбични",centriranje:"C",brojCvorova:2,celija:{a:1.4,b:1.9,c:2.4,alpha:90,beta:90,gamma:90},cvoroviFrakcioni:[[0,0,0],[.5,.5,0]],primitivniVektori:[[.5,.5,0],[-.5,.5,0],[0,0,1]]},{kljuc:"ortorombicna-I",naziv:"Орторомбична просторно центрирана (I)",sistem:"Орторомбични",centriranje:"I",brojCvorova:2,celija:{a:1.4,b:1.9,c:2.4,alpha:90,beta:90,gamma:90},cvoroviFrakcioni:[[0,0,0],[.5,.5,.5]],primitivniVektori:[[-.5,.5,.5],[.5,-.5,.5],[.5,.5,-.5]]},{kljuc:"ortorombicna-F",naziv:"Орторомбична површински центрирана (F)",sistem:"Орторомбични",centriranje:"F",brojCvorova:4,celija:{a:1.4,b:1.9,c:2.4,alpha:90,beta:90,gamma:90},cvoroviFrakcioni:[[0,0,0],[0,.5,.5],[.5,0,.5],[.5,.5,0]],primitivniVektori:[[0,.5,.5],[.5,0,.5],[.5,.5,0]]},{kljuc:"heksagonalna-P",naziv:"Хексагонална примитивна (P)",sistem:"Хексагонални",centriranje:"P",brojCvorova:1,celija:{a:1.8,b:1.8,c:2.2,alpha:90,beta:90,gamma:120},cvoroviFrakcioni:[[0,0,0]]},{kljuc:"romboedarska-R",naziv:"Ромбоедарска (R, хексагонална поставка)",sistem:"Тригонални",centriranje:"R",brojCvorova:3,celija:{a:1.8,b:1.8,c:2.5,alpha:90,beta:90,gamma:120},cvoroviFrakcioni:[[0,0,0],[2/3,1/3,1/3],[1/3,2/3,2/3]],primitivniVektori:[[2/3,1/3,1/3],[-1/3,1/3,1/3],[-1/3,-2/3,1/3]]},{kljuc:"monoklinicna-P",naziv:"Моноклинична примитивна (P)",sistem:"Моноклинични",centriranje:"P",brojCvorova:1,celija:{a:1.5,b:1.8,c:2.1,alpha:90,beta:110,gamma:90},cvoroviFrakcioni:[[0,0,0]]},{kljuc:"monoklinicna-C",naziv:"Моноклинична базно центрирана (C)",sistem:"Моноклинични",centriranje:"C",brojCvorova:2,celija:{a:1.5,b:1.8,c:2.1,alpha:90,beta:110,gamma:90},cvoroviFrakcioni:[[0,0,0],[.5,.5,0]],primitivniVektori:[[.5,.5,0],[-.5,.5,0],[0,0,1]]},{kljuc:"triklinicna-P",naziv:"Триклинична примитивна (P)",sistem:"Триклинични",centriranje:"P",brojCvorova:1,celija:{a:1.4,b:1.7,c:2.1,alpha:78,beta:108,gamma:102},cvoroviFrakcioni:[[0,0,0]]}],Um={imaPodrazumevanuAnimaciju(){return!0},pocetnaKamera(){return{theta:.65,phi:1.15,udaljenost:6.8}},kreiraj(n,e){let t=e.resetka==="sve"?"kubna-P":e.resetka;const i=new it;n.scena3D.add(i);const r=new xn(.08,16,16),a=new ot({color:new ce(n.tema.token("--primary")),roughness:.25,metalness:.2}),s=new ot({color:new ce(n.tema.token("--accent")),roughness:.25,metalness:.2}),o=new ht({color:new ce(n.tema.token("--text-secondary")),linewidth:2}),c=new Uu({color:new ce(n.tema.token("--border-color")),dashSize:.15,gapSize:.1}),l=new ht({color:new ce(n.tema.token("--warning")),linewidth:2});function d(p){for(;i.children.length>0;){const U=i.children[0];i.remove(U),It(U)}const u=Gs(p.celija),b=new F(...u.va),S=new F(...u.vb),M=new F(...u.vc),T=b.clone().add(S).add(M).multiplyScalar(.5).clone().negate(),A=[[0,0,0],[1,0,0],[1,1,0],[0,1,0],[0,0,1],[1,0,1],[1,1,1],[0,1,1]].map(([U,C,D])=>{const[k,N,O]=Cn(U,C,D,u);return new F(k,N,O).add(T)}),L=[[0,1],[1,2],[2,3],[3,0],[4,5],[5,6],[6,7],[7,4],[0,4],[1,5],[2,6],[3,7]],x=[];for(const U of L){const C=A[U[0]],D=A[U[1]];x.push(C.x,C.y,C.z,D.x,D.y,D.z)}const v=new Ze;v.setAttribute("position",new He(x,3)),i.add(new gt(v,o));const R=new Set;for(const[U,C,D]of p.cvoroviFrakcioni)for(let k=0;k<=1;k++)for(let N=0;N<=1;N++)for(let O=0;O<=1;O++){const z=U+k,H=C+N,q=D+O;if(z>=-1e-4&&z<=1.0001&&H>=-1e-4&&H<=1.0001&&q>=-1e-4&&q<=1.0001){const J=`${z.toFixed(2)},${H.toFixed(2)},${q.toFixed(2)}`;if(R.has(J))continue;R.add(J);const[fe,Ae,K]=Cn(z,H,q,u),ne=new F(fe,Ae,K).add(T),ue=(k===0||k===1)&&(N===0||N===1)&&(O===0||O===1)&&U===0&&C===0&&D===0,ae=new We(r,ue?a:s);ae.position.copy(ne),i.add(ae)}}if(e.prikazi_susedne_celije){const U=[];for(const k of[-1,0,1])for(const N of[-1,0,1])for(const O of[-1,0,1]){if(k===0&&N===0&&O===0)continue;const z=b.clone().multiplyScalar(k).add(S.clone().multiplyScalar(N)).add(M.clone().multiplyScalar(O));for(const H of L){const q=A[H[0]].clone().add(z),J=A[H[1]].clone().add(z);U.push(q.x,q.y,q.z,J.x,J.y,J.z)}}const C=new Ze;C.setAttribute("position",new He(U,3));const D=new gt(C,c);D.computeLineDistances(),i.add(D)}if(e.prikazi_primitivnu_celiju&&p.primitivniVektori){const U=[],C=A[0],D=p.primitivniVektori.map(([q,J,fe])=>{const[Ae,K,ne]=Cn(q,J,fe,u);return new F(Ae,K,ne)}),k=D[0],N=D[1],O=D[2],z=[C,C.clone().add(k),C.clone().add(k).add(N),C.clone().add(N),C.clone().add(O),C.clone().add(k).add(O),C.clone().add(k).add(N).add(O),C.clone().add(N).add(O)];for(const q of L){const J=z[q[0]],fe=z[q[1]];U.push(J.x,J.y,J.z,fe.x,fe.y,fe.z)}const H=new Ze;H.setAttribute("position",new He(U,3)),i.add(new gt(H,l))}}const h=document.createElement("div");h.className="udzbenik-scena-status",n.podnozje.append(h);function f(p){h.textContent=`${p.naziv} • Систем: ${p.sistem} • Чворова по конвенционалној ћелији: ${p.brojCvorova}`}if(e.resetka==="sve"){const p=document.createElement("div");p.className="udzbenik-bravais-traka",p.style.display="flex",p.style.flexWrap="wrap",p.style.gap="4px";for(const u of Ca){const b=document.createElement("button");b.type="button",b.className="udzbenik-dugme udzbenik-dugme--malo",u.kljuc===t&&b.classList.add("udzbenik-dugme--aktivno"),b.textContent=u.kljuc,b.setAttribute("aria-label",u.naziv),b.addEventListener("click",()=>{t=u.kljuc,p.querySelectorAll("button").forEach(S=>S.classList.remove("udzbenik-dugme--aktivno")),b.classList.add("udzbenik-dugme--aktivno"),d(u),f(u)}),p.append(b)}n.gornjeKontrole.append(p)}const m=Ca.find(p=>p.kljuc===t)??Ca[0];d(m),f(m);function g(){a.color.set(n.tema.token("--primary")),s.color.set(n.tema.token("--accent")),o.color.set(n.tema.token("--text-secondary")),c.color.set(n.tema.token("--border-color")),l.color.set(n.tema.token("--warning"))}let _=0;return{azuriraj(p){_+=p*.45,i.rotation.y=_},korak(){_+=.25,i.rotation.y=_},resetuj(){_=0,i.rotation.set(0,0,0)},osveziTemu(){g()},raspolazi(){r.dispose(),a.dispose(),s.dispose(),o.dispose(),c.dispose(),l.dispose(),It(i),h.remove()}}}},zm=[[0,1,2],[0,2,1],[1,0,2],[1,2,0],[2,0,1],[2,1,0]],Nm=[[1,1,1],[1,1,-1],[1,-1,1],[1,-1,-1],[-1,1,1],[-1,1,-1],[-1,-1,1],[-1,-1,-1]];function Ot(n){return n<0?`${Math.abs(n)}̄`:String(n)}function km(n){const e=Math.abs(n[0])>=10||Math.abs(n[1])>=10||Math.abs(n[2])>=10;return`(${[Ot(n[0]),Ot(n[1]),Ot(n[2])].join(e?" ":"")})`}function Fm(n){const e=Math.abs(n[0])>=10||Math.abs(n[1])>=10||Math.abs(n[2])>=10;return`{${[Ot(n[0]),Ot(n[1]),Ot(n[2])].join(e?" ":"")}}`}function uc(n){const[e,t,i]=n;if(!Number.isFinite(e)||!Number.isFinite(t)||!Number.isFinite(i))throw new Error("Милерови индекси морају бити коначни бројеви.");if(e===0&&t===0&&i===0)throw new Error("Милерови индекси не могу бити (000).");const r=new Set,a=[],s=[Math.trunc(e),Math.trunc(t),Math.trunc(i)];for(const[o,c,l]of zm){const d=s[o],h=s[c],f=s[l];for(const[m,g,_]of Nm){const p=d===0?0:d*m,u=h===0?0:h*g,b=f===0?0:f*_,S=`${p},${u},${b}`;if(r.has(S))continue;r.add(S);const M=Math.hypot(p,u,b),w=[p,u,b];a.push({hkl:w,normala:[p/M,u/M,b/M],oznaka:km(w)})}}return a}function Om(n,e){const t=e??56,i=Math.round((180-t)*10)/10;switch(n){case"kubna":return{naziv:"Кубна цепљивост {100}",brojPravaca:"3 правца",uglovi:"90°",podrazumevaniPrimer:"халит, галенит"};case"oktaedarska":return{naziv:"Октаедарска цепљивост {111}",brojPravaca:"4 правца",uglovi:"70,5° и 109,5°",podrazumevaniPrimer:"флуорит, дијамант"};case"dodekaedarska":return{naziv:"Додекаедарска цепљивост {110}",brojPravaca:"6 праваца",uglovi:"60°, 90° и 120°",podrazumevaniPrimer:"сфалерит"};case"romboedarska":return{naziv:"Ромбоедарска цепљивост {101̄1}",brojPravaca:"3 правца",uglovi:"~75° и ~105° (≠ 90°)",podrazumevaniPrimer:"калцит, доломит"};case"bazalna":return{naziv:"Базална (пинакоидална) цепљивост {001}",brojPravaca:"1 правац",uglovi:"паралелне ламеле (0°)",podrazumevaniPrimer:"лискун (мусковит), графит"};case"prizmatska":return{naziv:"Призматска цепљивост {110}",brojPravaca:"2 правца",uglovi:`${t}° и ${i}°`,podrazumevaniPrimer:t>75?"пироксен":"амфибол"};case"nema":return{naziv:"Нема цепљивости (шкољкаст прелом)",brojPravaca:"0 праваца",uglovi:"нема равни цепљивости",podrazumevaniPrimer:"кварц"}}}function Xn(n,e,t,i){const r=Ki(n);if(r.pljosni.length<4||r.temena.length<4)return null;const a=qi(r),s=new it;return s.add(new We(a.geometrijaMreze,t),new gt(a.geometrijaIvica,i)),{grupa:s,smerRazdvajanja:e}}function dn(n,e,t,i,r){const a=new zi(t,t),s=new We(a,i),o=new gt(new jr(a),r),c=new it;c.add(s,o);const l=new F(...n).normalize();return c.quaternion.setFromUnitVectors(new F(0,0,1),l),c.position.copy(l).multiplyScalar(e),c}function _i(n,e){const t=Math.hypot(n-.35,e-.25),i=.055*Math.sin(t*13.5);return .28*(n*n-.5*e*e)+.18*n+i}function Bm(n,e,t,i){if(!n){const h=[{normala:[0,-1,0],d:1.15}];for(let m=0;m<6;m++){const g=m*Math.PI/3,_=Math.cos(g),p=Math.sin(g);h.push({normala:[_,0,p],d:.95}),h.push({normala:[_*.72,.69,p*.72],d:1.28}),h.push({normala:[_*.72,-.69,p*.72],d:1.28})}const f=Xn(h,new F(0,0,0),e,i);return{fragmenti:f?[f]:[]}}const o=12,c=24;function l(h,f){const m=(f%(Math.PI/3)+Math.PI/3)%(Math.PI/3)-Math.PI/6,g=.95*Math.cos(Math.PI/6)/Math.cos(m);return[h*g*Math.cos(f),h*g*Math.sin(f)]}function d(h){const f=[],m=[],g=[],_=h?1.15:-1.15,p=h?1.85:-1.85;for(let w=0;w<o;w++){const T=w/o,A=(w+1)/o;for(let L=0;L<c;L++){const x=L/c*Math.PI*2,v=(L+1)/c*Math.PI*2,[R,U]=l(T,x),[C,D]=l(A,x),[k,N]=l(A,v),[O,z]=l(T,v),H=_i(R,U),q=_i(C,D),J=_i(k,N),fe=_i(O,z);h?m.push(R,H,U,k,J,N,C,q,D,R,H,U,O,fe,z,k,J,N):m.push(R,H,U,C,q,D,k,J,N,R,H,U,k,J,N,O,fe,z)}}for(let w=0;w<c;w++){const T=w/c*Math.PI*2,A=(w+1)/c*Math.PI*2,[L,x]=l(1,T),[v,R]=l(1,A),U=_i(L,x),C=_i(v,R);h?(f.push(L,U,x,v,C,R,v,_,R,L,U,x,v,_,R,L,_,x),f.push(L,_,x,v,_,R,0,p,0)):(f.push(L,_,x,v,_,R,v,C,R,L,_,x,v,C,R,L,U,x),f.push(v,_,R,L,_,x,0,p,0)),g.push(L,U,x,v,C,R),g.push(L,_,x,v,_,R),w%(c/6)===0&&(g.push(L,U,x,L,_,x),g.push(L,_,x,0,p,0))}const u=new Ze;u.setAttribute("position",new He(f,3)),u.computeVertexNormals();const b=new Ze;b.setAttribute("position",new He(m,3)),b.computeVertexNormals();const S=new Ze;S.setAttribute("position",new He(g,3));const M=new it;return M.add(new We(u,e),new We(b,t),new gt(S,i)),M}return{fragmenti:[{grupa:d(!0),smerRazdvajanja:new F(.18,.55,.1)},{grupa:d(!1),smerRazdvajanja:new F(-.18,-.55,-.1)}]}}const jm={imaPodrazumevanuAnimaciju(n){return!(n.vrsta==="nema"&&!n.prikazi_prelom)},pocetnaKamera(){return{theta:.68,phi:1.14,udaljenost:5.9}},kreiraj(n,e){const t=e.vrsta,i=e.ugao??56,r=e.prikazi_prelom??!1,a=new it,s=new it,o=new it;a.add(s,o),n.scena3D.add(a);const c=new ot({color:new ce(n.tema.token("--primary")),transparent:!0,opacity:.86,roughness:.32,metalness:.08,flatShading:!0}),l=new ot({color:new ce(n.tema.token("--accent")),roughness:.22,metalness:.15,side:St}),d=new ht({color:new ce(n.tema.token("--text-primary"))}),h=new Ui({color:new ce(n.tema.token("--accent")),transparent:!0,opacity:.26,side:St,depthWrite:!1}),f=new ht({color:new ce(n.tema.token("--accent"))}),m=[];function g(){if(t==="kubna"){const w=[-1,1];for(const T of w)for(const A of w)for(const L of w){const x=[{normala:[T,0,0],d:1.05},{normala:[-T,0,0],d:0},{normala:[0,A,0],d:1.05},{normala:[0,-A,0],d:0},{normala:[0,0,L],d:1.05},{normala:[0,0,-L],d:0}],v=Xn(x,new F(T,A,L).normalize().multiplyScalar(.52),c,d);v&&m.push(v)}o.add(dn([1,0,0],0,2.6,h,f),dn([0,1,0],0,2.6,h,f),dn([0,0,1],0,2.6,h,f))}else if(t==="oktaedarska"){const w=uc([1,1,1]).map(A=>({normala:A.normala,d:1.08})),T=[[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]];for(let A=0;A<16;A++){const L=[...w],x=new F;for(let R=0;R<4;R++){const U=(A&1<<R)!==0?1:-1,C=T[R];L.push({normala:[C[0]*U,C[1]*U,C[2]*U],d:0}),x.add(new F(C[0]*U,C[1]*U,C[2]*U))}const v=Xn(L,x.lengthSq()>1e-4?x.normalize().multiplyScalar(.52):x,c,d);v&&m.push(v)}for(const A of T)o.add(dn(A,0,2.8,h,f))}else if(t==="dodekaedarska"){const w=uc([1,1,0]).map(L=>({normala:L.normala,d:1.12})),T=[[1,1,0],[1,-1,0],[1,0,1],[1,0,-1],[0,1,1],[0,1,-1]];for(const L of T)o.add(dn(L,0,2.7,h,f));const A=[[1,1,0],[1,-1,0],[0,1,1]];for(let L=0;L<8;L++){const x=[...w],v=new F;for(let U=0;U<3;U++){const C=(L&1<<U)!==0?1:-1,D=A[U];x.push({normala:[D[0]*C,D[1]*C,D[2]*C],d:0}),v.add(new F(D[0]*C,D[1]*C,D[2]*C))}const R=Xn(x,v.normalize().multiplyScalar(.5),c,d);R&&m.push(R)}}else if(t==="romboedarska"){const w=[1,.26,.14],T=[.24,1,.22],A=[.18,.26,1],L=[w,T,A],x=[];for(const R of L)x.push({normala:R,d:1}),x.push({normala:[-R[0],-R[1],-R[2]],d:1}),o.add(dn(R,0,2.8,h,f));const v=[-1,1];for(const R of v)for(const U of v)for(const C of v){const D=[...x,{normala:[-w[0]*R,-w[1]*R,-w[2]*R],d:0},{normala:[-T[0]*U,-T[1]*U,-T[2]*U],d:0},{normala:[-A[0]*C,-A[1]*C,-A[2]*C],d:0}],k=new F(w[0]*R+T[0]*U+A[0]*C,w[1]*R+T[1]*U+A[1]*C,w[2]*R+T[2]*U+A[2]*C).normalize().multiplyScalar(.5),N=Xn(D,k,c,d);N&&m.push(N)}}else if(t==="bazalna"){const w=[];for(let x=0;x<6;x++){const v=x*Math.PI/3;w.push({normala:[Math.cos(v),0,Math.sin(v)],d:1.15})}const T=5,A=1.1,L=A/T;for(let x=0;x<T;x++){const v=-A/2+x*L,R=v+L,U=[...w,{normala:[0,1,0],d:R},{normala:[0,-1,0],d:-v}],C=x-(T-1)/2,D=Xn(U,new F(C*.08,C*.28,0),c,d);D&&m.push(D),x>0&&o.add(dn([0,1,0],v,2.7,h,f))}}else if(t==="prizmatska"){const w=i*Math.PI/180*.5,T=[Math.sin(w),0,Math.cos(w)],A=[-Math.sin(w),0,Math.cos(w)],L=[{normala:[0,1,0],d:1.3},{normala:[0,-1,0],d:1.3},{normala:T,d:.9},{normala:[-T[0],0,-T[2]],d:.9},{normala:A,d:.9},{normala:[-A[0],0,-A[2]],d:.9}];o.add(dn(T,0,2.9,h,f),dn(A,0,2.9,h,f));const x=[-1,1];for(const v of x)for(const R of x){const U=[...L,{normala:[-T[0]*v,0,-T[2]*v],d:0},{normala:[-A[0]*R,0,-A[2]*R],d:0}],C=new F(T[0]*v+A[0]*R,0,T[2]*v+A[2]*R).normalize().multiplyScalar(.48),D=Xn(U,C,c,d);D&&m.push(D)}}else{const w=Bm(r,c,l,d);m.push(...w.fragmenti)}for(const w of m)s.add(w.grupa)}g();const _=Om(t,i),p=e.primer||_.podrazumevaniPrimer,u=document.createElement("div");u.className="udzbenik-scena-info-red udzbenik-cepljivost-meta";const b=[[Ge("brojPravacaCepljivosti"),_.brojPravaca],[Ge("ugloviCepljivosti"),_.uglovi],[Ge("primerMinerala"),p]];for(const[w,T]of b){const A=document.createElement("span");A.className="udzbenik-meta-stavka";const L=document.createElement("strong");L.textContent=`${w}: `;const x=document.createElement("span");x.textContent=T,A.append(L,x),u.append(A)}n.podnozje.append(u);let S=n.smanjenPokret?.72:0;function M(){if(t==="nema"&&!r){o.visible=!1;return}let w=0,T=0;if(S<.3)w=S/.3,T=0;else if(S<.72){w=1;const A=(S-.3)/.42;T=A*A*(3-2*A)}else if(S<.85)w=1,T=1;else{const A=(S-.85)/.15;w=1-A,T=1-A*A*(3-2*A)}o.visible=t!=="nema"&&w>.02,o.scale.setScalar(.25+.75*w),h.opacity=.26*w*(1-.45*T);for(const A of m)A.grupa.position.copy(A.smerRazdvajanja).multiplyScalar(T)}return M(),{azuriraj(w){S=(S+w*.17)%1,a.rotation.y+=w*.24,M()},korak(){S=(S+.18)%1,M()},resetuj(){a.rotation.set(0,0,0),S=n.smanjenPokret?.72:0,M()},osveziTemu(w){c.color.set(w.token("--primary")),l.color.set(w.token("--accent")),d.color.set(w.token("--text-primary")),h.color.set(w.token("--accent")),f.color.set(w.token("--accent"))},raspolazi(){It(a),c.dispose(),l.dispose(),d.dispose(),h.dispose(),f.dispose()}}}};function Vm(n){if(n.length===4){const[e,t,i,r]=n;if(i!==-(e+t))throw new Error(`Неисправни Браве-Милерови индекси (${e} ${t} ${i} ${r}): мора важити i = -(h+k), добијено i=${i}, -(h+k)=${-(e+t)}.`);return[e,t,r]}return n}function Hm(n,e=!1){if(e){const[r,a,s]=n,o=-(r+a),c=Math.abs(r)>=10||Math.abs(a)>=10||Math.abs(o)>=10||Math.abs(s)>=10;return`(${[Ot(r),Ot(a),Ot(o),Ot(s)].join(c?" ":"")})`}const t=Math.abs(n[0])>=10||Math.abs(n[1])>=10||Math.abs(n[2])>=10;return`(${[Ot(n[0]),Ot(n[1]),Ot(n[2])].join(t?" ":"")})`}function Gm(n,e,t){const i=t?.a??1,r=t?.b??i,a=t?.c??i;let s=0,o=0,c=0;e==="heksagonalni"||e==="trigonalni"?(s=n[0]/i,o=(n[0]+2*n[1])/(i*Math.sqrt(3)),c=n[2]/a):(s=n[0]/i,o=n[1]/r,c=n[2]/a);const l=Math.hypot(s,o,c);if(l<1e-12)throw new Error("Милерови индекси не могу дати нулти вектор нормале.");return[s/l,o/l,c/l]}const Wm=[[0,1,2],[0,2,1],[1,0,2],[1,2,0],[2,0,1],[2,1,0]],qc=[[1,1,1],[1,1,-1],[1,-1,1],[1,-1,-1],[-1,1,1],[-1,1,-1],[-1,-1,1],[-1,-1,-1]];function dc(n){const e=new Set,t=[];for(const[i,r,a]of Wm)for(const[s,o,c]of qc){const l=[n[i]===0?0:n[i]*s,n[r]===0?0:n[r]*o,n[a]===0?0:n[a]*c],d=l.join(",");e.has(d)||(e.add(d),t.push(l))}return t}const Ws=[[0,1,2],[1,2,0],[2,0,1]];function Xm(n){const e=new Set,t=[];for(const[i,r,a]of Ws)for(const[s,o,c]of qc){const l=[n[i]===0?0:n[i]*s,n[r]===0?0:n[r]*o,n[a]===0?0:n[a]*c],d=l.join(",");e.has(d)||(e.add(d),t.push(l))}return t}const As=[[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]],$c=[[1,0,2],[0,2,1],[2,1,0]];function Km(n){const e=new Set,t=[];for(const[i,r,a]of Ws)for(const[s,o,c]of As){const l=[n[i]===0?0:n[i]*s,n[r]===0?0:n[r]*o,n[a]===0?0:n[a]*c],d=l.join(",");e.has(d)||(e.add(d),t.push(l))}for(const[i,r,a]of $c)for(const[s,o,c]of As){const l=[n[i]===0?0:n[i]*s,n[r]===0?0:n[r]*o,n[a]===0?0:n[a]*c],d=l.join(",");e.has(d)||(e.add(d),t.push(l))}return t}const qm=[[-1,-1,-1],[-1,1,1],[1,-1,1],[1,1,-1]];function $m(n){const e=new Set,t=[];for(const[i,r,a]of Ws)for(const[s,o,c]of As){const l=[n[i]===0?0:n[i]*s,n[r]===0?0:n[r]*o,n[a]===0?0:n[a]*c],d=l.join(",");e.has(d)||(e.add(d),t.push(l))}for(const[i,r,a]of $c)for(const[s,o,c]of qm){const l=[n[i]===0?0:n[i]*s,n[r]===0?0:n[r]*o,n[a]===0?0:n[a]*c],d=l.join(",");e.has(d)||(e.add(d),t.push(l))}return t}function Ym(n){const e=new Set,t=[],i=[[n[0],n[1]],[n[1],n[0]]];for(const r of i){const a=r[0],s=r[1];for(const o of[1,-1])for(const c of[1,-1])for(const l of[1,-1]){const d=[a===0?0:a*o,s===0?0:s*c,n[2]===0?0:n[2]*l],h=d.join(",");e.has(h)||(e.add(h),t.push(d))}}return t}function Zm(n){const e=new Set,t=[];for(const i of[1,-1])for(const r of[1,-1])for(const a of[1,-1]){const s=[n[0]===0?0:n[0]*i,n[1]===0?0:n[1]*r,n[2]===0?0:n[2]*a],o=s.join(",");e.has(o)||(e.add(o),t.push(s))}return t}function Jm(n){const e=n[0],t=n[1],i=-(e+t),r=n[2],a=[[e,t],[-i,-e],[t,i],[-e,-t],[i,e],[-t,-i]],s=new Set,o=[];for(const c of a){const l=c[0],d=c[1],h=[[l,d],[d,l]];for(const f of h){const m=f[0],g=f[1];for(const _ of[1,-1]){const p=[m,g,r===0?0:r*_],u=p.join(",");s.has(u)||(s.add(u),o.push(p))}}}return o}function Qm(n){const e=n[0],t=n[1],i=-(e+t),r=n[2],a=[[e,t],[-i,-e],[t,i],[-e,-t],[i,e],[-t,-i]],s=new Set,o=[];for(const c of a){const l=c[0],d=c[1];for(const h of[1,-1]){const f=[l,d,r===0?0:r*h],m=f.join(",");s.has(m)||(s.add(m),o.push(f))}}return o}function e0(n){const e=n[0],t=n[1],i=-(e+t),r=n[2],a=[[e,t],[i,e],[t,i]],s=new Set,o=[];for(const c of a){const l=c[0],d=c[1],h=[[l,d,r],[d,l,-r],[-l,-d,-r],[-d,-l,r]];for(const f of h){const m=f[0],g=f[1],_=f[2],p=[m,g,_===0?0:_],u=p.join(",");s.has(u)||(s.add(u),o.push(p))}}return o}function t0(n){const e=n[0],t=n[1],i=-(e+t),r=n[2],a=new Set,s=[];if(r===0){const c=[[e,t],[-i,-e],[t,i],[-e,-t],[i,e],[-t,-i]];for(const[l,d]of c){const h=[l,d,0],f=h.join(",");a.has(f)||(a.add(f),s.push(h))}return s}const o=[[e,t],[i,e],[t,i]];for(const[c,l]of o){const d=[c,l,r],h=d.join(",");a.has(h)||(a.add(h),s.push(d))}return s}function Yc(n){switch(n){case"kubni":return"m-3m";case"tetragonalni":return"4/mmm";case"heksagonalni":return"6/mmm";case"trigonalni":return"-3m";case"ortorombicni":return"mmm";default:return"m-3m"}}function kt(n,e,t,i){const r=Vm(n),[a,s,o]=r;if(!Number.isFinite(a)||!Number.isFinite(s)||!Number.isFinite(o))throw new Error("Милерови индекси морају бити коначни бројеви.");if(a===0&&s===0&&o===0)throw new Error("Милерови индекси не могу бити (000).");let c=[];switch(e){case"m-3m":c=dc(r);break;case"m-3":c=Xm(r);break;case"-43m":c=Km(r);break;case"432":c=$m(r);break;case"4/mmm":c=Ym(r);break;case"6/mmm":c=Jm(r);break;case"6/m":c=Qm(r);break;case"-3m":c=e0(r);break;case"32":c=t0(r);break;case"mmm":c=Zm(r);break;default:c=dc(r)}const l=t==="heksagonalni"||t==="trigonalni";return c.map(d=>({hkl:d,normala:Gm(d,t,i),oznaka:Hm(d,l)}))}const S0={"m-3m":(n,e,t)=>kt([n,e,t],"m-3m","kubni").map(i=>i.hkl),"m-3":(n,e,t)=>kt([n,e,t],"m-3","kubni").map(i=>i.hkl),"-43m":(n,e,t)=>kt([n,e,t],"-43m","kubni").map(i=>i.hkl),432:(n,e,t)=>kt([n,e,t],"432","kubni").map(i=>i.hkl),"4/mmm":(n,e,t)=>kt([n,e,t],"4/mmm","tetragonalni").map(i=>i.hkl),"6/mmm":(n,e,t)=>kt([n,e,t],"6/mmm","heksagonalni").map(i=>i.hkl),"6/m":(n,e,t)=>kt([n,e,t],"6/m","heksagonalni").map(i=>i.hkl),"-3m":(n,e,t)=>kt([n,e,t],"-3m","trigonalni").map(i=>i.hkl),32:(n,e,t)=>kt([n,e,t],"32","trigonalni").map(i=>i.hkl),mmm:(n,e,t)=>kt([n,e,t],"mmm","ortorombicni").map(i=>i.hkl)},Zc=new Map,n0=["m-3m","m-3","-43m","432","4/mmm","6/mmm","-3m","32","mmm"];for(const n of n0){let e="kubni";n==="4/mmm"?e="tetragonalni":n==="6/mmm"?e="heksagonalni":n==="-3m"||n==="32"?e="trigonalni":n==="mmm"&&(e="ortorombicni"),Zc.set(n,(t,i)=>kt(t,n,e,i))}const i0=["kubni","tetragonalni","heksagonalni","trigonalni","ortorombicni"];for(const n of i0){const e=Yc(n);Zc.set(n,(t,i)=>kt(t,e,n,i))}function r0(n,e,t,i){const r=t??Yc(e);return kt(n,r,e,i)}const a0={imaPodrazumevanuAnimaciju(n){return(n.animacija??"prelaz")!=="nema"},pocetnaKamera(){return{theta:.64,phi:1.12,udaljenost:4.8}},kreiraj(n,e){const t=e.animacija??"prelaz",r=e.forme.map((C,D)=>{const k=`forma-${D}`,N=C.naziv||(C.hkl.length===4?`{${C.hkl.join(" ")}}`:Fm(C.hkl)),O=r0(C.hkl,e.sistem,e.klasa,e.celija);return{grupaId:k,oznakaForme:N,baznoD:C.d,hkl:C.hkl,ekvivalentne:O}}),a=new it;n.scena3D.add(a);const s=new ht({color:new ce(n.tema.token("--text-primary"))}),o=r.map((C,D)=>new ot({color:new ce(n.tema.token("--primary")),roughness:.32,metalness:.1,flatShading:!0,name:`mat-forma-${D}`}));let c=null,l=null,d="";function h(){const C=new ce(n.tema.token("--primary")),D=new ce(n.tema.token("--accent")),k=new ce(n.tema.token("--bg-elevated"));for(let N=0;N<o.length;N++){const O=o[N],z=r[N].grupaId,H=r.length>1?N/(r.length-1):0,q=C.clone().lerp(D,H);N%2===1&&r.length>2&&q.lerp(k,.22),O.color.copy(q);const J=c===z;O.emissive.copy(J?q.clone().multiplyScalar(.28):new ce(0,0,0))}s.color.set(n.tema.token("--text-primary"))}h();const f=document.createElement("div");f.className="udzbenik-scena-etiketa udzbenik-scena-etiketa--istaknuta",f.hidden=!0,n.slojEtiketa.append(f);let m=.5,g=n.smanjenPokret?.25:0,_=null;if(r.length>1){const C=document.createElement("label");C.className="udzbenik-klizac-oznaka";const D=document.createElement("span");D.textContent=`${Ge("prelazFormi")}: ${r[0].oznakaForme} ↔ ${r[r.length-1].oznakaForme}`,_=document.createElement("input"),_.type="range",_.min="0",_.max="1",_.step="0.01",_.value="0.5",_.className="udzbenik-klizac",_.addEventListener("input",()=>{m=Number(_.value),x(m),n.zatraziRender()}),C.append(D,_),n.gornjeKontrole.append(C)}const p=document.createElement("div");p.className="udzbenik-habitus-forme";const u=new Map;for(const C of r){const D=document.createElement("button");D.type="button",D.className="udzbenik-mohs-cip",D.textContent=C.oznakaForme;const k=()=>{c=C.grupaId;const N=w?.pljosni.find(O=>O.grupaId===C.grupaId);N?(l=new F(...N.centar),d=`${C.oznakaForme} · ${N.oznaka}`):(l=null,d=C.oznakaForme),h(),A(),n.zatraziRender()};D.addEventListener("click",k),D.addEventListener("focus",k),D.addEventListener("blur",()=>{c===C.grupaId&&(c=null,l=null,h(),A(),n.zatraziRender())}),u.set(C.grupaId,D),p.append(D)}const b=document.createElement("span");b.className="udzbenik-habitus-status",p.append(b),n.podnozje.append(p);let S=null,M=null,w=null,T=[];function A(){if(!w)return;const C=w.pljosni.length,D=w.temena.length,k=e.primer?` · ${Ge("primerMinerala")}: ${e.primer}`:"",N=d&&c?` · ${d}`:"";b.textContent=`${C} пљосни, ${D} темена${k}${N}`;for(const[O,z]of u.entries()){const H=w.pljosni.some(q=>q.grupaId===O);z.classList.toggle("udzbenik-mohs-cip--aktivan",c===O),z.classList.toggle("udzbenik-mohs-cip--prigusen",!H)}}function L(C){const D=r.length;return D<=1?r.map(k=>k.baznoD):r.map((k,N)=>{const O=N/(D-1);let z=1;return C<.5?z=1+(.5-C)*2*O*.95:C>.5&&(z=1+(C-.5)*2*(1-O)*.95),k.baznoD*z})}function x(C){S&&(S.geometry.dispose(),a.remove(S)),M&&(M.geometry.dispose(),a.remove(M));const D=L(C),k=[];for(let J=0;J<r.length;J++){const fe=r[J],Ae=D[J];for(const K of fe.ekvivalentne)k.push({normala:K.normala,d:Ae,grupaId:fe.grupaId,oznaka:K.oznaka})}const N=Ki(k);let O=.001;for(const J of N.temena)O=Math.max(O,Math.hypot(J[0],J[1],J[2]));const z=1.48/O;for(const J of N.temena)J[0]*=z,J[1]*=z,J[2]*=z;for(const J of N.pljosni)J.centar[0]*=z,J.centar[1]*=z,J.centar[2]*=z;const H=qi(N),q=H.redosledGrupa.map(J=>{const fe=r.findIndex(Ae=>Ae.grupaId===J);return o[Math.max(0,fe)]});S=new We(H.geometrijaMreze,q),M=new gt(H.geometrijaIvica,s),a.add(S,M),w=N,T=H.mapaTrougaoUPljosan,A()}const v=new js,R=new Ke,U=C=>{if(!S||!w)return;const D=n.platno.getBoundingClientRect();if(D.width<=0||D.height<=0)return;R.x=(C.clientX-D.left)/D.width*2-1,R.y=-((C.clientY-D.top)/D.height)*2+1,v.setFromCamera(R,n.kamera);const k=v.intersectObject(S,!1);if(k.length>0&&k[0].faceIndex!==void 0&&k[0].faceIndex!==null){const N=T[k[0].faceIndex],O=N!==void 0?w.pljosni[N]:void 0;if(O){const z=r.find(H=>H.grupaId===O.grupaId);c=O.grupaId,l=new F(...O.centar),d=`${z?.oznakaForme??O.grupaId} · ${O.oznaka}`,h(),A(),n.zatraziRender();return}}c!==null&&C.pointerType==="mouse"&&(c=null,l=null,h(),A(),n.zatraziRender())};return n.platno.addEventListener("pointermove",U),x(m),{azuriraj(C){t==="prelaz"&&r.length>1?(g=(g+C*.14)%1,m=.5-.5*Math.cos(g*Math.PI*2),_&&(_.value=m.toFixed(2)),a.rotation.y+=C*.25,x(m)):t==="rotacija"&&(a.rotation.y+=C*.42)},korak(){t==="prelaz"&&r.length>1?(g=(g+.125)%1,m=.5-.5*Math.cos(g*Math.PI*2),_&&(_.value=m.toFixed(2)),x(m)):a.rotation.y+=.35},resetuj(){a.rotation.set(0,0,0),m=.5,g=.25,_&&(_.value="0.5"),c=null,l=null,h(),x(.5)},osveziTemu(){h()},posleRendera(){if(!c||!l){f.hidden=!0;return}a.updateMatrixWorld(!0);const C=l.clone().applyMatrix4(a.matrixWorld),D=n.projektujU2D(C);if(!D.vidljivo){f.hidden=!0;return}f.textContent=d,f.hidden=!1,f.style.transform=`translate(-50%, -120%) translate(${D.x.toFixed(1)}px, ${D.y.toFixed(1)}px)`},raspolazi(){n.platno.removeEventListener("pointermove",U),It(a),s.dispose();for(const C of o)C.dispose()}}}},hc={2:{kb:2,nazivOblika:"Линеарни",granicniOdnos:.155,vrhovi:[[0,0,1.4],[0,0,-1.4]],trougloviIndeksi:[]},3:{kb:3,nazivOblika:"Троугаони",granicniOdnos:.155,vrhovi:[[1.4,0,0],[-.7,1.212,0],[-.7,-1.212,0]],trougloviIndeksi:[0,1,2]},4:{kb:4,nazivOblika:"Тетраедарски",granicniOdnos:.225,vrhovi:[[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]].map(([n,e,t])=>[n*.9,e*.9,t*.9]),trougloviIndeksi:[0,1,2,0,3,1,0,2,3,1,3,2]},6:{kb:6,nazivOblika:"Октаедарски",granicniOdnos:.414,vrhovi:[[1.4,0,0],[-1.4,0,0],[0,1.4,0],[0,-1.4,0],[0,0,1.4],[0,0,-1.4]],trougloviIndeksi:[0,2,4,2,1,4,1,3,4,3,0,4,0,5,2,2,5,1,1,5,3,3,5,0]},8:{kb:8,nazivOblika:"Кубични",granicniOdnos:.732,vrhovi:[[-1,-1,-1],[1,-1,-1],[1,1,-1],[-1,1,-1],[-1,-1,1],[1,-1,1],[1,1,1],[-1,1,1]].map(([n,e,t])=>[n*.85,e*.85,t*.85]),trougloviIndeksi:[0,2,1,0,3,2,4,5,6,4,6,7,0,1,5,0,5,4,1,2,6,1,6,5,2,3,7,2,7,6,3,0,4,3,4,7]},12:{kb:12,nazivOblika:"Кубооктаедарски",granicniOdnos:1,vrhovi:[[1,1,0],[1,-1,0],[-1,-1,0],[-1,1,0],[1,0,1],[1,0,-1],[-1,0,-1],[-1,0,1],[0,1,1],[0,1,-1],[0,-1,-1],[0,-1,1]].map(([n,e,t])=>[n*1.05,e*1.05,t*1.05]),trougloviIndeksi:[0,8,4,1,4,11,2,11,7,3,7,8,0,5,9,1,10,5,2,6,10,3,9,6,0,4,1,0,1,5,2,7,3,2,3,6,8,9,3,8,3,0,11,1,2,11,2,10]}},s0={imaPodrazumevanuAnimaciju(n){return n.prikazi_odnos_radijusa!==!1},pocetnaKamera(){return{theta:.65,phi:1.18,udaljenost:5.4}},kreiraj(n,e){const t=new it;n.scena3D.add(t);const i=hc[e.kb]??hc[4],r=.52;let a=r*i.granicniOdnos;const s=new xn(a,24,24),o=new ot({color:new ce(n.tema.token("--accent")),roughness:.25,metalness:.2}),c=new We(s,o);t.add(c);const l=new xn(r,24,24),d=new ot({color:new ce(n.tema.token("--primary")),roughness:.35,metalness:.1,transparent:!0,opacity:.85}),h=new it;for(const[T,A,L]of i.vrhovi){const x=new We(l,d);x.position.set(T,A,L),h.add(x)}t.add(h);let f=null,m=null;const g=new ot({color:new ce(n.tema.token("--primary")),transparent:!0,opacity:.22,roughness:.2,side:St}),_=new ht({color:new ce(n.tema.token("--text-secondary")),linewidth:2});if(i.trougloviIndeksi.length>=3){const T=new Ze,A=[];for(const x of i.trougloviIndeksi){const v=i.vrhovi[x];A.push(v[0],v[1],v[2])}T.setAttribute("position",new He(A,3)),T.computeVertexNormals(),f=new We(T,g),t.add(f);const L=new jr(T);m=new gt(L,_),t.add(m)}const p=e.katjon||"Katjon",u=e.anjon||"Anjon",b=document.createElement("div");b.className="udzbenik-scena-status",b.textContent=`КБ = ${i.kb} (${i.nazivOblika}) • Гранични однос RA/RX = ${i.granicniOdnos.toFixed(3)} • ${p} / ${u}`,n.podnozje.append(b);let S=0;const M=e.prikazi_odnos_radijusa!==!1;function w(){o.color.set(n.tema.token("--accent")),d.color.set(n.tema.token("--primary")),g.color.set(n.tema.token("--primary")),_.color.set(n.tema.token("--text-secondary"))}return{azuriraj(T){if(S+=T,t.rotation.y=S*.35,M){const A=Math.sin(S*1.8);if(A<-.2){const L=.08*(Math.abs(A)-.2);c.position.set(Math.sin(S*22)*L,Math.cos(S*19)*L,Math.sin(S*25)*L),c.scale.setScalar(.72)}else c.position.set(0,0,0),c.scale.setScalar(1)}},korak(){S+=.3,t.rotation.y+=.2},resetuj(){S=0,c.position.set(0,0,0),c.scale.setScalar(1),t.rotation.set(0,0,0)},osveziTemu(){w()},raspolazi(){s.dispose(),o.dispose(),l.dispose(),d.dispose(),f&&f.geometry.dispose(),m&&m.geometry.dispose(),g.dispose(),_.dispose(),It(t),b.remove()}}}},o0={imaPodrazumevanuAnimaciju(){return!1},pocetnaKamera(n){return{theta:.65,phi:1.12,udaljenost:(n.prikaz??"celija")==="supercelija"?8.2:6.2}},kreiraj(n,e){const t=e.prikaz??"celija",i=e.stil??"kugle-stapici",r=e.prikazi_celiju??!0,a=e.oznake_atoma??!0,s=e.poluprecnici??"jonski";let o=!1,c=1.15,l=null,d=-1;const h=new it,f=new it,m=new it,g=new it;h.add(g,m,f),n.scena3D.add(h);const _=new ht({color:new ce(n.tema.token("--text-secondary"))}),p=new ot({color:new ce(n.tema.token("--text-muted")),roughness:.45,metalness:.15}),u=new Ui({color:new ce(n.tema.token("--accent")),wireframe:!0}),b=new We(new xn(1,14,12),u);b.visible=!1,h.add(b);const S=document.createElement("div");S.className="udzbenik-scena-etiketa udzbenik-scena-etiketa--atom",S.hidden=!0,n.slojEtiketa.append(S);const M=document.createElement("div");if(M.className="udzbenik-struktura-kontrole",i==="kugle-stapici"){const O=document.createElement("label");O.className="udzbenik-klizac-oznaka";const z=document.createElement("span");z.textContent=`${Ge("faktorVeza")}: ×1,15`;const H=document.createElement("input");H.type="range",H.min="0.85",H.max="1.40",H.step="0.05",H.value="1.15",H.className="udzbenik-klizac",H.addEventListener("input",()=>{c=Number(H.value),z.textContent=`${Ge("faktorVeza")}: ×${c.toFixed(2).replace(".",",")}`,l&&(C(l),n.zatraziRender())}),O.append(z,H),M.append(O)}const w=document.createElement("span");if(w.className="udzbenik-atom-status",w.setAttribute("aria-live","polite"),a){const O=document.createElement("button");O.type="button",O.className="udzbenik-dugme udzbenik-dugme--malo",O.textContent=Ge("sledeciAtom"),O.addEventListener("click",()=>{T.length!==0&&(d=(d+1)%T.length,v(d),n.zatraziRender())}),M.append(O,w)}M.childNodes.length>0&&n.gornjeKontrole.append(M);let T=[],A=null,L=new F,x=1;function v(O){if(O<0||O>=T.length){A=null,b.visible=!1,S.hidden=!0,w.textContent="";return}const z=T[O];A=z.atom;const H=z.mesh.scale.x*1.25;b.position.copy(z.mesh.position),b.scale.setScalar(H),b.visible=!0;const q=`(${z.atom.fx.toFixed(3)}, ${z.atom.fy.toFixed(3)}, ${z.atom.fz.toFixed(3)})`;S.textContent=`${z.atom.simbol} [${z.atom.oznaka}] ${q}`,w.textContent=`${z.atom.simbol} (${z.atom.oznaka}): ${q}`}function R(O){It(O),O.clear()}function U(O){n.podnozje.replaceChildren();const z=document.createElement("div");z.className="udzbenik-cpk-legenda",z.setAttribute("aria-label",Ge("legendaElemenata"));const H=document.createElement("div");H.className="udzbenik-cpk-stavke";let q=!1;for(const Ae of O){const K=ws(Ae),ne=lc(Ae,s);s==="jonski"&&ne.koriscenaVrsta==="kovalentni"&&(q=!0);const ue=document.createElement("span");ue.className="udzbenik-cpk-cip";const ae=document.createElement("span");ae.className="udzbenik-cpk-boja",ae.style.backgroundColor=K.bojaHex,ae.setAttribute("aria-hidden","true");const ee=ne.koriscenaVrsta==="jonski"&&ne.jon?`${K.simbol} (${ne.jon})`:K.simbol,_e=ne.poluprecnik.toFixed(2).replace(".",","),de=document.createElement("span");de.textContent=`${ee} — ${K.naziv} (r = ${_e} Å)`,ue.append(ae,de),H.append(ue)}const J=document.createElement("p");J.className="udzbenik-scena-izvor";const fe=i==="kugle-stapici"?` · ${Ge("detekcijaVezaKovalentniOznaka")}${c.toFixed(2).replace(".",",")}`:"";if(s==="jonski"){const Ae=q?`${ys.izvor}; ${Ge("kovalentnaRezervaOznaka")}: ${cc}`:ys.izvor;J.textContent=`${Ge("poluprecniciJonskiOznaka")} (${Ge("izvorPodataka")}: ${Ae})${fe}`}else J.textContent=`${Ge("poluprecniciKovalentniOznaka")} (${Ge("izvorPodataka")}: ${cc})${fe}`;z.append(H,J),n.podnozje.append(z)}function C(O){R(f),R(m),R(g),T=[];const z=Gs(O.celija),H=t==="supercelija"?2:1,q=Cn(H,H,H,z);L=new F(q[0]*.5,q[1]*.5,q[2]*.5);const J=Math.max(O.celija.a*H,O.celija.b*H,O.celija.c*H);x=3.6/Math.max(1,J);const fe=[],Ae=new Set,K=[];for(const ee of O.atomi){K.includes(ee.simbol)||K.push(ee.simbol);const _e=ws(ee.simbol),de=lc(ee.simbol,s),Y=(ee.fx%1+1)%1,re=(ee.fy%1+1)%1,oe=(ee.fz%1+1)%1,I=Y<.001?[0,1]:[0],Ie=re<.001?[0,1]:[0],Pe=oe<.001?[0,1]:[0];for(let Ce=0;Ce<H;Ce++)for(let Me=0;Me<H;Me++)for(let Fe=0;Fe<H;Fe++)for(const Re of I)for(const P of Ie)for(const E of Pe){const G=Y+Ce+Re,Q=re+Me+P,ie=oe+Fe+E;if(G>H+.001||Q>H+.001||ie>H+.001)continue;const Z=`${G.toFixed(3)},${Q.toFixed(3)},${ie.toFixed(3)},${ee.simbol}`;if(Ae.has(Z))continue;Ae.add(Z);const we=Cn(G,Q,ie,z);fe.push({oznaka:ee.oznaka,simbol:ee.simbol,fx:G,fy:Q,fz:ie,pozicija:new F(we[0],we[1],we[2]),poluprecnikPrikaza:de.poluprecnik,kovalentniPoluprecnik:_e.kovalentniPoluprecnik,bojaHex:_e.bojaHex})}}const ne=new xn(1,20,16),ue=new Map,ae=i==="kugle"?.52:.25;for(const ee of fe){let _e=ue.get(ee.simbol);_e||(_e=new ot({color:new ce(ee.bojaHex),roughness:.32,metalness:.1}),ue.set(ee.simbol,_e));const de=new We(ne,_e);de.position.copy(ee.pozicija).sub(L).multiplyScalar(x);const Y=Math.max(.045,ee.poluprecnikPrikaza*ae*x);de.scale.setScalar(Y),f.add(de),T.push({mesh:de,atom:ee})}if(i==="kugle-stapici"){const ee=new Ji(1,1,1,10,1),_e=new F(0,1,0),de=Math.max(.035,.09*x);for(let Y=0;Y<fe.length;Y++){const re=fe[Y];for(let oe=Y+1;oe<fe.length;oe++){const I=fe[oe],Ie=re.pozicija.distanceTo(I.pozicija),Pe=(re.kovalentniPoluprecnik+I.kovalentniPoluprecnik)*c;if(Ie>.35&&Ie<=Pe){const Ce=T[Y].mesh.position,Fe=T[oe].mesh.position.clone().sub(Ce),Re=Fe.length();if(Re<1e-4)continue;const P=new We(ee,p.clone());P.position.copy(Ce).addScaledVector(Fe,.5),P.quaternion.setFromUnitVectors(_e,Fe.clone().normalize()),P.scale.set(de,Re,de),m.add(P)}}}ee.dispose()}if(r){const ee=[],_e=[[[0,0,0],[1,0,0]],[[1,0,0],[1,1,0]],[[1,1,0],[0,1,0]],[[0,1,0],[0,0,0]],[[0,0,1],[1,0,1]],[[1,0,1],[1,1,1]],[[1,1,1],[0,1,1]],[[0,1,1],[0,0,1]],[[0,0,0],[0,0,1]],[[1,0,0],[1,0,1]],[[1,1,0],[1,1,1]],[[0,1,0],[0,1,1]]];for(let Y=0;Y<H;Y++)for(let re=0;re<H;re++)for(let oe=0;oe<H;oe++)for(const[I,Ie]of _e){const Pe=Cn(I[0]+Y,I[1]+re,I[2]+oe,z),Ce=Cn(Ie[0]+Y,Ie[1]+re,Ie[2]+oe,z),Me=new F(...Pe).sub(L).multiplyScalar(x),Fe=new F(...Ce).sub(L).multiplyScalar(x);ee.push(Me.x,Me.y,Me.z,Fe.x,Fe.y,Fe.z)}const de=new Ze;de.setAttribute("position",new He(ee,3)),g.add(new gt(de,_.clone()))}U(K),d=-1,v(-1)}const D=new js,k=new Ke,N=O=>{if(!a||T.length===0)return;const z=n.platno.getBoundingClientRect();if(z.width<=0||z.height<=0)return;k.x=(O.clientX-z.left)/z.width*2-1,k.y=-((O.clientY-z.top)/z.height)*2+1,D.setFromCamera(k,n.kamera);const H=D.intersectObjects(T.map(q=>q.mesh),!1);if(H.length>0){const q=H[0].object,J=T.findIndex(fe=>fe.mesh===q);J!==d&&(d=J,v(J),n.zatraziRender())}else d!==-1&&O.pointerType==="mouse"&&(d=-1,v(-1),n.zatraziRender())};return a&&n.platno.addEventListener("pointermove",N),n.api.ucitajStrukturuCif(e.mineral).then(O=>{o||(l=Im(O),C(l),n.zatraziRender())}).catch(O=>{if(o)return;const z=(O instanceof At&&O.status===404,Ge("strukturaNedostupna"));n.prikaziRezervu(z)}),{resetuj(){d=-1,v(-1)},osveziTemu(O){_.color.set(O.token("--text-secondary")),p.color.set(O.token("--text-muted")),u.color.set(O.token("--accent"));for(const z of g.children){const H=z;H.material instanceof ht&&H.material.color.set(O.token("--text-secondary"))}for(const z of m.children){const H=z;H.material instanceof ot&&H.material.color.set(O.token("--text-muted"))}},posleRendera(){if(!A||d<0){S.hidden=!0;return}const O=T[d];if(!O)return;O.mesh.updateMatrixWorld(!0);const z=O.mesh.position.clone().applyMatrix4(h.matrixWorld),H=n.projektujU2D(z);if(!H.vidljivo){S.hidden=!0;return}S.hidden=!1,S.style.transform=`translate(-50%, -130%) translate(${H.x.toFixed(1)}px, ${H.y.toFixed(1)}px)`},raspolazi(){o=!0,a&&n.platno.removeEventListener("pointermove",N),It(h),_.dispose(),p.dispose(),u.dispose()}}}},Pa=[{kljuc:"kubni",naziv:"Кубни",kratko:"Кубни",odnosIvica:"a = b = c",odnosUglova:"α = β = γ = 90°",reprezentativniOblik:"коцка",celija:{a:1.15,b:1.15,c:1.15,alpha:90,beta:90,gamma:90}},{kljuc:"tetragonalni",naziv:"Тетрагонални",kratko:"Тетраг.",odnosIvica:"a = b ≠ c",odnosUglova:"α = β = γ = 90°",reprezentativniOblik:"тетрагонална призма",celija:{a:1,b:1,c:1.62,alpha:90,beta:90,gamma:90}},{kljuc:"ortorombicni",naziv:"Орторомбични",kratko:"Орторомб.",odnosIvica:"a ≠ b ≠ c",odnosUglova:"α = β = γ = 90°",reprezentativniOblik:"правоугаона призма („цигла“)",celija:{a:.85,b:1.22,c:1.58,alpha:90,beta:90,gamma:90}},{kljuc:"heksagonalni",naziv:"Хексагонални",kratko:"Хексаг.",odnosIvica:"a = b ≠ c",odnosUglova:"α = β = 90°, γ = 120°",reprezentativniOblik:"хексагонална призма",celija:{a:1.08,b:1.08,c:1.55,alpha:90,beta:90,gamma:120}},{kljuc:"trigonalni",naziv:"Тригонални",kratko:"Тригон.",odnosIvica:"a = b = c",odnosUglova:"α = β = γ ≠ 90°",reprezentativniOblik:"ромбоедар",celija:{a:1.18,b:1.18,c:1.18,alpha:75,beta:75,gamma:75}},{kljuc:"monoklinicni",naziv:"Моноклинични",kratko:"Монокл.",odnosIvica:"a ≠ b ≠ c",odnosUglova:"α = γ = 90°, β ≠ 90°",reprezentativniOblik:"кос паралелопипед (β ≠ 90°)",celija:{a:.92,b:1.22,c:1.48,alpha:90,beta:112,gamma:90}},{kljuc:"triklinicni",naziv:"Триклинични",kratko:"Трикл.",odnosIvica:"a ≠ b ≠ c",odnosUglova:"α ≠ β ≠ γ ≠ 90°",reprezentativniOblik:"кос паралелопипед (α, β, γ ≠ 90°)",celija:{a:.88,b:1.18,c:1.46,alpha:78,beta:109,gamma:103}}],c0={a:1.15,b:1.15,c:1.15,alpha:90,beta:90,gamma:90};function l0(n,e,t){const i=Math.max(0,Math.min(1,t));return{a:n.a+(e.a-n.a)*i,b:n.b+(e.b-n.b)*i,c:n.c+(e.c-n.c)*i,alpha:n.alpha+(e.alpha-n.alpha)*i,beta:n.beta+(e.beta-n.beta)*i,gamma:n.gamma+(e.gamma-n.gamma)*i}}function Jc(n){const e=Gs(n),t=new F(...e.va),i=new F(...e.vb),r=new F(...e.vc),a=t.clone().add(i).add(r).multiplyScalar(.5),s=[],o=[[0,0,0],[1,0,0],[1,1,0],[0,1,0],[0,0,1],[1,0,1],[1,1,1],[0,1,1]];for(const[g,_,p]of o){const u=Cn(g,_,p,e);s.push(new F(u[0]-a.x,u[1]-a.y,u[2]-a.z))}const c=[[0,1],[1,2],[2,3],[3,0],[4,5],[5,6],[6,7],[7,4],[0,4],[1,5],[2,6],[3,7]],l=[];for(const[g,_]of c){const p=s[g],u=s[_];l.push(p.x,p.y,p.z,u.x,u.y,u.z)}const d=new Ze;d.setAttribute("position",new He(l,3));const h=[[0,3,2,1],[4,5,6,7],[0,1,5,4],[2,3,7,6],[1,2,6,5],[3,0,4,7]],f=[];for(const[g,_,p,u]of h){const b=s[g],S=s[_],M=s[p],w=s[u];f.push(b.x,b.y,b.z,S.x,S.y,S.z,M.x,M.y,M.z,b.x,b.y,b.z,M.x,M.y,M.z,w.x,w.y,w.z)}const m=new Ze;return m.setAttribute("position",new He(f,3)),m.computeVertexNormals(),{ivice:d,mreza:m,poreklo:s[0],va:t,vb:i,vc:r}}function Da(n,e,t,i){const r=e.clone().normalize(),a=t.clone().normalize(),s=18,o=[];let c=n.clone();for(let d=0;d<=s;d++){const h=d/s,f=r.clone().multiplyScalar(1-h).addScaledVector(a,h).normalize(),m=n.clone().addScaledVector(f,i);if(d===Math.floor(s/2)&&(c=n.clone().addScaledVector(f,i*1.38)),d>0){const g=(d-1)/s,_=r.clone().multiplyScalar(1-g).addScaledVector(a,g).normalize(),p=n.clone().addScaledVector(_,i);o.push(p.x,p.y,p.z,m.x,m.y,m.z)}}const l=new Ze;return l.setAttribute("position",new He(o,3)),{geometrija:l,sredina:c}}function u0(n,e,t){if(n==="heksagonalni"){const s=.58+.22*t,o=1.35-(1.35-.68)*t,c=[{normala:[0,1,0],d:s},{normala:[0,-1,0],d:s},{normala:[1,0,0],d:.68},{normala:[-1,0,0],d:.68},{normala:[0,0,1],d:.68+.14*t},{normala:[0,0,-1],d:.68+.14*t},{normala:[.5,0,Math.sqrt(3)/2],d:o},{normala:[-.5,0,Math.sqrt(3)/2],d:o},{normala:[.5,0,-Math.sqrt(3)/2],d:o},{normala:[-.5,0,-Math.sqrt(3)/2],d:o}],l=[{normala:[0,1,0],d:s},{normala:[0,-1,0],d:s}];if(t>.85){for(let g=0;g<6;g++){const _=g*Math.PI/3;l.push({normala:[Math.cos(_),0,Math.sin(_)],d:.68})}const f=Ki(l),m=qi(f);return{mreza:m.geometrijaMreze,ivice:m.geometrijaIvica}}const d=Ki(c),h=qi(d);return{mreza:h.geometrijaMreze,ivice:h.geometrijaIvica}}const i={a:e.a*.92,b:e.b*.92,c:e.c*.92,alpha:e.alpha,beta:e.beta,gamma:e.gamma},r=Jc(i);return{mreza:r.mreza,ivice:r.ivice}}const d0={imaPodrazumevanuAnimaciju(n){return(n.animacija??"rotacija")!=="nema"},pocetnaKamera(){return{theta:.42,phi:1.15,udaljenost:6.8}},kreiraj(n,e){const t=e.animacija??"rotacija",i=e.prikazi_ose??!0,r=e.prikazi_celiju??!0;let a=e.sistem==="svi"?"heksagonalni":e.sistem;e.sistem==="svi"&&(a="kubni");let s=n.smanjenPokret||t!=="uporedi"?1:0,o=0;const c=new it,l=new it,d=new it;r?(l.position.set(-1.55,-.05,0),d.position.set(1.55,-.05,0)):d.position.set(0,-.05,0),c.add(l,d),n.scena3D.add(c);const h=new ot({color:new ce(n.tema.token("--primary")),transparent:!0,opacity:.14,roughness:.45,metalness:.05,side:St,depthWrite:!1}),f=new ht({color:new ce(n.tema.token("--text-secondary"))}),m=new ht({color:new ce(n.tema.token("--danger"))}),g=new ht({color:new ce(n.tema.token("--success"))}),_=new ht({color:new ce(n.tema.token("--accent"))}),p=new ht({color:new ce(n.tema.token("--warning"))}),u=new ot({color:new ce(n.tema.token("--primary")),transparent:!0,opacity:.78,roughness:.35,metalness:.08,flatShading:!0}),b=new ht({color:new ce(n.tema.token("--text-primary"))}),S=["a","b","c","α","β","γ"],M=new Map,w=new Map;if(i&&r)for(const D of S){const k=document.createElement("span");k.className="udzbenik-scena-etiketa",k.textContent=D,n.slojEtiketa.append(k),M.set(D,k),w.set(D,new F)}const T=document.createElement("div");T.className="udzbenik-scena-info-red",n.podnozje.append(T);const A=new Map;if(e.sistem==="svi"){const D=document.createElement("div");D.className="udzbenik-sistemi-traka",D.setAttribute("role","group"),D.setAttribute("aria-label",Ge("izaberiKristalniSistem"));for(const k of Pa){const N=document.createElement("button");N.type="button",N.className="udzbenik-sistem-kartica",N.dataset.sistem=k.kljuc,N.setAttribute("aria-pressed",String(k.kljuc===a));const O=document.createElement("span");O.className="udzbenik-sistem-kartica-naslov",O.textContent=k.naziv;const z=document.createElement("span");z.className="udzbenik-sistem-kartica-meta",z.textContent=`${k.odnosIvica} · ${k.odnosUglova}`,N.append(O,z),N.addEventListener("click",()=>{a=k.kljuc,s=n.smanjenPokret||t!=="uporedi"?1:0,L(),U(),n.zatraziRender()}),A.set(k.kljuc,N),D.append(N)}n.gornjeKontrole.append(D)}function L(){for(const[D,k]of A.entries()){const N=D===a;k.classList.toggle("udzbenik-sistem-kartica--aktivna",N),k.setAttribute("aria-pressed",String(N))}}function x(){return Pa.find(D=>D.kljuc===a)??Pa[0]}function v(D){for(const k of D.children){const N=k.geometry;N&&N.dispose()}D.clear()}function R(){if(t!=="uporedi"||a==="kubni")return 1;const D=s%1;if(D<.4){const k=D/.4;return k*k*(3-2*k)}if(D<.72)return 1;if(D<.92){const k=(D-.72)/.2;return 1-k*k*(3-2*k)}return 0}function U(){const D=x(),k=R(),N=l0(c0,D.celija,k);if(v(l),v(d),r){const q=Jc(N),J=new We(q.mreza,h),fe=new gt(q.ivice,f);if(l.add(J,fe),i){const Ae=q.poreklo,K=Ae.clone().addScaledVector(q.va,1.16),ne=Ae.clone().addScaledVector(q.vb,1.16),ue=Ae.clone().addScaledVector(q.vc,1.16),ae=new Ze().setFromPoints([Ae,K]),ee=new Ze().setFromPoints([Ae,ne]),_e=new Ze().setFromPoints([Ae,ue]);l.add(new Wi(ae,m),new Wi(ee,g),new Wi(_e,_));const de=Da(Ae,q.vb,q.vc,.36),Y=Da(Ae,q.va,q.vc,.44),re=Da(Ae,q.va,q.vb,.36);l.add(new gt(de.geometrija,p),new gt(Y.geometrija,p),new gt(re.geometrija,p)),w.get("a")?.copy(K),w.get("b")?.copy(ne),w.get("c")?.copy(ue),w.get("α")?.copy(de.sredina),w.get("β")?.copy(Y.sredina),w.get("γ")?.copy(re.sredina)}}const O=u0(D.kljuc,N,k);d.add(new We(O.mreza,u),new gt(O.ivice,b)),T.replaceChildren();const z=document.createElement("strong");z.textContent=`${D.naziv}: `;const H=document.createElement("span");H.textContent=`${D.odnosIvica} · ${D.odnosUglova} — облик: ${D.reprezentativniOblik}`,T.append(z,H)}function C(){if(!i||!r)return;l.updateMatrixWorld(!0);const D=x();for(const[k,N]of M.entries()){const O=w.get(k);if(!O)continue;const z=O.clone().applyMatrix4(l.matrixWorld),H=n.projektujU2D(z);if(!H.vidljivo){N.hidden=!0;continue}N.hidden=!1,N.style.transform=`translate(-50%, -50%) translate(${H.x.toFixed(1)}px, ${H.y.toFixed(1)}px)`;const q=k==="c"&&D.celija.c!==D.celija.a||k==="b"&&D.celija.b!==D.celija.a||k==="α"&&D.celija.alpha!==90||k==="β"&&D.celija.beta!==90||k==="γ"&&D.celija.gamma!==90;N.classList.toggle("udzbenik-scena-etiketa--istaknuta",q)}}return L(),U(),{azuriraj(D){t==="uporedi"?(s=(s+D*.18)%1,o+=D*.22,c.rotation.y=Math.sin(o)*.18,U()):t==="rotacija"&&(c.rotation.y+=D*.45)},korak(){t==="uporedi"?(s=(s+.15)%1,o+=.45,c.rotation.y=Math.sin(o)*.18,U()):c.rotation.y+=.35},resetuj(){c.rotation.set(0,0,0),o=0,s=n.smanjenPokret||t!=="uporedi"?1:0,U()},osveziTemu(D){h.color.set(D.token("--primary")),f.color.set(D.token("--text-secondary")),m.color.set(D.token("--danger")),g.color.set(D.token("--success")),_.color.set(D.token("--accent")),p.color.set(D.token("--warning")),u.color.set(D.token("--primary")),b.color.set(D.token("--text-primary"))},posleRendera(){C()},raspolazi(){It(c),h.dispose(),f.dispose(),m.dispose(),g.dispose(),_.dispose(),p.dispose(),u.dispose(),b.dispose()}}}},Yt="Klein, C. & Dutrow, B. (2007), Manual of Mineral Science (23rd ed.), John Wiley & Sons, Table 2.3 (Knoop microhardness HK, kgf/mm²; теренске пробе: нокат ~2,5, бакарни новчић ~3, нож/стакло ~5,5, турпија ~6,5).",An=[{mohs:1,kljuc:"talk",naziv:"Талк",formula:"Mg₃Si₄O₁₀(OH)₂",apsolutnaKnoop:1,izvor:Yt},{mohs:2,kljuc:"gips",naziv:"Гипс",formula:"CaSO₄·2H₂O",apsolutnaKnoop:32,izvor:Yt},{mohs:3,kljuc:"kalcit",naziv:"Калцит",formula:"CaCO₃",apsolutnaKnoop:135,izvor:Yt},{mohs:4,kljuc:"fluorit",naziv:"Флуорит",formula:"CaF₂",apsolutnaKnoop:163,izvor:Yt},{mohs:5,kljuc:"apatit",naziv:"Апатит",formula:"Ca₅(PO₄)₃(F,Cl,OH)",apsolutnaKnoop:430,izvor:Yt},{mohs:6,kljuc:"ortoklas",naziv:"Ортоклас",formula:"KAlSi₃O₈",apsolutnaKnoop:560,izvor:Yt},{mohs:7,kljuc:"kvarc",naziv:"Кварц",formula:"SiO₂",apsolutnaKnoop:820,izvor:Yt},{mohs:8,kljuc:"topaz",naziv:"Топаз",formula:"Al₂SiO₄(F,OH)₂",apsolutnaKnoop:1340,izvor:Yt},{mohs:9,kljuc:"korund",naziv:"Корунд",formula:"Al₂O₃",apsolutnaKnoop:2100,izvor:Yt},{mohs:10,kljuc:"dijamant",naziv:"Дијамант",formula:"C",apsolutnaKnoop:7e3,izvor:Yt}],h0=[{naziv:"Нокат (~2,5)",mohs:2.5},{naziv:"Бакарни новчић (~3)",mohs:3},{naziv:"Нож / стакло (~5,5)",mohs:5.5},{naziv:"Челична турпија (~6,5)",mohs:6.5}];function fc(n,e){if(!e||e.length===0)return!1;const t=n.kljuc.toLowerCase(),i=n.naziv.toLowerCase();return e.some(r=>{const a=r.trim().toLowerCase();return a===t||a===i})}const f0={imaPodrazumevanuAnimaciju(){return!0},pocetnaKamera(){return{theta:.16,phi:1.18,udaljenost:8.6}},kreiraj(n,e){const t=e.prikazi_apsolutnu??!1,i=e.prikazi_terenske_probe??!0,r=e.istaknuti??[];let a=!1,s=0,o=6,c=5,l=n.smanjenPokret?.65:0;const d=new it;d.position.set(0,-.35,0),n.scena3D.add(d);const h=-4.05,f=.9,m=-.7,g=2.75,_=new ot({color:new ce(n.tema.token("--bg-elevated")),roughness:.7,metalness:.05}),p=new We(new gn(9.6,.14,1.4),_);p.position.set(0,m-.07,-.35),d.add(p);const u=[],b=new ht({color:new ce(n.tema.token("--text-primary"))}),S=new gn(.66,1,.66),M=new jr(S);for(let Y=0;Y<An.length;Y++){const re=An[Y],oe=fc(re,r),I=new ce(n.tema.token(oe?"--accent":"--primary")),Ie=new ot({color:I,emissive:oe?new ce(n.tema.token("--accent")).multiplyScalar(.22):new ce(0,0,0),roughness:.35,metalness:.12}),Pe=new We(S,Ie),Ce=new gt(M,b),Me=h+Y*f;Pe.position.set(Me,m+.5,-.35),Ce.position.copy(Pe.position),d.add(Pe,Ce);const Fe=document.createElement("span");Fe.className="udzbenik-scena-etiketa udzbenik-scena-etiketa--mala",oe&&Fe.classList.add("udzbenik-scena-etiketa--istaknuta"),Fe.textContent=`${re.mohs}`,n.slojEtiketa.append(Fe),u.push({mineral:re,istaknut:oe,mesh:Pe,ivice:Ce,mat:Ie,etiketaDom:Fe})}const w=new ot({color:new ce(n.tema.token("--warning")),roughness:.4}),T=[];if(i){const Y=new Ji(.035,.035,.65,8);for(const re of h0){const oe=h+(re.mohs-1)*f,I=new We(Y,w);I.position.set(oe,m+.32,.18),d.add(I);const Ie=document.createElement("span");Ie.className="udzbenik-scena-etiketa udzbenik-scena-etiketa--proba",Ie.textContent=re.naziv,n.slojEtiketa.append(Ie),T.push({x:oe,tekst:re.naziv,dom:Ie,stub:I})}}const A=new it;A.position.set(0,m-.52,1.35),d.add(A);const L=new ot({color:new ce(n.tema.token("--primary-light")),roughness:.45,metalness:.08}),x=new We(new gn(3.4,.24,.92),L),v=new gt(new jr(x.geometry),b);A.add(x,v);const R=new ot({color:new ce(n.tema.token("--danger")),roughness:.85}),U=new We(new gn(1,.05,.11),R);U.position.set(-1.1,.125,0),U.visible=!1,A.add(U);const C=new ot({color:new ce(n.tema.token("--accent")),roughness:.25,metalness:.2}),D=new We(new Os(.22,.72,6),C);D.rotation.x=Math.PI,D.rotation.z=-.22,D.position.set(-1.1,.5,0),A.add(D);const k=document.createElement("div");k.className="udzbenik-mohs-kontrole";const N=document.createElement("div");N.className="udzbenik-mohs-dugmad",N.setAttribute("role","group"),N.setAttribute("aria-label",Ge("ordinalnaTvrdocaOznaka"));const O=[];for(let Y=0;Y<An.length;Y++){const re=An[Y],oe=document.createElement("button");oe.type="button",oe.className="udzbenik-mohs-cip",fc(re,r)&&oe.classList.add("udzbenik-mohs-cip--istaknut"),oe.textContent=`${re.mohs}. ${re.naziv}`,oe.addEventListener("click",()=>{Ae(Y)}),O.push(oe),N.append(oe)}k.append(N);const z=document.createElement("div");z.className="udzbenik-mohs-akcije";const H=document.createElement("button");H.type="button",H.className="udzbenik-dugme udzbenik-dugme--malo",H.textContent=Ge("zameniMinerale"),H.addEventListener("click",()=>{const Y=o;o=c,c=Y,l=n.smanjenPokret?.75:0,ae(),n.zatraziRender()}),z.append(H);let q=null;t&&(q=document.createElement("button"),q.type="button",q.className="udzbenik-dugme udzbenik-dugme--malo udzbenik-dugme--preklopnik",q.setAttribute("role","switch"),q.setAttribute("aria-checked","false"),q.textContent=Ge("apsolutnaTvrdocaPreklopnik"),q.addEventListener("click",()=>{a=!a,q?.setAttribute("aria-checked",String(a)),q?.classList.toggle("udzbenik-dugme--aktivno",a),n.smanjenPokret&&(s=a?1:0,ne()),ae(),n.zatraziRender()}),z.append(q)),k.append(z),n.gornjeKontrole.append(k);const J=document.createElement("p");J.className="udzbenik-scena-info-red",J.setAttribute("aria-live","polite");const fe=document.createElement("p");fe.className="udzbenik-scena-izvor",fe.textContent=`${Ge("izvorPodataka")}: ${Yt}`,n.podnozje.append(J,fe);function Ae(Y){Y===o?c=Y<9?Y+1:Y-1:(o=Y,c=Y>0?Y-1:1),l=n.smanjenPokret?.75:0,ae(),n.zatraziRender()}function K(Y,re){const oe=Y.mohs/10*g,I=Math.max(.08,Y.apsolutnaKnoop/7e3*g);return oe+(I-oe)*re}function ne(){for(let Y=0;Y<u.length;Y++){const re=u[Y],oe=K(re.mineral,s);re.mesh.scale.y=oe,re.mesh.position.y=m+oe*.5,re.ivice.scale.y=oe,re.ivice.position.copy(re.mesh.position);const I=Y===o,Ie=Y===c,Pe=I?"--accent":Ie?"--warning":re.istaknut?"--accent":"--primary",Ce=new ce(n.tema.token(Pe));!I&&!Ie&&!re.istaknut&&Ce.lerp(new ce(n.tema.token("--bg-elevated")),.25),re.mat.color.copy(Ce),re.etiketaDom.textContent=a?`${re.mineral.mohs} (${re.mineral.apsolutnaKnoop})`:`${re.mineral.mohs}`}}function ue(){const Y=An[o],re=An[c],oe=Y.mohs>re.mohs,I=Math.min(1,l/.75),Ie=-1.15,Ce=Ie+(1.15-Ie)*I;if(D.position.x=Ce,D.position.y=oe?.44:.5,oe&&I>.03){const Me=Math.max(.05,Ce-Ie);U.visible=!0,U.scale.x=Me,U.position.x=Ie+Me*.5}else U.visible=!1}function ae(){for(let Ie=0;Ie<O.length;Ie++){const Pe=O[Ie],Ce=Ie===o;Pe.classList.toggle("udzbenik-mohs-cip--aktivan",Ce),Pe.setAttribute("aria-pressed",String(Ce))}const Y=An[o],re=An[c],I=Y.mohs>re.mohs?`${Ge("probaGrebanja")}: ${Y.naziv} (${Y.mohs}, HK ${Y.apsolutnaKnoop}) је тврђи и оставља бразду на минералу ${re.naziv} (${re.mohs}, HK ${re.apsolutnaKnoop}).`:`${Ge("probaGrebanja")}: ${Y.naziv} (${Y.mohs}, HK ${Y.apsolutnaKnoop}) је мекши и НЕ оставља бразду на минералу ${re.naziv} (${re.mohs}, HK ${re.apsolutnaKnoop}).`;J.textContent=I,ne(),ue()}const ee=new js,_e=new Ke,de=Y=>{const re=n.platno.getBoundingClientRect();if(re.width<=0||re.height<=0)return;_e.x=(Y.clientX-re.left)/re.width*2-1,_e.y=-((Y.clientY-re.top)/re.height)*2+1,ee.setFromCamera(_e,n.kamera);const oe=ee.intersectObjects(u.map(I=>I.mesh),!1);if(oe.length>0){const I=oe[0].object,Ie=u.findIndex(Pe=>Pe.mesh===I);Ie!==-1&&Ae(Ie)}};return n.platno.addEventListener("click",de),ae(),{azuriraj(Y){const re=a?1:0;Math.abs(s-re)>.002?(s+=(re-s)*Math.min(1,Y*6),ne()):s!==re&&(s=re,ne()),l=(l+Y*.42)%1,ue()},korak(){l=(l+.2)%1,s=a?1:0,ne(),ue()},resetuj(){a=!1,s=0,q&&(q.setAttribute("aria-checked","false"),q.classList.remove("udzbenik-dugme--aktivno")),o=6,c=5,l=n.smanjenPokret?.75:0,ae()},osveziTemu(Y){_.color.set(Y.token("--bg-elevated")),b.color.set(Y.token("--text-primary")),w.color.set(Y.token("--warning")),L.color.set(Y.token("--primary-light")),R.color.set(Y.token("--danger")),C.color.set(Y.token("--accent")),ne()},posleRendera(){d.updateMatrixWorld(!0);for(const Y of u){const re=Y.mesh.position.clone().add(new F(0,Y.mesh.scale.y*.5+.22,0)).applyMatrix4(d.matrixWorld),oe=n.projektujU2D(re);Y.etiketaDom.hidden=!oe.vidljivo,oe.vidljivo&&(Y.etiketaDom.style.transform=`translate(-50%, -50%) translate(${oe.x.toFixed(1)}px, ${oe.y.toFixed(1)}px)`)}for(const Y of T){const re=new F(Y.x,m-.22,.35).applyMatrix4(d.matrixWorld),oe=n.projektujU2D(re);Y.dom.hidden=!oe.vidljivo,oe.vidljivo&&(Y.dom.style.transform=`translate(-50%, 0%) translate(${oe.x.toFixed(1)}px, ${oe.y.toFixed(1)}px)`)}},raspolazi(){n.platno.removeEventListener("click",de),It(d),S.dispose(),M.dispose(),_.dispose(),b.dispose(),w.dispose(),L.dispose(),R.dispose(),C.dispose();for(const Y of u)Y.mat.dispose()}}}};function pc(n,e,t){const i=Math.hypot(...t),r=i>0?t[0]/i:0,a=i>0?t[1]/i:0,s=i>0?t[2]/i:1;if(n==="izotropna"){const v=e[0]??1.5;return{n1:v,n2:v,delta:0}}if(n==="jednoosna"){const v=e[0]??1.544,R=e[1]??1.553,U=s*s,C=Math.max(0,1-U),D=U/(v*v)+C/(R*R),k=Math.sqrt(1/Math.max(1e-12,D)),N=Math.abs(k-v);return{n1:Math.min(v,k),n2:Math.max(v,k),delta:N}}const o=e[0]??1.52,c=e[1]??1.53,l=e[2]??1.55,d=1/(o*o),h=1/(c*c),f=1/(l*l);let m=0;if(Math.abs(h-f)>1e-7&&d>=h&&h>=f){const v=(d-h)/(h-f);m=2*Math.atan(Math.sqrt(Math.max(0,v)))*180/Math.PI}const g=r*r,_=a*a,p=s*s,u=1,b=-(g*(h+f)+_*(d+f)+p*(d+h)),S=g*h*f+_*d*f+p*d*h,M=Math.max(0,b*b-4*u*S),w=(-b-Math.sqrt(M))/(2*u),T=(-b+Math.sqrt(M))/(2*u),A=Math.sqrt(1/Math.max(1e-12,T)),L=Math.sqrt(1/Math.max(1e-12,w)),x=Math.abs(L-A);return{n1:A,n2:L,delta:x,ugao2V:m}}const p0={imaPodrazumevanuAnimaciju(){return!0},pocetnaKamera(){return{theta:.72,phi:1.18,udaljenost:5.6}},kreiraj(n,e){const t=new it;n.scena3D.add(t);const i=e.tip,r=e.n&&e.n.length>0?e.n:i==="izotropna"?[1.5]:i==="jednoosna"?[1.658,1.486]:[1.52,1.53,1.55];let a=1.6,s=1.6,o=1.6;if(i==="jednoosna"){const U=r[0],C=r[1]??r[0];a=1.6,s=1.6,o=1.6*(C>=U?1.35:.72)}else i==="dvoosna"&&(a=1.25,s=1.65,o=2.15);const c=new xn(1,48,36);c.scale(a,s,o);const l=new ot({color:new ce(n.tema.token("--primary")),transparent:!0,opacity:.42,roughness:.25,metalness:.1,side:St}),d=new We(c,l);t.add(d);const h=new ht({color:new ce(n.tema.token("--text-secondary"))}),f=new Ze,m=[-a*1.3,0,0,a*1.3,0,0,0,-s*1.3,0,0,s*1.3,0,0,0,-o*1.3,0,0,o*1.3];f.setAttribute("position",new He(m,3)),t.add(new gt(f,h));const g=new ht({color:new ce(n.tema.token("--accent")),linewidth:3});if(e.prikazi_opticke_ose!==!1){const U=[];if(i==="jednoosna")U.push(0,0,-o*1.45,0,0,o*1.45);else if(i==="dvoosna"){const D=(pc(i,r,[0,0,1]).ugao2V??50)/2*(Math.PI/180),k=o*1.4,N=k*Math.sin(D),O=k*Math.cos(D);U.push(-N,0,-O,N,0,O),U.push(N,0,-O,-N,0,O)}if(U.length>0){const C=new Ze;C.setAttribute("position",new He(U,3)),t.add(new gt(C,g))}}const _=new it;t.add(_);const p=new Ui({color:new ce(n.tema.token("--warning")),transparent:!0,opacity:.35,side:St}),u=new Bs(0,2.2,48),b=new We(u,p);_.add(b);const S=new ht({color:new ce(n.tema.token("--danger"))}),M=new Ze;M.setAttribute("position",new He([0,0,-2.6,0,0,2.6],3)),_.add(new gt(M,S));const w=document.createElement("div");w.className="udzbenik-scena-status",n.podnozje.append(w);const T=document.createElement("small");T.className="udzbenik-scena-napomena",T.style.display="block",T.textContent="Напомена: Разлике индекса преламања су преувеличане ради јаснијег 3D приказа.",n.podnozje.append(T);let A=.5,L=.3;function x(){_.rotation.set(A,L,0);const U=new F(0,0,1).applyEuler(_.rotation),C=pc(i,r,[U.x,U.y,U.z]),D=C.delta.toFixed(4),k=e.mineral?` (${e.mineral})`:"",N=C.ugao2V?` • 2V = ${C.ugao2V.toFixed(1)}°`:"";w.textContent=`Тип: ${i}${k} • n'₁ = ${C.n1.toFixed(3)}, n'₂ = ${C.n2.toFixed(3)} • δ = ${D}${N}`}x();function v(){l.color.set(n.tema.token("--primary")),h.color.set(n.tema.token("--text-secondary")),g.color.set(n.tema.token("--accent")),p.color.set(n.tema.token("--warning")),S.color.set(n.tema.token("--danger"))}let R=0;return{azuriraj(U){R+=U*.35,L=Math.sin(R)*1.1,A=Math.cos(R*.7)*.7,x()},korak(){R+=.25,L+=.2,x()},resetuj(){R=0,A=.5,L=.3,x()},osveziTemu(){v()},raspolazi(){c.dispose(),l.dispose(),f.dispose(),h.dispose(),g.dispose(),u.dispose(),p.dispose(),M.dispose(),S.dispose(),It(t),w.remove(),T.remove()}}}},La={nezo:{klasa:"nezo",naziv:"Незосиликати (изоловани tetraedri)",odnosSiO:"1 : 4 (SiO₄⁴⁻)",zajednickiKiseonici:"0",primeri:"оливин, гранат, циркон"},soro:{klasa:"soro",naziv:"Соросиликати (парови tetraedara)",odnosSiO:"2 : 7 (Si₂O₇⁶⁻)",zajednickiKiseonici:"1",primeri:"епидот, хемиморфит"},"ciklo-3":{klasa:"ciklo-3",naziv:"Циклосиликати (трочлани прстен)",odnosSiO:"1 : 3 (Si₃O₉⁶⁻)",zajednickiKiseonici:"2",primeri:"бенитоит"},"ciklo-6":{klasa:"ciklo-6",naziv:"Циклосиликати (шесточлани прстен)",odnosSiO:"1 : 3 (Si₆O₁₈¹²⁻)",zajednickiKiseonici:"2",primeri:"берил, турмалин"},"ino-jednostruki":{klasa:"ino-jednostruki",naziv:"Иносиликати (једноструки ланци)",odnosSiO:"1 : 3 (Si₂O₆⁴⁻)",zajednickiKiseonici:"2",primeri:"пироксени (диопсид, енстатит)"},"ino-dvostruki":{klasa:"ino-dvostruki",naziv:"Иносиликати (двоструки ланци)",odnosSiO:"4 : 11 (Si₄O₁₁⁶⁻)",zajednickiKiseonici:"2 и 3 (просек 2,5)",primeri:"амфиболи (тремолит, хорнбленда)"},filo:{klasa:"filo",naziv:"Филосиликати (слојевити)",odnosSiO:"2 : 5 (Si₄O₁₀⁴⁻)",zajednickiKiseonici:"3",primeri:"лискуни (мусковит, биотит), талк, каолинит"},tekto:{klasa:"tekto",naziv:"Тектосиликати (просторна мрежа)",odnosSiO:"1 : 2 (SiO₂)",zajednickiKiseonici:"4",primeri:"кварц, фелдспати, зеолити"},sve:{klasa:"sve",naziv:"Преглед свих класа",odnosSiO:"од 1:4 до 1:2",zajednickiKiseonici:"0 до 4",primeri:"полимеризација од незо- до тектосиликата"}};function Qt(n,e,t,i,r,a){const s=new it;s.position.copy(n),s.rotation.copy(e);const o=.55,c=[[o,o,o],[o,-o,-o],[-o,o,-o],[-o,-o,o]];if(a==="tetraedri"||a==="oba"){const l=new Ze,d=[...c[0],...c[1],...c[2],...c[0],...c[3],...c[1],...c[0],...c[2],...c[3],...c[1],...c[3],...c[2]];l.setAttribute("position",new He(d,3)),l.computeVertexNormals();const h=new We(l,t);s.add(h)}if(a==="kugle"||a==="oba")for(const l of c){const d=new We(r,i);d.position.set(l[0],l[1],l[2]),s.add(d)}return s}const m0={imaPodrazumevanuAnimaciju(n){return(n.animacija??"rotacija")!=="nema"},pocetnaKamera(){return{theta:.65,phi:1.15,udaljenost:6.2}},kreiraj(n,e){let t=e.klasa==="sve"?"nezo":e.klasa;const i=e.prikaz??"tetraedri",r=new it;n.scena3D.add(r);const a=new xn(.18,16,16),s=new ot({color:new ce(n.tema.token("--primary")),transparent:!0,opacity:.65,roughness:.25,metalness:.1,side:St}),o=new ot({color:new ce(n.tema.token("--accent")),roughness:.25,metalness:.2}),c=document.createElement("div");c.className="udzbenik-scena-status",n.podnozje.append(c);function l(_){for(;r.children.length>0;){const u=r.children[0];r.remove(u),It(u)}const p=La[_]??La.nezo;if(c.textContent=`${p.naziv} • Si:O = ${p.odnosSiO} • Заједнички O: ${p.zajednickiKiseonici} (${p.primeri})`,_==="nezo")r.add(Qt(new F(0,0,0),new mt(0,0,0),s,o,a,i));else if(_==="soro")r.add(Qt(new F(-.55,0,0),new mt(0,0,0),s,o,a,i)),r.add(Qt(new F(.55,0,0),new mt(0,Math.PI,0),s,o,a,i));else if(_==="ciklo-3")for(let u=0;u<3;u++){const b=u*2*Math.PI/3,S=new F(Math.cos(b)*.95,Math.sin(b)*.95,0);r.add(Qt(S,new mt(0,0,b),s,o,a,i))}else if(_==="ciklo-6")for(let u=0;u<6;u++){const b=u*2*Math.PI/6,S=new F(Math.cos(b)*1.5,Math.sin(b)*1.5,0);r.add(Qt(S,new mt(0,0,b),s,o,a,i))}else if(_==="ino-jednostruki")for(let u=-2;u<=2;u++){const b=u%2===0?0:Math.PI;r.add(Qt(new F(u*.9,u%2*.2,0),new mt(0,0,b),s,o,a,i))}else if(_==="ino-dvostruki")for(let u=-2;u<=2;u++){const b=u%2===0?0:Math.PI;r.add(Qt(new F(u*.9,.45+u%2*.15,0),new mt(0,0,b),s,o,a,i)),r.add(Qt(new F(u*.9,-.45-u%2*.15,0),new mt(0,0,b+Math.PI),s,o,a,i))}else if(_==="filo")for(let u=-1;u<=1;u++)for(let b=-1;b<=1;b++){const S=u*1.4+b%2*.7,M=b*1.2;r.add(Qt(new F(S,M,0),new mt(0,0,0),s,o,a,i))}else for(const u of[-.7,.7])for(const b of[-.7,.7])for(const S of[-.7,.7])r.add(Qt(new F(u,b,S),new mt(u,b,S),s,o,a,i))}if(e.klasa==="sve"){const _=document.createElement("div");_.className="udzbenik-silikati-traka",_.style.display="flex",_.style.flexWrap="wrap",_.style.gap="4px";const p=["nezo","soro","ciklo-3","ciklo-6","ino-jednostruki","ino-dvostruki","filo","tekto"];for(const u of p){const b=La[u],S=document.createElement("button");S.type="button",S.className="udzbenik-dugme udzbenik-dugme--malo",u===t&&S.classList.add("udzbenik-dugme--aktivno"),S.textContent=u,S.setAttribute("aria-label",b.naziv),S.addEventListener("click",()=>{t=u,_.querySelectorAll("button").forEach(M=>M.classList.remove("udzbenik-dugme--aktivno")),S.classList.add("udzbenik-dugme--aktivno"),l(u)}),_.append(S)}n.gornjeKontrole.append(_)}l(t);let d=0;const h=(e.animacija??(e.klasa==="sve"?"polimerizacija":"rotacija"))==="polimerizacija",f=["nezo","soro","ciklo-6","ino-jednostruki","ino-dvostruki","filo","tekto"];let m=0;function g(){s.color.set(n.tema.token("--primary")),o.color.set(n.tema.token("--accent"))}return{azuriraj(_){if(d+=_,r.rotation.y=d*.35,h){const p=Math.floor(d/3)%f.length;if(p!==m){m=p;const u=f[m];l(u)}}},korak(){d+=.3,r.rotation.y+=.2,h&&(m=(m+1)%f.length,l(f[m]))},resetuj(){d=0,r.rotation.set(0,0,0),m=0,l(t)},osveziTemu(){g()},raspolazi(){a.dispose(),s.dispose(),o.dispose(),It(r),c.remove()}}}},g0={"kristalni-sistem":d0,"kristalna-struktura":o0,"mohsova-skala":f0,cepljivost:jm,habitus:a0,"bravaisova-resetka":Um,"opticka-indikatrisa":p0,blizanac:Dm,"koordinacioni-poliedar":s0,"silikatna-struktura":m0};function _0(n,e,t){const i=g0[n.scena];return i?Cm(i,n.parametri,e,t):(e.prikaziRezervu("Сцена није подржана у овој верзији мотора."),()=>{})}const E0=Object.freeze(Object.defineProperty({__proto__:null,pokreniScenuPoImenu:_0,raspolaziDeljenimRendererom:Rm},Symbol.toStringTag,{value:"Module"}));export{At as A,S0 as G,ys as J,qr as a,v0 as b,M0 as c,E0 as d,x0 as p,Ge as t};
