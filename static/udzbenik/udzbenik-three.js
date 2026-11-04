const hl={ucitavanjeUdzbenika:"Учитавање уџбеника…",ucitavanjeLekcije:"Учитавање лекције…",ucitavanjeScene:"Учитавање 3D приказа…",greskaUcitavanja:"Грешка при учитавању — покушај поново",pokusajPonovo:"Покушај поново",nemaSecureFetch:"Безбедно слање (secureFetch) није доступно на овој страници.",greskaCuvanjaNapretka:"Чување напретка није успело.",sadrzajDugme:"Садржај уџбеника",navigacijaAria:"Поглавља и лекције",napredakOznaka:"Завршено лекција",zavrsenaLekcijaOznaka:"Завршено",nezavrsenaLekcijaOznaka:"Није завршено",zavrsiLekciju:"Заврши лекцију",cuvanjeNapretka:"Чување…",lekcijaZavrsenaPoruka:"Лекција је означена као завршена.",sacuvajPonovo:"Сачувај напредак поново",prethodnaLekcija:"Претходна лекција",sledecaLekcija:"Следећа лекција",navigacijaLekcijeAria:"Навигација између лекција",tabelaAria:"Табела података",porekloFotografija:"Фотографија",porekloCrtez:"Цртеж",porekloAiIlustracija:"АИ илустрација",porekloDijagram:"Дијаграм",autorOznaka:"Аутор",primerakNedostupan:"Примерак тренутно није доступан",primerakNedostupanPodrazumevano:"Подаци о примерку се не могу приказати.",inventarniBroj:"Инв. бр.",lokalitet:"Локалитет",otvoriKarticuPrimerka:"Отвори картицу примерка у МИС-у",napomenaInfo:"Напомена",napomenaPazi:"Пажња",napomenaZanimljivost:"Занимљивост",proveriOdgovor:"Провери одговор",izaberiOdgovorUpozorenje:"Изаберите бар један одговор пре провере.",odgovorTacan:"Тачно!",odgovorNetacan:"Није тачно — погледајте објашњење.",oznakaTacnogOdgovora:"тачан одговор",oznakaViseTacnih:"Могуће је више тачних одговора.",kvizRezime:"Квиз у лекцији",scenaResetuj:"Ресетуј",scenaResetujAria:"Ресетуј камеру и стање сцене",scenaPauza:"Пауза",scenaPauzaAria:"Паузирај анимацију сцене",scenaNastavi:"Настави",scenaNastaviAria:"Настави анимацију сцене",scenaKorak:"Корак",scenaKorakAria:"Помери анимацију за један корак",scenaPrikaziObjasnjenje:"Прикажи објашњење",scenaSakrijObjasnjenje:"Сакриј објашњење",scenaObjasnjenjeAria:"Прикажи текстуално објашњење сцене",scenaZumPlusAria:"Увећај приказ",scenaZumMinusAria:"Умањи приказ",scenaDodirSavet:"Додирните приказ за ротацију једним прстом (или ротирајте са два прста)",scenaDodirAktivan:"3D ротација активна — заврши за скрол стране",scenaRezervaOznaka:"Статични приказ (3D WebGL није доступан)",strukturaNedostupna:"Структура није доступна за овај минерал",legendaElemenata:"Легенда хемијских елемената (CPK боје и полупречници)",poluprecniciJonskiOznaka:"Полупречници сфера: јонски",poluprecniciKovalentniOznaka:"Полупречници сфера: ковалентни",kovalentnaRezervaOznaka:"ковалентни за елементе ван јонске табеле",detekcijaVezaKovalentniOznaka:"детекција веза: ковалентни ×",faktorVeza:"Праг дужине веза",sledeciAtom:"Следећи атом",atomKoordinate:"Фракционе координате",izaberiKristalniSistem:"Кристални системи",apsolutnaTvrdocaPreklopnik:"Апсолутна тврдоћа (Knoop)",ordinalnaTvrdocaOznaka:"Мосова ординална скала (1–10)",terenskeProbeOznaka:"Теренске пробе",probaGrebanja:"Проба гребања",zameniMinerale:"Обрни смер гребања",izvorPodataka:"Извор",brojPravacaCepljivosti:"Број праваца",ugloviCepljivosti:"Углови",primerMinerala:"Пример",prelazFormi:"Однос форми (прелаз хабитуса)",aktivnaForma:"Кристална форма",izNaucneBiblioteke:"Из научне библиотеке",literaturaNedostupnaNaslov:"Научна библиотека тренутно није доступна",literaturaNedostupnaPodrazumevano:"Подаци из библиотеке се не могу приказати.",literaturaPrijavaNapomena:"За читање потребна је пријава у SciSearch.",stranaSkraceno:"стр.",literaturaNemaRezultata:"Нема пронађених резултата у научној библиотеци.",poglavljeOznaka:"Поглавље"},fl={А:"A",Б:"B",В:"V",Г:"G",Д:"D",Ђ:"Đ",Е:"E",Ж:"Ž",З:"Z",И:"I",Ј:"J",К:"K",Л:"L",Љ:"Lj",М:"M",Н:"N",Њ:"Nj",О:"O",П:"P",Р:"R",С:"S",Т:"T",Ћ:"Ć",У:"U",Ф:"F",Х:"H",Ц:"C",Ч:"Č",Џ:"Dž",Ш:"Š",а:"a",б:"b",в:"v",г:"g",д:"d",ђ:"đ",е:"e",ж:"ž",з:"z",и:"i",ј:"j",к:"k",л:"l",љ:"lj",м:"m",н:"n",њ:"nj",о:"o",п:"p",р:"r",с:"s",т:"t",ћ:"ć",у:"u",ф:"f",х:"h",ц:"c",ч:"č",џ:"dž",ш:"š"};function pl(n){let e="";for(const t of n)e+=fl[t]??t;return e}let Ec="cyrl";function R0(n){Ec=n}function We(n){const e=hl[n];return Ec==="latn"?pl(e):e}class wt extends Error{status;constructor(e,t=0){super(e),this.name="ApiGreska",this.status=t}}function ml(n,e){const t=n.replace(/\/+$/,""),i=`/${e}`;if(e&&t.endsWith(i))return t.slice(0,t.length-i.length)||"/api/udzbenik";const a=t.lastIndexOf("/");return a>0?t.slice(0,a):t}function C0(n){const e=(n.dataset.api??"").trim(),t=(n.dataset.zbirka??"minerali").trim();if(!e)throw new wt("Недостаје обавезан атрибут data-api на #udzbenik-app.");const i=(n.dataset.apiKoren??"").trim()||ml(e,t),r=(n.dataset.pismo??"cyrl").trim().toLowerCase()==="latn"?"latn":"cyrl";return{api:e.replace(/\/+$/,""),apiKoren:i.replace(/\/+$/,""),zbirka:t,pocetnoPoglavlje:(n.dataset.poglavlje??"").trim(),pocetnaLekcija:(n.dataset.lekcija??"").trim(),pismo:r,mozeUredjuje:n.dataset.mozeUredjuje==="true"}}async function $a(n,e){try{const t=await n.text();if(!t)return e;const i=JSON.parse(t);if(typeof i.greska=="string"&&i.greska.trim())return i.greska.trim()}catch{}return e}class P0{konfig;kesStruktura=new Map;constructor(e){this.konfig=e}get konfiguracija(){return this.konfig}ocistiKes(){this.kesStruktura.clear()}async ucitajUdzbenik(){let e;try{e=await fetch(this.konfig.api,{method:"GET",headers:{Accept:"application/json"}})}catch{throw new wt(We("greskaUcitavanja"),0)}if(!e.ok){const t=await $a(e,We("greskaUcitavanja"));throw new wt(t,e.status)}try{return await e.json()}catch{throw new wt(We("greskaUcitavanja"),e.status)}}async ucitajLekciju(e,t){const i=`${this.konfig.api}/lekcija/${encodeURIComponent(e)}/${encodeURIComponent(t)}`;let a;try{a=await fetch(i,{method:"GET",headers:{Accept:"application/json"}})}catch{throw new wt(We("greskaUcitavanja"),0)}if(!a.ok){const r=await $a(a,We("greskaUcitavanja"));throw new wt(r,a.status)}try{return await a.json()}catch{throw new wt(We("greskaUcitavanja"),a.status)}}async posaljiNapredak(e){if(typeof window>"u"||typeof window.secureFetch!="function")throw new wt(We("nemaSecureFetch"),0);const t=`${this.konfig.apiKoren}/napredak`;let i;try{i=await window.secureFetch(t,{method:"POST",headers:{"Content-Type":"application/json",Accept:"application/json"},body:JSON.stringify(e)})}catch{throw new wt(We("greskaCuvanjaNapretka"),0)}let a=null;try{a=await i.json()}catch{a=null}if(!i.ok||!a?.ok){const r=typeof a?.greska=="string"&&a.greska.trim()?a.greska.trim():We("greskaCuvanjaNapretka");throw new wt(r,i.status)}return a}async ucitajStrukturuCif(e){const t=e.trim().toLowerCase(),i=this.kesStruktura.get(t);if(i)return i;const a=`${this.konfig.apiKoren}/struktura/${encodeURIComponent(e.trim())}`,r=(async()=>{let s;try{s=await fetch(a,{method:"GET",headers:{Accept:"text/plain, */*"}})}catch{throw this.kesStruktura.delete(t),new wt(We("greskaUcitavanja"),0)}if(s.status===404)throw new wt(We("strukturaNedostupna"),404);if(!s.ok){this.kesStruktura.delete(t);const o=await $a(s,We("greskaUcitavanja"));throw new wt(o,s.status)}return s.text()})();return r.catch(s=>{s instanceof wt&&s.status===404||this.kesStruktura.delete(t)}),this.kesStruktura.set(t,r),r}}const gl=["--bg-body","--bg-card","--bg-elevated","--bg-hover","--text-primary","--text-secondary","--text-muted","--primary","--primary-light","--primary-dark","--accent","--accent-light","--accent-strong","--on-accent","--border-color","--border-strong","--focus-ring","--success","--success-soft","--warning","--warning-soft","--danger","--danger-soft","--info","--info-soft","--font-family","--font-display","--font-size-sm","--font-size-base","--font-size-lg","--lh-base","--radius-sm","--radius-md","--radius-card","--radius-btn","--shadow-sm","--shadow-card","--space-1","--space-2","--space-3","--space-4","--space-6","--space-8","--transition-fast","--transition-base"],bc={"--font-family":'system-ui, -apple-system, "Segoe UI", Roboto, sans-serif',"--font-display":'system-ui, -apple-system, "Segoe UI", Roboto, sans-serif',"--font-size-sm":"0.875rem","--font-size-base":"1rem","--font-size-lg":"1.25rem","--lh-base":"1.6","--radius-sm":"4px","--radius-md":"8px","--radius-card":"12px","--radius-btn":"8px","--space-1":"0.25rem","--space-2":"0.5rem","--space-3":"0.75rem","--space-4":"1rem","--space-6":"1.5rem","--space-8":"2rem","--transition-fast":"150ms ease","--transition-base":"240ms ease"},to={...bc,"--bg-body":"#f5f6f8","--bg-card":"#ffffff","--bg-elevated":"#eef1f5","--bg-hover":"#e3e8ef","--text-primary":"#161b22","--text-secondary":"#424d5c","--text-muted":"#596577","--primary":"#1b5e4a","--primary-light":"#e4f2ed","--primary-dark":"#124234","--accent":"#0f5c8c","--accent-light":"#e3f0f9","--accent-strong":"#0a4368","--on-accent":"#ffffff","--border-color":"#768396","--border-strong":"#4f5b6b","--focus-ring":"#0f5c8c","--success":"#166534","--success-soft":"#e6f5ec","--warning":"#854d0e","--warning-soft":"#fef3db","--danger":"#991b1b","--danger-soft":"#fdeaea","--info":"#1e4e8c","--info-soft":"#e8f0fb","--shadow-sm":"0 1px 2px rgba(15, 20, 26, 0.08)","--shadow-card":"0 2px 8px rgba(15, 20, 26, 0.10)"},no={...bc,"--bg-body":"#0f141a","--bg-card":"#18202a","--bg-elevated":"#212b38","--bg-hover":"#2b3848","--text-primary":"#f0f4f8","--text-secondary":"#c2cdd9","--text-muted":"#9aa8b8","--primary":"#56c7a3","--primary-light":"#1c3b33","--primary-dark":"#7adbb9","--accent":"#63b3ed","--accent-light":"#1b3247","--accent-strong":"#90cdf4","--on-accent":"#0f141a","--border-color":"#68788c","--border-strong":"#8fa0b5","--focus-ring":"#63b3ed","--success":"#5fd38d","--success-soft":"#163324","--warning":"#f6c453","--warning-soft":"#362a12","--danger":"#f88080","--danger-soft":"#3b1c20","--info":"#76b9f5","--info-soft":"#192e45","--shadow-sm":"0 1px 3px rgba(0, 0, 0, 0.35)","--shadow-card":"0 4px 12px rgba(0, 0, 0, 0.45)"},_l=["data-theme","data-palette","data-accent","data-style","data-density","data-bs-theme"];function vl(n=document.documentElement){const e=(n.getAttribute("data-theme")??"").toLowerCase(),t=(n.getAttribute("data-bs-theme")??"").toLowerCase();return e==="dark"||t==="dark"?!0:e==="light"||t==="light"?!1:typeof window<"u"&&typeof window.matchMedia=="function"?window.matchMedia("(prefers-color-scheme: dark)").matches:!1}class xl{slusaoci=new Set;posmatrac=null;medijaUpit=null;medijaSlusalac=null;kesiraniTokeni=new Map;ciljniKontejner=null;povezi(e){this.ciljniKontejner=e??null,this.osvezi(),typeof MutationObserver<"u"&&typeof document<"u"&&(this.posmatrac?.disconnect(),this.posmatrac=new MutationObserver(()=>{this.osvezi()}),this.posmatrac.observe(document.documentElement,{attributes:!0,attributeFilter:_l})),typeof window<"u"&&typeof window.matchMedia=="function"&&(this.medijaUpit=window.matchMedia("(prefers-color-scheme: dark)"),this.medijaSlusalac=()=>this.osvezi(),this.medijaUpit.addEventListener("change",this.medijaSlusalac))}odspoji(){this.posmatrac?.disconnect(),this.posmatrac=null,this.medijaUpit&&this.medijaSlusalac&&this.medijaUpit.removeEventListener("change",this.medijaSlusalac),this.medijaUpit=null,this.medijaSlusalac=null,this.slusaoci.clear()}pretplati(e){return this.slusaoci.add(e),()=>{this.slusaoci.delete(e)}}jeTamna(){return typeof document>"u"?!1:vl(document.documentElement)}osvezi(){this.kesiraniTokeni.clear();const t=this.jeTamna()?no:to,i=typeof window<"u"&&typeof document<"u"?window.getComputedStyle(document.documentElement):null;for(const a of gl){const r=i?i.getPropertyValue(a).trim():"",s=r||t[a];this.kesiraniTokeni.set(a,s),this.ciljniKontejner&&(r?this.ciljniKontejner.style.removeProperty(a):this.ciljniKontejner.style.setProperty(a,t[a]))}for(const a of this.slusaoci)a(this)}token(e){const t=this.kesiraniTokeni.get(e);if(t)return t;const i=this.jeTamna()?no:to;if(typeof window<"u"&&typeof document<"u"){const a=window.getComputedStyle(document.documentElement).getPropertyValue(e).trim();if(a)return a}return i[e]}}const Ya=new xl;/**
 * @license
 * Copyright 2010-2025 Three.js Authors
 * SPDX-License-Identifier: MIT
 */const Ps="174",Ml=0,io=1,Sl=2,yc=1,El=2,dn=3,Ln=0,Lt=1,mt=2,In=0,Ei=1,ao=2,ro=3,so=4,bl=5,qn=100,yl=101,Tl=102,Al=103,wl=104,Rl=200,Cl=201,Pl=202,Il=203,zr=204,kr=205,Dl=206,Ll=207,Ul=208,zl=209,kl=210,Nl=211,Fl=212,Ol=213,Bl=214,Nr=0,Fr=1,Or=2,Ti=3,Br=4,Vr=5,jr=6,Hr=7,Tc=0,Vl=1,jl=2,Dn=0,Hl=1,Gl=2,Wl=3,Xl=4,Kl=5,ql=6,$l=7,Ac=300,Ai=301,wi=302,Gr=303,Wr=304,Ga=306,Xr=1e3,Yn=1001,Kr=1002,Jt=1003,Yl=1004,ia=1005,en=1006,Za=1007,Zn=1008,_n=1009,wc=1010,Rc=1011,Ki=1012,Is=1013,ei=1014,fn=1015,Yi=1016,Ds=1017,Ls=1018,Ri=1020,Cc=35902,Pc=1021,Ic=1022,Zt=1023,Dc=1024,Lc=1025,bi=1026,Ci=1027,Uc=1028,Us=1029,zc=1030,zs=1031,ks=1033,Pa=33776,Ia=33777,Da=33778,La=33779,qr=35840,$r=35841,Yr=35842,Zr=35843,Jr=36196,Qr=37492,es=37496,ts=37808,ns=37809,is=37810,as=37811,rs=37812,ss=37813,os=37814,cs=37815,ls=37816,us=37817,ds=37818,hs=37819,fs=37820,ps=37821,Ua=36492,ms=36494,gs=36495,kc=36283,_s=36284,vs=36285,xs=36286,Zl=3200,Jl=3201,Nc=0,Ql=1,Cn="",Ft="srgb",Pi="srgb-linear",Fa="linear",at="srgb",ii=7680,oo=519,eu=512,tu=513,nu=514,Fc=515,iu=516,au=517,ru=518,su=519,co=35044,lo="300 es",pn=2e3,Oa=2001;class Di{addEventListener(e,t){this._listeners===void 0&&(this._listeners={});const i=this._listeners;i[e]===void 0&&(i[e]=[]),i[e].indexOf(t)===-1&&i[e].push(t)}hasEventListener(e,t){const i=this._listeners;return i===void 0?!1:i[e]!==void 0&&i[e].indexOf(t)!==-1}removeEventListener(e,t){const i=this._listeners;if(i===void 0)return;const a=i[e];if(a!==void 0){const r=a.indexOf(t);r!==-1&&a.splice(r,1)}}dispatchEvent(e){const t=this._listeners;if(t===void 0)return;const i=t[e.type];if(i!==void 0){e.target=this;const a=i.slice(0);for(let r=0,s=a.length;r<s;r++)a[r].call(this,e);e.target=null}}}const yt=["00","01","02","03","04","05","06","07","08","09","0a","0b","0c","0d","0e","0f","10","11","12","13","14","15","16","17","18","19","1a","1b","1c","1d","1e","1f","20","21","22","23","24","25","26","27","28","29","2a","2b","2c","2d","2e","2f","30","31","32","33","34","35","36","37","38","39","3a","3b","3c","3d","3e","3f","40","41","42","43","44","45","46","47","48","49","4a","4b","4c","4d","4e","4f","50","51","52","53","54","55","56","57","58","59","5a","5b","5c","5d","5e","5f","60","61","62","63","64","65","66","67","68","69","6a","6b","6c","6d","6e","6f","70","71","72","73","74","75","76","77","78","79","7a","7b","7c","7d","7e","7f","80","81","82","83","84","85","86","87","88","89","8a","8b","8c","8d","8e","8f","90","91","92","93","94","95","96","97","98","99","9a","9b","9c","9d","9e","9f","a0","a1","a2","a3","a4","a5","a6","a7","a8","a9","aa","ab","ac","ad","ae","af","b0","b1","b2","b3","b4","b5","b6","b7","b8","b9","ba","bb","bc","bd","be","bf","c0","c1","c2","c3","c4","c5","c6","c7","c8","c9","ca","cb","cc","cd","ce","cf","d0","d1","d2","d3","d4","d5","d6","d7","d8","d9","da","db","dc","dd","de","df","e0","e1","e2","e3","e4","e5","e6","e7","e8","e9","ea","eb","ec","ed","ee","ef","f0","f1","f2","f3","f4","f5","f6","f7","f8","f9","fa","fb","fc","fd","fe","ff"],za=Math.PI/180,Ms=180/Math.PI;function Zi(){const n=Math.random()*4294967295|0,e=Math.random()*4294967295|0,t=Math.random()*4294967295|0,i=Math.random()*4294967295|0;return(yt[n&255]+yt[n>>8&255]+yt[n>>16&255]+yt[n>>24&255]+"-"+yt[e&255]+yt[e>>8&255]+"-"+yt[e>>16&15|64]+yt[e>>24&255]+"-"+yt[t&63|128]+yt[t>>8&255]+"-"+yt[t>>16&255]+yt[t>>24&255]+yt[i&255]+yt[i>>8&255]+yt[i>>16&255]+yt[i>>24&255]).toLowerCase()}function Xe(n,e,t){return Math.max(e,Math.min(t,n))}function ou(n,e){return(n%e+e)%e}function Ja(n,e,t){return(1-t)*n+t*e}function Fi(n,e){switch(e.constructor){case Float32Array:return n;case Uint32Array:return n/4294967295;case Uint16Array:return n/65535;case Uint8Array:return n/255;case Int32Array:return Math.max(n/2147483647,-1);case Int16Array:return Math.max(n/32767,-1);case Int8Array:return Math.max(n/127,-1);default:throw new Error("Invalid component type.")}}function It(n,e){switch(e.constructor){case Float32Array:return n;case Uint32Array:return Math.round(n*4294967295);case Uint16Array:return Math.round(n*65535);case Uint8Array:return Math.round(n*255);case Int32Array:return Math.round(n*2147483647);case Int16Array:return Math.round(n*32767);case Int8Array:return Math.round(n*127);default:throw new Error("Invalid component type.")}}class Ke{constructor(e=0,t=0){Ke.prototype.isVector2=!0,this.x=e,this.y=t}get width(){return this.x}set width(e){this.x=e}get height(){return this.y}set height(e){this.y=e}set(e,t){return this.x=e,this.y=t,this}setScalar(e){return this.x=e,this.y=e,this}setX(e){return this.x=e,this}setY(e){return this.y=e,this}setComponent(e,t){switch(e){case 0:this.x=t;break;case 1:this.y=t;break;default:throw new Error("index is out of range: "+e)}return this}getComponent(e){switch(e){case 0:return this.x;case 1:return this.y;default:throw new Error("index is out of range: "+e)}}clone(){return new this.constructor(this.x,this.y)}copy(e){return this.x=e.x,this.y=e.y,this}add(e){return this.x+=e.x,this.y+=e.y,this}addScalar(e){return this.x+=e,this.y+=e,this}addVectors(e,t){return this.x=e.x+t.x,this.y=e.y+t.y,this}addScaledVector(e,t){return this.x+=e.x*t,this.y+=e.y*t,this}sub(e){return this.x-=e.x,this.y-=e.y,this}subScalar(e){return this.x-=e,this.y-=e,this}subVectors(e,t){return this.x=e.x-t.x,this.y=e.y-t.y,this}multiply(e){return this.x*=e.x,this.y*=e.y,this}multiplyScalar(e){return this.x*=e,this.y*=e,this}divide(e){return this.x/=e.x,this.y/=e.y,this}divideScalar(e){return this.multiplyScalar(1/e)}applyMatrix3(e){const t=this.x,i=this.y,a=e.elements;return this.x=a[0]*t+a[3]*i+a[6],this.y=a[1]*t+a[4]*i+a[7],this}min(e){return this.x=Math.min(this.x,e.x),this.y=Math.min(this.y,e.y),this}max(e){return this.x=Math.max(this.x,e.x),this.y=Math.max(this.y,e.y),this}clamp(e,t){return this.x=Xe(this.x,e.x,t.x),this.y=Xe(this.y,e.y,t.y),this}clampScalar(e,t){return this.x=Xe(this.x,e,t),this.y=Xe(this.y,e,t),this}clampLength(e,t){const i=this.length();return this.divideScalar(i||1).multiplyScalar(Xe(i,e,t))}floor(){return this.x=Math.floor(this.x),this.y=Math.floor(this.y),this}ceil(){return this.x=Math.ceil(this.x),this.y=Math.ceil(this.y),this}round(){return this.x=Math.round(this.x),this.y=Math.round(this.y),this}roundToZero(){return this.x=Math.trunc(this.x),this.y=Math.trunc(this.y),this}negate(){return this.x=-this.x,this.y=-this.y,this}dot(e){return this.x*e.x+this.y*e.y}cross(e){return this.x*e.y-this.y*e.x}lengthSq(){return this.x*this.x+this.y*this.y}length(){return Math.sqrt(this.x*this.x+this.y*this.y)}manhattanLength(){return Math.abs(this.x)+Math.abs(this.y)}normalize(){return this.divideScalar(this.length()||1)}angle(){return Math.atan2(-this.y,-this.x)+Math.PI}angleTo(e){const t=Math.sqrt(this.lengthSq()*e.lengthSq());if(t===0)return Math.PI/2;const i=this.dot(e)/t;return Math.acos(Xe(i,-1,1))}distanceTo(e){return Math.sqrt(this.distanceToSquared(e))}distanceToSquared(e){const t=this.x-e.x,i=this.y-e.y;return t*t+i*i}manhattanDistanceTo(e){return Math.abs(this.x-e.x)+Math.abs(this.y-e.y)}setLength(e){return this.normalize().multiplyScalar(e)}lerp(e,t){return this.x+=(e.x-this.x)*t,this.y+=(e.y-this.y)*t,this}lerpVectors(e,t,i){return this.x=e.x+(t.x-e.x)*i,this.y=e.y+(t.y-e.y)*i,this}equals(e){return e.x===this.x&&e.y===this.y}fromArray(e,t=0){return this.x=e[t],this.y=e[t+1],this}toArray(e=[],t=0){return e[t]=this.x,e[t+1]=this.y,e}fromBufferAttribute(e,t){return this.x=e.getX(t),this.y=e.getY(t),this}rotateAround(e,t){const i=Math.cos(t),a=Math.sin(t),r=this.x-e.x,s=this.y-e.y;return this.x=r*i-s*a+e.x,this.y=r*a+s*i+e.y,this}random(){return this.x=Math.random(),this.y=Math.random(),this}*[Symbol.iterator](){yield this.x,yield this.y}}class Be{constructor(e,t,i,a,r,s,o,c,l){Be.prototype.isMatrix3=!0,this.elements=[1,0,0,0,1,0,0,0,1],e!==void 0&&this.set(e,t,i,a,r,s,o,c,l)}set(e,t,i,a,r,s,o,c,l){const u=this.elements;return u[0]=e,u[1]=a,u[2]=o,u[3]=t,u[4]=r,u[5]=c,u[6]=i,u[7]=s,u[8]=l,this}identity(){return this.set(1,0,0,0,1,0,0,0,1),this}copy(e){const t=this.elements,i=e.elements;return t[0]=i[0],t[1]=i[1],t[2]=i[2],t[3]=i[3],t[4]=i[4],t[5]=i[5],t[6]=i[6],t[7]=i[7],t[8]=i[8],this}extractBasis(e,t,i){return e.setFromMatrix3Column(this,0),t.setFromMatrix3Column(this,1),i.setFromMatrix3Column(this,2),this}setFromMatrix4(e){const t=e.elements;return this.set(t[0],t[4],t[8],t[1],t[5],t[9],t[2],t[6],t[10]),this}multiply(e){return this.multiplyMatrices(this,e)}premultiply(e){return this.multiplyMatrices(e,this)}multiplyMatrices(e,t){const i=e.elements,a=t.elements,r=this.elements,s=i[0],o=i[3],c=i[6],l=i[1],u=i[4],h=i[7],f=i[2],m=i[5],g=i[8],_=a[0],p=a[3],d=a[6],E=a[1],S=a[4],x=a[7],T=a[2],y=a[5],w=a[8];return r[0]=s*_+o*E+c*T,r[3]=s*p+o*S+c*y,r[6]=s*d+o*x+c*w,r[1]=l*_+u*E+h*T,r[4]=l*p+u*S+h*y,r[7]=l*d+u*x+h*w,r[2]=f*_+m*E+g*T,r[5]=f*p+m*S+g*y,r[8]=f*d+m*x+g*w,this}multiplyScalar(e){const t=this.elements;return t[0]*=e,t[3]*=e,t[6]*=e,t[1]*=e,t[4]*=e,t[7]*=e,t[2]*=e,t[5]*=e,t[8]*=e,this}determinant(){const e=this.elements,t=e[0],i=e[1],a=e[2],r=e[3],s=e[4],o=e[5],c=e[6],l=e[7],u=e[8];return t*s*u-t*o*l-i*r*u+i*o*c+a*r*l-a*s*c}invert(){const e=this.elements,t=e[0],i=e[1],a=e[2],r=e[3],s=e[4],o=e[5],c=e[6],l=e[7],u=e[8],h=u*s-o*l,f=o*c-u*r,m=l*r-s*c,g=t*h+i*f+a*m;if(g===0)return this.set(0,0,0,0,0,0,0,0,0);const _=1/g;return e[0]=h*_,e[1]=(a*l-u*i)*_,e[2]=(o*i-a*s)*_,e[3]=f*_,e[4]=(u*t-a*c)*_,e[5]=(a*r-o*t)*_,e[6]=m*_,e[7]=(i*c-l*t)*_,e[8]=(s*t-i*r)*_,this}transpose(){let e;const t=this.elements;return e=t[1],t[1]=t[3],t[3]=e,e=t[2],t[2]=t[6],t[6]=e,e=t[5],t[5]=t[7],t[7]=e,this}getNormalMatrix(e){return this.setFromMatrix4(e).invert().transpose()}transposeIntoArray(e){const t=this.elements;return e[0]=t[0],e[1]=t[3],e[2]=t[6],e[3]=t[1],e[4]=t[4],e[5]=t[7],e[6]=t[2],e[7]=t[5],e[8]=t[8],this}setUvTransform(e,t,i,a,r,s,o){const c=Math.cos(r),l=Math.sin(r);return this.set(i*c,i*l,-i*(c*s+l*o)+s+e,-a*l,a*c,-a*(-l*s+c*o)+o+t,0,0,1),this}scale(e,t){return this.premultiply(Qa.makeScale(e,t)),this}rotate(e){return this.premultiply(Qa.makeRotation(-e)),this}translate(e,t){return this.premultiply(Qa.makeTranslation(e,t)),this}makeTranslation(e,t){return e.isVector2?this.set(1,0,e.x,0,1,e.y,0,0,1):this.set(1,0,e,0,1,t,0,0,1),this}makeRotation(e){const t=Math.cos(e),i=Math.sin(e);return this.set(t,-i,0,i,t,0,0,0,1),this}makeScale(e,t){return this.set(e,0,0,0,t,0,0,0,1),this}equals(e){const t=this.elements,i=e.elements;for(let a=0;a<9;a++)if(t[a]!==i[a])return!1;return!0}fromArray(e,t=0){for(let i=0;i<9;i++)this.elements[i]=e[i+t];return this}toArray(e=[],t=0){const i=this.elements;return e[t]=i[0],e[t+1]=i[1],e[t+2]=i[2],e[t+3]=i[3],e[t+4]=i[4],e[t+5]=i[5],e[t+6]=i[6],e[t+7]=i[7],e[t+8]=i[8],e}clone(){return new this.constructor().fromArray(this.elements)}}const Qa=new Be;function Oc(n){for(let e=n.length-1;e>=0;--e)if(n[e]>=65535)return!0;return!1}function Ba(n){return document.createElementNS("http://www.w3.org/1999/xhtml",n)}function cu(){const n=Ba("canvas");return n.style.display="block",n}const uo={};function Hn(n){n in uo||(uo[n]=!0,console.warn(n))}function lu(n,e,t){return new Promise(function(i,a){function r(){switch(n.clientWaitSync(e,n.SYNC_FLUSH_COMMANDS_BIT,0)){case n.WAIT_FAILED:a();break;case n.TIMEOUT_EXPIRED:setTimeout(r,t);break;default:i()}}setTimeout(r,t)})}function uu(n){const e=n.elements;e[2]=.5*e[2]+.5*e[3],e[6]=.5*e[6]+.5*e[7],e[10]=.5*e[10]+.5*e[11],e[14]=.5*e[14]+.5*e[15]}function du(n){const e=n.elements;e[11]===-1?(e[10]=-e[10]-1,e[14]=-e[14]):(e[10]=-e[10],e[14]=-e[14]+1)}const ho=new Be().set(.4123908,.3575843,.1804808,.212639,.7151687,.0721923,.0193308,.1191948,.9505322),fo=new Be().set(3.2409699,-1.5373832,-.4986108,-.9692436,1.8759675,.0415551,.0556301,-.203977,1.0569715);function hu(){const n={enabled:!0,workingColorSpace:Pi,spaces:{},convert:function(a,r,s){return this.enabled===!1||r===s||!r||!s||(this.spaces[r].transfer===at&&(a.r=gn(a.r),a.g=gn(a.g),a.b=gn(a.b)),this.spaces[r].primaries!==this.spaces[s].primaries&&(a.applyMatrix3(this.spaces[r].toXYZ),a.applyMatrix3(this.spaces[s].fromXYZ)),this.spaces[s].transfer===at&&(a.r=yi(a.r),a.g=yi(a.g),a.b=yi(a.b))),a},fromWorkingColorSpace:function(a,r){return this.convert(a,this.workingColorSpace,r)},toWorkingColorSpace:function(a,r){return this.convert(a,r,this.workingColorSpace)},getPrimaries:function(a){return this.spaces[a].primaries},getTransfer:function(a){return a===Cn?Fa:this.spaces[a].transfer},getLuminanceCoefficients:function(a,r=this.workingColorSpace){return a.fromArray(this.spaces[r].luminanceCoefficients)},define:function(a){Object.assign(this.spaces,a)},_getMatrix:function(a,r,s){return a.copy(this.spaces[r].toXYZ).multiply(this.spaces[s].fromXYZ)},_getDrawingBufferColorSpace:function(a){return this.spaces[a].outputColorSpaceConfig.drawingBufferColorSpace},_getUnpackColorSpace:function(a=this.workingColorSpace){return this.spaces[a].workingColorSpaceConfig.unpackColorSpace}},e=[.64,.33,.3,.6,.15,.06],t=[.2126,.7152,.0722],i=[.3127,.329];return n.define({[Pi]:{primaries:e,whitePoint:i,transfer:Fa,toXYZ:ho,fromXYZ:fo,luminanceCoefficients:t,workingColorSpaceConfig:{unpackColorSpace:Ft},outputColorSpaceConfig:{drawingBufferColorSpace:Ft}},[Ft]:{primaries:e,whitePoint:i,transfer:at,toXYZ:ho,fromXYZ:fo,luminanceCoefficients:t,outputColorSpaceConfig:{drawingBufferColorSpace:Ft}}}),n}const Qe=hu();function gn(n){return n<.04045?n*.0773993808:Math.pow(n*.9478672986+.0521327014,2.4)}function yi(n){return n<.0031308?n*12.92:1.055*Math.pow(n,.41666)-.055}let ai;class fu{static getDataURL(e){if(/^data:/i.test(e.src)||typeof HTMLCanvasElement>"u")return e.src;let t;if(e instanceof HTMLCanvasElement)t=e;else{ai===void 0&&(ai=Ba("canvas")),ai.width=e.width,ai.height=e.height;const i=ai.getContext("2d");e instanceof ImageData?i.putImageData(e,0,0):i.drawImage(e,0,0,e.width,e.height),t=ai}return t.toDataURL("image/png")}static sRGBToLinear(e){if(typeof HTMLImageElement<"u"&&e instanceof HTMLImageElement||typeof HTMLCanvasElement<"u"&&e instanceof HTMLCanvasElement||typeof ImageBitmap<"u"&&e instanceof ImageBitmap){const t=Ba("canvas");t.width=e.width,t.height=e.height;const i=t.getContext("2d");i.drawImage(e,0,0,e.width,e.height);const a=i.getImageData(0,0,e.width,e.height),r=a.data;for(let s=0;s<r.length;s++)r[s]=gn(r[s]/255)*255;return i.putImageData(a,0,0),t}else if(e.data){const t=e.data.slice(0);for(let i=0;i<t.length;i++)t instanceof Uint8Array||t instanceof Uint8ClampedArray?t[i]=Math.floor(gn(t[i]/255)*255):t[i]=gn(t[i]);return{data:t,width:e.width,height:e.height}}else return console.warn("THREE.ImageUtils.sRGBToLinear(): Unsupported image type. No color space conversion applied."),e}}let pu=0;class Ns{constructor(e=null){this.isSource=!0,Object.defineProperty(this,"id",{value:pu++}),this.uuid=Zi(),this.data=e,this.dataReady=!0,this.version=0}set needsUpdate(e){e===!0&&this.version++}toJSON(e){const t=e===void 0||typeof e=="string";if(!t&&e.images[this.uuid]!==void 0)return e.images[this.uuid];const i={uuid:this.uuid,url:""},a=this.data;if(a!==null){let r;if(Array.isArray(a)){r=[];for(let s=0,o=a.length;s<o;s++)a[s].isDataTexture?r.push(er(a[s].image)):r.push(er(a[s]))}else r=er(a);i.url=r}return t||(e.images[this.uuid]=i),i}}function er(n){return typeof HTMLImageElement<"u"&&n instanceof HTMLImageElement||typeof HTMLCanvasElement<"u"&&n instanceof HTMLCanvasElement||typeof ImageBitmap<"u"&&n instanceof ImageBitmap?fu.getDataURL(n):n.data?{data:Array.from(n.data),width:n.width,height:n.height,type:n.data.constructor.name}:(console.warn("THREE.Texture: Unable to serialize Texture."),{})}let mu=0;class Ct extends Di{constructor(e=Ct.DEFAULT_IMAGE,t=Ct.DEFAULT_MAPPING,i=Yn,a=Yn,r=en,s=Zn,o=Zt,c=_n,l=Ct.DEFAULT_ANISOTROPY,u=Cn){super(),this.isTexture=!0,Object.defineProperty(this,"id",{value:mu++}),this.uuid=Zi(),this.name="",this.source=new Ns(e),this.mipmaps=[],this.mapping=t,this.channel=0,this.wrapS=i,this.wrapT=a,this.magFilter=r,this.minFilter=s,this.anisotropy=l,this.format=o,this.internalFormat=null,this.type=c,this.offset=new Ke(0,0),this.repeat=new Ke(1,1),this.center=new Ke(0,0),this.rotation=0,this.matrixAutoUpdate=!0,this.matrix=new Be,this.generateMipmaps=!0,this.premultiplyAlpha=!1,this.flipY=!0,this.unpackAlignment=4,this.colorSpace=u,this.userData={},this.version=0,this.onUpdate=null,this.renderTarget=null,this.isRenderTargetTexture=!1,this.pmremVersion=0}get image(){return this.source.data}set image(e=null){this.source.data=e}updateMatrix(){this.matrix.setUvTransform(this.offset.x,this.offset.y,this.repeat.x,this.repeat.y,this.rotation,this.center.x,this.center.y)}clone(){return new this.constructor().copy(this)}copy(e){return this.name=e.name,this.source=e.source,this.mipmaps=e.mipmaps.slice(0),this.mapping=e.mapping,this.channel=e.channel,this.wrapS=e.wrapS,this.wrapT=e.wrapT,this.magFilter=e.magFilter,this.minFilter=e.minFilter,this.anisotropy=e.anisotropy,this.format=e.format,this.internalFormat=e.internalFormat,this.type=e.type,this.offset.copy(e.offset),this.repeat.copy(e.repeat),this.center.copy(e.center),this.rotation=e.rotation,this.matrixAutoUpdate=e.matrixAutoUpdate,this.matrix.copy(e.matrix),this.generateMipmaps=e.generateMipmaps,this.premultiplyAlpha=e.premultiplyAlpha,this.flipY=e.flipY,this.unpackAlignment=e.unpackAlignment,this.colorSpace=e.colorSpace,this.renderTarget=e.renderTarget,this.isRenderTargetTexture=e.isRenderTargetTexture,this.userData=JSON.parse(JSON.stringify(e.userData)),this.needsUpdate=!0,this}toJSON(e){const t=e===void 0||typeof e=="string";if(!t&&e.textures[this.uuid]!==void 0)return e.textures[this.uuid];const i={metadata:{version:4.6,type:"Texture",generator:"Texture.toJSON"},uuid:this.uuid,name:this.name,image:this.source.toJSON(e).uuid,mapping:this.mapping,channel:this.channel,repeat:[this.repeat.x,this.repeat.y],offset:[this.offset.x,this.offset.y],center:[this.center.x,this.center.y],rotation:this.rotation,wrap:[this.wrapS,this.wrapT],format:this.format,internalFormat:this.internalFormat,type:this.type,colorSpace:this.colorSpace,minFilter:this.minFilter,magFilter:this.magFilter,anisotropy:this.anisotropy,flipY:this.flipY,generateMipmaps:this.generateMipmaps,premultiplyAlpha:this.premultiplyAlpha,unpackAlignment:this.unpackAlignment};return Object.keys(this.userData).length>0&&(i.userData=this.userData),t||(e.textures[this.uuid]=i),i}dispose(){this.dispatchEvent({type:"dispose"})}transformUv(e){if(this.mapping!==Ac)return e;if(e.applyMatrix3(this.matrix),e.x<0||e.x>1)switch(this.wrapS){case Xr:e.x=e.x-Math.floor(e.x);break;case Yn:e.x=e.x<0?0:1;break;case Kr:Math.abs(Math.floor(e.x)%2)===1?e.x=Math.ceil(e.x)-e.x:e.x=e.x-Math.floor(e.x);break}if(e.y<0||e.y>1)switch(this.wrapT){case Xr:e.y=e.y-Math.floor(e.y);break;case Yn:e.y=e.y<0?0:1;break;case Kr:Math.abs(Math.floor(e.y)%2)===1?e.y=Math.ceil(e.y)-e.y:e.y=e.y-Math.floor(e.y);break}return this.flipY&&(e.y=1-e.y),e}set needsUpdate(e){e===!0&&(this.version++,this.source.needsUpdate=!0)}set needsPMREMUpdate(e){e===!0&&this.pmremVersion++}}Ct.DEFAULT_IMAGE=null;Ct.DEFAULT_MAPPING=Ac;Ct.DEFAULT_ANISOTROPY=1;class dt{constructor(e=0,t=0,i=0,a=1){dt.prototype.isVector4=!0,this.x=e,this.y=t,this.z=i,this.w=a}get width(){return this.z}set width(e){this.z=e}get height(){return this.w}set height(e){this.w=e}set(e,t,i,a){return this.x=e,this.y=t,this.z=i,this.w=a,this}setScalar(e){return this.x=e,this.y=e,this.z=e,this.w=e,this}setX(e){return this.x=e,this}setY(e){return this.y=e,this}setZ(e){return this.z=e,this}setW(e){return this.w=e,this}setComponent(e,t){switch(e){case 0:this.x=t;break;case 1:this.y=t;break;case 2:this.z=t;break;case 3:this.w=t;break;default:throw new Error("index is out of range: "+e)}return this}getComponent(e){switch(e){case 0:return this.x;case 1:return this.y;case 2:return this.z;case 3:return this.w;default:throw new Error("index is out of range: "+e)}}clone(){return new this.constructor(this.x,this.y,this.z,this.w)}copy(e){return this.x=e.x,this.y=e.y,this.z=e.z,this.w=e.w!==void 0?e.w:1,this}add(e){return this.x+=e.x,this.y+=e.y,this.z+=e.z,this.w+=e.w,this}addScalar(e){return this.x+=e,this.y+=e,this.z+=e,this.w+=e,this}addVectors(e,t){return this.x=e.x+t.x,this.y=e.y+t.y,this.z=e.z+t.z,this.w=e.w+t.w,this}addScaledVector(e,t){return this.x+=e.x*t,this.y+=e.y*t,this.z+=e.z*t,this.w+=e.w*t,this}sub(e){return this.x-=e.x,this.y-=e.y,this.z-=e.z,this.w-=e.w,this}subScalar(e){return this.x-=e,this.y-=e,this.z-=e,this.w-=e,this}subVectors(e,t){return this.x=e.x-t.x,this.y=e.y-t.y,this.z=e.z-t.z,this.w=e.w-t.w,this}multiply(e){return this.x*=e.x,this.y*=e.y,this.z*=e.z,this.w*=e.w,this}multiplyScalar(e){return this.x*=e,this.y*=e,this.z*=e,this.w*=e,this}applyMatrix4(e){const t=this.x,i=this.y,a=this.z,r=this.w,s=e.elements;return this.x=s[0]*t+s[4]*i+s[8]*a+s[12]*r,this.y=s[1]*t+s[5]*i+s[9]*a+s[13]*r,this.z=s[2]*t+s[6]*i+s[10]*a+s[14]*r,this.w=s[3]*t+s[7]*i+s[11]*a+s[15]*r,this}divide(e){return this.x/=e.x,this.y/=e.y,this.z/=e.z,this.w/=e.w,this}divideScalar(e){return this.multiplyScalar(1/e)}setAxisAngleFromQuaternion(e){this.w=2*Math.acos(e.w);const t=Math.sqrt(1-e.w*e.w);return t<1e-4?(this.x=1,this.y=0,this.z=0):(this.x=e.x/t,this.y=e.y/t,this.z=e.z/t),this}setAxisAngleFromRotationMatrix(e){let t,i,a,r;const c=e.elements,l=c[0],u=c[4],h=c[8],f=c[1],m=c[5],g=c[9],_=c[2],p=c[6],d=c[10];if(Math.abs(u-f)<.01&&Math.abs(h-_)<.01&&Math.abs(g-p)<.01){if(Math.abs(u+f)<.1&&Math.abs(h+_)<.1&&Math.abs(g+p)<.1&&Math.abs(l+m+d-3)<.1)return this.set(1,0,0,0),this;t=Math.PI;const S=(l+1)/2,x=(m+1)/2,T=(d+1)/2,y=(u+f)/4,w=(h+_)/4,D=(g+p)/4;return S>x&&S>T?S<.01?(i=0,a=.707106781,r=.707106781):(i=Math.sqrt(S),a=y/i,r=w/i):x>T?x<.01?(i=.707106781,a=0,r=.707106781):(a=Math.sqrt(x),i=y/a,r=D/a):T<.01?(i=.707106781,a=.707106781,r=0):(r=Math.sqrt(T),i=w/r,a=D/r),this.set(i,a,r,t),this}let E=Math.sqrt((p-g)*(p-g)+(h-_)*(h-_)+(f-u)*(f-u));return Math.abs(E)<.001&&(E=1),this.x=(p-g)/E,this.y=(h-_)/E,this.z=(f-u)/E,this.w=Math.acos((l+m+d-1)/2),this}setFromMatrixPosition(e){const t=e.elements;return this.x=t[12],this.y=t[13],this.z=t[14],this.w=t[15],this}min(e){return this.x=Math.min(this.x,e.x),this.y=Math.min(this.y,e.y),this.z=Math.min(this.z,e.z),this.w=Math.min(this.w,e.w),this}max(e){return this.x=Math.max(this.x,e.x),this.y=Math.max(this.y,e.y),this.z=Math.max(this.z,e.z),this.w=Math.max(this.w,e.w),this}clamp(e,t){return this.x=Xe(this.x,e.x,t.x),this.y=Xe(this.y,e.y,t.y),this.z=Xe(this.z,e.z,t.z),this.w=Xe(this.w,e.w,t.w),this}clampScalar(e,t){return this.x=Xe(this.x,e,t),this.y=Xe(this.y,e,t),this.z=Xe(this.z,e,t),this.w=Xe(this.w,e,t),this}clampLength(e,t){const i=this.length();return this.divideScalar(i||1).multiplyScalar(Xe(i,e,t))}floor(){return this.x=Math.floor(this.x),this.y=Math.floor(this.y),this.z=Math.floor(this.z),this.w=Math.floor(this.w),this}ceil(){return this.x=Math.ceil(this.x),this.y=Math.ceil(this.y),this.z=Math.ceil(this.z),this.w=Math.ceil(this.w),this}round(){return this.x=Math.round(this.x),this.y=Math.round(this.y),this.z=Math.round(this.z),this.w=Math.round(this.w),this}roundToZero(){return this.x=Math.trunc(this.x),this.y=Math.trunc(this.y),this.z=Math.trunc(this.z),this.w=Math.trunc(this.w),this}negate(){return this.x=-this.x,this.y=-this.y,this.z=-this.z,this.w=-this.w,this}dot(e){return this.x*e.x+this.y*e.y+this.z*e.z+this.w*e.w}lengthSq(){return this.x*this.x+this.y*this.y+this.z*this.z+this.w*this.w}length(){return Math.sqrt(this.x*this.x+this.y*this.y+this.z*this.z+this.w*this.w)}manhattanLength(){return Math.abs(this.x)+Math.abs(this.y)+Math.abs(this.z)+Math.abs(this.w)}normalize(){return this.divideScalar(this.length()||1)}setLength(e){return this.normalize().multiplyScalar(e)}lerp(e,t){return this.x+=(e.x-this.x)*t,this.y+=(e.y-this.y)*t,this.z+=(e.z-this.z)*t,this.w+=(e.w-this.w)*t,this}lerpVectors(e,t,i){return this.x=e.x+(t.x-e.x)*i,this.y=e.y+(t.y-e.y)*i,this.z=e.z+(t.z-e.z)*i,this.w=e.w+(t.w-e.w)*i,this}equals(e){return e.x===this.x&&e.y===this.y&&e.z===this.z&&e.w===this.w}fromArray(e,t=0){return this.x=e[t],this.y=e[t+1],this.z=e[t+2],this.w=e[t+3],this}toArray(e=[],t=0){return e[t]=this.x,e[t+1]=this.y,e[t+2]=this.z,e[t+3]=this.w,e}fromBufferAttribute(e,t){return this.x=e.getX(t),this.y=e.getY(t),this.z=e.getZ(t),this.w=e.getW(t),this}random(){return this.x=Math.random(),this.y=Math.random(),this.z=Math.random(),this.w=Math.random(),this}*[Symbol.iterator](){yield this.x,yield this.y,yield this.z,yield this.w}}class gu extends Di{constructor(e=1,t=1,i={}){super(),this.isRenderTarget=!0,this.width=e,this.height=t,this.depth=1,this.scissor=new dt(0,0,e,t),this.scissorTest=!1,this.viewport=new dt(0,0,e,t);const a={width:e,height:t,depth:1};i=Object.assign({generateMipmaps:!1,internalFormat:null,minFilter:en,depthBuffer:!0,stencilBuffer:!1,resolveDepthBuffer:!0,resolveStencilBuffer:!0,depthTexture:null,samples:0,count:1},i);const r=new Ct(a,i.mapping,i.wrapS,i.wrapT,i.magFilter,i.minFilter,i.format,i.type,i.anisotropy,i.colorSpace);r.flipY=!1,r.generateMipmaps=i.generateMipmaps,r.internalFormat=i.internalFormat,this.textures=[];const s=i.count;for(let o=0;o<s;o++)this.textures[o]=r.clone(),this.textures[o].isRenderTargetTexture=!0,this.textures[o].renderTarget=this;this.depthBuffer=i.depthBuffer,this.stencilBuffer=i.stencilBuffer,this.resolveDepthBuffer=i.resolveDepthBuffer,this.resolveStencilBuffer=i.resolveStencilBuffer,this._depthTexture=null,this.depthTexture=i.depthTexture,this.samples=i.samples}get texture(){return this.textures[0]}set texture(e){this.textures[0]=e}set depthTexture(e){this._depthTexture!==null&&(this._depthTexture.renderTarget=null),e!==null&&(e.renderTarget=this),this._depthTexture=e}get depthTexture(){return this._depthTexture}setSize(e,t,i=1){if(this.width!==e||this.height!==t||this.depth!==i){this.width=e,this.height=t,this.depth=i;for(let a=0,r=this.textures.length;a<r;a++)this.textures[a].image.width=e,this.textures[a].image.height=t,this.textures[a].image.depth=i;this.dispose()}this.viewport.set(0,0,e,t),this.scissor.set(0,0,e,t)}clone(){return new this.constructor().copy(this)}copy(e){this.width=e.width,this.height=e.height,this.depth=e.depth,this.scissor.copy(e.scissor),this.scissorTest=e.scissorTest,this.viewport.copy(e.viewport),this.textures.length=0;for(let t=0,i=e.textures.length;t<i;t++){this.textures[t]=e.textures[t].clone(),this.textures[t].isRenderTargetTexture=!0,this.textures[t].renderTarget=this;const a=Object.assign({},e.textures[t].image);this.textures[t].source=new Ns(a)}return this.depthBuffer=e.depthBuffer,this.stencilBuffer=e.stencilBuffer,this.resolveDepthBuffer=e.resolveDepthBuffer,this.resolveStencilBuffer=e.resolveStencilBuffer,e.depthTexture!==null&&(this.depthTexture=e.depthTexture.clone()),this.samples=e.samples,this}dispose(){this.dispatchEvent({type:"dispose"})}}class ti extends gu{constructor(e=1,t=1,i={}){super(e,t,i),this.isWebGLRenderTarget=!0}}class Bc extends Ct{constructor(e=null,t=1,i=1,a=1){super(null),this.isDataArrayTexture=!0,this.image={data:e,width:t,height:i,depth:a},this.magFilter=Jt,this.minFilter=Jt,this.wrapR=Yn,this.generateMipmaps=!1,this.flipY=!1,this.unpackAlignment=1,this.layerUpdates=new Set}addLayerUpdate(e){this.layerUpdates.add(e)}clearLayerUpdates(){this.layerUpdates.clear()}}class _u extends Ct{constructor(e=null,t=1,i=1,a=1){super(null),this.isData3DTexture=!0,this.image={data:e,width:t,height:i,depth:a},this.magFilter=Jt,this.minFilter=Jt,this.wrapR=Yn,this.generateMipmaps=!1,this.flipY=!1,this.unpackAlignment=1}}class Ji{constructor(e=0,t=0,i=0,a=1){this.isQuaternion=!0,this._x=e,this._y=t,this._z=i,this._w=a}static slerpFlat(e,t,i,a,r,s,o){let c=i[a+0],l=i[a+1],u=i[a+2],h=i[a+3];const f=r[s+0],m=r[s+1],g=r[s+2],_=r[s+3];if(o===0){e[t+0]=c,e[t+1]=l,e[t+2]=u,e[t+3]=h;return}if(o===1){e[t+0]=f,e[t+1]=m,e[t+2]=g,e[t+3]=_;return}if(h!==_||c!==f||l!==m||u!==g){let p=1-o;const d=c*f+l*m+u*g+h*_,E=d>=0?1:-1,S=1-d*d;if(S>Number.EPSILON){const T=Math.sqrt(S),y=Math.atan2(T,d*E);p=Math.sin(p*y)/T,o=Math.sin(o*y)/T}const x=o*E;if(c=c*p+f*x,l=l*p+m*x,u=u*p+g*x,h=h*p+_*x,p===1-o){const T=1/Math.sqrt(c*c+l*l+u*u+h*h);c*=T,l*=T,u*=T,h*=T}}e[t]=c,e[t+1]=l,e[t+2]=u,e[t+3]=h}static multiplyQuaternionsFlat(e,t,i,a,r,s){const o=i[a],c=i[a+1],l=i[a+2],u=i[a+3],h=r[s],f=r[s+1],m=r[s+2],g=r[s+3];return e[t]=o*g+u*h+c*m-l*f,e[t+1]=c*g+u*f+l*h-o*m,e[t+2]=l*g+u*m+o*f-c*h,e[t+3]=u*g-o*h-c*f-l*m,e}get x(){return this._x}set x(e){this._x=e,this._onChangeCallback()}get y(){return this._y}set y(e){this._y=e,this._onChangeCallback()}get z(){return this._z}set z(e){this._z=e,this._onChangeCallback()}get w(){return this._w}set w(e){this._w=e,this._onChangeCallback()}set(e,t,i,a){return this._x=e,this._y=t,this._z=i,this._w=a,this._onChangeCallback(),this}clone(){return new this.constructor(this._x,this._y,this._z,this._w)}copy(e){return this._x=e.x,this._y=e.y,this._z=e.z,this._w=e.w,this._onChangeCallback(),this}setFromEuler(e,t=!0){const i=e._x,a=e._y,r=e._z,s=e._order,o=Math.cos,c=Math.sin,l=o(i/2),u=o(a/2),h=o(r/2),f=c(i/2),m=c(a/2),g=c(r/2);switch(s){case"XYZ":this._x=f*u*h+l*m*g,this._y=l*m*h-f*u*g,this._z=l*u*g+f*m*h,this._w=l*u*h-f*m*g;break;case"YXZ":this._x=f*u*h+l*m*g,this._y=l*m*h-f*u*g,this._z=l*u*g-f*m*h,this._w=l*u*h+f*m*g;break;case"ZXY":this._x=f*u*h-l*m*g,this._y=l*m*h+f*u*g,this._z=l*u*g+f*m*h,this._w=l*u*h-f*m*g;break;case"ZYX":this._x=f*u*h-l*m*g,this._y=l*m*h+f*u*g,this._z=l*u*g-f*m*h,this._w=l*u*h+f*m*g;break;case"YZX":this._x=f*u*h+l*m*g,this._y=l*m*h+f*u*g,this._z=l*u*g-f*m*h,this._w=l*u*h-f*m*g;break;case"XZY":this._x=f*u*h-l*m*g,this._y=l*m*h-f*u*g,this._z=l*u*g+f*m*h,this._w=l*u*h+f*m*g;break;default:console.warn("THREE.Quaternion: .setFromEuler() encountered an unknown order: "+s)}return t===!0&&this._onChangeCallback(),this}setFromAxisAngle(e,t){const i=t/2,a=Math.sin(i);return this._x=e.x*a,this._y=e.y*a,this._z=e.z*a,this._w=Math.cos(i),this._onChangeCallback(),this}setFromRotationMatrix(e){const t=e.elements,i=t[0],a=t[4],r=t[8],s=t[1],o=t[5],c=t[9],l=t[2],u=t[6],h=t[10],f=i+o+h;if(f>0){const m=.5/Math.sqrt(f+1);this._w=.25/m,this._x=(u-c)*m,this._y=(r-l)*m,this._z=(s-a)*m}else if(i>o&&i>h){const m=2*Math.sqrt(1+i-o-h);this._w=(u-c)/m,this._x=.25*m,this._y=(a+s)/m,this._z=(r+l)/m}else if(o>h){const m=2*Math.sqrt(1+o-i-h);this._w=(r-l)/m,this._x=(a+s)/m,this._y=.25*m,this._z=(c+u)/m}else{const m=2*Math.sqrt(1+h-i-o);this._w=(s-a)/m,this._x=(r+l)/m,this._y=(c+u)/m,this._z=.25*m}return this._onChangeCallback(),this}setFromUnitVectors(e,t){let i=e.dot(t)+1;return i<Number.EPSILON?(i=0,Math.abs(e.x)>Math.abs(e.z)?(this._x=-e.y,this._y=e.x,this._z=0,this._w=i):(this._x=0,this._y=-e.z,this._z=e.y,this._w=i)):(this._x=e.y*t.z-e.z*t.y,this._y=e.z*t.x-e.x*t.z,this._z=e.x*t.y-e.y*t.x,this._w=i),this.normalize()}angleTo(e){return 2*Math.acos(Math.abs(Xe(this.dot(e),-1,1)))}rotateTowards(e,t){const i=this.angleTo(e);if(i===0)return this;const a=Math.min(1,t/i);return this.slerp(e,a),this}identity(){return this.set(0,0,0,1)}invert(){return this.conjugate()}conjugate(){return this._x*=-1,this._y*=-1,this._z*=-1,this._onChangeCallback(),this}dot(e){return this._x*e._x+this._y*e._y+this._z*e._z+this._w*e._w}lengthSq(){return this._x*this._x+this._y*this._y+this._z*this._z+this._w*this._w}length(){return Math.sqrt(this._x*this._x+this._y*this._y+this._z*this._z+this._w*this._w)}normalize(){let e=this.length();return e===0?(this._x=0,this._y=0,this._z=0,this._w=1):(e=1/e,this._x=this._x*e,this._y=this._y*e,this._z=this._z*e,this._w=this._w*e),this._onChangeCallback(),this}multiply(e){return this.multiplyQuaternions(this,e)}premultiply(e){return this.multiplyQuaternions(e,this)}multiplyQuaternions(e,t){const i=e._x,a=e._y,r=e._z,s=e._w,o=t._x,c=t._y,l=t._z,u=t._w;return this._x=i*u+s*o+a*l-r*c,this._y=a*u+s*c+r*o-i*l,this._z=r*u+s*l+i*c-a*o,this._w=s*u-i*o-a*c-r*l,this._onChangeCallback(),this}slerp(e,t){if(t===0)return this;if(t===1)return this.copy(e);const i=this._x,a=this._y,r=this._z,s=this._w;let o=s*e._w+i*e._x+a*e._y+r*e._z;if(o<0?(this._w=-e._w,this._x=-e._x,this._y=-e._y,this._z=-e._z,o=-o):this.copy(e),o>=1)return this._w=s,this._x=i,this._y=a,this._z=r,this;const c=1-o*o;if(c<=Number.EPSILON){const m=1-t;return this._w=m*s+t*this._w,this._x=m*i+t*this._x,this._y=m*a+t*this._y,this._z=m*r+t*this._z,this.normalize(),this}const l=Math.sqrt(c),u=Math.atan2(l,o),h=Math.sin((1-t)*u)/l,f=Math.sin(t*u)/l;return this._w=s*h+this._w*f,this._x=i*h+this._x*f,this._y=a*h+this._y*f,this._z=r*h+this._z*f,this._onChangeCallback(),this}slerpQuaternions(e,t,i){return this.copy(e).slerp(t,i)}random(){const e=2*Math.PI*Math.random(),t=2*Math.PI*Math.random(),i=Math.random(),a=Math.sqrt(1-i),r=Math.sqrt(i);return this.set(a*Math.sin(e),a*Math.cos(e),r*Math.sin(t),r*Math.cos(t))}equals(e){return e._x===this._x&&e._y===this._y&&e._z===this._z&&e._w===this._w}fromArray(e,t=0){return this._x=e[t],this._y=e[t+1],this._z=e[t+2],this._w=e[t+3],this._onChangeCallback(),this}toArray(e=[],t=0){return e[t]=this._x,e[t+1]=this._y,e[t+2]=this._z,e[t+3]=this._w,e}fromBufferAttribute(e,t){return this._x=e.getX(t),this._y=e.getY(t),this._z=e.getZ(t),this._w=e.getW(t),this._onChangeCallback(),this}toJSON(){return this.toArray()}_onChange(e){return this._onChangeCallback=e,this}_onChangeCallback(){}*[Symbol.iterator](){yield this._x,yield this._y,yield this._z,yield this._w}}class F{constructor(e=0,t=0,i=0){F.prototype.isVector3=!0,this.x=e,this.y=t,this.z=i}set(e,t,i){return i===void 0&&(i=this.z),this.x=e,this.y=t,this.z=i,this}setScalar(e){return this.x=e,this.y=e,this.z=e,this}setX(e){return this.x=e,this}setY(e){return this.y=e,this}setZ(e){return this.z=e,this}setComponent(e,t){switch(e){case 0:this.x=t;break;case 1:this.y=t;break;case 2:this.z=t;break;default:throw new Error("index is out of range: "+e)}return this}getComponent(e){switch(e){case 0:return this.x;case 1:return this.y;case 2:return this.z;default:throw new Error("index is out of range: "+e)}}clone(){return new this.constructor(this.x,this.y,this.z)}copy(e){return this.x=e.x,this.y=e.y,this.z=e.z,this}add(e){return this.x+=e.x,this.y+=e.y,this.z+=e.z,this}addScalar(e){return this.x+=e,this.y+=e,this.z+=e,this}addVectors(e,t){return this.x=e.x+t.x,this.y=e.y+t.y,this.z=e.z+t.z,this}addScaledVector(e,t){return this.x+=e.x*t,this.y+=e.y*t,this.z+=e.z*t,this}sub(e){return this.x-=e.x,this.y-=e.y,this.z-=e.z,this}subScalar(e){return this.x-=e,this.y-=e,this.z-=e,this}subVectors(e,t){return this.x=e.x-t.x,this.y=e.y-t.y,this.z=e.z-t.z,this}multiply(e){return this.x*=e.x,this.y*=e.y,this.z*=e.z,this}multiplyScalar(e){return this.x*=e,this.y*=e,this.z*=e,this}multiplyVectors(e,t){return this.x=e.x*t.x,this.y=e.y*t.y,this.z=e.z*t.z,this}applyEuler(e){return this.applyQuaternion(po.setFromEuler(e))}applyAxisAngle(e,t){return this.applyQuaternion(po.setFromAxisAngle(e,t))}applyMatrix3(e){const t=this.x,i=this.y,a=this.z,r=e.elements;return this.x=r[0]*t+r[3]*i+r[6]*a,this.y=r[1]*t+r[4]*i+r[7]*a,this.z=r[2]*t+r[5]*i+r[8]*a,this}applyNormalMatrix(e){return this.applyMatrix3(e).normalize()}applyMatrix4(e){const t=this.x,i=this.y,a=this.z,r=e.elements,s=1/(r[3]*t+r[7]*i+r[11]*a+r[15]);return this.x=(r[0]*t+r[4]*i+r[8]*a+r[12])*s,this.y=(r[1]*t+r[5]*i+r[9]*a+r[13])*s,this.z=(r[2]*t+r[6]*i+r[10]*a+r[14])*s,this}applyQuaternion(e){const t=this.x,i=this.y,a=this.z,r=e.x,s=e.y,o=e.z,c=e.w,l=2*(s*a-o*i),u=2*(o*t-r*a),h=2*(r*i-s*t);return this.x=t+c*l+s*h-o*u,this.y=i+c*u+o*l-r*h,this.z=a+c*h+r*u-s*l,this}project(e){return this.applyMatrix4(e.matrixWorldInverse).applyMatrix4(e.projectionMatrix)}unproject(e){return this.applyMatrix4(e.projectionMatrixInverse).applyMatrix4(e.matrixWorld)}transformDirection(e){const t=this.x,i=this.y,a=this.z,r=e.elements;return this.x=r[0]*t+r[4]*i+r[8]*a,this.y=r[1]*t+r[5]*i+r[9]*a,this.z=r[2]*t+r[6]*i+r[10]*a,this.normalize()}divide(e){return this.x/=e.x,this.y/=e.y,this.z/=e.z,this}divideScalar(e){return this.multiplyScalar(1/e)}min(e){return this.x=Math.min(this.x,e.x),this.y=Math.min(this.y,e.y),this.z=Math.min(this.z,e.z),this}max(e){return this.x=Math.max(this.x,e.x),this.y=Math.max(this.y,e.y),this.z=Math.max(this.z,e.z),this}clamp(e,t){return this.x=Xe(this.x,e.x,t.x),this.y=Xe(this.y,e.y,t.y),this.z=Xe(this.z,e.z,t.z),this}clampScalar(e,t){return this.x=Xe(this.x,e,t),this.y=Xe(this.y,e,t),this.z=Xe(this.z,e,t),this}clampLength(e,t){const i=this.length();return this.divideScalar(i||1).multiplyScalar(Xe(i,e,t))}floor(){return this.x=Math.floor(this.x),this.y=Math.floor(this.y),this.z=Math.floor(this.z),this}ceil(){return this.x=Math.ceil(this.x),this.y=Math.ceil(this.y),this.z=Math.ceil(this.z),this}round(){return this.x=Math.round(this.x),this.y=Math.round(this.y),this.z=Math.round(this.z),this}roundToZero(){return this.x=Math.trunc(this.x),this.y=Math.trunc(this.y),this.z=Math.trunc(this.z),this}negate(){return this.x=-this.x,this.y=-this.y,this.z=-this.z,this}dot(e){return this.x*e.x+this.y*e.y+this.z*e.z}lengthSq(){return this.x*this.x+this.y*this.y+this.z*this.z}length(){return Math.sqrt(this.x*this.x+this.y*this.y+this.z*this.z)}manhattanLength(){return Math.abs(this.x)+Math.abs(this.y)+Math.abs(this.z)}normalize(){return this.divideScalar(this.length()||1)}setLength(e){return this.normalize().multiplyScalar(e)}lerp(e,t){return this.x+=(e.x-this.x)*t,this.y+=(e.y-this.y)*t,this.z+=(e.z-this.z)*t,this}lerpVectors(e,t,i){return this.x=e.x+(t.x-e.x)*i,this.y=e.y+(t.y-e.y)*i,this.z=e.z+(t.z-e.z)*i,this}cross(e){return this.crossVectors(this,e)}crossVectors(e,t){const i=e.x,a=e.y,r=e.z,s=t.x,o=t.y,c=t.z;return this.x=a*c-r*o,this.y=r*s-i*c,this.z=i*o-a*s,this}projectOnVector(e){const t=e.lengthSq();if(t===0)return this.set(0,0,0);const i=e.dot(this)/t;return this.copy(e).multiplyScalar(i)}projectOnPlane(e){return tr.copy(this).projectOnVector(e),this.sub(tr)}reflect(e){return this.sub(tr.copy(e).multiplyScalar(2*this.dot(e)))}angleTo(e){const t=Math.sqrt(this.lengthSq()*e.lengthSq());if(t===0)return Math.PI/2;const i=this.dot(e)/t;return Math.acos(Xe(i,-1,1))}distanceTo(e){return Math.sqrt(this.distanceToSquared(e))}distanceToSquared(e){const t=this.x-e.x,i=this.y-e.y,a=this.z-e.z;return t*t+i*i+a*a}manhattanDistanceTo(e){return Math.abs(this.x-e.x)+Math.abs(this.y-e.y)+Math.abs(this.z-e.z)}setFromSpherical(e){return this.setFromSphericalCoords(e.radius,e.phi,e.theta)}setFromSphericalCoords(e,t,i){const a=Math.sin(t)*e;return this.x=a*Math.sin(i),this.y=Math.cos(t)*e,this.z=a*Math.cos(i),this}setFromCylindrical(e){return this.setFromCylindricalCoords(e.radius,e.theta,e.y)}setFromCylindricalCoords(e,t,i){return this.x=e*Math.sin(t),this.y=i,this.z=e*Math.cos(t),this}setFromMatrixPosition(e){const t=e.elements;return this.x=t[12],this.y=t[13],this.z=t[14],this}setFromMatrixScale(e){const t=this.setFromMatrixColumn(e,0).length(),i=this.setFromMatrixColumn(e,1).length(),a=this.setFromMatrixColumn(e,2).length();return this.x=t,this.y=i,this.z=a,this}setFromMatrixColumn(e,t){return this.fromArray(e.elements,t*4)}setFromMatrix3Column(e,t){return this.fromArray(e.elements,t*3)}setFromEuler(e){return this.x=e._x,this.y=e._y,this.z=e._z,this}setFromColor(e){return this.x=e.r,this.y=e.g,this.z=e.b,this}equals(e){return e.x===this.x&&e.y===this.y&&e.z===this.z}fromArray(e,t=0){return this.x=e[t],this.y=e[t+1],this.z=e[t+2],this}toArray(e=[],t=0){return e[t]=this.x,e[t+1]=this.y,e[t+2]=this.z,e}fromBufferAttribute(e,t){return this.x=e.getX(t),this.y=e.getY(t),this.z=e.getZ(t),this}random(){return this.x=Math.random(),this.y=Math.random(),this.z=Math.random(),this}randomDirection(){const e=Math.random()*Math.PI*2,t=Math.random()*2-1,i=Math.sqrt(1-t*t);return this.x=i*Math.cos(e),this.y=t,this.z=i*Math.sin(e),this}*[Symbol.iterator](){yield this.x,yield this.y,yield this.z}}const tr=new F,po=new Ji;class Qi{constructor(e=new F(1/0,1/0,1/0),t=new F(-1/0,-1/0,-1/0)){this.isBox3=!0,this.min=e,this.max=t}set(e,t){return this.min.copy(e),this.max.copy(t),this}setFromArray(e){this.makeEmpty();for(let t=0,i=e.length;t<i;t+=3)this.expandByPoint(Kt.fromArray(e,t));return this}setFromBufferAttribute(e){this.makeEmpty();for(let t=0,i=e.count;t<i;t++)this.expandByPoint(Kt.fromBufferAttribute(e,t));return this}setFromPoints(e){this.makeEmpty();for(let t=0,i=e.length;t<i;t++)this.expandByPoint(e[t]);return this}setFromCenterAndSize(e,t){const i=Kt.copy(t).multiplyScalar(.5);return this.min.copy(e).sub(i),this.max.copy(e).add(i),this}setFromObject(e,t=!1){return this.makeEmpty(),this.expandByObject(e,t)}clone(){return new this.constructor().copy(this)}copy(e){return this.min.copy(e.min),this.max.copy(e.max),this}makeEmpty(){return this.min.x=this.min.y=this.min.z=1/0,this.max.x=this.max.y=this.max.z=-1/0,this}isEmpty(){return this.max.x<this.min.x||this.max.y<this.min.y||this.max.z<this.min.z}getCenter(e){return this.isEmpty()?e.set(0,0,0):e.addVectors(this.min,this.max).multiplyScalar(.5)}getSize(e){return this.isEmpty()?e.set(0,0,0):e.subVectors(this.max,this.min)}expandByPoint(e){return this.min.min(e),this.max.max(e),this}expandByVector(e){return this.min.sub(e),this.max.add(e),this}expandByScalar(e){return this.min.addScalar(-e),this.max.addScalar(e),this}expandByObject(e,t=!1){e.updateWorldMatrix(!1,!1);const i=e.geometry;if(i!==void 0){const r=i.getAttribute("position");if(t===!0&&r!==void 0&&e.isInstancedMesh!==!0)for(let s=0,o=r.count;s<o;s++)e.isMesh===!0?e.getVertexPosition(s,Kt):Kt.fromBufferAttribute(r,s),Kt.applyMatrix4(e.matrixWorld),this.expandByPoint(Kt);else e.boundingBox!==void 0?(e.boundingBox===null&&e.computeBoundingBox(),aa.copy(e.boundingBox)):(i.boundingBox===null&&i.computeBoundingBox(),aa.copy(i.boundingBox)),aa.applyMatrix4(e.matrixWorld),this.union(aa)}const a=e.children;for(let r=0,s=a.length;r<s;r++)this.expandByObject(a[r],t);return this}containsPoint(e){return e.x>=this.min.x&&e.x<=this.max.x&&e.y>=this.min.y&&e.y<=this.max.y&&e.z>=this.min.z&&e.z<=this.max.z}containsBox(e){return this.min.x<=e.min.x&&e.max.x<=this.max.x&&this.min.y<=e.min.y&&e.max.y<=this.max.y&&this.min.z<=e.min.z&&e.max.z<=this.max.z}getParameter(e,t){return t.set((e.x-this.min.x)/(this.max.x-this.min.x),(e.y-this.min.y)/(this.max.y-this.min.y),(e.z-this.min.z)/(this.max.z-this.min.z))}intersectsBox(e){return e.max.x>=this.min.x&&e.min.x<=this.max.x&&e.max.y>=this.min.y&&e.min.y<=this.max.y&&e.max.z>=this.min.z&&e.min.z<=this.max.z}intersectsSphere(e){return this.clampPoint(e.center,Kt),Kt.distanceToSquared(e.center)<=e.radius*e.radius}intersectsPlane(e){let t,i;return e.normal.x>0?(t=e.normal.x*this.min.x,i=e.normal.x*this.max.x):(t=e.normal.x*this.max.x,i=e.normal.x*this.min.x),e.normal.y>0?(t+=e.normal.y*this.min.y,i+=e.normal.y*this.max.y):(t+=e.normal.y*this.max.y,i+=e.normal.y*this.min.y),e.normal.z>0?(t+=e.normal.z*this.min.z,i+=e.normal.z*this.max.z):(t+=e.normal.z*this.max.z,i+=e.normal.z*this.min.z),t<=-e.constant&&i>=-e.constant}intersectsTriangle(e){if(this.isEmpty())return!1;this.getCenter(Oi),ra.subVectors(this.max,Oi),ri.subVectors(e.a,Oi),si.subVectors(e.b,Oi),oi.subVectors(e.c,Oi),xn.subVectors(si,ri),Mn.subVectors(oi,si),Nn.subVectors(ri,oi);let t=[0,-xn.z,xn.y,0,-Mn.z,Mn.y,0,-Nn.z,Nn.y,xn.z,0,-xn.x,Mn.z,0,-Mn.x,Nn.z,0,-Nn.x,-xn.y,xn.x,0,-Mn.y,Mn.x,0,-Nn.y,Nn.x,0];return!nr(t,ri,si,oi,ra)||(t=[1,0,0,0,1,0,0,0,1],!nr(t,ri,si,oi,ra))?!1:(sa.crossVectors(xn,Mn),t=[sa.x,sa.y,sa.z],nr(t,ri,si,oi,ra))}clampPoint(e,t){return t.copy(e).clamp(this.min,this.max)}distanceToPoint(e){return this.clampPoint(e,Kt).distanceTo(e)}getBoundingSphere(e){return this.isEmpty()?e.makeEmpty():(this.getCenter(e.center),e.radius=this.getSize(Kt).length()*.5),e}intersect(e){return this.min.max(e.min),this.max.min(e.max),this.isEmpty()&&this.makeEmpty(),this}union(e){return this.min.min(e.min),this.max.max(e.max),this}applyMatrix4(e){return this.isEmpty()?this:(an[0].set(this.min.x,this.min.y,this.min.z).applyMatrix4(e),an[1].set(this.min.x,this.min.y,this.max.z).applyMatrix4(e),an[2].set(this.min.x,this.max.y,this.min.z).applyMatrix4(e),an[3].set(this.min.x,this.max.y,this.max.z).applyMatrix4(e),an[4].set(this.max.x,this.min.y,this.min.z).applyMatrix4(e),an[5].set(this.max.x,this.min.y,this.max.z).applyMatrix4(e),an[6].set(this.max.x,this.max.y,this.min.z).applyMatrix4(e),an[7].set(this.max.x,this.max.y,this.max.z).applyMatrix4(e),this.setFromPoints(an),this)}translate(e){return this.min.add(e),this.max.add(e),this}equals(e){return e.min.equals(this.min)&&e.max.equals(this.max)}}const an=[new F,new F,new F,new F,new F,new F,new F,new F],Kt=new F,aa=new Qi,ri=new F,si=new F,oi=new F,xn=new F,Mn=new F,Nn=new F,Oi=new F,ra=new F,sa=new F,Fn=new F;function nr(n,e,t,i,a){for(let r=0,s=n.length-3;r<=s;r+=3){Fn.fromArray(n,r);const o=a.x*Math.abs(Fn.x)+a.y*Math.abs(Fn.y)+a.z*Math.abs(Fn.z),c=e.dot(Fn),l=t.dot(Fn),u=i.dot(Fn);if(Math.max(-Math.max(c,l,u),Math.min(c,l,u))>o)return!1}return!0}const vu=new Qi,Bi=new F,ir=new F;class Wa{constructor(e=new F,t=-1){this.isSphere=!0,this.center=e,this.radius=t}set(e,t){return this.center.copy(e),this.radius=t,this}setFromPoints(e,t){const i=this.center;t!==void 0?i.copy(t):vu.setFromPoints(e).getCenter(i);let a=0;for(let r=0,s=e.length;r<s;r++)a=Math.max(a,i.distanceToSquared(e[r]));return this.radius=Math.sqrt(a),this}copy(e){return this.center.copy(e.center),this.radius=e.radius,this}isEmpty(){return this.radius<0}makeEmpty(){return this.center.set(0,0,0),this.radius=-1,this}containsPoint(e){return e.distanceToSquared(this.center)<=this.radius*this.radius}distanceToPoint(e){return e.distanceTo(this.center)-this.radius}intersectsSphere(e){const t=this.radius+e.radius;return e.center.distanceToSquared(this.center)<=t*t}intersectsBox(e){return e.intersectsSphere(this)}intersectsPlane(e){return Math.abs(e.distanceToPoint(this.center))<=this.radius}clampPoint(e,t){const i=this.center.distanceToSquared(e);return t.copy(e),i>this.radius*this.radius&&(t.sub(this.center).normalize(),t.multiplyScalar(this.radius).add(this.center)),t}getBoundingBox(e){return this.isEmpty()?(e.makeEmpty(),e):(e.set(this.center,this.center),e.expandByScalar(this.radius),e)}applyMatrix4(e){return this.center.applyMatrix4(e),this.radius=this.radius*e.getMaxScaleOnAxis(),this}translate(e){return this.center.add(e),this}expandByPoint(e){if(this.isEmpty())return this.center.copy(e),this.radius=0,this;Bi.subVectors(e,this.center);const t=Bi.lengthSq();if(t>this.radius*this.radius){const i=Math.sqrt(t),a=(i-this.radius)*.5;this.center.addScaledVector(Bi,a/i),this.radius+=a}return this}union(e){return e.isEmpty()?this:this.isEmpty()?(this.copy(e),this):(this.center.equals(e.center)===!0?this.radius=Math.max(this.radius,e.radius):(ir.subVectors(e.center,this.center).setLength(e.radius),this.expandByPoint(Bi.copy(e.center).add(ir)),this.expandByPoint(Bi.copy(e.center).sub(ir))),this)}equals(e){return e.center.equals(this.center)&&e.radius===this.radius}clone(){return new this.constructor().copy(this)}}const rn=new F,ar=new F,oa=new F,Sn=new F,rr=new F,ca=new F,sr=new F;class Fs{constructor(e=new F,t=new F(0,0,-1)){this.origin=e,this.direction=t}set(e,t){return this.origin.copy(e),this.direction.copy(t),this}copy(e){return this.origin.copy(e.origin),this.direction.copy(e.direction),this}at(e,t){return t.copy(this.origin).addScaledVector(this.direction,e)}lookAt(e){return this.direction.copy(e).sub(this.origin).normalize(),this}recast(e){return this.origin.copy(this.at(e,rn)),this}closestPointToPoint(e,t){t.subVectors(e,this.origin);const i=t.dot(this.direction);return i<0?t.copy(this.origin):t.copy(this.origin).addScaledVector(this.direction,i)}distanceToPoint(e){return Math.sqrt(this.distanceSqToPoint(e))}distanceSqToPoint(e){const t=rn.subVectors(e,this.origin).dot(this.direction);return t<0?this.origin.distanceToSquared(e):(rn.copy(this.origin).addScaledVector(this.direction,t),rn.distanceToSquared(e))}distanceSqToSegment(e,t,i,a){ar.copy(e).add(t).multiplyScalar(.5),oa.copy(t).sub(e).normalize(),Sn.copy(this.origin).sub(ar);const r=e.distanceTo(t)*.5,s=-this.direction.dot(oa),o=Sn.dot(this.direction),c=-Sn.dot(oa),l=Sn.lengthSq(),u=Math.abs(1-s*s);let h,f,m,g;if(u>0)if(h=s*c-o,f=s*o-c,g=r*u,h>=0)if(f>=-g)if(f<=g){const _=1/u;h*=_,f*=_,m=h*(h+s*f+2*o)+f*(s*h+f+2*c)+l}else f=r,h=Math.max(0,-(s*f+o)),m=-h*h+f*(f+2*c)+l;else f=-r,h=Math.max(0,-(s*f+o)),m=-h*h+f*(f+2*c)+l;else f<=-g?(h=Math.max(0,-(-s*r+o)),f=h>0?-r:Math.min(Math.max(-r,-c),r),m=-h*h+f*(f+2*c)+l):f<=g?(h=0,f=Math.min(Math.max(-r,-c),r),m=f*(f+2*c)+l):(h=Math.max(0,-(s*r+o)),f=h>0?r:Math.min(Math.max(-r,-c),r),m=-h*h+f*(f+2*c)+l);else f=s>0?-r:r,h=Math.max(0,-(s*f+o)),m=-h*h+f*(f+2*c)+l;return i&&i.copy(this.origin).addScaledVector(this.direction,h),a&&a.copy(ar).addScaledVector(oa,f),m}intersectSphere(e,t){rn.subVectors(e.center,this.origin);const i=rn.dot(this.direction),a=rn.dot(rn)-i*i,r=e.radius*e.radius;if(a>r)return null;const s=Math.sqrt(r-a),o=i-s,c=i+s;return c<0?null:o<0?this.at(c,t):this.at(o,t)}intersectsSphere(e){return this.distanceSqToPoint(e.center)<=e.radius*e.radius}distanceToPlane(e){const t=e.normal.dot(this.direction);if(t===0)return e.distanceToPoint(this.origin)===0?0:null;const i=-(this.origin.dot(e.normal)+e.constant)/t;return i>=0?i:null}intersectPlane(e,t){const i=this.distanceToPlane(e);return i===null?null:this.at(i,t)}intersectsPlane(e){const t=e.distanceToPoint(this.origin);return t===0||e.normal.dot(this.direction)*t<0}intersectBox(e,t){let i,a,r,s,o,c;const l=1/this.direction.x,u=1/this.direction.y,h=1/this.direction.z,f=this.origin;return l>=0?(i=(e.min.x-f.x)*l,a=(e.max.x-f.x)*l):(i=(e.max.x-f.x)*l,a=(e.min.x-f.x)*l),u>=0?(r=(e.min.y-f.y)*u,s=(e.max.y-f.y)*u):(r=(e.max.y-f.y)*u,s=(e.min.y-f.y)*u),i>s||r>a||((r>i||isNaN(i))&&(i=r),(s<a||isNaN(a))&&(a=s),h>=0?(o=(e.min.z-f.z)*h,c=(e.max.z-f.z)*h):(o=(e.max.z-f.z)*h,c=(e.min.z-f.z)*h),i>c||o>a)||((o>i||i!==i)&&(i=o),(c<a||a!==a)&&(a=c),a<0)?null:this.at(i>=0?i:a,t)}intersectsBox(e){return this.intersectBox(e,rn)!==null}intersectTriangle(e,t,i,a,r){rr.subVectors(t,e),ca.subVectors(i,e),sr.crossVectors(rr,ca);let s=this.direction.dot(sr),o;if(s>0){if(a)return null;o=1}else if(s<0)o=-1,s=-s;else return null;Sn.subVectors(this.origin,e);const c=o*this.direction.dot(ca.crossVectors(Sn,ca));if(c<0)return null;const l=o*this.direction.dot(rr.cross(Sn));if(l<0||c+l>s)return null;const u=-o*Sn.dot(sr);return u<0?null:this.at(u/s,r)}applyMatrix4(e){return this.origin.applyMatrix4(e),this.direction.transformDirection(e),this}equals(e){return e.origin.equals(this.origin)&&e.direction.equals(this.direction)}clone(){return new this.constructor().copy(this)}}class st{constructor(e,t,i,a,r,s,o,c,l,u,h,f,m,g,_,p){st.prototype.isMatrix4=!0,this.elements=[1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1],e!==void 0&&this.set(e,t,i,a,r,s,o,c,l,u,h,f,m,g,_,p)}set(e,t,i,a,r,s,o,c,l,u,h,f,m,g,_,p){const d=this.elements;return d[0]=e,d[4]=t,d[8]=i,d[12]=a,d[1]=r,d[5]=s,d[9]=o,d[13]=c,d[2]=l,d[6]=u,d[10]=h,d[14]=f,d[3]=m,d[7]=g,d[11]=_,d[15]=p,this}identity(){return this.set(1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1),this}clone(){return new st().fromArray(this.elements)}copy(e){const t=this.elements,i=e.elements;return t[0]=i[0],t[1]=i[1],t[2]=i[2],t[3]=i[3],t[4]=i[4],t[5]=i[5],t[6]=i[6],t[7]=i[7],t[8]=i[8],t[9]=i[9],t[10]=i[10],t[11]=i[11],t[12]=i[12],t[13]=i[13],t[14]=i[14],t[15]=i[15],this}copyPosition(e){const t=this.elements,i=e.elements;return t[12]=i[12],t[13]=i[13],t[14]=i[14],this}setFromMatrix3(e){const t=e.elements;return this.set(t[0],t[3],t[6],0,t[1],t[4],t[7],0,t[2],t[5],t[8],0,0,0,0,1),this}extractBasis(e,t,i){return e.setFromMatrixColumn(this,0),t.setFromMatrixColumn(this,1),i.setFromMatrixColumn(this,2),this}makeBasis(e,t,i){return this.set(e.x,t.x,i.x,0,e.y,t.y,i.y,0,e.z,t.z,i.z,0,0,0,0,1),this}extractRotation(e){const t=this.elements,i=e.elements,a=1/ci.setFromMatrixColumn(e,0).length(),r=1/ci.setFromMatrixColumn(e,1).length(),s=1/ci.setFromMatrixColumn(e,2).length();return t[0]=i[0]*a,t[1]=i[1]*a,t[2]=i[2]*a,t[3]=0,t[4]=i[4]*r,t[5]=i[5]*r,t[6]=i[6]*r,t[7]=0,t[8]=i[8]*s,t[9]=i[9]*s,t[10]=i[10]*s,t[11]=0,t[12]=0,t[13]=0,t[14]=0,t[15]=1,this}makeRotationFromEuler(e){const t=this.elements,i=e.x,a=e.y,r=e.z,s=Math.cos(i),o=Math.sin(i),c=Math.cos(a),l=Math.sin(a),u=Math.cos(r),h=Math.sin(r);if(e.order==="XYZ"){const f=s*u,m=s*h,g=o*u,_=o*h;t[0]=c*u,t[4]=-c*h,t[8]=l,t[1]=m+g*l,t[5]=f-_*l,t[9]=-o*c,t[2]=_-f*l,t[6]=g+m*l,t[10]=s*c}else if(e.order==="YXZ"){const f=c*u,m=c*h,g=l*u,_=l*h;t[0]=f+_*o,t[4]=g*o-m,t[8]=s*l,t[1]=s*h,t[5]=s*u,t[9]=-o,t[2]=m*o-g,t[6]=_+f*o,t[10]=s*c}else if(e.order==="ZXY"){const f=c*u,m=c*h,g=l*u,_=l*h;t[0]=f-_*o,t[4]=-s*h,t[8]=g+m*o,t[1]=m+g*o,t[5]=s*u,t[9]=_-f*o,t[2]=-s*l,t[6]=o,t[10]=s*c}else if(e.order==="ZYX"){const f=s*u,m=s*h,g=o*u,_=o*h;t[0]=c*u,t[4]=g*l-m,t[8]=f*l+_,t[1]=c*h,t[5]=_*l+f,t[9]=m*l-g,t[2]=-l,t[6]=o*c,t[10]=s*c}else if(e.order==="YZX"){const f=s*c,m=s*l,g=o*c,_=o*l;t[0]=c*u,t[4]=_-f*h,t[8]=g*h+m,t[1]=h,t[5]=s*u,t[9]=-o*u,t[2]=-l*u,t[6]=m*h+g,t[10]=f-_*h}else if(e.order==="XZY"){const f=s*c,m=s*l,g=o*c,_=o*l;t[0]=c*u,t[4]=-h,t[8]=l*u,t[1]=f*h+_,t[5]=s*u,t[9]=m*h-g,t[2]=g*h-m,t[6]=o*u,t[10]=_*h+f}return t[3]=0,t[7]=0,t[11]=0,t[12]=0,t[13]=0,t[14]=0,t[15]=1,this}makeRotationFromQuaternion(e){return this.compose(xu,e,Mu)}lookAt(e,t,i){const a=this.elements;return kt.subVectors(e,t),kt.lengthSq()===0&&(kt.z=1),kt.normalize(),En.crossVectors(i,kt),En.lengthSq()===0&&(Math.abs(i.z)===1?kt.x+=1e-4:kt.z+=1e-4,kt.normalize(),En.crossVectors(i,kt)),En.normalize(),la.crossVectors(kt,En),a[0]=En.x,a[4]=la.x,a[8]=kt.x,a[1]=En.y,a[5]=la.y,a[9]=kt.y,a[2]=En.z,a[6]=la.z,a[10]=kt.z,this}multiply(e){return this.multiplyMatrices(this,e)}premultiply(e){return this.multiplyMatrices(e,this)}multiplyMatrices(e,t){const i=e.elements,a=t.elements,r=this.elements,s=i[0],o=i[4],c=i[8],l=i[12],u=i[1],h=i[5],f=i[9],m=i[13],g=i[2],_=i[6],p=i[10],d=i[14],E=i[3],S=i[7],x=i[11],T=i[15],y=a[0],w=a[4],D=a[8],M=a[12],v=a[1],R=a[5],U=a[9],C=a[13],P=a[2],N=a[6],k=a[10],O=a[14],z=a[3],H=a[7],$=a[11],Y=a[15];return r[0]=s*y+o*v+c*P+l*z,r[4]=s*w+o*R+c*N+l*H,r[8]=s*D+o*U+c*k+l*$,r[12]=s*M+o*C+c*O+l*Y,r[1]=u*y+h*v+f*P+m*z,r[5]=u*w+h*R+f*N+m*H,r[9]=u*D+h*U+f*k+m*$,r[13]=u*M+h*C+f*O+m*Y,r[2]=g*y+_*v+p*P+d*z,r[6]=g*w+_*R+p*N+d*H,r[10]=g*D+_*U+p*k+d*$,r[14]=g*M+_*C+p*O+d*Y,r[3]=E*y+S*v+x*P+T*z,r[7]=E*w+S*R+x*N+T*H,r[11]=E*D+S*U+x*k+T*$,r[15]=E*M+S*C+x*O+T*Y,this}multiplyScalar(e){const t=this.elements;return t[0]*=e,t[4]*=e,t[8]*=e,t[12]*=e,t[1]*=e,t[5]*=e,t[9]*=e,t[13]*=e,t[2]*=e,t[6]*=e,t[10]*=e,t[14]*=e,t[3]*=e,t[7]*=e,t[11]*=e,t[15]*=e,this}determinant(){const e=this.elements,t=e[0],i=e[4],a=e[8],r=e[12],s=e[1],o=e[5],c=e[9],l=e[13],u=e[2],h=e[6],f=e[10],m=e[14],g=e[3],_=e[7],p=e[11],d=e[15];return g*(+r*c*h-a*l*h-r*o*f+i*l*f+a*o*m-i*c*m)+_*(+t*c*m-t*l*f+r*s*f-a*s*m+a*l*u-r*c*u)+p*(+t*l*h-t*o*m-r*s*h+i*s*m+r*o*u-i*l*u)+d*(-a*o*u-t*c*h+t*o*f+a*s*h-i*s*f+i*c*u)}transpose(){const e=this.elements;let t;return t=e[1],e[1]=e[4],e[4]=t,t=e[2],e[2]=e[8],e[8]=t,t=e[6],e[6]=e[9],e[9]=t,t=e[3],e[3]=e[12],e[12]=t,t=e[7],e[7]=e[13],e[13]=t,t=e[11],e[11]=e[14],e[14]=t,this}setPosition(e,t,i){const a=this.elements;return e.isVector3?(a[12]=e.x,a[13]=e.y,a[14]=e.z):(a[12]=e,a[13]=t,a[14]=i),this}invert(){const e=this.elements,t=e[0],i=e[1],a=e[2],r=e[3],s=e[4],o=e[5],c=e[6],l=e[7],u=e[8],h=e[9],f=e[10],m=e[11],g=e[12],_=e[13],p=e[14],d=e[15],E=h*p*l-_*f*l+_*c*m-o*p*m-h*c*d+o*f*d,S=g*f*l-u*p*l-g*c*m+s*p*m+u*c*d-s*f*d,x=u*_*l-g*h*l+g*o*m-s*_*m-u*o*d+s*h*d,T=g*h*c-u*_*c-g*o*f+s*_*f+u*o*p-s*h*p,y=t*E+i*S+a*x+r*T;if(y===0)return this.set(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);const w=1/y;return e[0]=E*w,e[1]=(_*f*r-h*p*r-_*a*m+i*p*m+h*a*d-i*f*d)*w,e[2]=(o*p*r-_*c*r+_*a*l-i*p*l-o*a*d+i*c*d)*w,e[3]=(h*c*r-o*f*r-h*a*l+i*f*l+o*a*m-i*c*m)*w,e[4]=S*w,e[5]=(u*p*r-g*f*r+g*a*m-t*p*m-u*a*d+t*f*d)*w,e[6]=(g*c*r-s*p*r-g*a*l+t*p*l+s*a*d-t*c*d)*w,e[7]=(s*f*r-u*c*r+u*a*l-t*f*l-s*a*m+t*c*m)*w,e[8]=x*w,e[9]=(g*h*r-u*_*r-g*i*m+t*_*m+u*i*d-t*h*d)*w,e[10]=(s*_*r-g*o*r+g*i*l-t*_*l-s*i*d+t*o*d)*w,e[11]=(u*o*r-s*h*r-u*i*l+t*h*l+s*i*m-t*o*m)*w,e[12]=T*w,e[13]=(u*_*a-g*h*a+g*i*f-t*_*f-u*i*p+t*h*p)*w,e[14]=(g*o*a-s*_*a-g*i*c+t*_*c+s*i*p-t*o*p)*w,e[15]=(s*h*a-u*o*a+u*i*c-t*h*c-s*i*f+t*o*f)*w,this}scale(e){const t=this.elements,i=e.x,a=e.y,r=e.z;return t[0]*=i,t[4]*=a,t[8]*=r,t[1]*=i,t[5]*=a,t[9]*=r,t[2]*=i,t[6]*=a,t[10]*=r,t[3]*=i,t[7]*=a,t[11]*=r,this}getMaxScaleOnAxis(){const e=this.elements,t=e[0]*e[0]+e[1]*e[1]+e[2]*e[2],i=e[4]*e[4]+e[5]*e[5]+e[6]*e[6],a=e[8]*e[8]+e[9]*e[9]+e[10]*e[10];return Math.sqrt(Math.max(t,i,a))}makeTranslation(e,t,i){return e.isVector3?this.set(1,0,0,e.x,0,1,0,e.y,0,0,1,e.z,0,0,0,1):this.set(1,0,0,e,0,1,0,t,0,0,1,i,0,0,0,1),this}makeRotationX(e){const t=Math.cos(e),i=Math.sin(e);return this.set(1,0,0,0,0,t,-i,0,0,i,t,0,0,0,0,1),this}makeRotationY(e){const t=Math.cos(e),i=Math.sin(e);return this.set(t,0,i,0,0,1,0,0,-i,0,t,0,0,0,0,1),this}makeRotationZ(e){const t=Math.cos(e),i=Math.sin(e);return this.set(t,-i,0,0,i,t,0,0,0,0,1,0,0,0,0,1),this}makeRotationAxis(e,t){const i=Math.cos(t),a=Math.sin(t),r=1-i,s=e.x,o=e.y,c=e.z,l=r*s,u=r*o;return this.set(l*s+i,l*o-a*c,l*c+a*o,0,l*o+a*c,u*o+i,u*c-a*s,0,l*c-a*o,u*c+a*s,r*c*c+i,0,0,0,0,1),this}makeScale(e,t,i){return this.set(e,0,0,0,0,t,0,0,0,0,i,0,0,0,0,1),this}makeShear(e,t,i,a,r,s){return this.set(1,i,r,0,e,1,s,0,t,a,1,0,0,0,0,1),this}compose(e,t,i){const a=this.elements,r=t._x,s=t._y,o=t._z,c=t._w,l=r+r,u=s+s,h=o+o,f=r*l,m=r*u,g=r*h,_=s*u,p=s*h,d=o*h,E=c*l,S=c*u,x=c*h,T=i.x,y=i.y,w=i.z;return a[0]=(1-(_+d))*T,a[1]=(m+x)*T,a[2]=(g-S)*T,a[3]=0,a[4]=(m-x)*y,a[5]=(1-(f+d))*y,a[6]=(p+E)*y,a[7]=0,a[8]=(g+S)*w,a[9]=(p-E)*w,a[10]=(1-(f+_))*w,a[11]=0,a[12]=e.x,a[13]=e.y,a[14]=e.z,a[15]=1,this}decompose(e,t,i){const a=this.elements;let r=ci.set(a[0],a[1],a[2]).length();const s=ci.set(a[4],a[5],a[6]).length(),o=ci.set(a[8],a[9],a[10]).length();this.determinant()<0&&(r=-r),e.x=a[12],e.y=a[13],e.z=a[14],qt.copy(this);const l=1/r,u=1/s,h=1/o;return qt.elements[0]*=l,qt.elements[1]*=l,qt.elements[2]*=l,qt.elements[4]*=u,qt.elements[5]*=u,qt.elements[6]*=u,qt.elements[8]*=h,qt.elements[9]*=h,qt.elements[10]*=h,t.setFromRotationMatrix(qt),i.x=r,i.y=s,i.z=o,this}makePerspective(e,t,i,a,r,s,o=pn){const c=this.elements,l=2*r/(t-e),u=2*r/(i-a),h=(t+e)/(t-e),f=(i+a)/(i-a);let m,g;if(o===pn)m=-(s+r)/(s-r),g=-2*s*r/(s-r);else if(o===Oa)m=-s/(s-r),g=-s*r/(s-r);else throw new Error("THREE.Matrix4.makePerspective(): Invalid coordinate system: "+o);return c[0]=l,c[4]=0,c[8]=h,c[12]=0,c[1]=0,c[5]=u,c[9]=f,c[13]=0,c[2]=0,c[6]=0,c[10]=m,c[14]=g,c[3]=0,c[7]=0,c[11]=-1,c[15]=0,this}makeOrthographic(e,t,i,a,r,s,o=pn){const c=this.elements,l=1/(t-e),u=1/(i-a),h=1/(s-r),f=(t+e)*l,m=(i+a)*u;let g,_;if(o===pn)g=(s+r)*h,_=-2*h;else if(o===Oa)g=r*h,_=-1*h;else throw new Error("THREE.Matrix4.makeOrthographic(): Invalid coordinate system: "+o);return c[0]=2*l,c[4]=0,c[8]=0,c[12]=-f,c[1]=0,c[5]=2*u,c[9]=0,c[13]=-m,c[2]=0,c[6]=0,c[10]=_,c[14]=-g,c[3]=0,c[7]=0,c[11]=0,c[15]=1,this}equals(e){const t=this.elements,i=e.elements;for(let a=0;a<16;a++)if(t[a]!==i[a])return!1;return!0}fromArray(e,t=0){for(let i=0;i<16;i++)this.elements[i]=e[i+t];return this}toArray(e=[],t=0){const i=this.elements;return e[t]=i[0],e[t+1]=i[1],e[t+2]=i[2],e[t+3]=i[3],e[t+4]=i[4],e[t+5]=i[5],e[t+6]=i[6],e[t+7]=i[7],e[t+8]=i[8],e[t+9]=i[9],e[t+10]=i[10],e[t+11]=i[11],e[t+12]=i[12],e[t+13]=i[13],e[t+14]=i[14],e[t+15]=i[15],e}}const ci=new F,qt=new st,xu=new F(0,0,0),Mu=new F(1,1,1),En=new F,la=new F,kt=new F,mo=new st,go=new Ji;class Mt{constructor(e=0,t=0,i=0,a=Mt.DEFAULT_ORDER){this.isEuler=!0,this._x=e,this._y=t,this._z=i,this._order=a}get x(){return this._x}set x(e){this._x=e,this._onChangeCallback()}get y(){return this._y}set y(e){this._y=e,this._onChangeCallback()}get z(){return this._z}set z(e){this._z=e,this._onChangeCallback()}get order(){return this._order}set order(e){this._order=e,this._onChangeCallback()}set(e,t,i,a=this._order){return this._x=e,this._y=t,this._z=i,this._order=a,this._onChangeCallback(),this}clone(){return new this.constructor(this._x,this._y,this._z,this._order)}copy(e){return this._x=e._x,this._y=e._y,this._z=e._z,this._order=e._order,this._onChangeCallback(),this}setFromRotationMatrix(e,t=this._order,i=!0){const a=e.elements,r=a[0],s=a[4],o=a[8],c=a[1],l=a[5],u=a[9],h=a[2],f=a[6],m=a[10];switch(t){case"XYZ":this._y=Math.asin(Xe(o,-1,1)),Math.abs(o)<.9999999?(this._x=Math.atan2(-u,m),this._z=Math.atan2(-s,r)):(this._x=Math.atan2(f,l),this._z=0);break;case"YXZ":this._x=Math.asin(-Xe(u,-1,1)),Math.abs(u)<.9999999?(this._y=Math.atan2(o,m),this._z=Math.atan2(c,l)):(this._y=Math.atan2(-h,r),this._z=0);break;case"ZXY":this._x=Math.asin(Xe(f,-1,1)),Math.abs(f)<.9999999?(this._y=Math.atan2(-h,m),this._z=Math.atan2(-s,l)):(this._y=0,this._z=Math.atan2(c,r));break;case"ZYX":this._y=Math.asin(-Xe(h,-1,1)),Math.abs(h)<.9999999?(this._x=Math.atan2(f,m),this._z=Math.atan2(c,r)):(this._x=0,this._z=Math.atan2(-s,l));break;case"YZX":this._z=Math.asin(Xe(c,-1,1)),Math.abs(c)<.9999999?(this._x=Math.atan2(-u,l),this._y=Math.atan2(-h,r)):(this._x=0,this._y=Math.atan2(o,m));break;case"XZY":this._z=Math.asin(-Xe(s,-1,1)),Math.abs(s)<.9999999?(this._x=Math.atan2(f,l),this._y=Math.atan2(o,r)):(this._x=Math.atan2(-u,m),this._y=0);break;default:console.warn("THREE.Euler: .setFromRotationMatrix() encountered an unknown order: "+t)}return this._order=t,i===!0&&this._onChangeCallback(),this}setFromQuaternion(e,t,i){return mo.makeRotationFromQuaternion(e),this.setFromRotationMatrix(mo,t,i)}setFromVector3(e,t=this._order){return this.set(e.x,e.y,e.z,t)}reorder(e){return go.setFromEuler(this),this.setFromQuaternion(go,e)}equals(e){return e._x===this._x&&e._y===this._y&&e._z===this._z&&e._order===this._order}fromArray(e){return this._x=e[0],this._y=e[1],this._z=e[2],e[3]!==void 0&&(this._order=e[3]),this._onChangeCallback(),this}toArray(e=[],t=0){return e[t]=this._x,e[t+1]=this._y,e[t+2]=this._z,e[t+3]=this._order,e}_onChange(e){return this._onChangeCallback=e,this}_onChangeCallback(){}*[Symbol.iterator](){yield this._x,yield this._y,yield this._z,yield this._order}}Mt.DEFAULT_ORDER="XYZ";class Os{constructor(){this.mask=1}set(e){this.mask=(1<<e|0)>>>0}enable(e){this.mask|=1<<e|0}enableAll(){this.mask=-1}toggle(e){this.mask^=1<<e|0}disable(e){this.mask&=~(1<<e|0)}disableAll(){this.mask=0}test(e){return(this.mask&e.mask)!==0}isEnabled(e){return(this.mask&(1<<e|0))!==0}}let Su=0;const _o=new F,li=new Ji,sn=new st,ua=new F,Vi=new F,Eu=new F,bu=new Ji,vo=new F(1,0,0),xo=new F(0,1,0),Mo=new F(0,0,1),So={type:"added"},yu={type:"removed"},ui={type:"childadded",child:null},or={type:"childremoved",child:null};class Et extends Di{constructor(){super(),this.isObject3D=!0,Object.defineProperty(this,"id",{value:Su++}),this.uuid=Zi(),this.name="",this.type="Object3D",this.parent=null,this.children=[],this.up=Et.DEFAULT_UP.clone();const e=new F,t=new Mt,i=new Ji,a=new F(1,1,1);function r(){i.setFromEuler(t,!1)}function s(){t.setFromQuaternion(i,void 0,!1)}t._onChange(r),i._onChange(s),Object.defineProperties(this,{position:{configurable:!0,enumerable:!0,value:e},rotation:{configurable:!0,enumerable:!0,value:t},quaternion:{configurable:!0,enumerable:!0,value:i},scale:{configurable:!0,enumerable:!0,value:a},modelViewMatrix:{value:new st},normalMatrix:{value:new Be}}),this.matrix=new st,this.matrixWorld=new st,this.matrixAutoUpdate=Et.DEFAULT_MATRIX_AUTO_UPDATE,this.matrixWorldAutoUpdate=Et.DEFAULT_MATRIX_WORLD_AUTO_UPDATE,this.matrixWorldNeedsUpdate=!1,this.layers=new Os,this.visible=!0,this.castShadow=!1,this.receiveShadow=!1,this.frustumCulled=!0,this.renderOrder=0,this.animations=[],this.userData={}}onBeforeShadow(){}onAfterShadow(){}onBeforeRender(){}onAfterRender(){}applyMatrix4(e){this.matrixAutoUpdate&&this.updateMatrix(),this.matrix.premultiply(e),this.matrix.decompose(this.position,this.quaternion,this.scale)}applyQuaternion(e){return this.quaternion.premultiply(e),this}setRotationFromAxisAngle(e,t){this.quaternion.setFromAxisAngle(e,t)}setRotationFromEuler(e){this.quaternion.setFromEuler(e,!0)}setRotationFromMatrix(e){this.quaternion.setFromRotationMatrix(e)}setRotationFromQuaternion(e){this.quaternion.copy(e)}rotateOnAxis(e,t){return li.setFromAxisAngle(e,t),this.quaternion.multiply(li),this}rotateOnWorldAxis(e,t){return li.setFromAxisAngle(e,t),this.quaternion.premultiply(li),this}rotateX(e){return this.rotateOnAxis(vo,e)}rotateY(e){return this.rotateOnAxis(xo,e)}rotateZ(e){return this.rotateOnAxis(Mo,e)}translateOnAxis(e,t){return _o.copy(e).applyQuaternion(this.quaternion),this.position.add(_o.multiplyScalar(t)),this}translateX(e){return this.translateOnAxis(vo,e)}translateY(e){return this.translateOnAxis(xo,e)}translateZ(e){return this.translateOnAxis(Mo,e)}localToWorld(e){return this.updateWorldMatrix(!0,!1),e.applyMatrix4(this.matrixWorld)}worldToLocal(e){return this.updateWorldMatrix(!0,!1),e.applyMatrix4(sn.copy(this.matrixWorld).invert())}lookAt(e,t,i){e.isVector3?ua.copy(e):ua.set(e,t,i);const a=this.parent;this.updateWorldMatrix(!0,!1),Vi.setFromMatrixPosition(this.matrixWorld),this.isCamera||this.isLight?sn.lookAt(Vi,ua,this.up):sn.lookAt(ua,Vi,this.up),this.quaternion.setFromRotationMatrix(sn),a&&(sn.extractRotation(a.matrixWorld),li.setFromRotationMatrix(sn),this.quaternion.premultiply(li.invert()))}add(e){if(arguments.length>1){for(let t=0;t<arguments.length;t++)this.add(arguments[t]);return this}return e===this?(console.error("THREE.Object3D.add: object can't be added as a child of itself.",e),this):(e&&e.isObject3D?(e.removeFromParent(),e.parent=this,this.children.push(e),e.dispatchEvent(So),ui.child=e,this.dispatchEvent(ui),ui.child=null):console.error("THREE.Object3D.add: object not an instance of THREE.Object3D.",e),this)}remove(e){if(arguments.length>1){for(let i=0;i<arguments.length;i++)this.remove(arguments[i]);return this}const t=this.children.indexOf(e);return t!==-1&&(e.parent=null,this.children.splice(t,1),e.dispatchEvent(yu),or.child=e,this.dispatchEvent(or),or.child=null),this}removeFromParent(){const e=this.parent;return e!==null&&e.remove(this),this}clear(){return this.remove(...this.children)}attach(e){return this.updateWorldMatrix(!0,!1),sn.copy(this.matrixWorld).invert(),e.parent!==null&&(e.parent.updateWorldMatrix(!0,!1),sn.multiply(e.parent.matrixWorld)),e.applyMatrix4(sn),e.removeFromParent(),e.parent=this,this.children.push(e),e.updateWorldMatrix(!1,!0),e.dispatchEvent(So),ui.child=e,this.dispatchEvent(ui),ui.child=null,this}getObjectById(e){return this.getObjectByProperty("id",e)}getObjectByName(e){return this.getObjectByProperty("name",e)}getObjectByProperty(e,t){if(this[e]===t)return this;for(let i=0,a=this.children.length;i<a;i++){const s=this.children[i].getObjectByProperty(e,t);if(s!==void 0)return s}}getObjectsByProperty(e,t,i=[]){this[e]===t&&i.push(this);const a=this.children;for(let r=0,s=a.length;r<s;r++)a[r].getObjectsByProperty(e,t,i);return i}getWorldPosition(e){return this.updateWorldMatrix(!0,!1),e.setFromMatrixPosition(this.matrixWorld)}getWorldQuaternion(e){return this.updateWorldMatrix(!0,!1),this.matrixWorld.decompose(Vi,e,Eu),e}getWorldScale(e){return this.updateWorldMatrix(!0,!1),this.matrixWorld.decompose(Vi,bu,e),e}getWorldDirection(e){this.updateWorldMatrix(!0,!1);const t=this.matrixWorld.elements;return e.set(t[8],t[9],t[10]).normalize()}raycast(){}traverse(e){e(this);const t=this.children;for(let i=0,a=t.length;i<a;i++)t[i].traverse(e)}traverseVisible(e){if(this.visible===!1)return;e(this);const t=this.children;for(let i=0,a=t.length;i<a;i++)t[i].traverseVisible(e)}traverseAncestors(e){const t=this.parent;t!==null&&(e(t),t.traverseAncestors(e))}updateMatrix(){this.matrix.compose(this.position,this.quaternion,this.scale),this.matrixWorldNeedsUpdate=!0}updateMatrixWorld(e){this.matrixAutoUpdate&&this.updateMatrix(),(this.matrixWorldNeedsUpdate||e)&&(this.matrixWorldAutoUpdate===!0&&(this.parent===null?this.matrixWorld.copy(this.matrix):this.matrixWorld.multiplyMatrices(this.parent.matrixWorld,this.matrix)),this.matrixWorldNeedsUpdate=!1,e=!0);const t=this.children;for(let i=0,a=t.length;i<a;i++)t[i].updateMatrixWorld(e)}updateWorldMatrix(e,t){const i=this.parent;if(e===!0&&i!==null&&i.updateWorldMatrix(!0,!1),this.matrixAutoUpdate&&this.updateMatrix(),this.matrixWorldAutoUpdate===!0&&(this.parent===null?this.matrixWorld.copy(this.matrix):this.matrixWorld.multiplyMatrices(this.parent.matrixWorld,this.matrix)),t===!0){const a=this.children;for(let r=0,s=a.length;r<s;r++)a[r].updateWorldMatrix(!1,!0)}}toJSON(e){const t=e===void 0||typeof e=="string",i={};t&&(e={geometries:{},materials:{},textures:{},images:{},shapes:{},skeletons:{},animations:{},nodes:{}},i.metadata={version:4.6,type:"Object",generator:"Object3D.toJSON"});const a={};a.uuid=this.uuid,a.type=this.type,this.name!==""&&(a.name=this.name),this.castShadow===!0&&(a.castShadow=!0),this.receiveShadow===!0&&(a.receiveShadow=!0),this.visible===!1&&(a.visible=!1),this.frustumCulled===!1&&(a.frustumCulled=!1),this.renderOrder!==0&&(a.renderOrder=this.renderOrder),Object.keys(this.userData).length>0&&(a.userData=this.userData),a.layers=this.layers.mask,a.matrix=this.matrix.toArray(),a.up=this.up.toArray(),this.matrixAutoUpdate===!1&&(a.matrixAutoUpdate=!1),this.isInstancedMesh&&(a.type="InstancedMesh",a.count=this.count,a.instanceMatrix=this.instanceMatrix.toJSON(),this.instanceColor!==null&&(a.instanceColor=this.instanceColor.toJSON())),this.isBatchedMesh&&(a.type="BatchedMesh",a.perObjectFrustumCulled=this.perObjectFrustumCulled,a.sortObjects=this.sortObjects,a.drawRanges=this._drawRanges,a.reservedRanges=this._reservedRanges,a.visibility=this._visibility,a.active=this._active,a.bounds=this._bounds.map(o=>({boxInitialized:o.boxInitialized,boxMin:o.box.min.toArray(),boxMax:o.box.max.toArray(),sphereInitialized:o.sphereInitialized,sphereRadius:o.sphere.radius,sphereCenter:o.sphere.center.toArray()})),a.maxInstanceCount=this._maxInstanceCount,a.maxVertexCount=this._maxVertexCount,a.maxIndexCount=this._maxIndexCount,a.geometryInitialized=this._geometryInitialized,a.geometryCount=this._geometryCount,a.matricesTexture=this._matricesTexture.toJSON(e),this._colorsTexture!==null&&(a.colorsTexture=this._colorsTexture.toJSON(e)),this.boundingSphere!==null&&(a.boundingSphere={center:a.boundingSphere.center.toArray(),radius:a.boundingSphere.radius}),this.boundingBox!==null&&(a.boundingBox={min:a.boundingBox.min.toArray(),max:a.boundingBox.max.toArray()}));function r(o,c){return o[c.uuid]===void 0&&(o[c.uuid]=c.toJSON(e)),c.uuid}if(this.isScene)this.background&&(this.background.isColor?a.background=this.background.toJSON():this.background.isTexture&&(a.background=this.background.toJSON(e).uuid)),this.environment&&this.environment.isTexture&&this.environment.isRenderTargetTexture!==!0&&(a.environment=this.environment.toJSON(e).uuid);else if(this.isMesh||this.isLine||this.isPoints){a.geometry=r(e.geometries,this.geometry);const o=this.geometry.parameters;if(o!==void 0&&o.shapes!==void 0){const c=o.shapes;if(Array.isArray(c))for(let l=0,u=c.length;l<u;l++){const h=c[l];r(e.shapes,h)}else r(e.shapes,c)}}if(this.isSkinnedMesh&&(a.bindMode=this.bindMode,a.bindMatrix=this.bindMatrix.toArray(),this.skeleton!==void 0&&(r(e.skeletons,this.skeleton),a.skeleton=this.skeleton.uuid)),this.material!==void 0)if(Array.isArray(this.material)){const o=[];for(let c=0,l=this.material.length;c<l;c++)o.push(r(e.materials,this.material[c]));a.material=o}else a.material=r(e.materials,this.material);if(this.children.length>0){a.children=[];for(let o=0;o<this.children.length;o++)a.children.push(this.children[o].toJSON(e).object)}if(this.animations.length>0){a.animations=[];for(let o=0;o<this.animations.length;o++){const c=this.animations[o];a.animations.push(r(e.animations,c))}}if(t){const o=s(e.geometries),c=s(e.materials),l=s(e.textures),u=s(e.images),h=s(e.shapes),f=s(e.skeletons),m=s(e.animations),g=s(e.nodes);o.length>0&&(i.geometries=o),c.length>0&&(i.materials=c),l.length>0&&(i.textures=l),u.length>0&&(i.images=u),h.length>0&&(i.shapes=h),f.length>0&&(i.skeletons=f),m.length>0&&(i.animations=m),g.length>0&&(i.nodes=g)}return i.object=a,i;function s(o){const c=[];for(const l in o){const u=o[l];delete u.metadata,c.push(u)}return c}}clone(e){return new this.constructor().copy(this,e)}copy(e,t=!0){if(this.name=e.name,this.up.copy(e.up),this.position.copy(e.position),this.rotation.order=e.rotation.order,this.quaternion.copy(e.quaternion),this.scale.copy(e.scale),this.matrix.copy(e.matrix),this.matrixWorld.copy(e.matrixWorld),this.matrixAutoUpdate=e.matrixAutoUpdate,this.matrixWorldAutoUpdate=e.matrixWorldAutoUpdate,this.matrixWorldNeedsUpdate=e.matrixWorldNeedsUpdate,this.layers.mask=e.layers.mask,this.visible=e.visible,this.castShadow=e.castShadow,this.receiveShadow=e.receiveShadow,this.frustumCulled=e.frustumCulled,this.renderOrder=e.renderOrder,this.animations=e.animations.slice(),this.userData=JSON.parse(JSON.stringify(e.userData)),t===!0)for(let i=0;i<e.children.length;i++){const a=e.children[i];this.add(a.clone())}return this}}Et.DEFAULT_UP=new F(0,1,0);Et.DEFAULT_MATRIX_AUTO_UPDATE=!0;Et.DEFAULT_MATRIX_WORLD_AUTO_UPDATE=!0;const $t=new F,on=new F,cr=new F,cn=new F,di=new F,hi=new F,Eo=new F,lr=new F,ur=new F,dr=new F,hr=new dt,fr=new dt,pr=new dt;class Gt{constructor(e=new F,t=new F,i=new F){this.a=e,this.b=t,this.c=i}static getNormal(e,t,i,a){a.subVectors(i,t),$t.subVectors(e,t),a.cross($t);const r=a.lengthSq();return r>0?a.multiplyScalar(1/Math.sqrt(r)):a.set(0,0,0)}static getBarycoord(e,t,i,a,r){$t.subVectors(a,t),on.subVectors(i,t),cr.subVectors(e,t);const s=$t.dot($t),o=$t.dot(on),c=$t.dot(cr),l=on.dot(on),u=on.dot(cr),h=s*l-o*o;if(h===0)return r.set(0,0,0),null;const f=1/h,m=(l*c-o*u)*f,g=(s*u-o*c)*f;return r.set(1-m-g,g,m)}static containsPoint(e,t,i,a){return this.getBarycoord(e,t,i,a,cn)===null?!1:cn.x>=0&&cn.y>=0&&cn.x+cn.y<=1}static getInterpolation(e,t,i,a,r,s,o,c){return this.getBarycoord(e,t,i,a,cn)===null?(c.x=0,c.y=0,"z"in c&&(c.z=0),"w"in c&&(c.w=0),null):(c.setScalar(0),c.addScaledVector(r,cn.x),c.addScaledVector(s,cn.y),c.addScaledVector(o,cn.z),c)}static getInterpolatedAttribute(e,t,i,a,r,s){return hr.setScalar(0),fr.setScalar(0),pr.setScalar(0),hr.fromBufferAttribute(e,t),fr.fromBufferAttribute(e,i),pr.fromBufferAttribute(e,a),s.setScalar(0),s.addScaledVector(hr,r.x),s.addScaledVector(fr,r.y),s.addScaledVector(pr,r.z),s}static isFrontFacing(e,t,i,a){return $t.subVectors(i,t),on.subVectors(e,t),$t.cross(on).dot(a)<0}set(e,t,i){return this.a.copy(e),this.b.copy(t),this.c.copy(i),this}setFromPointsAndIndices(e,t,i,a){return this.a.copy(e[t]),this.b.copy(e[i]),this.c.copy(e[a]),this}setFromAttributeAndIndices(e,t,i,a){return this.a.fromBufferAttribute(e,t),this.b.fromBufferAttribute(e,i),this.c.fromBufferAttribute(e,a),this}clone(){return new this.constructor().copy(this)}copy(e){return this.a.copy(e.a),this.b.copy(e.b),this.c.copy(e.c),this}getArea(){return $t.subVectors(this.c,this.b),on.subVectors(this.a,this.b),$t.cross(on).length()*.5}getMidpoint(e){return e.addVectors(this.a,this.b).add(this.c).multiplyScalar(1/3)}getNormal(e){return Gt.getNormal(this.a,this.b,this.c,e)}getPlane(e){return e.setFromCoplanarPoints(this.a,this.b,this.c)}getBarycoord(e,t){return Gt.getBarycoord(e,this.a,this.b,this.c,t)}getInterpolation(e,t,i,a,r){return Gt.getInterpolation(e,this.a,this.b,this.c,t,i,a,r)}containsPoint(e){return Gt.containsPoint(e,this.a,this.b,this.c)}isFrontFacing(e){return Gt.isFrontFacing(this.a,this.b,this.c,e)}intersectsBox(e){return e.intersectsTriangle(this)}closestPointToPoint(e,t){const i=this.a,a=this.b,r=this.c;let s,o;di.subVectors(a,i),hi.subVectors(r,i),lr.subVectors(e,i);const c=di.dot(lr),l=hi.dot(lr);if(c<=0&&l<=0)return t.copy(i);ur.subVectors(e,a);const u=di.dot(ur),h=hi.dot(ur);if(u>=0&&h<=u)return t.copy(a);const f=c*h-u*l;if(f<=0&&c>=0&&u<=0)return s=c/(c-u),t.copy(i).addScaledVector(di,s);dr.subVectors(e,r);const m=di.dot(dr),g=hi.dot(dr);if(g>=0&&m<=g)return t.copy(r);const _=m*l-c*g;if(_<=0&&l>=0&&g<=0)return o=l/(l-g),t.copy(i).addScaledVector(hi,o);const p=u*g-m*h;if(p<=0&&h-u>=0&&m-g>=0)return Eo.subVectors(r,a),o=(h-u)/(h-u+(m-g)),t.copy(a).addScaledVector(Eo,o);const d=1/(p+_+f);return s=_*d,o=f*d,t.copy(i).addScaledVector(di,s).addScaledVector(hi,o)}equals(e){return e.a.equals(this.a)&&e.b.equals(this.b)&&e.c.equals(this.c)}}const Vc={aliceblue:15792383,antiquewhite:16444375,aqua:65535,aquamarine:8388564,azure:15794175,beige:16119260,bisque:16770244,black:0,blanchedalmond:16772045,blue:255,blueviolet:9055202,brown:10824234,burlywood:14596231,cadetblue:6266528,chartreuse:8388352,chocolate:13789470,coral:16744272,cornflowerblue:6591981,cornsilk:16775388,crimson:14423100,cyan:65535,darkblue:139,darkcyan:35723,darkgoldenrod:12092939,darkgray:11119017,darkgreen:25600,darkgrey:11119017,darkkhaki:12433259,darkmagenta:9109643,darkolivegreen:5597999,darkorange:16747520,darkorchid:10040012,darkred:9109504,darksalmon:15308410,darkseagreen:9419919,darkslateblue:4734347,darkslategray:3100495,darkslategrey:3100495,darkturquoise:52945,darkviolet:9699539,deeppink:16716947,deepskyblue:49151,dimgray:6908265,dimgrey:6908265,dodgerblue:2003199,firebrick:11674146,floralwhite:16775920,forestgreen:2263842,fuchsia:16711935,gainsboro:14474460,ghostwhite:16316671,gold:16766720,goldenrod:14329120,gray:8421504,green:32768,greenyellow:11403055,grey:8421504,honeydew:15794160,hotpink:16738740,indianred:13458524,indigo:4915330,ivory:16777200,khaki:15787660,lavender:15132410,lavenderblush:16773365,lawngreen:8190976,lemonchiffon:16775885,lightblue:11393254,lightcoral:15761536,lightcyan:14745599,lightgoldenrodyellow:16448210,lightgray:13882323,lightgreen:9498256,lightgrey:13882323,lightpink:16758465,lightsalmon:16752762,lightseagreen:2142890,lightskyblue:8900346,lightslategray:7833753,lightslategrey:7833753,lightsteelblue:11584734,lightyellow:16777184,lime:65280,limegreen:3329330,linen:16445670,magenta:16711935,maroon:8388608,mediumaquamarine:6737322,mediumblue:205,mediumorchid:12211667,mediumpurple:9662683,mediumseagreen:3978097,mediumslateblue:8087790,mediumspringgreen:64154,mediumturquoise:4772300,mediumvioletred:13047173,midnightblue:1644912,mintcream:16121850,mistyrose:16770273,moccasin:16770229,navajowhite:16768685,navy:128,oldlace:16643558,olive:8421376,olivedrab:7048739,orange:16753920,orangered:16729344,orchid:14315734,palegoldenrod:15657130,palegreen:10025880,paleturquoise:11529966,palevioletred:14381203,papayawhip:16773077,peachpuff:16767673,peru:13468991,pink:16761035,plum:14524637,powderblue:11591910,purple:8388736,rebeccapurple:6697881,red:16711680,rosybrown:12357519,royalblue:4286945,saddlebrown:9127187,salmon:16416882,sandybrown:16032864,seagreen:3050327,seashell:16774638,sienna:10506797,silver:12632256,skyblue:8900331,slateblue:6970061,slategray:7372944,slategrey:7372944,snow:16775930,springgreen:65407,steelblue:4620980,tan:13808780,teal:32896,thistle:14204888,tomato:16737095,turquoise:4251856,violet:15631086,wheat:16113331,white:16777215,whitesmoke:16119285,yellow:16776960,yellowgreen:10145074},bn={h:0,s:0,l:0},da={h:0,s:0,l:0};function mr(n,e,t){return t<0&&(t+=1),t>1&&(t-=1),t<1/6?n+(e-n)*6*t:t<1/2?e:t<2/3?n+(e-n)*6*(2/3-t):n}class ce{constructor(e,t,i){return this.isColor=!0,this.r=1,this.g=1,this.b=1,this.set(e,t,i)}set(e,t,i){if(t===void 0&&i===void 0){const a=e;a&&a.isColor?this.copy(a):typeof a=="number"?this.setHex(a):typeof a=="string"&&this.setStyle(a)}else this.setRGB(e,t,i);return this}setScalar(e){return this.r=e,this.g=e,this.b=e,this}setHex(e,t=Ft){return e=Math.floor(e),this.r=(e>>16&255)/255,this.g=(e>>8&255)/255,this.b=(e&255)/255,Qe.toWorkingColorSpace(this,t),this}setRGB(e,t,i,a=Qe.workingColorSpace){return this.r=e,this.g=t,this.b=i,Qe.toWorkingColorSpace(this,a),this}setHSL(e,t,i,a=Qe.workingColorSpace){if(e=ou(e,1),t=Xe(t,0,1),i=Xe(i,0,1),t===0)this.r=this.g=this.b=i;else{const r=i<=.5?i*(1+t):i+t-i*t,s=2*i-r;this.r=mr(s,r,e+1/3),this.g=mr(s,r,e),this.b=mr(s,r,e-1/3)}return Qe.toWorkingColorSpace(this,a),this}setStyle(e,t=Ft){function i(r){r!==void 0&&parseFloat(r)<1&&console.warn("THREE.Color: Alpha component of "+e+" will be ignored.")}let a;if(a=/^(\w+)\(([^\)]*)\)/.exec(e)){let r;const s=a[1],o=a[2];switch(s){case"rgb":case"rgba":if(r=/^\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*(?:,\s*(\d*\.?\d+)\s*)?$/.exec(o))return i(r[4]),this.setRGB(Math.min(255,parseInt(r[1],10))/255,Math.min(255,parseInt(r[2],10))/255,Math.min(255,parseInt(r[3],10))/255,t);if(r=/^\s*(\d+)\%\s*,\s*(\d+)\%\s*,\s*(\d+)\%\s*(?:,\s*(\d*\.?\d+)\s*)?$/.exec(o))return i(r[4]),this.setRGB(Math.min(100,parseInt(r[1],10))/100,Math.min(100,parseInt(r[2],10))/100,Math.min(100,parseInt(r[3],10))/100,t);break;case"hsl":case"hsla":if(r=/^\s*(\d*\.?\d+)\s*,\s*(\d*\.?\d+)\%\s*,\s*(\d*\.?\d+)\%\s*(?:,\s*(\d*\.?\d+)\s*)?$/.exec(o))return i(r[4]),this.setHSL(parseFloat(r[1])/360,parseFloat(r[2])/100,parseFloat(r[3])/100,t);break;default:console.warn("THREE.Color: Unknown color model "+e)}}else if(a=/^\#([A-Fa-f\d]+)$/.exec(e)){const r=a[1],s=r.length;if(s===3)return this.setRGB(parseInt(r.charAt(0),16)/15,parseInt(r.charAt(1),16)/15,parseInt(r.charAt(2),16)/15,t);if(s===6)return this.setHex(parseInt(r,16),t);console.warn("THREE.Color: Invalid hex color "+e)}else if(e&&e.length>0)return this.setColorName(e,t);return this}setColorName(e,t=Ft){const i=Vc[e.toLowerCase()];return i!==void 0?this.setHex(i,t):console.warn("THREE.Color: Unknown color "+e),this}clone(){return new this.constructor(this.r,this.g,this.b)}copy(e){return this.r=e.r,this.g=e.g,this.b=e.b,this}copySRGBToLinear(e){return this.r=gn(e.r),this.g=gn(e.g),this.b=gn(e.b),this}copyLinearToSRGB(e){return this.r=yi(e.r),this.g=yi(e.g),this.b=yi(e.b),this}convertSRGBToLinear(){return this.copySRGBToLinear(this),this}convertLinearToSRGB(){return this.copyLinearToSRGB(this),this}getHex(e=Ft){return Qe.fromWorkingColorSpace(Tt.copy(this),e),Math.round(Xe(Tt.r*255,0,255))*65536+Math.round(Xe(Tt.g*255,0,255))*256+Math.round(Xe(Tt.b*255,0,255))}getHexString(e=Ft){return("000000"+this.getHex(e).toString(16)).slice(-6)}getHSL(e,t=Qe.workingColorSpace){Qe.fromWorkingColorSpace(Tt.copy(this),t);const i=Tt.r,a=Tt.g,r=Tt.b,s=Math.max(i,a,r),o=Math.min(i,a,r);let c,l;const u=(o+s)/2;if(o===s)c=0,l=0;else{const h=s-o;switch(l=u<=.5?h/(s+o):h/(2-s-o),s){case i:c=(a-r)/h+(a<r?6:0);break;case a:c=(r-i)/h+2;break;case r:c=(i-a)/h+4;break}c/=6}return e.h=c,e.s=l,e.l=u,e}getRGB(e,t=Qe.workingColorSpace){return Qe.fromWorkingColorSpace(Tt.copy(this),t),e.r=Tt.r,e.g=Tt.g,e.b=Tt.b,e}getStyle(e=Ft){Qe.fromWorkingColorSpace(Tt.copy(this),e);const t=Tt.r,i=Tt.g,a=Tt.b;return e!==Ft?`color(${e} ${t.toFixed(3)} ${i.toFixed(3)} ${a.toFixed(3)})`:`rgb(${Math.round(t*255)},${Math.round(i*255)},${Math.round(a*255)})`}offsetHSL(e,t,i){return this.getHSL(bn),this.setHSL(bn.h+e,bn.s+t,bn.l+i)}add(e){return this.r+=e.r,this.g+=e.g,this.b+=e.b,this}addColors(e,t){return this.r=e.r+t.r,this.g=e.g+t.g,this.b=e.b+t.b,this}addScalar(e){return this.r+=e,this.g+=e,this.b+=e,this}sub(e){return this.r=Math.max(0,this.r-e.r),this.g=Math.max(0,this.g-e.g),this.b=Math.max(0,this.b-e.b),this}multiply(e){return this.r*=e.r,this.g*=e.g,this.b*=e.b,this}multiplyScalar(e){return this.r*=e,this.g*=e,this.b*=e,this}lerp(e,t){return this.r+=(e.r-this.r)*t,this.g+=(e.g-this.g)*t,this.b+=(e.b-this.b)*t,this}lerpColors(e,t,i){return this.r=e.r+(t.r-e.r)*i,this.g=e.g+(t.g-e.g)*i,this.b=e.b+(t.b-e.b)*i,this}lerpHSL(e,t){this.getHSL(bn),e.getHSL(da);const i=Ja(bn.h,da.h,t),a=Ja(bn.s,da.s,t),r=Ja(bn.l,da.l,t);return this.setHSL(i,a,r),this}setFromVector3(e){return this.r=e.x,this.g=e.y,this.b=e.z,this}applyMatrix3(e){const t=this.r,i=this.g,a=this.b,r=e.elements;return this.r=r[0]*t+r[3]*i+r[6]*a,this.g=r[1]*t+r[4]*i+r[7]*a,this.b=r[2]*t+r[5]*i+r[8]*a,this}equals(e){return e.r===this.r&&e.g===this.g&&e.b===this.b}fromArray(e,t=0){return this.r=e[t],this.g=e[t+1],this.b=e[t+2],this}toArray(e=[],t=0){return e[t]=this.r,e[t+1]=this.g,e[t+2]=this.b,e}fromBufferAttribute(e,t){return this.r=e.getX(t),this.g=e.getY(t),this.b=e.getZ(t),this}toJSON(){return this.getHex()}*[Symbol.iterator](){yield this.r,yield this.g,yield this.b}}const Tt=new ce;ce.NAMES=Vc;let Tu=0;class Li extends Di{constructor(){super(),this.isMaterial=!0,Object.defineProperty(this,"id",{value:Tu++}),this.uuid=Zi(),this.name="",this.type="Material",this.blending=Ei,this.side=Ln,this.vertexColors=!1,this.opacity=1,this.transparent=!1,this.alphaHash=!1,this.blendSrc=zr,this.blendDst=kr,this.blendEquation=qn,this.blendSrcAlpha=null,this.blendDstAlpha=null,this.blendEquationAlpha=null,this.blendColor=new ce(0,0,0),this.blendAlpha=0,this.depthFunc=Ti,this.depthTest=!0,this.depthWrite=!0,this.stencilWriteMask=255,this.stencilFunc=oo,this.stencilRef=0,this.stencilFuncMask=255,this.stencilFail=ii,this.stencilZFail=ii,this.stencilZPass=ii,this.stencilWrite=!1,this.clippingPlanes=null,this.clipIntersection=!1,this.clipShadows=!1,this.shadowSide=null,this.colorWrite=!0,this.precision=null,this.polygonOffset=!1,this.polygonOffsetFactor=0,this.polygonOffsetUnits=0,this.dithering=!1,this.alphaToCoverage=!1,this.premultipliedAlpha=!1,this.forceSinglePass=!1,this.visible=!0,this.toneMapped=!0,this.userData={},this.version=0,this._alphaTest=0}get alphaTest(){return this._alphaTest}set alphaTest(e){this._alphaTest>0!=e>0&&this.version++,this._alphaTest=e}onBeforeRender(){}onBeforeCompile(){}customProgramCacheKey(){return this.onBeforeCompile.toString()}setValues(e){if(e!==void 0)for(const t in e){const i=e[t];if(i===void 0){console.warn(`THREE.Material: parameter '${t}' has value of undefined.`);continue}const a=this[t];if(a===void 0){console.warn(`THREE.Material: '${t}' is not a property of THREE.${this.type}.`);continue}a&&a.isColor?a.set(i):a&&a.isVector3&&i&&i.isVector3?a.copy(i):this[t]=i}}toJSON(e){const t=e===void 0||typeof e=="string";t&&(e={textures:{},images:{}});const i={metadata:{version:4.6,type:"Material",generator:"Material.toJSON"}};i.uuid=this.uuid,i.type=this.type,this.name!==""&&(i.name=this.name),this.color&&this.color.isColor&&(i.color=this.color.getHex()),this.roughness!==void 0&&(i.roughness=this.roughness),this.metalness!==void 0&&(i.metalness=this.metalness),this.sheen!==void 0&&(i.sheen=this.sheen),this.sheenColor&&this.sheenColor.isColor&&(i.sheenColor=this.sheenColor.getHex()),this.sheenRoughness!==void 0&&(i.sheenRoughness=this.sheenRoughness),this.emissive&&this.emissive.isColor&&(i.emissive=this.emissive.getHex()),this.emissiveIntensity!==void 0&&this.emissiveIntensity!==1&&(i.emissiveIntensity=this.emissiveIntensity),this.specular&&this.specular.isColor&&(i.specular=this.specular.getHex()),this.specularIntensity!==void 0&&(i.specularIntensity=this.specularIntensity),this.specularColor&&this.specularColor.isColor&&(i.specularColor=this.specularColor.getHex()),this.shininess!==void 0&&(i.shininess=this.shininess),this.clearcoat!==void 0&&(i.clearcoat=this.clearcoat),this.clearcoatRoughness!==void 0&&(i.clearcoatRoughness=this.clearcoatRoughness),this.clearcoatMap&&this.clearcoatMap.isTexture&&(i.clearcoatMap=this.clearcoatMap.toJSON(e).uuid),this.clearcoatRoughnessMap&&this.clearcoatRoughnessMap.isTexture&&(i.clearcoatRoughnessMap=this.clearcoatRoughnessMap.toJSON(e).uuid),this.clearcoatNormalMap&&this.clearcoatNormalMap.isTexture&&(i.clearcoatNormalMap=this.clearcoatNormalMap.toJSON(e).uuid,i.clearcoatNormalScale=this.clearcoatNormalScale.toArray()),this.dispersion!==void 0&&(i.dispersion=this.dispersion),this.iridescence!==void 0&&(i.iridescence=this.iridescence),this.iridescenceIOR!==void 0&&(i.iridescenceIOR=this.iridescenceIOR),this.iridescenceThicknessRange!==void 0&&(i.iridescenceThicknessRange=this.iridescenceThicknessRange),this.iridescenceMap&&this.iridescenceMap.isTexture&&(i.iridescenceMap=this.iridescenceMap.toJSON(e).uuid),this.iridescenceThicknessMap&&this.iridescenceThicknessMap.isTexture&&(i.iridescenceThicknessMap=this.iridescenceThicknessMap.toJSON(e).uuid),this.anisotropy!==void 0&&(i.anisotropy=this.anisotropy),this.anisotropyRotation!==void 0&&(i.anisotropyRotation=this.anisotropyRotation),this.anisotropyMap&&this.anisotropyMap.isTexture&&(i.anisotropyMap=this.anisotropyMap.toJSON(e).uuid),this.map&&this.map.isTexture&&(i.map=this.map.toJSON(e).uuid),this.matcap&&this.matcap.isTexture&&(i.matcap=this.matcap.toJSON(e).uuid),this.alphaMap&&this.alphaMap.isTexture&&(i.alphaMap=this.alphaMap.toJSON(e).uuid),this.lightMap&&this.lightMap.isTexture&&(i.lightMap=this.lightMap.toJSON(e).uuid,i.lightMapIntensity=this.lightMapIntensity),this.aoMap&&this.aoMap.isTexture&&(i.aoMap=this.aoMap.toJSON(e).uuid,i.aoMapIntensity=this.aoMapIntensity),this.bumpMap&&this.bumpMap.isTexture&&(i.bumpMap=this.bumpMap.toJSON(e).uuid,i.bumpScale=this.bumpScale),this.normalMap&&this.normalMap.isTexture&&(i.normalMap=this.normalMap.toJSON(e).uuid,i.normalMapType=this.normalMapType,i.normalScale=this.normalScale.toArray()),this.displacementMap&&this.displacementMap.isTexture&&(i.displacementMap=this.displacementMap.toJSON(e).uuid,i.displacementScale=this.displacementScale,i.displacementBias=this.displacementBias),this.roughnessMap&&this.roughnessMap.isTexture&&(i.roughnessMap=this.roughnessMap.toJSON(e).uuid),this.metalnessMap&&this.metalnessMap.isTexture&&(i.metalnessMap=this.metalnessMap.toJSON(e).uuid),this.emissiveMap&&this.emissiveMap.isTexture&&(i.emissiveMap=this.emissiveMap.toJSON(e).uuid),this.specularMap&&this.specularMap.isTexture&&(i.specularMap=this.specularMap.toJSON(e).uuid),this.specularIntensityMap&&this.specularIntensityMap.isTexture&&(i.specularIntensityMap=this.specularIntensityMap.toJSON(e).uuid),this.specularColorMap&&this.specularColorMap.isTexture&&(i.specularColorMap=this.specularColorMap.toJSON(e).uuid),this.envMap&&this.envMap.isTexture&&(i.envMap=this.envMap.toJSON(e).uuid,this.combine!==void 0&&(i.combine=this.combine)),this.envMapRotation!==void 0&&(i.envMapRotation=this.envMapRotation.toArray()),this.envMapIntensity!==void 0&&(i.envMapIntensity=this.envMapIntensity),this.reflectivity!==void 0&&(i.reflectivity=this.reflectivity),this.refractionRatio!==void 0&&(i.refractionRatio=this.refractionRatio),this.gradientMap&&this.gradientMap.isTexture&&(i.gradientMap=this.gradientMap.toJSON(e).uuid),this.transmission!==void 0&&(i.transmission=this.transmission),this.transmissionMap&&this.transmissionMap.isTexture&&(i.transmissionMap=this.transmissionMap.toJSON(e).uuid),this.thickness!==void 0&&(i.thickness=this.thickness),this.thicknessMap&&this.thicknessMap.isTexture&&(i.thicknessMap=this.thicknessMap.toJSON(e).uuid),this.attenuationDistance!==void 0&&this.attenuationDistance!==1/0&&(i.attenuationDistance=this.attenuationDistance),this.attenuationColor!==void 0&&(i.attenuationColor=this.attenuationColor.getHex()),this.size!==void 0&&(i.size=this.size),this.shadowSide!==null&&(i.shadowSide=this.shadowSide),this.sizeAttenuation!==void 0&&(i.sizeAttenuation=this.sizeAttenuation),this.blending!==Ei&&(i.blending=this.blending),this.side!==Ln&&(i.side=this.side),this.vertexColors===!0&&(i.vertexColors=!0),this.opacity<1&&(i.opacity=this.opacity),this.transparent===!0&&(i.transparent=!0),this.blendSrc!==zr&&(i.blendSrc=this.blendSrc),this.blendDst!==kr&&(i.blendDst=this.blendDst),this.blendEquation!==qn&&(i.blendEquation=this.blendEquation),this.blendSrcAlpha!==null&&(i.blendSrcAlpha=this.blendSrcAlpha),this.blendDstAlpha!==null&&(i.blendDstAlpha=this.blendDstAlpha),this.blendEquationAlpha!==null&&(i.blendEquationAlpha=this.blendEquationAlpha),this.blendColor&&this.blendColor.isColor&&(i.blendColor=this.blendColor.getHex()),this.blendAlpha!==0&&(i.blendAlpha=this.blendAlpha),this.depthFunc!==Ti&&(i.depthFunc=this.depthFunc),this.depthTest===!1&&(i.depthTest=this.depthTest),this.depthWrite===!1&&(i.depthWrite=this.depthWrite),this.colorWrite===!1&&(i.colorWrite=this.colorWrite),this.stencilWriteMask!==255&&(i.stencilWriteMask=this.stencilWriteMask),this.stencilFunc!==oo&&(i.stencilFunc=this.stencilFunc),this.stencilRef!==0&&(i.stencilRef=this.stencilRef),this.stencilFuncMask!==255&&(i.stencilFuncMask=this.stencilFuncMask),this.stencilFail!==ii&&(i.stencilFail=this.stencilFail),this.stencilZFail!==ii&&(i.stencilZFail=this.stencilZFail),this.stencilZPass!==ii&&(i.stencilZPass=this.stencilZPass),this.stencilWrite===!0&&(i.stencilWrite=this.stencilWrite),this.rotation!==void 0&&this.rotation!==0&&(i.rotation=this.rotation),this.polygonOffset===!0&&(i.polygonOffset=!0),this.polygonOffsetFactor!==0&&(i.polygonOffsetFactor=this.polygonOffsetFactor),this.polygonOffsetUnits!==0&&(i.polygonOffsetUnits=this.polygonOffsetUnits),this.linewidth!==void 0&&this.linewidth!==1&&(i.linewidth=this.linewidth),this.dashSize!==void 0&&(i.dashSize=this.dashSize),this.gapSize!==void 0&&(i.gapSize=this.gapSize),this.scale!==void 0&&(i.scale=this.scale),this.dithering===!0&&(i.dithering=!0),this.alphaTest>0&&(i.alphaTest=this.alphaTest),this.alphaHash===!0&&(i.alphaHash=!0),this.alphaToCoverage===!0&&(i.alphaToCoverage=!0),this.premultipliedAlpha===!0&&(i.premultipliedAlpha=!0),this.forceSinglePass===!0&&(i.forceSinglePass=!0),this.wireframe===!0&&(i.wireframe=!0),this.wireframeLinewidth>1&&(i.wireframeLinewidth=this.wireframeLinewidth),this.wireframeLinecap!=="round"&&(i.wireframeLinecap=this.wireframeLinecap),this.wireframeLinejoin!=="round"&&(i.wireframeLinejoin=this.wireframeLinejoin),this.flatShading===!0&&(i.flatShading=!0),this.visible===!1&&(i.visible=!1),this.toneMapped===!1&&(i.toneMapped=!1),this.fog===!1&&(i.fog=!1),Object.keys(this.userData).length>0&&(i.userData=this.userData);function a(r){const s=[];for(const o in r){const c=r[o];delete c.metadata,s.push(c)}return s}if(t){const r=a(e.textures),s=a(e.images);r.length>0&&(i.textures=r),s.length>0&&(i.images=s)}return i}clone(){return new this.constructor().copy(this)}copy(e){this.name=e.name,this.blending=e.blending,this.side=e.side,this.vertexColors=e.vertexColors,this.opacity=e.opacity,this.transparent=e.transparent,this.blendSrc=e.blendSrc,this.blendDst=e.blendDst,this.blendEquation=e.blendEquation,this.blendSrcAlpha=e.blendSrcAlpha,this.blendDstAlpha=e.blendDstAlpha,this.blendEquationAlpha=e.blendEquationAlpha,this.blendColor.copy(e.blendColor),this.blendAlpha=e.blendAlpha,this.depthFunc=e.depthFunc,this.depthTest=e.depthTest,this.depthWrite=e.depthWrite,this.stencilWriteMask=e.stencilWriteMask,this.stencilFunc=e.stencilFunc,this.stencilRef=e.stencilRef,this.stencilFuncMask=e.stencilFuncMask,this.stencilFail=e.stencilFail,this.stencilZFail=e.stencilZFail,this.stencilZPass=e.stencilZPass,this.stencilWrite=e.stencilWrite;const t=e.clippingPlanes;let i=null;if(t!==null){const a=t.length;i=new Array(a);for(let r=0;r!==a;++r)i[r]=t[r].clone()}return this.clippingPlanes=i,this.clipIntersection=e.clipIntersection,this.clipShadows=e.clipShadows,this.shadowSide=e.shadowSide,this.colorWrite=e.colorWrite,this.precision=e.precision,this.polygonOffset=e.polygonOffset,this.polygonOffsetFactor=e.polygonOffsetFactor,this.polygonOffsetUnits=e.polygonOffsetUnits,this.dithering=e.dithering,this.alphaTest=e.alphaTest,this.alphaHash=e.alphaHash,this.alphaToCoverage=e.alphaToCoverage,this.premultipliedAlpha=e.premultipliedAlpha,this.forceSinglePass=e.forceSinglePass,this.visible=e.visible,this.toneMapped=e.toneMapped,this.userData=JSON.parse(JSON.stringify(e.userData)),this}dispose(){this.dispatchEvent({type:"dispose"})}set needsUpdate(e){e===!0&&this.version++}onBuild(){console.warn("Material: onBuild() has been removed.")}}class Ui extends Li{constructor(e){super(),this.isMeshBasicMaterial=!0,this.type="MeshBasicMaterial",this.color=new ce(16777215),this.map=null,this.lightMap=null,this.lightMapIntensity=1,this.aoMap=null,this.aoMapIntensity=1,this.specularMap=null,this.alphaMap=null,this.envMap=null,this.envMapRotation=new Mt,this.combine=Tc,this.reflectivity=1,this.refractionRatio=.98,this.wireframe=!1,this.wireframeLinewidth=1,this.wireframeLinecap="round",this.wireframeLinejoin="round",this.fog=!0,this.setValues(e)}copy(e){return super.copy(e),this.color.copy(e.color),this.map=e.map,this.lightMap=e.lightMap,this.lightMapIntensity=e.lightMapIntensity,this.aoMap=e.aoMap,this.aoMapIntensity=e.aoMapIntensity,this.specularMap=e.specularMap,this.alphaMap=e.alphaMap,this.envMap=e.envMap,this.envMapRotation.copy(e.envMapRotation),this.combine=e.combine,this.reflectivity=e.reflectivity,this.refractionRatio=e.refractionRatio,this.wireframe=e.wireframe,this.wireframeLinewidth=e.wireframeLinewidth,this.wireframeLinecap=e.wireframeLinecap,this.wireframeLinejoin=e.wireframeLinejoin,this.fog=e.fog,this}}const pt=new F,ha=new Ke;let Au=0;class tn{constructor(e,t,i=!1){if(Array.isArray(e))throw new TypeError("THREE.BufferAttribute: array should be a Typed Array.");this.isBufferAttribute=!0,Object.defineProperty(this,"id",{value:Au++}),this.name="",this.array=e,this.itemSize=t,this.count=e!==void 0?e.length/t:0,this.normalized=i,this.usage=co,this.updateRanges=[],this.gpuType=fn,this.version=0}onUploadCallback(){}set needsUpdate(e){e===!0&&this.version++}setUsage(e){return this.usage=e,this}addUpdateRange(e,t){this.updateRanges.push({start:e,count:t})}clearUpdateRanges(){this.updateRanges.length=0}copy(e){return this.name=e.name,this.array=new e.array.constructor(e.array),this.itemSize=e.itemSize,this.count=e.count,this.normalized=e.normalized,this.usage=e.usage,this.gpuType=e.gpuType,this}copyAt(e,t,i){e*=this.itemSize,i*=t.itemSize;for(let a=0,r=this.itemSize;a<r;a++)this.array[e+a]=t.array[i+a];return this}copyArray(e){return this.array.set(e),this}applyMatrix3(e){if(this.itemSize===2)for(let t=0,i=this.count;t<i;t++)ha.fromBufferAttribute(this,t),ha.applyMatrix3(e),this.setXY(t,ha.x,ha.y);else if(this.itemSize===3)for(let t=0,i=this.count;t<i;t++)pt.fromBufferAttribute(this,t),pt.applyMatrix3(e),this.setXYZ(t,pt.x,pt.y,pt.z);return this}applyMatrix4(e){for(let t=0,i=this.count;t<i;t++)pt.fromBufferAttribute(this,t),pt.applyMatrix4(e),this.setXYZ(t,pt.x,pt.y,pt.z);return this}applyNormalMatrix(e){for(let t=0,i=this.count;t<i;t++)pt.fromBufferAttribute(this,t),pt.applyNormalMatrix(e),this.setXYZ(t,pt.x,pt.y,pt.z);return this}transformDirection(e){for(let t=0,i=this.count;t<i;t++)pt.fromBufferAttribute(this,t),pt.transformDirection(e),this.setXYZ(t,pt.x,pt.y,pt.z);return this}set(e,t=0){return this.array.set(e,t),this}getComponent(e,t){let i=this.array[e*this.itemSize+t];return this.normalized&&(i=Fi(i,this.array)),i}setComponent(e,t,i){return this.normalized&&(i=It(i,this.array)),this.array[e*this.itemSize+t]=i,this}getX(e){let t=this.array[e*this.itemSize];return this.normalized&&(t=Fi(t,this.array)),t}setX(e,t){return this.normalized&&(t=It(t,this.array)),this.array[e*this.itemSize]=t,this}getY(e){let t=this.array[e*this.itemSize+1];return this.normalized&&(t=Fi(t,this.array)),t}setY(e,t){return this.normalized&&(t=It(t,this.array)),this.array[e*this.itemSize+1]=t,this}getZ(e){let t=this.array[e*this.itemSize+2];return this.normalized&&(t=Fi(t,this.array)),t}setZ(e,t){return this.normalized&&(t=It(t,this.array)),this.array[e*this.itemSize+2]=t,this}getW(e){let t=this.array[e*this.itemSize+3];return this.normalized&&(t=Fi(t,this.array)),t}setW(e,t){return this.normalized&&(t=It(t,this.array)),this.array[e*this.itemSize+3]=t,this}setXY(e,t,i){return e*=this.itemSize,this.normalized&&(t=It(t,this.array),i=It(i,this.array)),this.array[e+0]=t,this.array[e+1]=i,this}setXYZ(e,t,i,a){return e*=this.itemSize,this.normalized&&(t=It(t,this.array),i=It(i,this.array),a=It(a,this.array)),this.array[e+0]=t,this.array[e+1]=i,this.array[e+2]=a,this}setXYZW(e,t,i,a,r){return e*=this.itemSize,this.normalized&&(t=It(t,this.array),i=It(i,this.array),a=It(a,this.array),r=It(r,this.array)),this.array[e+0]=t,this.array[e+1]=i,this.array[e+2]=a,this.array[e+3]=r,this}onUpload(e){return this.onUploadCallback=e,this}clone(){return new this.constructor(this.array,this.itemSize).copy(this)}toJSON(){const e={itemSize:this.itemSize,type:this.array.constructor.name,array:Array.from(this.array),normalized:this.normalized};return this.name!==""&&(e.name=this.name),this.usage!==co&&(e.usage=this.usage),e}}class jc extends tn{constructor(e,t,i){super(new Uint16Array(e),t,i)}}class Hc extends tn{constructor(e,t,i){super(new Uint32Array(e),t,i)}}class He extends tn{constructor(e,t,i){super(new Float32Array(e),t,i)}}let wu=0;const jt=new st,gr=new Et,fi=new F,Nt=new Qi,ji=new Qi,xt=new F;class $e extends Di{constructor(){super(),this.isBufferGeometry=!0,Object.defineProperty(this,"id",{value:wu++}),this.uuid=Zi(),this.name="",this.type="BufferGeometry",this.index=null,this.indirect=null,this.attributes={},this.morphAttributes={},this.morphTargetsRelative=!1,this.groups=[],this.boundingBox=null,this.boundingSphere=null,this.drawRange={start:0,count:1/0},this.userData={}}getIndex(){return this.index}setIndex(e){return Array.isArray(e)?this.index=new(Oc(e)?Hc:jc)(e,1):this.index=e,this}setIndirect(e){return this.indirect=e,this}getIndirect(){return this.indirect}getAttribute(e){return this.attributes[e]}setAttribute(e,t){return this.attributes[e]=t,this}deleteAttribute(e){return delete this.attributes[e],this}hasAttribute(e){return this.attributes[e]!==void 0}addGroup(e,t,i=0){this.groups.push({start:e,count:t,materialIndex:i})}clearGroups(){this.groups=[]}setDrawRange(e,t){this.drawRange.start=e,this.drawRange.count=t}applyMatrix4(e){const t=this.attributes.position;t!==void 0&&(t.applyMatrix4(e),t.needsUpdate=!0);const i=this.attributes.normal;if(i!==void 0){const r=new Be().getNormalMatrix(e);i.applyNormalMatrix(r),i.needsUpdate=!0}const a=this.attributes.tangent;return a!==void 0&&(a.transformDirection(e),a.needsUpdate=!0),this.boundingBox!==null&&this.computeBoundingBox(),this.boundingSphere!==null&&this.computeBoundingSphere(),this}applyQuaternion(e){return jt.makeRotationFromQuaternion(e),this.applyMatrix4(jt),this}rotateX(e){return jt.makeRotationX(e),this.applyMatrix4(jt),this}rotateY(e){return jt.makeRotationY(e),this.applyMatrix4(jt),this}rotateZ(e){return jt.makeRotationZ(e),this.applyMatrix4(jt),this}translate(e,t,i){return jt.makeTranslation(e,t,i),this.applyMatrix4(jt),this}scale(e,t,i){return jt.makeScale(e,t,i),this.applyMatrix4(jt),this}lookAt(e){return gr.lookAt(e),gr.updateMatrix(),this.applyMatrix4(gr.matrix),this}center(){return this.computeBoundingBox(),this.boundingBox.getCenter(fi).negate(),this.translate(fi.x,fi.y,fi.z),this}setFromPoints(e){const t=this.getAttribute("position");if(t===void 0){const i=[];for(let a=0,r=e.length;a<r;a++){const s=e[a];i.push(s.x,s.y,s.z||0)}this.setAttribute("position",new He(i,3))}else{const i=Math.min(e.length,t.count);for(let a=0;a<i;a++){const r=e[a];t.setXYZ(a,r.x,r.y,r.z||0)}e.length>t.count&&console.warn("THREE.BufferGeometry: Buffer size too small for points data. Use .dispose() and create a new geometry."),t.needsUpdate=!0}return this}computeBoundingBox(){this.boundingBox===null&&(this.boundingBox=new Qi);const e=this.attributes.position,t=this.morphAttributes.position;if(e&&e.isGLBufferAttribute){console.error("THREE.BufferGeometry.computeBoundingBox(): GLBufferAttribute requires a manual bounding box.",this),this.boundingBox.set(new F(-1/0,-1/0,-1/0),new F(1/0,1/0,1/0));return}if(e!==void 0){if(this.boundingBox.setFromBufferAttribute(e),t)for(let i=0,a=t.length;i<a;i++){const r=t[i];Nt.setFromBufferAttribute(r),this.morphTargetsRelative?(xt.addVectors(this.boundingBox.min,Nt.min),this.boundingBox.expandByPoint(xt),xt.addVectors(this.boundingBox.max,Nt.max),this.boundingBox.expandByPoint(xt)):(this.boundingBox.expandByPoint(Nt.min),this.boundingBox.expandByPoint(Nt.max))}}else this.boundingBox.makeEmpty();(isNaN(this.boundingBox.min.x)||isNaN(this.boundingBox.min.y)||isNaN(this.boundingBox.min.z))&&console.error('THREE.BufferGeometry.computeBoundingBox(): Computed min/max have NaN values. The "position" attribute is likely to have NaN values.',this)}computeBoundingSphere(){this.boundingSphere===null&&(this.boundingSphere=new Wa);const e=this.attributes.position,t=this.morphAttributes.position;if(e&&e.isGLBufferAttribute){console.error("THREE.BufferGeometry.computeBoundingSphere(): GLBufferAttribute requires a manual bounding sphere.",this),this.boundingSphere.set(new F,1/0);return}if(e){const i=this.boundingSphere.center;if(Nt.setFromBufferAttribute(e),t)for(let r=0,s=t.length;r<s;r++){const o=t[r];ji.setFromBufferAttribute(o),this.morphTargetsRelative?(xt.addVectors(Nt.min,ji.min),Nt.expandByPoint(xt),xt.addVectors(Nt.max,ji.max),Nt.expandByPoint(xt)):(Nt.expandByPoint(ji.min),Nt.expandByPoint(ji.max))}Nt.getCenter(i);let a=0;for(let r=0,s=e.count;r<s;r++)xt.fromBufferAttribute(e,r),a=Math.max(a,i.distanceToSquared(xt));if(t)for(let r=0,s=t.length;r<s;r++){const o=t[r],c=this.morphTargetsRelative;for(let l=0,u=o.count;l<u;l++)xt.fromBufferAttribute(o,l),c&&(fi.fromBufferAttribute(e,l),xt.add(fi)),a=Math.max(a,i.distanceToSquared(xt))}this.boundingSphere.radius=Math.sqrt(a),isNaN(this.boundingSphere.radius)&&console.error('THREE.BufferGeometry.computeBoundingSphere(): Computed radius is NaN. The "position" attribute is likely to have NaN values.',this)}}computeTangents(){const e=this.index,t=this.attributes;if(e===null||t.position===void 0||t.normal===void 0||t.uv===void 0){console.error("THREE.BufferGeometry: .computeTangents() failed. Missing required attributes (index, position, normal or uv)");return}const i=t.position,a=t.normal,r=t.uv;this.hasAttribute("tangent")===!1&&this.setAttribute("tangent",new tn(new Float32Array(4*i.count),4));const s=this.getAttribute("tangent"),o=[],c=[];for(let D=0;D<i.count;D++)o[D]=new F,c[D]=new F;const l=new F,u=new F,h=new F,f=new Ke,m=new Ke,g=new Ke,_=new F,p=new F;function d(D,M,v){l.fromBufferAttribute(i,D),u.fromBufferAttribute(i,M),h.fromBufferAttribute(i,v),f.fromBufferAttribute(r,D),m.fromBufferAttribute(r,M),g.fromBufferAttribute(r,v),u.sub(l),h.sub(l),m.sub(f),g.sub(f);const R=1/(m.x*g.y-g.x*m.y);isFinite(R)&&(_.copy(u).multiplyScalar(g.y).addScaledVector(h,-m.y).multiplyScalar(R),p.copy(h).multiplyScalar(m.x).addScaledVector(u,-g.x).multiplyScalar(R),o[D].add(_),o[M].add(_),o[v].add(_),c[D].add(p),c[M].add(p),c[v].add(p))}let E=this.groups;E.length===0&&(E=[{start:0,count:e.count}]);for(let D=0,M=E.length;D<M;++D){const v=E[D],R=v.start,U=v.count;for(let C=R,P=R+U;C<P;C+=3)d(e.getX(C+0),e.getX(C+1),e.getX(C+2))}const S=new F,x=new F,T=new F,y=new F;function w(D){T.fromBufferAttribute(a,D),y.copy(T);const M=o[D];S.copy(M),S.sub(T.multiplyScalar(T.dot(M))).normalize(),x.crossVectors(y,M);const R=x.dot(c[D])<0?-1:1;s.setXYZW(D,S.x,S.y,S.z,R)}for(let D=0,M=E.length;D<M;++D){const v=E[D],R=v.start,U=v.count;for(let C=R,P=R+U;C<P;C+=3)w(e.getX(C+0)),w(e.getX(C+1)),w(e.getX(C+2))}}computeVertexNormals(){const e=this.index,t=this.getAttribute("position");if(t!==void 0){let i=this.getAttribute("normal");if(i===void 0)i=new tn(new Float32Array(t.count*3),3),this.setAttribute("normal",i);else for(let f=0,m=i.count;f<m;f++)i.setXYZ(f,0,0,0);const a=new F,r=new F,s=new F,o=new F,c=new F,l=new F,u=new F,h=new F;if(e)for(let f=0,m=e.count;f<m;f+=3){const g=e.getX(f+0),_=e.getX(f+1),p=e.getX(f+2);a.fromBufferAttribute(t,g),r.fromBufferAttribute(t,_),s.fromBufferAttribute(t,p),u.subVectors(s,r),h.subVectors(a,r),u.cross(h),o.fromBufferAttribute(i,g),c.fromBufferAttribute(i,_),l.fromBufferAttribute(i,p),o.add(u),c.add(u),l.add(u),i.setXYZ(g,o.x,o.y,o.z),i.setXYZ(_,c.x,c.y,c.z),i.setXYZ(p,l.x,l.y,l.z)}else for(let f=0,m=t.count;f<m;f+=3)a.fromBufferAttribute(t,f+0),r.fromBufferAttribute(t,f+1),s.fromBufferAttribute(t,f+2),u.subVectors(s,r),h.subVectors(a,r),u.cross(h),i.setXYZ(f+0,u.x,u.y,u.z),i.setXYZ(f+1,u.x,u.y,u.z),i.setXYZ(f+2,u.x,u.y,u.z);this.normalizeNormals(),i.needsUpdate=!0}}normalizeNormals(){const e=this.attributes.normal;for(let t=0,i=e.count;t<i;t++)xt.fromBufferAttribute(e,t),xt.normalize(),e.setXYZ(t,xt.x,xt.y,xt.z)}toNonIndexed(){function e(o,c){const l=o.array,u=o.itemSize,h=o.normalized,f=new l.constructor(c.length*u);let m=0,g=0;for(let _=0,p=c.length;_<p;_++){o.isInterleavedBufferAttribute?m=c[_]*o.data.stride+o.offset:m=c[_]*u;for(let d=0;d<u;d++)f[g++]=l[m++]}return new tn(f,u,h)}if(this.index===null)return console.warn("THREE.BufferGeometry.toNonIndexed(): BufferGeometry is already non-indexed."),this;const t=new $e,i=this.index.array,a=this.attributes;for(const o in a){const c=a[o],l=e(c,i);t.setAttribute(o,l)}const r=this.morphAttributes;for(const o in r){const c=[],l=r[o];for(let u=0,h=l.length;u<h;u++){const f=l[u],m=e(f,i);c.push(m)}t.morphAttributes[o]=c}t.morphTargetsRelative=this.morphTargetsRelative;const s=this.groups;for(let o=0,c=s.length;o<c;o++){const l=s[o];t.addGroup(l.start,l.count,l.materialIndex)}return t}toJSON(){const e={metadata:{version:4.6,type:"BufferGeometry",generator:"BufferGeometry.toJSON"}};if(e.uuid=this.uuid,e.type=this.type,this.name!==""&&(e.name=this.name),Object.keys(this.userData).length>0&&(e.userData=this.userData),this.parameters!==void 0){const c=this.parameters;for(const l in c)c[l]!==void 0&&(e[l]=c[l]);return e}e.data={attributes:{}};const t=this.index;t!==null&&(e.data.index={type:t.array.constructor.name,array:Array.prototype.slice.call(t.array)});const i=this.attributes;for(const c in i){const l=i[c];e.data.attributes[c]=l.toJSON(e.data)}const a={};let r=!1;for(const c in this.morphAttributes){const l=this.morphAttributes[c],u=[];for(let h=0,f=l.length;h<f;h++){const m=l[h];u.push(m.toJSON(e.data))}u.length>0&&(a[c]=u,r=!0)}r&&(e.data.morphAttributes=a,e.data.morphTargetsRelative=this.morphTargetsRelative);const s=this.groups;s.length>0&&(e.data.groups=JSON.parse(JSON.stringify(s)));const o=this.boundingSphere;return o!==null&&(e.data.boundingSphere={center:o.center.toArray(),radius:o.radius}),e}clone(){return new this.constructor().copy(this)}copy(e){this.index=null,this.attributes={},this.morphAttributes={},this.groups=[],this.boundingBox=null,this.boundingSphere=null;const t={};this.name=e.name;const i=e.index;i!==null&&this.setIndex(i.clone(t));const a=e.attributes;for(const l in a){const u=a[l];this.setAttribute(l,u.clone(t))}const r=e.morphAttributes;for(const l in r){const u=[],h=r[l];for(let f=0,m=h.length;f<m;f++)u.push(h[f].clone(t));this.morphAttributes[l]=u}this.morphTargetsRelative=e.morphTargetsRelative;const s=e.groups;for(let l=0,u=s.length;l<u;l++){const h=s[l];this.addGroup(h.start,h.count,h.materialIndex)}const o=e.boundingBox;o!==null&&(this.boundingBox=o.clone());const c=e.boundingSphere;return c!==null&&(this.boundingSphere=c.clone()),this.drawRange.start=e.drawRange.start,this.drawRange.count=e.drawRange.count,this.userData=e.userData,this}dispose(){this.dispatchEvent({type:"dispose"})}}const bo=new st,On=new Fs,fa=new Wa,yo=new F,pa=new F,ma=new F,ga=new F,_r=new F,_a=new F,To=new F,va=new F;class Ge extends Et{constructor(e=new $e,t=new Ui){super(),this.isMesh=!0,this.type="Mesh",this.geometry=e,this.material=t,this.morphTargetDictionary=void 0,this.morphTargetInfluences=void 0,this.updateMorphTargets()}copy(e,t){return super.copy(e,t),e.morphTargetInfluences!==void 0&&(this.morphTargetInfluences=e.morphTargetInfluences.slice()),e.morphTargetDictionary!==void 0&&(this.morphTargetDictionary=Object.assign({},e.morphTargetDictionary)),this.material=Array.isArray(e.material)?e.material.slice():e.material,this.geometry=e.geometry,this}updateMorphTargets(){const t=this.geometry.morphAttributes,i=Object.keys(t);if(i.length>0){const a=t[i[0]];if(a!==void 0){this.morphTargetInfluences=[],this.morphTargetDictionary={};for(let r=0,s=a.length;r<s;r++){const o=a[r].name||String(r);this.morphTargetInfluences.push(0),this.morphTargetDictionary[o]=r}}}}getVertexPosition(e,t){const i=this.geometry,a=i.attributes.position,r=i.morphAttributes.position,s=i.morphTargetsRelative;t.fromBufferAttribute(a,e);const o=this.morphTargetInfluences;if(r&&o){_a.set(0,0,0);for(let c=0,l=r.length;c<l;c++){const u=o[c],h=r[c];u!==0&&(_r.fromBufferAttribute(h,e),s?_a.addScaledVector(_r,u):_a.addScaledVector(_r.sub(t),u))}t.add(_a)}return t}raycast(e,t){const i=this.geometry,a=this.material,r=this.matrixWorld;a!==void 0&&(i.boundingSphere===null&&i.computeBoundingSphere(),fa.copy(i.boundingSphere),fa.applyMatrix4(r),On.copy(e.ray).recast(e.near),!(fa.containsPoint(On.origin)===!1&&(On.intersectSphere(fa,yo)===null||On.origin.distanceToSquared(yo)>(e.far-e.near)**2))&&(bo.copy(r).invert(),On.copy(e.ray).applyMatrix4(bo),!(i.boundingBox!==null&&On.intersectsBox(i.boundingBox)===!1)&&this._computeIntersections(e,t,On)))}_computeIntersections(e,t,i){let a;const r=this.geometry,s=this.material,o=r.index,c=r.attributes.position,l=r.attributes.uv,u=r.attributes.uv1,h=r.attributes.normal,f=r.groups,m=r.drawRange;if(o!==null)if(Array.isArray(s))for(let g=0,_=f.length;g<_;g++){const p=f[g],d=s[p.materialIndex],E=Math.max(p.start,m.start),S=Math.min(o.count,Math.min(p.start+p.count,m.start+m.count));for(let x=E,T=S;x<T;x+=3){const y=o.getX(x),w=o.getX(x+1),D=o.getX(x+2);a=xa(this,d,e,i,l,u,h,y,w,D),a&&(a.faceIndex=Math.floor(x/3),a.face.materialIndex=p.materialIndex,t.push(a))}}else{const g=Math.max(0,m.start),_=Math.min(o.count,m.start+m.count);for(let p=g,d=_;p<d;p+=3){const E=o.getX(p),S=o.getX(p+1),x=o.getX(p+2);a=xa(this,s,e,i,l,u,h,E,S,x),a&&(a.faceIndex=Math.floor(p/3),t.push(a))}}else if(c!==void 0)if(Array.isArray(s))for(let g=0,_=f.length;g<_;g++){const p=f[g],d=s[p.materialIndex],E=Math.max(p.start,m.start),S=Math.min(c.count,Math.min(p.start+p.count,m.start+m.count));for(let x=E,T=S;x<T;x+=3){const y=x,w=x+1,D=x+2;a=xa(this,d,e,i,l,u,h,y,w,D),a&&(a.faceIndex=Math.floor(x/3),a.face.materialIndex=p.materialIndex,t.push(a))}}else{const g=Math.max(0,m.start),_=Math.min(c.count,m.start+m.count);for(let p=g,d=_;p<d;p+=3){const E=p,S=p+1,x=p+2;a=xa(this,s,e,i,l,u,h,E,S,x),a&&(a.faceIndex=Math.floor(p/3),t.push(a))}}}}function Ru(n,e,t,i,a,r,s,o){let c;if(e.side===Lt?c=i.intersectTriangle(s,r,a,!0,o):c=i.intersectTriangle(a,r,s,e.side===Ln,o),c===null)return null;va.copy(o),va.applyMatrix4(n.matrixWorld);const l=t.ray.origin.distanceTo(va);return l<t.near||l>t.far?null:{distance:l,point:va.clone(),object:n}}function xa(n,e,t,i,a,r,s,o,c,l){n.getVertexPosition(o,pa),n.getVertexPosition(c,ma),n.getVertexPosition(l,ga);const u=Ru(n,e,t,i,pa,ma,ga,To);if(u){const h=new F;Gt.getBarycoord(To,pa,ma,ga,h),a&&(u.uv=Gt.getInterpolatedAttribute(a,o,c,l,h,new Ke)),r&&(u.uv1=Gt.getInterpolatedAttribute(r,o,c,l,h,new Ke)),s&&(u.normal=Gt.getInterpolatedAttribute(s,o,c,l,h,new F),u.normal.dot(i.direction)>0&&u.normal.multiplyScalar(-1));const f={a:o,b:c,c:l,normal:new F,materialIndex:0};Gt.getNormal(pa,ma,ga,f.normal),u.face=f,u.barycoord=h}return u}class mn extends $e{constructor(e=1,t=1,i=1,a=1,r=1,s=1){super(),this.type="BoxGeometry",this.parameters={width:e,height:t,depth:i,widthSegments:a,heightSegments:r,depthSegments:s};const o=this;a=Math.floor(a),r=Math.floor(r),s=Math.floor(s);const c=[],l=[],u=[],h=[];let f=0,m=0;g("z","y","x",-1,-1,i,t,e,s,r,0),g("z","y","x",1,-1,i,t,-e,s,r,1),g("x","z","y",1,1,e,i,t,a,s,2),g("x","z","y",1,-1,e,i,-t,a,s,3),g("x","y","z",1,-1,e,t,i,a,r,4),g("x","y","z",-1,-1,e,t,-i,a,r,5),this.setIndex(c),this.setAttribute("position",new He(l,3)),this.setAttribute("normal",new He(u,3)),this.setAttribute("uv",new He(h,2));function g(_,p,d,E,S,x,T,y,w,D,M){const v=x/w,R=T/D,U=x/2,C=T/2,P=y/2,N=w+1,k=D+1;let O=0,z=0;const H=new F;for(let $=0;$<k;$++){const Y=$*R-C;for(let fe=0;fe<N;fe++){const Ie=fe*v-U;H[_]=Ie*E,H[p]=Y*S,H[d]=P,l.push(H.x,H.y,H.z),H[_]=0,H[p]=0,H[d]=y>0?1:-1,u.push(H.x,H.y,H.z),h.push(fe/w),h.push(1-$/D),O+=1}}for(let $=0;$<D;$++)for(let Y=0;Y<w;Y++){const fe=f+Y+N*$,Ie=f+Y+N*($+1),X=f+(Y+1)+N*($+1),ne=f+(Y+1)+N*$;c.push(fe,Ie,ne),c.push(Ie,X,ne),z+=6}o.addGroup(m,z,M),m+=z,f+=O}}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}static fromJSON(e){return new mn(e.width,e.height,e.depth,e.widthSegments,e.heightSegments,e.depthSegments)}}function Ii(n){const e={};for(const t in n){e[t]={};for(const i in n[t]){const a=n[t][i];a&&(a.isColor||a.isMatrix3||a.isMatrix4||a.isVector2||a.isVector3||a.isVector4||a.isTexture||a.isQuaternion)?a.isRenderTargetTexture?(console.warn("UniformsUtils: Textures of render targets cannot be cloned via cloneUniforms() or mergeUniforms()."),e[t][i]=null):e[t][i]=a.clone():Array.isArray(a)?e[t][i]=a.slice():e[t][i]=a}}return e}function Rt(n){const e={};for(let t=0;t<n.length;t++){const i=Ii(n[t]);for(const a in i)e[a]=i[a]}return e}function Cu(n){const e=[];for(let t=0;t<n.length;t++)e.push(n[t].clone());return e}function Gc(n){const e=n.getRenderTarget();return e===null?n.outputColorSpace:e.isXRRenderTarget===!0?e.texture.colorSpace:Qe.workingColorSpace}const Pu={clone:Ii,merge:Rt};var Iu=`void main() {
	gl_Position = projectionMatrix * modelViewMatrix * vec4( position, 1.0 );
}`,Du=`void main() {
	gl_FragColor = vec4( 1.0, 0.0, 0.0, 1.0 );
}`;class Un extends Li{constructor(e){super(),this.isShaderMaterial=!0,this.type="ShaderMaterial",this.defines={},this.uniforms={},this.uniformsGroups=[],this.vertexShader=Iu,this.fragmentShader=Du,this.linewidth=1,this.wireframe=!1,this.wireframeLinewidth=1,this.fog=!1,this.lights=!1,this.clipping=!1,this.forceSinglePass=!0,this.extensions={clipCullDistance:!1,multiDraw:!1},this.defaultAttributeValues={color:[1,1,1],uv:[0,0],uv1:[0,0]},this.index0AttributeName=void 0,this.uniformsNeedUpdate=!1,this.glslVersion=null,e!==void 0&&this.setValues(e)}copy(e){return super.copy(e),this.fragmentShader=e.fragmentShader,this.vertexShader=e.vertexShader,this.uniforms=Ii(e.uniforms),this.uniformsGroups=Cu(e.uniformsGroups),this.defines=Object.assign({},e.defines),this.wireframe=e.wireframe,this.wireframeLinewidth=e.wireframeLinewidth,this.fog=e.fog,this.lights=e.lights,this.clipping=e.clipping,this.extensions=Object.assign({},e.extensions),this.glslVersion=e.glslVersion,this}toJSON(e){const t=super.toJSON(e);t.glslVersion=this.glslVersion,t.uniforms={};for(const a in this.uniforms){const s=this.uniforms[a].value;s&&s.isTexture?t.uniforms[a]={type:"t",value:s.toJSON(e).uuid}:s&&s.isColor?t.uniforms[a]={type:"c",value:s.getHex()}:s&&s.isVector2?t.uniforms[a]={type:"v2",value:s.toArray()}:s&&s.isVector3?t.uniforms[a]={type:"v3",value:s.toArray()}:s&&s.isVector4?t.uniforms[a]={type:"v4",value:s.toArray()}:s&&s.isMatrix3?t.uniforms[a]={type:"m3",value:s.toArray()}:s&&s.isMatrix4?t.uniforms[a]={type:"m4",value:s.toArray()}:t.uniforms[a]={value:s}}Object.keys(this.defines).length>0&&(t.defines=this.defines),t.vertexShader=this.vertexShader,t.fragmentShader=this.fragmentShader,t.lights=this.lights,t.clipping=this.clipping;const i={};for(const a in this.extensions)this.extensions[a]===!0&&(i[a]=!0);return Object.keys(i).length>0&&(t.extensions=i),t}}class Wc extends Et{constructor(){super(),this.isCamera=!0,this.type="Camera",this.matrixWorldInverse=new st,this.projectionMatrix=new st,this.projectionMatrixInverse=new st,this.coordinateSystem=pn}copy(e,t){return super.copy(e,t),this.matrixWorldInverse.copy(e.matrixWorldInverse),this.projectionMatrix.copy(e.projectionMatrix),this.projectionMatrixInverse.copy(e.projectionMatrixInverse),this.coordinateSystem=e.coordinateSystem,this}getWorldDirection(e){return super.getWorldDirection(e).negate()}updateMatrixWorld(e){super.updateMatrixWorld(e),this.matrixWorldInverse.copy(this.matrixWorld).invert()}updateWorldMatrix(e,t){super.updateWorldMatrix(e,t),this.matrixWorldInverse.copy(this.matrixWorld).invert()}clone(){return new this.constructor().copy(this)}}const yn=new F,Ao=new Ke,wo=new Ke;class Ht extends Wc{constructor(e=50,t=1,i=.1,a=2e3){super(),this.isPerspectiveCamera=!0,this.type="PerspectiveCamera",this.fov=e,this.zoom=1,this.near=i,this.far=a,this.focus=10,this.aspect=t,this.view=null,this.filmGauge=35,this.filmOffset=0,this.updateProjectionMatrix()}copy(e,t){return super.copy(e,t),this.fov=e.fov,this.zoom=e.zoom,this.near=e.near,this.far=e.far,this.focus=e.focus,this.aspect=e.aspect,this.view=e.view===null?null:Object.assign({},e.view),this.filmGauge=e.filmGauge,this.filmOffset=e.filmOffset,this}setFocalLength(e){const t=.5*this.getFilmHeight()/e;this.fov=Ms*2*Math.atan(t),this.updateProjectionMatrix()}getFocalLength(){const e=Math.tan(za*.5*this.fov);return .5*this.getFilmHeight()/e}getEffectiveFOV(){return Ms*2*Math.atan(Math.tan(za*.5*this.fov)/this.zoom)}getFilmWidth(){return this.filmGauge*Math.min(this.aspect,1)}getFilmHeight(){return this.filmGauge/Math.max(this.aspect,1)}getViewBounds(e,t,i){yn.set(-1,-1,.5).applyMatrix4(this.projectionMatrixInverse),t.set(yn.x,yn.y).multiplyScalar(-e/yn.z),yn.set(1,1,.5).applyMatrix4(this.projectionMatrixInverse),i.set(yn.x,yn.y).multiplyScalar(-e/yn.z)}getViewSize(e,t){return this.getViewBounds(e,Ao,wo),t.subVectors(wo,Ao)}setViewOffset(e,t,i,a,r,s){this.aspect=e/t,this.view===null&&(this.view={enabled:!0,fullWidth:1,fullHeight:1,offsetX:0,offsetY:0,width:1,height:1}),this.view.enabled=!0,this.view.fullWidth=e,this.view.fullHeight=t,this.view.offsetX=i,this.view.offsetY=a,this.view.width=r,this.view.height=s,this.updateProjectionMatrix()}clearViewOffset(){this.view!==null&&(this.view.enabled=!1),this.updateProjectionMatrix()}updateProjectionMatrix(){const e=this.near;let t=e*Math.tan(za*.5*this.fov)/this.zoom,i=2*t,a=this.aspect*i,r=-.5*a;const s=this.view;if(this.view!==null&&this.view.enabled){const c=s.fullWidth,l=s.fullHeight;r+=s.offsetX*a/c,t-=s.offsetY*i/l,a*=s.width/c,i*=s.height/l}const o=this.filmOffset;o!==0&&(r+=e*o/this.getFilmWidth()),this.projectionMatrix.makePerspective(r,r+a,t,t-i,e,this.far,this.coordinateSystem),this.projectionMatrixInverse.copy(this.projectionMatrix).invert()}toJSON(e){const t=super.toJSON(e);return t.object.fov=this.fov,t.object.zoom=this.zoom,t.object.near=this.near,t.object.far=this.far,t.object.focus=this.focus,t.object.aspect=this.aspect,this.view!==null&&(t.object.view=Object.assign({},this.view)),t.object.filmGauge=this.filmGauge,t.object.filmOffset=this.filmOffset,t}}const pi=-90,mi=1;class Lu extends Et{constructor(e,t,i){super(),this.type="CubeCamera",this.renderTarget=i,this.coordinateSystem=null,this.activeMipmapLevel=0;const a=new Ht(pi,mi,e,t);a.layers=this.layers,this.add(a);const r=new Ht(pi,mi,e,t);r.layers=this.layers,this.add(r);const s=new Ht(pi,mi,e,t);s.layers=this.layers,this.add(s);const o=new Ht(pi,mi,e,t);o.layers=this.layers,this.add(o);const c=new Ht(pi,mi,e,t);c.layers=this.layers,this.add(c);const l=new Ht(pi,mi,e,t);l.layers=this.layers,this.add(l)}updateCoordinateSystem(){const e=this.coordinateSystem,t=this.children.concat(),[i,a,r,s,o,c]=t;for(const l of t)this.remove(l);if(e===pn)i.up.set(0,1,0),i.lookAt(1,0,0),a.up.set(0,1,0),a.lookAt(-1,0,0),r.up.set(0,0,-1),r.lookAt(0,1,0),s.up.set(0,0,1),s.lookAt(0,-1,0),o.up.set(0,1,0),o.lookAt(0,0,1),c.up.set(0,1,0),c.lookAt(0,0,-1);else if(e===Oa)i.up.set(0,-1,0),i.lookAt(-1,0,0),a.up.set(0,-1,0),a.lookAt(1,0,0),r.up.set(0,0,1),r.lookAt(0,1,0),s.up.set(0,0,-1),s.lookAt(0,-1,0),o.up.set(0,-1,0),o.lookAt(0,0,1),c.up.set(0,-1,0),c.lookAt(0,0,-1);else throw new Error("THREE.CubeCamera.updateCoordinateSystem(): Invalid coordinate system: "+e);for(const l of t)this.add(l),l.updateMatrixWorld()}update(e,t){this.parent===null&&this.updateMatrixWorld();const{renderTarget:i,activeMipmapLevel:a}=this;this.coordinateSystem!==e.coordinateSystem&&(this.coordinateSystem=e.coordinateSystem,this.updateCoordinateSystem());const[r,s,o,c,l,u]=this.children,h=e.getRenderTarget(),f=e.getActiveCubeFace(),m=e.getActiveMipmapLevel(),g=e.xr.enabled;e.xr.enabled=!1;const _=i.texture.generateMipmaps;i.texture.generateMipmaps=!1,e.setRenderTarget(i,0,a),e.render(t,r),e.setRenderTarget(i,1,a),e.render(t,s),e.setRenderTarget(i,2,a),e.render(t,o),e.setRenderTarget(i,3,a),e.render(t,c),e.setRenderTarget(i,4,a),e.render(t,l),i.texture.generateMipmaps=_,e.setRenderTarget(i,5,a),e.render(t,u),e.setRenderTarget(h,f,m),e.xr.enabled=g,i.texture.needsPMREMUpdate=!0}}class Xc extends Ct{constructor(e,t,i,a,r,s,o,c,l,u){e=e!==void 0?e:[],t=t!==void 0?t:Ai,super(e,t,i,a,r,s,o,c,l,u),this.isCubeTexture=!0,this.flipY=!1}get images(){return this.image}set images(e){this.image=e}}class Uu extends ti{constructor(e=1,t={}){super(e,e,t),this.isWebGLCubeRenderTarget=!0;const i={width:e,height:e,depth:1},a=[i,i,i,i,i,i];this.texture=new Xc(a,t.mapping,t.wrapS,t.wrapT,t.magFilter,t.minFilter,t.format,t.type,t.anisotropy,t.colorSpace),this.texture.isRenderTargetTexture=!0,this.texture.generateMipmaps=t.generateMipmaps!==void 0?t.generateMipmaps:!1,this.texture.minFilter=t.minFilter!==void 0?t.minFilter:en}fromEquirectangularTexture(e,t){this.texture.type=t.type,this.texture.colorSpace=t.colorSpace,this.texture.generateMipmaps=t.generateMipmaps,this.texture.minFilter=t.minFilter,this.texture.magFilter=t.magFilter;const i={uniforms:{tEquirect:{value:null}},vertexShader:`

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
			`},a=new mn(5,5,5),r=new Un({name:"CubemapFromEquirect",uniforms:Ii(i.uniforms),vertexShader:i.vertexShader,fragmentShader:i.fragmentShader,side:Lt,blending:In});r.uniforms.tEquirect.value=t;const s=new Ge(a,r),o=t.minFilter;return t.minFilter===Zn&&(t.minFilter=en),new Lu(1,10,this).update(e,s),t.minFilter=o,s.geometry.dispose(),s.material.dispose(),this}clear(e,t,i,a){const r=e.getRenderTarget();for(let s=0;s<6;s++)e.setRenderTarget(this,s),e.clear(t,i,a);e.setRenderTarget(r)}}class it extends Et{constructor(){super(),this.isGroup=!0,this.type="Group"}}const zu={type:"move"};class vr{constructor(){this._targetRay=null,this._grip=null,this._hand=null}getHandSpace(){return this._hand===null&&(this._hand=new it,this._hand.matrixAutoUpdate=!1,this._hand.visible=!1,this._hand.joints={},this._hand.inputState={pinching:!1}),this._hand}getTargetRaySpace(){return this._targetRay===null&&(this._targetRay=new it,this._targetRay.matrixAutoUpdate=!1,this._targetRay.visible=!1,this._targetRay.hasLinearVelocity=!1,this._targetRay.linearVelocity=new F,this._targetRay.hasAngularVelocity=!1,this._targetRay.angularVelocity=new F),this._targetRay}getGripSpace(){return this._grip===null&&(this._grip=new it,this._grip.matrixAutoUpdate=!1,this._grip.visible=!1,this._grip.hasLinearVelocity=!1,this._grip.linearVelocity=new F,this._grip.hasAngularVelocity=!1,this._grip.angularVelocity=new F),this._grip}dispatchEvent(e){return this._targetRay!==null&&this._targetRay.dispatchEvent(e),this._grip!==null&&this._grip.dispatchEvent(e),this._hand!==null&&this._hand.dispatchEvent(e),this}connect(e){if(e&&e.hand){const t=this._hand;if(t)for(const i of e.hand.values())this._getHandJoint(t,i)}return this.dispatchEvent({type:"connected",data:e}),this}disconnect(e){return this.dispatchEvent({type:"disconnected",data:e}),this._targetRay!==null&&(this._targetRay.visible=!1),this._grip!==null&&(this._grip.visible=!1),this._hand!==null&&(this._hand.visible=!1),this}update(e,t,i){let a=null,r=null,s=null;const o=this._targetRay,c=this._grip,l=this._hand;if(e&&t.session.visibilityState!=="visible-blurred"){if(l&&e.hand){s=!0;for(const _ of e.hand.values()){const p=t.getJointPose(_,i),d=this._getHandJoint(l,_);p!==null&&(d.matrix.fromArray(p.transform.matrix),d.matrix.decompose(d.position,d.rotation,d.scale),d.matrixWorldNeedsUpdate=!0,d.jointRadius=p.radius),d.visible=p!==null}const u=l.joints["index-finger-tip"],h=l.joints["thumb-tip"],f=u.position.distanceTo(h.position),m=.02,g=.005;l.inputState.pinching&&f>m+g?(l.inputState.pinching=!1,this.dispatchEvent({type:"pinchend",handedness:e.handedness,target:this})):!l.inputState.pinching&&f<=m-g&&(l.inputState.pinching=!0,this.dispatchEvent({type:"pinchstart",handedness:e.handedness,target:this}))}else c!==null&&e.gripSpace&&(r=t.getPose(e.gripSpace,i),r!==null&&(c.matrix.fromArray(r.transform.matrix),c.matrix.decompose(c.position,c.rotation,c.scale),c.matrixWorldNeedsUpdate=!0,r.linearVelocity?(c.hasLinearVelocity=!0,c.linearVelocity.copy(r.linearVelocity)):c.hasLinearVelocity=!1,r.angularVelocity?(c.hasAngularVelocity=!0,c.angularVelocity.copy(r.angularVelocity)):c.hasAngularVelocity=!1));o!==null&&(a=t.getPose(e.targetRaySpace,i),a===null&&r!==null&&(a=r),a!==null&&(o.matrix.fromArray(a.transform.matrix),o.matrix.decompose(o.position,o.rotation,o.scale),o.matrixWorldNeedsUpdate=!0,a.linearVelocity?(o.hasLinearVelocity=!0,o.linearVelocity.copy(a.linearVelocity)):o.hasLinearVelocity=!1,a.angularVelocity?(o.hasAngularVelocity=!0,o.angularVelocity.copy(a.angularVelocity)):o.hasAngularVelocity=!1,this.dispatchEvent(zu)))}return o!==null&&(o.visible=a!==null),c!==null&&(c.visible=r!==null),l!==null&&(l.visible=s!==null),this}_getHandJoint(e,t){if(e.joints[t.jointName]===void 0){const i=new it;i.matrixAutoUpdate=!1,i.visible=!1,e.joints[t.jointName]=i,e.add(i)}return e.joints[t.jointName]}}class ku extends Et{constructor(){super(),this.isScene=!0,this.type="Scene",this.background=null,this.environment=null,this.fog=null,this.backgroundBlurriness=0,this.backgroundIntensity=1,this.backgroundRotation=new Mt,this.environmentIntensity=1,this.environmentRotation=new Mt,this.overrideMaterial=null,typeof __THREE_DEVTOOLS__<"u"&&__THREE_DEVTOOLS__.dispatchEvent(new CustomEvent("observe",{detail:this}))}copy(e,t){return super.copy(e,t),e.background!==null&&(this.background=e.background.clone()),e.environment!==null&&(this.environment=e.environment.clone()),e.fog!==null&&(this.fog=e.fog.clone()),this.backgroundBlurriness=e.backgroundBlurriness,this.backgroundIntensity=e.backgroundIntensity,this.backgroundRotation.copy(e.backgroundRotation),this.environmentIntensity=e.environmentIntensity,this.environmentRotation.copy(e.environmentRotation),e.overrideMaterial!==null&&(this.overrideMaterial=e.overrideMaterial.clone()),this.matrixAutoUpdate=e.matrixAutoUpdate,this}toJSON(e){const t=super.toJSON(e);return this.fog!==null&&(t.object.fog=this.fog.toJSON()),this.backgroundBlurriness>0&&(t.object.backgroundBlurriness=this.backgroundBlurriness),this.backgroundIntensity!==1&&(t.object.backgroundIntensity=this.backgroundIntensity),t.object.backgroundRotation=this.backgroundRotation.toArray(),this.environmentIntensity!==1&&(t.object.environmentIntensity=this.environmentIntensity),t.object.environmentRotation=this.environmentRotation.toArray(),t}}const xr=new F,Nu=new F,Fu=new Be;class Gn{constructor(e=new F(1,0,0),t=0){this.isPlane=!0,this.normal=e,this.constant=t}set(e,t){return this.normal.copy(e),this.constant=t,this}setComponents(e,t,i,a){return this.normal.set(e,t,i),this.constant=a,this}setFromNormalAndCoplanarPoint(e,t){return this.normal.copy(e),this.constant=-t.dot(this.normal),this}setFromCoplanarPoints(e,t,i){const a=xr.subVectors(i,t).cross(Nu.subVectors(e,t)).normalize();return this.setFromNormalAndCoplanarPoint(a,e),this}copy(e){return this.normal.copy(e.normal),this.constant=e.constant,this}normalize(){const e=1/this.normal.length();return this.normal.multiplyScalar(e),this.constant*=e,this}negate(){return this.constant*=-1,this.normal.negate(),this}distanceToPoint(e){return this.normal.dot(e)+this.constant}distanceToSphere(e){return this.distanceToPoint(e.center)-e.radius}projectPoint(e,t){return t.copy(e).addScaledVector(this.normal,-this.distanceToPoint(e))}intersectLine(e,t){const i=e.delta(xr),a=this.normal.dot(i);if(a===0)return this.distanceToPoint(e.start)===0?t.copy(e.start):null;const r=-(e.start.dot(this.normal)+this.constant)/a;return r<0||r>1?null:t.copy(e.start).addScaledVector(i,r)}intersectsLine(e){const t=this.distanceToPoint(e.start),i=this.distanceToPoint(e.end);return t<0&&i>0||i<0&&t>0}intersectsBox(e){return e.intersectsPlane(this)}intersectsSphere(e){return e.intersectsPlane(this)}coplanarPoint(e){return e.copy(this.normal).multiplyScalar(-this.constant)}applyMatrix4(e,t){const i=t||Fu.getNormalMatrix(e),a=this.coplanarPoint(xr).applyMatrix4(e),r=this.normal.applyMatrix3(i).normalize();return this.constant=-a.dot(r),this}translate(e){return this.constant-=e.dot(this.normal),this}equals(e){return e.normal.equals(this.normal)&&e.constant===this.constant}clone(){return new this.constructor().copy(this)}}const Bn=new Wa,Ma=new F;class Bs{constructor(e=new Gn,t=new Gn,i=new Gn,a=new Gn,r=new Gn,s=new Gn){this.planes=[e,t,i,a,r,s]}set(e,t,i,a,r,s){const o=this.planes;return o[0].copy(e),o[1].copy(t),o[2].copy(i),o[3].copy(a),o[4].copy(r),o[5].copy(s),this}copy(e){const t=this.planes;for(let i=0;i<6;i++)t[i].copy(e.planes[i]);return this}setFromProjectionMatrix(e,t=pn){const i=this.planes,a=e.elements,r=a[0],s=a[1],o=a[2],c=a[3],l=a[4],u=a[5],h=a[6],f=a[7],m=a[8],g=a[9],_=a[10],p=a[11],d=a[12],E=a[13],S=a[14],x=a[15];if(i[0].setComponents(c-r,f-l,p-m,x-d).normalize(),i[1].setComponents(c+r,f+l,p+m,x+d).normalize(),i[2].setComponents(c+s,f+u,p+g,x+E).normalize(),i[3].setComponents(c-s,f-u,p-g,x-E).normalize(),i[4].setComponents(c-o,f-h,p-_,x-S).normalize(),t===pn)i[5].setComponents(c+o,f+h,p+_,x+S).normalize();else if(t===Oa)i[5].setComponents(o,h,_,S).normalize();else throw new Error("THREE.Frustum.setFromProjectionMatrix(): Invalid coordinate system: "+t);return this}intersectsObject(e){if(e.boundingSphere!==void 0)e.boundingSphere===null&&e.computeBoundingSphere(),Bn.copy(e.boundingSphere).applyMatrix4(e.matrixWorld);else{const t=e.geometry;t.boundingSphere===null&&t.computeBoundingSphere(),Bn.copy(t.boundingSphere).applyMatrix4(e.matrixWorld)}return this.intersectsSphere(Bn)}intersectsSprite(e){return Bn.center.set(0,0,0),Bn.radius=.7071067811865476,Bn.applyMatrix4(e.matrixWorld),this.intersectsSphere(Bn)}intersectsSphere(e){const t=this.planes,i=e.center,a=-e.radius;for(let r=0;r<6;r++)if(t[r].distanceToPoint(i)<a)return!1;return!0}intersectsBox(e){const t=this.planes;for(let i=0;i<6;i++){const a=t[i];if(Ma.x=a.normal.x>0?e.max.x:e.min.x,Ma.y=a.normal.y>0?e.max.y:e.min.y,Ma.z=a.normal.z>0?e.max.z:e.min.z,a.distanceToPoint(Ma)<0)return!1}return!0}containsPoint(e){const t=this.planes;for(let i=0;i<6;i++)if(t[i].distanceToPoint(e)<0)return!1;return!0}clone(){return new this.constructor().copy(this)}}class ht extends Li{constructor(e){super(),this.isLineBasicMaterial=!0,this.type="LineBasicMaterial",this.color=new ce(16777215),this.map=null,this.linewidth=1,this.linecap="round",this.linejoin="round",this.fog=!0,this.setValues(e)}copy(e){return super.copy(e),this.color.copy(e.color),this.map=e.map,this.linewidth=e.linewidth,this.linecap=e.linecap,this.linejoin=e.linejoin,this.fog=e.fog,this}}const Va=new F,ja=new F,Ro=new st,Hi=new Fs,Sa=new Wa,Mr=new F,Co=new F;class Xi extends Et{constructor(e=new $e,t=new ht){super(),this.isLine=!0,this.type="Line",this.geometry=e,this.material=t,this.morphTargetDictionary=void 0,this.morphTargetInfluences=void 0,this.updateMorphTargets()}copy(e,t){return super.copy(e,t),this.material=Array.isArray(e.material)?e.material.slice():e.material,this.geometry=e.geometry,this}computeLineDistances(){const e=this.geometry;if(e.index===null){const t=e.attributes.position,i=[0];for(let a=1,r=t.count;a<r;a++)Va.fromBufferAttribute(t,a-1),ja.fromBufferAttribute(t,a),i[a]=i[a-1],i[a]+=Va.distanceTo(ja);e.setAttribute("lineDistance",new He(i,1))}else console.warn("THREE.Line.computeLineDistances(): Computation only possible with non-indexed BufferGeometry.");return this}raycast(e,t){const i=this.geometry,a=this.matrixWorld,r=e.params.Line.threshold,s=i.drawRange;if(i.boundingSphere===null&&i.computeBoundingSphere(),Sa.copy(i.boundingSphere),Sa.applyMatrix4(a),Sa.radius+=r,e.ray.intersectsSphere(Sa)===!1)return;Ro.copy(a).invert(),Hi.copy(e.ray).applyMatrix4(Ro);const o=r/((this.scale.x+this.scale.y+this.scale.z)/3),c=o*o,l=this.isLineSegments?2:1,u=i.index,f=i.attributes.position;if(u!==null){const m=Math.max(0,s.start),g=Math.min(u.count,s.start+s.count);for(let _=m,p=g-1;_<p;_+=l){const d=u.getX(_),E=u.getX(_+1),S=Ea(this,e,Hi,c,d,E,_);S&&t.push(S)}if(this.isLineLoop){const _=u.getX(g-1),p=u.getX(m),d=Ea(this,e,Hi,c,_,p,g-1);d&&t.push(d)}}else{const m=Math.max(0,s.start),g=Math.min(f.count,s.start+s.count);for(let _=m,p=g-1;_<p;_+=l){const d=Ea(this,e,Hi,c,_,_+1,_);d&&t.push(d)}if(this.isLineLoop){const _=Ea(this,e,Hi,c,g-1,m,g-1);_&&t.push(_)}}}updateMorphTargets(){const t=this.geometry.morphAttributes,i=Object.keys(t);if(i.length>0){const a=t[i[0]];if(a!==void 0){this.morphTargetInfluences=[],this.morphTargetDictionary={};for(let r=0,s=a.length;r<s;r++){const o=a[r].name||String(r);this.morphTargetInfluences.push(0),this.morphTargetDictionary[o]=r}}}}}function Ea(n,e,t,i,a,r,s){const o=n.geometry.attributes.position;if(Va.fromBufferAttribute(o,a),ja.fromBufferAttribute(o,r),t.distanceSqToSegment(Va,ja,Mr,Co)>i)return;Mr.applyMatrix4(n.matrixWorld);const l=e.ray.origin.distanceTo(Mr);if(!(l<e.near||l>e.far))return{distance:l,point:Co.clone().applyMatrix4(n.matrixWorld),index:s,face:null,faceIndex:null,barycoord:null,object:n}}const Po=new F,Io=new F;class gt extends Xi{constructor(e,t){super(e,t),this.isLineSegments=!0,this.type="LineSegments"}computeLineDistances(){const e=this.geometry;if(e.index===null){const t=e.attributes.position,i=[];for(let a=0,r=t.count;a<r;a+=2)Po.fromBufferAttribute(t,a),Io.fromBufferAttribute(t,a+1),i[a]=a===0?0:i[a-1],i[a+1]=i[a]+Po.distanceTo(Io);e.setAttribute("lineDistance",new He(i,1))}else console.warn("THREE.LineSegments.computeLineDistances(): Computation only possible with non-indexed BufferGeometry.");return this}}class Kc extends Ct{constructor(e,t,i,a,r,s,o,c,l,u=bi){if(u!==bi&&u!==Ci)throw new Error("DepthTexture format must be either THREE.DepthFormat or THREE.DepthStencilFormat");i===void 0&&u===bi&&(i=ei),i===void 0&&u===Ci&&(i=Ri),super(null,a,r,s,o,c,u,i,l),this.isDepthTexture=!0,this.image={width:e,height:t},this.magFilter=o!==void 0?o:Jt,this.minFilter=c!==void 0?c:Jt,this.flipY=!1,this.generateMipmaps=!1,this.compareFunction=null}copy(e){return super.copy(e),this.source=new Ns(Object.assign({},e.image)),this.compareFunction=e.compareFunction,this}toJSON(e){const t=super.toJSON(e);return this.compareFunction!==null&&(t.compareFunction=this.compareFunction),t}}class ea extends $e{constructor(e=1,t=1,i=1,a=32,r=1,s=!1,o=0,c=Math.PI*2){super(),this.type="CylinderGeometry",this.parameters={radiusTop:e,radiusBottom:t,height:i,radialSegments:a,heightSegments:r,openEnded:s,thetaStart:o,thetaLength:c};const l=this;a=Math.floor(a),r=Math.floor(r);const u=[],h=[],f=[],m=[];let g=0;const _=[],p=i/2;let d=0;E(),s===!1&&(e>0&&S(!0),t>0&&S(!1)),this.setIndex(u),this.setAttribute("position",new He(h,3)),this.setAttribute("normal",new He(f,3)),this.setAttribute("uv",new He(m,2));function E(){const x=new F,T=new F;let y=0;const w=(t-e)/i;for(let D=0;D<=r;D++){const M=[],v=D/r,R=v*(t-e)+e;for(let U=0;U<=a;U++){const C=U/a,P=C*c+o,N=Math.sin(P),k=Math.cos(P);T.x=R*N,T.y=-v*i+p,T.z=R*k,h.push(T.x,T.y,T.z),x.set(N,w,k).normalize(),f.push(x.x,x.y,x.z),m.push(C,1-v),M.push(g++)}_.push(M)}for(let D=0;D<a;D++)for(let M=0;M<r;M++){const v=_[M][D],R=_[M+1][D],U=_[M+1][D+1],C=_[M][D+1];(e>0||M!==0)&&(u.push(v,R,C),y+=3),(t>0||M!==r-1)&&(u.push(R,U,C),y+=3)}l.addGroup(d,y,0),d+=y}function S(x){const T=g,y=new Ke,w=new F;let D=0;const M=x===!0?e:t,v=x===!0?1:-1;for(let U=1;U<=a;U++)h.push(0,p*v,0),f.push(0,v,0),m.push(.5,.5),g++;const R=g;for(let U=0;U<=a;U++){const P=U/a*c+o,N=Math.cos(P),k=Math.sin(P);w.x=M*k,w.y=p*v,w.z=M*N,h.push(w.x,w.y,w.z),f.push(0,v,0),y.x=N*.5+.5,y.y=k*.5*v+.5,m.push(y.x,y.y),g++}for(let U=0;U<a;U++){const C=T+U,P=R+U;x===!0?u.push(P,P+1,C):u.push(P+1,P,C),D+=3}l.addGroup(d,D,x===!0?1:2),d+=D}}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}static fromJSON(e){return new ea(e.radiusTop,e.radiusBottom,e.height,e.radialSegments,e.heightSegments,e.openEnded,e.thetaStart,e.thetaLength)}}class Vs extends ea{constructor(e=1,t=1,i=32,a=1,r=!1,s=0,o=Math.PI*2){super(0,e,t,i,a,r,s,o),this.type="ConeGeometry",this.parameters={radius:e,height:t,radialSegments:i,heightSegments:a,openEnded:r,thetaStart:s,thetaLength:o}}static fromJSON(e){return new Vs(e.radius,e.height,e.radialSegments,e.heightSegments,e.openEnded,e.thetaStart,e.thetaLength)}}const ba=new F,ya=new F,Sr=new F,Ta=new Gt;class Ha extends $e{constructor(e=null,t=1){if(super(),this.type="EdgesGeometry",this.parameters={geometry:e,thresholdAngle:t},e!==null){const a=Math.pow(10,4),r=Math.cos(za*t),s=e.getIndex(),o=e.getAttribute("position"),c=s?s.count:o.count,l=[0,0,0],u=["a","b","c"],h=new Array(3),f={},m=[];for(let g=0;g<c;g+=3){s?(l[0]=s.getX(g),l[1]=s.getX(g+1),l[2]=s.getX(g+2)):(l[0]=g,l[1]=g+1,l[2]=g+2);const{a:_,b:p,c:d}=Ta;if(_.fromBufferAttribute(o,l[0]),p.fromBufferAttribute(o,l[1]),d.fromBufferAttribute(o,l[2]),Ta.getNormal(Sr),h[0]=`${Math.round(_.x*a)},${Math.round(_.y*a)},${Math.round(_.z*a)}`,h[1]=`${Math.round(p.x*a)},${Math.round(p.y*a)},${Math.round(p.z*a)}`,h[2]=`${Math.round(d.x*a)},${Math.round(d.y*a)},${Math.round(d.z*a)}`,!(h[0]===h[1]||h[1]===h[2]||h[2]===h[0]))for(let E=0;E<3;E++){const S=(E+1)%3,x=h[E],T=h[S],y=Ta[u[E]],w=Ta[u[S]],D=`${x}_${T}`,M=`${T}_${x}`;M in f&&f[M]?(Sr.dot(f[M].normal)<=r&&(m.push(y.x,y.y,y.z),m.push(w.x,w.y,w.z)),f[M]=null):D in f||(f[D]={index0:l[E],index1:l[S],normal:Sr.clone()})}}for(const g in f)if(f[g]){const{index0:_,index1:p}=f[g];ba.fromBufferAttribute(o,_),ya.fromBufferAttribute(o,p),m.push(ba.x,ba.y,ba.z),m.push(ya.x,ya.y,ya.z)}this.setAttribute("position",new He(m,3))}}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}}class zi extends $e{constructor(e=1,t=1,i=1,a=1){super(),this.type="PlaneGeometry",this.parameters={width:e,height:t,widthSegments:i,heightSegments:a};const r=e/2,s=t/2,o=Math.floor(i),c=Math.floor(a),l=o+1,u=c+1,h=e/o,f=t/c,m=[],g=[],_=[],p=[];for(let d=0;d<u;d++){const E=d*f-s;for(let S=0;S<l;S++){const x=S*h-r;g.push(x,-E,0),_.push(0,0,1),p.push(S/o),p.push(1-d/c)}}for(let d=0;d<c;d++)for(let E=0;E<o;E++){const S=E+l*d,x=E+l*(d+1),T=E+1+l*(d+1),y=E+1+l*d;m.push(S,x,y),m.push(x,T,y)}this.setIndex(m),this.setAttribute("position",new He(g,3)),this.setAttribute("normal",new He(_,3)),this.setAttribute("uv",new He(p,2))}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}static fromJSON(e){return new zi(e.width,e.height,e.widthSegments,e.heightSegments)}}class js extends $e{constructor(e=.5,t=1,i=32,a=1,r=0,s=Math.PI*2){super(),this.type="RingGeometry",this.parameters={innerRadius:e,outerRadius:t,thetaSegments:i,phiSegments:a,thetaStart:r,thetaLength:s},i=Math.max(3,i),a=Math.max(1,a);const o=[],c=[],l=[],u=[];let h=e;const f=(t-e)/a,m=new F,g=new Ke;for(let _=0;_<=a;_++){for(let p=0;p<=i;p++){const d=r+p/i*s;m.x=h*Math.cos(d),m.y=h*Math.sin(d),c.push(m.x,m.y,m.z),l.push(0,0,1),g.x=(m.x/t+1)/2,g.y=(m.y/t+1)/2,u.push(g.x,g.y)}h+=f}for(let _=0;_<a;_++){const p=_*(i+1);for(let d=0;d<i;d++){const E=d+p,S=E,x=E+i+1,T=E+i+2,y=E+1;o.push(S,x,y),o.push(x,T,y)}}this.setIndex(o),this.setAttribute("position",new He(c,3)),this.setAttribute("normal",new He(l,3)),this.setAttribute("uv",new He(u,2))}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}static fromJSON(e){return new js(e.innerRadius,e.outerRadius,e.thetaSegments,e.phiSegments,e.thetaStart,e.thetaLength)}}class vn extends $e{constructor(e=1,t=32,i=16,a=0,r=Math.PI*2,s=0,o=Math.PI){super(),this.type="SphereGeometry",this.parameters={radius:e,widthSegments:t,heightSegments:i,phiStart:a,phiLength:r,thetaStart:s,thetaLength:o},t=Math.max(3,Math.floor(t)),i=Math.max(2,Math.floor(i));const c=Math.min(s+o,Math.PI);let l=0;const u=[],h=new F,f=new F,m=[],g=[],_=[],p=[];for(let d=0;d<=i;d++){const E=[],S=d/i;let x=0;d===0&&s===0?x=.5/t:d===i&&c===Math.PI&&(x=-.5/t);for(let T=0;T<=t;T++){const y=T/t;h.x=-e*Math.cos(a+y*r)*Math.sin(s+S*o),h.y=e*Math.cos(s+S*o),h.z=e*Math.sin(a+y*r)*Math.sin(s+S*o),g.push(h.x,h.y,h.z),f.copy(h).normalize(),_.push(f.x,f.y,f.z),p.push(y+x,1-S),E.push(l++)}u.push(E)}for(let d=0;d<i;d++)for(let E=0;E<t;E++){const S=u[d][E+1],x=u[d][E],T=u[d+1][E],y=u[d+1][E+1];(d!==0||s>0)&&m.push(S,x,y),(d!==i-1||c<Math.PI)&&m.push(x,T,y)}this.setIndex(m),this.setAttribute("position",new He(g,3)),this.setAttribute("normal",new He(_,3)),this.setAttribute("uv",new He(p,2))}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}static fromJSON(e){return new vn(e.radius,e.widthSegments,e.heightSegments,e.phiStart,e.phiLength,e.thetaStart,e.thetaLength)}}class ct extends Li{constructor(e){super(),this.isMeshStandardMaterial=!0,this.type="MeshStandardMaterial",this.defines={STANDARD:""},this.color=new ce(16777215),this.roughness=1,this.metalness=0,this.map=null,this.lightMap=null,this.lightMapIntensity=1,this.aoMap=null,this.aoMapIntensity=1,this.emissive=new ce(0),this.emissiveIntensity=1,this.emissiveMap=null,this.bumpMap=null,this.bumpScale=1,this.normalMap=null,this.normalMapType=Nc,this.normalScale=new Ke(1,1),this.displacementMap=null,this.displacementScale=1,this.displacementBias=0,this.roughnessMap=null,this.metalnessMap=null,this.alphaMap=null,this.envMap=null,this.envMapRotation=new Mt,this.envMapIntensity=1,this.wireframe=!1,this.wireframeLinewidth=1,this.wireframeLinecap="round",this.wireframeLinejoin="round",this.flatShading=!1,this.fog=!0,this.setValues(e)}copy(e){return super.copy(e),this.defines={STANDARD:""},this.color.copy(e.color),this.roughness=e.roughness,this.metalness=e.metalness,this.map=e.map,this.lightMap=e.lightMap,this.lightMapIntensity=e.lightMapIntensity,this.aoMap=e.aoMap,this.aoMapIntensity=e.aoMapIntensity,this.emissive.copy(e.emissive),this.emissiveMap=e.emissiveMap,this.emissiveIntensity=e.emissiveIntensity,this.bumpMap=e.bumpMap,this.bumpScale=e.bumpScale,this.normalMap=e.normalMap,this.normalMapType=e.normalMapType,this.normalScale.copy(e.normalScale),this.displacementMap=e.displacementMap,this.displacementScale=e.displacementScale,this.displacementBias=e.displacementBias,this.roughnessMap=e.roughnessMap,this.metalnessMap=e.metalnessMap,this.alphaMap=e.alphaMap,this.envMap=e.envMap,this.envMapRotation.copy(e.envMapRotation),this.envMapIntensity=e.envMapIntensity,this.wireframe=e.wireframe,this.wireframeLinewidth=e.wireframeLinewidth,this.wireframeLinecap=e.wireframeLinecap,this.wireframeLinejoin=e.wireframeLinejoin,this.flatShading=e.flatShading,this.fog=e.fog,this}}class Ou extends Li{constructor(e){super(),this.isMeshDepthMaterial=!0,this.type="MeshDepthMaterial",this.depthPacking=Zl,this.map=null,this.alphaMap=null,this.displacementMap=null,this.displacementScale=1,this.displacementBias=0,this.wireframe=!1,this.wireframeLinewidth=1,this.setValues(e)}copy(e){return super.copy(e),this.depthPacking=e.depthPacking,this.map=e.map,this.alphaMap=e.alphaMap,this.displacementMap=e.displacementMap,this.displacementScale=e.displacementScale,this.displacementBias=e.displacementBias,this.wireframe=e.wireframe,this.wireframeLinewidth=e.wireframeLinewidth,this}}class Bu extends Li{constructor(e){super(),this.isMeshDistanceMaterial=!0,this.type="MeshDistanceMaterial",this.map=null,this.alphaMap=null,this.displacementMap=null,this.displacementScale=1,this.displacementBias=0,this.setValues(e)}copy(e){return super.copy(e),this.map=e.map,this.alphaMap=e.alphaMap,this.displacementMap=e.displacementMap,this.displacementScale=e.displacementScale,this.displacementBias=e.displacementBias,this}}class Vu extends ht{constructor(e){super(),this.isLineDashedMaterial=!0,this.type="LineDashedMaterial",this.scale=1,this.dashSize=3,this.gapSize=1,this.setValues(e)}copy(e){return super.copy(e),this.scale=e.scale,this.dashSize=e.dashSize,this.gapSize=e.gapSize,this}}class qc extends Et{constructor(e,t=1){super(),this.isLight=!0,this.type="Light",this.color=new ce(e),this.intensity=t}dispose(){}copy(e,t){return super.copy(e,t),this.color.copy(e.color),this.intensity=e.intensity,this}toJSON(e){const t=super.toJSON(e);return t.object.color=this.color.getHex(),t.object.intensity=this.intensity,this.groundColor!==void 0&&(t.object.groundColor=this.groundColor.getHex()),this.distance!==void 0&&(t.object.distance=this.distance),this.angle!==void 0&&(t.object.angle=this.angle),this.decay!==void 0&&(t.object.decay=this.decay),this.penumbra!==void 0&&(t.object.penumbra=this.penumbra),this.shadow!==void 0&&(t.object.shadow=this.shadow.toJSON()),this.target!==void 0&&(t.object.target=this.target.uuid),t}}const Er=new st,Do=new F,Lo=new F;class ju{constructor(e){this.camera=e,this.intensity=1,this.bias=0,this.normalBias=0,this.radius=1,this.blurSamples=8,this.mapSize=new Ke(512,512),this.map=null,this.mapPass=null,this.matrix=new st,this.autoUpdate=!0,this.needsUpdate=!1,this._frustum=new Bs,this._frameExtents=new Ke(1,1),this._viewportCount=1,this._viewports=[new dt(0,0,1,1)]}getViewportCount(){return this._viewportCount}getFrustum(){return this._frustum}updateMatrices(e){const t=this.camera,i=this.matrix;Do.setFromMatrixPosition(e.matrixWorld),t.position.copy(Do),Lo.setFromMatrixPosition(e.target.matrixWorld),t.lookAt(Lo),t.updateMatrixWorld(),Er.multiplyMatrices(t.projectionMatrix,t.matrixWorldInverse),this._frustum.setFromProjectionMatrix(Er),i.set(.5,0,0,.5,0,.5,0,.5,0,0,.5,.5,0,0,0,1),i.multiply(Er)}getViewport(e){return this._viewports[e]}getFrameExtents(){return this._frameExtents}dispose(){this.map&&this.map.dispose(),this.mapPass&&this.mapPass.dispose()}copy(e){return this.camera=e.camera.clone(),this.intensity=e.intensity,this.bias=e.bias,this.radius=e.radius,this.mapSize.copy(e.mapSize),this}clone(){return new this.constructor().copy(this)}toJSON(){const e={};return this.intensity!==1&&(e.intensity=this.intensity),this.bias!==0&&(e.bias=this.bias),this.normalBias!==0&&(e.normalBias=this.normalBias),this.radius!==1&&(e.radius=this.radius),(this.mapSize.x!==512||this.mapSize.y!==512)&&(e.mapSize=this.mapSize.toArray()),e.camera=this.camera.toJSON(!1).object,delete e.camera.matrix,e}}class $c extends Wc{constructor(e=-1,t=1,i=1,a=-1,r=.1,s=2e3){super(),this.isOrthographicCamera=!0,this.type="OrthographicCamera",this.zoom=1,this.view=null,this.left=e,this.right=t,this.top=i,this.bottom=a,this.near=r,this.far=s,this.updateProjectionMatrix()}copy(e,t){return super.copy(e,t),this.left=e.left,this.right=e.right,this.top=e.top,this.bottom=e.bottom,this.near=e.near,this.far=e.far,this.zoom=e.zoom,this.view=e.view===null?null:Object.assign({},e.view),this}setViewOffset(e,t,i,a,r,s){this.view===null&&(this.view={enabled:!0,fullWidth:1,fullHeight:1,offsetX:0,offsetY:0,width:1,height:1}),this.view.enabled=!0,this.view.fullWidth=e,this.view.fullHeight=t,this.view.offsetX=i,this.view.offsetY=a,this.view.width=r,this.view.height=s,this.updateProjectionMatrix()}clearViewOffset(){this.view!==null&&(this.view.enabled=!1),this.updateProjectionMatrix()}updateProjectionMatrix(){const e=(this.right-this.left)/(2*this.zoom),t=(this.top-this.bottom)/(2*this.zoom),i=(this.right+this.left)/2,a=(this.top+this.bottom)/2;let r=i-e,s=i+e,o=a+t,c=a-t;if(this.view!==null&&this.view.enabled){const l=(this.right-this.left)/this.view.fullWidth/this.zoom,u=(this.top-this.bottom)/this.view.fullHeight/this.zoom;r+=l*this.view.offsetX,s=r+l*this.view.width,o-=u*this.view.offsetY,c=o-u*this.view.height}this.projectionMatrix.makeOrthographic(r,s,o,c,this.near,this.far,this.coordinateSystem),this.projectionMatrixInverse.copy(this.projectionMatrix).invert()}toJSON(e){const t=super.toJSON(e);return t.object.zoom=this.zoom,t.object.left=this.left,t.object.right=this.right,t.object.top=this.top,t.object.bottom=this.bottom,t.object.near=this.near,t.object.far=this.far,this.view!==null&&(t.object.view=Object.assign({},this.view)),t}}class Hu extends ju{constructor(){super(new $c(-5,5,5,-5,.5,500)),this.isDirectionalLightShadow=!0}}class Uo extends qc{constructor(e,t){super(e,t),this.isDirectionalLight=!0,this.type="DirectionalLight",this.position.copy(Et.DEFAULT_UP),this.updateMatrix(),this.target=new Et,this.shadow=new Hu}dispose(){this.shadow.dispose()}copy(e){return super.copy(e),this.target=e.target.clone(),this.shadow=e.shadow.clone(),this}}class Gu extends qc{constructor(e,t){super(e,t),this.isAmbientLight=!0,this.type="AmbientLight"}}class Wu extends Ht{constructor(e=[]){super(),this.isArrayCamera=!0,this.cameras=e,this.index=0}}const zo=new st;class Hs{constructor(e,t,i=0,a=1/0){this.ray=new Fs(e,t),this.near=i,this.far=a,this.camera=null,this.layers=new Os,this.params={Mesh:{},Line:{threshold:1},LOD:{},Points:{threshold:1},Sprite:{}}}set(e,t){this.ray.set(e,t)}setFromCamera(e,t){t.isPerspectiveCamera?(this.ray.origin.setFromMatrixPosition(t.matrixWorld),this.ray.direction.set(e.x,e.y,.5).unproject(t).sub(this.ray.origin).normalize(),this.camera=t):t.isOrthographicCamera?(this.ray.origin.set(e.x,e.y,(t.near+t.far)/(t.near-t.far)).unproject(t),this.ray.direction.set(0,0,-1).transformDirection(t.matrixWorld),this.camera=t):console.error("THREE.Raycaster: Unsupported camera type: "+t.type)}setFromXRController(e){return zo.identity().extractRotation(e.matrixWorld),this.ray.origin.setFromMatrixPosition(e.matrixWorld),this.ray.direction.set(0,0,-1).applyMatrix4(zo),this}intersectObject(e,t=!0,i=[]){return Ss(e,this,i,t),i.sort(ko),i}intersectObjects(e,t=!0,i=[]){for(let a=0,r=e.length;a<r;a++)Ss(e[a],this,i,t);return i.sort(ko),i}}function ko(n,e){return n.distance-e.distance}function Ss(n,e,t,i){let a=!0;if(n.layers.test(e.layers)&&n.raycast(e,t)===!1&&(a=!1),a===!0&&i===!0){const r=n.children;for(let s=0,o=r.length;s<o;s++)Ss(r[s],e,t,!0)}}function No(n,e,t,i){const a=Xu(i);switch(t){case Pc:return n*e;case Dc:return n*e;case Lc:return n*e*2;case Uc:return n*e/a.components*a.byteLength;case Us:return n*e/a.components*a.byteLength;case zc:return n*e*2/a.components*a.byteLength;case zs:return n*e*2/a.components*a.byteLength;case Ic:return n*e*3/a.components*a.byteLength;case Zt:return n*e*4/a.components*a.byteLength;case ks:return n*e*4/a.components*a.byteLength;case Pa:case Ia:return Math.floor((n+3)/4)*Math.floor((e+3)/4)*8;case Da:case La:return Math.floor((n+3)/4)*Math.floor((e+3)/4)*16;case $r:case Zr:return Math.max(n,16)*Math.max(e,8)/4;case qr:case Yr:return Math.max(n,8)*Math.max(e,8)/2;case Jr:case Qr:return Math.floor((n+3)/4)*Math.floor((e+3)/4)*8;case es:return Math.floor((n+3)/4)*Math.floor((e+3)/4)*16;case ts:return Math.floor((n+3)/4)*Math.floor((e+3)/4)*16;case ns:return Math.floor((n+4)/5)*Math.floor((e+3)/4)*16;case is:return Math.floor((n+4)/5)*Math.floor((e+4)/5)*16;case as:return Math.floor((n+5)/6)*Math.floor((e+4)/5)*16;case rs:return Math.floor((n+5)/6)*Math.floor((e+5)/6)*16;case ss:return Math.floor((n+7)/8)*Math.floor((e+4)/5)*16;case os:return Math.floor((n+7)/8)*Math.floor((e+5)/6)*16;case cs:return Math.floor((n+7)/8)*Math.floor((e+7)/8)*16;case ls:return Math.floor((n+9)/10)*Math.floor((e+4)/5)*16;case us:return Math.floor((n+9)/10)*Math.floor((e+5)/6)*16;case ds:return Math.floor((n+9)/10)*Math.floor((e+7)/8)*16;case hs:return Math.floor((n+9)/10)*Math.floor((e+9)/10)*16;case fs:return Math.floor((n+11)/12)*Math.floor((e+9)/10)*16;case ps:return Math.floor((n+11)/12)*Math.floor((e+11)/12)*16;case Ua:case ms:case gs:return Math.ceil(n/4)*Math.ceil(e/4)*16;case kc:case _s:return Math.ceil(n/4)*Math.ceil(e/4)*8;case vs:case xs:return Math.ceil(n/4)*Math.ceil(e/4)*16}throw new Error(`Unable to determine texture byte length for ${t} format.`)}function Xu(n){switch(n){case _n:case wc:return{byteLength:1,components:1};case Ki:case Rc:case Yi:return{byteLength:2,components:1};case Ds:case Ls:return{byteLength:2,components:4};case ei:case Is:case fn:return{byteLength:4,components:1};case Cc:return{byteLength:4,components:3}}throw new Error(`Unknown texture type ${n}.`)}typeof __THREE_DEVTOOLS__<"u"&&__THREE_DEVTOOLS__.dispatchEvent(new CustomEvent("register",{detail:{revision:Ps}}));typeof window<"u"&&(window.__THREE__?console.warn("WARNING: Multiple instances of Three.js being imported."):window.__THREE__=Ps);/**
 * @license
 * Copyright 2010-2025 Three.js Authors
 * SPDX-License-Identifier: MIT
 */function Yc(){let n=null,e=!1,t=null,i=null;function a(r,s){t(r,s),i=n.requestAnimationFrame(a)}return{start:function(){e!==!0&&t!==null&&(i=n.requestAnimationFrame(a),e=!0)},stop:function(){n.cancelAnimationFrame(i),e=!1},setAnimationLoop:function(r){t=r},setContext:function(r){n=r}}}function Ku(n){const e=new WeakMap;function t(o,c){const l=o.array,u=o.usage,h=l.byteLength,f=n.createBuffer();n.bindBuffer(c,f),n.bufferData(c,l,u),o.onUploadCallback();let m;if(l instanceof Float32Array)m=n.FLOAT;else if(l instanceof Uint16Array)o.isFloat16BufferAttribute?m=n.HALF_FLOAT:m=n.UNSIGNED_SHORT;else if(l instanceof Int16Array)m=n.SHORT;else if(l instanceof Uint32Array)m=n.UNSIGNED_INT;else if(l instanceof Int32Array)m=n.INT;else if(l instanceof Int8Array)m=n.BYTE;else if(l instanceof Uint8Array)m=n.UNSIGNED_BYTE;else if(l instanceof Uint8ClampedArray)m=n.UNSIGNED_BYTE;else throw new Error("THREE.WebGLAttributes: Unsupported buffer data format: "+l);return{buffer:f,type:m,bytesPerElement:l.BYTES_PER_ELEMENT,version:o.version,size:h}}function i(o,c,l){const u=c.array,h=c.updateRanges;if(n.bindBuffer(l,o),h.length===0)n.bufferSubData(l,0,u);else{h.sort((m,g)=>m.start-g.start);let f=0;for(let m=1;m<h.length;m++){const g=h[f],_=h[m];_.start<=g.start+g.count+1?g.count=Math.max(g.count,_.start+_.count-g.start):(++f,h[f]=_)}h.length=f+1;for(let m=0,g=h.length;m<g;m++){const _=h[m];n.bufferSubData(l,_.start*u.BYTES_PER_ELEMENT,u,_.start,_.count)}c.clearUpdateRanges()}c.onUploadCallback()}function a(o){return o.isInterleavedBufferAttribute&&(o=o.data),e.get(o)}function r(o){o.isInterleavedBufferAttribute&&(o=o.data);const c=e.get(o);c&&(n.deleteBuffer(c.buffer),e.delete(o))}function s(o,c){if(o.isInterleavedBufferAttribute&&(o=o.data),o.isGLBufferAttribute){const u=e.get(o);(!u||u.version<o.version)&&e.set(o,{buffer:o.buffer,type:o.type,bytesPerElement:o.elementSize,version:o.version});return}const l=e.get(o);if(l===void 0)e.set(o,t(o,c));else if(l.version<o.version){if(l.size!==o.array.byteLength)throw new Error("THREE.WebGLAttributes: The size of the buffer attribute's array buffer does not match the original size. Resizing buffer attributes is not supported.");i(l.buffer,o,c),l.version=o.version}}return{get:a,remove:r,update:s}}var qu=`#ifdef USE_ALPHAHASH
	if ( diffuseColor.a < getAlphaHashThreshold( vPosition ) ) discard;
#endif`,$u=`#ifdef USE_ALPHAHASH
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
#endif`,Yu=`#ifdef USE_ALPHAMAP
	diffuseColor.a *= texture2D( alphaMap, vAlphaMapUv ).g;
#endif`,Zu=`#ifdef USE_ALPHAMAP
	uniform sampler2D alphaMap;
#endif`,Ju=`#ifdef USE_ALPHATEST
	#ifdef ALPHA_TO_COVERAGE
	diffuseColor.a = smoothstep( alphaTest, alphaTest + fwidth( diffuseColor.a ), diffuseColor.a );
	if ( diffuseColor.a == 0.0 ) discard;
	#else
	if ( diffuseColor.a < alphaTest ) discard;
	#endif
#endif`,Qu=`#ifdef USE_ALPHATEST
	uniform float alphaTest;
#endif`,ed=`#ifdef USE_AOMAP
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
#endif`,td=`#ifdef USE_AOMAP
	uniform sampler2D aoMap;
	uniform float aoMapIntensity;
#endif`,nd=`#ifdef USE_BATCHING
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
#endif`,id=`#ifdef USE_BATCHING
	mat4 batchingMatrix = getBatchingMatrix( getIndirectIndex( gl_DrawID ) );
#endif`,ad=`vec3 transformed = vec3( position );
#ifdef USE_ALPHAHASH
	vPosition = vec3( position );
#endif`,rd=`vec3 objectNormal = vec3( normal );
#ifdef USE_TANGENT
	vec3 objectTangent = vec3( tangent.xyz );
#endif`,sd=`float G_BlinnPhong_Implicit( ) {
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
} // validated`,od=`#ifdef USE_IRIDESCENCE
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
#endif`,cd=`#ifdef USE_BUMPMAP
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
#endif`,ld=`#if NUM_CLIPPING_PLANES > 0
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
#endif`,ud=`#if NUM_CLIPPING_PLANES > 0
	varying vec3 vClipPosition;
	uniform vec4 clippingPlanes[ NUM_CLIPPING_PLANES ];
#endif`,dd=`#if NUM_CLIPPING_PLANES > 0
	varying vec3 vClipPosition;
#endif`,hd=`#if NUM_CLIPPING_PLANES > 0
	vClipPosition = - mvPosition.xyz;
#endif`,fd=`#if defined( USE_COLOR_ALPHA )
	diffuseColor *= vColor;
#elif defined( USE_COLOR )
	diffuseColor.rgb *= vColor;
#endif`,pd=`#if defined( USE_COLOR_ALPHA )
	varying vec4 vColor;
#elif defined( USE_COLOR )
	varying vec3 vColor;
#endif`,md=`#if defined( USE_COLOR_ALPHA )
	varying vec4 vColor;
#elif defined( USE_COLOR ) || defined( USE_INSTANCING_COLOR ) || defined( USE_BATCHING_COLOR )
	varying vec3 vColor;
#endif`,gd=`#if defined( USE_COLOR_ALPHA )
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
#endif`,_d=`#define PI 3.141592653589793
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
} // validated`,vd=`#ifdef ENVMAP_TYPE_CUBE_UV
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
#endif`,xd=`vec3 transformedNormal = objectNormal;
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
#endif`,Md=`#ifdef USE_DISPLACEMENTMAP
	uniform sampler2D displacementMap;
	uniform float displacementScale;
	uniform float displacementBias;
#endif`,Sd=`#ifdef USE_DISPLACEMENTMAP
	transformed += normalize( objectNormal ) * ( texture2D( displacementMap, vDisplacementMapUv ).x * displacementScale + displacementBias );
#endif`,Ed=`#ifdef USE_EMISSIVEMAP
	vec4 emissiveColor = texture2D( emissiveMap, vEmissiveMapUv );
	#ifdef DECODE_VIDEO_TEXTURE_EMISSIVE
		emissiveColor = sRGBTransferEOTF( emissiveColor );
	#endif
	totalEmissiveRadiance *= emissiveColor.rgb;
#endif`,bd=`#ifdef USE_EMISSIVEMAP
	uniform sampler2D emissiveMap;
#endif`,yd="gl_FragColor = linearToOutputTexel( gl_FragColor );",Td=`vec4 LinearTransferOETF( in vec4 value ) {
	return value;
}
vec4 sRGBTransferEOTF( in vec4 value ) {
	return vec4( mix( pow( value.rgb * 0.9478672986 + vec3( 0.0521327014 ), vec3( 2.4 ) ), value.rgb * 0.0773993808, vec3( lessThanEqual( value.rgb, vec3( 0.04045 ) ) ) ), value.a );
}
vec4 sRGBTransferOETF( in vec4 value ) {
	return vec4( mix( pow( value.rgb, vec3( 0.41666 ) ) * 1.055 - vec3( 0.055 ), value.rgb * 12.92, vec3( lessThanEqual( value.rgb, vec3( 0.0031308 ) ) ) ), value.a );
}`,Ad=`#ifdef USE_ENVMAP
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
#endif`,wd=`#ifdef USE_ENVMAP
	uniform float envMapIntensity;
	uniform float flipEnvMap;
	uniform mat3 envMapRotation;
	#ifdef ENVMAP_TYPE_CUBE
		uniform samplerCube envMap;
	#else
		uniform sampler2D envMap;
	#endif
	
#endif`,Rd=`#ifdef USE_ENVMAP
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
#endif`,Cd=`#ifdef USE_ENVMAP
	#if defined( USE_BUMPMAP ) || defined( USE_NORMALMAP ) || defined( PHONG ) || defined( LAMBERT )
		#define ENV_WORLDPOS
	#endif
	#ifdef ENV_WORLDPOS
		
		varying vec3 vWorldPosition;
	#else
		varying vec3 vReflect;
		uniform float refractionRatio;
	#endif
#endif`,Pd=`#ifdef USE_ENVMAP
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
#endif`,Id=`#ifdef USE_FOG
	vFogDepth = - mvPosition.z;
#endif`,Dd=`#ifdef USE_FOG
	varying float vFogDepth;
#endif`,Ld=`#ifdef USE_FOG
	#ifdef FOG_EXP2
		float fogFactor = 1.0 - exp( - fogDensity * fogDensity * vFogDepth * vFogDepth );
	#else
		float fogFactor = smoothstep( fogNear, fogFar, vFogDepth );
	#endif
	gl_FragColor.rgb = mix( gl_FragColor.rgb, fogColor, fogFactor );
#endif`,Ud=`#ifdef USE_FOG
	uniform vec3 fogColor;
	varying float vFogDepth;
	#ifdef FOG_EXP2
		uniform float fogDensity;
	#else
		uniform float fogNear;
		uniform float fogFar;
	#endif
#endif`,zd=`#ifdef USE_GRADIENTMAP
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
}`,kd=`#ifdef USE_LIGHTMAP
	uniform sampler2D lightMap;
	uniform float lightMapIntensity;
#endif`,Nd=`LambertMaterial material;
material.diffuseColor = diffuseColor.rgb;
material.specularStrength = specularStrength;`,Fd=`varying vec3 vViewPosition;
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
#define RE_IndirectDiffuse		RE_IndirectDiffuse_Lambert`,Od=`uniform bool receiveShadow;
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
#endif`,Bd=`#ifdef USE_ENVMAP
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
#endif`,Vd=`ToonMaterial material;
material.diffuseColor = diffuseColor.rgb;`,jd=`varying vec3 vViewPosition;
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
#define RE_IndirectDiffuse		RE_IndirectDiffuse_Toon`,Hd=`BlinnPhongMaterial material;
material.diffuseColor = diffuseColor.rgb;
material.specularColor = specular;
material.specularShininess = shininess;
material.specularStrength = specularStrength;`,Gd=`varying vec3 vViewPosition;
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
#define RE_IndirectDiffuse		RE_IndirectDiffuse_BlinnPhong`,Wd=`PhysicalMaterial material;
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
#endif`,Xd=`struct PhysicalMaterial {
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
}`,Kd=`
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
#endif`,qd=`#if defined( RE_IndirectDiffuse )
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
#endif`,$d=`#if defined( RE_IndirectDiffuse )
	RE_IndirectDiffuse( irradiance, geometryPosition, geometryNormal, geometryViewDir, geometryClearcoatNormal, material, reflectedLight );
#endif
#if defined( RE_IndirectSpecular )
	RE_IndirectSpecular( radiance, iblIrradiance, clearcoatRadiance, geometryPosition, geometryNormal, geometryViewDir, geometryClearcoatNormal, material, reflectedLight );
#endif`,Yd=`#if defined( USE_LOGDEPTHBUF )
	gl_FragDepth = vIsPerspective == 0.0 ? gl_FragCoord.z : log2( vFragDepth ) * logDepthBufFC * 0.5;
#endif`,Zd=`#if defined( USE_LOGDEPTHBUF )
	uniform float logDepthBufFC;
	varying float vFragDepth;
	varying float vIsPerspective;
#endif`,Jd=`#ifdef USE_LOGDEPTHBUF
	varying float vFragDepth;
	varying float vIsPerspective;
#endif`,Qd=`#ifdef USE_LOGDEPTHBUF
	vFragDepth = 1.0 + gl_Position.w;
	vIsPerspective = float( isPerspectiveMatrix( projectionMatrix ) );
#endif`,eh=`#ifdef USE_MAP
	vec4 sampledDiffuseColor = texture2D( map, vMapUv );
	#ifdef DECODE_VIDEO_TEXTURE
		sampledDiffuseColor = sRGBTransferEOTF( sampledDiffuseColor );
	#endif
	diffuseColor *= sampledDiffuseColor;
#endif`,th=`#ifdef USE_MAP
	uniform sampler2D map;
#endif`,nh=`#if defined( USE_MAP ) || defined( USE_ALPHAMAP )
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
#endif`,ih=`#if defined( USE_POINTS_UV )
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
#endif`,ah=`float metalnessFactor = metalness;
#ifdef USE_METALNESSMAP
	vec4 texelMetalness = texture2D( metalnessMap, vMetalnessMapUv );
	metalnessFactor *= texelMetalness.b;
#endif`,rh=`#ifdef USE_METALNESSMAP
	uniform sampler2D metalnessMap;
#endif`,sh=`#ifdef USE_INSTANCING_MORPH
	float morphTargetInfluences[ MORPHTARGETS_COUNT ];
	float morphTargetBaseInfluence = texelFetch( morphTexture, ivec2( 0, gl_InstanceID ), 0 ).r;
	for ( int i = 0; i < MORPHTARGETS_COUNT; i ++ ) {
		morphTargetInfluences[i] =  texelFetch( morphTexture, ivec2( i + 1, gl_InstanceID ), 0 ).r;
	}
#endif`,oh=`#if defined( USE_MORPHCOLORS )
	vColor *= morphTargetBaseInfluence;
	for ( int i = 0; i < MORPHTARGETS_COUNT; i ++ ) {
		#if defined( USE_COLOR_ALPHA )
			if ( morphTargetInfluences[ i ] != 0.0 ) vColor += getMorph( gl_VertexID, i, 2 ) * morphTargetInfluences[ i ];
		#elif defined( USE_COLOR )
			if ( morphTargetInfluences[ i ] != 0.0 ) vColor += getMorph( gl_VertexID, i, 2 ).rgb * morphTargetInfluences[ i ];
		#endif
	}
#endif`,ch=`#ifdef USE_MORPHNORMALS
	objectNormal *= morphTargetBaseInfluence;
	for ( int i = 0; i < MORPHTARGETS_COUNT; i ++ ) {
		if ( morphTargetInfluences[ i ] != 0.0 ) objectNormal += getMorph( gl_VertexID, i, 1 ).xyz * morphTargetInfluences[ i ];
	}
#endif`,lh=`#ifdef USE_MORPHTARGETS
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
#endif`,uh=`#ifdef USE_MORPHTARGETS
	transformed *= morphTargetBaseInfluence;
	for ( int i = 0; i < MORPHTARGETS_COUNT; i ++ ) {
		if ( morphTargetInfluences[ i ] != 0.0 ) transformed += getMorph( gl_VertexID, i, 0 ).xyz * morphTargetInfluences[ i ];
	}
#endif`,dh=`float faceDirection = gl_FrontFacing ? 1.0 : - 1.0;
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
vec3 nonPerturbedNormal = normal;`,hh=`#ifdef USE_NORMALMAP_OBJECTSPACE
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
#endif`,fh=`#ifndef FLAT_SHADED
	varying vec3 vNormal;
	#ifdef USE_TANGENT
		varying vec3 vTangent;
		varying vec3 vBitangent;
	#endif
#endif`,ph=`#ifndef FLAT_SHADED
	varying vec3 vNormal;
	#ifdef USE_TANGENT
		varying vec3 vTangent;
		varying vec3 vBitangent;
	#endif
#endif`,mh=`#ifndef FLAT_SHADED
	vNormal = normalize( transformedNormal );
	#ifdef USE_TANGENT
		vTangent = normalize( transformedTangent );
		vBitangent = normalize( cross( vNormal, vTangent ) * tangent.w );
	#endif
#endif`,gh=`#ifdef USE_NORMALMAP
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
#endif`,_h=`#ifdef USE_CLEARCOAT
	vec3 clearcoatNormal = nonPerturbedNormal;
#endif`,vh=`#ifdef USE_CLEARCOAT_NORMALMAP
	vec3 clearcoatMapN = texture2D( clearcoatNormalMap, vClearcoatNormalMapUv ).xyz * 2.0 - 1.0;
	clearcoatMapN.xy *= clearcoatNormalScale;
	clearcoatNormal = normalize( tbn2 * clearcoatMapN );
#endif`,xh=`#ifdef USE_CLEARCOATMAP
	uniform sampler2D clearcoatMap;
#endif
#ifdef USE_CLEARCOAT_NORMALMAP
	uniform sampler2D clearcoatNormalMap;
	uniform vec2 clearcoatNormalScale;
#endif
#ifdef USE_CLEARCOAT_ROUGHNESSMAP
	uniform sampler2D clearcoatRoughnessMap;
#endif`,Mh=`#ifdef USE_IRIDESCENCEMAP
	uniform sampler2D iridescenceMap;
#endif
#ifdef USE_IRIDESCENCE_THICKNESSMAP
	uniform sampler2D iridescenceThicknessMap;
#endif`,Sh=`#ifdef OPAQUE
diffuseColor.a = 1.0;
#endif
#ifdef USE_TRANSMISSION
diffuseColor.a *= material.transmissionAlpha;
#endif
gl_FragColor = vec4( outgoingLight, diffuseColor.a );`,Eh=`vec3 packNormalToRGB( const in vec3 normal ) {
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
}`,bh=`#ifdef PREMULTIPLIED_ALPHA
	gl_FragColor.rgb *= gl_FragColor.a;
#endif`,yh=`vec4 mvPosition = vec4( transformed, 1.0 );
#ifdef USE_BATCHING
	mvPosition = batchingMatrix * mvPosition;
#endif
#ifdef USE_INSTANCING
	mvPosition = instanceMatrix * mvPosition;
#endif
mvPosition = modelViewMatrix * mvPosition;
gl_Position = projectionMatrix * mvPosition;`,Th=`#ifdef DITHERING
	gl_FragColor.rgb = dithering( gl_FragColor.rgb );
#endif`,Ah=`#ifdef DITHERING
	vec3 dithering( vec3 color ) {
		float grid_position = rand( gl_FragCoord.xy );
		vec3 dither_shift_RGB = vec3( 0.25 / 255.0, -0.25 / 255.0, 0.25 / 255.0 );
		dither_shift_RGB = mix( 2.0 * dither_shift_RGB, -2.0 * dither_shift_RGB, grid_position );
		return color + dither_shift_RGB;
	}
#endif`,wh=`float roughnessFactor = roughness;
#ifdef USE_ROUGHNESSMAP
	vec4 texelRoughness = texture2D( roughnessMap, vRoughnessMapUv );
	roughnessFactor *= texelRoughness.g;
#endif`,Rh=`#ifdef USE_ROUGHNESSMAP
	uniform sampler2D roughnessMap;
#endif`,Ch=`#if NUM_SPOT_LIGHT_COORDS > 0
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
#endif`,Ph=`#if NUM_SPOT_LIGHT_COORDS > 0
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
#endif`,Ih=`#if ( defined( USE_SHADOWMAP ) && ( NUM_DIR_LIGHT_SHADOWS > 0 || NUM_POINT_LIGHT_SHADOWS > 0 ) ) || ( NUM_SPOT_LIGHT_COORDS > 0 )
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
#endif`,Dh=`float getShadowMask() {
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
}`,Lh=`#ifdef USE_SKINNING
	mat4 boneMatX = getBoneMatrix( skinIndex.x );
	mat4 boneMatY = getBoneMatrix( skinIndex.y );
	mat4 boneMatZ = getBoneMatrix( skinIndex.z );
	mat4 boneMatW = getBoneMatrix( skinIndex.w );
#endif`,Uh=`#ifdef USE_SKINNING
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
#endif`,zh=`#ifdef USE_SKINNING
	vec4 skinVertex = bindMatrix * vec4( transformed, 1.0 );
	vec4 skinned = vec4( 0.0 );
	skinned += boneMatX * skinVertex * skinWeight.x;
	skinned += boneMatY * skinVertex * skinWeight.y;
	skinned += boneMatZ * skinVertex * skinWeight.z;
	skinned += boneMatW * skinVertex * skinWeight.w;
	transformed = ( bindMatrixInverse * skinned ).xyz;
#endif`,kh=`#ifdef USE_SKINNING
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
#endif`,Nh=`float specularStrength;
#ifdef USE_SPECULARMAP
	vec4 texelSpecular = texture2D( specularMap, vSpecularMapUv );
	specularStrength = texelSpecular.r;
#else
	specularStrength = 1.0;
#endif`,Fh=`#ifdef USE_SPECULARMAP
	uniform sampler2D specularMap;
#endif`,Oh=`#if defined( TONE_MAPPING )
	gl_FragColor.rgb = toneMapping( gl_FragColor.rgb );
#endif`,Bh=`#ifndef saturate
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
vec3 CustomToneMapping( vec3 color ) { return color; }`,Vh=`#ifdef USE_TRANSMISSION
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
#endif`,jh=`#ifdef USE_TRANSMISSION
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
#endif`,Hh=`#if defined( USE_UV ) || defined( USE_ANISOTROPY )
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
#endif`,Gh=`#if defined( USE_UV ) || defined( USE_ANISOTROPY )
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
#endif`,Wh=`#if defined( USE_UV ) || defined( USE_ANISOTROPY )
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
#endif`,Xh=`#if defined( USE_ENVMAP ) || defined( DISTANCE ) || defined ( USE_SHADOWMAP ) || defined ( USE_TRANSMISSION ) || NUM_SPOT_LIGHT_COORDS > 0
	vec4 worldPosition = vec4( transformed, 1.0 );
	#ifdef USE_BATCHING
		worldPosition = batchingMatrix * worldPosition;
	#endif
	#ifdef USE_INSTANCING
		worldPosition = instanceMatrix * worldPosition;
	#endif
	worldPosition = modelMatrix * worldPosition;
#endif`;const Kh=`varying vec2 vUv;
uniform mat3 uvTransform;
void main() {
	vUv = ( uvTransform * vec3( uv, 1 ) ).xy;
	gl_Position = vec4( position.xy, 1.0, 1.0 );
}`,qh=`uniform sampler2D t2D;
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
}`,$h=`varying vec3 vWorldDirection;
#include <common>
void main() {
	vWorldDirection = transformDirection( position, modelMatrix );
	#include <begin_vertex>
	#include <project_vertex>
	gl_Position.z = gl_Position.w;
}`,Yh=`#ifdef ENVMAP_TYPE_CUBE
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
}`,Zh=`varying vec3 vWorldDirection;
#include <common>
void main() {
	vWorldDirection = transformDirection( position, modelMatrix );
	#include <begin_vertex>
	#include <project_vertex>
	gl_Position.z = gl_Position.w;
}`,Jh=`uniform samplerCube tCube;
uniform float tFlip;
uniform float opacity;
varying vec3 vWorldDirection;
void main() {
	vec4 texColor = textureCube( tCube, vec3( tFlip * vWorldDirection.x, vWorldDirection.yz ) );
	gl_FragColor = texColor;
	gl_FragColor.a *= opacity;
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
}`,Qh=`#include <common>
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
}`,ef=`#if DEPTH_PACKING == 3200
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
}`,tf=`#define DISTANCE
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
}`,nf=`#define DISTANCE
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
}`,af=`varying vec3 vWorldDirection;
#include <common>
void main() {
	vWorldDirection = transformDirection( position, modelMatrix );
	#include <begin_vertex>
	#include <project_vertex>
}`,rf=`uniform sampler2D tEquirect;
varying vec3 vWorldDirection;
#include <common>
void main() {
	vec3 direction = normalize( vWorldDirection );
	vec2 sampleUV = equirectUv( direction );
	gl_FragColor = texture2D( tEquirect, sampleUV );
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
}`,sf=`uniform float scale;
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
}`,of=`uniform vec3 diffuse;
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
}`,cf=`#include <common>
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
}`,lf=`uniform vec3 diffuse;
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
}`,uf=`#define LAMBERT
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
}`,df=`#define LAMBERT
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
}`,hf=`#define MATCAP
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
}`,ff=`#define MATCAP
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
}`,pf=`#define NORMAL
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
}`,mf=`#define NORMAL
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
}`,gf=`#define PHONG
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
}`,_f=`#define PHONG
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
}`,vf=`#define STANDARD
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
}`,xf=`#define STANDARD
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
}`,Mf=`#define TOON
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
}`,Sf=`#define TOON
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
}`,Ef=`uniform float size;
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
}`,bf=`uniform vec3 diffuse;
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
}`,yf=`#include <common>
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
}`,Tf=`uniform vec3 color;
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
}`,Af=`uniform float rotation;
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
}`,wf=`uniform vec3 diffuse;
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
}`,je={alphahash_fragment:qu,alphahash_pars_fragment:$u,alphamap_fragment:Yu,alphamap_pars_fragment:Zu,alphatest_fragment:Ju,alphatest_pars_fragment:Qu,aomap_fragment:ed,aomap_pars_fragment:td,batching_pars_vertex:nd,batching_vertex:id,begin_vertex:ad,beginnormal_vertex:rd,bsdfs:sd,iridescence_fragment:od,bumpmap_pars_fragment:cd,clipping_planes_fragment:ld,clipping_planes_pars_fragment:ud,clipping_planes_pars_vertex:dd,clipping_planes_vertex:hd,color_fragment:fd,color_pars_fragment:pd,color_pars_vertex:md,color_vertex:gd,common:_d,cube_uv_reflection_fragment:vd,defaultnormal_vertex:xd,displacementmap_pars_vertex:Md,displacementmap_vertex:Sd,emissivemap_fragment:Ed,emissivemap_pars_fragment:bd,colorspace_fragment:yd,colorspace_pars_fragment:Td,envmap_fragment:Ad,envmap_common_pars_fragment:wd,envmap_pars_fragment:Rd,envmap_pars_vertex:Cd,envmap_physical_pars_fragment:Bd,envmap_vertex:Pd,fog_vertex:Id,fog_pars_vertex:Dd,fog_fragment:Ld,fog_pars_fragment:Ud,gradientmap_pars_fragment:zd,lightmap_pars_fragment:kd,lights_lambert_fragment:Nd,lights_lambert_pars_fragment:Fd,lights_pars_begin:Od,lights_toon_fragment:Vd,lights_toon_pars_fragment:jd,lights_phong_fragment:Hd,lights_phong_pars_fragment:Gd,lights_physical_fragment:Wd,lights_physical_pars_fragment:Xd,lights_fragment_begin:Kd,lights_fragment_maps:qd,lights_fragment_end:$d,logdepthbuf_fragment:Yd,logdepthbuf_pars_fragment:Zd,logdepthbuf_pars_vertex:Jd,logdepthbuf_vertex:Qd,map_fragment:eh,map_pars_fragment:th,map_particle_fragment:nh,map_particle_pars_fragment:ih,metalnessmap_fragment:ah,metalnessmap_pars_fragment:rh,morphinstance_vertex:sh,morphcolor_vertex:oh,morphnormal_vertex:ch,morphtarget_pars_vertex:lh,morphtarget_vertex:uh,normal_fragment_begin:dh,normal_fragment_maps:hh,normal_pars_fragment:fh,normal_pars_vertex:ph,normal_vertex:mh,normalmap_pars_fragment:gh,clearcoat_normal_fragment_begin:_h,clearcoat_normal_fragment_maps:vh,clearcoat_pars_fragment:xh,iridescence_pars_fragment:Mh,opaque_fragment:Sh,packing:Eh,premultiplied_alpha_fragment:bh,project_vertex:yh,dithering_fragment:Th,dithering_pars_fragment:Ah,roughnessmap_fragment:wh,roughnessmap_pars_fragment:Rh,shadowmap_pars_fragment:Ch,shadowmap_pars_vertex:Ph,shadowmap_vertex:Ih,shadowmask_pars_fragment:Dh,skinbase_vertex:Lh,skinning_pars_vertex:Uh,skinning_vertex:zh,skinnormal_vertex:kh,specularmap_fragment:Nh,specularmap_pars_fragment:Fh,tonemapping_fragment:Oh,tonemapping_pars_fragment:Bh,transmission_fragment:Vh,transmission_pars_fragment:jh,uv_pars_fragment:Hh,uv_pars_vertex:Gh,uv_vertex:Wh,worldpos_vertex:Xh,background_vert:Kh,background_frag:qh,backgroundCube_vert:$h,backgroundCube_frag:Yh,cube_vert:Zh,cube_frag:Jh,depth_vert:Qh,depth_frag:ef,distanceRGBA_vert:tf,distanceRGBA_frag:nf,equirect_vert:af,equirect_frag:rf,linedashed_vert:sf,linedashed_frag:of,meshbasic_vert:cf,meshbasic_frag:lf,meshlambert_vert:uf,meshlambert_frag:df,meshmatcap_vert:hf,meshmatcap_frag:ff,meshnormal_vert:pf,meshnormal_frag:mf,meshphong_vert:gf,meshphong_frag:_f,meshphysical_vert:vf,meshphysical_frag:xf,meshtoon_vert:Mf,meshtoon_frag:Sf,points_vert:Ef,points_frag:bf,shadow_vert:yf,shadow_frag:Tf,sprite_vert:Af,sprite_frag:wf},he={common:{diffuse:{value:new ce(16777215)},opacity:{value:1},map:{value:null},mapTransform:{value:new Be},alphaMap:{value:null},alphaMapTransform:{value:new Be},alphaTest:{value:0}},specularmap:{specularMap:{value:null},specularMapTransform:{value:new Be}},envmap:{envMap:{value:null},envMapRotation:{value:new Be},flipEnvMap:{value:-1},reflectivity:{value:1},ior:{value:1.5},refractionRatio:{value:.98}},aomap:{aoMap:{value:null},aoMapIntensity:{value:1},aoMapTransform:{value:new Be}},lightmap:{lightMap:{value:null},lightMapIntensity:{value:1},lightMapTransform:{value:new Be}},bumpmap:{bumpMap:{value:null},bumpMapTransform:{value:new Be},bumpScale:{value:1}},normalmap:{normalMap:{value:null},normalMapTransform:{value:new Be},normalScale:{value:new Ke(1,1)}},displacementmap:{displacementMap:{value:null},displacementMapTransform:{value:new Be},displacementScale:{value:1},displacementBias:{value:0}},emissivemap:{emissiveMap:{value:null},emissiveMapTransform:{value:new Be}},metalnessmap:{metalnessMap:{value:null},metalnessMapTransform:{value:new Be}},roughnessmap:{roughnessMap:{value:null},roughnessMapTransform:{value:new Be}},gradientmap:{gradientMap:{value:null}},fog:{fogDensity:{value:25e-5},fogNear:{value:1},fogFar:{value:2e3},fogColor:{value:new ce(16777215)}},lights:{ambientLightColor:{value:[]},lightProbe:{value:[]},directionalLights:{value:[],properties:{direction:{},color:{}}},directionalLightShadows:{value:[],properties:{shadowIntensity:1,shadowBias:{},shadowNormalBias:{},shadowRadius:{},shadowMapSize:{}}},directionalShadowMap:{value:[]},directionalShadowMatrix:{value:[]},spotLights:{value:[],properties:{color:{},position:{},direction:{},distance:{},coneCos:{},penumbraCos:{},decay:{}}},spotLightShadows:{value:[],properties:{shadowIntensity:1,shadowBias:{},shadowNormalBias:{},shadowRadius:{},shadowMapSize:{}}},spotLightMap:{value:[]},spotShadowMap:{value:[]},spotLightMatrix:{value:[]},pointLights:{value:[],properties:{color:{},position:{},decay:{},distance:{}}},pointLightShadows:{value:[],properties:{shadowIntensity:1,shadowBias:{},shadowNormalBias:{},shadowRadius:{},shadowMapSize:{},shadowCameraNear:{},shadowCameraFar:{}}},pointShadowMap:{value:[]},pointShadowMatrix:{value:[]},hemisphereLights:{value:[],properties:{direction:{},skyColor:{},groundColor:{}}},rectAreaLights:{value:[],properties:{color:{},position:{},width:{},height:{}}},ltc_1:{value:null},ltc_2:{value:null}},points:{diffuse:{value:new ce(16777215)},opacity:{value:1},size:{value:1},scale:{value:1},map:{value:null},alphaMap:{value:null},alphaMapTransform:{value:new Be},alphaTest:{value:0},uvTransform:{value:new Be}},sprite:{diffuse:{value:new ce(16777215)},opacity:{value:1},center:{value:new Ke(.5,.5)},rotation:{value:0},map:{value:null},mapTransform:{value:new Be},alphaMap:{value:null},alphaMapTransform:{value:new Be},alphaTest:{value:0}}},Qt={basic:{uniforms:Rt([he.common,he.specularmap,he.envmap,he.aomap,he.lightmap,he.fog]),vertexShader:je.meshbasic_vert,fragmentShader:je.meshbasic_frag},lambert:{uniforms:Rt([he.common,he.specularmap,he.envmap,he.aomap,he.lightmap,he.emissivemap,he.bumpmap,he.normalmap,he.displacementmap,he.fog,he.lights,{emissive:{value:new ce(0)}}]),vertexShader:je.meshlambert_vert,fragmentShader:je.meshlambert_frag},phong:{uniforms:Rt([he.common,he.specularmap,he.envmap,he.aomap,he.lightmap,he.emissivemap,he.bumpmap,he.normalmap,he.displacementmap,he.fog,he.lights,{emissive:{value:new ce(0)},specular:{value:new ce(1118481)},shininess:{value:30}}]),vertexShader:je.meshphong_vert,fragmentShader:je.meshphong_frag},standard:{uniforms:Rt([he.common,he.envmap,he.aomap,he.lightmap,he.emissivemap,he.bumpmap,he.normalmap,he.displacementmap,he.roughnessmap,he.metalnessmap,he.fog,he.lights,{emissive:{value:new ce(0)},roughness:{value:1},metalness:{value:0},envMapIntensity:{value:1}}]),vertexShader:je.meshphysical_vert,fragmentShader:je.meshphysical_frag},toon:{uniforms:Rt([he.common,he.aomap,he.lightmap,he.emissivemap,he.bumpmap,he.normalmap,he.displacementmap,he.gradientmap,he.fog,he.lights,{emissive:{value:new ce(0)}}]),vertexShader:je.meshtoon_vert,fragmentShader:je.meshtoon_frag},matcap:{uniforms:Rt([he.common,he.bumpmap,he.normalmap,he.displacementmap,he.fog,{matcap:{value:null}}]),vertexShader:je.meshmatcap_vert,fragmentShader:je.meshmatcap_frag},points:{uniforms:Rt([he.points,he.fog]),vertexShader:je.points_vert,fragmentShader:je.points_frag},dashed:{uniforms:Rt([he.common,he.fog,{scale:{value:1},dashSize:{value:1},totalSize:{value:2}}]),vertexShader:je.linedashed_vert,fragmentShader:je.linedashed_frag},depth:{uniforms:Rt([he.common,he.displacementmap]),vertexShader:je.depth_vert,fragmentShader:je.depth_frag},normal:{uniforms:Rt([he.common,he.bumpmap,he.normalmap,he.displacementmap,{opacity:{value:1}}]),vertexShader:je.meshnormal_vert,fragmentShader:je.meshnormal_frag},sprite:{uniforms:Rt([he.sprite,he.fog]),vertexShader:je.sprite_vert,fragmentShader:je.sprite_frag},background:{uniforms:{uvTransform:{value:new Be},t2D:{value:null},backgroundIntensity:{value:1}},vertexShader:je.background_vert,fragmentShader:je.background_frag},backgroundCube:{uniforms:{envMap:{value:null},flipEnvMap:{value:-1},backgroundBlurriness:{value:0},backgroundIntensity:{value:1},backgroundRotation:{value:new Be}},vertexShader:je.backgroundCube_vert,fragmentShader:je.backgroundCube_frag},cube:{uniforms:{tCube:{value:null},tFlip:{value:-1},opacity:{value:1}},vertexShader:je.cube_vert,fragmentShader:je.cube_frag},equirect:{uniforms:{tEquirect:{value:null}},vertexShader:je.equirect_vert,fragmentShader:je.equirect_frag},distanceRGBA:{uniforms:Rt([he.common,he.displacementmap,{referencePosition:{value:new F},nearDistance:{value:1},farDistance:{value:1e3}}]),vertexShader:je.distanceRGBA_vert,fragmentShader:je.distanceRGBA_frag},shadow:{uniforms:Rt([he.lights,he.fog,{color:{value:new ce(0)},opacity:{value:1}}]),vertexShader:je.shadow_vert,fragmentShader:je.shadow_frag}};Qt.physical={uniforms:Rt([Qt.standard.uniforms,{clearcoat:{value:0},clearcoatMap:{value:null},clearcoatMapTransform:{value:new Be},clearcoatNormalMap:{value:null},clearcoatNormalMapTransform:{value:new Be},clearcoatNormalScale:{value:new Ke(1,1)},clearcoatRoughness:{value:0},clearcoatRoughnessMap:{value:null},clearcoatRoughnessMapTransform:{value:new Be},dispersion:{value:0},iridescence:{value:0},iridescenceMap:{value:null},iridescenceMapTransform:{value:new Be},iridescenceIOR:{value:1.3},iridescenceThicknessMinimum:{value:100},iridescenceThicknessMaximum:{value:400},iridescenceThicknessMap:{value:null},iridescenceThicknessMapTransform:{value:new Be},sheen:{value:0},sheenColor:{value:new ce(0)},sheenColorMap:{value:null},sheenColorMapTransform:{value:new Be},sheenRoughness:{value:1},sheenRoughnessMap:{value:null},sheenRoughnessMapTransform:{value:new Be},transmission:{value:0},transmissionMap:{value:null},transmissionMapTransform:{value:new Be},transmissionSamplerSize:{value:new Ke},transmissionSamplerMap:{value:null},thickness:{value:0},thicknessMap:{value:null},thicknessMapTransform:{value:new Be},attenuationDistance:{value:0},attenuationColor:{value:new ce(0)},specularColor:{value:new ce(1,1,1)},specularColorMap:{value:null},specularColorMapTransform:{value:new Be},specularIntensity:{value:1},specularIntensityMap:{value:null},specularIntensityMapTransform:{value:new Be},anisotropyVector:{value:new Ke},anisotropyMap:{value:null},anisotropyMapTransform:{value:new Be}}]),vertexShader:je.meshphysical_vert,fragmentShader:je.meshphysical_frag};const Aa={r:0,b:0,g:0},Vn=new Mt,Rf=new st;function Cf(n,e,t,i,a,r,s){const o=new ce(0);let c=r===!0?0:1,l,u,h=null,f=0,m=null;function g(S){let x=S.isScene===!0?S.background:null;return x&&x.isTexture&&(x=(S.backgroundBlurriness>0?t:e).get(x)),x}function _(S){let x=!1;const T=g(S);T===null?d(o,c):T&&T.isColor&&(d(T,1),x=!0);const y=n.xr.getEnvironmentBlendMode();y==="additive"?i.buffers.color.setClear(0,0,0,1,s):y==="alpha-blend"&&i.buffers.color.setClear(0,0,0,0,s),(n.autoClear||x)&&(i.buffers.depth.setTest(!0),i.buffers.depth.setMask(!0),i.buffers.color.setMask(!0),n.clear(n.autoClearColor,n.autoClearDepth,n.autoClearStencil))}function p(S,x){const T=g(x);T&&(T.isCubeTexture||T.mapping===Ga)?(u===void 0&&(u=new Ge(new mn(1,1,1),new Un({name:"BackgroundCubeMaterial",uniforms:Ii(Qt.backgroundCube.uniforms),vertexShader:Qt.backgroundCube.vertexShader,fragmentShader:Qt.backgroundCube.fragmentShader,side:Lt,depthTest:!1,depthWrite:!1,fog:!1})),u.geometry.deleteAttribute("normal"),u.geometry.deleteAttribute("uv"),u.onBeforeRender=function(y,w,D){this.matrixWorld.copyPosition(D.matrixWorld)},Object.defineProperty(u.material,"envMap",{get:function(){return this.uniforms.envMap.value}}),a.update(u)),Vn.copy(x.backgroundRotation),Vn.x*=-1,Vn.y*=-1,Vn.z*=-1,T.isCubeTexture&&T.isRenderTargetTexture===!1&&(Vn.y*=-1,Vn.z*=-1),u.material.uniforms.envMap.value=T,u.material.uniforms.flipEnvMap.value=T.isCubeTexture&&T.isRenderTargetTexture===!1?-1:1,u.material.uniforms.backgroundBlurriness.value=x.backgroundBlurriness,u.material.uniforms.backgroundIntensity.value=x.backgroundIntensity,u.material.uniforms.backgroundRotation.value.setFromMatrix4(Rf.makeRotationFromEuler(Vn)),u.material.toneMapped=Qe.getTransfer(T.colorSpace)!==at,(h!==T||f!==T.version||m!==n.toneMapping)&&(u.material.needsUpdate=!0,h=T,f=T.version,m=n.toneMapping),u.layers.enableAll(),S.unshift(u,u.geometry,u.material,0,0,null)):T&&T.isTexture&&(l===void 0&&(l=new Ge(new zi(2,2),new Un({name:"BackgroundMaterial",uniforms:Ii(Qt.background.uniforms),vertexShader:Qt.background.vertexShader,fragmentShader:Qt.background.fragmentShader,side:Ln,depthTest:!1,depthWrite:!1,fog:!1})),l.geometry.deleteAttribute("normal"),Object.defineProperty(l.material,"map",{get:function(){return this.uniforms.t2D.value}}),a.update(l)),l.material.uniforms.t2D.value=T,l.material.uniforms.backgroundIntensity.value=x.backgroundIntensity,l.material.toneMapped=Qe.getTransfer(T.colorSpace)!==at,T.matrixAutoUpdate===!0&&T.updateMatrix(),l.material.uniforms.uvTransform.value.copy(T.matrix),(h!==T||f!==T.version||m!==n.toneMapping)&&(l.material.needsUpdate=!0,h=T,f=T.version,m=n.toneMapping),l.layers.enableAll(),S.unshift(l,l.geometry,l.material,0,0,null))}function d(S,x){S.getRGB(Aa,Gc(n)),i.buffers.color.setClear(Aa.r,Aa.g,Aa.b,x,s)}function E(){u!==void 0&&(u.geometry.dispose(),u.material.dispose(),u=void 0),l!==void 0&&(l.geometry.dispose(),l.material.dispose(),l=void 0)}return{getClearColor:function(){return o},setClearColor:function(S,x=1){o.set(S),c=x,d(o,c)},getClearAlpha:function(){return c},setClearAlpha:function(S){c=S,d(o,c)},render:_,addToRenderList:p,dispose:E}}function Pf(n,e){const t=n.getParameter(n.MAX_VERTEX_ATTRIBS),i={},a=f(null);let r=a,s=!1;function o(v,R,U,C,P){let N=!1;const k=h(C,U,R);r!==k&&(r=k,l(r.object)),N=m(v,C,U,P),N&&g(v,C,U,P),P!==null&&e.update(P,n.ELEMENT_ARRAY_BUFFER),(N||s)&&(s=!1,x(v,R,U,C),P!==null&&n.bindBuffer(n.ELEMENT_ARRAY_BUFFER,e.get(P).buffer))}function c(){return n.createVertexArray()}function l(v){return n.bindVertexArray(v)}function u(v){return n.deleteVertexArray(v)}function h(v,R,U){const C=U.wireframe===!0;let P=i[v.id];P===void 0&&(P={},i[v.id]=P);let N=P[R.id];N===void 0&&(N={},P[R.id]=N);let k=N[C];return k===void 0&&(k=f(c()),N[C]=k),k}function f(v){const R=[],U=[],C=[];for(let P=0;P<t;P++)R[P]=0,U[P]=0,C[P]=0;return{geometry:null,program:null,wireframe:!1,newAttributes:R,enabledAttributes:U,attributeDivisors:C,object:v,attributes:{},index:null}}function m(v,R,U,C){const P=r.attributes,N=R.attributes;let k=0;const O=U.getAttributes();for(const z in O)if(O[z].location>=0){const $=P[z];let Y=N[z];if(Y===void 0&&(z==="instanceMatrix"&&v.instanceMatrix&&(Y=v.instanceMatrix),z==="instanceColor"&&v.instanceColor&&(Y=v.instanceColor)),$===void 0||$.attribute!==Y||Y&&$.data!==Y.data)return!0;k++}return r.attributesNum!==k||r.index!==C}function g(v,R,U,C){const P={},N=R.attributes;let k=0;const O=U.getAttributes();for(const z in O)if(O[z].location>=0){let $=N[z];$===void 0&&(z==="instanceMatrix"&&v.instanceMatrix&&($=v.instanceMatrix),z==="instanceColor"&&v.instanceColor&&($=v.instanceColor));const Y={};Y.attribute=$,$&&$.data&&(Y.data=$.data),P[z]=Y,k++}r.attributes=P,r.attributesNum=k,r.index=C}function _(){const v=r.newAttributes;for(let R=0,U=v.length;R<U;R++)v[R]=0}function p(v){d(v,0)}function d(v,R){const U=r.newAttributes,C=r.enabledAttributes,P=r.attributeDivisors;U[v]=1,C[v]===0&&(n.enableVertexAttribArray(v),C[v]=1),P[v]!==R&&(n.vertexAttribDivisor(v,R),P[v]=R)}function E(){const v=r.newAttributes,R=r.enabledAttributes;for(let U=0,C=R.length;U<C;U++)R[U]!==v[U]&&(n.disableVertexAttribArray(U),R[U]=0)}function S(v,R,U,C,P,N,k){k===!0?n.vertexAttribIPointer(v,R,U,P,N):n.vertexAttribPointer(v,R,U,C,P,N)}function x(v,R,U,C){_();const P=C.attributes,N=U.getAttributes(),k=R.defaultAttributeValues;for(const O in N){const z=N[O];if(z.location>=0){let H=P[O];if(H===void 0&&(O==="instanceMatrix"&&v.instanceMatrix&&(H=v.instanceMatrix),O==="instanceColor"&&v.instanceColor&&(H=v.instanceColor)),H!==void 0){const $=H.normalized,Y=H.itemSize,fe=e.get(H);if(fe===void 0)continue;const Ie=fe.buffer,X=fe.type,ne=fe.bytesPerElement,ue=X===n.INT||X===n.UNSIGNED_INT||H.gpuType===Is;if(H.isInterleavedBufferAttribute){const se=H.data,ee=se.stride,_e=H.offset;if(se.isInstancedInterleavedBuffer){for(let de=0;de<z.locationSize;de++)d(z.location+de,se.meshPerAttribute);v.isInstancedMesh!==!0&&C._maxInstanceCount===void 0&&(C._maxInstanceCount=se.meshPerAttribute*se.count)}else for(let de=0;de<z.locationSize;de++)p(z.location+de);n.bindBuffer(n.ARRAY_BUFFER,Ie);for(let de=0;de<z.locationSize;de++)S(z.location+de,Y/z.locationSize,X,$,ee*ne,(_e+Y/z.locationSize*de)*ne,ue)}else{if(H.isInstancedBufferAttribute){for(let se=0;se<z.locationSize;se++)d(z.location+se,H.meshPerAttribute);v.isInstancedMesh!==!0&&C._maxInstanceCount===void 0&&(C._maxInstanceCount=H.meshPerAttribute*H.count)}else for(let se=0;se<z.locationSize;se++)p(z.location+se);n.bindBuffer(n.ARRAY_BUFFER,Ie);for(let se=0;se<z.locationSize;se++)S(z.location+se,Y/z.locationSize,X,$,Y*ne,Y/z.locationSize*se*ne,ue)}}else if(k!==void 0){const $=k[O];if($!==void 0)switch($.length){case 2:n.vertexAttrib2fv(z.location,$);break;case 3:n.vertexAttrib3fv(z.location,$);break;case 4:n.vertexAttrib4fv(z.location,$);break;default:n.vertexAttrib1fv(z.location,$)}}}}E()}function T(){D();for(const v in i){const R=i[v];for(const U in R){const C=R[U];for(const P in C)u(C[P].object),delete C[P];delete R[U]}delete i[v]}}function y(v){if(i[v.id]===void 0)return;const R=i[v.id];for(const U in R){const C=R[U];for(const P in C)u(C[P].object),delete C[P];delete R[U]}delete i[v.id]}function w(v){for(const R in i){const U=i[R];if(U[v.id]===void 0)continue;const C=U[v.id];for(const P in C)u(C[P].object),delete C[P];delete U[v.id]}}function D(){M(),s=!0,r!==a&&(r=a,l(r.object))}function M(){a.geometry=null,a.program=null,a.wireframe=!1}return{setup:o,reset:D,resetDefaultState:M,dispose:T,releaseStatesOfGeometry:y,releaseStatesOfProgram:w,initAttributes:_,enableAttribute:p,disableUnusedAttributes:E}}function If(n,e,t){let i;function a(l){i=l}function r(l,u){n.drawArrays(i,l,u),t.update(u,i,1)}function s(l,u,h){h!==0&&(n.drawArraysInstanced(i,l,u,h),t.update(u,i,h))}function o(l,u,h){if(h===0)return;e.get("WEBGL_multi_draw").multiDrawArraysWEBGL(i,l,0,u,0,h);let m=0;for(let g=0;g<h;g++)m+=u[g];t.update(m,i,1)}function c(l,u,h,f){if(h===0)return;const m=e.get("WEBGL_multi_draw");if(m===null)for(let g=0;g<l.length;g++)s(l[g],u[g],f[g]);else{m.multiDrawArraysInstancedWEBGL(i,l,0,u,0,f,0,h);let g=0;for(let _=0;_<h;_++)g+=u[_]*f[_];t.update(g,i,1)}}this.setMode=a,this.render=r,this.renderInstances=s,this.renderMultiDraw=o,this.renderMultiDrawInstances=c}function Df(n,e,t,i){let a;function r(){if(a!==void 0)return a;if(e.has("EXT_texture_filter_anisotropic")===!0){const w=e.get("EXT_texture_filter_anisotropic");a=n.getParameter(w.MAX_TEXTURE_MAX_ANISOTROPY_EXT)}else a=0;return a}function s(w){return!(w!==Zt&&i.convert(w)!==n.getParameter(n.IMPLEMENTATION_COLOR_READ_FORMAT))}function o(w){const D=w===Yi&&(e.has("EXT_color_buffer_half_float")||e.has("EXT_color_buffer_float"));return!(w!==_n&&i.convert(w)!==n.getParameter(n.IMPLEMENTATION_COLOR_READ_TYPE)&&w!==fn&&!D)}function c(w){if(w==="highp"){if(n.getShaderPrecisionFormat(n.VERTEX_SHADER,n.HIGH_FLOAT).precision>0&&n.getShaderPrecisionFormat(n.FRAGMENT_SHADER,n.HIGH_FLOAT).precision>0)return"highp";w="mediump"}return w==="mediump"&&n.getShaderPrecisionFormat(n.VERTEX_SHADER,n.MEDIUM_FLOAT).precision>0&&n.getShaderPrecisionFormat(n.FRAGMENT_SHADER,n.MEDIUM_FLOAT).precision>0?"mediump":"lowp"}let l=t.precision!==void 0?t.precision:"highp";const u=c(l);u!==l&&(console.warn("THREE.WebGLRenderer:",l,"not supported, using",u,"instead."),l=u);const h=t.logarithmicDepthBuffer===!0,f=t.reverseDepthBuffer===!0&&e.has("EXT_clip_control"),m=n.getParameter(n.MAX_TEXTURE_IMAGE_UNITS),g=n.getParameter(n.MAX_VERTEX_TEXTURE_IMAGE_UNITS),_=n.getParameter(n.MAX_TEXTURE_SIZE),p=n.getParameter(n.MAX_CUBE_MAP_TEXTURE_SIZE),d=n.getParameter(n.MAX_VERTEX_ATTRIBS),E=n.getParameter(n.MAX_VERTEX_UNIFORM_VECTORS),S=n.getParameter(n.MAX_VARYING_VECTORS),x=n.getParameter(n.MAX_FRAGMENT_UNIFORM_VECTORS),T=g>0,y=n.getParameter(n.MAX_SAMPLES);return{isWebGL2:!0,getMaxAnisotropy:r,getMaxPrecision:c,textureFormatReadable:s,textureTypeReadable:o,precision:l,logarithmicDepthBuffer:h,reverseDepthBuffer:f,maxTextures:m,maxVertexTextures:g,maxTextureSize:_,maxCubemapSize:p,maxAttributes:d,maxVertexUniforms:E,maxVaryings:S,maxFragmentUniforms:x,vertexTextures:T,maxSamples:y}}function Lf(n){const e=this;let t=null,i=0,a=!1,r=!1;const s=new Gn,o=new Be,c={value:null,needsUpdate:!1};this.uniform=c,this.numPlanes=0,this.numIntersection=0,this.init=function(h,f){const m=h.length!==0||f||i!==0||a;return a=f,i=h.length,m},this.beginShadows=function(){r=!0,u(null)},this.endShadows=function(){r=!1},this.setGlobalState=function(h,f){t=u(h,f,0)},this.setState=function(h,f,m){const g=h.clippingPlanes,_=h.clipIntersection,p=h.clipShadows,d=n.get(h);if(!a||g===null||g.length===0||r&&!p)r?u(null):l();else{const E=r?0:i,S=E*4;let x=d.clippingState||null;c.value=x,x=u(g,f,S,m);for(let T=0;T!==S;++T)x[T]=t[T];d.clippingState=x,this.numIntersection=_?this.numPlanes:0,this.numPlanes+=E}};function l(){c.value!==t&&(c.value=t,c.needsUpdate=i>0),e.numPlanes=i,e.numIntersection=0}function u(h,f,m,g){const _=h!==null?h.length:0;let p=null;if(_!==0){if(p=c.value,g!==!0||p===null){const d=m+_*4,E=f.matrixWorldInverse;o.getNormalMatrix(E),(p===null||p.length<d)&&(p=new Float32Array(d));for(let S=0,x=m;S!==_;++S,x+=4)s.copy(h[S]).applyMatrix4(E,o),s.normal.toArray(p,x),p[x+3]=s.constant}c.value=p,c.needsUpdate=!0}return e.numPlanes=_,e.numIntersection=0,p}}function Uf(n){let e=new WeakMap;function t(s,o){return o===Gr?s.mapping=Ai:o===Wr&&(s.mapping=wi),s}function i(s){if(s&&s.isTexture){const o=s.mapping;if(o===Gr||o===Wr)if(e.has(s)){const c=e.get(s).texture;return t(c,s.mapping)}else{const c=s.image;if(c&&c.height>0){const l=new Uu(c.height);return l.fromEquirectangularTexture(n,s),e.set(s,l),s.addEventListener("dispose",a),t(l.texture,s.mapping)}else return null}}return s}function a(s){const o=s.target;o.removeEventListener("dispose",a);const c=e.get(o);c!==void 0&&(e.delete(o),c.dispose())}function r(){e=new WeakMap}return{get:i,dispose:r}}const xi=4,Fo=[.125,.215,.35,.446,.526,.582],$n=20,br=new $c,Oo=new ce;let yr=null,Tr=0,Ar=0,wr=!1;const Wn=(1+Math.sqrt(5))/2,gi=1/Wn,Bo=[new F(-Wn,gi,0),new F(Wn,gi,0),new F(-gi,0,Wn),new F(gi,0,Wn),new F(0,Wn,-gi),new F(0,Wn,gi),new F(-1,1,-1),new F(1,1,-1),new F(-1,1,1),new F(1,1,1)],zf=new F;class Vo{constructor(e){this._renderer=e,this._pingPongRenderTarget=null,this._lodMax=0,this._cubeSize=0,this._lodPlanes=[],this._sizeLods=[],this._sigmas=[],this._blurMaterial=null,this._cubemapMaterial=null,this._equirectMaterial=null,this._compileMaterial(this._blurMaterial)}fromScene(e,t=0,i=.1,a=100,r={}){const{size:s=256,position:o=zf}=r;yr=this._renderer.getRenderTarget(),Tr=this._renderer.getActiveCubeFace(),Ar=this._renderer.getActiveMipmapLevel(),wr=this._renderer.xr.enabled,this._renderer.xr.enabled=!1,this._setSize(s);const c=this._allocateTargets();return c.depthBuffer=!0,this._sceneToCubeUV(e,i,a,c,o),t>0&&this._blur(c,0,0,t),this._applyPMREM(c),this._cleanup(c),c}fromEquirectangular(e,t=null){return this._fromTexture(e,t)}fromCubemap(e,t=null){return this._fromTexture(e,t)}compileCubemapShader(){this._cubemapMaterial===null&&(this._cubemapMaterial=Go(),this._compileMaterial(this._cubemapMaterial))}compileEquirectangularShader(){this._equirectMaterial===null&&(this._equirectMaterial=Ho(),this._compileMaterial(this._equirectMaterial))}dispose(){this._dispose(),this._cubemapMaterial!==null&&this._cubemapMaterial.dispose(),this._equirectMaterial!==null&&this._equirectMaterial.dispose()}_setSize(e){this._lodMax=Math.floor(Math.log2(e)),this._cubeSize=Math.pow(2,this._lodMax)}_dispose(){this._blurMaterial!==null&&this._blurMaterial.dispose(),this._pingPongRenderTarget!==null&&this._pingPongRenderTarget.dispose();for(let e=0;e<this._lodPlanes.length;e++)this._lodPlanes[e].dispose()}_cleanup(e){this._renderer.setRenderTarget(yr,Tr,Ar),this._renderer.xr.enabled=wr,e.scissorTest=!1,wa(e,0,0,e.width,e.height)}_fromTexture(e,t){e.mapping===Ai||e.mapping===wi?this._setSize(e.image.length===0?16:e.image[0].width||e.image[0].image.width):this._setSize(e.image.width/4),yr=this._renderer.getRenderTarget(),Tr=this._renderer.getActiveCubeFace(),Ar=this._renderer.getActiveMipmapLevel(),wr=this._renderer.xr.enabled,this._renderer.xr.enabled=!1;const i=t||this._allocateTargets();return this._textureToCubeUV(e,i),this._applyPMREM(i),this._cleanup(i),i}_allocateTargets(){const e=3*Math.max(this._cubeSize,112),t=4*this._cubeSize,i={magFilter:en,minFilter:en,generateMipmaps:!1,type:Yi,format:Zt,colorSpace:Pi,depthBuffer:!1},a=jo(e,t,i);if(this._pingPongRenderTarget===null||this._pingPongRenderTarget.width!==e||this._pingPongRenderTarget.height!==t){this._pingPongRenderTarget!==null&&this._dispose(),this._pingPongRenderTarget=jo(e,t,i);const{_lodMax:r}=this;({sizeLods:this._sizeLods,lodPlanes:this._lodPlanes,sigmas:this._sigmas}=kf(r)),this._blurMaterial=Nf(r,e,t)}return a}_compileMaterial(e){const t=new Ge(this._lodPlanes[0],e);this._renderer.compile(t,br)}_sceneToCubeUV(e,t,i,a,r){const c=new Ht(90,1,t,i),l=[1,-1,1,1,1,1],u=[1,1,1,-1,-1,-1],h=this._renderer,f=h.autoClear,m=h.toneMapping;h.getClearColor(Oo),h.toneMapping=Dn,h.autoClear=!1;const g=new Ui({name:"PMREM.Background",side:Lt,depthWrite:!1,depthTest:!1}),_=new Ge(new mn,g);let p=!1;const d=e.background;d?d.isColor&&(g.color.copy(d),e.background=null,p=!0):(g.color.copy(Oo),p=!0);for(let E=0;E<6;E++){const S=E%3;S===0?(c.up.set(0,l[E],0),c.position.set(r.x,r.y,r.z),c.lookAt(r.x+u[E],r.y,r.z)):S===1?(c.up.set(0,0,l[E]),c.position.set(r.x,r.y,r.z),c.lookAt(r.x,r.y+u[E],r.z)):(c.up.set(0,l[E],0),c.position.set(r.x,r.y,r.z),c.lookAt(r.x,r.y,r.z+u[E]));const x=this._cubeSize;wa(a,S*x,E>2?x:0,x,x),h.setRenderTarget(a),p&&h.render(_,c),h.render(e,c)}_.geometry.dispose(),_.material.dispose(),h.toneMapping=m,h.autoClear=f,e.background=d}_textureToCubeUV(e,t){const i=this._renderer,a=e.mapping===Ai||e.mapping===wi;a?(this._cubemapMaterial===null&&(this._cubemapMaterial=Go()),this._cubemapMaterial.uniforms.flipEnvMap.value=e.isRenderTargetTexture===!1?-1:1):this._equirectMaterial===null&&(this._equirectMaterial=Ho());const r=a?this._cubemapMaterial:this._equirectMaterial,s=new Ge(this._lodPlanes[0],r),o=r.uniforms;o.envMap.value=e;const c=this._cubeSize;wa(t,0,0,3*c,2*c),i.setRenderTarget(t),i.render(s,br)}_applyPMREM(e){const t=this._renderer,i=t.autoClear;t.autoClear=!1;const a=this._lodPlanes.length;for(let r=1;r<a;r++){const s=Math.sqrt(this._sigmas[r]*this._sigmas[r]-this._sigmas[r-1]*this._sigmas[r-1]),o=Bo[(a-r-1)%Bo.length];this._blur(e,r-1,r,s,o)}t.autoClear=i}_blur(e,t,i,a,r){const s=this._pingPongRenderTarget;this._halfBlur(e,s,t,i,a,"latitudinal",r),this._halfBlur(s,e,i,i,a,"longitudinal",r)}_halfBlur(e,t,i,a,r,s,o){const c=this._renderer,l=this._blurMaterial;s!=="latitudinal"&&s!=="longitudinal"&&console.error("blur direction must be either latitudinal or longitudinal!");const u=3,h=new Ge(this._lodPlanes[a],l),f=l.uniforms,m=this._sizeLods[i]-1,g=isFinite(r)?Math.PI/(2*m):2*Math.PI/(2*$n-1),_=r/g,p=isFinite(r)?1+Math.floor(u*_):$n;p>$n&&console.warn(`sigmaRadians, ${r}, is too large and will clip, as it requested ${p} samples when the maximum is set to ${$n}`);const d=[];let E=0;for(let w=0;w<$n;++w){const D=w/_,M=Math.exp(-D*D/2);d.push(M),w===0?E+=M:w<p&&(E+=2*M)}for(let w=0;w<d.length;w++)d[w]=d[w]/E;f.envMap.value=e.texture,f.samples.value=p,f.weights.value=d,f.latitudinal.value=s==="latitudinal",o&&(f.poleAxis.value=o);const{_lodMax:S}=this;f.dTheta.value=g,f.mipInt.value=S-i;const x=this._sizeLods[a],T=3*x*(a>S-xi?a-S+xi:0),y=4*(this._cubeSize-x);wa(t,T,y,3*x,2*x),c.setRenderTarget(t),c.render(h,br)}}function kf(n){const e=[],t=[],i=[];let a=n;const r=n-xi+1+Fo.length;for(let s=0;s<r;s++){const o=Math.pow(2,a);t.push(o);let c=1/o;s>n-xi?c=Fo[s-n+xi-1]:s===0&&(c=0),i.push(c);const l=1/(o-2),u=-l,h=1+l,f=[u,u,h,u,h,h,u,u,h,h,u,h],m=6,g=6,_=3,p=2,d=1,E=new Float32Array(_*g*m),S=new Float32Array(p*g*m),x=new Float32Array(d*g*m);for(let y=0;y<m;y++){const w=y%3*2/3-1,D=y>2?0:-1,M=[w,D,0,w+2/3,D,0,w+2/3,D+1,0,w,D,0,w+2/3,D+1,0,w,D+1,0];E.set(M,_*g*y),S.set(f,p*g*y);const v=[y,y,y,y,y,y];x.set(v,d*g*y)}const T=new $e;T.setAttribute("position",new tn(E,_)),T.setAttribute("uv",new tn(S,p)),T.setAttribute("faceIndex",new tn(x,d)),e.push(T),a>xi&&a--}return{lodPlanes:e,sizeLods:t,sigmas:i}}function jo(n,e,t){const i=new ti(n,e,t);return i.texture.mapping=Ga,i.texture.name="PMREM.cubeUv",i.scissorTest=!0,i}function wa(n,e,t,i,a){n.viewport.set(e,t,i,a),n.scissor.set(e,t,i,a)}function Nf(n,e,t){const i=new Float32Array($n),a=new F(0,1,0);return new Un({name:"SphericalGaussianBlur",defines:{n:$n,CUBEUV_TEXEL_WIDTH:1/e,CUBEUV_TEXEL_HEIGHT:1/t,CUBEUV_MAX_MIP:`${n}.0`},uniforms:{envMap:{value:null},samples:{value:1},weights:{value:i},latitudinal:{value:!1},dTheta:{value:0},mipInt:{value:0},poleAxis:{value:a}},vertexShader:Gs(),fragmentShader:`

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
		`,blending:In,depthTest:!1,depthWrite:!1})}function Ho(){return new Un({name:"EquirectangularToCubeUV",uniforms:{envMap:{value:null}},vertexShader:Gs(),fragmentShader:`

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
		`,blending:In,depthTest:!1,depthWrite:!1})}function Go(){return new Un({name:"CubemapToCubeUV",uniforms:{envMap:{value:null},flipEnvMap:{value:-1}},vertexShader:Gs(),fragmentShader:`

			precision mediump float;
			precision mediump int;

			uniform float flipEnvMap;

			varying vec3 vOutputDirection;

			uniform samplerCube envMap;

			void main() {

				gl_FragColor = textureCube( envMap, vec3( flipEnvMap * vOutputDirection.x, vOutputDirection.yz ) );

			}
		`,blending:In,depthTest:!1,depthWrite:!1})}function Gs(){return`

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
	`}function Ff(n){let e=new WeakMap,t=null;function i(o){if(o&&o.isTexture){const c=o.mapping,l=c===Gr||c===Wr,u=c===Ai||c===wi;if(l||u){let h=e.get(o);const f=h!==void 0?h.texture.pmremVersion:0;if(o.isRenderTargetTexture&&o.pmremVersion!==f)return t===null&&(t=new Vo(n)),h=l?t.fromEquirectangular(o,h):t.fromCubemap(o,h),h.texture.pmremVersion=o.pmremVersion,e.set(o,h),h.texture;if(h!==void 0)return h.texture;{const m=o.image;return l&&m&&m.height>0||u&&m&&a(m)?(t===null&&(t=new Vo(n)),h=l?t.fromEquirectangular(o):t.fromCubemap(o),h.texture.pmremVersion=o.pmremVersion,e.set(o,h),o.addEventListener("dispose",r),h.texture):null}}}return o}function a(o){let c=0;const l=6;for(let u=0;u<l;u++)o[u]!==void 0&&c++;return c===l}function r(o){const c=o.target;c.removeEventListener("dispose",r);const l=e.get(c);l!==void 0&&(e.delete(c),l.dispose())}function s(){e=new WeakMap,t!==null&&(t.dispose(),t=null)}return{get:i,dispose:s}}function Of(n){const e={};function t(i){if(e[i]!==void 0)return e[i];let a;switch(i){case"WEBGL_depth_texture":a=n.getExtension("WEBGL_depth_texture")||n.getExtension("MOZ_WEBGL_depth_texture")||n.getExtension("WEBKIT_WEBGL_depth_texture");break;case"EXT_texture_filter_anisotropic":a=n.getExtension("EXT_texture_filter_anisotropic")||n.getExtension("MOZ_EXT_texture_filter_anisotropic")||n.getExtension("WEBKIT_EXT_texture_filter_anisotropic");break;case"WEBGL_compressed_texture_s3tc":a=n.getExtension("WEBGL_compressed_texture_s3tc")||n.getExtension("MOZ_WEBGL_compressed_texture_s3tc")||n.getExtension("WEBKIT_WEBGL_compressed_texture_s3tc");break;case"WEBGL_compressed_texture_pvrtc":a=n.getExtension("WEBGL_compressed_texture_pvrtc")||n.getExtension("WEBKIT_WEBGL_compressed_texture_pvrtc");break;default:a=n.getExtension(i)}return e[i]=a,a}return{has:function(i){return t(i)!==null},init:function(){t("EXT_color_buffer_float"),t("WEBGL_clip_cull_distance"),t("OES_texture_float_linear"),t("EXT_color_buffer_half_float"),t("WEBGL_multisampled_render_to_texture"),t("WEBGL_render_shared_exponent")},get:function(i){const a=t(i);return a===null&&Hn("THREE.WebGLRenderer: "+i+" extension not supported."),a}}}function Bf(n,e,t,i){const a={},r=new WeakMap;function s(h){const f=h.target;f.index!==null&&e.remove(f.index);for(const g in f.attributes)e.remove(f.attributes[g]);f.removeEventListener("dispose",s),delete a[f.id];const m=r.get(f);m&&(e.remove(m),r.delete(f)),i.releaseStatesOfGeometry(f),f.isInstancedBufferGeometry===!0&&delete f._maxInstanceCount,t.memory.geometries--}function o(h,f){return a[f.id]===!0||(f.addEventListener("dispose",s),a[f.id]=!0,t.memory.geometries++),f}function c(h){const f=h.attributes;for(const m in f)e.update(f[m],n.ARRAY_BUFFER)}function l(h){const f=[],m=h.index,g=h.attributes.position;let _=0;if(m!==null){const E=m.array;_=m.version;for(let S=0,x=E.length;S<x;S+=3){const T=E[S+0],y=E[S+1],w=E[S+2];f.push(T,y,y,w,w,T)}}else if(g!==void 0){const E=g.array;_=g.version;for(let S=0,x=E.length/3-1;S<x;S+=3){const T=S+0,y=S+1,w=S+2;f.push(T,y,y,w,w,T)}}else return;const p=new(Oc(f)?Hc:jc)(f,1);p.version=_;const d=r.get(h);d&&e.remove(d),r.set(h,p)}function u(h){const f=r.get(h);if(f){const m=h.index;m!==null&&f.version<m.version&&l(h)}else l(h);return r.get(h)}return{get:o,update:c,getWireframeAttribute:u}}function Vf(n,e,t){let i;function a(f){i=f}let r,s;function o(f){r=f.type,s=f.bytesPerElement}function c(f,m){n.drawElements(i,m,r,f*s),t.update(m,i,1)}function l(f,m,g){g!==0&&(n.drawElementsInstanced(i,m,r,f*s,g),t.update(m,i,g))}function u(f,m,g){if(g===0)return;e.get("WEBGL_multi_draw").multiDrawElementsWEBGL(i,m,0,r,f,0,g);let p=0;for(let d=0;d<g;d++)p+=m[d];t.update(p,i,1)}function h(f,m,g,_){if(g===0)return;const p=e.get("WEBGL_multi_draw");if(p===null)for(let d=0;d<f.length;d++)l(f[d]/s,m[d],_[d]);else{p.multiDrawElementsInstancedWEBGL(i,m,0,r,f,0,_,0,g);let d=0;for(let E=0;E<g;E++)d+=m[E]*_[E];t.update(d,i,1)}}this.setMode=a,this.setIndex=o,this.render=c,this.renderInstances=l,this.renderMultiDraw=u,this.renderMultiDrawInstances=h}function jf(n){const e={geometries:0,textures:0},t={frame:0,calls:0,triangles:0,points:0,lines:0};function i(r,s,o){switch(t.calls++,s){case n.TRIANGLES:t.triangles+=o*(r/3);break;case n.LINES:t.lines+=o*(r/2);break;case n.LINE_STRIP:t.lines+=o*(r-1);break;case n.LINE_LOOP:t.lines+=o*r;break;case n.POINTS:t.points+=o*r;break;default:console.error("THREE.WebGLInfo: Unknown draw mode:",s);break}}function a(){t.calls=0,t.triangles=0,t.points=0,t.lines=0}return{memory:e,render:t,programs:null,autoReset:!0,reset:a,update:i}}function Hf(n,e,t){const i=new WeakMap,a=new dt;function r(s,o,c){const l=s.morphTargetInfluences,u=o.morphAttributes.position||o.morphAttributes.normal||o.morphAttributes.color,h=u!==void 0?u.length:0;let f=i.get(o);if(f===void 0||f.count!==h){let M=function(){w.dispose(),i.delete(o),o.removeEventListener("dispose",M)};f!==void 0&&f.texture.dispose();const m=o.morphAttributes.position!==void 0,g=o.morphAttributes.normal!==void 0,_=o.morphAttributes.color!==void 0,p=o.morphAttributes.position||[],d=o.morphAttributes.normal||[],E=o.morphAttributes.color||[];let S=0;m===!0&&(S=1),g===!0&&(S=2),_===!0&&(S=3);let x=o.attributes.position.count*S,T=1;x>e.maxTextureSize&&(T=Math.ceil(x/e.maxTextureSize),x=e.maxTextureSize);const y=new Float32Array(x*T*4*h),w=new Bc(y,x,T,h);w.type=fn,w.needsUpdate=!0;const D=S*4;for(let v=0;v<h;v++){const R=p[v],U=d[v],C=E[v],P=x*T*4*v;for(let N=0;N<R.count;N++){const k=N*D;m===!0&&(a.fromBufferAttribute(R,N),y[P+k+0]=a.x,y[P+k+1]=a.y,y[P+k+2]=a.z,y[P+k+3]=0),g===!0&&(a.fromBufferAttribute(U,N),y[P+k+4]=a.x,y[P+k+5]=a.y,y[P+k+6]=a.z,y[P+k+7]=0),_===!0&&(a.fromBufferAttribute(C,N),y[P+k+8]=a.x,y[P+k+9]=a.y,y[P+k+10]=a.z,y[P+k+11]=C.itemSize===4?a.w:1)}}f={count:h,texture:w,size:new Ke(x,T)},i.set(o,f),o.addEventListener("dispose",M)}if(s.isInstancedMesh===!0&&s.morphTexture!==null)c.getUniforms().setValue(n,"morphTexture",s.morphTexture,t);else{let m=0;for(let _=0;_<l.length;_++)m+=l[_];const g=o.morphTargetsRelative?1:1-m;c.getUniforms().setValue(n,"morphTargetBaseInfluence",g),c.getUniforms().setValue(n,"morphTargetInfluences",l)}c.getUniforms().setValue(n,"morphTargetsTexture",f.texture,t),c.getUniforms().setValue(n,"morphTargetsTextureSize",f.size)}return{update:r}}function Gf(n,e,t,i){let a=new WeakMap;function r(c){const l=i.render.frame,u=c.geometry,h=e.get(c,u);if(a.get(h)!==l&&(e.update(h),a.set(h,l)),c.isInstancedMesh&&(c.hasEventListener("dispose",o)===!1&&c.addEventListener("dispose",o),a.get(c)!==l&&(t.update(c.instanceMatrix,n.ARRAY_BUFFER),c.instanceColor!==null&&t.update(c.instanceColor,n.ARRAY_BUFFER),a.set(c,l))),c.isSkinnedMesh){const f=c.skeleton;a.get(f)!==l&&(f.update(),a.set(f,l))}return h}function s(){a=new WeakMap}function o(c){const l=c.target;l.removeEventListener("dispose",o),t.remove(l.instanceMatrix),l.instanceColor!==null&&t.remove(l.instanceColor)}return{update:r,dispose:s}}const Zc=new Ct,Wo=new Kc(1,1),Jc=new Bc,Qc=new _u,el=new Xc,Xo=[],Ko=[],qo=new Float32Array(16),$o=new Float32Array(9),Yo=new Float32Array(4);function ki(n,e,t){const i=n[0];if(i<=0||i>0)return n;const a=e*t;let r=Xo[a];if(r===void 0&&(r=new Float32Array(a),Xo[a]=r),e!==0){i.toArray(r,0);for(let s=1,o=0;s!==e;++s)o+=t,n[s].toArray(r,o)}return r}function _t(n,e){if(n.length!==e.length)return!1;for(let t=0,i=n.length;t<i;t++)if(n[t]!==e[t])return!1;return!0}function vt(n,e){for(let t=0,i=e.length;t<i;t++)n[t]=e[t]}function Xa(n,e){let t=Ko[e];t===void 0&&(t=new Int32Array(e),Ko[e]=t);for(let i=0;i!==e;++i)t[i]=n.allocateTextureUnit();return t}function Wf(n,e){const t=this.cache;t[0]!==e&&(n.uniform1f(this.addr,e),t[0]=e)}function Xf(n,e){const t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y)&&(n.uniform2f(this.addr,e.x,e.y),t[0]=e.x,t[1]=e.y);else{if(_t(t,e))return;n.uniform2fv(this.addr,e),vt(t,e)}}function Kf(n,e){const t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y||t[2]!==e.z)&&(n.uniform3f(this.addr,e.x,e.y,e.z),t[0]=e.x,t[1]=e.y,t[2]=e.z);else if(e.r!==void 0)(t[0]!==e.r||t[1]!==e.g||t[2]!==e.b)&&(n.uniform3f(this.addr,e.r,e.g,e.b),t[0]=e.r,t[1]=e.g,t[2]=e.b);else{if(_t(t,e))return;n.uniform3fv(this.addr,e),vt(t,e)}}function qf(n,e){const t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y||t[2]!==e.z||t[3]!==e.w)&&(n.uniform4f(this.addr,e.x,e.y,e.z,e.w),t[0]=e.x,t[1]=e.y,t[2]=e.z,t[3]=e.w);else{if(_t(t,e))return;n.uniform4fv(this.addr,e),vt(t,e)}}function $f(n,e){const t=this.cache,i=e.elements;if(i===void 0){if(_t(t,e))return;n.uniformMatrix2fv(this.addr,!1,e),vt(t,e)}else{if(_t(t,i))return;Yo.set(i),n.uniformMatrix2fv(this.addr,!1,Yo),vt(t,i)}}function Yf(n,e){const t=this.cache,i=e.elements;if(i===void 0){if(_t(t,e))return;n.uniformMatrix3fv(this.addr,!1,e),vt(t,e)}else{if(_t(t,i))return;$o.set(i),n.uniformMatrix3fv(this.addr,!1,$o),vt(t,i)}}function Zf(n,e){const t=this.cache,i=e.elements;if(i===void 0){if(_t(t,e))return;n.uniformMatrix4fv(this.addr,!1,e),vt(t,e)}else{if(_t(t,i))return;qo.set(i),n.uniformMatrix4fv(this.addr,!1,qo),vt(t,i)}}function Jf(n,e){const t=this.cache;t[0]!==e&&(n.uniform1i(this.addr,e),t[0]=e)}function Qf(n,e){const t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y)&&(n.uniform2i(this.addr,e.x,e.y),t[0]=e.x,t[1]=e.y);else{if(_t(t,e))return;n.uniform2iv(this.addr,e),vt(t,e)}}function ep(n,e){const t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y||t[2]!==e.z)&&(n.uniform3i(this.addr,e.x,e.y,e.z),t[0]=e.x,t[1]=e.y,t[2]=e.z);else{if(_t(t,e))return;n.uniform3iv(this.addr,e),vt(t,e)}}function tp(n,e){const t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y||t[2]!==e.z||t[3]!==e.w)&&(n.uniform4i(this.addr,e.x,e.y,e.z,e.w),t[0]=e.x,t[1]=e.y,t[2]=e.z,t[3]=e.w);else{if(_t(t,e))return;n.uniform4iv(this.addr,e),vt(t,e)}}function np(n,e){const t=this.cache;t[0]!==e&&(n.uniform1ui(this.addr,e),t[0]=e)}function ip(n,e){const t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y)&&(n.uniform2ui(this.addr,e.x,e.y),t[0]=e.x,t[1]=e.y);else{if(_t(t,e))return;n.uniform2uiv(this.addr,e),vt(t,e)}}function ap(n,e){const t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y||t[2]!==e.z)&&(n.uniform3ui(this.addr,e.x,e.y,e.z),t[0]=e.x,t[1]=e.y,t[2]=e.z);else{if(_t(t,e))return;n.uniform3uiv(this.addr,e),vt(t,e)}}function rp(n,e){const t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y||t[2]!==e.z||t[3]!==e.w)&&(n.uniform4ui(this.addr,e.x,e.y,e.z,e.w),t[0]=e.x,t[1]=e.y,t[2]=e.z,t[3]=e.w);else{if(_t(t,e))return;n.uniform4uiv(this.addr,e),vt(t,e)}}function sp(n,e,t){const i=this.cache,a=t.allocateTextureUnit();i[0]!==a&&(n.uniform1i(this.addr,a),i[0]=a);let r;this.type===n.SAMPLER_2D_SHADOW?(Wo.compareFunction=Fc,r=Wo):r=Zc,t.setTexture2D(e||r,a)}function op(n,e,t){const i=this.cache,a=t.allocateTextureUnit();i[0]!==a&&(n.uniform1i(this.addr,a),i[0]=a),t.setTexture3D(e||Qc,a)}function cp(n,e,t){const i=this.cache,a=t.allocateTextureUnit();i[0]!==a&&(n.uniform1i(this.addr,a),i[0]=a),t.setTextureCube(e||el,a)}function lp(n,e,t){const i=this.cache,a=t.allocateTextureUnit();i[0]!==a&&(n.uniform1i(this.addr,a),i[0]=a),t.setTexture2DArray(e||Jc,a)}function up(n){switch(n){case 5126:return Wf;case 35664:return Xf;case 35665:return Kf;case 35666:return qf;case 35674:return $f;case 35675:return Yf;case 35676:return Zf;case 5124:case 35670:return Jf;case 35667:case 35671:return Qf;case 35668:case 35672:return ep;case 35669:case 35673:return tp;case 5125:return np;case 36294:return ip;case 36295:return ap;case 36296:return rp;case 35678:case 36198:case 36298:case 36306:case 35682:return sp;case 35679:case 36299:case 36307:return op;case 35680:case 36300:case 36308:case 36293:return cp;case 36289:case 36303:case 36311:case 36292:return lp}}function dp(n,e){n.uniform1fv(this.addr,e)}function hp(n,e){const t=ki(e,this.size,2);n.uniform2fv(this.addr,t)}function fp(n,e){const t=ki(e,this.size,3);n.uniform3fv(this.addr,t)}function pp(n,e){const t=ki(e,this.size,4);n.uniform4fv(this.addr,t)}function mp(n,e){const t=ki(e,this.size,4);n.uniformMatrix2fv(this.addr,!1,t)}function gp(n,e){const t=ki(e,this.size,9);n.uniformMatrix3fv(this.addr,!1,t)}function _p(n,e){const t=ki(e,this.size,16);n.uniformMatrix4fv(this.addr,!1,t)}function vp(n,e){n.uniform1iv(this.addr,e)}function xp(n,e){n.uniform2iv(this.addr,e)}function Mp(n,e){n.uniform3iv(this.addr,e)}function Sp(n,e){n.uniform4iv(this.addr,e)}function Ep(n,e){n.uniform1uiv(this.addr,e)}function bp(n,e){n.uniform2uiv(this.addr,e)}function yp(n,e){n.uniform3uiv(this.addr,e)}function Tp(n,e){n.uniform4uiv(this.addr,e)}function Ap(n,e,t){const i=this.cache,a=e.length,r=Xa(t,a);_t(i,r)||(n.uniform1iv(this.addr,r),vt(i,r));for(let s=0;s!==a;++s)t.setTexture2D(e[s]||Zc,r[s])}function wp(n,e,t){const i=this.cache,a=e.length,r=Xa(t,a);_t(i,r)||(n.uniform1iv(this.addr,r),vt(i,r));for(let s=0;s!==a;++s)t.setTexture3D(e[s]||Qc,r[s])}function Rp(n,e,t){const i=this.cache,a=e.length,r=Xa(t,a);_t(i,r)||(n.uniform1iv(this.addr,r),vt(i,r));for(let s=0;s!==a;++s)t.setTextureCube(e[s]||el,r[s])}function Cp(n,e,t){const i=this.cache,a=e.length,r=Xa(t,a);_t(i,r)||(n.uniform1iv(this.addr,r),vt(i,r));for(let s=0;s!==a;++s)t.setTexture2DArray(e[s]||Jc,r[s])}function Pp(n){switch(n){case 5126:return dp;case 35664:return hp;case 35665:return fp;case 35666:return pp;case 35674:return mp;case 35675:return gp;case 35676:return _p;case 5124:case 35670:return vp;case 35667:case 35671:return xp;case 35668:case 35672:return Mp;case 35669:case 35673:return Sp;case 5125:return Ep;case 36294:return bp;case 36295:return yp;case 36296:return Tp;case 35678:case 36198:case 36298:case 36306:case 35682:return Ap;case 35679:case 36299:case 36307:return wp;case 35680:case 36300:case 36308:case 36293:return Rp;case 36289:case 36303:case 36311:case 36292:return Cp}}class Ip{constructor(e,t,i){this.id=e,this.addr=i,this.cache=[],this.type=t.type,this.setValue=up(t.type)}}class Dp{constructor(e,t,i){this.id=e,this.addr=i,this.cache=[],this.type=t.type,this.size=t.size,this.setValue=Pp(t.type)}}class Lp{constructor(e){this.id=e,this.seq=[],this.map={}}setValue(e,t,i){const a=this.seq;for(let r=0,s=a.length;r!==s;++r){const o=a[r];o.setValue(e,t[o.id],i)}}}const Rr=/(\w+)(\])?(\[|\.)?/g;function Zo(n,e){n.seq.push(e),n.map[e.id]=e}function Up(n,e,t){const i=n.name,a=i.length;for(Rr.lastIndex=0;;){const r=Rr.exec(i),s=Rr.lastIndex;let o=r[1];const c=r[2]==="]",l=r[3];if(c&&(o=o|0),l===void 0||l==="["&&s+2===a){Zo(t,l===void 0?new Ip(o,n,e):new Dp(o,n,e));break}else{let h=t.map[o];h===void 0&&(h=new Lp(o),Zo(t,h)),t=h}}}class ka{constructor(e,t){this.seq=[],this.map={};const i=e.getProgramParameter(t,e.ACTIVE_UNIFORMS);for(let a=0;a<i;++a){const r=e.getActiveUniform(t,a),s=e.getUniformLocation(t,r.name);Up(r,s,this)}}setValue(e,t,i,a){const r=this.map[t];r!==void 0&&r.setValue(e,i,a)}setOptional(e,t,i){const a=t[i];a!==void 0&&this.setValue(e,i,a)}static upload(e,t,i,a){for(let r=0,s=t.length;r!==s;++r){const o=t[r],c=i[o.id];c.needsUpdate!==!1&&o.setValue(e,c.value,a)}}static seqWithValue(e,t){const i=[];for(let a=0,r=e.length;a!==r;++a){const s=e[a];s.id in t&&i.push(s)}return i}}function Jo(n,e,t){const i=n.createShader(e);return n.shaderSource(i,t),n.compileShader(i),i}const zp=37297;let kp=0;function Np(n,e){const t=n.split(`
`),i=[],a=Math.max(e-6,0),r=Math.min(e+6,t.length);for(let s=a;s<r;s++){const o=s+1;i.push(`${o===e?">":" "} ${o}: ${t[s]}`)}return i.join(`
`)}const Qo=new Be;function Fp(n){Qe._getMatrix(Qo,Qe.workingColorSpace,n);const e=`mat3( ${Qo.elements.map(t=>t.toFixed(4))} )`;switch(Qe.getTransfer(n)){case Fa:return[e,"LinearTransferOETF"];case at:return[e,"sRGBTransferOETF"];default:return console.warn("THREE.WebGLProgram: Unsupported color space: ",n),[e,"LinearTransferOETF"]}}function ec(n,e,t){const i=n.getShaderParameter(e,n.COMPILE_STATUS),a=n.getShaderInfoLog(e).trim();if(i&&a==="")return"";const r=/ERROR: 0:(\d+)/.exec(a);if(r){const s=parseInt(r[1]);return t.toUpperCase()+`

`+a+`

`+Np(n.getShaderSource(e),s)}else return a}function Op(n,e){const t=Fp(e);return[`vec4 ${n}( vec4 value ) {`,`	return ${t[1]}( vec4( value.rgb * ${t[0]}, value.a ) );`,"}"].join(`
`)}function Bp(n,e){let t;switch(e){case Hl:t="Linear";break;case Gl:t="Reinhard";break;case Wl:t="Cineon";break;case Xl:t="ACESFilmic";break;case ql:t="AgX";break;case $l:t="Neutral";break;case Kl:t="Custom";break;default:console.warn("THREE.WebGLProgram: Unsupported toneMapping:",e),t="Linear"}return"vec3 "+n+"( vec3 color ) { return "+t+"ToneMapping( color ); }"}const Ra=new F;function Vp(){Qe.getLuminanceCoefficients(Ra);const n=Ra.x.toFixed(4),e=Ra.y.toFixed(4),t=Ra.z.toFixed(4);return["float luminance( const in vec3 rgb ) {",`	const vec3 weights = vec3( ${n}, ${e}, ${t} );`,"	return dot( weights, rgb );","}"].join(`
`)}function jp(n){return[n.extensionClipCullDistance?"#extension GL_ANGLE_clip_cull_distance : require":"",n.extensionMultiDraw?"#extension GL_ANGLE_multi_draw : require":""].filter(Wi).join(`
`)}function Hp(n){const e=[];for(const t in n){const i=n[t];i!==!1&&e.push("#define "+t+" "+i)}return e.join(`
`)}function Gp(n,e){const t={},i=n.getProgramParameter(e,n.ACTIVE_ATTRIBUTES);for(let a=0;a<i;a++){const r=n.getActiveAttrib(e,a),s=r.name;let o=1;r.type===n.FLOAT_MAT2&&(o=2),r.type===n.FLOAT_MAT3&&(o=3),r.type===n.FLOAT_MAT4&&(o=4),t[s]={type:r.type,location:n.getAttribLocation(e,s),locationSize:o}}return t}function Wi(n){return n!==""}function tc(n,e){const t=e.numSpotLightShadows+e.numSpotLightMaps-e.numSpotLightShadowsWithMaps;return n.replace(/NUM_DIR_LIGHTS/g,e.numDirLights).replace(/NUM_SPOT_LIGHTS/g,e.numSpotLights).replace(/NUM_SPOT_LIGHT_MAPS/g,e.numSpotLightMaps).replace(/NUM_SPOT_LIGHT_COORDS/g,t).replace(/NUM_RECT_AREA_LIGHTS/g,e.numRectAreaLights).replace(/NUM_POINT_LIGHTS/g,e.numPointLights).replace(/NUM_HEMI_LIGHTS/g,e.numHemiLights).replace(/NUM_DIR_LIGHT_SHADOWS/g,e.numDirLightShadows).replace(/NUM_SPOT_LIGHT_SHADOWS_WITH_MAPS/g,e.numSpotLightShadowsWithMaps).replace(/NUM_SPOT_LIGHT_SHADOWS/g,e.numSpotLightShadows).replace(/NUM_POINT_LIGHT_SHADOWS/g,e.numPointLightShadows)}function nc(n,e){return n.replace(/NUM_CLIPPING_PLANES/g,e.numClippingPlanes).replace(/UNION_CLIPPING_PLANES/g,e.numClippingPlanes-e.numClipIntersection)}const Wp=/^[ \t]*#include +<([\w\d./]+)>/gm;function Es(n){return n.replace(Wp,Kp)}const Xp=new Map;function Kp(n,e){let t=je[e];if(t===void 0){const i=Xp.get(e);if(i!==void 0)t=je[i],console.warn('THREE.WebGLRenderer: Shader chunk "%s" has been deprecated. Use "%s" instead.',e,i);else throw new Error("Can not resolve #include <"+e+">")}return Es(t)}const qp=/#pragma unroll_loop_start\s+for\s*\(\s*int\s+i\s*=\s*(\d+)\s*;\s*i\s*<\s*(\d+)\s*;\s*i\s*\+\+\s*\)\s*{([\s\S]+?)}\s+#pragma unroll_loop_end/g;function ic(n){return n.replace(qp,$p)}function $p(n,e,t,i){let a="";for(let r=parseInt(e);r<parseInt(t);r++)a+=i.replace(/\[\s*i\s*\]/g,"[ "+r+" ]").replace(/UNROLLED_LOOP_INDEX/g,r);return a}function ac(n){let e=`precision ${n.precision} float;
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
#define LOW_PRECISION`),e}function Yp(n){let e="SHADOWMAP_TYPE_BASIC";return n.shadowMapType===yc?e="SHADOWMAP_TYPE_PCF":n.shadowMapType===El?e="SHADOWMAP_TYPE_PCF_SOFT":n.shadowMapType===dn&&(e="SHADOWMAP_TYPE_VSM"),e}function Zp(n){let e="ENVMAP_TYPE_CUBE";if(n.envMap)switch(n.envMapMode){case Ai:case wi:e="ENVMAP_TYPE_CUBE";break;case Ga:e="ENVMAP_TYPE_CUBE_UV";break}return e}function Jp(n){let e="ENVMAP_MODE_REFLECTION";if(n.envMap)switch(n.envMapMode){case wi:e="ENVMAP_MODE_REFRACTION";break}return e}function Qp(n){let e="ENVMAP_BLENDING_NONE";if(n.envMap)switch(n.combine){case Tc:e="ENVMAP_BLENDING_MULTIPLY";break;case Vl:e="ENVMAP_BLENDING_MIX";break;case jl:e="ENVMAP_BLENDING_ADD";break}return e}function em(n){const e=n.envMapCubeUVHeight;if(e===null)return null;const t=Math.log2(e)-2,i=1/e;return{texelWidth:1/(3*Math.max(Math.pow(2,t),112)),texelHeight:i,maxMip:t}}function tm(n,e,t,i){const a=n.getContext(),r=t.defines;let s=t.vertexShader,o=t.fragmentShader;const c=Yp(t),l=Zp(t),u=Jp(t),h=Qp(t),f=em(t),m=jp(t),g=Hp(r),_=a.createProgram();let p,d,E=t.glslVersion?"#version "+t.glslVersion+`
`:"";t.isRawShaderMaterial?(p=["#define SHADER_TYPE "+t.shaderType,"#define SHADER_NAME "+t.shaderName,g].filter(Wi).join(`
`),p.length>0&&(p+=`
`),d=["#define SHADER_TYPE "+t.shaderType,"#define SHADER_NAME "+t.shaderName,g].filter(Wi).join(`
`),d.length>0&&(d+=`
`)):(p=[ac(t),"#define SHADER_TYPE "+t.shaderType,"#define SHADER_NAME "+t.shaderName,g,t.extensionClipCullDistance?"#define USE_CLIP_DISTANCE":"",t.batching?"#define USE_BATCHING":"",t.batchingColor?"#define USE_BATCHING_COLOR":"",t.instancing?"#define USE_INSTANCING":"",t.instancingColor?"#define USE_INSTANCING_COLOR":"",t.instancingMorph?"#define USE_INSTANCING_MORPH":"",t.useFog&&t.fog?"#define USE_FOG":"",t.useFog&&t.fogExp2?"#define FOG_EXP2":"",t.map?"#define USE_MAP":"",t.envMap?"#define USE_ENVMAP":"",t.envMap?"#define "+u:"",t.lightMap?"#define USE_LIGHTMAP":"",t.aoMap?"#define USE_AOMAP":"",t.bumpMap?"#define USE_BUMPMAP":"",t.normalMap?"#define USE_NORMALMAP":"",t.normalMapObjectSpace?"#define USE_NORMALMAP_OBJECTSPACE":"",t.normalMapTangentSpace?"#define USE_NORMALMAP_TANGENTSPACE":"",t.displacementMap?"#define USE_DISPLACEMENTMAP":"",t.emissiveMap?"#define USE_EMISSIVEMAP":"",t.anisotropy?"#define USE_ANISOTROPY":"",t.anisotropyMap?"#define USE_ANISOTROPYMAP":"",t.clearcoatMap?"#define USE_CLEARCOATMAP":"",t.clearcoatRoughnessMap?"#define USE_CLEARCOAT_ROUGHNESSMAP":"",t.clearcoatNormalMap?"#define USE_CLEARCOAT_NORMALMAP":"",t.iridescenceMap?"#define USE_IRIDESCENCEMAP":"",t.iridescenceThicknessMap?"#define USE_IRIDESCENCE_THICKNESSMAP":"",t.specularMap?"#define USE_SPECULARMAP":"",t.specularColorMap?"#define USE_SPECULAR_COLORMAP":"",t.specularIntensityMap?"#define USE_SPECULAR_INTENSITYMAP":"",t.roughnessMap?"#define USE_ROUGHNESSMAP":"",t.metalnessMap?"#define USE_METALNESSMAP":"",t.alphaMap?"#define USE_ALPHAMAP":"",t.alphaHash?"#define USE_ALPHAHASH":"",t.transmission?"#define USE_TRANSMISSION":"",t.transmissionMap?"#define USE_TRANSMISSIONMAP":"",t.thicknessMap?"#define USE_THICKNESSMAP":"",t.sheenColorMap?"#define USE_SHEEN_COLORMAP":"",t.sheenRoughnessMap?"#define USE_SHEEN_ROUGHNESSMAP":"",t.mapUv?"#define MAP_UV "+t.mapUv:"",t.alphaMapUv?"#define ALPHAMAP_UV "+t.alphaMapUv:"",t.lightMapUv?"#define LIGHTMAP_UV "+t.lightMapUv:"",t.aoMapUv?"#define AOMAP_UV "+t.aoMapUv:"",t.emissiveMapUv?"#define EMISSIVEMAP_UV "+t.emissiveMapUv:"",t.bumpMapUv?"#define BUMPMAP_UV "+t.bumpMapUv:"",t.normalMapUv?"#define NORMALMAP_UV "+t.normalMapUv:"",t.displacementMapUv?"#define DISPLACEMENTMAP_UV "+t.displacementMapUv:"",t.metalnessMapUv?"#define METALNESSMAP_UV "+t.metalnessMapUv:"",t.roughnessMapUv?"#define ROUGHNESSMAP_UV "+t.roughnessMapUv:"",t.anisotropyMapUv?"#define ANISOTROPYMAP_UV "+t.anisotropyMapUv:"",t.clearcoatMapUv?"#define CLEARCOATMAP_UV "+t.clearcoatMapUv:"",t.clearcoatNormalMapUv?"#define CLEARCOAT_NORMALMAP_UV "+t.clearcoatNormalMapUv:"",t.clearcoatRoughnessMapUv?"#define CLEARCOAT_ROUGHNESSMAP_UV "+t.clearcoatRoughnessMapUv:"",t.iridescenceMapUv?"#define IRIDESCENCEMAP_UV "+t.iridescenceMapUv:"",t.iridescenceThicknessMapUv?"#define IRIDESCENCE_THICKNESSMAP_UV "+t.iridescenceThicknessMapUv:"",t.sheenColorMapUv?"#define SHEEN_COLORMAP_UV "+t.sheenColorMapUv:"",t.sheenRoughnessMapUv?"#define SHEEN_ROUGHNESSMAP_UV "+t.sheenRoughnessMapUv:"",t.specularMapUv?"#define SPECULARMAP_UV "+t.specularMapUv:"",t.specularColorMapUv?"#define SPECULAR_COLORMAP_UV "+t.specularColorMapUv:"",t.specularIntensityMapUv?"#define SPECULAR_INTENSITYMAP_UV "+t.specularIntensityMapUv:"",t.transmissionMapUv?"#define TRANSMISSIONMAP_UV "+t.transmissionMapUv:"",t.thicknessMapUv?"#define THICKNESSMAP_UV "+t.thicknessMapUv:"",t.vertexTangents&&t.flatShading===!1?"#define USE_TANGENT":"",t.vertexColors?"#define USE_COLOR":"",t.vertexAlphas?"#define USE_COLOR_ALPHA":"",t.vertexUv1s?"#define USE_UV1":"",t.vertexUv2s?"#define USE_UV2":"",t.vertexUv3s?"#define USE_UV3":"",t.pointsUvs?"#define USE_POINTS_UV":"",t.flatShading?"#define FLAT_SHADED":"",t.skinning?"#define USE_SKINNING":"",t.morphTargets?"#define USE_MORPHTARGETS":"",t.morphNormals&&t.flatShading===!1?"#define USE_MORPHNORMALS":"",t.morphColors?"#define USE_MORPHCOLORS":"",t.morphTargetsCount>0?"#define MORPHTARGETS_TEXTURE_STRIDE "+t.morphTextureStride:"",t.morphTargetsCount>0?"#define MORPHTARGETS_COUNT "+t.morphTargetsCount:"",t.doubleSided?"#define DOUBLE_SIDED":"",t.flipSided?"#define FLIP_SIDED":"",t.shadowMapEnabled?"#define USE_SHADOWMAP":"",t.shadowMapEnabled?"#define "+c:"",t.sizeAttenuation?"#define USE_SIZEATTENUATION":"",t.numLightProbes>0?"#define USE_LIGHT_PROBES":"",t.logarithmicDepthBuffer?"#define USE_LOGDEPTHBUF":"",t.reverseDepthBuffer?"#define USE_REVERSEDEPTHBUF":"","uniform mat4 modelMatrix;","uniform mat4 modelViewMatrix;","uniform mat4 projectionMatrix;","uniform mat4 viewMatrix;","uniform mat3 normalMatrix;","uniform vec3 cameraPosition;","uniform bool isOrthographic;","#ifdef USE_INSTANCING","	attribute mat4 instanceMatrix;","#endif","#ifdef USE_INSTANCING_COLOR","	attribute vec3 instanceColor;","#endif","#ifdef USE_INSTANCING_MORPH","	uniform sampler2D morphTexture;","#endif","attribute vec3 position;","attribute vec3 normal;","attribute vec2 uv;","#ifdef USE_UV1","	attribute vec2 uv1;","#endif","#ifdef USE_UV2","	attribute vec2 uv2;","#endif","#ifdef USE_UV3","	attribute vec2 uv3;","#endif","#ifdef USE_TANGENT","	attribute vec4 tangent;","#endif","#if defined( USE_COLOR_ALPHA )","	attribute vec4 color;","#elif defined( USE_COLOR )","	attribute vec3 color;","#endif","#ifdef USE_SKINNING","	attribute vec4 skinIndex;","	attribute vec4 skinWeight;","#endif",`
`].filter(Wi).join(`
`),d=[ac(t),"#define SHADER_TYPE "+t.shaderType,"#define SHADER_NAME "+t.shaderName,g,t.useFog&&t.fog?"#define USE_FOG":"",t.useFog&&t.fogExp2?"#define FOG_EXP2":"",t.alphaToCoverage?"#define ALPHA_TO_COVERAGE":"",t.map?"#define USE_MAP":"",t.matcap?"#define USE_MATCAP":"",t.envMap?"#define USE_ENVMAP":"",t.envMap?"#define "+l:"",t.envMap?"#define "+u:"",t.envMap?"#define "+h:"",f?"#define CUBEUV_TEXEL_WIDTH "+f.texelWidth:"",f?"#define CUBEUV_TEXEL_HEIGHT "+f.texelHeight:"",f?"#define CUBEUV_MAX_MIP "+f.maxMip+".0":"",t.lightMap?"#define USE_LIGHTMAP":"",t.aoMap?"#define USE_AOMAP":"",t.bumpMap?"#define USE_BUMPMAP":"",t.normalMap?"#define USE_NORMALMAP":"",t.normalMapObjectSpace?"#define USE_NORMALMAP_OBJECTSPACE":"",t.normalMapTangentSpace?"#define USE_NORMALMAP_TANGENTSPACE":"",t.emissiveMap?"#define USE_EMISSIVEMAP":"",t.anisotropy?"#define USE_ANISOTROPY":"",t.anisotropyMap?"#define USE_ANISOTROPYMAP":"",t.clearcoat?"#define USE_CLEARCOAT":"",t.clearcoatMap?"#define USE_CLEARCOATMAP":"",t.clearcoatRoughnessMap?"#define USE_CLEARCOAT_ROUGHNESSMAP":"",t.clearcoatNormalMap?"#define USE_CLEARCOAT_NORMALMAP":"",t.dispersion?"#define USE_DISPERSION":"",t.iridescence?"#define USE_IRIDESCENCE":"",t.iridescenceMap?"#define USE_IRIDESCENCEMAP":"",t.iridescenceThicknessMap?"#define USE_IRIDESCENCE_THICKNESSMAP":"",t.specularMap?"#define USE_SPECULARMAP":"",t.specularColorMap?"#define USE_SPECULAR_COLORMAP":"",t.specularIntensityMap?"#define USE_SPECULAR_INTENSITYMAP":"",t.roughnessMap?"#define USE_ROUGHNESSMAP":"",t.metalnessMap?"#define USE_METALNESSMAP":"",t.alphaMap?"#define USE_ALPHAMAP":"",t.alphaTest?"#define USE_ALPHATEST":"",t.alphaHash?"#define USE_ALPHAHASH":"",t.sheen?"#define USE_SHEEN":"",t.sheenColorMap?"#define USE_SHEEN_COLORMAP":"",t.sheenRoughnessMap?"#define USE_SHEEN_ROUGHNESSMAP":"",t.transmission?"#define USE_TRANSMISSION":"",t.transmissionMap?"#define USE_TRANSMISSIONMAP":"",t.thicknessMap?"#define USE_THICKNESSMAP":"",t.vertexTangents&&t.flatShading===!1?"#define USE_TANGENT":"",t.vertexColors||t.instancingColor||t.batchingColor?"#define USE_COLOR":"",t.vertexAlphas?"#define USE_COLOR_ALPHA":"",t.vertexUv1s?"#define USE_UV1":"",t.vertexUv2s?"#define USE_UV2":"",t.vertexUv3s?"#define USE_UV3":"",t.pointsUvs?"#define USE_POINTS_UV":"",t.gradientMap?"#define USE_GRADIENTMAP":"",t.flatShading?"#define FLAT_SHADED":"",t.doubleSided?"#define DOUBLE_SIDED":"",t.flipSided?"#define FLIP_SIDED":"",t.shadowMapEnabled?"#define USE_SHADOWMAP":"",t.shadowMapEnabled?"#define "+c:"",t.premultipliedAlpha?"#define PREMULTIPLIED_ALPHA":"",t.numLightProbes>0?"#define USE_LIGHT_PROBES":"",t.decodeVideoTexture?"#define DECODE_VIDEO_TEXTURE":"",t.decodeVideoTextureEmissive?"#define DECODE_VIDEO_TEXTURE_EMISSIVE":"",t.logarithmicDepthBuffer?"#define USE_LOGDEPTHBUF":"",t.reverseDepthBuffer?"#define USE_REVERSEDEPTHBUF":"","uniform mat4 viewMatrix;","uniform vec3 cameraPosition;","uniform bool isOrthographic;",t.toneMapping!==Dn?"#define TONE_MAPPING":"",t.toneMapping!==Dn?je.tonemapping_pars_fragment:"",t.toneMapping!==Dn?Bp("toneMapping",t.toneMapping):"",t.dithering?"#define DITHERING":"",t.opaque?"#define OPAQUE":"",je.colorspace_pars_fragment,Op("linearToOutputTexel",t.outputColorSpace),Vp(),t.useDepthPacking?"#define DEPTH_PACKING "+t.depthPacking:"",`
`].filter(Wi).join(`
`)),s=Es(s),s=tc(s,t),s=nc(s,t),o=Es(o),o=tc(o,t),o=nc(o,t),s=ic(s),o=ic(o),t.isRawShaderMaterial!==!0&&(E=`#version 300 es
`,p=[m,"#define attribute in","#define varying out","#define texture2D texture"].join(`
`)+`
`+p,d=["#define varying in",t.glslVersion===lo?"":"layout(location = 0) out highp vec4 pc_fragColor;",t.glslVersion===lo?"":"#define gl_FragColor pc_fragColor","#define gl_FragDepthEXT gl_FragDepth","#define texture2D texture","#define textureCube texture","#define texture2DProj textureProj","#define texture2DLodEXT textureLod","#define texture2DProjLodEXT textureProjLod","#define textureCubeLodEXT textureLod","#define texture2DGradEXT textureGrad","#define texture2DProjGradEXT textureProjGrad","#define textureCubeGradEXT textureGrad"].join(`
`)+`
`+d);const S=E+p+s,x=E+d+o,T=Jo(a,a.VERTEX_SHADER,S),y=Jo(a,a.FRAGMENT_SHADER,x);a.attachShader(_,T),a.attachShader(_,y),t.index0AttributeName!==void 0?a.bindAttribLocation(_,0,t.index0AttributeName):t.morphTargets===!0&&a.bindAttribLocation(_,0,"position"),a.linkProgram(_);function w(R){if(n.debug.checkShaderErrors){const U=a.getProgramInfoLog(_).trim(),C=a.getShaderInfoLog(T).trim(),P=a.getShaderInfoLog(y).trim();let N=!0,k=!0;if(a.getProgramParameter(_,a.LINK_STATUS)===!1)if(N=!1,typeof n.debug.onShaderError=="function")n.debug.onShaderError(a,_,T,y);else{const O=ec(a,T,"vertex"),z=ec(a,y,"fragment");console.error("THREE.WebGLProgram: Shader Error "+a.getError()+" - VALIDATE_STATUS "+a.getProgramParameter(_,a.VALIDATE_STATUS)+`

Material Name: `+R.name+`
Material Type: `+R.type+`

Program Info Log: `+U+`
`+O+`
`+z)}else U!==""?console.warn("THREE.WebGLProgram: Program Info Log:",U):(C===""||P==="")&&(k=!1);k&&(R.diagnostics={runnable:N,programLog:U,vertexShader:{log:C,prefix:p},fragmentShader:{log:P,prefix:d}})}a.deleteShader(T),a.deleteShader(y),D=new ka(a,_),M=Gp(a,_)}let D;this.getUniforms=function(){return D===void 0&&w(this),D};let M;this.getAttributes=function(){return M===void 0&&w(this),M};let v=t.rendererExtensionParallelShaderCompile===!1;return this.isReady=function(){return v===!1&&(v=a.getProgramParameter(_,zp)),v},this.destroy=function(){i.releaseStatesOfProgram(this),a.deleteProgram(_),this.program=void 0},this.type=t.shaderType,this.name=t.shaderName,this.id=kp++,this.cacheKey=e,this.usedTimes=1,this.program=_,this.vertexShader=T,this.fragmentShader=y,this}let nm=0;class im{constructor(){this.shaderCache=new Map,this.materialCache=new Map}update(e){const t=e.vertexShader,i=e.fragmentShader,a=this._getShaderStage(t),r=this._getShaderStage(i),s=this._getShaderCacheForMaterial(e);return s.has(a)===!1&&(s.add(a),a.usedTimes++),s.has(r)===!1&&(s.add(r),r.usedTimes++),this}remove(e){const t=this.materialCache.get(e);for(const i of t)i.usedTimes--,i.usedTimes===0&&this.shaderCache.delete(i.code);return this.materialCache.delete(e),this}getVertexShaderID(e){return this._getShaderStage(e.vertexShader).id}getFragmentShaderID(e){return this._getShaderStage(e.fragmentShader).id}dispose(){this.shaderCache.clear(),this.materialCache.clear()}_getShaderCacheForMaterial(e){const t=this.materialCache;let i=t.get(e);return i===void 0&&(i=new Set,t.set(e,i)),i}_getShaderStage(e){const t=this.shaderCache;let i=t.get(e);return i===void 0&&(i=new am(e),t.set(e,i)),i}}class am{constructor(e){this.id=nm++,this.code=e,this.usedTimes=0}}function rm(n,e,t,i,a,r,s){const o=new Os,c=new im,l=new Set,u=[],h=a.logarithmicDepthBuffer,f=a.vertexTextures;let m=a.precision;const g={MeshDepthMaterial:"depth",MeshDistanceMaterial:"distanceRGBA",MeshNormalMaterial:"normal",MeshBasicMaterial:"basic",MeshLambertMaterial:"lambert",MeshPhongMaterial:"phong",MeshToonMaterial:"toon",MeshStandardMaterial:"physical",MeshPhysicalMaterial:"physical",MeshMatcapMaterial:"matcap",LineBasicMaterial:"basic",LineDashedMaterial:"dashed",PointsMaterial:"points",ShadowMaterial:"shadow",SpriteMaterial:"sprite"};function _(M){return l.add(M),M===0?"uv":`uv${M}`}function p(M,v,R,U,C){const P=U.fog,N=C.geometry,k=M.isMeshStandardMaterial?U.environment:null,O=(M.isMeshStandardMaterial?t:e).get(M.envMap||k),z=O&&O.mapping===Ga?O.image.height:null,H=g[M.type];M.precision!==null&&(m=a.getMaxPrecision(M.precision),m!==M.precision&&console.warn("THREE.WebGLProgram.getParameters:",M.precision,"not supported, using",m,"instead."));const $=N.morphAttributes.position||N.morphAttributes.normal||N.morphAttributes.color,Y=$!==void 0?$.length:0;let fe=0;N.morphAttributes.position!==void 0&&(fe=1),N.morphAttributes.normal!==void 0&&(fe=2),N.morphAttributes.color!==void 0&&(fe=3);let Ie,X,ne,ue;if(H){const nt=Qt[H];Ie=nt.vertexShader,X=nt.fragmentShader}else Ie=M.vertexShader,X=M.fragmentShader,c.update(M),ne=c.getVertexShaderID(M),ue=c.getFragmentShaderID(M);const se=n.getRenderTarget(),ee=n.state.buffers.depth.getReversed(),_e=C.isInstancedMesh===!0,de=C.isBatchedMesh===!0,Z=!!M.map,ae=!!M.matcap,re=!!O,L=!!M.aoMap,Le=!!M.lightMap,Ce=!!M.bumpMap,Re=!!M.normalMap,Me=!!M.displacementMap,Fe=!!M.emissiveMap,we=!!M.metalnessMap,I=!!M.roughnessMap,b=M.anisotropy>0,G=M.clearcoat>0,Q=M.dispersion>0,ie=M.iridescence>0,J=M.sheen>0,Ae=M.transmission>0,ge=b&&!!M.anisotropyMap,Ee=G&&!!M.clearcoatMap,Ye=G&&!!M.clearcoatNormalMap,le=G&&!!M.clearcoatRoughnessMap,be=ie&&!!M.iridescenceMap,Ue=ie&&!!M.iridescenceThicknessMap,ze=J&&!!M.sheenColorMap,ye=J&&!!M.sheenRoughnessMap,qe=!!M.specularMap,Ve=!!M.specularColorMap,rt=!!M.specularIntensityMap,B=Ae&&!!M.transmissionMap,pe=Ae&&!!M.thicknessMap,q=!!M.gradientMap,te=!!M.alphaMap,xe=M.alphaTest>0,ve=!!M.alphaHash,Oe=!!M.extensions;let lt=Dn;M.toneMapped&&(se===null||se.isXRRenderTarget===!0)&&(lt=n.toneMapping);const bt={shaderID:H,shaderType:M.type,shaderName:M.name,vertexShader:Ie,fragmentShader:X,defines:M.defines,customVertexShaderID:ne,customFragmentShaderID:ue,isRawShaderMaterial:M.isRawShaderMaterial===!0,glslVersion:M.glslVersion,precision:m,batching:de,batchingColor:de&&C._colorsTexture!==null,instancing:_e,instancingColor:_e&&C.instanceColor!==null,instancingMorph:_e&&C.morphTexture!==null,supportsVertexTextures:f,outputColorSpace:se===null?n.outputColorSpace:se.isXRRenderTarget===!0?se.texture.colorSpace:Pi,alphaToCoverage:!!M.alphaToCoverage,map:Z,matcap:ae,envMap:re,envMapMode:re&&O.mapping,envMapCubeUVHeight:z,aoMap:L,lightMap:Le,bumpMap:Ce,normalMap:Re,displacementMap:f&&Me,emissiveMap:Fe,normalMapObjectSpace:Re&&M.normalMapType===Ql,normalMapTangentSpace:Re&&M.normalMapType===Nc,metalnessMap:we,roughnessMap:I,anisotropy:b,anisotropyMap:ge,clearcoat:G,clearcoatMap:Ee,clearcoatNormalMap:Ye,clearcoatRoughnessMap:le,dispersion:Q,iridescence:ie,iridescenceMap:be,iridescenceThicknessMap:Ue,sheen:J,sheenColorMap:ze,sheenRoughnessMap:ye,specularMap:qe,specularColorMap:Ve,specularIntensityMap:rt,transmission:Ae,transmissionMap:B,thicknessMap:pe,gradientMap:q,opaque:M.transparent===!1&&M.blending===Ei&&M.alphaToCoverage===!1,alphaMap:te,alphaTest:xe,alphaHash:ve,combine:M.combine,mapUv:Z&&_(M.map.channel),aoMapUv:L&&_(M.aoMap.channel),lightMapUv:Le&&_(M.lightMap.channel),bumpMapUv:Ce&&_(M.bumpMap.channel),normalMapUv:Re&&_(M.normalMap.channel),displacementMapUv:Me&&_(M.displacementMap.channel),emissiveMapUv:Fe&&_(M.emissiveMap.channel),metalnessMapUv:we&&_(M.metalnessMap.channel),roughnessMapUv:I&&_(M.roughnessMap.channel),anisotropyMapUv:ge&&_(M.anisotropyMap.channel),clearcoatMapUv:Ee&&_(M.clearcoatMap.channel),clearcoatNormalMapUv:Ye&&_(M.clearcoatNormalMap.channel),clearcoatRoughnessMapUv:le&&_(M.clearcoatRoughnessMap.channel),iridescenceMapUv:be&&_(M.iridescenceMap.channel),iridescenceThicknessMapUv:Ue&&_(M.iridescenceThicknessMap.channel),sheenColorMapUv:ze&&_(M.sheenColorMap.channel),sheenRoughnessMapUv:ye&&_(M.sheenRoughnessMap.channel),specularMapUv:qe&&_(M.specularMap.channel),specularColorMapUv:Ve&&_(M.specularColorMap.channel),specularIntensityMapUv:rt&&_(M.specularIntensityMap.channel),transmissionMapUv:B&&_(M.transmissionMap.channel),thicknessMapUv:pe&&_(M.thicknessMap.channel),alphaMapUv:te&&_(M.alphaMap.channel),vertexTangents:!!N.attributes.tangent&&(Re||b),vertexColors:M.vertexColors,vertexAlphas:M.vertexColors===!0&&!!N.attributes.color&&N.attributes.color.itemSize===4,pointsUvs:C.isPoints===!0&&!!N.attributes.uv&&(Z||te),fog:!!P,useFog:M.fog===!0,fogExp2:!!P&&P.isFogExp2,flatShading:M.flatShading===!0,sizeAttenuation:M.sizeAttenuation===!0,logarithmicDepthBuffer:h,reverseDepthBuffer:ee,skinning:C.isSkinnedMesh===!0,morphTargets:N.morphAttributes.position!==void 0,morphNormals:N.morphAttributes.normal!==void 0,morphColors:N.morphAttributes.color!==void 0,morphTargetsCount:Y,morphTextureStride:fe,numDirLights:v.directional.length,numPointLights:v.point.length,numSpotLights:v.spot.length,numSpotLightMaps:v.spotLightMap.length,numRectAreaLights:v.rectArea.length,numHemiLights:v.hemi.length,numDirLightShadows:v.directionalShadowMap.length,numPointLightShadows:v.pointShadowMap.length,numSpotLightShadows:v.spotShadowMap.length,numSpotLightShadowsWithMaps:v.numSpotLightShadowsWithMaps,numLightProbes:v.numLightProbes,numClippingPlanes:s.numPlanes,numClipIntersection:s.numIntersection,dithering:M.dithering,shadowMapEnabled:n.shadowMap.enabled&&R.length>0,shadowMapType:n.shadowMap.type,toneMapping:lt,decodeVideoTexture:Z&&M.map.isVideoTexture===!0&&Qe.getTransfer(M.map.colorSpace)===at,decodeVideoTextureEmissive:Fe&&M.emissiveMap.isVideoTexture===!0&&Qe.getTransfer(M.emissiveMap.colorSpace)===at,premultipliedAlpha:M.premultipliedAlpha,doubleSided:M.side===mt,flipSided:M.side===Lt,useDepthPacking:M.depthPacking>=0,depthPacking:M.depthPacking||0,index0AttributeName:M.index0AttributeName,extensionClipCullDistance:Oe&&M.extensions.clipCullDistance===!0&&i.has("WEBGL_clip_cull_distance"),extensionMultiDraw:(Oe&&M.extensions.multiDraw===!0||de)&&i.has("WEBGL_multi_draw"),rendererExtensionParallelShaderCompile:i.has("KHR_parallel_shader_compile"),customProgramCacheKey:M.customProgramCacheKey()};return bt.vertexUv1s=l.has(1),bt.vertexUv2s=l.has(2),bt.vertexUv3s=l.has(3),l.clear(),bt}function d(M){const v=[];if(M.shaderID?v.push(M.shaderID):(v.push(M.customVertexShaderID),v.push(M.customFragmentShaderID)),M.defines!==void 0)for(const R in M.defines)v.push(R),v.push(M.defines[R]);return M.isRawShaderMaterial===!1&&(E(v,M),S(v,M),v.push(n.outputColorSpace)),v.push(M.customProgramCacheKey),v.join()}function E(M,v){M.push(v.precision),M.push(v.outputColorSpace),M.push(v.envMapMode),M.push(v.envMapCubeUVHeight),M.push(v.mapUv),M.push(v.alphaMapUv),M.push(v.lightMapUv),M.push(v.aoMapUv),M.push(v.bumpMapUv),M.push(v.normalMapUv),M.push(v.displacementMapUv),M.push(v.emissiveMapUv),M.push(v.metalnessMapUv),M.push(v.roughnessMapUv),M.push(v.anisotropyMapUv),M.push(v.clearcoatMapUv),M.push(v.clearcoatNormalMapUv),M.push(v.clearcoatRoughnessMapUv),M.push(v.iridescenceMapUv),M.push(v.iridescenceThicknessMapUv),M.push(v.sheenColorMapUv),M.push(v.sheenRoughnessMapUv),M.push(v.specularMapUv),M.push(v.specularColorMapUv),M.push(v.specularIntensityMapUv),M.push(v.transmissionMapUv),M.push(v.thicknessMapUv),M.push(v.combine),M.push(v.fogExp2),M.push(v.sizeAttenuation),M.push(v.morphTargetsCount),M.push(v.morphAttributeCount),M.push(v.numDirLights),M.push(v.numPointLights),M.push(v.numSpotLights),M.push(v.numSpotLightMaps),M.push(v.numHemiLights),M.push(v.numRectAreaLights),M.push(v.numDirLightShadows),M.push(v.numPointLightShadows),M.push(v.numSpotLightShadows),M.push(v.numSpotLightShadowsWithMaps),M.push(v.numLightProbes),M.push(v.shadowMapType),M.push(v.toneMapping),M.push(v.numClippingPlanes),M.push(v.numClipIntersection),M.push(v.depthPacking)}function S(M,v){o.disableAll(),v.supportsVertexTextures&&o.enable(0),v.instancing&&o.enable(1),v.instancingColor&&o.enable(2),v.instancingMorph&&o.enable(3),v.matcap&&o.enable(4),v.envMap&&o.enable(5),v.normalMapObjectSpace&&o.enable(6),v.normalMapTangentSpace&&o.enable(7),v.clearcoat&&o.enable(8),v.iridescence&&o.enable(9),v.alphaTest&&o.enable(10),v.vertexColors&&o.enable(11),v.vertexAlphas&&o.enable(12),v.vertexUv1s&&o.enable(13),v.vertexUv2s&&o.enable(14),v.vertexUv3s&&o.enable(15),v.vertexTangents&&o.enable(16),v.anisotropy&&o.enable(17),v.alphaHash&&o.enable(18),v.batching&&o.enable(19),v.dispersion&&o.enable(20),v.batchingColor&&o.enable(21),M.push(o.mask),o.disableAll(),v.fog&&o.enable(0),v.useFog&&o.enable(1),v.flatShading&&o.enable(2),v.logarithmicDepthBuffer&&o.enable(3),v.reverseDepthBuffer&&o.enable(4),v.skinning&&o.enable(5),v.morphTargets&&o.enable(6),v.morphNormals&&o.enable(7),v.morphColors&&o.enable(8),v.premultipliedAlpha&&o.enable(9),v.shadowMapEnabled&&o.enable(10),v.doubleSided&&o.enable(11),v.flipSided&&o.enable(12),v.useDepthPacking&&o.enable(13),v.dithering&&o.enable(14),v.transmission&&o.enable(15),v.sheen&&o.enable(16),v.opaque&&o.enable(17),v.pointsUvs&&o.enable(18),v.decodeVideoTexture&&o.enable(19),v.decodeVideoTextureEmissive&&o.enable(20),v.alphaToCoverage&&o.enable(21),M.push(o.mask)}function x(M){const v=g[M.type];let R;if(v){const U=Qt[v];R=Pu.clone(U.uniforms)}else R=M.uniforms;return R}function T(M,v){let R;for(let U=0,C=u.length;U<C;U++){const P=u[U];if(P.cacheKey===v){R=P,++R.usedTimes;break}}return R===void 0&&(R=new tm(n,v,M,r),u.push(R)),R}function y(M){if(--M.usedTimes===0){const v=u.indexOf(M);u[v]=u[u.length-1],u.pop(),M.destroy()}}function w(M){c.remove(M)}function D(){c.dispose()}return{getParameters:p,getProgramCacheKey:d,getUniforms:x,acquireProgram:T,releaseProgram:y,releaseShaderCache:w,programs:u,dispose:D}}function sm(){let n=new WeakMap;function e(s){return n.has(s)}function t(s){let o=n.get(s);return o===void 0&&(o={},n.set(s,o)),o}function i(s){n.delete(s)}function a(s,o,c){n.get(s)[o]=c}function r(){n=new WeakMap}return{has:e,get:t,remove:i,update:a,dispose:r}}function om(n,e){return n.groupOrder!==e.groupOrder?n.groupOrder-e.groupOrder:n.renderOrder!==e.renderOrder?n.renderOrder-e.renderOrder:n.material.id!==e.material.id?n.material.id-e.material.id:n.z!==e.z?n.z-e.z:n.id-e.id}function rc(n,e){return n.groupOrder!==e.groupOrder?n.groupOrder-e.groupOrder:n.renderOrder!==e.renderOrder?n.renderOrder-e.renderOrder:n.z!==e.z?e.z-n.z:n.id-e.id}function sc(){const n=[];let e=0;const t=[],i=[],a=[];function r(){e=0,t.length=0,i.length=0,a.length=0}function s(h,f,m,g,_,p){let d=n[e];return d===void 0?(d={id:h.id,object:h,geometry:f,material:m,groupOrder:g,renderOrder:h.renderOrder,z:_,group:p},n[e]=d):(d.id=h.id,d.object=h,d.geometry=f,d.material=m,d.groupOrder=g,d.renderOrder=h.renderOrder,d.z=_,d.group=p),e++,d}function o(h,f,m,g,_,p){const d=s(h,f,m,g,_,p);m.transmission>0?i.push(d):m.transparent===!0?a.push(d):t.push(d)}function c(h,f,m,g,_,p){const d=s(h,f,m,g,_,p);m.transmission>0?i.unshift(d):m.transparent===!0?a.unshift(d):t.unshift(d)}function l(h,f){t.length>1&&t.sort(h||om),i.length>1&&i.sort(f||rc),a.length>1&&a.sort(f||rc)}function u(){for(let h=e,f=n.length;h<f;h++){const m=n[h];if(m.id===null)break;m.id=null,m.object=null,m.geometry=null,m.material=null,m.group=null}}return{opaque:t,transmissive:i,transparent:a,init:r,push:o,unshift:c,finish:u,sort:l}}function cm(){let n=new WeakMap;function e(i,a){const r=n.get(i);let s;return r===void 0?(s=new sc,n.set(i,[s])):a>=r.length?(s=new sc,r.push(s)):s=r[a],s}function t(){n=new WeakMap}return{get:e,dispose:t}}function lm(){const n={};return{get:function(e){if(n[e.id]!==void 0)return n[e.id];let t;switch(e.type){case"DirectionalLight":t={direction:new F,color:new ce};break;case"SpotLight":t={position:new F,direction:new F,color:new ce,distance:0,coneCos:0,penumbraCos:0,decay:0};break;case"PointLight":t={position:new F,color:new ce,distance:0,decay:0};break;case"HemisphereLight":t={direction:new F,skyColor:new ce,groundColor:new ce};break;case"RectAreaLight":t={color:new ce,position:new F,halfWidth:new F,halfHeight:new F};break}return n[e.id]=t,t}}}function um(){const n={};return{get:function(e){if(n[e.id]!==void 0)return n[e.id];let t;switch(e.type){case"DirectionalLight":t={shadowIntensity:1,shadowBias:0,shadowNormalBias:0,shadowRadius:1,shadowMapSize:new Ke};break;case"SpotLight":t={shadowIntensity:1,shadowBias:0,shadowNormalBias:0,shadowRadius:1,shadowMapSize:new Ke};break;case"PointLight":t={shadowIntensity:1,shadowBias:0,shadowNormalBias:0,shadowRadius:1,shadowMapSize:new Ke,shadowCameraNear:1,shadowCameraFar:1e3};break}return n[e.id]=t,t}}}let dm=0;function hm(n,e){return(e.castShadow?2:0)-(n.castShadow?2:0)+(e.map?1:0)-(n.map?1:0)}function fm(n){const e=new lm,t=um(),i={version:0,hash:{directionalLength:-1,pointLength:-1,spotLength:-1,rectAreaLength:-1,hemiLength:-1,numDirectionalShadows:-1,numPointShadows:-1,numSpotShadows:-1,numSpotMaps:-1,numLightProbes:-1},ambient:[0,0,0],probe:[],directional:[],directionalShadow:[],directionalShadowMap:[],directionalShadowMatrix:[],spot:[],spotLightMap:[],spotShadow:[],spotShadowMap:[],spotLightMatrix:[],rectArea:[],rectAreaLTC1:null,rectAreaLTC2:null,point:[],pointShadow:[],pointShadowMap:[],pointShadowMatrix:[],hemi:[],numSpotLightShadowsWithMaps:0,numLightProbes:0};for(let l=0;l<9;l++)i.probe.push(new F);const a=new F,r=new st,s=new st;function o(l){let u=0,h=0,f=0;for(let M=0;M<9;M++)i.probe[M].set(0,0,0);let m=0,g=0,_=0,p=0,d=0,E=0,S=0,x=0,T=0,y=0,w=0;l.sort(hm);for(let M=0,v=l.length;M<v;M++){const R=l[M],U=R.color,C=R.intensity,P=R.distance,N=R.shadow&&R.shadow.map?R.shadow.map.texture:null;if(R.isAmbientLight)u+=U.r*C,h+=U.g*C,f+=U.b*C;else if(R.isLightProbe){for(let k=0;k<9;k++)i.probe[k].addScaledVector(R.sh.coefficients[k],C);w++}else if(R.isDirectionalLight){const k=e.get(R);if(k.color.copy(R.color).multiplyScalar(R.intensity),R.castShadow){const O=R.shadow,z=t.get(R);z.shadowIntensity=O.intensity,z.shadowBias=O.bias,z.shadowNormalBias=O.normalBias,z.shadowRadius=O.radius,z.shadowMapSize=O.mapSize,i.directionalShadow[m]=z,i.directionalShadowMap[m]=N,i.directionalShadowMatrix[m]=R.shadow.matrix,E++}i.directional[m]=k,m++}else if(R.isSpotLight){const k=e.get(R);k.position.setFromMatrixPosition(R.matrixWorld),k.color.copy(U).multiplyScalar(C),k.distance=P,k.coneCos=Math.cos(R.angle),k.penumbraCos=Math.cos(R.angle*(1-R.penumbra)),k.decay=R.decay,i.spot[_]=k;const O=R.shadow;if(R.map&&(i.spotLightMap[T]=R.map,T++,O.updateMatrices(R),R.castShadow&&y++),i.spotLightMatrix[_]=O.matrix,R.castShadow){const z=t.get(R);z.shadowIntensity=O.intensity,z.shadowBias=O.bias,z.shadowNormalBias=O.normalBias,z.shadowRadius=O.radius,z.shadowMapSize=O.mapSize,i.spotShadow[_]=z,i.spotShadowMap[_]=N,x++}_++}else if(R.isRectAreaLight){const k=e.get(R);k.color.copy(U).multiplyScalar(C),k.halfWidth.set(R.width*.5,0,0),k.halfHeight.set(0,R.height*.5,0),i.rectArea[p]=k,p++}else if(R.isPointLight){const k=e.get(R);if(k.color.copy(R.color).multiplyScalar(R.intensity),k.distance=R.distance,k.decay=R.decay,R.castShadow){const O=R.shadow,z=t.get(R);z.shadowIntensity=O.intensity,z.shadowBias=O.bias,z.shadowNormalBias=O.normalBias,z.shadowRadius=O.radius,z.shadowMapSize=O.mapSize,z.shadowCameraNear=O.camera.near,z.shadowCameraFar=O.camera.far,i.pointShadow[g]=z,i.pointShadowMap[g]=N,i.pointShadowMatrix[g]=R.shadow.matrix,S++}i.point[g]=k,g++}else if(R.isHemisphereLight){const k=e.get(R);k.skyColor.copy(R.color).multiplyScalar(C),k.groundColor.copy(R.groundColor).multiplyScalar(C),i.hemi[d]=k,d++}}p>0&&(n.has("OES_texture_float_linear")===!0?(i.rectAreaLTC1=he.LTC_FLOAT_1,i.rectAreaLTC2=he.LTC_FLOAT_2):(i.rectAreaLTC1=he.LTC_HALF_1,i.rectAreaLTC2=he.LTC_HALF_2)),i.ambient[0]=u,i.ambient[1]=h,i.ambient[2]=f;const D=i.hash;(D.directionalLength!==m||D.pointLength!==g||D.spotLength!==_||D.rectAreaLength!==p||D.hemiLength!==d||D.numDirectionalShadows!==E||D.numPointShadows!==S||D.numSpotShadows!==x||D.numSpotMaps!==T||D.numLightProbes!==w)&&(i.directional.length=m,i.spot.length=_,i.rectArea.length=p,i.point.length=g,i.hemi.length=d,i.directionalShadow.length=E,i.directionalShadowMap.length=E,i.pointShadow.length=S,i.pointShadowMap.length=S,i.spotShadow.length=x,i.spotShadowMap.length=x,i.directionalShadowMatrix.length=E,i.pointShadowMatrix.length=S,i.spotLightMatrix.length=x+T-y,i.spotLightMap.length=T,i.numSpotLightShadowsWithMaps=y,i.numLightProbes=w,D.directionalLength=m,D.pointLength=g,D.spotLength=_,D.rectAreaLength=p,D.hemiLength=d,D.numDirectionalShadows=E,D.numPointShadows=S,D.numSpotShadows=x,D.numSpotMaps=T,D.numLightProbes=w,i.version=dm++)}function c(l,u){let h=0,f=0,m=0,g=0,_=0;const p=u.matrixWorldInverse;for(let d=0,E=l.length;d<E;d++){const S=l[d];if(S.isDirectionalLight){const x=i.directional[h];x.direction.setFromMatrixPosition(S.matrixWorld),a.setFromMatrixPosition(S.target.matrixWorld),x.direction.sub(a),x.direction.transformDirection(p),h++}else if(S.isSpotLight){const x=i.spot[m];x.position.setFromMatrixPosition(S.matrixWorld),x.position.applyMatrix4(p),x.direction.setFromMatrixPosition(S.matrixWorld),a.setFromMatrixPosition(S.target.matrixWorld),x.direction.sub(a),x.direction.transformDirection(p),m++}else if(S.isRectAreaLight){const x=i.rectArea[g];x.position.setFromMatrixPosition(S.matrixWorld),x.position.applyMatrix4(p),s.identity(),r.copy(S.matrixWorld),r.premultiply(p),s.extractRotation(r),x.halfWidth.set(S.width*.5,0,0),x.halfHeight.set(0,S.height*.5,0),x.halfWidth.applyMatrix4(s),x.halfHeight.applyMatrix4(s),g++}else if(S.isPointLight){const x=i.point[f];x.position.setFromMatrixPosition(S.matrixWorld),x.position.applyMatrix4(p),f++}else if(S.isHemisphereLight){const x=i.hemi[_];x.direction.setFromMatrixPosition(S.matrixWorld),x.direction.transformDirection(p),_++}}}return{setup:o,setupView:c,state:i}}function oc(n){const e=new fm(n),t=[],i=[];function a(u){l.camera=u,t.length=0,i.length=0}function r(u){t.push(u)}function s(u){i.push(u)}function o(){e.setup(t)}function c(u){e.setupView(t,u)}const l={lightsArray:t,shadowsArray:i,camera:null,lights:e,transmissionRenderTarget:{}};return{init:a,state:l,setupLights:o,setupLightsView:c,pushLight:r,pushShadow:s}}function pm(n){let e=new WeakMap;function t(a,r=0){const s=e.get(a);let o;return s===void 0?(o=new oc(n),e.set(a,[o])):r>=s.length?(o=new oc(n),s.push(o)):o=s[r],o}function i(){e=new WeakMap}return{get:t,dispose:i}}const mm=`void main() {
	gl_Position = vec4( position, 1.0 );
}`,gm=`uniform sampler2D shadow_pass;
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
}`;function _m(n,e,t){let i=new Bs;const a=new Ke,r=new Ke,s=new dt,o=new Ou({depthPacking:Jl}),c=new Bu,l={},u=t.maxTextureSize,h={[Ln]:Lt,[Lt]:Ln,[mt]:mt},f=new Un({defines:{VSM_SAMPLES:8},uniforms:{shadow_pass:{value:null},resolution:{value:new Ke},radius:{value:4}},vertexShader:mm,fragmentShader:gm}),m=f.clone();m.defines.HORIZONTAL_PASS=1;const g=new $e;g.setAttribute("position",new tn(new Float32Array([-1,-1,.5,3,-1,.5,-1,3,.5]),3));const _=new Ge(g,f),p=this;this.enabled=!1,this.autoUpdate=!0,this.needsUpdate=!1,this.type=yc;let d=this.type;this.render=function(y,w,D){if(p.enabled===!1||p.autoUpdate===!1&&p.needsUpdate===!1||y.length===0)return;const M=n.getRenderTarget(),v=n.getActiveCubeFace(),R=n.getActiveMipmapLevel(),U=n.state;U.setBlending(In),U.buffers.color.setClear(1,1,1,1),U.buffers.depth.setTest(!0),U.setScissorTest(!1);const C=d!==dn&&this.type===dn,P=d===dn&&this.type!==dn;for(let N=0,k=y.length;N<k;N++){const O=y[N],z=O.shadow;if(z===void 0){console.warn("THREE.WebGLShadowMap:",O,"has no shadow.");continue}if(z.autoUpdate===!1&&z.needsUpdate===!1)continue;a.copy(z.mapSize);const H=z.getFrameExtents();if(a.multiply(H),r.copy(z.mapSize),(a.x>u||a.y>u)&&(a.x>u&&(r.x=Math.floor(u/H.x),a.x=r.x*H.x,z.mapSize.x=r.x),a.y>u&&(r.y=Math.floor(u/H.y),a.y=r.y*H.y,z.mapSize.y=r.y)),z.map===null||C===!0||P===!0){const Y=this.type!==dn?{minFilter:Jt,magFilter:Jt}:{};z.map!==null&&z.map.dispose(),z.map=new ti(a.x,a.y,Y),z.map.texture.name=O.name+".shadowMap",z.camera.updateProjectionMatrix()}n.setRenderTarget(z.map),n.clear();const $=z.getViewportCount();for(let Y=0;Y<$;Y++){const fe=z.getViewport(Y);s.set(r.x*fe.x,r.y*fe.y,r.x*fe.z,r.y*fe.w),U.viewport(s),z.updateMatrices(O,Y),i=z.getFrustum(),x(w,D,z.camera,O,this.type)}z.isPointLightShadow!==!0&&this.type===dn&&E(z,D),z.needsUpdate=!1}d=this.type,p.needsUpdate=!1,n.setRenderTarget(M,v,R)};function E(y,w){const D=e.update(_);f.defines.VSM_SAMPLES!==y.blurSamples&&(f.defines.VSM_SAMPLES=y.blurSamples,m.defines.VSM_SAMPLES=y.blurSamples,f.needsUpdate=!0,m.needsUpdate=!0),y.mapPass===null&&(y.mapPass=new ti(a.x,a.y)),f.uniforms.shadow_pass.value=y.map.texture,f.uniforms.resolution.value=y.mapSize,f.uniforms.radius.value=y.radius,n.setRenderTarget(y.mapPass),n.clear(),n.renderBufferDirect(w,null,D,f,_,null),m.uniforms.shadow_pass.value=y.mapPass.texture,m.uniforms.resolution.value=y.mapSize,m.uniforms.radius.value=y.radius,n.setRenderTarget(y.map),n.clear(),n.renderBufferDirect(w,null,D,m,_,null)}function S(y,w,D,M){let v=null;const R=D.isPointLight===!0?y.customDistanceMaterial:y.customDepthMaterial;if(R!==void 0)v=R;else if(v=D.isPointLight===!0?c:o,n.localClippingEnabled&&w.clipShadows===!0&&Array.isArray(w.clippingPlanes)&&w.clippingPlanes.length!==0||w.displacementMap&&w.displacementScale!==0||w.alphaMap&&w.alphaTest>0||w.map&&w.alphaTest>0){const U=v.uuid,C=w.uuid;let P=l[U];P===void 0&&(P={},l[U]=P);let N=P[C];N===void 0&&(N=v.clone(),P[C]=N,w.addEventListener("dispose",T)),v=N}if(v.visible=w.visible,v.wireframe=w.wireframe,M===dn?v.side=w.shadowSide!==null?w.shadowSide:w.side:v.side=w.shadowSide!==null?w.shadowSide:h[w.side],v.alphaMap=w.alphaMap,v.alphaTest=w.alphaTest,v.map=w.map,v.clipShadows=w.clipShadows,v.clippingPlanes=w.clippingPlanes,v.clipIntersection=w.clipIntersection,v.displacementMap=w.displacementMap,v.displacementScale=w.displacementScale,v.displacementBias=w.displacementBias,v.wireframeLinewidth=w.wireframeLinewidth,v.linewidth=w.linewidth,D.isPointLight===!0&&v.isMeshDistanceMaterial===!0){const U=n.properties.get(v);U.light=D}return v}function x(y,w,D,M,v){if(y.visible===!1)return;if(y.layers.test(w.layers)&&(y.isMesh||y.isLine||y.isPoints)&&(y.castShadow||y.receiveShadow&&v===dn)&&(!y.frustumCulled||i.intersectsObject(y))){y.modelViewMatrix.multiplyMatrices(D.matrixWorldInverse,y.matrixWorld);const C=e.update(y),P=y.material;if(Array.isArray(P)){const N=C.groups;for(let k=0,O=N.length;k<O;k++){const z=N[k],H=P[z.materialIndex];if(H&&H.visible){const $=S(y,H,M,v);y.onBeforeShadow(n,y,w,D,C,$,z),n.renderBufferDirect(D,null,C,$,y,z),y.onAfterShadow(n,y,w,D,C,$,z)}}}else if(P.visible){const N=S(y,P,M,v);y.onBeforeShadow(n,y,w,D,C,N,null),n.renderBufferDirect(D,null,C,N,y,null),y.onAfterShadow(n,y,w,D,C,N,null)}}const U=y.children;for(let C=0,P=U.length;C<P;C++)x(U[C],w,D,M,v)}function T(y){y.target.removeEventListener("dispose",T);for(const D in l){const M=l[D],v=y.target.uuid;v in M&&(M[v].dispose(),delete M[v])}}}const vm={[Nr]:Fr,[Or]:jr,[Br]:Hr,[Ti]:Vr,[Fr]:Nr,[jr]:Or,[Hr]:Br,[Vr]:Ti};function xm(n,e){function t(){let B=!1;const pe=new dt;let q=null;const te=new dt(0,0,0,0);return{setMask:function(xe){q!==xe&&!B&&(n.colorMask(xe,xe,xe,xe),q=xe)},setLocked:function(xe){B=xe},setClear:function(xe,ve,Oe,lt,bt){bt===!0&&(xe*=lt,ve*=lt,Oe*=lt),pe.set(xe,ve,Oe,lt),te.equals(pe)===!1&&(n.clearColor(xe,ve,Oe,lt),te.copy(pe))},reset:function(){B=!1,q=null,te.set(-1,0,0,0)}}}function i(){let B=!1,pe=!1,q=null,te=null,xe=null;return{setReversed:function(ve){if(pe!==ve){const Oe=e.get("EXT_clip_control");pe?Oe.clipControlEXT(Oe.LOWER_LEFT_EXT,Oe.ZERO_TO_ONE_EXT):Oe.clipControlEXT(Oe.LOWER_LEFT_EXT,Oe.NEGATIVE_ONE_TO_ONE_EXT);const lt=xe;xe=null,this.setClear(lt)}pe=ve},getReversed:function(){return pe},setTest:function(ve){ve?se(n.DEPTH_TEST):ee(n.DEPTH_TEST)},setMask:function(ve){q!==ve&&!B&&(n.depthMask(ve),q=ve)},setFunc:function(ve){if(pe&&(ve=vm[ve]),te!==ve){switch(ve){case Nr:n.depthFunc(n.NEVER);break;case Fr:n.depthFunc(n.ALWAYS);break;case Or:n.depthFunc(n.LESS);break;case Ti:n.depthFunc(n.LEQUAL);break;case Br:n.depthFunc(n.EQUAL);break;case Vr:n.depthFunc(n.GEQUAL);break;case jr:n.depthFunc(n.GREATER);break;case Hr:n.depthFunc(n.NOTEQUAL);break;default:n.depthFunc(n.LEQUAL)}te=ve}},setLocked:function(ve){B=ve},setClear:function(ve){xe!==ve&&(pe&&(ve=1-ve),n.clearDepth(ve),xe=ve)},reset:function(){B=!1,q=null,te=null,xe=null,pe=!1}}}function a(){let B=!1,pe=null,q=null,te=null,xe=null,ve=null,Oe=null,lt=null,bt=null;return{setTest:function(nt){B||(nt?se(n.STENCIL_TEST):ee(n.STENCIL_TEST))},setMask:function(nt){pe!==nt&&!B&&(n.stencilMask(nt),pe=nt)},setFunc:function(nt,Wt,nn){(q!==nt||te!==Wt||xe!==nn)&&(n.stencilFunc(nt,Wt,nn),q=nt,te=Wt,xe=nn)},setOp:function(nt,Wt,nn){(ve!==nt||Oe!==Wt||lt!==nn)&&(n.stencilOp(nt,Wt,nn),ve=nt,Oe=Wt,lt=nn)},setLocked:function(nt){B=nt},setClear:function(nt){bt!==nt&&(n.clearStencil(nt),bt=nt)},reset:function(){B=!1,pe=null,q=null,te=null,xe=null,ve=null,Oe=null,lt=null,bt=null}}}const r=new t,s=new i,o=new a,c=new WeakMap,l=new WeakMap;let u={},h={},f=new WeakMap,m=[],g=null,_=!1,p=null,d=null,E=null,S=null,x=null,T=null,y=null,w=new ce(0,0,0),D=0,M=!1,v=null,R=null,U=null,C=null,P=null;const N=n.getParameter(n.MAX_COMBINED_TEXTURE_IMAGE_UNITS);let k=!1,O=0;const z=n.getParameter(n.VERSION);z.indexOf("WebGL")!==-1?(O=parseFloat(/^WebGL (\d)/.exec(z)[1]),k=O>=1):z.indexOf("OpenGL ES")!==-1&&(O=parseFloat(/^OpenGL ES (\d)/.exec(z)[1]),k=O>=2);let H=null,$={};const Y=n.getParameter(n.SCISSOR_BOX),fe=n.getParameter(n.VIEWPORT),Ie=new dt().fromArray(Y),X=new dt().fromArray(fe);function ne(B,pe,q,te){const xe=new Uint8Array(4),ve=n.createTexture();n.bindTexture(B,ve),n.texParameteri(B,n.TEXTURE_MIN_FILTER,n.NEAREST),n.texParameteri(B,n.TEXTURE_MAG_FILTER,n.NEAREST);for(let Oe=0;Oe<q;Oe++)B===n.TEXTURE_3D||B===n.TEXTURE_2D_ARRAY?n.texImage3D(pe,0,n.RGBA,1,1,te,0,n.RGBA,n.UNSIGNED_BYTE,xe):n.texImage2D(pe+Oe,0,n.RGBA,1,1,0,n.RGBA,n.UNSIGNED_BYTE,xe);return ve}const ue={};ue[n.TEXTURE_2D]=ne(n.TEXTURE_2D,n.TEXTURE_2D,1),ue[n.TEXTURE_CUBE_MAP]=ne(n.TEXTURE_CUBE_MAP,n.TEXTURE_CUBE_MAP_POSITIVE_X,6),ue[n.TEXTURE_2D_ARRAY]=ne(n.TEXTURE_2D_ARRAY,n.TEXTURE_2D_ARRAY,1,1),ue[n.TEXTURE_3D]=ne(n.TEXTURE_3D,n.TEXTURE_3D,1,1),r.setClear(0,0,0,1),s.setClear(1),o.setClear(0),se(n.DEPTH_TEST),s.setFunc(Ti),Ce(!1),Re(io),se(n.CULL_FACE),L(In);function se(B){u[B]!==!0&&(n.enable(B),u[B]=!0)}function ee(B){u[B]!==!1&&(n.disable(B),u[B]=!1)}function _e(B,pe){return h[B]!==pe?(n.bindFramebuffer(B,pe),h[B]=pe,B===n.DRAW_FRAMEBUFFER&&(h[n.FRAMEBUFFER]=pe),B===n.FRAMEBUFFER&&(h[n.DRAW_FRAMEBUFFER]=pe),!0):!1}function de(B,pe){let q=m,te=!1;if(B){q=f.get(pe),q===void 0&&(q=[],f.set(pe,q));const xe=B.textures;if(q.length!==xe.length||q[0]!==n.COLOR_ATTACHMENT0){for(let ve=0,Oe=xe.length;ve<Oe;ve++)q[ve]=n.COLOR_ATTACHMENT0+ve;q.length=xe.length,te=!0}}else q[0]!==n.BACK&&(q[0]=n.BACK,te=!0);te&&n.drawBuffers(q)}function Z(B){return g!==B?(n.useProgram(B),g=B,!0):!1}const ae={[qn]:n.FUNC_ADD,[yl]:n.FUNC_SUBTRACT,[Tl]:n.FUNC_REVERSE_SUBTRACT};ae[Al]=n.MIN,ae[wl]=n.MAX;const re={[Rl]:n.ZERO,[Cl]:n.ONE,[Pl]:n.SRC_COLOR,[zr]:n.SRC_ALPHA,[kl]:n.SRC_ALPHA_SATURATE,[Ul]:n.DST_COLOR,[Dl]:n.DST_ALPHA,[Il]:n.ONE_MINUS_SRC_COLOR,[kr]:n.ONE_MINUS_SRC_ALPHA,[zl]:n.ONE_MINUS_DST_COLOR,[Ll]:n.ONE_MINUS_DST_ALPHA,[Nl]:n.CONSTANT_COLOR,[Fl]:n.ONE_MINUS_CONSTANT_COLOR,[Ol]:n.CONSTANT_ALPHA,[Bl]:n.ONE_MINUS_CONSTANT_ALPHA};function L(B,pe,q,te,xe,ve,Oe,lt,bt,nt){if(B===In){_===!0&&(ee(n.BLEND),_=!1);return}if(_===!1&&(se(n.BLEND),_=!0),B!==bl){if(B!==p||nt!==M){if((d!==qn||x!==qn)&&(n.blendEquation(n.FUNC_ADD),d=qn,x=qn),nt)switch(B){case Ei:n.blendFuncSeparate(n.ONE,n.ONE_MINUS_SRC_ALPHA,n.ONE,n.ONE_MINUS_SRC_ALPHA);break;case ao:n.blendFunc(n.ONE,n.ONE);break;case ro:n.blendFuncSeparate(n.ZERO,n.ONE_MINUS_SRC_COLOR,n.ZERO,n.ONE);break;case so:n.blendFuncSeparate(n.ZERO,n.SRC_COLOR,n.ZERO,n.SRC_ALPHA);break;default:console.error("THREE.WebGLState: Invalid blending: ",B);break}else switch(B){case Ei:n.blendFuncSeparate(n.SRC_ALPHA,n.ONE_MINUS_SRC_ALPHA,n.ONE,n.ONE_MINUS_SRC_ALPHA);break;case ao:n.blendFunc(n.SRC_ALPHA,n.ONE);break;case ro:n.blendFuncSeparate(n.ZERO,n.ONE_MINUS_SRC_COLOR,n.ZERO,n.ONE);break;case so:n.blendFunc(n.ZERO,n.SRC_COLOR);break;default:console.error("THREE.WebGLState: Invalid blending: ",B);break}E=null,S=null,T=null,y=null,w.set(0,0,0),D=0,p=B,M=nt}return}xe=xe||pe,ve=ve||q,Oe=Oe||te,(pe!==d||xe!==x)&&(n.blendEquationSeparate(ae[pe],ae[xe]),d=pe,x=xe),(q!==E||te!==S||ve!==T||Oe!==y)&&(n.blendFuncSeparate(re[q],re[te],re[ve],re[Oe]),E=q,S=te,T=ve,y=Oe),(lt.equals(w)===!1||bt!==D)&&(n.blendColor(lt.r,lt.g,lt.b,bt),w.copy(lt),D=bt),p=B,M=!1}function Le(B,pe){B.side===mt?ee(n.CULL_FACE):se(n.CULL_FACE);let q=B.side===Lt;pe&&(q=!q),Ce(q),B.blending===Ei&&B.transparent===!1?L(In):L(B.blending,B.blendEquation,B.blendSrc,B.blendDst,B.blendEquationAlpha,B.blendSrcAlpha,B.blendDstAlpha,B.blendColor,B.blendAlpha,B.premultipliedAlpha),s.setFunc(B.depthFunc),s.setTest(B.depthTest),s.setMask(B.depthWrite),r.setMask(B.colorWrite);const te=B.stencilWrite;o.setTest(te),te&&(o.setMask(B.stencilWriteMask),o.setFunc(B.stencilFunc,B.stencilRef,B.stencilFuncMask),o.setOp(B.stencilFail,B.stencilZFail,B.stencilZPass)),Fe(B.polygonOffset,B.polygonOffsetFactor,B.polygonOffsetUnits),B.alphaToCoverage===!0?se(n.SAMPLE_ALPHA_TO_COVERAGE):ee(n.SAMPLE_ALPHA_TO_COVERAGE)}function Ce(B){v!==B&&(B?n.frontFace(n.CW):n.frontFace(n.CCW),v=B)}function Re(B){B!==Ml?(se(n.CULL_FACE),B!==R&&(B===io?n.cullFace(n.BACK):B===Sl?n.cullFace(n.FRONT):n.cullFace(n.FRONT_AND_BACK))):ee(n.CULL_FACE),R=B}function Me(B){B!==U&&(k&&n.lineWidth(B),U=B)}function Fe(B,pe,q){B?(se(n.POLYGON_OFFSET_FILL),(C!==pe||P!==q)&&(n.polygonOffset(pe,q),C=pe,P=q)):ee(n.POLYGON_OFFSET_FILL)}function we(B){B?se(n.SCISSOR_TEST):ee(n.SCISSOR_TEST)}function I(B){B===void 0&&(B=n.TEXTURE0+N-1),H!==B&&(n.activeTexture(B),H=B)}function b(B,pe,q){q===void 0&&(H===null?q=n.TEXTURE0+N-1:q=H);let te=$[q];te===void 0&&(te={type:void 0,texture:void 0},$[q]=te),(te.type!==B||te.texture!==pe)&&(H!==q&&(n.activeTexture(q),H=q),n.bindTexture(B,pe||ue[B]),te.type=B,te.texture=pe)}function G(){const B=$[H];B!==void 0&&B.type!==void 0&&(n.bindTexture(B.type,null),B.type=void 0,B.texture=void 0)}function Q(){try{n.compressedTexImage2D(...arguments)}catch(B){console.error("THREE.WebGLState:",B)}}function ie(){try{n.compressedTexImage3D(...arguments)}catch(B){console.error("THREE.WebGLState:",B)}}function J(){try{n.texSubImage2D(...arguments)}catch(B){console.error("THREE.WebGLState:",B)}}function Ae(){try{n.texSubImage3D(...arguments)}catch(B){console.error("THREE.WebGLState:",B)}}function ge(){try{n.compressedTexSubImage2D(...arguments)}catch(B){console.error("THREE.WebGLState:",B)}}function Ee(){try{n.compressedTexSubImage3D(...arguments)}catch(B){console.error("THREE.WebGLState:",B)}}function Ye(){try{n.texStorage2D(...arguments)}catch(B){console.error("THREE.WebGLState:",B)}}function le(){try{n.texStorage3D(...arguments)}catch(B){console.error("THREE.WebGLState:",B)}}function be(){try{n.texImage2D(...arguments)}catch(B){console.error("THREE.WebGLState:",B)}}function Ue(){try{n.texImage3D(...arguments)}catch(B){console.error("THREE.WebGLState:",B)}}function ze(B){Ie.equals(B)===!1&&(n.scissor(B.x,B.y,B.z,B.w),Ie.copy(B))}function ye(B){X.equals(B)===!1&&(n.viewport(B.x,B.y,B.z,B.w),X.copy(B))}function qe(B,pe){let q=l.get(pe);q===void 0&&(q=new WeakMap,l.set(pe,q));let te=q.get(B);te===void 0&&(te=n.getUniformBlockIndex(pe,B.name),q.set(B,te))}function Ve(B,pe){const te=l.get(pe).get(B);c.get(pe)!==te&&(n.uniformBlockBinding(pe,te,B.__bindingPointIndex),c.set(pe,te))}function rt(){n.disable(n.BLEND),n.disable(n.CULL_FACE),n.disable(n.DEPTH_TEST),n.disable(n.POLYGON_OFFSET_FILL),n.disable(n.SCISSOR_TEST),n.disable(n.STENCIL_TEST),n.disable(n.SAMPLE_ALPHA_TO_COVERAGE),n.blendEquation(n.FUNC_ADD),n.blendFunc(n.ONE,n.ZERO),n.blendFuncSeparate(n.ONE,n.ZERO,n.ONE,n.ZERO),n.blendColor(0,0,0,0),n.colorMask(!0,!0,!0,!0),n.clearColor(0,0,0,0),n.depthMask(!0),n.depthFunc(n.LESS),s.setReversed(!1),n.clearDepth(1),n.stencilMask(4294967295),n.stencilFunc(n.ALWAYS,0,4294967295),n.stencilOp(n.KEEP,n.KEEP,n.KEEP),n.clearStencil(0),n.cullFace(n.BACK),n.frontFace(n.CCW),n.polygonOffset(0,0),n.activeTexture(n.TEXTURE0),n.bindFramebuffer(n.FRAMEBUFFER,null),n.bindFramebuffer(n.DRAW_FRAMEBUFFER,null),n.bindFramebuffer(n.READ_FRAMEBUFFER,null),n.useProgram(null),n.lineWidth(1),n.scissor(0,0,n.canvas.width,n.canvas.height),n.viewport(0,0,n.canvas.width,n.canvas.height),u={},H=null,$={},h={},f=new WeakMap,m=[],g=null,_=!1,p=null,d=null,E=null,S=null,x=null,T=null,y=null,w=new ce(0,0,0),D=0,M=!1,v=null,R=null,U=null,C=null,P=null,Ie.set(0,0,n.canvas.width,n.canvas.height),X.set(0,0,n.canvas.width,n.canvas.height),r.reset(),s.reset(),o.reset()}return{buffers:{color:r,depth:s,stencil:o},enable:se,disable:ee,bindFramebuffer:_e,drawBuffers:de,useProgram:Z,setBlending:L,setMaterial:Le,setFlipSided:Ce,setCullFace:Re,setLineWidth:Me,setPolygonOffset:Fe,setScissorTest:we,activeTexture:I,bindTexture:b,unbindTexture:G,compressedTexImage2D:Q,compressedTexImage3D:ie,texImage2D:be,texImage3D:Ue,updateUBOMapping:qe,uniformBlockBinding:Ve,texStorage2D:Ye,texStorage3D:le,texSubImage2D:J,texSubImage3D:Ae,compressedTexSubImage2D:ge,compressedTexSubImage3D:Ee,scissor:ze,viewport:ye,reset:rt}}function Mm(n,e,t,i,a,r,s){const o=e.has("WEBGL_multisampled_render_to_texture")?e.get("WEBGL_multisampled_render_to_texture"):null,c=typeof navigator>"u"?!1:/OculusBrowser/g.test(navigator.userAgent),l=new Ke,u=new WeakMap;let h;const f=new WeakMap;let m=!1;try{m=typeof OffscreenCanvas<"u"&&new OffscreenCanvas(1,1).getContext("2d")!==null}catch{}function g(I,b){return m?new OffscreenCanvas(I,b):Ba("canvas")}function _(I,b,G){let Q=1;const ie=we(I);if((ie.width>G||ie.height>G)&&(Q=G/Math.max(ie.width,ie.height)),Q<1)if(typeof HTMLImageElement<"u"&&I instanceof HTMLImageElement||typeof HTMLCanvasElement<"u"&&I instanceof HTMLCanvasElement||typeof ImageBitmap<"u"&&I instanceof ImageBitmap||typeof VideoFrame<"u"&&I instanceof VideoFrame){const J=Math.floor(Q*ie.width),Ae=Math.floor(Q*ie.height);h===void 0&&(h=g(J,Ae));const ge=b?g(J,Ae):h;return ge.width=J,ge.height=Ae,ge.getContext("2d").drawImage(I,0,0,J,Ae),console.warn("THREE.WebGLRenderer: Texture has been resized from ("+ie.width+"x"+ie.height+") to ("+J+"x"+Ae+")."),ge}else return"data"in I&&console.warn("THREE.WebGLRenderer: Image in DataTexture is too big ("+ie.width+"x"+ie.height+")."),I;return I}function p(I){return I.generateMipmaps}function d(I){n.generateMipmap(I)}function E(I){return I.isWebGLCubeRenderTarget?n.TEXTURE_CUBE_MAP:I.isWebGL3DRenderTarget?n.TEXTURE_3D:I.isWebGLArrayRenderTarget||I.isCompressedArrayTexture?n.TEXTURE_2D_ARRAY:n.TEXTURE_2D}function S(I,b,G,Q,ie=!1){if(I!==null){if(n[I]!==void 0)return n[I];console.warn("THREE.WebGLRenderer: Attempt to use non-existing WebGL internal format '"+I+"'")}let J=b;if(b===n.RED&&(G===n.FLOAT&&(J=n.R32F),G===n.HALF_FLOAT&&(J=n.R16F),G===n.UNSIGNED_BYTE&&(J=n.R8)),b===n.RED_INTEGER&&(G===n.UNSIGNED_BYTE&&(J=n.R8UI),G===n.UNSIGNED_SHORT&&(J=n.R16UI),G===n.UNSIGNED_INT&&(J=n.R32UI),G===n.BYTE&&(J=n.R8I),G===n.SHORT&&(J=n.R16I),G===n.INT&&(J=n.R32I)),b===n.RG&&(G===n.FLOAT&&(J=n.RG32F),G===n.HALF_FLOAT&&(J=n.RG16F),G===n.UNSIGNED_BYTE&&(J=n.RG8)),b===n.RG_INTEGER&&(G===n.UNSIGNED_BYTE&&(J=n.RG8UI),G===n.UNSIGNED_SHORT&&(J=n.RG16UI),G===n.UNSIGNED_INT&&(J=n.RG32UI),G===n.BYTE&&(J=n.RG8I),G===n.SHORT&&(J=n.RG16I),G===n.INT&&(J=n.RG32I)),b===n.RGB_INTEGER&&(G===n.UNSIGNED_BYTE&&(J=n.RGB8UI),G===n.UNSIGNED_SHORT&&(J=n.RGB16UI),G===n.UNSIGNED_INT&&(J=n.RGB32UI),G===n.BYTE&&(J=n.RGB8I),G===n.SHORT&&(J=n.RGB16I),G===n.INT&&(J=n.RGB32I)),b===n.RGBA_INTEGER&&(G===n.UNSIGNED_BYTE&&(J=n.RGBA8UI),G===n.UNSIGNED_SHORT&&(J=n.RGBA16UI),G===n.UNSIGNED_INT&&(J=n.RGBA32UI),G===n.BYTE&&(J=n.RGBA8I),G===n.SHORT&&(J=n.RGBA16I),G===n.INT&&(J=n.RGBA32I)),b===n.RGB&&G===n.UNSIGNED_INT_5_9_9_9_REV&&(J=n.RGB9_E5),b===n.RGBA){const Ae=ie?Fa:Qe.getTransfer(Q);G===n.FLOAT&&(J=n.RGBA32F),G===n.HALF_FLOAT&&(J=n.RGBA16F),G===n.UNSIGNED_BYTE&&(J=Ae===at?n.SRGB8_ALPHA8:n.RGBA8),G===n.UNSIGNED_SHORT_4_4_4_4&&(J=n.RGBA4),G===n.UNSIGNED_SHORT_5_5_5_1&&(J=n.RGB5_A1)}return(J===n.R16F||J===n.R32F||J===n.RG16F||J===n.RG32F||J===n.RGBA16F||J===n.RGBA32F)&&e.get("EXT_color_buffer_float"),J}function x(I,b){let G;return I?b===null||b===ei||b===Ri?G=n.DEPTH24_STENCIL8:b===fn?G=n.DEPTH32F_STENCIL8:b===Ki&&(G=n.DEPTH24_STENCIL8,console.warn("DepthTexture: 16 bit depth attachment is not supported with stencil. Using 24-bit attachment.")):b===null||b===ei||b===Ri?G=n.DEPTH_COMPONENT24:b===fn?G=n.DEPTH_COMPONENT32F:b===Ki&&(G=n.DEPTH_COMPONENT16),G}function T(I,b){return p(I)===!0||I.isFramebufferTexture&&I.minFilter!==Jt&&I.minFilter!==en?Math.log2(Math.max(b.width,b.height))+1:I.mipmaps!==void 0&&I.mipmaps.length>0?I.mipmaps.length:I.isCompressedTexture&&Array.isArray(I.image)?b.mipmaps.length:1}function y(I){const b=I.target;b.removeEventListener("dispose",y),D(b),b.isVideoTexture&&u.delete(b)}function w(I){const b=I.target;b.removeEventListener("dispose",w),v(b)}function D(I){const b=i.get(I);if(b.__webglInit===void 0)return;const G=I.source,Q=f.get(G);if(Q){const ie=Q[b.__cacheKey];ie.usedTimes--,ie.usedTimes===0&&M(I),Object.keys(Q).length===0&&f.delete(G)}i.remove(I)}function M(I){const b=i.get(I);n.deleteTexture(b.__webglTexture);const G=I.source,Q=f.get(G);delete Q[b.__cacheKey],s.memory.textures--}function v(I){const b=i.get(I);if(I.depthTexture&&(I.depthTexture.dispose(),i.remove(I.depthTexture)),I.isWebGLCubeRenderTarget)for(let Q=0;Q<6;Q++){if(Array.isArray(b.__webglFramebuffer[Q]))for(let ie=0;ie<b.__webglFramebuffer[Q].length;ie++)n.deleteFramebuffer(b.__webglFramebuffer[Q][ie]);else n.deleteFramebuffer(b.__webglFramebuffer[Q]);b.__webglDepthbuffer&&n.deleteRenderbuffer(b.__webglDepthbuffer[Q])}else{if(Array.isArray(b.__webglFramebuffer))for(let Q=0;Q<b.__webglFramebuffer.length;Q++)n.deleteFramebuffer(b.__webglFramebuffer[Q]);else n.deleteFramebuffer(b.__webglFramebuffer);if(b.__webglDepthbuffer&&n.deleteRenderbuffer(b.__webglDepthbuffer),b.__webglMultisampledFramebuffer&&n.deleteFramebuffer(b.__webglMultisampledFramebuffer),b.__webglColorRenderbuffer)for(let Q=0;Q<b.__webglColorRenderbuffer.length;Q++)b.__webglColorRenderbuffer[Q]&&n.deleteRenderbuffer(b.__webglColorRenderbuffer[Q]);b.__webglDepthRenderbuffer&&n.deleteRenderbuffer(b.__webglDepthRenderbuffer)}const G=I.textures;for(let Q=0,ie=G.length;Q<ie;Q++){const J=i.get(G[Q]);J.__webglTexture&&(n.deleteTexture(J.__webglTexture),s.memory.textures--),i.remove(G[Q])}i.remove(I)}let R=0;function U(){R=0}function C(){const I=R;return I>=a.maxTextures&&console.warn("THREE.WebGLTextures: Trying to use "+I+" texture units while this GPU supports only "+a.maxTextures),R+=1,I}function P(I){const b=[];return b.push(I.wrapS),b.push(I.wrapT),b.push(I.wrapR||0),b.push(I.magFilter),b.push(I.minFilter),b.push(I.anisotropy),b.push(I.internalFormat),b.push(I.format),b.push(I.type),b.push(I.generateMipmaps),b.push(I.premultiplyAlpha),b.push(I.flipY),b.push(I.unpackAlignment),b.push(I.colorSpace),b.join()}function N(I,b){const G=i.get(I);if(I.isVideoTexture&&Me(I),I.isRenderTargetTexture===!1&&I.version>0&&G.__version!==I.version){const Q=I.image;if(Q===null)console.warn("THREE.WebGLRenderer: Texture marked for update but no image data found.");else if(Q.complete===!1)console.warn("THREE.WebGLRenderer: Texture marked for update but image is incomplete");else{X(G,I,b);return}}t.bindTexture(n.TEXTURE_2D,G.__webglTexture,n.TEXTURE0+b)}function k(I,b){const G=i.get(I);if(I.version>0&&G.__version!==I.version){X(G,I,b);return}t.bindTexture(n.TEXTURE_2D_ARRAY,G.__webglTexture,n.TEXTURE0+b)}function O(I,b){const G=i.get(I);if(I.version>0&&G.__version!==I.version){X(G,I,b);return}t.bindTexture(n.TEXTURE_3D,G.__webglTexture,n.TEXTURE0+b)}function z(I,b){const G=i.get(I);if(I.version>0&&G.__version!==I.version){ne(G,I,b);return}t.bindTexture(n.TEXTURE_CUBE_MAP,G.__webglTexture,n.TEXTURE0+b)}const H={[Xr]:n.REPEAT,[Yn]:n.CLAMP_TO_EDGE,[Kr]:n.MIRRORED_REPEAT},$={[Jt]:n.NEAREST,[Yl]:n.NEAREST_MIPMAP_NEAREST,[ia]:n.NEAREST_MIPMAP_LINEAR,[en]:n.LINEAR,[Za]:n.LINEAR_MIPMAP_NEAREST,[Zn]:n.LINEAR_MIPMAP_LINEAR},Y={[eu]:n.NEVER,[su]:n.ALWAYS,[tu]:n.LESS,[Fc]:n.LEQUAL,[nu]:n.EQUAL,[ru]:n.GEQUAL,[iu]:n.GREATER,[au]:n.NOTEQUAL};function fe(I,b){if(b.type===fn&&e.has("OES_texture_float_linear")===!1&&(b.magFilter===en||b.magFilter===Za||b.magFilter===ia||b.magFilter===Zn||b.minFilter===en||b.minFilter===Za||b.minFilter===ia||b.minFilter===Zn)&&console.warn("THREE.WebGLRenderer: Unable to use linear filtering with floating point textures. OES_texture_float_linear not supported on this device."),n.texParameteri(I,n.TEXTURE_WRAP_S,H[b.wrapS]),n.texParameteri(I,n.TEXTURE_WRAP_T,H[b.wrapT]),(I===n.TEXTURE_3D||I===n.TEXTURE_2D_ARRAY)&&n.texParameteri(I,n.TEXTURE_WRAP_R,H[b.wrapR]),n.texParameteri(I,n.TEXTURE_MAG_FILTER,$[b.magFilter]),n.texParameteri(I,n.TEXTURE_MIN_FILTER,$[b.minFilter]),b.compareFunction&&(n.texParameteri(I,n.TEXTURE_COMPARE_MODE,n.COMPARE_REF_TO_TEXTURE),n.texParameteri(I,n.TEXTURE_COMPARE_FUNC,Y[b.compareFunction])),e.has("EXT_texture_filter_anisotropic")===!0){if(b.magFilter===Jt||b.minFilter!==ia&&b.minFilter!==Zn||b.type===fn&&e.has("OES_texture_float_linear")===!1)return;if(b.anisotropy>1||i.get(b).__currentAnisotropy){const G=e.get("EXT_texture_filter_anisotropic");n.texParameterf(I,G.TEXTURE_MAX_ANISOTROPY_EXT,Math.min(b.anisotropy,a.getMaxAnisotropy())),i.get(b).__currentAnisotropy=b.anisotropy}}}function Ie(I,b){let G=!1;I.__webglInit===void 0&&(I.__webglInit=!0,b.addEventListener("dispose",y));const Q=b.source;let ie=f.get(Q);ie===void 0&&(ie={},f.set(Q,ie));const J=P(b);if(J!==I.__cacheKey){ie[J]===void 0&&(ie[J]={texture:n.createTexture(),usedTimes:0},s.memory.textures++,G=!0),ie[J].usedTimes++;const Ae=ie[I.__cacheKey];Ae!==void 0&&(ie[I.__cacheKey].usedTimes--,Ae.usedTimes===0&&M(b)),I.__cacheKey=J,I.__webglTexture=ie[J].texture}return G}function X(I,b,G){let Q=n.TEXTURE_2D;(b.isDataArrayTexture||b.isCompressedArrayTexture)&&(Q=n.TEXTURE_2D_ARRAY),b.isData3DTexture&&(Q=n.TEXTURE_3D);const ie=Ie(I,b),J=b.source;t.bindTexture(Q,I.__webglTexture,n.TEXTURE0+G);const Ae=i.get(J);if(J.version!==Ae.__version||ie===!0){t.activeTexture(n.TEXTURE0+G);const ge=Qe.getPrimaries(Qe.workingColorSpace),Ee=b.colorSpace===Cn?null:Qe.getPrimaries(b.colorSpace),Ye=b.colorSpace===Cn||ge===Ee?n.NONE:n.BROWSER_DEFAULT_WEBGL;n.pixelStorei(n.UNPACK_FLIP_Y_WEBGL,b.flipY),n.pixelStorei(n.UNPACK_PREMULTIPLY_ALPHA_WEBGL,b.premultiplyAlpha),n.pixelStorei(n.UNPACK_ALIGNMENT,b.unpackAlignment),n.pixelStorei(n.UNPACK_COLORSPACE_CONVERSION_WEBGL,Ye);let le=_(b.image,!1,a.maxTextureSize);le=Fe(b,le);const be=r.convert(b.format,b.colorSpace),Ue=r.convert(b.type);let ze=S(b.internalFormat,be,Ue,b.colorSpace,b.isVideoTexture);fe(Q,b);let ye;const qe=b.mipmaps,Ve=b.isVideoTexture!==!0,rt=Ae.__version===void 0||ie===!0,B=J.dataReady,pe=T(b,le);if(b.isDepthTexture)ze=x(b.format===Ci,b.type),rt&&(Ve?t.texStorage2D(n.TEXTURE_2D,1,ze,le.width,le.height):t.texImage2D(n.TEXTURE_2D,0,ze,le.width,le.height,0,be,Ue,null));else if(b.isDataTexture)if(qe.length>0){Ve&&rt&&t.texStorage2D(n.TEXTURE_2D,pe,ze,qe[0].width,qe[0].height);for(let q=0,te=qe.length;q<te;q++)ye=qe[q],Ve?B&&t.texSubImage2D(n.TEXTURE_2D,q,0,0,ye.width,ye.height,be,Ue,ye.data):t.texImage2D(n.TEXTURE_2D,q,ze,ye.width,ye.height,0,be,Ue,ye.data);b.generateMipmaps=!1}else Ve?(rt&&t.texStorage2D(n.TEXTURE_2D,pe,ze,le.width,le.height),B&&t.texSubImage2D(n.TEXTURE_2D,0,0,0,le.width,le.height,be,Ue,le.data)):t.texImage2D(n.TEXTURE_2D,0,ze,le.width,le.height,0,be,Ue,le.data);else if(b.isCompressedTexture)if(b.isCompressedArrayTexture){Ve&&rt&&t.texStorage3D(n.TEXTURE_2D_ARRAY,pe,ze,qe[0].width,qe[0].height,le.depth);for(let q=0,te=qe.length;q<te;q++)if(ye=qe[q],b.format!==Zt)if(be!==null)if(Ve){if(B)if(b.layerUpdates.size>0){const xe=No(ye.width,ye.height,b.format,b.type);for(const ve of b.layerUpdates){const Oe=ye.data.subarray(ve*xe/ye.data.BYTES_PER_ELEMENT,(ve+1)*xe/ye.data.BYTES_PER_ELEMENT);t.compressedTexSubImage3D(n.TEXTURE_2D_ARRAY,q,0,0,ve,ye.width,ye.height,1,be,Oe)}b.clearLayerUpdates()}else t.compressedTexSubImage3D(n.TEXTURE_2D_ARRAY,q,0,0,0,ye.width,ye.height,le.depth,be,ye.data)}else t.compressedTexImage3D(n.TEXTURE_2D_ARRAY,q,ze,ye.width,ye.height,le.depth,0,ye.data,0,0);else console.warn("THREE.WebGLRenderer: Attempt to load unsupported compressed texture format in .uploadTexture()");else Ve?B&&t.texSubImage3D(n.TEXTURE_2D_ARRAY,q,0,0,0,ye.width,ye.height,le.depth,be,Ue,ye.data):t.texImage3D(n.TEXTURE_2D_ARRAY,q,ze,ye.width,ye.height,le.depth,0,be,Ue,ye.data)}else{Ve&&rt&&t.texStorage2D(n.TEXTURE_2D,pe,ze,qe[0].width,qe[0].height);for(let q=0,te=qe.length;q<te;q++)ye=qe[q],b.format!==Zt?be!==null?Ve?B&&t.compressedTexSubImage2D(n.TEXTURE_2D,q,0,0,ye.width,ye.height,be,ye.data):t.compressedTexImage2D(n.TEXTURE_2D,q,ze,ye.width,ye.height,0,ye.data):console.warn("THREE.WebGLRenderer: Attempt to load unsupported compressed texture format in .uploadTexture()"):Ve?B&&t.texSubImage2D(n.TEXTURE_2D,q,0,0,ye.width,ye.height,be,Ue,ye.data):t.texImage2D(n.TEXTURE_2D,q,ze,ye.width,ye.height,0,be,Ue,ye.data)}else if(b.isDataArrayTexture)if(Ve){if(rt&&t.texStorage3D(n.TEXTURE_2D_ARRAY,pe,ze,le.width,le.height,le.depth),B)if(b.layerUpdates.size>0){const q=No(le.width,le.height,b.format,b.type);for(const te of b.layerUpdates){const xe=le.data.subarray(te*q/le.data.BYTES_PER_ELEMENT,(te+1)*q/le.data.BYTES_PER_ELEMENT);t.texSubImage3D(n.TEXTURE_2D_ARRAY,0,0,0,te,le.width,le.height,1,be,Ue,xe)}b.clearLayerUpdates()}else t.texSubImage3D(n.TEXTURE_2D_ARRAY,0,0,0,0,le.width,le.height,le.depth,be,Ue,le.data)}else t.texImage3D(n.TEXTURE_2D_ARRAY,0,ze,le.width,le.height,le.depth,0,be,Ue,le.data);else if(b.isData3DTexture)Ve?(rt&&t.texStorage3D(n.TEXTURE_3D,pe,ze,le.width,le.height,le.depth),B&&t.texSubImage3D(n.TEXTURE_3D,0,0,0,0,le.width,le.height,le.depth,be,Ue,le.data)):t.texImage3D(n.TEXTURE_3D,0,ze,le.width,le.height,le.depth,0,be,Ue,le.data);else if(b.isFramebufferTexture){if(rt)if(Ve)t.texStorage2D(n.TEXTURE_2D,pe,ze,le.width,le.height);else{let q=le.width,te=le.height;for(let xe=0;xe<pe;xe++)t.texImage2D(n.TEXTURE_2D,xe,ze,q,te,0,be,Ue,null),q>>=1,te>>=1}}else if(qe.length>0){if(Ve&&rt){const q=we(qe[0]);t.texStorage2D(n.TEXTURE_2D,pe,ze,q.width,q.height)}for(let q=0,te=qe.length;q<te;q++)ye=qe[q],Ve?B&&t.texSubImage2D(n.TEXTURE_2D,q,0,0,be,Ue,ye):t.texImage2D(n.TEXTURE_2D,q,ze,be,Ue,ye);b.generateMipmaps=!1}else if(Ve){if(rt){const q=we(le);t.texStorage2D(n.TEXTURE_2D,pe,ze,q.width,q.height)}B&&t.texSubImage2D(n.TEXTURE_2D,0,0,0,be,Ue,le)}else t.texImage2D(n.TEXTURE_2D,0,ze,be,Ue,le);p(b)&&d(Q),Ae.__version=J.version,b.onUpdate&&b.onUpdate(b)}I.__version=b.version}function ne(I,b,G){if(b.image.length!==6)return;const Q=Ie(I,b),ie=b.source;t.bindTexture(n.TEXTURE_CUBE_MAP,I.__webglTexture,n.TEXTURE0+G);const J=i.get(ie);if(ie.version!==J.__version||Q===!0){t.activeTexture(n.TEXTURE0+G);const Ae=Qe.getPrimaries(Qe.workingColorSpace),ge=b.colorSpace===Cn?null:Qe.getPrimaries(b.colorSpace),Ee=b.colorSpace===Cn||Ae===ge?n.NONE:n.BROWSER_DEFAULT_WEBGL;n.pixelStorei(n.UNPACK_FLIP_Y_WEBGL,b.flipY),n.pixelStorei(n.UNPACK_PREMULTIPLY_ALPHA_WEBGL,b.premultiplyAlpha),n.pixelStorei(n.UNPACK_ALIGNMENT,b.unpackAlignment),n.pixelStorei(n.UNPACK_COLORSPACE_CONVERSION_WEBGL,Ee);const Ye=b.isCompressedTexture||b.image[0].isCompressedTexture,le=b.image[0]&&b.image[0].isDataTexture,be=[];for(let te=0;te<6;te++)!Ye&&!le?be[te]=_(b.image[te],!0,a.maxCubemapSize):be[te]=le?b.image[te].image:b.image[te],be[te]=Fe(b,be[te]);const Ue=be[0],ze=r.convert(b.format,b.colorSpace),ye=r.convert(b.type),qe=S(b.internalFormat,ze,ye,b.colorSpace),Ve=b.isVideoTexture!==!0,rt=J.__version===void 0||Q===!0,B=ie.dataReady;let pe=T(b,Ue);fe(n.TEXTURE_CUBE_MAP,b);let q;if(Ye){Ve&&rt&&t.texStorage2D(n.TEXTURE_CUBE_MAP,pe,qe,Ue.width,Ue.height);for(let te=0;te<6;te++){q=be[te].mipmaps;for(let xe=0;xe<q.length;xe++){const ve=q[xe];b.format!==Zt?ze!==null?Ve?B&&t.compressedTexSubImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+te,xe,0,0,ve.width,ve.height,ze,ve.data):t.compressedTexImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+te,xe,qe,ve.width,ve.height,0,ve.data):console.warn("THREE.WebGLRenderer: Attempt to load unsupported compressed texture format in .setTextureCube()"):Ve?B&&t.texSubImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+te,xe,0,0,ve.width,ve.height,ze,ye,ve.data):t.texImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+te,xe,qe,ve.width,ve.height,0,ze,ye,ve.data)}}}else{if(q=b.mipmaps,Ve&&rt){q.length>0&&pe++;const te=we(be[0]);t.texStorage2D(n.TEXTURE_CUBE_MAP,pe,qe,te.width,te.height)}for(let te=0;te<6;te++)if(le){Ve?B&&t.texSubImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+te,0,0,0,be[te].width,be[te].height,ze,ye,be[te].data):t.texImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+te,0,qe,be[te].width,be[te].height,0,ze,ye,be[te].data);for(let xe=0;xe<q.length;xe++){const Oe=q[xe].image[te].image;Ve?B&&t.texSubImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+te,xe+1,0,0,Oe.width,Oe.height,ze,ye,Oe.data):t.texImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+te,xe+1,qe,Oe.width,Oe.height,0,ze,ye,Oe.data)}}else{Ve?B&&t.texSubImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+te,0,0,0,ze,ye,be[te]):t.texImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+te,0,qe,ze,ye,be[te]);for(let xe=0;xe<q.length;xe++){const ve=q[xe];Ve?B&&t.texSubImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+te,xe+1,0,0,ze,ye,ve.image[te]):t.texImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+te,xe+1,qe,ze,ye,ve.image[te])}}}p(b)&&d(n.TEXTURE_CUBE_MAP),J.__version=ie.version,b.onUpdate&&b.onUpdate(b)}I.__version=b.version}function ue(I,b,G,Q,ie,J){const Ae=r.convert(G.format,G.colorSpace),ge=r.convert(G.type),Ee=S(G.internalFormat,Ae,ge,G.colorSpace),Ye=i.get(b),le=i.get(G);if(le.__renderTarget=b,!Ye.__hasExternalTextures){const be=Math.max(1,b.width>>J),Ue=Math.max(1,b.height>>J);ie===n.TEXTURE_3D||ie===n.TEXTURE_2D_ARRAY?t.texImage3D(ie,J,Ee,be,Ue,b.depth,0,Ae,ge,null):t.texImage2D(ie,J,Ee,be,Ue,0,Ae,ge,null)}t.bindFramebuffer(n.FRAMEBUFFER,I),Re(b)?o.framebufferTexture2DMultisampleEXT(n.FRAMEBUFFER,Q,ie,le.__webglTexture,0,Ce(b)):(ie===n.TEXTURE_2D||ie>=n.TEXTURE_CUBE_MAP_POSITIVE_X&&ie<=n.TEXTURE_CUBE_MAP_NEGATIVE_Z)&&n.framebufferTexture2D(n.FRAMEBUFFER,Q,ie,le.__webglTexture,J),t.bindFramebuffer(n.FRAMEBUFFER,null)}function se(I,b,G){if(n.bindRenderbuffer(n.RENDERBUFFER,I),b.depthBuffer){const Q=b.depthTexture,ie=Q&&Q.isDepthTexture?Q.type:null,J=x(b.stencilBuffer,ie),Ae=b.stencilBuffer?n.DEPTH_STENCIL_ATTACHMENT:n.DEPTH_ATTACHMENT,ge=Ce(b);Re(b)?o.renderbufferStorageMultisampleEXT(n.RENDERBUFFER,ge,J,b.width,b.height):G?n.renderbufferStorageMultisample(n.RENDERBUFFER,ge,J,b.width,b.height):n.renderbufferStorage(n.RENDERBUFFER,J,b.width,b.height),n.framebufferRenderbuffer(n.FRAMEBUFFER,Ae,n.RENDERBUFFER,I)}else{const Q=b.textures;for(let ie=0;ie<Q.length;ie++){const J=Q[ie],Ae=r.convert(J.format,J.colorSpace),ge=r.convert(J.type),Ee=S(J.internalFormat,Ae,ge,J.colorSpace),Ye=Ce(b);G&&Re(b)===!1?n.renderbufferStorageMultisample(n.RENDERBUFFER,Ye,Ee,b.width,b.height):Re(b)?o.renderbufferStorageMultisampleEXT(n.RENDERBUFFER,Ye,Ee,b.width,b.height):n.renderbufferStorage(n.RENDERBUFFER,Ee,b.width,b.height)}}n.bindRenderbuffer(n.RENDERBUFFER,null)}function ee(I,b){if(b&&b.isWebGLCubeRenderTarget)throw new Error("Depth Texture with cube render targets is not supported");if(t.bindFramebuffer(n.FRAMEBUFFER,I),!(b.depthTexture&&b.depthTexture.isDepthTexture))throw new Error("renderTarget.depthTexture must be an instance of THREE.DepthTexture");const Q=i.get(b.depthTexture);Q.__renderTarget=b,(!Q.__webglTexture||b.depthTexture.image.width!==b.width||b.depthTexture.image.height!==b.height)&&(b.depthTexture.image.width=b.width,b.depthTexture.image.height=b.height,b.depthTexture.needsUpdate=!0),N(b.depthTexture,0);const ie=Q.__webglTexture,J=Ce(b);if(b.depthTexture.format===bi)Re(b)?o.framebufferTexture2DMultisampleEXT(n.FRAMEBUFFER,n.DEPTH_ATTACHMENT,n.TEXTURE_2D,ie,0,J):n.framebufferTexture2D(n.FRAMEBUFFER,n.DEPTH_ATTACHMENT,n.TEXTURE_2D,ie,0);else if(b.depthTexture.format===Ci)Re(b)?o.framebufferTexture2DMultisampleEXT(n.FRAMEBUFFER,n.DEPTH_STENCIL_ATTACHMENT,n.TEXTURE_2D,ie,0,J):n.framebufferTexture2D(n.FRAMEBUFFER,n.DEPTH_STENCIL_ATTACHMENT,n.TEXTURE_2D,ie,0);else throw new Error("Unknown depthTexture format")}function _e(I){const b=i.get(I),G=I.isWebGLCubeRenderTarget===!0;if(b.__boundDepthTexture!==I.depthTexture){const Q=I.depthTexture;if(b.__depthDisposeCallback&&b.__depthDisposeCallback(),Q){const ie=()=>{delete b.__boundDepthTexture,delete b.__depthDisposeCallback,Q.removeEventListener("dispose",ie)};Q.addEventListener("dispose",ie),b.__depthDisposeCallback=ie}b.__boundDepthTexture=Q}if(I.depthTexture&&!b.__autoAllocateDepthBuffer){if(G)throw new Error("target.depthTexture not supported in Cube render targets");ee(b.__webglFramebuffer,I)}else if(G){b.__webglDepthbuffer=[];for(let Q=0;Q<6;Q++)if(t.bindFramebuffer(n.FRAMEBUFFER,b.__webglFramebuffer[Q]),b.__webglDepthbuffer[Q]===void 0)b.__webglDepthbuffer[Q]=n.createRenderbuffer(),se(b.__webglDepthbuffer[Q],I,!1);else{const ie=I.stencilBuffer?n.DEPTH_STENCIL_ATTACHMENT:n.DEPTH_ATTACHMENT,J=b.__webglDepthbuffer[Q];n.bindRenderbuffer(n.RENDERBUFFER,J),n.framebufferRenderbuffer(n.FRAMEBUFFER,ie,n.RENDERBUFFER,J)}}else if(t.bindFramebuffer(n.FRAMEBUFFER,b.__webglFramebuffer),b.__webglDepthbuffer===void 0)b.__webglDepthbuffer=n.createRenderbuffer(),se(b.__webglDepthbuffer,I,!1);else{const Q=I.stencilBuffer?n.DEPTH_STENCIL_ATTACHMENT:n.DEPTH_ATTACHMENT,ie=b.__webglDepthbuffer;n.bindRenderbuffer(n.RENDERBUFFER,ie),n.framebufferRenderbuffer(n.FRAMEBUFFER,Q,n.RENDERBUFFER,ie)}t.bindFramebuffer(n.FRAMEBUFFER,null)}function de(I,b,G){const Q=i.get(I);b!==void 0&&ue(Q.__webglFramebuffer,I,I.texture,n.COLOR_ATTACHMENT0,n.TEXTURE_2D,0),G!==void 0&&_e(I)}function Z(I){const b=I.texture,G=i.get(I),Q=i.get(b);I.addEventListener("dispose",w);const ie=I.textures,J=I.isWebGLCubeRenderTarget===!0,Ae=ie.length>1;if(Ae||(Q.__webglTexture===void 0&&(Q.__webglTexture=n.createTexture()),Q.__version=b.version,s.memory.textures++),J){G.__webglFramebuffer=[];for(let ge=0;ge<6;ge++)if(b.mipmaps&&b.mipmaps.length>0){G.__webglFramebuffer[ge]=[];for(let Ee=0;Ee<b.mipmaps.length;Ee++)G.__webglFramebuffer[ge][Ee]=n.createFramebuffer()}else G.__webglFramebuffer[ge]=n.createFramebuffer()}else{if(b.mipmaps&&b.mipmaps.length>0){G.__webglFramebuffer=[];for(let ge=0;ge<b.mipmaps.length;ge++)G.__webglFramebuffer[ge]=n.createFramebuffer()}else G.__webglFramebuffer=n.createFramebuffer();if(Ae)for(let ge=0,Ee=ie.length;ge<Ee;ge++){const Ye=i.get(ie[ge]);Ye.__webglTexture===void 0&&(Ye.__webglTexture=n.createTexture(),s.memory.textures++)}if(I.samples>0&&Re(I)===!1){G.__webglMultisampledFramebuffer=n.createFramebuffer(),G.__webglColorRenderbuffer=[],t.bindFramebuffer(n.FRAMEBUFFER,G.__webglMultisampledFramebuffer);for(let ge=0;ge<ie.length;ge++){const Ee=ie[ge];G.__webglColorRenderbuffer[ge]=n.createRenderbuffer(),n.bindRenderbuffer(n.RENDERBUFFER,G.__webglColorRenderbuffer[ge]);const Ye=r.convert(Ee.format,Ee.colorSpace),le=r.convert(Ee.type),be=S(Ee.internalFormat,Ye,le,Ee.colorSpace,I.isXRRenderTarget===!0),Ue=Ce(I);n.renderbufferStorageMultisample(n.RENDERBUFFER,Ue,be,I.width,I.height),n.framebufferRenderbuffer(n.FRAMEBUFFER,n.COLOR_ATTACHMENT0+ge,n.RENDERBUFFER,G.__webglColorRenderbuffer[ge])}n.bindRenderbuffer(n.RENDERBUFFER,null),I.depthBuffer&&(G.__webglDepthRenderbuffer=n.createRenderbuffer(),se(G.__webglDepthRenderbuffer,I,!0)),t.bindFramebuffer(n.FRAMEBUFFER,null)}}if(J){t.bindTexture(n.TEXTURE_CUBE_MAP,Q.__webglTexture),fe(n.TEXTURE_CUBE_MAP,b);for(let ge=0;ge<6;ge++)if(b.mipmaps&&b.mipmaps.length>0)for(let Ee=0;Ee<b.mipmaps.length;Ee++)ue(G.__webglFramebuffer[ge][Ee],I,b,n.COLOR_ATTACHMENT0,n.TEXTURE_CUBE_MAP_POSITIVE_X+ge,Ee);else ue(G.__webglFramebuffer[ge],I,b,n.COLOR_ATTACHMENT0,n.TEXTURE_CUBE_MAP_POSITIVE_X+ge,0);p(b)&&d(n.TEXTURE_CUBE_MAP),t.unbindTexture()}else if(Ae){for(let ge=0,Ee=ie.length;ge<Ee;ge++){const Ye=ie[ge],le=i.get(Ye);t.bindTexture(n.TEXTURE_2D,le.__webglTexture),fe(n.TEXTURE_2D,Ye),ue(G.__webglFramebuffer,I,Ye,n.COLOR_ATTACHMENT0+ge,n.TEXTURE_2D,0),p(Ye)&&d(n.TEXTURE_2D)}t.unbindTexture()}else{let ge=n.TEXTURE_2D;if((I.isWebGL3DRenderTarget||I.isWebGLArrayRenderTarget)&&(ge=I.isWebGL3DRenderTarget?n.TEXTURE_3D:n.TEXTURE_2D_ARRAY),t.bindTexture(ge,Q.__webglTexture),fe(ge,b),b.mipmaps&&b.mipmaps.length>0)for(let Ee=0;Ee<b.mipmaps.length;Ee++)ue(G.__webglFramebuffer[Ee],I,b,n.COLOR_ATTACHMENT0,ge,Ee);else ue(G.__webglFramebuffer,I,b,n.COLOR_ATTACHMENT0,ge,0);p(b)&&d(ge),t.unbindTexture()}I.depthBuffer&&_e(I)}function ae(I){const b=I.textures;for(let G=0,Q=b.length;G<Q;G++){const ie=b[G];if(p(ie)){const J=E(I),Ae=i.get(ie).__webglTexture;t.bindTexture(J,Ae),d(J),t.unbindTexture()}}}const re=[],L=[];function Le(I){if(I.samples>0){if(Re(I)===!1){const b=I.textures,G=I.width,Q=I.height;let ie=n.COLOR_BUFFER_BIT;const J=I.stencilBuffer?n.DEPTH_STENCIL_ATTACHMENT:n.DEPTH_ATTACHMENT,Ae=i.get(I),ge=b.length>1;if(ge)for(let Ee=0;Ee<b.length;Ee++)t.bindFramebuffer(n.FRAMEBUFFER,Ae.__webglMultisampledFramebuffer),n.framebufferRenderbuffer(n.FRAMEBUFFER,n.COLOR_ATTACHMENT0+Ee,n.RENDERBUFFER,null),t.bindFramebuffer(n.FRAMEBUFFER,Ae.__webglFramebuffer),n.framebufferTexture2D(n.DRAW_FRAMEBUFFER,n.COLOR_ATTACHMENT0+Ee,n.TEXTURE_2D,null,0);t.bindFramebuffer(n.READ_FRAMEBUFFER,Ae.__webglMultisampledFramebuffer),t.bindFramebuffer(n.DRAW_FRAMEBUFFER,Ae.__webglFramebuffer);for(let Ee=0;Ee<b.length;Ee++){if(I.resolveDepthBuffer&&(I.depthBuffer&&(ie|=n.DEPTH_BUFFER_BIT),I.stencilBuffer&&I.resolveStencilBuffer&&(ie|=n.STENCIL_BUFFER_BIT)),ge){n.framebufferRenderbuffer(n.READ_FRAMEBUFFER,n.COLOR_ATTACHMENT0,n.RENDERBUFFER,Ae.__webglColorRenderbuffer[Ee]);const Ye=i.get(b[Ee]).__webglTexture;n.framebufferTexture2D(n.DRAW_FRAMEBUFFER,n.COLOR_ATTACHMENT0,n.TEXTURE_2D,Ye,0)}n.blitFramebuffer(0,0,G,Q,0,0,G,Q,ie,n.NEAREST),c===!0&&(re.length=0,L.length=0,re.push(n.COLOR_ATTACHMENT0+Ee),I.depthBuffer&&I.resolveDepthBuffer===!1&&(re.push(J),L.push(J),n.invalidateFramebuffer(n.DRAW_FRAMEBUFFER,L)),n.invalidateFramebuffer(n.READ_FRAMEBUFFER,re))}if(t.bindFramebuffer(n.READ_FRAMEBUFFER,null),t.bindFramebuffer(n.DRAW_FRAMEBUFFER,null),ge)for(let Ee=0;Ee<b.length;Ee++){t.bindFramebuffer(n.FRAMEBUFFER,Ae.__webglMultisampledFramebuffer),n.framebufferRenderbuffer(n.FRAMEBUFFER,n.COLOR_ATTACHMENT0+Ee,n.RENDERBUFFER,Ae.__webglColorRenderbuffer[Ee]);const Ye=i.get(b[Ee]).__webglTexture;t.bindFramebuffer(n.FRAMEBUFFER,Ae.__webglFramebuffer),n.framebufferTexture2D(n.DRAW_FRAMEBUFFER,n.COLOR_ATTACHMENT0+Ee,n.TEXTURE_2D,Ye,0)}t.bindFramebuffer(n.DRAW_FRAMEBUFFER,Ae.__webglMultisampledFramebuffer)}else if(I.depthBuffer&&I.resolveDepthBuffer===!1&&c){const b=I.stencilBuffer?n.DEPTH_STENCIL_ATTACHMENT:n.DEPTH_ATTACHMENT;n.invalidateFramebuffer(n.DRAW_FRAMEBUFFER,[b])}}}function Ce(I){return Math.min(a.maxSamples,I.samples)}function Re(I){const b=i.get(I);return I.samples>0&&e.has("WEBGL_multisampled_render_to_texture")===!0&&b.__useRenderToTexture!==!1}function Me(I){const b=s.render.frame;u.get(I)!==b&&(u.set(I,b),I.update())}function Fe(I,b){const G=I.colorSpace,Q=I.format,ie=I.type;return I.isCompressedTexture===!0||I.isVideoTexture===!0||G!==Pi&&G!==Cn&&(Qe.getTransfer(G)===at?(Q!==Zt||ie!==_n)&&console.warn("THREE.WebGLTextures: sRGB encoded textures have to use RGBAFormat and UnsignedByteType."):console.error("THREE.WebGLTextures: Unsupported texture color space:",G)),b}function we(I){return typeof HTMLImageElement<"u"&&I instanceof HTMLImageElement?(l.width=I.naturalWidth||I.width,l.height=I.naturalHeight||I.height):typeof VideoFrame<"u"&&I instanceof VideoFrame?(l.width=I.displayWidth,l.height=I.displayHeight):(l.width=I.width,l.height=I.height),l}this.allocateTextureUnit=C,this.resetTextureUnits=U,this.setTexture2D=N,this.setTexture2DArray=k,this.setTexture3D=O,this.setTextureCube=z,this.rebindTextures=de,this.setupRenderTarget=Z,this.updateRenderTargetMipmap=ae,this.updateMultisampleRenderTarget=Le,this.setupDepthRenderbuffer=_e,this.setupFrameBufferTexture=ue,this.useMultisampledRTT=Re}function Sm(n,e){function t(i,a=Cn){let r;const s=Qe.getTransfer(a);if(i===_n)return n.UNSIGNED_BYTE;if(i===Ds)return n.UNSIGNED_SHORT_4_4_4_4;if(i===Ls)return n.UNSIGNED_SHORT_5_5_5_1;if(i===Cc)return n.UNSIGNED_INT_5_9_9_9_REV;if(i===wc)return n.BYTE;if(i===Rc)return n.SHORT;if(i===Ki)return n.UNSIGNED_SHORT;if(i===Is)return n.INT;if(i===ei)return n.UNSIGNED_INT;if(i===fn)return n.FLOAT;if(i===Yi)return n.HALF_FLOAT;if(i===Pc)return n.ALPHA;if(i===Ic)return n.RGB;if(i===Zt)return n.RGBA;if(i===Dc)return n.LUMINANCE;if(i===Lc)return n.LUMINANCE_ALPHA;if(i===bi)return n.DEPTH_COMPONENT;if(i===Ci)return n.DEPTH_STENCIL;if(i===Uc)return n.RED;if(i===Us)return n.RED_INTEGER;if(i===zc)return n.RG;if(i===zs)return n.RG_INTEGER;if(i===ks)return n.RGBA_INTEGER;if(i===Pa||i===Ia||i===Da||i===La)if(s===at)if(r=e.get("WEBGL_compressed_texture_s3tc_srgb"),r!==null){if(i===Pa)return r.COMPRESSED_SRGB_S3TC_DXT1_EXT;if(i===Ia)return r.COMPRESSED_SRGB_ALPHA_S3TC_DXT1_EXT;if(i===Da)return r.COMPRESSED_SRGB_ALPHA_S3TC_DXT3_EXT;if(i===La)return r.COMPRESSED_SRGB_ALPHA_S3TC_DXT5_EXT}else return null;else if(r=e.get("WEBGL_compressed_texture_s3tc"),r!==null){if(i===Pa)return r.COMPRESSED_RGB_S3TC_DXT1_EXT;if(i===Ia)return r.COMPRESSED_RGBA_S3TC_DXT1_EXT;if(i===Da)return r.COMPRESSED_RGBA_S3TC_DXT3_EXT;if(i===La)return r.COMPRESSED_RGBA_S3TC_DXT5_EXT}else return null;if(i===qr||i===$r||i===Yr||i===Zr)if(r=e.get("WEBGL_compressed_texture_pvrtc"),r!==null){if(i===qr)return r.COMPRESSED_RGB_PVRTC_4BPPV1_IMG;if(i===$r)return r.COMPRESSED_RGB_PVRTC_2BPPV1_IMG;if(i===Yr)return r.COMPRESSED_RGBA_PVRTC_4BPPV1_IMG;if(i===Zr)return r.COMPRESSED_RGBA_PVRTC_2BPPV1_IMG}else return null;if(i===Jr||i===Qr||i===es)if(r=e.get("WEBGL_compressed_texture_etc"),r!==null){if(i===Jr||i===Qr)return s===at?r.COMPRESSED_SRGB8_ETC2:r.COMPRESSED_RGB8_ETC2;if(i===es)return s===at?r.COMPRESSED_SRGB8_ALPHA8_ETC2_EAC:r.COMPRESSED_RGBA8_ETC2_EAC}else return null;if(i===ts||i===ns||i===is||i===as||i===rs||i===ss||i===os||i===cs||i===ls||i===us||i===ds||i===hs||i===fs||i===ps)if(r=e.get("WEBGL_compressed_texture_astc"),r!==null){if(i===ts)return s===at?r.COMPRESSED_SRGB8_ALPHA8_ASTC_4x4_KHR:r.COMPRESSED_RGBA_ASTC_4x4_KHR;if(i===ns)return s===at?r.COMPRESSED_SRGB8_ALPHA8_ASTC_5x4_KHR:r.COMPRESSED_RGBA_ASTC_5x4_KHR;if(i===is)return s===at?r.COMPRESSED_SRGB8_ALPHA8_ASTC_5x5_KHR:r.COMPRESSED_RGBA_ASTC_5x5_KHR;if(i===as)return s===at?r.COMPRESSED_SRGB8_ALPHA8_ASTC_6x5_KHR:r.COMPRESSED_RGBA_ASTC_6x5_KHR;if(i===rs)return s===at?r.COMPRESSED_SRGB8_ALPHA8_ASTC_6x6_KHR:r.COMPRESSED_RGBA_ASTC_6x6_KHR;if(i===ss)return s===at?r.COMPRESSED_SRGB8_ALPHA8_ASTC_8x5_KHR:r.COMPRESSED_RGBA_ASTC_8x5_KHR;if(i===os)return s===at?r.COMPRESSED_SRGB8_ALPHA8_ASTC_8x6_KHR:r.COMPRESSED_RGBA_ASTC_8x6_KHR;if(i===cs)return s===at?r.COMPRESSED_SRGB8_ALPHA8_ASTC_8x8_KHR:r.COMPRESSED_RGBA_ASTC_8x8_KHR;if(i===ls)return s===at?r.COMPRESSED_SRGB8_ALPHA8_ASTC_10x5_KHR:r.COMPRESSED_RGBA_ASTC_10x5_KHR;if(i===us)return s===at?r.COMPRESSED_SRGB8_ALPHA8_ASTC_10x6_KHR:r.COMPRESSED_RGBA_ASTC_10x6_KHR;if(i===ds)return s===at?r.COMPRESSED_SRGB8_ALPHA8_ASTC_10x8_KHR:r.COMPRESSED_RGBA_ASTC_10x8_KHR;if(i===hs)return s===at?r.COMPRESSED_SRGB8_ALPHA8_ASTC_10x10_KHR:r.COMPRESSED_RGBA_ASTC_10x10_KHR;if(i===fs)return s===at?r.COMPRESSED_SRGB8_ALPHA8_ASTC_12x10_KHR:r.COMPRESSED_RGBA_ASTC_12x10_KHR;if(i===ps)return s===at?r.COMPRESSED_SRGB8_ALPHA8_ASTC_12x12_KHR:r.COMPRESSED_RGBA_ASTC_12x12_KHR}else return null;if(i===Ua||i===ms||i===gs)if(r=e.get("EXT_texture_compression_bptc"),r!==null){if(i===Ua)return s===at?r.COMPRESSED_SRGB_ALPHA_BPTC_UNORM_EXT:r.COMPRESSED_RGBA_BPTC_UNORM_EXT;if(i===ms)return r.COMPRESSED_RGB_BPTC_SIGNED_FLOAT_EXT;if(i===gs)return r.COMPRESSED_RGB_BPTC_UNSIGNED_FLOAT_EXT}else return null;if(i===kc||i===_s||i===vs||i===xs)if(r=e.get("EXT_texture_compression_rgtc"),r!==null){if(i===Ua)return r.COMPRESSED_RED_RGTC1_EXT;if(i===_s)return r.COMPRESSED_SIGNED_RED_RGTC1_EXT;if(i===vs)return r.COMPRESSED_RED_GREEN_RGTC2_EXT;if(i===xs)return r.COMPRESSED_SIGNED_RED_GREEN_RGTC2_EXT}else return null;return i===Ri?n.UNSIGNED_INT_24_8:n[i]!==void 0?n[i]:null}return{convert:t}}const Em=`
void main() {

	gl_Position = vec4( position, 1.0 );

}`,bm=`
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

}`;class ym{constructor(){this.texture=null,this.mesh=null,this.depthNear=0,this.depthFar=0}init(e,t,i){if(this.texture===null){const a=new Ct,r=e.properties.get(a);r.__webglTexture=t.texture,(t.depthNear!==i.depthNear||t.depthFar!==i.depthFar)&&(this.depthNear=t.depthNear,this.depthFar=t.depthFar),this.texture=a}}getMesh(e){if(this.texture!==null&&this.mesh===null){const t=e.cameras[0].viewport,i=new Un({vertexShader:Em,fragmentShader:bm,uniforms:{depthColor:{value:this.texture},depthWidth:{value:t.z},depthHeight:{value:t.w}}});this.mesh=new Ge(new zi(20,20),i)}return this.mesh}reset(){this.texture=null,this.mesh=null}getDepthTexture(){return this.texture}}class Tm extends Di{constructor(e,t){super();const i=this;let a=null,r=1,s=null,o="local-floor",c=1,l=null,u=null,h=null,f=null,m=null,g=null;const _=new ym,p=t.getContextAttributes();let d=null,E=null;const S=[],x=[],T=new Ke;let y=null;const w=new Ht;w.viewport=new dt;const D=new Ht;D.viewport=new dt;const M=[w,D],v=new Wu;let R=null,U=null;this.cameraAutoUpdate=!0,this.enabled=!1,this.isPresenting=!1,this.getController=function(X){let ne=S[X];return ne===void 0&&(ne=new vr,S[X]=ne),ne.getTargetRaySpace()},this.getControllerGrip=function(X){let ne=S[X];return ne===void 0&&(ne=new vr,S[X]=ne),ne.getGripSpace()},this.getHand=function(X){let ne=S[X];return ne===void 0&&(ne=new vr,S[X]=ne),ne.getHandSpace()};function C(X){const ne=x.indexOf(X.inputSource);if(ne===-1)return;const ue=S[ne];ue!==void 0&&(ue.update(X.inputSource,X.frame,l||s),ue.dispatchEvent({type:X.type,data:X.inputSource}))}function P(){a.removeEventListener("select",C),a.removeEventListener("selectstart",C),a.removeEventListener("selectend",C),a.removeEventListener("squeeze",C),a.removeEventListener("squeezestart",C),a.removeEventListener("squeezeend",C),a.removeEventListener("end",P),a.removeEventListener("inputsourceschange",N);for(let X=0;X<S.length;X++){const ne=x[X];ne!==null&&(x[X]=null,S[X].disconnect(ne))}R=null,U=null,_.reset(),e.setRenderTarget(d),m=null,f=null,h=null,a=null,E=null,Ie.stop(),i.isPresenting=!1,e.setPixelRatio(y),e.setSize(T.width,T.height,!1),i.dispatchEvent({type:"sessionend"})}this.setFramebufferScaleFactor=function(X){r=X,i.isPresenting===!0&&console.warn("THREE.WebXRManager: Cannot change framebuffer scale while presenting.")},this.setReferenceSpaceType=function(X){o=X,i.isPresenting===!0&&console.warn("THREE.WebXRManager: Cannot change reference space type while presenting.")},this.getReferenceSpace=function(){return l||s},this.setReferenceSpace=function(X){l=X},this.getBaseLayer=function(){return f!==null?f:m},this.getBinding=function(){return h},this.getFrame=function(){return g},this.getSession=function(){return a},this.setSession=async function(X){if(a=X,a!==null){if(d=e.getRenderTarget(),a.addEventListener("select",C),a.addEventListener("selectstart",C),a.addEventListener("selectend",C),a.addEventListener("squeeze",C),a.addEventListener("squeezestart",C),a.addEventListener("squeezeend",C),a.addEventListener("end",P),a.addEventListener("inputsourceschange",N),p.xrCompatible!==!0&&await t.makeXRCompatible(),y=e.getPixelRatio(),e.getSize(T),typeof XRWebGLBinding<"u"&&"createProjectionLayer"in XRWebGLBinding.prototype){let ue=null,se=null,ee=null;p.depth&&(ee=p.stencil?t.DEPTH24_STENCIL8:t.DEPTH_COMPONENT24,ue=p.stencil?Ci:bi,se=p.stencil?Ri:ei);const _e={colorFormat:t.RGBA8,depthFormat:ee,scaleFactor:r};h=new XRWebGLBinding(a,t),f=h.createProjectionLayer(_e),a.updateRenderState({layers:[f]}),e.setPixelRatio(1),e.setSize(f.textureWidth,f.textureHeight,!1),E=new ti(f.textureWidth,f.textureHeight,{format:Zt,type:_n,depthTexture:new Kc(f.textureWidth,f.textureHeight,se,void 0,void 0,void 0,void 0,void 0,void 0,ue),stencilBuffer:p.stencil,colorSpace:e.outputColorSpace,samples:p.antialias?4:0,resolveDepthBuffer:f.ignoreDepthValues===!1,resolveStencilBuffer:f.ignoreDepthValues===!1})}else{const ue={antialias:p.antialias,alpha:!0,depth:p.depth,stencil:p.stencil,framebufferScaleFactor:r};m=new XRWebGLLayer(a,t,ue),a.updateRenderState({baseLayer:m}),e.setPixelRatio(1),e.setSize(m.framebufferWidth,m.framebufferHeight,!1),E=new ti(m.framebufferWidth,m.framebufferHeight,{format:Zt,type:_n,colorSpace:e.outputColorSpace,stencilBuffer:p.stencil,resolveDepthBuffer:m.ignoreDepthValues===!1,resolveStencilBuffer:m.ignoreDepthValues===!1})}E.isXRRenderTarget=!0,this.setFoveation(c),l=null,s=await a.requestReferenceSpace(o),Ie.setContext(a),Ie.start(),i.isPresenting=!0,i.dispatchEvent({type:"sessionstart"})}},this.getEnvironmentBlendMode=function(){if(a!==null)return a.environmentBlendMode},this.getDepthTexture=function(){return _.getDepthTexture()};function N(X){for(let ne=0;ne<X.removed.length;ne++){const ue=X.removed[ne],se=x.indexOf(ue);se>=0&&(x[se]=null,S[se].disconnect(ue))}for(let ne=0;ne<X.added.length;ne++){const ue=X.added[ne];let se=x.indexOf(ue);if(se===-1){for(let _e=0;_e<S.length;_e++)if(_e>=x.length){x.push(ue),se=_e;break}else if(x[_e]===null){x[_e]=ue,se=_e;break}if(se===-1)break}const ee=S[se];ee&&ee.connect(ue)}}const k=new F,O=new F;function z(X,ne,ue){k.setFromMatrixPosition(ne.matrixWorld),O.setFromMatrixPosition(ue.matrixWorld);const se=k.distanceTo(O),ee=ne.projectionMatrix.elements,_e=ue.projectionMatrix.elements,de=ee[14]/(ee[10]-1),Z=ee[14]/(ee[10]+1),ae=(ee[9]+1)/ee[5],re=(ee[9]-1)/ee[5],L=(ee[8]-1)/ee[0],Le=(_e[8]+1)/_e[0],Ce=de*L,Re=de*Le,Me=se/(-L+Le),Fe=Me*-L;if(ne.matrixWorld.decompose(X.position,X.quaternion,X.scale),X.translateX(Fe),X.translateZ(Me),X.matrixWorld.compose(X.position,X.quaternion,X.scale),X.matrixWorldInverse.copy(X.matrixWorld).invert(),ee[10]===-1)X.projectionMatrix.copy(ne.projectionMatrix),X.projectionMatrixInverse.copy(ne.projectionMatrixInverse);else{const we=de+Me,I=Z+Me,b=Ce-Fe,G=Re+(se-Fe),Q=ae*Z/I*we,ie=re*Z/I*we;X.projectionMatrix.makePerspective(b,G,Q,ie,we,I),X.projectionMatrixInverse.copy(X.projectionMatrix).invert()}}function H(X,ne){ne===null?X.matrixWorld.copy(X.matrix):X.matrixWorld.multiplyMatrices(ne.matrixWorld,X.matrix),X.matrixWorldInverse.copy(X.matrixWorld).invert()}this.updateCamera=function(X){if(a===null)return;let ne=X.near,ue=X.far;_.texture!==null&&(_.depthNear>0&&(ne=_.depthNear),_.depthFar>0&&(ue=_.depthFar)),v.near=D.near=w.near=ne,v.far=D.far=w.far=ue,(R!==v.near||U!==v.far)&&(a.updateRenderState({depthNear:v.near,depthFar:v.far}),R=v.near,U=v.far),w.layers.mask=X.layers.mask|2,D.layers.mask=X.layers.mask|4,v.layers.mask=w.layers.mask|D.layers.mask;const se=X.parent,ee=v.cameras;H(v,se);for(let _e=0;_e<ee.length;_e++)H(ee[_e],se);ee.length===2?z(v,w,D):v.projectionMatrix.copy(w.projectionMatrix),$(X,v,se)};function $(X,ne,ue){ue===null?X.matrix.copy(ne.matrixWorld):(X.matrix.copy(ue.matrixWorld),X.matrix.invert(),X.matrix.multiply(ne.matrixWorld)),X.matrix.decompose(X.position,X.quaternion,X.scale),X.updateMatrixWorld(!0),X.projectionMatrix.copy(ne.projectionMatrix),X.projectionMatrixInverse.copy(ne.projectionMatrixInverse),X.isPerspectiveCamera&&(X.fov=Ms*2*Math.atan(1/X.projectionMatrix.elements[5]),X.zoom=1)}this.getCamera=function(){return v},this.getFoveation=function(){if(!(f===null&&m===null))return c},this.setFoveation=function(X){c=X,f!==null&&(f.fixedFoveation=X),m!==null&&m.fixedFoveation!==void 0&&(m.fixedFoveation=X)},this.hasDepthSensing=function(){return _.texture!==null},this.getDepthSensingMesh=function(){return _.getMesh(v)};let Y=null;function fe(X,ne){if(u=ne.getViewerPose(l||s),g=ne,u!==null){const ue=u.views;m!==null&&(e.setRenderTargetFramebuffer(E,m.framebuffer),e.setRenderTarget(E));let se=!1;ue.length!==v.cameras.length&&(v.cameras.length=0,se=!0);for(let de=0;de<ue.length;de++){const Z=ue[de];let ae=null;if(m!==null)ae=m.getViewport(Z);else{const L=h.getViewSubImage(f,Z);ae=L.viewport,de===0&&(e.setRenderTargetTextures(E,L.colorTexture,f.ignoreDepthValues?void 0:L.depthStencilTexture),e.setRenderTarget(E))}let re=M[de];re===void 0&&(re=new Ht,re.layers.enable(de),re.viewport=new dt,M[de]=re),re.matrix.fromArray(Z.transform.matrix),re.matrix.decompose(re.position,re.quaternion,re.scale),re.projectionMatrix.fromArray(Z.projectionMatrix),re.projectionMatrixInverse.copy(re.projectionMatrix).invert(),re.viewport.set(ae.x,ae.y,ae.width,ae.height),de===0&&(v.matrix.copy(re.matrix),v.matrix.decompose(v.position,v.quaternion,v.scale)),se===!0&&v.cameras.push(re)}const ee=a.enabledFeatures;if(ee&&ee.includes("depth-sensing")&&a.depthUsage=="gpu-optimized"&&h){const de=h.getDepthInformation(ue[0]);de&&de.isValid&&de.texture&&_.init(e,de,a.renderState)}}for(let ue=0;ue<S.length;ue++){const se=x[ue],ee=S[ue];se!==null&&ee!==void 0&&ee.update(se,ne,l||s)}Y&&Y(X,ne),ne.detectedPlanes&&i.dispatchEvent({type:"planesdetected",data:ne}),g=null}const Ie=new Yc;Ie.setAnimationLoop(fe),this.setAnimationLoop=function(X){Y=X},this.dispose=function(){}}}const jn=new Mt,Am=new st;function wm(n,e){function t(p,d){p.matrixAutoUpdate===!0&&p.updateMatrix(),d.value.copy(p.matrix)}function i(p,d){d.color.getRGB(p.fogColor.value,Gc(n)),d.isFog?(p.fogNear.value=d.near,p.fogFar.value=d.far):d.isFogExp2&&(p.fogDensity.value=d.density)}function a(p,d,E,S,x){d.isMeshBasicMaterial||d.isMeshLambertMaterial?r(p,d):d.isMeshToonMaterial?(r(p,d),h(p,d)):d.isMeshPhongMaterial?(r(p,d),u(p,d)):d.isMeshStandardMaterial?(r(p,d),f(p,d),d.isMeshPhysicalMaterial&&m(p,d,x)):d.isMeshMatcapMaterial?(r(p,d),g(p,d)):d.isMeshDepthMaterial?r(p,d):d.isMeshDistanceMaterial?(r(p,d),_(p,d)):d.isMeshNormalMaterial?r(p,d):d.isLineBasicMaterial?(s(p,d),d.isLineDashedMaterial&&o(p,d)):d.isPointsMaterial?c(p,d,E,S):d.isSpriteMaterial?l(p,d):d.isShadowMaterial?(p.color.value.copy(d.color),p.opacity.value=d.opacity):d.isShaderMaterial&&(d.uniformsNeedUpdate=!1)}function r(p,d){p.opacity.value=d.opacity,d.color&&p.diffuse.value.copy(d.color),d.emissive&&p.emissive.value.copy(d.emissive).multiplyScalar(d.emissiveIntensity),d.map&&(p.map.value=d.map,t(d.map,p.mapTransform)),d.alphaMap&&(p.alphaMap.value=d.alphaMap,t(d.alphaMap,p.alphaMapTransform)),d.bumpMap&&(p.bumpMap.value=d.bumpMap,t(d.bumpMap,p.bumpMapTransform),p.bumpScale.value=d.bumpScale,d.side===Lt&&(p.bumpScale.value*=-1)),d.normalMap&&(p.normalMap.value=d.normalMap,t(d.normalMap,p.normalMapTransform),p.normalScale.value.copy(d.normalScale),d.side===Lt&&p.normalScale.value.negate()),d.displacementMap&&(p.displacementMap.value=d.displacementMap,t(d.displacementMap,p.displacementMapTransform),p.displacementScale.value=d.displacementScale,p.displacementBias.value=d.displacementBias),d.emissiveMap&&(p.emissiveMap.value=d.emissiveMap,t(d.emissiveMap,p.emissiveMapTransform)),d.specularMap&&(p.specularMap.value=d.specularMap,t(d.specularMap,p.specularMapTransform)),d.alphaTest>0&&(p.alphaTest.value=d.alphaTest);const E=e.get(d),S=E.envMap,x=E.envMapRotation;S&&(p.envMap.value=S,jn.copy(x),jn.x*=-1,jn.y*=-1,jn.z*=-1,S.isCubeTexture&&S.isRenderTargetTexture===!1&&(jn.y*=-1,jn.z*=-1),p.envMapRotation.value.setFromMatrix4(Am.makeRotationFromEuler(jn)),p.flipEnvMap.value=S.isCubeTexture&&S.isRenderTargetTexture===!1?-1:1,p.reflectivity.value=d.reflectivity,p.ior.value=d.ior,p.refractionRatio.value=d.refractionRatio),d.lightMap&&(p.lightMap.value=d.lightMap,p.lightMapIntensity.value=d.lightMapIntensity,t(d.lightMap,p.lightMapTransform)),d.aoMap&&(p.aoMap.value=d.aoMap,p.aoMapIntensity.value=d.aoMapIntensity,t(d.aoMap,p.aoMapTransform))}function s(p,d){p.diffuse.value.copy(d.color),p.opacity.value=d.opacity,d.map&&(p.map.value=d.map,t(d.map,p.mapTransform))}function o(p,d){p.dashSize.value=d.dashSize,p.totalSize.value=d.dashSize+d.gapSize,p.scale.value=d.scale}function c(p,d,E,S){p.diffuse.value.copy(d.color),p.opacity.value=d.opacity,p.size.value=d.size*E,p.scale.value=S*.5,d.map&&(p.map.value=d.map,t(d.map,p.uvTransform)),d.alphaMap&&(p.alphaMap.value=d.alphaMap,t(d.alphaMap,p.alphaMapTransform)),d.alphaTest>0&&(p.alphaTest.value=d.alphaTest)}function l(p,d){p.diffuse.value.copy(d.color),p.opacity.value=d.opacity,p.rotation.value=d.rotation,d.map&&(p.map.value=d.map,t(d.map,p.mapTransform)),d.alphaMap&&(p.alphaMap.value=d.alphaMap,t(d.alphaMap,p.alphaMapTransform)),d.alphaTest>0&&(p.alphaTest.value=d.alphaTest)}function u(p,d){p.specular.value.copy(d.specular),p.shininess.value=Math.max(d.shininess,1e-4)}function h(p,d){d.gradientMap&&(p.gradientMap.value=d.gradientMap)}function f(p,d){p.metalness.value=d.metalness,d.metalnessMap&&(p.metalnessMap.value=d.metalnessMap,t(d.metalnessMap,p.metalnessMapTransform)),p.roughness.value=d.roughness,d.roughnessMap&&(p.roughnessMap.value=d.roughnessMap,t(d.roughnessMap,p.roughnessMapTransform)),d.envMap&&(p.envMapIntensity.value=d.envMapIntensity)}function m(p,d,E){p.ior.value=d.ior,d.sheen>0&&(p.sheenColor.value.copy(d.sheenColor).multiplyScalar(d.sheen),p.sheenRoughness.value=d.sheenRoughness,d.sheenColorMap&&(p.sheenColorMap.value=d.sheenColorMap,t(d.sheenColorMap,p.sheenColorMapTransform)),d.sheenRoughnessMap&&(p.sheenRoughnessMap.value=d.sheenRoughnessMap,t(d.sheenRoughnessMap,p.sheenRoughnessMapTransform))),d.clearcoat>0&&(p.clearcoat.value=d.clearcoat,p.clearcoatRoughness.value=d.clearcoatRoughness,d.clearcoatMap&&(p.clearcoatMap.value=d.clearcoatMap,t(d.clearcoatMap,p.clearcoatMapTransform)),d.clearcoatRoughnessMap&&(p.clearcoatRoughnessMap.value=d.clearcoatRoughnessMap,t(d.clearcoatRoughnessMap,p.clearcoatRoughnessMapTransform)),d.clearcoatNormalMap&&(p.clearcoatNormalMap.value=d.clearcoatNormalMap,t(d.clearcoatNormalMap,p.clearcoatNormalMapTransform),p.clearcoatNormalScale.value.copy(d.clearcoatNormalScale),d.side===Lt&&p.clearcoatNormalScale.value.negate())),d.dispersion>0&&(p.dispersion.value=d.dispersion),d.iridescence>0&&(p.iridescence.value=d.iridescence,p.iridescenceIOR.value=d.iridescenceIOR,p.iridescenceThicknessMinimum.value=d.iridescenceThicknessRange[0],p.iridescenceThicknessMaximum.value=d.iridescenceThicknessRange[1],d.iridescenceMap&&(p.iridescenceMap.value=d.iridescenceMap,t(d.iridescenceMap,p.iridescenceMapTransform)),d.iridescenceThicknessMap&&(p.iridescenceThicknessMap.value=d.iridescenceThicknessMap,t(d.iridescenceThicknessMap,p.iridescenceThicknessMapTransform))),d.transmission>0&&(p.transmission.value=d.transmission,p.transmissionSamplerMap.value=E.texture,p.transmissionSamplerSize.value.set(E.width,E.height),d.transmissionMap&&(p.transmissionMap.value=d.transmissionMap,t(d.transmissionMap,p.transmissionMapTransform)),p.thickness.value=d.thickness,d.thicknessMap&&(p.thicknessMap.value=d.thicknessMap,t(d.thicknessMap,p.thicknessMapTransform)),p.attenuationDistance.value=d.attenuationDistance,p.attenuationColor.value.copy(d.attenuationColor)),d.anisotropy>0&&(p.anisotropyVector.value.set(d.anisotropy*Math.cos(d.anisotropyRotation),d.anisotropy*Math.sin(d.anisotropyRotation)),d.anisotropyMap&&(p.anisotropyMap.value=d.anisotropyMap,t(d.anisotropyMap,p.anisotropyMapTransform))),p.specularIntensity.value=d.specularIntensity,p.specularColor.value.copy(d.specularColor),d.specularColorMap&&(p.specularColorMap.value=d.specularColorMap,t(d.specularColorMap,p.specularColorMapTransform)),d.specularIntensityMap&&(p.specularIntensityMap.value=d.specularIntensityMap,t(d.specularIntensityMap,p.specularIntensityMapTransform))}function g(p,d){d.matcap&&(p.matcap.value=d.matcap)}function _(p,d){const E=e.get(d).light;p.referencePosition.value.setFromMatrixPosition(E.matrixWorld),p.nearDistance.value=E.shadow.camera.near,p.farDistance.value=E.shadow.camera.far}return{refreshFogUniforms:i,refreshMaterialUniforms:a}}function Rm(n,e,t,i){let a={},r={},s=[];const o=n.getParameter(n.MAX_UNIFORM_BUFFER_BINDINGS);function c(E,S){const x=S.program;i.uniformBlockBinding(E,x)}function l(E,S){let x=a[E.id];x===void 0&&(g(E),x=u(E),a[E.id]=x,E.addEventListener("dispose",p));const T=S.program;i.updateUBOMapping(E,T);const y=e.render.frame;r[E.id]!==y&&(f(E),r[E.id]=y)}function u(E){const S=h();E.__bindingPointIndex=S;const x=n.createBuffer(),T=E.__size,y=E.usage;return n.bindBuffer(n.UNIFORM_BUFFER,x),n.bufferData(n.UNIFORM_BUFFER,T,y),n.bindBuffer(n.UNIFORM_BUFFER,null),n.bindBufferBase(n.UNIFORM_BUFFER,S,x),x}function h(){for(let E=0;E<o;E++)if(s.indexOf(E)===-1)return s.push(E),E;return console.error("THREE.WebGLRenderer: Maximum number of simultaneously usable uniforms groups reached."),0}function f(E){const S=a[E.id],x=E.uniforms,T=E.__cache;n.bindBuffer(n.UNIFORM_BUFFER,S);for(let y=0,w=x.length;y<w;y++){const D=Array.isArray(x[y])?x[y]:[x[y]];for(let M=0,v=D.length;M<v;M++){const R=D[M];if(m(R,y,M,T)===!0){const U=R.__offset,C=Array.isArray(R.value)?R.value:[R.value];let P=0;for(let N=0;N<C.length;N++){const k=C[N],O=_(k);typeof k=="number"||typeof k=="boolean"?(R.__data[0]=k,n.bufferSubData(n.UNIFORM_BUFFER,U+P,R.__data)):k.isMatrix3?(R.__data[0]=k.elements[0],R.__data[1]=k.elements[1],R.__data[2]=k.elements[2],R.__data[3]=0,R.__data[4]=k.elements[3],R.__data[5]=k.elements[4],R.__data[6]=k.elements[5],R.__data[7]=0,R.__data[8]=k.elements[6],R.__data[9]=k.elements[7],R.__data[10]=k.elements[8],R.__data[11]=0):(k.toArray(R.__data,P),P+=O.storage/Float32Array.BYTES_PER_ELEMENT)}n.bufferSubData(n.UNIFORM_BUFFER,U,R.__data)}}}n.bindBuffer(n.UNIFORM_BUFFER,null)}function m(E,S,x,T){const y=E.value,w=S+"_"+x;if(T[w]===void 0)return typeof y=="number"||typeof y=="boolean"?T[w]=y:T[w]=y.clone(),!0;{const D=T[w];if(typeof y=="number"||typeof y=="boolean"){if(D!==y)return T[w]=y,!0}else if(D.equals(y)===!1)return D.copy(y),!0}return!1}function g(E){const S=E.uniforms;let x=0;const T=16;for(let w=0,D=S.length;w<D;w++){const M=Array.isArray(S[w])?S[w]:[S[w]];for(let v=0,R=M.length;v<R;v++){const U=M[v],C=Array.isArray(U.value)?U.value:[U.value];for(let P=0,N=C.length;P<N;P++){const k=C[P],O=_(k),z=x%T,H=z%O.boundary,$=z+H;x+=H,$!==0&&T-$<O.storage&&(x+=T-$),U.__data=new Float32Array(O.storage/Float32Array.BYTES_PER_ELEMENT),U.__offset=x,x+=O.storage}}}const y=x%T;return y>0&&(x+=T-y),E.__size=x,E.__cache={},this}function _(E){const S={boundary:0,storage:0};return typeof E=="number"||typeof E=="boolean"?(S.boundary=4,S.storage=4):E.isVector2?(S.boundary=8,S.storage=8):E.isVector3||E.isColor?(S.boundary=16,S.storage=12):E.isVector4?(S.boundary=16,S.storage=16):E.isMatrix3?(S.boundary=48,S.storage=48):E.isMatrix4?(S.boundary=64,S.storage=64):E.isTexture?console.warn("THREE.WebGLRenderer: Texture samplers can not be part of an uniforms group."):console.warn("THREE.WebGLRenderer: Unsupported uniform value type.",E),S}function p(E){const S=E.target;S.removeEventListener("dispose",p);const x=s.indexOf(S.__bindingPointIndex);s.splice(x,1),n.deleteBuffer(a[S.id]),delete a[S.id],delete r[S.id]}function d(){for(const E in a)n.deleteBuffer(a[E]);s=[],a={},r={}}return{bind:c,update:l,dispose:d}}class Cm{constructor(e={}){const{canvas:t=cu(),context:i=null,depth:a=!0,stencil:r=!1,alpha:s=!1,antialias:o=!1,premultipliedAlpha:c=!0,preserveDrawingBuffer:l=!1,powerPreference:u="default",failIfMajorPerformanceCaveat:h=!1,reverseDepthBuffer:f=!1}=e;this.isWebGLRenderer=!0;let m;if(i!==null){if(typeof WebGLRenderingContext<"u"&&i instanceof WebGLRenderingContext)throw new Error("THREE.WebGLRenderer: WebGL 1 is not supported since r163.");m=i.getContextAttributes().alpha}else m=s;const g=new Uint32Array(4),_=new Int32Array(4);let p=null,d=null;const E=[],S=[];this.domElement=t,this.debug={checkShaderErrors:!0,onShaderError:null},this.autoClear=!0,this.autoClearColor=!0,this.autoClearDepth=!0,this.autoClearStencil=!0,this.sortObjects=!0,this.clippingPlanes=[],this.localClippingEnabled=!1,this._outputColorSpace=Ft,this.toneMapping=Dn,this.toneMappingExposure=1;const x=this;let T=!1,y=0,w=0,D=null,M=-1,v=null;const R=new dt,U=new dt;let C=null;const P=new ce(0);let N=0,k=t.width,O=t.height,z=1,H=null,$=null;const Y=new dt(0,0,k,O),fe=new dt(0,0,k,O);let Ie=!1;const X=new Bs;let ne=!1,ue=!1;this.transmissionResolutionScale=1;const se=new st,ee=new st,_e=new F,de=new dt,Z={background:null,fog:null,environment:null,overrideMaterial:null,isScene:!0};let ae=!1;function re(){return D===null?z:1}let L=i;function Le(A,V){return t.getContext(A,V)}try{const A={alpha:!0,depth:a,stencil:r,antialias:o,premultipliedAlpha:c,preserveDrawingBuffer:l,powerPreference:u,failIfMajorPerformanceCaveat:h};if("setAttribute"in t&&t.setAttribute("data-engine",`three.js r${Ps}`),t.addEventListener("webglcontextlost",te,!1),t.addEventListener("webglcontextrestored",xe,!1),t.addEventListener("webglcontextcreationerror",ve,!1),L===null){const V="webgl2";if(L=Le(V,A),L===null)throw Le(V)?new Error("Error creating WebGL context with your selected attributes."):new Error("Error creating WebGL context.")}}catch(A){throw console.error("THREE.WebGLRenderer: "+A.message),A}let Ce,Re,Me,Fe,we,I,b,G,Q,ie,J,Ae,ge,Ee,Ye,le,be,Ue,ze,ye,qe,Ve,rt,B;function pe(){Ce=new Of(L),Ce.init(),Ve=new Sm(L,Ce),Re=new Df(L,Ce,e,Ve),Me=new xm(L,Ce),Re.reverseDepthBuffer&&f&&Me.buffers.depth.setReversed(!0),Fe=new jf(L),we=new sm,I=new Mm(L,Ce,Me,we,Re,Ve,Fe),b=new Uf(x),G=new Ff(x),Q=new Ku(L),rt=new Pf(L,Q),ie=new Bf(L,Q,Fe,rt),J=new Gf(L,ie,Q,Fe),ze=new Hf(L,Re,I),le=new Lf(we),Ae=new rm(x,b,G,Ce,Re,rt,le),ge=new wm(x,we),Ee=new cm,Ye=new pm(Ce),Ue=new Cf(x,b,G,Me,J,m,c),be=new _m(x,J,Re),B=new Rm(L,Fe,Re,Me),ye=new If(L,Ce,Fe),qe=new Vf(L,Ce,Fe),Fe.programs=Ae.programs,x.capabilities=Re,x.extensions=Ce,x.properties=we,x.renderLists=Ee,x.shadowMap=be,x.state=Me,x.info=Fe}pe();const q=new Tm(x,L);this.xr=q,this.getContext=function(){return L},this.getContextAttributes=function(){return L.getContextAttributes()},this.forceContextLoss=function(){const A=Ce.get("WEBGL_lose_context");A&&A.loseContext()},this.forceContextRestore=function(){const A=Ce.get("WEBGL_lose_context");A&&A.restoreContext()},this.getPixelRatio=function(){return z},this.setPixelRatio=function(A){A!==void 0&&(z=A,this.setSize(k,O,!1))},this.getSize=function(A){return A.set(k,O)},this.setSize=function(A,V,W=!0){if(q.isPresenting){console.warn("THREE.WebGLRenderer: Can't change size while VR device is presenting.");return}k=A,O=V,t.width=Math.floor(A*z),t.height=Math.floor(V*z),W===!0&&(t.style.width=A+"px",t.style.height=V+"px"),this.setViewport(0,0,A,V)},this.getDrawingBufferSize=function(A){return A.set(k*z,O*z).floor()},this.setDrawingBufferSize=function(A,V,W){k=A,O=V,z=W,t.width=Math.floor(A*W),t.height=Math.floor(V*W),this.setViewport(0,0,A,V)},this.getCurrentViewport=function(A){return A.copy(R)},this.getViewport=function(A){return A.copy(Y)},this.setViewport=function(A,V,W,K){A.isVector4?Y.set(A.x,A.y,A.z,A.w):Y.set(A,V,W,K),Me.viewport(R.copy(Y).multiplyScalar(z).round())},this.getScissor=function(A){return A.copy(fe)},this.setScissor=function(A,V,W,K){A.isVector4?fe.set(A.x,A.y,A.z,A.w):fe.set(A,V,W,K),Me.scissor(U.copy(fe).multiplyScalar(z).round())},this.getScissorTest=function(){return Ie},this.setScissorTest=function(A){Me.setScissorTest(Ie=A)},this.setOpaqueSort=function(A){H=A},this.setTransparentSort=function(A){$=A},this.getClearColor=function(A){return A.copy(Ue.getClearColor())},this.setClearColor=function(){Ue.setClearColor(...arguments)},this.getClearAlpha=function(){return Ue.getClearAlpha()},this.setClearAlpha=function(){Ue.setClearAlpha(...arguments)},this.clear=function(A=!0,V=!0,W=!0){let K=0;if(A){let j=!1;if(D!==null){const oe=D.texture.format;j=oe===ks||oe===zs||oe===Us}if(j){const oe=D.texture.type,me=oe===_n||oe===ei||oe===Ki||oe===Ri||oe===Ds||oe===Ls,Se=Ue.getClearColor(),Te=Ue.getClearAlpha(),ke=Se.r,Ne=Se.g,Pe=Se.b;me?(g[0]=ke,g[1]=Ne,g[2]=Pe,g[3]=Te,L.clearBufferuiv(L.COLOR,0,g)):(_[0]=ke,_[1]=Ne,_[2]=Pe,_[3]=Te,L.clearBufferiv(L.COLOR,0,_))}else K|=L.COLOR_BUFFER_BIT}V&&(K|=L.DEPTH_BUFFER_BIT),W&&(K|=L.STENCIL_BUFFER_BIT,this.state.buffers.stencil.setMask(4294967295)),L.clear(K)},this.clearColor=function(){this.clear(!0,!1,!1)},this.clearDepth=function(){this.clear(!1,!0,!1)},this.clearStencil=function(){this.clear(!1,!1,!0)},this.dispose=function(){t.removeEventListener("webglcontextlost",te,!1),t.removeEventListener("webglcontextrestored",xe,!1),t.removeEventListener("webglcontextcreationerror",ve,!1),Ue.dispose(),Ee.dispose(),Ye.dispose(),we.dispose(),b.dispose(),G.dispose(),J.dispose(),rt.dispose(),B.dispose(),Ae.dispose(),q.dispose(),q.removeEventListener("sessionstart",qs),q.removeEventListener("sessionend",$s),zn.stop()};function te(A){A.preventDefault(),console.log("THREE.WebGLRenderer: Context Lost."),T=!0}function xe(){console.log("THREE.WebGLRenderer: Context Restored."),T=!1;const A=Fe.autoReset,V=be.enabled,W=be.autoUpdate,K=be.needsUpdate,j=be.type;pe(),Fe.autoReset=A,be.enabled=V,be.autoUpdate=W,be.needsUpdate=K,be.type=j}function ve(A){console.error("THREE.WebGLRenderer: A WebGL context could not be created. Reason: ",A.statusMessage)}function Oe(A){const V=A.target;V.removeEventListener("dispose",Oe),lt(V)}function lt(A){bt(A),we.remove(A)}function bt(A){const V=we.get(A).programs;V!==void 0&&(V.forEach(function(W){Ae.releaseProgram(W)}),A.isShaderMaterial&&Ae.releaseShaderCache(A))}this.renderBufferDirect=function(A,V,W,K,j,oe){V===null&&(V=Z);const me=j.isMesh&&j.matrixWorld.determinant()<0,Se=sl(A,V,W,K,j);Me.setMaterial(K,me);let Te=W.index,ke=1;if(K.wireframe===!0){if(Te=ie.getWireframeAttribute(W),Te===void 0)return;ke=2}const Ne=W.drawRange,Pe=W.attributes.position;let Ze=Ne.start*ke,et=(Ne.start+Ne.count)*ke;oe!==null&&(Ze=Math.max(Ze,oe.start*ke),et=Math.min(et,(oe.start+oe.count)*ke)),Te!==null?(Ze=Math.max(Ze,0),et=Math.min(et,Te.count)):Pe!=null&&(Ze=Math.max(Ze,0),et=Math.min(et,Pe.count));const ft=et-Ze;if(ft<0||ft===1/0)return;rt.setup(j,K,Se,W,Te);let ut,Je=ye;if(Te!==null&&(ut=Q.get(Te),Je=qe,Je.setIndex(ut)),j.isMesh)K.wireframe===!0?(Me.setLineWidth(K.wireframeLinewidth*re()),Je.setMode(L.LINES)):Je.setMode(L.TRIANGLES);else if(j.isLine){let De=K.linewidth;De===void 0&&(De=1),Me.setLineWidth(De*re()),j.isLineSegments?Je.setMode(L.LINES):j.isLineLoop?Je.setMode(L.LINE_LOOP):Je.setMode(L.LINE_STRIP)}else j.isPoints?Je.setMode(L.POINTS):j.isSprite&&Je.setMode(L.TRIANGLES);if(j.isBatchedMesh)if(j._multiDrawInstances!==null)Hn("THREE.WebGLRenderer: renderMultiDrawInstances has been deprecated and will be removed in r184. Append to renderMultiDraw arguments and use indirection."),Je.renderMultiDrawInstances(j._multiDrawStarts,j._multiDrawCounts,j._multiDrawCount,j._multiDrawInstances);else if(Ce.get("WEBGL_multi_draw"))Je.renderMultiDraw(j._multiDrawStarts,j._multiDrawCounts,j._multiDrawCount);else{const De=j._multiDrawStarts,St=j._multiDrawCounts,tt=j._multiDrawCount,Xt=Te?Q.get(Te).bytesPerElement:1,ni=we.get(K).currentProgram.getUniforms();for(let zt=0;zt<tt;zt++)ni.setValue(L,"_gl_DrawID",zt),Je.render(De[zt]/Xt,St[zt])}else if(j.isInstancedMesh)Je.renderInstances(Ze,ft,j.count);else if(W.isInstancedBufferGeometry){const De=W._maxInstanceCount!==void 0?W._maxInstanceCount:1/0,St=Math.min(W.instanceCount,De);Je.renderInstances(Ze,ft,St)}else Je.render(Ze,ft)};function nt(A,V,W){A.transparent===!0&&A.side===mt&&A.forceSinglePass===!1?(A.side=Lt,A.needsUpdate=!0,na(A,V,W),A.side=Ln,A.needsUpdate=!0,na(A,V,W),A.side=mt):na(A,V,W)}this.compile=function(A,V,W=null){W===null&&(W=A),d=Ye.get(W),d.init(V),S.push(d),W.traverseVisible(function(j){j.isLight&&j.layers.test(V.layers)&&(d.pushLight(j),j.castShadow&&d.pushShadow(j))}),A!==W&&A.traverseVisible(function(j){j.isLight&&j.layers.test(V.layers)&&(d.pushLight(j),j.castShadow&&d.pushShadow(j))}),d.setupLights();const K=new Set;return A.traverse(function(j){if(!(j.isMesh||j.isPoints||j.isLine||j.isSprite))return;const oe=j.material;if(oe)if(Array.isArray(oe))for(let me=0;me<oe.length;me++){const Se=oe[me];nt(Se,W,j),K.add(Se)}else nt(oe,W,j),K.add(oe)}),d=S.pop(),K},this.compileAsync=function(A,V,W=null){const K=this.compile(A,V,W);return new Promise(j=>{function oe(){if(K.forEach(function(me){we.get(me).currentProgram.isReady()&&K.delete(me)}),K.size===0){j(A);return}setTimeout(oe,10)}Ce.get("KHR_parallel_shader_compile")!==null?oe():setTimeout(oe,10)})};let Wt=null;function nn(A){Wt&&Wt(A)}function qs(){zn.stop()}function $s(){zn.start()}const zn=new Yc;zn.setAnimationLoop(nn),typeof self<"u"&&zn.setContext(self),this.setAnimationLoop=function(A){Wt=A,q.setAnimationLoop(A),A===null?zn.stop():zn.start()},q.addEventListener("sessionstart",qs),q.addEventListener("sessionend",$s),this.render=function(A,V){if(V!==void 0&&V.isCamera!==!0){console.error("THREE.WebGLRenderer.render: camera is not an instance of THREE.Camera.");return}if(T===!0)return;if(A.matrixWorldAutoUpdate===!0&&A.updateMatrixWorld(),V.parent===null&&V.matrixWorldAutoUpdate===!0&&V.updateMatrixWorld(),q.enabled===!0&&q.isPresenting===!0&&(q.cameraAutoUpdate===!0&&q.updateCamera(V),V=q.getCamera()),A.isScene===!0&&A.onBeforeRender(x,A,V,D),d=Ye.get(A,S.length),d.init(V),S.push(d),ee.multiplyMatrices(V.projectionMatrix,V.matrixWorldInverse),X.setFromProjectionMatrix(ee),ue=this.localClippingEnabled,ne=le.init(this.clippingPlanes,ue),p=Ee.get(A,E.length),p.init(),E.push(p),q.enabled===!0&&q.isPresenting===!0){const oe=x.xr.getDepthSensingMesh();oe!==null&&Ka(oe,V,-1/0,x.sortObjects)}Ka(A,V,0,x.sortObjects),p.finish(),x.sortObjects===!0&&p.sort(H,$),ae=q.enabled===!1||q.isPresenting===!1||q.hasDepthSensing()===!1,ae&&Ue.addToRenderList(p,A),this.info.render.frame++,ne===!0&&le.beginShadows();const W=d.state.shadowsArray;be.render(W,A,V),ne===!0&&le.endShadows(),this.info.autoReset===!0&&this.info.reset();const K=p.opaque,j=p.transmissive;if(d.setupLights(),V.isArrayCamera){const oe=V.cameras;if(j.length>0)for(let me=0,Se=oe.length;me<Se;me++){const Te=oe[me];Zs(K,j,A,Te)}ae&&Ue.render(A);for(let me=0,Se=oe.length;me<Se;me++){const Te=oe[me];Ys(p,A,Te,Te.viewport)}}else j.length>0&&Zs(K,j,A,V),ae&&Ue.render(A),Ys(p,A,V);D!==null&&w===0&&(I.updateMultisampleRenderTarget(D),I.updateRenderTargetMipmap(D)),A.isScene===!0&&A.onAfterRender(x,A,V),rt.resetDefaultState(),M=-1,v=null,S.pop(),S.length>0?(d=S[S.length-1],ne===!0&&le.setGlobalState(x.clippingPlanes,d.state.camera)):d=null,E.pop(),E.length>0?p=E[E.length-1]:p=null};function Ka(A,V,W,K){if(A.visible===!1)return;if(A.layers.test(V.layers)){if(A.isGroup)W=A.renderOrder;else if(A.isLOD)A.autoUpdate===!0&&A.update(V);else if(A.isLight)d.pushLight(A),A.castShadow&&d.pushShadow(A);else if(A.isSprite){if(!A.frustumCulled||X.intersectsSprite(A)){K&&de.setFromMatrixPosition(A.matrixWorld).applyMatrix4(ee);const me=J.update(A),Se=A.material;Se.visible&&p.push(A,me,Se,W,de.z,null)}}else if((A.isMesh||A.isLine||A.isPoints)&&(!A.frustumCulled||X.intersectsObject(A))){const me=J.update(A),Se=A.material;if(K&&(A.boundingSphere!==void 0?(A.boundingSphere===null&&A.computeBoundingSphere(),de.copy(A.boundingSphere.center)):(me.boundingSphere===null&&me.computeBoundingSphere(),de.copy(me.boundingSphere.center)),de.applyMatrix4(A.matrixWorld).applyMatrix4(ee)),Array.isArray(Se)){const Te=me.groups;for(let ke=0,Ne=Te.length;ke<Ne;ke++){const Pe=Te[ke],Ze=Se[Pe.materialIndex];Ze&&Ze.visible&&p.push(A,me,Ze,W,de.z,Pe)}}else Se.visible&&p.push(A,me,Se,W,de.z,null)}}const oe=A.children;for(let me=0,Se=oe.length;me<Se;me++)Ka(oe[me],V,W,K)}function Ys(A,V,W,K){const j=A.opaque,oe=A.transmissive,me=A.transparent;d.setupLightsView(W),ne===!0&&le.setGlobalState(x.clippingPlanes,W),K&&Me.viewport(R.copy(K)),j.length>0&&ta(j,V,W),oe.length>0&&ta(oe,V,W),me.length>0&&ta(me,V,W),Me.buffers.depth.setTest(!0),Me.buffers.depth.setMask(!0),Me.buffers.color.setMask(!0),Me.setPolygonOffset(!1)}function Zs(A,V,W,K){if((W.isScene===!0?W.overrideMaterial:null)!==null)return;d.state.transmissionRenderTarget[K.id]===void 0&&(d.state.transmissionRenderTarget[K.id]=new ti(1,1,{generateMipmaps:!0,type:Ce.has("EXT_color_buffer_half_float")||Ce.has("EXT_color_buffer_float")?Yi:_n,minFilter:Zn,samples:4,stencilBuffer:r,resolveDepthBuffer:!1,resolveStencilBuffer:!1,colorSpace:Qe.workingColorSpace}));const oe=d.state.transmissionRenderTarget[K.id],me=K.viewport||R;oe.setSize(me.z*x.transmissionResolutionScale,me.w*x.transmissionResolutionScale);const Se=x.getRenderTarget();x.setRenderTarget(oe),x.getClearColor(P),N=x.getClearAlpha(),N<1&&x.setClearColor(16777215,.5),x.clear(),ae&&Ue.render(W);const Te=x.toneMapping;x.toneMapping=Dn;const ke=K.viewport;if(K.viewport!==void 0&&(K.viewport=void 0),d.setupLightsView(K),ne===!0&&le.setGlobalState(x.clippingPlanes,K),ta(A,W,K),I.updateMultisampleRenderTarget(oe),I.updateRenderTargetMipmap(oe),Ce.has("WEBGL_multisampled_render_to_texture")===!1){let Ne=!1;for(let Pe=0,Ze=V.length;Pe<Ze;Pe++){const et=V[Pe],ft=et.object,ut=et.geometry,Je=et.material,De=et.group;if(Je.side===mt&&ft.layers.test(K.layers)){const St=Je.side;Je.side=Lt,Je.needsUpdate=!0,Js(ft,W,K,ut,Je,De),Je.side=St,Je.needsUpdate=!0,Ne=!0}}Ne===!0&&(I.updateMultisampleRenderTarget(oe),I.updateRenderTargetMipmap(oe))}x.setRenderTarget(Se),x.setClearColor(P,N),ke!==void 0&&(K.viewport=ke),x.toneMapping=Te}function ta(A,V,W){const K=V.isScene===!0?V.overrideMaterial:null;for(let j=0,oe=A.length;j<oe;j++){const me=A[j],Se=me.object,Te=me.geometry,ke=K===null?me.material:K,Ne=me.group;Se.layers.test(W.layers)&&Js(Se,V,W,Te,ke,Ne)}}function Js(A,V,W,K,j,oe){A.onBeforeRender(x,V,W,K,j,oe),A.modelViewMatrix.multiplyMatrices(W.matrixWorldInverse,A.matrixWorld),A.normalMatrix.getNormalMatrix(A.modelViewMatrix),j.onBeforeRender(x,V,W,K,A,oe),j.transparent===!0&&j.side===mt&&j.forceSinglePass===!1?(j.side=Lt,j.needsUpdate=!0,x.renderBufferDirect(W,V,K,j,A,oe),j.side=Ln,j.needsUpdate=!0,x.renderBufferDirect(W,V,K,j,A,oe),j.side=mt):x.renderBufferDirect(W,V,K,j,A,oe),A.onAfterRender(x,V,W,K,j,oe)}function na(A,V,W){V.isScene!==!0&&(V=Z);const K=we.get(A),j=d.state.lights,oe=d.state.shadowsArray,me=j.state.version,Se=Ae.getParameters(A,j.state,oe,V,W),Te=Ae.getProgramCacheKey(Se);let ke=K.programs;K.environment=A.isMeshStandardMaterial?V.environment:null,K.fog=V.fog,K.envMap=(A.isMeshStandardMaterial?G:b).get(A.envMap||K.environment),K.envMapRotation=K.environment!==null&&A.envMap===null?V.environmentRotation:A.envMapRotation,ke===void 0&&(A.addEventListener("dispose",Oe),ke=new Map,K.programs=ke);let Ne=ke.get(Te);if(Ne!==void 0){if(K.currentProgram===Ne&&K.lightsStateVersion===me)return eo(A,Se),Ne}else Se.uniforms=Ae.getUniforms(A),A.onBeforeCompile(Se,x),Ne=Ae.acquireProgram(Se,Te),ke.set(Te,Ne),K.uniforms=Se.uniforms;const Pe=K.uniforms;return(!A.isShaderMaterial&&!A.isRawShaderMaterial||A.clipping===!0)&&(Pe.clippingPlanes=le.uniform),eo(A,Se),K.needsLights=cl(A),K.lightsStateVersion=me,K.needsLights&&(Pe.ambientLightColor.value=j.state.ambient,Pe.lightProbe.value=j.state.probe,Pe.directionalLights.value=j.state.directional,Pe.directionalLightShadows.value=j.state.directionalShadow,Pe.spotLights.value=j.state.spot,Pe.spotLightShadows.value=j.state.spotShadow,Pe.rectAreaLights.value=j.state.rectArea,Pe.ltc_1.value=j.state.rectAreaLTC1,Pe.ltc_2.value=j.state.rectAreaLTC2,Pe.pointLights.value=j.state.point,Pe.pointLightShadows.value=j.state.pointShadow,Pe.hemisphereLights.value=j.state.hemi,Pe.directionalShadowMap.value=j.state.directionalShadowMap,Pe.directionalShadowMatrix.value=j.state.directionalShadowMatrix,Pe.spotShadowMap.value=j.state.spotShadowMap,Pe.spotLightMatrix.value=j.state.spotLightMatrix,Pe.spotLightMap.value=j.state.spotLightMap,Pe.pointShadowMap.value=j.state.pointShadowMap,Pe.pointShadowMatrix.value=j.state.pointShadowMatrix),K.currentProgram=Ne,K.uniformsList=null,Ne}function Qs(A){if(A.uniformsList===null){const V=A.currentProgram.getUniforms();A.uniformsList=ka.seqWithValue(V.seq,A.uniforms)}return A.uniformsList}function eo(A,V){const W=we.get(A);W.outputColorSpace=V.outputColorSpace,W.batching=V.batching,W.batchingColor=V.batchingColor,W.instancing=V.instancing,W.instancingColor=V.instancingColor,W.instancingMorph=V.instancingMorph,W.skinning=V.skinning,W.morphTargets=V.morphTargets,W.morphNormals=V.morphNormals,W.morphColors=V.morphColors,W.morphTargetsCount=V.morphTargetsCount,W.numClippingPlanes=V.numClippingPlanes,W.numIntersection=V.numClipIntersection,W.vertexAlphas=V.vertexAlphas,W.vertexTangents=V.vertexTangents,W.toneMapping=V.toneMapping}function sl(A,V,W,K,j){V.isScene!==!0&&(V=Z),I.resetTextureUnits();const oe=V.fog,me=K.isMeshStandardMaterial?V.environment:null,Se=D===null?x.outputColorSpace:D.isXRRenderTarget===!0?D.texture.colorSpace:Pi,Te=(K.isMeshStandardMaterial?G:b).get(K.envMap||me),ke=K.vertexColors===!0&&!!W.attributes.color&&W.attributes.color.itemSize===4,Ne=!!W.attributes.tangent&&(!!K.normalMap||K.anisotropy>0),Pe=!!W.morphAttributes.position,Ze=!!W.morphAttributes.normal,et=!!W.morphAttributes.color;let ft=Dn;K.toneMapped&&(D===null||D.isXRRenderTarget===!0)&&(ft=x.toneMapping);const ut=W.morphAttributes.position||W.morphAttributes.normal||W.morphAttributes.color,Je=ut!==void 0?ut.length:0,De=we.get(K),St=d.state.lights;if(ne===!0&&(ue===!0||A!==v)){const At=A===v&&K.id===M;le.setState(K,A,At)}let tt=!1;K.version===De.__version?(De.needsLights&&De.lightsStateVersion!==St.state.version||De.outputColorSpace!==Se||j.isBatchedMesh&&De.batching===!1||!j.isBatchedMesh&&De.batching===!0||j.isBatchedMesh&&De.batchingColor===!0&&j.colorTexture===null||j.isBatchedMesh&&De.batchingColor===!1&&j.colorTexture!==null||j.isInstancedMesh&&De.instancing===!1||!j.isInstancedMesh&&De.instancing===!0||j.isSkinnedMesh&&De.skinning===!1||!j.isSkinnedMesh&&De.skinning===!0||j.isInstancedMesh&&De.instancingColor===!0&&j.instanceColor===null||j.isInstancedMesh&&De.instancingColor===!1&&j.instanceColor!==null||j.isInstancedMesh&&De.instancingMorph===!0&&j.morphTexture===null||j.isInstancedMesh&&De.instancingMorph===!1&&j.morphTexture!==null||De.envMap!==Te||K.fog===!0&&De.fog!==oe||De.numClippingPlanes!==void 0&&(De.numClippingPlanes!==le.numPlanes||De.numIntersection!==le.numIntersection)||De.vertexAlphas!==ke||De.vertexTangents!==Ne||De.morphTargets!==Pe||De.morphNormals!==Ze||De.morphColors!==et||De.toneMapping!==ft||De.morphTargetsCount!==Je)&&(tt=!0):(tt=!0,De.__version=K.version);let Xt=De.currentProgram;tt===!0&&(Xt=na(K,V,j));let ni=!1,zt=!1,Ni=!1;const ot=Xt.getUniforms(),Bt=De.uniforms;if(Me.useProgram(Xt.program)&&(ni=!0,zt=!0,Ni=!0),K.id!==M&&(M=K.id,zt=!0),ni||v!==A){Me.buffers.depth.getReversed()?(se.copy(A.projectionMatrix),uu(se),du(se),ot.setValue(L,"projectionMatrix",se)):ot.setValue(L,"projectionMatrix",A.projectionMatrix),ot.setValue(L,"viewMatrix",A.matrixWorldInverse);const Pt=ot.map.cameraPosition;Pt!==void 0&&Pt.setValue(L,_e.setFromMatrixPosition(A.matrixWorld)),Re.logarithmicDepthBuffer&&ot.setValue(L,"logDepthBufFC",2/(Math.log(A.far+1)/Math.LN2)),(K.isMeshPhongMaterial||K.isMeshToonMaterial||K.isMeshLambertMaterial||K.isMeshBasicMaterial||K.isMeshStandardMaterial||K.isShaderMaterial)&&ot.setValue(L,"isOrthographic",A.isOrthographicCamera===!0),v!==A&&(v=A,zt=!0,Ni=!0)}if(j.isSkinnedMesh){ot.setOptional(L,j,"bindMatrix"),ot.setOptional(L,j,"bindMatrixInverse");const At=j.skeleton;At&&(At.boneTexture===null&&At.computeBoneTexture(),ot.setValue(L,"boneTexture",At.boneTexture,I))}j.isBatchedMesh&&(ot.setOptional(L,j,"batchingTexture"),ot.setValue(L,"batchingTexture",j._matricesTexture,I),ot.setOptional(L,j,"batchingIdTexture"),ot.setValue(L,"batchingIdTexture",j._indirectTexture,I),ot.setOptional(L,j,"batchingColorTexture"),j._colorsTexture!==null&&ot.setValue(L,"batchingColorTexture",j._colorsTexture,I));const Vt=W.morphAttributes;if((Vt.position!==void 0||Vt.normal!==void 0||Vt.color!==void 0)&&ze.update(j,W,Xt),(zt||De.receiveShadow!==j.receiveShadow)&&(De.receiveShadow=j.receiveShadow,ot.setValue(L,"receiveShadow",j.receiveShadow)),K.isMeshGouraudMaterial&&K.envMap!==null&&(Bt.envMap.value=Te,Bt.flipEnvMap.value=Te.isCubeTexture&&Te.isRenderTargetTexture===!1?-1:1),K.isMeshStandardMaterial&&K.envMap===null&&V.environment!==null&&(Bt.envMapIntensity.value=V.environmentIntensity),zt&&(ot.setValue(L,"toneMappingExposure",x.toneMappingExposure),De.needsLights&&ol(Bt,Ni),oe&&K.fog===!0&&ge.refreshFogUniforms(Bt,oe),ge.refreshMaterialUniforms(Bt,K,z,O,d.state.transmissionRenderTarget[A.id]),ka.upload(L,Qs(De),Bt,I)),K.isShaderMaterial&&K.uniformsNeedUpdate===!0&&(ka.upload(L,Qs(De),Bt,I),K.uniformsNeedUpdate=!1),K.isSpriteMaterial&&ot.setValue(L,"center",j.center),ot.setValue(L,"modelViewMatrix",j.modelViewMatrix),ot.setValue(L,"normalMatrix",j.normalMatrix),ot.setValue(L,"modelMatrix",j.matrixWorld),K.isShaderMaterial||K.isRawShaderMaterial){const At=K.uniformsGroups;for(let Pt=0,qa=At.length;Pt<qa;Pt++){const kn=At[Pt];B.update(kn,Xt),B.bind(kn,Xt)}}return Xt}function ol(A,V){A.ambientLightColor.needsUpdate=V,A.lightProbe.needsUpdate=V,A.directionalLights.needsUpdate=V,A.directionalLightShadows.needsUpdate=V,A.pointLights.needsUpdate=V,A.pointLightShadows.needsUpdate=V,A.spotLights.needsUpdate=V,A.spotLightShadows.needsUpdate=V,A.rectAreaLights.needsUpdate=V,A.hemisphereLights.needsUpdate=V}function cl(A){return A.isMeshLambertMaterial||A.isMeshToonMaterial||A.isMeshPhongMaterial||A.isMeshStandardMaterial||A.isShadowMaterial||A.isShaderMaterial&&A.lights===!0}this.getActiveCubeFace=function(){return y},this.getActiveMipmapLevel=function(){return w},this.getRenderTarget=function(){return D},this.setRenderTargetTextures=function(A,V,W){we.get(A.texture).__webglTexture=V,we.get(A.depthTexture).__webglTexture=W;const K=we.get(A);K.__hasExternalTextures=!0,K.__autoAllocateDepthBuffer=W===void 0,K.__autoAllocateDepthBuffer||Ce.has("WEBGL_multisampled_render_to_texture")===!0&&(console.warn("THREE.WebGLRenderer: Render-to-texture extension was disabled because an external texture was provided"),K.__useRenderToTexture=!1)},this.setRenderTargetFramebuffer=function(A,V){const W=we.get(A);W.__webglFramebuffer=V,W.__useDefaultFramebuffer=V===void 0};const ll=L.createFramebuffer();this.setRenderTarget=function(A,V=0,W=0){D=A,y=V,w=W;let K=!0,j=null,oe=!1,me=!1;if(A){const Te=we.get(A);if(Te.__useDefaultFramebuffer!==void 0)Me.bindFramebuffer(L.FRAMEBUFFER,null),K=!1;else if(Te.__webglFramebuffer===void 0)I.setupRenderTarget(A);else if(Te.__hasExternalTextures)I.rebindTextures(A,we.get(A.texture).__webglTexture,we.get(A.depthTexture).__webglTexture);else if(A.depthBuffer){const Pe=A.depthTexture;if(Te.__boundDepthTexture!==Pe){if(Pe!==null&&we.has(Pe)&&(A.width!==Pe.image.width||A.height!==Pe.image.height))throw new Error("WebGLRenderTarget: Attached DepthTexture is initialized to the incorrect size.");I.setupDepthRenderbuffer(A)}}const ke=A.texture;(ke.isData3DTexture||ke.isDataArrayTexture||ke.isCompressedArrayTexture)&&(me=!0);const Ne=we.get(A).__webglFramebuffer;A.isWebGLCubeRenderTarget?(Array.isArray(Ne[V])?j=Ne[V][W]:j=Ne[V],oe=!0):A.samples>0&&I.useMultisampledRTT(A)===!1?j=we.get(A).__webglMultisampledFramebuffer:Array.isArray(Ne)?j=Ne[W]:j=Ne,R.copy(A.viewport),U.copy(A.scissor),C=A.scissorTest}else R.copy(Y).multiplyScalar(z).floor(),U.copy(fe).multiplyScalar(z).floor(),C=Ie;if(W!==0&&(j=ll),Me.bindFramebuffer(L.FRAMEBUFFER,j)&&K&&Me.drawBuffers(A,j),Me.viewport(R),Me.scissor(U),Me.setScissorTest(C),oe){const Te=we.get(A.texture);L.framebufferTexture2D(L.FRAMEBUFFER,L.COLOR_ATTACHMENT0,L.TEXTURE_CUBE_MAP_POSITIVE_X+V,Te.__webglTexture,W)}else if(me){const Te=we.get(A.texture),ke=V;L.framebufferTextureLayer(L.FRAMEBUFFER,L.COLOR_ATTACHMENT0,Te.__webglTexture,W,ke)}else if(A!==null&&W!==0){const Te=we.get(A.texture);L.framebufferTexture2D(L.FRAMEBUFFER,L.COLOR_ATTACHMENT0,L.TEXTURE_2D,Te.__webglTexture,W)}M=-1},this.readRenderTargetPixels=function(A,V,W,K,j,oe,me){if(!(A&&A.isWebGLRenderTarget)){console.error("THREE.WebGLRenderer.readRenderTargetPixels: renderTarget is not THREE.WebGLRenderTarget.");return}let Se=we.get(A).__webglFramebuffer;if(A.isWebGLCubeRenderTarget&&me!==void 0&&(Se=Se[me]),Se){Me.bindFramebuffer(L.FRAMEBUFFER,Se);try{const Te=A.texture,ke=Te.format,Ne=Te.type;if(!Re.textureFormatReadable(ke)){console.error("THREE.WebGLRenderer.readRenderTargetPixels: renderTarget is not in RGBA or implementation defined format.");return}if(!Re.textureTypeReadable(Ne)){console.error("THREE.WebGLRenderer.readRenderTargetPixels: renderTarget is not in UnsignedByteType or implementation defined type.");return}V>=0&&V<=A.width-K&&W>=0&&W<=A.height-j&&L.readPixels(V,W,K,j,Ve.convert(ke),Ve.convert(Ne),oe)}finally{const Te=D!==null?we.get(D).__webglFramebuffer:null;Me.bindFramebuffer(L.FRAMEBUFFER,Te)}}},this.readRenderTargetPixelsAsync=async function(A,V,W,K,j,oe,me){if(!(A&&A.isWebGLRenderTarget))throw new Error("THREE.WebGLRenderer.readRenderTargetPixels: renderTarget is not THREE.WebGLRenderTarget.");let Se=we.get(A).__webglFramebuffer;if(A.isWebGLCubeRenderTarget&&me!==void 0&&(Se=Se[me]),Se){const Te=A.texture,ke=Te.format,Ne=Te.type;if(!Re.textureFormatReadable(ke))throw new Error("THREE.WebGLRenderer.readRenderTargetPixelsAsync: renderTarget is not in RGBA or implementation defined format.");if(!Re.textureTypeReadable(Ne))throw new Error("THREE.WebGLRenderer.readRenderTargetPixelsAsync: renderTarget is not in UnsignedByteType or implementation defined type.");if(V>=0&&V<=A.width-K&&W>=0&&W<=A.height-j){Me.bindFramebuffer(L.FRAMEBUFFER,Se);const Pe=L.createBuffer();L.bindBuffer(L.PIXEL_PACK_BUFFER,Pe),L.bufferData(L.PIXEL_PACK_BUFFER,oe.byteLength,L.STREAM_READ),L.readPixels(V,W,K,j,Ve.convert(ke),Ve.convert(Ne),0);const Ze=D!==null?we.get(D).__webglFramebuffer:null;Me.bindFramebuffer(L.FRAMEBUFFER,Ze);const et=L.fenceSync(L.SYNC_GPU_COMMANDS_COMPLETE,0);return L.flush(),await lu(L,et,4),L.bindBuffer(L.PIXEL_PACK_BUFFER,Pe),L.getBufferSubData(L.PIXEL_PACK_BUFFER,0,oe),L.deleteBuffer(Pe),L.deleteSync(et),oe}else throw new Error("THREE.WebGLRenderer.readRenderTargetPixelsAsync: requested read bounds are out of range.")}},this.copyFramebufferToTexture=function(A,V=null,W=0){A.isTexture!==!0&&(Hn("WebGLRenderer: copyFramebufferToTexture function signature has changed."),V=arguments[0]||null,A=arguments[1]);const K=Math.pow(2,-W),j=Math.floor(A.image.width*K),oe=Math.floor(A.image.height*K),me=V!==null?V.x:0,Se=V!==null?V.y:0;I.setTexture2D(A,0),L.copyTexSubImage2D(L.TEXTURE_2D,W,0,0,me,Se,j,oe),Me.unbindTexture()};const ul=L.createFramebuffer(),dl=L.createFramebuffer();this.copyTextureToTexture=function(A,V,W=null,K=null,j=0,oe=null){A.isTexture!==!0&&(Hn("WebGLRenderer: copyTextureToTexture function signature has changed."),K=arguments[0]||null,A=arguments[1],V=arguments[2],oe=arguments[3]||0,W=null),oe===null&&(j!==0?(Hn("WebGLRenderer: copyTextureToTexture function signature has changed to support src and dst mipmap levels."),oe=j,j=0):oe=0);let me,Se,Te,ke,Ne,Pe,Ze,et,ft;const ut=A.isCompressedTexture?A.mipmaps[oe]:A.image;if(W!==null)me=W.max.x-W.min.x,Se=W.max.y-W.min.y,Te=W.isBox3?W.max.z-W.min.z:1,ke=W.min.x,Ne=W.min.y,Pe=W.isBox3?W.min.z:0;else{const Vt=Math.pow(2,-j);me=Math.floor(ut.width*Vt),Se=Math.floor(ut.height*Vt),A.isDataArrayTexture?Te=ut.depth:A.isData3DTexture?Te=Math.floor(ut.depth*Vt):Te=1,ke=0,Ne=0,Pe=0}K!==null?(Ze=K.x,et=K.y,ft=K.z):(Ze=0,et=0,ft=0);const Je=Ve.convert(V.format),De=Ve.convert(V.type);let St;V.isData3DTexture?(I.setTexture3D(V,0),St=L.TEXTURE_3D):V.isDataArrayTexture||V.isCompressedArrayTexture?(I.setTexture2DArray(V,0),St=L.TEXTURE_2D_ARRAY):(I.setTexture2D(V,0),St=L.TEXTURE_2D),L.pixelStorei(L.UNPACK_FLIP_Y_WEBGL,V.flipY),L.pixelStorei(L.UNPACK_PREMULTIPLY_ALPHA_WEBGL,V.premultiplyAlpha),L.pixelStorei(L.UNPACK_ALIGNMENT,V.unpackAlignment);const tt=L.getParameter(L.UNPACK_ROW_LENGTH),Xt=L.getParameter(L.UNPACK_IMAGE_HEIGHT),ni=L.getParameter(L.UNPACK_SKIP_PIXELS),zt=L.getParameter(L.UNPACK_SKIP_ROWS),Ni=L.getParameter(L.UNPACK_SKIP_IMAGES);L.pixelStorei(L.UNPACK_ROW_LENGTH,ut.width),L.pixelStorei(L.UNPACK_IMAGE_HEIGHT,ut.height),L.pixelStorei(L.UNPACK_SKIP_PIXELS,ke),L.pixelStorei(L.UNPACK_SKIP_ROWS,Ne),L.pixelStorei(L.UNPACK_SKIP_IMAGES,Pe);const ot=A.isDataArrayTexture||A.isData3DTexture,Bt=V.isDataArrayTexture||V.isData3DTexture;if(A.isDepthTexture){const Vt=we.get(A),At=we.get(V),Pt=we.get(Vt.__renderTarget),qa=we.get(At.__renderTarget);Me.bindFramebuffer(L.READ_FRAMEBUFFER,Pt.__webglFramebuffer),Me.bindFramebuffer(L.DRAW_FRAMEBUFFER,qa.__webglFramebuffer);for(let kn=0;kn<Te;kn++)ot&&(L.framebufferTextureLayer(L.READ_FRAMEBUFFER,L.COLOR_ATTACHMENT0,we.get(A).__webglTexture,j,Pe+kn),L.framebufferTextureLayer(L.DRAW_FRAMEBUFFER,L.COLOR_ATTACHMENT0,we.get(V).__webglTexture,oe,ft+kn)),L.blitFramebuffer(ke,Ne,me,Se,Ze,et,me,Se,L.DEPTH_BUFFER_BIT,L.NEAREST);Me.bindFramebuffer(L.READ_FRAMEBUFFER,null),Me.bindFramebuffer(L.DRAW_FRAMEBUFFER,null)}else if(j!==0||A.isRenderTargetTexture||we.has(A)){const Vt=we.get(A),At=we.get(V);Me.bindFramebuffer(L.READ_FRAMEBUFFER,ul),Me.bindFramebuffer(L.DRAW_FRAMEBUFFER,dl);for(let Pt=0;Pt<Te;Pt++)ot?L.framebufferTextureLayer(L.READ_FRAMEBUFFER,L.COLOR_ATTACHMENT0,Vt.__webglTexture,j,Pe+Pt):L.framebufferTexture2D(L.READ_FRAMEBUFFER,L.COLOR_ATTACHMENT0,L.TEXTURE_2D,Vt.__webglTexture,j),Bt?L.framebufferTextureLayer(L.DRAW_FRAMEBUFFER,L.COLOR_ATTACHMENT0,At.__webglTexture,oe,ft+Pt):L.framebufferTexture2D(L.DRAW_FRAMEBUFFER,L.COLOR_ATTACHMENT0,L.TEXTURE_2D,At.__webglTexture,oe),j!==0?L.blitFramebuffer(ke,Ne,me,Se,Ze,et,me,Se,L.COLOR_BUFFER_BIT,L.NEAREST):Bt?L.copyTexSubImage3D(St,oe,Ze,et,ft+Pt,ke,Ne,me,Se):L.copyTexSubImage2D(St,oe,Ze,et,ke,Ne,me,Se);Me.bindFramebuffer(L.READ_FRAMEBUFFER,null),Me.bindFramebuffer(L.DRAW_FRAMEBUFFER,null)}else Bt?A.isDataTexture||A.isData3DTexture?L.texSubImage3D(St,oe,Ze,et,ft,me,Se,Te,Je,De,ut.data):V.isCompressedArrayTexture?L.compressedTexSubImage3D(St,oe,Ze,et,ft,me,Se,Te,Je,ut.data):L.texSubImage3D(St,oe,Ze,et,ft,me,Se,Te,Je,De,ut):A.isDataTexture?L.texSubImage2D(L.TEXTURE_2D,oe,Ze,et,me,Se,Je,De,ut.data):A.isCompressedTexture?L.compressedTexSubImage2D(L.TEXTURE_2D,oe,Ze,et,ut.width,ut.height,Je,ut.data):L.texSubImage2D(L.TEXTURE_2D,oe,Ze,et,me,Se,Je,De,ut);L.pixelStorei(L.UNPACK_ROW_LENGTH,tt),L.pixelStorei(L.UNPACK_IMAGE_HEIGHT,Xt),L.pixelStorei(L.UNPACK_SKIP_PIXELS,ni),L.pixelStorei(L.UNPACK_SKIP_ROWS,zt),L.pixelStorei(L.UNPACK_SKIP_IMAGES,Ni),oe===0&&V.generateMipmaps&&L.generateMipmap(St),Me.unbindTexture()},this.copyTextureToTexture3D=function(A,V,W=null,K=null,j=0){return A.isTexture!==!0&&(Hn("WebGLRenderer: copyTextureToTexture3D function signature has changed."),W=arguments[0]||null,K=arguments[1]||null,A=arguments[2],V=arguments[3],j=arguments[4]||0),Hn('WebGLRenderer: copyTextureToTexture3D function has been deprecated. Use "copyTextureToTexture" instead.'),this.copyTextureToTexture(A,V,W,K,j)},this.initRenderTarget=function(A){we.get(A).__webglFramebuffer===void 0&&I.setupRenderTarget(A)},this.initTexture=function(A){A.isCubeTexture?I.setTextureCube(A,0):A.isData3DTexture?I.setTexture3D(A,0):A.isDataArrayTexture||A.isCompressedArrayTexture?I.setTexture2DArray(A,0):I.setTexture2D(A,0),Me.unbindTexture()},this.resetState=function(){y=0,w=0,D=null,Me.reset(),rt.reset()},typeof __THREE_DEVTOOLS__<"u"&&__THREE_DEVTOOLS__.dispatchEvent(new CustomEvent("observe",{detail:this}))}get coordinateSystem(){return pn}get outputColorSpace(){return this._outputColorSpace}set outputColorSpace(e){this._outputColorSpace=e;const t=this.getContext();t.drawingBufferColorspace=Qe._getDrawingBufferColorSpace(e),t.unpackColorSpace=Qe._getUnpackColorSpace()}}const Tn=1e-6,Mi=5e-5,Cr=1e-7;function bs(n,e){return n[0]*e[0]+n[1]*e[1]+n[2]*e[2]}function ys(n,e){return[n[0]-e[0],n[1]-e[1],n[2]-e[2]]}function Ts(n,e){return[n[1]*e[2]-n[2]*e[1],n[2]*e[0]-n[0]*e[2],n[0]*e[1]-n[1]*e[0]]}function Pm(n){const e=Math.hypot(n[0],n[1],n[2]);return e<1e-12?null:[n[0]/e,n[1]/e,n[2]/e]}function Na(n,e){const t=n[0]-e[0],i=n[1]-e[1],a=n[2]-e[2];return t*t+i*i+a*a}function Pr(n){if(n.length<3)return 0;const e=n[0];let t=0,i=0,a=0;for(let r=1;r+1<n.length;r++){const s=ys(n[r],e),o=ys(n[r+1],e),c=Ts(s,o);t+=c[0],i+=c[1],a+=c[2]}return .5*Math.hypot(t,i,a)}function Im(n,e){const t=[],i=Mi*Mi;for(const f of n)t.some(m=>Na(f,m)<=i)||t.push(f);if(t.length<3)return[];let a=0,r=0,s=0;for(const f of t)a+=f[0],r+=f[1],s+=f[2];a/=t.length,r/=t.length,s/=t.length;const o=[a,r,s],c=Math.abs(e[0])<.8?[1,0,0]:[0,1,0],l=Pm(Ts(c,e));if(!l)return[];const u=Ts(e,l),h=t.map(f=>{const m=ys(f,o),g=bs(m,l),_=bs(m,u);return{tacka:f,ugao:Math.atan2(_,g)}});return h.sort((f,m)=>f.ugao-m.ugao),h.map(f=>f.tacka)}function Dm(n){return[{normala:[1,0,0],grupaId:"__okvir__",oznaka:"",temena:[[n,-n,-n],[n,n,-n],[n,n,n],[n,-n,n]]},{normala:[-1,0,0],grupaId:"__okvir__",oznaka:"",temena:[[-n,-n,n],[-n,n,n],[-n,n,-n],[-n,-n,-n]]},{normala:[0,1,0],grupaId:"__okvir__",oznaka:"",temena:[[-n,n,-n],[-n,n,n],[n,n,n],[n,n,-n]]},{normala:[0,-1,0],grupaId:"__okvir__",oznaka:"",temena:[[-n,-n,n],[-n,-n,-n],[n,-n,-n],[n,-n,n]]},{normala:[0,0,1],grupaId:"__okvir__",oznaka:"",temena:[[-n,-n,n],[n,-n,n],[n,n,n],[-n,n,n]]},{normala:[0,0,-1],grupaId:"__okvir__",oznaka:"",temena:[[n,-n,-n],[-n,-n,-n],[-n,n,-n],[n,n,-n]]}]}function qi(n){if(n.length===0)return{temena:[],pljosni:[]};let e=1;const t=[];for(let c=0;c<n.length;c++){const l=n[c],u=Math.hypot(l.normala[0],l.normala[1],l.normala[2]);if(u<1e-12)continue;const h=[l.normala[0]/u,l.normala[1]/u,l.normala[2]/u],f=l.d;e=Math.max(e,Math.abs(f)),t.push({normala:h,d:f,grupaId:l.grupaId??`forma-${c}`,oznaka:l.oznaka??""})}let i=Dm(Math.max(12,e*6));for(const c of t){const l=[],u=[];for(const f of i){const m=f.temena.length;if(m<3)continue;const g=f.temena.map(E=>bs(c.normala,E)-c.d),_=[];for(let E=0;E<m;E++){const S=(E+1)%m,x=f.temena[E],T=f.temena[S],y=g[E],w=g[S],D=y<=Tn,M=w<=Tn;if(Math.abs(y)<=Tn*4&&u.push(x),D&&_.push(x),y<-Tn&&w>Tn||y>Tn&&w<-Tn){const v=y/(y-w),R=[x[0]+(T[0]-x[0])*v,x[1]+(T[1]-x[1])*v,x[2]+(T[2]-x[2])*v];_.push(R),u.push(R)}else!D&&M&&Math.abs(w)<=Tn&&u.push(T)}const p=[],d=Mi*Mi;for(const E of _)(p.length===0||Na(E,p[p.length-1])>d)&&p.push(E);p.length>1&&Na(p[0],p[p.length-1])<=d&&p.pop(),p.length>=3&&Pr(p)>Cr&&l.push({temena:p,normala:f.normala,grupaId:f.grupaId,oznaka:f.oznaka})}const h=Im(u,c.normala);if(h.length>=3&&Pr(h)>Cr&&l.push({temena:h,normala:c.normala,grupaId:c.grupaId,oznaka:c.oznaka}),i=l,i.length===0)break}const a=[],r=[],s=Mi*Mi;function o(c){for(let l=0;l<a.length;l++)if(Na(a[l],c)<=s)return l;return a.push([Math.abs(c[0])<1e-10?0:c[0],Math.abs(c[1])<1e-10?0:c[1],Math.abs(c[2])<1e-10?0:c[2]]),a.length-1}for(const c of i){if(c.grupaId==="__okvir__")continue;const l=Pr(c.temena);if(l<=Cr)continue;const u=c.temena.map(p=>o(p)),h=[];for(const p of u)(h.length===0||h[h.length-1]!==p)&&h.push(p);if(h.length>1&&h[0]===h[h.length-1]&&h.pop(),h.length<3)continue;let f=0,m=0,g=0;for(const p of h){const d=a[p];f+=d[0],m+=d[1],g+=d[2]}const _=h.length;r.push({indeksiTemena:h,normala:c.normala,centar:[f/_,m/_,g/_],povrsina:l,grupaId:c.grupaId,oznaka:c.oznaka})}return{temena:a,pljosni:r}}function $i(n){const e=[];for(const u of n.pljosni)e.includes(u.grupaId)||e.push(u.grupaId);const t=[],i=[],a=[],r=[];for(let u=0;u<e.length;u++){const h=e[u],f=t.length/3;for(let g=0;g<n.pljosni.length;g++){const _=n.pljosni[g];if(_.grupaId!==h)continue;const p=_.indeksiTemena;if(p.length<3)continue;const d=n.temena[p[0]],[E,S,x]=_.normala;for(let T=1;T+1<p.length;T++){const y=n.temena[p[T]],w=n.temena[p[T+1]];t.push(d[0],d[1],d[2],y[0],y[1],y[2],w[0],w[1],w[2]),i.push(E,S,x,E,S,x,E,S,x),a.push(g)}}const m=t.length/3;m>f&&r.push({pocetak:f,broj:m-f,indeksMaterijala:u})}const s=new $e;s.setAttribute("position",new He(t,3)),s.setAttribute("normal",new He(i,3));for(const u of r)s.addGroup(u.pocetak,u.broj,u.indeksMaterijala);const o=new Set,c=[];for(const u of n.pljosni){const h=u.indeksiTemena;for(let f=0;f<h.length;f++){const m=h[f],g=h[(f+1)%h.length],_=m<g?`${m}-${g}`:`${g}-${m}`;if(o.has(_))continue;o.add(_);const p=n.temena[m],d=n.temena[g];c.push(p[0],p[1],p[2],d[0],d[1],d[2])}}const l=new $e;return l.setAttribute("position",new He(c,3)),{geometrijaMreze:s,geometrijaIvica:l,mapaTrougaoUPljosan:a,redosledGrupa:e}}function _i(n,e,t){return Math.max(e,Math.min(t,n))}class Lm{stanje;pocetno;minUdaljenost;maksUdaljenost;opcije;vuceMisem=!1;prethodniX=0;prethodniY=0;dodirAktiviran=!1;prethodniDodirX=0;prethodniDodirY=0;prethodniRazmakPrstiju=0;pocetakDodiraX=0;pocetakDodiraY=0;dodirPomeren=!1;cistaci=[];constructor(e){this.opcije=e,this.pocetno={...e.pocetno},this.stanje={...e.pocetno},this.minUdaljenost=e.minUdaljenost??2,this.maksUdaljenost=e.maksUdaljenost??24,this.poveziDogadjaje()}trenutnoStanje(){return{...this.stanje}}rotirajAzimut(e){this.stanje.theta+=e,this.opcije.naPromenu(this.trenutnoStanje())}rotirajElevaciju(e){this.stanje.phi=_i(this.stanje.phi+e,.15,Math.PI-.15),this.opcije.naPromenu(this.trenutnoStanje())}zumiraj(e){this.stanje.udaljenost=_i(this.stanje.udaljenost*e,this.minUdaljenost,this.maksUdaljenost),this.opcije.naPromenu(this.trenutnoStanje())}resetuj(){this.stanje={...this.pocetno},this.opcije.naPromenu(this.trenutnoStanje())}postaviAktivacijuDodira(e){this.dodirAktiviran=e,this.opcije.platno.classList.toggle("udzbenik-scena-platno--dodir-aktivan",e),this.opcije.dugmeDodira.hidden=!e,this.opcije.priPromeniAktivacijeDodira?.(e)}poveziDogadjaje(){const{bina:e,platno:t,dugmeDodira:i}=this.opcije,a=g=>{if(g.pointerType!=="touch"&&g.button===0){this.vuceMisem=!0,this.prethodniX=g.clientX,this.prethodniY=g.clientY;try{t.setPointerCapture(g.pointerId)}catch{}}},r=g=>{if(g.pointerType==="touch"||!this.vuceMisem)return;const _=g.clientX-this.prethodniX,p=g.clientY-this.prethodniY;this.prethodniX=g.clientX,this.prethodniY=g.clientY,this.stanje.theta-=_*.008,this.stanje.phi=_i(this.stanje.phi-p*.008,.15,Math.PI-.15),this.opcije.naPromenu(this.trenutnoStanje())},s=g=>{if(g.pointerType!=="touch"){this.vuceMisem=!1;try{t.hasPointerCapture(g.pointerId)&&t.releasePointerCapture(g.pointerId)}catch{}}},o=g=>{if(!(document.activeElement===e||e.contains(document.activeElement))&&!g.ctrlKey&&!g.metaKey)return;g.preventDefault();const p=g.deltaY>0?1.09:.92;this.zumiraj(p)},c=g=>{if(g.touches.length===2){const _=g.touches[0],p=g.touches[1];this.prethodniDodirX=(_.clientX+p.clientX)/2,this.prethodniDodirY=(_.clientY+p.clientY)/2,this.prethodniRazmakPrstiju=Math.hypot(p.clientX-_.clientX,p.clientY-_.clientY)}else if(g.touches.length===1){const _=g.touches[0];this.pocetakDodiraX=_.clientX,this.pocetakDodiraY=_.clientY,this.prethodniDodirX=_.clientX,this.prethodniDodirY=_.clientY,this.dodirPomeren=!1}},l=g=>{if(g.touches.length===2){g.preventDefault();const _=g.touches[0],p=g.touches[1],d=(_.clientX+p.clientX)/2,E=(_.clientY+p.clientY)/2,S=Math.hypot(p.clientX-_.clientX,p.clientY-_.clientY),x=d-this.prethodniDodirX,T=E-this.prethodniDodirY;if(this.prethodniDodirX=d,this.prethodniDodirY=E,this.stanje.theta-=x*.008,this.stanje.phi=_i(this.stanje.phi-T*.008,.15,Math.PI-.15),this.prethodniRazmakPrstiju>8&&S>8){const y=this.prethodniRazmakPrstiju/S;this.stanje.udaljenost=_i(this.stanje.udaljenost*y,this.minUdaljenost,this.maksUdaljenost)}this.prethodniRazmakPrstiju=S,this.dodirPomeren=!0,this.opcije.naPromenu(this.trenutnoStanje())}else if(g.touches.length===1){const _=g.touches[0];if(Math.hypot(_.clientX-this.pocetakDodiraX,_.clientY-this.pocetakDodiraY)>8&&(this.dodirPomeren=!0),this.dodirAktiviran){g.preventDefault();const p=_.clientX-this.prethodniDodirX,d=_.clientY-this.prethodniDodirY;this.prethodniDodirX=_.clientX,this.prethodniDodirY=_.clientY,this.stanje.theta-=p*.009,this.stanje.phi=_i(this.stanje.phi-d*.009,.15,Math.PI-.15),this.opcije.naPromenu(this.trenutnoStanje())}}},u=g=>{g.touches.length===0&&!this.dodirPomeren&&g.changedTouches.length===1&&this.postaviAktivacijuDodira(!this.dodirAktiviran)},h=()=>{this.postaviAktivacijuDodira(!1)},f=g=>{this.dodirAktiviran&&g.target instanceof Node&&!e.contains(g.target)&&this.postaviAktivacijuDodira(!1)},m=g=>{if(!(g.target instanceof HTMLElement&&g.target!==e&&(g.target.tagName==="BUTTON"||g.target.tagName==="INPUT")))switch(g.key){case"ArrowLeft":g.preventDefault(),this.rotirajAzimut(-.12);break;case"ArrowRight":g.preventDefault(),this.rotirajAzimut(.12);break;case"ArrowUp":g.preventDefault(),this.rotirajElevaciju(-.12);break;case"ArrowDown":g.preventDefault(),this.rotirajElevaciju(.12);break;case"+":case"=":g.preventDefault(),this.zumiraj(.88);break;case"-":case"_":g.preventDefault(),this.zumiraj(1.14);break;case"r":case"R":case"р":case"Р":g.preventDefault(),this.opcije.naReset();break;case" ":g.preventDefault(),this.opcije.naPrekidacPauze();break;case"Escape":this.dodirAktiviran&&(g.preventDefault(),this.postaviAktivacijuDodira(!1));break}};t.addEventListener("pointerdown",a),t.addEventListener("pointermove",r),t.addEventListener("pointerup",s),t.addEventListener("pointercancel",s),t.addEventListener("wheel",o,{passive:!1}),t.addEventListener("touchstart",c,{passive:!0}),t.addEventListener("touchmove",l,{passive:!1}),t.addEventListener("touchend",u),i.addEventListener("click",h),document.addEventListener("touchstart",f,{passive:!0}),e.addEventListener("keydown",m),this.cistaci.push(()=>{t.removeEventListener("pointerdown",a),t.removeEventListener("pointermove",r),t.removeEventListener("pointerup",s),t.removeEventListener("pointercancel",s),t.removeEventListener("wheel",o),t.removeEventListener("touchstart",c),t.removeEventListener("touchmove",l),t.removeEventListener("touchend",u),i.removeEventListener("click",h),document.removeEventListener("touchstart",f),e.removeEventListener("keydown",m)})}raspolazi(){for(const e of this.cistaci)e();this.cistaci.length=0}}let hn=null,Si=null,Jn=0,Qn=0;function Um(){if(hn)return hn;const n=document.createElement("canvas"),e=n.getContext("webgl2",{antialias:!0,alpha:!1,preserveDrawingBuffer:!1})??n.getContext("webgl",{antialias:!0,alpha:!1,preserveDrawingBuffer:!1});if(!e)throw new Error("WebGL контекст није доступан у овом прегледачу.");const t=new Cm({canvas:n,context:e,antialias:!0,alpha:!1,powerPreference:"default"});return t.setPixelRatio(1),t.outputColorSpace=Ft,Si=n,hn=t,Jn=320,Qn=240,hn.setSize(Jn,Qn,!1),hn}function zm(){hn&&(hn.forceContextLoss(),hn.dispose(),hn=null,Si=null,Jn=0,Qn=0)}function Ut(n){n.traverse(e=>{const t=e;t.geometry&&typeof t.geometry.dispose=="function"&&t.geometry.dispose();const i=t.material;if(Array.isArray(i))for(const a of i)cc(a);else i&&cc(i)})}function cc(n){for(const e of Object.values(n))e instanceof Ct&&e.dispose();n.dispose()}function km(n,e,t,i){const a=Um(),r=t.platno.getContext("2d");if(!r||!Si)throw new Error("2D контекст платна није доступан.");const s=typeof window<"u"&&typeof window.matchMedia=="function"&&window.matchMedia("(prefers-reduced-motion: reduce)").matches,o=new ku,c=new Ht(42,16/9,.1,100),l=new F(0,0,0),u=new Gu(new ce(1,1,1),.72),h=new Uo(new ce(1,1,1),.95);h.position.set(5,8,6);const f=new Uo(new ce(1,1,1),.38);f.position.set(-5,-3,-4),o.add(u,h,f);const m=n.pocetnaKamera?.(e)??{theta:.62,phi:1.12,udaljenost:6.2};function g(ee){const _e=Math.sin(ee.phi);c.position.set(l.x+ee.udaljenost*_e*Math.sin(ee.theta),l.y+ee.udaljenost*Math.cos(ee.phi),l.z+ee.udaljenost*_e*Math.cos(ee.theta)),c.lookAt(l),c.updateMatrixWorld()}g(m);let _=!1,p=!1,d=!0,E=n.imaPodrazumevanuAnimaciju?n.imaPodrazumevanuAnimaciju(e):!0,S=s||!E,x=null,T=null,y=0,w=0,D=Math.max(240,t.bina.clientWidth||600),M=Math.max(180,t.bina.clientHeight||360),v=null;function R(){if(_||p||!Si||!r)return;const ee=t.bina.clientWidth,_e=t.bina.clientHeight;ee>0&&_e>0&&(D=ee,M=_e);const de=Math.min(typeof window<"u"&&window.devicePixelRatio||1,2),Z=Math.max(1,Math.round(D*de)),ae=Math.max(1,Math.round(M*de));(t.platno.width!==Z||t.platno.height!==ae)&&(t.platno.width=Z,t.platno.height=ae),c.aspect=D/Math.max(1,M),c.updateProjectionMatrix();const re=Math.min(4096,Math.max(Jn,Z)),L=Math.min(4096,Math.max(Qn,ae));(re>Jn||L>Qn)&&(Jn=re,Qn=L,a.setSize(Jn,Qn,!1));const Le=new ce(Ya.token("--bg-card"));a.setViewport(0,0,Z,ae),a.setScissor(0,0,Z,ae),a.setScissorTest(!0),a.setClearColor(Le,1),a.clear(!0,!0,!0),a.render(o,c);const Ce=Math.max(0,Si.height-ae);r.drawImage(Si,0,Ce,Z,ae,0,0,Z,ae),v?.posleRendera?.()}function U(){_||p||x!==null||T!==null||(T=requestAnimationFrame(()=>{T=null,R()}))}function C(){const ee=typeof document<"u"&&document.hidden;return!_&&!p&&E&&!S&&d&&!ee}function P(ee){if(x=null,!C())return;const _e=y>0?Math.min(.05,(ee-y)/1e3):.016;y=ee,w+=_e,v?.azuriraj?.(_e,w),R(),C()&&(x=requestAnimationFrame(P))}function N(){t.azurirajDugmePauze(S,E),C()?x===null&&(y=performance.now(),x=requestAnimationFrame(P)):x!==null&&(cancelAnimationFrame(x),x=null)}function k(ee){const _e=ee.clone().project(c),de=_e.z>=-1&&_e.z<=1;return{x:(_e.x*.5+.5)*D,y:(-_e.y*.5+.5)*M,vidljivo:de}}const O={scena3D:o,kamera:c,platno:t.platno,slojEtiketa:t.slojEtiketa,gornjeKontrole:t.gornjeKontrole,podnozje:t.podnozje,api:i,tema:Ya,smanjenPokret:s,zatraziRender:U,postaviImaAnimaciju:ee=>{E=ee,ee||(S=!0),N()},prikaziRezervu:ee=>{p=!0,N(),t.prikaziRezervu(ee)},projektujU2D:k},z=new Lm({bina:t.bina,platno:t.platno,dugmeDodira:t.dugmeDodira,pocetno:m,naPromenu:ee=>{g(ee),U()},naReset:()=>{z.resetuj(),v?.resetuj?.(),R()},naPrekidacPauze:()=>{E&&(S=!S,N())}});v=n.kreiraj(O,e);const H=()=>{z.resetuj(),v?.resetuj?.(),R()},$=()=>{E&&(S=!S,N())},Y=()=>{S=!0,N(),v?.korak?v.korak():(w+=.45,v?.azuriraj?.(.45,w)),R()},fe=()=>z.zumiraj(.86),Ie=()=>z.zumiraj(1.16);t.dugmeReset.addEventListener("click",H),t.dugmePauza.addEventListener("click",$),t.dugmeKorak.addEventListener("click",Y),t.dugmeZumPlus.addEventListener("click",fe),t.dugmeZumMinus.addEventListener("click",Ie);let X=null;typeof ResizeObserver<"u"&&(X=new ResizeObserver(ee=>{for(const _e of ee){const de=Math.round(_e.contentRect.width),Z=Math.round(_e.contentRect.height);de>0&&Z>0&&(de!==D||Z!==M)&&(D=de,M=Z,R())}}),X.observe(t.bina));let ne=null;typeof IntersectionObserver<"u"&&(ne=new IntersectionObserver(ee=>{for(const _e of ee)d=_e.isIntersecting,N()},{threshold:.05}),ne.observe(t.bina));const ue=()=>{N(),document.hidden||U()};document.addEventListener("visibilitychange",ue);const se=Ya.pretplati(ee=>{v?.osveziTemu?.(ee),R()});return R(),N(),()=>{_||(_=!0,x!==null&&(cancelAnimationFrame(x),x=null),T!==null&&(cancelAnimationFrame(T),T=null),X?.disconnect(),ne?.disconnect(),document.removeEventListener("visibilitychange",ue),se(),t.dugmeReset.removeEventListener("click",H),t.dugmePauza.removeEventListener("click",$),t.dugmeKorak.removeEventListener("click",Y),t.dugmeZumPlus.removeEventListener("click",fe),t.dugmeZumMinus.removeEventListener("click",Ie),z.raspolazi(),v?.raspolazi?.(),Ut(o),o.clear(),t.slojEtiketa.replaceChildren(),t.gornjeKontrole.replaceChildren(),t.podnozje.replaceChildren())}}const lc={karlsbadski:{zakon:"karlsbadski",naziv:"Карлсбадски близанац",mineral:"ортоклас",sistem:"моноклинични",tipElementa:"osa",opisElementa:"Оса близањења [001] (c-оса), раван срастања (010)",normalaRavniIliOsa:[0,0,1],ugaoRotacijeStepeni:180,izvor:"Klein & Dutrow 2007, str. 235"},spinelov:{zakon:"spinelov",naziv:"Спинелов закон",mineral:"спинел (октаедар)",sistem:"кубни",tipElementa:"ravan",opisElementa:"Раван близањења (111)",normalaRavniIliOsa:[1/Math.sqrt(3),1/Math.sqrt(3),1/Math.sqrt(3)],izvor:"Klein & Dutrow 2007, str. 233"},baveno:{zakon:"baveno",naziv:"Бавено близанац",mineral:"ортоклас",sistem:"моноклинични",tipElementa:"ravan",opisElementa:"Раван близањења (021), моноклинична метрика (β ≈ 116°)",normalaRavniIliOsa:[.31,.7071,.6355],izvor:"Klein & Dutrow 2007, str. 235"},manebah:{zakon:"manebah",naziv:"Манебах близанац",mineral:"ортоклас",sistem:"моноклинични",tipElementa:"ravan",opisElementa:"Раван близањења (001), c* нормала одступа ~26° од c-осе због β ≈ 116°",normalaRavniIliOsa:[.4384,0,.8988],izvor:"Klein & Dutrow 2007, str. 235"},"albitski-polisintetski":{zakon:"albitski-polisintetski",naziv:"Албитски полисинтетски закон",mineral:"албит / плагиоклас",sistem:"триклинични",tipElementa:"ravan",opisElementa:"Раван близањења (010), вишеструке паралелне ламеле",normalaRavniIliOsa:[0,1,0],izvor:"Nesse 2012, str. 280"},japanski:{zakon:"japanski",naziv:"Јапански закон",mineral:"кварц",sistem:"тригонални",tipElementa:"ravan",opisElementa:"Раван близањења (11-22), теоријски угао међу c-осама 84°33′",normalaRavniIliOsa:[.37,.6408,.6726],ugaoOsaStepeni:84.55,izvor:"Frondel 1962, Dana System of Mineralogy Vol. III (a 4,913 c 5,405 Å)",napomena:"Угао 84°33′ је теоријски угао контакта две јединке кварца по (11-22)."},dofinejski:{zakon:"dofinejski",naziv:"Дофинејски закон",mineral:"кварц",sistem:"тригонални",tipElementa:"osa",opisElementa:"Оса близањења [0001] (c-оса), ротација за 180°",normalaRavniIliOsa:[0,0,1],ugaoRotacijeStepeni:180,izvor:"Klein & Dutrow 2007, str. 236"},brazilski:{zakon:"brazilski",naziv:"Бразилски закон",mineral:"кварц",sistem:"тригонални",tipElementa:"ravan",opisElementa:"Раван близањења (11-20), нормала [0,5, √3/2, 0] ≠ [100]",normalaRavniIliOsa:[.5,.866025,0],izvor:"Klein & Dutrow 2007, str. 236; International Tables хексагонска метрика"},"lastin-rep":{zakon:"lastin-rep",naziv:"Ластин реп (близанац гипса)",mineral:"гипс",sistem:"моноклинични",tipElementa:"ravan",opisElementa:"Раван близањења (100)",normalaRavniIliOsa:[1,0,0],izvor:"Klein & Dutrow 2007, str. 235"},"staurolit-90":{zakon:"staurolit-90",naziv:"Крстасти близанац стауролита (90°)",mineral:"стауролит",sistem:"моноклинични / псеудоорторомбични",tipElementa:"ravan",opisElementa:"Раван близањења (031), две јединке под ~90°",normalaRavniIliOsa:[0,.7071,.7071],izvor:"Klein & Dutrow 2007, str. 234"},"staurolit-60":{zakon:"staurolit-60",naziv:"Коси крстасти близанац стауролита (60°)",mineral:"стауролит",sistem:"моноклинични / псеудоорторомбични",tipElementa:"ravan",opisElementa:"Раван близањења (231), две c-осе заклапају ~60° (59°05′)",normalaRavniIliOsa:[.7093,.5038,.4931],ugaoOsaStepeni:59.08,izvor:"Klein & Dutrow 2007, str. 234 (метрика: a 7,87 b 16,62 c 5,66 Å)"},"kolenasti-rutil":{zakon:"kolenasti-rutil",naziv:"Коленасти близанац рутила",mineral:"рутил",sistem:"тетрагонални",tipElementa:"ravan",opisElementa:"Раван близањења (011), прегиб c-оса под 114°30′",normalaRavniIliOsa:[0,.542,.8404],ugaoOsaStepeni:114.5,izvor:"Klein & Dutrow 2007, str. 234 (тетрагонално a 4,59 c 2,96 Å)"},"trilinga-aragonit":{zakon:"trilinga-aragonit",naziv:"Циклички трилинг арагонита",mineral:"арагонит",sistem:"орторомбични",tipElementa:"ravan",opisElementa:"Раван близањења (110), псеудохексагонални склоп",normalaRavniIliOsa:[.707,.707,0],izvor:"Klein & Dutrow 2007, str. 235"},"gvozdeni-krst-pirit":{zakon:"gvozdeni-krst-pirit",naziv:"Гвоздени крст (близанац пирита)",mineral:"пирит",sistem:"кубни (m-3)",tipElementa:"osa",opisElementa:"Оса близањења [001] са прорастањем два пиритоедра",normalaRavniIliOsa:[0,0,1],ugaoRotacijeStepeni:90,izvor:"Klein & Dutrow 2007, str. 234"}};function Nm(n){const e=[];if(n.includes("спинел")||n.includes("октаедар"))for(const a of[1,-1])for(const r of[1,-1])for(const s of[1,-1]){const o=1/Math.sqrt(3);e.push({normala:[a*o,r*o,s*o],d:1})}else if(n.includes("ортоклас"))e.push({normala:[.707,.707,0],d:.9},{normala:[-.707,.707,0],d:.9},{normala:[.707,-.707,0],d:.9},{normala:[-.707,-.707,0],d:.9},{normala:[0,1,0],d:1},{normala:[0,-1,0],d:1},{normala:[0,0,1],d:1.5},{normala:[0,0,-1],d:1.5},{normala:[.5,0,.866],d:1.1},{normala:[-.5,0,-.866],d:1.1});else if(n.includes("кварц")){const a=Math.sqrt(3),r=[[1,0,0],[-1,0,0],[.5,a/2,0],[-.5,a/2,0],[.5,-a/2,0],[-.5,-a/2,0]];for(const l of r)e.push({normala:l,d:.85});const s=51.78*Math.PI/180,o=Math.sin(s),c=Math.cos(s);for(let l=0;l<6;l++){const u=l*60*Math.PI/180;e.push({normala:[o*Math.cos(u),o*Math.sin(u),c],d:1.35}),e.push({normala:[o*Math.cos(u),o*Math.sin(u),-c],d:1.35})}}else if(n.includes("пирит")){const a=[[0,1,2],[1,2,0],[2,0,1]],r=[[1,1],[1,-1],[-1,1],[-1,-1]],s=Math.sqrt(5);for(const o of a)for(const c of r){const l=[0,0,0];l[o[0]]=2*c[0]/s,l[o[1]]=1*c[1]/s,l[o[2]]=0,e.push({normala:[l[0],l[1],l[2]],d:1})}}else e.push({normala:[1,0,0],d:.75},{normala:[-1,0,0],d:.75},{normala:[0,1,0],d:.85},{normala:[0,-1,0],d:.85},{normala:[0,0,1],d:1.6},{normala:[0,0,-1],d:1.6},{normala:[.707,0,.707],d:1.25},{normala:[-.707,0,.707],d:1.25},{normala:[.707,0,-.707],d:1.25},{normala:[-.707,0,-.707],d:1.25});const t=qi(e);return $i(t).geometrijaMreze}const Fm={imaPodrazumevanuAnimaciju(n){return(n.animacija??"razdvoji-spoji")!=="nema"},pocetnaKamera(){return{theta:.65,phi:1.15,udaljenost:5.8}},kreiraj(n,e){const t=new it;n.scena3D.add(t);const i=lc[e.zakon]??lc.karlsbadski,a=Nm(i.mineral),r=new ct({color:new ce(n.tema.token("--primary")),roughness:.35,metalness:.1,flatShading:!0,side:mt}),s=new ct({color:new ce(n.tema.token("--accent")),roughness:.35,metalness:.1,flatShading:!0,side:mt}),o=new Ge(a,r),c=a.clone(),l=new Ge(c,s),u=new F(...i.normalaRavniIliOsa).normalize(),h=new it;if(h.add(l),i.tipElementa==="osa"){const x=(i.ugaoRotacijeStepeni??180)*Math.PI/180;l.rotateOnAxis(u,x)}else{const x=new st().set(1-2*u.x*u.x,-2*u.x*u.y,-2*u.x*u.z,0,-2*u.y*u.x,1-2*u.y*u.y,-2*u.y*u.z,0,-2*u.z*u.x,-2*u.z*u.y,1-2*u.z*u.z,0,0,0,0,1);c.applyMatrix4(x);const T=c.index;if(T){for(let y=0;y<T.count;y+=3){const w=T.getX(y+1);T.setX(y+1,T.getX(y+2)),T.setX(y+2,w)}T.needsUpdate=!0}c.computeVertexNormals()}t.add(o),t.add(h);const f=new Ui({color:new ce(n.tema.token("--warning")),transparent:!0,opacity:.35,side:mt}),m=new ht({color:new ce(n.tema.token("--warning")),linewidth:2});let g=null,_=null;if(e.prikazi_element!==!1)if(i.tipElementa==="ravan"){const x=new zi(3.5,3.5);g=new Ge(x,f),g.quaternion.setFromUnitVectors(new F(0,0,1),u),t.add(g)}else{const x=new $e,T=u.clone().multiplyScalar(-2.8),y=u.clone().multiplyScalar(2.8);x.setAttribute("position",new He([T.x,T.y,T.z,y.x,y.y,y.z],3)),_=new Xi(x,m),t.add(_)}const p=document.createElement("div");p.className="udzbenik-scena-status",p.textContent=`${i.naziv} (${i.mineral}) • ${i.opisElementa}`,n.podnozje.append(p);const d=e.animacija??"razdvoji-spoji";let E=0;function S(){r.color.set(n.tema.token("--primary")),s.color.set(n.tema.token("--accent")),f.color.set(n.tema.token("--warning")),m.color.set(n.tema.token("--warning"))}return{azuriraj(x){if(E+=x,d==="razdvoji-spoji"){const T=(Math.sin(E*1.5)*.5+.5)*1.1;h.position.copy(u.clone().multiplyScalar(T)),t.rotation.y=E*.25}else d==="rotacija"&&(t.rotation.y=E*.45)},korak(){E+=.4;const x=(Math.sin(E*1.5)*.5+.5)*1.1;h.position.copy(u.clone().multiplyScalar(x)),t.rotation.y+=.2},resetuj(){E=0,h.position.set(0,0,0),t.rotation.set(0,0,0)},osveziTemu(){S()},raspolazi(){a.dispose(),l.geometry.dispose(),r.dispose(),s.dispose(),f.dispose(),m.dispose(),g&&g.geometry.dispose(),_&&_.geometry.dispose(),Ut(t),p.remove()}}}},uc="Cordero et al., Dalton Trans., 2008, 2832–2838 (DOI: 10.1039/B801115J)",As={izvor:"Shannon 1976",vrednosti:{Na:{jon:"Na⁺",poluprecnik:1.02,koordinacija:"VI",poKoordinaciji:{VI:1.02,VIII:1.18}},K:{jon:"K⁺",poluprecnik:1.38,koordinacija:"VI",poKoordinaciji:{VI:1.38,VIII:1.51}},Ca:{jon:"Ca²⁺",poluprecnik:1,koordinacija:"VI",poKoordinaciji:{VI:1,VIII:1.12}},Mg:{jon:"Mg²⁺",poluprecnik:.72,koordinacija:"VI",poKoordinaciji:{IV:.57,VI:.72,VIII:.89}},Fe:{jon:"Fe²⁺",poluprecnik:.78,koordinacija:"VI-HS",poKoordinaciji:{"VI-HS":.78,"VI-LS":.61,IV:.63}},Al:{jon:"Al³⁺",poluprecnik:.535,koordinacija:"VI",poKoordinaciji:{IV:.39,VI:.535}},Si:{jon:"Si⁴⁺",poluprecnik:.26,koordinacija:"IV",poKoordinaciji:{IV:.26,VI:.4}},Ti:{jon:"Ti⁴⁺",poluprecnik:.61,koordinacija:"VI",poKoordinaciji:{IV:.42,VI:.605}},Mn:{jon:"Mn²⁺",poluprecnik:.83,koordinacija:"VI-HS",poKoordinaciji:{"VI-HS":.83,"VI-LS":.67,IV:.66}},Cu:{jon:"Cu²⁺",poluprecnik:.73,koordinacija:"VI",poKoordinaciji:{IV:.57,VI:.73}},Zn:{jon:"Zn²⁺",poluprecnik:.74,koordinacija:"VI",poKoordinaciji:{IV:.6,VI:.74}},Pb:{jon:"Pb²⁺",poluprecnik:1.19,koordinacija:"VI",poKoordinaciji:{VI:1.19,VIII:1.29}},Ba:{jon:"Ba²⁺",poluprecnik:1.35,koordinacija:"VI",poKoordinaciji:{VI:1.35,VIII:1.42}},Cs:{jon:"Cs⁺",poluprecnik:1.67,koordinacija:"VI",poKoordinaciji:{VI:1.67,VIII:1.74}},O:{jon:"O²⁻",poluprecnik:1.4,koordinacija:"VI",poKoordinaciji:{II:1.35,IV:1.38,VI:1.4}},F:{jon:"F⁻",poluprecnik:1.33,koordinacija:"VI",poKoordinaciji:{II:1.285,IV:1.31,VI:1.33}},Cl:{jon:"Cl⁻",poluprecnik:1.81,koordinacija:"VI",poKoordinaciji:{VI:1.81}},S:{jon:"S²⁻",poluprecnik:1.84,koordinacija:"VI",poKoordinaciji:{VI:1.84}}}},ws={H:{simbol:"H",naziv:"Водоник",bojaHex:"#ffffff",kovalentniPoluprecnik:.31},Li:{simbol:"Li",naziv:"Литијум",bojaHex:"#cc80ff",kovalentniPoluprecnik:1.28},Be:{simbol:"Be",naziv:"Берилијум",bojaHex:"#c2ff00",kovalentniPoluprecnik:.96},B:{simbol:"B",naziv:"Бор",bojaHex:"#ffb5b5",kovalentniPoluprecnik:.84},C:{simbol:"C",naziv:"Угљеник",bojaHex:"#505050",kovalentniPoluprecnik:.76},N:{simbol:"N",naziv:"Азот",bojaHex:"#3050f8",kovalentniPoluprecnik:.71},O:{simbol:"O",naziv:"Кисеоник",bojaHex:"#ff0d0d",kovalentniPoluprecnik:.66},F:{simbol:"F",naziv:"Флуор",bojaHex:"#90e050",kovalentniPoluprecnik:.57},Na:{simbol:"Na",naziv:"Натријум",bojaHex:"#ab5cf2",kovalentniPoluprecnik:1.66},Mg:{simbol:"Mg",naziv:"Магнезијум",bojaHex:"#8aff00",kovalentniPoluprecnik:1.41},Al:{simbol:"Al",naziv:"Алуминијум",bojaHex:"#bfa6a6",kovalentniPoluprecnik:1.21},Si:{simbol:"Si",naziv:"Силицијум",bojaHex:"#f0c8a0",kovalentniPoluprecnik:1.11},P:{simbol:"P",naziv:"Фосфор",bojaHex:"#ff8000",kovalentniPoluprecnik:1.07},S:{simbol:"S",naziv:"Сумпор",bojaHex:"#ffff30",kovalentniPoluprecnik:1.05},Cl:{simbol:"Cl",naziv:"Хлор",bojaHex:"#1ff01f",kovalentniPoluprecnik:1.02},K:{simbol:"K",naziv:"Калијум",bojaHex:"#8f40d4",kovalentniPoluprecnik:2.03},Ca:{simbol:"Ca",naziv:"Калцијум",bojaHex:"#3dff00",kovalentniPoluprecnik:1.76},Ti:{simbol:"Ti",naziv:"Титанијум",bojaHex:"#bfc2c7",kovalentniPoluprecnik:1.6},V:{simbol:"V",naziv:"Ванадијум",bojaHex:"#a6a6ab",kovalentniPoluprecnik:1.53},Cr:{simbol:"Cr",naziv:"Хром",bojaHex:"#8a99c7",kovalentniPoluprecnik:1.39},Mn:{simbol:"Mn",naziv:"Манган",bojaHex:"#9c7ac7",kovalentniPoluprecnik:1.61},Fe:{simbol:"Fe",naziv:"Гвожђе",bojaHex:"#e06633",kovalentniPoluprecnik:1.52},Co:{simbol:"Co",naziv:"Кобалт",bojaHex:"#f090a0",kovalentniPoluprecnik:1.5},Ni:{simbol:"Ni",naziv:"Никл",bojaHex:"#50d050",kovalentniPoluprecnik:1.24},Cu:{simbol:"Cu",naziv:"Бакар",bojaHex:"#c88033",kovalentniPoluprecnik:1.32},Zn:{simbol:"Zn",naziv:"Цинк",bojaHex:"#7d80b0",kovalentniPoluprecnik:1.22},As:{simbol:"As",naziv:"Арсен",bojaHex:"#bd80e3",kovalentniPoluprecnik:1.19},Sr:{simbol:"Sr",naziv:"Стронцијум",bojaHex:"#00ff00",kovalentniPoluprecnik:1.95},Zr:{simbol:"Zr",naziv:"Цирконијум",bojaHex:"#94e0e0",kovalentniPoluprecnik:1.75},Mo:{simbol:"Mo",naziv:"Молибден",bojaHex:"#54b5b5",kovalentniPoluprecnik:1.54},Ag:{simbol:"Ag",naziv:"Сребро",bojaHex:"#c0c0c0",kovalentniPoluprecnik:1.45},Sn:{simbol:"Sn",naziv:"Калај",bojaHex:"#668080",kovalentniPoluprecnik:1.39},Sb:{simbol:"Sb",naziv:"Антимон",bojaHex:"#9e63b5",kovalentniPoluprecnik:1.39},Ba:{simbol:"Ba",naziv:"Баријум",bojaHex:"#00c900",kovalentniPoluprecnik:2.15},W:{simbol:"W",naziv:"Волфрам",bojaHex:"#2194d6",kovalentniPoluprecnik:1.62},Pt:{simbol:"Pt",naziv:"Платина",bojaHex:"#d0d0e0",kovalentniPoluprecnik:1.36},Au:{simbol:"Au",naziv:"Злато",bojaHex:"#ffd123",kovalentniPoluprecnik:1.36},Hg:{simbol:"Hg",naziv:"Жива",bojaHex:"#b8b8d0",kovalentniPoluprecnik:1.32},Pb:{simbol:"Pb",naziv:"Олово",bojaHex:"#575961",kovalentniPoluprecnik:1.46},Bi:{simbol:"Bi",naziv:"Бизмут",bojaHex:"#9e4fb5",kovalentniPoluprecnik:1.48}},Om={simbol:"?",naziv:"Непознат елемент",bojaHex:"#ff1493",kovalentniPoluprecnik:1.2};function Ws(n){const e=n.trim().replace(/[^A-Za-z]/g,"");if(!e)return"?";const t=e[0].toUpperCase(),i=e.length>1?e[1].toLowerCase():"",a=t+i;return a in ws?a:t in ws?t:a}function Rs(n){const e=Ws(n);return ws[e]??{...Om,simbol:e}}function dc(n,e="jonski",t){const i=Ws(n),a=Rs(i);if(e==="jonski"){const r=As.vrednosti[i];if(r)return{poluprecnik:r.poluprecnik,koriscenaVrsta:"jonski",jon:r.jon}}return{poluprecnik:a.kovalentniPoluprecnik,koriscenaVrsta:"kovalentni"}}class Xn extends Error{constructor(e){super(e),this.name="CifGreska"}}function ln(n,e){const t=n.trim().replace(/\([0-9]+\)$/,""),i=Number(t);if(!Number.isFinite(i))throw new Xn(`Неисправна нумеричка вредност у CIF пољу ${e}: "${n}"`);return i}function Ca(n){const e=[];let t=0;const i=n.length;for(;t<i;){for(;t<i&&/\s/.test(n[t]);)t++;if(t>=i)break;const a=n[t];if(a==="#")break;if(a==="'"||a==='"'){const r=a;t++;let s=t;for(;t<i&&!(n[t]===r&&(t+1>=i||/\s/.test(n[t+1])));)t++;e.push(n.slice(s,t)),t<i&&n[t]===r&&t++}else{const r=t;for(;t<i&&!/\s/.test(n[t]);)t++;e.push(n.slice(r,t))}}return e}function Bm(n){if(!n||!n.trim())throw new Xn("CIF садржај је празан.");const e=n.split(/\r?\n/);let t="struktura";const i=new Map,a=[];let r=0;for(;r<e.length;){const m=e[r].trim();if(!m||m.startsWith("#")){r++;continue}if(m.toLowerCase().startsWith("data_")){t=m.slice(5).trim()||t,r++;continue}if(m.toLowerCase()==="loop_"){r++;const g=[];for(;r<e.length;){const T=e[r].trim();if(!T||T.startsWith("#")){r++;continue}if(T.startsWith("_")){const y=Ca(T);y[0]&&g.push(y[0].toLowerCase()),r++}else break}const _=g.indexOf("_atom_site_label"),p=g.indexOf("_atom_site_type_symbol"),d=g.indexOf("_atom_site_fract_x"),E=g.indexOf("_atom_site_fract_y"),S=g.indexOf("_atom_site_fract_z"),x=_!==-1&&p!==-1&&d!==-1&&E!==-1&&S!==-1;for(;r<e.length;){const T=e[r].trim();if(!T||T.startsWith("#")){r++;continue}const y=T.toLowerCase();if(T.startsWith("_")||y==="loop_"||y.startsWith("data_")||T.startsWith(";"))break;if(x&&g.length>0){const w=Ca(T);if(w.length<g.length)throw new Xn("Непотпун ред у _atom_site табели CIF фајла.");const D=w[_],M=w[p],v=ln(w[d],"_atom_site_fract_x"),R=ln(w[E],"_atom_site_fract_y"),U=ln(w[S],"_atom_site_fract_z");a.push({oznaka:D,simbol:Ws(M),fx:v,fy:R,fz:U})}r++}continue}if(m.startsWith("_")){const g=Ca(m);if(g.length>=2&&g[0]&&g[1]!==void 0)i.set(g[0].toLowerCase(),g[1]);else if(g.length===1&&g[0]&&r+1<e.length){const _=Ca(e[r+1].trim());_[0]&&!_[0].startsWith("_")&&_[0].toLowerCase()!=="loop_"&&(i.set(g[0].toLowerCase(),_[0]),r++)}}r++}const s=["_cell_length_a","_cell_length_b","_cell_length_c","_cell_angle_alpha","_cell_angle_beta","_cell_angle_gamma"];for(const m of s)if(!i.has(m))throw new Xn(`Недостаје обавезно CIF поље: ${m}`);const o=ln(i.get("_cell_length_a"),"_cell_length_a"),c=ln(i.get("_cell_length_b"),"_cell_length_b"),l=ln(i.get("_cell_length_c"),"_cell_length_c"),u=ln(i.get("_cell_angle_alpha"),"_cell_angle_alpha"),h=ln(i.get("_cell_angle_beta"),"_cell_angle_beta"),f=ln(i.get("_cell_angle_gamma"),"_cell_angle_gamma");if(o<=0||c<=0||l<=0)throw new Xn("Димензије јединичне ћелије a, b, c морају бити позитивне.");if(u<=0||u>=180||h<=0||h>=180||f<=0||f>=180||u+h+f>=360)throw new Xn("Углови јединичне ћелије α, β, γ нису физички валидни.");if(a.length===0)throw new Xn("CIF не садржи ниједан атом у loop_ _atom_site блоку.");return{nazivBloka:t,celija:{a:o,b:c,c:l,alpha:u,beta:h,gamma:f},atomi:a}}function Xs(n){const e=Math.PI/180,t=n.alpha*e,i=n.beta*e,a=n.gamma*e,r=Math.cos(t),s=Math.cos(i),o=Math.cos(a),c=Math.sin(a),l=n.a,u=0,h=n.b*o,f=n.b*c,m=0,g=n.c*s,_=n.c*(r-s*o)/c,p=Math.max(0,n.c*n.c-g*g-_*_),d=Math.sqrt(p);return{va:[l,u,-0],vb:[h,m,-f],vc:[g,d,-_]}}function Pn(n,e,t,i){return[n*i.va[0]+e*i.vb[0]+t*i.vc[0],n*i.va[1]+e*i.vb[1]+t*i.vc[1],n*i.va[2]+e*i.vb[2]+t*i.vc[2]]}const Ir=[{kljuc:"kubna-P",naziv:"Кубна примитивна (P)",sistem:"Кубни",centriranje:"P",brojCvorova:1,celija:{a:1.8,b:1.8,c:1.8,alpha:90,beta:90,gamma:90},cvoroviFrakcioni:[[0,0,0]]},{kljuc:"kubna-I",naziv:"Кубна просторно центрирана (I)",sistem:"Кубни",centriranje:"I",brojCvorova:2,celija:{a:1.8,b:1.8,c:1.8,alpha:90,beta:90,gamma:90},cvoroviFrakcioni:[[0,0,0],[.5,.5,.5]],primitivniVektori:[[-.5,.5,.5],[.5,-.5,.5],[.5,.5,-.5]]},{kljuc:"kubna-F",naziv:"Кубна површински центрирана (F)",sistem:"Кубни",centriranje:"F",brojCvorova:4,celija:{a:1.8,b:1.8,c:1.8,alpha:90,beta:90,gamma:90},cvoroviFrakcioni:[[0,0,0],[0,.5,.5],[.5,0,.5],[.5,.5,0]],primitivniVektori:[[0,.5,.5],[.5,0,.5],[.5,.5,0]]},{kljuc:"tetragonalna-P",naziv:"Тетрагонална примитивна (P)",sistem:"Тетрагонални",centriranje:"P",brojCvorova:1,celija:{a:1.6,b:1.6,c:2.3,alpha:90,beta:90,gamma:90},cvoroviFrakcioni:[[0,0,0]]},{kljuc:"tetragonalna-I",naziv:"Тетрагонална просторно центрирана (I)",sistem:"Тетрагонални",centriranje:"I",brojCvorova:2,celija:{a:1.6,b:1.6,c:2.3,alpha:90,beta:90,gamma:90},cvoroviFrakcioni:[[0,0,0],[.5,.5,.5]],primitivniVektori:[[-.5,.5,.5],[.5,-.5,.5],[.5,.5,-.5]]},{kljuc:"ortorombicna-P",naziv:"Орторомбична примитивна (P)",sistem:"Орторомбични",centriranje:"P",brojCvorova:1,celija:{a:1.4,b:1.9,c:2.4,alpha:90,beta:90,gamma:90},cvoroviFrakcioni:[[0,0,0]]},{kljuc:"ortorombicna-C",naziv:"Орторомбична базно центрирана (C)",sistem:"Орторомбични",centriranje:"C",brojCvorova:2,celija:{a:1.4,b:1.9,c:2.4,alpha:90,beta:90,gamma:90},cvoroviFrakcioni:[[0,0,0],[.5,.5,0]],primitivniVektori:[[.5,.5,0],[-.5,.5,0],[0,0,1]]},{kljuc:"ortorombicna-I",naziv:"Орторомбична просторно центрирана (I)",sistem:"Орторомбични",centriranje:"I",brojCvorova:2,celija:{a:1.4,b:1.9,c:2.4,alpha:90,beta:90,gamma:90},cvoroviFrakcioni:[[0,0,0],[.5,.5,.5]],primitivniVektori:[[-.5,.5,.5],[.5,-.5,.5],[.5,.5,-.5]]},{kljuc:"ortorombicna-F",naziv:"Орторомбична површински центрирана (F)",sistem:"Орторомбични",centriranje:"F",brojCvorova:4,celija:{a:1.4,b:1.9,c:2.4,alpha:90,beta:90,gamma:90},cvoroviFrakcioni:[[0,0,0],[0,.5,.5],[.5,0,.5],[.5,.5,0]],primitivniVektori:[[0,.5,.5],[.5,0,.5],[.5,.5,0]]},{kljuc:"heksagonalna-P",naziv:"Хексагонална примитивна (P)",sistem:"Хексагонални",centriranje:"P",brojCvorova:1,celija:{a:1.8,b:1.8,c:2.2,alpha:90,beta:90,gamma:120},cvoroviFrakcioni:[[0,0,0]]},{kljuc:"romboedarska-R",naziv:"Ромбоедарска (R, хексагонална поставка)",sistem:"Тригонални",centriranje:"R",brojCvorova:3,celija:{a:1.8,b:1.8,c:2.5,alpha:90,beta:90,gamma:120},cvoroviFrakcioni:[[0,0,0],[2/3,1/3,1/3],[1/3,2/3,2/3]],primitivniVektori:[[2/3,1/3,1/3],[-1/3,1/3,1/3],[-1/3,-2/3,1/3]]},{kljuc:"monoklinicna-P",naziv:"Моноклинична примитивна (P)",sistem:"Моноклинични",centriranje:"P",brojCvorova:1,celija:{a:1.5,b:1.8,c:2.1,alpha:90,beta:110,gamma:90},cvoroviFrakcioni:[[0,0,0]]},{kljuc:"monoklinicna-C",naziv:"Моноклинична базно центрирана (C)",sistem:"Моноклинични",centriranje:"C",brojCvorova:2,celija:{a:1.5,b:1.8,c:2.1,alpha:90,beta:110,gamma:90},cvoroviFrakcioni:[[0,0,0],[.5,.5,0]],primitivniVektori:[[.5,.5,0],[-.5,.5,0],[0,0,1]]},{kljuc:"triklinicna-P",naziv:"Триклинична примитивна (P)",sistem:"Триклинични",centriranje:"P",brojCvorova:1,celija:{a:1.4,b:1.7,c:2.1,alpha:78,beta:108,gamma:102},cvoroviFrakcioni:[[0,0,0]]}],Vm={imaPodrazumevanuAnimaciju(){return!0},pocetnaKamera(){return{theta:.65,phi:1.15,udaljenost:6.8}},kreiraj(n,e){let t=e.resetka==="sve"?"kubna-P":e.resetka;const i=new it;n.scena3D.add(i);const a=new vn(.08,16,16),r=new ct({color:new ce(n.tema.token("--primary")),roughness:.25,metalness:.2}),s=new ct({color:new ce(n.tema.token("--accent")),roughness:.25,metalness:.2}),o=new ht({color:new ce(n.tema.token("--text-secondary")),linewidth:2}),c=new Vu({color:new ce(n.tema.token("--border-color")),dashSize:.15,gapSize:.1}),l=new ht({color:new ce(n.tema.token("--warning")),linewidth:2});function u(p){for(;i.children.length>0;){const U=i.children[0];i.remove(U),Ut(U)}const d=Xs(p.celija),E=new F(...d.va),S=new F(...d.vb),x=new F(...d.vc),y=E.clone().add(S).add(x).multiplyScalar(.5).clone().negate(),w=[[0,0,0],[1,0,0],[1,1,0],[0,1,0],[0,0,1],[1,0,1],[1,1,1],[0,1,1]].map(([U,C,P])=>{const[N,k,O]=Pn(U,C,P,d);return new F(N,k,O).add(y)}),D=[[0,1],[1,2],[2,3],[3,0],[4,5],[5,6],[6,7],[7,4],[0,4],[1,5],[2,6],[3,7]],M=[];for(const U of D){const C=w[U[0]],P=w[U[1]];M.push(C.x,C.y,C.z,P.x,P.y,P.z)}const v=new $e;v.setAttribute("position",new He(M,3)),i.add(new gt(v,o));const R=new Set;for(const[U,C,P]of p.cvoroviFrakcioni)for(let N=0;N<=1;N++)for(let k=0;k<=1;k++)for(let O=0;O<=1;O++){const z=U+N,H=C+k,$=P+O;if(z>=-1e-4&&z<=1.0001&&H>=-1e-4&&H<=1.0001&&$>=-1e-4&&$<=1.0001){const Y=`${z.toFixed(2)},${H.toFixed(2)},${$.toFixed(2)}`;if(R.has(Y))continue;R.add(Y);const[fe,Ie,X]=Pn(z,H,$,d),ne=new F(fe,Ie,X).add(y),ue=(N===0||N===1)&&(k===0||k===1)&&(O===0||O===1)&&U===0&&C===0&&P===0,se=new Ge(a,ue?r:s);se.position.copy(ne),i.add(se)}}if(e.prikazi_susedne_celije){const U=[];for(const N of[-1,0,1])for(const k of[-1,0,1])for(const O of[-1,0,1]){if(N===0&&k===0&&O===0)continue;const z=E.clone().multiplyScalar(N).add(S.clone().multiplyScalar(k)).add(x.clone().multiplyScalar(O));for(const H of D){const $=w[H[0]].clone().add(z),Y=w[H[1]].clone().add(z);U.push($.x,$.y,$.z,Y.x,Y.y,Y.z)}}const C=new $e;C.setAttribute("position",new He(U,3));const P=new gt(C,c);P.computeLineDistances(),i.add(P)}if(e.prikazi_primitivnu_celiju&&p.primitivniVektori){const U=[],C=w[0],P=p.primitivniVektori.map(([$,Y,fe])=>{const[Ie,X,ne]=Pn($,Y,fe,d);return new F(Ie,X,ne)}),N=P[0],k=P[1],O=P[2],z=[C,C.clone().add(N),C.clone().add(N).add(k),C.clone().add(k),C.clone().add(O),C.clone().add(N).add(O),C.clone().add(N).add(k).add(O),C.clone().add(k).add(O)];for(const $ of D){const Y=z[$[0]],fe=z[$[1]];U.push(Y.x,Y.y,Y.z,fe.x,fe.y,fe.z)}const H=new $e;H.setAttribute("position",new He(U,3)),i.add(new gt(H,l))}}const h=document.createElement("div");h.className="udzbenik-scena-status",n.podnozje.append(h);function f(p){h.textContent=`${p.naziv} • Систем: ${p.sistem} • Чворова по конвенционалној ћелији: ${p.brojCvorova}`}if(e.resetka==="sve"){const p=document.createElement("div");p.className="udzbenik-bravais-traka",p.style.display="flex",p.style.flexWrap="wrap",p.style.gap="4px";for(const d of Ir){const E=document.createElement("button");E.type="button",E.className="udzbenik-dugme udzbenik-dugme--malo",d.kljuc===t&&E.classList.add("udzbenik-dugme--aktivno"),E.textContent=d.kljuc,E.setAttribute("aria-label",d.naziv),E.addEventListener("click",()=>{t=d.kljuc,p.querySelectorAll("button").forEach(S=>S.classList.remove("udzbenik-dugme--aktivno")),E.classList.add("udzbenik-dugme--aktivno"),u(d),f(d)}),p.append(E)}n.gornjeKontrole.append(p)}const m=Ir.find(p=>p.kljuc===t)??Ir[0];u(m),f(m);function g(){r.color.set(n.tema.token("--primary")),s.color.set(n.tema.token("--accent")),o.color.set(n.tema.token("--text-secondary")),c.color.set(n.tema.token("--border-color")),l.color.set(n.tema.token("--warning"))}let _=0;return{azuriraj(p){_+=p*.45,i.rotation.y=_},korak(){_+=.25,i.rotation.y=_},resetuj(){_=0,i.rotation.set(0,0,0)},osveziTemu(){g()},raspolazi(){a.dispose(),r.dispose(),s.dispose(),o.dispose(),c.dispose(),l.dispose(),Ut(i),h.remove()}}}},jm=[[0,1,2],[0,2,1],[1,0,2],[1,2,0],[2,0,1],[2,1,0]],Hm=[[1,1,1],[1,1,-1],[1,-1,1],[1,-1,-1],[-1,1,1],[-1,1,-1],[-1,-1,1],[-1,-1,-1]];function Ot(n){return n<0?`${Math.abs(n)}̄`:String(n)}function Gm(n){const e=Math.abs(n[0])>=10||Math.abs(n[1])>=10||Math.abs(n[2])>=10;return`(${[Ot(n[0]),Ot(n[1]),Ot(n[2])].join(e?" ":"")})`}function Wm(n){const e=Math.abs(n[0])>=10||Math.abs(n[1])>=10||Math.abs(n[2])>=10;return`{${[Ot(n[0]),Ot(n[1]),Ot(n[2])].join(e?" ":"")}}`}function hc(n){const[e,t,i]=n;if(!Number.isFinite(e)||!Number.isFinite(t)||!Number.isFinite(i))throw new Error("Милерови индекси морају бити коначни бројеви.");if(e===0&&t===0&&i===0)throw new Error("Милерови индекси не могу бити (000).");const a=new Set,r=[],s=[Math.trunc(e),Math.trunc(t),Math.trunc(i)];for(const[o,c,l]of jm){const u=s[o],h=s[c],f=s[l];for(const[m,g,_]of Hm){const p=u===0?0:u*m,d=h===0?0:h*g,E=f===0?0:f*_,S=`${p},${d},${E}`;if(a.has(S))continue;a.add(S);const x=Math.hypot(p,d,E),T=[p,d,E];r.push({hkl:T,normala:[p/x,d/x,E/x],oznaka:Gm(T)})}}return r}function Xm(n,e){const t=e??56,i=Math.round((180-t)*10)/10;switch(n){case"kubna":return{naziv:"Кубна цепљивост {100}",brojPravaca:"3 правца",uglovi:"90°",podrazumevaniPrimer:"халит, галенит"};case"oktaedarska":return{naziv:"Октаедарска цепљивост {111}",brojPravaca:"4 правца",uglovi:"70,5° и 109,5°",podrazumevaniPrimer:"флуорит, дијамант"};case"dodekaedarska":return{naziv:"Додекаедарска цепљивост {110}",brojPravaca:"6 праваца",uglovi:"60°, 90° и 120°",podrazumevaniPrimer:"сфалерит"};case"romboedarska":return{naziv:"Ромбоедарска цепљивост {101̄1}",brojPravaca:"3 правца",uglovi:"~75° и ~105° (≠ 90°)",podrazumevaniPrimer:"калцит, доломит"};case"bazalna":return{naziv:"Базална (пинакоидална) цепљивост {001}",brojPravaca:"1 правац",uglovi:"паралелне ламеле (0°)",podrazumevaniPrimer:"лискун (мусковит), графит"};case"prizmatska":return{naziv:"Призматска цепљивост {110}",brojPravaca:"2 правца",uglovi:`${t}° и ${i}°`,podrazumevaniPrimer:t>75?"пироксен":"амфибол"};case"nema":return{naziv:"Нема цепљивости (шкољкаст прелом)",brojPravaca:"0 праваца",uglovi:"нема равни цепљивости",podrazumevaniPrimer:"кварц"}}}function Kn(n,e,t,i){const a=qi(n);if(a.pljosni.length<4||a.temena.length<4)return null;const r=$i(a),s=new it;return s.add(new Ge(r.geometrijaMreze,t),new gt(r.geometrijaIvica,i)),{grupa:s,smerRazdvajanja:e}}function un(n,e,t,i,a){const r=new zi(t,t),s=new Ge(r,i),o=new gt(new Ha(r),a),c=new it;c.add(s,o);const l=new F(...n).normalize();return c.quaternion.setFromUnitVectors(new F(0,0,1),l),c.position.copy(l).multiplyScalar(e),c}function vi(n,e){const t=Math.hypot(n-.35,e-.25),i=.055*Math.sin(t*13.5);return .28*(n*n-.5*e*e)+.18*n+i}function Km(n,e,t,i){if(!n){const h=[{normala:[0,-1,0],d:1.15}];for(let m=0;m<6;m++){const g=m*Math.PI/3,_=Math.cos(g),p=Math.sin(g);h.push({normala:[_,0,p],d:.95}),h.push({normala:[_*.72,.69,p*.72],d:1.28}),h.push({normala:[_*.72,-.69,p*.72],d:1.28})}const f=Kn(h,new F(0,0,0),e,i);return{fragmenti:f?[f]:[]}}const o=12,c=24;function l(h,f){const m=(f%(Math.PI/3)+Math.PI/3)%(Math.PI/3)-Math.PI/6,g=.95*Math.cos(Math.PI/6)/Math.cos(m);return[h*g*Math.cos(f),h*g*Math.sin(f)]}function u(h){const f=[],m=[],g=[],_=h?1.15:-1.15,p=h?1.85:-1.85;for(let T=0;T<o;T++){const y=T/o,w=(T+1)/o;for(let D=0;D<c;D++){const M=D/c*Math.PI*2,v=(D+1)/c*Math.PI*2,[R,U]=l(y,M),[C,P]=l(w,M),[N,k]=l(w,v),[O,z]=l(y,v),H=vi(R,U),$=vi(C,P),Y=vi(N,k),fe=vi(O,z);h?m.push(R,H,U,N,Y,k,C,$,P,R,H,U,O,fe,z,N,Y,k):m.push(R,H,U,C,$,P,N,Y,k,R,H,U,N,Y,k,O,fe,z)}}for(let T=0;T<c;T++){const y=T/c*Math.PI*2,w=(T+1)/c*Math.PI*2,[D,M]=l(1,y),[v,R]=l(1,w),U=vi(D,M),C=vi(v,R);h?(f.push(D,U,M,v,C,R,v,_,R,D,U,M,v,_,R,D,_,M),f.push(D,_,M,v,_,R,0,p,0)):(f.push(D,_,M,v,_,R,v,C,R,D,_,M,v,C,R,D,U,M),f.push(v,_,R,D,_,M,0,p,0)),g.push(D,U,M,v,C,R),g.push(D,_,M,v,_,R),T%(c/6)===0&&(g.push(D,U,M,D,_,M),g.push(D,_,M,0,p,0))}const d=new $e;d.setAttribute("position",new He(f,3)),d.computeVertexNormals();const E=new $e;E.setAttribute("position",new He(m,3)),E.computeVertexNormals();const S=new $e;S.setAttribute("position",new He(g,3));const x=new it;return x.add(new Ge(d,e),new Ge(E,t),new gt(S,i)),x}return{fragmenti:[{grupa:u(!0),smerRazdvajanja:new F(.18,.55,.1)},{grupa:u(!1),smerRazdvajanja:new F(-.18,-.55,-.1)}]}}const qm={imaPodrazumevanuAnimaciju(n){return!(n.vrsta==="nema"&&!n.prikazi_prelom)},pocetnaKamera(){return{theta:.68,phi:1.14,udaljenost:5.9}},kreiraj(n,e){const t=e.vrsta,i=e.ugao??56,a=e.prikazi_prelom??!1,r=new it,s=new it,o=new it;r.add(s,o),n.scena3D.add(r);const c=new ct({color:new ce(n.tema.token("--primary")),transparent:!0,opacity:.86,roughness:.32,metalness:.08,flatShading:!0}),l=new ct({color:new ce(n.tema.token("--accent")),roughness:.22,metalness:.15,side:mt}),u=new ht({color:new ce(n.tema.token("--text-primary"))}),h=new Ui({color:new ce(n.tema.token("--accent")),transparent:!0,opacity:.26,side:mt,depthWrite:!1}),f=new ht({color:new ce(n.tema.token("--accent"))}),m=[];function g(){if(t==="kubna"){const T=[-1,1];for(const y of T)for(const w of T)for(const D of T){const M=[{normala:[y,0,0],d:1.05},{normala:[-y,0,0],d:0},{normala:[0,w,0],d:1.05},{normala:[0,-w,0],d:0},{normala:[0,0,D],d:1.05},{normala:[0,0,-D],d:0}],v=Kn(M,new F(y,w,D).normalize().multiplyScalar(.52),c,u);v&&m.push(v)}o.add(un([1,0,0],0,2.6,h,f),un([0,1,0],0,2.6,h,f),un([0,0,1],0,2.6,h,f))}else if(t==="oktaedarska"){const T=hc([1,1,1]).map(w=>({normala:w.normala,d:1.08})),y=[[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]];for(let w=0;w<16;w++){const D=[...T],M=new F;for(let R=0;R<4;R++){const U=(w&1<<R)!==0?1:-1,C=y[R];D.push({normala:[C[0]*U,C[1]*U,C[2]*U],d:0}),M.add(new F(C[0]*U,C[1]*U,C[2]*U))}const v=Kn(D,M.lengthSq()>1e-4?M.normalize().multiplyScalar(.52):M,c,u);v&&m.push(v)}for(const w of y)o.add(un(w,0,2.8,h,f))}else if(t==="dodekaedarska"){const T=hc([1,1,0]).map(D=>({normala:D.normala,d:1.12})),y=[[1,1,0],[1,-1,0],[1,0,1],[1,0,-1],[0,1,1],[0,1,-1]];for(const D of y)o.add(un(D,0,2.7,h,f));const w=[[1,1,0],[1,-1,0],[0,1,1]];for(let D=0;D<8;D++){const M=[...T],v=new F;for(let U=0;U<3;U++){const C=(D&1<<U)!==0?1:-1,P=w[U];M.push({normala:[P[0]*C,P[1]*C,P[2]*C],d:0}),v.add(new F(P[0]*C,P[1]*C,P[2]*C))}const R=Kn(M,v.normalize().multiplyScalar(.5),c,u);R&&m.push(R)}}else if(t==="romboedarska"){const T=[1,.26,.14],y=[.24,1,.22],w=[.18,.26,1],D=[T,y,w],M=[];for(const R of D)M.push({normala:R,d:1}),M.push({normala:[-R[0],-R[1],-R[2]],d:1}),o.add(un(R,0,2.8,h,f));const v=[-1,1];for(const R of v)for(const U of v)for(const C of v){const P=[...M,{normala:[-T[0]*R,-T[1]*R,-T[2]*R],d:0},{normala:[-y[0]*U,-y[1]*U,-y[2]*U],d:0},{normala:[-w[0]*C,-w[1]*C,-w[2]*C],d:0}],N=new F(T[0]*R+y[0]*U+w[0]*C,T[1]*R+y[1]*U+w[1]*C,T[2]*R+y[2]*U+w[2]*C).normalize().multiplyScalar(.5),k=Kn(P,N,c,u);k&&m.push(k)}}else if(t==="bazalna"){const T=[];for(let M=0;M<6;M++){const v=M*Math.PI/3;T.push({normala:[Math.cos(v),0,Math.sin(v)],d:1.15})}const y=5,w=1.1,D=w/y;for(let M=0;M<y;M++){const v=-w/2+M*D,R=v+D,U=[...T,{normala:[0,1,0],d:R},{normala:[0,-1,0],d:-v}],C=M-(y-1)/2,P=Kn(U,new F(C*.08,C*.28,0),c,u);P&&m.push(P),M>0&&o.add(un([0,1,0],v,2.7,h,f))}}else if(t==="prizmatska"){const T=i*Math.PI/180*.5,y=[Math.sin(T),0,Math.cos(T)],w=[-Math.sin(T),0,Math.cos(T)],D=[{normala:[0,1,0],d:1.3},{normala:[0,-1,0],d:1.3},{normala:y,d:.9},{normala:[-y[0],0,-y[2]],d:.9},{normala:w,d:.9},{normala:[-w[0],0,-w[2]],d:.9}];o.add(un(y,0,2.9,h,f),un(w,0,2.9,h,f));const M=[-1,1];for(const v of M)for(const R of M){const U=[...D,{normala:[-y[0]*v,0,-y[2]*v],d:0},{normala:[-w[0]*R,0,-w[2]*R],d:0}],C=new F(y[0]*v+w[0]*R,0,y[2]*v+w[2]*R).normalize().multiplyScalar(.48),P=Kn(U,C,c,u);P&&m.push(P)}}else{const T=Km(a,c,l,u);m.push(...T.fragmenti)}for(const T of m)s.add(T.grupa)}g();const _=Xm(t,i),p=e.primer||_.podrazumevaniPrimer,d=document.createElement("div");d.className="udzbenik-scena-info-red udzbenik-cepljivost-meta";const E=[[We("brojPravacaCepljivosti"),_.brojPravaca],[We("ugloviCepljivosti"),_.uglovi],[We("primerMinerala"),p]];for(const[T,y]of E){const w=document.createElement("span");w.className="udzbenik-meta-stavka";const D=document.createElement("strong");D.textContent=`${T}: `;const M=document.createElement("span");M.textContent=y,w.append(D,M),d.append(w)}n.podnozje.append(d);let S=n.smanjenPokret?.72:0;function x(){if(t==="nema"&&!a){o.visible=!1;return}let T=0,y=0;if(S<.3)T=S/.3,y=0;else if(S<.72){T=1;const w=(S-.3)/.42;y=w*w*(3-2*w)}else if(S<.85)T=1,y=1;else{const w=(S-.85)/.15;T=1-w,y=1-w*w*(3-2*w)}o.visible=t!=="nema"&&T>.02,o.scale.setScalar(.25+.75*T),h.opacity=.26*T*(1-.45*y);for(const w of m)w.grupa.position.copy(w.smerRazdvajanja).multiplyScalar(y)}return x(),{azuriraj(T){S=(S+T*.17)%1,r.rotation.y+=T*.24,x()},korak(){S=(S+.18)%1,x()},resetuj(){r.rotation.set(0,0,0),S=n.smanjenPokret?.72:0,x()},osveziTemu(T){c.color.set(T.token("--primary")),l.color.set(T.token("--accent")),u.color.set(T.token("--text-primary")),h.color.set(T.token("--accent")),f.color.set(T.token("--accent"))},raspolazi(){Ut(r),c.dispose(),l.dispose(),u.dispose(),h.dispose(),f.dispose()}}}};function $m(n){if(n.length===4){const[e,t,i,a]=n;if(i!==-(e+t))throw new Error(`Неисправни Браве-Милерови индекси (${e} ${t} ${i} ${a}): мора важити i = -(h+k), добијено i=${i}, -(h+k)=${-(e+t)}.`);return[e,t,a]}return n}function Ym(n,e=!1){if(e){const[a,r,s]=n,o=-(a+r),c=Math.abs(a)>=10||Math.abs(r)>=10||Math.abs(o)>=10||Math.abs(s)>=10;return`(${[Ot(a),Ot(r),Ot(o),Ot(s)].join(c?" ":"")})`}const t=Math.abs(n[0])>=10||Math.abs(n[1])>=10||Math.abs(n[2])>=10;return`(${[Ot(n[0]),Ot(n[1]),Ot(n[2])].join(t?" ":"")})`}function Zm(n,e,t){const i=t?.a??1,a=t?.b??i,r=t?.c??i;let s=0,o=0,c=0;if(e==="heksagonalni"||e==="trigonalni")s=n[0]/i,o=(n[0]+2*n[1])/(i*Math.sqrt(3)),c=n[2]/r;else if(e==="monoklinicni"&&t?.beta!==void 0&&Math.abs(t.beta-90)>.01){const u=t.beta*Math.PI/180,h=Math.sin(u),f=Math.cos(u);s=n[0]/(i*h)-n[2]*f/(r*h),o=n[1]/a,c=n[2]/r}else s=n[0]/i,o=n[1]/a,c=n[2]/r;const l=Math.hypot(s,o,c);if(l<1e-12)throw new Error("Милерови индекси не могу дати нулти вектор нормале.");return[s/l,o/l,c/l]}const Jm=[[0,1,2],[0,2,1],[1,0,2],[1,2,0],[2,0,1],[2,1,0]],tl=[[1,1,1],[1,1,-1],[1,-1,1],[1,-1,-1],[-1,1,1],[-1,1,-1],[-1,-1,1],[-1,-1,-1]];function fc(n){const e=new Set,t=[];for(const[i,a,r]of Jm)for(const[s,o,c]of tl){const l=[n[i]===0?0:n[i]*s,n[a]===0?0:n[a]*o,n[r]===0?0:n[r]*c],u=l.join(",");e.has(u)||(e.add(u),t.push(l))}return t}const Ks=[[0,1,2],[1,2,0],[2,0,1]];function Qm(n){const e=new Set,t=[];for(const[i,a,r]of Ks)for(const[s,o,c]of tl){const l=[n[i]===0?0:n[i]*s,n[a]===0?0:n[a]*o,n[r]===0?0:n[r]*c],u=l.join(",");e.has(u)||(e.add(u),t.push(l))}return t}const Cs=[[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]],nl=[[1,0,2],[0,2,1],[2,1,0]];function e0(n){const e=new Set,t=[];for(const[i,a,r]of Ks)for(const[s,o,c]of Cs){const l=[n[i]===0?0:n[i]*s,n[a]===0?0:n[a]*o,n[r]===0?0:n[r]*c],u=l.join(",");e.has(u)||(e.add(u),t.push(l))}for(const[i,a,r]of nl)for(const[s,o,c]of Cs){const l=[n[i]===0?0:n[i]*s,n[a]===0?0:n[a]*o,n[r]===0?0:n[r]*c],u=l.join(",");e.has(u)||(e.add(u),t.push(l))}return t}const t0=[[-1,-1,-1],[-1,1,1],[1,-1,1],[1,1,-1]];function n0(n){const e=new Set,t=[];for(const[i,a,r]of Ks)for(const[s,o,c]of Cs){const l=[n[i]===0?0:n[i]*s,n[a]===0?0:n[a]*o,n[r]===0?0:n[r]*c],u=l.join(",");e.has(u)||(e.add(u),t.push(l))}for(const[i,a,r]of nl)for(const[s,o,c]of t0){const l=[n[i]===0?0:n[i]*s,n[a]===0?0:n[a]*o,n[r]===0?0:n[r]*c],u=l.join(",");e.has(u)||(e.add(u),t.push(l))}return t}function i0(n){const e=new Set,t=[],i=[[n[0],n[1]],[n[1],n[0]]];for(const a of i){const r=a[0],s=a[1];for(const o of[1,-1])for(const c of[1,-1])for(const l of[1,-1]){const u=[r===0?0:r*o,s===0?0:s*c,n[2]===0?0:n[2]*l],h=u.join(",");e.has(h)||(e.add(h),t.push(u))}}return t}function a0(n){const e=new Set,t=[];for(const i of[1,-1])for(const a of[1,-1])for(const r of[1,-1]){const s=[n[0]===0?0:n[0]*i,n[1]===0?0:n[1]*a,n[2]===0?0:n[2]*r],o=s.join(",");e.has(o)||(e.add(o),t.push(s))}return t}function r0(n){const e=n[0],t=n[1],i=-(e+t),a=n[2],r=[[e,t],[-i,-e],[t,i],[-e,-t],[i,e],[-t,-i]],s=new Set,o=[];for(const c of r){const l=c[0],u=c[1],h=[[l,u],[u,l]];for(const f of h){const m=f[0],g=f[1];for(const _ of[1,-1]){const p=[m,g,a===0?0:a*_],d=p.join(",");s.has(d)||(s.add(d),o.push(p))}}}return o}function s0(n){const e=n[0],t=n[1],i=-(e+t),a=n[2],r=[[e,t],[-i,-e],[t,i],[-e,-t],[i,e],[-t,-i]],s=new Set,o=[];for(const c of r){const l=c[0],u=c[1];for(const h of[1,-1]){const f=[l,u,a===0?0:a*h],m=f.join(",");s.has(m)||(s.add(m),o.push(f))}}return o}function o0(n){const e=n[0],t=n[1],i=-(e+t),a=n[2],r=[[e,t],[i,e],[t,i]],s=new Set,o=[];for(const c of r){const l=c[0],u=c[1],h=[[l,u,a],[u,l,-a],[-l,-u,-a],[-u,-l,a]];for(const f of h){const m=f[0],g=f[1],_=f[2],p=[m,g,_===0?0:_],d=p.join(",");s.has(d)||(s.add(d),o.push(p))}}return o}function c0(n){const e=n[0],t=n[1],i=-(e+t),a=n[2],r=new Set,s=[],o=[[e,t,a],[i,e,a],[t,i,a],[e,i,-a],[t,e,-a],[i,t,-a]];for(const c of o){const l=c.join(",");r.has(l)||(r.add(l),s.push(c))}return s}function l0(n){const[e,t,i]=n,a=new Set,r=[],s=[[e,t,i],[-e,t,-i],[e,-t,i],[-e,-t,-i]];for(const o of s){const c=o.join(",");a.has(c)||(a.add(c),r.push(o))}return r}function il(n){switch(n){case"kubni":return"m-3m";case"tetragonalni":return"4/mmm";case"heksagonalni":return"6/mmm";case"trigonalni":return"-3m";case"ortorombicni":return"mmm";case"monoklinicni":return"2/m";default:return"m-3m"}}function Dt(n,e,t,i){const a=$m(n),[r,s,o]=a;if(!Number.isFinite(r)||!Number.isFinite(s)||!Number.isFinite(o))throw new Error("Милерови индекси морају бити коначни бројеви.");if(r===0&&s===0&&o===0)throw new Error("Милерови индекси не могу бити (000).");let c=[];switch(e){case"m-3m":c=fc(a);break;case"m-3":c=Qm(a);break;case"-43m":c=e0(a);break;case"432":c=n0(a);break;case"4/mmm":c=i0(a);break;case"6/mmm":c=r0(a);break;case"6/m":c=s0(a);break;case"-3m":c=o0(a);break;case"32":c=c0(a);break;case"mmm":c=a0(a);break;case"2/m":c=l0(a);break;default:c=fc(a)}const l=t==="heksagonalni"||t==="trigonalni";return c.map(u=>({hkl:u,normala:Zm(u,t,i),oznaka:Ym(u,l)}))}const I0={"m-3m":(n,e,t)=>Dt([n,e,t],"m-3m","kubni").map(i=>i.hkl),"m-3":(n,e,t)=>Dt([n,e,t],"m-3","kubni").map(i=>i.hkl),"-43m":(n,e,t)=>Dt([n,e,t],"-43m","kubni").map(i=>i.hkl),432:(n,e,t)=>Dt([n,e,t],"432","kubni").map(i=>i.hkl),"4/mmm":(n,e,t)=>Dt([n,e,t],"4/mmm","tetragonalni").map(i=>i.hkl),"6/mmm":(n,e,t)=>Dt([n,e,t],"6/mmm","heksagonalni").map(i=>i.hkl),"6/m":(n,e,t)=>Dt([n,e,t],"6/m","heksagonalni").map(i=>i.hkl),"-3m":(n,e,t)=>Dt([n,e,t],"-3m","trigonalni").map(i=>i.hkl),32:(n,e,t)=>Dt([n,e,t],"32","trigonalni").map(i=>i.hkl),mmm:(n,e,t)=>Dt([n,e,t],"mmm","ortorombicni").map(i=>i.hkl),"2/m":(n,e,t)=>Dt([n,e,t],"2/m","monoklinicni").map(i=>i.hkl)},al=new Map,u0=["m-3m","m-3","-43m","432","4/mmm","6/mmm","6/m","-3m","32","mmm","2/m"];for(const n of u0){let e="kubni";n==="4/mmm"?e="tetragonalni":n==="6/mmm"||n==="6/m"?e="heksagonalni":n==="-3m"||n==="32"?e="trigonalni":n==="mmm"?e="ortorombicni":n==="2/m"&&(e="monoklinicni"),al.set(n,(t,i)=>Dt(t,n,e,i))}const d0=["kubni","tetragonalni","heksagonalni","trigonalni","ortorombicni"];for(const n of d0){const e=il(n);al.set(n,(t,i)=>Dt(t,e,n,i))}function h0(n,e,t,i){const a=t??il(e);return Dt(n,a,e,i)}const f0={imaPodrazumevanuAnimaciju(n){return(n.animacija??"prelaz")!=="nema"},pocetnaKamera(){return{theta:.64,phi:1.12,udaljenost:4.8}},kreiraj(n,e){const t=e.animacija??"prelaz",a=e.forme.map((C,P)=>{const N=`forma-${P}`,k=C.naziv||(C.hkl.length===4?`{${C.hkl.join(" ")}}`:Wm(C.hkl)),O=h0(C.hkl,e.sistem,e.klasa,e.celija);return{grupaId:N,oznakaForme:k,baznoD:C.d,hkl:C.hkl,ekvivalentne:O}}),r=new it;n.scena3D.add(r);const s=new ht({color:new ce(n.tema.token("--text-primary"))}),o=a.map((C,P)=>new ct({color:new ce(n.tema.token("--primary")),roughness:.32,metalness:.1,flatShading:!0,name:`mat-forma-${P}`}));let c=null,l=null,u="";function h(){const C=new ce(n.tema.token("--primary")),P=new ce(n.tema.token("--accent")),N=new ce(n.tema.token("--bg-elevated"));for(let k=0;k<o.length;k++){const O=o[k],z=a[k].grupaId,H=a.length>1?k/(a.length-1):0,$=C.clone().lerp(P,H);k%2===1&&a.length>2&&$.lerp(N,.22),O.color.copy($);const Y=c===z;O.emissive.copy(Y?$.clone().multiplyScalar(.28):new ce(0,0,0))}s.color.set(n.tema.token("--text-primary"))}h();const f=document.createElement("div");f.className="udzbenik-scena-etiketa udzbenik-scena-etiketa--istaknuta",f.hidden=!0,n.slojEtiketa.append(f);let m=.5,g=n.smanjenPokret?.25:0,_=null;if(a.length>1){const C=document.createElement("label");C.className="udzbenik-klizac-oznaka";const P=document.createElement("span");P.textContent=`${We("prelazFormi")}: ${a[0].oznakaForme} ↔ ${a[a.length-1].oznakaForme}`,_=document.createElement("input"),_.type="range",_.min="0",_.max="1",_.step="0.01",_.value="0.5",_.className="udzbenik-klizac",_.addEventListener("input",()=>{m=Number(_.value),M(m),n.zatraziRender()}),C.append(P,_),n.gornjeKontrole.append(C)}const p=document.createElement("div");p.className="udzbenik-habitus-forme";const d=new Map;for(const C of a){const P=document.createElement("button");P.type="button",P.className="udzbenik-mohs-cip",P.textContent=C.oznakaForme;const N=()=>{c=C.grupaId;const k=T?.pljosni.find(O=>O.grupaId===C.grupaId);k?(l=new F(...k.centar),u=`${C.oznakaForme} · ${k.oznaka}`):(l=null,u=C.oznakaForme),h(),w(),n.zatraziRender()};P.addEventListener("click",N),P.addEventListener("focus",N),P.addEventListener("blur",()=>{c===C.grupaId&&(c=null,l=null,h(),w(),n.zatraziRender())}),d.set(C.grupaId,P),p.append(P)}const E=document.createElement("span");E.className="udzbenik-habitus-status",p.append(E),n.podnozje.append(p);let S=null,x=null,T=null,y=[];function w(){if(!T)return;const C=T.pljosni.length,P=T.temena.length,N=e.primer?` · ${We("primerMinerala")}: ${e.primer}`:"",k=u&&c?` · ${u}`:"";E.textContent=`${C} пљосни, ${P} темена${N}${k}`;for(const[O,z]of d.entries()){const H=T.pljosni.some($=>$.grupaId===O);z.classList.toggle("udzbenik-mohs-cip--aktivan",c===O),z.classList.toggle("udzbenik-mohs-cip--prigusen",!H)}}function D(C){const P=a.length;return P<=1?a.map(N=>N.baznoD):a.map((N,k)=>{const O=k/(P-1);let z=1;return C<.5?z=1+(.5-C)*2*O*.95:C>.5&&(z=1+(C-.5)*2*(1-O)*.95),N.baznoD*z})}function M(C){S&&(S.geometry.dispose(),r.remove(S)),x&&(x.geometry.dispose(),r.remove(x));const P=D(C),N=[];for(let Y=0;Y<a.length;Y++){const fe=a[Y],Ie=P[Y];for(const X of fe.ekvivalentne)N.push({normala:X.normala,d:Ie,grupaId:fe.grupaId,oznaka:X.oznaka})}const k=qi(N);let O=.001;for(const Y of k.temena)O=Math.max(O,Math.hypot(Y[0],Y[1],Y[2]));const z=1.48/O;for(const Y of k.temena)Y[0]*=z,Y[1]*=z,Y[2]*=z;for(const Y of k.pljosni)Y.centar[0]*=z,Y.centar[1]*=z,Y.centar[2]*=z;const H=$i(k),$=H.redosledGrupa.map(Y=>{const fe=a.findIndex(Ie=>Ie.grupaId===Y);return o[Math.max(0,fe)]});S=new Ge(H.geometrijaMreze,$),x=new gt(H.geometrijaIvica,s),r.add(S,x),T=k,y=H.mapaTrougaoUPljosan,w()}const v=new Hs,R=new Ke,U=C=>{if(!S||!T)return;const P=n.platno.getBoundingClientRect();if(P.width<=0||P.height<=0)return;R.x=(C.clientX-P.left)/P.width*2-1,R.y=-((C.clientY-P.top)/P.height)*2+1,v.setFromCamera(R,n.kamera);const N=v.intersectObject(S,!1);if(N.length>0&&N[0].faceIndex!==void 0&&N[0].faceIndex!==null){const k=y[N[0].faceIndex],O=k!==void 0?T.pljosni[k]:void 0;if(O){const z=a.find(H=>H.grupaId===O.grupaId);c=O.grupaId,l=new F(...O.centar),u=`${z?.oznakaForme??O.grupaId} · ${O.oznaka}`,h(),w(),n.zatraziRender();return}}c!==null&&C.pointerType==="mouse"&&(c=null,l=null,h(),w(),n.zatraziRender())};return n.platno.addEventListener("pointermove",U),M(m),{azuriraj(C){t==="prelaz"&&a.length>1?(g=(g+C*.14)%1,m=.5-.5*Math.cos(g*Math.PI*2),_&&(_.value=m.toFixed(2)),r.rotation.y+=C*.25,M(m)):t==="rotacija"&&(r.rotation.y+=C*.42)},korak(){t==="prelaz"&&a.length>1?(g=(g+.125)%1,m=.5-.5*Math.cos(g*Math.PI*2),_&&(_.value=m.toFixed(2)),M(m)):r.rotation.y+=.35},resetuj(){r.rotation.set(0,0,0),m=.5,g=.25,_&&(_.value="0.5"),c=null,l=null,h(),M(.5)},osveziTemu(){h()},posleRendera(){if(!c||!l){f.hidden=!0;return}r.updateMatrixWorld(!0);const C=l.clone().applyMatrix4(r.matrixWorld),P=n.projektujU2D(C);if(!P.vidljivo){f.hidden=!0;return}f.textContent=u,f.hidden=!1,f.style.transform=`translate(-50%, -120%) translate(${P.x.toFixed(1)}px, ${P.y.toFixed(1)}px)`},raspolazi(){n.platno.removeEventListener("pointermove",U),Ut(r),s.dispose();for(const C of o)C.dispose()}}}},Rn=.8;function Gi(n,e){return n.map(([t,i,a])=>{const r=Math.hypot(t,i,a)||1;return[t/r*e,i/r*e,a/r*e]})}const pc=2/Math.sqrt(3)-1,mc=Math.sqrt(1.5)-1,gc=Math.SQRT2-1,_c=Math.sqrt(3)-1,vc=1,xc={2:{kb:2,nazivOblika:"Линеарни",granicniOdnos:.155,vrhovi:[[0,0,Rn*(1+.155)],[0,0,-Rn*(1+.155)]],trougloviIndeksi:[]},3:{kb:3,nazivOblika:"Троугаони",granicniOdnos:pc,vrhovi:Gi([[1,0,0],[-.5,Math.sqrt(3)/2,0],[-.5,-Math.sqrt(3)/2,0]],Rn*(1+pc)),trougloviIndeksi:[0,1,2]},4:{kb:4,nazivOblika:"Тетраедарски",granicniOdnos:mc,vrhovi:Gi([[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]],Rn*(1+mc)),trougloviIndeksi:[0,1,2,0,3,1,0,2,3,1,3,2]},6:{kb:6,nazivOblika:"Октаедарски",granicniOdnos:gc,vrhovi:Gi([[1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,1],[0,0,-1]],Rn*(1+gc)),trougloviIndeksi:[0,2,4,2,1,4,1,3,4,3,0,4,0,5,2,2,5,1,1,5,3,3,5,0]},8:{kb:8,nazivOblika:"Кубични",granicniOdnos:_c,vrhovi:Gi([[-1,-1,-1],[1,-1,-1],[1,1,-1],[-1,1,-1],[-1,-1,1],[1,-1,1],[1,1,1],[-1,1,1]],Rn*(1+_c)),trougloviIndeksi:[0,2,1,0,3,2,4,5,6,4,6,7,0,1,5,0,5,4,1,2,6,1,6,5,2,3,7,2,7,6,3,0,4,3,4,7]},12:{kb:12,nazivOblika:"Кубооктаедарски",granicniOdnos:vc,vrhovi:Gi([[1,1,0],[1,-1,0],[-1,-1,0],[-1,1,0],[1,0,1],[1,0,-1],[-1,0,-1],[-1,0,1],[0,1,1],[0,1,-1],[0,-1,-1],[0,-1,1]],Rn*(1+vc)),trougloviIndeksi:[0,8,4,1,4,11,2,11,7,3,7,8,0,5,9,1,10,5,2,6,10,3,9,6,0,4,1,0,1,5,2,7,3,2,3,6,8,9,3,8,3,0,11,1,2,11,2,10]}},p0={imaPodrazumevanuAnimaciju(n){return n.prikazi_odnos_radijusa!==!1},pocetnaKamera(){return{theta:.65,phi:1.18,udaljenost:5.4}},kreiraj(n,e){const t=new it;n.scena3D.add(t);const i=xc[e.kb]??xc[4],a=Rn,r=a*i.granicniOdnos,s=new vn(r,24,24),o=new ct({color:new ce(n.tema.token("--accent")),roughness:.25,metalness:.2}),c=new Ge(s,o);t.add(c);const l=new vn(a,24,24),u=new ct({color:new ce(n.tema.token("--primary")),roughness:.35,metalness:.1,transparent:!0,opacity:.85}),h=new it;for(const[y,w,D]of i.vrhovi){const M=new Ge(l,u);M.position.set(y,w,D),h.add(M)}t.add(h);let f=null,m=null;const g=new ct({color:new ce(n.tema.token("--primary")),transparent:!0,opacity:.22,roughness:.2,side:mt}),_=new ht({color:new ce(n.tema.token("--text-secondary")),linewidth:2});if(i.trougloviIndeksi.length>=3){const y=new $e,w=[];for(const M of i.trougloviIndeksi){const v=i.vrhovi[M];w.push(v[0],v[1],v[2])}y.setAttribute("position",new He(w,3)),y.computeVertexNormals(),f=new Ge(y,g),t.add(f);const D=new Ha(y);m=new gt(D,_),t.add(m)}const p=e.katjon||"Katjon",d=e.anjon||"Anjon",E=document.createElement("div");E.className="udzbenik-scena-status",E.textContent=`КБ = ${i.kb} (${i.nazivOblika}) • Гранични однос RA/RX = ${i.granicniOdnos.toFixed(3)} • ${p} / ${d}`,n.podnozje.append(E);let S=0;const x=e.prikazi_odnos_radijusa!==!1;function T(){o.color.set(n.tema.token("--accent")),u.color.set(n.tema.token("--primary")),g.color.set(n.tema.token("--primary")),_.color.set(n.tema.token("--text-secondary"))}return{azuriraj(y){if(S+=y,t.rotation.y=S*.35,x){const w=Math.sin(S*1.8);if(w<-.2){const D=.08*(Math.abs(w)-.2);c.position.set(Math.sin(S*22)*D,Math.cos(S*19)*D,Math.sin(S*25)*D),c.scale.setScalar(.72)}else c.position.set(0,0,0),c.scale.setScalar(1)}},korak(){S+=.3,t.rotation.y+=.2},resetuj(){S=0,c.position.set(0,0,0),c.scale.setScalar(1),t.rotation.set(0,0,0)},osveziTemu(){T()},raspolazi(){s.dispose(),o.dispose(),l.dispose(),u.dispose(),f&&f.geometry.dispose(),m&&m.geometry.dispose(),g.dispose(),_.dispose(),Ut(t),E.remove()}}}},m0={imaPodrazumevanuAnimaciju(){return!1},pocetnaKamera(n){return{theta:.65,phi:1.12,udaljenost:(n.prikaz??"celija")==="supercelija"?8.2:6.2}},kreiraj(n,e){const t=e.prikaz??"celija",i=e.stil??"kugle-stapici",a=e.prikazi_celiju??!0,r=e.oznake_atoma??!0,s=e.poluprecnici??"jonski";let o=!1,c=1.15,l=null,u=-1;const h=new it,f=new it,m=new it,g=new it;h.add(g,m,f),n.scena3D.add(h);const _=new ht({color:new ce(n.tema.token("--text-secondary"))}),p=new ct({color:new ce(n.tema.token("--text-muted")),roughness:.45,metalness:.15}),d=new Ui({color:new ce(n.tema.token("--accent")),wireframe:!0}),E=new Ge(new vn(1,14,12),d);E.visible=!1,h.add(E);const S=document.createElement("div");S.className="udzbenik-scena-etiketa udzbenik-scena-etiketa--atom",S.hidden=!0,n.slojEtiketa.append(S);const x=document.createElement("div");if(x.className="udzbenik-struktura-kontrole",i==="kugle-stapici"){const O=document.createElement("label");O.className="udzbenik-klizac-oznaka";const z=document.createElement("span");z.textContent=`${We("faktorVeza")}: ×1,15`;const H=document.createElement("input");H.type="range",H.min="0.85",H.max="1.40",H.step="0.05",H.value="1.15",H.className="udzbenik-klizac",H.addEventListener("input",()=>{c=Number(H.value),z.textContent=`${We("faktorVeza")}: ×${c.toFixed(2).replace(".",",")}`,l&&(C(l),n.zatraziRender())}),O.append(z,H),x.append(O)}const T=document.createElement("span");if(T.className="udzbenik-atom-status",T.setAttribute("aria-live","polite"),r){const O=document.createElement("button");O.type="button",O.className="udzbenik-dugme udzbenik-dugme--malo",O.textContent=We("sledeciAtom"),O.addEventListener("click",()=>{y.length!==0&&(u=(u+1)%y.length,v(u),n.zatraziRender())}),x.append(O,T)}x.childNodes.length>0&&n.gornjeKontrole.append(x);let y=[],w=null,D=new F,M=1;function v(O){if(O<0||O>=y.length){w=null,E.visible=!1,S.hidden=!0,T.textContent="";return}const z=y[O];w=z.atom;const H=z.mesh.scale.x*1.25;E.position.copy(z.mesh.position),E.scale.setScalar(H),E.visible=!0;const $=`(${z.atom.fx.toFixed(3)}, ${z.atom.fy.toFixed(3)}, ${z.atom.fz.toFixed(3)})`;S.textContent=`${z.atom.simbol} [${z.atom.oznaka}] ${$}`,T.textContent=`${z.atom.simbol} (${z.atom.oznaka}): ${$}`}function R(O){Ut(O),O.clear()}function U(O){n.podnozje.replaceChildren();const z=document.createElement("div");z.className="udzbenik-cpk-legenda",z.setAttribute("aria-label",We("legendaElemenata"));const H=document.createElement("div");H.className="udzbenik-cpk-stavke";let $=!1;for(const Ie of O){const X=Rs(Ie),ne=dc(Ie,s);s==="jonski"&&ne.koriscenaVrsta==="kovalentni"&&($=!0);const ue=document.createElement("span");ue.className="udzbenik-cpk-cip";const se=document.createElement("span");se.className="udzbenik-cpk-boja",se.style.backgroundColor=X.bojaHex,se.setAttribute("aria-hidden","true");const ee=ne.koriscenaVrsta==="jonski"&&ne.jon?`${X.simbol} (${ne.jon})`:X.simbol,_e=ne.poluprecnik.toFixed(2).replace(".",","),de=document.createElement("span");de.textContent=`${ee} — ${X.naziv} (r = ${_e} Å)`,ue.append(se,de),H.append(ue)}const Y=document.createElement("p");Y.className="udzbenik-scena-izvor";const fe=i==="kugle-stapici"?` · ${We("detekcijaVezaKovalentniOznaka")}${c.toFixed(2).replace(".",",")}`:"";if(s==="jonski"){const Ie=$?`${As.izvor}; ${We("kovalentnaRezervaOznaka")}: ${uc}`:As.izvor;Y.textContent=`${We("poluprecniciJonskiOznaka")} (${We("izvorPodataka")}: ${Ie})${fe}`}else Y.textContent=`${We("poluprecniciKovalentniOznaka")} (${We("izvorPodataka")}: ${uc})${fe}`;z.append(H,Y),n.podnozje.append(z)}function C(O){R(f),R(m),R(g),y=[];const z=Xs(O.celija),H=t==="supercelija"?2:1,$=Pn(H,H,H,z);D=new F($[0]*.5,$[1]*.5,$[2]*.5);const Y=Math.max(O.celija.a*H,O.celija.b*H,O.celija.c*H);M=3.6/Math.max(1,Y);const fe=[],Ie=new Set,X=[];for(const ee of O.atomi){X.includes(ee.simbol)||X.push(ee.simbol);const _e=Rs(ee.simbol),de=dc(ee.simbol,s),Z=(ee.fx%1+1)%1,ae=(ee.fy%1+1)%1,re=(ee.fz%1+1)%1,L=Z<.001?[0,1]:[0],Le=ae<.001?[0,1]:[0],Ce=re<.001?[0,1]:[0];for(let Re=0;Re<H;Re++)for(let Me=0;Me<H;Me++)for(let Fe=0;Fe<H;Fe++)for(const we of L)for(const I of Le)for(const b of Ce){const G=Z+Re+we,Q=ae+Me+I,ie=re+Fe+b;if(G>H+.001||Q>H+.001||ie>H+.001)continue;const J=`${G.toFixed(3)},${Q.toFixed(3)},${ie.toFixed(3)},${ee.simbol}`;if(Ie.has(J))continue;Ie.add(J);const Ae=Pn(G,Q,ie,z);fe.push({oznaka:ee.oznaka,simbol:ee.simbol,fx:G,fy:Q,fz:ie,pozicija:new F(Ae[0],Ae[1],Ae[2]),poluprecnikPrikaza:de.poluprecnik,kovalentniPoluprecnik:_e.kovalentniPoluprecnik,bojaHex:_e.bojaHex})}}const ne=new vn(1,20,16),ue=new Map,se=i==="kugle"?.52:.25;for(const ee of fe){let _e=ue.get(ee.simbol);_e||(_e=new ct({color:new ce(ee.bojaHex),roughness:.32,metalness:.1}),ue.set(ee.simbol,_e));const de=new Ge(ne,_e);de.position.copy(ee.pozicija).sub(D).multiplyScalar(M);const Z=Math.max(.045,ee.poluprecnikPrikaza*se*M);de.scale.setScalar(Z),f.add(de),y.push({mesh:de,atom:ee})}if(i==="kugle-stapici"){const ee=new ea(1,1,1,10,1),_e=new F(0,1,0),de=Math.max(.035,.09*M);for(let Z=0;Z<fe.length;Z++){const ae=fe[Z];for(let re=Z+1;re<fe.length;re++){const L=fe[re],Le=ae.pozicija.distanceTo(L.pozicija),Ce=(ae.kovalentniPoluprecnik+L.kovalentniPoluprecnik)*c;if(Le>.35&&Le<=Ce){const Re=y[Z].mesh.position,Fe=y[re].mesh.position.clone().sub(Re),we=Fe.length();if(we<1e-4)continue;const I=new Ge(ee,p.clone());I.position.copy(Re).addScaledVector(Fe,.5),I.quaternion.setFromUnitVectors(_e,Fe.clone().normalize()),I.scale.set(de,we,de),m.add(I)}}}ee.dispose()}if(a){const ee=[],_e=[[[0,0,0],[1,0,0]],[[1,0,0],[1,1,0]],[[1,1,0],[0,1,0]],[[0,1,0],[0,0,0]],[[0,0,1],[1,0,1]],[[1,0,1],[1,1,1]],[[1,1,1],[0,1,1]],[[0,1,1],[0,0,1]],[[0,0,0],[0,0,1]],[[1,0,0],[1,0,1]],[[1,1,0],[1,1,1]],[[0,1,0],[0,1,1]]];for(let Z=0;Z<H;Z++)for(let ae=0;ae<H;ae++)for(let re=0;re<H;re++)for(const[L,Le]of _e){const Ce=Pn(L[0]+Z,L[1]+ae,L[2]+re,z),Re=Pn(Le[0]+Z,Le[1]+ae,Le[2]+re,z),Me=new F(...Ce).sub(D).multiplyScalar(M),Fe=new F(...Re).sub(D).multiplyScalar(M);ee.push(Me.x,Me.y,Me.z,Fe.x,Fe.y,Fe.z)}const de=new $e;de.setAttribute("position",new He(ee,3)),g.add(new gt(de,_.clone()))}U(X),u=-1,v(-1)}const P=new Hs,N=new Ke,k=O=>{if(!r||y.length===0)return;const z=n.platno.getBoundingClientRect();if(z.width<=0||z.height<=0)return;N.x=(O.clientX-z.left)/z.width*2-1,N.y=-((O.clientY-z.top)/z.height)*2+1,P.setFromCamera(N,n.kamera);const H=P.intersectObjects(y.map($=>$.mesh),!1);if(H.length>0){const $=H[0].object,Y=y.findIndex(fe=>fe.mesh===$);Y!==u&&(u=Y,v(Y),n.zatraziRender())}else u!==-1&&O.pointerType==="mouse"&&(u=-1,v(-1),n.zatraziRender())};return r&&n.platno.addEventListener("pointermove",k),n.api.ucitajStrukturuCif(e.mineral).then(O=>{o||(l=Bm(O),C(l),n.zatraziRender())}).catch(O=>{if(o)return;const z=(O instanceof wt&&O.status===404,We("strukturaNedostupna"));n.prikaziRezervu(z)}),{resetuj(){u=-1,v(-1)},osveziTemu(O){_.color.set(O.token("--text-secondary")),p.color.set(O.token("--text-muted")),d.color.set(O.token("--accent"));for(const z of g.children){const H=z;H.material instanceof ht&&H.material.color.set(O.token("--text-secondary"))}for(const z of m.children){const H=z;H.material instanceof ct&&H.material.color.set(O.token("--text-muted"))}},posleRendera(){if(!w||u<0){S.hidden=!0;return}const O=y[u];if(!O)return;O.mesh.updateMatrixWorld(!0);const z=O.mesh.position.clone().applyMatrix4(h.matrixWorld),H=n.projektujU2D(z);if(!H.vidljivo){S.hidden=!0;return}S.hidden=!1,S.style.transform=`translate(-50%, -130%) translate(${H.x.toFixed(1)}px, ${H.y.toFixed(1)}px)`},raspolazi(){o=!0,r&&n.platno.removeEventListener("pointermove",k),Ut(h),_.dispose(),p.dispose(),d.dispose()}}}},Dr=[{kljuc:"kubni",naziv:"Кубни",kratko:"Кубни",odnosIvica:"a = b = c",odnosUglova:"α = β = γ = 90°",reprezentativniOblik:"коцка",celija:{a:1.15,b:1.15,c:1.15,alpha:90,beta:90,gamma:90}},{kljuc:"tetragonalni",naziv:"Тетрагонални",kratko:"Тетраг.",odnosIvica:"a = b ≠ c",odnosUglova:"α = β = γ = 90°",reprezentativniOblik:"тетрагонална призма",celija:{a:1,b:1,c:1.62,alpha:90,beta:90,gamma:90}},{kljuc:"ortorombicni",naziv:"Орторомбични",kratko:"Орторомб.",odnosIvica:"a ≠ b ≠ c",odnosUglova:"α = β = γ = 90°",reprezentativniOblik:"правоугаона призма („цигла“)",celija:{a:.85,b:1.22,c:1.58,alpha:90,beta:90,gamma:90}},{kljuc:"heksagonalni",naziv:"Хексагонални",kratko:"Хексаг.",odnosIvica:"a = b ≠ c",odnosUglova:"α = β = 90°, γ = 120°",reprezentativniOblik:"хексагонална призма",celija:{a:1.08,b:1.08,c:1.55,alpha:90,beta:90,gamma:120}},{kljuc:"trigonalni",naziv:"Тригонални",kratko:"Тригон.",odnosIvica:"a = b = c (ромбоедарска) / a = b ≠ c (хексагонална)",odnosUglova:"α = β = γ ≠ 90° (ромб.) / α = β = 90°, γ = 120° (хекс.)",reprezentativniOblik:"ромбоедар (у кристалографији се стандардно описује и хексагоналном поставком)",celija:{a:1.18,b:1.18,c:1.18,alpha:75,beta:75,gamma:75}},{kljuc:"monoklinicni",naziv:"Моноклинични",kratko:"Монокл.",odnosIvica:"a ≠ b ≠ c",odnosUglova:"α = γ = 90°, β ≠ 90°",reprezentativniOblik:"кос паралелопипед (β ≠ 90°)",celija:{a:.92,b:1.22,c:1.48,alpha:90,beta:112,gamma:90}},{kljuc:"triklinicni",naziv:"Триклинични",kratko:"Трикл.",odnosIvica:"a ≠ b ≠ c",odnosUglova:"α ≠ β ≠ γ ≠ 90°",reprezentativniOblik:"кос паралелопипед (α, β, γ ≠ 90°)",celija:{a:.88,b:1.18,c:1.46,alpha:78,beta:109,gamma:103}}],g0={a:1.15,b:1.15,c:1.15,alpha:90,beta:90,gamma:90};function _0(n,e,t){const i=Math.max(0,Math.min(1,t));return{a:n.a+(e.a-n.a)*i,b:n.b+(e.b-n.b)*i,c:n.c+(e.c-n.c)*i,alpha:n.alpha+(e.alpha-n.alpha)*i,beta:n.beta+(e.beta-n.beta)*i,gamma:n.gamma+(e.gamma-n.gamma)*i}}function rl(n){const e=Xs(n),t=new F(...e.va),i=new F(...e.vb),a=new F(...e.vc),r=t.clone().add(i).add(a).multiplyScalar(.5),s=[],o=[[0,0,0],[1,0,0],[1,1,0],[0,1,0],[0,0,1],[1,0,1],[1,1,1],[0,1,1]];for(const[g,_,p]of o){const d=Pn(g,_,p,e);s.push(new F(d[0]-r.x,d[1]-r.y,d[2]-r.z))}const c=[[0,1],[1,2],[2,3],[3,0],[4,5],[5,6],[6,7],[7,4],[0,4],[1,5],[2,6],[3,7]],l=[];for(const[g,_]of c){const p=s[g],d=s[_];l.push(p.x,p.y,p.z,d.x,d.y,d.z)}const u=new $e;u.setAttribute("position",new He(l,3));const h=[[0,3,2,1],[4,5,6,7],[0,1,5,4],[2,3,7,6],[1,2,6,5],[3,0,4,7]],f=[];for(const[g,_,p,d]of h){const E=s[g],S=s[_],x=s[p],T=s[d];f.push(E.x,E.y,E.z,S.x,S.y,S.z,x.x,x.y,x.z,E.x,E.y,E.z,x.x,x.y,x.z,T.x,T.y,T.z)}const m=new $e;return m.setAttribute("position",new He(f,3)),m.computeVertexNormals(),{ivice:u,mreza:m,poreklo:s[0],va:t,vb:i,vc:a}}function Lr(n,e,t,i){const a=e.clone().normalize(),r=t.clone().normalize(),s=18,o=[];let c=n.clone();for(let u=0;u<=s;u++){const h=u/s,f=a.clone().multiplyScalar(1-h).addScaledVector(r,h).normalize(),m=n.clone().addScaledVector(f,i);if(u===Math.floor(s/2)&&(c=n.clone().addScaledVector(f,i*1.38)),u>0){const g=(u-1)/s,_=a.clone().multiplyScalar(1-g).addScaledVector(r,g).normalize(),p=n.clone().addScaledVector(_,i);o.push(p.x,p.y,p.z,m.x,m.y,m.z)}}const l=new $e;return l.setAttribute("position",new He(o,3)),{geometrija:l,sredina:c}}function v0(n,e,t){if(n==="heksagonalni"){const s=.58+.22*t,o=1.35-(1.35-.68)*t,c=[{normala:[0,1,0],d:s},{normala:[0,-1,0],d:s},{normala:[1,0,0],d:.68},{normala:[-1,0,0],d:.68},{normala:[0,0,1],d:.68+.14*t},{normala:[0,0,-1],d:.68+.14*t},{normala:[.5,0,Math.sqrt(3)/2],d:o},{normala:[-.5,0,Math.sqrt(3)/2],d:o},{normala:[.5,0,-Math.sqrt(3)/2],d:o},{normala:[-.5,0,-Math.sqrt(3)/2],d:o}],l=[{normala:[0,1,0],d:s},{normala:[0,-1,0],d:s}];if(t>.85){for(let g=0;g<6;g++){const _=g*Math.PI/3;l.push({normala:[Math.cos(_),0,Math.sin(_)],d:.68})}const f=qi(l),m=$i(f);return{mreza:m.geometrijaMreze,ivice:m.geometrijaIvica}}const u=qi(c),h=$i(u);return{mreza:h.geometrijaMreze,ivice:h.geometrijaIvica}}const i={a:e.a*.92,b:e.b*.92,c:e.c*.92,alpha:e.alpha,beta:e.beta,gamma:e.gamma},a=rl(i);return{mreza:a.mreza,ivice:a.ivice}}const x0={imaPodrazumevanuAnimaciju(n){return(n.animacija??"rotacija")!=="nema"},pocetnaKamera(){return{theta:.42,phi:1.15,udaljenost:6.8}},kreiraj(n,e){const t=e.animacija??"rotacija",i=e.prikazi_ose??!0,a=e.prikazi_celiju??!0;let r=e.sistem==="svi"?"heksagonalni":e.sistem;e.sistem==="svi"&&(r="kubni");let s=n.smanjenPokret||t!=="uporedi"?1:0,o=0;const c=new it,l=new it,u=new it;a?(l.position.set(-1.55,-.05,0),u.position.set(1.55,-.05,0)):u.position.set(0,-.05,0),c.add(l,u),n.scena3D.add(c);const h=new ct({color:new ce(n.tema.token("--primary")),transparent:!0,opacity:.14,roughness:.45,metalness:.05,side:mt,depthWrite:!1}),f=new ht({color:new ce(n.tema.token("--text-secondary"))}),m=new ht({color:new ce(n.tema.token("--danger"))}),g=new ht({color:new ce(n.tema.token("--success"))}),_=new ht({color:new ce(n.tema.token("--accent"))}),p=new ht({color:new ce(n.tema.token("--warning"))}),d=new ct({color:new ce(n.tema.token("--primary")),transparent:!0,opacity:.78,roughness:.35,metalness:.08,flatShading:!0}),E=new ht({color:new ce(n.tema.token("--text-primary"))}),S=["a","b","c","α","β","γ"],x=new Map,T=new Map;if(i&&a)for(const P of S){const N=document.createElement("span");N.className="udzbenik-scena-etiketa",N.textContent=P,n.slojEtiketa.append(N),x.set(P,N),T.set(P,new F)}const y=document.createElement("div");y.className="udzbenik-scena-info-red",n.podnozje.append(y);const w=new Map;if(e.sistem==="svi"){const P=document.createElement("div");P.className="udzbenik-sistemi-traka",P.setAttribute("role","group"),P.setAttribute("aria-label",We("izaberiKristalniSistem"));for(const N of Dr){const k=document.createElement("button");k.type="button",k.className="udzbenik-sistem-kartica",k.dataset.sistem=N.kljuc,k.setAttribute("aria-pressed",String(N.kljuc===r));const O=document.createElement("span");O.className="udzbenik-sistem-kartica-naslov",O.textContent=N.naziv;const z=document.createElement("span");z.className="udzbenik-sistem-kartica-meta",z.textContent=`${N.odnosIvica} · ${N.odnosUglova}`,k.append(O,z),k.addEventListener("click",()=>{r=N.kljuc,s=n.smanjenPokret||t!=="uporedi"?1:0,D(),U(),n.zatraziRender()}),w.set(N.kljuc,k),P.append(k)}n.gornjeKontrole.append(P)}function D(){for(const[P,N]of w.entries()){const k=P===r;N.classList.toggle("udzbenik-sistem-kartica--aktivna",k),N.setAttribute("aria-pressed",String(k))}}function M(){return Dr.find(P=>P.kljuc===r)??Dr[0]}function v(P){for(const N of P.children){const k=N.geometry;k&&k.dispose()}P.clear()}function R(){if(t!=="uporedi"||r==="kubni")return 1;const P=s%1;if(P<.4){const N=P/.4;return N*N*(3-2*N)}if(P<.72)return 1;if(P<.92){const N=(P-.72)/.2;return 1-N*N*(3-2*N)}return 0}function U(){const P=M(),N=R(),k=_0(g0,P.celija,N);if(v(l),v(u),a){const Y=rl(k),fe=new Ge(Y.mreza,h),Ie=new gt(Y.ivice,f);if(l.add(fe,Ie),i){const X=Y.poreklo,ne=X.clone().addScaledVector(Y.va,1.16),ue=X.clone().addScaledVector(Y.vb,1.16),se=X.clone().addScaledVector(Y.vc,1.16),ee=new $e().setFromPoints([X,ne]),_e=new $e().setFromPoints([X,ue]),de=new $e().setFromPoints([X,se]);l.add(new Xi(ee,m),new Xi(_e,g),new Xi(de,_));const Z=Lr(X,Y.vb,Y.vc,.36),ae=Lr(X,Y.va,Y.vc,.44),re=Lr(X,Y.va,Y.vb,.36);l.add(new gt(Z.geometrija,p),new gt(ae.geometrija,p),new gt(re.geometrija,p)),T.get("a")?.copy(ne),T.get("b")?.copy(ue),T.get("c")?.copy(se),T.get("α")?.copy(Z.sredina),T.get("β")?.copy(ae.sredina),T.get("γ")?.copy(re.sredina)}}const O=v0(P.kljuc,k,N);u.add(new Ge(O.mreza,d),new gt(O.ivice,E)),y.replaceChildren();const z=document.createElement("strong");z.textContent=`${P.naziv}: `;const H=document.createElement("span"),$=P.kljuc==="trigonalni"?" • Стандардна кристалографска поставка за тригоналне минерале (кварц, калцит) је хексагонална (a = b ≠ c, γ = 120°).":"";H.textContent=`${P.odnosIvica} · ${P.odnosUglova} — облик: ${P.reprezentativniOblik}${$}`,y.append(z,H)}function C(){if(!i||!a)return;l.updateMatrixWorld(!0);const P=M();for(const[N,k]of x.entries()){const O=T.get(N);if(!O)continue;const z=O.clone().applyMatrix4(l.matrixWorld),H=n.projektujU2D(z);if(!H.vidljivo){k.hidden=!0;continue}k.hidden=!1,k.style.transform=`translate(-50%, -50%) translate(${H.x.toFixed(1)}px, ${H.y.toFixed(1)}px)`;const $=N==="c"&&P.celija.c!==P.celija.a||N==="b"&&P.celija.b!==P.celija.a||N==="α"&&P.celija.alpha!==90||N==="β"&&P.celija.beta!==90||N==="γ"&&P.celija.gamma!==90;k.classList.toggle("udzbenik-scena-etiketa--istaknuta",$)}}return D(),U(),{azuriraj(P){t==="uporedi"?(s=(s+P*.18)%1,o+=P*.22,c.rotation.y=Math.sin(o)*.18,U()):t==="rotacija"&&(c.rotation.y+=P*.45)},korak(){t==="uporedi"?(s=(s+.15)%1,o+=.45,c.rotation.y=Math.sin(o)*.18,U()):c.rotation.y+=.35},resetuj(){c.rotation.set(0,0,0),o=0,s=n.smanjenPokret||t!=="uporedi"?1:0,U()},osveziTemu(P){h.color.set(P.token("--primary")),f.color.set(P.token("--text-secondary")),m.color.set(P.token("--danger")),g.color.set(P.token("--success")),_.color.set(P.token("--accent")),p.color.set(P.token("--warning")),d.color.set(P.token("--primary")),E.color.set(P.token("--text-primary"))},posleRendera(){C()},raspolazi(){Ut(c),h.dispose(),f.dispose(),m.dispose(),g.dispose(),_.dispose(),p.dispose(),d.dispose(),E.dispose()}}}},Yt="Klein, C. & Dutrow, B. (2007), Manual of Mineral Science (23rd ed.), John Wiley & Sons, Table 2.3 (Knoop microhardness HK, kgf/mm²; теренске пробе: нокат ~2,5, бакарни новчић ~3, нож/стакло ~5,5, турпија ~6,5).",An=[{mohs:1,kljuc:"talk",naziv:"Талк",formula:"Mg₃Si₄O₁₀(OH)₂",apsolutnaKnoop:1,izvor:Yt},{mohs:2,kljuc:"gips",naziv:"Гипс",formula:"CaSO₄·2H₂O",apsolutnaKnoop:32,izvor:Yt},{mohs:3,kljuc:"kalcit",naziv:"Калцит",formula:"CaCO₃",apsolutnaKnoop:135,izvor:Yt},{mohs:4,kljuc:"fluorit",naziv:"Флуорит",formula:"CaF₂",apsolutnaKnoop:163,izvor:Yt},{mohs:5,kljuc:"apatit",naziv:"Апатит",formula:"Ca₅(PO₄)₃(F,Cl,OH)",apsolutnaKnoop:430,izvor:Yt},{mohs:6,kljuc:"ortoklas",naziv:"Ортоклас",formula:"KAlSi₃O₈",apsolutnaKnoop:560,izvor:Yt},{mohs:7,kljuc:"kvarc",naziv:"Кварц",formula:"SiO₂",apsolutnaKnoop:820,izvor:Yt},{mohs:8,kljuc:"topaz",naziv:"Топаз",formula:"Al₂SiO₄(F,OH)₂",apsolutnaKnoop:1340,izvor:Yt},{mohs:9,kljuc:"korund",naziv:"Корунд",formula:"Al₂O₃",apsolutnaKnoop:2100,izvor:Yt},{mohs:10,kljuc:"dijamant",naziv:"Дијамант",formula:"C",apsolutnaKnoop:7e3,izvor:Yt}],M0=[{naziv:"Нокат (~2,5)",mohs:2.5},{naziv:"Бакарни новчић (~3)",mohs:3},{naziv:"Нож / стакло (~5,5)",mohs:5.5},{naziv:"Челична турпија (~6,5)",mohs:6.5}];function Mc(n,e){if(!e||e.length===0)return!1;const t=n.kljuc.toLowerCase(),i=n.naziv.toLowerCase();return e.some(a=>{const r=a.trim().toLowerCase();return r===t||r===i})}const S0={imaPodrazumevanuAnimaciju(){return!0},pocetnaKamera(){return{theta:.16,phi:1.18,udaljenost:8.6}},kreiraj(n,e){const t=e.prikazi_apsolutnu??!1,i=e.prikazi_terenske_probe??!0,a=e.istaknuti??[];let r=!1,s=0,o=6,c=5,l=n.smanjenPokret?.65:0;const u=new it;u.position.set(0,-.35,0),n.scena3D.add(u);const h=-4.05,f=.9,m=-.7,g=2.75,_=new ct({color:new ce(n.tema.token("--bg-elevated")),roughness:.7,metalness:.05}),p=new Ge(new mn(9.6,.14,1.4),_);p.position.set(0,m-.07,-.35),u.add(p);const d=[],E=new ht({color:new ce(n.tema.token("--text-primary"))}),S=new mn(.66,1,.66),x=new Ha(S);for(let Z=0;Z<An.length;Z++){const ae=An[Z],re=Mc(ae,a),L=new ce(n.tema.token(re?"--accent":"--primary")),Le=new ct({color:L,emissive:re?new ce(n.tema.token("--accent")).multiplyScalar(.22):new ce(0,0,0),roughness:.35,metalness:.12}),Ce=new Ge(S,Le),Re=new gt(x,E),Me=h+Z*f;Ce.position.set(Me,m+.5,-.35),Re.position.copy(Ce.position),u.add(Ce,Re);const Fe=document.createElement("span");Fe.className="udzbenik-scena-etiketa udzbenik-scena-etiketa--mala",re&&Fe.classList.add("udzbenik-scena-etiketa--istaknuta"),Fe.textContent=`${ae.mohs}`,n.slojEtiketa.append(Fe),d.push({mineral:ae,istaknut:re,mesh:Ce,ivice:Re,mat:Le,etiketaDom:Fe})}const T=new ct({color:new ce(n.tema.token("--warning")),roughness:.4}),y=[];if(i){const Z=new ea(.035,.035,.65,8);for(const ae of M0){const re=h+(ae.mohs-1)*f,L=new Ge(Z,T);L.position.set(re,m+.32,.18),u.add(L);const Le=document.createElement("span");Le.className="udzbenik-scena-etiketa udzbenik-scena-etiketa--proba",Le.textContent=ae.naziv,n.slojEtiketa.append(Le),y.push({x:re,tekst:ae.naziv,dom:Le,stub:L})}}const w=new it;w.position.set(0,m-.52,1.35),u.add(w);const D=new ct({color:new ce(n.tema.token("--primary-light")),roughness:.45,metalness:.08}),M=new Ge(new mn(3.4,.24,.92),D),v=new gt(new Ha(M.geometry),E);w.add(M,v);const R=new ct({color:new ce(n.tema.token("--danger")),roughness:.85}),U=new Ge(new mn(1,.05,.11),R);U.position.set(-1.1,.125,0),U.visible=!1,w.add(U);const C=new ct({color:new ce(n.tema.token("--accent")),roughness:.25,metalness:.2}),P=new Ge(new Vs(.22,.72,6),C);P.rotation.x=Math.PI,P.rotation.z=-.22,P.position.set(-1.1,.5,0),w.add(P);const N=document.createElement("div");N.className="udzbenik-mohs-kontrole";const k=document.createElement("div");k.className="udzbenik-mohs-dugmad",k.setAttribute("role","group"),k.setAttribute("aria-label",We("ordinalnaTvrdocaOznaka"));const O=[];for(let Z=0;Z<An.length;Z++){const ae=An[Z],re=document.createElement("button");re.type="button",re.className="udzbenik-mohs-cip",Mc(ae,a)&&re.classList.add("udzbenik-mohs-cip--istaknut"),re.textContent=`${ae.mohs}. ${ae.naziv}`,re.addEventListener("click",()=>{Ie(Z)}),O.push(re),k.append(re)}N.append(k);const z=document.createElement("div");z.className="udzbenik-mohs-akcije";const H=document.createElement("button");H.type="button",H.className="udzbenik-dugme udzbenik-dugme--malo",H.textContent=We("zameniMinerale"),H.addEventListener("click",()=>{const Z=o;o=c,c=Z,l=n.smanjenPokret?.75:0,se(),n.zatraziRender()}),z.append(H);let $=null;t&&($=document.createElement("button"),$.type="button",$.className="udzbenik-dugme udzbenik-dugme--malo udzbenik-dugme--preklopnik",$.setAttribute("role","switch"),$.setAttribute("aria-checked","false"),$.textContent=We("apsolutnaTvrdocaPreklopnik"),$.addEventListener("click",()=>{r=!r,$?.setAttribute("aria-checked",String(r)),$?.classList.toggle("udzbenik-dugme--aktivno",r),n.smanjenPokret&&(s=r?1:0,ne()),se(),n.zatraziRender()}),z.append($)),N.append(z),n.gornjeKontrole.append(N);const Y=document.createElement("p");Y.className="udzbenik-scena-info-red",Y.setAttribute("aria-live","polite");const fe=document.createElement("p");fe.className="udzbenik-scena-izvor",fe.textContent=`${We("izvorPodataka")}: ${Yt}`,n.podnozje.append(Y,fe);function Ie(Z){Z===o?c=Z<9?Z+1:Z-1:(o=Z,c=Z>0?Z-1:1),l=n.smanjenPokret?.75:0,se(),n.zatraziRender()}function X(Z,ae){const re=Z.mohs/10*g,L=Math.max(.08,Z.apsolutnaKnoop/7e3*g);return re+(L-re)*ae}function ne(){for(let Z=0;Z<d.length;Z++){const ae=d[Z],re=X(ae.mineral,s);ae.mesh.scale.y=re,ae.mesh.position.y=m+re*.5,ae.ivice.scale.y=re,ae.ivice.position.copy(ae.mesh.position);const L=Z===o,Le=Z===c,Ce=L?"--accent":Le?"--warning":ae.istaknut?"--accent":"--primary",Re=new ce(n.tema.token(Ce));!L&&!Le&&!ae.istaknut&&Re.lerp(new ce(n.tema.token("--bg-elevated")),.25),ae.mat.color.copy(Re),ae.etiketaDom.textContent=r?`${ae.mineral.mohs} (${ae.mineral.apsolutnaKnoop})`:`${ae.mineral.mohs}`}}function ue(){const Z=An[o],ae=An[c],re=Z.mohs>ae.mohs,L=Math.min(1,l/.75),Le=-1.15,Re=Le+(1.15-Le)*L;if(P.position.x=Re,P.position.y=re?.44:.5,re&&L>.03){const Me=Math.max(.05,Re-Le);U.visible=!0,U.scale.x=Me,U.position.x=Le+Me*.5}else U.visible=!1}function se(){for(let Le=0;Le<O.length;Le++){const Ce=O[Le],Re=Le===o;Ce.classList.toggle("udzbenik-mohs-cip--aktivan",Re),Ce.setAttribute("aria-pressed",String(Re))}const Z=An[o],ae=An[c],L=Z.mohs>ae.mohs?`${We("probaGrebanja")}: ${Z.naziv} (${Z.mohs}, HK ${Z.apsolutnaKnoop}) је тврђи и оставља бразду на минералу ${ae.naziv} (${ae.mohs}, HK ${ae.apsolutnaKnoop}).`:`${We("probaGrebanja")}: ${Z.naziv} (${Z.mohs}, HK ${Z.apsolutnaKnoop}) је мекши и НЕ оставља бразду на минералу ${ae.naziv} (${ae.mohs}, HK ${ae.apsolutnaKnoop}).`;Y.textContent=L,ne(),ue()}const ee=new Hs,_e=new Ke,de=Z=>{const ae=n.platno.getBoundingClientRect();if(ae.width<=0||ae.height<=0)return;_e.x=(Z.clientX-ae.left)/ae.width*2-1,_e.y=-((Z.clientY-ae.top)/ae.height)*2+1,ee.setFromCamera(_e,n.kamera);const re=ee.intersectObjects(d.map(L=>L.mesh),!1);if(re.length>0){const L=re[0].object,Le=d.findIndex(Ce=>Ce.mesh===L);Le!==-1&&Ie(Le)}};return n.platno.addEventListener("click",de),se(),{azuriraj(Z){const ae=r?1:0;Math.abs(s-ae)>.002?(s+=(ae-s)*Math.min(1,Z*6),ne()):s!==ae&&(s=ae,ne()),l=(l+Z*.42)%1,ue()},korak(){l=(l+.2)%1,s=r?1:0,ne(),ue()},resetuj(){r=!1,s=0,$&&($.setAttribute("aria-checked","false"),$.classList.remove("udzbenik-dugme--aktivno")),o=6,c=5,l=n.smanjenPokret?.75:0,se()},osveziTemu(Z){_.color.set(Z.token("--bg-elevated")),E.color.set(Z.token("--text-primary")),T.color.set(Z.token("--warning")),D.color.set(Z.token("--primary-light")),R.color.set(Z.token("--danger")),C.color.set(Z.token("--accent")),ne()},posleRendera(){u.updateMatrixWorld(!0);for(const Z of d){const ae=Z.mesh.position.clone().add(new F(0,Z.mesh.scale.y*.5+.22,0)).applyMatrix4(u.matrixWorld),re=n.projektujU2D(ae);Z.etiketaDom.hidden=!re.vidljivo,re.vidljivo&&(Z.etiketaDom.style.transform=`translate(-50%, -50%) translate(${re.x.toFixed(1)}px, ${re.y.toFixed(1)}px)`)}for(const Z of y){const ae=new F(Z.x,m-.22,.35).applyMatrix4(u.matrixWorld),re=n.projektujU2D(ae);Z.dom.hidden=!re.vidljivo,re.vidljivo&&(Z.dom.style.transform=`translate(-50%, 0%) translate(${re.x.toFixed(1)}px, ${re.y.toFixed(1)}px)`)}},raspolazi(){n.platno.removeEventListener("click",de),Ut(u),S.dispose(),x.dispose(),_.dispose(),E.dispose(),T.dispose(),D.dispose(),R.dispose(),C.dispose();for(const Z of d)Z.mat.dispose()}}}};function E0(n,e,t){const i=1/(n*n),a=1/(e*e),r=1/(t*t),s=(i-a)/Math.max(1e-12,a-r),c=2*Math.atan(Math.sqrt(Math.max(0,s)))*180/Math.PI;return c<=90?{dvaV:c,dvaVZ:c,znak:"+",bisektrisaOstra:"Z (γ)"}:{dvaV:180-c,dvaVZ:c,znak:"-",bisektrisaOstra:"X (α)"}}function Sc(n,e,t){const i=Math.hypot(...t),a=i>0?t[0]/i:0,r=i>0?t[1]/i:0,s=i>0?t[2]/i:1;if(n==="izotropna"){const C=e[0]??1.5;return{n1:C,n2:C,delta:0}}if(n==="jednoosna"){const C=e[0]??1.544,P=e[1]??1.553,N=s*s,k=Math.max(0,1-N),O=N/(C*C)+k/(P*P),z=Math.sqrt(1/Math.max(1e-12,O)),H=Math.abs(z-C);return{n1:Math.min(C,z),n2:Math.max(C,z),delta:H}}const o=e[0]??1.52,c=e[1]??1.53,l=e[2]??1.55,u=1/(o*o),h=1/(c*c),f=1/(l*l);let m,g,_,p;if(Math.abs(h-f)>1e-7&&u>=h&&h>=f){const C=E0(o,c,l);m=C.dvaV,g=C.dvaVZ,_=C.znak,p=C.bisektrisaOstra}const d=a*a,E=r*r,S=s*s,x=1,T=-(d*(h+f)+E*(u+f)+S*(u+h)),y=d*h*f+E*u*f+S*u*h,w=Math.max(0,T*T-4*x*y),D=(-T-Math.sqrt(w))/(2*x),M=(-T+Math.sqrt(w))/(2*x),v=Math.sqrt(1/Math.max(1e-12,M)),R=Math.sqrt(1/Math.max(1e-12,D)),U=Math.abs(R-v);return{n1:v,n2:R,delta:U,ugao2V:m,ugao2VZ:g,optickiZnak:_,bisektrisaOstra:p}}const b0={imaPodrazumevanuAnimaciju(){return!0},pocetnaKamera(){return{theta:.72,phi:1.18,udaljenost:5.6}},kreiraj(n,e){const t=new it;n.scena3D.add(t);const i=e.tip,a=e.n&&e.n.length>0?e.n:i==="izotropna"?[1.5]:i==="jednoosna"?[1.658,1.486]:[1.52,1.53,1.55];let r=1.6,s=1.6,o=1.6;if(i==="jednoosna"){const U=a[0],C=a[1]??a[0];r=1.6,s=1.6,o=1.6*(C>=U?1.35:.72)}else i==="dvoosna"&&(r=1.25,s=1.65,o=2.15);const c=new vn(1,48,36);c.scale(r,s,o);const l=new ct({color:new ce(n.tema.token("--primary")),transparent:!0,opacity:.42,roughness:.25,metalness:.1,side:mt}),u=new Ge(c,l);t.add(u);const h=new ht({color:new ce(n.tema.token("--text-secondary"))}),f=new $e,m=[-r*1.3,0,0,r*1.3,0,0,0,-s*1.3,0,0,s*1.3,0,0,0,-o*1.3,0,0,o*1.3];f.setAttribute("position",new He(m,3)),t.add(new gt(f,h));const g=new ht({color:new ce(n.tema.token("--accent")),linewidth:3});if(e.prikazi_opticke_ose!==!1){const U=[];if(i==="jednoosna")U.push(0,0,-o*1.45,0,0,o*1.45);else if(i==="dvoosna"){const P=(Sc(i,a,[0,0,1]).ugao2V??50)/2*(Math.PI/180),N=o*1.4,k=N*Math.sin(P),O=N*Math.cos(P);U.push(-k,0,-O,k,0,O),U.push(k,0,-O,-k,0,O)}if(U.length>0){const C=new $e;C.setAttribute("position",new He(U,3)),t.add(new gt(C,g))}}const _=new it;t.add(_);const p=new Ui({color:new ce(n.tema.token("--warning")),transparent:!0,opacity:.35,side:mt}),d=new js(0,2.2,48),E=new Ge(d,p);_.add(E);const S=new ht({color:new ce(n.tema.token("--danger"))}),x=new $e;x.setAttribute("position",new He([0,0,-2.6,0,0,2.6],3)),_.add(new gt(x,S));const T=document.createElement("div");T.className="udzbenik-scena-status",n.podnozje.append(T);const y=document.createElement("small");y.className="udzbenik-scena-napomena",y.style.display="block",y.textContent="Напомена: Разлике индекса преламања су преувеличане ради јаснијег 3D приказа.",n.podnozje.append(y);let w=.5,D=.3;function M(){_.rotation.set(w,D,0);const U=new F(0,0,1).applyEuler(_.rotation),C=Sc(i,a,[U.x,U.y,U.z]),P=C.delta.toFixed(4),N=e.mineral?` (${e.mineral})`:"",k=C.ugao2V!==void 0?` • 2V = ${C.ugao2V.toFixed(1)}° (${C.optickiZnak}, Bxa = ${C.bisektrisaOstra})`:"";T.textContent=`Тип: ${i}${N} • n'₁ = ${C.n1.toFixed(3)}, n'₂ = ${C.n2.toFixed(3)} • δ = ${P}${k}`}M();function v(){l.color.set(n.tema.token("--primary")),h.color.set(n.tema.token("--text-secondary")),g.color.set(n.tema.token("--accent")),p.color.set(n.tema.token("--warning")),S.color.set(n.tema.token("--danger"))}let R=0;return{azuriraj(U){R+=U*.35,D=Math.sin(R)*1.1,w=Math.cos(R*.7)*.7,M()},korak(){R+=.25,D+=.2,M()},resetuj(){R=0,w=.5,D=.3,M()},osveziTemu(){v()},raspolazi(){c.dispose(),l.dispose(),f.dispose(),h.dispose(),g.dispose(),d.dispose(),p.dispose(),x.dispose(),S.dispose(),Ut(t),T.remove(),y.remove()}}}},Ur={nezo:{klasa:"nezo",naziv:"Незосиликати (изоловани tetraedri)",odnosSiO:"1 : 4 (SiO₄⁴⁻)",zajednickiKiseonici:"0",primeri:"оливин, гранат, циркон"},soro:{klasa:"soro",naziv:"Соросиликати (парови tetraedara)",odnosSiO:"2 : 7 (Si₂O₇⁶⁻)",zajednickiKiseonici:"1",primeri:"епидот, хемиморфит"},"ciklo-3":{klasa:"ciklo-3",naziv:"Циклосиликати (трочлани прстен)",odnosSiO:"1 : 3 (Si₃O₉⁶⁻)",zajednickiKiseonici:"2",primeri:"бенитоит"},"ciklo-6":{klasa:"ciklo-6",naziv:"Циклосиликати (шесточлани прстен)",odnosSiO:"1 : 3 (Si₆O₁₈¹²⁻)",zajednickiKiseonici:"2",primeri:"берил, турмалин"},"ino-jednostruki":{klasa:"ino-jednostruki",naziv:"Иносиликати (једноструки ланци)",odnosSiO:"1 : 3 (Si₂O₆⁴⁻)",zajednickiKiseonici:"2",primeri:"пироксени (диопсид, енстатит)"},"ino-dvostruki":{klasa:"ino-dvostruki",naziv:"Иносиликати (двоструки ланци)",odnosSiO:"4 : 11 (Si₄O₁₁⁶⁻)",zajednickiKiseonici:"2 и 3 (просек 2,5)",primeri:"амфиболи (тремолит, хорнбленда)"},filo:{klasa:"filo",naziv:"Филосиликати (слојевити)",odnosSiO:"2 : 5 (Si₄O₁₀⁴⁻)",zajednickiKiseonici:"3",primeri:"лискуни (мусковит, биотит), талк, каолинит"},tekto:{klasa:"tekto",naziv:"Тектосиликати (просторна мрежа)",odnosSiO:"1 : 2 (SiO₂)",zajednickiKiseonici:"4",primeri:"кварц, фелдспати, зеолити"},sve:{klasa:"sve",naziv:"Преглед свих класа",odnosSiO:"од 1:4 до 1:2",zajednickiKiseonici:"0 до 4",primeri:"полимеризација од незо- до тектосиликата"}};function y0(){const e=.65*Math.SQRT2,t=[0,0,0],i=[-e,.65,0],a=[-e,-.5*.65,Math.sqrt(3)/2*.65],r=[-e,-.5*.65,-(Math.sqrt(3)/2)*.65],s=[e,-.65,0],o=[e,.5*.65,-(Math.sqrt(3)/2)*.65],c=[e,.5*.65,Math.sqrt(3)/2*.65];return{vrhoviLevi:[t,i,a,r],vrhoviDesni:[t,s,o,c],svih7Kiseonika:[t,i,a,r,s,o,c]}}function wn(n,e,t,i,a,r){const s=new it;s.position.copy(n),s.rotation.copy(e);const o=.55,c=[[o,o,o],[o,-o,-o],[-o,o,-o],[-o,-o,o]];if(r==="tetraedri"||r==="oba"){const l=new $e,u=[...c[0],...c[1],...c[2],...c[0],...c[3],...c[1],...c[0],...c[2],...c[3],...c[1],...c[3],...c[2]];l.setAttribute("position",new He(u,3)),l.computeVertexNormals();const h=new Ge(l,t);s.add(h)}if(r==="kugle"||r==="oba")for(const l of c){const u=new Ge(a,i);u.position.set(l[0],l[1],l[2]),s.add(u)}return s}const T0={imaPodrazumevanuAnimaciju(n){return(n.animacija??"rotacija")!=="nema"},pocetnaKamera(){return{theta:.65,phi:1.15,udaljenost:6.2}},kreiraj(n,e){let t=e.klasa==="sve"?"nezo":e.klasa;const i=e.prikaz??"tetraedri",a=new it;n.scena3D.add(a);const r=new vn(.18,16,16),s=new ct({color:new ce(n.tema.token("--primary")),transparent:!0,opacity:.65,roughness:.25,metalness:.1,side:mt}),o=new ct({color:new ce(n.tema.token("--accent")),roughness:.25,metalness:.2}),c=document.createElement("div");c.className="udzbenik-scena-status",n.podnozje.append(c);function l(_){for(;a.children.length>0;){const d=a.children[0];a.remove(d),Ut(d)}const p=Ur[_]??Ur.nezo;if(c.textContent=`${p.naziv} • Si:O = ${p.odnosSiO} • Заједнички O: ${p.zajednickiKiseonici} (${p.primeri})`,_==="nezo")a.add(wn(new F(0,0,0),new Mt(0,0,0),s,o,r,i));else if(_==="soro"){const{vrhoviLevi:d,vrhoviDesni:E,svih7Kiseonika:S}=y0(),[x,T,y,w]=d,[,D,M,v]=E;if(i==="tetraedri"||i==="oba"){const R=new $e,U=[...x,...T,...y,...x,...y,...w,...x,...w,...T,...T,...w,...y,...x,...M,...D,...x,...v,...M,...x,...D,...v,...D,...M,...v];R.setAttribute("position",new He(U,3)),R.computeVertexNormals(),a.add(new Ge(R,s))}if(i==="kugle"||i==="oba")for(const R of S){const U=new Ge(r,o);U.position.set(R[0],R[1],R[2]),a.add(U)}}else if(_==="ciklo-3")for(let d=0;d<3;d++){const E=d*2*Math.PI/3,S=new F(Math.cos(E)*.95,Math.sin(E)*.95,0);a.add(wn(S,new Mt(0,0,E),s,o,r,i))}else if(_==="ciklo-6")for(let d=0;d<6;d++){const E=d*2*Math.PI/6,S=new F(Math.cos(E)*1.5,Math.sin(E)*1.5,0);a.add(wn(S,new Mt(0,0,E),s,o,r,i))}else if(_==="ino-jednostruki")for(let d=-2;d<=2;d++){const E=d%2===0?0:Math.PI;a.add(wn(new F(d*.9,d%2*.2,0),new Mt(0,0,E),s,o,r,i))}else if(_==="ino-dvostruki")for(let d=-2;d<=2;d++){const E=d%2===0?0:Math.PI;a.add(wn(new F(d*.9,.45+d%2*.15,0),new Mt(0,0,E),s,o,r,i)),a.add(wn(new F(d*.9,-.45-d%2*.15,0),new Mt(0,0,E+Math.PI),s,o,r,i))}else if(_==="filo")for(let d=-1;d<=1;d++)for(let E=-1;E<=1;E++){const S=d*1.4+E%2*.7,x=E*1.2;a.add(wn(new F(S,x,0),new Mt(0,0,0),s,o,r,i))}else for(const d of[-.7,.7])for(const E of[-.7,.7])for(const S of[-.7,.7])a.add(wn(new F(d,E,S),new Mt(d,E,S),s,o,r,i))}if(e.klasa==="sve"){const _=document.createElement("div");_.className="udzbenik-silikati-traka",_.style.display="flex",_.style.flexWrap="wrap",_.style.gap="4px";const p=["nezo","soro","ciklo-3","ciklo-6","ino-jednostruki","ino-dvostruki","filo","tekto"];for(const d of p){const E=Ur[d],S=document.createElement("button");S.type="button",S.className="udzbenik-dugme udzbenik-dugme--malo",d===t&&S.classList.add("udzbenik-dugme--aktivno"),S.textContent=d,S.setAttribute("aria-label",E.naziv),S.addEventListener("click",()=>{t=d,_.querySelectorAll("button").forEach(x=>x.classList.remove("udzbenik-dugme--aktivno")),S.classList.add("udzbenik-dugme--aktivno"),l(d)}),_.append(S)}n.gornjeKontrole.append(_)}l(t);let u=0;const h=(e.animacija??(e.klasa==="sve"?"polimerizacija":"rotacija"))==="polimerizacija",f=["nezo","soro","ciklo-6","ino-jednostruki","ino-dvostruki","filo","tekto"];let m=0;function g(){s.color.set(n.tema.token("--primary")),o.color.set(n.tema.token("--accent"))}return{azuriraj(_){if(u+=_,a.rotation.y=u*.35,h){const p=Math.floor(u/3)%f.length;if(p!==m){m=p;const d=f[m];l(d)}}},korak(){u+=.3,a.rotation.y+=.2,h&&(m=(m+1)%f.length,l(f[m]))},resetuj(){u=0,a.rotation.set(0,0,0),m=0,l(t)},osveziTemu(){g()},raspolazi(){r.dispose(),s.dispose(),o.dispose(),Ut(a),c.remove()}}}},A0={"kristalni-sistem":x0,"kristalna-struktura":m0,"mohsova-skala":S0,cepljivost:qm,habitus:f0,"bravaisova-resetka":Vm,"opticka-indikatrisa":b0,blizanac:Fm,"koordinacioni-poliedar":p0,"silikatna-struktura":T0};function w0(n,e,t){const i=A0[n.scena];return i?km(i,n.parametri,e,t):(e.prikaziRezervu("Сцена није подржана у овој верзији мотора."),()=>{})}const D0=Object.freeze(Object.defineProperty({__proto__:null,pokreniScenuPoImenu:w0,raspolaziDeljenimRendererom:zm},Symbol.toStringTag,{value:"Module"}));export{wt as A,I0 as G,As as J,Ya as a,R0 as b,P0 as c,D0 as d,Ym as f,Zm as i,C0 as p,We as t};
