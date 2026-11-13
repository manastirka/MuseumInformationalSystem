import{t as ai,n as _l,a as ot,g as ro,b as Is,d as Pc,f as vl,A as xl,p as ao,c as so,J as oo,I as co}from"./udzbenik-jezgro-C6N5lslw.js";/**
 * @license
 * Copyright 2010-2025 Three.js Authors
 * SPDX-License-Identifier: MIT
 */const Us="174",Ml=0,lo=1,Sl=2,Dc=1,El=2,un=3,Pn=0,Ct=1,St=2,Rn=0,wi=1,uo=2,ho=3,fo=4,yl=5,Xn=100,bl=101,Tl=102,wl=103,Al=104,Rl=200,Cl=201,Pl=202,Dl=203,Oa=204,Ba=205,Ll=206,Il=207,Ul=208,zl=209,Nl=210,kl=211,Fl=212,Ol=213,Bl=214,Va=0,Ga=1,Ha=2,Ci=3,ja=4,Wa=5,Xa=6,qa=7,Lc=0,Vl=1,Gl=2,Cn=0,Hl=1,jl=2,Wl=3,Xl=4,ql=5,Kl=6,$l=7,Ic=300,Pi=301,Di=302,Ka=303,$a=304,Kr=306,Ya=1e3,$n=1001,Za=1002,Ft=1003,Yl=1004,cr=1005,Jt=1006,ea=1007,Yn=1008,mn=1009,Uc=1010,zc=1011,Ji=1012,zs=1013,ei=1014,hn=1015,ir=1016,Ns=1017,ks=1018,Li=1020,Nc=35902,kc=1021,Fc=1022,Ht=1023,Oc=1024,Bc=1025,Ai=1026,Ii=1027,Vc=1028,Fs=1029,Gc=1030,Os=1031,Bs=1033,zr=33776,Nr=33777,kr=33778,Fr=33779,Ja=35840,Qa=35841,es=35842,ts=35843,ns=36196,is=37492,rs=37496,as=37808,ss=37809,os=37810,cs=37811,ls=37812,us=37813,ds=37814,hs=37815,fs=37816,ps=37817,ms=37818,gs=37819,_s=37820,vs=37821,Or=36492,xs=36494,Ms=36495,Hc=36283,Ss=36284,Es=36285,ys=36286,Zl=3200,Jl=3201,jc=0,Ql=1,wn="",Nt="srgb",Ui="srgb-linear",Hr="linear",it="srgb",si=7680,po=519,eu=512,tu=513,nu=514,Wc=515,iu=516,ru=517,au=518,su=519,mo=35044,go="300 es",fn=2e3,jr=2001;class ki{addEventListener(e,t){this._listeners===void 0&&(this._listeners={});const i=this._listeners;i[e]===void 0&&(i[e]=[]),i[e].indexOf(t)===-1&&i[e].push(t)}hasEventListener(e,t){const i=this._listeners;return i===void 0?!1:i[e]!==void 0&&i[e].indexOf(t)!==-1}removeEventListener(e,t){const i=this._listeners;if(i===void 0)return;const r=i[e];if(r!==void 0){const a=r.indexOf(t);a!==-1&&r.splice(a,1)}}dispatchEvent(e){const t=this._listeners;if(t===void 0)return;const i=t[e.type];if(i!==void 0){e.target=this;const r=i.slice(0);for(let a=0,s=r.length;a<s;a++)r[a].call(this,e);e.target=null}}}const bt=["00","01","02","03","04","05","06","07","08","09","0a","0b","0c","0d","0e","0f","10","11","12","13","14","15","16","17","18","19","1a","1b","1c","1d","1e","1f","20","21","22","23","24","25","26","27","28","29","2a","2b","2c","2d","2e","2f","30","31","32","33","34","35","36","37","38","39","3a","3b","3c","3d","3e","3f","40","41","42","43","44","45","46","47","48","49","4a","4b","4c","4d","4e","4f","50","51","52","53","54","55","56","57","58","59","5a","5b","5c","5d","5e","5f","60","61","62","63","64","65","66","67","68","69","6a","6b","6c","6d","6e","6f","70","71","72","73","74","75","76","77","78","79","7a","7b","7c","7d","7e","7f","80","81","82","83","84","85","86","87","88","89","8a","8b","8c","8d","8e","8f","90","91","92","93","94","95","96","97","98","99","9a","9b","9c","9d","9e","9f","a0","a1","a2","a3","a4","a5","a6","a7","a8","a9","aa","ab","ac","ad","ae","af","b0","b1","b2","b3","b4","b5","b6","b7","b8","b9","ba","bb","bc","bd","be","bf","c0","c1","c2","c3","c4","c5","c6","c7","c8","c9","ca","cb","cc","cd","ce","cf","d0","d1","d2","d3","d4","d5","d6","d7","d8","d9","da","db","dc","dd","de","df","e0","e1","e2","e3","e4","e5","e6","e7","e8","e9","ea","eb","ec","ed","ee","ef","f0","f1","f2","f3","f4","f5","f6","f7","f8","f9","fa","fb","fc","fd","fe","ff"],Br=Math.PI/180,bs=180/Math.PI;function rr(){const n=Math.random()*4294967295|0,e=Math.random()*4294967295|0,t=Math.random()*4294967295|0,i=Math.random()*4294967295|0;return(bt[n&255]+bt[n>>8&255]+bt[n>>16&255]+bt[n>>24&255]+"-"+bt[e&255]+bt[e>>8&255]+"-"+bt[e>>16&15|64]+bt[e>>24&255]+"-"+bt[t&63|128]+bt[t>>8&255]+"-"+bt[t>>16&255]+bt[t>>24&255]+bt[i&255]+bt[i>>8&255]+bt[i>>16&255]+bt[i>>24&255]).toLowerCase()}function qe(n,e,t){return Math.max(e,Math.min(t,n))}function ou(n,e){return(n%e+e)%e}function ta(n,e,t){return(1-t)*n+t*e}function Hi(n,e){switch(e.constructor){case Float32Array:return n;case Uint32Array:return n/4294967295;case Uint16Array:return n/65535;case Uint8Array:return n/255;case Int32Array:return Math.max(n/2147483647,-1);case Int16Array:return Math.max(n/32767,-1);case Int8Array:return Math.max(n/127,-1);default:throw new Error("Invalid component type.")}}function Lt(n,e){switch(e.constructor){case Float32Array:return n;case Uint32Array:return Math.round(n*4294967295);case Uint16Array:return Math.round(n*65535);case Uint8Array:return Math.round(n*255);case Int32Array:return Math.round(n*2147483647);case Int16Array:return Math.round(n*32767);case Int8Array:return Math.round(n*127);default:throw new Error("Invalid component type.")}}class We{constructor(e=0,t=0){We.prototype.isVector2=!0,this.x=e,this.y=t}get width(){return this.x}set width(e){this.x=e}get height(){return this.y}set height(e){this.y=e}set(e,t){return this.x=e,this.y=t,this}setScalar(e){return this.x=e,this.y=e,this}setX(e){return this.x=e,this}setY(e){return this.y=e,this}setComponent(e,t){switch(e){case 0:this.x=t;break;case 1:this.y=t;break;default:throw new Error("index is out of range: "+e)}return this}getComponent(e){switch(e){case 0:return this.x;case 1:return this.y;default:throw new Error("index is out of range: "+e)}}clone(){return new this.constructor(this.x,this.y)}copy(e){return this.x=e.x,this.y=e.y,this}add(e){return this.x+=e.x,this.y+=e.y,this}addScalar(e){return this.x+=e,this.y+=e,this}addVectors(e,t){return this.x=e.x+t.x,this.y=e.y+t.y,this}addScaledVector(e,t){return this.x+=e.x*t,this.y+=e.y*t,this}sub(e){return this.x-=e.x,this.y-=e.y,this}subScalar(e){return this.x-=e,this.y-=e,this}subVectors(e,t){return this.x=e.x-t.x,this.y=e.y-t.y,this}multiply(e){return this.x*=e.x,this.y*=e.y,this}multiplyScalar(e){return this.x*=e,this.y*=e,this}divide(e){return this.x/=e.x,this.y/=e.y,this}divideScalar(e){return this.multiplyScalar(1/e)}applyMatrix3(e){const t=this.x,i=this.y,r=e.elements;return this.x=r[0]*t+r[3]*i+r[6],this.y=r[1]*t+r[4]*i+r[7],this}min(e){return this.x=Math.min(this.x,e.x),this.y=Math.min(this.y,e.y),this}max(e){return this.x=Math.max(this.x,e.x),this.y=Math.max(this.y,e.y),this}clamp(e,t){return this.x=qe(this.x,e.x,t.x),this.y=qe(this.y,e.y,t.y),this}clampScalar(e,t){return this.x=qe(this.x,e,t),this.y=qe(this.y,e,t),this}clampLength(e,t){const i=this.length();return this.divideScalar(i||1).multiplyScalar(qe(i,e,t))}floor(){return this.x=Math.floor(this.x),this.y=Math.floor(this.y),this}ceil(){return this.x=Math.ceil(this.x),this.y=Math.ceil(this.y),this}round(){return this.x=Math.round(this.x),this.y=Math.round(this.y),this}roundToZero(){return this.x=Math.trunc(this.x),this.y=Math.trunc(this.y),this}negate(){return this.x=-this.x,this.y=-this.y,this}dot(e){return this.x*e.x+this.y*e.y}cross(e){return this.x*e.y-this.y*e.x}lengthSq(){return this.x*this.x+this.y*this.y}length(){return Math.sqrt(this.x*this.x+this.y*this.y)}manhattanLength(){return Math.abs(this.x)+Math.abs(this.y)}normalize(){return this.divideScalar(this.length()||1)}angle(){return Math.atan2(-this.y,-this.x)+Math.PI}angleTo(e){const t=Math.sqrt(this.lengthSq()*e.lengthSq());if(t===0)return Math.PI/2;const i=this.dot(e)/t;return Math.acos(qe(i,-1,1))}distanceTo(e){return Math.sqrt(this.distanceToSquared(e))}distanceToSquared(e){const t=this.x-e.x,i=this.y-e.y;return t*t+i*i}manhattanDistanceTo(e){return Math.abs(this.x-e.x)+Math.abs(this.y-e.y)}setLength(e){return this.normalize().multiplyScalar(e)}lerp(e,t){return this.x+=(e.x-this.x)*t,this.y+=(e.y-this.y)*t,this}lerpVectors(e,t,i){return this.x=e.x+(t.x-e.x)*i,this.y=e.y+(t.y-e.y)*i,this}equals(e){return e.x===this.x&&e.y===this.y}fromArray(e,t=0){return this.x=e[t],this.y=e[t+1],this}toArray(e=[],t=0){return e[t]=this.x,e[t+1]=this.y,e}fromBufferAttribute(e,t){return this.x=e.getX(t),this.y=e.getY(t),this}rotateAround(e,t){const i=Math.cos(t),r=Math.sin(t),a=this.x-e.x,s=this.y-e.y;return this.x=a*i-s*r+e.x,this.y=a*r+s*i+e.y,this}random(){return this.x=Math.random(),this.y=Math.random(),this}*[Symbol.iterator](){yield this.x,yield this.y}}class Ve{constructor(e,t,i,r,a,s,o,c,l){Ve.prototype.isMatrix3=!0,this.elements=[1,0,0,0,1,0,0,0,1],e!==void 0&&this.set(e,t,i,r,a,s,o,c,l)}set(e,t,i,r,a,s,o,c,l){const d=this.elements;return d[0]=e,d[1]=r,d[2]=o,d[3]=t,d[4]=a,d[5]=c,d[6]=i,d[7]=s,d[8]=l,this}identity(){return this.set(1,0,0,0,1,0,0,0,1),this}copy(e){const t=this.elements,i=e.elements;return t[0]=i[0],t[1]=i[1],t[2]=i[2],t[3]=i[3],t[4]=i[4],t[5]=i[5],t[6]=i[6],t[7]=i[7],t[8]=i[8],this}extractBasis(e,t,i){return e.setFromMatrix3Column(this,0),t.setFromMatrix3Column(this,1),i.setFromMatrix3Column(this,2),this}setFromMatrix4(e){const t=e.elements;return this.set(t[0],t[4],t[8],t[1],t[5],t[9],t[2],t[6],t[10]),this}multiply(e){return this.multiplyMatrices(this,e)}premultiply(e){return this.multiplyMatrices(e,this)}multiplyMatrices(e,t){const i=e.elements,r=t.elements,a=this.elements,s=i[0],o=i[3],c=i[6],l=i[1],d=i[4],h=i[7],f=i[2],m=i[5],g=i[8],_=r[0],p=r[3],u=r[6],E=r[1],y=r[4],M=r[7],D=r[2],A=r[5],b=r[8];return a[0]=s*_+o*E+c*D,a[3]=s*p+o*y+c*A,a[6]=s*u+o*M+c*b,a[1]=l*_+d*E+h*D,a[4]=l*p+d*y+h*A,a[7]=l*u+d*M+h*b,a[2]=f*_+m*E+g*D,a[5]=f*p+m*y+g*A,a[8]=f*u+m*M+g*b,this}multiplyScalar(e){const t=this.elements;return t[0]*=e,t[3]*=e,t[6]*=e,t[1]*=e,t[4]*=e,t[7]*=e,t[2]*=e,t[5]*=e,t[8]*=e,this}determinant(){const e=this.elements,t=e[0],i=e[1],r=e[2],a=e[3],s=e[4],o=e[5],c=e[6],l=e[7],d=e[8];return t*s*d-t*o*l-i*a*d+i*o*c+r*a*l-r*s*c}invert(){const e=this.elements,t=e[0],i=e[1],r=e[2],a=e[3],s=e[4],o=e[5],c=e[6],l=e[7],d=e[8],h=d*s-o*l,f=o*c-d*a,m=l*a-s*c,g=t*h+i*f+r*m;if(g===0)return this.set(0,0,0,0,0,0,0,0,0);const _=1/g;return e[0]=h*_,e[1]=(r*l-d*i)*_,e[2]=(o*i-r*s)*_,e[3]=f*_,e[4]=(d*t-r*c)*_,e[5]=(r*a-o*t)*_,e[6]=m*_,e[7]=(i*c-l*t)*_,e[8]=(s*t-i*a)*_,this}transpose(){let e;const t=this.elements;return e=t[1],t[1]=t[3],t[3]=e,e=t[2],t[2]=t[6],t[6]=e,e=t[5],t[5]=t[7],t[7]=e,this}getNormalMatrix(e){return this.setFromMatrix4(e).invert().transpose()}transposeIntoArray(e){const t=this.elements;return e[0]=t[0],e[1]=t[3],e[2]=t[6],e[3]=t[1],e[4]=t[4],e[5]=t[7],e[6]=t[2],e[7]=t[5],e[8]=t[8],this}setUvTransform(e,t,i,r,a,s,o){const c=Math.cos(a),l=Math.sin(a);return this.set(i*c,i*l,-i*(c*s+l*o)+s+e,-r*l,r*c,-r*(-l*s+c*o)+o+t,0,0,1),this}scale(e,t){return this.premultiply(na.makeScale(e,t)),this}rotate(e){return this.premultiply(na.makeRotation(-e)),this}translate(e,t){return this.premultiply(na.makeTranslation(e,t)),this}makeTranslation(e,t){return e.isVector2?this.set(1,0,e.x,0,1,e.y,0,0,1):this.set(1,0,e,0,1,t,0,0,1),this}makeRotation(e){const t=Math.cos(e),i=Math.sin(e);return this.set(t,-i,0,i,t,0,0,0,1),this}makeScale(e,t){return this.set(e,0,0,0,t,0,0,0,1),this}equals(e){const t=this.elements,i=e.elements;for(let r=0;r<9;r++)if(t[r]!==i[r])return!1;return!0}fromArray(e,t=0){for(let i=0;i<9;i++)this.elements[i]=e[i+t];return this}toArray(e=[],t=0){const i=this.elements;return e[t]=i[0],e[t+1]=i[1],e[t+2]=i[2],e[t+3]=i[3],e[t+4]=i[4],e[t+5]=i[5],e[t+6]=i[6],e[t+7]=i[7],e[t+8]=i[8],e}clone(){return new this.constructor().fromArray(this.elements)}}const na=new Ve;function Xc(n){for(let e=n.length-1;e>=0;--e)if(n[e]>=65535)return!0;return!1}function Wr(n){return document.createElementNS("http://www.w3.org/1999/xhtml",n)}function cu(){const n=Wr("canvas");return n.style.display="block",n}const _o={};function Vn(n){n in _o||(_o[n]=!0,console.warn(n))}function lu(n,e,t){return new Promise(function(i,r){function a(){switch(n.clientWaitSync(e,n.SYNC_FLUSH_COMMANDS_BIT,0)){case n.WAIT_FAILED:r();break;case n.TIMEOUT_EXPIRED:setTimeout(a,t);break;default:i()}}setTimeout(a,t)})}function uu(n){const e=n.elements;e[2]=.5*e[2]+.5*e[3],e[6]=.5*e[6]+.5*e[7],e[10]=.5*e[10]+.5*e[11],e[14]=.5*e[14]+.5*e[15]}function du(n){const e=n.elements;e[11]===-1?(e[10]=-e[10]-1,e[14]=-e[14]):(e[10]=-e[10],e[14]=-e[14]+1)}const vo=new Ve().set(.4123908,.3575843,.1804808,.212639,.7151687,.0721923,.0193308,.1191948,.9505322),xo=new Ve().set(3.2409699,-1.5373832,-.4986108,-.9692436,1.8759675,.0415551,.0556301,-.203977,1.0569715);function hu(){const n={enabled:!0,workingColorSpace:Ui,spaces:{},convert:function(r,a,s){return this.enabled===!1||a===s||!a||!s||(this.spaces[a].transfer===it&&(r.r=pn(r.r),r.g=pn(r.g),r.b=pn(r.b)),this.spaces[a].primaries!==this.spaces[s].primaries&&(r.applyMatrix3(this.spaces[a].toXYZ),r.applyMatrix3(this.spaces[s].fromXYZ)),this.spaces[s].transfer===it&&(r.r=Ri(r.r),r.g=Ri(r.g),r.b=Ri(r.b))),r},fromWorkingColorSpace:function(r,a){return this.convert(r,this.workingColorSpace,a)},toWorkingColorSpace:function(r,a){return this.convert(r,a,this.workingColorSpace)},getPrimaries:function(r){return this.spaces[r].primaries},getTransfer:function(r){return r===wn?Hr:this.spaces[r].transfer},getLuminanceCoefficients:function(r,a=this.workingColorSpace){return r.fromArray(this.spaces[a].luminanceCoefficients)},define:function(r){Object.assign(this.spaces,r)},_getMatrix:function(r,a,s){return r.copy(this.spaces[a].toXYZ).multiply(this.spaces[s].fromXYZ)},_getDrawingBufferColorSpace:function(r){return this.spaces[r].outputColorSpaceConfig.drawingBufferColorSpace},_getUnpackColorSpace:function(r=this.workingColorSpace){return this.spaces[r].workingColorSpaceConfig.unpackColorSpace}},e=[.64,.33,.3,.6,.15,.06],t=[.2126,.7152,.0722],i=[.3127,.329];return n.define({[Ui]:{primaries:e,whitePoint:i,transfer:Hr,toXYZ:vo,fromXYZ:xo,luminanceCoefficients:t,workingColorSpaceConfig:{unpackColorSpace:Nt},outputColorSpaceConfig:{drawingBufferColorSpace:Nt}},[Nt]:{primaries:e,whitePoint:i,transfer:it,toXYZ:vo,fromXYZ:xo,luminanceCoefficients:t,outputColorSpaceConfig:{drawingBufferColorSpace:Nt}}}),n}const Je=hu();function pn(n){return n<.04045?n*.0773993808:Math.pow(n*.9478672986+.0521327014,2.4)}function Ri(n){return n<.0031308?n*12.92:1.055*Math.pow(n,.41666)-.055}let oi;class fu{static getDataURL(e){if(/^data:/i.test(e.src)||typeof HTMLCanvasElement>"u")return e.src;let t;if(e instanceof HTMLCanvasElement)t=e;else{oi===void 0&&(oi=Wr("canvas")),oi.width=e.width,oi.height=e.height;const i=oi.getContext("2d");e instanceof ImageData?i.putImageData(e,0,0):i.drawImage(e,0,0,e.width,e.height),t=oi}return t.toDataURL("image/png")}static sRGBToLinear(e){if(typeof HTMLImageElement<"u"&&e instanceof HTMLImageElement||typeof HTMLCanvasElement<"u"&&e instanceof HTMLCanvasElement||typeof ImageBitmap<"u"&&e instanceof ImageBitmap){const t=Wr("canvas");t.width=e.width,t.height=e.height;const i=t.getContext("2d");i.drawImage(e,0,0,e.width,e.height);const r=i.getImageData(0,0,e.width,e.height),a=r.data;for(let s=0;s<a.length;s++)a[s]=pn(a[s]/255)*255;return i.putImageData(r,0,0),t}else if(e.data){const t=e.data.slice(0);for(let i=0;i<t.length;i++)t instanceof Uint8Array||t instanceof Uint8ClampedArray?t[i]=Math.floor(pn(t[i]/255)*255):t[i]=pn(t[i]);return{data:t,width:e.width,height:e.height}}else return console.warn("THREE.ImageUtils.sRGBToLinear(): Unsupported image type. No color space conversion applied."),e}}let pu=0;class Vs{constructor(e=null){this.isSource=!0,Object.defineProperty(this,"id",{value:pu++}),this.uuid=rr(),this.data=e,this.dataReady=!0,this.version=0}set needsUpdate(e){e===!0&&this.version++}toJSON(e){const t=e===void 0||typeof e=="string";if(!t&&e.images[this.uuid]!==void 0)return e.images[this.uuid];const i={uuid:this.uuid,url:""},r=this.data;if(r!==null){let a;if(Array.isArray(r)){a=[];for(let s=0,o=r.length;s<o;s++)r[s].isDataTexture?a.push(ia(r[s].image)):a.push(ia(r[s]))}else a=ia(r);i.url=a}return t||(e.images[this.uuid]=i),i}}function ia(n){return typeof HTMLImageElement<"u"&&n instanceof HTMLImageElement||typeof HTMLCanvasElement<"u"&&n instanceof HTMLCanvasElement||typeof ImageBitmap<"u"&&n instanceof ImageBitmap?fu.getDataURL(n):n.data?{data:Array.from(n.data),width:n.width,height:n.height,type:n.data.constructor.name}:(console.warn("THREE.Texture: Unable to serialize Texture."),{})}let mu=0;class wt extends ki{constructor(e=wt.DEFAULT_IMAGE,t=wt.DEFAULT_MAPPING,i=$n,r=$n,a=Jt,s=Yn,o=Ht,c=mn,l=wt.DEFAULT_ANISOTROPY,d=wn){super(),this.isTexture=!0,Object.defineProperty(this,"id",{value:mu++}),this.uuid=rr(),this.name="",this.source=new Vs(e),this.mipmaps=[],this.mapping=t,this.channel=0,this.wrapS=i,this.wrapT=r,this.magFilter=a,this.minFilter=s,this.anisotropy=l,this.format=o,this.internalFormat=null,this.type=c,this.offset=new We(0,0),this.repeat=new We(1,1),this.center=new We(0,0),this.rotation=0,this.matrixAutoUpdate=!0,this.matrix=new Ve,this.generateMipmaps=!0,this.premultiplyAlpha=!1,this.flipY=!0,this.unpackAlignment=4,this.colorSpace=d,this.userData={},this.version=0,this.onUpdate=null,this.renderTarget=null,this.isRenderTargetTexture=!1,this.pmremVersion=0}get image(){return this.source.data}set image(e=null){this.source.data=e}updateMatrix(){this.matrix.setUvTransform(this.offset.x,this.offset.y,this.repeat.x,this.repeat.y,this.rotation,this.center.x,this.center.y)}clone(){return new this.constructor().copy(this)}copy(e){return this.name=e.name,this.source=e.source,this.mipmaps=e.mipmaps.slice(0),this.mapping=e.mapping,this.channel=e.channel,this.wrapS=e.wrapS,this.wrapT=e.wrapT,this.magFilter=e.magFilter,this.minFilter=e.minFilter,this.anisotropy=e.anisotropy,this.format=e.format,this.internalFormat=e.internalFormat,this.type=e.type,this.offset.copy(e.offset),this.repeat.copy(e.repeat),this.center.copy(e.center),this.rotation=e.rotation,this.matrixAutoUpdate=e.matrixAutoUpdate,this.matrix.copy(e.matrix),this.generateMipmaps=e.generateMipmaps,this.premultiplyAlpha=e.premultiplyAlpha,this.flipY=e.flipY,this.unpackAlignment=e.unpackAlignment,this.colorSpace=e.colorSpace,this.renderTarget=e.renderTarget,this.isRenderTargetTexture=e.isRenderTargetTexture,this.userData=JSON.parse(JSON.stringify(e.userData)),this.needsUpdate=!0,this}toJSON(e){const t=e===void 0||typeof e=="string";if(!t&&e.textures[this.uuid]!==void 0)return e.textures[this.uuid];const i={metadata:{version:4.6,type:"Texture",generator:"Texture.toJSON"},uuid:this.uuid,name:this.name,image:this.source.toJSON(e).uuid,mapping:this.mapping,channel:this.channel,repeat:[this.repeat.x,this.repeat.y],offset:[this.offset.x,this.offset.y],center:[this.center.x,this.center.y],rotation:this.rotation,wrap:[this.wrapS,this.wrapT],format:this.format,internalFormat:this.internalFormat,type:this.type,colorSpace:this.colorSpace,minFilter:this.minFilter,magFilter:this.magFilter,anisotropy:this.anisotropy,flipY:this.flipY,generateMipmaps:this.generateMipmaps,premultiplyAlpha:this.premultiplyAlpha,unpackAlignment:this.unpackAlignment};return Object.keys(this.userData).length>0&&(i.userData=this.userData),t||(e.textures[this.uuid]=i),i}dispose(){this.dispatchEvent({type:"dispose"})}transformUv(e){if(this.mapping!==Ic)return e;if(e.applyMatrix3(this.matrix),e.x<0||e.x>1)switch(this.wrapS){case Ya:e.x=e.x-Math.floor(e.x);break;case $n:e.x=e.x<0?0:1;break;case Za:Math.abs(Math.floor(e.x)%2)===1?e.x=Math.ceil(e.x)-e.x:e.x=e.x-Math.floor(e.x);break}if(e.y<0||e.y>1)switch(this.wrapT){case Ya:e.y=e.y-Math.floor(e.y);break;case $n:e.y=e.y<0?0:1;break;case Za:Math.abs(Math.floor(e.y)%2)===1?e.y=Math.ceil(e.y)-e.y:e.y=e.y-Math.floor(e.y);break}return this.flipY&&(e.y=1-e.y),e}set needsUpdate(e){e===!0&&(this.version++,this.source.needsUpdate=!0)}set needsPMREMUpdate(e){e===!0&&this.pmremVersion++}}wt.DEFAULT_IMAGE=null;wt.DEFAULT_MAPPING=Ic;wt.DEFAULT_ANISOTROPY=1;class rt{constructor(e=0,t=0,i=0,r=1){rt.prototype.isVector4=!0,this.x=e,this.y=t,this.z=i,this.w=r}get width(){return this.z}set width(e){this.z=e}get height(){return this.w}set height(e){this.w=e}set(e,t,i,r){return this.x=e,this.y=t,this.z=i,this.w=r,this}setScalar(e){return this.x=e,this.y=e,this.z=e,this.w=e,this}setX(e){return this.x=e,this}setY(e){return this.y=e,this}setZ(e){return this.z=e,this}setW(e){return this.w=e,this}setComponent(e,t){switch(e){case 0:this.x=t;break;case 1:this.y=t;break;case 2:this.z=t;break;case 3:this.w=t;break;default:throw new Error("index is out of range: "+e)}return this}getComponent(e){switch(e){case 0:return this.x;case 1:return this.y;case 2:return this.z;case 3:return this.w;default:throw new Error("index is out of range: "+e)}}clone(){return new this.constructor(this.x,this.y,this.z,this.w)}copy(e){return this.x=e.x,this.y=e.y,this.z=e.z,this.w=e.w!==void 0?e.w:1,this}add(e){return this.x+=e.x,this.y+=e.y,this.z+=e.z,this.w+=e.w,this}addScalar(e){return this.x+=e,this.y+=e,this.z+=e,this.w+=e,this}addVectors(e,t){return this.x=e.x+t.x,this.y=e.y+t.y,this.z=e.z+t.z,this.w=e.w+t.w,this}addScaledVector(e,t){return this.x+=e.x*t,this.y+=e.y*t,this.z+=e.z*t,this.w+=e.w*t,this}sub(e){return this.x-=e.x,this.y-=e.y,this.z-=e.z,this.w-=e.w,this}subScalar(e){return this.x-=e,this.y-=e,this.z-=e,this.w-=e,this}subVectors(e,t){return this.x=e.x-t.x,this.y=e.y-t.y,this.z=e.z-t.z,this.w=e.w-t.w,this}multiply(e){return this.x*=e.x,this.y*=e.y,this.z*=e.z,this.w*=e.w,this}multiplyScalar(e){return this.x*=e,this.y*=e,this.z*=e,this.w*=e,this}applyMatrix4(e){const t=this.x,i=this.y,r=this.z,a=this.w,s=e.elements;return this.x=s[0]*t+s[4]*i+s[8]*r+s[12]*a,this.y=s[1]*t+s[5]*i+s[9]*r+s[13]*a,this.z=s[2]*t+s[6]*i+s[10]*r+s[14]*a,this.w=s[3]*t+s[7]*i+s[11]*r+s[15]*a,this}divide(e){return this.x/=e.x,this.y/=e.y,this.z/=e.z,this.w/=e.w,this}divideScalar(e){return this.multiplyScalar(1/e)}setAxisAngleFromQuaternion(e){this.w=2*Math.acos(e.w);const t=Math.sqrt(1-e.w*e.w);return t<1e-4?(this.x=1,this.y=0,this.z=0):(this.x=e.x/t,this.y=e.y/t,this.z=e.z/t),this}setAxisAngleFromRotationMatrix(e){let t,i,r,a;const c=e.elements,l=c[0],d=c[4],h=c[8],f=c[1],m=c[5],g=c[9],_=c[2],p=c[6],u=c[10];if(Math.abs(d-f)<.01&&Math.abs(h-_)<.01&&Math.abs(g-p)<.01){if(Math.abs(d+f)<.1&&Math.abs(h+_)<.1&&Math.abs(g+p)<.1&&Math.abs(l+m+u-3)<.1)return this.set(1,0,0,0),this;t=Math.PI;const y=(l+1)/2,M=(m+1)/2,D=(u+1)/2,A=(d+f)/4,b=(h+_)/4,C=(g+p)/4;return y>M&&y>D?y<.01?(i=0,r=.707106781,a=.707106781):(i=Math.sqrt(y),r=A/i,a=b/i):M>D?M<.01?(i=.707106781,r=0,a=.707106781):(r=Math.sqrt(M),i=A/r,a=C/r):D<.01?(i=.707106781,r=.707106781,a=0):(a=Math.sqrt(D),i=b/a,r=C/a),this.set(i,r,a,t),this}let E=Math.sqrt((p-g)*(p-g)+(h-_)*(h-_)+(f-d)*(f-d));return Math.abs(E)<.001&&(E=1),this.x=(p-g)/E,this.y=(h-_)/E,this.z=(f-d)/E,this.w=Math.acos((l+m+u-1)/2),this}setFromMatrixPosition(e){const t=e.elements;return this.x=t[12],this.y=t[13],this.z=t[14],this.w=t[15],this}min(e){return this.x=Math.min(this.x,e.x),this.y=Math.min(this.y,e.y),this.z=Math.min(this.z,e.z),this.w=Math.min(this.w,e.w),this}max(e){return this.x=Math.max(this.x,e.x),this.y=Math.max(this.y,e.y),this.z=Math.max(this.z,e.z),this.w=Math.max(this.w,e.w),this}clamp(e,t){return this.x=qe(this.x,e.x,t.x),this.y=qe(this.y,e.y,t.y),this.z=qe(this.z,e.z,t.z),this.w=qe(this.w,e.w,t.w),this}clampScalar(e,t){return this.x=qe(this.x,e,t),this.y=qe(this.y,e,t),this.z=qe(this.z,e,t),this.w=qe(this.w,e,t),this}clampLength(e,t){const i=this.length();return this.divideScalar(i||1).multiplyScalar(qe(i,e,t))}floor(){return this.x=Math.floor(this.x),this.y=Math.floor(this.y),this.z=Math.floor(this.z),this.w=Math.floor(this.w),this}ceil(){return this.x=Math.ceil(this.x),this.y=Math.ceil(this.y),this.z=Math.ceil(this.z),this.w=Math.ceil(this.w),this}round(){return this.x=Math.round(this.x),this.y=Math.round(this.y),this.z=Math.round(this.z),this.w=Math.round(this.w),this}roundToZero(){return this.x=Math.trunc(this.x),this.y=Math.trunc(this.y),this.z=Math.trunc(this.z),this.w=Math.trunc(this.w),this}negate(){return this.x=-this.x,this.y=-this.y,this.z=-this.z,this.w=-this.w,this}dot(e){return this.x*e.x+this.y*e.y+this.z*e.z+this.w*e.w}lengthSq(){return this.x*this.x+this.y*this.y+this.z*this.z+this.w*this.w}length(){return Math.sqrt(this.x*this.x+this.y*this.y+this.z*this.z+this.w*this.w)}manhattanLength(){return Math.abs(this.x)+Math.abs(this.y)+Math.abs(this.z)+Math.abs(this.w)}normalize(){return this.divideScalar(this.length()||1)}setLength(e){return this.normalize().multiplyScalar(e)}lerp(e,t){return this.x+=(e.x-this.x)*t,this.y+=(e.y-this.y)*t,this.z+=(e.z-this.z)*t,this.w+=(e.w-this.w)*t,this}lerpVectors(e,t,i){return this.x=e.x+(t.x-e.x)*i,this.y=e.y+(t.y-e.y)*i,this.z=e.z+(t.z-e.z)*i,this.w=e.w+(t.w-e.w)*i,this}equals(e){return e.x===this.x&&e.y===this.y&&e.z===this.z&&e.w===this.w}fromArray(e,t=0){return this.x=e[t],this.y=e[t+1],this.z=e[t+2],this.w=e[t+3],this}toArray(e=[],t=0){return e[t]=this.x,e[t+1]=this.y,e[t+2]=this.z,e[t+3]=this.w,e}fromBufferAttribute(e,t){return this.x=e.getX(t),this.y=e.getY(t),this.z=e.getZ(t),this.w=e.getW(t),this}random(){return this.x=Math.random(),this.y=Math.random(),this.z=Math.random(),this.w=Math.random(),this}*[Symbol.iterator](){yield this.x,yield this.y,yield this.z,yield this.w}}class gu extends ki{constructor(e=1,t=1,i={}){super(),this.isRenderTarget=!0,this.width=e,this.height=t,this.depth=1,this.scissor=new rt(0,0,e,t),this.scissorTest=!1,this.viewport=new rt(0,0,e,t);const r={width:e,height:t,depth:1};i=Object.assign({generateMipmaps:!1,internalFormat:null,minFilter:Jt,depthBuffer:!0,stencilBuffer:!1,resolveDepthBuffer:!0,resolveStencilBuffer:!0,depthTexture:null,samples:0,count:1},i);const a=new wt(r,i.mapping,i.wrapS,i.wrapT,i.magFilter,i.minFilter,i.format,i.type,i.anisotropy,i.colorSpace);a.flipY=!1,a.generateMipmaps=i.generateMipmaps,a.internalFormat=i.internalFormat,this.textures=[];const s=i.count;for(let o=0;o<s;o++)this.textures[o]=a.clone(),this.textures[o].isRenderTargetTexture=!0,this.textures[o].renderTarget=this;this.depthBuffer=i.depthBuffer,this.stencilBuffer=i.stencilBuffer,this.resolveDepthBuffer=i.resolveDepthBuffer,this.resolveStencilBuffer=i.resolveStencilBuffer,this._depthTexture=null,this.depthTexture=i.depthTexture,this.samples=i.samples}get texture(){return this.textures[0]}set texture(e){this.textures[0]=e}set depthTexture(e){this._depthTexture!==null&&(this._depthTexture.renderTarget=null),e!==null&&(e.renderTarget=this),this._depthTexture=e}get depthTexture(){return this._depthTexture}setSize(e,t,i=1){if(this.width!==e||this.height!==t||this.depth!==i){this.width=e,this.height=t,this.depth=i;for(let r=0,a=this.textures.length;r<a;r++)this.textures[r].image.width=e,this.textures[r].image.height=t,this.textures[r].image.depth=i;this.dispose()}this.viewport.set(0,0,e,t),this.scissor.set(0,0,e,t)}clone(){return new this.constructor().copy(this)}copy(e){this.width=e.width,this.height=e.height,this.depth=e.depth,this.scissor.copy(e.scissor),this.scissorTest=e.scissorTest,this.viewport.copy(e.viewport),this.textures.length=0;for(let t=0,i=e.textures.length;t<i;t++){this.textures[t]=e.textures[t].clone(),this.textures[t].isRenderTargetTexture=!0,this.textures[t].renderTarget=this;const r=Object.assign({},e.textures[t].image);this.textures[t].source=new Vs(r)}return this.depthBuffer=e.depthBuffer,this.stencilBuffer=e.stencilBuffer,this.resolveDepthBuffer=e.resolveDepthBuffer,this.resolveStencilBuffer=e.resolveStencilBuffer,e.depthTexture!==null&&(this.depthTexture=e.depthTexture.clone()),this.samples=e.samples,this}dispose(){this.dispatchEvent({type:"dispose"})}}class ti extends gu{constructor(e=1,t=1,i={}){super(e,t,i),this.isWebGLRenderTarget=!0}}class qc extends wt{constructor(e=null,t=1,i=1,r=1){super(null),this.isDataArrayTexture=!0,this.image={data:e,width:t,height:i,depth:r},this.magFilter=Ft,this.minFilter=Ft,this.wrapR=$n,this.generateMipmaps=!1,this.flipY=!1,this.unpackAlignment=1,this.layerUpdates=new Set}addLayerUpdate(e){this.layerUpdates.add(e)}clearLayerUpdates(){this.layerUpdates.clear()}}class _u extends wt{constructor(e=null,t=1,i=1,r=1){super(null),this.isData3DTexture=!0,this.image={data:e,width:t,height:i,depth:r},this.magFilter=Ft,this.minFilter=Ft,this.wrapR=$n,this.generateMipmaps=!1,this.flipY=!1,this.unpackAlignment=1}}class Fi{constructor(e=0,t=0,i=0,r=1){this.isQuaternion=!0,this._x=e,this._y=t,this._z=i,this._w=r}static slerpFlat(e,t,i,r,a,s,o){let c=i[r+0],l=i[r+1],d=i[r+2],h=i[r+3];const f=a[s+0],m=a[s+1],g=a[s+2],_=a[s+3];if(o===0){e[t+0]=c,e[t+1]=l,e[t+2]=d,e[t+3]=h;return}if(o===1){e[t+0]=f,e[t+1]=m,e[t+2]=g,e[t+3]=_;return}if(h!==_||c!==f||l!==m||d!==g){let p=1-o;const u=c*f+l*m+d*g+h*_,E=u>=0?1:-1,y=1-u*u;if(y>Number.EPSILON){const D=Math.sqrt(y),A=Math.atan2(D,u*E);p=Math.sin(p*A)/D,o=Math.sin(o*A)/D}const M=o*E;if(c=c*p+f*M,l=l*p+m*M,d=d*p+g*M,h=h*p+_*M,p===1-o){const D=1/Math.sqrt(c*c+l*l+d*d+h*h);c*=D,l*=D,d*=D,h*=D}}e[t]=c,e[t+1]=l,e[t+2]=d,e[t+3]=h}static multiplyQuaternionsFlat(e,t,i,r,a,s){const o=i[r],c=i[r+1],l=i[r+2],d=i[r+3],h=a[s],f=a[s+1],m=a[s+2],g=a[s+3];return e[t]=o*g+d*h+c*m-l*f,e[t+1]=c*g+d*f+l*h-o*m,e[t+2]=l*g+d*m+o*f-c*h,e[t+3]=d*g-o*h-c*f-l*m,e}get x(){return this._x}set x(e){this._x=e,this._onChangeCallback()}get y(){return this._y}set y(e){this._y=e,this._onChangeCallback()}get z(){return this._z}set z(e){this._z=e,this._onChangeCallback()}get w(){return this._w}set w(e){this._w=e,this._onChangeCallback()}set(e,t,i,r){return this._x=e,this._y=t,this._z=i,this._w=r,this._onChangeCallback(),this}clone(){return new this.constructor(this._x,this._y,this._z,this._w)}copy(e){return this._x=e.x,this._y=e.y,this._z=e.z,this._w=e.w,this._onChangeCallback(),this}setFromEuler(e,t=!0){const i=e._x,r=e._y,a=e._z,s=e._order,o=Math.cos,c=Math.sin,l=o(i/2),d=o(r/2),h=o(a/2),f=c(i/2),m=c(r/2),g=c(a/2);switch(s){case"XYZ":this._x=f*d*h+l*m*g,this._y=l*m*h-f*d*g,this._z=l*d*g+f*m*h,this._w=l*d*h-f*m*g;break;case"YXZ":this._x=f*d*h+l*m*g,this._y=l*m*h-f*d*g,this._z=l*d*g-f*m*h,this._w=l*d*h+f*m*g;break;case"ZXY":this._x=f*d*h-l*m*g,this._y=l*m*h+f*d*g,this._z=l*d*g+f*m*h,this._w=l*d*h-f*m*g;break;case"ZYX":this._x=f*d*h-l*m*g,this._y=l*m*h+f*d*g,this._z=l*d*g-f*m*h,this._w=l*d*h+f*m*g;break;case"YZX":this._x=f*d*h+l*m*g,this._y=l*m*h+f*d*g,this._z=l*d*g-f*m*h,this._w=l*d*h-f*m*g;break;case"XZY":this._x=f*d*h-l*m*g,this._y=l*m*h-f*d*g,this._z=l*d*g+f*m*h,this._w=l*d*h+f*m*g;break;default:console.warn("THREE.Quaternion: .setFromEuler() encountered an unknown order: "+s)}return t===!0&&this._onChangeCallback(),this}setFromAxisAngle(e,t){const i=t/2,r=Math.sin(i);return this._x=e.x*r,this._y=e.y*r,this._z=e.z*r,this._w=Math.cos(i),this._onChangeCallback(),this}setFromRotationMatrix(e){const t=e.elements,i=t[0],r=t[4],a=t[8],s=t[1],o=t[5],c=t[9],l=t[2],d=t[6],h=t[10],f=i+o+h;if(f>0){const m=.5/Math.sqrt(f+1);this._w=.25/m,this._x=(d-c)*m,this._y=(a-l)*m,this._z=(s-r)*m}else if(i>o&&i>h){const m=2*Math.sqrt(1+i-o-h);this._w=(d-c)/m,this._x=.25*m,this._y=(r+s)/m,this._z=(a+l)/m}else if(o>h){const m=2*Math.sqrt(1+o-i-h);this._w=(a-l)/m,this._x=(r+s)/m,this._y=.25*m,this._z=(c+d)/m}else{const m=2*Math.sqrt(1+h-i-o);this._w=(s-r)/m,this._x=(a+l)/m,this._y=(c+d)/m,this._z=.25*m}return this._onChangeCallback(),this}setFromUnitVectors(e,t){let i=e.dot(t)+1;return i<Number.EPSILON?(i=0,Math.abs(e.x)>Math.abs(e.z)?(this._x=-e.y,this._y=e.x,this._z=0,this._w=i):(this._x=0,this._y=-e.z,this._z=e.y,this._w=i)):(this._x=e.y*t.z-e.z*t.y,this._y=e.z*t.x-e.x*t.z,this._z=e.x*t.y-e.y*t.x,this._w=i),this.normalize()}angleTo(e){return 2*Math.acos(Math.abs(qe(this.dot(e),-1,1)))}rotateTowards(e,t){const i=this.angleTo(e);if(i===0)return this;const r=Math.min(1,t/i);return this.slerp(e,r),this}identity(){return this.set(0,0,0,1)}invert(){return this.conjugate()}conjugate(){return this._x*=-1,this._y*=-1,this._z*=-1,this._onChangeCallback(),this}dot(e){return this._x*e._x+this._y*e._y+this._z*e._z+this._w*e._w}lengthSq(){return this._x*this._x+this._y*this._y+this._z*this._z+this._w*this._w}length(){return Math.sqrt(this._x*this._x+this._y*this._y+this._z*this._z+this._w*this._w)}normalize(){let e=this.length();return e===0?(this._x=0,this._y=0,this._z=0,this._w=1):(e=1/e,this._x=this._x*e,this._y=this._y*e,this._z=this._z*e,this._w=this._w*e),this._onChangeCallback(),this}multiply(e){return this.multiplyQuaternions(this,e)}premultiply(e){return this.multiplyQuaternions(e,this)}multiplyQuaternions(e,t){const i=e._x,r=e._y,a=e._z,s=e._w,o=t._x,c=t._y,l=t._z,d=t._w;return this._x=i*d+s*o+r*l-a*c,this._y=r*d+s*c+a*o-i*l,this._z=a*d+s*l+i*c-r*o,this._w=s*d-i*o-r*c-a*l,this._onChangeCallback(),this}slerp(e,t){if(t===0)return this;if(t===1)return this.copy(e);const i=this._x,r=this._y,a=this._z,s=this._w;let o=s*e._w+i*e._x+r*e._y+a*e._z;if(o<0?(this._w=-e._w,this._x=-e._x,this._y=-e._y,this._z=-e._z,o=-o):this.copy(e),o>=1)return this._w=s,this._x=i,this._y=r,this._z=a,this;const c=1-o*o;if(c<=Number.EPSILON){const m=1-t;return this._w=m*s+t*this._w,this._x=m*i+t*this._x,this._y=m*r+t*this._y,this._z=m*a+t*this._z,this.normalize(),this}const l=Math.sqrt(c),d=Math.atan2(l,o),h=Math.sin((1-t)*d)/l,f=Math.sin(t*d)/l;return this._w=s*h+this._w*f,this._x=i*h+this._x*f,this._y=r*h+this._y*f,this._z=a*h+this._z*f,this._onChangeCallback(),this}slerpQuaternions(e,t,i){return this.copy(e).slerp(t,i)}random(){const e=2*Math.PI*Math.random(),t=2*Math.PI*Math.random(),i=Math.random(),r=Math.sqrt(1-i),a=Math.sqrt(i);return this.set(r*Math.sin(e),r*Math.cos(e),a*Math.sin(t),a*Math.cos(t))}equals(e){return e._x===this._x&&e._y===this._y&&e._z===this._z&&e._w===this._w}fromArray(e,t=0){return this._x=e[t],this._y=e[t+1],this._z=e[t+2],this._w=e[t+3],this._onChangeCallback(),this}toArray(e=[],t=0){return e[t]=this._x,e[t+1]=this._y,e[t+2]=this._z,e[t+3]=this._w,e}fromBufferAttribute(e,t){return this._x=e.getX(t),this._y=e.getY(t),this._z=e.getZ(t),this._w=e.getW(t),this._onChangeCallback(),this}toJSON(){return this.toArray()}_onChange(e){return this._onChangeCallback=e,this}_onChangeCallback(){}*[Symbol.iterator](){yield this._x,yield this._y,yield this._z,yield this._w}}class F{constructor(e=0,t=0,i=0){F.prototype.isVector3=!0,this.x=e,this.y=t,this.z=i}set(e,t,i){return i===void 0&&(i=this.z),this.x=e,this.y=t,this.z=i,this}setScalar(e){return this.x=e,this.y=e,this.z=e,this}setX(e){return this.x=e,this}setY(e){return this.y=e,this}setZ(e){return this.z=e,this}setComponent(e,t){switch(e){case 0:this.x=t;break;case 1:this.y=t;break;case 2:this.z=t;break;default:throw new Error("index is out of range: "+e)}return this}getComponent(e){switch(e){case 0:return this.x;case 1:return this.y;case 2:return this.z;default:throw new Error("index is out of range: "+e)}}clone(){return new this.constructor(this.x,this.y,this.z)}copy(e){return this.x=e.x,this.y=e.y,this.z=e.z,this}add(e){return this.x+=e.x,this.y+=e.y,this.z+=e.z,this}addScalar(e){return this.x+=e,this.y+=e,this.z+=e,this}addVectors(e,t){return this.x=e.x+t.x,this.y=e.y+t.y,this.z=e.z+t.z,this}addScaledVector(e,t){return this.x+=e.x*t,this.y+=e.y*t,this.z+=e.z*t,this}sub(e){return this.x-=e.x,this.y-=e.y,this.z-=e.z,this}subScalar(e){return this.x-=e,this.y-=e,this.z-=e,this}subVectors(e,t){return this.x=e.x-t.x,this.y=e.y-t.y,this.z=e.z-t.z,this}multiply(e){return this.x*=e.x,this.y*=e.y,this.z*=e.z,this}multiplyScalar(e){return this.x*=e,this.y*=e,this.z*=e,this}multiplyVectors(e,t){return this.x=e.x*t.x,this.y=e.y*t.y,this.z=e.z*t.z,this}applyEuler(e){return this.applyQuaternion(Mo.setFromEuler(e))}applyAxisAngle(e,t){return this.applyQuaternion(Mo.setFromAxisAngle(e,t))}applyMatrix3(e){const t=this.x,i=this.y,r=this.z,a=e.elements;return this.x=a[0]*t+a[3]*i+a[6]*r,this.y=a[1]*t+a[4]*i+a[7]*r,this.z=a[2]*t+a[5]*i+a[8]*r,this}applyNormalMatrix(e){return this.applyMatrix3(e).normalize()}applyMatrix4(e){const t=this.x,i=this.y,r=this.z,a=e.elements,s=1/(a[3]*t+a[7]*i+a[11]*r+a[15]);return this.x=(a[0]*t+a[4]*i+a[8]*r+a[12])*s,this.y=(a[1]*t+a[5]*i+a[9]*r+a[13])*s,this.z=(a[2]*t+a[6]*i+a[10]*r+a[14])*s,this}applyQuaternion(e){const t=this.x,i=this.y,r=this.z,a=e.x,s=e.y,o=e.z,c=e.w,l=2*(s*r-o*i),d=2*(o*t-a*r),h=2*(a*i-s*t);return this.x=t+c*l+s*h-o*d,this.y=i+c*d+o*l-a*h,this.z=r+c*h+a*d-s*l,this}project(e){return this.applyMatrix4(e.matrixWorldInverse).applyMatrix4(e.projectionMatrix)}unproject(e){return this.applyMatrix4(e.projectionMatrixInverse).applyMatrix4(e.matrixWorld)}transformDirection(e){const t=this.x,i=this.y,r=this.z,a=e.elements;return this.x=a[0]*t+a[4]*i+a[8]*r,this.y=a[1]*t+a[5]*i+a[9]*r,this.z=a[2]*t+a[6]*i+a[10]*r,this.normalize()}divide(e){return this.x/=e.x,this.y/=e.y,this.z/=e.z,this}divideScalar(e){return this.multiplyScalar(1/e)}min(e){return this.x=Math.min(this.x,e.x),this.y=Math.min(this.y,e.y),this.z=Math.min(this.z,e.z),this}max(e){return this.x=Math.max(this.x,e.x),this.y=Math.max(this.y,e.y),this.z=Math.max(this.z,e.z),this}clamp(e,t){return this.x=qe(this.x,e.x,t.x),this.y=qe(this.y,e.y,t.y),this.z=qe(this.z,e.z,t.z),this}clampScalar(e,t){return this.x=qe(this.x,e,t),this.y=qe(this.y,e,t),this.z=qe(this.z,e,t),this}clampLength(e,t){const i=this.length();return this.divideScalar(i||1).multiplyScalar(qe(i,e,t))}floor(){return this.x=Math.floor(this.x),this.y=Math.floor(this.y),this.z=Math.floor(this.z),this}ceil(){return this.x=Math.ceil(this.x),this.y=Math.ceil(this.y),this.z=Math.ceil(this.z),this}round(){return this.x=Math.round(this.x),this.y=Math.round(this.y),this.z=Math.round(this.z),this}roundToZero(){return this.x=Math.trunc(this.x),this.y=Math.trunc(this.y),this.z=Math.trunc(this.z),this}negate(){return this.x=-this.x,this.y=-this.y,this.z=-this.z,this}dot(e){return this.x*e.x+this.y*e.y+this.z*e.z}lengthSq(){return this.x*this.x+this.y*this.y+this.z*this.z}length(){return Math.sqrt(this.x*this.x+this.y*this.y+this.z*this.z)}manhattanLength(){return Math.abs(this.x)+Math.abs(this.y)+Math.abs(this.z)}normalize(){return this.divideScalar(this.length()||1)}setLength(e){return this.normalize().multiplyScalar(e)}lerp(e,t){return this.x+=(e.x-this.x)*t,this.y+=(e.y-this.y)*t,this.z+=(e.z-this.z)*t,this}lerpVectors(e,t,i){return this.x=e.x+(t.x-e.x)*i,this.y=e.y+(t.y-e.y)*i,this.z=e.z+(t.z-e.z)*i,this}cross(e){return this.crossVectors(this,e)}crossVectors(e,t){const i=e.x,r=e.y,a=e.z,s=t.x,o=t.y,c=t.z;return this.x=r*c-a*o,this.y=a*s-i*c,this.z=i*o-r*s,this}projectOnVector(e){const t=e.lengthSq();if(t===0)return this.set(0,0,0);const i=e.dot(this)/t;return this.copy(e).multiplyScalar(i)}projectOnPlane(e){return ra.copy(this).projectOnVector(e),this.sub(ra)}reflect(e){return this.sub(ra.copy(e).multiplyScalar(2*this.dot(e)))}angleTo(e){const t=Math.sqrt(this.lengthSq()*e.lengthSq());if(t===0)return Math.PI/2;const i=this.dot(e)/t;return Math.acos(qe(i,-1,1))}distanceTo(e){return Math.sqrt(this.distanceToSquared(e))}distanceToSquared(e){const t=this.x-e.x,i=this.y-e.y,r=this.z-e.z;return t*t+i*i+r*r}manhattanDistanceTo(e){return Math.abs(this.x-e.x)+Math.abs(this.y-e.y)+Math.abs(this.z-e.z)}setFromSpherical(e){return this.setFromSphericalCoords(e.radius,e.phi,e.theta)}setFromSphericalCoords(e,t,i){const r=Math.sin(t)*e;return this.x=r*Math.sin(i),this.y=Math.cos(t)*e,this.z=r*Math.cos(i),this}setFromCylindrical(e){return this.setFromCylindricalCoords(e.radius,e.theta,e.y)}setFromCylindricalCoords(e,t,i){return this.x=e*Math.sin(t),this.y=i,this.z=e*Math.cos(t),this}setFromMatrixPosition(e){const t=e.elements;return this.x=t[12],this.y=t[13],this.z=t[14],this}setFromMatrixScale(e){const t=this.setFromMatrixColumn(e,0).length(),i=this.setFromMatrixColumn(e,1).length(),r=this.setFromMatrixColumn(e,2).length();return this.x=t,this.y=i,this.z=r,this}setFromMatrixColumn(e,t){return this.fromArray(e.elements,t*4)}setFromMatrix3Column(e,t){return this.fromArray(e.elements,t*3)}setFromEuler(e){return this.x=e._x,this.y=e._y,this.z=e._z,this}setFromColor(e){return this.x=e.r,this.y=e.g,this.z=e.b,this}equals(e){return e.x===this.x&&e.y===this.y&&e.z===this.z}fromArray(e,t=0){return this.x=e[t],this.y=e[t+1],this.z=e[t+2],this}toArray(e=[],t=0){return e[t]=this.x,e[t+1]=this.y,e[t+2]=this.z,e}fromBufferAttribute(e,t){return this.x=e.getX(t),this.y=e.getY(t),this.z=e.getZ(t),this}random(){return this.x=Math.random(),this.y=Math.random(),this.z=Math.random(),this}randomDirection(){const e=Math.random()*Math.PI*2,t=Math.random()*2-1,i=Math.sqrt(1-t*t);return this.x=i*Math.cos(e),this.y=t,this.z=i*Math.sin(e),this}*[Symbol.iterator](){yield this.x,yield this.y,yield this.z}}const ra=new F,Mo=new Fi;class Oi{constructor(e=new F(1/0,1/0,1/0),t=new F(-1/0,-1/0,-1/0)){this.isBox3=!0,this.min=e,this.max=t}set(e,t){return this.min.copy(e),this.max.copy(t),this}setFromArray(e){this.makeEmpty();for(let t=0,i=e.length;t<i;t+=3)this.expandByPoint(Xt.fromArray(e,t));return this}setFromBufferAttribute(e){this.makeEmpty();for(let t=0,i=e.count;t<i;t++)this.expandByPoint(Xt.fromBufferAttribute(e,t));return this}setFromPoints(e){this.makeEmpty();for(let t=0,i=e.length;t<i;t++)this.expandByPoint(e[t]);return this}setFromCenterAndSize(e,t){const i=Xt.copy(t).multiplyScalar(.5);return this.min.copy(e).sub(i),this.max.copy(e).add(i),this}setFromObject(e,t=!1){return this.makeEmpty(),this.expandByObject(e,t)}clone(){return new this.constructor().copy(this)}copy(e){return this.min.copy(e.min),this.max.copy(e.max),this}makeEmpty(){return this.min.x=this.min.y=this.min.z=1/0,this.max.x=this.max.y=this.max.z=-1/0,this}isEmpty(){return this.max.x<this.min.x||this.max.y<this.min.y||this.max.z<this.min.z}getCenter(e){return this.isEmpty()?e.set(0,0,0):e.addVectors(this.min,this.max).multiplyScalar(.5)}getSize(e){return this.isEmpty()?e.set(0,0,0):e.subVectors(this.max,this.min)}expandByPoint(e){return this.min.min(e),this.max.max(e),this}expandByVector(e){return this.min.sub(e),this.max.add(e),this}expandByScalar(e){return this.min.addScalar(-e),this.max.addScalar(e),this}expandByObject(e,t=!1){e.updateWorldMatrix(!1,!1);const i=e.geometry;if(i!==void 0){const a=i.getAttribute("position");if(t===!0&&a!==void 0&&e.isInstancedMesh!==!0)for(let s=0,o=a.count;s<o;s++)e.isMesh===!0?e.getVertexPosition(s,Xt):Xt.fromBufferAttribute(a,s),Xt.applyMatrix4(e.matrixWorld),this.expandByPoint(Xt);else e.boundingBox!==void 0?(e.boundingBox===null&&e.computeBoundingBox(),lr.copy(e.boundingBox)):(i.boundingBox===null&&i.computeBoundingBox(),lr.copy(i.boundingBox)),lr.applyMatrix4(e.matrixWorld),this.union(lr)}const r=e.children;for(let a=0,s=r.length;a<s;a++)this.expandByObject(r[a],t);return this}containsPoint(e){return e.x>=this.min.x&&e.x<=this.max.x&&e.y>=this.min.y&&e.y<=this.max.y&&e.z>=this.min.z&&e.z<=this.max.z}containsBox(e){return this.min.x<=e.min.x&&e.max.x<=this.max.x&&this.min.y<=e.min.y&&e.max.y<=this.max.y&&this.min.z<=e.min.z&&e.max.z<=this.max.z}getParameter(e,t){return t.set((e.x-this.min.x)/(this.max.x-this.min.x),(e.y-this.min.y)/(this.max.y-this.min.y),(e.z-this.min.z)/(this.max.z-this.min.z))}intersectsBox(e){return e.max.x>=this.min.x&&e.min.x<=this.max.x&&e.max.y>=this.min.y&&e.min.y<=this.max.y&&e.max.z>=this.min.z&&e.min.z<=this.max.z}intersectsSphere(e){return this.clampPoint(e.center,Xt),Xt.distanceToSquared(e.center)<=e.radius*e.radius}intersectsPlane(e){let t,i;return e.normal.x>0?(t=e.normal.x*this.min.x,i=e.normal.x*this.max.x):(t=e.normal.x*this.max.x,i=e.normal.x*this.min.x),e.normal.y>0?(t+=e.normal.y*this.min.y,i+=e.normal.y*this.max.y):(t+=e.normal.y*this.max.y,i+=e.normal.y*this.min.y),e.normal.z>0?(t+=e.normal.z*this.min.z,i+=e.normal.z*this.max.z):(t+=e.normal.z*this.max.z,i+=e.normal.z*this.min.z),t<=-e.constant&&i>=-e.constant}intersectsTriangle(e){if(this.isEmpty())return!1;this.getCenter(ji),ur.subVectors(this.max,ji),ci.subVectors(e.a,ji),li.subVectors(e.b,ji),ui.subVectors(e.c,ji),gn.subVectors(li,ci),_n.subVectors(ui,li),zn.subVectors(ci,ui);let t=[0,-gn.z,gn.y,0,-_n.z,_n.y,0,-zn.z,zn.y,gn.z,0,-gn.x,_n.z,0,-_n.x,zn.z,0,-zn.x,-gn.y,gn.x,0,-_n.y,_n.x,0,-zn.y,zn.x,0];return!aa(t,ci,li,ui,ur)||(t=[1,0,0,0,1,0,0,0,1],!aa(t,ci,li,ui,ur))?!1:(dr.crossVectors(gn,_n),t=[dr.x,dr.y,dr.z],aa(t,ci,li,ui,ur))}clampPoint(e,t){return t.copy(e).clamp(this.min,this.max)}distanceToPoint(e){return this.clampPoint(e,Xt).distanceTo(e)}getBoundingSphere(e){return this.isEmpty()?e.makeEmpty():(this.getCenter(e.center),e.radius=this.getSize(Xt).length()*.5),e}intersect(e){return this.min.max(e.min),this.max.min(e.max),this.isEmpty()&&this.makeEmpty(),this}union(e){return this.min.min(e.min),this.max.max(e.max),this}applyMatrix4(e){return this.isEmpty()?this:(nn[0].set(this.min.x,this.min.y,this.min.z).applyMatrix4(e),nn[1].set(this.min.x,this.min.y,this.max.z).applyMatrix4(e),nn[2].set(this.min.x,this.max.y,this.min.z).applyMatrix4(e),nn[3].set(this.min.x,this.max.y,this.max.z).applyMatrix4(e),nn[4].set(this.max.x,this.min.y,this.min.z).applyMatrix4(e),nn[5].set(this.max.x,this.min.y,this.max.z).applyMatrix4(e),nn[6].set(this.max.x,this.max.y,this.min.z).applyMatrix4(e),nn[7].set(this.max.x,this.max.y,this.max.z).applyMatrix4(e),this.setFromPoints(nn),this)}translate(e){return this.min.add(e),this.max.add(e),this}equals(e){return e.min.equals(this.min)&&e.max.equals(this.max)}}const nn=[new F,new F,new F,new F,new F,new F,new F,new F],Xt=new F,lr=new Oi,ci=new F,li=new F,ui=new F,gn=new F,_n=new F,zn=new F,ji=new F,ur=new F,dr=new F,Nn=new F;function aa(n,e,t,i,r){for(let a=0,s=n.length-3;a<=s;a+=3){Nn.fromArray(n,a);const o=r.x*Math.abs(Nn.x)+r.y*Math.abs(Nn.y)+r.z*Math.abs(Nn.z),c=e.dot(Nn),l=t.dot(Nn),d=i.dot(Nn);if(Math.max(-Math.max(c,l,d),Math.min(c,l,d))>o)return!1}return!0}const vu=new Oi,Wi=new F,sa=new F;class $r{constructor(e=new F,t=-1){this.isSphere=!0,this.center=e,this.radius=t}set(e,t){return this.center.copy(e),this.radius=t,this}setFromPoints(e,t){const i=this.center;t!==void 0?i.copy(t):vu.setFromPoints(e).getCenter(i);let r=0;for(let a=0,s=e.length;a<s;a++)r=Math.max(r,i.distanceToSquared(e[a]));return this.radius=Math.sqrt(r),this}copy(e){return this.center.copy(e.center),this.radius=e.radius,this}isEmpty(){return this.radius<0}makeEmpty(){return this.center.set(0,0,0),this.radius=-1,this}containsPoint(e){return e.distanceToSquared(this.center)<=this.radius*this.radius}distanceToPoint(e){return e.distanceTo(this.center)-this.radius}intersectsSphere(e){const t=this.radius+e.radius;return e.center.distanceToSquared(this.center)<=t*t}intersectsBox(e){return e.intersectsSphere(this)}intersectsPlane(e){return Math.abs(e.distanceToPoint(this.center))<=this.radius}clampPoint(e,t){const i=this.center.distanceToSquared(e);return t.copy(e),i>this.radius*this.radius&&(t.sub(this.center).normalize(),t.multiplyScalar(this.radius).add(this.center)),t}getBoundingBox(e){return this.isEmpty()?(e.makeEmpty(),e):(e.set(this.center,this.center),e.expandByScalar(this.radius),e)}applyMatrix4(e){return this.center.applyMatrix4(e),this.radius=this.radius*e.getMaxScaleOnAxis(),this}translate(e){return this.center.add(e),this}expandByPoint(e){if(this.isEmpty())return this.center.copy(e),this.radius=0,this;Wi.subVectors(e,this.center);const t=Wi.lengthSq();if(t>this.radius*this.radius){const i=Math.sqrt(t),r=(i-this.radius)*.5;this.center.addScaledVector(Wi,r/i),this.radius+=r}return this}union(e){return e.isEmpty()?this:this.isEmpty()?(this.copy(e),this):(this.center.equals(e.center)===!0?this.radius=Math.max(this.radius,e.radius):(sa.subVectors(e.center,this.center).setLength(e.radius),this.expandByPoint(Wi.copy(e.center).add(sa)),this.expandByPoint(Wi.copy(e.center).sub(sa))),this)}equals(e){return e.center.equals(this.center)&&e.radius===this.radius}clone(){return new this.constructor().copy(this)}}const rn=new F,oa=new F,hr=new F,vn=new F,ca=new F,fr=new F,la=new F;class Gs{constructor(e=new F,t=new F(0,0,-1)){this.origin=e,this.direction=t}set(e,t){return this.origin.copy(e),this.direction.copy(t),this}copy(e){return this.origin.copy(e.origin),this.direction.copy(e.direction),this}at(e,t){return t.copy(this.origin).addScaledVector(this.direction,e)}lookAt(e){return this.direction.copy(e).sub(this.origin).normalize(),this}recast(e){return this.origin.copy(this.at(e,rn)),this}closestPointToPoint(e,t){t.subVectors(e,this.origin);const i=t.dot(this.direction);return i<0?t.copy(this.origin):t.copy(this.origin).addScaledVector(this.direction,i)}distanceToPoint(e){return Math.sqrt(this.distanceSqToPoint(e))}distanceSqToPoint(e){const t=rn.subVectors(e,this.origin).dot(this.direction);return t<0?this.origin.distanceToSquared(e):(rn.copy(this.origin).addScaledVector(this.direction,t),rn.distanceToSquared(e))}distanceSqToSegment(e,t,i,r){oa.copy(e).add(t).multiplyScalar(.5),hr.copy(t).sub(e).normalize(),vn.copy(this.origin).sub(oa);const a=e.distanceTo(t)*.5,s=-this.direction.dot(hr),o=vn.dot(this.direction),c=-vn.dot(hr),l=vn.lengthSq(),d=Math.abs(1-s*s);let h,f,m,g;if(d>0)if(h=s*c-o,f=s*o-c,g=a*d,h>=0)if(f>=-g)if(f<=g){const _=1/d;h*=_,f*=_,m=h*(h+s*f+2*o)+f*(s*h+f+2*c)+l}else f=a,h=Math.max(0,-(s*f+o)),m=-h*h+f*(f+2*c)+l;else f=-a,h=Math.max(0,-(s*f+o)),m=-h*h+f*(f+2*c)+l;else f<=-g?(h=Math.max(0,-(-s*a+o)),f=h>0?-a:Math.min(Math.max(-a,-c),a),m=-h*h+f*(f+2*c)+l):f<=g?(h=0,f=Math.min(Math.max(-a,-c),a),m=f*(f+2*c)+l):(h=Math.max(0,-(s*a+o)),f=h>0?a:Math.min(Math.max(-a,-c),a),m=-h*h+f*(f+2*c)+l);else f=s>0?-a:a,h=Math.max(0,-(s*f+o)),m=-h*h+f*(f+2*c)+l;return i&&i.copy(this.origin).addScaledVector(this.direction,h),r&&r.copy(oa).addScaledVector(hr,f),m}intersectSphere(e,t){rn.subVectors(e.center,this.origin);const i=rn.dot(this.direction),r=rn.dot(rn)-i*i,a=e.radius*e.radius;if(r>a)return null;const s=Math.sqrt(a-r),o=i-s,c=i+s;return c<0?null:o<0?this.at(c,t):this.at(o,t)}intersectsSphere(e){return this.distanceSqToPoint(e.center)<=e.radius*e.radius}distanceToPlane(e){const t=e.normal.dot(this.direction);if(t===0)return e.distanceToPoint(this.origin)===0?0:null;const i=-(this.origin.dot(e.normal)+e.constant)/t;return i>=0?i:null}intersectPlane(e,t){const i=this.distanceToPlane(e);return i===null?null:this.at(i,t)}intersectsPlane(e){const t=e.distanceToPoint(this.origin);return t===0||e.normal.dot(this.direction)*t<0}intersectBox(e,t){let i,r,a,s,o,c;const l=1/this.direction.x,d=1/this.direction.y,h=1/this.direction.z,f=this.origin;return l>=0?(i=(e.min.x-f.x)*l,r=(e.max.x-f.x)*l):(i=(e.max.x-f.x)*l,r=(e.min.x-f.x)*l),d>=0?(a=(e.min.y-f.y)*d,s=(e.max.y-f.y)*d):(a=(e.max.y-f.y)*d,s=(e.min.y-f.y)*d),i>s||a>r||((a>i||isNaN(i))&&(i=a),(s<r||isNaN(r))&&(r=s),h>=0?(o=(e.min.z-f.z)*h,c=(e.max.z-f.z)*h):(o=(e.max.z-f.z)*h,c=(e.min.z-f.z)*h),i>c||o>r)||((o>i||i!==i)&&(i=o),(c<r||r!==r)&&(r=c),r<0)?null:this.at(i>=0?i:r,t)}intersectsBox(e){return this.intersectBox(e,rn)!==null}intersectTriangle(e,t,i,r,a){ca.subVectors(t,e),fr.subVectors(i,e),la.crossVectors(ca,fr);let s=this.direction.dot(la),o;if(s>0){if(r)return null;o=1}else if(s<0)o=-1,s=-s;else return null;vn.subVectors(this.origin,e);const c=o*this.direction.dot(fr.crossVectors(vn,fr));if(c<0)return null;const l=o*this.direction.dot(ca.cross(vn));if(l<0||c+l>s)return null;const d=-o*vn.dot(la);return d<0?null:this.at(d/s,a)}applyMatrix4(e){return this.origin.applyMatrix4(e),this.direction.transformDirection(e),this}equals(e){return e.origin.equals(this.origin)&&e.direction.equals(this.direction)}clone(){return new this.constructor().copy(this)}}class at{constructor(e,t,i,r,a,s,o,c,l,d,h,f,m,g,_,p){at.prototype.isMatrix4=!0,this.elements=[1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1],e!==void 0&&this.set(e,t,i,r,a,s,o,c,l,d,h,f,m,g,_,p)}set(e,t,i,r,a,s,o,c,l,d,h,f,m,g,_,p){const u=this.elements;return u[0]=e,u[4]=t,u[8]=i,u[12]=r,u[1]=a,u[5]=s,u[9]=o,u[13]=c,u[2]=l,u[6]=d,u[10]=h,u[14]=f,u[3]=m,u[7]=g,u[11]=_,u[15]=p,this}identity(){return this.set(1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1),this}clone(){return new at().fromArray(this.elements)}copy(e){const t=this.elements,i=e.elements;return t[0]=i[0],t[1]=i[1],t[2]=i[2],t[3]=i[3],t[4]=i[4],t[5]=i[5],t[6]=i[6],t[7]=i[7],t[8]=i[8],t[9]=i[9],t[10]=i[10],t[11]=i[11],t[12]=i[12],t[13]=i[13],t[14]=i[14],t[15]=i[15],this}copyPosition(e){const t=this.elements,i=e.elements;return t[12]=i[12],t[13]=i[13],t[14]=i[14],this}setFromMatrix3(e){const t=e.elements;return this.set(t[0],t[3],t[6],0,t[1],t[4],t[7],0,t[2],t[5],t[8],0,0,0,0,1),this}extractBasis(e,t,i){return e.setFromMatrixColumn(this,0),t.setFromMatrixColumn(this,1),i.setFromMatrixColumn(this,2),this}makeBasis(e,t,i){return this.set(e.x,t.x,i.x,0,e.y,t.y,i.y,0,e.z,t.z,i.z,0,0,0,0,1),this}extractRotation(e){const t=this.elements,i=e.elements,r=1/di.setFromMatrixColumn(e,0).length(),a=1/di.setFromMatrixColumn(e,1).length(),s=1/di.setFromMatrixColumn(e,2).length();return t[0]=i[0]*r,t[1]=i[1]*r,t[2]=i[2]*r,t[3]=0,t[4]=i[4]*a,t[5]=i[5]*a,t[6]=i[6]*a,t[7]=0,t[8]=i[8]*s,t[9]=i[9]*s,t[10]=i[10]*s,t[11]=0,t[12]=0,t[13]=0,t[14]=0,t[15]=1,this}makeRotationFromEuler(e){const t=this.elements,i=e.x,r=e.y,a=e.z,s=Math.cos(i),o=Math.sin(i),c=Math.cos(r),l=Math.sin(r),d=Math.cos(a),h=Math.sin(a);if(e.order==="XYZ"){const f=s*d,m=s*h,g=o*d,_=o*h;t[0]=c*d,t[4]=-c*h,t[8]=l,t[1]=m+g*l,t[5]=f-_*l,t[9]=-o*c,t[2]=_-f*l,t[6]=g+m*l,t[10]=s*c}else if(e.order==="YXZ"){const f=c*d,m=c*h,g=l*d,_=l*h;t[0]=f+_*o,t[4]=g*o-m,t[8]=s*l,t[1]=s*h,t[5]=s*d,t[9]=-o,t[2]=m*o-g,t[6]=_+f*o,t[10]=s*c}else if(e.order==="ZXY"){const f=c*d,m=c*h,g=l*d,_=l*h;t[0]=f-_*o,t[4]=-s*h,t[8]=g+m*o,t[1]=m+g*o,t[5]=s*d,t[9]=_-f*o,t[2]=-s*l,t[6]=o,t[10]=s*c}else if(e.order==="ZYX"){const f=s*d,m=s*h,g=o*d,_=o*h;t[0]=c*d,t[4]=g*l-m,t[8]=f*l+_,t[1]=c*h,t[5]=_*l+f,t[9]=m*l-g,t[2]=-l,t[6]=o*c,t[10]=s*c}else if(e.order==="YZX"){const f=s*c,m=s*l,g=o*c,_=o*l;t[0]=c*d,t[4]=_-f*h,t[8]=g*h+m,t[1]=h,t[5]=s*d,t[9]=-o*d,t[2]=-l*d,t[6]=m*h+g,t[10]=f-_*h}else if(e.order==="XZY"){const f=s*c,m=s*l,g=o*c,_=o*l;t[0]=c*d,t[4]=-h,t[8]=l*d,t[1]=f*h+_,t[5]=s*d,t[9]=m*h-g,t[2]=g*h-m,t[6]=o*d,t[10]=_*h+f}return t[3]=0,t[7]=0,t[11]=0,t[12]=0,t[13]=0,t[14]=0,t[15]=1,this}makeRotationFromQuaternion(e){return this.compose(xu,e,Mu)}lookAt(e,t,i){const r=this.elements;return Ut.subVectors(e,t),Ut.lengthSq()===0&&(Ut.z=1),Ut.normalize(),xn.crossVectors(i,Ut),xn.lengthSq()===0&&(Math.abs(i.z)===1?Ut.x+=1e-4:Ut.z+=1e-4,Ut.normalize(),xn.crossVectors(i,Ut)),xn.normalize(),pr.crossVectors(Ut,xn),r[0]=xn.x,r[4]=pr.x,r[8]=Ut.x,r[1]=xn.y,r[5]=pr.y,r[9]=Ut.y,r[2]=xn.z,r[6]=pr.z,r[10]=Ut.z,this}multiply(e){return this.multiplyMatrices(this,e)}premultiply(e){return this.multiplyMatrices(e,this)}multiplyMatrices(e,t){const i=e.elements,r=t.elements,a=this.elements,s=i[0],o=i[4],c=i[8],l=i[12],d=i[1],h=i[5],f=i[9],m=i[13],g=i[2],_=i[6],p=i[10],u=i[14],E=i[3],y=i[7],M=i[11],D=i[15],A=r[0],b=r[4],C=r[8],v=r[12],x=r[1],P=r[5],U=r[9],w=r[13],R=r[2],z=r[6],N=r[10],B=r[14],k=r[3],O=r[7],q=r[11],K=r[15];return a[0]=s*A+o*x+c*R+l*k,a[4]=s*b+o*P+c*z+l*O,a[8]=s*C+o*U+c*N+l*q,a[12]=s*v+o*w+c*B+l*K,a[1]=d*A+h*x+f*R+m*k,a[5]=d*b+h*P+f*z+m*O,a[9]=d*C+h*U+f*N+m*q,a[13]=d*v+h*w+f*B+m*K,a[2]=g*A+_*x+p*R+u*k,a[6]=g*b+_*P+p*z+u*O,a[10]=g*C+_*U+p*N+u*q,a[14]=g*v+_*w+p*B+u*K,a[3]=E*A+y*x+M*R+D*k,a[7]=E*b+y*P+M*z+D*O,a[11]=E*C+y*U+M*N+D*q,a[15]=E*v+y*w+M*B+D*K,this}multiplyScalar(e){const t=this.elements;return t[0]*=e,t[4]*=e,t[8]*=e,t[12]*=e,t[1]*=e,t[5]*=e,t[9]*=e,t[13]*=e,t[2]*=e,t[6]*=e,t[10]*=e,t[14]*=e,t[3]*=e,t[7]*=e,t[11]*=e,t[15]*=e,this}determinant(){const e=this.elements,t=e[0],i=e[4],r=e[8],a=e[12],s=e[1],o=e[5],c=e[9],l=e[13],d=e[2],h=e[6],f=e[10],m=e[14],g=e[3],_=e[7],p=e[11],u=e[15];return g*(+a*c*h-r*l*h-a*o*f+i*l*f+r*o*m-i*c*m)+_*(+t*c*m-t*l*f+a*s*f-r*s*m+r*l*d-a*c*d)+p*(+t*l*h-t*o*m-a*s*h+i*s*m+a*o*d-i*l*d)+u*(-r*o*d-t*c*h+t*o*f+r*s*h-i*s*f+i*c*d)}transpose(){const e=this.elements;let t;return t=e[1],e[1]=e[4],e[4]=t,t=e[2],e[2]=e[8],e[8]=t,t=e[6],e[6]=e[9],e[9]=t,t=e[3],e[3]=e[12],e[12]=t,t=e[7],e[7]=e[13],e[13]=t,t=e[11],e[11]=e[14],e[14]=t,this}setPosition(e,t,i){const r=this.elements;return e.isVector3?(r[12]=e.x,r[13]=e.y,r[14]=e.z):(r[12]=e,r[13]=t,r[14]=i),this}invert(){const e=this.elements,t=e[0],i=e[1],r=e[2],a=e[3],s=e[4],o=e[5],c=e[6],l=e[7],d=e[8],h=e[9],f=e[10],m=e[11],g=e[12],_=e[13],p=e[14],u=e[15],E=h*p*l-_*f*l+_*c*m-o*p*m-h*c*u+o*f*u,y=g*f*l-d*p*l-g*c*m+s*p*m+d*c*u-s*f*u,M=d*_*l-g*h*l+g*o*m-s*_*m-d*o*u+s*h*u,D=g*h*c-d*_*c-g*o*f+s*_*f+d*o*p-s*h*p,A=t*E+i*y+r*M+a*D;if(A===0)return this.set(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);const b=1/A;return e[0]=E*b,e[1]=(_*f*a-h*p*a-_*r*m+i*p*m+h*r*u-i*f*u)*b,e[2]=(o*p*a-_*c*a+_*r*l-i*p*l-o*r*u+i*c*u)*b,e[3]=(h*c*a-o*f*a-h*r*l+i*f*l+o*r*m-i*c*m)*b,e[4]=y*b,e[5]=(d*p*a-g*f*a+g*r*m-t*p*m-d*r*u+t*f*u)*b,e[6]=(g*c*a-s*p*a-g*r*l+t*p*l+s*r*u-t*c*u)*b,e[7]=(s*f*a-d*c*a+d*r*l-t*f*l-s*r*m+t*c*m)*b,e[8]=M*b,e[9]=(g*h*a-d*_*a-g*i*m+t*_*m+d*i*u-t*h*u)*b,e[10]=(s*_*a-g*o*a+g*i*l-t*_*l-s*i*u+t*o*u)*b,e[11]=(d*o*a-s*h*a-d*i*l+t*h*l+s*i*m-t*o*m)*b,e[12]=D*b,e[13]=(d*_*r-g*h*r+g*i*f-t*_*f-d*i*p+t*h*p)*b,e[14]=(g*o*r-s*_*r-g*i*c+t*_*c+s*i*p-t*o*p)*b,e[15]=(s*h*r-d*o*r+d*i*c-t*h*c-s*i*f+t*o*f)*b,this}scale(e){const t=this.elements,i=e.x,r=e.y,a=e.z;return t[0]*=i,t[4]*=r,t[8]*=a,t[1]*=i,t[5]*=r,t[9]*=a,t[2]*=i,t[6]*=r,t[10]*=a,t[3]*=i,t[7]*=r,t[11]*=a,this}getMaxScaleOnAxis(){const e=this.elements,t=e[0]*e[0]+e[1]*e[1]+e[2]*e[2],i=e[4]*e[4]+e[5]*e[5]+e[6]*e[6],r=e[8]*e[8]+e[9]*e[9]+e[10]*e[10];return Math.sqrt(Math.max(t,i,r))}makeTranslation(e,t,i){return e.isVector3?this.set(1,0,0,e.x,0,1,0,e.y,0,0,1,e.z,0,0,0,1):this.set(1,0,0,e,0,1,0,t,0,0,1,i,0,0,0,1),this}makeRotationX(e){const t=Math.cos(e),i=Math.sin(e);return this.set(1,0,0,0,0,t,-i,0,0,i,t,0,0,0,0,1),this}makeRotationY(e){const t=Math.cos(e),i=Math.sin(e);return this.set(t,0,i,0,0,1,0,0,-i,0,t,0,0,0,0,1),this}makeRotationZ(e){const t=Math.cos(e),i=Math.sin(e);return this.set(t,-i,0,0,i,t,0,0,0,0,1,0,0,0,0,1),this}makeRotationAxis(e,t){const i=Math.cos(t),r=Math.sin(t),a=1-i,s=e.x,o=e.y,c=e.z,l=a*s,d=a*o;return this.set(l*s+i,l*o-r*c,l*c+r*o,0,l*o+r*c,d*o+i,d*c-r*s,0,l*c-r*o,d*c+r*s,a*c*c+i,0,0,0,0,1),this}makeScale(e,t,i){return this.set(e,0,0,0,0,t,0,0,0,0,i,0,0,0,0,1),this}makeShear(e,t,i,r,a,s){return this.set(1,i,a,0,e,1,s,0,t,r,1,0,0,0,0,1),this}compose(e,t,i){const r=this.elements,a=t._x,s=t._y,o=t._z,c=t._w,l=a+a,d=s+s,h=o+o,f=a*l,m=a*d,g=a*h,_=s*d,p=s*h,u=o*h,E=c*l,y=c*d,M=c*h,D=i.x,A=i.y,b=i.z;return r[0]=(1-(_+u))*D,r[1]=(m+M)*D,r[2]=(g-y)*D,r[3]=0,r[4]=(m-M)*A,r[5]=(1-(f+u))*A,r[6]=(p+E)*A,r[7]=0,r[8]=(g+y)*b,r[9]=(p-E)*b,r[10]=(1-(f+_))*b,r[11]=0,r[12]=e.x,r[13]=e.y,r[14]=e.z,r[15]=1,this}decompose(e,t,i){const r=this.elements;let a=di.set(r[0],r[1],r[2]).length();const s=di.set(r[4],r[5],r[6]).length(),o=di.set(r[8],r[9],r[10]).length();this.determinant()<0&&(a=-a),e.x=r[12],e.y=r[13],e.z=r[14],qt.copy(this);const l=1/a,d=1/s,h=1/o;return qt.elements[0]*=l,qt.elements[1]*=l,qt.elements[2]*=l,qt.elements[4]*=d,qt.elements[5]*=d,qt.elements[6]*=d,qt.elements[8]*=h,qt.elements[9]*=h,qt.elements[10]*=h,t.setFromRotationMatrix(qt),i.x=a,i.y=s,i.z=o,this}makePerspective(e,t,i,r,a,s,o=fn){const c=this.elements,l=2*a/(t-e),d=2*a/(i-r),h=(t+e)/(t-e),f=(i+r)/(i-r);let m,g;if(o===fn)m=-(s+a)/(s-a),g=-2*s*a/(s-a);else if(o===jr)m=-s/(s-a),g=-s*a/(s-a);else throw new Error("THREE.Matrix4.makePerspective(): Invalid coordinate system: "+o);return c[0]=l,c[4]=0,c[8]=h,c[12]=0,c[1]=0,c[5]=d,c[9]=f,c[13]=0,c[2]=0,c[6]=0,c[10]=m,c[14]=g,c[3]=0,c[7]=0,c[11]=-1,c[15]=0,this}makeOrthographic(e,t,i,r,a,s,o=fn){const c=this.elements,l=1/(t-e),d=1/(i-r),h=1/(s-a),f=(t+e)*l,m=(i+r)*d;let g,_;if(o===fn)g=(s+a)*h,_=-2*h;else if(o===jr)g=a*h,_=-1*h;else throw new Error("THREE.Matrix4.makeOrthographic(): Invalid coordinate system: "+o);return c[0]=2*l,c[4]=0,c[8]=0,c[12]=-f,c[1]=0,c[5]=2*d,c[9]=0,c[13]=-m,c[2]=0,c[6]=0,c[10]=_,c[14]=-g,c[3]=0,c[7]=0,c[11]=0,c[15]=1,this}equals(e){const t=this.elements,i=e.elements;for(let r=0;r<16;r++)if(t[r]!==i[r])return!1;return!0}fromArray(e,t=0){for(let i=0;i<16;i++)this.elements[i]=e[i+t];return this}toArray(e=[],t=0){const i=this.elements;return e[t]=i[0],e[t+1]=i[1],e[t+2]=i[2],e[t+3]=i[3],e[t+4]=i[4],e[t+5]=i[5],e[t+6]=i[6],e[t+7]=i[7],e[t+8]=i[8],e[t+9]=i[9],e[t+10]=i[10],e[t+11]=i[11],e[t+12]=i[12],e[t+13]=i[13],e[t+14]=i[14],e[t+15]=i[15],e}}const di=new F,qt=new at,xu=new F(0,0,0),Mu=new F(1,1,1),xn=new F,pr=new F,Ut=new F,So=new at,Eo=new Fi;class xt{constructor(e=0,t=0,i=0,r=xt.DEFAULT_ORDER){this.isEuler=!0,this._x=e,this._y=t,this._z=i,this._order=r}get x(){return this._x}set x(e){this._x=e,this._onChangeCallback()}get y(){return this._y}set y(e){this._y=e,this._onChangeCallback()}get z(){return this._z}set z(e){this._z=e,this._onChangeCallback()}get order(){return this._order}set order(e){this._order=e,this._onChangeCallback()}set(e,t,i,r=this._order){return this._x=e,this._y=t,this._z=i,this._order=r,this._onChangeCallback(),this}clone(){return new this.constructor(this._x,this._y,this._z,this._order)}copy(e){return this._x=e._x,this._y=e._y,this._z=e._z,this._order=e._order,this._onChangeCallback(),this}setFromRotationMatrix(e,t=this._order,i=!0){const r=e.elements,a=r[0],s=r[4],o=r[8],c=r[1],l=r[5],d=r[9],h=r[2],f=r[6],m=r[10];switch(t){case"XYZ":this._y=Math.asin(qe(o,-1,1)),Math.abs(o)<.9999999?(this._x=Math.atan2(-d,m),this._z=Math.atan2(-s,a)):(this._x=Math.atan2(f,l),this._z=0);break;case"YXZ":this._x=Math.asin(-qe(d,-1,1)),Math.abs(d)<.9999999?(this._y=Math.atan2(o,m),this._z=Math.atan2(c,l)):(this._y=Math.atan2(-h,a),this._z=0);break;case"ZXY":this._x=Math.asin(qe(f,-1,1)),Math.abs(f)<.9999999?(this._y=Math.atan2(-h,m),this._z=Math.atan2(-s,l)):(this._y=0,this._z=Math.atan2(c,a));break;case"ZYX":this._y=Math.asin(-qe(h,-1,1)),Math.abs(h)<.9999999?(this._x=Math.atan2(f,m),this._z=Math.atan2(c,a)):(this._x=0,this._z=Math.atan2(-s,l));break;case"YZX":this._z=Math.asin(qe(c,-1,1)),Math.abs(c)<.9999999?(this._x=Math.atan2(-d,l),this._y=Math.atan2(-h,a)):(this._x=0,this._y=Math.atan2(o,m));break;case"XZY":this._z=Math.asin(-qe(s,-1,1)),Math.abs(s)<.9999999?(this._x=Math.atan2(f,l),this._y=Math.atan2(o,a)):(this._x=Math.atan2(-d,m),this._y=0);break;default:console.warn("THREE.Euler: .setFromRotationMatrix() encountered an unknown order: "+t)}return this._order=t,i===!0&&this._onChangeCallback(),this}setFromQuaternion(e,t,i){return So.makeRotationFromQuaternion(e),this.setFromRotationMatrix(So,t,i)}setFromVector3(e,t=this._order){return this.set(e.x,e.y,e.z,t)}reorder(e){return Eo.setFromEuler(this),this.setFromQuaternion(Eo,e)}equals(e){return e._x===this._x&&e._y===this._y&&e._z===this._z&&e._order===this._order}fromArray(e){return this._x=e[0],this._y=e[1],this._z=e[2],e[3]!==void 0&&(this._order=e[3]),this._onChangeCallback(),this}toArray(e=[],t=0){return e[t]=this._x,e[t+1]=this._y,e[t+2]=this._z,e[t+3]=this._order,e}_onChange(e){return this._onChangeCallback=e,this}_onChangeCallback(){}*[Symbol.iterator](){yield this._x,yield this._y,yield this._z,yield this._order}}xt.DEFAULT_ORDER="XYZ";class Hs{constructor(){this.mask=1}set(e){this.mask=(1<<e|0)>>>0}enable(e){this.mask|=1<<e|0}enableAll(){this.mask=-1}toggle(e){this.mask^=1<<e|0}disable(e){this.mask&=~(1<<e|0)}disableAll(){this.mask=0}test(e){return(this.mask&e.mask)!==0}isEnabled(e){return(this.mask&(1<<e|0))!==0}}let Su=0;const yo=new F,hi=new Fi,an=new at,mr=new F,Xi=new F,Eu=new F,yu=new Fi,bo=new F(1,0,0),To=new F(0,1,0),wo=new F(0,0,1),Ao={type:"added"},bu={type:"removed"},fi={type:"childadded",child:null},ua={type:"childremoved",child:null};class Et extends ki{constructor(){super(),this.isObject3D=!0,Object.defineProperty(this,"id",{value:Su++}),this.uuid=rr(),this.name="",this.type="Object3D",this.parent=null,this.children=[],this.up=Et.DEFAULT_UP.clone();const e=new F,t=new xt,i=new Fi,r=new F(1,1,1);function a(){i.setFromEuler(t,!1)}function s(){t.setFromQuaternion(i,void 0,!1)}t._onChange(a),i._onChange(s),Object.defineProperties(this,{position:{configurable:!0,enumerable:!0,value:e},rotation:{configurable:!0,enumerable:!0,value:t},quaternion:{configurable:!0,enumerable:!0,value:i},scale:{configurable:!0,enumerable:!0,value:r},modelViewMatrix:{value:new at},normalMatrix:{value:new Ve}}),this.matrix=new at,this.matrixWorld=new at,this.matrixAutoUpdate=Et.DEFAULT_MATRIX_AUTO_UPDATE,this.matrixWorldAutoUpdate=Et.DEFAULT_MATRIX_WORLD_AUTO_UPDATE,this.matrixWorldNeedsUpdate=!1,this.layers=new Hs,this.visible=!0,this.castShadow=!1,this.receiveShadow=!1,this.frustumCulled=!0,this.renderOrder=0,this.animations=[],this.userData={}}onBeforeShadow(){}onAfterShadow(){}onBeforeRender(){}onAfterRender(){}applyMatrix4(e){this.matrixAutoUpdate&&this.updateMatrix(),this.matrix.premultiply(e),this.matrix.decompose(this.position,this.quaternion,this.scale)}applyQuaternion(e){return this.quaternion.premultiply(e),this}setRotationFromAxisAngle(e,t){this.quaternion.setFromAxisAngle(e,t)}setRotationFromEuler(e){this.quaternion.setFromEuler(e,!0)}setRotationFromMatrix(e){this.quaternion.setFromRotationMatrix(e)}setRotationFromQuaternion(e){this.quaternion.copy(e)}rotateOnAxis(e,t){return hi.setFromAxisAngle(e,t),this.quaternion.multiply(hi),this}rotateOnWorldAxis(e,t){return hi.setFromAxisAngle(e,t),this.quaternion.premultiply(hi),this}rotateX(e){return this.rotateOnAxis(bo,e)}rotateY(e){return this.rotateOnAxis(To,e)}rotateZ(e){return this.rotateOnAxis(wo,e)}translateOnAxis(e,t){return yo.copy(e).applyQuaternion(this.quaternion),this.position.add(yo.multiplyScalar(t)),this}translateX(e){return this.translateOnAxis(bo,e)}translateY(e){return this.translateOnAxis(To,e)}translateZ(e){return this.translateOnAxis(wo,e)}localToWorld(e){return this.updateWorldMatrix(!0,!1),e.applyMatrix4(this.matrixWorld)}worldToLocal(e){return this.updateWorldMatrix(!0,!1),e.applyMatrix4(an.copy(this.matrixWorld).invert())}lookAt(e,t,i){e.isVector3?mr.copy(e):mr.set(e,t,i);const r=this.parent;this.updateWorldMatrix(!0,!1),Xi.setFromMatrixPosition(this.matrixWorld),this.isCamera||this.isLight?an.lookAt(Xi,mr,this.up):an.lookAt(mr,Xi,this.up),this.quaternion.setFromRotationMatrix(an),r&&(an.extractRotation(r.matrixWorld),hi.setFromRotationMatrix(an),this.quaternion.premultiply(hi.invert()))}add(e){if(arguments.length>1){for(let t=0;t<arguments.length;t++)this.add(arguments[t]);return this}return e===this?(console.error("THREE.Object3D.add: object can't be added as a child of itself.",e),this):(e&&e.isObject3D?(e.removeFromParent(),e.parent=this,this.children.push(e),e.dispatchEvent(Ao),fi.child=e,this.dispatchEvent(fi),fi.child=null):console.error("THREE.Object3D.add: object not an instance of THREE.Object3D.",e),this)}remove(e){if(arguments.length>1){for(let i=0;i<arguments.length;i++)this.remove(arguments[i]);return this}const t=this.children.indexOf(e);return t!==-1&&(e.parent=null,this.children.splice(t,1),e.dispatchEvent(bu),ua.child=e,this.dispatchEvent(ua),ua.child=null),this}removeFromParent(){const e=this.parent;return e!==null&&e.remove(this),this}clear(){return this.remove(...this.children)}attach(e){return this.updateWorldMatrix(!0,!1),an.copy(this.matrixWorld).invert(),e.parent!==null&&(e.parent.updateWorldMatrix(!0,!1),an.multiply(e.parent.matrixWorld)),e.applyMatrix4(an),e.removeFromParent(),e.parent=this,this.children.push(e),e.updateWorldMatrix(!1,!0),e.dispatchEvent(Ao),fi.child=e,this.dispatchEvent(fi),fi.child=null,this}getObjectById(e){return this.getObjectByProperty("id",e)}getObjectByName(e){return this.getObjectByProperty("name",e)}getObjectByProperty(e,t){if(this[e]===t)return this;for(let i=0,r=this.children.length;i<r;i++){const s=this.children[i].getObjectByProperty(e,t);if(s!==void 0)return s}}getObjectsByProperty(e,t,i=[]){this[e]===t&&i.push(this);const r=this.children;for(let a=0,s=r.length;a<s;a++)r[a].getObjectsByProperty(e,t,i);return i}getWorldPosition(e){return this.updateWorldMatrix(!0,!1),e.setFromMatrixPosition(this.matrixWorld)}getWorldQuaternion(e){return this.updateWorldMatrix(!0,!1),this.matrixWorld.decompose(Xi,e,Eu),e}getWorldScale(e){return this.updateWorldMatrix(!0,!1),this.matrixWorld.decompose(Xi,yu,e),e}getWorldDirection(e){this.updateWorldMatrix(!0,!1);const t=this.matrixWorld.elements;return e.set(t[8],t[9],t[10]).normalize()}raycast(){}traverse(e){e(this);const t=this.children;for(let i=0,r=t.length;i<r;i++)t[i].traverse(e)}traverseVisible(e){if(this.visible===!1)return;e(this);const t=this.children;for(let i=0,r=t.length;i<r;i++)t[i].traverseVisible(e)}traverseAncestors(e){const t=this.parent;t!==null&&(e(t),t.traverseAncestors(e))}updateMatrix(){this.matrix.compose(this.position,this.quaternion,this.scale),this.matrixWorldNeedsUpdate=!0}updateMatrixWorld(e){this.matrixAutoUpdate&&this.updateMatrix(),(this.matrixWorldNeedsUpdate||e)&&(this.matrixWorldAutoUpdate===!0&&(this.parent===null?this.matrixWorld.copy(this.matrix):this.matrixWorld.multiplyMatrices(this.parent.matrixWorld,this.matrix)),this.matrixWorldNeedsUpdate=!1,e=!0);const t=this.children;for(let i=0,r=t.length;i<r;i++)t[i].updateMatrixWorld(e)}updateWorldMatrix(e,t){const i=this.parent;if(e===!0&&i!==null&&i.updateWorldMatrix(!0,!1),this.matrixAutoUpdate&&this.updateMatrix(),this.matrixWorldAutoUpdate===!0&&(this.parent===null?this.matrixWorld.copy(this.matrix):this.matrixWorld.multiplyMatrices(this.parent.matrixWorld,this.matrix)),t===!0){const r=this.children;for(let a=0,s=r.length;a<s;a++)r[a].updateWorldMatrix(!1,!0)}}toJSON(e){const t=e===void 0||typeof e=="string",i={};t&&(e={geometries:{},materials:{},textures:{},images:{},shapes:{},skeletons:{},animations:{},nodes:{}},i.metadata={version:4.6,type:"Object",generator:"Object3D.toJSON"});const r={};r.uuid=this.uuid,r.type=this.type,this.name!==""&&(r.name=this.name),this.castShadow===!0&&(r.castShadow=!0),this.receiveShadow===!0&&(r.receiveShadow=!0),this.visible===!1&&(r.visible=!1),this.frustumCulled===!1&&(r.frustumCulled=!1),this.renderOrder!==0&&(r.renderOrder=this.renderOrder),Object.keys(this.userData).length>0&&(r.userData=this.userData),r.layers=this.layers.mask,r.matrix=this.matrix.toArray(),r.up=this.up.toArray(),this.matrixAutoUpdate===!1&&(r.matrixAutoUpdate=!1),this.isInstancedMesh&&(r.type="InstancedMesh",r.count=this.count,r.instanceMatrix=this.instanceMatrix.toJSON(),this.instanceColor!==null&&(r.instanceColor=this.instanceColor.toJSON())),this.isBatchedMesh&&(r.type="BatchedMesh",r.perObjectFrustumCulled=this.perObjectFrustumCulled,r.sortObjects=this.sortObjects,r.drawRanges=this._drawRanges,r.reservedRanges=this._reservedRanges,r.visibility=this._visibility,r.active=this._active,r.bounds=this._bounds.map(o=>({boxInitialized:o.boxInitialized,boxMin:o.box.min.toArray(),boxMax:o.box.max.toArray(),sphereInitialized:o.sphereInitialized,sphereRadius:o.sphere.radius,sphereCenter:o.sphere.center.toArray()})),r.maxInstanceCount=this._maxInstanceCount,r.maxVertexCount=this._maxVertexCount,r.maxIndexCount=this._maxIndexCount,r.geometryInitialized=this._geometryInitialized,r.geometryCount=this._geometryCount,r.matricesTexture=this._matricesTexture.toJSON(e),this._colorsTexture!==null&&(r.colorsTexture=this._colorsTexture.toJSON(e)),this.boundingSphere!==null&&(r.boundingSphere={center:r.boundingSphere.center.toArray(),radius:r.boundingSphere.radius}),this.boundingBox!==null&&(r.boundingBox={min:r.boundingBox.min.toArray(),max:r.boundingBox.max.toArray()}));function a(o,c){return o[c.uuid]===void 0&&(o[c.uuid]=c.toJSON(e)),c.uuid}if(this.isScene)this.background&&(this.background.isColor?r.background=this.background.toJSON():this.background.isTexture&&(r.background=this.background.toJSON(e).uuid)),this.environment&&this.environment.isTexture&&this.environment.isRenderTargetTexture!==!0&&(r.environment=this.environment.toJSON(e).uuid);else if(this.isMesh||this.isLine||this.isPoints){r.geometry=a(e.geometries,this.geometry);const o=this.geometry.parameters;if(o!==void 0&&o.shapes!==void 0){const c=o.shapes;if(Array.isArray(c))for(let l=0,d=c.length;l<d;l++){const h=c[l];a(e.shapes,h)}else a(e.shapes,c)}}if(this.isSkinnedMesh&&(r.bindMode=this.bindMode,r.bindMatrix=this.bindMatrix.toArray(),this.skeleton!==void 0&&(a(e.skeletons,this.skeleton),r.skeleton=this.skeleton.uuid)),this.material!==void 0)if(Array.isArray(this.material)){const o=[];for(let c=0,l=this.material.length;c<l;c++)o.push(a(e.materials,this.material[c]));r.material=o}else r.material=a(e.materials,this.material);if(this.children.length>0){r.children=[];for(let o=0;o<this.children.length;o++)r.children.push(this.children[o].toJSON(e).object)}if(this.animations.length>0){r.animations=[];for(let o=0;o<this.animations.length;o++){const c=this.animations[o];r.animations.push(a(e.animations,c))}}if(t){const o=s(e.geometries),c=s(e.materials),l=s(e.textures),d=s(e.images),h=s(e.shapes),f=s(e.skeletons),m=s(e.animations),g=s(e.nodes);o.length>0&&(i.geometries=o),c.length>0&&(i.materials=c),l.length>0&&(i.textures=l),d.length>0&&(i.images=d),h.length>0&&(i.shapes=h),f.length>0&&(i.skeletons=f),m.length>0&&(i.animations=m),g.length>0&&(i.nodes=g)}return i.object=r,i;function s(o){const c=[];for(const l in o){const d=o[l];delete d.metadata,c.push(d)}return c}}clone(e){return new this.constructor().copy(this,e)}copy(e,t=!0){if(this.name=e.name,this.up.copy(e.up),this.position.copy(e.position),this.rotation.order=e.rotation.order,this.quaternion.copy(e.quaternion),this.scale.copy(e.scale),this.matrix.copy(e.matrix),this.matrixWorld.copy(e.matrixWorld),this.matrixAutoUpdate=e.matrixAutoUpdate,this.matrixWorldAutoUpdate=e.matrixWorldAutoUpdate,this.matrixWorldNeedsUpdate=e.matrixWorldNeedsUpdate,this.layers.mask=e.layers.mask,this.visible=e.visible,this.castShadow=e.castShadow,this.receiveShadow=e.receiveShadow,this.frustumCulled=e.frustumCulled,this.renderOrder=e.renderOrder,this.animations=e.animations.slice(),this.userData=JSON.parse(JSON.stringify(e.userData)),t===!0)for(let i=0;i<e.children.length;i++){const r=e.children[i];this.add(r.clone())}return this}}Et.DEFAULT_UP=new F(0,1,0);Et.DEFAULT_MATRIX_AUTO_UPDATE=!0;Et.DEFAULT_MATRIX_WORLD_AUTO_UPDATE=!0;const Kt=new F,sn=new F,da=new F,on=new F,pi=new F,mi=new F,Ro=new F,ha=new F,fa=new F,pa=new F,ma=new rt,ga=new rt,_a=new rt;class Gt{constructor(e=new F,t=new F,i=new F){this.a=e,this.b=t,this.c=i}static getNormal(e,t,i,r){r.subVectors(i,t),Kt.subVectors(e,t),r.cross(Kt);const a=r.lengthSq();return a>0?r.multiplyScalar(1/Math.sqrt(a)):r.set(0,0,0)}static getBarycoord(e,t,i,r,a){Kt.subVectors(r,t),sn.subVectors(i,t),da.subVectors(e,t);const s=Kt.dot(Kt),o=Kt.dot(sn),c=Kt.dot(da),l=sn.dot(sn),d=sn.dot(da),h=s*l-o*o;if(h===0)return a.set(0,0,0),null;const f=1/h,m=(l*c-o*d)*f,g=(s*d-o*c)*f;return a.set(1-m-g,g,m)}static containsPoint(e,t,i,r){return this.getBarycoord(e,t,i,r,on)===null?!1:on.x>=0&&on.y>=0&&on.x+on.y<=1}static getInterpolation(e,t,i,r,a,s,o,c){return this.getBarycoord(e,t,i,r,on)===null?(c.x=0,c.y=0,"z"in c&&(c.z=0),"w"in c&&(c.w=0),null):(c.setScalar(0),c.addScaledVector(a,on.x),c.addScaledVector(s,on.y),c.addScaledVector(o,on.z),c)}static getInterpolatedAttribute(e,t,i,r,a,s){return ma.setScalar(0),ga.setScalar(0),_a.setScalar(0),ma.fromBufferAttribute(e,t),ga.fromBufferAttribute(e,i),_a.fromBufferAttribute(e,r),s.setScalar(0),s.addScaledVector(ma,a.x),s.addScaledVector(ga,a.y),s.addScaledVector(_a,a.z),s}static isFrontFacing(e,t,i,r){return Kt.subVectors(i,t),sn.subVectors(e,t),Kt.cross(sn).dot(r)<0}set(e,t,i){return this.a.copy(e),this.b.copy(t),this.c.copy(i),this}setFromPointsAndIndices(e,t,i,r){return this.a.copy(e[t]),this.b.copy(e[i]),this.c.copy(e[r]),this}setFromAttributeAndIndices(e,t,i,r){return this.a.fromBufferAttribute(e,t),this.b.fromBufferAttribute(e,i),this.c.fromBufferAttribute(e,r),this}clone(){return new this.constructor().copy(this)}copy(e){return this.a.copy(e.a),this.b.copy(e.b),this.c.copy(e.c),this}getArea(){return Kt.subVectors(this.c,this.b),sn.subVectors(this.a,this.b),Kt.cross(sn).length()*.5}getMidpoint(e){return e.addVectors(this.a,this.b).add(this.c).multiplyScalar(1/3)}getNormal(e){return Gt.getNormal(this.a,this.b,this.c,e)}getPlane(e){return e.setFromCoplanarPoints(this.a,this.b,this.c)}getBarycoord(e,t){return Gt.getBarycoord(e,this.a,this.b,this.c,t)}getInterpolation(e,t,i,r,a){return Gt.getInterpolation(e,this.a,this.b,this.c,t,i,r,a)}containsPoint(e){return Gt.containsPoint(e,this.a,this.b,this.c)}isFrontFacing(e){return Gt.isFrontFacing(this.a,this.b,this.c,e)}intersectsBox(e){return e.intersectsTriangle(this)}closestPointToPoint(e,t){const i=this.a,r=this.b,a=this.c;let s,o;pi.subVectors(r,i),mi.subVectors(a,i),ha.subVectors(e,i);const c=pi.dot(ha),l=mi.dot(ha);if(c<=0&&l<=0)return t.copy(i);fa.subVectors(e,r);const d=pi.dot(fa),h=mi.dot(fa);if(d>=0&&h<=d)return t.copy(r);const f=c*h-d*l;if(f<=0&&c>=0&&d<=0)return s=c/(c-d),t.copy(i).addScaledVector(pi,s);pa.subVectors(e,a);const m=pi.dot(pa),g=mi.dot(pa);if(g>=0&&m<=g)return t.copy(a);const _=m*l-c*g;if(_<=0&&l>=0&&g<=0)return o=l/(l-g),t.copy(i).addScaledVector(mi,o);const p=d*g-m*h;if(p<=0&&h-d>=0&&m-g>=0)return Ro.subVectors(a,r),o=(h-d)/(h-d+(m-g)),t.copy(r).addScaledVector(Ro,o);const u=1/(p+_+f);return s=_*u,o=f*u,t.copy(i).addScaledVector(pi,s).addScaledVector(mi,o)}equals(e){return e.a.equals(this.a)&&e.b.equals(this.b)&&e.c.equals(this.c)}}const Kc={aliceblue:15792383,antiquewhite:16444375,aqua:65535,aquamarine:8388564,azure:15794175,beige:16119260,bisque:16770244,black:0,blanchedalmond:16772045,blue:255,blueviolet:9055202,brown:10824234,burlywood:14596231,cadetblue:6266528,chartreuse:8388352,chocolate:13789470,coral:16744272,cornflowerblue:6591981,cornsilk:16775388,crimson:14423100,cyan:65535,darkblue:139,darkcyan:35723,darkgoldenrod:12092939,darkgray:11119017,darkgreen:25600,darkgrey:11119017,darkkhaki:12433259,darkmagenta:9109643,darkolivegreen:5597999,darkorange:16747520,darkorchid:10040012,darkred:9109504,darksalmon:15308410,darkseagreen:9419919,darkslateblue:4734347,darkslategray:3100495,darkslategrey:3100495,darkturquoise:52945,darkviolet:9699539,deeppink:16716947,deepskyblue:49151,dimgray:6908265,dimgrey:6908265,dodgerblue:2003199,firebrick:11674146,floralwhite:16775920,forestgreen:2263842,fuchsia:16711935,gainsboro:14474460,ghostwhite:16316671,gold:16766720,goldenrod:14329120,gray:8421504,green:32768,greenyellow:11403055,grey:8421504,honeydew:15794160,hotpink:16738740,indianred:13458524,indigo:4915330,ivory:16777200,khaki:15787660,lavender:15132410,lavenderblush:16773365,lawngreen:8190976,lemonchiffon:16775885,lightblue:11393254,lightcoral:15761536,lightcyan:14745599,lightgoldenrodyellow:16448210,lightgray:13882323,lightgreen:9498256,lightgrey:13882323,lightpink:16758465,lightsalmon:16752762,lightseagreen:2142890,lightskyblue:8900346,lightslategray:7833753,lightslategrey:7833753,lightsteelblue:11584734,lightyellow:16777184,lime:65280,limegreen:3329330,linen:16445670,magenta:16711935,maroon:8388608,mediumaquamarine:6737322,mediumblue:205,mediumorchid:12211667,mediumpurple:9662683,mediumseagreen:3978097,mediumslateblue:8087790,mediumspringgreen:64154,mediumturquoise:4772300,mediumvioletred:13047173,midnightblue:1644912,mintcream:16121850,mistyrose:16770273,moccasin:16770229,navajowhite:16768685,navy:128,oldlace:16643558,olive:8421376,olivedrab:7048739,orange:16753920,orangered:16729344,orchid:14315734,palegoldenrod:15657130,palegreen:10025880,paleturquoise:11529966,palevioletred:14381203,papayawhip:16773077,peachpuff:16767673,peru:13468991,pink:16761035,plum:14524637,powderblue:11591910,purple:8388736,rebeccapurple:6697881,red:16711680,rosybrown:12357519,royalblue:4286945,saddlebrown:9127187,salmon:16416882,sandybrown:16032864,seagreen:3050327,seashell:16774638,sienna:10506797,silver:12632256,skyblue:8900331,slateblue:6970061,slategray:7372944,slategrey:7372944,snow:16775930,springgreen:65407,steelblue:4620980,tan:13808780,teal:32896,thistle:14204888,tomato:16737095,turquoise:4251856,violet:15631086,wheat:16113331,white:16777215,whitesmoke:16119285,yellow:16776960,yellowgreen:10145074},Mn={h:0,s:0,l:0},gr={h:0,s:0,l:0};function va(n,e,t){return t<0&&(t+=1),t>1&&(t-=1),t<1/6?n+(e-n)*6*t:t<1/2?e:t<2/3?n+(e-n)*6*(2/3-t):n}class oe{constructor(e,t,i){return this.isColor=!0,this.r=1,this.g=1,this.b=1,this.set(e,t,i)}set(e,t,i){if(t===void 0&&i===void 0){const r=e;r&&r.isColor?this.copy(r):typeof r=="number"?this.setHex(r):typeof r=="string"&&this.setStyle(r)}else this.setRGB(e,t,i);return this}setScalar(e){return this.r=e,this.g=e,this.b=e,this}setHex(e,t=Nt){return e=Math.floor(e),this.r=(e>>16&255)/255,this.g=(e>>8&255)/255,this.b=(e&255)/255,Je.toWorkingColorSpace(this,t),this}setRGB(e,t,i,r=Je.workingColorSpace){return this.r=e,this.g=t,this.b=i,Je.toWorkingColorSpace(this,r),this}setHSL(e,t,i,r=Je.workingColorSpace){if(e=ou(e,1),t=qe(t,0,1),i=qe(i,0,1),t===0)this.r=this.g=this.b=i;else{const a=i<=.5?i*(1+t):i+t-i*t,s=2*i-a;this.r=va(s,a,e+1/3),this.g=va(s,a,e),this.b=va(s,a,e-1/3)}return Je.toWorkingColorSpace(this,r),this}setStyle(e,t=Nt){function i(a){a!==void 0&&parseFloat(a)<1&&console.warn("THREE.Color: Alpha component of "+e+" will be ignored.")}let r;if(r=/^(\w+)\(([^\)]*)\)/.exec(e)){let a;const s=r[1],o=r[2];switch(s){case"rgb":case"rgba":if(a=/^\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*(?:,\s*(\d*\.?\d+)\s*)?$/.exec(o))return i(a[4]),this.setRGB(Math.min(255,parseInt(a[1],10))/255,Math.min(255,parseInt(a[2],10))/255,Math.min(255,parseInt(a[3],10))/255,t);if(a=/^\s*(\d+)\%\s*,\s*(\d+)\%\s*,\s*(\d+)\%\s*(?:,\s*(\d*\.?\d+)\s*)?$/.exec(o))return i(a[4]),this.setRGB(Math.min(100,parseInt(a[1],10))/100,Math.min(100,parseInt(a[2],10))/100,Math.min(100,parseInt(a[3],10))/100,t);break;case"hsl":case"hsla":if(a=/^\s*(\d*\.?\d+)\s*,\s*(\d*\.?\d+)\%\s*,\s*(\d*\.?\d+)\%\s*(?:,\s*(\d*\.?\d+)\s*)?$/.exec(o))return i(a[4]),this.setHSL(parseFloat(a[1])/360,parseFloat(a[2])/100,parseFloat(a[3])/100,t);break;default:console.warn("THREE.Color: Unknown color model "+e)}}else if(r=/^\#([A-Fa-f\d]+)$/.exec(e)){const a=r[1],s=a.length;if(s===3)return this.setRGB(parseInt(a.charAt(0),16)/15,parseInt(a.charAt(1),16)/15,parseInt(a.charAt(2),16)/15,t);if(s===6)return this.setHex(parseInt(a,16),t);console.warn("THREE.Color: Invalid hex color "+e)}else if(e&&e.length>0)return this.setColorName(e,t);return this}setColorName(e,t=Nt){const i=Kc[e.toLowerCase()];return i!==void 0?this.setHex(i,t):console.warn("THREE.Color: Unknown color "+e),this}clone(){return new this.constructor(this.r,this.g,this.b)}copy(e){return this.r=e.r,this.g=e.g,this.b=e.b,this}copySRGBToLinear(e){return this.r=pn(e.r),this.g=pn(e.g),this.b=pn(e.b),this}copyLinearToSRGB(e){return this.r=Ri(e.r),this.g=Ri(e.g),this.b=Ri(e.b),this}convertSRGBToLinear(){return this.copySRGBToLinear(this),this}convertLinearToSRGB(){return this.copyLinearToSRGB(this),this}getHex(e=Nt){return Je.fromWorkingColorSpace(Tt.copy(this),e),Math.round(qe(Tt.r*255,0,255))*65536+Math.round(qe(Tt.g*255,0,255))*256+Math.round(qe(Tt.b*255,0,255))}getHexString(e=Nt){return("000000"+this.getHex(e).toString(16)).slice(-6)}getHSL(e,t=Je.workingColorSpace){Je.fromWorkingColorSpace(Tt.copy(this),t);const i=Tt.r,r=Tt.g,a=Tt.b,s=Math.max(i,r,a),o=Math.min(i,r,a);let c,l;const d=(o+s)/2;if(o===s)c=0,l=0;else{const h=s-o;switch(l=d<=.5?h/(s+o):h/(2-s-o),s){case i:c=(r-a)/h+(r<a?6:0);break;case r:c=(a-i)/h+2;break;case a:c=(i-r)/h+4;break}c/=6}return e.h=c,e.s=l,e.l=d,e}getRGB(e,t=Je.workingColorSpace){return Je.fromWorkingColorSpace(Tt.copy(this),t),e.r=Tt.r,e.g=Tt.g,e.b=Tt.b,e}getStyle(e=Nt){Je.fromWorkingColorSpace(Tt.copy(this),e);const t=Tt.r,i=Tt.g,r=Tt.b;return e!==Nt?`color(${e} ${t.toFixed(3)} ${i.toFixed(3)} ${r.toFixed(3)})`:`rgb(${Math.round(t*255)},${Math.round(i*255)},${Math.round(r*255)})`}offsetHSL(e,t,i){return this.getHSL(Mn),this.setHSL(Mn.h+e,Mn.s+t,Mn.l+i)}add(e){return this.r+=e.r,this.g+=e.g,this.b+=e.b,this}addColors(e,t){return this.r=e.r+t.r,this.g=e.g+t.g,this.b=e.b+t.b,this}addScalar(e){return this.r+=e,this.g+=e,this.b+=e,this}sub(e){return this.r=Math.max(0,this.r-e.r),this.g=Math.max(0,this.g-e.g),this.b=Math.max(0,this.b-e.b),this}multiply(e){return this.r*=e.r,this.g*=e.g,this.b*=e.b,this}multiplyScalar(e){return this.r*=e,this.g*=e,this.b*=e,this}lerp(e,t){return this.r+=(e.r-this.r)*t,this.g+=(e.g-this.g)*t,this.b+=(e.b-this.b)*t,this}lerpColors(e,t,i){return this.r=e.r+(t.r-e.r)*i,this.g=e.g+(t.g-e.g)*i,this.b=e.b+(t.b-e.b)*i,this}lerpHSL(e,t){this.getHSL(Mn),e.getHSL(gr);const i=ta(Mn.h,gr.h,t),r=ta(Mn.s,gr.s,t),a=ta(Mn.l,gr.l,t);return this.setHSL(i,r,a),this}setFromVector3(e){return this.r=e.x,this.g=e.y,this.b=e.z,this}applyMatrix3(e){const t=this.r,i=this.g,r=this.b,a=e.elements;return this.r=a[0]*t+a[3]*i+a[6]*r,this.g=a[1]*t+a[4]*i+a[7]*r,this.b=a[2]*t+a[5]*i+a[8]*r,this}equals(e){return e.r===this.r&&e.g===this.g&&e.b===this.b}fromArray(e,t=0){return this.r=e[t],this.g=e[t+1],this.b=e[t+2],this}toArray(e=[],t=0){return e[t]=this.r,e[t+1]=this.g,e[t+2]=this.b,e}fromBufferAttribute(e,t){return this.r=e.getX(t),this.g=e.getY(t),this.b=e.getZ(t),this}toJSON(){return this.getHex()}*[Symbol.iterator](){yield this.r,yield this.g,yield this.b}}const Tt=new oe;oe.NAMES=Kc;let Tu=0;class Bi extends ki{constructor(){super(),this.isMaterial=!0,Object.defineProperty(this,"id",{value:Tu++}),this.uuid=rr(),this.name="",this.type="Material",this.blending=wi,this.side=Pn,this.vertexColors=!1,this.opacity=1,this.transparent=!1,this.alphaHash=!1,this.blendSrc=Oa,this.blendDst=Ba,this.blendEquation=Xn,this.blendSrcAlpha=null,this.blendDstAlpha=null,this.blendEquationAlpha=null,this.blendColor=new oe(0,0,0),this.blendAlpha=0,this.depthFunc=Ci,this.depthTest=!0,this.depthWrite=!0,this.stencilWriteMask=255,this.stencilFunc=po,this.stencilRef=0,this.stencilFuncMask=255,this.stencilFail=si,this.stencilZFail=si,this.stencilZPass=si,this.stencilWrite=!1,this.clippingPlanes=null,this.clipIntersection=!1,this.clipShadows=!1,this.shadowSide=null,this.colorWrite=!0,this.precision=null,this.polygonOffset=!1,this.polygonOffsetFactor=0,this.polygonOffsetUnits=0,this.dithering=!1,this.alphaToCoverage=!1,this.premultipliedAlpha=!1,this.forceSinglePass=!1,this.visible=!0,this.toneMapped=!0,this.userData={},this.version=0,this._alphaTest=0}get alphaTest(){return this._alphaTest}set alphaTest(e){this._alphaTest>0!=e>0&&this.version++,this._alphaTest=e}onBeforeRender(){}onBeforeCompile(){}customProgramCacheKey(){return this.onBeforeCompile.toString()}setValues(e){if(e!==void 0)for(const t in e){const i=e[t];if(i===void 0){console.warn(`THREE.Material: parameter '${t}' has value of undefined.`);continue}const r=this[t];if(r===void 0){console.warn(`THREE.Material: '${t}' is not a property of THREE.${this.type}.`);continue}r&&r.isColor?r.set(i):r&&r.isVector3&&i&&i.isVector3?r.copy(i):this[t]=i}}toJSON(e){const t=e===void 0||typeof e=="string";t&&(e={textures:{},images:{}});const i={metadata:{version:4.6,type:"Material",generator:"Material.toJSON"}};i.uuid=this.uuid,i.type=this.type,this.name!==""&&(i.name=this.name),this.color&&this.color.isColor&&(i.color=this.color.getHex()),this.roughness!==void 0&&(i.roughness=this.roughness),this.metalness!==void 0&&(i.metalness=this.metalness),this.sheen!==void 0&&(i.sheen=this.sheen),this.sheenColor&&this.sheenColor.isColor&&(i.sheenColor=this.sheenColor.getHex()),this.sheenRoughness!==void 0&&(i.sheenRoughness=this.sheenRoughness),this.emissive&&this.emissive.isColor&&(i.emissive=this.emissive.getHex()),this.emissiveIntensity!==void 0&&this.emissiveIntensity!==1&&(i.emissiveIntensity=this.emissiveIntensity),this.specular&&this.specular.isColor&&(i.specular=this.specular.getHex()),this.specularIntensity!==void 0&&(i.specularIntensity=this.specularIntensity),this.specularColor&&this.specularColor.isColor&&(i.specularColor=this.specularColor.getHex()),this.shininess!==void 0&&(i.shininess=this.shininess),this.clearcoat!==void 0&&(i.clearcoat=this.clearcoat),this.clearcoatRoughness!==void 0&&(i.clearcoatRoughness=this.clearcoatRoughness),this.clearcoatMap&&this.clearcoatMap.isTexture&&(i.clearcoatMap=this.clearcoatMap.toJSON(e).uuid),this.clearcoatRoughnessMap&&this.clearcoatRoughnessMap.isTexture&&(i.clearcoatRoughnessMap=this.clearcoatRoughnessMap.toJSON(e).uuid),this.clearcoatNormalMap&&this.clearcoatNormalMap.isTexture&&(i.clearcoatNormalMap=this.clearcoatNormalMap.toJSON(e).uuid,i.clearcoatNormalScale=this.clearcoatNormalScale.toArray()),this.dispersion!==void 0&&(i.dispersion=this.dispersion),this.iridescence!==void 0&&(i.iridescence=this.iridescence),this.iridescenceIOR!==void 0&&(i.iridescenceIOR=this.iridescenceIOR),this.iridescenceThicknessRange!==void 0&&(i.iridescenceThicknessRange=this.iridescenceThicknessRange),this.iridescenceMap&&this.iridescenceMap.isTexture&&(i.iridescenceMap=this.iridescenceMap.toJSON(e).uuid),this.iridescenceThicknessMap&&this.iridescenceThicknessMap.isTexture&&(i.iridescenceThicknessMap=this.iridescenceThicknessMap.toJSON(e).uuid),this.anisotropy!==void 0&&(i.anisotropy=this.anisotropy),this.anisotropyRotation!==void 0&&(i.anisotropyRotation=this.anisotropyRotation),this.anisotropyMap&&this.anisotropyMap.isTexture&&(i.anisotropyMap=this.anisotropyMap.toJSON(e).uuid),this.map&&this.map.isTexture&&(i.map=this.map.toJSON(e).uuid),this.matcap&&this.matcap.isTexture&&(i.matcap=this.matcap.toJSON(e).uuid),this.alphaMap&&this.alphaMap.isTexture&&(i.alphaMap=this.alphaMap.toJSON(e).uuid),this.lightMap&&this.lightMap.isTexture&&(i.lightMap=this.lightMap.toJSON(e).uuid,i.lightMapIntensity=this.lightMapIntensity),this.aoMap&&this.aoMap.isTexture&&(i.aoMap=this.aoMap.toJSON(e).uuid,i.aoMapIntensity=this.aoMapIntensity),this.bumpMap&&this.bumpMap.isTexture&&(i.bumpMap=this.bumpMap.toJSON(e).uuid,i.bumpScale=this.bumpScale),this.normalMap&&this.normalMap.isTexture&&(i.normalMap=this.normalMap.toJSON(e).uuid,i.normalMapType=this.normalMapType,i.normalScale=this.normalScale.toArray()),this.displacementMap&&this.displacementMap.isTexture&&(i.displacementMap=this.displacementMap.toJSON(e).uuid,i.displacementScale=this.displacementScale,i.displacementBias=this.displacementBias),this.roughnessMap&&this.roughnessMap.isTexture&&(i.roughnessMap=this.roughnessMap.toJSON(e).uuid),this.metalnessMap&&this.metalnessMap.isTexture&&(i.metalnessMap=this.metalnessMap.toJSON(e).uuid),this.emissiveMap&&this.emissiveMap.isTexture&&(i.emissiveMap=this.emissiveMap.toJSON(e).uuid),this.specularMap&&this.specularMap.isTexture&&(i.specularMap=this.specularMap.toJSON(e).uuid),this.specularIntensityMap&&this.specularIntensityMap.isTexture&&(i.specularIntensityMap=this.specularIntensityMap.toJSON(e).uuid),this.specularColorMap&&this.specularColorMap.isTexture&&(i.specularColorMap=this.specularColorMap.toJSON(e).uuid),this.envMap&&this.envMap.isTexture&&(i.envMap=this.envMap.toJSON(e).uuid,this.combine!==void 0&&(i.combine=this.combine)),this.envMapRotation!==void 0&&(i.envMapRotation=this.envMapRotation.toArray()),this.envMapIntensity!==void 0&&(i.envMapIntensity=this.envMapIntensity),this.reflectivity!==void 0&&(i.reflectivity=this.reflectivity),this.refractionRatio!==void 0&&(i.refractionRatio=this.refractionRatio),this.gradientMap&&this.gradientMap.isTexture&&(i.gradientMap=this.gradientMap.toJSON(e).uuid),this.transmission!==void 0&&(i.transmission=this.transmission),this.transmissionMap&&this.transmissionMap.isTexture&&(i.transmissionMap=this.transmissionMap.toJSON(e).uuid),this.thickness!==void 0&&(i.thickness=this.thickness),this.thicknessMap&&this.thicknessMap.isTexture&&(i.thicknessMap=this.thicknessMap.toJSON(e).uuid),this.attenuationDistance!==void 0&&this.attenuationDistance!==1/0&&(i.attenuationDistance=this.attenuationDistance),this.attenuationColor!==void 0&&(i.attenuationColor=this.attenuationColor.getHex()),this.size!==void 0&&(i.size=this.size),this.shadowSide!==null&&(i.shadowSide=this.shadowSide),this.sizeAttenuation!==void 0&&(i.sizeAttenuation=this.sizeAttenuation),this.blending!==wi&&(i.blending=this.blending),this.side!==Pn&&(i.side=this.side),this.vertexColors===!0&&(i.vertexColors=!0),this.opacity<1&&(i.opacity=this.opacity),this.transparent===!0&&(i.transparent=!0),this.blendSrc!==Oa&&(i.blendSrc=this.blendSrc),this.blendDst!==Ba&&(i.blendDst=this.blendDst),this.blendEquation!==Xn&&(i.blendEquation=this.blendEquation),this.blendSrcAlpha!==null&&(i.blendSrcAlpha=this.blendSrcAlpha),this.blendDstAlpha!==null&&(i.blendDstAlpha=this.blendDstAlpha),this.blendEquationAlpha!==null&&(i.blendEquationAlpha=this.blendEquationAlpha),this.blendColor&&this.blendColor.isColor&&(i.blendColor=this.blendColor.getHex()),this.blendAlpha!==0&&(i.blendAlpha=this.blendAlpha),this.depthFunc!==Ci&&(i.depthFunc=this.depthFunc),this.depthTest===!1&&(i.depthTest=this.depthTest),this.depthWrite===!1&&(i.depthWrite=this.depthWrite),this.colorWrite===!1&&(i.colorWrite=this.colorWrite),this.stencilWriteMask!==255&&(i.stencilWriteMask=this.stencilWriteMask),this.stencilFunc!==po&&(i.stencilFunc=this.stencilFunc),this.stencilRef!==0&&(i.stencilRef=this.stencilRef),this.stencilFuncMask!==255&&(i.stencilFuncMask=this.stencilFuncMask),this.stencilFail!==si&&(i.stencilFail=this.stencilFail),this.stencilZFail!==si&&(i.stencilZFail=this.stencilZFail),this.stencilZPass!==si&&(i.stencilZPass=this.stencilZPass),this.stencilWrite===!0&&(i.stencilWrite=this.stencilWrite),this.rotation!==void 0&&this.rotation!==0&&(i.rotation=this.rotation),this.polygonOffset===!0&&(i.polygonOffset=!0),this.polygonOffsetFactor!==0&&(i.polygonOffsetFactor=this.polygonOffsetFactor),this.polygonOffsetUnits!==0&&(i.polygonOffsetUnits=this.polygonOffsetUnits),this.linewidth!==void 0&&this.linewidth!==1&&(i.linewidth=this.linewidth),this.dashSize!==void 0&&(i.dashSize=this.dashSize),this.gapSize!==void 0&&(i.gapSize=this.gapSize),this.scale!==void 0&&(i.scale=this.scale),this.dithering===!0&&(i.dithering=!0),this.alphaTest>0&&(i.alphaTest=this.alphaTest),this.alphaHash===!0&&(i.alphaHash=!0),this.alphaToCoverage===!0&&(i.alphaToCoverage=!0),this.premultipliedAlpha===!0&&(i.premultipliedAlpha=!0),this.forceSinglePass===!0&&(i.forceSinglePass=!0),this.wireframe===!0&&(i.wireframe=!0),this.wireframeLinewidth>1&&(i.wireframeLinewidth=this.wireframeLinewidth),this.wireframeLinecap!=="round"&&(i.wireframeLinecap=this.wireframeLinecap),this.wireframeLinejoin!=="round"&&(i.wireframeLinejoin=this.wireframeLinejoin),this.flatShading===!0&&(i.flatShading=!0),this.visible===!1&&(i.visible=!1),this.toneMapped===!1&&(i.toneMapped=!1),this.fog===!1&&(i.fog=!1),Object.keys(this.userData).length>0&&(i.userData=this.userData);function r(a){const s=[];for(const o in a){const c=a[o];delete c.metadata,s.push(c)}return s}if(t){const a=r(e.textures),s=r(e.images);a.length>0&&(i.textures=a),s.length>0&&(i.images=s)}return i}clone(){return new this.constructor().copy(this)}copy(e){this.name=e.name,this.blending=e.blending,this.side=e.side,this.vertexColors=e.vertexColors,this.opacity=e.opacity,this.transparent=e.transparent,this.blendSrc=e.blendSrc,this.blendDst=e.blendDst,this.blendEquation=e.blendEquation,this.blendSrcAlpha=e.blendSrcAlpha,this.blendDstAlpha=e.blendDstAlpha,this.blendEquationAlpha=e.blendEquationAlpha,this.blendColor.copy(e.blendColor),this.blendAlpha=e.blendAlpha,this.depthFunc=e.depthFunc,this.depthTest=e.depthTest,this.depthWrite=e.depthWrite,this.stencilWriteMask=e.stencilWriteMask,this.stencilFunc=e.stencilFunc,this.stencilRef=e.stencilRef,this.stencilFuncMask=e.stencilFuncMask,this.stencilFail=e.stencilFail,this.stencilZFail=e.stencilZFail,this.stencilZPass=e.stencilZPass,this.stencilWrite=e.stencilWrite;const t=e.clippingPlanes;let i=null;if(t!==null){const r=t.length;i=new Array(r);for(let a=0;a!==r;++a)i[a]=t[a].clone()}return this.clippingPlanes=i,this.clipIntersection=e.clipIntersection,this.clipShadows=e.clipShadows,this.shadowSide=e.shadowSide,this.colorWrite=e.colorWrite,this.precision=e.precision,this.polygonOffset=e.polygonOffset,this.polygonOffsetFactor=e.polygonOffsetFactor,this.polygonOffsetUnits=e.polygonOffsetUnits,this.dithering=e.dithering,this.alphaTest=e.alphaTest,this.alphaHash=e.alphaHash,this.alphaToCoverage=e.alphaToCoverage,this.premultipliedAlpha=e.premultipliedAlpha,this.forceSinglePass=e.forceSinglePass,this.visible=e.visible,this.toneMapped=e.toneMapped,this.userData=JSON.parse(JSON.stringify(e.userData)),this}dispose(){this.dispatchEvent({type:"dispose"})}set needsUpdate(e){e===!0&&this.version++}onBuild(){console.warn("Material: onBuild() has been removed.")}}class Ln extends Bi{constructor(e){super(),this.isMeshBasicMaterial=!0,this.type="MeshBasicMaterial",this.color=new oe(16777215),this.map=null,this.lightMap=null,this.lightMapIntensity=1,this.aoMap=null,this.aoMapIntensity=1,this.specularMap=null,this.alphaMap=null,this.envMap=null,this.envMapRotation=new xt,this.combine=Lc,this.reflectivity=1,this.refractionRatio=.98,this.wireframe=!1,this.wireframeLinewidth=1,this.wireframeLinecap="round",this.wireframeLinejoin="round",this.fog=!0,this.setValues(e)}copy(e){return super.copy(e),this.color.copy(e.color),this.map=e.map,this.lightMap=e.lightMap,this.lightMapIntensity=e.lightMapIntensity,this.aoMap=e.aoMap,this.aoMapIntensity=e.aoMapIntensity,this.specularMap=e.specularMap,this.alphaMap=e.alphaMap,this.envMap=e.envMap,this.envMapRotation.copy(e.envMapRotation),this.combine=e.combine,this.reflectivity=e.reflectivity,this.refractionRatio=e.refractionRatio,this.wireframe=e.wireframe,this.wireframeLinewidth=e.wireframeLinewidth,this.wireframeLinecap=e.wireframeLinecap,this.wireframeLinejoin=e.wireframeLinejoin,this.fog=e.fog,this}}const mt=new F,_r=new We;let wu=0;class en{constructor(e,t,i=!1){if(Array.isArray(e))throw new TypeError("THREE.BufferAttribute: array should be a Typed Array.");this.isBufferAttribute=!0,Object.defineProperty(this,"id",{value:wu++}),this.name="",this.array=e,this.itemSize=t,this.count=e!==void 0?e.length/t:0,this.normalized=i,this.usage=mo,this.updateRanges=[],this.gpuType=hn,this.version=0}onUploadCallback(){}set needsUpdate(e){e===!0&&this.version++}setUsage(e){return this.usage=e,this}addUpdateRange(e,t){this.updateRanges.push({start:e,count:t})}clearUpdateRanges(){this.updateRanges.length=0}copy(e){return this.name=e.name,this.array=new e.array.constructor(e.array),this.itemSize=e.itemSize,this.count=e.count,this.normalized=e.normalized,this.usage=e.usage,this.gpuType=e.gpuType,this}copyAt(e,t,i){e*=this.itemSize,i*=t.itemSize;for(let r=0,a=this.itemSize;r<a;r++)this.array[e+r]=t.array[i+r];return this}copyArray(e){return this.array.set(e),this}applyMatrix3(e){if(this.itemSize===2)for(let t=0,i=this.count;t<i;t++)_r.fromBufferAttribute(this,t),_r.applyMatrix3(e),this.setXY(t,_r.x,_r.y);else if(this.itemSize===3)for(let t=0,i=this.count;t<i;t++)mt.fromBufferAttribute(this,t),mt.applyMatrix3(e),this.setXYZ(t,mt.x,mt.y,mt.z);return this}applyMatrix4(e){for(let t=0,i=this.count;t<i;t++)mt.fromBufferAttribute(this,t),mt.applyMatrix4(e),this.setXYZ(t,mt.x,mt.y,mt.z);return this}applyNormalMatrix(e){for(let t=0,i=this.count;t<i;t++)mt.fromBufferAttribute(this,t),mt.applyNormalMatrix(e),this.setXYZ(t,mt.x,mt.y,mt.z);return this}transformDirection(e){for(let t=0,i=this.count;t<i;t++)mt.fromBufferAttribute(this,t),mt.transformDirection(e),this.setXYZ(t,mt.x,mt.y,mt.z);return this}set(e,t=0){return this.array.set(e,t),this}getComponent(e,t){let i=this.array[e*this.itemSize+t];return this.normalized&&(i=Hi(i,this.array)),i}setComponent(e,t,i){return this.normalized&&(i=Lt(i,this.array)),this.array[e*this.itemSize+t]=i,this}getX(e){let t=this.array[e*this.itemSize];return this.normalized&&(t=Hi(t,this.array)),t}setX(e,t){return this.normalized&&(t=Lt(t,this.array)),this.array[e*this.itemSize]=t,this}getY(e){let t=this.array[e*this.itemSize+1];return this.normalized&&(t=Hi(t,this.array)),t}setY(e,t){return this.normalized&&(t=Lt(t,this.array)),this.array[e*this.itemSize+1]=t,this}getZ(e){let t=this.array[e*this.itemSize+2];return this.normalized&&(t=Hi(t,this.array)),t}setZ(e,t){return this.normalized&&(t=Lt(t,this.array)),this.array[e*this.itemSize+2]=t,this}getW(e){let t=this.array[e*this.itemSize+3];return this.normalized&&(t=Hi(t,this.array)),t}setW(e,t){return this.normalized&&(t=Lt(t,this.array)),this.array[e*this.itemSize+3]=t,this}setXY(e,t,i){return e*=this.itemSize,this.normalized&&(t=Lt(t,this.array),i=Lt(i,this.array)),this.array[e+0]=t,this.array[e+1]=i,this}setXYZ(e,t,i,r){return e*=this.itemSize,this.normalized&&(t=Lt(t,this.array),i=Lt(i,this.array),r=Lt(r,this.array)),this.array[e+0]=t,this.array[e+1]=i,this.array[e+2]=r,this}setXYZW(e,t,i,r,a){return e*=this.itemSize,this.normalized&&(t=Lt(t,this.array),i=Lt(i,this.array),r=Lt(r,this.array),a=Lt(a,this.array)),this.array[e+0]=t,this.array[e+1]=i,this.array[e+2]=r,this.array[e+3]=a,this}onUpload(e){return this.onUploadCallback=e,this}clone(){return new this.constructor(this.array,this.itemSize).copy(this)}toJSON(){const e={itemSize:this.itemSize,type:this.array.constructor.name,array:Array.from(this.array),normalized:this.normalized};return this.name!==""&&(e.name=this.name),this.usage!==mo&&(e.usage=this.usage),e}}class $c extends en{constructor(e,t,i){super(new Uint16Array(e),t,i)}}class Yc extends en{constructor(e,t,i){super(new Uint32Array(e),t,i)}}class je extends en{constructor(e,t,i){super(new Float32Array(e),t,i)}}let Au=0;const Vt=new at,xa=new Et,gi=new F,zt=new Oi,qi=new Oi,vt=new F;class Xe extends ki{constructor(){super(),this.isBufferGeometry=!0,Object.defineProperty(this,"id",{value:Au++}),this.uuid=rr(),this.name="",this.type="BufferGeometry",this.index=null,this.indirect=null,this.attributes={},this.morphAttributes={},this.morphTargetsRelative=!1,this.groups=[],this.boundingBox=null,this.boundingSphere=null,this.drawRange={start:0,count:1/0},this.userData={}}getIndex(){return this.index}setIndex(e){return Array.isArray(e)?this.index=new(Xc(e)?Yc:$c)(e,1):this.index=e,this}setIndirect(e){return this.indirect=e,this}getIndirect(){return this.indirect}getAttribute(e){return this.attributes[e]}setAttribute(e,t){return this.attributes[e]=t,this}deleteAttribute(e){return delete this.attributes[e],this}hasAttribute(e){return this.attributes[e]!==void 0}addGroup(e,t,i=0){this.groups.push({start:e,count:t,materialIndex:i})}clearGroups(){this.groups=[]}setDrawRange(e,t){this.drawRange.start=e,this.drawRange.count=t}applyMatrix4(e){const t=this.attributes.position;t!==void 0&&(t.applyMatrix4(e),t.needsUpdate=!0);const i=this.attributes.normal;if(i!==void 0){const a=new Ve().getNormalMatrix(e);i.applyNormalMatrix(a),i.needsUpdate=!0}const r=this.attributes.tangent;return r!==void 0&&(r.transformDirection(e),r.needsUpdate=!0),this.boundingBox!==null&&this.computeBoundingBox(),this.boundingSphere!==null&&this.computeBoundingSphere(),this}applyQuaternion(e){return Vt.makeRotationFromQuaternion(e),this.applyMatrix4(Vt),this}rotateX(e){return Vt.makeRotationX(e),this.applyMatrix4(Vt),this}rotateY(e){return Vt.makeRotationY(e),this.applyMatrix4(Vt),this}rotateZ(e){return Vt.makeRotationZ(e),this.applyMatrix4(Vt),this}translate(e,t,i){return Vt.makeTranslation(e,t,i),this.applyMatrix4(Vt),this}scale(e,t,i){return Vt.makeScale(e,t,i),this.applyMatrix4(Vt),this}lookAt(e){return xa.lookAt(e),xa.updateMatrix(),this.applyMatrix4(xa.matrix),this}center(){return this.computeBoundingBox(),this.boundingBox.getCenter(gi).negate(),this.translate(gi.x,gi.y,gi.z),this}setFromPoints(e){const t=this.getAttribute("position");if(t===void 0){const i=[];for(let r=0,a=e.length;r<a;r++){const s=e[r];i.push(s.x,s.y,s.z||0)}this.setAttribute("position",new je(i,3))}else{const i=Math.min(e.length,t.count);for(let r=0;r<i;r++){const a=e[r];t.setXYZ(r,a.x,a.y,a.z||0)}e.length>t.count&&console.warn("THREE.BufferGeometry: Buffer size too small for points data. Use .dispose() and create a new geometry."),t.needsUpdate=!0}return this}computeBoundingBox(){this.boundingBox===null&&(this.boundingBox=new Oi);const e=this.attributes.position,t=this.morphAttributes.position;if(e&&e.isGLBufferAttribute){console.error("THREE.BufferGeometry.computeBoundingBox(): GLBufferAttribute requires a manual bounding box.",this),this.boundingBox.set(new F(-1/0,-1/0,-1/0),new F(1/0,1/0,1/0));return}if(e!==void 0){if(this.boundingBox.setFromBufferAttribute(e),t)for(let i=0,r=t.length;i<r;i++){const a=t[i];zt.setFromBufferAttribute(a),this.morphTargetsRelative?(vt.addVectors(this.boundingBox.min,zt.min),this.boundingBox.expandByPoint(vt),vt.addVectors(this.boundingBox.max,zt.max),this.boundingBox.expandByPoint(vt)):(this.boundingBox.expandByPoint(zt.min),this.boundingBox.expandByPoint(zt.max))}}else this.boundingBox.makeEmpty();(isNaN(this.boundingBox.min.x)||isNaN(this.boundingBox.min.y)||isNaN(this.boundingBox.min.z))&&console.error('THREE.BufferGeometry.computeBoundingBox(): Computed min/max have NaN values. The "position" attribute is likely to have NaN values.',this)}computeBoundingSphere(){this.boundingSphere===null&&(this.boundingSphere=new $r);const e=this.attributes.position,t=this.morphAttributes.position;if(e&&e.isGLBufferAttribute){console.error("THREE.BufferGeometry.computeBoundingSphere(): GLBufferAttribute requires a manual bounding sphere.",this),this.boundingSphere.set(new F,1/0);return}if(e){const i=this.boundingSphere.center;if(zt.setFromBufferAttribute(e),t)for(let a=0,s=t.length;a<s;a++){const o=t[a];qi.setFromBufferAttribute(o),this.morphTargetsRelative?(vt.addVectors(zt.min,qi.min),zt.expandByPoint(vt),vt.addVectors(zt.max,qi.max),zt.expandByPoint(vt)):(zt.expandByPoint(qi.min),zt.expandByPoint(qi.max))}zt.getCenter(i);let r=0;for(let a=0,s=e.count;a<s;a++)vt.fromBufferAttribute(e,a),r=Math.max(r,i.distanceToSquared(vt));if(t)for(let a=0,s=t.length;a<s;a++){const o=t[a],c=this.morphTargetsRelative;for(let l=0,d=o.count;l<d;l++)vt.fromBufferAttribute(o,l),c&&(gi.fromBufferAttribute(e,l),vt.add(gi)),r=Math.max(r,i.distanceToSquared(vt))}this.boundingSphere.radius=Math.sqrt(r),isNaN(this.boundingSphere.radius)&&console.error('THREE.BufferGeometry.computeBoundingSphere(): Computed radius is NaN. The "position" attribute is likely to have NaN values.',this)}}computeTangents(){const e=this.index,t=this.attributes;if(e===null||t.position===void 0||t.normal===void 0||t.uv===void 0){console.error("THREE.BufferGeometry: .computeTangents() failed. Missing required attributes (index, position, normal or uv)");return}const i=t.position,r=t.normal,a=t.uv;this.hasAttribute("tangent")===!1&&this.setAttribute("tangent",new en(new Float32Array(4*i.count),4));const s=this.getAttribute("tangent"),o=[],c=[];for(let C=0;C<i.count;C++)o[C]=new F,c[C]=new F;const l=new F,d=new F,h=new F,f=new We,m=new We,g=new We,_=new F,p=new F;function u(C,v,x){l.fromBufferAttribute(i,C),d.fromBufferAttribute(i,v),h.fromBufferAttribute(i,x),f.fromBufferAttribute(a,C),m.fromBufferAttribute(a,v),g.fromBufferAttribute(a,x),d.sub(l),h.sub(l),m.sub(f),g.sub(f);const P=1/(m.x*g.y-g.x*m.y);isFinite(P)&&(_.copy(d).multiplyScalar(g.y).addScaledVector(h,-m.y).multiplyScalar(P),p.copy(h).multiplyScalar(m.x).addScaledVector(d,-g.x).multiplyScalar(P),o[C].add(_),o[v].add(_),o[x].add(_),c[C].add(p),c[v].add(p),c[x].add(p))}let E=this.groups;E.length===0&&(E=[{start:0,count:e.count}]);for(let C=0,v=E.length;C<v;++C){const x=E[C],P=x.start,U=x.count;for(let w=P,R=P+U;w<R;w+=3)u(e.getX(w+0),e.getX(w+1),e.getX(w+2))}const y=new F,M=new F,D=new F,A=new F;function b(C){D.fromBufferAttribute(r,C),A.copy(D);const v=o[C];y.copy(v),y.sub(D.multiplyScalar(D.dot(v))).normalize(),M.crossVectors(A,v);const P=M.dot(c[C])<0?-1:1;s.setXYZW(C,y.x,y.y,y.z,P)}for(let C=0,v=E.length;C<v;++C){const x=E[C],P=x.start,U=x.count;for(let w=P,R=P+U;w<R;w+=3)b(e.getX(w+0)),b(e.getX(w+1)),b(e.getX(w+2))}}computeVertexNormals(){const e=this.index,t=this.getAttribute("position");if(t!==void 0){let i=this.getAttribute("normal");if(i===void 0)i=new en(new Float32Array(t.count*3),3),this.setAttribute("normal",i);else for(let f=0,m=i.count;f<m;f++)i.setXYZ(f,0,0,0);const r=new F,a=new F,s=new F,o=new F,c=new F,l=new F,d=new F,h=new F;if(e)for(let f=0,m=e.count;f<m;f+=3){const g=e.getX(f+0),_=e.getX(f+1),p=e.getX(f+2);r.fromBufferAttribute(t,g),a.fromBufferAttribute(t,_),s.fromBufferAttribute(t,p),d.subVectors(s,a),h.subVectors(r,a),d.cross(h),o.fromBufferAttribute(i,g),c.fromBufferAttribute(i,_),l.fromBufferAttribute(i,p),o.add(d),c.add(d),l.add(d),i.setXYZ(g,o.x,o.y,o.z),i.setXYZ(_,c.x,c.y,c.z),i.setXYZ(p,l.x,l.y,l.z)}else for(let f=0,m=t.count;f<m;f+=3)r.fromBufferAttribute(t,f+0),a.fromBufferAttribute(t,f+1),s.fromBufferAttribute(t,f+2),d.subVectors(s,a),h.subVectors(r,a),d.cross(h),i.setXYZ(f+0,d.x,d.y,d.z),i.setXYZ(f+1,d.x,d.y,d.z),i.setXYZ(f+2,d.x,d.y,d.z);this.normalizeNormals(),i.needsUpdate=!0}}normalizeNormals(){const e=this.attributes.normal;for(let t=0,i=e.count;t<i;t++)vt.fromBufferAttribute(e,t),vt.normalize(),e.setXYZ(t,vt.x,vt.y,vt.z)}toNonIndexed(){function e(o,c){const l=o.array,d=o.itemSize,h=o.normalized,f=new l.constructor(c.length*d);let m=0,g=0;for(let _=0,p=c.length;_<p;_++){o.isInterleavedBufferAttribute?m=c[_]*o.data.stride+o.offset:m=c[_]*d;for(let u=0;u<d;u++)f[g++]=l[m++]}return new en(f,d,h)}if(this.index===null)return console.warn("THREE.BufferGeometry.toNonIndexed(): BufferGeometry is already non-indexed."),this;const t=new Xe,i=this.index.array,r=this.attributes;for(const o in r){const c=r[o],l=e(c,i);t.setAttribute(o,l)}const a=this.morphAttributes;for(const o in a){const c=[],l=a[o];for(let d=0,h=l.length;d<h;d++){const f=l[d],m=e(f,i);c.push(m)}t.morphAttributes[o]=c}t.morphTargetsRelative=this.morphTargetsRelative;const s=this.groups;for(let o=0,c=s.length;o<c;o++){const l=s[o];t.addGroup(l.start,l.count,l.materialIndex)}return t}toJSON(){const e={metadata:{version:4.6,type:"BufferGeometry",generator:"BufferGeometry.toJSON"}};if(e.uuid=this.uuid,e.type=this.type,this.name!==""&&(e.name=this.name),Object.keys(this.userData).length>0&&(e.userData=this.userData),this.parameters!==void 0){const c=this.parameters;for(const l in c)c[l]!==void 0&&(e[l]=c[l]);return e}e.data={attributes:{}};const t=this.index;t!==null&&(e.data.index={type:t.array.constructor.name,array:Array.prototype.slice.call(t.array)});const i=this.attributes;for(const c in i){const l=i[c];e.data.attributes[c]=l.toJSON(e.data)}const r={};let a=!1;for(const c in this.morphAttributes){const l=this.morphAttributes[c],d=[];for(let h=0,f=l.length;h<f;h++){const m=l[h];d.push(m.toJSON(e.data))}d.length>0&&(r[c]=d,a=!0)}a&&(e.data.morphAttributes=r,e.data.morphTargetsRelative=this.morphTargetsRelative);const s=this.groups;s.length>0&&(e.data.groups=JSON.parse(JSON.stringify(s)));const o=this.boundingSphere;return o!==null&&(e.data.boundingSphere={center:o.center.toArray(),radius:o.radius}),e}clone(){return new this.constructor().copy(this)}copy(e){this.index=null,this.attributes={},this.morphAttributes={},this.groups=[],this.boundingBox=null,this.boundingSphere=null;const t={};this.name=e.name;const i=e.index;i!==null&&this.setIndex(i.clone(t));const r=e.attributes;for(const l in r){const d=r[l];this.setAttribute(l,d.clone(t))}const a=e.morphAttributes;for(const l in a){const d=[],h=a[l];for(let f=0,m=h.length;f<m;f++)d.push(h[f].clone(t));this.morphAttributes[l]=d}this.morphTargetsRelative=e.morphTargetsRelative;const s=e.groups;for(let l=0,d=s.length;l<d;l++){const h=s[l];this.addGroup(h.start,h.count,h.materialIndex)}const o=e.boundingBox;o!==null&&(this.boundingBox=o.clone());const c=e.boundingSphere;return c!==null&&(this.boundingSphere=c.clone()),this.drawRange.start=e.drawRange.start,this.drawRange.count=e.drawRange.count,this.userData=e.userData,this}dispose(){this.dispatchEvent({type:"dispose"})}}const Co=new at,kn=new Gs,vr=new $r,Po=new F,xr=new F,Mr=new F,Sr=new F,Ma=new F,Er=new F,Do=new F,yr=new F;class Le extends Et{constructor(e=new Xe,t=new Ln){super(),this.isMesh=!0,this.type="Mesh",this.geometry=e,this.material=t,this.morphTargetDictionary=void 0,this.morphTargetInfluences=void 0,this.updateMorphTargets()}copy(e,t){return super.copy(e,t),e.morphTargetInfluences!==void 0&&(this.morphTargetInfluences=e.morphTargetInfluences.slice()),e.morphTargetDictionary!==void 0&&(this.morphTargetDictionary=Object.assign({},e.morphTargetDictionary)),this.material=Array.isArray(e.material)?e.material.slice():e.material,this.geometry=e.geometry,this}updateMorphTargets(){const t=this.geometry.morphAttributes,i=Object.keys(t);if(i.length>0){const r=t[i[0]];if(r!==void 0){this.morphTargetInfluences=[],this.morphTargetDictionary={};for(let a=0,s=r.length;a<s;a++){const o=r[a].name||String(a);this.morphTargetInfluences.push(0),this.morphTargetDictionary[o]=a}}}}getVertexPosition(e,t){const i=this.geometry,r=i.attributes.position,a=i.morphAttributes.position,s=i.morphTargetsRelative;t.fromBufferAttribute(r,e);const o=this.morphTargetInfluences;if(a&&o){Er.set(0,0,0);for(let c=0,l=a.length;c<l;c++){const d=o[c],h=a[c];d!==0&&(Ma.fromBufferAttribute(h,e),s?Er.addScaledVector(Ma,d):Er.addScaledVector(Ma.sub(t),d))}t.add(Er)}return t}raycast(e,t){const i=this.geometry,r=this.material,a=this.matrixWorld;r!==void 0&&(i.boundingSphere===null&&i.computeBoundingSphere(),vr.copy(i.boundingSphere),vr.applyMatrix4(a),kn.copy(e.ray).recast(e.near),!(vr.containsPoint(kn.origin)===!1&&(kn.intersectSphere(vr,Po)===null||kn.origin.distanceToSquared(Po)>(e.far-e.near)**2))&&(Co.copy(a).invert(),kn.copy(e.ray).applyMatrix4(Co),!(i.boundingBox!==null&&kn.intersectsBox(i.boundingBox)===!1)&&this._computeIntersections(e,t,kn)))}_computeIntersections(e,t,i){let r;const a=this.geometry,s=this.material,o=a.index,c=a.attributes.position,l=a.attributes.uv,d=a.attributes.uv1,h=a.attributes.normal,f=a.groups,m=a.drawRange;if(o!==null)if(Array.isArray(s))for(let g=0,_=f.length;g<_;g++){const p=f[g],u=s[p.materialIndex],E=Math.max(p.start,m.start),y=Math.min(o.count,Math.min(p.start+p.count,m.start+m.count));for(let M=E,D=y;M<D;M+=3){const A=o.getX(M),b=o.getX(M+1),C=o.getX(M+2);r=br(this,u,e,i,l,d,h,A,b,C),r&&(r.faceIndex=Math.floor(M/3),r.face.materialIndex=p.materialIndex,t.push(r))}}else{const g=Math.max(0,m.start),_=Math.min(o.count,m.start+m.count);for(let p=g,u=_;p<u;p+=3){const E=o.getX(p),y=o.getX(p+1),M=o.getX(p+2);r=br(this,s,e,i,l,d,h,E,y,M),r&&(r.faceIndex=Math.floor(p/3),t.push(r))}}else if(c!==void 0)if(Array.isArray(s))for(let g=0,_=f.length;g<_;g++){const p=f[g],u=s[p.materialIndex],E=Math.max(p.start,m.start),y=Math.min(c.count,Math.min(p.start+p.count,m.start+m.count));for(let M=E,D=y;M<D;M+=3){const A=M,b=M+1,C=M+2;r=br(this,u,e,i,l,d,h,A,b,C),r&&(r.faceIndex=Math.floor(M/3),r.face.materialIndex=p.materialIndex,t.push(r))}}else{const g=Math.max(0,m.start),_=Math.min(c.count,m.start+m.count);for(let p=g,u=_;p<u;p+=3){const E=p,y=p+1,M=p+2;r=br(this,s,e,i,l,d,h,E,y,M),r&&(r.faceIndex=Math.floor(p/3),t.push(r))}}}}function Ru(n,e,t,i,r,a,s,o){let c;if(e.side===Ct?c=i.intersectTriangle(s,a,r,!0,o):c=i.intersectTriangle(r,a,s,e.side===Pn,o),c===null)return null;yr.copy(o),yr.applyMatrix4(n.matrixWorld);const l=t.ray.origin.distanceTo(yr);return l<t.near||l>t.far?null:{distance:l,point:yr.clone(),object:n}}function br(n,e,t,i,r,a,s,o,c,l){n.getVertexPosition(o,xr),n.getVertexPosition(c,Mr),n.getVertexPosition(l,Sr);const d=Ru(n,e,t,i,xr,Mr,Sr,Do);if(d){const h=new F;Gt.getBarycoord(Do,xr,Mr,Sr,h),r&&(d.uv=Gt.getInterpolatedAttribute(r,o,c,l,h,new We)),a&&(d.uv1=Gt.getInterpolatedAttribute(a,o,c,l,h,new We)),s&&(d.normal=Gt.getInterpolatedAttribute(s,o,c,l,h,new F),d.normal.dot(i.direction)>0&&d.normal.multiplyScalar(-1));const f={a:o,b:c,c:l,normal:new F,materialIndex:0};Gt.getNormal(xr,Mr,Sr,f.normal),d.face=f,d.barycoord=h}return d}class Qt extends Xe{constructor(e=1,t=1,i=1,r=1,a=1,s=1){super(),this.type="BoxGeometry",this.parameters={width:e,height:t,depth:i,widthSegments:r,heightSegments:a,depthSegments:s};const o=this;r=Math.floor(r),a=Math.floor(a),s=Math.floor(s);const c=[],l=[],d=[],h=[];let f=0,m=0;g("z","y","x",-1,-1,i,t,e,s,a,0),g("z","y","x",1,-1,i,t,-e,s,a,1),g("x","z","y",1,1,e,i,t,r,s,2),g("x","z","y",1,-1,e,i,-t,r,s,3),g("x","y","z",1,-1,e,t,i,r,a,4),g("x","y","z",-1,-1,e,t,-i,r,a,5),this.setIndex(c),this.setAttribute("position",new je(l,3)),this.setAttribute("normal",new je(d,3)),this.setAttribute("uv",new je(h,2));function g(_,p,u,E,y,M,D,A,b,C,v){const x=M/b,P=D/C,U=M/2,w=D/2,R=A/2,z=b+1,N=C+1;let B=0,k=0;const O=new F;for(let q=0;q<N;q++){const K=q*P-w;for(let le=0;le<z;le++){const De=le*x-U;O[_]=De*E,O[p]=K*y,O[u]=R,l.push(O.x,O.y,O.z),O[_]=0,O[p]=0,O[u]=A>0?1:-1,d.push(O.x,O.y,O.z),h.push(le/b),h.push(1-q/C),B+=1}}for(let q=0;q<C;q++)for(let K=0;K<b;K++){const le=f+K+z*q,De=f+K+z*(q+1),X=f+(K+1)+z*(q+1),J=f+(K+1)+z*q;c.push(le,De,J),c.push(De,X,J),k+=6}o.addGroup(m,k,v),m+=k,f+=B}}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}static fromJSON(e){return new Qt(e.width,e.height,e.depth,e.widthSegments,e.heightSegments,e.depthSegments)}}function zi(n){const e={};for(const t in n){e[t]={};for(const i in n[t]){const r=n[t][i];r&&(r.isColor||r.isMatrix3||r.isMatrix4||r.isVector2||r.isVector3||r.isVector4||r.isTexture||r.isQuaternion)?r.isRenderTargetTexture?(console.warn("UniformsUtils: Textures of render targets cannot be cloned via cloneUniforms() or mergeUniforms()."),e[t][i]=null):e[t][i]=r.clone():Array.isArray(r)?e[t][i]=r.slice():e[t][i]=r}}return e}function Rt(n){const e={};for(let t=0;t<n.length;t++){const i=zi(n[t]);for(const r in i)e[r]=i[r]}return e}function Cu(n){const e=[];for(let t=0;t<n.length;t++)e.push(n[t].clone());return e}function Zc(n){const e=n.getRenderTarget();return e===null?n.outputColorSpace:e.isXRRenderTarget===!0?e.texture.colorSpace:Je.workingColorSpace}const Pu={clone:zi,merge:Rt};var Du=`void main() {
	gl_Position = projectionMatrix * modelViewMatrix * vec4( position, 1.0 );
}`,Lu=`void main() {
	gl_FragColor = vec4( 1.0, 0.0, 0.0, 1.0 );
}`;class Dn extends Bi{constructor(e){super(),this.isShaderMaterial=!0,this.type="ShaderMaterial",this.defines={},this.uniforms={},this.uniformsGroups=[],this.vertexShader=Du,this.fragmentShader=Lu,this.linewidth=1,this.wireframe=!1,this.wireframeLinewidth=1,this.fog=!1,this.lights=!1,this.clipping=!1,this.forceSinglePass=!0,this.extensions={clipCullDistance:!1,multiDraw:!1},this.defaultAttributeValues={color:[1,1,1],uv:[0,0],uv1:[0,0]},this.index0AttributeName=void 0,this.uniformsNeedUpdate=!1,this.glslVersion=null,e!==void 0&&this.setValues(e)}copy(e){return super.copy(e),this.fragmentShader=e.fragmentShader,this.vertexShader=e.vertexShader,this.uniforms=zi(e.uniforms),this.uniformsGroups=Cu(e.uniformsGroups),this.defines=Object.assign({},e.defines),this.wireframe=e.wireframe,this.wireframeLinewidth=e.wireframeLinewidth,this.fog=e.fog,this.lights=e.lights,this.clipping=e.clipping,this.extensions=Object.assign({},e.extensions),this.glslVersion=e.glslVersion,this}toJSON(e){const t=super.toJSON(e);t.glslVersion=this.glslVersion,t.uniforms={};for(const r in this.uniforms){const s=this.uniforms[r].value;s&&s.isTexture?t.uniforms[r]={type:"t",value:s.toJSON(e).uuid}:s&&s.isColor?t.uniforms[r]={type:"c",value:s.getHex()}:s&&s.isVector2?t.uniforms[r]={type:"v2",value:s.toArray()}:s&&s.isVector3?t.uniforms[r]={type:"v3",value:s.toArray()}:s&&s.isVector4?t.uniforms[r]={type:"v4",value:s.toArray()}:s&&s.isMatrix3?t.uniforms[r]={type:"m3",value:s.toArray()}:s&&s.isMatrix4?t.uniforms[r]={type:"m4",value:s.toArray()}:t.uniforms[r]={value:s}}Object.keys(this.defines).length>0&&(t.defines=this.defines),t.vertexShader=this.vertexShader,t.fragmentShader=this.fragmentShader,t.lights=this.lights,t.clipping=this.clipping;const i={};for(const r in this.extensions)this.extensions[r]===!0&&(i[r]=!0);return Object.keys(i).length>0&&(t.extensions=i),t}}class Jc extends Et{constructor(){super(),this.isCamera=!0,this.type="Camera",this.matrixWorldInverse=new at,this.projectionMatrix=new at,this.projectionMatrixInverse=new at,this.coordinateSystem=fn}copy(e,t){return super.copy(e,t),this.matrixWorldInverse.copy(e.matrixWorldInverse),this.projectionMatrix.copy(e.projectionMatrix),this.projectionMatrixInverse.copy(e.projectionMatrixInverse),this.coordinateSystem=e.coordinateSystem,this}getWorldDirection(e){return super.getWorldDirection(e).negate()}updateMatrixWorld(e){super.updateMatrixWorld(e),this.matrixWorldInverse.copy(this.matrixWorld).invert()}updateWorldMatrix(e,t){super.updateWorldMatrix(e,t),this.matrixWorldInverse.copy(this.matrixWorld).invert()}clone(){return new this.constructor().copy(this)}}const Sn=new F,Lo=new We,Io=new We;class kt extends Jc{constructor(e=50,t=1,i=.1,r=2e3){super(),this.isPerspectiveCamera=!0,this.type="PerspectiveCamera",this.fov=e,this.zoom=1,this.near=i,this.far=r,this.focus=10,this.aspect=t,this.view=null,this.filmGauge=35,this.filmOffset=0,this.updateProjectionMatrix()}copy(e,t){return super.copy(e,t),this.fov=e.fov,this.zoom=e.zoom,this.near=e.near,this.far=e.far,this.focus=e.focus,this.aspect=e.aspect,this.view=e.view===null?null:Object.assign({},e.view),this.filmGauge=e.filmGauge,this.filmOffset=e.filmOffset,this}setFocalLength(e){const t=.5*this.getFilmHeight()/e;this.fov=bs*2*Math.atan(t),this.updateProjectionMatrix()}getFocalLength(){const e=Math.tan(Br*.5*this.fov);return .5*this.getFilmHeight()/e}getEffectiveFOV(){return bs*2*Math.atan(Math.tan(Br*.5*this.fov)/this.zoom)}getFilmWidth(){return this.filmGauge*Math.min(this.aspect,1)}getFilmHeight(){return this.filmGauge/Math.max(this.aspect,1)}getViewBounds(e,t,i){Sn.set(-1,-1,.5).applyMatrix4(this.projectionMatrixInverse),t.set(Sn.x,Sn.y).multiplyScalar(-e/Sn.z),Sn.set(1,1,.5).applyMatrix4(this.projectionMatrixInverse),i.set(Sn.x,Sn.y).multiplyScalar(-e/Sn.z)}getViewSize(e,t){return this.getViewBounds(e,Lo,Io),t.subVectors(Io,Lo)}setViewOffset(e,t,i,r,a,s){this.aspect=e/t,this.view===null&&(this.view={enabled:!0,fullWidth:1,fullHeight:1,offsetX:0,offsetY:0,width:1,height:1}),this.view.enabled=!0,this.view.fullWidth=e,this.view.fullHeight=t,this.view.offsetX=i,this.view.offsetY=r,this.view.width=a,this.view.height=s,this.updateProjectionMatrix()}clearViewOffset(){this.view!==null&&(this.view.enabled=!1),this.updateProjectionMatrix()}updateProjectionMatrix(){const e=this.near;let t=e*Math.tan(Br*.5*this.fov)/this.zoom,i=2*t,r=this.aspect*i,a=-.5*r;const s=this.view;if(this.view!==null&&this.view.enabled){const c=s.fullWidth,l=s.fullHeight;a+=s.offsetX*r/c,t-=s.offsetY*i/l,r*=s.width/c,i*=s.height/l}const o=this.filmOffset;o!==0&&(a+=e*o/this.getFilmWidth()),this.projectionMatrix.makePerspective(a,a+r,t,t-i,e,this.far,this.coordinateSystem),this.projectionMatrixInverse.copy(this.projectionMatrix).invert()}toJSON(e){const t=super.toJSON(e);return t.object.fov=this.fov,t.object.zoom=this.zoom,t.object.near=this.near,t.object.far=this.far,t.object.focus=this.focus,t.object.aspect=this.aspect,this.view!==null&&(t.object.view=Object.assign({},this.view)),t.object.filmGauge=this.filmGauge,t.object.filmOffset=this.filmOffset,t}}const _i=-90,vi=1;class Iu extends Et{constructor(e,t,i){super(),this.type="CubeCamera",this.renderTarget=i,this.coordinateSystem=null,this.activeMipmapLevel=0;const r=new kt(_i,vi,e,t);r.layers=this.layers,this.add(r);const a=new kt(_i,vi,e,t);a.layers=this.layers,this.add(a);const s=new kt(_i,vi,e,t);s.layers=this.layers,this.add(s);const o=new kt(_i,vi,e,t);o.layers=this.layers,this.add(o);const c=new kt(_i,vi,e,t);c.layers=this.layers,this.add(c);const l=new kt(_i,vi,e,t);l.layers=this.layers,this.add(l)}updateCoordinateSystem(){const e=this.coordinateSystem,t=this.children.concat(),[i,r,a,s,o,c]=t;for(const l of t)this.remove(l);if(e===fn)i.up.set(0,1,0),i.lookAt(1,0,0),r.up.set(0,1,0),r.lookAt(-1,0,0),a.up.set(0,0,-1),a.lookAt(0,1,0),s.up.set(0,0,1),s.lookAt(0,-1,0),o.up.set(0,1,0),o.lookAt(0,0,1),c.up.set(0,1,0),c.lookAt(0,0,-1);else if(e===jr)i.up.set(0,-1,0),i.lookAt(-1,0,0),r.up.set(0,-1,0),r.lookAt(1,0,0),a.up.set(0,0,1),a.lookAt(0,1,0),s.up.set(0,0,-1),s.lookAt(0,-1,0),o.up.set(0,-1,0),o.lookAt(0,0,1),c.up.set(0,-1,0),c.lookAt(0,0,-1);else throw new Error("THREE.CubeCamera.updateCoordinateSystem(): Invalid coordinate system: "+e);for(const l of t)this.add(l),l.updateMatrixWorld()}update(e,t){this.parent===null&&this.updateMatrixWorld();const{renderTarget:i,activeMipmapLevel:r}=this;this.coordinateSystem!==e.coordinateSystem&&(this.coordinateSystem=e.coordinateSystem,this.updateCoordinateSystem());const[a,s,o,c,l,d]=this.children,h=e.getRenderTarget(),f=e.getActiveCubeFace(),m=e.getActiveMipmapLevel(),g=e.xr.enabled;e.xr.enabled=!1;const _=i.texture.generateMipmaps;i.texture.generateMipmaps=!1,e.setRenderTarget(i,0,r),e.render(t,a),e.setRenderTarget(i,1,r),e.render(t,s),e.setRenderTarget(i,2,r),e.render(t,o),e.setRenderTarget(i,3,r),e.render(t,c),e.setRenderTarget(i,4,r),e.render(t,l),i.texture.generateMipmaps=_,e.setRenderTarget(i,5,r),e.render(t,d),e.setRenderTarget(h,f,m),e.xr.enabled=g,i.texture.needsPMREMUpdate=!0}}class Qc extends wt{constructor(e,t,i,r,a,s,o,c,l,d){e=e!==void 0?e:[],t=t!==void 0?t:Pi,super(e,t,i,r,a,s,o,c,l,d),this.isCubeTexture=!0,this.flipY=!1}get images(){return this.image}set images(e){this.image=e}}class Uu extends ti{constructor(e=1,t={}){super(e,e,t),this.isWebGLCubeRenderTarget=!0;const i={width:e,height:e,depth:1},r=[i,i,i,i,i,i];this.texture=new Qc(r,t.mapping,t.wrapS,t.wrapT,t.magFilter,t.minFilter,t.format,t.type,t.anisotropy,t.colorSpace),this.texture.isRenderTargetTexture=!0,this.texture.generateMipmaps=t.generateMipmaps!==void 0?t.generateMipmaps:!1,this.texture.minFilter=t.minFilter!==void 0?t.minFilter:Jt}fromEquirectangularTexture(e,t){this.texture.type=t.type,this.texture.colorSpace=t.colorSpace,this.texture.generateMipmaps=t.generateMipmaps,this.texture.minFilter=t.minFilter,this.texture.magFilter=t.magFilter;const i={uniforms:{tEquirect:{value:null}},vertexShader:`

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
			`},r=new Qt(5,5,5),a=new Dn({name:"CubemapFromEquirect",uniforms:zi(i.uniforms),vertexShader:i.vertexShader,fragmentShader:i.fragmentShader,side:Ct,blending:Rn});a.uniforms.tEquirect.value=t;const s=new Le(r,a),o=t.minFilter;return t.minFilter===Yn&&(t.minFilter=Jt),new Iu(1,10,this).update(e,s),t.minFilter=o,s.geometry.dispose(),s.material.dispose(),this}clear(e,t,i,r){const a=e.getRenderTarget();for(let s=0;s<6;s++)e.setRenderTarget(this,s),e.clear(t,i,r);e.setRenderTarget(a)}}class Qe extends Et{constructor(){super(),this.isGroup=!0,this.type="Group"}}const zu={type:"move"};class Sa{constructor(){this._targetRay=null,this._grip=null,this._hand=null}getHandSpace(){return this._hand===null&&(this._hand=new Qe,this._hand.matrixAutoUpdate=!1,this._hand.visible=!1,this._hand.joints={},this._hand.inputState={pinching:!1}),this._hand}getTargetRaySpace(){return this._targetRay===null&&(this._targetRay=new Qe,this._targetRay.matrixAutoUpdate=!1,this._targetRay.visible=!1,this._targetRay.hasLinearVelocity=!1,this._targetRay.linearVelocity=new F,this._targetRay.hasAngularVelocity=!1,this._targetRay.angularVelocity=new F),this._targetRay}getGripSpace(){return this._grip===null&&(this._grip=new Qe,this._grip.matrixAutoUpdate=!1,this._grip.visible=!1,this._grip.hasLinearVelocity=!1,this._grip.linearVelocity=new F,this._grip.hasAngularVelocity=!1,this._grip.angularVelocity=new F),this._grip}dispatchEvent(e){return this._targetRay!==null&&this._targetRay.dispatchEvent(e),this._grip!==null&&this._grip.dispatchEvent(e),this._hand!==null&&this._hand.dispatchEvent(e),this}connect(e){if(e&&e.hand){const t=this._hand;if(t)for(const i of e.hand.values())this._getHandJoint(t,i)}return this.dispatchEvent({type:"connected",data:e}),this}disconnect(e){return this.dispatchEvent({type:"disconnected",data:e}),this._targetRay!==null&&(this._targetRay.visible=!1),this._grip!==null&&(this._grip.visible=!1),this._hand!==null&&(this._hand.visible=!1),this}update(e,t,i){let r=null,a=null,s=null;const o=this._targetRay,c=this._grip,l=this._hand;if(e&&t.session.visibilityState!=="visible-blurred"){if(l&&e.hand){s=!0;for(const _ of e.hand.values()){const p=t.getJointPose(_,i),u=this._getHandJoint(l,_);p!==null&&(u.matrix.fromArray(p.transform.matrix),u.matrix.decompose(u.position,u.rotation,u.scale),u.matrixWorldNeedsUpdate=!0,u.jointRadius=p.radius),u.visible=p!==null}const d=l.joints["index-finger-tip"],h=l.joints["thumb-tip"],f=d.position.distanceTo(h.position),m=.02,g=.005;l.inputState.pinching&&f>m+g?(l.inputState.pinching=!1,this.dispatchEvent({type:"pinchend",handedness:e.handedness,target:this})):!l.inputState.pinching&&f<=m-g&&(l.inputState.pinching=!0,this.dispatchEvent({type:"pinchstart",handedness:e.handedness,target:this}))}else c!==null&&e.gripSpace&&(a=t.getPose(e.gripSpace,i),a!==null&&(c.matrix.fromArray(a.transform.matrix),c.matrix.decompose(c.position,c.rotation,c.scale),c.matrixWorldNeedsUpdate=!0,a.linearVelocity?(c.hasLinearVelocity=!0,c.linearVelocity.copy(a.linearVelocity)):c.hasLinearVelocity=!1,a.angularVelocity?(c.hasAngularVelocity=!0,c.angularVelocity.copy(a.angularVelocity)):c.hasAngularVelocity=!1));o!==null&&(r=t.getPose(e.targetRaySpace,i),r===null&&a!==null&&(r=a),r!==null&&(o.matrix.fromArray(r.transform.matrix),o.matrix.decompose(o.position,o.rotation,o.scale),o.matrixWorldNeedsUpdate=!0,r.linearVelocity?(o.hasLinearVelocity=!0,o.linearVelocity.copy(r.linearVelocity)):o.hasLinearVelocity=!1,r.angularVelocity?(o.hasAngularVelocity=!0,o.angularVelocity.copy(r.angularVelocity)):o.hasAngularVelocity=!1,this.dispatchEvent(zu)))}return o!==null&&(o.visible=r!==null),c!==null&&(c.visible=a!==null),l!==null&&(l.visible=s!==null),this}_getHandJoint(e,t){if(e.joints[t.jointName]===void 0){const i=new Qe;i.matrixAutoUpdate=!1,i.visible=!1,e.joints[t.jointName]=i,e.add(i)}return e.joints[t.jointName]}}class el extends Et{constructor(){super(),this.isScene=!0,this.type="Scene",this.background=null,this.environment=null,this.fog=null,this.backgroundBlurriness=0,this.backgroundIntensity=1,this.backgroundRotation=new xt,this.environmentIntensity=1,this.environmentRotation=new xt,this.overrideMaterial=null,typeof __THREE_DEVTOOLS__<"u"&&__THREE_DEVTOOLS__.dispatchEvent(new CustomEvent("observe",{detail:this}))}copy(e,t){return super.copy(e,t),e.background!==null&&(this.background=e.background.clone()),e.environment!==null&&(this.environment=e.environment.clone()),e.fog!==null&&(this.fog=e.fog.clone()),this.backgroundBlurriness=e.backgroundBlurriness,this.backgroundIntensity=e.backgroundIntensity,this.backgroundRotation.copy(e.backgroundRotation),this.environmentIntensity=e.environmentIntensity,this.environmentRotation.copy(e.environmentRotation),e.overrideMaterial!==null&&(this.overrideMaterial=e.overrideMaterial.clone()),this.matrixAutoUpdate=e.matrixAutoUpdate,this}toJSON(e){const t=super.toJSON(e);return this.fog!==null&&(t.object.fog=this.fog.toJSON()),this.backgroundBlurriness>0&&(t.object.backgroundBlurriness=this.backgroundBlurriness),this.backgroundIntensity!==1&&(t.object.backgroundIntensity=this.backgroundIntensity),t.object.backgroundRotation=this.backgroundRotation.toArray(),this.environmentIntensity!==1&&(t.object.environmentIntensity=this.environmentIntensity),t.object.environmentRotation=this.environmentRotation.toArray(),t}}class Nu extends wt{constructor(e=null,t=1,i=1,r,a,s,o,c,l=Ft,d=Ft,h,f){super(null,s,o,c,l,d,r,a,h,f),this.isDataTexture=!0,this.image={data:e,width:t,height:i},this.generateMipmaps=!1,this.flipY=!1,this.unpackAlignment=1}}const Ea=new F,ku=new F,Fu=new Ve;class Gn{constructor(e=new F(1,0,0),t=0){this.isPlane=!0,this.normal=e,this.constant=t}set(e,t){return this.normal.copy(e),this.constant=t,this}setComponents(e,t,i,r){return this.normal.set(e,t,i),this.constant=r,this}setFromNormalAndCoplanarPoint(e,t){return this.normal.copy(e),this.constant=-t.dot(this.normal),this}setFromCoplanarPoints(e,t,i){const r=Ea.subVectors(i,t).cross(ku.subVectors(e,t)).normalize();return this.setFromNormalAndCoplanarPoint(r,e),this}copy(e){return this.normal.copy(e.normal),this.constant=e.constant,this}normalize(){const e=1/this.normal.length();return this.normal.multiplyScalar(e),this.constant*=e,this}negate(){return this.constant*=-1,this.normal.negate(),this}distanceToPoint(e){return this.normal.dot(e)+this.constant}distanceToSphere(e){return this.distanceToPoint(e.center)-e.radius}projectPoint(e,t){return t.copy(e).addScaledVector(this.normal,-this.distanceToPoint(e))}intersectLine(e,t){const i=e.delta(Ea),r=this.normal.dot(i);if(r===0)return this.distanceToPoint(e.start)===0?t.copy(e.start):null;const a=-(e.start.dot(this.normal)+this.constant)/r;return a<0||a>1?null:t.copy(e.start).addScaledVector(i,a)}intersectsLine(e){const t=this.distanceToPoint(e.start),i=this.distanceToPoint(e.end);return t<0&&i>0||i<0&&t>0}intersectsBox(e){return e.intersectsPlane(this)}intersectsSphere(e){return e.intersectsPlane(this)}coplanarPoint(e){return e.copy(this.normal).multiplyScalar(-this.constant)}applyMatrix4(e,t){const i=t||Fu.getNormalMatrix(e),r=this.coplanarPoint(Ea).applyMatrix4(e),a=this.normal.applyMatrix3(i).normalize();return this.constant=-r.dot(a),this}translate(e){return this.constant-=e.dot(this.normal),this}equals(e){return e.normal.equals(this.normal)&&e.constant===this.constant}clone(){return new this.constructor().copy(this)}}const Fn=new $r,Tr=new F;class js{constructor(e=new Gn,t=new Gn,i=new Gn,r=new Gn,a=new Gn,s=new Gn){this.planes=[e,t,i,r,a,s]}set(e,t,i,r,a,s){const o=this.planes;return o[0].copy(e),o[1].copy(t),o[2].copy(i),o[3].copy(r),o[4].copy(a),o[5].copy(s),this}copy(e){const t=this.planes;for(let i=0;i<6;i++)t[i].copy(e.planes[i]);return this}setFromProjectionMatrix(e,t=fn){const i=this.planes,r=e.elements,a=r[0],s=r[1],o=r[2],c=r[3],l=r[4],d=r[5],h=r[6],f=r[7],m=r[8],g=r[9],_=r[10],p=r[11],u=r[12],E=r[13],y=r[14],M=r[15];if(i[0].setComponents(c-a,f-l,p-m,M-u).normalize(),i[1].setComponents(c+a,f+l,p+m,M+u).normalize(),i[2].setComponents(c+s,f+d,p+g,M+E).normalize(),i[3].setComponents(c-s,f-d,p-g,M-E).normalize(),i[4].setComponents(c-o,f-h,p-_,M-y).normalize(),t===fn)i[5].setComponents(c+o,f+h,p+_,M+y).normalize();else if(t===jr)i[5].setComponents(o,h,_,y).normalize();else throw new Error("THREE.Frustum.setFromProjectionMatrix(): Invalid coordinate system: "+t);return this}intersectsObject(e){if(e.boundingSphere!==void 0)e.boundingSphere===null&&e.computeBoundingSphere(),Fn.copy(e.boundingSphere).applyMatrix4(e.matrixWorld);else{const t=e.geometry;t.boundingSphere===null&&t.computeBoundingSphere(),Fn.copy(t.boundingSphere).applyMatrix4(e.matrixWorld)}return this.intersectsSphere(Fn)}intersectsSprite(e){return Fn.center.set(0,0,0),Fn.radius=.7071067811865476,Fn.applyMatrix4(e.matrixWorld),this.intersectsSphere(Fn)}intersectsSphere(e){const t=this.planes,i=e.center,r=-e.radius;for(let a=0;a<6;a++)if(t[a].distanceToPoint(i)<r)return!1;return!0}intersectsBox(e){const t=this.planes;for(let i=0;i<6;i++){const r=t[i];if(Tr.x=r.normal.x>0?e.max.x:e.min.x,Tr.y=r.normal.y>0?e.max.y:e.min.y,Tr.z=r.normal.z>0?e.max.z:e.min.z,r.distanceToPoint(Tr)<0)return!1}return!0}containsPoint(e){const t=this.planes;for(let i=0;i<6;i++)if(t[i].distanceToPoint(e)<0)return!1;return!0}clone(){return new this.constructor().copy(this)}}class lt extends Bi{constructor(e){super(),this.isLineBasicMaterial=!0,this.type="LineBasicMaterial",this.color=new oe(16777215),this.map=null,this.linewidth=1,this.linecap="round",this.linejoin="round",this.fog=!0,this.setValues(e)}copy(e){return super.copy(e),this.color.copy(e.color),this.map=e.map,this.linewidth=e.linewidth,this.linecap=e.linecap,this.linejoin=e.linejoin,this.fog=e.fog,this}}const Xr=new F,qr=new F,Uo=new at,Ki=new Gs,wr=new $r,ya=new F,zo=new F;class Qn extends Et{constructor(e=new Xe,t=new lt){super(),this.isLine=!0,this.type="Line",this.geometry=e,this.material=t,this.morphTargetDictionary=void 0,this.morphTargetInfluences=void 0,this.updateMorphTargets()}copy(e,t){return super.copy(e,t),this.material=Array.isArray(e.material)?e.material.slice():e.material,this.geometry=e.geometry,this}computeLineDistances(){const e=this.geometry;if(e.index===null){const t=e.attributes.position,i=[0];for(let r=1,a=t.count;r<a;r++)Xr.fromBufferAttribute(t,r-1),qr.fromBufferAttribute(t,r),i[r]=i[r-1],i[r]+=Xr.distanceTo(qr);e.setAttribute("lineDistance",new je(i,1))}else console.warn("THREE.Line.computeLineDistances(): Computation only possible with non-indexed BufferGeometry.");return this}raycast(e,t){const i=this.geometry,r=this.matrixWorld,a=e.params.Line.threshold,s=i.drawRange;if(i.boundingSphere===null&&i.computeBoundingSphere(),wr.copy(i.boundingSphere),wr.applyMatrix4(r),wr.radius+=a,e.ray.intersectsSphere(wr)===!1)return;Uo.copy(r).invert(),Ki.copy(e.ray).applyMatrix4(Uo);const o=a/((this.scale.x+this.scale.y+this.scale.z)/3),c=o*o,l=this.isLineSegments?2:1,d=i.index,f=i.attributes.position;if(d!==null){const m=Math.max(0,s.start),g=Math.min(d.count,s.start+s.count);for(let _=m,p=g-1;_<p;_+=l){const u=d.getX(_),E=d.getX(_+1),y=Ar(this,e,Ki,c,u,E,_);y&&t.push(y)}if(this.isLineLoop){const _=d.getX(g-1),p=d.getX(m),u=Ar(this,e,Ki,c,_,p,g-1);u&&t.push(u)}}else{const m=Math.max(0,s.start),g=Math.min(f.count,s.start+s.count);for(let _=m,p=g-1;_<p;_+=l){const u=Ar(this,e,Ki,c,_,_+1,_);u&&t.push(u)}if(this.isLineLoop){const _=Ar(this,e,Ki,c,g-1,m,g-1);_&&t.push(_)}}}updateMorphTargets(){const t=this.geometry.morphAttributes,i=Object.keys(t);if(i.length>0){const r=t[i[0]];if(r!==void 0){this.morphTargetInfluences=[],this.morphTargetDictionary={};for(let a=0,s=r.length;a<s;a++){const o=r[a].name||String(a);this.morphTargetInfluences.push(0),this.morphTargetDictionary[o]=a}}}}}function Ar(n,e,t,i,r,a,s){const o=n.geometry.attributes.position;if(Xr.fromBufferAttribute(o,r),qr.fromBufferAttribute(o,a),t.distanceSqToSegment(Xr,qr,ya,zo)>i)return;ya.applyMatrix4(n.matrixWorld);const l=e.ray.origin.distanceTo(ya);if(!(l<e.near||l>e.far))return{distance:l,point:zo.clone().applyMatrix4(n.matrixWorld),index:s,face:null,faceIndex:null,barycoord:null,object:n}}const No=new F,ko=new F;class ut extends Qn{constructor(e,t){super(e,t),this.isLineSegments=!0,this.type="LineSegments"}computeLineDistances(){const e=this.geometry;if(e.index===null){const t=e.attributes.position,i=[];for(let r=0,a=t.count;r<a;r+=2)No.fromBufferAttribute(t,r),ko.fromBufferAttribute(t,r+1),i[r]=r===0?0:i[r-1],i[r+1]=i[r]+No.distanceTo(ko);e.setAttribute("lineDistance",new je(i,1))}else console.warn("THREE.LineSegments.computeLineDistances(): Computation only possible with non-indexed BufferGeometry.");return this}}class tl extends wt{constructor(e,t,i,r,a,s,o,c,l,d=Ai){if(d!==Ai&&d!==Ii)throw new Error("DepthTexture format must be either THREE.DepthFormat or THREE.DepthStencilFormat");i===void 0&&d===Ai&&(i=ei),i===void 0&&d===Ii&&(i=Li),super(null,r,a,s,o,c,d,i,l),this.isDepthTexture=!0,this.image={width:e,height:t},this.magFilter=o!==void 0?o:Ft,this.minFilter=c!==void 0?c:Ft,this.flipY=!1,this.generateMipmaps=!1,this.compareFunction=null}copy(e){return super.copy(e),this.source=new Vs(Object.assign({},e.image)),this.compareFunction=e.compareFunction,this}toJSON(e){const t=super.toJSON(e);return this.compareFunction!==null&&(t.compareFunction=this.compareFunction),t}}class ar extends Xe{constructor(e=1,t=1,i=1,r=32,a=1,s=!1,o=0,c=Math.PI*2){super(),this.type="CylinderGeometry",this.parameters={radiusTop:e,radiusBottom:t,height:i,radialSegments:r,heightSegments:a,openEnded:s,thetaStart:o,thetaLength:c};const l=this;r=Math.floor(r),a=Math.floor(a);const d=[],h=[],f=[],m=[];let g=0;const _=[],p=i/2;let u=0;E(),s===!1&&(e>0&&y(!0),t>0&&y(!1)),this.setIndex(d),this.setAttribute("position",new je(h,3)),this.setAttribute("normal",new je(f,3)),this.setAttribute("uv",new je(m,2));function E(){const M=new F,D=new F;let A=0;const b=(t-e)/i;for(let C=0;C<=a;C++){const v=[],x=C/a,P=x*(t-e)+e;for(let U=0;U<=r;U++){const w=U/r,R=w*c+o,z=Math.sin(R),N=Math.cos(R);D.x=P*z,D.y=-x*i+p,D.z=P*N,h.push(D.x,D.y,D.z),M.set(z,b,N).normalize(),f.push(M.x,M.y,M.z),m.push(w,1-x),v.push(g++)}_.push(v)}for(let C=0;C<r;C++)for(let v=0;v<a;v++){const x=_[v][C],P=_[v+1][C],U=_[v+1][C+1],w=_[v][C+1];(e>0||v!==0)&&(d.push(x,P,w),A+=3),(t>0||v!==a-1)&&(d.push(P,U,w),A+=3)}l.addGroup(u,A,0),u+=A}function y(M){const D=g,A=new We,b=new F;let C=0;const v=M===!0?e:t,x=M===!0?1:-1;for(let U=1;U<=r;U++)h.push(0,p*x,0),f.push(0,x,0),m.push(.5,.5),g++;const P=g;for(let U=0;U<=r;U++){const R=U/r*c+o,z=Math.cos(R),N=Math.sin(R);b.x=v*N,b.y=p*x,b.z=v*z,h.push(b.x,b.y,b.z),f.push(0,x,0),A.x=z*.5+.5,A.y=N*.5*x+.5,m.push(A.x,A.y),g++}for(let U=0;U<r;U++){const w=D+U,R=P+U;M===!0?d.push(R,R+1,w):d.push(R+1,R,w),C+=3}l.addGroup(u,C,M===!0?1:2),u+=C}}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}static fromJSON(e){return new ar(e.radiusTop,e.radiusBottom,e.height,e.radialSegments,e.heightSegments,e.openEnded,e.thetaStart,e.thetaLength)}}class Ws extends ar{constructor(e=1,t=1,i=32,r=1,a=!1,s=0,o=Math.PI*2){super(0,e,t,i,r,a,s,o),this.type="ConeGeometry",this.parameters={radius:e,height:t,radialSegments:i,heightSegments:r,openEnded:a,thetaStart:s,thetaLength:o}}static fromJSON(e){return new Ws(e.radius,e.height,e.radialSegments,e.heightSegments,e.openEnded,e.thetaStart,e.thetaLength)}}const Rr=new F,Cr=new F,ba=new F,Pr=new Gt;class Qi extends Xe{constructor(e=null,t=1){if(super(),this.type="EdgesGeometry",this.parameters={geometry:e,thresholdAngle:t},e!==null){const r=Math.pow(10,4),a=Math.cos(Br*t),s=e.getIndex(),o=e.getAttribute("position"),c=s?s.count:o.count,l=[0,0,0],d=["a","b","c"],h=new Array(3),f={},m=[];for(let g=0;g<c;g+=3){s?(l[0]=s.getX(g),l[1]=s.getX(g+1),l[2]=s.getX(g+2)):(l[0]=g,l[1]=g+1,l[2]=g+2);const{a:_,b:p,c:u}=Pr;if(_.fromBufferAttribute(o,l[0]),p.fromBufferAttribute(o,l[1]),u.fromBufferAttribute(o,l[2]),Pr.getNormal(ba),h[0]=`${Math.round(_.x*r)},${Math.round(_.y*r)},${Math.round(_.z*r)}`,h[1]=`${Math.round(p.x*r)},${Math.round(p.y*r)},${Math.round(p.z*r)}`,h[2]=`${Math.round(u.x*r)},${Math.round(u.y*r)},${Math.round(u.z*r)}`,!(h[0]===h[1]||h[1]===h[2]||h[2]===h[0]))for(let E=0;E<3;E++){const y=(E+1)%3,M=h[E],D=h[y],A=Pr[d[E]],b=Pr[d[y]],C=`${M}_${D}`,v=`${D}_${M}`;v in f&&f[v]?(ba.dot(f[v].normal)<=a&&(m.push(A.x,A.y,A.z),m.push(b.x,b.y,b.z)),f[v]=null):C in f||(f[C]={index0:l[E],index1:l[y],normal:ba.clone()})}}for(const g in f)if(f[g]){const{index0:_,index1:p}=f[g];Rr.fromBufferAttribute(o,_),Cr.fromBufferAttribute(o,p),m.push(Rr.x,Rr.y,Rr.z),m.push(Cr.x,Cr.y,Cr.z)}this.setAttribute("position",new je(m,3))}}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}}class ii extends Xe{constructor(e=1,t=1,i=1,r=1){super(),this.type="PlaneGeometry",this.parameters={width:e,height:t,widthSegments:i,heightSegments:r};const a=e/2,s=t/2,o=Math.floor(i),c=Math.floor(r),l=o+1,d=c+1,h=e/o,f=t/c,m=[],g=[],_=[],p=[];for(let u=0;u<d;u++){const E=u*f-s;for(let y=0;y<l;y++){const M=y*h-a;g.push(M,-E,0),_.push(0,0,1),p.push(y/o),p.push(1-u/c)}}for(let u=0;u<c;u++)for(let E=0;E<o;E++){const y=E+l*u,M=E+l*(u+1),D=E+1+l*(u+1),A=E+1+l*u;m.push(y,M,A),m.push(M,D,A)}this.setIndex(m),this.setAttribute("position",new je(g,3)),this.setAttribute("normal",new je(_,3)),this.setAttribute("uv",new je(p,2))}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}static fromJSON(e){return new ii(e.width,e.height,e.widthSegments,e.heightSegments)}}class Xs extends Xe{constructor(e=.5,t=1,i=32,r=1,a=0,s=Math.PI*2){super(),this.type="RingGeometry",this.parameters={innerRadius:e,outerRadius:t,thetaSegments:i,phiSegments:r,thetaStart:a,thetaLength:s},i=Math.max(3,i),r=Math.max(1,r);const o=[],c=[],l=[],d=[];let h=e;const f=(t-e)/r,m=new F,g=new We;for(let _=0;_<=r;_++){for(let p=0;p<=i;p++){const u=a+p/i*s;m.x=h*Math.cos(u),m.y=h*Math.sin(u),c.push(m.x,m.y,m.z),l.push(0,0,1),g.x=(m.x/t+1)/2,g.y=(m.y/t+1)/2,d.push(g.x,g.y)}h+=f}for(let _=0;_<r;_++){const p=_*(i+1);for(let u=0;u<i;u++){const E=u+p,y=E,M=E+i+1,D=E+i+2,A=E+1;o.push(y,M,A),o.push(M,D,A)}}this.setIndex(o),this.setAttribute("position",new je(c,3)),this.setAttribute("normal",new je(l,3)),this.setAttribute("uv",new je(d,2))}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}static fromJSON(e){return new Xs(e.innerRadius,e.outerRadius,e.thetaSegments,e.phiSegments,e.thetaStart,e.thetaLength)}}class Yt extends Xe{constructor(e=1,t=32,i=16,r=0,a=Math.PI*2,s=0,o=Math.PI){super(),this.type="SphereGeometry",this.parameters={radius:e,widthSegments:t,heightSegments:i,phiStart:r,phiLength:a,thetaStart:s,thetaLength:o},t=Math.max(3,Math.floor(t)),i=Math.max(2,Math.floor(i));const c=Math.min(s+o,Math.PI);let l=0;const d=[],h=new F,f=new F,m=[],g=[],_=[],p=[];for(let u=0;u<=i;u++){const E=[],y=u/i;let M=0;u===0&&s===0?M=.5/t:u===i&&c===Math.PI&&(M=-.5/t);for(let D=0;D<=t;D++){const A=D/t;h.x=-e*Math.cos(r+A*a)*Math.sin(s+y*o),h.y=e*Math.cos(s+y*o),h.z=e*Math.sin(r+A*a)*Math.sin(s+y*o),g.push(h.x,h.y,h.z),f.copy(h).normalize(),_.push(f.x,f.y,f.z),p.push(A+M,1-y),E.push(l++)}d.push(E)}for(let u=0;u<i;u++)for(let E=0;E<t;E++){const y=d[u][E+1],M=d[u][E],D=d[u+1][E],A=d[u+1][E+1];(u!==0||s>0)&&m.push(y,M,A),(u!==i-1||c<Math.PI)&&m.push(M,D,A)}this.setIndex(m),this.setAttribute("position",new je(g,3)),this.setAttribute("normal",new je(_,3)),this.setAttribute("uv",new je(p,2))}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}static fromJSON(e){return new Yt(e.radius,e.widthSegments,e.heightSegments,e.phiStart,e.phiLength,e.thetaStart,e.thetaLength)}}class Ou extends Xe{constructor(e=null){if(super(),this.type="WireframeGeometry",this.parameters={geometry:e},e!==null){const t=[],i=new Set,r=new F,a=new F;if(e.index!==null){const s=e.attributes.position,o=e.index;let c=e.groups;c.length===0&&(c=[{start:0,count:o.count,materialIndex:0}]);for(let l=0,d=c.length;l<d;++l){const h=c[l],f=h.start,m=h.count;for(let g=f,_=f+m;g<_;g+=3)for(let p=0;p<3;p++){const u=o.getX(g+p),E=o.getX(g+(p+1)%3);r.fromBufferAttribute(s,u),a.fromBufferAttribute(s,E),Fo(r,a,i)===!0&&(t.push(r.x,r.y,r.z),t.push(a.x,a.y,a.z))}}}else{const s=e.attributes.position;for(let o=0,c=s.count/3;o<c;o++)for(let l=0;l<3;l++){const d=3*o+l,h=3*o+(l+1)%3;r.fromBufferAttribute(s,d),a.fromBufferAttribute(s,h),Fo(r,a,i)===!0&&(t.push(r.x,r.y,r.z),t.push(a.x,a.y,a.z))}}this.setAttribute("position",new je(t,3))}}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}}function Fo(n,e,t){const i=`${n.x},${n.y},${n.z}-${e.x},${e.y},${e.z}`,r=`${e.x},${e.y},${e.z}-${n.x},${n.y},${n.z}`;return t.has(i)===!0||t.has(r)===!0?!1:(t.add(i),t.add(r),!0)}class ft extends Bi{constructor(e){super(),this.isMeshStandardMaterial=!0,this.type="MeshStandardMaterial",this.defines={STANDARD:""},this.color=new oe(16777215),this.roughness=1,this.metalness=0,this.map=null,this.lightMap=null,this.lightMapIntensity=1,this.aoMap=null,this.aoMapIntensity=1,this.emissive=new oe(0),this.emissiveIntensity=1,this.emissiveMap=null,this.bumpMap=null,this.bumpScale=1,this.normalMap=null,this.normalMapType=jc,this.normalScale=new We(1,1),this.displacementMap=null,this.displacementScale=1,this.displacementBias=0,this.roughnessMap=null,this.metalnessMap=null,this.alphaMap=null,this.envMap=null,this.envMapRotation=new xt,this.envMapIntensity=1,this.wireframe=!1,this.wireframeLinewidth=1,this.wireframeLinecap="round",this.wireframeLinejoin="round",this.flatShading=!1,this.fog=!0,this.setValues(e)}copy(e){return super.copy(e),this.defines={STANDARD:""},this.color.copy(e.color),this.roughness=e.roughness,this.metalness=e.metalness,this.map=e.map,this.lightMap=e.lightMap,this.lightMapIntensity=e.lightMapIntensity,this.aoMap=e.aoMap,this.aoMapIntensity=e.aoMapIntensity,this.emissive.copy(e.emissive),this.emissiveMap=e.emissiveMap,this.emissiveIntensity=e.emissiveIntensity,this.bumpMap=e.bumpMap,this.bumpScale=e.bumpScale,this.normalMap=e.normalMap,this.normalMapType=e.normalMapType,this.normalScale.copy(e.normalScale),this.displacementMap=e.displacementMap,this.displacementScale=e.displacementScale,this.displacementBias=e.displacementBias,this.roughnessMap=e.roughnessMap,this.metalnessMap=e.metalnessMap,this.alphaMap=e.alphaMap,this.envMap=e.envMap,this.envMapRotation.copy(e.envMapRotation),this.envMapIntensity=e.envMapIntensity,this.wireframe=e.wireframe,this.wireframeLinewidth=e.wireframeLinewidth,this.wireframeLinecap=e.wireframeLinecap,this.wireframeLinejoin=e.wireframeLinejoin,this.flatShading=e.flatShading,this.fog=e.fog,this}}class Bu extends ft{constructor(e){super(),this.isMeshPhysicalMaterial=!0,this.defines={STANDARD:"",PHYSICAL:""},this.type="MeshPhysicalMaterial",this.anisotropyRotation=0,this.anisotropyMap=null,this.clearcoatMap=null,this.clearcoatRoughness=0,this.clearcoatRoughnessMap=null,this.clearcoatNormalScale=new We(1,1),this.clearcoatNormalMap=null,this.ior=1.5,Object.defineProperty(this,"reflectivity",{get:function(){return qe(2.5*(this.ior-1)/(this.ior+1),0,1)},set:function(t){this.ior=(1+.4*t)/(1-.4*t)}}),this.iridescenceMap=null,this.iridescenceIOR=1.3,this.iridescenceThicknessRange=[100,400],this.iridescenceThicknessMap=null,this.sheenColor=new oe(0),this.sheenColorMap=null,this.sheenRoughness=1,this.sheenRoughnessMap=null,this.transmissionMap=null,this.thickness=0,this.thicknessMap=null,this.attenuationDistance=1/0,this.attenuationColor=new oe(1,1,1),this.specularIntensity=1,this.specularIntensityMap=null,this.specularColor=new oe(1,1,1),this.specularColorMap=null,this._anisotropy=0,this._clearcoat=0,this._dispersion=0,this._iridescence=0,this._sheen=0,this._transmission=0,this.setValues(e)}get anisotropy(){return this._anisotropy}set anisotropy(e){this._anisotropy>0!=e>0&&this.version++,this._anisotropy=e}get clearcoat(){return this._clearcoat}set clearcoat(e){this._clearcoat>0!=e>0&&this.version++,this._clearcoat=e}get iridescence(){return this._iridescence}set iridescence(e){this._iridescence>0!=e>0&&this.version++,this._iridescence=e}get dispersion(){return this._dispersion}set dispersion(e){this._dispersion>0!=e>0&&this.version++,this._dispersion=e}get sheen(){return this._sheen}set sheen(e){this._sheen>0!=e>0&&this.version++,this._sheen=e}get transmission(){return this._transmission}set transmission(e){this._transmission>0!=e>0&&this.version++,this._transmission=e}copy(e){return super.copy(e),this.defines={STANDARD:"",PHYSICAL:""},this.anisotropy=e.anisotropy,this.anisotropyRotation=e.anisotropyRotation,this.anisotropyMap=e.anisotropyMap,this.clearcoat=e.clearcoat,this.clearcoatMap=e.clearcoatMap,this.clearcoatRoughness=e.clearcoatRoughness,this.clearcoatRoughnessMap=e.clearcoatRoughnessMap,this.clearcoatNormalMap=e.clearcoatNormalMap,this.clearcoatNormalScale.copy(e.clearcoatNormalScale),this.dispersion=e.dispersion,this.ior=e.ior,this.iridescence=e.iridescence,this.iridescenceMap=e.iridescenceMap,this.iridescenceIOR=e.iridescenceIOR,this.iridescenceThicknessRange=[...e.iridescenceThicknessRange],this.iridescenceThicknessMap=e.iridescenceThicknessMap,this.sheen=e.sheen,this.sheenColor.copy(e.sheenColor),this.sheenColorMap=e.sheenColorMap,this.sheenRoughness=e.sheenRoughness,this.sheenRoughnessMap=e.sheenRoughnessMap,this.transmission=e.transmission,this.transmissionMap=e.transmissionMap,this.thickness=e.thickness,this.thicknessMap=e.thicknessMap,this.attenuationDistance=e.attenuationDistance,this.attenuationColor.copy(e.attenuationColor),this.specularIntensity=e.specularIntensity,this.specularIntensityMap=e.specularIntensityMap,this.specularColor.copy(e.specularColor),this.specularColorMap=e.specularColorMap,this}}class Vu extends Bi{constructor(e){super(),this.isMeshDepthMaterial=!0,this.type="MeshDepthMaterial",this.depthPacking=Zl,this.map=null,this.alphaMap=null,this.displacementMap=null,this.displacementScale=1,this.displacementBias=0,this.wireframe=!1,this.wireframeLinewidth=1,this.setValues(e)}copy(e){return super.copy(e),this.depthPacking=e.depthPacking,this.map=e.map,this.alphaMap=e.alphaMap,this.displacementMap=e.displacementMap,this.displacementScale=e.displacementScale,this.displacementBias=e.displacementBias,this.wireframe=e.wireframe,this.wireframeLinewidth=e.wireframeLinewidth,this}}class Gu extends Bi{constructor(e){super(),this.isMeshDistanceMaterial=!0,this.type="MeshDistanceMaterial",this.map=null,this.alphaMap=null,this.displacementMap=null,this.displacementScale=1,this.displacementBias=0,this.setValues(e)}copy(e){return super.copy(e),this.map=e.map,this.alphaMap=e.alphaMap,this.displacementMap=e.displacementMap,this.displacementScale=e.displacementScale,this.displacementBias=e.displacementBias,this}}class Hu extends lt{constructor(e){super(),this.isLineDashedMaterial=!0,this.type="LineDashedMaterial",this.scale=1,this.dashSize=3,this.gapSize=1,this.setValues(e)}copy(e){return super.copy(e),this.scale=e.scale,this.dashSize=e.dashSize,this.gapSize=e.gapSize,this}}class qs extends Et{constructor(e,t=1){super(),this.isLight=!0,this.type="Light",this.color=new oe(e),this.intensity=t}dispose(){}copy(e,t){return super.copy(e,t),this.color.copy(e.color),this.intensity=e.intensity,this}toJSON(e){const t=super.toJSON(e);return t.object.color=this.color.getHex(),t.object.intensity=this.intensity,this.groundColor!==void 0&&(t.object.groundColor=this.groundColor.getHex()),this.distance!==void 0&&(t.object.distance=this.distance),this.angle!==void 0&&(t.object.angle=this.angle),this.decay!==void 0&&(t.object.decay=this.decay),this.penumbra!==void 0&&(t.object.penumbra=this.penumbra),this.shadow!==void 0&&(t.object.shadow=this.shadow.toJSON()),this.target!==void 0&&(t.object.target=this.target.uuid),t}}const Ta=new at,Oo=new F,Bo=new F;class nl{constructor(e){this.camera=e,this.intensity=1,this.bias=0,this.normalBias=0,this.radius=1,this.blurSamples=8,this.mapSize=new We(512,512),this.map=null,this.mapPass=null,this.matrix=new at,this.autoUpdate=!0,this.needsUpdate=!1,this._frustum=new js,this._frameExtents=new We(1,1),this._viewportCount=1,this._viewports=[new rt(0,0,1,1)]}getViewportCount(){return this._viewportCount}getFrustum(){return this._frustum}updateMatrices(e){const t=this.camera,i=this.matrix;Oo.setFromMatrixPosition(e.matrixWorld),t.position.copy(Oo),Bo.setFromMatrixPosition(e.target.matrixWorld),t.lookAt(Bo),t.updateMatrixWorld(),Ta.multiplyMatrices(t.projectionMatrix,t.matrixWorldInverse),this._frustum.setFromProjectionMatrix(Ta),i.set(.5,0,0,.5,0,.5,0,.5,0,0,.5,.5,0,0,0,1),i.multiply(Ta)}getViewport(e){return this._viewports[e]}getFrameExtents(){return this._frameExtents}dispose(){this.map&&this.map.dispose(),this.mapPass&&this.mapPass.dispose()}copy(e){return this.camera=e.camera.clone(),this.intensity=e.intensity,this.bias=e.bias,this.radius=e.radius,this.mapSize.copy(e.mapSize),this}clone(){return new this.constructor().copy(this)}toJSON(){const e={};return this.intensity!==1&&(e.intensity=this.intensity),this.bias!==0&&(e.bias=this.bias),this.normalBias!==0&&(e.normalBias=this.normalBias),this.radius!==1&&(e.radius=this.radius),(this.mapSize.x!==512||this.mapSize.y!==512)&&(e.mapSize=this.mapSize.toArray()),e.camera=this.camera.toJSON(!1).object,delete e.camera.matrix,e}}const Vo=new at,$i=new F,wa=new F;class ju extends nl{constructor(){super(new kt(90,1,.5,500)),this.isPointLightShadow=!0,this._frameExtents=new We(4,2),this._viewportCount=6,this._viewports=[new rt(2,1,1,1),new rt(0,1,1,1),new rt(3,1,1,1),new rt(1,1,1,1),new rt(3,0,1,1),new rt(1,0,1,1)],this._cubeDirections=[new F(1,0,0),new F(-1,0,0),new F(0,0,1),new F(0,0,-1),new F(0,1,0),new F(0,-1,0)],this._cubeUps=[new F(0,1,0),new F(0,1,0),new F(0,1,0),new F(0,1,0),new F(0,0,1),new F(0,0,-1)]}updateMatrices(e,t=0){const i=this.camera,r=this.matrix,a=e.distance||i.far;a!==i.far&&(i.far=a,i.updateProjectionMatrix()),$i.setFromMatrixPosition(e.matrixWorld),i.position.copy($i),wa.copy(i.position),wa.add(this._cubeDirections[t]),i.up.copy(this._cubeUps[t]),i.lookAt(wa),i.updateMatrixWorld(),r.makeTranslation(-$i.x,-$i.y,-$i.z),Vo.multiplyMatrices(i.projectionMatrix,i.matrixWorldInverse),this._frustum.setFromProjectionMatrix(Vo)}}class Wu extends qs{constructor(e,t,i=0,r=2){super(e,t),this.isPointLight=!0,this.type="PointLight",this.distance=i,this.decay=r,this.shadow=new ju}get power(){return this.intensity*4*Math.PI}set power(e){this.intensity=e/(4*Math.PI)}dispose(){this.shadow.dispose()}copy(e,t){return super.copy(e,t),this.distance=e.distance,this.decay=e.decay,this.shadow=e.shadow.clone(),this}}class il extends Jc{constructor(e=-1,t=1,i=1,r=-1,a=.1,s=2e3){super(),this.isOrthographicCamera=!0,this.type="OrthographicCamera",this.zoom=1,this.view=null,this.left=e,this.right=t,this.top=i,this.bottom=r,this.near=a,this.far=s,this.updateProjectionMatrix()}copy(e,t){return super.copy(e,t),this.left=e.left,this.right=e.right,this.top=e.top,this.bottom=e.bottom,this.near=e.near,this.far=e.far,this.zoom=e.zoom,this.view=e.view===null?null:Object.assign({},e.view),this}setViewOffset(e,t,i,r,a,s){this.view===null&&(this.view={enabled:!0,fullWidth:1,fullHeight:1,offsetX:0,offsetY:0,width:1,height:1}),this.view.enabled=!0,this.view.fullWidth=e,this.view.fullHeight=t,this.view.offsetX=i,this.view.offsetY=r,this.view.width=a,this.view.height=s,this.updateProjectionMatrix()}clearViewOffset(){this.view!==null&&(this.view.enabled=!1),this.updateProjectionMatrix()}updateProjectionMatrix(){const e=(this.right-this.left)/(2*this.zoom),t=(this.top-this.bottom)/(2*this.zoom),i=(this.right+this.left)/2,r=(this.top+this.bottom)/2;let a=i-e,s=i+e,o=r+t,c=r-t;if(this.view!==null&&this.view.enabled){const l=(this.right-this.left)/this.view.fullWidth/this.zoom,d=(this.top-this.bottom)/this.view.fullHeight/this.zoom;a+=l*this.view.offsetX,s=a+l*this.view.width,o-=d*this.view.offsetY,c=o-d*this.view.height}this.projectionMatrix.makeOrthographic(a,s,o,c,this.near,this.far,this.coordinateSystem),this.projectionMatrixInverse.copy(this.projectionMatrix).invert()}toJSON(e){const t=super.toJSON(e);return t.object.zoom=this.zoom,t.object.left=this.left,t.object.right=this.right,t.object.top=this.top,t.object.bottom=this.bottom,t.object.near=this.near,t.object.far=this.far,this.view!==null&&(t.object.view=Object.assign({},this.view)),t}}class Xu extends nl{constructor(){super(new il(-5,5,5,-5,.5,500)),this.isDirectionalLightShadow=!0}}class Go extends qs{constructor(e,t){super(e,t),this.isDirectionalLight=!0,this.type="DirectionalLight",this.position.copy(Et.DEFAULT_UP),this.updateMatrix(),this.target=new Et,this.shadow=new Xu}dispose(){this.shadow.dispose()}copy(e){return super.copy(e),this.target=e.target.clone(),this.shadow=e.shadow.clone(),this}}class qu extends qs{constructor(e,t){super(e,t),this.isAmbientLight=!0,this.type="AmbientLight"}}class Ku extends kt{constructor(e=[]){super(),this.isArrayCamera=!0,this.cameras=e,this.index=0}}const Ho=new at;class Ks{constructor(e,t,i=0,r=1/0){this.ray=new Gs(e,t),this.near=i,this.far=r,this.camera=null,this.layers=new Hs,this.params={Mesh:{},Line:{threshold:1},LOD:{},Points:{threshold:1},Sprite:{}}}set(e,t){this.ray.set(e,t)}setFromCamera(e,t){t.isPerspectiveCamera?(this.ray.origin.setFromMatrixPosition(t.matrixWorld),this.ray.direction.set(e.x,e.y,.5).unproject(t).sub(this.ray.origin).normalize(),this.camera=t):t.isOrthographicCamera?(this.ray.origin.set(e.x,e.y,(t.near+t.far)/(t.near-t.far)).unproject(t),this.ray.direction.set(0,0,-1).transformDirection(t.matrixWorld),this.camera=t):console.error("THREE.Raycaster: Unsupported camera type: "+t.type)}setFromXRController(e){return Ho.identity().extractRotation(e.matrixWorld),this.ray.origin.setFromMatrixPosition(e.matrixWorld),this.ray.direction.set(0,0,-1).applyMatrix4(Ho),this}intersectObject(e,t=!0,i=[]){return Ts(e,this,i,t),i.sort(jo),i}intersectObjects(e,t=!0,i=[]){for(let r=0,a=e.length;r<a;r++)Ts(e[r],this,i,t);return i.sort(jo),i}}function jo(n,e){return n.distance-e.distance}function Ts(n,e,t,i){let r=!0;if(n.layers.test(e.layers)&&n.raycast(e,t)===!1&&(r=!1),r===!0&&i===!0){const a=n.children;for(let s=0,o=a.length;s<o;s++)Ts(a[s],e,t,!0)}}function Wo(n,e,t,i){const r=$u(i);switch(t){case kc:return n*e;case Oc:return n*e;case Bc:return n*e*2;case Vc:return n*e/r.components*r.byteLength;case Fs:return n*e/r.components*r.byteLength;case Gc:return n*e*2/r.components*r.byteLength;case Os:return n*e*2/r.components*r.byteLength;case Fc:return n*e*3/r.components*r.byteLength;case Ht:return n*e*4/r.components*r.byteLength;case Bs:return n*e*4/r.components*r.byteLength;case zr:case Nr:return Math.floor((n+3)/4)*Math.floor((e+3)/4)*8;case kr:case Fr:return Math.floor((n+3)/4)*Math.floor((e+3)/4)*16;case Qa:case ts:return Math.max(n,16)*Math.max(e,8)/4;case Ja:case es:return Math.max(n,8)*Math.max(e,8)/2;case ns:case is:return Math.floor((n+3)/4)*Math.floor((e+3)/4)*8;case rs:return Math.floor((n+3)/4)*Math.floor((e+3)/4)*16;case as:return Math.floor((n+3)/4)*Math.floor((e+3)/4)*16;case ss:return Math.floor((n+4)/5)*Math.floor((e+3)/4)*16;case os:return Math.floor((n+4)/5)*Math.floor((e+4)/5)*16;case cs:return Math.floor((n+5)/6)*Math.floor((e+4)/5)*16;case ls:return Math.floor((n+5)/6)*Math.floor((e+5)/6)*16;case us:return Math.floor((n+7)/8)*Math.floor((e+4)/5)*16;case ds:return Math.floor((n+7)/8)*Math.floor((e+5)/6)*16;case hs:return Math.floor((n+7)/8)*Math.floor((e+7)/8)*16;case fs:return Math.floor((n+9)/10)*Math.floor((e+4)/5)*16;case ps:return Math.floor((n+9)/10)*Math.floor((e+5)/6)*16;case ms:return Math.floor((n+9)/10)*Math.floor((e+7)/8)*16;case gs:return Math.floor((n+9)/10)*Math.floor((e+9)/10)*16;case _s:return Math.floor((n+11)/12)*Math.floor((e+9)/10)*16;case vs:return Math.floor((n+11)/12)*Math.floor((e+11)/12)*16;case Or:case xs:case Ms:return Math.ceil(n/4)*Math.ceil(e/4)*16;case Hc:case Ss:return Math.ceil(n/4)*Math.ceil(e/4)*8;case Es:case ys:return Math.ceil(n/4)*Math.ceil(e/4)*16}throw new Error(`Unable to determine texture byte length for ${t} format.`)}function $u(n){switch(n){case mn:case Uc:return{byteLength:1,components:1};case Ji:case zc:case ir:return{byteLength:2,components:1};case Ns:case ks:return{byteLength:2,components:4};case ei:case zs:case hn:return{byteLength:4,components:1};case Nc:return{byteLength:4,components:3}}throw new Error(`Unknown texture type ${n}.`)}typeof __THREE_DEVTOOLS__<"u"&&__THREE_DEVTOOLS__.dispatchEvent(new CustomEvent("register",{detail:{revision:Us}}));typeof window<"u"&&(window.__THREE__?console.warn("WARNING: Multiple instances of Three.js being imported."):window.__THREE__=Us);/**
 * @license
 * Copyright 2010-2025 Three.js Authors
 * SPDX-License-Identifier: MIT
 */function rl(){let n=null,e=!1,t=null,i=null;function r(a,s){t(a,s),i=n.requestAnimationFrame(r)}return{start:function(){e!==!0&&t!==null&&(i=n.requestAnimationFrame(r),e=!0)},stop:function(){n.cancelAnimationFrame(i),e=!1},setAnimationLoop:function(a){t=a},setContext:function(a){n=a}}}function Yu(n){const e=new WeakMap;function t(o,c){const l=o.array,d=o.usage,h=l.byteLength,f=n.createBuffer();n.bindBuffer(c,f),n.bufferData(c,l,d),o.onUploadCallback();let m;if(l instanceof Float32Array)m=n.FLOAT;else if(l instanceof Uint16Array)o.isFloat16BufferAttribute?m=n.HALF_FLOAT:m=n.UNSIGNED_SHORT;else if(l instanceof Int16Array)m=n.SHORT;else if(l instanceof Uint32Array)m=n.UNSIGNED_INT;else if(l instanceof Int32Array)m=n.INT;else if(l instanceof Int8Array)m=n.BYTE;else if(l instanceof Uint8Array)m=n.UNSIGNED_BYTE;else if(l instanceof Uint8ClampedArray)m=n.UNSIGNED_BYTE;else throw new Error("THREE.WebGLAttributes: Unsupported buffer data format: "+l);return{buffer:f,type:m,bytesPerElement:l.BYTES_PER_ELEMENT,version:o.version,size:h}}function i(o,c,l){const d=c.array,h=c.updateRanges;if(n.bindBuffer(l,o),h.length===0)n.bufferSubData(l,0,d);else{h.sort((m,g)=>m.start-g.start);let f=0;for(let m=1;m<h.length;m++){const g=h[f],_=h[m];_.start<=g.start+g.count+1?g.count=Math.max(g.count,_.start+_.count-g.start):(++f,h[f]=_)}h.length=f+1;for(let m=0,g=h.length;m<g;m++){const _=h[m];n.bufferSubData(l,_.start*d.BYTES_PER_ELEMENT,d,_.start,_.count)}c.clearUpdateRanges()}c.onUploadCallback()}function r(o){return o.isInterleavedBufferAttribute&&(o=o.data),e.get(o)}function a(o){o.isInterleavedBufferAttribute&&(o=o.data);const c=e.get(o);c&&(n.deleteBuffer(c.buffer),e.delete(o))}function s(o,c){if(o.isInterleavedBufferAttribute&&(o=o.data),o.isGLBufferAttribute){const d=e.get(o);(!d||d.version<o.version)&&e.set(o,{buffer:o.buffer,type:o.type,bytesPerElement:o.elementSize,version:o.version});return}const l=e.get(o);if(l===void 0)e.set(o,t(o,c));else if(l.version<o.version){if(l.size!==o.array.byteLength)throw new Error("THREE.WebGLAttributes: The size of the buffer attribute's array buffer does not match the original size. Resizing buffer attributes is not supported.");i(l.buffer,o,c),l.version=o.version}}return{get:r,remove:a,update:s}}var Zu=`#ifdef USE_ALPHAHASH
	if ( diffuseColor.a < getAlphaHashThreshold( vPosition ) ) discard;
#endif`,Ju=`#ifdef USE_ALPHAHASH
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
#endif`,Qu=`#ifdef USE_ALPHAMAP
	diffuseColor.a *= texture2D( alphaMap, vAlphaMapUv ).g;
#endif`,ed=`#ifdef USE_ALPHAMAP
	uniform sampler2D alphaMap;
#endif`,td=`#ifdef USE_ALPHATEST
	#ifdef ALPHA_TO_COVERAGE
	diffuseColor.a = smoothstep( alphaTest, alphaTest + fwidth( diffuseColor.a ), diffuseColor.a );
	if ( diffuseColor.a == 0.0 ) discard;
	#else
	if ( diffuseColor.a < alphaTest ) discard;
	#endif
#endif`,nd=`#ifdef USE_ALPHATEST
	uniform float alphaTest;
#endif`,id=`#ifdef USE_AOMAP
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
#endif`,rd=`#ifdef USE_AOMAP
	uniform sampler2D aoMap;
	uniform float aoMapIntensity;
#endif`,ad=`#ifdef USE_BATCHING
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
#endif`,sd=`#ifdef USE_BATCHING
	mat4 batchingMatrix = getBatchingMatrix( getIndirectIndex( gl_DrawID ) );
#endif`,od=`vec3 transformed = vec3( position );
#ifdef USE_ALPHAHASH
	vPosition = vec3( position );
#endif`,cd=`vec3 objectNormal = vec3( normal );
#ifdef USE_TANGENT
	vec3 objectTangent = vec3( tangent.xyz );
#endif`,ld=`float G_BlinnPhong_Implicit( ) {
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
} // validated`,ud=`#ifdef USE_IRIDESCENCE
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
#endif`,dd=`#ifdef USE_BUMPMAP
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
#endif`,hd=`#if NUM_CLIPPING_PLANES > 0
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
#endif`,fd=`#if NUM_CLIPPING_PLANES > 0
	varying vec3 vClipPosition;
	uniform vec4 clippingPlanes[ NUM_CLIPPING_PLANES ];
#endif`,pd=`#if NUM_CLIPPING_PLANES > 0
	varying vec3 vClipPosition;
#endif`,md=`#if NUM_CLIPPING_PLANES > 0
	vClipPosition = - mvPosition.xyz;
#endif`,gd=`#if defined( USE_COLOR_ALPHA )
	diffuseColor *= vColor;
#elif defined( USE_COLOR )
	diffuseColor.rgb *= vColor;
#endif`,_d=`#if defined( USE_COLOR_ALPHA )
	varying vec4 vColor;
#elif defined( USE_COLOR )
	varying vec3 vColor;
#endif`,vd=`#if defined( USE_COLOR_ALPHA )
	varying vec4 vColor;
#elif defined( USE_COLOR ) || defined( USE_INSTANCING_COLOR ) || defined( USE_BATCHING_COLOR )
	varying vec3 vColor;
#endif`,xd=`#if defined( USE_COLOR_ALPHA )
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
#endif`,Md=`#define PI 3.141592653589793
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
} // validated`,Sd=`#ifdef ENVMAP_TYPE_CUBE_UV
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
#endif`,Ed=`vec3 transformedNormal = objectNormal;
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
#endif`,yd=`#ifdef USE_DISPLACEMENTMAP
	uniform sampler2D displacementMap;
	uniform float displacementScale;
	uniform float displacementBias;
#endif`,bd=`#ifdef USE_DISPLACEMENTMAP
	transformed += normalize( objectNormal ) * ( texture2D( displacementMap, vDisplacementMapUv ).x * displacementScale + displacementBias );
#endif`,Td=`#ifdef USE_EMISSIVEMAP
	vec4 emissiveColor = texture2D( emissiveMap, vEmissiveMapUv );
	#ifdef DECODE_VIDEO_TEXTURE_EMISSIVE
		emissiveColor = sRGBTransferEOTF( emissiveColor );
	#endif
	totalEmissiveRadiance *= emissiveColor.rgb;
#endif`,wd=`#ifdef USE_EMISSIVEMAP
	uniform sampler2D emissiveMap;
#endif`,Ad="gl_FragColor = linearToOutputTexel( gl_FragColor );",Rd=`vec4 LinearTransferOETF( in vec4 value ) {
	return value;
}
vec4 sRGBTransferEOTF( in vec4 value ) {
	return vec4( mix( pow( value.rgb * 0.9478672986 + vec3( 0.0521327014 ), vec3( 2.4 ) ), value.rgb * 0.0773993808, vec3( lessThanEqual( value.rgb, vec3( 0.04045 ) ) ) ), value.a );
}
vec4 sRGBTransferOETF( in vec4 value ) {
	return vec4( mix( pow( value.rgb, vec3( 0.41666 ) ) * 1.055 - vec3( 0.055 ), value.rgb * 12.92, vec3( lessThanEqual( value.rgb, vec3( 0.0031308 ) ) ) ), value.a );
}`,Cd=`#ifdef USE_ENVMAP
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
#endif`,Pd=`#ifdef USE_ENVMAP
	uniform float envMapIntensity;
	uniform float flipEnvMap;
	uniform mat3 envMapRotation;
	#ifdef ENVMAP_TYPE_CUBE
		uniform samplerCube envMap;
	#else
		uniform sampler2D envMap;
	#endif
	
#endif`,Dd=`#ifdef USE_ENVMAP
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
#endif`,Ld=`#ifdef USE_ENVMAP
	#if defined( USE_BUMPMAP ) || defined( USE_NORMALMAP ) || defined( PHONG ) || defined( LAMBERT )
		#define ENV_WORLDPOS
	#endif
	#ifdef ENV_WORLDPOS
		
		varying vec3 vWorldPosition;
	#else
		varying vec3 vReflect;
		uniform float refractionRatio;
	#endif
#endif`,Id=`#ifdef USE_ENVMAP
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
#endif`,Ud=`#ifdef USE_FOG
	vFogDepth = - mvPosition.z;
#endif`,zd=`#ifdef USE_FOG
	varying float vFogDepth;
#endif`,Nd=`#ifdef USE_FOG
	#ifdef FOG_EXP2
		float fogFactor = 1.0 - exp( - fogDensity * fogDensity * vFogDepth * vFogDepth );
	#else
		float fogFactor = smoothstep( fogNear, fogFar, vFogDepth );
	#endif
	gl_FragColor.rgb = mix( gl_FragColor.rgb, fogColor, fogFactor );
#endif`,kd=`#ifdef USE_FOG
	uniform vec3 fogColor;
	varying float vFogDepth;
	#ifdef FOG_EXP2
		uniform float fogDensity;
	#else
		uniform float fogNear;
		uniform float fogFar;
	#endif
#endif`,Fd=`#ifdef USE_GRADIENTMAP
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
}`,Od=`#ifdef USE_LIGHTMAP
	uniform sampler2D lightMap;
	uniform float lightMapIntensity;
#endif`,Bd=`LambertMaterial material;
material.diffuseColor = diffuseColor.rgb;
material.specularStrength = specularStrength;`,Vd=`varying vec3 vViewPosition;
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
#define RE_IndirectDiffuse		RE_IndirectDiffuse_Lambert`,Gd=`uniform bool receiveShadow;
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
#endif`,Hd=`#ifdef USE_ENVMAP
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
#endif`,jd=`ToonMaterial material;
material.diffuseColor = diffuseColor.rgb;`,Wd=`varying vec3 vViewPosition;
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
#define RE_IndirectDiffuse		RE_IndirectDiffuse_Toon`,Xd=`BlinnPhongMaterial material;
material.diffuseColor = diffuseColor.rgb;
material.specularColor = specular;
material.specularShininess = shininess;
material.specularStrength = specularStrength;`,qd=`varying vec3 vViewPosition;
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
#define RE_IndirectDiffuse		RE_IndirectDiffuse_BlinnPhong`,Kd=`PhysicalMaterial material;
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
#endif`,$d=`struct PhysicalMaterial {
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
}`,Yd=`
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
#endif`,Zd=`#if defined( RE_IndirectDiffuse )
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
#endif`,Jd=`#if defined( RE_IndirectDiffuse )
	RE_IndirectDiffuse( irradiance, geometryPosition, geometryNormal, geometryViewDir, geometryClearcoatNormal, material, reflectedLight );
#endif
#if defined( RE_IndirectSpecular )
	RE_IndirectSpecular( radiance, iblIrradiance, clearcoatRadiance, geometryPosition, geometryNormal, geometryViewDir, geometryClearcoatNormal, material, reflectedLight );
#endif`,Qd=`#if defined( USE_LOGDEPTHBUF )
	gl_FragDepth = vIsPerspective == 0.0 ? gl_FragCoord.z : log2( vFragDepth ) * logDepthBufFC * 0.5;
#endif`,eh=`#if defined( USE_LOGDEPTHBUF )
	uniform float logDepthBufFC;
	varying float vFragDepth;
	varying float vIsPerspective;
#endif`,th=`#ifdef USE_LOGDEPTHBUF
	varying float vFragDepth;
	varying float vIsPerspective;
#endif`,nh=`#ifdef USE_LOGDEPTHBUF
	vFragDepth = 1.0 + gl_Position.w;
	vIsPerspective = float( isPerspectiveMatrix( projectionMatrix ) );
#endif`,ih=`#ifdef USE_MAP
	vec4 sampledDiffuseColor = texture2D( map, vMapUv );
	#ifdef DECODE_VIDEO_TEXTURE
		sampledDiffuseColor = sRGBTransferEOTF( sampledDiffuseColor );
	#endif
	diffuseColor *= sampledDiffuseColor;
#endif`,rh=`#ifdef USE_MAP
	uniform sampler2D map;
#endif`,ah=`#if defined( USE_MAP ) || defined( USE_ALPHAMAP )
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
#endif`,sh=`#if defined( USE_POINTS_UV )
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
#endif`,oh=`float metalnessFactor = metalness;
#ifdef USE_METALNESSMAP
	vec4 texelMetalness = texture2D( metalnessMap, vMetalnessMapUv );
	metalnessFactor *= texelMetalness.b;
#endif`,ch=`#ifdef USE_METALNESSMAP
	uniform sampler2D metalnessMap;
#endif`,lh=`#ifdef USE_INSTANCING_MORPH
	float morphTargetInfluences[ MORPHTARGETS_COUNT ];
	float morphTargetBaseInfluence = texelFetch( morphTexture, ivec2( 0, gl_InstanceID ), 0 ).r;
	for ( int i = 0; i < MORPHTARGETS_COUNT; i ++ ) {
		morphTargetInfluences[i] =  texelFetch( morphTexture, ivec2( i + 1, gl_InstanceID ), 0 ).r;
	}
#endif`,uh=`#if defined( USE_MORPHCOLORS )
	vColor *= morphTargetBaseInfluence;
	for ( int i = 0; i < MORPHTARGETS_COUNT; i ++ ) {
		#if defined( USE_COLOR_ALPHA )
			if ( morphTargetInfluences[ i ] != 0.0 ) vColor += getMorph( gl_VertexID, i, 2 ) * morphTargetInfluences[ i ];
		#elif defined( USE_COLOR )
			if ( morphTargetInfluences[ i ] != 0.0 ) vColor += getMorph( gl_VertexID, i, 2 ).rgb * morphTargetInfluences[ i ];
		#endif
	}
#endif`,dh=`#ifdef USE_MORPHNORMALS
	objectNormal *= morphTargetBaseInfluence;
	for ( int i = 0; i < MORPHTARGETS_COUNT; i ++ ) {
		if ( morphTargetInfluences[ i ] != 0.0 ) objectNormal += getMorph( gl_VertexID, i, 1 ).xyz * morphTargetInfluences[ i ];
	}
#endif`,hh=`#ifdef USE_MORPHTARGETS
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
#endif`,fh=`#ifdef USE_MORPHTARGETS
	transformed *= morphTargetBaseInfluence;
	for ( int i = 0; i < MORPHTARGETS_COUNT; i ++ ) {
		if ( morphTargetInfluences[ i ] != 0.0 ) transformed += getMorph( gl_VertexID, i, 0 ).xyz * morphTargetInfluences[ i ];
	}
#endif`,ph=`float faceDirection = gl_FrontFacing ? 1.0 : - 1.0;
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
vec3 nonPerturbedNormal = normal;`,mh=`#ifdef USE_NORMALMAP_OBJECTSPACE
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
#endif`,gh=`#ifndef FLAT_SHADED
	varying vec3 vNormal;
	#ifdef USE_TANGENT
		varying vec3 vTangent;
		varying vec3 vBitangent;
	#endif
#endif`,_h=`#ifndef FLAT_SHADED
	varying vec3 vNormal;
	#ifdef USE_TANGENT
		varying vec3 vTangent;
		varying vec3 vBitangent;
	#endif
#endif`,vh=`#ifndef FLAT_SHADED
	vNormal = normalize( transformedNormal );
	#ifdef USE_TANGENT
		vTangent = normalize( transformedTangent );
		vBitangent = normalize( cross( vNormal, vTangent ) * tangent.w );
	#endif
#endif`,xh=`#ifdef USE_NORMALMAP
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
#endif`,Mh=`#ifdef USE_CLEARCOAT
	vec3 clearcoatNormal = nonPerturbedNormal;
#endif`,Sh=`#ifdef USE_CLEARCOAT_NORMALMAP
	vec3 clearcoatMapN = texture2D( clearcoatNormalMap, vClearcoatNormalMapUv ).xyz * 2.0 - 1.0;
	clearcoatMapN.xy *= clearcoatNormalScale;
	clearcoatNormal = normalize( tbn2 * clearcoatMapN );
#endif`,Eh=`#ifdef USE_CLEARCOATMAP
	uniform sampler2D clearcoatMap;
#endif
#ifdef USE_CLEARCOAT_NORMALMAP
	uniform sampler2D clearcoatNormalMap;
	uniform vec2 clearcoatNormalScale;
#endif
#ifdef USE_CLEARCOAT_ROUGHNESSMAP
	uniform sampler2D clearcoatRoughnessMap;
#endif`,yh=`#ifdef USE_IRIDESCENCEMAP
	uniform sampler2D iridescenceMap;
#endif
#ifdef USE_IRIDESCENCE_THICKNESSMAP
	uniform sampler2D iridescenceThicknessMap;
#endif`,bh=`#ifdef OPAQUE
diffuseColor.a = 1.0;
#endif
#ifdef USE_TRANSMISSION
diffuseColor.a *= material.transmissionAlpha;
#endif
gl_FragColor = vec4( outgoingLight, diffuseColor.a );`,Th=`vec3 packNormalToRGB( const in vec3 normal ) {
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
}`,wh=`#ifdef PREMULTIPLIED_ALPHA
	gl_FragColor.rgb *= gl_FragColor.a;
#endif`,Ah=`vec4 mvPosition = vec4( transformed, 1.0 );
#ifdef USE_BATCHING
	mvPosition = batchingMatrix * mvPosition;
#endif
#ifdef USE_INSTANCING
	mvPosition = instanceMatrix * mvPosition;
#endif
mvPosition = modelViewMatrix * mvPosition;
gl_Position = projectionMatrix * mvPosition;`,Rh=`#ifdef DITHERING
	gl_FragColor.rgb = dithering( gl_FragColor.rgb );
#endif`,Ch=`#ifdef DITHERING
	vec3 dithering( vec3 color ) {
		float grid_position = rand( gl_FragCoord.xy );
		vec3 dither_shift_RGB = vec3( 0.25 / 255.0, -0.25 / 255.0, 0.25 / 255.0 );
		dither_shift_RGB = mix( 2.0 * dither_shift_RGB, -2.0 * dither_shift_RGB, grid_position );
		return color + dither_shift_RGB;
	}
#endif`,Ph=`float roughnessFactor = roughness;
#ifdef USE_ROUGHNESSMAP
	vec4 texelRoughness = texture2D( roughnessMap, vRoughnessMapUv );
	roughnessFactor *= texelRoughness.g;
#endif`,Dh=`#ifdef USE_ROUGHNESSMAP
	uniform sampler2D roughnessMap;
#endif`,Lh=`#if NUM_SPOT_LIGHT_COORDS > 0
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
#endif`,Ih=`#if NUM_SPOT_LIGHT_COORDS > 0
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
#endif`,Uh=`#if ( defined( USE_SHADOWMAP ) && ( NUM_DIR_LIGHT_SHADOWS > 0 || NUM_POINT_LIGHT_SHADOWS > 0 ) ) || ( NUM_SPOT_LIGHT_COORDS > 0 )
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
#endif`,zh=`float getShadowMask() {
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
}`,Nh=`#ifdef USE_SKINNING
	mat4 boneMatX = getBoneMatrix( skinIndex.x );
	mat4 boneMatY = getBoneMatrix( skinIndex.y );
	mat4 boneMatZ = getBoneMatrix( skinIndex.z );
	mat4 boneMatW = getBoneMatrix( skinIndex.w );
#endif`,kh=`#ifdef USE_SKINNING
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
#endif`,Fh=`#ifdef USE_SKINNING
	vec4 skinVertex = bindMatrix * vec4( transformed, 1.0 );
	vec4 skinned = vec4( 0.0 );
	skinned += boneMatX * skinVertex * skinWeight.x;
	skinned += boneMatY * skinVertex * skinWeight.y;
	skinned += boneMatZ * skinVertex * skinWeight.z;
	skinned += boneMatW * skinVertex * skinWeight.w;
	transformed = ( bindMatrixInverse * skinned ).xyz;
#endif`,Oh=`#ifdef USE_SKINNING
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
#endif`,Bh=`float specularStrength;
#ifdef USE_SPECULARMAP
	vec4 texelSpecular = texture2D( specularMap, vSpecularMapUv );
	specularStrength = texelSpecular.r;
#else
	specularStrength = 1.0;
#endif`,Vh=`#ifdef USE_SPECULARMAP
	uniform sampler2D specularMap;
#endif`,Gh=`#if defined( TONE_MAPPING )
	gl_FragColor.rgb = toneMapping( gl_FragColor.rgb );
#endif`,Hh=`#ifndef saturate
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
vec3 CustomToneMapping( vec3 color ) { return color; }`,jh=`#ifdef USE_TRANSMISSION
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
#endif`,Wh=`#ifdef USE_TRANSMISSION
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
#endif`,Xh=`#if defined( USE_UV ) || defined( USE_ANISOTROPY )
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
#endif`,qh=`#if defined( USE_UV ) || defined( USE_ANISOTROPY )
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
#endif`,Kh=`#if defined( USE_UV ) || defined( USE_ANISOTROPY )
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
#endif`,$h=`#if defined( USE_ENVMAP ) || defined( DISTANCE ) || defined ( USE_SHADOWMAP ) || defined ( USE_TRANSMISSION ) || NUM_SPOT_LIGHT_COORDS > 0
	vec4 worldPosition = vec4( transformed, 1.0 );
	#ifdef USE_BATCHING
		worldPosition = batchingMatrix * worldPosition;
	#endif
	#ifdef USE_INSTANCING
		worldPosition = instanceMatrix * worldPosition;
	#endif
	worldPosition = modelMatrix * worldPosition;
#endif`;const Yh=`varying vec2 vUv;
uniform mat3 uvTransform;
void main() {
	vUv = ( uvTransform * vec3( uv, 1 ) ).xy;
	gl_Position = vec4( position.xy, 1.0, 1.0 );
}`,Zh=`uniform sampler2D t2D;
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
}`,Jh=`varying vec3 vWorldDirection;
#include <common>
void main() {
	vWorldDirection = transformDirection( position, modelMatrix );
	#include <begin_vertex>
	#include <project_vertex>
	gl_Position.z = gl_Position.w;
}`,Qh=`#ifdef ENVMAP_TYPE_CUBE
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
}`,ef=`varying vec3 vWorldDirection;
#include <common>
void main() {
	vWorldDirection = transformDirection( position, modelMatrix );
	#include <begin_vertex>
	#include <project_vertex>
	gl_Position.z = gl_Position.w;
}`,tf=`uniform samplerCube tCube;
uniform float tFlip;
uniform float opacity;
varying vec3 vWorldDirection;
void main() {
	vec4 texColor = textureCube( tCube, vec3( tFlip * vWorldDirection.x, vWorldDirection.yz ) );
	gl_FragColor = texColor;
	gl_FragColor.a *= opacity;
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
}`,nf=`#include <common>
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
}`,rf=`#if DEPTH_PACKING == 3200
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
}`,af=`#define DISTANCE
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
}`,sf=`#define DISTANCE
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
}`,of=`varying vec3 vWorldDirection;
#include <common>
void main() {
	vWorldDirection = transformDirection( position, modelMatrix );
	#include <begin_vertex>
	#include <project_vertex>
}`,cf=`uniform sampler2D tEquirect;
varying vec3 vWorldDirection;
#include <common>
void main() {
	vec3 direction = normalize( vWorldDirection );
	vec2 sampleUV = equirectUv( direction );
	gl_FragColor = texture2D( tEquirect, sampleUV );
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
}`,lf=`uniform float scale;
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
}`,uf=`uniform vec3 diffuse;
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
}`,df=`#include <common>
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
}`,hf=`uniform vec3 diffuse;
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
}`,ff=`#define LAMBERT
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
}`,pf=`#define LAMBERT
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
}`,mf=`#define MATCAP
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
}`,gf=`#define MATCAP
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
}`,_f=`#define NORMAL
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
}`,vf=`#define NORMAL
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
}`,xf=`#define PHONG
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
}`,Mf=`#define PHONG
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
}`,Sf=`#define STANDARD
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
}`,Ef=`#define STANDARD
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
}`,yf=`#define TOON
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
}`,bf=`#define TOON
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
}`,Tf=`uniform float size;
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
}`,wf=`uniform vec3 diffuse;
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
}`,Af=`#include <common>
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
}`,Rf=`uniform vec3 color;
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
}`,Cf=`uniform float rotation;
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
}`,Pf=`uniform vec3 diffuse;
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
}`,He={alphahash_fragment:Zu,alphahash_pars_fragment:Ju,alphamap_fragment:Qu,alphamap_pars_fragment:ed,alphatest_fragment:td,alphatest_pars_fragment:nd,aomap_fragment:id,aomap_pars_fragment:rd,batching_pars_vertex:ad,batching_vertex:sd,begin_vertex:od,beginnormal_vertex:cd,bsdfs:ld,iridescence_fragment:ud,bumpmap_pars_fragment:dd,clipping_planes_fragment:hd,clipping_planes_pars_fragment:fd,clipping_planes_pars_vertex:pd,clipping_planes_vertex:md,color_fragment:gd,color_pars_fragment:_d,color_pars_vertex:vd,color_vertex:xd,common:Md,cube_uv_reflection_fragment:Sd,defaultnormal_vertex:Ed,displacementmap_pars_vertex:yd,displacementmap_vertex:bd,emissivemap_fragment:Td,emissivemap_pars_fragment:wd,colorspace_fragment:Ad,colorspace_pars_fragment:Rd,envmap_fragment:Cd,envmap_common_pars_fragment:Pd,envmap_pars_fragment:Dd,envmap_pars_vertex:Ld,envmap_physical_pars_fragment:Hd,envmap_vertex:Id,fog_vertex:Ud,fog_pars_vertex:zd,fog_fragment:Nd,fog_pars_fragment:kd,gradientmap_pars_fragment:Fd,lightmap_pars_fragment:Od,lights_lambert_fragment:Bd,lights_lambert_pars_fragment:Vd,lights_pars_begin:Gd,lights_toon_fragment:jd,lights_toon_pars_fragment:Wd,lights_phong_fragment:Xd,lights_phong_pars_fragment:qd,lights_physical_fragment:Kd,lights_physical_pars_fragment:$d,lights_fragment_begin:Yd,lights_fragment_maps:Zd,lights_fragment_end:Jd,logdepthbuf_fragment:Qd,logdepthbuf_pars_fragment:eh,logdepthbuf_pars_vertex:th,logdepthbuf_vertex:nh,map_fragment:ih,map_pars_fragment:rh,map_particle_fragment:ah,map_particle_pars_fragment:sh,metalnessmap_fragment:oh,metalnessmap_pars_fragment:ch,morphinstance_vertex:lh,morphcolor_vertex:uh,morphnormal_vertex:dh,morphtarget_pars_vertex:hh,morphtarget_vertex:fh,normal_fragment_begin:ph,normal_fragment_maps:mh,normal_pars_fragment:gh,normal_pars_vertex:_h,normal_vertex:vh,normalmap_pars_fragment:xh,clearcoat_normal_fragment_begin:Mh,clearcoat_normal_fragment_maps:Sh,clearcoat_pars_fragment:Eh,iridescence_pars_fragment:yh,opaque_fragment:bh,packing:Th,premultiplied_alpha_fragment:wh,project_vertex:Ah,dithering_fragment:Rh,dithering_pars_fragment:Ch,roughnessmap_fragment:Ph,roughnessmap_pars_fragment:Dh,shadowmap_pars_fragment:Lh,shadowmap_pars_vertex:Ih,shadowmap_vertex:Uh,shadowmask_pars_fragment:zh,skinbase_vertex:Nh,skinning_pars_vertex:kh,skinning_vertex:Fh,skinnormal_vertex:Oh,specularmap_fragment:Bh,specularmap_pars_fragment:Vh,tonemapping_fragment:Gh,tonemapping_pars_fragment:Hh,transmission_fragment:jh,transmission_pars_fragment:Wh,uv_pars_fragment:Xh,uv_pars_vertex:qh,uv_vertex:Kh,worldpos_vertex:$h,background_vert:Yh,background_frag:Zh,backgroundCube_vert:Jh,backgroundCube_frag:Qh,cube_vert:ef,cube_frag:tf,depth_vert:nf,depth_frag:rf,distanceRGBA_vert:af,distanceRGBA_frag:sf,equirect_vert:of,equirect_frag:cf,linedashed_vert:lf,linedashed_frag:uf,meshbasic_vert:df,meshbasic_frag:hf,meshlambert_vert:ff,meshlambert_frag:pf,meshmatcap_vert:mf,meshmatcap_frag:gf,meshnormal_vert:_f,meshnormal_frag:vf,meshphong_vert:xf,meshphong_frag:Mf,meshphysical_vert:Sf,meshphysical_frag:Ef,meshtoon_vert:yf,meshtoon_frag:bf,points_vert:Tf,points_frag:wf,shadow_vert:Af,shadow_frag:Rf,sprite_vert:Cf,sprite_frag:Pf},he={common:{diffuse:{value:new oe(16777215)},opacity:{value:1},map:{value:null},mapTransform:{value:new Ve},alphaMap:{value:null},alphaMapTransform:{value:new Ve},alphaTest:{value:0}},specularmap:{specularMap:{value:null},specularMapTransform:{value:new Ve}},envmap:{envMap:{value:null},envMapRotation:{value:new Ve},flipEnvMap:{value:-1},reflectivity:{value:1},ior:{value:1.5},refractionRatio:{value:.98}},aomap:{aoMap:{value:null},aoMapIntensity:{value:1},aoMapTransform:{value:new Ve}},lightmap:{lightMap:{value:null},lightMapIntensity:{value:1},lightMapTransform:{value:new Ve}},bumpmap:{bumpMap:{value:null},bumpMapTransform:{value:new Ve},bumpScale:{value:1}},normalmap:{normalMap:{value:null},normalMapTransform:{value:new Ve},normalScale:{value:new We(1,1)}},displacementmap:{displacementMap:{value:null},displacementMapTransform:{value:new Ve},displacementScale:{value:1},displacementBias:{value:0}},emissivemap:{emissiveMap:{value:null},emissiveMapTransform:{value:new Ve}},metalnessmap:{metalnessMap:{value:null},metalnessMapTransform:{value:new Ve}},roughnessmap:{roughnessMap:{value:null},roughnessMapTransform:{value:new Ve}},gradientmap:{gradientMap:{value:null}},fog:{fogDensity:{value:25e-5},fogNear:{value:1},fogFar:{value:2e3},fogColor:{value:new oe(16777215)}},lights:{ambientLightColor:{value:[]},lightProbe:{value:[]},directionalLights:{value:[],properties:{direction:{},color:{}}},directionalLightShadows:{value:[],properties:{shadowIntensity:1,shadowBias:{},shadowNormalBias:{},shadowRadius:{},shadowMapSize:{}}},directionalShadowMap:{value:[]},directionalShadowMatrix:{value:[]},spotLights:{value:[],properties:{color:{},position:{},direction:{},distance:{},coneCos:{},penumbraCos:{},decay:{}}},spotLightShadows:{value:[],properties:{shadowIntensity:1,shadowBias:{},shadowNormalBias:{},shadowRadius:{},shadowMapSize:{}}},spotLightMap:{value:[]},spotShadowMap:{value:[]},spotLightMatrix:{value:[]},pointLights:{value:[],properties:{color:{},position:{},decay:{},distance:{}}},pointLightShadows:{value:[],properties:{shadowIntensity:1,shadowBias:{},shadowNormalBias:{},shadowRadius:{},shadowMapSize:{},shadowCameraNear:{},shadowCameraFar:{}}},pointShadowMap:{value:[]},pointShadowMatrix:{value:[]},hemisphereLights:{value:[],properties:{direction:{},skyColor:{},groundColor:{}}},rectAreaLights:{value:[],properties:{color:{},position:{},width:{},height:{}}},ltc_1:{value:null},ltc_2:{value:null}},points:{diffuse:{value:new oe(16777215)},opacity:{value:1},size:{value:1},scale:{value:1},map:{value:null},alphaMap:{value:null},alphaMapTransform:{value:new Ve},alphaTest:{value:0},uvTransform:{value:new Ve}},sprite:{diffuse:{value:new oe(16777215)},opacity:{value:1},center:{value:new We(.5,.5)},rotation:{value:0},map:{value:null},mapTransform:{value:new Ve},alphaMap:{value:null},alphaMapTransform:{value:new Ve},alphaTest:{value:0}}},Zt={basic:{uniforms:Rt([he.common,he.specularmap,he.envmap,he.aomap,he.lightmap,he.fog]),vertexShader:He.meshbasic_vert,fragmentShader:He.meshbasic_frag},lambert:{uniforms:Rt([he.common,he.specularmap,he.envmap,he.aomap,he.lightmap,he.emissivemap,he.bumpmap,he.normalmap,he.displacementmap,he.fog,he.lights,{emissive:{value:new oe(0)}}]),vertexShader:He.meshlambert_vert,fragmentShader:He.meshlambert_frag},phong:{uniforms:Rt([he.common,he.specularmap,he.envmap,he.aomap,he.lightmap,he.emissivemap,he.bumpmap,he.normalmap,he.displacementmap,he.fog,he.lights,{emissive:{value:new oe(0)},specular:{value:new oe(1118481)},shininess:{value:30}}]),vertexShader:He.meshphong_vert,fragmentShader:He.meshphong_frag},standard:{uniforms:Rt([he.common,he.envmap,he.aomap,he.lightmap,he.emissivemap,he.bumpmap,he.normalmap,he.displacementmap,he.roughnessmap,he.metalnessmap,he.fog,he.lights,{emissive:{value:new oe(0)},roughness:{value:1},metalness:{value:0},envMapIntensity:{value:1}}]),vertexShader:He.meshphysical_vert,fragmentShader:He.meshphysical_frag},toon:{uniforms:Rt([he.common,he.aomap,he.lightmap,he.emissivemap,he.bumpmap,he.normalmap,he.displacementmap,he.gradientmap,he.fog,he.lights,{emissive:{value:new oe(0)}}]),vertexShader:He.meshtoon_vert,fragmentShader:He.meshtoon_frag},matcap:{uniforms:Rt([he.common,he.bumpmap,he.normalmap,he.displacementmap,he.fog,{matcap:{value:null}}]),vertexShader:He.meshmatcap_vert,fragmentShader:He.meshmatcap_frag},points:{uniforms:Rt([he.points,he.fog]),vertexShader:He.points_vert,fragmentShader:He.points_frag},dashed:{uniforms:Rt([he.common,he.fog,{scale:{value:1},dashSize:{value:1},totalSize:{value:2}}]),vertexShader:He.linedashed_vert,fragmentShader:He.linedashed_frag},depth:{uniforms:Rt([he.common,he.displacementmap]),vertexShader:He.depth_vert,fragmentShader:He.depth_frag},normal:{uniforms:Rt([he.common,he.bumpmap,he.normalmap,he.displacementmap,{opacity:{value:1}}]),vertexShader:He.meshnormal_vert,fragmentShader:He.meshnormal_frag},sprite:{uniforms:Rt([he.sprite,he.fog]),vertexShader:He.sprite_vert,fragmentShader:He.sprite_frag},background:{uniforms:{uvTransform:{value:new Ve},t2D:{value:null},backgroundIntensity:{value:1}},vertexShader:He.background_vert,fragmentShader:He.background_frag},backgroundCube:{uniforms:{envMap:{value:null},flipEnvMap:{value:-1},backgroundBlurriness:{value:0},backgroundIntensity:{value:1},backgroundRotation:{value:new Ve}},vertexShader:He.backgroundCube_vert,fragmentShader:He.backgroundCube_frag},cube:{uniforms:{tCube:{value:null},tFlip:{value:-1},opacity:{value:1}},vertexShader:He.cube_vert,fragmentShader:He.cube_frag},equirect:{uniforms:{tEquirect:{value:null}},vertexShader:He.equirect_vert,fragmentShader:He.equirect_frag},distanceRGBA:{uniforms:Rt([he.common,he.displacementmap,{referencePosition:{value:new F},nearDistance:{value:1},farDistance:{value:1e3}}]),vertexShader:He.distanceRGBA_vert,fragmentShader:He.distanceRGBA_frag},shadow:{uniforms:Rt([he.lights,he.fog,{color:{value:new oe(0)},opacity:{value:1}}]),vertexShader:He.shadow_vert,fragmentShader:He.shadow_frag}};Zt.physical={uniforms:Rt([Zt.standard.uniforms,{clearcoat:{value:0},clearcoatMap:{value:null},clearcoatMapTransform:{value:new Ve},clearcoatNormalMap:{value:null},clearcoatNormalMapTransform:{value:new Ve},clearcoatNormalScale:{value:new We(1,1)},clearcoatRoughness:{value:0},clearcoatRoughnessMap:{value:null},clearcoatRoughnessMapTransform:{value:new Ve},dispersion:{value:0},iridescence:{value:0},iridescenceMap:{value:null},iridescenceMapTransform:{value:new Ve},iridescenceIOR:{value:1.3},iridescenceThicknessMinimum:{value:100},iridescenceThicknessMaximum:{value:400},iridescenceThicknessMap:{value:null},iridescenceThicknessMapTransform:{value:new Ve},sheen:{value:0},sheenColor:{value:new oe(0)},sheenColorMap:{value:null},sheenColorMapTransform:{value:new Ve},sheenRoughness:{value:1},sheenRoughnessMap:{value:null},sheenRoughnessMapTransform:{value:new Ve},transmission:{value:0},transmissionMap:{value:null},transmissionMapTransform:{value:new Ve},transmissionSamplerSize:{value:new We},transmissionSamplerMap:{value:null},thickness:{value:0},thicknessMap:{value:null},thicknessMapTransform:{value:new Ve},attenuationDistance:{value:0},attenuationColor:{value:new oe(0)},specularColor:{value:new oe(1,1,1)},specularColorMap:{value:null},specularColorMapTransform:{value:new Ve},specularIntensity:{value:1},specularIntensityMap:{value:null},specularIntensityMapTransform:{value:new Ve},anisotropyVector:{value:new We},anisotropyMap:{value:null},anisotropyMapTransform:{value:new Ve}}]),vertexShader:He.meshphysical_vert,fragmentShader:He.meshphysical_frag};const Dr={r:0,b:0,g:0},On=new xt,Df=new at;function Lf(n,e,t,i,r,a,s){const o=new oe(0);let c=a===!0?0:1,l,d,h=null,f=0,m=null;function g(y){let M=y.isScene===!0?y.background:null;return M&&M.isTexture&&(M=(y.backgroundBlurriness>0?t:e).get(M)),M}function _(y){let M=!1;const D=g(y);D===null?u(o,c):D&&D.isColor&&(u(D,1),M=!0);const A=n.xr.getEnvironmentBlendMode();A==="additive"?i.buffers.color.setClear(0,0,0,1,s):A==="alpha-blend"&&i.buffers.color.setClear(0,0,0,0,s),(n.autoClear||M)&&(i.buffers.depth.setTest(!0),i.buffers.depth.setMask(!0),i.buffers.color.setMask(!0),n.clear(n.autoClearColor,n.autoClearDepth,n.autoClearStencil))}function p(y,M){const D=g(M);D&&(D.isCubeTexture||D.mapping===Kr)?(d===void 0&&(d=new Le(new Qt(1,1,1),new Dn({name:"BackgroundCubeMaterial",uniforms:zi(Zt.backgroundCube.uniforms),vertexShader:Zt.backgroundCube.vertexShader,fragmentShader:Zt.backgroundCube.fragmentShader,side:Ct,depthTest:!1,depthWrite:!1,fog:!1})),d.geometry.deleteAttribute("normal"),d.geometry.deleteAttribute("uv"),d.onBeforeRender=function(A,b,C){this.matrixWorld.copyPosition(C.matrixWorld)},Object.defineProperty(d.material,"envMap",{get:function(){return this.uniforms.envMap.value}}),r.update(d)),On.copy(M.backgroundRotation),On.x*=-1,On.y*=-1,On.z*=-1,D.isCubeTexture&&D.isRenderTargetTexture===!1&&(On.y*=-1,On.z*=-1),d.material.uniforms.envMap.value=D,d.material.uniforms.flipEnvMap.value=D.isCubeTexture&&D.isRenderTargetTexture===!1?-1:1,d.material.uniforms.backgroundBlurriness.value=M.backgroundBlurriness,d.material.uniforms.backgroundIntensity.value=M.backgroundIntensity,d.material.uniforms.backgroundRotation.value.setFromMatrix4(Df.makeRotationFromEuler(On)),d.material.toneMapped=Je.getTransfer(D.colorSpace)!==it,(h!==D||f!==D.version||m!==n.toneMapping)&&(d.material.needsUpdate=!0,h=D,f=D.version,m=n.toneMapping),d.layers.enableAll(),y.unshift(d,d.geometry,d.material,0,0,null)):D&&D.isTexture&&(l===void 0&&(l=new Le(new ii(2,2),new Dn({name:"BackgroundMaterial",uniforms:zi(Zt.background.uniforms),vertexShader:Zt.background.vertexShader,fragmentShader:Zt.background.fragmentShader,side:Pn,depthTest:!1,depthWrite:!1,fog:!1})),l.geometry.deleteAttribute("normal"),Object.defineProperty(l.material,"map",{get:function(){return this.uniforms.t2D.value}}),r.update(l)),l.material.uniforms.t2D.value=D,l.material.uniforms.backgroundIntensity.value=M.backgroundIntensity,l.material.toneMapped=Je.getTransfer(D.colorSpace)!==it,D.matrixAutoUpdate===!0&&D.updateMatrix(),l.material.uniforms.uvTransform.value.copy(D.matrix),(h!==D||f!==D.version||m!==n.toneMapping)&&(l.material.needsUpdate=!0,h=D,f=D.version,m=n.toneMapping),l.layers.enableAll(),y.unshift(l,l.geometry,l.material,0,0,null))}function u(y,M){y.getRGB(Dr,Zc(n)),i.buffers.color.setClear(Dr.r,Dr.g,Dr.b,M,s)}function E(){d!==void 0&&(d.geometry.dispose(),d.material.dispose(),d=void 0),l!==void 0&&(l.geometry.dispose(),l.material.dispose(),l=void 0)}return{getClearColor:function(){return o},setClearColor:function(y,M=1){o.set(y),c=M,u(o,c)},getClearAlpha:function(){return c},setClearAlpha:function(y){c=y,u(o,c)},render:_,addToRenderList:p,dispose:E}}function If(n,e){const t=n.getParameter(n.MAX_VERTEX_ATTRIBS),i={},r=f(null);let a=r,s=!1;function o(x,P,U,w,R){let z=!1;const N=h(w,U,P);a!==N&&(a=N,l(a.object)),z=m(x,w,U,R),z&&g(x,w,U,R),R!==null&&e.update(R,n.ELEMENT_ARRAY_BUFFER),(z||s)&&(s=!1,M(x,P,U,w),R!==null&&n.bindBuffer(n.ELEMENT_ARRAY_BUFFER,e.get(R).buffer))}function c(){return n.createVertexArray()}function l(x){return n.bindVertexArray(x)}function d(x){return n.deleteVertexArray(x)}function h(x,P,U){const w=U.wireframe===!0;let R=i[x.id];R===void 0&&(R={},i[x.id]=R);let z=R[P.id];z===void 0&&(z={},R[P.id]=z);let N=z[w];return N===void 0&&(N=f(c()),z[w]=N),N}function f(x){const P=[],U=[],w=[];for(let R=0;R<t;R++)P[R]=0,U[R]=0,w[R]=0;return{geometry:null,program:null,wireframe:!1,newAttributes:P,enabledAttributes:U,attributeDivisors:w,object:x,attributes:{},index:null}}function m(x,P,U,w){const R=a.attributes,z=P.attributes;let N=0;const B=U.getAttributes();for(const k in B)if(B[k].location>=0){const q=R[k];let K=z[k];if(K===void 0&&(k==="instanceMatrix"&&x.instanceMatrix&&(K=x.instanceMatrix),k==="instanceColor"&&x.instanceColor&&(K=x.instanceColor)),q===void 0||q.attribute!==K||K&&q.data!==K.data)return!0;N++}return a.attributesNum!==N||a.index!==w}function g(x,P,U,w){const R={},z=P.attributes;let N=0;const B=U.getAttributes();for(const k in B)if(B[k].location>=0){let q=z[k];q===void 0&&(k==="instanceMatrix"&&x.instanceMatrix&&(q=x.instanceMatrix),k==="instanceColor"&&x.instanceColor&&(q=x.instanceColor));const K={};K.attribute=q,q&&q.data&&(K.data=q.data),R[k]=K,N++}a.attributes=R,a.attributesNum=N,a.index=w}function _(){const x=a.newAttributes;for(let P=0,U=x.length;P<U;P++)x[P]=0}function p(x){u(x,0)}function u(x,P){const U=a.newAttributes,w=a.enabledAttributes,R=a.attributeDivisors;U[x]=1,w[x]===0&&(n.enableVertexAttribArray(x),w[x]=1),R[x]!==P&&(n.vertexAttribDivisor(x,P),R[x]=P)}function E(){const x=a.newAttributes,P=a.enabledAttributes;for(let U=0,w=P.length;U<w;U++)P[U]!==x[U]&&(n.disableVertexAttribArray(U),P[U]=0)}function y(x,P,U,w,R,z,N){N===!0?n.vertexAttribIPointer(x,P,U,R,z):n.vertexAttribPointer(x,P,U,w,R,z)}function M(x,P,U,w){_();const R=w.attributes,z=U.getAttributes(),N=P.defaultAttributeValues;for(const B in z){const k=z[B];if(k.location>=0){let O=R[B];if(O===void 0&&(B==="instanceMatrix"&&x.instanceMatrix&&(O=x.instanceMatrix),B==="instanceColor"&&x.instanceColor&&(O=x.instanceColor)),O!==void 0){const q=O.normalized,K=O.itemSize,le=e.get(O);if(le===void 0)continue;const De=le.buffer,X=le.type,J=le.bytesPerElement,ae=X===n.INT||X===n.UNSIGNED_INT||O.gpuType===zs;if(O.isInterleavedBufferAttribute){const re=O.data,ue=re.stride,Pe=O.offset;if(re.isInstancedInterleavedBuffer){for(let fe=0;fe<k.locationSize;fe++)u(k.location+fe,re.meshPerAttribute);x.isInstancedMesh!==!0&&w._maxInstanceCount===void 0&&(w._maxInstanceCount=re.meshPerAttribute*re.count)}else for(let fe=0;fe<k.locationSize;fe++)p(k.location+fe);n.bindBuffer(n.ARRAY_BUFFER,De);for(let fe=0;fe<k.locationSize;fe++)y(k.location+fe,K/k.locationSize,X,q,ue*J,(Pe+K/k.locationSize*fe)*J,ae)}else{if(O.isInstancedBufferAttribute){for(let re=0;re<k.locationSize;re++)u(k.location+re,O.meshPerAttribute);x.isInstancedMesh!==!0&&w._maxInstanceCount===void 0&&(w._maxInstanceCount=O.meshPerAttribute*O.count)}else for(let re=0;re<k.locationSize;re++)p(k.location+re);n.bindBuffer(n.ARRAY_BUFFER,De);for(let re=0;re<k.locationSize;re++)y(k.location+re,K/k.locationSize,X,q,K*J,K/k.locationSize*re*J,ae)}}else if(N!==void 0){const q=N[B];if(q!==void 0)switch(q.length){case 2:n.vertexAttrib2fv(k.location,q);break;case 3:n.vertexAttrib3fv(k.location,q);break;case 4:n.vertexAttrib4fv(k.location,q);break;default:n.vertexAttrib1fv(k.location,q)}}}}E()}function D(){C();for(const x in i){const P=i[x];for(const U in P){const w=P[U];for(const R in w)d(w[R].object),delete w[R];delete P[U]}delete i[x]}}function A(x){if(i[x.id]===void 0)return;const P=i[x.id];for(const U in P){const w=P[U];for(const R in w)d(w[R].object),delete w[R];delete P[U]}delete i[x.id]}function b(x){for(const P in i){const U=i[P];if(U[x.id]===void 0)continue;const w=U[x.id];for(const R in w)d(w[R].object),delete w[R];delete U[x.id]}}function C(){v(),s=!0,a!==r&&(a=r,l(a.object))}function v(){r.geometry=null,r.program=null,r.wireframe=!1}return{setup:o,reset:C,resetDefaultState:v,dispose:D,releaseStatesOfGeometry:A,releaseStatesOfProgram:b,initAttributes:_,enableAttribute:p,disableUnusedAttributes:E}}function Uf(n,e,t){let i;function r(l){i=l}function a(l,d){n.drawArrays(i,l,d),t.update(d,i,1)}function s(l,d,h){h!==0&&(n.drawArraysInstanced(i,l,d,h),t.update(d,i,h))}function o(l,d,h){if(h===0)return;e.get("WEBGL_multi_draw").multiDrawArraysWEBGL(i,l,0,d,0,h);let m=0;for(let g=0;g<h;g++)m+=d[g];t.update(m,i,1)}function c(l,d,h,f){if(h===0)return;const m=e.get("WEBGL_multi_draw");if(m===null)for(let g=0;g<l.length;g++)s(l[g],d[g],f[g]);else{m.multiDrawArraysInstancedWEBGL(i,l,0,d,0,f,0,h);let g=0;for(let _=0;_<h;_++)g+=d[_]*f[_];t.update(g,i,1)}}this.setMode=r,this.render=a,this.renderInstances=s,this.renderMultiDraw=o,this.renderMultiDrawInstances=c}function zf(n,e,t,i){let r;function a(){if(r!==void 0)return r;if(e.has("EXT_texture_filter_anisotropic")===!0){const b=e.get("EXT_texture_filter_anisotropic");r=n.getParameter(b.MAX_TEXTURE_MAX_ANISOTROPY_EXT)}else r=0;return r}function s(b){return!(b!==Ht&&i.convert(b)!==n.getParameter(n.IMPLEMENTATION_COLOR_READ_FORMAT))}function o(b){const C=b===ir&&(e.has("EXT_color_buffer_half_float")||e.has("EXT_color_buffer_float"));return!(b!==mn&&i.convert(b)!==n.getParameter(n.IMPLEMENTATION_COLOR_READ_TYPE)&&b!==hn&&!C)}function c(b){if(b==="highp"){if(n.getShaderPrecisionFormat(n.VERTEX_SHADER,n.HIGH_FLOAT).precision>0&&n.getShaderPrecisionFormat(n.FRAGMENT_SHADER,n.HIGH_FLOAT).precision>0)return"highp";b="mediump"}return b==="mediump"&&n.getShaderPrecisionFormat(n.VERTEX_SHADER,n.MEDIUM_FLOAT).precision>0&&n.getShaderPrecisionFormat(n.FRAGMENT_SHADER,n.MEDIUM_FLOAT).precision>0?"mediump":"lowp"}let l=t.precision!==void 0?t.precision:"highp";const d=c(l);d!==l&&(console.warn("THREE.WebGLRenderer:",l,"not supported, using",d,"instead."),l=d);const h=t.logarithmicDepthBuffer===!0,f=t.reverseDepthBuffer===!0&&e.has("EXT_clip_control"),m=n.getParameter(n.MAX_TEXTURE_IMAGE_UNITS),g=n.getParameter(n.MAX_VERTEX_TEXTURE_IMAGE_UNITS),_=n.getParameter(n.MAX_TEXTURE_SIZE),p=n.getParameter(n.MAX_CUBE_MAP_TEXTURE_SIZE),u=n.getParameter(n.MAX_VERTEX_ATTRIBS),E=n.getParameter(n.MAX_VERTEX_UNIFORM_VECTORS),y=n.getParameter(n.MAX_VARYING_VECTORS),M=n.getParameter(n.MAX_FRAGMENT_UNIFORM_VECTORS),D=g>0,A=n.getParameter(n.MAX_SAMPLES);return{isWebGL2:!0,getMaxAnisotropy:a,getMaxPrecision:c,textureFormatReadable:s,textureTypeReadable:o,precision:l,logarithmicDepthBuffer:h,reverseDepthBuffer:f,maxTextures:m,maxVertexTextures:g,maxTextureSize:_,maxCubemapSize:p,maxAttributes:u,maxVertexUniforms:E,maxVaryings:y,maxFragmentUniforms:M,vertexTextures:D,maxSamples:A}}function Nf(n){const e=this;let t=null,i=0,r=!1,a=!1;const s=new Gn,o=new Ve,c={value:null,needsUpdate:!1};this.uniform=c,this.numPlanes=0,this.numIntersection=0,this.init=function(h,f){const m=h.length!==0||f||i!==0||r;return r=f,i=h.length,m},this.beginShadows=function(){a=!0,d(null)},this.endShadows=function(){a=!1},this.setGlobalState=function(h,f){t=d(h,f,0)},this.setState=function(h,f,m){const g=h.clippingPlanes,_=h.clipIntersection,p=h.clipShadows,u=n.get(h);if(!r||g===null||g.length===0||a&&!p)a?d(null):l();else{const E=a?0:i,y=E*4;let M=u.clippingState||null;c.value=M,M=d(g,f,y,m);for(let D=0;D!==y;++D)M[D]=t[D];u.clippingState=M,this.numIntersection=_?this.numPlanes:0,this.numPlanes+=E}};function l(){c.value!==t&&(c.value=t,c.needsUpdate=i>0),e.numPlanes=i,e.numIntersection=0}function d(h,f,m,g){const _=h!==null?h.length:0;let p=null;if(_!==0){if(p=c.value,g!==!0||p===null){const u=m+_*4,E=f.matrixWorldInverse;o.getNormalMatrix(E),(p===null||p.length<u)&&(p=new Float32Array(u));for(let y=0,M=m;y!==_;++y,M+=4)s.copy(h[y]).applyMatrix4(E,o),s.normal.toArray(p,M),p[M+3]=s.constant}c.value=p,c.needsUpdate=!0}return e.numPlanes=_,e.numIntersection=0,p}}function kf(n){let e=new WeakMap;function t(s,o){return o===Ka?s.mapping=Pi:o===$a&&(s.mapping=Di),s}function i(s){if(s&&s.isTexture){const o=s.mapping;if(o===Ka||o===$a)if(e.has(s)){const c=e.get(s).texture;return t(c,s.mapping)}else{const c=s.image;if(c&&c.height>0){const l=new Uu(c.height);return l.fromEquirectangularTexture(n,s),e.set(s,l),s.addEventListener("dispose",r),t(l.texture,s.mapping)}else return null}}return s}function r(s){const o=s.target;o.removeEventListener("dispose",r);const c=e.get(o);c!==void 0&&(e.delete(o),c.dispose())}function a(){e=new WeakMap}return{get:i,dispose:a}}const yi=4,Xo=[.125,.215,.35,.446,.526,.582],qn=20,Aa=new il,qo=new oe;let Ra=null,Ca=0,Pa=0,Da=!1;const Hn=(1+Math.sqrt(5))/2,xi=1/Hn,Ko=[new F(-Hn,xi,0),new F(Hn,xi,0),new F(-xi,0,Hn),new F(xi,0,Hn),new F(0,Hn,-xi),new F(0,Hn,xi),new F(-1,1,-1),new F(1,1,-1),new F(-1,1,1),new F(1,1,1)],Ff=new F;class ws{constructor(e){this._renderer=e,this._pingPongRenderTarget=null,this._lodMax=0,this._cubeSize=0,this._lodPlanes=[],this._sizeLods=[],this._sigmas=[],this._blurMaterial=null,this._cubemapMaterial=null,this._equirectMaterial=null,this._compileMaterial(this._blurMaterial)}fromScene(e,t=0,i=.1,r=100,a={}){const{size:s=256,position:o=Ff}=a;Ra=this._renderer.getRenderTarget(),Ca=this._renderer.getActiveCubeFace(),Pa=this._renderer.getActiveMipmapLevel(),Da=this._renderer.xr.enabled,this._renderer.xr.enabled=!1,this._setSize(s);const c=this._allocateTargets();return c.depthBuffer=!0,this._sceneToCubeUV(e,i,r,c,o),t>0&&this._blur(c,0,0,t),this._applyPMREM(c),this._cleanup(c),c}fromEquirectangular(e,t=null){return this._fromTexture(e,t)}fromCubemap(e,t=null){return this._fromTexture(e,t)}compileCubemapShader(){this._cubemapMaterial===null&&(this._cubemapMaterial=Zo(),this._compileMaterial(this._cubemapMaterial))}compileEquirectangularShader(){this._equirectMaterial===null&&(this._equirectMaterial=Yo(),this._compileMaterial(this._equirectMaterial))}dispose(){this._dispose(),this._cubemapMaterial!==null&&this._cubemapMaterial.dispose(),this._equirectMaterial!==null&&this._equirectMaterial.dispose()}_setSize(e){this._lodMax=Math.floor(Math.log2(e)),this._cubeSize=Math.pow(2,this._lodMax)}_dispose(){this._blurMaterial!==null&&this._blurMaterial.dispose(),this._pingPongRenderTarget!==null&&this._pingPongRenderTarget.dispose();for(let e=0;e<this._lodPlanes.length;e++)this._lodPlanes[e].dispose()}_cleanup(e){this._renderer.setRenderTarget(Ra,Ca,Pa),this._renderer.xr.enabled=Da,e.scissorTest=!1,Lr(e,0,0,e.width,e.height)}_fromTexture(e,t){e.mapping===Pi||e.mapping===Di?this._setSize(e.image.length===0?16:e.image[0].width||e.image[0].image.width):this._setSize(e.image.width/4),Ra=this._renderer.getRenderTarget(),Ca=this._renderer.getActiveCubeFace(),Pa=this._renderer.getActiveMipmapLevel(),Da=this._renderer.xr.enabled,this._renderer.xr.enabled=!1;const i=t||this._allocateTargets();return this._textureToCubeUV(e,i),this._applyPMREM(i),this._cleanup(i),i}_allocateTargets(){const e=3*Math.max(this._cubeSize,112),t=4*this._cubeSize,i={magFilter:Jt,minFilter:Jt,generateMipmaps:!1,type:ir,format:Ht,colorSpace:Ui,depthBuffer:!1},r=$o(e,t,i);if(this._pingPongRenderTarget===null||this._pingPongRenderTarget.width!==e||this._pingPongRenderTarget.height!==t){this._pingPongRenderTarget!==null&&this._dispose(),this._pingPongRenderTarget=$o(e,t,i);const{_lodMax:a}=this;({sizeLods:this._sizeLods,lodPlanes:this._lodPlanes,sigmas:this._sigmas}=Of(a)),this._blurMaterial=Bf(a,e,t)}return r}_compileMaterial(e){const t=new Le(this._lodPlanes[0],e);this._renderer.compile(t,Aa)}_sceneToCubeUV(e,t,i,r,a){const c=new kt(90,1,t,i),l=[1,-1,1,1,1,1],d=[1,1,1,-1,-1,-1],h=this._renderer,f=h.autoClear,m=h.toneMapping;h.getClearColor(qo),h.toneMapping=Cn,h.autoClear=!1;const g=new Ln({name:"PMREM.Background",side:Ct,depthWrite:!1,depthTest:!1}),_=new Le(new Qt,g);let p=!1;const u=e.background;u?u.isColor&&(g.color.copy(u),e.background=null,p=!0):(g.color.copy(qo),p=!0);for(let E=0;E<6;E++){const y=E%3;y===0?(c.up.set(0,l[E],0),c.position.set(a.x,a.y,a.z),c.lookAt(a.x+d[E],a.y,a.z)):y===1?(c.up.set(0,0,l[E]),c.position.set(a.x,a.y,a.z),c.lookAt(a.x,a.y+d[E],a.z)):(c.up.set(0,l[E],0),c.position.set(a.x,a.y,a.z),c.lookAt(a.x,a.y,a.z+d[E]));const M=this._cubeSize;Lr(r,y*M,E>2?M:0,M,M),h.setRenderTarget(r),p&&h.render(_,c),h.render(e,c)}_.geometry.dispose(),_.material.dispose(),h.toneMapping=m,h.autoClear=f,e.background=u}_textureToCubeUV(e,t){const i=this._renderer,r=e.mapping===Pi||e.mapping===Di;r?(this._cubemapMaterial===null&&(this._cubemapMaterial=Zo()),this._cubemapMaterial.uniforms.flipEnvMap.value=e.isRenderTargetTexture===!1?-1:1):this._equirectMaterial===null&&(this._equirectMaterial=Yo());const a=r?this._cubemapMaterial:this._equirectMaterial,s=new Le(this._lodPlanes[0],a),o=a.uniforms;o.envMap.value=e;const c=this._cubeSize;Lr(t,0,0,3*c,2*c),i.setRenderTarget(t),i.render(s,Aa)}_applyPMREM(e){const t=this._renderer,i=t.autoClear;t.autoClear=!1;const r=this._lodPlanes.length;for(let a=1;a<r;a++){const s=Math.sqrt(this._sigmas[a]*this._sigmas[a]-this._sigmas[a-1]*this._sigmas[a-1]),o=Ko[(r-a-1)%Ko.length];this._blur(e,a-1,a,s,o)}t.autoClear=i}_blur(e,t,i,r,a){const s=this._pingPongRenderTarget;this._halfBlur(e,s,t,i,r,"latitudinal",a),this._halfBlur(s,e,i,i,r,"longitudinal",a)}_halfBlur(e,t,i,r,a,s,o){const c=this._renderer,l=this._blurMaterial;s!=="latitudinal"&&s!=="longitudinal"&&console.error("blur direction must be either latitudinal or longitudinal!");const d=3,h=new Le(this._lodPlanes[r],l),f=l.uniforms,m=this._sizeLods[i]-1,g=isFinite(a)?Math.PI/(2*m):2*Math.PI/(2*qn-1),_=a/g,p=isFinite(a)?1+Math.floor(d*_):qn;p>qn&&console.warn(`sigmaRadians, ${a}, is too large and will clip, as it requested ${p} samples when the maximum is set to ${qn}`);const u=[];let E=0;for(let b=0;b<qn;++b){const C=b/_,v=Math.exp(-C*C/2);u.push(v),b===0?E+=v:b<p&&(E+=2*v)}for(let b=0;b<u.length;b++)u[b]=u[b]/E;f.envMap.value=e.texture,f.samples.value=p,f.weights.value=u,f.latitudinal.value=s==="latitudinal",o&&(f.poleAxis.value=o);const{_lodMax:y}=this;f.dTheta.value=g,f.mipInt.value=y-i;const M=this._sizeLods[r],D=3*M*(r>y-yi?r-y+yi:0),A=4*(this._cubeSize-M);Lr(t,D,A,3*M,2*M),c.setRenderTarget(t),c.render(h,Aa)}}function Of(n){const e=[],t=[],i=[];let r=n;const a=n-yi+1+Xo.length;for(let s=0;s<a;s++){const o=Math.pow(2,r);t.push(o);let c=1/o;s>n-yi?c=Xo[s-n+yi-1]:s===0&&(c=0),i.push(c);const l=1/(o-2),d=-l,h=1+l,f=[d,d,h,d,h,h,d,d,h,h,d,h],m=6,g=6,_=3,p=2,u=1,E=new Float32Array(_*g*m),y=new Float32Array(p*g*m),M=new Float32Array(u*g*m);for(let A=0;A<m;A++){const b=A%3*2/3-1,C=A>2?0:-1,v=[b,C,0,b+2/3,C,0,b+2/3,C+1,0,b,C,0,b+2/3,C+1,0,b,C+1,0];E.set(v,_*g*A),y.set(f,p*g*A);const x=[A,A,A,A,A,A];M.set(x,u*g*A)}const D=new Xe;D.setAttribute("position",new en(E,_)),D.setAttribute("uv",new en(y,p)),D.setAttribute("faceIndex",new en(M,u)),e.push(D),r>yi&&r--}return{lodPlanes:e,sizeLods:t,sigmas:i}}function $o(n,e,t){const i=new ti(n,e,t);return i.texture.mapping=Kr,i.texture.name="PMREM.cubeUv",i.scissorTest=!0,i}function Lr(n,e,t,i,r){n.viewport.set(e,t,i,r),n.scissor.set(e,t,i,r)}function Bf(n,e,t){const i=new Float32Array(qn),r=new F(0,1,0);return new Dn({name:"SphericalGaussianBlur",defines:{n:qn,CUBEUV_TEXEL_WIDTH:1/e,CUBEUV_TEXEL_HEIGHT:1/t,CUBEUV_MAX_MIP:`${n}.0`},uniforms:{envMap:{value:null},samples:{value:1},weights:{value:i},latitudinal:{value:!1},dTheta:{value:0},mipInt:{value:0},poleAxis:{value:r}},vertexShader:$s(),fragmentShader:`

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
		`,blending:Rn,depthTest:!1,depthWrite:!1})}function Yo(){return new Dn({name:"EquirectangularToCubeUV",uniforms:{envMap:{value:null}},vertexShader:$s(),fragmentShader:`

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
		`,blending:Rn,depthTest:!1,depthWrite:!1})}function Zo(){return new Dn({name:"CubemapToCubeUV",uniforms:{envMap:{value:null},flipEnvMap:{value:-1}},vertexShader:$s(),fragmentShader:`

			precision mediump float;
			precision mediump int;

			uniform float flipEnvMap;

			varying vec3 vOutputDirection;

			uniform samplerCube envMap;

			void main() {

				gl_FragColor = textureCube( envMap, vec3( flipEnvMap * vOutputDirection.x, vOutputDirection.yz ) );

			}
		`,blending:Rn,depthTest:!1,depthWrite:!1})}function $s(){return`

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
	`}function Vf(n){let e=new WeakMap,t=null;function i(o){if(o&&o.isTexture){const c=o.mapping,l=c===Ka||c===$a,d=c===Pi||c===Di;if(l||d){let h=e.get(o);const f=h!==void 0?h.texture.pmremVersion:0;if(o.isRenderTargetTexture&&o.pmremVersion!==f)return t===null&&(t=new ws(n)),h=l?t.fromEquirectangular(o,h):t.fromCubemap(o,h),h.texture.pmremVersion=o.pmremVersion,e.set(o,h),h.texture;if(h!==void 0)return h.texture;{const m=o.image;return l&&m&&m.height>0||d&&m&&r(m)?(t===null&&(t=new ws(n)),h=l?t.fromEquirectangular(o):t.fromCubemap(o),h.texture.pmremVersion=o.pmremVersion,e.set(o,h),o.addEventListener("dispose",a),h.texture):null}}}return o}function r(o){let c=0;const l=6;for(let d=0;d<l;d++)o[d]!==void 0&&c++;return c===l}function a(o){const c=o.target;c.removeEventListener("dispose",a);const l=e.get(c);l!==void 0&&(e.delete(c),l.dispose())}function s(){e=new WeakMap,t!==null&&(t.dispose(),t=null)}return{get:i,dispose:s}}function Gf(n){const e={};function t(i){if(e[i]!==void 0)return e[i];let r;switch(i){case"WEBGL_depth_texture":r=n.getExtension("WEBGL_depth_texture")||n.getExtension("MOZ_WEBGL_depth_texture")||n.getExtension("WEBKIT_WEBGL_depth_texture");break;case"EXT_texture_filter_anisotropic":r=n.getExtension("EXT_texture_filter_anisotropic")||n.getExtension("MOZ_EXT_texture_filter_anisotropic")||n.getExtension("WEBKIT_EXT_texture_filter_anisotropic");break;case"WEBGL_compressed_texture_s3tc":r=n.getExtension("WEBGL_compressed_texture_s3tc")||n.getExtension("MOZ_WEBGL_compressed_texture_s3tc")||n.getExtension("WEBKIT_WEBGL_compressed_texture_s3tc");break;case"WEBGL_compressed_texture_pvrtc":r=n.getExtension("WEBGL_compressed_texture_pvrtc")||n.getExtension("WEBKIT_WEBGL_compressed_texture_pvrtc");break;default:r=n.getExtension(i)}return e[i]=r,r}return{has:function(i){return t(i)!==null},init:function(){t("EXT_color_buffer_float"),t("WEBGL_clip_cull_distance"),t("OES_texture_float_linear"),t("EXT_color_buffer_half_float"),t("WEBGL_multisampled_render_to_texture"),t("WEBGL_render_shared_exponent")},get:function(i){const r=t(i);return r===null&&Vn("THREE.WebGLRenderer: "+i+" extension not supported."),r}}}function Hf(n,e,t,i){const r={},a=new WeakMap;function s(h){const f=h.target;f.index!==null&&e.remove(f.index);for(const g in f.attributes)e.remove(f.attributes[g]);f.removeEventListener("dispose",s),delete r[f.id];const m=a.get(f);m&&(e.remove(m),a.delete(f)),i.releaseStatesOfGeometry(f),f.isInstancedBufferGeometry===!0&&delete f._maxInstanceCount,t.memory.geometries--}function o(h,f){return r[f.id]===!0||(f.addEventListener("dispose",s),r[f.id]=!0,t.memory.geometries++),f}function c(h){const f=h.attributes;for(const m in f)e.update(f[m],n.ARRAY_BUFFER)}function l(h){const f=[],m=h.index,g=h.attributes.position;let _=0;if(m!==null){const E=m.array;_=m.version;for(let y=0,M=E.length;y<M;y+=3){const D=E[y+0],A=E[y+1],b=E[y+2];f.push(D,A,A,b,b,D)}}else if(g!==void 0){const E=g.array;_=g.version;for(let y=0,M=E.length/3-1;y<M;y+=3){const D=y+0,A=y+1,b=y+2;f.push(D,A,A,b,b,D)}}else return;const p=new(Xc(f)?Yc:$c)(f,1);p.version=_;const u=a.get(h);u&&e.remove(u),a.set(h,p)}function d(h){const f=a.get(h);if(f){const m=h.index;m!==null&&f.version<m.version&&l(h)}else l(h);return a.get(h)}return{get:o,update:c,getWireframeAttribute:d}}function jf(n,e,t){let i;function r(f){i=f}let a,s;function o(f){a=f.type,s=f.bytesPerElement}function c(f,m){n.drawElements(i,m,a,f*s),t.update(m,i,1)}function l(f,m,g){g!==0&&(n.drawElementsInstanced(i,m,a,f*s,g),t.update(m,i,g))}function d(f,m,g){if(g===0)return;e.get("WEBGL_multi_draw").multiDrawElementsWEBGL(i,m,0,a,f,0,g);let p=0;for(let u=0;u<g;u++)p+=m[u];t.update(p,i,1)}function h(f,m,g,_){if(g===0)return;const p=e.get("WEBGL_multi_draw");if(p===null)for(let u=0;u<f.length;u++)l(f[u]/s,m[u],_[u]);else{p.multiDrawElementsInstancedWEBGL(i,m,0,a,f,0,_,0,g);let u=0;for(let E=0;E<g;E++)u+=m[E]*_[E];t.update(u,i,1)}}this.setMode=r,this.setIndex=o,this.render=c,this.renderInstances=l,this.renderMultiDraw=d,this.renderMultiDrawInstances=h}function Wf(n){const e={geometries:0,textures:0},t={frame:0,calls:0,triangles:0,points:0,lines:0};function i(a,s,o){switch(t.calls++,s){case n.TRIANGLES:t.triangles+=o*(a/3);break;case n.LINES:t.lines+=o*(a/2);break;case n.LINE_STRIP:t.lines+=o*(a-1);break;case n.LINE_LOOP:t.lines+=o*a;break;case n.POINTS:t.points+=o*a;break;default:console.error("THREE.WebGLInfo: Unknown draw mode:",s);break}}function r(){t.calls=0,t.triangles=0,t.points=0,t.lines=0}return{memory:e,render:t,programs:null,autoReset:!0,reset:r,update:i}}function Xf(n,e,t){const i=new WeakMap,r=new rt;function a(s,o,c){const l=s.morphTargetInfluences,d=o.morphAttributes.position||o.morphAttributes.normal||o.morphAttributes.color,h=d!==void 0?d.length:0;let f=i.get(o);if(f===void 0||f.count!==h){let v=function(){b.dispose(),i.delete(o),o.removeEventListener("dispose",v)};f!==void 0&&f.texture.dispose();const m=o.morphAttributes.position!==void 0,g=o.morphAttributes.normal!==void 0,_=o.morphAttributes.color!==void 0,p=o.morphAttributes.position||[],u=o.morphAttributes.normal||[],E=o.morphAttributes.color||[];let y=0;m===!0&&(y=1),g===!0&&(y=2),_===!0&&(y=3);let M=o.attributes.position.count*y,D=1;M>e.maxTextureSize&&(D=Math.ceil(M/e.maxTextureSize),M=e.maxTextureSize);const A=new Float32Array(M*D*4*h),b=new qc(A,M,D,h);b.type=hn,b.needsUpdate=!0;const C=y*4;for(let x=0;x<h;x++){const P=p[x],U=u[x],w=E[x],R=M*D*4*x;for(let z=0;z<P.count;z++){const N=z*C;m===!0&&(r.fromBufferAttribute(P,z),A[R+N+0]=r.x,A[R+N+1]=r.y,A[R+N+2]=r.z,A[R+N+3]=0),g===!0&&(r.fromBufferAttribute(U,z),A[R+N+4]=r.x,A[R+N+5]=r.y,A[R+N+6]=r.z,A[R+N+7]=0),_===!0&&(r.fromBufferAttribute(w,z),A[R+N+8]=r.x,A[R+N+9]=r.y,A[R+N+10]=r.z,A[R+N+11]=w.itemSize===4?r.w:1)}}f={count:h,texture:b,size:new We(M,D)},i.set(o,f),o.addEventListener("dispose",v)}if(s.isInstancedMesh===!0&&s.morphTexture!==null)c.getUniforms().setValue(n,"morphTexture",s.morphTexture,t);else{let m=0;for(let _=0;_<l.length;_++)m+=l[_];const g=o.morphTargetsRelative?1:1-m;c.getUniforms().setValue(n,"morphTargetBaseInfluence",g),c.getUniforms().setValue(n,"morphTargetInfluences",l)}c.getUniforms().setValue(n,"morphTargetsTexture",f.texture,t),c.getUniforms().setValue(n,"morphTargetsTextureSize",f.size)}return{update:a}}function qf(n,e,t,i){let r=new WeakMap;function a(c){const l=i.render.frame,d=c.geometry,h=e.get(c,d);if(r.get(h)!==l&&(e.update(h),r.set(h,l)),c.isInstancedMesh&&(c.hasEventListener("dispose",o)===!1&&c.addEventListener("dispose",o),r.get(c)!==l&&(t.update(c.instanceMatrix,n.ARRAY_BUFFER),c.instanceColor!==null&&t.update(c.instanceColor,n.ARRAY_BUFFER),r.set(c,l))),c.isSkinnedMesh){const f=c.skeleton;r.get(f)!==l&&(f.update(),r.set(f,l))}return h}function s(){r=new WeakMap}function o(c){const l=c.target;l.removeEventListener("dispose",o),t.remove(l.instanceMatrix),l.instanceColor!==null&&t.remove(l.instanceColor)}return{update:a,dispose:s}}const al=new wt,Jo=new tl(1,1),sl=new qc,ol=new _u,cl=new Qc,Qo=[],ec=[],tc=new Float32Array(16),nc=new Float32Array(9),ic=new Float32Array(4);function Vi(n,e,t){const i=n[0];if(i<=0||i>0)return n;const r=e*t;let a=Qo[r];if(a===void 0&&(a=new Float32Array(r),Qo[r]=a),e!==0){i.toArray(a,0);for(let s=1,o=0;s!==e;++s)o+=t,n[s].toArray(a,o)}return a}function gt(n,e){if(n.length!==e.length)return!1;for(let t=0,i=n.length;t<i;t++)if(n[t]!==e[t])return!1;return!0}function _t(n,e){for(let t=0,i=e.length;t<i;t++)n[t]=e[t]}function Yr(n,e){let t=ec[e];t===void 0&&(t=new Int32Array(e),ec[e]=t);for(let i=0;i!==e;++i)t[i]=n.allocateTextureUnit();return t}function Kf(n,e){const t=this.cache;t[0]!==e&&(n.uniform1f(this.addr,e),t[0]=e)}function $f(n,e){const t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y)&&(n.uniform2f(this.addr,e.x,e.y),t[0]=e.x,t[1]=e.y);else{if(gt(t,e))return;n.uniform2fv(this.addr,e),_t(t,e)}}function Yf(n,e){const t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y||t[2]!==e.z)&&(n.uniform3f(this.addr,e.x,e.y,e.z),t[0]=e.x,t[1]=e.y,t[2]=e.z);else if(e.r!==void 0)(t[0]!==e.r||t[1]!==e.g||t[2]!==e.b)&&(n.uniform3f(this.addr,e.r,e.g,e.b),t[0]=e.r,t[1]=e.g,t[2]=e.b);else{if(gt(t,e))return;n.uniform3fv(this.addr,e),_t(t,e)}}function Zf(n,e){const t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y||t[2]!==e.z||t[3]!==e.w)&&(n.uniform4f(this.addr,e.x,e.y,e.z,e.w),t[0]=e.x,t[1]=e.y,t[2]=e.z,t[3]=e.w);else{if(gt(t,e))return;n.uniform4fv(this.addr,e),_t(t,e)}}function Jf(n,e){const t=this.cache,i=e.elements;if(i===void 0){if(gt(t,e))return;n.uniformMatrix2fv(this.addr,!1,e),_t(t,e)}else{if(gt(t,i))return;ic.set(i),n.uniformMatrix2fv(this.addr,!1,ic),_t(t,i)}}function Qf(n,e){const t=this.cache,i=e.elements;if(i===void 0){if(gt(t,e))return;n.uniformMatrix3fv(this.addr,!1,e),_t(t,e)}else{if(gt(t,i))return;nc.set(i),n.uniformMatrix3fv(this.addr,!1,nc),_t(t,i)}}function ep(n,e){const t=this.cache,i=e.elements;if(i===void 0){if(gt(t,e))return;n.uniformMatrix4fv(this.addr,!1,e),_t(t,e)}else{if(gt(t,i))return;tc.set(i),n.uniformMatrix4fv(this.addr,!1,tc),_t(t,i)}}function tp(n,e){const t=this.cache;t[0]!==e&&(n.uniform1i(this.addr,e),t[0]=e)}function np(n,e){const t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y)&&(n.uniform2i(this.addr,e.x,e.y),t[0]=e.x,t[1]=e.y);else{if(gt(t,e))return;n.uniform2iv(this.addr,e),_t(t,e)}}function ip(n,e){const t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y||t[2]!==e.z)&&(n.uniform3i(this.addr,e.x,e.y,e.z),t[0]=e.x,t[1]=e.y,t[2]=e.z);else{if(gt(t,e))return;n.uniform3iv(this.addr,e),_t(t,e)}}function rp(n,e){const t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y||t[2]!==e.z||t[3]!==e.w)&&(n.uniform4i(this.addr,e.x,e.y,e.z,e.w),t[0]=e.x,t[1]=e.y,t[2]=e.z,t[3]=e.w);else{if(gt(t,e))return;n.uniform4iv(this.addr,e),_t(t,e)}}function ap(n,e){const t=this.cache;t[0]!==e&&(n.uniform1ui(this.addr,e),t[0]=e)}function sp(n,e){const t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y)&&(n.uniform2ui(this.addr,e.x,e.y),t[0]=e.x,t[1]=e.y);else{if(gt(t,e))return;n.uniform2uiv(this.addr,e),_t(t,e)}}function op(n,e){const t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y||t[2]!==e.z)&&(n.uniform3ui(this.addr,e.x,e.y,e.z),t[0]=e.x,t[1]=e.y,t[2]=e.z);else{if(gt(t,e))return;n.uniform3uiv(this.addr,e),_t(t,e)}}function cp(n,e){const t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y||t[2]!==e.z||t[3]!==e.w)&&(n.uniform4ui(this.addr,e.x,e.y,e.z,e.w),t[0]=e.x,t[1]=e.y,t[2]=e.z,t[3]=e.w);else{if(gt(t,e))return;n.uniform4uiv(this.addr,e),_t(t,e)}}function lp(n,e,t){const i=this.cache,r=t.allocateTextureUnit();i[0]!==r&&(n.uniform1i(this.addr,r),i[0]=r);let a;this.type===n.SAMPLER_2D_SHADOW?(Jo.compareFunction=Wc,a=Jo):a=al,t.setTexture2D(e||a,r)}function up(n,e,t){const i=this.cache,r=t.allocateTextureUnit();i[0]!==r&&(n.uniform1i(this.addr,r),i[0]=r),t.setTexture3D(e||ol,r)}function dp(n,e,t){const i=this.cache,r=t.allocateTextureUnit();i[0]!==r&&(n.uniform1i(this.addr,r),i[0]=r),t.setTextureCube(e||cl,r)}function hp(n,e,t){const i=this.cache,r=t.allocateTextureUnit();i[0]!==r&&(n.uniform1i(this.addr,r),i[0]=r),t.setTexture2DArray(e||sl,r)}function fp(n){switch(n){case 5126:return Kf;case 35664:return $f;case 35665:return Yf;case 35666:return Zf;case 35674:return Jf;case 35675:return Qf;case 35676:return ep;case 5124:case 35670:return tp;case 35667:case 35671:return np;case 35668:case 35672:return ip;case 35669:case 35673:return rp;case 5125:return ap;case 36294:return sp;case 36295:return op;case 36296:return cp;case 35678:case 36198:case 36298:case 36306:case 35682:return lp;case 35679:case 36299:case 36307:return up;case 35680:case 36300:case 36308:case 36293:return dp;case 36289:case 36303:case 36311:case 36292:return hp}}function pp(n,e){n.uniform1fv(this.addr,e)}function mp(n,e){const t=Vi(e,this.size,2);n.uniform2fv(this.addr,t)}function gp(n,e){const t=Vi(e,this.size,3);n.uniform3fv(this.addr,t)}function _p(n,e){const t=Vi(e,this.size,4);n.uniform4fv(this.addr,t)}function vp(n,e){const t=Vi(e,this.size,4);n.uniformMatrix2fv(this.addr,!1,t)}function xp(n,e){const t=Vi(e,this.size,9);n.uniformMatrix3fv(this.addr,!1,t)}function Mp(n,e){const t=Vi(e,this.size,16);n.uniformMatrix4fv(this.addr,!1,t)}function Sp(n,e){n.uniform1iv(this.addr,e)}function Ep(n,e){n.uniform2iv(this.addr,e)}function yp(n,e){n.uniform3iv(this.addr,e)}function bp(n,e){n.uniform4iv(this.addr,e)}function Tp(n,e){n.uniform1uiv(this.addr,e)}function wp(n,e){n.uniform2uiv(this.addr,e)}function Ap(n,e){n.uniform3uiv(this.addr,e)}function Rp(n,e){n.uniform4uiv(this.addr,e)}function Cp(n,e,t){const i=this.cache,r=e.length,a=Yr(t,r);gt(i,a)||(n.uniform1iv(this.addr,a),_t(i,a));for(let s=0;s!==r;++s)t.setTexture2D(e[s]||al,a[s])}function Pp(n,e,t){const i=this.cache,r=e.length,a=Yr(t,r);gt(i,a)||(n.uniform1iv(this.addr,a),_t(i,a));for(let s=0;s!==r;++s)t.setTexture3D(e[s]||ol,a[s])}function Dp(n,e,t){const i=this.cache,r=e.length,a=Yr(t,r);gt(i,a)||(n.uniform1iv(this.addr,a),_t(i,a));for(let s=0;s!==r;++s)t.setTextureCube(e[s]||cl,a[s])}function Lp(n,e,t){const i=this.cache,r=e.length,a=Yr(t,r);gt(i,a)||(n.uniform1iv(this.addr,a),_t(i,a));for(let s=0;s!==r;++s)t.setTexture2DArray(e[s]||sl,a[s])}function Ip(n){switch(n){case 5126:return pp;case 35664:return mp;case 35665:return gp;case 35666:return _p;case 35674:return vp;case 35675:return xp;case 35676:return Mp;case 5124:case 35670:return Sp;case 35667:case 35671:return Ep;case 35668:case 35672:return yp;case 35669:case 35673:return bp;case 5125:return Tp;case 36294:return wp;case 36295:return Ap;case 36296:return Rp;case 35678:case 36198:case 36298:case 36306:case 35682:return Cp;case 35679:case 36299:case 36307:return Pp;case 35680:case 36300:case 36308:case 36293:return Dp;case 36289:case 36303:case 36311:case 36292:return Lp}}class Up{constructor(e,t,i){this.id=e,this.addr=i,this.cache=[],this.type=t.type,this.setValue=fp(t.type)}}class zp{constructor(e,t,i){this.id=e,this.addr=i,this.cache=[],this.type=t.type,this.size=t.size,this.setValue=Ip(t.type)}}class Np{constructor(e){this.id=e,this.seq=[],this.map={}}setValue(e,t,i){const r=this.seq;for(let a=0,s=r.length;a!==s;++a){const o=r[a];o.setValue(e,t[o.id],i)}}}const La=/(\w+)(\])?(\[|\.)?/g;function rc(n,e){n.seq.push(e),n.map[e.id]=e}function kp(n,e,t){const i=n.name,r=i.length;for(La.lastIndex=0;;){const a=La.exec(i),s=La.lastIndex;let o=a[1];const c=a[2]==="]",l=a[3];if(c&&(o=o|0),l===void 0||l==="["&&s+2===r){rc(t,l===void 0?new Up(o,n,e):new zp(o,n,e));break}else{let h=t.map[o];h===void 0&&(h=new Np(o),rc(t,h)),t=h}}}class Vr{constructor(e,t){this.seq=[],this.map={};const i=e.getProgramParameter(t,e.ACTIVE_UNIFORMS);for(let r=0;r<i;++r){const a=e.getActiveUniform(t,r),s=e.getUniformLocation(t,a.name);kp(a,s,this)}}setValue(e,t,i,r){const a=this.map[t];a!==void 0&&a.setValue(e,i,r)}setOptional(e,t,i){const r=t[i];r!==void 0&&this.setValue(e,i,r)}static upload(e,t,i,r){for(let a=0,s=t.length;a!==s;++a){const o=t[a],c=i[o.id];c.needsUpdate!==!1&&o.setValue(e,c.value,r)}}static seqWithValue(e,t){const i=[];for(let r=0,a=e.length;r!==a;++r){const s=e[r];s.id in t&&i.push(s)}return i}}function ac(n,e,t){const i=n.createShader(e);return n.shaderSource(i,t),n.compileShader(i),i}const Fp=37297;let Op=0;function Bp(n,e){const t=n.split(`
`),i=[],r=Math.max(e-6,0),a=Math.min(e+6,t.length);for(let s=r;s<a;s++){const o=s+1;i.push(`${o===e?">":" "} ${o}: ${t[s]}`)}return i.join(`
`)}const sc=new Ve;function Vp(n){Je._getMatrix(sc,Je.workingColorSpace,n);const e=`mat3( ${sc.elements.map(t=>t.toFixed(4))} )`;switch(Je.getTransfer(n)){case Hr:return[e,"LinearTransferOETF"];case it:return[e,"sRGBTransferOETF"];default:return console.warn("THREE.WebGLProgram: Unsupported color space: ",n),[e,"LinearTransferOETF"]}}function oc(n,e,t){const i=n.getShaderParameter(e,n.COMPILE_STATUS),r=n.getShaderInfoLog(e).trim();if(i&&r==="")return"";const a=/ERROR: 0:(\d+)/.exec(r);if(a){const s=parseInt(a[1]);return t.toUpperCase()+`

`+r+`

`+Bp(n.getShaderSource(e),s)}else return r}function Gp(n,e){const t=Vp(e);return[`vec4 ${n}( vec4 value ) {`,`	return ${t[1]}( vec4( value.rgb * ${t[0]}, value.a ) );`,"}"].join(`
`)}function Hp(n,e){let t;switch(e){case Hl:t="Linear";break;case jl:t="Reinhard";break;case Wl:t="Cineon";break;case Xl:t="ACESFilmic";break;case Kl:t="AgX";break;case $l:t="Neutral";break;case ql:t="Custom";break;default:console.warn("THREE.WebGLProgram: Unsupported toneMapping:",e),t="Linear"}return"vec3 "+n+"( vec3 color ) { return "+t+"ToneMapping( color ); }"}const Ir=new F;function jp(){Je.getLuminanceCoefficients(Ir);const n=Ir.x.toFixed(4),e=Ir.y.toFixed(4),t=Ir.z.toFixed(4);return["float luminance( const in vec3 rgb ) {",`	const vec3 weights = vec3( ${n}, ${e}, ${t} );`,"	return dot( weights, rgb );","}"].join(`
`)}function Wp(n){return[n.extensionClipCullDistance?"#extension GL_ANGLE_clip_cull_distance : require":"",n.extensionMultiDraw?"#extension GL_ANGLE_multi_draw : require":""].filter(Zi).join(`
`)}function Xp(n){const e=[];for(const t in n){const i=n[t];i!==!1&&e.push("#define "+t+" "+i)}return e.join(`
`)}function qp(n,e){const t={},i=n.getProgramParameter(e,n.ACTIVE_ATTRIBUTES);for(let r=0;r<i;r++){const a=n.getActiveAttrib(e,r),s=a.name;let o=1;a.type===n.FLOAT_MAT2&&(o=2),a.type===n.FLOAT_MAT3&&(o=3),a.type===n.FLOAT_MAT4&&(o=4),t[s]={type:a.type,location:n.getAttribLocation(e,s),locationSize:o}}return t}function Zi(n){return n!==""}function cc(n,e){const t=e.numSpotLightShadows+e.numSpotLightMaps-e.numSpotLightShadowsWithMaps;return n.replace(/NUM_DIR_LIGHTS/g,e.numDirLights).replace(/NUM_SPOT_LIGHTS/g,e.numSpotLights).replace(/NUM_SPOT_LIGHT_MAPS/g,e.numSpotLightMaps).replace(/NUM_SPOT_LIGHT_COORDS/g,t).replace(/NUM_RECT_AREA_LIGHTS/g,e.numRectAreaLights).replace(/NUM_POINT_LIGHTS/g,e.numPointLights).replace(/NUM_HEMI_LIGHTS/g,e.numHemiLights).replace(/NUM_DIR_LIGHT_SHADOWS/g,e.numDirLightShadows).replace(/NUM_SPOT_LIGHT_SHADOWS_WITH_MAPS/g,e.numSpotLightShadowsWithMaps).replace(/NUM_SPOT_LIGHT_SHADOWS/g,e.numSpotLightShadows).replace(/NUM_POINT_LIGHT_SHADOWS/g,e.numPointLightShadows)}function lc(n,e){return n.replace(/NUM_CLIPPING_PLANES/g,e.numClippingPlanes).replace(/UNION_CLIPPING_PLANES/g,e.numClippingPlanes-e.numClipIntersection)}const Kp=/^[ \t]*#include +<([\w\d./]+)>/gm;function As(n){return n.replace(Kp,Yp)}const $p=new Map;function Yp(n,e){let t=He[e];if(t===void 0){const i=$p.get(e);if(i!==void 0)t=He[i],console.warn('THREE.WebGLRenderer: Shader chunk "%s" has been deprecated. Use "%s" instead.',e,i);else throw new Error("Can not resolve #include <"+e+">")}return As(t)}const Zp=/#pragma unroll_loop_start\s+for\s*\(\s*int\s+i\s*=\s*(\d+)\s*;\s*i\s*<\s*(\d+)\s*;\s*i\s*\+\+\s*\)\s*{([\s\S]+?)}\s+#pragma unroll_loop_end/g;function uc(n){return n.replace(Zp,Jp)}function Jp(n,e,t,i){let r="";for(let a=parseInt(e);a<parseInt(t);a++)r+=i.replace(/\[\s*i\s*\]/g,"[ "+a+" ]").replace(/UNROLLED_LOOP_INDEX/g,a);return r}function dc(n){let e=`precision ${n.precision} float;
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
#define LOW_PRECISION`),e}function Qp(n){let e="SHADOWMAP_TYPE_BASIC";return n.shadowMapType===Dc?e="SHADOWMAP_TYPE_PCF":n.shadowMapType===El?e="SHADOWMAP_TYPE_PCF_SOFT":n.shadowMapType===un&&(e="SHADOWMAP_TYPE_VSM"),e}function em(n){let e="ENVMAP_TYPE_CUBE";if(n.envMap)switch(n.envMapMode){case Pi:case Di:e="ENVMAP_TYPE_CUBE";break;case Kr:e="ENVMAP_TYPE_CUBE_UV";break}return e}function tm(n){let e="ENVMAP_MODE_REFLECTION";if(n.envMap)switch(n.envMapMode){case Di:e="ENVMAP_MODE_REFRACTION";break}return e}function nm(n){let e="ENVMAP_BLENDING_NONE";if(n.envMap)switch(n.combine){case Lc:e="ENVMAP_BLENDING_MULTIPLY";break;case Vl:e="ENVMAP_BLENDING_MIX";break;case Gl:e="ENVMAP_BLENDING_ADD";break}return e}function im(n){const e=n.envMapCubeUVHeight;if(e===null)return null;const t=Math.log2(e)-2,i=1/e;return{texelWidth:1/(3*Math.max(Math.pow(2,t),112)),texelHeight:i,maxMip:t}}function rm(n,e,t,i){const r=n.getContext(),a=t.defines;let s=t.vertexShader,o=t.fragmentShader;const c=Qp(t),l=em(t),d=tm(t),h=nm(t),f=im(t),m=Wp(t),g=Xp(a),_=r.createProgram();let p,u,E=t.glslVersion?"#version "+t.glslVersion+`
`:"";t.isRawShaderMaterial?(p=["#define SHADER_TYPE "+t.shaderType,"#define SHADER_NAME "+t.shaderName,g].filter(Zi).join(`
`),p.length>0&&(p+=`
`),u=["#define SHADER_TYPE "+t.shaderType,"#define SHADER_NAME "+t.shaderName,g].filter(Zi).join(`
`),u.length>0&&(u+=`
`)):(p=[dc(t),"#define SHADER_TYPE "+t.shaderType,"#define SHADER_NAME "+t.shaderName,g,t.extensionClipCullDistance?"#define USE_CLIP_DISTANCE":"",t.batching?"#define USE_BATCHING":"",t.batchingColor?"#define USE_BATCHING_COLOR":"",t.instancing?"#define USE_INSTANCING":"",t.instancingColor?"#define USE_INSTANCING_COLOR":"",t.instancingMorph?"#define USE_INSTANCING_MORPH":"",t.useFog&&t.fog?"#define USE_FOG":"",t.useFog&&t.fogExp2?"#define FOG_EXP2":"",t.map?"#define USE_MAP":"",t.envMap?"#define USE_ENVMAP":"",t.envMap?"#define "+d:"",t.lightMap?"#define USE_LIGHTMAP":"",t.aoMap?"#define USE_AOMAP":"",t.bumpMap?"#define USE_BUMPMAP":"",t.normalMap?"#define USE_NORMALMAP":"",t.normalMapObjectSpace?"#define USE_NORMALMAP_OBJECTSPACE":"",t.normalMapTangentSpace?"#define USE_NORMALMAP_TANGENTSPACE":"",t.displacementMap?"#define USE_DISPLACEMENTMAP":"",t.emissiveMap?"#define USE_EMISSIVEMAP":"",t.anisotropy?"#define USE_ANISOTROPY":"",t.anisotropyMap?"#define USE_ANISOTROPYMAP":"",t.clearcoatMap?"#define USE_CLEARCOATMAP":"",t.clearcoatRoughnessMap?"#define USE_CLEARCOAT_ROUGHNESSMAP":"",t.clearcoatNormalMap?"#define USE_CLEARCOAT_NORMALMAP":"",t.iridescenceMap?"#define USE_IRIDESCENCEMAP":"",t.iridescenceThicknessMap?"#define USE_IRIDESCENCE_THICKNESSMAP":"",t.specularMap?"#define USE_SPECULARMAP":"",t.specularColorMap?"#define USE_SPECULAR_COLORMAP":"",t.specularIntensityMap?"#define USE_SPECULAR_INTENSITYMAP":"",t.roughnessMap?"#define USE_ROUGHNESSMAP":"",t.metalnessMap?"#define USE_METALNESSMAP":"",t.alphaMap?"#define USE_ALPHAMAP":"",t.alphaHash?"#define USE_ALPHAHASH":"",t.transmission?"#define USE_TRANSMISSION":"",t.transmissionMap?"#define USE_TRANSMISSIONMAP":"",t.thicknessMap?"#define USE_THICKNESSMAP":"",t.sheenColorMap?"#define USE_SHEEN_COLORMAP":"",t.sheenRoughnessMap?"#define USE_SHEEN_ROUGHNESSMAP":"",t.mapUv?"#define MAP_UV "+t.mapUv:"",t.alphaMapUv?"#define ALPHAMAP_UV "+t.alphaMapUv:"",t.lightMapUv?"#define LIGHTMAP_UV "+t.lightMapUv:"",t.aoMapUv?"#define AOMAP_UV "+t.aoMapUv:"",t.emissiveMapUv?"#define EMISSIVEMAP_UV "+t.emissiveMapUv:"",t.bumpMapUv?"#define BUMPMAP_UV "+t.bumpMapUv:"",t.normalMapUv?"#define NORMALMAP_UV "+t.normalMapUv:"",t.displacementMapUv?"#define DISPLACEMENTMAP_UV "+t.displacementMapUv:"",t.metalnessMapUv?"#define METALNESSMAP_UV "+t.metalnessMapUv:"",t.roughnessMapUv?"#define ROUGHNESSMAP_UV "+t.roughnessMapUv:"",t.anisotropyMapUv?"#define ANISOTROPYMAP_UV "+t.anisotropyMapUv:"",t.clearcoatMapUv?"#define CLEARCOATMAP_UV "+t.clearcoatMapUv:"",t.clearcoatNormalMapUv?"#define CLEARCOAT_NORMALMAP_UV "+t.clearcoatNormalMapUv:"",t.clearcoatRoughnessMapUv?"#define CLEARCOAT_ROUGHNESSMAP_UV "+t.clearcoatRoughnessMapUv:"",t.iridescenceMapUv?"#define IRIDESCENCEMAP_UV "+t.iridescenceMapUv:"",t.iridescenceThicknessMapUv?"#define IRIDESCENCE_THICKNESSMAP_UV "+t.iridescenceThicknessMapUv:"",t.sheenColorMapUv?"#define SHEEN_COLORMAP_UV "+t.sheenColorMapUv:"",t.sheenRoughnessMapUv?"#define SHEEN_ROUGHNESSMAP_UV "+t.sheenRoughnessMapUv:"",t.specularMapUv?"#define SPECULARMAP_UV "+t.specularMapUv:"",t.specularColorMapUv?"#define SPECULAR_COLORMAP_UV "+t.specularColorMapUv:"",t.specularIntensityMapUv?"#define SPECULAR_INTENSITYMAP_UV "+t.specularIntensityMapUv:"",t.transmissionMapUv?"#define TRANSMISSIONMAP_UV "+t.transmissionMapUv:"",t.thicknessMapUv?"#define THICKNESSMAP_UV "+t.thicknessMapUv:"",t.vertexTangents&&t.flatShading===!1?"#define USE_TANGENT":"",t.vertexColors?"#define USE_COLOR":"",t.vertexAlphas?"#define USE_COLOR_ALPHA":"",t.vertexUv1s?"#define USE_UV1":"",t.vertexUv2s?"#define USE_UV2":"",t.vertexUv3s?"#define USE_UV3":"",t.pointsUvs?"#define USE_POINTS_UV":"",t.flatShading?"#define FLAT_SHADED":"",t.skinning?"#define USE_SKINNING":"",t.morphTargets?"#define USE_MORPHTARGETS":"",t.morphNormals&&t.flatShading===!1?"#define USE_MORPHNORMALS":"",t.morphColors?"#define USE_MORPHCOLORS":"",t.morphTargetsCount>0?"#define MORPHTARGETS_TEXTURE_STRIDE "+t.morphTextureStride:"",t.morphTargetsCount>0?"#define MORPHTARGETS_COUNT "+t.morphTargetsCount:"",t.doubleSided?"#define DOUBLE_SIDED":"",t.flipSided?"#define FLIP_SIDED":"",t.shadowMapEnabled?"#define USE_SHADOWMAP":"",t.shadowMapEnabled?"#define "+c:"",t.sizeAttenuation?"#define USE_SIZEATTENUATION":"",t.numLightProbes>0?"#define USE_LIGHT_PROBES":"",t.logarithmicDepthBuffer?"#define USE_LOGDEPTHBUF":"",t.reverseDepthBuffer?"#define USE_REVERSEDEPTHBUF":"","uniform mat4 modelMatrix;","uniform mat4 modelViewMatrix;","uniform mat4 projectionMatrix;","uniform mat4 viewMatrix;","uniform mat3 normalMatrix;","uniform vec3 cameraPosition;","uniform bool isOrthographic;","#ifdef USE_INSTANCING","	attribute mat4 instanceMatrix;","#endif","#ifdef USE_INSTANCING_COLOR","	attribute vec3 instanceColor;","#endif","#ifdef USE_INSTANCING_MORPH","	uniform sampler2D morphTexture;","#endif","attribute vec3 position;","attribute vec3 normal;","attribute vec2 uv;","#ifdef USE_UV1","	attribute vec2 uv1;","#endif","#ifdef USE_UV2","	attribute vec2 uv2;","#endif","#ifdef USE_UV3","	attribute vec2 uv3;","#endif","#ifdef USE_TANGENT","	attribute vec4 tangent;","#endif","#if defined( USE_COLOR_ALPHA )","	attribute vec4 color;","#elif defined( USE_COLOR )","	attribute vec3 color;","#endif","#ifdef USE_SKINNING","	attribute vec4 skinIndex;","	attribute vec4 skinWeight;","#endif",`
`].filter(Zi).join(`
`),u=[dc(t),"#define SHADER_TYPE "+t.shaderType,"#define SHADER_NAME "+t.shaderName,g,t.useFog&&t.fog?"#define USE_FOG":"",t.useFog&&t.fogExp2?"#define FOG_EXP2":"",t.alphaToCoverage?"#define ALPHA_TO_COVERAGE":"",t.map?"#define USE_MAP":"",t.matcap?"#define USE_MATCAP":"",t.envMap?"#define USE_ENVMAP":"",t.envMap?"#define "+l:"",t.envMap?"#define "+d:"",t.envMap?"#define "+h:"",f?"#define CUBEUV_TEXEL_WIDTH "+f.texelWidth:"",f?"#define CUBEUV_TEXEL_HEIGHT "+f.texelHeight:"",f?"#define CUBEUV_MAX_MIP "+f.maxMip+".0":"",t.lightMap?"#define USE_LIGHTMAP":"",t.aoMap?"#define USE_AOMAP":"",t.bumpMap?"#define USE_BUMPMAP":"",t.normalMap?"#define USE_NORMALMAP":"",t.normalMapObjectSpace?"#define USE_NORMALMAP_OBJECTSPACE":"",t.normalMapTangentSpace?"#define USE_NORMALMAP_TANGENTSPACE":"",t.emissiveMap?"#define USE_EMISSIVEMAP":"",t.anisotropy?"#define USE_ANISOTROPY":"",t.anisotropyMap?"#define USE_ANISOTROPYMAP":"",t.clearcoat?"#define USE_CLEARCOAT":"",t.clearcoatMap?"#define USE_CLEARCOATMAP":"",t.clearcoatRoughnessMap?"#define USE_CLEARCOAT_ROUGHNESSMAP":"",t.clearcoatNormalMap?"#define USE_CLEARCOAT_NORMALMAP":"",t.dispersion?"#define USE_DISPERSION":"",t.iridescence?"#define USE_IRIDESCENCE":"",t.iridescenceMap?"#define USE_IRIDESCENCEMAP":"",t.iridescenceThicknessMap?"#define USE_IRIDESCENCE_THICKNESSMAP":"",t.specularMap?"#define USE_SPECULARMAP":"",t.specularColorMap?"#define USE_SPECULAR_COLORMAP":"",t.specularIntensityMap?"#define USE_SPECULAR_INTENSITYMAP":"",t.roughnessMap?"#define USE_ROUGHNESSMAP":"",t.metalnessMap?"#define USE_METALNESSMAP":"",t.alphaMap?"#define USE_ALPHAMAP":"",t.alphaTest?"#define USE_ALPHATEST":"",t.alphaHash?"#define USE_ALPHAHASH":"",t.sheen?"#define USE_SHEEN":"",t.sheenColorMap?"#define USE_SHEEN_COLORMAP":"",t.sheenRoughnessMap?"#define USE_SHEEN_ROUGHNESSMAP":"",t.transmission?"#define USE_TRANSMISSION":"",t.transmissionMap?"#define USE_TRANSMISSIONMAP":"",t.thicknessMap?"#define USE_THICKNESSMAP":"",t.vertexTangents&&t.flatShading===!1?"#define USE_TANGENT":"",t.vertexColors||t.instancingColor||t.batchingColor?"#define USE_COLOR":"",t.vertexAlphas?"#define USE_COLOR_ALPHA":"",t.vertexUv1s?"#define USE_UV1":"",t.vertexUv2s?"#define USE_UV2":"",t.vertexUv3s?"#define USE_UV3":"",t.pointsUvs?"#define USE_POINTS_UV":"",t.gradientMap?"#define USE_GRADIENTMAP":"",t.flatShading?"#define FLAT_SHADED":"",t.doubleSided?"#define DOUBLE_SIDED":"",t.flipSided?"#define FLIP_SIDED":"",t.shadowMapEnabled?"#define USE_SHADOWMAP":"",t.shadowMapEnabled?"#define "+c:"",t.premultipliedAlpha?"#define PREMULTIPLIED_ALPHA":"",t.numLightProbes>0?"#define USE_LIGHT_PROBES":"",t.decodeVideoTexture?"#define DECODE_VIDEO_TEXTURE":"",t.decodeVideoTextureEmissive?"#define DECODE_VIDEO_TEXTURE_EMISSIVE":"",t.logarithmicDepthBuffer?"#define USE_LOGDEPTHBUF":"",t.reverseDepthBuffer?"#define USE_REVERSEDEPTHBUF":"","uniform mat4 viewMatrix;","uniform vec3 cameraPosition;","uniform bool isOrthographic;",t.toneMapping!==Cn?"#define TONE_MAPPING":"",t.toneMapping!==Cn?He.tonemapping_pars_fragment:"",t.toneMapping!==Cn?Hp("toneMapping",t.toneMapping):"",t.dithering?"#define DITHERING":"",t.opaque?"#define OPAQUE":"",He.colorspace_pars_fragment,Gp("linearToOutputTexel",t.outputColorSpace),jp(),t.useDepthPacking?"#define DEPTH_PACKING "+t.depthPacking:"",`
`].filter(Zi).join(`
`)),s=As(s),s=cc(s,t),s=lc(s,t),o=As(o),o=cc(o,t),o=lc(o,t),s=uc(s),o=uc(o),t.isRawShaderMaterial!==!0&&(E=`#version 300 es
`,p=[m,"#define attribute in","#define varying out","#define texture2D texture"].join(`
`)+`
`+p,u=["#define varying in",t.glslVersion===go?"":"layout(location = 0) out highp vec4 pc_fragColor;",t.glslVersion===go?"":"#define gl_FragColor pc_fragColor","#define gl_FragDepthEXT gl_FragDepth","#define texture2D texture","#define textureCube texture","#define texture2DProj textureProj","#define texture2DLodEXT textureLod","#define texture2DProjLodEXT textureProjLod","#define textureCubeLodEXT textureLod","#define texture2DGradEXT textureGrad","#define texture2DProjGradEXT textureProjGrad","#define textureCubeGradEXT textureGrad"].join(`
`)+`
`+u);const y=E+p+s,M=E+u+o,D=ac(r,r.VERTEX_SHADER,y),A=ac(r,r.FRAGMENT_SHADER,M);r.attachShader(_,D),r.attachShader(_,A),t.index0AttributeName!==void 0?r.bindAttribLocation(_,0,t.index0AttributeName):t.morphTargets===!0&&r.bindAttribLocation(_,0,"position"),r.linkProgram(_);function b(P){if(n.debug.checkShaderErrors){const U=r.getProgramInfoLog(_).trim(),w=r.getShaderInfoLog(D).trim(),R=r.getShaderInfoLog(A).trim();let z=!0,N=!0;if(r.getProgramParameter(_,r.LINK_STATUS)===!1)if(z=!1,typeof n.debug.onShaderError=="function")n.debug.onShaderError(r,_,D,A);else{const B=oc(r,D,"vertex"),k=oc(r,A,"fragment");console.error("THREE.WebGLProgram: Shader Error "+r.getError()+" - VALIDATE_STATUS "+r.getProgramParameter(_,r.VALIDATE_STATUS)+`

Material Name: `+P.name+`
Material Type: `+P.type+`

Program Info Log: `+U+`
`+B+`
`+k)}else U!==""?console.warn("THREE.WebGLProgram: Program Info Log:",U):(w===""||R==="")&&(N=!1);N&&(P.diagnostics={runnable:z,programLog:U,vertexShader:{log:w,prefix:p},fragmentShader:{log:R,prefix:u}})}r.deleteShader(D),r.deleteShader(A),C=new Vr(r,_),v=qp(r,_)}let C;this.getUniforms=function(){return C===void 0&&b(this),C};let v;this.getAttributes=function(){return v===void 0&&b(this),v};let x=t.rendererExtensionParallelShaderCompile===!1;return this.isReady=function(){return x===!1&&(x=r.getProgramParameter(_,Fp)),x},this.destroy=function(){i.releaseStatesOfProgram(this),r.deleteProgram(_),this.program=void 0},this.type=t.shaderType,this.name=t.shaderName,this.id=Op++,this.cacheKey=e,this.usedTimes=1,this.program=_,this.vertexShader=D,this.fragmentShader=A,this}let am=0;class sm{constructor(){this.shaderCache=new Map,this.materialCache=new Map}update(e){const t=e.vertexShader,i=e.fragmentShader,r=this._getShaderStage(t),a=this._getShaderStage(i),s=this._getShaderCacheForMaterial(e);return s.has(r)===!1&&(s.add(r),r.usedTimes++),s.has(a)===!1&&(s.add(a),a.usedTimes++),this}remove(e){const t=this.materialCache.get(e);for(const i of t)i.usedTimes--,i.usedTimes===0&&this.shaderCache.delete(i.code);return this.materialCache.delete(e),this}getVertexShaderID(e){return this._getShaderStage(e.vertexShader).id}getFragmentShaderID(e){return this._getShaderStage(e.fragmentShader).id}dispose(){this.shaderCache.clear(),this.materialCache.clear()}_getShaderCacheForMaterial(e){const t=this.materialCache;let i=t.get(e);return i===void 0&&(i=new Set,t.set(e,i)),i}_getShaderStage(e){const t=this.shaderCache;let i=t.get(e);return i===void 0&&(i=new om(e),t.set(e,i)),i}}class om{constructor(e){this.id=am++,this.code=e,this.usedTimes=0}}function cm(n,e,t,i,r,a,s){const o=new Hs,c=new sm,l=new Set,d=[],h=r.logarithmicDepthBuffer,f=r.vertexTextures;let m=r.precision;const g={MeshDepthMaterial:"depth",MeshDistanceMaterial:"distanceRGBA",MeshNormalMaterial:"normal",MeshBasicMaterial:"basic",MeshLambertMaterial:"lambert",MeshPhongMaterial:"phong",MeshToonMaterial:"toon",MeshStandardMaterial:"physical",MeshPhysicalMaterial:"physical",MeshMatcapMaterial:"matcap",LineBasicMaterial:"basic",LineDashedMaterial:"dashed",PointsMaterial:"points",ShadowMaterial:"shadow",SpriteMaterial:"sprite"};function _(v){return l.add(v),v===0?"uv":`uv${v}`}function p(v,x,P,U,w){const R=U.fog,z=w.geometry,N=v.isMeshStandardMaterial?U.environment:null,B=(v.isMeshStandardMaterial?t:e).get(v.envMap||N),k=B&&B.mapping===Kr?B.image.height:null,O=g[v.type];v.precision!==null&&(m=r.getMaxPrecision(v.precision),m!==v.precision&&console.warn("THREE.WebGLProgram.getParameters:",v.precision,"not supported, using",m,"instead."));const q=z.morphAttributes.position||z.morphAttributes.normal||z.morphAttributes.color,K=q!==void 0?q.length:0;let le=0;z.morphAttributes.position!==void 0&&(le=1),z.morphAttributes.normal!==void 0&&(le=2),z.morphAttributes.color!==void 0&&(le=3);let De,X,J,ae;if(O){const nt=Zt[O];De=nt.vertexShader,X=nt.fragmentShader}else De=v.vertexShader,X=v.fragmentShader,c.update(v),J=c.getVertexShaderID(v),ae=c.getFragmentShaderID(v);const re=n.getRenderTarget(),ue=n.state.buffers.depth.getReversed(),Pe=w.isInstancedMesh===!0,fe=w.isBatchedMesh===!0,te=!!v.map,se=!!v.matcap,W=!!B,L=!!v.aoMap,Ee=!!v.lightMap,Se=!!v.bumpMap,_e=!!v.normalMap,ve=!!v.displacementMap,Ne=!!v.emissiveMap,Re=!!v.metalnessMap,I=!!v.roughnessMap,S=v.anisotropy>0,j=v.clearcoat>0,ee=v.dispersion>0,ie=v.iridescence>0,Q=v.sheen>0,Ce=v.transmission>0,ge=S&&!!v.anisotropyMap,be=j&&!!v.clearcoatMap,$e=j&&!!v.clearcoatNormalMap,de=j&&!!v.clearcoatRoughnessMap,Te=ie&&!!v.iridescenceMap,ze=ie&&!!v.iridescenceThicknessMap,ke=Q&&!!v.sheenColorMap,we=Q&&!!v.sheenRoughnessMap,Ke=!!v.specularMap,Ge=!!v.specularColorMap,st=!!v.specularIntensityMap,V=Ce&&!!v.transmissionMap,pe=Ce&&!!v.thicknessMap,Z=!!v.gradientMap,ne=!!v.alphaMap,Me=v.alphaTest>0,xe=!!v.alphaHash,Be=!!v.extensions;let dt=Cn;v.toneMapped&&(re===null||re.isXRRenderTarget===!0)&&(dt=n.toneMapping);const yt={shaderID:O,shaderType:v.type,shaderName:v.name,vertexShader:De,fragmentShader:X,defines:v.defines,customVertexShaderID:J,customFragmentShaderID:ae,isRawShaderMaterial:v.isRawShaderMaterial===!0,glslVersion:v.glslVersion,precision:m,batching:fe,batchingColor:fe&&w._colorsTexture!==null,instancing:Pe,instancingColor:Pe&&w.instanceColor!==null,instancingMorph:Pe&&w.morphTexture!==null,supportsVertexTextures:f,outputColorSpace:re===null?n.outputColorSpace:re.isXRRenderTarget===!0?re.texture.colorSpace:Ui,alphaToCoverage:!!v.alphaToCoverage,map:te,matcap:se,envMap:W,envMapMode:W&&B.mapping,envMapCubeUVHeight:k,aoMap:L,lightMap:Ee,bumpMap:Se,normalMap:_e,displacementMap:f&&ve,emissiveMap:Ne,normalMapObjectSpace:_e&&v.normalMapType===Ql,normalMapTangentSpace:_e&&v.normalMapType===jc,metalnessMap:Re,roughnessMap:I,anisotropy:S,anisotropyMap:ge,clearcoat:j,clearcoatMap:be,clearcoatNormalMap:$e,clearcoatRoughnessMap:de,dispersion:ee,iridescence:ie,iridescenceMap:Te,iridescenceThicknessMap:ze,sheen:Q,sheenColorMap:ke,sheenRoughnessMap:we,specularMap:Ke,specularColorMap:Ge,specularIntensityMap:st,transmission:Ce,transmissionMap:V,thicknessMap:pe,gradientMap:Z,opaque:v.transparent===!1&&v.blending===wi&&v.alphaToCoverage===!1,alphaMap:ne,alphaTest:Me,alphaHash:xe,combine:v.combine,mapUv:te&&_(v.map.channel),aoMapUv:L&&_(v.aoMap.channel),lightMapUv:Ee&&_(v.lightMap.channel),bumpMapUv:Se&&_(v.bumpMap.channel),normalMapUv:_e&&_(v.normalMap.channel),displacementMapUv:ve&&_(v.displacementMap.channel),emissiveMapUv:Ne&&_(v.emissiveMap.channel),metalnessMapUv:Re&&_(v.metalnessMap.channel),roughnessMapUv:I&&_(v.roughnessMap.channel),anisotropyMapUv:ge&&_(v.anisotropyMap.channel),clearcoatMapUv:be&&_(v.clearcoatMap.channel),clearcoatNormalMapUv:$e&&_(v.clearcoatNormalMap.channel),clearcoatRoughnessMapUv:de&&_(v.clearcoatRoughnessMap.channel),iridescenceMapUv:Te&&_(v.iridescenceMap.channel),iridescenceThicknessMapUv:ze&&_(v.iridescenceThicknessMap.channel),sheenColorMapUv:ke&&_(v.sheenColorMap.channel),sheenRoughnessMapUv:we&&_(v.sheenRoughnessMap.channel),specularMapUv:Ke&&_(v.specularMap.channel),specularColorMapUv:Ge&&_(v.specularColorMap.channel),specularIntensityMapUv:st&&_(v.specularIntensityMap.channel),transmissionMapUv:V&&_(v.transmissionMap.channel),thicknessMapUv:pe&&_(v.thicknessMap.channel),alphaMapUv:ne&&_(v.alphaMap.channel),vertexTangents:!!z.attributes.tangent&&(_e||S),vertexColors:v.vertexColors,vertexAlphas:v.vertexColors===!0&&!!z.attributes.color&&z.attributes.color.itemSize===4,pointsUvs:w.isPoints===!0&&!!z.attributes.uv&&(te||ne),fog:!!R,useFog:v.fog===!0,fogExp2:!!R&&R.isFogExp2,flatShading:v.flatShading===!0,sizeAttenuation:v.sizeAttenuation===!0,logarithmicDepthBuffer:h,reverseDepthBuffer:ue,skinning:w.isSkinnedMesh===!0,morphTargets:z.morphAttributes.position!==void 0,morphNormals:z.morphAttributes.normal!==void 0,morphColors:z.morphAttributes.color!==void 0,morphTargetsCount:K,morphTextureStride:le,numDirLights:x.directional.length,numPointLights:x.point.length,numSpotLights:x.spot.length,numSpotLightMaps:x.spotLightMap.length,numRectAreaLights:x.rectArea.length,numHemiLights:x.hemi.length,numDirLightShadows:x.directionalShadowMap.length,numPointLightShadows:x.pointShadowMap.length,numSpotLightShadows:x.spotShadowMap.length,numSpotLightShadowsWithMaps:x.numSpotLightShadowsWithMaps,numLightProbes:x.numLightProbes,numClippingPlanes:s.numPlanes,numClipIntersection:s.numIntersection,dithering:v.dithering,shadowMapEnabled:n.shadowMap.enabled&&P.length>0,shadowMapType:n.shadowMap.type,toneMapping:dt,decodeVideoTexture:te&&v.map.isVideoTexture===!0&&Je.getTransfer(v.map.colorSpace)===it,decodeVideoTextureEmissive:Ne&&v.emissiveMap.isVideoTexture===!0&&Je.getTransfer(v.emissiveMap.colorSpace)===it,premultipliedAlpha:v.premultipliedAlpha,doubleSided:v.side===St,flipSided:v.side===Ct,useDepthPacking:v.depthPacking>=0,depthPacking:v.depthPacking||0,index0AttributeName:v.index0AttributeName,extensionClipCullDistance:Be&&v.extensions.clipCullDistance===!0&&i.has("WEBGL_clip_cull_distance"),extensionMultiDraw:(Be&&v.extensions.multiDraw===!0||fe)&&i.has("WEBGL_multi_draw"),rendererExtensionParallelShaderCompile:i.has("KHR_parallel_shader_compile"),customProgramCacheKey:v.customProgramCacheKey()};return yt.vertexUv1s=l.has(1),yt.vertexUv2s=l.has(2),yt.vertexUv3s=l.has(3),l.clear(),yt}function u(v){const x=[];if(v.shaderID?x.push(v.shaderID):(x.push(v.customVertexShaderID),x.push(v.customFragmentShaderID)),v.defines!==void 0)for(const P in v.defines)x.push(P),x.push(v.defines[P]);return v.isRawShaderMaterial===!1&&(E(x,v),y(x,v),x.push(n.outputColorSpace)),x.push(v.customProgramCacheKey),x.join()}function E(v,x){v.push(x.precision),v.push(x.outputColorSpace),v.push(x.envMapMode),v.push(x.envMapCubeUVHeight),v.push(x.mapUv),v.push(x.alphaMapUv),v.push(x.lightMapUv),v.push(x.aoMapUv),v.push(x.bumpMapUv),v.push(x.normalMapUv),v.push(x.displacementMapUv),v.push(x.emissiveMapUv),v.push(x.metalnessMapUv),v.push(x.roughnessMapUv),v.push(x.anisotropyMapUv),v.push(x.clearcoatMapUv),v.push(x.clearcoatNormalMapUv),v.push(x.clearcoatRoughnessMapUv),v.push(x.iridescenceMapUv),v.push(x.iridescenceThicknessMapUv),v.push(x.sheenColorMapUv),v.push(x.sheenRoughnessMapUv),v.push(x.specularMapUv),v.push(x.specularColorMapUv),v.push(x.specularIntensityMapUv),v.push(x.transmissionMapUv),v.push(x.thicknessMapUv),v.push(x.combine),v.push(x.fogExp2),v.push(x.sizeAttenuation),v.push(x.morphTargetsCount),v.push(x.morphAttributeCount),v.push(x.numDirLights),v.push(x.numPointLights),v.push(x.numSpotLights),v.push(x.numSpotLightMaps),v.push(x.numHemiLights),v.push(x.numRectAreaLights),v.push(x.numDirLightShadows),v.push(x.numPointLightShadows),v.push(x.numSpotLightShadows),v.push(x.numSpotLightShadowsWithMaps),v.push(x.numLightProbes),v.push(x.shadowMapType),v.push(x.toneMapping),v.push(x.numClippingPlanes),v.push(x.numClipIntersection),v.push(x.depthPacking)}function y(v,x){o.disableAll(),x.supportsVertexTextures&&o.enable(0),x.instancing&&o.enable(1),x.instancingColor&&o.enable(2),x.instancingMorph&&o.enable(3),x.matcap&&o.enable(4),x.envMap&&o.enable(5),x.normalMapObjectSpace&&o.enable(6),x.normalMapTangentSpace&&o.enable(7),x.clearcoat&&o.enable(8),x.iridescence&&o.enable(9),x.alphaTest&&o.enable(10),x.vertexColors&&o.enable(11),x.vertexAlphas&&o.enable(12),x.vertexUv1s&&o.enable(13),x.vertexUv2s&&o.enable(14),x.vertexUv3s&&o.enable(15),x.vertexTangents&&o.enable(16),x.anisotropy&&o.enable(17),x.alphaHash&&o.enable(18),x.batching&&o.enable(19),x.dispersion&&o.enable(20),x.batchingColor&&o.enable(21),v.push(o.mask),o.disableAll(),x.fog&&o.enable(0),x.useFog&&o.enable(1),x.flatShading&&o.enable(2),x.logarithmicDepthBuffer&&o.enable(3),x.reverseDepthBuffer&&o.enable(4),x.skinning&&o.enable(5),x.morphTargets&&o.enable(6),x.morphNormals&&o.enable(7),x.morphColors&&o.enable(8),x.premultipliedAlpha&&o.enable(9),x.shadowMapEnabled&&o.enable(10),x.doubleSided&&o.enable(11),x.flipSided&&o.enable(12),x.useDepthPacking&&o.enable(13),x.dithering&&o.enable(14),x.transmission&&o.enable(15),x.sheen&&o.enable(16),x.opaque&&o.enable(17),x.pointsUvs&&o.enable(18),x.decodeVideoTexture&&o.enable(19),x.decodeVideoTextureEmissive&&o.enable(20),x.alphaToCoverage&&o.enable(21),v.push(o.mask)}function M(v){const x=g[v.type];let P;if(x){const U=Zt[x];P=Pu.clone(U.uniforms)}else P=v.uniforms;return P}function D(v,x){let P;for(let U=0,w=d.length;U<w;U++){const R=d[U];if(R.cacheKey===x){P=R,++P.usedTimes;break}}return P===void 0&&(P=new rm(n,x,v,a),d.push(P)),P}function A(v){if(--v.usedTimes===0){const x=d.indexOf(v);d[x]=d[d.length-1],d.pop(),v.destroy()}}function b(v){c.remove(v)}function C(){c.dispose()}return{getParameters:p,getProgramCacheKey:u,getUniforms:M,acquireProgram:D,releaseProgram:A,releaseShaderCache:b,programs:d,dispose:C}}function lm(){let n=new WeakMap;function e(s){return n.has(s)}function t(s){let o=n.get(s);return o===void 0&&(o={},n.set(s,o)),o}function i(s){n.delete(s)}function r(s,o,c){n.get(s)[o]=c}function a(){n=new WeakMap}return{has:e,get:t,remove:i,update:r,dispose:a}}function um(n,e){return n.groupOrder!==e.groupOrder?n.groupOrder-e.groupOrder:n.renderOrder!==e.renderOrder?n.renderOrder-e.renderOrder:n.material.id!==e.material.id?n.material.id-e.material.id:n.z!==e.z?n.z-e.z:n.id-e.id}function hc(n,e){return n.groupOrder!==e.groupOrder?n.groupOrder-e.groupOrder:n.renderOrder!==e.renderOrder?n.renderOrder-e.renderOrder:n.z!==e.z?e.z-n.z:n.id-e.id}function fc(){const n=[];let e=0;const t=[],i=[],r=[];function a(){e=0,t.length=0,i.length=0,r.length=0}function s(h,f,m,g,_,p){let u=n[e];return u===void 0?(u={id:h.id,object:h,geometry:f,material:m,groupOrder:g,renderOrder:h.renderOrder,z:_,group:p},n[e]=u):(u.id=h.id,u.object=h,u.geometry=f,u.material=m,u.groupOrder=g,u.renderOrder=h.renderOrder,u.z=_,u.group=p),e++,u}function o(h,f,m,g,_,p){const u=s(h,f,m,g,_,p);m.transmission>0?i.push(u):m.transparent===!0?r.push(u):t.push(u)}function c(h,f,m,g,_,p){const u=s(h,f,m,g,_,p);m.transmission>0?i.unshift(u):m.transparent===!0?r.unshift(u):t.unshift(u)}function l(h,f){t.length>1&&t.sort(h||um),i.length>1&&i.sort(f||hc),r.length>1&&r.sort(f||hc)}function d(){for(let h=e,f=n.length;h<f;h++){const m=n[h];if(m.id===null)break;m.id=null,m.object=null,m.geometry=null,m.material=null,m.group=null}}return{opaque:t,transmissive:i,transparent:r,init:a,push:o,unshift:c,finish:d,sort:l}}function dm(){let n=new WeakMap;function e(i,r){const a=n.get(i);let s;return a===void 0?(s=new fc,n.set(i,[s])):r>=a.length?(s=new fc,a.push(s)):s=a[r],s}function t(){n=new WeakMap}return{get:e,dispose:t}}function hm(){const n={};return{get:function(e){if(n[e.id]!==void 0)return n[e.id];let t;switch(e.type){case"DirectionalLight":t={direction:new F,color:new oe};break;case"SpotLight":t={position:new F,direction:new F,color:new oe,distance:0,coneCos:0,penumbraCos:0,decay:0};break;case"PointLight":t={position:new F,color:new oe,distance:0,decay:0};break;case"HemisphereLight":t={direction:new F,skyColor:new oe,groundColor:new oe};break;case"RectAreaLight":t={color:new oe,position:new F,halfWidth:new F,halfHeight:new F};break}return n[e.id]=t,t}}}function fm(){const n={};return{get:function(e){if(n[e.id]!==void 0)return n[e.id];let t;switch(e.type){case"DirectionalLight":t={shadowIntensity:1,shadowBias:0,shadowNormalBias:0,shadowRadius:1,shadowMapSize:new We};break;case"SpotLight":t={shadowIntensity:1,shadowBias:0,shadowNormalBias:0,shadowRadius:1,shadowMapSize:new We};break;case"PointLight":t={shadowIntensity:1,shadowBias:0,shadowNormalBias:0,shadowRadius:1,shadowMapSize:new We,shadowCameraNear:1,shadowCameraFar:1e3};break}return n[e.id]=t,t}}}let pm=0;function mm(n,e){return(e.castShadow?2:0)-(n.castShadow?2:0)+(e.map?1:0)-(n.map?1:0)}function gm(n){const e=new hm,t=fm(),i={version:0,hash:{directionalLength:-1,pointLength:-1,spotLength:-1,rectAreaLength:-1,hemiLength:-1,numDirectionalShadows:-1,numPointShadows:-1,numSpotShadows:-1,numSpotMaps:-1,numLightProbes:-1},ambient:[0,0,0],probe:[],directional:[],directionalShadow:[],directionalShadowMap:[],directionalShadowMatrix:[],spot:[],spotLightMap:[],spotShadow:[],spotShadowMap:[],spotLightMatrix:[],rectArea:[],rectAreaLTC1:null,rectAreaLTC2:null,point:[],pointShadow:[],pointShadowMap:[],pointShadowMatrix:[],hemi:[],numSpotLightShadowsWithMaps:0,numLightProbes:0};for(let l=0;l<9;l++)i.probe.push(new F);const r=new F,a=new at,s=new at;function o(l){let d=0,h=0,f=0;for(let v=0;v<9;v++)i.probe[v].set(0,0,0);let m=0,g=0,_=0,p=0,u=0,E=0,y=0,M=0,D=0,A=0,b=0;l.sort(mm);for(let v=0,x=l.length;v<x;v++){const P=l[v],U=P.color,w=P.intensity,R=P.distance,z=P.shadow&&P.shadow.map?P.shadow.map.texture:null;if(P.isAmbientLight)d+=U.r*w,h+=U.g*w,f+=U.b*w;else if(P.isLightProbe){for(let N=0;N<9;N++)i.probe[N].addScaledVector(P.sh.coefficients[N],w);b++}else if(P.isDirectionalLight){const N=e.get(P);if(N.color.copy(P.color).multiplyScalar(P.intensity),P.castShadow){const B=P.shadow,k=t.get(P);k.shadowIntensity=B.intensity,k.shadowBias=B.bias,k.shadowNormalBias=B.normalBias,k.shadowRadius=B.radius,k.shadowMapSize=B.mapSize,i.directionalShadow[m]=k,i.directionalShadowMap[m]=z,i.directionalShadowMatrix[m]=P.shadow.matrix,E++}i.directional[m]=N,m++}else if(P.isSpotLight){const N=e.get(P);N.position.setFromMatrixPosition(P.matrixWorld),N.color.copy(U).multiplyScalar(w),N.distance=R,N.coneCos=Math.cos(P.angle),N.penumbraCos=Math.cos(P.angle*(1-P.penumbra)),N.decay=P.decay,i.spot[_]=N;const B=P.shadow;if(P.map&&(i.spotLightMap[D]=P.map,D++,B.updateMatrices(P),P.castShadow&&A++),i.spotLightMatrix[_]=B.matrix,P.castShadow){const k=t.get(P);k.shadowIntensity=B.intensity,k.shadowBias=B.bias,k.shadowNormalBias=B.normalBias,k.shadowRadius=B.radius,k.shadowMapSize=B.mapSize,i.spotShadow[_]=k,i.spotShadowMap[_]=z,M++}_++}else if(P.isRectAreaLight){const N=e.get(P);N.color.copy(U).multiplyScalar(w),N.halfWidth.set(P.width*.5,0,0),N.halfHeight.set(0,P.height*.5,0),i.rectArea[p]=N,p++}else if(P.isPointLight){const N=e.get(P);if(N.color.copy(P.color).multiplyScalar(P.intensity),N.distance=P.distance,N.decay=P.decay,P.castShadow){const B=P.shadow,k=t.get(P);k.shadowIntensity=B.intensity,k.shadowBias=B.bias,k.shadowNormalBias=B.normalBias,k.shadowRadius=B.radius,k.shadowMapSize=B.mapSize,k.shadowCameraNear=B.camera.near,k.shadowCameraFar=B.camera.far,i.pointShadow[g]=k,i.pointShadowMap[g]=z,i.pointShadowMatrix[g]=P.shadow.matrix,y++}i.point[g]=N,g++}else if(P.isHemisphereLight){const N=e.get(P);N.skyColor.copy(P.color).multiplyScalar(w),N.groundColor.copy(P.groundColor).multiplyScalar(w),i.hemi[u]=N,u++}}p>0&&(n.has("OES_texture_float_linear")===!0?(i.rectAreaLTC1=he.LTC_FLOAT_1,i.rectAreaLTC2=he.LTC_FLOAT_2):(i.rectAreaLTC1=he.LTC_HALF_1,i.rectAreaLTC2=he.LTC_HALF_2)),i.ambient[0]=d,i.ambient[1]=h,i.ambient[2]=f;const C=i.hash;(C.directionalLength!==m||C.pointLength!==g||C.spotLength!==_||C.rectAreaLength!==p||C.hemiLength!==u||C.numDirectionalShadows!==E||C.numPointShadows!==y||C.numSpotShadows!==M||C.numSpotMaps!==D||C.numLightProbes!==b)&&(i.directional.length=m,i.spot.length=_,i.rectArea.length=p,i.point.length=g,i.hemi.length=u,i.directionalShadow.length=E,i.directionalShadowMap.length=E,i.pointShadow.length=y,i.pointShadowMap.length=y,i.spotShadow.length=M,i.spotShadowMap.length=M,i.directionalShadowMatrix.length=E,i.pointShadowMatrix.length=y,i.spotLightMatrix.length=M+D-A,i.spotLightMap.length=D,i.numSpotLightShadowsWithMaps=A,i.numLightProbes=b,C.directionalLength=m,C.pointLength=g,C.spotLength=_,C.rectAreaLength=p,C.hemiLength=u,C.numDirectionalShadows=E,C.numPointShadows=y,C.numSpotShadows=M,C.numSpotMaps=D,C.numLightProbes=b,i.version=pm++)}function c(l,d){let h=0,f=0,m=0,g=0,_=0;const p=d.matrixWorldInverse;for(let u=0,E=l.length;u<E;u++){const y=l[u];if(y.isDirectionalLight){const M=i.directional[h];M.direction.setFromMatrixPosition(y.matrixWorld),r.setFromMatrixPosition(y.target.matrixWorld),M.direction.sub(r),M.direction.transformDirection(p),h++}else if(y.isSpotLight){const M=i.spot[m];M.position.setFromMatrixPosition(y.matrixWorld),M.position.applyMatrix4(p),M.direction.setFromMatrixPosition(y.matrixWorld),r.setFromMatrixPosition(y.target.matrixWorld),M.direction.sub(r),M.direction.transformDirection(p),m++}else if(y.isRectAreaLight){const M=i.rectArea[g];M.position.setFromMatrixPosition(y.matrixWorld),M.position.applyMatrix4(p),s.identity(),a.copy(y.matrixWorld),a.premultiply(p),s.extractRotation(a),M.halfWidth.set(y.width*.5,0,0),M.halfHeight.set(0,y.height*.5,0),M.halfWidth.applyMatrix4(s),M.halfHeight.applyMatrix4(s),g++}else if(y.isPointLight){const M=i.point[f];M.position.setFromMatrixPosition(y.matrixWorld),M.position.applyMatrix4(p),f++}else if(y.isHemisphereLight){const M=i.hemi[_];M.direction.setFromMatrixPosition(y.matrixWorld),M.direction.transformDirection(p),_++}}}return{setup:o,setupView:c,state:i}}function pc(n){const e=new gm(n),t=[],i=[];function r(d){l.camera=d,t.length=0,i.length=0}function a(d){t.push(d)}function s(d){i.push(d)}function o(){e.setup(t)}function c(d){e.setupView(t,d)}const l={lightsArray:t,shadowsArray:i,camera:null,lights:e,transmissionRenderTarget:{}};return{init:r,state:l,setupLights:o,setupLightsView:c,pushLight:a,pushShadow:s}}function _m(n){let e=new WeakMap;function t(r,a=0){const s=e.get(r);let o;return s===void 0?(o=new pc(n),e.set(r,[o])):a>=s.length?(o=new pc(n),s.push(o)):o=s[a],o}function i(){e=new WeakMap}return{get:t,dispose:i}}const vm=`void main() {
	gl_Position = vec4( position, 1.0 );
}`,xm=`uniform sampler2D shadow_pass;
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
}`;function Mm(n,e,t){let i=new js;const r=new We,a=new We,s=new rt,o=new Vu({depthPacking:Jl}),c=new Gu,l={},d=t.maxTextureSize,h={[Pn]:Ct,[Ct]:Pn,[St]:St},f=new Dn({defines:{VSM_SAMPLES:8},uniforms:{shadow_pass:{value:null},resolution:{value:new We},radius:{value:4}},vertexShader:vm,fragmentShader:xm}),m=f.clone();m.defines.HORIZONTAL_PASS=1;const g=new Xe;g.setAttribute("position",new en(new Float32Array([-1,-1,.5,3,-1,.5,-1,3,.5]),3));const _=new Le(g,f),p=this;this.enabled=!1,this.autoUpdate=!0,this.needsUpdate=!1,this.type=Dc;let u=this.type;this.render=function(A,b,C){if(p.enabled===!1||p.autoUpdate===!1&&p.needsUpdate===!1||A.length===0)return;const v=n.getRenderTarget(),x=n.getActiveCubeFace(),P=n.getActiveMipmapLevel(),U=n.state;U.setBlending(Rn),U.buffers.color.setClear(1,1,1,1),U.buffers.depth.setTest(!0),U.setScissorTest(!1);const w=u!==un&&this.type===un,R=u===un&&this.type!==un;for(let z=0,N=A.length;z<N;z++){const B=A[z],k=B.shadow;if(k===void 0){console.warn("THREE.WebGLShadowMap:",B,"has no shadow.");continue}if(k.autoUpdate===!1&&k.needsUpdate===!1)continue;r.copy(k.mapSize);const O=k.getFrameExtents();if(r.multiply(O),a.copy(k.mapSize),(r.x>d||r.y>d)&&(r.x>d&&(a.x=Math.floor(d/O.x),r.x=a.x*O.x,k.mapSize.x=a.x),r.y>d&&(a.y=Math.floor(d/O.y),r.y=a.y*O.y,k.mapSize.y=a.y)),k.map===null||w===!0||R===!0){const K=this.type!==un?{minFilter:Ft,magFilter:Ft}:{};k.map!==null&&k.map.dispose(),k.map=new ti(r.x,r.y,K),k.map.texture.name=B.name+".shadowMap",k.camera.updateProjectionMatrix()}n.setRenderTarget(k.map),n.clear();const q=k.getViewportCount();for(let K=0;K<q;K++){const le=k.getViewport(K);s.set(a.x*le.x,a.y*le.y,a.x*le.z,a.y*le.w),U.viewport(s),k.updateMatrices(B,K),i=k.getFrustum(),M(b,C,k.camera,B,this.type)}k.isPointLightShadow!==!0&&this.type===un&&E(k,C),k.needsUpdate=!1}u=this.type,p.needsUpdate=!1,n.setRenderTarget(v,x,P)};function E(A,b){const C=e.update(_);f.defines.VSM_SAMPLES!==A.blurSamples&&(f.defines.VSM_SAMPLES=A.blurSamples,m.defines.VSM_SAMPLES=A.blurSamples,f.needsUpdate=!0,m.needsUpdate=!0),A.mapPass===null&&(A.mapPass=new ti(r.x,r.y)),f.uniforms.shadow_pass.value=A.map.texture,f.uniforms.resolution.value=A.mapSize,f.uniforms.radius.value=A.radius,n.setRenderTarget(A.mapPass),n.clear(),n.renderBufferDirect(b,null,C,f,_,null),m.uniforms.shadow_pass.value=A.mapPass.texture,m.uniforms.resolution.value=A.mapSize,m.uniforms.radius.value=A.radius,n.setRenderTarget(A.map),n.clear(),n.renderBufferDirect(b,null,C,m,_,null)}function y(A,b,C,v){let x=null;const P=C.isPointLight===!0?A.customDistanceMaterial:A.customDepthMaterial;if(P!==void 0)x=P;else if(x=C.isPointLight===!0?c:o,n.localClippingEnabled&&b.clipShadows===!0&&Array.isArray(b.clippingPlanes)&&b.clippingPlanes.length!==0||b.displacementMap&&b.displacementScale!==0||b.alphaMap&&b.alphaTest>0||b.map&&b.alphaTest>0){const U=x.uuid,w=b.uuid;let R=l[U];R===void 0&&(R={},l[U]=R);let z=R[w];z===void 0&&(z=x.clone(),R[w]=z,b.addEventListener("dispose",D)),x=z}if(x.visible=b.visible,x.wireframe=b.wireframe,v===un?x.side=b.shadowSide!==null?b.shadowSide:b.side:x.side=b.shadowSide!==null?b.shadowSide:h[b.side],x.alphaMap=b.alphaMap,x.alphaTest=b.alphaTest,x.map=b.map,x.clipShadows=b.clipShadows,x.clippingPlanes=b.clippingPlanes,x.clipIntersection=b.clipIntersection,x.displacementMap=b.displacementMap,x.displacementScale=b.displacementScale,x.displacementBias=b.displacementBias,x.wireframeLinewidth=b.wireframeLinewidth,x.linewidth=b.linewidth,C.isPointLight===!0&&x.isMeshDistanceMaterial===!0){const U=n.properties.get(x);U.light=C}return x}function M(A,b,C,v,x){if(A.visible===!1)return;if(A.layers.test(b.layers)&&(A.isMesh||A.isLine||A.isPoints)&&(A.castShadow||A.receiveShadow&&x===un)&&(!A.frustumCulled||i.intersectsObject(A))){A.modelViewMatrix.multiplyMatrices(C.matrixWorldInverse,A.matrixWorld);const w=e.update(A),R=A.material;if(Array.isArray(R)){const z=w.groups;for(let N=0,B=z.length;N<B;N++){const k=z[N],O=R[k.materialIndex];if(O&&O.visible){const q=y(A,O,v,x);A.onBeforeShadow(n,A,b,C,w,q,k),n.renderBufferDirect(C,null,w,q,A,k),A.onAfterShadow(n,A,b,C,w,q,k)}}}else if(R.visible){const z=y(A,R,v,x);A.onBeforeShadow(n,A,b,C,w,z,null),n.renderBufferDirect(C,null,w,z,A,null),A.onAfterShadow(n,A,b,C,w,z,null)}}const U=A.children;for(let w=0,R=U.length;w<R;w++)M(U[w],b,C,v,x)}function D(A){A.target.removeEventListener("dispose",D);for(const C in l){const v=l[C],x=A.target.uuid;x in v&&(v[x].dispose(),delete v[x])}}}const Sm={[Va]:Ga,[Ha]:Xa,[ja]:qa,[Ci]:Wa,[Ga]:Va,[Xa]:Ha,[qa]:ja,[Wa]:Ci};function Em(n,e){function t(){let V=!1;const pe=new rt;let Z=null;const ne=new rt(0,0,0,0);return{setMask:function(Me){Z!==Me&&!V&&(n.colorMask(Me,Me,Me,Me),Z=Me)},setLocked:function(Me){V=Me},setClear:function(Me,xe,Be,dt,yt){yt===!0&&(Me*=dt,xe*=dt,Be*=dt),pe.set(Me,xe,Be,dt),ne.equals(pe)===!1&&(n.clearColor(Me,xe,Be,dt),ne.copy(pe))},reset:function(){V=!1,Z=null,ne.set(-1,0,0,0)}}}function i(){let V=!1,pe=!1,Z=null,ne=null,Me=null;return{setReversed:function(xe){if(pe!==xe){const Be=e.get("EXT_clip_control");pe?Be.clipControlEXT(Be.LOWER_LEFT_EXT,Be.ZERO_TO_ONE_EXT):Be.clipControlEXT(Be.LOWER_LEFT_EXT,Be.NEGATIVE_ONE_TO_ONE_EXT);const dt=Me;Me=null,this.setClear(dt)}pe=xe},getReversed:function(){return pe},setTest:function(xe){xe?re(n.DEPTH_TEST):ue(n.DEPTH_TEST)},setMask:function(xe){Z!==xe&&!V&&(n.depthMask(xe),Z=xe)},setFunc:function(xe){if(pe&&(xe=Sm[xe]),ne!==xe){switch(xe){case Va:n.depthFunc(n.NEVER);break;case Ga:n.depthFunc(n.ALWAYS);break;case Ha:n.depthFunc(n.LESS);break;case Ci:n.depthFunc(n.LEQUAL);break;case ja:n.depthFunc(n.EQUAL);break;case Wa:n.depthFunc(n.GEQUAL);break;case Xa:n.depthFunc(n.GREATER);break;case qa:n.depthFunc(n.NOTEQUAL);break;default:n.depthFunc(n.LEQUAL)}ne=xe}},setLocked:function(xe){V=xe},setClear:function(xe){Me!==xe&&(pe&&(xe=1-xe),n.clearDepth(xe),Me=xe)},reset:function(){V=!1,Z=null,ne=null,Me=null,pe=!1}}}function r(){let V=!1,pe=null,Z=null,ne=null,Me=null,xe=null,Be=null,dt=null,yt=null;return{setTest:function(nt){V||(nt?re(n.STENCIL_TEST):ue(n.STENCIL_TEST))},setMask:function(nt){pe!==nt&&!V&&(n.stencilMask(nt),pe=nt)},setFunc:function(nt,jt,tn){(Z!==nt||ne!==jt||Me!==tn)&&(n.stencilFunc(nt,jt,tn),Z=nt,ne=jt,Me=tn)},setOp:function(nt,jt,tn){(xe!==nt||Be!==jt||dt!==tn)&&(n.stencilOp(nt,jt,tn),xe=nt,Be=jt,dt=tn)},setLocked:function(nt){V=nt},setClear:function(nt){yt!==nt&&(n.clearStencil(nt),yt=nt)},reset:function(){V=!1,pe=null,Z=null,ne=null,Me=null,xe=null,Be=null,dt=null,yt=null}}}const a=new t,s=new i,o=new r,c=new WeakMap,l=new WeakMap;let d={},h={},f=new WeakMap,m=[],g=null,_=!1,p=null,u=null,E=null,y=null,M=null,D=null,A=null,b=new oe(0,0,0),C=0,v=!1,x=null,P=null,U=null,w=null,R=null;const z=n.getParameter(n.MAX_COMBINED_TEXTURE_IMAGE_UNITS);let N=!1,B=0;const k=n.getParameter(n.VERSION);k.indexOf("WebGL")!==-1?(B=parseFloat(/^WebGL (\d)/.exec(k)[1]),N=B>=1):k.indexOf("OpenGL ES")!==-1&&(B=parseFloat(/^OpenGL ES (\d)/.exec(k)[1]),N=B>=2);let O=null,q={};const K=n.getParameter(n.SCISSOR_BOX),le=n.getParameter(n.VIEWPORT),De=new rt().fromArray(K),X=new rt().fromArray(le);function J(V,pe,Z,ne){const Me=new Uint8Array(4),xe=n.createTexture();n.bindTexture(V,xe),n.texParameteri(V,n.TEXTURE_MIN_FILTER,n.NEAREST),n.texParameteri(V,n.TEXTURE_MAG_FILTER,n.NEAREST);for(let Be=0;Be<Z;Be++)V===n.TEXTURE_3D||V===n.TEXTURE_2D_ARRAY?n.texImage3D(pe,0,n.RGBA,1,1,ne,0,n.RGBA,n.UNSIGNED_BYTE,Me):n.texImage2D(pe+Be,0,n.RGBA,1,1,0,n.RGBA,n.UNSIGNED_BYTE,Me);return xe}const ae={};ae[n.TEXTURE_2D]=J(n.TEXTURE_2D,n.TEXTURE_2D,1),ae[n.TEXTURE_CUBE_MAP]=J(n.TEXTURE_CUBE_MAP,n.TEXTURE_CUBE_MAP_POSITIVE_X,6),ae[n.TEXTURE_2D_ARRAY]=J(n.TEXTURE_2D_ARRAY,n.TEXTURE_2D_ARRAY,1,1),ae[n.TEXTURE_3D]=J(n.TEXTURE_3D,n.TEXTURE_3D,1,1),a.setClear(0,0,0,1),s.setClear(1),o.setClear(0),re(n.DEPTH_TEST),s.setFunc(Ci),Se(!1),_e(lo),re(n.CULL_FACE),L(Rn);function re(V){d[V]!==!0&&(n.enable(V),d[V]=!0)}function ue(V){d[V]!==!1&&(n.disable(V),d[V]=!1)}function Pe(V,pe){return h[V]!==pe?(n.bindFramebuffer(V,pe),h[V]=pe,V===n.DRAW_FRAMEBUFFER&&(h[n.FRAMEBUFFER]=pe),V===n.FRAMEBUFFER&&(h[n.DRAW_FRAMEBUFFER]=pe),!0):!1}function fe(V,pe){let Z=m,ne=!1;if(V){Z=f.get(pe),Z===void 0&&(Z=[],f.set(pe,Z));const Me=V.textures;if(Z.length!==Me.length||Z[0]!==n.COLOR_ATTACHMENT0){for(let xe=0,Be=Me.length;xe<Be;xe++)Z[xe]=n.COLOR_ATTACHMENT0+xe;Z.length=Me.length,ne=!0}}else Z[0]!==n.BACK&&(Z[0]=n.BACK,ne=!0);ne&&n.drawBuffers(Z)}function te(V){return g!==V?(n.useProgram(V),g=V,!0):!1}const se={[Xn]:n.FUNC_ADD,[bl]:n.FUNC_SUBTRACT,[Tl]:n.FUNC_REVERSE_SUBTRACT};se[wl]=n.MIN,se[Al]=n.MAX;const W={[Rl]:n.ZERO,[Cl]:n.ONE,[Pl]:n.SRC_COLOR,[Oa]:n.SRC_ALPHA,[Nl]:n.SRC_ALPHA_SATURATE,[Ul]:n.DST_COLOR,[Ll]:n.DST_ALPHA,[Dl]:n.ONE_MINUS_SRC_COLOR,[Ba]:n.ONE_MINUS_SRC_ALPHA,[zl]:n.ONE_MINUS_DST_COLOR,[Il]:n.ONE_MINUS_DST_ALPHA,[kl]:n.CONSTANT_COLOR,[Fl]:n.ONE_MINUS_CONSTANT_COLOR,[Ol]:n.CONSTANT_ALPHA,[Bl]:n.ONE_MINUS_CONSTANT_ALPHA};function L(V,pe,Z,ne,Me,xe,Be,dt,yt,nt){if(V===Rn){_===!0&&(ue(n.BLEND),_=!1);return}if(_===!1&&(re(n.BLEND),_=!0),V!==yl){if(V!==p||nt!==v){if((u!==Xn||M!==Xn)&&(n.blendEquation(n.FUNC_ADD),u=Xn,M=Xn),nt)switch(V){case wi:n.blendFuncSeparate(n.ONE,n.ONE_MINUS_SRC_ALPHA,n.ONE,n.ONE_MINUS_SRC_ALPHA);break;case uo:n.blendFunc(n.ONE,n.ONE);break;case ho:n.blendFuncSeparate(n.ZERO,n.ONE_MINUS_SRC_COLOR,n.ZERO,n.ONE);break;case fo:n.blendFuncSeparate(n.ZERO,n.SRC_COLOR,n.ZERO,n.SRC_ALPHA);break;default:console.error("THREE.WebGLState: Invalid blending: ",V);break}else switch(V){case wi:n.blendFuncSeparate(n.SRC_ALPHA,n.ONE_MINUS_SRC_ALPHA,n.ONE,n.ONE_MINUS_SRC_ALPHA);break;case uo:n.blendFunc(n.SRC_ALPHA,n.ONE);break;case ho:n.blendFuncSeparate(n.ZERO,n.ONE_MINUS_SRC_COLOR,n.ZERO,n.ONE);break;case fo:n.blendFunc(n.ZERO,n.SRC_COLOR);break;default:console.error("THREE.WebGLState: Invalid blending: ",V);break}E=null,y=null,D=null,A=null,b.set(0,0,0),C=0,p=V,v=nt}return}Me=Me||pe,xe=xe||Z,Be=Be||ne,(pe!==u||Me!==M)&&(n.blendEquationSeparate(se[pe],se[Me]),u=pe,M=Me),(Z!==E||ne!==y||xe!==D||Be!==A)&&(n.blendFuncSeparate(W[Z],W[ne],W[xe],W[Be]),E=Z,y=ne,D=xe,A=Be),(dt.equals(b)===!1||yt!==C)&&(n.blendColor(dt.r,dt.g,dt.b,yt),b.copy(dt),C=yt),p=V,v=!1}function Ee(V,pe){V.side===St?ue(n.CULL_FACE):re(n.CULL_FACE);let Z=V.side===Ct;pe&&(Z=!Z),Se(Z),V.blending===wi&&V.transparent===!1?L(Rn):L(V.blending,V.blendEquation,V.blendSrc,V.blendDst,V.blendEquationAlpha,V.blendSrcAlpha,V.blendDstAlpha,V.blendColor,V.blendAlpha,V.premultipliedAlpha),s.setFunc(V.depthFunc),s.setTest(V.depthTest),s.setMask(V.depthWrite),a.setMask(V.colorWrite);const ne=V.stencilWrite;o.setTest(ne),ne&&(o.setMask(V.stencilWriteMask),o.setFunc(V.stencilFunc,V.stencilRef,V.stencilFuncMask),o.setOp(V.stencilFail,V.stencilZFail,V.stencilZPass)),Ne(V.polygonOffset,V.polygonOffsetFactor,V.polygonOffsetUnits),V.alphaToCoverage===!0?re(n.SAMPLE_ALPHA_TO_COVERAGE):ue(n.SAMPLE_ALPHA_TO_COVERAGE)}function Se(V){x!==V&&(V?n.frontFace(n.CW):n.frontFace(n.CCW),x=V)}function _e(V){V!==Ml?(re(n.CULL_FACE),V!==P&&(V===lo?n.cullFace(n.BACK):V===Sl?n.cullFace(n.FRONT):n.cullFace(n.FRONT_AND_BACK))):ue(n.CULL_FACE),P=V}function ve(V){V!==U&&(N&&n.lineWidth(V),U=V)}function Ne(V,pe,Z){V?(re(n.POLYGON_OFFSET_FILL),(w!==pe||R!==Z)&&(n.polygonOffset(pe,Z),w=pe,R=Z)):ue(n.POLYGON_OFFSET_FILL)}function Re(V){V?re(n.SCISSOR_TEST):ue(n.SCISSOR_TEST)}function I(V){V===void 0&&(V=n.TEXTURE0+z-1),O!==V&&(n.activeTexture(V),O=V)}function S(V,pe,Z){Z===void 0&&(O===null?Z=n.TEXTURE0+z-1:Z=O);let ne=q[Z];ne===void 0&&(ne={type:void 0,texture:void 0},q[Z]=ne),(ne.type!==V||ne.texture!==pe)&&(O!==Z&&(n.activeTexture(Z),O=Z),n.bindTexture(V,pe||ae[V]),ne.type=V,ne.texture=pe)}function j(){const V=q[O];V!==void 0&&V.type!==void 0&&(n.bindTexture(V.type,null),V.type=void 0,V.texture=void 0)}function ee(){try{n.compressedTexImage2D(...arguments)}catch(V){console.error("THREE.WebGLState:",V)}}function ie(){try{n.compressedTexImage3D(...arguments)}catch(V){console.error("THREE.WebGLState:",V)}}function Q(){try{n.texSubImage2D(...arguments)}catch(V){console.error("THREE.WebGLState:",V)}}function Ce(){try{n.texSubImage3D(...arguments)}catch(V){console.error("THREE.WebGLState:",V)}}function ge(){try{n.compressedTexSubImage2D(...arguments)}catch(V){console.error("THREE.WebGLState:",V)}}function be(){try{n.compressedTexSubImage3D(...arguments)}catch(V){console.error("THREE.WebGLState:",V)}}function $e(){try{n.texStorage2D(...arguments)}catch(V){console.error("THREE.WebGLState:",V)}}function de(){try{n.texStorage3D(...arguments)}catch(V){console.error("THREE.WebGLState:",V)}}function Te(){try{n.texImage2D(...arguments)}catch(V){console.error("THREE.WebGLState:",V)}}function ze(){try{n.texImage3D(...arguments)}catch(V){console.error("THREE.WebGLState:",V)}}function ke(V){De.equals(V)===!1&&(n.scissor(V.x,V.y,V.z,V.w),De.copy(V))}function we(V){X.equals(V)===!1&&(n.viewport(V.x,V.y,V.z,V.w),X.copy(V))}function Ke(V,pe){let Z=l.get(pe);Z===void 0&&(Z=new WeakMap,l.set(pe,Z));let ne=Z.get(V);ne===void 0&&(ne=n.getUniformBlockIndex(pe,V.name),Z.set(V,ne))}function Ge(V,pe){const ne=l.get(pe).get(V);c.get(pe)!==ne&&(n.uniformBlockBinding(pe,ne,V.__bindingPointIndex),c.set(pe,ne))}function st(){n.disable(n.BLEND),n.disable(n.CULL_FACE),n.disable(n.DEPTH_TEST),n.disable(n.POLYGON_OFFSET_FILL),n.disable(n.SCISSOR_TEST),n.disable(n.STENCIL_TEST),n.disable(n.SAMPLE_ALPHA_TO_COVERAGE),n.blendEquation(n.FUNC_ADD),n.blendFunc(n.ONE,n.ZERO),n.blendFuncSeparate(n.ONE,n.ZERO,n.ONE,n.ZERO),n.blendColor(0,0,0,0),n.colorMask(!0,!0,!0,!0),n.clearColor(0,0,0,0),n.depthMask(!0),n.depthFunc(n.LESS),s.setReversed(!1),n.clearDepth(1),n.stencilMask(4294967295),n.stencilFunc(n.ALWAYS,0,4294967295),n.stencilOp(n.KEEP,n.KEEP,n.KEEP),n.clearStencil(0),n.cullFace(n.BACK),n.frontFace(n.CCW),n.polygonOffset(0,0),n.activeTexture(n.TEXTURE0),n.bindFramebuffer(n.FRAMEBUFFER,null),n.bindFramebuffer(n.DRAW_FRAMEBUFFER,null),n.bindFramebuffer(n.READ_FRAMEBUFFER,null),n.useProgram(null),n.lineWidth(1),n.scissor(0,0,n.canvas.width,n.canvas.height),n.viewport(0,0,n.canvas.width,n.canvas.height),d={},O=null,q={},h={},f=new WeakMap,m=[],g=null,_=!1,p=null,u=null,E=null,y=null,M=null,D=null,A=null,b=new oe(0,0,0),C=0,v=!1,x=null,P=null,U=null,w=null,R=null,De.set(0,0,n.canvas.width,n.canvas.height),X.set(0,0,n.canvas.width,n.canvas.height),a.reset(),s.reset(),o.reset()}return{buffers:{color:a,depth:s,stencil:o},enable:re,disable:ue,bindFramebuffer:Pe,drawBuffers:fe,useProgram:te,setBlending:L,setMaterial:Ee,setFlipSided:Se,setCullFace:_e,setLineWidth:ve,setPolygonOffset:Ne,setScissorTest:Re,activeTexture:I,bindTexture:S,unbindTexture:j,compressedTexImage2D:ee,compressedTexImage3D:ie,texImage2D:Te,texImage3D:ze,updateUBOMapping:Ke,uniformBlockBinding:Ge,texStorage2D:$e,texStorage3D:de,texSubImage2D:Q,texSubImage3D:Ce,compressedTexSubImage2D:ge,compressedTexSubImage3D:be,scissor:ke,viewport:we,reset:st}}function ym(n,e,t,i,r,a,s){const o=e.has("WEBGL_multisampled_render_to_texture")?e.get("WEBGL_multisampled_render_to_texture"):null,c=typeof navigator>"u"?!1:/OculusBrowser/g.test(navigator.userAgent),l=new We,d=new WeakMap;let h;const f=new WeakMap;let m=!1;try{m=typeof OffscreenCanvas<"u"&&new OffscreenCanvas(1,1).getContext("2d")!==null}catch{}function g(I,S){return m?new OffscreenCanvas(I,S):Wr("canvas")}function _(I,S,j){let ee=1;const ie=Re(I);if((ie.width>j||ie.height>j)&&(ee=j/Math.max(ie.width,ie.height)),ee<1)if(typeof HTMLImageElement<"u"&&I instanceof HTMLImageElement||typeof HTMLCanvasElement<"u"&&I instanceof HTMLCanvasElement||typeof ImageBitmap<"u"&&I instanceof ImageBitmap||typeof VideoFrame<"u"&&I instanceof VideoFrame){const Q=Math.floor(ee*ie.width),Ce=Math.floor(ee*ie.height);h===void 0&&(h=g(Q,Ce));const ge=S?g(Q,Ce):h;return ge.width=Q,ge.height=Ce,ge.getContext("2d").drawImage(I,0,0,Q,Ce),console.warn("THREE.WebGLRenderer: Texture has been resized from ("+ie.width+"x"+ie.height+") to ("+Q+"x"+Ce+")."),ge}else return"data"in I&&console.warn("THREE.WebGLRenderer: Image in DataTexture is too big ("+ie.width+"x"+ie.height+")."),I;return I}function p(I){return I.generateMipmaps}function u(I){n.generateMipmap(I)}function E(I){return I.isWebGLCubeRenderTarget?n.TEXTURE_CUBE_MAP:I.isWebGL3DRenderTarget?n.TEXTURE_3D:I.isWebGLArrayRenderTarget||I.isCompressedArrayTexture?n.TEXTURE_2D_ARRAY:n.TEXTURE_2D}function y(I,S,j,ee,ie=!1){if(I!==null){if(n[I]!==void 0)return n[I];console.warn("THREE.WebGLRenderer: Attempt to use non-existing WebGL internal format '"+I+"'")}let Q=S;if(S===n.RED&&(j===n.FLOAT&&(Q=n.R32F),j===n.HALF_FLOAT&&(Q=n.R16F),j===n.UNSIGNED_BYTE&&(Q=n.R8)),S===n.RED_INTEGER&&(j===n.UNSIGNED_BYTE&&(Q=n.R8UI),j===n.UNSIGNED_SHORT&&(Q=n.R16UI),j===n.UNSIGNED_INT&&(Q=n.R32UI),j===n.BYTE&&(Q=n.R8I),j===n.SHORT&&(Q=n.R16I),j===n.INT&&(Q=n.R32I)),S===n.RG&&(j===n.FLOAT&&(Q=n.RG32F),j===n.HALF_FLOAT&&(Q=n.RG16F),j===n.UNSIGNED_BYTE&&(Q=n.RG8)),S===n.RG_INTEGER&&(j===n.UNSIGNED_BYTE&&(Q=n.RG8UI),j===n.UNSIGNED_SHORT&&(Q=n.RG16UI),j===n.UNSIGNED_INT&&(Q=n.RG32UI),j===n.BYTE&&(Q=n.RG8I),j===n.SHORT&&(Q=n.RG16I),j===n.INT&&(Q=n.RG32I)),S===n.RGB_INTEGER&&(j===n.UNSIGNED_BYTE&&(Q=n.RGB8UI),j===n.UNSIGNED_SHORT&&(Q=n.RGB16UI),j===n.UNSIGNED_INT&&(Q=n.RGB32UI),j===n.BYTE&&(Q=n.RGB8I),j===n.SHORT&&(Q=n.RGB16I),j===n.INT&&(Q=n.RGB32I)),S===n.RGBA_INTEGER&&(j===n.UNSIGNED_BYTE&&(Q=n.RGBA8UI),j===n.UNSIGNED_SHORT&&(Q=n.RGBA16UI),j===n.UNSIGNED_INT&&(Q=n.RGBA32UI),j===n.BYTE&&(Q=n.RGBA8I),j===n.SHORT&&(Q=n.RGBA16I),j===n.INT&&(Q=n.RGBA32I)),S===n.RGB&&j===n.UNSIGNED_INT_5_9_9_9_REV&&(Q=n.RGB9_E5),S===n.RGBA){const Ce=ie?Hr:Je.getTransfer(ee);j===n.FLOAT&&(Q=n.RGBA32F),j===n.HALF_FLOAT&&(Q=n.RGBA16F),j===n.UNSIGNED_BYTE&&(Q=Ce===it?n.SRGB8_ALPHA8:n.RGBA8),j===n.UNSIGNED_SHORT_4_4_4_4&&(Q=n.RGBA4),j===n.UNSIGNED_SHORT_5_5_5_1&&(Q=n.RGB5_A1)}return(Q===n.R16F||Q===n.R32F||Q===n.RG16F||Q===n.RG32F||Q===n.RGBA16F||Q===n.RGBA32F)&&e.get("EXT_color_buffer_float"),Q}function M(I,S){let j;return I?S===null||S===ei||S===Li?j=n.DEPTH24_STENCIL8:S===hn?j=n.DEPTH32F_STENCIL8:S===Ji&&(j=n.DEPTH24_STENCIL8,console.warn("DepthTexture: 16 bit depth attachment is not supported with stencil. Using 24-bit attachment.")):S===null||S===ei||S===Li?j=n.DEPTH_COMPONENT24:S===hn?j=n.DEPTH_COMPONENT32F:S===Ji&&(j=n.DEPTH_COMPONENT16),j}function D(I,S){return p(I)===!0||I.isFramebufferTexture&&I.minFilter!==Ft&&I.minFilter!==Jt?Math.log2(Math.max(S.width,S.height))+1:I.mipmaps!==void 0&&I.mipmaps.length>0?I.mipmaps.length:I.isCompressedTexture&&Array.isArray(I.image)?S.mipmaps.length:1}function A(I){const S=I.target;S.removeEventListener("dispose",A),C(S),S.isVideoTexture&&d.delete(S)}function b(I){const S=I.target;S.removeEventListener("dispose",b),x(S)}function C(I){const S=i.get(I);if(S.__webglInit===void 0)return;const j=I.source,ee=f.get(j);if(ee){const ie=ee[S.__cacheKey];ie.usedTimes--,ie.usedTimes===0&&v(I),Object.keys(ee).length===0&&f.delete(j)}i.remove(I)}function v(I){const S=i.get(I);n.deleteTexture(S.__webglTexture);const j=I.source,ee=f.get(j);delete ee[S.__cacheKey],s.memory.textures--}function x(I){const S=i.get(I);if(I.depthTexture&&(I.depthTexture.dispose(),i.remove(I.depthTexture)),I.isWebGLCubeRenderTarget)for(let ee=0;ee<6;ee++){if(Array.isArray(S.__webglFramebuffer[ee]))for(let ie=0;ie<S.__webglFramebuffer[ee].length;ie++)n.deleteFramebuffer(S.__webglFramebuffer[ee][ie]);else n.deleteFramebuffer(S.__webglFramebuffer[ee]);S.__webglDepthbuffer&&n.deleteRenderbuffer(S.__webglDepthbuffer[ee])}else{if(Array.isArray(S.__webglFramebuffer))for(let ee=0;ee<S.__webglFramebuffer.length;ee++)n.deleteFramebuffer(S.__webglFramebuffer[ee]);else n.deleteFramebuffer(S.__webglFramebuffer);if(S.__webglDepthbuffer&&n.deleteRenderbuffer(S.__webglDepthbuffer),S.__webglMultisampledFramebuffer&&n.deleteFramebuffer(S.__webglMultisampledFramebuffer),S.__webglColorRenderbuffer)for(let ee=0;ee<S.__webglColorRenderbuffer.length;ee++)S.__webglColorRenderbuffer[ee]&&n.deleteRenderbuffer(S.__webglColorRenderbuffer[ee]);S.__webglDepthRenderbuffer&&n.deleteRenderbuffer(S.__webglDepthRenderbuffer)}const j=I.textures;for(let ee=0,ie=j.length;ee<ie;ee++){const Q=i.get(j[ee]);Q.__webglTexture&&(n.deleteTexture(Q.__webglTexture),s.memory.textures--),i.remove(j[ee])}i.remove(I)}let P=0;function U(){P=0}function w(){const I=P;return I>=r.maxTextures&&console.warn("THREE.WebGLTextures: Trying to use "+I+" texture units while this GPU supports only "+r.maxTextures),P+=1,I}function R(I){const S=[];return S.push(I.wrapS),S.push(I.wrapT),S.push(I.wrapR||0),S.push(I.magFilter),S.push(I.minFilter),S.push(I.anisotropy),S.push(I.internalFormat),S.push(I.format),S.push(I.type),S.push(I.generateMipmaps),S.push(I.premultiplyAlpha),S.push(I.flipY),S.push(I.unpackAlignment),S.push(I.colorSpace),S.join()}function z(I,S){const j=i.get(I);if(I.isVideoTexture&&ve(I),I.isRenderTargetTexture===!1&&I.version>0&&j.__version!==I.version){const ee=I.image;if(ee===null)console.warn("THREE.WebGLRenderer: Texture marked for update but no image data found.");else if(ee.complete===!1)console.warn("THREE.WebGLRenderer: Texture marked for update but image is incomplete");else{X(j,I,S);return}}t.bindTexture(n.TEXTURE_2D,j.__webglTexture,n.TEXTURE0+S)}function N(I,S){const j=i.get(I);if(I.version>0&&j.__version!==I.version){X(j,I,S);return}t.bindTexture(n.TEXTURE_2D_ARRAY,j.__webglTexture,n.TEXTURE0+S)}function B(I,S){const j=i.get(I);if(I.version>0&&j.__version!==I.version){X(j,I,S);return}t.bindTexture(n.TEXTURE_3D,j.__webglTexture,n.TEXTURE0+S)}function k(I,S){const j=i.get(I);if(I.version>0&&j.__version!==I.version){J(j,I,S);return}t.bindTexture(n.TEXTURE_CUBE_MAP,j.__webglTexture,n.TEXTURE0+S)}const O={[Ya]:n.REPEAT,[$n]:n.CLAMP_TO_EDGE,[Za]:n.MIRRORED_REPEAT},q={[Ft]:n.NEAREST,[Yl]:n.NEAREST_MIPMAP_NEAREST,[cr]:n.NEAREST_MIPMAP_LINEAR,[Jt]:n.LINEAR,[ea]:n.LINEAR_MIPMAP_NEAREST,[Yn]:n.LINEAR_MIPMAP_LINEAR},K={[eu]:n.NEVER,[su]:n.ALWAYS,[tu]:n.LESS,[Wc]:n.LEQUAL,[nu]:n.EQUAL,[au]:n.GEQUAL,[iu]:n.GREATER,[ru]:n.NOTEQUAL};function le(I,S){if(S.type===hn&&e.has("OES_texture_float_linear")===!1&&(S.magFilter===Jt||S.magFilter===ea||S.magFilter===cr||S.magFilter===Yn||S.minFilter===Jt||S.minFilter===ea||S.minFilter===cr||S.minFilter===Yn)&&console.warn("THREE.WebGLRenderer: Unable to use linear filtering with floating point textures. OES_texture_float_linear not supported on this device."),n.texParameteri(I,n.TEXTURE_WRAP_S,O[S.wrapS]),n.texParameteri(I,n.TEXTURE_WRAP_T,O[S.wrapT]),(I===n.TEXTURE_3D||I===n.TEXTURE_2D_ARRAY)&&n.texParameteri(I,n.TEXTURE_WRAP_R,O[S.wrapR]),n.texParameteri(I,n.TEXTURE_MAG_FILTER,q[S.magFilter]),n.texParameteri(I,n.TEXTURE_MIN_FILTER,q[S.minFilter]),S.compareFunction&&(n.texParameteri(I,n.TEXTURE_COMPARE_MODE,n.COMPARE_REF_TO_TEXTURE),n.texParameteri(I,n.TEXTURE_COMPARE_FUNC,K[S.compareFunction])),e.has("EXT_texture_filter_anisotropic")===!0){if(S.magFilter===Ft||S.minFilter!==cr&&S.minFilter!==Yn||S.type===hn&&e.has("OES_texture_float_linear")===!1)return;if(S.anisotropy>1||i.get(S).__currentAnisotropy){const j=e.get("EXT_texture_filter_anisotropic");n.texParameterf(I,j.TEXTURE_MAX_ANISOTROPY_EXT,Math.min(S.anisotropy,r.getMaxAnisotropy())),i.get(S).__currentAnisotropy=S.anisotropy}}}function De(I,S){let j=!1;I.__webglInit===void 0&&(I.__webglInit=!0,S.addEventListener("dispose",A));const ee=S.source;let ie=f.get(ee);ie===void 0&&(ie={},f.set(ee,ie));const Q=R(S);if(Q!==I.__cacheKey){ie[Q]===void 0&&(ie[Q]={texture:n.createTexture(),usedTimes:0},s.memory.textures++,j=!0),ie[Q].usedTimes++;const Ce=ie[I.__cacheKey];Ce!==void 0&&(ie[I.__cacheKey].usedTimes--,Ce.usedTimes===0&&v(S)),I.__cacheKey=Q,I.__webglTexture=ie[Q].texture}return j}function X(I,S,j){let ee=n.TEXTURE_2D;(S.isDataArrayTexture||S.isCompressedArrayTexture)&&(ee=n.TEXTURE_2D_ARRAY),S.isData3DTexture&&(ee=n.TEXTURE_3D);const ie=De(I,S),Q=S.source;t.bindTexture(ee,I.__webglTexture,n.TEXTURE0+j);const Ce=i.get(Q);if(Q.version!==Ce.__version||ie===!0){t.activeTexture(n.TEXTURE0+j);const ge=Je.getPrimaries(Je.workingColorSpace),be=S.colorSpace===wn?null:Je.getPrimaries(S.colorSpace),$e=S.colorSpace===wn||ge===be?n.NONE:n.BROWSER_DEFAULT_WEBGL;n.pixelStorei(n.UNPACK_FLIP_Y_WEBGL,S.flipY),n.pixelStorei(n.UNPACK_PREMULTIPLY_ALPHA_WEBGL,S.premultiplyAlpha),n.pixelStorei(n.UNPACK_ALIGNMENT,S.unpackAlignment),n.pixelStorei(n.UNPACK_COLORSPACE_CONVERSION_WEBGL,$e);let de=_(S.image,!1,r.maxTextureSize);de=Ne(S,de);const Te=a.convert(S.format,S.colorSpace),ze=a.convert(S.type);let ke=y(S.internalFormat,Te,ze,S.colorSpace,S.isVideoTexture);le(ee,S);let we;const Ke=S.mipmaps,Ge=S.isVideoTexture!==!0,st=Ce.__version===void 0||ie===!0,V=Q.dataReady,pe=D(S,de);if(S.isDepthTexture)ke=M(S.format===Ii,S.type),st&&(Ge?t.texStorage2D(n.TEXTURE_2D,1,ke,de.width,de.height):t.texImage2D(n.TEXTURE_2D,0,ke,de.width,de.height,0,Te,ze,null));else if(S.isDataTexture)if(Ke.length>0){Ge&&st&&t.texStorage2D(n.TEXTURE_2D,pe,ke,Ke[0].width,Ke[0].height);for(let Z=0,ne=Ke.length;Z<ne;Z++)we=Ke[Z],Ge?V&&t.texSubImage2D(n.TEXTURE_2D,Z,0,0,we.width,we.height,Te,ze,we.data):t.texImage2D(n.TEXTURE_2D,Z,ke,we.width,we.height,0,Te,ze,we.data);S.generateMipmaps=!1}else Ge?(st&&t.texStorage2D(n.TEXTURE_2D,pe,ke,de.width,de.height),V&&t.texSubImage2D(n.TEXTURE_2D,0,0,0,de.width,de.height,Te,ze,de.data)):t.texImage2D(n.TEXTURE_2D,0,ke,de.width,de.height,0,Te,ze,de.data);else if(S.isCompressedTexture)if(S.isCompressedArrayTexture){Ge&&st&&t.texStorage3D(n.TEXTURE_2D_ARRAY,pe,ke,Ke[0].width,Ke[0].height,de.depth);for(let Z=0,ne=Ke.length;Z<ne;Z++)if(we=Ke[Z],S.format!==Ht)if(Te!==null)if(Ge){if(V)if(S.layerUpdates.size>0){const Me=Wo(we.width,we.height,S.format,S.type);for(const xe of S.layerUpdates){const Be=we.data.subarray(xe*Me/we.data.BYTES_PER_ELEMENT,(xe+1)*Me/we.data.BYTES_PER_ELEMENT);t.compressedTexSubImage3D(n.TEXTURE_2D_ARRAY,Z,0,0,xe,we.width,we.height,1,Te,Be)}S.clearLayerUpdates()}else t.compressedTexSubImage3D(n.TEXTURE_2D_ARRAY,Z,0,0,0,we.width,we.height,de.depth,Te,we.data)}else t.compressedTexImage3D(n.TEXTURE_2D_ARRAY,Z,ke,we.width,we.height,de.depth,0,we.data,0,0);else console.warn("THREE.WebGLRenderer: Attempt to load unsupported compressed texture format in .uploadTexture()");else Ge?V&&t.texSubImage3D(n.TEXTURE_2D_ARRAY,Z,0,0,0,we.width,we.height,de.depth,Te,ze,we.data):t.texImage3D(n.TEXTURE_2D_ARRAY,Z,ke,we.width,we.height,de.depth,0,Te,ze,we.data)}else{Ge&&st&&t.texStorage2D(n.TEXTURE_2D,pe,ke,Ke[0].width,Ke[0].height);for(let Z=0,ne=Ke.length;Z<ne;Z++)we=Ke[Z],S.format!==Ht?Te!==null?Ge?V&&t.compressedTexSubImage2D(n.TEXTURE_2D,Z,0,0,we.width,we.height,Te,we.data):t.compressedTexImage2D(n.TEXTURE_2D,Z,ke,we.width,we.height,0,we.data):console.warn("THREE.WebGLRenderer: Attempt to load unsupported compressed texture format in .uploadTexture()"):Ge?V&&t.texSubImage2D(n.TEXTURE_2D,Z,0,0,we.width,we.height,Te,ze,we.data):t.texImage2D(n.TEXTURE_2D,Z,ke,we.width,we.height,0,Te,ze,we.data)}else if(S.isDataArrayTexture)if(Ge){if(st&&t.texStorage3D(n.TEXTURE_2D_ARRAY,pe,ke,de.width,de.height,de.depth),V)if(S.layerUpdates.size>0){const Z=Wo(de.width,de.height,S.format,S.type);for(const ne of S.layerUpdates){const Me=de.data.subarray(ne*Z/de.data.BYTES_PER_ELEMENT,(ne+1)*Z/de.data.BYTES_PER_ELEMENT);t.texSubImage3D(n.TEXTURE_2D_ARRAY,0,0,0,ne,de.width,de.height,1,Te,ze,Me)}S.clearLayerUpdates()}else t.texSubImage3D(n.TEXTURE_2D_ARRAY,0,0,0,0,de.width,de.height,de.depth,Te,ze,de.data)}else t.texImage3D(n.TEXTURE_2D_ARRAY,0,ke,de.width,de.height,de.depth,0,Te,ze,de.data);else if(S.isData3DTexture)Ge?(st&&t.texStorage3D(n.TEXTURE_3D,pe,ke,de.width,de.height,de.depth),V&&t.texSubImage3D(n.TEXTURE_3D,0,0,0,0,de.width,de.height,de.depth,Te,ze,de.data)):t.texImage3D(n.TEXTURE_3D,0,ke,de.width,de.height,de.depth,0,Te,ze,de.data);else if(S.isFramebufferTexture){if(st)if(Ge)t.texStorage2D(n.TEXTURE_2D,pe,ke,de.width,de.height);else{let Z=de.width,ne=de.height;for(let Me=0;Me<pe;Me++)t.texImage2D(n.TEXTURE_2D,Me,ke,Z,ne,0,Te,ze,null),Z>>=1,ne>>=1}}else if(Ke.length>0){if(Ge&&st){const Z=Re(Ke[0]);t.texStorage2D(n.TEXTURE_2D,pe,ke,Z.width,Z.height)}for(let Z=0,ne=Ke.length;Z<ne;Z++)we=Ke[Z],Ge?V&&t.texSubImage2D(n.TEXTURE_2D,Z,0,0,Te,ze,we):t.texImage2D(n.TEXTURE_2D,Z,ke,Te,ze,we);S.generateMipmaps=!1}else if(Ge){if(st){const Z=Re(de);t.texStorage2D(n.TEXTURE_2D,pe,ke,Z.width,Z.height)}V&&t.texSubImage2D(n.TEXTURE_2D,0,0,0,Te,ze,de)}else t.texImage2D(n.TEXTURE_2D,0,ke,Te,ze,de);p(S)&&u(ee),Ce.__version=Q.version,S.onUpdate&&S.onUpdate(S)}I.__version=S.version}function J(I,S,j){if(S.image.length!==6)return;const ee=De(I,S),ie=S.source;t.bindTexture(n.TEXTURE_CUBE_MAP,I.__webglTexture,n.TEXTURE0+j);const Q=i.get(ie);if(ie.version!==Q.__version||ee===!0){t.activeTexture(n.TEXTURE0+j);const Ce=Je.getPrimaries(Je.workingColorSpace),ge=S.colorSpace===wn?null:Je.getPrimaries(S.colorSpace),be=S.colorSpace===wn||Ce===ge?n.NONE:n.BROWSER_DEFAULT_WEBGL;n.pixelStorei(n.UNPACK_FLIP_Y_WEBGL,S.flipY),n.pixelStorei(n.UNPACK_PREMULTIPLY_ALPHA_WEBGL,S.premultiplyAlpha),n.pixelStorei(n.UNPACK_ALIGNMENT,S.unpackAlignment),n.pixelStorei(n.UNPACK_COLORSPACE_CONVERSION_WEBGL,be);const $e=S.isCompressedTexture||S.image[0].isCompressedTexture,de=S.image[0]&&S.image[0].isDataTexture,Te=[];for(let ne=0;ne<6;ne++)!$e&&!de?Te[ne]=_(S.image[ne],!0,r.maxCubemapSize):Te[ne]=de?S.image[ne].image:S.image[ne],Te[ne]=Ne(S,Te[ne]);const ze=Te[0],ke=a.convert(S.format,S.colorSpace),we=a.convert(S.type),Ke=y(S.internalFormat,ke,we,S.colorSpace),Ge=S.isVideoTexture!==!0,st=Q.__version===void 0||ee===!0,V=ie.dataReady;let pe=D(S,ze);le(n.TEXTURE_CUBE_MAP,S);let Z;if($e){Ge&&st&&t.texStorage2D(n.TEXTURE_CUBE_MAP,pe,Ke,ze.width,ze.height);for(let ne=0;ne<6;ne++){Z=Te[ne].mipmaps;for(let Me=0;Me<Z.length;Me++){const xe=Z[Me];S.format!==Ht?ke!==null?Ge?V&&t.compressedTexSubImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+ne,Me,0,0,xe.width,xe.height,ke,xe.data):t.compressedTexImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+ne,Me,Ke,xe.width,xe.height,0,xe.data):console.warn("THREE.WebGLRenderer: Attempt to load unsupported compressed texture format in .setTextureCube()"):Ge?V&&t.texSubImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+ne,Me,0,0,xe.width,xe.height,ke,we,xe.data):t.texImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+ne,Me,Ke,xe.width,xe.height,0,ke,we,xe.data)}}}else{if(Z=S.mipmaps,Ge&&st){Z.length>0&&pe++;const ne=Re(Te[0]);t.texStorage2D(n.TEXTURE_CUBE_MAP,pe,Ke,ne.width,ne.height)}for(let ne=0;ne<6;ne++)if(de){Ge?V&&t.texSubImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+ne,0,0,0,Te[ne].width,Te[ne].height,ke,we,Te[ne].data):t.texImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+ne,0,Ke,Te[ne].width,Te[ne].height,0,ke,we,Te[ne].data);for(let Me=0;Me<Z.length;Me++){const Be=Z[Me].image[ne].image;Ge?V&&t.texSubImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+ne,Me+1,0,0,Be.width,Be.height,ke,we,Be.data):t.texImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+ne,Me+1,Ke,Be.width,Be.height,0,ke,we,Be.data)}}else{Ge?V&&t.texSubImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+ne,0,0,0,ke,we,Te[ne]):t.texImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+ne,0,Ke,ke,we,Te[ne]);for(let Me=0;Me<Z.length;Me++){const xe=Z[Me];Ge?V&&t.texSubImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+ne,Me+1,0,0,ke,we,xe.image[ne]):t.texImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+ne,Me+1,Ke,ke,we,xe.image[ne])}}}p(S)&&u(n.TEXTURE_CUBE_MAP),Q.__version=ie.version,S.onUpdate&&S.onUpdate(S)}I.__version=S.version}function ae(I,S,j,ee,ie,Q){const Ce=a.convert(j.format,j.colorSpace),ge=a.convert(j.type),be=y(j.internalFormat,Ce,ge,j.colorSpace),$e=i.get(S),de=i.get(j);if(de.__renderTarget=S,!$e.__hasExternalTextures){const Te=Math.max(1,S.width>>Q),ze=Math.max(1,S.height>>Q);ie===n.TEXTURE_3D||ie===n.TEXTURE_2D_ARRAY?t.texImage3D(ie,Q,be,Te,ze,S.depth,0,Ce,ge,null):t.texImage2D(ie,Q,be,Te,ze,0,Ce,ge,null)}t.bindFramebuffer(n.FRAMEBUFFER,I),_e(S)?o.framebufferTexture2DMultisampleEXT(n.FRAMEBUFFER,ee,ie,de.__webglTexture,0,Se(S)):(ie===n.TEXTURE_2D||ie>=n.TEXTURE_CUBE_MAP_POSITIVE_X&&ie<=n.TEXTURE_CUBE_MAP_NEGATIVE_Z)&&n.framebufferTexture2D(n.FRAMEBUFFER,ee,ie,de.__webglTexture,Q),t.bindFramebuffer(n.FRAMEBUFFER,null)}function re(I,S,j){if(n.bindRenderbuffer(n.RENDERBUFFER,I),S.depthBuffer){const ee=S.depthTexture,ie=ee&&ee.isDepthTexture?ee.type:null,Q=M(S.stencilBuffer,ie),Ce=S.stencilBuffer?n.DEPTH_STENCIL_ATTACHMENT:n.DEPTH_ATTACHMENT,ge=Se(S);_e(S)?o.renderbufferStorageMultisampleEXT(n.RENDERBUFFER,ge,Q,S.width,S.height):j?n.renderbufferStorageMultisample(n.RENDERBUFFER,ge,Q,S.width,S.height):n.renderbufferStorage(n.RENDERBUFFER,Q,S.width,S.height),n.framebufferRenderbuffer(n.FRAMEBUFFER,Ce,n.RENDERBUFFER,I)}else{const ee=S.textures;for(let ie=0;ie<ee.length;ie++){const Q=ee[ie],Ce=a.convert(Q.format,Q.colorSpace),ge=a.convert(Q.type),be=y(Q.internalFormat,Ce,ge,Q.colorSpace),$e=Se(S);j&&_e(S)===!1?n.renderbufferStorageMultisample(n.RENDERBUFFER,$e,be,S.width,S.height):_e(S)?o.renderbufferStorageMultisampleEXT(n.RENDERBUFFER,$e,be,S.width,S.height):n.renderbufferStorage(n.RENDERBUFFER,be,S.width,S.height)}}n.bindRenderbuffer(n.RENDERBUFFER,null)}function ue(I,S){if(S&&S.isWebGLCubeRenderTarget)throw new Error("Depth Texture with cube render targets is not supported");if(t.bindFramebuffer(n.FRAMEBUFFER,I),!(S.depthTexture&&S.depthTexture.isDepthTexture))throw new Error("renderTarget.depthTexture must be an instance of THREE.DepthTexture");const ee=i.get(S.depthTexture);ee.__renderTarget=S,(!ee.__webglTexture||S.depthTexture.image.width!==S.width||S.depthTexture.image.height!==S.height)&&(S.depthTexture.image.width=S.width,S.depthTexture.image.height=S.height,S.depthTexture.needsUpdate=!0),z(S.depthTexture,0);const ie=ee.__webglTexture,Q=Se(S);if(S.depthTexture.format===Ai)_e(S)?o.framebufferTexture2DMultisampleEXT(n.FRAMEBUFFER,n.DEPTH_ATTACHMENT,n.TEXTURE_2D,ie,0,Q):n.framebufferTexture2D(n.FRAMEBUFFER,n.DEPTH_ATTACHMENT,n.TEXTURE_2D,ie,0);else if(S.depthTexture.format===Ii)_e(S)?o.framebufferTexture2DMultisampleEXT(n.FRAMEBUFFER,n.DEPTH_STENCIL_ATTACHMENT,n.TEXTURE_2D,ie,0,Q):n.framebufferTexture2D(n.FRAMEBUFFER,n.DEPTH_STENCIL_ATTACHMENT,n.TEXTURE_2D,ie,0);else throw new Error("Unknown depthTexture format")}function Pe(I){const S=i.get(I),j=I.isWebGLCubeRenderTarget===!0;if(S.__boundDepthTexture!==I.depthTexture){const ee=I.depthTexture;if(S.__depthDisposeCallback&&S.__depthDisposeCallback(),ee){const ie=()=>{delete S.__boundDepthTexture,delete S.__depthDisposeCallback,ee.removeEventListener("dispose",ie)};ee.addEventListener("dispose",ie),S.__depthDisposeCallback=ie}S.__boundDepthTexture=ee}if(I.depthTexture&&!S.__autoAllocateDepthBuffer){if(j)throw new Error("target.depthTexture not supported in Cube render targets");ue(S.__webglFramebuffer,I)}else if(j){S.__webglDepthbuffer=[];for(let ee=0;ee<6;ee++)if(t.bindFramebuffer(n.FRAMEBUFFER,S.__webglFramebuffer[ee]),S.__webglDepthbuffer[ee]===void 0)S.__webglDepthbuffer[ee]=n.createRenderbuffer(),re(S.__webglDepthbuffer[ee],I,!1);else{const ie=I.stencilBuffer?n.DEPTH_STENCIL_ATTACHMENT:n.DEPTH_ATTACHMENT,Q=S.__webglDepthbuffer[ee];n.bindRenderbuffer(n.RENDERBUFFER,Q),n.framebufferRenderbuffer(n.FRAMEBUFFER,ie,n.RENDERBUFFER,Q)}}else if(t.bindFramebuffer(n.FRAMEBUFFER,S.__webglFramebuffer),S.__webglDepthbuffer===void 0)S.__webglDepthbuffer=n.createRenderbuffer(),re(S.__webglDepthbuffer,I,!1);else{const ee=I.stencilBuffer?n.DEPTH_STENCIL_ATTACHMENT:n.DEPTH_ATTACHMENT,ie=S.__webglDepthbuffer;n.bindRenderbuffer(n.RENDERBUFFER,ie),n.framebufferRenderbuffer(n.FRAMEBUFFER,ee,n.RENDERBUFFER,ie)}t.bindFramebuffer(n.FRAMEBUFFER,null)}function fe(I,S,j){const ee=i.get(I);S!==void 0&&ae(ee.__webglFramebuffer,I,I.texture,n.COLOR_ATTACHMENT0,n.TEXTURE_2D,0),j!==void 0&&Pe(I)}function te(I){const S=I.texture,j=i.get(I),ee=i.get(S);I.addEventListener("dispose",b);const ie=I.textures,Q=I.isWebGLCubeRenderTarget===!0,Ce=ie.length>1;if(Ce||(ee.__webglTexture===void 0&&(ee.__webglTexture=n.createTexture()),ee.__version=S.version,s.memory.textures++),Q){j.__webglFramebuffer=[];for(let ge=0;ge<6;ge++)if(S.mipmaps&&S.mipmaps.length>0){j.__webglFramebuffer[ge]=[];for(let be=0;be<S.mipmaps.length;be++)j.__webglFramebuffer[ge][be]=n.createFramebuffer()}else j.__webglFramebuffer[ge]=n.createFramebuffer()}else{if(S.mipmaps&&S.mipmaps.length>0){j.__webglFramebuffer=[];for(let ge=0;ge<S.mipmaps.length;ge++)j.__webglFramebuffer[ge]=n.createFramebuffer()}else j.__webglFramebuffer=n.createFramebuffer();if(Ce)for(let ge=0,be=ie.length;ge<be;ge++){const $e=i.get(ie[ge]);$e.__webglTexture===void 0&&($e.__webglTexture=n.createTexture(),s.memory.textures++)}if(I.samples>0&&_e(I)===!1){j.__webglMultisampledFramebuffer=n.createFramebuffer(),j.__webglColorRenderbuffer=[],t.bindFramebuffer(n.FRAMEBUFFER,j.__webglMultisampledFramebuffer);for(let ge=0;ge<ie.length;ge++){const be=ie[ge];j.__webglColorRenderbuffer[ge]=n.createRenderbuffer(),n.bindRenderbuffer(n.RENDERBUFFER,j.__webglColorRenderbuffer[ge]);const $e=a.convert(be.format,be.colorSpace),de=a.convert(be.type),Te=y(be.internalFormat,$e,de,be.colorSpace,I.isXRRenderTarget===!0),ze=Se(I);n.renderbufferStorageMultisample(n.RENDERBUFFER,ze,Te,I.width,I.height),n.framebufferRenderbuffer(n.FRAMEBUFFER,n.COLOR_ATTACHMENT0+ge,n.RENDERBUFFER,j.__webglColorRenderbuffer[ge])}n.bindRenderbuffer(n.RENDERBUFFER,null),I.depthBuffer&&(j.__webglDepthRenderbuffer=n.createRenderbuffer(),re(j.__webglDepthRenderbuffer,I,!0)),t.bindFramebuffer(n.FRAMEBUFFER,null)}}if(Q){t.bindTexture(n.TEXTURE_CUBE_MAP,ee.__webglTexture),le(n.TEXTURE_CUBE_MAP,S);for(let ge=0;ge<6;ge++)if(S.mipmaps&&S.mipmaps.length>0)for(let be=0;be<S.mipmaps.length;be++)ae(j.__webglFramebuffer[ge][be],I,S,n.COLOR_ATTACHMENT0,n.TEXTURE_CUBE_MAP_POSITIVE_X+ge,be);else ae(j.__webglFramebuffer[ge],I,S,n.COLOR_ATTACHMENT0,n.TEXTURE_CUBE_MAP_POSITIVE_X+ge,0);p(S)&&u(n.TEXTURE_CUBE_MAP),t.unbindTexture()}else if(Ce){for(let ge=0,be=ie.length;ge<be;ge++){const $e=ie[ge],de=i.get($e);t.bindTexture(n.TEXTURE_2D,de.__webglTexture),le(n.TEXTURE_2D,$e),ae(j.__webglFramebuffer,I,$e,n.COLOR_ATTACHMENT0+ge,n.TEXTURE_2D,0),p($e)&&u(n.TEXTURE_2D)}t.unbindTexture()}else{let ge=n.TEXTURE_2D;if((I.isWebGL3DRenderTarget||I.isWebGLArrayRenderTarget)&&(ge=I.isWebGL3DRenderTarget?n.TEXTURE_3D:n.TEXTURE_2D_ARRAY),t.bindTexture(ge,ee.__webglTexture),le(ge,S),S.mipmaps&&S.mipmaps.length>0)for(let be=0;be<S.mipmaps.length;be++)ae(j.__webglFramebuffer[be],I,S,n.COLOR_ATTACHMENT0,ge,be);else ae(j.__webglFramebuffer,I,S,n.COLOR_ATTACHMENT0,ge,0);p(S)&&u(ge),t.unbindTexture()}I.depthBuffer&&Pe(I)}function se(I){const S=I.textures;for(let j=0,ee=S.length;j<ee;j++){const ie=S[j];if(p(ie)){const Q=E(I),Ce=i.get(ie).__webglTexture;t.bindTexture(Q,Ce),u(Q),t.unbindTexture()}}}const W=[],L=[];function Ee(I){if(I.samples>0){if(_e(I)===!1){const S=I.textures,j=I.width,ee=I.height;let ie=n.COLOR_BUFFER_BIT;const Q=I.stencilBuffer?n.DEPTH_STENCIL_ATTACHMENT:n.DEPTH_ATTACHMENT,Ce=i.get(I),ge=S.length>1;if(ge)for(let be=0;be<S.length;be++)t.bindFramebuffer(n.FRAMEBUFFER,Ce.__webglMultisampledFramebuffer),n.framebufferRenderbuffer(n.FRAMEBUFFER,n.COLOR_ATTACHMENT0+be,n.RENDERBUFFER,null),t.bindFramebuffer(n.FRAMEBUFFER,Ce.__webglFramebuffer),n.framebufferTexture2D(n.DRAW_FRAMEBUFFER,n.COLOR_ATTACHMENT0+be,n.TEXTURE_2D,null,0);t.bindFramebuffer(n.READ_FRAMEBUFFER,Ce.__webglMultisampledFramebuffer),t.bindFramebuffer(n.DRAW_FRAMEBUFFER,Ce.__webglFramebuffer);for(let be=0;be<S.length;be++){if(I.resolveDepthBuffer&&(I.depthBuffer&&(ie|=n.DEPTH_BUFFER_BIT),I.stencilBuffer&&I.resolveStencilBuffer&&(ie|=n.STENCIL_BUFFER_BIT)),ge){n.framebufferRenderbuffer(n.READ_FRAMEBUFFER,n.COLOR_ATTACHMENT0,n.RENDERBUFFER,Ce.__webglColorRenderbuffer[be]);const $e=i.get(S[be]).__webglTexture;n.framebufferTexture2D(n.DRAW_FRAMEBUFFER,n.COLOR_ATTACHMENT0,n.TEXTURE_2D,$e,0)}n.blitFramebuffer(0,0,j,ee,0,0,j,ee,ie,n.NEAREST),c===!0&&(W.length=0,L.length=0,W.push(n.COLOR_ATTACHMENT0+be),I.depthBuffer&&I.resolveDepthBuffer===!1&&(W.push(Q),L.push(Q),n.invalidateFramebuffer(n.DRAW_FRAMEBUFFER,L)),n.invalidateFramebuffer(n.READ_FRAMEBUFFER,W))}if(t.bindFramebuffer(n.READ_FRAMEBUFFER,null),t.bindFramebuffer(n.DRAW_FRAMEBUFFER,null),ge)for(let be=0;be<S.length;be++){t.bindFramebuffer(n.FRAMEBUFFER,Ce.__webglMultisampledFramebuffer),n.framebufferRenderbuffer(n.FRAMEBUFFER,n.COLOR_ATTACHMENT0+be,n.RENDERBUFFER,Ce.__webglColorRenderbuffer[be]);const $e=i.get(S[be]).__webglTexture;t.bindFramebuffer(n.FRAMEBUFFER,Ce.__webglFramebuffer),n.framebufferTexture2D(n.DRAW_FRAMEBUFFER,n.COLOR_ATTACHMENT0+be,n.TEXTURE_2D,$e,0)}t.bindFramebuffer(n.DRAW_FRAMEBUFFER,Ce.__webglMultisampledFramebuffer)}else if(I.depthBuffer&&I.resolveDepthBuffer===!1&&c){const S=I.stencilBuffer?n.DEPTH_STENCIL_ATTACHMENT:n.DEPTH_ATTACHMENT;n.invalidateFramebuffer(n.DRAW_FRAMEBUFFER,[S])}}}function Se(I){return Math.min(r.maxSamples,I.samples)}function _e(I){const S=i.get(I);return I.samples>0&&e.has("WEBGL_multisampled_render_to_texture")===!0&&S.__useRenderToTexture!==!1}function ve(I){const S=s.render.frame;d.get(I)!==S&&(d.set(I,S),I.update())}function Ne(I,S){const j=I.colorSpace,ee=I.format,ie=I.type;return I.isCompressedTexture===!0||I.isVideoTexture===!0||j!==Ui&&j!==wn&&(Je.getTransfer(j)===it?(ee!==Ht||ie!==mn)&&console.warn("THREE.WebGLTextures: sRGB encoded textures have to use RGBAFormat and UnsignedByteType."):console.error("THREE.WebGLTextures: Unsupported texture color space:",j)),S}function Re(I){return typeof HTMLImageElement<"u"&&I instanceof HTMLImageElement?(l.width=I.naturalWidth||I.width,l.height=I.naturalHeight||I.height):typeof VideoFrame<"u"&&I instanceof VideoFrame?(l.width=I.displayWidth,l.height=I.displayHeight):(l.width=I.width,l.height=I.height),l}this.allocateTextureUnit=w,this.resetTextureUnits=U,this.setTexture2D=z,this.setTexture2DArray=N,this.setTexture3D=B,this.setTextureCube=k,this.rebindTextures=fe,this.setupRenderTarget=te,this.updateRenderTargetMipmap=se,this.updateMultisampleRenderTarget=Ee,this.setupDepthRenderbuffer=Pe,this.setupFrameBufferTexture=ae,this.useMultisampledRTT=_e}function bm(n,e){function t(i,r=wn){let a;const s=Je.getTransfer(r);if(i===mn)return n.UNSIGNED_BYTE;if(i===Ns)return n.UNSIGNED_SHORT_4_4_4_4;if(i===ks)return n.UNSIGNED_SHORT_5_5_5_1;if(i===Nc)return n.UNSIGNED_INT_5_9_9_9_REV;if(i===Uc)return n.BYTE;if(i===zc)return n.SHORT;if(i===Ji)return n.UNSIGNED_SHORT;if(i===zs)return n.INT;if(i===ei)return n.UNSIGNED_INT;if(i===hn)return n.FLOAT;if(i===ir)return n.HALF_FLOAT;if(i===kc)return n.ALPHA;if(i===Fc)return n.RGB;if(i===Ht)return n.RGBA;if(i===Oc)return n.LUMINANCE;if(i===Bc)return n.LUMINANCE_ALPHA;if(i===Ai)return n.DEPTH_COMPONENT;if(i===Ii)return n.DEPTH_STENCIL;if(i===Vc)return n.RED;if(i===Fs)return n.RED_INTEGER;if(i===Gc)return n.RG;if(i===Os)return n.RG_INTEGER;if(i===Bs)return n.RGBA_INTEGER;if(i===zr||i===Nr||i===kr||i===Fr)if(s===it)if(a=e.get("WEBGL_compressed_texture_s3tc_srgb"),a!==null){if(i===zr)return a.COMPRESSED_SRGB_S3TC_DXT1_EXT;if(i===Nr)return a.COMPRESSED_SRGB_ALPHA_S3TC_DXT1_EXT;if(i===kr)return a.COMPRESSED_SRGB_ALPHA_S3TC_DXT3_EXT;if(i===Fr)return a.COMPRESSED_SRGB_ALPHA_S3TC_DXT5_EXT}else return null;else if(a=e.get("WEBGL_compressed_texture_s3tc"),a!==null){if(i===zr)return a.COMPRESSED_RGB_S3TC_DXT1_EXT;if(i===Nr)return a.COMPRESSED_RGBA_S3TC_DXT1_EXT;if(i===kr)return a.COMPRESSED_RGBA_S3TC_DXT3_EXT;if(i===Fr)return a.COMPRESSED_RGBA_S3TC_DXT5_EXT}else return null;if(i===Ja||i===Qa||i===es||i===ts)if(a=e.get("WEBGL_compressed_texture_pvrtc"),a!==null){if(i===Ja)return a.COMPRESSED_RGB_PVRTC_4BPPV1_IMG;if(i===Qa)return a.COMPRESSED_RGB_PVRTC_2BPPV1_IMG;if(i===es)return a.COMPRESSED_RGBA_PVRTC_4BPPV1_IMG;if(i===ts)return a.COMPRESSED_RGBA_PVRTC_2BPPV1_IMG}else return null;if(i===ns||i===is||i===rs)if(a=e.get("WEBGL_compressed_texture_etc"),a!==null){if(i===ns||i===is)return s===it?a.COMPRESSED_SRGB8_ETC2:a.COMPRESSED_RGB8_ETC2;if(i===rs)return s===it?a.COMPRESSED_SRGB8_ALPHA8_ETC2_EAC:a.COMPRESSED_RGBA8_ETC2_EAC}else return null;if(i===as||i===ss||i===os||i===cs||i===ls||i===us||i===ds||i===hs||i===fs||i===ps||i===ms||i===gs||i===_s||i===vs)if(a=e.get("WEBGL_compressed_texture_astc"),a!==null){if(i===as)return s===it?a.COMPRESSED_SRGB8_ALPHA8_ASTC_4x4_KHR:a.COMPRESSED_RGBA_ASTC_4x4_KHR;if(i===ss)return s===it?a.COMPRESSED_SRGB8_ALPHA8_ASTC_5x4_KHR:a.COMPRESSED_RGBA_ASTC_5x4_KHR;if(i===os)return s===it?a.COMPRESSED_SRGB8_ALPHA8_ASTC_5x5_KHR:a.COMPRESSED_RGBA_ASTC_5x5_KHR;if(i===cs)return s===it?a.COMPRESSED_SRGB8_ALPHA8_ASTC_6x5_KHR:a.COMPRESSED_RGBA_ASTC_6x5_KHR;if(i===ls)return s===it?a.COMPRESSED_SRGB8_ALPHA8_ASTC_6x6_KHR:a.COMPRESSED_RGBA_ASTC_6x6_KHR;if(i===us)return s===it?a.COMPRESSED_SRGB8_ALPHA8_ASTC_8x5_KHR:a.COMPRESSED_RGBA_ASTC_8x5_KHR;if(i===ds)return s===it?a.COMPRESSED_SRGB8_ALPHA8_ASTC_8x6_KHR:a.COMPRESSED_RGBA_ASTC_8x6_KHR;if(i===hs)return s===it?a.COMPRESSED_SRGB8_ALPHA8_ASTC_8x8_KHR:a.COMPRESSED_RGBA_ASTC_8x8_KHR;if(i===fs)return s===it?a.COMPRESSED_SRGB8_ALPHA8_ASTC_10x5_KHR:a.COMPRESSED_RGBA_ASTC_10x5_KHR;if(i===ps)return s===it?a.COMPRESSED_SRGB8_ALPHA8_ASTC_10x6_KHR:a.COMPRESSED_RGBA_ASTC_10x6_KHR;if(i===ms)return s===it?a.COMPRESSED_SRGB8_ALPHA8_ASTC_10x8_KHR:a.COMPRESSED_RGBA_ASTC_10x8_KHR;if(i===gs)return s===it?a.COMPRESSED_SRGB8_ALPHA8_ASTC_10x10_KHR:a.COMPRESSED_RGBA_ASTC_10x10_KHR;if(i===_s)return s===it?a.COMPRESSED_SRGB8_ALPHA8_ASTC_12x10_KHR:a.COMPRESSED_RGBA_ASTC_12x10_KHR;if(i===vs)return s===it?a.COMPRESSED_SRGB8_ALPHA8_ASTC_12x12_KHR:a.COMPRESSED_RGBA_ASTC_12x12_KHR}else return null;if(i===Or||i===xs||i===Ms)if(a=e.get("EXT_texture_compression_bptc"),a!==null){if(i===Or)return s===it?a.COMPRESSED_SRGB_ALPHA_BPTC_UNORM_EXT:a.COMPRESSED_RGBA_BPTC_UNORM_EXT;if(i===xs)return a.COMPRESSED_RGB_BPTC_SIGNED_FLOAT_EXT;if(i===Ms)return a.COMPRESSED_RGB_BPTC_UNSIGNED_FLOAT_EXT}else return null;if(i===Hc||i===Ss||i===Es||i===ys)if(a=e.get("EXT_texture_compression_rgtc"),a!==null){if(i===Or)return a.COMPRESSED_RED_RGTC1_EXT;if(i===Ss)return a.COMPRESSED_SIGNED_RED_RGTC1_EXT;if(i===Es)return a.COMPRESSED_RED_GREEN_RGTC2_EXT;if(i===ys)return a.COMPRESSED_SIGNED_RED_GREEN_RGTC2_EXT}else return null;return i===Li?n.UNSIGNED_INT_24_8:n[i]!==void 0?n[i]:null}return{convert:t}}const Tm=`
void main() {

	gl_Position = vec4( position, 1.0 );

}`,wm=`
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

}`;class Am{constructor(){this.texture=null,this.mesh=null,this.depthNear=0,this.depthFar=0}init(e,t,i){if(this.texture===null){const r=new wt,a=e.properties.get(r);a.__webglTexture=t.texture,(t.depthNear!==i.depthNear||t.depthFar!==i.depthFar)&&(this.depthNear=t.depthNear,this.depthFar=t.depthFar),this.texture=r}}getMesh(e){if(this.texture!==null&&this.mesh===null){const t=e.cameras[0].viewport,i=new Dn({vertexShader:Tm,fragmentShader:wm,uniforms:{depthColor:{value:this.texture},depthWidth:{value:t.z},depthHeight:{value:t.w}}});this.mesh=new Le(new ii(20,20),i)}return this.mesh}reset(){this.texture=null,this.mesh=null}getDepthTexture(){return this.texture}}class Rm extends ki{constructor(e,t){super();const i=this;let r=null,a=1,s=null,o="local-floor",c=1,l=null,d=null,h=null,f=null,m=null,g=null;const _=new Am,p=t.getContextAttributes();let u=null,E=null;const y=[],M=[],D=new We;let A=null;const b=new kt;b.viewport=new rt;const C=new kt;C.viewport=new rt;const v=[b,C],x=new Ku;let P=null,U=null;this.cameraAutoUpdate=!0,this.enabled=!1,this.isPresenting=!1,this.getController=function(X){let J=y[X];return J===void 0&&(J=new Sa,y[X]=J),J.getTargetRaySpace()},this.getControllerGrip=function(X){let J=y[X];return J===void 0&&(J=new Sa,y[X]=J),J.getGripSpace()},this.getHand=function(X){let J=y[X];return J===void 0&&(J=new Sa,y[X]=J),J.getHandSpace()};function w(X){const J=M.indexOf(X.inputSource);if(J===-1)return;const ae=y[J];ae!==void 0&&(ae.update(X.inputSource,X.frame,l||s),ae.dispatchEvent({type:X.type,data:X.inputSource}))}function R(){r.removeEventListener("select",w),r.removeEventListener("selectstart",w),r.removeEventListener("selectend",w),r.removeEventListener("squeeze",w),r.removeEventListener("squeezestart",w),r.removeEventListener("squeezeend",w),r.removeEventListener("end",R),r.removeEventListener("inputsourceschange",z);for(let X=0;X<y.length;X++){const J=M[X];J!==null&&(M[X]=null,y[X].disconnect(J))}P=null,U=null,_.reset(),e.setRenderTarget(u),m=null,f=null,h=null,r=null,E=null,De.stop(),i.isPresenting=!1,e.setPixelRatio(A),e.setSize(D.width,D.height,!1),i.dispatchEvent({type:"sessionend"})}this.setFramebufferScaleFactor=function(X){a=X,i.isPresenting===!0&&console.warn("THREE.WebXRManager: Cannot change framebuffer scale while presenting.")},this.setReferenceSpaceType=function(X){o=X,i.isPresenting===!0&&console.warn("THREE.WebXRManager: Cannot change reference space type while presenting.")},this.getReferenceSpace=function(){return l||s},this.setReferenceSpace=function(X){l=X},this.getBaseLayer=function(){return f!==null?f:m},this.getBinding=function(){return h},this.getFrame=function(){return g},this.getSession=function(){return r},this.setSession=async function(X){if(r=X,r!==null){if(u=e.getRenderTarget(),r.addEventListener("select",w),r.addEventListener("selectstart",w),r.addEventListener("selectend",w),r.addEventListener("squeeze",w),r.addEventListener("squeezestart",w),r.addEventListener("squeezeend",w),r.addEventListener("end",R),r.addEventListener("inputsourceschange",z),p.xrCompatible!==!0&&await t.makeXRCompatible(),A=e.getPixelRatio(),e.getSize(D),typeof XRWebGLBinding<"u"&&"createProjectionLayer"in XRWebGLBinding.prototype){let ae=null,re=null,ue=null;p.depth&&(ue=p.stencil?t.DEPTH24_STENCIL8:t.DEPTH_COMPONENT24,ae=p.stencil?Ii:Ai,re=p.stencil?Li:ei);const Pe={colorFormat:t.RGBA8,depthFormat:ue,scaleFactor:a};h=new XRWebGLBinding(r,t),f=h.createProjectionLayer(Pe),r.updateRenderState({layers:[f]}),e.setPixelRatio(1),e.setSize(f.textureWidth,f.textureHeight,!1),E=new ti(f.textureWidth,f.textureHeight,{format:Ht,type:mn,depthTexture:new tl(f.textureWidth,f.textureHeight,re,void 0,void 0,void 0,void 0,void 0,void 0,ae),stencilBuffer:p.stencil,colorSpace:e.outputColorSpace,samples:p.antialias?4:0,resolveDepthBuffer:f.ignoreDepthValues===!1,resolveStencilBuffer:f.ignoreDepthValues===!1})}else{const ae={antialias:p.antialias,alpha:!0,depth:p.depth,stencil:p.stencil,framebufferScaleFactor:a};m=new XRWebGLLayer(r,t,ae),r.updateRenderState({baseLayer:m}),e.setPixelRatio(1),e.setSize(m.framebufferWidth,m.framebufferHeight,!1),E=new ti(m.framebufferWidth,m.framebufferHeight,{format:Ht,type:mn,colorSpace:e.outputColorSpace,stencilBuffer:p.stencil,resolveDepthBuffer:m.ignoreDepthValues===!1,resolveStencilBuffer:m.ignoreDepthValues===!1})}E.isXRRenderTarget=!0,this.setFoveation(c),l=null,s=await r.requestReferenceSpace(o),De.setContext(r),De.start(),i.isPresenting=!0,i.dispatchEvent({type:"sessionstart"})}},this.getEnvironmentBlendMode=function(){if(r!==null)return r.environmentBlendMode},this.getDepthTexture=function(){return _.getDepthTexture()};function z(X){for(let J=0;J<X.removed.length;J++){const ae=X.removed[J],re=M.indexOf(ae);re>=0&&(M[re]=null,y[re].disconnect(ae))}for(let J=0;J<X.added.length;J++){const ae=X.added[J];let re=M.indexOf(ae);if(re===-1){for(let Pe=0;Pe<y.length;Pe++)if(Pe>=M.length){M.push(ae),re=Pe;break}else if(M[Pe]===null){M[Pe]=ae,re=Pe;break}if(re===-1)break}const ue=y[re];ue&&ue.connect(ae)}}const N=new F,B=new F;function k(X,J,ae){N.setFromMatrixPosition(J.matrixWorld),B.setFromMatrixPosition(ae.matrixWorld);const re=N.distanceTo(B),ue=J.projectionMatrix.elements,Pe=ae.projectionMatrix.elements,fe=ue[14]/(ue[10]-1),te=ue[14]/(ue[10]+1),se=(ue[9]+1)/ue[5],W=(ue[9]-1)/ue[5],L=(ue[8]-1)/ue[0],Ee=(Pe[8]+1)/Pe[0],Se=fe*L,_e=fe*Ee,ve=re/(-L+Ee),Ne=ve*-L;if(J.matrixWorld.decompose(X.position,X.quaternion,X.scale),X.translateX(Ne),X.translateZ(ve),X.matrixWorld.compose(X.position,X.quaternion,X.scale),X.matrixWorldInverse.copy(X.matrixWorld).invert(),ue[10]===-1)X.projectionMatrix.copy(J.projectionMatrix),X.projectionMatrixInverse.copy(J.projectionMatrixInverse);else{const Re=fe+ve,I=te+ve,S=Se-Ne,j=_e+(re-Ne),ee=se*te/I*Re,ie=W*te/I*Re;X.projectionMatrix.makePerspective(S,j,ee,ie,Re,I),X.projectionMatrixInverse.copy(X.projectionMatrix).invert()}}function O(X,J){J===null?X.matrixWorld.copy(X.matrix):X.matrixWorld.multiplyMatrices(J.matrixWorld,X.matrix),X.matrixWorldInverse.copy(X.matrixWorld).invert()}this.updateCamera=function(X){if(r===null)return;let J=X.near,ae=X.far;_.texture!==null&&(_.depthNear>0&&(J=_.depthNear),_.depthFar>0&&(ae=_.depthFar)),x.near=C.near=b.near=J,x.far=C.far=b.far=ae,(P!==x.near||U!==x.far)&&(r.updateRenderState({depthNear:x.near,depthFar:x.far}),P=x.near,U=x.far),b.layers.mask=X.layers.mask|2,C.layers.mask=X.layers.mask|4,x.layers.mask=b.layers.mask|C.layers.mask;const re=X.parent,ue=x.cameras;O(x,re);for(let Pe=0;Pe<ue.length;Pe++)O(ue[Pe],re);ue.length===2?k(x,b,C):x.projectionMatrix.copy(b.projectionMatrix),q(X,x,re)};function q(X,J,ae){ae===null?X.matrix.copy(J.matrixWorld):(X.matrix.copy(ae.matrixWorld),X.matrix.invert(),X.matrix.multiply(J.matrixWorld)),X.matrix.decompose(X.position,X.quaternion,X.scale),X.updateMatrixWorld(!0),X.projectionMatrix.copy(J.projectionMatrix),X.projectionMatrixInverse.copy(J.projectionMatrixInverse),X.isPerspectiveCamera&&(X.fov=bs*2*Math.atan(1/X.projectionMatrix.elements[5]),X.zoom=1)}this.getCamera=function(){return x},this.getFoveation=function(){if(!(f===null&&m===null))return c},this.setFoveation=function(X){c=X,f!==null&&(f.fixedFoveation=X),m!==null&&m.fixedFoveation!==void 0&&(m.fixedFoveation=X)},this.hasDepthSensing=function(){return _.texture!==null},this.getDepthSensingMesh=function(){return _.getMesh(x)};let K=null;function le(X,J){if(d=J.getViewerPose(l||s),g=J,d!==null){const ae=d.views;m!==null&&(e.setRenderTargetFramebuffer(E,m.framebuffer),e.setRenderTarget(E));let re=!1;ae.length!==x.cameras.length&&(x.cameras.length=0,re=!0);for(let fe=0;fe<ae.length;fe++){const te=ae[fe];let se=null;if(m!==null)se=m.getViewport(te);else{const L=h.getViewSubImage(f,te);se=L.viewport,fe===0&&(e.setRenderTargetTextures(E,L.colorTexture,f.ignoreDepthValues?void 0:L.depthStencilTexture),e.setRenderTarget(E))}let W=v[fe];W===void 0&&(W=new kt,W.layers.enable(fe),W.viewport=new rt,v[fe]=W),W.matrix.fromArray(te.transform.matrix),W.matrix.decompose(W.position,W.quaternion,W.scale),W.projectionMatrix.fromArray(te.projectionMatrix),W.projectionMatrixInverse.copy(W.projectionMatrix).invert(),W.viewport.set(se.x,se.y,se.width,se.height),fe===0&&(x.matrix.copy(W.matrix),x.matrix.decompose(x.position,x.quaternion,x.scale)),re===!0&&x.cameras.push(W)}const ue=r.enabledFeatures;if(ue&&ue.includes("depth-sensing")&&r.depthUsage=="gpu-optimized"&&h){const fe=h.getDepthInformation(ae[0]);fe&&fe.isValid&&fe.texture&&_.init(e,fe,r.renderState)}}for(let ae=0;ae<y.length;ae++){const re=M[ae],ue=y[ae];re!==null&&ue!==void 0&&ue.update(re,J,l||s)}K&&K(X,J),J.detectedPlanes&&i.dispatchEvent({type:"planesdetected",data:J}),g=null}const De=new rl;De.setAnimationLoop(le),this.setAnimationLoop=function(X){K=X},this.dispose=function(){}}}const Bn=new xt,Cm=new at;function Pm(n,e){function t(p,u){p.matrixAutoUpdate===!0&&p.updateMatrix(),u.value.copy(p.matrix)}function i(p,u){u.color.getRGB(p.fogColor.value,Zc(n)),u.isFog?(p.fogNear.value=u.near,p.fogFar.value=u.far):u.isFogExp2&&(p.fogDensity.value=u.density)}function r(p,u,E,y,M){u.isMeshBasicMaterial||u.isMeshLambertMaterial?a(p,u):u.isMeshToonMaterial?(a(p,u),h(p,u)):u.isMeshPhongMaterial?(a(p,u),d(p,u)):u.isMeshStandardMaterial?(a(p,u),f(p,u),u.isMeshPhysicalMaterial&&m(p,u,M)):u.isMeshMatcapMaterial?(a(p,u),g(p,u)):u.isMeshDepthMaterial?a(p,u):u.isMeshDistanceMaterial?(a(p,u),_(p,u)):u.isMeshNormalMaterial?a(p,u):u.isLineBasicMaterial?(s(p,u),u.isLineDashedMaterial&&o(p,u)):u.isPointsMaterial?c(p,u,E,y):u.isSpriteMaterial?l(p,u):u.isShadowMaterial?(p.color.value.copy(u.color),p.opacity.value=u.opacity):u.isShaderMaterial&&(u.uniformsNeedUpdate=!1)}function a(p,u){p.opacity.value=u.opacity,u.color&&p.diffuse.value.copy(u.color),u.emissive&&p.emissive.value.copy(u.emissive).multiplyScalar(u.emissiveIntensity),u.map&&(p.map.value=u.map,t(u.map,p.mapTransform)),u.alphaMap&&(p.alphaMap.value=u.alphaMap,t(u.alphaMap,p.alphaMapTransform)),u.bumpMap&&(p.bumpMap.value=u.bumpMap,t(u.bumpMap,p.bumpMapTransform),p.bumpScale.value=u.bumpScale,u.side===Ct&&(p.bumpScale.value*=-1)),u.normalMap&&(p.normalMap.value=u.normalMap,t(u.normalMap,p.normalMapTransform),p.normalScale.value.copy(u.normalScale),u.side===Ct&&p.normalScale.value.negate()),u.displacementMap&&(p.displacementMap.value=u.displacementMap,t(u.displacementMap,p.displacementMapTransform),p.displacementScale.value=u.displacementScale,p.displacementBias.value=u.displacementBias),u.emissiveMap&&(p.emissiveMap.value=u.emissiveMap,t(u.emissiveMap,p.emissiveMapTransform)),u.specularMap&&(p.specularMap.value=u.specularMap,t(u.specularMap,p.specularMapTransform)),u.alphaTest>0&&(p.alphaTest.value=u.alphaTest);const E=e.get(u),y=E.envMap,M=E.envMapRotation;y&&(p.envMap.value=y,Bn.copy(M),Bn.x*=-1,Bn.y*=-1,Bn.z*=-1,y.isCubeTexture&&y.isRenderTargetTexture===!1&&(Bn.y*=-1,Bn.z*=-1),p.envMapRotation.value.setFromMatrix4(Cm.makeRotationFromEuler(Bn)),p.flipEnvMap.value=y.isCubeTexture&&y.isRenderTargetTexture===!1?-1:1,p.reflectivity.value=u.reflectivity,p.ior.value=u.ior,p.refractionRatio.value=u.refractionRatio),u.lightMap&&(p.lightMap.value=u.lightMap,p.lightMapIntensity.value=u.lightMapIntensity,t(u.lightMap,p.lightMapTransform)),u.aoMap&&(p.aoMap.value=u.aoMap,p.aoMapIntensity.value=u.aoMapIntensity,t(u.aoMap,p.aoMapTransform))}function s(p,u){p.diffuse.value.copy(u.color),p.opacity.value=u.opacity,u.map&&(p.map.value=u.map,t(u.map,p.mapTransform))}function o(p,u){p.dashSize.value=u.dashSize,p.totalSize.value=u.dashSize+u.gapSize,p.scale.value=u.scale}function c(p,u,E,y){p.diffuse.value.copy(u.color),p.opacity.value=u.opacity,p.size.value=u.size*E,p.scale.value=y*.5,u.map&&(p.map.value=u.map,t(u.map,p.uvTransform)),u.alphaMap&&(p.alphaMap.value=u.alphaMap,t(u.alphaMap,p.alphaMapTransform)),u.alphaTest>0&&(p.alphaTest.value=u.alphaTest)}function l(p,u){p.diffuse.value.copy(u.color),p.opacity.value=u.opacity,p.rotation.value=u.rotation,u.map&&(p.map.value=u.map,t(u.map,p.mapTransform)),u.alphaMap&&(p.alphaMap.value=u.alphaMap,t(u.alphaMap,p.alphaMapTransform)),u.alphaTest>0&&(p.alphaTest.value=u.alphaTest)}function d(p,u){p.specular.value.copy(u.specular),p.shininess.value=Math.max(u.shininess,1e-4)}function h(p,u){u.gradientMap&&(p.gradientMap.value=u.gradientMap)}function f(p,u){p.metalness.value=u.metalness,u.metalnessMap&&(p.metalnessMap.value=u.metalnessMap,t(u.metalnessMap,p.metalnessMapTransform)),p.roughness.value=u.roughness,u.roughnessMap&&(p.roughnessMap.value=u.roughnessMap,t(u.roughnessMap,p.roughnessMapTransform)),u.envMap&&(p.envMapIntensity.value=u.envMapIntensity)}function m(p,u,E){p.ior.value=u.ior,u.sheen>0&&(p.sheenColor.value.copy(u.sheenColor).multiplyScalar(u.sheen),p.sheenRoughness.value=u.sheenRoughness,u.sheenColorMap&&(p.sheenColorMap.value=u.sheenColorMap,t(u.sheenColorMap,p.sheenColorMapTransform)),u.sheenRoughnessMap&&(p.sheenRoughnessMap.value=u.sheenRoughnessMap,t(u.sheenRoughnessMap,p.sheenRoughnessMapTransform))),u.clearcoat>0&&(p.clearcoat.value=u.clearcoat,p.clearcoatRoughness.value=u.clearcoatRoughness,u.clearcoatMap&&(p.clearcoatMap.value=u.clearcoatMap,t(u.clearcoatMap,p.clearcoatMapTransform)),u.clearcoatRoughnessMap&&(p.clearcoatRoughnessMap.value=u.clearcoatRoughnessMap,t(u.clearcoatRoughnessMap,p.clearcoatRoughnessMapTransform)),u.clearcoatNormalMap&&(p.clearcoatNormalMap.value=u.clearcoatNormalMap,t(u.clearcoatNormalMap,p.clearcoatNormalMapTransform),p.clearcoatNormalScale.value.copy(u.clearcoatNormalScale),u.side===Ct&&p.clearcoatNormalScale.value.negate())),u.dispersion>0&&(p.dispersion.value=u.dispersion),u.iridescence>0&&(p.iridescence.value=u.iridescence,p.iridescenceIOR.value=u.iridescenceIOR,p.iridescenceThicknessMinimum.value=u.iridescenceThicknessRange[0],p.iridescenceThicknessMaximum.value=u.iridescenceThicknessRange[1],u.iridescenceMap&&(p.iridescenceMap.value=u.iridescenceMap,t(u.iridescenceMap,p.iridescenceMapTransform)),u.iridescenceThicknessMap&&(p.iridescenceThicknessMap.value=u.iridescenceThicknessMap,t(u.iridescenceThicknessMap,p.iridescenceThicknessMapTransform))),u.transmission>0&&(p.transmission.value=u.transmission,p.transmissionSamplerMap.value=E.texture,p.transmissionSamplerSize.value.set(E.width,E.height),u.transmissionMap&&(p.transmissionMap.value=u.transmissionMap,t(u.transmissionMap,p.transmissionMapTransform)),p.thickness.value=u.thickness,u.thicknessMap&&(p.thicknessMap.value=u.thicknessMap,t(u.thicknessMap,p.thicknessMapTransform)),p.attenuationDistance.value=u.attenuationDistance,p.attenuationColor.value.copy(u.attenuationColor)),u.anisotropy>0&&(p.anisotropyVector.value.set(u.anisotropy*Math.cos(u.anisotropyRotation),u.anisotropy*Math.sin(u.anisotropyRotation)),u.anisotropyMap&&(p.anisotropyMap.value=u.anisotropyMap,t(u.anisotropyMap,p.anisotropyMapTransform))),p.specularIntensity.value=u.specularIntensity,p.specularColor.value.copy(u.specularColor),u.specularColorMap&&(p.specularColorMap.value=u.specularColorMap,t(u.specularColorMap,p.specularColorMapTransform)),u.specularIntensityMap&&(p.specularIntensityMap.value=u.specularIntensityMap,t(u.specularIntensityMap,p.specularIntensityMapTransform))}function g(p,u){u.matcap&&(p.matcap.value=u.matcap)}function _(p,u){const E=e.get(u).light;p.referencePosition.value.setFromMatrixPosition(E.matrixWorld),p.nearDistance.value=E.shadow.camera.near,p.farDistance.value=E.shadow.camera.far}return{refreshFogUniforms:i,refreshMaterialUniforms:r}}function Dm(n,e,t,i){let r={},a={},s=[];const o=n.getParameter(n.MAX_UNIFORM_BUFFER_BINDINGS);function c(E,y){const M=y.program;i.uniformBlockBinding(E,M)}function l(E,y){let M=r[E.id];M===void 0&&(g(E),M=d(E),r[E.id]=M,E.addEventListener("dispose",p));const D=y.program;i.updateUBOMapping(E,D);const A=e.render.frame;a[E.id]!==A&&(f(E),a[E.id]=A)}function d(E){const y=h();E.__bindingPointIndex=y;const M=n.createBuffer(),D=E.__size,A=E.usage;return n.bindBuffer(n.UNIFORM_BUFFER,M),n.bufferData(n.UNIFORM_BUFFER,D,A),n.bindBuffer(n.UNIFORM_BUFFER,null),n.bindBufferBase(n.UNIFORM_BUFFER,y,M),M}function h(){for(let E=0;E<o;E++)if(s.indexOf(E)===-1)return s.push(E),E;return console.error("THREE.WebGLRenderer: Maximum number of simultaneously usable uniforms groups reached."),0}function f(E){const y=r[E.id],M=E.uniforms,D=E.__cache;n.bindBuffer(n.UNIFORM_BUFFER,y);for(let A=0,b=M.length;A<b;A++){const C=Array.isArray(M[A])?M[A]:[M[A]];for(let v=0,x=C.length;v<x;v++){const P=C[v];if(m(P,A,v,D)===!0){const U=P.__offset,w=Array.isArray(P.value)?P.value:[P.value];let R=0;for(let z=0;z<w.length;z++){const N=w[z],B=_(N);typeof N=="number"||typeof N=="boolean"?(P.__data[0]=N,n.bufferSubData(n.UNIFORM_BUFFER,U+R,P.__data)):N.isMatrix3?(P.__data[0]=N.elements[0],P.__data[1]=N.elements[1],P.__data[2]=N.elements[2],P.__data[3]=0,P.__data[4]=N.elements[3],P.__data[5]=N.elements[4],P.__data[6]=N.elements[5],P.__data[7]=0,P.__data[8]=N.elements[6],P.__data[9]=N.elements[7],P.__data[10]=N.elements[8],P.__data[11]=0):(N.toArray(P.__data,R),R+=B.storage/Float32Array.BYTES_PER_ELEMENT)}n.bufferSubData(n.UNIFORM_BUFFER,U,P.__data)}}}n.bindBuffer(n.UNIFORM_BUFFER,null)}function m(E,y,M,D){const A=E.value,b=y+"_"+M;if(D[b]===void 0)return typeof A=="number"||typeof A=="boolean"?D[b]=A:D[b]=A.clone(),!0;{const C=D[b];if(typeof A=="number"||typeof A=="boolean"){if(C!==A)return D[b]=A,!0}else if(C.equals(A)===!1)return C.copy(A),!0}return!1}function g(E){const y=E.uniforms;let M=0;const D=16;for(let b=0,C=y.length;b<C;b++){const v=Array.isArray(y[b])?y[b]:[y[b]];for(let x=0,P=v.length;x<P;x++){const U=v[x],w=Array.isArray(U.value)?U.value:[U.value];for(let R=0,z=w.length;R<z;R++){const N=w[R],B=_(N),k=M%D,O=k%B.boundary,q=k+O;M+=O,q!==0&&D-q<B.storage&&(M+=D-q),U.__data=new Float32Array(B.storage/Float32Array.BYTES_PER_ELEMENT),U.__offset=M,M+=B.storage}}}const A=M%D;return A>0&&(M+=D-A),E.__size=M,E.__cache={},this}function _(E){const y={boundary:0,storage:0};return typeof E=="number"||typeof E=="boolean"?(y.boundary=4,y.storage=4):E.isVector2?(y.boundary=8,y.storage=8):E.isVector3||E.isColor?(y.boundary=16,y.storage=12):E.isVector4?(y.boundary=16,y.storage=16):E.isMatrix3?(y.boundary=48,y.storage=48):E.isMatrix4?(y.boundary=64,y.storage=64):E.isTexture?console.warn("THREE.WebGLRenderer: Texture samplers can not be part of an uniforms group."):console.warn("THREE.WebGLRenderer: Unsupported uniform value type.",E),y}function p(E){const y=E.target;y.removeEventListener("dispose",p);const M=s.indexOf(y.__bindingPointIndex);s.splice(M,1),n.deleteBuffer(r[y.id]),delete r[y.id],delete a[y.id]}function u(){for(const E in r)n.deleteBuffer(r[E]);s=[],r={},a={}}return{bind:c,update:l,dispose:u}}class Lm{constructor(e={}){const{canvas:t=cu(),context:i=null,depth:r=!0,stencil:a=!1,alpha:s=!1,antialias:o=!1,premultipliedAlpha:c=!0,preserveDrawingBuffer:l=!1,powerPreference:d="default",failIfMajorPerformanceCaveat:h=!1,reverseDepthBuffer:f=!1}=e;this.isWebGLRenderer=!0;let m;if(i!==null){if(typeof WebGLRenderingContext<"u"&&i instanceof WebGLRenderingContext)throw new Error("THREE.WebGLRenderer: WebGL 1 is not supported since r163.");m=i.getContextAttributes().alpha}else m=s;const g=new Uint32Array(4),_=new Int32Array(4);let p=null,u=null;const E=[],y=[];this.domElement=t,this.debug={checkShaderErrors:!0,onShaderError:null},this.autoClear=!0,this.autoClearColor=!0,this.autoClearDepth=!0,this.autoClearStencil=!0,this.sortObjects=!0,this.clippingPlanes=[],this.localClippingEnabled=!1,this._outputColorSpace=Nt,this.toneMapping=Cn,this.toneMappingExposure=1;const M=this;let D=!1,A=0,b=0,C=null,v=-1,x=null;const P=new rt,U=new rt;let w=null;const R=new oe(0);let z=0,N=t.width,B=t.height,k=1,O=null,q=null;const K=new rt(0,0,N,B),le=new rt(0,0,N,B);let De=!1;const X=new js;let J=!1,ae=!1;this.transmissionResolutionScale=1;const re=new at,ue=new at,Pe=new F,fe=new rt,te={background:null,fog:null,environment:null,overrideMaterial:null,isScene:!0};let se=!1;function W(){return C===null?k:1}let L=i;function Ee(T,G){return t.getContext(T,G)}try{const T={alpha:!0,depth:r,stencil:a,antialias:o,premultipliedAlpha:c,preserveDrawingBuffer:l,powerPreference:d,failIfMajorPerformanceCaveat:h};if("setAttribute"in t&&t.setAttribute("data-engine",`three.js r${Us}`),t.addEventListener("webglcontextlost",ne,!1),t.addEventListener("webglcontextrestored",Me,!1),t.addEventListener("webglcontextcreationerror",xe,!1),L===null){const G="webgl2";if(L=Ee(G,T),L===null)throw Ee(G)?new Error("Error creating WebGL context with your selected attributes."):new Error("Error creating WebGL context.")}}catch(T){throw console.error("THREE.WebGLRenderer: "+T.message),T}let Se,_e,ve,Ne,Re,I,S,j,ee,ie,Q,Ce,ge,be,$e,de,Te,ze,ke,we,Ke,Ge,st,V;function pe(){Se=new Gf(L),Se.init(),Ge=new bm(L,Se),_e=new zf(L,Se,e,Ge),ve=new Em(L,Se),_e.reverseDepthBuffer&&f&&ve.buffers.depth.setReversed(!0),Ne=new Wf(L),Re=new lm,I=new ym(L,Se,ve,Re,_e,Ge,Ne),S=new kf(M),j=new Vf(M),ee=new Yu(L),st=new If(L,ee),ie=new Hf(L,ee,Ne,st),Q=new qf(L,ie,ee,Ne),ke=new Xf(L,_e,I),de=new Nf(Re),Ce=new cm(M,S,j,Se,_e,st,de),ge=new Pm(M,Re),be=new dm,$e=new _m(Se),ze=new Lf(M,S,j,ve,Q,m,c),Te=new Mm(M,Q,_e),V=new Dm(L,Ne,_e,ve),we=new Uf(L,Se,Ne),Ke=new jf(L,Se,Ne),Ne.programs=Ce.programs,M.capabilities=_e,M.extensions=Se,M.properties=Re,M.renderLists=be,M.shadowMap=Te,M.state=ve,M.info=Ne}pe();const Z=new Rm(M,L);this.xr=Z,this.getContext=function(){return L},this.getContextAttributes=function(){return L.getContextAttributes()},this.forceContextLoss=function(){const T=Se.get("WEBGL_lose_context");T&&T.loseContext()},this.forceContextRestore=function(){const T=Se.get("WEBGL_lose_context");T&&T.restoreContext()},this.getPixelRatio=function(){return k},this.setPixelRatio=function(T){T!==void 0&&(k=T,this.setSize(N,B,!1))},this.getSize=function(T){return T.set(N,B)},this.setSize=function(T,G,$=!0){if(Z.isPresenting){console.warn("THREE.WebGLRenderer: Can't change size while VR device is presenting.");return}N=T,B=G,t.width=Math.floor(T*k),t.height=Math.floor(G*k),$===!0&&(t.style.width=T+"px",t.style.height=G+"px"),this.setViewport(0,0,T,G)},this.getDrawingBufferSize=function(T){return T.set(N*k,B*k).floor()},this.setDrawingBufferSize=function(T,G,$){N=T,B=G,k=$,t.width=Math.floor(T*$),t.height=Math.floor(G*$),this.setViewport(0,0,T,G)},this.getCurrentViewport=function(T){return T.copy(P)},this.getViewport=function(T){return T.copy(K)},this.setViewport=function(T,G,$,Y){T.isVector4?K.set(T.x,T.y,T.z,T.w):K.set(T,G,$,Y),ve.viewport(P.copy(K).multiplyScalar(k).round())},this.getScissor=function(T){return T.copy(le)},this.setScissor=function(T,G,$,Y){T.isVector4?le.set(T.x,T.y,T.z,T.w):le.set(T,G,$,Y),ve.scissor(U.copy(le).multiplyScalar(k).round())},this.getScissorTest=function(){return De},this.setScissorTest=function(T){ve.setScissorTest(De=T)},this.setOpaqueSort=function(T){O=T},this.setTransparentSort=function(T){q=T},this.getClearColor=function(T){return T.copy(ze.getClearColor())},this.setClearColor=function(){ze.setClearColor(...arguments)},this.getClearAlpha=function(){return ze.getClearAlpha()},this.setClearAlpha=function(){ze.setClearAlpha(...arguments)},this.clear=function(T=!0,G=!0,$=!0){let Y=0;if(T){let H=!1;if(C!==null){const ce=C.texture.format;H=ce===Bs||ce===Os||ce===Fs}if(H){const ce=C.texture.type,me=ce===mn||ce===ei||ce===Ji||ce===Li||ce===Ns||ce===ks,ye=ze.getClearColor(),Ae=ze.getClearAlpha(),Fe=ye.r,Oe=ye.g,Ie=ye.b;me?(g[0]=Fe,g[1]=Oe,g[2]=Ie,g[3]=Ae,L.clearBufferuiv(L.COLOR,0,g)):(_[0]=Fe,_[1]=Oe,_[2]=Ie,_[3]=Ae,L.clearBufferiv(L.COLOR,0,_))}else Y|=L.COLOR_BUFFER_BIT}G&&(Y|=L.DEPTH_BUFFER_BIT),$&&(Y|=L.STENCIL_BUFFER_BIT,this.state.buffers.stencil.setMask(4294967295)),L.clear(Y)},this.clearColor=function(){this.clear(!0,!1,!1)},this.clearDepth=function(){this.clear(!1,!0,!1)},this.clearStencil=function(){this.clear(!1,!1,!0)},this.dispose=function(){t.removeEventListener("webglcontextlost",ne,!1),t.removeEventListener("webglcontextrestored",Me,!1),t.removeEventListener("webglcontextcreationerror",xe,!1),ze.dispose(),be.dispose(),$e.dispose(),Re.dispose(),S.dispose(),j.dispose(),Q.dispose(),st.dispose(),V.dispose(),Ce.dispose(),Z.dispose(),Z.removeEventListener("sessionstart",Zs),Z.removeEventListener("sessionend",Js),In.stop()};function ne(T){T.preventDefault(),console.log("THREE.WebGLRenderer: Context Lost."),D=!0}function Me(){console.log("THREE.WebGLRenderer: Context Restored."),D=!1;const T=Ne.autoReset,G=Te.enabled,$=Te.autoUpdate,Y=Te.needsUpdate,H=Te.type;pe(),Ne.autoReset=T,Te.enabled=G,Te.autoUpdate=$,Te.needsUpdate=Y,Te.type=H}function xe(T){console.error("THREE.WebGLRenderer: A WebGL context could not be created. Reason: ",T.statusMessage)}function Be(T){const G=T.target;G.removeEventListener("dispose",Be),dt(G)}function dt(T){yt(T),Re.remove(T)}function yt(T){const G=Re.get(T).programs;G!==void 0&&(G.forEach(function($){Ce.releaseProgram($)}),T.isShaderMaterial&&Ce.releaseShaderCache(T))}this.renderBufferDirect=function(T,G,$,Y,H,ce){G===null&&(G=te);const me=H.isMesh&&H.matrixWorld.determinant()<0,ye=dl(T,G,$,Y,H);ve.setMaterial(Y,me);let Ae=$.index,Fe=1;if(Y.wireframe===!0){if(Ae=ie.getWireframeAttribute($),Ae===void 0)return;Fe=2}const Oe=$.drawRange,Ie=$.attributes.position;let Ye=Oe.start*Fe,et=(Oe.start+Oe.count)*Fe;ce!==null&&(Ye=Math.max(Ye,ce.start*Fe),et=Math.min(et,(ce.start+ce.count)*Fe)),Ae!==null?(Ye=Math.max(Ye,0),et=Math.min(et,Ae.count)):Ie!=null&&(Ye=Math.max(Ye,0),et=Math.min(et,Ie.count));const pt=et-Ye;if(pt<0||pt===1/0)return;st.setup(H,Y,ye,$,Ae);let ht,Ze=we;if(Ae!==null&&(ht=ee.get(Ae),Ze=Ke,Ze.setIndex(ht)),H.isMesh)Y.wireframe===!0?(ve.setLineWidth(Y.wireframeLinewidth*W()),Ze.setMode(L.LINES)):Ze.setMode(L.TRIANGLES);else if(H.isLine){let Ue=Y.linewidth;Ue===void 0&&(Ue=1),ve.setLineWidth(Ue*W()),H.isLineSegments?Ze.setMode(L.LINES):H.isLineLoop?Ze.setMode(L.LINE_LOOP):Ze.setMode(L.LINE_STRIP)}else H.isPoints?Ze.setMode(L.POINTS):H.isSprite&&Ze.setMode(L.TRIANGLES);if(H.isBatchedMesh)if(H._multiDrawInstances!==null)Vn("THREE.WebGLRenderer: renderMultiDrawInstances has been deprecated and will be removed in r184. Append to renderMultiDraw arguments and use indirection."),Ze.renderMultiDrawInstances(H._multiDrawStarts,H._multiDrawCounts,H._multiDrawCount,H._multiDrawInstances);else if(Se.get("WEBGL_multi_draw"))Ze.renderMultiDraw(H._multiDrawStarts,H._multiDrawCounts,H._multiDrawCount);else{const Ue=H._multiDrawStarts,Mt=H._multiDrawCounts,tt=H._multiDrawCount,Wt=Ae?ee.get(Ae).bytesPerElement:1,ri=Re.get(Y).currentProgram.getUniforms();for(let It=0;It<tt;It++)ri.setValue(L,"_gl_DrawID",It),Ze.render(Ue[It]/Wt,Mt[It])}else if(H.isInstancedMesh)Ze.renderInstances(Ye,pt,H.count);else if($.isInstancedBufferGeometry){const Ue=$._maxInstanceCount!==void 0?$._maxInstanceCount:1/0,Mt=Math.min($.instanceCount,Ue);Ze.renderInstances(Ye,pt,Mt)}else Ze.render(Ye,pt)};function nt(T,G,$){T.transparent===!0&&T.side===St&&T.forceSinglePass===!1?(T.side=Ct,T.needsUpdate=!0,or(T,G,$),T.side=Pn,T.needsUpdate=!0,or(T,G,$),T.side=St):or(T,G,$)}this.compile=function(T,G,$=null){$===null&&($=T),u=$e.get($),u.init(G),y.push(u),$.traverseVisible(function(H){H.isLight&&H.layers.test(G.layers)&&(u.pushLight(H),H.castShadow&&u.pushShadow(H))}),T!==$&&T.traverseVisible(function(H){H.isLight&&H.layers.test(G.layers)&&(u.pushLight(H),H.castShadow&&u.pushShadow(H))}),u.setupLights();const Y=new Set;return T.traverse(function(H){if(!(H.isMesh||H.isPoints||H.isLine||H.isSprite))return;const ce=H.material;if(ce)if(Array.isArray(ce))for(let me=0;me<ce.length;me++){const ye=ce[me];nt(ye,$,H),Y.add(ye)}else nt(ce,$,H),Y.add(ce)}),u=y.pop(),Y},this.compileAsync=function(T,G,$=null){const Y=this.compile(T,G,$);return new Promise(H=>{function ce(){if(Y.forEach(function(me){Re.get(me).currentProgram.isReady()&&Y.delete(me)}),Y.size===0){H(T);return}setTimeout(ce,10)}Se.get("KHR_parallel_shader_compile")!==null?ce():setTimeout(ce,10)})};let jt=null;function tn(T){jt&&jt(T)}function Zs(){In.stop()}function Js(){In.start()}const In=new rl;In.setAnimationLoop(tn),typeof self<"u"&&In.setContext(self),this.setAnimationLoop=function(T){jt=T,Z.setAnimationLoop(T),T===null?In.stop():In.start()},Z.addEventListener("sessionstart",Zs),Z.addEventListener("sessionend",Js),this.render=function(T,G){if(G!==void 0&&G.isCamera!==!0){console.error("THREE.WebGLRenderer.render: camera is not an instance of THREE.Camera.");return}if(D===!0)return;if(T.matrixWorldAutoUpdate===!0&&T.updateMatrixWorld(),G.parent===null&&G.matrixWorldAutoUpdate===!0&&G.updateMatrixWorld(),Z.enabled===!0&&Z.isPresenting===!0&&(Z.cameraAutoUpdate===!0&&Z.updateCamera(G),G=Z.getCamera()),T.isScene===!0&&T.onBeforeRender(M,T,G,C),u=$e.get(T,y.length),u.init(G),y.push(u),ue.multiplyMatrices(G.projectionMatrix,G.matrixWorldInverse),X.setFromProjectionMatrix(ue),ae=this.localClippingEnabled,J=de.init(this.clippingPlanes,ae),p=be.get(T,E.length),p.init(),E.push(p),Z.enabled===!0&&Z.isPresenting===!0){const ce=M.xr.getDepthSensingMesh();ce!==null&&Jr(ce,G,-1/0,M.sortObjects)}Jr(T,G,0,M.sortObjects),p.finish(),M.sortObjects===!0&&p.sort(O,q),se=Z.enabled===!1||Z.isPresenting===!1||Z.hasDepthSensing()===!1,se&&ze.addToRenderList(p,T),this.info.render.frame++,J===!0&&de.beginShadows();const $=u.state.shadowsArray;Te.render($,T,G),J===!0&&de.endShadows(),this.info.autoReset===!0&&this.info.reset();const Y=p.opaque,H=p.transmissive;if(u.setupLights(),G.isArrayCamera){const ce=G.cameras;if(H.length>0)for(let me=0,ye=ce.length;me<ye;me++){const Ae=ce[me];eo(Y,H,T,Ae)}se&&ze.render(T);for(let me=0,ye=ce.length;me<ye;me++){const Ae=ce[me];Qs(p,T,Ae,Ae.viewport)}}else H.length>0&&eo(Y,H,T,G),se&&ze.render(T),Qs(p,T,G);C!==null&&b===0&&(I.updateMultisampleRenderTarget(C),I.updateRenderTargetMipmap(C)),T.isScene===!0&&T.onAfterRender(M,T,G),st.resetDefaultState(),v=-1,x=null,y.pop(),y.length>0?(u=y[y.length-1],J===!0&&de.setGlobalState(M.clippingPlanes,u.state.camera)):u=null,E.pop(),E.length>0?p=E[E.length-1]:p=null};function Jr(T,G,$,Y){if(T.visible===!1)return;if(T.layers.test(G.layers)){if(T.isGroup)$=T.renderOrder;else if(T.isLOD)T.autoUpdate===!0&&T.update(G);else if(T.isLight)u.pushLight(T),T.castShadow&&u.pushShadow(T);else if(T.isSprite){if(!T.frustumCulled||X.intersectsSprite(T)){Y&&fe.setFromMatrixPosition(T.matrixWorld).applyMatrix4(ue);const me=Q.update(T),ye=T.material;ye.visible&&p.push(T,me,ye,$,fe.z,null)}}else if((T.isMesh||T.isLine||T.isPoints)&&(!T.frustumCulled||X.intersectsObject(T))){const me=Q.update(T),ye=T.material;if(Y&&(T.boundingSphere!==void 0?(T.boundingSphere===null&&T.computeBoundingSphere(),fe.copy(T.boundingSphere.center)):(me.boundingSphere===null&&me.computeBoundingSphere(),fe.copy(me.boundingSphere.center)),fe.applyMatrix4(T.matrixWorld).applyMatrix4(ue)),Array.isArray(ye)){const Ae=me.groups;for(let Fe=0,Oe=Ae.length;Fe<Oe;Fe++){const Ie=Ae[Fe],Ye=ye[Ie.materialIndex];Ye&&Ye.visible&&p.push(T,me,Ye,$,fe.z,Ie)}}else ye.visible&&p.push(T,me,ye,$,fe.z,null)}}const ce=T.children;for(let me=0,ye=ce.length;me<ye;me++)Jr(ce[me],G,$,Y)}function Qs(T,G,$,Y){const H=T.opaque,ce=T.transmissive,me=T.transparent;u.setupLightsView($),J===!0&&de.setGlobalState(M.clippingPlanes,$),Y&&ve.viewport(P.copy(Y)),H.length>0&&sr(H,G,$),ce.length>0&&sr(ce,G,$),me.length>0&&sr(me,G,$),ve.buffers.depth.setTest(!0),ve.buffers.depth.setMask(!0),ve.buffers.color.setMask(!0),ve.setPolygonOffset(!1)}function eo(T,G,$,Y){if(($.isScene===!0?$.overrideMaterial:null)!==null)return;u.state.transmissionRenderTarget[Y.id]===void 0&&(u.state.transmissionRenderTarget[Y.id]=new ti(1,1,{generateMipmaps:!0,type:Se.has("EXT_color_buffer_half_float")||Se.has("EXT_color_buffer_float")?ir:mn,minFilter:Yn,samples:4,stencilBuffer:a,resolveDepthBuffer:!1,resolveStencilBuffer:!1,colorSpace:Je.workingColorSpace}));const ce=u.state.transmissionRenderTarget[Y.id],me=Y.viewport||P;ce.setSize(me.z*M.transmissionResolutionScale,me.w*M.transmissionResolutionScale);const ye=M.getRenderTarget();M.setRenderTarget(ce),M.getClearColor(R),z=M.getClearAlpha(),z<1&&M.setClearColor(16777215,.5),M.clear(),se&&ze.render($);const Ae=M.toneMapping;M.toneMapping=Cn;const Fe=Y.viewport;if(Y.viewport!==void 0&&(Y.viewport=void 0),u.setupLightsView(Y),J===!0&&de.setGlobalState(M.clippingPlanes,Y),sr(T,$,Y),I.updateMultisampleRenderTarget(ce),I.updateRenderTargetMipmap(ce),Se.has("WEBGL_multisampled_render_to_texture")===!1){let Oe=!1;for(let Ie=0,Ye=G.length;Ie<Ye;Ie++){const et=G[Ie],pt=et.object,ht=et.geometry,Ze=et.material,Ue=et.group;if(Ze.side===St&&pt.layers.test(Y.layers)){const Mt=Ze.side;Ze.side=Ct,Ze.needsUpdate=!0,to(pt,$,Y,ht,Ze,Ue),Ze.side=Mt,Ze.needsUpdate=!0,Oe=!0}}Oe===!0&&(I.updateMultisampleRenderTarget(ce),I.updateRenderTargetMipmap(ce))}M.setRenderTarget(ye),M.setClearColor(R,z),Fe!==void 0&&(Y.viewport=Fe),M.toneMapping=Ae}function sr(T,G,$){const Y=G.isScene===!0?G.overrideMaterial:null;for(let H=0,ce=T.length;H<ce;H++){const me=T[H],ye=me.object,Ae=me.geometry,Fe=Y===null?me.material:Y,Oe=me.group;ye.layers.test($.layers)&&to(ye,G,$,Ae,Fe,Oe)}}function to(T,G,$,Y,H,ce){T.onBeforeRender(M,G,$,Y,H,ce),T.modelViewMatrix.multiplyMatrices($.matrixWorldInverse,T.matrixWorld),T.normalMatrix.getNormalMatrix(T.modelViewMatrix),H.onBeforeRender(M,G,$,Y,T,ce),H.transparent===!0&&H.side===St&&H.forceSinglePass===!1?(H.side=Ct,H.needsUpdate=!0,M.renderBufferDirect($,G,Y,H,T,ce),H.side=Pn,H.needsUpdate=!0,M.renderBufferDirect($,G,Y,H,T,ce),H.side=St):M.renderBufferDirect($,G,Y,H,T,ce),T.onAfterRender(M,G,$,Y,H,ce)}function or(T,G,$){G.isScene!==!0&&(G=te);const Y=Re.get(T),H=u.state.lights,ce=u.state.shadowsArray,me=H.state.version,ye=Ce.getParameters(T,H.state,ce,G,$),Ae=Ce.getProgramCacheKey(ye);let Fe=Y.programs;Y.environment=T.isMeshStandardMaterial?G.environment:null,Y.fog=G.fog,Y.envMap=(T.isMeshStandardMaterial?j:S).get(T.envMap||Y.environment),Y.envMapRotation=Y.environment!==null&&T.envMap===null?G.environmentRotation:T.envMapRotation,Fe===void 0&&(T.addEventListener("dispose",Be),Fe=new Map,Y.programs=Fe);let Oe=Fe.get(Ae);if(Oe!==void 0){if(Y.currentProgram===Oe&&Y.lightsStateVersion===me)return io(T,ye),Oe}else ye.uniforms=Ce.getUniforms(T),T.onBeforeCompile(ye,M),Oe=Ce.acquireProgram(ye,Ae),Fe.set(Ae,Oe),Y.uniforms=ye.uniforms;const Ie=Y.uniforms;return(!T.isShaderMaterial&&!T.isRawShaderMaterial||T.clipping===!0)&&(Ie.clippingPlanes=de.uniform),io(T,ye),Y.needsLights=fl(T),Y.lightsStateVersion=me,Y.needsLights&&(Ie.ambientLightColor.value=H.state.ambient,Ie.lightProbe.value=H.state.probe,Ie.directionalLights.value=H.state.directional,Ie.directionalLightShadows.value=H.state.directionalShadow,Ie.spotLights.value=H.state.spot,Ie.spotLightShadows.value=H.state.spotShadow,Ie.rectAreaLights.value=H.state.rectArea,Ie.ltc_1.value=H.state.rectAreaLTC1,Ie.ltc_2.value=H.state.rectAreaLTC2,Ie.pointLights.value=H.state.point,Ie.pointLightShadows.value=H.state.pointShadow,Ie.hemisphereLights.value=H.state.hemi,Ie.directionalShadowMap.value=H.state.directionalShadowMap,Ie.directionalShadowMatrix.value=H.state.directionalShadowMatrix,Ie.spotShadowMap.value=H.state.spotShadowMap,Ie.spotLightMatrix.value=H.state.spotLightMatrix,Ie.spotLightMap.value=H.state.spotLightMap,Ie.pointShadowMap.value=H.state.pointShadowMap,Ie.pointShadowMatrix.value=H.state.pointShadowMatrix),Y.currentProgram=Oe,Y.uniformsList=null,Oe}function no(T){if(T.uniformsList===null){const G=T.currentProgram.getUniforms();T.uniformsList=Vr.seqWithValue(G.seq,T.uniforms)}return T.uniformsList}function io(T,G){const $=Re.get(T);$.outputColorSpace=G.outputColorSpace,$.batching=G.batching,$.batchingColor=G.batchingColor,$.instancing=G.instancing,$.instancingColor=G.instancingColor,$.instancingMorph=G.instancingMorph,$.skinning=G.skinning,$.morphTargets=G.morphTargets,$.morphNormals=G.morphNormals,$.morphColors=G.morphColors,$.morphTargetsCount=G.morphTargetsCount,$.numClippingPlanes=G.numClippingPlanes,$.numIntersection=G.numClipIntersection,$.vertexAlphas=G.vertexAlphas,$.vertexTangents=G.vertexTangents,$.toneMapping=G.toneMapping}function dl(T,G,$,Y,H){G.isScene!==!0&&(G=te),I.resetTextureUnits();const ce=G.fog,me=Y.isMeshStandardMaterial?G.environment:null,ye=C===null?M.outputColorSpace:C.isXRRenderTarget===!0?C.texture.colorSpace:Ui,Ae=(Y.isMeshStandardMaterial?j:S).get(Y.envMap||me),Fe=Y.vertexColors===!0&&!!$.attributes.color&&$.attributes.color.itemSize===4,Oe=!!$.attributes.tangent&&(!!Y.normalMap||Y.anisotropy>0),Ie=!!$.morphAttributes.position,Ye=!!$.morphAttributes.normal,et=!!$.morphAttributes.color;let pt=Cn;Y.toneMapped&&(C===null||C.isXRRenderTarget===!0)&&(pt=M.toneMapping);const ht=$.morphAttributes.position||$.morphAttributes.normal||$.morphAttributes.color,Ze=ht!==void 0?ht.length:0,Ue=Re.get(Y),Mt=u.state.lights;if(J===!0&&(ae===!0||T!==x)){const At=T===x&&Y.id===v;de.setState(Y,T,At)}let tt=!1;Y.version===Ue.__version?(Ue.needsLights&&Ue.lightsStateVersion!==Mt.state.version||Ue.outputColorSpace!==ye||H.isBatchedMesh&&Ue.batching===!1||!H.isBatchedMesh&&Ue.batching===!0||H.isBatchedMesh&&Ue.batchingColor===!0&&H.colorTexture===null||H.isBatchedMesh&&Ue.batchingColor===!1&&H.colorTexture!==null||H.isInstancedMesh&&Ue.instancing===!1||!H.isInstancedMesh&&Ue.instancing===!0||H.isSkinnedMesh&&Ue.skinning===!1||!H.isSkinnedMesh&&Ue.skinning===!0||H.isInstancedMesh&&Ue.instancingColor===!0&&H.instanceColor===null||H.isInstancedMesh&&Ue.instancingColor===!1&&H.instanceColor!==null||H.isInstancedMesh&&Ue.instancingMorph===!0&&H.morphTexture===null||H.isInstancedMesh&&Ue.instancingMorph===!1&&H.morphTexture!==null||Ue.envMap!==Ae||Y.fog===!0&&Ue.fog!==ce||Ue.numClippingPlanes!==void 0&&(Ue.numClippingPlanes!==de.numPlanes||Ue.numIntersection!==de.numIntersection)||Ue.vertexAlphas!==Fe||Ue.vertexTangents!==Oe||Ue.morphTargets!==Ie||Ue.morphNormals!==Ye||Ue.morphColors!==et||Ue.toneMapping!==pt||Ue.morphTargetsCount!==Ze)&&(tt=!0):(tt=!0,Ue.__version=Y.version);let Wt=Ue.currentProgram;tt===!0&&(Wt=or(Y,G,H));let ri=!1,It=!1,Gi=!1;const ct=Wt.getUniforms(),Ot=Ue.uniforms;if(ve.useProgram(Wt.program)&&(ri=!0,It=!0,Gi=!0),Y.id!==v&&(v=Y.id,It=!0),ri||x!==T){ve.buffers.depth.getReversed()?(re.copy(T.projectionMatrix),uu(re),du(re),ct.setValue(L,"projectionMatrix",re)):ct.setValue(L,"projectionMatrix",T.projectionMatrix),ct.setValue(L,"viewMatrix",T.matrixWorldInverse);const Dt=ct.map.cameraPosition;Dt!==void 0&&Dt.setValue(L,Pe.setFromMatrixPosition(T.matrixWorld)),_e.logarithmicDepthBuffer&&ct.setValue(L,"logDepthBufFC",2/(Math.log(T.far+1)/Math.LN2)),(Y.isMeshPhongMaterial||Y.isMeshToonMaterial||Y.isMeshLambertMaterial||Y.isMeshBasicMaterial||Y.isMeshStandardMaterial||Y.isShaderMaterial)&&ct.setValue(L,"isOrthographic",T.isOrthographicCamera===!0),x!==T&&(x=T,It=!0,Gi=!0)}if(H.isSkinnedMesh){ct.setOptional(L,H,"bindMatrix"),ct.setOptional(L,H,"bindMatrixInverse");const At=H.skeleton;At&&(At.boneTexture===null&&At.computeBoneTexture(),ct.setValue(L,"boneTexture",At.boneTexture,I))}H.isBatchedMesh&&(ct.setOptional(L,H,"batchingTexture"),ct.setValue(L,"batchingTexture",H._matricesTexture,I),ct.setOptional(L,H,"batchingIdTexture"),ct.setValue(L,"batchingIdTexture",H._indirectTexture,I),ct.setOptional(L,H,"batchingColorTexture"),H._colorsTexture!==null&&ct.setValue(L,"batchingColorTexture",H._colorsTexture,I));const Bt=$.morphAttributes;if((Bt.position!==void 0||Bt.normal!==void 0||Bt.color!==void 0)&&ke.update(H,$,Wt),(It||Ue.receiveShadow!==H.receiveShadow)&&(Ue.receiveShadow=H.receiveShadow,ct.setValue(L,"receiveShadow",H.receiveShadow)),Y.isMeshGouraudMaterial&&Y.envMap!==null&&(Ot.envMap.value=Ae,Ot.flipEnvMap.value=Ae.isCubeTexture&&Ae.isRenderTargetTexture===!1?-1:1),Y.isMeshStandardMaterial&&Y.envMap===null&&G.environment!==null&&(Ot.envMapIntensity.value=G.environmentIntensity),It&&(ct.setValue(L,"toneMappingExposure",M.toneMappingExposure),Ue.needsLights&&hl(Ot,Gi),ce&&Y.fog===!0&&ge.refreshFogUniforms(Ot,ce),ge.refreshMaterialUniforms(Ot,Y,k,B,u.state.transmissionRenderTarget[T.id]),Vr.upload(L,no(Ue),Ot,I)),Y.isShaderMaterial&&Y.uniformsNeedUpdate===!0&&(Vr.upload(L,no(Ue),Ot,I),Y.uniformsNeedUpdate=!1),Y.isSpriteMaterial&&ct.setValue(L,"center",H.center),ct.setValue(L,"modelViewMatrix",H.modelViewMatrix),ct.setValue(L,"normalMatrix",H.normalMatrix),ct.setValue(L,"modelMatrix",H.matrixWorld),Y.isShaderMaterial||Y.isRawShaderMaterial){const At=Y.uniformsGroups;for(let Dt=0,Qr=At.length;Dt<Qr;Dt++){const Un=At[Dt];V.update(Un,Wt),V.bind(Un,Wt)}}return Wt}function hl(T,G){T.ambientLightColor.needsUpdate=G,T.lightProbe.needsUpdate=G,T.directionalLights.needsUpdate=G,T.directionalLightShadows.needsUpdate=G,T.pointLights.needsUpdate=G,T.pointLightShadows.needsUpdate=G,T.spotLights.needsUpdate=G,T.spotLightShadows.needsUpdate=G,T.rectAreaLights.needsUpdate=G,T.hemisphereLights.needsUpdate=G}function fl(T){return T.isMeshLambertMaterial||T.isMeshToonMaterial||T.isMeshPhongMaterial||T.isMeshStandardMaterial||T.isShadowMaterial||T.isShaderMaterial&&T.lights===!0}this.getActiveCubeFace=function(){return A},this.getActiveMipmapLevel=function(){return b},this.getRenderTarget=function(){return C},this.setRenderTargetTextures=function(T,G,$){Re.get(T.texture).__webglTexture=G,Re.get(T.depthTexture).__webglTexture=$;const Y=Re.get(T);Y.__hasExternalTextures=!0,Y.__autoAllocateDepthBuffer=$===void 0,Y.__autoAllocateDepthBuffer||Se.has("WEBGL_multisampled_render_to_texture")===!0&&(console.warn("THREE.WebGLRenderer: Render-to-texture extension was disabled because an external texture was provided"),Y.__useRenderToTexture=!1)},this.setRenderTargetFramebuffer=function(T,G){const $=Re.get(T);$.__webglFramebuffer=G,$.__useDefaultFramebuffer=G===void 0};const pl=L.createFramebuffer();this.setRenderTarget=function(T,G=0,$=0){C=T,A=G,b=$;let Y=!0,H=null,ce=!1,me=!1;if(T){const Ae=Re.get(T);if(Ae.__useDefaultFramebuffer!==void 0)ve.bindFramebuffer(L.FRAMEBUFFER,null),Y=!1;else if(Ae.__webglFramebuffer===void 0)I.setupRenderTarget(T);else if(Ae.__hasExternalTextures)I.rebindTextures(T,Re.get(T.texture).__webglTexture,Re.get(T.depthTexture).__webglTexture);else if(T.depthBuffer){const Ie=T.depthTexture;if(Ae.__boundDepthTexture!==Ie){if(Ie!==null&&Re.has(Ie)&&(T.width!==Ie.image.width||T.height!==Ie.image.height))throw new Error("WebGLRenderTarget: Attached DepthTexture is initialized to the incorrect size.");I.setupDepthRenderbuffer(T)}}const Fe=T.texture;(Fe.isData3DTexture||Fe.isDataArrayTexture||Fe.isCompressedArrayTexture)&&(me=!0);const Oe=Re.get(T).__webglFramebuffer;T.isWebGLCubeRenderTarget?(Array.isArray(Oe[G])?H=Oe[G][$]:H=Oe[G],ce=!0):T.samples>0&&I.useMultisampledRTT(T)===!1?H=Re.get(T).__webglMultisampledFramebuffer:Array.isArray(Oe)?H=Oe[$]:H=Oe,P.copy(T.viewport),U.copy(T.scissor),w=T.scissorTest}else P.copy(K).multiplyScalar(k).floor(),U.copy(le).multiplyScalar(k).floor(),w=De;if($!==0&&(H=pl),ve.bindFramebuffer(L.FRAMEBUFFER,H)&&Y&&ve.drawBuffers(T,H),ve.viewport(P),ve.scissor(U),ve.setScissorTest(w),ce){const Ae=Re.get(T.texture);L.framebufferTexture2D(L.FRAMEBUFFER,L.COLOR_ATTACHMENT0,L.TEXTURE_CUBE_MAP_POSITIVE_X+G,Ae.__webglTexture,$)}else if(me){const Ae=Re.get(T.texture),Fe=G;L.framebufferTextureLayer(L.FRAMEBUFFER,L.COLOR_ATTACHMENT0,Ae.__webglTexture,$,Fe)}else if(T!==null&&$!==0){const Ae=Re.get(T.texture);L.framebufferTexture2D(L.FRAMEBUFFER,L.COLOR_ATTACHMENT0,L.TEXTURE_2D,Ae.__webglTexture,$)}v=-1},this.readRenderTargetPixels=function(T,G,$,Y,H,ce,me){if(!(T&&T.isWebGLRenderTarget)){console.error("THREE.WebGLRenderer.readRenderTargetPixels: renderTarget is not THREE.WebGLRenderTarget.");return}let ye=Re.get(T).__webglFramebuffer;if(T.isWebGLCubeRenderTarget&&me!==void 0&&(ye=ye[me]),ye){ve.bindFramebuffer(L.FRAMEBUFFER,ye);try{const Ae=T.texture,Fe=Ae.format,Oe=Ae.type;if(!_e.textureFormatReadable(Fe)){console.error("THREE.WebGLRenderer.readRenderTargetPixels: renderTarget is not in RGBA or implementation defined format.");return}if(!_e.textureTypeReadable(Oe)){console.error("THREE.WebGLRenderer.readRenderTargetPixels: renderTarget is not in UnsignedByteType or implementation defined type.");return}G>=0&&G<=T.width-Y&&$>=0&&$<=T.height-H&&L.readPixels(G,$,Y,H,Ge.convert(Fe),Ge.convert(Oe),ce)}finally{const Ae=C!==null?Re.get(C).__webglFramebuffer:null;ve.bindFramebuffer(L.FRAMEBUFFER,Ae)}}},this.readRenderTargetPixelsAsync=async function(T,G,$,Y,H,ce,me){if(!(T&&T.isWebGLRenderTarget))throw new Error("THREE.WebGLRenderer.readRenderTargetPixels: renderTarget is not THREE.WebGLRenderTarget.");let ye=Re.get(T).__webglFramebuffer;if(T.isWebGLCubeRenderTarget&&me!==void 0&&(ye=ye[me]),ye){const Ae=T.texture,Fe=Ae.format,Oe=Ae.type;if(!_e.textureFormatReadable(Fe))throw new Error("THREE.WebGLRenderer.readRenderTargetPixelsAsync: renderTarget is not in RGBA or implementation defined format.");if(!_e.textureTypeReadable(Oe))throw new Error("THREE.WebGLRenderer.readRenderTargetPixelsAsync: renderTarget is not in UnsignedByteType or implementation defined type.");if(G>=0&&G<=T.width-Y&&$>=0&&$<=T.height-H){ve.bindFramebuffer(L.FRAMEBUFFER,ye);const Ie=L.createBuffer();L.bindBuffer(L.PIXEL_PACK_BUFFER,Ie),L.bufferData(L.PIXEL_PACK_BUFFER,ce.byteLength,L.STREAM_READ),L.readPixels(G,$,Y,H,Ge.convert(Fe),Ge.convert(Oe),0);const Ye=C!==null?Re.get(C).__webglFramebuffer:null;ve.bindFramebuffer(L.FRAMEBUFFER,Ye);const et=L.fenceSync(L.SYNC_GPU_COMMANDS_COMPLETE,0);return L.flush(),await lu(L,et,4),L.bindBuffer(L.PIXEL_PACK_BUFFER,Ie),L.getBufferSubData(L.PIXEL_PACK_BUFFER,0,ce),L.deleteBuffer(Ie),L.deleteSync(et),ce}else throw new Error("THREE.WebGLRenderer.readRenderTargetPixelsAsync: requested read bounds are out of range.")}},this.copyFramebufferToTexture=function(T,G=null,$=0){T.isTexture!==!0&&(Vn("WebGLRenderer: copyFramebufferToTexture function signature has changed."),G=arguments[0]||null,T=arguments[1]);const Y=Math.pow(2,-$),H=Math.floor(T.image.width*Y),ce=Math.floor(T.image.height*Y),me=G!==null?G.x:0,ye=G!==null?G.y:0;I.setTexture2D(T,0),L.copyTexSubImage2D(L.TEXTURE_2D,$,0,0,me,ye,H,ce),ve.unbindTexture()};const ml=L.createFramebuffer(),gl=L.createFramebuffer();this.copyTextureToTexture=function(T,G,$=null,Y=null,H=0,ce=null){T.isTexture!==!0&&(Vn("WebGLRenderer: copyTextureToTexture function signature has changed."),Y=arguments[0]||null,T=arguments[1],G=arguments[2],ce=arguments[3]||0,$=null),ce===null&&(H!==0?(Vn("WebGLRenderer: copyTextureToTexture function signature has changed to support src and dst mipmap levels."),ce=H,H=0):ce=0);let me,ye,Ae,Fe,Oe,Ie,Ye,et,pt;const ht=T.isCompressedTexture?T.mipmaps[ce]:T.image;if($!==null)me=$.max.x-$.min.x,ye=$.max.y-$.min.y,Ae=$.isBox3?$.max.z-$.min.z:1,Fe=$.min.x,Oe=$.min.y,Ie=$.isBox3?$.min.z:0;else{const Bt=Math.pow(2,-H);me=Math.floor(ht.width*Bt),ye=Math.floor(ht.height*Bt),T.isDataArrayTexture?Ae=ht.depth:T.isData3DTexture?Ae=Math.floor(ht.depth*Bt):Ae=1,Fe=0,Oe=0,Ie=0}Y!==null?(Ye=Y.x,et=Y.y,pt=Y.z):(Ye=0,et=0,pt=0);const Ze=Ge.convert(G.format),Ue=Ge.convert(G.type);let Mt;G.isData3DTexture?(I.setTexture3D(G,0),Mt=L.TEXTURE_3D):G.isDataArrayTexture||G.isCompressedArrayTexture?(I.setTexture2DArray(G,0),Mt=L.TEXTURE_2D_ARRAY):(I.setTexture2D(G,0),Mt=L.TEXTURE_2D),L.pixelStorei(L.UNPACK_FLIP_Y_WEBGL,G.flipY),L.pixelStorei(L.UNPACK_PREMULTIPLY_ALPHA_WEBGL,G.premultiplyAlpha),L.pixelStorei(L.UNPACK_ALIGNMENT,G.unpackAlignment);const tt=L.getParameter(L.UNPACK_ROW_LENGTH),Wt=L.getParameter(L.UNPACK_IMAGE_HEIGHT),ri=L.getParameter(L.UNPACK_SKIP_PIXELS),It=L.getParameter(L.UNPACK_SKIP_ROWS),Gi=L.getParameter(L.UNPACK_SKIP_IMAGES);L.pixelStorei(L.UNPACK_ROW_LENGTH,ht.width),L.pixelStorei(L.UNPACK_IMAGE_HEIGHT,ht.height),L.pixelStorei(L.UNPACK_SKIP_PIXELS,Fe),L.pixelStorei(L.UNPACK_SKIP_ROWS,Oe),L.pixelStorei(L.UNPACK_SKIP_IMAGES,Ie);const ct=T.isDataArrayTexture||T.isData3DTexture,Ot=G.isDataArrayTexture||G.isData3DTexture;if(T.isDepthTexture){const Bt=Re.get(T),At=Re.get(G),Dt=Re.get(Bt.__renderTarget),Qr=Re.get(At.__renderTarget);ve.bindFramebuffer(L.READ_FRAMEBUFFER,Dt.__webglFramebuffer),ve.bindFramebuffer(L.DRAW_FRAMEBUFFER,Qr.__webglFramebuffer);for(let Un=0;Un<Ae;Un++)ct&&(L.framebufferTextureLayer(L.READ_FRAMEBUFFER,L.COLOR_ATTACHMENT0,Re.get(T).__webglTexture,H,Ie+Un),L.framebufferTextureLayer(L.DRAW_FRAMEBUFFER,L.COLOR_ATTACHMENT0,Re.get(G).__webglTexture,ce,pt+Un)),L.blitFramebuffer(Fe,Oe,me,ye,Ye,et,me,ye,L.DEPTH_BUFFER_BIT,L.NEAREST);ve.bindFramebuffer(L.READ_FRAMEBUFFER,null),ve.bindFramebuffer(L.DRAW_FRAMEBUFFER,null)}else if(H!==0||T.isRenderTargetTexture||Re.has(T)){const Bt=Re.get(T),At=Re.get(G);ve.bindFramebuffer(L.READ_FRAMEBUFFER,ml),ve.bindFramebuffer(L.DRAW_FRAMEBUFFER,gl);for(let Dt=0;Dt<Ae;Dt++)ct?L.framebufferTextureLayer(L.READ_FRAMEBUFFER,L.COLOR_ATTACHMENT0,Bt.__webglTexture,H,Ie+Dt):L.framebufferTexture2D(L.READ_FRAMEBUFFER,L.COLOR_ATTACHMENT0,L.TEXTURE_2D,Bt.__webglTexture,H),Ot?L.framebufferTextureLayer(L.DRAW_FRAMEBUFFER,L.COLOR_ATTACHMENT0,At.__webglTexture,ce,pt+Dt):L.framebufferTexture2D(L.DRAW_FRAMEBUFFER,L.COLOR_ATTACHMENT0,L.TEXTURE_2D,At.__webglTexture,ce),H!==0?L.blitFramebuffer(Fe,Oe,me,ye,Ye,et,me,ye,L.COLOR_BUFFER_BIT,L.NEAREST):Ot?L.copyTexSubImage3D(Mt,ce,Ye,et,pt+Dt,Fe,Oe,me,ye):L.copyTexSubImage2D(Mt,ce,Ye,et,Fe,Oe,me,ye);ve.bindFramebuffer(L.READ_FRAMEBUFFER,null),ve.bindFramebuffer(L.DRAW_FRAMEBUFFER,null)}else Ot?T.isDataTexture||T.isData3DTexture?L.texSubImage3D(Mt,ce,Ye,et,pt,me,ye,Ae,Ze,Ue,ht.data):G.isCompressedArrayTexture?L.compressedTexSubImage3D(Mt,ce,Ye,et,pt,me,ye,Ae,Ze,ht.data):L.texSubImage3D(Mt,ce,Ye,et,pt,me,ye,Ae,Ze,Ue,ht):T.isDataTexture?L.texSubImage2D(L.TEXTURE_2D,ce,Ye,et,me,ye,Ze,Ue,ht.data):T.isCompressedTexture?L.compressedTexSubImage2D(L.TEXTURE_2D,ce,Ye,et,ht.width,ht.height,Ze,ht.data):L.texSubImage2D(L.TEXTURE_2D,ce,Ye,et,me,ye,Ze,Ue,ht);L.pixelStorei(L.UNPACK_ROW_LENGTH,tt),L.pixelStorei(L.UNPACK_IMAGE_HEIGHT,Wt),L.pixelStorei(L.UNPACK_SKIP_PIXELS,ri),L.pixelStorei(L.UNPACK_SKIP_ROWS,It),L.pixelStorei(L.UNPACK_SKIP_IMAGES,Gi),ce===0&&G.generateMipmaps&&L.generateMipmap(Mt),ve.unbindTexture()},this.copyTextureToTexture3D=function(T,G,$=null,Y=null,H=0){return T.isTexture!==!0&&(Vn("WebGLRenderer: copyTextureToTexture3D function signature has changed."),$=arguments[0]||null,Y=arguments[1]||null,T=arguments[2],G=arguments[3],H=arguments[4]||0),Vn('WebGLRenderer: copyTextureToTexture3D function has been deprecated. Use "copyTextureToTexture" instead.'),this.copyTextureToTexture(T,G,$,Y,H)},this.initRenderTarget=function(T){Re.get(T).__webglFramebuffer===void 0&&I.setupRenderTarget(T)},this.initTexture=function(T){T.isCubeTexture?I.setTextureCube(T,0):T.isData3DTexture?I.setTexture3D(T,0):T.isDataArrayTexture||T.isCompressedArrayTexture?I.setTexture2DArray(T,0):I.setTexture2D(T,0),ve.unbindTexture()},this.resetState=function(){A=0,b=0,C=null,ve.reset(),st.reset()},typeof __THREE_DEVTOOLS__<"u"&&__THREE_DEVTOOLS__.dispatchEvent(new CustomEvent("observe",{detail:this}))}get coordinateSystem(){return fn}get outputColorSpace(){return this._outputColorSpace}set outputColorSpace(e){this._outputColorSpace=e;const t=this.getContext();t.drawingBufferColorspace=Je._getDrawingBufferColorSpace(e),t.unpackColorSpace=Je._getUnpackColorSpace()}}const En=1e-6,bi=5e-5,Ia=1e-7;function Rs(n,e){return n[0]*e[0]+n[1]*e[1]+n[2]*e[2]}function Cs(n,e){return[n[0]-e[0],n[1]-e[1],n[2]-e[2]]}function Ps(n,e){return[n[1]*e[2]-n[2]*e[1],n[2]*e[0]-n[0]*e[2],n[0]*e[1]-n[1]*e[0]]}function Im(n){const e=Math.hypot(n[0],n[1],n[2]);return e<1e-12?null:[n[0]/e,n[1]/e,n[2]/e]}function Gr(n,e){const t=n[0]-e[0],i=n[1]-e[1],r=n[2]-e[2];return t*t+i*i+r*r}function Ua(n){if(n.length<3)return 0;const e=n[0];let t=0,i=0,r=0;for(let a=1;a+1<n.length;a++){const s=Cs(n[a],e),o=Cs(n[a+1],e),c=Ps(s,o);t+=c[0],i+=c[1],r+=c[2]}return .5*Math.hypot(t,i,r)}function Um(n,e){const t=[],i=bi*bi;for(const f of n)t.some(m=>Gr(f,m)<=i)||t.push(f);if(t.length<3)return[];let r=0,a=0,s=0;for(const f of t)r+=f[0],a+=f[1],s+=f[2];r/=t.length,a/=t.length,s/=t.length;const o=[r,a,s],c=Math.abs(e[0])<.8?[1,0,0]:[0,1,0],l=Im(Ps(c,e));if(!l)return[];const d=Ps(e,l),h=t.map(f=>{const m=Cs(f,o),g=Rs(m,l),_=Rs(m,d);return{tacka:f,ugao:Math.atan2(_,g)}});return h.sort((f,m)=>f.ugao-m.ugao),h.map(f=>f.tacka)}function zm(n){return[{normala:[1,0,0],grupaId:"__okvir__",oznaka:"",temena:[[n,-n,-n],[n,n,-n],[n,n,n],[n,-n,n]]},{normala:[-1,0,0],grupaId:"__okvir__",oznaka:"",temena:[[-n,-n,n],[-n,n,n],[-n,n,-n],[-n,-n,-n]]},{normala:[0,1,0],grupaId:"__okvir__",oznaka:"",temena:[[-n,n,-n],[-n,n,n],[n,n,n],[n,n,-n]]},{normala:[0,-1,0],grupaId:"__okvir__",oznaka:"",temena:[[-n,-n,n],[-n,-n,-n],[n,-n,-n],[n,-n,n]]},{normala:[0,0,1],grupaId:"__okvir__",oznaka:"",temena:[[-n,-n,n],[n,-n,n],[n,n,n],[-n,n,n]]},{normala:[0,0,-1],grupaId:"__okvir__",oznaka:"",temena:[[n,-n,-n],[-n,-n,-n],[-n,n,-n],[n,n,-n]]}]}function er(n){if(n.length===0)return{temena:[],pljosni:[]};let e=1;const t=[];for(let c=0;c<n.length;c++){const l=n[c],d=Math.hypot(l.normala[0],l.normala[1],l.normala[2]);if(d<1e-12)continue;const h=[l.normala[0]/d,l.normala[1]/d,l.normala[2]/d],f=l.d;e=Math.max(e,Math.abs(f)),t.push({normala:h,d:f,grupaId:l.grupaId??`forma-${c}`,oznaka:l.oznaka??""})}let i=zm(Math.max(12,e*6));for(const c of t){const l=[],d=[];for(const f of i){const m=f.temena.length;if(m<3)continue;const g=f.temena.map(E=>Rs(c.normala,E)-c.d),_=[];for(let E=0;E<m;E++){const y=(E+1)%m,M=f.temena[E],D=f.temena[y],A=g[E],b=g[y],C=A<=En,v=b<=En;if(Math.abs(A)<=En*4&&d.push(M),C&&_.push(M),A<-En&&b>En||A>En&&b<-En){const x=A/(A-b),P=[M[0]+(D[0]-M[0])*x,M[1]+(D[1]-M[1])*x,M[2]+(D[2]-M[2])*x];_.push(P),d.push(P)}else!C&&v&&Math.abs(b)<=En&&d.push(D)}const p=[],u=bi*bi;for(const E of _)(p.length===0||Gr(E,p[p.length-1])>u)&&p.push(E);p.length>1&&Gr(p[0],p[p.length-1])<=u&&p.pop(),p.length>=3&&Ua(p)>Ia&&l.push({temena:p,normala:f.normala,grupaId:f.grupaId,oznaka:f.oznaka})}const h=Um(d,c.normala);if(h.length>=3&&Ua(h)>Ia&&l.push({temena:h,normala:c.normala,grupaId:c.grupaId,oznaka:c.oznaka}),i=l,i.length===0)break}const r=[],a=[],s=bi*bi;function o(c){for(let l=0;l<r.length;l++)if(Gr(r[l],c)<=s)return l;return r.push([Math.abs(c[0])<1e-10?0:c[0],Math.abs(c[1])<1e-10?0:c[1],Math.abs(c[2])<1e-10?0:c[2]]),r.length-1}for(const c of i){if(c.grupaId==="__okvir__")continue;const l=Ua(c.temena);if(l<=Ia)continue;const d=c.temena.map(p=>o(p)),h=[];for(const p of d)(h.length===0||h[h.length-1]!==p)&&h.push(p);if(h.length>1&&h[0]===h[h.length-1]&&h.pop(),h.length<3)continue;let f=0,m=0,g=0;for(const p of h){const u=r[p];f+=u[0],m+=u[1],g+=u[2]}const _=h.length;a.push({indeksiTemena:h,normala:c.normala,centar:[f/_,m/_,g/_],povrsina:l,grupaId:c.grupaId,oznaka:c.oznaka})}return{temena:r,pljosni:a}}function tr(n){const e=[];for(const d of n.pljosni)e.includes(d.grupaId)||e.push(d.grupaId);const t=[],i=[],r=[],a=[];for(let d=0;d<e.length;d++){const h=e[d],f=t.length/3;for(let g=0;g<n.pljosni.length;g++){const _=n.pljosni[g];if(_.grupaId!==h)continue;const p=_.indeksiTemena;if(p.length<3)continue;const u=n.temena[p[0]],[E,y,M]=_.normala;for(let D=1;D+1<p.length;D++){const A=n.temena[p[D]],b=n.temena[p[D+1]];t.push(u[0],u[1],u[2],A[0],A[1],A[2],b[0],b[1],b[2]),i.push(E,y,M,E,y,M,E,y,M),r.push(g)}}const m=t.length/3;m>f&&a.push({pocetak:f,broj:m-f,indeksMaterijala:d})}const s=new Xe;s.setAttribute("position",new je(t,3)),s.setAttribute("normal",new je(i,3));for(const d of a)s.addGroup(d.pocetak,d.broj,d.indeksMaterijala);const o=new Set,c=[];for(const d of n.pljosni){const h=d.indeksiTemena;for(let f=0;f<h.length;f++){const m=h[f],g=h[(f+1)%h.length],_=m<g?`${m}-${g}`:`${g}-${m}`;if(o.has(_))continue;o.add(_);const p=n.temena[m],u=n.temena[g];c.push(p[0],p[1],p[2],u[0],u[1],u[2])}}const l=new Xe;return l.setAttribute("position",new je(c,3)),{geometrijaMreze:s,geometrijaIvica:l,mapaTrougaoUPljosan:r,redosledGrupa:e}}const Nm=.5,km=.35,Fm=.6;function ni(n,e={}){const t=Math.min(Fm,Math.max(km,e.providnost??Nm));return new Bu({color:new oe(n),transparent:!0,opacity:t,depthWrite:!1,side:St,roughness:.1,metalness:0,ior:1.56,specularIntensity:1,clearcoat:1,clearcoatRoughness:.06,envMapIntensity:1.1,flatShading:!0})}function Ni(n,e){return new oe(n).lerp(new oe(e),.3)}function nr(n,e){return new lt({color:Ni(n,e)})}function Om(n,e){return Math.hypot(n.r-e.r,n.g-e.g,n.b-e.b)}function Ys(n,e){const t=new oe(n);let i=new oe(e[0]??n),r=-1;for(const a of e){const s=new oe(a),o=Om(t,s);o>r+1e-6&&(r=o,i=s)}return i}const Ds=64;function Bm(n=Ds){const e=new Uint8Array(n*n*4),t=(n-1)/2;for(let i=0;i<n;i++)for(let r=0;r<n;r++){const a=Math.min(1,Math.hypot(r-t,i-t)/t),s=1-a*a*(3-2*a),o=Math.round(255*s*s),c=(i*n+r)*4;e[c]=o,e[c+1]=o,e[c+2]=o,e[c+3]=255}return e}function Vm(n){const e=new Nu(Bm(),Ds,Ds,Ht);e.needsUpdate=!0;const t=new Ln({alphaMap:e,transparent:!0,depthWrite:!1,opacity:.2}),i=new Le(new ii(n*2,n*2),t);return i.rotation.x=-Math.PI/2,i.renderOrder=-1,i.name="kontaktna-senka",{mreza:i,osveziBoju(r,a,s){t.color.set(r?s:a),t.opacity=r?.14:.2}}}class Gm extends el{constructor(){super();const e=new Qt;e.deleteAttribute("uv");const t=new ft({side:Ct}),i=new ft,r=new Wu(16777215,900,28,2);r.position.set(.418,16.199,.3),this.add(r);const a=new Le(e,t);a.position.set(-.757,13.219,.717),a.scale.set(31.713,28.305,28.591),this.add(a);const s=new Le(e,i);s.position.set(-10.906,2.009,1.846),s.rotation.set(0,-.195,0),s.scale.set(2.328,7.905,4.651),this.add(s);const o=new Le(e,i);o.position.set(-5.607,-.754,-.758),o.rotation.set(0,.994,0),o.scale.set(1.97,1.534,3.955),this.add(o);const c=new Le(e,i);c.position.set(6.167,.857,7.803),c.rotation.set(0,.561,0),c.scale.set(3.927,6.285,3.687),this.add(c);const l=new Le(e,i);l.position.set(-2.017,.018,6.124),l.rotation.set(0,.333,0),l.scale.set(2.002,4.566,2.064),this.add(l);const d=new Le(e,i);d.position.set(2.291,-.756,-2.621),d.rotation.set(0,-.286,0),d.scale.set(1.546,1.552,1.496),this.add(d);const h=new Le(e,i);h.position.set(-2.193,-.369,-5.547),h.rotation.set(0,.516,0),h.scale.set(3.875,3.487,2.986),this.add(h);const f=new Le(e,Mi(50));f.position.set(-16.116,14.37,8.208),f.scale.set(.1,2.428,2.739),this.add(f);const m=new Le(e,Mi(50));m.position.set(-16.109,18.021,-8.207),m.scale.set(.1,2.425,2.751),this.add(m);const g=new Le(e,Mi(17));g.position.set(14.904,12.198,-1.832),g.scale.set(.15,4.265,6.331),this.add(g);const _=new Le(e,Mi(43));_.position.set(-.462,8.89,14.52),_.scale.set(4.38,5.441,.088),this.add(_);const p=new Le(e,Mi(20));p.position.set(3.235,11.486,-12.541),p.scale.set(2.5,2,.1),this.add(p);const u=new Le(e,Mi(100));u.position.set(0,20,0),u.scale.set(1,.1,1),this.add(u)}dispose(){const e=new Set;this.traverse(t=>{t.isMesh&&(e.add(t.geometry),e.add(t.material))});for(const t of e)t.dispose()}}function Mi(n){const e=new Ln;return e.color.setScalar(n),e}function Si(n,e,t){return Math.max(e,Math.min(t,n))}class Hm{stanje;pocetno;minUdaljenost;maksUdaljenost;opcije;vuceMisem=!1;prethodniX=0;prethodniY=0;dodirAktiviran=!1;prethodniDodirX=0;prethodniDodirY=0;prethodniRazmakPrstiju=0;pocetakDodiraX=0;pocetakDodiraY=0;dodirPomeren=!1;cistaci=[];constructor(e){this.opcije=e,this.pocetno={...e.pocetno},this.stanje={...e.pocetno},this.minUdaljenost=e.minUdaljenost??2,this.maksUdaljenost=e.maksUdaljenost??24,this.poveziDogadjaje()}trenutnoStanje(){return{...this.stanje}}rotirajAzimut(e){this.stanje.theta+=e,this.opcije.naPromenu(this.trenutnoStanje())}rotirajElevaciju(e){this.stanje.phi=Si(this.stanje.phi+e,.15,Math.PI-.15),this.opcije.naPromenu(this.trenutnoStanje())}zumiraj(e){this.stanje.udaljenost=Si(this.stanje.udaljenost*e,this.minUdaljenost,this.maksUdaljenost),this.opcije.naPromenu(this.trenutnoStanje())}resetuj(){this.stanje={...this.pocetno},this.opcije.naPromenu(this.trenutnoStanje())}postaviAktivacijuDodira(e){this.dodirAktiviran=e,this.opcije.platno.classList.toggle("udzbenik-scena-platno--dodir-aktivan",e),this.opcije.dugmeDodira.hidden=!e,this.opcije.priPromeniAktivacijeDodira?.(e)}poveziDogadjaje(){const{bina:e,platno:t,dugmeDodira:i}=this.opcije,r=g=>{if(g.pointerType!=="touch"&&g.button===0){this.vuceMisem=!0,this.prethodniX=g.clientX,this.prethodniY=g.clientY;try{t.setPointerCapture(g.pointerId)}catch{}}},a=g=>{if(g.pointerType==="touch"||!this.vuceMisem)return;const _=g.clientX-this.prethodniX,p=g.clientY-this.prethodniY;this.prethodniX=g.clientX,this.prethodniY=g.clientY,this.stanje.theta-=_*.008,this.stanje.phi=Si(this.stanje.phi-p*.008,.15,Math.PI-.15),this.opcije.naPromenu(this.trenutnoStanje())},s=g=>{if(g.pointerType!=="touch"){this.vuceMisem=!1;try{t.hasPointerCapture(g.pointerId)&&t.releasePointerCapture(g.pointerId)}catch{}}},o=g=>{if(!(document.activeElement===e||e.contains(document.activeElement))&&!g.ctrlKey&&!g.metaKey)return;g.preventDefault();const p=g.deltaY>0?1.09:.92;this.zumiraj(p)},c=g=>{if(g.touches.length===2){const _=g.touches[0],p=g.touches[1];this.prethodniDodirX=(_.clientX+p.clientX)/2,this.prethodniDodirY=(_.clientY+p.clientY)/2,this.prethodniRazmakPrstiju=Math.hypot(p.clientX-_.clientX,p.clientY-_.clientY)}else if(g.touches.length===1){const _=g.touches[0];this.pocetakDodiraX=_.clientX,this.pocetakDodiraY=_.clientY,this.prethodniDodirX=_.clientX,this.prethodniDodirY=_.clientY,this.dodirPomeren=!1}},l=g=>{if(g.touches.length===2){g.preventDefault();const _=g.touches[0],p=g.touches[1],u=(_.clientX+p.clientX)/2,E=(_.clientY+p.clientY)/2,y=Math.hypot(p.clientX-_.clientX,p.clientY-_.clientY),M=u-this.prethodniDodirX,D=E-this.prethodniDodirY;if(this.prethodniDodirX=u,this.prethodniDodirY=E,this.stanje.theta-=M*.008,this.stanje.phi=Si(this.stanje.phi-D*.008,.15,Math.PI-.15),this.prethodniRazmakPrstiju>8&&y>8){const A=this.prethodniRazmakPrstiju/y;this.stanje.udaljenost=Si(this.stanje.udaljenost*A,this.minUdaljenost,this.maksUdaljenost)}this.prethodniRazmakPrstiju=y,this.dodirPomeren=!0,this.opcije.naPromenu(this.trenutnoStanje())}else if(g.touches.length===1){const _=g.touches[0];if(Math.hypot(_.clientX-this.pocetakDodiraX,_.clientY-this.pocetakDodiraY)>8&&(this.dodirPomeren=!0),this.dodirAktiviran){g.preventDefault();const p=_.clientX-this.prethodniDodirX,u=_.clientY-this.prethodniDodirY;this.prethodniDodirX=_.clientX,this.prethodniDodirY=_.clientY,this.stanje.theta-=p*.009,this.stanje.phi=Si(this.stanje.phi-u*.009,.15,Math.PI-.15),this.opcije.naPromenu(this.trenutnoStanje())}}},d=g=>{g.touches.length===0&&!this.dodirPomeren&&g.changedTouches.length===1&&this.postaviAktivacijuDodira(!this.dodirAktiviran)},h=()=>{this.postaviAktivacijuDodira(!1)},f=g=>{this.dodirAktiviran&&g.target instanceof Node&&!e.contains(g.target)&&this.postaviAktivacijuDodira(!1)},m=g=>{if(!(g.target instanceof HTMLElement&&g.target!==e&&(g.target.tagName==="BUTTON"||g.target.tagName==="INPUT")))switch(g.key){case"ArrowLeft":g.preventDefault(),this.rotirajAzimut(-.12);break;case"ArrowRight":g.preventDefault(),this.rotirajAzimut(.12);break;case"ArrowUp":g.preventDefault(),this.rotirajElevaciju(-.12);break;case"ArrowDown":g.preventDefault(),this.rotirajElevaciju(.12);break;case"+":case"=":g.preventDefault(),this.zumiraj(.88);break;case"-":case"_":g.preventDefault(),this.zumiraj(1.14);break;case"r":case"R":case"р":case"Р":g.preventDefault(),this.opcije.naReset();break;case" ":g.preventDefault(),this.opcije.naPrekidacPauze();break;case"Escape":this.dodirAktiviran&&(g.preventDefault(),this.postaviAktivacijuDodira(!1));break}};t.addEventListener("pointerdown",r),t.addEventListener("pointermove",a),t.addEventListener("pointerup",s),t.addEventListener("pointercancel",s),t.addEventListener("wheel",o,{passive:!1}),t.addEventListener("touchstart",c,{passive:!0}),t.addEventListener("touchmove",l,{passive:!1}),t.addEventListener("touchend",d),i.addEventListener("click",h),document.addEventListener("touchstart",f,{passive:!0}),e.addEventListener("keydown",m),this.cistaci.push(()=>{t.removeEventListener("pointerdown",r),t.removeEventListener("pointermove",a),t.removeEventListener("pointerup",s),t.removeEventListener("pointercancel",s),t.removeEventListener("wheel",o),t.removeEventListener("touchstart",c),t.removeEventListener("touchmove",l),t.removeEventListener("touchend",d),i.removeEventListener("click",h),document.removeEventListener("touchstart",f),e.removeEventListener("keydown",m)})}raspolazi(){for(const e of this.cistaci)e();this.cistaci.length=0}}let dn=null,Ti=null,Zn=0,Jn=0,Kn=null;function jm(){if(dn)return dn;const n=document.createElement("canvas"),e=n.getContext("webgl2",{antialias:!0,alpha:!1,preserveDrawingBuffer:!1})??n.getContext("webgl",{antialias:!0,alpha:!1,preserveDrawingBuffer:!1});if(!e)throw new Error("WebGL контекст није доступан у овом прегледачу.");const t=new Lm({canvas:n,context:e,antialias:!0,alpha:!1,powerPreference:"default"});return t.setPixelRatio(1),t.outputColorSpace=Nt,Ti=n,dn=t,Zn=320,Jn=240,dn.setSize(Zn,Jn,!1),dn}function Wm(n){if(Kn)return Kn;try{const e=new ws(n),t=new Gm;Kn=e.fromScene(t,.04).texture,t.dispose(),e.dispose()}catch{Kn=null}return Kn}function y0(){Kn?.dispose(),Kn=null,dn&&(dn.forceContextLoss(),dn.dispose(),dn=null,Ti=null,Zn=0,Jn=0)}function Pt(n){n.traverse(e=>{const t=e;t.geometry&&typeof t.geometry.dispose=="function"&&t.geometry.dispose();const i=t.material;if(Array.isArray(i))for(const r of i)mc(r);else i&&mc(i)})}function mc(n){for(const e of Object.values(n))e instanceof wt&&e.dispose();n.dispose()}function Xm(n,e,t,i){const r=jm(),a=t.platno.getContext("2d");if(!a||!Ti)throw new Error("2D контекст платна није доступан.");const s=typeof window<"u"&&typeof window.matchMedia=="function"&&window.matchMedia("(prefers-reduced-motion: reduce)").matches,o=new el,c=new kt(42,16/9,.1,100),l=new F(0,0,0),d=new qu(new oe(1,1,1),.72),h=new Go(new oe(1,1,1),.95);h.position.set(5,8,6);const f=new Go(new oe(1,1,1),.38);if(f.position.set(-5,-3,-4),o.add(d,h,f),n.izgled==="kristal"){const W=Wm(r);W&&(o.environment=W,o.environmentIntensity=.85,d.intensity=.32,h.intensity=1.25,h.position.set(4,9,5),f.intensity=0)}const m=[];function g(){for(const W of m)W.osveziBoju(ai.jeTamna(),ai.token("--text-primary"),ai.token("--text-secondary"))}let _=!1;const p=n.pocetnaKamera?.(e)??{theta:.62,phi:1.12,udaljenost:6.2};function u(W){const L=Math.sin(W.phi);c.position.set(l.x+W.udaljenost*L*Math.sin(W.theta),l.y+W.udaljenost*Math.cos(W.phi),l.z+W.udaljenost*L*Math.cos(W.theta)),c.lookAt(l),c.updateMatrixWorld()}u(p);let E=!1,y=!1,M=!0,D=n.imaPodrazumevanuAnimaciju?n.imaPodrazumevanuAnimaciju(e):!0,A=s||!D,b=null,C=null,v=0,x=0,P=Math.max(240,t.bina.clientWidth||600),U=Math.max(180,t.bina.clientHeight||360),w=null;function R(){if(E||y||!Ti||!a)return;const W=t.bina.clientWidth,L=t.bina.clientHeight;W>0&&L>0&&(P=W,U=L);const Ee=Math.min(typeof window<"u"&&window.devicePixelRatio||1,2),Se=Math.max(1,Math.round(P*Ee)),_e=Math.max(1,Math.round(U*Ee));(t.platno.width!==Se||t.platno.height!==_e)&&(t.platno.width=Se,t.platno.height=_e),c.aspect=P/Math.max(1,U),c.updateProjectionMatrix();const ve=Math.min(4096,Math.max(Zn,Se)),Ne=Math.min(4096,Math.max(Jn,_e));(ve>Zn||Ne>Jn)&&(Zn=ve,Jn=Ne,r.setSize(Zn,Jn,!1));const Re=new oe(ai.token("--bg-card"));r.setViewport(0,0,Se,_e),r.setScissor(0,0,Se,_e),r.setScissorTest(!0),r.setClearColor(Re,1),r.clear(!0,!0,!0),r.render(o,c);const I=Math.max(0,Ti.height-_e);a.drawImage(Ti,0,I,Se,_e,0,0,Se,_e),w?.posleRendera?.()}function z(){E||y||b!==null||C!==null||(C=requestAnimationFrame(()=>{C=null,R()}))}function N(){const W=typeof document<"u"&&document.hidden;return!E&&!y&&D&&!A&&M&&!W}function B(W){if(b=null,!N())return;const L=v>0?Math.min(.05,(W-v)/1e3):.016;v=W,x+=L,w?.azuriraj?.(L,x),R(),N()&&(b=requestAnimationFrame(B))}function k(){t.azurirajDugmePauze(A,D),N()?b===null&&(v=performance.now(),b=requestAnimationFrame(B)):b!==null&&(cancelAnimationFrame(b),b=null)}function O(W){const L=W.clone().project(c),Ee=L.z>=-1&&L.z<=1;return{x:(L.x*.5+.5)*P,y:(-L.y*.5+.5)*U,vidljivo:Ee}}const q={scena3D:o,kamera:c,platno:t.platno,slojEtiketa:t.slojEtiketa,gornjeKontrole:t.gornjeKontrole,podnozje:t.podnozje,api:i,tema:ai,smanjenPokret:s,zatraziRender:z,korisnikUpravlja:()=>_,dodajKontaktnuSenku:(W,L,Ee,Se=0)=>{const _e=Vm(W);return _e.mreza.position.set(Se,L,0),(Ee??o).add(_e.mreza),m.push(_e),g(),_e.mreza},postaviImaAnimaciju:W=>{D=W,W||(A=!0),k()},prikaziRezervu:W=>{y=!0,k(),t.prikaziRezervu(W)},projektujU2D:O},K=new Hm({bina:t.bina,platno:t.platno,dugmeDodira:t.dugmeDodira,pocetno:p,naPromenu:W=>{u(W),z()},naReset:()=>{_=!1,K.resetuj(),w?.resetuj?.(),R()},naPrekidacPauze:()=>{D&&(A=!A,k())}});w=n.kreiraj(q,e);const le=()=>{_=!1,K.resetuj(),w?.resetuj?.(),R()},De=()=>{D&&(A=!A,k())},X=()=>{A=!0,k(),w?.korak?w.korak():(x+=.45,w?.azuriraj?.(.45,x)),R()},J=()=>{_=!0},ae=()=>{J(),K.zumiraj(.86)},re=()=>{J(),K.zumiraj(1.16)},ue=W=>{(W.key.startsWith("Arrow")||W.key==="+"||W.key==="-"||W.key==="=")&&J()};t.platno.addEventListener("pointerdown",J),t.platno.addEventListener("wheel",J,{passive:!0}),t.bina.addEventListener("keydown",ue),t.dugmeReset.addEventListener("click",le),t.dugmePauza.addEventListener("click",De),t.dugmeKorak.addEventListener("click",X),t.dugmeZumPlus.addEventListener("click",ae),t.dugmeZumMinus.addEventListener("click",re);let Pe=null;typeof ResizeObserver<"u"&&(Pe=new ResizeObserver(W=>{for(const L of W){const Ee=Math.round(L.contentRect.width),Se=Math.round(L.contentRect.height);Ee>0&&Se>0&&(Ee!==P||Se!==U)&&(P=Ee,U=Se,R())}}),Pe.observe(t.bina));let fe=null;typeof IntersectionObserver<"u"&&(fe=new IntersectionObserver(W=>{for(const L of W)M=L.isIntersecting,k()},{threshold:.05}),fe.observe(t.bina));const te=()=>{k(),document.hidden||z()};document.addEventListener("visibilitychange",te);const se=ai.pretplati(W=>{w?.osveziTemu?.(W),g(),R()});return R(),k(),()=>{E||(E=!0,b!==null&&(cancelAnimationFrame(b),b=null),C!==null&&(cancelAnimationFrame(C),C=null),Pe?.disconnect(),fe?.disconnect(),document.removeEventListener("visibilitychange",te),se(),t.dugmeReset.removeEventListener("click",le),t.dugmePauza.removeEventListener("click",De),t.dugmeKorak.removeEventListener("click",X),t.dugmeZumPlus.removeEventListener("click",ae),t.dugmeZumMinus.removeEventListener("click",re),t.platno.removeEventListener("pointerdown",J),t.platno.removeEventListener("wheel",J),t.bina.removeEventListener("keydown",ue),K.raspolazi(),w?.raspolazi?.(),Pt(o),o.clear(),t.slojEtiketa.replaceChildren(),t.gornjeKontrole.replaceChildren(),t.podnozje.replaceChildren())}}const gc={karlsbadski:{zakon:"karlsbadski",naziv:"Карлсбадски близанац",mineral:"ортоклас",sistem:"моноклинични",tipElementa:"osa",opisElementa:"Оса ближњења [001] (c-оса), раван срастања (010)",normalaRavniIliOsa:[0,0,1],ugaoRotacijeStepeni:180,izvor:"Klein & Dutrow 2007, str. 235"},spinelov:{zakon:"spinelov",naziv:"Спинелов закон",mineral:"спинел (октаедар)",sistem:"тесерални",tipElementa:"ravan",opisElementa:"Раван ближњења (111)",normalaRavniIliOsa:[1/Math.sqrt(3),1/Math.sqrt(3),1/Math.sqrt(3)],izvor:"Klein & Dutrow 2007, str. 233"},baveno:{zakon:"baveno",naziv:"Бавено близанац",mineral:"ортоклас",sistem:"моноклинични",tipElementa:"ravan",opisElementa:"Раван ближњења (021), моноклинична метрика (β ≈ 116°)",normalaRavniIliOsa:[.31,.7071,.6355],izvor:"Klein & Dutrow 2007, str. 235"},manebah:{zakon:"manebah",naziv:"Манебах близанац",mineral:"ортоклас",sistem:"моноклинични",tipElementa:"ravan",opisElementa:"Раван ближњења (001), c* нормала одступа ~26° од c-осе због β ≈ 116°",normalaRavniIliOsa:[.4384,0,.8988],izvor:"Klein & Dutrow 2007, str. 235"},"albitski-polisintetski":{zakon:"albitski-polisintetski",naziv:"Албитски полисинтетски закон",mineral:"албит / плагиоклас",sistem:"триклинични",tipElementa:"ravan",opisElementa:"Раван ближњења (010), вишеструке паралелне ламеле",normalaRavniIliOsa:[0,1,0],izvor:"Nesse 2012, str. 280"},japanski:{zakon:"japanski",naziv:"Јапански закон",mineral:"кварц",sistem:"тригонални",tipElementa:"ravan",opisElementa:"Раван ближњења (11-22), теоријски угао међу c-осама 84°33′",normalaRavniIliOsa:[.37,.6408,.6726],ugaoOsaStepeni:84.55,izvor:"Frondel 1962, Dana System of Mineralogy Vol. III (a 4,913 c 5,405 Å)",napomena:"Угао 84°33′ је теоријски угао контакта две јединке кварца по (11-22)."},dofinejski:{zakon:"dofinejski",naziv:"Дофинејски закон",mineral:"кварц",sistem:"тригонални",tipElementa:"osa",opisElementa:"Оса ближњења [0001] (c-оса), ротација за 180°",normalaRavniIliOsa:[0,0,1],ugaoRotacijeStepeni:180,izvor:"Klein & Dutrow 2007, str. 236"},brazilski:{zakon:"brazilski",naziv:"Бразилски закон",mineral:"кварц",sistem:"тригонални",tipElementa:"ravan",opisElementa:"Раван ближњења (11-20), нормала [0,5, √3/2, 0] ≠ [100]",normalaRavniIliOsa:[.5,.866025,0],izvor:"Klein & Dutrow 2007, str. 236; International Tables хексагонска метрика"},"lastin-rep":{zakon:"lastin-rep",naziv:"Ластин реп (близанац гипса)",mineral:"гипс",sistem:"моноклинични",tipElementa:"ravan",opisElementa:"Раван ближњења (100)",normalaRavniIliOsa:[1,0,0],izvor:"Klein & Dutrow 2007, str. 235"},"staurolit-90":{zakon:"staurolit-90",naziv:"Крстасти близанац стауролита (90°)",mineral:"стауролит",sistem:"моноклинични / псеудоромбични",tipElementa:"ravan",opisElementa:"Раван ближњења (031), две јединке под ~90°",normalaRavniIliOsa:[0,.7071,.7071],izvor:"Klein & Dutrow 2007, str. 234"},"staurolit-60":{zakon:"staurolit-60",naziv:"Коси крстасти близанац стауролита (60°)",mineral:"стауролит",sistem:"моноклинични / псеудоромбични",tipElementa:"ravan",opisElementa:"Раван ближњења (231), две c-осе заклапају ~60° (59°05′)",normalaRavniIliOsa:[.7093,.5038,.4931],ugaoOsaStepeni:59.08,izvor:"Klein & Dutrow 2007, str. 234 (метрика: a 7,87 b 16,62 c 5,66 Å)"},"kolenasti-rutil":{zakon:"kolenasti-rutil",naziv:"Коленасти близанац рутила",mineral:"рутил",sistem:"тетрагонални",tipElementa:"ravan",opisElementa:"Раван ближњења (011), прегиб c-оса под 114°30′",normalaRavniIliOsa:[0,.542,.8404],ugaoOsaStepeni:114.5,izvor:"Klein & Dutrow 2007, str. 234 (тетрагонално a 4,59 c 2,96 Å)"},"trilinga-aragonit":{zakon:"trilinga-aragonit",naziv:"Циклички трилинг арагонита",mineral:"арагонит",sistem:"ромбични",tipElementa:"ravan",opisElementa:"Раван ближњења (110), псеудохексагонални склоп",normalaRavniIliOsa:[.707,.707,0],izvor:"Klein & Dutrow 2007, str. 235"},"gvozdeni-krst-pirit":{zakon:"gvozdeni-krst-pirit",naziv:"Гвоздени крст (близанац пирита)",mineral:"пирит",sistem:"тесерални (m-3)",tipElementa:"osa",opisElementa:"Оса ближњења [001] са прорастањем два пиритоедра",normalaRavniIliOsa:[0,0,1],ugaoRotacijeStepeni:90,izvor:"Klein & Dutrow 2007, str. 234"}};function qm(n){const e=[];if(n.includes("спинел")||n.includes("октаедар"))for(const r of[1,-1])for(const a of[1,-1])for(const s of[1,-1]){const o=1/Math.sqrt(3);e.push({normala:[r*o,a*o,s*o],d:1})}else if(n.includes("ортоклас"))e.push({normala:[.707,.707,0],d:.9},{normala:[-.707,.707,0],d:.9},{normala:[.707,-.707,0],d:.9},{normala:[-.707,-.707,0],d:.9},{normala:[0,1,0],d:1},{normala:[0,-1,0],d:1},{normala:[0,0,1],d:1.5},{normala:[0,0,-1],d:1.5},{normala:[.5,0,.866],d:1.1},{normala:[-.5,0,-.866],d:1.1});else if(n.includes("кварц")){const r=Math.sqrt(3),a=[[1,0,0],[-1,0,0],[.5,r/2,0],[-.5,r/2,0],[.5,-r/2,0],[-.5,-r/2,0]];for(const l of a)e.push({normala:l,d:.85});const s=51.78*Math.PI/180,o=Math.sin(s),c=Math.cos(s);for(let l=0;l<6;l++){const d=l*60*Math.PI/180;e.push({normala:[o*Math.cos(d),o*Math.sin(d),c],d:1.35}),e.push({normala:[o*Math.cos(d),o*Math.sin(d),-c],d:1.35})}}else if(n.includes("пирит")){const r=[[0,1,2],[1,2,0],[2,0,1]],a=[[1,1],[1,-1],[-1,1],[-1,-1]],s=Math.sqrt(5);for(const o of r)for(const c of a){const l=[0,0,0];l[o[0]]=2*c[0]/s,l[o[1]]=1*c[1]/s,l[o[2]]=0,e.push({normala:[l[0],l[1],l[2]],d:1})}}else e.push({normala:[1,0,0],d:.75},{normala:[-1,0,0],d:.75},{normala:[0,1,0],d:.85},{normala:[0,-1,0],d:.85},{normala:[0,0,1],d:1.6},{normala:[0,0,-1],d:1.6},{normala:[.707,0,.707],d:1.25},{normala:[-.707,0,.707],d:1.25},{normala:[.707,0,-.707],d:1.25},{normala:[-.707,0,-.707],d:1.25});const t=er(e),i=tr(t);return{mreza:i.geometrijaMreze,ivice:i.geometrijaIvica}}function _c(n){const e=new oe(n.token("--primary")),t=Ys(e,[n.token("--accent"),n.token("--success"),n.token("--info")]);return[e,t]}const Km={izgled:"kristal",imaPodrazumevanuAnimaciju(n){return(n.animacija??"razdvoji-spoji")!=="nema"},pocetnaKamera(){return{theta:.65,phi:1.15,udaljenost:5.8}},kreiraj(n,e){const t=new Qe;n.scena3D.add(t);const i=gc[e.zakon]??gc.karlsbadski,r=qm(i.mineral),a=r.mreza,[s,o]=_c(n.tema),c=n.tema.token("--text-primary"),l=ni(s),d=ni(o),h=nr(c,s),f=nr(c,o),m=new Le(a,l);m.add(new ut(r.ivice,h));const g=a.clone(),_=r.ivice.clone(),p=new Le(g,d);p.add(new ut(_,f));const u=new F(...i.normalaRavniIliOsa).normalize(),E=new Qe;if(E.add(p),i.tipElementa==="osa"){const U=(i.ugaoRotacijeStepeni??180)*Math.PI/180;p.rotateOnAxis(u,U)}else{const U=new at().set(1-2*u.x*u.x,-2*u.x*u.y,-2*u.x*u.z,0,-2*u.y*u.x,1-2*u.y*u.y,-2*u.y*u.z,0,-2*u.z*u.x,-2*u.z*u.y,1-2*u.z*u.z,0,0,0,0,1);g.applyMatrix4(U),_.applyMatrix4(U);const w=g.index;if(w){for(let R=0;R<w.count;R+=3){const z=w.getX(R+1);w.setX(R+1,w.getX(R+2)),w.setX(R+2,z)}w.needsUpdate=!0}g.computeVertexNormals()}t.add(m),t.add(E),a.computeBoundingSphere();const y=a.boundingSphere?.radius??1.5;n.dodajKontaktnuSenku(y*1.7,-y*1.15-.1);const M=new Ln({color:new oe(n.tema.token("--warning")),transparent:!0,opacity:.3,side:St,depthWrite:!1}),D=new lt({color:new oe(n.tema.token("--warning")),linewidth:2});let A=null,b=null;if(e.prikazi_element!==!1)if(i.tipElementa==="ravan"){const U=new ii(3.5,3.5);A=new Le(U,M),A.renderOrder=-.5,A.add(new ut(new Qi(U),D)),A.quaternion.setFromUnitVectors(new F(0,0,1),u),t.add(A)}else{const U=new Xe,w=u.clone().multiplyScalar(-2.8),R=u.clone().multiplyScalar(2.8);U.setAttribute("position",new je([w.x,w.y,w.z,R.x,R.y,R.z],3)),b=new Qn(U,D),t.add(b)}const C=document.createElement("div");C.className="udzbenik-scena-status",C.textContent=`${i.naziv} (${i.mineral}) • ${i.opisElementa}`,n.podnozje.append(C);const v=e.animacija??"razdvoji-spoji";let x=0;function P(){const[U,w]=_c(n.tema),R=n.tema.token("--text-primary");l.color.copy(U),d.color.copy(w),h.color.copy(Ni(R,U)),f.color.copy(Ni(R,w)),M.color.set(n.tema.token("--warning")),D.color.set(n.tema.token("--warning"))}return{azuriraj(U){if(x+=U,v==="razdvoji-spoji"){const w=(Math.sin(x*1.5)*.5+.5)*1.1;E.position.copy(u.clone().multiplyScalar(w)),n.korisnikUpravlja()||(t.rotation.y+=U*.25)}else v==="rotacija"&&!n.korisnikUpravlja()&&(t.rotation.y+=U*.45)},korak(){x+=.4;const U=(Math.sin(x*1.5)*.5+.5)*1.1;E.position.copy(u.clone().multiplyScalar(U)),t.rotation.y+=.2},resetuj(){x=0,E.position.set(0,0,0),t.rotation.set(0,0,0)},osveziTemu(){P()},raspolazi(){a.dispose(),p.geometry.dispose(),l.dispose(),d.dispose(),h.dispose(),f.dispose(),M.dispose(),D.dispose(),A&&A.geometry.dispose(),b&&b.geometry.dispose(),Pt(t),C.remove()}}}};class jn extends Error{constructor(e){super(e),this.name="CifGreska"}}function cn(n,e){const t=n.trim().replace(/\([0-9]+\)$/,""),i=Number(t);if(!Number.isFinite(i))throw new jn(`Неисправна нумеричка вредност у CIF пољу ${e}: "${n}"`);return i}function Ur(n){const e=[];let t=0;const i=n.length;for(;t<i;){for(;t<i&&/\s/.test(n[t]);)t++;if(t>=i)break;const r=n[t];if(r==="#")break;if(r==="'"||r==='"'){const a=r;t++;let s=t;for(;t<i&&!(n[t]===a&&(t+1>=i||/\s/.test(n[t+1])));)t++;e.push(n.slice(s,t)),t<i&&n[t]===a&&t++}else{const a=t;for(;t<i&&!/\s/.test(n[t]);)t++;e.push(n.slice(a,t))}}return e}function $m(n){if(!n||!n.trim())throw new jn("CIF садржај је празан.");const e=n.split(/\r?\n/);let t="struktura";const i=new Map,r=[];let a=0;for(;a<e.length;){const m=e[a].trim();if(!m||m.startsWith("#")){a++;continue}if(m.toLowerCase().startsWith("data_")){t=m.slice(5).trim()||t,a++;continue}if(m.toLowerCase()==="loop_"){a++;const g=[];for(;a<e.length;){const D=e[a].trim();if(!D||D.startsWith("#")){a++;continue}if(D.startsWith("_")){const A=Ur(D);A[0]&&g.push(A[0].toLowerCase()),a++}else break}const _=g.indexOf("_atom_site_label"),p=g.indexOf("_atom_site_type_symbol"),u=g.indexOf("_atom_site_fract_x"),E=g.indexOf("_atom_site_fract_y"),y=g.indexOf("_atom_site_fract_z"),M=_!==-1&&p!==-1&&u!==-1&&E!==-1&&y!==-1;for(;a<e.length;){const D=e[a].trim();if(!D||D.startsWith("#")){a++;continue}const A=D.toLowerCase();if(D.startsWith("_")||A==="loop_"||A.startsWith("data_")||D.startsWith(";"))break;if(M&&g.length>0){const b=Ur(D);if(b.length<g.length)throw new jn("Непотпун ред у _atom_site табели CIF фајла.");const C=b[_],v=b[p],x=cn(b[u],"_atom_site_fract_x"),P=cn(b[E],"_atom_site_fract_y"),U=cn(b[y],"_atom_site_fract_z");r.push({oznaka:C,simbol:_l(v),fx:x,fy:P,fz:U})}a++}continue}if(m.startsWith("_")){const g=Ur(m);if(g.length>=2&&g[0]&&g[1]!==void 0)i.set(g[0].toLowerCase(),g[1]);else if(g.length===1&&g[0]&&a+1<e.length){const _=Ur(e[a+1].trim());_[0]&&!_[0].startsWith("_")&&_[0].toLowerCase()!=="loop_"&&(i.set(g[0].toLowerCase(),_[0]),a++)}}a++}const s=["_cell_length_a","_cell_length_b","_cell_length_c","_cell_angle_alpha","_cell_angle_beta","_cell_angle_gamma"];for(const m of s)if(!i.has(m))throw new jn(`Недостаје обавезно CIF поље: ${m}`);const o=cn(i.get("_cell_length_a"),"_cell_length_a"),c=cn(i.get("_cell_length_b"),"_cell_length_b"),l=cn(i.get("_cell_length_c"),"_cell_length_c"),d=cn(i.get("_cell_angle_alpha"),"_cell_angle_alpha"),h=cn(i.get("_cell_angle_beta"),"_cell_angle_beta"),f=cn(i.get("_cell_angle_gamma"),"_cell_angle_gamma");if(o<=0||c<=0||l<=0)throw new jn("Димензије јединичне ћелије a, b, c морају бити позитивне.");if(d<=0||d>=180||h<=0||h>=180||f<=0||f>=180||d+h+f>=360)throw new jn("Углови јединичне ћелије α, β, γ нису физички валидни.");if(r.length===0)throw new jn("CIF не садржи ниједан атом у loop_ _atom_site блоку.");return{nazivBloka:t,celija:{a:o,b:c,c:l,alpha:d,beta:h,gamma:f},atomi:r}}function Zr(n){const e=Math.PI/180,t=n.alpha*e,i=n.beta*e,r=n.gamma*e,a=Math.cos(t),s=Math.cos(i),o=Math.cos(r),c=Math.sin(r),l=n.a,d=0,h=n.b*o,f=n.b*c,m=0,g=n.c*s,_=n.c*(a-s*o)/c,p=Math.max(0,n.c*n.c-g*g-_*_),u=Math.sqrt(p);return{va:[l,d,-0],vb:[h,m,-f],vc:[g,u,-_]}}function An(n,e,t,i){return[n*i.va[0]+e*i.vb[0]+t*i.vc[0],n*i.va[1]+e*i.vb[1]+t*i.vc[1],n*i.va[2]+e*i.vb[2]+t*i.vc[2]]}const za=[{kljuc:"kubna-P",naziv:"Тесерална примитивна (P)",sistem:"Тесерални",centriranje:"P",brojCvorova:1,celija:{a:1.8,b:1.8,c:1.8,alpha:90,beta:90,gamma:90},cvoroviFrakcioni:[[0,0,0]]},{kljuc:"kubna-I",naziv:"Тесерална просторно центрирана (I)",sistem:"Тесерални",centriranje:"I",brojCvorova:2,celija:{a:1.8,b:1.8,c:1.8,alpha:90,beta:90,gamma:90},cvoroviFrakcioni:[[0,0,0],[.5,.5,.5]],primitivniVektori:[[-.5,.5,.5],[.5,-.5,.5],[.5,.5,-.5]]},{kljuc:"kubna-F",naziv:"Тесерална површински центрирана (F)",sistem:"Тесерални",centriranje:"F",brojCvorova:4,celija:{a:1.8,b:1.8,c:1.8,alpha:90,beta:90,gamma:90},cvoroviFrakcioni:[[0,0,0],[0,.5,.5],[.5,0,.5],[.5,.5,0]],primitivniVektori:[[0,.5,.5],[.5,0,.5],[.5,.5,0]]},{kljuc:"tetragonalna-P",naziv:"Тетрагонална примитивна (P)",sistem:"Тетрагонални",centriranje:"P",brojCvorova:1,celija:{a:1.6,b:1.6,c:2.3,alpha:90,beta:90,gamma:90},cvoroviFrakcioni:[[0,0,0]]},{kljuc:"tetragonalna-I",naziv:"Тетрагонална просторно центрирана (I)",sistem:"Тетрагонални",centriranje:"I",brojCvorova:2,celija:{a:1.6,b:1.6,c:2.3,alpha:90,beta:90,gamma:90},cvoroviFrakcioni:[[0,0,0],[.5,.5,.5]],primitivniVektori:[[-.5,.5,.5],[.5,-.5,.5],[.5,.5,-.5]]},{kljuc:"ortorombicna-P",naziv:"Ромбична примитивна (P)",sistem:"Ромбични",centriranje:"P",brojCvorova:1,celija:{a:1.4,b:1.9,c:2.4,alpha:90,beta:90,gamma:90},cvoroviFrakcioni:[[0,0,0]]},{kljuc:"ortorombicna-C",naziv:"Ромбична базно центрирана (C)",sistem:"Ромбични",centriranje:"C",brojCvorova:2,celija:{a:1.4,b:1.9,c:2.4,alpha:90,beta:90,gamma:90},cvoroviFrakcioni:[[0,0,0],[.5,.5,0]],primitivniVektori:[[.5,.5,0],[-.5,.5,0],[0,0,1]]},{kljuc:"ortorombicna-I",naziv:"Ромбична просторно центрирана (I)",sistem:"Ромбични",centriranje:"I",brojCvorova:2,celija:{a:1.4,b:1.9,c:2.4,alpha:90,beta:90,gamma:90},cvoroviFrakcioni:[[0,0,0],[.5,.5,.5]],primitivniVektori:[[-.5,.5,.5],[.5,-.5,.5],[.5,.5,-.5]]},{kljuc:"ortorombicna-F",naziv:"Ромбична површински центрирана (F)",sistem:"Ромбични",centriranje:"F",brojCvorova:4,celija:{a:1.4,b:1.9,c:2.4,alpha:90,beta:90,gamma:90},cvoroviFrakcioni:[[0,0,0],[0,.5,.5],[.5,0,.5],[.5,.5,0]],primitivniVektori:[[0,.5,.5],[.5,0,.5],[.5,.5,0]]},{kljuc:"heksagonalna-P",naziv:"Хексагонална примитивна (P)",sistem:"Хексагонални",centriranje:"P",brojCvorova:1,celija:{a:1.8,b:1.8,c:2.2,alpha:90,beta:90,gamma:120},cvoroviFrakcioni:[[0,0,0]]},{kljuc:"romboedarska-R",naziv:"Ромбоедарска (R, хексагонална поставка)",sistem:"Тригонални",centriranje:"R",brojCvorova:3,celija:{a:1.8,b:1.8,c:2.5,alpha:90,beta:90,gamma:120},cvoroviFrakcioni:[[0,0,0],[2/3,1/3,1/3],[1/3,2/3,2/3]],primitivniVektori:[[2/3,1/3,1/3],[-1/3,1/3,1/3],[-1/3,-2/3,1/3]]},{kljuc:"monoklinicna-P",naziv:"Моноклинична примитивна (P)",sistem:"Моноклинични",centriranje:"P",brojCvorova:1,celija:{a:1.5,b:1.8,c:2.1,alpha:90,beta:110,gamma:90},cvoroviFrakcioni:[[0,0,0]]},{kljuc:"monoklinicna-C",naziv:"Моноклинична базно центрирана (C)",sistem:"Моноклинични",centriranje:"C",brojCvorova:2,celija:{a:1.5,b:1.8,c:2.1,alpha:90,beta:110,gamma:90},cvoroviFrakcioni:[[0,0,0],[.5,.5,0]],primitivniVektori:[[.5,.5,0],[-.5,.5,0],[0,0,1]]},{kljuc:"triklinicna-P",naziv:"Триклинична примитивна (P)",sistem:"Триклинични",centriranje:"P",brojCvorova:1,celija:{a:1.4,b:1.7,c:2.1,alpha:78,beta:108,gamma:102},cvoroviFrakcioni:[[0,0,0]]}],Ym={imaPodrazumevanuAnimaciju(){return!0},pocetnaKamera(){return{theta:.65,phi:1.15,udaljenost:6.8}},kreiraj(n,e){let t=e.resetka==="sve"?"kubna-P":e.resetka;const i=new Qe;n.scena3D.add(i);const r=new Yt(.08,16,16),a=new ft({color:new oe(n.tema.token("--primary")),roughness:.25,metalness:.2}),s=new ft({color:new oe(n.tema.token("--accent")),roughness:.25,metalness:.2}),o=new lt({color:new oe(n.tema.token("--text-secondary")),linewidth:2}),c=new Hu({color:new oe(n.tema.token("--border-color")),dashSize:.15,gapSize:.1}),l=new lt({color:new oe(n.tema.token("--warning")),linewidth:2});function d(p){for(;i.children.length>0;){const U=i.children[0];i.remove(U),Pt(U)}const u=Zr(p.celija),E=new F(...u.va),y=new F(...u.vb),M=new F(...u.vc),A=E.clone().add(y).add(M).multiplyScalar(.5).clone().negate(),b=[[0,0,0],[1,0,0],[1,1,0],[0,1,0],[0,0,1],[1,0,1],[1,1,1],[0,1,1]].map(([U,w,R])=>{const[z,N,B]=An(U,w,R,u);return new F(z,N,B).add(A)}),C=[[0,1],[1,2],[2,3],[3,0],[4,5],[5,6],[6,7],[7,4],[0,4],[1,5],[2,6],[3,7]],v=[];for(const U of C){const w=b[U[0]],R=b[U[1]];v.push(w.x,w.y,w.z,R.x,R.y,R.z)}const x=new Xe;x.setAttribute("position",new je(v,3)),i.add(new ut(x,o));const P=new Set;for(const[U,w,R]of p.cvoroviFrakcioni)for(let z=0;z<=1;z++)for(let N=0;N<=1;N++)for(let B=0;B<=1;B++){const k=U+z,O=w+N,q=R+B;if(k>=-1e-4&&k<=1.0001&&O>=-1e-4&&O<=1.0001&&q>=-1e-4&&q<=1.0001){const K=`${k.toFixed(2)},${O.toFixed(2)},${q.toFixed(2)}`;if(P.has(K))continue;P.add(K);const[le,De,X]=An(k,O,q,u),J=new F(le,De,X).add(A),ae=(z===0||z===1)&&(N===0||N===1)&&(B===0||B===1)&&U===0&&w===0&&R===0,re=new Le(r,ae?a:s);re.position.copy(J),i.add(re)}}if(e.prikazi_susedne_celije){const U=[];for(const z of[-1,0,1])for(const N of[-1,0,1])for(const B of[-1,0,1]){if(z===0&&N===0&&B===0)continue;const k=E.clone().multiplyScalar(z).add(y.clone().multiplyScalar(N)).add(M.clone().multiplyScalar(B));for(const O of C){const q=b[O[0]].clone().add(k),K=b[O[1]].clone().add(k);U.push(q.x,q.y,q.z,K.x,K.y,K.z)}}const w=new Xe;w.setAttribute("position",new je(U,3));const R=new ut(w,c);R.computeLineDistances(),i.add(R)}if(e.prikazi_primitivnu_celiju&&p.primitivniVektori){const U=[],w=b[0],R=p.primitivniVektori.map(([q,K,le])=>{const[De,X,J]=An(q,K,le,u);return new F(De,X,J)}),z=R[0],N=R[1],B=R[2],k=[w,w.clone().add(z),w.clone().add(z).add(N),w.clone().add(N),w.clone().add(B),w.clone().add(z).add(B),w.clone().add(z).add(N).add(B),w.clone().add(N).add(B)];for(const q of C){const K=k[q[0]],le=k[q[1]];U.push(K.x,K.y,K.z,le.x,le.y,le.z)}const O=new Xe;O.setAttribute("position",new je(U,3)),i.add(new ut(O,l))}}const h=document.createElement("div");h.className="udzbenik-scena-status",n.podnozje.append(h);function f(p){h.textContent=`${p.naziv} • Систем: ${p.sistem} • Чворова по конвенционалној ћелији: ${p.brojCvorova}`}if(e.resetka==="sve"){const p=document.createElement("div");p.className="udzbenik-bravais-traka",p.style.display="flex",p.style.flexWrap="wrap",p.style.gap="4px";for(const u of za){const E=document.createElement("button");E.type="button",E.className="udzbenik-dugme udzbenik-dugme--malo",u.kljuc===t&&E.classList.add("udzbenik-dugme--aktivno"),E.textContent=u.kljuc,E.setAttribute("aria-label",u.naziv),E.addEventListener("click",()=>{t=u.kljuc,p.querySelectorAll("button").forEach(y=>y.classList.remove("udzbenik-dugme--aktivno")),E.classList.add("udzbenik-dugme--aktivno"),d(u),f(u)}),p.append(E)}n.gornjeKontrole.append(p)}const m=za.find(p=>p.kljuc===t)??za[0];d(m),f(m);function g(){a.color.set(n.tema.token("--primary")),s.color.set(n.tema.token("--accent")),o.color.set(n.tema.token("--text-secondary")),c.color.set(n.tema.token("--border-color")),l.color.set(n.tema.token("--warning"))}let _=0;return{azuriraj(p){_+=p*.45,i.rotation.y=_},korak(){_+=.25,i.rotation.y=_},resetuj(){_=0,i.rotation.set(0,0,0)},osveziTemu(){g()},raspolazi(){r.dispose(),a.dispose(),s.dispose(),o.dispose(),c.dispose(),l.dispose(),Pt(i),h.remove()}}}};function Zm(n,e){const t=e??56,i=Math.round((180-t)*10)/10;switch(n){case"kubna":return{naziv:"Кубна цепљивост {100}",brojPravaca:"3 правца",uglovi:"90°",podrazumevaniPrimer:"халит, галенит"};case"oktaedarska":return{naziv:"Октаедарска цепљивост {111}",brojPravaca:"4 правца",uglovi:"70,5° и 109,5°",podrazumevaniPrimer:"флуорит, дијамант"};case"dodekaedarska":return{naziv:"Додекаедарска цепљивост {110}",brojPravaca:"6 праваца",uglovi:"60°, 90° и 120°",podrazumevaniPrimer:"сфалерит"};case"romboedarska":return{naziv:"Ромбоедарска цепљивост {101̄1}",brojPravaca:"3 правца",uglovi:"~75° и ~105° (≠ 90°)",podrazumevaniPrimer:"калцит, доломит"};case"bazalna":return{naziv:"Базална (пинакоидална) цепљивост {001}",brojPravaca:"1 правац",uglovi:"паралелне ламеле (0°)",podrazumevaniPrimer:"лискун (мусковит), графит"};case"prizmatska":return{naziv:"Призматска цепљивост {110}",brojPravaca:"2 правца",uglovi:`${t}° и ${i}°`,podrazumevaniPrimer:t>75?"пироксен":"амфибол"};case"nema":return{naziv:"Нема цепљивости (шкољкаст прелом)",brojPravaca:"0 праваца",uglovi:"нема равни цепљивости",podrazumevaniPrimer:"кварц"}}}function Wn(n,e,t,i){const r=er(n);if(r.pljosni.length<4||r.temena.length<4)return null;const a=tr(r),s=new Qe;return s.add(new Le(a.geometrijaMreze,t),new ut(a.geometrijaIvica,i)),{grupa:s,smerRazdvajanja:e}}function ln(n,e,t,i,r){const a=new ii(t,t),s=new Le(a,i),o=new ut(new Qi(a),r),c=new Qe;c.add(s,o);const l=new F(...n).normalize();return c.quaternion.setFromUnitVectors(new F(0,0,1),l),c.position.copy(l).multiplyScalar(e),c}function Ei(n,e){const t=Math.hypot(n-.35,e-.25),i=.055*Math.sin(t*13.5);return .28*(n*n-.5*e*e)+.18*n+i}function Jm(n,e,t,i){if(!n){const h=[{normala:[0,-1,0],d:1.15}];for(let m=0;m<6;m++){const g=m*Math.PI/3,_=Math.cos(g),p=Math.sin(g);h.push({normala:[_,0,p],d:.95}),h.push({normala:[_*.72,.69,p*.72],d:1.28}),h.push({normala:[_*.72,-.69,p*.72],d:1.28})}const f=Wn(h,new F(0,0,0),e,i);return{fragmenti:f?[f]:[]}}const o=12,c=24;function l(h,f){const m=(f%(Math.PI/3)+Math.PI/3)%(Math.PI/3)-Math.PI/6,g=.95*Math.cos(Math.PI/6)/Math.cos(m);return[h*g*Math.cos(f),h*g*Math.sin(f)]}function d(h){const f=[],m=[],g=[],_=h?1.15:-1.15,p=h?1.85:-1.85;for(let D=0;D<o;D++){const A=D/o,b=(D+1)/o;for(let C=0;C<c;C++){const v=C/c*Math.PI*2,x=(C+1)/c*Math.PI*2,[P,U]=l(A,v),[w,R]=l(b,v),[z,N]=l(b,x),[B,k]=l(A,x),O=Ei(P,U),q=Ei(w,R),K=Ei(z,N),le=Ei(B,k);h?m.push(P,O,U,z,K,N,w,q,R,P,O,U,B,le,k,z,K,N):m.push(P,O,U,w,q,R,z,K,N,P,O,U,z,K,N,B,le,k)}}for(let D=0;D<c;D++){const A=D/c*Math.PI*2,b=(D+1)/c*Math.PI*2,[C,v]=l(1,A),[x,P]=l(1,b),U=Ei(C,v),w=Ei(x,P);h?(f.push(C,U,v,x,w,P,x,_,P,C,U,v,x,_,P,C,_,v),f.push(C,_,v,x,_,P,0,p,0)):(f.push(C,_,v,x,_,P,x,w,P,C,_,v,x,w,P,C,U,v),f.push(x,_,P,C,_,v,0,p,0)),g.push(C,U,v,x,w,P),g.push(C,_,v,x,_,P),D%(c/6)===0&&(g.push(C,U,v,C,_,v),g.push(C,_,v,0,p,0))}const u=new Xe;u.setAttribute("position",new je(f,3)),u.computeVertexNormals();const E=new Xe;E.setAttribute("position",new je(m,3)),E.computeVertexNormals();const y=new Xe;y.setAttribute("position",new je(g,3));const M=new Qe;return M.add(new Le(u,e),new Le(E,t),new ut(y,i)),M}return{fragmenti:[{grupa:d(!0),smerRazdvajanja:new F(.18,.55,.1)},{grupa:d(!1),smerRazdvajanja:new F(-.18,-.55,-.1)}]}}const vc=.4;function xc(n){return Ys(n.token("--primary"),[n.token("--accent"),n.token("--warning"),n.token("--info"),n.token("--success")])}const Qm={izgled:"kristal",imaPodrazumevanuAnimaciju(n){return!(n.vrsta==="nema"&&!n.prikazi_prelom)},pocetnaKamera(){return{theta:.68,phi:1.14,udaljenost:5.9}},kreiraj(n,e){const t=e.vrsta,i=e.ugao??56,r=e.prikazi_prelom??!1,a=new Qe,s=new Qe,o=new Qe;a.add(s,o),n.scena3D.add(a);const c=xc(n.tema),l=ni(n.tema.token("--primary"),{providnost:.45}),d=ni(c,{providnost:.6});d.flatShading=!1;const h=nr(n.tema.token("--text-primary"),n.tema.token("--primary")),f=new Ln({color:c.clone(),transparent:!0,opacity:vc,side:St,depthWrite:!1}),m=new lt({color:c.clone()}),g=[];function _(){if(t==="kubna"){const b=[-1,1];for(const C of b)for(const v of b)for(const x of b){const P=[{normala:[C,0,0],d:1.05},{normala:[-C,0,0],d:0},{normala:[0,v,0],d:1.05},{normala:[0,-v,0],d:0},{normala:[0,0,x],d:1.05},{normala:[0,0,-x],d:0}],U=Wn(P,new F(C,v,x).normalize().multiplyScalar(.52),l,h);U&&g.push(U)}o.add(ln([1,0,0],0,2.6,f,m),ln([0,1,0],0,2.6,f,m),ln([0,0,1],0,2.6,f,m))}else if(t==="oktaedarska"){const b=ro([1,1,1]).map(v=>({normala:v.normala,d:1.08})),C=[[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]];for(let v=0;v<16;v++){const x=[...b],P=new F;for(let w=0;w<4;w++){const R=(v&1<<w)!==0?1:-1,z=C[w];x.push({normala:[z[0]*R,z[1]*R,z[2]*R],d:0}),P.add(new F(z[0]*R,z[1]*R,z[2]*R))}const U=Wn(x,P.lengthSq()>1e-4?P.normalize().multiplyScalar(.52):P,l,h);U&&g.push(U)}for(const v of C)o.add(ln(v,0,2.8,f,m))}else if(t==="dodekaedarska"){const b=ro([1,1,0]).map(x=>({normala:x.normala,d:1.12})),C=[[1,1,0],[1,-1,0],[1,0,1],[1,0,-1],[0,1,1],[0,1,-1]];for(const x of C)o.add(ln(x,0,2.7,f,m));const v=[[1,1,0],[1,-1,0],[0,1,1]];for(let x=0;x<8;x++){const P=[...b],U=new F;for(let R=0;R<3;R++){const z=(x&1<<R)!==0?1:-1,N=v[R];P.push({normala:[N[0]*z,N[1]*z,N[2]*z],d:0}),U.add(new F(N[0]*z,N[1]*z,N[2]*z))}const w=Wn(P,U.normalize().multiplyScalar(.5),l,h);w&&g.push(w)}}else if(t==="romboedarska"){const b=[1,.26,.14],C=[.24,1,.22],v=[.18,.26,1],x=[b,C,v],P=[];for(const w of x)P.push({normala:w,d:1}),P.push({normala:[-w[0],-w[1],-w[2]],d:1}),o.add(ln(w,0,2.8,f,m));const U=[-1,1];for(const w of U)for(const R of U)for(const z of U){const N=[...P,{normala:[-b[0]*w,-b[1]*w,-b[2]*w],d:0},{normala:[-C[0]*R,-C[1]*R,-C[2]*R],d:0},{normala:[-v[0]*z,-v[1]*z,-v[2]*z],d:0}],B=new F(b[0]*w+C[0]*R+v[0]*z,b[1]*w+C[1]*R+v[1]*z,b[2]*w+C[2]*R+v[2]*z).normalize().multiplyScalar(.5),k=Wn(N,B,l,h);k&&g.push(k)}}else if(t==="bazalna"){const b=[];for(let P=0;P<6;P++){const U=P*Math.PI/3;b.push({normala:[Math.cos(U),0,Math.sin(U)],d:1.15})}const C=5,v=1.1,x=v/C;for(let P=0;P<C;P++){const U=-v/2+P*x,w=U+x,R=[...b,{normala:[0,1,0],d:w},{normala:[0,-1,0],d:-U}],z=P-(C-1)/2,N=Wn(R,new F(z*.08,z*.28,0),l,h);N&&g.push(N),P>0&&o.add(ln([0,1,0],U,2.7,f,m))}}else if(t==="prizmatska"){const b=i*Math.PI/180*.5,C=[Math.sin(b),0,Math.cos(b)],v=[-Math.sin(b),0,Math.cos(b)],x=[{normala:[0,1,0],d:1.3},{normala:[0,-1,0],d:1.3},{normala:C,d:.9},{normala:[-C[0],0,-C[2]],d:.9},{normala:v,d:.9},{normala:[-v[0],0,-v[2]],d:.9}];o.add(ln(C,0,2.9,f,m),ln(v,0,2.9,f,m));const P=[-1,1];for(const U of P)for(const w of P){const R=[...x,{normala:[-C[0]*U,0,-C[2]*U],d:0},{normala:[-v[0]*w,0,-v[2]*w],d:0}],z=new F(C[0]*U+v[0]*w,0,C[2]*U+v[2]*w).normalize().multiplyScalar(.48),N=Wn(R,z,l,h);N&&g.push(N)}}else{const b=Jm(r,l,d,h);g.push(...b.fragmenti)}for(const b of g)s.add(b.grupa)}_();const p=new Oi().setFromObject(s);if(!p.isEmpty()){const b=Math.max(p.max.x-p.min.x,p.max.z-p.min.z);n.dodajKontaktnuSenku(b*.85+.4,p.min.y-.35)}const u=Zm(t,i),E=e.primer||u.podrazumevaniPrimer,y=document.createElement("div");y.className="udzbenik-scena-info-red udzbenik-cepljivost-meta";const M=[[ot("brojPravacaCepljivosti"),u.brojPravaca],[ot("ugloviCepljivosti"),u.uglovi],[ot("primerMinerala"),E]];for(const[b,C]of M){const v=document.createElement("span");v.className="udzbenik-meta-stavka";const x=document.createElement("strong");x.textContent=`${b}: `;const P=document.createElement("span");P.textContent=C,v.append(x,P),y.append(v)}n.podnozje.append(y);let D=n.smanjenPokret?.72:0;function A(){if(t==="nema"&&!r){o.visible=!1;return}let b=0,C=0;if(D<.3)b=D/.3,C=0;else if(D<.72){b=1;const v=(D-.3)/.42;C=v*v*(3-2*v)}else if(D<.85)b=1,C=1;else{const v=(D-.85)/.15;b=1-v,C=1-v*v*(3-2*v)}o.visible=t!=="nema"&&b>.02,o.scale.setScalar(.25+.75*b),f.opacity=vc*b*(1-.45*C);for(const v of g)v.grupa.position.copy(v.smerRazdvajanja).multiplyScalar(C)}return A(),{azuriraj(b){D=(D+b*.17)%1,n.korisnikUpravlja()||(a.rotation.y+=b*.24),A()},korak(){D=(D+.18)%1,A()},resetuj(){a.rotation.set(0,0,0),D=n.smanjenPokret?.72:0,A()},osveziTemu(b){const C=xc(b);l.color.set(b.token("--primary")),d.color.copy(C),h.color.copy(Ni(b.token("--text-primary"),b.token("--primary"))),f.color.copy(C),m.color.copy(C)},raspolazi(){Pt(a),l.dispose(),d.dispose(),h.dispose(),f.dispose(),m.dispose()}}}},ll=new Map,e0=["m-3m","m-3","-43m","432","4/mmm","6/mmm","6/m","-3m","32","mmm","2/m"];for(const n of e0){let e="kubni";n==="4/mmm"?e="tetragonalni":n==="6/mmm"||n==="6/m"?e="heksagonalni":n==="-3m"||n==="32"?e="trigonalni":n==="mmm"?e="ortorombicni":n==="2/m"&&(e="monoklinicni"),ll.set(n,(t,i)=>Is(t,n,e,i))}const t0=["kubni","tetragonalni","heksagonalni","trigonalni","ortorombicni"];for(const n of t0){const e=Pc(n);ll.set(n,(t,i)=>Is(t,e,n,i))}function n0(n,e,t,i){const r=t??Pc(e);return Is(n,r,e,i)}const i0={izgled:"kristal",imaPodrazumevanuAnimaciju(n){return(n.animacija??"prelaz")!=="nema"},pocetnaKamera(){return{theta:.64,phi:1.12,udaljenost:4.8}},kreiraj(n,e){const t=e.animacija??"prelaz",r=e.forme.map((w,R)=>{const z=`forma-${R}`,N=w.naziv||(w.hkl.length===4?`{${w.hkl.join(" ")}}`:vl(w.hkl)),B=n0(w.hkl,e.sistem,e.klasa,e.celija);return{grupaId:z,oznakaForme:N,baznoD:w.d,hkl:w.hkl,ekvivalentne:B}}),a=new Qe;n.scena3D.add(a),n.dodajKontaktnuSenku(1.7,-1.6);const s=nr(n.tema.token("--text-primary"),n.tema.token("--primary")),o=r.map((w,R)=>{const z=ni(n.tema.token("--primary"));return z.name=`mat-forma-${R}`,z});let c=null,l=null,d="";function h(){const w=new oe(n.tema.token("--primary")),R=Ys(w,[n.tema.token("--accent"),n.tema.token("--info"),n.tema.token("--success")]),z=new oe(n.tema.token("--bg-elevated"));for(let N=0;N<o.length;N++){const B=o[N],k=r[N].grupaId,O=r.length>1?N/(r.length-1):0,q=w.clone().lerp(R,O);N%2===1&&r.length>2&&q.lerp(z,.22),B.color.copy(q);const K=c===k;B.emissive.copy(K?q.clone().multiplyScalar(.28):new oe(0,0,0))}s.color.copy(Ni(n.tema.token("--text-primary"),w))}h();const f=document.createElement("div");f.className="udzbenik-scena-etiketa udzbenik-scena-etiketa--istaknuta",f.hidden=!0,n.slojEtiketa.append(f);let m=.5,g=n.smanjenPokret?.25:0,_=null;if(r.length>1){const w=document.createElement("label");w.className="udzbenik-klizac-oznaka";const R=document.createElement("span");R.textContent=`${ot("prelazFormi")}: ${r[0].oznakaForme} ↔ ${r[r.length-1].oznakaForme}`,_=document.createElement("input"),_.type="range",_.min="0",_.max="1",_.step="0.01",_.value="0.5",_.className="udzbenik-klizac",_.addEventListener("input",()=>{m=Number(_.value),v(m),n.zatraziRender()}),w.append(R,_),n.gornjeKontrole.append(w)}const p=document.createElement("div");p.className="udzbenik-habitus-forme";const u=new Map;for(const w of r){const R=document.createElement("button");R.type="button",R.className="udzbenik-mohs-cip",R.textContent=w.oznakaForme;const z=()=>{c=w.grupaId;const N=D?.pljosni.find(B=>B.grupaId===w.grupaId);N?(l=new F(...N.centar),d=`${w.oznakaForme} · ${N.oznaka}`):(l=null,d=w.oznakaForme),h(),b(),n.zatraziRender()};R.addEventListener("click",z),R.addEventListener("focus",z),R.addEventListener("blur",()=>{c===w.grupaId&&(c=null,l=null,h(),b(),n.zatraziRender())}),u.set(w.grupaId,R),p.append(R)}const E=document.createElement("span");E.className="udzbenik-habitus-status",p.append(E),n.podnozje.append(p);let y=null,M=null,D=null,A=[];function b(){if(!D)return;const w=D.pljosni.length,R=D.temena.length,z=e.primer?` · ${ot("primerMinerala")}: ${e.primer}`:"",N=d&&c?` · ${d}`:"";E.textContent=`${w} пљосни, ${R} темена${z}${N}`;for(const[B,k]of u.entries()){const O=D.pljosni.some(q=>q.grupaId===B);k.classList.toggle("udzbenik-mohs-cip--aktivan",c===B),k.classList.toggle("udzbenik-mohs-cip--prigusen",!O)}}function C(w){const R=r.length;return R<=1?r.map(z=>z.baznoD):r.map((z,N)=>{const B=N/(R-1);let k=1;return w<.5?k=1+(.5-w)*2*B*.95:w>.5&&(k=1+(w-.5)*2*(1-B)*.95),z.baznoD*k})}function v(w){y&&(y.geometry.dispose(),a.remove(y)),M&&(M.geometry.dispose(),a.remove(M));const R=C(w),z=[];for(let K=0;K<r.length;K++){const le=r[K],De=R[K];for(const X of le.ekvivalentne)z.push({normala:X.normala,d:De,grupaId:le.grupaId,oznaka:X.oznaka})}const N=er(z);let B=.001;for(const K of N.temena)B=Math.max(B,Math.hypot(K[0],K[1],K[2]));const k=1.48/B;for(const K of N.temena)K[0]*=k,K[1]*=k,K[2]*=k;for(const K of N.pljosni)K.centar[0]*=k,K.centar[1]*=k,K.centar[2]*=k;const O=tr(N),q=O.redosledGrupa.map(K=>{const le=r.findIndex(De=>De.grupaId===K);return o[Math.max(0,le)]});y=new Le(O.geometrijaMreze,q),M=new ut(O.geometrijaIvica,s),a.add(y,M),D=N,A=O.mapaTrougaoUPljosan,b()}const x=new Ks,P=new We,U=w=>{if(!y||!D)return;const R=n.platno.getBoundingClientRect();if(R.width<=0||R.height<=0)return;P.x=(w.clientX-R.left)/R.width*2-1,P.y=-((w.clientY-R.top)/R.height)*2+1,x.setFromCamera(P,n.kamera);const z=x.intersectObject(y,!1);if(z.length>0&&z[0].faceIndex!==void 0&&z[0].faceIndex!==null){const N=A[z[0].faceIndex],B=N!==void 0?D.pljosni[N]:void 0;if(B){const k=r.find(O=>O.grupaId===B.grupaId);c=B.grupaId,l=new F(...B.centar),d=`${k?.oznakaForme??B.grupaId} · ${B.oznaka}`,h(),b(),n.zatraziRender();return}}c!==null&&w.pointerType==="mouse"&&(c=null,l=null,h(),b(),n.zatraziRender())};return n.platno.addEventListener("pointermove",U),v(m),{azuriraj(w){t==="prelaz"&&r.length>1?(g=(g+w*.14)%1,m=.5-.5*Math.cos(g*Math.PI*2),_&&(_.value=m.toFixed(2)),n.korisnikUpravlja()||(a.rotation.y+=w*.25),v(m)):t==="rotacija"&&!n.korisnikUpravlja()&&(a.rotation.y+=w*.42)},korak(){t==="prelaz"&&r.length>1?(g=(g+.125)%1,m=.5-.5*Math.cos(g*Math.PI*2),_&&(_.value=m.toFixed(2)),v(m)):a.rotation.y+=.35},resetuj(){a.rotation.set(0,0,0),m=.5,g=.25,_&&(_.value="0.5"),c=null,l=null,h(),v(.5)},osveziTemu(){h()},posleRendera(){if(!c||!l){f.hidden=!0;return}a.updateMatrixWorld(!0);const w=l.clone().applyMatrix4(a.matrixWorld),R=n.projektujU2D(w);if(!R.vidljivo){f.hidden=!0;return}f.textContent=d,f.hidden=!1,f.style.transform=`translate(-50%, -120%) translate(${R.x.toFixed(1)}px, ${R.y.toFixed(1)}px)`},raspolazi(){n.platno.removeEventListener("pointermove",U),Pt(a),s.dispose();for(const w of o)w.dispose()}}}},Tn=.8;function Yi(n,e){return n.map(([t,i,r])=>{const a=Math.hypot(t,i,r)||1;return[t/a*e,i/a*e,r/a*e]})}const Mc=2/Math.sqrt(3)-1,Sc=Math.sqrt(1.5)-1,Ec=Math.SQRT2-1,yc=Math.sqrt(3)-1,bc=1,Tc={2:{kb:2,nazivOblika:"Линеарни",granicniOdnos:.155,vrhovi:[[0,0,Tn*(1+.155)],[0,0,-Tn*(1+.155)]],trougloviIndeksi:[]},3:{kb:3,nazivOblika:"Троугаони",granicniOdnos:Mc,vrhovi:Yi([[1,0,0],[-.5,Math.sqrt(3)/2,0],[-.5,-Math.sqrt(3)/2,0]],Tn*(1+Mc)),trougloviIndeksi:[0,1,2]},4:{kb:4,nazivOblika:"Тетраедарски",granicniOdnos:Sc,vrhovi:Yi([[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]],Tn*(1+Sc)),trougloviIndeksi:[0,1,2,0,3,1,0,2,3,1,3,2]},6:{kb:6,nazivOblika:"Октаедарски",granicniOdnos:Ec,vrhovi:Yi([[1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,1],[0,0,-1]],Tn*(1+Ec)),trougloviIndeksi:[0,2,4,2,1,4,1,3,4,3,0,4,0,5,2,2,5,1,1,5,3,3,5,0]},8:{kb:8,nazivOblika:"Хексаедарски",granicniOdnos:yc,vrhovi:Yi([[-1,-1,-1],[1,-1,-1],[1,1,-1],[-1,1,-1],[-1,-1,1],[1,-1,1],[1,1,1],[-1,1,1]],Tn*(1+yc)),trougloviIndeksi:[0,2,1,0,3,2,4,5,6,4,6,7,0,1,5,0,5,4,1,2,6,1,6,5,2,3,7,2,7,6,3,0,4,3,4,7]},12:{kb:12,nazivOblika:"Кубооктаедарски",granicniOdnos:bc,vrhovi:Yi([[1,1,0],[1,-1,0],[-1,-1,0],[-1,1,0],[1,0,1],[1,0,-1],[-1,0,-1],[-1,0,1],[0,1,1],[0,1,-1],[0,-1,-1],[0,-1,1]],Tn*(1+bc)),trougloviIndeksi:[0,8,4,1,4,11,2,11,7,3,7,8,0,5,9,1,10,5,2,6,10,3,9,6,0,4,1,0,1,5,2,7,3,2,3,6,8,9,3,8,3,0,11,1,2,11,2,10]}},r0={izgled:"kristal",imaPodrazumevanuAnimaciju(n){return n.prikazi_odnos_radijusa!==!1},pocetnaKamera(){return{theta:.65,phi:1.18,udaljenost:5.4}},kreiraj(n,e){const t=new Qe;n.scena3D.add(t);const i=Tc[e.kb]??Tc[4],r=Tn,a=r*i.granicniOdnos,s=new Yt(a,24,24),o=new ft({color:new oe(n.tema.token("--accent")),roughness:.25,metalness:.2}),c=new Le(s,o);t.add(c);const l=new Yt(r,24,24),d=new ft({color:new oe(n.tema.token("--primary")),roughness:.35,metalness:.1,transparent:!0,opacity:.85}),h=new Qe;for(const[A,b,C]of i.vrhovi){const v=new Le(l,d);v.position.set(A,b,C),h.add(v)}t.add(h);let f=null,m=null;const g=ni(n.tema.token("--primary"),{providnost:.35}),_=new lt({color:new oe(n.tema.token("--text-secondary")),linewidth:2});if(i.trougloviIndeksi.length>=3){const A=new Xe,b=[];for(const v of i.trougloviIndeksi){const x=i.vrhovi[v];b.push(x[0],x[1],x[2])}A.setAttribute("position",new je(b,3)),A.computeVertexNormals(),f=new Le(A,g),t.add(f);const C=new Qi(A);m=new ut(C,_),t.add(m)}const p=e.katjon||"Katjon",u=e.anjon||"Anjon",E=document.createElement("div");E.className="udzbenik-scena-status",E.textContent=`КБ = ${i.kb} (${i.nazivOblika}) • Гранични однос RA/RX = ${i.granicniOdnos.toFixed(3)} • ${p} / ${u}`,n.podnozje.append(E);let y=0;const M=e.prikazi_odnos_radijusa!==!1;function D(){o.color.set(n.tema.token("--accent")),d.color.set(n.tema.token("--primary")),g.color.set(n.tema.token("--primary")),_.color.set(n.tema.token("--text-secondary"))}return{azuriraj(A){if(y+=A,t.rotation.y=y*.35,M){const b=Math.sin(y*1.8);if(b<-.2){const C=.08*(Math.abs(b)-.2);c.position.set(Math.sin(y*22)*C,Math.cos(y*19)*C,Math.sin(y*25)*C),c.scale.setScalar(.72)}else c.position.set(0,0,0),c.scale.setScalar(1)}},korak(){y+=.3,t.rotation.y+=.2},resetuj(){y=0,c.position.set(0,0,0),c.scale.setScalar(1),t.rotation.set(0,0,0)},osveziTemu(){D()},raspolazi(){s.dispose(),o.dispose(),l.dispose(),d.dispose(),f&&f.geometry.dispose(),m&&m.geometry.dispose(),g.dispose(),_.dispose(),Pt(t),E.remove()}}}},a0={imaPodrazumevanuAnimaciju(){return!1},pocetnaKamera(n){return{theta:.65,phi:1.12,udaljenost:(n.prikaz??"celija")==="supercelija"?8.2:6.2}},kreiraj(n,e){const t=e.prikaz??"celija",i=e.stil??"kugle-stapici",r=e.prikazi_celiju??!0,a=e.oznake_atoma??!0,s=e.poluprecnici??"jonski";let o=!1,c=1.15,l=null,d=-1;const h=new Qe,f=new Qe,m=new Qe,g=new Qe;h.add(g,m,f),n.scena3D.add(h);const _=new lt({color:new oe(n.tema.token("--text-secondary"))}),p=new ft({color:new oe(n.tema.token("--text-muted")),roughness:.45,metalness:.15}),u=new Ln({color:new oe(n.tema.token("--accent")),wireframe:!0}),E=new Le(new Yt(1,14,12),u);E.visible=!1,h.add(E);const y=document.createElement("div");y.className="udzbenik-scena-etiketa udzbenik-scena-etiketa--atom",y.hidden=!0,n.slojEtiketa.append(y);const M=document.createElement("div");if(M.className="udzbenik-struktura-kontrole",i==="kugle-stapici"){const B=document.createElement("label");B.className="udzbenik-klizac-oznaka";const k=document.createElement("span");k.textContent=`${ot("faktorVeza")}: ×1,15`;const O=document.createElement("input");O.type="range",O.min="0.85",O.max="1.40",O.step="0.05",O.value="1.15",O.className="udzbenik-klizac",O.addEventListener("input",()=>{c=Number(O.value),k.textContent=`${ot("faktorVeza")}: ×${c.toFixed(2).replace(".",",")}`,l&&(w(l),n.zatraziRender())}),B.append(k,O),M.append(B)}const D=document.createElement("span");if(D.className="udzbenik-atom-status",D.setAttribute("aria-live","polite"),a){const B=document.createElement("button");B.type="button",B.className="udzbenik-dugme udzbenik-dugme--malo",B.textContent=ot("sledeciAtom"),B.addEventListener("click",()=>{A.length!==0&&(d=(d+1)%A.length,x(d),n.zatraziRender())}),M.append(B,D)}M.childNodes.length>0&&n.gornjeKontrole.append(M);let A=[],b=null,C=new F,v=1;function x(B){if(B<0||B>=A.length){b=null,E.visible=!1,y.hidden=!0,D.textContent="";return}const k=A[B];b=k.atom;const O=k.mesh.scale.x*1.25;E.position.copy(k.mesh.position),E.scale.setScalar(O),E.visible=!0;const q=`(${k.atom.fx.toFixed(3)}, ${k.atom.fy.toFixed(3)}, ${k.atom.fz.toFixed(3)})`;y.textContent=`${k.atom.simbol} [${k.atom.oznaka}] ${q}`,D.textContent=`${k.atom.simbol} (${k.atom.oznaka}): ${q}`}function P(B){Pt(B),B.clear()}function U(B){n.podnozje.replaceChildren();const k=document.createElement("div");k.className="udzbenik-cpk-legenda",k.setAttribute("aria-label",ot("legendaElemenata"));const O=document.createElement("div");O.className="udzbenik-cpk-stavke";let q=!1;for(const De of B){const X=ao(De),J=so(De,s);s==="jonski"&&J.koriscenaVrsta==="kovalentni"&&(q=!0);const ae=document.createElement("span");ae.className="udzbenik-cpk-cip";const re=document.createElement("span");re.className="udzbenik-cpk-boja",re.style.backgroundColor=X.bojaHex,re.setAttribute("aria-hidden","true");const ue=J.koriscenaVrsta==="jonski"&&J.jon?`${X.simbol} (${J.jon})`:X.simbol,Pe=J.poluprecnik.toFixed(2).replace(".",","),fe=document.createElement("span");fe.textContent=`${ue} — ${X.naziv} (r = ${Pe} Å)`,ae.append(re,fe),O.append(ae)}const K=document.createElement("p");K.className="udzbenik-scena-izvor";const le=i==="kugle-stapici"?` · ${ot("detekcijaVezaKovalentniOznaka")}${c.toFixed(2).replace(".",",")}`:"";if(s==="jonski"){const De=q?`${oo.izvor}; ${ot("kovalentnaRezervaOznaka")}: ${co}`:oo.izvor;K.textContent=`${ot("poluprecniciJonskiOznaka")} (${ot("izvorPodataka")}: ${De})${le}`}else K.textContent=`${ot("poluprecniciKovalentniOznaka")} (${ot("izvorPodataka")}: ${co})${le}`;k.append(O,K),n.podnozje.append(k)}function w(B){P(f),P(m),P(g),A=[];const k=Zr(B.celija),O=t==="supercelija"?2:1,q=An(O,O,O,k);C=new F(q[0]*.5,q[1]*.5,q[2]*.5);const K=Math.max(B.celija.a*O,B.celija.b*O,B.celija.c*O);v=3.6/Math.max(1,K);const le=[],De=new Set,X=[];for(const ue of B.atomi){X.includes(ue.simbol)||X.push(ue.simbol);const Pe=ao(ue.simbol),fe=so(ue.simbol,s),te=(ue.fx%1+1)%1,se=(ue.fy%1+1)%1,W=(ue.fz%1+1)%1,L=te<.001?[0,1]:[0],Ee=se<.001?[0,1]:[0],Se=W<.001?[0,1]:[0];for(let _e=0;_e<O;_e++)for(let ve=0;ve<O;ve++)for(let Ne=0;Ne<O;Ne++)for(const Re of L)for(const I of Ee)for(const S of Se){const j=te+_e+Re,ee=se+ve+I,ie=W+Ne+S;if(j>O+.001||ee>O+.001||ie>O+.001)continue;const Q=`${j.toFixed(3)},${ee.toFixed(3)},${ie.toFixed(3)},${ue.simbol}`;if(De.has(Q))continue;De.add(Q);const Ce=An(j,ee,ie,k);le.push({oznaka:ue.oznaka,simbol:ue.simbol,fx:j,fy:ee,fz:ie,pozicija:new F(Ce[0],Ce[1],Ce[2]),poluprecnikPrikaza:fe.poluprecnik,kovalentniPoluprecnik:Pe.kovalentniPoluprecnik,bojaHex:Pe.bojaHex})}}const J=new Yt(1,20,16),ae=new Map,re=i==="kugle"?.52:.25;for(const ue of le){let Pe=ae.get(ue.simbol);Pe||(Pe=new ft({color:new oe(ue.bojaHex),roughness:.32,metalness:.1}),ae.set(ue.simbol,Pe));const fe=new Le(J,Pe);fe.position.copy(ue.pozicija).sub(C).multiplyScalar(v);const te=Math.max(.045,ue.poluprecnikPrikaza*re*v);fe.scale.setScalar(te),f.add(fe),A.push({mesh:fe,atom:ue})}if(i==="kugle-stapici"){const ue=new ar(1,1,1,10,1),Pe=new F(0,1,0),fe=Math.max(.035,.09*v);for(let te=0;te<le.length;te++){const se=le[te];for(let W=te+1;W<le.length;W++){const L=le[W],Ee=se.pozicija.distanceTo(L.pozicija),Se=(se.kovalentniPoluprecnik+L.kovalentniPoluprecnik)*c;if(Ee>.35&&Ee<=Se){const _e=A[te].mesh.position,Ne=A[W].mesh.position.clone().sub(_e),Re=Ne.length();if(Re<1e-4)continue;const I=new Le(ue,p.clone());I.position.copy(_e).addScaledVector(Ne,.5),I.quaternion.setFromUnitVectors(Pe,Ne.clone().normalize()),I.scale.set(fe,Re,fe),m.add(I)}}}ue.dispose()}if(r){const ue=[],Pe=[[[0,0,0],[1,0,0]],[[1,0,0],[1,1,0]],[[1,1,0],[0,1,0]],[[0,1,0],[0,0,0]],[[0,0,1],[1,0,1]],[[1,0,1],[1,1,1]],[[1,1,1],[0,1,1]],[[0,1,1],[0,0,1]],[[0,0,0],[0,0,1]],[[1,0,0],[1,0,1]],[[1,1,0],[1,1,1]],[[0,1,0],[0,1,1]]];for(let te=0;te<O;te++)for(let se=0;se<O;se++)for(let W=0;W<O;W++)for(const[L,Ee]of Pe){const Se=An(L[0]+te,L[1]+se,L[2]+W,k),_e=An(Ee[0]+te,Ee[1]+se,Ee[2]+W,k),ve=new F(...Se).sub(C).multiplyScalar(v),Ne=new F(..._e).sub(C).multiplyScalar(v);ue.push(ve.x,ve.y,ve.z,Ne.x,Ne.y,Ne.z)}const fe=new Xe;fe.setAttribute("position",new je(ue,3)),g.add(new ut(fe,_.clone()))}U(X),d=-1,x(-1)}const R=new Ks,z=new We,N=B=>{if(!a||A.length===0)return;const k=n.platno.getBoundingClientRect();if(k.width<=0||k.height<=0)return;z.x=(B.clientX-k.left)/k.width*2-1,z.y=-((B.clientY-k.top)/k.height)*2+1,R.setFromCamera(z,n.kamera);const O=R.intersectObjects(A.map(q=>q.mesh),!1);if(O.length>0){const q=O[0].object,K=A.findIndex(le=>le.mesh===q);K!==d&&(d=K,x(K),n.zatraziRender())}else d!==-1&&B.pointerType==="mouse"&&(d=-1,x(-1),n.zatraziRender())};return a&&n.platno.addEventListener("pointermove",N),n.api.ucitajStrukturuCif(e.mineral).then(B=>{o||(l=$m(B),w(l),n.zatraziRender())}).catch(B=>{if(o)return;const k=B instanceof xl&&B.status===404?ot("strukturaNedostupna"):ot("strukturaNedostupna");n.prikaziRezervu(k)}),{resetuj(){d=-1,x(-1)},osveziTemu(B){_.color.set(B.token("--text-secondary")),p.color.set(B.token("--text-muted")),u.color.set(B.token("--accent"));for(const k of g.children){const O=k;O.material instanceof lt&&O.material.color.set(B.token("--text-secondary"))}for(const k of m.children){const O=k;O.material instanceof ft&&O.material.color.set(B.token("--text-muted"))}},posleRendera(){if(!b||d<0){y.hidden=!0;return}const B=A[d];if(!B)return;B.mesh.updateMatrixWorld(!0);const k=B.mesh.position.clone().applyMatrix4(h.matrixWorld),O=n.projektujU2D(k);if(!O.vidljivo){y.hidden=!0;return}y.hidden=!1,y.style.transform=`translate(-50%, -130%) translate(${O.x.toFixed(1)}px, ${O.y.toFixed(1)}px)`},raspolazi(){o=!0,a&&n.platno.removeEventListener("pointermove",N),Pt(h),_.dispose(),p.dispose(),u.dispose()}}}},Na=[{kljuc:"kubni",naziv:"Тесерални",kratko:"Тесерални",odnosIvica:"a = b = c",odnosUglova:"α = β = γ = 90°",reprezentativniOblik:"коцка",celija:{a:1.15,b:1.15,c:1.15,alpha:90,beta:90,gamma:90}},{kljuc:"tetragonalni",naziv:"Тетрагонални",kratko:"Тетраг.",odnosIvica:"a = b ≠ c",odnosUglova:"α = β = γ = 90°",reprezentativniOblik:"тетрагонална призма",celija:{a:1,b:1,c:1.62,alpha:90,beta:90,gamma:90}},{kljuc:"ortorombicni",naziv:"Ромбични",kratko:"Ромб.",odnosIvica:"a ≠ b ≠ c",odnosUglova:"α = β = γ = 90°",reprezentativniOblik:"правоугаона призма („цигла“)",celija:{a:.85,b:1.22,c:1.58,alpha:90,beta:90,gamma:90}},{kljuc:"heksagonalni",naziv:"Хексагонални",kratko:"Хексаг.",odnosIvica:"a = b ≠ c",odnosUglova:"α = β = 90°, γ = 120°",reprezentativniOblik:"хексагонална призма",celija:{a:1.08,b:1.08,c:1.55,alpha:90,beta:90,gamma:120}},{kljuc:"trigonalni",naziv:"Тригонални",kratko:"Тригон.",odnosIvica:"a = b = c (ромбоедарска) / a = b ≠ c (хексагонална)",odnosUglova:"α = β = γ ≠ 90° (ромб.) / α = β = 90°, γ = 120° (хекс.)",reprezentativniOblik:"ромбоедар (у кристалографији се стандардно описује и хексагоналном поставком)",celija:{a:1.18,b:1.18,c:1.18,alpha:75,beta:75,gamma:75}},{kljuc:"monoklinicni",naziv:"Моноклинични",kratko:"Монокл.",odnosIvica:"a ≠ b ≠ c",odnosUglova:"α = γ = 90°, β ≠ 90°",reprezentativniOblik:"кос паралелопипед (β ≠ 90°)",celija:{a:.92,b:1.22,c:1.48,alpha:90,beta:112,gamma:90}},{kljuc:"triklinicni",naziv:"Триклинични",kratko:"Трикл.",odnosIvica:"a ≠ b ≠ c",odnosUglova:"α ≠ β ≠ γ ≠ 90°",reprezentativniOblik:"кос паралелопипед (α, β, γ ≠ 90°)",celija:{a:.88,b:1.18,c:1.46,alpha:78,beta:109,gamma:103}}],s0={a:1.15,b:1.15,c:1.15,alpha:90,beta:90,gamma:90};function o0(n,e,t){const i=Math.max(0,Math.min(1,t));return{a:n.a+(e.a-n.a)*i,b:n.b+(e.b-n.b)*i,c:n.c+(e.c-n.c)*i,alpha:n.alpha+(e.alpha-n.alpha)*i,beta:n.beta+(e.beta-n.beta)*i,gamma:n.gamma+(e.gamma-n.gamma)*i}}function ul(n){const e=Zr(n),t=new F(...e.va),i=new F(...e.vb),r=new F(...e.vc),a=t.clone().add(i).add(r).multiplyScalar(.5),s=[],o=[[0,0,0],[1,0,0],[1,1,0],[0,1,0],[0,0,1],[1,0,1],[1,1,1],[0,1,1]];for(const[g,_,p]of o){const u=An(g,_,p,e);s.push(new F(u[0]-a.x,u[1]-a.y,u[2]-a.z))}const c=[[0,1],[1,2],[2,3],[3,0],[4,5],[5,6],[6,7],[7,4],[0,4],[1,5],[2,6],[3,7]],l=[];for(const[g,_]of c){const p=s[g],u=s[_];l.push(p.x,p.y,p.z,u.x,u.y,u.z)}const d=new Xe;d.setAttribute("position",new je(l,3));const h=[[0,3,2,1],[4,5,6,7],[0,1,5,4],[2,3,7,6],[1,2,6,5],[3,0,4,7]],f=[];for(const[g,_,p,u]of h){const E=s[g],y=s[_],M=s[p],D=s[u];f.push(E.x,E.y,E.z,y.x,y.y,y.z,M.x,M.y,M.z,E.x,E.y,E.z,M.x,M.y,M.z,D.x,D.y,D.z)}const m=new Xe;return m.setAttribute("position",new je(f,3)),m.computeVertexNormals(),{ivice:d,mreza:m,poreklo:s[0],va:t,vb:i,vc:r}}function ka(n,e,t,i){const r=e.clone().normalize(),a=t.clone().normalize(),s=18,o=[];let c=n.clone();for(let d=0;d<=s;d++){const h=d/s,f=r.clone().multiplyScalar(1-h).addScaledVector(a,h).normalize(),m=n.clone().addScaledVector(f,i);if(d===Math.floor(s/2)&&(c=n.clone().addScaledVector(f,i*1.38)),d>0){const g=(d-1)/s,_=r.clone().multiplyScalar(1-g).addScaledVector(a,g).normalize(),p=n.clone().addScaledVector(_,i);o.push(p.x,p.y,p.z,m.x,m.y,m.z)}}const l=new Xe;return l.setAttribute("position",new je(o,3)),{geometrija:l,sredina:c}}function c0(n,e,t){if(n==="heksagonalni"){const s=.58+.22*t,o=1.35-(1.35-.68)*t,c=[{normala:[0,1,0],d:s},{normala:[0,-1,0],d:s},{normala:[1,0,0],d:.68},{normala:[-1,0,0],d:.68},{normala:[0,0,1],d:.68+.14*t},{normala:[0,0,-1],d:.68+.14*t},{normala:[.5,0,Math.sqrt(3)/2],d:o},{normala:[-.5,0,Math.sqrt(3)/2],d:o},{normala:[.5,0,-Math.sqrt(3)/2],d:o},{normala:[-.5,0,-Math.sqrt(3)/2],d:o}],l=[{normala:[0,1,0],d:s},{normala:[0,-1,0],d:s}];if(t>.85){for(let g=0;g<6;g++){const _=g*Math.PI/3;l.push({normala:[Math.cos(_),0,Math.sin(_)],d:.68})}const f=er(l),m=tr(f);return{mreza:m.geometrijaMreze,ivice:m.geometrijaIvica}}const d=er(c),h=tr(d);return{mreza:h.geometrijaMreze,ivice:h.geometrijaIvica}}const i={a:e.a*.92,b:e.b*.92,c:e.c*.92,alpha:e.alpha,beta:e.beta,gamma:e.gamma},r=ul(i);return{mreza:r.mreza,ivice:r.ivice}}const l0={izgled:"kristal",imaPodrazumevanuAnimaciju(n){return(n.animacija??"rotacija")!=="nema"},pocetnaKamera(){return{theta:.42,phi:1.15,udaljenost:6.8}},kreiraj(n,e){const t=e.animacija??"rotacija",i=e.prikazi_ose??!0,r=e.prikazi_celiju??!0;let a=e.sistem==="svi"?"heksagonalni":e.sistem;e.sistem==="svi"&&(a="kubni");let s=n.smanjenPokret||t!=="uporedi"?1:0,o=0;const c=new Qe,l=new Qe,d=new Qe;r?(l.position.set(-1.55,-.05,0),d.position.set(1.55,-.05,0)):d.position.set(0,-.05,0),c.add(l,d),n.scena3D.add(c),n.dodajKontaktnuSenku(1.3,-1.02,c,d.position.x);const h=new ft({color:new oe(n.tema.token("--primary")),transparent:!0,opacity:.14,roughness:.45,metalness:.05,side:St,depthWrite:!1}),f=new lt({color:new oe(n.tema.token("--text-secondary"))}),m=new lt({color:new oe(n.tema.token("--danger"))}),g=new lt({color:new oe(n.tema.token("--success"))}),_=new lt({color:new oe(n.tema.token("--accent"))}),p=new lt({color:new oe(n.tema.token("--warning"))}),u=ni(n.tema.token("--primary"),{providnost:.55}),E=nr(n.tema.token("--text-primary"),n.tema.token("--primary")),y=["a","b","c","α","β","γ"],M=new Map,D=new Map;if(i&&r)for(const R of y){const z=document.createElement("span");z.className="udzbenik-scena-etiketa",z.textContent=R,n.slojEtiketa.append(z),M.set(R,z),D.set(R,new F)}const A=document.createElement("div");A.className="udzbenik-scena-info-red",n.podnozje.append(A);const b=new Map;if(e.sistem==="svi"){const R=document.createElement("div");R.className="udzbenik-sistemi-traka",R.setAttribute("role","group"),R.setAttribute("aria-label",ot("izaberiKristalniSistem"));for(const z of Na){const N=document.createElement("button");N.type="button",N.className="udzbenik-sistem-kartica",N.dataset.sistem=z.kljuc,N.setAttribute("aria-pressed",String(z.kljuc===a));const B=document.createElement("span");B.className="udzbenik-sistem-kartica-naslov",B.textContent=z.naziv;const k=document.createElement("span");k.className="udzbenik-sistem-kartica-meta",k.textContent=`${z.odnosIvica} · ${z.odnosUglova}`,N.append(B,k),N.addEventListener("click",()=>{a=z.kljuc,s=n.smanjenPokret||t!=="uporedi"?1:0,C(),U(),n.zatraziRender()}),b.set(z.kljuc,N),R.append(N)}n.gornjeKontrole.append(R)}function C(){for(const[R,z]of b.entries()){const N=R===a;z.classList.toggle("udzbenik-sistem-kartica--aktivna",N),z.setAttribute("aria-pressed",String(N))}}function v(){return Na.find(R=>R.kljuc===a)??Na[0]}function x(R){for(const z of R.children){const N=z.geometry;N&&N.dispose()}R.clear()}function P(){if(t!=="uporedi"||a==="kubni"||s>=1)return 1;const R=s%1;if(R<.4){const z=R/.4;return z*z*(3-2*z)}if(R<.72)return 1;if(R<.92){const z=(R-.72)/.2;return 1-z*z*(3-2*z)}return 0}function U(){const R=v(),z=P(),N=o0(s0,R.celija,z);if(x(l),x(d),r){const K=ul(N),le=new Le(K.mreza,h),De=new ut(K.ivice,f);if(l.add(le,De),i){const X=K.poreklo,J=X.clone().addScaledVector(K.va,1.16),ae=X.clone().addScaledVector(K.vb,1.16),re=X.clone().addScaledVector(K.vc,1.16),ue=new Xe().setFromPoints([X,J]),Pe=new Xe().setFromPoints([X,ae]),fe=new Xe().setFromPoints([X,re]);l.add(new Qn(ue,m),new Qn(Pe,g),new Qn(fe,_));const te=ka(X,K.vb,K.vc,.36),se=ka(X,K.va,K.vc,.44),W=ka(X,K.va,K.vb,.36);l.add(new ut(te.geometrija,p),new ut(se.geometrija,p),new ut(W.geometrija,p)),D.get("a")?.copy(J),D.get("b")?.copy(ae),D.get("c")?.copy(re),D.get("α")?.copy(te.sredina),D.get("β")?.copy(se.sredina),D.get("γ")?.copy(W.sredina)}}const B=c0(R.kljuc,N,z);d.add(new Le(B.mreza,u),new ut(B.ivice,E)),A.replaceChildren();const k=document.createElement("strong");k.textContent=`${R.naziv}: `;const O=document.createElement("span"),q=R.kljuc==="trigonalni"?" • Стандардна кристалографска поставка за тригоналне минерале (кварц, калцит) је хексагонална (a = b ≠ c, γ = 120°).":"";O.textContent=`${R.odnosIvica} · ${R.odnosUglova} — облик: ${R.reprezentativniOblik}${q}`,A.append(k,O)}function w(){if(!i||!r)return;l.updateMatrixWorld(!0);const R=v();for(const[z,N]of M.entries()){const B=D.get(z);if(!B)continue;const k=B.clone().applyMatrix4(l.matrixWorld),O=n.projektujU2D(k);if(!O.vidljivo){N.hidden=!0;continue}N.hidden=!1,N.style.transform=`translate(-50%, -50%) translate(${O.x.toFixed(1)}px, ${O.y.toFixed(1)}px)`;const q=z==="c"&&R.celija.c!==R.celija.a||z==="b"&&R.celija.b!==R.celija.a||z==="α"&&R.celija.alpha!==90||z==="β"&&R.celija.beta!==90||z==="γ"&&R.celija.gamma!==90;N.classList.toggle("udzbenik-scena-etiketa--istaknuta",q)}}return C(),U(),{azuriraj(R){t==="uporedi"?(s=(s+R*.18)%1,n.korisnikUpravlja()||(o+=R*.22,c.rotation.y=Math.sin(o)*.18),U()):t==="rotacija"&&!n.korisnikUpravlja()&&(c.rotation.y+=R*.45)},korak(){t==="uporedi"?(s=(s+.15)%1,o+=.45,c.rotation.y=Math.sin(o)*.18,U()):c.rotation.y+=.35},resetuj(){c.rotation.set(0,0,0),o=0,s=n.smanjenPokret||t!=="uporedi"?1:0,U()},osveziTemu(R){h.color.set(R.token("--primary")),f.color.set(R.token("--text-secondary")),m.color.set(R.token("--danger")),g.color.set(R.token("--success")),_.color.set(R.token("--accent")),p.color.set(R.token("--warning")),u.color.set(R.token("--primary")),E.color.copy(Ni(R.token("--text-primary"),R.token("--primary")))},posleRendera(){w()},raspolazi(){Pt(c),h.dispose(),f.dispose(),m.dispose(),g.dispose(),_.dispose(),p.dispose(),u.dispose(),E.dispose()}}}},$t="Klein, C. & Dutrow, B. (2007), Manual of Mineral Science (23rd ed.), John Wiley & Sons, Table 2.3 (Knoop microhardness HK, kgf/mm²; теренске пробе: нокат ~2,5, бакарни новчић ~3, нож/стакло ~5,5, турпија ~6,5).",yn=[{mohs:1,kljuc:"talk",naziv:"Талк",formula:"Mg₃Si₄O₁₀(OH)₂",apsolutnaKnoop:1,izvor:$t},{mohs:2,kljuc:"gips",naziv:"Гипс",formula:"CaSO₄·2H₂O",apsolutnaKnoop:32,izvor:$t},{mohs:3,kljuc:"kalcit",naziv:"Калцит",formula:"CaCO₃",apsolutnaKnoop:135,izvor:$t},{mohs:4,kljuc:"fluorit",naziv:"Флуорит",formula:"CaF₂",apsolutnaKnoop:163,izvor:$t},{mohs:5,kljuc:"apatit",naziv:"Апатит",formula:"Ca₅(PO₄)₃(F,Cl,OH)",apsolutnaKnoop:430,izvor:$t},{mohs:6,kljuc:"ortoklas",naziv:"Ортоклас",formula:"KAlSi₃O₈",apsolutnaKnoop:560,izvor:$t},{mohs:7,kljuc:"kvarc",naziv:"Кварц",formula:"SiO₂",apsolutnaKnoop:820,izvor:$t},{mohs:8,kljuc:"topaz",naziv:"Топаз",formula:"Al₂SiO₄(F,OH)₂",apsolutnaKnoop:1340,izvor:$t},{mohs:9,kljuc:"korund",naziv:"Корунд",formula:"Al₂O₃",apsolutnaKnoop:2100,izvor:$t},{mohs:10,kljuc:"dijamant",naziv:"Дијамант",formula:"C",apsolutnaKnoop:7e3,izvor:$t}],u0=[{naziv:"Нокат (~2,5)",mohs:2.5},{naziv:"Бакарни новчић (~3)",mohs:3},{naziv:"Нож / стакло (~5,5)",mohs:5.5},{naziv:"Челична турпија (~6,5)",mohs:6.5}];function wc(n,e){if(!e||e.length===0)return!1;const t=n.kljuc.toLowerCase(),i=n.naziv.toLowerCase();return e.some(r=>{const a=r.trim().toLowerCase();return a===t||a===i})}const d0={imaPodrazumevanuAnimaciju(){return!0},pocetnaKamera(){return{theta:.16,phi:1.18,udaljenost:8.6}},kreiraj(n,e){const t=e.prikazi_apsolutnu??!1,i=e.prikazi_terenske_probe??!0,r=e.istaknuti??[];let a=!1,s=0,o=6,c=5,l=n.smanjenPokret?.65:0;const d=new Qe;d.position.set(0,-.35,0),n.scena3D.add(d);const h=-4.05,f=.9,m=-.7,g=2.75,_=new ft({color:new oe(n.tema.token("--bg-elevated")),roughness:.7,metalness:.05}),p=new Le(new Qt(9.6,.14,1.4),_);p.position.set(0,m-.07,-.35),d.add(p);const u=[],E=new lt({color:new oe(n.tema.token("--text-primary"))}),y=new Qt(.66,1,.66),M=new Qi(y);for(let te=0;te<yn.length;te++){const se=yn[te],W=wc(se,r),L=new oe(n.tema.token(W?"--accent":"--primary")),Ee=new ft({color:L,emissive:W?new oe(n.tema.token("--accent")).multiplyScalar(.22):new oe(0,0,0),roughness:.35,metalness:.12}),Se=new Le(y,Ee),_e=new ut(M,E),ve=h+te*f;Se.position.set(ve,m+.5,-.35),_e.position.copy(Se.position),d.add(Se,_e);const Ne=document.createElement("span");Ne.className="udzbenik-scena-etiketa udzbenik-scena-etiketa--mala",W&&Ne.classList.add("udzbenik-scena-etiketa--istaknuta"),Ne.textContent=`${se.mohs}`,n.slojEtiketa.append(Ne),u.push({mineral:se,istaknut:W,mesh:Se,ivice:_e,mat:Ee,etiketaDom:Ne})}const D=new ft({color:new oe(n.tema.token("--warning")),roughness:.4}),A=[];if(i){const te=new ar(.035,.035,.65,8);for(const se of u0){const W=h+(se.mohs-1)*f,L=new Le(te,D);L.position.set(W,m+.32,.18),d.add(L);const Ee=document.createElement("span");Ee.className="udzbenik-scena-etiketa udzbenik-scena-etiketa--proba",Ee.textContent=se.naziv,n.slojEtiketa.append(Ee),A.push({x:W,tekst:se.naziv,dom:Ee,stub:L})}}const b=new Qe;b.position.set(0,m-.52,1.35),d.add(b);const C=new ft({color:new oe(n.tema.token("--primary-light")),roughness:.45,metalness:.08}),v=new Le(new Qt(3.4,.24,.92),C),x=new ut(new Qi(v.geometry),E);b.add(v,x);const P=new ft({color:new oe(n.tema.token("--danger")),roughness:.85}),U=new Le(new Qt(1,.05,.11),P);U.position.set(-1.1,.125,0),U.visible=!1,b.add(U);const w=new ft({color:new oe(n.tema.token("--accent")),roughness:.25,metalness:.2}),R=new Le(new Ws(.22,.72,6),w);R.rotation.x=Math.PI,R.rotation.z=-.22,R.position.set(-1.1,.5,0),b.add(R);const z=document.createElement("div");z.className="udzbenik-mohs-kontrole";const N=document.createElement("div");N.className="udzbenik-mohs-dugmad",N.setAttribute("role","group"),N.setAttribute("aria-label",ot("ordinalnaTvrdocaOznaka"));const B=[];for(let te=0;te<yn.length;te++){const se=yn[te],W=document.createElement("button");W.type="button",W.className="udzbenik-mohs-cip",wc(se,r)&&W.classList.add("udzbenik-mohs-cip--istaknut"),W.textContent=`${se.mohs}. ${se.naziv}`,W.addEventListener("click",()=>{De(te)}),B.push(W),N.append(W)}z.append(N);const k=document.createElement("div");k.className="udzbenik-mohs-akcije";const O=document.createElement("button");O.type="button",O.className="udzbenik-dugme udzbenik-dugme--malo",O.textContent=ot("zameniMinerale"),O.addEventListener("click",()=>{const te=o;o=c,c=te,l=n.smanjenPokret?.75:0,re(),n.zatraziRender()}),k.append(O);let q=null;t&&(q=document.createElement("button"),q.type="button",q.className="udzbenik-dugme udzbenik-dugme--malo udzbenik-dugme--preklopnik",q.setAttribute("role","switch"),q.setAttribute("aria-checked","false"),q.textContent=ot("apsolutnaTvrdocaPreklopnik"),q.addEventListener("click",()=>{a=!a,q?.setAttribute("aria-checked",String(a)),q?.classList.toggle("udzbenik-dugme--aktivno",a),n.smanjenPokret&&(s=a?1:0,J()),re(),n.zatraziRender()}),k.append(q)),z.append(k),n.gornjeKontrole.append(z);const K=document.createElement("p");K.className="udzbenik-scena-info-red",K.setAttribute("aria-live","polite");const le=document.createElement("p");le.className="udzbenik-scena-izvor",le.textContent=`${ot("izvorPodataka")}: ${$t}`,n.podnozje.append(K,le);function De(te){te===o?c=te<9?te+1:te-1:(o=te,c=te>0?te-1:1),l=n.smanjenPokret?.75:0,re(),n.zatraziRender()}function X(te,se){const W=te.mohs/10*g,L=Math.max(.08,te.apsolutnaKnoop/7e3*g);return W+(L-W)*se}function J(){for(let te=0;te<u.length;te++){const se=u[te],W=X(se.mineral,s);se.mesh.scale.y=W,se.mesh.position.y=m+W*.5,se.ivice.scale.y=W,se.ivice.position.copy(se.mesh.position);const L=te===o,Ee=te===c,Se=L?"--accent":Ee?"--warning":se.istaknut?"--accent":"--primary",_e=new oe(n.tema.token(Se));!L&&!Ee&&!se.istaknut&&_e.lerp(new oe(n.tema.token("--bg-elevated")),.25),se.mat.color.copy(_e),se.etiketaDom.textContent=a?`${se.mineral.mohs} (${se.mineral.apsolutnaKnoop})`:`${se.mineral.mohs}`}}function ae(){const te=yn[o],se=yn[c],W=te.mohs>se.mohs,L=Math.min(1,l/.75),Ee=-1.15,_e=Ee+(1.15-Ee)*L;if(R.position.x=_e,R.position.y=W?.44:.5,W&&L>.03){const ve=Math.max(.05,_e-Ee);U.visible=!0,U.scale.x=ve,U.position.x=Ee+ve*.5}else U.visible=!1}function re(){for(let Ee=0;Ee<B.length;Ee++){const Se=B[Ee],_e=Ee===o;Se.classList.toggle("udzbenik-mohs-cip--aktivan",_e),Se.setAttribute("aria-pressed",String(_e))}const te=yn[o],se=yn[c],L=te.mohs>se.mohs?`${ot("probaGrebanja")}: ${te.naziv} (${te.mohs}, HK ${te.apsolutnaKnoop}) је тврђи и оставља бразду на минералу ${se.naziv} (${se.mohs}, HK ${se.apsolutnaKnoop}).`:`${ot("probaGrebanja")}: ${te.naziv} (${te.mohs}, HK ${te.apsolutnaKnoop}) је мекши и НЕ оставља бразду на минералу ${se.naziv} (${se.mohs}, HK ${se.apsolutnaKnoop}).`;K.textContent=L,J(),ae()}const ue=new Ks,Pe=new We,fe=te=>{const se=n.platno.getBoundingClientRect();if(se.width<=0||se.height<=0)return;Pe.x=(te.clientX-se.left)/se.width*2-1,Pe.y=-((te.clientY-se.top)/se.height)*2+1,ue.setFromCamera(Pe,n.kamera);const W=ue.intersectObjects(u.map(L=>L.mesh),!1);if(W.length>0){const L=W[0].object,Ee=u.findIndex(Se=>Se.mesh===L);Ee!==-1&&De(Ee)}};return n.platno.addEventListener("click",fe),re(),{azuriraj(te){const se=a?1:0;Math.abs(s-se)>.002?(s+=(se-s)*Math.min(1,te*6),J()):s!==se&&(s=se,J()),l=(l+te*.42)%1,ae()},korak(){l=(l+.2)%1,s=a?1:0,J(),ae()},resetuj(){a=!1,s=0,q&&(q.setAttribute("aria-checked","false"),q.classList.remove("udzbenik-dugme--aktivno")),o=6,c=5,l=n.smanjenPokret?.75:0,re()},osveziTemu(te){_.color.set(te.token("--bg-elevated")),E.color.set(te.token("--text-primary")),D.color.set(te.token("--warning")),C.color.set(te.token("--primary-light")),P.color.set(te.token("--danger")),w.color.set(te.token("--accent")),J()},posleRendera(){d.updateMatrixWorld(!0);for(const te of u){const se=te.mesh.position.clone().add(new F(0,te.mesh.scale.y*.5+.22,0)).applyMatrix4(d.matrixWorld),W=n.projektujU2D(se);te.etiketaDom.hidden=!W.vidljivo,W.vidljivo&&(te.etiketaDom.style.transform=`translate(-50%, -50%) translate(${W.x.toFixed(1)}px, ${W.y.toFixed(1)}px)`)}for(const te of A){const se=new F(te.x,m-.22,.35).applyMatrix4(d.matrixWorld),W=n.projektujU2D(se);te.dom.hidden=!W.vidljivo,W.vidljivo&&(te.dom.style.transform=`translate(-50%, 0%) translate(${W.x.toFixed(1)}px, ${W.y.toFixed(1)}px)`)}},raspolazi(){n.platno.removeEventListener("click",fe),Pt(d),y.dispose(),M.dispose(),_.dispose(),E.dispose(),D.dispose(),C.dispose(),P.dispose(),w.dispose();for(const te of u)te.mat.dispose()}}}};function h0(n,e,t){const i=1/(n*n),r=1/(e*e),a=1/(t*t),s=(i-r)/Math.max(1e-12,r-a),c=2*Math.atan(Math.sqrt(Math.max(0,s)))*180/Math.PI;return c<=90?{dvaV:c,dvaVZ:c,znak:"+",bisektrisaOstra:"Z (γ)"}:{dvaV:180-c,dvaVZ:c,znak:"-",bisektrisaOstra:"X (α)"}}function Ac(n,e,t){const i=Math.hypot(...t),r=i>0?t[0]/i:0,a=i>0?t[1]/i:0,s=i>0?t[2]/i:1;if(n==="izotropna"){const w=e[0]??1.5;return{n1:w,n2:w,delta:0}}if(n==="jednoosna"){const w=e[0]??1.544,R=e[1]??1.553,z=s*s,N=Math.max(0,1-z),B=z/(w*w)+N/(R*R),k=Math.sqrt(1/Math.max(1e-12,B)),O=Math.abs(k-w);return{n1:Math.min(w,k),n2:Math.max(w,k),delta:O}}const o=e[0]??1.52,c=e[1]??1.53,l=e[2]??1.55,d=1/(o*o),h=1/(c*c),f=1/(l*l);let m,g,_,p;if(Math.abs(h-f)>1e-7&&d>=h&&h>=f){const w=h0(o,c,l);m=w.dvaV,g=w.dvaVZ,_=w.znak,p=w.bisektrisaOstra}const u=r*r,E=a*a,y=s*s,M=1,D=-(u*(h+f)+E*(d+f)+y*(d+h)),A=u*h*f+E*d*f+y*d*h,b=Math.max(0,D*D-4*M*A),C=(-D-Math.sqrt(b))/(2*M),v=(-D+Math.sqrt(b))/(2*M),x=Math.sqrt(1/Math.max(1e-12,v)),P=Math.sqrt(1/Math.max(1e-12,C)),U=Math.abs(P-x);return{n1:x,n2:P,delta:U,ugao2V:m,ugao2VZ:g,optickiZnak:_,bisektrisaOstra:p}}const f0={imaPodrazumevanuAnimaciju(){return!0},pocetnaKamera(){return{theta:.72,phi:1.18,udaljenost:5.6}},kreiraj(n,e){const t=new Qe;n.scena3D.add(t);const i=e.tip,r=e.n&&e.n.length>0?e.n:i==="izotropna"?[1.5]:i==="jednoosna"?[1.658,1.486]:[1.52,1.53,1.55];let a=1.6,s=1.6,o=1.6;if(i==="jednoosna"){const U=r[0],w=r[1]??r[0];a=1.6,s=1.6,o=1.6*(w>=U?1.35:.72)}else i==="dvoosna"&&(a=1.25,s=1.65,o=2.15);const c=new Yt(1,48,36);c.scale(a,s,o);const l=new ft({color:new oe(n.tema.token("--primary")),transparent:!0,opacity:.42,roughness:.25,metalness:.1,side:St}),d=new Le(c,l);t.add(d);const h=new lt({color:new oe(n.tema.token("--text-secondary"))}),f=new Xe,m=[-a*1.3,0,0,a*1.3,0,0,0,-s*1.3,0,0,s*1.3,0,0,0,-o*1.3,0,0,o*1.3];f.setAttribute("position",new je(m,3)),t.add(new ut(f,h));const g=new lt({color:new oe(n.tema.token("--accent")),linewidth:3});if(e.prikazi_opticke_ose!==!1){const U=[];if(i==="jednoosna")U.push(0,0,-o*1.45,0,0,o*1.45);else if(i==="dvoosna"){const R=(Ac(i,r,[0,0,1]).ugao2V??50)/2*(Math.PI/180),z=o*1.4,N=z*Math.sin(R),B=z*Math.cos(R);U.push(-N,0,-B,N,0,B),U.push(N,0,-B,-N,0,B)}if(U.length>0){const w=new Xe;w.setAttribute("position",new je(U,3)),t.add(new ut(w,g))}}const _=new Qe;t.add(_);const p=new Ln({color:new oe(n.tema.token("--warning")),transparent:!0,opacity:.35,side:St}),u=new Xs(0,2.2,48),E=new Le(u,p);_.add(E);const y=new lt({color:new oe(n.tema.token("--danger"))}),M=new Xe;M.setAttribute("position",new je([0,0,-2.6,0,0,2.6],3)),_.add(new ut(M,y));const D=document.createElement("div");D.className="udzbenik-scena-status",n.podnozje.append(D);const A=document.createElement("small");A.className="udzbenik-scena-napomena",A.style.display="block",A.textContent="Напомена: Разлике индекса преламања су преувеличане ради јаснијег 3D приказа.",n.podnozje.append(A);let b=.5,C=.3;function v(){_.rotation.set(b,C,0);const U=new F(0,0,1).applyEuler(_.rotation),w=Ac(i,r,[U.x,U.y,U.z]),R=w.delta.toFixed(4),z=e.mineral?` (${e.mineral})`:"",N=w.ugao2V!==void 0?` • 2V = ${w.ugao2V.toFixed(1)}° (${w.optickiZnak}, Bxa = ${w.bisektrisaOstra})`:"";D.textContent=`Тип: ${i}${z} • n'₁ = ${w.n1.toFixed(3)}, n'₂ = ${w.n2.toFixed(3)} • δ = ${R}${N}`}v();function x(){l.color.set(n.tema.token("--primary")),h.color.set(n.tema.token("--text-secondary")),g.color.set(n.tema.token("--accent")),p.color.set(n.tema.token("--warning")),y.color.set(n.tema.token("--danger"))}let P=0;return{azuriraj(U){P+=U*.35,C=Math.sin(P)*1.1,b=Math.cos(P*.7)*.7,v()},korak(){P+=.25,C+=.2,v()},resetuj(){P=0,b=.5,C=.3,v()},osveziTemu(){x()},raspolazi(){c.dispose(),l.dispose(),f.dispose(),h.dispose(),g.dispose(),u.dispose(),p.dispose(),M.dispose(),y.dispose(),Pt(t),D.remove(),A.remove()}}}},Fa={nezo:{klasa:"nezo",naziv:"Незосиликати (изоловани tetraedri)",odnosSiO:"1 : 4 (SiO₄⁴⁻)",zajednickiKiseonici:"0",primeri:"оливин, гранат, циркон"},soro:{klasa:"soro",naziv:"Соросиликати (парови tetraedara)",odnosSiO:"2 : 7 (Si₂O₇⁶⁻)",zajednickiKiseonici:"1",primeri:"епидот, хемиморфит"},"ciklo-3":{klasa:"ciklo-3",naziv:"Циклосиликати (трочлани прстен)",odnosSiO:"1 : 3 (Si₃O₉⁶⁻)",zajednickiKiseonici:"2",primeri:"бенитоит"},"ciklo-6":{klasa:"ciklo-6",naziv:"Циклосиликати (шесточлани прстен)",odnosSiO:"1 : 3 (Si₆O₁₈¹²⁻)",zajednickiKiseonici:"2",primeri:"берил, турмалин"},"ino-jednostruki":{klasa:"ino-jednostruki",naziv:"Иносиликати (једноструки ланци)",odnosSiO:"1 : 3 (Si₂O₆⁴⁻)",zajednickiKiseonici:"2",primeri:"пироксени (диопсид, енстатит)"},"ino-dvostruki":{klasa:"ino-dvostruki",naziv:"Иносиликати (двоструки ланци)",odnosSiO:"4 : 11 (Si₄O₁₁⁶⁻)",zajednickiKiseonici:"2 и 3 (просек 2,5)",primeri:"амфиболи (тремолит, хорнбленда)"},filo:{klasa:"filo",naziv:"Филосиликати (слојевити)",odnosSiO:"2 : 5 (Si₄O₁₀⁴⁻)",zajednickiKiseonici:"3",primeri:"лискуни (мусковит, биотит), талк, каолинит"},tekto:{klasa:"tekto",naziv:"Тектосиликати (просторна мрежа)",odnosSiO:"1 : 2 (SiO₂)",zajednickiKiseonici:"4",primeri:"кварц, фелдспати, зеолити"},sve:{klasa:"sve",naziv:"Преглед свих класа",odnosSiO:"од 1:4 до 1:2",zajednickiKiseonici:"0 до 4",primeri:"полимеризација од незо- до тектосиликата"}};function p0(){const e=.65*Math.SQRT2,t=[0,0,0],i=[-e,.65,0],r=[-e,-.5*.65,Math.sqrt(3)/2*.65],a=[-e,-.5*.65,-(Math.sqrt(3)/2)*.65],s=[e,-.65,0],o=[e,.5*.65,-(Math.sqrt(3)/2)*.65],c=[e,.5*.65,Math.sqrt(3)/2*.65];return{vrhoviLevi:[t,i,r,a],vrhoviDesni:[t,s,o,c],svih7Kiseonika:[t,i,r,a,s,o,c]}}function bn(n,e,t,i,r,a){const s=new Qe;s.position.copy(n),s.rotation.copy(e);const o=.55,c=[[o,o,o],[o,-o,-o],[-o,o,-o],[-o,-o,o]];if(a==="tetraedri"||a==="oba"){const l=new Xe,d=[...c[0],...c[1],...c[2],...c[0],...c[3],...c[1],...c[0],...c[2],...c[3],...c[1],...c[3],...c[2]];l.setAttribute("position",new je(d,3)),l.computeVertexNormals();const h=new Le(l,t);s.add(h)}if(a==="kugle"||a==="oba")for(const l of c){const d=new Le(r,i);d.position.set(l[0],l[1],l[2]),s.add(d)}return s}const m0={imaPodrazumevanuAnimaciju(n){return(n.animacija??"rotacija")!=="nema"},pocetnaKamera(){return{theta:.65,phi:1.15,udaljenost:6.2}},kreiraj(n,e){let t=e.klasa==="sve"?"nezo":e.klasa;const i=e.prikaz??"tetraedri",r=new Qe;n.scena3D.add(r);const a=new Yt(.18,16,16),s=new ft({color:new oe(n.tema.token("--primary")),transparent:!0,opacity:.65,roughness:.25,metalness:.1,side:St}),o=new ft({color:new oe(n.tema.token("--accent")),roughness:.25,metalness:.2}),c=document.createElement("div");c.className="udzbenik-scena-status",n.podnozje.append(c);function l(_){for(;r.children.length>0;){const u=r.children[0];r.remove(u),Pt(u)}const p=Fa[_]??Fa.nezo;if(c.textContent=`${p.naziv} • Si:O = ${p.odnosSiO} • Заједнички O: ${p.zajednickiKiseonici} (${p.primeri})`,_==="nezo")r.add(bn(new F(0,0,0),new xt(0,0,0),s,o,a,i));else if(_==="soro"){const{vrhoviLevi:u,vrhoviDesni:E,svih7Kiseonika:y}=p0(),[M,D,A,b]=u,[,C,v,x]=E;if(i==="tetraedri"||i==="oba"){const P=new Xe,U=[...M,...D,...A,...M,...A,...b,...M,...b,...D,...D,...b,...A,...M,...v,...C,...M,...x,...v,...M,...C,...x,...C,...v,...x];P.setAttribute("position",new je(U,3)),P.computeVertexNormals(),r.add(new Le(P,s))}if(i==="kugle"||i==="oba")for(const P of y){const U=new Le(a,o);U.position.set(P[0],P[1],P[2]),r.add(U)}}else if(_==="ciklo-3")for(let u=0;u<3;u++){const E=u*2*Math.PI/3,y=new F(Math.cos(E)*.95,Math.sin(E)*.95,0);r.add(bn(y,new xt(0,0,E),s,o,a,i))}else if(_==="ciklo-6")for(let u=0;u<6;u++){const E=u*2*Math.PI/6,y=new F(Math.cos(E)*1.5,Math.sin(E)*1.5,0);r.add(bn(y,new xt(0,0,E),s,o,a,i))}else if(_==="ino-jednostruki")for(let u=-2;u<=2;u++){const E=u%2===0?0:Math.PI;r.add(bn(new F(u*.9,u%2*.2,0),new xt(0,0,E),s,o,a,i))}else if(_==="ino-dvostruki")for(let u=-2;u<=2;u++){const E=u%2===0?0:Math.PI;r.add(bn(new F(u*.9,.45+u%2*.15,0),new xt(0,0,E),s,o,a,i)),r.add(bn(new F(u*.9,-.45-u%2*.15,0),new xt(0,0,E+Math.PI),s,o,a,i))}else if(_==="filo")for(let u=-1;u<=1;u++)for(let E=-1;E<=1;E++){const y=u*1.4+E%2*.7,M=E*1.2;r.add(bn(new F(y,M,0),new xt(0,0,0),s,o,a,i))}else for(const u of[-.7,.7])for(const E of[-.7,.7])for(const y of[-.7,.7])r.add(bn(new F(u,E,y),new xt(u,E,y),s,o,a,i))}if(e.klasa==="sve"){const _=document.createElement("div");_.className="udzbenik-silikati-traka",_.style.display="flex",_.style.flexWrap="wrap",_.style.gap="4px";const p=["nezo","soro","ciklo-3","ciklo-6","ino-jednostruki","ino-dvostruki","filo","tekto"];for(const u of p){const E=Fa[u],y=document.createElement("button");y.type="button",y.className="udzbenik-dugme udzbenik-dugme--malo",u===t&&y.classList.add("udzbenik-dugme--aktivno"),y.textContent=u,y.setAttribute("aria-label",E.naziv),y.addEventListener("click",()=>{t=u,_.querySelectorAll("button").forEach(M=>M.classList.remove("udzbenik-dugme--aktivno")),y.classList.add("udzbenik-dugme--aktivno"),l(u)}),_.append(y)}n.gornjeKontrole.append(_)}l(t);let d=0;const h=(e.animacija??(e.klasa==="sve"?"polimerizacija":"rotacija"))==="polimerizacija",f=["nezo","soro","ciklo-6","ino-jednostruki","ino-dvostruki","filo","tekto"];let m=0;function g(){s.color.set(n.tema.token("--primary")),o.color.set(n.tema.token("--accent"))}return{azuriraj(_){if(d+=_,r.rotation.y=d*.35,h){const p=Math.floor(d/3)%f.length;if(p!==m){m=p;const u=f[m];l(u)}}},korak(){d+=.3,r.rotation.y+=.2,h&&(m=(m+1)%f.length,l(f[m]))},resetuj(){d=0,r.rotation.set(0,0,0),m=0,l(t)},osveziTemu(){g()},raspolazi(){a.dispose(),s.dispose(),o.dispose(),Pt(r),c.remove()}}}},g0="Authier (2003), ITC Vol. D, §1.1.3.5.2 (репрезентативна површина тензора другог ранга) и §1.1.4 (Нојманов принцип); Nye (1985), погл. 1.",Ls=[{kljuc:"kubni",naziv:"Тесерални",oblik:"sfera",nezavisnih:1,veza:"сфера — својство је исто у свим правцима (изотропно)",oznakeOsa:["a₁","a₂","a₃"],celija:{a:1,b:1,c:1,alpha:90,beta:90,gamma:90}},{kljuc:"tetragonalni",naziv:"Тетрагонални",oblik:"obrtni",nezavisnih:2,veza:"обртни елипсоид, оса обртања ∥ c (оса четвртог степена)",oznakeOsa:["a₁","a₂","c"],celija:{a:1,b:1,c:1,alpha:90,beta:90,gamma:90}},{kljuc:"heksagonalni",naziv:"Хексагонални",oblik:"obrtni",nezavisnih:2,veza:"обртни елипсоид, оса обртања ∥ c (оса шестог степена)",oznakeOsa:["a₁","a₂","c"],celija:{a:1,b:1,c:1,alpha:90,beta:90,gamma:120}},{kljuc:"trigonalni",naziv:"Тригонални",oblik:"obrtni",nezavisnih:2,veza:"обртни елипсоид, оса обртања ∥ c (оса трећег степена; хексагонална поставка)",oznakeOsa:["a₁","a₂","c"],celija:{a:1,b:1,c:1,alpha:90,beta:90,gamma:120}},{kljuc:"ortorombicni",naziv:"Ромбични",oblik:"troosni",nezavisnih:3,veza:"троосни елипсоид, све три главне осе ∥ a, b, c",oznakeOsa:["a","b","c"],celija:{a:1,b:1,c:1,alpha:90,beta:90,gamma:90}},{kljuc:"monoklinicni",naziv:"Моноклинични",oblik:"troosni",nezavisnih:4,veza:"троосни елипсоид, једна главна оса ∥ b; друге две у равни a–c под углом φ који симетрија не одређује",oznakeOsa:["a","b","c"],celija:{a:1,b:1,c:1,alpha:90,beta:112,gamma:90}},{kljuc:"triklinicni",naziv:"Триклинични",oblik:"troosni",nezavisnih:6,veza:"троосни елипсоид, ниједна главна оса није везана за кристалографске осе",oznakeOsa:["a","b","c"],celija:{a:1,b:1,c:1,alpha:78,beta:109,gamma:103}}];function Rc(n){return Ls.find(e=>e.kljuc===n)??Ls[0]}function _0(n,e){return n==="sfera"?[e[0],e[0],e[0]]:n==="obrtni"?[e[0],e[0],e[2]]:[e[0],e[1],e[2]]}function v0(n,e){const t=e*Math.PI/180,i=new F(1,0,0),r=new F(0,1,0),a=new F(0,0,1);if(n==="monoklinicni"){const s=new F(0,0,-1),o=i.clone().applyAxisAngle(s,t),c=r.clone().applyAxisAngle(s,t);return[o,s,c]}if(n==="triklinicni"){const s=new F(1,.7,.4).normalize(),o=new Fi().setFromAxisAngle(s,.5+t);return[i.clone().applyQuaternion(o),a.clone().negate().applyQuaternion(o),r.clone().applyQuaternion(o)]}return[i,a.clone().negate(),r]}let Cc=0;const x0={sfera:["r"],obrtni:["r⊥ (⊥ c)","","r∥ (∥ c)"],troosni:["r₁","r₂","r₃"]},M0={imaPodrazumevanuAnimaciju(){return!1},pocetnaKamera(){return{theta:.62,phi:1.12,udaljenost:6.4}},kreiraj(n,e){const t=new Qe;n.scena3D.add(t);let i=e.sistem&&e.sistem!=="svi"?e.sistem:"ortorombicni";const r=[e.poluose?.[0]??1,e.poluose?.[1]??1.25,e.poluose?.[2]??1.5];let a=[...r],s=e.ugao_phi??25;const o=new ft({color:new oe(n.tema.token("--primary")),transparent:!0,opacity:.38,roughness:.3,metalness:.05,side:St,depthWrite:!1}),c=new lt({color:new oe(n.tema.token("--primary")),transparent:!0,opacity:.45}),l=new lt({color:new oe(n.tema.token("--text-primary"))}),d=new lt({color:new oe(n.tema.token("--danger"))}),h=new lt({color:new oe(n.tema.token("--success"))}),f=new lt({color:new oe(n.tema.token("--accent"))}),m=new Qe,g=new Qe;t.add(m,g);const _=new Yt(1,48,32),p=new Le(_,o),u=new Ou(new Yt(1,16,10)),E=new ut(u,c);g.add(p,E);const y=[],M=O=>{const q=document.createElement("span");q.className="udzbenik-scena-etiketa",O&&q.classList.add("udzbenik-scena-etiketa--istaknuta"),n.slojEtiketa.append(q);const K={span:q,tacka:new F};return y.push(K),K},D=[M(!1),M(!1),M(!1)],A=[M(!0),M(!0),M(!0)],b=document.createElement("div");b.className="udzbenik-sistemi-traka",b.setAttribute("role","group"),b.setAttribute("aria-label",ot("izaberiKristalniSistem"));const C=new Map;for(const O of Ls){const q=document.createElement("button");q.type="button",q.className="udzbenik-sistem-kartica";const K=document.createElement("span");K.className="udzbenik-sistem-kartica-naslov",K.textContent=O.naziv;const le=document.createElement("span");le.className="udzbenik-sistem-kartica-meta",le.textContent=`${O.nezavisnih} ${O.nezavisnih===1?"компонента":O.nezavisnih<5?"компоненте":"компонената"}`,q.append(K,le),q.addEventListener("click",()=>{i=O.kljuc,B()}),C.set(O.kljuc,q),b.append(q)}n.gornjeKontrole.append(b);const v=document.createElement("div");v.className="udzbenik-tenzor-klizaci",n.gornjeKontrole.append(v);const x=(O,q,K,le,De)=>{const X=document.createElement("div");X.className="udzbenik-kontrola-red",Cc+=1;const J=document.createElement("label");J.className="udzbenik-kontrola-labela";const ae=document.createElement("input");ae.id=`udz-tenzor-klizac-${Cc}`,J.htmlFor=ae.id,ae.type="range",ae.min=String(O),ae.max=String(q),ae.step=String(K),ae.value=String(le),ae.className="udzbenik-kontrola-klizac";const re=document.createElement("span");re.className="udzbenik-kontrola-vrednost",ae.addEventListener("input",()=>{De(parseFloat(ae.value)),B()});const ue=document.createElement("span");return J.append(ue),X.append(J,ae,re),v.append(X),{red:X,tekstLabele:ue,ulaz:ae,izlaz:re}},P=[0,1,2].map(O=>x(.6,1.8,.05,a[O],q=>a[O]=q)),U=x(0,180,1,s,O=>s=O),w=document.createElement("p");w.className="udzbenik-scena-info-red",w.setAttribute("aria-live","polite");const R=document.createElement("p");R.className="udzbenik-scena-izvor",R.textContent="Полуосе елипсоида r₁, r₂, r₃ су главне вредности приказане у произвољним јединицама. За квадрику Sᵢⱼxᵢxⱼ = 1 полуосе су 1/√Sᵢ; код оптичке индикатрисе полуосе су индекси преламања.";const z=document.createElement("p");z.className="udzbenik-scena-izvor",z.textContent=`${ot("izvorPodataka")}: ${g0}`,n.podnozje.append(w,R,z);const N=()=>{for(const O of m.children)O.geometry.dispose();m.clear()};function B(){const O=Rc(i);for(const[W,L]of C){const Ee=W===i;L.classList.toggle("udzbenik-sistem-kartica--aktivna",Ee),L.setAttribute("aria-pressed",String(Ee))}const q=x0[O.oblik];P.forEach((W,L)=>{const Ee=!!q[L];W.red.hidden=!Ee,W.tekstLabele.textContent=`${q[L]??""}:`,W.izlaz.textContent=a[L].toFixed(2).replace(".",",")}),U.red.hidden=O.oblik!=="troosni"||i==="ortorombicni",U.tekstLabele.textContent=i==="monoklinicni"?"угао φ у равни a–c (°):":"оријентација φ (°):",U.izlaz.textContent=`${Math.round(s)}°`,N();const K=Zr(O.celija),le=1.9,De=[K.va,K.vb,K.vc].map(W=>new F(...W).normalize()),X=[d,h,f];De.forEach((W,L)=>{const Ee=new Xe().setFromPoints([W.clone().multiplyScalar(-le),W.clone().multiplyScalar(le)]);m.add(new Qn(Ee,X[L])),D[L].span.textContent=O.oznakeOsa[L],D[L].tacka.copy(W).multiplyScalar(le+.15)});const[J,ae,re]=_0(O.oblik,a),[ue,Pe,fe]=v0(i,s),te=new at().makeBasis(ue,fe,Pe.clone().negate());g.setRotationFromMatrix(te),g.scale.set(J,re,ae),[ue.clone().multiplyScalar(J),Pe.clone().multiplyScalar(ae),fe.clone().multiplyScalar(re)].forEach((W,L)=>{const Ee=new Xe().setFromPoints([W.clone().multiplyScalar(-1),W]);m.add(new Qn(Ee,l)),A[L].span.textContent=`${L+1}`,A[L].tacka.copy(W).multiplyScalar(-(1+.14/W.length())),A[L].span.hidden=O.oblik==="sfera"}),w.textContent=`${O.naziv}: ${O.veza}. Независних компонената: ${O.nezavisnih}.`,n.zatraziRender()}function k(){t.updateMatrixWorld(!0);const O=Rc(i);for(const[q,K]of y.entries()){if(q>=3&&O.oblik==="sfera"){K.span.hidden=!0;continue}const le=n.projektujU2D(K.tacka.clone().applyMatrix4(t.matrixWorld));K.span.hidden=!le.vidljivo,K.span.style.transform=`translate(-50%, -50%) translate(${le.x.toFixed(1)}px, ${le.y.toFixed(1)}px)`}}return B(),{korak(){t.rotation.y+=.35},resetuj(){t.rotation.set(0,0,0),a=[...r],P.forEach((O,q)=>O.ulaz.value=String(a[q])),s=e.ugao_phi??25,U.ulaz.value=String(s),B()},osveziTemu(O){o.color.set(O.token("--primary")),c.color.set(O.token("--primary")),l.color.set(O.token("--text-primary")),d.color.set(O.token("--danger")),h.color.set(O.token("--success")),f.color.set(O.token("--accent"))},posleRendera(){k()},raspolazi(){N(),_.dispose(),u.dispose(),Pt(t);for(const O of[o,c,l,d,h,f])O.dispose();for(const O of y)O.span.remove()}}}},S0={"kristalni-sistem":l0,"kristalna-struktura":a0,"mohsova-skala":d0,cepljivost:Qm,habitus:i0,"bravaisova-resetka":Ym,"opticka-indikatrisa":f0,blizanac:Km,"koordinacioni-poliedar":r0,"silikatna-struktura":m0,"tenzor-drugog-ranga":M0};function b0(n,e,t){const i=S0[n.scena];return i?Xm(i,n.parametri,e,t):(e.prikaziRezervu("Сцена није подржана у овој верзији мотора."),()=>{})}export{b0 as pokreniScenuPoImenu,y0 as raspolaziDeljenimRendererom};
