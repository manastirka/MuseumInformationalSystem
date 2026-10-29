const jc={ucitavanjeUdzbenika:"Учитавање уџбеника…",ucitavanjeLekcije:"Учитавање лекције…",ucitavanjeScene:"Учитавање 3D приказа…",greskaUcitavanja:"Грешка при учитавању — покушај поново",pokusajPonovo:"Покушај поново",nemaSecureFetch:"Безбедно слање (secureFetch) није доступно на овој страници.",greskaCuvanjaNapretka:"Чување напретка није успело.",sadrzajDugme:"Садржај уџбеника",navigacijaAria:"Поглавља и лекције",napredakOznaka:"Завршено лекција",zavrsenaLekcijaOznaka:"Завршено",nezavrsenaLekcijaOznaka:"Није завршено",zavrsiLekciju:"Заврши лекцију",cuvanjeNapretka:"Чување…",lekcijaZavrsenaPoruka:"Лекција је означена као завршена.",sacuvajPonovo:"Сачувај напредак поново",prethodnaLekcija:"Претходна лекција",sledecaLekcija:"Следећа лекција",navigacijaLekcijeAria:"Навигација између лекција",tabelaAria:"Табела података",porekloFotografija:"Фотографија",porekloCrtez:"Цртеж",porekloAiIlustracija:"АИ илустрација",porekloDijagram:"Дијаграм",autorOznaka:"Аутор",primerakNedostupan:"Примерак тренутно није доступан",primerakNedostupanPodrazumevano:"Подаци о примерку се не могу приказати.",inventarniBroj:"Инв. бр.",lokalitet:"Локалитет",otvoriKarticuPrimerka:"Отвори картицу примерка у МИС-у",napomenaInfo:"Напомена",napomenaPazi:"Пажња",napomenaZanimljivost:"Занимљивост",proveriOdgovor:"Провери одговор",izaberiOdgovorUpozorenje:"Изаберите бар један одговор пре провере.",odgovorTacan:"Тачно!",odgovorNetacan:"Није тачно — погледајте објашњење.",oznakaTacnogOdgovora:"тачан одговор",oznakaViseTacnih:"Могуће је више тачних одговора.",kvizRezime:"Квиз у лекцији",scenaResetuj:"Ресетуј",scenaResetujAria:"Ресетуј камеру и стање сцене",scenaPauza:"Пауза",scenaPauzaAria:"Паузирај анимацију сцене",scenaNastavi:"Настави",scenaNastaviAria:"Настави анимацију сцене",scenaKorak:"Корак",scenaKorakAria:"Помери анимацију за један корак",scenaPrikaziObjasnjenje:"Прикажи објашњење",scenaSakrijObjasnjenje:"Сакриј објашњење",scenaObjasnjenjeAria:"Прикажи текстуално објашњење сцене",scenaZumPlusAria:"Увећај приказ",scenaZumMinusAria:"Умањи приказ",scenaDodirSavet:"Додирните приказ за ротацију једним прстом (или ротирајте са два прста)",scenaDodirAktivan:"3D ротација активна — заврши за скрол стране",scenaRezervaOznaka:"Статични приказ (3D WebGL није доступан)",strukturaNedostupna:"Структура није доступна за овај минерал",legendaElemenata:"Легенда хемијских елемената (CPK боје и полупречници)",poluprecniciJonskiOznaka:"Полупречници сфера: јонски",poluprecniciKovalentniOznaka:"Полупречници сфера: ковалентни",kovalentnaRezervaOznaka:"ковалентни за елементе ван јонске табеле",detekcijaVezaKovalentniOznaka:"детекција веза: ковалентни ×",faktorVeza:"Праг дужине веза",sledeciAtom:"Следећи атом",atomKoordinate:"Фракционе координате",izaberiKristalniSistem:"Кристални системи",apsolutnaTvrdocaPreklopnik:"Апсолутна тврдоћа (Knoop)",ordinalnaTvrdocaOznaka:"Мосова ординална скала (1–10)",terenskeProbeOznaka:"Теренске пробе",probaGrebanja:"Проба гребања",zameniMinerale:"Обрни смер гребања",izvorPodataka:"Извор",brojPravacaCepljivosti:"Број праваца",ugloviCepljivosti:"Углови",primerMinerala:"Пример",prelazFormi:"Однос форми (прелаз хабитуса)",aktivnaForma:"Кристална форма"},Wc={А:"A",Б:"B",В:"V",Г:"G",Д:"D",Ђ:"Đ",Е:"E",Ж:"Ž",З:"Z",И:"I",Ј:"J",К:"K",Л:"L",Љ:"Lj",М:"M",Н:"N",Њ:"Nj",О:"O",П:"P",Р:"R",С:"S",Т:"T",Ћ:"Ć",У:"U",Ф:"F",Х:"H",Ц:"C",Ч:"Č",Џ:"Dž",Ш:"Š",а:"a",б:"b",в:"v",г:"g",д:"d",ђ:"đ",е:"e",ж:"ž",з:"z",и:"i",ј:"j",к:"k",л:"l",љ:"lj",м:"m",н:"n",њ:"nj",о:"o",п:"p",р:"r",с:"s",т:"t",ћ:"ć",у:"u",ф:"f",х:"h",ц:"c",ч:"č",џ:"dž",ш:"š"};function Xc(n){let e="";for(const t of n)e+=Wc[t]??t;return e}let ic="cyrl";function Nm(n){ic=n}function Ge(n){const e=jc[n];return ic==="latn"?Xc(e):e}class Et extends Error{status;constructor(e,t=0){super(e),this.name="ApiGreska",this.status=t}}function Yc(n,e){const t=n.replace(/\/+$/,""),i=`/${e}`;if(e&&t.endsWith(i))return t.slice(0,t.length-i.length)||"/api/udzbenik";const r=t.lastIndexOf("/");return r>0?t.slice(0,r):t}function Fm(n){const e=(n.dataset.api??"").trim(),t=(n.dataset.zbirka??"minerali").trim();if(!e)throw new Et("Недостаје обавезан атрибут data-api на #udzbenik-app.");const i=(n.dataset.apiKoren??"").trim()||Yc(e,t),a=(n.dataset.pismo??"cyrl").trim().toLowerCase()==="latn"?"latn":"cyrl";return{api:e.replace(/\/+$/,""),apiKoren:i.replace(/\/+$/,""),zbirka:t,pocetnoPoglavlje:(n.dataset.poglavlje??"").trim(),pocetnaLekcija:(n.dataset.lekcija??"").trim(),pismo:a,mozeUredjuje:n.dataset.mozeUredjuje==="true"}}async function Wr(n,e){try{const t=await n.text();if(!t)return e;const i=JSON.parse(t);if(typeof i.greska=="string"&&i.greska.trim())return i.greska.trim()}catch{}return e}class zm{konfig;kesStruktura=new Map;constructor(e){this.konfig=e}get konfiguracija(){return this.konfig}ocistiKes(){this.kesStruktura.clear()}async ucitajUdzbenik(){let e;try{e=await fetch(this.konfig.api,{method:"GET",headers:{Accept:"application/json"}})}catch{throw new Et(Ge("greskaUcitavanja"),0)}if(!e.ok){const t=await Wr(e,Ge("greskaUcitavanja"));throw new Et(t,e.status)}try{return await e.json()}catch{throw new Et(Ge("greskaUcitavanja"),e.status)}}async ucitajLekciju(e,t){const i=`${this.konfig.api}/lekcija/${encodeURIComponent(e)}/${encodeURIComponent(t)}`;let r;try{r=await fetch(i,{method:"GET",headers:{Accept:"application/json"}})}catch{throw new Et(Ge("greskaUcitavanja"),0)}if(!r.ok){const a=await Wr(r,Ge("greskaUcitavanja"));throw new Et(a,r.status)}try{return await r.json()}catch{throw new Et(Ge("greskaUcitavanja"),r.status)}}async posaljiNapredak(e){if(typeof window>"u"||typeof window.secureFetch!="function")throw new Et(Ge("nemaSecureFetch"),0);const t=`${this.konfig.apiKoren}/napredak`;let i;try{i=await window.secureFetch(t,{method:"POST",headers:{"Content-Type":"application/json",Accept:"application/json"},body:JSON.stringify(e)})}catch{throw new Et(Ge("greskaCuvanjaNapretka"),0)}let r=null;try{r=await i.json()}catch{r=null}if(!i.ok||!r?.ok){const a=typeof r?.greska=="string"&&r.greska.trim()?r.greska.trim():Ge("greskaCuvanjaNapretka");throw new Et(a,i.status)}return r}async ucitajStrukturuCif(e){const t=e.trim().toLowerCase(),i=this.kesStruktura.get(t);if(i)return i;const r=`${this.konfig.apiKoren}/struktura/${encodeURIComponent(e.trim())}`,a=(async()=>{let s;try{s=await fetch(r,{method:"GET",headers:{Accept:"text/plain, */*"}})}catch{throw this.kesStruktura.delete(t),new Et(Ge("greskaUcitavanja"),0)}if(s.status===404)throw new Et(Ge("strukturaNedostupna"),404);if(!s.ok){this.kesStruktura.delete(t);const o=await Wr(s,Ge("greskaUcitavanja"));throw new Et(o,s.status)}return s.text()})();return a.catch(s=>{s instanceof Et&&s.status===404||this.kesStruktura.delete(t)}),this.kesStruktura.set(t,a),a}}const qc=["--bg-body","--bg-card","--bg-elevated","--bg-hover","--text-primary","--text-secondary","--text-muted","--primary","--primary-light","--primary-dark","--accent","--accent-light","--accent-strong","--on-accent","--border-color","--border-strong","--focus-ring","--success","--success-soft","--warning","--warning-soft","--danger","--danger-soft","--info","--info-soft","--font-family","--font-display","--font-size-sm","--font-size-base","--font-size-lg","--lh-base","--radius-sm","--radius-md","--radius-card","--radius-btn","--shadow-sm","--shadow-card","--space-1","--space-2","--space-3","--space-4","--space-6","--space-8","--transition-fast","--transition-base"],rc={"--font-family":'system-ui, -apple-system, "Segoe UI", Roboto, sans-serif',"--font-display":'system-ui, -apple-system, "Segoe UI", Roboto, sans-serif',"--font-size-sm":"0.875rem","--font-size-base":"1rem","--font-size-lg":"1.25rem","--lh-base":"1.6","--radius-sm":"4px","--radius-md":"8px","--radius-card":"12px","--radius-btn":"8px","--space-1":"0.25rem","--space-2":"0.5rem","--space-3":"0.75rem","--space-4":"1rem","--space-6":"1.5rem","--space-8":"2rem","--transition-fast":"150ms ease","--transition-base":"240ms ease"},Xs={...rc,"--bg-body":"#f5f6f8","--bg-card":"#ffffff","--bg-elevated":"#eef1f5","--bg-hover":"#e3e8ef","--text-primary":"#161b22","--text-secondary":"#424d5c","--text-muted":"#596577","--primary":"#1b5e4a","--primary-light":"#e4f2ed","--primary-dark":"#124234","--accent":"#0f5c8c","--accent-light":"#e3f0f9","--accent-strong":"#0a4368","--on-accent":"#ffffff","--border-color":"#768396","--border-strong":"#4f5b6b","--focus-ring":"#0f5c8c","--success":"#166534","--success-soft":"#e6f5ec","--warning":"#854d0e","--warning-soft":"#fef3db","--danger":"#991b1b","--danger-soft":"#fdeaea","--info":"#1e4e8c","--info-soft":"#e8f0fb","--shadow-sm":"0 1px 2px rgba(15, 20, 26, 0.08)","--shadow-card":"0 2px 8px rgba(15, 20, 26, 0.10)"},Ys={...rc,"--bg-body":"#0f141a","--bg-card":"#18202a","--bg-elevated":"#212b38","--bg-hover":"#2b3848","--text-primary":"#f0f4f8","--text-secondary":"#c2cdd9","--text-muted":"#9aa8b8","--primary":"#56c7a3","--primary-light":"#1c3b33","--primary-dark":"#7adbb9","--accent":"#63b3ed","--accent-light":"#1b3247","--accent-strong":"#90cdf4","--on-accent":"#0f141a","--border-color":"#68788c","--border-strong":"#8fa0b5","--focus-ring":"#63b3ed","--success":"#5fd38d","--success-soft":"#163324","--warning":"#f6c453","--warning-soft":"#362a12","--danger":"#f88080","--danger-soft":"#3b1c20","--info":"#76b9f5","--info-soft":"#192e45","--shadow-sm":"0 1px 3px rgba(0, 0, 0, 0.35)","--shadow-card":"0 4px 12px rgba(0, 0, 0, 0.45)"},$c=["data-theme","data-palette","data-accent","data-style","data-density","data-bs-theme"];function Kc(n=document.documentElement){const e=(n.getAttribute("data-theme")??"").toLowerCase(),t=(n.getAttribute("data-bs-theme")??"").toLowerCase();return e==="dark"||t==="dark"?!0:e==="light"||t==="light"?!1:typeof window<"u"&&typeof window.matchMedia=="function"?window.matchMedia("(prefers-color-scheme: dark)").matches:!1}class Zc{slusaoci=new Set;posmatrac=null;medijaUpit=null;medijaSlusalac=null;kesiraniTokeni=new Map;ciljniKontejner=null;povezi(e){this.ciljniKontejner=e??null,this.osvezi(),typeof MutationObserver<"u"&&typeof document<"u"&&(this.posmatrac?.disconnect(),this.posmatrac=new MutationObserver(()=>{this.osvezi()}),this.posmatrac.observe(document.documentElement,{attributes:!0,attributeFilter:$c})),typeof window<"u"&&typeof window.matchMedia=="function"&&(this.medijaUpit=window.matchMedia("(prefers-color-scheme: dark)"),this.medijaSlusalac=()=>this.osvezi(),this.medijaUpit.addEventListener("change",this.medijaSlusalac))}odspoji(){this.posmatrac?.disconnect(),this.posmatrac=null,this.medijaUpit&&this.medijaSlusalac&&this.medijaUpit.removeEventListener("change",this.medijaSlusalac),this.medijaUpit=null,this.medijaSlusalac=null,this.slusaoci.clear()}pretplati(e){return this.slusaoci.add(e),()=>{this.slusaoci.delete(e)}}jeTamna(){return typeof document>"u"?!1:Kc(document.documentElement)}osvezi(){this.kesiraniTokeni.clear();const t=this.jeTamna()?Ys:Xs,i=typeof window<"u"&&typeof document<"u"?window.getComputedStyle(document.documentElement):null;for(const r of qc){const a=i?i.getPropertyValue(r).trim():"",s=a||t[r];this.kesiraniTokeni.set(r,s),this.ciljniKontejner&&(a?this.ciljniKontejner.style.removeProperty(r):this.ciljniKontejner.style.setProperty(r,t[r]))}for(const r of this.slusaoci)r(this)}token(e){const t=this.kesiraniTokeni.get(e);if(t)return t;const i=this.jeTamna()?Ys:Xs;if(typeof window<"u"&&typeof document<"u"){const r=window.getComputedStyle(document.documentElement).getPropertyValue(e).trim();if(r)return r}return i[e]}}const Xr=new Zc;/**
 * @license
 * Copyright 2010-2025 Three.js Authors
 * SPDX-License-Identifier: MIT
 */const bs="174",Jc=0,qs=1,Qc=2,ac=1,el=2,cn=3,An=0,Rt=1,kt=2,bn=0,gi=1,$s=2,Ks=3,Zs=4,tl=5,Hn=100,nl=101,il=102,rl=103,al=104,sl=200,ol=201,cl=202,ll=203,Ca=204,Pa=205,ul=206,dl=207,hl=208,fl=209,pl=210,ml=211,gl=212,_l=213,vl=214,Da=0,La=1,Ia=2,Mi=3,Ua=4,Na=5,Fa=6,za=7,sc=0,xl=1,Ml=2,Tn=0,Sl=1,El=2,yl=3,bl=4,Tl=5,Al=6,wl=7,oc=300,Si=301,Ei=302,ka=303,Oa=304,Or=306,Ba=1e3,Gn=1001,Ha=1002,qt=1003,Rl=1004,qi=1005,Kt=1006,Yr=1007,jn=1008,pn=1009,cc=1010,lc=1011,Oi=1012,Ts=1013,Yn=1014,un=1015,Bi=1016,As=1017,ws=1018,yi=1020,uc=35902,dc=1021,hc=1022,Yt=1023,fc=1024,pc=1025,_i=1026,bi=1027,mc=1028,Rs=1029,gc=1030,Cs=1031,Ps=1033,Sr=33776,Er=33777,yr=33778,br=33779,Va=35840,Ga=35841,ja=35842,Wa=35843,Xa=36196,Ya=37492,qa=37496,$a=37808,Ka=37809,Za=37810,Ja=37811,Qa=37812,es=37813,ts=37814,ns=37815,is=37816,rs=37817,as=37818,ss=37819,os=37820,cs=37821,Tr=36492,ls=36494,us=36495,_c=36283,ds=36284,hs=36285,fs=36286,Cl=3200,Pl=3201,vc=0,Dl=1,yn="",Lt="srgb",Ti="srgb-linear",Pr="linear",et="srgb",Zn=7680,Js=519,Ll=512,Il=513,Ul=514,xc=515,Nl=516,Fl=517,zl=518,kl=519,Qs=35044,eo="300 es",dn=2e3,Dr=2001;class wi{addEventListener(e,t){this._listeners===void 0&&(this._listeners={});const i=this._listeners;i[e]===void 0&&(i[e]=[]),i[e].indexOf(t)===-1&&i[e].push(t)}hasEventListener(e,t){const i=this._listeners;return i===void 0?!1:i[e]!==void 0&&i[e].indexOf(t)!==-1}removeEventListener(e,t){const i=this._listeners;if(i===void 0)return;const r=i[e];if(r!==void 0){const a=r.indexOf(t);a!==-1&&r.splice(a,1)}}dispatchEvent(e){const t=this._listeners;if(t===void 0)return;const i=t[e.type];if(i!==void 0){e.target=this;const r=i.slice(0);for(let a=0,s=r.length;a<s;a++)r[a].call(this,e);e.target=null}}}const xt=["00","01","02","03","04","05","06","07","08","09","0a","0b","0c","0d","0e","0f","10","11","12","13","14","15","16","17","18","19","1a","1b","1c","1d","1e","1f","20","21","22","23","24","25","26","27","28","29","2a","2b","2c","2d","2e","2f","30","31","32","33","34","35","36","37","38","39","3a","3b","3c","3d","3e","3f","40","41","42","43","44","45","46","47","48","49","4a","4b","4c","4d","4e","4f","50","51","52","53","54","55","56","57","58","59","5a","5b","5c","5d","5e","5f","60","61","62","63","64","65","66","67","68","69","6a","6b","6c","6d","6e","6f","70","71","72","73","74","75","76","77","78","79","7a","7b","7c","7d","7e","7f","80","81","82","83","84","85","86","87","88","89","8a","8b","8c","8d","8e","8f","90","91","92","93","94","95","96","97","98","99","9a","9b","9c","9d","9e","9f","a0","a1","a2","a3","a4","a5","a6","a7","a8","a9","aa","ab","ac","ad","ae","af","b0","b1","b2","b3","b4","b5","b6","b7","b8","b9","ba","bb","bc","bd","be","bf","c0","c1","c2","c3","c4","c5","c6","c7","c8","c9","ca","cb","cc","cd","ce","cf","d0","d1","d2","d3","d4","d5","d6","d7","d8","d9","da","db","dc","dd","de","df","e0","e1","e2","e3","e4","e5","e6","e7","e8","e9","ea","eb","ec","ed","ee","ef","f0","f1","f2","f3","f4","f5","f6","f7","f8","f9","fa","fb","fc","fd","fe","ff"],Ar=Math.PI/180,ps=180/Math.PI;function Hi(){const n=Math.random()*4294967295|0,e=Math.random()*4294967295|0,t=Math.random()*4294967295|0,i=Math.random()*4294967295|0;return(xt[n&255]+xt[n>>8&255]+xt[n>>16&255]+xt[n>>24&255]+"-"+xt[e&255]+xt[e>>8&255]+"-"+xt[e>>16&15|64]+xt[e>>24&255]+"-"+xt[t&63|128]+xt[t>>8&255]+"-"+xt[t>>16&255]+xt[t>>24&255]+xt[i&255]+xt[i>>8&255]+xt[i>>16&255]+xt[i>>24&255]).toLowerCase()}function je(n,e,t){return Math.max(e,Math.min(t,n))}function Ol(n,e){return(n%e+e)%e}function qr(n,e,t){return(1-t)*n+t*e}function Di(n,e){switch(e.constructor){case Float32Array:return n;case Uint32Array:return n/4294967295;case Uint16Array:return n/65535;case Uint8Array:return n/255;case Int32Array:return Math.max(n/2147483647,-1);case Int16Array:return Math.max(n/32767,-1);case Int8Array:return Math.max(n/127,-1);default:throw new Error("Invalid component type.")}}function At(n,e){switch(e.constructor){case Float32Array:return n;case Uint32Array:return Math.round(n*4294967295);case Uint16Array:return Math.round(n*65535);case Uint8Array:return Math.round(n*255);case Int32Array:return Math.round(n*2147483647);case Int16Array:return Math.round(n*32767);case Int8Array:return Math.round(n*127);default:throw new Error("Invalid component type.")}}class Xe{constructor(e=0,t=0){Xe.prototype.isVector2=!0,this.x=e,this.y=t}get width(){return this.x}set width(e){this.x=e}get height(){return this.y}set height(e){this.y=e}set(e,t){return this.x=e,this.y=t,this}setScalar(e){return this.x=e,this.y=e,this}setX(e){return this.x=e,this}setY(e){return this.y=e,this}setComponent(e,t){switch(e){case 0:this.x=t;break;case 1:this.y=t;break;default:throw new Error("index is out of range: "+e)}return this}getComponent(e){switch(e){case 0:return this.x;case 1:return this.y;default:throw new Error("index is out of range: "+e)}}clone(){return new this.constructor(this.x,this.y)}copy(e){return this.x=e.x,this.y=e.y,this}add(e){return this.x+=e.x,this.y+=e.y,this}addScalar(e){return this.x+=e,this.y+=e,this}addVectors(e,t){return this.x=e.x+t.x,this.y=e.y+t.y,this}addScaledVector(e,t){return this.x+=e.x*t,this.y+=e.y*t,this}sub(e){return this.x-=e.x,this.y-=e.y,this}subScalar(e){return this.x-=e,this.y-=e,this}subVectors(e,t){return this.x=e.x-t.x,this.y=e.y-t.y,this}multiply(e){return this.x*=e.x,this.y*=e.y,this}multiplyScalar(e){return this.x*=e,this.y*=e,this}divide(e){return this.x/=e.x,this.y/=e.y,this}divideScalar(e){return this.multiplyScalar(1/e)}applyMatrix3(e){const t=this.x,i=this.y,r=e.elements;return this.x=r[0]*t+r[3]*i+r[6],this.y=r[1]*t+r[4]*i+r[7],this}min(e){return this.x=Math.min(this.x,e.x),this.y=Math.min(this.y,e.y),this}max(e){return this.x=Math.max(this.x,e.x),this.y=Math.max(this.y,e.y),this}clamp(e,t){return this.x=je(this.x,e.x,t.x),this.y=je(this.y,e.y,t.y),this}clampScalar(e,t){return this.x=je(this.x,e,t),this.y=je(this.y,e,t),this}clampLength(e,t){const i=this.length();return this.divideScalar(i||1).multiplyScalar(je(i,e,t))}floor(){return this.x=Math.floor(this.x),this.y=Math.floor(this.y),this}ceil(){return this.x=Math.ceil(this.x),this.y=Math.ceil(this.y),this}round(){return this.x=Math.round(this.x),this.y=Math.round(this.y),this}roundToZero(){return this.x=Math.trunc(this.x),this.y=Math.trunc(this.y),this}negate(){return this.x=-this.x,this.y=-this.y,this}dot(e){return this.x*e.x+this.y*e.y}cross(e){return this.x*e.y-this.y*e.x}lengthSq(){return this.x*this.x+this.y*this.y}length(){return Math.sqrt(this.x*this.x+this.y*this.y)}manhattanLength(){return Math.abs(this.x)+Math.abs(this.y)}normalize(){return this.divideScalar(this.length()||1)}angle(){return Math.atan2(-this.y,-this.x)+Math.PI}angleTo(e){const t=Math.sqrt(this.lengthSq()*e.lengthSq());if(t===0)return Math.PI/2;const i=this.dot(e)/t;return Math.acos(je(i,-1,1))}distanceTo(e){return Math.sqrt(this.distanceToSquared(e))}distanceToSquared(e){const t=this.x-e.x,i=this.y-e.y;return t*t+i*i}manhattanDistanceTo(e){return Math.abs(this.x-e.x)+Math.abs(this.y-e.y)}setLength(e){return this.normalize().multiplyScalar(e)}lerp(e,t){return this.x+=(e.x-this.x)*t,this.y+=(e.y-this.y)*t,this}lerpVectors(e,t,i){return this.x=e.x+(t.x-e.x)*i,this.y=e.y+(t.y-e.y)*i,this}equals(e){return e.x===this.x&&e.y===this.y}fromArray(e,t=0){return this.x=e[t],this.y=e[t+1],this}toArray(e=[],t=0){return e[t]=this.x,e[t+1]=this.y,e}fromBufferAttribute(e,t){return this.x=e.getX(t),this.y=e.getY(t),this}rotateAround(e,t){const i=Math.cos(t),r=Math.sin(t),a=this.x-e.x,s=this.y-e.y;return this.x=a*i-s*r+e.x,this.y=a*r+s*i+e.y,this}random(){return this.x=Math.random(),this.y=Math.random(),this}*[Symbol.iterator](){yield this.x,yield this.y}}class Be{constructor(e,t,i,r,a,s,o,c,l){Be.prototype.isMatrix3=!0,this.elements=[1,0,0,0,1,0,0,0,1],e!==void 0&&this.set(e,t,i,r,a,s,o,c,l)}set(e,t,i,r,a,s,o,c,l){const d=this.elements;return d[0]=e,d[1]=r,d[2]=o,d[3]=t,d[4]=a,d[5]=c,d[6]=i,d[7]=s,d[8]=l,this}identity(){return this.set(1,0,0,0,1,0,0,0,1),this}copy(e){const t=this.elements,i=e.elements;return t[0]=i[0],t[1]=i[1],t[2]=i[2],t[3]=i[3],t[4]=i[4],t[5]=i[5],t[6]=i[6],t[7]=i[7],t[8]=i[8],this}extractBasis(e,t,i){return e.setFromMatrix3Column(this,0),t.setFromMatrix3Column(this,1),i.setFromMatrix3Column(this,2),this}setFromMatrix4(e){const t=e.elements;return this.set(t[0],t[4],t[8],t[1],t[5],t[9],t[2],t[6],t[10]),this}multiply(e){return this.multiplyMatrices(this,e)}premultiply(e){return this.multiplyMatrices(e,this)}multiplyMatrices(e,t){const i=e.elements,r=t.elements,a=this.elements,s=i[0],o=i[3],c=i[6],l=i[1],d=i[4],h=i[7],f=i[2],m=i[5],g=i[8],_=r[0],p=r[3],u=r[6],w=r[1],b=r[4],S=r[7],T=r[2],y=r[5],A=r[8];return a[0]=s*_+o*w+c*T,a[3]=s*p+o*b+c*y,a[6]=s*u+o*S+c*A,a[1]=l*_+d*w+h*T,a[4]=l*p+d*b+h*y,a[7]=l*u+d*S+h*A,a[2]=f*_+m*w+g*T,a[5]=f*p+m*b+g*y,a[8]=f*u+m*S+g*A,this}multiplyScalar(e){const t=this.elements;return t[0]*=e,t[3]*=e,t[6]*=e,t[1]*=e,t[4]*=e,t[7]*=e,t[2]*=e,t[5]*=e,t[8]*=e,this}determinant(){const e=this.elements,t=e[0],i=e[1],r=e[2],a=e[3],s=e[4],o=e[5],c=e[6],l=e[7],d=e[8];return t*s*d-t*o*l-i*a*d+i*o*c+r*a*l-r*s*c}invert(){const e=this.elements,t=e[0],i=e[1],r=e[2],a=e[3],s=e[4],o=e[5],c=e[6],l=e[7],d=e[8],h=d*s-o*l,f=o*c-d*a,m=l*a-s*c,g=t*h+i*f+r*m;if(g===0)return this.set(0,0,0,0,0,0,0,0,0);const _=1/g;return e[0]=h*_,e[1]=(r*l-d*i)*_,e[2]=(o*i-r*s)*_,e[3]=f*_,e[4]=(d*t-r*c)*_,e[5]=(r*a-o*t)*_,e[6]=m*_,e[7]=(i*c-l*t)*_,e[8]=(s*t-i*a)*_,this}transpose(){let e;const t=this.elements;return e=t[1],t[1]=t[3],t[3]=e,e=t[2],t[2]=t[6],t[6]=e,e=t[5],t[5]=t[7],t[7]=e,this}getNormalMatrix(e){return this.setFromMatrix4(e).invert().transpose()}transposeIntoArray(e){const t=this.elements;return e[0]=t[0],e[1]=t[3],e[2]=t[6],e[3]=t[1],e[4]=t[4],e[5]=t[7],e[6]=t[2],e[7]=t[5],e[8]=t[8],this}setUvTransform(e,t,i,r,a,s,o){const c=Math.cos(a),l=Math.sin(a);return this.set(i*c,i*l,-i*(c*s+l*o)+s+e,-r*l,r*c,-r*(-l*s+c*o)+o+t,0,0,1),this}scale(e,t){return this.premultiply($r.makeScale(e,t)),this}rotate(e){return this.premultiply($r.makeRotation(-e)),this}translate(e,t){return this.premultiply($r.makeTranslation(e,t)),this}makeTranslation(e,t){return e.isVector2?this.set(1,0,e.x,0,1,e.y,0,0,1):this.set(1,0,e,0,1,t,0,0,1),this}makeRotation(e){const t=Math.cos(e),i=Math.sin(e);return this.set(t,-i,0,i,t,0,0,0,1),this}makeScale(e,t){return this.set(e,0,0,0,t,0,0,0,1),this}equals(e){const t=this.elements,i=e.elements;for(let r=0;r<9;r++)if(t[r]!==i[r])return!1;return!0}fromArray(e,t=0){for(let i=0;i<9;i++)this.elements[i]=e[i+t];return this}toArray(e=[],t=0){const i=this.elements;return e[t]=i[0],e[t+1]=i[1],e[t+2]=i[2],e[t+3]=i[3],e[t+4]=i[4],e[t+5]=i[5],e[t+6]=i[6],e[t+7]=i[7],e[t+8]=i[8],e}clone(){return new this.constructor().fromArray(this.elements)}}const $r=new Be;function Mc(n){for(let e=n.length-1;e>=0;--e)if(n[e]>=65535)return!0;return!1}function Lr(n){return document.createElementNS("http://www.w3.org/1999/xhtml",n)}function Bl(){const n=Lr("canvas");return n.style.display="block",n}const to={};function Fn(n){n in to||(to[n]=!0,console.warn(n))}function Hl(n,e,t){return new Promise(function(i,r){function a(){switch(n.clientWaitSync(e,n.SYNC_FLUSH_COMMANDS_BIT,0)){case n.WAIT_FAILED:r();break;case n.TIMEOUT_EXPIRED:setTimeout(a,t);break;default:i()}}setTimeout(a,t)})}function Vl(n){const e=n.elements;e[2]=.5*e[2]+.5*e[3],e[6]=.5*e[6]+.5*e[7],e[10]=.5*e[10]+.5*e[11],e[14]=.5*e[14]+.5*e[15]}function Gl(n){const e=n.elements;e[11]===-1?(e[10]=-e[10]-1,e[14]=-e[14]):(e[10]=-e[10],e[14]=-e[14]+1)}const no=new Be().set(.4123908,.3575843,.1804808,.212639,.7151687,.0721923,.0193308,.1191948,.9505322),io=new Be().set(3.2409699,-1.5373832,-.4986108,-.9692436,1.8759675,.0415551,.0556301,-.203977,1.0569715);function jl(){const n={enabled:!0,workingColorSpace:Ti,spaces:{},convert:function(r,a,s){return this.enabled===!1||a===s||!a||!s||(this.spaces[a].transfer===et&&(r.r=fn(r.r),r.g=fn(r.g),r.b=fn(r.b)),this.spaces[a].primaries!==this.spaces[s].primaries&&(r.applyMatrix3(this.spaces[a].toXYZ),r.applyMatrix3(this.spaces[s].fromXYZ)),this.spaces[s].transfer===et&&(r.r=vi(r.r),r.g=vi(r.g),r.b=vi(r.b))),r},fromWorkingColorSpace:function(r,a){return this.convert(r,this.workingColorSpace,a)},toWorkingColorSpace:function(r,a){return this.convert(r,a,this.workingColorSpace)},getPrimaries:function(r){return this.spaces[r].primaries},getTransfer:function(r){return r===yn?Pr:this.spaces[r].transfer},getLuminanceCoefficients:function(r,a=this.workingColorSpace){return r.fromArray(this.spaces[a].luminanceCoefficients)},define:function(r){Object.assign(this.spaces,r)},_getMatrix:function(r,a,s){return r.copy(this.spaces[a].toXYZ).multiply(this.spaces[s].fromXYZ)},_getDrawingBufferColorSpace:function(r){return this.spaces[r].outputColorSpaceConfig.drawingBufferColorSpace},_getUnpackColorSpace:function(r=this.workingColorSpace){return this.spaces[r].workingColorSpaceConfig.unpackColorSpace}},e=[.64,.33,.3,.6,.15,.06],t=[.2126,.7152,.0722],i=[.3127,.329];return n.define({[Ti]:{primaries:e,whitePoint:i,transfer:Pr,toXYZ:no,fromXYZ:io,luminanceCoefficients:t,workingColorSpaceConfig:{unpackColorSpace:Lt},outputColorSpaceConfig:{drawingBufferColorSpace:Lt}},[Lt]:{primaries:e,whitePoint:i,transfer:et,toXYZ:no,fromXYZ:io,luminanceCoefficients:t,outputColorSpaceConfig:{drawingBufferColorSpace:Lt}}}),n}const Ke=jl();function fn(n){return n<.04045?n*.0773993808:Math.pow(n*.9478672986+.0521327014,2.4)}function vi(n){return n<.0031308?n*12.92:1.055*Math.pow(n,.41666)-.055}let Jn;class Wl{static getDataURL(e){if(/^data:/i.test(e.src)||typeof HTMLCanvasElement>"u")return e.src;let t;if(e instanceof HTMLCanvasElement)t=e;else{Jn===void 0&&(Jn=Lr("canvas")),Jn.width=e.width,Jn.height=e.height;const i=Jn.getContext("2d");e instanceof ImageData?i.putImageData(e,0,0):i.drawImage(e,0,0,e.width,e.height),t=Jn}return t.toDataURL("image/png")}static sRGBToLinear(e){if(typeof HTMLImageElement<"u"&&e instanceof HTMLImageElement||typeof HTMLCanvasElement<"u"&&e instanceof HTMLCanvasElement||typeof ImageBitmap<"u"&&e instanceof ImageBitmap){const t=Lr("canvas");t.width=e.width,t.height=e.height;const i=t.getContext("2d");i.drawImage(e,0,0,e.width,e.height);const r=i.getImageData(0,0,e.width,e.height),a=r.data;for(let s=0;s<a.length;s++)a[s]=fn(a[s]/255)*255;return i.putImageData(r,0,0),t}else if(e.data){const t=e.data.slice(0);for(let i=0;i<t.length;i++)t instanceof Uint8Array||t instanceof Uint8ClampedArray?t[i]=Math.floor(fn(t[i]/255)*255):t[i]=fn(t[i]);return{data:t,width:e.width,height:e.height}}else return console.warn("THREE.ImageUtils.sRGBToLinear(): Unsupported image type. No color space conversion applied."),e}}let Xl=0;class Ds{constructor(e=null){this.isSource=!0,Object.defineProperty(this,"id",{value:Xl++}),this.uuid=Hi(),this.data=e,this.dataReady=!0,this.version=0}set needsUpdate(e){e===!0&&this.version++}toJSON(e){const t=e===void 0||typeof e=="string";if(!t&&e.images[this.uuid]!==void 0)return e.images[this.uuid];const i={uuid:this.uuid,url:""},r=this.data;if(r!==null){let a;if(Array.isArray(r)){a=[];for(let s=0,o=r.length;s<o;s++)r[s].isDataTexture?a.push(Kr(r[s].image)):a.push(Kr(r[s]))}else a=Kr(r);i.url=a}return t||(e.images[this.uuid]=i),i}}function Kr(n){return typeof HTMLImageElement<"u"&&n instanceof HTMLImageElement||typeof HTMLCanvasElement<"u"&&n instanceof HTMLCanvasElement||typeof ImageBitmap<"u"&&n instanceof ImageBitmap?Wl.getDataURL(n):n.data?{data:Array.from(n.data),width:n.width,height:n.height,type:n.data.constructor.name}:(console.warn("THREE.Texture: Unable to serialize Texture."),{})}let Yl=0;class bt extends wi{constructor(e=bt.DEFAULT_IMAGE,t=bt.DEFAULT_MAPPING,i=Gn,r=Gn,a=Kt,s=jn,o=Yt,c=pn,l=bt.DEFAULT_ANISOTROPY,d=yn){super(),this.isTexture=!0,Object.defineProperty(this,"id",{value:Yl++}),this.uuid=Hi(),this.name="",this.source=new Ds(e),this.mipmaps=[],this.mapping=t,this.channel=0,this.wrapS=i,this.wrapT=r,this.magFilter=a,this.minFilter=s,this.anisotropy=l,this.format=o,this.internalFormat=null,this.type=c,this.offset=new Xe(0,0),this.repeat=new Xe(1,1),this.center=new Xe(0,0),this.rotation=0,this.matrixAutoUpdate=!0,this.matrix=new Be,this.generateMipmaps=!0,this.premultiplyAlpha=!1,this.flipY=!0,this.unpackAlignment=4,this.colorSpace=d,this.userData={},this.version=0,this.onUpdate=null,this.renderTarget=null,this.isRenderTargetTexture=!1,this.pmremVersion=0}get image(){return this.source.data}set image(e=null){this.source.data=e}updateMatrix(){this.matrix.setUvTransform(this.offset.x,this.offset.y,this.repeat.x,this.repeat.y,this.rotation,this.center.x,this.center.y)}clone(){return new this.constructor().copy(this)}copy(e){return this.name=e.name,this.source=e.source,this.mipmaps=e.mipmaps.slice(0),this.mapping=e.mapping,this.channel=e.channel,this.wrapS=e.wrapS,this.wrapT=e.wrapT,this.magFilter=e.magFilter,this.minFilter=e.minFilter,this.anisotropy=e.anisotropy,this.format=e.format,this.internalFormat=e.internalFormat,this.type=e.type,this.offset.copy(e.offset),this.repeat.copy(e.repeat),this.center.copy(e.center),this.rotation=e.rotation,this.matrixAutoUpdate=e.matrixAutoUpdate,this.matrix.copy(e.matrix),this.generateMipmaps=e.generateMipmaps,this.premultiplyAlpha=e.premultiplyAlpha,this.flipY=e.flipY,this.unpackAlignment=e.unpackAlignment,this.colorSpace=e.colorSpace,this.renderTarget=e.renderTarget,this.isRenderTargetTexture=e.isRenderTargetTexture,this.userData=JSON.parse(JSON.stringify(e.userData)),this.needsUpdate=!0,this}toJSON(e){const t=e===void 0||typeof e=="string";if(!t&&e.textures[this.uuid]!==void 0)return e.textures[this.uuid];const i={metadata:{version:4.6,type:"Texture",generator:"Texture.toJSON"},uuid:this.uuid,name:this.name,image:this.source.toJSON(e).uuid,mapping:this.mapping,channel:this.channel,repeat:[this.repeat.x,this.repeat.y],offset:[this.offset.x,this.offset.y],center:[this.center.x,this.center.y],rotation:this.rotation,wrap:[this.wrapS,this.wrapT],format:this.format,internalFormat:this.internalFormat,type:this.type,colorSpace:this.colorSpace,minFilter:this.minFilter,magFilter:this.magFilter,anisotropy:this.anisotropy,flipY:this.flipY,generateMipmaps:this.generateMipmaps,premultiplyAlpha:this.premultiplyAlpha,unpackAlignment:this.unpackAlignment};return Object.keys(this.userData).length>0&&(i.userData=this.userData),t||(e.textures[this.uuid]=i),i}dispose(){this.dispatchEvent({type:"dispose"})}transformUv(e){if(this.mapping!==oc)return e;if(e.applyMatrix3(this.matrix),e.x<0||e.x>1)switch(this.wrapS){case Ba:e.x=e.x-Math.floor(e.x);break;case Gn:e.x=e.x<0?0:1;break;case Ha:Math.abs(Math.floor(e.x)%2)===1?e.x=Math.ceil(e.x)-e.x:e.x=e.x-Math.floor(e.x);break}if(e.y<0||e.y>1)switch(this.wrapT){case Ba:e.y=e.y-Math.floor(e.y);break;case Gn:e.y=e.y<0?0:1;break;case Ha:Math.abs(Math.floor(e.y)%2)===1?e.y=Math.ceil(e.y)-e.y:e.y=e.y-Math.floor(e.y);break}return this.flipY&&(e.y=1-e.y),e}set needsUpdate(e){e===!0&&(this.version++,this.source.needsUpdate=!0)}set needsPMREMUpdate(e){e===!0&&this.pmremVersion++}}bt.DEFAULT_IMAGE=null;bt.DEFAULT_MAPPING=oc;bt.DEFAULT_ANISOTROPY=1;class lt{constructor(e=0,t=0,i=0,r=1){lt.prototype.isVector4=!0,this.x=e,this.y=t,this.z=i,this.w=r}get width(){return this.z}set width(e){this.z=e}get height(){return this.w}set height(e){this.w=e}set(e,t,i,r){return this.x=e,this.y=t,this.z=i,this.w=r,this}setScalar(e){return this.x=e,this.y=e,this.z=e,this.w=e,this}setX(e){return this.x=e,this}setY(e){return this.y=e,this}setZ(e){return this.z=e,this}setW(e){return this.w=e,this}setComponent(e,t){switch(e){case 0:this.x=t;break;case 1:this.y=t;break;case 2:this.z=t;break;case 3:this.w=t;break;default:throw new Error("index is out of range: "+e)}return this}getComponent(e){switch(e){case 0:return this.x;case 1:return this.y;case 2:return this.z;case 3:return this.w;default:throw new Error("index is out of range: "+e)}}clone(){return new this.constructor(this.x,this.y,this.z,this.w)}copy(e){return this.x=e.x,this.y=e.y,this.z=e.z,this.w=e.w!==void 0?e.w:1,this}add(e){return this.x+=e.x,this.y+=e.y,this.z+=e.z,this.w+=e.w,this}addScalar(e){return this.x+=e,this.y+=e,this.z+=e,this.w+=e,this}addVectors(e,t){return this.x=e.x+t.x,this.y=e.y+t.y,this.z=e.z+t.z,this.w=e.w+t.w,this}addScaledVector(e,t){return this.x+=e.x*t,this.y+=e.y*t,this.z+=e.z*t,this.w+=e.w*t,this}sub(e){return this.x-=e.x,this.y-=e.y,this.z-=e.z,this.w-=e.w,this}subScalar(e){return this.x-=e,this.y-=e,this.z-=e,this.w-=e,this}subVectors(e,t){return this.x=e.x-t.x,this.y=e.y-t.y,this.z=e.z-t.z,this.w=e.w-t.w,this}multiply(e){return this.x*=e.x,this.y*=e.y,this.z*=e.z,this.w*=e.w,this}multiplyScalar(e){return this.x*=e,this.y*=e,this.z*=e,this.w*=e,this}applyMatrix4(e){const t=this.x,i=this.y,r=this.z,a=this.w,s=e.elements;return this.x=s[0]*t+s[4]*i+s[8]*r+s[12]*a,this.y=s[1]*t+s[5]*i+s[9]*r+s[13]*a,this.z=s[2]*t+s[6]*i+s[10]*r+s[14]*a,this.w=s[3]*t+s[7]*i+s[11]*r+s[15]*a,this}divide(e){return this.x/=e.x,this.y/=e.y,this.z/=e.z,this.w/=e.w,this}divideScalar(e){return this.multiplyScalar(1/e)}setAxisAngleFromQuaternion(e){this.w=2*Math.acos(e.w);const t=Math.sqrt(1-e.w*e.w);return t<1e-4?(this.x=1,this.y=0,this.z=0):(this.x=e.x/t,this.y=e.y/t,this.z=e.z/t),this}setAxisAngleFromRotationMatrix(e){let t,i,r,a;const c=e.elements,l=c[0],d=c[4],h=c[8],f=c[1],m=c[5],g=c[9],_=c[2],p=c[6],u=c[10];if(Math.abs(d-f)<.01&&Math.abs(h-_)<.01&&Math.abs(g-p)<.01){if(Math.abs(d+f)<.1&&Math.abs(h+_)<.1&&Math.abs(g+p)<.1&&Math.abs(l+m+u-3)<.1)return this.set(1,0,0,0),this;t=Math.PI;const b=(l+1)/2,S=(m+1)/2,T=(u+1)/2,y=(d+f)/4,A=(h+_)/4,D=(g+p)/4;return b>S&&b>T?b<.01?(i=0,r=.707106781,a=.707106781):(i=Math.sqrt(b),r=y/i,a=A/i):S>T?S<.01?(i=.707106781,r=0,a=.707106781):(r=Math.sqrt(S),i=y/r,a=D/r):T<.01?(i=.707106781,r=.707106781,a=0):(a=Math.sqrt(T),i=A/a,r=D/a),this.set(i,r,a,t),this}let w=Math.sqrt((p-g)*(p-g)+(h-_)*(h-_)+(f-d)*(f-d));return Math.abs(w)<.001&&(w=1),this.x=(p-g)/w,this.y=(h-_)/w,this.z=(f-d)/w,this.w=Math.acos((l+m+u-1)/2),this}setFromMatrixPosition(e){const t=e.elements;return this.x=t[12],this.y=t[13],this.z=t[14],this.w=t[15],this}min(e){return this.x=Math.min(this.x,e.x),this.y=Math.min(this.y,e.y),this.z=Math.min(this.z,e.z),this.w=Math.min(this.w,e.w),this}max(e){return this.x=Math.max(this.x,e.x),this.y=Math.max(this.y,e.y),this.z=Math.max(this.z,e.z),this.w=Math.max(this.w,e.w),this}clamp(e,t){return this.x=je(this.x,e.x,t.x),this.y=je(this.y,e.y,t.y),this.z=je(this.z,e.z,t.z),this.w=je(this.w,e.w,t.w),this}clampScalar(e,t){return this.x=je(this.x,e,t),this.y=je(this.y,e,t),this.z=je(this.z,e,t),this.w=je(this.w,e,t),this}clampLength(e,t){const i=this.length();return this.divideScalar(i||1).multiplyScalar(je(i,e,t))}floor(){return this.x=Math.floor(this.x),this.y=Math.floor(this.y),this.z=Math.floor(this.z),this.w=Math.floor(this.w),this}ceil(){return this.x=Math.ceil(this.x),this.y=Math.ceil(this.y),this.z=Math.ceil(this.z),this.w=Math.ceil(this.w),this}round(){return this.x=Math.round(this.x),this.y=Math.round(this.y),this.z=Math.round(this.z),this.w=Math.round(this.w),this}roundToZero(){return this.x=Math.trunc(this.x),this.y=Math.trunc(this.y),this.z=Math.trunc(this.z),this.w=Math.trunc(this.w),this}negate(){return this.x=-this.x,this.y=-this.y,this.z=-this.z,this.w=-this.w,this}dot(e){return this.x*e.x+this.y*e.y+this.z*e.z+this.w*e.w}lengthSq(){return this.x*this.x+this.y*this.y+this.z*this.z+this.w*this.w}length(){return Math.sqrt(this.x*this.x+this.y*this.y+this.z*this.z+this.w*this.w)}manhattanLength(){return Math.abs(this.x)+Math.abs(this.y)+Math.abs(this.z)+Math.abs(this.w)}normalize(){return this.divideScalar(this.length()||1)}setLength(e){return this.normalize().multiplyScalar(e)}lerp(e,t){return this.x+=(e.x-this.x)*t,this.y+=(e.y-this.y)*t,this.z+=(e.z-this.z)*t,this.w+=(e.w-this.w)*t,this}lerpVectors(e,t,i){return this.x=e.x+(t.x-e.x)*i,this.y=e.y+(t.y-e.y)*i,this.z=e.z+(t.z-e.z)*i,this.w=e.w+(t.w-e.w)*i,this}equals(e){return e.x===this.x&&e.y===this.y&&e.z===this.z&&e.w===this.w}fromArray(e,t=0){return this.x=e[t],this.y=e[t+1],this.z=e[t+2],this.w=e[t+3],this}toArray(e=[],t=0){return e[t]=this.x,e[t+1]=this.y,e[t+2]=this.z,e[t+3]=this.w,e}fromBufferAttribute(e,t){return this.x=e.getX(t),this.y=e.getY(t),this.z=e.getZ(t),this.w=e.getW(t),this}random(){return this.x=Math.random(),this.y=Math.random(),this.z=Math.random(),this.w=Math.random(),this}*[Symbol.iterator](){yield this.x,yield this.y,yield this.z,yield this.w}}class ql extends wi{constructor(e=1,t=1,i={}){super(),this.isRenderTarget=!0,this.width=e,this.height=t,this.depth=1,this.scissor=new lt(0,0,e,t),this.scissorTest=!1,this.viewport=new lt(0,0,e,t);const r={width:e,height:t,depth:1};i=Object.assign({generateMipmaps:!1,internalFormat:null,minFilter:Kt,depthBuffer:!0,stencilBuffer:!1,resolveDepthBuffer:!0,resolveStencilBuffer:!0,depthTexture:null,samples:0,count:1},i);const a=new bt(r,i.mapping,i.wrapS,i.wrapT,i.magFilter,i.minFilter,i.format,i.type,i.anisotropy,i.colorSpace);a.flipY=!1,a.generateMipmaps=i.generateMipmaps,a.internalFormat=i.internalFormat,this.textures=[];const s=i.count;for(let o=0;o<s;o++)this.textures[o]=a.clone(),this.textures[o].isRenderTargetTexture=!0,this.textures[o].renderTarget=this;this.depthBuffer=i.depthBuffer,this.stencilBuffer=i.stencilBuffer,this.resolveDepthBuffer=i.resolveDepthBuffer,this.resolveStencilBuffer=i.resolveStencilBuffer,this._depthTexture=null,this.depthTexture=i.depthTexture,this.samples=i.samples}get texture(){return this.textures[0]}set texture(e){this.textures[0]=e}set depthTexture(e){this._depthTexture!==null&&(this._depthTexture.renderTarget=null),e!==null&&(e.renderTarget=this),this._depthTexture=e}get depthTexture(){return this._depthTexture}setSize(e,t,i=1){if(this.width!==e||this.height!==t||this.depth!==i){this.width=e,this.height=t,this.depth=i;for(let r=0,a=this.textures.length;r<a;r++)this.textures[r].image.width=e,this.textures[r].image.height=t,this.textures[r].image.depth=i;this.dispose()}this.viewport.set(0,0,e,t),this.scissor.set(0,0,e,t)}clone(){return new this.constructor().copy(this)}copy(e){this.width=e.width,this.height=e.height,this.depth=e.depth,this.scissor.copy(e.scissor),this.scissorTest=e.scissorTest,this.viewport.copy(e.viewport),this.textures.length=0;for(let t=0,i=e.textures.length;t<i;t++){this.textures[t]=e.textures[t].clone(),this.textures[t].isRenderTargetTexture=!0,this.textures[t].renderTarget=this;const r=Object.assign({},e.textures[t].image);this.textures[t].source=new Ds(r)}return this.depthBuffer=e.depthBuffer,this.stencilBuffer=e.stencilBuffer,this.resolveDepthBuffer=e.resolveDepthBuffer,this.resolveStencilBuffer=e.resolveStencilBuffer,e.depthTexture!==null&&(this.depthTexture=e.depthTexture.clone()),this.samples=e.samples,this}dispose(){this.dispatchEvent({type:"dispose"})}}class qn extends ql{constructor(e=1,t=1,i={}){super(e,t,i),this.isWebGLRenderTarget=!0}}class Sc extends bt{constructor(e=null,t=1,i=1,r=1){super(null),this.isDataArrayTexture=!0,this.image={data:e,width:t,height:i,depth:r},this.magFilter=qt,this.minFilter=qt,this.wrapR=Gn,this.generateMipmaps=!1,this.flipY=!1,this.unpackAlignment=1,this.layerUpdates=new Set}addLayerUpdate(e){this.layerUpdates.add(e)}clearLayerUpdates(){this.layerUpdates.clear()}}class $l extends bt{constructor(e=null,t=1,i=1,r=1){super(null),this.isData3DTexture=!0,this.image={data:e,width:t,height:i,depth:r},this.magFilter=qt,this.minFilter=qt,this.wrapR=Gn,this.generateMipmaps=!1,this.flipY=!1,this.unpackAlignment=1}}class Vi{constructor(e=0,t=0,i=0,r=1){this.isQuaternion=!0,this._x=e,this._y=t,this._z=i,this._w=r}static slerpFlat(e,t,i,r,a,s,o){let c=i[r+0],l=i[r+1],d=i[r+2],h=i[r+3];const f=a[s+0],m=a[s+1],g=a[s+2],_=a[s+3];if(o===0){e[t+0]=c,e[t+1]=l,e[t+2]=d,e[t+3]=h;return}if(o===1){e[t+0]=f,e[t+1]=m,e[t+2]=g,e[t+3]=_;return}if(h!==_||c!==f||l!==m||d!==g){let p=1-o;const u=c*f+l*m+d*g+h*_,w=u>=0?1:-1,b=1-u*u;if(b>Number.EPSILON){const T=Math.sqrt(b),y=Math.atan2(T,u*w);p=Math.sin(p*y)/T,o=Math.sin(o*y)/T}const S=o*w;if(c=c*p+f*S,l=l*p+m*S,d=d*p+g*S,h=h*p+_*S,p===1-o){const T=1/Math.sqrt(c*c+l*l+d*d+h*h);c*=T,l*=T,d*=T,h*=T}}e[t]=c,e[t+1]=l,e[t+2]=d,e[t+3]=h}static multiplyQuaternionsFlat(e,t,i,r,a,s){const o=i[r],c=i[r+1],l=i[r+2],d=i[r+3],h=a[s],f=a[s+1],m=a[s+2],g=a[s+3];return e[t]=o*g+d*h+c*m-l*f,e[t+1]=c*g+d*f+l*h-o*m,e[t+2]=l*g+d*m+o*f-c*h,e[t+3]=d*g-o*h-c*f-l*m,e}get x(){return this._x}set x(e){this._x=e,this._onChangeCallback()}get y(){return this._y}set y(e){this._y=e,this._onChangeCallback()}get z(){return this._z}set z(e){this._z=e,this._onChangeCallback()}get w(){return this._w}set w(e){this._w=e,this._onChangeCallback()}set(e,t,i,r){return this._x=e,this._y=t,this._z=i,this._w=r,this._onChangeCallback(),this}clone(){return new this.constructor(this._x,this._y,this._z,this._w)}copy(e){return this._x=e.x,this._y=e.y,this._z=e.z,this._w=e.w,this._onChangeCallback(),this}setFromEuler(e,t=!0){const i=e._x,r=e._y,a=e._z,s=e._order,o=Math.cos,c=Math.sin,l=o(i/2),d=o(r/2),h=o(a/2),f=c(i/2),m=c(r/2),g=c(a/2);switch(s){case"XYZ":this._x=f*d*h+l*m*g,this._y=l*m*h-f*d*g,this._z=l*d*g+f*m*h,this._w=l*d*h-f*m*g;break;case"YXZ":this._x=f*d*h+l*m*g,this._y=l*m*h-f*d*g,this._z=l*d*g-f*m*h,this._w=l*d*h+f*m*g;break;case"ZXY":this._x=f*d*h-l*m*g,this._y=l*m*h+f*d*g,this._z=l*d*g+f*m*h,this._w=l*d*h-f*m*g;break;case"ZYX":this._x=f*d*h-l*m*g,this._y=l*m*h+f*d*g,this._z=l*d*g-f*m*h,this._w=l*d*h+f*m*g;break;case"YZX":this._x=f*d*h+l*m*g,this._y=l*m*h+f*d*g,this._z=l*d*g-f*m*h,this._w=l*d*h-f*m*g;break;case"XZY":this._x=f*d*h-l*m*g,this._y=l*m*h-f*d*g,this._z=l*d*g+f*m*h,this._w=l*d*h+f*m*g;break;default:console.warn("THREE.Quaternion: .setFromEuler() encountered an unknown order: "+s)}return t===!0&&this._onChangeCallback(),this}setFromAxisAngle(e,t){const i=t/2,r=Math.sin(i);return this._x=e.x*r,this._y=e.y*r,this._z=e.z*r,this._w=Math.cos(i),this._onChangeCallback(),this}setFromRotationMatrix(e){const t=e.elements,i=t[0],r=t[4],a=t[8],s=t[1],o=t[5],c=t[9],l=t[2],d=t[6],h=t[10],f=i+o+h;if(f>0){const m=.5/Math.sqrt(f+1);this._w=.25/m,this._x=(d-c)*m,this._y=(a-l)*m,this._z=(s-r)*m}else if(i>o&&i>h){const m=2*Math.sqrt(1+i-o-h);this._w=(d-c)/m,this._x=.25*m,this._y=(r+s)/m,this._z=(a+l)/m}else if(o>h){const m=2*Math.sqrt(1+o-i-h);this._w=(a-l)/m,this._x=(r+s)/m,this._y=.25*m,this._z=(c+d)/m}else{const m=2*Math.sqrt(1+h-i-o);this._w=(s-r)/m,this._x=(a+l)/m,this._y=(c+d)/m,this._z=.25*m}return this._onChangeCallback(),this}setFromUnitVectors(e,t){let i=e.dot(t)+1;return i<Number.EPSILON?(i=0,Math.abs(e.x)>Math.abs(e.z)?(this._x=-e.y,this._y=e.x,this._z=0,this._w=i):(this._x=0,this._y=-e.z,this._z=e.y,this._w=i)):(this._x=e.y*t.z-e.z*t.y,this._y=e.z*t.x-e.x*t.z,this._z=e.x*t.y-e.y*t.x,this._w=i),this.normalize()}angleTo(e){return 2*Math.acos(Math.abs(je(this.dot(e),-1,1)))}rotateTowards(e,t){const i=this.angleTo(e);if(i===0)return this;const r=Math.min(1,t/i);return this.slerp(e,r),this}identity(){return this.set(0,0,0,1)}invert(){return this.conjugate()}conjugate(){return this._x*=-1,this._y*=-1,this._z*=-1,this._onChangeCallback(),this}dot(e){return this._x*e._x+this._y*e._y+this._z*e._z+this._w*e._w}lengthSq(){return this._x*this._x+this._y*this._y+this._z*this._z+this._w*this._w}length(){return Math.sqrt(this._x*this._x+this._y*this._y+this._z*this._z+this._w*this._w)}normalize(){let e=this.length();return e===0?(this._x=0,this._y=0,this._z=0,this._w=1):(e=1/e,this._x=this._x*e,this._y=this._y*e,this._z=this._z*e,this._w=this._w*e),this._onChangeCallback(),this}multiply(e){return this.multiplyQuaternions(this,e)}premultiply(e){return this.multiplyQuaternions(e,this)}multiplyQuaternions(e,t){const i=e._x,r=e._y,a=e._z,s=e._w,o=t._x,c=t._y,l=t._z,d=t._w;return this._x=i*d+s*o+r*l-a*c,this._y=r*d+s*c+a*o-i*l,this._z=a*d+s*l+i*c-r*o,this._w=s*d-i*o-r*c-a*l,this._onChangeCallback(),this}slerp(e,t){if(t===0)return this;if(t===1)return this.copy(e);const i=this._x,r=this._y,a=this._z,s=this._w;let o=s*e._w+i*e._x+r*e._y+a*e._z;if(o<0?(this._w=-e._w,this._x=-e._x,this._y=-e._y,this._z=-e._z,o=-o):this.copy(e),o>=1)return this._w=s,this._x=i,this._y=r,this._z=a,this;const c=1-o*o;if(c<=Number.EPSILON){const m=1-t;return this._w=m*s+t*this._w,this._x=m*i+t*this._x,this._y=m*r+t*this._y,this._z=m*a+t*this._z,this.normalize(),this}const l=Math.sqrt(c),d=Math.atan2(l,o),h=Math.sin((1-t)*d)/l,f=Math.sin(t*d)/l;return this._w=s*h+this._w*f,this._x=i*h+this._x*f,this._y=r*h+this._y*f,this._z=a*h+this._z*f,this._onChangeCallback(),this}slerpQuaternions(e,t,i){return this.copy(e).slerp(t,i)}random(){const e=2*Math.PI*Math.random(),t=2*Math.PI*Math.random(),i=Math.random(),r=Math.sqrt(1-i),a=Math.sqrt(i);return this.set(r*Math.sin(e),r*Math.cos(e),a*Math.sin(t),a*Math.cos(t))}equals(e){return e._x===this._x&&e._y===this._y&&e._z===this._z&&e._w===this._w}fromArray(e,t=0){return this._x=e[t],this._y=e[t+1],this._z=e[t+2],this._w=e[t+3],this._onChangeCallback(),this}toArray(e=[],t=0){return e[t]=this._x,e[t+1]=this._y,e[t+2]=this._z,e[t+3]=this._w,e}fromBufferAttribute(e,t){return this._x=e.getX(t),this._y=e.getY(t),this._z=e.getZ(t),this._w=e.getW(t),this._onChangeCallback(),this}toJSON(){return this.toArray()}_onChange(e){return this._onChangeCallback=e,this}_onChangeCallback(){}*[Symbol.iterator](){yield this._x,yield this._y,yield this._z,yield this._w}}class k{constructor(e=0,t=0,i=0){k.prototype.isVector3=!0,this.x=e,this.y=t,this.z=i}set(e,t,i){return i===void 0&&(i=this.z),this.x=e,this.y=t,this.z=i,this}setScalar(e){return this.x=e,this.y=e,this.z=e,this}setX(e){return this.x=e,this}setY(e){return this.y=e,this}setZ(e){return this.z=e,this}setComponent(e,t){switch(e){case 0:this.x=t;break;case 1:this.y=t;break;case 2:this.z=t;break;default:throw new Error("index is out of range: "+e)}return this}getComponent(e){switch(e){case 0:return this.x;case 1:return this.y;case 2:return this.z;default:throw new Error("index is out of range: "+e)}}clone(){return new this.constructor(this.x,this.y,this.z)}copy(e){return this.x=e.x,this.y=e.y,this.z=e.z,this}add(e){return this.x+=e.x,this.y+=e.y,this.z+=e.z,this}addScalar(e){return this.x+=e,this.y+=e,this.z+=e,this}addVectors(e,t){return this.x=e.x+t.x,this.y=e.y+t.y,this.z=e.z+t.z,this}addScaledVector(e,t){return this.x+=e.x*t,this.y+=e.y*t,this.z+=e.z*t,this}sub(e){return this.x-=e.x,this.y-=e.y,this.z-=e.z,this}subScalar(e){return this.x-=e,this.y-=e,this.z-=e,this}subVectors(e,t){return this.x=e.x-t.x,this.y=e.y-t.y,this.z=e.z-t.z,this}multiply(e){return this.x*=e.x,this.y*=e.y,this.z*=e.z,this}multiplyScalar(e){return this.x*=e,this.y*=e,this.z*=e,this}multiplyVectors(e,t){return this.x=e.x*t.x,this.y=e.y*t.y,this.z=e.z*t.z,this}applyEuler(e){return this.applyQuaternion(ro.setFromEuler(e))}applyAxisAngle(e,t){return this.applyQuaternion(ro.setFromAxisAngle(e,t))}applyMatrix3(e){const t=this.x,i=this.y,r=this.z,a=e.elements;return this.x=a[0]*t+a[3]*i+a[6]*r,this.y=a[1]*t+a[4]*i+a[7]*r,this.z=a[2]*t+a[5]*i+a[8]*r,this}applyNormalMatrix(e){return this.applyMatrix3(e).normalize()}applyMatrix4(e){const t=this.x,i=this.y,r=this.z,a=e.elements,s=1/(a[3]*t+a[7]*i+a[11]*r+a[15]);return this.x=(a[0]*t+a[4]*i+a[8]*r+a[12])*s,this.y=(a[1]*t+a[5]*i+a[9]*r+a[13])*s,this.z=(a[2]*t+a[6]*i+a[10]*r+a[14])*s,this}applyQuaternion(e){const t=this.x,i=this.y,r=this.z,a=e.x,s=e.y,o=e.z,c=e.w,l=2*(s*r-o*i),d=2*(o*t-a*r),h=2*(a*i-s*t);return this.x=t+c*l+s*h-o*d,this.y=i+c*d+o*l-a*h,this.z=r+c*h+a*d-s*l,this}project(e){return this.applyMatrix4(e.matrixWorldInverse).applyMatrix4(e.projectionMatrix)}unproject(e){return this.applyMatrix4(e.projectionMatrixInverse).applyMatrix4(e.matrixWorld)}transformDirection(e){const t=this.x,i=this.y,r=this.z,a=e.elements;return this.x=a[0]*t+a[4]*i+a[8]*r,this.y=a[1]*t+a[5]*i+a[9]*r,this.z=a[2]*t+a[6]*i+a[10]*r,this.normalize()}divide(e){return this.x/=e.x,this.y/=e.y,this.z/=e.z,this}divideScalar(e){return this.multiplyScalar(1/e)}min(e){return this.x=Math.min(this.x,e.x),this.y=Math.min(this.y,e.y),this.z=Math.min(this.z,e.z),this}max(e){return this.x=Math.max(this.x,e.x),this.y=Math.max(this.y,e.y),this.z=Math.max(this.z,e.z),this}clamp(e,t){return this.x=je(this.x,e.x,t.x),this.y=je(this.y,e.y,t.y),this.z=je(this.z,e.z,t.z),this}clampScalar(e,t){return this.x=je(this.x,e,t),this.y=je(this.y,e,t),this.z=je(this.z,e,t),this}clampLength(e,t){const i=this.length();return this.divideScalar(i||1).multiplyScalar(je(i,e,t))}floor(){return this.x=Math.floor(this.x),this.y=Math.floor(this.y),this.z=Math.floor(this.z),this}ceil(){return this.x=Math.ceil(this.x),this.y=Math.ceil(this.y),this.z=Math.ceil(this.z),this}round(){return this.x=Math.round(this.x),this.y=Math.round(this.y),this.z=Math.round(this.z),this}roundToZero(){return this.x=Math.trunc(this.x),this.y=Math.trunc(this.y),this.z=Math.trunc(this.z),this}negate(){return this.x=-this.x,this.y=-this.y,this.z=-this.z,this}dot(e){return this.x*e.x+this.y*e.y+this.z*e.z}lengthSq(){return this.x*this.x+this.y*this.y+this.z*this.z}length(){return Math.sqrt(this.x*this.x+this.y*this.y+this.z*this.z)}manhattanLength(){return Math.abs(this.x)+Math.abs(this.y)+Math.abs(this.z)}normalize(){return this.divideScalar(this.length()||1)}setLength(e){return this.normalize().multiplyScalar(e)}lerp(e,t){return this.x+=(e.x-this.x)*t,this.y+=(e.y-this.y)*t,this.z+=(e.z-this.z)*t,this}lerpVectors(e,t,i){return this.x=e.x+(t.x-e.x)*i,this.y=e.y+(t.y-e.y)*i,this.z=e.z+(t.z-e.z)*i,this}cross(e){return this.crossVectors(this,e)}crossVectors(e,t){const i=e.x,r=e.y,a=e.z,s=t.x,o=t.y,c=t.z;return this.x=r*c-a*o,this.y=a*s-i*c,this.z=i*o-r*s,this}projectOnVector(e){const t=e.lengthSq();if(t===0)return this.set(0,0,0);const i=e.dot(this)/t;return this.copy(e).multiplyScalar(i)}projectOnPlane(e){return Zr.copy(this).projectOnVector(e),this.sub(Zr)}reflect(e){return this.sub(Zr.copy(e).multiplyScalar(2*this.dot(e)))}angleTo(e){const t=Math.sqrt(this.lengthSq()*e.lengthSq());if(t===0)return Math.PI/2;const i=this.dot(e)/t;return Math.acos(je(i,-1,1))}distanceTo(e){return Math.sqrt(this.distanceToSquared(e))}distanceToSquared(e){const t=this.x-e.x,i=this.y-e.y,r=this.z-e.z;return t*t+i*i+r*r}manhattanDistanceTo(e){return Math.abs(this.x-e.x)+Math.abs(this.y-e.y)+Math.abs(this.z-e.z)}setFromSpherical(e){return this.setFromSphericalCoords(e.radius,e.phi,e.theta)}setFromSphericalCoords(e,t,i){const r=Math.sin(t)*e;return this.x=r*Math.sin(i),this.y=Math.cos(t)*e,this.z=r*Math.cos(i),this}setFromCylindrical(e){return this.setFromCylindricalCoords(e.radius,e.theta,e.y)}setFromCylindricalCoords(e,t,i){return this.x=e*Math.sin(t),this.y=i,this.z=e*Math.cos(t),this}setFromMatrixPosition(e){const t=e.elements;return this.x=t[12],this.y=t[13],this.z=t[14],this}setFromMatrixScale(e){const t=this.setFromMatrixColumn(e,0).length(),i=this.setFromMatrixColumn(e,1).length(),r=this.setFromMatrixColumn(e,2).length();return this.x=t,this.y=i,this.z=r,this}setFromMatrixColumn(e,t){return this.fromArray(e.elements,t*4)}setFromMatrix3Column(e,t){return this.fromArray(e.elements,t*3)}setFromEuler(e){return this.x=e._x,this.y=e._y,this.z=e._z,this}setFromColor(e){return this.x=e.r,this.y=e.g,this.z=e.b,this}equals(e){return e.x===this.x&&e.y===this.y&&e.z===this.z}fromArray(e,t=0){return this.x=e[t],this.y=e[t+1],this.z=e[t+2],this}toArray(e=[],t=0){return e[t]=this.x,e[t+1]=this.y,e[t+2]=this.z,e}fromBufferAttribute(e,t){return this.x=e.getX(t),this.y=e.getY(t),this.z=e.getZ(t),this}random(){return this.x=Math.random(),this.y=Math.random(),this.z=Math.random(),this}randomDirection(){const e=Math.random()*Math.PI*2,t=Math.random()*2-1,i=Math.sqrt(1-t*t);return this.x=i*Math.cos(e),this.y=t,this.z=i*Math.sin(e),this}*[Symbol.iterator](){yield this.x,yield this.y,yield this.z}}const Zr=new k,ro=new Vi;class Gi{constructor(e=new k(1/0,1/0,1/0),t=new k(-1/0,-1/0,-1/0)){this.isBox3=!0,this.min=e,this.max=t}set(e,t){return this.min.copy(e),this.max.copy(t),this}setFromArray(e){this.makeEmpty();for(let t=0,i=e.length;t<i;t+=3)this.expandByPoint(Gt.fromArray(e,t));return this}setFromBufferAttribute(e){this.makeEmpty();for(let t=0,i=e.count;t<i;t++)this.expandByPoint(Gt.fromBufferAttribute(e,t));return this}setFromPoints(e){this.makeEmpty();for(let t=0,i=e.length;t<i;t++)this.expandByPoint(e[t]);return this}setFromCenterAndSize(e,t){const i=Gt.copy(t).multiplyScalar(.5);return this.min.copy(e).sub(i),this.max.copy(e).add(i),this}setFromObject(e,t=!1){return this.makeEmpty(),this.expandByObject(e,t)}clone(){return new this.constructor().copy(this)}copy(e){return this.min.copy(e.min),this.max.copy(e.max),this}makeEmpty(){return this.min.x=this.min.y=this.min.z=1/0,this.max.x=this.max.y=this.max.z=-1/0,this}isEmpty(){return this.max.x<this.min.x||this.max.y<this.min.y||this.max.z<this.min.z}getCenter(e){return this.isEmpty()?e.set(0,0,0):e.addVectors(this.min,this.max).multiplyScalar(.5)}getSize(e){return this.isEmpty()?e.set(0,0,0):e.subVectors(this.max,this.min)}expandByPoint(e){return this.min.min(e),this.max.max(e),this}expandByVector(e){return this.min.sub(e),this.max.add(e),this}expandByScalar(e){return this.min.addScalar(-e),this.max.addScalar(e),this}expandByObject(e,t=!1){e.updateWorldMatrix(!1,!1);const i=e.geometry;if(i!==void 0){const a=i.getAttribute("position");if(t===!0&&a!==void 0&&e.isInstancedMesh!==!0)for(let s=0,o=a.count;s<o;s++)e.isMesh===!0?e.getVertexPosition(s,Gt):Gt.fromBufferAttribute(a,s),Gt.applyMatrix4(e.matrixWorld),this.expandByPoint(Gt);else e.boundingBox!==void 0?(e.boundingBox===null&&e.computeBoundingBox(),$i.copy(e.boundingBox)):(i.boundingBox===null&&i.computeBoundingBox(),$i.copy(i.boundingBox)),$i.applyMatrix4(e.matrixWorld),this.union($i)}const r=e.children;for(let a=0,s=r.length;a<s;a++)this.expandByObject(r[a],t);return this}containsPoint(e){return e.x>=this.min.x&&e.x<=this.max.x&&e.y>=this.min.y&&e.y<=this.max.y&&e.z>=this.min.z&&e.z<=this.max.z}containsBox(e){return this.min.x<=e.min.x&&e.max.x<=this.max.x&&this.min.y<=e.min.y&&e.max.y<=this.max.y&&this.min.z<=e.min.z&&e.max.z<=this.max.z}getParameter(e,t){return t.set((e.x-this.min.x)/(this.max.x-this.min.x),(e.y-this.min.y)/(this.max.y-this.min.y),(e.z-this.min.z)/(this.max.z-this.min.z))}intersectsBox(e){return e.max.x>=this.min.x&&e.min.x<=this.max.x&&e.max.y>=this.min.y&&e.min.y<=this.max.y&&e.max.z>=this.min.z&&e.min.z<=this.max.z}intersectsSphere(e){return this.clampPoint(e.center,Gt),Gt.distanceToSquared(e.center)<=e.radius*e.radius}intersectsPlane(e){let t,i;return e.normal.x>0?(t=e.normal.x*this.min.x,i=e.normal.x*this.max.x):(t=e.normal.x*this.max.x,i=e.normal.x*this.min.x),e.normal.y>0?(t+=e.normal.y*this.min.y,i+=e.normal.y*this.max.y):(t+=e.normal.y*this.max.y,i+=e.normal.y*this.min.y),e.normal.z>0?(t+=e.normal.z*this.min.z,i+=e.normal.z*this.max.z):(t+=e.normal.z*this.max.z,i+=e.normal.z*this.min.z),t<=-e.constant&&i>=-e.constant}intersectsTriangle(e){if(this.isEmpty())return!1;this.getCenter(Li),Ki.subVectors(this.max,Li),Qn.subVectors(e.a,Li),ei.subVectors(e.b,Li),ti.subVectors(e.c,Li),mn.subVectors(ei,Qn),gn.subVectors(ti,ei),Pn.subVectors(Qn,ti);let t=[0,-mn.z,mn.y,0,-gn.z,gn.y,0,-Pn.z,Pn.y,mn.z,0,-mn.x,gn.z,0,-gn.x,Pn.z,0,-Pn.x,-mn.y,mn.x,0,-gn.y,gn.x,0,-Pn.y,Pn.x,0];return!Jr(t,Qn,ei,ti,Ki)||(t=[1,0,0,0,1,0,0,0,1],!Jr(t,Qn,ei,ti,Ki))?!1:(Zi.crossVectors(mn,gn),t=[Zi.x,Zi.y,Zi.z],Jr(t,Qn,ei,ti,Ki))}clampPoint(e,t){return t.copy(e).clamp(this.min,this.max)}distanceToPoint(e){return this.clampPoint(e,Gt).distanceTo(e)}getBoundingSphere(e){return this.isEmpty()?e.makeEmpty():(this.getCenter(e.center),e.radius=this.getSize(Gt).length()*.5),e}intersect(e){return this.min.max(e.min),this.max.min(e.max),this.isEmpty()&&this.makeEmpty(),this}union(e){return this.min.min(e.min),this.max.max(e.max),this}applyMatrix4(e){return this.isEmpty()?this:(en[0].set(this.min.x,this.min.y,this.min.z).applyMatrix4(e),en[1].set(this.min.x,this.min.y,this.max.z).applyMatrix4(e),en[2].set(this.min.x,this.max.y,this.min.z).applyMatrix4(e),en[3].set(this.min.x,this.max.y,this.max.z).applyMatrix4(e),en[4].set(this.max.x,this.min.y,this.min.z).applyMatrix4(e),en[5].set(this.max.x,this.min.y,this.max.z).applyMatrix4(e),en[6].set(this.max.x,this.max.y,this.min.z).applyMatrix4(e),en[7].set(this.max.x,this.max.y,this.max.z).applyMatrix4(e),this.setFromPoints(en),this)}translate(e){return this.min.add(e),this.max.add(e),this}equals(e){return e.min.equals(this.min)&&e.max.equals(this.max)}}const en=[new k,new k,new k,new k,new k,new k,new k,new k],Gt=new k,$i=new Gi,Qn=new k,ei=new k,ti=new k,mn=new k,gn=new k,Pn=new k,Li=new k,Ki=new k,Zi=new k,Dn=new k;function Jr(n,e,t,i,r){for(let a=0,s=n.length-3;a<=s;a+=3){Dn.fromArray(n,a);const o=r.x*Math.abs(Dn.x)+r.y*Math.abs(Dn.y)+r.z*Math.abs(Dn.z),c=e.dot(Dn),l=t.dot(Dn),d=i.dot(Dn);if(Math.max(-Math.max(c,l,d),Math.min(c,l,d))>o)return!1}return!0}const Kl=new Gi,Ii=new k,Qr=new k;class Br{constructor(e=new k,t=-1){this.isSphere=!0,this.center=e,this.radius=t}set(e,t){return this.center.copy(e),this.radius=t,this}setFromPoints(e,t){const i=this.center;t!==void 0?i.copy(t):Kl.setFromPoints(e).getCenter(i);let r=0;for(let a=0,s=e.length;a<s;a++)r=Math.max(r,i.distanceToSquared(e[a]));return this.radius=Math.sqrt(r),this}copy(e){return this.center.copy(e.center),this.radius=e.radius,this}isEmpty(){return this.radius<0}makeEmpty(){return this.center.set(0,0,0),this.radius=-1,this}containsPoint(e){return e.distanceToSquared(this.center)<=this.radius*this.radius}distanceToPoint(e){return e.distanceTo(this.center)-this.radius}intersectsSphere(e){const t=this.radius+e.radius;return e.center.distanceToSquared(this.center)<=t*t}intersectsBox(e){return e.intersectsSphere(this)}intersectsPlane(e){return Math.abs(e.distanceToPoint(this.center))<=this.radius}clampPoint(e,t){const i=this.center.distanceToSquared(e);return t.copy(e),i>this.radius*this.radius&&(t.sub(this.center).normalize(),t.multiplyScalar(this.radius).add(this.center)),t}getBoundingBox(e){return this.isEmpty()?(e.makeEmpty(),e):(e.set(this.center,this.center),e.expandByScalar(this.radius),e)}applyMatrix4(e){return this.center.applyMatrix4(e),this.radius=this.radius*e.getMaxScaleOnAxis(),this}translate(e){return this.center.add(e),this}expandByPoint(e){if(this.isEmpty())return this.center.copy(e),this.radius=0,this;Ii.subVectors(e,this.center);const t=Ii.lengthSq();if(t>this.radius*this.radius){const i=Math.sqrt(t),r=(i-this.radius)*.5;this.center.addScaledVector(Ii,r/i),this.radius+=r}return this}union(e){return e.isEmpty()?this:this.isEmpty()?(this.copy(e),this):(this.center.equals(e.center)===!0?this.radius=Math.max(this.radius,e.radius):(Qr.subVectors(e.center,this.center).setLength(e.radius),this.expandByPoint(Ii.copy(e.center).add(Qr)),this.expandByPoint(Ii.copy(e.center).sub(Qr))),this)}equals(e){return e.center.equals(this.center)&&e.radius===this.radius}clone(){return new this.constructor().copy(this)}}const tn=new k,ea=new k,Ji=new k,_n=new k,ta=new k,Qi=new k,na=new k;class Ls{constructor(e=new k,t=new k(0,0,-1)){this.origin=e,this.direction=t}set(e,t){return this.origin.copy(e),this.direction.copy(t),this}copy(e){return this.origin.copy(e.origin),this.direction.copy(e.direction),this}at(e,t){return t.copy(this.origin).addScaledVector(this.direction,e)}lookAt(e){return this.direction.copy(e).sub(this.origin).normalize(),this}recast(e){return this.origin.copy(this.at(e,tn)),this}closestPointToPoint(e,t){t.subVectors(e,this.origin);const i=t.dot(this.direction);return i<0?t.copy(this.origin):t.copy(this.origin).addScaledVector(this.direction,i)}distanceToPoint(e){return Math.sqrt(this.distanceSqToPoint(e))}distanceSqToPoint(e){const t=tn.subVectors(e,this.origin).dot(this.direction);return t<0?this.origin.distanceToSquared(e):(tn.copy(this.origin).addScaledVector(this.direction,t),tn.distanceToSquared(e))}distanceSqToSegment(e,t,i,r){ea.copy(e).add(t).multiplyScalar(.5),Ji.copy(t).sub(e).normalize(),_n.copy(this.origin).sub(ea);const a=e.distanceTo(t)*.5,s=-this.direction.dot(Ji),o=_n.dot(this.direction),c=-_n.dot(Ji),l=_n.lengthSq(),d=Math.abs(1-s*s);let h,f,m,g;if(d>0)if(h=s*c-o,f=s*o-c,g=a*d,h>=0)if(f>=-g)if(f<=g){const _=1/d;h*=_,f*=_,m=h*(h+s*f+2*o)+f*(s*h+f+2*c)+l}else f=a,h=Math.max(0,-(s*f+o)),m=-h*h+f*(f+2*c)+l;else f=-a,h=Math.max(0,-(s*f+o)),m=-h*h+f*(f+2*c)+l;else f<=-g?(h=Math.max(0,-(-s*a+o)),f=h>0?-a:Math.min(Math.max(-a,-c),a),m=-h*h+f*(f+2*c)+l):f<=g?(h=0,f=Math.min(Math.max(-a,-c),a),m=f*(f+2*c)+l):(h=Math.max(0,-(s*a+o)),f=h>0?a:Math.min(Math.max(-a,-c),a),m=-h*h+f*(f+2*c)+l);else f=s>0?-a:a,h=Math.max(0,-(s*f+o)),m=-h*h+f*(f+2*c)+l;return i&&i.copy(this.origin).addScaledVector(this.direction,h),r&&r.copy(ea).addScaledVector(Ji,f),m}intersectSphere(e,t){tn.subVectors(e.center,this.origin);const i=tn.dot(this.direction),r=tn.dot(tn)-i*i,a=e.radius*e.radius;if(r>a)return null;const s=Math.sqrt(a-r),o=i-s,c=i+s;return c<0?null:o<0?this.at(c,t):this.at(o,t)}intersectsSphere(e){return this.distanceSqToPoint(e.center)<=e.radius*e.radius}distanceToPlane(e){const t=e.normal.dot(this.direction);if(t===0)return e.distanceToPoint(this.origin)===0?0:null;const i=-(this.origin.dot(e.normal)+e.constant)/t;return i>=0?i:null}intersectPlane(e,t){const i=this.distanceToPlane(e);return i===null?null:this.at(i,t)}intersectsPlane(e){const t=e.distanceToPoint(this.origin);return t===0||e.normal.dot(this.direction)*t<0}intersectBox(e,t){let i,r,a,s,o,c;const l=1/this.direction.x,d=1/this.direction.y,h=1/this.direction.z,f=this.origin;return l>=0?(i=(e.min.x-f.x)*l,r=(e.max.x-f.x)*l):(i=(e.max.x-f.x)*l,r=(e.min.x-f.x)*l),d>=0?(a=(e.min.y-f.y)*d,s=(e.max.y-f.y)*d):(a=(e.max.y-f.y)*d,s=(e.min.y-f.y)*d),i>s||a>r||((a>i||isNaN(i))&&(i=a),(s<r||isNaN(r))&&(r=s),h>=0?(o=(e.min.z-f.z)*h,c=(e.max.z-f.z)*h):(o=(e.max.z-f.z)*h,c=(e.min.z-f.z)*h),i>c||o>r)||((o>i||i!==i)&&(i=o),(c<r||r!==r)&&(r=c),r<0)?null:this.at(i>=0?i:r,t)}intersectsBox(e){return this.intersectBox(e,tn)!==null}intersectTriangle(e,t,i,r,a){ta.subVectors(t,e),Qi.subVectors(i,e),na.crossVectors(ta,Qi);let s=this.direction.dot(na),o;if(s>0){if(r)return null;o=1}else if(s<0)o=-1,s=-s;else return null;_n.subVectors(this.origin,e);const c=o*this.direction.dot(Qi.crossVectors(_n,Qi));if(c<0)return null;const l=o*this.direction.dot(ta.cross(_n));if(l<0||c+l>s)return null;const d=-o*_n.dot(na);return d<0?null:this.at(d/s,a)}applyMatrix4(e){return this.origin.applyMatrix4(e),this.direction.transformDirection(e),this}equals(e){return e.origin.equals(this.origin)&&e.direction.equals(this.direction)}clone(){return new this.constructor().copy(this)}}class at{constructor(e,t,i,r,a,s,o,c,l,d,h,f,m,g,_,p){at.prototype.isMatrix4=!0,this.elements=[1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1],e!==void 0&&this.set(e,t,i,r,a,s,o,c,l,d,h,f,m,g,_,p)}set(e,t,i,r,a,s,o,c,l,d,h,f,m,g,_,p){const u=this.elements;return u[0]=e,u[4]=t,u[8]=i,u[12]=r,u[1]=a,u[5]=s,u[9]=o,u[13]=c,u[2]=l,u[6]=d,u[10]=h,u[14]=f,u[3]=m,u[7]=g,u[11]=_,u[15]=p,this}identity(){return this.set(1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1),this}clone(){return new at().fromArray(this.elements)}copy(e){const t=this.elements,i=e.elements;return t[0]=i[0],t[1]=i[1],t[2]=i[2],t[3]=i[3],t[4]=i[4],t[5]=i[5],t[6]=i[6],t[7]=i[7],t[8]=i[8],t[9]=i[9],t[10]=i[10],t[11]=i[11],t[12]=i[12],t[13]=i[13],t[14]=i[14],t[15]=i[15],this}copyPosition(e){const t=this.elements,i=e.elements;return t[12]=i[12],t[13]=i[13],t[14]=i[14],this}setFromMatrix3(e){const t=e.elements;return this.set(t[0],t[3],t[6],0,t[1],t[4],t[7],0,t[2],t[5],t[8],0,0,0,0,1),this}extractBasis(e,t,i){return e.setFromMatrixColumn(this,0),t.setFromMatrixColumn(this,1),i.setFromMatrixColumn(this,2),this}makeBasis(e,t,i){return this.set(e.x,t.x,i.x,0,e.y,t.y,i.y,0,e.z,t.z,i.z,0,0,0,0,1),this}extractRotation(e){const t=this.elements,i=e.elements,r=1/ni.setFromMatrixColumn(e,0).length(),a=1/ni.setFromMatrixColumn(e,1).length(),s=1/ni.setFromMatrixColumn(e,2).length();return t[0]=i[0]*r,t[1]=i[1]*r,t[2]=i[2]*r,t[3]=0,t[4]=i[4]*a,t[5]=i[5]*a,t[6]=i[6]*a,t[7]=0,t[8]=i[8]*s,t[9]=i[9]*s,t[10]=i[10]*s,t[11]=0,t[12]=0,t[13]=0,t[14]=0,t[15]=1,this}makeRotationFromEuler(e){const t=this.elements,i=e.x,r=e.y,a=e.z,s=Math.cos(i),o=Math.sin(i),c=Math.cos(r),l=Math.sin(r),d=Math.cos(a),h=Math.sin(a);if(e.order==="XYZ"){const f=s*d,m=s*h,g=o*d,_=o*h;t[0]=c*d,t[4]=-c*h,t[8]=l,t[1]=m+g*l,t[5]=f-_*l,t[9]=-o*c,t[2]=_-f*l,t[6]=g+m*l,t[10]=s*c}else if(e.order==="YXZ"){const f=c*d,m=c*h,g=l*d,_=l*h;t[0]=f+_*o,t[4]=g*o-m,t[8]=s*l,t[1]=s*h,t[5]=s*d,t[9]=-o,t[2]=m*o-g,t[6]=_+f*o,t[10]=s*c}else if(e.order==="ZXY"){const f=c*d,m=c*h,g=l*d,_=l*h;t[0]=f-_*o,t[4]=-s*h,t[8]=g+m*o,t[1]=m+g*o,t[5]=s*d,t[9]=_-f*o,t[2]=-s*l,t[6]=o,t[10]=s*c}else if(e.order==="ZYX"){const f=s*d,m=s*h,g=o*d,_=o*h;t[0]=c*d,t[4]=g*l-m,t[8]=f*l+_,t[1]=c*h,t[5]=_*l+f,t[9]=m*l-g,t[2]=-l,t[6]=o*c,t[10]=s*c}else if(e.order==="YZX"){const f=s*c,m=s*l,g=o*c,_=o*l;t[0]=c*d,t[4]=_-f*h,t[8]=g*h+m,t[1]=h,t[5]=s*d,t[9]=-o*d,t[2]=-l*d,t[6]=m*h+g,t[10]=f-_*h}else if(e.order==="XZY"){const f=s*c,m=s*l,g=o*c,_=o*l;t[0]=c*d,t[4]=-h,t[8]=l*d,t[1]=f*h+_,t[5]=s*d,t[9]=m*h-g,t[2]=g*h-m,t[6]=o*d,t[10]=_*h+f}return t[3]=0,t[7]=0,t[11]=0,t[12]=0,t[13]=0,t[14]=0,t[15]=1,this}makeRotationFromQuaternion(e){return this.compose(Zl,e,Jl)}lookAt(e,t,i){const r=this.elements;return Pt.subVectors(e,t),Pt.lengthSq()===0&&(Pt.z=1),Pt.normalize(),vn.crossVectors(i,Pt),vn.lengthSq()===0&&(Math.abs(i.z)===1?Pt.x+=1e-4:Pt.z+=1e-4,Pt.normalize(),vn.crossVectors(i,Pt)),vn.normalize(),er.crossVectors(Pt,vn),r[0]=vn.x,r[4]=er.x,r[8]=Pt.x,r[1]=vn.y,r[5]=er.y,r[9]=Pt.y,r[2]=vn.z,r[6]=er.z,r[10]=Pt.z,this}multiply(e){return this.multiplyMatrices(this,e)}premultiply(e){return this.multiplyMatrices(e,this)}multiplyMatrices(e,t){const i=e.elements,r=t.elements,a=this.elements,s=i[0],o=i[4],c=i[8],l=i[12],d=i[1],h=i[5],f=i[9],m=i[13],g=i[2],_=i[6],p=i[10],u=i[14],w=i[3],b=i[7],S=i[11],T=i[15],y=r[0],A=r[4],D=r[8],x=r[12],v=r[1],C=r[5],F=r[9],N=r[13],P=r[2],U=r[6],z=r[10],H=r[14],I=r[3],G=r[7],q=r[11],oe=r[15];return a[0]=s*y+o*v+c*P+l*I,a[4]=s*A+o*C+c*U+l*G,a[8]=s*D+o*F+c*z+l*q,a[12]=s*x+o*N+c*H+l*oe,a[1]=d*y+h*v+f*P+m*I,a[5]=d*A+h*C+f*U+m*G,a[9]=d*D+h*F+f*z+m*q,a[13]=d*x+h*N+f*H+m*oe,a[2]=g*y+_*v+p*P+u*I,a[6]=g*A+_*C+p*U+u*G,a[10]=g*D+_*F+p*z+u*q,a[14]=g*x+_*N+p*H+u*oe,a[3]=w*y+b*v+S*P+T*I,a[7]=w*A+b*C+S*U+T*G,a[11]=w*D+b*F+S*z+T*q,a[15]=w*x+b*N+S*H+T*oe,this}multiplyScalar(e){const t=this.elements;return t[0]*=e,t[4]*=e,t[8]*=e,t[12]*=e,t[1]*=e,t[5]*=e,t[9]*=e,t[13]*=e,t[2]*=e,t[6]*=e,t[10]*=e,t[14]*=e,t[3]*=e,t[7]*=e,t[11]*=e,t[15]*=e,this}determinant(){const e=this.elements,t=e[0],i=e[4],r=e[8],a=e[12],s=e[1],o=e[5],c=e[9],l=e[13],d=e[2],h=e[6],f=e[10],m=e[14],g=e[3],_=e[7],p=e[11],u=e[15];return g*(+a*c*h-r*l*h-a*o*f+i*l*f+r*o*m-i*c*m)+_*(+t*c*m-t*l*f+a*s*f-r*s*m+r*l*d-a*c*d)+p*(+t*l*h-t*o*m-a*s*h+i*s*m+a*o*d-i*l*d)+u*(-r*o*d-t*c*h+t*o*f+r*s*h-i*s*f+i*c*d)}transpose(){const e=this.elements;let t;return t=e[1],e[1]=e[4],e[4]=t,t=e[2],e[2]=e[8],e[8]=t,t=e[6],e[6]=e[9],e[9]=t,t=e[3],e[3]=e[12],e[12]=t,t=e[7],e[7]=e[13],e[13]=t,t=e[11],e[11]=e[14],e[14]=t,this}setPosition(e,t,i){const r=this.elements;return e.isVector3?(r[12]=e.x,r[13]=e.y,r[14]=e.z):(r[12]=e,r[13]=t,r[14]=i),this}invert(){const e=this.elements,t=e[0],i=e[1],r=e[2],a=e[3],s=e[4],o=e[5],c=e[6],l=e[7],d=e[8],h=e[9],f=e[10],m=e[11],g=e[12],_=e[13],p=e[14],u=e[15],w=h*p*l-_*f*l+_*c*m-o*p*m-h*c*u+o*f*u,b=g*f*l-d*p*l-g*c*m+s*p*m+d*c*u-s*f*u,S=d*_*l-g*h*l+g*o*m-s*_*m-d*o*u+s*h*u,T=g*h*c-d*_*c-g*o*f+s*_*f+d*o*p-s*h*p,y=t*w+i*b+r*S+a*T;if(y===0)return this.set(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);const A=1/y;return e[0]=w*A,e[1]=(_*f*a-h*p*a-_*r*m+i*p*m+h*r*u-i*f*u)*A,e[2]=(o*p*a-_*c*a+_*r*l-i*p*l-o*r*u+i*c*u)*A,e[3]=(h*c*a-o*f*a-h*r*l+i*f*l+o*r*m-i*c*m)*A,e[4]=b*A,e[5]=(d*p*a-g*f*a+g*r*m-t*p*m-d*r*u+t*f*u)*A,e[6]=(g*c*a-s*p*a-g*r*l+t*p*l+s*r*u-t*c*u)*A,e[7]=(s*f*a-d*c*a+d*r*l-t*f*l-s*r*m+t*c*m)*A,e[8]=S*A,e[9]=(g*h*a-d*_*a-g*i*m+t*_*m+d*i*u-t*h*u)*A,e[10]=(s*_*a-g*o*a+g*i*l-t*_*l-s*i*u+t*o*u)*A,e[11]=(d*o*a-s*h*a-d*i*l+t*h*l+s*i*m-t*o*m)*A,e[12]=T*A,e[13]=(d*_*r-g*h*r+g*i*f-t*_*f-d*i*p+t*h*p)*A,e[14]=(g*o*r-s*_*r-g*i*c+t*_*c+s*i*p-t*o*p)*A,e[15]=(s*h*r-d*o*r+d*i*c-t*h*c-s*i*f+t*o*f)*A,this}scale(e){const t=this.elements,i=e.x,r=e.y,a=e.z;return t[0]*=i,t[4]*=r,t[8]*=a,t[1]*=i,t[5]*=r,t[9]*=a,t[2]*=i,t[6]*=r,t[10]*=a,t[3]*=i,t[7]*=r,t[11]*=a,this}getMaxScaleOnAxis(){const e=this.elements,t=e[0]*e[0]+e[1]*e[1]+e[2]*e[2],i=e[4]*e[4]+e[5]*e[5]+e[6]*e[6],r=e[8]*e[8]+e[9]*e[9]+e[10]*e[10];return Math.sqrt(Math.max(t,i,r))}makeTranslation(e,t,i){return e.isVector3?this.set(1,0,0,e.x,0,1,0,e.y,0,0,1,e.z,0,0,0,1):this.set(1,0,0,e,0,1,0,t,0,0,1,i,0,0,0,1),this}makeRotationX(e){const t=Math.cos(e),i=Math.sin(e);return this.set(1,0,0,0,0,t,-i,0,0,i,t,0,0,0,0,1),this}makeRotationY(e){const t=Math.cos(e),i=Math.sin(e);return this.set(t,0,i,0,0,1,0,0,-i,0,t,0,0,0,0,1),this}makeRotationZ(e){const t=Math.cos(e),i=Math.sin(e);return this.set(t,-i,0,0,i,t,0,0,0,0,1,0,0,0,0,1),this}makeRotationAxis(e,t){const i=Math.cos(t),r=Math.sin(t),a=1-i,s=e.x,o=e.y,c=e.z,l=a*s,d=a*o;return this.set(l*s+i,l*o-r*c,l*c+r*o,0,l*o+r*c,d*o+i,d*c-r*s,0,l*c-r*o,d*c+r*s,a*c*c+i,0,0,0,0,1),this}makeScale(e,t,i){return this.set(e,0,0,0,0,t,0,0,0,0,i,0,0,0,0,1),this}makeShear(e,t,i,r,a,s){return this.set(1,i,a,0,e,1,s,0,t,r,1,0,0,0,0,1),this}compose(e,t,i){const r=this.elements,a=t._x,s=t._y,o=t._z,c=t._w,l=a+a,d=s+s,h=o+o,f=a*l,m=a*d,g=a*h,_=s*d,p=s*h,u=o*h,w=c*l,b=c*d,S=c*h,T=i.x,y=i.y,A=i.z;return r[0]=(1-(_+u))*T,r[1]=(m+S)*T,r[2]=(g-b)*T,r[3]=0,r[4]=(m-S)*y,r[5]=(1-(f+u))*y,r[6]=(p+w)*y,r[7]=0,r[8]=(g+b)*A,r[9]=(p-w)*A,r[10]=(1-(f+_))*A,r[11]=0,r[12]=e.x,r[13]=e.y,r[14]=e.z,r[15]=1,this}decompose(e,t,i){const r=this.elements;let a=ni.set(r[0],r[1],r[2]).length();const s=ni.set(r[4],r[5],r[6]).length(),o=ni.set(r[8],r[9],r[10]).length();this.determinant()<0&&(a=-a),e.x=r[12],e.y=r[13],e.z=r[14],jt.copy(this);const l=1/a,d=1/s,h=1/o;return jt.elements[0]*=l,jt.elements[1]*=l,jt.elements[2]*=l,jt.elements[4]*=d,jt.elements[5]*=d,jt.elements[6]*=d,jt.elements[8]*=h,jt.elements[9]*=h,jt.elements[10]*=h,t.setFromRotationMatrix(jt),i.x=a,i.y=s,i.z=o,this}makePerspective(e,t,i,r,a,s,o=dn){const c=this.elements,l=2*a/(t-e),d=2*a/(i-r),h=(t+e)/(t-e),f=(i+r)/(i-r);let m,g;if(o===dn)m=-(s+a)/(s-a),g=-2*s*a/(s-a);else if(o===Dr)m=-s/(s-a),g=-s*a/(s-a);else throw new Error("THREE.Matrix4.makePerspective(): Invalid coordinate system: "+o);return c[0]=l,c[4]=0,c[8]=h,c[12]=0,c[1]=0,c[5]=d,c[9]=f,c[13]=0,c[2]=0,c[6]=0,c[10]=m,c[14]=g,c[3]=0,c[7]=0,c[11]=-1,c[15]=0,this}makeOrthographic(e,t,i,r,a,s,o=dn){const c=this.elements,l=1/(t-e),d=1/(i-r),h=1/(s-a),f=(t+e)*l,m=(i+r)*d;let g,_;if(o===dn)g=(s+a)*h,_=-2*h;else if(o===Dr)g=a*h,_=-1*h;else throw new Error("THREE.Matrix4.makeOrthographic(): Invalid coordinate system: "+o);return c[0]=2*l,c[4]=0,c[8]=0,c[12]=-f,c[1]=0,c[5]=2*d,c[9]=0,c[13]=-m,c[2]=0,c[6]=0,c[10]=_,c[14]=-g,c[3]=0,c[7]=0,c[11]=0,c[15]=1,this}equals(e){const t=this.elements,i=e.elements;for(let r=0;r<16;r++)if(t[r]!==i[r])return!1;return!0}fromArray(e,t=0){for(let i=0;i<16;i++)this.elements[i]=e[i+t];return this}toArray(e=[],t=0){const i=this.elements;return e[t]=i[0],e[t+1]=i[1],e[t+2]=i[2],e[t+3]=i[3],e[t+4]=i[4],e[t+5]=i[5],e[t+6]=i[6],e[t+7]=i[7],e[t+8]=i[8],e[t+9]=i[9],e[t+10]=i[10],e[t+11]=i[11],e[t+12]=i[12],e[t+13]=i[13],e[t+14]=i[14],e[t+15]=i[15],e}}const ni=new k,jt=new at,Zl=new k(0,0,0),Jl=new k(1,1,1),vn=new k,er=new k,Pt=new k,ao=new at,so=new Vi;class Jt{constructor(e=0,t=0,i=0,r=Jt.DEFAULT_ORDER){this.isEuler=!0,this._x=e,this._y=t,this._z=i,this._order=r}get x(){return this._x}set x(e){this._x=e,this._onChangeCallback()}get y(){return this._y}set y(e){this._y=e,this._onChangeCallback()}get z(){return this._z}set z(e){this._z=e,this._onChangeCallback()}get order(){return this._order}set order(e){this._order=e,this._onChangeCallback()}set(e,t,i,r=this._order){return this._x=e,this._y=t,this._z=i,this._order=r,this._onChangeCallback(),this}clone(){return new this.constructor(this._x,this._y,this._z,this._order)}copy(e){return this._x=e._x,this._y=e._y,this._z=e._z,this._order=e._order,this._onChangeCallback(),this}setFromRotationMatrix(e,t=this._order,i=!0){const r=e.elements,a=r[0],s=r[4],o=r[8],c=r[1],l=r[5],d=r[9],h=r[2],f=r[6],m=r[10];switch(t){case"XYZ":this._y=Math.asin(je(o,-1,1)),Math.abs(o)<.9999999?(this._x=Math.atan2(-d,m),this._z=Math.atan2(-s,a)):(this._x=Math.atan2(f,l),this._z=0);break;case"YXZ":this._x=Math.asin(-je(d,-1,1)),Math.abs(d)<.9999999?(this._y=Math.atan2(o,m),this._z=Math.atan2(c,l)):(this._y=Math.atan2(-h,a),this._z=0);break;case"ZXY":this._x=Math.asin(je(f,-1,1)),Math.abs(f)<.9999999?(this._y=Math.atan2(-h,m),this._z=Math.atan2(-s,l)):(this._y=0,this._z=Math.atan2(c,a));break;case"ZYX":this._y=Math.asin(-je(h,-1,1)),Math.abs(h)<.9999999?(this._x=Math.atan2(f,m),this._z=Math.atan2(c,a)):(this._x=0,this._z=Math.atan2(-s,l));break;case"YZX":this._z=Math.asin(je(c,-1,1)),Math.abs(c)<.9999999?(this._x=Math.atan2(-d,l),this._y=Math.atan2(-h,a)):(this._x=0,this._y=Math.atan2(o,m));break;case"XZY":this._z=Math.asin(-je(s,-1,1)),Math.abs(s)<.9999999?(this._x=Math.atan2(f,l),this._y=Math.atan2(o,a)):(this._x=Math.atan2(-d,m),this._y=0);break;default:console.warn("THREE.Euler: .setFromRotationMatrix() encountered an unknown order: "+t)}return this._order=t,i===!0&&this._onChangeCallback(),this}setFromQuaternion(e,t,i){return ao.makeRotationFromQuaternion(e),this.setFromRotationMatrix(ao,t,i)}setFromVector3(e,t=this._order){return this.set(e.x,e.y,e.z,t)}reorder(e){return so.setFromEuler(this),this.setFromQuaternion(so,e)}equals(e){return e._x===this._x&&e._y===this._y&&e._z===this._z&&e._order===this._order}fromArray(e){return this._x=e[0],this._y=e[1],this._z=e[2],e[3]!==void 0&&(this._order=e[3]),this._onChangeCallback(),this}toArray(e=[],t=0){return e[t]=this._x,e[t+1]=this._y,e[t+2]=this._z,e[t+3]=this._order,e}_onChange(e){return this._onChangeCallback=e,this}_onChangeCallback(){}*[Symbol.iterator](){yield this._x,yield this._y,yield this._z,yield this._order}}Jt.DEFAULT_ORDER="XYZ";class Is{constructor(){this.mask=1}set(e){this.mask=(1<<e|0)>>>0}enable(e){this.mask|=1<<e|0}enableAll(){this.mask=-1}toggle(e){this.mask^=1<<e|0}disable(e){this.mask&=~(1<<e|0)}disableAll(){this.mask=0}test(e){return(this.mask&e.mask)!==0}isEnabled(e){return(this.mask&(1<<e|0))!==0}}let Ql=0;const oo=new k,ii=new Vi,nn=new at,tr=new k,Ui=new k,eu=new k,tu=new Vi,co=new k(1,0,0),lo=new k(0,1,0),uo=new k(0,0,1),ho={type:"added"},nu={type:"removed"},ri={type:"childadded",child:null},ia={type:"childremoved",child:null};class _t extends wi{constructor(){super(),this.isObject3D=!0,Object.defineProperty(this,"id",{value:Ql++}),this.uuid=Hi(),this.name="",this.type="Object3D",this.parent=null,this.children=[],this.up=_t.DEFAULT_UP.clone();const e=new k,t=new Jt,i=new Vi,r=new k(1,1,1);function a(){i.setFromEuler(t,!1)}function s(){t.setFromQuaternion(i,void 0,!1)}t._onChange(a),i._onChange(s),Object.defineProperties(this,{position:{configurable:!0,enumerable:!0,value:e},rotation:{configurable:!0,enumerable:!0,value:t},quaternion:{configurable:!0,enumerable:!0,value:i},scale:{configurable:!0,enumerable:!0,value:r},modelViewMatrix:{value:new at},normalMatrix:{value:new Be}}),this.matrix=new at,this.matrixWorld=new at,this.matrixAutoUpdate=_t.DEFAULT_MATRIX_AUTO_UPDATE,this.matrixWorldAutoUpdate=_t.DEFAULT_MATRIX_WORLD_AUTO_UPDATE,this.matrixWorldNeedsUpdate=!1,this.layers=new Is,this.visible=!0,this.castShadow=!1,this.receiveShadow=!1,this.frustumCulled=!0,this.renderOrder=0,this.animations=[],this.userData={}}onBeforeShadow(){}onAfterShadow(){}onBeforeRender(){}onAfterRender(){}applyMatrix4(e){this.matrixAutoUpdate&&this.updateMatrix(),this.matrix.premultiply(e),this.matrix.decompose(this.position,this.quaternion,this.scale)}applyQuaternion(e){return this.quaternion.premultiply(e),this}setRotationFromAxisAngle(e,t){this.quaternion.setFromAxisAngle(e,t)}setRotationFromEuler(e){this.quaternion.setFromEuler(e,!0)}setRotationFromMatrix(e){this.quaternion.setFromRotationMatrix(e)}setRotationFromQuaternion(e){this.quaternion.copy(e)}rotateOnAxis(e,t){return ii.setFromAxisAngle(e,t),this.quaternion.multiply(ii),this}rotateOnWorldAxis(e,t){return ii.setFromAxisAngle(e,t),this.quaternion.premultiply(ii),this}rotateX(e){return this.rotateOnAxis(co,e)}rotateY(e){return this.rotateOnAxis(lo,e)}rotateZ(e){return this.rotateOnAxis(uo,e)}translateOnAxis(e,t){return oo.copy(e).applyQuaternion(this.quaternion),this.position.add(oo.multiplyScalar(t)),this}translateX(e){return this.translateOnAxis(co,e)}translateY(e){return this.translateOnAxis(lo,e)}translateZ(e){return this.translateOnAxis(uo,e)}localToWorld(e){return this.updateWorldMatrix(!0,!1),e.applyMatrix4(this.matrixWorld)}worldToLocal(e){return this.updateWorldMatrix(!0,!1),e.applyMatrix4(nn.copy(this.matrixWorld).invert())}lookAt(e,t,i){e.isVector3?tr.copy(e):tr.set(e,t,i);const r=this.parent;this.updateWorldMatrix(!0,!1),Ui.setFromMatrixPosition(this.matrixWorld),this.isCamera||this.isLight?nn.lookAt(Ui,tr,this.up):nn.lookAt(tr,Ui,this.up),this.quaternion.setFromRotationMatrix(nn),r&&(nn.extractRotation(r.matrixWorld),ii.setFromRotationMatrix(nn),this.quaternion.premultiply(ii.invert()))}add(e){if(arguments.length>1){for(let t=0;t<arguments.length;t++)this.add(arguments[t]);return this}return e===this?(console.error("THREE.Object3D.add: object can't be added as a child of itself.",e),this):(e&&e.isObject3D?(e.removeFromParent(),e.parent=this,this.children.push(e),e.dispatchEvent(ho),ri.child=e,this.dispatchEvent(ri),ri.child=null):console.error("THREE.Object3D.add: object not an instance of THREE.Object3D.",e),this)}remove(e){if(arguments.length>1){for(let i=0;i<arguments.length;i++)this.remove(arguments[i]);return this}const t=this.children.indexOf(e);return t!==-1&&(e.parent=null,this.children.splice(t,1),e.dispatchEvent(nu),ia.child=e,this.dispatchEvent(ia),ia.child=null),this}removeFromParent(){const e=this.parent;return e!==null&&e.remove(this),this}clear(){return this.remove(...this.children)}attach(e){return this.updateWorldMatrix(!0,!1),nn.copy(this.matrixWorld).invert(),e.parent!==null&&(e.parent.updateWorldMatrix(!0,!1),nn.multiply(e.parent.matrixWorld)),e.applyMatrix4(nn),e.removeFromParent(),e.parent=this,this.children.push(e),e.updateWorldMatrix(!1,!0),e.dispatchEvent(ho),ri.child=e,this.dispatchEvent(ri),ri.child=null,this}getObjectById(e){return this.getObjectByProperty("id",e)}getObjectByName(e){return this.getObjectByProperty("name",e)}getObjectByProperty(e,t){if(this[e]===t)return this;for(let i=0,r=this.children.length;i<r;i++){const s=this.children[i].getObjectByProperty(e,t);if(s!==void 0)return s}}getObjectsByProperty(e,t,i=[]){this[e]===t&&i.push(this);const r=this.children;for(let a=0,s=r.length;a<s;a++)r[a].getObjectsByProperty(e,t,i);return i}getWorldPosition(e){return this.updateWorldMatrix(!0,!1),e.setFromMatrixPosition(this.matrixWorld)}getWorldQuaternion(e){return this.updateWorldMatrix(!0,!1),this.matrixWorld.decompose(Ui,e,eu),e}getWorldScale(e){return this.updateWorldMatrix(!0,!1),this.matrixWorld.decompose(Ui,tu,e),e}getWorldDirection(e){this.updateWorldMatrix(!0,!1);const t=this.matrixWorld.elements;return e.set(t[8],t[9],t[10]).normalize()}raycast(){}traverse(e){e(this);const t=this.children;for(let i=0,r=t.length;i<r;i++)t[i].traverse(e)}traverseVisible(e){if(this.visible===!1)return;e(this);const t=this.children;for(let i=0,r=t.length;i<r;i++)t[i].traverseVisible(e)}traverseAncestors(e){const t=this.parent;t!==null&&(e(t),t.traverseAncestors(e))}updateMatrix(){this.matrix.compose(this.position,this.quaternion,this.scale),this.matrixWorldNeedsUpdate=!0}updateMatrixWorld(e){this.matrixAutoUpdate&&this.updateMatrix(),(this.matrixWorldNeedsUpdate||e)&&(this.matrixWorldAutoUpdate===!0&&(this.parent===null?this.matrixWorld.copy(this.matrix):this.matrixWorld.multiplyMatrices(this.parent.matrixWorld,this.matrix)),this.matrixWorldNeedsUpdate=!1,e=!0);const t=this.children;for(let i=0,r=t.length;i<r;i++)t[i].updateMatrixWorld(e)}updateWorldMatrix(e,t){const i=this.parent;if(e===!0&&i!==null&&i.updateWorldMatrix(!0,!1),this.matrixAutoUpdate&&this.updateMatrix(),this.matrixWorldAutoUpdate===!0&&(this.parent===null?this.matrixWorld.copy(this.matrix):this.matrixWorld.multiplyMatrices(this.parent.matrixWorld,this.matrix)),t===!0){const r=this.children;for(let a=0,s=r.length;a<s;a++)r[a].updateWorldMatrix(!1,!0)}}toJSON(e){const t=e===void 0||typeof e=="string",i={};t&&(e={geometries:{},materials:{},textures:{},images:{},shapes:{},skeletons:{},animations:{},nodes:{}},i.metadata={version:4.6,type:"Object",generator:"Object3D.toJSON"});const r={};r.uuid=this.uuid,r.type=this.type,this.name!==""&&(r.name=this.name),this.castShadow===!0&&(r.castShadow=!0),this.receiveShadow===!0&&(r.receiveShadow=!0),this.visible===!1&&(r.visible=!1),this.frustumCulled===!1&&(r.frustumCulled=!1),this.renderOrder!==0&&(r.renderOrder=this.renderOrder),Object.keys(this.userData).length>0&&(r.userData=this.userData),r.layers=this.layers.mask,r.matrix=this.matrix.toArray(),r.up=this.up.toArray(),this.matrixAutoUpdate===!1&&(r.matrixAutoUpdate=!1),this.isInstancedMesh&&(r.type="InstancedMesh",r.count=this.count,r.instanceMatrix=this.instanceMatrix.toJSON(),this.instanceColor!==null&&(r.instanceColor=this.instanceColor.toJSON())),this.isBatchedMesh&&(r.type="BatchedMesh",r.perObjectFrustumCulled=this.perObjectFrustumCulled,r.sortObjects=this.sortObjects,r.drawRanges=this._drawRanges,r.reservedRanges=this._reservedRanges,r.visibility=this._visibility,r.active=this._active,r.bounds=this._bounds.map(o=>({boxInitialized:o.boxInitialized,boxMin:o.box.min.toArray(),boxMax:o.box.max.toArray(),sphereInitialized:o.sphereInitialized,sphereRadius:o.sphere.radius,sphereCenter:o.sphere.center.toArray()})),r.maxInstanceCount=this._maxInstanceCount,r.maxVertexCount=this._maxVertexCount,r.maxIndexCount=this._maxIndexCount,r.geometryInitialized=this._geometryInitialized,r.geometryCount=this._geometryCount,r.matricesTexture=this._matricesTexture.toJSON(e),this._colorsTexture!==null&&(r.colorsTexture=this._colorsTexture.toJSON(e)),this.boundingSphere!==null&&(r.boundingSphere={center:r.boundingSphere.center.toArray(),radius:r.boundingSphere.radius}),this.boundingBox!==null&&(r.boundingBox={min:r.boundingBox.min.toArray(),max:r.boundingBox.max.toArray()}));function a(o,c){return o[c.uuid]===void 0&&(o[c.uuid]=c.toJSON(e)),c.uuid}if(this.isScene)this.background&&(this.background.isColor?r.background=this.background.toJSON():this.background.isTexture&&(r.background=this.background.toJSON(e).uuid)),this.environment&&this.environment.isTexture&&this.environment.isRenderTargetTexture!==!0&&(r.environment=this.environment.toJSON(e).uuid);else if(this.isMesh||this.isLine||this.isPoints){r.geometry=a(e.geometries,this.geometry);const o=this.geometry.parameters;if(o!==void 0&&o.shapes!==void 0){const c=o.shapes;if(Array.isArray(c))for(let l=0,d=c.length;l<d;l++){const h=c[l];a(e.shapes,h)}else a(e.shapes,c)}}if(this.isSkinnedMesh&&(r.bindMode=this.bindMode,r.bindMatrix=this.bindMatrix.toArray(),this.skeleton!==void 0&&(a(e.skeletons,this.skeleton),r.skeleton=this.skeleton.uuid)),this.material!==void 0)if(Array.isArray(this.material)){const o=[];for(let c=0,l=this.material.length;c<l;c++)o.push(a(e.materials,this.material[c]));r.material=o}else r.material=a(e.materials,this.material);if(this.children.length>0){r.children=[];for(let o=0;o<this.children.length;o++)r.children.push(this.children[o].toJSON(e).object)}if(this.animations.length>0){r.animations=[];for(let o=0;o<this.animations.length;o++){const c=this.animations[o];r.animations.push(a(e.animations,c))}}if(t){const o=s(e.geometries),c=s(e.materials),l=s(e.textures),d=s(e.images),h=s(e.shapes),f=s(e.skeletons),m=s(e.animations),g=s(e.nodes);o.length>0&&(i.geometries=o),c.length>0&&(i.materials=c),l.length>0&&(i.textures=l),d.length>0&&(i.images=d),h.length>0&&(i.shapes=h),f.length>0&&(i.skeletons=f),m.length>0&&(i.animations=m),g.length>0&&(i.nodes=g)}return i.object=r,i;function s(o){const c=[];for(const l in o){const d=o[l];delete d.metadata,c.push(d)}return c}}clone(e){return new this.constructor().copy(this,e)}copy(e,t=!0){if(this.name=e.name,this.up.copy(e.up),this.position.copy(e.position),this.rotation.order=e.rotation.order,this.quaternion.copy(e.quaternion),this.scale.copy(e.scale),this.matrix.copy(e.matrix),this.matrixWorld.copy(e.matrixWorld),this.matrixAutoUpdate=e.matrixAutoUpdate,this.matrixWorldAutoUpdate=e.matrixWorldAutoUpdate,this.matrixWorldNeedsUpdate=e.matrixWorldNeedsUpdate,this.layers.mask=e.layers.mask,this.visible=e.visible,this.castShadow=e.castShadow,this.receiveShadow=e.receiveShadow,this.frustumCulled=e.frustumCulled,this.renderOrder=e.renderOrder,this.animations=e.animations.slice(),this.userData=JSON.parse(JSON.stringify(e.userData)),t===!0)for(let i=0;i<e.children.length;i++){const r=e.children[i];this.add(r.clone())}return this}}_t.DEFAULT_UP=new k(0,1,0);_t.DEFAULT_MATRIX_AUTO_UPDATE=!0;_t.DEFAULT_MATRIX_WORLD_AUTO_UPDATE=!0;const Wt=new k,rn=new k,ra=new k,an=new k,ai=new k,si=new k,fo=new k,aa=new k,sa=new k,oa=new k,ca=new lt,la=new lt,ua=new lt;class Ot{constructor(e=new k,t=new k,i=new k){this.a=e,this.b=t,this.c=i}static getNormal(e,t,i,r){r.subVectors(i,t),Wt.subVectors(e,t),r.cross(Wt);const a=r.lengthSq();return a>0?r.multiplyScalar(1/Math.sqrt(a)):r.set(0,0,0)}static getBarycoord(e,t,i,r,a){Wt.subVectors(r,t),rn.subVectors(i,t),ra.subVectors(e,t);const s=Wt.dot(Wt),o=Wt.dot(rn),c=Wt.dot(ra),l=rn.dot(rn),d=rn.dot(ra),h=s*l-o*o;if(h===0)return a.set(0,0,0),null;const f=1/h,m=(l*c-o*d)*f,g=(s*d-o*c)*f;return a.set(1-m-g,g,m)}static containsPoint(e,t,i,r){return this.getBarycoord(e,t,i,r,an)===null?!1:an.x>=0&&an.y>=0&&an.x+an.y<=1}static getInterpolation(e,t,i,r,a,s,o,c){return this.getBarycoord(e,t,i,r,an)===null?(c.x=0,c.y=0,"z"in c&&(c.z=0),"w"in c&&(c.w=0),null):(c.setScalar(0),c.addScaledVector(a,an.x),c.addScaledVector(s,an.y),c.addScaledVector(o,an.z),c)}static getInterpolatedAttribute(e,t,i,r,a,s){return ca.setScalar(0),la.setScalar(0),ua.setScalar(0),ca.fromBufferAttribute(e,t),la.fromBufferAttribute(e,i),ua.fromBufferAttribute(e,r),s.setScalar(0),s.addScaledVector(ca,a.x),s.addScaledVector(la,a.y),s.addScaledVector(ua,a.z),s}static isFrontFacing(e,t,i,r){return Wt.subVectors(i,t),rn.subVectors(e,t),Wt.cross(rn).dot(r)<0}set(e,t,i){return this.a.copy(e),this.b.copy(t),this.c.copy(i),this}setFromPointsAndIndices(e,t,i,r){return this.a.copy(e[t]),this.b.copy(e[i]),this.c.copy(e[r]),this}setFromAttributeAndIndices(e,t,i,r){return this.a.fromBufferAttribute(e,t),this.b.fromBufferAttribute(e,i),this.c.fromBufferAttribute(e,r),this}clone(){return new this.constructor().copy(this)}copy(e){return this.a.copy(e.a),this.b.copy(e.b),this.c.copy(e.c),this}getArea(){return Wt.subVectors(this.c,this.b),rn.subVectors(this.a,this.b),Wt.cross(rn).length()*.5}getMidpoint(e){return e.addVectors(this.a,this.b).add(this.c).multiplyScalar(1/3)}getNormal(e){return Ot.getNormal(this.a,this.b,this.c,e)}getPlane(e){return e.setFromCoplanarPoints(this.a,this.b,this.c)}getBarycoord(e,t){return Ot.getBarycoord(e,this.a,this.b,this.c,t)}getInterpolation(e,t,i,r,a){return Ot.getInterpolation(e,this.a,this.b,this.c,t,i,r,a)}containsPoint(e){return Ot.containsPoint(e,this.a,this.b,this.c)}isFrontFacing(e){return Ot.isFrontFacing(this.a,this.b,this.c,e)}intersectsBox(e){return e.intersectsTriangle(this)}closestPointToPoint(e,t){const i=this.a,r=this.b,a=this.c;let s,o;ai.subVectors(r,i),si.subVectors(a,i),aa.subVectors(e,i);const c=ai.dot(aa),l=si.dot(aa);if(c<=0&&l<=0)return t.copy(i);sa.subVectors(e,r);const d=ai.dot(sa),h=si.dot(sa);if(d>=0&&h<=d)return t.copy(r);const f=c*h-d*l;if(f<=0&&c>=0&&d<=0)return s=c/(c-d),t.copy(i).addScaledVector(ai,s);oa.subVectors(e,a);const m=ai.dot(oa),g=si.dot(oa);if(g>=0&&m<=g)return t.copy(a);const _=m*l-c*g;if(_<=0&&l>=0&&g<=0)return o=l/(l-g),t.copy(i).addScaledVector(si,o);const p=d*g-m*h;if(p<=0&&h-d>=0&&m-g>=0)return fo.subVectors(a,r),o=(h-d)/(h-d+(m-g)),t.copy(r).addScaledVector(fo,o);const u=1/(p+_+f);return s=_*u,o=f*u,t.copy(i).addScaledVector(ai,s).addScaledVector(si,o)}equals(e){return e.a.equals(this.a)&&e.b.equals(this.b)&&e.c.equals(this.c)}}const Ec={aliceblue:15792383,antiquewhite:16444375,aqua:65535,aquamarine:8388564,azure:15794175,beige:16119260,bisque:16770244,black:0,blanchedalmond:16772045,blue:255,blueviolet:9055202,brown:10824234,burlywood:14596231,cadetblue:6266528,chartreuse:8388352,chocolate:13789470,coral:16744272,cornflowerblue:6591981,cornsilk:16775388,crimson:14423100,cyan:65535,darkblue:139,darkcyan:35723,darkgoldenrod:12092939,darkgray:11119017,darkgreen:25600,darkgrey:11119017,darkkhaki:12433259,darkmagenta:9109643,darkolivegreen:5597999,darkorange:16747520,darkorchid:10040012,darkred:9109504,darksalmon:15308410,darkseagreen:9419919,darkslateblue:4734347,darkslategray:3100495,darkslategrey:3100495,darkturquoise:52945,darkviolet:9699539,deeppink:16716947,deepskyblue:49151,dimgray:6908265,dimgrey:6908265,dodgerblue:2003199,firebrick:11674146,floralwhite:16775920,forestgreen:2263842,fuchsia:16711935,gainsboro:14474460,ghostwhite:16316671,gold:16766720,goldenrod:14329120,gray:8421504,green:32768,greenyellow:11403055,grey:8421504,honeydew:15794160,hotpink:16738740,indianred:13458524,indigo:4915330,ivory:16777200,khaki:15787660,lavender:15132410,lavenderblush:16773365,lawngreen:8190976,lemonchiffon:16775885,lightblue:11393254,lightcoral:15761536,lightcyan:14745599,lightgoldenrodyellow:16448210,lightgray:13882323,lightgreen:9498256,lightgrey:13882323,lightpink:16758465,lightsalmon:16752762,lightseagreen:2142890,lightskyblue:8900346,lightslategray:7833753,lightslategrey:7833753,lightsteelblue:11584734,lightyellow:16777184,lime:65280,limegreen:3329330,linen:16445670,magenta:16711935,maroon:8388608,mediumaquamarine:6737322,mediumblue:205,mediumorchid:12211667,mediumpurple:9662683,mediumseagreen:3978097,mediumslateblue:8087790,mediumspringgreen:64154,mediumturquoise:4772300,mediumvioletred:13047173,midnightblue:1644912,mintcream:16121850,mistyrose:16770273,moccasin:16770229,navajowhite:16768685,navy:128,oldlace:16643558,olive:8421376,olivedrab:7048739,orange:16753920,orangered:16729344,orchid:14315734,palegoldenrod:15657130,palegreen:10025880,paleturquoise:11529966,palevioletred:14381203,papayawhip:16773077,peachpuff:16767673,peru:13468991,pink:16761035,plum:14524637,powderblue:11591910,purple:8388736,rebeccapurple:6697881,red:16711680,rosybrown:12357519,royalblue:4286945,saddlebrown:9127187,salmon:16416882,sandybrown:16032864,seagreen:3050327,seashell:16774638,sienna:10506797,silver:12632256,skyblue:8900331,slateblue:6970061,slategray:7372944,slategrey:7372944,snow:16775930,springgreen:65407,steelblue:4620980,tan:13808780,teal:32896,thistle:14204888,tomato:16737095,turquoise:4251856,violet:15631086,wheat:16113331,white:16777215,whitesmoke:16119285,yellow:16776960,yellowgreen:10145074},xn={h:0,s:0,l:0},nr={h:0,s:0,l:0};function da(n,e,t){return t<0&&(t+=1),t>1&&(t-=1),t<1/6?n+(e-n)*6*t:t<1/2?e:t<2/3?n+(e-n)*6*(2/3-t):n}class ve{constructor(e,t,i){return this.isColor=!0,this.r=1,this.g=1,this.b=1,this.set(e,t,i)}set(e,t,i){if(t===void 0&&i===void 0){const r=e;r&&r.isColor?this.copy(r):typeof r=="number"?this.setHex(r):typeof r=="string"&&this.setStyle(r)}else this.setRGB(e,t,i);return this}setScalar(e){return this.r=e,this.g=e,this.b=e,this}setHex(e,t=Lt){return e=Math.floor(e),this.r=(e>>16&255)/255,this.g=(e>>8&255)/255,this.b=(e&255)/255,Ke.toWorkingColorSpace(this,t),this}setRGB(e,t,i,r=Ke.workingColorSpace){return this.r=e,this.g=t,this.b=i,Ke.toWorkingColorSpace(this,r),this}setHSL(e,t,i,r=Ke.workingColorSpace){if(e=Ol(e,1),t=je(t,0,1),i=je(i,0,1),t===0)this.r=this.g=this.b=i;else{const a=i<=.5?i*(1+t):i+t-i*t,s=2*i-a;this.r=da(s,a,e+1/3),this.g=da(s,a,e),this.b=da(s,a,e-1/3)}return Ke.toWorkingColorSpace(this,r),this}setStyle(e,t=Lt){function i(a){a!==void 0&&parseFloat(a)<1&&console.warn("THREE.Color: Alpha component of "+e+" will be ignored.")}let r;if(r=/^(\w+)\(([^\)]*)\)/.exec(e)){let a;const s=r[1],o=r[2];switch(s){case"rgb":case"rgba":if(a=/^\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*(?:,\s*(\d*\.?\d+)\s*)?$/.exec(o))return i(a[4]),this.setRGB(Math.min(255,parseInt(a[1],10))/255,Math.min(255,parseInt(a[2],10))/255,Math.min(255,parseInt(a[3],10))/255,t);if(a=/^\s*(\d+)\%\s*,\s*(\d+)\%\s*,\s*(\d+)\%\s*(?:,\s*(\d*\.?\d+)\s*)?$/.exec(o))return i(a[4]),this.setRGB(Math.min(100,parseInt(a[1],10))/100,Math.min(100,parseInt(a[2],10))/100,Math.min(100,parseInt(a[3],10))/100,t);break;case"hsl":case"hsla":if(a=/^\s*(\d*\.?\d+)\s*,\s*(\d*\.?\d+)\%\s*,\s*(\d*\.?\d+)\%\s*(?:,\s*(\d*\.?\d+)\s*)?$/.exec(o))return i(a[4]),this.setHSL(parseFloat(a[1])/360,parseFloat(a[2])/100,parseFloat(a[3])/100,t);break;default:console.warn("THREE.Color: Unknown color model "+e)}}else if(r=/^\#([A-Fa-f\d]+)$/.exec(e)){const a=r[1],s=a.length;if(s===3)return this.setRGB(parseInt(a.charAt(0),16)/15,parseInt(a.charAt(1),16)/15,parseInt(a.charAt(2),16)/15,t);if(s===6)return this.setHex(parseInt(a,16),t);console.warn("THREE.Color: Invalid hex color "+e)}else if(e&&e.length>0)return this.setColorName(e,t);return this}setColorName(e,t=Lt){const i=Ec[e.toLowerCase()];return i!==void 0?this.setHex(i,t):console.warn("THREE.Color: Unknown color "+e),this}clone(){return new this.constructor(this.r,this.g,this.b)}copy(e){return this.r=e.r,this.g=e.g,this.b=e.b,this}copySRGBToLinear(e){return this.r=fn(e.r),this.g=fn(e.g),this.b=fn(e.b),this}copyLinearToSRGB(e){return this.r=vi(e.r),this.g=vi(e.g),this.b=vi(e.b),this}convertSRGBToLinear(){return this.copySRGBToLinear(this),this}convertLinearToSRGB(){return this.copyLinearToSRGB(this),this}getHex(e=Lt){return Ke.fromWorkingColorSpace(Mt.copy(this),e),Math.round(je(Mt.r*255,0,255))*65536+Math.round(je(Mt.g*255,0,255))*256+Math.round(je(Mt.b*255,0,255))}getHexString(e=Lt){return("000000"+this.getHex(e).toString(16)).slice(-6)}getHSL(e,t=Ke.workingColorSpace){Ke.fromWorkingColorSpace(Mt.copy(this),t);const i=Mt.r,r=Mt.g,a=Mt.b,s=Math.max(i,r,a),o=Math.min(i,r,a);let c,l;const d=(o+s)/2;if(o===s)c=0,l=0;else{const h=s-o;switch(l=d<=.5?h/(s+o):h/(2-s-o),s){case i:c=(r-a)/h+(r<a?6:0);break;case r:c=(a-i)/h+2;break;case a:c=(i-r)/h+4;break}c/=6}return e.h=c,e.s=l,e.l=d,e}getRGB(e,t=Ke.workingColorSpace){return Ke.fromWorkingColorSpace(Mt.copy(this),t),e.r=Mt.r,e.g=Mt.g,e.b=Mt.b,e}getStyle(e=Lt){Ke.fromWorkingColorSpace(Mt.copy(this),e);const t=Mt.r,i=Mt.g,r=Mt.b;return e!==Lt?`color(${e} ${t.toFixed(3)} ${i.toFixed(3)} ${r.toFixed(3)})`:`rgb(${Math.round(t*255)},${Math.round(i*255)},${Math.round(r*255)})`}offsetHSL(e,t,i){return this.getHSL(xn),this.setHSL(xn.h+e,xn.s+t,xn.l+i)}add(e){return this.r+=e.r,this.g+=e.g,this.b+=e.b,this}addColors(e,t){return this.r=e.r+t.r,this.g=e.g+t.g,this.b=e.b+t.b,this}addScalar(e){return this.r+=e,this.g+=e,this.b+=e,this}sub(e){return this.r=Math.max(0,this.r-e.r),this.g=Math.max(0,this.g-e.g),this.b=Math.max(0,this.b-e.b),this}multiply(e){return this.r*=e.r,this.g*=e.g,this.b*=e.b,this}multiplyScalar(e){return this.r*=e,this.g*=e,this.b*=e,this}lerp(e,t){return this.r+=(e.r-this.r)*t,this.g+=(e.g-this.g)*t,this.b+=(e.b-this.b)*t,this}lerpColors(e,t,i){return this.r=e.r+(t.r-e.r)*i,this.g=e.g+(t.g-e.g)*i,this.b=e.b+(t.b-e.b)*i,this}lerpHSL(e,t){this.getHSL(xn),e.getHSL(nr);const i=qr(xn.h,nr.h,t),r=qr(xn.s,nr.s,t),a=qr(xn.l,nr.l,t);return this.setHSL(i,r,a),this}setFromVector3(e){return this.r=e.x,this.g=e.y,this.b=e.z,this}applyMatrix3(e){const t=this.r,i=this.g,r=this.b,a=e.elements;return this.r=a[0]*t+a[3]*i+a[6]*r,this.g=a[1]*t+a[4]*i+a[7]*r,this.b=a[2]*t+a[5]*i+a[8]*r,this}equals(e){return e.r===this.r&&e.g===this.g&&e.b===this.b}fromArray(e,t=0){return this.r=e[t],this.g=e[t+1],this.b=e[t+2],this}toArray(e=[],t=0){return e[t]=this.r,e[t+1]=this.g,e[t+2]=this.b,e}fromBufferAttribute(e,t){return this.r=e.getX(t),this.g=e.getY(t),this.b=e.getZ(t),this}toJSON(){return this.getHex()}*[Symbol.iterator](){yield this.r,yield this.g,yield this.b}}const Mt=new ve;ve.NAMES=Ec;let iu=0;class Ri extends wi{constructor(){super(),this.isMaterial=!0,Object.defineProperty(this,"id",{value:iu++}),this.uuid=Hi(),this.name="",this.type="Material",this.blending=gi,this.side=An,this.vertexColors=!1,this.opacity=1,this.transparent=!1,this.alphaHash=!1,this.blendSrc=Ca,this.blendDst=Pa,this.blendEquation=Hn,this.blendSrcAlpha=null,this.blendDstAlpha=null,this.blendEquationAlpha=null,this.blendColor=new ve(0,0,0),this.blendAlpha=0,this.depthFunc=Mi,this.depthTest=!0,this.depthWrite=!0,this.stencilWriteMask=255,this.stencilFunc=Js,this.stencilRef=0,this.stencilFuncMask=255,this.stencilFail=Zn,this.stencilZFail=Zn,this.stencilZPass=Zn,this.stencilWrite=!1,this.clippingPlanes=null,this.clipIntersection=!1,this.clipShadows=!1,this.shadowSide=null,this.colorWrite=!0,this.precision=null,this.polygonOffset=!1,this.polygonOffsetFactor=0,this.polygonOffsetUnits=0,this.dithering=!1,this.alphaToCoverage=!1,this.premultipliedAlpha=!1,this.forceSinglePass=!1,this.visible=!0,this.toneMapped=!0,this.userData={},this.version=0,this._alphaTest=0}get alphaTest(){return this._alphaTest}set alphaTest(e){this._alphaTest>0!=e>0&&this.version++,this._alphaTest=e}onBeforeRender(){}onBeforeCompile(){}customProgramCacheKey(){return this.onBeforeCompile.toString()}setValues(e){if(e!==void 0)for(const t in e){const i=e[t];if(i===void 0){console.warn(`THREE.Material: parameter '${t}' has value of undefined.`);continue}const r=this[t];if(r===void 0){console.warn(`THREE.Material: '${t}' is not a property of THREE.${this.type}.`);continue}r&&r.isColor?r.set(i):r&&r.isVector3&&i&&i.isVector3?r.copy(i):this[t]=i}}toJSON(e){const t=e===void 0||typeof e=="string";t&&(e={textures:{},images:{}});const i={metadata:{version:4.6,type:"Material",generator:"Material.toJSON"}};i.uuid=this.uuid,i.type=this.type,this.name!==""&&(i.name=this.name),this.color&&this.color.isColor&&(i.color=this.color.getHex()),this.roughness!==void 0&&(i.roughness=this.roughness),this.metalness!==void 0&&(i.metalness=this.metalness),this.sheen!==void 0&&(i.sheen=this.sheen),this.sheenColor&&this.sheenColor.isColor&&(i.sheenColor=this.sheenColor.getHex()),this.sheenRoughness!==void 0&&(i.sheenRoughness=this.sheenRoughness),this.emissive&&this.emissive.isColor&&(i.emissive=this.emissive.getHex()),this.emissiveIntensity!==void 0&&this.emissiveIntensity!==1&&(i.emissiveIntensity=this.emissiveIntensity),this.specular&&this.specular.isColor&&(i.specular=this.specular.getHex()),this.specularIntensity!==void 0&&(i.specularIntensity=this.specularIntensity),this.specularColor&&this.specularColor.isColor&&(i.specularColor=this.specularColor.getHex()),this.shininess!==void 0&&(i.shininess=this.shininess),this.clearcoat!==void 0&&(i.clearcoat=this.clearcoat),this.clearcoatRoughness!==void 0&&(i.clearcoatRoughness=this.clearcoatRoughness),this.clearcoatMap&&this.clearcoatMap.isTexture&&(i.clearcoatMap=this.clearcoatMap.toJSON(e).uuid),this.clearcoatRoughnessMap&&this.clearcoatRoughnessMap.isTexture&&(i.clearcoatRoughnessMap=this.clearcoatRoughnessMap.toJSON(e).uuid),this.clearcoatNormalMap&&this.clearcoatNormalMap.isTexture&&(i.clearcoatNormalMap=this.clearcoatNormalMap.toJSON(e).uuid,i.clearcoatNormalScale=this.clearcoatNormalScale.toArray()),this.dispersion!==void 0&&(i.dispersion=this.dispersion),this.iridescence!==void 0&&(i.iridescence=this.iridescence),this.iridescenceIOR!==void 0&&(i.iridescenceIOR=this.iridescenceIOR),this.iridescenceThicknessRange!==void 0&&(i.iridescenceThicknessRange=this.iridescenceThicknessRange),this.iridescenceMap&&this.iridescenceMap.isTexture&&(i.iridescenceMap=this.iridescenceMap.toJSON(e).uuid),this.iridescenceThicknessMap&&this.iridescenceThicknessMap.isTexture&&(i.iridescenceThicknessMap=this.iridescenceThicknessMap.toJSON(e).uuid),this.anisotropy!==void 0&&(i.anisotropy=this.anisotropy),this.anisotropyRotation!==void 0&&(i.anisotropyRotation=this.anisotropyRotation),this.anisotropyMap&&this.anisotropyMap.isTexture&&(i.anisotropyMap=this.anisotropyMap.toJSON(e).uuid),this.map&&this.map.isTexture&&(i.map=this.map.toJSON(e).uuid),this.matcap&&this.matcap.isTexture&&(i.matcap=this.matcap.toJSON(e).uuid),this.alphaMap&&this.alphaMap.isTexture&&(i.alphaMap=this.alphaMap.toJSON(e).uuid),this.lightMap&&this.lightMap.isTexture&&(i.lightMap=this.lightMap.toJSON(e).uuid,i.lightMapIntensity=this.lightMapIntensity),this.aoMap&&this.aoMap.isTexture&&(i.aoMap=this.aoMap.toJSON(e).uuid,i.aoMapIntensity=this.aoMapIntensity),this.bumpMap&&this.bumpMap.isTexture&&(i.bumpMap=this.bumpMap.toJSON(e).uuid,i.bumpScale=this.bumpScale),this.normalMap&&this.normalMap.isTexture&&(i.normalMap=this.normalMap.toJSON(e).uuid,i.normalMapType=this.normalMapType,i.normalScale=this.normalScale.toArray()),this.displacementMap&&this.displacementMap.isTexture&&(i.displacementMap=this.displacementMap.toJSON(e).uuid,i.displacementScale=this.displacementScale,i.displacementBias=this.displacementBias),this.roughnessMap&&this.roughnessMap.isTexture&&(i.roughnessMap=this.roughnessMap.toJSON(e).uuid),this.metalnessMap&&this.metalnessMap.isTexture&&(i.metalnessMap=this.metalnessMap.toJSON(e).uuid),this.emissiveMap&&this.emissiveMap.isTexture&&(i.emissiveMap=this.emissiveMap.toJSON(e).uuid),this.specularMap&&this.specularMap.isTexture&&(i.specularMap=this.specularMap.toJSON(e).uuid),this.specularIntensityMap&&this.specularIntensityMap.isTexture&&(i.specularIntensityMap=this.specularIntensityMap.toJSON(e).uuid),this.specularColorMap&&this.specularColorMap.isTexture&&(i.specularColorMap=this.specularColorMap.toJSON(e).uuid),this.envMap&&this.envMap.isTexture&&(i.envMap=this.envMap.toJSON(e).uuid,this.combine!==void 0&&(i.combine=this.combine)),this.envMapRotation!==void 0&&(i.envMapRotation=this.envMapRotation.toArray()),this.envMapIntensity!==void 0&&(i.envMapIntensity=this.envMapIntensity),this.reflectivity!==void 0&&(i.reflectivity=this.reflectivity),this.refractionRatio!==void 0&&(i.refractionRatio=this.refractionRatio),this.gradientMap&&this.gradientMap.isTexture&&(i.gradientMap=this.gradientMap.toJSON(e).uuid),this.transmission!==void 0&&(i.transmission=this.transmission),this.transmissionMap&&this.transmissionMap.isTexture&&(i.transmissionMap=this.transmissionMap.toJSON(e).uuid),this.thickness!==void 0&&(i.thickness=this.thickness),this.thicknessMap&&this.thicknessMap.isTexture&&(i.thicknessMap=this.thicknessMap.toJSON(e).uuid),this.attenuationDistance!==void 0&&this.attenuationDistance!==1/0&&(i.attenuationDistance=this.attenuationDistance),this.attenuationColor!==void 0&&(i.attenuationColor=this.attenuationColor.getHex()),this.size!==void 0&&(i.size=this.size),this.shadowSide!==null&&(i.shadowSide=this.shadowSide),this.sizeAttenuation!==void 0&&(i.sizeAttenuation=this.sizeAttenuation),this.blending!==gi&&(i.blending=this.blending),this.side!==An&&(i.side=this.side),this.vertexColors===!0&&(i.vertexColors=!0),this.opacity<1&&(i.opacity=this.opacity),this.transparent===!0&&(i.transparent=!0),this.blendSrc!==Ca&&(i.blendSrc=this.blendSrc),this.blendDst!==Pa&&(i.blendDst=this.blendDst),this.blendEquation!==Hn&&(i.blendEquation=this.blendEquation),this.blendSrcAlpha!==null&&(i.blendSrcAlpha=this.blendSrcAlpha),this.blendDstAlpha!==null&&(i.blendDstAlpha=this.blendDstAlpha),this.blendEquationAlpha!==null&&(i.blendEquationAlpha=this.blendEquationAlpha),this.blendColor&&this.blendColor.isColor&&(i.blendColor=this.blendColor.getHex()),this.blendAlpha!==0&&(i.blendAlpha=this.blendAlpha),this.depthFunc!==Mi&&(i.depthFunc=this.depthFunc),this.depthTest===!1&&(i.depthTest=this.depthTest),this.depthWrite===!1&&(i.depthWrite=this.depthWrite),this.colorWrite===!1&&(i.colorWrite=this.colorWrite),this.stencilWriteMask!==255&&(i.stencilWriteMask=this.stencilWriteMask),this.stencilFunc!==Js&&(i.stencilFunc=this.stencilFunc),this.stencilRef!==0&&(i.stencilRef=this.stencilRef),this.stencilFuncMask!==255&&(i.stencilFuncMask=this.stencilFuncMask),this.stencilFail!==Zn&&(i.stencilFail=this.stencilFail),this.stencilZFail!==Zn&&(i.stencilZFail=this.stencilZFail),this.stencilZPass!==Zn&&(i.stencilZPass=this.stencilZPass),this.stencilWrite===!0&&(i.stencilWrite=this.stencilWrite),this.rotation!==void 0&&this.rotation!==0&&(i.rotation=this.rotation),this.polygonOffset===!0&&(i.polygonOffset=!0),this.polygonOffsetFactor!==0&&(i.polygonOffsetFactor=this.polygonOffsetFactor),this.polygonOffsetUnits!==0&&(i.polygonOffsetUnits=this.polygonOffsetUnits),this.linewidth!==void 0&&this.linewidth!==1&&(i.linewidth=this.linewidth),this.dashSize!==void 0&&(i.dashSize=this.dashSize),this.gapSize!==void 0&&(i.gapSize=this.gapSize),this.scale!==void 0&&(i.scale=this.scale),this.dithering===!0&&(i.dithering=!0),this.alphaTest>0&&(i.alphaTest=this.alphaTest),this.alphaHash===!0&&(i.alphaHash=!0),this.alphaToCoverage===!0&&(i.alphaToCoverage=!0),this.premultipliedAlpha===!0&&(i.premultipliedAlpha=!0),this.forceSinglePass===!0&&(i.forceSinglePass=!0),this.wireframe===!0&&(i.wireframe=!0),this.wireframeLinewidth>1&&(i.wireframeLinewidth=this.wireframeLinewidth),this.wireframeLinecap!=="round"&&(i.wireframeLinecap=this.wireframeLinecap),this.wireframeLinejoin!=="round"&&(i.wireframeLinejoin=this.wireframeLinejoin),this.flatShading===!0&&(i.flatShading=!0),this.visible===!1&&(i.visible=!1),this.toneMapped===!1&&(i.toneMapped=!1),this.fog===!1&&(i.fog=!1),Object.keys(this.userData).length>0&&(i.userData=this.userData);function r(a){const s=[];for(const o in a){const c=a[o];delete c.metadata,s.push(c)}return s}if(t){const a=r(e.textures),s=r(e.images);a.length>0&&(i.textures=a),s.length>0&&(i.images=s)}return i}clone(){return new this.constructor().copy(this)}copy(e){this.name=e.name,this.blending=e.blending,this.side=e.side,this.vertexColors=e.vertexColors,this.opacity=e.opacity,this.transparent=e.transparent,this.blendSrc=e.blendSrc,this.blendDst=e.blendDst,this.blendEquation=e.blendEquation,this.blendSrcAlpha=e.blendSrcAlpha,this.blendDstAlpha=e.blendDstAlpha,this.blendEquationAlpha=e.blendEquationAlpha,this.blendColor.copy(e.blendColor),this.blendAlpha=e.blendAlpha,this.depthFunc=e.depthFunc,this.depthTest=e.depthTest,this.depthWrite=e.depthWrite,this.stencilWriteMask=e.stencilWriteMask,this.stencilFunc=e.stencilFunc,this.stencilRef=e.stencilRef,this.stencilFuncMask=e.stencilFuncMask,this.stencilFail=e.stencilFail,this.stencilZFail=e.stencilZFail,this.stencilZPass=e.stencilZPass,this.stencilWrite=e.stencilWrite;const t=e.clippingPlanes;let i=null;if(t!==null){const r=t.length;i=new Array(r);for(let a=0;a!==r;++a)i[a]=t[a].clone()}return this.clippingPlanes=i,this.clipIntersection=e.clipIntersection,this.clipShadows=e.clipShadows,this.shadowSide=e.shadowSide,this.colorWrite=e.colorWrite,this.precision=e.precision,this.polygonOffset=e.polygonOffset,this.polygonOffsetFactor=e.polygonOffsetFactor,this.polygonOffsetUnits=e.polygonOffsetUnits,this.dithering=e.dithering,this.alphaTest=e.alphaTest,this.alphaHash=e.alphaHash,this.alphaToCoverage=e.alphaToCoverage,this.premultipliedAlpha=e.premultipliedAlpha,this.forceSinglePass=e.forceSinglePass,this.visible=e.visible,this.toneMapped=e.toneMapped,this.userData=JSON.parse(JSON.stringify(e.userData)),this}dispose(){this.dispatchEvent({type:"dispose"})}set needsUpdate(e){e===!0&&this.version++}onBuild(){console.warn("Material: onBuild() has been removed.")}}class Hr extends Ri{constructor(e){super(),this.isMeshBasicMaterial=!0,this.type="MeshBasicMaterial",this.color=new ve(16777215),this.map=null,this.lightMap=null,this.lightMapIntensity=1,this.aoMap=null,this.aoMapIntensity=1,this.specularMap=null,this.alphaMap=null,this.envMap=null,this.envMapRotation=new Jt,this.combine=sc,this.reflectivity=1,this.refractionRatio=.98,this.wireframe=!1,this.wireframeLinewidth=1,this.wireframeLinecap="round",this.wireframeLinejoin="round",this.fog=!0,this.setValues(e)}copy(e){return super.copy(e),this.color.copy(e.color),this.map=e.map,this.lightMap=e.lightMap,this.lightMapIntensity=e.lightMapIntensity,this.aoMap=e.aoMap,this.aoMapIntensity=e.aoMapIntensity,this.specularMap=e.specularMap,this.alphaMap=e.alphaMap,this.envMap=e.envMap,this.envMapRotation.copy(e.envMapRotation),this.combine=e.combine,this.reflectivity=e.reflectivity,this.refractionRatio=e.refractionRatio,this.wireframe=e.wireframe,this.wireframeLinewidth=e.wireframeLinewidth,this.wireframeLinecap=e.wireframeLinecap,this.wireframeLinejoin=e.wireframeLinejoin,this.fog=e.fog,this}}const dt=new k,ir=new Xe;let ru=0;class Zt{constructor(e,t,i=!1){if(Array.isArray(e))throw new TypeError("THREE.BufferAttribute: array should be a Typed Array.");this.isBufferAttribute=!0,Object.defineProperty(this,"id",{value:ru++}),this.name="",this.array=e,this.itemSize=t,this.count=e!==void 0?e.length/t:0,this.normalized=i,this.usage=Qs,this.updateRanges=[],this.gpuType=un,this.version=0}onUploadCallback(){}set needsUpdate(e){e===!0&&this.version++}setUsage(e){return this.usage=e,this}addUpdateRange(e,t){this.updateRanges.push({start:e,count:t})}clearUpdateRanges(){this.updateRanges.length=0}copy(e){return this.name=e.name,this.array=new e.array.constructor(e.array),this.itemSize=e.itemSize,this.count=e.count,this.normalized=e.normalized,this.usage=e.usage,this.gpuType=e.gpuType,this}copyAt(e,t,i){e*=this.itemSize,i*=t.itemSize;for(let r=0,a=this.itemSize;r<a;r++)this.array[e+r]=t.array[i+r];return this}copyArray(e){return this.array.set(e),this}applyMatrix3(e){if(this.itemSize===2)for(let t=0,i=this.count;t<i;t++)ir.fromBufferAttribute(this,t),ir.applyMatrix3(e),this.setXY(t,ir.x,ir.y);else if(this.itemSize===3)for(let t=0,i=this.count;t<i;t++)dt.fromBufferAttribute(this,t),dt.applyMatrix3(e),this.setXYZ(t,dt.x,dt.y,dt.z);return this}applyMatrix4(e){for(let t=0,i=this.count;t<i;t++)dt.fromBufferAttribute(this,t),dt.applyMatrix4(e),this.setXYZ(t,dt.x,dt.y,dt.z);return this}applyNormalMatrix(e){for(let t=0,i=this.count;t<i;t++)dt.fromBufferAttribute(this,t),dt.applyNormalMatrix(e),this.setXYZ(t,dt.x,dt.y,dt.z);return this}transformDirection(e){for(let t=0,i=this.count;t<i;t++)dt.fromBufferAttribute(this,t),dt.transformDirection(e),this.setXYZ(t,dt.x,dt.y,dt.z);return this}set(e,t=0){return this.array.set(e,t),this}getComponent(e,t){let i=this.array[e*this.itemSize+t];return this.normalized&&(i=Di(i,this.array)),i}setComponent(e,t,i){return this.normalized&&(i=At(i,this.array)),this.array[e*this.itemSize+t]=i,this}getX(e){let t=this.array[e*this.itemSize];return this.normalized&&(t=Di(t,this.array)),t}setX(e,t){return this.normalized&&(t=At(t,this.array)),this.array[e*this.itemSize]=t,this}getY(e){let t=this.array[e*this.itemSize+1];return this.normalized&&(t=Di(t,this.array)),t}setY(e,t){return this.normalized&&(t=At(t,this.array)),this.array[e*this.itemSize+1]=t,this}getZ(e){let t=this.array[e*this.itemSize+2];return this.normalized&&(t=Di(t,this.array)),t}setZ(e,t){return this.normalized&&(t=At(t,this.array)),this.array[e*this.itemSize+2]=t,this}getW(e){let t=this.array[e*this.itemSize+3];return this.normalized&&(t=Di(t,this.array)),t}setW(e,t){return this.normalized&&(t=At(t,this.array)),this.array[e*this.itemSize+3]=t,this}setXY(e,t,i){return e*=this.itemSize,this.normalized&&(t=At(t,this.array),i=At(i,this.array)),this.array[e+0]=t,this.array[e+1]=i,this}setXYZ(e,t,i,r){return e*=this.itemSize,this.normalized&&(t=At(t,this.array),i=At(i,this.array),r=At(r,this.array)),this.array[e+0]=t,this.array[e+1]=i,this.array[e+2]=r,this}setXYZW(e,t,i,r,a){return e*=this.itemSize,this.normalized&&(t=At(t,this.array),i=At(i,this.array),r=At(r,this.array),a=At(a,this.array)),this.array[e+0]=t,this.array[e+1]=i,this.array[e+2]=r,this.array[e+3]=a,this}onUpload(e){return this.onUploadCallback=e,this}clone(){return new this.constructor(this.array,this.itemSize).copy(this)}toJSON(){const e={itemSize:this.itemSize,type:this.array.constructor.name,array:Array.from(this.array),normalized:this.normalized};return this.name!==""&&(e.name=this.name),this.usage!==Qs&&(e.usage=this.usage),e}}class yc extends Zt{constructor(e,t,i){super(new Uint16Array(e),t,i)}}class bc extends Zt{constructor(e,t,i){super(new Uint32Array(e),t,i)}}class nt extends Zt{constructor(e,t,i){super(new Float32Array(e),t,i)}}let au=0;const Ft=new at,ha=new _t,oi=new k,Dt=new Gi,Ni=new Gi,mt=new k;class st extends wi{constructor(){super(),this.isBufferGeometry=!0,Object.defineProperty(this,"id",{value:au++}),this.uuid=Hi(),this.name="",this.type="BufferGeometry",this.index=null,this.indirect=null,this.attributes={},this.morphAttributes={},this.morphTargetsRelative=!1,this.groups=[],this.boundingBox=null,this.boundingSphere=null,this.drawRange={start:0,count:1/0},this.userData={}}getIndex(){return this.index}setIndex(e){return Array.isArray(e)?this.index=new(Mc(e)?bc:yc)(e,1):this.index=e,this}setIndirect(e){return this.indirect=e,this}getIndirect(){return this.indirect}getAttribute(e){return this.attributes[e]}setAttribute(e,t){return this.attributes[e]=t,this}deleteAttribute(e){return delete this.attributes[e],this}hasAttribute(e){return this.attributes[e]!==void 0}addGroup(e,t,i=0){this.groups.push({start:e,count:t,materialIndex:i})}clearGroups(){this.groups=[]}setDrawRange(e,t){this.drawRange.start=e,this.drawRange.count=t}applyMatrix4(e){const t=this.attributes.position;t!==void 0&&(t.applyMatrix4(e),t.needsUpdate=!0);const i=this.attributes.normal;if(i!==void 0){const a=new Be().getNormalMatrix(e);i.applyNormalMatrix(a),i.needsUpdate=!0}const r=this.attributes.tangent;return r!==void 0&&(r.transformDirection(e),r.needsUpdate=!0),this.boundingBox!==null&&this.computeBoundingBox(),this.boundingSphere!==null&&this.computeBoundingSphere(),this}applyQuaternion(e){return Ft.makeRotationFromQuaternion(e),this.applyMatrix4(Ft),this}rotateX(e){return Ft.makeRotationX(e),this.applyMatrix4(Ft),this}rotateY(e){return Ft.makeRotationY(e),this.applyMatrix4(Ft),this}rotateZ(e){return Ft.makeRotationZ(e),this.applyMatrix4(Ft),this}translate(e,t,i){return Ft.makeTranslation(e,t,i),this.applyMatrix4(Ft),this}scale(e,t,i){return Ft.makeScale(e,t,i),this.applyMatrix4(Ft),this}lookAt(e){return ha.lookAt(e),ha.updateMatrix(),this.applyMatrix4(ha.matrix),this}center(){return this.computeBoundingBox(),this.boundingBox.getCenter(oi).negate(),this.translate(oi.x,oi.y,oi.z),this}setFromPoints(e){const t=this.getAttribute("position");if(t===void 0){const i=[];for(let r=0,a=e.length;r<a;r++){const s=e[r];i.push(s.x,s.y,s.z||0)}this.setAttribute("position",new nt(i,3))}else{const i=Math.min(e.length,t.count);for(let r=0;r<i;r++){const a=e[r];t.setXYZ(r,a.x,a.y,a.z||0)}e.length>t.count&&console.warn("THREE.BufferGeometry: Buffer size too small for points data. Use .dispose() and create a new geometry."),t.needsUpdate=!0}return this}computeBoundingBox(){this.boundingBox===null&&(this.boundingBox=new Gi);const e=this.attributes.position,t=this.morphAttributes.position;if(e&&e.isGLBufferAttribute){console.error("THREE.BufferGeometry.computeBoundingBox(): GLBufferAttribute requires a manual bounding box.",this),this.boundingBox.set(new k(-1/0,-1/0,-1/0),new k(1/0,1/0,1/0));return}if(e!==void 0){if(this.boundingBox.setFromBufferAttribute(e),t)for(let i=0,r=t.length;i<r;i++){const a=t[i];Dt.setFromBufferAttribute(a),this.morphTargetsRelative?(mt.addVectors(this.boundingBox.min,Dt.min),this.boundingBox.expandByPoint(mt),mt.addVectors(this.boundingBox.max,Dt.max),this.boundingBox.expandByPoint(mt)):(this.boundingBox.expandByPoint(Dt.min),this.boundingBox.expandByPoint(Dt.max))}}else this.boundingBox.makeEmpty();(isNaN(this.boundingBox.min.x)||isNaN(this.boundingBox.min.y)||isNaN(this.boundingBox.min.z))&&console.error('THREE.BufferGeometry.computeBoundingBox(): Computed min/max have NaN values. The "position" attribute is likely to have NaN values.',this)}computeBoundingSphere(){this.boundingSphere===null&&(this.boundingSphere=new Br);const e=this.attributes.position,t=this.morphAttributes.position;if(e&&e.isGLBufferAttribute){console.error("THREE.BufferGeometry.computeBoundingSphere(): GLBufferAttribute requires a manual bounding sphere.",this),this.boundingSphere.set(new k,1/0);return}if(e){const i=this.boundingSphere.center;if(Dt.setFromBufferAttribute(e),t)for(let a=0,s=t.length;a<s;a++){const o=t[a];Ni.setFromBufferAttribute(o),this.morphTargetsRelative?(mt.addVectors(Dt.min,Ni.min),Dt.expandByPoint(mt),mt.addVectors(Dt.max,Ni.max),Dt.expandByPoint(mt)):(Dt.expandByPoint(Ni.min),Dt.expandByPoint(Ni.max))}Dt.getCenter(i);let r=0;for(let a=0,s=e.count;a<s;a++)mt.fromBufferAttribute(e,a),r=Math.max(r,i.distanceToSquared(mt));if(t)for(let a=0,s=t.length;a<s;a++){const o=t[a],c=this.morphTargetsRelative;for(let l=0,d=o.count;l<d;l++)mt.fromBufferAttribute(o,l),c&&(oi.fromBufferAttribute(e,l),mt.add(oi)),r=Math.max(r,i.distanceToSquared(mt))}this.boundingSphere.radius=Math.sqrt(r),isNaN(this.boundingSphere.radius)&&console.error('THREE.BufferGeometry.computeBoundingSphere(): Computed radius is NaN. The "position" attribute is likely to have NaN values.',this)}}computeTangents(){const e=this.index,t=this.attributes;if(e===null||t.position===void 0||t.normal===void 0||t.uv===void 0){console.error("THREE.BufferGeometry: .computeTangents() failed. Missing required attributes (index, position, normal or uv)");return}const i=t.position,r=t.normal,a=t.uv;this.hasAttribute("tangent")===!1&&this.setAttribute("tangent",new Zt(new Float32Array(4*i.count),4));const s=this.getAttribute("tangent"),o=[],c=[];for(let D=0;D<i.count;D++)o[D]=new k,c[D]=new k;const l=new k,d=new k,h=new k,f=new Xe,m=new Xe,g=new Xe,_=new k,p=new k;function u(D,x,v){l.fromBufferAttribute(i,D),d.fromBufferAttribute(i,x),h.fromBufferAttribute(i,v),f.fromBufferAttribute(a,D),m.fromBufferAttribute(a,x),g.fromBufferAttribute(a,v),d.sub(l),h.sub(l),m.sub(f),g.sub(f);const C=1/(m.x*g.y-g.x*m.y);isFinite(C)&&(_.copy(d).multiplyScalar(g.y).addScaledVector(h,-m.y).multiplyScalar(C),p.copy(h).multiplyScalar(m.x).addScaledVector(d,-g.x).multiplyScalar(C),o[D].add(_),o[x].add(_),o[v].add(_),c[D].add(p),c[x].add(p),c[v].add(p))}let w=this.groups;w.length===0&&(w=[{start:0,count:e.count}]);for(let D=0,x=w.length;D<x;++D){const v=w[D],C=v.start,F=v.count;for(let N=C,P=C+F;N<P;N+=3)u(e.getX(N+0),e.getX(N+1),e.getX(N+2))}const b=new k,S=new k,T=new k,y=new k;function A(D){T.fromBufferAttribute(r,D),y.copy(T);const x=o[D];b.copy(x),b.sub(T.multiplyScalar(T.dot(x))).normalize(),S.crossVectors(y,x);const C=S.dot(c[D])<0?-1:1;s.setXYZW(D,b.x,b.y,b.z,C)}for(let D=0,x=w.length;D<x;++D){const v=w[D],C=v.start,F=v.count;for(let N=C,P=C+F;N<P;N+=3)A(e.getX(N+0)),A(e.getX(N+1)),A(e.getX(N+2))}}computeVertexNormals(){const e=this.index,t=this.getAttribute("position");if(t!==void 0){let i=this.getAttribute("normal");if(i===void 0)i=new Zt(new Float32Array(t.count*3),3),this.setAttribute("normal",i);else for(let f=0,m=i.count;f<m;f++)i.setXYZ(f,0,0,0);const r=new k,a=new k,s=new k,o=new k,c=new k,l=new k,d=new k,h=new k;if(e)for(let f=0,m=e.count;f<m;f+=3){const g=e.getX(f+0),_=e.getX(f+1),p=e.getX(f+2);r.fromBufferAttribute(t,g),a.fromBufferAttribute(t,_),s.fromBufferAttribute(t,p),d.subVectors(s,a),h.subVectors(r,a),d.cross(h),o.fromBufferAttribute(i,g),c.fromBufferAttribute(i,_),l.fromBufferAttribute(i,p),o.add(d),c.add(d),l.add(d),i.setXYZ(g,o.x,o.y,o.z),i.setXYZ(_,c.x,c.y,c.z),i.setXYZ(p,l.x,l.y,l.z)}else for(let f=0,m=t.count;f<m;f+=3)r.fromBufferAttribute(t,f+0),a.fromBufferAttribute(t,f+1),s.fromBufferAttribute(t,f+2),d.subVectors(s,a),h.subVectors(r,a),d.cross(h),i.setXYZ(f+0,d.x,d.y,d.z),i.setXYZ(f+1,d.x,d.y,d.z),i.setXYZ(f+2,d.x,d.y,d.z);this.normalizeNormals(),i.needsUpdate=!0}}normalizeNormals(){const e=this.attributes.normal;for(let t=0,i=e.count;t<i;t++)mt.fromBufferAttribute(e,t),mt.normalize(),e.setXYZ(t,mt.x,mt.y,mt.z)}toNonIndexed(){function e(o,c){const l=o.array,d=o.itemSize,h=o.normalized,f=new l.constructor(c.length*d);let m=0,g=0;for(let _=0,p=c.length;_<p;_++){o.isInterleavedBufferAttribute?m=c[_]*o.data.stride+o.offset:m=c[_]*d;for(let u=0;u<d;u++)f[g++]=l[m++]}return new Zt(f,d,h)}if(this.index===null)return console.warn("THREE.BufferGeometry.toNonIndexed(): BufferGeometry is already non-indexed."),this;const t=new st,i=this.index.array,r=this.attributes;for(const o in r){const c=r[o],l=e(c,i);t.setAttribute(o,l)}const a=this.morphAttributes;for(const o in a){const c=[],l=a[o];for(let d=0,h=l.length;d<h;d++){const f=l[d],m=e(f,i);c.push(m)}t.morphAttributes[o]=c}t.morphTargetsRelative=this.morphTargetsRelative;const s=this.groups;for(let o=0,c=s.length;o<c;o++){const l=s[o];t.addGroup(l.start,l.count,l.materialIndex)}return t}toJSON(){const e={metadata:{version:4.6,type:"BufferGeometry",generator:"BufferGeometry.toJSON"}};if(e.uuid=this.uuid,e.type=this.type,this.name!==""&&(e.name=this.name),Object.keys(this.userData).length>0&&(e.userData=this.userData),this.parameters!==void 0){const c=this.parameters;for(const l in c)c[l]!==void 0&&(e[l]=c[l]);return e}e.data={attributes:{}};const t=this.index;t!==null&&(e.data.index={type:t.array.constructor.name,array:Array.prototype.slice.call(t.array)});const i=this.attributes;for(const c in i){const l=i[c];e.data.attributes[c]=l.toJSON(e.data)}const r={};let a=!1;for(const c in this.morphAttributes){const l=this.morphAttributes[c],d=[];for(let h=0,f=l.length;h<f;h++){const m=l[h];d.push(m.toJSON(e.data))}d.length>0&&(r[c]=d,a=!0)}a&&(e.data.morphAttributes=r,e.data.morphTargetsRelative=this.morphTargetsRelative);const s=this.groups;s.length>0&&(e.data.groups=JSON.parse(JSON.stringify(s)));const o=this.boundingSphere;return o!==null&&(e.data.boundingSphere={center:o.center.toArray(),radius:o.radius}),e}clone(){return new this.constructor().copy(this)}copy(e){this.index=null,this.attributes={},this.morphAttributes={},this.groups=[],this.boundingBox=null,this.boundingSphere=null;const t={};this.name=e.name;const i=e.index;i!==null&&this.setIndex(i.clone(t));const r=e.attributes;for(const l in r){const d=r[l];this.setAttribute(l,d.clone(t))}const a=e.morphAttributes;for(const l in a){const d=[],h=a[l];for(let f=0,m=h.length;f<m;f++)d.push(h[f].clone(t));this.morphAttributes[l]=d}this.morphTargetsRelative=e.morphTargetsRelative;const s=e.groups;for(let l=0,d=s.length;l<d;l++){const h=s[l];this.addGroup(h.start,h.count,h.materialIndex)}const o=e.boundingBox;o!==null&&(this.boundingBox=o.clone());const c=e.boundingSphere;return c!==null&&(this.boundingSphere=c.clone()),this.drawRange.start=e.drawRange.start,this.drawRange.count=e.drawRange.count,this.userData=e.userData,this}dispose(){this.dispatchEvent({type:"dispose"})}}const po=new at,Ln=new Ls,rr=new Br,mo=new k,ar=new k,sr=new k,or=new k,fa=new k,cr=new k,go=new k,lr=new k;class it extends _t{constructor(e=new st,t=new Hr){super(),this.isMesh=!0,this.type="Mesh",this.geometry=e,this.material=t,this.morphTargetDictionary=void 0,this.morphTargetInfluences=void 0,this.updateMorphTargets()}copy(e,t){return super.copy(e,t),e.morphTargetInfluences!==void 0&&(this.morphTargetInfluences=e.morphTargetInfluences.slice()),e.morphTargetDictionary!==void 0&&(this.morphTargetDictionary=Object.assign({},e.morphTargetDictionary)),this.material=Array.isArray(e.material)?e.material.slice():e.material,this.geometry=e.geometry,this}updateMorphTargets(){const t=this.geometry.morphAttributes,i=Object.keys(t);if(i.length>0){const r=t[i[0]];if(r!==void 0){this.morphTargetInfluences=[],this.morphTargetDictionary={};for(let a=0,s=r.length;a<s;a++){const o=r[a].name||String(a);this.morphTargetInfluences.push(0),this.morphTargetDictionary[o]=a}}}}getVertexPosition(e,t){const i=this.geometry,r=i.attributes.position,a=i.morphAttributes.position,s=i.morphTargetsRelative;t.fromBufferAttribute(r,e);const o=this.morphTargetInfluences;if(a&&o){cr.set(0,0,0);for(let c=0,l=a.length;c<l;c++){const d=o[c],h=a[c];d!==0&&(fa.fromBufferAttribute(h,e),s?cr.addScaledVector(fa,d):cr.addScaledVector(fa.sub(t),d))}t.add(cr)}return t}raycast(e,t){const i=this.geometry,r=this.material,a=this.matrixWorld;r!==void 0&&(i.boundingSphere===null&&i.computeBoundingSphere(),rr.copy(i.boundingSphere),rr.applyMatrix4(a),Ln.copy(e.ray).recast(e.near),!(rr.containsPoint(Ln.origin)===!1&&(Ln.intersectSphere(rr,mo)===null||Ln.origin.distanceToSquared(mo)>(e.far-e.near)**2))&&(po.copy(a).invert(),Ln.copy(e.ray).applyMatrix4(po),!(i.boundingBox!==null&&Ln.intersectsBox(i.boundingBox)===!1)&&this._computeIntersections(e,t,Ln)))}_computeIntersections(e,t,i){let r;const a=this.geometry,s=this.material,o=a.index,c=a.attributes.position,l=a.attributes.uv,d=a.attributes.uv1,h=a.attributes.normal,f=a.groups,m=a.drawRange;if(o!==null)if(Array.isArray(s))for(let g=0,_=f.length;g<_;g++){const p=f[g],u=s[p.materialIndex],w=Math.max(p.start,m.start),b=Math.min(o.count,Math.min(p.start+p.count,m.start+m.count));for(let S=w,T=b;S<T;S+=3){const y=o.getX(S),A=o.getX(S+1),D=o.getX(S+2);r=ur(this,u,e,i,l,d,h,y,A,D),r&&(r.faceIndex=Math.floor(S/3),r.face.materialIndex=p.materialIndex,t.push(r))}}else{const g=Math.max(0,m.start),_=Math.min(o.count,m.start+m.count);for(let p=g,u=_;p<u;p+=3){const w=o.getX(p),b=o.getX(p+1),S=o.getX(p+2);r=ur(this,s,e,i,l,d,h,w,b,S),r&&(r.faceIndex=Math.floor(p/3),t.push(r))}}else if(c!==void 0)if(Array.isArray(s))for(let g=0,_=f.length;g<_;g++){const p=f[g],u=s[p.materialIndex],w=Math.max(p.start,m.start),b=Math.min(c.count,Math.min(p.start+p.count,m.start+m.count));for(let S=w,T=b;S<T;S+=3){const y=S,A=S+1,D=S+2;r=ur(this,u,e,i,l,d,h,y,A,D),r&&(r.faceIndex=Math.floor(S/3),r.face.materialIndex=p.materialIndex,t.push(r))}}else{const g=Math.max(0,m.start),_=Math.min(c.count,m.start+m.count);for(let p=g,u=_;p<u;p+=3){const w=p,b=p+1,S=p+2;r=ur(this,s,e,i,l,d,h,w,b,S),r&&(r.faceIndex=Math.floor(p/3),t.push(r))}}}}function su(n,e,t,i,r,a,s,o){let c;if(e.side===Rt?c=i.intersectTriangle(s,a,r,!0,o):c=i.intersectTriangle(r,a,s,e.side===An,o),c===null)return null;lr.copy(o),lr.applyMatrix4(n.matrixWorld);const l=t.ray.origin.distanceTo(lr);return l<t.near||l>t.far?null:{distance:l,point:lr.clone(),object:n}}function ur(n,e,t,i,r,a,s,o,c,l){n.getVertexPosition(o,ar),n.getVertexPosition(c,sr),n.getVertexPosition(l,or);const d=su(n,e,t,i,ar,sr,or,go);if(d){const h=new k;Ot.getBarycoord(go,ar,sr,or,h),r&&(d.uv=Ot.getInterpolatedAttribute(r,o,c,l,h,new Xe)),a&&(d.uv1=Ot.getInterpolatedAttribute(a,o,c,l,h,new Xe)),s&&(d.normal=Ot.getInterpolatedAttribute(s,o,c,l,h,new k),d.normal.dot(i.direction)>0&&d.normal.multiplyScalar(-1));const f={a:o,b:c,c:l,normal:new k,materialIndex:0};Ot.getNormal(ar,sr,or,f.normal),d.face=f,d.barycoord=h}return d}class hn extends st{constructor(e=1,t=1,i=1,r=1,a=1,s=1){super(),this.type="BoxGeometry",this.parameters={width:e,height:t,depth:i,widthSegments:r,heightSegments:a,depthSegments:s};const o=this;r=Math.floor(r),a=Math.floor(a),s=Math.floor(s);const c=[],l=[],d=[],h=[];let f=0,m=0;g("z","y","x",-1,-1,i,t,e,s,a,0),g("z","y","x",1,-1,i,t,-e,s,a,1),g("x","z","y",1,1,e,i,t,r,s,2),g("x","z","y",1,-1,e,i,-t,r,s,3),g("x","y","z",1,-1,e,t,i,r,a,4),g("x","y","z",-1,-1,e,t,-i,r,a,5),this.setIndex(c),this.setAttribute("position",new nt(l,3)),this.setAttribute("normal",new nt(d,3)),this.setAttribute("uv",new nt(h,2));function g(_,p,u,w,b,S,T,y,A,D,x){const v=S/A,C=T/D,F=S/2,N=T/2,P=y/2,U=A+1,z=D+1;let H=0,I=0;const G=new k;for(let q=0;q<z;q++){const oe=q*C-N;for(let le=0;le<U;le++){const Re=le*v-F;G[_]=Re*w,G[p]=oe*b,G[u]=P,l.push(G.x,G.y,G.z),G[_]=0,G[p]=0,G[u]=y>0?1:-1,d.push(G.x,G.y,G.z),h.push(le/A),h.push(1-q/D),H+=1}}for(let q=0;q<D;q++)for(let oe=0;oe<A;oe++){const le=f+oe+U*q,Re=f+oe+U*(q+1),Y=f+(oe+1)+U*(q+1),te=f+(oe+1)+U*q;c.push(le,Re,te),c.push(Re,Y,te),I+=6}o.addGroup(m,I,x),m+=I,f+=H}}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}static fromJSON(e){return new hn(e.width,e.height,e.depth,e.widthSegments,e.heightSegments,e.depthSegments)}}function Ai(n){const e={};for(const t in n){e[t]={};for(const i in n[t]){const r=n[t][i];r&&(r.isColor||r.isMatrix3||r.isMatrix4||r.isVector2||r.isVector3||r.isVector4||r.isTexture||r.isQuaternion)?r.isRenderTargetTexture?(console.warn("UniformsUtils: Textures of render targets cannot be cloned via cloneUniforms() or mergeUniforms()."),e[t][i]=null):e[t][i]=r.clone():Array.isArray(r)?e[t][i]=r.slice():e[t][i]=r}}return e}function yt(n){const e={};for(let t=0;t<n.length;t++){const i=Ai(n[t]);for(const r in i)e[r]=i[r]}return e}function ou(n){const e=[];for(let t=0;t<n.length;t++)e.push(n[t].clone());return e}function Tc(n){const e=n.getRenderTarget();return e===null?n.outputColorSpace:e.isXRRenderTarget===!0?e.texture.colorSpace:Ke.workingColorSpace}const cu={clone:Ai,merge:yt};var lu=`void main() {
	gl_Position = projectionMatrix * modelViewMatrix * vec4( position, 1.0 );
}`,uu=`void main() {
	gl_FragColor = vec4( 1.0, 0.0, 0.0, 1.0 );
}`;class wn extends Ri{constructor(e){super(),this.isShaderMaterial=!0,this.type="ShaderMaterial",this.defines={},this.uniforms={},this.uniformsGroups=[],this.vertexShader=lu,this.fragmentShader=uu,this.linewidth=1,this.wireframe=!1,this.wireframeLinewidth=1,this.fog=!1,this.lights=!1,this.clipping=!1,this.forceSinglePass=!0,this.extensions={clipCullDistance:!1,multiDraw:!1},this.defaultAttributeValues={color:[1,1,1],uv:[0,0],uv1:[0,0]},this.index0AttributeName=void 0,this.uniformsNeedUpdate=!1,this.glslVersion=null,e!==void 0&&this.setValues(e)}copy(e){return super.copy(e),this.fragmentShader=e.fragmentShader,this.vertexShader=e.vertexShader,this.uniforms=Ai(e.uniforms),this.uniformsGroups=ou(e.uniformsGroups),this.defines=Object.assign({},e.defines),this.wireframe=e.wireframe,this.wireframeLinewidth=e.wireframeLinewidth,this.fog=e.fog,this.lights=e.lights,this.clipping=e.clipping,this.extensions=Object.assign({},e.extensions),this.glslVersion=e.glslVersion,this}toJSON(e){const t=super.toJSON(e);t.glslVersion=this.glslVersion,t.uniforms={};for(const r in this.uniforms){const s=this.uniforms[r].value;s&&s.isTexture?t.uniforms[r]={type:"t",value:s.toJSON(e).uuid}:s&&s.isColor?t.uniforms[r]={type:"c",value:s.getHex()}:s&&s.isVector2?t.uniforms[r]={type:"v2",value:s.toArray()}:s&&s.isVector3?t.uniforms[r]={type:"v3",value:s.toArray()}:s&&s.isVector4?t.uniforms[r]={type:"v4",value:s.toArray()}:s&&s.isMatrix3?t.uniforms[r]={type:"m3",value:s.toArray()}:s&&s.isMatrix4?t.uniforms[r]={type:"m4",value:s.toArray()}:t.uniforms[r]={value:s}}Object.keys(this.defines).length>0&&(t.defines=this.defines),t.vertexShader=this.vertexShader,t.fragmentShader=this.fragmentShader,t.lights=this.lights,t.clipping=this.clipping;const i={};for(const r in this.extensions)this.extensions[r]===!0&&(i[r]=!0);return Object.keys(i).length>0&&(t.extensions=i),t}}class Ac extends _t{constructor(){super(),this.isCamera=!0,this.type="Camera",this.matrixWorldInverse=new at,this.projectionMatrix=new at,this.projectionMatrixInverse=new at,this.coordinateSystem=dn}copy(e,t){return super.copy(e,t),this.matrixWorldInverse.copy(e.matrixWorldInverse),this.projectionMatrix.copy(e.projectionMatrix),this.projectionMatrixInverse.copy(e.projectionMatrixInverse),this.coordinateSystem=e.coordinateSystem,this}getWorldDirection(e){return super.getWorldDirection(e).negate()}updateMatrixWorld(e){super.updateMatrixWorld(e),this.matrixWorldInverse.copy(this.matrixWorld).invert()}updateWorldMatrix(e,t){super.updateWorldMatrix(e,t),this.matrixWorldInverse.copy(this.matrixWorld).invert()}clone(){return new this.constructor().copy(this)}}const Mn=new k,_o=new Xe,vo=new Xe;class zt extends Ac{constructor(e=50,t=1,i=.1,r=2e3){super(),this.isPerspectiveCamera=!0,this.type="PerspectiveCamera",this.fov=e,this.zoom=1,this.near=i,this.far=r,this.focus=10,this.aspect=t,this.view=null,this.filmGauge=35,this.filmOffset=0,this.updateProjectionMatrix()}copy(e,t){return super.copy(e,t),this.fov=e.fov,this.zoom=e.zoom,this.near=e.near,this.far=e.far,this.focus=e.focus,this.aspect=e.aspect,this.view=e.view===null?null:Object.assign({},e.view),this.filmGauge=e.filmGauge,this.filmOffset=e.filmOffset,this}setFocalLength(e){const t=.5*this.getFilmHeight()/e;this.fov=ps*2*Math.atan(t),this.updateProjectionMatrix()}getFocalLength(){const e=Math.tan(Ar*.5*this.fov);return .5*this.getFilmHeight()/e}getEffectiveFOV(){return ps*2*Math.atan(Math.tan(Ar*.5*this.fov)/this.zoom)}getFilmWidth(){return this.filmGauge*Math.min(this.aspect,1)}getFilmHeight(){return this.filmGauge/Math.max(this.aspect,1)}getViewBounds(e,t,i){Mn.set(-1,-1,.5).applyMatrix4(this.projectionMatrixInverse),t.set(Mn.x,Mn.y).multiplyScalar(-e/Mn.z),Mn.set(1,1,.5).applyMatrix4(this.projectionMatrixInverse),i.set(Mn.x,Mn.y).multiplyScalar(-e/Mn.z)}getViewSize(e,t){return this.getViewBounds(e,_o,vo),t.subVectors(vo,_o)}setViewOffset(e,t,i,r,a,s){this.aspect=e/t,this.view===null&&(this.view={enabled:!0,fullWidth:1,fullHeight:1,offsetX:0,offsetY:0,width:1,height:1}),this.view.enabled=!0,this.view.fullWidth=e,this.view.fullHeight=t,this.view.offsetX=i,this.view.offsetY=r,this.view.width=a,this.view.height=s,this.updateProjectionMatrix()}clearViewOffset(){this.view!==null&&(this.view.enabled=!1),this.updateProjectionMatrix()}updateProjectionMatrix(){const e=this.near;let t=e*Math.tan(Ar*.5*this.fov)/this.zoom,i=2*t,r=this.aspect*i,a=-.5*r;const s=this.view;if(this.view!==null&&this.view.enabled){const c=s.fullWidth,l=s.fullHeight;a+=s.offsetX*r/c,t-=s.offsetY*i/l,r*=s.width/c,i*=s.height/l}const o=this.filmOffset;o!==0&&(a+=e*o/this.getFilmWidth()),this.projectionMatrix.makePerspective(a,a+r,t,t-i,e,this.far,this.coordinateSystem),this.projectionMatrixInverse.copy(this.projectionMatrix).invert()}toJSON(e){const t=super.toJSON(e);return t.object.fov=this.fov,t.object.zoom=this.zoom,t.object.near=this.near,t.object.far=this.far,t.object.focus=this.focus,t.object.aspect=this.aspect,this.view!==null&&(t.object.view=Object.assign({},this.view)),t.object.filmGauge=this.filmGauge,t.object.filmOffset=this.filmOffset,t}}const ci=-90,li=1;class du extends _t{constructor(e,t,i){super(),this.type="CubeCamera",this.renderTarget=i,this.coordinateSystem=null,this.activeMipmapLevel=0;const r=new zt(ci,li,e,t);r.layers=this.layers,this.add(r);const a=new zt(ci,li,e,t);a.layers=this.layers,this.add(a);const s=new zt(ci,li,e,t);s.layers=this.layers,this.add(s);const o=new zt(ci,li,e,t);o.layers=this.layers,this.add(o);const c=new zt(ci,li,e,t);c.layers=this.layers,this.add(c);const l=new zt(ci,li,e,t);l.layers=this.layers,this.add(l)}updateCoordinateSystem(){const e=this.coordinateSystem,t=this.children.concat(),[i,r,a,s,o,c]=t;for(const l of t)this.remove(l);if(e===dn)i.up.set(0,1,0),i.lookAt(1,0,0),r.up.set(0,1,0),r.lookAt(-1,0,0),a.up.set(0,0,-1),a.lookAt(0,1,0),s.up.set(0,0,1),s.lookAt(0,-1,0),o.up.set(0,1,0),o.lookAt(0,0,1),c.up.set(0,1,0),c.lookAt(0,0,-1);else if(e===Dr)i.up.set(0,-1,0),i.lookAt(-1,0,0),r.up.set(0,-1,0),r.lookAt(1,0,0),a.up.set(0,0,1),a.lookAt(0,1,0),s.up.set(0,0,-1),s.lookAt(0,-1,0),o.up.set(0,-1,0),o.lookAt(0,0,1),c.up.set(0,-1,0),c.lookAt(0,0,-1);else throw new Error("THREE.CubeCamera.updateCoordinateSystem(): Invalid coordinate system: "+e);for(const l of t)this.add(l),l.updateMatrixWorld()}update(e,t){this.parent===null&&this.updateMatrixWorld();const{renderTarget:i,activeMipmapLevel:r}=this;this.coordinateSystem!==e.coordinateSystem&&(this.coordinateSystem=e.coordinateSystem,this.updateCoordinateSystem());const[a,s,o,c,l,d]=this.children,h=e.getRenderTarget(),f=e.getActiveCubeFace(),m=e.getActiveMipmapLevel(),g=e.xr.enabled;e.xr.enabled=!1;const _=i.texture.generateMipmaps;i.texture.generateMipmaps=!1,e.setRenderTarget(i,0,r),e.render(t,a),e.setRenderTarget(i,1,r),e.render(t,s),e.setRenderTarget(i,2,r),e.render(t,o),e.setRenderTarget(i,3,r),e.render(t,c),e.setRenderTarget(i,4,r),e.render(t,l),i.texture.generateMipmaps=_,e.setRenderTarget(i,5,r),e.render(t,d),e.setRenderTarget(h,f,m),e.xr.enabled=g,i.texture.needsPMREMUpdate=!0}}class wc extends bt{constructor(e,t,i,r,a,s,o,c,l,d){e=e!==void 0?e:[],t=t!==void 0?t:Si,super(e,t,i,r,a,s,o,c,l,d),this.isCubeTexture=!0,this.flipY=!1}get images(){return this.image}set images(e){this.image=e}}class hu extends qn{constructor(e=1,t={}){super(e,e,t),this.isWebGLCubeRenderTarget=!0;const i={width:e,height:e,depth:1},r=[i,i,i,i,i,i];this.texture=new wc(r,t.mapping,t.wrapS,t.wrapT,t.magFilter,t.minFilter,t.format,t.type,t.anisotropy,t.colorSpace),this.texture.isRenderTargetTexture=!0,this.texture.generateMipmaps=t.generateMipmaps!==void 0?t.generateMipmaps:!1,this.texture.minFilter=t.minFilter!==void 0?t.minFilter:Kt}fromEquirectangularTexture(e,t){this.texture.type=t.type,this.texture.colorSpace=t.colorSpace,this.texture.generateMipmaps=t.generateMipmaps,this.texture.minFilter=t.minFilter,this.texture.magFilter=t.magFilter;const i={uniforms:{tEquirect:{value:null}},vertexShader:`

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
			`},r=new hn(5,5,5),a=new wn({name:"CubemapFromEquirect",uniforms:Ai(i.uniforms),vertexShader:i.vertexShader,fragmentShader:i.fragmentShader,side:Rt,blending:bn});a.uniforms.tEquirect.value=t;const s=new it(r,a),o=t.minFilter;return t.minFilter===jn&&(t.minFilter=Kt),new du(1,10,this).update(e,s),t.minFilter=o,s.geometry.dispose(),s.material.dispose(),this}clear(e,t,i,r){const a=e.getRenderTarget();for(let s=0;s<6;s++)e.setRenderTarget(this,s),e.clear(t,i,r);e.setRenderTarget(a)}}class ht extends _t{constructor(){super(),this.isGroup=!0,this.type="Group"}}const fu={type:"move"};class pa{constructor(){this._targetRay=null,this._grip=null,this._hand=null}getHandSpace(){return this._hand===null&&(this._hand=new ht,this._hand.matrixAutoUpdate=!1,this._hand.visible=!1,this._hand.joints={},this._hand.inputState={pinching:!1}),this._hand}getTargetRaySpace(){return this._targetRay===null&&(this._targetRay=new ht,this._targetRay.matrixAutoUpdate=!1,this._targetRay.visible=!1,this._targetRay.hasLinearVelocity=!1,this._targetRay.linearVelocity=new k,this._targetRay.hasAngularVelocity=!1,this._targetRay.angularVelocity=new k),this._targetRay}getGripSpace(){return this._grip===null&&(this._grip=new ht,this._grip.matrixAutoUpdate=!1,this._grip.visible=!1,this._grip.hasLinearVelocity=!1,this._grip.linearVelocity=new k,this._grip.hasAngularVelocity=!1,this._grip.angularVelocity=new k),this._grip}dispatchEvent(e){return this._targetRay!==null&&this._targetRay.dispatchEvent(e),this._grip!==null&&this._grip.dispatchEvent(e),this._hand!==null&&this._hand.dispatchEvent(e),this}connect(e){if(e&&e.hand){const t=this._hand;if(t)for(const i of e.hand.values())this._getHandJoint(t,i)}return this.dispatchEvent({type:"connected",data:e}),this}disconnect(e){return this.dispatchEvent({type:"disconnected",data:e}),this._targetRay!==null&&(this._targetRay.visible=!1),this._grip!==null&&(this._grip.visible=!1),this._hand!==null&&(this._hand.visible=!1),this}update(e,t,i){let r=null,a=null,s=null;const o=this._targetRay,c=this._grip,l=this._hand;if(e&&t.session.visibilityState!=="visible-blurred"){if(l&&e.hand){s=!0;for(const _ of e.hand.values()){const p=t.getJointPose(_,i),u=this._getHandJoint(l,_);p!==null&&(u.matrix.fromArray(p.transform.matrix),u.matrix.decompose(u.position,u.rotation,u.scale),u.matrixWorldNeedsUpdate=!0,u.jointRadius=p.radius),u.visible=p!==null}const d=l.joints["index-finger-tip"],h=l.joints["thumb-tip"],f=d.position.distanceTo(h.position),m=.02,g=.005;l.inputState.pinching&&f>m+g?(l.inputState.pinching=!1,this.dispatchEvent({type:"pinchend",handedness:e.handedness,target:this})):!l.inputState.pinching&&f<=m-g&&(l.inputState.pinching=!0,this.dispatchEvent({type:"pinchstart",handedness:e.handedness,target:this}))}else c!==null&&e.gripSpace&&(a=t.getPose(e.gripSpace,i),a!==null&&(c.matrix.fromArray(a.transform.matrix),c.matrix.decompose(c.position,c.rotation,c.scale),c.matrixWorldNeedsUpdate=!0,a.linearVelocity?(c.hasLinearVelocity=!0,c.linearVelocity.copy(a.linearVelocity)):c.hasLinearVelocity=!1,a.angularVelocity?(c.hasAngularVelocity=!0,c.angularVelocity.copy(a.angularVelocity)):c.hasAngularVelocity=!1));o!==null&&(r=t.getPose(e.targetRaySpace,i),r===null&&a!==null&&(r=a),r!==null&&(o.matrix.fromArray(r.transform.matrix),o.matrix.decompose(o.position,o.rotation,o.scale),o.matrixWorldNeedsUpdate=!0,r.linearVelocity?(o.hasLinearVelocity=!0,o.linearVelocity.copy(r.linearVelocity)):o.hasLinearVelocity=!1,r.angularVelocity?(o.hasAngularVelocity=!0,o.angularVelocity.copy(r.angularVelocity)):o.hasAngularVelocity=!1,this.dispatchEvent(fu)))}return o!==null&&(o.visible=r!==null),c!==null&&(c.visible=a!==null),l!==null&&(l.visible=s!==null),this}_getHandJoint(e,t){if(e.joints[t.jointName]===void 0){const i=new ht;i.matrixAutoUpdate=!1,i.visible=!1,e.joints[t.jointName]=i,e.add(i)}return e.joints[t.jointName]}}class pu extends _t{constructor(){super(),this.isScene=!0,this.type="Scene",this.background=null,this.environment=null,this.fog=null,this.backgroundBlurriness=0,this.backgroundIntensity=1,this.backgroundRotation=new Jt,this.environmentIntensity=1,this.environmentRotation=new Jt,this.overrideMaterial=null,typeof __THREE_DEVTOOLS__<"u"&&__THREE_DEVTOOLS__.dispatchEvent(new CustomEvent("observe",{detail:this}))}copy(e,t){return super.copy(e,t),e.background!==null&&(this.background=e.background.clone()),e.environment!==null&&(this.environment=e.environment.clone()),e.fog!==null&&(this.fog=e.fog.clone()),this.backgroundBlurriness=e.backgroundBlurriness,this.backgroundIntensity=e.backgroundIntensity,this.backgroundRotation.copy(e.backgroundRotation),this.environmentIntensity=e.environmentIntensity,this.environmentRotation.copy(e.environmentRotation),e.overrideMaterial!==null&&(this.overrideMaterial=e.overrideMaterial.clone()),this.matrixAutoUpdate=e.matrixAutoUpdate,this}toJSON(e){const t=super.toJSON(e);return this.fog!==null&&(t.object.fog=this.fog.toJSON()),this.backgroundBlurriness>0&&(t.object.backgroundBlurriness=this.backgroundBlurriness),this.backgroundIntensity!==1&&(t.object.backgroundIntensity=this.backgroundIntensity),t.object.backgroundRotation=this.backgroundRotation.toArray(),this.environmentIntensity!==1&&(t.object.environmentIntensity=this.environmentIntensity),t.object.environmentRotation=this.environmentRotation.toArray(),t}}const ma=new k,mu=new k,gu=new Be;class zn{constructor(e=new k(1,0,0),t=0){this.isPlane=!0,this.normal=e,this.constant=t}set(e,t){return this.normal.copy(e),this.constant=t,this}setComponents(e,t,i,r){return this.normal.set(e,t,i),this.constant=r,this}setFromNormalAndCoplanarPoint(e,t){return this.normal.copy(e),this.constant=-t.dot(this.normal),this}setFromCoplanarPoints(e,t,i){const r=ma.subVectors(i,t).cross(mu.subVectors(e,t)).normalize();return this.setFromNormalAndCoplanarPoint(r,e),this}copy(e){return this.normal.copy(e.normal),this.constant=e.constant,this}normalize(){const e=1/this.normal.length();return this.normal.multiplyScalar(e),this.constant*=e,this}negate(){return this.constant*=-1,this.normal.negate(),this}distanceToPoint(e){return this.normal.dot(e)+this.constant}distanceToSphere(e){return this.distanceToPoint(e.center)-e.radius}projectPoint(e,t){return t.copy(e).addScaledVector(this.normal,-this.distanceToPoint(e))}intersectLine(e,t){const i=e.delta(ma),r=this.normal.dot(i);if(r===0)return this.distanceToPoint(e.start)===0?t.copy(e.start):null;const a=-(e.start.dot(this.normal)+this.constant)/r;return a<0||a>1?null:t.copy(e.start).addScaledVector(i,a)}intersectsLine(e){const t=this.distanceToPoint(e.start),i=this.distanceToPoint(e.end);return t<0&&i>0||i<0&&t>0}intersectsBox(e){return e.intersectsPlane(this)}intersectsSphere(e){return e.intersectsPlane(this)}coplanarPoint(e){return e.copy(this.normal).multiplyScalar(-this.constant)}applyMatrix4(e,t){const i=t||gu.getNormalMatrix(e),r=this.coplanarPoint(ma).applyMatrix4(e),a=this.normal.applyMatrix3(i).normalize();return this.constant=-r.dot(a),this}translate(e){return this.constant-=e.dot(this.normal),this}equals(e){return e.normal.equals(this.normal)&&e.constant===this.constant}clone(){return new this.constructor().copy(this)}}const In=new Br,dr=new k;class Us{constructor(e=new zn,t=new zn,i=new zn,r=new zn,a=new zn,s=new zn){this.planes=[e,t,i,r,a,s]}set(e,t,i,r,a,s){const o=this.planes;return o[0].copy(e),o[1].copy(t),o[2].copy(i),o[3].copy(r),o[4].copy(a),o[5].copy(s),this}copy(e){const t=this.planes;for(let i=0;i<6;i++)t[i].copy(e.planes[i]);return this}setFromProjectionMatrix(e,t=dn){const i=this.planes,r=e.elements,a=r[0],s=r[1],o=r[2],c=r[3],l=r[4],d=r[5],h=r[6],f=r[7],m=r[8],g=r[9],_=r[10],p=r[11],u=r[12],w=r[13],b=r[14],S=r[15];if(i[0].setComponents(c-a,f-l,p-m,S-u).normalize(),i[1].setComponents(c+a,f+l,p+m,S+u).normalize(),i[2].setComponents(c+s,f+d,p+g,S+w).normalize(),i[3].setComponents(c-s,f-d,p-g,S-w).normalize(),i[4].setComponents(c-o,f-h,p-_,S-b).normalize(),t===dn)i[5].setComponents(c+o,f+h,p+_,S+b).normalize();else if(t===Dr)i[5].setComponents(o,h,_,b).normalize();else throw new Error("THREE.Frustum.setFromProjectionMatrix(): Invalid coordinate system: "+t);return this}intersectsObject(e){if(e.boundingSphere!==void 0)e.boundingSphere===null&&e.computeBoundingSphere(),In.copy(e.boundingSphere).applyMatrix4(e.matrixWorld);else{const t=e.geometry;t.boundingSphere===null&&t.computeBoundingSphere(),In.copy(t.boundingSphere).applyMatrix4(e.matrixWorld)}return this.intersectsSphere(In)}intersectsSprite(e){return In.center.set(0,0,0),In.radius=.7071067811865476,In.applyMatrix4(e.matrixWorld),this.intersectsSphere(In)}intersectsSphere(e){const t=this.planes,i=e.center,r=-e.radius;for(let a=0;a<6;a++)if(t[a].distanceToPoint(i)<r)return!1;return!0}intersectsBox(e){const t=this.planes;for(let i=0;i<6;i++){const r=t[i];if(dr.x=r.normal.x>0?e.max.x:e.min.x,dr.y=r.normal.y>0?e.max.y:e.min.y,dr.z=r.normal.z>0?e.max.z:e.min.z,r.distanceToPoint(dr)<0)return!1}return!0}containsPoint(e){const t=this.planes;for(let i=0;i<6;i++)if(t[i].distanceToPoint(e)<0)return!1;return!0}clone(){return new this.constructor().copy(this)}}class It extends Ri{constructor(e){super(),this.isLineBasicMaterial=!0,this.type="LineBasicMaterial",this.color=new ve(16777215),this.map=null,this.linewidth=1,this.linecap="round",this.linejoin="round",this.fog=!0,this.setValues(e)}copy(e){return super.copy(e),this.color.copy(e.color),this.map=e.map,this.linewidth=e.linewidth,this.linecap=e.linecap,this.linejoin=e.linejoin,this.fog=e.fog,this}}const Ir=new k,Ur=new k,xo=new at,Fi=new Ls,hr=new Br,ga=new k,Mo=new k;class wr extends _t{constructor(e=new st,t=new It){super(),this.isLine=!0,this.type="Line",this.geometry=e,this.material=t,this.morphTargetDictionary=void 0,this.morphTargetInfluences=void 0,this.updateMorphTargets()}copy(e,t){return super.copy(e,t),this.material=Array.isArray(e.material)?e.material.slice():e.material,this.geometry=e.geometry,this}computeLineDistances(){const e=this.geometry;if(e.index===null){const t=e.attributes.position,i=[0];for(let r=1,a=t.count;r<a;r++)Ir.fromBufferAttribute(t,r-1),Ur.fromBufferAttribute(t,r),i[r]=i[r-1],i[r]+=Ir.distanceTo(Ur);e.setAttribute("lineDistance",new nt(i,1))}else console.warn("THREE.Line.computeLineDistances(): Computation only possible with non-indexed BufferGeometry.");return this}raycast(e,t){const i=this.geometry,r=this.matrixWorld,a=e.params.Line.threshold,s=i.drawRange;if(i.boundingSphere===null&&i.computeBoundingSphere(),hr.copy(i.boundingSphere),hr.applyMatrix4(r),hr.radius+=a,e.ray.intersectsSphere(hr)===!1)return;xo.copy(r).invert(),Fi.copy(e.ray).applyMatrix4(xo);const o=a/((this.scale.x+this.scale.y+this.scale.z)/3),c=o*o,l=this.isLineSegments?2:1,d=i.index,f=i.attributes.position;if(d!==null){const m=Math.max(0,s.start),g=Math.min(d.count,s.start+s.count);for(let _=m,p=g-1;_<p;_+=l){const u=d.getX(_),w=d.getX(_+1),b=fr(this,e,Fi,c,u,w,_);b&&t.push(b)}if(this.isLineLoop){const _=d.getX(g-1),p=d.getX(m),u=fr(this,e,Fi,c,_,p,g-1);u&&t.push(u)}}else{const m=Math.max(0,s.start),g=Math.min(f.count,s.start+s.count);for(let _=m,p=g-1;_<p;_+=l){const u=fr(this,e,Fi,c,_,_+1,_);u&&t.push(u)}if(this.isLineLoop){const _=fr(this,e,Fi,c,g-1,m,g-1);_&&t.push(_)}}}updateMorphTargets(){const t=this.geometry.morphAttributes,i=Object.keys(t);if(i.length>0){const r=t[i[0]];if(r!==void 0){this.morphTargetInfluences=[],this.morphTargetDictionary={};for(let a=0,s=r.length;a<s;a++){const o=r[a].name||String(a);this.morphTargetInfluences.push(0),this.morphTargetDictionary[o]=a}}}}}function fr(n,e,t,i,r,a,s){const o=n.geometry.attributes.position;if(Ir.fromBufferAttribute(o,r),Ur.fromBufferAttribute(o,a),t.distanceSqToSegment(Ir,Ur,ga,Mo)>i)return;ga.applyMatrix4(n.matrixWorld);const l=e.ray.origin.distanceTo(ga);if(!(l<e.near||l>e.far))return{distance:l,point:Mo.clone().applyMatrix4(n.matrixWorld),index:s,face:null,faceIndex:null,barycoord:null,object:n}}const So=new k,Eo=new k;class Bt extends wr{constructor(e,t){super(e,t),this.isLineSegments=!0,this.type="LineSegments"}computeLineDistances(){const e=this.geometry;if(e.index===null){const t=e.attributes.position,i=[];for(let r=0,a=t.count;r<a;r+=2)So.fromBufferAttribute(t,r),Eo.fromBufferAttribute(t,r+1),i[r]=r===0?0:i[r-1],i[r+1]=i[r]+So.distanceTo(Eo);e.setAttribute("lineDistance",new nt(i,1))}else console.warn("THREE.LineSegments.computeLineDistances(): Computation only possible with non-indexed BufferGeometry.");return this}}class Rc extends bt{constructor(e,t,i,r,a,s,o,c,l,d=_i){if(d!==_i&&d!==bi)throw new Error("DepthTexture format must be either THREE.DepthFormat or THREE.DepthStencilFormat");i===void 0&&d===_i&&(i=Yn),i===void 0&&d===bi&&(i=yi),super(null,r,a,s,o,c,d,i,l),this.isDepthTexture=!0,this.image={width:e,height:t},this.magFilter=o!==void 0?o:qt,this.minFilter=c!==void 0?c:qt,this.flipY=!1,this.generateMipmaps=!1,this.compareFunction=null}copy(e){return super.copy(e),this.source=new Ds(Object.assign({},e.image)),this.compareFunction=e.compareFunction,this}toJSON(e){const t=super.toJSON(e);return this.compareFunction!==null&&(t.compareFunction=this.compareFunction),t}}class ji extends st{constructor(e=1,t=1,i=1,r=32,a=1,s=!1,o=0,c=Math.PI*2){super(),this.type="CylinderGeometry",this.parameters={radiusTop:e,radiusBottom:t,height:i,radialSegments:r,heightSegments:a,openEnded:s,thetaStart:o,thetaLength:c};const l=this;r=Math.floor(r),a=Math.floor(a);const d=[],h=[],f=[],m=[];let g=0;const _=[],p=i/2;let u=0;w(),s===!1&&(e>0&&b(!0),t>0&&b(!1)),this.setIndex(d),this.setAttribute("position",new nt(h,3)),this.setAttribute("normal",new nt(f,3)),this.setAttribute("uv",new nt(m,2));function w(){const S=new k,T=new k;let y=0;const A=(t-e)/i;for(let D=0;D<=a;D++){const x=[],v=D/a,C=v*(t-e)+e;for(let F=0;F<=r;F++){const N=F/r,P=N*c+o,U=Math.sin(P),z=Math.cos(P);T.x=C*U,T.y=-v*i+p,T.z=C*z,h.push(T.x,T.y,T.z),S.set(U,A,z).normalize(),f.push(S.x,S.y,S.z),m.push(N,1-v),x.push(g++)}_.push(x)}for(let D=0;D<r;D++)for(let x=0;x<a;x++){const v=_[x][D],C=_[x+1][D],F=_[x+1][D+1],N=_[x][D+1];(e>0||x!==0)&&(d.push(v,C,N),y+=3),(t>0||x!==a-1)&&(d.push(C,F,N),y+=3)}l.addGroup(u,y,0),u+=y}function b(S){const T=g,y=new Xe,A=new k;let D=0;const x=S===!0?e:t,v=S===!0?1:-1;for(let F=1;F<=r;F++)h.push(0,p*v,0),f.push(0,v,0),m.push(.5,.5),g++;const C=g;for(let F=0;F<=r;F++){const P=F/r*c+o,U=Math.cos(P),z=Math.sin(P);A.x=x*z,A.y=p*v,A.z=x*U,h.push(A.x,A.y,A.z),f.push(0,v,0),y.x=U*.5+.5,y.y=z*.5*v+.5,m.push(y.x,y.y),g++}for(let F=0;F<r;F++){const N=T+F,P=C+F;S===!0?d.push(P,P+1,N):d.push(P+1,P,N),D+=3}l.addGroup(u,D,S===!0?1:2),u+=D}}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}static fromJSON(e){return new ji(e.radiusTop,e.radiusBottom,e.height,e.radialSegments,e.heightSegments,e.openEnded,e.thetaStart,e.thetaLength)}}class Ns extends ji{constructor(e=1,t=1,i=32,r=1,a=!1,s=0,o=Math.PI*2){super(0,e,t,i,r,a,s,o),this.type="ConeGeometry",this.parameters={radius:e,height:t,radialSegments:i,heightSegments:r,openEnded:a,thetaStart:s,thetaLength:o}}static fromJSON(e){return new Ns(e.radius,e.height,e.radialSegments,e.heightSegments,e.openEnded,e.thetaStart,e.thetaLength)}}const pr=new k,mr=new k,_a=new k,gr=new Ot;class ms extends st{constructor(e=null,t=1){if(super(),this.type="EdgesGeometry",this.parameters={geometry:e,thresholdAngle:t},e!==null){const r=Math.pow(10,4),a=Math.cos(Ar*t),s=e.getIndex(),o=e.getAttribute("position"),c=s?s.count:o.count,l=[0,0,0],d=["a","b","c"],h=new Array(3),f={},m=[];for(let g=0;g<c;g+=3){s?(l[0]=s.getX(g),l[1]=s.getX(g+1),l[2]=s.getX(g+2)):(l[0]=g,l[1]=g+1,l[2]=g+2);const{a:_,b:p,c:u}=gr;if(_.fromBufferAttribute(o,l[0]),p.fromBufferAttribute(o,l[1]),u.fromBufferAttribute(o,l[2]),gr.getNormal(_a),h[0]=`${Math.round(_.x*r)},${Math.round(_.y*r)},${Math.round(_.z*r)}`,h[1]=`${Math.round(p.x*r)},${Math.round(p.y*r)},${Math.round(p.z*r)}`,h[2]=`${Math.round(u.x*r)},${Math.round(u.y*r)},${Math.round(u.z*r)}`,!(h[0]===h[1]||h[1]===h[2]||h[2]===h[0]))for(let w=0;w<3;w++){const b=(w+1)%3,S=h[w],T=h[b],y=gr[d[w]],A=gr[d[b]],D=`${S}_${T}`,x=`${T}_${S}`;x in f&&f[x]?(_a.dot(f[x].normal)<=a&&(m.push(y.x,y.y,y.z),m.push(A.x,A.y,A.z)),f[x]=null):D in f||(f[D]={index0:l[w],index1:l[b],normal:_a.clone()})}}for(const g in f)if(f[g]){const{index0:_,index1:p}=f[g];pr.fromBufferAttribute(o,_),mr.fromBufferAttribute(o,p),m.push(pr.x,pr.y,pr.z),m.push(mr.x,mr.y,mr.z)}this.setAttribute("position",new nt(m,3))}}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}}class Wi extends st{constructor(e=1,t=1,i=1,r=1){super(),this.type="PlaneGeometry",this.parameters={width:e,height:t,widthSegments:i,heightSegments:r};const a=e/2,s=t/2,o=Math.floor(i),c=Math.floor(r),l=o+1,d=c+1,h=e/o,f=t/c,m=[],g=[],_=[],p=[];for(let u=0;u<d;u++){const w=u*f-s;for(let b=0;b<l;b++){const S=b*h-a;g.push(S,-w,0),_.push(0,0,1),p.push(b/o),p.push(1-u/c)}}for(let u=0;u<c;u++)for(let w=0;w<o;w++){const b=w+l*u,S=w+l*(u+1),T=w+1+l*(u+1),y=w+1+l*u;m.push(b,S,y),m.push(S,T,y)}this.setIndex(m),this.setAttribute("position",new nt(g,3)),this.setAttribute("normal",new nt(_,3)),this.setAttribute("uv",new nt(p,2))}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}static fromJSON(e){return new Wi(e.width,e.height,e.widthSegments,e.heightSegments)}}class Nr extends st{constructor(e=1,t=32,i=16,r=0,a=Math.PI*2,s=0,o=Math.PI){super(),this.type="SphereGeometry",this.parameters={radius:e,widthSegments:t,heightSegments:i,phiStart:r,phiLength:a,thetaStart:s,thetaLength:o},t=Math.max(3,Math.floor(t)),i=Math.max(2,Math.floor(i));const c=Math.min(s+o,Math.PI);let l=0;const d=[],h=new k,f=new k,m=[],g=[],_=[],p=[];for(let u=0;u<=i;u++){const w=[],b=u/i;let S=0;u===0&&s===0?S=.5/t:u===i&&c===Math.PI&&(S=-.5/t);for(let T=0;T<=t;T++){const y=T/t;h.x=-e*Math.cos(r+y*a)*Math.sin(s+b*o),h.y=e*Math.cos(s+b*o),h.z=e*Math.sin(r+y*a)*Math.sin(s+b*o),g.push(h.x,h.y,h.z),f.copy(h).normalize(),_.push(f.x,f.y,f.z),p.push(y+S,1-b),w.push(l++)}d.push(w)}for(let u=0;u<i;u++)for(let w=0;w<t;w++){const b=d[u][w+1],S=d[u][w],T=d[u+1][w],y=d[u+1][w+1];(u!==0||s>0)&&m.push(b,S,y),(u!==i-1||c<Math.PI)&&m.push(S,T,y)}this.setIndex(m),this.setAttribute("position",new nt(g,3)),this.setAttribute("normal",new nt(_,3)),this.setAttribute("uv",new nt(p,2))}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}static fromJSON(e){return new Nr(e.radius,e.widthSegments,e.heightSegments,e.phiStart,e.phiLength,e.thetaStart,e.thetaLength)}}class wt extends Ri{constructor(e){super(),this.isMeshStandardMaterial=!0,this.type="MeshStandardMaterial",this.defines={STANDARD:""},this.color=new ve(16777215),this.roughness=1,this.metalness=0,this.map=null,this.lightMap=null,this.lightMapIntensity=1,this.aoMap=null,this.aoMapIntensity=1,this.emissive=new ve(0),this.emissiveIntensity=1,this.emissiveMap=null,this.bumpMap=null,this.bumpScale=1,this.normalMap=null,this.normalMapType=vc,this.normalScale=new Xe(1,1),this.displacementMap=null,this.displacementScale=1,this.displacementBias=0,this.roughnessMap=null,this.metalnessMap=null,this.alphaMap=null,this.envMap=null,this.envMapRotation=new Jt,this.envMapIntensity=1,this.wireframe=!1,this.wireframeLinewidth=1,this.wireframeLinecap="round",this.wireframeLinejoin="round",this.flatShading=!1,this.fog=!0,this.setValues(e)}copy(e){return super.copy(e),this.defines={STANDARD:""},this.color.copy(e.color),this.roughness=e.roughness,this.metalness=e.metalness,this.map=e.map,this.lightMap=e.lightMap,this.lightMapIntensity=e.lightMapIntensity,this.aoMap=e.aoMap,this.aoMapIntensity=e.aoMapIntensity,this.emissive.copy(e.emissive),this.emissiveMap=e.emissiveMap,this.emissiveIntensity=e.emissiveIntensity,this.bumpMap=e.bumpMap,this.bumpScale=e.bumpScale,this.normalMap=e.normalMap,this.normalMapType=e.normalMapType,this.normalScale.copy(e.normalScale),this.displacementMap=e.displacementMap,this.displacementScale=e.displacementScale,this.displacementBias=e.displacementBias,this.roughnessMap=e.roughnessMap,this.metalnessMap=e.metalnessMap,this.alphaMap=e.alphaMap,this.envMap=e.envMap,this.envMapRotation.copy(e.envMapRotation),this.envMapIntensity=e.envMapIntensity,this.wireframe=e.wireframe,this.wireframeLinewidth=e.wireframeLinewidth,this.wireframeLinecap=e.wireframeLinecap,this.wireframeLinejoin=e.wireframeLinejoin,this.flatShading=e.flatShading,this.fog=e.fog,this}}class _u extends Ri{constructor(e){super(),this.isMeshDepthMaterial=!0,this.type="MeshDepthMaterial",this.depthPacking=Cl,this.map=null,this.alphaMap=null,this.displacementMap=null,this.displacementScale=1,this.displacementBias=0,this.wireframe=!1,this.wireframeLinewidth=1,this.setValues(e)}copy(e){return super.copy(e),this.depthPacking=e.depthPacking,this.map=e.map,this.alphaMap=e.alphaMap,this.displacementMap=e.displacementMap,this.displacementScale=e.displacementScale,this.displacementBias=e.displacementBias,this.wireframe=e.wireframe,this.wireframeLinewidth=e.wireframeLinewidth,this}}class vu extends Ri{constructor(e){super(),this.isMeshDistanceMaterial=!0,this.type="MeshDistanceMaterial",this.map=null,this.alphaMap=null,this.displacementMap=null,this.displacementScale=1,this.displacementBias=0,this.setValues(e)}copy(e){return super.copy(e),this.map=e.map,this.alphaMap=e.alphaMap,this.displacementMap=e.displacementMap,this.displacementScale=e.displacementScale,this.displacementBias=e.displacementBias,this}}class Cc extends _t{constructor(e,t=1){super(),this.isLight=!0,this.type="Light",this.color=new ve(e),this.intensity=t}dispose(){}copy(e,t){return super.copy(e,t),this.color.copy(e.color),this.intensity=e.intensity,this}toJSON(e){const t=super.toJSON(e);return t.object.color=this.color.getHex(),t.object.intensity=this.intensity,this.groundColor!==void 0&&(t.object.groundColor=this.groundColor.getHex()),this.distance!==void 0&&(t.object.distance=this.distance),this.angle!==void 0&&(t.object.angle=this.angle),this.decay!==void 0&&(t.object.decay=this.decay),this.penumbra!==void 0&&(t.object.penumbra=this.penumbra),this.shadow!==void 0&&(t.object.shadow=this.shadow.toJSON()),this.target!==void 0&&(t.object.target=this.target.uuid),t}}const va=new at,yo=new k,bo=new k;class xu{constructor(e){this.camera=e,this.intensity=1,this.bias=0,this.normalBias=0,this.radius=1,this.blurSamples=8,this.mapSize=new Xe(512,512),this.map=null,this.mapPass=null,this.matrix=new at,this.autoUpdate=!0,this.needsUpdate=!1,this._frustum=new Us,this._frameExtents=new Xe(1,1),this._viewportCount=1,this._viewports=[new lt(0,0,1,1)]}getViewportCount(){return this._viewportCount}getFrustum(){return this._frustum}updateMatrices(e){const t=this.camera,i=this.matrix;yo.setFromMatrixPosition(e.matrixWorld),t.position.copy(yo),bo.setFromMatrixPosition(e.target.matrixWorld),t.lookAt(bo),t.updateMatrixWorld(),va.multiplyMatrices(t.projectionMatrix,t.matrixWorldInverse),this._frustum.setFromProjectionMatrix(va),i.set(.5,0,0,.5,0,.5,0,.5,0,0,.5,.5,0,0,0,1),i.multiply(va)}getViewport(e){return this._viewports[e]}getFrameExtents(){return this._frameExtents}dispose(){this.map&&this.map.dispose(),this.mapPass&&this.mapPass.dispose()}copy(e){return this.camera=e.camera.clone(),this.intensity=e.intensity,this.bias=e.bias,this.radius=e.radius,this.mapSize.copy(e.mapSize),this}clone(){return new this.constructor().copy(this)}toJSON(){const e={};return this.intensity!==1&&(e.intensity=this.intensity),this.bias!==0&&(e.bias=this.bias),this.normalBias!==0&&(e.normalBias=this.normalBias),this.radius!==1&&(e.radius=this.radius),(this.mapSize.x!==512||this.mapSize.y!==512)&&(e.mapSize=this.mapSize.toArray()),e.camera=this.camera.toJSON(!1).object,delete e.camera.matrix,e}}class Pc extends Ac{constructor(e=-1,t=1,i=1,r=-1,a=.1,s=2e3){super(),this.isOrthographicCamera=!0,this.type="OrthographicCamera",this.zoom=1,this.view=null,this.left=e,this.right=t,this.top=i,this.bottom=r,this.near=a,this.far=s,this.updateProjectionMatrix()}copy(e,t){return super.copy(e,t),this.left=e.left,this.right=e.right,this.top=e.top,this.bottom=e.bottom,this.near=e.near,this.far=e.far,this.zoom=e.zoom,this.view=e.view===null?null:Object.assign({},e.view),this}setViewOffset(e,t,i,r,a,s){this.view===null&&(this.view={enabled:!0,fullWidth:1,fullHeight:1,offsetX:0,offsetY:0,width:1,height:1}),this.view.enabled=!0,this.view.fullWidth=e,this.view.fullHeight=t,this.view.offsetX=i,this.view.offsetY=r,this.view.width=a,this.view.height=s,this.updateProjectionMatrix()}clearViewOffset(){this.view!==null&&(this.view.enabled=!1),this.updateProjectionMatrix()}updateProjectionMatrix(){const e=(this.right-this.left)/(2*this.zoom),t=(this.top-this.bottom)/(2*this.zoom),i=(this.right+this.left)/2,r=(this.top+this.bottom)/2;let a=i-e,s=i+e,o=r+t,c=r-t;if(this.view!==null&&this.view.enabled){const l=(this.right-this.left)/this.view.fullWidth/this.zoom,d=(this.top-this.bottom)/this.view.fullHeight/this.zoom;a+=l*this.view.offsetX,s=a+l*this.view.width,o-=d*this.view.offsetY,c=o-d*this.view.height}this.projectionMatrix.makeOrthographic(a,s,o,c,this.near,this.far,this.coordinateSystem),this.projectionMatrixInverse.copy(this.projectionMatrix).invert()}toJSON(e){const t=super.toJSON(e);return t.object.zoom=this.zoom,t.object.left=this.left,t.object.right=this.right,t.object.top=this.top,t.object.bottom=this.bottom,t.object.near=this.near,t.object.far=this.far,this.view!==null&&(t.object.view=Object.assign({},this.view)),t}}class Mu extends xu{constructor(){super(new Pc(-5,5,5,-5,.5,500)),this.isDirectionalLightShadow=!0}}class To extends Cc{constructor(e,t){super(e,t),this.isDirectionalLight=!0,this.type="DirectionalLight",this.position.copy(_t.DEFAULT_UP),this.updateMatrix(),this.target=new _t,this.shadow=new Mu}dispose(){this.shadow.dispose()}copy(e){return super.copy(e),this.target=e.target.clone(),this.shadow=e.shadow.clone(),this}}class Su extends Cc{constructor(e,t){super(e,t),this.isAmbientLight=!0,this.type="AmbientLight"}}class Eu extends zt{constructor(e=[]){super(),this.isArrayCamera=!0,this.cameras=e,this.index=0}}const Ao=new at;class Fs{constructor(e,t,i=0,r=1/0){this.ray=new Ls(e,t),this.near=i,this.far=r,this.camera=null,this.layers=new Is,this.params={Mesh:{},Line:{threshold:1},LOD:{},Points:{threshold:1},Sprite:{}}}set(e,t){this.ray.set(e,t)}setFromCamera(e,t){t.isPerspectiveCamera?(this.ray.origin.setFromMatrixPosition(t.matrixWorld),this.ray.direction.set(e.x,e.y,.5).unproject(t).sub(this.ray.origin).normalize(),this.camera=t):t.isOrthographicCamera?(this.ray.origin.set(e.x,e.y,(t.near+t.far)/(t.near-t.far)).unproject(t),this.ray.direction.set(0,0,-1).transformDirection(t.matrixWorld),this.camera=t):console.error("THREE.Raycaster: Unsupported camera type: "+t.type)}setFromXRController(e){return Ao.identity().extractRotation(e.matrixWorld),this.ray.origin.setFromMatrixPosition(e.matrixWorld),this.ray.direction.set(0,0,-1).applyMatrix4(Ao),this}intersectObject(e,t=!0,i=[]){return gs(e,this,i,t),i.sort(wo),i}intersectObjects(e,t=!0,i=[]){for(let r=0,a=e.length;r<a;r++)gs(e[r],this,i,t);return i.sort(wo),i}}function wo(n,e){return n.distance-e.distance}function gs(n,e,t,i){let r=!0;if(n.layers.test(e.layers)&&n.raycast(e,t)===!1&&(r=!1),r===!0&&i===!0){const a=n.children;for(let s=0,o=a.length;s<o;s++)gs(a[s],e,t,!0)}}function Ro(n,e,t,i){const r=yu(i);switch(t){case dc:return n*e;case fc:return n*e;case pc:return n*e*2;case mc:return n*e/r.components*r.byteLength;case Rs:return n*e/r.components*r.byteLength;case gc:return n*e*2/r.components*r.byteLength;case Cs:return n*e*2/r.components*r.byteLength;case hc:return n*e*3/r.components*r.byteLength;case Yt:return n*e*4/r.components*r.byteLength;case Ps:return n*e*4/r.components*r.byteLength;case Sr:case Er:return Math.floor((n+3)/4)*Math.floor((e+3)/4)*8;case yr:case br:return Math.floor((n+3)/4)*Math.floor((e+3)/4)*16;case Ga:case Wa:return Math.max(n,16)*Math.max(e,8)/4;case Va:case ja:return Math.max(n,8)*Math.max(e,8)/2;case Xa:case Ya:return Math.floor((n+3)/4)*Math.floor((e+3)/4)*8;case qa:return Math.floor((n+3)/4)*Math.floor((e+3)/4)*16;case $a:return Math.floor((n+3)/4)*Math.floor((e+3)/4)*16;case Ka:return Math.floor((n+4)/5)*Math.floor((e+3)/4)*16;case Za:return Math.floor((n+4)/5)*Math.floor((e+4)/5)*16;case Ja:return Math.floor((n+5)/6)*Math.floor((e+4)/5)*16;case Qa:return Math.floor((n+5)/6)*Math.floor((e+5)/6)*16;case es:return Math.floor((n+7)/8)*Math.floor((e+4)/5)*16;case ts:return Math.floor((n+7)/8)*Math.floor((e+5)/6)*16;case ns:return Math.floor((n+7)/8)*Math.floor((e+7)/8)*16;case is:return Math.floor((n+9)/10)*Math.floor((e+4)/5)*16;case rs:return Math.floor((n+9)/10)*Math.floor((e+5)/6)*16;case as:return Math.floor((n+9)/10)*Math.floor((e+7)/8)*16;case ss:return Math.floor((n+9)/10)*Math.floor((e+9)/10)*16;case os:return Math.floor((n+11)/12)*Math.floor((e+9)/10)*16;case cs:return Math.floor((n+11)/12)*Math.floor((e+11)/12)*16;case Tr:case ls:case us:return Math.ceil(n/4)*Math.ceil(e/4)*16;case _c:case ds:return Math.ceil(n/4)*Math.ceil(e/4)*8;case hs:case fs:return Math.ceil(n/4)*Math.ceil(e/4)*16}throw new Error(`Unable to determine texture byte length for ${t} format.`)}function yu(n){switch(n){case pn:case cc:return{byteLength:1,components:1};case Oi:case lc:case Bi:return{byteLength:2,components:1};case As:case ws:return{byteLength:2,components:4};case Yn:case Ts:case un:return{byteLength:4,components:1};case uc:return{byteLength:4,components:3}}throw new Error(`Unknown texture type ${n}.`)}typeof __THREE_DEVTOOLS__<"u"&&__THREE_DEVTOOLS__.dispatchEvent(new CustomEvent("register",{detail:{revision:bs}}));typeof window<"u"&&(window.__THREE__?console.warn("WARNING: Multiple instances of Three.js being imported."):window.__THREE__=bs);/**
 * @license
 * Copyright 2010-2025 Three.js Authors
 * SPDX-License-Identifier: MIT
 */function Dc(){let n=null,e=!1,t=null,i=null;function r(a,s){t(a,s),i=n.requestAnimationFrame(r)}return{start:function(){e!==!0&&t!==null&&(i=n.requestAnimationFrame(r),e=!0)},stop:function(){n.cancelAnimationFrame(i),e=!1},setAnimationLoop:function(a){t=a},setContext:function(a){n=a}}}function bu(n){const e=new WeakMap;function t(o,c){const l=o.array,d=o.usage,h=l.byteLength,f=n.createBuffer();n.bindBuffer(c,f),n.bufferData(c,l,d),o.onUploadCallback();let m;if(l instanceof Float32Array)m=n.FLOAT;else if(l instanceof Uint16Array)o.isFloat16BufferAttribute?m=n.HALF_FLOAT:m=n.UNSIGNED_SHORT;else if(l instanceof Int16Array)m=n.SHORT;else if(l instanceof Uint32Array)m=n.UNSIGNED_INT;else if(l instanceof Int32Array)m=n.INT;else if(l instanceof Int8Array)m=n.BYTE;else if(l instanceof Uint8Array)m=n.UNSIGNED_BYTE;else if(l instanceof Uint8ClampedArray)m=n.UNSIGNED_BYTE;else throw new Error("THREE.WebGLAttributes: Unsupported buffer data format: "+l);return{buffer:f,type:m,bytesPerElement:l.BYTES_PER_ELEMENT,version:o.version,size:h}}function i(o,c,l){const d=c.array,h=c.updateRanges;if(n.bindBuffer(l,o),h.length===0)n.bufferSubData(l,0,d);else{h.sort((m,g)=>m.start-g.start);let f=0;for(let m=1;m<h.length;m++){const g=h[f],_=h[m];_.start<=g.start+g.count+1?g.count=Math.max(g.count,_.start+_.count-g.start):(++f,h[f]=_)}h.length=f+1;for(let m=0,g=h.length;m<g;m++){const _=h[m];n.bufferSubData(l,_.start*d.BYTES_PER_ELEMENT,d,_.start,_.count)}c.clearUpdateRanges()}c.onUploadCallback()}function r(o){return o.isInterleavedBufferAttribute&&(o=o.data),e.get(o)}function a(o){o.isInterleavedBufferAttribute&&(o=o.data);const c=e.get(o);c&&(n.deleteBuffer(c.buffer),e.delete(o))}function s(o,c){if(o.isInterleavedBufferAttribute&&(o=o.data),o.isGLBufferAttribute){const d=e.get(o);(!d||d.version<o.version)&&e.set(o,{buffer:o.buffer,type:o.type,bytesPerElement:o.elementSize,version:o.version});return}const l=e.get(o);if(l===void 0)e.set(o,t(o,c));else if(l.version<o.version){if(l.size!==o.array.byteLength)throw new Error("THREE.WebGLAttributes: The size of the buffer attribute's array buffer does not match the original size. Resizing buffer attributes is not supported.");i(l.buffer,o,c),l.version=o.version}}return{get:r,remove:a,update:s}}var Tu=`#ifdef USE_ALPHAHASH
	if ( diffuseColor.a < getAlphaHashThreshold( vPosition ) ) discard;
#endif`,Au=`#ifdef USE_ALPHAHASH
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
#endif`,wu=`#ifdef USE_ALPHAMAP
	diffuseColor.a *= texture2D( alphaMap, vAlphaMapUv ).g;
#endif`,Ru=`#ifdef USE_ALPHAMAP
	uniform sampler2D alphaMap;
#endif`,Cu=`#ifdef USE_ALPHATEST
	#ifdef ALPHA_TO_COVERAGE
	diffuseColor.a = smoothstep( alphaTest, alphaTest + fwidth( diffuseColor.a ), diffuseColor.a );
	if ( diffuseColor.a == 0.0 ) discard;
	#else
	if ( diffuseColor.a < alphaTest ) discard;
	#endif
#endif`,Pu=`#ifdef USE_ALPHATEST
	uniform float alphaTest;
#endif`,Du=`#ifdef USE_AOMAP
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
#endif`,Lu=`#ifdef USE_AOMAP
	uniform sampler2D aoMap;
	uniform float aoMapIntensity;
#endif`,Iu=`#ifdef USE_BATCHING
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
#endif`,Uu=`#ifdef USE_BATCHING
	mat4 batchingMatrix = getBatchingMatrix( getIndirectIndex( gl_DrawID ) );
#endif`,Nu=`vec3 transformed = vec3( position );
#ifdef USE_ALPHAHASH
	vPosition = vec3( position );
#endif`,Fu=`vec3 objectNormal = vec3( normal );
#ifdef USE_TANGENT
	vec3 objectTangent = vec3( tangent.xyz );
#endif`,zu=`float G_BlinnPhong_Implicit( ) {
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
} // validated`,ku=`#ifdef USE_IRIDESCENCE
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
#endif`,Ou=`#ifdef USE_BUMPMAP
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
#endif`,Bu=`#if NUM_CLIPPING_PLANES > 0
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
#endif`,Hu=`#if NUM_CLIPPING_PLANES > 0
	varying vec3 vClipPosition;
	uniform vec4 clippingPlanes[ NUM_CLIPPING_PLANES ];
#endif`,Vu=`#if NUM_CLIPPING_PLANES > 0
	varying vec3 vClipPosition;
#endif`,Gu=`#if NUM_CLIPPING_PLANES > 0
	vClipPosition = - mvPosition.xyz;
#endif`,ju=`#if defined( USE_COLOR_ALPHA )
	diffuseColor *= vColor;
#elif defined( USE_COLOR )
	diffuseColor.rgb *= vColor;
#endif`,Wu=`#if defined( USE_COLOR_ALPHA )
	varying vec4 vColor;
#elif defined( USE_COLOR )
	varying vec3 vColor;
#endif`,Xu=`#if defined( USE_COLOR_ALPHA )
	varying vec4 vColor;
#elif defined( USE_COLOR ) || defined( USE_INSTANCING_COLOR ) || defined( USE_BATCHING_COLOR )
	varying vec3 vColor;
#endif`,Yu=`#if defined( USE_COLOR_ALPHA )
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
#endif`,qu=`#define PI 3.141592653589793
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
} // validated`,$u=`#ifdef ENVMAP_TYPE_CUBE_UV
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
#endif`,Ku=`vec3 transformedNormal = objectNormal;
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
#endif`,Zu=`#ifdef USE_DISPLACEMENTMAP
	uniform sampler2D displacementMap;
	uniform float displacementScale;
	uniform float displacementBias;
#endif`,Ju=`#ifdef USE_DISPLACEMENTMAP
	transformed += normalize( objectNormal ) * ( texture2D( displacementMap, vDisplacementMapUv ).x * displacementScale + displacementBias );
#endif`,Qu=`#ifdef USE_EMISSIVEMAP
	vec4 emissiveColor = texture2D( emissiveMap, vEmissiveMapUv );
	#ifdef DECODE_VIDEO_TEXTURE_EMISSIVE
		emissiveColor = sRGBTransferEOTF( emissiveColor );
	#endif
	totalEmissiveRadiance *= emissiveColor.rgb;
#endif`,ed=`#ifdef USE_EMISSIVEMAP
	uniform sampler2D emissiveMap;
#endif`,td="gl_FragColor = linearToOutputTexel( gl_FragColor );",nd=`vec4 LinearTransferOETF( in vec4 value ) {
	return value;
}
vec4 sRGBTransferEOTF( in vec4 value ) {
	return vec4( mix( pow( value.rgb * 0.9478672986 + vec3( 0.0521327014 ), vec3( 2.4 ) ), value.rgb * 0.0773993808, vec3( lessThanEqual( value.rgb, vec3( 0.04045 ) ) ) ), value.a );
}
vec4 sRGBTransferOETF( in vec4 value ) {
	return vec4( mix( pow( value.rgb, vec3( 0.41666 ) ) * 1.055 - vec3( 0.055 ), value.rgb * 12.92, vec3( lessThanEqual( value.rgb, vec3( 0.0031308 ) ) ) ), value.a );
}`,id=`#ifdef USE_ENVMAP
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
#endif`,rd=`#ifdef USE_ENVMAP
	uniform float envMapIntensity;
	uniform float flipEnvMap;
	uniform mat3 envMapRotation;
	#ifdef ENVMAP_TYPE_CUBE
		uniform samplerCube envMap;
	#else
		uniform sampler2D envMap;
	#endif
	
#endif`,ad=`#ifdef USE_ENVMAP
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
#endif`,sd=`#ifdef USE_ENVMAP
	#if defined( USE_BUMPMAP ) || defined( USE_NORMALMAP ) || defined( PHONG ) || defined( LAMBERT )
		#define ENV_WORLDPOS
	#endif
	#ifdef ENV_WORLDPOS
		
		varying vec3 vWorldPosition;
	#else
		varying vec3 vReflect;
		uniform float refractionRatio;
	#endif
#endif`,od=`#ifdef USE_ENVMAP
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
#endif`,cd=`#ifdef USE_FOG
	vFogDepth = - mvPosition.z;
#endif`,ld=`#ifdef USE_FOG
	varying float vFogDepth;
#endif`,ud=`#ifdef USE_FOG
	#ifdef FOG_EXP2
		float fogFactor = 1.0 - exp( - fogDensity * fogDensity * vFogDepth * vFogDepth );
	#else
		float fogFactor = smoothstep( fogNear, fogFar, vFogDepth );
	#endif
	gl_FragColor.rgb = mix( gl_FragColor.rgb, fogColor, fogFactor );
#endif`,dd=`#ifdef USE_FOG
	uniform vec3 fogColor;
	varying float vFogDepth;
	#ifdef FOG_EXP2
		uniform float fogDensity;
	#else
		uniform float fogNear;
		uniform float fogFar;
	#endif
#endif`,hd=`#ifdef USE_GRADIENTMAP
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
}`,fd=`#ifdef USE_LIGHTMAP
	uniform sampler2D lightMap;
	uniform float lightMapIntensity;
#endif`,pd=`LambertMaterial material;
material.diffuseColor = diffuseColor.rgb;
material.specularStrength = specularStrength;`,md=`varying vec3 vViewPosition;
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
#define RE_IndirectDiffuse		RE_IndirectDiffuse_Lambert`,gd=`uniform bool receiveShadow;
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
#endif`,_d=`#ifdef USE_ENVMAP
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
#endif`,vd=`ToonMaterial material;
material.diffuseColor = diffuseColor.rgb;`,xd=`varying vec3 vViewPosition;
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
#define RE_IndirectDiffuse		RE_IndirectDiffuse_Toon`,Md=`BlinnPhongMaterial material;
material.diffuseColor = diffuseColor.rgb;
material.specularColor = specular;
material.specularShininess = shininess;
material.specularStrength = specularStrength;`,Sd=`varying vec3 vViewPosition;
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
#define RE_IndirectDiffuse		RE_IndirectDiffuse_BlinnPhong`,Ed=`PhysicalMaterial material;
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
#endif`,yd=`struct PhysicalMaterial {
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
}`,bd=`
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
#endif`,Td=`#if defined( RE_IndirectDiffuse )
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
#endif`,Ad=`#if defined( RE_IndirectDiffuse )
	RE_IndirectDiffuse( irradiance, geometryPosition, geometryNormal, geometryViewDir, geometryClearcoatNormal, material, reflectedLight );
#endif
#if defined( RE_IndirectSpecular )
	RE_IndirectSpecular( radiance, iblIrradiance, clearcoatRadiance, geometryPosition, geometryNormal, geometryViewDir, geometryClearcoatNormal, material, reflectedLight );
#endif`,wd=`#if defined( USE_LOGDEPTHBUF )
	gl_FragDepth = vIsPerspective == 0.0 ? gl_FragCoord.z : log2( vFragDepth ) * logDepthBufFC * 0.5;
#endif`,Rd=`#if defined( USE_LOGDEPTHBUF )
	uniform float logDepthBufFC;
	varying float vFragDepth;
	varying float vIsPerspective;
#endif`,Cd=`#ifdef USE_LOGDEPTHBUF
	varying float vFragDepth;
	varying float vIsPerspective;
#endif`,Pd=`#ifdef USE_LOGDEPTHBUF
	vFragDepth = 1.0 + gl_Position.w;
	vIsPerspective = float( isPerspectiveMatrix( projectionMatrix ) );
#endif`,Dd=`#ifdef USE_MAP
	vec4 sampledDiffuseColor = texture2D( map, vMapUv );
	#ifdef DECODE_VIDEO_TEXTURE
		sampledDiffuseColor = sRGBTransferEOTF( sampledDiffuseColor );
	#endif
	diffuseColor *= sampledDiffuseColor;
#endif`,Ld=`#ifdef USE_MAP
	uniform sampler2D map;
#endif`,Id=`#if defined( USE_MAP ) || defined( USE_ALPHAMAP )
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
#endif`,Ud=`#if defined( USE_POINTS_UV )
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
#endif`,Nd=`float metalnessFactor = metalness;
#ifdef USE_METALNESSMAP
	vec4 texelMetalness = texture2D( metalnessMap, vMetalnessMapUv );
	metalnessFactor *= texelMetalness.b;
#endif`,Fd=`#ifdef USE_METALNESSMAP
	uniform sampler2D metalnessMap;
#endif`,zd=`#ifdef USE_INSTANCING_MORPH
	float morphTargetInfluences[ MORPHTARGETS_COUNT ];
	float morphTargetBaseInfluence = texelFetch( morphTexture, ivec2( 0, gl_InstanceID ), 0 ).r;
	for ( int i = 0; i < MORPHTARGETS_COUNT; i ++ ) {
		morphTargetInfluences[i] =  texelFetch( morphTexture, ivec2( i + 1, gl_InstanceID ), 0 ).r;
	}
#endif`,kd=`#if defined( USE_MORPHCOLORS )
	vColor *= morphTargetBaseInfluence;
	for ( int i = 0; i < MORPHTARGETS_COUNT; i ++ ) {
		#if defined( USE_COLOR_ALPHA )
			if ( morphTargetInfluences[ i ] != 0.0 ) vColor += getMorph( gl_VertexID, i, 2 ) * morphTargetInfluences[ i ];
		#elif defined( USE_COLOR )
			if ( morphTargetInfluences[ i ] != 0.0 ) vColor += getMorph( gl_VertexID, i, 2 ).rgb * morphTargetInfluences[ i ];
		#endif
	}
#endif`,Od=`#ifdef USE_MORPHNORMALS
	objectNormal *= morphTargetBaseInfluence;
	for ( int i = 0; i < MORPHTARGETS_COUNT; i ++ ) {
		if ( morphTargetInfluences[ i ] != 0.0 ) objectNormal += getMorph( gl_VertexID, i, 1 ).xyz * morphTargetInfluences[ i ];
	}
#endif`,Bd=`#ifdef USE_MORPHTARGETS
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
#endif`,Hd=`#ifdef USE_MORPHTARGETS
	transformed *= morphTargetBaseInfluence;
	for ( int i = 0; i < MORPHTARGETS_COUNT; i ++ ) {
		if ( morphTargetInfluences[ i ] != 0.0 ) transformed += getMorph( gl_VertexID, i, 0 ).xyz * morphTargetInfluences[ i ];
	}
#endif`,Vd=`float faceDirection = gl_FrontFacing ? 1.0 : - 1.0;
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
vec3 nonPerturbedNormal = normal;`,Gd=`#ifdef USE_NORMALMAP_OBJECTSPACE
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
#endif`,jd=`#ifndef FLAT_SHADED
	varying vec3 vNormal;
	#ifdef USE_TANGENT
		varying vec3 vTangent;
		varying vec3 vBitangent;
	#endif
#endif`,Wd=`#ifndef FLAT_SHADED
	varying vec3 vNormal;
	#ifdef USE_TANGENT
		varying vec3 vTangent;
		varying vec3 vBitangent;
	#endif
#endif`,Xd=`#ifndef FLAT_SHADED
	vNormal = normalize( transformedNormal );
	#ifdef USE_TANGENT
		vTangent = normalize( transformedTangent );
		vBitangent = normalize( cross( vNormal, vTangent ) * tangent.w );
	#endif
#endif`,Yd=`#ifdef USE_NORMALMAP
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
#endif`,qd=`#ifdef USE_CLEARCOAT
	vec3 clearcoatNormal = nonPerturbedNormal;
#endif`,$d=`#ifdef USE_CLEARCOAT_NORMALMAP
	vec3 clearcoatMapN = texture2D( clearcoatNormalMap, vClearcoatNormalMapUv ).xyz * 2.0 - 1.0;
	clearcoatMapN.xy *= clearcoatNormalScale;
	clearcoatNormal = normalize( tbn2 * clearcoatMapN );
#endif`,Kd=`#ifdef USE_CLEARCOATMAP
	uniform sampler2D clearcoatMap;
#endif
#ifdef USE_CLEARCOAT_NORMALMAP
	uniform sampler2D clearcoatNormalMap;
	uniform vec2 clearcoatNormalScale;
#endif
#ifdef USE_CLEARCOAT_ROUGHNESSMAP
	uniform sampler2D clearcoatRoughnessMap;
#endif`,Zd=`#ifdef USE_IRIDESCENCEMAP
	uniform sampler2D iridescenceMap;
#endif
#ifdef USE_IRIDESCENCE_THICKNESSMAP
	uniform sampler2D iridescenceThicknessMap;
#endif`,Jd=`#ifdef OPAQUE
diffuseColor.a = 1.0;
#endif
#ifdef USE_TRANSMISSION
diffuseColor.a *= material.transmissionAlpha;
#endif
gl_FragColor = vec4( outgoingLight, diffuseColor.a );`,Qd=`vec3 packNormalToRGB( const in vec3 normal ) {
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
}`,eh=`#ifdef PREMULTIPLIED_ALPHA
	gl_FragColor.rgb *= gl_FragColor.a;
#endif`,th=`vec4 mvPosition = vec4( transformed, 1.0 );
#ifdef USE_BATCHING
	mvPosition = batchingMatrix * mvPosition;
#endif
#ifdef USE_INSTANCING
	mvPosition = instanceMatrix * mvPosition;
#endif
mvPosition = modelViewMatrix * mvPosition;
gl_Position = projectionMatrix * mvPosition;`,nh=`#ifdef DITHERING
	gl_FragColor.rgb = dithering( gl_FragColor.rgb );
#endif`,ih=`#ifdef DITHERING
	vec3 dithering( vec3 color ) {
		float grid_position = rand( gl_FragCoord.xy );
		vec3 dither_shift_RGB = vec3( 0.25 / 255.0, -0.25 / 255.0, 0.25 / 255.0 );
		dither_shift_RGB = mix( 2.0 * dither_shift_RGB, -2.0 * dither_shift_RGB, grid_position );
		return color + dither_shift_RGB;
	}
#endif`,rh=`float roughnessFactor = roughness;
#ifdef USE_ROUGHNESSMAP
	vec4 texelRoughness = texture2D( roughnessMap, vRoughnessMapUv );
	roughnessFactor *= texelRoughness.g;
#endif`,ah=`#ifdef USE_ROUGHNESSMAP
	uniform sampler2D roughnessMap;
#endif`,sh=`#if NUM_SPOT_LIGHT_COORDS > 0
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
#endif`,oh=`#if NUM_SPOT_LIGHT_COORDS > 0
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
#endif`,ch=`#if ( defined( USE_SHADOWMAP ) && ( NUM_DIR_LIGHT_SHADOWS > 0 || NUM_POINT_LIGHT_SHADOWS > 0 ) ) || ( NUM_SPOT_LIGHT_COORDS > 0 )
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
#endif`,lh=`float getShadowMask() {
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
}`,uh=`#ifdef USE_SKINNING
	mat4 boneMatX = getBoneMatrix( skinIndex.x );
	mat4 boneMatY = getBoneMatrix( skinIndex.y );
	mat4 boneMatZ = getBoneMatrix( skinIndex.z );
	mat4 boneMatW = getBoneMatrix( skinIndex.w );
#endif`,dh=`#ifdef USE_SKINNING
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
#endif`,hh=`#ifdef USE_SKINNING
	vec4 skinVertex = bindMatrix * vec4( transformed, 1.0 );
	vec4 skinned = vec4( 0.0 );
	skinned += boneMatX * skinVertex * skinWeight.x;
	skinned += boneMatY * skinVertex * skinWeight.y;
	skinned += boneMatZ * skinVertex * skinWeight.z;
	skinned += boneMatW * skinVertex * skinWeight.w;
	transformed = ( bindMatrixInverse * skinned ).xyz;
#endif`,fh=`#ifdef USE_SKINNING
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
#endif`,ph=`float specularStrength;
#ifdef USE_SPECULARMAP
	vec4 texelSpecular = texture2D( specularMap, vSpecularMapUv );
	specularStrength = texelSpecular.r;
#else
	specularStrength = 1.0;
#endif`,mh=`#ifdef USE_SPECULARMAP
	uniform sampler2D specularMap;
#endif`,gh=`#if defined( TONE_MAPPING )
	gl_FragColor.rgb = toneMapping( gl_FragColor.rgb );
#endif`,_h=`#ifndef saturate
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
vec3 CustomToneMapping( vec3 color ) { return color; }`,vh=`#ifdef USE_TRANSMISSION
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
#endif`,xh=`#ifdef USE_TRANSMISSION
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
#endif`,Mh=`#if defined( USE_UV ) || defined( USE_ANISOTROPY )
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
#endif`,Sh=`#if defined( USE_UV ) || defined( USE_ANISOTROPY )
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
#endif`,Eh=`#if defined( USE_UV ) || defined( USE_ANISOTROPY )
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
#endif`,yh=`#if defined( USE_ENVMAP ) || defined( DISTANCE ) || defined ( USE_SHADOWMAP ) || defined ( USE_TRANSMISSION ) || NUM_SPOT_LIGHT_COORDS > 0
	vec4 worldPosition = vec4( transformed, 1.0 );
	#ifdef USE_BATCHING
		worldPosition = batchingMatrix * worldPosition;
	#endif
	#ifdef USE_INSTANCING
		worldPosition = instanceMatrix * worldPosition;
	#endif
	worldPosition = modelMatrix * worldPosition;
#endif`;const bh=`varying vec2 vUv;
uniform mat3 uvTransform;
void main() {
	vUv = ( uvTransform * vec3( uv, 1 ) ).xy;
	gl_Position = vec4( position.xy, 1.0, 1.0 );
}`,Th=`uniform sampler2D t2D;
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
}`,Ah=`varying vec3 vWorldDirection;
#include <common>
void main() {
	vWorldDirection = transformDirection( position, modelMatrix );
	#include <begin_vertex>
	#include <project_vertex>
	gl_Position.z = gl_Position.w;
}`,wh=`#ifdef ENVMAP_TYPE_CUBE
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
}`,Rh=`varying vec3 vWorldDirection;
#include <common>
void main() {
	vWorldDirection = transformDirection( position, modelMatrix );
	#include <begin_vertex>
	#include <project_vertex>
	gl_Position.z = gl_Position.w;
}`,Ch=`uniform samplerCube tCube;
uniform float tFlip;
uniform float opacity;
varying vec3 vWorldDirection;
void main() {
	vec4 texColor = textureCube( tCube, vec3( tFlip * vWorldDirection.x, vWorldDirection.yz ) );
	gl_FragColor = texColor;
	gl_FragColor.a *= opacity;
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
}`,Ph=`#include <common>
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
}`,Dh=`#if DEPTH_PACKING == 3200
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
}`,Lh=`#define DISTANCE
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
}`,Ih=`#define DISTANCE
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
}`,Uh=`varying vec3 vWorldDirection;
#include <common>
void main() {
	vWorldDirection = transformDirection( position, modelMatrix );
	#include <begin_vertex>
	#include <project_vertex>
}`,Nh=`uniform sampler2D tEquirect;
varying vec3 vWorldDirection;
#include <common>
void main() {
	vec3 direction = normalize( vWorldDirection );
	vec2 sampleUV = equirectUv( direction );
	gl_FragColor = texture2D( tEquirect, sampleUV );
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
}`,Fh=`uniform float scale;
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
}`,zh=`uniform vec3 diffuse;
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
}`,kh=`#include <common>
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
}`,Oh=`uniform vec3 diffuse;
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
}`,Bh=`#define LAMBERT
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
}`,Hh=`#define LAMBERT
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
}`,Vh=`#define MATCAP
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
}`,Gh=`#define MATCAP
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
}`,jh=`#define NORMAL
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
}`,Wh=`#define NORMAL
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
}`,Xh=`#define PHONG
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
}`,Yh=`#define PHONG
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
}`,qh=`#define STANDARD
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
}`,$h=`#define STANDARD
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
}`,Kh=`#define TOON
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
}`,Zh=`#define TOON
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
}`,Jh=`uniform float size;
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
}`,Qh=`uniform vec3 diffuse;
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
}`,ef=`#include <common>
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
}`,tf=`uniform vec3 color;
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
}`,nf=`uniform float rotation;
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
}`,rf=`uniform vec3 diffuse;
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
}`,Ve={alphahash_fragment:Tu,alphahash_pars_fragment:Au,alphamap_fragment:wu,alphamap_pars_fragment:Ru,alphatest_fragment:Cu,alphatest_pars_fragment:Pu,aomap_fragment:Du,aomap_pars_fragment:Lu,batching_pars_vertex:Iu,batching_vertex:Uu,begin_vertex:Nu,beginnormal_vertex:Fu,bsdfs:zu,iridescence_fragment:ku,bumpmap_pars_fragment:Ou,clipping_planes_fragment:Bu,clipping_planes_pars_fragment:Hu,clipping_planes_pars_vertex:Vu,clipping_planes_vertex:Gu,color_fragment:ju,color_pars_fragment:Wu,color_pars_vertex:Xu,color_vertex:Yu,common:qu,cube_uv_reflection_fragment:$u,defaultnormal_vertex:Ku,displacementmap_pars_vertex:Zu,displacementmap_vertex:Ju,emissivemap_fragment:Qu,emissivemap_pars_fragment:ed,colorspace_fragment:td,colorspace_pars_fragment:nd,envmap_fragment:id,envmap_common_pars_fragment:rd,envmap_pars_fragment:ad,envmap_pars_vertex:sd,envmap_physical_pars_fragment:_d,envmap_vertex:od,fog_vertex:cd,fog_pars_vertex:ld,fog_fragment:ud,fog_pars_fragment:dd,gradientmap_pars_fragment:hd,lightmap_pars_fragment:fd,lights_lambert_fragment:pd,lights_lambert_pars_fragment:md,lights_pars_begin:gd,lights_toon_fragment:vd,lights_toon_pars_fragment:xd,lights_phong_fragment:Md,lights_phong_pars_fragment:Sd,lights_physical_fragment:Ed,lights_physical_pars_fragment:yd,lights_fragment_begin:bd,lights_fragment_maps:Td,lights_fragment_end:Ad,logdepthbuf_fragment:wd,logdepthbuf_pars_fragment:Rd,logdepthbuf_pars_vertex:Cd,logdepthbuf_vertex:Pd,map_fragment:Dd,map_pars_fragment:Ld,map_particle_fragment:Id,map_particle_pars_fragment:Ud,metalnessmap_fragment:Nd,metalnessmap_pars_fragment:Fd,morphinstance_vertex:zd,morphcolor_vertex:kd,morphnormal_vertex:Od,morphtarget_pars_vertex:Bd,morphtarget_vertex:Hd,normal_fragment_begin:Vd,normal_fragment_maps:Gd,normal_pars_fragment:jd,normal_pars_vertex:Wd,normal_vertex:Xd,normalmap_pars_fragment:Yd,clearcoat_normal_fragment_begin:qd,clearcoat_normal_fragment_maps:$d,clearcoat_pars_fragment:Kd,iridescence_pars_fragment:Zd,opaque_fragment:Jd,packing:Qd,premultiplied_alpha_fragment:eh,project_vertex:th,dithering_fragment:nh,dithering_pars_fragment:ih,roughnessmap_fragment:rh,roughnessmap_pars_fragment:ah,shadowmap_pars_fragment:sh,shadowmap_pars_vertex:oh,shadowmap_vertex:ch,shadowmask_pars_fragment:lh,skinbase_vertex:uh,skinning_pars_vertex:dh,skinning_vertex:hh,skinnormal_vertex:fh,specularmap_fragment:ph,specularmap_pars_fragment:mh,tonemapping_fragment:gh,tonemapping_pars_fragment:_h,transmission_fragment:vh,transmission_pars_fragment:xh,uv_pars_fragment:Mh,uv_pars_vertex:Sh,uv_vertex:Eh,worldpos_vertex:yh,background_vert:bh,background_frag:Th,backgroundCube_vert:Ah,backgroundCube_frag:wh,cube_vert:Rh,cube_frag:Ch,depth_vert:Ph,depth_frag:Dh,distanceRGBA_vert:Lh,distanceRGBA_frag:Ih,equirect_vert:Uh,equirect_frag:Nh,linedashed_vert:Fh,linedashed_frag:zh,meshbasic_vert:kh,meshbasic_frag:Oh,meshlambert_vert:Bh,meshlambert_frag:Hh,meshmatcap_vert:Vh,meshmatcap_frag:Gh,meshnormal_vert:jh,meshnormal_frag:Wh,meshphong_vert:Xh,meshphong_frag:Yh,meshphysical_vert:qh,meshphysical_frag:$h,meshtoon_vert:Kh,meshtoon_frag:Zh,points_vert:Jh,points_frag:Qh,shadow_vert:ef,shadow_frag:tf,sprite_vert:nf,sprite_frag:rf},he={common:{diffuse:{value:new ve(16777215)},opacity:{value:1},map:{value:null},mapTransform:{value:new Be},alphaMap:{value:null},alphaMapTransform:{value:new Be},alphaTest:{value:0}},specularmap:{specularMap:{value:null},specularMapTransform:{value:new Be}},envmap:{envMap:{value:null},envMapRotation:{value:new Be},flipEnvMap:{value:-1},reflectivity:{value:1},ior:{value:1.5},refractionRatio:{value:.98}},aomap:{aoMap:{value:null},aoMapIntensity:{value:1},aoMapTransform:{value:new Be}},lightmap:{lightMap:{value:null},lightMapIntensity:{value:1},lightMapTransform:{value:new Be}},bumpmap:{bumpMap:{value:null},bumpMapTransform:{value:new Be},bumpScale:{value:1}},normalmap:{normalMap:{value:null},normalMapTransform:{value:new Be},normalScale:{value:new Xe(1,1)}},displacementmap:{displacementMap:{value:null},displacementMapTransform:{value:new Be},displacementScale:{value:1},displacementBias:{value:0}},emissivemap:{emissiveMap:{value:null},emissiveMapTransform:{value:new Be}},metalnessmap:{metalnessMap:{value:null},metalnessMapTransform:{value:new Be}},roughnessmap:{roughnessMap:{value:null},roughnessMapTransform:{value:new Be}},gradientmap:{gradientMap:{value:null}},fog:{fogDensity:{value:25e-5},fogNear:{value:1},fogFar:{value:2e3},fogColor:{value:new ve(16777215)}},lights:{ambientLightColor:{value:[]},lightProbe:{value:[]},directionalLights:{value:[],properties:{direction:{},color:{}}},directionalLightShadows:{value:[],properties:{shadowIntensity:1,shadowBias:{},shadowNormalBias:{},shadowRadius:{},shadowMapSize:{}}},directionalShadowMap:{value:[]},directionalShadowMatrix:{value:[]},spotLights:{value:[],properties:{color:{},position:{},direction:{},distance:{},coneCos:{},penumbraCos:{},decay:{}}},spotLightShadows:{value:[],properties:{shadowIntensity:1,shadowBias:{},shadowNormalBias:{},shadowRadius:{},shadowMapSize:{}}},spotLightMap:{value:[]},spotShadowMap:{value:[]},spotLightMatrix:{value:[]},pointLights:{value:[],properties:{color:{},position:{},decay:{},distance:{}}},pointLightShadows:{value:[],properties:{shadowIntensity:1,shadowBias:{},shadowNormalBias:{},shadowRadius:{},shadowMapSize:{},shadowCameraNear:{},shadowCameraFar:{}}},pointShadowMap:{value:[]},pointShadowMatrix:{value:[]},hemisphereLights:{value:[],properties:{direction:{},skyColor:{},groundColor:{}}},rectAreaLights:{value:[],properties:{color:{},position:{},width:{},height:{}}},ltc_1:{value:null},ltc_2:{value:null}},points:{diffuse:{value:new ve(16777215)},opacity:{value:1},size:{value:1},scale:{value:1},map:{value:null},alphaMap:{value:null},alphaMapTransform:{value:new Be},alphaTest:{value:0},uvTransform:{value:new Be}},sprite:{diffuse:{value:new ve(16777215)},opacity:{value:1},center:{value:new Xe(.5,.5)},rotation:{value:0},map:{value:null},mapTransform:{value:new Be},alphaMap:{value:null},alphaMapTransform:{value:new Be},alphaTest:{value:0}}},$t={basic:{uniforms:yt([he.common,he.specularmap,he.envmap,he.aomap,he.lightmap,he.fog]),vertexShader:Ve.meshbasic_vert,fragmentShader:Ve.meshbasic_frag},lambert:{uniforms:yt([he.common,he.specularmap,he.envmap,he.aomap,he.lightmap,he.emissivemap,he.bumpmap,he.normalmap,he.displacementmap,he.fog,he.lights,{emissive:{value:new ve(0)}}]),vertexShader:Ve.meshlambert_vert,fragmentShader:Ve.meshlambert_frag},phong:{uniforms:yt([he.common,he.specularmap,he.envmap,he.aomap,he.lightmap,he.emissivemap,he.bumpmap,he.normalmap,he.displacementmap,he.fog,he.lights,{emissive:{value:new ve(0)},specular:{value:new ve(1118481)},shininess:{value:30}}]),vertexShader:Ve.meshphong_vert,fragmentShader:Ve.meshphong_frag},standard:{uniforms:yt([he.common,he.envmap,he.aomap,he.lightmap,he.emissivemap,he.bumpmap,he.normalmap,he.displacementmap,he.roughnessmap,he.metalnessmap,he.fog,he.lights,{emissive:{value:new ve(0)},roughness:{value:1},metalness:{value:0},envMapIntensity:{value:1}}]),vertexShader:Ve.meshphysical_vert,fragmentShader:Ve.meshphysical_frag},toon:{uniforms:yt([he.common,he.aomap,he.lightmap,he.emissivemap,he.bumpmap,he.normalmap,he.displacementmap,he.gradientmap,he.fog,he.lights,{emissive:{value:new ve(0)}}]),vertexShader:Ve.meshtoon_vert,fragmentShader:Ve.meshtoon_frag},matcap:{uniforms:yt([he.common,he.bumpmap,he.normalmap,he.displacementmap,he.fog,{matcap:{value:null}}]),vertexShader:Ve.meshmatcap_vert,fragmentShader:Ve.meshmatcap_frag},points:{uniforms:yt([he.points,he.fog]),vertexShader:Ve.points_vert,fragmentShader:Ve.points_frag},dashed:{uniforms:yt([he.common,he.fog,{scale:{value:1},dashSize:{value:1},totalSize:{value:2}}]),vertexShader:Ve.linedashed_vert,fragmentShader:Ve.linedashed_frag},depth:{uniforms:yt([he.common,he.displacementmap]),vertexShader:Ve.depth_vert,fragmentShader:Ve.depth_frag},normal:{uniforms:yt([he.common,he.bumpmap,he.normalmap,he.displacementmap,{opacity:{value:1}}]),vertexShader:Ve.meshnormal_vert,fragmentShader:Ve.meshnormal_frag},sprite:{uniforms:yt([he.sprite,he.fog]),vertexShader:Ve.sprite_vert,fragmentShader:Ve.sprite_frag},background:{uniforms:{uvTransform:{value:new Be},t2D:{value:null},backgroundIntensity:{value:1}},vertexShader:Ve.background_vert,fragmentShader:Ve.background_frag},backgroundCube:{uniforms:{envMap:{value:null},flipEnvMap:{value:-1},backgroundBlurriness:{value:0},backgroundIntensity:{value:1},backgroundRotation:{value:new Be}},vertexShader:Ve.backgroundCube_vert,fragmentShader:Ve.backgroundCube_frag},cube:{uniforms:{tCube:{value:null},tFlip:{value:-1},opacity:{value:1}},vertexShader:Ve.cube_vert,fragmentShader:Ve.cube_frag},equirect:{uniforms:{tEquirect:{value:null}},vertexShader:Ve.equirect_vert,fragmentShader:Ve.equirect_frag},distanceRGBA:{uniforms:yt([he.common,he.displacementmap,{referencePosition:{value:new k},nearDistance:{value:1},farDistance:{value:1e3}}]),vertexShader:Ve.distanceRGBA_vert,fragmentShader:Ve.distanceRGBA_frag},shadow:{uniforms:yt([he.lights,he.fog,{color:{value:new ve(0)},opacity:{value:1}}]),vertexShader:Ve.shadow_vert,fragmentShader:Ve.shadow_frag}};$t.physical={uniforms:yt([$t.standard.uniforms,{clearcoat:{value:0},clearcoatMap:{value:null},clearcoatMapTransform:{value:new Be},clearcoatNormalMap:{value:null},clearcoatNormalMapTransform:{value:new Be},clearcoatNormalScale:{value:new Xe(1,1)},clearcoatRoughness:{value:0},clearcoatRoughnessMap:{value:null},clearcoatRoughnessMapTransform:{value:new Be},dispersion:{value:0},iridescence:{value:0},iridescenceMap:{value:null},iridescenceMapTransform:{value:new Be},iridescenceIOR:{value:1.3},iridescenceThicknessMinimum:{value:100},iridescenceThicknessMaximum:{value:400},iridescenceThicknessMap:{value:null},iridescenceThicknessMapTransform:{value:new Be},sheen:{value:0},sheenColor:{value:new ve(0)},sheenColorMap:{value:null},sheenColorMapTransform:{value:new Be},sheenRoughness:{value:1},sheenRoughnessMap:{value:null},sheenRoughnessMapTransform:{value:new Be},transmission:{value:0},transmissionMap:{value:null},transmissionMapTransform:{value:new Be},transmissionSamplerSize:{value:new Xe},transmissionSamplerMap:{value:null},thickness:{value:0},thicknessMap:{value:null},thicknessMapTransform:{value:new Be},attenuationDistance:{value:0},attenuationColor:{value:new ve(0)},specularColor:{value:new ve(1,1,1)},specularColorMap:{value:null},specularColorMapTransform:{value:new Be},specularIntensity:{value:1},specularIntensityMap:{value:null},specularIntensityMapTransform:{value:new Be},anisotropyVector:{value:new Xe},anisotropyMap:{value:null},anisotropyMapTransform:{value:new Be}}]),vertexShader:Ve.meshphysical_vert,fragmentShader:Ve.meshphysical_frag};const _r={r:0,b:0,g:0},Un=new Jt,af=new at;function sf(n,e,t,i,r,a,s){const o=new ve(0);let c=a===!0?0:1,l,d,h=null,f=0,m=null;function g(b){let S=b.isScene===!0?b.background:null;return S&&S.isTexture&&(S=(b.backgroundBlurriness>0?t:e).get(S)),S}function _(b){let S=!1;const T=g(b);T===null?u(o,c):T&&T.isColor&&(u(T,1),S=!0);const y=n.xr.getEnvironmentBlendMode();y==="additive"?i.buffers.color.setClear(0,0,0,1,s):y==="alpha-blend"&&i.buffers.color.setClear(0,0,0,0,s),(n.autoClear||S)&&(i.buffers.depth.setTest(!0),i.buffers.depth.setMask(!0),i.buffers.color.setMask(!0),n.clear(n.autoClearColor,n.autoClearDepth,n.autoClearStencil))}function p(b,S){const T=g(S);T&&(T.isCubeTexture||T.mapping===Or)?(d===void 0&&(d=new it(new hn(1,1,1),new wn({name:"BackgroundCubeMaterial",uniforms:Ai($t.backgroundCube.uniforms),vertexShader:$t.backgroundCube.vertexShader,fragmentShader:$t.backgroundCube.fragmentShader,side:Rt,depthTest:!1,depthWrite:!1,fog:!1})),d.geometry.deleteAttribute("normal"),d.geometry.deleteAttribute("uv"),d.onBeforeRender=function(y,A,D){this.matrixWorld.copyPosition(D.matrixWorld)},Object.defineProperty(d.material,"envMap",{get:function(){return this.uniforms.envMap.value}}),r.update(d)),Un.copy(S.backgroundRotation),Un.x*=-1,Un.y*=-1,Un.z*=-1,T.isCubeTexture&&T.isRenderTargetTexture===!1&&(Un.y*=-1,Un.z*=-1),d.material.uniforms.envMap.value=T,d.material.uniforms.flipEnvMap.value=T.isCubeTexture&&T.isRenderTargetTexture===!1?-1:1,d.material.uniforms.backgroundBlurriness.value=S.backgroundBlurriness,d.material.uniforms.backgroundIntensity.value=S.backgroundIntensity,d.material.uniforms.backgroundRotation.value.setFromMatrix4(af.makeRotationFromEuler(Un)),d.material.toneMapped=Ke.getTransfer(T.colorSpace)!==et,(h!==T||f!==T.version||m!==n.toneMapping)&&(d.material.needsUpdate=!0,h=T,f=T.version,m=n.toneMapping),d.layers.enableAll(),b.unshift(d,d.geometry,d.material,0,0,null)):T&&T.isTexture&&(l===void 0&&(l=new it(new Wi(2,2),new wn({name:"BackgroundMaterial",uniforms:Ai($t.background.uniforms),vertexShader:$t.background.vertexShader,fragmentShader:$t.background.fragmentShader,side:An,depthTest:!1,depthWrite:!1,fog:!1})),l.geometry.deleteAttribute("normal"),Object.defineProperty(l.material,"map",{get:function(){return this.uniforms.t2D.value}}),r.update(l)),l.material.uniforms.t2D.value=T,l.material.uniforms.backgroundIntensity.value=S.backgroundIntensity,l.material.toneMapped=Ke.getTransfer(T.colorSpace)!==et,T.matrixAutoUpdate===!0&&T.updateMatrix(),l.material.uniforms.uvTransform.value.copy(T.matrix),(h!==T||f!==T.version||m!==n.toneMapping)&&(l.material.needsUpdate=!0,h=T,f=T.version,m=n.toneMapping),l.layers.enableAll(),b.unshift(l,l.geometry,l.material,0,0,null))}function u(b,S){b.getRGB(_r,Tc(n)),i.buffers.color.setClear(_r.r,_r.g,_r.b,S,s)}function w(){d!==void 0&&(d.geometry.dispose(),d.material.dispose(),d=void 0),l!==void 0&&(l.geometry.dispose(),l.material.dispose(),l=void 0)}return{getClearColor:function(){return o},setClearColor:function(b,S=1){o.set(b),c=S,u(o,c)},getClearAlpha:function(){return c},setClearAlpha:function(b){c=b,u(o,c)},render:_,addToRenderList:p,dispose:w}}function of(n,e){const t=n.getParameter(n.MAX_VERTEX_ATTRIBS),i={},r=f(null);let a=r,s=!1;function o(v,C,F,N,P){let U=!1;const z=h(N,F,C);a!==z&&(a=z,l(a.object)),U=m(v,N,F,P),U&&g(v,N,F,P),P!==null&&e.update(P,n.ELEMENT_ARRAY_BUFFER),(U||s)&&(s=!1,S(v,C,F,N),P!==null&&n.bindBuffer(n.ELEMENT_ARRAY_BUFFER,e.get(P).buffer))}function c(){return n.createVertexArray()}function l(v){return n.bindVertexArray(v)}function d(v){return n.deleteVertexArray(v)}function h(v,C,F){const N=F.wireframe===!0;let P=i[v.id];P===void 0&&(P={},i[v.id]=P);let U=P[C.id];U===void 0&&(U={},P[C.id]=U);let z=U[N];return z===void 0&&(z=f(c()),U[N]=z),z}function f(v){const C=[],F=[],N=[];for(let P=0;P<t;P++)C[P]=0,F[P]=0,N[P]=0;return{geometry:null,program:null,wireframe:!1,newAttributes:C,enabledAttributes:F,attributeDivisors:N,object:v,attributes:{},index:null}}function m(v,C,F,N){const P=a.attributes,U=C.attributes;let z=0;const H=F.getAttributes();for(const I in H)if(H[I].location>=0){const q=P[I];let oe=U[I];if(oe===void 0&&(I==="instanceMatrix"&&v.instanceMatrix&&(oe=v.instanceMatrix),I==="instanceColor"&&v.instanceColor&&(oe=v.instanceColor)),q===void 0||q.attribute!==oe||oe&&q.data!==oe.data)return!0;z++}return a.attributesNum!==z||a.index!==N}function g(v,C,F,N){const P={},U=C.attributes;let z=0;const H=F.getAttributes();for(const I in H)if(H[I].location>=0){let q=U[I];q===void 0&&(I==="instanceMatrix"&&v.instanceMatrix&&(q=v.instanceMatrix),I==="instanceColor"&&v.instanceColor&&(q=v.instanceColor));const oe={};oe.attribute=q,q&&q.data&&(oe.data=q.data),P[I]=oe,z++}a.attributes=P,a.attributesNum=z,a.index=N}function _(){const v=a.newAttributes;for(let C=0,F=v.length;C<F;C++)v[C]=0}function p(v){u(v,0)}function u(v,C){const F=a.newAttributes,N=a.enabledAttributes,P=a.attributeDivisors;F[v]=1,N[v]===0&&(n.enableVertexAttribArray(v),N[v]=1),P[v]!==C&&(n.vertexAttribDivisor(v,C),P[v]=C)}function w(){const v=a.newAttributes,C=a.enabledAttributes;for(let F=0,N=C.length;F<N;F++)C[F]!==v[F]&&(n.disableVertexAttribArray(F),C[F]=0)}function b(v,C,F,N,P,U,z){z===!0?n.vertexAttribIPointer(v,C,F,P,U):n.vertexAttribPointer(v,C,F,N,P,U)}function S(v,C,F,N){_();const P=N.attributes,U=F.getAttributes(),z=C.defaultAttributeValues;for(const H in U){const I=U[H];if(I.location>=0){let G=P[H];if(G===void 0&&(H==="instanceMatrix"&&v.instanceMatrix&&(G=v.instanceMatrix),H==="instanceColor"&&v.instanceColor&&(G=v.instanceColor)),G!==void 0){const q=G.normalized,oe=G.itemSize,le=e.get(G);if(le===void 0)continue;const Re=le.buffer,Y=le.type,te=le.bytesPerElement,de=Y===n.INT||Y===n.UNSIGNED_INT||G.gpuType===Ts;if(G.isInterleavedBufferAttribute){const se=G.data,Q=se.stride,ge=G.offset;if(se.isInstancedInterleavedBuffer){for(let ue=0;ue<I.locationSize;ue++)u(I.location+ue,se.meshPerAttribute);v.isInstancedMesh!==!0&&N._maxInstanceCount===void 0&&(N._maxInstanceCount=se.meshPerAttribute*se.count)}else for(let ue=0;ue<I.locationSize;ue++)p(I.location+ue);n.bindBuffer(n.ARRAY_BUFFER,Re);for(let ue=0;ue<I.locationSize;ue++)b(I.location+ue,oe/I.locationSize,Y,q,Q*te,(ge+oe/I.locationSize*ue)*te,de)}else{if(G.isInstancedBufferAttribute){for(let se=0;se<I.locationSize;se++)u(I.location+se,G.meshPerAttribute);v.isInstancedMesh!==!0&&N._maxInstanceCount===void 0&&(N._maxInstanceCount=G.meshPerAttribute*G.count)}else for(let se=0;se<I.locationSize;se++)p(I.location+se);n.bindBuffer(n.ARRAY_BUFFER,Re);for(let se=0;se<I.locationSize;se++)b(I.location+se,oe/I.locationSize,Y,q,oe*te,oe/I.locationSize*se*te,de)}}else if(z!==void 0){const q=z[H];if(q!==void 0)switch(q.length){case 2:n.vertexAttrib2fv(I.location,q);break;case 3:n.vertexAttrib3fv(I.location,q);break;case 4:n.vertexAttrib4fv(I.location,q);break;default:n.vertexAttrib1fv(I.location,q)}}}}w()}function T(){D();for(const v in i){const C=i[v];for(const F in C){const N=C[F];for(const P in N)d(N[P].object),delete N[P];delete C[F]}delete i[v]}}function y(v){if(i[v.id]===void 0)return;const C=i[v.id];for(const F in C){const N=C[F];for(const P in N)d(N[P].object),delete N[P];delete C[F]}delete i[v.id]}function A(v){for(const C in i){const F=i[C];if(F[v.id]===void 0)continue;const N=F[v.id];for(const P in N)d(N[P].object),delete N[P];delete F[v.id]}}function D(){x(),s=!0,a!==r&&(a=r,l(a.object))}function x(){r.geometry=null,r.program=null,r.wireframe=!1}return{setup:o,reset:D,resetDefaultState:x,dispose:T,releaseStatesOfGeometry:y,releaseStatesOfProgram:A,initAttributes:_,enableAttribute:p,disableUnusedAttributes:w}}function cf(n,e,t){let i;function r(l){i=l}function a(l,d){n.drawArrays(i,l,d),t.update(d,i,1)}function s(l,d,h){h!==0&&(n.drawArraysInstanced(i,l,d,h),t.update(d,i,h))}function o(l,d,h){if(h===0)return;e.get("WEBGL_multi_draw").multiDrawArraysWEBGL(i,l,0,d,0,h);let m=0;for(let g=0;g<h;g++)m+=d[g];t.update(m,i,1)}function c(l,d,h,f){if(h===0)return;const m=e.get("WEBGL_multi_draw");if(m===null)for(let g=0;g<l.length;g++)s(l[g],d[g],f[g]);else{m.multiDrawArraysInstancedWEBGL(i,l,0,d,0,f,0,h);let g=0;for(let _=0;_<h;_++)g+=d[_]*f[_];t.update(g,i,1)}}this.setMode=r,this.render=a,this.renderInstances=s,this.renderMultiDraw=o,this.renderMultiDrawInstances=c}function lf(n,e,t,i){let r;function a(){if(r!==void 0)return r;if(e.has("EXT_texture_filter_anisotropic")===!0){const A=e.get("EXT_texture_filter_anisotropic");r=n.getParameter(A.MAX_TEXTURE_MAX_ANISOTROPY_EXT)}else r=0;return r}function s(A){return!(A!==Yt&&i.convert(A)!==n.getParameter(n.IMPLEMENTATION_COLOR_READ_FORMAT))}function o(A){const D=A===Bi&&(e.has("EXT_color_buffer_half_float")||e.has("EXT_color_buffer_float"));return!(A!==pn&&i.convert(A)!==n.getParameter(n.IMPLEMENTATION_COLOR_READ_TYPE)&&A!==un&&!D)}function c(A){if(A==="highp"){if(n.getShaderPrecisionFormat(n.VERTEX_SHADER,n.HIGH_FLOAT).precision>0&&n.getShaderPrecisionFormat(n.FRAGMENT_SHADER,n.HIGH_FLOAT).precision>0)return"highp";A="mediump"}return A==="mediump"&&n.getShaderPrecisionFormat(n.VERTEX_SHADER,n.MEDIUM_FLOAT).precision>0&&n.getShaderPrecisionFormat(n.FRAGMENT_SHADER,n.MEDIUM_FLOAT).precision>0?"mediump":"lowp"}let l=t.precision!==void 0?t.precision:"highp";const d=c(l);d!==l&&(console.warn("THREE.WebGLRenderer:",l,"not supported, using",d,"instead."),l=d);const h=t.logarithmicDepthBuffer===!0,f=t.reverseDepthBuffer===!0&&e.has("EXT_clip_control"),m=n.getParameter(n.MAX_TEXTURE_IMAGE_UNITS),g=n.getParameter(n.MAX_VERTEX_TEXTURE_IMAGE_UNITS),_=n.getParameter(n.MAX_TEXTURE_SIZE),p=n.getParameter(n.MAX_CUBE_MAP_TEXTURE_SIZE),u=n.getParameter(n.MAX_VERTEX_ATTRIBS),w=n.getParameter(n.MAX_VERTEX_UNIFORM_VECTORS),b=n.getParameter(n.MAX_VARYING_VECTORS),S=n.getParameter(n.MAX_FRAGMENT_UNIFORM_VECTORS),T=g>0,y=n.getParameter(n.MAX_SAMPLES);return{isWebGL2:!0,getMaxAnisotropy:a,getMaxPrecision:c,textureFormatReadable:s,textureTypeReadable:o,precision:l,logarithmicDepthBuffer:h,reverseDepthBuffer:f,maxTextures:m,maxVertexTextures:g,maxTextureSize:_,maxCubemapSize:p,maxAttributes:u,maxVertexUniforms:w,maxVaryings:b,maxFragmentUniforms:S,vertexTextures:T,maxSamples:y}}function uf(n){const e=this;let t=null,i=0,r=!1,a=!1;const s=new zn,o=new Be,c={value:null,needsUpdate:!1};this.uniform=c,this.numPlanes=0,this.numIntersection=0,this.init=function(h,f){const m=h.length!==0||f||i!==0||r;return r=f,i=h.length,m},this.beginShadows=function(){a=!0,d(null)},this.endShadows=function(){a=!1},this.setGlobalState=function(h,f){t=d(h,f,0)},this.setState=function(h,f,m){const g=h.clippingPlanes,_=h.clipIntersection,p=h.clipShadows,u=n.get(h);if(!r||g===null||g.length===0||a&&!p)a?d(null):l();else{const w=a?0:i,b=w*4;let S=u.clippingState||null;c.value=S,S=d(g,f,b,m);for(let T=0;T!==b;++T)S[T]=t[T];u.clippingState=S,this.numIntersection=_?this.numPlanes:0,this.numPlanes+=w}};function l(){c.value!==t&&(c.value=t,c.needsUpdate=i>0),e.numPlanes=i,e.numIntersection=0}function d(h,f,m,g){const _=h!==null?h.length:0;let p=null;if(_!==0){if(p=c.value,g!==!0||p===null){const u=m+_*4,w=f.matrixWorldInverse;o.getNormalMatrix(w),(p===null||p.length<u)&&(p=new Float32Array(u));for(let b=0,S=m;b!==_;++b,S+=4)s.copy(h[b]).applyMatrix4(w,o),s.normal.toArray(p,S),p[S+3]=s.constant}c.value=p,c.needsUpdate=!0}return e.numPlanes=_,e.numIntersection=0,p}}function df(n){let e=new WeakMap;function t(s,o){return o===ka?s.mapping=Si:o===Oa&&(s.mapping=Ei),s}function i(s){if(s&&s.isTexture){const o=s.mapping;if(o===ka||o===Oa)if(e.has(s)){const c=e.get(s).texture;return t(c,s.mapping)}else{const c=s.image;if(c&&c.height>0){const l=new hu(c.height);return l.fromEquirectangularTexture(n,s),e.set(s,l),s.addEventListener("dispose",r),t(l.texture,s.mapping)}else return null}}return s}function r(s){const o=s.target;o.removeEventListener("dispose",r);const c=e.get(o);c!==void 0&&(e.delete(o),c.dispose())}function a(){e=new WeakMap}return{get:i,dispose:a}}const fi=4,Co=[.125,.215,.35,.446,.526,.582],Vn=20,xa=new Pc,Po=new ve;let Ma=null,Sa=0,Ea=0,ya=!1;const kn=(1+Math.sqrt(5))/2,ui=1/kn,Do=[new k(-kn,ui,0),new k(kn,ui,0),new k(-ui,0,kn),new k(ui,0,kn),new k(0,kn,-ui),new k(0,kn,ui),new k(-1,1,-1),new k(1,1,-1),new k(-1,1,1),new k(1,1,1)],hf=new k;class Lo{constructor(e){this._renderer=e,this._pingPongRenderTarget=null,this._lodMax=0,this._cubeSize=0,this._lodPlanes=[],this._sizeLods=[],this._sigmas=[],this._blurMaterial=null,this._cubemapMaterial=null,this._equirectMaterial=null,this._compileMaterial(this._blurMaterial)}fromScene(e,t=0,i=.1,r=100,a={}){const{size:s=256,position:o=hf}=a;Ma=this._renderer.getRenderTarget(),Sa=this._renderer.getActiveCubeFace(),Ea=this._renderer.getActiveMipmapLevel(),ya=this._renderer.xr.enabled,this._renderer.xr.enabled=!1,this._setSize(s);const c=this._allocateTargets();return c.depthBuffer=!0,this._sceneToCubeUV(e,i,r,c,o),t>0&&this._blur(c,0,0,t),this._applyPMREM(c),this._cleanup(c),c}fromEquirectangular(e,t=null){return this._fromTexture(e,t)}fromCubemap(e,t=null){return this._fromTexture(e,t)}compileCubemapShader(){this._cubemapMaterial===null&&(this._cubemapMaterial=No(),this._compileMaterial(this._cubemapMaterial))}compileEquirectangularShader(){this._equirectMaterial===null&&(this._equirectMaterial=Uo(),this._compileMaterial(this._equirectMaterial))}dispose(){this._dispose(),this._cubemapMaterial!==null&&this._cubemapMaterial.dispose(),this._equirectMaterial!==null&&this._equirectMaterial.dispose()}_setSize(e){this._lodMax=Math.floor(Math.log2(e)),this._cubeSize=Math.pow(2,this._lodMax)}_dispose(){this._blurMaterial!==null&&this._blurMaterial.dispose(),this._pingPongRenderTarget!==null&&this._pingPongRenderTarget.dispose();for(let e=0;e<this._lodPlanes.length;e++)this._lodPlanes[e].dispose()}_cleanup(e){this._renderer.setRenderTarget(Ma,Sa,Ea),this._renderer.xr.enabled=ya,e.scissorTest=!1,vr(e,0,0,e.width,e.height)}_fromTexture(e,t){e.mapping===Si||e.mapping===Ei?this._setSize(e.image.length===0?16:e.image[0].width||e.image[0].image.width):this._setSize(e.image.width/4),Ma=this._renderer.getRenderTarget(),Sa=this._renderer.getActiveCubeFace(),Ea=this._renderer.getActiveMipmapLevel(),ya=this._renderer.xr.enabled,this._renderer.xr.enabled=!1;const i=t||this._allocateTargets();return this._textureToCubeUV(e,i),this._applyPMREM(i),this._cleanup(i),i}_allocateTargets(){const e=3*Math.max(this._cubeSize,112),t=4*this._cubeSize,i={magFilter:Kt,minFilter:Kt,generateMipmaps:!1,type:Bi,format:Yt,colorSpace:Ti,depthBuffer:!1},r=Io(e,t,i);if(this._pingPongRenderTarget===null||this._pingPongRenderTarget.width!==e||this._pingPongRenderTarget.height!==t){this._pingPongRenderTarget!==null&&this._dispose(),this._pingPongRenderTarget=Io(e,t,i);const{_lodMax:a}=this;({sizeLods:this._sizeLods,lodPlanes:this._lodPlanes,sigmas:this._sigmas}=ff(a)),this._blurMaterial=pf(a,e,t)}return r}_compileMaterial(e){const t=new it(this._lodPlanes[0],e);this._renderer.compile(t,xa)}_sceneToCubeUV(e,t,i,r,a){const c=new zt(90,1,t,i),l=[1,-1,1,1,1,1],d=[1,1,1,-1,-1,-1],h=this._renderer,f=h.autoClear,m=h.toneMapping;h.getClearColor(Po),h.toneMapping=Tn,h.autoClear=!1;const g=new Hr({name:"PMREM.Background",side:Rt,depthWrite:!1,depthTest:!1}),_=new it(new hn,g);let p=!1;const u=e.background;u?u.isColor&&(g.color.copy(u),e.background=null,p=!0):(g.color.copy(Po),p=!0);for(let w=0;w<6;w++){const b=w%3;b===0?(c.up.set(0,l[w],0),c.position.set(a.x,a.y,a.z),c.lookAt(a.x+d[w],a.y,a.z)):b===1?(c.up.set(0,0,l[w]),c.position.set(a.x,a.y,a.z),c.lookAt(a.x,a.y+d[w],a.z)):(c.up.set(0,l[w],0),c.position.set(a.x,a.y,a.z),c.lookAt(a.x,a.y,a.z+d[w]));const S=this._cubeSize;vr(r,b*S,w>2?S:0,S,S),h.setRenderTarget(r),p&&h.render(_,c),h.render(e,c)}_.geometry.dispose(),_.material.dispose(),h.toneMapping=m,h.autoClear=f,e.background=u}_textureToCubeUV(e,t){const i=this._renderer,r=e.mapping===Si||e.mapping===Ei;r?(this._cubemapMaterial===null&&(this._cubemapMaterial=No()),this._cubemapMaterial.uniforms.flipEnvMap.value=e.isRenderTargetTexture===!1?-1:1):this._equirectMaterial===null&&(this._equirectMaterial=Uo());const a=r?this._cubemapMaterial:this._equirectMaterial,s=new it(this._lodPlanes[0],a),o=a.uniforms;o.envMap.value=e;const c=this._cubeSize;vr(t,0,0,3*c,2*c),i.setRenderTarget(t),i.render(s,xa)}_applyPMREM(e){const t=this._renderer,i=t.autoClear;t.autoClear=!1;const r=this._lodPlanes.length;for(let a=1;a<r;a++){const s=Math.sqrt(this._sigmas[a]*this._sigmas[a]-this._sigmas[a-1]*this._sigmas[a-1]),o=Do[(r-a-1)%Do.length];this._blur(e,a-1,a,s,o)}t.autoClear=i}_blur(e,t,i,r,a){const s=this._pingPongRenderTarget;this._halfBlur(e,s,t,i,r,"latitudinal",a),this._halfBlur(s,e,i,i,r,"longitudinal",a)}_halfBlur(e,t,i,r,a,s,o){const c=this._renderer,l=this._blurMaterial;s!=="latitudinal"&&s!=="longitudinal"&&console.error("blur direction must be either latitudinal or longitudinal!");const d=3,h=new it(this._lodPlanes[r],l),f=l.uniforms,m=this._sizeLods[i]-1,g=isFinite(a)?Math.PI/(2*m):2*Math.PI/(2*Vn-1),_=a/g,p=isFinite(a)?1+Math.floor(d*_):Vn;p>Vn&&console.warn(`sigmaRadians, ${a}, is too large and will clip, as it requested ${p} samples when the maximum is set to ${Vn}`);const u=[];let w=0;for(let A=0;A<Vn;++A){const D=A/_,x=Math.exp(-D*D/2);u.push(x),A===0?w+=x:A<p&&(w+=2*x)}for(let A=0;A<u.length;A++)u[A]=u[A]/w;f.envMap.value=e.texture,f.samples.value=p,f.weights.value=u,f.latitudinal.value=s==="latitudinal",o&&(f.poleAxis.value=o);const{_lodMax:b}=this;f.dTheta.value=g,f.mipInt.value=b-i;const S=this._sizeLods[r],T=3*S*(r>b-fi?r-b+fi:0),y=4*(this._cubeSize-S);vr(t,T,y,3*S,2*S),c.setRenderTarget(t),c.render(h,xa)}}function ff(n){const e=[],t=[],i=[];let r=n;const a=n-fi+1+Co.length;for(let s=0;s<a;s++){const o=Math.pow(2,r);t.push(o);let c=1/o;s>n-fi?c=Co[s-n+fi-1]:s===0&&(c=0),i.push(c);const l=1/(o-2),d=-l,h=1+l,f=[d,d,h,d,h,h,d,d,h,h,d,h],m=6,g=6,_=3,p=2,u=1,w=new Float32Array(_*g*m),b=new Float32Array(p*g*m),S=new Float32Array(u*g*m);for(let y=0;y<m;y++){const A=y%3*2/3-1,D=y>2?0:-1,x=[A,D,0,A+2/3,D,0,A+2/3,D+1,0,A,D,0,A+2/3,D+1,0,A,D+1,0];w.set(x,_*g*y),b.set(f,p*g*y);const v=[y,y,y,y,y,y];S.set(v,u*g*y)}const T=new st;T.setAttribute("position",new Zt(w,_)),T.setAttribute("uv",new Zt(b,p)),T.setAttribute("faceIndex",new Zt(S,u)),e.push(T),r>fi&&r--}return{lodPlanes:e,sizeLods:t,sigmas:i}}function Io(n,e,t){const i=new qn(n,e,t);return i.texture.mapping=Or,i.texture.name="PMREM.cubeUv",i.scissorTest=!0,i}function vr(n,e,t,i,r){n.viewport.set(e,t,i,r),n.scissor.set(e,t,i,r)}function pf(n,e,t){const i=new Float32Array(Vn),r=new k(0,1,0);return new wn({name:"SphericalGaussianBlur",defines:{n:Vn,CUBEUV_TEXEL_WIDTH:1/e,CUBEUV_TEXEL_HEIGHT:1/t,CUBEUV_MAX_MIP:`${n}.0`},uniforms:{envMap:{value:null},samples:{value:1},weights:{value:i},latitudinal:{value:!1},dTheta:{value:0},mipInt:{value:0},poleAxis:{value:r}},vertexShader:zs(),fragmentShader:`

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
		`,blending:bn,depthTest:!1,depthWrite:!1})}function Uo(){return new wn({name:"EquirectangularToCubeUV",uniforms:{envMap:{value:null}},vertexShader:zs(),fragmentShader:`

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
		`,blending:bn,depthTest:!1,depthWrite:!1})}function No(){return new wn({name:"CubemapToCubeUV",uniforms:{envMap:{value:null},flipEnvMap:{value:-1}},vertexShader:zs(),fragmentShader:`

			precision mediump float;
			precision mediump int;

			uniform float flipEnvMap;

			varying vec3 vOutputDirection;

			uniform samplerCube envMap;

			void main() {

				gl_FragColor = textureCube( envMap, vec3( flipEnvMap * vOutputDirection.x, vOutputDirection.yz ) );

			}
		`,blending:bn,depthTest:!1,depthWrite:!1})}function zs(){return`

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
	`}function mf(n){let e=new WeakMap,t=null;function i(o){if(o&&o.isTexture){const c=o.mapping,l=c===ka||c===Oa,d=c===Si||c===Ei;if(l||d){let h=e.get(o);const f=h!==void 0?h.texture.pmremVersion:0;if(o.isRenderTargetTexture&&o.pmremVersion!==f)return t===null&&(t=new Lo(n)),h=l?t.fromEquirectangular(o,h):t.fromCubemap(o,h),h.texture.pmremVersion=o.pmremVersion,e.set(o,h),h.texture;if(h!==void 0)return h.texture;{const m=o.image;return l&&m&&m.height>0||d&&m&&r(m)?(t===null&&(t=new Lo(n)),h=l?t.fromEquirectangular(o):t.fromCubemap(o),h.texture.pmremVersion=o.pmremVersion,e.set(o,h),o.addEventListener("dispose",a),h.texture):null}}}return o}function r(o){let c=0;const l=6;for(let d=0;d<l;d++)o[d]!==void 0&&c++;return c===l}function a(o){const c=o.target;c.removeEventListener("dispose",a);const l=e.get(c);l!==void 0&&(e.delete(c),l.dispose())}function s(){e=new WeakMap,t!==null&&(t.dispose(),t=null)}return{get:i,dispose:s}}function gf(n){const e={};function t(i){if(e[i]!==void 0)return e[i];let r;switch(i){case"WEBGL_depth_texture":r=n.getExtension("WEBGL_depth_texture")||n.getExtension("MOZ_WEBGL_depth_texture")||n.getExtension("WEBKIT_WEBGL_depth_texture");break;case"EXT_texture_filter_anisotropic":r=n.getExtension("EXT_texture_filter_anisotropic")||n.getExtension("MOZ_EXT_texture_filter_anisotropic")||n.getExtension("WEBKIT_EXT_texture_filter_anisotropic");break;case"WEBGL_compressed_texture_s3tc":r=n.getExtension("WEBGL_compressed_texture_s3tc")||n.getExtension("MOZ_WEBGL_compressed_texture_s3tc")||n.getExtension("WEBKIT_WEBGL_compressed_texture_s3tc");break;case"WEBGL_compressed_texture_pvrtc":r=n.getExtension("WEBGL_compressed_texture_pvrtc")||n.getExtension("WEBKIT_WEBGL_compressed_texture_pvrtc");break;default:r=n.getExtension(i)}return e[i]=r,r}return{has:function(i){return t(i)!==null},init:function(){t("EXT_color_buffer_float"),t("WEBGL_clip_cull_distance"),t("OES_texture_float_linear"),t("EXT_color_buffer_half_float"),t("WEBGL_multisampled_render_to_texture"),t("WEBGL_render_shared_exponent")},get:function(i){const r=t(i);return r===null&&Fn("THREE.WebGLRenderer: "+i+" extension not supported."),r}}}function _f(n,e,t,i){const r={},a=new WeakMap;function s(h){const f=h.target;f.index!==null&&e.remove(f.index);for(const g in f.attributes)e.remove(f.attributes[g]);f.removeEventListener("dispose",s),delete r[f.id];const m=a.get(f);m&&(e.remove(m),a.delete(f)),i.releaseStatesOfGeometry(f),f.isInstancedBufferGeometry===!0&&delete f._maxInstanceCount,t.memory.geometries--}function o(h,f){return r[f.id]===!0||(f.addEventListener("dispose",s),r[f.id]=!0,t.memory.geometries++),f}function c(h){const f=h.attributes;for(const m in f)e.update(f[m],n.ARRAY_BUFFER)}function l(h){const f=[],m=h.index,g=h.attributes.position;let _=0;if(m!==null){const w=m.array;_=m.version;for(let b=0,S=w.length;b<S;b+=3){const T=w[b+0],y=w[b+1],A=w[b+2];f.push(T,y,y,A,A,T)}}else if(g!==void 0){const w=g.array;_=g.version;for(let b=0,S=w.length/3-1;b<S;b+=3){const T=b+0,y=b+1,A=b+2;f.push(T,y,y,A,A,T)}}else return;const p=new(Mc(f)?bc:yc)(f,1);p.version=_;const u=a.get(h);u&&e.remove(u),a.set(h,p)}function d(h){const f=a.get(h);if(f){const m=h.index;m!==null&&f.version<m.version&&l(h)}else l(h);return a.get(h)}return{get:o,update:c,getWireframeAttribute:d}}function vf(n,e,t){let i;function r(f){i=f}let a,s;function o(f){a=f.type,s=f.bytesPerElement}function c(f,m){n.drawElements(i,m,a,f*s),t.update(m,i,1)}function l(f,m,g){g!==0&&(n.drawElementsInstanced(i,m,a,f*s,g),t.update(m,i,g))}function d(f,m,g){if(g===0)return;e.get("WEBGL_multi_draw").multiDrawElementsWEBGL(i,m,0,a,f,0,g);let p=0;for(let u=0;u<g;u++)p+=m[u];t.update(p,i,1)}function h(f,m,g,_){if(g===0)return;const p=e.get("WEBGL_multi_draw");if(p===null)for(let u=0;u<f.length;u++)l(f[u]/s,m[u],_[u]);else{p.multiDrawElementsInstancedWEBGL(i,m,0,a,f,0,_,0,g);let u=0;for(let w=0;w<g;w++)u+=m[w]*_[w];t.update(u,i,1)}}this.setMode=r,this.setIndex=o,this.render=c,this.renderInstances=l,this.renderMultiDraw=d,this.renderMultiDrawInstances=h}function xf(n){const e={geometries:0,textures:0},t={frame:0,calls:0,triangles:0,points:0,lines:0};function i(a,s,o){switch(t.calls++,s){case n.TRIANGLES:t.triangles+=o*(a/3);break;case n.LINES:t.lines+=o*(a/2);break;case n.LINE_STRIP:t.lines+=o*(a-1);break;case n.LINE_LOOP:t.lines+=o*a;break;case n.POINTS:t.points+=o*a;break;default:console.error("THREE.WebGLInfo: Unknown draw mode:",s);break}}function r(){t.calls=0,t.triangles=0,t.points=0,t.lines=0}return{memory:e,render:t,programs:null,autoReset:!0,reset:r,update:i}}function Mf(n,e,t){const i=new WeakMap,r=new lt;function a(s,o,c){const l=s.morphTargetInfluences,d=o.morphAttributes.position||o.morphAttributes.normal||o.morphAttributes.color,h=d!==void 0?d.length:0;let f=i.get(o);if(f===void 0||f.count!==h){let x=function(){A.dispose(),i.delete(o),o.removeEventListener("dispose",x)};f!==void 0&&f.texture.dispose();const m=o.morphAttributes.position!==void 0,g=o.morphAttributes.normal!==void 0,_=o.morphAttributes.color!==void 0,p=o.morphAttributes.position||[],u=o.morphAttributes.normal||[],w=o.morphAttributes.color||[];let b=0;m===!0&&(b=1),g===!0&&(b=2),_===!0&&(b=3);let S=o.attributes.position.count*b,T=1;S>e.maxTextureSize&&(T=Math.ceil(S/e.maxTextureSize),S=e.maxTextureSize);const y=new Float32Array(S*T*4*h),A=new Sc(y,S,T,h);A.type=un,A.needsUpdate=!0;const D=b*4;for(let v=0;v<h;v++){const C=p[v],F=u[v],N=w[v],P=S*T*4*v;for(let U=0;U<C.count;U++){const z=U*D;m===!0&&(r.fromBufferAttribute(C,U),y[P+z+0]=r.x,y[P+z+1]=r.y,y[P+z+2]=r.z,y[P+z+3]=0),g===!0&&(r.fromBufferAttribute(F,U),y[P+z+4]=r.x,y[P+z+5]=r.y,y[P+z+6]=r.z,y[P+z+7]=0),_===!0&&(r.fromBufferAttribute(N,U),y[P+z+8]=r.x,y[P+z+9]=r.y,y[P+z+10]=r.z,y[P+z+11]=N.itemSize===4?r.w:1)}}f={count:h,texture:A,size:new Xe(S,T)},i.set(o,f),o.addEventListener("dispose",x)}if(s.isInstancedMesh===!0&&s.morphTexture!==null)c.getUniforms().setValue(n,"morphTexture",s.morphTexture,t);else{let m=0;for(let _=0;_<l.length;_++)m+=l[_];const g=o.morphTargetsRelative?1:1-m;c.getUniforms().setValue(n,"morphTargetBaseInfluence",g),c.getUniforms().setValue(n,"morphTargetInfluences",l)}c.getUniforms().setValue(n,"morphTargetsTexture",f.texture,t),c.getUniforms().setValue(n,"morphTargetsTextureSize",f.size)}return{update:a}}function Sf(n,e,t,i){let r=new WeakMap;function a(c){const l=i.render.frame,d=c.geometry,h=e.get(c,d);if(r.get(h)!==l&&(e.update(h),r.set(h,l)),c.isInstancedMesh&&(c.hasEventListener("dispose",o)===!1&&c.addEventListener("dispose",o),r.get(c)!==l&&(t.update(c.instanceMatrix,n.ARRAY_BUFFER),c.instanceColor!==null&&t.update(c.instanceColor,n.ARRAY_BUFFER),r.set(c,l))),c.isSkinnedMesh){const f=c.skeleton;r.get(f)!==l&&(f.update(),r.set(f,l))}return h}function s(){r=new WeakMap}function o(c){const l=c.target;l.removeEventListener("dispose",o),t.remove(l.instanceMatrix),l.instanceColor!==null&&t.remove(l.instanceColor)}return{update:a,dispose:s}}const Lc=new bt,Fo=new Rc(1,1),Ic=new Sc,Uc=new $l,Nc=new wc,zo=[],ko=[],Oo=new Float32Array(16),Bo=new Float32Array(9),Ho=new Float32Array(4);function Ci(n,e,t){const i=n[0];if(i<=0||i>0)return n;const r=e*t;let a=zo[r];if(a===void 0&&(a=new Float32Array(r),zo[r]=a),e!==0){i.toArray(a,0);for(let s=1,o=0;s!==e;++s)o+=t,n[s].toArray(a,o)}return a}function ft(n,e){if(n.length!==e.length)return!1;for(let t=0,i=n.length;t<i;t++)if(n[t]!==e[t])return!1;return!0}function pt(n,e){for(let t=0,i=e.length;t<i;t++)n[t]=e[t]}function Vr(n,e){let t=ko[e];t===void 0&&(t=new Int32Array(e),ko[e]=t);for(let i=0;i!==e;++i)t[i]=n.allocateTextureUnit();return t}function Ef(n,e){const t=this.cache;t[0]!==e&&(n.uniform1f(this.addr,e),t[0]=e)}function yf(n,e){const t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y)&&(n.uniform2f(this.addr,e.x,e.y),t[0]=e.x,t[1]=e.y);else{if(ft(t,e))return;n.uniform2fv(this.addr,e),pt(t,e)}}function bf(n,e){const t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y||t[2]!==e.z)&&(n.uniform3f(this.addr,e.x,e.y,e.z),t[0]=e.x,t[1]=e.y,t[2]=e.z);else if(e.r!==void 0)(t[0]!==e.r||t[1]!==e.g||t[2]!==e.b)&&(n.uniform3f(this.addr,e.r,e.g,e.b),t[0]=e.r,t[1]=e.g,t[2]=e.b);else{if(ft(t,e))return;n.uniform3fv(this.addr,e),pt(t,e)}}function Tf(n,e){const t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y||t[2]!==e.z||t[3]!==e.w)&&(n.uniform4f(this.addr,e.x,e.y,e.z,e.w),t[0]=e.x,t[1]=e.y,t[2]=e.z,t[3]=e.w);else{if(ft(t,e))return;n.uniform4fv(this.addr,e),pt(t,e)}}function Af(n,e){const t=this.cache,i=e.elements;if(i===void 0){if(ft(t,e))return;n.uniformMatrix2fv(this.addr,!1,e),pt(t,e)}else{if(ft(t,i))return;Ho.set(i),n.uniformMatrix2fv(this.addr,!1,Ho),pt(t,i)}}function wf(n,e){const t=this.cache,i=e.elements;if(i===void 0){if(ft(t,e))return;n.uniformMatrix3fv(this.addr,!1,e),pt(t,e)}else{if(ft(t,i))return;Bo.set(i),n.uniformMatrix3fv(this.addr,!1,Bo),pt(t,i)}}function Rf(n,e){const t=this.cache,i=e.elements;if(i===void 0){if(ft(t,e))return;n.uniformMatrix4fv(this.addr,!1,e),pt(t,e)}else{if(ft(t,i))return;Oo.set(i),n.uniformMatrix4fv(this.addr,!1,Oo),pt(t,i)}}function Cf(n,e){const t=this.cache;t[0]!==e&&(n.uniform1i(this.addr,e),t[0]=e)}function Pf(n,e){const t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y)&&(n.uniform2i(this.addr,e.x,e.y),t[0]=e.x,t[1]=e.y);else{if(ft(t,e))return;n.uniform2iv(this.addr,e),pt(t,e)}}function Df(n,e){const t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y||t[2]!==e.z)&&(n.uniform3i(this.addr,e.x,e.y,e.z),t[0]=e.x,t[1]=e.y,t[2]=e.z);else{if(ft(t,e))return;n.uniform3iv(this.addr,e),pt(t,e)}}function Lf(n,e){const t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y||t[2]!==e.z||t[3]!==e.w)&&(n.uniform4i(this.addr,e.x,e.y,e.z,e.w),t[0]=e.x,t[1]=e.y,t[2]=e.z,t[3]=e.w);else{if(ft(t,e))return;n.uniform4iv(this.addr,e),pt(t,e)}}function If(n,e){const t=this.cache;t[0]!==e&&(n.uniform1ui(this.addr,e),t[0]=e)}function Uf(n,e){const t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y)&&(n.uniform2ui(this.addr,e.x,e.y),t[0]=e.x,t[1]=e.y);else{if(ft(t,e))return;n.uniform2uiv(this.addr,e),pt(t,e)}}function Nf(n,e){const t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y||t[2]!==e.z)&&(n.uniform3ui(this.addr,e.x,e.y,e.z),t[0]=e.x,t[1]=e.y,t[2]=e.z);else{if(ft(t,e))return;n.uniform3uiv(this.addr,e),pt(t,e)}}function Ff(n,e){const t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y||t[2]!==e.z||t[3]!==e.w)&&(n.uniform4ui(this.addr,e.x,e.y,e.z,e.w),t[0]=e.x,t[1]=e.y,t[2]=e.z,t[3]=e.w);else{if(ft(t,e))return;n.uniform4uiv(this.addr,e),pt(t,e)}}function zf(n,e,t){const i=this.cache,r=t.allocateTextureUnit();i[0]!==r&&(n.uniform1i(this.addr,r),i[0]=r);let a;this.type===n.SAMPLER_2D_SHADOW?(Fo.compareFunction=xc,a=Fo):a=Lc,t.setTexture2D(e||a,r)}function kf(n,e,t){const i=this.cache,r=t.allocateTextureUnit();i[0]!==r&&(n.uniform1i(this.addr,r),i[0]=r),t.setTexture3D(e||Uc,r)}function Of(n,e,t){const i=this.cache,r=t.allocateTextureUnit();i[0]!==r&&(n.uniform1i(this.addr,r),i[0]=r),t.setTextureCube(e||Nc,r)}function Bf(n,e,t){const i=this.cache,r=t.allocateTextureUnit();i[0]!==r&&(n.uniform1i(this.addr,r),i[0]=r),t.setTexture2DArray(e||Ic,r)}function Hf(n){switch(n){case 5126:return Ef;case 35664:return yf;case 35665:return bf;case 35666:return Tf;case 35674:return Af;case 35675:return wf;case 35676:return Rf;case 5124:case 35670:return Cf;case 35667:case 35671:return Pf;case 35668:case 35672:return Df;case 35669:case 35673:return Lf;case 5125:return If;case 36294:return Uf;case 36295:return Nf;case 36296:return Ff;case 35678:case 36198:case 36298:case 36306:case 35682:return zf;case 35679:case 36299:case 36307:return kf;case 35680:case 36300:case 36308:case 36293:return Of;case 36289:case 36303:case 36311:case 36292:return Bf}}function Vf(n,e){n.uniform1fv(this.addr,e)}function Gf(n,e){const t=Ci(e,this.size,2);n.uniform2fv(this.addr,t)}function jf(n,e){const t=Ci(e,this.size,3);n.uniform3fv(this.addr,t)}function Wf(n,e){const t=Ci(e,this.size,4);n.uniform4fv(this.addr,t)}function Xf(n,e){const t=Ci(e,this.size,4);n.uniformMatrix2fv(this.addr,!1,t)}function Yf(n,e){const t=Ci(e,this.size,9);n.uniformMatrix3fv(this.addr,!1,t)}function qf(n,e){const t=Ci(e,this.size,16);n.uniformMatrix4fv(this.addr,!1,t)}function $f(n,e){n.uniform1iv(this.addr,e)}function Kf(n,e){n.uniform2iv(this.addr,e)}function Zf(n,e){n.uniform3iv(this.addr,e)}function Jf(n,e){n.uniform4iv(this.addr,e)}function Qf(n,e){n.uniform1uiv(this.addr,e)}function ep(n,e){n.uniform2uiv(this.addr,e)}function tp(n,e){n.uniform3uiv(this.addr,e)}function np(n,e){n.uniform4uiv(this.addr,e)}function ip(n,e,t){const i=this.cache,r=e.length,a=Vr(t,r);ft(i,a)||(n.uniform1iv(this.addr,a),pt(i,a));for(let s=0;s!==r;++s)t.setTexture2D(e[s]||Lc,a[s])}function rp(n,e,t){const i=this.cache,r=e.length,a=Vr(t,r);ft(i,a)||(n.uniform1iv(this.addr,a),pt(i,a));for(let s=0;s!==r;++s)t.setTexture3D(e[s]||Uc,a[s])}function ap(n,e,t){const i=this.cache,r=e.length,a=Vr(t,r);ft(i,a)||(n.uniform1iv(this.addr,a),pt(i,a));for(let s=0;s!==r;++s)t.setTextureCube(e[s]||Nc,a[s])}function sp(n,e,t){const i=this.cache,r=e.length,a=Vr(t,r);ft(i,a)||(n.uniform1iv(this.addr,a),pt(i,a));for(let s=0;s!==r;++s)t.setTexture2DArray(e[s]||Ic,a[s])}function op(n){switch(n){case 5126:return Vf;case 35664:return Gf;case 35665:return jf;case 35666:return Wf;case 35674:return Xf;case 35675:return Yf;case 35676:return qf;case 5124:case 35670:return $f;case 35667:case 35671:return Kf;case 35668:case 35672:return Zf;case 35669:case 35673:return Jf;case 5125:return Qf;case 36294:return ep;case 36295:return tp;case 36296:return np;case 35678:case 36198:case 36298:case 36306:case 35682:return ip;case 35679:case 36299:case 36307:return rp;case 35680:case 36300:case 36308:case 36293:return ap;case 36289:case 36303:case 36311:case 36292:return sp}}class cp{constructor(e,t,i){this.id=e,this.addr=i,this.cache=[],this.type=t.type,this.setValue=Hf(t.type)}}class lp{constructor(e,t,i){this.id=e,this.addr=i,this.cache=[],this.type=t.type,this.size=t.size,this.setValue=op(t.type)}}class up{constructor(e){this.id=e,this.seq=[],this.map={}}setValue(e,t,i){const r=this.seq;for(let a=0,s=r.length;a!==s;++a){const o=r[a];o.setValue(e,t[o.id],i)}}}const ba=/(\w+)(\])?(\[|\.)?/g;function Vo(n,e){n.seq.push(e),n.map[e.id]=e}function dp(n,e,t){const i=n.name,r=i.length;for(ba.lastIndex=0;;){const a=ba.exec(i),s=ba.lastIndex;let o=a[1];const c=a[2]==="]",l=a[3];if(c&&(o=o|0),l===void 0||l==="["&&s+2===r){Vo(t,l===void 0?new cp(o,n,e):new lp(o,n,e));break}else{let h=t.map[o];h===void 0&&(h=new up(o),Vo(t,h)),t=h}}}class Rr{constructor(e,t){this.seq=[],this.map={};const i=e.getProgramParameter(t,e.ACTIVE_UNIFORMS);for(let r=0;r<i;++r){const a=e.getActiveUniform(t,r),s=e.getUniformLocation(t,a.name);dp(a,s,this)}}setValue(e,t,i,r){const a=this.map[t];a!==void 0&&a.setValue(e,i,r)}setOptional(e,t,i){const r=t[i];r!==void 0&&this.setValue(e,i,r)}static upload(e,t,i,r){for(let a=0,s=t.length;a!==s;++a){const o=t[a],c=i[o.id];c.needsUpdate!==!1&&o.setValue(e,c.value,r)}}static seqWithValue(e,t){const i=[];for(let r=0,a=e.length;r!==a;++r){const s=e[r];s.id in t&&i.push(s)}return i}}function Go(n,e,t){const i=n.createShader(e);return n.shaderSource(i,t),n.compileShader(i),i}const hp=37297;let fp=0;function pp(n,e){const t=n.split(`
`),i=[],r=Math.max(e-6,0),a=Math.min(e+6,t.length);for(let s=r;s<a;s++){const o=s+1;i.push(`${o===e?">":" "} ${o}: ${t[s]}`)}return i.join(`
`)}const jo=new Be;function mp(n){Ke._getMatrix(jo,Ke.workingColorSpace,n);const e=`mat3( ${jo.elements.map(t=>t.toFixed(4))} )`;switch(Ke.getTransfer(n)){case Pr:return[e,"LinearTransferOETF"];case et:return[e,"sRGBTransferOETF"];default:return console.warn("THREE.WebGLProgram: Unsupported color space: ",n),[e,"LinearTransferOETF"]}}function Wo(n,e,t){const i=n.getShaderParameter(e,n.COMPILE_STATUS),r=n.getShaderInfoLog(e).trim();if(i&&r==="")return"";const a=/ERROR: 0:(\d+)/.exec(r);if(a){const s=parseInt(a[1]);return t.toUpperCase()+`

`+r+`

`+pp(n.getShaderSource(e),s)}else return r}function gp(n,e){const t=mp(e);return[`vec4 ${n}( vec4 value ) {`,`	return ${t[1]}( vec4( value.rgb * ${t[0]}, value.a ) );`,"}"].join(`
`)}function _p(n,e){let t;switch(e){case Sl:t="Linear";break;case El:t="Reinhard";break;case yl:t="Cineon";break;case bl:t="ACESFilmic";break;case Al:t="AgX";break;case wl:t="Neutral";break;case Tl:t="Custom";break;default:console.warn("THREE.WebGLProgram: Unsupported toneMapping:",e),t="Linear"}return"vec3 "+n+"( vec3 color ) { return "+t+"ToneMapping( color ); }"}const xr=new k;function vp(){Ke.getLuminanceCoefficients(xr);const n=xr.x.toFixed(4),e=xr.y.toFixed(4),t=xr.z.toFixed(4);return["float luminance( const in vec3 rgb ) {",`	const vec3 weights = vec3( ${n}, ${e}, ${t} );`,"	return dot( weights, rgb );","}"].join(`
`)}function xp(n){return[n.extensionClipCullDistance?"#extension GL_ANGLE_clip_cull_distance : require":"",n.extensionMultiDraw?"#extension GL_ANGLE_multi_draw : require":""].filter(zi).join(`
`)}function Mp(n){const e=[];for(const t in n){const i=n[t];i!==!1&&e.push("#define "+t+" "+i)}return e.join(`
`)}function Sp(n,e){const t={},i=n.getProgramParameter(e,n.ACTIVE_ATTRIBUTES);for(let r=0;r<i;r++){const a=n.getActiveAttrib(e,r),s=a.name;let o=1;a.type===n.FLOAT_MAT2&&(o=2),a.type===n.FLOAT_MAT3&&(o=3),a.type===n.FLOAT_MAT4&&(o=4),t[s]={type:a.type,location:n.getAttribLocation(e,s),locationSize:o}}return t}function zi(n){return n!==""}function Xo(n,e){const t=e.numSpotLightShadows+e.numSpotLightMaps-e.numSpotLightShadowsWithMaps;return n.replace(/NUM_DIR_LIGHTS/g,e.numDirLights).replace(/NUM_SPOT_LIGHTS/g,e.numSpotLights).replace(/NUM_SPOT_LIGHT_MAPS/g,e.numSpotLightMaps).replace(/NUM_SPOT_LIGHT_COORDS/g,t).replace(/NUM_RECT_AREA_LIGHTS/g,e.numRectAreaLights).replace(/NUM_POINT_LIGHTS/g,e.numPointLights).replace(/NUM_HEMI_LIGHTS/g,e.numHemiLights).replace(/NUM_DIR_LIGHT_SHADOWS/g,e.numDirLightShadows).replace(/NUM_SPOT_LIGHT_SHADOWS_WITH_MAPS/g,e.numSpotLightShadowsWithMaps).replace(/NUM_SPOT_LIGHT_SHADOWS/g,e.numSpotLightShadows).replace(/NUM_POINT_LIGHT_SHADOWS/g,e.numPointLightShadows)}function Yo(n,e){return n.replace(/NUM_CLIPPING_PLANES/g,e.numClippingPlanes).replace(/UNION_CLIPPING_PLANES/g,e.numClippingPlanes-e.numClipIntersection)}const Ep=/^[ \t]*#include +<([\w\d./]+)>/gm;function _s(n){return n.replace(Ep,bp)}const yp=new Map;function bp(n,e){let t=Ve[e];if(t===void 0){const i=yp.get(e);if(i!==void 0)t=Ve[i],console.warn('THREE.WebGLRenderer: Shader chunk "%s" has been deprecated. Use "%s" instead.',e,i);else throw new Error("Can not resolve #include <"+e+">")}return _s(t)}const Tp=/#pragma unroll_loop_start\s+for\s*\(\s*int\s+i\s*=\s*(\d+)\s*;\s*i\s*<\s*(\d+)\s*;\s*i\s*\+\+\s*\)\s*{([\s\S]+?)}\s+#pragma unroll_loop_end/g;function qo(n){return n.replace(Tp,Ap)}function Ap(n,e,t,i){let r="";for(let a=parseInt(e);a<parseInt(t);a++)r+=i.replace(/\[\s*i\s*\]/g,"[ "+a+" ]").replace(/UNROLLED_LOOP_INDEX/g,a);return r}function $o(n){let e=`precision ${n.precision} float;
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
#define LOW_PRECISION`),e}function wp(n){let e="SHADOWMAP_TYPE_BASIC";return n.shadowMapType===ac?e="SHADOWMAP_TYPE_PCF":n.shadowMapType===el?e="SHADOWMAP_TYPE_PCF_SOFT":n.shadowMapType===cn&&(e="SHADOWMAP_TYPE_VSM"),e}function Rp(n){let e="ENVMAP_TYPE_CUBE";if(n.envMap)switch(n.envMapMode){case Si:case Ei:e="ENVMAP_TYPE_CUBE";break;case Or:e="ENVMAP_TYPE_CUBE_UV";break}return e}function Cp(n){let e="ENVMAP_MODE_REFLECTION";if(n.envMap)switch(n.envMapMode){case Ei:e="ENVMAP_MODE_REFRACTION";break}return e}function Pp(n){let e="ENVMAP_BLENDING_NONE";if(n.envMap)switch(n.combine){case sc:e="ENVMAP_BLENDING_MULTIPLY";break;case xl:e="ENVMAP_BLENDING_MIX";break;case Ml:e="ENVMAP_BLENDING_ADD";break}return e}function Dp(n){const e=n.envMapCubeUVHeight;if(e===null)return null;const t=Math.log2(e)-2,i=1/e;return{texelWidth:1/(3*Math.max(Math.pow(2,t),112)),texelHeight:i,maxMip:t}}function Lp(n,e,t,i){const r=n.getContext(),a=t.defines;let s=t.vertexShader,o=t.fragmentShader;const c=wp(t),l=Rp(t),d=Cp(t),h=Pp(t),f=Dp(t),m=xp(t),g=Mp(a),_=r.createProgram();let p,u,w=t.glslVersion?"#version "+t.glslVersion+`
`:"";t.isRawShaderMaterial?(p=["#define SHADER_TYPE "+t.shaderType,"#define SHADER_NAME "+t.shaderName,g].filter(zi).join(`
`),p.length>0&&(p+=`
`),u=["#define SHADER_TYPE "+t.shaderType,"#define SHADER_NAME "+t.shaderName,g].filter(zi).join(`
`),u.length>0&&(u+=`
`)):(p=[$o(t),"#define SHADER_TYPE "+t.shaderType,"#define SHADER_NAME "+t.shaderName,g,t.extensionClipCullDistance?"#define USE_CLIP_DISTANCE":"",t.batching?"#define USE_BATCHING":"",t.batchingColor?"#define USE_BATCHING_COLOR":"",t.instancing?"#define USE_INSTANCING":"",t.instancingColor?"#define USE_INSTANCING_COLOR":"",t.instancingMorph?"#define USE_INSTANCING_MORPH":"",t.useFog&&t.fog?"#define USE_FOG":"",t.useFog&&t.fogExp2?"#define FOG_EXP2":"",t.map?"#define USE_MAP":"",t.envMap?"#define USE_ENVMAP":"",t.envMap?"#define "+d:"",t.lightMap?"#define USE_LIGHTMAP":"",t.aoMap?"#define USE_AOMAP":"",t.bumpMap?"#define USE_BUMPMAP":"",t.normalMap?"#define USE_NORMALMAP":"",t.normalMapObjectSpace?"#define USE_NORMALMAP_OBJECTSPACE":"",t.normalMapTangentSpace?"#define USE_NORMALMAP_TANGENTSPACE":"",t.displacementMap?"#define USE_DISPLACEMENTMAP":"",t.emissiveMap?"#define USE_EMISSIVEMAP":"",t.anisotropy?"#define USE_ANISOTROPY":"",t.anisotropyMap?"#define USE_ANISOTROPYMAP":"",t.clearcoatMap?"#define USE_CLEARCOATMAP":"",t.clearcoatRoughnessMap?"#define USE_CLEARCOAT_ROUGHNESSMAP":"",t.clearcoatNormalMap?"#define USE_CLEARCOAT_NORMALMAP":"",t.iridescenceMap?"#define USE_IRIDESCENCEMAP":"",t.iridescenceThicknessMap?"#define USE_IRIDESCENCE_THICKNESSMAP":"",t.specularMap?"#define USE_SPECULARMAP":"",t.specularColorMap?"#define USE_SPECULAR_COLORMAP":"",t.specularIntensityMap?"#define USE_SPECULAR_INTENSITYMAP":"",t.roughnessMap?"#define USE_ROUGHNESSMAP":"",t.metalnessMap?"#define USE_METALNESSMAP":"",t.alphaMap?"#define USE_ALPHAMAP":"",t.alphaHash?"#define USE_ALPHAHASH":"",t.transmission?"#define USE_TRANSMISSION":"",t.transmissionMap?"#define USE_TRANSMISSIONMAP":"",t.thicknessMap?"#define USE_THICKNESSMAP":"",t.sheenColorMap?"#define USE_SHEEN_COLORMAP":"",t.sheenRoughnessMap?"#define USE_SHEEN_ROUGHNESSMAP":"",t.mapUv?"#define MAP_UV "+t.mapUv:"",t.alphaMapUv?"#define ALPHAMAP_UV "+t.alphaMapUv:"",t.lightMapUv?"#define LIGHTMAP_UV "+t.lightMapUv:"",t.aoMapUv?"#define AOMAP_UV "+t.aoMapUv:"",t.emissiveMapUv?"#define EMISSIVEMAP_UV "+t.emissiveMapUv:"",t.bumpMapUv?"#define BUMPMAP_UV "+t.bumpMapUv:"",t.normalMapUv?"#define NORMALMAP_UV "+t.normalMapUv:"",t.displacementMapUv?"#define DISPLACEMENTMAP_UV "+t.displacementMapUv:"",t.metalnessMapUv?"#define METALNESSMAP_UV "+t.metalnessMapUv:"",t.roughnessMapUv?"#define ROUGHNESSMAP_UV "+t.roughnessMapUv:"",t.anisotropyMapUv?"#define ANISOTROPYMAP_UV "+t.anisotropyMapUv:"",t.clearcoatMapUv?"#define CLEARCOATMAP_UV "+t.clearcoatMapUv:"",t.clearcoatNormalMapUv?"#define CLEARCOAT_NORMALMAP_UV "+t.clearcoatNormalMapUv:"",t.clearcoatRoughnessMapUv?"#define CLEARCOAT_ROUGHNESSMAP_UV "+t.clearcoatRoughnessMapUv:"",t.iridescenceMapUv?"#define IRIDESCENCEMAP_UV "+t.iridescenceMapUv:"",t.iridescenceThicknessMapUv?"#define IRIDESCENCE_THICKNESSMAP_UV "+t.iridescenceThicknessMapUv:"",t.sheenColorMapUv?"#define SHEEN_COLORMAP_UV "+t.sheenColorMapUv:"",t.sheenRoughnessMapUv?"#define SHEEN_ROUGHNESSMAP_UV "+t.sheenRoughnessMapUv:"",t.specularMapUv?"#define SPECULARMAP_UV "+t.specularMapUv:"",t.specularColorMapUv?"#define SPECULAR_COLORMAP_UV "+t.specularColorMapUv:"",t.specularIntensityMapUv?"#define SPECULAR_INTENSITYMAP_UV "+t.specularIntensityMapUv:"",t.transmissionMapUv?"#define TRANSMISSIONMAP_UV "+t.transmissionMapUv:"",t.thicknessMapUv?"#define THICKNESSMAP_UV "+t.thicknessMapUv:"",t.vertexTangents&&t.flatShading===!1?"#define USE_TANGENT":"",t.vertexColors?"#define USE_COLOR":"",t.vertexAlphas?"#define USE_COLOR_ALPHA":"",t.vertexUv1s?"#define USE_UV1":"",t.vertexUv2s?"#define USE_UV2":"",t.vertexUv3s?"#define USE_UV3":"",t.pointsUvs?"#define USE_POINTS_UV":"",t.flatShading?"#define FLAT_SHADED":"",t.skinning?"#define USE_SKINNING":"",t.morphTargets?"#define USE_MORPHTARGETS":"",t.morphNormals&&t.flatShading===!1?"#define USE_MORPHNORMALS":"",t.morphColors?"#define USE_MORPHCOLORS":"",t.morphTargetsCount>0?"#define MORPHTARGETS_TEXTURE_STRIDE "+t.morphTextureStride:"",t.morphTargetsCount>0?"#define MORPHTARGETS_COUNT "+t.morphTargetsCount:"",t.doubleSided?"#define DOUBLE_SIDED":"",t.flipSided?"#define FLIP_SIDED":"",t.shadowMapEnabled?"#define USE_SHADOWMAP":"",t.shadowMapEnabled?"#define "+c:"",t.sizeAttenuation?"#define USE_SIZEATTENUATION":"",t.numLightProbes>0?"#define USE_LIGHT_PROBES":"",t.logarithmicDepthBuffer?"#define USE_LOGDEPTHBUF":"",t.reverseDepthBuffer?"#define USE_REVERSEDEPTHBUF":"","uniform mat4 modelMatrix;","uniform mat4 modelViewMatrix;","uniform mat4 projectionMatrix;","uniform mat4 viewMatrix;","uniform mat3 normalMatrix;","uniform vec3 cameraPosition;","uniform bool isOrthographic;","#ifdef USE_INSTANCING","	attribute mat4 instanceMatrix;","#endif","#ifdef USE_INSTANCING_COLOR","	attribute vec3 instanceColor;","#endif","#ifdef USE_INSTANCING_MORPH","	uniform sampler2D morphTexture;","#endif","attribute vec3 position;","attribute vec3 normal;","attribute vec2 uv;","#ifdef USE_UV1","	attribute vec2 uv1;","#endif","#ifdef USE_UV2","	attribute vec2 uv2;","#endif","#ifdef USE_UV3","	attribute vec2 uv3;","#endif","#ifdef USE_TANGENT","	attribute vec4 tangent;","#endif","#if defined( USE_COLOR_ALPHA )","	attribute vec4 color;","#elif defined( USE_COLOR )","	attribute vec3 color;","#endif","#ifdef USE_SKINNING","	attribute vec4 skinIndex;","	attribute vec4 skinWeight;","#endif",`
`].filter(zi).join(`
`),u=[$o(t),"#define SHADER_TYPE "+t.shaderType,"#define SHADER_NAME "+t.shaderName,g,t.useFog&&t.fog?"#define USE_FOG":"",t.useFog&&t.fogExp2?"#define FOG_EXP2":"",t.alphaToCoverage?"#define ALPHA_TO_COVERAGE":"",t.map?"#define USE_MAP":"",t.matcap?"#define USE_MATCAP":"",t.envMap?"#define USE_ENVMAP":"",t.envMap?"#define "+l:"",t.envMap?"#define "+d:"",t.envMap?"#define "+h:"",f?"#define CUBEUV_TEXEL_WIDTH "+f.texelWidth:"",f?"#define CUBEUV_TEXEL_HEIGHT "+f.texelHeight:"",f?"#define CUBEUV_MAX_MIP "+f.maxMip+".0":"",t.lightMap?"#define USE_LIGHTMAP":"",t.aoMap?"#define USE_AOMAP":"",t.bumpMap?"#define USE_BUMPMAP":"",t.normalMap?"#define USE_NORMALMAP":"",t.normalMapObjectSpace?"#define USE_NORMALMAP_OBJECTSPACE":"",t.normalMapTangentSpace?"#define USE_NORMALMAP_TANGENTSPACE":"",t.emissiveMap?"#define USE_EMISSIVEMAP":"",t.anisotropy?"#define USE_ANISOTROPY":"",t.anisotropyMap?"#define USE_ANISOTROPYMAP":"",t.clearcoat?"#define USE_CLEARCOAT":"",t.clearcoatMap?"#define USE_CLEARCOATMAP":"",t.clearcoatRoughnessMap?"#define USE_CLEARCOAT_ROUGHNESSMAP":"",t.clearcoatNormalMap?"#define USE_CLEARCOAT_NORMALMAP":"",t.dispersion?"#define USE_DISPERSION":"",t.iridescence?"#define USE_IRIDESCENCE":"",t.iridescenceMap?"#define USE_IRIDESCENCEMAP":"",t.iridescenceThicknessMap?"#define USE_IRIDESCENCE_THICKNESSMAP":"",t.specularMap?"#define USE_SPECULARMAP":"",t.specularColorMap?"#define USE_SPECULAR_COLORMAP":"",t.specularIntensityMap?"#define USE_SPECULAR_INTENSITYMAP":"",t.roughnessMap?"#define USE_ROUGHNESSMAP":"",t.metalnessMap?"#define USE_METALNESSMAP":"",t.alphaMap?"#define USE_ALPHAMAP":"",t.alphaTest?"#define USE_ALPHATEST":"",t.alphaHash?"#define USE_ALPHAHASH":"",t.sheen?"#define USE_SHEEN":"",t.sheenColorMap?"#define USE_SHEEN_COLORMAP":"",t.sheenRoughnessMap?"#define USE_SHEEN_ROUGHNESSMAP":"",t.transmission?"#define USE_TRANSMISSION":"",t.transmissionMap?"#define USE_TRANSMISSIONMAP":"",t.thicknessMap?"#define USE_THICKNESSMAP":"",t.vertexTangents&&t.flatShading===!1?"#define USE_TANGENT":"",t.vertexColors||t.instancingColor||t.batchingColor?"#define USE_COLOR":"",t.vertexAlphas?"#define USE_COLOR_ALPHA":"",t.vertexUv1s?"#define USE_UV1":"",t.vertexUv2s?"#define USE_UV2":"",t.vertexUv3s?"#define USE_UV3":"",t.pointsUvs?"#define USE_POINTS_UV":"",t.gradientMap?"#define USE_GRADIENTMAP":"",t.flatShading?"#define FLAT_SHADED":"",t.doubleSided?"#define DOUBLE_SIDED":"",t.flipSided?"#define FLIP_SIDED":"",t.shadowMapEnabled?"#define USE_SHADOWMAP":"",t.shadowMapEnabled?"#define "+c:"",t.premultipliedAlpha?"#define PREMULTIPLIED_ALPHA":"",t.numLightProbes>0?"#define USE_LIGHT_PROBES":"",t.decodeVideoTexture?"#define DECODE_VIDEO_TEXTURE":"",t.decodeVideoTextureEmissive?"#define DECODE_VIDEO_TEXTURE_EMISSIVE":"",t.logarithmicDepthBuffer?"#define USE_LOGDEPTHBUF":"",t.reverseDepthBuffer?"#define USE_REVERSEDEPTHBUF":"","uniform mat4 viewMatrix;","uniform vec3 cameraPosition;","uniform bool isOrthographic;",t.toneMapping!==Tn?"#define TONE_MAPPING":"",t.toneMapping!==Tn?Ve.tonemapping_pars_fragment:"",t.toneMapping!==Tn?_p("toneMapping",t.toneMapping):"",t.dithering?"#define DITHERING":"",t.opaque?"#define OPAQUE":"",Ve.colorspace_pars_fragment,gp("linearToOutputTexel",t.outputColorSpace),vp(),t.useDepthPacking?"#define DEPTH_PACKING "+t.depthPacking:"",`
`].filter(zi).join(`
`)),s=_s(s),s=Xo(s,t),s=Yo(s,t),o=_s(o),o=Xo(o,t),o=Yo(o,t),s=qo(s),o=qo(o),t.isRawShaderMaterial!==!0&&(w=`#version 300 es
`,p=[m,"#define attribute in","#define varying out","#define texture2D texture"].join(`
`)+`
`+p,u=["#define varying in",t.glslVersion===eo?"":"layout(location = 0) out highp vec4 pc_fragColor;",t.glslVersion===eo?"":"#define gl_FragColor pc_fragColor","#define gl_FragDepthEXT gl_FragDepth","#define texture2D texture","#define textureCube texture","#define texture2DProj textureProj","#define texture2DLodEXT textureLod","#define texture2DProjLodEXT textureProjLod","#define textureCubeLodEXT textureLod","#define texture2DGradEXT textureGrad","#define texture2DProjGradEXT textureProjGrad","#define textureCubeGradEXT textureGrad"].join(`
`)+`
`+u);const b=w+p+s,S=w+u+o,T=Go(r,r.VERTEX_SHADER,b),y=Go(r,r.FRAGMENT_SHADER,S);r.attachShader(_,T),r.attachShader(_,y),t.index0AttributeName!==void 0?r.bindAttribLocation(_,0,t.index0AttributeName):t.morphTargets===!0&&r.bindAttribLocation(_,0,"position"),r.linkProgram(_);function A(C){if(n.debug.checkShaderErrors){const F=r.getProgramInfoLog(_).trim(),N=r.getShaderInfoLog(T).trim(),P=r.getShaderInfoLog(y).trim();let U=!0,z=!0;if(r.getProgramParameter(_,r.LINK_STATUS)===!1)if(U=!1,typeof n.debug.onShaderError=="function")n.debug.onShaderError(r,_,T,y);else{const H=Wo(r,T,"vertex"),I=Wo(r,y,"fragment");console.error("THREE.WebGLProgram: Shader Error "+r.getError()+" - VALIDATE_STATUS "+r.getProgramParameter(_,r.VALIDATE_STATUS)+`

Material Name: `+C.name+`
Material Type: `+C.type+`

Program Info Log: `+F+`
`+H+`
`+I)}else F!==""?console.warn("THREE.WebGLProgram: Program Info Log:",F):(N===""||P==="")&&(z=!1);z&&(C.diagnostics={runnable:U,programLog:F,vertexShader:{log:N,prefix:p},fragmentShader:{log:P,prefix:u}})}r.deleteShader(T),r.deleteShader(y),D=new Rr(r,_),x=Sp(r,_)}let D;this.getUniforms=function(){return D===void 0&&A(this),D};let x;this.getAttributes=function(){return x===void 0&&A(this),x};let v=t.rendererExtensionParallelShaderCompile===!1;return this.isReady=function(){return v===!1&&(v=r.getProgramParameter(_,hp)),v},this.destroy=function(){i.releaseStatesOfProgram(this),r.deleteProgram(_),this.program=void 0},this.type=t.shaderType,this.name=t.shaderName,this.id=fp++,this.cacheKey=e,this.usedTimes=1,this.program=_,this.vertexShader=T,this.fragmentShader=y,this}let Ip=0;class Up{constructor(){this.shaderCache=new Map,this.materialCache=new Map}update(e){const t=e.vertexShader,i=e.fragmentShader,r=this._getShaderStage(t),a=this._getShaderStage(i),s=this._getShaderCacheForMaterial(e);return s.has(r)===!1&&(s.add(r),r.usedTimes++),s.has(a)===!1&&(s.add(a),a.usedTimes++),this}remove(e){const t=this.materialCache.get(e);for(const i of t)i.usedTimes--,i.usedTimes===0&&this.shaderCache.delete(i.code);return this.materialCache.delete(e),this}getVertexShaderID(e){return this._getShaderStage(e.vertexShader).id}getFragmentShaderID(e){return this._getShaderStage(e.fragmentShader).id}dispose(){this.shaderCache.clear(),this.materialCache.clear()}_getShaderCacheForMaterial(e){const t=this.materialCache;let i=t.get(e);return i===void 0&&(i=new Set,t.set(e,i)),i}_getShaderStage(e){const t=this.shaderCache;let i=t.get(e);return i===void 0&&(i=new Np(e),t.set(e,i)),i}}class Np{constructor(e){this.id=Ip++,this.code=e,this.usedTimes=0}}function Fp(n,e,t,i,r,a,s){const o=new Is,c=new Up,l=new Set,d=[],h=r.logarithmicDepthBuffer,f=r.vertexTextures;let m=r.precision;const g={MeshDepthMaterial:"depth",MeshDistanceMaterial:"distanceRGBA",MeshNormalMaterial:"normal",MeshBasicMaterial:"basic",MeshLambertMaterial:"lambert",MeshPhongMaterial:"phong",MeshToonMaterial:"toon",MeshStandardMaterial:"physical",MeshPhysicalMaterial:"physical",MeshMatcapMaterial:"matcap",LineBasicMaterial:"basic",LineDashedMaterial:"dashed",PointsMaterial:"points",ShadowMaterial:"shadow",SpriteMaterial:"sprite"};function _(x){return l.add(x),x===0?"uv":`uv${x}`}function p(x,v,C,F,N){const P=F.fog,U=N.geometry,z=x.isMeshStandardMaterial?F.environment:null,H=(x.isMeshStandardMaterial?t:e).get(x.envMap||z),I=H&&H.mapping===Or?H.image.height:null,G=g[x.type];x.precision!==null&&(m=r.getMaxPrecision(x.precision),m!==x.precision&&console.warn("THREE.WebGLProgram.getParameters:",x.precision,"not supported, using",m,"instead."));const q=U.morphAttributes.position||U.morphAttributes.normal||U.morphAttributes.color,oe=q!==void 0?q.length:0;let le=0;U.morphAttributes.position!==void 0&&(le=1),U.morphAttributes.normal!==void 0&&(le=2),U.morphAttributes.color!==void 0&&(le=3);let Re,Y,te,de;if(G){const Qe=$t[G];Re=Qe.vertexShader,Y=Qe.fragmentShader}else Re=x.vertexShader,Y=x.fragmentShader,c.update(x),te=c.getVertexShaderID(x),de=c.getFragmentShaderID(x);const se=n.getRenderTarget(),Q=n.state.buffers.depth.getReversed(),ge=N.isInstancedMesh===!0,ue=N.isBatchedMesh===!0,K=!!x.map,ie=!!x.matcap,ae=!!H,L=!!x.aoMap,Ie=!!x.lightMap,Pe=!!x.bumpMap,Ce=!!x.normalMap,Me=!!x.displacementMap,ke=!!x.emissiveMap,we=!!x.metalnessMap,R=!!x.roughnessMap,M=x.anisotropy>0,j=x.clearcoat>0,J=x.dispersion>0,ne=x.iridescence>0,Z=x.sheen>0,Ae=x.transmission>0,me=M&&!!x.anisotropyMap,Ee=j&&!!x.clearcoatMap,Ye=j&&!!x.clearcoatNormalMap,ce=j&&!!x.clearcoatRoughnessMap,ye=ne&&!!x.iridescenceMap,Ue=ne&&!!x.iridescenceThicknessMap,Ne=Z&&!!x.sheenColorMap,be=Z&&!!x.sheenRoughnessMap,We=!!x.specularMap,He=!!x.specularColorMap,tt=!!x.specularIntensityMap,O=Ae&&!!x.transmissionMap,fe=Ae&&!!x.thicknessMap,$=!!x.gradientMap,ee=!!x.alphaMap,xe=x.alphaTest>0,_e=!!x.alphaHash,Oe=!!x.extensions;let ot=Tn;x.toneMapped&&(se===null||se.isXRRenderTarget===!0)&&(ot=n.toneMapping);const vt={shaderID:G,shaderType:x.type,shaderName:x.name,vertexShader:Re,fragmentShader:Y,defines:x.defines,customVertexShaderID:te,customFragmentShaderID:de,isRawShaderMaterial:x.isRawShaderMaterial===!0,glslVersion:x.glslVersion,precision:m,batching:ue,batchingColor:ue&&N._colorsTexture!==null,instancing:ge,instancingColor:ge&&N.instanceColor!==null,instancingMorph:ge&&N.morphTexture!==null,supportsVertexTextures:f,outputColorSpace:se===null?n.outputColorSpace:se.isXRRenderTarget===!0?se.texture.colorSpace:Ti,alphaToCoverage:!!x.alphaToCoverage,map:K,matcap:ie,envMap:ae,envMapMode:ae&&H.mapping,envMapCubeUVHeight:I,aoMap:L,lightMap:Ie,bumpMap:Pe,normalMap:Ce,displacementMap:f&&Me,emissiveMap:ke,normalMapObjectSpace:Ce&&x.normalMapType===Dl,normalMapTangentSpace:Ce&&x.normalMapType===vc,metalnessMap:we,roughnessMap:R,anisotropy:M,anisotropyMap:me,clearcoat:j,clearcoatMap:Ee,clearcoatNormalMap:Ye,clearcoatRoughnessMap:ce,dispersion:J,iridescence:ne,iridescenceMap:ye,iridescenceThicknessMap:Ue,sheen:Z,sheenColorMap:Ne,sheenRoughnessMap:be,specularMap:We,specularColorMap:He,specularIntensityMap:tt,transmission:Ae,transmissionMap:O,thicknessMap:fe,gradientMap:$,opaque:x.transparent===!1&&x.blending===gi&&x.alphaToCoverage===!1,alphaMap:ee,alphaTest:xe,alphaHash:_e,combine:x.combine,mapUv:K&&_(x.map.channel),aoMapUv:L&&_(x.aoMap.channel),lightMapUv:Ie&&_(x.lightMap.channel),bumpMapUv:Pe&&_(x.bumpMap.channel),normalMapUv:Ce&&_(x.normalMap.channel),displacementMapUv:Me&&_(x.displacementMap.channel),emissiveMapUv:ke&&_(x.emissiveMap.channel),metalnessMapUv:we&&_(x.metalnessMap.channel),roughnessMapUv:R&&_(x.roughnessMap.channel),anisotropyMapUv:me&&_(x.anisotropyMap.channel),clearcoatMapUv:Ee&&_(x.clearcoatMap.channel),clearcoatNormalMapUv:Ye&&_(x.clearcoatNormalMap.channel),clearcoatRoughnessMapUv:ce&&_(x.clearcoatRoughnessMap.channel),iridescenceMapUv:ye&&_(x.iridescenceMap.channel),iridescenceThicknessMapUv:Ue&&_(x.iridescenceThicknessMap.channel),sheenColorMapUv:Ne&&_(x.sheenColorMap.channel),sheenRoughnessMapUv:be&&_(x.sheenRoughnessMap.channel),specularMapUv:We&&_(x.specularMap.channel),specularColorMapUv:He&&_(x.specularColorMap.channel),specularIntensityMapUv:tt&&_(x.specularIntensityMap.channel),transmissionMapUv:O&&_(x.transmissionMap.channel),thicknessMapUv:fe&&_(x.thicknessMap.channel),alphaMapUv:ee&&_(x.alphaMap.channel),vertexTangents:!!U.attributes.tangent&&(Ce||M),vertexColors:x.vertexColors,vertexAlphas:x.vertexColors===!0&&!!U.attributes.color&&U.attributes.color.itemSize===4,pointsUvs:N.isPoints===!0&&!!U.attributes.uv&&(K||ee),fog:!!P,useFog:x.fog===!0,fogExp2:!!P&&P.isFogExp2,flatShading:x.flatShading===!0,sizeAttenuation:x.sizeAttenuation===!0,logarithmicDepthBuffer:h,reverseDepthBuffer:Q,skinning:N.isSkinnedMesh===!0,morphTargets:U.morphAttributes.position!==void 0,morphNormals:U.morphAttributes.normal!==void 0,morphColors:U.morphAttributes.color!==void 0,morphTargetsCount:oe,morphTextureStride:le,numDirLights:v.directional.length,numPointLights:v.point.length,numSpotLights:v.spot.length,numSpotLightMaps:v.spotLightMap.length,numRectAreaLights:v.rectArea.length,numHemiLights:v.hemi.length,numDirLightShadows:v.directionalShadowMap.length,numPointLightShadows:v.pointShadowMap.length,numSpotLightShadows:v.spotShadowMap.length,numSpotLightShadowsWithMaps:v.numSpotLightShadowsWithMaps,numLightProbes:v.numLightProbes,numClippingPlanes:s.numPlanes,numClipIntersection:s.numIntersection,dithering:x.dithering,shadowMapEnabled:n.shadowMap.enabled&&C.length>0,shadowMapType:n.shadowMap.type,toneMapping:ot,decodeVideoTexture:K&&x.map.isVideoTexture===!0&&Ke.getTransfer(x.map.colorSpace)===et,decodeVideoTextureEmissive:ke&&x.emissiveMap.isVideoTexture===!0&&Ke.getTransfer(x.emissiveMap.colorSpace)===et,premultipliedAlpha:x.premultipliedAlpha,doubleSided:x.side===kt,flipSided:x.side===Rt,useDepthPacking:x.depthPacking>=0,depthPacking:x.depthPacking||0,index0AttributeName:x.index0AttributeName,extensionClipCullDistance:Oe&&x.extensions.clipCullDistance===!0&&i.has("WEBGL_clip_cull_distance"),extensionMultiDraw:(Oe&&x.extensions.multiDraw===!0||ue)&&i.has("WEBGL_multi_draw"),rendererExtensionParallelShaderCompile:i.has("KHR_parallel_shader_compile"),customProgramCacheKey:x.customProgramCacheKey()};return vt.vertexUv1s=l.has(1),vt.vertexUv2s=l.has(2),vt.vertexUv3s=l.has(3),l.clear(),vt}function u(x){const v=[];if(x.shaderID?v.push(x.shaderID):(v.push(x.customVertexShaderID),v.push(x.customFragmentShaderID)),x.defines!==void 0)for(const C in x.defines)v.push(C),v.push(x.defines[C]);return x.isRawShaderMaterial===!1&&(w(v,x),b(v,x),v.push(n.outputColorSpace)),v.push(x.customProgramCacheKey),v.join()}function w(x,v){x.push(v.precision),x.push(v.outputColorSpace),x.push(v.envMapMode),x.push(v.envMapCubeUVHeight),x.push(v.mapUv),x.push(v.alphaMapUv),x.push(v.lightMapUv),x.push(v.aoMapUv),x.push(v.bumpMapUv),x.push(v.normalMapUv),x.push(v.displacementMapUv),x.push(v.emissiveMapUv),x.push(v.metalnessMapUv),x.push(v.roughnessMapUv),x.push(v.anisotropyMapUv),x.push(v.clearcoatMapUv),x.push(v.clearcoatNormalMapUv),x.push(v.clearcoatRoughnessMapUv),x.push(v.iridescenceMapUv),x.push(v.iridescenceThicknessMapUv),x.push(v.sheenColorMapUv),x.push(v.sheenRoughnessMapUv),x.push(v.specularMapUv),x.push(v.specularColorMapUv),x.push(v.specularIntensityMapUv),x.push(v.transmissionMapUv),x.push(v.thicknessMapUv),x.push(v.combine),x.push(v.fogExp2),x.push(v.sizeAttenuation),x.push(v.morphTargetsCount),x.push(v.morphAttributeCount),x.push(v.numDirLights),x.push(v.numPointLights),x.push(v.numSpotLights),x.push(v.numSpotLightMaps),x.push(v.numHemiLights),x.push(v.numRectAreaLights),x.push(v.numDirLightShadows),x.push(v.numPointLightShadows),x.push(v.numSpotLightShadows),x.push(v.numSpotLightShadowsWithMaps),x.push(v.numLightProbes),x.push(v.shadowMapType),x.push(v.toneMapping),x.push(v.numClippingPlanes),x.push(v.numClipIntersection),x.push(v.depthPacking)}function b(x,v){o.disableAll(),v.supportsVertexTextures&&o.enable(0),v.instancing&&o.enable(1),v.instancingColor&&o.enable(2),v.instancingMorph&&o.enable(3),v.matcap&&o.enable(4),v.envMap&&o.enable(5),v.normalMapObjectSpace&&o.enable(6),v.normalMapTangentSpace&&o.enable(7),v.clearcoat&&o.enable(8),v.iridescence&&o.enable(9),v.alphaTest&&o.enable(10),v.vertexColors&&o.enable(11),v.vertexAlphas&&o.enable(12),v.vertexUv1s&&o.enable(13),v.vertexUv2s&&o.enable(14),v.vertexUv3s&&o.enable(15),v.vertexTangents&&o.enable(16),v.anisotropy&&o.enable(17),v.alphaHash&&o.enable(18),v.batching&&o.enable(19),v.dispersion&&o.enable(20),v.batchingColor&&o.enable(21),x.push(o.mask),o.disableAll(),v.fog&&o.enable(0),v.useFog&&o.enable(1),v.flatShading&&o.enable(2),v.logarithmicDepthBuffer&&o.enable(3),v.reverseDepthBuffer&&o.enable(4),v.skinning&&o.enable(5),v.morphTargets&&o.enable(6),v.morphNormals&&o.enable(7),v.morphColors&&o.enable(8),v.premultipliedAlpha&&o.enable(9),v.shadowMapEnabled&&o.enable(10),v.doubleSided&&o.enable(11),v.flipSided&&o.enable(12),v.useDepthPacking&&o.enable(13),v.dithering&&o.enable(14),v.transmission&&o.enable(15),v.sheen&&o.enable(16),v.opaque&&o.enable(17),v.pointsUvs&&o.enable(18),v.decodeVideoTexture&&o.enable(19),v.decodeVideoTextureEmissive&&o.enable(20),v.alphaToCoverage&&o.enable(21),x.push(o.mask)}function S(x){const v=g[x.type];let C;if(v){const F=$t[v];C=cu.clone(F.uniforms)}else C=x.uniforms;return C}function T(x,v){let C;for(let F=0,N=d.length;F<N;F++){const P=d[F];if(P.cacheKey===v){C=P,++C.usedTimes;break}}return C===void 0&&(C=new Lp(n,v,x,a),d.push(C)),C}function y(x){if(--x.usedTimes===0){const v=d.indexOf(x);d[v]=d[d.length-1],d.pop(),x.destroy()}}function A(x){c.remove(x)}function D(){c.dispose()}return{getParameters:p,getProgramCacheKey:u,getUniforms:S,acquireProgram:T,releaseProgram:y,releaseShaderCache:A,programs:d,dispose:D}}function zp(){let n=new WeakMap;function e(s){return n.has(s)}function t(s){let o=n.get(s);return o===void 0&&(o={},n.set(s,o)),o}function i(s){n.delete(s)}function r(s,o,c){n.get(s)[o]=c}function a(){n=new WeakMap}return{has:e,get:t,remove:i,update:r,dispose:a}}function kp(n,e){return n.groupOrder!==e.groupOrder?n.groupOrder-e.groupOrder:n.renderOrder!==e.renderOrder?n.renderOrder-e.renderOrder:n.material.id!==e.material.id?n.material.id-e.material.id:n.z!==e.z?n.z-e.z:n.id-e.id}function Ko(n,e){return n.groupOrder!==e.groupOrder?n.groupOrder-e.groupOrder:n.renderOrder!==e.renderOrder?n.renderOrder-e.renderOrder:n.z!==e.z?e.z-n.z:n.id-e.id}function Zo(){const n=[];let e=0;const t=[],i=[],r=[];function a(){e=0,t.length=0,i.length=0,r.length=0}function s(h,f,m,g,_,p){let u=n[e];return u===void 0?(u={id:h.id,object:h,geometry:f,material:m,groupOrder:g,renderOrder:h.renderOrder,z:_,group:p},n[e]=u):(u.id=h.id,u.object=h,u.geometry=f,u.material=m,u.groupOrder=g,u.renderOrder=h.renderOrder,u.z=_,u.group=p),e++,u}function o(h,f,m,g,_,p){const u=s(h,f,m,g,_,p);m.transmission>0?i.push(u):m.transparent===!0?r.push(u):t.push(u)}function c(h,f,m,g,_,p){const u=s(h,f,m,g,_,p);m.transmission>0?i.unshift(u):m.transparent===!0?r.unshift(u):t.unshift(u)}function l(h,f){t.length>1&&t.sort(h||kp),i.length>1&&i.sort(f||Ko),r.length>1&&r.sort(f||Ko)}function d(){for(let h=e,f=n.length;h<f;h++){const m=n[h];if(m.id===null)break;m.id=null,m.object=null,m.geometry=null,m.material=null,m.group=null}}return{opaque:t,transmissive:i,transparent:r,init:a,push:o,unshift:c,finish:d,sort:l}}function Op(){let n=new WeakMap;function e(i,r){const a=n.get(i);let s;return a===void 0?(s=new Zo,n.set(i,[s])):r>=a.length?(s=new Zo,a.push(s)):s=a[r],s}function t(){n=new WeakMap}return{get:e,dispose:t}}function Bp(){const n={};return{get:function(e){if(n[e.id]!==void 0)return n[e.id];let t;switch(e.type){case"DirectionalLight":t={direction:new k,color:new ve};break;case"SpotLight":t={position:new k,direction:new k,color:new ve,distance:0,coneCos:0,penumbraCos:0,decay:0};break;case"PointLight":t={position:new k,color:new ve,distance:0,decay:0};break;case"HemisphereLight":t={direction:new k,skyColor:new ve,groundColor:new ve};break;case"RectAreaLight":t={color:new ve,position:new k,halfWidth:new k,halfHeight:new k};break}return n[e.id]=t,t}}}function Hp(){const n={};return{get:function(e){if(n[e.id]!==void 0)return n[e.id];let t;switch(e.type){case"DirectionalLight":t={shadowIntensity:1,shadowBias:0,shadowNormalBias:0,shadowRadius:1,shadowMapSize:new Xe};break;case"SpotLight":t={shadowIntensity:1,shadowBias:0,shadowNormalBias:0,shadowRadius:1,shadowMapSize:new Xe};break;case"PointLight":t={shadowIntensity:1,shadowBias:0,shadowNormalBias:0,shadowRadius:1,shadowMapSize:new Xe,shadowCameraNear:1,shadowCameraFar:1e3};break}return n[e.id]=t,t}}}let Vp=0;function Gp(n,e){return(e.castShadow?2:0)-(n.castShadow?2:0)+(e.map?1:0)-(n.map?1:0)}function jp(n){const e=new Bp,t=Hp(),i={version:0,hash:{directionalLength:-1,pointLength:-1,spotLength:-1,rectAreaLength:-1,hemiLength:-1,numDirectionalShadows:-1,numPointShadows:-1,numSpotShadows:-1,numSpotMaps:-1,numLightProbes:-1},ambient:[0,0,0],probe:[],directional:[],directionalShadow:[],directionalShadowMap:[],directionalShadowMatrix:[],spot:[],spotLightMap:[],spotShadow:[],spotShadowMap:[],spotLightMatrix:[],rectArea:[],rectAreaLTC1:null,rectAreaLTC2:null,point:[],pointShadow:[],pointShadowMap:[],pointShadowMatrix:[],hemi:[],numSpotLightShadowsWithMaps:0,numLightProbes:0};for(let l=0;l<9;l++)i.probe.push(new k);const r=new k,a=new at,s=new at;function o(l){let d=0,h=0,f=0;for(let x=0;x<9;x++)i.probe[x].set(0,0,0);let m=0,g=0,_=0,p=0,u=0,w=0,b=0,S=0,T=0,y=0,A=0;l.sort(Gp);for(let x=0,v=l.length;x<v;x++){const C=l[x],F=C.color,N=C.intensity,P=C.distance,U=C.shadow&&C.shadow.map?C.shadow.map.texture:null;if(C.isAmbientLight)d+=F.r*N,h+=F.g*N,f+=F.b*N;else if(C.isLightProbe){for(let z=0;z<9;z++)i.probe[z].addScaledVector(C.sh.coefficients[z],N);A++}else if(C.isDirectionalLight){const z=e.get(C);if(z.color.copy(C.color).multiplyScalar(C.intensity),C.castShadow){const H=C.shadow,I=t.get(C);I.shadowIntensity=H.intensity,I.shadowBias=H.bias,I.shadowNormalBias=H.normalBias,I.shadowRadius=H.radius,I.shadowMapSize=H.mapSize,i.directionalShadow[m]=I,i.directionalShadowMap[m]=U,i.directionalShadowMatrix[m]=C.shadow.matrix,w++}i.directional[m]=z,m++}else if(C.isSpotLight){const z=e.get(C);z.position.setFromMatrixPosition(C.matrixWorld),z.color.copy(F).multiplyScalar(N),z.distance=P,z.coneCos=Math.cos(C.angle),z.penumbraCos=Math.cos(C.angle*(1-C.penumbra)),z.decay=C.decay,i.spot[_]=z;const H=C.shadow;if(C.map&&(i.spotLightMap[T]=C.map,T++,H.updateMatrices(C),C.castShadow&&y++),i.spotLightMatrix[_]=H.matrix,C.castShadow){const I=t.get(C);I.shadowIntensity=H.intensity,I.shadowBias=H.bias,I.shadowNormalBias=H.normalBias,I.shadowRadius=H.radius,I.shadowMapSize=H.mapSize,i.spotShadow[_]=I,i.spotShadowMap[_]=U,S++}_++}else if(C.isRectAreaLight){const z=e.get(C);z.color.copy(F).multiplyScalar(N),z.halfWidth.set(C.width*.5,0,0),z.halfHeight.set(0,C.height*.5,0),i.rectArea[p]=z,p++}else if(C.isPointLight){const z=e.get(C);if(z.color.copy(C.color).multiplyScalar(C.intensity),z.distance=C.distance,z.decay=C.decay,C.castShadow){const H=C.shadow,I=t.get(C);I.shadowIntensity=H.intensity,I.shadowBias=H.bias,I.shadowNormalBias=H.normalBias,I.shadowRadius=H.radius,I.shadowMapSize=H.mapSize,I.shadowCameraNear=H.camera.near,I.shadowCameraFar=H.camera.far,i.pointShadow[g]=I,i.pointShadowMap[g]=U,i.pointShadowMatrix[g]=C.shadow.matrix,b++}i.point[g]=z,g++}else if(C.isHemisphereLight){const z=e.get(C);z.skyColor.copy(C.color).multiplyScalar(N),z.groundColor.copy(C.groundColor).multiplyScalar(N),i.hemi[u]=z,u++}}p>0&&(n.has("OES_texture_float_linear")===!0?(i.rectAreaLTC1=he.LTC_FLOAT_1,i.rectAreaLTC2=he.LTC_FLOAT_2):(i.rectAreaLTC1=he.LTC_HALF_1,i.rectAreaLTC2=he.LTC_HALF_2)),i.ambient[0]=d,i.ambient[1]=h,i.ambient[2]=f;const D=i.hash;(D.directionalLength!==m||D.pointLength!==g||D.spotLength!==_||D.rectAreaLength!==p||D.hemiLength!==u||D.numDirectionalShadows!==w||D.numPointShadows!==b||D.numSpotShadows!==S||D.numSpotMaps!==T||D.numLightProbes!==A)&&(i.directional.length=m,i.spot.length=_,i.rectArea.length=p,i.point.length=g,i.hemi.length=u,i.directionalShadow.length=w,i.directionalShadowMap.length=w,i.pointShadow.length=b,i.pointShadowMap.length=b,i.spotShadow.length=S,i.spotShadowMap.length=S,i.directionalShadowMatrix.length=w,i.pointShadowMatrix.length=b,i.spotLightMatrix.length=S+T-y,i.spotLightMap.length=T,i.numSpotLightShadowsWithMaps=y,i.numLightProbes=A,D.directionalLength=m,D.pointLength=g,D.spotLength=_,D.rectAreaLength=p,D.hemiLength=u,D.numDirectionalShadows=w,D.numPointShadows=b,D.numSpotShadows=S,D.numSpotMaps=T,D.numLightProbes=A,i.version=Vp++)}function c(l,d){let h=0,f=0,m=0,g=0,_=0;const p=d.matrixWorldInverse;for(let u=0,w=l.length;u<w;u++){const b=l[u];if(b.isDirectionalLight){const S=i.directional[h];S.direction.setFromMatrixPosition(b.matrixWorld),r.setFromMatrixPosition(b.target.matrixWorld),S.direction.sub(r),S.direction.transformDirection(p),h++}else if(b.isSpotLight){const S=i.spot[m];S.position.setFromMatrixPosition(b.matrixWorld),S.position.applyMatrix4(p),S.direction.setFromMatrixPosition(b.matrixWorld),r.setFromMatrixPosition(b.target.matrixWorld),S.direction.sub(r),S.direction.transformDirection(p),m++}else if(b.isRectAreaLight){const S=i.rectArea[g];S.position.setFromMatrixPosition(b.matrixWorld),S.position.applyMatrix4(p),s.identity(),a.copy(b.matrixWorld),a.premultiply(p),s.extractRotation(a),S.halfWidth.set(b.width*.5,0,0),S.halfHeight.set(0,b.height*.5,0),S.halfWidth.applyMatrix4(s),S.halfHeight.applyMatrix4(s),g++}else if(b.isPointLight){const S=i.point[f];S.position.setFromMatrixPosition(b.matrixWorld),S.position.applyMatrix4(p),f++}else if(b.isHemisphereLight){const S=i.hemi[_];S.direction.setFromMatrixPosition(b.matrixWorld),S.direction.transformDirection(p),_++}}}return{setup:o,setupView:c,state:i}}function Jo(n){const e=new jp(n),t=[],i=[];function r(d){l.camera=d,t.length=0,i.length=0}function a(d){t.push(d)}function s(d){i.push(d)}function o(){e.setup(t)}function c(d){e.setupView(t,d)}const l={lightsArray:t,shadowsArray:i,camera:null,lights:e,transmissionRenderTarget:{}};return{init:r,state:l,setupLights:o,setupLightsView:c,pushLight:a,pushShadow:s}}function Wp(n){let e=new WeakMap;function t(r,a=0){const s=e.get(r);let o;return s===void 0?(o=new Jo(n),e.set(r,[o])):a>=s.length?(o=new Jo(n),s.push(o)):o=s[a],o}function i(){e=new WeakMap}return{get:t,dispose:i}}const Xp=`void main() {
	gl_Position = vec4( position, 1.0 );
}`,Yp=`uniform sampler2D shadow_pass;
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
}`;function qp(n,e,t){let i=new Us;const r=new Xe,a=new Xe,s=new lt,o=new _u({depthPacking:Pl}),c=new vu,l={},d=t.maxTextureSize,h={[An]:Rt,[Rt]:An,[kt]:kt},f=new wn({defines:{VSM_SAMPLES:8},uniforms:{shadow_pass:{value:null},resolution:{value:new Xe},radius:{value:4}},vertexShader:Xp,fragmentShader:Yp}),m=f.clone();m.defines.HORIZONTAL_PASS=1;const g=new st;g.setAttribute("position",new Zt(new Float32Array([-1,-1,.5,3,-1,.5,-1,3,.5]),3));const _=new it(g,f),p=this;this.enabled=!1,this.autoUpdate=!0,this.needsUpdate=!1,this.type=ac;let u=this.type;this.render=function(y,A,D){if(p.enabled===!1||p.autoUpdate===!1&&p.needsUpdate===!1||y.length===0)return;const x=n.getRenderTarget(),v=n.getActiveCubeFace(),C=n.getActiveMipmapLevel(),F=n.state;F.setBlending(bn),F.buffers.color.setClear(1,1,1,1),F.buffers.depth.setTest(!0),F.setScissorTest(!1);const N=u!==cn&&this.type===cn,P=u===cn&&this.type!==cn;for(let U=0,z=y.length;U<z;U++){const H=y[U],I=H.shadow;if(I===void 0){console.warn("THREE.WebGLShadowMap:",H,"has no shadow.");continue}if(I.autoUpdate===!1&&I.needsUpdate===!1)continue;r.copy(I.mapSize);const G=I.getFrameExtents();if(r.multiply(G),a.copy(I.mapSize),(r.x>d||r.y>d)&&(r.x>d&&(a.x=Math.floor(d/G.x),r.x=a.x*G.x,I.mapSize.x=a.x),r.y>d&&(a.y=Math.floor(d/G.y),r.y=a.y*G.y,I.mapSize.y=a.y)),I.map===null||N===!0||P===!0){const oe=this.type!==cn?{minFilter:qt,magFilter:qt}:{};I.map!==null&&I.map.dispose(),I.map=new qn(r.x,r.y,oe),I.map.texture.name=H.name+".shadowMap",I.camera.updateProjectionMatrix()}n.setRenderTarget(I.map),n.clear();const q=I.getViewportCount();for(let oe=0;oe<q;oe++){const le=I.getViewport(oe);s.set(a.x*le.x,a.y*le.y,a.x*le.z,a.y*le.w),F.viewport(s),I.updateMatrices(H,oe),i=I.getFrustum(),S(A,D,I.camera,H,this.type)}I.isPointLightShadow!==!0&&this.type===cn&&w(I,D),I.needsUpdate=!1}u=this.type,p.needsUpdate=!1,n.setRenderTarget(x,v,C)};function w(y,A){const D=e.update(_);f.defines.VSM_SAMPLES!==y.blurSamples&&(f.defines.VSM_SAMPLES=y.blurSamples,m.defines.VSM_SAMPLES=y.blurSamples,f.needsUpdate=!0,m.needsUpdate=!0),y.mapPass===null&&(y.mapPass=new qn(r.x,r.y)),f.uniforms.shadow_pass.value=y.map.texture,f.uniforms.resolution.value=y.mapSize,f.uniforms.radius.value=y.radius,n.setRenderTarget(y.mapPass),n.clear(),n.renderBufferDirect(A,null,D,f,_,null),m.uniforms.shadow_pass.value=y.mapPass.texture,m.uniforms.resolution.value=y.mapSize,m.uniforms.radius.value=y.radius,n.setRenderTarget(y.map),n.clear(),n.renderBufferDirect(A,null,D,m,_,null)}function b(y,A,D,x){let v=null;const C=D.isPointLight===!0?y.customDistanceMaterial:y.customDepthMaterial;if(C!==void 0)v=C;else if(v=D.isPointLight===!0?c:o,n.localClippingEnabled&&A.clipShadows===!0&&Array.isArray(A.clippingPlanes)&&A.clippingPlanes.length!==0||A.displacementMap&&A.displacementScale!==0||A.alphaMap&&A.alphaTest>0||A.map&&A.alphaTest>0){const F=v.uuid,N=A.uuid;let P=l[F];P===void 0&&(P={},l[F]=P);let U=P[N];U===void 0&&(U=v.clone(),P[N]=U,A.addEventListener("dispose",T)),v=U}if(v.visible=A.visible,v.wireframe=A.wireframe,x===cn?v.side=A.shadowSide!==null?A.shadowSide:A.side:v.side=A.shadowSide!==null?A.shadowSide:h[A.side],v.alphaMap=A.alphaMap,v.alphaTest=A.alphaTest,v.map=A.map,v.clipShadows=A.clipShadows,v.clippingPlanes=A.clippingPlanes,v.clipIntersection=A.clipIntersection,v.displacementMap=A.displacementMap,v.displacementScale=A.displacementScale,v.displacementBias=A.displacementBias,v.wireframeLinewidth=A.wireframeLinewidth,v.linewidth=A.linewidth,D.isPointLight===!0&&v.isMeshDistanceMaterial===!0){const F=n.properties.get(v);F.light=D}return v}function S(y,A,D,x,v){if(y.visible===!1)return;if(y.layers.test(A.layers)&&(y.isMesh||y.isLine||y.isPoints)&&(y.castShadow||y.receiveShadow&&v===cn)&&(!y.frustumCulled||i.intersectsObject(y))){y.modelViewMatrix.multiplyMatrices(D.matrixWorldInverse,y.matrixWorld);const N=e.update(y),P=y.material;if(Array.isArray(P)){const U=N.groups;for(let z=0,H=U.length;z<H;z++){const I=U[z],G=P[I.materialIndex];if(G&&G.visible){const q=b(y,G,x,v);y.onBeforeShadow(n,y,A,D,N,q,I),n.renderBufferDirect(D,null,N,q,y,I),y.onAfterShadow(n,y,A,D,N,q,I)}}}else if(P.visible){const U=b(y,P,x,v);y.onBeforeShadow(n,y,A,D,N,U,null),n.renderBufferDirect(D,null,N,U,y,null),y.onAfterShadow(n,y,A,D,N,U,null)}}const F=y.children;for(let N=0,P=F.length;N<P;N++)S(F[N],A,D,x,v)}function T(y){y.target.removeEventListener("dispose",T);for(const D in l){const x=l[D],v=y.target.uuid;v in x&&(x[v].dispose(),delete x[v])}}}const $p={[Da]:La,[Ia]:Fa,[Ua]:za,[Mi]:Na,[La]:Da,[Fa]:Ia,[za]:Ua,[Na]:Mi};function Kp(n,e){function t(){let O=!1;const fe=new lt;let $=null;const ee=new lt(0,0,0,0);return{setMask:function(xe){$!==xe&&!O&&(n.colorMask(xe,xe,xe,xe),$=xe)},setLocked:function(xe){O=xe},setClear:function(xe,_e,Oe,ot,vt){vt===!0&&(xe*=ot,_e*=ot,Oe*=ot),fe.set(xe,_e,Oe,ot),ee.equals(fe)===!1&&(n.clearColor(xe,_e,Oe,ot),ee.copy(fe))},reset:function(){O=!1,$=null,ee.set(-1,0,0,0)}}}function i(){let O=!1,fe=!1,$=null,ee=null,xe=null;return{setReversed:function(_e){if(fe!==_e){const Oe=e.get("EXT_clip_control");fe?Oe.clipControlEXT(Oe.LOWER_LEFT_EXT,Oe.ZERO_TO_ONE_EXT):Oe.clipControlEXT(Oe.LOWER_LEFT_EXT,Oe.NEGATIVE_ONE_TO_ONE_EXT);const ot=xe;xe=null,this.setClear(ot)}fe=_e},getReversed:function(){return fe},setTest:function(_e){_e?se(n.DEPTH_TEST):Q(n.DEPTH_TEST)},setMask:function(_e){$!==_e&&!O&&(n.depthMask(_e),$=_e)},setFunc:function(_e){if(fe&&(_e=$p[_e]),ee!==_e){switch(_e){case Da:n.depthFunc(n.NEVER);break;case La:n.depthFunc(n.ALWAYS);break;case Ia:n.depthFunc(n.LESS);break;case Mi:n.depthFunc(n.LEQUAL);break;case Ua:n.depthFunc(n.EQUAL);break;case Na:n.depthFunc(n.GEQUAL);break;case Fa:n.depthFunc(n.GREATER);break;case za:n.depthFunc(n.NOTEQUAL);break;default:n.depthFunc(n.LEQUAL)}ee=_e}},setLocked:function(_e){O=_e},setClear:function(_e){xe!==_e&&(fe&&(_e=1-_e),n.clearDepth(_e),xe=_e)},reset:function(){O=!1,$=null,ee=null,xe=null,fe=!1}}}function r(){let O=!1,fe=null,$=null,ee=null,xe=null,_e=null,Oe=null,ot=null,vt=null;return{setTest:function(Qe){O||(Qe?se(n.STENCIL_TEST):Q(n.STENCIL_TEST))},setMask:function(Qe){fe!==Qe&&!O&&(n.stencilMask(Qe),fe=Qe)},setFunc:function(Qe,Ht,Qt){($!==Qe||ee!==Ht||xe!==Qt)&&(n.stencilFunc(Qe,Ht,Qt),$=Qe,ee=Ht,xe=Qt)},setOp:function(Qe,Ht,Qt){(_e!==Qe||Oe!==Ht||ot!==Qt)&&(n.stencilOp(Qe,Ht,Qt),_e=Qe,Oe=Ht,ot=Qt)},setLocked:function(Qe){O=Qe},setClear:function(Qe){vt!==Qe&&(n.clearStencil(Qe),vt=Qe)},reset:function(){O=!1,fe=null,$=null,ee=null,xe=null,_e=null,Oe=null,ot=null,vt=null}}}const a=new t,s=new i,o=new r,c=new WeakMap,l=new WeakMap;let d={},h={},f=new WeakMap,m=[],g=null,_=!1,p=null,u=null,w=null,b=null,S=null,T=null,y=null,A=new ve(0,0,0),D=0,x=!1,v=null,C=null,F=null,N=null,P=null;const U=n.getParameter(n.MAX_COMBINED_TEXTURE_IMAGE_UNITS);let z=!1,H=0;const I=n.getParameter(n.VERSION);I.indexOf("WebGL")!==-1?(H=parseFloat(/^WebGL (\d)/.exec(I)[1]),z=H>=1):I.indexOf("OpenGL ES")!==-1&&(H=parseFloat(/^OpenGL ES (\d)/.exec(I)[1]),z=H>=2);let G=null,q={};const oe=n.getParameter(n.SCISSOR_BOX),le=n.getParameter(n.VIEWPORT),Re=new lt().fromArray(oe),Y=new lt().fromArray(le);function te(O,fe,$,ee){const xe=new Uint8Array(4),_e=n.createTexture();n.bindTexture(O,_e),n.texParameteri(O,n.TEXTURE_MIN_FILTER,n.NEAREST),n.texParameteri(O,n.TEXTURE_MAG_FILTER,n.NEAREST);for(let Oe=0;Oe<$;Oe++)O===n.TEXTURE_3D||O===n.TEXTURE_2D_ARRAY?n.texImage3D(fe,0,n.RGBA,1,1,ee,0,n.RGBA,n.UNSIGNED_BYTE,xe):n.texImage2D(fe+Oe,0,n.RGBA,1,1,0,n.RGBA,n.UNSIGNED_BYTE,xe);return _e}const de={};de[n.TEXTURE_2D]=te(n.TEXTURE_2D,n.TEXTURE_2D,1),de[n.TEXTURE_CUBE_MAP]=te(n.TEXTURE_CUBE_MAP,n.TEXTURE_CUBE_MAP_POSITIVE_X,6),de[n.TEXTURE_2D_ARRAY]=te(n.TEXTURE_2D_ARRAY,n.TEXTURE_2D_ARRAY,1,1),de[n.TEXTURE_3D]=te(n.TEXTURE_3D,n.TEXTURE_3D,1,1),a.setClear(0,0,0,1),s.setClear(1),o.setClear(0),se(n.DEPTH_TEST),s.setFunc(Mi),Pe(!1),Ce(qs),se(n.CULL_FACE),L(bn);function se(O){d[O]!==!0&&(n.enable(O),d[O]=!0)}function Q(O){d[O]!==!1&&(n.disable(O),d[O]=!1)}function ge(O,fe){return h[O]!==fe?(n.bindFramebuffer(O,fe),h[O]=fe,O===n.DRAW_FRAMEBUFFER&&(h[n.FRAMEBUFFER]=fe),O===n.FRAMEBUFFER&&(h[n.DRAW_FRAMEBUFFER]=fe),!0):!1}function ue(O,fe){let $=m,ee=!1;if(O){$=f.get(fe),$===void 0&&($=[],f.set(fe,$));const xe=O.textures;if($.length!==xe.length||$[0]!==n.COLOR_ATTACHMENT0){for(let _e=0,Oe=xe.length;_e<Oe;_e++)$[_e]=n.COLOR_ATTACHMENT0+_e;$.length=xe.length,ee=!0}}else $[0]!==n.BACK&&($[0]=n.BACK,ee=!0);ee&&n.drawBuffers($)}function K(O){return g!==O?(n.useProgram(O),g=O,!0):!1}const ie={[Hn]:n.FUNC_ADD,[nl]:n.FUNC_SUBTRACT,[il]:n.FUNC_REVERSE_SUBTRACT};ie[rl]=n.MIN,ie[al]=n.MAX;const ae={[sl]:n.ZERO,[ol]:n.ONE,[cl]:n.SRC_COLOR,[Ca]:n.SRC_ALPHA,[pl]:n.SRC_ALPHA_SATURATE,[hl]:n.DST_COLOR,[ul]:n.DST_ALPHA,[ll]:n.ONE_MINUS_SRC_COLOR,[Pa]:n.ONE_MINUS_SRC_ALPHA,[fl]:n.ONE_MINUS_DST_COLOR,[dl]:n.ONE_MINUS_DST_ALPHA,[ml]:n.CONSTANT_COLOR,[gl]:n.ONE_MINUS_CONSTANT_COLOR,[_l]:n.CONSTANT_ALPHA,[vl]:n.ONE_MINUS_CONSTANT_ALPHA};function L(O,fe,$,ee,xe,_e,Oe,ot,vt,Qe){if(O===bn){_===!0&&(Q(n.BLEND),_=!1);return}if(_===!1&&(se(n.BLEND),_=!0),O!==tl){if(O!==p||Qe!==x){if((u!==Hn||S!==Hn)&&(n.blendEquation(n.FUNC_ADD),u=Hn,S=Hn),Qe)switch(O){case gi:n.blendFuncSeparate(n.ONE,n.ONE_MINUS_SRC_ALPHA,n.ONE,n.ONE_MINUS_SRC_ALPHA);break;case $s:n.blendFunc(n.ONE,n.ONE);break;case Ks:n.blendFuncSeparate(n.ZERO,n.ONE_MINUS_SRC_COLOR,n.ZERO,n.ONE);break;case Zs:n.blendFuncSeparate(n.ZERO,n.SRC_COLOR,n.ZERO,n.SRC_ALPHA);break;default:console.error("THREE.WebGLState: Invalid blending: ",O);break}else switch(O){case gi:n.blendFuncSeparate(n.SRC_ALPHA,n.ONE_MINUS_SRC_ALPHA,n.ONE,n.ONE_MINUS_SRC_ALPHA);break;case $s:n.blendFunc(n.SRC_ALPHA,n.ONE);break;case Ks:n.blendFuncSeparate(n.ZERO,n.ONE_MINUS_SRC_COLOR,n.ZERO,n.ONE);break;case Zs:n.blendFunc(n.ZERO,n.SRC_COLOR);break;default:console.error("THREE.WebGLState: Invalid blending: ",O);break}w=null,b=null,T=null,y=null,A.set(0,0,0),D=0,p=O,x=Qe}return}xe=xe||fe,_e=_e||$,Oe=Oe||ee,(fe!==u||xe!==S)&&(n.blendEquationSeparate(ie[fe],ie[xe]),u=fe,S=xe),($!==w||ee!==b||_e!==T||Oe!==y)&&(n.blendFuncSeparate(ae[$],ae[ee],ae[_e],ae[Oe]),w=$,b=ee,T=_e,y=Oe),(ot.equals(A)===!1||vt!==D)&&(n.blendColor(ot.r,ot.g,ot.b,vt),A.copy(ot),D=vt),p=O,x=!1}function Ie(O,fe){O.side===kt?Q(n.CULL_FACE):se(n.CULL_FACE);let $=O.side===Rt;fe&&($=!$),Pe($),O.blending===gi&&O.transparent===!1?L(bn):L(O.blending,O.blendEquation,O.blendSrc,O.blendDst,O.blendEquationAlpha,O.blendSrcAlpha,O.blendDstAlpha,O.blendColor,O.blendAlpha,O.premultipliedAlpha),s.setFunc(O.depthFunc),s.setTest(O.depthTest),s.setMask(O.depthWrite),a.setMask(O.colorWrite);const ee=O.stencilWrite;o.setTest(ee),ee&&(o.setMask(O.stencilWriteMask),o.setFunc(O.stencilFunc,O.stencilRef,O.stencilFuncMask),o.setOp(O.stencilFail,O.stencilZFail,O.stencilZPass)),ke(O.polygonOffset,O.polygonOffsetFactor,O.polygonOffsetUnits),O.alphaToCoverage===!0?se(n.SAMPLE_ALPHA_TO_COVERAGE):Q(n.SAMPLE_ALPHA_TO_COVERAGE)}function Pe(O){v!==O&&(O?n.frontFace(n.CW):n.frontFace(n.CCW),v=O)}function Ce(O){O!==Jc?(se(n.CULL_FACE),O!==C&&(O===qs?n.cullFace(n.BACK):O===Qc?n.cullFace(n.FRONT):n.cullFace(n.FRONT_AND_BACK))):Q(n.CULL_FACE),C=O}function Me(O){O!==F&&(z&&n.lineWidth(O),F=O)}function ke(O,fe,$){O?(se(n.POLYGON_OFFSET_FILL),(N!==fe||P!==$)&&(n.polygonOffset(fe,$),N=fe,P=$)):Q(n.POLYGON_OFFSET_FILL)}function we(O){O?se(n.SCISSOR_TEST):Q(n.SCISSOR_TEST)}function R(O){O===void 0&&(O=n.TEXTURE0+U-1),G!==O&&(n.activeTexture(O),G=O)}function M(O,fe,$){$===void 0&&(G===null?$=n.TEXTURE0+U-1:$=G);let ee=q[$];ee===void 0&&(ee={type:void 0,texture:void 0},q[$]=ee),(ee.type!==O||ee.texture!==fe)&&(G!==$&&(n.activeTexture($),G=$),n.bindTexture(O,fe||de[O]),ee.type=O,ee.texture=fe)}function j(){const O=q[G];O!==void 0&&O.type!==void 0&&(n.bindTexture(O.type,null),O.type=void 0,O.texture=void 0)}function J(){try{n.compressedTexImage2D(...arguments)}catch(O){console.error("THREE.WebGLState:",O)}}function ne(){try{n.compressedTexImage3D(...arguments)}catch(O){console.error("THREE.WebGLState:",O)}}function Z(){try{n.texSubImage2D(...arguments)}catch(O){console.error("THREE.WebGLState:",O)}}function Ae(){try{n.texSubImage3D(...arguments)}catch(O){console.error("THREE.WebGLState:",O)}}function me(){try{n.compressedTexSubImage2D(...arguments)}catch(O){console.error("THREE.WebGLState:",O)}}function Ee(){try{n.compressedTexSubImage3D(...arguments)}catch(O){console.error("THREE.WebGLState:",O)}}function Ye(){try{n.texStorage2D(...arguments)}catch(O){console.error("THREE.WebGLState:",O)}}function ce(){try{n.texStorage3D(...arguments)}catch(O){console.error("THREE.WebGLState:",O)}}function ye(){try{n.texImage2D(...arguments)}catch(O){console.error("THREE.WebGLState:",O)}}function Ue(){try{n.texImage3D(...arguments)}catch(O){console.error("THREE.WebGLState:",O)}}function Ne(O){Re.equals(O)===!1&&(n.scissor(O.x,O.y,O.z,O.w),Re.copy(O))}function be(O){Y.equals(O)===!1&&(n.viewport(O.x,O.y,O.z,O.w),Y.copy(O))}function We(O,fe){let $=l.get(fe);$===void 0&&($=new WeakMap,l.set(fe,$));let ee=$.get(O);ee===void 0&&(ee=n.getUniformBlockIndex(fe,O.name),$.set(O,ee))}function He(O,fe){const ee=l.get(fe).get(O);c.get(fe)!==ee&&(n.uniformBlockBinding(fe,ee,O.__bindingPointIndex),c.set(fe,ee))}function tt(){n.disable(n.BLEND),n.disable(n.CULL_FACE),n.disable(n.DEPTH_TEST),n.disable(n.POLYGON_OFFSET_FILL),n.disable(n.SCISSOR_TEST),n.disable(n.STENCIL_TEST),n.disable(n.SAMPLE_ALPHA_TO_COVERAGE),n.blendEquation(n.FUNC_ADD),n.blendFunc(n.ONE,n.ZERO),n.blendFuncSeparate(n.ONE,n.ZERO,n.ONE,n.ZERO),n.blendColor(0,0,0,0),n.colorMask(!0,!0,!0,!0),n.clearColor(0,0,0,0),n.depthMask(!0),n.depthFunc(n.LESS),s.setReversed(!1),n.clearDepth(1),n.stencilMask(4294967295),n.stencilFunc(n.ALWAYS,0,4294967295),n.stencilOp(n.KEEP,n.KEEP,n.KEEP),n.clearStencil(0),n.cullFace(n.BACK),n.frontFace(n.CCW),n.polygonOffset(0,0),n.activeTexture(n.TEXTURE0),n.bindFramebuffer(n.FRAMEBUFFER,null),n.bindFramebuffer(n.DRAW_FRAMEBUFFER,null),n.bindFramebuffer(n.READ_FRAMEBUFFER,null),n.useProgram(null),n.lineWidth(1),n.scissor(0,0,n.canvas.width,n.canvas.height),n.viewport(0,0,n.canvas.width,n.canvas.height),d={},G=null,q={},h={},f=new WeakMap,m=[],g=null,_=!1,p=null,u=null,w=null,b=null,S=null,T=null,y=null,A=new ve(0,0,0),D=0,x=!1,v=null,C=null,F=null,N=null,P=null,Re.set(0,0,n.canvas.width,n.canvas.height),Y.set(0,0,n.canvas.width,n.canvas.height),a.reset(),s.reset(),o.reset()}return{buffers:{color:a,depth:s,stencil:o},enable:se,disable:Q,bindFramebuffer:ge,drawBuffers:ue,useProgram:K,setBlending:L,setMaterial:Ie,setFlipSided:Pe,setCullFace:Ce,setLineWidth:Me,setPolygonOffset:ke,setScissorTest:we,activeTexture:R,bindTexture:M,unbindTexture:j,compressedTexImage2D:J,compressedTexImage3D:ne,texImage2D:ye,texImage3D:Ue,updateUBOMapping:We,uniformBlockBinding:He,texStorage2D:Ye,texStorage3D:ce,texSubImage2D:Z,texSubImage3D:Ae,compressedTexSubImage2D:me,compressedTexSubImage3D:Ee,scissor:Ne,viewport:be,reset:tt}}function Zp(n,e,t,i,r,a,s){const o=e.has("WEBGL_multisampled_render_to_texture")?e.get("WEBGL_multisampled_render_to_texture"):null,c=typeof navigator>"u"?!1:/OculusBrowser/g.test(navigator.userAgent),l=new Xe,d=new WeakMap;let h;const f=new WeakMap;let m=!1;try{m=typeof OffscreenCanvas<"u"&&new OffscreenCanvas(1,1).getContext("2d")!==null}catch{}function g(R,M){return m?new OffscreenCanvas(R,M):Lr("canvas")}function _(R,M,j){let J=1;const ne=we(R);if((ne.width>j||ne.height>j)&&(J=j/Math.max(ne.width,ne.height)),J<1)if(typeof HTMLImageElement<"u"&&R instanceof HTMLImageElement||typeof HTMLCanvasElement<"u"&&R instanceof HTMLCanvasElement||typeof ImageBitmap<"u"&&R instanceof ImageBitmap||typeof VideoFrame<"u"&&R instanceof VideoFrame){const Z=Math.floor(J*ne.width),Ae=Math.floor(J*ne.height);h===void 0&&(h=g(Z,Ae));const me=M?g(Z,Ae):h;return me.width=Z,me.height=Ae,me.getContext("2d").drawImage(R,0,0,Z,Ae),console.warn("THREE.WebGLRenderer: Texture has been resized from ("+ne.width+"x"+ne.height+") to ("+Z+"x"+Ae+")."),me}else return"data"in R&&console.warn("THREE.WebGLRenderer: Image in DataTexture is too big ("+ne.width+"x"+ne.height+")."),R;return R}function p(R){return R.generateMipmaps}function u(R){n.generateMipmap(R)}function w(R){return R.isWebGLCubeRenderTarget?n.TEXTURE_CUBE_MAP:R.isWebGL3DRenderTarget?n.TEXTURE_3D:R.isWebGLArrayRenderTarget||R.isCompressedArrayTexture?n.TEXTURE_2D_ARRAY:n.TEXTURE_2D}function b(R,M,j,J,ne=!1){if(R!==null){if(n[R]!==void 0)return n[R];console.warn("THREE.WebGLRenderer: Attempt to use non-existing WebGL internal format '"+R+"'")}let Z=M;if(M===n.RED&&(j===n.FLOAT&&(Z=n.R32F),j===n.HALF_FLOAT&&(Z=n.R16F),j===n.UNSIGNED_BYTE&&(Z=n.R8)),M===n.RED_INTEGER&&(j===n.UNSIGNED_BYTE&&(Z=n.R8UI),j===n.UNSIGNED_SHORT&&(Z=n.R16UI),j===n.UNSIGNED_INT&&(Z=n.R32UI),j===n.BYTE&&(Z=n.R8I),j===n.SHORT&&(Z=n.R16I),j===n.INT&&(Z=n.R32I)),M===n.RG&&(j===n.FLOAT&&(Z=n.RG32F),j===n.HALF_FLOAT&&(Z=n.RG16F),j===n.UNSIGNED_BYTE&&(Z=n.RG8)),M===n.RG_INTEGER&&(j===n.UNSIGNED_BYTE&&(Z=n.RG8UI),j===n.UNSIGNED_SHORT&&(Z=n.RG16UI),j===n.UNSIGNED_INT&&(Z=n.RG32UI),j===n.BYTE&&(Z=n.RG8I),j===n.SHORT&&(Z=n.RG16I),j===n.INT&&(Z=n.RG32I)),M===n.RGB_INTEGER&&(j===n.UNSIGNED_BYTE&&(Z=n.RGB8UI),j===n.UNSIGNED_SHORT&&(Z=n.RGB16UI),j===n.UNSIGNED_INT&&(Z=n.RGB32UI),j===n.BYTE&&(Z=n.RGB8I),j===n.SHORT&&(Z=n.RGB16I),j===n.INT&&(Z=n.RGB32I)),M===n.RGBA_INTEGER&&(j===n.UNSIGNED_BYTE&&(Z=n.RGBA8UI),j===n.UNSIGNED_SHORT&&(Z=n.RGBA16UI),j===n.UNSIGNED_INT&&(Z=n.RGBA32UI),j===n.BYTE&&(Z=n.RGBA8I),j===n.SHORT&&(Z=n.RGBA16I),j===n.INT&&(Z=n.RGBA32I)),M===n.RGB&&j===n.UNSIGNED_INT_5_9_9_9_REV&&(Z=n.RGB9_E5),M===n.RGBA){const Ae=ne?Pr:Ke.getTransfer(J);j===n.FLOAT&&(Z=n.RGBA32F),j===n.HALF_FLOAT&&(Z=n.RGBA16F),j===n.UNSIGNED_BYTE&&(Z=Ae===et?n.SRGB8_ALPHA8:n.RGBA8),j===n.UNSIGNED_SHORT_4_4_4_4&&(Z=n.RGBA4),j===n.UNSIGNED_SHORT_5_5_5_1&&(Z=n.RGB5_A1)}return(Z===n.R16F||Z===n.R32F||Z===n.RG16F||Z===n.RG32F||Z===n.RGBA16F||Z===n.RGBA32F)&&e.get("EXT_color_buffer_float"),Z}function S(R,M){let j;return R?M===null||M===Yn||M===yi?j=n.DEPTH24_STENCIL8:M===un?j=n.DEPTH32F_STENCIL8:M===Oi&&(j=n.DEPTH24_STENCIL8,console.warn("DepthTexture: 16 bit depth attachment is not supported with stencil. Using 24-bit attachment.")):M===null||M===Yn||M===yi?j=n.DEPTH_COMPONENT24:M===un?j=n.DEPTH_COMPONENT32F:M===Oi&&(j=n.DEPTH_COMPONENT16),j}function T(R,M){return p(R)===!0||R.isFramebufferTexture&&R.minFilter!==qt&&R.minFilter!==Kt?Math.log2(Math.max(M.width,M.height))+1:R.mipmaps!==void 0&&R.mipmaps.length>0?R.mipmaps.length:R.isCompressedTexture&&Array.isArray(R.image)?M.mipmaps.length:1}function y(R){const M=R.target;M.removeEventListener("dispose",y),D(M),M.isVideoTexture&&d.delete(M)}function A(R){const M=R.target;M.removeEventListener("dispose",A),v(M)}function D(R){const M=i.get(R);if(M.__webglInit===void 0)return;const j=R.source,J=f.get(j);if(J){const ne=J[M.__cacheKey];ne.usedTimes--,ne.usedTimes===0&&x(R),Object.keys(J).length===0&&f.delete(j)}i.remove(R)}function x(R){const M=i.get(R);n.deleteTexture(M.__webglTexture);const j=R.source,J=f.get(j);delete J[M.__cacheKey],s.memory.textures--}function v(R){const M=i.get(R);if(R.depthTexture&&(R.depthTexture.dispose(),i.remove(R.depthTexture)),R.isWebGLCubeRenderTarget)for(let J=0;J<6;J++){if(Array.isArray(M.__webglFramebuffer[J]))for(let ne=0;ne<M.__webglFramebuffer[J].length;ne++)n.deleteFramebuffer(M.__webglFramebuffer[J][ne]);else n.deleteFramebuffer(M.__webglFramebuffer[J]);M.__webglDepthbuffer&&n.deleteRenderbuffer(M.__webglDepthbuffer[J])}else{if(Array.isArray(M.__webglFramebuffer))for(let J=0;J<M.__webglFramebuffer.length;J++)n.deleteFramebuffer(M.__webglFramebuffer[J]);else n.deleteFramebuffer(M.__webglFramebuffer);if(M.__webglDepthbuffer&&n.deleteRenderbuffer(M.__webglDepthbuffer),M.__webglMultisampledFramebuffer&&n.deleteFramebuffer(M.__webglMultisampledFramebuffer),M.__webglColorRenderbuffer)for(let J=0;J<M.__webglColorRenderbuffer.length;J++)M.__webglColorRenderbuffer[J]&&n.deleteRenderbuffer(M.__webglColorRenderbuffer[J]);M.__webglDepthRenderbuffer&&n.deleteRenderbuffer(M.__webglDepthRenderbuffer)}const j=R.textures;for(let J=0,ne=j.length;J<ne;J++){const Z=i.get(j[J]);Z.__webglTexture&&(n.deleteTexture(Z.__webglTexture),s.memory.textures--),i.remove(j[J])}i.remove(R)}let C=0;function F(){C=0}function N(){const R=C;return R>=r.maxTextures&&console.warn("THREE.WebGLTextures: Trying to use "+R+" texture units while this GPU supports only "+r.maxTextures),C+=1,R}function P(R){const M=[];return M.push(R.wrapS),M.push(R.wrapT),M.push(R.wrapR||0),M.push(R.magFilter),M.push(R.minFilter),M.push(R.anisotropy),M.push(R.internalFormat),M.push(R.format),M.push(R.type),M.push(R.generateMipmaps),M.push(R.premultiplyAlpha),M.push(R.flipY),M.push(R.unpackAlignment),M.push(R.colorSpace),M.join()}function U(R,M){const j=i.get(R);if(R.isVideoTexture&&Me(R),R.isRenderTargetTexture===!1&&R.version>0&&j.__version!==R.version){const J=R.image;if(J===null)console.warn("THREE.WebGLRenderer: Texture marked for update but no image data found.");else if(J.complete===!1)console.warn("THREE.WebGLRenderer: Texture marked for update but image is incomplete");else{Y(j,R,M);return}}t.bindTexture(n.TEXTURE_2D,j.__webglTexture,n.TEXTURE0+M)}function z(R,M){const j=i.get(R);if(R.version>0&&j.__version!==R.version){Y(j,R,M);return}t.bindTexture(n.TEXTURE_2D_ARRAY,j.__webglTexture,n.TEXTURE0+M)}function H(R,M){const j=i.get(R);if(R.version>0&&j.__version!==R.version){Y(j,R,M);return}t.bindTexture(n.TEXTURE_3D,j.__webglTexture,n.TEXTURE0+M)}function I(R,M){const j=i.get(R);if(R.version>0&&j.__version!==R.version){te(j,R,M);return}t.bindTexture(n.TEXTURE_CUBE_MAP,j.__webglTexture,n.TEXTURE0+M)}const G={[Ba]:n.REPEAT,[Gn]:n.CLAMP_TO_EDGE,[Ha]:n.MIRRORED_REPEAT},q={[qt]:n.NEAREST,[Rl]:n.NEAREST_MIPMAP_NEAREST,[qi]:n.NEAREST_MIPMAP_LINEAR,[Kt]:n.LINEAR,[Yr]:n.LINEAR_MIPMAP_NEAREST,[jn]:n.LINEAR_MIPMAP_LINEAR},oe={[Ll]:n.NEVER,[kl]:n.ALWAYS,[Il]:n.LESS,[xc]:n.LEQUAL,[Ul]:n.EQUAL,[zl]:n.GEQUAL,[Nl]:n.GREATER,[Fl]:n.NOTEQUAL};function le(R,M){if(M.type===un&&e.has("OES_texture_float_linear")===!1&&(M.magFilter===Kt||M.magFilter===Yr||M.magFilter===qi||M.magFilter===jn||M.minFilter===Kt||M.minFilter===Yr||M.minFilter===qi||M.minFilter===jn)&&console.warn("THREE.WebGLRenderer: Unable to use linear filtering with floating point textures. OES_texture_float_linear not supported on this device."),n.texParameteri(R,n.TEXTURE_WRAP_S,G[M.wrapS]),n.texParameteri(R,n.TEXTURE_WRAP_T,G[M.wrapT]),(R===n.TEXTURE_3D||R===n.TEXTURE_2D_ARRAY)&&n.texParameteri(R,n.TEXTURE_WRAP_R,G[M.wrapR]),n.texParameteri(R,n.TEXTURE_MAG_FILTER,q[M.magFilter]),n.texParameteri(R,n.TEXTURE_MIN_FILTER,q[M.minFilter]),M.compareFunction&&(n.texParameteri(R,n.TEXTURE_COMPARE_MODE,n.COMPARE_REF_TO_TEXTURE),n.texParameteri(R,n.TEXTURE_COMPARE_FUNC,oe[M.compareFunction])),e.has("EXT_texture_filter_anisotropic")===!0){if(M.magFilter===qt||M.minFilter!==qi&&M.minFilter!==jn||M.type===un&&e.has("OES_texture_float_linear")===!1)return;if(M.anisotropy>1||i.get(M).__currentAnisotropy){const j=e.get("EXT_texture_filter_anisotropic");n.texParameterf(R,j.TEXTURE_MAX_ANISOTROPY_EXT,Math.min(M.anisotropy,r.getMaxAnisotropy())),i.get(M).__currentAnisotropy=M.anisotropy}}}function Re(R,M){let j=!1;R.__webglInit===void 0&&(R.__webglInit=!0,M.addEventListener("dispose",y));const J=M.source;let ne=f.get(J);ne===void 0&&(ne={},f.set(J,ne));const Z=P(M);if(Z!==R.__cacheKey){ne[Z]===void 0&&(ne[Z]={texture:n.createTexture(),usedTimes:0},s.memory.textures++,j=!0),ne[Z].usedTimes++;const Ae=ne[R.__cacheKey];Ae!==void 0&&(ne[R.__cacheKey].usedTimes--,Ae.usedTimes===0&&x(M)),R.__cacheKey=Z,R.__webglTexture=ne[Z].texture}return j}function Y(R,M,j){let J=n.TEXTURE_2D;(M.isDataArrayTexture||M.isCompressedArrayTexture)&&(J=n.TEXTURE_2D_ARRAY),M.isData3DTexture&&(J=n.TEXTURE_3D);const ne=Re(R,M),Z=M.source;t.bindTexture(J,R.__webglTexture,n.TEXTURE0+j);const Ae=i.get(Z);if(Z.version!==Ae.__version||ne===!0){t.activeTexture(n.TEXTURE0+j);const me=Ke.getPrimaries(Ke.workingColorSpace),Ee=M.colorSpace===yn?null:Ke.getPrimaries(M.colorSpace),Ye=M.colorSpace===yn||me===Ee?n.NONE:n.BROWSER_DEFAULT_WEBGL;n.pixelStorei(n.UNPACK_FLIP_Y_WEBGL,M.flipY),n.pixelStorei(n.UNPACK_PREMULTIPLY_ALPHA_WEBGL,M.premultiplyAlpha),n.pixelStorei(n.UNPACK_ALIGNMENT,M.unpackAlignment),n.pixelStorei(n.UNPACK_COLORSPACE_CONVERSION_WEBGL,Ye);let ce=_(M.image,!1,r.maxTextureSize);ce=ke(M,ce);const ye=a.convert(M.format,M.colorSpace),Ue=a.convert(M.type);let Ne=b(M.internalFormat,ye,Ue,M.colorSpace,M.isVideoTexture);le(J,M);let be;const We=M.mipmaps,He=M.isVideoTexture!==!0,tt=Ae.__version===void 0||ne===!0,O=Z.dataReady,fe=T(M,ce);if(M.isDepthTexture)Ne=S(M.format===bi,M.type),tt&&(He?t.texStorage2D(n.TEXTURE_2D,1,Ne,ce.width,ce.height):t.texImage2D(n.TEXTURE_2D,0,Ne,ce.width,ce.height,0,ye,Ue,null));else if(M.isDataTexture)if(We.length>0){He&&tt&&t.texStorage2D(n.TEXTURE_2D,fe,Ne,We[0].width,We[0].height);for(let $=0,ee=We.length;$<ee;$++)be=We[$],He?O&&t.texSubImage2D(n.TEXTURE_2D,$,0,0,be.width,be.height,ye,Ue,be.data):t.texImage2D(n.TEXTURE_2D,$,Ne,be.width,be.height,0,ye,Ue,be.data);M.generateMipmaps=!1}else He?(tt&&t.texStorage2D(n.TEXTURE_2D,fe,Ne,ce.width,ce.height),O&&t.texSubImage2D(n.TEXTURE_2D,0,0,0,ce.width,ce.height,ye,Ue,ce.data)):t.texImage2D(n.TEXTURE_2D,0,Ne,ce.width,ce.height,0,ye,Ue,ce.data);else if(M.isCompressedTexture)if(M.isCompressedArrayTexture){He&&tt&&t.texStorage3D(n.TEXTURE_2D_ARRAY,fe,Ne,We[0].width,We[0].height,ce.depth);for(let $=0,ee=We.length;$<ee;$++)if(be=We[$],M.format!==Yt)if(ye!==null)if(He){if(O)if(M.layerUpdates.size>0){const xe=Ro(be.width,be.height,M.format,M.type);for(const _e of M.layerUpdates){const Oe=be.data.subarray(_e*xe/be.data.BYTES_PER_ELEMENT,(_e+1)*xe/be.data.BYTES_PER_ELEMENT);t.compressedTexSubImage3D(n.TEXTURE_2D_ARRAY,$,0,0,_e,be.width,be.height,1,ye,Oe)}M.clearLayerUpdates()}else t.compressedTexSubImage3D(n.TEXTURE_2D_ARRAY,$,0,0,0,be.width,be.height,ce.depth,ye,be.data)}else t.compressedTexImage3D(n.TEXTURE_2D_ARRAY,$,Ne,be.width,be.height,ce.depth,0,be.data,0,0);else console.warn("THREE.WebGLRenderer: Attempt to load unsupported compressed texture format in .uploadTexture()");else He?O&&t.texSubImage3D(n.TEXTURE_2D_ARRAY,$,0,0,0,be.width,be.height,ce.depth,ye,Ue,be.data):t.texImage3D(n.TEXTURE_2D_ARRAY,$,Ne,be.width,be.height,ce.depth,0,ye,Ue,be.data)}else{He&&tt&&t.texStorage2D(n.TEXTURE_2D,fe,Ne,We[0].width,We[0].height);for(let $=0,ee=We.length;$<ee;$++)be=We[$],M.format!==Yt?ye!==null?He?O&&t.compressedTexSubImage2D(n.TEXTURE_2D,$,0,0,be.width,be.height,ye,be.data):t.compressedTexImage2D(n.TEXTURE_2D,$,Ne,be.width,be.height,0,be.data):console.warn("THREE.WebGLRenderer: Attempt to load unsupported compressed texture format in .uploadTexture()"):He?O&&t.texSubImage2D(n.TEXTURE_2D,$,0,0,be.width,be.height,ye,Ue,be.data):t.texImage2D(n.TEXTURE_2D,$,Ne,be.width,be.height,0,ye,Ue,be.data)}else if(M.isDataArrayTexture)if(He){if(tt&&t.texStorage3D(n.TEXTURE_2D_ARRAY,fe,Ne,ce.width,ce.height,ce.depth),O)if(M.layerUpdates.size>0){const $=Ro(ce.width,ce.height,M.format,M.type);for(const ee of M.layerUpdates){const xe=ce.data.subarray(ee*$/ce.data.BYTES_PER_ELEMENT,(ee+1)*$/ce.data.BYTES_PER_ELEMENT);t.texSubImage3D(n.TEXTURE_2D_ARRAY,0,0,0,ee,ce.width,ce.height,1,ye,Ue,xe)}M.clearLayerUpdates()}else t.texSubImage3D(n.TEXTURE_2D_ARRAY,0,0,0,0,ce.width,ce.height,ce.depth,ye,Ue,ce.data)}else t.texImage3D(n.TEXTURE_2D_ARRAY,0,Ne,ce.width,ce.height,ce.depth,0,ye,Ue,ce.data);else if(M.isData3DTexture)He?(tt&&t.texStorage3D(n.TEXTURE_3D,fe,Ne,ce.width,ce.height,ce.depth),O&&t.texSubImage3D(n.TEXTURE_3D,0,0,0,0,ce.width,ce.height,ce.depth,ye,Ue,ce.data)):t.texImage3D(n.TEXTURE_3D,0,Ne,ce.width,ce.height,ce.depth,0,ye,Ue,ce.data);else if(M.isFramebufferTexture){if(tt)if(He)t.texStorage2D(n.TEXTURE_2D,fe,Ne,ce.width,ce.height);else{let $=ce.width,ee=ce.height;for(let xe=0;xe<fe;xe++)t.texImage2D(n.TEXTURE_2D,xe,Ne,$,ee,0,ye,Ue,null),$>>=1,ee>>=1}}else if(We.length>0){if(He&&tt){const $=we(We[0]);t.texStorage2D(n.TEXTURE_2D,fe,Ne,$.width,$.height)}for(let $=0,ee=We.length;$<ee;$++)be=We[$],He?O&&t.texSubImage2D(n.TEXTURE_2D,$,0,0,ye,Ue,be):t.texImage2D(n.TEXTURE_2D,$,Ne,ye,Ue,be);M.generateMipmaps=!1}else if(He){if(tt){const $=we(ce);t.texStorage2D(n.TEXTURE_2D,fe,Ne,$.width,$.height)}O&&t.texSubImage2D(n.TEXTURE_2D,0,0,0,ye,Ue,ce)}else t.texImage2D(n.TEXTURE_2D,0,Ne,ye,Ue,ce);p(M)&&u(J),Ae.__version=Z.version,M.onUpdate&&M.onUpdate(M)}R.__version=M.version}function te(R,M,j){if(M.image.length!==6)return;const J=Re(R,M),ne=M.source;t.bindTexture(n.TEXTURE_CUBE_MAP,R.__webglTexture,n.TEXTURE0+j);const Z=i.get(ne);if(ne.version!==Z.__version||J===!0){t.activeTexture(n.TEXTURE0+j);const Ae=Ke.getPrimaries(Ke.workingColorSpace),me=M.colorSpace===yn?null:Ke.getPrimaries(M.colorSpace),Ee=M.colorSpace===yn||Ae===me?n.NONE:n.BROWSER_DEFAULT_WEBGL;n.pixelStorei(n.UNPACK_FLIP_Y_WEBGL,M.flipY),n.pixelStorei(n.UNPACK_PREMULTIPLY_ALPHA_WEBGL,M.premultiplyAlpha),n.pixelStorei(n.UNPACK_ALIGNMENT,M.unpackAlignment),n.pixelStorei(n.UNPACK_COLORSPACE_CONVERSION_WEBGL,Ee);const Ye=M.isCompressedTexture||M.image[0].isCompressedTexture,ce=M.image[0]&&M.image[0].isDataTexture,ye=[];for(let ee=0;ee<6;ee++)!Ye&&!ce?ye[ee]=_(M.image[ee],!0,r.maxCubemapSize):ye[ee]=ce?M.image[ee].image:M.image[ee],ye[ee]=ke(M,ye[ee]);const Ue=ye[0],Ne=a.convert(M.format,M.colorSpace),be=a.convert(M.type),We=b(M.internalFormat,Ne,be,M.colorSpace),He=M.isVideoTexture!==!0,tt=Z.__version===void 0||J===!0,O=ne.dataReady;let fe=T(M,Ue);le(n.TEXTURE_CUBE_MAP,M);let $;if(Ye){He&&tt&&t.texStorage2D(n.TEXTURE_CUBE_MAP,fe,We,Ue.width,Ue.height);for(let ee=0;ee<6;ee++){$=ye[ee].mipmaps;for(let xe=0;xe<$.length;xe++){const _e=$[xe];M.format!==Yt?Ne!==null?He?O&&t.compressedTexSubImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+ee,xe,0,0,_e.width,_e.height,Ne,_e.data):t.compressedTexImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+ee,xe,We,_e.width,_e.height,0,_e.data):console.warn("THREE.WebGLRenderer: Attempt to load unsupported compressed texture format in .setTextureCube()"):He?O&&t.texSubImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+ee,xe,0,0,_e.width,_e.height,Ne,be,_e.data):t.texImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+ee,xe,We,_e.width,_e.height,0,Ne,be,_e.data)}}}else{if($=M.mipmaps,He&&tt){$.length>0&&fe++;const ee=we(ye[0]);t.texStorage2D(n.TEXTURE_CUBE_MAP,fe,We,ee.width,ee.height)}for(let ee=0;ee<6;ee++)if(ce){He?O&&t.texSubImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+ee,0,0,0,ye[ee].width,ye[ee].height,Ne,be,ye[ee].data):t.texImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+ee,0,We,ye[ee].width,ye[ee].height,0,Ne,be,ye[ee].data);for(let xe=0;xe<$.length;xe++){const Oe=$[xe].image[ee].image;He?O&&t.texSubImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+ee,xe+1,0,0,Oe.width,Oe.height,Ne,be,Oe.data):t.texImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+ee,xe+1,We,Oe.width,Oe.height,0,Ne,be,Oe.data)}}else{He?O&&t.texSubImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+ee,0,0,0,Ne,be,ye[ee]):t.texImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+ee,0,We,Ne,be,ye[ee]);for(let xe=0;xe<$.length;xe++){const _e=$[xe];He?O&&t.texSubImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+ee,xe+1,0,0,Ne,be,_e.image[ee]):t.texImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+ee,xe+1,We,Ne,be,_e.image[ee])}}}p(M)&&u(n.TEXTURE_CUBE_MAP),Z.__version=ne.version,M.onUpdate&&M.onUpdate(M)}R.__version=M.version}function de(R,M,j,J,ne,Z){const Ae=a.convert(j.format,j.colorSpace),me=a.convert(j.type),Ee=b(j.internalFormat,Ae,me,j.colorSpace),Ye=i.get(M),ce=i.get(j);if(ce.__renderTarget=M,!Ye.__hasExternalTextures){const ye=Math.max(1,M.width>>Z),Ue=Math.max(1,M.height>>Z);ne===n.TEXTURE_3D||ne===n.TEXTURE_2D_ARRAY?t.texImage3D(ne,Z,Ee,ye,Ue,M.depth,0,Ae,me,null):t.texImage2D(ne,Z,Ee,ye,Ue,0,Ae,me,null)}t.bindFramebuffer(n.FRAMEBUFFER,R),Ce(M)?o.framebufferTexture2DMultisampleEXT(n.FRAMEBUFFER,J,ne,ce.__webglTexture,0,Pe(M)):(ne===n.TEXTURE_2D||ne>=n.TEXTURE_CUBE_MAP_POSITIVE_X&&ne<=n.TEXTURE_CUBE_MAP_NEGATIVE_Z)&&n.framebufferTexture2D(n.FRAMEBUFFER,J,ne,ce.__webglTexture,Z),t.bindFramebuffer(n.FRAMEBUFFER,null)}function se(R,M,j){if(n.bindRenderbuffer(n.RENDERBUFFER,R),M.depthBuffer){const J=M.depthTexture,ne=J&&J.isDepthTexture?J.type:null,Z=S(M.stencilBuffer,ne),Ae=M.stencilBuffer?n.DEPTH_STENCIL_ATTACHMENT:n.DEPTH_ATTACHMENT,me=Pe(M);Ce(M)?o.renderbufferStorageMultisampleEXT(n.RENDERBUFFER,me,Z,M.width,M.height):j?n.renderbufferStorageMultisample(n.RENDERBUFFER,me,Z,M.width,M.height):n.renderbufferStorage(n.RENDERBUFFER,Z,M.width,M.height),n.framebufferRenderbuffer(n.FRAMEBUFFER,Ae,n.RENDERBUFFER,R)}else{const J=M.textures;for(let ne=0;ne<J.length;ne++){const Z=J[ne],Ae=a.convert(Z.format,Z.colorSpace),me=a.convert(Z.type),Ee=b(Z.internalFormat,Ae,me,Z.colorSpace),Ye=Pe(M);j&&Ce(M)===!1?n.renderbufferStorageMultisample(n.RENDERBUFFER,Ye,Ee,M.width,M.height):Ce(M)?o.renderbufferStorageMultisampleEXT(n.RENDERBUFFER,Ye,Ee,M.width,M.height):n.renderbufferStorage(n.RENDERBUFFER,Ee,M.width,M.height)}}n.bindRenderbuffer(n.RENDERBUFFER,null)}function Q(R,M){if(M&&M.isWebGLCubeRenderTarget)throw new Error("Depth Texture with cube render targets is not supported");if(t.bindFramebuffer(n.FRAMEBUFFER,R),!(M.depthTexture&&M.depthTexture.isDepthTexture))throw new Error("renderTarget.depthTexture must be an instance of THREE.DepthTexture");const J=i.get(M.depthTexture);J.__renderTarget=M,(!J.__webglTexture||M.depthTexture.image.width!==M.width||M.depthTexture.image.height!==M.height)&&(M.depthTexture.image.width=M.width,M.depthTexture.image.height=M.height,M.depthTexture.needsUpdate=!0),U(M.depthTexture,0);const ne=J.__webglTexture,Z=Pe(M);if(M.depthTexture.format===_i)Ce(M)?o.framebufferTexture2DMultisampleEXT(n.FRAMEBUFFER,n.DEPTH_ATTACHMENT,n.TEXTURE_2D,ne,0,Z):n.framebufferTexture2D(n.FRAMEBUFFER,n.DEPTH_ATTACHMENT,n.TEXTURE_2D,ne,0);else if(M.depthTexture.format===bi)Ce(M)?o.framebufferTexture2DMultisampleEXT(n.FRAMEBUFFER,n.DEPTH_STENCIL_ATTACHMENT,n.TEXTURE_2D,ne,0,Z):n.framebufferTexture2D(n.FRAMEBUFFER,n.DEPTH_STENCIL_ATTACHMENT,n.TEXTURE_2D,ne,0);else throw new Error("Unknown depthTexture format")}function ge(R){const M=i.get(R),j=R.isWebGLCubeRenderTarget===!0;if(M.__boundDepthTexture!==R.depthTexture){const J=R.depthTexture;if(M.__depthDisposeCallback&&M.__depthDisposeCallback(),J){const ne=()=>{delete M.__boundDepthTexture,delete M.__depthDisposeCallback,J.removeEventListener("dispose",ne)};J.addEventListener("dispose",ne),M.__depthDisposeCallback=ne}M.__boundDepthTexture=J}if(R.depthTexture&&!M.__autoAllocateDepthBuffer){if(j)throw new Error("target.depthTexture not supported in Cube render targets");Q(M.__webglFramebuffer,R)}else if(j){M.__webglDepthbuffer=[];for(let J=0;J<6;J++)if(t.bindFramebuffer(n.FRAMEBUFFER,M.__webglFramebuffer[J]),M.__webglDepthbuffer[J]===void 0)M.__webglDepthbuffer[J]=n.createRenderbuffer(),se(M.__webglDepthbuffer[J],R,!1);else{const ne=R.stencilBuffer?n.DEPTH_STENCIL_ATTACHMENT:n.DEPTH_ATTACHMENT,Z=M.__webglDepthbuffer[J];n.bindRenderbuffer(n.RENDERBUFFER,Z),n.framebufferRenderbuffer(n.FRAMEBUFFER,ne,n.RENDERBUFFER,Z)}}else if(t.bindFramebuffer(n.FRAMEBUFFER,M.__webglFramebuffer),M.__webglDepthbuffer===void 0)M.__webglDepthbuffer=n.createRenderbuffer(),se(M.__webglDepthbuffer,R,!1);else{const J=R.stencilBuffer?n.DEPTH_STENCIL_ATTACHMENT:n.DEPTH_ATTACHMENT,ne=M.__webglDepthbuffer;n.bindRenderbuffer(n.RENDERBUFFER,ne),n.framebufferRenderbuffer(n.FRAMEBUFFER,J,n.RENDERBUFFER,ne)}t.bindFramebuffer(n.FRAMEBUFFER,null)}function ue(R,M,j){const J=i.get(R);M!==void 0&&de(J.__webglFramebuffer,R,R.texture,n.COLOR_ATTACHMENT0,n.TEXTURE_2D,0),j!==void 0&&ge(R)}function K(R){const M=R.texture,j=i.get(R),J=i.get(M);R.addEventListener("dispose",A);const ne=R.textures,Z=R.isWebGLCubeRenderTarget===!0,Ae=ne.length>1;if(Ae||(J.__webglTexture===void 0&&(J.__webglTexture=n.createTexture()),J.__version=M.version,s.memory.textures++),Z){j.__webglFramebuffer=[];for(let me=0;me<6;me++)if(M.mipmaps&&M.mipmaps.length>0){j.__webglFramebuffer[me]=[];for(let Ee=0;Ee<M.mipmaps.length;Ee++)j.__webglFramebuffer[me][Ee]=n.createFramebuffer()}else j.__webglFramebuffer[me]=n.createFramebuffer()}else{if(M.mipmaps&&M.mipmaps.length>0){j.__webglFramebuffer=[];for(let me=0;me<M.mipmaps.length;me++)j.__webglFramebuffer[me]=n.createFramebuffer()}else j.__webglFramebuffer=n.createFramebuffer();if(Ae)for(let me=0,Ee=ne.length;me<Ee;me++){const Ye=i.get(ne[me]);Ye.__webglTexture===void 0&&(Ye.__webglTexture=n.createTexture(),s.memory.textures++)}if(R.samples>0&&Ce(R)===!1){j.__webglMultisampledFramebuffer=n.createFramebuffer(),j.__webglColorRenderbuffer=[],t.bindFramebuffer(n.FRAMEBUFFER,j.__webglMultisampledFramebuffer);for(let me=0;me<ne.length;me++){const Ee=ne[me];j.__webglColorRenderbuffer[me]=n.createRenderbuffer(),n.bindRenderbuffer(n.RENDERBUFFER,j.__webglColorRenderbuffer[me]);const Ye=a.convert(Ee.format,Ee.colorSpace),ce=a.convert(Ee.type),ye=b(Ee.internalFormat,Ye,ce,Ee.colorSpace,R.isXRRenderTarget===!0),Ue=Pe(R);n.renderbufferStorageMultisample(n.RENDERBUFFER,Ue,ye,R.width,R.height),n.framebufferRenderbuffer(n.FRAMEBUFFER,n.COLOR_ATTACHMENT0+me,n.RENDERBUFFER,j.__webglColorRenderbuffer[me])}n.bindRenderbuffer(n.RENDERBUFFER,null),R.depthBuffer&&(j.__webglDepthRenderbuffer=n.createRenderbuffer(),se(j.__webglDepthRenderbuffer,R,!0)),t.bindFramebuffer(n.FRAMEBUFFER,null)}}if(Z){t.bindTexture(n.TEXTURE_CUBE_MAP,J.__webglTexture),le(n.TEXTURE_CUBE_MAP,M);for(let me=0;me<6;me++)if(M.mipmaps&&M.mipmaps.length>0)for(let Ee=0;Ee<M.mipmaps.length;Ee++)de(j.__webglFramebuffer[me][Ee],R,M,n.COLOR_ATTACHMENT0,n.TEXTURE_CUBE_MAP_POSITIVE_X+me,Ee);else de(j.__webglFramebuffer[me],R,M,n.COLOR_ATTACHMENT0,n.TEXTURE_CUBE_MAP_POSITIVE_X+me,0);p(M)&&u(n.TEXTURE_CUBE_MAP),t.unbindTexture()}else if(Ae){for(let me=0,Ee=ne.length;me<Ee;me++){const Ye=ne[me],ce=i.get(Ye);t.bindTexture(n.TEXTURE_2D,ce.__webglTexture),le(n.TEXTURE_2D,Ye),de(j.__webglFramebuffer,R,Ye,n.COLOR_ATTACHMENT0+me,n.TEXTURE_2D,0),p(Ye)&&u(n.TEXTURE_2D)}t.unbindTexture()}else{let me=n.TEXTURE_2D;if((R.isWebGL3DRenderTarget||R.isWebGLArrayRenderTarget)&&(me=R.isWebGL3DRenderTarget?n.TEXTURE_3D:n.TEXTURE_2D_ARRAY),t.bindTexture(me,J.__webglTexture),le(me,M),M.mipmaps&&M.mipmaps.length>0)for(let Ee=0;Ee<M.mipmaps.length;Ee++)de(j.__webglFramebuffer[Ee],R,M,n.COLOR_ATTACHMENT0,me,Ee);else de(j.__webglFramebuffer,R,M,n.COLOR_ATTACHMENT0,me,0);p(M)&&u(me),t.unbindTexture()}R.depthBuffer&&ge(R)}function ie(R){const M=R.textures;for(let j=0,J=M.length;j<J;j++){const ne=M[j];if(p(ne)){const Z=w(R),Ae=i.get(ne).__webglTexture;t.bindTexture(Z,Ae),u(Z),t.unbindTexture()}}}const ae=[],L=[];function Ie(R){if(R.samples>0){if(Ce(R)===!1){const M=R.textures,j=R.width,J=R.height;let ne=n.COLOR_BUFFER_BIT;const Z=R.stencilBuffer?n.DEPTH_STENCIL_ATTACHMENT:n.DEPTH_ATTACHMENT,Ae=i.get(R),me=M.length>1;if(me)for(let Ee=0;Ee<M.length;Ee++)t.bindFramebuffer(n.FRAMEBUFFER,Ae.__webglMultisampledFramebuffer),n.framebufferRenderbuffer(n.FRAMEBUFFER,n.COLOR_ATTACHMENT0+Ee,n.RENDERBUFFER,null),t.bindFramebuffer(n.FRAMEBUFFER,Ae.__webglFramebuffer),n.framebufferTexture2D(n.DRAW_FRAMEBUFFER,n.COLOR_ATTACHMENT0+Ee,n.TEXTURE_2D,null,0);t.bindFramebuffer(n.READ_FRAMEBUFFER,Ae.__webglMultisampledFramebuffer),t.bindFramebuffer(n.DRAW_FRAMEBUFFER,Ae.__webglFramebuffer);for(let Ee=0;Ee<M.length;Ee++){if(R.resolveDepthBuffer&&(R.depthBuffer&&(ne|=n.DEPTH_BUFFER_BIT),R.stencilBuffer&&R.resolveStencilBuffer&&(ne|=n.STENCIL_BUFFER_BIT)),me){n.framebufferRenderbuffer(n.READ_FRAMEBUFFER,n.COLOR_ATTACHMENT0,n.RENDERBUFFER,Ae.__webglColorRenderbuffer[Ee]);const Ye=i.get(M[Ee]).__webglTexture;n.framebufferTexture2D(n.DRAW_FRAMEBUFFER,n.COLOR_ATTACHMENT0,n.TEXTURE_2D,Ye,0)}n.blitFramebuffer(0,0,j,J,0,0,j,J,ne,n.NEAREST),c===!0&&(ae.length=0,L.length=0,ae.push(n.COLOR_ATTACHMENT0+Ee),R.depthBuffer&&R.resolveDepthBuffer===!1&&(ae.push(Z),L.push(Z),n.invalidateFramebuffer(n.DRAW_FRAMEBUFFER,L)),n.invalidateFramebuffer(n.READ_FRAMEBUFFER,ae))}if(t.bindFramebuffer(n.READ_FRAMEBUFFER,null),t.bindFramebuffer(n.DRAW_FRAMEBUFFER,null),me)for(let Ee=0;Ee<M.length;Ee++){t.bindFramebuffer(n.FRAMEBUFFER,Ae.__webglMultisampledFramebuffer),n.framebufferRenderbuffer(n.FRAMEBUFFER,n.COLOR_ATTACHMENT0+Ee,n.RENDERBUFFER,Ae.__webglColorRenderbuffer[Ee]);const Ye=i.get(M[Ee]).__webglTexture;t.bindFramebuffer(n.FRAMEBUFFER,Ae.__webglFramebuffer),n.framebufferTexture2D(n.DRAW_FRAMEBUFFER,n.COLOR_ATTACHMENT0+Ee,n.TEXTURE_2D,Ye,0)}t.bindFramebuffer(n.DRAW_FRAMEBUFFER,Ae.__webglMultisampledFramebuffer)}else if(R.depthBuffer&&R.resolveDepthBuffer===!1&&c){const M=R.stencilBuffer?n.DEPTH_STENCIL_ATTACHMENT:n.DEPTH_ATTACHMENT;n.invalidateFramebuffer(n.DRAW_FRAMEBUFFER,[M])}}}function Pe(R){return Math.min(r.maxSamples,R.samples)}function Ce(R){const M=i.get(R);return R.samples>0&&e.has("WEBGL_multisampled_render_to_texture")===!0&&M.__useRenderToTexture!==!1}function Me(R){const M=s.render.frame;d.get(R)!==M&&(d.set(R,M),R.update())}function ke(R,M){const j=R.colorSpace,J=R.format,ne=R.type;return R.isCompressedTexture===!0||R.isVideoTexture===!0||j!==Ti&&j!==yn&&(Ke.getTransfer(j)===et?(J!==Yt||ne!==pn)&&console.warn("THREE.WebGLTextures: sRGB encoded textures have to use RGBAFormat and UnsignedByteType."):console.error("THREE.WebGLTextures: Unsupported texture color space:",j)),M}function we(R){return typeof HTMLImageElement<"u"&&R instanceof HTMLImageElement?(l.width=R.naturalWidth||R.width,l.height=R.naturalHeight||R.height):typeof VideoFrame<"u"&&R instanceof VideoFrame?(l.width=R.displayWidth,l.height=R.displayHeight):(l.width=R.width,l.height=R.height),l}this.allocateTextureUnit=N,this.resetTextureUnits=F,this.setTexture2D=U,this.setTexture2DArray=z,this.setTexture3D=H,this.setTextureCube=I,this.rebindTextures=ue,this.setupRenderTarget=K,this.updateRenderTargetMipmap=ie,this.updateMultisampleRenderTarget=Ie,this.setupDepthRenderbuffer=ge,this.setupFrameBufferTexture=de,this.useMultisampledRTT=Ce}function Jp(n,e){function t(i,r=yn){let a;const s=Ke.getTransfer(r);if(i===pn)return n.UNSIGNED_BYTE;if(i===As)return n.UNSIGNED_SHORT_4_4_4_4;if(i===ws)return n.UNSIGNED_SHORT_5_5_5_1;if(i===uc)return n.UNSIGNED_INT_5_9_9_9_REV;if(i===cc)return n.BYTE;if(i===lc)return n.SHORT;if(i===Oi)return n.UNSIGNED_SHORT;if(i===Ts)return n.INT;if(i===Yn)return n.UNSIGNED_INT;if(i===un)return n.FLOAT;if(i===Bi)return n.HALF_FLOAT;if(i===dc)return n.ALPHA;if(i===hc)return n.RGB;if(i===Yt)return n.RGBA;if(i===fc)return n.LUMINANCE;if(i===pc)return n.LUMINANCE_ALPHA;if(i===_i)return n.DEPTH_COMPONENT;if(i===bi)return n.DEPTH_STENCIL;if(i===mc)return n.RED;if(i===Rs)return n.RED_INTEGER;if(i===gc)return n.RG;if(i===Cs)return n.RG_INTEGER;if(i===Ps)return n.RGBA_INTEGER;if(i===Sr||i===Er||i===yr||i===br)if(s===et)if(a=e.get("WEBGL_compressed_texture_s3tc_srgb"),a!==null){if(i===Sr)return a.COMPRESSED_SRGB_S3TC_DXT1_EXT;if(i===Er)return a.COMPRESSED_SRGB_ALPHA_S3TC_DXT1_EXT;if(i===yr)return a.COMPRESSED_SRGB_ALPHA_S3TC_DXT3_EXT;if(i===br)return a.COMPRESSED_SRGB_ALPHA_S3TC_DXT5_EXT}else return null;else if(a=e.get("WEBGL_compressed_texture_s3tc"),a!==null){if(i===Sr)return a.COMPRESSED_RGB_S3TC_DXT1_EXT;if(i===Er)return a.COMPRESSED_RGBA_S3TC_DXT1_EXT;if(i===yr)return a.COMPRESSED_RGBA_S3TC_DXT3_EXT;if(i===br)return a.COMPRESSED_RGBA_S3TC_DXT5_EXT}else return null;if(i===Va||i===Ga||i===ja||i===Wa)if(a=e.get("WEBGL_compressed_texture_pvrtc"),a!==null){if(i===Va)return a.COMPRESSED_RGB_PVRTC_4BPPV1_IMG;if(i===Ga)return a.COMPRESSED_RGB_PVRTC_2BPPV1_IMG;if(i===ja)return a.COMPRESSED_RGBA_PVRTC_4BPPV1_IMG;if(i===Wa)return a.COMPRESSED_RGBA_PVRTC_2BPPV1_IMG}else return null;if(i===Xa||i===Ya||i===qa)if(a=e.get("WEBGL_compressed_texture_etc"),a!==null){if(i===Xa||i===Ya)return s===et?a.COMPRESSED_SRGB8_ETC2:a.COMPRESSED_RGB8_ETC2;if(i===qa)return s===et?a.COMPRESSED_SRGB8_ALPHA8_ETC2_EAC:a.COMPRESSED_RGBA8_ETC2_EAC}else return null;if(i===$a||i===Ka||i===Za||i===Ja||i===Qa||i===es||i===ts||i===ns||i===is||i===rs||i===as||i===ss||i===os||i===cs)if(a=e.get("WEBGL_compressed_texture_astc"),a!==null){if(i===$a)return s===et?a.COMPRESSED_SRGB8_ALPHA8_ASTC_4x4_KHR:a.COMPRESSED_RGBA_ASTC_4x4_KHR;if(i===Ka)return s===et?a.COMPRESSED_SRGB8_ALPHA8_ASTC_5x4_KHR:a.COMPRESSED_RGBA_ASTC_5x4_KHR;if(i===Za)return s===et?a.COMPRESSED_SRGB8_ALPHA8_ASTC_5x5_KHR:a.COMPRESSED_RGBA_ASTC_5x5_KHR;if(i===Ja)return s===et?a.COMPRESSED_SRGB8_ALPHA8_ASTC_6x5_KHR:a.COMPRESSED_RGBA_ASTC_6x5_KHR;if(i===Qa)return s===et?a.COMPRESSED_SRGB8_ALPHA8_ASTC_6x6_KHR:a.COMPRESSED_RGBA_ASTC_6x6_KHR;if(i===es)return s===et?a.COMPRESSED_SRGB8_ALPHA8_ASTC_8x5_KHR:a.COMPRESSED_RGBA_ASTC_8x5_KHR;if(i===ts)return s===et?a.COMPRESSED_SRGB8_ALPHA8_ASTC_8x6_KHR:a.COMPRESSED_RGBA_ASTC_8x6_KHR;if(i===ns)return s===et?a.COMPRESSED_SRGB8_ALPHA8_ASTC_8x8_KHR:a.COMPRESSED_RGBA_ASTC_8x8_KHR;if(i===is)return s===et?a.COMPRESSED_SRGB8_ALPHA8_ASTC_10x5_KHR:a.COMPRESSED_RGBA_ASTC_10x5_KHR;if(i===rs)return s===et?a.COMPRESSED_SRGB8_ALPHA8_ASTC_10x6_KHR:a.COMPRESSED_RGBA_ASTC_10x6_KHR;if(i===as)return s===et?a.COMPRESSED_SRGB8_ALPHA8_ASTC_10x8_KHR:a.COMPRESSED_RGBA_ASTC_10x8_KHR;if(i===ss)return s===et?a.COMPRESSED_SRGB8_ALPHA8_ASTC_10x10_KHR:a.COMPRESSED_RGBA_ASTC_10x10_KHR;if(i===os)return s===et?a.COMPRESSED_SRGB8_ALPHA8_ASTC_12x10_KHR:a.COMPRESSED_RGBA_ASTC_12x10_KHR;if(i===cs)return s===et?a.COMPRESSED_SRGB8_ALPHA8_ASTC_12x12_KHR:a.COMPRESSED_RGBA_ASTC_12x12_KHR}else return null;if(i===Tr||i===ls||i===us)if(a=e.get("EXT_texture_compression_bptc"),a!==null){if(i===Tr)return s===et?a.COMPRESSED_SRGB_ALPHA_BPTC_UNORM_EXT:a.COMPRESSED_RGBA_BPTC_UNORM_EXT;if(i===ls)return a.COMPRESSED_RGB_BPTC_SIGNED_FLOAT_EXT;if(i===us)return a.COMPRESSED_RGB_BPTC_UNSIGNED_FLOAT_EXT}else return null;if(i===_c||i===ds||i===hs||i===fs)if(a=e.get("EXT_texture_compression_rgtc"),a!==null){if(i===Tr)return a.COMPRESSED_RED_RGTC1_EXT;if(i===ds)return a.COMPRESSED_SIGNED_RED_RGTC1_EXT;if(i===hs)return a.COMPRESSED_RED_GREEN_RGTC2_EXT;if(i===fs)return a.COMPRESSED_SIGNED_RED_GREEN_RGTC2_EXT}else return null;return i===yi?n.UNSIGNED_INT_24_8:n[i]!==void 0?n[i]:null}return{convert:t}}const Qp=`
void main() {

	gl_Position = vec4( position, 1.0 );

}`,em=`
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

}`;class tm{constructor(){this.texture=null,this.mesh=null,this.depthNear=0,this.depthFar=0}init(e,t,i){if(this.texture===null){const r=new bt,a=e.properties.get(r);a.__webglTexture=t.texture,(t.depthNear!==i.depthNear||t.depthFar!==i.depthFar)&&(this.depthNear=t.depthNear,this.depthFar=t.depthFar),this.texture=r}}getMesh(e){if(this.texture!==null&&this.mesh===null){const t=e.cameras[0].viewport,i=new wn({vertexShader:Qp,fragmentShader:em,uniforms:{depthColor:{value:this.texture},depthWidth:{value:t.z},depthHeight:{value:t.w}}});this.mesh=new it(new Wi(20,20),i)}return this.mesh}reset(){this.texture=null,this.mesh=null}getDepthTexture(){return this.texture}}class nm extends wi{constructor(e,t){super();const i=this;let r=null,a=1,s=null,o="local-floor",c=1,l=null,d=null,h=null,f=null,m=null,g=null;const _=new tm,p=t.getContextAttributes();let u=null,w=null;const b=[],S=[],T=new Xe;let y=null;const A=new zt;A.viewport=new lt;const D=new zt;D.viewport=new lt;const x=[A,D],v=new Eu;let C=null,F=null;this.cameraAutoUpdate=!0,this.enabled=!1,this.isPresenting=!1,this.getController=function(Y){let te=b[Y];return te===void 0&&(te=new pa,b[Y]=te),te.getTargetRaySpace()},this.getControllerGrip=function(Y){let te=b[Y];return te===void 0&&(te=new pa,b[Y]=te),te.getGripSpace()},this.getHand=function(Y){let te=b[Y];return te===void 0&&(te=new pa,b[Y]=te),te.getHandSpace()};function N(Y){const te=S.indexOf(Y.inputSource);if(te===-1)return;const de=b[te];de!==void 0&&(de.update(Y.inputSource,Y.frame,l||s),de.dispatchEvent({type:Y.type,data:Y.inputSource}))}function P(){r.removeEventListener("select",N),r.removeEventListener("selectstart",N),r.removeEventListener("selectend",N),r.removeEventListener("squeeze",N),r.removeEventListener("squeezestart",N),r.removeEventListener("squeezeend",N),r.removeEventListener("end",P),r.removeEventListener("inputsourceschange",U);for(let Y=0;Y<b.length;Y++){const te=S[Y];te!==null&&(S[Y]=null,b[Y].disconnect(te))}C=null,F=null,_.reset(),e.setRenderTarget(u),m=null,f=null,h=null,r=null,w=null,Re.stop(),i.isPresenting=!1,e.setPixelRatio(y),e.setSize(T.width,T.height,!1),i.dispatchEvent({type:"sessionend"})}this.setFramebufferScaleFactor=function(Y){a=Y,i.isPresenting===!0&&console.warn("THREE.WebXRManager: Cannot change framebuffer scale while presenting.")},this.setReferenceSpaceType=function(Y){o=Y,i.isPresenting===!0&&console.warn("THREE.WebXRManager: Cannot change reference space type while presenting.")},this.getReferenceSpace=function(){return l||s},this.setReferenceSpace=function(Y){l=Y},this.getBaseLayer=function(){return f!==null?f:m},this.getBinding=function(){return h},this.getFrame=function(){return g},this.getSession=function(){return r},this.setSession=async function(Y){if(r=Y,r!==null){if(u=e.getRenderTarget(),r.addEventListener("select",N),r.addEventListener("selectstart",N),r.addEventListener("selectend",N),r.addEventListener("squeeze",N),r.addEventListener("squeezestart",N),r.addEventListener("squeezeend",N),r.addEventListener("end",P),r.addEventListener("inputsourceschange",U),p.xrCompatible!==!0&&await t.makeXRCompatible(),y=e.getPixelRatio(),e.getSize(T),typeof XRWebGLBinding<"u"&&"createProjectionLayer"in XRWebGLBinding.prototype){let de=null,se=null,Q=null;p.depth&&(Q=p.stencil?t.DEPTH24_STENCIL8:t.DEPTH_COMPONENT24,de=p.stencil?bi:_i,se=p.stencil?yi:Yn);const ge={colorFormat:t.RGBA8,depthFormat:Q,scaleFactor:a};h=new XRWebGLBinding(r,t),f=h.createProjectionLayer(ge),r.updateRenderState({layers:[f]}),e.setPixelRatio(1),e.setSize(f.textureWidth,f.textureHeight,!1),w=new qn(f.textureWidth,f.textureHeight,{format:Yt,type:pn,depthTexture:new Rc(f.textureWidth,f.textureHeight,se,void 0,void 0,void 0,void 0,void 0,void 0,de),stencilBuffer:p.stencil,colorSpace:e.outputColorSpace,samples:p.antialias?4:0,resolveDepthBuffer:f.ignoreDepthValues===!1,resolveStencilBuffer:f.ignoreDepthValues===!1})}else{const de={antialias:p.antialias,alpha:!0,depth:p.depth,stencil:p.stencil,framebufferScaleFactor:a};m=new XRWebGLLayer(r,t,de),r.updateRenderState({baseLayer:m}),e.setPixelRatio(1),e.setSize(m.framebufferWidth,m.framebufferHeight,!1),w=new qn(m.framebufferWidth,m.framebufferHeight,{format:Yt,type:pn,colorSpace:e.outputColorSpace,stencilBuffer:p.stencil,resolveDepthBuffer:m.ignoreDepthValues===!1,resolveStencilBuffer:m.ignoreDepthValues===!1})}w.isXRRenderTarget=!0,this.setFoveation(c),l=null,s=await r.requestReferenceSpace(o),Re.setContext(r),Re.start(),i.isPresenting=!0,i.dispatchEvent({type:"sessionstart"})}},this.getEnvironmentBlendMode=function(){if(r!==null)return r.environmentBlendMode},this.getDepthTexture=function(){return _.getDepthTexture()};function U(Y){for(let te=0;te<Y.removed.length;te++){const de=Y.removed[te],se=S.indexOf(de);se>=0&&(S[se]=null,b[se].disconnect(de))}for(let te=0;te<Y.added.length;te++){const de=Y.added[te];let se=S.indexOf(de);if(se===-1){for(let ge=0;ge<b.length;ge++)if(ge>=S.length){S.push(de),se=ge;break}else if(S[ge]===null){S[ge]=de,se=ge;break}if(se===-1)break}const Q=b[se];Q&&Q.connect(de)}}const z=new k,H=new k;function I(Y,te,de){z.setFromMatrixPosition(te.matrixWorld),H.setFromMatrixPosition(de.matrixWorld);const se=z.distanceTo(H),Q=te.projectionMatrix.elements,ge=de.projectionMatrix.elements,ue=Q[14]/(Q[10]-1),K=Q[14]/(Q[10]+1),ie=(Q[9]+1)/Q[5],ae=(Q[9]-1)/Q[5],L=(Q[8]-1)/Q[0],Ie=(ge[8]+1)/ge[0],Pe=ue*L,Ce=ue*Ie,Me=se/(-L+Ie),ke=Me*-L;if(te.matrixWorld.decompose(Y.position,Y.quaternion,Y.scale),Y.translateX(ke),Y.translateZ(Me),Y.matrixWorld.compose(Y.position,Y.quaternion,Y.scale),Y.matrixWorldInverse.copy(Y.matrixWorld).invert(),Q[10]===-1)Y.projectionMatrix.copy(te.projectionMatrix),Y.projectionMatrixInverse.copy(te.projectionMatrixInverse);else{const we=ue+Me,R=K+Me,M=Pe-ke,j=Ce+(se-ke),J=ie*K/R*we,ne=ae*K/R*we;Y.projectionMatrix.makePerspective(M,j,J,ne,we,R),Y.projectionMatrixInverse.copy(Y.projectionMatrix).invert()}}function G(Y,te){te===null?Y.matrixWorld.copy(Y.matrix):Y.matrixWorld.multiplyMatrices(te.matrixWorld,Y.matrix),Y.matrixWorldInverse.copy(Y.matrixWorld).invert()}this.updateCamera=function(Y){if(r===null)return;let te=Y.near,de=Y.far;_.texture!==null&&(_.depthNear>0&&(te=_.depthNear),_.depthFar>0&&(de=_.depthFar)),v.near=D.near=A.near=te,v.far=D.far=A.far=de,(C!==v.near||F!==v.far)&&(r.updateRenderState({depthNear:v.near,depthFar:v.far}),C=v.near,F=v.far),A.layers.mask=Y.layers.mask|2,D.layers.mask=Y.layers.mask|4,v.layers.mask=A.layers.mask|D.layers.mask;const se=Y.parent,Q=v.cameras;G(v,se);for(let ge=0;ge<Q.length;ge++)G(Q[ge],se);Q.length===2?I(v,A,D):v.projectionMatrix.copy(A.projectionMatrix),q(Y,v,se)};function q(Y,te,de){de===null?Y.matrix.copy(te.matrixWorld):(Y.matrix.copy(de.matrixWorld),Y.matrix.invert(),Y.matrix.multiply(te.matrixWorld)),Y.matrix.decompose(Y.position,Y.quaternion,Y.scale),Y.updateMatrixWorld(!0),Y.projectionMatrix.copy(te.projectionMatrix),Y.projectionMatrixInverse.copy(te.projectionMatrixInverse),Y.isPerspectiveCamera&&(Y.fov=ps*2*Math.atan(1/Y.projectionMatrix.elements[5]),Y.zoom=1)}this.getCamera=function(){return v},this.getFoveation=function(){if(!(f===null&&m===null))return c},this.setFoveation=function(Y){c=Y,f!==null&&(f.fixedFoveation=Y),m!==null&&m.fixedFoveation!==void 0&&(m.fixedFoveation=Y)},this.hasDepthSensing=function(){return _.texture!==null},this.getDepthSensingMesh=function(){return _.getMesh(v)};let oe=null;function le(Y,te){if(d=te.getViewerPose(l||s),g=te,d!==null){const de=d.views;m!==null&&(e.setRenderTargetFramebuffer(w,m.framebuffer),e.setRenderTarget(w));let se=!1;de.length!==v.cameras.length&&(v.cameras.length=0,se=!0);for(let ue=0;ue<de.length;ue++){const K=de[ue];let ie=null;if(m!==null)ie=m.getViewport(K);else{const L=h.getViewSubImage(f,K);ie=L.viewport,ue===0&&(e.setRenderTargetTextures(w,L.colorTexture,f.ignoreDepthValues?void 0:L.depthStencilTexture),e.setRenderTarget(w))}let ae=x[ue];ae===void 0&&(ae=new zt,ae.layers.enable(ue),ae.viewport=new lt,x[ue]=ae),ae.matrix.fromArray(K.transform.matrix),ae.matrix.decompose(ae.position,ae.quaternion,ae.scale),ae.projectionMatrix.fromArray(K.projectionMatrix),ae.projectionMatrixInverse.copy(ae.projectionMatrix).invert(),ae.viewport.set(ie.x,ie.y,ie.width,ie.height),ue===0&&(v.matrix.copy(ae.matrix),v.matrix.decompose(v.position,v.quaternion,v.scale)),se===!0&&v.cameras.push(ae)}const Q=r.enabledFeatures;if(Q&&Q.includes("depth-sensing")&&r.depthUsage=="gpu-optimized"&&h){const ue=h.getDepthInformation(de[0]);ue&&ue.isValid&&ue.texture&&_.init(e,ue,r.renderState)}}for(let de=0;de<b.length;de++){const se=S[de],Q=b[de];se!==null&&Q!==void 0&&Q.update(se,te,l||s)}oe&&oe(Y,te),te.detectedPlanes&&i.dispatchEvent({type:"planesdetected",data:te}),g=null}const Re=new Dc;Re.setAnimationLoop(le),this.setAnimationLoop=function(Y){oe=Y},this.dispose=function(){}}}const Nn=new Jt,im=new at;function rm(n,e){function t(p,u){p.matrixAutoUpdate===!0&&p.updateMatrix(),u.value.copy(p.matrix)}function i(p,u){u.color.getRGB(p.fogColor.value,Tc(n)),u.isFog?(p.fogNear.value=u.near,p.fogFar.value=u.far):u.isFogExp2&&(p.fogDensity.value=u.density)}function r(p,u,w,b,S){u.isMeshBasicMaterial||u.isMeshLambertMaterial?a(p,u):u.isMeshToonMaterial?(a(p,u),h(p,u)):u.isMeshPhongMaterial?(a(p,u),d(p,u)):u.isMeshStandardMaterial?(a(p,u),f(p,u),u.isMeshPhysicalMaterial&&m(p,u,S)):u.isMeshMatcapMaterial?(a(p,u),g(p,u)):u.isMeshDepthMaterial?a(p,u):u.isMeshDistanceMaterial?(a(p,u),_(p,u)):u.isMeshNormalMaterial?a(p,u):u.isLineBasicMaterial?(s(p,u),u.isLineDashedMaterial&&o(p,u)):u.isPointsMaterial?c(p,u,w,b):u.isSpriteMaterial?l(p,u):u.isShadowMaterial?(p.color.value.copy(u.color),p.opacity.value=u.opacity):u.isShaderMaterial&&(u.uniformsNeedUpdate=!1)}function a(p,u){p.opacity.value=u.opacity,u.color&&p.diffuse.value.copy(u.color),u.emissive&&p.emissive.value.copy(u.emissive).multiplyScalar(u.emissiveIntensity),u.map&&(p.map.value=u.map,t(u.map,p.mapTransform)),u.alphaMap&&(p.alphaMap.value=u.alphaMap,t(u.alphaMap,p.alphaMapTransform)),u.bumpMap&&(p.bumpMap.value=u.bumpMap,t(u.bumpMap,p.bumpMapTransform),p.bumpScale.value=u.bumpScale,u.side===Rt&&(p.bumpScale.value*=-1)),u.normalMap&&(p.normalMap.value=u.normalMap,t(u.normalMap,p.normalMapTransform),p.normalScale.value.copy(u.normalScale),u.side===Rt&&p.normalScale.value.negate()),u.displacementMap&&(p.displacementMap.value=u.displacementMap,t(u.displacementMap,p.displacementMapTransform),p.displacementScale.value=u.displacementScale,p.displacementBias.value=u.displacementBias),u.emissiveMap&&(p.emissiveMap.value=u.emissiveMap,t(u.emissiveMap,p.emissiveMapTransform)),u.specularMap&&(p.specularMap.value=u.specularMap,t(u.specularMap,p.specularMapTransform)),u.alphaTest>0&&(p.alphaTest.value=u.alphaTest);const w=e.get(u),b=w.envMap,S=w.envMapRotation;b&&(p.envMap.value=b,Nn.copy(S),Nn.x*=-1,Nn.y*=-1,Nn.z*=-1,b.isCubeTexture&&b.isRenderTargetTexture===!1&&(Nn.y*=-1,Nn.z*=-1),p.envMapRotation.value.setFromMatrix4(im.makeRotationFromEuler(Nn)),p.flipEnvMap.value=b.isCubeTexture&&b.isRenderTargetTexture===!1?-1:1,p.reflectivity.value=u.reflectivity,p.ior.value=u.ior,p.refractionRatio.value=u.refractionRatio),u.lightMap&&(p.lightMap.value=u.lightMap,p.lightMapIntensity.value=u.lightMapIntensity,t(u.lightMap,p.lightMapTransform)),u.aoMap&&(p.aoMap.value=u.aoMap,p.aoMapIntensity.value=u.aoMapIntensity,t(u.aoMap,p.aoMapTransform))}function s(p,u){p.diffuse.value.copy(u.color),p.opacity.value=u.opacity,u.map&&(p.map.value=u.map,t(u.map,p.mapTransform))}function o(p,u){p.dashSize.value=u.dashSize,p.totalSize.value=u.dashSize+u.gapSize,p.scale.value=u.scale}function c(p,u,w,b){p.diffuse.value.copy(u.color),p.opacity.value=u.opacity,p.size.value=u.size*w,p.scale.value=b*.5,u.map&&(p.map.value=u.map,t(u.map,p.uvTransform)),u.alphaMap&&(p.alphaMap.value=u.alphaMap,t(u.alphaMap,p.alphaMapTransform)),u.alphaTest>0&&(p.alphaTest.value=u.alphaTest)}function l(p,u){p.diffuse.value.copy(u.color),p.opacity.value=u.opacity,p.rotation.value=u.rotation,u.map&&(p.map.value=u.map,t(u.map,p.mapTransform)),u.alphaMap&&(p.alphaMap.value=u.alphaMap,t(u.alphaMap,p.alphaMapTransform)),u.alphaTest>0&&(p.alphaTest.value=u.alphaTest)}function d(p,u){p.specular.value.copy(u.specular),p.shininess.value=Math.max(u.shininess,1e-4)}function h(p,u){u.gradientMap&&(p.gradientMap.value=u.gradientMap)}function f(p,u){p.metalness.value=u.metalness,u.metalnessMap&&(p.metalnessMap.value=u.metalnessMap,t(u.metalnessMap,p.metalnessMapTransform)),p.roughness.value=u.roughness,u.roughnessMap&&(p.roughnessMap.value=u.roughnessMap,t(u.roughnessMap,p.roughnessMapTransform)),u.envMap&&(p.envMapIntensity.value=u.envMapIntensity)}function m(p,u,w){p.ior.value=u.ior,u.sheen>0&&(p.sheenColor.value.copy(u.sheenColor).multiplyScalar(u.sheen),p.sheenRoughness.value=u.sheenRoughness,u.sheenColorMap&&(p.sheenColorMap.value=u.sheenColorMap,t(u.sheenColorMap,p.sheenColorMapTransform)),u.sheenRoughnessMap&&(p.sheenRoughnessMap.value=u.sheenRoughnessMap,t(u.sheenRoughnessMap,p.sheenRoughnessMapTransform))),u.clearcoat>0&&(p.clearcoat.value=u.clearcoat,p.clearcoatRoughness.value=u.clearcoatRoughness,u.clearcoatMap&&(p.clearcoatMap.value=u.clearcoatMap,t(u.clearcoatMap,p.clearcoatMapTransform)),u.clearcoatRoughnessMap&&(p.clearcoatRoughnessMap.value=u.clearcoatRoughnessMap,t(u.clearcoatRoughnessMap,p.clearcoatRoughnessMapTransform)),u.clearcoatNormalMap&&(p.clearcoatNormalMap.value=u.clearcoatNormalMap,t(u.clearcoatNormalMap,p.clearcoatNormalMapTransform),p.clearcoatNormalScale.value.copy(u.clearcoatNormalScale),u.side===Rt&&p.clearcoatNormalScale.value.negate())),u.dispersion>0&&(p.dispersion.value=u.dispersion),u.iridescence>0&&(p.iridescence.value=u.iridescence,p.iridescenceIOR.value=u.iridescenceIOR,p.iridescenceThicknessMinimum.value=u.iridescenceThicknessRange[0],p.iridescenceThicknessMaximum.value=u.iridescenceThicknessRange[1],u.iridescenceMap&&(p.iridescenceMap.value=u.iridescenceMap,t(u.iridescenceMap,p.iridescenceMapTransform)),u.iridescenceThicknessMap&&(p.iridescenceThicknessMap.value=u.iridescenceThicknessMap,t(u.iridescenceThicknessMap,p.iridescenceThicknessMapTransform))),u.transmission>0&&(p.transmission.value=u.transmission,p.transmissionSamplerMap.value=w.texture,p.transmissionSamplerSize.value.set(w.width,w.height),u.transmissionMap&&(p.transmissionMap.value=u.transmissionMap,t(u.transmissionMap,p.transmissionMapTransform)),p.thickness.value=u.thickness,u.thicknessMap&&(p.thicknessMap.value=u.thicknessMap,t(u.thicknessMap,p.thicknessMapTransform)),p.attenuationDistance.value=u.attenuationDistance,p.attenuationColor.value.copy(u.attenuationColor)),u.anisotropy>0&&(p.anisotropyVector.value.set(u.anisotropy*Math.cos(u.anisotropyRotation),u.anisotropy*Math.sin(u.anisotropyRotation)),u.anisotropyMap&&(p.anisotropyMap.value=u.anisotropyMap,t(u.anisotropyMap,p.anisotropyMapTransform))),p.specularIntensity.value=u.specularIntensity,p.specularColor.value.copy(u.specularColor),u.specularColorMap&&(p.specularColorMap.value=u.specularColorMap,t(u.specularColorMap,p.specularColorMapTransform)),u.specularIntensityMap&&(p.specularIntensityMap.value=u.specularIntensityMap,t(u.specularIntensityMap,p.specularIntensityMapTransform))}function g(p,u){u.matcap&&(p.matcap.value=u.matcap)}function _(p,u){const w=e.get(u).light;p.referencePosition.value.setFromMatrixPosition(w.matrixWorld),p.nearDistance.value=w.shadow.camera.near,p.farDistance.value=w.shadow.camera.far}return{refreshFogUniforms:i,refreshMaterialUniforms:r}}function am(n,e,t,i){let r={},a={},s=[];const o=n.getParameter(n.MAX_UNIFORM_BUFFER_BINDINGS);function c(w,b){const S=b.program;i.uniformBlockBinding(w,S)}function l(w,b){let S=r[w.id];S===void 0&&(g(w),S=d(w),r[w.id]=S,w.addEventListener("dispose",p));const T=b.program;i.updateUBOMapping(w,T);const y=e.render.frame;a[w.id]!==y&&(f(w),a[w.id]=y)}function d(w){const b=h();w.__bindingPointIndex=b;const S=n.createBuffer(),T=w.__size,y=w.usage;return n.bindBuffer(n.UNIFORM_BUFFER,S),n.bufferData(n.UNIFORM_BUFFER,T,y),n.bindBuffer(n.UNIFORM_BUFFER,null),n.bindBufferBase(n.UNIFORM_BUFFER,b,S),S}function h(){for(let w=0;w<o;w++)if(s.indexOf(w)===-1)return s.push(w),w;return console.error("THREE.WebGLRenderer: Maximum number of simultaneously usable uniforms groups reached."),0}function f(w){const b=r[w.id],S=w.uniforms,T=w.__cache;n.bindBuffer(n.UNIFORM_BUFFER,b);for(let y=0,A=S.length;y<A;y++){const D=Array.isArray(S[y])?S[y]:[S[y]];for(let x=0,v=D.length;x<v;x++){const C=D[x];if(m(C,y,x,T)===!0){const F=C.__offset,N=Array.isArray(C.value)?C.value:[C.value];let P=0;for(let U=0;U<N.length;U++){const z=N[U],H=_(z);typeof z=="number"||typeof z=="boolean"?(C.__data[0]=z,n.bufferSubData(n.UNIFORM_BUFFER,F+P,C.__data)):z.isMatrix3?(C.__data[0]=z.elements[0],C.__data[1]=z.elements[1],C.__data[2]=z.elements[2],C.__data[3]=0,C.__data[4]=z.elements[3],C.__data[5]=z.elements[4],C.__data[6]=z.elements[5],C.__data[7]=0,C.__data[8]=z.elements[6],C.__data[9]=z.elements[7],C.__data[10]=z.elements[8],C.__data[11]=0):(z.toArray(C.__data,P),P+=H.storage/Float32Array.BYTES_PER_ELEMENT)}n.bufferSubData(n.UNIFORM_BUFFER,F,C.__data)}}}n.bindBuffer(n.UNIFORM_BUFFER,null)}function m(w,b,S,T){const y=w.value,A=b+"_"+S;if(T[A]===void 0)return typeof y=="number"||typeof y=="boolean"?T[A]=y:T[A]=y.clone(),!0;{const D=T[A];if(typeof y=="number"||typeof y=="boolean"){if(D!==y)return T[A]=y,!0}else if(D.equals(y)===!1)return D.copy(y),!0}return!1}function g(w){const b=w.uniforms;let S=0;const T=16;for(let A=0,D=b.length;A<D;A++){const x=Array.isArray(b[A])?b[A]:[b[A]];for(let v=0,C=x.length;v<C;v++){const F=x[v],N=Array.isArray(F.value)?F.value:[F.value];for(let P=0,U=N.length;P<U;P++){const z=N[P],H=_(z),I=S%T,G=I%H.boundary,q=I+G;S+=G,q!==0&&T-q<H.storage&&(S+=T-q),F.__data=new Float32Array(H.storage/Float32Array.BYTES_PER_ELEMENT),F.__offset=S,S+=H.storage}}}const y=S%T;return y>0&&(S+=T-y),w.__size=S,w.__cache={},this}function _(w){const b={boundary:0,storage:0};return typeof w=="number"||typeof w=="boolean"?(b.boundary=4,b.storage=4):w.isVector2?(b.boundary=8,b.storage=8):w.isVector3||w.isColor?(b.boundary=16,b.storage=12):w.isVector4?(b.boundary=16,b.storage=16):w.isMatrix3?(b.boundary=48,b.storage=48):w.isMatrix4?(b.boundary=64,b.storage=64):w.isTexture?console.warn("THREE.WebGLRenderer: Texture samplers can not be part of an uniforms group."):console.warn("THREE.WebGLRenderer: Unsupported uniform value type.",w),b}function p(w){const b=w.target;b.removeEventListener("dispose",p);const S=s.indexOf(b.__bindingPointIndex);s.splice(S,1),n.deleteBuffer(r[b.id]),delete r[b.id],delete a[b.id]}function u(){for(const w in r)n.deleteBuffer(r[w]);s=[],r={},a={}}return{bind:c,update:l,dispose:u}}class sm{constructor(e={}){const{canvas:t=Bl(),context:i=null,depth:r=!0,stencil:a=!1,alpha:s=!1,antialias:o=!1,premultipliedAlpha:c=!0,preserveDrawingBuffer:l=!1,powerPreference:d="default",failIfMajorPerformanceCaveat:h=!1,reverseDepthBuffer:f=!1}=e;this.isWebGLRenderer=!0;let m;if(i!==null){if(typeof WebGLRenderingContext<"u"&&i instanceof WebGLRenderingContext)throw new Error("THREE.WebGLRenderer: WebGL 1 is not supported since r163.");m=i.getContextAttributes().alpha}else m=s;const g=new Uint32Array(4),_=new Int32Array(4);let p=null,u=null;const w=[],b=[];this.domElement=t,this.debug={checkShaderErrors:!0,onShaderError:null},this.autoClear=!0,this.autoClearColor=!0,this.autoClearDepth=!0,this.autoClearStencil=!0,this.sortObjects=!0,this.clippingPlanes=[],this.localClippingEnabled=!1,this._outputColorSpace=Lt,this.toneMapping=Tn,this.toneMappingExposure=1;const S=this;let T=!1,y=0,A=0,D=null,x=-1,v=null;const C=new lt,F=new lt;let N=null;const P=new ve(0);let U=0,z=t.width,H=t.height,I=1,G=null,q=null;const oe=new lt(0,0,z,H),le=new lt(0,0,z,H);let Re=!1;const Y=new Us;let te=!1,de=!1;this.transmissionResolutionScale=1;const se=new at,Q=new at,ge=new k,ue=new lt,K={background:null,fog:null,environment:null,overrideMaterial:null,isScene:!0};let ie=!1;function ae(){return D===null?I:1}let L=i;function Ie(E,B){return t.getContext(E,B)}try{const E={alpha:!0,depth:r,stencil:a,antialias:o,premultipliedAlpha:c,preserveDrawingBuffer:l,powerPreference:d,failIfMajorPerformanceCaveat:h};if("setAttribute"in t&&t.setAttribute("data-engine",`three.js r${bs}`),t.addEventListener("webglcontextlost",ee,!1),t.addEventListener("webglcontextrestored",xe,!1),t.addEventListener("webglcontextcreationerror",_e,!1),L===null){const B="webgl2";if(L=Ie(B,E),L===null)throw Ie(B)?new Error("Error creating WebGL context with your selected attributes."):new Error("Error creating WebGL context.")}}catch(E){throw console.error("THREE.WebGLRenderer: "+E.message),E}let Pe,Ce,Me,ke,we,R,M,j,J,ne,Z,Ae,me,Ee,Ye,ce,ye,Ue,Ne,be,We,He,tt,O;function fe(){Pe=new gf(L),Pe.init(),He=new Jp(L,Pe),Ce=new lf(L,Pe,e,He),Me=new Kp(L,Pe),Ce.reverseDepthBuffer&&f&&Me.buffers.depth.setReversed(!0),ke=new xf(L),we=new zp,R=new Zp(L,Pe,Me,we,Ce,He,ke),M=new df(S),j=new mf(S),J=new bu(L),tt=new of(L,J),ne=new _f(L,J,ke,tt),Z=new Sf(L,ne,J,ke),Ne=new Mf(L,Ce,R),ce=new uf(we),Ae=new Fp(S,M,j,Pe,Ce,tt,ce),me=new rm(S,we),Ee=new Op,Ye=new Wp(Pe),Ue=new sf(S,M,j,Me,Z,m,c),ye=new qp(S,Z,Ce),O=new am(L,ke,Ce,Me),be=new cf(L,Pe,ke),We=new vf(L,Pe,ke),ke.programs=Ae.programs,S.capabilities=Ce,S.extensions=Pe,S.properties=we,S.renderLists=Ee,S.shadowMap=ye,S.state=Me,S.info=ke}fe();const $=new nm(S,L);this.xr=$,this.getContext=function(){return L},this.getContextAttributes=function(){return L.getContextAttributes()},this.forceContextLoss=function(){const E=Pe.get("WEBGL_lose_context");E&&E.loseContext()},this.forceContextRestore=function(){const E=Pe.get("WEBGL_lose_context");E&&E.restoreContext()},this.getPixelRatio=function(){return I},this.setPixelRatio=function(E){E!==void 0&&(I=E,this.setSize(z,H,!1))},this.getSize=function(E){return E.set(z,H)},this.setSize=function(E,B,W=!0){if($.isPresenting){console.warn("THREE.WebGLRenderer: Can't change size while VR device is presenting.");return}z=E,H=B,t.width=Math.floor(E*I),t.height=Math.floor(B*I),W===!0&&(t.style.width=E+"px",t.style.height=B+"px"),this.setViewport(0,0,E,B)},this.getDrawingBufferSize=function(E){return E.set(z*I,H*I).floor()},this.setDrawingBufferSize=function(E,B,W){z=E,H=B,I=W,t.width=Math.floor(E*W),t.height=Math.floor(B*W),this.setViewport(0,0,E,B)},this.getCurrentViewport=function(E){return E.copy(C)},this.getViewport=function(E){return E.copy(oe)},this.setViewport=function(E,B,W,X){E.isVector4?oe.set(E.x,E.y,E.z,E.w):oe.set(E,B,W,X),Me.viewport(C.copy(oe).multiplyScalar(I).round())},this.getScissor=function(E){return E.copy(le)},this.setScissor=function(E,B,W,X){E.isVector4?le.set(E.x,E.y,E.z,E.w):le.set(E,B,W,X),Me.scissor(F.copy(le).multiplyScalar(I).round())},this.getScissorTest=function(){return Re},this.setScissorTest=function(E){Me.setScissorTest(Re=E)},this.setOpaqueSort=function(E){G=E},this.setTransparentSort=function(E){q=E},this.getClearColor=function(E){return E.copy(Ue.getClearColor())},this.setClearColor=function(){Ue.setClearColor(...arguments)},this.getClearAlpha=function(){return Ue.getClearAlpha()},this.setClearAlpha=function(){Ue.setClearAlpha(...arguments)},this.clear=function(E=!0,B=!0,W=!0){let X=0;if(E){let V=!1;if(D!==null){const re=D.texture.format;V=re===Ps||re===Cs||re===Rs}if(V){const re=D.texture.type,pe=re===pn||re===Yn||re===Oi||re===yi||re===As||re===ws,Se=Ue.getClearColor(),Te=Ue.getClearAlpha(),Fe=Se.r,ze=Se.g,De=Se.b;pe?(g[0]=Fe,g[1]=ze,g[2]=De,g[3]=Te,L.clearBufferuiv(L.COLOR,0,g)):(_[0]=Fe,_[1]=ze,_[2]=De,_[3]=Te,L.clearBufferiv(L.COLOR,0,_))}else X|=L.COLOR_BUFFER_BIT}B&&(X|=L.DEPTH_BUFFER_BIT),W&&(X|=L.STENCIL_BUFFER_BIT,this.state.buffers.stencil.setMask(4294967295)),L.clear(X)},this.clearColor=function(){this.clear(!0,!1,!1)},this.clearDepth=function(){this.clear(!1,!0,!1)},this.clearStencil=function(){this.clear(!1,!1,!0)},this.dispose=function(){t.removeEventListener("webglcontextlost",ee,!1),t.removeEventListener("webglcontextrestored",xe,!1),t.removeEventListener("webglcontextcreationerror",_e,!1),Ue.dispose(),Ee.dispose(),Ye.dispose(),we.dispose(),M.dispose(),j.dispose(),Z.dispose(),tt.dispose(),O.dispose(),Ae.dispose(),$.dispose(),$.removeEventListener("sessionstart",Os),$.removeEventListener("sessionend",Bs),Rn.stop()};function ee(E){E.preventDefault(),console.log("THREE.WebGLRenderer: Context Lost."),T=!0}function xe(){console.log("THREE.WebGLRenderer: Context Restored."),T=!1;const E=ke.autoReset,B=ye.enabled,W=ye.autoUpdate,X=ye.needsUpdate,V=ye.type;fe(),ke.autoReset=E,ye.enabled=B,ye.autoUpdate=W,ye.needsUpdate=X,ye.type=V}function _e(E){console.error("THREE.WebGLRenderer: A WebGL context could not be created. Reason: ",E.statusMessage)}function Oe(E){const B=E.target;B.removeEventListener("dispose",Oe),ot(B)}function ot(E){vt(E),we.remove(E)}function vt(E){const B=we.get(E).programs;B!==void 0&&(B.forEach(function(W){Ae.releaseProgram(W)}),E.isShaderMaterial&&Ae.releaseShaderCache(E))}this.renderBufferDirect=function(E,B,W,X,V,re){B===null&&(B=K);const pe=V.isMesh&&V.matrixWorld.determinant()<0,Se=kc(E,B,W,X,V);Me.setMaterial(X,pe);let Te=W.index,Fe=1;if(X.wireframe===!0){if(Te=ne.getWireframeAttribute(W),Te===void 0)return;Fe=2}const ze=W.drawRange,De=W.attributes.position;let qe=ze.start*Fe,Ze=(ze.start+ze.count)*Fe;re!==null&&(qe=Math.max(qe,re.start*Fe),Ze=Math.min(Ze,(re.start+re.count)*Fe)),Te!==null?(qe=Math.max(qe,0),Ze=Math.min(Ze,Te.count)):De!=null&&(qe=Math.max(qe,0),Ze=Math.min(Ze,De.count));const ut=Ze-qe;if(ut<0||ut===1/0)return;tt.setup(V,X,Se,W,Te);let ct,$e=be;if(Te!==null&&(ct=J.get(Te),$e=We,$e.setIndex(ct)),V.isMesh)X.wireframe===!0?(Me.setLineWidth(X.wireframeLinewidth*ae()),$e.setMode(L.LINES)):$e.setMode(L.TRIANGLES);else if(V.isLine){let Le=X.linewidth;Le===void 0&&(Le=1),Me.setLineWidth(Le*ae()),V.isLineSegments?$e.setMode(L.LINES):V.isLineLoop?$e.setMode(L.LINE_LOOP):$e.setMode(L.LINE_STRIP)}else V.isPoints?$e.setMode(L.POINTS):V.isSprite&&$e.setMode(L.TRIANGLES);if(V.isBatchedMesh)if(V._multiDrawInstances!==null)Fn("THREE.WebGLRenderer: renderMultiDrawInstances has been deprecated and will be removed in r184. Append to renderMultiDraw arguments and use indirection."),$e.renderMultiDrawInstances(V._multiDrawStarts,V._multiDrawCounts,V._multiDrawCount,V._multiDrawInstances);else if(Pe.get("WEBGL_multi_draw"))$e.renderMultiDraw(V._multiDrawStarts,V._multiDrawCounts,V._multiDrawCount);else{const Le=V._multiDrawStarts,gt=V._multiDrawCounts,Je=V._multiDrawCount,Vt=Te?J.get(Te).bytesPerElement:1,Kn=we.get(X).currentProgram.getUniforms();for(let Ct=0;Ct<Je;Ct++)Kn.setValue(L,"_gl_DrawID",Ct),$e.render(Le[Ct]/Vt,gt[Ct])}else if(V.isInstancedMesh)$e.renderInstances(qe,ut,V.count);else if(W.isInstancedBufferGeometry){const Le=W._maxInstanceCount!==void 0?W._maxInstanceCount:1/0,gt=Math.min(W.instanceCount,Le);$e.renderInstances(qe,ut,gt)}else $e.render(qe,ut)};function Qe(E,B,W){E.transparent===!0&&E.side===kt&&E.forceSinglePass===!1?(E.side=Rt,E.needsUpdate=!0,Yi(E,B,W),E.side=An,E.needsUpdate=!0,Yi(E,B,W),E.side=kt):Yi(E,B,W)}this.compile=function(E,B,W=null){W===null&&(W=E),u=Ye.get(W),u.init(B),b.push(u),W.traverseVisible(function(V){V.isLight&&V.layers.test(B.layers)&&(u.pushLight(V),V.castShadow&&u.pushShadow(V))}),E!==W&&E.traverseVisible(function(V){V.isLight&&V.layers.test(B.layers)&&(u.pushLight(V),V.castShadow&&u.pushShadow(V))}),u.setupLights();const X=new Set;return E.traverse(function(V){if(!(V.isMesh||V.isPoints||V.isLine||V.isSprite))return;const re=V.material;if(re)if(Array.isArray(re))for(let pe=0;pe<re.length;pe++){const Se=re[pe];Qe(Se,W,V),X.add(Se)}else Qe(re,W,V),X.add(re)}),u=b.pop(),X},this.compileAsync=function(E,B,W=null){const X=this.compile(E,B,W);return new Promise(V=>{function re(){if(X.forEach(function(pe){we.get(pe).currentProgram.isReady()&&X.delete(pe)}),X.size===0){V(E);return}setTimeout(re,10)}Pe.get("KHR_parallel_shader_compile")!==null?re():setTimeout(re,10)})};let Ht=null;function Qt(E){Ht&&Ht(E)}function Os(){Rn.stop()}function Bs(){Rn.start()}const Rn=new Dc;Rn.setAnimationLoop(Qt),typeof self<"u"&&Rn.setContext(self),this.setAnimationLoop=function(E){Ht=E,$.setAnimationLoop(E),E===null?Rn.stop():Rn.start()},$.addEventListener("sessionstart",Os),$.addEventListener("sessionend",Bs),this.render=function(E,B){if(B!==void 0&&B.isCamera!==!0){console.error("THREE.WebGLRenderer.render: camera is not an instance of THREE.Camera.");return}if(T===!0)return;if(E.matrixWorldAutoUpdate===!0&&E.updateMatrixWorld(),B.parent===null&&B.matrixWorldAutoUpdate===!0&&B.updateMatrixWorld(),$.enabled===!0&&$.isPresenting===!0&&($.cameraAutoUpdate===!0&&$.updateCamera(B),B=$.getCamera()),E.isScene===!0&&E.onBeforeRender(S,E,B,D),u=Ye.get(E,b.length),u.init(B),b.push(u),Q.multiplyMatrices(B.projectionMatrix,B.matrixWorldInverse),Y.setFromProjectionMatrix(Q),de=this.localClippingEnabled,te=ce.init(this.clippingPlanes,de),p=Ee.get(E,w.length),p.init(),w.push(p),$.enabled===!0&&$.isPresenting===!0){const re=S.xr.getDepthSensingMesh();re!==null&&Gr(re,B,-1/0,S.sortObjects)}Gr(E,B,0,S.sortObjects),p.finish(),S.sortObjects===!0&&p.sort(G,q),ie=$.enabled===!1||$.isPresenting===!1||$.hasDepthSensing()===!1,ie&&Ue.addToRenderList(p,E),this.info.render.frame++,te===!0&&ce.beginShadows();const W=u.state.shadowsArray;ye.render(W,E,B),te===!0&&ce.endShadows(),this.info.autoReset===!0&&this.info.reset();const X=p.opaque,V=p.transmissive;if(u.setupLights(),B.isArrayCamera){const re=B.cameras;if(V.length>0)for(let pe=0,Se=re.length;pe<Se;pe++){const Te=re[pe];Vs(X,V,E,Te)}ie&&Ue.render(E);for(let pe=0,Se=re.length;pe<Se;pe++){const Te=re[pe];Hs(p,E,Te,Te.viewport)}}else V.length>0&&Vs(X,V,E,B),ie&&Ue.render(E),Hs(p,E,B);D!==null&&A===0&&(R.updateMultisampleRenderTarget(D),R.updateRenderTargetMipmap(D)),E.isScene===!0&&E.onAfterRender(S,E,B),tt.resetDefaultState(),x=-1,v=null,b.pop(),b.length>0?(u=b[b.length-1],te===!0&&ce.setGlobalState(S.clippingPlanes,u.state.camera)):u=null,w.pop(),w.length>0?p=w[w.length-1]:p=null};function Gr(E,B,W,X){if(E.visible===!1)return;if(E.layers.test(B.layers)){if(E.isGroup)W=E.renderOrder;else if(E.isLOD)E.autoUpdate===!0&&E.update(B);else if(E.isLight)u.pushLight(E),E.castShadow&&u.pushShadow(E);else if(E.isSprite){if(!E.frustumCulled||Y.intersectsSprite(E)){X&&ue.setFromMatrixPosition(E.matrixWorld).applyMatrix4(Q);const pe=Z.update(E),Se=E.material;Se.visible&&p.push(E,pe,Se,W,ue.z,null)}}else if((E.isMesh||E.isLine||E.isPoints)&&(!E.frustumCulled||Y.intersectsObject(E))){const pe=Z.update(E),Se=E.material;if(X&&(E.boundingSphere!==void 0?(E.boundingSphere===null&&E.computeBoundingSphere(),ue.copy(E.boundingSphere.center)):(pe.boundingSphere===null&&pe.computeBoundingSphere(),ue.copy(pe.boundingSphere.center)),ue.applyMatrix4(E.matrixWorld).applyMatrix4(Q)),Array.isArray(Se)){const Te=pe.groups;for(let Fe=0,ze=Te.length;Fe<ze;Fe++){const De=Te[Fe],qe=Se[De.materialIndex];qe&&qe.visible&&p.push(E,pe,qe,W,ue.z,De)}}else Se.visible&&p.push(E,pe,Se,W,ue.z,null)}}const re=E.children;for(let pe=0,Se=re.length;pe<Se;pe++)Gr(re[pe],B,W,X)}function Hs(E,B,W,X){const V=E.opaque,re=E.transmissive,pe=E.transparent;u.setupLightsView(W),te===!0&&ce.setGlobalState(S.clippingPlanes,W),X&&Me.viewport(C.copy(X)),V.length>0&&Xi(V,B,W),re.length>0&&Xi(re,B,W),pe.length>0&&Xi(pe,B,W),Me.buffers.depth.setTest(!0),Me.buffers.depth.setMask(!0),Me.buffers.color.setMask(!0),Me.setPolygonOffset(!1)}function Vs(E,B,W,X){if((W.isScene===!0?W.overrideMaterial:null)!==null)return;u.state.transmissionRenderTarget[X.id]===void 0&&(u.state.transmissionRenderTarget[X.id]=new qn(1,1,{generateMipmaps:!0,type:Pe.has("EXT_color_buffer_half_float")||Pe.has("EXT_color_buffer_float")?Bi:pn,minFilter:jn,samples:4,stencilBuffer:a,resolveDepthBuffer:!1,resolveStencilBuffer:!1,colorSpace:Ke.workingColorSpace}));const re=u.state.transmissionRenderTarget[X.id],pe=X.viewport||C;re.setSize(pe.z*S.transmissionResolutionScale,pe.w*S.transmissionResolutionScale);const Se=S.getRenderTarget();S.setRenderTarget(re),S.getClearColor(P),U=S.getClearAlpha(),U<1&&S.setClearColor(16777215,.5),S.clear(),ie&&Ue.render(W);const Te=S.toneMapping;S.toneMapping=Tn;const Fe=X.viewport;if(X.viewport!==void 0&&(X.viewport=void 0),u.setupLightsView(X),te===!0&&ce.setGlobalState(S.clippingPlanes,X),Xi(E,W,X),R.updateMultisampleRenderTarget(re),R.updateRenderTargetMipmap(re),Pe.has("WEBGL_multisampled_render_to_texture")===!1){let ze=!1;for(let De=0,qe=B.length;De<qe;De++){const Ze=B[De],ut=Ze.object,ct=Ze.geometry,$e=Ze.material,Le=Ze.group;if($e.side===kt&&ut.layers.test(X.layers)){const gt=$e.side;$e.side=Rt,$e.needsUpdate=!0,Gs(ut,W,X,ct,$e,Le),$e.side=gt,$e.needsUpdate=!0,ze=!0}}ze===!0&&(R.updateMultisampleRenderTarget(re),R.updateRenderTargetMipmap(re))}S.setRenderTarget(Se),S.setClearColor(P,U),Fe!==void 0&&(X.viewport=Fe),S.toneMapping=Te}function Xi(E,B,W){const X=B.isScene===!0?B.overrideMaterial:null;for(let V=0,re=E.length;V<re;V++){const pe=E[V],Se=pe.object,Te=pe.geometry,Fe=X===null?pe.material:X,ze=pe.group;Se.layers.test(W.layers)&&Gs(Se,B,W,Te,Fe,ze)}}function Gs(E,B,W,X,V,re){E.onBeforeRender(S,B,W,X,V,re),E.modelViewMatrix.multiplyMatrices(W.matrixWorldInverse,E.matrixWorld),E.normalMatrix.getNormalMatrix(E.modelViewMatrix),V.onBeforeRender(S,B,W,X,E,re),V.transparent===!0&&V.side===kt&&V.forceSinglePass===!1?(V.side=Rt,V.needsUpdate=!0,S.renderBufferDirect(W,B,X,V,E,re),V.side=An,V.needsUpdate=!0,S.renderBufferDirect(W,B,X,V,E,re),V.side=kt):S.renderBufferDirect(W,B,X,V,E,re),E.onAfterRender(S,B,W,X,V,re)}function Yi(E,B,W){B.isScene!==!0&&(B=K);const X=we.get(E),V=u.state.lights,re=u.state.shadowsArray,pe=V.state.version,Se=Ae.getParameters(E,V.state,re,B,W),Te=Ae.getProgramCacheKey(Se);let Fe=X.programs;X.environment=E.isMeshStandardMaterial?B.environment:null,X.fog=B.fog,X.envMap=(E.isMeshStandardMaterial?j:M).get(E.envMap||X.environment),X.envMapRotation=X.environment!==null&&E.envMap===null?B.environmentRotation:E.envMapRotation,Fe===void 0&&(E.addEventListener("dispose",Oe),Fe=new Map,X.programs=Fe);let ze=Fe.get(Te);if(ze!==void 0){if(X.currentProgram===ze&&X.lightsStateVersion===pe)return Ws(E,Se),ze}else Se.uniforms=Ae.getUniforms(E),E.onBeforeCompile(Se,S),ze=Ae.acquireProgram(Se,Te),Fe.set(Te,ze),X.uniforms=Se.uniforms;const De=X.uniforms;return(!E.isShaderMaterial&&!E.isRawShaderMaterial||E.clipping===!0)&&(De.clippingPlanes=ce.uniform),Ws(E,Se),X.needsLights=Bc(E),X.lightsStateVersion=pe,X.needsLights&&(De.ambientLightColor.value=V.state.ambient,De.lightProbe.value=V.state.probe,De.directionalLights.value=V.state.directional,De.directionalLightShadows.value=V.state.directionalShadow,De.spotLights.value=V.state.spot,De.spotLightShadows.value=V.state.spotShadow,De.rectAreaLights.value=V.state.rectArea,De.ltc_1.value=V.state.rectAreaLTC1,De.ltc_2.value=V.state.rectAreaLTC2,De.pointLights.value=V.state.point,De.pointLightShadows.value=V.state.pointShadow,De.hemisphereLights.value=V.state.hemi,De.directionalShadowMap.value=V.state.directionalShadowMap,De.directionalShadowMatrix.value=V.state.directionalShadowMatrix,De.spotShadowMap.value=V.state.spotShadowMap,De.spotLightMatrix.value=V.state.spotLightMatrix,De.spotLightMap.value=V.state.spotLightMap,De.pointShadowMap.value=V.state.pointShadowMap,De.pointShadowMatrix.value=V.state.pointShadowMatrix),X.currentProgram=ze,X.uniformsList=null,ze}function js(E){if(E.uniformsList===null){const B=E.currentProgram.getUniforms();E.uniformsList=Rr.seqWithValue(B.seq,E.uniforms)}return E.uniformsList}function Ws(E,B){const W=we.get(E);W.outputColorSpace=B.outputColorSpace,W.batching=B.batching,W.batchingColor=B.batchingColor,W.instancing=B.instancing,W.instancingColor=B.instancingColor,W.instancingMorph=B.instancingMorph,W.skinning=B.skinning,W.morphTargets=B.morphTargets,W.morphNormals=B.morphNormals,W.morphColors=B.morphColors,W.morphTargetsCount=B.morphTargetsCount,W.numClippingPlanes=B.numClippingPlanes,W.numIntersection=B.numClipIntersection,W.vertexAlphas=B.vertexAlphas,W.vertexTangents=B.vertexTangents,W.toneMapping=B.toneMapping}function kc(E,B,W,X,V){B.isScene!==!0&&(B=K),R.resetTextureUnits();const re=B.fog,pe=X.isMeshStandardMaterial?B.environment:null,Se=D===null?S.outputColorSpace:D.isXRRenderTarget===!0?D.texture.colorSpace:Ti,Te=(X.isMeshStandardMaterial?j:M).get(X.envMap||pe),Fe=X.vertexColors===!0&&!!W.attributes.color&&W.attributes.color.itemSize===4,ze=!!W.attributes.tangent&&(!!X.normalMap||X.anisotropy>0),De=!!W.morphAttributes.position,qe=!!W.morphAttributes.normal,Ze=!!W.morphAttributes.color;let ut=Tn;X.toneMapped&&(D===null||D.isXRRenderTarget===!0)&&(ut=S.toneMapping);const ct=W.morphAttributes.position||W.morphAttributes.normal||W.morphAttributes.color,$e=ct!==void 0?ct.length:0,Le=we.get(X),gt=u.state.lights;if(te===!0&&(de===!0||E!==v)){const St=E===v&&X.id===x;ce.setState(X,E,St)}let Je=!1;X.version===Le.__version?(Le.needsLights&&Le.lightsStateVersion!==gt.state.version||Le.outputColorSpace!==Se||V.isBatchedMesh&&Le.batching===!1||!V.isBatchedMesh&&Le.batching===!0||V.isBatchedMesh&&Le.batchingColor===!0&&V.colorTexture===null||V.isBatchedMesh&&Le.batchingColor===!1&&V.colorTexture!==null||V.isInstancedMesh&&Le.instancing===!1||!V.isInstancedMesh&&Le.instancing===!0||V.isSkinnedMesh&&Le.skinning===!1||!V.isSkinnedMesh&&Le.skinning===!0||V.isInstancedMesh&&Le.instancingColor===!0&&V.instanceColor===null||V.isInstancedMesh&&Le.instancingColor===!1&&V.instanceColor!==null||V.isInstancedMesh&&Le.instancingMorph===!0&&V.morphTexture===null||V.isInstancedMesh&&Le.instancingMorph===!1&&V.morphTexture!==null||Le.envMap!==Te||X.fog===!0&&Le.fog!==re||Le.numClippingPlanes!==void 0&&(Le.numClippingPlanes!==ce.numPlanes||Le.numIntersection!==ce.numIntersection)||Le.vertexAlphas!==Fe||Le.vertexTangents!==ze||Le.morphTargets!==De||Le.morphNormals!==qe||Le.morphColors!==Ze||Le.toneMapping!==ut||Le.morphTargetsCount!==$e)&&(Je=!0):(Je=!0,Le.__version=X.version);let Vt=Le.currentProgram;Je===!0&&(Vt=Yi(X,B,V));let Kn=!1,Ct=!1,Pi=!1;const rt=Vt.getUniforms(),Ut=Le.uniforms;if(Me.useProgram(Vt.program)&&(Kn=!0,Ct=!0,Pi=!0),X.id!==x&&(x=X.id,Ct=!0),Kn||v!==E){Me.buffers.depth.getReversed()?(se.copy(E.projectionMatrix),Vl(se),Gl(se),rt.setValue(L,"projectionMatrix",se)):rt.setValue(L,"projectionMatrix",E.projectionMatrix),rt.setValue(L,"viewMatrix",E.matrixWorldInverse);const Tt=rt.map.cameraPosition;Tt!==void 0&&Tt.setValue(L,ge.setFromMatrixPosition(E.matrixWorld)),Ce.logarithmicDepthBuffer&&rt.setValue(L,"logDepthBufFC",2/(Math.log(E.far+1)/Math.LN2)),(X.isMeshPhongMaterial||X.isMeshToonMaterial||X.isMeshLambertMaterial||X.isMeshBasicMaterial||X.isMeshStandardMaterial||X.isShaderMaterial)&&rt.setValue(L,"isOrthographic",E.isOrthographicCamera===!0),v!==E&&(v=E,Ct=!0,Pi=!0)}if(V.isSkinnedMesh){rt.setOptional(L,V,"bindMatrix"),rt.setOptional(L,V,"bindMatrixInverse");const St=V.skeleton;St&&(St.boneTexture===null&&St.computeBoneTexture(),rt.setValue(L,"boneTexture",St.boneTexture,R))}V.isBatchedMesh&&(rt.setOptional(L,V,"batchingTexture"),rt.setValue(L,"batchingTexture",V._matricesTexture,R),rt.setOptional(L,V,"batchingIdTexture"),rt.setValue(L,"batchingIdTexture",V._indirectTexture,R),rt.setOptional(L,V,"batchingColorTexture"),V._colorsTexture!==null&&rt.setValue(L,"batchingColorTexture",V._colorsTexture,R));const Nt=W.morphAttributes;if((Nt.position!==void 0||Nt.normal!==void 0||Nt.color!==void 0)&&Ne.update(V,W,Vt),(Ct||Le.receiveShadow!==V.receiveShadow)&&(Le.receiveShadow=V.receiveShadow,rt.setValue(L,"receiveShadow",V.receiveShadow)),X.isMeshGouraudMaterial&&X.envMap!==null&&(Ut.envMap.value=Te,Ut.flipEnvMap.value=Te.isCubeTexture&&Te.isRenderTargetTexture===!1?-1:1),X.isMeshStandardMaterial&&X.envMap===null&&B.environment!==null&&(Ut.envMapIntensity.value=B.environmentIntensity),Ct&&(rt.setValue(L,"toneMappingExposure",S.toneMappingExposure),Le.needsLights&&Oc(Ut,Pi),re&&X.fog===!0&&me.refreshFogUniforms(Ut,re),me.refreshMaterialUniforms(Ut,X,I,H,u.state.transmissionRenderTarget[E.id]),Rr.upload(L,js(Le),Ut,R)),X.isShaderMaterial&&X.uniformsNeedUpdate===!0&&(Rr.upload(L,js(Le),Ut,R),X.uniformsNeedUpdate=!1),X.isSpriteMaterial&&rt.setValue(L,"center",V.center),rt.setValue(L,"modelViewMatrix",V.modelViewMatrix),rt.setValue(L,"normalMatrix",V.normalMatrix),rt.setValue(L,"modelMatrix",V.matrixWorld),X.isShaderMaterial||X.isRawShaderMaterial){const St=X.uniformsGroups;for(let Tt=0,jr=St.length;Tt<jr;Tt++){const Cn=St[Tt];O.update(Cn,Vt),O.bind(Cn,Vt)}}return Vt}function Oc(E,B){E.ambientLightColor.needsUpdate=B,E.lightProbe.needsUpdate=B,E.directionalLights.needsUpdate=B,E.directionalLightShadows.needsUpdate=B,E.pointLights.needsUpdate=B,E.pointLightShadows.needsUpdate=B,E.spotLights.needsUpdate=B,E.spotLightShadows.needsUpdate=B,E.rectAreaLights.needsUpdate=B,E.hemisphereLights.needsUpdate=B}function Bc(E){return E.isMeshLambertMaterial||E.isMeshToonMaterial||E.isMeshPhongMaterial||E.isMeshStandardMaterial||E.isShadowMaterial||E.isShaderMaterial&&E.lights===!0}this.getActiveCubeFace=function(){return y},this.getActiveMipmapLevel=function(){return A},this.getRenderTarget=function(){return D},this.setRenderTargetTextures=function(E,B,W){we.get(E.texture).__webglTexture=B,we.get(E.depthTexture).__webglTexture=W;const X=we.get(E);X.__hasExternalTextures=!0,X.__autoAllocateDepthBuffer=W===void 0,X.__autoAllocateDepthBuffer||Pe.has("WEBGL_multisampled_render_to_texture")===!0&&(console.warn("THREE.WebGLRenderer: Render-to-texture extension was disabled because an external texture was provided"),X.__useRenderToTexture=!1)},this.setRenderTargetFramebuffer=function(E,B){const W=we.get(E);W.__webglFramebuffer=B,W.__useDefaultFramebuffer=B===void 0};const Hc=L.createFramebuffer();this.setRenderTarget=function(E,B=0,W=0){D=E,y=B,A=W;let X=!0,V=null,re=!1,pe=!1;if(E){const Te=we.get(E);if(Te.__useDefaultFramebuffer!==void 0)Me.bindFramebuffer(L.FRAMEBUFFER,null),X=!1;else if(Te.__webglFramebuffer===void 0)R.setupRenderTarget(E);else if(Te.__hasExternalTextures)R.rebindTextures(E,we.get(E.texture).__webglTexture,we.get(E.depthTexture).__webglTexture);else if(E.depthBuffer){const De=E.depthTexture;if(Te.__boundDepthTexture!==De){if(De!==null&&we.has(De)&&(E.width!==De.image.width||E.height!==De.image.height))throw new Error("WebGLRenderTarget: Attached DepthTexture is initialized to the incorrect size.");R.setupDepthRenderbuffer(E)}}const Fe=E.texture;(Fe.isData3DTexture||Fe.isDataArrayTexture||Fe.isCompressedArrayTexture)&&(pe=!0);const ze=we.get(E).__webglFramebuffer;E.isWebGLCubeRenderTarget?(Array.isArray(ze[B])?V=ze[B][W]:V=ze[B],re=!0):E.samples>0&&R.useMultisampledRTT(E)===!1?V=we.get(E).__webglMultisampledFramebuffer:Array.isArray(ze)?V=ze[W]:V=ze,C.copy(E.viewport),F.copy(E.scissor),N=E.scissorTest}else C.copy(oe).multiplyScalar(I).floor(),F.copy(le).multiplyScalar(I).floor(),N=Re;if(W!==0&&(V=Hc),Me.bindFramebuffer(L.FRAMEBUFFER,V)&&X&&Me.drawBuffers(E,V),Me.viewport(C),Me.scissor(F),Me.setScissorTest(N),re){const Te=we.get(E.texture);L.framebufferTexture2D(L.FRAMEBUFFER,L.COLOR_ATTACHMENT0,L.TEXTURE_CUBE_MAP_POSITIVE_X+B,Te.__webglTexture,W)}else if(pe){const Te=we.get(E.texture),Fe=B;L.framebufferTextureLayer(L.FRAMEBUFFER,L.COLOR_ATTACHMENT0,Te.__webglTexture,W,Fe)}else if(E!==null&&W!==0){const Te=we.get(E.texture);L.framebufferTexture2D(L.FRAMEBUFFER,L.COLOR_ATTACHMENT0,L.TEXTURE_2D,Te.__webglTexture,W)}x=-1},this.readRenderTargetPixels=function(E,B,W,X,V,re,pe){if(!(E&&E.isWebGLRenderTarget)){console.error("THREE.WebGLRenderer.readRenderTargetPixels: renderTarget is not THREE.WebGLRenderTarget.");return}let Se=we.get(E).__webglFramebuffer;if(E.isWebGLCubeRenderTarget&&pe!==void 0&&(Se=Se[pe]),Se){Me.bindFramebuffer(L.FRAMEBUFFER,Se);try{const Te=E.texture,Fe=Te.format,ze=Te.type;if(!Ce.textureFormatReadable(Fe)){console.error("THREE.WebGLRenderer.readRenderTargetPixels: renderTarget is not in RGBA or implementation defined format.");return}if(!Ce.textureTypeReadable(ze)){console.error("THREE.WebGLRenderer.readRenderTargetPixels: renderTarget is not in UnsignedByteType or implementation defined type.");return}B>=0&&B<=E.width-X&&W>=0&&W<=E.height-V&&L.readPixels(B,W,X,V,He.convert(Fe),He.convert(ze),re)}finally{const Te=D!==null?we.get(D).__webglFramebuffer:null;Me.bindFramebuffer(L.FRAMEBUFFER,Te)}}},this.readRenderTargetPixelsAsync=async function(E,B,W,X,V,re,pe){if(!(E&&E.isWebGLRenderTarget))throw new Error("THREE.WebGLRenderer.readRenderTargetPixels: renderTarget is not THREE.WebGLRenderTarget.");let Se=we.get(E).__webglFramebuffer;if(E.isWebGLCubeRenderTarget&&pe!==void 0&&(Se=Se[pe]),Se){const Te=E.texture,Fe=Te.format,ze=Te.type;if(!Ce.textureFormatReadable(Fe))throw new Error("THREE.WebGLRenderer.readRenderTargetPixelsAsync: renderTarget is not in RGBA or implementation defined format.");if(!Ce.textureTypeReadable(ze))throw new Error("THREE.WebGLRenderer.readRenderTargetPixelsAsync: renderTarget is not in UnsignedByteType or implementation defined type.");if(B>=0&&B<=E.width-X&&W>=0&&W<=E.height-V){Me.bindFramebuffer(L.FRAMEBUFFER,Se);const De=L.createBuffer();L.bindBuffer(L.PIXEL_PACK_BUFFER,De),L.bufferData(L.PIXEL_PACK_BUFFER,re.byteLength,L.STREAM_READ),L.readPixels(B,W,X,V,He.convert(Fe),He.convert(ze),0);const qe=D!==null?we.get(D).__webglFramebuffer:null;Me.bindFramebuffer(L.FRAMEBUFFER,qe);const Ze=L.fenceSync(L.SYNC_GPU_COMMANDS_COMPLETE,0);return L.flush(),await Hl(L,Ze,4),L.bindBuffer(L.PIXEL_PACK_BUFFER,De),L.getBufferSubData(L.PIXEL_PACK_BUFFER,0,re),L.deleteBuffer(De),L.deleteSync(Ze),re}else throw new Error("THREE.WebGLRenderer.readRenderTargetPixelsAsync: requested read bounds are out of range.")}},this.copyFramebufferToTexture=function(E,B=null,W=0){E.isTexture!==!0&&(Fn("WebGLRenderer: copyFramebufferToTexture function signature has changed."),B=arguments[0]||null,E=arguments[1]);const X=Math.pow(2,-W),V=Math.floor(E.image.width*X),re=Math.floor(E.image.height*X),pe=B!==null?B.x:0,Se=B!==null?B.y:0;R.setTexture2D(E,0),L.copyTexSubImage2D(L.TEXTURE_2D,W,0,0,pe,Se,V,re),Me.unbindTexture()};const Vc=L.createFramebuffer(),Gc=L.createFramebuffer();this.copyTextureToTexture=function(E,B,W=null,X=null,V=0,re=null){E.isTexture!==!0&&(Fn("WebGLRenderer: copyTextureToTexture function signature has changed."),X=arguments[0]||null,E=arguments[1],B=arguments[2],re=arguments[3]||0,W=null),re===null&&(V!==0?(Fn("WebGLRenderer: copyTextureToTexture function signature has changed to support src and dst mipmap levels."),re=V,V=0):re=0);let pe,Se,Te,Fe,ze,De,qe,Ze,ut;const ct=E.isCompressedTexture?E.mipmaps[re]:E.image;if(W!==null)pe=W.max.x-W.min.x,Se=W.max.y-W.min.y,Te=W.isBox3?W.max.z-W.min.z:1,Fe=W.min.x,ze=W.min.y,De=W.isBox3?W.min.z:0;else{const Nt=Math.pow(2,-V);pe=Math.floor(ct.width*Nt),Se=Math.floor(ct.height*Nt),E.isDataArrayTexture?Te=ct.depth:E.isData3DTexture?Te=Math.floor(ct.depth*Nt):Te=1,Fe=0,ze=0,De=0}X!==null?(qe=X.x,Ze=X.y,ut=X.z):(qe=0,Ze=0,ut=0);const $e=He.convert(B.format),Le=He.convert(B.type);let gt;B.isData3DTexture?(R.setTexture3D(B,0),gt=L.TEXTURE_3D):B.isDataArrayTexture||B.isCompressedArrayTexture?(R.setTexture2DArray(B,0),gt=L.TEXTURE_2D_ARRAY):(R.setTexture2D(B,0),gt=L.TEXTURE_2D),L.pixelStorei(L.UNPACK_FLIP_Y_WEBGL,B.flipY),L.pixelStorei(L.UNPACK_PREMULTIPLY_ALPHA_WEBGL,B.premultiplyAlpha),L.pixelStorei(L.UNPACK_ALIGNMENT,B.unpackAlignment);const Je=L.getParameter(L.UNPACK_ROW_LENGTH),Vt=L.getParameter(L.UNPACK_IMAGE_HEIGHT),Kn=L.getParameter(L.UNPACK_SKIP_PIXELS),Ct=L.getParameter(L.UNPACK_SKIP_ROWS),Pi=L.getParameter(L.UNPACK_SKIP_IMAGES);L.pixelStorei(L.UNPACK_ROW_LENGTH,ct.width),L.pixelStorei(L.UNPACK_IMAGE_HEIGHT,ct.height),L.pixelStorei(L.UNPACK_SKIP_PIXELS,Fe),L.pixelStorei(L.UNPACK_SKIP_ROWS,ze),L.pixelStorei(L.UNPACK_SKIP_IMAGES,De);const rt=E.isDataArrayTexture||E.isData3DTexture,Ut=B.isDataArrayTexture||B.isData3DTexture;if(E.isDepthTexture){const Nt=we.get(E),St=we.get(B),Tt=we.get(Nt.__renderTarget),jr=we.get(St.__renderTarget);Me.bindFramebuffer(L.READ_FRAMEBUFFER,Tt.__webglFramebuffer),Me.bindFramebuffer(L.DRAW_FRAMEBUFFER,jr.__webglFramebuffer);for(let Cn=0;Cn<Te;Cn++)rt&&(L.framebufferTextureLayer(L.READ_FRAMEBUFFER,L.COLOR_ATTACHMENT0,we.get(E).__webglTexture,V,De+Cn),L.framebufferTextureLayer(L.DRAW_FRAMEBUFFER,L.COLOR_ATTACHMENT0,we.get(B).__webglTexture,re,ut+Cn)),L.blitFramebuffer(Fe,ze,pe,Se,qe,Ze,pe,Se,L.DEPTH_BUFFER_BIT,L.NEAREST);Me.bindFramebuffer(L.READ_FRAMEBUFFER,null),Me.bindFramebuffer(L.DRAW_FRAMEBUFFER,null)}else if(V!==0||E.isRenderTargetTexture||we.has(E)){const Nt=we.get(E),St=we.get(B);Me.bindFramebuffer(L.READ_FRAMEBUFFER,Vc),Me.bindFramebuffer(L.DRAW_FRAMEBUFFER,Gc);for(let Tt=0;Tt<Te;Tt++)rt?L.framebufferTextureLayer(L.READ_FRAMEBUFFER,L.COLOR_ATTACHMENT0,Nt.__webglTexture,V,De+Tt):L.framebufferTexture2D(L.READ_FRAMEBUFFER,L.COLOR_ATTACHMENT0,L.TEXTURE_2D,Nt.__webglTexture,V),Ut?L.framebufferTextureLayer(L.DRAW_FRAMEBUFFER,L.COLOR_ATTACHMENT0,St.__webglTexture,re,ut+Tt):L.framebufferTexture2D(L.DRAW_FRAMEBUFFER,L.COLOR_ATTACHMENT0,L.TEXTURE_2D,St.__webglTexture,re),V!==0?L.blitFramebuffer(Fe,ze,pe,Se,qe,Ze,pe,Se,L.COLOR_BUFFER_BIT,L.NEAREST):Ut?L.copyTexSubImage3D(gt,re,qe,Ze,ut+Tt,Fe,ze,pe,Se):L.copyTexSubImage2D(gt,re,qe,Ze,Fe,ze,pe,Se);Me.bindFramebuffer(L.READ_FRAMEBUFFER,null),Me.bindFramebuffer(L.DRAW_FRAMEBUFFER,null)}else Ut?E.isDataTexture||E.isData3DTexture?L.texSubImage3D(gt,re,qe,Ze,ut,pe,Se,Te,$e,Le,ct.data):B.isCompressedArrayTexture?L.compressedTexSubImage3D(gt,re,qe,Ze,ut,pe,Se,Te,$e,ct.data):L.texSubImage3D(gt,re,qe,Ze,ut,pe,Se,Te,$e,Le,ct):E.isDataTexture?L.texSubImage2D(L.TEXTURE_2D,re,qe,Ze,pe,Se,$e,Le,ct.data):E.isCompressedTexture?L.compressedTexSubImage2D(L.TEXTURE_2D,re,qe,Ze,ct.width,ct.height,$e,ct.data):L.texSubImage2D(L.TEXTURE_2D,re,qe,Ze,pe,Se,$e,Le,ct);L.pixelStorei(L.UNPACK_ROW_LENGTH,Je),L.pixelStorei(L.UNPACK_IMAGE_HEIGHT,Vt),L.pixelStorei(L.UNPACK_SKIP_PIXELS,Kn),L.pixelStorei(L.UNPACK_SKIP_ROWS,Ct),L.pixelStorei(L.UNPACK_SKIP_IMAGES,Pi),re===0&&B.generateMipmaps&&L.generateMipmap(gt),Me.unbindTexture()},this.copyTextureToTexture3D=function(E,B,W=null,X=null,V=0){return E.isTexture!==!0&&(Fn("WebGLRenderer: copyTextureToTexture3D function signature has changed."),W=arguments[0]||null,X=arguments[1]||null,E=arguments[2],B=arguments[3],V=arguments[4]||0),Fn('WebGLRenderer: copyTextureToTexture3D function has been deprecated. Use "copyTextureToTexture" instead.'),this.copyTextureToTexture(E,B,W,X,V)},this.initRenderTarget=function(E){we.get(E).__webglFramebuffer===void 0&&R.setupRenderTarget(E)},this.initTexture=function(E){E.isCubeTexture?R.setTextureCube(E,0):E.isData3DTexture?R.setTexture3D(E,0):E.isDataArrayTexture||E.isCompressedArrayTexture?R.setTexture2DArray(E,0):R.setTexture2D(E,0),Me.unbindTexture()},this.resetState=function(){y=0,A=0,D=null,Me.reset(),tt.reset()},typeof __THREE_DEVTOOLS__<"u"&&__THREE_DEVTOOLS__.dispatchEvent(new CustomEvent("observe",{detail:this}))}get coordinateSystem(){return dn}get outputColorSpace(){return this._outputColorSpace}set outputColorSpace(e){this._outputColorSpace=e;const t=this.getContext();t.drawingBufferColorspace=Ke._getDrawingBufferColorSpace(e),t.unpackColorSpace=Ke._getUnpackColorSpace()}}const Sn=1e-6,pi=5e-5,Ta=1e-7;function vs(n,e){return n[0]*e[0]+n[1]*e[1]+n[2]*e[2]}function xs(n,e){return[n[0]-e[0],n[1]-e[1],n[2]-e[2]]}function Ms(n,e){return[n[1]*e[2]-n[2]*e[1],n[2]*e[0]-n[0]*e[2],n[0]*e[1]-n[1]*e[0]]}function om(n){const e=Math.hypot(n[0],n[1],n[2]);return e<1e-12?null:[n[0]/e,n[1]/e,n[2]/e]}function Cr(n,e){const t=n[0]-e[0],i=n[1]-e[1],r=n[2]-e[2];return t*t+i*i+r*r}function Aa(n){if(n.length<3)return 0;const e=n[0];let t=0,i=0,r=0;for(let a=1;a+1<n.length;a++){const s=xs(n[a],e),o=xs(n[a+1],e),c=Ms(s,o);t+=c[0],i+=c[1],r+=c[2]}return .5*Math.hypot(t,i,r)}function cm(n,e){const t=[],i=pi*pi;for(const f of n)t.some(m=>Cr(f,m)<=i)||t.push(f);if(t.length<3)return[];let r=0,a=0,s=0;for(const f of t)r+=f[0],a+=f[1],s+=f[2];r/=t.length,a/=t.length,s/=t.length;const o=[r,a,s],c=Math.abs(e[0])<.8?[1,0,0]:[0,1,0],l=om(Ms(c,e));if(!l)return[];const d=Ms(e,l),h=t.map(f=>{const m=xs(f,o),g=vs(m,l),_=vs(m,d);return{tacka:f,ugao:Math.atan2(_,g)}});return h.sort((f,m)=>f.ugao-m.ugao),h.map(f=>f.tacka)}function lm(n){return[{normala:[1,0,0],grupaId:"__okvir__",oznaka:"",temena:[[n,-n,-n],[n,n,-n],[n,n,n],[n,-n,n]]},{normala:[-1,0,0],grupaId:"__okvir__",oznaka:"",temena:[[-n,-n,n],[-n,n,n],[-n,n,-n],[-n,-n,-n]]},{normala:[0,1,0],grupaId:"__okvir__",oznaka:"",temena:[[-n,n,-n],[-n,n,n],[n,n,n],[n,n,-n]]},{normala:[0,-1,0],grupaId:"__okvir__",oznaka:"",temena:[[-n,-n,n],[-n,-n,-n],[n,-n,-n],[n,-n,n]]},{normala:[0,0,1],grupaId:"__okvir__",oznaka:"",temena:[[-n,-n,n],[n,-n,n],[n,n,n],[-n,n,n]]},{normala:[0,0,-1],grupaId:"__okvir__",oznaka:"",temena:[[n,-n,-n],[-n,-n,-n],[-n,n,-n],[n,n,-n]]}]}function Fr(n){if(n.length===0)return{temena:[],pljosni:[]};let e=1;const t=[];for(let c=0;c<n.length;c++){const l=n[c],d=Math.hypot(l.normala[0],l.normala[1],l.normala[2]);if(d<1e-12)continue;const h=[l.normala[0]/d,l.normala[1]/d,l.normala[2]/d],f=l.d;e=Math.max(e,Math.abs(f)),t.push({normala:h,d:f,grupaId:l.grupaId??`forma-${c}`,oznaka:l.oznaka??""})}let i=lm(Math.max(12,e*6));for(const c of t){const l=[],d=[];for(const f of i){const m=f.temena.length;if(m<3)continue;const g=f.temena.map(w=>vs(c.normala,w)-c.d),_=[];for(let w=0;w<m;w++){const b=(w+1)%m,S=f.temena[w],T=f.temena[b],y=g[w],A=g[b],D=y<=Sn,x=A<=Sn;if(Math.abs(y)<=Sn*4&&d.push(S),D&&_.push(S),y<-Sn&&A>Sn||y>Sn&&A<-Sn){const v=y/(y-A),C=[S[0]+(T[0]-S[0])*v,S[1]+(T[1]-S[1])*v,S[2]+(T[2]-S[2])*v];_.push(C),d.push(C)}else!D&&x&&Math.abs(A)<=Sn&&d.push(T)}const p=[],u=pi*pi;for(const w of _)(p.length===0||Cr(w,p[p.length-1])>u)&&p.push(w);p.length>1&&Cr(p[0],p[p.length-1])<=u&&p.pop(),p.length>=3&&Aa(p)>Ta&&l.push({temena:p,normala:f.normala,grupaId:f.grupaId,oznaka:f.oznaka})}const h=cm(d,c.normala);if(h.length>=3&&Aa(h)>Ta&&l.push({temena:h,normala:c.normala,grupaId:c.grupaId,oznaka:c.oznaka}),i=l,i.length===0)break}const r=[],a=[],s=pi*pi;function o(c){for(let l=0;l<r.length;l++)if(Cr(r[l],c)<=s)return l;return r.push([Math.abs(c[0])<1e-10?0:c[0],Math.abs(c[1])<1e-10?0:c[1],Math.abs(c[2])<1e-10?0:c[2]]),r.length-1}for(const c of i){if(c.grupaId==="__okvir__")continue;const l=Aa(c.temena);if(l<=Ta)continue;const d=c.temena.map(p=>o(p)),h=[];for(const p of d)(h.length===0||h[h.length-1]!==p)&&h.push(p);if(h.length>1&&h[0]===h[h.length-1]&&h.pop(),h.length<3)continue;let f=0,m=0,g=0;for(const p of h){const u=r[p];f+=u[0],m+=u[1],g+=u[2]}const _=h.length;a.push({indeksiTemena:h,normala:c.normala,centar:[f/_,m/_,g/_],povrsina:l,grupaId:c.grupaId,oznaka:c.oznaka})}return{temena:r,pljosni:a}}const um=[[0,1,2],[0,2,1],[1,0,2],[1,2,0],[2,0,1],[2,1,0]],dm=[[1,1,1],[1,1,-1],[1,-1,1],[1,-1,-1],[-1,1,1],[-1,1,-1],[-1,-1,1],[-1,-1,-1]];function xi(n){return n<0?`${Math.abs(n)}̄`:String(n)}function hm(n){const e=Math.abs(n[0])>=10||Math.abs(n[1])>=10||Math.abs(n[2])>=10;return`(${[xi(n[0]),xi(n[1]),xi(n[2])].join(e?" ":"")})`}function fm(n){const e=Math.abs(n[0])>=10||Math.abs(n[1])>=10||Math.abs(n[2])>=10;return`{${[xi(n[0]),xi(n[1]),xi(n[2])].join(e?" ":"")}}`}function zr(n){const[e,t,i]=n;if(!Number.isFinite(e)||!Number.isFinite(t)||!Number.isFinite(i))throw new Error("Милерови индекси морају бити коначни бројеви.");if(e===0&&t===0&&i===0)throw new Error("Милерови индекси не могу бити (000).");const r=new Set,a=[],s=[Math.trunc(e),Math.trunc(t),Math.trunc(i)];for(const[o,c,l]of um){const d=s[o],h=s[c],f=s[l];for(const[m,g,_]of dm){const p=d===0?0:d*m,u=h===0?0:h*g,w=f===0?0:f*_,b=`${p},${u},${w}`;if(r.has(b))continue;r.add(b);const S=Math.hypot(p,u,w),T=[p,u,w];a.push({hkl:T,normala:[p/S,u/S,w/S],oznaka:hm(T)})}}return a}function kr(n){const e=[];for(const d of n.pljosni)e.includes(d.grupaId)||e.push(d.grupaId);const t=[],i=[],r=[],a=[];for(let d=0;d<e.length;d++){const h=e[d],f=t.length/3;for(let g=0;g<n.pljosni.length;g++){const _=n.pljosni[g];if(_.grupaId!==h)continue;const p=_.indeksiTemena;if(p.length<3)continue;const u=n.temena[p[0]],[w,b,S]=_.normala;for(let T=1;T+1<p.length;T++){const y=n.temena[p[T]],A=n.temena[p[T+1]];t.push(u[0],u[1],u[2],y[0],y[1],y[2],A[0],A[1],A[2]),i.push(w,b,S,w,b,S,w,b,S),r.push(g)}}const m=t.length/3;m>f&&a.push({pocetak:f,broj:m-f,indeksMaterijala:d})}const s=new st;s.setAttribute("position",new nt(t,3)),s.setAttribute("normal",new nt(i,3));for(const d of a)s.addGroup(d.pocetak,d.broj,d.indeksMaterijala);const o=new Set,c=[];for(const d of n.pljosni){const h=d.indeksiTemena;for(let f=0;f<h.length;f++){const m=h[f],g=h[(f+1)%h.length],_=m<g?`${m}-${g}`:`${g}-${m}`;if(o.has(_))continue;o.add(_);const p=n.temena[m],u=n.temena[g];c.push(p[0],p[1],p[2],u[0],u[1],u[2])}}const l=new st;return l.setAttribute("position",new nt(c,3)),{geometrijaMreze:s,geometrijaIvica:l,mapaTrougaoUPljosan:r,redosledGrupa:e}}function di(n,e,t){return Math.max(e,Math.min(t,n))}class pm{stanje;pocetno;minUdaljenost;maksUdaljenost;opcije;vuceMisem=!1;prethodniX=0;prethodniY=0;dodirAktiviran=!1;prethodniDodirX=0;prethodniDodirY=0;prethodniRazmakPrstiju=0;pocetakDodiraX=0;pocetakDodiraY=0;dodirPomeren=!1;cistaci=[];constructor(e){this.opcije=e,this.pocetno={...e.pocetno},this.stanje={...e.pocetno},this.minUdaljenost=e.minUdaljenost??2,this.maksUdaljenost=e.maksUdaljenost??24,this.poveziDogadjaje()}trenutnoStanje(){return{...this.stanje}}rotirajAzimut(e){this.stanje.theta+=e,this.opcije.naPromenu(this.trenutnoStanje())}rotirajElevaciju(e){this.stanje.phi=di(this.stanje.phi+e,.15,Math.PI-.15),this.opcije.naPromenu(this.trenutnoStanje())}zumiraj(e){this.stanje.udaljenost=di(this.stanje.udaljenost*e,this.minUdaljenost,this.maksUdaljenost),this.opcije.naPromenu(this.trenutnoStanje())}resetuj(){this.stanje={...this.pocetno},this.opcije.naPromenu(this.trenutnoStanje())}postaviAktivacijuDodira(e){this.dodirAktiviran=e,this.opcije.platno.classList.toggle("udzbenik-scena-platno--dodir-aktivan",e),this.opcije.dugmeDodira.hidden=!e,this.opcije.priPromeniAktivacijeDodira?.(e)}poveziDogadjaje(){const{bina:e,platno:t,dugmeDodira:i}=this.opcije,r=g=>{if(g.pointerType!=="touch"&&g.button===0){this.vuceMisem=!0,this.prethodniX=g.clientX,this.prethodniY=g.clientY;try{t.setPointerCapture(g.pointerId)}catch{}}},a=g=>{if(g.pointerType==="touch"||!this.vuceMisem)return;const _=g.clientX-this.prethodniX,p=g.clientY-this.prethodniY;this.prethodniX=g.clientX,this.prethodniY=g.clientY,this.stanje.theta-=_*.008,this.stanje.phi=di(this.stanje.phi-p*.008,.15,Math.PI-.15),this.opcije.naPromenu(this.trenutnoStanje())},s=g=>{if(g.pointerType!=="touch"){this.vuceMisem=!1;try{t.hasPointerCapture(g.pointerId)&&t.releasePointerCapture(g.pointerId)}catch{}}},o=g=>{if(!(document.activeElement===e||e.contains(document.activeElement))&&!g.ctrlKey&&!g.metaKey)return;g.preventDefault();const p=g.deltaY>0?1.09:.92;this.zumiraj(p)},c=g=>{if(g.touches.length===2){const _=g.touches[0],p=g.touches[1];this.prethodniDodirX=(_.clientX+p.clientX)/2,this.prethodniDodirY=(_.clientY+p.clientY)/2,this.prethodniRazmakPrstiju=Math.hypot(p.clientX-_.clientX,p.clientY-_.clientY)}else if(g.touches.length===1){const _=g.touches[0];this.pocetakDodiraX=_.clientX,this.pocetakDodiraY=_.clientY,this.prethodniDodirX=_.clientX,this.prethodniDodirY=_.clientY,this.dodirPomeren=!1}},l=g=>{if(g.touches.length===2){g.preventDefault();const _=g.touches[0],p=g.touches[1],u=(_.clientX+p.clientX)/2,w=(_.clientY+p.clientY)/2,b=Math.hypot(p.clientX-_.clientX,p.clientY-_.clientY),S=u-this.prethodniDodirX,T=w-this.prethodniDodirY;if(this.prethodniDodirX=u,this.prethodniDodirY=w,this.stanje.theta-=S*.008,this.stanje.phi=di(this.stanje.phi-T*.008,.15,Math.PI-.15),this.prethodniRazmakPrstiju>8&&b>8){const y=this.prethodniRazmakPrstiju/b;this.stanje.udaljenost=di(this.stanje.udaljenost*y,this.minUdaljenost,this.maksUdaljenost)}this.prethodniRazmakPrstiju=b,this.dodirPomeren=!0,this.opcije.naPromenu(this.trenutnoStanje())}else if(g.touches.length===1){const _=g.touches[0];if(Math.hypot(_.clientX-this.pocetakDodiraX,_.clientY-this.pocetakDodiraY)>8&&(this.dodirPomeren=!0),this.dodirAktiviran){g.preventDefault();const p=_.clientX-this.prethodniDodirX,u=_.clientY-this.prethodniDodirY;this.prethodniDodirX=_.clientX,this.prethodniDodirY=_.clientY,this.stanje.theta-=p*.009,this.stanje.phi=di(this.stanje.phi-u*.009,.15,Math.PI-.15),this.opcije.naPromenu(this.trenutnoStanje())}}},d=g=>{g.touches.length===0&&!this.dodirPomeren&&g.changedTouches.length===1&&this.postaviAktivacijuDodira(!this.dodirAktiviran)},h=()=>{this.postaviAktivacijuDodira(!1)},f=g=>{this.dodirAktiviran&&g.target instanceof Node&&!e.contains(g.target)&&this.postaviAktivacijuDodira(!1)},m=g=>{if(!(g.target instanceof HTMLElement&&g.target!==e&&(g.target.tagName==="BUTTON"||g.target.tagName==="INPUT")))switch(g.key){case"ArrowLeft":g.preventDefault(),this.rotirajAzimut(-.12);break;case"ArrowRight":g.preventDefault(),this.rotirajAzimut(.12);break;case"ArrowUp":g.preventDefault(),this.rotirajElevaciju(-.12);break;case"ArrowDown":g.preventDefault(),this.rotirajElevaciju(.12);break;case"+":case"=":g.preventDefault(),this.zumiraj(.88);break;case"-":case"_":g.preventDefault(),this.zumiraj(1.14);break;case"r":case"R":case"р":case"Р":g.preventDefault(),this.opcije.naReset();break;case" ":g.preventDefault(),this.opcije.naPrekidacPauze();break;case"Escape":this.dodirAktiviran&&(g.preventDefault(),this.postaviAktivacijuDodira(!1));break}};t.addEventListener("pointerdown",r),t.addEventListener("pointermove",a),t.addEventListener("pointerup",s),t.addEventListener("pointercancel",s),t.addEventListener("wheel",o,{passive:!1}),t.addEventListener("touchstart",c,{passive:!0}),t.addEventListener("touchmove",l,{passive:!1}),t.addEventListener("touchend",d),i.addEventListener("click",h),document.addEventListener("touchstart",f,{passive:!0}),e.addEventListener("keydown",m),this.cistaci.push(()=>{t.removeEventListener("pointerdown",r),t.removeEventListener("pointermove",a),t.removeEventListener("pointerup",s),t.removeEventListener("pointercancel",s),t.removeEventListener("wheel",o),t.removeEventListener("touchstart",c),t.removeEventListener("touchmove",l),t.removeEventListener("touchend",d),i.removeEventListener("click",h),document.removeEventListener("touchstart",f),e.removeEventListener("keydown",m)})}raspolazi(){for(const e of this.cistaci)e();this.cistaci.length=0}}let ln=null,mi=null,Wn=0,Xn=0;function mm(){if(ln)return ln;const n=document.createElement("canvas"),e=n.getContext("webgl2",{antialias:!0,alpha:!1,preserveDrawingBuffer:!1})??n.getContext("webgl",{antialias:!0,alpha:!1,preserveDrawingBuffer:!1});if(!e)throw new Error("WebGL контекст није доступан у овом прегледачу.");const t=new sm({canvas:n,context:e,antialias:!0,alpha:!1,powerPreference:"default"});return t.setPixelRatio(1),t.outputColorSpace=Lt,mi=n,ln=t,Wn=320,Xn=240,ln.setSize(Wn,Xn,!1),ln}function gm(){ln&&(ln.forceContextLoss(),ln.dispose(),ln=null,mi=null,Wn=0,Xn=0)}function $n(n){n.traverse(e=>{const t=e;t.geometry&&typeof t.geometry.dispose=="function"&&t.geometry.dispose();const i=t.material;if(Array.isArray(i))for(const r of i)Qo(r);else i&&Qo(i)})}function Qo(n){for(const e of Object.values(n))e instanceof bt&&e.dispose();n.dispose()}function _m(n,e,t,i){const r=mm(),a=t.platno.getContext("2d");if(!a||!mi)throw new Error("2D контекст платна није доступан.");const s=typeof window<"u"&&typeof window.matchMedia=="function"&&window.matchMedia("(prefers-reduced-motion: reduce)").matches,o=new pu,c=new zt(42,16/9,.1,100),l=new k(0,0,0),d=new Su(new ve(1,1,1),.72),h=new To(new ve(1,1,1),.95);h.position.set(5,8,6);const f=new To(new ve(1,1,1),.38);f.position.set(-5,-3,-4),o.add(d,h,f);const m=n.pocetnaKamera?.(e)??{theta:.62,phi:1.12,udaljenost:6.2};function g(Q){const ge=Math.sin(Q.phi);c.position.set(l.x+Q.udaljenost*ge*Math.sin(Q.theta),l.y+Q.udaljenost*Math.cos(Q.phi),l.z+Q.udaljenost*ge*Math.cos(Q.theta)),c.lookAt(l),c.updateMatrixWorld()}g(m);let _=!1,p=!1,u=!0,w=n.imaPodrazumevanuAnimaciju?n.imaPodrazumevanuAnimaciju(e):!0,b=s||!w,S=null,T=null,y=0,A=0,D=Math.max(240,t.bina.clientWidth||600),x=Math.max(180,t.bina.clientHeight||360),v=null;function C(){if(_||p||!mi||!a)return;const Q=t.bina.clientWidth,ge=t.bina.clientHeight;Q>0&&ge>0&&(D=Q,x=ge);const ue=Math.min(typeof window<"u"&&window.devicePixelRatio||1,2),K=Math.max(1,Math.round(D*ue)),ie=Math.max(1,Math.round(x*ue));(t.platno.width!==K||t.platno.height!==ie)&&(t.platno.width=K,t.platno.height=ie),c.aspect=D/Math.max(1,x),c.updateProjectionMatrix();const ae=Math.min(4096,Math.max(Wn,K)),L=Math.min(4096,Math.max(Xn,ie));(ae>Wn||L>Xn)&&(Wn=ae,Xn=L,r.setSize(Wn,Xn,!1));const Ie=new ve(Xr.token("--bg-card"));r.setViewport(0,0,K,ie),r.setScissor(0,0,K,ie),r.setScissorTest(!0),r.setClearColor(Ie,1),r.clear(!0,!0,!0),r.render(o,c);const Pe=Math.max(0,mi.height-ie);a.drawImage(mi,0,Pe,K,ie,0,0,K,ie),v?.posleRendera?.()}function F(){_||p||S!==null||T!==null||(T=requestAnimationFrame(()=>{T=null,C()}))}function N(){const Q=typeof document<"u"&&document.hidden;return!_&&!p&&w&&!b&&u&&!Q}function P(Q){if(S=null,!N())return;const ge=y>0?Math.min(.05,(Q-y)/1e3):.016;y=Q,A+=ge,v?.azuriraj?.(ge,A),C(),N()&&(S=requestAnimationFrame(P))}function U(){t.azurirajDugmePauze(b,w),N()?S===null&&(y=performance.now(),S=requestAnimationFrame(P)):S!==null&&(cancelAnimationFrame(S),S=null)}function z(Q){const ge=Q.clone().project(c),ue=ge.z>=-1&&ge.z<=1;return{x:(ge.x*.5+.5)*D,y:(-ge.y*.5+.5)*x,vidljivo:ue}}const H={scena3D:o,kamera:c,platno:t.platno,slojEtiketa:t.slojEtiketa,gornjeKontrole:t.gornjeKontrole,podnozje:t.podnozje,api:i,tema:Xr,smanjenPokret:s,zatraziRender:F,postaviImaAnimaciju:Q=>{w=Q,Q||(b=!0),U()},prikaziRezervu:Q=>{p=!0,U(),t.prikaziRezervu(Q)},projektujU2D:z},I=new pm({bina:t.bina,platno:t.platno,dugmeDodira:t.dugmeDodira,pocetno:m,naPromenu:Q=>{g(Q),F()},naReset:()=>{I.resetuj(),v?.resetuj?.(),C()},naPrekidacPauze:()=>{w&&(b=!b,U())}});v=n.kreiraj(H,e);const G=()=>{I.resetuj(),v?.resetuj?.(),C()},q=()=>{w&&(b=!b,U())},oe=()=>{b=!0,U(),v?.korak?v.korak():(A+=.45,v?.azuriraj?.(.45,A)),C()},le=()=>I.zumiraj(.86),Re=()=>I.zumiraj(1.16);t.dugmeReset.addEventListener("click",G),t.dugmePauza.addEventListener("click",q),t.dugmeKorak.addEventListener("click",oe),t.dugmeZumPlus.addEventListener("click",le),t.dugmeZumMinus.addEventListener("click",Re);let Y=null;typeof ResizeObserver<"u"&&(Y=new ResizeObserver(Q=>{for(const ge of Q){const ue=Math.round(ge.contentRect.width),K=Math.round(ge.contentRect.height);ue>0&&K>0&&(ue!==D||K!==x)&&(D=ue,x=K,C())}}),Y.observe(t.bina));let te=null;typeof IntersectionObserver<"u"&&(te=new IntersectionObserver(Q=>{for(const ge of Q)u=ge.isIntersecting,U()},{threshold:.05}),te.observe(t.bina));const de=()=>{U(),document.hidden||F()};document.addEventListener("visibilitychange",de);const se=Xr.pretplati(Q=>{v?.osveziTemu?.(Q),C()});return C(),U(),()=>{_||(_=!0,S!==null&&(cancelAnimationFrame(S),S=null),T!==null&&(cancelAnimationFrame(T),T=null),Y?.disconnect(),te?.disconnect(),document.removeEventListener("visibilitychange",de),se(),t.dugmeReset.removeEventListener("click",G),t.dugmePauza.removeEventListener("click",q),t.dugmeKorak.removeEventListener("click",oe),t.dugmeZumPlus.removeEventListener("click",le),t.dugmeZumMinus.removeEventListener("click",Re),I.raspolazi(),v?.raspolazi?.(),$n(o),o.clear(),t.slojEtiketa.replaceChildren(),t.gornjeKontrole.replaceChildren(),t.podnozje.replaceChildren())}}function vm(n,e){const t=e??56,i=Math.round((180-t)*10)/10;switch(n){case"kubna":return{naziv:"Кубна цепљивост {100}",brojPravaca:"3 правца",uglovi:"90°",podrazumevaniPrimer:"халит, галенит"};case"oktaedarska":return{naziv:"Октаедарска цепљивост {111}",brojPravaca:"4 правца",uglovi:"70,5° и 109,5°",podrazumevaniPrimer:"флуорит, дијамант"};case"dodekaedarska":return{naziv:"Додекаедарска цепљивост {110}",brojPravaca:"6 праваца",uglovi:"60°, 90° и 120°",podrazumevaniPrimer:"сфалерит"};case"romboedarska":return{naziv:"Ромбоедарска цепљивост {101̄1}",brojPravaca:"3 правца",uglovi:"~75° и ~105° (≠ 90°)",podrazumevaniPrimer:"калцит, доломит"};case"bazalna":return{naziv:"Базална (пинакоидална) цепљивост {001}",brojPravaca:"1 правац",uglovi:"паралелне ламеле (0°)",podrazumevaniPrimer:"лискун (мусковит), графит"};case"prizmatska":return{naziv:"Призматска цепљивост {110}",brojPravaca:"2 правца",uglovi:`${t}° и ${i}°`,podrazumevaniPrimer:t>75?"пироксен":"амфибол"};case"nema":return{naziv:"Нема цепљивости (шкољкаст прелом)",brojPravaca:"0 праваца",uglovi:"нема равни цепљивости",podrazumevaniPrimer:"кварц"}}}function On(n,e,t,i){const r=Fr(n);if(r.pljosni.length<4||r.temena.length<4)return null;const a=kr(r),s=new ht;return s.add(new it(a.geometrijaMreze,t),new Bt(a.geometrijaIvica,i)),{grupa:s,smerRazdvajanja:e}}function sn(n,e,t,i,r){const a=new Wi(t,t),s=new it(a,i),o=new Bt(new ms(a),r),c=new ht;c.add(s,o);const l=new k(...n).normalize();return c.quaternion.setFromUnitVectors(new k(0,0,1),l),c.position.copy(l).multiplyScalar(e),c}function hi(n,e){const t=Math.hypot(n-.35,e-.25),i=.055*Math.sin(t*13.5);return .28*(n*n-.5*e*e)+.18*n+i}function xm(n,e,t,i){if(!n){const h=[{normala:[0,-1,0],d:1.15}];for(let m=0;m<6;m++){const g=m*Math.PI/3,_=Math.cos(g),p=Math.sin(g);h.push({normala:[_,0,p],d:.95}),h.push({normala:[_*.72,.69,p*.72],d:1.28}),h.push({normala:[_*.72,-.69,p*.72],d:1.28})}const f=On(h,new k(0,0,0),e,i);return{fragmenti:f?[f]:[]}}const o=12,c=24;function l(h,f){const m=(f%(Math.PI/3)+Math.PI/3)%(Math.PI/3)-Math.PI/6,g=.95*Math.cos(Math.PI/6)/Math.cos(m);return[h*g*Math.cos(f),h*g*Math.sin(f)]}function d(h){const f=[],m=[],g=[],_=h?1.15:-1.15,p=h?1.85:-1.85;for(let T=0;T<o;T++){const y=T/o,A=(T+1)/o;for(let D=0;D<c;D++){const x=D/c*Math.PI*2,v=(D+1)/c*Math.PI*2,[C,F]=l(y,x),[N,P]=l(A,x),[U,z]=l(A,v),[H,I]=l(y,v),G=hi(C,F),q=hi(N,P),oe=hi(U,z),le=hi(H,I);h?m.push(C,G,F,U,oe,z,N,q,P,C,G,F,H,le,I,U,oe,z):m.push(C,G,F,N,q,P,U,oe,z,C,G,F,U,oe,z,H,le,I)}}for(let T=0;T<c;T++){const y=T/c*Math.PI*2,A=(T+1)/c*Math.PI*2,[D,x]=l(1,y),[v,C]=l(1,A),F=hi(D,x),N=hi(v,C);h?(f.push(D,F,x,v,N,C,v,_,C,D,F,x,v,_,C,D,_,x),f.push(D,_,x,v,_,C,0,p,0)):(f.push(D,_,x,v,_,C,v,N,C,D,_,x,v,N,C,D,F,x),f.push(v,_,C,D,_,x,0,p,0)),g.push(D,F,x,v,N,C),g.push(D,_,x,v,_,C),T%(c/6)===0&&(g.push(D,F,x,D,_,x),g.push(D,_,x,0,p,0))}const u=new st;u.setAttribute("position",new nt(f,3)),u.computeVertexNormals();const w=new st;w.setAttribute("position",new nt(m,3)),w.computeVertexNormals();const b=new st;b.setAttribute("position",new nt(g,3));const S=new ht;return S.add(new it(u,e),new it(w,t),new Bt(b,i)),S}return{fragmenti:[{grupa:d(!0),smerRazdvajanja:new k(.18,.55,.1)},{grupa:d(!1),smerRazdvajanja:new k(-.18,-.55,-.1)}]}}const Mm={imaPodrazumevanuAnimaciju(n){return!(n.vrsta==="nema"&&!n.prikazi_prelom)},pocetnaKamera(){return{theta:.68,phi:1.14,udaljenost:5.9}},kreiraj(n,e){const t=e.vrsta,i=e.ugao??56,r=e.prikazi_prelom??!1,a=new ht,s=new ht,o=new ht;a.add(s,o),n.scena3D.add(a);const c=new wt({color:new ve(n.tema.token("--primary")),transparent:!0,opacity:.86,roughness:.32,metalness:.08,flatShading:!0}),l=new wt({color:new ve(n.tema.token("--accent")),roughness:.22,metalness:.15,side:kt}),d=new It({color:new ve(n.tema.token("--text-primary"))}),h=new Hr({color:new ve(n.tema.token("--accent")),transparent:!0,opacity:.26,side:kt,depthWrite:!1}),f=new It({color:new ve(n.tema.token("--accent"))}),m=[];function g(){if(t==="kubna"){const T=[-1,1];for(const y of T)for(const A of T)for(const D of T){const x=[{normala:[y,0,0],d:1.05},{normala:[-y,0,0],d:0},{normala:[0,A,0],d:1.05},{normala:[0,-A,0],d:0},{normala:[0,0,D],d:1.05},{normala:[0,0,-D],d:0}],v=On(x,new k(y,A,D).normalize().multiplyScalar(.52),c,d);v&&m.push(v)}o.add(sn([1,0,0],0,2.6,h,f),sn([0,1,0],0,2.6,h,f),sn([0,0,1],0,2.6,h,f))}else if(t==="oktaedarska"){const T=zr([1,1,1]).map(A=>({normala:A.normala,d:1.08})),y=[[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]];for(let A=0;A<16;A++){const D=[...T],x=new k;for(let C=0;C<4;C++){const F=(A&1<<C)!==0?1:-1,N=y[C];D.push({normala:[N[0]*F,N[1]*F,N[2]*F],d:0}),x.add(new k(N[0]*F,N[1]*F,N[2]*F))}const v=On(D,x.lengthSq()>1e-4?x.normalize().multiplyScalar(.52):x,c,d);v&&m.push(v)}for(const A of y)o.add(sn(A,0,2.8,h,f))}else if(t==="dodekaedarska"){const T=zr([1,1,0]).map(D=>({normala:D.normala,d:1.12})),y=[[1,1,0],[1,-1,0],[1,0,1],[1,0,-1],[0,1,1],[0,1,-1]];for(const D of y)o.add(sn(D,0,2.7,h,f));const A=[[1,1,0],[1,-1,0],[0,1,1]];for(let D=0;D<8;D++){const x=[...T],v=new k;for(let F=0;F<3;F++){const N=(D&1<<F)!==0?1:-1,P=A[F];x.push({normala:[P[0]*N,P[1]*N,P[2]*N],d:0}),v.add(new k(P[0]*N,P[1]*N,P[2]*N))}const C=On(x,v.normalize().multiplyScalar(.5),c,d);C&&m.push(C)}}else if(t==="romboedarska"){const T=[1,.26,.14],y=[.24,1,.22],A=[.18,.26,1],D=[T,y,A],x=[];for(const C of D)x.push({normala:C,d:1}),x.push({normala:[-C[0],-C[1],-C[2]],d:1}),o.add(sn(C,0,2.8,h,f));const v=[-1,1];for(const C of v)for(const F of v)for(const N of v){const P=[...x,{normala:[-T[0]*C,-T[1]*C,-T[2]*C],d:0},{normala:[-y[0]*F,-y[1]*F,-y[2]*F],d:0},{normala:[-A[0]*N,-A[1]*N,-A[2]*N],d:0}],U=new k(T[0]*C+y[0]*F+A[0]*N,T[1]*C+y[1]*F+A[1]*N,T[2]*C+y[2]*F+A[2]*N).normalize().multiplyScalar(.5),z=On(P,U,c,d);z&&m.push(z)}}else if(t==="bazalna"){const T=[];for(let x=0;x<6;x++){const v=x*Math.PI/3;T.push({normala:[Math.cos(v),0,Math.sin(v)],d:1.15})}const y=5,A=1.1,D=A/y;for(let x=0;x<y;x++){const v=-A/2+x*D,C=v+D,F=[...T,{normala:[0,1,0],d:C},{normala:[0,-1,0],d:-v}],N=x-(y-1)/2,P=On(F,new k(N*.08,N*.28,0),c,d);P&&m.push(P),x>0&&o.add(sn([0,1,0],v,2.7,h,f))}}else if(t==="prizmatska"){const T=i*Math.PI/180*.5,y=[Math.sin(T),0,Math.cos(T)],A=[-Math.sin(T),0,Math.cos(T)],D=[{normala:[0,1,0],d:1.3},{normala:[0,-1,0],d:1.3},{normala:y,d:.9},{normala:[-y[0],0,-y[2]],d:.9},{normala:A,d:.9},{normala:[-A[0],0,-A[2]],d:.9}];o.add(sn(y,0,2.9,h,f),sn(A,0,2.9,h,f));const x=[-1,1];for(const v of x)for(const C of x){const F=[...D,{normala:[-y[0]*v,0,-y[2]*v],d:0},{normala:[-A[0]*C,0,-A[2]*C],d:0}],N=new k(y[0]*v+A[0]*C,0,y[2]*v+A[2]*C).normalize().multiplyScalar(.48),P=On(F,N,c,d);P&&m.push(P)}}else{const T=xm(r,c,l,d);m.push(...T.fragmenti)}for(const T of m)s.add(T.grupa)}g();const _=vm(t,i),p=e.primer||_.podrazumevaniPrimer,u=document.createElement("div");u.className="udzbenik-scena-info-red udzbenik-cepljivost-meta";const w=[[Ge("brojPravacaCepljivosti"),_.brojPravaca],[Ge("ugloviCepljivosti"),_.uglovi],[Ge("primerMinerala"),p]];for(const[T,y]of w){const A=document.createElement("span");A.className="udzbenik-meta-stavka";const D=document.createElement("strong");D.textContent=`${T}: `;const x=document.createElement("span");x.textContent=y,A.append(D,x),u.append(A)}n.podnozje.append(u);let b=n.smanjenPokret?.72:0;function S(){if(t==="nema"&&!r){o.visible=!1;return}let T=0,y=0;if(b<.3)T=b/.3,y=0;else if(b<.72){T=1;const A=(b-.3)/.42;y=A*A*(3-2*A)}else if(b<.85)T=1,y=1;else{const A=(b-.85)/.15;T=1-A,y=1-A*A*(3-2*A)}o.visible=t!=="nema"&&T>.02,o.scale.setScalar(.25+.75*T),h.opacity=.26*T*(1-.45*y);for(const A of m)A.grupa.position.copy(A.smerRazdvajanja).multiplyScalar(y)}return S(),{azuriraj(T){b=(b+T*.17)%1,a.rotation.y+=T*.24,S()},korak(){b=(b+.18)%1,S()},resetuj(){a.rotation.set(0,0,0),b=n.smanjenPokret?.72:0,S()},osveziTemu(T){c.color.set(T.token("--primary")),l.color.set(T.token("--accent")),d.color.set(T.token("--text-primary")),h.color.set(T.token("--accent")),f.color.set(T.token("--accent"))},raspolazi(){$n(a),c.dispose(),l.dispose(),d.dispose(),h.dispose(),f.dispose()}}}},Sm=new Map([["kubni",zr],["m-3m",zr]]);function Em(n){const e=Sm.get(n);if(!e)throw new Error(`Неподржана група симетрије за хабитус: ${n}`);return e}const ym={imaPodrazumevanuAnimaciju(n){return(n.animacija??"prelaz")!=="nema"},pocetnaKamera(){return{theta:.64,phi:1.12,udaljenost:4.8}},kreiraj(n,e){const t=e.animacija??"prelaz",i=Em(e.sistem),a=e.forme.map((P,U)=>{const z=`forma-${U}`,H=P.naziv||fm(P.hkl),I=i(P.hkl);return{grupaId:z,oznakaForme:H,baznoD:P.d,hkl:P.hkl,ekvivalentne:I}}),s=new ht;n.scena3D.add(s);const o=new It({color:new ve(n.tema.token("--text-primary"))}),c=a.map((P,U)=>new wt({color:new ve(n.tema.token("--primary")),roughness:.32,metalness:.1,flatShading:!0,name:`mat-forma-${U}`}));let l=null,d=null,h="";function f(){const P=new ve(n.tema.token("--primary")),U=new ve(n.tema.token("--accent")),z=new ve(n.tema.token("--bg-elevated"));for(let H=0;H<c.length;H++){const I=c[H],G=a[H].grupaId,q=a.length>1?H/(a.length-1):0,oe=P.clone().lerp(U,q);H%2===1&&a.length>2&&oe.lerp(z,.22),I.color.copy(oe);const le=l===G;I.emissive.copy(le?oe.clone().multiplyScalar(.28):new ve(0,0,0))}o.color.set(n.tema.token("--text-primary"))}f();const m=document.createElement("div");m.className="udzbenik-scena-etiketa udzbenik-scena-etiketa--istaknuta",m.hidden=!0,n.slojEtiketa.append(m);let g=.5,_=n.smanjenPokret?.25:0,p=null;if(a.length>1){const P=document.createElement("label");P.className="udzbenik-klizac-oznaka";const U=document.createElement("span");U.textContent=`${Ge("prelazFormi")}: ${a[0].oznakaForme} ↔ ${a[a.length-1].oznakaForme}`,p=document.createElement("input"),p.type="range",p.min="0",p.max="1",p.step="0.01",p.value="0.5",p.className="udzbenik-klizac",p.addEventListener("input",()=>{g=Number(p.value),v(g),n.zatraziRender()}),P.append(U,p),n.gornjeKontrole.append(P)}const u=document.createElement("div");u.className="udzbenik-habitus-forme";const w=new Map;for(const P of a){const U=document.createElement("button");U.type="button",U.className="udzbenik-mohs-cip",U.textContent=P.oznakaForme;const z=()=>{l=P.grupaId;const H=y?.pljosni.find(I=>I.grupaId===P.grupaId);H?(d=new k(...H.centar),h=`${P.oznakaForme} · ${H.oznaka}`):(d=null,h=P.oznakaForme),f(),D(),n.zatraziRender()};U.addEventListener("click",z),U.addEventListener("focus",z),U.addEventListener("blur",()=>{l===P.grupaId&&(l=null,d=null,f(),D(),n.zatraziRender())}),w.set(P.grupaId,U),u.append(U)}const b=document.createElement("span");b.className="udzbenik-habitus-status",u.append(b),n.podnozje.append(u);let S=null,T=null,y=null,A=[];function D(){if(!y)return;const P=y.pljosni.length,U=y.temena.length,z=e.primer?` · ${Ge("primerMinerala")}: ${e.primer}`:"",H=h&&l?` · ${h}`:"";b.textContent=`${P} пљосни, ${U} темена${z}${H}`;for(const[I,G]of w.entries()){const q=y.pljosni.some(oe=>oe.grupaId===I);G.classList.toggle("udzbenik-mohs-cip--aktivan",l===I),G.classList.toggle("udzbenik-mohs-cip--prigusen",!q)}}function x(P){const U=a.length;return U<=1?a.map(z=>z.baznoD):a.map((z,H)=>{const I=H/(U-1);let G=1;return P<.5?G=1+(.5-P)*2*I*.95:P>.5&&(G=1+(P-.5)*2*(1-I)*.95),z.baznoD*G})}function v(P){S&&(S.geometry.dispose(),s.remove(S)),T&&(T.geometry.dispose(),s.remove(T));const U=x(P),z=[];for(let le=0;le<a.length;le++){const Re=a[le],Y=U[le];for(const te of Re.ekvivalentne)z.push({normala:te.normala,d:Y,grupaId:Re.grupaId,oznaka:te.oznaka})}const H=Fr(z);let I=.001;for(const le of H.temena)I=Math.max(I,Math.hypot(le[0],le[1],le[2]));const G=1.48/I;for(const le of H.temena)le[0]*=G,le[1]*=G,le[2]*=G;for(const le of H.pljosni)le.centar[0]*=G,le.centar[1]*=G,le.centar[2]*=G;const q=kr(H),oe=q.redosledGrupa.map(le=>{const Re=a.findIndex(Y=>Y.grupaId===le);return c[Math.max(0,Re)]});S=new it(q.geometrijaMreze,oe),T=new Bt(q.geometrijaIvica,o),s.add(S,T),y=H,A=q.mapaTrougaoUPljosan,D()}const C=new Fs,F=new Xe,N=P=>{if(!S||!y)return;const U=n.platno.getBoundingClientRect();if(U.width<=0||U.height<=0)return;F.x=(P.clientX-U.left)/U.width*2-1,F.y=-((P.clientY-U.top)/U.height)*2+1,C.setFromCamera(F,n.kamera);const z=C.intersectObject(S,!1);if(z.length>0&&z[0].faceIndex!==void 0&&z[0].faceIndex!==null){const H=A[z[0].faceIndex],I=H!==void 0?y.pljosni[H]:void 0;if(I){const G=a.find(q=>q.grupaId===I.grupaId);l=I.grupaId,d=new k(...I.centar),h=`${G?.oznakaForme??I.grupaId} · ${I.oznaka}`,f(),D(),n.zatraziRender();return}}l!==null&&P.pointerType==="mouse"&&(l=null,d=null,f(),D(),n.zatraziRender())};return n.platno.addEventListener("pointermove",N),v(g),{azuriraj(P){t==="prelaz"&&a.length>1?(_=(_+P*.14)%1,g=.5-.5*Math.cos(_*Math.PI*2),p&&(p.value=g.toFixed(2)),s.rotation.y+=P*.25,v(g)):t==="rotacija"&&(s.rotation.y+=P*.42)},korak(){t==="prelaz"&&a.length>1?(_=(_+.125)%1,g=.5-.5*Math.cos(_*Math.PI*2),p&&(p.value=g.toFixed(2)),v(g)):s.rotation.y+=.35},resetuj(){s.rotation.set(0,0,0),g=.5,_=.25,p&&(p.value="0.5"),l=null,d=null,f(),v(.5)},osveziTemu(){f()},posleRendera(){if(!l||!d){m.hidden=!0;return}s.updateMatrixWorld(!0);const P=d.clone().applyMatrix4(s.matrixWorld),U=n.projektujU2D(P);if(!U.vidljivo){m.hidden=!0;return}m.textContent=h,m.hidden=!1,m.style.transform=`translate(-50%, -120%) translate(${U.x.toFixed(1)}px, ${U.y.toFixed(1)}px)`},raspolazi(){n.platno.removeEventListener("pointermove",N),$n(s),o.dispose();for(const P of c)P.dispose()}}}},ec="Cordero et al., Dalton Trans., 2008, 2832–2838 (DOI: 10.1039/B801115J)",Ss={izvor:"Shannon 1976",vrednosti:{Na:{jon:"Na⁺",poluprecnik:1.02},K:{jon:"K⁺",poluprecnik:1.38},Ca:{jon:"Ca²⁺",poluprecnik:1},Mg:{jon:"Mg²⁺",poluprecnik:.72},Fe:{jon:"Fe²⁺",poluprecnik:.78},Al:{jon:"Al³⁺",poluprecnik:.54},Si:{jon:"Si⁴⁺",poluprecnik:.4},Ti:{jon:"Ti⁴⁺",poluprecnik:.61},Mn:{jon:"Mn²⁺",poluprecnik:.83},Cu:{jon:"Cu²⁺",poluprecnik:.73},Zn:{jon:"Zn²⁺",poluprecnik:.74},Pb:{jon:"Pb²⁺",poluprecnik:1.19},Ba:{jon:"Ba²⁺",poluprecnik:1.35},O:{jon:"O²⁻",poluprecnik:1.4},F:{jon:"F⁻",poluprecnik:1.33},Cl:{jon:"Cl⁻",poluprecnik:1.81},S:{jon:"S²⁻",poluprecnik:1.84}}},Es={H:{simbol:"H",naziv:"Водоник",bojaHex:"#ffffff",kovalentniPoluprecnik:.31},Li:{simbol:"Li",naziv:"Литијум",bojaHex:"#cc80ff",kovalentniPoluprecnik:1.28},Be:{simbol:"Be",naziv:"Берилијум",bojaHex:"#c2ff00",kovalentniPoluprecnik:.96},B:{simbol:"B",naziv:"Бор",bojaHex:"#ffb5b5",kovalentniPoluprecnik:.84},C:{simbol:"C",naziv:"Угљеник",bojaHex:"#505050",kovalentniPoluprecnik:.76},N:{simbol:"N",naziv:"Азот",bojaHex:"#3050f8",kovalentniPoluprecnik:.71},O:{simbol:"O",naziv:"Кисеоник",bojaHex:"#ff0d0d",kovalentniPoluprecnik:.66},F:{simbol:"F",naziv:"Флуор",bojaHex:"#90e050",kovalentniPoluprecnik:.57},Na:{simbol:"Na",naziv:"Натријум",bojaHex:"#ab5cf2",kovalentniPoluprecnik:1.66},Mg:{simbol:"Mg",naziv:"Магнезијум",bojaHex:"#8aff00",kovalentniPoluprecnik:1.41},Al:{simbol:"Al",naziv:"Алуминијум",bojaHex:"#bfa6a6",kovalentniPoluprecnik:1.21},Si:{simbol:"Si",naziv:"Силицијум",bojaHex:"#f0c8a0",kovalentniPoluprecnik:1.11},P:{simbol:"P",naziv:"Фосфор",bojaHex:"#ff8000",kovalentniPoluprecnik:1.07},S:{simbol:"S",naziv:"Сумпор",bojaHex:"#ffff30",kovalentniPoluprecnik:1.05},Cl:{simbol:"Cl",naziv:"Хлор",bojaHex:"#1ff01f",kovalentniPoluprecnik:1.02},K:{simbol:"K",naziv:"Калијум",bojaHex:"#8f40d4",kovalentniPoluprecnik:2.03},Ca:{simbol:"Ca",naziv:"Калцијум",bojaHex:"#3dff00",kovalentniPoluprecnik:1.76},Ti:{simbol:"Ti",naziv:"Титанијум",bojaHex:"#bfc2c7",kovalentniPoluprecnik:1.6},V:{simbol:"V",naziv:"Ванадијум",bojaHex:"#a6a6ab",kovalentniPoluprecnik:1.53},Cr:{simbol:"Cr",naziv:"Хром",bojaHex:"#8a99c7",kovalentniPoluprecnik:1.39},Mn:{simbol:"Mn",naziv:"Манган",bojaHex:"#9c7ac7",kovalentniPoluprecnik:1.39},Fe:{simbol:"Fe",naziv:"Гвожђе",bojaHex:"#e06633",kovalentniPoluprecnik:1.32},Co:{simbol:"Co",naziv:"Кобалт",bojaHex:"#f090a0",kovalentniPoluprecnik:1.26},Ni:{simbol:"Ni",naziv:"Никл",bojaHex:"#50d050",kovalentniPoluprecnik:1.24},Cu:{simbol:"Cu",naziv:"Бакар",bojaHex:"#c88033",kovalentniPoluprecnik:1.32},Zn:{simbol:"Zn",naziv:"Цинк",bojaHex:"#7d80b0",kovalentniPoluprecnik:1.22},As:{simbol:"As",naziv:"Арсен",bojaHex:"#bd80e3",kovalentniPoluprecnik:1.19},Sr:{simbol:"Sr",naziv:"Стронцијум",bojaHex:"#00ff00",kovalentniPoluprecnik:1.95},Zr:{simbol:"Zr",naziv:"Цирконијум",bojaHex:"#94e0e0",kovalentniPoluprecnik:1.75},Mo:{simbol:"Mo",naziv:"Молибден",bojaHex:"#54b5b5",kovalentniPoluprecnik:1.54},Ag:{simbol:"Ag",naziv:"Сребро",bojaHex:"#c0c0c0",kovalentniPoluprecnik:1.45},Sn:{simbol:"Sn",naziv:"Калај",bojaHex:"#668080",kovalentniPoluprecnik:1.39},Sb:{simbol:"Sb",naziv:"Антимон",bojaHex:"#9e63b5",kovalentniPoluprecnik:1.39},Ba:{simbol:"Ba",naziv:"Баријум",bojaHex:"#00c900",kovalentniPoluprecnik:2.15},W:{simbol:"W",naziv:"Волфрам",bojaHex:"#2194d6",kovalentniPoluprecnik:1.62},Pt:{simbol:"Pt",naziv:"Платина",bojaHex:"#d0d0e0",kovalentniPoluprecnik:1.36},Au:{simbol:"Au",naziv:"Злато",bojaHex:"#ffd123",kovalentniPoluprecnik:1.36},Hg:{simbol:"Hg",naziv:"Жива",bojaHex:"#b8b8d0",kovalentniPoluprecnik:1.32},Pb:{simbol:"Pb",naziv:"Олово",bojaHex:"#575961",kovalentniPoluprecnik:1.46},Bi:{simbol:"Bi",naziv:"Бизмут",bojaHex:"#9e4fb5",kovalentniPoluprecnik:1.48}},bm={simbol:"?",naziv:"Непознат елемент",bojaHex:"#ff1493",kovalentniPoluprecnik:1.2};function ks(n){const e=n.trim().replace(/[^A-Za-z]/g,"");if(!e)return"?";const t=e[0].toUpperCase(),i=e.length>1?e[1].toLowerCase():"",r=t+i;return r in Es?r:t in Es?t:r}function ys(n){const e=ks(n);return Es[e]??{...bm,simbol:e}}function tc(n,e="jonski"){const t=ks(n),i=ys(t);if(e==="jonski"){const r=Ss.vrednosti[t];if(r)return{poluprecnik:r.poluprecnik,koriscenaVrsta:"jonski",jon:r.jon}}return{poluprecnik:i.kovalentniPoluprecnik,koriscenaVrsta:"kovalentni"}}class Bn extends Error{constructor(e){super(e),this.name="CifGreska"}}function on(n,e){const t=n.trim().replace(/\([0-9]+\)$/,""),i=Number(t);if(!Number.isFinite(i))throw new Bn(`Неисправна нумеричка вредност у CIF пољу ${e}: "${n}"`);return i}function Mr(n){const e=[];let t=0;const i=n.length;for(;t<i;){for(;t<i&&/\s/.test(n[t]);)t++;if(t>=i)break;const r=n[t];if(r==="#")break;if(r==="'"||r==='"'){const a=r;t++;let s=t;for(;t<i&&!(n[t]===a&&(t+1>=i||/\s/.test(n[t+1])));)t++;e.push(n.slice(s,t)),t<i&&n[t]===a&&t++}else{const a=t;for(;t<i&&!/\s/.test(n[t]);)t++;e.push(n.slice(a,t))}}return e}function Tm(n){if(!n||!n.trim())throw new Bn("CIF садржај је празан.");const e=n.split(/\r?\n/);let t="struktura";const i=new Map,r=[];let a=0;for(;a<e.length;){const m=e[a].trim();if(!m||m.startsWith("#")){a++;continue}if(m.toLowerCase().startsWith("data_")){t=m.slice(5).trim()||t,a++;continue}if(m.toLowerCase()==="loop_"){a++;const g=[];for(;a<e.length;){const T=e[a].trim();if(!T||T.startsWith("#")){a++;continue}if(T.startsWith("_")){const y=Mr(T);y[0]&&g.push(y[0].toLowerCase()),a++}else break}const _=g.indexOf("_atom_site_label"),p=g.indexOf("_atom_site_type_symbol"),u=g.indexOf("_atom_site_fract_x"),w=g.indexOf("_atom_site_fract_y"),b=g.indexOf("_atom_site_fract_z"),S=_!==-1&&p!==-1&&u!==-1&&w!==-1&&b!==-1;for(;a<e.length;){const T=e[a].trim();if(!T||T.startsWith("#")){a++;continue}const y=T.toLowerCase();if(T.startsWith("_")||y==="loop_"||y.startsWith("data_")||T.startsWith(";"))break;if(S&&g.length>0){const A=Mr(T);if(A.length<g.length)throw new Bn("Непотпун ред у _atom_site табели CIF фајла.");const D=A[_],x=A[p],v=on(A[u],"_atom_site_fract_x"),C=on(A[w],"_atom_site_fract_y"),F=on(A[b],"_atom_site_fract_z");r.push({oznaka:D,simbol:ks(x),fx:v,fy:C,fz:F})}a++}continue}if(m.startsWith("_")){const g=Mr(m);if(g.length>=2&&g[0]&&g[1]!==void 0)i.set(g[0].toLowerCase(),g[1]);else if(g.length===1&&g[0]&&a+1<e.length){const _=Mr(e[a+1].trim());_[0]&&!_[0].startsWith("_")&&_[0].toLowerCase()!=="loop_"&&(i.set(g[0].toLowerCase(),_[0]),a++)}}a++}const s=["_cell_length_a","_cell_length_b","_cell_length_c","_cell_angle_alpha","_cell_angle_beta","_cell_angle_gamma"];for(const m of s)if(!i.has(m))throw new Bn(`Недостаје обавезно CIF поље: ${m}`);const o=on(i.get("_cell_length_a"),"_cell_length_a"),c=on(i.get("_cell_length_b"),"_cell_length_b"),l=on(i.get("_cell_length_c"),"_cell_length_c"),d=on(i.get("_cell_angle_alpha"),"_cell_angle_alpha"),h=on(i.get("_cell_angle_beta"),"_cell_angle_beta"),f=on(i.get("_cell_angle_gamma"),"_cell_angle_gamma");if(o<=0||c<=0||l<=0)throw new Bn("Димензије јединичне ћелије a, b, c морају бити позитивне.");if(d<=0||d>=180||h<=0||h>=180||f<=0||f>=180||d+h+f>=360)throw new Bn("Углови јединичне ћелије α, β, γ нису физички валидни.");if(r.length===0)throw new Bn("CIF не садржи ниједан атом у loop_ _atom_site блоку.");return{nazivBloka:t,celija:{a:o,b:c,c:l,alpha:d,beta:h,gamma:f},atomi:r}}function Fc(n){const e=Math.PI/180,t=n.alpha*e,i=n.beta*e,r=n.gamma*e,a=Math.cos(t),s=Math.cos(i),o=Math.cos(r),c=Math.sin(r),l=n.a,d=0,h=n.b*o,f=n.b*c,m=0,g=n.c*s,_=n.c*(a-s*o)/c,p=Math.max(0,n.c*n.c-g*g-_*_),u=Math.sqrt(p);return{va:[l,d,-0],vb:[h,m,-f],vc:[g,u,-_]}}function ki(n,e,t,i){return[n*i.va[0]+e*i.vb[0]+t*i.vc[0],n*i.va[1]+e*i.vb[1]+t*i.vc[1],n*i.va[2]+e*i.vb[2]+t*i.vc[2]]}const Am={imaPodrazumevanuAnimaciju(){return!1},pocetnaKamera(n){return{theta:.65,phi:1.12,udaljenost:(n.prikaz??"celija")==="supercelija"?8.2:6.2}},kreiraj(n,e){const t=e.prikaz??"celija",i=e.stil??"kugle-stapici",r=e.prikazi_celiju??!0,a=e.oznake_atoma??!0,s=e.poluprecnici??"jonski";let o=!1,c=1.15,l=null,d=-1;const h=new ht,f=new ht,m=new ht,g=new ht;h.add(g,m,f),n.scena3D.add(h);const _=new It({color:new ve(n.tema.token("--text-secondary"))}),p=new wt({color:new ve(n.tema.token("--text-muted")),roughness:.45,metalness:.15}),u=new Hr({color:new ve(n.tema.token("--accent")),wireframe:!0}),w=new it(new Nr(1,14,12),u);w.visible=!1,h.add(w);const b=document.createElement("div");b.className="udzbenik-scena-etiketa udzbenik-scena-etiketa--atom",b.hidden=!0,n.slojEtiketa.append(b);const S=document.createElement("div");if(S.className="udzbenik-struktura-kontrole",i==="kugle-stapici"){const H=document.createElement("label");H.className="udzbenik-klizac-oznaka";const I=document.createElement("span");I.textContent=`${Ge("faktorVeza")}: ×1,15`;const G=document.createElement("input");G.type="range",G.min="0.85",G.max="1.40",G.step="0.05",G.value="1.15",G.className="udzbenik-klizac",G.addEventListener("input",()=>{c=Number(G.value),I.textContent=`${Ge("faktorVeza")}: ×${c.toFixed(2).replace(".",",")}`,l&&(N(l),n.zatraziRender())}),H.append(I,G),S.append(H)}const T=document.createElement("span");if(T.className="udzbenik-atom-status",T.setAttribute("aria-live","polite"),a){const H=document.createElement("button");H.type="button",H.className="udzbenik-dugme udzbenik-dugme--malo",H.textContent=Ge("sledeciAtom"),H.addEventListener("click",()=>{y.length!==0&&(d=(d+1)%y.length,v(d),n.zatraziRender())}),S.append(H,T)}S.childNodes.length>0&&n.gornjeKontrole.append(S);let y=[],A=null,D=new k,x=1;function v(H){if(H<0||H>=y.length){A=null,w.visible=!1,b.hidden=!0,T.textContent="";return}const I=y[H];A=I.atom;const G=I.mesh.scale.x*1.25;w.position.copy(I.mesh.position),w.scale.setScalar(G),w.visible=!0;const q=`(${I.atom.fx.toFixed(3)}, ${I.atom.fy.toFixed(3)}, ${I.atom.fz.toFixed(3)})`;b.textContent=`${I.atom.simbol} [${I.atom.oznaka}] ${q}`,T.textContent=`${I.atom.simbol} (${I.atom.oznaka}): ${q}`}function C(H){$n(H),H.clear()}function F(H){n.podnozje.replaceChildren();const I=document.createElement("div");I.className="udzbenik-cpk-legenda",I.setAttribute("aria-label",Ge("legendaElemenata"));const G=document.createElement("div");G.className="udzbenik-cpk-stavke";let q=!1;for(const Re of H){const Y=ys(Re),te=tc(Re,s);s==="jonski"&&te.koriscenaVrsta==="kovalentni"&&(q=!0);const de=document.createElement("span");de.className="udzbenik-cpk-cip";const se=document.createElement("span");se.className="udzbenik-cpk-boja",se.style.backgroundColor=Y.bojaHex,se.setAttribute("aria-hidden","true");const Q=te.koriscenaVrsta==="jonski"&&te.jon?`${Y.simbol} (${te.jon})`:Y.simbol,ge=te.poluprecnik.toFixed(2).replace(".",","),ue=document.createElement("span");ue.textContent=`${Q} — ${Y.naziv} (r = ${ge} Å)`,de.append(se,ue),G.append(de)}const oe=document.createElement("p");oe.className="udzbenik-scena-izvor";const le=i==="kugle-stapici"?` · ${Ge("detekcijaVezaKovalentniOznaka")}${c.toFixed(2).replace(".",",")}`:"";if(s==="jonski"){const Re=q?`${Ss.izvor}; ${Ge("kovalentnaRezervaOznaka")}: ${ec}`:Ss.izvor;oe.textContent=`${Ge("poluprecniciJonskiOznaka")} (${Ge("izvorPodataka")}: ${Re})${le}`}else oe.textContent=`${Ge("poluprecniciKovalentniOznaka")} (${Ge("izvorPodataka")}: ${ec})${le}`;I.append(G,oe),n.podnozje.append(I)}function N(H){C(f),C(m),C(g),y=[];const I=Fc(H.celija),G=t==="supercelija"?2:1,q=ki(G,G,G,I);D=new k(q[0]*.5,q[1]*.5,q[2]*.5);const oe=Math.max(H.celija.a*G,H.celija.b*G,H.celija.c*G);x=3.6/Math.max(1,oe);const le=[],Re=new Set,Y=[];for(const Q of H.atomi){Y.includes(Q.simbol)||Y.push(Q.simbol);const ge=ys(Q.simbol),ue=tc(Q.simbol,s),K=(Q.fx%1+1)%1,ie=(Q.fy%1+1)%1,ae=(Q.fz%1+1)%1,L=K<.001?[0,1]:[0],Ie=ie<.001?[0,1]:[0],Pe=ae<.001?[0,1]:[0];for(let Ce=0;Ce<G;Ce++)for(let Me=0;Me<G;Me++)for(let ke=0;ke<G;ke++)for(const we of L)for(const R of Ie)for(const M of Pe){const j=K+Ce+we,J=ie+Me+R,ne=ae+ke+M;if(j>G+.001||J>G+.001||ne>G+.001)continue;const Z=`${j.toFixed(3)},${J.toFixed(3)},${ne.toFixed(3)},${Q.simbol}`;if(Re.has(Z))continue;Re.add(Z);const Ae=ki(j,J,ne,I);le.push({oznaka:Q.oznaka,simbol:Q.simbol,fx:j,fy:J,fz:ne,pozicija:new k(Ae[0],Ae[1],Ae[2]),poluprecnikPrikaza:ue.poluprecnik,kovalentniPoluprecnik:ge.kovalentniPoluprecnik,bojaHex:ge.bojaHex})}}const te=new Nr(1,20,16),de=new Map,se=i==="kugle"?.52:.25;for(const Q of le){let ge=de.get(Q.simbol);ge||(ge=new wt({color:new ve(Q.bojaHex),roughness:.32,metalness:.1}),de.set(Q.simbol,ge));const ue=new it(te,ge);ue.position.copy(Q.pozicija).sub(D).multiplyScalar(x);const K=Math.max(.045,Q.poluprecnikPrikaza*se*x);ue.scale.setScalar(K),f.add(ue),y.push({mesh:ue,atom:Q})}if(i==="kugle-stapici"){const Q=new ji(1,1,1,10,1),ge=new k(0,1,0),ue=Math.max(.035,.09*x);for(let K=0;K<le.length;K++){const ie=le[K];for(let ae=K+1;ae<le.length;ae++){const L=le[ae],Ie=ie.pozicija.distanceTo(L.pozicija),Pe=(ie.kovalentniPoluprecnik+L.kovalentniPoluprecnik)*c;if(Ie>.35&&Ie<=Pe){const Ce=y[K].mesh.position,ke=y[ae].mesh.position.clone().sub(Ce),we=ke.length();if(we<1e-4)continue;const R=new it(Q,p.clone());R.position.copy(Ce).addScaledVector(ke,.5),R.quaternion.setFromUnitVectors(ge,ke.clone().normalize()),R.scale.set(ue,we,ue),m.add(R)}}}Q.dispose()}if(r){const Q=[],ge=[[[0,0,0],[1,0,0]],[[1,0,0],[1,1,0]],[[1,1,0],[0,1,0]],[[0,1,0],[0,0,0]],[[0,0,1],[1,0,1]],[[1,0,1],[1,1,1]],[[1,1,1],[0,1,1]],[[0,1,1],[0,0,1]],[[0,0,0],[0,0,1]],[[1,0,0],[1,0,1]],[[1,1,0],[1,1,1]],[[0,1,0],[0,1,1]]];for(let K=0;K<G;K++)for(let ie=0;ie<G;ie++)for(let ae=0;ae<G;ae++)for(const[L,Ie]of ge){const Pe=ki(L[0]+K,L[1]+ie,L[2]+ae,I),Ce=ki(Ie[0]+K,Ie[1]+ie,Ie[2]+ae,I),Me=new k(...Pe).sub(D).multiplyScalar(x),ke=new k(...Ce).sub(D).multiplyScalar(x);Q.push(Me.x,Me.y,Me.z,ke.x,ke.y,ke.z)}const ue=new st;ue.setAttribute("position",new nt(Q,3)),g.add(new Bt(ue,_.clone()))}F(Y),d=-1,v(-1)}const P=new Fs,U=new Xe,z=H=>{if(!a||y.length===0)return;const I=n.platno.getBoundingClientRect();if(I.width<=0||I.height<=0)return;U.x=(H.clientX-I.left)/I.width*2-1,U.y=-((H.clientY-I.top)/I.height)*2+1,P.setFromCamera(U,n.kamera);const G=P.intersectObjects(y.map(q=>q.mesh),!1);if(G.length>0){const q=G[0].object,oe=y.findIndex(le=>le.mesh===q);oe!==d&&(d=oe,v(oe),n.zatraziRender())}else d!==-1&&H.pointerType==="mouse"&&(d=-1,v(-1),n.zatraziRender())};return a&&n.platno.addEventListener("pointermove",z),n.api.ucitajStrukturuCif(e.mineral).then(H=>{o||(l=Tm(H),N(l),n.zatraziRender())}).catch(H=>{if(o)return;const I=(H instanceof Et&&H.status===404,Ge("strukturaNedostupna"));n.prikaziRezervu(I)}),{resetuj(){d=-1,v(-1)},osveziTemu(H){_.color.set(H.token("--text-secondary")),p.color.set(H.token("--text-muted")),u.color.set(H.token("--accent"));for(const I of g.children){const G=I;G.material instanceof It&&G.material.color.set(H.token("--text-secondary"))}for(const I of m.children){const G=I;G.material instanceof wt&&G.material.color.set(H.token("--text-muted"))}},posleRendera(){if(!A||d<0){b.hidden=!0;return}const H=y[d];if(!H)return;H.mesh.updateMatrixWorld(!0);const I=H.mesh.position.clone().applyMatrix4(h.matrixWorld),G=n.projektujU2D(I);if(!G.vidljivo){b.hidden=!0;return}b.hidden=!1,b.style.transform=`translate(-50%, -130%) translate(${G.x.toFixed(1)}px, ${G.y.toFixed(1)}px)`},raspolazi(){o=!0,a&&n.platno.removeEventListener("pointermove",z),$n(h),_.dispose(),p.dispose(),u.dispose()}}}},wa=[{kljuc:"kubni",naziv:"Кубни",kratko:"Кубни",odnosIvica:"a = b = c",odnosUglova:"α = β = γ = 90°",reprezentativniOblik:"коцка",celija:{a:1.15,b:1.15,c:1.15,alpha:90,beta:90,gamma:90}},{kljuc:"tetragonalni",naziv:"Тетрагонални",kratko:"Тетраг.",odnosIvica:"a = b ≠ c",odnosUglova:"α = β = γ = 90°",reprezentativniOblik:"тетрагонална призма",celija:{a:1,b:1,c:1.62,alpha:90,beta:90,gamma:90}},{kljuc:"ortorombicni",naziv:"Орторомбични",kratko:"Орторомб.",odnosIvica:"a ≠ b ≠ c",odnosUglova:"α = β = γ = 90°",reprezentativniOblik:"правоугаона призма („цигла“)",celija:{a:.85,b:1.22,c:1.58,alpha:90,beta:90,gamma:90}},{kljuc:"heksagonalni",naziv:"Хексагонални",kratko:"Хексаг.",odnosIvica:"a = b ≠ c",odnosUglova:"α = β = 90°, γ = 120°",reprezentativniOblik:"хексагонална призма",celija:{a:1.08,b:1.08,c:1.55,alpha:90,beta:90,gamma:120}},{kljuc:"trigonalni",naziv:"Тригонални",kratko:"Тригон.",odnosIvica:"a = b = c",odnosUglova:"α = β = γ ≠ 90°",reprezentativniOblik:"ромбоедар",celija:{a:1.18,b:1.18,c:1.18,alpha:75,beta:75,gamma:75}},{kljuc:"monoklinicni",naziv:"Моноклинични",kratko:"Монокл.",odnosIvica:"a ≠ b ≠ c",odnosUglova:"α = γ = 90°, β ≠ 90°",reprezentativniOblik:"кос паралелопипед (β ≠ 90°)",celija:{a:.92,b:1.22,c:1.48,alpha:90,beta:112,gamma:90}},{kljuc:"triklinicni",naziv:"Триклинични",kratko:"Трикл.",odnosIvica:"a ≠ b ≠ c",odnosUglova:"α ≠ β ≠ γ ≠ 90°",reprezentativniOblik:"кос паралелопипед (α, β, γ ≠ 90°)",celija:{a:.88,b:1.18,c:1.46,alpha:78,beta:109,gamma:103}}],wm={a:1.15,b:1.15,c:1.15,alpha:90,beta:90,gamma:90};function Rm(n,e,t){const i=Math.max(0,Math.min(1,t));return{a:n.a+(e.a-n.a)*i,b:n.b+(e.b-n.b)*i,c:n.c+(e.c-n.c)*i,alpha:n.alpha+(e.alpha-n.alpha)*i,beta:n.beta+(e.beta-n.beta)*i,gamma:n.gamma+(e.gamma-n.gamma)*i}}function zc(n){const e=Fc(n),t=new k(...e.va),i=new k(...e.vb),r=new k(...e.vc),a=t.clone().add(i).add(r).multiplyScalar(.5),s=[],o=[[0,0,0],[1,0,0],[1,1,0],[0,1,0],[0,0,1],[1,0,1],[1,1,1],[0,1,1]];for(const[g,_,p]of o){const u=ki(g,_,p,e);s.push(new k(u[0]-a.x,u[1]-a.y,u[2]-a.z))}const c=[[0,1],[1,2],[2,3],[3,0],[4,5],[5,6],[6,7],[7,4],[0,4],[1,5],[2,6],[3,7]],l=[];for(const[g,_]of c){const p=s[g],u=s[_];l.push(p.x,p.y,p.z,u.x,u.y,u.z)}const d=new st;d.setAttribute("position",new nt(l,3));const h=[[0,3,2,1],[4,5,6,7],[0,1,5,4],[2,3,7,6],[1,2,6,5],[3,0,4,7]],f=[];for(const[g,_,p,u]of h){const w=s[g],b=s[_],S=s[p],T=s[u];f.push(w.x,w.y,w.z,b.x,b.y,b.z,S.x,S.y,S.z,w.x,w.y,w.z,S.x,S.y,S.z,T.x,T.y,T.z)}const m=new st;return m.setAttribute("position",new nt(f,3)),m.computeVertexNormals(),{ivice:d,mreza:m,poreklo:s[0],va:t,vb:i,vc:r}}function Ra(n,e,t,i){const r=e.clone().normalize(),a=t.clone().normalize(),s=18,o=[];let c=n.clone();for(let d=0;d<=s;d++){const h=d/s,f=r.clone().multiplyScalar(1-h).addScaledVector(a,h).normalize(),m=n.clone().addScaledVector(f,i);if(d===Math.floor(s/2)&&(c=n.clone().addScaledVector(f,i*1.38)),d>0){const g=(d-1)/s,_=r.clone().multiplyScalar(1-g).addScaledVector(a,g).normalize(),p=n.clone().addScaledVector(_,i);o.push(p.x,p.y,p.z,m.x,m.y,m.z)}}const l=new st;return l.setAttribute("position",new nt(o,3)),{geometrija:l,sredina:c}}function Cm(n,e,t){if(n==="heksagonalni"){const s=.58+.22*t,o=1.35-(1.35-.68)*t,c=[{normala:[0,1,0],d:s},{normala:[0,-1,0],d:s},{normala:[1,0,0],d:.68},{normala:[-1,0,0],d:.68},{normala:[0,0,1],d:.68+.14*t},{normala:[0,0,-1],d:.68+.14*t},{normala:[.5,0,Math.sqrt(3)/2],d:o},{normala:[-.5,0,Math.sqrt(3)/2],d:o},{normala:[.5,0,-Math.sqrt(3)/2],d:o},{normala:[-.5,0,-Math.sqrt(3)/2],d:o}],l=[{normala:[0,1,0],d:s},{normala:[0,-1,0],d:s}];if(t>.85){for(let g=0;g<6;g++){const _=g*Math.PI/3;l.push({normala:[Math.cos(_),0,Math.sin(_)],d:.68})}const f=Fr(l),m=kr(f);return{mreza:m.geometrijaMreze,ivice:m.geometrijaIvica}}const d=Fr(c),h=kr(d);return{mreza:h.geometrijaMreze,ivice:h.geometrijaIvica}}const i={a:e.a*.92,b:e.b*.92,c:e.c*.92,alpha:e.alpha,beta:e.beta,gamma:e.gamma},r=zc(i);return{mreza:r.mreza,ivice:r.ivice}}const Pm={imaPodrazumevanuAnimaciju(n){return(n.animacija??"rotacija")!=="nema"},pocetnaKamera(){return{theta:.42,phi:1.15,udaljenost:6.8}},kreiraj(n,e){const t=e.animacija??"rotacija",i=e.prikazi_ose??!0,r=e.prikazi_celiju??!0;let a=e.sistem==="svi"?"heksagonalni":e.sistem;e.sistem==="svi"&&(a="kubni");let s=n.smanjenPokret||t!=="uporedi"?1:0,o=0;const c=new ht,l=new ht,d=new ht;r?(l.position.set(-1.55,-.05,0),d.position.set(1.55,-.05,0)):d.position.set(0,-.05,0),c.add(l,d),n.scena3D.add(c);const h=new wt({color:new ve(n.tema.token("--primary")),transparent:!0,opacity:.14,roughness:.45,metalness:.05,side:kt,depthWrite:!1}),f=new It({color:new ve(n.tema.token("--text-secondary"))}),m=new It({color:new ve(n.tema.token("--danger"))}),g=new It({color:new ve(n.tema.token("--success"))}),_=new It({color:new ve(n.tema.token("--accent"))}),p=new It({color:new ve(n.tema.token("--warning"))}),u=new wt({color:new ve(n.tema.token("--primary")),transparent:!0,opacity:.78,roughness:.35,metalness:.08,flatShading:!0}),w=new It({color:new ve(n.tema.token("--text-primary"))}),b=["a","b","c","α","β","γ"],S=new Map,T=new Map;if(i&&r)for(const P of b){const U=document.createElement("span");U.className="udzbenik-scena-etiketa",U.textContent=P,n.slojEtiketa.append(U),S.set(P,U),T.set(P,new k)}const y=document.createElement("div");y.className="udzbenik-scena-info-red",n.podnozje.append(y);const A=new Map;if(e.sistem==="svi"){const P=document.createElement("div");P.className="udzbenik-sistemi-traka",P.setAttribute("role","group"),P.setAttribute("aria-label",Ge("izaberiKristalniSistem"));for(const U of wa){const z=document.createElement("button");z.type="button",z.className="udzbenik-sistem-kartica",z.dataset.sistem=U.kljuc,z.setAttribute("aria-pressed",String(U.kljuc===a));const H=document.createElement("span");H.className="udzbenik-sistem-kartica-naslov",H.textContent=U.naziv;const I=document.createElement("span");I.className="udzbenik-sistem-kartica-meta",I.textContent=`${U.odnosIvica} · ${U.odnosUglova}`,z.append(H,I),z.addEventListener("click",()=>{a=U.kljuc,s=n.smanjenPokret||t!=="uporedi"?1:0,D(),F(),n.zatraziRender()}),A.set(U.kljuc,z),P.append(z)}n.gornjeKontrole.append(P)}function D(){for(const[P,U]of A.entries()){const z=P===a;U.classList.toggle("udzbenik-sistem-kartica--aktivna",z),U.setAttribute("aria-pressed",String(z))}}function x(){return wa.find(P=>P.kljuc===a)??wa[0]}function v(P){for(const U of P.children){const z=U.geometry;z&&z.dispose()}P.clear()}function C(){if(t!=="uporedi"||a==="kubni")return 1;const P=s%1;if(P<.4){const U=P/.4;return U*U*(3-2*U)}if(P<.72)return 1;if(P<.92){const U=(P-.72)/.2;return 1-U*U*(3-2*U)}return 0}function F(){const P=x(),U=C(),z=Rm(wm,P.celija,U);if(v(l),v(d),r){const q=zc(z),oe=new it(q.mreza,h),le=new Bt(q.ivice,f);if(l.add(oe,le),i){const Re=q.poreklo,Y=Re.clone().addScaledVector(q.va,1.16),te=Re.clone().addScaledVector(q.vb,1.16),de=Re.clone().addScaledVector(q.vc,1.16),se=new st().setFromPoints([Re,Y]),Q=new st().setFromPoints([Re,te]),ge=new st().setFromPoints([Re,de]);l.add(new wr(se,m),new wr(Q,g),new wr(ge,_));const ue=Ra(Re,q.vb,q.vc,.36),K=Ra(Re,q.va,q.vc,.44),ie=Ra(Re,q.va,q.vb,.36);l.add(new Bt(ue.geometrija,p),new Bt(K.geometrija,p),new Bt(ie.geometrija,p)),T.get("a")?.copy(Y),T.get("b")?.copy(te),T.get("c")?.copy(de),T.get("α")?.copy(ue.sredina),T.get("β")?.copy(K.sredina),T.get("γ")?.copy(ie.sredina)}}const H=Cm(P.kljuc,z,U);d.add(new it(H.mreza,u),new Bt(H.ivice,w)),y.replaceChildren();const I=document.createElement("strong");I.textContent=`${P.naziv}: `;const G=document.createElement("span");G.textContent=`${P.odnosIvica} · ${P.odnosUglova} — облик: ${P.reprezentativniOblik}`,y.append(I,G)}function N(){if(!i||!r)return;l.updateMatrixWorld(!0);const P=x();for(const[U,z]of S.entries()){const H=T.get(U);if(!H)continue;const I=H.clone().applyMatrix4(l.matrixWorld),G=n.projektujU2D(I);if(!G.vidljivo){z.hidden=!0;continue}z.hidden=!1,z.style.transform=`translate(-50%, -50%) translate(${G.x.toFixed(1)}px, ${G.y.toFixed(1)}px)`;const q=U==="c"&&P.celija.c!==P.celija.a||U==="b"&&P.celija.b!==P.celija.a||U==="α"&&P.celija.alpha!==90||U==="β"&&P.celija.beta!==90||U==="γ"&&P.celija.gamma!==90;z.classList.toggle("udzbenik-scena-etiketa--istaknuta",q)}}return D(),F(),{azuriraj(P){t==="uporedi"?(s=(s+P*.18)%1,o+=P*.22,c.rotation.y=Math.sin(o)*.18,F()):t==="rotacija"&&(c.rotation.y+=P*.45)},korak(){t==="uporedi"?(s=(s+.15)%1,o+=.45,c.rotation.y=Math.sin(o)*.18,F()):c.rotation.y+=.35},resetuj(){c.rotation.set(0,0,0),o=0,s=n.smanjenPokret||t!=="uporedi"?1:0,F()},osveziTemu(P){h.color.set(P.token("--primary")),f.color.set(P.token("--text-secondary")),m.color.set(P.token("--danger")),g.color.set(P.token("--success")),_.color.set(P.token("--accent")),p.color.set(P.token("--warning")),u.color.set(P.token("--primary")),w.color.set(P.token("--text-primary"))},posleRendera(){N()},raspolazi(){$n(c),h.dispose(),f.dispose(),m.dispose(),g.dispose(),_.dispose(),p.dispose(),u.dispose(),w.dispose()}}}},Xt="Klein, C. & Dutrow, B. (2007), Manual of Mineral Science (23rd ed.), John Wiley & Sons, Table 2.3 (Knoop microhardness HK, kgf/mm²).",En=[{mohs:1,kljuc:"talk",naziv:"Талк",formula:"Mg₃Si₄O₁₀(OH)₂",apsolutnaKnoop:1,izvor:Xt},{mohs:2,kljuc:"gips",naziv:"Гипс",formula:"CaSO₄·2H₂O",apsolutnaKnoop:32,izvor:Xt},{mohs:3,kljuc:"kalcit",naziv:"Калцит",formula:"CaCO₃",apsolutnaKnoop:135,izvor:Xt},{mohs:4,kljuc:"fluorit",naziv:"Флуорит",formula:"CaF₂",apsolutnaKnoop:163,izvor:Xt},{mohs:5,kljuc:"apatit",naziv:"Апатит",formula:"Ca₅(PO₄)₃(F,Cl,OH)",apsolutnaKnoop:430,izvor:Xt},{mohs:6,kljuc:"ortoklas",naziv:"Ортоклас",formula:"KAlSi₃O₈",apsolutnaKnoop:560,izvor:Xt},{mohs:7,kljuc:"kvarc",naziv:"Кварц",formula:"SiO₂",apsolutnaKnoop:820,izvor:Xt},{mohs:8,kljuc:"topaz",naziv:"Топаз",formula:"Al₂SiO₄(F,OH)₂",apsolutnaKnoop:1340,izvor:Xt},{mohs:9,kljuc:"korund",naziv:"Корунд",formula:"Al₂O₃",apsolutnaKnoop:2100,izvor:Xt},{mohs:10,kljuc:"dijamant",naziv:"Дијамант",formula:"C",apsolutnaKnoop:7e3,izvor:Xt}],Dm=[{naziv:"Нокат (~2,5)",mohs:2.5},{naziv:"Бакар (~3,5)",mohs:3.5},{naziv:"Нож / стакло (~5,5)",mohs:5.5},{naziv:"Челична турпија (~6,5)",mohs:6.5}];function nc(n,e){if(!e||e.length===0)return!1;const t=n.kljuc.toLowerCase(),i=n.naziv.toLowerCase();return e.some(r=>{const a=r.trim().toLowerCase();return a===t||a===i})}const Lm={imaPodrazumevanuAnimaciju(){return!0},pocetnaKamera(){return{theta:.16,phi:1.18,udaljenost:8.6}},kreiraj(n,e){const t=e.prikazi_apsolutnu??!1,i=e.prikazi_terenske_probe??!0,r=e.istaknuti??[];let a=!1,s=0,o=6,c=5,l=n.smanjenPokret?.65:0;const d=new ht;d.position.set(0,-.35,0),n.scena3D.add(d);const h=-4.05,f=.9,m=-.7,g=2.75,_=new wt({color:new ve(n.tema.token("--bg-elevated")),roughness:.7,metalness:.05}),p=new it(new hn(9.6,.14,1.4),_);p.position.set(0,m-.07,-.35),d.add(p);const u=[],w=new It({color:new ve(n.tema.token("--text-primary"))}),b=new hn(.66,1,.66),S=new ms(b);for(let K=0;K<En.length;K++){const ie=En[K],ae=nc(ie,r),L=new ve(n.tema.token(ae?"--accent":"--primary")),Ie=new wt({color:L,emissive:ae?new ve(n.tema.token("--accent")).multiplyScalar(.22):new ve(0,0,0),roughness:.35,metalness:.12}),Pe=new it(b,Ie),Ce=new Bt(S,w),Me=h+K*f;Pe.position.set(Me,m+.5,-.35),Ce.position.copy(Pe.position),d.add(Pe,Ce);const ke=document.createElement("span");ke.className="udzbenik-scena-etiketa udzbenik-scena-etiketa--mala",ae&&ke.classList.add("udzbenik-scena-etiketa--istaknuta"),ke.textContent=`${ie.mohs}`,n.slojEtiketa.append(ke),u.push({mineral:ie,istaknut:ae,mesh:Pe,ivice:Ce,mat:Ie,etiketaDom:ke})}const T=new wt({color:new ve(n.tema.token("--warning")),roughness:.4}),y=[];if(i){const K=new ji(.035,.035,.65,8);for(const ie of Dm){const ae=h+(ie.mohs-1)*f,L=new it(K,T);L.position.set(ae,m+.32,.18),d.add(L);const Ie=document.createElement("span");Ie.className="udzbenik-scena-etiketa udzbenik-scena-etiketa--proba",Ie.textContent=ie.naziv,n.slojEtiketa.append(Ie),y.push({x:ae,tekst:ie.naziv,dom:Ie,stub:L})}}const A=new ht;A.position.set(0,m-.52,1.35),d.add(A);const D=new wt({color:new ve(n.tema.token("--primary-light")),roughness:.45,metalness:.08}),x=new it(new hn(3.4,.24,.92),D),v=new Bt(new ms(x.geometry),w);A.add(x,v);const C=new wt({color:new ve(n.tema.token("--danger")),roughness:.85}),F=new it(new hn(1,.05,.11),C);F.position.set(-1.1,.125,0),F.visible=!1,A.add(F);const N=new wt({color:new ve(n.tema.token("--accent")),roughness:.25,metalness:.2}),P=new it(new Ns(.22,.72,6),N);P.rotation.x=Math.PI,P.rotation.z=-.22,P.position.set(-1.1,.5,0),A.add(P);const U=document.createElement("div");U.className="udzbenik-mohs-kontrole";const z=document.createElement("div");z.className="udzbenik-mohs-dugmad",z.setAttribute("role","group"),z.setAttribute("aria-label",Ge("ordinalnaTvrdocaOznaka"));const H=[];for(let K=0;K<En.length;K++){const ie=En[K],ae=document.createElement("button");ae.type="button",ae.className="udzbenik-mohs-cip",nc(ie,r)&&ae.classList.add("udzbenik-mohs-cip--istaknut"),ae.textContent=`${ie.mohs}. ${ie.naziv}`,ae.addEventListener("click",()=>{Re(K)}),H.push(ae),z.append(ae)}U.append(z);const I=document.createElement("div");I.className="udzbenik-mohs-akcije";const G=document.createElement("button");G.type="button",G.className="udzbenik-dugme udzbenik-dugme--malo",G.textContent=Ge("zameniMinerale"),G.addEventListener("click",()=>{const K=o;o=c,c=K,l=n.smanjenPokret?.75:0,se(),n.zatraziRender()}),I.append(G);let q=null;t&&(q=document.createElement("button"),q.type="button",q.className="udzbenik-dugme udzbenik-dugme--malo udzbenik-dugme--preklopnik",q.setAttribute("role","switch"),q.setAttribute("aria-checked","false"),q.textContent=Ge("apsolutnaTvrdocaPreklopnik"),q.addEventListener("click",()=>{a=!a,q?.setAttribute("aria-checked",String(a)),q?.classList.toggle("udzbenik-dugme--aktivno",a),n.smanjenPokret&&(s=a?1:0,te()),se(),n.zatraziRender()}),I.append(q)),U.append(I),n.gornjeKontrole.append(U);const oe=document.createElement("p");oe.className="udzbenik-scena-info-red",oe.setAttribute("aria-live","polite");const le=document.createElement("p");le.className="udzbenik-scena-izvor",le.textContent=`${Ge("izvorPodataka")}: ${Xt}`,n.podnozje.append(oe,le);function Re(K){K===o?c=K<9?K+1:K-1:(o=K,c=K>0?K-1:1),l=n.smanjenPokret?.75:0,se(),n.zatraziRender()}function Y(K,ie){const ae=K.mohs/10*g,L=Math.max(.08,K.apsolutnaKnoop/7e3*g);return ae+(L-ae)*ie}function te(){for(let K=0;K<u.length;K++){const ie=u[K],ae=Y(ie.mineral,s);ie.mesh.scale.y=ae,ie.mesh.position.y=m+ae*.5,ie.ivice.scale.y=ae,ie.ivice.position.copy(ie.mesh.position);const L=K===o,Ie=K===c,Pe=L?"--accent":Ie?"--warning":ie.istaknut?"--accent":"--primary",Ce=new ve(n.tema.token(Pe));!L&&!Ie&&!ie.istaknut&&Ce.lerp(new ve(n.tema.token("--bg-elevated")),.25),ie.mat.color.copy(Ce),ie.etiketaDom.textContent=a?`${ie.mineral.mohs} (${ie.mineral.apsolutnaKnoop})`:`${ie.mineral.mohs}`}}function de(){const K=En[o],ie=En[c],ae=K.mohs>ie.mohs,L=Math.min(1,l/.75),Ie=-1.15,Ce=Ie+(1.15-Ie)*L;if(P.position.x=Ce,P.position.y=ae?.44:.5,ae&&L>.03){const Me=Math.max(.05,Ce-Ie);F.visible=!0,F.scale.x=Me,F.position.x=Ie+Me*.5}else F.visible=!1}function se(){for(let Ie=0;Ie<H.length;Ie++){const Pe=H[Ie],Ce=Ie===o;Pe.classList.toggle("udzbenik-mohs-cip--aktivan",Ce),Pe.setAttribute("aria-pressed",String(Ce))}const K=En[o],ie=En[c],L=K.mohs>ie.mohs?`${Ge("probaGrebanja")}: ${K.naziv} (${K.mohs}, HK ${K.apsolutnaKnoop}) је тврђи и оставља бразду на минералу ${ie.naziv} (${ie.mohs}, HK ${ie.apsolutnaKnoop}).`:`${Ge("probaGrebanja")}: ${K.naziv} (${K.mohs}, HK ${K.apsolutnaKnoop}) је мекши и НЕ оставља бразду на минералу ${ie.naziv} (${ie.mohs}, HK ${ie.apsolutnaKnoop}).`;oe.textContent=L,te(),de()}const Q=new Fs,ge=new Xe,ue=K=>{const ie=n.platno.getBoundingClientRect();if(ie.width<=0||ie.height<=0)return;ge.x=(K.clientX-ie.left)/ie.width*2-1,ge.y=-((K.clientY-ie.top)/ie.height)*2+1,Q.setFromCamera(ge,n.kamera);const ae=Q.intersectObjects(u.map(L=>L.mesh),!1);if(ae.length>0){const L=ae[0].object,Ie=u.findIndex(Pe=>Pe.mesh===L);Ie!==-1&&Re(Ie)}};return n.platno.addEventListener("click",ue),se(),{azuriraj(K){const ie=a?1:0;Math.abs(s-ie)>.002?(s+=(ie-s)*Math.min(1,K*6),te()):s!==ie&&(s=ie,te()),l=(l+K*.42)%1,de()},korak(){l=(l+.2)%1,s=a?1:0,te(),de()},resetuj(){a=!1,s=0,q&&(q.setAttribute("aria-checked","false"),q.classList.remove("udzbenik-dugme--aktivno")),o=6,c=5,l=n.smanjenPokret?.75:0,se()},osveziTemu(K){_.color.set(K.token("--bg-elevated")),w.color.set(K.token("--text-primary")),T.color.set(K.token("--warning")),D.color.set(K.token("--primary-light")),C.color.set(K.token("--danger")),N.color.set(K.token("--accent")),te()},posleRendera(){d.updateMatrixWorld(!0);for(const K of u){const ie=K.mesh.position.clone().add(new k(0,K.mesh.scale.y*.5+.22,0)).applyMatrix4(d.matrixWorld),ae=n.projektujU2D(ie);K.etiketaDom.hidden=!ae.vidljivo,ae.vidljivo&&(K.etiketaDom.style.transform=`translate(-50%, -50%) translate(${ae.x.toFixed(1)}px, ${ae.y.toFixed(1)}px)`)}for(const K of y){const ie=new k(K.x,m-.22,.35).applyMatrix4(d.matrixWorld),ae=n.projektujU2D(ie);K.dom.hidden=!ae.vidljivo,ae.vidljivo&&(K.dom.style.transform=`translate(-50%, 0%) translate(${ae.x.toFixed(1)}px, ${ae.y.toFixed(1)}px)`)}},raspolazi(){n.platno.removeEventListener("click",ue),$n(d),b.dispose(),S.dispose(),_.dispose(),w.dispose(),T.dispose(),D.dispose(),C.dispose(),N.dispose();for(const K of u)K.mat.dispose()}}}},Im={"kristalni-sistem":Pm,"kristalna-struktura":Am,"mohsova-skala":Lm,cepljivost:Mm,habitus:ym};function Um(n,e,t){const i=Im[n.scena];if(!i)throw new Error(`Непознат тип сцене: ${String(n.scena)}`);return _m(i,n.parametri,e,t)}const km=Object.freeze(Object.defineProperty({__proto__:null,pokreniScenuPoImenu:Um,raspolaziDeljenimRendererom:gm},Symbol.toStringTag,{value:"Module"}));export{Et as A,Xr as a,Nm as b,zm as c,km as d,Fm as p,Ge as t};
