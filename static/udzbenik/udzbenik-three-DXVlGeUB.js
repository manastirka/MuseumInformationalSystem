import{t as Xr,n as Jc,a as ot,g as Xs,b as Es,d as hc,f as Qc,A as el,p as qs,c as Ys,J as Ks,I as $s}from"./udzbenik-jezgro-5hpfdIwc.js";/**
 * @license
 * Copyright 2010-2025 Three.js Authors
 * SPDX-License-Identifier: MIT
 */const ys="174",tl=0,Zs=1,nl=2,fc=1,il=2,cn=3,Pn=0,Dt=1,mt=2,Rn=0,xi=1,Js=2,Qs=3,eo=4,rl=5,Wn=100,al=101,sl=102,ol=103,cl=104,ll=200,ul=201,dl=202,hl=203,Da=204,La=205,fl=206,pl=207,ml=208,gl=209,_l=210,vl=211,xl=212,Ml=213,Sl=214,Ia=0,Ua=1,za=2,Ei=3,Na=4,Fa=5,ka=6,Oa=7,pc=0,El=1,yl=2,Cn=0,bl=1,Tl=2,Al=3,wl=4,Rl=5,Cl=6,Pl=7,mc=300,yi=301,bi=302,Ba=303,Va=304,Vr=306,Ha=1e3,qn=1001,Ga=1002,Kt=1003,Dl=1004,er=1005,Zt=1006,qr=1007,Yn=1008,pn=1009,gc=1010,_c=1011,ji=1012,bs=1013,Zn=1014,un=1015,qi=1016,Ts=1017,As=1018,Ti=1020,vc=35902,xc=1021,Mc=1022,Yt=1023,Sc=1024,Ec=1025,Mi=1026,Ai=1027,yc=1028,ws=1029,bc=1030,Rs=1031,Cs=1033,wr=33776,Rr=33777,Cr=33778,Pr=33779,ja=35840,Wa=35841,Xa=35842,qa=35843,Ya=36196,Ka=37492,$a=37496,Za=37808,Ja=37809,Qa=37810,es=37811,ts=37812,ns=37813,is=37814,rs=37815,as=37816,ss=37817,os=37818,cs=37819,ls=37820,us=37821,Dr=36492,ds=36494,hs=36495,Tc=36283,fs=36284,ps=36285,ms=36286,Ll=3200,Il=3201,Ac=0,Ul=1,An="",Nt="srgb",wi="srgb-linear",zr="linear",it="srgb",ei=7680,to=519,zl=512,Nl=513,Fl=514,wc=515,kl=516,Ol=517,Bl=518,Vl=519,no=35044,io="300 es",dn=2e3,Nr=2001;class Ci{addEventListener(e,t){this._listeners===void 0&&(this._listeners={});const i=this._listeners;i[e]===void 0&&(i[e]=[]),i[e].indexOf(t)===-1&&i[e].push(t)}hasEventListener(e,t){const i=this._listeners;return i===void 0?!1:i[e]!==void 0&&i[e].indexOf(t)!==-1}removeEventListener(e,t){const i=this._listeners;if(i===void 0)return;const r=i[e];if(r!==void 0){const a=r.indexOf(t);a!==-1&&r.splice(a,1)}}dispatchEvent(e){const t=this._listeners;if(t===void 0)return;const i=t[e.type];if(i!==void 0){e.target=this;const r=i.slice(0);for(let a=0,s=r.length;a<s;a++)r[a].call(this,e);e.target=null}}}const bt=["00","01","02","03","04","05","06","07","08","09","0a","0b","0c","0d","0e","0f","10","11","12","13","14","15","16","17","18","19","1a","1b","1c","1d","1e","1f","20","21","22","23","24","25","26","27","28","29","2a","2b","2c","2d","2e","2f","30","31","32","33","34","35","36","37","38","39","3a","3b","3c","3d","3e","3f","40","41","42","43","44","45","46","47","48","49","4a","4b","4c","4d","4e","4f","50","51","52","53","54","55","56","57","58","59","5a","5b","5c","5d","5e","5f","60","61","62","63","64","65","66","67","68","69","6a","6b","6c","6d","6e","6f","70","71","72","73","74","75","76","77","78","79","7a","7b","7c","7d","7e","7f","80","81","82","83","84","85","86","87","88","89","8a","8b","8c","8d","8e","8f","90","91","92","93","94","95","96","97","98","99","9a","9b","9c","9d","9e","9f","a0","a1","a2","a3","a4","a5","a6","a7","a8","a9","aa","ab","ac","ad","ae","af","b0","b1","b2","b3","b4","b5","b6","b7","b8","b9","ba","bb","bc","bd","be","bf","c0","c1","c2","c3","c4","c5","c6","c7","c8","c9","ca","cb","cc","cd","ce","cf","d0","d1","d2","d3","d4","d5","d6","d7","d8","d9","da","db","dc","dd","de","df","e0","e1","e2","e3","e4","e5","e6","e7","e8","e9","ea","eb","ec","ed","ee","ef","f0","f1","f2","f3","f4","f5","f6","f7","f8","f9","fa","fb","fc","fd","fe","ff"],Lr=Math.PI/180,gs=180/Math.PI;function Yi(){const n=Math.random()*4294967295|0,e=Math.random()*4294967295|0,t=Math.random()*4294967295|0,i=Math.random()*4294967295|0;return(bt[n&255]+bt[n>>8&255]+bt[n>>16&255]+bt[n>>24&255]+"-"+bt[e&255]+bt[e>>8&255]+"-"+bt[e>>16&15|64]+bt[e>>24&255]+"-"+bt[t&63|128]+bt[t>>8&255]+"-"+bt[t>>16&255]+bt[t>>24&255]+bt[i&255]+bt[i>>8&255]+bt[i>>16&255]+bt[i>>24&255]).toLowerCase()}function We(n,e,t){return Math.max(e,Math.min(t,n))}function Hl(n,e){return(n%e+e)%e}function Yr(n,e,t){return(1-t)*n+t*e}function zi(n,e){switch(e.constructor){case Float32Array:return n;case Uint32Array:return n/4294967295;case Uint16Array:return n/65535;case Uint8Array:return n/255;case Int32Array:return Math.max(n/2147483647,-1);case Int16Array:return Math.max(n/32767,-1);case Int8Array:return Math.max(n/127,-1);default:throw new Error("Invalid component type.")}}function Pt(n,e){switch(e.constructor){case Float32Array:return n;case Uint32Array:return Math.round(n*4294967295);case Uint16Array:return Math.round(n*65535);case Uint8Array:return Math.round(n*255);case Int32Array:return Math.round(n*2147483647);case Int16Array:return Math.round(n*32767);case Int8Array:return Math.round(n*127);default:throw new Error("Invalid component type.")}}class Xe{constructor(e=0,t=0){Xe.prototype.isVector2=!0,this.x=e,this.y=t}get width(){return this.x}set width(e){this.x=e}get height(){return this.y}set height(e){this.y=e}set(e,t){return this.x=e,this.y=t,this}setScalar(e){return this.x=e,this.y=e,this}setX(e){return this.x=e,this}setY(e){return this.y=e,this}setComponent(e,t){switch(e){case 0:this.x=t;break;case 1:this.y=t;break;default:throw new Error("index is out of range: "+e)}return this}getComponent(e){switch(e){case 0:return this.x;case 1:return this.y;default:throw new Error("index is out of range: "+e)}}clone(){return new this.constructor(this.x,this.y)}copy(e){return this.x=e.x,this.y=e.y,this}add(e){return this.x+=e.x,this.y+=e.y,this}addScalar(e){return this.x+=e,this.y+=e,this}addVectors(e,t){return this.x=e.x+t.x,this.y=e.y+t.y,this}addScaledVector(e,t){return this.x+=e.x*t,this.y+=e.y*t,this}sub(e){return this.x-=e.x,this.y-=e.y,this}subScalar(e){return this.x-=e,this.y-=e,this}subVectors(e,t){return this.x=e.x-t.x,this.y=e.y-t.y,this}multiply(e){return this.x*=e.x,this.y*=e.y,this}multiplyScalar(e){return this.x*=e,this.y*=e,this}divide(e){return this.x/=e.x,this.y/=e.y,this}divideScalar(e){return this.multiplyScalar(1/e)}applyMatrix3(e){const t=this.x,i=this.y,r=e.elements;return this.x=r[0]*t+r[3]*i+r[6],this.y=r[1]*t+r[4]*i+r[7],this}min(e){return this.x=Math.min(this.x,e.x),this.y=Math.min(this.y,e.y),this}max(e){return this.x=Math.max(this.x,e.x),this.y=Math.max(this.y,e.y),this}clamp(e,t){return this.x=We(this.x,e.x,t.x),this.y=We(this.y,e.y,t.y),this}clampScalar(e,t){return this.x=We(this.x,e,t),this.y=We(this.y,e,t),this}clampLength(e,t){const i=this.length();return this.divideScalar(i||1).multiplyScalar(We(i,e,t))}floor(){return this.x=Math.floor(this.x),this.y=Math.floor(this.y),this}ceil(){return this.x=Math.ceil(this.x),this.y=Math.ceil(this.y),this}round(){return this.x=Math.round(this.x),this.y=Math.round(this.y),this}roundToZero(){return this.x=Math.trunc(this.x),this.y=Math.trunc(this.y),this}negate(){return this.x=-this.x,this.y=-this.y,this}dot(e){return this.x*e.x+this.y*e.y}cross(e){return this.x*e.y-this.y*e.x}lengthSq(){return this.x*this.x+this.y*this.y}length(){return Math.sqrt(this.x*this.x+this.y*this.y)}manhattanLength(){return Math.abs(this.x)+Math.abs(this.y)}normalize(){return this.divideScalar(this.length()||1)}angle(){return Math.atan2(-this.y,-this.x)+Math.PI}angleTo(e){const t=Math.sqrt(this.lengthSq()*e.lengthSq());if(t===0)return Math.PI/2;const i=this.dot(e)/t;return Math.acos(We(i,-1,1))}distanceTo(e){return Math.sqrt(this.distanceToSquared(e))}distanceToSquared(e){const t=this.x-e.x,i=this.y-e.y;return t*t+i*i}manhattanDistanceTo(e){return Math.abs(this.x-e.x)+Math.abs(this.y-e.y)}setLength(e){return this.normalize().multiplyScalar(e)}lerp(e,t){return this.x+=(e.x-this.x)*t,this.y+=(e.y-this.y)*t,this}lerpVectors(e,t,i){return this.x=e.x+(t.x-e.x)*i,this.y=e.y+(t.y-e.y)*i,this}equals(e){return e.x===this.x&&e.y===this.y}fromArray(e,t=0){return this.x=e[t],this.y=e[t+1],this}toArray(e=[],t=0){return e[t]=this.x,e[t+1]=this.y,e}fromBufferAttribute(e,t){return this.x=e.getX(t),this.y=e.getY(t),this}rotateAround(e,t){const i=Math.cos(t),r=Math.sin(t),a=this.x-e.x,s=this.y-e.y;return this.x=a*i-s*r+e.x,this.y=a*r+s*i+e.y,this}random(){return this.x=Math.random(),this.y=Math.random(),this}*[Symbol.iterator](){yield this.x,yield this.y}}class Be{constructor(e,t,i,r,a,s,o,c,l){Be.prototype.isMatrix3=!0,this.elements=[1,0,0,0,1,0,0,0,1],e!==void 0&&this.set(e,t,i,r,a,s,o,c,l)}set(e,t,i,r,a,s,o,c,l){const d=this.elements;return d[0]=e,d[1]=r,d[2]=o,d[3]=t,d[4]=a,d[5]=c,d[6]=i,d[7]=s,d[8]=l,this}identity(){return this.set(1,0,0,0,1,0,0,0,1),this}copy(e){const t=this.elements,i=e.elements;return t[0]=i[0],t[1]=i[1],t[2]=i[2],t[3]=i[3],t[4]=i[4],t[5]=i[5],t[6]=i[6],t[7]=i[7],t[8]=i[8],this}extractBasis(e,t,i){return e.setFromMatrix3Column(this,0),t.setFromMatrix3Column(this,1),i.setFromMatrix3Column(this,2),this}setFromMatrix4(e){const t=e.elements;return this.set(t[0],t[4],t[8],t[1],t[5],t[9],t[2],t[6],t[10]),this}multiply(e){return this.multiplyMatrices(this,e)}premultiply(e){return this.multiplyMatrices(e,this)}multiplyMatrices(e,t){const i=e.elements,r=t.elements,a=this.elements,s=i[0],o=i[3],c=i[6],l=i[1],d=i[4],h=i[7],f=i[2],m=i[5],g=i[8],_=r[0],p=r[3],u=r[6],y=r[1],S=r[4],M=r[7],T=r[2],b=r[5],w=r[8];return a[0]=s*_+o*y+c*T,a[3]=s*p+o*S+c*b,a[6]=s*u+o*M+c*w,a[1]=l*_+d*y+h*T,a[4]=l*p+d*S+h*b,a[7]=l*u+d*M+h*w,a[2]=f*_+m*y+g*T,a[5]=f*p+m*S+g*b,a[8]=f*u+m*M+g*w,this}multiplyScalar(e){const t=this.elements;return t[0]*=e,t[3]*=e,t[6]*=e,t[1]*=e,t[4]*=e,t[7]*=e,t[2]*=e,t[5]*=e,t[8]*=e,this}determinant(){const e=this.elements,t=e[0],i=e[1],r=e[2],a=e[3],s=e[4],o=e[5],c=e[6],l=e[7],d=e[8];return t*s*d-t*o*l-i*a*d+i*o*c+r*a*l-r*s*c}invert(){const e=this.elements,t=e[0],i=e[1],r=e[2],a=e[3],s=e[4],o=e[5],c=e[6],l=e[7],d=e[8],h=d*s-o*l,f=o*c-d*a,m=l*a-s*c,g=t*h+i*f+r*m;if(g===0)return this.set(0,0,0,0,0,0,0,0,0);const _=1/g;return e[0]=h*_,e[1]=(r*l-d*i)*_,e[2]=(o*i-r*s)*_,e[3]=f*_,e[4]=(d*t-r*c)*_,e[5]=(r*a-o*t)*_,e[6]=m*_,e[7]=(i*c-l*t)*_,e[8]=(s*t-i*a)*_,this}transpose(){let e;const t=this.elements;return e=t[1],t[1]=t[3],t[3]=e,e=t[2],t[2]=t[6],t[6]=e,e=t[5],t[5]=t[7],t[7]=e,this}getNormalMatrix(e){return this.setFromMatrix4(e).invert().transpose()}transposeIntoArray(e){const t=this.elements;return e[0]=t[0],e[1]=t[3],e[2]=t[6],e[3]=t[1],e[4]=t[4],e[5]=t[7],e[6]=t[2],e[7]=t[5],e[8]=t[8],this}setUvTransform(e,t,i,r,a,s,o){const c=Math.cos(a),l=Math.sin(a);return this.set(i*c,i*l,-i*(c*s+l*o)+s+e,-r*l,r*c,-r*(-l*s+c*o)+o+t,0,0,1),this}scale(e,t){return this.premultiply(Kr.makeScale(e,t)),this}rotate(e){return this.premultiply(Kr.makeRotation(-e)),this}translate(e,t){return this.premultiply(Kr.makeTranslation(e,t)),this}makeTranslation(e,t){return e.isVector2?this.set(1,0,e.x,0,1,e.y,0,0,1):this.set(1,0,e,0,1,t,0,0,1),this}makeRotation(e){const t=Math.cos(e),i=Math.sin(e);return this.set(t,-i,0,i,t,0,0,0,1),this}makeScale(e,t){return this.set(e,0,0,0,t,0,0,0,1),this}equals(e){const t=this.elements,i=e.elements;for(let r=0;r<9;r++)if(t[r]!==i[r])return!1;return!0}fromArray(e,t=0){for(let i=0;i<9;i++)this.elements[i]=e[i+t];return this}toArray(e=[],t=0){const i=this.elements;return e[t]=i[0],e[t+1]=i[1],e[t+2]=i[2],e[t+3]=i[3],e[t+4]=i[4],e[t+5]=i[5],e[t+6]=i[6],e[t+7]=i[7],e[t+8]=i[8],e}clone(){return new this.constructor().fromArray(this.elements)}}const Kr=new Be;function Rc(n){for(let e=n.length-1;e>=0;--e)if(n[e]>=65535)return!0;return!1}function Fr(n){return document.createElementNS("http://www.w3.org/1999/xhtml",n)}function Gl(){const n=Fr("canvas");return n.style.display="block",n}const ro={};function Bn(n){n in ro||(ro[n]=!0,console.warn(n))}function jl(n,e,t){return new Promise(function(i,r){function a(){switch(n.clientWaitSync(e,n.SYNC_FLUSH_COMMANDS_BIT,0)){case n.WAIT_FAILED:r();break;case n.TIMEOUT_EXPIRED:setTimeout(a,t);break;default:i()}}setTimeout(a,t)})}function Wl(n){const e=n.elements;e[2]=.5*e[2]+.5*e[3],e[6]=.5*e[6]+.5*e[7],e[10]=.5*e[10]+.5*e[11],e[14]=.5*e[14]+.5*e[15]}function Xl(n){const e=n.elements;e[11]===-1?(e[10]=-e[10]-1,e[14]=-e[14]):(e[10]=-e[10],e[14]=-e[14]+1)}const ao=new Be().set(.4123908,.3575843,.1804808,.212639,.7151687,.0721923,.0193308,.1191948,.9505322),so=new Be().set(3.2409699,-1.5373832,-.4986108,-.9692436,1.8759675,.0415551,.0556301,-.203977,1.0569715);function ql(){const n={enabled:!0,workingColorSpace:wi,spaces:{},convert:function(r,a,s){return this.enabled===!1||a===s||!a||!s||(this.spaces[a].transfer===it&&(r.r=fn(r.r),r.g=fn(r.g),r.b=fn(r.b)),this.spaces[a].primaries!==this.spaces[s].primaries&&(r.applyMatrix3(this.spaces[a].toXYZ),r.applyMatrix3(this.spaces[s].fromXYZ)),this.spaces[s].transfer===it&&(r.r=Si(r.r),r.g=Si(r.g),r.b=Si(r.b))),r},fromWorkingColorSpace:function(r,a){return this.convert(r,this.workingColorSpace,a)},toWorkingColorSpace:function(r,a){return this.convert(r,a,this.workingColorSpace)},getPrimaries:function(r){return this.spaces[r].primaries},getTransfer:function(r){return r===An?zr:this.spaces[r].transfer},getLuminanceCoefficients:function(r,a=this.workingColorSpace){return r.fromArray(this.spaces[a].luminanceCoefficients)},define:function(r){Object.assign(this.spaces,r)},_getMatrix:function(r,a,s){return r.copy(this.spaces[a].toXYZ).multiply(this.spaces[s].fromXYZ)},_getDrawingBufferColorSpace:function(r){return this.spaces[r].outputColorSpaceConfig.drawingBufferColorSpace},_getUnpackColorSpace:function(r=this.workingColorSpace){return this.spaces[r].workingColorSpaceConfig.unpackColorSpace}},e=[.64,.33,.3,.6,.15,.06],t=[.2126,.7152,.0722],i=[.3127,.329];return n.define({[wi]:{primaries:e,whitePoint:i,transfer:zr,toXYZ:ao,fromXYZ:so,luminanceCoefficients:t,workingColorSpaceConfig:{unpackColorSpace:Nt},outputColorSpaceConfig:{drawingBufferColorSpace:Nt}},[Nt]:{primaries:e,whitePoint:i,transfer:it,toXYZ:ao,fromXYZ:so,luminanceCoefficients:t,outputColorSpaceConfig:{drawingBufferColorSpace:Nt}}}),n}const Je=ql();function fn(n){return n<.04045?n*.0773993808:Math.pow(n*.9478672986+.0521327014,2.4)}function Si(n){return n<.0031308?n*12.92:1.055*Math.pow(n,.41666)-.055}let ti;class Yl{static getDataURL(e){if(/^data:/i.test(e.src)||typeof HTMLCanvasElement>"u")return e.src;let t;if(e instanceof HTMLCanvasElement)t=e;else{ti===void 0&&(ti=Fr("canvas")),ti.width=e.width,ti.height=e.height;const i=ti.getContext("2d");e instanceof ImageData?i.putImageData(e,0,0):i.drawImage(e,0,0,e.width,e.height),t=ti}return t.toDataURL("image/png")}static sRGBToLinear(e){if(typeof HTMLImageElement<"u"&&e instanceof HTMLImageElement||typeof HTMLCanvasElement<"u"&&e instanceof HTMLCanvasElement||typeof ImageBitmap<"u"&&e instanceof ImageBitmap){const t=Fr("canvas");t.width=e.width,t.height=e.height;const i=t.getContext("2d");i.drawImage(e,0,0,e.width,e.height);const r=i.getImageData(0,0,e.width,e.height),a=r.data;for(let s=0;s<a.length;s++)a[s]=fn(a[s]/255)*255;return i.putImageData(r,0,0),t}else if(e.data){const t=e.data.slice(0);for(let i=0;i<t.length;i++)t instanceof Uint8Array||t instanceof Uint8ClampedArray?t[i]=Math.floor(fn(t[i]/255)*255):t[i]=fn(t[i]);return{data:t,width:e.width,height:e.height}}else return console.warn("THREE.ImageUtils.sRGBToLinear(): Unsupported image type. No color space conversion applied."),e}}let Kl=0;class Ps{constructor(e=null){this.isSource=!0,Object.defineProperty(this,"id",{value:Kl++}),this.uuid=Yi(),this.data=e,this.dataReady=!0,this.version=0}set needsUpdate(e){e===!0&&this.version++}toJSON(e){const t=e===void 0||typeof e=="string";if(!t&&e.images[this.uuid]!==void 0)return e.images[this.uuid];const i={uuid:this.uuid,url:""},r=this.data;if(r!==null){let a;if(Array.isArray(r)){a=[];for(let s=0,o=r.length;s<o;s++)r[s].isDataTexture?a.push($r(r[s].image)):a.push($r(r[s]))}else a=$r(r);i.url=a}return t||(e.images[this.uuid]=i),i}}function $r(n){return typeof HTMLImageElement<"u"&&n instanceof HTMLImageElement||typeof HTMLCanvasElement<"u"&&n instanceof HTMLCanvasElement||typeof ImageBitmap<"u"&&n instanceof ImageBitmap?Yl.getDataURL(n):n.data?{data:Array.from(n.data),width:n.width,height:n.height,type:n.data.constructor.name}:(console.warn("THREE.Texture: Unable to serialize Texture."),{})}let $l=0;class Rt extends Ci{constructor(e=Rt.DEFAULT_IMAGE,t=Rt.DEFAULT_MAPPING,i=qn,r=qn,a=Zt,s=Yn,o=Yt,c=pn,l=Rt.DEFAULT_ANISOTROPY,d=An){super(),this.isTexture=!0,Object.defineProperty(this,"id",{value:$l++}),this.uuid=Yi(),this.name="",this.source=new Ps(e),this.mipmaps=[],this.mapping=t,this.channel=0,this.wrapS=i,this.wrapT=r,this.magFilter=a,this.minFilter=s,this.anisotropy=l,this.format=o,this.internalFormat=null,this.type=c,this.offset=new Xe(0,0),this.repeat=new Xe(1,1),this.center=new Xe(0,0),this.rotation=0,this.matrixAutoUpdate=!0,this.matrix=new Be,this.generateMipmaps=!0,this.premultiplyAlpha=!1,this.flipY=!0,this.unpackAlignment=4,this.colorSpace=d,this.userData={},this.version=0,this.onUpdate=null,this.renderTarget=null,this.isRenderTargetTexture=!1,this.pmremVersion=0}get image(){return this.source.data}set image(e=null){this.source.data=e}updateMatrix(){this.matrix.setUvTransform(this.offset.x,this.offset.y,this.repeat.x,this.repeat.y,this.rotation,this.center.x,this.center.y)}clone(){return new this.constructor().copy(this)}copy(e){return this.name=e.name,this.source=e.source,this.mipmaps=e.mipmaps.slice(0),this.mapping=e.mapping,this.channel=e.channel,this.wrapS=e.wrapS,this.wrapT=e.wrapT,this.magFilter=e.magFilter,this.minFilter=e.minFilter,this.anisotropy=e.anisotropy,this.format=e.format,this.internalFormat=e.internalFormat,this.type=e.type,this.offset.copy(e.offset),this.repeat.copy(e.repeat),this.center.copy(e.center),this.rotation=e.rotation,this.matrixAutoUpdate=e.matrixAutoUpdate,this.matrix.copy(e.matrix),this.generateMipmaps=e.generateMipmaps,this.premultiplyAlpha=e.premultiplyAlpha,this.flipY=e.flipY,this.unpackAlignment=e.unpackAlignment,this.colorSpace=e.colorSpace,this.renderTarget=e.renderTarget,this.isRenderTargetTexture=e.isRenderTargetTexture,this.userData=JSON.parse(JSON.stringify(e.userData)),this.needsUpdate=!0,this}toJSON(e){const t=e===void 0||typeof e=="string";if(!t&&e.textures[this.uuid]!==void 0)return e.textures[this.uuid];const i={metadata:{version:4.6,type:"Texture",generator:"Texture.toJSON"},uuid:this.uuid,name:this.name,image:this.source.toJSON(e).uuid,mapping:this.mapping,channel:this.channel,repeat:[this.repeat.x,this.repeat.y],offset:[this.offset.x,this.offset.y],center:[this.center.x,this.center.y],rotation:this.rotation,wrap:[this.wrapS,this.wrapT],format:this.format,internalFormat:this.internalFormat,type:this.type,colorSpace:this.colorSpace,minFilter:this.minFilter,magFilter:this.magFilter,anisotropy:this.anisotropy,flipY:this.flipY,generateMipmaps:this.generateMipmaps,premultiplyAlpha:this.premultiplyAlpha,unpackAlignment:this.unpackAlignment};return Object.keys(this.userData).length>0&&(i.userData=this.userData),t||(e.textures[this.uuid]=i),i}dispose(){this.dispatchEvent({type:"dispose"})}transformUv(e){if(this.mapping!==mc)return e;if(e.applyMatrix3(this.matrix),e.x<0||e.x>1)switch(this.wrapS){case Ha:e.x=e.x-Math.floor(e.x);break;case qn:e.x=e.x<0?0:1;break;case Ga:Math.abs(Math.floor(e.x)%2)===1?e.x=Math.ceil(e.x)-e.x:e.x=e.x-Math.floor(e.x);break}if(e.y<0||e.y>1)switch(this.wrapT){case Ha:e.y=e.y-Math.floor(e.y);break;case qn:e.y=e.y<0?0:1;break;case Ga:Math.abs(Math.floor(e.y)%2)===1?e.y=Math.ceil(e.y)-e.y:e.y=e.y-Math.floor(e.y);break}return this.flipY&&(e.y=1-e.y),e}set needsUpdate(e){e===!0&&(this.version++,this.source.needsUpdate=!0)}set needsPMREMUpdate(e){e===!0&&this.pmremVersion++}}Rt.DEFAULT_IMAGE=null;Rt.DEFAULT_MAPPING=mc;Rt.DEFAULT_ANISOTROPY=1;class dt{constructor(e=0,t=0,i=0,r=1){dt.prototype.isVector4=!0,this.x=e,this.y=t,this.z=i,this.w=r}get width(){return this.z}set width(e){this.z=e}get height(){return this.w}set height(e){this.w=e}set(e,t,i,r){return this.x=e,this.y=t,this.z=i,this.w=r,this}setScalar(e){return this.x=e,this.y=e,this.z=e,this.w=e,this}setX(e){return this.x=e,this}setY(e){return this.y=e,this}setZ(e){return this.z=e,this}setW(e){return this.w=e,this}setComponent(e,t){switch(e){case 0:this.x=t;break;case 1:this.y=t;break;case 2:this.z=t;break;case 3:this.w=t;break;default:throw new Error("index is out of range: "+e)}return this}getComponent(e){switch(e){case 0:return this.x;case 1:return this.y;case 2:return this.z;case 3:return this.w;default:throw new Error("index is out of range: "+e)}}clone(){return new this.constructor(this.x,this.y,this.z,this.w)}copy(e){return this.x=e.x,this.y=e.y,this.z=e.z,this.w=e.w!==void 0?e.w:1,this}add(e){return this.x+=e.x,this.y+=e.y,this.z+=e.z,this.w+=e.w,this}addScalar(e){return this.x+=e,this.y+=e,this.z+=e,this.w+=e,this}addVectors(e,t){return this.x=e.x+t.x,this.y=e.y+t.y,this.z=e.z+t.z,this.w=e.w+t.w,this}addScaledVector(e,t){return this.x+=e.x*t,this.y+=e.y*t,this.z+=e.z*t,this.w+=e.w*t,this}sub(e){return this.x-=e.x,this.y-=e.y,this.z-=e.z,this.w-=e.w,this}subScalar(e){return this.x-=e,this.y-=e,this.z-=e,this.w-=e,this}subVectors(e,t){return this.x=e.x-t.x,this.y=e.y-t.y,this.z=e.z-t.z,this.w=e.w-t.w,this}multiply(e){return this.x*=e.x,this.y*=e.y,this.z*=e.z,this.w*=e.w,this}multiplyScalar(e){return this.x*=e,this.y*=e,this.z*=e,this.w*=e,this}applyMatrix4(e){const t=this.x,i=this.y,r=this.z,a=this.w,s=e.elements;return this.x=s[0]*t+s[4]*i+s[8]*r+s[12]*a,this.y=s[1]*t+s[5]*i+s[9]*r+s[13]*a,this.z=s[2]*t+s[6]*i+s[10]*r+s[14]*a,this.w=s[3]*t+s[7]*i+s[11]*r+s[15]*a,this}divide(e){return this.x/=e.x,this.y/=e.y,this.z/=e.z,this.w/=e.w,this}divideScalar(e){return this.multiplyScalar(1/e)}setAxisAngleFromQuaternion(e){this.w=2*Math.acos(e.w);const t=Math.sqrt(1-e.w*e.w);return t<1e-4?(this.x=1,this.y=0,this.z=0):(this.x=e.x/t,this.y=e.y/t,this.z=e.z/t),this}setAxisAngleFromRotationMatrix(e){let t,i,r,a;const c=e.elements,l=c[0],d=c[4],h=c[8],f=c[1],m=c[5],g=c[9],_=c[2],p=c[6],u=c[10];if(Math.abs(d-f)<.01&&Math.abs(h-_)<.01&&Math.abs(g-p)<.01){if(Math.abs(d+f)<.1&&Math.abs(h+_)<.1&&Math.abs(g+p)<.1&&Math.abs(l+m+u-3)<.1)return this.set(1,0,0,0),this;t=Math.PI;const S=(l+1)/2,M=(m+1)/2,T=(u+1)/2,b=(d+f)/4,w=(h+_)/4,L=(g+p)/4;return S>M&&S>T?S<.01?(i=0,r=.707106781,a=.707106781):(i=Math.sqrt(S),r=b/i,a=w/i):M>T?M<.01?(i=.707106781,r=0,a=.707106781):(r=Math.sqrt(M),i=b/r,a=L/r):T<.01?(i=.707106781,r=.707106781,a=0):(a=Math.sqrt(T),i=w/a,r=L/a),this.set(i,r,a,t),this}let y=Math.sqrt((p-g)*(p-g)+(h-_)*(h-_)+(f-d)*(f-d));return Math.abs(y)<.001&&(y=1),this.x=(p-g)/y,this.y=(h-_)/y,this.z=(f-d)/y,this.w=Math.acos((l+m+u-1)/2),this}setFromMatrixPosition(e){const t=e.elements;return this.x=t[12],this.y=t[13],this.z=t[14],this.w=t[15],this}min(e){return this.x=Math.min(this.x,e.x),this.y=Math.min(this.y,e.y),this.z=Math.min(this.z,e.z),this.w=Math.min(this.w,e.w),this}max(e){return this.x=Math.max(this.x,e.x),this.y=Math.max(this.y,e.y),this.z=Math.max(this.z,e.z),this.w=Math.max(this.w,e.w),this}clamp(e,t){return this.x=We(this.x,e.x,t.x),this.y=We(this.y,e.y,t.y),this.z=We(this.z,e.z,t.z),this.w=We(this.w,e.w,t.w),this}clampScalar(e,t){return this.x=We(this.x,e,t),this.y=We(this.y,e,t),this.z=We(this.z,e,t),this.w=We(this.w,e,t),this}clampLength(e,t){const i=this.length();return this.divideScalar(i||1).multiplyScalar(We(i,e,t))}floor(){return this.x=Math.floor(this.x),this.y=Math.floor(this.y),this.z=Math.floor(this.z),this.w=Math.floor(this.w),this}ceil(){return this.x=Math.ceil(this.x),this.y=Math.ceil(this.y),this.z=Math.ceil(this.z),this.w=Math.ceil(this.w),this}round(){return this.x=Math.round(this.x),this.y=Math.round(this.y),this.z=Math.round(this.z),this.w=Math.round(this.w),this}roundToZero(){return this.x=Math.trunc(this.x),this.y=Math.trunc(this.y),this.z=Math.trunc(this.z),this.w=Math.trunc(this.w),this}negate(){return this.x=-this.x,this.y=-this.y,this.z=-this.z,this.w=-this.w,this}dot(e){return this.x*e.x+this.y*e.y+this.z*e.z+this.w*e.w}lengthSq(){return this.x*this.x+this.y*this.y+this.z*this.z+this.w*this.w}length(){return Math.sqrt(this.x*this.x+this.y*this.y+this.z*this.z+this.w*this.w)}manhattanLength(){return Math.abs(this.x)+Math.abs(this.y)+Math.abs(this.z)+Math.abs(this.w)}normalize(){return this.divideScalar(this.length()||1)}setLength(e){return this.normalize().multiplyScalar(e)}lerp(e,t){return this.x+=(e.x-this.x)*t,this.y+=(e.y-this.y)*t,this.z+=(e.z-this.z)*t,this.w+=(e.w-this.w)*t,this}lerpVectors(e,t,i){return this.x=e.x+(t.x-e.x)*i,this.y=e.y+(t.y-e.y)*i,this.z=e.z+(t.z-e.z)*i,this.w=e.w+(t.w-e.w)*i,this}equals(e){return e.x===this.x&&e.y===this.y&&e.z===this.z&&e.w===this.w}fromArray(e,t=0){return this.x=e[t],this.y=e[t+1],this.z=e[t+2],this.w=e[t+3],this}toArray(e=[],t=0){return e[t]=this.x,e[t+1]=this.y,e[t+2]=this.z,e[t+3]=this.w,e}fromBufferAttribute(e,t){return this.x=e.getX(t),this.y=e.getY(t),this.z=e.getZ(t),this.w=e.getW(t),this}random(){return this.x=Math.random(),this.y=Math.random(),this.z=Math.random(),this.w=Math.random(),this}*[Symbol.iterator](){yield this.x,yield this.y,yield this.z,yield this.w}}class Zl extends Ci{constructor(e=1,t=1,i={}){super(),this.isRenderTarget=!0,this.width=e,this.height=t,this.depth=1,this.scissor=new dt(0,0,e,t),this.scissorTest=!1,this.viewport=new dt(0,0,e,t);const r={width:e,height:t,depth:1};i=Object.assign({generateMipmaps:!1,internalFormat:null,minFilter:Zt,depthBuffer:!0,stencilBuffer:!1,resolveDepthBuffer:!0,resolveStencilBuffer:!0,depthTexture:null,samples:0,count:1},i);const a=new Rt(r,i.mapping,i.wrapS,i.wrapT,i.magFilter,i.minFilter,i.format,i.type,i.anisotropy,i.colorSpace);a.flipY=!1,a.generateMipmaps=i.generateMipmaps,a.internalFormat=i.internalFormat,this.textures=[];const s=i.count;for(let o=0;o<s;o++)this.textures[o]=a.clone(),this.textures[o].isRenderTargetTexture=!0,this.textures[o].renderTarget=this;this.depthBuffer=i.depthBuffer,this.stencilBuffer=i.stencilBuffer,this.resolveDepthBuffer=i.resolveDepthBuffer,this.resolveStencilBuffer=i.resolveStencilBuffer,this._depthTexture=null,this.depthTexture=i.depthTexture,this.samples=i.samples}get texture(){return this.textures[0]}set texture(e){this.textures[0]=e}set depthTexture(e){this._depthTexture!==null&&(this._depthTexture.renderTarget=null),e!==null&&(e.renderTarget=this),this._depthTexture=e}get depthTexture(){return this._depthTexture}setSize(e,t,i=1){if(this.width!==e||this.height!==t||this.depth!==i){this.width=e,this.height=t,this.depth=i;for(let r=0,a=this.textures.length;r<a;r++)this.textures[r].image.width=e,this.textures[r].image.height=t,this.textures[r].image.depth=i;this.dispose()}this.viewport.set(0,0,e,t),this.scissor.set(0,0,e,t)}clone(){return new this.constructor().copy(this)}copy(e){this.width=e.width,this.height=e.height,this.depth=e.depth,this.scissor.copy(e.scissor),this.scissorTest=e.scissorTest,this.viewport.copy(e.viewport),this.textures.length=0;for(let t=0,i=e.textures.length;t<i;t++){this.textures[t]=e.textures[t].clone(),this.textures[t].isRenderTargetTexture=!0,this.textures[t].renderTarget=this;const r=Object.assign({},e.textures[t].image);this.textures[t].source=new Ps(r)}return this.depthBuffer=e.depthBuffer,this.stencilBuffer=e.stencilBuffer,this.resolveDepthBuffer=e.resolveDepthBuffer,this.resolveStencilBuffer=e.resolveStencilBuffer,e.depthTexture!==null&&(this.depthTexture=e.depthTexture.clone()),this.samples=e.samples,this}dispose(){this.dispatchEvent({type:"dispose"})}}class Jn extends Zl{constructor(e=1,t=1,i={}){super(e,t,i),this.isWebGLRenderTarget=!0}}class Cc extends Rt{constructor(e=null,t=1,i=1,r=1){super(null),this.isDataArrayTexture=!0,this.image={data:e,width:t,height:i,depth:r},this.magFilter=Kt,this.minFilter=Kt,this.wrapR=qn,this.generateMipmaps=!1,this.flipY=!1,this.unpackAlignment=1,this.layerUpdates=new Set}addLayerUpdate(e){this.layerUpdates.add(e)}clearLayerUpdates(){this.layerUpdates.clear()}}class Jl extends Rt{constructor(e=null,t=1,i=1,r=1){super(null),this.isData3DTexture=!0,this.image={data:e,width:t,height:i,depth:r},this.magFilter=Kt,this.minFilter=Kt,this.wrapR=qn,this.generateMipmaps=!1,this.flipY=!1,this.unpackAlignment=1}}class Ki{constructor(e=0,t=0,i=0,r=1){this.isQuaternion=!0,this._x=e,this._y=t,this._z=i,this._w=r}static slerpFlat(e,t,i,r,a,s,o){let c=i[r+0],l=i[r+1],d=i[r+2],h=i[r+3];const f=a[s+0],m=a[s+1],g=a[s+2],_=a[s+3];if(o===0){e[t+0]=c,e[t+1]=l,e[t+2]=d,e[t+3]=h;return}if(o===1){e[t+0]=f,e[t+1]=m,e[t+2]=g,e[t+3]=_;return}if(h!==_||c!==f||l!==m||d!==g){let p=1-o;const u=c*f+l*m+d*g+h*_,y=u>=0?1:-1,S=1-u*u;if(S>Number.EPSILON){const T=Math.sqrt(S),b=Math.atan2(T,u*y);p=Math.sin(p*b)/T,o=Math.sin(o*b)/T}const M=o*y;if(c=c*p+f*M,l=l*p+m*M,d=d*p+g*M,h=h*p+_*M,p===1-o){const T=1/Math.sqrt(c*c+l*l+d*d+h*h);c*=T,l*=T,d*=T,h*=T}}e[t]=c,e[t+1]=l,e[t+2]=d,e[t+3]=h}static multiplyQuaternionsFlat(e,t,i,r,a,s){const o=i[r],c=i[r+1],l=i[r+2],d=i[r+3],h=a[s],f=a[s+1],m=a[s+2],g=a[s+3];return e[t]=o*g+d*h+c*m-l*f,e[t+1]=c*g+d*f+l*h-o*m,e[t+2]=l*g+d*m+o*f-c*h,e[t+3]=d*g-o*h-c*f-l*m,e}get x(){return this._x}set x(e){this._x=e,this._onChangeCallback()}get y(){return this._y}set y(e){this._y=e,this._onChangeCallback()}get z(){return this._z}set z(e){this._z=e,this._onChangeCallback()}get w(){return this._w}set w(e){this._w=e,this._onChangeCallback()}set(e,t,i,r){return this._x=e,this._y=t,this._z=i,this._w=r,this._onChangeCallback(),this}clone(){return new this.constructor(this._x,this._y,this._z,this._w)}copy(e){return this._x=e.x,this._y=e.y,this._z=e.z,this._w=e.w,this._onChangeCallback(),this}setFromEuler(e,t=!0){const i=e._x,r=e._y,a=e._z,s=e._order,o=Math.cos,c=Math.sin,l=o(i/2),d=o(r/2),h=o(a/2),f=c(i/2),m=c(r/2),g=c(a/2);switch(s){case"XYZ":this._x=f*d*h+l*m*g,this._y=l*m*h-f*d*g,this._z=l*d*g+f*m*h,this._w=l*d*h-f*m*g;break;case"YXZ":this._x=f*d*h+l*m*g,this._y=l*m*h-f*d*g,this._z=l*d*g-f*m*h,this._w=l*d*h+f*m*g;break;case"ZXY":this._x=f*d*h-l*m*g,this._y=l*m*h+f*d*g,this._z=l*d*g+f*m*h,this._w=l*d*h-f*m*g;break;case"ZYX":this._x=f*d*h-l*m*g,this._y=l*m*h+f*d*g,this._z=l*d*g-f*m*h,this._w=l*d*h+f*m*g;break;case"YZX":this._x=f*d*h+l*m*g,this._y=l*m*h+f*d*g,this._z=l*d*g-f*m*h,this._w=l*d*h-f*m*g;break;case"XZY":this._x=f*d*h-l*m*g,this._y=l*m*h-f*d*g,this._z=l*d*g+f*m*h,this._w=l*d*h+f*m*g;break;default:console.warn("THREE.Quaternion: .setFromEuler() encountered an unknown order: "+s)}return t===!0&&this._onChangeCallback(),this}setFromAxisAngle(e,t){const i=t/2,r=Math.sin(i);return this._x=e.x*r,this._y=e.y*r,this._z=e.z*r,this._w=Math.cos(i),this._onChangeCallback(),this}setFromRotationMatrix(e){const t=e.elements,i=t[0],r=t[4],a=t[8],s=t[1],o=t[5],c=t[9],l=t[2],d=t[6],h=t[10],f=i+o+h;if(f>0){const m=.5/Math.sqrt(f+1);this._w=.25/m,this._x=(d-c)*m,this._y=(a-l)*m,this._z=(s-r)*m}else if(i>o&&i>h){const m=2*Math.sqrt(1+i-o-h);this._w=(d-c)/m,this._x=.25*m,this._y=(r+s)/m,this._z=(a+l)/m}else if(o>h){const m=2*Math.sqrt(1+o-i-h);this._w=(a-l)/m,this._x=(r+s)/m,this._y=.25*m,this._z=(c+d)/m}else{const m=2*Math.sqrt(1+h-i-o);this._w=(s-r)/m,this._x=(a+l)/m,this._y=(c+d)/m,this._z=.25*m}return this._onChangeCallback(),this}setFromUnitVectors(e,t){let i=e.dot(t)+1;return i<Number.EPSILON?(i=0,Math.abs(e.x)>Math.abs(e.z)?(this._x=-e.y,this._y=e.x,this._z=0,this._w=i):(this._x=0,this._y=-e.z,this._z=e.y,this._w=i)):(this._x=e.y*t.z-e.z*t.y,this._y=e.z*t.x-e.x*t.z,this._z=e.x*t.y-e.y*t.x,this._w=i),this.normalize()}angleTo(e){return 2*Math.acos(Math.abs(We(this.dot(e),-1,1)))}rotateTowards(e,t){const i=this.angleTo(e);if(i===0)return this;const r=Math.min(1,t/i);return this.slerp(e,r),this}identity(){return this.set(0,0,0,1)}invert(){return this.conjugate()}conjugate(){return this._x*=-1,this._y*=-1,this._z*=-1,this._onChangeCallback(),this}dot(e){return this._x*e._x+this._y*e._y+this._z*e._z+this._w*e._w}lengthSq(){return this._x*this._x+this._y*this._y+this._z*this._z+this._w*this._w}length(){return Math.sqrt(this._x*this._x+this._y*this._y+this._z*this._z+this._w*this._w)}normalize(){let e=this.length();return e===0?(this._x=0,this._y=0,this._z=0,this._w=1):(e=1/e,this._x=this._x*e,this._y=this._y*e,this._z=this._z*e,this._w=this._w*e),this._onChangeCallback(),this}multiply(e){return this.multiplyQuaternions(this,e)}premultiply(e){return this.multiplyQuaternions(e,this)}multiplyQuaternions(e,t){const i=e._x,r=e._y,a=e._z,s=e._w,o=t._x,c=t._y,l=t._z,d=t._w;return this._x=i*d+s*o+r*l-a*c,this._y=r*d+s*c+a*o-i*l,this._z=a*d+s*l+i*c-r*o,this._w=s*d-i*o-r*c-a*l,this._onChangeCallback(),this}slerp(e,t){if(t===0)return this;if(t===1)return this.copy(e);const i=this._x,r=this._y,a=this._z,s=this._w;let o=s*e._w+i*e._x+r*e._y+a*e._z;if(o<0?(this._w=-e._w,this._x=-e._x,this._y=-e._y,this._z=-e._z,o=-o):this.copy(e),o>=1)return this._w=s,this._x=i,this._y=r,this._z=a,this;const c=1-o*o;if(c<=Number.EPSILON){const m=1-t;return this._w=m*s+t*this._w,this._x=m*i+t*this._x,this._y=m*r+t*this._y,this._z=m*a+t*this._z,this.normalize(),this}const l=Math.sqrt(c),d=Math.atan2(l,o),h=Math.sin((1-t)*d)/l,f=Math.sin(t*d)/l;return this._w=s*h+this._w*f,this._x=i*h+this._x*f,this._y=r*h+this._y*f,this._z=a*h+this._z*f,this._onChangeCallback(),this}slerpQuaternions(e,t,i){return this.copy(e).slerp(t,i)}random(){const e=2*Math.PI*Math.random(),t=2*Math.PI*Math.random(),i=Math.random(),r=Math.sqrt(1-i),a=Math.sqrt(i);return this.set(r*Math.sin(e),r*Math.cos(e),a*Math.sin(t),a*Math.cos(t))}equals(e){return e._x===this._x&&e._y===this._y&&e._z===this._z&&e._w===this._w}fromArray(e,t=0){return this._x=e[t],this._y=e[t+1],this._z=e[t+2],this._w=e[t+3],this._onChangeCallback(),this}toArray(e=[],t=0){return e[t]=this._x,e[t+1]=this._y,e[t+2]=this._z,e[t+3]=this._w,e}fromBufferAttribute(e,t){return this._x=e.getX(t),this._y=e.getY(t),this._z=e.getZ(t),this._w=e.getW(t),this._onChangeCallback(),this}toJSON(){return this.toArray()}_onChange(e){return this._onChangeCallback=e,this}_onChangeCallback(){}*[Symbol.iterator](){yield this._x,yield this._y,yield this._z,yield this._w}}class k{constructor(e=0,t=0,i=0){k.prototype.isVector3=!0,this.x=e,this.y=t,this.z=i}set(e,t,i){return i===void 0&&(i=this.z),this.x=e,this.y=t,this.z=i,this}setScalar(e){return this.x=e,this.y=e,this.z=e,this}setX(e){return this.x=e,this}setY(e){return this.y=e,this}setZ(e){return this.z=e,this}setComponent(e,t){switch(e){case 0:this.x=t;break;case 1:this.y=t;break;case 2:this.z=t;break;default:throw new Error("index is out of range: "+e)}return this}getComponent(e){switch(e){case 0:return this.x;case 1:return this.y;case 2:return this.z;default:throw new Error("index is out of range: "+e)}}clone(){return new this.constructor(this.x,this.y,this.z)}copy(e){return this.x=e.x,this.y=e.y,this.z=e.z,this}add(e){return this.x+=e.x,this.y+=e.y,this.z+=e.z,this}addScalar(e){return this.x+=e,this.y+=e,this.z+=e,this}addVectors(e,t){return this.x=e.x+t.x,this.y=e.y+t.y,this.z=e.z+t.z,this}addScaledVector(e,t){return this.x+=e.x*t,this.y+=e.y*t,this.z+=e.z*t,this}sub(e){return this.x-=e.x,this.y-=e.y,this.z-=e.z,this}subScalar(e){return this.x-=e,this.y-=e,this.z-=e,this}subVectors(e,t){return this.x=e.x-t.x,this.y=e.y-t.y,this.z=e.z-t.z,this}multiply(e){return this.x*=e.x,this.y*=e.y,this.z*=e.z,this}multiplyScalar(e){return this.x*=e,this.y*=e,this.z*=e,this}multiplyVectors(e,t){return this.x=e.x*t.x,this.y=e.y*t.y,this.z=e.z*t.z,this}applyEuler(e){return this.applyQuaternion(oo.setFromEuler(e))}applyAxisAngle(e,t){return this.applyQuaternion(oo.setFromAxisAngle(e,t))}applyMatrix3(e){const t=this.x,i=this.y,r=this.z,a=e.elements;return this.x=a[0]*t+a[3]*i+a[6]*r,this.y=a[1]*t+a[4]*i+a[7]*r,this.z=a[2]*t+a[5]*i+a[8]*r,this}applyNormalMatrix(e){return this.applyMatrix3(e).normalize()}applyMatrix4(e){const t=this.x,i=this.y,r=this.z,a=e.elements,s=1/(a[3]*t+a[7]*i+a[11]*r+a[15]);return this.x=(a[0]*t+a[4]*i+a[8]*r+a[12])*s,this.y=(a[1]*t+a[5]*i+a[9]*r+a[13])*s,this.z=(a[2]*t+a[6]*i+a[10]*r+a[14])*s,this}applyQuaternion(e){const t=this.x,i=this.y,r=this.z,a=e.x,s=e.y,o=e.z,c=e.w,l=2*(s*r-o*i),d=2*(o*t-a*r),h=2*(a*i-s*t);return this.x=t+c*l+s*h-o*d,this.y=i+c*d+o*l-a*h,this.z=r+c*h+a*d-s*l,this}project(e){return this.applyMatrix4(e.matrixWorldInverse).applyMatrix4(e.projectionMatrix)}unproject(e){return this.applyMatrix4(e.projectionMatrixInverse).applyMatrix4(e.matrixWorld)}transformDirection(e){const t=this.x,i=this.y,r=this.z,a=e.elements;return this.x=a[0]*t+a[4]*i+a[8]*r,this.y=a[1]*t+a[5]*i+a[9]*r,this.z=a[2]*t+a[6]*i+a[10]*r,this.normalize()}divide(e){return this.x/=e.x,this.y/=e.y,this.z/=e.z,this}divideScalar(e){return this.multiplyScalar(1/e)}min(e){return this.x=Math.min(this.x,e.x),this.y=Math.min(this.y,e.y),this.z=Math.min(this.z,e.z),this}max(e){return this.x=Math.max(this.x,e.x),this.y=Math.max(this.y,e.y),this.z=Math.max(this.z,e.z),this}clamp(e,t){return this.x=We(this.x,e.x,t.x),this.y=We(this.y,e.y,t.y),this.z=We(this.z,e.z,t.z),this}clampScalar(e,t){return this.x=We(this.x,e,t),this.y=We(this.y,e,t),this.z=We(this.z,e,t),this}clampLength(e,t){const i=this.length();return this.divideScalar(i||1).multiplyScalar(We(i,e,t))}floor(){return this.x=Math.floor(this.x),this.y=Math.floor(this.y),this.z=Math.floor(this.z),this}ceil(){return this.x=Math.ceil(this.x),this.y=Math.ceil(this.y),this.z=Math.ceil(this.z),this}round(){return this.x=Math.round(this.x),this.y=Math.round(this.y),this.z=Math.round(this.z),this}roundToZero(){return this.x=Math.trunc(this.x),this.y=Math.trunc(this.y),this.z=Math.trunc(this.z),this}negate(){return this.x=-this.x,this.y=-this.y,this.z=-this.z,this}dot(e){return this.x*e.x+this.y*e.y+this.z*e.z}lengthSq(){return this.x*this.x+this.y*this.y+this.z*this.z}length(){return Math.sqrt(this.x*this.x+this.y*this.y+this.z*this.z)}manhattanLength(){return Math.abs(this.x)+Math.abs(this.y)+Math.abs(this.z)}normalize(){return this.divideScalar(this.length()||1)}setLength(e){return this.normalize().multiplyScalar(e)}lerp(e,t){return this.x+=(e.x-this.x)*t,this.y+=(e.y-this.y)*t,this.z+=(e.z-this.z)*t,this}lerpVectors(e,t,i){return this.x=e.x+(t.x-e.x)*i,this.y=e.y+(t.y-e.y)*i,this.z=e.z+(t.z-e.z)*i,this}cross(e){return this.crossVectors(this,e)}crossVectors(e,t){const i=e.x,r=e.y,a=e.z,s=t.x,o=t.y,c=t.z;return this.x=r*c-a*o,this.y=a*s-i*c,this.z=i*o-r*s,this}projectOnVector(e){const t=e.lengthSq();if(t===0)return this.set(0,0,0);const i=e.dot(this)/t;return this.copy(e).multiplyScalar(i)}projectOnPlane(e){return Zr.copy(this).projectOnVector(e),this.sub(Zr)}reflect(e){return this.sub(Zr.copy(e).multiplyScalar(2*this.dot(e)))}angleTo(e){const t=Math.sqrt(this.lengthSq()*e.lengthSq());if(t===0)return Math.PI/2;const i=this.dot(e)/t;return Math.acos(We(i,-1,1))}distanceTo(e){return Math.sqrt(this.distanceToSquared(e))}distanceToSquared(e){const t=this.x-e.x,i=this.y-e.y,r=this.z-e.z;return t*t+i*i+r*r}manhattanDistanceTo(e){return Math.abs(this.x-e.x)+Math.abs(this.y-e.y)+Math.abs(this.z-e.z)}setFromSpherical(e){return this.setFromSphericalCoords(e.radius,e.phi,e.theta)}setFromSphericalCoords(e,t,i){const r=Math.sin(t)*e;return this.x=r*Math.sin(i),this.y=Math.cos(t)*e,this.z=r*Math.cos(i),this}setFromCylindrical(e){return this.setFromCylindricalCoords(e.radius,e.theta,e.y)}setFromCylindricalCoords(e,t,i){return this.x=e*Math.sin(t),this.y=i,this.z=e*Math.cos(t),this}setFromMatrixPosition(e){const t=e.elements;return this.x=t[12],this.y=t[13],this.z=t[14],this}setFromMatrixScale(e){const t=this.setFromMatrixColumn(e,0).length(),i=this.setFromMatrixColumn(e,1).length(),r=this.setFromMatrixColumn(e,2).length();return this.x=t,this.y=i,this.z=r,this}setFromMatrixColumn(e,t){return this.fromArray(e.elements,t*4)}setFromMatrix3Column(e,t){return this.fromArray(e.elements,t*3)}setFromEuler(e){return this.x=e._x,this.y=e._y,this.z=e._z,this}setFromColor(e){return this.x=e.r,this.y=e.g,this.z=e.b,this}equals(e){return e.x===this.x&&e.y===this.y&&e.z===this.z}fromArray(e,t=0){return this.x=e[t],this.y=e[t+1],this.z=e[t+2],this}toArray(e=[],t=0){return e[t]=this.x,e[t+1]=this.y,e[t+2]=this.z,e}fromBufferAttribute(e,t){return this.x=e.getX(t),this.y=e.getY(t),this.z=e.getZ(t),this}random(){return this.x=Math.random(),this.y=Math.random(),this.z=Math.random(),this}randomDirection(){const e=Math.random()*Math.PI*2,t=Math.random()*2-1,i=Math.sqrt(1-t*t);return this.x=i*Math.cos(e),this.y=t,this.z=i*Math.sin(e),this}*[Symbol.iterator](){yield this.x,yield this.y,yield this.z}}const Zr=new k,oo=new Ki;class $i{constructor(e=new k(1/0,1/0,1/0),t=new k(-1/0,-1/0,-1/0)){this.isBox3=!0,this.min=e,this.max=t}set(e,t){return this.min.copy(e),this.max.copy(t),this}setFromArray(e){this.makeEmpty();for(let t=0,i=e.length;t<i;t+=3)this.expandByPoint(jt.fromArray(e,t));return this}setFromBufferAttribute(e){this.makeEmpty();for(let t=0,i=e.count;t<i;t++)this.expandByPoint(jt.fromBufferAttribute(e,t));return this}setFromPoints(e){this.makeEmpty();for(let t=0,i=e.length;t<i;t++)this.expandByPoint(e[t]);return this}setFromCenterAndSize(e,t){const i=jt.copy(t).multiplyScalar(.5);return this.min.copy(e).sub(i),this.max.copy(e).add(i),this}setFromObject(e,t=!1){return this.makeEmpty(),this.expandByObject(e,t)}clone(){return new this.constructor().copy(this)}copy(e){return this.min.copy(e.min),this.max.copy(e.max),this}makeEmpty(){return this.min.x=this.min.y=this.min.z=1/0,this.max.x=this.max.y=this.max.z=-1/0,this}isEmpty(){return this.max.x<this.min.x||this.max.y<this.min.y||this.max.z<this.min.z}getCenter(e){return this.isEmpty()?e.set(0,0,0):e.addVectors(this.min,this.max).multiplyScalar(.5)}getSize(e){return this.isEmpty()?e.set(0,0,0):e.subVectors(this.max,this.min)}expandByPoint(e){return this.min.min(e),this.max.max(e),this}expandByVector(e){return this.min.sub(e),this.max.add(e),this}expandByScalar(e){return this.min.addScalar(-e),this.max.addScalar(e),this}expandByObject(e,t=!1){e.updateWorldMatrix(!1,!1);const i=e.geometry;if(i!==void 0){const a=i.getAttribute("position");if(t===!0&&a!==void 0&&e.isInstancedMesh!==!0)for(let s=0,o=a.count;s<o;s++)e.isMesh===!0?e.getVertexPosition(s,jt):jt.fromBufferAttribute(a,s),jt.applyMatrix4(e.matrixWorld),this.expandByPoint(jt);else e.boundingBox!==void 0?(e.boundingBox===null&&e.computeBoundingBox(),tr.copy(e.boundingBox)):(i.boundingBox===null&&i.computeBoundingBox(),tr.copy(i.boundingBox)),tr.applyMatrix4(e.matrixWorld),this.union(tr)}const r=e.children;for(let a=0,s=r.length;a<s;a++)this.expandByObject(r[a],t);return this}containsPoint(e){return e.x>=this.min.x&&e.x<=this.max.x&&e.y>=this.min.y&&e.y<=this.max.y&&e.z>=this.min.z&&e.z<=this.max.z}containsBox(e){return this.min.x<=e.min.x&&e.max.x<=this.max.x&&this.min.y<=e.min.y&&e.max.y<=this.max.y&&this.min.z<=e.min.z&&e.max.z<=this.max.z}getParameter(e,t){return t.set((e.x-this.min.x)/(this.max.x-this.min.x),(e.y-this.min.y)/(this.max.y-this.min.y),(e.z-this.min.z)/(this.max.z-this.min.z))}intersectsBox(e){return e.max.x>=this.min.x&&e.min.x<=this.max.x&&e.max.y>=this.min.y&&e.min.y<=this.max.y&&e.max.z>=this.min.z&&e.min.z<=this.max.z}intersectsSphere(e){return this.clampPoint(e.center,jt),jt.distanceToSquared(e.center)<=e.radius*e.radius}intersectsPlane(e){let t,i;return e.normal.x>0?(t=e.normal.x*this.min.x,i=e.normal.x*this.max.x):(t=e.normal.x*this.max.x,i=e.normal.x*this.min.x),e.normal.y>0?(t+=e.normal.y*this.min.y,i+=e.normal.y*this.max.y):(t+=e.normal.y*this.max.y,i+=e.normal.y*this.min.y),e.normal.z>0?(t+=e.normal.z*this.min.z,i+=e.normal.z*this.max.z):(t+=e.normal.z*this.max.z,i+=e.normal.z*this.min.z),t<=-e.constant&&i>=-e.constant}intersectsTriangle(e){if(this.isEmpty())return!1;this.getCenter(Ni),nr.subVectors(this.max,Ni),ni.subVectors(e.a,Ni),ii.subVectors(e.b,Ni),ri.subVectors(e.c,Ni),gn.subVectors(ii,ni),_n.subVectors(ri,ii),Un.subVectors(ni,ri);let t=[0,-gn.z,gn.y,0,-_n.z,_n.y,0,-Un.z,Un.y,gn.z,0,-gn.x,_n.z,0,-_n.x,Un.z,0,-Un.x,-gn.y,gn.x,0,-_n.y,_n.x,0,-Un.y,Un.x,0];return!Jr(t,ni,ii,ri,nr)||(t=[1,0,0,0,1,0,0,0,1],!Jr(t,ni,ii,ri,nr))?!1:(ir.crossVectors(gn,_n),t=[ir.x,ir.y,ir.z],Jr(t,ni,ii,ri,nr))}clampPoint(e,t){return t.copy(e).clamp(this.min,this.max)}distanceToPoint(e){return this.clampPoint(e,jt).distanceTo(e)}getBoundingSphere(e){return this.isEmpty()?e.makeEmpty():(this.getCenter(e.center),e.radius=this.getSize(jt).length()*.5),e}intersect(e){return this.min.max(e.min),this.max.min(e.max),this.isEmpty()&&this.makeEmpty(),this}union(e){return this.min.min(e.min),this.max.max(e.max),this}applyMatrix4(e){return this.isEmpty()?this:(en[0].set(this.min.x,this.min.y,this.min.z).applyMatrix4(e),en[1].set(this.min.x,this.min.y,this.max.z).applyMatrix4(e),en[2].set(this.min.x,this.max.y,this.min.z).applyMatrix4(e),en[3].set(this.min.x,this.max.y,this.max.z).applyMatrix4(e),en[4].set(this.max.x,this.min.y,this.min.z).applyMatrix4(e),en[5].set(this.max.x,this.min.y,this.max.z).applyMatrix4(e),en[6].set(this.max.x,this.max.y,this.min.z).applyMatrix4(e),en[7].set(this.max.x,this.max.y,this.max.z).applyMatrix4(e),this.setFromPoints(en),this)}translate(e){return this.min.add(e),this.max.add(e),this}equals(e){return e.min.equals(this.min)&&e.max.equals(this.max)}}const en=[new k,new k,new k,new k,new k,new k,new k,new k],jt=new k,tr=new $i,ni=new k,ii=new k,ri=new k,gn=new k,_n=new k,Un=new k,Ni=new k,nr=new k,ir=new k,zn=new k;function Jr(n,e,t,i,r){for(let a=0,s=n.length-3;a<=s;a+=3){zn.fromArray(n,a);const o=r.x*Math.abs(zn.x)+r.y*Math.abs(zn.y)+r.z*Math.abs(zn.z),c=e.dot(zn),l=t.dot(zn),d=i.dot(zn);if(Math.max(-Math.max(c,l,d),Math.min(c,l,d))>o)return!1}return!0}const Ql=new $i,Fi=new k,Qr=new k;class Hr{constructor(e=new k,t=-1){this.isSphere=!0,this.center=e,this.radius=t}set(e,t){return this.center.copy(e),this.radius=t,this}setFromPoints(e,t){const i=this.center;t!==void 0?i.copy(t):Ql.setFromPoints(e).getCenter(i);let r=0;for(let a=0,s=e.length;a<s;a++)r=Math.max(r,i.distanceToSquared(e[a]));return this.radius=Math.sqrt(r),this}copy(e){return this.center.copy(e.center),this.radius=e.radius,this}isEmpty(){return this.radius<0}makeEmpty(){return this.center.set(0,0,0),this.radius=-1,this}containsPoint(e){return e.distanceToSquared(this.center)<=this.radius*this.radius}distanceToPoint(e){return e.distanceTo(this.center)-this.radius}intersectsSphere(e){const t=this.radius+e.radius;return e.center.distanceToSquared(this.center)<=t*t}intersectsBox(e){return e.intersectsSphere(this)}intersectsPlane(e){return Math.abs(e.distanceToPoint(this.center))<=this.radius}clampPoint(e,t){const i=this.center.distanceToSquared(e);return t.copy(e),i>this.radius*this.radius&&(t.sub(this.center).normalize(),t.multiplyScalar(this.radius).add(this.center)),t}getBoundingBox(e){return this.isEmpty()?(e.makeEmpty(),e):(e.set(this.center,this.center),e.expandByScalar(this.radius),e)}applyMatrix4(e){return this.center.applyMatrix4(e),this.radius=this.radius*e.getMaxScaleOnAxis(),this}translate(e){return this.center.add(e),this}expandByPoint(e){if(this.isEmpty())return this.center.copy(e),this.radius=0,this;Fi.subVectors(e,this.center);const t=Fi.lengthSq();if(t>this.radius*this.radius){const i=Math.sqrt(t),r=(i-this.radius)*.5;this.center.addScaledVector(Fi,r/i),this.radius+=r}return this}union(e){return e.isEmpty()?this:this.isEmpty()?(this.copy(e),this):(this.center.equals(e.center)===!0?this.radius=Math.max(this.radius,e.radius):(Qr.subVectors(e.center,this.center).setLength(e.radius),this.expandByPoint(Fi.copy(e.center).add(Qr)),this.expandByPoint(Fi.copy(e.center).sub(Qr))),this)}equals(e){return e.center.equals(this.center)&&e.radius===this.radius}clone(){return new this.constructor().copy(this)}}const tn=new k,ea=new k,rr=new k,vn=new k,ta=new k,ar=new k,na=new k;class Ds{constructor(e=new k,t=new k(0,0,-1)){this.origin=e,this.direction=t}set(e,t){return this.origin.copy(e),this.direction.copy(t),this}copy(e){return this.origin.copy(e.origin),this.direction.copy(e.direction),this}at(e,t){return t.copy(this.origin).addScaledVector(this.direction,e)}lookAt(e){return this.direction.copy(e).sub(this.origin).normalize(),this}recast(e){return this.origin.copy(this.at(e,tn)),this}closestPointToPoint(e,t){t.subVectors(e,this.origin);const i=t.dot(this.direction);return i<0?t.copy(this.origin):t.copy(this.origin).addScaledVector(this.direction,i)}distanceToPoint(e){return Math.sqrt(this.distanceSqToPoint(e))}distanceSqToPoint(e){const t=tn.subVectors(e,this.origin).dot(this.direction);return t<0?this.origin.distanceToSquared(e):(tn.copy(this.origin).addScaledVector(this.direction,t),tn.distanceToSquared(e))}distanceSqToSegment(e,t,i,r){ea.copy(e).add(t).multiplyScalar(.5),rr.copy(t).sub(e).normalize(),vn.copy(this.origin).sub(ea);const a=e.distanceTo(t)*.5,s=-this.direction.dot(rr),o=vn.dot(this.direction),c=-vn.dot(rr),l=vn.lengthSq(),d=Math.abs(1-s*s);let h,f,m,g;if(d>0)if(h=s*c-o,f=s*o-c,g=a*d,h>=0)if(f>=-g)if(f<=g){const _=1/d;h*=_,f*=_,m=h*(h+s*f+2*o)+f*(s*h+f+2*c)+l}else f=a,h=Math.max(0,-(s*f+o)),m=-h*h+f*(f+2*c)+l;else f=-a,h=Math.max(0,-(s*f+o)),m=-h*h+f*(f+2*c)+l;else f<=-g?(h=Math.max(0,-(-s*a+o)),f=h>0?-a:Math.min(Math.max(-a,-c),a),m=-h*h+f*(f+2*c)+l):f<=g?(h=0,f=Math.min(Math.max(-a,-c),a),m=f*(f+2*c)+l):(h=Math.max(0,-(s*a+o)),f=h>0?a:Math.min(Math.max(-a,-c),a),m=-h*h+f*(f+2*c)+l);else f=s>0?-a:a,h=Math.max(0,-(s*f+o)),m=-h*h+f*(f+2*c)+l;return i&&i.copy(this.origin).addScaledVector(this.direction,h),r&&r.copy(ea).addScaledVector(rr,f),m}intersectSphere(e,t){tn.subVectors(e.center,this.origin);const i=tn.dot(this.direction),r=tn.dot(tn)-i*i,a=e.radius*e.radius;if(r>a)return null;const s=Math.sqrt(a-r),o=i-s,c=i+s;return c<0?null:o<0?this.at(c,t):this.at(o,t)}intersectsSphere(e){return this.distanceSqToPoint(e.center)<=e.radius*e.radius}distanceToPlane(e){const t=e.normal.dot(this.direction);if(t===0)return e.distanceToPoint(this.origin)===0?0:null;const i=-(this.origin.dot(e.normal)+e.constant)/t;return i>=0?i:null}intersectPlane(e,t){const i=this.distanceToPlane(e);return i===null?null:this.at(i,t)}intersectsPlane(e){const t=e.distanceToPoint(this.origin);return t===0||e.normal.dot(this.direction)*t<0}intersectBox(e,t){let i,r,a,s,o,c;const l=1/this.direction.x,d=1/this.direction.y,h=1/this.direction.z,f=this.origin;return l>=0?(i=(e.min.x-f.x)*l,r=(e.max.x-f.x)*l):(i=(e.max.x-f.x)*l,r=(e.min.x-f.x)*l),d>=0?(a=(e.min.y-f.y)*d,s=(e.max.y-f.y)*d):(a=(e.max.y-f.y)*d,s=(e.min.y-f.y)*d),i>s||a>r||((a>i||isNaN(i))&&(i=a),(s<r||isNaN(r))&&(r=s),h>=0?(o=(e.min.z-f.z)*h,c=(e.max.z-f.z)*h):(o=(e.max.z-f.z)*h,c=(e.min.z-f.z)*h),i>c||o>r)||((o>i||i!==i)&&(i=o),(c<r||r!==r)&&(r=c),r<0)?null:this.at(i>=0?i:r,t)}intersectsBox(e){return this.intersectBox(e,tn)!==null}intersectTriangle(e,t,i,r,a){ta.subVectors(t,e),ar.subVectors(i,e),na.crossVectors(ta,ar);let s=this.direction.dot(na),o;if(s>0){if(r)return null;o=1}else if(s<0)o=-1,s=-s;else return null;vn.subVectors(this.origin,e);const c=o*this.direction.dot(ar.crossVectors(vn,ar));if(c<0)return null;const l=o*this.direction.dot(ta.cross(vn));if(l<0||c+l>s)return null;const d=-o*vn.dot(na);return d<0?null:this.at(d/s,a)}applyMatrix4(e){return this.origin.applyMatrix4(e),this.direction.transformDirection(e),this}equals(e){return e.origin.equals(this.origin)&&e.direction.equals(this.direction)}clone(){return new this.constructor().copy(this)}}class at{constructor(e,t,i,r,a,s,o,c,l,d,h,f,m,g,_,p){at.prototype.isMatrix4=!0,this.elements=[1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1],e!==void 0&&this.set(e,t,i,r,a,s,o,c,l,d,h,f,m,g,_,p)}set(e,t,i,r,a,s,o,c,l,d,h,f,m,g,_,p){const u=this.elements;return u[0]=e,u[4]=t,u[8]=i,u[12]=r,u[1]=a,u[5]=s,u[9]=o,u[13]=c,u[2]=l,u[6]=d,u[10]=h,u[14]=f,u[3]=m,u[7]=g,u[11]=_,u[15]=p,this}identity(){return this.set(1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1),this}clone(){return new at().fromArray(this.elements)}copy(e){const t=this.elements,i=e.elements;return t[0]=i[0],t[1]=i[1],t[2]=i[2],t[3]=i[3],t[4]=i[4],t[5]=i[5],t[6]=i[6],t[7]=i[7],t[8]=i[8],t[9]=i[9],t[10]=i[10],t[11]=i[11],t[12]=i[12],t[13]=i[13],t[14]=i[14],t[15]=i[15],this}copyPosition(e){const t=this.elements,i=e.elements;return t[12]=i[12],t[13]=i[13],t[14]=i[14],this}setFromMatrix3(e){const t=e.elements;return this.set(t[0],t[3],t[6],0,t[1],t[4],t[7],0,t[2],t[5],t[8],0,0,0,0,1),this}extractBasis(e,t,i){return e.setFromMatrixColumn(this,0),t.setFromMatrixColumn(this,1),i.setFromMatrixColumn(this,2),this}makeBasis(e,t,i){return this.set(e.x,t.x,i.x,0,e.y,t.y,i.y,0,e.z,t.z,i.z,0,0,0,0,1),this}extractRotation(e){const t=this.elements,i=e.elements,r=1/ai.setFromMatrixColumn(e,0).length(),a=1/ai.setFromMatrixColumn(e,1).length(),s=1/ai.setFromMatrixColumn(e,2).length();return t[0]=i[0]*r,t[1]=i[1]*r,t[2]=i[2]*r,t[3]=0,t[4]=i[4]*a,t[5]=i[5]*a,t[6]=i[6]*a,t[7]=0,t[8]=i[8]*s,t[9]=i[9]*s,t[10]=i[10]*s,t[11]=0,t[12]=0,t[13]=0,t[14]=0,t[15]=1,this}makeRotationFromEuler(e){const t=this.elements,i=e.x,r=e.y,a=e.z,s=Math.cos(i),o=Math.sin(i),c=Math.cos(r),l=Math.sin(r),d=Math.cos(a),h=Math.sin(a);if(e.order==="XYZ"){const f=s*d,m=s*h,g=o*d,_=o*h;t[0]=c*d,t[4]=-c*h,t[8]=l,t[1]=m+g*l,t[5]=f-_*l,t[9]=-o*c,t[2]=_-f*l,t[6]=g+m*l,t[10]=s*c}else if(e.order==="YXZ"){const f=c*d,m=c*h,g=l*d,_=l*h;t[0]=f+_*o,t[4]=g*o-m,t[8]=s*l,t[1]=s*h,t[5]=s*d,t[9]=-o,t[2]=m*o-g,t[6]=_+f*o,t[10]=s*c}else if(e.order==="ZXY"){const f=c*d,m=c*h,g=l*d,_=l*h;t[0]=f-_*o,t[4]=-s*h,t[8]=g+m*o,t[1]=m+g*o,t[5]=s*d,t[9]=_-f*o,t[2]=-s*l,t[6]=o,t[10]=s*c}else if(e.order==="ZYX"){const f=s*d,m=s*h,g=o*d,_=o*h;t[0]=c*d,t[4]=g*l-m,t[8]=f*l+_,t[1]=c*h,t[5]=_*l+f,t[9]=m*l-g,t[2]=-l,t[6]=o*c,t[10]=s*c}else if(e.order==="YZX"){const f=s*c,m=s*l,g=o*c,_=o*l;t[0]=c*d,t[4]=_-f*h,t[8]=g*h+m,t[1]=h,t[5]=s*d,t[9]=-o*d,t[2]=-l*d,t[6]=m*h+g,t[10]=f-_*h}else if(e.order==="XZY"){const f=s*c,m=s*l,g=o*c,_=o*l;t[0]=c*d,t[4]=-h,t[8]=l*d,t[1]=f*h+_,t[5]=s*d,t[9]=m*h-g,t[2]=g*h-m,t[6]=o*d,t[10]=_*h+f}return t[3]=0,t[7]=0,t[11]=0,t[12]=0,t[13]=0,t[14]=0,t[15]=1,this}makeRotationFromQuaternion(e){return this.compose(eu,e,tu)}lookAt(e,t,i){const r=this.elements;return Ut.subVectors(e,t),Ut.lengthSq()===0&&(Ut.z=1),Ut.normalize(),xn.crossVectors(i,Ut),xn.lengthSq()===0&&(Math.abs(i.z)===1?Ut.x+=1e-4:Ut.z+=1e-4,Ut.normalize(),xn.crossVectors(i,Ut)),xn.normalize(),sr.crossVectors(Ut,xn),r[0]=xn.x,r[4]=sr.x,r[8]=Ut.x,r[1]=xn.y,r[5]=sr.y,r[9]=Ut.y,r[2]=xn.z,r[6]=sr.z,r[10]=Ut.z,this}multiply(e){return this.multiplyMatrices(this,e)}premultiply(e){return this.multiplyMatrices(e,this)}multiplyMatrices(e,t){const i=e.elements,r=t.elements,a=this.elements,s=i[0],o=i[4],c=i[8],l=i[12],d=i[1],h=i[5],f=i[9],m=i[13],g=i[2],_=i[6],p=i[10],u=i[14],y=i[3],S=i[7],M=i[11],T=i[15],b=r[0],w=r[4],L=r[8],x=r[12],v=r[1],R=r[5],U=r[9],C=r[13],P=r[2],F=r[6],N=r[10],O=r[14],z=r[3],G=r[7],K=r[11],$=r[15];return a[0]=s*b+o*v+c*P+l*z,a[4]=s*w+o*R+c*F+l*G,a[8]=s*L+o*U+c*N+l*K,a[12]=s*x+o*C+c*O+l*$,a[1]=d*b+h*v+f*P+m*z,a[5]=d*w+h*R+f*F+m*G,a[9]=d*L+h*U+f*N+m*K,a[13]=d*x+h*C+f*O+m*$,a[2]=g*b+_*v+p*P+u*z,a[6]=g*w+_*R+p*F+u*G,a[10]=g*L+_*U+p*N+u*K,a[14]=g*x+_*C+p*O+u*$,a[3]=y*b+S*v+M*P+T*z,a[7]=y*w+S*R+M*F+T*G,a[11]=y*L+S*U+M*N+T*K,a[15]=y*x+S*C+M*O+T*$,this}multiplyScalar(e){const t=this.elements;return t[0]*=e,t[4]*=e,t[8]*=e,t[12]*=e,t[1]*=e,t[5]*=e,t[9]*=e,t[13]*=e,t[2]*=e,t[6]*=e,t[10]*=e,t[14]*=e,t[3]*=e,t[7]*=e,t[11]*=e,t[15]*=e,this}determinant(){const e=this.elements,t=e[0],i=e[4],r=e[8],a=e[12],s=e[1],o=e[5],c=e[9],l=e[13],d=e[2],h=e[6],f=e[10],m=e[14],g=e[3],_=e[7],p=e[11],u=e[15];return g*(+a*c*h-r*l*h-a*o*f+i*l*f+r*o*m-i*c*m)+_*(+t*c*m-t*l*f+a*s*f-r*s*m+r*l*d-a*c*d)+p*(+t*l*h-t*o*m-a*s*h+i*s*m+a*o*d-i*l*d)+u*(-r*o*d-t*c*h+t*o*f+r*s*h-i*s*f+i*c*d)}transpose(){const e=this.elements;let t;return t=e[1],e[1]=e[4],e[4]=t,t=e[2],e[2]=e[8],e[8]=t,t=e[6],e[6]=e[9],e[9]=t,t=e[3],e[3]=e[12],e[12]=t,t=e[7],e[7]=e[13],e[13]=t,t=e[11],e[11]=e[14],e[14]=t,this}setPosition(e,t,i){const r=this.elements;return e.isVector3?(r[12]=e.x,r[13]=e.y,r[14]=e.z):(r[12]=e,r[13]=t,r[14]=i),this}invert(){const e=this.elements,t=e[0],i=e[1],r=e[2],a=e[3],s=e[4],o=e[5],c=e[6],l=e[7],d=e[8],h=e[9],f=e[10],m=e[11],g=e[12],_=e[13],p=e[14],u=e[15],y=h*p*l-_*f*l+_*c*m-o*p*m-h*c*u+o*f*u,S=g*f*l-d*p*l-g*c*m+s*p*m+d*c*u-s*f*u,M=d*_*l-g*h*l+g*o*m-s*_*m-d*o*u+s*h*u,T=g*h*c-d*_*c-g*o*f+s*_*f+d*o*p-s*h*p,b=t*y+i*S+r*M+a*T;if(b===0)return this.set(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);const w=1/b;return e[0]=y*w,e[1]=(_*f*a-h*p*a-_*r*m+i*p*m+h*r*u-i*f*u)*w,e[2]=(o*p*a-_*c*a+_*r*l-i*p*l-o*r*u+i*c*u)*w,e[3]=(h*c*a-o*f*a-h*r*l+i*f*l+o*r*m-i*c*m)*w,e[4]=S*w,e[5]=(d*p*a-g*f*a+g*r*m-t*p*m-d*r*u+t*f*u)*w,e[6]=(g*c*a-s*p*a-g*r*l+t*p*l+s*r*u-t*c*u)*w,e[7]=(s*f*a-d*c*a+d*r*l-t*f*l-s*r*m+t*c*m)*w,e[8]=M*w,e[9]=(g*h*a-d*_*a-g*i*m+t*_*m+d*i*u-t*h*u)*w,e[10]=(s*_*a-g*o*a+g*i*l-t*_*l-s*i*u+t*o*u)*w,e[11]=(d*o*a-s*h*a-d*i*l+t*h*l+s*i*m-t*o*m)*w,e[12]=T*w,e[13]=(d*_*r-g*h*r+g*i*f-t*_*f-d*i*p+t*h*p)*w,e[14]=(g*o*r-s*_*r-g*i*c+t*_*c+s*i*p-t*o*p)*w,e[15]=(s*h*r-d*o*r+d*i*c-t*h*c-s*i*f+t*o*f)*w,this}scale(e){const t=this.elements,i=e.x,r=e.y,a=e.z;return t[0]*=i,t[4]*=r,t[8]*=a,t[1]*=i,t[5]*=r,t[9]*=a,t[2]*=i,t[6]*=r,t[10]*=a,t[3]*=i,t[7]*=r,t[11]*=a,this}getMaxScaleOnAxis(){const e=this.elements,t=e[0]*e[0]+e[1]*e[1]+e[2]*e[2],i=e[4]*e[4]+e[5]*e[5]+e[6]*e[6],r=e[8]*e[8]+e[9]*e[9]+e[10]*e[10];return Math.sqrt(Math.max(t,i,r))}makeTranslation(e,t,i){return e.isVector3?this.set(1,0,0,e.x,0,1,0,e.y,0,0,1,e.z,0,0,0,1):this.set(1,0,0,e,0,1,0,t,0,0,1,i,0,0,0,1),this}makeRotationX(e){const t=Math.cos(e),i=Math.sin(e);return this.set(1,0,0,0,0,t,-i,0,0,i,t,0,0,0,0,1),this}makeRotationY(e){const t=Math.cos(e),i=Math.sin(e);return this.set(t,0,i,0,0,1,0,0,-i,0,t,0,0,0,0,1),this}makeRotationZ(e){const t=Math.cos(e),i=Math.sin(e);return this.set(t,-i,0,0,i,t,0,0,0,0,1,0,0,0,0,1),this}makeRotationAxis(e,t){const i=Math.cos(t),r=Math.sin(t),a=1-i,s=e.x,o=e.y,c=e.z,l=a*s,d=a*o;return this.set(l*s+i,l*o-r*c,l*c+r*o,0,l*o+r*c,d*o+i,d*c-r*s,0,l*c-r*o,d*c+r*s,a*c*c+i,0,0,0,0,1),this}makeScale(e,t,i){return this.set(e,0,0,0,0,t,0,0,0,0,i,0,0,0,0,1),this}makeShear(e,t,i,r,a,s){return this.set(1,i,a,0,e,1,s,0,t,r,1,0,0,0,0,1),this}compose(e,t,i){const r=this.elements,a=t._x,s=t._y,o=t._z,c=t._w,l=a+a,d=s+s,h=o+o,f=a*l,m=a*d,g=a*h,_=s*d,p=s*h,u=o*h,y=c*l,S=c*d,M=c*h,T=i.x,b=i.y,w=i.z;return r[0]=(1-(_+u))*T,r[1]=(m+M)*T,r[2]=(g-S)*T,r[3]=0,r[4]=(m-M)*b,r[5]=(1-(f+u))*b,r[6]=(p+y)*b,r[7]=0,r[8]=(g+S)*w,r[9]=(p-y)*w,r[10]=(1-(f+_))*w,r[11]=0,r[12]=e.x,r[13]=e.y,r[14]=e.z,r[15]=1,this}decompose(e,t,i){const r=this.elements;let a=ai.set(r[0],r[1],r[2]).length();const s=ai.set(r[4],r[5],r[6]).length(),o=ai.set(r[8],r[9],r[10]).length();this.determinant()<0&&(a=-a),e.x=r[12],e.y=r[13],e.z=r[14],Wt.copy(this);const l=1/a,d=1/s,h=1/o;return Wt.elements[0]*=l,Wt.elements[1]*=l,Wt.elements[2]*=l,Wt.elements[4]*=d,Wt.elements[5]*=d,Wt.elements[6]*=d,Wt.elements[8]*=h,Wt.elements[9]*=h,Wt.elements[10]*=h,t.setFromRotationMatrix(Wt),i.x=a,i.y=s,i.z=o,this}makePerspective(e,t,i,r,a,s,o=dn){const c=this.elements,l=2*a/(t-e),d=2*a/(i-r),h=(t+e)/(t-e),f=(i+r)/(i-r);let m,g;if(o===dn)m=-(s+a)/(s-a),g=-2*s*a/(s-a);else if(o===Nr)m=-s/(s-a),g=-s*a/(s-a);else throw new Error("THREE.Matrix4.makePerspective(): Invalid coordinate system: "+o);return c[0]=l,c[4]=0,c[8]=h,c[12]=0,c[1]=0,c[5]=d,c[9]=f,c[13]=0,c[2]=0,c[6]=0,c[10]=m,c[14]=g,c[3]=0,c[7]=0,c[11]=-1,c[15]=0,this}makeOrthographic(e,t,i,r,a,s,o=dn){const c=this.elements,l=1/(t-e),d=1/(i-r),h=1/(s-a),f=(t+e)*l,m=(i+r)*d;let g,_;if(o===dn)g=(s+a)*h,_=-2*h;else if(o===Nr)g=a*h,_=-1*h;else throw new Error("THREE.Matrix4.makeOrthographic(): Invalid coordinate system: "+o);return c[0]=2*l,c[4]=0,c[8]=0,c[12]=-f,c[1]=0,c[5]=2*d,c[9]=0,c[13]=-m,c[2]=0,c[6]=0,c[10]=_,c[14]=-g,c[3]=0,c[7]=0,c[11]=0,c[15]=1,this}equals(e){const t=this.elements,i=e.elements;for(let r=0;r<16;r++)if(t[r]!==i[r])return!1;return!0}fromArray(e,t=0){for(let i=0;i<16;i++)this.elements[i]=e[i+t];return this}toArray(e=[],t=0){const i=this.elements;return e[t]=i[0],e[t+1]=i[1],e[t+2]=i[2],e[t+3]=i[3],e[t+4]=i[4],e[t+5]=i[5],e[t+6]=i[6],e[t+7]=i[7],e[t+8]=i[8],e[t+9]=i[9],e[t+10]=i[10],e[t+11]=i[11],e[t+12]=i[12],e[t+13]=i[13],e[t+14]=i[14],e[t+15]=i[15],e}}const ai=new k,Wt=new at,eu=new k(0,0,0),tu=new k(1,1,1),xn=new k,sr=new k,Ut=new k,co=new at,lo=new Ki;class Mt{constructor(e=0,t=0,i=0,r=Mt.DEFAULT_ORDER){this.isEuler=!0,this._x=e,this._y=t,this._z=i,this._order=r}get x(){return this._x}set x(e){this._x=e,this._onChangeCallback()}get y(){return this._y}set y(e){this._y=e,this._onChangeCallback()}get z(){return this._z}set z(e){this._z=e,this._onChangeCallback()}get order(){return this._order}set order(e){this._order=e,this._onChangeCallback()}set(e,t,i,r=this._order){return this._x=e,this._y=t,this._z=i,this._order=r,this._onChangeCallback(),this}clone(){return new this.constructor(this._x,this._y,this._z,this._order)}copy(e){return this._x=e._x,this._y=e._y,this._z=e._z,this._order=e._order,this._onChangeCallback(),this}setFromRotationMatrix(e,t=this._order,i=!0){const r=e.elements,a=r[0],s=r[4],o=r[8],c=r[1],l=r[5],d=r[9],h=r[2],f=r[6],m=r[10];switch(t){case"XYZ":this._y=Math.asin(We(o,-1,1)),Math.abs(o)<.9999999?(this._x=Math.atan2(-d,m),this._z=Math.atan2(-s,a)):(this._x=Math.atan2(f,l),this._z=0);break;case"YXZ":this._x=Math.asin(-We(d,-1,1)),Math.abs(d)<.9999999?(this._y=Math.atan2(o,m),this._z=Math.atan2(c,l)):(this._y=Math.atan2(-h,a),this._z=0);break;case"ZXY":this._x=Math.asin(We(f,-1,1)),Math.abs(f)<.9999999?(this._y=Math.atan2(-h,m),this._z=Math.atan2(-s,l)):(this._y=0,this._z=Math.atan2(c,a));break;case"ZYX":this._y=Math.asin(-We(h,-1,1)),Math.abs(h)<.9999999?(this._x=Math.atan2(f,m),this._z=Math.atan2(c,a)):(this._x=0,this._z=Math.atan2(-s,l));break;case"YZX":this._z=Math.asin(We(c,-1,1)),Math.abs(c)<.9999999?(this._x=Math.atan2(-d,l),this._y=Math.atan2(-h,a)):(this._x=0,this._y=Math.atan2(o,m));break;case"XZY":this._z=Math.asin(-We(s,-1,1)),Math.abs(s)<.9999999?(this._x=Math.atan2(f,l),this._y=Math.atan2(o,a)):(this._x=Math.atan2(-d,m),this._y=0);break;default:console.warn("THREE.Euler: .setFromRotationMatrix() encountered an unknown order: "+t)}return this._order=t,i===!0&&this._onChangeCallback(),this}setFromQuaternion(e,t,i){return co.makeRotationFromQuaternion(e),this.setFromRotationMatrix(co,t,i)}setFromVector3(e,t=this._order){return this.set(e.x,e.y,e.z,t)}reorder(e){return lo.setFromEuler(this),this.setFromQuaternion(lo,e)}equals(e){return e._x===this._x&&e._y===this._y&&e._z===this._z&&e._order===this._order}fromArray(e){return this._x=e[0],this._y=e[1],this._z=e[2],e[3]!==void 0&&(this._order=e[3]),this._onChangeCallback(),this}toArray(e=[],t=0){return e[t]=this._x,e[t+1]=this._y,e[t+2]=this._z,e[t+3]=this._order,e}_onChange(e){return this._onChangeCallback=e,this}_onChangeCallback(){}*[Symbol.iterator](){yield this._x,yield this._y,yield this._z,yield this._order}}Mt.DEFAULT_ORDER="XYZ";class Ls{constructor(){this.mask=1}set(e){this.mask=(1<<e|0)>>>0}enable(e){this.mask|=1<<e|0}enableAll(){this.mask=-1}toggle(e){this.mask^=1<<e|0}disable(e){this.mask&=~(1<<e|0)}disableAll(){this.mask=0}test(e){return(this.mask&e.mask)!==0}isEnabled(e){return(this.mask&(1<<e|0))!==0}}let nu=0;const uo=new k,si=new Ki,nn=new at,or=new k,ki=new k,iu=new k,ru=new Ki,ho=new k(1,0,0),fo=new k(0,1,0),po=new k(0,0,1),mo={type:"added"},au={type:"removed"},oi={type:"childadded",child:null},ia={type:"childremoved",child:null};class Et extends Ci{constructor(){super(),this.isObject3D=!0,Object.defineProperty(this,"id",{value:nu++}),this.uuid=Yi(),this.name="",this.type="Object3D",this.parent=null,this.children=[],this.up=Et.DEFAULT_UP.clone();const e=new k,t=new Mt,i=new Ki,r=new k(1,1,1);function a(){i.setFromEuler(t,!1)}function s(){t.setFromQuaternion(i,void 0,!1)}t._onChange(a),i._onChange(s),Object.defineProperties(this,{position:{configurable:!0,enumerable:!0,value:e},rotation:{configurable:!0,enumerable:!0,value:t},quaternion:{configurable:!0,enumerable:!0,value:i},scale:{configurable:!0,enumerable:!0,value:r},modelViewMatrix:{value:new at},normalMatrix:{value:new Be}}),this.matrix=new at,this.matrixWorld=new at,this.matrixAutoUpdate=Et.DEFAULT_MATRIX_AUTO_UPDATE,this.matrixWorldAutoUpdate=Et.DEFAULT_MATRIX_WORLD_AUTO_UPDATE,this.matrixWorldNeedsUpdate=!1,this.layers=new Ls,this.visible=!0,this.castShadow=!1,this.receiveShadow=!1,this.frustumCulled=!0,this.renderOrder=0,this.animations=[],this.userData={}}onBeforeShadow(){}onAfterShadow(){}onBeforeRender(){}onAfterRender(){}applyMatrix4(e){this.matrixAutoUpdate&&this.updateMatrix(),this.matrix.premultiply(e),this.matrix.decompose(this.position,this.quaternion,this.scale)}applyQuaternion(e){return this.quaternion.premultiply(e),this}setRotationFromAxisAngle(e,t){this.quaternion.setFromAxisAngle(e,t)}setRotationFromEuler(e){this.quaternion.setFromEuler(e,!0)}setRotationFromMatrix(e){this.quaternion.setFromRotationMatrix(e)}setRotationFromQuaternion(e){this.quaternion.copy(e)}rotateOnAxis(e,t){return si.setFromAxisAngle(e,t),this.quaternion.multiply(si),this}rotateOnWorldAxis(e,t){return si.setFromAxisAngle(e,t),this.quaternion.premultiply(si),this}rotateX(e){return this.rotateOnAxis(ho,e)}rotateY(e){return this.rotateOnAxis(fo,e)}rotateZ(e){return this.rotateOnAxis(po,e)}translateOnAxis(e,t){return uo.copy(e).applyQuaternion(this.quaternion),this.position.add(uo.multiplyScalar(t)),this}translateX(e){return this.translateOnAxis(ho,e)}translateY(e){return this.translateOnAxis(fo,e)}translateZ(e){return this.translateOnAxis(po,e)}localToWorld(e){return this.updateWorldMatrix(!0,!1),e.applyMatrix4(this.matrixWorld)}worldToLocal(e){return this.updateWorldMatrix(!0,!1),e.applyMatrix4(nn.copy(this.matrixWorld).invert())}lookAt(e,t,i){e.isVector3?or.copy(e):or.set(e,t,i);const r=this.parent;this.updateWorldMatrix(!0,!1),ki.setFromMatrixPosition(this.matrixWorld),this.isCamera||this.isLight?nn.lookAt(ki,or,this.up):nn.lookAt(or,ki,this.up),this.quaternion.setFromRotationMatrix(nn),r&&(nn.extractRotation(r.matrixWorld),si.setFromRotationMatrix(nn),this.quaternion.premultiply(si.invert()))}add(e){if(arguments.length>1){for(let t=0;t<arguments.length;t++)this.add(arguments[t]);return this}return e===this?(console.error("THREE.Object3D.add: object can't be added as a child of itself.",e),this):(e&&e.isObject3D?(e.removeFromParent(),e.parent=this,this.children.push(e),e.dispatchEvent(mo),oi.child=e,this.dispatchEvent(oi),oi.child=null):console.error("THREE.Object3D.add: object not an instance of THREE.Object3D.",e),this)}remove(e){if(arguments.length>1){for(let i=0;i<arguments.length;i++)this.remove(arguments[i]);return this}const t=this.children.indexOf(e);return t!==-1&&(e.parent=null,this.children.splice(t,1),e.dispatchEvent(au),ia.child=e,this.dispatchEvent(ia),ia.child=null),this}removeFromParent(){const e=this.parent;return e!==null&&e.remove(this),this}clear(){return this.remove(...this.children)}attach(e){return this.updateWorldMatrix(!0,!1),nn.copy(this.matrixWorld).invert(),e.parent!==null&&(e.parent.updateWorldMatrix(!0,!1),nn.multiply(e.parent.matrixWorld)),e.applyMatrix4(nn),e.removeFromParent(),e.parent=this,this.children.push(e),e.updateWorldMatrix(!1,!0),e.dispatchEvent(mo),oi.child=e,this.dispatchEvent(oi),oi.child=null,this}getObjectById(e){return this.getObjectByProperty("id",e)}getObjectByName(e){return this.getObjectByProperty("name",e)}getObjectByProperty(e,t){if(this[e]===t)return this;for(let i=0,r=this.children.length;i<r;i++){const s=this.children[i].getObjectByProperty(e,t);if(s!==void 0)return s}}getObjectsByProperty(e,t,i=[]){this[e]===t&&i.push(this);const r=this.children;for(let a=0,s=r.length;a<s;a++)r[a].getObjectsByProperty(e,t,i);return i}getWorldPosition(e){return this.updateWorldMatrix(!0,!1),e.setFromMatrixPosition(this.matrixWorld)}getWorldQuaternion(e){return this.updateWorldMatrix(!0,!1),this.matrixWorld.decompose(ki,e,iu),e}getWorldScale(e){return this.updateWorldMatrix(!0,!1),this.matrixWorld.decompose(ki,ru,e),e}getWorldDirection(e){this.updateWorldMatrix(!0,!1);const t=this.matrixWorld.elements;return e.set(t[8],t[9],t[10]).normalize()}raycast(){}traverse(e){e(this);const t=this.children;for(let i=0,r=t.length;i<r;i++)t[i].traverse(e)}traverseVisible(e){if(this.visible===!1)return;e(this);const t=this.children;for(let i=0,r=t.length;i<r;i++)t[i].traverseVisible(e)}traverseAncestors(e){const t=this.parent;t!==null&&(e(t),t.traverseAncestors(e))}updateMatrix(){this.matrix.compose(this.position,this.quaternion,this.scale),this.matrixWorldNeedsUpdate=!0}updateMatrixWorld(e){this.matrixAutoUpdate&&this.updateMatrix(),(this.matrixWorldNeedsUpdate||e)&&(this.matrixWorldAutoUpdate===!0&&(this.parent===null?this.matrixWorld.copy(this.matrix):this.matrixWorld.multiplyMatrices(this.parent.matrixWorld,this.matrix)),this.matrixWorldNeedsUpdate=!1,e=!0);const t=this.children;for(let i=0,r=t.length;i<r;i++)t[i].updateMatrixWorld(e)}updateWorldMatrix(e,t){const i=this.parent;if(e===!0&&i!==null&&i.updateWorldMatrix(!0,!1),this.matrixAutoUpdate&&this.updateMatrix(),this.matrixWorldAutoUpdate===!0&&(this.parent===null?this.matrixWorld.copy(this.matrix):this.matrixWorld.multiplyMatrices(this.parent.matrixWorld,this.matrix)),t===!0){const r=this.children;for(let a=0,s=r.length;a<s;a++)r[a].updateWorldMatrix(!1,!0)}}toJSON(e){const t=e===void 0||typeof e=="string",i={};t&&(e={geometries:{},materials:{},textures:{},images:{},shapes:{},skeletons:{},animations:{},nodes:{}},i.metadata={version:4.6,type:"Object",generator:"Object3D.toJSON"});const r={};r.uuid=this.uuid,r.type=this.type,this.name!==""&&(r.name=this.name),this.castShadow===!0&&(r.castShadow=!0),this.receiveShadow===!0&&(r.receiveShadow=!0),this.visible===!1&&(r.visible=!1),this.frustumCulled===!1&&(r.frustumCulled=!1),this.renderOrder!==0&&(r.renderOrder=this.renderOrder),Object.keys(this.userData).length>0&&(r.userData=this.userData),r.layers=this.layers.mask,r.matrix=this.matrix.toArray(),r.up=this.up.toArray(),this.matrixAutoUpdate===!1&&(r.matrixAutoUpdate=!1),this.isInstancedMesh&&(r.type="InstancedMesh",r.count=this.count,r.instanceMatrix=this.instanceMatrix.toJSON(),this.instanceColor!==null&&(r.instanceColor=this.instanceColor.toJSON())),this.isBatchedMesh&&(r.type="BatchedMesh",r.perObjectFrustumCulled=this.perObjectFrustumCulled,r.sortObjects=this.sortObjects,r.drawRanges=this._drawRanges,r.reservedRanges=this._reservedRanges,r.visibility=this._visibility,r.active=this._active,r.bounds=this._bounds.map(o=>({boxInitialized:o.boxInitialized,boxMin:o.box.min.toArray(),boxMax:o.box.max.toArray(),sphereInitialized:o.sphereInitialized,sphereRadius:o.sphere.radius,sphereCenter:o.sphere.center.toArray()})),r.maxInstanceCount=this._maxInstanceCount,r.maxVertexCount=this._maxVertexCount,r.maxIndexCount=this._maxIndexCount,r.geometryInitialized=this._geometryInitialized,r.geometryCount=this._geometryCount,r.matricesTexture=this._matricesTexture.toJSON(e),this._colorsTexture!==null&&(r.colorsTexture=this._colorsTexture.toJSON(e)),this.boundingSphere!==null&&(r.boundingSphere={center:r.boundingSphere.center.toArray(),radius:r.boundingSphere.radius}),this.boundingBox!==null&&(r.boundingBox={min:r.boundingBox.min.toArray(),max:r.boundingBox.max.toArray()}));function a(o,c){return o[c.uuid]===void 0&&(o[c.uuid]=c.toJSON(e)),c.uuid}if(this.isScene)this.background&&(this.background.isColor?r.background=this.background.toJSON():this.background.isTexture&&(r.background=this.background.toJSON(e).uuid)),this.environment&&this.environment.isTexture&&this.environment.isRenderTargetTexture!==!0&&(r.environment=this.environment.toJSON(e).uuid);else if(this.isMesh||this.isLine||this.isPoints){r.geometry=a(e.geometries,this.geometry);const o=this.geometry.parameters;if(o!==void 0&&o.shapes!==void 0){const c=o.shapes;if(Array.isArray(c))for(let l=0,d=c.length;l<d;l++){const h=c[l];a(e.shapes,h)}else a(e.shapes,c)}}if(this.isSkinnedMesh&&(r.bindMode=this.bindMode,r.bindMatrix=this.bindMatrix.toArray(),this.skeleton!==void 0&&(a(e.skeletons,this.skeleton),r.skeleton=this.skeleton.uuid)),this.material!==void 0)if(Array.isArray(this.material)){const o=[];for(let c=0,l=this.material.length;c<l;c++)o.push(a(e.materials,this.material[c]));r.material=o}else r.material=a(e.materials,this.material);if(this.children.length>0){r.children=[];for(let o=0;o<this.children.length;o++)r.children.push(this.children[o].toJSON(e).object)}if(this.animations.length>0){r.animations=[];for(let o=0;o<this.animations.length;o++){const c=this.animations[o];r.animations.push(a(e.animations,c))}}if(t){const o=s(e.geometries),c=s(e.materials),l=s(e.textures),d=s(e.images),h=s(e.shapes),f=s(e.skeletons),m=s(e.animations),g=s(e.nodes);o.length>0&&(i.geometries=o),c.length>0&&(i.materials=c),l.length>0&&(i.textures=l),d.length>0&&(i.images=d),h.length>0&&(i.shapes=h),f.length>0&&(i.skeletons=f),m.length>0&&(i.animations=m),g.length>0&&(i.nodes=g)}return i.object=r,i;function s(o){const c=[];for(const l in o){const d=o[l];delete d.metadata,c.push(d)}return c}}clone(e){return new this.constructor().copy(this,e)}copy(e,t=!0){if(this.name=e.name,this.up.copy(e.up),this.position.copy(e.position),this.rotation.order=e.rotation.order,this.quaternion.copy(e.quaternion),this.scale.copy(e.scale),this.matrix.copy(e.matrix),this.matrixWorld.copy(e.matrixWorld),this.matrixAutoUpdate=e.matrixAutoUpdate,this.matrixWorldAutoUpdate=e.matrixWorldAutoUpdate,this.matrixWorldNeedsUpdate=e.matrixWorldNeedsUpdate,this.layers.mask=e.layers.mask,this.visible=e.visible,this.castShadow=e.castShadow,this.receiveShadow=e.receiveShadow,this.frustumCulled=e.frustumCulled,this.renderOrder=e.renderOrder,this.animations=e.animations.slice(),this.userData=JSON.parse(JSON.stringify(e.userData)),t===!0)for(let i=0;i<e.children.length;i++){const r=e.children[i];this.add(r.clone())}return this}}Et.DEFAULT_UP=new k(0,1,0);Et.DEFAULT_MATRIX_AUTO_UPDATE=!0;Et.DEFAULT_MATRIX_WORLD_AUTO_UPDATE=!0;const Xt=new k,rn=new k,ra=new k,an=new k,ci=new k,li=new k,go=new k,aa=new k,sa=new k,oa=new k,ca=new dt,la=new dt,ua=new dt;class Vt{constructor(e=new k,t=new k,i=new k){this.a=e,this.b=t,this.c=i}static getNormal(e,t,i,r){r.subVectors(i,t),Xt.subVectors(e,t),r.cross(Xt);const a=r.lengthSq();return a>0?r.multiplyScalar(1/Math.sqrt(a)):r.set(0,0,0)}static getBarycoord(e,t,i,r,a){Xt.subVectors(r,t),rn.subVectors(i,t),ra.subVectors(e,t);const s=Xt.dot(Xt),o=Xt.dot(rn),c=Xt.dot(ra),l=rn.dot(rn),d=rn.dot(ra),h=s*l-o*o;if(h===0)return a.set(0,0,0),null;const f=1/h,m=(l*c-o*d)*f,g=(s*d-o*c)*f;return a.set(1-m-g,g,m)}static containsPoint(e,t,i,r){return this.getBarycoord(e,t,i,r,an)===null?!1:an.x>=0&&an.y>=0&&an.x+an.y<=1}static getInterpolation(e,t,i,r,a,s,o,c){return this.getBarycoord(e,t,i,r,an)===null?(c.x=0,c.y=0,"z"in c&&(c.z=0),"w"in c&&(c.w=0),null):(c.setScalar(0),c.addScaledVector(a,an.x),c.addScaledVector(s,an.y),c.addScaledVector(o,an.z),c)}static getInterpolatedAttribute(e,t,i,r,a,s){return ca.setScalar(0),la.setScalar(0),ua.setScalar(0),ca.fromBufferAttribute(e,t),la.fromBufferAttribute(e,i),ua.fromBufferAttribute(e,r),s.setScalar(0),s.addScaledVector(ca,a.x),s.addScaledVector(la,a.y),s.addScaledVector(ua,a.z),s}static isFrontFacing(e,t,i,r){return Xt.subVectors(i,t),rn.subVectors(e,t),Xt.cross(rn).dot(r)<0}set(e,t,i){return this.a.copy(e),this.b.copy(t),this.c.copy(i),this}setFromPointsAndIndices(e,t,i,r){return this.a.copy(e[t]),this.b.copy(e[i]),this.c.copy(e[r]),this}setFromAttributeAndIndices(e,t,i,r){return this.a.fromBufferAttribute(e,t),this.b.fromBufferAttribute(e,i),this.c.fromBufferAttribute(e,r),this}clone(){return new this.constructor().copy(this)}copy(e){return this.a.copy(e.a),this.b.copy(e.b),this.c.copy(e.c),this}getArea(){return Xt.subVectors(this.c,this.b),rn.subVectors(this.a,this.b),Xt.cross(rn).length()*.5}getMidpoint(e){return e.addVectors(this.a,this.b).add(this.c).multiplyScalar(1/3)}getNormal(e){return Vt.getNormal(this.a,this.b,this.c,e)}getPlane(e){return e.setFromCoplanarPoints(this.a,this.b,this.c)}getBarycoord(e,t){return Vt.getBarycoord(e,this.a,this.b,this.c,t)}getInterpolation(e,t,i,r,a){return Vt.getInterpolation(e,this.a,this.b,this.c,t,i,r,a)}containsPoint(e){return Vt.containsPoint(e,this.a,this.b,this.c)}isFrontFacing(e){return Vt.isFrontFacing(this.a,this.b,this.c,e)}intersectsBox(e){return e.intersectsTriangle(this)}closestPointToPoint(e,t){const i=this.a,r=this.b,a=this.c;let s,o;ci.subVectors(r,i),li.subVectors(a,i),aa.subVectors(e,i);const c=ci.dot(aa),l=li.dot(aa);if(c<=0&&l<=0)return t.copy(i);sa.subVectors(e,r);const d=ci.dot(sa),h=li.dot(sa);if(d>=0&&h<=d)return t.copy(r);const f=c*h-d*l;if(f<=0&&c>=0&&d<=0)return s=c/(c-d),t.copy(i).addScaledVector(ci,s);oa.subVectors(e,a);const m=ci.dot(oa),g=li.dot(oa);if(g>=0&&m<=g)return t.copy(a);const _=m*l-c*g;if(_<=0&&l>=0&&g<=0)return o=l/(l-g),t.copy(i).addScaledVector(li,o);const p=d*g-m*h;if(p<=0&&h-d>=0&&m-g>=0)return go.subVectors(a,r),o=(h-d)/(h-d+(m-g)),t.copy(r).addScaledVector(go,o);const u=1/(p+_+f);return s=_*u,o=f*u,t.copy(i).addScaledVector(ci,s).addScaledVector(li,o)}equals(e){return e.a.equals(this.a)&&e.b.equals(this.b)&&e.c.equals(this.c)}}const Pc={aliceblue:15792383,antiquewhite:16444375,aqua:65535,aquamarine:8388564,azure:15794175,beige:16119260,bisque:16770244,black:0,blanchedalmond:16772045,blue:255,blueviolet:9055202,brown:10824234,burlywood:14596231,cadetblue:6266528,chartreuse:8388352,chocolate:13789470,coral:16744272,cornflowerblue:6591981,cornsilk:16775388,crimson:14423100,cyan:65535,darkblue:139,darkcyan:35723,darkgoldenrod:12092939,darkgray:11119017,darkgreen:25600,darkgrey:11119017,darkkhaki:12433259,darkmagenta:9109643,darkolivegreen:5597999,darkorange:16747520,darkorchid:10040012,darkred:9109504,darksalmon:15308410,darkseagreen:9419919,darkslateblue:4734347,darkslategray:3100495,darkslategrey:3100495,darkturquoise:52945,darkviolet:9699539,deeppink:16716947,deepskyblue:49151,dimgray:6908265,dimgrey:6908265,dodgerblue:2003199,firebrick:11674146,floralwhite:16775920,forestgreen:2263842,fuchsia:16711935,gainsboro:14474460,ghostwhite:16316671,gold:16766720,goldenrod:14329120,gray:8421504,green:32768,greenyellow:11403055,grey:8421504,honeydew:15794160,hotpink:16738740,indianred:13458524,indigo:4915330,ivory:16777200,khaki:15787660,lavender:15132410,lavenderblush:16773365,lawngreen:8190976,lemonchiffon:16775885,lightblue:11393254,lightcoral:15761536,lightcyan:14745599,lightgoldenrodyellow:16448210,lightgray:13882323,lightgreen:9498256,lightgrey:13882323,lightpink:16758465,lightsalmon:16752762,lightseagreen:2142890,lightskyblue:8900346,lightslategray:7833753,lightslategrey:7833753,lightsteelblue:11584734,lightyellow:16777184,lime:65280,limegreen:3329330,linen:16445670,magenta:16711935,maroon:8388608,mediumaquamarine:6737322,mediumblue:205,mediumorchid:12211667,mediumpurple:9662683,mediumseagreen:3978097,mediumslateblue:8087790,mediumspringgreen:64154,mediumturquoise:4772300,mediumvioletred:13047173,midnightblue:1644912,mintcream:16121850,mistyrose:16770273,moccasin:16770229,navajowhite:16768685,navy:128,oldlace:16643558,olive:8421376,olivedrab:7048739,orange:16753920,orangered:16729344,orchid:14315734,palegoldenrod:15657130,palegreen:10025880,paleturquoise:11529966,palevioletred:14381203,papayawhip:16773077,peachpuff:16767673,peru:13468991,pink:16761035,plum:14524637,powderblue:11591910,purple:8388736,rebeccapurple:6697881,red:16711680,rosybrown:12357519,royalblue:4286945,saddlebrown:9127187,salmon:16416882,sandybrown:16032864,seagreen:3050327,seashell:16774638,sienna:10506797,silver:12632256,skyblue:8900331,slateblue:6970061,slategray:7372944,slategrey:7372944,snow:16775930,springgreen:65407,steelblue:4620980,tan:13808780,teal:32896,thistle:14204888,tomato:16737095,turquoise:4251856,violet:15631086,wheat:16113331,white:16777215,whitesmoke:16119285,yellow:16776960,yellowgreen:10145074},Mn={h:0,s:0,l:0},cr={h:0,s:0,l:0};function da(n,e,t){return t<0&&(t+=1),t>1&&(t-=1),t<1/6?n+(e-n)*6*t:t<1/2?e:t<2/3?n+(e-n)*6*(2/3-t):n}class ce{constructor(e,t,i){return this.isColor=!0,this.r=1,this.g=1,this.b=1,this.set(e,t,i)}set(e,t,i){if(t===void 0&&i===void 0){const r=e;r&&r.isColor?this.copy(r):typeof r=="number"?this.setHex(r):typeof r=="string"&&this.setStyle(r)}else this.setRGB(e,t,i);return this}setScalar(e){return this.r=e,this.g=e,this.b=e,this}setHex(e,t=Nt){return e=Math.floor(e),this.r=(e>>16&255)/255,this.g=(e>>8&255)/255,this.b=(e&255)/255,Je.toWorkingColorSpace(this,t),this}setRGB(e,t,i,r=Je.workingColorSpace){return this.r=e,this.g=t,this.b=i,Je.toWorkingColorSpace(this,r),this}setHSL(e,t,i,r=Je.workingColorSpace){if(e=Hl(e,1),t=We(t,0,1),i=We(i,0,1),t===0)this.r=this.g=this.b=i;else{const a=i<=.5?i*(1+t):i+t-i*t,s=2*i-a;this.r=da(s,a,e+1/3),this.g=da(s,a,e),this.b=da(s,a,e-1/3)}return Je.toWorkingColorSpace(this,r),this}setStyle(e,t=Nt){function i(a){a!==void 0&&parseFloat(a)<1&&console.warn("THREE.Color: Alpha component of "+e+" will be ignored.")}let r;if(r=/^(\w+)\(([^\)]*)\)/.exec(e)){let a;const s=r[1],o=r[2];switch(s){case"rgb":case"rgba":if(a=/^\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*(?:,\s*(\d*\.?\d+)\s*)?$/.exec(o))return i(a[4]),this.setRGB(Math.min(255,parseInt(a[1],10))/255,Math.min(255,parseInt(a[2],10))/255,Math.min(255,parseInt(a[3],10))/255,t);if(a=/^\s*(\d+)\%\s*,\s*(\d+)\%\s*,\s*(\d+)\%\s*(?:,\s*(\d*\.?\d+)\s*)?$/.exec(o))return i(a[4]),this.setRGB(Math.min(100,parseInt(a[1],10))/100,Math.min(100,parseInt(a[2],10))/100,Math.min(100,parseInt(a[3],10))/100,t);break;case"hsl":case"hsla":if(a=/^\s*(\d*\.?\d+)\s*,\s*(\d*\.?\d+)\%\s*,\s*(\d*\.?\d+)\%\s*(?:,\s*(\d*\.?\d+)\s*)?$/.exec(o))return i(a[4]),this.setHSL(parseFloat(a[1])/360,parseFloat(a[2])/100,parseFloat(a[3])/100,t);break;default:console.warn("THREE.Color: Unknown color model "+e)}}else if(r=/^\#([A-Fa-f\d]+)$/.exec(e)){const a=r[1],s=a.length;if(s===3)return this.setRGB(parseInt(a.charAt(0),16)/15,parseInt(a.charAt(1),16)/15,parseInt(a.charAt(2),16)/15,t);if(s===6)return this.setHex(parseInt(a,16),t);console.warn("THREE.Color: Invalid hex color "+e)}else if(e&&e.length>0)return this.setColorName(e,t);return this}setColorName(e,t=Nt){const i=Pc[e.toLowerCase()];return i!==void 0?this.setHex(i,t):console.warn("THREE.Color: Unknown color "+e),this}clone(){return new this.constructor(this.r,this.g,this.b)}copy(e){return this.r=e.r,this.g=e.g,this.b=e.b,this}copySRGBToLinear(e){return this.r=fn(e.r),this.g=fn(e.g),this.b=fn(e.b),this}copyLinearToSRGB(e){return this.r=Si(e.r),this.g=Si(e.g),this.b=Si(e.b),this}convertSRGBToLinear(){return this.copySRGBToLinear(this),this}convertLinearToSRGB(){return this.copyLinearToSRGB(this),this}getHex(e=Nt){return Je.fromWorkingColorSpace(Tt.copy(this),e),Math.round(We(Tt.r*255,0,255))*65536+Math.round(We(Tt.g*255,0,255))*256+Math.round(We(Tt.b*255,0,255))}getHexString(e=Nt){return("000000"+this.getHex(e).toString(16)).slice(-6)}getHSL(e,t=Je.workingColorSpace){Je.fromWorkingColorSpace(Tt.copy(this),t);const i=Tt.r,r=Tt.g,a=Tt.b,s=Math.max(i,r,a),o=Math.min(i,r,a);let c,l;const d=(o+s)/2;if(o===s)c=0,l=0;else{const h=s-o;switch(l=d<=.5?h/(s+o):h/(2-s-o),s){case i:c=(r-a)/h+(r<a?6:0);break;case r:c=(a-i)/h+2;break;case a:c=(i-r)/h+4;break}c/=6}return e.h=c,e.s=l,e.l=d,e}getRGB(e,t=Je.workingColorSpace){return Je.fromWorkingColorSpace(Tt.copy(this),t),e.r=Tt.r,e.g=Tt.g,e.b=Tt.b,e}getStyle(e=Nt){Je.fromWorkingColorSpace(Tt.copy(this),e);const t=Tt.r,i=Tt.g,r=Tt.b;return e!==Nt?`color(${e} ${t.toFixed(3)} ${i.toFixed(3)} ${r.toFixed(3)})`:`rgb(${Math.round(t*255)},${Math.round(i*255)},${Math.round(r*255)})`}offsetHSL(e,t,i){return this.getHSL(Mn),this.setHSL(Mn.h+e,Mn.s+t,Mn.l+i)}add(e){return this.r+=e.r,this.g+=e.g,this.b+=e.b,this}addColors(e,t){return this.r=e.r+t.r,this.g=e.g+t.g,this.b=e.b+t.b,this}addScalar(e){return this.r+=e,this.g+=e,this.b+=e,this}sub(e){return this.r=Math.max(0,this.r-e.r),this.g=Math.max(0,this.g-e.g),this.b=Math.max(0,this.b-e.b),this}multiply(e){return this.r*=e.r,this.g*=e.g,this.b*=e.b,this}multiplyScalar(e){return this.r*=e,this.g*=e,this.b*=e,this}lerp(e,t){return this.r+=(e.r-this.r)*t,this.g+=(e.g-this.g)*t,this.b+=(e.b-this.b)*t,this}lerpColors(e,t,i){return this.r=e.r+(t.r-e.r)*i,this.g=e.g+(t.g-e.g)*i,this.b=e.b+(t.b-e.b)*i,this}lerpHSL(e,t){this.getHSL(Mn),e.getHSL(cr);const i=Yr(Mn.h,cr.h,t),r=Yr(Mn.s,cr.s,t),a=Yr(Mn.l,cr.l,t);return this.setHSL(i,r,a),this}setFromVector3(e){return this.r=e.x,this.g=e.y,this.b=e.z,this}applyMatrix3(e){const t=this.r,i=this.g,r=this.b,a=e.elements;return this.r=a[0]*t+a[3]*i+a[6]*r,this.g=a[1]*t+a[4]*i+a[7]*r,this.b=a[2]*t+a[5]*i+a[8]*r,this}equals(e){return e.r===this.r&&e.g===this.g&&e.b===this.b}fromArray(e,t=0){return this.r=e[t],this.g=e[t+1],this.b=e[t+2],this}toArray(e=[],t=0){return e[t]=this.r,e[t+1]=this.g,e[t+2]=this.b,e}fromBufferAttribute(e,t){return this.r=e.getX(t),this.g=e.getY(t),this.b=e.getZ(t),this}toJSON(){return this.getHex()}*[Symbol.iterator](){yield this.r,yield this.g,yield this.b}}const Tt=new ce;ce.NAMES=Pc;let su=0;class Pi extends Ci{constructor(){super(),this.isMaterial=!0,Object.defineProperty(this,"id",{value:su++}),this.uuid=Yi(),this.name="",this.type="Material",this.blending=xi,this.side=Pn,this.vertexColors=!1,this.opacity=1,this.transparent=!1,this.alphaHash=!1,this.blendSrc=Da,this.blendDst=La,this.blendEquation=Wn,this.blendSrcAlpha=null,this.blendDstAlpha=null,this.blendEquationAlpha=null,this.blendColor=new ce(0,0,0),this.blendAlpha=0,this.depthFunc=Ei,this.depthTest=!0,this.depthWrite=!0,this.stencilWriteMask=255,this.stencilFunc=to,this.stencilRef=0,this.stencilFuncMask=255,this.stencilFail=ei,this.stencilZFail=ei,this.stencilZPass=ei,this.stencilWrite=!1,this.clippingPlanes=null,this.clipIntersection=!1,this.clipShadows=!1,this.shadowSide=null,this.colorWrite=!0,this.precision=null,this.polygonOffset=!1,this.polygonOffsetFactor=0,this.polygonOffsetUnits=0,this.dithering=!1,this.alphaToCoverage=!1,this.premultipliedAlpha=!1,this.forceSinglePass=!1,this.visible=!0,this.toneMapped=!0,this.userData={},this.version=0,this._alphaTest=0}get alphaTest(){return this._alphaTest}set alphaTest(e){this._alphaTest>0!=e>0&&this.version++,this._alphaTest=e}onBeforeRender(){}onBeforeCompile(){}customProgramCacheKey(){return this.onBeforeCompile.toString()}setValues(e){if(e!==void 0)for(const t in e){const i=e[t];if(i===void 0){console.warn(`THREE.Material: parameter '${t}' has value of undefined.`);continue}const r=this[t];if(r===void 0){console.warn(`THREE.Material: '${t}' is not a property of THREE.${this.type}.`);continue}r&&r.isColor?r.set(i):r&&r.isVector3&&i&&i.isVector3?r.copy(i):this[t]=i}}toJSON(e){const t=e===void 0||typeof e=="string";t&&(e={textures:{},images:{}});const i={metadata:{version:4.6,type:"Material",generator:"Material.toJSON"}};i.uuid=this.uuid,i.type=this.type,this.name!==""&&(i.name=this.name),this.color&&this.color.isColor&&(i.color=this.color.getHex()),this.roughness!==void 0&&(i.roughness=this.roughness),this.metalness!==void 0&&(i.metalness=this.metalness),this.sheen!==void 0&&(i.sheen=this.sheen),this.sheenColor&&this.sheenColor.isColor&&(i.sheenColor=this.sheenColor.getHex()),this.sheenRoughness!==void 0&&(i.sheenRoughness=this.sheenRoughness),this.emissive&&this.emissive.isColor&&(i.emissive=this.emissive.getHex()),this.emissiveIntensity!==void 0&&this.emissiveIntensity!==1&&(i.emissiveIntensity=this.emissiveIntensity),this.specular&&this.specular.isColor&&(i.specular=this.specular.getHex()),this.specularIntensity!==void 0&&(i.specularIntensity=this.specularIntensity),this.specularColor&&this.specularColor.isColor&&(i.specularColor=this.specularColor.getHex()),this.shininess!==void 0&&(i.shininess=this.shininess),this.clearcoat!==void 0&&(i.clearcoat=this.clearcoat),this.clearcoatRoughness!==void 0&&(i.clearcoatRoughness=this.clearcoatRoughness),this.clearcoatMap&&this.clearcoatMap.isTexture&&(i.clearcoatMap=this.clearcoatMap.toJSON(e).uuid),this.clearcoatRoughnessMap&&this.clearcoatRoughnessMap.isTexture&&(i.clearcoatRoughnessMap=this.clearcoatRoughnessMap.toJSON(e).uuid),this.clearcoatNormalMap&&this.clearcoatNormalMap.isTexture&&(i.clearcoatNormalMap=this.clearcoatNormalMap.toJSON(e).uuid,i.clearcoatNormalScale=this.clearcoatNormalScale.toArray()),this.dispersion!==void 0&&(i.dispersion=this.dispersion),this.iridescence!==void 0&&(i.iridescence=this.iridescence),this.iridescenceIOR!==void 0&&(i.iridescenceIOR=this.iridescenceIOR),this.iridescenceThicknessRange!==void 0&&(i.iridescenceThicknessRange=this.iridescenceThicknessRange),this.iridescenceMap&&this.iridescenceMap.isTexture&&(i.iridescenceMap=this.iridescenceMap.toJSON(e).uuid),this.iridescenceThicknessMap&&this.iridescenceThicknessMap.isTexture&&(i.iridescenceThicknessMap=this.iridescenceThicknessMap.toJSON(e).uuid),this.anisotropy!==void 0&&(i.anisotropy=this.anisotropy),this.anisotropyRotation!==void 0&&(i.anisotropyRotation=this.anisotropyRotation),this.anisotropyMap&&this.anisotropyMap.isTexture&&(i.anisotropyMap=this.anisotropyMap.toJSON(e).uuid),this.map&&this.map.isTexture&&(i.map=this.map.toJSON(e).uuid),this.matcap&&this.matcap.isTexture&&(i.matcap=this.matcap.toJSON(e).uuid),this.alphaMap&&this.alphaMap.isTexture&&(i.alphaMap=this.alphaMap.toJSON(e).uuid),this.lightMap&&this.lightMap.isTexture&&(i.lightMap=this.lightMap.toJSON(e).uuid,i.lightMapIntensity=this.lightMapIntensity),this.aoMap&&this.aoMap.isTexture&&(i.aoMap=this.aoMap.toJSON(e).uuid,i.aoMapIntensity=this.aoMapIntensity),this.bumpMap&&this.bumpMap.isTexture&&(i.bumpMap=this.bumpMap.toJSON(e).uuid,i.bumpScale=this.bumpScale),this.normalMap&&this.normalMap.isTexture&&(i.normalMap=this.normalMap.toJSON(e).uuid,i.normalMapType=this.normalMapType,i.normalScale=this.normalScale.toArray()),this.displacementMap&&this.displacementMap.isTexture&&(i.displacementMap=this.displacementMap.toJSON(e).uuid,i.displacementScale=this.displacementScale,i.displacementBias=this.displacementBias),this.roughnessMap&&this.roughnessMap.isTexture&&(i.roughnessMap=this.roughnessMap.toJSON(e).uuid),this.metalnessMap&&this.metalnessMap.isTexture&&(i.metalnessMap=this.metalnessMap.toJSON(e).uuid),this.emissiveMap&&this.emissiveMap.isTexture&&(i.emissiveMap=this.emissiveMap.toJSON(e).uuid),this.specularMap&&this.specularMap.isTexture&&(i.specularMap=this.specularMap.toJSON(e).uuid),this.specularIntensityMap&&this.specularIntensityMap.isTexture&&(i.specularIntensityMap=this.specularIntensityMap.toJSON(e).uuid),this.specularColorMap&&this.specularColorMap.isTexture&&(i.specularColorMap=this.specularColorMap.toJSON(e).uuid),this.envMap&&this.envMap.isTexture&&(i.envMap=this.envMap.toJSON(e).uuid,this.combine!==void 0&&(i.combine=this.combine)),this.envMapRotation!==void 0&&(i.envMapRotation=this.envMapRotation.toArray()),this.envMapIntensity!==void 0&&(i.envMapIntensity=this.envMapIntensity),this.reflectivity!==void 0&&(i.reflectivity=this.reflectivity),this.refractionRatio!==void 0&&(i.refractionRatio=this.refractionRatio),this.gradientMap&&this.gradientMap.isTexture&&(i.gradientMap=this.gradientMap.toJSON(e).uuid),this.transmission!==void 0&&(i.transmission=this.transmission),this.transmissionMap&&this.transmissionMap.isTexture&&(i.transmissionMap=this.transmissionMap.toJSON(e).uuid),this.thickness!==void 0&&(i.thickness=this.thickness),this.thicknessMap&&this.thicknessMap.isTexture&&(i.thicknessMap=this.thicknessMap.toJSON(e).uuid),this.attenuationDistance!==void 0&&this.attenuationDistance!==1/0&&(i.attenuationDistance=this.attenuationDistance),this.attenuationColor!==void 0&&(i.attenuationColor=this.attenuationColor.getHex()),this.size!==void 0&&(i.size=this.size),this.shadowSide!==null&&(i.shadowSide=this.shadowSide),this.sizeAttenuation!==void 0&&(i.sizeAttenuation=this.sizeAttenuation),this.blending!==xi&&(i.blending=this.blending),this.side!==Pn&&(i.side=this.side),this.vertexColors===!0&&(i.vertexColors=!0),this.opacity<1&&(i.opacity=this.opacity),this.transparent===!0&&(i.transparent=!0),this.blendSrc!==Da&&(i.blendSrc=this.blendSrc),this.blendDst!==La&&(i.blendDst=this.blendDst),this.blendEquation!==Wn&&(i.blendEquation=this.blendEquation),this.blendSrcAlpha!==null&&(i.blendSrcAlpha=this.blendSrcAlpha),this.blendDstAlpha!==null&&(i.blendDstAlpha=this.blendDstAlpha),this.blendEquationAlpha!==null&&(i.blendEquationAlpha=this.blendEquationAlpha),this.blendColor&&this.blendColor.isColor&&(i.blendColor=this.blendColor.getHex()),this.blendAlpha!==0&&(i.blendAlpha=this.blendAlpha),this.depthFunc!==Ei&&(i.depthFunc=this.depthFunc),this.depthTest===!1&&(i.depthTest=this.depthTest),this.depthWrite===!1&&(i.depthWrite=this.depthWrite),this.colorWrite===!1&&(i.colorWrite=this.colorWrite),this.stencilWriteMask!==255&&(i.stencilWriteMask=this.stencilWriteMask),this.stencilFunc!==to&&(i.stencilFunc=this.stencilFunc),this.stencilRef!==0&&(i.stencilRef=this.stencilRef),this.stencilFuncMask!==255&&(i.stencilFuncMask=this.stencilFuncMask),this.stencilFail!==ei&&(i.stencilFail=this.stencilFail),this.stencilZFail!==ei&&(i.stencilZFail=this.stencilZFail),this.stencilZPass!==ei&&(i.stencilZPass=this.stencilZPass),this.stencilWrite===!0&&(i.stencilWrite=this.stencilWrite),this.rotation!==void 0&&this.rotation!==0&&(i.rotation=this.rotation),this.polygonOffset===!0&&(i.polygonOffset=!0),this.polygonOffsetFactor!==0&&(i.polygonOffsetFactor=this.polygonOffsetFactor),this.polygonOffsetUnits!==0&&(i.polygonOffsetUnits=this.polygonOffsetUnits),this.linewidth!==void 0&&this.linewidth!==1&&(i.linewidth=this.linewidth),this.dashSize!==void 0&&(i.dashSize=this.dashSize),this.gapSize!==void 0&&(i.gapSize=this.gapSize),this.scale!==void 0&&(i.scale=this.scale),this.dithering===!0&&(i.dithering=!0),this.alphaTest>0&&(i.alphaTest=this.alphaTest),this.alphaHash===!0&&(i.alphaHash=!0),this.alphaToCoverage===!0&&(i.alphaToCoverage=!0),this.premultipliedAlpha===!0&&(i.premultipliedAlpha=!0),this.forceSinglePass===!0&&(i.forceSinglePass=!0),this.wireframe===!0&&(i.wireframe=!0),this.wireframeLinewidth>1&&(i.wireframeLinewidth=this.wireframeLinewidth),this.wireframeLinecap!=="round"&&(i.wireframeLinecap=this.wireframeLinecap),this.wireframeLinejoin!=="round"&&(i.wireframeLinejoin=this.wireframeLinejoin),this.flatShading===!0&&(i.flatShading=!0),this.visible===!1&&(i.visible=!1),this.toneMapped===!1&&(i.toneMapped=!1),this.fog===!1&&(i.fog=!1),Object.keys(this.userData).length>0&&(i.userData=this.userData);function r(a){const s=[];for(const o in a){const c=a[o];delete c.metadata,s.push(c)}return s}if(t){const a=r(e.textures),s=r(e.images);a.length>0&&(i.textures=a),s.length>0&&(i.images=s)}return i}clone(){return new this.constructor().copy(this)}copy(e){this.name=e.name,this.blending=e.blending,this.side=e.side,this.vertexColors=e.vertexColors,this.opacity=e.opacity,this.transparent=e.transparent,this.blendSrc=e.blendSrc,this.blendDst=e.blendDst,this.blendEquation=e.blendEquation,this.blendSrcAlpha=e.blendSrcAlpha,this.blendDstAlpha=e.blendDstAlpha,this.blendEquationAlpha=e.blendEquationAlpha,this.blendColor.copy(e.blendColor),this.blendAlpha=e.blendAlpha,this.depthFunc=e.depthFunc,this.depthTest=e.depthTest,this.depthWrite=e.depthWrite,this.stencilWriteMask=e.stencilWriteMask,this.stencilFunc=e.stencilFunc,this.stencilRef=e.stencilRef,this.stencilFuncMask=e.stencilFuncMask,this.stencilFail=e.stencilFail,this.stencilZFail=e.stencilZFail,this.stencilZPass=e.stencilZPass,this.stencilWrite=e.stencilWrite;const t=e.clippingPlanes;let i=null;if(t!==null){const r=t.length;i=new Array(r);for(let a=0;a!==r;++a)i[a]=t[a].clone()}return this.clippingPlanes=i,this.clipIntersection=e.clipIntersection,this.clipShadows=e.clipShadows,this.shadowSide=e.shadowSide,this.colorWrite=e.colorWrite,this.precision=e.precision,this.polygonOffset=e.polygonOffset,this.polygonOffsetFactor=e.polygonOffsetFactor,this.polygonOffsetUnits=e.polygonOffsetUnits,this.dithering=e.dithering,this.alphaTest=e.alphaTest,this.alphaHash=e.alphaHash,this.alphaToCoverage=e.alphaToCoverage,this.premultipliedAlpha=e.premultipliedAlpha,this.forceSinglePass=e.forceSinglePass,this.visible=e.visible,this.toneMapped=e.toneMapped,this.userData=JSON.parse(JSON.stringify(e.userData)),this}dispose(){this.dispatchEvent({type:"dispose"})}set needsUpdate(e){e===!0&&this.version++}onBuild(){console.warn("Material: onBuild() has been removed.")}}class Di extends Pi{constructor(e){super(),this.isMeshBasicMaterial=!0,this.type="MeshBasicMaterial",this.color=new ce(16777215),this.map=null,this.lightMap=null,this.lightMapIntensity=1,this.aoMap=null,this.aoMapIntensity=1,this.specularMap=null,this.alphaMap=null,this.envMap=null,this.envMapRotation=new Mt,this.combine=pc,this.reflectivity=1,this.refractionRatio=.98,this.wireframe=!1,this.wireframeLinewidth=1,this.wireframeLinecap="round",this.wireframeLinejoin="round",this.fog=!0,this.setValues(e)}copy(e){return super.copy(e),this.color.copy(e.color),this.map=e.map,this.lightMap=e.lightMap,this.lightMapIntensity=e.lightMapIntensity,this.aoMap=e.aoMap,this.aoMapIntensity=e.aoMapIntensity,this.specularMap=e.specularMap,this.alphaMap=e.alphaMap,this.envMap=e.envMap,this.envMapRotation.copy(e.envMapRotation),this.combine=e.combine,this.reflectivity=e.reflectivity,this.refractionRatio=e.refractionRatio,this.wireframe=e.wireframe,this.wireframeLinewidth=e.wireframeLinewidth,this.wireframeLinecap=e.wireframeLinecap,this.wireframeLinejoin=e.wireframeLinejoin,this.fog=e.fog,this}}const pt=new k,lr=new Xe;let ou=0;class Jt{constructor(e,t,i=!1){if(Array.isArray(e))throw new TypeError("THREE.BufferAttribute: array should be a Typed Array.");this.isBufferAttribute=!0,Object.defineProperty(this,"id",{value:ou++}),this.name="",this.array=e,this.itemSize=t,this.count=e!==void 0?e.length/t:0,this.normalized=i,this.usage=no,this.updateRanges=[],this.gpuType=un,this.version=0}onUploadCallback(){}set needsUpdate(e){e===!0&&this.version++}setUsage(e){return this.usage=e,this}addUpdateRange(e,t){this.updateRanges.push({start:e,count:t})}clearUpdateRanges(){this.updateRanges.length=0}copy(e){return this.name=e.name,this.array=new e.array.constructor(e.array),this.itemSize=e.itemSize,this.count=e.count,this.normalized=e.normalized,this.usage=e.usage,this.gpuType=e.gpuType,this}copyAt(e,t,i){e*=this.itemSize,i*=t.itemSize;for(let r=0,a=this.itemSize;r<a;r++)this.array[e+r]=t.array[i+r];return this}copyArray(e){return this.array.set(e),this}applyMatrix3(e){if(this.itemSize===2)for(let t=0,i=this.count;t<i;t++)lr.fromBufferAttribute(this,t),lr.applyMatrix3(e),this.setXY(t,lr.x,lr.y);else if(this.itemSize===3)for(let t=0,i=this.count;t<i;t++)pt.fromBufferAttribute(this,t),pt.applyMatrix3(e),this.setXYZ(t,pt.x,pt.y,pt.z);return this}applyMatrix4(e){for(let t=0,i=this.count;t<i;t++)pt.fromBufferAttribute(this,t),pt.applyMatrix4(e),this.setXYZ(t,pt.x,pt.y,pt.z);return this}applyNormalMatrix(e){for(let t=0,i=this.count;t<i;t++)pt.fromBufferAttribute(this,t),pt.applyNormalMatrix(e),this.setXYZ(t,pt.x,pt.y,pt.z);return this}transformDirection(e){for(let t=0,i=this.count;t<i;t++)pt.fromBufferAttribute(this,t),pt.transformDirection(e),this.setXYZ(t,pt.x,pt.y,pt.z);return this}set(e,t=0){return this.array.set(e,t),this}getComponent(e,t){let i=this.array[e*this.itemSize+t];return this.normalized&&(i=zi(i,this.array)),i}setComponent(e,t,i){return this.normalized&&(i=Pt(i,this.array)),this.array[e*this.itemSize+t]=i,this}getX(e){let t=this.array[e*this.itemSize];return this.normalized&&(t=zi(t,this.array)),t}setX(e,t){return this.normalized&&(t=Pt(t,this.array)),this.array[e*this.itemSize]=t,this}getY(e){let t=this.array[e*this.itemSize+1];return this.normalized&&(t=zi(t,this.array)),t}setY(e,t){return this.normalized&&(t=Pt(t,this.array)),this.array[e*this.itemSize+1]=t,this}getZ(e){let t=this.array[e*this.itemSize+2];return this.normalized&&(t=zi(t,this.array)),t}setZ(e,t){return this.normalized&&(t=Pt(t,this.array)),this.array[e*this.itemSize+2]=t,this}getW(e){let t=this.array[e*this.itemSize+3];return this.normalized&&(t=zi(t,this.array)),t}setW(e,t){return this.normalized&&(t=Pt(t,this.array)),this.array[e*this.itemSize+3]=t,this}setXY(e,t,i){return e*=this.itemSize,this.normalized&&(t=Pt(t,this.array),i=Pt(i,this.array)),this.array[e+0]=t,this.array[e+1]=i,this}setXYZ(e,t,i,r){return e*=this.itemSize,this.normalized&&(t=Pt(t,this.array),i=Pt(i,this.array),r=Pt(r,this.array)),this.array[e+0]=t,this.array[e+1]=i,this.array[e+2]=r,this}setXYZW(e,t,i,r,a){return e*=this.itemSize,this.normalized&&(t=Pt(t,this.array),i=Pt(i,this.array),r=Pt(r,this.array),a=Pt(a,this.array)),this.array[e+0]=t,this.array[e+1]=i,this.array[e+2]=r,this.array[e+3]=a,this}onUpload(e){return this.onUploadCallback=e,this}clone(){return new this.constructor(this.array,this.itemSize).copy(this)}toJSON(){const e={itemSize:this.itemSize,type:this.array.constructor.name,array:Array.from(this.array),normalized:this.normalized};return this.name!==""&&(e.name=this.name),this.usage!==no&&(e.usage=this.usage),e}}class Dc extends Jt{constructor(e,t,i){super(new Uint16Array(e),t,i)}}class Lc extends Jt{constructor(e,t,i){super(new Uint32Array(e),t,i)}}class Ge extends Jt{constructor(e,t,i){super(new Float32Array(e),t,i)}}let cu=0;const Ot=new at,ha=new Et,ui=new k,zt=new $i,Oi=new $i,xt=new k;class Ye extends Ci{constructor(){super(),this.isBufferGeometry=!0,Object.defineProperty(this,"id",{value:cu++}),this.uuid=Yi(),this.name="",this.type="BufferGeometry",this.index=null,this.indirect=null,this.attributes={},this.morphAttributes={},this.morphTargetsRelative=!1,this.groups=[],this.boundingBox=null,this.boundingSphere=null,this.drawRange={start:0,count:1/0},this.userData={}}getIndex(){return this.index}setIndex(e){return Array.isArray(e)?this.index=new(Rc(e)?Lc:Dc)(e,1):this.index=e,this}setIndirect(e){return this.indirect=e,this}getIndirect(){return this.indirect}getAttribute(e){return this.attributes[e]}setAttribute(e,t){return this.attributes[e]=t,this}deleteAttribute(e){return delete this.attributes[e],this}hasAttribute(e){return this.attributes[e]!==void 0}addGroup(e,t,i=0){this.groups.push({start:e,count:t,materialIndex:i})}clearGroups(){this.groups=[]}setDrawRange(e,t){this.drawRange.start=e,this.drawRange.count=t}applyMatrix4(e){const t=this.attributes.position;t!==void 0&&(t.applyMatrix4(e),t.needsUpdate=!0);const i=this.attributes.normal;if(i!==void 0){const a=new Be().getNormalMatrix(e);i.applyNormalMatrix(a),i.needsUpdate=!0}const r=this.attributes.tangent;return r!==void 0&&(r.transformDirection(e),r.needsUpdate=!0),this.boundingBox!==null&&this.computeBoundingBox(),this.boundingSphere!==null&&this.computeBoundingSphere(),this}applyQuaternion(e){return Ot.makeRotationFromQuaternion(e),this.applyMatrix4(Ot),this}rotateX(e){return Ot.makeRotationX(e),this.applyMatrix4(Ot),this}rotateY(e){return Ot.makeRotationY(e),this.applyMatrix4(Ot),this}rotateZ(e){return Ot.makeRotationZ(e),this.applyMatrix4(Ot),this}translate(e,t,i){return Ot.makeTranslation(e,t,i),this.applyMatrix4(Ot),this}scale(e,t,i){return Ot.makeScale(e,t,i),this.applyMatrix4(Ot),this}lookAt(e){return ha.lookAt(e),ha.updateMatrix(),this.applyMatrix4(ha.matrix),this}center(){return this.computeBoundingBox(),this.boundingBox.getCenter(ui).negate(),this.translate(ui.x,ui.y,ui.z),this}setFromPoints(e){const t=this.getAttribute("position");if(t===void 0){const i=[];for(let r=0,a=e.length;r<a;r++){const s=e[r];i.push(s.x,s.y,s.z||0)}this.setAttribute("position",new Ge(i,3))}else{const i=Math.min(e.length,t.count);for(let r=0;r<i;r++){const a=e[r];t.setXYZ(r,a.x,a.y,a.z||0)}e.length>t.count&&console.warn("THREE.BufferGeometry: Buffer size too small for points data. Use .dispose() and create a new geometry."),t.needsUpdate=!0}return this}computeBoundingBox(){this.boundingBox===null&&(this.boundingBox=new $i);const e=this.attributes.position,t=this.morphAttributes.position;if(e&&e.isGLBufferAttribute){console.error("THREE.BufferGeometry.computeBoundingBox(): GLBufferAttribute requires a manual bounding box.",this),this.boundingBox.set(new k(-1/0,-1/0,-1/0),new k(1/0,1/0,1/0));return}if(e!==void 0){if(this.boundingBox.setFromBufferAttribute(e),t)for(let i=0,r=t.length;i<r;i++){const a=t[i];zt.setFromBufferAttribute(a),this.morphTargetsRelative?(xt.addVectors(this.boundingBox.min,zt.min),this.boundingBox.expandByPoint(xt),xt.addVectors(this.boundingBox.max,zt.max),this.boundingBox.expandByPoint(xt)):(this.boundingBox.expandByPoint(zt.min),this.boundingBox.expandByPoint(zt.max))}}else this.boundingBox.makeEmpty();(isNaN(this.boundingBox.min.x)||isNaN(this.boundingBox.min.y)||isNaN(this.boundingBox.min.z))&&console.error('THREE.BufferGeometry.computeBoundingBox(): Computed min/max have NaN values. The "position" attribute is likely to have NaN values.',this)}computeBoundingSphere(){this.boundingSphere===null&&(this.boundingSphere=new Hr);const e=this.attributes.position,t=this.morphAttributes.position;if(e&&e.isGLBufferAttribute){console.error("THREE.BufferGeometry.computeBoundingSphere(): GLBufferAttribute requires a manual bounding sphere.",this),this.boundingSphere.set(new k,1/0);return}if(e){const i=this.boundingSphere.center;if(zt.setFromBufferAttribute(e),t)for(let a=0,s=t.length;a<s;a++){const o=t[a];Oi.setFromBufferAttribute(o),this.morphTargetsRelative?(xt.addVectors(zt.min,Oi.min),zt.expandByPoint(xt),xt.addVectors(zt.max,Oi.max),zt.expandByPoint(xt)):(zt.expandByPoint(Oi.min),zt.expandByPoint(Oi.max))}zt.getCenter(i);let r=0;for(let a=0,s=e.count;a<s;a++)xt.fromBufferAttribute(e,a),r=Math.max(r,i.distanceToSquared(xt));if(t)for(let a=0,s=t.length;a<s;a++){const o=t[a],c=this.morphTargetsRelative;for(let l=0,d=o.count;l<d;l++)xt.fromBufferAttribute(o,l),c&&(ui.fromBufferAttribute(e,l),xt.add(ui)),r=Math.max(r,i.distanceToSquared(xt))}this.boundingSphere.radius=Math.sqrt(r),isNaN(this.boundingSphere.radius)&&console.error('THREE.BufferGeometry.computeBoundingSphere(): Computed radius is NaN. The "position" attribute is likely to have NaN values.',this)}}computeTangents(){const e=this.index,t=this.attributes;if(e===null||t.position===void 0||t.normal===void 0||t.uv===void 0){console.error("THREE.BufferGeometry: .computeTangents() failed. Missing required attributes (index, position, normal or uv)");return}const i=t.position,r=t.normal,a=t.uv;this.hasAttribute("tangent")===!1&&this.setAttribute("tangent",new Jt(new Float32Array(4*i.count),4));const s=this.getAttribute("tangent"),o=[],c=[];for(let L=0;L<i.count;L++)o[L]=new k,c[L]=new k;const l=new k,d=new k,h=new k,f=new Xe,m=new Xe,g=new Xe,_=new k,p=new k;function u(L,x,v){l.fromBufferAttribute(i,L),d.fromBufferAttribute(i,x),h.fromBufferAttribute(i,v),f.fromBufferAttribute(a,L),m.fromBufferAttribute(a,x),g.fromBufferAttribute(a,v),d.sub(l),h.sub(l),m.sub(f),g.sub(f);const R=1/(m.x*g.y-g.x*m.y);isFinite(R)&&(_.copy(d).multiplyScalar(g.y).addScaledVector(h,-m.y).multiplyScalar(R),p.copy(h).multiplyScalar(m.x).addScaledVector(d,-g.x).multiplyScalar(R),o[L].add(_),o[x].add(_),o[v].add(_),c[L].add(p),c[x].add(p),c[v].add(p))}let y=this.groups;y.length===0&&(y=[{start:0,count:e.count}]);for(let L=0,x=y.length;L<x;++L){const v=y[L],R=v.start,U=v.count;for(let C=R,P=R+U;C<P;C+=3)u(e.getX(C+0),e.getX(C+1),e.getX(C+2))}const S=new k,M=new k,T=new k,b=new k;function w(L){T.fromBufferAttribute(r,L),b.copy(T);const x=o[L];S.copy(x),S.sub(T.multiplyScalar(T.dot(x))).normalize(),M.crossVectors(b,x);const R=M.dot(c[L])<0?-1:1;s.setXYZW(L,S.x,S.y,S.z,R)}for(let L=0,x=y.length;L<x;++L){const v=y[L],R=v.start,U=v.count;for(let C=R,P=R+U;C<P;C+=3)w(e.getX(C+0)),w(e.getX(C+1)),w(e.getX(C+2))}}computeVertexNormals(){const e=this.index,t=this.getAttribute("position");if(t!==void 0){let i=this.getAttribute("normal");if(i===void 0)i=new Jt(new Float32Array(t.count*3),3),this.setAttribute("normal",i);else for(let f=0,m=i.count;f<m;f++)i.setXYZ(f,0,0,0);const r=new k,a=new k,s=new k,o=new k,c=new k,l=new k,d=new k,h=new k;if(e)for(let f=0,m=e.count;f<m;f+=3){const g=e.getX(f+0),_=e.getX(f+1),p=e.getX(f+2);r.fromBufferAttribute(t,g),a.fromBufferAttribute(t,_),s.fromBufferAttribute(t,p),d.subVectors(s,a),h.subVectors(r,a),d.cross(h),o.fromBufferAttribute(i,g),c.fromBufferAttribute(i,_),l.fromBufferAttribute(i,p),o.add(d),c.add(d),l.add(d),i.setXYZ(g,o.x,o.y,o.z),i.setXYZ(_,c.x,c.y,c.z),i.setXYZ(p,l.x,l.y,l.z)}else for(let f=0,m=t.count;f<m;f+=3)r.fromBufferAttribute(t,f+0),a.fromBufferAttribute(t,f+1),s.fromBufferAttribute(t,f+2),d.subVectors(s,a),h.subVectors(r,a),d.cross(h),i.setXYZ(f+0,d.x,d.y,d.z),i.setXYZ(f+1,d.x,d.y,d.z),i.setXYZ(f+2,d.x,d.y,d.z);this.normalizeNormals(),i.needsUpdate=!0}}normalizeNormals(){const e=this.attributes.normal;for(let t=0,i=e.count;t<i;t++)xt.fromBufferAttribute(e,t),xt.normalize(),e.setXYZ(t,xt.x,xt.y,xt.z)}toNonIndexed(){function e(o,c){const l=o.array,d=o.itemSize,h=o.normalized,f=new l.constructor(c.length*d);let m=0,g=0;for(let _=0,p=c.length;_<p;_++){o.isInterleavedBufferAttribute?m=c[_]*o.data.stride+o.offset:m=c[_]*d;for(let u=0;u<d;u++)f[g++]=l[m++]}return new Jt(f,d,h)}if(this.index===null)return console.warn("THREE.BufferGeometry.toNonIndexed(): BufferGeometry is already non-indexed."),this;const t=new Ye,i=this.index.array,r=this.attributes;for(const o in r){const c=r[o],l=e(c,i);t.setAttribute(o,l)}const a=this.morphAttributes;for(const o in a){const c=[],l=a[o];for(let d=0,h=l.length;d<h;d++){const f=l[d],m=e(f,i);c.push(m)}t.morphAttributes[o]=c}t.morphTargetsRelative=this.morphTargetsRelative;const s=this.groups;for(let o=0,c=s.length;o<c;o++){const l=s[o];t.addGroup(l.start,l.count,l.materialIndex)}return t}toJSON(){const e={metadata:{version:4.6,type:"BufferGeometry",generator:"BufferGeometry.toJSON"}};if(e.uuid=this.uuid,e.type=this.type,this.name!==""&&(e.name=this.name),Object.keys(this.userData).length>0&&(e.userData=this.userData),this.parameters!==void 0){const c=this.parameters;for(const l in c)c[l]!==void 0&&(e[l]=c[l]);return e}e.data={attributes:{}};const t=this.index;t!==null&&(e.data.index={type:t.array.constructor.name,array:Array.prototype.slice.call(t.array)});const i=this.attributes;for(const c in i){const l=i[c];e.data.attributes[c]=l.toJSON(e.data)}const r={};let a=!1;for(const c in this.morphAttributes){const l=this.morphAttributes[c],d=[];for(let h=0,f=l.length;h<f;h++){const m=l[h];d.push(m.toJSON(e.data))}d.length>0&&(r[c]=d,a=!0)}a&&(e.data.morphAttributes=r,e.data.morphTargetsRelative=this.morphTargetsRelative);const s=this.groups;s.length>0&&(e.data.groups=JSON.parse(JSON.stringify(s)));const o=this.boundingSphere;return o!==null&&(e.data.boundingSphere={center:o.center.toArray(),radius:o.radius}),e}clone(){return new this.constructor().copy(this)}copy(e){this.index=null,this.attributes={},this.morphAttributes={},this.groups=[],this.boundingBox=null,this.boundingSphere=null;const t={};this.name=e.name;const i=e.index;i!==null&&this.setIndex(i.clone(t));const r=e.attributes;for(const l in r){const d=r[l];this.setAttribute(l,d.clone(t))}const a=e.morphAttributes;for(const l in a){const d=[],h=a[l];for(let f=0,m=h.length;f<m;f++)d.push(h[f].clone(t));this.morphAttributes[l]=d}this.morphTargetsRelative=e.morphTargetsRelative;const s=e.groups;for(let l=0,d=s.length;l<d;l++){const h=s[l];this.addGroup(h.start,h.count,h.materialIndex)}const o=e.boundingBox;o!==null&&(this.boundingBox=o.clone());const c=e.boundingSphere;return c!==null&&(this.boundingSphere=c.clone()),this.drawRange.start=e.drawRange.start,this.drawRange.count=e.drawRange.count,this.userData=e.userData,this}dispose(){this.dispatchEvent({type:"dispose"})}}const _o=new at,Nn=new Ds,ur=new Hr,vo=new k,dr=new k,hr=new k,fr=new k,fa=new k,pr=new k,xo=new k,mr=new k;class je extends Et{constructor(e=new Ye,t=new Di){super(),this.isMesh=!0,this.type="Mesh",this.geometry=e,this.material=t,this.morphTargetDictionary=void 0,this.morphTargetInfluences=void 0,this.updateMorphTargets()}copy(e,t){return super.copy(e,t),e.morphTargetInfluences!==void 0&&(this.morphTargetInfluences=e.morphTargetInfluences.slice()),e.morphTargetDictionary!==void 0&&(this.morphTargetDictionary=Object.assign({},e.morphTargetDictionary)),this.material=Array.isArray(e.material)?e.material.slice():e.material,this.geometry=e.geometry,this}updateMorphTargets(){const t=this.geometry.morphAttributes,i=Object.keys(t);if(i.length>0){const r=t[i[0]];if(r!==void 0){this.morphTargetInfluences=[],this.morphTargetDictionary={};for(let a=0,s=r.length;a<s;a++){const o=r[a].name||String(a);this.morphTargetInfluences.push(0),this.morphTargetDictionary[o]=a}}}}getVertexPosition(e,t){const i=this.geometry,r=i.attributes.position,a=i.morphAttributes.position,s=i.morphTargetsRelative;t.fromBufferAttribute(r,e);const o=this.morphTargetInfluences;if(a&&o){pr.set(0,0,0);for(let c=0,l=a.length;c<l;c++){const d=o[c],h=a[c];d!==0&&(fa.fromBufferAttribute(h,e),s?pr.addScaledVector(fa,d):pr.addScaledVector(fa.sub(t),d))}t.add(pr)}return t}raycast(e,t){const i=this.geometry,r=this.material,a=this.matrixWorld;r!==void 0&&(i.boundingSphere===null&&i.computeBoundingSphere(),ur.copy(i.boundingSphere),ur.applyMatrix4(a),Nn.copy(e.ray).recast(e.near),!(ur.containsPoint(Nn.origin)===!1&&(Nn.intersectSphere(ur,vo)===null||Nn.origin.distanceToSquared(vo)>(e.far-e.near)**2))&&(_o.copy(a).invert(),Nn.copy(e.ray).applyMatrix4(_o),!(i.boundingBox!==null&&Nn.intersectsBox(i.boundingBox)===!1)&&this._computeIntersections(e,t,Nn)))}_computeIntersections(e,t,i){let r;const a=this.geometry,s=this.material,o=a.index,c=a.attributes.position,l=a.attributes.uv,d=a.attributes.uv1,h=a.attributes.normal,f=a.groups,m=a.drawRange;if(o!==null)if(Array.isArray(s))for(let g=0,_=f.length;g<_;g++){const p=f[g],u=s[p.materialIndex],y=Math.max(p.start,m.start),S=Math.min(o.count,Math.min(p.start+p.count,m.start+m.count));for(let M=y,T=S;M<T;M+=3){const b=o.getX(M),w=o.getX(M+1),L=o.getX(M+2);r=gr(this,u,e,i,l,d,h,b,w,L),r&&(r.faceIndex=Math.floor(M/3),r.face.materialIndex=p.materialIndex,t.push(r))}}else{const g=Math.max(0,m.start),_=Math.min(o.count,m.start+m.count);for(let p=g,u=_;p<u;p+=3){const y=o.getX(p),S=o.getX(p+1),M=o.getX(p+2);r=gr(this,s,e,i,l,d,h,y,S,M),r&&(r.faceIndex=Math.floor(p/3),t.push(r))}}else if(c!==void 0)if(Array.isArray(s))for(let g=0,_=f.length;g<_;g++){const p=f[g],u=s[p.materialIndex],y=Math.max(p.start,m.start),S=Math.min(c.count,Math.min(p.start+p.count,m.start+m.count));for(let M=y,T=S;M<T;M+=3){const b=M,w=M+1,L=M+2;r=gr(this,u,e,i,l,d,h,b,w,L),r&&(r.faceIndex=Math.floor(M/3),r.face.materialIndex=p.materialIndex,t.push(r))}}else{const g=Math.max(0,m.start),_=Math.min(c.count,m.start+m.count);for(let p=g,u=_;p<u;p+=3){const y=p,S=p+1,M=p+2;r=gr(this,s,e,i,l,d,h,y,S,M),r&&(r.faceIndex=Math.floor(p/3),t.push(r))}}}}function lu(n,e,t,i,r,a,s,o){let c;if(e.side===Dt?c=i.intersectTriangle(s,a,r,!0,o):c=i.intersectTriangle(r,a,s,e.side===Pn,o),c===null)return null;mr.copy(o),mr.applyMatrix4(n.matrixWorld);const l=t.ray.origin.distanceTo(mr);return l<t.near||l>t.far?null:{distance:l,point:mr.clone(),object:n}}function gr(n,e,t,i,r,a,s,o,c,l){n.getVertexPosition(o,dr),n.getVertexPosition(c,hr),n.getVertexPosition(l,fr);const d=lu(n,e,t,i,dr,hr,fr,xo);if(d){const h=new k;Vt.getBarycoord(xo,dr,hr,fr,h),r&&(d.uv=Vt.getInterpolatedAttribute(r,o,c,l,h,new Xe)),a&&(d.uv1=Vt.getInterpolatedAttribute(a,o,c,l,h,new Xe)),s&&(d.normal=Vt.getInterpolatedAttribute(s,o,c,l,h,new k),d.normal.dot(i.direction)>0&&d.normal.multiplyScalar(-1));const f={a:o,b:c,c:l,normal:new k,materialIndex:0};Vt.getNormal(dr,hr,fr,f.normal),d.face=f,d.barycoord=h}return d}class hn extends Ye{constructor(e=1,t=1,i=1,r=1,a=1,s=1){super(),this.type="BoxGeometry",this.parameters={width:e,height:t,depth:i,widthSegments:r,heightSegments:a,depthSegments:s};const o=this;r=Math.floor(r),a=Math.floor(a),s=Math.floor(s);const c=[],l=[],d=[],h=[];let f=0,m=0;g("z","y","x",-1,-1,i,t,e,s,a,0),g("z","y","x",1,-1,i,t,-e,s,a,1),g("x","z","y",1,1,e,i,t,r,s,2),g("x","z","y",1,-1,e,i,-t,r,s,3),g("x","y","z",1,-1,e,t,i,r,a,4),g("x","y","z",-1,-1,e,t,-i,r,a,5),this.setIndex(c),this.setAttribute("position",new Ge(l,3)),this.setAttribute("normal",new Ge(d,3)),this.setAttribute("uv",new Ge(h,2));function g(_,p,u,y,S,M,T,b,w,L,x){const v=M/w,R=T/L,U=M/2,C=T/2,P=b/2,F=w+1,N=L+1;let O=0,z=0;const G=new k;for(let K=0;K<N;K++){const $=K*R-C;for(let fe=0;fe<F;fe++){const De=fe*v-U;G[_]=De*y,G[p]=$*S,G[u]=P,l.push(G.x,G.y,G.z),G[_]=0,G[p]=0,G[u]=b>0?1:-1,d.push(G.x,G.y,G.z),h.push(fe/w),h.push(1-K/L),O+=1}}for(let K=0;K<L;K++)for(let $=0;$<w;$++){const fe=f+$+F*K,De=f+$+F*(K+1),X=f+($+1)+F*(K+1),ne=f+($+1)+F*K;c.push(fe,De,ne),c.push(De,X,ne),z+=6}o.addGroup(m,z,x),m+=z,f+=O}}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}static fromJSON(e){return new hn(e.width,e.height,e.depth,e.widthSegments,e.heightSegments,e.depthSegments)}}function Ri(n){const e={};for(const t in n){e[t]={};for(const i in n[t]){const r=n[t][i];r&&(r.isColor||r.isMatrix3||r.isMatrix4||r.isVector2||r.isVector3||r.isVector4||r.isTexture||r.isQuaternion)?r.isRenderTargetTexture?(console.warn("UniformsUtils: Textures of render targets cannot be cloned via cloneUniforms() or mergeUniforms()."),e[t][i]=null):e[t][i]=r.clone():Array.isArray(r)?e[t][i]=r.slice():e[t][i]=r}}return e}function wt(n){const e={};for(let t=0;t<n.length;t++){const i=Ri(n[t]);for(const r in i)e[r]=i[r]}return e}function uu(n){const e=[];for(let t=0;t<n.length;t++)e.push(n[t].clone());return e}function Ic(n){const e=n.getRenderTarget();return e===null?n.outputColorSpace:e.isXRRenderTarget===!0?e.texture.colorSpace:Je.workingColorSpace}const du={clone:Ri,merge:wt};var hu=`void main() {
	gl_Position = projectionMatrix * modelViewMatrix * vec4( position, 1.0 );
}`,fu=`void main() {
	gl_FragColor = vec4( 1.0, 0.0, 0.0, 1.0 );
}`;class Dn extends Pi{constructor(e){super(),this.isShaderMaterial=!0,this.type="ShaderMaterial",this.defines={},this.uniforms={},this.uniformsGroups=[],this.vertexShader=hu,this.fragmentShader=fu,this.linewidth=1,this.wireframe=!1,this.wireframeLinewidth=1,this.fog=!1,this.lights=!1,this.clipping=!1,this.forceSinglePass=!0,this.extensions={clipCullDistance:!1,multiDraw:!1},this.defaultAttributeValues={color:[1,1,1],uv:[0,0],uv1:[0,0]},this.index0AttributeName=void 0,this.uniformsNeedUpdate=!1,this.glslVersion=null,e!==void 0&&this.setValues(e)}copy(e){return super.copy(e),this.fragmentShader=e.fragmentShader,this.vertexShader=e.vertexShader,this.uniforms=Ri(e.uniforms),this.uniformsGroups=uu(e.uniformsGroups),this.defines=Object.assign({},e.defines),this.wireframe=e.wireframe,this.wireframeLinewidth=e.wireframeLinewidth,this.fog=e.fog,this.lights=e.lights,this.clipping=e.clipping,this.extensions=Object.assign({},e.extensions),this.glslVersion=e.glslVersion,this}toJSON(e){const t=super.toJSON(e);t.glslVersion=this.glslVersion,t.uniforms={};for(const r in this.uniforms){const s=this.uniforms[r].value;s&&s.isTexture?t.uniforms[r]={type:"t",value:s.toJSON(e).uuid}:s&&s.isColor?t.uniforms[r]={type:"c",value:s.getHex()}:s&&s.isVector2?t.uniforms[r]={type:"v2",value:s.toArray()}:s&&s.isVector3?t.uniforms[r]={type:"v3",value:s.toArray()}:s&&s.isVector4?t.uniforms[r]={type:"v4",value:s.toArray()}:s&&s.isMatrix3?t.uniforms[r]={type:"m3",value:s.toArray()}:s&&s.isMatrix4?t.uniforms[r]={type:"m4",value:s.toArray()}:t.uniforms[r]={value:s}}Object.keys(this.defines).length>0&&(t.defines=this.defines),t.vertexShader=this.vertexShader,t.fragmentShader=this.fragmentShader,t.lights=this.lights,t.clipping=this.clipping;const i={};for(const r in this.extensions)this.extensions[r]===!0&&(i[r]=!0);return Object.keys(i).length>0&&(t.extensions=i),t}}class Uc extends Et{constructor(){super(),this.isCamera=!0,this.type="Camera",this.matrixWorldInverse=new at,this.projectionMatrix=new at,this.projectionMatrixInverse=new at,this.coordinateSystem=dn}copy(e,t){return super.copy(e,t),this.matrixWorldInverse.copy(e.matrixWorldInverse),this.projectionMatrix.copy(e.projectionMatrix),this.projectionMatrixInverse.copy(e.projectionMatrixInverse),this.coordinateSystem=e.coordinateSystem,this}getWorldDirection(e){return super.getWorldDirection(e).negate()}updateMatrixWorld(e){super.updateMatrixWorld(e),this.matrixWorldInverse.copy(this.matrixWorld).invert()}updateWorldMatrix(e,t){super.updateWorldMatrix(e,t),this.matrixWorldInverse.copy(this.matrixWorld).invert()}clone(){return new this.constructor().copy(this)}}const Sn=new k,Mo=new Xe,So=new Xe;class Bt extends Uc{constructor(e=50,t=1,i=.1,r=2e3){super(),this.isPerspectiveCamera=!0,this.type="PerspectiveCamera",this.fov=e,this.zoom=1,this.near=i,this.far=r,this.focus=10,this.aspect=t,this.view=null,this.filmGauge=35,this.filmOffset=0,this.updateProjectionMatrix()}copy(e,t){return super.copy(e,t),this.fov=e.fov,this.zoom=e.zoom,this.near=e.near,this.far=e.far,this.focus=e.focus,this.aspect=e.aspect,this.view=e.view===null?null:Object.assign({},e.view),this.filmGauge=e.filmGauge,this.filmOffset=e.filmOffset,this}setFocalLength(e){const t=.5*this.getFilmHeight()/e;this.fov=gs*2*Math.atan(t),this.updateProjectionMatrix()}getFocalLength(){const e=Math.tan(Lr*.5*this.fov);return .5*this.getFilmHeight()/e}getEffectiveFOV(){return gs*2*Math.atan(Math.tan(Lr*.5*this.fov)/this.zoom)}getFilmWidth(){return this.filmGauge*Math.min(this.aspect,1)}getFilmHeight(){return this.filmGauge/Math.max(this.aspect,1)}getViewBounds(e,t,i){Sn.set(-1,-1,.5).applyMatrix4(this.projectionMatrixInverse),t.set(Sn.x,Sn.y).multiplyScalar(-e/Sn.z),Sn.set(1,1,.5).applyMatrix4(this.projectionMatrixInverse),i.set(Sn.x,Sn.y).multiplyScalar(-e/Sn.z)}getViewSize(e,t){return this.getViewBounds(e,Mo,So),t.subVectors(So,Mo)}setViewOffset(e,t,i,r,a,s){this.aspect=e/t,this.view===null&&(this.view={enabled:!0,fullWidth:1,fullHeight:1,offsetX:0,offsetY:0,width:1,height:1}),this.view.enabled=!0,this.view.fullWidth=e,this.view.fullHeight=t,this.view.offsetX=i,this.view.offsetY=r,this.view.width=a,this.view.height=s,this.updateProjectionMatrix()}clearViewOffset(){this.view!==null&&(this.view.enabled=!1),this.updateProjectionMatrix()}updateProjectionMatrix(){const e=this.near;let t=e*Math.tan(Lr*.5*this.fov)/this.zoom,i=2*t,r=this.aspect*i,a=-.5*r;const s=this.view;if(this.view!==null&&this.view.enabled){const c=s.fullWidth,l=s.fullHeight;a+=s.offsetX*r/c,t-=s.offsetY*i/l,r*=s.width/c,i*=s.height/l}const o=this.filmOffset;o!==0&&(a+=e*o/this.getFilmWidth()),this.projectionMatrix.makePerspective(a,a+r,t,t-i,e,this.far,this.coordinateSystem),this.projectionMatrixInverse.copy(this.projectionMatrix).invert()}toJSON(e){const t=super.toJSON(e);return t.object.fov=this.fov,t.object.zoom=this.zoom,t.object.near=this.near,t.object.far=this.far,t.object.focus=this.focus,t.object.aspect=this.aspect,this.view!==null&&(t.object.view=Object.assign({},this.view)),t.object.filmGauge=this.filmGauge,t.object.filmOffset=this.filmOffset,t}}const di=-90,hi=1;class pu extends Et{constructor(e,t,i){super(),this.type="CubeCamera",this.renderTarget=i,this.coordinateSystem=null,this.activeMipmapLevel=0;const r=new Bt(di,hi,e,t);r.layers=this.layers,this.add(r);const a=new Bt(di,hi,e,t);a.layers=this.layers,this.add(a);const s=new Bt(di,hi,e,t);s.layers=this.layers,this.add(s);const o=new Bt(di,hi,e,t);o.layers=this.layers,this.add(o);const c=new Bt(di,hi,e,t);c.layers=this.layers,this.add(c);const l=new Bt(di,hi,e,t);l.layers=this.layers,this.add(l)}updateCoordinateSystem(){const e=this.coordinateSystem,t=this.children.concat(),[i,r,a,s,o,c]=t;for(const l of t)this.remove(l);if(e===dn)i.up.set(0,1,0),i.lookAt(1,0,0),r.up.set(0,1,0),r.lookAt(-1,0,0),a.up.set(0,0,-1),a.lookAt(0,1,0),s.up.set(0,0,1),s.lookAt(0,-1,0),o.up.set(0,1,0),o.lookAt(0,0,1),c.up.set(0,1,0),c.lookAt(0,0,-1);else if(e===Nr)i.up.set(0,-1,0),i.lookAt(-1,0,0),r.up.set(0,-1,0),r.lookAt(1,0,0),a.up.set(0,0,1),a.lookAt(0,1,0),s.up.set(0,0,-1),s.lookAt(0,-1,0),o.up.set(0,-1,0),o.lookAt(0,0,1),c.up.set(0,-1,0),c.lookAt(0,0,-1);else throw new Error("THREE.CubeCamera.updateCoordinateSystem(): Invalid coordinate system: "+e);for(const l of t)this.add(l),l.updateMatrixWorld()}update(e,t){this.parent===null&&this.updateMatrixWorld();const{renderTarget:i,activeMipmapLevel:r}=this;this.coordinateSystem!==e.coordinateSystem&&(this.coordinateSystem=e.coordinateSystem,this.updateCoordinateSystem());const[a,s,o,c,l,d]=this.children,h=e.getRenderTarget(),f=e.getActiveCubeFace(),m=e.getActiveMipmapLevel(),g=e.xr.enabled;e.xr.enabled=!1;const _=i.texture.generateMipmaps;i.texture.generateMipmaps=!1,e.setRenderTarget(i,0,r),e.render(t,a),e.setRenderTarget(i,1,r),e.render(t,s),e.setRenderTarget(i,2,r),e.render(t,o),e.setRenderTarget(i,3,r),e.render(t,c),e.setRenderTarget(i,4,r),e.render(t,l),i.texture.generateMipmaps=_,e.setRenderTarget(i,5,r),e.render(t,d),e.setRenderTarget(h,f,m),e.xr.enabled=g,i.texture.needsPMREMUpdate=!0}}class zc extends Rt{constructor(e,t,i,r,a,s,o,c,l,d){e=e!==void 0?e:[],t=t!==void 0?t:yi,super(e,t,i,r,a,s,o,c,l,d),this.isCubeTexture=!0,this.flipY=!1}get images(){return this.image}set images(e){this.image=e}}class mu extends Jn{constructor(e=1,t={}){super(e,e,t),this.isWebGLCubeRenderTarget=!0;const i={width:e,height:e,depth:1},r=[i,i,i,i,i,i];this.texture=new zc(r,t.mapping,t.wrapS,t.wrapT,t.magFilter,t.minFilter,t.format,t.type,t.anisotropy,t.colorSpace),this.texture.isRenderTargetTexture=!0,this.texture.generateMipmaps=t.generateMipmaps!==void 0?t.generateMipmaps:!1,this.texture.minFilter=t.minFilter!==void 0?t.minFilter:Zt}fromEquirectangularTexture(e,t){this.texture.type=t.type,this.texture.colorSpace=t.colorSpace,this.texture.generateMipmaps=t.generateMipmaps,this.texture.minFilter=t.minFilter,this.texture.magFilter=t.magFilter;const i={uniforms:{tEquirect:{value:null}},vertexShader:`

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
			`},r=new hn(5,5,5),a=new Dn({name:"CubemapFromEquirect",uniforms:Ri(i.uniforms),vertexShader:i.vertexShader,fragmentShader:i.fragmentShader,side:Dt,blending:Rn});a.uniforms.tEquirect.value=t;const s=new je(r,a),o=t.minFilter;return t.minFilter===Yn&&(t.minFilter=Zt),new pu(1,10,this).update(e,s),t.minFilter=o,s.geometry.dispose(),s.material.dispose(),this}clear(e,t,i,r){const a=e.getRenderTarget();for(let s=0;s<6;s++)e.setRenderTarget(this,s),e.clear(t,i,r);e.setRenderTarget(a)}}class nt extends Et{constructor(){super(),this.isGroup=!0,this.type="Group"}}const gu={type:"move"};class pa{constructor(){this._targetRay=null,this._grip=null,this._hand=null}getHandSpace(){return this._hand===null&&(this._hand=new nt,this._hand.matrixAutoUpdate=!1,this._hand.visible=!1,this._hand.joints={},this._hand.inputState={pinching:!1}),this._hand}getTargetRaySpace(){return this._targetRay===null&&(this._targetRay=new nt,this._targetRay.matrixAutoUpdate=!1,this._targetRay.visible=!1,this._targetRay.hasLinearVelocity=!1,this._targetRay.linearVelocity=new k,this._targetRay.hasAngularVelocity=!1,this._targetRay.angularVelocity=new k),this._targetRay}getGripSpace(){return this._grip===null&&(this._grip=new nt,this._grip.matrixAutoUpdate=!1,this._grip.visible=!1,this._grip.hasLinearVelocity=!1,this._grip.linearVelocity=new k,this._grip.hasAngularVelocity=!1,this._grip.angularVelocity=new k),this._grip}dispatchEvent(e){return this._targetRay!==null&&this._targetRay.dispatchEvent(e),this._grip!==null&&this._grip.dispatchEvent(e),this._hand!==null&&this._hand.dispatchEvent(e),this}connect(e){if(e&&e.hand){const t=this._hand;if(t)for(const i of e.hand.values())this._getHandJoint(t,i)}return this.dispatchEvent({type:"connected",data:e}),this}disconnect(e){return this.dispatchEvent({type:"disconnected",data:e}),this._targetRay!==null&&(this._targetRay.visible=!1),this._grip!==null&&(this._grip.visible=!1),this._hand!==null&&(this._hand.visible=!1),this}update(e,t,i){let r=null,a=null,s=null;const o=this._targetRay,c=this._grip,l=this._hand;if(e&&t.session.visibilityState!=="visible-blurred"){if(l&&e.hand){s=!0;for(const _ of e.hand.values()){const p=t.getJointPose(_,i),u=this._getHandJoint(l,_);p!==null&&(u.matrix.fromArray(p.transform.matrix),u.matrix.decompose(u.position,u.rotation,u.scale),u.matrixWorldNeedsUpdate=!0,u.jointRadius=p.radius),u.visible=p!==null}const d=l.joints["index-finger-tip"],h=l.joints["thumb-tip"],f=d.position.distanceTo(h.position),m=.02,g=.005;l.inputState.pinching&&f>m+g?(l.inputState.pinching=!1,this.dispatchEvent({type:"pinchend",handedness:e.handedness,target:this})):!l.inputState.pinching&&f<=m-g&&(l.inputState.pinching=!0,this.dispatchEvent({type:"pinchstart",handedness:e.handedness,target:this}))}else c!==null&&e.gripSpace&&(a=t.getPose(e.gripSpace,i),a!==null&&(c.matrix.fromArray(a.transform.matrix),c.matrix.decompose(c.position,c.rotation,c.scale),c.matrixWorldNeedsUpdate=!0,a.linearVelocity?(c.hasLinearVelocity=!0,c.linearVelocity.copy(a.linearVelocity)):c.hasLinearVelocity=!1,a.angularVelocity?(c.hasAngularVelocity=!0,c.angularVelocity.copy(a.angularVelocity)):c.hasAngularVelocity=!1));o!==null&&(r=t.getPose(e.targetRaySpace,i),r===null&&a!==null&&(r=a),r!==null&&(o.matrix.fromArray(r.transform.matrix),o.matrix.decompose(o.position,o.rotation,o.scale),o.matrixWorldNeedsUpdate=!0,r.linearVelocity?(o.hasLinearVelocity=!0,o.linearVelocity.copy(r.linearVelocity)):o.hasLinearVelocity=!1,r.angularVelocity?(o.hasAngularVelocity=!0,o.angularVelocity.copy(r.angularVelocity)):o.hasAngularVelocity=!1,this.dispatchEvent(gu)))}return o!==null&&(o.visible=r!==null),c!==null&&(c.visible=a!==null),l!==null&&(l.visible=s!==null),this}_getHandJoint(e,t){if(e.joints[t.jointName]===void 0){const i=new nt;i.matrixAutoUpdate=!1,i.visible=!1,e.joints[t.jointName]=i,e.add(i)}return e.joints[t.jointName]}}class _u extends Et{constructor(){super(),this.isScene=!0,this.type="Scene",this.background=null,this.environment=null,this.fog=null,this.backgroundBlurriness=0,this.backgroundIntensity=1,this.backgroundRotation=new Mt,this.environmentIntensity=1,this.environmentRotation=new Mt,this.overrideMaterial=null,typeof __THREE_DEVTOOLS__<"u"&&__THREE_DEVTOOLS__.dispatchEvent(new CustomEvent("observe",{detail:this}))}copy(e,t){return super.copy(e,t),e.background!==null&&(this.background=e.background.clone()),e.environment!==null&&(this.environment=e.environment.clone()),e.fog!==null&&(this.fog=e.fog.clone()),this.backgroundBlurriness=e.backgroundBlurriness,this.backgroundIntensity=e.backgroundIntensity,this.backgroundRotation.copy(e.backgroundRotation),this.environmentIntensity=e.environmentIntensity,this.environmentRotation.copy(e.environmentRotation),e.overrideMaterial!==null&&(this.overrideMaterial=e.overrideMaterial.clone()),this.matrixAutoUpdate=e.matrixAutoUpdate,this}toJSON(e){const t=super.toJSON(e);return this.fog!==null&&(t.object.fog=this.fog.toJSON()),this.backgroundBlurriness>0&&(t.object.backgroundBlurriness=this.backgroundBlurriness),this.backgroundIntensity!==1&&(t.object.backgroundIntensity=this.backgroundIntensity),t.object.backgroundRotation=this.backgroundRotation.toArray(),this.environmentIntensity!==1&&(t.object.environmentIntensity=this.environmentIntensity),t.object.environmentRotation=this.environmentRotation.toArray(),t}}const ma=new k,vu=new k,xu=new Be;class Vn{constructor(e=new k(1,0,0),t=0){this.isPlane=!0,this.normal=e,this.constant=t}set(e,t){return this.normal.copy(e),this.constant=t,this}setComponents(e,t,i,r){return this.normal.set(e,t,i),this.constant=r,this}setFromNormalAndCoplanarPoint(e,t){return this.normal.copy(e),this.constant=-t.dot(this.normal),this}setFromCoplanarPoints(e,t,i){const r=ma.subVectors(i,t).cross(vu.subVectors(e,t)).normalize();return this.setFromNormalAndCoplanarPoint(r,e),this}copy(e){return this.normal.copy(e.normal),this.constant=e.constant,this}normalize(){const e=1/this.normal.length();return this.normal.multiplyScalar(e),this.constant*=e,this}negate(){return this.constant*=-1,this.normal.negate(),this}distanceToPoint(e){return this.normal.dot(e)+this.constant}distanceToSphere(e){return this.distanceToPoint(e.center)-e.radius}projectPoint(e,t){return t.copy(e).addScaledVector(this.normal,-this.distanceToPoint(e))}intersectLine(e,t){const i=e.delta(ma),r=this.normal.dot(i);if(r===0)return this.distanceToPoint(e.start)===0?t.copy(e.start):null;const a=-(e.start.dot(this.normal)+this.constant)/r;return a<0||a>1?null:t.copy(e.start).addScaledVector(i,a)}intersectsLine(e){const t=this.distanceToPoint(e.start),i=this.distanceToPoint(e.end);return t<0&&i>0||i<0&&t>0}intersectsBox(e){return e.intersectsPlane(this)}intersectsSphere(e){return e.intersectsPlane(this)}coplanarPoint(e){return e.copy(this.normal).multiplyScalar(-this.constant)}applyMatrix4(e,t){const i=t||xu.getNormalMatrix(e),r=this.coplanarPoint(ma).applyMatrix4(e),a=this.normal.applyMatrix3(i).normalize();return this.constant=-r.dot(a),this}translate(e){return this.constant-=e.dot(this.normal),this}equals(e){return e.normal.equals(this.normal)&&e.constant===this.constant}clone(){return new this.constructor().copy(this)}}const Fn=new Hr,_r=new k;class Is{constructor(e=new Vn,t=new Vn,i=new Vn,r=new Vn,a=new Vn,s=new Vn){this.planes=[e,t,i,r,a,s]}set(e,t,i,r,a,s){const o=this.planes;return o[0].copy(e),o[1].copy(t),o[2].copy(i),o[3].copy(r),o[4].copy(a),o[5].copy(s),this}copy(e){const t=this.planes;for(let i=0;i<6;i++)t[i].copy(e.planes[i]);return this}setFromProjectionMatrix(e,t=dn){const i=this.planes,r=e.elements,a=r[0],s=r[1],o=r[2],c=r[3],l=r[4],d=r[5],h=r[6],f=r[7],m=r[8],g=r[9],_=r[10],p=r[11],u=r[12],y=r[13],S=r[14],M=r[15];if(i[0].setComponents(c-a,f-l,p-m,M-u).normalize(),i[1].setComponents(c+a,f+l,p+m,M+u).normalize(),i[2].setComponents(c+s,f+d,p+g,M+y).normalize(),i[3].setComponents(c-s,f-d,p-g,M-y).normalize(),i[4].setComponents(c-o,f-h,p-_,M-S).normalize(),t===dn)i[5].setComponents(c+o,f+h,p+_,M+S).normalize();else if(t===Nr)i[5].setComponents(o,h,_,S).normalize();else throw new Error("THREE.Frustum.setFromProjectionMatrix(): Invalid coordinate system: "+t);return this}intersectsObject(e){if(e.boundingSphere!==void 0)e.boundingSphere===null&&e.computeBoundingSphere(),Fn.copy(e.boundingSphere).applyMatrix4(e.matrixWorld);else{const t=e.geometry;t.boundingSphere===null&&t.computeBoundingSphere(),Fn.copy(t.boundingSphere).applyMatrix4(e.matrixWorld)}return this.intersectsSphere(Fn)}intersectsSprite(e){return Fn.center.set(0,0,0),Fn.radius=.7071067811865476,Fn.applyMatrix4(e.matrixWorld),this.intersectsSphere(Fn)}intersectsSphere(e){const t=this.planes,i=e.center,r=-e.radius;for(let a=0;a<6;a++)if(t[a].distanceToPoint(i)<r)return!1;return!0}intersectsBox(e){const t=this.planes;for(let i=0;i<6;i++){const r=t[i];if(_r.x=r.normal.x>0?e.max.x:e.min.x,_r.y=r.normal.y>0?e.max.y:e.min.y,_r.z=r.normal.z>0?e.max.z:e.min.z,r.distanceToPoint(_r)<0)return!1}return!0}containsPoint(e){const t=this.planes;for(let i=0;i<6;i++)if(t[i].distanceToPoint(e)<0)return!1;return!0}clone(){return new this.constructor().copy(this)}}class ht extends Pi{constructor(e){super(),this.isLineBasicMaterial=!0,this.type="LineBasicMaterial",this.color=new ce(16777215),this.map=null,this.linewidth=1,this.linecap="round",this.linejoin="round",this.fog=!0,this.setValues(e)}copy(e){return super.copy(e),this.color.copy(e.color),this.map=e.map,this.linewidth=e.linewidth,this.linecap=e.linecap,this.linejoin=e.linejoin,this.fog=e.fog,this}}const kr=new k,Or=new k,Eo=new at,Bi=new Ds,vr=new Hr,ga=new k,yo=new k;class Gi extends Et{constructor(e=new Ye,t=new ht){super(),this.isLine=!0,this.type="Line",this.geometry=e,this.material=t,this.morphTargetDictionary=void 0,this.morphTargetInfluences=void 0,this.updateMorphTargets()}copy(e,t){return super.copy(e,t),this.material=Array.isArray(e.material)?e.material.slice():e.material,this.geometry=e.geometry,this}computeLineDistances(){const e=this.geometry;if(e.index===null){const t=e.attributes.position,i=[0];for(let r=1,a=t.count;r<a;r++)kr.fromBufferAttribute(t,r-1),Or.fromBufferAttribute(t,r),i[r]=i[r-1],i[r]+=kr.distanceTo(Or);e.setAttribute("lineDistance",new Ge(i,1))}else console.warn("THREE.Line.computeLineDistances(): Computation only possible with non-indexed BufferGeometry.");return this}raycast(e,t){const i=this.geometry,r=this.matrixWorld,a=e.params.Line.threshold,s=i.drawRange;if(i.boundingSphere===null&&i.computeBoundingSphere(),vr.copy(i.boundingSphere),vr.applyMatrix4(r),vr.radius+=a,e.ray.intersectsSphere(vr)===!1)return;Eo.copy(r).invert(),Bi.copy(e.ray).applyMatrix4(Eo);const o=a/((this.scale.x+this.scale.y+this.scale.z)/3),c=o*o,l=this.isLineSegments?2:1,d=i.index,f=i.attributes.position;if(d!==null){const m=Math.max(0,s.start),g=Math.min(d.count,s.start+s.count);for(let _=m,p=g-1;_<p;_+=l){const u=d.getX(_),y=d.getX(_+1),S=xr(this,e,Bi,c,u,y,_);S&&t.push(S)}if(this.isLineLoop){const _=d.getX(g-1),p=d.getX(m),u=xr(this,e,Bi,c,_,p,g-1);u&&t.push(u)}}else{const m=Math.max(0,s.start),g=Math.min(f.count,s.start+s.count);for(let _=m,p=g-1;_<p;_+=l){const u=xr(this,e,Bi,c,_,_+1,_);u&&t.push(u)}if(this.isLineLoop){const _=xr(this,e,Bi,c,g-1,m,g-1);_&&t.push(_)}}}updateMorphTargets(){const t=this.geometry.morphAttributes,i=Object.keys(t);if(i.length>0){const r=t[i[0]];if(r!==void 0){this.morphTargetInfluences=[],this.morphTargetDictionary={};for(let a=0,s=r.length;a<s;a++){const o=r[a].name||String(a);this.morphTargetInfluences.push(0),this.morphTargetDictionary[o]=a}}}}}function xr(n,e,t,i,r,a,s){const o=n.geometry.attributes.position;if(kr.fromBufferAttribute(o,r),Or.fromBufferAttribute(o,a),t.distanceSqToSegment(kr,Or,ga,yo)>i)return;ga.applyMatrix4(n.matrixWorld);const l=e.ray.origin.distanceTo(ga);if(!(l<e.near||l>e.far))return{distance:l,point:yo.clone().applyMatrix4(n.matrixWorld),index:s,face:null,faceIndex:null,barycoord:null,object:n}}const bo=new k,To=new k;class gt extends Gi{constructor(e,t){super(e,t),this.isLineSegments=!0,this.type="LineSegments"}computeLineDistances(){const e=this.geometry;if(e.index===null){const t=e.attributes.position,i=[];for(let r=0,a=t.count;r<a;r+=2)bo.fromBufferAttribute(t,r),To.fromBufferAttribute(t,r+1),i[r]=r===0?0:i[r-1],i[r+1]=i[r]+bo.distanceTo(To);e.setAttribute("lineDistance",new Ge(i,1))}else console.warn("THREE.LineSegments.computeLineDistances(): Computation only possible with non-indexed BufferGeometry.");return this}}class Nc extends Rt{constructor(e,t,i,r,a,s,o,c,l,d=Mi){if(d!==Mi&&d!==Ai)throw new Error("DepthTexture format must be either THREE.DepthFormat or THREE.DepthStencilFormat");i===void 0&&d===Mi&&(i=Zn),i===void 0&&d===Ai&&(i=Ti),super(null,r,a,s,o,c,d,i,l),this.isDepthTexture=!0,this.image={width:e,height:t},this.magFilter=o!==void 0?o:Kt,this.minFilter=c!==void 0?c:Kt,this.flipY=!1,this.generateMipmaps=!1,this.compareFunction=null}copy(e){return super.copy(e),this.source=new Ps(Object.assign({},e.image)),this.compareFunction=e.compareFunction,this}toJSON(e){const t=super.toJSON(e);return this.compareFunction!==null&&(t.compareFunction=this.compareFunction),t}}class Zi extends Ye{constructor(e=1,t=1,i=1,r=32,a=1,s=!1,o=0,c=Math.PI*2){super(),this.type="CylinderGeometry",this.parameters={radiusTop:e,radiusBottom:t,height:i,radialSegments:r,heightSegments:a,openEnded:s,thetaStart:o,thetaLength:c};const l=this;r=Math.floor(r),a=Math.floor(a);const d=[],h=[],f=[],m=[];let g=0;const _=[],p=i/2;let u=0;y(),s===!1&&(e>0&&S(!0),t>0&&S(!1)),this.setIndex(d),this.setAttribute("position",new Ge(h,3)),this.setAttribute("normal",new Ge(f,3)),this.setAttribute("uv",new Ge(m,2));function y(){const M=new k,T=new k;let b=0;const w=(t-e)/i;for(let L=0;L<=a;L++){const x=[],v=L/a,R=v*(t-e)+e;for(let U=0;U<=r;U++){const C=U/r,P=C*c+o,F=Math.sin(P),N=Math.cos(P);T.x=R*F,T.y=-v*i+p,T.z=R*N,h.push(T.x,T.y,T.z),M.set(F,w,N).normalize(),f.push(M.x,M.y,M.z),m.push(C,1-v),x.push(g++)}_.push(x)}for(let L=0;L<r;L++)for(let x=0;x<a;x++){const v=_[x][L],R=_[x+1][L],U=_[x+1][L+1],C=_[x][L+1];(e>0||x!==0)&&(d.push(v,R,C),b+=3),(t>0||x!==a-1)&&(d.push(R,U,C),b+=3)}l.addGroup(u,b,0),u+=b}function S(M){const T=g,b=new Xe,w=new k;let L=0;const x=M===!0?e:t,v=M===!0?1:-1;for(let U=1;U<=r;U++)h.push(0,p*v,0),f.push(0,v,0),m.push(.5,.5),g++;const R=g;for(let U=0;U<=r;U++){const P=U/r*c+o,F=Math.cos(P),N=Math.sin(P);w.x=x*N,w.y=p*v,w.z=x*F,h.push(w.x,w.y,w.z),f.push(0,v,0),b.x=F*.5+.5,b.y=N*.5*v+.5,m.push(b.x,b.y),g++}for(let U=0;U<r;U++){const C=T+U,P=R+U;M===!0?d.push(P,P+1,C):d.push(P+1,P,C),L+=3}l.addGroup(u,L,M===!0?1:2),u+=L}}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}static fromJSON(e){return new Zi(e.radiusTop,e.radiusBottom,e.height,e.radialSegments,e.heightSegments,e.openEnded,e.thetaStart,e.thetaLength)}}class Us extends Zi{constructor(e=1,t=1,i=32,r=1,a=!1,s=0,o=Math.PI*2){super(0,e,t,i,r,a,s,o),this.type="ConeGeometry",this.parameters={radius:e,height:t,radialSegments:i,heightSegments:r,openEnded:a,thetaStart:s,thetaLength:o}}static fromJSON(e){return new Us(e.radius,e.height,e.radialSegments,e.heightSegments,e.openEnded,e.thetaStart,e.thetaLength)}}const Mr=new k,Sr=new k,_a=new k,Er=new Vt;class Br extends Ye{constructor(e=null,t=1){if(super(),this.type="EdgesGeometry",this.parameters={geometry:e,thresholdAngle:t},e!==null){const r=Math.pow(10,4),a=Math.cos(Lr*t),s=e.getIndex(),o=e.getAttribute("position"),c=s?s.count:o.count,l=[0,0,0],d=["a","b","c"],h=new Array(3),f={},m=[];for(let g=0;g<c;g+=3){s?(l[0]=s.getX(g),l[1]=s.getX(g+1),l[2]=s.getX(g+2)):(l[0]=g,l[1]=g+1,l[2]=g+2);const{a:_,b:p,c:u}=Er;if(_.fromBufferAttribute(o,l[0]),p.fromBufferAttribute(o,l[1]),u.fromBufferAttribute(o,l[2]),Er.getNormal(_a),h[0]=`${Math.round(_.x*r)},${Math.round(_.y*r)},${Math.round(_.z*r)}`,h[1]=`${Math.round(p.x*r)},${Math.round(p.y*r)},${Math.round(p.z*r)}`,h[2]=`${Math.round(u.x*r)},${Math.round(u.y*r)},${Math.round(u.z*r)}`,!(h[0]===h[1]||h[1]===h[2]||h[2]===h[0]))for(let y=0;y<3;y++){const S=(y+1)%3,M=h[y],T=h[S],b=Er[d[y]],w=Er[d[S]],L=`${M}_${T}`,x=`${T}_${M}`;x in f&&f[x]?(_a.dot(f[x].normal)<=a&&(m.push(b.x,b.y,b.z),m.push(w.x,w.y,w.z)),f[x]=null):L in f||(f[L]={index0:l[y],index1:l[S],normal:_a.clone()})}}for(const g in f)if(f[g]){const{index0:_,index1:p}=f[g];Mr.fromBufferAttribute(o,_),Sr.fromBufferAttribute(o,p),m.push(Mr.x,Mr.y,Mr.z),m.push(Sr.x,Sr.y,Sr.z)}this.setAttribute("position",new Ge(m,3))}}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}}class Li extends Ye{constructor(e=1,t=1,i=1,r=1){super(),this.type="PlaneGeometry",this.parameters={width:e,height:t,widthSegments:i,heightSegments:r};const a=e/2,s=t/2,o=Math.floor(i),c=Math.floor(r),l=o+1,d=c+1,h=e/o,f=t/c,m=[],g=[],_=[],p=[];for(let u=0;u<d;u++){const y=u*f-s;for(let S=0;S<l;S++){const M=S*h-a;g.push(M,-y,0),_.push(0,0,1),p.push(S/o),p.push(1-u/c)}}for(let u=0;u<c;u++)for(let y=0;y<o;y++){const S=y+l*u,M=y+l*(u+1),T=y+1+l*(u+1),b=y+1+l*u;m.push(S,M,b),m.push(M,T,b)}this.setIndex(m),this.setAttribute("position",new Ge(g,3)),this.setAttribute("normal",new Ge(_,3)),this.setAttribute("uv",new Ge(p,2))}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}static fromJSON(e){return new Li(e.width,e.height,e.widthSegments,e.heightSegments)}}class zs extends Ye{constructor(e=.5,t=1,i=32,r=1,a=0,s=Math.PI*2){super(),this.type="RingGeometry",this.parameters={innerRadius:e,outerRadius:t,thetaSegments:i,phiSegments:r,thetaStart:a,thetaLength:s},i=Math.max(3,i),r=Math.max(1,r);const o=[],c=[],l=[],d=[];let h=e;const f=(t-e)/r,m=new k,g=new Xe;for(let _=0;_<=r;_++){for(let p=0;p<=i;p++){const u=a+p/i*s;m.x=h*Math.cos(u),m.y=h*Math.sin(u),c.push(m.x,m.y,m.z),l.push(0,0,1),g.x=(m.x/t+1)/2,g.y=(m.y/t+1)/2,d.push(g.x,g.y)}h+=f}for(let _=0;_<r;_++){const p=_*(i+1);for(let u=0;u<i;u++){const y=u+p,S=y,M=y+i+1,T=y+i+2,b=y+1;o.push(S,M,b),o.push(M,T,b)}}this.setIndex(o),this.setAttribute("position",new Ge(c,3)),this.setAttribute("normal",new Ge(l,3)),this.setAttribute("uv",new Ge(d,2))}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}static fromJSON(e){return new zs(e.innerRadius,e.outerRadius,e.thetaSegments,e.phiSegments,e.thetaStart,e.thetaLength)}}class mn extends Ye{constructor(e=1,t=32,i=16,r=0,a=Math.PI*2,s=0,o=Math.PI){super(),this.type="SphereGeometry",this.parameters={radius:e,widthSegments:t,heightSegments:i,phiStart:r,phiLength:a,thetaStart:s,thetaLength:o},t=Math.max(3,Math.floor(t)),i=Math.max(2,Math.floor(i));const c=Math.min(s+o,Math.PI);let l=0;const d=[],h=new k,f=new k,m=[],g=[],_=[],p=[];for(let u=0;u<=i;u++){const y=[],S=u/i;let M=0;u===0&&s===0?M=.5/t:u===i&&c===Math.PI&&(M=-.5/t);for(let T=0;T<=t;T++){const b=T/t;h.x=-e*Math.cos(r+b*a)*Math.sin(s+S*o),h.y=e*Math.cos(s+S*o),h.z=e*Math.sin(r+b*a)*Math.sin(s+S*o),g.push(h.x,h.y,h.z),f.copy(h).normalize(),_.push(f.x,f.y,f.z),p.push(b+M,1-S),y.push(l++)}d.push(y)}for(let u=0;u<i;u++)for(let y=0;y<t;y++){const S=d[u][y+1],M=d[u][y],T=d[u+1][y],b=d[u+1][y+1];(u!==0||s>0)&&m.push(S,M,b),(u!==i-1||c<Math.PI)&&m.push(M,T,b)}this.setIndex(m),this.setAttribute("position",new Ge(g,3)),this.setAttribute("normal",new Ge(_,3)),this.setAttribute("uv",new Ge(p,2))}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}static fromJSON(e){return new mn(e.radius,e.widthSegments,e.heightSegments,e.phiStart,e.phiLength,e.thetaStart,e.thetaLength)}}class ct extends Pi{constructor(e){super(),this.isMeshStandardMaterial=!0,this.type="MeshStandardMaterial",this.defines={STANDARD:""},this.color=new ce(16777215),this.roughness=1,this.metalness=0,this.map=null,this.lightMap=null,this.lightMapIntensity=1,this.aoMap=null,this.aoMapIntensity=1,this.emissive=new ce(0),this.emissiveIntensity=1,this.emissiveMap=null,this.bumpMap=null,this.bumpScale=1,this.normalMap=null,this.normalMapType=Ac,this.normalScale=new Xe(1,1),this.displacementMap=null,this.displacementScale=1,this.displacementBias=0,this.roughnessMap=null,this.metalnessMap=null,this.alphaMap=null,this.envMap=null,this.envMapRotation=new Mt,this.envMapIntensity=1,this.wireframe=!1,this.wireframeLinewidth=1,this.wireframeLinecap="round",this.wireframeLinejoin="round",this.flatShading=!1,this.fog=!0,this.setValues(e)}copy(e){return super.copy(e),this.defines={STANDARD:""},this.color.copy(e.color),this.roughness=e.roughness,this.metalness=e.metalness,this.map=e.map,this.lightMap=e.lightMap,this.lightMapIntensity=e.lightMapIntensity,this.aoMap=e.aoMap,this.aoMapIntensity=e.aoMapIntensity,this.emissive.copy(e.emissive),this.emissiveMap=e.emissiveMap,this.emissiveIntensity=e.emissiveIntensity,this.bumpMap=e.bumpMap,this.bumpScale=e.bumpScale,this.normalMap=e.normalMap,this.normalMapType=e.normalMapType,this.normalScale.copy(e.normalScale),this.displacementMap=e.displacementMap,this.displacementScale=e.displacementScale,this.displacementBias=e.displacementBias,this.roughnessMap=e.roughnessMap,this.metalnessMap=e.metalnessMap,this.alphaMap=e.alphaMap,this.envMap=e.envMap,this.envMapRotation.copy(e.envMapRotation),this.envMapIntensity=e.envMapIntensity,this.wireframe=e.wireframe,this.wireframeLinewidth=e.wireframeLinewidth,this.wireframeLinecap=e.wireframeLinecap,this.wireframeLinejoin=e.wireframeLinejoin,this.flatShading=e.flatShading,this.fog=e.fog,this}}class Mu extends Pi{constructor(e){super(),this.isMeshDepthMaterial=!0,this.type="MeshDepthMaterial",this.depthPacking=Ll,this.map=null,this.alphaMap=null,this.displacementMap=null,this.displacementScale=1,this.displacementBias=0,this.wireframe=!1,this.wireframeLinewidth=1,this.setValues(e)}copy(e){return super.copy(e),this.depthPacking=e.depthPacking,this.map=e.map,this.alphaMap=e.alphaMap,this.displacementMap=e.displacementMap,this.displacementScale=e.displacementScale,this.displacementBias=e.displacementBias,this.wireframe=e.wireframe,this.wireframeLinewidth=e.wireframeLinewidth,this}}class Su extends Pi{constructor(e){super(),this.isMeshDistanceMaterial=!0,this.type="MeshDistanceMaterial",this.map=null,this.alphaMap=null,this.displacementMap=null,this.displacementScale=1,this.displacementBias=0,this.setValues(e)}copy(e){return super.copy(e),this.map=e.map,this.alphaMap=e.alphaMap,this.displacementMap=e.displacementMap,this.displacementScale=e.displacementScale,this.displacementBias=e.displacementBias,this}}class Eu extends ht{constructor(e){super(),this.isLineDashedMaterial=!0,this.type="LineDashedMaterial",this.scale=1,this.dashSize=3,this.gapSize=1,this.setValues(e)}copy(e){return super.copy(e),this.scale=e.scale,this.dashSize=e.dashSize,this.gapSize=e.gapSize,this}}class Fc extends Et{constructor(e,t=1){super(),this.isLight=!0,this.type="Light",this.color=new ce(e),this.intensity=t}dispose(){}copy(e,t){return super.copy(e,t),this.color.copy(e.color),this.intensity=e.intensity,this}toJSON(e){const t=super.toJSON(e);return t.object.color=this.color.getHex(),t.object.intensity=this.intensity,this.groundColor!==void 0&&(t.object.groundColor=this.groundColor.getHex()),this.distance!==void 0&&(t.object.distance=this.distance),this.angle!==void 0&&(t.object.angle=this.angle),this.decay!==void 0&&(t.object.decay=this.decay),this.penumbra!==void 0&&(t.object.penumbra=this.penumbra),this.shadow!==void 0&&(t.object.shadow=this.shadow.toJSON()),this.target!==void 0&&(t.object.target=this.target.uuid),t}}const va=new at,Ao=new k,wo=new k;class yu{constructor(e){this.camera=e,this.intensity=1,this.bias=0,this.normalBias=0,this.radius=1,this.blurSamples=8,this.mapSize=new Xe(512,512),this.map=null,this.mapPass=null,this.matrix=new at,this.autoUpdate=!0,this.needsUpdate=!1,this._frustum=new Is,this._frameExtents=new Xe(1,1),this._viewportCount=1,this._viewports=[new dt(0,0,1,1)]}getViewportCount(){return this._viewportCount}getFrustum(){return this._frustum}updateMatrices(e){const t=this.camera,i=this.matrix;Ao.setFromMatrixPosition(e.matrixWorld),t.position.copy(Ao),wo.setFromMatrixPosition(e.target.matrixWorld),t.lookAt(wo),t.updateMatrixWorld(),va.multiplyMatrices(t.projectionMatrix,t.matrixWorldInverse),this._frustum.setFromProjectionMatrix(va),i.set(.5,0,0,.5,0,.5,0,.5,0,0,.5,.5,0,0,0,1),i.multiply(va)}getViewport(e){return this._viewports[e]}getFrameExtents(){return this._frameExtents}dispose(){this.map&&this.map.dispose(),this.mapPass&&this.mapPass.dispose()}copy(e){return this.camera=e.camera.clone(),this.intensity=e.intensity,this.bias=e.bias,this.radius=e.radius,this.mapSize.copy(e.mapSize),this}clone(){return new this.constructor().copy(this)}toJSON(){const e={};return this.intensity!==1&&(e.intensity=this.intensity),this.bias!==0&&(e.bias=this.bias),this.normalBias!==0&&(e.normalBias=this.normalBias),this.radius!==1&&(e.radius=this.radius),(this.mapSize.x!==512||this.mapSize.y!==512)&&(e.mapSize=this.mapSize.toArray()),e.camera=this.camera.toJSON(!1).object,delete e.camera.matrix,e}}class kc extends Uc{constructor(e=-1,t=1,i=1,r=-1,a=.1,s=2e3){super(),this.isOrthographicCamera=!0,this.type="OrthographicCamera",this.zoom=1,this.view=null,this.left=e,this.right=t,this.top=i,this.bottom=r,this.near=a,this.far=s,this.updateProjectionMatrix()}copy(e,t){return super.copy(e,t),this.left=e.left,this.right=e.right,this.top=e.top,this.bottom=e.bottom,this.near=e.near,this.far=e.far,this.zoom=e.zoom,this.view=e.view===null?null:Object.assign({},e.view),this}setViewOffset(e,t,i,r,a,s){this.view===null&&(this.view={enabled:!0,fullWidth:1,fullHeight:1,offsetX:0,offsetY:0,width:1,height:1}),this.view.enabled=!0,this.view.fullWidth=e,this.view.fullHeight=t,this.view.offsetX=i,this.view.offsetY=r,this.view.width=a,this.view.height=s,this.updateProjectionMatrix()}clearViewOffset(){this.view!==null&&(this.view.enabled=!1),this.updateProjectionMatrix()}updateProjectionMatrix(){const e=(this.right-this.left)/(2*this.zoom),t=(this.top-this.bottom)/(2*this.zoom),i=(this.right+this.left)/2,r=(this.top+this.bottom)/2;let a=i-e,s=i+e,o=r+t,c=r-t;if(this.view!==null&&this.view.enabled){const l=(this.right-this.left)/this.view.fullWidth/this.zoom,d=(this.top-this.bottom)/this.view.fullHeight/this.zoom;a+=l*this.view.offsetX,s=a+l*this.view.width,o-=d*this.view.offsetY,c=o-d*this.view.height}this.projectionMatrix.makeOrthographic(a,s,o,c,this.near,this.far,this.coordinateSystem),this.projectionMatrixInverse.copy(this.projectionMatrix).invert()}toJSON(e){const t=super.toJSON(e);return t.object.zoom=this.zoom,t.object.left=this.left,t.object.right=this.right,t.object.top=this.top,t.object.bottom=this.bottom,t.object.near=this.near,t.object.far=this.far,this.view!==null&&(t.object.view=Object.assign({},this.view)),t}}class bu extends yu{constructor(){super(new kc(-5,5,5,-5,.5,500)),this.isDirectionalLightShadow=!0}}class Ro extends Fc{constructor(e,t){super(e,t),this.isDirectionalLight=!0,this.type="DirectionalLight",this.position.copy(Et.DEFAULT_UP),this.updateMatrix(),this.target=new Et,this.shadow=new bu}dispose(){this.shadow.dispose()}copy(e){return super.copy(e),this.target=e.target.clone(),this.shadow=e.shadow.clone(),this}}class Tu extends Fc{constructor(e,t){super(e,t),this.isAmbientLight=!0,this.type="AmbientLight"}}class Au extends Bt{constructor(e=[]){super(),this.isArrayCamera=!0,this.cameras=e,this.index=0}}const Co=new at;class Ns{constructor(e,t,i=0,r=1/0){this.ray=new Ds(e,t),this.near=i,this.far=r,this.camera=null,this.layers=new Ls,this.params={Mesh:{},Line:{threshold:1},LOD:{},Points:{threshold:1},Sprite:{}}}set(e,t){this.ray.set(e,t)}setFromCamera(e,t){t.isPerspectiveCamera?(this.ray.origin.setFromMatrixPosition(t.matrixWorld),this.ray.direction.set(e.x,e.y,.5).unproject(t).sub(this.ray.origin).normalize(),this.camera=t):t.isOrthographicCamera?(this.ray.origin.set(e.x,e.y,(t.near+t.far)/(t.near-t.far)).unproject(t),this.ray.direction.set(0,0,-1).transformDirection(t.matrixWorld),this.camera=t):console.error("THREE.Raycaster: Unsupported camera type: "+t.type)}setFromXRController(e){return Co.identity().extractRotation(e.matrixWorld),this.ray.origin.setFromMatrixPosition(e.matrixWorld),this.ray.direction.set(0,0,-1).applyMatrix4(Co),this}intersectObject(e,t=!0,i=[]){return _s(e,this,i,t),i.sort(Po),i}intersectObjects(e,t=!0,i=[]){for(let r=0,a=e.length;r<a;r++)_s(e[r],this,i,t);return i.sort(Po),i}}function Po(n,e){return n.distance-e.distance}function _s(n,e,t,i){let r=!0;if(n.layers.test(e.layers)&&n.raycast(e,t)===!1&&(r=!1),r===!0&&i===!0){const a=n.children;for(let s=0,o=a.length;s<o;s++)_s(a[s],e,t,!0)}}function Do(n,e,t,i){const r=wu(i);switch(t){case xc:return n*e;case Sc:return n*e;case Ec:return n*e*2;case yc:return n*e/r.components*r.byteLength;case ws:return n*e/r.components*r.byteLength;case bc:return n*e*2/r.components*r.byteLength;case Rs:return n*e*2/r.components*r.byteLength;case Mc:return n*e*3/r.components*r.byteLength;case Yt:return n*e*4/r.components*r.byteLength;case Cs:return n*e*4/r.components*r.byteLength;case wr:case Rr:return Math.floor((n+3)/4)*Math.floor((e+3)/4)*8;case Cr:case Pr:return Math.floor((n+3)/4)*Math.floor((e+3)/4)*16;case Wa:case qa:return Math.max(n,16)*Math.max(e,8)/4;case ja:case Xa:return Math.max(n,8)*Math.max(e,8)/2;case Ya:case Ka:return Math.floor((n+3)/4)*Math.floor((e+3)/4)*8;case $a:return Math.floor((n+3)/4)*Math.floor((e+3)/4)*16;case Za:return Math.floor((n+3)/4)*Math.floor((e+3)/4)*16;case Ja:return Math.floor((n+4)/5)*Math.floor((e+3)/4)*16;case Qa:return Math.floor((n+4)/5)*Math.floor((e+4)/5)*16;case es:return Math.floor((n+5)/6)*Math.floor((e+4)/5)*16;case ts:return Math.floor((n+5)/6)*Math.floor((e+5)/6)*16;case ns:return Math.floor((n+7)/8)*Math.floor((e+4)/5)*16;case is:return Math.floor((n+7)/8)*Math.floor((e+5)/6)*16;case rs:return Math.floor((n+7)/8)*Math.floor((e+7)/8)*16;case as:return Math.floor((n+9)/10)*Math.floor((e+4)/5)*16;case ss:return Math.floor((n+9)/10)*Math.floor((e+5)/6)*16;case os:return Math.floor((n+9)/10)*Math.floor((e+7)/8)*16;case cs:return Math.floor((n+9)/10)*Math.floor((e+9)/10)*16;case ls:return Math.floor((n+11)/12)*Math.floor((e+9)/10)*16;case us:return Math.floor((n+11)/12)*Math.floor((e+11)/12)*16;case Dr:case ds:case hs:return Math.ceil(n/4)*Math.ceil(e/4)*16;case Tc:case fs:return Math.ceil(n/4)*Math.ceil(e/4)*8;case ps:case ms:return Math.ceil(n/4)*Math.ceil(e/4)*16}throw new Error(`Unable to determine texture byte length for ${t} format.`)}function wu(n){switch(n){case pn:case gc:return{byteLength:1,components:1};case ji:case _c:case qi:return{byteLength:2,components:1};case Ts:case As:return{byteLength:2,components:4};case Zn:case bs:case un:return{byteLength:4,components:1};case vc:return{byteLength:4,components:3}}throw new Error(`Unknown texture type ${n}.`)}typeof __THREE_DEVTOOLS__<"u"&&__THREE_DEVTOOLS__.dispatchEvent(new CustomEvent("register",{detail:{revision:ys}}));typeof window<"u"&&(window.__THREE__?console.warn("WARNING: Multiple instances of Three.js being imported."):window.__THREE__=ys);/**
 * @license
 * Copyright 2010-2025 Three.js Authors
 * SPDX-License-Identifier: MIT
 */function Oc(){let n=null,e=!1,t=null,i=null;function r(a,s){t(a,s),i=n.requestAnimationFrame(r)}return{start:function(){e!==!0&&t!==null&&(i=n.requestAnimationFrame(r),e=!0)},stop:function(){n.cancelAnimationFrame(i),e=!1},setAnimationLoop:function(a){t=a},setContext:function(a){n=a}}}function Ru(n){const e=new WeakMap;function t(o,c){const l=o.array,d=o.usage,h=l.byteLength,f=n.createBuffer();n.bindBuffer(c,f),n.bufferData(c,l,d),o.onUploadCallback();let m;if(l instanceof Float32Array)m=n.FLOAT;else if(l instanceof Uint16Array)o.isFloat16BufferAttribute?m=n.HALF_FLOAT:m=n.UNSIGNED_SHORT;else if(l instanceof Int16Array)m=n.SHORT;else if(l instanceof Uint32Array)m=n.UNSIGNED_INT;else if(l instanceof Int32Array)m=n.INT;else if(l instanceof Int8Array)m=n.BYTE;else if(l instanceof Uint8Array)m=n.UNSIGNED_BYTE;else if(l instanceof Uint8ClampedArray)m=n.UNSIGNED_BYTE;else throw new Error("THREE.WebGLAttributes: Unsupported buffer data format: "+l);return{buffer:f,type:m,bytesPerElement:l.BYTES_PER_ELEMENT,version:o.version,size:h}}function i(o,c,l){const d=c.array,h=c.updateRanges;if(n.bindBuffer(l,o),h.length===0)n.bufferSubData(l,0,d);else{h.sort((m,g)=>m.start-g.start);let f=0;for(let m=1;m<h.length;m++){const g=h[f],_=h[m];_.start<=g.start+g.count+1?g.count=Math.max(g.count,_.start+_.count-g.start):(++f,h[f]=_)}h.length=f+1;for(let m=0,g=h.length;m<g;m++){const _=h[m];n.bufferSubData(l,_.start*d.BYTES_PER_ELEMENT,d,_.start,_.count)}c.clearUpdateRanges()}c.onUploadCallback()}function r(o){return o.isInterleavedBufferAttribute&&(o=o.data),e.get(o)}function a(o){o.isInterleavedBufferAttribute&&(o=o.data);const c=e.get(o);c&&(n.deleteBuffer(c.buffer),e.delete(o))}function s(o,c){if(o.isInterleavedBufferAttribute&&(o=o.data),o.isGLBufferAttribute){const d=e.get(o);(!d||d.version<o.version)&&e.set(o,{buffer:o.buffer,type:o.type,bytesPerElement:o.elementSize,version:o.version});return}const l=e.get(o);if(l===void 0)e.set(o,t(o,c));else if(l.version<o.version){if(l.size!==o.array.byteLength)throw new Error("THREE.WebGLAttributes: The size of the buffer attribute's array buffer does not match the original size. Resizing buffer attributes is not supported.");i(l.buffer,o,c),l.version=o.version}}return{get:r,remove:a,update:s}}var Cu=`#ifdef USE_ALPHAHASH
	if ( diffuseColor.a < getAlphaHashThreshold( vPosition ) ) discard;
#endif`,Pu=`#ifdef USE_ALPHAHASH
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
#endif`,Du=`#ifdef USE_ALPHAMAP
	diffuseColor.a *= texture2D( alphaMap, vAlphaMapUv ).g;
#endif`,Lu=`#ifdef USE_ALPHAMAP
	uniform sampler2D alphaMap;
#endif`,Iu=`#ifdef USE_ALPHATEST
	#ifdef ALPHA_TO_COVERAGE
	diffuseColor.a = smoothstep( alphaTest, alphaTest + fwidth( diffuseColor.a ), diffuseColor.a );
	if ( diffuseColor.a == 0.0 ) discard;
	#else
	if ( diffuseColor.a < alphaTest ) discard;
	#endif
#endif`,Uu=`#ifdef USE_ALPHATEST
	uniform float alphaTest;
#endif`,zu=`#ifdef USE_AOMAP
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
#endif`,Nu=`#ifdef USE_AOMAP
	uniform sampler2D aoMap;
	uniform float aoMapIntensity;
#endif`,Fu=`#ifdef USE_BATCHING
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
#endif`,ku=`#ifdef USE_BATCHING
	mat4 batchingMatrix = getBatchingMatrix( getIndirectIndex( gl_DrawID ) );
#endif`,Ou=`vec3 transformed = vec3( position );
#ifdef USE_ALPHAHASH
	vPosition = vec3( position );
#endif`,Bu=`vec3 objectNormal = vec3( normal );
#ifdef USE_TANGENT
	vec3 objectTangent = vec3( tangent.xyz );
#endif`,Vu=`float G_BlinnPhong_Implicit( ) {
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
} // validated`,Hu=`#ifdef USE_IRIDESCENCE
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
#endif`,Gu=`#ifdef USE_BUMPMAP
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
#endif`,ju=`#if NUM_CLIPPING_PLANES > 0
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
#endif`,Wu=`#if NUM_CLIPPING_PLANES > 0
	varying vec3 vClipPosition;
	uniform vec4 clippingPlanes[ NUM_CLIPPING_PLANES ];
#endif`,Xu=`#if NUM_CLIPPING_PLANES > 0
	varying vec3 vClipPosition;
#endif`,qu=`#if NUM_CLIPPING_PLANES > 0
	vClipPosition = - mvPosition.xyz;
#endif`,Yu=`#if defined( USE_COLOR_ALPHA )
	diffuseColor *= vColor;
#elif defined( USE_COLOR )
	diffuseColor.rgb *= vColor;
#endif`,Ku=`#if defined( USE_COLOR_ALPHA )
	varying vec4 vColor;
#elif defined( USE_COLOR )
	varying vec3 vColor;
#endif`,$u=`#if defined( USE_COLOR_ALPHA )
	varying vec4 vColor;
#elif defined( USE_COLOR ) || defined( USE_INSTANCING_COLOR ) || defined( USE_BATCHING_COLOR )
	varying vec3 vColor;
#endif`,Zu=`#if defined( USE_COLOR_ALPHA )
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
#endif`,Ju=`#define PI 3.141592653589793
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
} // validated`,Qu=`#ifdef ENVMAP_TYPE_CUBE_UV
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
#endif`,ed=`vec3 transformedNormal = objectNormal;
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
#endif`,td=`#ifdef USE_DISPLACEMENTMAP
	uniform sampler2D displacementMap;
	uniform float displacementScale;
	uniform float displacementBias;
#endif`,nd=`#ifdef USE_DISPLACEMENTMAP
	transformed += normalize( objectNormal ) * ( texture2D( displacementMap, vDisplacementMapUv ).x * displacementScale + displacementBias );
#endif`,id=`#ifdef USE_EMISSIVEMAP
	vec4 emissiveColor = texture2D( emissiveMap, vEmissiveMapUv );
	#ifdef DECODE_VIDEO_TEXTURE_EMISSIVE
		emissiveColor = sRGBTransferEOTF( emissiveColor );
	#endif
	totalEmissiveRadiance *= emissiveColor.rgb;
#endif`,rd=`#ifdef USE_EMISSIVEMAP
	uniform sampler2D emissiveMap;
#endif`,ad="gl_FragColor = linearToOutputTexel( gl_FragColor );",sd=`vec4 LinearTransferOETF( in vec4 value ) {
	return value;
}
vec4 sRGBTransferEOTF( in vec4 value ) {
	return vec4( mix( pow( value.rgb * 0.9478672986 + vec3( 0.0521327014 ), vec3( 2.4 ) ), value.rgb * 0.0773993808, vec3( lessThanEqual( value.rgb, vec3( 0.04045 ) ) ) ), value.a );
}
vec4 sRGBTransferOETF( in vec4 value ) {
	return vec4( mix( pow( value.rgb, vec3( 0.41666 ) ) * 1.055 - vec3( 0.055 ), value.rgb * 12.92, vec3( lessThanEqual( value.rgb, vec3( 0.0031308 ) ) ) ), value.a );
}`,od=`#ifdef USE_ENVMAP
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
#endif`,cd=`#ifdef USE_ENVMAP
	uniform float envMapIntensity;
	uniform float flipEnvMap;
	uniform mat3 envMapRotation;
	#ifdef ENVMAP_TYPE_CUBE
		uniform samplerCube envMap;
	#else
		uniform sampler2D envMap;
	#endif
	
#endif`,ld=`#ifdef USE_ENVMAP
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
#endif`,ud=`#ifdef USE_ENVMAP
	#if defined( USE_BUMPMAP ) || defined( USE_NORMALMAP ) || defined( PHONG ) || defined( LAMBERT )
		#define ENV_WORLDPOS
	#endif
	#ifdef ENV_WORLDPOS
		
		varying vec3 vWorldPosition;
	#else
		varying vec3 vReflect;
		uniform float refractionRatio;
	#endif
#endif`,dd=`#ifdef USE_ENVMAP
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
#endif`,hd=`#ifdef USE_FOG
	vFogDepth = - mvPosition.z;
#endif`,fd=`#ifdef USE_FOG
	varying float vFogDepth;
#endif`,pd=`#ifdef USE_FOG
	#ifdef FOG_EXP2
		float fogFactor = 1.0 - exp( - fogDensity * fogDensity * vFogDepth * vFogDepth );
	#else
		float fogFactor = smoothstep( fogNear, fogFar, vFogDepth );
	#endif
	gl_FragColor.rgb = mix( gl_FragColor.rgb, fogColor, fogFactor );
#endif`,md=`#ifdef USE_FOG
	uniform vec3 fogColor;
	varying float vFogDepth;
	#ifdef FOG_EXP2
		uniform float fogDensity;
	#else
		uniform float fogNear;
		uniform float fogFar;
	#endif
#endif`,gd=`#ifdef USE_GRADIENTMAP
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
}`,_d=`#ifdef USE_LIGHTMAP
	uniform sampler2D lightMap;
	uniform float lightMapIntensity;
#endif`,vd=`LambertMaterial material;
material.diffuseColor = diffuseColor.rgb;
material.specularStrength = specularStrength;`,xd=`varying vec3 vViewPosition;
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
#define RE_IndirectDiffuse		RE_IndirectDiffuse_Lambert`,Md=`uniform bool receiveShadow;
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
#endif`,Sd=`#ifdef USE_ENVMAP
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
#endif`,Ed=`ToonMaterial material;
material.diffuseColor = diffuseColor.rgb;`,yd=`varying vec3 vViewPosition;
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
#define RE_IndirectDiffuse		RE_IndirectDiffuse_Toon`,bd=`BlinnPhongMaterial material;
material.diffuseColor = diffuseColor.rgb;
material.specularColor = specular;
material.specularShininess = shininess;
material.specularStrength = specularStrength;`,Td=`varying vec3 vViewPosition;
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
#define RE_IndirectDiffuse		RE_IndirectDiffuse_BlinnPhong`,Ad=`PhysicalMaterial material;
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
#endif`,wd=`struct PhysicalMaterial {
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
}`,Rd=`
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
#endif`,Cd=`#if defined( RE_IndirectDiffuse )
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
#endif`,Pd=`#if defined( RE_IndirectDiffuse )
	RE_IndirectDiffuse( irradiance, geometryPosition, geometryNormal, geometryViewDir, geometryClearcoatNormal, material, reflectedLight );
#endif
#if defined( RE_IndirectSpecular )
	RE_IndirectSpecular( radiance, iblIrradiance, clearcoatRadiance, geometryPosition, geometryNormal, geometryViewDir, geometryClearcoatNormal, material, reflectedLight );
#endif`,Dd=`#if defined( USE_LOGDEPTHBUF )
	gl_FragDepth = vIsPerspective == 0.0 ? gl_FragCoord.z : log2( vFragDepth ) * logDepthBufFC * 0.5;
#endif`,Ld=`#if defined( USE_LOGDEPTHBUF )
	uniform float logDepthBufFC;
	varying float vFragDepth;
	varying float vIsPerspective;
#endif`,Id=`#ifdef USE_LOGDEPTHBUF
	varying float vFragDepth;
	varying float vIsPerspective;
#endif`,Ud=`#ifdef USE_LOGDEPTHBUF
	vFragDepth = 1.0 + gl_Position.w;
	vIsPerspective = float( isPerspectiveMatrix( projectionMatrix ) );
#endif`,zd=`#ifdef USE_MAP
	vec4 sampledDiffuseColor = texture2D( map, vMapUv );
	#ifdef DECODE_VIDEO_TEXTURE
		sampledDiffuseColor = sRGBTransferEOTF( sampledDiffuseColor );
	#endif
	diffuseColor *= sampledDiffuseColor;
#endif`,Nd=`#ifdef USE_MAP
	uniform sampler2D map;
#endif`,Fd=`#if defined( USE_MAP ) || defined( USE_ALPHAMAP )
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
#endif`,kd=`#if defined( USE_POINTS_UV )
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
#endif`,Od=`float metalnessFactor = metalness;
#ifdef USE_METALNESSMAP
	vec4 texelMetalness = texture2D( metalnessMap, vMetalnessMapUv );
	metalnessFactor *= texelMetalness.b;
#endif`,Bd=`#ifdef USE_METALNESSMAP
	uniform sampler2D metalnessMap;
#endif`,Vd=`#ifdef USE_INSTANCING_MORPH
	float morphTargetInfluences[ MORPHTARGETS_COUNT ];
	float morphTargetBaseInfluence = texelFetch( morphTexture, ivec2( 0, gl_InstanceID ), 0 ).r;
	for ( int i = 0; i < MORPHTARGETS_COUNT; i ++ ) {
		morphTargetInfluences[i] =  texelFetch( morphTexture, ivec2( i + 1, gl_InstanceID ), 0 ).r;
	}
#endif`,Hd=`#if defined( USE_MORPHCOLORS )
	vColor *= morphTargetBaseInfluence;
	for ( int i = 0; i < MORPHTARGETS_COUNT; i ++ ) {
		#if defined( USE_COLOR_ALPHA )
			if ( morphTargetInfluences[ i ] != 0.0 ) vColor += getMorph( gl_VertexID, i, 2 ) * morphTargetInfluences[ i ];
		#elif defined( USE_COLOR )
			if ( morphTargetInfluences[ i ] != 0.0 ) vColor += getMorph( gl_VertexID, i, 2 ).rgb * morphTargetInfluences[ i ];
		#endif
	}
#endif`,Gd=`#ifdef USE_MORPHNORMALS
	objectNormal *= morphTargetBaseInfluence;
	for ( int i = 0; i < MORPHTARGETS_COUNT; i ++ ) {
		if ( morphTargetInfluences[ i ] != 0.0 ) objectNormal += getMorph( gl_VertexID, i, 1 ).xyz * morphTargetInfluences[ i ];
	}
#endif`,jd=`#ifdef USE_MORPHTARGETS
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
#endif`,Wd=`#ifdef USE_MORPHTARGETS
	transformed *= morphTargetBaseInfluence;
	for ( int i = 0; i < MORPHTARGETS_COUNT; i ++ ) {
		if ( morphTargetInfluences[ i ] != 0.0 ) transformed += getMorph( gl_VertexID, i, 0 ).xyz * morphTargetInfluences[ i ];
	}
#endif`,Xd=`float faceDirection = gl_FrontFacing ? 1.0 : - 1.0;
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
vec3 nonPerturbedNormal = normal;`,qd=`#ifdef USE_NORMALMAP_OBJECTSPACE
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
#endif`,Yd=`#ifndef FLAT_SHADED
	varying vec3 vNormal;
	#ifdef USE_TANGENT
		varying vec3 vTangent;
		varying vec3 vBitangent;
	#endif
#endif`,Kd=`#ifndef FLAT_SHADED
	varying vec3 vNormal;
	#ifdef USE_TANGENT
		varying vec3 vTangent;
		varying vec3 vBitangent;
	#endif
#endif`,$d=`#ifndef FLAT_SHADED
	vNormal = normalize( transformedNormal );
	#ifdef USE_TANGENT
		vTangent = normalize( transformedTangent );
		vBitangent = normalize( cross( vNormal, vTangent ) * tangent.w );
	#endif
#endif`,Zd=`#ifdef USE_NORMALMAP
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
#endif`,Jd=`#ifdef USE_CLEARCOAT
	vec3 clearcoatNormal = nonPerturbedNormal;
#endif`,Qd=`#ifdef USE_CLEARCOAT_NORMALMAP
	vec3 clearcoatMapN = texture2D( clearcoatNormalMap, vClearcoatNormalMapUv ).xyz * 2.0 - 1.0;
	clearcoatMapN.xy *= clearcoatNormalScale;
	clearcoatNormal = normalize( tbn2 * clearcoatMapN );
#endif`,eh=`#ifdef USE_CLEARCOATMAP
	uniform sampler2D clearcoatMap;
#endif
#ifdef USE_CLEARCOAT_NORMALMAP
	uniform sampler2D clearcoatNormalMap;
	uniform vec2 clearcoatNormalScale;
#endif
#ifdef USE_CLEARCOAT_ROUGHNESSMAP
	uniform sampler2D clearcoatRoughnessMap;
#endif`,th=`#ifdef USE_IRIDESCENCEMAP
	uniform sampler2D iridescenceMap;
#endif
#ifdef USE_IRIDESCENCE_THICKNESSMAP
	uniform sampler2D iridescenceThicknessMap;
#endif`,nh=`#ifdef OPAQUE
diffuseColor.a = 1.0;
#endif
#ifdef USE_TRANSMISSION
diffuseColor.a *= material.transmissionAlpha;
#endif
gl_FragColor = vec4( outgoingLight, diffuseColor.a );`,ih=`vec3 packNormalToRGB( const in vec3 normal ) {
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
}`,rh=`#ifdef PREMULTIPLIED_ALPHA
	gl_FragColor.rgb *= gl_FragColor.a;
#endif`,ah=`vec4 mvPosition = vec4( transformed, 1.0 );
#ifdef USE_BATCHING
	mvPosition = batchingMatrix * mvPosition;
#endif
#ifdef USE_INSTANCING
	mvPosition = instanceMatrix * mvPosition;
#endif
mvPosition = modelViewMatrix * mvPosition;
gl_Position = projectionMatrix * mvPosition;`,sh=`#ifdef DITHERING
	gl_FragColor.rgb = dithering( gl_FragColor.rgb );
#endif`,oh=`#ifdef DITHERING
	vec3 dithering( vec3 color ) {
		float grid_position = rand( gl_FragCoord.xy );
		vec3 dither_shift_RGB = vec3( 0.25 / 255.0, -0.25 / 255.0, 0.25 / 255.0 );
		dither_shift_RGB = mix( 2.0 * dither_shift_RGB, -2.0 * dither_shift_RGB, grid_position );
		return color + dither_shift_RGB;
	}
#endif`,ch=`float roughnessFactor = roughness;
#ifdef USE_ROUGHNESSMAP
	vec4 texelRoughness = texture2D( roughnessMap, vRoughnessMapUv );
	roughnessFactor *= texelRoughness.g;
#endif`,lh=`#ifdef USE_ROUGHNESSMAP
	uniform sampler2D roughnessMap;
#endif`,uh=`#if NUM_SPOT_LIGHT_COORDS > 0
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
#endif`,dh=`#if NUM_SPOT_LIGHT_COORDS > 0
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
#endif`,hh=`#if ( defined( USE_SHADOWMAP ) && ( NUM_DIR_LIGHT_SHADOWS > 0 || NUM_POINT_LIGHT_SHADOWS > 0 ) ) || ( NUM_SPOT_LIGHT_COORDS > 0 )
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
#endif`,fh=`float getShadowMask() {
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
}`,ph=`#ifdef USE_SKINNING
	mat4 boneMatX = getBoneMatrix( skinIndex.x );
	mat4 boneMatY = getBoneMatrix( skinIndex.y );
	mat4 boneMatZ = getBoneMatrix( skinIndex.z );
	mat4 boneMatW = getBoneMatrix( skinIndex.w );
#endif`,mh=`#ifdef USE_SKINNING
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
#endif`,gh=`#ifdef USE_SKINNING
	vec4 skinVertex = bindMatrix * vec4( transformed, 1.0 );
	vec4 skinned = vec4( 0.0 );
	skinned += boneMatX * skinVertex * skinWeight.x;
	skinned += boneMatY * skinVertex * skinWeight.y;
	skinned += boneMatZ * skinVertex * skinWeight.z;
	skinned += boneMatW * skinVertex * skinWeight.w;
	transformed = ( bindMatrixInverse * skinned ).xyz;
#endif`,_h=`#ifdef USE_SKINNING
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
#endif`,vh=`float specularStrength;
#ifdef USE_SPECULARMAP
	vec4 texelSpecular = texture2D( specularMap, vSpecularMapUv );
	specularStrength = texelSpecular.r;
#else
	specularStrength = 1.0;
#endif`,xh=`#ifdef USE_SPECULARMAP
	uniform sampler2D specularMap;
#endif`,Mh=`#if defined( TONE_MAPPING )
	gl_FragColor.rgb = toneMapping( gl_FragColor.rgb );
#endif`,Sh=`#ifndef saturate
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
vec3 CustomToneMapping( vec3 color ) { return color; }`,Eh=`#ifdef USE_TRANSMISSION
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
#endif`,yh=`#ifdef USE_TRANSMISSION
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
#endif`,bh=`#if defined( USE_UV ) || defined( USE_ANISOTROPY )
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
#endif`,Th=`#if defined( USE_UV ) || defined( USE_ANISOTROPY )
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
#endif`,Ah=`#if defined( USE_UV ) || defined( USE_ANISOTROPY )
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
#endif`,wh=`#if defined( USE_ENVMAP ) || defined( DISTANCE ) || defined ( USE_SHADOWMAP ) || defined ( USE_TRANSMISSION ) || NUM_SPOT_LIGHT_COORDS > 0
	vec4 worldPosition = vec4( transformed, 1.0 );
	#ifdef USE_BATCHING
		worldPosition = batchingMatrix * worldPosition;
	#endif
	#ifdef USE_INSTANCING
		worldPosition = instanceMatrix * worldPosition;
	#endif
	worldPosition = modelMatrix * worldPosition;
#endif`;const Rh=`varying vec2 vUv;
uniform mat3 uvTransform;
void main() {
	vUv = ( uvTransform * vec3( uv, 1 ) ).xy;
	gl_Position = vec4( position.xy, 1.0, 1.0 );
}`,Ch=`uniform sampler2D t2D;
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
}`,Ph=`varying vec3 vWorldDirection;
#include <common>
void main() {
	vWorldDirection = transformDirection( position, modelMatrix );
	#include <begin_vertex>
	#include <project_vertex>
	gl_Position.z = gl_Position.w;
}`,Dh=`#ifdef ENVMAP_TYPE_CUBE
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
}`,Lh=`varying vec3 vWorldDirection;
#include <common>
void main() {
	vWorldDirection = transformDirection( position, modelMatrix );
	#include <begin_vertex>
	#include <project_vertex>
	gl_Position.z = gl_Position.w;
}`,Ih=`uniform samplerCube tCube;
uniform float tFlip;
uniform float opacity;
varying vec3 vWorldDirection;
void main() {
	vec4 texColor = textureCube( tCube, vec3( tFlip * vWorldDirection.x, vWorldDirection.yz ) );
	gl_FragColor = texColor;
	gl_FragColor.a *= opacity;
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
}`,Uh=`#include <common>
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
}`,zh=`#if DEPTH_PACKING == 3200
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
}`,Nh=`#define DISTANCE
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
}`,Fh=`#define DISTANCE
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
}`,kh=`varying vec3 vWorldDirection;
#include <common>
void main() {
	vWorldDirection = transformDirection( position, modelMatrix );
	#include <begin_vertex>
	#include <project_vertex>
}`,Oh=`uniform sampler2D tEquirect;
varying vec3 vWorldDirection;
#include <common>
void main() {
	vec3 direction = normalize( vWorldDirection );
	vec2 sampleUV = equirectUv( direction );
	gl_FragColor = texture2D( tEquirect, sampleUV );
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
}`,Bh=`uniform float scale;
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
}`,Vh=`uniform vec3 diffuse;
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
}`,Hh=`#include <common>
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
}`,Gh=`uniform vec3 diffuse;
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
}`,jh=`#define LAMBERT
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
}`,Wh=`#define LAMBERT
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
}`,Xh=`#define MATCAP
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
}`,qh=`#define MATCAP
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
}`,Yh=`#define NORMAL
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
}`,Kh=`#define NORMAL
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
}`,$h=`#define PHONG
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
}`,Zh=`#define PHONG
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
}`,Jh=`#define STANDARD
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
}`,Qh=`#define STANDARD
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
}`,ef=`#define TOON
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
}`,tf=`#define TOON
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
}`,nf=`uniform float size;
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
}`,rf=`uniform vec3 diffuse;
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
}`,af=`#include <common>
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
}`,sf=`uniform vec3 color;
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
}`,of=`uniform float rotation;
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
}`,cf=`uniform vec3 diffuse;
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
}`,He={alphahash_fragment:Cu,alphahash_pars_fragment:Pu,alphamap_fragment:Du,alphamap_pars_fragment:Lu,alphatest_fragment:Iu,alphatest_pars_fragment:Uu,aomap_fragment:zu,aomap_pars_fragment:Nu,batching_pars_vertex:Fu,batching_vertex:ku,begin_vertex:Ou,beginnormal_vertex:Bu,bsdfs:Vu,iridescence_fragment:Hu,bumpmap_pars_fragment:Gu,clipping_planes_fragment:ju,clipping_planes_pars_fragment:Wu,clipping_planes_pars_vertex:Xu,clipping_planes_vertex:qu,color_fragment:Yu,color_pars_fragment:Ku,color_pars_vertex:$u,color_vertex:Zu,common:Ju,cube_uv_reflection_fragment:Qu,defaultnormal_vertex:ed,displacementmap_pars_vertex:td,displacementmap_vertex:nd,emissivemap_fragment:id,emissivemap_pars_fragment:rd,colorspace_fragment:ad,colorspace_pars_fragment:sd,envmap_fragment:od,envmap_common_pars_fragment:cd,envmap_pars_fragment:ld,envmap_pars_vertex:ud,envmap_physical_pars_fragment:Sd,envmap_vertex:dd,fog_vertex:hd,fog_pars_vertex:fd,fog_fragment:pd,fog_pars_fragment:md,gradientmap_pars_fragment:gd,lightmap_pars_fragment:_d,lights_lambert_fragment:vd,lights_lambert_pars_fragment:xd,lights_pars_begin:Md,lights_toon_fragment:Ed,lights_toon_pars_fragment:yd,lights_phong_fragment:bd,lights_phong_pars_fragment:Td,lights_physical_fragment:Ad,lights_physical_pars_fragment:wd,lights_fragment_begin:Rd,lights_fragment_maps:Cd,lights_fragment_end:Pd,logdepthbuf_fragment:Dd,logdepthbuf_pars_fragment:Ld,logdepthbuf_pars_vertex:Id,logdepthbuf_vertex:Ud,map_fragment:zd,map_pars_fragment:Nd,map_particle_fragment:Fd,map_particle_pars_fragment:kd,metalnessmap_fragment:Od,metalnessmap_pars_fragment:Bd,morphinstance_vertex:Vd,morphcolor_vertex:Hd,morphnormal_vertex:Gd,morphtarget_pars_vertex:jd,morphtarget_vertex:Wd,normal_fragment_begin:Xd,normal_fragment_maps:qd,normal_pars_fragment:Yd,normal_pars_vertex:Kd,normal_vertex:$d,normalmap_pars_fragment:Zd,clearcoat_normal_fragment_begin:Jd,clearcoat_normal_fragment_maps:Qd,clearcoat_pars_fragment:eh,iridescence_pars_fragment:th,opaque_fragment:nh,packing:ih,premultiplied_alpha_fragment:rh,project_vertex:ah,dithering_fragment:sh,dithering_pars_fragment:oh,roughnessmap_fragment:ch,roughnessmap_pars_fragment:lh,shadowmap_pars_fragment:uh,shadowmap_pars_vertex:dh,shadowmap_vertex:hh,shadowmask_pars_fragment:fh,skinbase_vertex:ph,skinning_pars_vertex:mh,skinning_vertex:gh,skinnormal_vertex:_h,specularmap_fragment:vh,specularmap_pars_fragment:xh,tonemapping_fragment:Mh,tonemapping_pars_fragment:Sh,transmission_fragment:Eh,transmission_pars_fragment:yh,uv_pars_fragment:bh,uv_pars_vertex:Th,uv_vertex:Ah,worldpos_vertex:wh,background_vert:Rh,background_frag:Ch,backgroundCube_vert:Ph,backgroundCube_frag:Dh,cube_vert:Lh,cube_frag:Ih,depth_vert:Uh,depth_frag:zh,distanceRGBA_vert:Nh,distanceRGBA_frag:Fh,equirect_vert:kh,equirect_frag:Oh,linedashed_vert:Bh,linedashed_frag:Vh,meshbasic_vert:Hh,meshbasic_frag:Gh,meshlambert_vert:jh,meshlambert_frag:Wh,meshmatcap_vert:Xh,meshmatcap_frag:qh,meshnormal_vert:Yh,meshnormal_frag:Kh,meshphong_vert:$h,meshphong_frag:Zh,meshphysical_vert:Jh,meshphysical_frag:Qh,meshtoon_vert:ef,meshtoon_frag:tf,points_vert:nf,points_frag:rf,shadow_vert:af,shadow_frag:sf,sprite_vert:of,sprite_frag:cf},he={common:{diffuse:{value:new ce(16777215)},opacity:{value:1},map:{value:null},mapTransform:{value:new Be},alphaMap:{value:null},alphaMapTransform:{value:new Be},alphaTest:{value:0}},specularmap:{specularMap:{value:null},specularMapTransform:{value:new Be}},envmap:{envMap:{value:null},envMapRotation:{value:new Be},flipEnvMap:{value:-1},reflectivity:{value:1},ior:{value:1.5},refractionRatio:{value:.98}},aomap:{aoMap:{value:null},aoMapIntensity:{value:1},aoMapTransform:{value:new Be}},lightmap:{lightMap:{value:null},lightMapIntensity:{value:1},lightMapTransform:{value:new Be}},bumpmap:{bumpMap:{value:null},bumpMapTransform:{value:new Be},bumpScale:{value:1}},normalmap:{normalMap:{value:null},normalMapTransform:{value:new Be},normalScale:{value:new Xe(1,1)}},displacementmap:{displacementMap:{value:null},displacementMapTransform:{value:new Be},displacementScale:{value:1},displacementBias:{value:0}},emissivemap:{emissiveMap:{value:null},emissiveMapTransform:{value:new Be}},metalnessmap:{metalnessMap:{value:null},metalnessMapTransform:{value:new Be}},roughnessmap:{roughnessMap:{value:null},roughnessMapTransform:{value:new Be}},gradientmap:{gradientMap:{value:null}},fog:{fogDensity:{value:25e-5},fogNear:{value:1},fogFar:{value:2e3},fogColor:{value:new ce(16777215)}},lights:{ambientLightColor:{value:[]},lightProbe:{value:[]},directionalLights:{value:[],properties:{direction:{},color:{}}},directionalLightShadows:{value:[],properties:{shadowIntensity:1,shadowBias:{},shadowNormalBias:{},shadowRadius:{},shadowMapSize:{}}},directionalShadowMap:{value:[]},directionalShadowMatrix:{value:[]},spotLights:{value:[],properties:{color:{},position:{},direction:{},distance:{},coneCos:{},penumbraCos:{},decay:{}}},spotLightShadows:{value:[],properties:{shadowIntensity:1,shadowBias:{},shadowNormalBias:{},shadowRadius:{},shadowMapSize:{}}},spotLightMap:{value:[]},spotShadowMap:{value:[]},spotLightMatrix:{value:[]},pointLights:{value:[],properties:{color:{},position:{},decay:{},distance:{}}},pointLightShadows:{value:[],properties:{shadowIntensity:1,shadowBias:{},shadowNormalBias:{},shadowRadius:{},shadowMapSize:{},shadowCameraNear:{},shadowCameraFar:{}}},pointShadowMap:{value:[]},pointShadowMatrix:{value:[]},hemisphereLights:{value:[],properties:{direction:{},skyColor:{},groundColor:{}}},rectAreaLights:{value:[],properties:{color:{},position:{},width:{},height:{}}},ltc_1:{value:null},ltc_2:{value:null}},points:{diffuse:{value:new ce(16777215)},opacity:{value:1},size:{value:1},scale:{value:1},map:{value:null},alphaMap:{value:null},alphaMapTransform:{value:new Be},alphaTest:{value:0},uvTransform:{value:new Be}},sprite:{diffuse:{value:new ce(16777215)},opacity:{value:1},center:{value:new Xe(.5,.5)},rotation:{value:0},map:{value:null},mapTransform:{value:new Be},alphaMap:{value:null},alphaMapTransform:{value:new Be},alphaTest:{value:0}}},$t={basic:{uniforms:wt([he.common,he.specularmap,he.envmap,he.aomap,he.lightmap,he.fog]),vertexShader:He.meshbasic_vert,fragmentShader:He.meshbasic_frag},lambert:{uniforms:wt([he.common,he.specularmap,he.envmap,he.aomap,he.lightmap,he.emissivemap,he.bumpmap,he.normalmap,he.displacementmap,he.fog,he.lights,{emissive:{value:new ce(0)}}]),vertexShader:He.meshlambert_vert,fragmentShader:He.meshlambert_frag},phong:{uniforms:wt([he.common,he.specularmap,he.envmap,he.aomap,he.lightmap,he.emissivemap,he.bumpmap,he.normalmap,he.displacementmap,he.fog,he.lights,{emissive:{value:new ce(0)},specular:{value:new ce(1118481)},shininess:{value:30}}]),vertexShader:He.meshphong_vert,fragmentShader:He.meshphong_frag},standard:{uniforms:wt([he.common,he.envmap,he.aomap,he.lightmap,he.emissivemap,he.bumpmap,he.normalmap,he.displacementmap,he.roughnessmap,he.metalnessmap,he.fog,he.lights,{emissive:{value:new ce(0)},roughness:{value:1},metalness:{value:0},envMapIntensity:{value:1}}]),vertexShader:He.meshphysical_vert,fragmentShader:He.meshphysical_frag},toon:{uniforms:wt([he.common,he.aomap,he.lightmap,he.emissivemap,he.bumpmap,he.normalmap,he.displacementmap,he.gradientmap,he.fog,he.lights,{emissive:{value:new ce(0)}}]),vertexShader:He.meshtoon_vert,fragmentShader:He.meshtoon_frag},matcap:{uniforms:wt([he.common,he.bumpmap,he.normalmap,he.displacementmap,he.fog,{matcap:{value:null}}]),vertexShader:He.meshmatcap_vert,fragmentShader:He.meshmatcap_frag},points:{uniforms:wt([he.points,he.fog]),vertexShader:He.points_vert,fragmentShader:He.points_frag},dashed:{uniforms:wt([he.common,he.fog,{scale:{value:1},dashSize:{value:1},totalSize:{value:2}}]),vertexShader:He.linedashed_vert,fragmentShader:He.linedashed_frag},depth:{uniforms:wt([he.common,he.displacementmap]),vertexShader:He.depth_vert,fragmentShader:He.depth_frag},normal:{uniforms:wt([he.common,he.bumpmap,he.normalmap,he.displacementmap,{opacity:{value:1}}]),vertexShader:He.meshnormal_vert,fragmentShader:He.meshnormal_frag},sprite:{uniforms:wt([he.sprite,he.fog]),vertexShader:He.sprite_vert,fragmentShader:He.sprite_frag},background:{uniforms:{uvTransform:{value:new Be},t2D:{value:null},backgroundIntensity:{value:1}},vertexShader:He.background_vert,fragmentShader:He.background_frag},backgroundCube:{uniforms:{envMap:{value:null},flipEnvMap:{value:-1},backgroundBlurriness:{value:0},backgroundIntensity:{value:1},backgroundRotation:{value:new Be}},vertexShader:He.backgroundCube_vert,fragmentShader:He.backgroundCube_frag},cube:{uniforms:{tCube:{value:null},tFlip:{value:-1},opacity:{value:1}},vertexShader:He.cube_vert,fragmentShader:He.cube_frag},equirect:{uniforms:{tEquirect:{value:null}},vertexShader:He.equirect_vert,fragmentShader:He.equirect_frag},distanceRGBA:{uniforms:wt([he.common,he.displacementmap,{referencePosition:{value:new k},nearDistance:{value:1},farDistance:{value:1e3}}]),vertexShader:He.distanceRGBA_vert,fragmentShader:He.distanceRGBA_frag},shadow:{uniforms:wt([he.lights,he.fog,{color:{value:new ce(0)},opacity:{value:1}}]),vertexShader:He.shadow_vert,fragmentShader:He.shadow_frag}};$t.physical={uniforms:wt([$t.standard.uniforms,{clearcoat:{value:0},clearcoatMap:{value:null},clearcoatMapTransform:{value:new Be},clearcoatNormalMap:{value:null},clearcoatNormalMapTransform:{value:new Be},clearcoatNormalScale:{value:new Xe(1,1)},clearcoatRoughness:{value:0},clearcoatRoughnessMap:{value:null},clearcoatRoughnessMapTransform:{value:new Be},dispersion:{value:0},iridescence:{value:0},iridescenceMap:{value:null},iridescenceMapTransform:{value:new Be},iridescenceIOR:{value:1.3},iridescenceThicknessMinimum:{value:100},iridescenceThicknessMaximum:{value:400},iridescenceThicknessMap:{value:null},iridescenceThicknessMapTransform:{value:new Be},sheen:{value:0},sheenColor:{value:new ce(0)},sheenColorMap:{value:null},sheenColorMapTransform:{value:new Be},sheenRoughness:{value:1},sheenRoughnessMap:{value:null},sheenRoughnessMapTransform:{value:new Be},transmission:{value:0},transmissionMap:{value:null},transmissionMapTransform:{value:new Be},transmissionSamplerSize:{value:new Xe},transmissionSamplerMap:{value:null},thickness:{value:0},thicknessMap:{value:null},thicknessMapTransform:{value:new Be},attenuationDistance:{value:0},attenuationColor:{value:new ce(0)},specularColor:{value:new ce(1,1,1)},specularColorMap:{value:null},specularColorMapTransform:{value:new Be},specularIntensity:{value:1},specularIntensityMap:{value:null},specularIntensityMapTransform:{value:new Be},anisotropyVector:{value:new Xe},anisotropyMap:{value:null},anisotropyMapTransform:{value:new Be}}]),vertexShader:He.meshphysical_vert,fragmentShader:He.meshphysical_frag};const yr={r:0,b:0,g:0},kn=new Mt,lf=new at;function uf(n,e,t,i,r,a,s){const o=new ce(0);let c=a===!0?0:1,l,d,h=null,f=0,m=null;function g(S){let M=S.isScene===!0?S.background:null;return M&&M.isTexture&&(M=(S.backgroundBlurriness>0?t:e).get(M)),M}function _(S){let M=!1;const T=g(S);T===null?u(o,c):T&&T.isColor&&(u(T,1),M=!0);const b=n.xr.getEnvironmentBlendMode();b==="additive"?i.buffers.color.setClear(0,0,0,1,s):b==="alpha-blend"&&i.buffers.color.setClear(0,0,0,0,s),(n.autoClear||M)&&(i.buffers.depth.setTest(!0),i.buffers.depth.setMask(!0),i.buffers.color.setMask(!0),n.clear(n.autoClearColor,n.autoClearDepth,n.autoClearStencil))}function p(S,M){const T=g(M);T&&(T.isCubeTexture||T.mapping===Vr)?(d===void 0&&(d=new je(new hn(1,1,1),new Dn({name:"BackgroundCubeMaterial",uniforms:Ri($t.backgroundCube.uniforms),vertexShader:$t.backgroundCube.vertexShader,fragmentShader:$t.backgroundCube.fragmentShader,side:Dt,depthTest:!1,depthWrite:!1,fog:!1})),d.geometry.deleteAttribute("normal"),d.geometry.deleteAttribute("uv"),d.onBeforeRender=function(b,w,L){this.matrixWorld.copyPosition(L.matrixWorld)},Object.defineProperty(d.material,"envMap",{get:function(){return this.uniforms.envMap.value}}),r.update(d)),kn.copy(M.backgroundRotation),kn.x*=-1,kn.y*=-1,kn.z*=-1,T.isCubeTexture&&T.isRenderTargetTexture===!1&&(kn.y*=-1,kn.z*=-1),d.material.uniforms.envMap.value=T,d.material.uniforms.flipEnvMap.value=T.isCubeTexture&&T.isRenderTargetTexture===!1?-1:1,d.material.uniforms.backgroundBlurriness.value=M.backgroundBlurriness,d.material.uniforms.backgroundIntensity.value=M.backgroundIntensity,d.material.uniforms.backgroundRotation.value.setFromMatrix4(lf.makeRotationFromEuler(kn)),d.material.toneMapped=Je.getTransfer(T.colorSpace)!==it,(h!==T||f!==T.version||m!==n.toneMapping)&&(d.material.needsUpdate=!0,h=T,f=T.version,m=n.toneMapping),d.layers.enableAll(),S.unshift(d,d.geometry,d.material,0,0,null)):T&&T.isTexture&&(l===void 0&&(l=new je(new Li(2,2),new Dn({name:"BackgroundMaterial",uniforms:Ri($t.background.uniforms),vertexShader:$t.background.vertexShader,fragmentShader:$t.background.fragmentShader,side:Pn,depthTest:!1,depthWrite:!1,fog:!1})),l.geometry.deleteAttribute("normal"),Object.defineProperty(l.material,"map",{get:function(){return this.uniforms.t2D.value}}),r.update(l)),l.material.uniforms.t2D.value=T,l.material.uniforms.backgroundIntensity.value=M.backgroundIntensity,l.material.toneMapped=Je.getTransfer(T.colorSpace)!==it,T.matrixAutoUpdate===!0&&T.updateMatrix(),l.material.uniforms.uvTransform.value.copy(T.matrix),(h!==T||f!==T.version||m!==n.toneMapping)&&(l.material.needsUpdate=!0,h=T,f=T.version,m=n.toneMapping),l.layers.enableAll(),S.unshift(l,l.geometry,l.material,0,0,null))}function u(S,M){S.getRGB(yr,Ic(n)),i.buffers.color.setClear(yr.r,yr.g,yr.b,M,s)}function y(){d!==void 0&&(d.geometry.dispose(),d.material.dispose(),d=void 0),l!==void 0&&(l.geometry.dispose(),l.material.dispose(),l=void 0)}return{getClearColor:function(){return o},setClearColor:function(S,M=1){o.set(S),c=M,u(o,c)},getClearAlpha:function(){return c},setClearAlpha:function(S){c=S,u(o,c)},render:_,addToRenderList:p,dispose:y}}function df(n,e){const t=n.getParameter(n.MAX_VERTEX_ATTRIBS),i={},r=f(null);let a=r,s=!1;function o(v,R,U,C,P){let F=!1;const N=h(C,U,R);a!==N&&(a=N,l(a.object)),F=m(v,C,U,P),F&&g(v,C,U,P),P!==null&&e.update(P,n.ELEMENT_ARRAY_BUFFER),(F||s)&&(s=!1,M(v,R,U,C),P!==null&&n.bindBuffer(n.ELEMENT_ARRAY_BUFFER,e.get(P).buffer))}function c(){return n.createVertexArray()}function l(v){return n.bindVertexArray(v)}function d(v){return n.deleteVertexArray(v)}function h(v,R,U){const C=U.wireframe===!0;let P=i[v.id];P===void 0&&(P={},i[v.id]=P);let F=P[R.id];F===void 0&&(F={},P[R.id]=F);let N=F[C];return N===void 0&&(N=f(c()),F[C]=N),N}function f(v){const R=[],U=[],C=[];for(let P=0;P<t;P++)R[P]=0,U[P]=0,C[P]=0;return{geometry:null,program:null,wireframe:!1,newAttributes:R,enabledAttributes:U,attributeDivisors:C,object:v,attributes:{},index:null}}function m(v,R,U,C){const P=a.attributes,F=R.attributes;let N=0;const O=U.getAttributes();for(const z in O)if(O[z].location>=0){const K=P[z];let $=F[z];if($===void 0&&(z==="instanceMatrix"&&v.instanceMatrix&&($=v.instanceMatrix),z==="instanceColor"&&v.instanceColor&&($=v.instanceColor)),K===void 0||K.attribute!==$||$&&K.data!==$.data)return!0;N++}return a.attributesNum!==N||a.index!==C}function g(v,R,U,C){const P={},F=R.attributes;let N=0;const O=U.getAttributes();for(const z in O)if(O[z].location>=0){let K=F[z];K===void 0&&(z==="instanceMatrix"&&v.instanceMatrix&&(K=v.instanceMatrix),z==="instanceColor"&&v.instanceColor&&(K=v.instanceColor));const $={};$.attribute=K,K&&K.data&&($.data=K.data),P[z]=$,N++}a.attributes=P,a.attributesNum=N,a.index=C}function _(){const v=a.newAttributes;for(let R=0,U=v.length;R<U;R++)v[R]=0}function p(v){u(v,0)}function u(v,R){const U=a.newAttributes,C=a.enabledAttributes,P=a.attributeDivisors;U[v]=1,C[v]===0&&(n.enableVertexAttribArray(v),C[v]=1),P[v]!==R&&(n.vertexAttribDivisor(v,R),P[v]=R)}function y(){const v=a.newAttributes,R=a.enabledAttributes;for(let U=0,C=R.length;U<C;U++)R[U]!==v[U]&&(n.disableVertexAttribArray(U),R[U]=0)}function S(v,R,U,C,P,F,N){N===!0?n.vertexAttribIPointer(v,R,U,P,F):n.vertexAttribPointer(v,R,U,C,P,F)}function M(v,R,U,C){_();const P=C.attributes,F=U.getAttributes(),N=R.defaultAttributeValues;for(const O in F){const z=F[O];if(z.location>=0){let G=P[O];if(G===void 0&&(O==="instanceMatrix"&&v.instanceMatrix&&(G=v.instanceMatrix),O==="instanceColor"&&v.instanceColor&&(G=v.instanceColor)),G!==void 0){const K=G.normalized,$=G.itemSize,fe=e.get(G);if(fe===void 0)continue;const De=fe.buffer,X=fe.type,ne=fe.bytesPerElement,ue=X===n.INT||X===n.UNSIGNED_INT||G.gpuType===bs;if(G.isInterleavedBufferAttribute){const se=G.data,ee=se.stride,_e=G.offset;if(se.isInstancedInterleavedBuffer){for(let de=0;de<z.locationSize;de++)u(z.location+de,se.meshPerAttribute);v.isInstancedMesh!==!0&&C._maxInstanceCount===void 0&&(C._maxInstanceCount=se.meshPerAttribute*se.count)}else for(let de=0;de<z.locationSize;de++)p(z.location+de);n.bindBuffer(n.ARRAY_BUFFER,De);for(let de=0;de<z.locationSize;de++)S(z.location+de,$/z.locationSize,X,K,ee*ne,(_e+$/z.locationSize*de)*ne,ue)}else{if(G.isInstancedBufferAttribute){for(let se=0;se<z.locationSize;se++)u(z.location+se,G.meshPerAttribute);v.isInstancedMesh!==!0&&C._maxInstanceCount===void 0&&(C._maxInstanceCount=G.meshPerAttribute*G.count)}else for(let se=0;se<z.locationSize;se++)p(z.location+se);n.bindBuffer(n.ARRAY_BUFFER,De);for(let se=0;se<z.locationSize;se++)S(z.location+se,$/z.locationSize,X,K,$*ne,$/z.locationSize*se*ne,ue)}}else if(N!==void 0){const K=N[O];if(K!==void 0)switch(K.length){case 2:n.vertexAttrib2fv(z.location,K);break;case 3:n.vertexAttrib3fv(z.location,K);break;case 4:n.vertexAttrib4fv(z.location,K);break;default:n.vertexAttrib1fv(z.location,K)}}}}y()}function T(){L();for(const v in i){const R=i[v];for(const U in R){const C=R[U];for(const P in C)d(C[P].object),delete C[P];delete R[U]}delete i[v]}}function b(v){if(i[v.id]===void 0)return;const R=i[v.id];for(const U in R){const C=R[U];for(const P in C)d(C[P].object),delete C[P];delete R[U]}delete i[v.id]}function w(v){for(const R in i){const U=i[R];if(U[v.id]===void 0)continue;const C=U[v.id];for(const P in C)d(C[P].object),delete C[P];delete U[v.id]}}function L(){x(),s=!0,a!==r&&(a=r,l(a.object))}function x(){r.geometry=null,r.program=null,r.wireframe=!1}return{setup:o,reset:L,resetDefaultState:x,dispose:T,releaseStatesOfGeometry:b,releaseStatesOfProgram:w,initAttributes:_,enableAttribute:p,disableUnusedAttributes:y}}function hf(n,e,t){let i;function r(l){i=l}function a(l,d){n.drawArrays(i,l,d),t.update(d,i,1)}function s(l,d,h){h!==0&&(n.drawArraysInstanced(i,l,d,h),t.update(d,i,h))}function o(l,d,h){if(h===0)return;e.get("WEBGL_multi_draw").multiDrawArraysWEBGL(i,l,0,d,0,h);let m=0;for(let g=0;g<h;g++)m+=d[g];t.update(m,i,1)}function c(l,d,h,f){if(h===0)return;const m=e.get("WEBGL_multi_draw");if(m===null)for(let g=0;g<l.length;g++)s(l[g],d[g],f[g]);else{m.multiDrawArraysInstancedWEBGL(i,l,0,d,0,f,0,h);let g=0;for(let _=0;_<h;_++)g+=d[_]*f[_];t.update(g,i,1)}}this.setMode=r,this.render=a,this.renderInstances=s,this.renderMultiDraw=o,this.renderMultiDrawInstances=c}function ff(n,e,t,i){let r;function a(){if(r!==void 0)return r;if(e.has("EXT_texture_filter_anisotropic")===!0){const w=e.get("EXT_texture_filter_anisotropic");r=n.getParameter(w.MAX_TEXTURE_MAX_ANISOTROPY_EXT)}else r=0;return r}function s(w){return!(w!==Yt&&i.convert(w)!==n.getParameter(n.IMPLEMENTATION_COLOR_READ_FORMAT))}function o(w){const L=w===qi&&(e.has("EXT_color_buffer_half_float")||e.has("EXT_color_buffer_float"));return!(w!==pn&&i.convert(w)!==n.getParameter(n.IMPLEMENTATION_COLOR_READ_TYPE)&&w!==un&&!L)}function c(w){if(w==="highp"){if(n.getShaderPrecisionFormat(n.VERTEX_SHADER,n.HIGH_FLOAT).precision>0&&n.getShaderPrecisionFormat(n.FRAGMENT_SHADER,n.HIGH_FLOAT).precision>0)return"highp";w="mediump"}return w==="mediump"&&n.getShaderPrecisionFormat(n.VERTEX_SHADER,n.MEDIUM_FLOAT).precision>0&&n.getShaderPrecisionFormat(n.FRAGMENT_SHADER,n.MEDIUM_FLOAT).precision>0?"mediump":"lowp"}let l=t.precision!==void 0?t.precision:"highp";const d=c(l);d!==l&&(console.warn("THREE.WebGLRenderer:",l,"not supported, using",d,"instead."),l=d);const h=t.logarithmicDepthBuffer===!0,f=t.reverseDepthBuffer===!0&&e.has("EXT_clip_control"),m=n.getParameter(n.MAX_TEXTURE_IMAGE_UNITS),g=n.getParameter(n.MAX_VERTEX_TEXTURE_IMAGE_UNITS),_=n.getParameter(n.MAX_TEXTURE_SIZE),p=n.getParameter(n.MAX_CUBE_MAP_TEXTURE_SIZE),u=n.getParameter(n.MAX_VERTEX_ATTRIBS),y=n.getParameter(n.MAX_VERTEX_UNIFORM_VECTORS),S=n.getParameter(n.MAX_VARYING_VECTORS),M=n.getParameter(n.MAX_FRAGMENT_UNIFORM_VECTORS),T=g>0,b=n.getParameter(n.MAX_SAMPLES);return{isWebGL2:!0,getMaxAnisotropy:a,getMaxPrecision:c,textureFormatReadable:s,textureTypeReadable:o,precision:l,logarithmicDepthBuffer:h,reverseDepthBuffer:f,maxTextures:m,maxVertexTextures:g,maxTextureSize:_,maxCubemapSize:p,maxAttributes:u,maxVertexUniforms:y,maxVaryings:S,maxFragmentUniforms:M,vertexTextures:T,maxSamples:b}}function pf(n){const e=this;let t=null,i=0,r=!1,a=!1;const s=new Vn,o=new Be,c={value:null,needsUpdate:!1};this.uniform=c,this.numPlanes=0,this.numIntersection=0,this.init=function(h,f){const m=h.length!==0||f||i!==0||r;return r=f,i=h.length,m},this.beginShadows=function(){a=!0,d(null)},this.endShadows=function(){a=!1},this.setGlobalState=function(h,f){t=d(h,f,0)},this.setState=function(h,f,m){const g=h.clippingPlanes,_=h.clipIntersection,p=h.clipShadows,u=n.get(h);if(!r||g===null||g.length===0||a&&!p)a?d(null):l();else{const y=a?0:i,S=y*4;let M=u.clippingState||null;c.value=M,M=d(g,f,S,m);for(let T=0;T!==S;++T)M[T]=t[T];u.clippingState=M,this.numIntersection=_?this.numPlanes:0,this.numPlanes+=y}};function l(){c.value!==t&&(c.value=t,c.needsUpdate=i>0),e.numPlanes=i,e.numIntersection=0}function d(h,f,m,g){const _=h!==null?h.length:0;let p=null;if(_!==0){if(p=c.value,g!==!0||p===null){const u=m+_*4,y=f.matrixWorldInverse;o.getNormalMatrix(y),(p===null||p.length<u)&&(p=new Float32Array(u));for(let S=0,M=m;S!==_;++S,M+=4)s.copy(h[S]).applyMatrix4(y,o),s.normal.toArray(p,M),p[M+3]=s.constant}c.value=p,c.needsUpdate=!0}return e.numPlanes=_,e.numIntersection=0,p}}function mf(n){let e=new WeakMap;function t(s,o){return o===Ba?s.mapping=yi:o===Va&&(s.mapping=bi),s}function i(s){if(s&&s.isTexture){const o=s.mapping;if(o===Ba||o===Va)if(e.has(s)){const c=e.get(s).texture;return t(c,s.mapping)}else{const c=s.image;if(c&&c.height>0){const l=new mu(c.height);return l.fromEquirectangularTexture(n,s),e.set(s,l),s.addEventListener("dispose",r),t(l.texture,s.mapping)}else return null}}return s}function r(s){const o=s.target;o.removeEventListener("dispose",r);const c=e.get(o);c!==void 0&&(e.delete(o),c.dispose())}function a(){e=new WeakMap}return{get:i,dispose:a}}const gi=4,Lo=[.125,.215,.35,.446,.526,.582],Xn=20,xa=new kc,Io=new ce;let Ma=null,Sa=0,Ea=0,ya=!1;const Hn=(1+Math.sqrt(5))/2,fi=1/Hn,Uo=[new k(-Hn,fi,0),new k(Hn,fi,0),new k(-fi,0,Hn),new k(fi,0,Hn),new k(0,Hn,-fi),new k(0,Hn,fi),new k(-1,1,-1),new k(1,1,-1),new k(-1,1,1),new k(1,1,1)],gf=new k;class zo{constructor(e){this._renderer=e,this._pingPongRenderTarget=null,this._lodMax=0,this._cubeSize=0,this._lodPlanes=[],this._sizeLods=[],this._sigmas=[],this._blurMaterial=null,this._cubemapMaterial=null,this._equirectMaterial=null,this._compileMaterial(this._blurMaterial)}fromScene(e,t=0,i=.1,r=100,a={}){const{size:s=256,position:o=gf}=a;Ma=this._renderer.getRenderTarget(),Sa=this._renderer.getActiveCubeFace(),Ea=this._renderer.getActiveMipmapLevel(),ya=this._renderer.xr.enabled,this._renderer.xr.enabled=!1,this._setSize(s);const c=this._allocateTargets();return c.depthBuffer=!0,this._sceneToCubeUV(e,i,r,c,o),t>0&&this._blur(c,0,0,t),this._applyPMREM(c),this._cleanup(c),c}fromEquirectangular(e,t=null){return this._fromTexture(e,t)}fromCubemap(e,t=null){return this._fromTexture(e,t)}compileCubemapShader(){this._cubemapMaterial===null&&(this._cubemapMaterial=ko(),this._compileMaterial(this._cubemapMaterial))}compileEquirectangularShader(){this._equirectMaterial===null&&(this._equirectMaterial=Fo(),this._compileMaterial(this._equirectMaterial))}dispose(){this._dispose(),this._cubemapMaterial!==null&&this._cubemapMaterial.dispose(),this._equirectMaterial!==null&&this._equirectMaterial.dispose()}_setSize(e){this._lodMax=Math.floor(Math.log2(e)),this._cubeSize=Math.pow(2,this._lodMax)}_dispose(){this._blurMaterial!==null&&this._blurMaterial.dispose(),this._pingPongRenderTarget!==null&&this._pingPongRenderTarget.dispose();for(let e=0;e<this._lodPlanes.length;e++)this._lodPlanes[e].dispose()}_cleanup(e){this._renderer.setRenderTarget(Ma,Sa,Ea),this._renderer.xr.enabled=ya,e.scissorTest=!1,br(e,0,0,e.width,e.height)}_fromTexture(e,t){e.mapping===yi||e.mapping===bi?this._setSize(e.image.length===0?16:e.image[0].width||e.image[0].image.width):this._setSize(e.image.width/4),Ma=this._renderer.getRenderTarget(),Sa=this._renderer.getActiveCubeFace(),Ea=this._renderer.getActiveMipmapLevel(),ya=this._renderer.xr.enabled,this._renderer.xr.enabled=!1;const i=t||this._allocateTargets();return this._textureToCubeUV(e,i),this._applyPMREM(i),this._cleanup(i),i}_allocateTargets(){const e=3*Math.max(this._cubeSize,112),t=4*this._cubeSize,i={magFilter:Zt,minFilter:Zt,generateMipmaps:!1,type:qi,format:Yt,colorSpace:wi,depthBuffer:!1},r=No(e,t,i);if(this._pingPongRenderTarget===null||this._pingPongRenderTarget.width!==e||this._pingPongRenderTarget.height!==t){this._pingPongRenderTarget!==null&&this._dispose(),this._pingPongRenderTarget=No(e,t,i);const{_lodMax:a}=this;({sizeLods:this._sizeLods,lodPlanes:this._lodPlanes,sigmas:this._sigmas}=_f(a)),this._blurMaterial=vf(a,e,t)}return r}_compileMaterial(e){const t=new je(this._lodPlanes[0],e);this._renderer.compile(t,xa)}_sceneToCubeUV(e,t,i,r,a){const c=new Bt(90,1,t,i),l=[1,-1,1,1,1,1],d=[1,1,1,-1,-1,-1],h=this._renderer,f=h.autoClear,m=h.toneMapping;h.getClearColor(Io),h.toneMapping=Cn,h.autoClear=!1;const g=new Di({name:"PMREM.Background",side:Dt,depthWrite:!1,depthTest:!1}),_=new je(new hn,g);let p=!1;const u=e.background;u?u.isColor&&(g.color.copy(u),e.background=null,p=!0):(g.color.copy(Io),p=!0);for(let y=0;y<6;y++){const S=y%3;S===0?(c.up.set(0,l[y],0),c.position.set(a.x,a.y,a.z),c.lookAt(a.x+d[y],a.y,a.z)):S===1?(c.up.set(0,0,l[y]),c.position.set(a.x,a.y,a.z),c.lookAt(a.x,a.y+d[y],a.z)):(c.up.set(0,l[y],0),c.position.set(a.x,a.y,a.z),c.lookAt(a.x,a.y,a.z+d[y]));const M=this._cubeSize;br(r,S*M,y>2?M:0,M,M),h.setRenderTarget(r),p&&h.render(_,c),h.render(e,c)}_.geometry.dispose(),_.material.dispose(),h.toneMapping=m,h.autoClear=f,e.background=u}_textureToCubeUV(e,t){const i=this._renderer,r=e.mapping===yi||e.mapping===bi;r?(this._cubemapMaterial===null&&(this._cubemapMaterial=ko()),this._cubemapMaterial.uniforms.flipEnvMap.value=e.isRenderTargetTexture===!1?-1:1):this._equirectMaterial===null&&(this._equirectMaterial=Fo());const a=r?this._cubemapMaterial:this._equirectMaterial,s=new je(this._lodPlanes[0],a),o=a.uniforms;o.envMap.value=e;const c=this._cubeSize;br(t,0,0,3*c,2*c),i.setRenderTarget(t),i.render(s,xa)}_applyPMREM(e){const t=this._renderer,i=t.autoClear;t.autoClear=!1;const r=this._lodPlanes.length;for(let a=1;a<r;a++){const s=Math.sqrt(this._sigmas[a]*this._sigmas[a]-this._sigmas[a-1]*this._sigmas[a-1]),o=Uo[(r-a-1)%Uo.length];this._blur(e,a-1,a,s,o)}t.autoClear=i}_blur(e,t,i,r,a){const s=this._pingPongRenderTarget;this._halfBlur(e,s,t,i,r,"latitudinal",a),this._halfBlur(s,e,i,i,r,"longitudinal",a)}_halfBlur(e,t,i,r,a,s,o){const c=this._renderer,l=this._blurMaterial;s!=="latitudinal"&&s!=="longitudinal"&&console.error("blur direction must be either latitudinal or longitudinal!");const d=3,h=new je(this._lodPlanes[r],l),f=l.uniforms,m=this._sizeLods[i]-1,g=isFinite(a)?Math.PI/(2*m):2*Math.PI/(2*Xn-1),_=a/g,p=isFinite(a)?1+Math.floor(d*_):Xn;p>Xn&&console.warn(`sigmaRadians, ${a}, is too large and will clip, as it requested ${p} samples when the maximum is set to ${Xn}`);const u=[];let y=0;for(let w=0;w<Xn;++w){const L=w/_,x=Math.exp(-L*L/2);u.push(x),w===0?y+=x:w<p&&(y+=2*x)}for(let w=0;w<u.length;w++)u[w]=u[w]/y;f.envMap.value=e.texture,f.samples.value=p,f.weights.value=u,f.latitudinal.value=s==="latitudinal",o&&(f.poleAxis.value=o);const{_lodMax:S}=this;f.dTheta.value=g,f.mipInt.value=S-i;const M=this._sizeLods[r],T=3*M*(r>S-gi?r-S+gi:0),b=4*(this._cubeSize-M);br(t,T,b,3*M,2*M),c.setRenderTarget(t),c.render(h,xa)}}function _f(n){const e=[],t=[],i=[];let r=n;const a=n-gi+1+Lo.length;for(let s=0;s<a;s++){const o=Math.pow(2,r);t.push(o);let c=1/o;s>n-gi?c=Lo[s-n+gi-1]:s===0&&(c=0),i.push(c);const l=1/(o-2),d=-l,h=1+l,f=[d,d,h,d,h,h,d,d,h,h,d,h],m=6,g=6,_=3,p=2,u=1,y=new Float32Array(_*g*m),S=new Float32Array(p*g*m),M=new Float32Array(u*g*m);for(let b=0;b<m;b++){const w=b%3*2/3-1,L=b>2?0:-1,x=[w,L,0,w+2/3,L,0,w+2/3,L+1,0,w,L,0,w+2/3,L+1,0,w,L+1,0];y.set(x,_*g*b),S.set(f,p*g*b);const v=[b,b,b,b,b,b];M.set(v,u*g*b)}const T=new Ye;T.setAttribute("position",new Jt(y,_)),T.setAttribute("uv",new Jt(S,p)),T.setAttribute("faceIndex",new Jt(M,u)),e.push(T),r>gi&&r--}return{lodPlanes:e,sizeLods:t,sigmas:i}}function No(n,e,t){const i=new Jn(n,e,t);return i.texture.mapping=Vr,i.texture.name="PMREM.cubeUv",i.scissorTest=!0,i}function br(n,e,t,i,r){n.viewport.set(e,t,i,r),n.scissor.set(e,t,i,r)}function vf(n,e,t){const i=new Float32Array(Xn),r=new k(0,1,0);return new Dn({name:"SphericalGaussianBlur",defines:{n:Xn,CUBEUV_TEXEL_WIDTH:1/e,CUBEUV_TEXEL_HEIGHT:1/t,CUBEUV_MAX_MIP:`${n}.0`},uniforms:{envMap:{value:null},samples:{value:1},weights:{value:i},latitudinal:{value:!1},dTheta:{value:0},mipInt:{value:0},poleAxis:{value:r}},vertexShader:Fs(),fragmentShader:`

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
		`,blending:Rn,depthTest:!1,depthWrite:!1})}function Fo(){return new Dn({name:"EquirectangularToCubeUV",uniforms:{envMap:{value:null}},vertexShader:Fs(),fragmentShader:`

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
		`,blending:Rn,depthTest:!1,depthWrite:!1})}function ko(){return new Dn({name:"CubemapToCubeUV",uniforms:{envMap:{value:null},flipEnvMap:{value:-1}},vertexShader:Fs(),fragmentShader:`

			precision mediump float;
			precision mediump int;

			uniform float flipEnvMap;

			varying vec3 vOutputDirection;

			uniform samplerCube envMap;

			void main() {

				gl_FragColor = textureCube( envMap, vec3( flipEnvMap * vOutputDirection.x, vOutputDirection.yz ) );

			}
		`,blending:Rn,depthTest:!1,depthWrite:!1})}function Fs(){return`

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
	`}function xf(n){let e=new WeakMap,t=null;function i(o){if(o&&o.isTexture){const c=o.mapping,l=c===Ba||c===Va,d=c===yi||c===bi;if(l||d){let h=e.get(o);const f=h!==void 0?h.texture.pmremVersion:0;if(o.isRenderTargetTexture&&o.pmremVersion!==f)return t===null&&(t=new zo(n)),h=l?t.fromEquirectangular(o,h):t.fromCubemap(o,h),h.texture.pmremVersion=o.pmremVersion,e.set(o,h),h.texture;if(h!==void 0)return h.texture;{const m=o.image;return l&&m&&m.height>0||d&&m&&r(m)?(t===null&&(t=new zo(n)),h=l?t.fromEquirectangular(o):t.fromCubemap(o),h.texture.pmremVersion=o.pmremVersion,e.set(o,h),o.addEventListener("dispose",a),h.texture):null}}}return o}function r(o){let c=0;const l=6;for(let d=0;d<l;d++)o[d]!==void 0&&c++;return c===l}function a(o){const c=o.target;c.removeEventListener("dispose",a);const l=e.get(c);l!==void 0&&(e.delete(c),l.dispose())}function s(){e=new WeakMap,t!==null&&(t.dispose(),t=null)}return{get:i,dispose:s}}function Mf(n){const e={};function t(i){if(e[i]!==void 0)return e[i];let r;switch(i){case"WEBGL_depth_texture":r=n.getExtension("WEBGL_depth_texture")||n.getExtension("MOZ_WEBGL_depth_texture")||n.getExtension("WEBKIT_WEBGL_depth_texture");break;case"EXT_texture_filter_anisotropic":r=n.getExtension("EXT_texture_filter_anisotropic")||n.getExtension("MOZ_EXT_texture_filter_anisotropic")||n.getExtension("WEBKIT_EXT_texture_filter_anisotropic");break;case"WEBGL_compressed_texture_s3tc":r=n.getExtension("WEBGL_compressed_texture_s3tc")||n.getExtension("MOZ_WEBGL_compressed_texture_s3tc")||n.getExtension("WEBKIT_WEBGL_compressed_texture_s3tc");break;case"WEBGL_compressed_texture_pvrtc":r=n.getExtension("WEBGL_compressed_texture_pvrtc")||n.getExtension("WEBKIT_WEBGL_compressed_texture_pvrtc");break;default:r=n.getExtension(i)}return e[i]=r,r}return{has:function(i){return t(i)!==null},init:function(){t("EXT_color_buffer_float"),t("WEBGL_clip_cull_distance"),t("OES_texture_float_linear"),t("EXT_color_buffer_half_float"),t("WEBGL_multisampled_render_to_texture"),t("WEBGL_render_shared_exponent")},get:function(i){const r=t(i);return r===null&&Bn("THREE.WebGLRenderer: "+i+" extension not supported."),r}}}function Sf(n,e,t,i){const r={},a=new WeakMap;function s(h){const f=h.target;f.index!==null&&e.remove(f.index);for(const g in f.attributes)e.remove(f.attributes[g]);f.removeEventListener("dispose",s),delete r[f.id];const m=a.get(f);m&&(e.remove(m),a.delete(f)),i.releaseStatesOfGeometry(f),f.isInstancedBufferGeometry===!0&&delete f._maxInstanceCount,t.memory.geometries--}function o(h,f){return r[f.id]===!0||(f.addEventListener("dispose",s),r[f.id]=!0,t.memory.geometries++),f}function c(h){const f=h.attributes;for(const m in f)e.update(f[m],n.ARRAY_BUFFER)}function l(h){const f=[],m=h.index,g=h.attributes.position;let _=0;if(m!==null){const y=m.array;_=m.version;for(let S=0,M=y.length;S<M;S+=3){const T=y[S+0],b=y[S+1],w=y[S+2];f.push(T,b,b,w,w,T)}}else if(g!==void 0){const y=g.array;_=g.version;for(let S=0,M=y.length/3-1;S<M;S+=3){const T=S+0,b=S+1,w=S+2;f.push(T,b,b,w,w,T)}}else return;const p=new(Rc(f)?Lc:Dc)(f,1);p.version=_;const u=a.get(h);u&&e.remove(u),a.set(h,p)}function d(h){const f=a.get(h);if(f){const m=h.index;m!==null&&f.version<m.version&&l(h)}else l(h);return a.get(h)}return{get:o,update:c,getWireframeAttribute:d}}function Ef(n,e,t){let i;function r(f){i=f}let a,s;function o(f){a=f.type,s=f.bytesPerElement}function c(f,m){n.drawElements(i,m,a,f*s),t.update(m,i,1)}function l(f,m,g){g!==0&&(n.drawElementsInstanced(i,m,a,f*s,g),t.update(m,i,g))}function d(f,m,g){if(g===0)return;e.get("WEBGL_multi_draw").multiDrawElementsWEBGL(i,m,0,a,f,0,g);let p=0;for(let u=0;u<g;u++)p+=m[u];t.update(p,i,1)}function h(f,m,g,_){if(g===0)return;const p=e.get("WEBGL_multi_draw");if(p===null)for(let u=0;u<f.length;u++)l(f[u]/s,m[u],_[u]);else{p.multiDrawElementsInstancedWEBGL(i,m,0,a,f,0,_,0,g);let u=0;for(let y=0;y<g;y++)u+=m[y]*_[y];t.update(u,i,1)}}this.setMode=r,this.setIndex=o,this.render=c,this.renderInstances=l,this.renderMultiDraw=d,this.renderMultiDrawInstances=h}function yf(n){const e={geometries:0,textures:0},t={frame:0,calls:0,triangles:0,points:0,lines:0};function i(a,s,o){switch(t.calls++,s){case n.TRIANGLES:t.triangles+=o*(a/3);break;case n.LINES:t.lines+=o*(a/2);break;case n.LINE_STRIP:t.lines+=o*(a-1);break;case n.LINE_LOOP:t.lines+=o*a;break;case n.POINTS:t.points+=o*a;break;default:console.error("THREE.WebGLInfo: Unknown draw mode:",s);break}}function r(){t.calls=0,t.triangles=0,t.points=0,t.lines=0}return{memory:e,render:t,programs:null,autoReset:!0,reset:r,update:i}}function bf(n,e,t){const i=new WeakMap,r=new dt;function a(s,o,c){const l=s.morphTargetInfluences,d=o.morphAttributes.position||o.morphAttributes.normal||o.morphAttributes.color,h=d!==void 0?d.length:0;let f=i.get(o);if(f===void 0||f.count!==h){let x=function(){w.dispose(),i.delete(o),o.removeEventListener("dispose",x)};f!==void 0&&f.texture.dispose();const m=o.morphAttributes.position!==void 0,g=o.morphAttributes.normal!==void 0,_=o.morphAttributes.color!==void 0,p=o.morphAttributes.position||[],u=o.morphAttributes.normal||[],y=o.morphAttributes.color||[];let S=0;m===!0&&(S=1),g===!0&&(S=2),_===!0&&(S=3);let M=o.attributes.position.count*S,T=1;M>e.maxTextureSize&&(T=Math.ceil(M/e.maxTextureSize),M=e.maxTextureSize);const b=new Float32Array(M*T*4*h),w=new Cc(b,M,T,h);w.type=un,w.needsUpdate=!0;const L=S*4;for(let v=0;v<h;v++){const R=p[v],U=u[v],C=y[v],P=M*T*4*v;for(let F=0;F<R.count;F++){const N=F*L;m===!0&&(r.fromBufferAttribute(R,F),b[P+N+0]=r.x,b[P+N+1]=r.y,b[P+N+2]=r.z,b[P+N+3]=0),g===!0&&(r.fromBufferAttribute(U,F),b[P+N+4]=r.x,b[P+N+5]=r.y,b[P+N+6]=r.z,b[P+N+7]=0),_===!0&&(r.fromBufferAttribute(C,F),b[P+N+8]=r.x,b[P+N+9]=r.y,b[P+N+10]=r.z,b[P+N+11]=C.itemSize===4?r.w:1)}}f={count:h,texture:w,size:new Xe(M,T)},i.set(o,f),o.addEventListener("dispose",x)}if(s.isInstancedMesh===!0&&s.morphTexture!==null)c.getUniforms().setValue(n,"morphTexture",s.morphTexture,t);else{let m=0;for(let _=0;_<l.length;_++)m+=l[_];const g=o.morphTargetsRelative?1:1-m;c.getUniforms().setValue(n,"morphTargetBaseInfluence",g),c.getUniforms().setValue(n,"morphTargetInfluences",l)}c.getUniforms().setValue(n,"morphTargetsTexture",f.texture,t),c.getUniforms().setValue(n,"morphTargetsTextureSize",f.size)}return{update:a}}function Tf(n,e,t,i){let r=new WeakMap;function a(c){const l=i.render.frame,d=c.geometry,h=e.get(c,d);if(r.get(h)!==l&&(e.update(h),r.set(h,l)),c.isInstancedMesh&&(c.hasEventListener("dispose",o)===!1&&c.addEventListener("dispose",o),r.get(c)!==l&&(t.update(c.instanceMatrix,n.ARRAY_BUFFER),c.instanceColor!==null&&t.update(c.instanceColor,n.ARRAY_BUFFER),r.set(c,l))),c.isSkinnedMesh){const f=c.skeleton;r.get(f)!==l&&(f.update(),r.set(f,l))}return h}function s(){r=new WeakMap}function o(c){const l=c.target;l.removeEventListener("dispose",o),t.remove(l.instanceMatrix),l.instanceColor!==null&&t.remove(l.instanceColor)}return{update:a,dispose:s}}const Bc=new Rt,Oo=new Nc(1,1),Vc=new Cc,Hc=new Jl,Gc=new zc,Bo=[],Vo=[],Ho=new Float32Array(16),Go=new Float32Array(9),jo=new Float32Array(4);function Ii(n,e,t){const i=n[0];if(i<=0||i>0)return n;const r=e*t;let a=Bo[r];if(a===void 0&&(a=new Float32Array(r),Bo[r]=a),e!==0){i.toArray(a,0);for(let s=1,o=0;s!==e;++s)o+=t,n[s].toArray(a,o)}return a}function _t(n,e){if(n.length!==e.length)return!1;for(let t=0,i=n.length;t<i;t++)if(n[t]!==e[t])return!1;return!0}function vt(n,e){for(let t=0,i=e.length;t<i;t++)n[t]=e[t]}function Gr(n,e){let t=Vo[e];t===void 0&&(t=new Int32Array(e),Vo[e]=t);for(let i=0;i!==e;++i)t[i]=n.allocateTextureUnit();return t}function Af(n,e){const t=this.cache;t[0]!==e&&(n.uniform1f(this.addr,e),t[0]=e)}function wf(n,e){const t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y)&&(n.uniform2f(this.addr,e.x,e.y),t[0]=e.x,t[1]=e.y);else{if(_t(t,e))return;n.uniform2fv(this.addr,e),vt(t,e)}}function Rf(n,e){const t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y||t[2]!==e.z)&&(n.uniform3f(this.addr,e.x,e.y,e.z),t[0]=e.x,t[1]=e.y,t[2]=e.z);else if(e.r!==void 0)(t[0]!==e.r||t[1]!==e.g||t[2]!==e.b)&&(n.uniform3f(this.addr,e.r,e.g,e.b),t[0]=e.r,t[1]=e.g,t[2]=e.b);else{if(_t(t,e))return;n.uniform3fv(this.addr,e),vt(t,e)}}function Cf(n,e){const t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y||t[2]!==e.z||t[3]!==e.w)&&(n.uniform4f(this.addr,e.x,e.y,e.z,e.w),t[0]=e.x,t[1]=e.y,t[2]=e.z,t[3]=e.w);else{if(_t(t,e))return;n.uniform4fv(this.addr,e),vt(t,e)}}function Pf(n,e){const t=this.cache,i=e.elements;if(i===void 0){if(_t(t,e))return;n.uniformMatrix2fv(this.addr,!1,e),vt(t,e)}else{if(_t(t,i))return;jo.set(i),n.uniformMatrix2fv(this.addr,!1,jo),vt(t,i)}}function Df(n,e){const t=this.cache,i=e.elements;if(i===void 0){if(_t(t,e))return;n.uniformMatrix3fv(this.addr,!1,e),vt(t,e)}else{if(_t(t,i))return;Go.set(i),n.uniformMatrix3fv(this.addr,!1,Go),vt(t,i)}}function Lf(n,e){const t=this.cache,i=e.elements;if(i===void 0){if(_t(t,e))return;n.uniformMatrix4fv(this.addr,!1,e),vt(t,e)}else{if(_t(t,i))return;Ho.set(i),n.uniformMatrix4fv(this.addr,!1,Ho),vt(t,i)}}function If(n,e){const t=this.cache;t[0]!==e&&(n.uniform1i(this.addr,e),t[0]=e)}function Uf(n,e){const t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y)&&(n.uniform2i(this.addr,e.x,e.y),t[0]=e.x,t[1]=e.y);else{if(_t(t,e))return;n.uniform2iv(this.addr,e),vt(t,e)}}function zf(n,e){const t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y||t[2]!==e.z)&&(n.uniform3i(this.addr,e.x,e.y,e.z),t[0]=e.x,t[1]=e.y,t[2]=e.z);else{if(_t(t,e))return;n.uniform3iv(this.addr,e),vt(t,e)}}function Nf(n,e){const t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y||t[2]!==e.z||t[3]!==e.w)&&(n.uniform4i(this.addr,e.x,e.y,e.z,e.w),t[0]=e.x,t[1]=e.y,t[2]=e.z,t[3]=e.w);else{if(_t(t,e))return;n.uniform4iv(this.addr,e),vt(t,e)}}function Ff(n,e){const t=this.cache;t[0]!==e&&(n.uniform1ui(this.addr,e),t[0]=e)}function kf(n,e){const t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y)&&(n.uniform2ui(this.addr,e.x,e.y),t[0]=e.x,t[1]=e.y);else{if(_t(t,e))return;n.uniform2uiv(this.addr,e),vt(t,e)}}function Of(n,e){const t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y||t[2]!==e.z)&&(n.uniform3ui(this.addr,e.x,e.y,e.z),t[0]=e.x,t[1]=e.y,t[2]=e.z);else{if(_t(t,e))return;n.uniform3uiv(this.addr,e),vt(t,e)}}function Bf(n,e){const t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y||t[2]!==e.z||t[3]!==e.w)&&(n.uniform4ui(this.addr,e.x,e.y,e.z,e.w),t[0]=e.x,t[1]=e.y,t[2]=e.z,t[3]=e.w);else{if(_t(t,e))return;n.uniform4uiv(this.addr,e),vt(t,e)}}function Vf(n,e,t){const i=this.cache,r=t.allocateTextureUnit();i[0]!==r&&(n.uniform1i(this.addr,r),i[0]=r);let a;this.type===n.SAMPLER_2D_SHADOW?(Oo.compareFunction=wc,a=Oo):a=Bc,t.setTexture2D(e||a,r)}function Hf(n,e,t){const i=this.cache,r=t.allocateTextureUnit();i[0]!==r&&(n.uniform1i(this.addr,r),i[0]=r),t.setTexture3D(e||Hc,r)}function Gf(n,e,t){const i=this.cache,r=t.allocateTextureUnit();i[0]!==r&&(n.uniform1i(this.addr,r),i[0]=r),t.setTextureCube(e||Gc,r)}function jf(n,e,t){const i=this.cache,r=t.allocateTextureUnit();i[0]!==r&&(n.uniform1i(this.addr,r),i[0]=r),t.setTexture2DArray(e||Vc,r)}function Wf(n){switch(n){case 5126:return Af;case 35664:return wf;case 35665:return Rf;case 35666:return Cf;case 35674:return Pf;case 35675:return Df;case 35676:return Lf;case 5124:case 35670:return If;case 35667:case 35671:return Uf;case 35668:case 35672:return zf;case 35669:case 35673:return Nf;case 5125:return Ff;case 36294:return kf;case 36295:return Of;case 36296:return Bf;case 35678:case 36198:case 36298:case 36306:case 35682:return Vf;case 35679:case 36299:case 36307:return Hf;case 35680:case 36300:case 36308:case 36293:return Gf;case 36289:case 36303:case 36311:case 36292:return jf}}function Xf(n,e){n.uniform1fv(this.addr,e)}function qf(n,e){const t=Ii(e,this.size,2);n.uniform2fv(this.addr,t)}function Yf(n,e){const t=Ii(e,this.size,3);n.uniform3fv(this.addr,t)}function Kf(n,e){const t=Ii(e,this.size,4);n.uniform4fv(this.addr,t)}function $f(n,e){const t=Ii(e,this.size,4);n.uniformMatrix2fv(this.addr,!1,t)}function Zf(n,e){const t=Ii(e,this.size,9);n.uniformMatrix3fv(this.addr,!1,t)}function Jf(n,e){const t=Ii(e,this.size,16);n.uniformMatrix4fv(this.addr,!1,t)}function Qf(n,e){n.uniform1iv(this.addr,e)}function ep(n,e){n.uniform2iv(this.addr,e)}function tp(n,e){n.uniform3iv(this.addr,e)}function np(n,e){n.uniform4iv(this.addr,e)}function ip(n,e){n.uniform1uiv(this.addr,e)}function rp(n,e){n.uniform2uiv(this.addr,e)}function ap(n,e){n.uniform3uiv(this.addr,e)}function sp(n,e){n.uniform4uiv(this.addr,e)}function op(n,e,t){const i=this.cache,r=e.length,a=Gr(t,r);_t(i,a)||(n.uniform1iv(this.addr,a),vt(i,a));for(let s=0;s!==r;++s)t.setTexture2D(e[s]||Bc,a[s])}function cp(n,e,t){const i=this.cache,r=e.length,a=Gr(t,r);_t(i,a)||(n.uniform1iv(this.addr,a),vt(i,a));for(let s=0;s!==r;++s)t.setTexture3D(e[s]||Hc,a[s])}function lp(n,e,t){const i=this.cache,r=e.length,a=Gr(t,r);_t(i,a)||(n.uniform1iv(this.addr,a),vt(i,a));for(let s=0;s!==r;++s)t.setTextureCube(e[s]||Gc,a[s])}function up(n,e,t){const i=this.cache,r=e.length,a=Gr(t,r);_t(i,a)||(n.uniform1iv(this.addr,a),vt(i,a));for(let s=0;s!==r;++s)t.setTexture2DArray(e[s]||Vc,a[s])}function dp(n){switch(n){case 5126:return Xf;case 35664:return qf;case 35665:return Yf;case 35666:return Kf;case 35674:return $f;case 35675:return Zf;case 35676:return Jf;case 5124:case 35670:return Qf;case 35667:case 35671:return ep;case 35668:case 35672:return tp;case 35669:case 35673:return np;case 5125:return ip;case 36294:return rp;case 36295:return ap;case 36296:return sp;case 35678:case 36198:case 36298:case 36306:case 35682:return op;case 35679:case 36299:case 36307:return cp;case 35680:case 36300:case 36308:case 36293:return lp;case 36289:case 36303:case 36311:case 36292:return up}}class hp{constructor(e,t,i){this.id=e,this.addr=i,this.cache=[],this.type=t.type,this.setValue=Wf(t.type)}}class fp{constructor(e,t,i){this.id=e,this.addr=i,this.cache=[],this.type=t.type,this.size=t.size,this.setValue=dp(t.type)}}class pp{constructor(e){this.id=e,this.seq=[],this.map={}}setValue(e,t,i){const r=this.seq;for(let a=0,s=r.length;a!==s;++a){const o=r[a];o.setValue(e,t[o.id],i)}}}const ba=/(\w+)(\])?(\[|\.)?/g;function Wo(n,e){n.seq.push(e),n.map[e.id]=e}function mp(n,e,t){const i=n.name,r=i.length;for(ba.lastIndex=0;;){const a=ba.exec(i),s=ba.lastIndex;let o=a[1];const c=a[2]==="]",l=a[3];if(c&&(o=o|0),l===void 0||l==="["&&s+2===r){Wo(t,l===void 0?new hp(o,n,e):new fp(o,n,e));break}else{let h=t.map[o];h===void 0&&(h=new pp(o),Wo(t,h)),t=h}}}class Ir{constructor(e,t){this.seq=[],this.map={};const i=e.getProgramParameter(t,e.ACTIVE_UNIFORMS);for(let r=0;r<i;++r){const a=e.getActiveUniform(t,r),s=e.getUniformLocation(t,a.name);mp(a,s,this)}}setValue(e,t,i,r){const a=this.map[t];a!==void 0&&a.setValue(e,i,r)}setOptional(e,t,i){const r=t[i];r!==void 0&&this.setValue(e,i,r)}static upload(e,t,i,r){for(let a=0,s=t.length;a!==s;++a){const o=t[a],c=i[o.id];c.needsUpdate!==!1&&o.setValue(e,c.value,r)}}static seqWithValue(e,t){const i=[];for(let r=0,a=e.length;r!==a;++r){const s=e[r];s.id in t&&i.push(s)}return i}}function Xo(n,e,t){const i=n.createShader(e);return n.shaderSource(i,t),n.compileShader(i),i}const gp=37297;let _p=0;function vp(n,e){const t=n.split(`
`),i=[],r=Math.max(e-6,0),a=Math.min(e+6,t.length);for(let s=r;s<a;s++){const o=s+1;i.push(`${o===e?">":" "} ${o}: ${t[s]}`)}return i.join(`
`)}const qo=new Be;function xp(n){Je._getMatrix(qo,Je.workingColorSpace,n);const e=`mat3( ${qo.elements.map(t=>t.toFixed(4))} )`;switch(Je.getTransfer(n)){case zr:return[e,"LinearTransferOETF"];case it:return[e,"sRGBTransferOETF"];default:return console.warn("THREE.WebGLProgram: Unsupported color space: ",n),[e,"LinearTransferOETF"]}}function Yo(n,e,t){const i=n.getShaderParameter(e,n.COMPILE_STATUS),r=n.getShaderInfoLog(e).trim();if(i&&r==="")return"";const a=/ERROR: 0:(\d+)/.exec(r);if(a){const s=parseInt(a[1]);return t.toUpperCase()+`

`+r+`

`+vp(n.getShaderSource(e),s)}else return r}function Mp(n,e){const t=xp(e);return[`vec4 ${n}( vec4 value ) {`,`	return ${t[1]}( vec4( value.rgb * ${t[0]}, value.a ) );`,"}"].join(`
`)}function Sp(n,e){let t;switch(e){case bl:t="Linear";break;case Tl:t="Reinhard";break;case Al:t="Cineon";break;case wl:t="ACESFilmic";break;case Cl:t="AgX";break;case Pl:t="Neutral";break;case Rl:t="Custom";break;default:console.warn("THREE.WebGLProgram: Unsupported toneMapping:",e),t="Linear"}return"vec3 "+n+"( vec3 color ) { return "+t+"ToneMapping( color ); }"}const Tr=new k;function Ep(){Je.getLuminanceCoefficients(Tr);const n=Tr.x.toFixed(4),e=Tr.y.toFixed(4),t=Tr.z.toFixed(4);return["float luminance( const in vec3 rgb ) {",`	const vec3 weights = vec3( ${n}, ${e}, ${t} );`,"	return dot( weights, rgb );","}"].join(`
`)}function yp(n){return[n.extensionClipCullDistance?"#extension GL_ANGLE_clip_cull_distance : require":"",n.extensionMultiDraw?"#extension GL_ANGLE_multi_draw : require":""].filter(Hi).join(`
`)}function bp(n){const e=[];for(const t in n){const i=n[t];i!==!1&&e.push("#define "+t+" "+i)}return e.join(`
`)}function Tp(n,e){const t={},i=n.getProgramParameter(e,n.ACTIVE_ATTRIBUTES);for(let r=0;r<i;r++){const a=n.getActiveAttrib(e,r),s=a.name;let o=1;a.type===n.FLOAT_MAT2&&(o=2),a.type===n.FLOAT_MAT3&&(o=3),a.type===n.FLOAT_MAT4&&(o=4),t[s]={type:a.type,location:n.getAttribLocation(e,s),locationSize:o}}return t}function Hi(n){return n!==""}function Ko(n,e){const t=e.numSpotLightShadows+e.numSpotLightMaps-e.numSpotLightShadowsWithMaps;return n.replace(/NUM_DIR_LIGHTS/g,e.numDirLights).replace(/NUM_SPOT_LIGHTS/g,e.numSpotLights).replace(/NUM_SPOT_LIGHT_MAPS/g,e.numSpotLightMaps).replace(/NUM_SPOT_LIGHT_COORDS/g,t).replace(/NUM_RECT_AREA_LIGHTS/g,e.numRectAreaLights).replace(/NUM_POINT_LIGHTS/g,e.numPointLights).replace(/NUM_HEMI_LIGHTS/g,e.numHemiLights).replace(/NUM_DIR_LIGHT_SHADOWS/g,e.numDirLightShadows).replace(/NUM_SPOT_LIGHT_SHADOWS_WITH_MAPS/g,e.numSpotLightShadowsWithMaps).replace(/NUM_SPOT_LIGHT_SHADOWS/g,e.numSpotLightShadows).replace(/NUM_POINT_LIGHT_SHADOWS/g,e.numPointLightShadows)}function $o(n,e){return n.replace(/NUM_CLIPPING_PLANES/g,e.numClippingPlanes).replace(/UNION_CLIPPING_PLANES/g,e.numClippingPlanes-e.numClipIntersection)}const Ap=/^[ \t]*#include +<([\w\d./]+)>/gm;function vs(n){return n.replace(Ap,Rp)}const wp=new Map;function Rp(n,e){let t=He[e];if(t===void 0){const i=wp.get(e);if(i!==void 0)t=He[i],console.warn('THREE.WebGLRenderer: Shader chunk "%s" has been deprecated. Use "%s" instead.',e,i);else throw new Error("Can not resolve #include <"+e+">")}return vs(t)}const Cp=/#pragma unroll_loop_start\s+for\s*\(\s*int\s+i\s*=\s*(\d+)\s*;\s*i\s*<\s*(\d+)\s*;\s*i\s*\+\+\s*\)\s*{([\s\S]+?)}\s+#pragma unroll_loop_end/g;function Zo(n){return n.replace(Cp,Pp)}function Pp(n,e,t,i){let r="";for(let a=parseInt(e);a<parseInt(t);a++)r+=i.replace(/\[\s*i\s*\]/g,"[ "+a+" ]").replace(/UNROLLED_LOOP_INDEX/g,a);return r}function Jo(n){let e=`precision ${n.precision} float;
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
#define LOW_PRECISION`),e}function Dp(n){let e="SHADOWMAP_TYPE_BASIC";return n.shadowMapType===fc?e="SHADOWMAP_TYPE_PCF":n.shadowMapType===il?e="SHADOWMAP_TYPE_PCF_SOFT":n.shadowMapType===cn&&(e="SHADOWMAP_TYPE_VSM"),e}function Lp(n){let e="ENVMAP_TYPE_CUBE";if(n.envMap)switch(n.envMapMode){case yi:case bi:e="ENVMAP_TYPE_CUBE";break;case Vr:e="ENVMAP_TYPE_CUBE_UV";break}return e}function Ip(n){let e="ENVMAP_MODE_REFLECTION";if(n.envMap)switch(n.envMapMode){case bi:e="ENVMAP_MODE_REFRACTION";break}return e}function Up(n){let e="ENVMAP_BLENDING_NONE";if(n.envMap)switch(n.combine){case pc:e="ENVMAP_BLENDING_MULTIPLY";break;case El:e="ENVMAP_BLENDING_MIX";break;case yl:e="ENVMAP_BLENDING_ADD";break}return e}function zp(n){const e=n.envMapCubeUVHeight;if(e===null)return null;const t=Math.log2(e)-2,i=1/e;return{texelWidth:1/(3*Math.max(Math.pow(2,t),112)),texelHeight:i,maxMip:t}}function Np(n,e,t,i){const r=n.getContext(),a=t.defines;let s=t.vertexShader,o=t.fragmentShader;const c=Dp(t),l=Lp(t),d=Ip(t),h=Up(t),f=zp(t),m=yp(t),g=bp(a),_=r.createProgram();let p,u,y=t.glslVersion?"#version "+t.glslVersion+`
`:"";t.isRawShaderMaterial?(p=["#define SHADER_TYPE "+t.shaderType,"#define SHADER_NAME "+t.shaderName,g].filter(Hi).join(`
`),p.length>0&&(p+=`
`),u=["#define SHADER_TYPE "+t.shaderType,"#define SHADER_NAME "+t.shaderName,g].filter(Hi).join(`
`),u.length>0&&(u+=`
`)):(p=[Jo(t),"#define SHADER_TYPE "+t.shaderType,"#define SHADER_NAME "+t.shaderName,g,t.extensionClipCullDistance?"#define USE_CLIP_DISTANCE":"",t.batching?"#define USE_BATCHING":"",t.batchingColor?"#define USE_BATCHING_COLOR":"",t.instancing?"#define USE_INSTANCING":"",t.instancingColor?"#define USE_INSTANCING_COLOR":"",t.instancingMorph?"#define USE_INSTANCING_MORPH":"",t.useFog&&t.fog?"#define USE_FOG":"",t.useFog&&t.fogExp2?"#define FOG_EXP2":"",t.map?"#define USE_MAP":"",t.envMap?"#define USE_ENVMAP":"",t.envMap?"#define "+d:"",t.lightMap?"#define USE_LIGHTMAP":"",t.aoMap?"#define USE_AOMAP":"",t.bumpMap?"#define USE_BUMPMAP":"",t.normalMap?"#define USE_NORMALMAP":"",t.normalMapObjectSpace?"#define USE_NORMALMAP_OBJECTSPACE":"",t.normalMapTangentSpace?"#define USE_NORMALMAP_TANGENTSPACE":"",t.displacementMap?"#define USE_DISPLACEMENTMAP":"",t.emissiveMap?"#define USE_EMISSIVEMAP":"",t.anisotropy?"#define USE_ANISOTROPY":"",t.anisotropyMap?"#define USE_ANISOTROPYMAP":"",t.clearcoatMap?"#define USE_CLEARCOATMAP":"",t.clearcoatRoughnessMap?"#define USE_CLEARCOAT_ROUGHNESSMAP":"",t.clearcoatNormalMap?"#define USE_CLEARCOAT_NORMALMAP":"",t.iridescenceMap?"#define USE_IRIDESCENCEMAP":"",t.iridescenceThicknessMap?"#define USE_IRIDESCENCE_THICKNESSMAP":"",t.specularMap?"#define USE_SPECULARMAP":"",t.specularColorMap?"#define USE_SPECULAR_COLORMAP":"",t.specularIntensityMap?"#define USE_SPECULAR_INTENSITYMAP":"",t.roughnessMap?"#define USE_ROUGHNESSMAP":"",t.metalnessMap?"#define USE_METALNESSMAP":"",t.alphaMap?"#define USE_ALPHAMAP":"",t.alphaHash?"#define USE_ALPHAHASH":"",t.transmission?"#define USE_TRANSMISSION":"",t.transmissionMap?"#define USE_TRANSMISSIONMAP":"",t.thicknessMap?"#define USE_THICKNESSMAP":"",t.sheenColorMap?"#define USE_SHEEN_COLORMAP":"",t.sheenRoughnessMap?"#define USE_SHEEN_ROUGHNESSMAP":"",t.mapUv?"#define MAP_UV "+t.mapUv:"",t.alphaMapUv?"#define ALPHAMAP_UV "+t.alphaMapUv:"",t.lightMapUv?"#define LIGHTMAP_UV "+t.lightMapUv:"",t.aoMapUv?"#define AOMAP_UV "+t.aoMapUv:"",t.emissiveMapUv?"#define EMISSIVEMAP_UV "+t.emissiveMapUv:"",t.bumpMapUv?"#define BUMPMAP_UV "+t.bumpMapUv:"",t.normalMapUv?"#define NORMALMAP_UV "+t.normalMapUv:"",t.displacementMapUv?"#define DISPLACEMENTMAP_UV "+t.displacementMapUv:"",t.metalnessMapUv?"#define METALNESSMAP_UV "+t.metalnessMapUv:"",t.roughnessMapUv?"#define ROUGHNESSMAP_UV "+t.roughnessMapUv:"",t.anisotropyMapUv?"#define ANISOTROPYMAP_UV "+t.anisotropyMapUv:"",t.clearcoatMapUv?"#define CLEARCOATMAP_UV "+t.clearcoatMapUv:"",t.clearcoatNormalMapUv?"#define CLEARCOAT_NORMALMAP_UV "+t.clearcoatNormalMapUv:"",t.clearcoatRoughnessMapUv?"#define CLEARCOAT_ROUGHNESSMAP_UV "+t.clearcoatRoughnessMapUv:"",t.iridescenceMapUv?"#define IRIDESCENCEMAP_UV "+t.iridescenceMapUv:"",t.iridescenceThicknessMapUv?"#define IRIDESCENCE_THICKNESSMAP_UV "+t.iridescenceThicknessMapUv:"",t.sheenColorMapUv?"#define SHEEN_COLORMAP_UV "+t.sheenColorMapUv:"",t.sheenRoughnessMapUv?"#define SHEEN_ROUGHNESSMAP_UV "+t.sheenRoughnessMapUv:"",t.specularMapUv?"#define SPECULARMAP_UV "+t.specularMapUv:"",t.specularColorMapUv?"#define SPECULAR_COLORMAP_UV "+t.specularColorMapUv:"",t.specularIntensityMapUv?"#define SPECULAR_INTENSITYMAP_UV "+t.specularIntensityMapUv:"",t.transmissionMapUv?"#define TRANSMISSIONMAP_UV "+t.transmissionMapUv:"",t.thicknessMapUv?"#define THICKNESSMAP_UV "+t.thicknessMapUv:"",t.vertexTangents&&t.flatShading===!1?"#define USE_TANGENT":"",t.vertexColors?"#define USE_COLOR":"",t.vertexAlphas?"#define USE_COLOR_ALPHA":"",t.vertexUv1s?"#define USE_UV1":"",t.vertexUv2s?"#define USE_UV2":"",t.vertexUv3s?"#define USE_UV3":"",t.pointsUvs?"#define USE_POINTS_UV":"",t.flatShading?"#define FLAT_SHADED":"",t.skinning?"#define USE_SKINNING":"",t.morphTargets?"#define USE_MORPHTARGETS":"",t.morphNormals&&t.flatShading===!1?"#define USE_MORPHNORMALS":"",t.morphColors?"#define USE_MORPHCOLORS":"",t.morphTargetsCount>0?"#define MORPHTARGETS_TEXTURE_STRIDE "+t.morphTextureStride:"",t.morphTargetsCount>0?"#define MORPHTARGETS_COUNT "+t.morphTargetsCount:"",t.doubleSided?"#define DOUBLE_SIDED":"",t.flipSided?"#define FLIP_SIDED":"",t.shadowMapEnabled?"#define USE_SHADOWMAP":"",t.shadowMapEnabled?"#define "+c:"",t.sizeAttenuation?"#define USE_SIZEATTENUATION":"",t.numLightProbes>0?"#define USE_LIGHT_PROBES":"",t.logarithmicDepthBuffer?"#define USE_LOGDEPTHBUF":"",t.reverseDepthBuffer?"#define USE_REVERSEDEPTHBUF":"","uniform mat4 modelMatrix;","uniform mat4 modelViewMatrix;","uniform mat4 projectionMatrix;","uniform mat4 viewMatrix;","uniform mat3 normalMatrix;","uniform vec3 cameraPosition;","uniform bool isOrthographic;","#ifdef USE_INSTANCING","	attribute mat4 instanceMatrix;","#endif","#ifdef USE_INSTANCING_COLOR","	attribute vec3 instanceColor;","#endif","#ifdef USE_INSTANCING_MORPH","	uniform sampler2D morphTexture;","#endif","attribute vec3 position;","attribute vec3 normal;","attribute vec2 uv;","#ifdef USE_UV1","	attribute vec2 uv1;","#endif","#ifdef USE_UV2","	attribute vec2 uv2;","#endif","#ifdef USE_UV3","	attribute vec2 uv3;","#endif","#ifdef USE_TANGENT","	attribute vec4 tangent;","#endif","#if defined( USE_COLOR_ALPHA )","	attribute vec4 color;","#elif defined( USE_COLOR )","	attribute vec3 color;","#endif","#ifdef USE_SKINNING","	attribute vec4 skinIndex;","	attribute vec4 skinWeight;","#endif",`
`].filter(Hi).join(`
`),u=[Jo(t),"#define SHADER_TYPE "+t.shaderType,"#define SHADER_NAME "+t.shaderName,g,t.useFog&&t.fog?"#define USE_FOG":"",t.useFog&&t.fogExp2?"#define FOG_EXP2":"",t.alphaToCoverage?"#define ALPHA_TO_COVERAGE":"",t.map?"#define USE_MAP":"",t.matcap?"#define USE_MATCAP":"",t.envMap?"#define USE_ENVMAP":"",t.envMap?"#define "+l:"",t.envMap?"#define "+d:"",t.envMap?"#define "+h:"",f?"#define CUBEUV_TEXEL_WIDTH "+f.texelWidth:"",f?"#define CUBEUV_TEXEL_HEIGHT "+f.texelHeight:"",f?"#define CUBEUV_MAX_MIP "+f.maxMip+".0":"",t.lightMap?"#define USE_LIGHTMAP":"",t.aoMap?"#define USE_AOMAP":"",t.bumpMap?"#define USE_BUMPMAP":"",t.normalMap?"#define USE_NORMALMAP":"",t.normalMapObjectSpace?"#define USE_NORMALMAP_OBJECTSPACE":"",t.normalMapTangentSpace?"#define USE_NORMALMAP_TANGENTSPACE":"",t.emissiveMap?"#define USE_EMISSIVEMAP":"",t.anisotropy?"#define USE_ANISOTROPY":"",t.anisotropyMap?"#define USE_ANISOTROPYMAP":"",t.clearcoat?"#define USE_CLEARCOAT":"",t.clearcoatMap?"#define USE_CLEARCOATMAP":"",t.clearcoatRoughnessMap?"#define USE_CLEARCOAT_ROUGHNESSMAP":"",t.clearcoatNormalMap?"#define USE_CLEARCOAT_NORMALMAP":"",t.dispersion?"#define USE_DISPERSION":"",t.iridescence?"#define USE_IRIDESCENCE":"",t.iridescenceMap?"#define USE_IRIDESCENCEMAP":"",t.iridescenceThicknessMap?"#define USE_IRIDESCENCE_THICKNESSMAP":"",t.specularMap?"#define USE_SPECULARMAP":"",t.specularColorMap?"#define USE_SPECULAR_COLORMAP":"",t.specularIntensityMap?"#define USE_SPECULAR_INTENSITYMAP":"",t.roughnessMap?"#define USE_ROUGHNESSMAP":"",t.metalnessMap?"#define USE_METALNESSMAP":"",t.alphaMap?"#define USE_ALPHAMAP":"",t.alphaTest?"#define USE_ALPHATEST":"",t.alphaHash?"#define USE_ALPHAHASH":"",t.sheen?"#define USE_SHEEN":"",t.sheenColorMap?"#define USE_SHEEN_COLORMAP":"",t.sheenRoughnessMap?"#define USE_SHEEN_ROUGHNESSMAP":"",t.transmission?"#define USE_TRANSMISSION":"",t.transmissionMap?"#define USE_TRANSMISSIONMAP":"",t.thicknessMap?"#define USE_THICKNESSMAP":"",t.vertexTangents&&t.flatShading===!1?"#define USE_TANGENT":"",t.vertexColors||t.instancingColor||t.batchingColor?"#define USE_COLOR":"",t.vertexAlphas?"#define USE_COLOR_ALPHA":"",t.vertexUv1s?"#define USE_UV1":"",t.vertexUv2s?"#define USE_UV2":"",t.vertexUv3s?"#define USE_UV3":"",t.pointsUvs?"#define USE_POINTS_UV":"",t.gradientMap?"#define USE_GRADIENTMAP":"",t.flatShading?"#define FLAT_SHADED":"",t.doubleSided?"#define DOUBLE_SIDED":"",t.flipSided?"#define FLIP_SIDED":"",t.shadowMapEnabled?"#define USE_SHADOWMAP":"",t.shadowMapEnabled?"#define "+c:"",t.premultipliedAlpha?"#define PREMULTIPLIED_ALPHA":"",t.numLightProbes>0?"#define USE_LIGHT_PROBES":"",t.decodeVideoTexture?"#define DECODE_VIDEO_TEXTURE":"",t.decodeVideoTextureEmissive?"#define DECODE_VIDEO_TEXTURE_EMISSIVE":"",t.logarithmicDepthBuffer?"#define USE_LOGDEPTHBUF":"",t.reverseDepthBuffer?"#define USE_REVERSEDEPTHBUF":"","uniform mat4 viewMatrix;","uniform vec3 cameraPosition;","uniform bool isOrthographic;",t.toneMapping!==Cn?"#define TONE_MAPPING":"",t.toneMapping!==Cn?He.tonemapping_pars_fragment:"",t.toneMapping!==Cn?Sp("toneMapping",t.toneMapping):"",t.dithering?"#define DITHERING":"",t.opaque?"#define OPAQUE":"",He.colorspace_pars_fragment,Mp("linearToOutputTexel",t.outputColorSpace),Ep(),t.useDepthPacking?"#define DEPTH_PACKING "+t.depthPacking:"",`
`].filter(Hi).join(`
`)),s=vs(s),s=Ko(s,t),s=$o(s,t),o=vs(o),o=Ko(o,t),o=$o(o,t),s=Zo(s),o=Zo(o),t.isRawShaderMaterial!==!0&&(y=`#version 300 es
`,p=[m,"#define attribute in","#define varying out","#define texture2D texture"].join(`
`)+`
`+p,u=["#define varying in",t.glslVersion===io?"":"layout(location = 0) out highp vec4 pc_fragColor;",t.glslVersion===io?"":"#define gl_FragColor pc_fragColor","#define gl_FragDepthEXT gl_FragDepth","#define texture2D texture","#define textureCube texture","#define texture2DProj textureProj","#define texture2DLodEXT textureLod","#define texture2DProjLodEXT textureProjLod","#define textureCubeLodEXT textureLod","#define texture2DGradEXT textureGrad","#define texture2DProjGradEXT textureProjGrad","#define textureCubeGradEXT textureGrad"].join(`
`)+`
`+u);const S=y+p+s,M=y+u+o,T=Xo(r,r.VERTEX_SHADER,S),b=Xo(r,r.FRAGMENT_SHADER,M);r.attachShader(_,T),r.attachShader(_,b),t.index0AttributeName!==void 0?r.bindAttribLocation(_,0,t.index0AttributeName):t.morphTargets===!0&&r.bindAttribLocation(_,0,"position"),r.linkProgram(_);function w(R){if(n.debug.checkShaderErrors){const U=r.getProgramInfoLog(_).trim(),C=r.getShaderInfoLog(T).trim(),P=r.getShaderInfoLog(b).trim();let F=!0,N=!0;if(r.getProgramParameter(_,r.LINK_STATUS)===!1)if(F=!1,typeof n.debug.onShaderError=="function")n.debug.onShaderError(r,_,T,b);else{const O=Yo(r,T,"vertex"),z=Yo(r,b,"fragment");console.error("THREE.WebGLProgram: Shader Error "+r.getError()+" - VALIDATE_STATUS "+r.getProgramParameter(_,r.VALIDATE_STATUS)+`

Material Name: `+R.name+`
Material Type: `+R.type+`

Program Info Log: `+U+`
`+O+`
`+z)}else U!==""?console.warn("THREE.WebGLProgram: Program Info Log:",U):(C===""||P==="")&&(N=!1);N&&(R.diagnostics={runnable:F,programLog:U,vertexShader:{log:C,prefix:p},fragmentShader:{log:P,prefix:u}})}r.deleteShader(T),r.deleteShader(b),L=new Ir(r,_),x=Tp(r,_)}let L;this.getUniforms=function(){return L===void 0&&w(this),L};let x;this.getAttributes=function(){return x===void 0&&w(this),x};let v=t.rendererExtensionParallelShaderCompile===!1;return this.isReady=function(){return v===!1&&(v=r.getProgramParameter(_,gp)),v},this.destroy=function(){i.releaseStatesOfProgram(this),r.deleteProgram(_),this.program=void 0},this.type=t.shaderType,this.name=t.shaderName,this.id=_p++,this.cacheKey=e,this.usedTimes=1,this.program=_,this.vertexShader=T,this.fragmentShader=b,this}let Fp=0;class kp{constructor(){this.shaderCache=new Map,this.materialCache=new Map}update(e){const t=e.vertexShader,i=e.fragmentShader,r=this._getShaderStage(t),a=this._getShaderStage(i),s=this._getShaderCacheForMaterial(e);return s.has(r)===!1&&(s.add(r),r.usedTimes++),s.has(a)===!1&&(s.add(a),a.usedTimes++),this}remove(e){const t=this.materialCache.get(e);for(const i of t)i.usedTimes--,i.usedTimes===0&&this.shaderCache.delete(i.code);return this.materialCache.delete(e),this}getVertexShaderID(e){return this._getShaderStage(e.vertexShader).id}getFragmentShaderID(e){return this._getShaderStage(e.fragmentShader).id}dispose(){this.shaderCache.clear(),this.materialCache.clear()}_getShaderCacheForMaterial(e){const t=this.materialCache;let i=t.get(e);return i===void 0&&(i=new Set,t.set(e,i)),i}_getShaderStage(e){const t=this.shaderCache;let i=t.get(e);return i===void 0&&(i=new Op(e),t.set(e,i)),i}}class Op{constructor(e){this.id=Fp++,this.code=e,this.usedTimes=0}}function Bp(n,e,t,i,r,a,s){const o=new Ls,c=new kp,l=new Set,d=[],h=r.logarithmicDepthBuffer,f=r.vertexTextures;let m=r.precision;const g={MeshDepthMaterial:"depth",MeshDistanceMaterial:"distanceRGBA",MeshNormalMaterial:"normal",MeshBasicMaterial:"basic",MeshLambertMaterial:"lambert",MeshPhongMaterial:"phong",MeshToonMaterial:"toon",MeshStandardMaterial:"physical",MeshPhysicalMaterial:"physical",MeshMatcapMaterial:"matcap",LineBasicMaterial:"basic",LineDashedMaterial:"dashed",PointsMaterial:"points",ShadowMaterial:"shadow",SpriteMaterial:"sprite"};function _(x){return l.add(x),x===0?"uv":`uv${x}`}function p(x,v,R,U,C){const P=U.fog,F=C.geometry,N=x.isMeshStandardMaterial?U.environment:null,O=(x.isMeshStandardMaterial?t:e).get(x.envMap||N),z=O&&O.mapping===Vr?O.image.height:null,G=g[x.type];x.precision!==null&&(m=r.getMaxPrecision(x.precision),m!==x.precision&&console.warn("THREE.WebGLProgram.getParameters:",x.precision,"not supported, using",m,"instead."));const K=F.morphAttributes.position||F.morphAttributes.normal||F.morphAttributes.color,$=K!==void 0?K.length:0;let fe=0;F.morphAttributes.position!==void 0&&(fe=1),F.morphAttributes.normal!==void 0&&(fe=2),F.morphAttributes.color!==void 0&&(fe=3);let De,X,ne,ue;if(G){const tt=$t[G];De=tt.vertexShader,X=tt.fragmentShader}else De=x.vertexShader,X=x.fragmentShader,c.update(x),ne=c.getVertexShaderID(x),ue=c.getFragmentShaderID(x);const se=n.getRenderTarget(),ee=n.state.buffers.depth.getReversed(),_e=C.isInstancedMesh===!0,de=C.isBatchedMesh===!0,Z=!!x.map,re=!!x.matcap,ae=!!O,I=!!x.aoMap,Ie=!!x.lightMap,Ce=!!x.bumpMap,Re=!!x.normalMap,Me=!!x.displacementMap,ke=!!x.emissiveMap,we=!!x.metalnessMap,D=!!x.roughnessMap,E=x.anisotropy>0,j=x.clearcoat>0,Q=x.dispersion>0,ie=x.iridescence>0,J=x.sheen>0,Ae=x.transmission>0,ge=E&&!!x.anisotropyMap,Ee=j&&!!x.clearcoatMap,Ke=j&&!!x.clearcoatNormalMap,le=j&&!!x.clearcoatRoughnessMap,ye=ie&&!!x.iridescenceMap,Ue=ie&&!!x.iridescenceThicknessMap,ze=J&&!!x.sheenColorMap,be=J&&!!x.sheenRoughnessMap,qe=!!x.specularMap,Ve=!!x.specularColorMap,rt=!!x.specularIntensityMap,B=Ae&&!!x.transmissionMap,pe=Ae&&!!x.thicknessMap,Y=!!x.gradientMap,te=!!x.alphaMap,xe=x.alphaTest>0,ve=!!x.alphaHash,Oe=!!x.extensions;let lt=Cn;x.toneMapped&&(se===null||se.isXRRenderTarget===!0)&&(lt=n.toneMapping);const yt={shaderID:G,shaderType:x.type,shaderName:x.name,vertexShader:De,fragmentShader:X,defines:x.defines,customVertexShaderID:ne,customFragmentShaderID:ue,isRawShaderMaterial:x.isRawShaderMaterial===!0,glslVersion:x.glslVersion,precision:m,batching:de,batchingColor:de&&C._colorsTexture!==null,instancing:_e,instancingColor:_e&&C.instanceColor!==null,instancingMorph:_e&&C.morphTexture!==null,supportsVertexTextures:f,outputColorSpace:se===null?n.outputColorSpace:se.isXRRenderTarget===!0?se.texture.colorSpace:wi,alphaToCoverage:!!x.alphaToCoverage,map:Z,matcap:re,envMap:ae,envMapMode:ae&&O.mapping,envMapCubeUVHeight:z,aoMap:I,lightMap:Ie,bumpMap:Ce,normalMap:Re,displacementMap:f&&Me,emissiveMap:ke,normalMapObjectSpace:Re&&x.normalMapType===Ul,normalMapTangentSpace:Re&&x.normalMapType===Ac,metalnessMap:we,roughnessMap:D,anisotropy:E,anisotropyMap:ge,clearcoat:j,clearcoatMap:Ee,clearcoatNormalMap:Ke,clearcoatRoughnessMap:le,dispersion:Q,iridescence:ie,iridescenceMap:ye,iridescenceThicknessMap:Ue,sheen:J,sheenColorMap:ze,sheenRoughnessMap:be,specularMap:qe,specularColorMap:Ve,specularIntensityMap:rt,transmission:Ae,transmissionMap:B,thicknessMap:pe,gradientMap:Y,opaque:x.transparent===!1&&x.blending===xi&&x.alphaToCoverage===!1,alphaMap:te,alphaTest:xe,alphaHash:ve,combine:x.combine,mapUv:Z&&_(x.map.channel),aoMapUv:I&&_(x.aoMap.channel),lightMapUv:Ie&&_(x.lightMap.channel),bumpMapUv:Ce&&_(x.bumpMap.channel),normalMapUv:Re&&_(x.normalMap.channel),displacementMapUv:Me&&_(x.displacementMap.channel),emissiveMapUv:ke&&_(x.emissiveMap.channel),metalnessMapUv:we&&_(x.metalnessMap.channel),roughnessMapUv:D&&_(x.roughnessMap.channel),anisotropyMapUv:ge&&_(x.anisotropyMap.channel),clearcoatMapUv:Ee&&_(x.clearcoatMap.channel),clearcoatNormalMapUv:Ke&&_(x.clearcoatNormalMap.channel),clearcoatRoughnessMapUv:le&&_(x.clearcoatRoughnessMap.channel),iridescenceMapUv:ye&&_(x.iridescenceMap.channel),iridescenceThicknessMapUv:Ue&&_(x.iridescenceThicknessMap.channel),sheenColorMapUv:ze&&_(x.sheenColorMap.channel),sheenRoughnessMapUv:be&&_(x.sheenRoughnessMap.channel),specularMapUv:qe&&_(x.specularMap.channel),specularColorMapUv:Ve&&_(x.specularColorMap.channel),specularIntensityMapUv:rt&&_(x.specularIntensityMap.channel),transmissionMapUv:B&&_(x.transmissionMap.channel),thicknessMapUv:pe&&_(x.thicknessMap.channel),alphaMapUv:te&&_(x.alphaMap.channel),vertexTangents:!!F.attributes.tangent&&(Re||E),vertexColors:x.vertexColors,vertexAlphas:x.vertexColors===!0&&!!F.attributes.color&&F.attributes.color.itemSize===4,pointsUvs:C.isPoints===!0&&!!F.attributes.uv&&(Z||te),fog:!!P,useFog:x.fog===!0,fogExp2:!!P&&P.isFogExp2,flatShading:x.flatShading===!0,sizeAttenuation:x.sizeAttenuation===!0,logarithmicDepthBuffer:h,reverseDepthBuffer:ee,skinning:C.isSkinnedMesh===!0,morphTargets:F.morphAttributes.position!==void 0,morphNormals:F.morphAttributes.normal!==void 0,morphColors:F.morphAttributes.color!==void 0,morphTargetsCount:$,morphTextureStride:fe,numDirLights:v.directional.length,numPointLights:v.point.length,numSpotLights:v.spot.length,numSpotLightMaps:v.spotLightMap.length,numRectAreaLights:v.rectArea.length,numHemiLights:v.hemi.length,numDirLightShadows:v.directionalShadowMap.length,numPointLightShadows:v.pointShadowMap.length,numSpotLightShadows:v.spotShadowMap.length,numSpotLightShadowsWithMaps:v.numSpotLightShadowsWithMaps,numLightProbes:v.numLightProbes,numClippingPlanes:s.numPlanes,numClipIntersection:s.numIntersection,dithering:x.dithering,shadowMapEnabled:n.shadowMap.enabled&&R.length>0,shadowMapType:n.shadowMap.type,toneMapping:lt,decodeVideoTexture:Z&&x.map.isVideoTexture===!0&&Je.getTransfer(x.map.colorSpace)===it,decodeVideoTextureEmissive:ke&&x.emissiveMap.isVideoTexture===!0&&Je.getTransfer(x.emissiveMap.colorSpace)===it,premultipliedAlpha:x.premultipliedAlpha,doubleSided:x.side===mt,flipSided:x.side===Dt,useDepthPacking:x.depthPacking>=0,depthPacking:x.depthPacking||0,index0AttributeName:x.index0AttributeName,extensionClipCullDistance:Oe&&x.extensions.clipCullDistance===!0&&i.has("WEBGL_clip_cull_distance"),extensionMultiDraw:(Oe&&x.extensions.multiDraw===!0||de)&&i.has("WEBGL_multi_draw"),rendererExtensionParallelShaderCompile:i.has("KHR_parallel_shader_compile"),customProgramCacheKey:x.customProgramCacheKey()};return yt.vertexUv1s=l.has(1),yt.vertexUv2s=l.has(2),yt.vertexUv3s=l.has(3),l.clear(),yt}function u(x){const v=[];if(x.shaderID?v.push(x.shaderID):(v.push(x.customVertexShaderID),v.push(x.customFragmentShaderID)),x.defines!==void 0)for(const R in x.defines)v.push(R),v.push(x.defines[R]);return x.isRawShaderMaterial===!1&&(y(v,x),S(v,x),v.push(n.outputColorSpace)),v.push(x.customProgramCacheKey),v.join()}function y(x,v){x.push(v.precision),x.push(v.outputColorSpace),x.push(v.envMapMode),x.push(v.envMapCubeUVHeight),x.push(v.mapUv),x.push(v.alphaMapUv),x.push(v.lightMapUv),x.push(v.aoMapUv),x.push(v.bumpMapUv),x.push(v.normalMapUv),x.push(v.displacementMapUv),x.push(v.emissiveMapUv),x.push(v.metalnessMapUv),x.push(v.roughnessMapUv),x.push(v.anisotropyMapUv),x.push(v.clearcoatMapUv),x.push(v.clearcoatNormalMapUv),x.push(v.clearcoatRoughnessMapUv),x.push(v.iridescenceMapUv),x.push(v.iridescenceThicknessMapUv),x.push(v.sheenColorMapUv),x.push(v.sheenRoughnessMapUv),x.push(v.specularMapUv),x.push(v.specularColorMapUv),x.push(v.specularIntensityMapUv),x.push(v.transmissionMapUv),x.push(v.thicknessMapUv),x.push(v.combine),x.push(v.fogExp2),x.push(v.sizeAttenuation),x.push(v.morphTargetsCount),x.push(v.morphAttributeCount),x.push(v.numDirLights),x.push(v.numPointLights),x.push(v.numSpotLights),x.push(v.numSpotLightMaps),x.push(v.numHemiLights),x.push(v.numRectAreaLights),x.push(v.numDirLightShadows),x.push(v.numPointLightShadows),x.push(v.numSpotLightShadows),x.push(v.numSpotLightShadowsWithMaps),x.push(v.numLightProbes),x.push(v.shadowMapType),x.push(v.toneMapping),x.push(v.numClippingPlanes),x.push(v.numClipIntersection),x.push(v.depthPacking)}function S(x,v){o.disableAll(),v.supportsVertexTextures&&o.enable(0),v.instancing&&o.enable(1),v.instancingColor&&o.enable(2),v.instancingMorph&&o.enable(3),v.matcap&&o.enable(4),v.envMap&&o.enable(5),v.normalMapObjectSpace&&o.enable(6),v.normalMapTangentSpace&&o.enable(7),v.clearcoat&&o.enable(8),v.iridescence&&o.enable(9),v.alphaTest&&o.enable(10),v.vertexColors&&o.enable(11),v.vertexAlphas&&o.enable(12),v.vertexUv1s&&o.enable(13),v.vertexUv2s&&o.enable(14),v.vertexUv3s&&o.enable(15),v.vertexTangents&&o.enable(16),v.anisotropy&&o.enable(17),v.alphaHash&&o.enable(18),v.batching&&o.enable(19),v.dispersion&&o.enable(20),v.batchingColor&&o.enable(21),x.push(o.mask),o.disableAll(),v.fog&&o.enable(0),v.useFog&&o.enable(1),v.flatShading&&o.enable(2),v.logarithmicDepthBuffer&&o.enable(3),v.reverseDepthBuffer&&o.enable(4),v.skinning&&o.enable(5),v.morphTargets&&o.enable(6),v.morphNormals&&o.enable(7),v.morphColors&&o.enable(8),v.premultipliedAlpha&&o.enable(9),v.shadowMapEnabled&&o.enable(10),v.doubleSided&&o.enable(11),v.flipSided&&o.enable(12),v.useDepthPacking&&o.enable(13),v.dithering&&o.enable(14),v.transmission&&o.enable(15),v.sheen&&o.enable(16),v.opaque&&o.enable(17),v.pointsUvs&&o.enable(18),v.decodeVideoTexture&&o.enable(19),v.decodeVideoTextureEmissive&&o.enable(20),v.alphaToCoverage&&o.enable(21),x.push(o.mask)}function M(x){const v=g[x.type];let R;if(v){const U=$t[v];R=du.clone(U.uniforms)}else R=x.uniforms;return R}function T(x,v){let R;for(let U=0,C=d.length;U<C;U++){const P=d[U];if(P.cacheKey===v){R=P,++R.usedTimes;break}}return R===void 0&&(R=new Np(n,v,x,a),d.push(R)),R}function b(x){if(--x.usedTimes===0){const v=d.indexOf(x);d[v]=d[d.length-1],d.pop(),x.destroy()}}function w(x){c.remove(x)}function L(){c.dispose()}return{getParameters:p,getProgramCacheKey:u,getUniforms:M,acquireProgram:T,releaseProgram:b,releaseShaderCache:w,programs:d,dispose:L}}function Vp(){let n=new WeakMap;function e(s){return n.has(s)}function t(s){let o=n.get(s);return o===void 0&&(o={},n.set(s,o)),o}function i(s){n.delete(s)}function r(s,o,c){n.get(s)[o]=c}function a(){n=new WeakMap}return{has:e,get:t,remove:i,update:r,dispose:a}}function Hp(n,e){return n.groupOrder!==e.groupOrder?n.groupOrder-e.groupOrder:n.renderOrder!==e.renderOrder?n.renderOrder-e.renderOrder:n.material.id!==e.material.id?n.material.id-e.material.id:n.z!==e.z?n.z-e.z:n.id-e.id}function Qo(n,e){return n.groupOrder!==e.groupOrder?n.groupOrder-e.groupOrder:n.renderOrder!==e.renderOrder?n.renderOrder-e.renderOrder:n.z!==e.z?e.z-n.z:n.id-e.id}function ec(){const n=[];let e=0;const t=[],i=[],r=[];function a(){e=0,t.length=0,i.length=0,r.length=0}function s(h,f,m,g,_,p){let u=n[e];return u===void 0?(u={id:h.id,object:h,geometry:f,material:m,groupOrder:g,renderOrder:h.renderOrder,z:_,group:p},n[e]=u):(u.id=h.id,u.object=h,u.geometry=f,u.material=m,u.groupOrder=g,u.renderOrder=h.renderOrder,u.z=_,u.group=p),e++,u}function o(h,f,m,g,_,p){const u=s(h,f,m,g,_,p);m.transmission>0?i.push(u):m.transparent===!0?r.push(u):t.push(u)}function c(h,f,m,g,_,p){const u=s(h,f,m,g,_,p);m.transmission>0?i.unshift(u):m.transparent===!0?r.unshift(u):t.unshift(u)}function l(h,f){t.length>1&&t.sort(h||Hp),i.length>1&&i.sort(f||Qo),r.length>1&&r.sort(f||Qo)}function d(){for(let h=e,f=n.length;h<f;h++){const m=n[h];if(m.id===null)break;m.id=null,m.object=null,m.geometry=null,m.material=null,m.group=null}}return{opaque:t,transmissive:i,transparent:r,init:a,push:o,unshift:c,finish:d,sort:l}}function Gp(){let n=new WeakMap;function e(i,r){const a=n.get(i);let s;return a===void 0?(s=new ec,n.set(i,[s])):r>=a.length?(s=new ec,a.push(s)):s=a[r],s}function t(){n=new WeakMap}return{get:e,dispose:t}}function jp(){const n={};return{get:function(e){if(n[e.id]!==void 0)return n[e.id];let t;switch(e.type){case"DirectionalLight":t={direction:new k,color:new ce};break;case"SpotLight":t={position:new k,direction:new k,color:new ce,distance:0,coneCos:0,penumbraCos:0,decay:0};break;case"PointLight":t={position:new k,color:new ce,distance:0,decay:0};break;case"HemisphereLight":t={direction:new k,skyColor:new ce,groundColor:new ce};break;case"RectAreaLight":t={color:new ce,position:new k,halfWidth:new k,halfHeight:new k};break}return n[e.id]=t,t}}}function Wp(){const n={};return{get:function(e){if(n[e.id]!==void 0)return n[e.id];let t;switch(e.type){case"DirectionalLight":t={shadowIntensity:1,shadowBias:0,shadowNormalBias:0,shadowRadius:1,shadowMapSize:new Xe};break;case"SpotLight":t={shadowIntensity:1,shadowBias:0,shadowNormalBias:0,shadowRadius:1,shadowMapSize:new Xe};break;case"PointLight":t={shadowIntensity:1,shadowBias:0,shadowNormalBias:0,shadowRadius:1,shadowMapSize:new Xe,shadowCameraNear:1,shadowCameraFar:1e3};break}return n[e.id]=t,t}}}let Xp=0;function qp(n,e){return(e.castShadow?2:0)-(n.castShadow?2:0)+(e.map?1:0)-(n.map?1:0)}function Yp(n){const e=new jp,t=Wp(),i={version:0,hash:{directionalLength:-1,pointLength:-1,spotLength:-1,rectAreaLength:-1,hemiLength:-1,numDirectionalShadows:-1,numPointShadows:-1,numSpotShadows:-1,numSpotMaps:-1,numLightProbes:-1},ambient:[0,0,0],probe:[],directional:[],directionalShadow:[],directionalShadowMap:[],directionalShadowMatrix:[],spot:[],spotLightMap:[],spotShadow:[],spotShadowMap:[],spotLightMatrix:[],rectArea:[],rectAreaLTC1:null,rectAreaLTC2:null,point:[],pointShadow:[],pointShadowMap:[],pointShadowMatrix:[],hemi:[],numSpotLightShadowsWithMaps:0,numLightProbes:0};for(let l=0;l<9;l++)i.probe.push(new k);const r=new k,a=new at,s=new at;function o(l){let d=0,h=0,f=0;for(let x=0;x<9;x++)i.probe[x].set(0,0,0);let m=0,g=0,_=0,p=0,u=0,y=0,S=0,M=0,T=0,b=0,w=0;l.sort(qp);for(let x=0,v=l.length;x<v;x++){const R=l[x],U=R.color,C=R.intensity,P=R.distance,F=R.shadow&&R.shadow.map?R.shadow.map.texture:null;if(R.isAmbientLight)d+=U.r*C,h+=U.g*C,f+=U.b*C;else if(R.isLightProbe){for(let N=0;N<9;N++)i.probe[N].addScaledVector(R.sh.coefficients[N],C);w++}else if(R.isDirectionalLight){const N=e.get(R);if(N.color.copy(R.color).multiplyScalar(R.intensity),R.castShadow){const O=R.shadow,z=t.get(R);z.shadowIntensity=O.intensity,z.shadowBias=O.bias,z.shadowNormalBias=O.normalBias,z.shadowRadius=O.radius,z.shadowMapSize=O.mapSize,i.directionalShadow[m]=z,i.directionalShadowMap[m]=F,i.directionalShadowMatrix[m]=R.shadow.matrix,y++}i.directional[m]=N,m++}else if(R.isSpotLight){const N=e.get(R);N.position.setFromMatrixPosition(R.matrixWorld),N.color.copy(U).multiplyScalar(C),N.distance=P,N.coneCos=Math.cos(R.angle),N.penumbraCos=Math.cos(R.angle*(1-R.penumbra)),N.decay=R.decay,i.spot[_]=N;const O=R.shadow;if(R.map&&(i.spotLightMap[T]=R.map,T++,O.updateMatrices(R),R.castShadow&&b++),i.spotLightMatrix[_]=O.matrix,R.castShadow){const z=t.get(R);z.shadowIntensity=O.intensity,z.shadowBias=O.bias,z.shadowNormalBias=O.normalBias,z.shadowRadius=O.radius,z.shadowMapSize=O.mapSize,i.spotShadow[_]=z,i.spotShadowMap[_]=F,M++}_++}else if(R.isRectAreaLight){const N=e.get(R);N.color.copy(U).multiplyScalar(C),N.halfWidth.set(R.width*.5,0,0),N.halfHeight.set(0,R.height*.5,0),i.rectArea[p]=N,p++}else if(R.isPointLight){const N=e.get(R);if(N.color.copy(R.color).multiplyScalar(R.intensity),N.distance=R.distance,N.decay=R.decay,R.castShadow){const O=R.shadow,z=t.get(R);z.shadowIntensity=O.intensity,z.shadowBias=O.bias,z.shadowNormalBias=O.normalBias,z.shadowRadius=O.radius,z.shadowMapSize=O.mapSize,z.shadowCameraNear=O.camera.near,z.shadowCameraFar=O.camera.far,i.pointShadow[g]=z,i.pointShadowMap[g]=F,i.pointShadowMatrix[g]=R.shadow.matrix,S++}i.point[g]=N,g++}else if(R.isHemisphereLight){const N=e.get(R);N.skyColor.copy(R.color).multiplyScalar(C),N.groundColor.copy(R.groundColor).multiplyScalar(C),i.hemi[u]=N,u++}}p>0&&(n.has("OES_texture_float_linear")===!0?(i.rectAreaLTC1=he.LTC_FLOAT_1,i.rectAreaLTC2=he.LTC_FLOAT_2):(i.rectAreaLTC1=he.LTC_HALF_1,i.rectAreaLTC2=he.LTC_HALF_2)),i.ambient[0]=d,i.ambient[1]=h,i.ambient[2]=f;const L=i.hash;(L.directionalLength!==m||L.pointLength!==g||L.spotLength!==_||L.rectAreaLength!==p||L.hemiLength!==u||L.numDirectionalShadows!==y||L.numPointShadows!==S||L.numSpotShadows!==M||L.numSpotMaps!==T||L.numLightProbes!==w)&&(i.directional.length=m,i.spot.length=_,i.rectArea.length=p,i.point.length=g,i.hemi.length=u,i.directionalShadow.length=y,i.directionalShadowMap.length=y,i.pointShadow.length=S,i.pointShadowMap.length=S,i.spotShadow.length=M,i.spotShadowMap.length=M,i.directionalShadowMatrix.length=y,i.pointShadowMatrix.length=S,i.spotLightMatrix.length=M+T-b,i.spotLightMap.length=T,i.numSpotLightShadowsWithMaps=b,i.numLightProbes=w,L.directionalLength=m,L.pointLength=g,L.spotLength=_,L.rectAreaLength=p,L.hemiLength=u,L.numDirectionalShadows=y,L.numPointShadows=S,L.numSpotShadows=M,L.numSpotMaps=T,L.numLightProbes=w,i.version=Xp++)}function c(l,d){let h=0,f=0,m=0,g=0,_=0;const p=d.matrixWorldInverse;for(let u=0,y=l.length;u<y;u++){const S=l[u];if(S.isDirectionalLight){const M=i.directional[h];M.direction.setFromMatrixPosition(S.matrixWorld),r.setFromMatrixPosition(S.target.matrixWorld),M.direction.sub(r),M.direction.transformDirection(p),h++}else if(S.isSpotLight){const M=i.spot[m];M.position.setFromMatrixPosition(S.matrixWorld),M.position.applyMatrix4(p),M.direction.setFromMatrixPosition(S.matrixWorld),r.setFromMatrixPosition(S.target.matrixWorld),M.direction.sub(r),M.direction.transformDirection(p),m++}else if(S.isRectAreaLight){const M=i.rectArea[g];M.position.setFromMatrixPosition(S.matrixWorld),M.position.applyMatrix4(p),s.identity(),a.copy(S.matrixWorld),a.premultiply(p),s.extractRotation(a),M.halfWidth.set(S.width*.5,0,0),M.halfHeight.set(0,S.height*.5,0),M.halfWidth.applyMatrix4(s),M.halfHeight.applyMatrix4(s),g++}else if(S.isPointLight){const M=i.point[f];M.position.setFromMatrixPosition(S.matrixWorld),M.position.applyMatrix4(p),f++}else if(S.isHemisphereLight){const M=i.hemi[_];M.direction.setFromMatrixPosition(S.matrixWorld),M.direction.transformDirection(p),_++}}}return{setup:o,setupView:c,state:i}}function tc(n){const e=new Yp(n),t=[],i=[];function r(d){l.camera=d,t.length=0,i.length=0}function a(d){t.push(d)}function s(d){i.push(d)}function o(){e.setup(t)}function c(d){e.setupView(t,d)}const l={lightsArray:t,shadowsArray:i,camera:null,lights:e,transmissionRenderTarget:{}};return{init:r,state:l,setupLights:o,setupLightsView:c,pushLight:a,pushShadow:s}}function Kp(n){let e=new WeakMap;function t(r,a=0){const s=e.get(r);let o;return s===void 0?(o=new tc(n),e.set(r,[o])):a>=s.length?(o=new tc(n),s.push(o)):o=s[a],o}function i(){e=new WeakMap}return{get:t,dispose:i}}const $p=`void main() {
	gl_Position = vec4( position, 1.0 );
}`,Zp=`uniform sampler2D shadow_pass;
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
}`;function Jp(n,e,t){let i=new Is;const r=new Xe,a=new Xe,s=new dt,o=new Mu({depthPacking:Il}),c=new Su,l={},d=t.maxTextureSize,h={[Pn]:Dt,[Dt]:Pn,[mt]:mt},f=new Dn({defines:{VSM_SAMPLES:8},uniforms:{shadow_pass:{value:null},resolution:{value:new Xe},radius:{value:4}},vertexShader:$p,fragmentShader:Zp}),m=f.clone();m.defines.HORIZONTAL_PASS=1;const g=new Ye;g.setAttribute("position",new Jt(new Float32Array([-1,-1,.5,3,-1,.5,-1,3,.5]),3));const _=new je(g,f),p=this;this.enabled=!1,this.autoUpdate=!0,this.needsUpdate=!1,this.type=fc;let u=this.type;this.render=function(b,w,L){if(p.enabled===!1||p.autoUpdate===!1&&p.needsUpdate===!1||b.length===0)return;const x=n.getRenderTarget(),v=n.getActiveCubeFace(),R=n.getActiveMipmapLevel(),U=n.state;U.setBlending(Rn),U.buffers.color.setClear(1,1,1,1),U.buffers.depth.setTest(!0),U.setScissorTest(!1);const C=u!==cn&&this.type===cn,P=u===cn&&this.type!==cn;for(let F=0,N=b.length;F<N;F++){const O=b[F],z=O.shadow;if(z===void 0){console.warn("THREE.WebGLShadowMap:",O,"has no shadow.");continue}if(z.autoUpdate===!1&&z.needsUpdate===!1)continue;r.copy(z.mapSize);const G=z.getFrameExtents();if(r.multiply(G),a.copy(z.mapSize),(r.x>d||r.y>d)&&(r.x>d&&(a.x=Math.floor(d/G.x),r.x=a.x*G.x,z.mapSize.x=a.x),r.y>d&&(a.y=Math.floor(d/G.y),r.y=a.y*G.y,z.mapSize.y=a.y)),z.map===null||C===!0||P===!0){const $=this.type!==cn?{minFilter:Kt,magFilter:Kt}:{};z.map!==null&&z.map.dispose(),z.map=new Jn(r.x,r.y,$),z.map.texture.name=O.name+".shadowMap",z.camera.updateProjectionMatrix()}n.setRenderTarget(z.map),n.clear();const K=z.getViewportCount();for(let $=0;$<K;$++){const fe=z.getViewport($);s.set(a.x*fe.x,a.y*fe.y,a.x*fe.z,a.y*fe.w),U.viewport(s),z.updateMatrices(O,$),i=z.getFrustum(),M(w,L,z.camera,O,this.type)}z.isPointLightShadow!==!0&&this.type===cn&&y(z,L),z.needsUpdate=!1}u=this.type,p.needsUpdate=!1,n.setRenderTarget(x,v,R)};function y(b,w){const L=e.update(_);f.defines.VSM_SAMPLES!==b.blurSamples&&(f.defines.VSM_SAMPLES=b.blurSamples,m.defines.VSM_SAMPLES=b.blurSamples,f.needsUpdate=!0,m.needsUpdate=!0),b.mapPass===null&&(b.mapPass=new Jn(r.x,r.y)),f.uniforms.shadow_pass.value=b.map.texture,f.uniforms.resolution.value=b.mapSize,f.uniforms.radius.value=b.radius,n.setRenderTarget(b.mapPass),n.clear(),n.renderBufferDirect(w,null,L,f,_,null),m.uniforms.shadow_pass.value=b.mapPass.texture,m.uniforms.resolution.value=b.mapSize,m.uniforms.radius.value=b.radius,n.setRenderTarget(b.map),n.clear(),n.renderBufferDirect(w,null,L,m,_,null)}function S(b,w,L,x){let v=null;const R=L.isPointLight===!0?b.customDistanceMaterial:b.customDepthMaterial;if(R!==void 0)v=R;else if(v=L.isPointLight===!0?c:o,n.localClippingEnabled&&w.clipShadows===!0&&Array.isArray(w.clippingPlanes)&&w.clippingPlanes.length!==0||w.displacementMap&&w.displacementScale!==0||w.alphaMap&&w.alphaTest>0||w.map&&w.alphaTest>0){const U=v.uuid,C=w.uuid;let P=l[U];P===void 0&&(P={},l[U]=P);let F=P[C];F===void 0&&(F=v.clone(),P[C]=F,w.addEventListener("dispose",T)),v=F}if(v.visible=w.visible,v.wireframe=w.wireframe,x===cn?v.side=w.shadowSide!==null?w.shadowSide:w.side:v.side=w.shadowSide!==null?w.shadowSide:h[w.side],v.alphaMap=w.alphaMap,v.alphaTest=w.alphaTest,v.map=w.map,v.clipShadows=w.clipShadows,v.clippingPlanes=w.clippingPlanes,v.clipIntersection=w.clipIntersection,v.displacementMap=w.displacementMap,v.displacementScale=w.displacementScale,v.displacementBias=w.displacementBias,v.wireframeLinewidth=w.wireframeLinewidth,v.linewidth=w.linewidth,L.isPointLight===!0&&v.isMeshDistanceMaterial===!0){const U=n.properties.get(v);U.light=L}return v}function M(b,w,L,x,v){if(b.visible===!1)return;if(b.layers.test(w.layers)&&(b.isMesh||b.isLine||b.isPoints)&&(b.castShadow||b.receiveShadow&&v===cn)&&(!b.frustumCulled||i.intersectsObject(b))){b.modelViewMatrix.multiplyMatrices(L.matrixWorldInverse,b.matrixWorld);const C=e.update(b),P=b.material;if(Array.isArray(P)){const F=C.groups;for(let N=0,O=F.length;N<O;N++){const z=F[N],G=P[z.materialIndex];if(G&&G.visible){const K=S(b,G,x,v);b.onBeforeShadow(n,b,w,L,C,K,z),n.renderBufferDirect(L,null,C,K,b,z),b.onAfterShadow(n,b,w,L,C,K,z)}}}else if(P.visible){const F=S(b,P,x,v);b.onBeforeShadow(n,b,w,L,C,F,null),n.renderBufferDirect(L,null,C,F,b,null),b.onAfterShadow(n,b,w,L,C,F,null)}}const U=b.children;for(let C=0,P=U.length;C<P;C++)M(U[C],w,L,x,v)}function T(b){b.target.removeEventListener("dispose",T);for(const L in l){const x=l[L],v=b.target.uuid;v in x&&(x[v].dispose(),delete x[v])}}}const Qp={[Ia]:Ua,[za]:ka,[Na]:Oa,[Ei]:Fa,[Ua]:Ia,[ka]:za,[Oa]:Na,[Fa]:Ei};function em(n,e){function t(){let B=!1;const pe=new dt;let Y=null;const te=new dt(0,0,0,0);return{setMask:function(xe){Y!==xe&&!B&&(n.colorMask(xe,xe,xe,xe),Y=xe)},setLocked:function(xe){B=xe},setClear:function(xe,ve,Oe,lt,yt){yt===!0&&(xe*=lt,ve*=lt,Oe*=lt),pe.set(xe,ve,Oe,lt),te.equals(pe)===!1&&(n.clearColor(xe,ve,Oe,lt),te.copy(pe))},reset:function(){B=!1,Y=null,te.set(-1,0,0,0)}}}function i(){let B=!1,pe=!1,Y=null,te=null,xe=null;return{setReversed:function(ve){if(pe!==ve){const Oe=e.get("EXT_clip_control");pe?Oe.clipControlEXT(Oe.LOWER_LEFT_EXT,Oe.ZERO_TO_ONE_EXT):Oe.clipControlEXT(Oe.LOWER_LEFT_EXT,Oe.NEGATIVE_ONE_TO_ONE_EXT);const lt=xe;xe=null,this.setClear(lt)}pe=ve},getReversed:function(){return pe},setTest:function(ve){ve?se(n.DEPTH_TEST):ee(n.DEPTH_TEST)},setMask:function(ve){Y!==ve&&!B&&(n.depthMask(ve),Y=ve)},setFunc:function(ve){if(pe&&(ve=Qp[ve]),te!==ve){switch(ve){case Ia:n.depthFunc(n.NEVER);break;case Ua:n.depthFunc(n.ALWAYS);break;case za:n.depthFunc(n.LESS);break;case Ei:n.depthFunc(n.LEQUAL);break;case Na:n.depthFunc(n.EQUAL);break;case Fa:n.depthFunc(n.GEQUAL);break;case ka:n.depthFunc(n.GREATER);break;case Oa:n.depthFunc(n.NOTEQUAL);break;default:n.depthFunc(n.LEQUAL)}te=ve}},setLocked:function(ve){B=ve},setClear:function(ve){xe!==ve&&(pe&&(ve=1-ve),n.clearDepth(ve),xe=ve)},reset:function(){B=!1,Y=null,te=null,xe=null,pe=!1}}}function r(){let B=!1,pe=null,Y=null,te=null,xe=null,ve=null,Oe=null,lt=null,yt=null;return{setTest:function(tt){B||(tt?se(n.STENCIL_TEST):ee(n.STENCIL_TEST))},setMask:function(tt){pe!==tt&&!B&&(n.stencilMask(tt),pe=tt)},setFunc:function(tt,Ht,Qt){(Y!==tt||te!==Ht||xe!==Qt)&&(n.stencilFunc(tt,Ht,Qt),Y=tt,te=Ht,xe=Qt)},setOp:function(tt,Ht,Qt){(ve!==tt||Oe!==Ht||lt!==Qt)&&(n.stencilOp(tt,Ht,Qt),ve=tt,Oe=Ht,lt=Qt)},setLocked:function(tt){B=tt},setClear:function(tt){yt!==tt&&(n.clearStencil(tt),yt=tt)},reset:function(){B=!1,pe=null,Y=null,te=null,xe=null,ve=null,Oe=null,lt=null,yt=null}}}const a=new t,s=new i,o=new r,c=new WeakMap,l=new WeakMap;let d={},h={},f=new WeakMap,m=[],g=null,_=!1,p=null,u=null,y=null,S=null,M=null,T=null,b=null,w=new ce(0,0,0),L=0,x=!1,v=null,R=null,U=null,C=null,P=null;const F=n.getParameter(n.MAX_COMBINED_TEXTURE_IMAGE_UNITS);let N=!1,O=0;const z=n.getParameter(n.VERSION);z.indexOf("WebGL")!==-1?(O=parseFloat(/^WebGL (\d)/.exec(z)[1]),N=O>=1):z.indexOf("OpenGL ES")!==-1&&(O=parseFloat(/^OpenGL ES (\d)/.exec(z)[1]),N=O>=2);let G=null,K={};const $=n.getParameter(n.SCISSOR_BOX),fe=n.getParameter(n.VIEWPORT),De=new dt().fromArray($),X=new dt().fromArray(fe);function ne(B,pe,Y,te){const xe=new Uint8Array(4),ve=n.createTexture();n.bindTexture(B,ve),n.texParameteri(B,n.TEXTURE_MIN_FILTER,n.NEAREST),n.texParameteri(B,n.TEXTURE_MAG_FILTER,n.NEAREST);for(let Oe=0;Oe<Y;Oe++)B===n.TEXTURE_3D||B===n.TEXTURE_2D_ARRAY?n.texImage3D(pe,0,n.RGBA,1,1,te,0,n.RGBA,n.UNSIGNED_BYTE,xe):n.texImage2D(pe+Oe,0,n.RGBA,1,1,0,n.RGBA,n.UNSIGNED_BYTE,xe);return ve}const ue={};ue[n.TEXTURE_2D]=ne(n.TEXTURE_2D,n.TEXTURE_2D,1),ue[n.TEXTURE_CUBE_MAP]=ne(n.TEXTURE_CUBE_MAP,n.TEXTURE_CUBE_MAP_POSITIVE_X,6),ue[n.TEXTURE_2D_ARRAY]=ne(n.TEXTURE_2D_ARRAY,n.TEXTURE_2D_ARRAY,1,1),ue[n.TEXTURE_3D]=ne(n.TEXTURE_3D,n.TEXTURE_3D,1,1),a.setClear(0,0,0,1),s.setClear(1),o.setClear(0),se(n.DEPTH_TEST),s.setFunc(Ei),Ce(!1),Re(Zs),se(n.CULL_FACE),I(Rn);function se(B){d[B]!==!0&&(n.enable(B),d[B]=!0)}function ee(B){d[B]!==!1&&(n.disable(B),d[B]=!1)}function _e(B,pe){return h[B]!==pe?(n.bindFramebuffer(B,pe),h[B]=pe,B===n.DRAW_FRAMEBUFFER&&(h[n.FRAMEBUFFER]=pe),B===n.FRAMEBUFFER&&(h[n.DRAW_FRAMEBUFFER]=pe),!0):!1}function de(B,pe){let Y=m,te=!1;if(B){Y=f.get(pe),Y===void 0&&(Y=[],f.set(pe,Y));const xe=B.textures;if(Y.length!==xe.length||Y[0]!==n.COLOR_ATTACHMENT0){for(let ve=0,Oe=xe.length;ve<Oe;ve++)Y[ve]=n.COLOR_ATTACHMENT0+ve;Y.length=xe.length,te=!0}}else Y[0]!==n.BACK&&(Y[0]=n.BACK,te=!0);te&&n.drawBuffers(Y)}function Z(B){return g!==B?(n.useProgram(B),g=B,!0):!1}const re={[Wn]:n.FUNC_ADD,[al]:n.FUNC_SUBTRACT,[sl]:n.FUNC_REVERSE_SUBTRACT};re[ol]=n.MIN,re[cl]=n.MAX;const ae={[ll]:n.ZERO,[ul]:n.ONE,[dl]:n.SRC_COLOR,[Da]:n.SRC_ALPHA,[_l]:n.SRC_ALPHA_SATURATE,[ml]:n.DST_COLOR,[fl]:n.DST_ALPHA,[hl]:n.ONE_MINUS_SRC_COLOR,[La]:n.ONE_MINUS_SRC_ALPHA,[gl]:n.ONE_MINUS_DST_COLOR,[pl]:n.ONE_MINUS_DST_ALPHA,[vl]:n.CONSTANT_COLOR,[xl]:n.ONE_MINUS_CONSTANT_COLOR,[Ml]:n.CONSTANT_ALPHA,[Sl]:n.ONE_MINUS_CONSTANT_ALPHA};function I(B,pe,Y,te,xe,ve,Oe,lt,yt,tt){if(B===Rn){_===!0&&(ee(n.BLEND),_=!1);return}if(_===!1&&(se(n.BLEND),_=!0),B!==rl){if(B!==p||tt!==x){if((u!==Wn||M!==Wn)&&(n.blendEquation(n.FUNC_ADD),u=Wn,M=Wn),tt)switch(B){case xi:n.blendFuncSeparate(n.ONE,n.ONE_MINUS_SRC_ALPHA,n.ONE,n.ONE_MINUS_SRC_ALPHA);break;case Js:n.blendFunc(n.ONE,n.ONE);break;case Qs:n.blendFuncSeparate(n.ZERO,n.ONE_MINUS_SRC_COLOR,n.ZERO,n.ONE);break;case eo:n.blendFuncSeparate(n.ZERO,n.SRC_COLOR,n.ZERO,n.SRC_ALPHA);break;default:console.error("THREE.WebGLState: Invalid blending: ",B);break}else switch(B){case xi:n.blendFuncSeparate(n.SRC_ALPHA,n.ONE_MINUS_SRC_ALPHA,n.ONE,n.ONE_MINUS_SRC_ALPHA);break;case Js:n.blendFunc(n.SRC_ALPHA,n.ONE);break;case Qs:n.blendFuncSeparate(n.ZERO,n.ONE_MINUS_SRC_COLOR,n.ZERO,n.ONE);break;case eo:n.blendFunc(n.ZERO,n.SRC_COLOR);break;default:console.error("THREE.WebGLState: Invalid blending: ",B);break}y=null,S=null,T=null,b=null,w.set(0,0,0),L=0,p=B,x=tt}return}xe=xe||pe,ve=ve||Y,Oe=Oe||te,(pe!==u||xe!==M)&&(n.blendEquationSeparate(re[pe],re[xe]),u=pe,M=xe),(Y!==y||te!==S||ve!==T||Oe!==b)&&(n.blendFuncSeparate(ae[Y],ae[te],ae[ve],ae[Oe]),y=Y,S=te,T=ve,b=Oe),(lt.equals(w)===!1||yt!==L)&&(n.blendColor(lt.r,lt.g,lt.b,yt),w.copy(lt),L=yt),p=B,x=!1}function Ie(B,pe){B.side===mt?ee(n.CULL_FACE):se(n.CULL_FACE);let Y=B.side===Dt;pe&&(Y=!Y),Ce(Y),B.blending===xi&&B.transparent===!1?I(Rn):I(B.blending,B.blendEquation,B.blendSrc,B.blendDst,B.blendEquationAlpha,B.blendSrcAlpha,B.blendDstAlpha,B.blendColor,B.blendAlpha,B.premultipliedAlpha),s.setFunc(B.depthFunc),s.setTest(B.depthTest),s.setMask(B.depthWrite),a.setMask(B.colorWrite);const te=B.stencilWrite;o.setTest(te),te&&(o.setMask(B.stencilWriteMask),o.setFunc(B.stencilFunc,B.stencilRef,B.stencilFuncMask),o.setOp(B.stencilFail,B.stencilZFail,B.stencilZPass)),ke(B.polygonOffset,B.polygonOffsetFactor,B.polygonOffsetUnits),B.alphaToCoverage===!0?se(n.SAMPLE_ALPHA_TO_COVERAGE):ee(n.SAMPLE_ALPHA_TO_COVERAGE)}function Ce(B){v!==B&&(B?n.frontFace(n.CW):n.frontFace(n.CCW),v=B)}function Re(B){B!==tl?(se(n.CULL_FACE),B!==R&&(B===Zs?n.cullFace(n.BACK):B===nl?n.cullFace(n.FRONT):n.cullFace(n.FRONT_AND_BACK))):ee(n.CULL_FACE),R=B}function Me(B){B!==U&&(N&&n.lineWidth(B),U=B)}function ke(B,pe,Y){B?(se(n.POLYGON_OFFSET_FILL),(C!==pe||P!==Y)&&(n.polygonOffset(pe,Y),C=pe,P=Y)):ee(n.POLYGON_OFFSET_FILL)}function we(B){B?se(n.SCISSOR_TEST):ee(n.SCISSOR_TEST)}function D(B){B===void 0&&(B=n.TEXTURE0+F-1),G!==B&&(n.activeTexture(B),G=B)}function E(B,pe,Y){Y===void 0&&(G===null?Y=n.TEXTURE0+F-1:Y=G);let te=K[Y];te===void 0&&(te={type:void 0,texture:void 0},K[Y]=te),(te.type!==B||te.texture!==pe)&&(G!==Y&&(n.activeTexture(Y),G=Y),n.bindTexture(B,pe||ue[B]),te.type=B,te.texture=pe)}function j(){const B=K[G];B!==void 0&&B.type!==void 0&&(n.bindTexture(B.type,null),B.type=void 0,B.texture=void 0)}function Q(){try{n.compressedTexImage2D(...arguments)}catch(B){console.error("THREE.WebGLState:",B)}}function ie(){try{n.compressedTexImage3D(...arguments)}catch(B){console.error("THREE.WebGLState:",B)}}function J(){try{n.texSubImage2D(...arguments)}catch(B){console.error("THREE.WebGLState:",B)}}function Ae(){try{n.texSubImage3D(...arguments)}catch(B){console.error("THREE.WebGLState:",B)}}function ge(){try{n.compressedTexSubImage2D(...arguments)}catch(B){console.error("THREE.WebGLState:",B)}}function Ee(){try{n.compressedTexSubImage3D(...arguments)}catch(B){console.error("THREE.WebGLState:",B)}}function Ke(){try{n.texStorage2D(...arguments)}catch(B){console.error("THREE.WebGLState:",B)}}function le(){try{n.texStorage3D(...arguments)}catch(B){console.error("THREE.WebGLState:",B)}}function ye(){try{n.texImage2D(...arguments)}catch(B){console.error("THREE.WebGLState:",B)}}function Ue(){try{n.texImage3D(...arguments)}catch(B){console.error("THREE.WebGLState:",B)}}function ze(B){De.equals(B)===!1&&(n.scissor(B.x,B.y,B.z,B.w),De.copy(B))}function be(B){X.equals(B)===!1&&(n.viewport(B.x,B.y,B.z,B.w),X.copy(B))}function qe(B,pe){let Y=l.get(pe);Y===void 0&&(Y=new WeakMap,l.set(pe,Y));let te=Y.get(B);te===void 0&&(te=n.getUniformBlockIndex(pe,B.name),Y.set(B,te))}function Ve(B,pe){const te=l.get(pe).get(B);c.get(pe)!==te&&(n.uniformBlockBinding(pe,te,B.__bindingPointIndex),c.set(pe,te))}function rt(){n.disable(n.BLEND),n.disable(n.CULL_FACE),n.disable(n.DEPTH_TEST),n.disable(n.POLYGON_OFFSET_FILL),n.disable(n.SCISSOR_TEST),n.disable(n.STENCIL_TEST),n.disable(n.SAMPLE_ALPHA_TO_COVERAGE),n.blendEquation(n.FUNC_ADD),n.blendFunc(n.ONE,n.ZERO),n.blendFuncSeparate(n.ONE,n.ZERO,n.ONE,n.ZERO),n.blendColor(0,0,0,0),n.colorMask(!0,!0,!0,!0),n.clearColor(0,0,0,0),n.depthMask(!0),n.depthFunc(n.LESS),s.setReversed(!1),n.clearDepth(1),n.stencilMask(4294967295),n.stencilFunc(n.ALWAYS,0,4294967295),n.stencilOp(n.KEEP,n.KEEP,n.KEEP),n.clearStencil(0),n.cullFace(n.BACK),n.frontFace(n.CCW),n.polygonOffset(0,0),n.activeTexture(n.TEXTURE0),n.bindFramebuffer(n.FRAMEBUFFER,null),n.bindFramebuffer(n.DRAW_FRAMEBUFFER,null),n.bindFramebuffer(n.READ_FRAMEBUFFER,null),n.useProgram(null),n.lineWidth(1),n.scissor(0,0,n.canvas.width,n.canvas.height),n.viewport(0,0,n.canvas.width,n.canvas.height),d={},G=null,K={},h={},f=new WeakMap,m=[],g=null,_=!1,p=null,u=null,y=null,S=null,M=null,T=null,b=null,w=new ce(0,0,0),L=0,x=!1,v=null,R=null,U=null,C=null,P=null,De.set(0,0,n.canvas.width,n.canvas.height),X.set(0,0,n.canvas.width,n.canvas.height),a.reset(),s.reset(),o.reset()}return{buffers:{color:a,depth:s,stencil:o},enable:se,disable:ee,bindFramebuffer:_e,drawBuffers:de,useProgram:Z,setBlending:I,setMaterial:Ie,setFlipSided:Ce,setCullFace:Re,setLineWidth:Me,setPolygonOffset:ke,setScissorTest:we,activeTexture:D,bindTexture:E,unbindTexture:j,compressedTexImage2D:Q,compressedTexImage3D:ie,texImage2D:ye,texImage3D:Ue,updateUBOMapping:qe,uniformBlockBinding:Ve,texStorage2D:Ke,texStorage3D:le,texSubImage2D:J,texSubImage3D:Ae,compressedTexSubImage2D:ge,compressedTexSubImage3D:Ee,scissor:ze,viewport:be,reset:rt}}function tm(n,e,t,i,r,a,s){const o=e.has("WEBGL_multisampled_render_to_texture")?e.get("WEBGL_multisampled_render_to_texture"):null,c=typeof navigator>"u"?!1:/OculusBrowser/g.test(navigator.userAgent),l=new Xe,d=new WeakMap;let h;const f=new WeakMap;let m=!1;try{m=typeof OffscreenCanvas<"u"&&new OffscreenCanvas(1,1).getContext("2d")!==null}catch{}function g(D,E){return m?new OffscreenCanvas(D,E):Fr("canvas")}function _(D,E,j){let Q=1;const ie=we(D);if((ie.width>j||ie.height>j)&&(Q=j/Math.max(ie.width,ie.height)),Q<1)if(typeof HTMLImageElement<"u"&&D instanceof HTMLImageElement||typeof HTMLCanvasElement<"u"&&D instanceof HTMLCanvasElement||typeof ImageBitmap<"u"&&D instanceof ImageBitmap||typeof VideoFrame<"u"&&D instanceof VideoFrame){const J=Math.floor(Q*ie.width),Ae=Math.floor(Q*ie.height);h===void 0&&(h=g(J,Ae));const ge=E?g(J,Ae):h;return ge.width=J,ge.height=Ae,ge.getContext("2d").drawImage(D,0,0,J,Ae),console.warn("THREE.WebGLRenderer: Texture has been resized from ("+ie.width+"x"+ie.height+") to ("+J+"x"+Ae+")."),ge}else return"data"in D&&console.warn("THREE.WebGLRenderer: Image in DataTexture is too big ("+ie.width+"x"+ie.height+")."),D;return D}function p(D){return D.generateMipmaps}function u(D){n.generateMipmap(D)}function y(D){return D.isWebGLCubeRenderTarget?n.TEXTURE_CUBE_MAP:D.isWebGL3DRenderTarget?n.TEXTURE_3D:D.isWebGLArrayRenderTarget||D.isCompressedArrayTexture?n.TEXTURE_2D_ARRAY:n.TEXTURE_2D}function S(D,E,j,Q,ie=!1){if(D!==null){if(n[D]!==void 0)return n[D];console.warn("THREE.WebGLRenderer: Attempt to use non-existing WebGL internal format '"+D+"'")}let J=E;if(E===n.RED&&(j===n.FLOAT&&(J=n.R32F),j===n.HALF_FLOAT&&(J=n.R16F),j===n.UNSIGNED_BYTE&&(J=n.R8)),E===n.RED_INTEGER&&(j===n.UNSIGNED_BYTE&&(J=n.R8UI),j===n.UNSIGNED_SHORT&&(J=n.R16UI),j===n.UNSIGNED_INT&&(J=n.R32UI),j===n.BYTE&&(J=n.R8I),j===n.SHORT&&(J=n.R16I),j===n.INT&&(J=n.R32I)),E===n.RG&&(j===n.FLOAT&&(J=n.RG32F),j===n.HALF_FLOAT&&(J=n.RG16F),j===n.UNSIGNED_BYTE&&(J=n.RG8)),E===n.RG_INTEGER&&(j===n.UNSIGNED_BYTE&&(J=n.RG8UI),j===n.UNSIGNED_SHORT&&(J=n.RG16UI),j===n.UNSIGNED_INT&&(J=n.RG32UI),j===n.BYTE&&(J=n.RG8I),j===n.SHORT&&(J=n.RG16I),j===n.INT&&(J=n.RG32I)),E===n.RGB_INTEGER&&(j===n.UNSIGNED_BYTE&&(J=n.RGB8UI),j===n.UNSIGNED_SHORT&&(J=n.RGB16UI),j===n.UNSIGNED_INT&&(J=n.RGB32UI),j===n.BYTE&&(J=n.RGB8I),j===n.SHORT&&(J=n.RGB16I),j===n.INT&&(J=n.RGB32I)),E===n.RGBA_INTEGER&&(j===n.UNSIGNED_BYTE&&(J=n.RGBA8UI),j===n.UNSIGNED_SHORT&&(J=n.RGBA16UI),j===n.UNSIGNED_INT&&(J=n.RGBA32UI),j===n.BYTE&&(J=n.RGBA8I),j===n.SHORT&&(J=n.RGBA16I),j===n.INT&&(J=n.RGBA32I)),E===n.RGB&&j===n.UNSIGNED_INT_5_9_9_9_REV&&(J=n.RGB9_E5),E===n.RGBA){const Ae=ie?zr:Je.getTransfer(Q);j===n.FLOAT&&(J=n.RGBA32F),j===n.HALF_FLOAT&&(J=n.RGBA16F),j===n.UNSIGNED_BYTE&&(J=Ae===it?n.SRGB8_ALPHA8:n.RGBA8),j===n.UNSIGNED_SHORT_4_4_4_4&&(J=n.RGBA4),j===n.UNSIGNED_SHORT_5_5_5_1&&(J=n.RGB5_A1)}return(J===n.R16F||J===n.R32F||J===n.RG16F||J===n.RG32F||J===n.RGBA16F||J===n.RGBA32F)&&e.get("EXT_color_buffer_float"),J}function M(D,E){let j;return D?E===null||E===Zn||E===Ti?j=n.DEPTH24_STENCIL8:E===un?j=n.DEPTH32F_STENCIL8:E===ji&&(j=n.DEPTH24_STENCIL8,console.warn("DepthTexture: 16 bit depth attachment is not supported with stencil. Using 24-bit attachment.")):E===null||E===Zn||E===Ti?j=n.DEPTH_COMPONENT24:E===un?j=n.DEPTH_COMPONENT32F:E===ji&&(j=n.DEPTH_COMPONENT16),j}function T(D,E){return p(D)===!0||D.isFramebufferTexture&&D.minFilter!==Kt&&D.minFilter!==Zt?Math.log2(Math.max(E.width,E.height))+1:D.mipmaps!==void 0&&D.mipmaps.length>0?D.mipmaps.length:D.isCompressedTexture&&Array.isArray(D.image)?E.mipmaps.length:1}function b(D){const E=D.target;E.removeEventListener("dispose",b),L(E),E.isVideoTexture&&d.delete(E)}function w(D){const E=D.target;E.removeEventListener("dispose",w),v(E)}function L(D){const E=i.get(D);if(E.__webglInit===void 0)return;const j=D.source,Q=f.get(j);if(Q){const ie=Q[E.__cacheKey];ie.usedTimes--,ie.usedTimes===0&&x(D),Object.keys(Q).length===0&&f.delete(j)}i.remove(D)}function x(D){const E=i.get(D);n.deleteTexture(E.__webglTexture);const j=D.source,Q=f.get(j);delete Q[E.__cacheKey],s.memory.textures--}function v(D){const E=i.get(D);if(D.depthTexture&&(D.depthTexture.dispose(),i.remove(D.depthTexture)),D.isWebGLCubeRenderTarget)for(let Q=0;Q<6;Q++){if(Array.isArray(E.__webglFramebuffer[Q]))for(let ie=0;ie<E.__webglFramebuffer[Q].length;ie++)n.deleteFramebuffer(E.__webglFramebuffer[Q][ie]);else n.deleteFramebuffer(E.__webglFramebuffer[Q]);E.__webglDepthbuffer&&n.deleteRenderbuffer(E.__webglDepthbuffer[Q])}else{if(Array.isArray(E.__webglFramebuffer))for(let Q=0;Q<E.__webglFramebuffer.length;Q++)n.deleteFramebuffer(E.__webglFramebuffer[Q]);else n.deleteFramebuffer(E.__webglFramebuffer);if(E.__webglDepthbuffer&&n.deleteRenderbuffer(E.__webglDepthbuffer),E.__webglMultisampledFramebuffer&&n.deleteFramebuffer(E.__webglMultisampledFramebuffer),E.__webglColorRenderbuffer)for(let Q=0;Q<E.__webglColorRenderbuffer.length;Q++)E.__webglColorRenderbuffer[Q]&&n.deleteRenderbuffer(E.__webglColorRenderbuffer[Q]);E.__webglDepthRenderbuffer&&n.deleteRenderbuffer(E.__webglDepthRenderbuffer)}const j=D.textures;for(let Q=0,ie=j.length;Q<ie;Q++){const J=i.get(j[Q]);J.__webglTexture&&(n.deleteTexture(J.__webglTexture),s.memory.textures--),i.remove(j[Q])}i.remove(D)}let R=0;function U(){R=0}function C(){const D=R;return D>=r.maxTextures&&console.warn("THREE.WebGLTextures: Trying to use "+D+" texture units while this GPU supports only "+r.maxTextures),R+=1,D}function P(D){const E=[];return E.push(D.wrapS),E.push(D.wrapT),E.push(D.wrapR||0),E.push(D.magFilter),E.push(D.minFilter),E.push(D.anisotropy),E.push(D.internalFormat),E.push(D.format),E.push(D.type),E.push(D.generateMipmaps),E.push(D.premultiplyAlpha),E.push(D.flipY),E.push(D.unpackAlignment),E.push(D.colorSpace),E.join()}function F(D,E){const j=i.get(D);if(D.isVideoTexture&&Me(D),D.isRenderTargetTexture===!1&&D.version>0&&j.__version!==D.version){const Q=D.image;if(Q===null)console.warn("THREE.WebGLRenderer: Texture marked for update but no image data found.");else if(Q.complete===!1)console.warn("THREE.WebGLRenderer: Texture marked for update but image is incomplete");else{X(j,D,E);return}}t.bindTexture(n.TEXTURE_2D,j.__webglTexture,n.TEXTURE0+E)}function N(D,E){const j=i.get(D);if(D.version>0&&j.__version!==D.version){X(j,D,E);return}t.bindTexture(n.TEXTURE_2D_ARRAY,j.__webglTexture,n.TEXTURE0+E)}function O(D,E){const j=i.get(D);if(D.version>0&&j.__version!==D.version){X(j,D,E);return}t.bindTexture(n.TEXTURE_3D,j.__webglTexture,n.TEXTURE0+E)}function z(D,E){const j=i.get(D);if(D.version>0&&j.__version!==D.version){ne(j,D,E);return}t.bindTexture(n.TEXTURE_CUBE_MAP,j.__webglTexture,n.TEXTURE0+E)}const G={[Ha]:n.REPEAT,[qn]:n.CLAMP_TO_EDGE,[Ga]:n.MIRRORED_REPEAT},K={[Kt]:n.NEAREST,[Dl]:n.NEAREST_MIPMAP_NEAREST,[er]:n.NEAREST_MIPMAP_LINEAR,[Zt]:n.LINEAR,[qr]:n.LINEAR_MIPMAP_NEAREST,[Yn]:n.LINEAR_MIPMAP_LINEAR},$={[zl]:n.NEVER,[Vl]:n.ALWAYS,[Nl]:n.LESS,[wc]:n.LEQUAL,[Fl]:n.EQUAL,[Bl]:n.GEQUAL,[kl]:n.GREATER,[Ol]:n.NOTEQUAL};function fe(D,E){if(E.type===un&&e.has("OES_texture_float_linear")===!1&&(E.magFilter===Zt||E.magFilter===qr||E.magFilter===er||E.magFilter===Yn||E.minFilter===Zt||E.minFilter===qr||E.minFilter===er||E.minFilter===Yn)&&console.warn("THREE.WebGLRenderer: Unable to use linear filtering with floating point textures. OES_texture_float_linear not supported on this device."),n.texParameteri(D,n.TEXTURE_WRAP_S,G[E.wrapS]),n.texParameteri(D,n.TEXTURE_WRAP_T,G[E.wrapT]),(D===n.TEXTURE_3D||D===n.TEXTURE_2D_ARRAY)&&n.texParameteri(D,n.TEXTURE_WRAP_R,G[E.wrapR]),n.texParameteri(D,n.TEXTURE_MAG_FILTER,K[E.magFilter]),n.texParameteri(D,n.TEXTURE_MIN_FILTER,K[E.minFilter]),E.compareFunction&&(n.texParameteri(D,n.TEXTURE_COMPARE_MODE,n.COMPARE_REF_TO_TEXTURE),n.texParameteri(D,n.TEXTURE_COMPARE_FUNC,$[E.compareFunction])),e.has("EXT_texture_filter_anisotropic")===!0){if(E.magFilter===Kt||E.minFilter!==er&&E.minFilter!==Yn||E.type===un&&e.has("OES_texture_float_linear")===!1)return;if(E.anisotropy>1||i.get(E).__currentAnisotropy){const j=e.get("EXT_texture_filter_anisotropic");n.texParameterf(D,j.TEXTURE_MAX_ANISOTROPY_EXT,Math.min(E.anisotropy,r.getMaxAnisotropy())),i.get(E).__currentAnisotropy=E.anisotropy}}}function De(D,E){let j=!1;D.__webglInit===void 0&&(D.__webglInit=!0,E.addEventListener("dispose",b));const Q=E.source;let ie=f.get(Q);ie===void 0&&(ie={},f.set(Q,ie));const J=P(E);if(J!==D.__cacheKey){ie[J]===void 0&&(ie[J]={texture:n.createTexture(),usedTimes:0},s.memory.textures++,j=!0),ie[J].usedTimes++;const Ae=ie[D.__cacheKey];Ae!==void 0&&(ie[D.__cacheKey].usedTimes--,Ae.usedTimes===0&&x(E)),D.__cacheKey=J,D.__webglTexture=ie[J].texture}return j}function X(D,E,j){let Q=n.TEXTURE_2D;(E.isDataArrayTexture||E.isCompressedArrayTexture)&&(Q=n.TEXTURE_2D_ARRAY),E.isData3DTexture&&(Q=n.TEXTURE_3D);const ie=De(D,E),J=E.source;t.bindTexture(Q,D.__webglTexture,n.TEXTURE0+j);const Ae=i.get(J);if(J.version!==Ae.__version||ie===!0){t.activeTexture(n.TEXTURE0+j);const ge=Je.getPrimaries(Je.workingColorSpace),Ee=E.colorSpace===An?null:Je.getPrimaries(E.colorSpace),Ke=E.colorSpace===An||ge===Ee?n.NONE:n.BROWSER_DEFAULT_WEBGL;n.pixelStorei(n.UNPACK_FLIP_Y_WEBGL,E.flipY),n.pixelStorei(n.UNPACK_PREMULTIPLY_ALPHA_WEBGL,E.premultiplyAlpha),n.pixelStorei(n.UNPACK_ALIGNMENT,E.unpackAlignment),n.pixelStorei(n.UNPACK_COLORSPACE_CONVERSION_WEBGL,Ke);let le=_(E.image,!1,r.maxTextureSize);le=ke(E,le);const ye=a.convert(E.format,E.colorSpace),Ue=a.convert(E.type);let ze=S(E.internalFormat,ye,Ue,E.colorSpace,E.isVideoTexture);fe(Q,E);let be;const qe=E.mipmaps,Ve=E.isVideoTexture!==!0,rt=Ae.__version===void 0||ie===!0,B=J.dataReady,pe=T(E,le);if(E.isDepthTexture)ze=M(E.format===Ai,E.type),rt&&(Ve?t.texStorage2D(n.TEXTURE_2D,1,ze,le.width,le.height):t.texImage2D(n.TEXTURE_2D,0,ze,le.width,le.height,0,ye,Ue,null));else if(E.isDataTexture)if(qe.length>0){Ve&&rt&&t.texStorage2D(n.TEXTURE_2D,pe,ze,qe[0].width,qe[0].height);for(let Y=0,te=qe.length;Y<te;Y++)be=qe[Y],Ve?B&&t.texSubImage2D(n.TEXTURE_2D,Y,0,0,be.width,be.height,ye,Ue,be.data):t.texImage2D(n.TEXTURE_2D,Y,ze,be.width,be.height,0,ye,Ue,be.data);E.generateMipmaps=!1}else Ve?(rt&&t.texStorage2D(n.TEXTURE_2D,pe,ze,le.width,le.height),B&&t.texSubImage2D(n.TEXTURE_2D,0,0,0,le.width,le.height,ye,Ue,le.data)):t.texImage2D(n.TEXTURE_2D,0,ze,le.width,le.height,0,ye,Ue,le.data);else if(E.isCompressedTexture)if(E.isCompressedArrayTexture){Ve&&rt&&t.texStorage3D(n.TEXTURE_2D_ARRAY,pe,ze,qe[0].width,qe[0].height,le.depth);for(let Y=0,te=qe.length;Y<te;Y++)if(be=qe[Y],E.format!==Yt)if(ye!==null)if(Ve){if(B)if(E.layerUpdates.size>0){const xe=Do(be.width,be.height,E.format,E.type);for(const ve of E.layerUpdates){const Oe=be.data.subarray(ve*xe/be.data.BYTES_PER_ELEMENT,(ve+1)*xe/be.data.BYTES_PER_ELEMENT);t.compressedTexSubImage3D(n.TEXTURE_2D_ARRAY,Y,0,0,ve,be.width,be.height,1,ye,Oe)}E.clearLayerUpdates()}else t.compressedTexSubImage3D(n.TEXTURE_2D_ARRAY,Y,0,0,0,be.width,be.height,le.depth,ye,be.data)}else t.compressedTexImage3D(n.TEXTURE_2D_ARRAY,Y,ze,be.width,be.height,le.depth,0,be.data,0,0);else console.warn("THREE.WebGLRenderer: Attempt to load unsupported compressed texture format in .uploadTexture()");else Ve?B&&t.texSubImage3D(n.TEXTURE_2D_ARRAY,Y,0,0,0,be.width,be.height,le.depth,ye,Ue,be.data):t.texImage3D(n.TEXTURE_2D_ARRAY,Y,ze,be.width,be.height,le.depth,0,ye,Ue,be.data)}else{Ve&&rt&&t.texStorage2D(n.TEXTURE_2D,pe,ze,qe[0].width,qe[0].height);for(let Y=0,te=qe.length;Y<te;Y++)be=qe[Y],E.format!==Yt?ye!==null?Ve?B&&t.compressedTexSubImage2D(n.TEXTURE_2D,Y,0,0,be.width,be.height,ye,be.data):t.compressedTexImage2D(n.TEXTURE_2D,Y,ze,be.width,be.height,0,be.data):console.warn("THREE.WebGLRenderer: Attempt to load unsupported compressed texture format in .uploadTexture()"):Ve?B&&t.texSubImage2D(n.TEXTURE_2D,Y,0,0,be.width,be.height,ye,Ue,be.data):t.texImage2D(n.TEXTURE_2D,Y,ze,be.width,be.height,0,ye,Ue,be.data)}else if(E.isDataArrayTexture)if(Ve){if(rt&&t.texStorage3D(n.TEXTURE_2D_ARRAY,pe,ze,le.width,le.height,le.depth),B)if(E.layerUpdates.size>0){const Y=Do(le.width,le.height,E.format,E.type);for(const te of E.layerUpdates){const xe=le.data.subarray(te*Y/le.data.BYTES_PER_ELEMENT,(te+1)*Y/le.data.BYTES_PER_ELEMENT);t.texSubImage3D(n.TEXTURE_2D_ARRAY,0,0,0,te,le.width,le.height,1,ye,Ue,xe)}E.clearLayerUpdates()}else t.texSubImage3D(n.TEXTURE_2D_ARRAY,0,0,0,0,le.width,le.height,le.depth,ye,Ue,le.data)}else t.texImage3D(n.TEXTURE_2D_ARRAY,0,ze,le.width,le.height,le.depth,0,ye,Ue,le.data);else if(E.isData3DTexture)Ve?(rt&&t.texStorage3D(n.TEXTURE_3D,pe,ze,le.width,le.height,le.depth),B&&t.texSubImage3D(n.TEXTURE_3D,0,0,0,0,le.width,le.height,le.depth,ye,Ue,le.data)):t.texImage3D(n.TEXTURE_3D,0,ze,le.width,le.height,le.depth,0,ye,Ue,le.data);else if(E.isFramebufferTexture){if(rt)if(Ve)t.texStorage2D(n.TEXTURE_2D,pe,ze,le.width,le.height);else{let Y=le.width,te=le.height;for(let xe=0;xe<pe;xe++)t.texImage2D(n.TEXTURE_2D,xe,ze,Y,te,0,ye,Ue,null),Y>>=1,te>>=1}}else if(qe.length>0){if(Ve&&rt){const Y=we(qe[0]);t.texStorage2D(n.TEXTURE_2D,pe,ze,Y.width,Y.height)}for(let Y=0,te=qe.length;Y<te;Y++)be=qe[Y],Ve?B&&t.texSubImage2D(n.TEXTURE_2D,Y,0,0,ye,Ue,be):t.texImage2D(n.TEXTURE_2D,Y,ze,ye,Ue,be);E.generateMipmaps=!1}else if(Ve){if(rt){const Y=we(le);t.texStorage2D(n.TEXTURE_2D,pe,ze,Y.width,Y.height)}B&&t.texSubImage2D(n.TEXTURE_2D,0,0,0,ye,Ue,le)}else t.texImage2D(n.TEXTURE_2D,0,ze,ye,Ue,le);p(E)&&u(Q),Ae.__version=J.version,E.onUpdate&&E.onUpdate(E)}D.__version=E.version}function ne(D,E,j){if(E.image.length!==6)return;const Q=De(D,E),ie=E.source;t.bindTexture(n.TEXTURE_CUBE_MAP,D.__webglTexture,n.TEXTURE0+j);const J=i.get(ie);if(ie.version!==J.__version||Q===!0){t.activeTexture(n.TEXTURE0+j);const Ae=Je.getPrimaries(Je.workingColorSpace),ge=E.colorSpace===An?null:Je.getPrimaries(E.colorSpace),Ee=E.colorSpace===An||Ae===ge?n.NONE:n.BROWSER_DEFAULT_WEBGL;n.pixelStorei(n.UNPACK_FLIP_Y_WEBGL,E.flipY),n.pixelStorei(n.UNPACK_PREMULTIPLY_ALPHA_WEBGL,E.premultiplyAlpha),n.pixelStorei(n.UNPACK_ALIGNMENT,E.unpackAlignment),n.pixelStorei(n.UNPACK_COLORSPACE_CONVERSION_WEBGL,Ee);const Ke=E.isCompressedTexture||E.image[0].isCompressedTexture,le=E.image[0]&&E.image[0].isDataTexture,ye=[];for(let te=0;te<6;te++)!Ke&&!le?ye[te]=_(E.image[te],!0,r.maxCubemapSize):ye[te]=le?E.image[te].image:E.image[te],ye[te]=ke(E,ye[te]);const Ue=ye[0],ze=a.convert(E.format,E.colorSpace),be=a.convert(E.type),qe=S(E.internalFormat,ze,be,E.colorSpace),Ve=E.isVideoTexture!==!0,rt=J.__version===void 0||Q===!0,B=ie.dataReady;let pe=T(E,Ue);fe(n.TEXTURE_CUBE_MAP,E);let Y;if(Ke){Ve&&rt&&t.texStorage2D(n.TEXTURE_CUBE_MAP,pe,qe,Ue.width,Ue.height);for(let te=0;te<6;te++){Y=ye[te].mipmaps;for(let xe=0;xe<Y.length;xe++){const ve=Y[xe];E.format!==Yt?ze!==null?Ve?B&&t.compressedTexSubImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+te,xe,0,0,ve.width,ve.height,ze,ve.data):t.compressedTexImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+te,xe,qe,ve.width,ve.height,0,ve.data):console.warn("THREE.WebGLRenderer: Attempt to load unsupported compressed texture format in .setTextureCube()"):Ve?B&&t.texSubImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+te,xe,0,0,ve.width,ve.height,ze,be,ve.data):t.texImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+te,xe,qe,ve.width,ve.height,0,ze,be,ve.data)}}}else{if(Y=E.mipmaps,Ve&&rt){Y.length>0&&pe++;const te=we(ye[0]);t.texStorage2D(n.TEXTURE_CUBE_MAP,pe,qe,te.width,te.height)}for(let te=0;te<6;te++)if(le){Ve?B&&t.texSubImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+te,0,0,0,ye[te].width,ye[te].height,ze,be,ye[te].data):t.texImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+te,0,qe,ye[te].width,ye[te].height,0,ze,be,ye[te].data);for(let xe=0;xe<Y.length;xe++){const Oe=Y[xe].image[te].image;Ve?B&&t.texSubImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+te,xe+1,0,0,Oe.width,Oe.height,ze,be,Oe.data):t.texImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+te,xe+1,qe,Oe.width,Oe.height,0,ze,be,Oe.data)}}else{Ve?B&&t.texSubImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+te,0,0,0,ze,be,ye[te]):t.texImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+te,0,qe,ze,be,ye[te]);for(let xe=0;xe<Y.length;xe++){const ve=Y[xe];Ve?B&&t.texSubImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+te,xe+1,0,0,ze,be,ve.image[te]):t.texImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+te,xe+1,qe,ze,be,ve.image[te])}}}p(E)&&u(n.TEXTURE_CUBE_MAP),J.__version=ie.version,E.onUpdate&&E.onUpdate(E)}D.__version=E.version}function ue(D,E,j,Q,ie,J){const Ae=a.convert(j.format,j.colorSpace),ge=a.convert(j.type),Ee=S(j.internalFormat,Ae,ge,j.colorSpace),Ke=i.get(E),le=i.get(j);if(le.__renderTarget=E,!Ke.__hasExternalTextures){const ye=Math.max(1,E.width>>J),Ue=Math.max(1,E.height>>J);ie===n.TEXTURE_3D||ie===n.TEXTURE_2D_ARRAY?t.texImage3D(ie,J,Ee,ye,Ue,E.depth,0,Ae,ge,null):t.texImage2D(ie,J,Ee,ye,Ue,0,Ae,ge,null)}t.bindFramebuffer(n.FRAMEBUFFER,D),Re(E)?o.framebufferTexture2DMultisampleEXT(n.FRAMEBUFFER,Q,ie,le.__webglTexture,0,Ce(E)):(ie===n.TEXTURE_2D||ie>=n.TEXTURE_CUBE_MAP_POSITIVE_X&&ie<=n.TEXTURE_CUBE_MAP_NEGATIVE_Z)&&n.framebufferTexture2D(n.FRAMEBUFFER,Q,ie,le.__webglTexture,J),t.bindFramebuffer(n.FRAMEBUFFER,null)}function se(D,E,j){if(n.bindRenderbuffer(n.RENDERBUFFER,D),E.depthBuffer){const Q=E.depthTexture,ie=Q&&Q.isDepthTexture?Q.type:null,J=M(E.stencilBuffer,ie),Ae=E.stencilBuffer?n.DEPTH_STENCIL_ATTACHMENT:n.DEPTH_ATTACHMENT,ge=Ce(E);Re(E)?o.renderbufferStorageMultisampleEXT(n.RENDERBUFFER,ge,J,E.width,E.height):j?n.renderbufferStorageMultisample(n.RENDERBUFFER,ge,J,E.width,E.height):n.renderbufferStorage(n.RENDERBUFFER,J,E.width,E.height),n.framebufferRenderbuffer(n.FRAMEBUFFER,Ae,n.RENDERBUFFER,D)}else{const Q=E.textures;for(let ie=0;ie<Q.length;ie++){const J=Q[ie],Ae=a.convert(J.format,J.colorSpace),ge=a.convert(J.type),Ee=S(J.internalFormat,Ae,ge,J.colorSpace),Ke=Ce(E);j&&Re(E)===!1?n.renderbufferStorageMultisample(n.RENDERBUFFER,Ke,Ee,E.width,E.height):Re(E)?o.renderbufferStorageMultisampleEXT(n.RENDERBUFFER,Ke,Ee,E.width,E.height):n.renderbufferStorage(n.RENDERBUFFER,Ee,E.width,E.height)}}n.bindRenderbuffer(n.RENDERBUFFER,null)}function ee(D,E){if(E&&E.isWebGLCubeRenderTarget)throw new Error("Depth Texture with cube render targets is not supported");if(t.bindFramebuffer(n.FRAMEBUFFER,D),!(E.depthTexture&&E.depthTexture.isDepthTexture))throw new Error("renderTarget.depthTexture must be an instance of THREE.DepthTexture");const Q=i.get(E.depthTexture);Q.__renderTarget=E,(!Q.__webglTexture||E.depthTexture.image.width!==E.width||E.depthTexture.image.height!==E.height)&&(E.depthTexture.image.width=E.width,E.depthTexture.image.height=E.height,E.depthTexture.needsUpdate=!0),F(E.depthTexture,0);const ie=Q.__webglTexture,J=Ce(E);if(E.depthTexture.format===Mi)Re(E)?o.framebufferTexture2DMultisampleEXT(n.FRAMEBUFFER,n.DEPTH_ATTACHMENT,n.TEXTURE_2D,ie,0,J):n.framebufferTexture2D(n.FRAMEBUFFER,n.DEPTH_ATTACHMENT,n.TEXTURE_2D,ie,0);else if(E.depthTexture.format===Ai)Re(E)?o.framebufferTexture2DMultisampleEXT(n.FRAMEBUFFER,n.DEPTH_STENCIL_ATTACHMENT,n.TEXTURE_2D,ie,0,J):n.framebufferTexture2D(n.FRAMEBUFFER,n.DEPTH_STENCIL_ATTACHMENT,n.TEXTURE_2D,ie,0);else throw new Error("Unknown depthTexture format")}function _e(D){const E=i.get(D),j=D.isWebGLCubeRenderTarget===!0;if(E.__boundDepthTexture!==D.depthTexture){const Q=D.depthTexture;if(E.__depthDisposeCallback&&E.__depthDisposeCallback(),Q){const ie=()=>{delete E.__boundDepthTexture,delete E.__depthDisposeCallback,Q.removeEventListener("dispose",ie)};Q.addEventListener("dispose",ie),E.__depthDisposeCallback=ie}E.__boundDepthTexture=Q}if(D.depthTexture&&!E.__autoAllocateDepthBuffer){if(j)throw new Error("target.depthTexture not supported in Cube render targets");ee(E.__webglFramebuffer,D)}else if(j){E.__webglDepthbuffer=[];for(let Q=0;Q<6;Q++)if(t.bindFramebuffer(n.FRAMEBUFFER,E.__webglFramebuffer[Q]),E.__webglDepthbuffer[Q]===void 0)E.__webglDepthbuffer[Q]=n.createRenderbuffer(),se(E.__webglDepthbuffer[Q],D,!1);else{const ie=D.stencilBuffer?n.DEPTH_STENCIL_ATTACHMENT:n.DEPTH_ATTACHMENT,J=E.__webglDepthbuffer[Q];n.bindRenderbuffer(n.RENDERBUFFER,J),n.framebufferRenderbuffer(n.FRAMEBUFFER,ie,n.RENDERBUFFER,J)}}else if(t.bindFramebuffer(n.FRAMEBUFFER,E.__webglFramebuffer),E.__webglDepthbuffer===void 0)E.__webglDepthbuffer=n.createRenderbuffer(),se(E.__webglDepthbuffer,D,!1);else{const Q=D.stencilBuffer?n.DEPTH_STENCIL_ATTACHMENT:n.DEPTH_ATTACHMENT,ie=E.__webglDepthbuffer;n.bindRenderbuffer(n.RENDERBUFFER,ie),n.framebufferRenderbuffer(n.FRAMEBUFFER,Q,n.RENDERBUFFER,ie)}t.bindFramebuffer(n.FRAMEBUFFER,null)}function de(D,E,j){const Q=i.get(D);E!==void 0&&ue(Q.__webglFramebuffer,D,D.texture,n.COLOR_ATTACHMENT0,n.TEXTURE_2D,0),j!==void 0&&_e(D)}function Z(D){const E=D.texture,j=i.get(D),Q=i.get(E);D.addEventListener("dispose",w);const ie=D.textures,J=D.isWebGLCubeRenderTarget===!0,Ae=ie.length>1;if(Ae||(Q.__webglTexture===void 0&&(Q.__webglTexture=n.createTexture()),Q.__version=E.version,s.memory.textures++),J){j.__webglFramebuffer=[];for(let ge=0;ge<6;ge++)if(E.mipmaps&&E.mipmaps.length>0){j.__webglFramebuffer[ge]=[];for(let Ee=0;Ee<E.mipmaps.length;Ee++)j.__webglFramebuffer[ge][Ee]=n.createFramebuffer()}else j.__webglFramebuffer[ge]=n.createFramebuffer()}else{if(E.mipmaps&&E.mipmaps.length>0){j.__webglFramebuffer=[];for(let ge=0;ge<E.mipmaps.length;ge++)j.__webglFramebuffer[ge]=n.createFramebuffer()}else j.__webglFramebuffer=n.createFramebuffer();if(Ae)for(let ge=0,Ee=ie.length;ge<Ee;ge++){const Ke=i.get(ie[ge]);Ke.__webglTexture===void 0&&(Ke.__webglTexture=n.createTexture(),s.memory.textures++)}if(D.samples>0&&Re(D)===!1){j.__webglMultisampledFramebuffer=n.createFramebuffer(),j.__webglColorRenderbuffer=[],t.bindFramebuffer(n.FRAMEBUFFER,j.__webglMultisampledFramebuffer);for(let ge=0;ge<ie.length;ge++){const Ee=ie[ge];j.__webglColorRenderbuffer[ge]=n.createRenderbuffer(),n.bindRenderbuffer(n.RENDERBUFFER,j.__webglColorRenderbuffer[ge]);const Ke=a.convert(Ee.format,Ee.colorSpace),le=a.convert(Ee.type),ye=S(Ee.internalFormat,Ke,le,Ee.colorSpace,D.isXRRenderTarget===!0),Ue=Ce(D);n.renderbufferStorageMultisample(n.RENDERBUFFER,Ue,ye,D.width,D.height),n.framebufferRenderbuffer(n.FRAMEBUFFER,n.COLOR_ATTACHMENT0+ge,n.RENDERBUFFER,j.__webglColorRenderbuffer[ge])}n.bindRenderbuffer(n.RENDERBUFFER,null),D.depthBuffer&&(j.__webglDepthRenderbuffer=n.createRenderbuffer(),se(j.__webglDepthRenderbuffer,D,!0)),t.bindFramebuffer(n.FRAMEBUFFER,null)}}if(J){t.bindTexture(n.TEXTURE_CUBE_MAP,Q.__webglTexture),fe(n.TEXTURE_CUBE_MAP,E);for(let ge=0;ge<6;ge++)if(E.mipmaps&&E.mipmaps.length>0)for(let Ee=0;Ee<E.mipmaps.length;Ee++)ue(j.__webglFramebuffer[ge][Ee],D,E,n.COLOR_ATTACHMENT0,n.TEXTURE_CUBE_MAP_POSITIVE_X+ge,Ee);else ue(j.__webglFramebuffer[ge],D,E,n.COLOR_ATTACHMENT0,n.TEXTURE_CUBE_MAP_POSITIVE_X+ge,0);p(E)&&u(n.TEXTURE_CUBE_MAP),t.unbindTexture()}else if(Ae){for(let ge=0,Ee=ie.length;ge<Ee;ge++){const Ke=ie[ge],le=i.get(Ke);t.bindTexture(n.TEXTURE_2D,le.__webglTexture),fe(n.TEXTURE_2D,Ke),ue(j.__webglFramebuffer,D,Ke,n.COLOR_ATTACHMENT0+ge,n.TEXTURE_2D,0),p(Ke)&&u(n.TEXTURE_2D)}t.unbindTexture()}else{let ge=n.TEXTURE_2D;if((D.isWebGL3DRenderTarget||D.isWebGLArrayRenderTarget)&&(ge=D.isWebGL3DRenderTarget?n.TEXTURE_3D:n.TEXTURE_2D_ARRAY),t.bindTexture(ge,Q.__webglTexture),fe(ge,E),E.mipmaps&&E.mipmaps.length>0)for(let Ee=0;Ee<E.mipmaps.length;Ee++)ue(j.__webglFramebuffer[Ee],D,E,n.COLOR_ATTACHMENT0,ge,Ee);else ue(j.__webglFramebuffer,D,E,n.COLOR_ATTACHMENT0,ge,0);p(E)&&u(ge),t.unbindTexture()}D.depthBuffer&&_e(D)}function re(D){const E=D.textures;for(let j=0,Q=E.length;j<Q;j++){const ie=E[j];if(p(ie)){const J=y(D),Ae=i.get(ie).__webglTexture;t.bindTexture(J,Ae),u(J),t.unbindTexture()}}}const ae=[],I=[];function Ie(D){if(D.samples>0){if(Re(D)===!1){const E=D.textures,j=D.width,Q=D.height;let ie=n.COLOR_BUFFER_BIT;const J=D.stencilBuffer?n.DEPTH_STENCIL_ATTACHMENT:n.DEPTH_ATTACHMENT,Ae=i.get(D),ge=E.length>1;if(ge)for(let Ee=0;Ee<E.length;Ee++)t.bindFramebuffer(n.FRAMEBUFFER,Ae.__webglMultisampledFramebuffer),n.framebufferRenderbuffer(n.FRAMEBUFFER,n.COLOR_ATTACHMENT0+Ee,n.RENDERBUFFER,null),t.bindFramebuffer(n.FRAMEBUFFER,Ae.__webglFramebuffer),n.framebufferTexture2D(n.DRAW_FRAMEBUFFER,n.COLOR_ATTACHMENT0+Ee,n.TEXTURE_2D,null,0);t.bindFramebuffer(n.READ_FRAMEBUFFER,Ae.__webglMultisampledFramebuffer),t.bindFramebuffer(n.DRAW_FRAMEBUFFER,Ae.__webglFramebuffer);for(let Ee=0;Ee<E.length;Ee++){if(D.resolveDepthBuffer&&(D.depthBuffer&&(ie|=n.DEPTH_BUFFER_BIT),D.stencilBuffer&&D.resolveStencilBuffer&&(ie|=n.STENCIL_BUFFER_BIT)),ge){n.framebufferRenderbuffer(n.READ_FRAMEBUFFER,n.COLOR_ATTACHMENT0,n.RENDERBUFFER,Ae.__webglColorRenderbuffer[Ee]);const Ke=i.get(E[Ee]).__webglTexture;n.framebufferTexture2D(n.DRAW_FRAMEBUFFER,n.COLOR_ATTACHMENT0,n.TEXTURE_2D,Ke,0)}n.blitFramebuffer(0,0,j,Q,0,0,j,Q,ie,n.NEAREST),c===!0&&(ae.length=0,I.length=0,ae.push(n.COLOR_ATTACHMENT0+Ee),D.depthBuffer&&D.resolveDepthBuffer===!1&&(ae.push(J),I.push(J),n.invalidateFramebuffer(n.DRAW_FRAMEBUFFER,I)),n.invalidateFramebuffer(n.READ_FRAMEBUFFER,ae))}if(t.bindFramebuffer(n.READ_FRAMEBUFFER,null),t.bindFramebuffer(n.DRAW_FRAMEBUFFER,null),ge)for(let Ee=0;Ee<E.length;Ee++){t.bindFramebuffer(n.FRAMEBUFFER,Ae.__webglMultisampledFramebuffer),n.framebufferRenderbuffer(n.FRAMEBUFFER,n.COLOR_ATTACHMENT0+Ee,n.RENDERBUFFER,Ae.__webglColorRenderbuffer[Ee]);const Ke=i.get(E[Ee]).__webglTexture;t.bindFramebuffer(n.FRAMEBUFFER,Ae.__webglFramebuffer),n.framebufferTexture2D(n.DRAW_FRAMEBUFFER,n.COLOR_ATTACHMENT0+Ee,n.TEXTURE_2D,Ke,0)}t.bindFramebuffer(n.DRAW_FRAMEBUFFER,Ae.__webglMultisampledFramebuffer)}else if(D.depthBuffer&&D.resolveDepthBuffer===!1&&c){const E=D.stencilBuffer?n.DEPTH_STENCIL_ATTACHMENT:n.DEPTH_ATTACHMENT;n.invalidateFramebuffer(n.DRAW_FRAMEBUFFER,[E])}}}function Ce(D){return Math.min(r.maxSamples,D.samples)}function Re(D){const E=i.get(D);return D.samples>0&&e.has("WEBGL_multisampled_render_to_texture")===!0&&E.__useRenderToTexture!==!1}function Me(D){const E=s.render.frame;d.get(D)!==E&&(d.set(D,E),D.update())}function ke(D,E){const j=D.colorSpace,Q=D.format,ie=D.type;return D.isCompressedTexture===!0||D.isVideoTexture===!0||j!==wi&&j!==An&&(Je.getTransfer(j)===it?(Q!==Yt||ie!==pn)&&console.warn("THREE.WebGLTextures: sRGB encoded textures have to use RGBAFormat and UnsignedByteType."):console.error("THREE.WebGLTextures: Unsupported texture color space:",j)),E}function we(D){return typeof HTMLImageElement<"u"&&D instanceof HTMLImageElement?(l.width=D.naturalWidth||D.width,l.height=D.naturalHeight||D.height):typeof VideoFrame<"u"&&D instanceof VideoFrame?(l.width=D.displayWidth,l.height=D.displayHeight):(l.width=D.width,l.height=D.height),l}this.allocateTextureUnit=C,this.resetTextureUnits=U,this.setTexture2D=F,this.setTexture2DArray=N,this.setTexture3D=O,this.setTextureCube=z,this.rebindTextures=de,this.setupRenderTarget=Z,this.updateRenderTargetMipmap=re,this.updateMultisampleRenderTarget=Ie,this.setupDepthRenderbuffer=_e,this.setupFrameBufferTexture=ue,this.useMultisampledRTT=Re}function nm(n,e){function t(i,r=An){let a;const s=Je.getTransfer(r);if(i===pn)return n.UNSIGNED_BYTE;if(i===Ts)return n.UNSIGNED_SHORT_4_4_4_4;if(i===As)return n.UNSIGNED_SHORT_5_5_5_1;if(i===vc)return n.UNSIGNED_INT_5_9_9_9_REV;if(i===gc)return n.BYTE;if(i===_c)return n.SHORT;if(i===ji)return n.UNSIGNED_SHORT;if(i===bs)return n.INT;if(i===Zn)return n.UNSIGNED_INT;if(i===un)return n.FLOAT;if(i===qi)return n.HALF_FLOAT;if(i===xc)return n.ALPHA;if(i===Mc)return n.RGB;if(i===Yt)return n.RGBA;if(i===Sc)return n.LUMINANCE;if(i===Ec)return n.LUMINANCE_ALPHA;if(i===Mi)return n.DEPTH_COMPONENT;if(i===Ai)return n.DEPTH_STENCIL;if(i===yc)return n.RED;if(i===ws)return n.RED_INTEGER;if(i===bc)return n.RG;if(i===Rs)return n.RG_INTEGER;if(i===Cs)return n.RGBA_INTEGER;if(i===wr||i===Rr||i===Cr||i===Pr)if(s===it)if(a=e.get("WEBGL_compressed_texture_s3tc_srgb"),a!==null){if(i===wr)return a.COMPRESSED_SRGB_S3TC_DXT1_EXT;if(i===Rr)return a.COMPRESSED_SRGB_ALPHA_S3TC_DXT1_EXT;if(i===Cr)return a.COMPRESSED_SRGB_ALPHA_S3TC_DXT3_EXT;if(i===Pr)return a.COMPRESSED_SRGB_ALPHA_S3TC_DXT5_EXT}else return null;else if(a=e.get("WEBGL_compressed_texture_s3tc"),a!==null){if(i===wr)return a.COMPRESSED_RGB_S3TC_DXT1_EXT;if(i===Rr)return a.COMPRESSED_RGBA_S3TC_DXT1_EXT;if(i===Cr)return a.COMPRESSED_RGBA_S3TC_DXT3_EXT;if(i===Pr)return a.COMPRESSED_RGBA_S3TC_DXT5_EXT}else return null;if(i===ja||i===Wa||i===Xa||i===qa)if(a=e.get("WEBGL_compressed_texture_pvrtc"),a!==null){if(i===ja)return a.COMPRESSED_RGB_PVRTC_4BPPV1_IMG;if(i===Wa)return a.COMPRESSED_RGB_PVRTC_2BPPV1_IMG;if(i===Xa)return a.COMPRESSED_RGBA_PVRTC_4BPPV1_IMG;if(i===qa)return a.COMPRESSED_RGBA_PVRTC_2BPPV1_IMG}else return null;if(i===Ya||i===Ka||i===$a)if(a=e.get("WEBGL_compressed_texture_etc"),a!==null){if(i===Ya||i===Ka)return s===it?a.COMPRESSED_SRGB8_ETC2:a.COMPRESSED_RGB8_ETC2;if(i===$a)return s===it?a.COMPRESSED_SRGB8_ALPHA8_ETC2_EAC:a.COMPRESSED_RGBA8_ETC2_EAC}else return null;if(i===Za||i===Ja||i===Qa||i===es||i===ts||i===ns||i===is||i===rs||i===as||i===ss||i===os||i===cs||i===ls||i===us)if(a=e.get("WEBGL_compressed_texture_astc"),a!==null){if(i===Za)return s===it?a.COMPRESSED_SRGB8_ALPHA8_ASTC_4x4_KHR:a.COMPRESSED_RGBA_ASTC_4x4_KHR;if(i===Ja)return s===it?a.COMPRESSED_SRGB8_ALPHA8_ASTC_5x4_KHR:a.COMPRESSED_RGBA_ASTC_5x4_KHR;if(i===Qa)return s===it?a.COMPRESSED_SRGB8_ALPHA8_ASTC_5x5_KHR:a.COMPRESSED_RGBA_ASTC_5x5_KHR;if(i===es)return s===it?a.COMPRESSED_SRGB8_ALPHA8_ASTC_6x5_KHR:a.COMPRESSED_RGBA_ASTC_6x5_KHR;if(i===ts)return s===it?a.COMPRESSED_SRGB8_ALPHA8_ASTC_6x6_KHR:a.COMPRESSED_RGBA_ASTC_6x6_KHR;if(i===ns)return s===it?a.COMPRESSED_SRGB8_ALPHA8_ASTC_8x5_KHR:a.COMPRESSED_RGBA_ASTC_8x5_KHR;if(i===is)return s===it?a.COMPRESSED_SRGB8_ALPHA8_ASTC_8x6_KHR:a.COMPRESSED_RGBA_ASTC_8x6_KHR;if(i===rs)return s===it?a.COMPRESSED_SRGB8_ALPHA8_ASTC_8x8_KHR:a.COMPRESSED_RGBA_ASTC_8x8_KHR;if(i===as)return s===it?a.COMPRESSED_SRGB8_ALPHA8_ASTC_10x5_KHR:a.COMPRESSED_RGBA_ASTC_10x5_KHR;if(i===ss)return s===it?a.COMPRESSED_SRGB8_ALPHA8_ASTC_10x6_KHR:a.COMPRESSED_RGBA_ASTC_10x6_KHR;if(i===os)return s===it?a.COMPRESSED_SRGB8_ALPHA8_ASTC_10x8_KHR:a.COMPRESSED_RGBA_ASTC_10x8_KHR;if(i===cs)return s===it?a.COMPRESSED_SRGB8_ALPHA8_ASTC_10x10_KHR:a.COMPRESSED_RGBA_ASTC_10x10_KHR;if(i===ls)return s===it?a.COMPRESSED_SRGB8_ALPHA8_ASTC_12x10_KHR:a.COMPRESSED_RGBA_ASTC_12x10_KHR;if(i===us)return s===it?a.COMPRESSED_SRGB8_ALPHA8_ASTC_12x12_KHR:a.COMPRESSED_RGBA_ASTC_12x12_KHR}else return null;if(i===Dr||i===ds||i===hs)if(a=e.get("EXT_texture_compression_bptc"),a!==null){if(i===Dr)return s===it?a.COMPRESSED_SRGB_ALPHA_BPTC_UNORM_EXT:a.COMPRESSED_RGBA_BPTC_UNORM_EXT;if(i===ds)return a.COMPRESSED_RGB_BPTC_SIGNED_FLOAT_EXT;if(i===hs)return a.COMPRESSED_RGB_BPTC_UNSIGNED_FLOAT_EXT}else return null;if(i===Tc||i===fs||i===ps||i===ms)if(a=e.get("EXT_texture_compression_rgtc"),a!==null){if(i===Dr)return a.COMPRESSED_RED_RGTC1_EXT;if(i===fs)return a.COMPRESSED_SIGNED_RED_RGTC1_EXT;if(i===ps)return a.COMPRESSED_RED_GREEN_RGTC2_EXT;if(i===ms)return a.COMPRESSED_SIGNED_RED_GREEN_RGTC2_EXT}else return null;return i===Ti?n.UNSIGNED_INT_24_8:n[i]!==void 0?n[i]:null}return{convert:t}}const im=`
void main() {

	gl_Position = vec4( position, 1.0 );

}`,rm=`
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

}`;class am{constructor(){this.texture=null,this.mesh=null,this.depthNear=0,this.depthFar=0}init(e,t,i){if(this.texture===null){const r=new Rt,a=e.properties.get(r);a.__webglTexture=t.texture,(t.depthNear!==i.depthNear||t.depthFar!==i.depthFar)&&(this.depthNear=t.depthNear,this.depthFar=t.depthFar),this.texture=r}}getMesh(e){if(this.texture!==null&&this.mesh===null){const t=e.cameras[0].viewport,i=new Dn({vertexShader:im,fragmentShader:rm,uniforms:{depthColor:{value:this.texture},depthWidth:{value:t.z},depthHeight:{value:t.w}}});this.mesh=new je(new Li(20,20),i)}return this.mesh}reset(){this.texture=null,this.mesh=null}getDepthTexture(){return this.texture}}class sm extends Ci{constructor(e,t){super();const i=this;let r=null,a=1,s=null,o="local-floor",c=1,l=null,d=null,h=null,f=null,m=null,g=null;const _=new am,p=t.getContextAttributes();let u=null,y=null;const S=[],M=[],T=new Xe;let b=null;const w=new Bt;w.viewport=new dt;const L=new Bt;L.viewport=new dt;const x=[w,L],v=new Au;let R=null,U=null;this.cameraAutoUpdate=!0,this.enabled=!1,this.isPresenting=!1,this.getController=function(X){let ne=S[X];return ne===void 0&&(ne=new pa,S[X]=ne),ne.getTargetRaySpace()},this.getControllerGrip=function(X){let ne=S[X];return ne===void 0&&(ne=new pa,S[X]=ne),ne.getGripSpace()},this.getHand=function(X){let ne=S[X];return ne===void 0&&(ne=new pa,S[X]=ne),ne.getHandSpace()};function C(X){const ne=M.indexOf(X.inputSource);if(ne===-1)return;const ue=S[ne];ue!==void 0&&(ue.update(X.inputSource,X.frame,l||s),ue.dispatchEvent({type:X.type,data:X.inputSource}))}function P(){r.removeEventListener("select",C),r.removeEventListener("selectstart",C),r.removeEventListener("selectend",C),r.removeEventListener("squeeze",C),r.removeEventListener("squeezestart",C),r.removeEventListener("squeezeend",C),r.removeEventListener("end",P),r.removeEventListener("inputsourceschange",F);for(let X=0;X<S.length;X++){const ne=M[X];ne!==null&&(M[X]=null,S[X].disconnect(ne))}R=null,U=null,_.reset(),e.setRenderTarget(u),m=null,f=null,h=null,r=null,y=null,De.stop(),i.isPresenting=!1,e.setPixelRatio(b),e.setSize(T.width,T.height,!1),i.dispatchEvent({type:"sessionend"})}this.setFramebufferScaleFactor=function(X){a=X,i.isPresenting===!0&&console.warn("THREE.WebXRManager: Cannot change framebuffer scale while presenting.")},this.setReferenceSpaceType=function(X){o=X,i.isPresenting===!0&&console.warn("THREE.WebXRManager: Cannot change reference space type while presenting.")},this.getReferenceSpace=function(){return l||s},this.setReferenceSpace=function(X){l=X},this.getBaseLayer=function(){return f!==null?f:m},this.getBinding=function(){return h},this.getFrame=function(){return g},this.getSession=function(){return r},this.setSession=async function(X){if(r=X,r!==null){if(u=e.getRenderTarget(),r.addEventListener("select",C),r.addEventListener("selectstart",C),r.addEventListener("selectend",C),r.addEventListener("squeeze",C),r.addEventListener("squeezestart",C),r.addEventListener("squeezeend",C),r.addEventListener("end",P),r.addEventListener("inputsourceschange",F),p.xrCompatible!==!0&&await t.makeXRCompatible(),b=e.getPixelRatio(),e.getSize(T),typeof XRWebGLBinding<"u"&&"createProjectionLayer"in XRWebGLBinding.prototype){let ue=null,se=null,ee=null;p.depth&&(ee=p.stencil?t.DEPTH24_STENCIL8:t.DEPTH_COMPONENT24,ue=p.stencil?Ai:Mi,se=p.stencil?Ti:Zn);const _e={colorFormat:t.RGBA8,depthFormat:ee,scaleFactor:a};h=new XRWebGLBinding(r,t),f=h.createProjectionLayer(_e),r.updateRenderState({layers:[f]}),e.setPixelRatio(1),e.setSize(f.textureWidth,f.textureHeight,!1),y=new Jn(f.textureWidth,f.textureHeight,{format:Yt,type:pn,depthTexture:new Nc(f.textureWidth,f.textureHeight,se,void 0,void 0,void 0,void 0,void 0,void 0,ue),stencilBuffer:p.stencil,colorSpace:e.outputColorSpace,samples:p.antialias?4:0,resolveDepthBuffer:f.ignoreDepthValues===!1,resolveStencilBuffer:f.ignoreDepthValues===!1})}else{const ue={antialias:p.antialias,alpha:!0,depth:p.depth,stencil:p.stencil,framebufferScaleFactor:a};m=new XRWebGLLayer(r,t,ue),r.updateRenderState({baseLayer:m}),e.setPixelRatio(1),e.setSize(m.framebufferWidth,m.framebufferHeight,!1),y=new Jn(m.framebufferWidth,m.framebufferHeight,{format:Yt,type:pn,colorSpace:e.outputColorSpace,stencilBuffer:p.stencil,resolveDepthBuffer:m.ignoreDepthValues===!1,resolveStencilBuffer:m.ignoreDepthValues===!1})}y.isXRRenderTarget=!0,this.setFoveation(c),l=null,s=await r.requestReferenceSpace(o),De.setContext(r),De.start(),i.isPresenting=!0,i.dispatchEvent({type:"sessionstart"})}},this.getEnvironmentBlendMode=function(){if(r!==null)return r.environmentBlendMode},this.getDepthTexture=function(){return _.getDepthTexture()};function F(X){for(let ne=0;ne<X.removed.length;ne++){const ue=X.removed[ne],se=M.indexOf(ue);se>=0&&(M[se]=null,S[se].disconnect(ue))}for(let ne=0;ne<X.added.length;ne++){const ue=X.added[ne];let se=M.indexOf(ue);if(se===-1){for(let _e=0;_e<S.length;_e++)if(_e>=M.length){M.push(ue),se=_e;break}else if(M[_e]===null){M[_e]=ue,se=_e;break}if(se===-1)break}const ee=S[se];ee&&ee.connect(ue)}}const N=new k,O=new k;function z(X,ne,ue){N.setFromMatrixPosition(ne.matrixWorld),O.setFromMatrixPosition(ue.matrixWorld);const se=N.distanceTo(O),ee=ne.projectionMatrix.elements,_e=ue.projectionMatrix.elements,de=ee[14]/(ee[10]-1),Z=ee[14]/(ee[10]+1),re=(ee[9]+1)/ee[5],ae=(ee[9]-1)/ee[5],I=(ee[8]-1)/ee[0],Ie=(_e[8]+1)/_e[0],Ce=de*I,Re=de*Ie,Me=se/(-I+Ie),ke=Me*-I;if(ne.matrixWorld.decompose(X.position,X.quaternion,X.scale),X.translateX(ke),X.translateZ(Me),X.matrixWorld.compose(X.position,X.quaternion,X.scale),X.matrixWorldInverse.copy(X.matrixWorld).invert(),ee[10]===-1)X.projectionMatrix.copy(ne.projectionMatrix),X.projectionMatrixInverse.copy(ne.projectionMatrixInverse);else{const we=de+Me,D=Z+Me,E=Ce-ke,j=Re+(se-ke),Q=re*Z/D*we,ie=ae*Z/D*we;X.projectionMatrix.makePerspective(E,j,Q,ie,we,D),X.projectionMatrixInverse.copy(X.projectionMatrix).invert()}}function G(X,ne){ne===null?X.matrixWorld.copy(X.matrix):X.matrixWorld.multiplyMatrices(ne.matrixWorld,X.matrix),X.matrixWorldInverse.copy(X.matrixWorld).invert()}this.updateCamera=function(X){if(r===null)return;let ne=X.near,ue=X.far;_.texture!==null&&(_.depthNear>0&&(ne=_.depthNear),_.depthFar>0&&(ue=_.depthFar)),v.near=L.near=w.near=ne,v.far=L.far=w.far=ue,(R!==v.near||U!==v.far)&&(r.updateRenderState({depthNear:v.near,depthFar:v.far}),R=v.near,U=v.far),w.layers.mask=X.layers.mask|2,L.layers.mask=X.layers.mask|4,v.layers.mask=w.layers.mask|L.layers.mask;const se=X.parent,ee=v.cameras;G(v,se);for(let _e=0;_e<ee.length;_e++)G(ee[_e],se);ee.length===2?z(v,w,L):v.projectionMatrix.copy(w.projectionMatrix),K(X,v,se)};function K(X,ne,ue){ue===null?X.matrix.copy(ne.matrixWorld):(X.matrix.copy(ue.matrixWorld),X.matrix.invert(),X.matrix.multiply(ne.matrixWorld)),X.matrix.decompose(X.position,X.quaternion,X.scale),X.updateMatrixWorld(!0),X.projectionMatrix.copy(ne.projectionMatrix),X.projectionMatrixInverse.copy(ne.projectionMatrixInverse),X.isPerspectiveCamera&&(X.fov=gs*2*Math.atan(1/X.projectionMatrix.elements[5]),X.zoom=1)}this.getCamera=function(){return v},this.getFoveation=function(){if(!(f===null&&m===null))return c},this.setFoveation=function(X){c=X,f!==null&&(f.fixedFoveation=X),m!==null&&m.fixedFoveation!==void 0&&(m.fixedFoveation=X)},this.hasDepthSensing=function(){return _.texture!==null},this.getDepthSensingMesh=function(){return _.getMesh(v)};let $=null;function fe(X,ne){if(d=ne.getViewerPose(l||s),g=ne,d!==null){const ue=d.views;m!==null&&(e.setRenderTargetFramebuffer(y,m.framebuffer),e.setRenderTarget(y));let se=!1;ue.length!==v.cameras.length&&(v.cameras.length=0,se=!0);for(let de=0;de<ue.length;de++){const Z=ue[de];let re=null;if(m!==null)re=m.getViewport(Z);else{const I=h.getViewSubImage(f,Z);re=I.viewport,de===0&&(e.setRenderTargetTextures(y,I.colorTexture,f.ignoreDepthValues?void 0:I.depthStencilTexture),e.setRenderTarget(y))}let ae=x[de];ae===void 0&&(ae=new Bt,ae.layers.enable(de),ae.viewport=new dt,x[de]=ae),ae.matrix.fromArray(Z.transform.matrix),ae.matrix.decompose(ae.position,ae.quaternion,ae.scale),ae.projectionMatrix.fromArray(Z.projectionMatrix),ae.projectionMatrixInverse.copy(ae.projectionMatrix).invert(),ae.viewport.set(re.x,re.y,re.width,re.height),de===0&&(v.matrix.copy(ae.matrix),v.matrix.decompose(v.position,v.quaternion,v.scale)),se===!0&&v.cameras.push(ae)}const ee=r.enabledFeatures;if(ee&&ee.includes("depth-sensing")&&r.depthUsage=="gpu-optimized"&&h){const de=h.getDepthInformation(ue[0]);de&&de.isValid&&de.texture&&_.init(e,de,r.renderState)}}for(let ue=0;ue<S.length;ue++){const se=M[ue],ee=S[ue];se!==null&&ee!==void 0&&ee.update(se,ne,l||s)}$&&$(X,ne),ne.detectedPlanes&&i.dispatchEvent({type:"planesdetected",data:ne}),g=null}const De=new Oc;De.setAnimationLoop(fe),this.setAnimationLoop=function(X){$=X},this.dispose=function(){}}}const On=new Mt,om=new at;function cm(n,e){function t(p,u){p.matrixAutoUpdate===!0&&p.updateMatrix(),u.value.copy(p.matrix)}function i(p,u){u.color.getRGB(p.fogColor.value,Ic(n)),u.isFog?(p.fogNear.value=u.near,p.fogFar.value=u.far):u.isFogExp2&&(p.fogDensity.value=u.density)}function r(p,u,y,S,M){u.isMeshBasicMaterial||u.isMeshLambertMaterial?a(p,u):u.isMeshToonMaterial?(a(p,u),h(p,u)):u.isMeshPhongMaterial?(a(p,u),d(p,u)):u.isMeshStandardMaterial?(a(p,u),f(p,u),u.isMeshPhysicalMaterial&&m(p,u,M)):u.isMeshMatcapMaterial?(a(p,u),g(p,u)):u.isMeshDepthMaterial?a(p,u):u.isMeshDistanceMaterial?(a(p,u),_(p,u)):u.isMeshNormalMaterial?a(p,u):u.isLineBasicMaterial?(s(p,u),u.isLineDashedMaterial&&o(p,u)):u.isPointsMaterial?c(p,u,y,S):u.isSpriteMaterial?l(p,u):u.isShadowMaterial?(p.color.value.copy(u.color),p.opacity.value=u.opacity):u.isShaderMaterial&&(u.uniformsNeedUpdate=!1)}function a(p,u){p.opacity.value=u.opacity,u.color&&p.diffuse.value.copy(u.color),u.emissive&&p.emissive.value.copy(u.emissive).multiplyScalar(u.emissiveIntensity),u.map&&(p.map.value=u.map,t(u.map,p.mapTransform)),u.alphaMap&&(p.alphaMap.value=u.alphaMap,t(u.alphaMap,p.alphaMapTransform)),u.bumpMap&&(p.bumpMap.value=u.bumpMap,t(u.bumpMap,p.bumpMapTransform),p.bumpScale.value=u.bumpScale,u.side===Dt&&(p.bumpScale.value*=-1)),u.normalMap&&(p.normalMap.value=u.normalMap,t(u.normalMap,p.normalMapTransform),p.normalScale.value.copy(u.normalScale),u.side===Dt&&p.normalScale.value.negate()),u.displacementMap&&(p.displacementMap.value=u.displacementMap,t(u.displacementMap,p.displacementMapTransform),p.displacementScale.value=u.displacementScale,p.displacementBias.value=u.displacementBias),u.emissiveMap&&(p.emissiveMap.value=u.emissiveMap,t(u.emissiveMap,p.emissiveMapTransform)),u.specularMap&&(p.specularMap.value=u.specularMap,t(u.specularMap,p.specularMapTransform)),u.alphaTest>0&&(p.alphaTest.value=u.alphaTest);const y=e.get(u),S=y.envMap,M=y.envMapRotation;S&&(p.envMap.value=S,On.copy(M),On.x*=-1,On.y*=-1,On.z*=-1,S.isCubeTexture&&S.isRenderTargetTexture===!1&&(On.y*=-1,On.z*=-1),p.envMapRotation.value.setFromMatrix4(om.makeRotationFromEuler(On)),p.flipEnvMap.value=S.isCubeTexture&&S.isRenderTargetTexture===!1?-1:1,p.reflectivity.value=u.reflectivity,p.ior.value=u.ior,p.refractionRatio.value=u.refractionRatio),u.lightMap&&(p.lightMap.value=u.lightMap,p.lightMapIntensity.value=u.lightMapIntensity,t(u.lightMap,p.lightMapTransform)),u.aoMap&&(p.aoMap.value=u.aoMap,p.aoMapIntensity.value=u.aoMapIntensity,t(u.aoMap,p.aoMapTransform))}function s(p,u){p.diffuse.value.copy(u.color),p.opacity.value=u.opacity,u.map&&(p.map.value=u.map,t(u.map,p.mapTransform))}function o(p,u){p.dashSize.value=u.dashSize,p.totalSize.value=u.dashSize+u.gapSize,p.scale.value=u.scale}function c(p,u,y,S){p.diffuse.value.copy(u.color),p.opacity.value=u.opacity,p.size.value=u.size*y,p.scale.value=S*.5,u.map&&(p.map.value=u.map,t(u.map,p.uvTransform)),u.alphaMap&&(p.alphaMap.value=u.alphaMap,t(u.alphaMap,p.alphaMapTransform)),u.alphaTest>0&&(p.alphaTest.value=u.alphaTest)}function l(p,u){p.diffuse.value.copy(u.color),p.opacity.value=u.opacity,p.rotation.value=u.rotation,u.map&&(p.map.value=u.map,t(u.map,p.mapTransform)),u.alphaMap&&(p.alphaMap.value=u.alphaMap,t(u.alphaMap,p.alphaMapTransform)),u.alphaTest>0&&(p.alphaTest.value=u.alphaTest)}function d(p,u){p.specular.value.copy(u.specular),p.shininess.value=Math.max(u.shininess,1e-4)}function h(p,u){u.gradientMap&&(p.gradientMap.value=u.gradientMap)}function f(p,u){p.metalness.value=u.metalness,u.metalnessMap&&(p.metalnessMap.value=u.metalnessMap,t(u.metalnessMap,p.metalnessMapTransform)),p.roughness.value=u.roughness,u.roughnessMap&&(p.roughnessMap.value=u.roughnessMap,t(u.roughnessMap,p.roughnessMapTransform)),u.envMap&&(p.envMapIntensity.value=u.envMapIntensity)}function m(p,u,y){p.ior.value=u.ior,u.sheen>0&&(p.sheenColor.value.copy(u.sheenColor).multiplyScalar(u.sheen),p.sheenRoughness.value=u.sheenRoughness,u.sheenColorMap&&(p.sheenColorMap.value=u.sheenColorMap,t(u.sheenColorMap,p.sheenColorMapTransform)),u.sheenRoughnessMap&&(p.sheenRoughnessMap.value=u.sheenRoughnessMap,t(u.sheenRoughnessMap,p.sheenRoughnessMapTransform))),u.clearcoat>0&&(p.clearcoat.value=u.clearcoat,p.clearcoatRoughness.value=u.clearcoatRoughness,u.clearcoatMap&&(p.clearcoatMap.value=u.clearcoatMap,t(u.clearcoatMap,p.clearcoatMapTransform)),u.clearcoatRoughnessMap&&(p.clearcoatRoughnessMap.value=u.clearcoatRoughnessMap,t(u.clearcoatRoughnessMap,p.clearcoatRoughnessMapTransform)),u.clearcoatNormalMap&&(p.clearcoatNormalMap.value=u.clearcoatNormalMap,t(u.clearcoatNormalMap,p.clearcoatNormalMapTransform),p.clearcoatNormalScale.value.copy(u.clearcoatNormalScale),u.side===Dt&&p.clearcoatNormalScale.value.negate())),u.dispersion>0&&(p.dispersion.value=u.dispersion),u.iridescence>0&&(p.iridescence.value=u.iridescence,p.iridescenceIOR.value=u.iridescenceIOR,p.iridescenceThicknessMinimum.value=u.iridescenceThicknessRange[0],p.iridescenceThicknessMaximum.value=u.iridescenceThicknessRange[1],u.iridescenceMap&&(p.iridescenceMap.value=u.iridescenceMap,t(u.iridescenceMap,p.iridescenceMapTransform)),u.iridescenceThicknessMap&&(p.iridescenceThicknessMap.value=u.iridescenceThicknessMap,t(u.iridescenceThicknessMap,p.iridescenceThicknessMapTransform))),u.transmission>0&&(p.transmission.value=u.transmission,p.transmissionSamplerMap.value=y.texture,p.transmissionSamplerSize.value.set(y.width,y.height),u.transmissionMap&&(p.transmissionMap.value=u.transmissionMap,t(u.transmissionMap,p.transmissionMapTransform)),p.thickness.value=u.thickness,u.thicknessMap&&(p.thicknessMap.value=u.thicknessMap,t(u.thicknessMap,p.thicknessMapTransform)),p.attenuationDistance.value=u.attenuationDistance,p.attenuationColor.value.copy(u.attenuationColor)),u.anisotropy>0&&(p.anisotropyVector.value.set(u.anisotropy*Math.cos(u.anisotropyRotation),u.anisotropy*Math.sin(u.anisotropyRotation)),u.anisotropyMap&&(p.anisotropyMap.value=u.anisotropyMap,t(u.anisotropyMap,p.anisotropyMapTransform))),p.specularIntensity.value=u.specularIntensity,p.specularColor.value.copy(u.specularColor),u.specularColorMap&&(p.specularColorMap.value=u.specularColorMap,t(u.specularColorMap,p.specularColorMapTransform)),u.specularIntensityMap&&(p.specularIntensityMap.value=u.specularIntensityMap,t(u.specularIntensityMap,p.specularIntensityMapTransform))}function g(p,u){u.matcap&&(p.matcap.value=u.matcap)}function _(p,u){const y=e.get(u).light;p.referencePosition.value.setFromMatrixPosition(y.matrixWorld),p.nearDistance.value=y.shadow.camera.near,p.farDistance.value=y.shadow.camera.far}return{refreshFogUniforms:i,refreshMaterialUniforms:r}}function lm(n,e,t,i){let r={},a={},s=[];const o=n.getParameter(n.MAX_UNIFORM_BUFFER_BINDINGS);function c(y,S){const M=S.program;i.uniformBlockBinding(y,M)}function l(y,S){let M=r[y.id];M===void 0&&(g(y),M=d(y),r[y.id]=M,y.addEventListener("dispose",p));const T=S.program;i.updateUBOMapping(y,T);const b=e.render.frame;a[y.id]!==b&&(f(y),a[y.id]=b)}function d(y){const S=h();y.__bindingPointIndex=S;const M=n.createBuffer(),T=y.__size,b=y.usage;return n.bindBuffer(n.UNIFORM_BUFFER,M),n.bufferData(n.UNIFORM_BUFFER,T,b),n.bindBuffer(n.UNIFORM_BUFFER,null),n.bindBufferBase(n.UNIFORM_BUFFER,S,M),M}function h(){for(let y=0;y<o;y++)if(s.indexOf(y)===-1)return s.push(y),y;return console.error("THREE.WebGLRenderer: Maximum number of simultaneously usable uniforms groups reached."),0}function f(y){const S=r[y.id],M=y.uniforms,T=y.__cache;n.bindBuffer(n.UNIFORM_BUFFER,S);for(let b=0,w=M.length;b<w;b++){const L=Array.isArray(M[b])?M[b]:[M[b]];for(let x=0,v=L.length;x<v;x++){const R=L[x];if(m(R,b,x,T)===!0){const U=R.__offset,C=Array.isArray(R.value)?R.value:[R.value];let P=0;for(let F=0;F<C.length;F++){const N=C[F],O=_(N);typeof N=="number"||typeof N=="boolean"?(R.__data[0]=N,n.bufferSubData(n.UNIFORM_BUFFER,U+P,R.__data)):N.isMatrix3?(R.__data[0]=N.elements[0],R.__data[1]=N.elements[1],R.__data[2]=N.elements[2],R.__data[3]=0,R.__data[4]=N.elements[3],R.__data[5]=N.elements[4],R.__data[6]=N.elements[5],R.__data[7]=0,R.__data[8]=N.elements[6],R.__data[9]=N.elements[7],R.__data[10]=N.elements[8],R.__data[11]=0):(N.toArray(R.__data,P),P+=O.storage/Float32Array.BYTES_PER_ELEMENT)}n.bufferSubData(n.UNIFORM_BUFFER,U,R.__data)}}}n.bindBuffer(n.UNIFORM_BUFFER,null)}function m(y,S,M,T){const b=y.value,w=S+"_"+M;if(T[w]===void 0)return typeof b=="number"||typeof b=="boolean"?T[w]=b:T[w]=b.clone(),!0;{const L=T[w];if(typeof b=="number"||typeof b=="boolean"){if(L!==b)return T[w]=b,!0}else if(L.equals(b)===!1)return L.copy(b),!0}return!1}function g(y){const S=y.uniforms;let M=0;const T=16;for(let w=0,L=S.length;w<L;w++){const x=Array.isArray(S[w])?S[w]:[S[w]];for(let v=0,R=x.length;v<R;v++){const U=x[v],C=Array.isArray(U.value)?U.value:[U.value];for(let P=0,F=C.length;P<F;P++){const N=C[P],O=_(N),z=M%T,G=z%O.boundary,K=z+G;M+=G,K!==0&&T-K<O.storage&&(M+=T-K),U.__data=new Float32Array(O.storage/Float32Array.BYTES_PER_ELEMENT),U.__offset=M,M+=O.storage}}}const b=M%T;return b>0&&(M+=T-b),y.__size=M,y.__cache={},this}function _(y){const S={boundary:0,storage:0};return typeof y=="number"||typeof y=="boolean"?(S.boundary=4,S.storage=4):y.isVector2?(S.boundary=8,S.storage=8):y.isVector3||y.isColor?(S.boundary=16,S.storage=12):y.isVector4?(S.boundary=16,S.storage=16):y.isMatrix3?(S.boundary=48,S.storage=48):y.isMatrix4?(S.boundary=64,S.storage=64):y.isTexture?console.warn("THREE.WebGLRenderer: Texture samplers can not be part of an uniforms group."):console.warn("THREE.WebGLRenderer: Unsupported uniform value type.",y),S}function p(y){const S=y.target;S.removeEventListener("dispose",p);const M=s.indexOf(S.__bindingPointIndex);s.splice(M,1),n.deleteBuffer(r[S.id]),delete r[S.id],delete a[S.id]}function u(){for(const y in r)n.deleteBuffer(r[y]);s=[],r={},a={}}return{bind:c,update:l,dispose:u}}class um{constructor(e={}){const{canvas:t=Gl(),context:i=null,depth:r=!0,stencil:a=!1,alpha:s=!1,antialias:o=!1,premultipliedAlpha:c=!0,preserveDrawingBuffer:l=!1,powerPreference:d="default",failIfMajorPerformanceCaveat:h=!1,reverseDepthBuffer:f=!1}=e;this.isWebGLRenderer=!0;let m;if(i!==null){if(typeof WebGLRenderingContext<"u"&&i instanceof WebGLRenderingContext)throw new Error("THREE.WebGLRenderer: WebGL 1 is not supported since r163.");m=i.getContextAttributes().alpha}else m=s;const g=new Uint32Array(4),_=new Int32Array(4);let p=null,u=null;const y=[],S=[];this.domElement=t,this.debug={checkShaderErrors:!0,onShaderError:null},this.autoClear=!0,this.autoClearColor=!0,this.autoClearDepth=!0,this.autoClearStencil=!0,this.sortObjects=!0,this.clippingPlanes=[],this.localClippingEnabled=!1,this._outputColorSpace=Nt,this.toneMapping=Cn,this.toneMappingExposure=1;const M=this;let T=!1,b=0,w=0,L=null,x=-1,v=null;const R=new dt,U=new dt;let C=null;const P=new ce(0);let F=0,N=t.width,O=t.height,z=1,G=null,K=null;const $=new dt(0,0,N,O),fe=new dt(0,0,N,O);let De=!1;const X=new Is;let ne=!1,ue=!1;this.transmissionResolutionScale=1;const se=new at,ee=new at,_e=new k,de=new dt,Z={background:null,fog:null,environment:null,overrideMaterial:null,isScene:!0};let re=!1;function ae(){return L===null?z:1}let I=i;function Ie(A,V){return t.getContext(A,V)}try{const A={alpha:!0,depth:r,stencil:a,antialias:o,premultipliedAlpha:c,preserveDrawingBuffer:l,powerPreference:d,failIfMajorPerformanceCaveat:h};if("setAttribute"in t&&t.setAttribute("data-engine",`three.js r${ys}`),t.addEventListener("webglcontextlost",te,!1),t.addEventListener("webglcontextrestored",xe,!1),t.addEventListener("webglcontextcreationerror",ve,!1),I===null){const V="webgl2";if(I=Ie(V,A),I===null)throw Ie(V)?new Error("Error creating WebGL context with your selected attributes."):new Error("Error creating WebGL context.")}}catch(A){throw console.error("THREE.WebGLRenderer: "+A.message),A}let Ce,Re,Me,ke,we,D,E,j,Q,ie,J,Ae,ge,Ee,Ke,le,ye,Ue,ze,be,qe,Ve,rt,B;function pe(){Ce=new Mf(I),Ce.init(),Ve=new nm(I,Ce),Re=new ff(I,Ce,e,Ve),Me=new em(I,Ce),Re.reverseDepthBuffer&&f&&Me.buffers.depth.setReversed(!0),ke=new yf(I),we=new Vp,D=new tm(I,Ce,Me,we,Re,Ve,ke),E=new mf(M),j=new xf(M),Q=new Ru(I),rt=new df(I,Q),ie=new Sf(I,Q,ke,rt),J=new Tf(I,ie,Q,ke),ze=new bf(I,Re,D),le=new pf(we),Ae=new Bp(M,E,j,Ce,Re,rt,le),ge=new cm(M,we),Ee=new Gp,Ke=new Kp(Ce),Ue=new uf(M,E,j,Me,J,m,c),ye=new Jp(M,J,Re),B=new lm(I,ke,Re,Me),be=new hf(I,Ce,ke),qe=new Ef(I,Ce,ke),ke.programs=Ae.programs,M.capabilities=Re,M.extensions=Ce,M.properties=we,M.renderLists=Ee,M.shadowMap=ye,M.state=Me,M.info=ke}pe();const Y=new sm(M,I);this.xr=Y,this.getContext=function(){return I},this.getContextAttributes=function(){return I.getContextAttributes()},this.forceContextLoss=function(){const A=Ce.get("WEBGL_lose_context");A&&A.loseContext()},this.forceContextRestore=function(){const A=Ce.get("WEBGL_lose_context");A&&A.restoreContext()},this.getPixelRatio=function(){return z},this.setPixelRatio=function(A){A!==void 0&&(z=A,this.setSize(N,O,!1))},this.getSize=function(A){return A.set(N,O)},this.setSize=function(A,V,W=!0){if(Y.isPresenting){console.warn("THREE.WebGLRenderer: Can't change size while VR device is presenting.");return}N=A,O=V,t.width=Math.floor(A*z),t.height=Math.floor(V*z),W===!0&&(t.style.width=A+"px",t.style.height=V+"px"),this.setViewport(0,0,A,V)},this.getDrawingBufferSize=function(A){return A.set(N*z,O*z).floor()},this.setDrawingBufferSize=function(A,V,W){N=A,O=V,z=W,t.width=Math.floor(A*W),t.height=Math.floor(V*W),this.setViewport(0,0,A,V)},this.getCurrentViewport=function(A){return A.copy(R)},this.getViewport=function(A){return A.copy($)},this.setViewport=function(A,V,W,q){A.isVector4?$.set(A.x,A.y,A.z,A.w):$.set(A,V,W,q),Me.viewport(R.copy($).multiplyScalar(z).round())},this.getScissor=function(A){return A.copy(fe)},this.setScissor=function(A,V,W,q){A.isVector4?fe.set(A.x,A.y,A.z,A.w):fe.set(A,V,W,q),Me.scissor(U.copy(fe).multiplyScalar(z).round())},this.getScissorTest=function(){return De},this.setScissorTest=function(A){Me.setScissorTest(De=A)},this.setOpaqueSort=function(A){G=A},this.setTransparentSort=function(A){K=A},this.getClearColor=function(A){return A.copy(Ue.getClearColor())},this.setClearColor=function(){Ue.setClearColor(...arguments)},this.getClearAlpha=function(){return Ue.getClearAlpha()},this.setClearAlpha=function(){Ue.setClearAlpha(...arguments)},this.clear=function(A=!0,V=!0,W=!0){let q=0;if(A){let H=!1;if(L!==null){const oe=L.texture.format;H=oe===Cs||oe===Rs||oe===ws}if(H){const oe=L.texture.type,me=oe===pn||oe===Zn||oe===ji||oe===Ti||oe===Ts||oe===As,Se=Ue.getClearColor(),Te=Ue.getClearAlpha(),Ne=Se.r,Fe=Se.g,Pe=Se.b;me?(g[0]=Ne,g[1]=Fe,g[2]=Pe,g[3]=Te,I.clearBufferuiv(I.COLOR,0,g)):(_[0]=Ne,_[1]=Fe,_[2]=Pe,_[3]=Te,I.clearBufferiv(I.COLOR,0,_))}else q|=I.COLOR_BUFFER_BIT}V&&(q|=I.DEPTH_BUFFER_BIT),W&&(q|=I.STENCIL_BUFFER_BIT,this.state.buffers.stencil.setMask(4294967295)),I.clear(q)},this.clearColor=function(){this.clear(!0,!1,!1)},this.clearDepth=function(){this.clear(!1,!0,!1)},this.clearStencil=function(){this.clear(!1,!1,!0)},this.dispose=function(){t.removeEventListener("webglcontextlost",te,!1),t.removeEventListener("webglcontextrestored",xe,!1),t.removeEventListener("webglcontextcreationerror",ve,!1),Ue.dispose(),Ee.dispose(),Ke.dispose(),we.dispose(),E.dispose(),j.dispose(),J.dispose(),rt.dispose(),B.dispose(),Ae.dispose(),Y.dispose(),Y.removeEventListener("sessionstart",Os),Y.removeEventListener("sessionend",Bs),Ln.stop()};function te(A){A.preventDefault(),console.log("THREE.WebGLRenderer: Context Lost."),T=!0}function xe(){console.log("THREE.WebGLRenderer: Context Restored."),T=!1;const A=ke.autoReset,V=ye.enabled,W=ye.autoUpdate,q=ye.needsUpdate,H=ye.type;pe(),ke.autoReset=A,ye.enabled=V,ye.autoUpdate=W,ye.needsUpdate=q,ye.type=H}function ve(A){console.error("THREE.WebGLRenderer: A WebGL context could not be created. Reason: ",A.statusMessage)}function Oe(A){const V=A.target;V.removeEventListener("dispose",Oe),lt(V)}function lt(A){yt(A),we.remove(A)}function yt(A){const V=we.get(A).programs;V!==void 0&&(V.forEach(function(W){Ae.releaseProgram(W)}),A.isShaderMaterial&&Ae.releaseShaderCache(A))}this.renderBufferDirect=function(A,V,W,q,H,oe){V===null&&(V=Z);const me=H.isMesh&&H.matrixWorld.determinant()<0,Se=Xc(A,V,W,q,H);Me.setMaterial(q,me);let Te=W.index,Ne=1;if(q.wireframe===!0){if(Te=ie.getWireframeAttribute(W),Te===void 0)return;Ne=2}const Fe=W.drawRange,Pe=W.attributes.position;let $e=Fe.start*Ne,Qe=(Fe.start+Fe.count)*Ne;oe!==null&&($e=Math.max($e,oe.start*Ne),Qe=Math.min(Qe,(oe.start+oe.count)*Ne)),Te!==null?($e=Math.max($e,0),Qe=Math.min(Qe,Te.count)):Pe!=null&&($e=Math.max($e,0),Qe=Math.min(Qe,Pe.count));const ft=Qe-$e;if(ft<0||ft===1/0)return;rt.setup(H,q,Se,W,Te);let ut,Ze=be;if(Te!==null&&(ut=Q.get(Te),Ze=qe,Ze.setIndex(ut)),H.isMesh)q.wireframe===!0?(Me.setLineWidth(q.wireframeLinewidth*ae()),Ze.setMode(I.LINES)):Ze.setMode(I.TRIANGLES);else if(H.isLine){let Le=q.linewidth;Le===void 0&&(Le=1),Me.setLineWidth(Le*ae()),H.isLineSegments?Ze.setMode(I.LINES):H.isLineLoop?Ze.setMode(I.LINE_LOOP):Ze.setMode(I.LINE_STRIP)}else H.isPoints?Ze.setMode(I.POINTS):H.isSprite&&Ze.setMode(I.TRIANGLES);if(H.isBatchedMesh)if(H._multiDrawInstances!==null)Bn("THREE.WebGLRenderer: renderMultiDrawInstances has been deprecated and will be removed in r184. Append to renderMultiDraw arguments and use indirection."),Ze.renderMultiDrawInstances(H._multiDrawStarts,H._multiDrawCounts,H._multiDrawCount,H._multiDrawInstances);else if(Ce.get("WEBGL_multi_draw"))Ze.renderMultiDraw(H._multiDrawStarts,H._multiDrawCounts,H._multiDrawCount);else{const Le=H._multiDrawStarts,St=H._multiDrawCounts,et=H._multiDrawCount,Gt=Te?Q.get(Te).bytesPerElement:1,Qn=we.get(q).currentProgram.getUniforms();for(let It=0;It<et;It++)Qn.setValue(I,"_gl_DrawID",It),Ze.render(Le[It]/Gt,St[It])}else if(H.isInstancedMesh)Ze.renderInstances($e,ft,H.count);else if(W.isInstancedBufferGeometry){const Le=W._maxInstanceCount!==void 0?W._maxInstanceCount:1/0,St=Math.min(W.instanceCount,Le);Ze.renderInstances($e,ft,St)}else Ze.render($e,ft)};function tt(A,V,W){A.transparent===!0&&A.side===mt&&A.forceSinglePass===!1?(A.side=Dt,A.needsUpdate=!0,Qi(A,V,W),A.side=Pn,A.needsUpdate=!0,Qi(A,V,W),A.side=mt):Qi(A,V,W)}this.compile=function(A,V,W=null){W===null&&(W=A),u=Ke.get(W),u.init(V),S.push(u),W.traverseVisible(function(H){H.isLight&&H.layers.test(V.layers)&&(u.pushLight(H),H.castShadow&&u.pushShadow(H))}),A!==W&&A.traverseVisible(function(H){H.isLight&&H.layers.test(V.layers)&&(u.pushLight(H),H.castShadow&&u.pushShadow(H))}),u.setupLights();const q=new Set;return A.traverse(function(H){if(!(H.isMesh||H.isPoints||H.isLine||H.isSprite))return;const oe=H.material;if(oe)if(Array.isArray(oe))for(let me=0;me<oe.length;me++){const Se=oe[me];tt(Se,W,H),q.add(Se)}else tt(oe,W,H),q.add(oe)}),u=S.pop(),q},this.compileAsync=function(A,V,W=null){const q=this.compile(A,V,W);return new Promise(H=>{function oe(){if(q.forEach(function(me){we.get(me).currentProgram.isReady()&&q.delete(me)}),q.size===0){H(A);return}setTimeout(oe,10)}Ce.get("KHR_parallel_shader_compile")!==null?oe():setTimeout(oe,10)})};let Ht=null;function Qt(A){Ht&&Ht(A)}function Os(){Ln.stop()}function Bs(){Ln.start()}const Ln=new Oc;Ln.setAnimationLoop(Qt),typeof self<"u"&&Ln.setContext(self),this.setAnimationLoop=function(A){Ht=A,Y.setAnimationLoop(A),A===null?Ln.stop():Ln.start()},Y.addEventListener("sessionstart",Os),Y.addEventListener("sessionend",Bs),this.render=function(A,V){if(V!==void 0&&V.isCamera!==!0){console.error("THREE.WebGLRenderer.render: camera is not an instance of THREE.Camera.");return}if(T===!0)return;if(A.matrixWorldAutoUpdate===!0&&A.updateMatrixWorld(),V.parent===null&&V.matrixWorldAutoUpdate===!0&&V.updateMatrixWorld(),Y.enabled===!0&&Y.isPresenting===!0&&(Y.cameraAutoUpdate===!0&&Y.updateCamera(V),V=Y.getCamera()),A.isScene===!0&&A.onBeforeRender(M,A,V,L),u=Ke.get(A,S.length),u.init(V),S.push(u),ee.multiplyMatrices(V.projectionMatrix,V.matrixWorldInverse),X.setFromProjectionMatrix(ee),ue=this.localClippingEnabled,ne=le.init(this.clippingPlanes,ue),p=Ee.get(A,y.length),p.init(),y.push(p),Y.enabled===!0&&Y.isPresenting===!0){const oe=M.xr.getDepthSensingMesh();oe!==null&&jr(oe,V,-1/0,M.sortObjects)}jr(A,V,0,M.sortObjects),p.finish(),M.sortObjects===!0&&p.sort(G,K),re=Y.enabled===!1||Y.isPresenting===!1||Y.hasDepthSensing()===!1,re&&Ue.addToRenderList(p,A),this.info.render.frame++,ne===!0&&le.beginShadows();const W=u.state.shadowsArray;ye.render(W,A,V),ne===!0&&le.endShadows(),this.info.autoReset===!0&&this.info.reset();const q=p.opaque,H=p.transmissive;if(u.setupLights(),V.isArrayCamera){const oe=V.cameras;if(H.length>0)for(let me=0,Se=oe.length;me<Se;me++){const Te=oe[me];Hs(q,H,A,Te)}re&&Ue.render(A);for(let me=0,Se=oe.length;me<Se;me++){const Te=oe[me];Vs(p,A,Te,Te.viewport)}}else H.length>0&&Hs(q,H,A,V),re&&Ue.render(A),Vs(p,A,V);L!==null&&w===0&&(D.updateMultisampleRenderTarget(L),D.updateRenderTargetMipmap(L)),A.isScene===!0&&A.onAfterRender(M,A,V),rt.resetDefaultState(),x=-1,v=null,S.pop(),S.length>0?(u=S[S.length-1],ne===!0&&le.setGlobalState(M.clippingPlanes,u.state.camera)):u=null,y.pop(),y.length>0?p=y[y.length-1]:p=null};function jr(A,V,W,q){if(A.visible===!1)return;if(A.layers.test(V.layers)){if(A.isGroup)W=A.renderOrder;else if(A.isLOD)A.autoUpdate===!0&&A.update(V);else if(A.isLight)u.pushLight(A),A.castShadow&&u.pushShadow(A);else if(A.isSprite){if(!A.frustumCulled||X.intersectsSprite(A)){q&&de.setFromMatrixPosition(A.matrixWorld).applyMatrix4(ee);const me=J.update(A),Se=A.material;Se.visible&&p.push(A,me,Se,W,de.z,null)}}else if((A.isMesh||A.isLine||A.isPoints)&&(!A.frustumCulled||X.intersectsObject(A))){const me=J.update(A),Se=A.material;if(q&&(A.boundingSphere!==void 0?(A.boundingSphere===null&&A.computeBoundingSphere(),de.copy(A.boundingSphere.center)):(me.boundingSphere===null&&me.computeBoundingSphere(),de.copy(me.boundingSphere.center)),de.applyMatrix4(A.matrixWorld).applyMatrix4(ee)),Array.isArray(Se)){const Te=me.groups;for(let Ne=0,Fe=Te.length;Ne<Fe;Ne++){const Pe=Te[Ne],$e=Se[Pe.materialIndex];$e&&$e.visible&&p.push(A,me,$e,W,de.z,Pe)}}else Se.visible&&p.push(A,me,Se,W,de.z,null)}}const oe=A.children;for(let me=0,Se=oe.length;me<Se;me++)jr(oe[me],V,W,q)}function Vs(A,V,W,q){const H=A.opaque,oe=A.transmissive,me=A.transparent;u.setupLightsView(W),ne===!0&&le.setGlobalState(M.clippingPlanes,W),q&&Me.viewport(R.copy(q)),H.length>0&&Ji(H,V,W),oe.length>0&&Ji(oe,V,W),me.length>0&&Ji(me,V,W),Me.buffers.depth.setTest(!0),Me.buffers.depth.setMask(!0),Me.buffers.color.setMask(!0),Me.setPolygonOffset(!1)}function Hs(A,V,W,q){if((W.isScene===!0?W.overrideMaterial:null)!==null)return;u.state.transmissionRenderTarget[q.id]===void 0&&(u.state.transmissionRenderTarget[q.id]=new Jn(1,1,{generateMipmaps:!0,type:Ce.has("EXT_color_buffer_half_float")||Ce.has("EXT_color_buffer_float")?qi:pn,minFilter:Yn,samples:4,stencilBuffer:a,resolveDepthBuffer:!1,resolveStencilBuffer:!1,colorSpace:Je.workingColorSpace}));const oe=u.state.transmissionRenderTarget[q.id],me=q.viewport||R;oe.setSize(me.z*M.transmissionResolutionScale,me.w*M.transmissionResolutionScale);const Se=M.getRenderTarget();M.setRenderTarget(oe),M.getClearColor(P),F=M.getClearAlpha(),F<1&&M.setClearColor(16777215,.5),M.clear(),re&&Ue.render(W);const Te=M.toneMapping;M.toneMapping=Cn;const Ne=q.viewport;if(q.viewport!==void 0&&(q.viewport=void 0),u.setupLightsView(q),ne===!0&&le.setGlobalState(M.clippingPlanes,q),Ji(A,W,q),D.updateMultisampleRenderTarget(oe),D.updateRenderTargetMipmap(oe),Ce.has("WEBGL_multisampled_render_to_texture")===!1){let Fe=!1;for(let Pe=0,$e=V.length;Pe<$e;Pe++){const Qe=V[Pe],ft=Qe.object,ut=Qe.geometry,Ze=Qe.material,Le=Qe.group;if(Ze.side===mt&&ft.layers.test(q.layers)){const St=Ze.side;Ze.side=Dt,Ze.needsUpdate=!0,Gs(ft,W,q,ut,Ze,Le),Ze.side=St,Ze.needsUpdate=!0,Fe=!0}}Fe===!0&&(D.updateMultisampleRenderTarget(oe),D.updateRenderTargetMipmap(oe))}M.setRenderTarget(Se),M.setClearColor(P,F),Ne!==void 0&&(q.viewport=Ne),M.toneMapping=Te}function Ji(A,V,W){const q=V.isScene===!0?V.overrideMaterial:null;for(let H=0,oe=A.length;H<oe;H++){const me=A[H],Se=me.object,Te=me.geometry,Ne=q===null?me.material:q,Fe=me.group;Se.layers.test(W.layers)&&Gs(Se,V,W,Te,Ne,Fe)}}function Gs(A,V,W,q,H,oe){A.onBeforeRender(M,V,W,q,H,oe),A.modelViewMatrix.multiplyMatrices(W.matrixWorldInverse,A.matrixWorld),A.normalMatrix.getNormalMatrix(A.modelViewMatrix),H.onBeforeRender(M,V,W,q,A,oe),H.transparent===!0&&H.side===mt&&H.forceSinglePass===!1?(H.side=Dt,H.needsUpdate=!0,M.renderBufferDirect(W,V,q,H,A,oe),H.side=Pn,H.needsUpdate=!0,M.renderBufferDirect(W,V,q,H,A,oe),H.side=mt):M.renderBufferDirect(W,V,q,H,A,oe),A.onAfterRender(M,V,W,q,H,oe)}function Qi(A,V,W){V.isScene!==!0&&(V=Z);const q=we.get(A),H=u.state.lights,oe=u.state.shadowsArray,me=H.state.version,Se=Ae.getParameters(A,H.state,oe,V,W),Te=Ae.getProgramCacheKey(Se);let Ne=q.programs;q.environment=A.isMeshStandardMaterial?V.environment:null,q.fog=V.fog,q.envMap=(A.isMeshStandardMaterial?j:E).get(A.envMap||q.environment),q.envMapRotation=q.environment!==null&&A.envMap===null?V.environmentRotation:A.envMapRotation,Ne===void 0&&(A.addEventListener("dispose",Oe),Ne=new Map,q.programs=Ne);let Fe=Ne.get(Te);if(Fe!==void 0){if(q.currentProgram===Fe&&q.lightsStateVersion===me)return Ws(A,Se),Fe}else Se.uniforms=Ae.getUniforms(A),A.onBeforeCompile(Se,M),Fe=Ae.acquireProgram(Se,Te),Ne.set(Te,Fe),q.uniforms=Se.uniforms;const Pe=q.uniforms;return(!A.isShaderMaterial&&!A.isRawShaderMaterial||A.clipping===!0)&&(Pe.clippingPlanes=le.uniform),Ws(A,Se),q.needsLights=Yc(A),q.lightsStateVersion=me,q.needsLights&&(Pe.ambientLightColor.value=H.state.ambient,Pe.lightProbe.value=H.state.probe,Pe.directionalLights.value=H.state.directional,Pe.directionalLightShadows.value=H.state.directionalShadow,Pe.spotLights.value=H.state.spot,Pe.spotLightShadows.value=H.state.spotShadow,Pe.rectAreaLights.value=H.state.rectArea,Pe.ltc_1.value=H.state.rectAreaLTC1,Pe.ltc_2.value=H.state.rectAreaLTC2,Pe.pointLights.value=H.state.point,Pe.pointLightShadows.value=H.state.pointShadow,Pe.hemisphereLights.value=H.state.hemi,Pe.directionalShadowMap.value=H.state.directionalShadowMap,Pe.directionalShadowMatrix.value=H.state.directionalShadowMatrix,Pe.spotShadowMap.value=H.state.spotShadowMap,Pe.spotLightMatrix.value=H.state.spotLightMatrix,Pe.spotLightMap.value=H.state.spotLightMap,Pe.pointShadowMap.value=H.state.pointShadowMap,Pe.pointShadowMatrix.value=H.state.pointShadowMatrix),q.currentProgram=Fe,q.uniformsList=null,Fe}function js(A){if(A.uniformsList===null){const V=A.currentProgram.getUniforms();A.uniformsList=Ir.seqWithValue(V.seq,A.uniforms)}return A.uniformsList}function Ws(A,V){const W=we.get(A);W.outputColorSpace=V.outputColorSpace,W.batching=V.batching,W.batchingColor=V.batchingColor,W.instancing=V.instancing,W.instancingColor=V.instancingColor,W.instancingMorph=V.instancingMorph,W.skinning=V.skinning,W.morphTargets=V.morphTargets,W.morphNormals=V.morphNormals,W.morphColors=V.morphColors,W.morphTargetsCount=V.morphTargetsCount,W.numClippingPlanes=V.numClippingPlanes,W.numIntersection=V.numClipIntersection,W.vertexAlphas=V.vertexAlphas,W.vertexTangents=V.vertexTangents,W.toneMapping=V.toneMapping}function Xc(A,V,W,q,H){V.isScene!==!0&&(V=Z),D.resetTextureUnits();const oe=V.fog,me=q.isMeshStandardMaterial?V.environment:null,Se=L===null?M.outputColorSpace:L.isXRRenderTarget===!0?L.texture.colorSpace:wi,Te=(q.isMeshStandardMaterial?j:E).get(q.envMap||me),Ne=q.vertexColors===!0&&!!W.attributes.color&&W.attributes.color.itemSize===4,Fe=!!W.attributes.tangent&&(!!q.normalMap||q.anisotropy>0),Pe=!!W.morphAttributes.position,$e=!!W.morphAttributes.normal,Qe=!!W.morphAttributes.color;let ft=Cn;q.toneMapped&&(L===null||L.isXRRenderTarget===!0)&&(ft=M.toneMapping);const ut=W.morphAttributes.position||W.morphAttributes.normal||W.morphAttributes.color,Ze=ut!==void 0?ut.length:0,Le=we.get(q),St=u.state.lights;if(ne===!0&&(ue===!0||A!==v)){const At=A===v&&q.id===x;le.setState(q,A,At)}let et=!1;q.version===Le.__version?(Le.needsLights&&Le.lightsStateVersion!==St.state.version||Le.outputColorSpace!==Se||H.isBatchedMesh&&Le.batching===!1||!H.isBatchedMesh&&Le.batching===!0||H.isBatchedMesh&&Le.batchingColor===!0&&H.colorTexture===null||H.isBatchedMesh&&Le.batchingColor===!1&&H.colorTexture!==null||H.isInstancedMesh&&Le.instancing===!1||!H.isInstancedMesh&&Le.instancing===!0||H.isSkinnedMesh&&Le.skinning===!1||!H.isSkinnedMesh&&Le.skinning===!0||H.isInstancedMesh&&Le.instancingColor===!0&&H.instanceColor===null||H.isInstancedMesh&&Le.instancingColor===!1&&H.instanceColor!==null||H.isInstancedMesh&&Le.instancingMorph===!0&&H.morphTexture===null||H.isInstancedMesh&&Le.instancingMorph===!1&&H.morphTexture!==null||Le.envMap!==Te||q.fog===!0&&Le.fog!==oe||Le.numClippingPlanes!==void 0&&(Le.numClippingPlanes!==le.numPlanes||Le.numIntersection!==le.numIntersection)||Le.vertexAlphas!==Ne||Le.vertexTangents!==Fe||Le.morphTargets!==Pe||Le.morphNormals!==$e||Le.morphColors!==Qe||Le.toneMapping!==ft||Le.morphTargetsCount!==Ze)&&(et=!0):(et=!0,Le.__version=q.version);let Gt=Le.currentProgram;et===!0&&(Gt=Qi(q,V,H));let Qn=!1,It=!1,Ui=!1;const st=Gt.getUniforms(),Ft=Le.uniforms;if(Me.useProgram(Gt.program)&&(Qn=!0,It=!0,Ui=!0),q.id!==x&&(x=q.id,It=!0),Qn||v!==A){Me.buffers.depth.getReversed()?(se.copy(A.projectionMatrix),Wl(se),Xl(se),st.setValue(I,"projectionMatrix",se)):st.setValue(I,"projectionMatrix",A.projectionMatrix),st.setValue(I,"viewMatrix",A.matrixWorldInverse);const Ct=st.map.cameraPosition;Ct!==void 0&&Ct.setValue(I,_e.setFromMatrixPosition(A.matrixWorld)),Re.logarithmicDepthBuffer&&st.setValue(I,"logDepthBufFC",2/(Math.log(A.far+1)/Math.LN2)),(q.isMeshPhongMaterial||q.isMeshToonMaterial||q.isMeshLambertMaterial||q.isMeshBasicMaterial||q.isMeshStandardMaterial||q.isShaderMaterial)&&st.setValue(I,"isOrthographic",A.isOrthographicCamera===!0),v!==A&&(v=A,It=!0,Ui=!0)}if(H.isSkinnedMesh){st.setOptional(I,H,"bindMatrix"),st.setOptional(I,H,"bindMatrixInverse");const At=H.skeleton;At&&(At.boneTexture===null&&At.computeBoneTexture(),st.setValue(I,"boneTexture",At.boneTexture,D))}H.isBatchedMesh&&(st.setOptional(I,H,"batchingTexture"),st.setValue(I,"batchingTexture",H._matricesTexture,D),st.setOptional(I,H,"batchingIdTexture"),st.setValue(I,"batchingIdTexture",H._indirectTexture,D),st.setOptional(I,H,"batchingColorTexture"),H._colorsTexture!==null&&st.setValue(I,"batchingColorTexture",H._colorsTexture,D));const kt=W.morphAttributes;if((kt.position!==void 0||kt.normal!==void 0||kt.color!==void 0)&&ze.update(H,W,Gt),(It||Le.receiveShadow!==H.receiveShadow)&&(Le.receiveShadow=H.receiveShadow,st.setValue(I,"receiveShadow",H.receiveShadow)),q.isMeshGouraudMaterial&&q.envMap!==null&&(Ft.envMap.value=Te,Ft.flipEnvMap.value=Te.isCubeTexture&&Te.isRenderTargetTexture===!1?-1:1),q.isMeshStandardMaterial&&q.envMap===null&&V.environment!==null&&(Ft.envMapIntensity.value=V.environmentIntensity),It&&(st.setValue(I,"toneMappingExposure",M.toneMappingExposure),Le.needsLights&&qc(Ft,Ui),oe&&q.fog===!0&&ge.refreshFogUniforms(Ft,oe),ge.refreshMaterialUniforms(Ft,q,z,O,u.state.transmissionRenderTarget[A.id]),Ir.upload(I,js(Le),Ft,D)),q.isShaderMaterial&&q.uniformsNeedUpdate===!0&&(Ir.upload(I,js(Le),Ft,D),q.uniformsNeedUpdate=!1),q.isSpriteMaterial&&st.setValue(I,"center",H.center),st.setValue(I,"modelViewMatrix",H.modelViewMatrix),st.setValue(I,"normalMatrix",H.normalMatrix),st.setValue(I,"modelMatrix",H.matrixWorld),q.isShaderMaterial||q.isRawShaderMaterial){const At=q.uniformsGroups;for(let Ct=0,Wr=At.length;Ct<Wr;Ct++){const In=At[Ct];B.update(In,Gt),B.bind(In,Gt)}}return Gt}function qc(A,V){A.ambientLightColor.needsUpdate=V,A.lightProbe.needsUpdate=V,A.directionalLights.needsUpdate=V,A.directionalLightShadows.needsUpdate=V,A.pointLights.needsUpdate=V,A.pointLightShadows.needsUpdate=V,A.spotLights.needsUpdate=V,A.spotLightShadows.needsUpdate=V,A.rectAreaLights.needsUpdate=V,A.hemisphereLights.needsUpdate=V}function Yc(A){return A.isMeshLambertMaterial||A.isMeshToonMaterial||A.isMeshPhongMaterial||A.isMeshStandardMaterial||A.isShadowMaterial||A.isShaderMaterial&&A.lights===!0}this.getActiveCubeFace=function(){return b},this.getActiveMipmapLevel=function(){return w},this.getRenderTarget=function(){return L},this.setRenderTargetTextures=function(A,V,W){we.get(A.texture).__webglTexture=V,we.get(A.depthTexture).__webglTexture=W;const q=we.get(A);q.__hasExternalTextures=!0,q.__autoAllocateDepthBuffer=W===void 0,q.__autoAllocateDepthBuffer||Ce.has("WEBGL_multisampled_render_to_texture")===!0&&(console.warn("THREE.WebGLRenderer: Render-to-texture extension was disabled because an external texture was provided"),q.__useRenderToTexture=!1)},this.setRenderTargetFramebuffer=function(A,V){const W=we.get(A);W.__webglFramebuffer=V,W.__useDefaultFramebuffer=V===void 0};const Kc=I.createFramebuffer();this.setRenderTarget=function(A,V=0,W=0){L=A,b=V,w=W;let q=!0,H=null,oe=!1,me=!1;if(A){const Te=we.get(A);if(Te.__useDefaultFramebuffer!==void 0)Me.bindFramebuffer(I.FRAMEBUFFER,null),q=!1;else if(Te.__webglFramebuffer===void 0)D.setupRenderTarget(A);else if(Te.__hasExternalTextures)D.rebindTextures(A,we.get(A.texture).__webglTexture,we.get(A.depthTexture).__webglTexture);else if(A.depthBuffer){const Pe=A.depthTexture;if(Te.__boundDepthTexture!==Pe){if(Pe!==null&&we.has(Pe)&&(A.width!==Pe.image.width||A.height!==Pe.image.height))throw new Error("WebGLRenderTarget: Attached DepthTexture is initialized to the incorrect size.");D.setupDepthRenderbuffer(A)}}const Ne=A.texture;(Ne.isData3DTexture||Ne.isDataArrayTexture||Ne.isCompressedArrayTexture)&&(me=!0);const Fe=we.get(A).__webglFramebuffer;A.isWebGLCubeRenderTarget?(Array.isArray(Fe[V])?H=Fe[V][W]:H=Fe[V],oe=!0):A.samples>0&&D.useMultisampledRTT(A)===!1?H=we.get(A).__webglMultisampledFramebuffer:Array.isArray(Fe)?H=Fe[W]:H=Fe,R.copy(A.viewport),U.copy(A.scissor),C=A.scissorTest}else R.copy($).multiplyScalar(z).floor(),U.copy(fe).multiplyScalar(z).floor(),C=De;if(W!==0&&(H=Kc),Me.bindFramebuffer(I.FRAMEBUFFER,H)&&q&&Me.drawBuffers(A,H),Me.viewport(R),Me.scissor(U),Me.setScissorTest(C),oe){const Te=we.get(A.texture);I.framebufferTexture2D(I.FRAMEBUFFER,I.COLOR_ATTACHMENT0,I.TEXTURE_CUBE_MAP_POSITIVE_X+V,Te.__webglTexture,W)}else if(me){const Te=we.get(A.texture),Ne=V;I.framebufferTextureLayer(I.FRAMEBUFFER,I.COLOR_ATTACHMENT0,Te.__webglTexture,W,Ne)}else if(A!==null&&W!==0){const Te=we.get(A.texture);I.framebufferTexture2D(I.FRAMEBUFFER,I.COLOR_ATTACHMENT0,I.TEXTURE_2D,Te.__webglTexture,W)}x=-1},this.readRenderTargetPixels=function(A,V,W,q,H,oe,me){if(!(A&&A.isWebGLRenderTarget)){console.error("THREE.WebGLRenderer.readRenderTargetPixels: renderTarget is not THREE.WebGLRenderTarget.");return}let Se=we.get(A).__webglFramebuffer;if(A.isWebGLCubeRenderTarget&&me!==void 0&&(Se=Se[me]),Se){Me.bindFramebuffer(I.FRAMEBUFFER,Se);try{const Te=A.texture,Ne=Te.format,Fe=Te.type;if(!Re.textureFormatReadable(Ne)){console.error("THREE.WebGLRenderer.readRenderTargetPixels: renderTarget is not in RGBA or implementation defined format.");return}if(!Re.textureTypeReadable(Fe)){console.error("THREE.WebGLRenderer.readRenderTargetPixels: renderTarget is not in UnsignedByteType or implementation defined type.");return}V>=0&&V<=A.width-q&&W>=0&&W<=A.height-H&&I.readPixels(V,W,q,H,Ve.convert(Ne),Ve.convert(Fe),oe)}finally{const Te=L!==null?we.get(L).__webglFramebuffer:null;Me.bindFramebuffer(I.FRAMEBUFFER,Te)}}},this.readRenderTargetPixelsAsync=async function(A,V,W,q,H,oe,me){if(!(A&&A.isWebGLRenderTarget))throw new Error("THREE.WebGLRenderer.readRenderTargetPixels: renderTarget is not THREE.WebGLRenderTarget.");let Se=we.get(A).__webglFramebuffer;if(A.isWebGLCubeRenderTarget&&me!==void 0&&(Se=Se[me]),Se){const Te=A.texture,Ne=Te.format,Fe=Te.type;if(!Re.textureFormatReadable(Ne))throw new Error("THREE.WebGLRenderer.readRenderTargetPixelsAsync: renderTarget is not in RGBA or implementation defined format.");if(!Re.textureTypeReadable(Fe))throw new Error("THREE.WebGLRenderer.readRenderTargetPixelsAsync: renderTarget is not in UnsignedByteType or implementation defined type.");if(V>=0&&V<=A.width-q&&W>=0&&W<=A.height-H){Me.bindFramebuffer(I.FRAMEBUFFER,Se);const Pe=I.createBuffer();I.bindBuffer(I.PIXEL_PACK_BUFFER,Pe),I.bufferData(I.PIXEL_PACK_BUFFER,oe.byteLength,I.STREAM_READ),I.readPixels(V,W,q,H,Ve.convert(Ne),Ve.convert(Fe),0);const $e=L!==null?we.get(L).__webglFramebuffer:null;Me.bindFramebuffer(I.FRAMEBUFFER,$e);const Qe=I.fenceSync(I.SYNC_GPU_COMMANDS_COMPLETE,0);return I.flush(),await jl(I,Qe,4),I.bindBuffer(I.PIXEL_PACK_BUFFER,Pe),I.getBufferSubData(I.PIXEL_PACK_BUFFER,0,oe),I.deleteBuffer(Pe),I.deleteSync(Qe),oe}else throw new Error("THREE.WebGLRenderer.readRenderTargetPixelsAsync: requested read bounds are out of range.")}},this.copyFramebufferToTexture=function(A,V=null,W=0){A.isTexture!==!0&&(Bn("WebGLRenderer: copyFramebufferToTexture function signature has changed."),V=arguments[0]||null,A=arguments[1]);const q=Math.pow(2,-W),H=Math.floor(A.image.width*q),oe=Math.floor(A.image.height*q),me=V!==null?V.x:0,Se=V!==null?V.y:0;D.setTexture2D(A,0),I.copyTexSubImage2D(I.TEXTURE_2D,W,0,0,me,Se,H,oe),Me.unbindTexture()};const $c=I.createFramebuffer(),Zc=I.createFramebuffer();this.copyTextureToTexture=function(A,V,W=null,q=null,H=0,oe=null){A.isTexture!==!0&&(Bn("WebGLRenderer: copyTextureToTexture function signature has changed."),q=arguments[0]||null,A=arguments[1],V=arguments[2],oe=arguments[3]||0,W=null),oe===null&&(H!==0?(Bn("WebGLRenderer: copyTextureToTexture function signature has changed to support src and dst mipmap levels."),oe=H,H=0):oe=0);let me,Se,Te,Ne,Fe,Pe,$e,Qe,ft;const ut=A.isCompressedTexture?A.mipmaps[oe]:A.image;if(W!==null)me=W.max.x-W.min.x,Se=W.max.y-W.min.y,Te=W.isBox3?W.max.z-W.min.z:1,Ne=W.min.x,Fe=W.min.y,Pe=W.isBox3?W.min.z:0;else{const kt=Math.pow(2,-H);me=Math.floor(ut.width*kt),Se=Math.floor(ut.height*kt),A.isDataArrayTexture?Te=ut.depth:A.isData3DTexture?Te=Math.floor(ut.depth*kt):Te=1,Ne=0,Fe=0,Pe=0}q!==null?($e=q.x,Qe=q.y,ft=q.z):($e=0,Qe=0,ft=0);const Ze=Ve.convert(V.format),Le=Ve.convert(V.type);let St;V.isData3DTexture?(D.setTexture3D(V,0),St=I.TEXTURE_3D):V.isDataArrayTexture||V.isCompressedArrayTexture?(D.setTexture2DArray(V,0),St=I.TEXTURE_2D_ARRAY):(D.setTexture2D(V,0),St=I.TEXTURE_2D),I.pixelStorei(I.UNPACK_FLIP_Y_WEBGL,V.flipY),I.pixelStorei(I.UNPACK_PREMULTIPLY_ALPHA_WEBGL,V.premultiplyAlpha),I.pixelStorei(I.UNPACK_ALIGNMENT,V.unpackAlignment);const et=I.getParameter(I.UNPACK_ROW_LENGTH),Gt=I.getParameter(I.UNPACK_IMAGE_HEIGHT),Qn=I.getParameter(I.UNPACK_SKIP_PIXELS),It=I.getParameter(I.UNPACK_SKIP_ROWS),Ui=I.getParameter(I.UNPACK_SKIP_IMAGES);I.pixelStorei(I.UNPACK_ROW_LENGTH,ut.width),I.pixelStorei(I.UNPACK_IMAGE_HEIGHT,ut.height),I.pixelStorei(I.UNPACK_SKIP_PIXELS,Ne),I.pixelStorei(I.UNPACK_SKIP_ROWS,Fe),I.pixelStorei(I.UNPACK_SKIP_IMAGES,Pe);const st=A.isDataArrayTexture||A.isData3DTexture,Ft=V.isDataArrayTexture||V.isData3DTexture;if(A.isDepthTexture){const kt=we.get(A),At=we.get(V),Ct=we.get(kt.__renderTarget),Wr=we.get(At.__renderTarget);Me.bindFramebuffer(I.READ_FRAMEBUFFER,Ct.__webglFramebuffer),Me.bindFramebuffer(I.DRAW_FRAMEBUFFER,Wr.__webglFramebuffer);for(let In=0;In<Te;In++)st&&(I.framebufferTextureLayer(I.READ_FRAMEBUFFER,I.COLOR_ATTACHMENT0,we.get(A).__webglTexture,H,Pe+In),I.framebufferTextureLayer(I.DRAW_FRAMEBUFFER,I.COLOR_ATTACHMENT0,we.get(V).__webglTexture,oe,ft+In)),I.blitFramebuffer(Ne,Fe,me,Se,$e,Qe,me,Se,I.DEPTH_BUFFER_BIT,I.NEAREST);Me.bindFramebuffer(I.READ_FRAMEBUFFER,null),Me.bindFramebuffer(I.DRAW_FRAMEBUFFER,null)}else if(H!==0||A.isRenderTargetTexture||we.has(A)){const kt=we.get(A),At=we.get(V);Me.bindFramebuffer(I.READ_FRAMEBUFFER,$c),Me.bindFramebuffer(I.DRAW_FRAMEBUFFER,Zc);for(let Ct=0;Ct<Te;Ct++)st?I.framebufferTextureLayer(I.READ_FRAMEBUFFER,I.COLOR_ATTACHMENT0,kt.__webglTexture,H,Pe+Ct):I.framebufferTexture2D(I.READ_FRAMEBUFFER,I.COLOR_ATTACHMENT0,I.TEXTURE_2D,kt.__webglTexture,H),Ft?I.framebufferTextureLayer(I.DRAW_FRAMEBUFFER,I.COLOR_ATTACHMENT0,At.__webglTexture,oe,ft+Ct):I.framebufferTexture2D(I.DRAW_FRAMEBUFFER,I.COLOR_ATTACHMENT0,I.TEXTURE_2D,At.__webglTexture,oe),H!==0?I.blitFramebuffer(Ne,Fe,me,Se,$e,Qe,me,Se,I.COLOR_BUFFER_BIT,I.NEAREST):Ft?I.copyTexSubImage3D(St,oe,$e,Qe,ft+Ct,Ne,Fe,me,Se):I.copyTexSubImage2D(St,oe,$e,Qe,Ne,Fe,me,Se);Me.bindFramebuffer(I.READ_FRAMEBUFFER,null),Me.bindFramebuffer(I.DRAW_FRAMEBUFFER,null)}else Ft?A.isDataTexture||A.isData3DTexture?I.texSubImage3D(St,oe,$e,Qe,ft,me,Se,Te,Ze,Le,ut.data):V.isCompressedArrayTexture?I.compressedTexSubImage3D(St,oe,$e,Qe,ft,me,Se,Te,Ze,ut.data):I.texSubImage3D(St,oe,$e,Qe,ft,me,Se,Te,Ze,Le,ut):A.isDataTexture?I.texSubImage2D(I.TEXTURE_2D,oe,$e,Qe,me,Se,Ze,Le,ut.data):A.isCompressedTexture?I.compressedTexSubImage2D(I.TEXTURE_2D,oe,$e,Qe,ut.width,ut.height,Ze,ut.data):I.texSubImage2D(I.TEXTURE_2D,oe,$e,Qe,me,Se,Ze,Le,ut);I.pixelStorei(I.UNPACK_ROW_LENGTH,et),I.pixelStorei(I.UNPACK_IMAGE_HEIGHT,Gt),I.pixelStorei(I.UNPACK_SKIP_PIXELS,Qn),I.pixelStorei(I.UNPACK_SKIP_ROWS,It),I.pixelStorei(I.UNPACK_SKIP_IMAGES,Ui),oe===0&&V.generateMipmaps&&I.generateMipmap(St),Me.unbindTexture()},this.copyTextureToTexture3D=function(A,V,W=null,q=null,H=0){return A.isTexture!==!0&&(Bn("WebGLRenderer: copyTextureToTexture3D function signature has changed."),W=arguments[0]||null,q=arguments[1]||null,A=arguments[2],V=arguments[3],H=arguments[4]||0),Bn('WebGLRenderer: copyTextureToTexture3D function has been deprecated. Use "copyTextureToTexture" instead.'),this.copyTextureToTexture(A,V,W,q,H)},this.initRenderTarget=function(A){we.get(A).__webglFramebuffer===void 0&&D.setupRenderTarget(A)},this.initTexture=function(A){A.isCubeTexture?D.setTextureCube(A,0):A.isData3DTexture?D.setTexture3D(A,0):A.isDataArrayTexture||A.isCompressedArrayTexture?D.setTexture2DArray(A,0):D.setTexture2D(A,0),Me.unbindTexture()},this.resetState=function(){b=0,w=0,L=null,Me.reset(),rt.reset()},typeof __THREE_DEVTOOLS__<"u"&&__THREE_DEVTOOLS__.dispatchEvent(new CustomEvent("observe",{detail:this}))}get coordinateSystem(){return dn}get outputColorSpace(){return this._outputColorSpace}set outputColorSpace(e){this._outputColorSpace=e;const t=this.getContext();t.drawingBufferColorspace=Je._getDrawingBufferColorSpace(e),t.unpackColorSpace=Je._getUnpackColorSpace()}}const En=1e-6,_i=5e-5,Ta=1e-7;function xs(n,e){return n[0]*e[0]+n[1]*e[1]+n[2]*e[2]}function Ms(n,e){return[n[0]-e[0],n[1]-e[1],n[2]-e[2]]}function Ss(n,e){return[n[1]*e[2]-n[2]*e[1],n[2]*e[0]-n[0]*e[2],n[0]*e[1]-n[1]*e[0]]}function dm(n){const e=Math.hypot(n[0],n[1],n[2]);return e<1e-12?null:[n[0]/e,n[1]/e,n[2]/e]}function Ur(n,e){const t=n[0]-e[0],i=n[1]-e[1],r=n[2]-e[2];return t*t+i*i+r*r}function Aa(n){if(n.length<3)return 0;const e=n[0];let t=0,i=0,r=0;for(let a=1;a+1<n.length;a++){const s=Ms(n[a],e),o=Ms(n[a+1],e),c=Ss(s,o);t+=c[0],i+=c[1],r+=c[2]}return .5*Math.hypot(t,i,r)}function hm(n,e){const t=[],i=_i*_i;for(const f of n)t.some(m=>Ur(f,m)<=i)||t.push(f);if(t.length<3)return[];let r=0,a=0,s=0;for(const f of t)r+=f[0],a+=f[1],s+=f[2];r/=t.length,a/=t.length,s/=t.length;const o=[r,a,s],c=Math.abs(e[0])<.8?[1,0,0]:[0,1,0],l=dm(Ss(c,e));if(!l)return[];const d=Ss(e,l),h=t.map(f=>{const m=Ms(f,o),g=xs(m,l),_=xs(m,d);return{tacka:f,ugao:Math.atan2(_,g)}});return h.sort((f,m)=>f.ugao-m.ugao),h.map(f=>f.tacka)}function fm(n){return[{normala:[1,0,0],grupaId:"__okvir__",oznaka:"",temena:[[n,-n,-n],[n,n,-n],[n,n,n],[n,-n,n]]},{normala:[-1,0,0],grupaId:"__okvir__",oznaka:"",temena:[[-n,-n,n],[-n,n,n],[-n,n,-n],[-n,-n,-n]]},{normala:[0,1,0],grupaId:"__okvir__",oznaka:"",temena:[[-n,n,-n],[-n,n,n],[n,n,n],[n,n,-n]]},{normala:[0,-1,0],grupaId:"__okvir__",oznaka:"",temena:[[-n,-n,n],[-n,-n,-n],[n,-n,-n],[n,-n,n]]},{normala:[0,0,1],grupaId:"__okvir__",oznaka:"",temena:[[-n,-n,n],[n,-n,n],[n,n,n],[-n,n,n]]},{normala:[0,0,-1],grupaId:"__okvir__",oznaka:"",temena:[[n,-n,-n],[-n,-n,-n],[-n,n,-n],[n,n,-n]]}]}function Wi(n){if(n.length===0)return{temena:[],pljosni:[]};let e=1;const t=[];for(let c=0;c<n.length;c++){const l=n[c],d=Math.hypot(l.normala[0],l.normala[1],l.normala[2]);if(d<1e-12)continue;const h=[l.normala[0]/d,l.normala[1]/d,l.normala[2]/d],f=l.d;e=Math.max(e,Math.abs(f)),t.push({normala:h,d:f,grupaId:l.grupaId??`forma-${c}`,oznaka:l.oznaka??""})}let i=fm(Math.max(12,e*6));for(const c of t){const l=[],d=[];for(const f of i){const m=f.temena.length;if(m<3)continue;const g=f.temena.map(y=>xs(c.normala,y)-c.d),_=[];for(let y=0;y<m;y++){const S=(y+1)%m,M=f.temena[y],T=f.temena[S],b=g[y],w=g[S],L=b<=En,x=w<=En;if(Math.abs(b)<=En*4&&d.push(M),L&&_.push(M),b<-En&&w>En||b>En&&w<-En){const v=b/(b-w),R=[M[0]+(T[0]-M[0])*v,M[1]+(T[1]-M[1])*v,M[2]+(T[2]-M[2])*v];_.push(R),d.push(R)}else!L&&x&&Math.abs(w)<=En&&d.push(T)}const p=[],u=_i*_i;for(const y of _)(p.length===0||Ur(y,p[p.length-1])>u)&&p.push(y);p.length>1&&Ur(p[0],p[p.length-1])<=u&&p.pop(),p.length>=3&&Aa(p)>Ta&&l.push({temena:p,normala:f.normala,grupaId:f.grupaId,oznaka:f.oznaka})}const h=hm(d,c.normala);if(h.length>=3&&Aa(h)>Ta&&l.push({temena:h,normala:c.normala,grupaId:c.grupaId,oznaka:c.oznaka}),i=l,i.length===0)break}const r=[],a=[],s=_i*_i;function o(c){for(let l=0;l<r.length;l++)if(Ur(r[l],c)<=s)return l;return r.push([Math.abs(c[0])<1e-10?0:c[0],Math.abs(c[1])<1e-10?0:c[1],Math.abs(c[2])<1e-10?0:c[2]]),r.length-1}for(const c of i){if(c.grupaId==="__okvir__")continue;const l=Aa(c.temena);if(l<=Ta)continue;const d=c.temena.map(p=>o(p)),h=[];for(const p of d)(h.length===0||h[h.length-1]!==p)&&h.push(p);if(h.length>1&&h[0]===h[h.length-1]&&h.pop(),h.length<3)continue;let f=0,m=0,g=0;for(const p of h){const u=r[p];f+=u[0],m+=u[1],g+=u[2]}const _=h.length;a.push({indeksiTemena:h,normala:c.normala,centar:[f/_,m/_,g/_],povrsina:l,grupaId:c.grupaId,oznaka:c.oznaka})}return{temena:r,pljosni:a}}function Xi(n){const e=[];for(const d of n.pljosni)e.includes(d.grupaId)||e.push(d.grupaId);const t=[],i=[],r=[],a=[];for(let d=0;d<e.length;d++){const h=e[d],f=t.length/3;for(let g=0;g<n.pljosni.length;g++){const _=n.pljosni[g];if(_.grupaId!==h)continue;const p=_.indeksiTemena;if(p.length<3)continue;const u=n.temena[p[0]],[y,S,M]=_.normala;for(let T=1;T+1<p.length;T++){const b=n.temena[p[T]],w=n.temena[p[T+1]];t.push(u[0],u[1],u[2],b[0],b[1],b[2],w[0],w[1],w[2]),i.push(y,S,M,y,S,M,y,S,M),r.push(g)}}const m=t.length/3;m>f&&a.push({pocetak:f,broj:m-f,indeksMaterijala:d})}const s=new Ye;s.setAttribute("position",new Ge(t,3)),s.setAttribute("normal",new Ge(i,3));for(const d of a)s.addGroup(d.pocetak,d.broj,d.indeksMaterijala);const o=new Set,c=[];for(const d of n.pljosni){const h=d.indeksiTemena;for(let f=0;f<h.length;f++){const m=h[f],g=h[(f+1)%h.length],_=m<g?`${m}-${g}`:`${g}-${m}`;if(o.has(_))continue;o.add(_);const p=n.temena[m],u=n.temena[g];c.push(p[0],p[1],p[2],u[0],u[1],u[2])}}const l=new Ye;return l.setAttribute("position",new Ge(c,3)),{geometrijaMreze:s,geometrijaIvica:l,mapaTrougaoUPljosan:r,redosledGrupa:e}}function pi(n,e,t){return Math.max(e,Math.min(t,n))}class pm{stanje;pocetno;minUdaljenost;maksUdaljenost;opcije;vuceMisem=!1;prethodniX=0;prethodniY=0;dodirAktiviran=!1;prethodniDodirX=0;prethodniDodirY=0;prethodniRazmakPrstiju=0;pocetakDodiraX=0;pocetakDodiraY=0;dodirPomeren=!1;cistaci=[];constructor(e){this.opcije=e,this.pocetno={...e.pocetno},this.stanje={...e.pocetno},this.minUdaljenost=e.minUdaljenost??2,this.maksUdaljenost=e.maksUdaljenost??24,this.poveziDogadjaje()}trenutnoStanje(){return{...this.stanje}}rotirajAzimut(e){this.stanje.theta+=e,this.opcije.naPromenu(this.trenutnoStanje())}rotirajElevaciju(e){this.stanje.phi=pi(this.stanje.phi+e,.15,Math.PI-.15),this.opcije.naPromenu(this.trenutnoStanje())}zumiraj(e){this.stanje.udaljenost=pi(this.stanje.udaljenost*e,this.minUdaljenost,this.maksUdaljenost),this.opcije.naPromenu(this.trenutnoStanje())}resetuj(){this.stanje={...this.pocetno},this.opcije.naPromenu(this.trenutnoStanje())}postaviAktivacijuDodira(e){this.dodirAktiviran=e,this.opcije.platno.classList.toggle("udzbenik-scena-platno--dodir-aktivan",e),this.opcije.dugmeDodira.hidden=!e,this.opcije.priPromeniAktivacijeDodira?.(e)}poveziDogadjaje(){const{bina:e,platno:t,dugmeDodira:i}=this.opcije,r=g=>{if(g.pointerType!=="touch"&&g.button===0){this.vuceMisem=!0,this.prethodniX=g.clientX,this.prethodniY=g.clientY;try{t.setPointerCapture(g.pointerId)}catch{}}},a=g=>{if(g.pointerType==="touch"||!this.vuceMisem)return;const _=g.clientX-this.prethodniX,p=g.clientY-this.prethodniY;this.prethodniX=g.clientX,this.prethodniY=g.clientY,this.stanje.theta-=_*.008,this.stanje.phi=pi(this.stanje.phi-p*.008,.15,Math.PI-.15),this.opcije.naPromenu(this.trenutnoStanje())},s=g=>{if(g.pointerType!=="touch"){this.vuceMisem=!1;try{t.hasPointerCapture(g.pointerId)&&t.releasePointerCapture(g.pointerId)}catch{}}},o=g=>{if(!(document.activeElement===e||e.contains(document.activeElement))&&!g.ctrlKey&&!g.metaKey)return;g.preventDefault();const p=g.deltaY>0?1.09:.92;this.zumiraj(p)},c=g=>{if(g.touches.length===2){const _=g.touches[0],p=g.touches[1];this.prethodniDodirX=(_.clientX+p.clientX)/2,this.prethodniDodirY=(_.clientY+p.clientY)/2,this.prethodniRazmakPrstiju=Math.hypot(p.clientX-_.clientX,p.clientY-_.clientY)}else if(g.touches.length===1){const _=g.touches[0];this.pocetakDodiraX=_.clientX,this.pocetakDodiraY=_.clientY,this.prethodniDodirX=_.clientX,this.prethodniDodirY=_.clientY,this.dodirPomeren=!1}},l=g=>{if(g.touches.length===2){g.preventDefault();const _=g.touches[0],p=g.touches[1],u=(_.clientX+p.clientX)/2,y=(_.clientY+p.clientY)/2,S=Math.hypot(p.clientX-_.clientX,p.clientY-_.clientY),M=u-this.prethodniDodirX,T=y-this.prethodniDodirY;if(this.prethodniDodirX=u,this.prethodniDodirY=y,this.stanje.theta-=M*.008,this.stanje.phi=pi(this.stanje.phi-T*.008,.15,Math.PI-.15),this.prethodniRazmakPrstiju>8&&S>8){const b=this.prethodniRazmakPrstiju/S;this.stanje.udaljenost=pi(this.stanje.udaljenost*b,this.minUdaljenost,this.maksUdaljenost)}this.prethodniRazmakPrstiju=S,this.dodirPomeren=!0,this.opcije.naPromenu(this.trenutnoStanje())}else if(g.touches.length===1){const _=g.touches[0];if(Math.hypot(_.clientX-this.pocetakDodiraX,_.clientY-this.pocetakDodiraY)>8&&(this.dodirPomeren=!0),this.dodirAktiviran){g.preventDefault();const p=_.clientX-this.prethodniDodirX,u=_.clientY-this.prethodniDodirY;this.prethodniDodirX=_.clientX,this.prethodniDodirY=_.clientY,this.stanje.theta-=p*.009,this.stanje.phi=pi(this.stanje.phi-u*.009,.15,Math.PI-.15),this.opcije.naPromenu(this.trenutnoStanje())}}},d=g=>{g.touches.length===0&&!this.dodirPomeren&&g.changedTouches.length===1&&this.postaviAktivacijuDodira(!this.dodirAktiviran)},h=()=>{this.postaviAktivacijuDodira(!1)},f=g=>{this.dodirAktiviran&&g.target instanceof Node&&!e.contains(g.target)&&this.postaviAktivacijuDodira(!1)},m=g=>{if(!(g.target instanceof HTMLElement&&g.target!==e&&(g.target.tagName==="BUTTON"||g.target.tagName==="INPUT")))switch(g.key){case"ArrowLeft":g.preventDefault(),this.rotirajAzimut(-.12);break;case"ArrowRight":g.preventDefault(),this.rotirajAzimut(.12);break;case"ArrowUp":g.preventDefault(),this.rotirajElevaciju(-.12);break;case"ArrowDown":g.preventDefault(),this.rotirajElevaciju(.12);break;case"+":case"=":g.preventDefault(),this.zumiraj(.88);break;case"-":case"_":g.preventDefault(),this.zumiraj(1.14);break;case"r":case"R":case"р":case"Р":g.preventDefault(),this.opcije.naReset();break;case" ":g.preventDefault(),this.opcije.naPrekidacPauze();break;case"Escape":this.dodirAktiviran&&(g.preventDefault(),this.postaviAktivacijuDodira(!1));break}};t.addEventListener("pointerdown",r),t.addEventListener("pointermove",a),t.addEventListener("pointerup",s),t.addEventListener("pointercancel",s),t.addEventListener("wheel",o,{passive:!1}),t.addEventListener("touchstart",c,{passive:!0}),t.addEventListener("touchmove",l,{passive:!1}),t.addEventListener("touchend",d),i.addEventListener("click",h),document.addEventListener("touchstart",f,{passive:!0}),e.addEventListener("keydown",m),this.cistaci.push(()=>{t.removeEventListener("pointerdown",r),t.removeEventListener("pointermove",a),t.removeEventListener("pointerup",s),t.removeEventListener("pointercancel",s),t.removeEventListener("wheel",o),t.removeEventListener("touchstart",c),t.removeEventListener("touchmove",l),t.removeEventListener("touchend",d),i.removeEventListener("click",h),document.removeEventListener("touchstart",f),e.removeEventListener("keydown",m)})}raspolazi(){for(const e of this.cistaci)e();this.cistaci.length=0}}let ln=null,vi=null,Kn=0,$n=0;function mm(){if(ln)return ln;const n=document.createElement("canvas"),e=n.getContext("webgl2",{antialias:!0,alpha:!1,preserveDrawingBuffer:!1})??n.getContext("webgl",{antialias:!0,alpha:!1,preserveDrawingBuffer:!1});if(!e)throw new Error("WebGL контекст није доступан у овом прегледачу.");const t=new um({canvas:n,context:e,antialias:!0,alpha:!1,powerPreference:"default"});return t.setPixelRatio(1),t.outputColorSpace=Nt,vi=n,ln=t,Kn=320,$n=240,ln.setSize(Kn,$n,!1),ln}function Hm(){ln&&(ln.forceContextLoss(),ln.dispose(),ln=null,vi=null,Kn=0,$n=0)}function Lt(n){n.traverse(e=>{const t=e;t.geometry&&typeof t.geometry.dispose=="function"&&t.geometry.dispose();const i=t.material;if(Array.isArray(i))for(const r of i)nc(r);else i&&nc(i)})}function nc(n){for(const e of Object.values(n))e instanceof Rt&&e.dispose();n.dispose()}function gm(n,e,t,i){const r=mm(),a=t.platno.getContext("2d");if(!a||!vi)throw new Error("2D контекст платна није доступан.");const s=typeof window<"u"&&typeof window.matchMedia=="function"&&window.matchMedia("(prefers-reduced-motion: reduce)").matches,o=new _u,c=new Bt(42,16/9,.1,100),l=new k(0,0,0),d=new Tu(new ce(1,1,1),.72),h=new Ro(new ce(1,1,1),.95);h.position.set(5,8,6);const f=new Ro(new ce(1,1,1),.38);f.position.set(-5,-3,-4),o.add(d,h,f);const m=n.pocetnaKamera?.(e)??{theta:.62,phi:1.12,udaljenost:6.2};function g(ee){const _e=Math.sin(ee.phi);c.position.set(l.x+ee.udaljenost*_e*Math.sin(ee.theta),l.y+ee.udaljenost*Math.cos(ee.phi),l.z+ee.udaljenost*_e*Math.cos(ee.theta)),c.lookAt(l),c.updateMatrixWorld()}g(m);let _=!1,p=!1,u=!0,y=n.imaPodrazumevanuAnimaciju?n.imaPodrazumevanuAnimaciju(e):!0,S=s||!y,M=null,T=null,b=0,w=0,L=Math.max(240,t.bina.clientWidth||600),x=Math.max(180,t.bina.clientHeight||360),v=null;function R(){if(_||p||!vi||!a)return;const ee=t.bina.clientWidth,_e=t.bina.clientHeight;ee>0&&_e>0&&(L=ee,x=_e);const de=Math.min(typeof window<"u"&&window.devicePixelRatio||1,2),Z=Math.max(1,Math.round(L*de)),re=Math.max(1,Math.round(x*de));(t.platno.width!==Z||t.platno.height!==re)&&(t.platno.width=Z,t.platno.height=re),c.aspect=L/Math.max(1,x),c.updateProjectionMatrix();const ae=Math.min(4096,Math.max(Kn,Z)),I=Math.min(4096,Math.max($n,re));(ae>Kn||I>$n)&&(Kn=ae,$n=I,r.setSize(Kn,$n,!1));const Ie=new ce(Xr.token("--bg-card"));r.setViewport(0,0,Z,re),r.setScissor(0,0,Z,re),r.setScissorTest(!0),r.setClearColor(Ie,1),r.clear(!0,!0,!0),r.render(o,c);const Ce=Math.max(0,vi.height-re);a.drawImage(vi,0,Ce,Z,re,0,0,Z,re),v?.posleRendera?.()}function U(){_||p||M!==null||T!==null||(T=requestAnimationFrame(()=>{T=null,R()}))}function C(){const ee=typeof document<"u"&&document.hidden;return!_&&!p&&y&&!S&&u&&!ee}function P(ee){if(M=null,!C())return;const _e=b>0?Math.min(.05,(ee-b)/1e3):.016;b=ee,w+=_e,v?.azuriraj?.(_e,w),R(),C()&&(M=requestAnimationFrame(P))}function F(){t.azurirajDugmePauze(S,y),C()?M===null&&(b=performance.now(),M=requestAnimationFrame(P)):M!==null&&(cancelAnimationFrame(M),M=null)}function N(ee){const _e=ee.clone().project(c),de=_e.z>=-1&&_e.z<=1;return{x:(_e.x*.5+.5)*L,y:(-_e.y*.5+.5)*x,vidljivo:de}}const O={scena3D:o,kamera:c,platno:t.platno,slojEtiketa:t.slojEtiketa,gornjeKontrole:t.gornjeKontrole,podnozje:t.podnozje,api:i,tema:Xr,smanjenPokret:s,zatraziRender:U,postaviImaAnimaciju:ee=>{y=ee,ee||(S=!0),F()},prikaziRezervu:ee=>{p=!0,F(),t.prikaziRezervu(ee)},projektujU2D:N},z=new pm({bina:t.bina,platno:t.platno,dugmeDodira:t.dugmeDodira,pocetno:m,naPromenu:ee=>{g(ee),U()},naReset:()=>{z.resetuj(),v?.resetuj?.(),R()},naPrekidacPauze:()=>{y&&(S=!S,F())}});v=n.kreiraj(O,e);const G=()=>{z.resetuj(),v?.resetuj?.(),R()},K=()=>{y&&(S=!S,F())},$=()=>{S=!0,F(),v?.korak?v.korak():(w+=.45,v?.azuriraj?.(.45,w)),R()},fe=()=>z.zumiraj(.86),De=()=>z.zumiraj(1.16);t.dugmeReset.addEventListener("click",G),t.dugmePauza.addEventListener("click",K),t.dugmeKorak.addEventListener("click",$),t.dugmeZumPlus.addEventListener("click",fe),t.dugmeZumMinus.addEventListener("click",De);let X=null;typeof ResizeObserver<"u"&&(X=new ResizeObserver(ee=>{for(const _e of ee){const de=Math.round(_e.contentRect.width),Z=Math.round(_e.contentRect.height);de>0&&Z>0&&(de!==L||Z!==x)&&(L=de,x=Z,R())}}),X.observe(t.bina));let ne=null;typeof IntersectionObserver<"u"&&(ne=new IntersectionObserver(ee=>{for(const _e of ee)u=_e.isIntersecting,F()},{threshold:.05}),ne.observe(t.bina));const ue=()=>{F(),document.hidden||U()};document.addEventListener("visibilitychange",ue);const se=Xr.pretplati(ee=>{v?.osveziTemu?.(ee),R()});return R(),F(),()=>{_||(_=!0,M!==null&&(cancelAnimationFrame(M),M=null),T!==null&&(cancelAnimationFrame(T),T=null),X?.disconnect(),ne?.disconnect(),document.removeEventListener("visibilitychange",ue),se(),t.dugmeReset.removeEventListener("click",G),t.dugmePauza.removeEventListener("click",K),t.dugmeKorak.removeEventListener("click",$),t.dugmeZumPlus.removeEventListener("click",fe),t.dugmeZumMinus.removeEventListener("click",De),z.raspolazi(),v?.raspolazi?.(),Lt(o),o.clear(),t.slojEtiketa.replaceChildren(),t.gornjeKontrole.replaceChildren(),t.podnozje.replaceChildren())}}const ic={karlsbadski:{zakon:"karlsbadski",naziv:"Карлсбадски близанац",mineral:"ортоклас",sistem:"моноклинични",tipElementa:"osa",opisElementa:"Оса близањења [001] (c-оса), раван срастања (010)",normalaRavniIliOsa:[0,0,1],ugaoRotacijeStepeni:180,izvor:"Klein & Dutrow 2007, str. 235"},spinelov:{zakon:"spinelov",naziv:"Спинелов закон",mineral:"спинел (октаедар)",sistem:"кубни",tipElementa:"ravan",opisElementa:"Раван близањења (111)",normalaRavniIliOsa:[1/Math.sqrt(3),1/Math.sqrt(3),1/Math.sqrt(3)],izvor:"Klein & Dutrow 2007, str. 233"},baveno:{zakon:"baveno",naziv:"Бавено близанац",mineral:"ортоклас",sistem:"моноклинични",tipElementa:"ravan",opisElementa:"Раван близањења (021), моноклинична метрика (β ≈ 116°)",normalaRavniIliOsa:[.31,.7071,.6355],izvor:"Klein & Dutrow 2007, str. 235"},manebah:{zakon:"manebah",naziv:"Манебах близанац",mineral:"ортоклас",sistem:"моноклинични",tipElementa:"ravan",opisElementa:"Раван близањења (001), c* нормала одступа ~26° од c-осе због β ≈ 116°",normalaRavniIliOsa:[.4384,0,.8988],izvor:"Klein & Dutrow 2007, str. 235"},"albitski-polisintetski":{zakon:"albitski-polisintetski",naziv:"Албитски полисинтетски закон",mineral:"албит / плагиоклас",sistem:"триклинични",tipElementa:"ravan",opisElementa:"Раван близањења (010), вишеструке паралелне ламеле",normalaRavniIliOsa:[0,1,0],izvor:"Nesse 2012, str. 280"},japanski:{zakon:"japanski",naziv:"Јапански закон",mineral:"кварц",sistem:"тригонални",tipElementa:"ravan",opisElementa:"Раван близањења (11-22), теоријски угао међу c-осама 84°33′",normalaRavniIliOsa:[.37,.6408,.6726],ugaoOsaStepeni:84.55,izvor:"Frondel 1962, Dana System of Mineralogy Vol. III (a 4,913 c 5,405 Å)",napomena:"Угао 84°33′ је теоријски угао контакта две јединке кварца по (11-22)."},dofinejski:{zakon:"dofinejski",naziv:"Дофинејски закон",mineral:"кварц",sistem:"тригонални",tipElementa:"osa",opisElementa:"Оса близањења [0001] (c-оса), ротација за 180°",normalaRavniIliOsa:[0,0,1],ugaoRotacijeStepeni:180,izvor:"Klein & Dutrow 2007, str. 236"},brazilski:{zakon:"brazilski",naziv:"Бразилски закон",mineral:"кварц",sistem:"тригонални",tipElementa:"ravan",opisElementa:"Раван близањења (11-20), нормала [0,5, √3/2, 0] ≠ [100]",normalaRavniIliOsa:[.5,.866025,0],izvor:"Klein & Dutrow 2007, str. 236; International Tables хексагонска метрика"},"lastin-rep":{zakon:"lastin-rep",naziv:"Ластин реп (близанац гипса)",mineral:"гипс",sistem:"моноклинични",tipElementa:"ravan",opisElementa:"Раван близањења (100)",normalaRavniIliOsa:[1,0,0],izvor:"Klein & Dutrow 2007, str. 235"},"staurolit-90":{zakon:"staurolit-90",naziv:"Крстасти близанац стауролита (90°)",mineral:"стауролит",sistem:"моноклинични / псеудоорторомбични",tipElementa:"ravan",opisElementa:"Раван близањења (031), две јединке под ~90°",normalaRavniIliOsa:[0,.7071,.7071],izvor:"Klein & Dutrow 2007, str. 234"},"staurolit-60":{zakon:"staurolit-60",naziv:"Коси крстасти близанац стауролита (60°)",mineral:"стауролит",sistem:"моноклинични / псеудоорторомбични",tipElementa:"ravan",opisElementa:"Раван близањења (231), две c-осе заклапају ~60° (59°05′)",normalaRavniIliOsa:[.7093,.5038,.4931],ugaoOsaStepeni:59.08,izvor:"Klein & Dutrow 2007, str. 234 (метрика: a 7,87 b 16,62 c 5,66 Å)"},"kolenasti-rutil":{zakon:"kolenasti-rutil",naziv:"Коленасти близанац рутила",mineral:"рутил",sistem:"тетрагонални",tipElementa:"ravan",opisElementa:"Раван близањења (011), прегиб c-оса под 114°30′",normalaRavniIliOsa:[0,.542,.8404],ugaoOsaStepeni:114.5,izvor:"Klein & Dutrow 2007, str. 234 (тетрагонално a 4,59 c 2,96 Å)"},"trilinga-aragonit":{zakon:"trilinga-aragonit",naziv:"Циклички трилинг арагонита",mineral:"арагонит",sistem:"орторомбични",tipElementa:"ravan",opisElementa:"Раван близањења (110), псеудохексагонални склоп",normalaRavniIliOsa:[.707,.707,0],izvor:"Klein & Dutrow 2007, str. 235"},"gvozdeni-krst-pirit":{zakon:"gvozdeni-krst-pirit",naziv:"Гвоздени крст (близанац пирита)",mineral:"пирит",sistem:"кубни (m-3)",tipElementa:"osa",opisElementa:"Оса близањења [001] са прорастањем два пиритоедра",normalaRavniIliOsa:[0,0,1],ugaoRotacijeStepeni:90,izvor:"Klein & Dutrow 2007, str. 234"}};function _m(n){const e=[];if(n.includes("спинел")||n.includes("октаедар"))for(const r of[1,-1])for(const a of[1,-1])for(const s of[1,-1]){const o=1/Math.sqrt(3);e.push({normala:[r*o,a*o,s*o],d:1})}else if(n.includes("ортоклас"))e.push({normala:[.707,.707,0],d:.9},{normala:[-.707,.707,0],d:.9},{normala:[.707,-.707,0],d:.9},{normala:[-.707,-.707,0],d:.9},{normala:[0,1,0],d:1},{normala:[0,-1,0],d:1},{normala:[0,0,1],d:1.5},{normala:[0,0,-1],d:1.5},{normala:[.5,0,.866],d:1.1},{normala:[-.5,0,-.866],d:1.1});else if(n.includes("кварц")){const r=Math.sqrt(3),a=[[1,0,0],[-1,0,0],[.5,r/2,0],[-.5,r/2,0],[.5,-r/2,0],[-.5,-r/2,0]];for(const l of a)e.push({normala:l,d:.85});const s=51.78*Math.PI/180,o=Math.sin(s),c=Math.cos(s);for(let l=0;l<6;l++){const d=l*60*Math.PI/180;e.push({normala:[o*Math.cos(d),o*Math.sin(d),c],d:1.35}),e.push({normala:[o*Math.cos(d),o*Math.sin(d),-c],d:1.35})}}else if(n.includes("пирит")){const r=[[0,1,2],[1,2,0],[2,0,1]],a=[[1,1],[1,-1],[-1,1],[-1,-1]],s=Math.sqrt(5);for(const o of r)for(const c of a){const l=[0,0,0];l[o[0]]=2*c[0]/s,l[o[1]]=1*c[1]/s,l[o[2]]=0,e.push({normala:[l[0],l[1],l[2]],d:1})}}else e.push({normala:[1,0,0],d:.75},{normala:[-1,0,0],d:.75},{normala:[0,1,0],d:.85},{normala:[0,-1,0],d:.85},{normala:[0,0,1],d:1.6},{normala:[0,0,-1],d:1.6},{normala:[.707,0,.707],d:1.25},{normala:[-.707,0,.707],d:1.25},{normala:[.707,0,-.707],d:1.25},{normala:[-.707,0,-.707],d:1.25});const t=Wi(e);return Xi(t).geometrijaMreze}const vm={imaPodrazumevanuAnimaciju(n){return(n.animacija??"razdvoji-spoji")!=="nema"},pocetnaKamera(){return{theta:.65,phi:1.15,udaljenost:5.8}},kreiraj(n,e){const t=new nt;n.scena3D.add(t);const i=ic[e.zakon]??ic.karlsbadski,r=_m(i.mineral),a=new ct({color:new ce(n.tema.token("--primary")),roughness:.35,metalness:.1,flatShading:!0,side:mt}),s=new ct({color:new ce(n.tema.token("--accent")),roughness:.35,metalness:.1,flatShading:!0,side:mt}),o=new je(r,a),c=r.clone(),l=new je(c,s),d=new k(...i.normalaRavniIliOsa).normalize(),h=new nt;if(h.add(l),i.tipElementa==="osa"){const M=(i.ugaoRotacijeStepeni??180)*Math.PI/180;l.rotateOnAxis(d,M)}else{const M=new at().set(1-2*d.x*d.x,-2*d.x*d.y,-2*d.x*d.z,0,-2*d.y*d.x,1-2*d.y*d.y,-2*d.y*d.z,0,-2*d.z*d.x,-2*d.z*d.y,1-2*d.z*d.z,0,0,0,0,1);c.applyMatrix4(M);const T=c.index;if(T){for(let b=0;b<T.count;b+=3){const w=T.getX(b+1);T.setX(b+1,T.getX(b+2)),T.setX(b+2,w)}T.needsUpdate=!0}c.computeVertexNormals()}t.add(o),t.add(h);const f=new Di({color:new ce(n.tema.token("--warning")),transparent:!0,opacity:.35,side:mt}),m=new ht({color:new ce(n.tema.token("--warning")),linewidth:2});let g=null,_=null;if(e.prikazi_element!==!1)if(i.tipElementa==="ravan"){const M=new Li(3.5,3.5);g=new je(M,f),g.quaternion.setFromUnitVectors(new k(0,0,1),d),t.add(g)}else{const M=new Ye,T=d.clone().multiplyScalar(-2.8),b=d.clone().multiplyScalar(2.8);M.setAttribute("position",new Ge([T.x,T.y,T.z,b.x,b.y,b.z],3)),_=new Gi(M,m),t.add(_)}const p=document.createElement("div");p.className="udzbenik-scena-status",p.textContent=`${i.naziv} (${i.mineral}) • ${i.opisElementa}`,n.podnozje.append(p);const u=e.animacija??"razdvoji-spoji";let y=0;function S(){a.color.set(n.tema.token("--primary")),s.color.set(n.tema.token("--accent")),f.color.set(n.tema.token("--warning")),m.color.set(n.tema.token("--warning"))}return{azuriraj(M){if(y+=M,u==="razdvoji-spoji"){const T=(Math.sin(y*1.5)*.5+.5)*1.1;h.position.copy(d.clone().multiplyScalar(T)),t.rotation.y=y*.25}else u==="rotacija"&&(t.rotation.y=y*.45)},korak(){y+=.4;const M=(Math.sin(y*1.5)*.5+.5)*1.1;h.position.copy(d.clone().multiplyScalar(M)),t.rotation.y+=.2},resetuj(){y=0,h.position.set(0,0,0),t.rotation.set(0,0,0)},osveziTemu(){S()},raspolazi(){r.dispose(),l.geometry.dispose(),a.dispose(),s.dispose(),f.dispose(),m.dispose(),g&&g.geometry.dispose(),_&&_.geometry.dispose(),Lt(t),p.remove()}}}};class Gn extends Error{constructor(e){super(e),this.name="CifGreska"}}function sn(n,e){const t=n.trim().replace(/\([0-9]+\)$/,""),i=Number(t);if(!Number.isFinite(i))throw new Gn(`Неисправна нумеричка вредност у CIF пољу ${e}: "${n}"`);return i}function Ar(n){const e=[];let t=0;const i=n.length;for(;t<i;){for(;t<i&&/\s/.test(n[t]);)t++;if(t>=i)break;const r=n[t];if(r==="#")break;if(r==="'"||r==='"'){const a=r;t++;let s=t;for(;t<i&&!(n[t]===a&&(t+1>=i||/\s/.test(n[t+1])));)t++;e.push(n.slice(s,t)),t<i&&n[t]===a&&t++}else{const a=t;for(;t<i&&!/\s/.test(n[t]);)t++;e.push(n.slice(a,t))}}return e}function xm(n){if(!n||!n.trim())throw new Gn("CIF садржај је празан.");const e=n.split(/\r?\n/);let t="struktura";const i=new Map,r=[];let a=0;for(;a<e.length;){const m=e[a].trim();if(!m||m.startsWith("#")){a++;continue}if(m.toLowerCase().startsWith("data_")){t=m.slice(5).trim()||t,a++;continue}if(m.toLowerCase()==="loop_"){a++;const g=[];for(;a<e.length;){const T=e[a].trim();if(!T||T.startsWith("#")){a++;continue}if(T.startsWith("_")){const b=Ar(T);b[0]&&g.push(b[0].toLowerCase()),a++}else break}const _=g.indexOf("_atom_site_label"),p=g.indexOf("_atom_site_type_symbol"),u=g.indexOf("_atom_site_fract_x"),y=g.indexOf("_atom_site_fract_y"),S=g.indexOf("_atom_site_fract_z"),M=_!==-1&&p!==-1&&u!==-1&&y!==-1&&S!==-1;for(;a<e.length;){const T=e[a].trim();if(!T||T.startsWith("#")){a++;continue}const b=T.toLowerCase();if(T.startsWith("_")||b==="loop_"||b.startsWith("data_")||T.startsWith(";"))break;if(M&&g.length>0){const w=Ar(T);if(w.length<g.length)throw new Gn("Непотпун ред у _atom_site табели CIF фајла.");const L=w[_],x=w[p],v=sn(w[u],"_atom_site_fract_x"),R=sn(w[y],"_atom_site_fract_y"),U=sn(w[S],"_atom_site_fract_z");r.push({oznaka:L,simbol:Jc(x),fx:v,fy:R,fz:U})}a++}continue}if(m.startsWith("_")){const g=Ar(m);if(g.length>=2&&g[0]&&g[1]!==void 0)i.set(g[0].toLowerCase(),g[1]);else if(g.length===1&&g[0]&&a+1<e.length){const _=Ar(e[a+1].trim());_[0]&&!_[0].startsWith("_")&&_[0].toLowerCase()!=="loop_"&&(i.set(g[0].toLowerCase(),_[0]),a++)}}a++}const s=["_cell_length_a","_cell_length_b","_cell_length_c","_cell_angle_alpha","_cell_angle_beta","_cell_angle_gamma"];for(const m of s)if(!i.has(m))throw new Gn(`Недостаје обавезно CIF поље: ${m}`);const o=sn(i.get("_cell_length_a"),"_cell_length_a"),c=sn(i.get("_cell_length_b"),"_cell_length_b"),l=sn(i.get("_cell_length_c"),"_cell_length_c"),d=sn(i.get("_cell_angle_alpha"),"_cell_angle_alpha"),h=sn(i.get("_cell_angle_beta"),"_cell_angle_beta"),f=sn(i.get("_cell_angle_gamma"),"_cell_angle_gamma");if(o<=0||c<=0||l<=0)throw new Gn("Димензије јединичне ћелије a, b, c морају бити позитивне.");if(d<=0||d>=180||h<=0||h>=180||f<=0||f>=180||d+h+f>=360)throw new Gn("Углови јединичне ћелије α, β, γ нису физички валидни.");if(r.length===0)throw new Gn("CIF не садржи ниједан атом у loop_ _atom_site блоку.");return{nazivBloka:t,celija:{a:o,b:c,c:l,alpha:d,beta:h,gamma:f},atomi:r}}function ks(n){const e=Math.PI/180,t=n.alpha*e,i=n.beta*e,r=n.gamma*e,a=Math.cos(t),s=Math.cos(i),o=Math.cos(r),c=Math.sin(r),l=n.a,d=0,h=n.b*o,f=n.b*c,m=0,g=n.c*s,_=n.c*(a-s*o)/c,p=Math.max(0,n.c*n.c-g*g-_*_),u=Math.sqrt(p);return{va:[l,d,-0],vb:[h,m,-f],vc:[g,u,-_]}}function wn(n,e,t,i){return[n*i.va[0]+e*i.vb[0]+t*i.vc[0],n*i.va[1]+e*i.vb[1]+t*i.vc[1],n*i.va[2]+e*i.vb[2]+t*i.vc[2]]}const wa=[{kljuc:"kubna-P",naziv:"Кубна примитивна (P)",sistem:"Кубни",centriranje:"P",brojCvorova:1,celija:{a:1.8,b:1.8,c:1.8,alpha:90,beta:90,gamma:90},cvoroviFrakcioni:[[0,0,0]]},{kljuc:"kubna-I",naziv:"Кубна просторно центрирана (I)",sistem:"Кубни",centriranje:"I",brojCvorova:2,celija:{a:1.8,b:1.8,c:1.8,alpha:90,beta:90,gamma:90},cvoroviFrakcioni:[[0,0,0],[.5,.5,.5]],primitivniVektori:[[-.5,.5,.5],[.5,-.5,.5],[.5,.5,-.5]]},{kljuc:"kubna-F",naziv:"Кубна површински центрирана (F)",sistem:"Кубни",centriranje:"F",brojCvorova:4,celija:{a:1.8,b:1.8,c:1.8,alpha:90,beta:90,gamma:90},cvoroviFrakcioni:[[0,0,0],[0,.5,.5],[.5,0,.5],[.5,.5,0]],primitivniVektori:[[0,.5,.5],[.5,0,.5],[.5,.5,0]]},{kljuc:"tetragonalna-P",naziv:"Тетрагонална примитивна (P)",sistem:"Тетрагонални",centriranje:"P",brojCvorova:1,celija:{a:1.6,b:1.6,c:2.3,alpha:90,beta:90,gamma:90},cvoroviFrakcioni:[[0,0,0]]},{kljuc:"tetragonalna-I",naziv:"Тетрагонална просторно центрирана (I)",sistem:"Тетрагонални",centriranje:"I",brojCvorova:2,celija:{a:1.6,b:1.6,c:2.3,alpha:90,beta:90,gamma:90},cvoroviFrakcioni:[[0,0,0],[.5,.5,.5]],primitivniVektori:[[-.5,.5,.5],[.5,-.5,.5],[.5,.5,-.5]]},{kljuc:"ortorombicna-P",naziv:"Орторомбична примитивна (P)",sistem:"Орторомбични",centriranje:"P",brojCvorova:1,celija:{a:1.4,b:1.9,c:2.4,alpha:90,beta:90,gamma:90},cvoroviFrakcioni:[[0,0,0]]},{kljuc:"ortorombicna-C",naziv:"Орторомбична базно центрирана (C)",sistem:"Орторомбични",centriranje:"C",brojCvorova:2,celija:{a:1.4,b:1.9,c:2.4,alpha:90,beta:90,gamma:90},cvoroviFrakcioni:[[0,0,0],[.5,.5,0]],primitivniVektori:[[.5,.5,0],[-.5,.5,0],[0,0,1]]},{kljuc:"ortorombicna-I",naziv:"Орторомбична просторно центрирана (I)",sistem:"Орторомбични",centriranje:"I",brojCvorova:2,celija:{a:1.4,b:1.9,c:2.4,alpha:90,beta:90,gamma:90},cvoroviFrakcioni:[[0,0,0],[.5,.5,.5]],primitivniVektori:[[-.5,.5,.5],[.5,-.5,.5],[.5,.5,-.5]]},{kljuc:"ortorombicna-F",naziv:"Орторомбична површински центрирана (F)",sistem:"Орторомбични",centriranje:"F",brojCvorova:4,celija:{a:1.4,b:1.9,c:2.4,alpha:90,beta:90,gamma:90},cvoroviFrakcioni:[[0,0,0],[0,.5,.5],[.5,0,.5],[.5,.5,0]],primitivniVektori:[[0,.5,.5],[.5,0,.5],[.5,.5,0]]},{kljuc:"heksagonalna-P",naziv:"Хексагонална примитивна (P)",sistem:"Хексагонални",centriranje:"P",brojCvorova:1,celija:{a:1.8,b:1.8,c:2.2,alpha:90,beta:90,gamma:120},cvoroviFrakcioni:[[0,0,0]]},{kljuc:"romboedarska-R",naziv:"Ромбоедарска (R, хексагонална поставка)",sistem:"Тригонални",centriranje:"R",brojCvorova:3,celija:{a:1.8,b:1.8,c:2.5,alpha:90,beta:90,gamma:120},cvoroviFrakcioni:[[0,0,0],[2/3,1/3,1/3],[1/3,2/3,2/3]],primitivniVektori:[[2/3,1/3,1/3],[-1/3,1/3,1/3],[-1/3,-2/3,1/3]]},{kljuc:"monoklinicna-P",naziv:"Моноклинична примитивна (P)",sistem:"Моноклинични",centriranje:"P",brojCvorova:1,celija:{a:1.5,b:1.8,c:2.1,alpha:90,beta:110,gamma:90},cvoroviFrakcioni:[[0,0,0]]},{kljuc:"monoklinicna-C",naziv:"Моноклинична базно центрирана (C)",sistem:"Моноклинични",centriranje:"C",brojCvorova:2,celija:{a:1.5,b:1.8,c:2.1,alpha:90,beta:110,gamma:90},cvoroviFrakcioni:[[0,0,0],[.5,.5,0]],primitivniVektori:[[.5,.5,0],[-.5,.5,0],[0,0,1]]},{kljuc:"triklinicna-P",naziv:"Триклинична примитивна (P)",sistem:"Триклинични",centriranje:"P",brojCvorova:1,celija:{a:1.4,b:1.7,c:2.1,alpha:78,beta:108,gamma:102},cvoroviFrakcioni:[[0,0,0]]}],Mm={imaPodrazumevanuAnimaciju(){return!0},pocetnaKamera(){return{theta:.65,phi:1.15,udaljenost:6.8}},kreiraj(n,e){let t=e.resetka==="sve"?"kubna-P":e.resetka;const i=new nt;n.scena3D.add(i);const r=new mn(.08,16,16),a=new ct({color:new ce(n.tema.token("--primary")),roughness:.25,metalness:.2}),s=new ct({color:new ce(n.tema.token("--accent")),roughness:.25,metalness:.2}),o=new ht({color:new ce(n.tema.token("--text-secondary")),linewidth:2}),c=new Eu({color:new ce(n.tema.token("--border-color")),dashSize:.15,gapSize:.1}),l=new ht({color:new ce(n.tema.token("--warning")),linewidth:2});function d(p){for(;i.children.length>0;){const U=i.children[0];i.remove(U),Lt(U)}const u=ks(p.celija),y=new k(...u.va),S=new k(...u.vb),M=new k(...u.vc),b=y.clone().add(S).add(M).multiplyScalar(.5).clone().negate(),w=[[0,0,0],[1,0,0],[1,1,0],[0,1,0],[0,0,1],[1,0,1],[1,1,1],[0,1,1]].map(([U,C,P])=>{const[F,N,O]=wn(U,C,P,u);return new k(F,N,O).add(b)}),L=[[0,1],[1,2],[2,3],[3,0],[4,5],[5,6],[6,7],[7,4],[0,4],[1,5],[2,6],[3,7]],x=[];for(const U of L){const C=w[U[0]],P=w[U[1]];x.push(C.x,C.y,C.z,P.x,P.y,P.z)}const v=new Ye;v.setAttribute("position",new Ge(x,3)),i.add(new gt(v,o));const R=new Set;for(const[U,C,P]of p.cvoroviFrakcioni)for(let F=0;F<=1;F++)for(let N=0;N<=1;N++)for(let O=0;O<=1;O++){const z=U+F,G=C+N,K=P+O;if(z>=-1e-4&&z<=1.0001&&G>=-1e-4&&G<=1.0001&&K>=-1e-4&&K<=1.0001){const $=`${z.toFixed(2)},${G.toFixed(2)},${K.toFixed(2)}`;if(R.has($))continue;R.add($);const[fe,De,X]=wn(z,G,K,u),ne=new k(fe,De,X).add(b),ue=(F===0||F===1)&&(N===0||N===1)&&(O===0||O===1)&&U===0&&C===0&&P===0,se=new je(r,ue?a:s);se.position.copy(ne),i.add(se)}}if(e.prikazi_susedne_celije){const U=[];for(const F of[-1,0,1])for(const N of[-1,0,1])for(const O of[-1,0,1]){if(F===0&&N===0&&O===0)continue;const z=y.clone().multiplyScalar(F).add(S.clone().multiplyScalar(N)).add(M.clone().multiplyScalar(O));for(const G of L){const K=w[G[0]].clone().add(z),$=w[G[1]].clone().add(z);U.push(K.x,K.y,K.z,$.x,$.y,$.z)}}const C=new Ye;C.setAttribute("position",new Ge(U,3));const P=new gt(C,c);P.computeLineDistances(),i.add(P)}if(e.prikazi_primitivnu_celiju&&p.primitivniVektori){const U=[],C=w[0],P=p.primitivniVektori.map(([K,$,fe])=>{const[De,X,ne]=wn(K,$,fe,u);return new k(De,X,ne)}),F=P[0],N=P[1],O=P[2],z=[C,C.clone().add(F),C.clone().add(F).add(N),C.clone().add(N),C.clone().add(O),C.clone().add(F).add(O),C.clone().add(F).add(N).add(O),C.clone().add(N).add(O)];for(const K of L){const $=z[K[0]],fe=z[K[1]];U.push($.x,$.y,$.z,fe.x,fe.y,fe.z)}const G=new Ye;G.setAttribute("position",new Ge(U,3)),i.add(new gt(G,l))}}const h=document.createElement("div");h.className="udzbenik-scena-status",n.podnozje.append(h);function f(p){h.textContent=`${p.naziv} • Систем: ${p.sistem} • Чворова по конвенционалној ћелији: ${p.brojCvorova}`}if(e.resetka==="sve"){const p=document.createElement("div");p.className="udzbenik-bravais-traka",p.style.display="flex",p.style.flexWrap="wrap",p.style.gap="4px";for(const u of wa){const y=document.createElement("button");y.type="button",y.className="udzbenik-dugme udzbenik-dugme--malo",u.kljuc===t&&y.classList.add("udzbenik-dugme--aktivno"),y.textContent=u.kljuc,y.setAttribute("aria-label",u.naziv),y.addEventListener("click",()=>{t=u.kljuc,p.querySelectorAll("button").forEach(S=>S.classList.remove("udzbenik-dugme--aktivno")),y.classList.add("udzbenik-dugme--aktivno"),d(u),f(u)}),p.append(y)}n.gornjeKontrole.append(p)}const m=wa.find(p=>p.kljuc===t)??wa[0];d(m),f(m);function g(){a.color.set(n.tema.token("--primary")),s.color.set(n.tema.token("--accent")),o.color.set(n.tema.token("--text-secondary")),c.color.set(n.tema.token("--border-color")),l.color.set(n.tema.token("--warning"))}let _=0;return{azuriraj(p){_+=p*.45,i.rotation.y=_},korak(){_+=.25,i.rotation.y=_},resetuj(){_=0,i.rotation.set(0,0,0)},osveziTemu(){g()},raspolazi(){r.dispose(),a.dispose(),s.dispose(),o.dispose(),c.dispose(),l.dispose(),Lt(i),h.remove()}}}};function Sm(n,e){const t=e??56,i=Math.round((180-t)*10)/10;switch(n){case"kubna":return{naziv:"Кубна цепљивост {100}",brojPravaca:"3 правца",uglovi:"90°",podrazumevaniPrimer:"халит, галенит"};case"oktaedarska":return{naziv:"Октаедарска цепљивост {111}",brojPravaca:"4 правца",uglovi:"70,5° и 109,5°",podrazumevaniPrimer:"флуорит, дијамант"};case"dodekaedarska":return{naziv:"Додекаедарска цепљивост {110}",brojPravaca:"6 праваца",uglovi:"60°, 90° и 120°",podrazumevaniPrimer:"сфалерит"};case"romboedarska":return{naziv:"Ромбоедарска цепљивост {101̄1}",brojPravaca:"3 правца",uglovi:"~75° и ~105° (≠ 90°)",podrazumevaniPrimer:"калцит, доломит"};case"bazalna":return{naziv:"Базална (пинакоидална) цепљивост {001}",brojPravaca:"1 правац",uglovi:"паралелне ламеле (0°)",podrazumevaniPrimer:"лискун (мусковит), графит"};case"prizmatska":return{naziv:"Призматска цепљивост {110}",brojPravaca:"2 правца",uglovi:`${t}° и ${i}°`,podrazumevaniPrimer:t>75?"пироксен":"амфибол"};case"nema":return{naziv:"Нема цепљивости (шкољкаст прелом)",brojPravaca:"0 праваца",uglovi:"нема равни цепљивости",podrazumevaniPrimer:"кварц"}}}function jn(n,e,t,i){const r=Wi(n);if(r.pljosni.length<4||r.temena.length<4)return null;const a=Xi(r),s=new nt;return s.add(new je(a.geometrijaMreze,t),new gt(a.geometrijaIvica,i)),{grupa:s,smerRazdvajanja:e}}function on(n,e,t,i,r){const a=new Li(t,t),s=new je(a,i),o=new gt(new Br(a),r),c=new nt;c.add(s,o);const l=new k(...n).normalize();return c.quaternion.setFromUnitVectors(new k(0,0,1),l),c.position.copy(l).multiplyScalar(e),c}function mi(n,e){const t=Math.hypot(n-.35,e-.25),i=.055*Math.sin(t*13.5);return .28*(n*n-.5*e*e)+.18*n+i}function Em(n,e,t,i){if(!n){const h=[{normala:[0,-1,0],d:1.15}];for(let m=0;m<6;m++){const g=m*Math.PI/3,_=Math.cos(g),p=Math.sin(g);h.push({normala:[_,0,p],d:.95}),h.push({normala:[_*.72,.69,p*.72],d:1.28}),h.push({normala:[_*.72,-.69,p*.72],d:1.28})}const f=jn(h,new k(0,0,0),e,i);return{fragmenti:f?[f]:[]}}const o=12,c=24;function l(h,f){const m=(f%(Math.PI/3)+Math.PI/3)%(Math.PI/3)-Math.PI/6,g=.95*Math.cos(Math.PI/6)/Math.cos(m);return[h*g*Math.cos(f),h*g*Math.sin(f)]}function d(h){const f=[],m=[],g=[],_=h?1.15:-1.15,p=h?1.85:-1.85;for(let T=0;T<o;T++){const b=T/o,w=(T+1)/o;for(let L=0;L<c;L++){const x=L/c*Math.PI*2,v=(L+1)/c*Math.PI*2,[R,U]=l(b,x),[C,P]=l(w,x),[F,N]=l(w,v),[O,z]=l(b,v),G=mi(R,U),K=mi(C,P),$=mi(F,N),fe=mi(O,z);h?m.push(R,G,U,F,$,N,C,K,P,R,G,U,O,fe,z,F,$,N):m.push(R,G,U,C,K,P,F,$,N,R,G,U,F,$,N,O,fe,z)}}for(let T=0;T<c;T++){const b=T/c*Math.PI*2,w=(T+1)/c*Math.PI*2,[L,x]=l(1,b),[v,R]=l(1,w),U=mi(L,x),C=mi(v,R);h?(f.push(L,U,x,v,C,R,v,_,R,L,U,x,v,_,R,L,_,x),f.push(L,_,x,v,_,R,0,p,0)):(f.push(L,_,x,v,_,R,v,C,R,L,_,x,v,C,R,L,U,x),f.push(v,_,R,L,_,x,0,p,0)),g.push(L,U,x,v,C,R),g.push(L,_,x,v,_,R),T%(c/6)===0&&(g.push(L,U,x,L,_,x),g.push(L,_,x,0,p,0))}const u=new Ye;u.setAttribute("position",new Ge(f,3)),u.computeVertexNormals();const y=new Ye;y.setAttribute("position",new Ge(m,3)),y.computeVertexNormals();const S=new Ye;S.setAttribute("position",new Ge(g,3));const M=new nt;return M.add(new je(u,e),new je(y,t),new gt(S,i)),M}return{fragmenti:[{grupa:d(!0),smerRazdvajanja:new k(.18,.55,.1)},{grupa:d(!1),smerRazdvajanja:new k(-.18,-.55,-.1)}]}}const ym={imaPodrazumevanuAnimaciju(n){return!(n.vrsta==="nema"&&!n.prikazi_prelom)},pocetnaKamera(){return{theta:.68,phi:1.14,udaljenost:5.9}},kreiraj(n,e){const t=e.vrsta,i=e.ugao??56,r=e.prikazi_prelom??!1,a=new nt,s=new nt,o=new nt;a.add(s,o),n.scena3D.add(a);const c=new ct({color:new ce(n.tema.token("--primary")),transparent:!0,opacity:.86,roughness:.32,metalness:.08,flatShading:!0}),l=new ct({color:new ce(n.tema.token("--accent")),roughness:.22,metalness:.15,side:mt}),d=new ht({color:new ce(n.tema.token("--text-primary"))}),h=new Di({color:new ce(n.tema.token("--accent")),transparent:!0,opacity:.26,side:mt,depthWrite:!1}),f=new ht({color:new ce(n.tema.token("--accent"))}),m=[];function g(){if(t==="kubna"){const T=[-1,1];for(const b of T)for(const w of T)for(const L of T){const x=[{normala:[b,0,0],d:1.05},{normala:[-b,0,0],d:0},{normala:[0,w,0],d:1.05},{normala:[0,-w,0],d:0},{normala:[0,0,L],d:1.05},{normala:[0,0,-L],d:0}],v=jn(x,new k(b,w,L).normalize().multiplyScalar(.52),c,d);v&&m.push(v)}o.add(on([1,0,0],0,2.6,h,f),on([0,1,0],0,2.6,h,f),on([0,0,1],0,2.6,h,f))}else if(t==="oktaedarska"){const T=Xs([1,1,1]).map(w=>({normala:w.normala,d:1.08})),b=[[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]];for(let w=0;w<16;w++){const L=[...T],x=new k;for(let R=0;R<4;R++){const U=(w&1<<R)!==0?1:-1,C=b[R];L.push({normala:[C[0]*U,C[1]*U,C[2]*U],d:0}),x.add(new k(C[0]*U,C[1]*U,C[2]*U))}const v=jn(L,x.lengthSq()>1e-4?x.normalize().multiplyScalar(.52):x,c,d);v&&m.push(v)}for(const w of b)o.add(on(w,0,2.8,h,f))}else if(t==="dodekaedarska"){const T=Xs([1,1,0]).map(L=>({normala:L.normala,d:1.12})),b=[[1,1,0],[1,-1,0],[1,0,1],[1,0,-1],[0,1,1],[0,1,-1]];for(const L of b)o.add(on(L,0,2.7,h,f));const w=[[1,1,0],[1,-1,0],[0,1,1]];for(let L=0;L<8;L++){const x=[...T],v=new k;for(let U=0;U<3;U++){const C=(L&1<<U)!==0?1:-1,P=w[U];x.push({normala:[P[0]*C,P[1]*C,P[2]*C],d:0}),v.add(new k(P[0]*C,P[1]*C,P[2]*C))}const R=jn(x,v.normalize().multiplyScalar(.5),c,d);R&&m.push(R)}}else if(t==="romboedarska"){const T=[1,.26,.14],b=[.24,1,.22],w=[.18,.26,1],L=[T,b,w],x=[];for(const R of L)x.push({normala:R,d:1}),x.push({normala:[-R[0],-R[1],-R[2]],d:1}),o.add(on(R,0,2.8,h,f));const v=[-1,1];for(const R of v)for(const U of v)for(const C of v){const P=[...x,{normala:[-T[0]*R,-T[1]*R,-T[2]*R],d:0},{normala:[-b[0]*U,-b[1]*U,-b[2]*U],d:0},{normala:[-w[0]*C,-w[1]*C,-w[2]*C],d:0}],F=new k(T[0]*R+b[0]*U+w[0]*C,T[1]*R+b[1]*U+w[1]*C,T[2]*R+b[2]*U+w[2]*C).normalize().multiplyScalar(.5),N=jn(P,F,c,d);N&&m.push(N)}}else if(t==="bazalna"){const T=[];for(let x=0;x<6;x++){const v=x*Math.PI/3;T.push({normala:[Math.cos(v),0,Math.sin(v)],d:1.15})}const b=5,w=1.1,L=w/b;for(let x=0;x<b;x++){const v=-w/2+x*L,R=v+L,U=[...T,{normala:[0,1,0],d:R},{normala:[0,-1,0],d:-v}],C=x-(b-1)/2,P=jn(U,new k(C*.08,C*.28,0),c,d);P&&m.push(P),x>0&&o.add(on([0,1,0],v,2.7,h,f))}}else if(t==="prizmatska"){const T=i*Math.PI/180*.5,b=[Math.sin(T),0,Math.cos(T)],w=[-Math.sin(T),0,Math.cos(T)],L=[{normala:[0,1,0],d:1.3},{normala:[0,-1,0],d:1.3},{normala:b,d:.9},{normala:[-b[0],0,-b[2]],d:.9},{normala:w,d:.9},{normala:[-w[0],0,-w[2]],d:.9}];o.add(on(b,0,2.9,h,f),on(w,0,2.9,h,f));const x=[-1,1];for(const v of x)for(const R of x){const U=[...L,{normala:[-b[0]*v,0,-b[2]*v],d:0},{normala:[-w[0]*R,0,-w[2]*R],d:0}],C=new k(b[0]*v+w[0]*R,0,b[2]*v+w[2]*R).normalize().multiplyScalar(.48),P=jn(U,C,c,d);P&&m.push(P)}}else{const T=Em(r,c,l,d);m.push(...T.fragmenti)}for(const T of m)s.add(T.grupa)}g();const _=Sm(t,i),p=e.primer||_.podrazumevaniPrimer,u=document.createElement("div");u.className="udzbenik-scena-info-red udzbenik-cepljivost-meta";const y=[[ot("brojPravacaCepljivosti"),_.brojPravaca],[ot("ugloviCepljivosti"),_.uglovi],[ot("primerMinerala"),p]];for(const[T,b]of y){const w=document.createElement("span");w.className="udzbenik-meta-stavka";const L=document.createElement("strong");L.textContent=`${T}: `;const x=document.createElement("span");x.textContent=b,w.append(L,x),u.append(w)}n.podnozje.append(u);let S=n.smanjenPokret?.72:0;function M(){if(t==="nema"&&!r){o.visible=!1;return}let T=0,b=0;if(S<.3)T=S/.3,b=0;else if(S<.72){T=1;const w=(S-.3)/.42;b=w*w*(3-2*w)}else if(S<.85)T=1,b=1;else{const w=(S-.85)/.15;T=1-w,b=1-w*w*(3-2*w)}o.visible=t!=="nema"&&T>.02,o.scale.setScalar(.25+.75*T),h.opacity=.26*T*(1-.45*b);for(const w of m)w.grupa.position.copy(w.smerRazdvajanja).multiplyScalar(b)}return M(),{azuriraj(T){S=(S+T*.17)%1,a.rotation.y+=T*.24,M()},korak(){S=(S+.18)%1,M()},resetuj(){a.rotation.set(0,0,0),S=n.smanjenPokret?.72:0,M()},osveziTemu(T){c.color.set(T.token("--primary")),l.color.set(T.token("--accent")),d.color.set(T.token("--text-primary")),h.color.set(T.token("--accent")),f.color.set(T.token("--accent"))},raspolazi(){Lt(a),c.dispose(),l.dispose(),d.dispose(),h.dispose(),f.dispose()}}}},jc=new Map,bm=["m-3m","m-3","-43m","432","4/mmm","6/mmm","6/m","-3m","32","mmm","2/m"];for(const n of bm){let e="kubni";n==="4/mmm"?e="tetragonalni":n==="6/mmm"||n==="6/m"?e="heksagonalni":n==="-3m"||n==="32"?e="trigonalni":n==="mmm"?e="ortorombicni":n==="2/m"&&(e="monoklinicni"),jc.set(n,(t,i)=>Es(t,n,e,i))}const Tm=["kubni","tetragonalni","heksagonalni","trigonalni","ortorombicni"];for(const n of Tm){const e=hc(n);jc.set(n,(t,i)=>Es(t,e,n,i))}function Am(n,e,t,i){const r=t??hc(e);return Es(n,r,e,i)}const wm={imaPodrazumevanuAnimaciju(n){return(n.animacija??"prelaz")!=="nema"},pocetnaKamera(){return{theta:.64,phi:1.12,udaljenost:4.8}},kreiraj(n,e){const t=e.animacija??"prelaz",r=e.forme.map((C,P)=>{const F=`forma-${P}`,N=C.naziv||(C.hkl.length===4?`{${C.hkl.join(" ")}}`:Qc(C.hkl)),O=Am(C.hkl,e.sistem,e.klasa,e.celija);return{grupaId:F,oznakaForme:N,baznoD:C.d,hkl:C.hkl,ekvivalentne:O}}),a=new nt;n.scena3D.add(a);const s=new ht({color:new ce(n.tema.token("--text-primary"))}),o=r.map((C,P)=>new ct({color:new ce(n.tema.token("--primary")),roughness:.32,metalness:.1,flatShading:!0,name:`mat-forma-${P}`}));let c=null,l=null,d="";function h(){const C=new ce(n.tema.token("--primary")),P=new ce(n.tema.token("--accent")),F=new ce(n.tema.token("--bg-elevated"));for(let N=0;N<o.length;N++){const O=o[N],z=r[N].grupaId,G=r.length>1?N/(r.length-1):0,K=C.clone().lerp(P,G);N%2===1&&r.length>2&&K.lerp(F,.22),O.color.copy(K);const $=c===z;O.emissive.copy($?K.clone().multiplyScalar(.28):new ce(0,0,0))}s.color.set(n.tema.token("--text-primary"))}h();const f=document.createElement("div");f.className="udzbenik-scena-etiketa udzbenik-scena-etiketa--istaknuta",f.hidden=!0,n.slojEtiketa.append(f);let m=.5,g=n.smanjenPokret?.25:0,_=null;if(r.length>1){const C=document.createElement("label");C.className="udzbenik-klizac-oznaka";const P=document.createElement("span");P.textContent=`${ot("prelazFormi")}: ${r[0].oznakaForme} ↔ ${r[r.length-1].oznakaForme}`,_=document.createElement("input"),_.type="range",_.min="0",_.max="1",_.step="0.01",_.value="0.5",_.className="udzbenik-klizac",_.addEventListener("input",()=>{m=Number(_.value),x(m),n.zatraziRender()}),C.append(P,_),n.gornjeKontrole.append(C)}const p=document.createElement("div");p.className="udzbenik-habitus-forme";const u=new Map;for(const C of r){const P=document.createElement("button");P.type="button",P.className="udzbenik-mohs-cip",P.textContent=C.oznakaForme;const F=()=>{c=C.grupaId;const N=T?.pljosni.find(O=>O.grupaId===C.grupaId);N?(l=new k(...N.centar),d=`${C.oznakaForme} · ${N.oznaka}`):(l=null,d=C.oznakaForme),h(),w(),n.zatraziRender()};P.addEventListener("click",F),P.addEventListener("focus",F),P.addEventListener("blur",()=>{c===C.grupaId&&(c=null,l=null,h(),w(),n.zatraziRender())}),u.set(C.grupaId,P),p.append(P)}const y=document.createElement("span");y.className="udzbenik-habitus-status",p.append(y),n.podnozje.append(p);let S=null,M=null,T=null,b=[];function w(){if(!T)return;const C=T.pljosni.length,P=T.temena.length,F=e.primer?` · ${ot("primerMinerala")}: ${e.primer}`:"",N=d&&c?` · ${d}`:"";y.textContent=`${C} пљосни, ${P} темена${F}${N}`;for(const[O,z]of u.entries()){const G=T.pljosni.some(K=>K.grupaId===O);z.classList.toggle("udzbenik-mohs-cip--aktivan",c===O),z.classList.toggle("udzbenik-mohs-cip--prigusen",!G)}}function L(C){const P=r.length;return P<=1?r.map(F=>F.baznoD):r.map((F,N)=>{const O=N/(P-1);let z=1;return C<.5?z=1+(.5-C)*2*O*.95:C>.5&&(z=1+(C-.5)*2*(1-O)*.95),F.baznoD*z})}function x(C){S&&(S.geometry.dispose(),a.remove(S)),M&&(M.geometry.dispose(),a.remove(M));const P=L(C),F=[];for(let $=0;$<r.length;$++){const fe=r[$],De=P[$];for(const X of fe.ekvivalentne)F.push({normala:X.normala,d:De,grupaId:fe.grupaId,oznaka:X.oznaka})}const N=Wi(F);let O=.001;for(const $ of N.temena)O=Math.max(O,Math.hypot($[0],$[1],$[2]));const z=1.48/O;for(const $ of N.temena)$[0]*=z,$[1]*=z,$[2]*=z;for(const $ of N.pljosni)$.centar[0]*=z,$.centar[1]*=z,$.centar[2]*=z;const G=Xi(N),K=G.redosledGrupa.map($=>{const fe=r.findIndex(De=>De.grupaId===$);return o[Math.max(0,fe)]});S=new je(G.geometrijaMreze,K),M=new gt(G.geometrijaIvica,s),a.add(S,M),T=N,b=G.mapaTrougaoUPljosan,w()}const v=new Ns,R=new Xe,U=C=>{if(!S||!T)return;const P=n.platno.getBoundingClientRect();if(P.width<=0||P.height<=0)return;R.x=(C.clientX-P.left)/P.width*2-1,R.y=-((C.clientY-P.top)/P.height)*2+1,v.setFromCamera(R,n.kamera);const F=v.intersectObject(S,!1);if(F.length>0&&F[0].faceIndex!==void 0&&F[0].faceIndex!==null){const N=b[F[0].faceIndex],O=N!==void 0?T.pljosni[N]:void 0;if(O){const z=r.find(G=>G.grupaId===O.grupaId);c=O.grupaId,l=new k(...O.centar),d=`${z?.oznakaForme??O.grupaId} · ${O.oznaka}`,h(),w(),n.zatraziRender();return}}c!==null&&C.pointerType==="mouse"&&(c=null,l=null,h(),w(),n.zatraziRender())};return n.platno.addEventListener("pointermove",U),x(m),{azuriraj(C){t==="prelaz"&&r.length>1?(g=(g+C*.14)%1,m=.5-.5*Math.cos(g*Math.PI*2),_&&(_.value=m.toFixed(2)),a.rotation.y+=C*.25,x(m)):t==="rotacija"&&(a.rotation.y+=C*.42)},korak(){t==="prelaz"&&r.length>1?(g=(g+.125)%1,m=.5-.5*Math.cos(g*Math.PI*2),_&&(_.value=m.toFixed(2)),x(m)):a.rotation.y+=.35},resetuj(){a.rotation.set(0,0,0),m=.5,g=.25,_&&(_.value="0.5"),c=null,l=null,h(),x(.5)},osveziTemu(){h()},posleRendera(){if(!c||!l){f.hidden=!0;return}a.updateMatrixWorld(!0);const C=l.clone().applyMatrix4(a.matrixWorld),P=n.projektujU2D(C);if(!P.vidljivo){f.hidden=!0;return}f.textContent=d,f.hidden=!1,f.style.transform=`translate(-50%, -120%) translate(${P.x.toFixed(1)}px, ${P.y.toFixed(1)}px)`},raspolazi(){n.platno.removeEventListener("pointermove",U),Lt(a),s.dispose();for(const C of o)C.dispose()}}}},Tn=.8;function Vi(n,e){return n.map(([t,i,r])=>{const a=Math.hypot(t,i,r)||1;return[t/a*e,i/a*e,r/a*e]})}const rc=2/Math.sqrt(3)-1,ac=Math.sqrt(1.5)-1,sc=Math.SQRT2-1,oc=Math.sqrt(3)-1,cc=1,lc={2:{kb:2,nazivOblika:"Линеарни",granicniOdnos:.155,vrhovi:[[0,0,Tn*(1+.155)],[0,0,-Tn*(1+.155)]],trougloviIndeksi:[]},3:{kb:3,nazivOblika:"Троугаони",granicniOdnos:rc,vrhovi:Vi([[1,0,0],[-.5,Math.sqrt(3)/2,0],[-.5,-Math.sqrt(3)/2,0]],Tn*(1+rc)),trougloviIndeksi:[0,1,2]},4:{kb:4,nazivOblika:"Тетраедарски",granicniOdnos:ac,vrhovi:Vi([[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]],Tn*(1+ac)),trougloviIndeksi:[0,1,2,0,3,1,0,2,3,1,3,2]},6:{kb:6,nazivOblika:"Октаедарски",granicniOdnos:sc,vrhovi:Vi([[1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,1],[0,0,-1]],Tn*(1+sc)),trougloviIndeksi:[0,2,4,2,1,4,1,3,4,3,0,4,0,5,2,2,5,1,1,5,3,3,5,0]},8:{kb:8,nazivOblika:"Кубични",granicniOdnos:oc,vrhovi:Vi([[-1,-1,-1],[1,-1,-1],[1,1,-1],[-1,1,-1],[-1,-1,1],[1,-1,1],[1,1,1],[-1,1,1]],Tn*(1+oc)),trougloviIndeksi:[0,2,1,0,3,2,4,5,6,4,6,7,0,1,5,0,5,4,1,2,6,1,6,5,2,3,7,2,7,6,3,0,4,3,4,7]},12:{kb:12,nazivOblika:"Кубооктаедарски",granicniOdnos:cc,vrhovi:Vi([[1,1,0],[1,-1,0],[-1,-1,0],[-1,1,0],[1,0,1],[1,0,-1],[-1,0,-1],[-1,0,1],[0,1,1],[0,1,-1],[0,-1,-1],[0,-1,1]],Tn*(1+cc)),trougloviIndeksi:[0,8,4,1,4,11,2,11,7,3,7,8,0,5,9,1,10,5,2,6,10,3,9,6,0,4,1,0,1,5,2,7,3,2,3,6,8,9,3,8,3,0,11,1,2,11,2,10]}},Rm={imaPodrazumevanuAnimaciju(n){return n.prikazi_odnos_radijusa!==!1},pocetnaKamera(){return{theta:.65,phi:1.18,udaljenost:5.4}},kreiraj(n,e){const t=new nt;n.scena3D.add(t);const i=lc[e.kb]??lc[4],r=Tn,a=r*i.granicniOdnos,s=new mn(a,24,24),o=new ct({color:new ce(n.tema.token("--accent")),roughness:.25,metalness:.2}),c=new je(s,o);t.add(c);const l=new mn(r,24,24),d=new ct({color:new ce(n.tema.token("--primary")),roughness:.35,metalness:.1,transparent:!0,opacity:.85}),h=new nt;for(const[b,w,L]of i.vrhovi){const x=new je(l,d);x.position.set(b,w,L),h.add(x)}t.add(h);let f=null,m=null;const g=new ct({color:new ce(n.tema.token("--primary")),transparent:!0,opacity:.22,roughness:.2,side:mt}),_=new ht({color:new ce(n.tema.token("--text-secondary")),linewidth:2});if(i.trougloviIndeksi.length>=3){const b=new Ye,w=[];for(const x of i.trougloviIndeksi){const v=i.vrhovi[x];w.push(v[0],v[1],v[2])}b.setAttribute("position",new Ge(w,3)),b.computeVertexNormals(),f=new je(b,g),t.add(f);const L=new Br(b);m=new gt(L,_),t.add(m)}const p=e.katjon||"Katjon",u=e.anjon||"Anjon",y=document.createElement("div");y.className="udzbenik-scena-status",y.textContent=`КБ = ${i.kb} (${i.nazivOblika}) • Гранични однос RA/RX = ${i.granicniOdnos.toFixed(3)} • ${p} / ${u}`,n.podnozje.append(y);let S=0;const M=e.prikazi_odnos_radijusa!==!1;function T(){o.color.set(n.tema.token("--accent")),d.color.set(n.tema.token("--primary")),g.color.set(n.tema.token("--primary")),_.color.set(n.tema.token("--text-secondary"))}return{azuriraj(b){if(S+=b,t.rotation.y=S*.35,M){const w=Math.sin(S*1.8);if(w<-.2){const L=.08*(Math.abs(w)-.2);c.position.set(Math.sin(S*22)*L,Math.cos(S*19)*L,Math.sin(S*25)*L),c.scale.setScalar(.72)}else c.position.set(0,0,0),c.scale.setScalar(1)}},korak(){S+=.3,t.rotation.y+=.2},resetuj(){S=0,c.position.set(0,0,0),c.scale.setScalar(1),t.rotation.set(0,0,0)},osveziTemu(){T()},raspolazi(){s.dispose(),o.dispose(),l.dispose(),d.dispose(),f&&f.geometry.dispose(),m&&m.geometry.dispose(),g.dispose(),_.dispose(),Lt(t),y.remove()}}}},Cm={imaPodrazumevanuAnimaciju(){return!1},pocetnaKamera(n){return{theta:.65,phi:1.12,udaljenost:(n.prikaz??"celija")==="supercelija"?8.2:6.2}},kreiraj(n,e){const t=e.prikaz??"celija",i=e.stil??"kugle-stapici",r=e.prikazi_celiju??!0,a=e.oznake_atoma??!0,s=e.poluprecnici??"jonski";let o=!1,c=1.15,l=null,d=-1;const h=new nt,f=new nt,m=new nt,g=new nt;h.add(g,m,f),n.scena3D.add(h);const _=new ht({color:new ce(n.tema.token("--text-secondary"))}),p=new ct({color:new ce(n.tema.token("--text-muted")),roughness:.45,metalness:.15}),u=new Di({color:new ce(n.tema.token("--accent")),wireframe:!0}),y=new je(new mn(1,14,12),u);y.visible=!1,h.add(y);const S=document.createElement("div");S.className="udzbenik-scena-etiketa udzbenik-scena-etiketa--atom",S.hidden=!0,n.slojEtiketa.append(S);const M=document.createElement("div");if(M.className="udzbenik-struktura-kontrole",i==="kugle-stapici"){const O=document.createElement("label");O.className="udzbenik-klizac-oznaka";const z=document.createElement("span");z.textContent=`${ot("faktorVeza")}: ×1,15`;const G=document.createElement("input");G.type="range",G.min="0.85",G.max="1.40",G.step="0.05",G.value="1.15",G.className="udzbenik-klizac",G.addEventListener("input",()=>{c=Number(G.value),z.textContent=`${ot("faktorVeza")}: ×${c.toFixed(2).replace(".",",")}`,l&&(C(l),n.zatraziRender())}),O.append(z,G),M.append(O)}const T=document.createElement("span");if(T.className="udzbenik-atom-status",T.setAttribute("aria-live","polite"),a){const O=document.createElement("button");O.type="button",O.className="udzbenik-dugme udzbenik-dugme--malo",O.textContent=ot("sledeciAtom"),O.addEventListener("click",()=>{b.length!==0&&(d=(d+1)%b.length,v(d),n.zatraziRender())}),M.append(O,T)}M.childNodes.length>0&&n.gornjeKontrole.append(M);let b=[],w=null,L=new k,x=1;function v(O){if(O<0||O>=b.length){w=null,y.visible=!1,S.hidden=!0,T.textContent="";return}const z=b[O];w=z.atom;const G=z.mesh.scale.x*1.25;y.position.copy(z.mesh.position),y.scale.setScalar(G),y.visible=!0;const K=`(${z.atom.fx.toFixed(3)}, ${z.atom.fy.toFixed(3)}, ${z.atom.fz.toFixed(3)})`;S.textContent=`${z.atom.simbol} [${z.atom.oznaka}] ${K}`,T.textContent=`${z.atom.simbol} (${z.atom.oznaka}): ${K}`}function R(O){Lt(O),O.clear()}function U(O){n.podnozje.replaceChildren();const z=document.createElement("div");z.className="udzbenik-cpk-legenda",z.setAttribute("aria-label",ot("legendaElemenata"));const G=document.createElement("div");G.className="udzbenik-cpk-stavke";let K=!1;for(const De of O){const X=qs(De),ne=Ys(De,s);s==="jonski"&&ne.koriscenaVrsta==="kovalentni"&&(K=!0);const ue=document.createElement("span");ue.className="udzbenik-cpk-cip";const se=document.createElement("span");se.className="udzbenik-cpk-boja",se.style.backgroundColor=X.bojaHex,se.setAttribute("aria-hidden","true");const ee=ne.koriscenaVrsta==="jonski"&&ne.jon?`${X.simbol} (${ne.jon})`:X.simbol,_e=ne.poluprecnik.toFixed(2).replace(".",","),de=document.createElement("span");de.textContent=`${ee} — ${X.naziv} (r = ${_e} Å)`,ue.append(se,de),G.append(ue)}const $=document.createElement("p");$.className="udzbenik-scena-izvor";const fe=i==="kugle-stapici"?` · ${ot("detekcijaVezaKovalentniOznaka")}${c.toFixed(2).replace(".",",")}`:"";if(s==="jonski"){const De=K?`${Ks.izvor}; ${ot("kovalentnaRezervaOznaka")}: ${$s}`:Ks.izvor;$.textContent=`${ot("poluprecniciJonskiOznaka")} (${ot("izvorPodataka")}: ${De})${fe}`}else $.textContent=`${ot("poluprecniciKovalentniOznaka")} (${ot("izvorPodataka")}: ${$s})${fe}`;z.append(G,$),n.podnozje.append(z)}function C(O){R(f),R(m),R(g),b=[];const z=ks(O.celija),G=t==="supercelija"?2:1,K=wn(G,G,G,z);L=new k(K[0]*.5,K[1]*.5,K[2]*.5);const $=Math.max(O.celija.a*G,O.celija.b*G,O.celija.c*G);x=3.6/Math.max(1,$);const fe=[],De=new Set,X=[];for(const ee of O.atomi){X.includes(ee.simbol)||X.push(ee.simbol);const _e=qs(ee.simbol),de=Ys(ee.simbol,s),Z=(ee.fx%1+1)%1,re=(ee.fy%1+1)%1,ae=(ee.fz%1+1)%1,I=Z<.001?[0,1]:[0],Ie=re<.001?[0,1]:[0],Ce=ae<.001?[0,1]:[0];for(let Re=0;Re<G;Re++)for(let Me=0;Me<G;Me++)for(let ke=0;ke<G;ke++)for(const we of I)for(const D of Ie)for(const E of Ce){const j=Z+Re+we,Q=re+Me+D,ie=ae+ke+E;if(j>G+.001||Q>G+.001||ie>G+.001)continue;const J=`${j.toFixed(3)},${Q.toFixed(3)},${ie.toFixed(3)},${ee.simbol}`;if(De.has(J))continue;De.add(J);const Ae=wn(j,Q,ie,z);fe.push({oznaka:ee.oznaka,simbol:ee.simbol,fx:j,fy:Q,fz:ie,pozicija:new k(Ae[0],Ae[1],Ae[2]),poluprecnikPrikaza:de.poluprecnik,kovalentniPoluprecnik:_e.kovalentniPoluprecnik,bojaHex:_e.bojaHex})}}const ne=new mn(1,20,16),ue=new Map,se=i==="kugle"?.52:.25;for(const ee of fe){let _e=ue.get(ee.simbol);_e||(_e=new ct({color:new ce(ee.bojaHex),roughness:.32,metalness:.1}),ue.set(ee.simbol,_e));const de=new je(ne,_e);de.position.copy(ee.pozicija).sub(L).multiplyScalar(x);const Z=Math.max(.045,ee.poluprecnikPrikaza*se*x);de.scale.setScalar(Z),f.add(de),b.push({mesh:de,atom:ee})}if(i==="kugle-stapici"){const ee=new Zi(1,1,1,10,1),_e=new k(0,1,0),de=Math.max(.035,.09*x);for(let Z=0;Z<fe.length;Z++){const re=fe[Z];for(let ae=Z+1;ae<fe.length;ae++){const I=fe[ae],Ie=re.pozicija.distanceTo(I.pozicija),Ce=(re.kovalentniPoluprecnik+I.kovalentniPoluprecnik)*c;if(Ie>.35&&Ie<=Ce){const Re=b[Z].mesh.position,ke=b[ae].mesh.position.clone().sub(Re),we=ke.length();if(we<1e-4)continue;const D=new je(ee,p.clone());D.position.copy(Re).addScaledVector(ke,.5),D.quaternion.setFromUnitVectors(_e,ke.clone().normalize()),D.scale.set(de,we,de),m.add(D)}}}ee.dispose()}if(r){const ee=[],_e=[[[0,0,0],[1,0,0]],[[1,0,0],[1,1,0]],[[1,1,0],[0,1,0]],[[0,1,0],[0,0,0]],[[0,0,1],[1,0,1]],[[1,0,1],[1,1,1]],[[1,1,1],[0,1,1]],[[0,1,1],[0,0,1]],[[0,0,0],[0,0,1]],[[1,0,0],[1,0,1]],[[1,1,0],[1,1,1]],[[0,1,0],[0,1,1]]];for(let Z=0;Z<G;Z++)for(let re=0;re<G;re++)for(let ae=0;ae<G;ae++)for(const[I,Ie]of _e){const Ce=wn(I[0]+Z,I[1]+re,I[2]+ae,z),Re=wn(Ie[0]+Z,Ie[1]+re,Ie[2]+ae,z),Me=new k(...Ce).sub(L).multiplyScalar(x),ke=new k(...Re).sub(L).multiplyScalar(x);ee.push(Me.x,Me.y,Me.z,ke.x,ke.y,ke.z)}const de=new Ye;de.setAttribute("position",new Ge(ee,3)),g.add(new gt(de,_.clone()))}U(X),d=-1,v(-1)}const P=new Ns,F=new Xe,N=O=>{if(!a||b.length===0)return;const z=n.platno.getBoundingClientRect();if(z.width<=0||z.height<=0)return;F.x=(O.clientX-z.left)/z.width*2-1,F.y=-((O.clientY-z.top)/z.height)*2+1,P.setFromCamera(F,n.kamera);const G=P.intersectObjects(b.map(K=>K.mesh),!1);if(G.length>0){const K=G[0].object,$=b.findIndex(fe=>fe.mesh===K);$!==d&&(d=$,v($),n.zatraziRender())}else d!==-1&&O.pointerType==="mouse"&&(d=-1,v(-1),n.zatraziRender())};return a&&n.platno.addEventListener("pointermove",N),n.api.ucitajStrukturuCif(e.mineral).then(O=>{o||(l=xm(O),C(l),n.zatraziRender())}).catch(O=>{if(o)return;const z=O instanceof el&&O.status===404?ot("strukturaNedostupna"):ot("strukturaNedostupna");n.prikaziRezervu(z)}),{resetuj(){d=-1,v(-1)},osveziTemu(O){_.color.set(O.token("--text-secondary")),p.color.set(O.token("--text-muted")),u.color.set(O.token("--accent"));for(const z of g.children){const G=z;G.material instanceof ht&&G.material.color.set(O.token("--text-secondary"))}for(const z of m.children){const G=z;G.material instanceof ct&&G.material.color.set(O.token("--text-muted"))}},posleRendera(){if(!w||d<0){S.hidden=!0;return}const O=b[d];if(!O)return;O.mesh.updateMatrixWorld(!0);const z=O.mesh.position.clone().applyMatrix4(h.matrixWorld),G=n.projektujU2D(z);if(!G.vidljivo){S.hidden=!0;return}S.hidden=!1,S.style.transform=`translate(-50%, -130%) translate(${G.x.toFixed(1)}px, ${G.y.toFixed(1)}px)`},raspolazi(){o=!0,a&&n.platno.removeEventListener("pointermove",N),Lt(h),_.dispose(),p.dispose(),u.dispose()}}}},Ra=[{kljuc:"kubni",naziv:"Кубни",kratko:"Кубни",odnosIvica:"a = b = c",odnosUglova:"α = β = γ = 90°",reprezentativniOblik:"коцка",celija:{a:1.15,b:1.15,c:1.15,alpha:90,beta:90,gamma:90}},{kljuc:"tetragonalni",naziv:"Тетрагонални",kratko:"Тетраг.",odnosIvica:"a = b ≠ c",odnosUglova:"α = β = γ = 90°",reprezentativniOblik:"тетрагонална призма",celija:{a:1,b:1,c:1.62,alpha:90,beta:90,gamma:90}},{kljuc:"ortorombicni",naziv:"Орторомбични",kratko:"Орторомб.",odnosIvica:"a ≠ b ≠ c",odnosUglova:"α = β = γ = 90°",reprezentativniOblik:"правоугаона призма („цигла“)",celija:{a:.85,b:1.22,c:1.58,alpha:90,beta:90,gamma:90}},{kljuc:"heksagonalni",naziv:"Хексагонални",kratko:"Хексаг.",odnosIvica:"a = b ≠ c",odnosUglova:"α = β = 90°, γ = 120°",reprezentativniOblik:"хексагонална призма",celija:{a:1.08,b:1.08,c:1.55,alpha:90,beta:90,gamma:120}},{kljuc:"trigonalni",naziv:"Тригонални",kratko:"Тригон.",odnosIvica:"a = b = c (ромбоедарска) / a = b ≠ c (хексагонална)",odnosUglova:"α = β = γ ≠ 90° (ромб.) / α = β = 90°, γ = 120° (хекс.)",reprezentativniOblik:"ромбоедар (у кристалографији се стандардно описује и хексагоналном поставком)",celija:{a:1.18,b:1.18,c:1.18,alpha:75,beta:75,gamma:75}},{kljuc:"monoklinicni",naziv:"Моноклинични",kratko:"Монокл.",odnosIvica:"a ≠ b ≠ c",odnosUglova:"α = γ = 90°, β ≠ 90°",reprezentativniOblik:"кос паралелопипед (β ≠ 90°)",celija:{a:.92,b:1.22,c:1.48,alpha:90,beta:112,gamma:90}},{kljuc:"triklinicni",naziv:"Триклинични",kratko:"Трикл.",odnosIvica:"a ≠ b ≠ c",odnosUglova:"α ≠ β ≠ γ ≠ 90°",reprezentativniOblik:"кос паралелопипед (α, β, γ ≠ 90°)",celija:{a:.88,b:1.18,c:1.46,alpha:78,beta:109,gamma:103}}],Pm={a:1.15,b:1.15,c:1.15,alpha:90,beta:90,gamma:90};function Dm(n,e,t){const i=Math.max(0,Math.min(1,t));return{a:n.a+(e.a-n.a)*i,b:n.b+(e.b-n.b)*i,c:n.c+(e.c-n.c)*i,alpha:n.alpha+(e.alpha-n.alpha)*i,beta:n.beta+(e.beta-n.beta)*i,gamma:n.gamma+(e.gamma-n.gamma)*i}}function Wc(n){const e=ks(n),t=new k(...e.va),i=new k(...e.vb),r=new k(...e.vc),a=t.clone().add(i).add(r).multiplyScalar(.5),s=[],o=[[0,0,0],[1,0,0],[1,1,0],[0,1,0],[0,0,1],[1,0,1],[1,1,1],[0,1,1]];for(const[g,_,p]of o){const u=wn(g,_,p,e);s.push(new k(u[0]-a.x,u[1]-a.y,u[2]-a.z))}const c=[[0,1],[1,2],[2,3],[3,0],[4,5],[5,6],[6,7],[7,4],[0,4],[1,5],[2,6],[3,7]],l=[];for(const[g,_]of c){const p=s[g],u=s[_];l.push(p.x,p.y,p.z,u.x,u.y,u.z)}const d=new Ye;d.setAttribute("position",new Ge(l,3));const h=[[0,3,2,1],[4,5,6,7],[0,1,5,4],[2,3,7,6],[1,2,6,5],[3,0,4,7]],f=[];for(const[g,_,p,u]of h){const y=s[g],S=s[_],M=s[p],T=s[u];f.push(y.x,y.y,y.z,S.x,S.y,S.z,M.x,M.y,M.z,y.x,y.y,y.z,M.x,M.y,M.z,T.x,T.y,T.z)}const m=new Ye;return m.setAttribute("position",new Ge(f,3)),m.computeVertexNormals(),{ivice:d,mreza:m,poreklo:s[0],va:t,vb:i,vc:r}}function Ca(n,e,t,i){const r=e.clone().normalize(),a=t.clone().normalize(),s=18,o=[];let c=n.clone();for(let d=0;d<=s;d++){const h=d/s,f=r.clone().multiplyScalar(1-h).addScaledVector(a,h).normalize(),m=n.clone().addScaledVector(f,i);if(d===Math.floor(s/2)&&(c=n.clone().addScaledVector(f,i*1.38)),d>0){const g=(d-1)/s,_=r.clone().multiplyScalar(1-g).addScaledVector(a,g).normalize(),p=n.clone().addScaledVector(_,i);o.push(p.x,p.y,p.z,m.x,m.y,m.z)}}const l=new Ye;return l.setAttribute("position",new Ge(o,3)),{geometrija:l,sredina:c}}function Lm(n,e,t){if(n==="heksagonalni"){const s=.58+.22*t,o=1.35-(1.35-.68)*t,c=[{normala:[0,1,0],d:s},{normala:[0,-1,0],d:s},{normala:[1,0,0],d:.68},{normala:[-1,0,0],d:.68},{normala:[0,0,1],d:.68+.14*t},{normala:[0,0,-1],d:.68+.14*t},{normala:[.5,0,Math.sqrt(3)/2],d:o},{normala:[-.5,0,Math.sqrt(3)/2],d:o},{normala:[.5,0,-Math.sqrt(3)/2],d:o},{normala:[-.5,0,-Math.sqrt(3)/2],d:o}],l=[{normala:[0,1,0],d:s},{normala:[0,-1,0],d:s}];if(t>.85){for(let g=0;g<6;g++){const _=g*Math.PI/3;l.push({normala:[Math.cos(_),0,Math.sin(_)],d:.68})}const f=Wi(l),m=Xi(f);return{mreza:m.geometrijaMreze,ivice:m.geometrijaIvica}}const d=Wi(c),h=Xi(d);return{mreza:h.geometrijaMreze,ivice:h.geometrijaIvica}}const i={a:e.a*.92,b:e.b*.92,c:e.c*.92,alpha:e.alpha,beta:e.beta,gamma:e.gamma},r=Wc(i);return{mreza:r.mreza,ivice:r.ivice}}const Im={imaPodrazumevanuAnimaciju(n){return(n.animacija??"rotacija")!=="nema"},pocetnaKamera(){return{theta:.42,phi:1.15,udaljenost:6.8}},kreiraj(n,e){const t=e.animacija??"rotacija",i=e.prikazi_ose??!0,r=e.prikazi_celiju??!0;let a=e.sistem==="svi"?"heksagonalni":e.sistem;e.sistem==="svi"&&(a="kubni");let s=n.smanjenPokret||t!=="uporedi"?1:0,o=0;const c=new nt,l=new nt,d=new nt;r?(l.position.set(-1.55,-.05,0),d.position.set(1.55,-.05,0)):d.position.set(0,-.05,0),c.add(l,d),n.scena3D.add(c);const h=new ct({color:new ce(n.tema.token("--primary")),transparent:!0,opacity:.14,roughness:.45,metalness:.05,side:mt,depthWrite:!1}),f=new ht({color:new ce(n.tema.token("--text-secondary"))}),m=new ht({color:new ce(n.tema.token("--danger"))}),g=new ht({color:new ce(n.tema.token("--success"))}),_=new ht({color:new ce(n.tema.token("--accent"))}),p=new ht({color:new ce(n.tema.token("--warning"))}),u=new ct({color:new ce(n.tema.token("--primary")),transparent:!0,opacity:.78,roughness:.35,metalness:.08,flatShading:!0}),y=new ht({color:new ce(n.tema.token("--text-primary"))}),S=["a","b","c","α","β","γ"],M=new Map,T=new Map;if(i&&r)for(const P of S){const F=document.createElement("span");F.className="udzbenik-scena-etiketa",F.textContent=P,n.slojEtiketa.append(F),M.set(P,F),T.set(P,new k)}const b=document.createElement("div");b.className="udzbenik-scena-info-red",n.podnozje.append(b);const w=new Map;if(e.sistem==="svi"){const P=document.createElement("div");P.className="udzbenik-sistemi-traka",P.setAttribute("role","group"),P.setAttribute("aria-label",ot("izaberiKristalniSistem"));for(const F of Ra){const N=document.createElement("button");N.type="button",N.className="udzbenik-sistem-kartica",N.dataset.sistem=F.kljuc,N.setAttribute("aria-pressed",String(F.kljuc===a));const O=document.createElement("span");O.className="udzbenik-sistem-kartica-naslov",O.textContent=F.naziv;const z=document.createElement("span");z.className="udzbenik-sistem-kartica-meta",z.textContent=`${F.odnosIvica} · ${F.odnosUglova}`,N.append(O,z),N.addEventListener("click",()=>{a=F.kljuc,s=n.smanjenPokret||t!=="uporedi"?1:0,L(),U(),n.zatraziRender()}),w.set(F.kljuc,N),P.append(N)}n.gornjeKontrole.append(P)}function L(){for(const[P,F]of w.entries()){const N=P===a;F.classList.toggle("udzbenik-sistem-kartica--aktivna",N),F.setAttribute("aria-pressed",String(N))}}function x(){return Ra.find(P=>P.kljuc===a)??Ra[0]}function v(P){for(const F of P.children){const N=F.geometry;N&&N.dispose()}P.clear()}function R(){if(t!=="uporedi"||a==="kubni")return 1;const P=s%1;if(P<.4){const F=P/.4;return F*F*(3-2*F)}if(P<.72)return 1;if(P<.92){const F=(P-.72)/.2;return 1-F*F*(3-2*F)}return 0}function U(){const P=x(),F=R(),N=Dm(Pm,P.celija,F);if(v(l),v(d),r){const $=Wc(N),fe=new je($.mreza,h),De=new gt($.ivice,f);if(l.add(fe,De),i){const X=$.poreklo,ne=X.clone().addScaledVector($.va,1.16),ue=X.clone().addScaledVector($.vb,1.16),se=X.clone().addScaledVector($.vc,1.16),ee=new Ye().setFromPoints([X,ne]),_e=new Ye().setFromPoints([X,ue]),de=new Ye().setFromPoints([X,se]);l.add(new Gi(ee,m),new Gi(_e,g),new Gi(de,_));const Z=Ca(X,$.vb,$.vc,.36),re=Ca(X,$.va,$.vc,.44),ae=Ca(X,$.va,$.vb,.36);l.add(new gt(Z.geometrija,p),new gt(re.geometrija,p),new gt(ae.geometrija,p)),T.get("a")?.copy(ne),T.get("b")?.copy(ue),T.get("c")?.copy(se),T.get("α")?.copy(Z.sredina),T.get("β")?.copy(re.sredina),T.get("γ")?.copy(ae.sredina)}}const O=Lm(P.kljuc,N,F);d.add(new je(O.mreza,u),new gt(O.ivice,y)),b.replaceChildren();const z=document.createElement("strong");z.textContent=`${P.naziv}: `;const G=document.createElement("span"),K=P.kljuc==="trigonalni"?" • Стандардна кристалографска поставка за тригоналне минерале (кварц, калцит) је хексагонална (a = b ≠ c, γ = 120°).":"";G.textContent=`${P.odnosIvica} · ${P.odnosUglova} — облик: ${P.reprezentativniOblik}${K}`,b.append(z,G)}function C(){if(!i||!r)return;l.updateMatrixWorld(!0);const P=x();for(const[F,N]of M.entries()){const O=T.get(F);if(!O)continue;const z=O.clone().applyMatrix4(l.matrixWorld),G=n.projektujU2D(z);if(!G.vidljivo){N.hidden=!0;continue}N.hidden=!1,N.style.transform=`translate(-50%, -50%) translate(${G.x.toFixed(1)}px, ${G.y.toFixed(1)}px)`;const K=F==="c"&&P.celija.c!==P.celija.a||F==="b"&&P.celija.b!==P.celija.a||F==="α"&&P.celija.alpha!==90||F==="β"&&P.celija.beta!==90||F==="γ"&&P.celija.gamma!==90;N.classList.toggle("udzbenik-scena-etiketa--istaknuta",K)}}return L(),U(),{azuriraj(P){t==="uporedi"?(s=(s+P*.18)%1,o+=P*.22,c.rotation.y=Math.sin(o)*.18,U()):t==="rotacija"&&(c.rotation.y+=P*.45)},korak(){t==="uporedi"?(s=(s+.15)%1,o+=.45,c.rotation.y=Math.sin(o)*.18,U()):c.rotation.y+=.35},resetuj(){c.rotation.set(0,0,0),o=0,s=n.smanjenPokret||t!=="uporedi"?1:0,U()},osveziTemu(P){h.color.set(P.token("--primary")),f.color.set(P.token("--text-secondary")),m.color.set(P.token("--danger")),g.color.set(P.token("--success")),_.color.set(P.token("--accent")),p.color.set(P.token("--warning")),u.color.set(P.token("--primary")),y.color.set(P.token("--text-primary"))},posleRendera(){C()},raspolazi(){Lt(c),h.dispose(),f.dispose(),m.dispose(),g.dispose(),_.dispose(),p.dispose(),u.dispose(),y.dispose()}}}},qt="Klein, C. & Dutrow, B. (2007), Manual of Mineral Science (23rd ed.), John Wiley & Sons, Table 2.3 (Knoop microhardness HK, kgf/mm²; теренске пробе: нокат ~2,5, бакарни новчић ~3, нож/стакло ~5,5, турпија ~6,5).",yn=[{mohs:1,kljuc:"talk",naziv:"Талк",formula:"Mg₃Si₄O₁₀(OH)₂",apsolutnaKnoop:1,izvor:qt},{mohs:2,kljuc:"gips",naziv:"Гипс",formula:"CaSO₄·2H₂O",apsolutnaKnoop:32,izvor:qt},{mohs:3,kljuc:"kalcit",naziv:"Калцит",formula:"CaCO₃",apsolutnaKnoop:135,izvor:qt},{mohs:4,kljuc:"fluorit",naziv:"Флуорит",formula:"CaF₂",apsolutnaKnoop:163,izvor:qt},{mohs:5,kljuc:"apatit",naziv:"Апатит",formula:"Ca₅(PO₄)₃(F,Cl,OH)",apsolutnaKnoop:430,izvor:qt},{mohs:6,kljuc:"ortoklas",naziv:"Ортоклас",formula:"KAlSi₃O₈",apsolutnaKnoop:560,izvor:qt},{mohs:7,kljuc:"kvarc",naziv:"Кварц",formula:"SiO₂",apsolutnaKnoop:820,izvor:qt},{mohs:8,kljuc:"topaz",naziv:"Топаз",formula:"Al₂SiO₄(F,OH)₂",apsolutnaKnoop:1340,izvor:qt},{mohs:9,kljuc:"korund",naziv:"Корунд",formula:"Al₂O₃",apsolutnaKnoop:2100,izvor:qt},{mohs:10,kljuc:"dijamant",naziv:"Дијамант",formula:"C",apsolutnaKnoop:7e3,izvor:qt}],Um=[{naziv:"Нокат (~2,5)",mohs:2.5},{naziv:"Бакарни новчић (~3)",mohs:3},{naziv:"Нож / стакло (~5,5)",mohs:5.5},{naziv:"Челична турпија (~6,5)",mohs:6.5}];function uc(n,e){if(!e||e.length===0)return!1;const t=n.kljuc.toLowerCase(),i=n.naziv.toLowerCase();return e.some(r=>{const a=r.trim().toLowerCase();return a===t||a===i})}const zm={imaPodrazumevanuAnimaciju(){return!0},pocetnaKamera(){return{theta:.16,phi:1.18,udaljenost:8.6}},kreiraj(n,e){const t=e.prikazi_apsolutnu??!1,i=e.prikazi_terenske_probe??!0,r=e.istaknuti??[];let a=!1,s=0,o=6,c=5,l=n.smanjenPokret?.65:0;const d=new nt;d.position.set(0,-.35,0),n.scena3D.add(d);const h=-4.05,f=.9,m=-.7,g=2.75,_=new ct({color:new ce(n.tema.token("--bg-elevated")),roughness:.7,metalness:.05}),p=new je(new hn(9.6,.14,1.4),_);p.position.set(0,m-.07,-.35),d.add(p);const u=[],y=new ht({color:new ce(n.tema.token("--text-primary"))}),S=new hn(.66,1,.66),M=new Br(S);for(let Z=0;Z<yn.length;Z++){const re=yn[Z],ae=uc(re,r),I=new ce(n.tema.token(ae?"--accent":"--primary")),Ie=new ct({color:I,emissive:ae?new ce(n.tema.token("--accent")).multiplyScalar(.22):new ce(0,0,0),roughness:.35,metalness:.12}),Ce=new je(S,Ie),Re=new gt(M,y),Me=h+Z*f;Ce.position.set(Me,m+.5,-.35),Re.position.copy(Ce.position),d.add(Ce,Re);const ke=document.createElement("span");ke.className="udzbenik-scena-etiketa udzbenik-scena-etiketa--mala",ae&&ke.classList.add("udzbenik-scena-etiketa--istaknuta"),ke.textContent=`${re.mohs}`,n.slojEtiketa.append(ke),u.push({mineral:re,istaknut:ae,mesh:Ce,ivice:Re,mat:Ie,etiketaDom:ke})}const T=new ct({color:new ce(n.tema.token("--warning")),roughness:.4}),b=[];if(i){const Z=new Zi(.035,.035,.65,8);for(const re of Um){const ae=h+(re.mohs-1)*f,I=new je(Z,T);I.position.set(ae,m+.32,.18),d.add(I);const Ie=document.createElement("span");Ie.className="udzbenik-scena-etiketa udzbenik-scena-etiketa--proba",Ie.textContent=re.naziv,n.slojEtiketa.append(Ie),b.push({x:ae,tekst:re.naziv,dom:Ie,stub:I})}}const w=new nt;w.position.set(0,m-.52,1.35),d.add(w);const L=new ct({color:new ce(n.tema.token("--primary-light")),roughness:.45,metalness:.08}),x=new je(new hn(3.4,.24,.92),L),v=new gt(new Br(x.geometry),y);w.add(x,v);const R=new ct({color:new ce(n.tema.token("--danger")),roughness:.85}),U=new je(new hn(1,.05,.11),R);U.position.set(-1.1,.125,0),U.visible=!1,w.add(U);const C=new ct({color:new ce(n.tema.token("--accent")),roughness:.25,metalness:.2}),P=new je(new Us(.22,.72,6),C);P.rotation.x=Math.PI,P.rotation.z=-.22,P.position.set(-1.1,.5,0),w.add(P);const F=document.createElement("div");F.className="udzbenik-mohs-kontrole";const N=document.createElement("div");N.className="udzbenik-mohs-dugmad",N.setAttribute("role","group"),N.setAttribute("aria-label",ot("ordinalnaTvrdocaOznaka"));const O=[];for(let Z=0;Z<yn.length;Z++){const re=yn[Z],ae=document.createElement("button");ae.type="button",ae.className="udzbenik-mohs-cip",uc(re,r)&&ae.classList.add("udzbenik-mohs-cip--istaknut"),ae.textContent=`${re.mohs}. ${re.naziv}`,ae.addEventListener("click",()=>{De(Z)}),O.push(ae),N.append(ae)}F.append(N);const z=document.createElement("div");z.className="udzbenik-mohs-akcije";const G=document.createElement("button");G.type="button",G.className="udzbenik-dugme udzbenik-dugme--malo",G.textContent=ot("zameniMinerale"),G.addEventListener("click",()=>{const Z=o;o=c,c=Z,l=n.smanjenPokret?.75:0,se(),n.zatraziRender()}),z.append(G);let K=null;t&&(K=document.createElement("button"),K.type="button",K.className="udzbenik-dugme udzbenik-dugme--malo udzbenik-dugme--preklopnik",K.setAttribute("role","switch"),K.setAttribute("aria-checked","false"),K.textContent=ot("apsolutnaTvrdocaPreklopnik"),K.addEventListener("click",()=>{a=!a,K?.setAttribute("aria-checked",String(a)),K?.classList.toggle("udzbenik-dugme--aktivno",a),n.smanjenPokret&&(s=a?1:0,ne()),se(),n.zatraziRender()}),z.append(K)),F.append(z),n.gornjeKontrole.append(F);const $=document.createElement("p");$.className="udzbenik-scena-info-red",$.setAttribute("aria-live","polite");const fe=document.createElement("p");fe.className="udzbenik-scena-izvor",fe.textContent=`${ot("izvorPodataka")}: ${qt}`,n.podnozje.append($,fe);function De(Z){Z===o?c=Z<9?Z+1:Z-1:(o=Z,c=Z>0?Z-1:1),l=n.smanjenPokret?.75:0,se(),n.zatraziRender()}function X(Z,re){const ae=Z.mohs/10*g,I=Math.max(.08,Z.apsolutnaKnoop/7e3*g);return ae+(I-ae)*re}function ne(){for(let Z=0;Z<u.length;Z++){const re=u[Z],ae=X(re.mineral,s);re.mesh.scale.y=ae,re.mesh.position.y=m+ae*.5,re.ivice.scale.y=ae,re.ivice.position.copy(re.mesh.position);const I=Z===o,Ie=Z===c,Ce=I?"--accent":Ie?"--warning":re.istaknut?"--accent":"--primary",Re=new ce(n.tema.token(Ce));!I&&!Ie&&!re.istaknut&&Re.lerp(new ce(n.tema.token("--bg-elevated")),.25),re.mat.color.copy(Re),re.etiketaDom.textContent=a?`${re.mineral.mohs} (${re.mineral.apsolutnaKnoop})`:`${re.mineral.mohs}`}}function ue(){const Z=yn[o],re=yn[c],ae=Z.mohs>re.mohs,I=Math.min(1,l/.75),Ie=-1.15,Re=Ie+(1.15-Ie)*I;if(P.position.x=Re,P.position.y=ae?.44:.5,ae&&I>.03){const Me=Math.max(.05,Re-Ie);U.visible=!0,U.scale.x=Me,U.position.x=Ie+Me*.5}else U.visible=!1}function se(){for(let Ie=0;Ie<O.length;Ie++){const Ce=O[Ie],Re=Ie===o;Ce.classList.toggle("udzbenik-mohs-cip--aktivan",Re),Ce.setAttribute("aria-pressed",String(Re))}const Z=yn[o],re=yn[c],I=Z.mohs>re.mohs?`${ot("probaGrebanja")}: ${Z.naziv} (${Z.mohs}, HK ${Z.apsolutnaKnoop}) је тврђи и оставља бразду на минералу ${re.naziv} (${re.mohs}, HK ${re.apsolutnaKnoop}).`:`${ot("probaGrebanja")}: ${Z.naziv} (${Z.mohs}, HK ${Z.apsolutnaKnoop}) је мекши и НЕ оставља бразду на минералу ${re.naziv} (${re.mohs}, HK ${re.apsolutnaKnoop}).`;$.textContent=I,ne(),ue()}const ee=new Ns,_e=new Xe,de=Z=>{const re=n.platno.getBoundingClientRect();if(re.width<=0||re.height<=0)return;_e.x=(Z.clientX-re.left)/re.width*2-1,_e.y=-((Z.clientY-re.top)/re.height)*2+1,ee.setFromCamera(_e,n.kamera);const ae=ee.intersectObjects(u.map(I=>I.mesh),!1);if(ae.length>0){const I=ae[0].object,Ie=u.findIndex(Ce=>Ce.mesh===I);Ie!==-1&&De(Ie)}};return n.platno.addEventListener("click",de),se(),{azuriraj(Z){const re=a?1:0;Math.abs(s-re)>.002?(s+=(re-s)*Math.min(1,Z*6),ne()):s!==re&&(s=re,ne()),l=(l+Z*.42)%1,ue()},korak(){l=(l+.2)%1,s=a?1:0,ne(),ue()},resetuj(){a=!1,s=0,K&&(K.setAttribute("aria-checked","false"),K.classList.remove("udzbenik-dugme--aktivno")),o=6,c=5,l=n.smanjenPokret?.75:0,se()},osveziTemu(Z){_.color.set(Z.token("--bg-elevated")),y.color.set(Z.token("--text-primary")),T.color.set(Z.token("--warning")),L.color.set(Z.token("--primary-light")),R.color.set(Z.token("--danger")),C.color.set(Z.token("--accent")),ne()},posleRendera(){d.updateMatrixWorld(!0);for(const Z of u){const re=Z.mesh.position.clone().add(new k(0,Z.mesh.scale.y*.5+.22,0)).applyMatrix4(d.matrixWorld),ae=n.projektujU2D(re);Z.etiketaDom.hidden=!ae.vidljivo,ae.vidljivo&&(Z.etiketaDom.style.transform=`translate(-50%, -50%) translate(${ae.x.toFixed(1)}px, ${ae.y.toFixed(1)}px)`)}for(const Z of b){const re=new k(Z.x,m-.22,.35).applyMatrix4(d.matrixWorld),ae=n.projektujU2D(re);Z.dom.hidden=!ae.vidljivo,ae.vidljivo&&(Z.dom.style.transform=`translate(-50%, 0%) translate(${ae.x.toFixed(1)}px, ${ae.y.toFixed(1)}px)`)}},raspolazi(){n.platno.removeEventListener("click",de),Lt(d),S.dispose(),M.dispose(),_.dispose(),y.dispose(),T.dispose(),L.dispose(),R.dispose(),C.dispose();for(const Z of u)Z.mat.dispose()}}}};function Nm(n,e,t){const i=1/(n*n),r=1/(e*e),a=1/(t*t),s=(i-r)/Math.max(1e-12,r-a),c=2*Math.atan(Math.sqrt(Math.max(0,s)))*180/Math.PI;return c<=90?{dvaV:c,dvaVZ:c,znak:"+",bisektrisaOstra:"Z (γ)"}:{dvaV:180-c,dvaVZ:c,znak:"-",bisektrisaOstra:"X (α)"}}function dc(n,e,t){const i=Math.hypot(...t),r=i>0?t[0]/i:0,a=i>0?t[1]/i:0,s=i>0?t[2]/i:1;if(n==="izotropna"){const C=e[0]??1.5;return{n1:C,n2:C,delta:0}}if(n==="jednoosna"){const C=e[0]??1.544,P=e[1]??1.553,F=s*s,N=Math.max(0,1-F),O=F/(C*C)+N/(P*P),z=Math.sqrt(1/Math.max(1e-12,O)),G=Math.abs(z-C);return{n1:Math.min(C,z),n2:Math.max(C,z),delta:G}}const o=e[0]??1.52,c=e[1]??1.53,l=e[2]??1.55,d=1/(o*o),h=1/(c*c),f=1/(l*l);let m,g,_,p;if(Math.abs(h-f)>1e-7&&d>=h&&h>=f){const C=Nm(o,c,l);m=C.dvaV,g=C.dvaVZ,_=C.znak,p=C.bisektrisaOstra}const u=r*r,y=a*a,S=s*s,M=1,T=-(u*(h+f)+y*(d+f)+S*(d+h)),b=u*h*f+y*d*f+S*d*h,w=Math.max(0,T*T-4*M*b),L=(-T-Math.sqrt(w))/(2*M),x=(-T+Math.sqrt(w))/(2*M),v=Math.sqrt(1/Math.max(1e-12,x)),R=Math.sqrt(1/Math.max(1e-12,L)),U=Math.abs(R-v);return{n1:v,n2:R,delta:U,ugao2V:m,ugao2VZ:g,optickiZnak:_,bisektrisaOstra:p}}const Fm={imaPodrazumevanuAnimaciju(){return!0},pocetnaKamera(){return{theta:.72,phi:1.18,udaljenost:5.6}},kreiraj(n,e){const t=new nt;n.scena3D.add(t);const i=e.tip,r=e.n&&e.n.length>0?e.n:i==="izotropna"?[1.5]:i==="jednoosna"?[1.658,1.486]:[1.52,1.53,1.55];let a=1.6,s=1.6,o=1.6;if(i==="jednoosna"){const U=r[0],C=r[1]??r[0];a=1.6,s=1.6,o=1.6*(C>=U?1.35:.72)}else i==="dvoosna"&&(a=1.25,s=1.65,o=2.15);const c=new mn(1,48,36);c.scale(a,s,o);const l=new ct({color:new ce(n.tema.token("--primary")),transparent:!0,opacity:.42,roughness:.25,metalness:.1,side:mt}),d=new je(c,l);t.add(d);const h=new ht({color:new ce(n.tema.token("--text-secondary"))}),f=new Ye,m=[-a*1.3,0,0,a*1.3,0,0,0,-s*1.3,0,0,s*1.3,0,0,0,-o*1.3,0,0,o*1.3];f.setAttribute("position",new Ge(m,3)),t.add(new gt(f,h));const g=new ht({color:new ce(n.tema.token("--accent")),linewidth:3});if(e.prikazi_opticke_ose!==!1){const U=[];if(i==="jednoosna")U.push(0,0,-o*1.45,0,0,o*1.45);else if(i==="dvoosna"){const P=(dc(i,r,[0,0,1]).ugao2V??50)/2*(Math.PI/180),F=o*1.4,N=F*Math.sin(P),O=F*Math.cos(P);U.push(-N,0,-O,N,0,O),U.push(N,0,-O,-N,0,O)}if(U.length>0){const C=new Ye;C.setAttribute("position",new Ge(U,3)),t.add(new gt(C,g))}}const _=new nt;t.add(_);const p=new Di({color:new ce(n.tema.token("--warning")),transparent:!0,opacity:.35,side:mt}),u=new zs(0,2.2,48),y=new je(u,p);_.add(y);const S=new ht({color:new ce(n.tema.token("--danger"))}),M=new Ye;M.setAttribute("position",new Ge([0,0,-2.6,0,0,2.6],3)),_.add(new gt(M,S));const T=document.createElement("div");T.className="udzbenik-scena-status",n.podnozje.append(T);const b=document.createElement("small");b.className="udzbenik-scena-napomena",b.style.display="block",b.textContent="Напомена: Разлике индекса преламања су преувеличане ради јаснијег 3D приказа.",n.podnozje.append(b);let w=.5,L=.3;function x(){_.rotation.set(w,L,0);const U=new k(0,0,1).applyEuler(_.rotation),C=dc(i,r,[U.x,U.y,U.z]),P=C.delta.toFixed(4),F=e.mineral?` (${e.mineral})`:"",N=C.ugao2V!==void 0?` • 2V = ${C.ugao2V.toFixed(1)}° (${C.optickiZnak}, Bxa = ${C.bisektrisaOstra})`:"";T.textContent=`Тип: ${i}${F} • n'₁ = ${C.n1.toFixed(3)}, n'₂ = ${C.n2.toFixed(3)} • δ = ${P}${N}`}x();function v(){l.color.set(n.tema.token("--primary")),h.color.set(n.tema.token("--text-secondary")),g.color.set(n.tema.token("--accent")),p.color.set(n.tema.token("--warning")),S.color.set(n.tema.token("--danger"))}let R=0;return{azuriraj(U){R+=U*.35,L=Math.sin(R)*1.1,w=Math.cos(R*.7)*.7,x()},korak(){R+=.25,L+=.2,x()},resetuj(){R=0,w=.5,L=.3,x()},osveziTemu(){v()},raspolazi(){c.dispose(),l.dispose(),f.dispose(),h.dispose(),g.dispose(),u.dispose(),p.dispose(),M.dispose(),S.dispose(),Lt(t),T.remove(),b.remove()}}}},Pa={nezo:{klasa:"nezo",naziv:"Незосиликати (изоловани tetraedri)",odnosSiO:"1 : 4 (SiO₄⁴⁻)",zajednickiKiseonici:"0",primeri:"оливин, гранат, циркон"},soro:{klasa:"soro",naziv:"Соросиликати (парови tetraedara)",odnosSiO:"2 : 7 (Si₂O₇⁶⁻)",zajednickiKiseonici:"1",primeri:"епидот, хемиморфит"},"ciklo-3":{klasa:"ciklo-3",naziv:"Циклосиликати (трочлани прстен)",odnosSiO:"1 : 3 (Si₃O₉⁶⁻)",zajednickiKiseonici:"2",primeri:"бенитоит"},"ciklo-6":{klasa:"ciklo-6",naziv:"Циклосиликати (шесточлани прстен)",odnosSiO:"1 : 3 (Si₆O₁₈¹²⁻)",zajednickiKiseonici:"2",primeri:"берил, турмалин"},"ino-jednostruki":{klasa:"ino-jednostruki",naziv:"Иносиликати (једноструки ланци)",odnosSiO:"1 : 3 (Si₂O₆⁴⁻)",zajednickiKiseonici:"2",primeri:"пироксени (диопсид, енстатит)"},"ino-dvostruki":{klasa:"ino-dvostruki",naziv:"Иносиликати (двоструки ланци)",odnosSiO:"4 : 11 (Si₄O₁₁⁶⁻)",zajednickiKiseonici:"2 и 3 (просек 2,5)",primeri:"амфиболи (тремолит, хорнбленда)"},filo:{klasa:"filo",naziv:"Филосиликати (слојевити)",odnosSiO:"2 : 5 (Si₄O₁₀⁴⁻)",zajednickiKiseonici:"3",primeri:"лискуни (мусковит, биотит), талк, каолинит"},tekto:{klasa:"tekto",naziv:"Тектосиликати (просторна мрежа)",odnosSiO:"1 : 2 (SiO₂)",zajednickiKiseonici:"4",primeri:"кварц, фелдспати, зеолити"},sve:{klasa:"sve",naziv:"Преглед свих класа",odnosSiO:"од 1:4 до 1:2",zajednickiKiseonici:"0 до 4",primeri:"полимеризација од незо- до тектосиликата"}};function km(){const e=.65*Math.SQRT2,t=[0,0,0],i=[-e,.65,0],r=[-e,-.5*.65,Math.sqrt(3)/2*.65],a=[-e,-.5*.65,-(Math.sqrt(3)/2)*.65],s=[e,-.65,0],o=[e,.5*.65,-(Math.sqrt(3)/2)*.65],c=[e,.5*.65,Math.sqrt(3)/2*.65];return{vrhoviLevi:[t,i,r,a],vrhoviDesni:[t,s,o,c],svih7Kiseonika:[t,i,r,a,s,o,c]}}function bn(n,e,t,i,r,a){const s=new nt;s.position.copy(n),s.rotation.copy(e);const o=.55,c=[[o,o,o],[o,-o,-o],[-o,o,-o],[-o,-o,o]];if(a==="tetraedri"||a==="oba"){const l=new Ye,d=[...c[0],...c[1],...c[2],...c[0],...c[3],...c[1],...c[0],...c[2],...c[3],...c[1],...c[3],...c[2]];l.setAttribute("position",new Ge(d,3)),l.computeVertexNormals();const h=new je(l,t);s.add(h)}if(a==="kugle"||a==="oba")for(const l of c){const d=new je(r,i);d.position.set(l[0],l[1],l[2]),s.add(d)}return s}const Om={imaPodrazumevanuAnimaciju(n){return(n.animacija??"rotacija")!=="nema"},pocetnaKamera(){return{theta:.65,phi:1.15,udaljenost:6.2}},kreiraj(n,e){let t=e.klasa==="sve"?"nezo":e.klasa;const i=e.prikaz??"tetraedri",r=new nt;n.scena3D.add(r);const a=new mn(.18,16,16),s=new ct({color:new ce(n.tema.token("--primary")),transparent:!0,opacity:.65,roughness:.25,metalness:.1,side:mt}),o=new ct({color:new ce(n.tema.token("--accent")),roughness:.25,metalness:.2}),c=document.createElement("div");c.className="udzbenik-scena-status",n.podnozje.append(c);function l(_){for(;r.children.length>0;){const u=r.children[0];r.remove(u),Lt(u)}const p=Pa[_]??Pa.nezo;if(c.textContent=`${p.naziv} • Si:O = ${p.odnosSiO} • Заједнички O: ${p.zajednickiKiseonici} (${p.primeri})`,_==="nezo")r.add(bn(new k(0,0,0),new Mt(0,0,0),s,o,a,i));else if(_==="soro"){const{vrhoviLevi:u,vrhoviDesni:y,svih7Kiseonika:S}=km(),[M,T,b,w]=u,[,L,x,v]=y;if(i==="tetraedri"||i==="oba"){const R=new Ye,U=[...M,...T,...b,...M,...b,...w,...M,...w,...T,...T,...w,...b,...M,...x,...L,...M,...v,...x,...M,...L,...v,...L,...x,...v];R.setAttribute("position",new Ge(U,3)),R.computeVertexNormals(),r.add(new je(R,s))}if(i==="kugle"||i==="oba")for(const R of S){const U=new je(a,o);U.position.set(R[0],R[1],R[2]),r.add(U)}}else if(_==="ciklo-3")for(let u=0;u<3;u++){const y=u*2*Math.PI/3,S=new k(Math.cos(y)*.95,Math.sin(y)*.95,0);r.add(bn(S,new Mt(0,0,y),s,o,a,i))}else if(_==="ciklo-6")for(let u=0;u<6;u++){const y=u*2*Math.PI/6,S=new k(Math.cos(y)*1.5,Math.sin(y)*1.5,0);r.add(bn(S,new Mt(0,0,y),s,o,a,i))}else if(_==="ino-jednostruki")for(let u=-2;u<=2;u++){const y=u%2===0?0:Math.PI;r.add(bn(new k(u*.9,u%2*.2,0),new Mt(0,0,y),s,o,a,i))}else if(_==="ino-dvostruki")for(let u=-2;u<=2;u++){const y=u%2===0?0:Math.PI;r.add(bn(new k(u*.9,.45+u%2*.15,0),new Mt(0,0,y),s,o,a,i)),r.add(bn(new k(u*.9,-.45-u%2*.15,0),new Mt(0,0,y+Math.PI),s,o,a,i))}else if(_==="filo")for(let u=-1;u<=1;u++)for(let y=-1;y<=1;y++){const S=u*1.4+y%2*.7,M=y*1.2;r.add(bn(new k(S,M,0),new Mt(0,0,0),s,o,a,i))}else for(const u of[-.7,.7])for(const y of[-.7,.7])for(const S of[-.7,.7])r.add(bn(new k(u,y,S),new Mt(u,y,S),s,o,a,i))}if(e.klasa==="sve"){const _=document.createElement("div");_.className="udzbenik-silikati-traka",_.style.display="flex",_.style.flexWrap="wrap",_.style.gap="4px";const p=["nezo","soro","ciklo-3","ciklo-6","ino-jednostruki","ino-dvostruki","filo","tekto"];for(const u of p){const y=Pa[u],S=document.createElement("button");S.type="button",S.className="udzbenik-dugme udzbenik-dugme--malo",u===t&&S.classList.add("udzbenik-dugme--aktivno"),S.textContent=u,S.setAttribute("aria-label",y.naziv),S.addEventListener("click",()=>{t=u,_.querySelectorAll("button").forEach(M=>M.classList.remove("udzbenik-dugme--aktivno")),S.classList.add("udzbenik-dugme--aktivno"),l(u)}),_.append(S)}n.gornjeKontrole.append(_)}l(t);let d=0;const h=(e.animacija??(e.klasa==="sve"?"polimerizacija":"rotacija"))==="polimerizacija",f=["nezo","soro","ciklo-6","ino-jednostruki","ino-dvostruki","filo","tekto"];let m=0;function g(){s.color.set(n.tema.token("--primary")),o.color.set(n.tema.token("--accent"))}return{azuriraj(_){if(d+=_,r.rotation.y=d*.35,h){const p=Math.floor(d/3)%f.length;if(p!==m){m=p;const u=f[m];l(u)}}},korak(){d+=.3,r.rotation.y+=.2,h&&(m=(m+1)%f.length,l(f[m]))},resetuj(){d=0,r.rotation.set(0,0,0),m=0,l(t)},osveziTemu(){g()},raspolazi(){a.dispose(),s.dispose(),o.dispose(),Lt(r),c.remove()}}}},Bm={"kristalni-sistem":Im,"kristalna-struktura":Cm,"mohsova-skala":zm,cepljivost:ym,habitus:wm,"bravaisova-resetka":Mm,"opticka-indikatrisa":Fm,blizanac:vm,"koordinacioni-poliedar":Rm,"silikatna-struktura":Om};function Gm(n,e,t){const i=Bm[n.scena];return i?gm(i,n.parametri,e,t):(e.prikaziRezervu("Сцена није подржана у овој верзији мотора."),()=>{})}export{Gm as pokreniScenuPoImenu,Hm as raspolaziDeljenimRendererom};
