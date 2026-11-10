import{t as ri,n as fl,a as ct,g as io,b as Da,d as Ac,f as pl,A as ml,p as ro,c as so,J as ao,I as oo}from"./udzbenik-jezgro-CgECpr28.js";/**
 * @license
 * Copyright 2010-2025 Three.js Authors
 * SPDX-License-Identifier: MIT
 */const La="174",gl=0,co=1,_l=2,wc=1,vl=2,ln=3,Pn=0,Ct=1,Tt=2,Rn=0,Ti=1,lo=2,uo=3,ho=4,xl=5,Xn=100,Ml=101,Sl=102,El=103,yl=104,bl=200,Tl=201,Al=202,wl=203,ks=204,Os=205,Rl=206,Cl=207,Pl=208,Dl=209,Ll=210,Il=211,Ul=212,zl=213,Nl=214,Bs=0,Vs=1,Hs=2,Ri=3,Gs=4,js=5,Ws=6,Xs=7,Rc=0,Fl=1,kl=2,Cn=0,Ol=1,Bl=2,Vl=3,Hl=4,Gl=5,jl=6,Wl=7,Cc=300,Ci=301,Pi=302,qs=303,Ks=304,Kr=306,Ys=1e3,Yn=1001,$s=1002,kt=1003,Xl=1004,cr=1005,Zt=1006,Qr=1007,$n=1008,pn=1009,Pc=1010,Dc=1011,Zi=1012,Ia=1013,Qn=1014,dn=1015,nr=1016,Ua=1017,za=1018,Di=1020,Lc=35902,Ic=1021,Uc=1022,Gt=1023,zc=1024,Nc=1025,Ai=1026,Li=1027,Fc=1028,Na=1029,kc=1030,Fa=1031,ka=1033,zr=33776,Nr=33777,Fr=33778,kr=33779,Zs=35840,Js=35841,Qs=35842,ea=35843,ta=36196,na=37492,ia=37496,ra=37808,sa=37809,aa=37810,oa=37811,ca=37812,la=37813,ua=37814,da=37815,ha=37816,fa=37817,pa=37818,ma=37819,ga=37820,_a=37821,Or=36492,va=36494,xa=36495,Oc=36283,Ma=36284,Sa=36285,Ea=36286,ql=3200,Kl=3201,Bc=0,Yl=1,An="",Nt="srgb",Ii="srgb-linear",Gr="linear",it="srgb",si=7680,fo=519,$l=512,Zl=513,Jl=514,Vc=515,Ql=516,eu=517,tu=518,nu=519,po=35044,mo="300 es",hn=2e3,jr=2001;class Ni{addEventListener(e,t){this._listeners===void 0&&(this._listeners={});const i=this._listeners;i[e]===void 0&&(i[e]=[]),i[e].indexOf(t)===-1&&i[e].push(t)}hasEventListener(e,t){const i=this._listeners;return i===void 0?!1:i[e]!==void 0&&i[e].indexOf(t)!==-1}removeEventListener(e,t){const i=this._listeners;if(i===void 0)return;const r=i[e];if(r!==void 0){const s=r.indexOf(t);s!==-1&&r.splice(s,1)}}dispatchEvent(e){const t=this._listeners;if(t===void 0)return;const i=t[e.type];if(i!==void 0){e.target=this;const r=i.slice(0);for(let s=0,a=r.length;s<a;s++)r[s].call(this,e);e.target=null}}}const yt=["00","01","02","03","04","05","06","07","08","09","0a","0b","0c","0d","0e","0f","10","11","12","13","14","15","16","17","18","19","1a","1b","1c","1d","1e","1f","20","21","22","23","24","25","26","27","28","29","2a","2b","2c","2d","2e","2f","30","31","32","33","34","35","36","37","38","39","3a","3b","3c","3d","3e","3f","40","41","42","43","44","45","46","47","48","49","4a","4b","4c","4d","4e","4f","50","51","52","53","54","55","56","57","58","59","5a","5b","5c","5d","5e","5f","60","61","62","63","64","65","66","67","68","69","6a","6b","6c","6d","6e","6f","70","71","72","73","74","75","76","77","78","79","7a","7b","7c","7d","7e","7f","80","81","82","83","84","85","86","87","88","89","8a","8b","8c","8d","8e","8f","90","91","92","93","94","95","96","97","98","99","9a","9b","9c","9d","9e","9f","a0","a1","a2","a3","a4","a5","a6","a7","a8","a9","aa","ab","ac","ad","ae","af","b0","b1","b2","b3","b4","b5","b6","b7","b8","b9","ba","bb","bc","bd","be","bf","c0","c1","c2","c3","c4","c5","c6","c7","c8","c9","ca","cb","cc","cd","ce","cf","d0","d1","d2","d3","d4","d5","d6","d7","d8","d9","da","db","dc","dd","de","df","e0","e1","e2","e3","e4","e5","e6","e7","e8","e9","ea","eb","ec","ed","ee","ef","f0","f1","f2","f3","f4","f5","f6","f7","f8","f9","fa","fb","fc","fd","fe","ff"],Br=Math.PI/180,ya=180/Math.PI;function ir(){const n=Math.random()*4294967295|0,e=Math.random()*4294967295|0,t=Math.random()*4294967295|0,i=Math.random()*4294967295|0;return(yt[n&255]+yt[n>>8&255]+yt[n>>16&255]+yt[n>>24&255]+"-"+yt[e&255]+yt[e>>8&255]+"-"+yt[e>>16&15|64]+yt[e>>24&255]+"-"+yt[t&63|128]+yt[t>>8&255]+"-"+yt[t>>16&255]+yt[t>>24&255]+yt[i&255]+yt[i>>8&255]+yt[i>>16&255]+yt[i>>24&255]).toLowerCase()}function Xe(n,e,t){return Math.max(e,Math.min(t,n))}function iu(n,e){return(n%e+e)%e}function es(n,e,t){return(1-t)*n+t*e}function Vi(n,e){switch(e.constructor){case Float32Array:return n;case Uint32Array:return n/4294967295;case Uint16Array:return n/65535;case Uint8Array:return n/255;case Int32Array:return Math.max(n/2147483647,-1);case Int16Array:return Math.max(n/32767,-1);case Int8Array:return Math.max(n/127,-1);default:throw new Error("Invalid component type.")}}function Dt(n,e){switch(e.constructor){case Float32Array:return n;case Uint32Array:return Math.round(n*4294967295);case Uint16Array:return Math.round(n*65535);case Uint8Array:return Math.round(n*255);case Int32Array:return Math.round(n*2147483647);case Int16Array:return Math.round(n*32767);case Int8Array:return Math.round(n*127);default:throw new Error("Invalid component type.")}}class We{constructor(e=0,t=0){We.prototype.isVector2=!0,this.x=e,this.y=t}get width(){return this.x}set width(e){this.x=e}get height(){return this.y}set height(e){this.y=e}set(e,t){return this.x=e,this.y=t,this}setScalar(e){return this.x=e,this.y=e,this}setX(e){return this.x=e,this}setY(e){return this.y=e,this}setComponent(e,t){switch(e){case 0:this.x=t;break;case 1:this.y=t;break;default:throw new Error("index is out of range: "+e)}return this}getComponent(e){switch(e){case 0:return this.x;case 1:return this.y;default:throw new Error("index is out of range: "+e)}}clone(){return new this.constructor(this.x,this.y)}copy(e){return this.x=e.x,this.y=e.y,this}add(e){return this.x+=e.x,this.y+=e.y,this}addScalar(e){return this.x+=e,this.y+=e,this}addVectors(e,t){return this.x=e.x+t.x,this.y=e.y+t.y,this}addScaledVector(e,t){return this.x+=e.x*t,this.y+=e.y*t,this}sub(e){return this.x-=e.x,this.y-=e.y,this}subScalar(e){return this.x-=e,this.y-=e,this}subVectors(e,t){return this.x=e.x-t.x,this.y=e.y-t.y,this}multiply(e){return this.x*=e.x,this.y*=e.y,this}multiplyScalar(e){return this.x*=e,this.y*=e,this}divide(e){return this.x/=e.x,this.y/=e.y,this}divideScalar(e){return this.multiplyScalar(1/e)}applyMatrix3(e){const t=this.x,i=this.y,r=e.elements;return this.x=r[0]*t+r[3]*i+r[6],this.y=r[1]*t+r[4]*i+r[7],this}min(e){return this.x=Math.min(this.x,e.x),this.y=Math.min(this.y,e.y),this}max(e){return this.x=Math.max(this.x,e.x),this.y=Math.max(this.y,e.y),this}clamp(e,t){return this.x=Xe(this.x,e.x,t.x),this.y=Xe(this.y,e.y,t.y),this}clampScalar(e,t){return this.x=Xe(this.x,e,t),this.y=Xe(this.y,e,t),this}clampLength(e,t){const i=this.length();return this.divideScalar(i||1).multiplyScalar(Xe(i,e,t))}floor(){return this.x=Math.floor(this.x),this.y=Math.floor(this.y),this}ceil(){return this.x=Math.ceil(this.x),this.y=Math.ceil(this.y),this}round(){return this.x=Math.round(this.x),this.y=Math.round(this.y),this}roundToZero(){return this.x=Math.trunc(this.x),this.y=Math.trunc(this.y),this}negate(){return this.x=-this.x,this.y=-this.y,this}dot(e){return this.x*e.x+this.y*e.y}cross(e){return this.x*e.y-this.y*e.x}lengthSq(){return this.x*this.x+this.y*this.y}length(){return Math.sqrt(this.x*this.x+this.y*this.y)}manhattanLength(){return Math.abs(this.x)+Math.abs(this.y)}normalize(){return this.divideScalar(this.length()||1)}angle(){return Math.atan2(-this.y,-this.x)+Math.PI}angleTo(e){const t=Math.sqrt(this.lengthSq()*e.lengthSq());if(t===0)return Math.PI/2;const i=this.dot(e)/t;return Math.acos(Xe(i,-1,1))}distanceTo(e){return Math.sqrt(this.distanceToSquared(e))}distanceToSquared(e){const t=this.x-e.x,i=this.y-e.y;return t*t+i*i}manhattanDistanceTo(e){return Math.abs(this.x-e.x)+Math.abs(this.y-e.y)}setLength(e){return this.normalize().multiplyScalar(e)}lerp(e,t){return this.x+=(e.x-this.x)*t,this.y+=(e.y-this.y)*t,this}lerpVectors(e,t,i){return this.x=e.x+(t.x-e.x)*i,this.y=e.y+(t.y-e.y)*i,this}equals(e){return e.x===this.x&&e.y===this.y}fromArray(e,t=0){return this.x=e[t],this.y=e[t+1],this}toArray(e=[],t=0){return e[t]=this.x,e[t+1]=this.y,e}fromBufferAttribute(e,t){return this.x=e.getX(t),this.y=e.getY(t),this}rotateAround(e,t){const i=Math.cos(t),r=Math.sin(t),s=this.x-e.x,a=this.y-e.y;return this.x=s*i-a*r+e.x,this.y=s*r+a*i+e.y,this}random(){return this.x=Math.random(),this.y=Math.random(),this}*[Symbol.iterator](){yield this.x,yield this.y}}class Ve{constructor(e,t,i,r,s,a,o,c,l){Ve.prototype.isMatrix3=!0,this.elements=[1,0,0,0,1,0,0,0,1],e!==void 0&&this.set(e,t,i,r,s,a,o,c,l)}set(e,t,i,r,s,a,o,c,l){const d=this.elements;return d[0]=e,d[1]=r,d[2]=o,d[3]=t,d[4]=s,d[5]=c,d[6]=i,d[7]=a,d[8]=l,this}identity(){return this.set(1,0,0,0,1,0,0,0,1),this}copy(e){const t=this.elements,i=e.elements;return t[0]=i[0],t[1]=i[1],t[2]=i[2],t[3]=i[3],t[4]=i[4],t[5]=i[5],t[6]=i[6],t[7]=i[7],t[8]=i[8],this}extractBasis(e,t,i){return e.setFromMatrix3Column(this,0),t.setFromMatrix3Column(this,1),i.setFromMatrix3Column(this,2),this}setFromMatrix4(e){const t=e.elements;return this.set(t[0],t[4],t[8],t[1],t[5],t[9],t[2],t[6],t[10]),this}multiply(e){return this.multiplyMatrices(this,e)}premultiply(e){return this.multiplyMatrices(e,this)}multiplyMatrices(e,t){const i=e.elements,r=t.elements,s=this.elements,a=i[0],o=i[3],c=i[6],l=i[1],d=i[4],h=i[7],f=i[2],m=i[5],g=i[8],_=r[0],p=r[3],u=r[6],E=r[1],y=r[4],M=r[7],D=r[2],w=r[5],b=r[8];return s[0]=a*_+o*E+c*D,s[3]=a*p+o*y+c*w,s[6]=a*u+o*M+c*b,s[1]=l*_+d*E+h*D,s[4]=l*p+d*y+h*w,s[7]=l*u+d*M+h*b,s[2]=f*_+m*E+g*D,s[5]=f*p+m*y+g*w,s[8]=f*u+m*M+g*b,this}multiplyScalar(e){const t=this.elements;return t[0]*=e,t[3]*=e,t[6]*=e,t[1]*=e,t[4]*=e,t[7]*=e,t[2]*=e,t[5]*=e,t[8]*=e,this}determinant(){const e=this.elements,t=e[0],i=e[1],r=e[2],s=e[3],a=e[4],o=e[5],c=e[6],l=e[7],d=e[8];return t*a*d-t*o*l-i*s*d+i*o*c+r*s*l-r*a*c}invert(){const e=this.elements,t=e[0],i=e[1],r=e[2],s=e[3],a=e[4],o=e[5],c=e[6],l=e[7],d=e[8],h=d*a-o*l,f=o*c-d*s,m=l*s-a*c,g=t*h+i*f+r*m;if(g===0)return this.set(0,0,0,0,0,0,0,0,0);const _=1/g;return e[0]=h*_,e[1]=(r*l-d*i)*_,e[2]=(o*i-r*a)*_,e[3]=f*_,e[4]=(d*t-r*c)*_,e[5]=(r*s-o*t)*_,e[6]=m*_,e[7]=(i*c-l*t)*_,e[8]=(a*t-i*s)*_,this}transpose(){let e;const t=this.elements;return e=t[1],t[1]=t[3],t[3]=e,e=t[2],t[2]=t[6],t[6]=e,e=t[5],t[5]=t[7],t[7]=e,this}getNormalMatrix(e){return this.setFromMatrix4(e).invert().transpose()}transposeIntoArray(e){const t=this.elements;return e[0]=t[0],e[1]=t[3],e[2]=t[6],e[3]=t[1],e[4]=t[4],e[5]=t[7],e[6]=t[2],e[7]=t[5],e[8]=t[8],this}setUvTransform(e,t,i,r,s,a,o){const c=Math.cos(s),l=Math.sin(s);return this.set(i*c,i*l,-i*(c*a+l*o)+a+e,-r*l,r*c,-r*(-l*a+c*o)+o+t,0,0,1),this}scale(e,t){return this.premultiply(ts.makeScale(e,t)),this}rotate(e){return this.premultiply(ts.makeRotation(-e)),this}translate(e,t){return this.premultiply(ts.makeTranslation(e,t)),this}makeTranslation(e,t){return e.isVector2?this.set(1,0,e.x,0,1,e.y,0,0,1):this.set(1,0,e,0,1,t,0,0,1),this}makeRotation(e){const t=Math.cos(e),i=Math.sin(e);return this.set(t,-i,0,i,t,0,0,0,1),this}makeScale(e,t){return this.set(e,0,0,0,t,0,0,0,1),this}equals(e){const t=this.elements,i=e.elements;for(let r=0;r<9;r++)if(t[r]!==i[r])return!1;return!0}fromArray(e,t=0){for(let i=0;i<9;i++)this.elements[i]=e[i+t];return this}toArray(e=[],t=0){const i=this.elements;return e[t]=i[0],e[t+1]=i[1],e[t+2]=i[2],e[t+3]=i[3],e[t+4]=i[4],e[t+5]=i[5],e[t+6]=i[6],e[t+7]=i[7],e[t+8]=i[8],e}clone(){return new this.constructor().fromArray(this.elements)}}const ts=new Ve;function Hc(n){for(let e=n.length-1;e>=0;--e)if(n[e]>=65535)return!0;return!1}function Wr(n){return document.createElementNS("http://www.w3.org/1999/xhtml",n)}function ru(){const n=Wr("canvas");return n.style.display="block",n}const go={};function Vn(n){n in go||(go[n]=!0,console.warn(n))}function su(n,e,t){return new Promise(function(i,r){function s(){switch(n.clientWaitSync(e,n.SYNC_FLUSH_COMMANDS_BIT,0)){case n.WAIT_FAILED:r();break;case n.TIMEOUT_EXPIRED:setTimeout(s,t);break;default:i()}}setTimeout(s,t)})}function au(n){const e=n.elements;e[2]=.5*e[2]+.5*e[3],e[6]=.5*e[6]+.5*e[7],e[10]=.5*e[10]+.5*e[11],e[14]=.5*e[14]+.5*e[15]}function ou(n){const e=n.elements;e[11]===-1?(e[10]=-e[10]-1,e[14]=-e[14]):(e[10]=-e[10],e[14]=-e[14]+1)}const _o=new Ve().set(.4123908,.3575843,.1804808,.212639,.7151687,.0721923,.0193308,.1191948,.9505322),vo=new Ve().set(3.2409699,-1.5373832,-.4986108,-.9692436,1.8759675,.0415551,.0556301,-.203977,1.0569715);function cu(){const n={enabled:!0,workingColorSpace:Ii,spaces:{},convert:function(r,s,a){return this.enabled===!1||s===a||!s||!a||(this.spaces[s].transfer===it&&(r.r=fn(r.r),r.g=fn(r.g),r.b=fn(r.b)),this.spaces[s].primaries!==this.spaces[a].primaries&&(r.applyMatrix3(this.spaces[s].toXYZ),r.applyMatrix3(this.spaces[a].fromXYZ)),this.spaces[a].transfer===it&&(r.r=wi(r.r),r.g=wi(r.g),r.b=wi(r.b))),r},fromWorkingColorSpace:function(r,s){return this.convert(r,this.workingColorSpace,s)},toWorkingColorSpace:function(r,s){return this.convert(r,s,this.workingColorSpace)},getPrimaries:function(r){return this.spaces[r].primaries},getTransfer:function(r){return r===An?Gr:this.spaces[r].transfer},getLuminanceCoefficients:function(r,s=this.workingColorSpace){return r.fromArray(this.spaces[s].luminanceCoefficients)},define:function(r){Object.assign(this.spaces,r)},_getMatrix:function(r,s,a){return r.copy(this.spaces[s].toXYZ).multiply(this.spaces[a].fromXYZ)},_getDrawingBufferColorSpace:function(r){return this.spaces[r].outputColorSpaceConfig.drawingBufferColorSpace},_getUnpackColorSpace:function(r=this.workingColorSpace){return this.spaces[r].workingColorSpaceConfig.unpackColorSpace}},e=[.64,.33,.3,.6,.15,.06],t=[.2126,.7152,.0722],i=[.3127,.329];return n.define({[Ii]:{primaries:e,whitePoint:i,transfer:Gr,toXYZ:_o,fromXYZ:vo,luminanceCoefficients:t,workingColorSpaceConfig:{unpackColorSpace:Nt},outputColorSpaceConfig:{drawingBufferColorSpace:Nt}},[Nt]:{primaries:e,whitePoint:i,transfer:it,toXYZ:_o,fromXYZ:vo,luminanceCoefficients:t,outputColorSpaceConfig:{drawingBufferColorSpace:Nt}}}),n}const Je=cu();function fn(n){return n<.04045?n*.0773993808:Math.pow(n*.9478672986+.0521327014,2.4)}function wi(n){return n<.0031308?n*12.92:1.055*Math.pow(n,.41666)-.055}let ai;class lu{static getDataURL(e){if(/^data:/i.test(e.src)||typeof HTMLCanvasElement>"u")return e.src;let t;if(e instanceof HTMLCanvasElement)t=e;else{ai===void 0&&(ai=Wr("canvas")),ai.width=e.width,ai.height=e.height;const i=ai.getContext("2d");e instanceof ImageData?i.putImageData(e,0,0):i.drawImage(e,0,0,e.width,e.height),t=ai}return t.toDataURL("image/png")}static sRGBToLinear(e){if(typeof HTMLImageElement<"u"&&e instanceof HTMLImageElement||typeof HTMLCanvasElement<"u"&&e instanceof HTMLCanvasElement||typeof ImageBitmap<"u"&&e instanceof ImageBitmap){const t=Wr("canvas");t.width=e.width,t.height=e.height;const i=t.getContext("2d");i.drawImage(e,0,0,e.width,e.height);const r=i.getImageData(0,0,e.width,e.height),s=r.data;for(let a=0;a<s.length;a++)s[a]=fn(s[a]/255)*255;return i.putImageData(r,0,0),t}else if(e.data){const t=e.data.slice(0);for(let i=0;i<t.length;i++)t instanceof Uint8Array||t instanceof Uint8ClampedArray?t[i]=Math.floor(fn(t[i]/255)*255):t[i]=fn(t[i]);return{data:t,width:e.width,height:e.height}}else return console.warn("THREE.ImageUtils.sRGBToLinear(): Unsupported image type. No color space conversion applied."),e}}let uu=0;class Oa{constructor(e=null){this.isSource=!0,Object.defineProperty(this,"id",{value:uu++}),this.uuid=ir(),this.data=e,this.dataReady=!0,this.version=0}set needsUpdate(e){e===!0&&this.version++}toJSON(e){const t=e===void 0||typeof e=="string";if(!t&&e.images[this.uuid]!==void 0)return e.images[this.uuid];const i={uuid:this.uuid,url:""},r=this.data;if(r!==null){let s;if(Array.isArray(r)){s=[];for(let a=0,o=r.length;a<o;a++)r[a].isDataTexture?s.push(ns(r[a].image)):s.push(ns(r[a]))}else s=ns(r);i.url=s}return t||(e.images[this.uuid]=i),i}}function ns(n){return typeof HTMLImageElement<"u"&&n instanceof HTMLImageElement||typeof HTMLCanvasElement<"u"&&n instanceof HTMLCanvasElement||typeof ImageBitmap<"u"&&n instanceof ImageBitmap?lu.getDataURL(n):n.data?{data:Array.from(n.data),width:n.width,height:n.height,type:n.data.constructor.name}:(console.warn("THREE.Texture: Unable to serialize Texture."),{})}let du=0;class At extends Ni{constructor(e=At.DEFAULT_IMAGE,t=At.DEFAULT_MAPPING,i=Yn,r=Yn,s=Zt,a=$n,o=Gt,c=pn,l=At.DEFAULT_ANISOTROPY,d=An){super(),this.isTexture=!0,Object.defineProperty(this,"id",{value:du++}),this.uuid=ir(),this.name="",this.source=new Oa(e),this.mipmaps=[],this.mapping=t,this.channel=0,this.wrapS=i,this.wrapT=r,this.magFilter=s,this.minFilter=a,this.anisotropy=l,this.format=o,this.internalFormat=null,this.type=c,this.offset=new We(0,0),this.repeat=new We(1,1),this.center=new We(0,0),this.rotation=0,this.matrixAutoUpdate=!0,this.matrix=new Ve,this.generateMipmaps=!0,this.premultiplyAlpha=!1,this.flipY=!0,this.unpackAlignment=4,this.colorSpace=d,this.userData={},this.version=0,this.onUpdate=null,this.renderTarget=null,this.isRenderTargetTexture=!1,this.pmremVersion=0}get image(){return this.source.data}set image(e=null){this.source.data=e}updateMatrix(){this.matrix.setUvTransform(this.offset.x,this.offset.y,this.repeat.x,this.repeat.y,this.rotation,this.center.x,this.center.y)}clone(){return new this.constructor().copy(this)}copy(e){return this.name=e.name,this.source=e.source,this.mipmaps=e.mipmaps.slice(0),this.mapping=e.mapping,this.channel=e.channel,this.wrapS=e.wrapS,this.wrapT=e.wrapT,this.magFilter=e.magFilter,this.minFilter=e.minFilter,this.anisotropy=e.anisotropy,this.format=e.format,this.internalFormat=e.internalFormat,this.type=e.type,this.offset.copy(e.offset),this.repeat.copy(e.repeat),this.center.copy(e.center),this.rotation=e.rotation,this.matrixAutoUpdate=e.matrixAutoUpdate,this.matrix.copy(e.matrix),this.generateMipmaps=e.generateMipmaps,this.premultiplyAlpha=e.premultiplyAlpha,this.flipY=e.flipY,this.unpackAlignment=e.unpackAlignment,this.colorSpace=e.colorSpace,this.renderTarget=e.renderTarget,this.isRenderTargetTexture=e.isRenderTargetTexture,this.userData=JSON.parse(JSON.stringify(e.userData)),this.needsUpdate=!0,this}toJSON(e){const t=e===void 0||typeof e=="string";if(!t&&e.textures[this.uuid]!==void 0)return e.textures[this.uuid];const i={metadata:{version:4.6,type:"Texture",generator:"Texture.toJSON"},uuid:this.uuid,name:this.name,image:this.source.toJSON(e).uuid,mapping:this.mapping,channel:this.channel,repeat:[this.repeat.x,this.repeat.y],offset:[this.offset.x,this.offset.y],center:[this.center.x,this.center.y],rotation:this.rotation,wrap:[this.wrapS,this.wrapT],format:this.format,internalFormat:this.internalFormat,type:this.type,colorSpace:this.colorSpace,minFilter:this.minFilter,magFilter:this.magFilter,anisotropy:this.anisotropy,flipY:this.flipY,generateMipmaps:this.generateMipmaps,premultiplyAlpha:this.premultiplyAlpha,unpackAlignment:this.unpackAlignment};return Object.keys(this.userData).length>0&&(i.userData=this.userData),t||(e.textures[this.uuid]=i),i}dispose(){this.dispatchEvent({type:"dispose"})}transformUv(e){if(this.mapping!==Cc)return e;if(e.applyMatrix3(this.matrix),e.x<0||e.x>1)switch(this.wrapS){case Ys:e.x=e.x-Math.floor(e.x);break;case Yn:e.x=e.x<0?0:1;break;case $s:Math.abs(Math.floor(e.x)%2)===1?e.x=Math.ceil(e.x)-e.x:e.x=e.x-Math.floor(e.x);break}if(e.y<0||e.y>1)switch(this.wrapT){case Ys:e.y=e.y-Math.floor(e.y);break;case Yn:e.y=e.y<0?0:1;break;case $s:Math.abs(Math.floor(e.y)%2)===1?e.y=Math.ceil(e.y)-e.y:e.y=e.y-Math.floor(e.y);break}return this.flipY&&(e.y=1-e.y),e}set needsUpdate(e){e===!0&&(this.version++,this.source.needsUpdate=!0)}set needsPMREMUpdate(e){e===!0&&this.pmremVersion++}}At.DEFAULT_IMAGE=null;At.DEFAULT_MAPPING=Cc;At.DEFAULT_ANISOTROPY=1;class rt{constructor(e=0,t=0,i=0,r=1){rt.prototype.isVector4=!0,this.x=e,this.y=t,this.z=i,this.w=r}get width(){return this.z}set width(e){this.z=e}get height(){return this.w}set height(e){this.w=e}set(e,t,i,r){return this.x=e,this.y=t,this.z=i,this.w=r,this}setScalar(e){return this.x=e,this.y=e,this.z=e,this.w=e,this}setX(e){return this.x=e,this}setY(e){return this.y=e,this}setZ(e){return this.z=e,this}setW(e){return this.w=e,this}setComponent(e,t){switch(e){case 0:this.x=t;break;case 1:this.y=t;break;case 2:this.z=t;break;case 3:this.w=t;break;default:throw new Error("index is out of range: "+e)}return this}getComponent(e){switch(e){case 0:return this.x;case 1:return this.y;case 2:return this.z;case 3:return this.w;default:throw new Error("index is out of range: "+e)}}clone(){return new this.constructor(this.x,this.y,this.z,this.w)}copy(e){return this.x=e.x,this.y=e.y,this.z=e.z,this.w=e.w!==void 0?e.w:1,this}add(e){return this.x+=e.x,this.y+=e.y,this.z+=e.z,this.w+=e.w,this}addScalar(e){return this.x+=e,this.y+=e,this.z+=e,this.w+=e,this}addVectors(e,t){return this.x=e.x+t.x,this.y=e.y+t.y,this.z=e.z+t.z,this.w=e.w+t.w,this}addScaledVector(e,t){return this.x+=e.x*t,this.y+=e.y*t,this.z+=e.z*t,this.w+=e.w*t,this}sub(e){return this.x-=e.x,this.y-=e.y,this.z-=e.z,this.w-=e.w,this}subScalar(e){return this.x-=e,this.y-=e,this.z-=e,this.w-=e,this}subVectors(e,t){return this.x=e.x-t.x,this.y=e.y-t.y,this.z=e.z-t.z,this.w=e.w-t.w,this}multiply(e){return this.x*=e.x,this.y*=e.y,this.z*=e.z,this.w*=e.w,this}multiplyScalar(e){return this.x*=e,this.y*=e,this.z*=e,this.w*=e,this}applyMatrix4(e){const t=this.x,i=this.y,r=this.z,s=this.w,a=e.elements;return this.x=a[0]*t+a[4]*i+a[8]*r+a[12]*s,this.y=a[1]*t+a[5]*i+a[9]*r+a[13]*s,this.z=a[2]*t+a[6]*i+a[10]*r+a[14]*s,this.w=a[3]*t+a[7]*i+a[11]*r+a[15]*s,this}divide(e){return this.x/=e.x,this.y/=e.y,this.z/=e.z,this.w/=e.w,this}divideScalar(e){return this.multiplyScalar(1/e)}setAxisAngleFromQuaternion(e){this.w=2*Math.acos(e.w);const t=Math.sqrt(1-e.w*e.w);return t<1e-4?(this.x=1,this.y=0,this.z=0):(this.x=e.x/t,this.y=e.y/t,this.z=e.z/t),this}setAxisAngleFromRotationMatrix(e){let t,i,r,s;const c=e.elements,l=c[0],d=c[4],h=c[8],f=c[1],m=c[5],g=c[9],_=c[2],p=c[6],u=c[10];if(Math.abs(d-f)<.01&&Math.abs(h-_)<.01&&Math.abs(g-p)<.01){if(Math.abs(d+f)<.1&&Math.abs(h+_)<.1&&Math.abs(g+p)<.1&&Math.abs(l+m+u-3)<.1)return this.set(1,0,0,0),this;t=Math.PI;const y=(l+1)/2,M=(m+1)/2,D=(u+1)/2,w=(d+f)/4,b=(h+_)/4,C=(g+p)/4;return y>M&&y>D?y<.01?(i=0,r=.707106781,s=.707106781):(i=Math.sqrt(y),r=w/i,s=b/i):M>D?M<.01?(i=.707106781,r=0,s=.707106781):(r=Math.sqrt(M),i=w/r,s=C/r):D<.01?(i=.707106781,r=.707106781,s=0):(s=Math.sqrt(D),i=b/s,r=C/s),this.set(i,r,s,t),this}let E=Math.sqrt((p-g)*(p-g)+(h-_)*(h-_)+(f-d)*(f-d));return Math.abs(E)<.001&&(E=1),this.x=(p-g)/E,this.y=(h-_)/E,this.z=(f-d)/E,this.w=Math.acos((l+m+u-1)/2),this}setFromMatrixPosition(e){const t=e.elements;return this.x=t[12],this.y=t[13],this.z=t[14],this.w=t[15],this}min(e){return this.x=Math.min(this.x,e.x),this.y=Math.min(this.y,e.y),this.z=Math.min(this.z,e.z),this.w=Math.min(this.w,e.w),this}max(e){return this.x=Math.max(this.x,e.x),this.y=Math.max(this.y,e.y),this.z=Math.max(this.z,e.z),this.w=Math.max(this.w,e.w),this}clamp(e,t){return this.x=Xe(this.x,e.x,t.x),this.y=Xe(this.y,e.y,t.y),this.z=Xe(this.z,e.z,t.z),this.w=Xe(this.w,e.w,t.w),this}clampScalar(e,t){return this.x=Xe(this.x,e,t),this.y=Xe(this.y,e,t),this.z=Xe(this.z,e,t),this.w=Xe(this.w,e,t),this}clampLength(e,t){const i=this.length();return this.divideScalar(i||1).multiplyScalar(Xe(i,e,t))}floor(){return this.x=Math.floor(this.x),this.y=Math.floor(this.y),this.z=Math.floor(this.z),this.w=Math.floor(this.w),this}ceil(){return this.x=Math.ceil(this.x),this.y=Math.ceil(this.y),this.z=Math.ceil(this.z),this.w=Math.ceil(this.w),this}round(){return this.x=Math.round(this.x),this.y=Math.round(this.y),this.z=Math.round(this.z),this.w=Math.round(this.w),this}roundToZero(){return this.x=Math.trunc(this.x),this.y=Math.trunc(this.y),this.z=Math.trunc(this.z),this.w=Math.trunc(this.w),this}negate(){return this.x=-this.x,this.y=-this.y,this.z=-this.z,this.w=-this.w,this}dot(e){return this.x*e.x+this.y*e.y+this.z*e.z+this.w*e.w}lengthSq(){return this.x*this.x+this.y*this.y+this.z*this.z+this.w*this.w}length(){return Math.sqrt(this.x*this.x+this.y*this.y+this.z*this.z+this.w*this.w)}manhattanLength(){return Math.abs(this.x)+Math.abs(this.y)+Math.abs(this.z)+Math.abs(this.w)}normalize(){return this.divideScalar(this.length()||1)}setLength(e){return this.normalize().multiplyScalar(e)}lerp(e,t){return this.x+=(e.x-this.x)*t,this.y+=(e.y-this.y)*t,this.z+=(e.z-this.z)*t,this.w+=(e.w-this.w)*t,this}lerpVectors(e,t,i){return this.x=e.x+(t.x-e.x)*i,this.y=e.y+(t.y-e.y)*i,this.z=e.z+(t.z-e.z)*i,this.w=e.w+(t.w-e.w)*i,this}equals(e){return e.x===this.x&&e.y===this.y&&e.z===this.z&&e.w===this.w}fromArray(e,t=0){return this.x=e[t],this.y=e[t+1],this.z=e[t+2],this.w=e[t+3],this}toArray(e=[],t=0){return e[t]=this.x,e[t+1]=this.y,e[t+2]=this.z,e[t+3]=this.w,e}fromBufferAttribute(e,t){return this.x=e.getX(t),this.y=e.getY(t),this.z=e.getZ(t),this.w=e.getW(t),this}random(){return this.x=Math.random(),this.y=Math.random(),this.z=Math.random(),this.w=Math.random(),this}*[Symbol.iterator](){yield this.x,yield this.y,yield this.z,yield this.w}}class hu extends Ni{constructor(e=1,t=1,i={}){super(),this.isRenderTarget=!0,this.width=e,this.height=t,this.depth=1,this.scissor=new rt(0,0,e,t),this.scissorTest=!1,this.viewport=new rt(0,0,e,t);const r={width:e,height:t,depth:1};i=Object.assign({generateMipmaps:!1,internalFormat:null,minFilter:Zt,depthBuffer:!0,stencilBuffer:!1,resolveDepthBuffer:!0,resolveStencilBuffer:!0,depthTexture:null,samples:0,count:1},i);const s=new At(r,i.mapping,i.wrapS,i.wrapT,i.magFilter,i.minFilter,i.format,i.type,i.anisotropy,i.colorSpace);s.flipY=!1,s.generateMipmaps=i.generateMipmaps,s.internalFormat=i.internalFormat,this.textures=[];const a=i.count;for(let o=0;o<a;o++)this.textures[o]=s.clone(),this.textures[o].isRenderTargetTexture=!0,this.textures[o].renderTarget=this;this.depthBuffer=i.depthBuffer,this.stencilBuffer=i.stencilBuffer,this.resolveDepthBuffer=i.resolveDepthBuffer,this.resolveStencilBuffer=i.resolveStencilBuffer,this._depthTexture=null,this.depthTexture=i.depthTexture,this.samples=i.samples}get texture(){return this.textures[0]}set texture(e){this.textures[0]=e}set depthTexture(e){this._depthTexture!==null&&(this._depthTexture.renderTarget=null),e!==null&&(e.renderTarget=this),this._depthTexture=e}get depthTexture(){return this._depthTexture}setSize(e,t,i=1){if(this.width!==e||this.height!==t||this.depth!==i){this.width=e,this.height=t,this.depth=i;for(let r=0,s=this.textures.length;r<s;r++)this.textures[r].image.width=e,this.textures[r].image.height=t,this.textures[r].image.depth=i;this.dispose()}this.viewport.set(0,0,e,t),this.scissor.set(0,0,e,t)}clone(){return new this.constructor().copy(this)}copy(e){this.width=e.width,this.height=e.height,this.depth=e.depth,this.scissor.copy(e.scissor),this.scissorTest=e.scissorTest,this.viewport.copy(e.viewport),this.textures.length=0;for(let t=0,i=e.textures.length;t<i;t++){this.textures[t]=e.textures[t].clone(),this.textures[t].isRenderTargetTexture=!0,this.textures[t].renderTarget=this;const r=Object.assign({},e.textures[t].image);this.textures[t].source=new Oa(r)}return this.depthBuffer=e.depthBuffer,this.stencilBuffer=e.stencilBuffer,this.resolveDepthBuffer=e.resolveDepthBuffer,this.resolveStencilBuffer=e.resolveStencilBuffer,e.depthTexture!==null&&(this.depthTexture=e.depthTexture.clone()),this.samples=e.samples,this}dispose(){this.dispatchEvent({type:"dispose"})}}class ei extends hu{constructor(e=1,t=1,i={}){super(e,t,i),this.isWebGLRenderTarget=!0}}class Gc extends At{constructor(e=null,t=1,i=1,r=1){super(null),this.isDataArrayTexture=!0,this.image={data:e,width:t,height:i,depth:r},this.magFilter=kt,this.minFilter=kt,this.wrapR=Yn,this.generateMipmaps=!1,this.flipY=!1,this.unpackAlignment=1,this.layerUpdates=new Set}addLayerUpdate(e){this.layerUpdates.add(e)}clearLayerUpdates(){this.layerUpdates.clear()}}class fu extends At{constructor(e=null,t=1,i=1,r=1){super(null),this.isData3DTexture=!0,this.image={data:e,width:t,height:i,depth:r},this.magFilter=kt,this.minFilter=kt,this.wrapR=Yn,this.generateMipmaps=!1,this.flipY=!1,this.unpackAlignment=1}}class rr{constructor(e=0,t=0,i=0,r=1){this.isQuaternion=!0,this._x=e,this._y=t,this._z=i,this._w=r}static slerpFlat(e,t,i,r,s,a,o){let c=i[r+0],l=i[r+1],d=i[r+2],h=i[r+3];const f=s[a+0],m=s[a+1],g=s[a+2],_=s[a+3];if(o===0){e[t+0]=c,e[t+1]=l,e[t+2]=d,e[t+3]=h;return}if(o===1){e[t+0]=f,e[t+1]=m,e[t+2]=g,e[t+3]=_;return}if(h!==_||c!==f||l!==m||d!==g){let p=1-o;const u=c*f+l*m+d*g+h*_,E=u>=0?1:-1,y=1-u*u;if(y>Number.EPSILON){const D=Math.sqrt(y),w=Math.atan2(D,u*E);p=Math.sin(p*w)/D,o=Math.sin(o*w)/D}const M=o*E;if(c=c*p+f*M,l=l*p+m*M,d=d*p+g*M,h=h*p+_*M,p===1-o){const D=1/Math.sqrt(c*c+l*l+d*d+h*h);c*=D,l*=D,d*=D,h*=D}}e[t]=c,e[t+1]=l,e[t+2]=d,e[t+3]=h}static multiplyQuaternionsFlat(e,t,i,r,s,a){const o=i[r],c=i[r+1],l=i[r+2],d=i[r+3],h=s[a],f=s[a+1],m=s[a+2],g=s[a+3];return e[t]=o*g+d*h+c*m-l*f,e[t+1]=c*g+d*f+l*h-o*m,e[t+2]=l*g+d*m+o*f-c*h,e[t+3]=d*g-o*h-c*f-l*m,e}get x(){return this._x}set x(e){this._x=e,this._onChangeCallback()}get y(){return this._y}set y(e){this._y=e,this._onChangeCallback()}get z(){return this._z}set z(e){this._z=e,this._onChangeCallback()}get w(){return this._w}set w(e){this._w=e,this._onChangeCallback()}set(e,t,i,r){return this._x=e,this._y=t,this._z=i,this._w=r,this._onChangeCallback(),this}clone(){return new this.constructor(this._x,this._y,this._z,this._w)}copy(e){return this._x=e.x,this._y=e.y,this._z=e.z,this._w=e.w,this._onChangeCallback(),this}setFromEuler(e,t=!0){const i=e._x,r=e._y,s=e._z,a=e._order,o=Math.cos,c=Math.sin,l=o(i/2),d=o(r/2),h=o(s/2),f=c(i/2),m=c(r/2),g=c(s/2);switch(a){case"XYZ":this._x=f*d*h+l*m*g,this._y=l*m*h-f*d*g,this._z=l*d*g+f*m*h,this._w=l*d*h-f*m*g;break;case"YXZ":this._x=f*d*h+l*m*g,this._y=l*m*h-f*d*g,this._z=l*d*g-f*m*h,this._w=l*d*h+f*m*g;break;case"ZXY":this._x=f*d*h-l*m*g,this._y=l*m*h+f*d*g,this._z=l*d*g+f*m*h,this._w=l*d*h-f*m*g;break;case"ZYX":this._x=f*d*h-l*m*g,this._y=l*m*h+f*d*g,this._z=l*d*g-f*m*h,this._w=l*d*h+f*m*g;break;case"YZX":this._x=f*d*h+l*m*g,this._y=l*m*h+f*d*g,this._z=l*d*g-f*m*h,this._w=l*d*h-f*m*g;break;case"XZY":this._x=f*d*h-l*m*g,this._y=l*m*h-f*d*g,this._z=l*d*g+f*m*h,this._w=l*d*h+f*m*g;break;default:console.warn("THREE.Quaternion: .setFromEuler() encountered an unknown order: "+a)}return t===!0&&this._onChangeCallback(),this}setFromAxisAngle(e,t){const i=t/2,r=Math.sin(i);return this._x=e.x*r,this._y=e.y*r,this._z=e.z*r,this._w=Math.cos(i),this._onChangeCallback(),this}setFromRotationMatrix(e){const t=e.elements,i=t[0],r=t[4],s=t[8],a=t[1],o=t[5],c=t[9],l=t[2],d=t[6],h=t[10],f=i+o+h;if(f>0){const m=.5/Math.sqrt(f+1);this._w=.25/m,this._x=(d-c)*m,this._y=(s-l)*m,this._z=(a-r)*m}else if(i>o&&i>h){const m=2*Math.sqrt(1+i-o-h);this._w=(d-c)/m,this._x=.25*m,this._y=(r+a)/m,this._z=(s+l)/m}else if(o>h){const m=2*Math.sqrt(1+o-i-h);this._w=(s-l)/m,this._x=(r+a)/m,this._y=.25*m,this._z=(c+d)/m}else{const m=2*Math.sqrt(1+h-i-o);this._w=(a-r)/m,this._x=(s+l)/m,this._y=(c+d)/m,this._z=.25*m}return this._onChangeCallback(),this}setFromUnitVectors(e,t){let i=e.dot(t)+1;return i<Number.EPSILON?(i=0,Math.abs(e.x)>Math.abs(e.z)?(this._x=-e.y,this._y=e.x,this._z=0,this._w=i):(this._x=0,this._y=-e.z,this._z=e.y,this._w=i)):(this._x=e.y*t.z-e.z*t.y,this._y=e.z*t.x-e.x*t.z,this._z=e.x*t.y-e.y*t.x,this._w=i),this.normalize()}angleTo(e){return 2*Math.acos(Math.abs(Xe(this.dot(e),-1,1)))}rotateTowards(e,t){const i=this.angleTo(e);if(i===0)return this;const r=Math.min(1,t/i);return this.slerp(e,r),this}identity(){return this.set(0,0,0,1)}invert(){return this.conjugate()}conjugate(){return this._x*=-1,this._y*=-1,this._z*=-1,this._onChangeCallback(),this}dot(e){return this._x*e._x+this._y*e._y+this._z*e._z+this._w*e._w}lengthSq(){return this._x*this._x+this._y*this._y+this._z*this._z+this._w*this._w}length(){return Math.sqrt(this._x*this._x+this._y*this._y+this._z*this._z+this._w*this._w)}normalize(){let e=this.length();return e===0?(this._x=0,this._y=0,this._z=0,this._w=1):(e=1/e,this._x=this._x*e,this._y=this._y*e,this._z=this._z*e,this._w=this._w*e),this._onChangeCallback(),this}multiply(e){return this.multiplyQuaternions(this,e)}premultiply(e){return this.multiplyQuaternions(e,this)}multiplyQuaternions(e,t){const i=e._x,r=e._y,s=e._z,a=e._w,o=t._x,c=t._y,l=t._z,d=t._w;return this._x=i*d+a*o+r*l-s*c,this._y=r*d+a*c+s*o-i*l,this._z=s*d+a*l+i*c-r*o,this._w=a*d-i*o-r*c-s*l,this._onChangeCallback(),this}slerp(e,t){if(t===0)return this;if(t===1)return this.copy(e);const i=this._x,r=this._y,s=this._z,a=this._w;let o=a*e._w+i*e._x+r*e._y+s*e._z;if(o<0?(this._w=-e._w,this._x=-e._x,this._y=-e._y,this._z=-e._z,o=-o):this.copy(e),o>=1)return this._w=a,this._x=i,this._y=r,this._z=s,this;const c=1-o*o;if(c<=Number.EPSILON){const m=1-t;return this._w=m*a+t*this._w,this._x=m*i+t*this._x,this._y=m*r+t*this._y,this._z=m*s+t*this._z,this.normalize(),this}const l=Math.sqrt(c),d=Math.atan2(l,o),h=Math.sin((1-t)*d)/l,f=Math.sin(t*d)/l;return this._w=a*h+this._w*f,this._x=i*h+this._x*f,this._y=r*h+this._y*f,this._z=s*h+this._z*f,this._onChangeCallback(),this}slerpQuaternions(e,t,i){return this.copy(e).slerp(t,i)}random(){const e=2*Math.PI*Math.random(),t=2*Math.PI*Math.random(),i=Math.random(),r=Math.sqrt(1-i),s=Math.sqrt(i);return this.set(r*Math.sin(e),r*Math.cos(e),s*Math.sin(t),s*Math.cos(t))}equals(e){return e._x===this._x&&e._y===this._y&&e._z===this._z&&e._w===this._w}fromArray(e,t=0){return this._x=e[t],this._y=e[t+1],this._z=e[t+2],this._w=e[t+3],this._onChangeCallback(),this}toArray(e=[],t=0){return e[t]=this._x,e[t+1]=this._y,e[t+2]=this._z,e[t+3]=this._w,e}fromBufferAttribute(e,t){return this._x=e.getX(t),this._y=e.getY(t),this._z=e.getZ(t),this._w=e.getW(t),this._onChangeCallback(),this}toJSON(){return this.toArray()}_onChange(e){return this._onChangeCallback=e,this}_onChangeCallback(){}*[Symbol.iterator](){yield this._x,yield this._y,yield this._z,yield this._w}}class k{constructor(e=0,t=0,i=0){k.prototype.isVector3=!0,this.x=e,this.y=t,this.z=i}set(e,t,i){return i===void 0&&(i=this.z),this.x=e,this.y=t,this.z=i,this}setScalar(e){return this.x=e,this.y=e,this.z=e,this}setX(e){return this.x=e,this}setY(e){return this.y=e,this}setZ(e){return this.z=e,this}setComponent(e,t){switch(e){case 0:this.x=t;break;case 1:this.y=t;break;case 2:this.z=t;break;default:throw new Error("index is out of range: "+e)}return this}getComponent(e){switch(e){case 0:return this.x;case 1:return this.y;case 2:return this.z;default:throw new Error("index is out of range: "+e)}}clone(){return new this.constructor(this.x,this.y,this.z)}copy(e){return this.x=e.x,this.y=e.y,this.z=e.z,this}add(e){return this.x+=e.x,this.y+=e.y,this.z+=e.z,this}addScalar(e){return this.x+=e,this.y+=e,this.z+=e,this}addVectors(e,t){return this.x=e.x+t.x,this.y=e.y+t.y,this.z=e.z+t.z,this}addScaledVector(e,t){return this.x+=e.x*t,this.y+=e.y*t,this.z+=e.z*t,this}sub(e){return this.x-=e.x,this.y-=e.y,this.z-=e.z,this}subScalar(e){return this.x-=e,this.y-=e,this.z-=e,this}subVectors(e,t){return this.x=e.x-t.x,this.y=e.y-t.y,this.z=e.z-t.z,this}multiply(e){return this.x*=e.x,this.y*=e.y,this.z*=e.z,this}multiplyScalar(e){return this.x*=e,this.y*=e,this.z*=e,this}multiplyVectors(e,t){return this.x=e.x*t.x,this.y=e.y*t.y,this.z=e.z*t.z,this}applyEuler(e){return this.applyQuaternion(xo.setFromEuler(e))}applyAxisAngle(e,t){return this.applyQuaternion(xo.setFromAxisAngle(e,t))}applyMatrix3(e){const t=this.x,i=this.y,r=this.z,s=e.elements;return this.x=s[0]*t+s[3]*i+s[6]*r,this.y=s[1]*t+s[4]*i+s[7]*r,this.z=s[2]*t+s[5]*i+s[8]*r,this}applyNormalMatrix(e){return this.applyMatrix3(e).normalize()}applyMatrix4(e){const t=this.x,i=this.y,r=this.z,s=e.elements,a=1/(s[3]*t+s[7]*i+s[11]*r+s[15]);return this.x=(s[0]*t+s[4]*i+s[8]*r+s[12])*a,this.y=(s[1]*t+s[5]*i+s[9]*r+s[13])*a,this.z=(s[2]*t+s[6]*i+s[10]*r+s[14])*a,this}applyQuaternion(e){const t=this.x,i=this.y,r=this.z,s=e.x,a=e.y,o=e.z,c=e.w,l=2*(a*r-o*i),d=2*(o*t-s*r),h=2*(s*i-a*t);return this.x=t+c*l+a*h-o*d,this.y=i+c*d+o*l-s*h,this.z=r+c*h+s*d-a*l,this}project(e){return this.applyMatrix4(e.matrixWorldInverse).applyMatrix4(e.projectionMatrix)}unproject(e){return this.applyMatrix4(e.projectionMatrixInverse).applyMatrix4(e.matrixWorld)}transformDirection(e){const t=this.x,i=this.y,r=this.z,s=e.elements;return this.x=s[0]*t+s[4]*i+s[8]*r,this.y=s[1]*t+s[5]*i+s[9]*r,this.z=s[2]*t+s[6]*i+s[10]*r,this.normalize()}divide(e){return this.x/=e.x,this.y/=e.y,this.z/=e.z,this}divideScalar(e){return this.multiplyScalar(1/e)}min(e){return this.x=Math.min(this.x,e.x),this.y=Math.min(this.y,e.y),this.z=Math.min(this.z,e.z),this}max(e){return this.x=Math.max(this.x,e.x),this.y=Math.max(this.y,e.y),this.z=Math.max(this.z,e.z),this}clamp(e,t){return this.x=Xe(this.x,e.x,t.x),this.y=Xe(this.y,e.y,t.y),this.z=Xe(this.z,e.z,t.z),this}clampScalar(e,t){return this.x=Xe(this.x,e,t),this.y=Xe(this.y,e,t),this.z=Xe(this.z,e,t),this}clampLength(e,t){const i=this.length();return this.divideScalar(i||1).multiplyScalar(Xe(i,e,t))}floor(){return this.x=Math.floor(this.x),this.y=Math.floor(this.y),this.z=Math.floor(this.z),this}ceil(){return this.x=Math.ceil(this.x),this.y=Math.ceil(this.y),this.z=Math.ceil(this.z),this}round(){return this.x=Math.round(this.x),this.y=Math.round(this.y),this.z=Math.round(this.z),this}roundToZero(){return this.x=Math.trunc(this.x),this.y=Math.trunc(this.y),this.z=Math.trunc(this.z),this}negate(){return this.x=-this.x,this.y=-this.y,this.z=-this.z,this}dot(e){return this.x*e.x+this.y*e.y+this.z*e.z}lengthSq(){return this.x*this.x+this.y*this.y+this.z*this.z}length(){return Math.sqrt(this.x*this.x+this.y*this.y+this.z*this.z)}manhattanLength(){return Math.abs(this.x)+Math.abs(this.y)+Math.abs(this.z)}normalize(){return this.divideScalar(this.length()||1)}setLength(e){return this.normalize().multiplyScalar(e)}lerp(e,t){return this.x+=(e.x-this.x)*t,this.y+=(e.y-this.y)*t,this.z+=(e.z-this.z)*t,this}lerpVectors(e,t,i){return this.x=e.x+(t.x-e.x)*i,this.y=e.y+(t.y-e.y)*i,this.z=e.z+(t.z-e.z)*i,this}cross(e){return this.crossVectors(this,e)}crossVectors(e,t){const i=e.x,r=e.y,s=e.z,a=t.x,o=t.y,c=t.z;return this.x=r*c-s*o,this.y=s*a-i*c,this.z=i*o-r*a,this}projectOnVector(e){const t=e.lengthSq();if(t===0)return this.set(0,0,0);const i=e.dot(this)/t;return this.copy(e).multiplyScalar(i)}projectOnPlane(e){return is.copy(this).projectOnVector(e),this.sub(is)}reflect(e){return this.sub(is.copy(e).multiplyScalar(2*this.dot(e)))}angleTo(e){const t=Math.sqrt(this.lengthSq()*e.lengthSq());if(t===0)return Math.PI/2;const i=this.dot(e)/t;return Math.acos(Xe(i,-1,1))}distanceTo(e){return Math.sqrt(this.distanceToSquared(e))}distanceToSquared(e){const t=this.x-e.x,i=this.y-e.y,r=this.z-e.z;return t*t+i*i+r*r}manhattanDistanceTo(e){return Math.abs(this.x-e.x)+Math.abs(this.y-e.y)+Math.abs(this.z-e.z)}setFromSpherical(e){return this.setFromSphericalCoords(e.radius,e.phi,e.theta)}setFromSphericalCoords(e,t,i){const r=Math.sin(t)*e;return this.x=r*Math.sin(i),this.y=Math.cos(t)*e,this.z=r*Math.cos(i),this}setFromCylindrical(e){return this.setFromCylindricalCoords(e.radius,e.theta,e.y)}setFromCylindricalCoords(e,t,i){return this.x=e*Math.sin(t),this.y=i,this.z=e*Math.cos(t),this}setFromMatrixPosition(e){const t=e.elements;return this.x=t[12],this.y=t[13],this.z=t[14],this}setFromMatrixScale(e){const t=this.setFromMatrixColumn(e,0).length(),i=this.setFromMatrixColumn(e,1).length(),r=this.setFromMatrixColumn(e,2).length();return this.x=t,this.y=i,this.z=r,this}setFromMatrixColumn(e,t){return this.fromArray(e.elements,t*4)}setFromMatrix3Column(e,t){return this.fromArray(e.elements,t*3)}setFromEuler(e){return this.x=e._x,this.y=e._y,this.z=e._z,this}setFromColor(e){return this.x=e.r,this.y=e.g,this.z=e.b,this}equals(e){return e.x===this.x&&e.y===this.y&&e.z===this.z}fromArray(e,t=0){return this.x=e[t],this.y=e[t+1],this.z=e[t+2],this}toArray(e=[],t=0){return e[t]=this.x,e[t+1]=this.y,e[t+2]=this.z,e}fromBufferAttribute(e,t){return this.x=e.getX(t),this.y=e.getY(t),this.z=e.getZ(t),this}random(){return this.x=Math.random(),this.y=Math.random(),this.z=Math.random(),this}randomDirection(){const e=Math.random()*Math.PI*2,t=Math.random()*2-1,i=Math.sqrt(1-t*t);return this.x=i*Math.cos(e),this.y=t,this.z=i*Math.sin(e),this}*[Symbol.iterator](){yield this.x,yield this.y,yield this.z}}const is=new k,xo=new rr;class Fi{constructor(e=new k(1/0,1/0,1/0),t=new k(-1/0,-1/0,-1/0)){this.isBox3=!0,this.min=e,this.max=t}set(e,t){return this.min.copy(e),this.max.copy(t),this}setFromArray(e){this.makeEmpty();for(let t=0,i=e.length;t<i;t+=3)this.expandByPoint(Xt.fromArray(e,t));return this}setFromBufferAttribute(e){this.makeEmpty();for(let t=0,i=e.count;t<i;t++)this.expandByPoint(Xt.fromBufferAttribute(e,t));return this}setFromPoints(e){this.makeEmpty();for(let t=0,i=e.length;t<i;t++)this.expandByPoint(e[t]);return this}setFromCenterAndSize(e,t){const i=Xt.copy(t).multiplyScalar(.5);return this.min.copy(e).sub(i),this.max.copy(e).add(i),this}setFromObject(e,t=!1){return this.makeEmpty(),this.expandByObject(e,t)}clone(){return new this.constructor().copy(this)}copy(e){return this.min.copy(e.min),this.max.copy(e.max),this}makeEmpty(){return this.min.x=this.min.y=this.min.z=1/0,this.max.x=this.max.y=this.max.z=-1/0,this}isEmpty(){return this.max.x<this.min.x||this.max.y<this.min.y||this.max.z<this.min.z}getCenter(e){return this.isEmpty()?e.set(0,0,0):e.addVectors(this.min,this.max).multiplyScalar(.5)}getSize(e){return this.isEmpty()?e.set(0,0,0):e.subVectors(this.max,this.min)}expandByPoint(e){return this.min.min(e),this.max.max(e),this}expandByVector(e){return this.min.sub(e),this.max.add(e),this}expandByScalar(e){return this.min.addScalar(-e),this.max.addScalar(e),this}expandByObject(e,t=!1){e.updateWorldMatrix(!1,!1);const i=e.geometry;if(i!==void 0){const s=i.getAttribute("position");if(t===!0&&s!==void 0&&e.isInstancedMesh!==!0)for(let a=0,o=s.count;a<o;a++)e.isMesh===!0?e.getVertexPosition(a,Xt):Xt.fromBufferAttribute(s,a),Xt.applyMatrix4(e.matrixWorld),this.expandByPoint(Xt);else e.boundingBox!==void 0?(e.boundingBox===null&&e.computeBoundingBox(),lr.copy(e.boundingBox)):(i.boundingBox===null&&i.computeBoundingBox(),lr.copy(i.boundingBox)),lr.applyMatrix4(e.matrixWorld),this.union(lr)}const r=e.children;for(let s=0,a=r.length;s<a;s++)this.expandByObject(r[s],t);return this}containsPoint(e){return e.x>=this.min.x&&e.x<=this.max.x&&e.y>=this.min.y&&e.y<=this.max.y&&e.z>=this.min.z&&e.z<=this.max.z}containsBox(e){return this.min.x<=e.min.x&&e.max.x<=this.max.x&&this.min.y<=e.min.y&&e.max.y<=this.max.y&&this.min.z<=e.min.z&&e.max.z<=this.max.z}getParameter(e,t){return t.set((e.x-this.min.x)/(this.max.x-this.min.x),(e.y-this.min.y)/(this.max.y-this.min.y),(e.z-this.min.z)/(this.max.z-this.min.z))}intersectsBox(e){return e.max.x>=this.min.x&&e.min.x<=this.max.x&&e.max.y>=this.min.y&&e.min.y<=this.max.y&&e.max.z>=this.min.z&&e.min.z<=this.max.z}intersectsSphere(e){return this.clampPoint(e.center,Xt),Xt.distanceToSquared(e.center)<=e.radius*e.radius}intersectsPlane(e){let t,i;return e.normal.x>0?(t=e.normal.x*this.min.x,i=e.normal.x*this.max.x):(t=e.normal.x*this.max.x,i=e.normal.x*this.min.x),e.normal.y>0?(t+=e.normal.y*this.min.y,i+=e.normal.y*this.max.y):(t+=e.normal.y*this.max.y,i+=e.normal.y*this.min.y),e.normal.z>0?(t+=e.normal.z*this.min.z,i+=e.normal.z*this.max.z):(t+=e.normal.z*this.max.z,i+=e.normal.z*this.min.z),t<=-e.constant&&i>=-e.constant}intersectsTriangle(e){if(this.isEmpty())return!1;this.getCenter(Hi),ur.subVectors(this.max,Hi),oi.subVectors(e.a,Hi),ci.subVectors(e.b,Hi),li.subVectors(e.c,Hi),gn.subVectors(ci,oi),_n.subVectors(li,ci),zn.subVectors(oi,li);let t=[0,-gn.z,gn.y,0,-_n.z,_n.y,0,-zn.z,zn.y,gn.z,0,-gn.x,_n.z,0,-_n.x,zn.z,0,-zn.x,-gn.y,gn.x,0,-_n.y,_n.x,0,-zn.y,zn.x,0];return!rs(t,oi,ci,li,ur)||(t=[1,0,0,0,1,0,0,0,1],!rs(t,oi,ci,li,ur))?!1:(dr.crossVectors(gn,_n),t=[dr.x,dr.y,dr.z],rs(t,oi,ci,li,ur))}clampPoint(e,t){return t.copy(e).clamp(this.min,this.max)}distanceToPoint(e){return this.clampPoint(e,Xt).distanceTo(e)}getBoundingSphere(e){return this.isEmpty()?e.makeEmpty():(this.getCenter(e.center),e.radius=this.getSize(Xt).length()*.5),e}intersect(e){return this.min.max(e.min),this.max.min(e.max),this.isEmpty()&&this.makeEmpty(),this}union(e){return this.min.min(e.min),this.max.max(e.max),this}applyMatrix4(e){return this.isEmpty()?this:(tn[0].set(this.min.x,this.min.y,this.min.z).applyMatrix4(e),tn[1].set(this.min.x,this.min.y,this.max.z).applyMatrix4(e),tn[2].set(this.min.x,this.max.y,this.min.z).applyMatrix4(e),tn[3].set(this.min.x,this.max.y,this.max.z).applyMatrix4(e),tn[4].set(this.max.x,this.min.y,this.min.z).applyMatrix4(e),tn[5].set(this.max.x,this.min.y,this.max.z).applyMatrix4(e),tn[6].set(this.max.x,this.max.y,this.min.z).applyMatrix4(e),tn[7].set(this.max.x,this.max.y,this.max.z).applyMatrix4(e),this.setFromPoints(tn),this)}translate(e){return this.min.add(e),this.max.add(e),this}equals(e){return e.min.equals(this.min)&&e.max.equals(this.max)}}const tn=[new k,new k,new k,new k,new k,new k,new k,new k],Xt=new k,lr=new Fi,oi=new k,ci=new k,li=new k,gn=new k,_n=new k,zn=new k,Hi=new k,ur=new k,dr=new k,Nn=new k;function rs(n,e,t,i,r){for(let s=0,a=n.length-3;s<=a;s+=3){Nn.fromArray(n,s);const o=r.x*Math.abs(Nn.x)+r.y*Math.abs(Nn.y)+r.z*Math.abs(Nn.z),c=e.dot(Nn),l=t.dot(Nn),d=i.dot(Nn);if(Math.max(-Math.max(c,l,d),Math.min(c,l,d))>o)return!1}return!0}const pu=new Fi,Gi=new k,ss=new k;class Yr{constructor(e=new k,t=-1){this.isSphere=!0,this.center=e,this.radius=t}set(e,t){return this.center.copy(e),this.radius=t,this}setFromPoints(e,t){const i=this.center;t!==void 0?i.copy(t):pu.setFromPoints(e).getCenter(i);let r=0;for(let s=0,a=e.length;s<a;s++)r=Math.max(r,i.distanceToSquared(e[s]));return this.radius=Math.sqrt(r),this}copy(e){return this.center.copy(e.center),this.radius=e.radius,this}isEmpty(){return this.radius<0}makeEmpty(){return this.center.set(0,0,0),this.radius=-1,this}containsPoint(e){return e.distanceToSquared(this.center)<=this.radius*this.radius}distanceToPoint(e){return e.distanceTo(this.center)-this.radius}intersectsSphere(e){const t=this.radius+e.radius;return e.center.distanceToSquared(this.center)<=t*t}intersectsBox(e){return e.intersectsSphere(this)}intersectsPlane(e){return Math.abs(e.distanceToPoint(this.center))<=this.radius}clampPoint(e,t){const i=this.center.distanceToSquared(e);return t.copy(e),i>this.radius*this.radius&&(t.sub(this.center).normalize(),t.multiplyScalar(this.radius).add(this.center)),t}getBoundingBox(e){return this.isEmpty()?(e.makeEmpty(),e):(e.set(this.center,this.center),e.expandByScalar(this.radius),e)}applyMatrix4(e){return this.center.applyMatrix4(e),this.radius=this.radius*e.getMaxScaleOnAxis(),this}translate(e){return this.center.add(e),this}expandByPoint(e){if(this.isEmpty())return this.center.copy(e),this.radius=0,this;Gi.subVectors(e,this.center);const t=Gi.lengthSq();if(t>this.radius*this.radius){const i=Math.sqrt(t),r=(i-this.radius)*.5;this.center.addScaledVector(Gi,r/i),this.radius+=r}return this}union(e){return e.isEmpty()?this:this.isEmpty()?(this.copy(e),this):(this.center.equals(e.center)===!0?this.radius=Math.max(this.radius,e.radius):(ss.subVectors(e.center,this.center).setLength(e.radius),this.expandByPoint(Gi.copy(e.center).add(ss)),this.expandByPoint(Gi.copy(e.center).sub(ss))),this)}equals(e){return e.center.equals(this.center)&&e.radius===this.radius}clone(){return new this.constructor().copy(this)}}const nn=new k,as=new k,hr=new k,vn=new k,os=new k,fr=new k,cs=new k;class Ba{constructor(e=new k,t=new k(0,0,-1)){this.origin=e,this.direction=t}set(e,t){return this.origin.copy(e),this.direction.copy(t),this}copy(e){return this.origin.copy(e.origin),this.direction.copy(e.direction),this}at(e,t){return t.copy(this.origin).addScaledVector(this.direction,e)}lookAt(e){return this.direction.copy(e).sub(this.origin).normalize(),this}recast(e){return this.origin.copy(this.at(e,nn)),this}closestPointToPoint(e,t){t.subVectors(e,this.origin);const i=t.dot(this.direction);return i<0?t.copy(this.origin):t.copy(this.origin).addScaledVector(this.direction,i)}distanceToPoint(e){return Math.sqrt(this.distanceSqToPoint(e))}distanceSqToPoint(e){const t=nn.subVectors(e,this.origin).dot(this.direction);return t<0?this.origin.distanceToSquared(e):(nn.copy(this.origin).addScaledVector(this.direction,t),nn.distanceToSquared(e))}distanceSqToSegment(e,t,i,r){as.copy(e).add(t).multiplyScalar(.5),hr.copy(t).sub(e).normalize(),vn.copy(this.origin).sub(as);const s=e.distanceTo(t)*.5,a=-this.direction.dot(hr),o=vn.dot(this.direction),c=-vn.dot(hr),l=vn.lengthSq(),d=Math.abs(1-a*a);let h,f,m,g;if(d>0)if(h=a*c-o,f=a*o-c,g=s*d,h>=0)if(f>=-g)if(f<=g){const _=1/d;h*=_,f*=_,m=h*(h+a*f+2*o)+f*(a*h+f+2*c)+l}else f=s,h=Math.max(0,-(a*f+o)),m=-h*h+f*(f+2*c)+l;else f=-s,h=Math.max(0,-(a*f+o)),m=-h*h+f*(f+2*c)+l;else f<=-g?(h=Math.max(0,-(-a*s+o)),f=h>0?-s:Math.min(Math.max(-s,-c),s),m=-h*h+f*(f+2*c)+l):f<=g?(h=0,f=Math.min(Math.max(-s,-c),s),m=f*(f+2*c)+l):(h=Math.max(0,-(a*s+o)),f=h>0?s:Math.min(Math.max(-s,-c),s),m=-h*h+f*(f+2*c)+l);else f=a>0?-s:s,h=Math.max(0,-(a*f+o)),m=-h*h+f*(f+2*c)+l;return i&&i.copy(this.origin).addScaledVector(this.direction,h),r&&r.copy(as).addScaledVector(hr,f),m}intersectSphere(e,t){nn.subVectors(e.center,this.origin);const i=nn.dot(this.direction),r=nn.dot(nn)-i*i,s=e.radius*e.radius;if(r>s)return null;const a=Math.sqrt(s-r),o=i-a,c=i+a;return c<0?null:o<0?this.at(c,t):this.at(o,t)}intersectsSphere(e){return this.distanceSqToPoint(e.center)<=e.radius*e.radius}distanceToPlane(e){const t=e.normal.dot(this.direction);if(t===0)return e.distanceToPoint(this.origin)===0?0:null;const i=-(this.origin.dot(e.normal)+e.constant)/t;return i>=0?i:null}intersectPlane(e,t){const i=this.distanceToPlane(e);return i===null?null:this.at(i,t)}intersectsPlane(e){const t=e.distanceToPoint(this.origin);return t===0||e.normal.dot(this.direction)*t<0}intersectBox(e,t){let i,r,s,a,o,c;const l=1/this.direction.x,d=1/this.direction.y,h=1/this.direction.z,f=this.origin;return l>=0?(i=(e.min.x-f.x)*l,r=(e.max.x-f.x)*l):(i=(e.max.x-f.x)*l,r=(e.min.x-f.x)*l),d>=0?(s=(e.min.y-f.y)*d,a=(e.max.y-f.y)*d):(s=(e.max.y-f.y)*d,a=(e.min.y-f.y)*d),i>a||s>r||((s>i||isNaN(i))&&(i=s),(a<r||isNaN(r))&&(r=a),h>=0?(o=(e.min.z-f.z)*h,c=(e.max.z-f.z)*h):(o=(e.max.z-f.z)*h,c=(e.min.z-f.z)*h),i>c||o>r)||((o>i||i!==i)&&(i=o),(c<r||r!==r)&&(r=c),r<0)?null:this.at(i>=0?i:r,t)}intersectsBox(e){return this.intersectBox(e,nn)!==null}intersectTriangle(e,t,i,r,s){os.subVectors(t,e),fr.subVectors(i,e),cs.crossVectors(os,fr);let a=this.direction.dot(cs),o;if(a>0){if(r)return null;o=1}else if(a<0)o=-1,a=-a;else return null;vn.subVectors(this.origin,e);const c=o*this.direction.dot(fr.crossVectors(vn,fr));if(c<0)return null;const l=o*this.direction.dot(os.cross(vn));if(l<0||c+l>a)return null;const d=-o*vn.dot(cs);return d<0?null:this.at(d/a,s)}applyMatrix4(e){return this.origin.applyMatrix4(e),this.direction.transformDirection(e),this}equals(e){return e.origin.equals(this.origin)&&e.direction.equals(this.direction)}clone(){return new this.constructor().copy(this)}}class at{constructor(e,t,i,r,s,a,o,c,l,d,h,f,m,g,_,p){at.prototype.isMatrix4=!0,this.elements=[1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1],e!==void 0&&this.set(e,t,i,r,s,a,o,c,l,d,h,f,m,g,_,p)}set(e,t,i,r,s,a,o,c,l,d,h,f,m,g,_,p){const u=this.elements;return u[0]=e,u[4]=t,u[8]=i,u[12]=r,u[1]=s,u[5]=a,u[9]=o,u[13]=c,u[2]=l,u[6]=d,u[10]=h,u[14]=f,u[3]=m,u[7]=g,u[11]=_,u[15]=p,this}identity(){return this.set(1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1),this}clone(){return new at().fromArray(this.elements)}copy(e){const t=this.elements,i=e.elements;return t[0]=i[0],t[1]=i[1],t[2]=i[2],t[3]=i[3],t[4]=i[4],t[5]=i[5],t[6]=i[6],t[7]=i[7],t[8]=i[8],t[9]=i[9],t[10]=i[10],t[11]=i[11],t[12]=i[12],t[13]=i[13],t[14]=i[14],t[15]=i[15],this}copyPosition(e){const t=this.elements,i=e.elements;return t[12]=i[12],t[13]=i[13],t[14]=i[14],this}setFromMatrix3(e){const t=e.elements;return this.set(t[0],t[3],t[6],0,t[1],t[4],t[7],0,t[2],t[5],t[8],0,0,0,0,1),this}extractBasis(e,t,i){return e.setFromMatrixColumn(this,0),t.setFromMatrixColumn(this,1),i.setFromMatrixColumn(this,2),this}makeBasis(e,t,i){return this.set(e.x,t.x,i.x,0,e.y,t.y,i.y,0,e.z,t.z,i.z,0,0,0,0,1),this}extractRotation(e){const t=this.elements,i=e.elements,r=1/ui.setFromMatrixColumn(e,0).length(),s=1/ui.setFromMatrixColumn(e,1).length(),a=1/ui.setFromMatrixColumn(e,2).length();return t[0]=i[0]*r,t[1]=i[1]*r,t[2]=i[2]*r,t[3]=0,t[4]=i[4]*s,t[5]=i[5]*s,t[6]=i[6]*s,t[7]=0,t[8]=i[8]*a,t[9]=i[9]*a,t[10]=i[10]*a,t[11]=0,t[12]=0,t[13]=0,t[14]=0,t[15]=1,this}makeRotationFromEuler(e){const t=this.elements,i=e.x,r=e.y,s=e.z,a=Math.cos(i),o=Math.sin(i),c=Math.cos(r),l=Math.sin(r),d=Math.cos(s),h=Math.sin(s);if(e.order==="XYZ"){const f=a*d,m=a*h,g=o*d,_=o*h;t[0]=c*d,t[4]=-c*h,t[8]=l,t[1]=m+g*l,t[5]=f-_*l,t[9]=-o*c,t[2]=_-f*l,t[6]=g+m*l,t[10]=a*c}else if(e.order==="YXZ"){const f=c*d,m=c*h,g=l*d,_=l*h;t[0]=f+_*o,t[4]=g*o-m,t[8]=a*l,t[1]=a*h,t[5]=a*d,t[9]=-o,t[2]=m*o-g,t[6]=_+f*o,t[10]=a*c}else if(e.order==="ZXY"){const f=c*d,m=c*h,g=l*d,_=l*h;t[0]=f-_*o,t[4]=-a*h,t[8]=g+m*o,t[1]=m+g*o,t[5]=a*d,t[9]=_-f*o,t[2]=-a*l,t[6]=o,t[10]=a*c}else if(e.order==="ZYX"){const f=a*d,m=a*h,g=o*d,_=o*h;t[0]=c*d,t[4]=g*l-m,t[8]=f*l+_,t[1]=c*h,t[5]=_*l+f,t[9]=m*l-g,t[2]=-l,t[6]=o*c,t[10]=a*c}else if(e.order==="YZX"){const f=a*c,m=a*l,g=o*c,_=o*l;t[0]=c*d,t[4]=_-f*h,t[8]=g*h+m,t[1]=h,t[5]=a*d,t[9]=-o*d,t[2]=-l*d,t[6]=m*h+g,t[10]=f-_*h}else if(e.order==="XZY"){const f=a*c,m=a*l,g=o*c,_=o*l;t[0]=c*d,t[4]=-h,t[8]=l*d,t[1]=f*h+_,t[5]=a*d,t[9]=m*h-g,t[2]=g*h-m,t[6]=o*d,t[10]=_*h+f}return t[3]=0,t[7]=0,t[11]=0,t[12]=0,t[13]=0,t[14]=0,t[15]=1,this}makeRotationFromQuaternion(e){return this.compose(mu,e,gu)}lookAt(e,t,i){const r=this.elements;return Ut.subVectors(e,t),Ut.lengthSq()===0&&(Ut.z=1),Ut.normalize(),xn.crossVectors(i,Ut),xn.lengthSq()===0&&(Math.abs(i.z)===1?Ut.x+=1e-4:Ut.z+=1e-4,Ut.normalize(),xn.crossVectors(i,Ut)),xn.normalize(),pr.crossVectors(Ut,xn),r[0]=xn.x,r[4]=pr.x,r[8]=Ut.x,r[1]=xn.y,r[5]=pr.y,r[9]=Ut.y,r[2]=xn.z,r[6]=pr.z,r[10]=Ut.z,this}multiply(e){return this.multiplyMatrices(this,e)}premultiply(e){return this.multiplyMatrices(e,this)}multiplyMatrices(e,t){const i=e.elements,r=t.elements,s=this.elements,a=i[0],o=i[4],c=i[8],l=i[12],d=i[1],h=i[5],f=i[9],m=i[13],g=i[2],_=i[6],p=i[10],u=i[14],E=i[3],y=i[7],M=i[11],D=i[15],w=r[0],b=r[4],C=r[8],v=r[12],x=r[1],P=r[5],U=r[9],A=r[13],R=r[2],z=r[6],N=r[10],O=r[14],F=r[3],G=r[7],Z=r[11],Y=r[15];return s[0]=a*w+o*x+c*R+l*F,s[4]=a*b+o*P+c*z+l*G,s[8]=a*C+o*U+c*N+l*Z,s[12]=a*v+o*A+c*O+l*Y,s[1]=d*w+h*x+f*R+m*F,s[5]=d*b+h*P+f*z+m*G,s[9]=d*C+h*U+f*N+m*Z,s[13]=d*v+h*A+f*O+m*Y,s[2]=g*w+_*x+p*R+u*F,s[6]=g*b+_*P+p*z+u*G,s[10]=g*C+_*U+p*N+u*Z,s[14]=g*v+_*A+p*O+u*Y,s[3]=E*w+y*x+M*R+D*F,s[7]=E*b+y*P+M*z+D*G,s[11]=E*C+y*U+M*N+D*Z,s[15]=E*v+y*A+M*O+D*Y,this}multiplyScalar(e){const t=this.elements;return t[0]*=e,t[4]*=e,t[8]*=e,t[12]*=e,t[1]*=e,t[5]*=e,t[9]*=e,t[13]*=e,t[2]*=e,t[6]*=e,t[10]*=e,t[14]*=e,t[3]*=e,t[7]*=e,t[11]*=e,t[15]*=e,this}determinant(){const e=this.elements,t=e[0],i=e[4],r=e[8],s=e[12],a=e[1],o=e[5],c=e[9],l=e[13],d=e[2],h=e[6],f=e[10],m=e[14],g=e[3],_=e[7],p=e[11],u=e[15];return g*(+s*c*h-r*l*h-s*o*f+i*l*f+r*o*m-i*c*m)+_*(+t*c*m-t*l*f+s*a*f-r*a*m+r*l*d-s*c*d)+p*(+t*l*h-t*o*m-s*a*h+i*a*m+s*o*d-i*l*d)+u*(-r*o*d-t*c*h+t*o*f+r*a*h-i*a*f+i*c*d)}transpose(){const e=this.elements;let t;return t=e[1],e[1]=e[4],e[4]=t,t=e[2],e[2]=e[8],e[8]=t,t=e[6],e[6]=e[9],e[9]=t,t=e[3],e[3]=e[12],e[12]=t,t=e[7],e[7]=e[13],e[13]=t,t=e[11],e[11]=e[14],e[14]=t,this}setPosition(e,t,i){const r=this.elements;return e.isVector3?(r[12]=e.x,r[13]=e.y,r[14]=e.z):(r[12]=e,r[13]=t,r[14]=i),this}invert(){const e=this.elements,t=e[0],i=e[1],r=e[2],s=e[3],a=e[4],o=e[5],c=e[6],l=e[7],d=e[8],h=e[9],f=e[10],m=e[11],g=e[12],_=e[13],p=e[14],u=e[15],E=h*p*l-_*f*l+_*c*m-o*p*m-h*c*u+o*f*u,y=g*f*l-d*p*l-g*c*m+a*p*m+d*c*u-a*f*u,M=d*_*l-g*h*l+g*o*m-a*_*m-d*o*u+a*h*u,D=g*h*c-d*_*c-g*o*f+a*_*f+d*o*p-a*h*p,w=t*E+i*y+r*M+s*D;if(w===0)return this.set(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);const b=1/w;return e[0]=E*b,e[1]=(_*f*s-h*p*s-_*r*m+i*p*m+h*r*u-i*f*u)*b,e[2]=(o*p*s-_*c*s+_*r*l-i*p*l-o*r*u+i*c*u)*b,e[3]=(h*c*s-o*f*s-h*r*l+i*f*l+o*r*m-i*c*m)*b,e[4]=y*b,e[5]=(d*p*s-g*f*s+g*r*m-t*p*m-d*r*u+t*f*u)*b,e[6]=(g*c*s-a*p*s-g*r*l+t*p*l+a*r*u-t*c*u)*b,e[7]=(a*f*s-d*c*s+d*r*l-t*f*l-a*r*m+t*c*m)*b,e[8]=M*b,e[9]=(g*h*s-d*_*s-g*i*m+t*_*m+d*i*u-t*h*u)*b,e[10]=(a*_*s-g*o*s+g*i*l-t*_*l-a*i*u+t*o*u)*b,e[11]=(d*o*s-a*h*s-d*i*l+t*h*l+a*i*m-t*o*m)*b,e[12]=D*b,e[13]=(d*_*r-g*h*r+g*i*f-t*_*f-d*i*p+t*h*p)*b,e[14]=(g*o*r-a*_*r-g*i*c+t*_*c+a*i*p-t*o*p)*b,e[15]=(a*h*r-d*o*r+d*i*c-t*h*c-a*i*f+t*o*f)*b,this}scale(e){const t=this.elements,i=e.x,r=e.y,s=e.z;return t[0]*=i,t[4]*=r,t[8]*=s,t[1]*=i,t[5]*=r,t[9]*=s,t[2]*=i,t[6]*=r,t[10]*=s,t[3]*=i,t[7]*=r,t[11]*=s,this}getMaxScaleOnAxis(){const e=this.elements,t=e[0]*e[0]+e[1]*e[1]+e[2]*e[2],i=e[4]*e[4]+e[5]*e[5]+e[6]*e[6],r=e[8]*e[8]+e[9]*e[9]+e[10]*e[10];return Math.sqrt(Math.max(t,i,r))}makeTranslation(e,t,i){return e.isVector3?this.set(1,0,0,e.x,0,1,0,e.y,0,0,1,e.z,0,0,0,1):this.set(1,0,0,e,0,1,0,t,0,0,1,i,0,0,0,1),this}makeRotationX(e){const t=Math.cos(e),i=Math.sin(e);return this.set(1,0,0,0,0,t,-i,0,0,i,t,0,0,0,0,1),this}makeRotationY(e){const t=Math.cos(e),i=Math.sin(e);return this.set(t,0,i,0,0,1,0,0,-i,0,t,0,0,0,0,1),this}makeRotationZ(e){const t=Math.cos(e),i=Math.sin(e);return this.set(t,-i,0,0,i,t,0,0,0,0,1,0,0,0,0,1),this}makeRotationAxis(e,t){const i=Math.cos(t),r=Math.sin(t),s=1-i,a=e.x,o=e.y,c=e.z,l=s*a,d=s*o;return this.set(l*a+i,l*o-r*c,l*c+r*o,0,l*o+r*c,d*o+i,d*c-r*a,0,l*c-r*o,d*c+r*a,s*c*c+i,0,0,0,0,1),this}makeScale(e,t,i){return this.set(e,0,0,0,0,t,0,0,0,0,i,0,0,0,0,1),this}makeShear(e,t,i,r,s,a){return this.set(1,i,s,0,e,1,a,0,t,r,1,0,0,0,0,1),this}compose(e,t,i){const r=this.elements,s=t._x,a=t._y,o=t._z,c=t._w,l=s+s,d=a+a,h=o+o,f=s*l,m=s*d,g=s*h,_=a*d,p=a*h,u=o*h,E=c*l,y=c*d,M=c*h,D=i.x,w=i.y,b=i.z;return r[0]=(1-(_+u))*D,r[1]=(m+M)*D,r[2]=(g-y)*D,r[3]=0,r[4]=(m-M)*w,r[5]=(1-(f+u))*w,r[6]=(p+E)*w,r[7]=0,r[8]=(g+y)*b,r[9]=(p-E)*b,r[10]=(1-(f+_))*b,r[11]=0,r[12]=e.x,r[13]=e.y,r[14]=e.z,r[15]=1,this}decompose(e,t,i){const r=this.elements;let s=ui.set(r[0],r[1],r[2]).length();const a=ui.set(r[4],r[5],r[6]).length(),o=ui.set(r[8],r[9],r[10]).length();this.determinant()<0&&(s=-s),e.x=r[12],e.y=r[13],e.z=r[14],qt.copy(this);const l=1/s,d=1/a,h=1/o;return qt.elements[0]*=l,qt.elements[1]*=l,qt.elements[2]*=l,qt.elements[4]*=d,qt.elements[5]*=d,qt.elements[6]*=d,qt.elements[8]*=h,qt.elements[9]*=h,qt.elements[10]*=h,t.setFromRotationMatrix(qt),i.x=s,i.y=a,i.z=o,this}makePerspective(e,t,i,r,s,a,o=hn){const c=this.elements,l=2*s/(t-e),d=2*s/(i-r),h=(t+e)/(t-e),f=(i+r)/(i-r);let m,g;if(o===hn)m=-(a+s)/(a-s),g=-2*a*s/(a-s);else if(o===jr)m=-a/(a-s),g=-a*s/(a-s);else throw new Error("THREE.Matrix4.makePerspective(): Invalid coordinate system: "+o);return c[0]=l,c[4]=0,c[8]=h,c[12]=0,c[1]=0,c[5]=d,c[9]=f,c[13]=0,c[2]=0,c[6]=0,c[10]=m,c[14]=g,c[3]=0,c[7]=0,c[11]=-1,c[15]=0,this}makeOrthographic(e,t,i,r,s,a,o=hn){const c=this.elements,l=1/(t-e),d=1/(i-r),h=1/(a-s),f=(t+e)*l,m=(i+r)*d;let g,_;if(o===hn)g=(a+s)*h,_=-2*h;else if(o===jr)g=s*h,_=-1*h;else throw new Error("THREE.Matrix4.makeOrthographic(): Invalid coordinate system: "+o);return c[0]=2*l,c[4]=0,c[8]=0,c[12]=-f,c[1]=0,c[5]=2*d,c[9]=0,c[13]=-m,c[2]=0,c[6]=0,c[10]=_,c[14]=-g,c[3]=0,c[7]=0,c[11]=0,c[15]=1,this}equals(e){const t=this.elements,i=e.elements;for(let r=0;r<16;r++)if(t[r]!==i[r])return!1;return!0}fromArray(e,t=0){for(let i=0;i<16;i++)this.elements[i]=e[i+t];return this}toArray(e=[],t=0){const i=this.elements;return e[t]=i[0],e[t+1]=i[1],e[t+2]=i[2],e[t+3]=i[3],e[t+4]=i[4],e[t+5]=i[5],e[t+6]=i[6],e[t+7]=i[7],e[t+8]=i[8],e[t+9]=i[9],e[t+10]=i[10],e[t+11]=i[11],e[t+12]=i[12],e[t+13]=i[13],e[t+14]=i[14],e[t+15]=i[15],e}}const ui=new k,qt=new at,mu=new k(0,0,0),gu=new k(1,1,1),xn=new k,pr=new k,Ut=new k,Mo=new at,So=new rr;class xt{constructor(e=0,t=0,i=0,r=xt.DEFAULT_ORDER){this.isEuler=!0,this._x=e,this._y=t,this._z=i,this._order=r}get x(){return this._x}set x(e){this._x=e,this._onChangeCallback()}get y(){return this._y}set y(e){this._y=e,this._onChangeCallback()}get z(){return this._z}set z(e){this._z=e,this._onChangeCallback()}get order(){return this._order}set order(e){this._order=e,this._onChangeCallback()}set(e,t,i,r=this._order){return this._x=e,this._y=t,this._z=i,this._order=r,this._onChangeCallback(),this}clone(){return new this.constructor(this._x,this._y,this._z,this._order)}copy(e){return this._x=e._x,this._y=e._y,this._z=e._z,this._order=e._order,this._onChangeCallback(),this}setFromRotationMatrix(e,t=this._order,i=!0){const r=e.elements,s=r[0],a=r[4],o=r[8],c=r[1],l=r[5],d=r[9],h=r[2],f=r[6],m=r[10];switch(t){case"XYZ":this._y=Math.asin(Xe(o,-1,1)),Math.abs(o)<.9999999?(this._x=Math.atan2(-d,m),this._z=Math.atan2(-a,s)):(this._x=Math.atan2(f,l),this._z=0);break;case"YXZ":this._x=Math.asin(-Xe(d,-1,1)),Math.abs(d)<.9999999?(this._y=Math.atan2(o,m),this._z=Math.atan2(c,l)):(this._y=Math.atan2(-h,s),this._z=0);break;case"ZXY":this._x=Math.asin(Xe(f,-1,1)),Math.abs(f)<.9999999?(this._y=Math.atan2(-h,m),this._z=Math.atan2(-a,l)):(this._y=0,this._z=Math.atan2(c,s));break;case"ZYX":this._y=Math.asin(-Xe(h,-1,1)),Math.abs(h)<.9999999?(this._x=Math.atan2(f,m),this._z=Math.atan2(c,s)):(this._x=0,this._z=Math.atan2(-a,l));break;case"YZX":this._z=Math.asin(Xe(c,-1,1)),Math.abs(c)<.9999999?(this._x=Math.atan2(-d,l),this._y=Math.atan2(-h,s)):(this._x=0,this._y=Math.atan2(o,m));break;case"XZY":this._z=Math.asin(-Xe(a,-1,1)),Math.abs(a)<.9999999?(this._x=Math.atan2(f,l),this._y=Math.atan2(o,s)):(this._x=Math.atan2(-d,m),this._y=0);break;default:console.warn("THREE.Euler: .setFromRotationMatrix() encountered an unknown order: "+t)}return this._order=t,i===!0&&this._onChangeCallback(),this}setFromQuaternion(e,t,i){return Mo.makeRotationFromQuaternion(e),this.setFromRotationMatrix(Mo,t,i)}setFromVector3(e,t=this._order){return this.set(e.x,e.y,e.z,t)}reorder(e){return So.setFromEuler(this),this.setFromQuaternion(So,e)}equals(e){return e._x===this._x&&e._y===this._y&&e._z===this._z&&e._order===this._order}fromArray(e){return this._x=e[0],this._y=e[1],this._z=e[2],e[3]!==void 0&&(this._order=e[3]),this._onChangeCallback(),this}toArray(e=[],t=0){return e[t]=this._x,e[t+1]=this._y,e[t+2]=this._z,e[t+3]=this._order,e}_onChange(e){return this._onChangeCallback=e,this}_onChangeCallback(){}*[Symbol.iterator](){yield this._x,yield this._y,yield this._z,yield this._order}}xt.DEFAULT_ORDER="XYZ";class Va{constructor(){this.mask=1}set(e){this.mask=(1<<e|0)>>>0}enable(e){this.mask|=1<<e|0}enableAll(){this.mask=-1}toggle(e){this.mask^=1<<e|0}disable(e){this.mask&=~(1<<e|0)}disableAll(){this.mask=0}test(e){return(this.mask&e.mask)!==0}isEnabled(e){return(this.mask&(1<<e|0))!==0}}let _u=0;const Eo=new k,di=new rr,rn=new at,mr=new k,ji=new k,vu=new k,xu=new rr,yo=new k(1,0,0),bo=new k(0,1,0),To=new k(0,0,1),Ao={type:"added"},Mu={type:"removed"},hi={type:"childadded",child:null},ls={type:"childremoved",child:null};class St extends Ni{constructor(){super(),this.isObject3D=!0,Object.defineProperty(this,"id",{value:_u++}),this.uuid=ir(),this.name="",this.type="Object3D",this.parent=null,this.children=[],this.up=St.DEFAULT_UP.clone();const e=new k,t=new xt,i=new rr,r=new k(1,1,1);function s(){i.setFromEuler(t,!1)}function a(){t.setFromQuaternion(i,void 0,!1)}t._onChange(s),i._onChange(a),Object.defineProperties(this,{position:{configurable:!0,enumerable:!0,value:e},rotation:{configurable:!0,enumerable:!0,value:t},quaternion:{configurable:!0,enumerable:!0,value:i},scale:{configurable:!0,enumerable:!0,value:r},modelViewMatrix:{value:new at},normalMatrix:{value:new Ve}}),this.matrix=new at,this.matrixWorld=new at,this.matrixAutoUpdate=St.DEFAULT_MATRIX_AUTO_UPDATE,this.matrixWorldAutoUpdate=St.DEFAULT_MATRIX_WORLD_AUTO_UPDATE,this.matrixWorldNeedsUpdate=!1,this.layers=new Va,this.visible=!0,this.castShadow=!1,this.receiveShadow=!1,this.frustumCulled=!0,this.renderOrder=0,this.animations=[],this.userData={}}onBeforeShadow(){}onAfterShadow(){}onBeforeRender(){}onAfterRender(){}applyMatrix4(e){this.matrixAutoUpdate&&this.updateMatrix(),this.matrix.premultiply(e),this.matrix.decompose(this.position,this.quaternion,this.scale)}applyQuaternion(e){return this.quaternion.premultiply(e),this}setRotationFromAxisAngle(e,t){this.quaternion.setFromAxisAngle(e,t)}setRotationFromEuler(e){this.quaternion.setFromEuler(e,!0)}setRotationFromMatrix(e){this.quaternion.setFromRotationMatrix(e)}setRotationFromQuaternion(e){this.quaternion.copy(e)}rotateOnAxis(e,t){return di.setFromAxisAngle(e,t),this.quaternion.multiply(di),this}rotateOnWorldAxis(e,t){return di.setFromAxisAngle(e,t),this.quaternion.premultiply(di),this}rotateX(e){return this.rotateOnAxis(yo,e)}rotateY(e){return this.rotateOnAxis(bo,e)}rotateZ(e){return this.rotateOnAxis(To,e)}translateOnAxis(e,t){return Eo.copy(e).applyQuaternion(this.quaternion),this.position.add(Eo.multiplyScalar(t)),this}translateX(e){return this.translateOnAxis(yo,e)}translateY(e){return this.translateOnAxis(bo,e)}translateZ(e){return this.translateOnAxis(To,e)}localToWorld(e){return this.updateWorldMatrix(!0,!1),e.applyMatrix4(this.matrixWorld)}worldToLocal(e){return this.updateWorldMatrix(!0,!1),e.applyMatrix4(rn.copy(this.matrixWorld).invert())}lookAt(e,t,i){e.isVector3?mr.copy(e):mr.set(e,t,i);const r=this.parent;this.updateWorldMatrix(!0,!1),ji.setFromMatrixPosition(this.matrixWorld),this.isCamera||this.isLight?rn.lookAt(ji,mr,this.up):rn.lookAt(mr,ji,this.up),this.quaternion.setFromRotationMatrix(rn),r&&(rn.extractRotation(r.matrixWorld),di.setFromRotationMatrix(rn),this.quaternion.premultiply(di.invert()))}add(e){if(arguments.length>1){for(let t=0;t<arguments.length;t++)this.add(arguments[t]);return this}return e===this?(console.error("THREE.Object3D.add: object can't be added as a child of itself.",e),this):(e&&e.isObject3D?(e.removeFromParent(),e.parent=this,this.children.push(e),e.dispatchEvent(Ao),hi.child=e,this.dispatchEvent(hi),hi.child=null):console.error("THREE.Object3D.add: object not an instance of THREE.Object3D.",e),this)}remove(e){if(arguments.length>1){for(let i=0;i<arguments.length;i++)this.remove(arguments[i]);return this}const t=this.children.indexOf(e);return t!==-1&&(e.parent=null,this.children.splice(t,1),e.dispatchEvent(Mu),ls.child=e,this.dispatchEvent(ls),ls.child=null),this}removeFromParent(){const e=this.parent;return e!==null&&e.remove(this),this}clear(){return this.remove(...this.children)}attach(e){return this.updateWorldMatrix(!0,!1),rn.copy(this.matrixWorld).invert(),e.parent!==null&&(e.parent.updateWorldMatrix(!0,!1),rn.multiply(e.parent.matrixWorld)),e.applyMatrix4(rn),e.removeFromParent(),e.parent=this,this.children.push(e),e.updateWorldMatrix(!1,!0),e.dispatchEvent(Ao),hi.child=e,this.dispatchEvent(hi),hi.child=null,this}getObjectById(e){return this.getObjectByProperty("id",e)}getObjectByName(e){return this.getObjectByProperty("name",e)}getObjectByProperty(e,t){if(this[e]===t)return this;for(let i=0,r=this.children.length;i<r;i++){const a=this.children[i].getObjectByProperty(e,t);if(a!==void 0)return a}}getObjectsByProperty(e,t,i=[]){this[e]===t&&i.push(this);const r=this.children;for(let s=0,a=r.length;s<a;s++)r[s].getObjectsByProperty(e,t,i);return i}getWorldPosition(e){return this.updateWorldMatrix(!0,!1),e.setFromMatrixPosition(this.matrixWorld)}getWorldQuaternion(e){return this.updateWorldMatrix(!0,!1),this.matrixWorld.decompose(ji,e,vu),e}getWorldScale(e){return this.updateWorldMatrix(!0,!1),this.matrixWorld.decompose(ji,xu,e),e}getWorldDirection(e){this.updateWorldMatrix(!0,!1);const t=this.matrixWorld.elements;return e.set(t[8],t[9],t[10]).normalize()}raycast(){}traverse(e){e(this);const t=this.children;for(let i=0,r=t.length;i<r;i++)t[i].traverse(e)}traverseVisible(e){if(this.visible===!1)return;e(this);const t=this.children;for(let i=0,r=t.length;i<r;i++)t[i].traverseVisible(e)}traverseAncestors(e){const t=this.parent;t!==null&&(e(t),t.traverseAncestors(e))}updateMatrix(){this.matrix.compose(this.position,this.quaternion,this.scale),this.matrixWorldNeedsUpdate=!0}updateMatrixWorld(e){this.matrixAutoUpdate&&this.updateMatrix(),(this.matrixWorldNeedsUpdate||e)&&(this.matrixWorldAutoUpdate===!0&&(this.parent===null?this.matrixWorld.copy(this.matrix):this.matrixWorld.multiplyMatrices(this.parent.matrixWorld,this.matrix)),this.matrixWorldNeedsUpdate=!1,e=!0);const t=this.children;for(let i=0,r=t.length;i<r;i++)t[i].updateMatrixWorld(e)}updateWorldMatrix(e,t){const i=this.parent;if(e===!0&&i!==null&&i.updateWorldMatrix(!0,!1),this.matrixAutoUpdate&&this.updateMatrix(),this.matrixWorldAutoUpdate===!0&&(this.parent===null?this.matrixWorld.copy(this.matrix):this.matrixWorld.multiplyMatrices(this.parent.matrixWorld,this.matrix)),t===!0){const r=this.children;for(let s=0,a=r.length;s<a;s++)r[s].updateWorldMatrix(!1,!0)}}toJSON(e){const t=e===void 0||typeof e=="string",i={};t&&(e={geometries:{},materials:{},textures:{},images:{},shapes:{},skeletons:{},animations:{},nodes:{}},i.metadata={version:4.6,type:"Object",generator:"Object3D.toJSON"});const r={};r.uuid=this.uuid,r.type=this.type,this.name!==""&&(r.name=this.name),this.castShadow===!0&&(r.castShadow=!0),this.receiveShadow===!0&&(r.receiveShadow=!0),this.visible===!1&&(r.visible=!1),this.frustumCulled===!1&&(r.frustumCulled=!1),this.renderOrder!==0&&(r.renderOrder=this.renderOrder),Object.keys(this.userData).length>0&&(r.userData=this.userData),r.layers=this.layers.mask,r.matrix=this.matrix.toArray(),r.up=this.up.toArray(),this.matrixAutoUpdate===!1&&(r.matrixAutoUpdate=!1),this.isInstancedMesh&&(r.type="InstancedMesh",r.count=this.count,r.instanceMatrix=this.instanceMatrix.toJSON(),this.instanceColor!==null&&(r.instanceColor=this.instanceColor.toJSON())),this.isBatchedMesh&&(r.type="BatchedMesh",r.perObjectFrustumCulled=this.perObjectFrustumCulled,r.sortObjects=this.sortObjects,r.drawRanges=this._drawRanges,r.reservedRanges=this._reservedRanges,r.visibility=this._visibility,r.active=this._active,r.bounds=this._bounds.map(o=>({boxInitialized:o.boxInitialized,boxMin:o.box.min.toArray(),boxMax:o.box.max.toArray(),sphereInitialized:o.sphereInitialized,sphereRadius:o.sphere.radius,sphereCenter:o.sphere.center.toArray()})),r.maxInstanceCount=this._maxInstanceCount,r.maxVertexCount=this._maxVertexCount,r.maxIndexCount=this._maxIndexCount,r.geometryInitialized=this._geometryInitialized,r.geometryCount=this._geometryCount,r.matricesTexture=this._matricesTexture.toJSON(e),this._colorsTexture!==null&&(r.colorsTexture=this._colorsTexture.toJSON(e)),this.boundingSphere!==null&&(r.boundingSphere={center:r.boundingSphere.center.toArray(),radius:r.boundingSphere.radius}),this.boundingBox!==null&&(r.boundingBox={min:r.boundingBox.min.toArray(),max:r.boundingBox.max.toArray()}));function s(o,c){return o[c.uuid]===void 0&&(o[c.uuid]=c.toJSON(e)),c.uuid}if(this.isScene)this.background&&(this.background.isColor?r.background=this.background.toJSON():this.background.isTexture&&(r.background=this.background.toJSON(e).uuid)),this.environment&&this.environment.isTexture&&this.environment.isRenderTargetTexture!==!0&&(r.environment=this.environment.toJSON(e).uuid);else if(this.isMesh||this.isLine||this.isPoints){r.geometry=s(e.geometries,this.geometry);const o=this.geometry.parameters;if(o!==void 0&&o.shapes!==void 0){const c=o.shapes;if(Array.isArray(c))for(let l=0,d=c.length;l<d;l++){const h=c[l];s(e.shapes,h)}else s(e.shapes,c)}}if(this.isSkinnedMesh&&(r.bindMode=this.bindMode,r.bindMatrix=this.bindMatrix.toArray(),this.skeleton!==void 0&&(s(e.skeletons,this.skeleton),r.skeleton=this.skeleton.uuid)),this.material!==void 0)if(Array.isArray(this.material)){const o=[];for(let c=0,l=this.material.length;c<l;c++)o.push(s(e.materials,this.material[c]));r.material=o}else r.material=s(e.materials,this.material);if(this.children.length>0){r.children=[];for(let o=0;o<this.children.length;o++)r.children.push(this.children[o].toJSON(e).object)}if(this.animations.length>0){r.animations=[];for(let o=0;o<this.animations.length;o++){const c=this.animations[o];r.animations.push(s(e.animations,c))}}if(t){const o=a(e.geometries),c=a(e.materials),l=a(e.textures),d=a(e.images),h=a(e.shapes),f=a(e.skeletons),m=a(e.animations),g=a(e.nodes);o.length>0&&(i.geometries=o),c.length>0&&(i.materials=c),l.length>0&&(i.textures=l),d.length>0&&(i.images=d),h.length>0&&(i.shapes=h),f.length>0&&(i.skeletons=f),m.length>0&&(i.animations=m),g.length>0&&(i.nodes=g)}return i.object=r,i;function a(o){const c=[];for(const l in o){const d=o[l];delete d.metadata,c.push(d)}return c}}clone(e){return new this.constructor().copy(this,e)}copy(e,t=!0){if(this.name=e.name,this.up.copy(e.up),this.position.copy(e.position),this.rotation.order=e.rotation.order,this.quaternion.copy(e.quaternion),this.scale.copy(e.scale),this.matrix.copy(e.matrix),this.matrixWorld.copy(e.matrixWorld),this.matrixAutoUpdate=e.matrixAutoUpdate,this.matrixWorldAutoUpdate=e.matrixWorldAutoUpdate,this.matrixWorldNeedsUpdate=e.matrixWorldNeedsUpdate,this.layers.mask=e.layers.mask,this.visible=e.visible,this.castShadow=e.castShadow,this.receiveShadow=e.receiveShadow,this.frustumCulled=e.frustumCulled,this.renderOrder=e.renderOrder,this.animations=e.animations.slice(),this.userData=JSON.parse(JSON.stringify(e.userData)),t===!0)for(let i=0;i<e.children.length;i++){const r=e.children[i];this.add(r.clone())}return this}}St.DEFAULT_UP=new k(0,1,0);St.DEFAULT_MATRIX_AUTO_UPDATE=!0;St.DEFAULT_MATRIX_WORLD_AUTO_UPDATE=!0;const Kt=new k,sn=new k,us=new k,an=new k,fi=new k,pi=new k,wo=new k,ds=new k,hs=new k,fs=new k,ps=new rt,ms=new rt,gs=new rt;class Ht{constructor(e=new k,t=new k,i=new k){this.a=e,this.b=t,this.c=i}static getNormal(e,t,i,r){r.subVectors(i,t),Kt.subVectors(e,t),r.cross(Kt);const s=r.lengthSq();return s>0?r.multiplyScalar(1/Math.sqrt(s)):r.set(0,0,0)}static getBarycoord(e,t,i,r,s){Kt.subVectors(r,t),sn.subVectors(i,t),us.subVectors(e,t);const a=Kt.dot(Kt),o=Kt.dot(sn),c=Kt.dot(us),l=sn.dot(sn),d=sn.dot(us),h=a*l-o*o;if(h===0)return s.set(0,0,0),null;const f=1/h,m=(l*c-o*d)*f,g=(a*d-o*c)*f;return s.set(1-m-g,g,m)}static containsPoint(e,t,i,r){return this.getBarycoord(e,t,i,r,an)===null?!1:an.x>=0&&an.y>=0&&an.x+an.y<=1}static getInterpolation(e,t,i,r,s,a,o,c){return this.getBarycoord(e,t,i,r,an)===null?(c.x=0,c.y=0,"z"in c&&(c.z=0),"w"in c&&(c.w=0),null):(c.setScalar(0),c.addScaledVector(s,an.x),c.addScaledVector(a,an.y),c.addScaledVector(o,an.z),c)}static getInterpolatedAttribute(e,t,i,r,s,a){return ps.setScalar(0),ms.setScalar(0),gs.setScalar(0),ps.fromBufferAttribute(e,t),ms.fromBufferAttribute(e,i),gs.fromBufferAttribute(e,r),a.setScalar(0),a.addScaledVector(ps,s.x),a.addScaledVector(ms,s.y),a.addScaledVector(gs,s.z),a}static isFrontFacing(e,t,i,r){return Kt.subVectors(i,t),sn.subVectors(e,t),Kt.cross(sn).dot(r)<0}set(e,t,i){return this.a.copy(e),this.b.copy(t),this.c.copy(i),this}setFromPointsAndIndices(e,t,i,r){return this.a.copy(e[t]),this.b.copy(e[i]),this.c.copy(e[r]),this}setFromAttributeAndIndices(e,t,i,r){return this.a.fromBufferAttribute(e,t),this.b.fromBufferAttribute(e,i),this.c.fromBufferAttribute(e,r),this}clone(){return new this.constructor().copy(this)}copy(e){return this.a.copy(e.a),this.b.copy(e.b),this.c.copy(e.c),this}getArea(){return Kt.subVectors(this.c,this.b),sn.subVectors(this.a,this.b),Kt.cross(sn).length()*.5}getMidpoint(e){return e.addVectors(this.a,this.b).add(this.c).multiplyScalar(1/3)}getNormal(e){return Ht.getNormal(this.a,this.b,this.c,e)}getPlane(e){return e.setFromCoplanarPoints(this.a,this.b,this.c)}getBarycoord(e,t){return Ht.getBarycoord(e,this.a,this.b,this.c,t)}getInterpolation(e,t,i,r,s){return Ht.getInterpolation(e,this.a,this.b,this.c,t,i,r,s)}containsPoint(e){return Ht.containsPoint(e,this.a,this.b,this.c)}isFrontFacing(e){return Ht.isFrontFacing(this.a,this.b,this.c,e)}intersectsBox(e){return e.intersectsTriangle(this)}closestPointToPoint(e,t){const i=this.a,r=this.b,s=this.c;let a,o;fi.subVectors(r,i),pi.subVectors(s,i),ds.subVectors(e,i);const c=fi.dot(ds),l=pi.dot(ds);if(c<=0&&l<=0)return t.copy(i);hs.subVectors(e,r);const d=fi.dot(hs),h=pi.dot(hs);if(d>=0&&h<=d)return t.copy(r);const f=c*h-d*l;if(f<=0&&c>=0&&d<=0)return a=c/(c-d),t.copy(i).addScaledVector(fi,a);fs.subVectors(e,s);const m=fi.dot(fs),g=pi.dot(fs);if(g>=0&&m<=g)return t.copy(s);const _=m*l-c*g;if(_<=0&&l>=0&&g<=0)return o=l/(l-g),t.copy(i).addScaledVector(pi,o);const p=d*g-m*h;if(p<=0&&h-d>=0&&m-g>=0)return wo.subVectors(s,r),o=(h-d)/(h-d+(m-g)),t.copy(r).addScaledVector(wo,o);const u=1/(p+_+f);return a=_*u,o=f*u,t.copy(i).addScaledVector(fi,a).addScaledVector(pi,o)}equals(e){return e.a.equals(this.a)&&e.b.equals(this.b)&&e.c.equals(this.c)}}const jc={aliceblue:15792383,antiquewhite:16444375,aqua:65535,aquamarine:8388564,azure:15794175,beige:16119260,bisque:16770244,black:0,blanchedalmond:16772045,blue:255,blueviolet:9055202,brown:10824234,burlywood:14596231,cadetblue:6266528,chartreuse:8388352,chocolate:13789470,coral:16744272,cornflowerblue:6591981,cornsilk:16775388,crimson:14423100,cyan:65535,darkblue:139,darkcyan:35723,darkgoldenrod:12092939,darkgray:11119017,darkgreen:25600,darkgrey:11119017,darkkhaki:12433259,darkmagenta:9109643,darkolivegreen:5597999,darkorange:16747520,darkorchid:10040012,darkred:9109504,darksalmon:15308410,darkseagreen:9419919,darkslateblue:4734347,darkslategray:3100495,darkslategrey:3100495,darkturquoise:52945,darkviolet:9699539,deeppink:16716947,deepskyblue:49151,dimgray:6908265,dimgrey:6908265,dodgerblue:2003199,firebrick:11674146,floralwhite:16775920,forestgreen:2263842,fuchsia:16711935,gainsboro:14474460,ghostwhite:16316671,gold:16766720,goldenrod:14329120,gray:8421504,green:32768,greenyellow:11403055,grey:8421504,honeydew:15794160,hotpink:16738740,indianred:13458524,indigo:4915330,ivory:16777200,khaki:15787660,lavender:15132410,lavenderblush:16773365,lawngreen:8190976,lemonchiffon:16775885,lightblue:11393254,lightcoral:15761536,lightcyan:14745599,lightgoldenrodyellow:16448210,lightgray:13882323,lightgreen:9498256,lightgrey:13882323,lightpink:16758465,lightsalmon:16752762,lightseagreen:2142890,lightskyblue:8900346,lightslategray:7833753,lightslategrey:7833753,lightsteelblue:11584734,lightyellow:16777184,lime:65280,limegreen:3329330,linen:16445670,magenta:16711935,maroon:8388608,mediumaquamarine:6737322,mediumblue:205,mediumorchid:12211667,mediumpurple:9662683,mediumseagreen:3978097,mediumslateblue:8087790,mediumspringgreen:64154,mediumturquoise:4772300,mediumvioletred:13047173,midnightblue:1644912,mintcream:16121850,mistyrose:16770273,moccasin:16770229,navajowhite:16768685,navy:128,oldlace:16643558,olive:8421376,olivedrab:7048739,orange:16753920,orangered:16729344,orchid:14315734,palegoldenrod:15657130,palegreen:10025880,paleturquoise:11529966,palevioletred:14381203,papayawhip:16773077,peachpuff:16767673,peru:13468991,pink:16761035,plum:14524637,powderblue:11591910,purple:8388736,rebeccapurple:6697881,red:16711680,rosybrown:12357519,royalblue:4286945,saddlebrown:9127187,salmon:16416882,sandybrown:16032864,seagreen:3050327,seashell:16774638,sienna:10506797,silver:12632256,skyblue:8900331,slateblue:6970061,slategray:7372944,slategrey:7372944,snow:16775930,springgreen:65407,steelblue:4620980,tan:13808780,teal:32896,thistle:14204888,tomato:16737095,turquoise:4251856,violet:15631086,wheat:16113331,white:16777215,whitesmoke:16119285,yellow:16776960,yellowgreen:10145074},Mn={h:0,s:0,l:0},gr={h:0,s:0,l:0};function _s(n,e,t){return t<0&&(t+=1),t>1&&(t-=1),t<1/6?n+(e-n)*6*t:t<1/2?e:t<2/3?n+(e-n)*6*(2/3-t):n}class oe{constructor(e,t,i){return this.isColor=!0,this.r=1,this.g=1,this.b=1,this.set(e,t,i)}set(e,t,i){if(t===void 0&&i===void 0){const r=e;r&&r.isColor?this.copy(r):typeof r=="number"?this.setHex(r):typeof r=="string"&&this.setStyle(r)}else this.setRGB(e,t,i);return this}setScalar(e){return this.r=e,this.g=e,this.b=e,this}setHex(e,t=Nt){return e=Math.floor(e),this.r=(e>>16&255)/255,this.g=(e>>8&255)/255,this.b=(e&255)/255,Je.toWorkingColorSpace(this,t),this}setRGB(e,t,i,r=Je.workingColorSpace){return this.r=e,this.g=t,this.b=i,Je.toWorkingColorSpace(this,r),this}setHSL(e,t,i,r=Je.workingColorSpace){if(e=iu(e,1),t=Xe(t,0,1),i=Xe(i,0,1),t===0)this.r=this.g=this.b=i;else{const s=i<=.5?i*(1+t):i+t-i*t,a=2*i-s;this.r=_s(a,s,e+1/3),this.g=_s(a,s,e),this.b=_s(a,s,e-1/3)}return Je.toWorkingColorSpace(this,r),this}setStyle(e,t=Nt){function i(s){s!==void 0&&parseFloat(s)<1&&console.warn("THREE.Color: Alpha component of "+e+" will be ignored.")}let r;if(r=/^(\w+)\(([^\)]*)\)/.exec(e)){let s;const a=r[1],o=r[2];switch(a){case"rgb":case"rgba":if(s=/^\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*(?:,\s*(\d*\.?\d+)\s*)?$/.exec(o))return i(s[4]),this.setRGB(Math.min(255,parseInt(s[1],10))/255,Math.min(255,parseInt(s[2],10))/255,Math.min(255,parseInt(s[3],10))/255,t);if(s=/^\s*(\d+)\%\s*,\s*(\d+)\%\s*,\s*(\d+)\%\s*(?:,\s*(\d*\.?\d+)\s*)?$/.exec(o))return i(s[4]),this.setRGB(Math.min(100,parseInt(s[1],10))/100,Math.min(100,parseInt(s[2],10))/100,Math.min(100,parseInt(s[3],10))/100,t);break;case"hsl":case"hsla":if(s=/^\s*(\d*\.?\d+)\s*,\s*(\d*\.?\d+)\%\s*,\s*(\d*\.?\d+)\%\s*(?:,\s*(\d*\.?\d+)\s*)?$/.exec(o))return i(s[4]),this.setHSL(parseFloat(s[1])/360,parseFloat(s[2])/100,parseFloat(s[3])/100,t);break;default:console.warn("THREE.Color: Unknown color model "+e)}}else if(r=/^\#([A-Fa-f\d]+)$/.exec(e)){const s=r[1],a=s.length;if(a===3)return this.setRGB(parseInt(s.charAt(0),16)/15,parseInt(s.charAt(1),16)/15,parseInt(s.charAt(2),16)/15,t);if(a===6)return this.setHex(parseInt(s,16),t);console.warn("THREE.Color: Invalid hex color "+e)}else if(e&&e.length>0)return this.setColorName(e,t);return this}setColorName(e,t=Nt){const i=jc[e.toLowerCase()];return i!==void 0?this.setHex(i,t):console.warn("THREE.Color: Unknown color "+e),this}clone(){return new this.constructor(this.r,this.g,this.b)}copy(e){return this.r=e.r,this.g=e.g,this.b=e.b,this}copySRGBToLinear(e){return this.r=fn(e.r),this.g=fn(e.g),this.b=fn(e.b),this}copyLinearToSRGB(e){return this.r=wi(e.r),this.g=wi(e.g),this.b=wi(e.b),this}convertSRGBToLinear(){return this.copySRGBToLinear(this),this}convertLinearToSRGB(){return this.copyLinearToSRGB(this),this}getHex(e=Nt){return Je.fromWorkingColorSpace(bt.copy(this),e),Math.round(Xe(bt.r*255,0,255))*65536+Math.round(Xe(bt.g*255,0,255))*256+Math.round(Xe(bt.b*255,0,255))}getHexString(e=Nt){return("000000"+this.getHex(e).toString(16)).slice(-6)}getHSL(e,t=Je.workingColorSpace){Je.fromWorkingColorSpace(bt.copy(this),t);const i=bt.r,r=bt.g,s=bt.b,a=Math.max(i,r,s),o=Math.min(i,r,s);let c,l;const d=(o+a)/2;if(o===a)c=0,l=0;else{const h=a-o;switch(l=d<=.5?h/(a+o):h/(2-a-o),a){case i:c=(r-s)/h+(r<s?6:0);break;case r:c=(s-i)/h+2;break;case s:c=(i-r)/h+4;break}c/=6}return e.h=c,e.s=l,e.l=d,e}getRGB(e,t=Je.workingColorSpace){return Je.fromWorkingColorSpace(bt.copy(this),t),e.r=bt.r,e.g=bt.g,e.b=bt.b,e}getStyle(e=Nt){Je.fromWorkingColorSpace(bt.copy(this),e);const t=bt.r,i=bt.g,r=bt.b;return e!==Nt?`color(${e} ${t.toFixed(3)} ${i.toFixed(3)} ${r.toFixed(3)})`:`rgb(${Math.round(t*255)},${Math.round(i*255)},${Math.round(r*255)})`}offsetHSL(e,t,i){return this.getHSL(Mn),this.setHSL(Mn.h+e,Mn.s+t,Mn.l+i)}add(e){return this.r+=e.r,this.g+=e.g,this.b+=e.b,this}addColors(e,t){return this.r=e.r+t.r,this.g=e.g+t.g,this.b=e.b+t.b,this}addScalar(e){return this.r+=e,this.g+=e,this.b+=e,this}sub(e){return this.r=Math.max(0,this.r-e.r),this.g=Math.max(0,this.g-e.g),this.b=Math.max(0,this.b-e.b),this}multiply(e){return this.r*=e.r,this.g*=e.g,this.b*=e.b,this}multiplyScalar(e){return this.r*=e,this.g*=e,this.b*=e,this}lerp(e,t){return this.r+=(e.r-this.r)*t,this.g+=(e.g-this.g)*t,this.b+=(e.b-this.b)*t,this}lerpColors(e,t,i){return this.r=e.r+(t.r-e.r)*i,this.g=e.g+(t.g-e.g)*i,this.b=e.b+(t.b-e.b)*i,this}lerpHSL(e,t){this.getHSL(Mn),e.getHSL(gr);const i=es(Mn.h,gr.h,t),r=es(Mn.s,gr.s,t),s=es(Mn.l,gr.l,t);return this.setHSL(i,r,s),this}setFromVector3(e){return this.r=e.x,this.g=e.y,this.b=e.z,this}applyMatrix3(e){const t=this.r,i=this.g,r=this.b,s=e.elements;return this.r=s[0]*t+s[3]*i+s[6]*r,this.g=s[1]*t+s[4]*i+s[7]*r,this.b=s[2]*t+s[5]*i+s[8]*r,this}equals(e){return e.r===this.r&&e.g===this.g&&e.b===this.b}fromArray(e,t=0){return this.r=e[t],this.g=e[t+1],this.b=e[t+2],this}toArray(e=[],t=0){return e[t]=this.r,e[t+1]=this.g,e[t+2]=this.b,e}fromBufferAttribute(e,t){return this.r=e.getX(t),this.g=e.getY(t),this.b=e.getZ(t),this}toJSON(){return this.getHex()}*[Symbol.iterator](){yield this.r,yield this.g,yield this.b}}const bt=new oe;oe.NAMES=jc;let Su=0;class ki extends Ni{constructor(){super(),this.isMaterial=!0,Object.defineProperty(this,"id",{value:Su++}),this.uuid=ir(),this.name="",this.type="Material",this.blending=Ti,this.side=Pn,this.vertexColors=!1,this.opacity=1,this.transparent=!1,this.alphaHash=!1,this.blendSrc=ks,this.blendDst=Os,this.blendEquation=Xn,this.blendSrcAlpha=null,this.blendDstAlpha=null,this.blendEquationAlpha=null,this.blendColor=new oe(0,0,0),this.blendAlpha=0,this.depthFunc=Ri,this.depthTest=!0,this.depthWrite=!0,this.stencilWriteMask=255,this.stencilFunc=fo,this.stencilRef=0,this.stencilFuncMask=255,this.stencilFail=si,this.stencilZFail=si,this.stencilZPass=si,this.stencilWrite=!1,this.clippingPlanes=null,this.clipIntersection=!1,this.clipShadows=!1,this.shadowSide=null,this.colorWrite=!0,this.precision=null,this.polygonOffset=!1,this.polygonOffsetFactor=0,this.polygonOffsetUnits=0,this.dithering=!1,this.alphaToCoverage=!1,this.premultipliedAlpha=!1,this.forceSinglePass=!1,this.visible=!0,this.toneMapped=!0,this.userData={},this.version=0,this._alphaTest=0}get alphaTest(){return this._alphaTest}set alphaTest(e){this._alphaTest>0!=e>0&&this.version++,this._alphaTest=e}onBeforeRender(){}onBeforeCompile(){}customProgramCacheKey(){return this.onBeforeCompile.toString()}setValues(e){if(e!==void 0)for(const t in e){const i=e[t];if(i===void 0){console.warn(`THREE.Material: parameter '${t}' has value of undefined.`);continue}const r=this[t];if(r===void 0){console.warn(`THREE.Material: '${t}' is not a property of THREE.${this.type}.`);continue}r&&r.isColor?r.set(i):r&&r.isVector3&&i&&i.isVector3?r.copy(i):this[t]=i}}toJSON(e){const t=e===void 0||typeof e=="string";t&&(e={textures:{},images:{}});const i={metadata:{version:4.6,type:"Material",generator:"Material.toJSON"}};i.uuid=this.uuid,i.type=this.type,this.name!==""&&(i.name=this.name),this.color&&this.color.isColor&&(i.color=this.color.getHex()),this.roughness!==void 0&&(i.roughness=this.roughness),this.metalness!==void 0&&(i.metalness=this.metalness),this.sheen!==void 0&&(i.sheen=this.sheen),this.sheenColor&&this.sheenColor.isColor&&(i.sheenColor=this.sheenColor.getHex()),this.sheenRoughness!==void 0&&(i.sheenRoughness=this.sheenRoughness),this.emissive&&this.emissive.isColor&&(i.emissive=this.emissive.getHex()),this.emissiveIntensity!==void 0&&this.emissiveIntensity!==1&&(i.emissiveIntensity=this.emissiveIntensity),this.specular&&this.specular.isColor&&(i.specular=this.specular.getHex()),this.specularIntensity!==void 0&&(i.specularIntensity=this.specularIntensity),this.specularColor&&this.specularColor.isColor&&(i.specularColor=this.specularColor.getHex()),this.shininess!==void 0&&(i.shininess=this.shininess),this.clearcoat!==void 0&&(i.clearcoat=this.clearcoat),this.clearcoatRoughness!==void 0&&(i.clearcoatRoughness=this.clearcoatRoughness),this.clearcoatMap&&this.clearcoatMap.isTexture&&(i.clearcoatMap=this.clearcoatMap.toJSON(e).uuid),this.clearcoatRoughnessMap&&this.clearcoatRoughnessMap.isTexture&&(i.clearcoatRoughnessMap=this.clearcoatRoughnessMap.toJSON(e).uuid),this.clearcoatNormalMap&&this.clearcoatNormalMap.isTexture&&(i.clearcoatNormalMap=this.clearcoatNormalMap.toJSON(e).uuid,i.clearcoatNormalScale=this.clearcoatNormalScale.toArray()),this.dispersion!==void 0&&(i.dispersion=this.dispersion),this.iridescence!==void 0&&(i.iridescence=this.iridescence),this.iridescenceIOR!==void 0&&(i.iridescenceIOR=this.iridescenceIOR),this.iridescenceThicknessRange!==void 0&&(i.iridescenceThicknessRange=this.iridescenceThicknessRange),this.iridescenceMap&&this.iridescenceMap.isTexture&&(i.iridescenceMap=this.iridescenceMap.toJSON(e).uuid),this.iridescenceThicknessMap&&this.iridescenceThicknessMap.isTexture&&(i.iridescenceThicknessMap=this.iridescenceThicknessMap.toJSON(e).uuid),this.anisotropy!==void 0&&(i.anisotropy=this.anisotropy),this.anisotropyRotation!==void 0&&(i.anisotropyRotation=this.anisotropyRotation),this.anisotropyMap&&this.anisotropyMap.isTexture&&(i.anisotropyMap=this.anisotropyMap.toJSON(e).uuid),this.map&&this.map.isTexture&&(i.map=this.map.toJSON(e).uuid),this.matcap&&this.matcap.isTexture&&(i.matcap=this.matcap.toJSON(e).uuid),this.alphaMap&&this.alphaMap.isTexture&&(i.alphaMap=this.alphaMap.toJSON(e).uuid),this.lightMap&&this.lightMap.isTexture&&(i.lightMap=this.lightMap.toJSON(e).uuid,i.lightMapIntensity=this.lightMapIntensity),this.aoMap&&this.aoMap.isTexture&&(i.aoMap=this.aoMap.toJSON(e).uuid,i.aoMapIntensity=this.aoMapIntensity),this.bumpMap&&this.bumpMap.isTexture&&(i.bumpMap=this.bumpMap.toJSON(e).uuid,i.bumpScale=this.bumpScale),this.normalMap&&this.normalMap.isTexture&&(i.normalMap=this.normalMap.toJSON(e).uuid,i.normalMapType=this.normalMapType,i.normalScale=this.normalScale.toArray()),this.displacementMap&&this.displacementMap.isTexture&&(i.displacementMap=this.displacementMap.toJSON(e).uuid,i.displacementScale=this.displacementScale,i.displacementBias=this.displacementBias),this.roughnessMap&&this.roughnessMap.isTexture&&(i.roughnessMap=this.roughnessMap.toJSON(e).uuid),this.metalnessMap&&this.metalnessMap.isTexture&&(i.metalnessMap=this.metalnessMap.toJSON(e).uuid),this.emissiveMap&&this.emissiveMap.isTexture&&(i.emissiveMap=this.emissiveMap.toJSON(e).uuid),this.specularMap&&this.specularMap.isTexture&&(i.specularMap=this.specularMap.toJSON(e).uuid),this.specularIntensityMap&&this.specularIntensityMap.isTexture&&(i.specularIntensityMap=this.specularIntensityMap.toJSON(e).uuid),this.specularColorMap&&this.specularColorMap.isTexture&&(i.specularColorMap=this.specularColorMap.toJSON(e).uuid),this.envMap&&this.envMap.isTexture&&(i.envMap=this.envMap.toJSON(e).uuid,this.combine!==void 0&&(i.combine=this.combine)),this.envMapRotation!==void 0&&(i.envMapRotation=this.envMapRotation.toArray()),this.envMapIntensity!==void 0&&(i.envMapIntensity=this.envMapIntensity),this.reflectivity!==void 0&&(i.reflectivity=this.reflectivity),this.refractionRatio!==void 0&&(i.refractionRatio=this.refractionRatio),this.gradientMap&&this.gradientMap.isTexture&&(i.gradientMap=this.gradientMap.toJSON(e).uuid),this.transmission!==void 0&&(i.transmission=this.transmission),this.transmissionMap&&this.transmissionMap.isTexture&&(i.transmissionMap=this.transmissionMap.toJSON(e).uuid),this.thickness!==void 0&&(i.thickness=this.thickness),this.thicknessMap&&this.thicknessMap.isTexture&&(i.thicknessMap=this.thicknessMap.toJSON(e).uuid),this.attenuationDistance!==void 0&&this.attenuationDistance!==1/0&&(i.attenuationDistance=this.attenuationDistance),this.attenuationColor!==void 0&&(i.attenuationColor=this.attenuationColor.getHex()),this.size!==void 0&&(i.size=this.size),this.shadowSide!==null&&(i.shadowSide=this.shadowSide),this.sizeAttenuation!==void 0&&(i.sizeAttenuation=this.sizeAttenuation),this.blending!==Ti&&(i.blending=this.blending),this.side!==Pn&&(i.side=this.side),this.vertexColors===!0&&(i.vertexColors=!0),this.opacity<1&&(i.opacity=this.opacity),this.transparent===!0&&(i.transparent=!0),this.blendSrc!==ks&&(i.blendSrc=this.blendSrc),this.blendDst!==Os&&(i.blendDst=this.blendDst),this.blendEquation!==Xn&&(i.blendEquation=this.blendEquation),this.blendSrcAlpha!==null&&(i.blendSrcAlpha=this.blendSrcAlpha),this.blendDstAlpha!==null&&(i.blendDstAlpha=this.blendDstAlpha),this.blendEquationAlpha!==null&&(i.blendEquationAlpha=this.blendEquationAlpha),this.blendColor&&this.blendColor.isColor&&(i.blendColor=this.blendColor.getHex()),this.blendAlpha!==0&&(i.blendAlpha=this.blendAlpha),this.depthFunc!==Ri&&(i.depthFunc=this.depthFunc),this.depthTest===!1&&(i.depthTest=this.depthTest),this.depthWrite===!1&&(i.depthWrite=this.depthWrite),this.colorWrite===!1&&(i.colorWrite=this.colorWrite),this.stencilWriteMask!==255&&(i.stencilWriteMask=this.stencilWriteMask),this.stencilFunc!==fo&&(i.stencilFunc=this.stencilFunc),this.stencilRef!==0&&(i.stencilRef=this.stencilRef),this.stencilFuncMask!==255&&(i.stencilFuncMask=this.stencilFuncMask),this.stencilFail!==si&&(i.stencilFail=this.stencilFail),this.stencilZFail!==si&&(i.stencilZFail=this.stencilZFail),this.stencilZPass!==si&&(i.stencilZPass=this.stencilZPass),this.stencilWrite===!0&&(i.stencilWrite=this.stencilWrite),this.rotation!==void 0&&this.rotation!==0&&(i.rotation=this.rotation),this.polygonOffset===!0&&(i.polygonOffset=!0),this.polygonOffsetFactor!==0&&(i.polygonOffsetFactor=this.polygonOffsetFactor),this.polygonOffsetUnits!==0&&(i.polygonOffsetUnits=this.polygonOffsetUnits),this.linewidth!==void 0&&this.linewidth!==1&&(i.linewidth=this.linewidth),this.dashSize!==void 0&&(i.dashSize=this.dashSize),this.gapSize!==void 0&&(i.gapSize=this.gapSize),this.scale!==void 0&&(i.scale=this.scale),this.dithering===!0&&(i.dithering=!0),this.alphaTest>0&&(i.alphaTest=this.alphaTest),this.alphaHash===!0&&(i.alphaHash=!0),this.alphaToCoverage===!0&&(i.alphaToCoverage=!0),this.premultipliedAlpha===!0&&(i.premultipliedAlpha=!0),this.forceSinglePass===!0&&(i.forceSinglePass=!0),this.wireframe===!0&&(i.wireframe=!0),this.wireframeLinewidth>1&&(i.wireframeLinewidth=this.wireframeLinewidth),this.wireframeLinecap!=="round"&&(i.wireframeLinecap=this.wireframeLinecap),this.wireframeLinejoin!=="round"&&(i.wireframeLinejoin=this.wireframeLinejoin),this.flatShading===!0&&(i.flatShading=!0),this.visible===!1&&(i.visible=!1),this.toneMapped===!1&&(i.toneMapped=!1),this.fog===!1&&(i.fog=!1),Object.keys(this.userData).length>0&&(i.userData=this.userData);function r(s){const a=[];for(const o in s){const c=s[o];delete c.metadata,a.push(c)}return a}if(t){const s=r(e.textures),a=r(e.images);s.length>0&&(i.textures=s),a.length>0&&(i.images=a)}return i}clone(){return new this.constructor().copy(this)}copy(e){this.name=e.name,this.blending=e.blending,this.side=e.side,this.vertexColors=e.vertexColors,this.opacity=e.opacity,this.transparent=e.transparent,this.blendSrc=e.blendSrc,this.blendDst=e.blendDst,this.blendEquation=e.blendEquation,this.blendSrcAlpha=e.blendSrcAlpha,this.blendDstAlpha=e.blendDstAlpha,this.blendEquationAlpha=e.blendEquationAlpha,this.blendColor.copy(e.blendColor),this.blendAlpha=e.blendAlpha,this.depthFunc=e.depthFunc,this.depthTest=e.depthTest,this.depthWrite=e.depthWrite,this.stencilWriteMask=e.stencilWriteMask,this.stencilFunc=e.stencilFunc,this.stencilRef=e.stencilRef,this.stencilFuncMask=e.stencilFuncMask,this.stencilFail=e.stencilFail,this.stencilZFail=e.stencilZFail,this.stencilZPass=e.stencilZPass,this.stencilWrite=e.stencilWrite;const t=e.clippingPlanes;let i=null;if(t!==null){const r=t.length;i=new Array(r);for(let s=0;s!==r;++s)i[s]=t[s].clone()}return this.clippingPlanes=i,this.clipIntersection=e.clipIntersection,this.clipShadows=e.clipShadows,this.shadowSide=e.shadowSide,this.colorWrite=e.colorWrite,this.precision=e.precision,this.polygonOffset=e.polygonOffset,this.polygonOffsetFactor=e.polygonOffsetFactor,this.polygonOffsetUnits=e.polygonOffsetUnits,this.dithering=e.dithering,this.alphaTest=e.alphaTest,this.alphaHash=e.alphaHash,this.alphaToCoverage=e.alphaToCoverage,this.premultipliedAlpha=e.premultipliedAlpha,this.forceSinglePass=e.forceSinglePass,this.visible=e.visible,this.toneMapped=e.toneMapped,this.userData=JSON.parse(JSON.stringify(e.userData)),this}dispose(){this.dispatchEvent({type:"dispose"})}set needsUpdate(e){e===!0&&this.version++}onBuild(){console.warn("Material: onBuild() has been removed.")}}class Ln extends ki{constructor(e){super(),this.isMeshBasicMaterial=!0,this.type="MeshBasicMaterial",this.color=new oe(16777215),this.map=null,this.lightMap=null,this.lightMapIntensity=1,this.aoMap=null,this.aoMapIntensity=1,this.specularMap=null,this.alphaMap=null,this.envMap=null,this.envMapRotation=new xt,this.combine=Rc,this.reflectivity=1,this.refractionRatio=.98,this.wireframe=!1,this.wireframeLinewidth=1,this.wireframeLinecap="round",this.wireframeLinejoin="round",this.fog=!0,this.setValues(e)}copy(e){return super.copy(e),this.color.copy(e.color),this.map=e.map,this.lightMap=e.lightMap,this.lightMapIntensity=e.lightMapIntensity,this.aoMap=e.aoMap,this.aoMapIntensity=e.aoMapIntensity,this.specularMap=e.specularMap,this.alphaMap=e.alphaMap,this.envMap=e.envMap,this.envMapRotation.copy(e.envMapRotation),this.combine=e.combine,this.reflectivity=e.reflectivity,this.refractionRatio=e.refractionRatio,this.wireframe=e.wireframe,this.wireframeLinewidth=e.wireframeLinewidth,this.wireframeLinecap=e.wireframeLinecap,this.wireframeLinejoin=e.wireframeLinejoin,this.fog=e.fog,this}}const ft=new k,_r=new We;let Eu=0;class Qt{constructor(e,t,i=!1){if(Array.isArray(e))throw new TypeError("THREE.BufferAttribute: array should be a Typed Array.");this.isBufferAttribute=!0,Object.defineProperty(this,"id",{value:Eu++}),this.name="",this.array=e,this.itemSize=t,this.count=e!==void 0?e.length/t:0,this.normalized=i,this.usage=po,this.updateRanges=[],this.gpuType=dn,this.version=0}onUploadCallback(){}set needsUpdate(e){e===!0&&this.version++}setUsage(e){return this.usage=e,this}addUpdateRange(e,t){this.updateRanges.push({start:e,count:t})}clearUpdateRanges(){this.updateRanges.length=0}copy(e){return this.name=e.name,this.array=new e.array.constructor(e.array),this.itemSize=e.itemSize,this.count=e.count,this.normalized=e.normalized,this.usage=e.usage,this.gpuType=e.gpuType,this}copyAt(e,t,i){e*=this.itemSize,i*=t.itemSize;for(let r=0,s=this.itemSize;r<s;r++)this.array[e+r]=t.array[i+r];return this}copyArray(e){return this.array.set(e),this}applyMatrix3(e){if(this.itemSize===2)for(let t=0,i=this.count;t<i;t++)_r.fromBufferAttribute(this,t),_r.applyMatrix3(e),this.setXY(t,_r.x,_r.y);else if(this.itemSize===3)for(let t=0,i=this.count;t<i;t++)ft.fromBufferAttribute(this,t),ft.applyMatrix3(e),this.setXYZ(t,ft.x,ft.y,ft.z);return this}applyMatrix4(e){for(let t=0,i=this.count;t<i;t++)ft.fromBufferAttribute(this,t),ft.applyMatrix4(e),this.setXYZ(t,ft.x,ft.y,ft.z);return this}applyNormalMatrix(e){for(let t=0,i=this.count;t<i;t++)ft.fromBufferAttribute(this,t),ft.applyNormalMatrix(e),this.setXYZ(t,ft.x,ft.y,ft.z);return this}transformDirection(e){for(let t=0,i=this.count;t<i;t++)ft.fromBufferAttribute(this,t),ft.transformDirection(e),this.setXYZ(t,ft.x,ft.y,ft.z);return this}set(e,t=0){return this.array.set(e,t),this}getComponent(e,t){let i=this.array[e*this.itemSize+t];return this.normalized&&(i=Vi(i,this.array)),i}setComponent(e,t,i){return this.normalized&&(i=Dt(i,this.array)),this.array[e*this.itemSize+t]=i,this}getX(e){let t=this.array[e*this.itemSize];return this.normalized&&(t=Vi(t,this.array)),t}setX(e,t){return this.normalized&&(t=Dt(t,this.array)),this.array[e*this.itemSize]=t,this}getY(e){let t=this.array[e*this.itemSize+1];return this.normalized&&(t=Vi(t,this.array)),t}setY(e,t){return this.normalized&&(t=Dt(t,this.array)),this.array[e*this.itemSize+1]=t,this}getZ(e){let t=this.array[e*this.itemSize+2];return this.normalized&&(t=Vi(t,this.array)),t}setZ(e,t){return this.normalized&&(t=Dt(t,this.array)),this.array[e*this.itemSize+2]=t,this}getW(e){let t=this.array[e*this.itemSize+3];return this.normalized&&(t=Vi(t,this.array)),t}setW(e,t){return this.normalized&&(t=Dt(t,this.array)),this.array[e*this.itemSize+3]=t,this}setXY(e,t,i){return e*=this.itemSize,this.normalized&&(t=Dt(t,this.array),i=Dt(i,this.array)),this.array[e+0]=t,this.array[e+1]=i,this}setXYZ(e,t,i,r){return e*=this.itemSize,this.normalized&&(t=Dt(t,this.array),i=Dt(i,this.array),r=Dt(r,this.array)),this.array[e+0]=t,this.array[e+1]=i,this.array[e+2]=r,this}setXYZW(e,t,i,r,s){return e*=this.itemSize,this.normalized&&(t=Dt(t,this.array),i=Dt(i,this.array),r=Dt(r,this.array),s=Dt(s,this.array)),this.array[e+0]=t,this.array[e+1]=i,this.array[e+2]=r,this.array[e+3]=s,this}onUpload(e){return this.onUploadCallback=e,this}clone(){return new this.constructor(this.array,this.itemSize).copy(this)}toJSON(){const e={itemSize:this.itemSize,type:this.array.constructor.name,array:Array.from(this.array),normalized:this.normalized};return this.name!==""&&(e.name=this.name),this.usage!==po&&(e.usage=this.usage),e}}class Wc extends Qt{constructor(e,t,i){super(new Uint16Array(e),t,i)}}class Xc extends Qt{constructor(e,t,i){super(new Uint32Array(e),t,i)}}class je extends Qt{constructor(e,t,i){super(new Float32Array(e),t,i)}}let yu=0;const Vt=new at,vs=new St,mi=new k,zt=new Fi,Wi=new Fi,vt=new k;class Ke extends Ni{constructor(){super(),this.isBufferGeometry=!0,Object.defineProperty(this,"id",{value:yu++}),this.uuid=ir(),this.name="",this.type="BufferGeometry",this.index=null,this.indirect=null,this.attributes={},this.morphAttributes={},this.morphTargetsRelative=!1,this.groups=[],this.boundingBox=null,this.boundingSphere=null,this.drawRange={start:0,count:1/0},this.userData={}}getIndex(){return this.index}setIndex(e){return Array.isArray(e)?this.index=new(Hc(e)?Xc:Wc)(e,1):this.index=e,this}setIndirect(e){return this.indirect=e,this}getIndirect(){return this.indirect}getAttribute(e){return this.attributes[e]}setAttribute(e,t){return this.attributes[e]=t,this}deleteAttribute(e){return delete this.attributes[e],this}hasAttribute(e){return this.attributes[e]!==void 0}addGroup(e,t,i=0){this.groups.push({start:e,count:t,materialIndex:i})}clearGroups(){this.groups=[]}setDrawRange(e,t){this.drawRange.start=e,this.drawRange.count=t}applyMatrix4(e){const t=this.attributes.position;t!==void 0&&(t.applyMatrix4(e),t.needsUpdate=!0);const i=this.attributes.normal;if(i!==void 0){const s=new Ve().getNormalMatrix(e);i.applyNormalMatrix(s),i.needsUpdate=!0}const r=this.attributes.tangent;return r!==void 0&&(r.transformDirection(e),r.needsUpdate=!0),this.boundingBox!==null&&this.computeBoundingBox(),this.boundingSphere!==null&&this.computeBoundingSphere(),this}applyQuaternion(e){return Vt.makeRotationFromQuaternion(e),this.applyMatrix4(Vt),this}rotateX(e){return Vt.makeRotationX(e),this.applyMatrix4(Vt),this}rotateY(e){return Vt.makeRotationY(e),this.applyMatrix4(Vt),this}rotateZ(e){return Vt.makeRotationZ(e),this.applyMatrix4(Vt),this}translate(e,t,i){return Vt.makeTranslation(e,t,i),this.applyMatrix4(Vt),this}scale(e,t,i){return Vt.makeScale(e,t,i),this.applyMatrix4(Vt),this}lookAt(e){return vs.lookAt(e),vs.updateMatrix(),this.applyMatrix4(vs.matrix),this}center(){return this.computeBoundingBox(),this.boundingBox.getCenter(mi).negate(),this.translate(mi.x,mi.y,mi.z),this}setFromPoints(e){const t=this.getAttribute("position");if(t===void 0){const i=[];for(let r=0,s=e.length;r<s;r++){const a=e[r];i.push(a.x,a.y,a.z||0)}this.setAttribute("position",new je(i,3))}else{const i=Math.min(e.length,t.count);for(let r=0;r<i;r++){const s=e[r];t.setXYZ(r,s.x,s.y,s.z||0)}e.length>t.count&&console.warn("THREE.BufferGeometry: Buffer size too small for points data. Use .dispose() and create a new geometry."),t.needsUpdate=!0}return this}computeBoundingBox(){this.boundingBox===null&&(this.boundingBox=new Fi);const e=this.attributes.position,t=this.morphAttributes.position;if(e&&e.isGLBufferAttribute){console.error("THREE.BufferGeometry.computeBoundingBox(): GLBufferAttribute requires a manual bounding box.",this),this.boundingBox.set(new k(-1/0,-1/0,-1/0),new k(1/0,1/0,1/0));return}if(e!==void 0){if(this.boundingBox.setFromBufferAttribute(e),t)for(let i=0,r=t.length;i<r;i++){const s=t[i];zt.setFromBufferAttribute(s),this.morphTargetsRelative?(vt.addVectors(this.boundingBox.min,zt.min),this.boundingBox.expandByPoint(vt),vt.addVectors(this.boundingBox.max,zt.max),this.boundingBox.expandByPoint(vt)):(this.boundingBox.expandByPoint(zt.min),this.boundingBox.expandByPoint(zt.max))}}else this.boundingBox.makeEmpty();(isNaN(this.boundingBox.min.x)||isNaN(this.boundingBox.min.y)||isNaN(this.boundingBox.min.z))&&console.error('THREE.BufferGeometry.computeBoundingBox(): Computed min/max have NaN values. The "position" attribute is likely to have NaN values.',this)}computeBoundingSphere(){this.boundingSphere===null&&(this.boundingSphere=new Yr);const e=this.attributes.position,t=this.morphAttributes.position;if(e&&e.isGLBufferAttribute){console.error("THREE.BufferGeometry.computeBoundingSphere(): GLBufferAttribute requires a manual bounding sphere.",this),this.boundingSphere.set(new k,1/0);return}if(e){const i=this.boundingSphere.center;if(zt.setFromBufferAttribute(e),t)for(let s=0,a=t.length;s<a;s++){const o=t[s];Wi.setFromBufferAttribute(o),this.morphTargetsRelative?(vt.addVectors(zt.min,Wi.min),zt.expandByPoint(vt),vt.addVectors(zt.max,Wi.max),zt.expandByPoint(vt)):(zt.expandByPoint(Wi.min),zt.expandByPoint(Wi.max))}zt.getCenter(i);let r=0;for(let s=0,a=e.count;s<a;s++)vt.fromBufferAttribute(e,s),r=Math.max(r,i.distanceToSquared(vt));if(t)for(let s=0,a=t.length;s<a;s++){const o=t[s],c=this.morphTargetsRelative;for(let l=0,d=o.count;l<d;l++)vt.fromBufferAttribute(o,l),c&&(mi.fromBufferAttribute(e,l),vt.add(mi)),r=Math.max(r,i.distanceToSquared(vt))}this.boundingSphere.radius=Math.sqrt(r),isNaN(this.boundingSphere.radius)&&console.error('THREE.BufferGeometry.computeBoundingSphere(): Computed radius is NaN. The "position" attribute is likely to have NaN values.',this)}}computeTangents(){const e=this.index,t=this.attributes;if(e===null||t.position===void 0||t.normal===void 0||t.uv===void 0){console.error("THREE.BufferGeometry: .computeTangents() failed. Missing required attributes (index, position, normal or uv)");return}const i=t.position,r=t.normal,s=t.uv;this.hasAttribute("tangent")===!1&&this.setAttribute("tangent",new Qt(new Float32Array(4*i.count),4));const a=this.getAttribute("tangent"),o=[],c=[];for(let C=0;C<i.count;C++)o[C]=new k,c[C]=new k;const l=new k,d=new k,h=new k,f=new We,m=new We,g=new We,_=new k,p=new k;function u(C,v,x){l.fromBufferAttribute(i,C),d.fromBufferAttribute(i,v),h.fromBufferAttribute(i,x),f.fromBufferAttribute(s,C),m.fromBufferAttribute(s,v),g.fromBufferAttribute(s,x),d.sub(l),h.sub(l),m.sub(f),g.sub(f);const P=1/(m.x*g.y-g.x*m.y);isFinite(P)&&(_.copy(d).multiplyScalar(g.y).addScaledVector(h,-m.y).multiplyScalar(P),p.copy(h).multiplyScalar(m.x).addScaledVector(d,-g.x).multiplyScalar(P),o[C].add(_),o[v].add(_),o[x].add(_),c[C].add(p),c[v].add(p),c[x].add(p))}let E=this.groups;E.length===0&&(E=[{start:0,count:e.count}]);for(let C=0,v=E.length;C<v;++C){const x=E[C],P=x.start,U=x.count;for(let A=P,R=P+U;A<R;A+=3)u(e.getX(A+0),e.getX(A+1),e.getX(A+2))}const y=new k,M=new k,D=new k,w=new k;function b(C){D.fromBufferAttribute(r,C),w.copy(D);const v=o[C];y.copy(v),y.sub(D.multiplyScalar(D.dot(v))).normalize(),M.crossVectors(w,v);const P=M.dot(c[C])<0?-1:1;a.setXYZW(C,y.x,y.y,y.z,P)}for(let C=0,v=E.length;C<v;++C){const x=E[C],P=x.start,U=x.count;for(let A=P,R=P+U;A<R;A+=3)b(e.getX(A+0)),b(e.getX(A+1)),b(e.getX(A+2))}}computeVertexNormals(){const e=this.index,t=this.getAttribute("position");if(t!==void 0){let i=this.getAttribute("normal");if(i===void 0)i=new Qt(new Float32Array(t.count*3),3),this.setAttribute("normal",i);else for(let f=0,m=i.count;f<m;f++)i.setXYZ(f,0,0,0);const r=new k,s=new k,a=new k,o=new k,c=new k,l=new k,d=new k,h=new k;if(e)for(let f=0,m=e.count;f<m;f+=3){const g=e.getX(f+0),_=e.getX(f+1),p=e.getX(f+2);r.fromBufferAttribute(t,g),s.fromBufferAttribute(t,_),a.fromBufferAttribute(t,p),d.subVectors(a,s),h.subVectors(r,s),d.cross(h),o.fromBufferAttribute(i,g),c.fromBufferAttribute(i,_),l.fromBufferAttribute(i,p),o.add(d),c.add(d),l.add(d),i.setXYZ(g,o.x,o.y,o.z),i.setXYZ(_,c.x,c.y,c.z),i.setXYZ(p,l.x,l.y,l.z)}else for(let f=0,m=t.count;f<m;f+=3)r.fromBufferAttribute(t,f+0),s.fromBufferAttribute(t,f+1),a.fromBufferAttribute(t,f+2),d.subVectors(a,s),h.subVectors(r,s),d.cross(h),i.setXYZ(f+0,d.x,d.y,d.z),i.setXYZ(f+1,d.x,d.y,d.z),i.setXYZ(f+2,d.x,d.y,d.z);this.normalizeNormals(),i.needsUpdate=!0}}normalizeNormals(){const e=this.attributes.normal;for(let t=0,i=e.count;t<i;t++)vt.fromBufferAttribute(e,t),vt.normalize(),e.setXYZ(t,vt.x,vt.y,vt.z)}toNonIndexed(){function e(o,c){const l=o.array,d=o.itemSize,h=o.normalized,f=new l.constructor(c.length*d);let m=0,g=0;for(let _=0,p=c.length;_<p;_++){o.isInterleavedBufferAttribute?m=c[_]*o.data.stride+o.offset:m=c[_]*d;for(let u=0;u<d;u++)f[g++]=l[m++]}return new Qt(f,d,h)}if(this.index===null)return console.warn("THREE.BufferGeometry.toNonIndexed(): BufferGeometry is already non-indexed."),this;const t=new Ke,i=this.index.array,r=this.attributes;for(const o in r){const c=r[o],l=e(c,i);t.setAttribute(o,l)}const s=this.morphAttributes;for(const o in s){const c=[],l=s[o];for(let d=0,h=l.length;d<h;d++){const f=l[d],m=e(f,i);c.push(m)}t.morphAttributes[o]=c}t.morphTargetsRelative=this.morphTargetsRelative;const a=this.groups;for(let o=0,c=a.length;o<c;o++){const l=a[o];t.addGroup(l.start,l.count,l.materialIndex)}return t}toJSON(){const e={metadata:{version:4.6,type:"BufferGeometry",generator:"BufferGeometry.toJSON"}};if(e.uuid=this.uuid,e.type=this.type,this.name!==""&&(e.name=this.name),Object.keys(this.userData).length>0&&(e.userData=this.userData),this.parameters!==void 0){const c=this.parameters;for(const l in c)c[l]!==void 0&&(e[l]=c[l]);return e}e.data={attributes:{}};const t=this.index;t!==null&&(e.data.index={type:t.array.constructor.name,array:Array.prototype.slice.call(t.array)});const i=this.attributes;for(const c in i){const l=i[c];e.data.attributes[c]=l.toJSON(e.data)}const r={};let s=!1;for(const c in this.morphAttributes){const l=this.morphAttributes[c],d=[];for(let h=0,f=l.length;h<f;h++){const m=l[h];d.push(m.toJSON(e.data))}d.length>0&&(r[c]=d,s=!0)}s&&(e.data.morphAttributes=r,e.data.morphTargetsRelative=this.morphTargetsRelative);const a=this.groups;a.length>0&&(e.data.groups=JSON.parse(JSON.stringify(a)));const o=this.boundingSphere;return o!==null&&(e.data.boundingSphere={center:o.center.toArray(),radius:o.radius}),e}clone(){return new this.constructor().copy(this)}copy(e){this.index=null,this.attributes={},this.morphAttributes={},this.groups=[],this.boundingBox=null,this.boundingSphere=null;const t={};this.name=e.name;const i=e.index;i!==null&&this.setIndex(i.clone(t));const r=e.attributes;for(const l in r){const d=r[l];this.setAttribute(l,d.clone(t))}const s=e.morphAttributes;for(const l in s){const d=[],h=s[l];for(let f=0,m=h.length;f<m;f++)d.push(h[f].clone(t));this.morphAttributes[l]=d}this.morphTargetsRelative=e.morphTargetsRelative;const a=e.groups;for(let l=0,d=a.length;l<d;l++){const h=a[l];this.addGroup(h.start,h.count,h.materialIndex)}const o=e.boundingBox;o!==null&&(this.boundingBox=o.clone());const c=e.boundingSphere;return c!==null&&(this.boundingSphere=c.clone()),this.drawRange.start=e.drawRange.start,this.drawRange.count=e.drawRange.count,this.userData=e.userData,this}dispose(){this.dispatchEvent({type:"dispose"})}}const Ro=new at,Fn=new Ba,vr=new Yr,Co=new k,xr=new k,Mr=new k,Sr=new k,xs=new k,Er=new k,Po=new k,yr=new k;class Le extends St{constructor(e=new Ke,t=new Ln){super(),this.isMesh=!0,this.type="Mesh",this.geometry=e,this.material=t,this.morphTargetDictionary=void 0,this.morphTargetInfluences=void 0,this.updateMorphTargets()}copy(e,t){return super.copy(e,t),e.morphTargetInfluences!==void 0&&(this.morphTargetInfluences=e.morphTargetInfluences.slice()),e.morphTargetDictionary!==void 0&&(this.morphTargetDictionary=Object.assign({},e.morphTargetDictionary)),this.material=Array.isArray(e.material)?e.material.slice():e.material,this.geometry=e.geometry,this}updateMorphTargets(){const t=this.geometry.morphAttributes,i=Object.keys(t);if(i.length>0){const r=t[i[0]];if(r!==void 0){this.morphTargetInfluences=[],this.morphTargetDictionary={};for(let s=0,a=r.length;s<a;s++){const o=r[s].name||String(s);this.morphTargetInfluences.push(0),this.morphTargetDictionary[o]=s}}}}getVertexPosition(e,t){const i=this.geometry,r=i.attributes.position,s=i.morphAttributes.position,a=i.morphTargetsRelative;t.fromBufferAttribute(r,e);const o=this.morphTargetInfluences;if(s&&o){Er.set(0,0,0);for(let c=0,l=s.length;c<l;c++){const d=o[c],h=s[c];d!==0&&(xs.fromBufferAttribute(h,e),a?Er.addScaledVector(xs,d):Er.addScaledVector(xs.sub(t),d))}t.add(Er)}return t}raycast(e,t){const i=this.geometry,r=this.material,s=this.matrixWorld;r!==void 0&&(i.boundingSphere===null&&i.computeBoundingSphere(),vr.copy(i.boundingSphere),vr.applyMatrix4(s),Fn.copy(e.ray).recast(e.near),!(vr.containsPoint(Fn.origin)===!1&&(Fn.intersectSphere(vr,Co)===null||Fn.origin.distanceToSquared(Co)>(e.far-e.near)**2))&&(Ro.copy(s).invert(),Fn.copy(e.ray).applyMatrix4(Ro),!(i.boundingBox!==null&&Fn.intersectsBox(i.boundingBox)===!1)&&this._computeIntersections(e,t,Fn)))}_computeIntersections(e,t,i){let r;const s=this.geometry,a=this.material,o=s.index,c=s.attributes.position,l=s.attributes.uv,d=s.attributes.uv1,h=s.attributes.normal,f=s.groups,m=s.drawRange;if(o!==null)if(Array.isArray(a))for(let g=0,_=f.length;g<_;g++){const p=f[g],u=a[p.materialIndex],E=Math.max(p.start,m.start),y=Math.min(o.count,Math.min(p.start+p.count,m.start+m.count));for(let M=E,D=y;M<D;M+=3){const w=o.getX(M),b=o.getX(M+1),C=o.getX(M+2);r=br(this,u,e,i,l,d,h,w,b,C),r&&(r.faceIndex=Math.floor(M/3),r.face.materialIndex=p.materialIndex,t.push(r))}}else{const g=Math.max(0,m.start),_=Math.min(o.count,m.start+m.count);for(let p=g,u=_;p<u;p+=3){const E=o.getX(p),y=o.getX(p+1),M=o.getX(p+2);r=br(this,a,e,i,l,d,h,E,y,M),r&&(r.faceIndex=Math.floor(p/3),t.push(r))}}else if(c!==void 0)if(Array.isArray(a))for(let g=0,_=f.length;g<_;g++){const p=f[g],u=a[p.materialIndex],E=Math.max(p.start,m.start),y=Math.min(c.count,Math.min(p.start+p.count,m.start+m.count));for(let M=E,D=y;M<D;M+=3){const w=M,b=M+1,C=M+2;r=br(this,u,e,i,l,d,h,w,b,C),r&&(r.faceIndex=Math.floor(M/3),r.face.materialIndex=p.materialIndex,t.push(r))}}else{const g=Math.max(0,m.start),_=Math.min(c.count,m.start+m.count);for(let p=g,u=_;p<u;p+=3){const E=p,y=p+1,M=p+2;r=br(this,a,e,i,l,d,h,E,y,M),r&&(r.faceIndex=Math.floor(p/3),t.push(r))}}}}function bu(n,e,t,i,r,s,a,o){let c;if(e.side===Ct?c=i.intersectTriangle(a,s,r,!0,o):c=i.intersectTriangle(r,s,a,e.side===Pn,o),c===null)return null;yr.copy(o),yr.applyMatrix4(n.matrixWorld);const l=t.ray.origin.distanceTo(yr);return l<t.near||l>t.far?null:{distance:l,point:yr.clone(),object:n}}function br(n,e,t,i,r,s,a,o,c,l){n.getVertexPosition(o,xr),n.getVertexPosition(c,Mr),n.getVertexPosition(l,Sr);const d=bu(n,e,t,i,xr,Mr,Sr,Po);if(d){const h=new k;Ht.getBarycoord(Po,xr,Mr,Sr,h),r&&(d.uv=Ht.getInterpolatedAttribute(r,o,c,l,h,new We)),s&&(d.uv1=Ht.getInterpolatedAttribute(s,o,c,l,h,new We)),a&&(d.normal=Ht.getInterpolatedAttribute(a,o,c,l,h,new k),d.normal.dot(i.direction)>0&&d.normal.multiplyScalar(-1));const f={a:o,b:c,c:l,normal:new k,materialIndex:0};Ht.getNormal(xr,Mr,Sr,f.normal),d.face=f,d.barycoord=h}return d}class Jt extends Ke{constructor(e=1,t=1,i=1,r=1,s=1,a=1){super(),this.type="BoxGeometry",this.parameters={width:e,height:t,depth:i,widthSegments:r,heightSegments:s,depthSegments:a};const o=this;r=Math.floor(r),s=Math.floor(s),a=Math.floor(a);const c=[],l=[],d=[],h=[];let f=0,m=0;g("z","y","x",-1,-1,i,t,e,a,s,0),g("z","y","x",1,-1,i,t,-e,a,s,1),g("x","z","y",1,1,e,i,t,r,a,2),g("x","z","y",1,-1,e,i,-t,r,a,3),g("x","y","z",1,-1,e,t,i,r,s,4),g("x","y","z",-1,-1,e,t,-i,r,s,5),this.setIndex(c),this.setAttribute("position",new je(l,3)),this.setAttribute("normal",new je(d,3)),this.setAttribute("uv",new je(h,2));function g(_,p,u,E,y,M,D,w,b,C,v){const x=M/b,P=D/C,U=M/2,A=D/2,R=w/2,z=b+1,N=C+1;let O=0,F=0;const G=new k;for(let Z=0;Z<N;Z++){const Y=Z*P-A;for(let he=0;he<z;he++){const Ie=he*x-U;G[_]=Ie*E,G[p]=Y*y,G[u]=R,l.push(G.x,G.y,G.z),G[_]=0,G[p]=0,G[u]=w>0?1:-1,d.push(G.x,G.y,G.z),h.push(he/b),h.push(1-Z/C),O+=1}}for(let Z=0;Z<C;Z++)for(let Y=0;Y<b;Y++){const he=f+Y+z*Z,Ie=f+Y+z*(Z+1),X=f+(Y+1)+z*(Z+1),ee=f+(Y+1)+z*Z;c.push(he,Ie,ee),c.push(Ie,X,ee),F+=6}o.addGroup(m,F,v),m+=F,f+=O}}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}static fromJSON(e){return new Jt(e.width,e.height,e.depth,e.widthSegments,e.heightSegments,e.depthSegments)}}function Ui(n){const e={};for(const t in n){e[t]={};for(const i in n[t]){const r=n[t][i];r&&(r.isColor||r.isMatrix3||r.isMatrix4||r.isVector2||r.isVector3||r.isVector4||r.isTexture||r.isQuaternion)?r.isRenderTargetTexture?(console.warn("UniformsUtils: Textures of render targets cannot be cloned via cloneUniforms() or mergeUniforms()."),e[t][i]=null):e[t][i]=r.clone():Array.isArray(r)?e[t][i]=r.slice():e[t][i]=r}}return e}function Rt(n){const e={};for(let t=0;t<n.length;t++){const i=Ui(n[t]);for(const r in i)e[r]=i[r]}return e}function Tu(n){const e=[];for(let t=0;t<n.length;t++)e.push(n[t].clone());return e}function qc(n){const e=n.getRenderTarget();return e===null?n.outputColorSpace:e.isXRRenderTarget===!0?e.texture.colorSpace:Je.workingColorSpace}const Au={clone:Ui,merge:Rt};var wu=`void main() {
	gl_Position = projectionMatrix * modelViewMatrix * vec4( position, 1.0 );
}`,Ru=`void main() {
	gl_FragColor = vec4( 1.0, 0.0, 0.0, 1.0 );
}`;class Dn extends ki{constructor(e){super(),this.isShaderMaterial=!0,this.type="ShaderMaterial",this.defines={},this.uniforms={},this.uniformsGroups=[],this.vertexShader=wu,this.fragmentShader=Ru,this.linewidth=1,this.wireframe=!1,this.wireframeLinewidth=1,this.fog=!1,this.lights=!1,this.clipping=!1,this.forceSinglePass=!0,this.extensions={clipCullDistance:!1,multiDraw:!1},this.defaultAttributeValues={color:[1,1,1],uv:[0,0],uv1:[0,0]},this.index0AttributeName=void 0,this.uniformsNeedUpdate=!1,this.glslVersion=null,e!==void 0&&this.setValues(e)}copy(e){return super.copy(e),this.fragmentShader=e.fragmentShader,this.vertexShader=e.vertexShader,this.uniforms=Ui(e.uniforms),this.uniformsGroups=Tu(e.uniformsGroups),this.defines=Object.assign({},e.defines),this.wireframe=e.wireframe,this.wireframeLinewidth=e.wireframeLinewidth,this.fog=e.fog,this.lights=e.lights,this.clipping=e.clipping,this.extensions=Object.assign({},e.extensions),this.glslVersion=e.glslVersion,this}toJSON(e){const t=super.toJSON(e);t.glslVersion=this.glslVersion,t.uniforms={};for(const r in this.uniforms){const a=this.uniforms[r].value;a&&a.isTexture?t.uniforms[r]={type:"t",value:a.toJSON(e).uuid}:a&&a.isColor?t.uniforms[r]={type:"c",value:a.getHex()}:a&&a.isVector2?t.uniforms[r]={type:"v2",value:a.toArray()}:a&&a.isVector3?t.uniforms[r]={type:"v3",value:a.toArray()}:a&&a.isVector4?t.uniforms[r]={type:"v4",value:a.toArray()}:a&&a.isMatrix3?t.uniforms[r]={type:"m3",value:a.toArray()}:a&&a.isMatrix4?t.uniforms[r]={type:"m4",value:a.toArray()}:t.uniforms[r]={value:a}}Object.keys(this.defines).length>0&&(t.defines=this.defines),t.vertexShader=this.vertexShader,t.fragmentShader=this.fragmentShader,t.lights=this.lights,t.clipping=this.clipping;const i={};for(const r in this.extensions)this.extensions[r]===!0&&(i[r]=!0);return Object.keys(i).length>0&&(t.extensions=i),t}}class Kc extends St{constructor(){super(),this.isCamera=!0,this.type="Camera",this.matrixWorldInverse=new at,this.projectionMatrix=new at,this.projectionMatrixInverse=new at,this.coordinateSystem=hn}copy(e,t){return super.copy(e,t),this.matrixWorldInverse.copy(e.matrixWorldInverse),this.projectionMatrix.copy(e.projectionMatrix),this.projectionMatrixInverse.copy(e.projectionMatrixInverse),this.coordinateSystem=e.coordinateSystem,this}getWorldDirection(e){return super.getWorldDirection(e).negate()}updateMatrixWorld(e){super.updateMatrixWorld(e),this.matrixWorldInverse.copy(this.matrixWorld).invert()}updateWorldMatrix(e,t){super.updateWorldMatrix(e,t),this.matrixWorldInverse.copy(this.matrixWorld).invert()}clone(){return new this.constructor().copy(this)}}const Sn=new k,Do=new We,Lo=new We;class Ft extends Kc{constructor(e=50,t=1,i=.1,r=2e3){super(),this.isPerspectiveCamera=!0,this.type="PerspectiveCamera",this.fov=e,this.zoom=1,this.near=i,this.far=r,this.focus=10,this.aspect=t,this.view=null,this.filmGauge=35,this.filmOffset=0,this.updateProjectionMatrix()}copy(e,t){return super.copy(e,t),this.fov=e.fov,this.zoom=e.zoom,this.near=e.near,this.far=e.far,this.focus=e.focus,this.aspect=e.aspect,this.view=e.view===null?null:Object.assign({},e.view),this.filmGauge=e.filmGauge,this.filmOffset=e.filmOffset,this}setFocalLength(e){const t=.5*this.getFilmHeight()/e;this.fov=ya*2*Math.atan(t),this.updateProjectionMatrix()}getFocalLength(){const e=Math.tan(Br*.5*this.fov);return .5*this.getFilmHeight()/e}getEffectiveFOV(){return ya*2*Math.atan(Math.tan(Br*.5*this.fov)/this.zoom)}getFilmWidth(){return this.filmGauge*Math.min(this.aspect,1)}getFilmHeight(){return this.filmGauge/Math.max(this.aspect,1)}getViewBounds(e,t,i){Sn.set(-1,-1,.5).applyMatrix4(this.projectionMatrixInverse),t.set(Sn.x,Sn.y).multiplyScalar(-e/Sn.z),Sn.set(1,1,.5).applyMatrix4(this.projectionMatrixInverse),i.set(Sn.x,Sn.y).multiplyScalar(-e/Sn.z)}getViewSize(e,t){return this.getViewBounds(e,Do,Lo),t.subVectors(Lo,Do)}setViewOffset(e,t,i,r,s,a){this.aspect=e/t,this.view===null&&(this.view={enabled:!0,fullWidth:1,fullHeight:1,offsetX:0,offsetY:0,width:1,height:1}),this.view.enabled=!0,this.view.fullWidth=e,this.view.fullHeight=t,this.view.offsetX=i,this.view.offsetY=r,this.view.width=s,this.view.height=a,this.updateProjectionMatrix()}clearViewOffset(){this.view!==null&&(this.view.enabled=!1),this.updateProjectionMatrix()}updateProjectionMatrix(){const e=this.near;let t=e*Math.tan(Br*.5*this.fov)/this.zoom,i=2*t,r=this.aspect*i,s=-.5*r;const a=this.view;if(this.view!==null&&this.view.enabled){const c=a.fullWidth,l=a.fullHeight;s+=a.offsetX*r/c,t-=a.offsetY*i/l,r*=a.width/c,i*=a.height/l}const o=this.filmOffset;o!==0&&(s+=e*o/this.getFilmWidth()),this.projectionMatrix.makePerspective(s,s+r,t,t-i,e,this.far,this.coordinateSystem),this.projectionMatrixInverse.copy(this.projectionMatrix).invert()}toJSON(e){const t=super.toJSON(e);return t.object.fov=this.fov,t.object.zoom=this.zoom,t.object.near=this.near,t.object.far=this.far,t.object.focus=this.focus,t.object.aspect=this.aspect,this.view!==null&&(t.object.view=Object.assign({},this.view)),t.object.filmGauge=this.filmGauge,t.object.filmOffset=this.filmOffset,t}}const gi=-90,_i=1;class Cu extends St{constructor(e,t,i){super(),this.type="CubeCamera",this.renderTarget=i,this.coordinateSystem=null,this.activeMipmapLevel=0;const r=new Ft(gi,_i,e,t);r.layers=this.layers,this.add(r);const s=new Ft(gi,_i,e,t);s.layers=this.layers,this.add(s);const a=new Ft(gi,_i,e,t);a.layers=this.layers,this.add(a);const o=new Ft(gi,_i,e,t);o.layers=this.layers,this.add(o);const c=new Ft(gi,_i,e,t);c.layers=this.layers,this.add(c);const l=new Ft(gi,_i,e,t);l.layers=this.layers,this.add(l)}updateCoordinateSystem(){const e=this.coordinateSystem,t=this.children.concat(),[i,r,s,a,o,c]=t;for(const l of t)this.remove(l);if(e===hn)i.up.set(0,1,0),i.lookAt(1,0,0),r.up.set(0,1,0),r.lookAt(-1,0,0),s.up.set(0,0,-1),s.lookAt(0,1,0),a.up.set(0,0,1),a.lookAt(0,-1,0),o.up.set(0,1,0),o.lookAt(0,0,1),c.up.set(0,1,0),c.lookAt(0,0,-1);else if(e===jr)i.up.set(0,-1,0),i.lookAt(-1,0,0),r.up.set(0,-1,0),r.lookAt(1,0,0),s.up.set(0,0,1),s.lookAt(0,1,0),a.up.set(0,0,-1),a.lookAt(0,-1,0),o.up.set(0,-1,0),o.lookAt(0,0,1),c.up.set(0,-1,0),c.lookAt(0,0,-1);else throw new Error("THREE.CubeCamera.updateCoordinateSystem(): Invalid coordinate system: "+e);for(const l of t)this.add(l),l.updateMatrixWorld()}update(e,t){this.parent===null&&this.updateMatrixWorld();const{renderTarget:i,activeMipmapLevel:r}=this;this.coordinateSystem!==e.coordinateSystem&&(this.coordinateSystem=e.coordinateSystem,this.updateCoordinateSystem());const[s,a,o,c,l,d]=this.children,h=e.getRenderTarget(),f=e.getActiveCubeFace(),m=e.getActiveMipmapLevel(),g=e.xr.enabled;e.xr.enabled=!1;const _=i.texture.generateMipmaps;i.texture.generateMipmaps=!1,e.setRenderTarget(i,0,r),e.render(t,s),e.setRenderTarget(i,1,r),e.render(t,a),e.setRenderTarget(i,2,r),e.render(t,o),e.setRenderTarget(i,3,r),e.render(t,c),e.setRenderTarget(i,4,r),e.render(t,l),i.texture.generateMipmaps=_,e.setRenderTarget(i,5,r),e.render(t,d),e.setRenderTarget(h,f,m),e.xr.enabled=g,i.texture.needsPMREMUpdate=!0}}class Yc extends At{constructor(e,t,i,r,s,a,o,c,l,d){e=e!==void 0?e:[],t=t!==void 0?t:Ci,super(e,t,i,r,s,a,o,c,l,d),this.isCubeTexture=!0,this.flipY=!1}get images(){return this.image}set images(e){this.image=e}}class Pu extends ei{constructor(e=1,t={}){super(e,e,t),this.isWebGLCubeRenderTarget=!0;const i={width:e,height:e,depth:1},r=[i,i,i,i,i,i];this.texture=new Yc(r,t.mapping,t.wrapS,t.wrapT,t.magFilter,t.minFilter,t.format,t.type,t.anisotropy,t.colorSpace),this.texture.isRenderTargetTexture=!0,this.texture.generateMipmaps=t.generateMipmaps!==void 0?t.generateMipmaps:!1,this.texture.minFilter=t.minFilter!==void 0?t.minFilter:Zt}fromEquirectangularTexture(e,t){this.texture.type=t.type,this.texture.colorSpace=t.colorSpace,this.texture.generateMipmaps=t.generateMipmaps,this.texture.minFilter=t.minFilter,this.texture.magFilter=t.magFilter;const i={uniforms:{tEquirect:{value:null}},vertexShader:`

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
			`},r=new Jt(5,5,5),s=new Dn({name:"CubemapFromEquirect",uniforms:Ui(i.uniforms),vertexShader:i.vertexShader,fragmentShader:i.fragmentShader,side:Ct,blending:Rn});s.uniforms.tEquirect.value=t;const a=new Le(r,s),o=t.minFilter;return t.minFilter===$n&&(t.minFilter=Zt),new Cu(1,10,this).update(e,a),t.minFilter=o,a.geometry.dispose(),a.material.dispose(),this}clear(e,t,i,r){const s=e.getRenderTarget();for(let a=0;a<6;a++)e.setRenderTarget(this,a),e.clear(t,i,r);e.setRenderTarget(s)}}class nt extends St{constructor(){super(),this.isGroup=!0,this.type="Group"}}const Du={type:"move"};class Ms{constructor(){this._targetRay=null,this._grip=null,this._hand=null}getHandSpace(){return this._hand===null&&(this._hand=new nt,this._hand.matrixAutoUpdate=!1,this._hand.visible=!1,this._hand.joints={},this._hand.inputState={pinching:!1}),this._hand}getTargetRaySpace(){return this._targetRay===null&&(this._targetRay=new nt,this._targetRay.matrixAutoUpdate=!1,this._targetRay.visible=!1,this._targetRay.hasLinearVelocity=!1,this._targetRay.linearVelocity=new k,this._targetRay.hasAngularVelocity=!1,this._targetRay.angularVelocity=new k),this._targetRay}getGripSpace(){return this._grip===null&&(this._grip=new nt,this._grip.matrixAutoUpdate=!1,this._grip.visible=!1,this._grip.hasLinearVelocity=!1,this._grip.linearVelocity=new k,this._grip.hasAngularVelocity=!1,this._grip.angularVelocity=new k),this._grip}dispatchEvent(e){return this._targetRay!==null&&this._targetRay.dispatchEvent(e),this._grip!==null&&this._grip.dispatchEvent(e),this._hand!==null&&this._hand.dispatchEvent(e),this}connect(e){if(e&&e.hand){const t=this._hand;if(t)for(const i of e.hand.values())this._getHandJoint(t,i)}return this.dispatchEvent({type:"connected",data:e}),this}disconnect(e){return this.dispatchEvent({type:"disconnected",data:e}),this._targetRay!==null&&(this._targetRay.visible=!1),this._grip!==null&&(this._grip.visible=!1),this._hand!==null&&(this._hand.visible=!1),this}update(e,t,i){let r=null,s=null,a=null;const o=this._targetRay,c=this._grip,l=this._hand;if(e&&t.session.visibilityState!=="visible-blurred"){if(l&&e.hand){a=!0;for(const _ of e.hand.values()){const p=t.getJointPose(_,i),u=this._getHandJoint(l,_);p!==null&&(u.matrix.fromArray(p.transform.matrix),u.matrix.decompose(u.position,u.rotation,u.scale),u.matrixWorldNeedsUpdate=!0,u.jointRadius=p.radius),u.visible=p!==null}const d=l.joints["index-finger-tip"],h=l.joints["thumb-tip"],f=d.position.distanceTo(h.position),m=.02,g=.005;l.inputState.pinching&&f>m+g?(l.inputState.pinching=!1,this.dispatchEvent({type:"pinchend",handedness:e.handedness,target:this})):!l.inputState.pinching&&f<=m-g&&(l.inputState.pinching=!0,this.dispatchEvent({type:"pinchstart",handedness:e.handedness,target:this}))}else c!==null&&e.gripSpace&&(s=t.getPose(e.gripSpace,i),s!==null&&(c.matrix.fromArray(s.transform.matrix),c.matrix.decompose(c.position,c.rotation,c.scale),c.matrixWorldNeedsUpdate=!0,s.linearVelocity?(c.hasLinearVelocity=!0,c.linearVelocity.copy(s.linearVelocity)):c.hasLinearVelocity=!1,s.angularVelocity?(c.hasAngularVelocity=!0,c.angularVelocity.copy(s.angularVelocity)):c.hasAngularVelocity=!1));o!==null&&(r=t.getPose(e.targetRaySpace,i),r===null&&s!==null&&(r=s),r!==null&&(o.matrix.fromArray(r.transform.matrix),o.matrix.decompose(o.position,o.rotation,o.scale),o.matrixWorldNeedsUpdate=!0,r.linearVelocity?(o.hasLinearVelocity=!0,o.linearVelocity.copy(r.linearVelocity)):o.hasLinearVelocity=!1,r.angularVelocity?(o.hasAngularVelocity=!0,o.angularVelocity.copy(r.angularVelocity)):o.hasAngularVelocity=!1,this.dispatchEvent(Du)))}return o!==null&&(o.visible=r!==null),c!==null&&(c.visible=s!==null),l!==null&&(l.visible=a!==null),this}_getHandJoint(e,t){if(e.joints[t.jointName]===void 0){const i=new nt;i.matrixAutoUpdate=!1,i.visible=!1,e.joints[t.jointName]=i,e.add(i)}return e.joints[t.jointName]}}class $c extends St{constructor(){super(),this.isScene=!0,this.type="Scene",this.background=null,this.environment=null,this.fog=null,this.backgroundBlurriness=0,this.backgroundIntensity=1,this.backgroundRotation=new xt,this.environmentIntensity=1,this.environmentRotation=new xt,this.overrideMaterial=null,typeof __THREE_DEVTOOLS__<"u"&&__THREE_DEVTOOLS__.dispatchEvent(new CustomEvent("observe",{detail:this}))}copy(e,t){return super.copy(e,t),e.background!==null&&(this.background=e.background.clone()),e.environment!==null&&(this.environment=e.environment.clone()),e.fog!==null&&(this.fog=e.fog.clone()),this.backgroundBlurriness=e.backgroundBlurriness,this.backgroundIntensity=e.backgroundIntensity,this.backgroundRotation.copy(e.backgroundRotation),this.environmentIntensity=e.environmentIntensity,this.environmentRotation.copy(e.environmentRotation),e.overrideMaterial!==null&&(this.overrideMaterial=e.overrideMaterial.clone()),this.matrixAutoUpdate=e.matrixAutoUpdate,this}toJSON(e){const t=super.toJSON(e);return this.fog!==null&&(t.object.fog=this.fog.toJSON()),this.backgroundBlurriness>0&&(t.object.backgroundBlurriness=this.backgroundBlurriness),this.backgroundIntensity!==1&&(t.object.backgroundIntensity=this.backgroundIntensity),t.object.backgroundRotation=this.backgroundRotation.toArray(),this.environmentIntensity!==1&&(t.object.environmentIntensity=this.environmentIntensity),t.object.environmentRotation=this.environmentRotation.toArray(),t}}class Lu extends At{constructor(e=null,t=1,i=1,r,s,a,o,c,l=kt,d=kt,h,f){super(null,a,o,c,l,d,r,s,h,f),this.isDataTexture=!0,this.image={data:e,width:t,height:i},this.generateMipmaps=!1,this.flipY=!1,this.unpackAlignment=1}}const Ss=new k,Iu=new k,Uu=new Ve;class Hn{constructor(e=new k(1,0,0),t=0){this.isPlane=!0,this.normal=e,this.constant=t}set(e,t){return this.normal.copy(e),this.constant=t,this}setComponents(e,t,i,r){return this.normal.set(e,t,i),this.constant=r,this}setFromNormalAndCoplanarPoint(e,t){return this.normal.copy(e),this.constant=-t.dot(this.normal),this}setFromCoplanarPoints(e,t,i){const r=Ss.subVectors(i,t).cross(Iu.subVectors(e,t)).normalize();return this.setFromNormalAndCoplanarPoint(r,e),this}copy(e){return this.normal.copy(e.normal),this.constant=e.constant,this}normalize(){const e=1/this.normal.length();return this.normal.multiplyScalar(e),this.constant*=e,this}negate(){return this.constant*=-1,this.normal.negate(),this}distanceToPoint(e){return this.normal.dot(e)+this.constant}distanceToSphere(e){return this.distanceToPoint(e.center)-e.radius}projectPoint(e,t){return t.copy(e).addScaledVector(this.normal,-this.distanceToPoint(e))}intersectLine(e,t){const i=e.delta(Ss),r=this.normal.dot(i);if(r===0)return this.distanceToPoint(e.start)===0?t.copy(e.start):null;const s=-(e.start.dot(this.normal)+this.constant)/r;return s<0||s>1?null:t.copy(e.start).addScaledVector(i,s)}intersectsLine(e){const t=this.distanceToPoint(e.start),i=this.distanceToPoint(e.end);return t<0&&i>0||i<0&&t>0}intersectsBox(e){return e.intersectsPlane(this)}intersectsSphere(e){return e.intersectsPlane(this)}coplanarPoint(e){return e.copy(this.normal).multiplyScalar(-this.constant)}applyMatrix4(e,t){const i=t||Uu.getNormalMatrix(e),r=this.coplanarPoint(Ss).applyMatrix4(e),s=this.normal.applyMatrix3(i).normalize();return this.constant=-r.dot(s),this}translate(e){return this.constant-=e.dot(this.normal),this}equals(e){return e.normal.equals(this.normal)&&e.constant===this.constant}clone(){return new this.constructor().copy(this)}}const kn=new Yr,Tr=new k;class Ha{constructor(e=new Hn,t=new Hn,i=new Hn,r=new Hn,s=new Hn,a=new Hn){this.planes=[e,t,i,r,s,a]}set(e,t,i,r,s,a){const o=this.planes;return o[0].copy(e),o[1].copy(t),o[2].copy(i),o[3].copy(r),o[4].copy(s),o[5].copy(a),this}copy(e){const t=this.planes;for(let i=0;i<6;i++)t[i].copy(e.planes[i]);return this}setFromProjectionMatrix(e,t=hn){const i=this.planes,r=e.elements,s=r[0],a=r[1],o=r[2],c=r[3],l=r[4],d=r[5],h=r[6],f=r[7],m=r[8],g=r[9],_=r[10],p=r[11],u=r[12],E=r[13],y=r[14],M=r[15];if(i[0].setComponents(c-s,f-l,p-m,M-u).normalize(),i[1].setComponents(c+s,f+l,p+m,M+u).normalize(),i[2].setComponents(c+a,f+d,p+g,M+E).normalize(),i[3].setComponents(c-a,f-d,p-g,M-E).normalize(),i[4].setComponents(c-o,f-h,p-_,M-y).normalize(),t===hn)i[5].setComponents(c+o,f+h,p+_,M+y).normalize();else if(t===jr)i[5].setComponents(o,h,_,y).normalize();else throw new Error("THREE.Frustum.setFromProjectionMatrix(): Invalid coordinate system: "+t);return this}intersectsObject(e){if(e.boundingSphere!==void 0)e.boundingSphere===null&&e.computeBoundingSphere(),kn.copy(e.boundingSphere).applyMatrix4(e.matrixWorld);else{const t=e.geometry;t.boundingSphere===null&&t.computeBoundingSphere(),kn.copy(t.boundingSphere).applyMatrix4(e.matrixWorld)}return this.intersectsSphere(kn)}intersectsSprite(e){return kn.center.set(0,0,0),kn.radius=.7071067811865476,kn.applyMatrix4(e.matrixWorld),this.intersectsSphere(kn)}intersectsSphere(e){const t=this.planes,i=e.center,r=-e.radius;for(let s=0;s<6;s++)if(t[s].distanceToPoint(i)<r)return!1;return!0}intersectsBox(e){const t=this.planes;for(let i=0;i<6;i++){const r=t[i];if(Tr.x=r.normal.x>0?e.max.x:e.min.x,Tr.y=r.normal.y>0?e.max.y:e.min.y,Tr.z=r.normal.z>0?e.max.z:e.min.z,r.distanceToPoint(Tr)<0)return!1}return!0}containsPoint(e){const t=this.planes;for(let i=0;i<6;i++)if(t[i].distanceToPoint(e)<0)return!1;return!0}clone(){return new this.constructor().copy(this)}}class mt extends ki{constructor(e){super(),this.isLineBasicMaterial=!0,this.type="LineBasicMaterial",this.color=new oe(16777215),this.map=null,this.linewidth=1,this.linecap="round",this.linejoin="round",this.fog=!0,this.setValues(e)}copy(e){return super.copy(e),this.color.copy(e.color),this.map=e.map,this.linewidth=e.linewidth,this.linecap=e.linecap,this.linejoin=e.linejoin,this.fog=e.fog,this}}const Xr=new k,qr=new k,Io=new at,Xi=new Ba,Ar=new Yr,Es=new k,Uo=new k;class $i extends St{constructor(e=new Ke,t=new mt){super(),this.isLine=!0,this.type="Line",this.geometry=e,this.material=t,this.morphTargetDictionary=void 0,this.morphTargetInfluences=void 0,this.updateMorphTargets()}copy(e,t){return super.copy(e,t),this.material=Array.isArray(e.material)?e.material.slice():e.material,this.geometry=e.geometry,this}computeLineDistances(){const e=this.geometry;if(e.index===null){const t=e.attributes.position,i=[0];for(let r=1,s=t.count;r<s;r++)Xr.fromBufferAttribute(t,r-1),qr.fromBufferAttribute(t,r),i[r]=i[r-1],i[r]+=Xr.distanceTo(qr);e.setAttribute("lineDistance",new je(i,1))}else console.warn("THREE.Line.computeLineDistances(): Computation only possible with non-indexed BufferGeometry.");return this}raycast(e,t){const i=this.geometry,r=this.matrixWorld,s=e.params.Line.threshold,a=i.drawRange;if(i.boundingSphere===null&&i.computeBoundingSphere(),Ar.copy(i.boundingSphere),Ar.applyMatrix4(r),Ar.radius+=s,e.ray.intersectsSphere(Ar)===!1)return;Io.copy(r).invert(),Xi.copy(e.ray).applyMatrix4(Io);const o=s/((this.scale.x+this.scale.y+this.scale.z)/3),c=o*o,l=this.isLineSegments?2:1,d=i.index,f=i.attributes.position;if(d!==null){const m=Math.max(0,a.start),g=Math.min(d.count,a.start+a.count);for(let _=m,p=g-1;_<p;_+=l){const u=d.getX(_),E=d.getX(_+1),y=wr(this,e,Xi,c,u,E,_);y&&t.push(y)}if(this.isLineLoop){const _=d.getX(g-1),p=d.getX(m),u=wr(this,e,Xi,c,_,p,g-1);u&&t.push(u)}}else{const m=Math.max(0,a.start),g=Math.min(f.count,a.start+a.count);for(let _=m,p=g-1;_<p;_+=l){const u=wr(this,e,Xi,c,_,_+1,_);u&&t.push(u)}if(this.isLineLoop){const _=wr(this,e,Xi,c,g-1,m,g-1);_&&t.push(_)}}}updateMorphTargets(){const t=this.geometry.morphAttributes,i=Object.keys(t);if(i.length>0){const r=t[i[0]];if(r!==void 0){this.morphTargetInfluences=[],this.morphTargetDictionary={};for(let s=0,a=r.length;s<a;s++){const o=r[s].name||String(s);this.morphTargetInfluences.push(0),this.morphTargetDictionary[o]=s}}}}}function wr(n,e,t,i,r,s,a){const o=n.geometry.attributes.position;if(Xr.fromBufferAttribute(o,r),qr.fromBufferAttribute(o,s),t.distanceSqToSegment(Xr,qr,Es,Uo)>i)return;Es.applyMatrix4(n.matrixWorld);const l=e.ray.origin.distanceTo(Es);if(!(l<e.near||l>e.far))return{distance:l,point:Uo.clone().applyMatrix4(n.matrixWorld),index:a,face:null,faceIndex:null,barycoord:null,object:n}}const zo=new k,No=new k;class dt extends $i{constructor(e,t){super(e,t),this.isLineSegments=!0,this.type="LineSegments"}computeLineDistances(){const e=this.geometry;if(e.index===null){const t=e.attributes.position,i=[];for(let r=0,s=t.count;r<s;r+=2)zo.fromBufferAttribute(t,r),No.fromBufferAttribute(t,r+1),i[r]=r===0?0:i[r-1],i[r+1]=i[r]+zo.distanceTo(No);e.setAttribute("lineDistance",new je(i,1))}else console.warn("THREE.LineSegments.computeLineDistances(): Computation only possible with non-indexed BufferGeometry.");return this}}class Zc extends At{constructor(e,t,i,r,s,a,o,c,l,d=Ai){if(d!==Ai&&d!==Li)throw new Error("DepthTexture format must be either THREE.DepthFormat or THREE.DepthStencilFormat");i===void 0&&d===Ai&&(i=Qn),i===void 0&&d===Li&&(i=Di),super(null,r,s,a,o,c,d,i,l),this.isDepthTexture=!0,this.image={width:e,height:t},this.magFilter=o!==void 0?o:kt,this.minFilter=c!==void 0?c:kt,this.flipY=!1,this.generateMipmaps=!1,this.compareFunction=null}copy(e){return super.copy(e),this.source=new Oa(Object.assign({},e.image)),this.compareFunction=e.compareFunction,this}toJSON(e){const t=super.toJSON(e);return this.compareFunction!==null&&(t.compareFunction=this.compareFunction),t}}class sr extends Ke{constructor(e=1,t=1,i=1,r=32,s=1,a=!1,o=0,c=Math.PI*2){super(),this.type="CylinderGeometry",this.parameters={radiusTop:e,radiusBottom:t,height:i,radialSegments:r,heightSegments:s,openEnded:a,thetaStart:o,thetaLength:c};const l=this;r=Math.floor(r),s=Math.floor(s);const d=[],h=[],f=[],m=[];let g=0;const _=[],p=i/2;let u=0;E(),a===!1&&(e>0&&y(!0),t>0&&y(!1)),this.setIndex(d),this.setAttribute("position",new je(h,3)),this.setAttribute("normal",new je(f,3)),this.setAttribute("uv",new je(m,2));function E(){const M=new k,D=new k;let w=0;const b=(t-e)/i;for(let C=0;C<=s;C++){const v=[],x=C/s,P=x*(t-e)+e;for(let U=0;U<=r;U++){const A=U/r,R=A*c+o,z=Math.sin(R),N=Math.cos(R);D.x=P*z,D.y=-x*i+p,D.z=P*N,h.push(D.x,D.y,D.z),M.set(z,b,N).normalize(),f.push(M.x,M.y,M.z),m.push(A,1-x),v.push(g++)}_.push(v)}for(let C=0;C<r;C++)for(let v=0;v<s;v++){const x=_[v][C],P=_[v+1][C],U=_[v+1][C+1],A=_[v][C+1];(e>0||v!==0)&&(d.push(x,P,A),w+=3),(t>0||v!==s-1)&&(d.push(P,U,A),w+=3)}l.addGroup(u,w,0),u+=w}function y(M){const D=g,w=new We,b=new k;let C=0;const v=M===!0?e:t,x=M===!0?1:-1;for(let U=1;U<=r;U++)h.push(0,p*x,0),f.push(0,x,0),m.push(.5,.5),g++;const P=g;for(let U=0;U<=r;U++){const R=U/r*c+o,z=Math.cos(R),N=Math.sin(R);b.x=v*N,b.y=p*x,b.z=v*z,h.push(b.x,b.y,b.z),f.push(0,x,0),w.x=z*.5+.5,w.y=N*.5*x+.5,m.push(w.x,w.y),g++}for(let U=0;U<r;U++){const A=D+U,R=P+U;M===!0?d.push(R,R+1,A):d.push(R+1,R,A),C+=3}l.addGroup(u,C,M===!0?1:2),u+=C}}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}static fromJSON(e){return new sr(e.radiusTop,e.radiusBottom,e.height,e.radialSegments,e.heightSegments,e.openEnded,e.thetaStart,e.thetaLength)}}class Ga extends sr{constructor(e=1,t=1,i=32,r=1,s=!1,a=0,o=Math.PI*2){super(0,e,t,i,r,s,a,o),this.type="ConeGeometry",this.parameters={radius:e,height:t,radialSegments:i,heightSegments:r,openEnded:s,thetaStart:a,thetaLength:o}}static fromJSON(e){return new Ga(e.radius,e.height,e.radialSegments,e.heightSegments,e.openEnded,e.thetaStart,e.thetaLength)}}const Rr=new k,Cr=new k,ys=new k,Pr=new Ht;class Ji extends Ke{constructor(e=null,t=1){if(super(),this.type="EdgesGeometry",this.parameters={geometry:e,thresholdAngle:t},e!==null){const r=Math.pow(10,4),s=Math.cos(Br*t),a=e.getIndex(),o=e.getAttribute("position"),c=a?a.count:o.count,l=[0,0,0],d=["a","b","c"],h=new Array(3),f={},m=[];for(let g=0;g<c;g+=3){a?(l[0]=a.getX(g),l[1]=a.getX(g+1),l[2]=a.getX(g+2)):(l[0]=g,l[1]=g+1,l[2]=g+2);const{a:_,b:p,c:u}=Pr;if(_.fromBufferAttribute(o,l[0]),p.fromBufferAttribute(o,l[1]),u.fromBufferAttribute(o,l[2]),Pr.getNormal(ys),h[0]=`${Math.round(_.x*r)},${Math.round(_.y*r)},${Math.round(_.z*r)}`,h[1]=`${Math.round(p.x*r)},${Math.round(p.y*r)},${Math.round(p.z*r)}`,h[2]=`${Math.round(u.x*r)},${Math.round(u.y*r)},${Math.round(u.z*r)}`,!(h[0]===h[1]||h[1]===h[2]||h[2]===h[0]))for(let E=0;E<3;E++){const y=(E+1)%3,M=h[E],D=h[y],w=Pr[d[E]],b=Pr[d[y]],C=`${M}_${D}`,v=`${D}_${M}`;v in f&&f[v]?(ys.dot(f[v].normal)<=s&&(m.push(w.x,w.y,w.z),m.push(b.x,b.y,b.z)),f[v]=null):C in f||(f[C]={index0:l[E],index1:l[y],normal:ys.clone()})}}for(const g in f)if(f[g]){const{index0:_,index1:p}=f[g];Rr.fromBufferAttribute(o,_),Cr.fromBufferAttribute(o,p),m.push(Rr.x,Rr.y,Rr.z),m.push(Cr.x,Cr.y,Cr.z)}this.setAttribute("position",new je(m,3))}}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}}class ni extends Ke{constructor(e=1,t=1,i=1,r=1){super(),this.type="PlaneGeometry",this.parameters={width:e,height:t,widthSegments:i,heightSegments:r};const s=e/2,a=t/2,o=Math.floor(i),c=Math.floor(r),l=o+1,d=c+1,h=e/o,f=t/c,m=[],g=[],_=[],p=[];for(let u=0;u<d;u++){const E=u*f-a;for(let y=0;y<l;y++){const M=y*h-s;g.push(M,-E,0),_.push(0,0,1),p.push(y/o),p.push(1-u/c)}}for(let u=0;u<c;u++)for(let E=0;E<o;E++){const y=E+l*u,M=E+l*(u+1),D=E+1+l*(u+1),w=E+1+l*u;m.push(y,M,w),m.push(M,D,w)}this.setIndex(m),this.setAttribute("position",new je(g,3)),this.setAttribute("normal",new je(_,3)),this.setAttribute("uv",new je(p,2))}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}static fromJSON(e){return new ni(e.width,e.height,e.widthSegments,e.heightSegments)}}class ja extends Ke{constructor(e=.5,t=1,i=32,r=1,s=0,a=Math.PI*2){super(),this.type="RingGeometry",this.parameters={innerRadius:e,outerRadius:t,thetaSegments:i,phiSegments:r,thetaStart:s,thetaLength:a},i=Math.max(3,i),r=Math.max(1,r);const o=[],c=[],l=[],d=[];let h=e;const f=(t-e)/r,m=new k,g=new We;for(let _=0;_<=r;_++){for(let p=0;p<=i;p++){const u=s+p/i*a;m.x=h*Math.cos(u),m.y=h*Math.sin(u),c.push(m.x,m.y,m.z),l.push(0,0,1),g.x=(m.x/t+1)/2,g.y=(m.y/t+1)/2,d.push(g.x,g.y)}h+=f}for(let _=0;_<r;_++){const p=_*(i+1);for(let u=0;u<i;u++){const E=u+p,y=E,M=E+i+1,D=E+i+2,w=E+1;o.push(y,M,w),o.push(M,D,w)}}this.setIndex(o),this.setAttribute("position",new je(c,3)),this.setAttribute("normal",new je(l,3)),this.setAttribute("uv",new je(d,2))}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}static fromJSON(e){return new ja(e.innerRadius,e.outerRadius,e.thetaSegments,e.phiSegments,e.thetaStart,e.thetaLength)}}class mn extends Ke{constructor(e=1,t=32,i=16,r=0,s=Math.PI*2,a=0,o=Math.PI){super(),this.type="SphereGeometry",this.parameters={radius:e,widthSegments:t,heightSegments:i,phiStart:r,phiLength:s,thetaStart:a,thetaLength:o},t=Math.max(3,Math.floor(t)),i=Math.max(2,Math.floor(i));const c=Math.min(a+o,Math.PI);let l=0;const d=[],h=new k,f=new k,m=[],g=[],_=[],p=[];for(let u=0;u<=i;u++){const E=[],y=u/i;let M=0;u===0&&a===0?M=.5/t:u===i&&c===Math.PI&&(M=-.5/t);for(let D=0;D<=t;D++){const w=D/t;h.x=-e*Math.cos(r+w*s)*Math.sin(a+y*o),h.y=e*Math.cos(a+y*o),h.z=e*Math.sin(r+w*s)*Math.sin(a+y*o),g.push(h.x,h.y,h.z),f.copy(h).normalize(),_.push(f.x,f.y,f.z),p.push(w+M,1-y),E.push(l++)}d.push(E)}for(let u=0;u<i;u++)for(let E=0;E<t;E++){const y=d[u][E+1],M=d[u][E],D=d[u+1][E],w=d[u+1][E+1];(u!==0||a>0)&&m.push(y,M,w),(u!==i-1||c<Math.PI)&&m.push(M,D,w)}this.setIndex(m),this.setAttribute("position",new je(g,3)),this.setAttribute("normal",new je(_,3)),this.setAttribute("uv",new je(p,2))}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}static fromJSON(e){return new mn(e.radius,e.widthSegments,e.heightSegments,e.phiStart,e.phiLength,e.thetaStart,e.thetaLength)}}class pt extends ki{constructor(e){super(),this.isMeshStandardMaterial=!0,this.type="MeshStandardMaterial",this.defines={STANDARD:""},this.color=new oe(16777215),this.roughness=1,this.metalness=0,this.map=null,this.lightMap=null,this.lightMapIntensity=1,this.aoMap=null,this.aoMapIntensity=1,this.emissive=new oe(0),this.emissiveIntensity=1,this.emissiveMap=null,this.bumpMap=null,this.bumpScale=1,this.normalMap=null,this.normalMapType=Bc,this.normalScale=new We(1,1),this.displacementMap=null,this.displacementScale=1,this.displacementBias=0,this.roughnessMap=null,this.metalnessMap=null,this.alphaMap=null,this.envMap=null,this.envMapRotation=new xt,this.envMapIntensity=1,this.wireframe=!1,this.wireframeLinewidth=1,this.wireframeLinecap="round",this.wireframeLinejoin="round",this.flatShading=!1,this.fog=!0,this.setValues(e)}copy(e){return super.copy(e),this.defines={STANDARD:""},this.color.copy(e.color),this.roughness=e.roughness,this.metalness=e.metalness,this.map=e.map,this.lightMap=e.lightMap,this.lightMapIntensity=e.lightMapIntensity,this.aoMap=e.aoMap,this.aoMapIntensity=e.aoMapIntensity,this.emissive.copy(e.emissive),this.emissiveMap=e.emissiveMap,this.emissiveIntensity=e.emissiveIntensity,this.bumpMap=e.bumpMap,this.bumpScale=e.bumpScale,this.normalMap=e.normalMap,this.normalMapType=e.normalMapType,this.normalScale.copy(e.normalScale),this.displacementMap=e.displacementMap,this.displacementScale=e.displacementScale,this.displacementBias=e.displacementBias,this.roughnessMap=e.roughnessMap,this.metalnessMap=e.metalnessMap,this.alphaMap=e.alphaMap,this.envMap=e.envMap,this.envMapRotation.copy(e.envMapRotation),this.envMapIntensity=e.envMapIntensity,this.wireframe=e.wireframe,this.wireframeLinewidth=e.wireframeLinewidth,this.wireframeLinecap=e.wireframeLinecap,this.wireframeLinejoin=e.wireframeLinejoin,this.flatShading=e.flatShading,this.fog=e.fog,this}}class zu extends pt{constructor(e){super(),this.isMeshPhysicalMaterial=!0,this.defines={STANDARD:"",PHYSICAL:""},this.type="MeshPhysicalMaterial",this.anisotropyRotation=0,this.anisotropyMap=null,this.clearcoatMap=null,this.clearcoatRoughness=0,this.clearcoatRoughnessMap=null,this.clearcoatNormalScale=new We(1,1),this.clearcoatNormalMap=null,this.ior=1.5,Object.defineProperty(this,"reflectivity",{get:function(){return Xe(2.5*(this.ior-1)/(this.ior+1),0,1)},set:function(t){this.ior=(1+.4*t)/(1-.4*t)}}),this.iridescenceMap=null,this.iridescenceIOR=1.3,this.iridescenceThicknessRange=[100,400],this.iridescenceThicknessMap=null,this.sheenColor=new oe(0),this.sheenColorMap=null,this.sheenRoughness=1,this.sheenRoughnessMap=null,this.transmissionMap=null,this.thickness=0,this.thicknessMap=null,this.attenuationDistance=1/0,this.attenuationColor=new oe(1,1,1),this.specularIntensity=1,this.specularIntensityMap=null,this.specularColor=new oe(1,1,1),this.specularColorMap=null,this._anisotropy=0,this._clearcoat=0,this._dispersion=0,this._iridescence=0,this._sheen=0,this._transmission=0,this.setValues(e)}get anisotropy(){return this._anisotropy}set anisotropy(e){this._anisotropy>0!=e>0&&this.version++,this._anisotropy=e}get clearcoat(){return this._clearcoat}set clearcoat(e){this._clearcoat>0!=e>0&&this.version++,this._clearcoat=e}get iridescence(){return this._iridescence}set iridescence(e){this._iridescence>0!=e>0&&this.version++,this._iridescence=e}get dispersion(){return this._dispersion}set dispersion(e){this._dispersion>0!=e>0&&this.version++,this._dispersion=e}get sheen(){return this._sheen}set sheen(e){this._sheen>0!=e>0&&this.version++,this._sheen=e}get transmission(){return this._transmission}set transmission(e){this._transmission>0!=e>0&&this.version++,this._transmission=e}copy(e){return super.copy(e),this.defines={STANDARD:"",PHYSICAL:""},this.anisotropy=e.anisotropy,this.anisotropyRotation=e.anisotropyRotation,this.anisotropyMap=e.anisotropyMap,this.clearcoat=e.clearcoat,this.clearcoatMap=e.clearcoatMap,this.clearcoatRoughness=e.clearcoatRoughness,this.clearcoatRoughnessMap=e.clearcoatRoughnessMap,this.clearcoatNormalMap=e.clearcoatNormalMap,this.clearcoatNormalScale.copy(e.clearcoatNormalScale),this.dispersion=e.dispersion,this.ior=e.ior,this.iridescence=e.iridescence,this.iridescenceMap=e.iridescenceMap,this.iridescenceIOR=e.iridescenceIOR,this.iridescenceThicknessRange=[...e.iridescenceThicknessRange],this.iridescenceThicknessMap=e.iridescenceThicknessMap,this.sheen=e.sheen,this.sheenColor.copy(e.sheenColor),this.sheenColorMap=e.sheenColorMap,this.sheenRoughness=e.sheenRoughness,this.sheenRoughnessMap=e.sheenRoughnessMap,this.transmission=e.transmission,this.transmissionMap=e.transmissionMap,this.thickness=e.thickness,this.thicknessMap=e.thicknessMap,this.attenuationDistance=e.attenuationDistance,this.attenuationColor.copy(e.attenuationColor),this.specularIntensity=e.specularIntensity,this.specularIntensityMap=e.specularIntensityMap,this.specularColor.copy(e.specularColor),this.specularColorMap=e.specularColorMap,this}}class Nu extends ki{constructor(e){super(),this.isMeshDepthMaterial=!0,this.type="MeshDepthMaterial",this.depthPacking=ql,this.map=null,this.alphaMap=null,this.displacementMap=null,this.displacementScale=1,this.displacementBias=0,this.wireframe=!1,this.wireframeLinewidth=1,this.setValues(e)}copy(e){return super.copy(e),this.depthPacking=e.depthPacking,this.map=e.map,this.alphaMap=e.alphaMap,this.displacementMap=e.displacementMap,this.displacementScale=e.displacementScale,this.displacementBias=e.displacementBias,this.wireframe=e.wireframe,this.wireframeLinewidth=e.wireframeLinewidth,this}}class Fu extends ki{constructor(e){super(),this.isMeshDistanceMaterial=!0,this.type="MeshDistanceMaterial",this.map=null,this.alphaMap=null,this.displacementMap=null,this.displacementScale=1,this.displacementBias=0,this.setValues(e)}copy(e){return super.copy(e),this.map=e.map,this.alphaMap=e.alphaMap,this.displacementMap=e.displacementMap,this.displacementScale=e.displacementScale,this.displacementBias=e.displacementBias,this}}class ku extends mt{constructor(e){super(),this.isLineDashedMaterial=!0,this.type="LineDashedMaterial",this.scale=1,this.dashSize=3,this.gapSize=1,this.setValues(e)}copy(e){return super.copy(e),this.scale=e.scale,this.dashSize=e.dashSize,this.gapSize=e.gapSize,this}}class Wa extends St{constructor(e,t=1){super(),this.isLight=!0,this.type="Light",this.color=new oe(e),this.intensity=t}dispose(){}copy(e,t){return super.copy(e,t),this.color.copy(e.color),this.intensity=e.intensity,this}toJSON(e){const t=super.toJSON(e);return t.object.color=this.color.getHex(),t.object.intensity=this.intensity,this.groundColor!==void 0&&(t.object.groundColor=this.groundColor.getHex()),this.distance!==void 0&&(t.object.distance=this.distance),this.angle!==void 0&&(t.object.angle=this.angle),this.decay!==void 0&&(t.object.decay=this.decay),this.penumbra!==void 0&&(t.object.penumbra=this.penumbra),this.shadow!==void 0&&(t.object.shadow=this.shadow.toJSON()),this.target!==void 0&&(t.object.target=this.target.uuid),t}}const bs=new at,Fo=new k,ko=new k;class Jc{constructor(e){this.camera=e,this.intensity=1,this.bias=0,this.normalBias=0,this.radius=1,this.blurSamples=8,this.mapSize=new We(512,512),this.map=null,this.mapPass=null,this.matrix=new at,this.autoUpdate=!0,this.needsUpdate=!1,this._frustum=new Ha,this._frameExtents=new We(1,1),this._viewportCount=1,this._viewports=[new rt(0,0,1,1)]}getViewportCount(){return this._viewportCount}getFrustum(){return this._frustum}updateMatrices(e){const t=this.camera,i=this.matrix;Fo.setFromMatrixPosition(e.matrixWorld),t.position.copy(Fo),ko.setFromMatrixPosition(e.target.matrixWorld),t.lookAt(ko),t.updateMatrixWorld(),bs.multiplyMatrices(t.projectionMatrix,t.matrixWorldInverse),this._frustum.setFromProjectionMatrix(bs),i.set(.5,0,0,.5,0,.5,0,.5,0,0,.5,.5,0,0,0,1),i.multiply(bs)}getViewport(e){return this._viewports[e]}getFrameExtents(){return this._frameExtents}dispose(){this.map&&this.map.dispose(),this.mapPass&&this.mapPass.dispose()}copy(e){return this.camera=e.camera.clone(),this.intensity=e.intensity,this.bias=e.bias,this.radius=e.radius,this.mapSize.copy(e.mapSize),this}clone(){return new this.constructor().copy(this)}toJSON(){const e={};return this.intensity!==1&&(e.intensity=this.intensity),this.bias!==0&&(e.bias=this.bias),this.normalBias!==0&&(e.normalBias=this.normalBias),this.radius!==1&&(e.radius=this.radius),(this.mapSize.x!==512||this.mapSize.y!==512)&&(e.mapSize=this.mapSize.toArray()),e.camera=this.camera.toJSON(!1).object,delete e.camera.matrix,e}}const Oo=new at,qi=new k,Ts=new k;class Ou extends Jc{constructor(){super(new Ft(90,1,.5,500)),this.isPointLightShadow=!0,this._frameExtents=new We(4,2),this._viewportCount=6,this._viewports=[new rt(2,1,1,1),new rt(0,1,1,1),new rt(3,1,1,1),new rt(1,1,1,1),new rt(3,0,1,1),new rt(1,0,1,1)],this._cubeDirections=[new k(1,0,0),new k(-1,0,0),new k(0,0,1),new k(0,0,-1),new k(0,1,0),new k(0,-1,0)],this._cubeUps=[new k(0,1,0),new k(0,1,0),new k(0,1,0),new k(0,1,0),new k(0,0,1),new k(0,0,-1)]}updateMatrices(e,t=0){const i=this.camera,r=this.matrix,s=e.distance||i.far;s!==i.far&&(i.far=s,i.updateProjectionMatrix()),qi.setFromMatrixPosition(e.matrixWorld),i.position.copy(qi),Ts.copy(i.position),Ts.add(this._cubeDirections[t]),i.up.copy(this._cubeUps[t]),i.lookAt(Ts),i.updateMatrixWorld(),r.makeTranslation(-qi.x,-qi.y,-qi.z),Oo.multiplyMatrices(i.projectionMatrix,i.matrixWorldInverse),this._frustum.setFromProjectionMatrix(Oo)}}class Bu extends Wa{constructor(e,t,i=0,r=2){super(e,t),this.isPointLight=!0,this.type="PointLight",this.distance=i,this.decay=r,this.shadow=new Ou}get power(){return this.intensity*4*Math.PI}set power(e){this.intensity=e/(4*Math.PI)}dispose(){this.shadow.dispose()}copy(e,t){return super.copy(e,t),this.distance=e.distance,this.decay=e.decay,this.shadow=e.shadow.clone(),this}}class Qc extends Kc{constructor(e=-1,t=1,i=1,r=-1,s=.1,a=2e3){super(),this.isOrthographicCamera=!0,this.type="OrthographicCamera",this.zoom=1,this.view=null,this.left=e,this.right=t,this.top=i,this.bottom=r,this.near=s,this.far=a,this.updateProjectionMatrix()}copy(e,t){return super.copy(e,t),this.left=e.left,this.right=e.right,this.top=e.top,this.bottom=e.bottom,this.near=e.near,this.far=e.far,this.zoom=e.zoom,this.view=e.view===null?null:Object.assign({},e.view),this}setViewOffset(e,t,i,r,s,a){this.view===null&&(this.view={enabled:!0,fullWidth:1,fullHeight:1,offsetX:0,offsetY:0,width:1,height:1}),this.view.enabled=!0,this.view.fullWidth=e,this.view.fullHeight=t,this.view.offsetX=i,this.view.offsetY=r,this.view.width=s,this.view.height=a,this.updateProjectionMatrix()}clearViewOffset(){this.view!==null&&(this.view.enabled=!1),this.updateProjectionMatrix()}updateProjectionMatrix(){const e=(this.right-this.left)/(2*this.zoom),t=(this.top-this.bottom)/(2*this.zoom),i=(this.right+this.left)/2,r=(this.top+this.bottom)/2;let s=i-e,a=i+e,o=r+t,c=r-t;if(this.view!==null&&this.view.enabled){const l=(this.right-this.left)/this.view.fullWidth/this.zoom,d=(this.top-this.bottom)/this.view.fullHeight/this.zoom;s+=l*this.view.offsetX,a=s+l*this.view.width,o-=d*this.view.offsetY,c=o-d*this.view.height}this.projectionMatrix.makeOrthographic(s,a,o,c,this.near,this.far,this.coordinateSystem),this.projectionMatrixInverse.copy(this.projectionMatrix).invert()}toJSON(e){const t=super.toJSON(e);return t.object.zoom=this.zoom,t.object.left=this.left,t.object.right=this.right,t.object.top=this.top,t.object.bottom=this.bottom,t.object.near=this.near,t.object.far=this.far,this.view!==null&&(t.object.view=Object.assign({},this.view)),t}}class Vu extends Jc{constructor(){super(new Qc(-5,5,5,-5,.5,500)),this.isDirectionalLightShadow=!0}}class Bo extends Wa{constructor(e,t){super(e,t),this.isDirectionalLight=!0,this.type="DirectionalLight",this.position.copy(St.DEFAULT_UP),this.updateMatrix(),this.target=new St,this.shadow=new Vu}dispose(){this.shadow.dispose()}copy(e){return super.copy(e),this.target=e.target.clone(),this.shadow=e.shadow.clone(),this}}class Hu extends Wa{constructor(e,t){super(e,t),this.isAmbientLight=!0,this.type="AmbientLight"}}class Gu extends Ft{constructor(e=[]){super(),this.isArrayCamera=!0,this.cameras=e,this.index=0}}const Vo=new at;class Xa{constructor(e,t,i=0,r=1/0){this.ray=new Ba(e,t),this.near=i,this.far=r,this.camera=null,this.layers=new Va,this.params={Mesh:{},Line:{threshold:1},LOD:{},Points:{threshold:1},Sprite:{}}}set(e,t){this.ray.set(e,t)}setFromCamera(e,t){t.isPerspectiveCamera?(this.ray.origin.setFromMatrixPosition(t.matrixWorld),this.ray.direction.set(e.x,e.y,.5).unproject(t).sub(this.ray.origin).normalize(),this.camera=t):t.isOrthographicCamera?(this.ray.origin.set(e.x,e.y,(t.near+t.far)/(t.near-t.far)).unproject(t),this.ray.direction.set(0,0,-1).transformDirection(t.matrixWorld),this.camera=t):console.error("THREE.Raycaster: Unsupported camera type: "+t.type)}setFromXRController(e){return Vo.identity().extractRotation(e.matrixWorld),this.ray.origin.setFromMatrixPosition(e.matrixWorld),this.ray.direction.set(0,0,-1).applyMatrix4(Vo),this}intersectObject(e,t=!0,i=[]){return ba(e,this,i,t),i.sort(Ho),i}intersectObjects(e,t=!0,i=[]){for(let r=0,s=e.length;r<s;r++)ba(e[r],this,i,t);return i.sort(Ho),i}}function Ho(n,e){return n.distance-e.distance}function ba(n,e,t,i){let r=!0;if(n.layers.test(e.layers)&&n.raycast(e,t)===!1&&(r=!1),r===!0&&i===!0){const s=n.children;for(let a=0,o=s.length;a<o;a++)ba(s[a],e,t,!0)}}function Go(n,e,t,i){const r=ju(i);switch(t){case Ic:return n*e;case zc:return n*e;case Nc:return n*e*2;case Fc:return n*e/r.components*r.byteLength;case Na:return n*e/r.components*r.byteLength;case kc:return n*e*2/r.components*r.byteLength;case Fa:return n*e*2/r.components*r.byteLength;case Uc:return n*e*3/r.components*r.byteLength;case Gt:return n*e*4/r.components*r.byteLength;case ka:return n*e*4/r.components*r.byteLength;case zr:case Nr:return Math.floor((n+3)/4)*Math.floor((e+3)/4)*8;case Fr:case kr:return Math.floor((n+3)/4)*Math.floor((e+3)/4)*16;case Js:case ea:return Math.max(n,16)*Math.max(e,8)/4;case Zs:case Qs:return Math.max(n,8)*Math.max(e,8)/2;case ta:case na:return Math.floor((n+3)/4)*Math.floor((e+3)/4)*8;case ia:return Math.floor((n+3)/4)*Math.floor((e+3)/4)*16;case ra:return Math.floor((n+3)/4)*Math.floor((e+3)/4)*16;case sa:return Math.floor((n+4)/5)*Math.floor((e+3)/4)*16;case aa:return Math.floor((n+4)/5)*Math.floor((e+4)/5)*16;case oa:return Math.floor((n+5)/6)*Math.floor((e+4)/5)*16;case ca:return Math.floor((n+5)/6)*Math.floor((e+5)/6)*16;case la:return Math.floor((n+7)/8)*Math.floor((e+4)/5)*16;case ua:return Math.floor((n+7)/8)*Math.floor((e+5)/6)*16;case da:return Math.floor((n+7)/8)*Math.floor((e+7)/8)*16;case ha:return Math.floor((n+9)/10)*Math.floor((e+4)/5)*16;case fa:return Math.floor((n+9)/10)*Math.floor((e+5)/6)*16;case pa:return Math.floor((n+9)/10)*Math.floor((e+7)/8)*16;case ma:return Math.floor((n+9)/10)*Math.floor((e+9)/10)*16;case ga:return Math.floor((n+11)/12)*Math.floor((e+9)/10)*16;case _a:return Math.floor((n+11)/12)*Math.floor((e+11)/12)*16;case Or:case va:case xa:return Math.ceil(n/4)*Math.ceil(e/4)*16;case Oc:case Ma:return Math.ceil(n/4)*Math.ceil(e/4)*8;case Sa:case Ea:return Math.ceil(n/4)*Math.ceil(e/4)*16}throw new Error(`Unable to determine texture byte length for ${t} format.`)}function ju(n){switch(n){case pn:case Pc:return{byteLength:1,components:1};case Zi:case Dc:case nr:return{byteLength:2,components:1};case Ua:case za:return{byteLength:2,components:4};case Qn:case Ia:case dn:return{byteLength:4,components:1};case Lc:return{byteLength:4,components:3}}throw new Error(`Unknown texture type ${n}.`)}typeof __THREE_DEVTOOLS__<"u"&&__THREE_DEVTOOLS__.dispatchEvent(new CustomEvent("register",{detail:{revision:La}}));typeof window<"u"&&(window.__THREE__?console.warn("WARNING: Multiple instances of Three.js being imported."):window.__THREE__=La);/**
 * @license
 * Copyright 2010-2025 Three.js Authors
 * SPDX-License-Identifier: MIT
 */function el(){let n=null,e=!1,t=null,i=null;function r(s,a){t(s,a),i=n.requestAnimationFrame(r)}return{start:function(){e!==!0&&t!==null&&(i=n.requestAnimationFrame(r),e=!0)},stop:function(){n.cancelAnimationFrame(i),e=!1},setAnimationLoop:function(s){t=s},setContext:function(s){n=s}}}function Wu(n){const e=new WeakMap;function t(o,c){const l=o.array,d=o.usage,h=l.byteLength,f=n.createBuffer();n.bindBuffer(c,f),n.bufferData(c,l,d),o.onUploadCallback();let m;if(l instanceof Float32Array)m=n.FLOAT;else if(l instanceof Uint16Array)o.isFloat16BufferAttribute?m=n.HALF_FLOAT:m=n.UNSIGNED_SHORT;else if(l instanceof Int16Array)m=n.SHORT;else if(l instanceof Uint32Array)m=n.UNSIGNED_INT;else if(l instanceof Int32Array)m=n.INT;else if(l instanceof Int8Array)m=n.BYTE;else if(l instanceof Uint8Array)m=n.UNSIGNED_BYTE;else if(l instanceof Uint8ClampedArray)m=n.UNSIGNED_BYTE;else throw new Error("THREE.WebGLAttributes: Unsupported buffer data format: "+l);return{buffer:f,type:m,bytesPerElement:l.BYTES_PER_ELEMENT,version:o.version,size:h}}function i(o,c,l){const d=c.array,h=c.updateRanges;if(n.bindBuffer(l,o),h.length===0)n.bufferSubData(l,0,d);else{h.sort((m,g)=>m.start-g.start);let f=0;for(let m=1;m<h.length;m++){const g=h[f],_=h[m];_.start<=g.start+g.count+1?g.count=Math.max(g.count,_.start+_.count-g.start):(++f,h[f]=_)}h.length=f+1;for(let m=0,g=h.length;m<g;m++){const _=h[m];n.bufferSubData(l,_.start*d.BYTES_PER_ELEMENT,d,_.start,_.count)}c.clearUpdateRanges()}c.onUploadCallback()}function r(o){return o.isInterleavedBufferAttribute&&(o=o.data),e.get(o)}function s(o){o.isInterleavedBufferAttribute&&(o=o.data);const c=e.get(o);c&&(n.deleteBuffer(c.buffer),e.delete(o))}function a(o,c){if(o.isInterleavedBufferAttribute&&(o=o.data),o.isGLBufferAttribute){const d=e.get(o);(!d||d.version<o.version)&&e.set(o,{buffer:o.buffer,type:o.type,bytesPerElement:o.elementSize,version:o.version});return}const l=e.get(o);if(l===void 0)e.set(o,t(o,c));else if(l.version<o.version){if(l.size!==o.array.byteLength)throw new Error("THREE.WebGLAttributes: The size of the buffer attribute's array buffer does not match the original size. Resizing buffer attributes is not supported.");i(l.buffer,o,c),l.version=o.version}}return{get:r,remove:s,update:a}}var Xu=`#ifdef USE_ALPHAHASH
	if ( diffuseColor.a < getAlphaHashThreshold( vPosition ) ) discard;
#endif`,qu=`#ifdef USE_ALPHAHASH
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
#endif`,Ku=`#ifdef USE_ALPHAMAP
	diffuseColor.a *= texture2D( alphaMap, vAlphaMapUv ).g;
#endif`,Yu=`#ifdef USE_ALPHAMAP
	uniform sampler2D alphaMap;
#endif`,$u=`#ifdef USE_ALPHATEST
	#ifdef ALPHA_TO_COVERAGE
	diffuseColor.a = smoothstep( alphaTest, alphaTest + fwidth( diffuseColor.a ), diffuseColor.a );
	if ( diffuseColor.a == 0.0 ) discard;
	#else
	if ( diffuseColor.a < alphaTest ) discard;
	#endif
#endif`,Zu=`#ifdef USE_ALPHATEST
	uniform float alphaTest;
#endif`,Ju=`#ifdef USE_AOMAP
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
#endif`,Qu=`#ifdef USE_AOMAP
	uniform sampler2D aoMap;
	uniform float aoMapIntensity;
#endif`,ed=`#ifdef USE_BATCHING
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
#endif`,td=`#ifdef USE_BATCHING
	mat4 batchingMatrix = getBatchingMatrix( getIndirectIndex( gl_DrawID ) );
#endif`,nd=`vec3 transformed = vec3( position );
#ifdef USE_ALPHAHASH
	vPosition = vec3( position );
#endif`,id=`vec3 objectNormal = vec3( normal );
#ifdef USE_TANGENT
	vec3 objectTangent = vec3( tangent.xyz );
#endif`,rd=`float G_BlinnPhong_Implicit( ) {
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
} // validated`,sd=`#ifdef USE_IRIDESCENCE
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
#endif`,ad=`#ifdef USE_BUMPMAP
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
#endif`,od=`#if NUM_CLIPPING_PLANES > 0
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
#endif`,cd=`#if NUM_CLIPPING_PLANES > 0
	varying vec3 vClipPosition;
	uniform vec4 clippingPlanes[ NUM_CLIPPING_PLANES ];
#endif`,ld=`#if NUM_CLIPPING_PLANES > 0
	varying vec3 vClipPosition;
#endif`,ud=`#if NUM_CLIPPING_PLANES > 0
	vClipPosition = - mvPosition.xyz;
#endif`,dd=`#if defined( USE_COLOR_ALPHA )
	diffuseColor *= vColor;
#elif defined( USE_COLOR )
	diffuseColor.rgb *= vColor;
#endif`,hd=`#if defined( USE_COLOR_ALPHA )
	varying vec4 vColor;
#elif defined( USE_COLOR )
	varying vec3 vColor;
#endif`,fd=`#if defined( USE_COLOR_ALPHA )
	varying vec4 vColor;
#elif defined( USE_COLOR ) || defined( USE_INSTANCING_COLOR ) || defined( USE_BATCHING_COLOR )
	varying vec3 vColor;
#endif`,pd=`#if defined( USE_COLOR_ALPHA )
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
#endif`,md=`#define PI 3.141592653589793
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
} // validated`,gd=`#ifdef ENVMAP_TYPE_CUBE_UV
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
#endif`,_d=`vec3 transformedNormal = objectNormal;
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
#endif`,vd=`#ifdef USE_DISPLACEMENTMAP
	uniform sampler2D displacementMap;
	uniform float displacementScale;
	uniform float displacementBias;
#endif`,xd=`#ifdef USE_DISPLACEMENTMAP
	transformed += normalize( objectNormal ) * ( texture2D( displacementMap, vDisplacementMapUv ).x * displacementScale + displacementBias );
#endif`,Md=`#ifdef USE_EMISSIVEMAP
	vec4 emissiveColor = texture2D( emissiveMap, vEmissiveMapUv );
	#ifdef DECODE_VIDEO_TEXTURE_EMISSIVE
		emissiveColor = sRGBTransferEOTF( emissiveColor );
	#endif
	totalEmissiveRadiance *= emissiveColor.rgb;
#endif`,Sd=`#ifdef USE_EMISSIVEMAP
	uniform sampler2D emissiveMap;
#endif`,Ed="gl_FragColor = linearToOutputTexel( gl_FragColor );",yd=`vec4 LinearTransferOETF( in vec4 value ) {
	return value;
}
vec4 sRGBTransferEOTF( in vec4 value ) {
	return vec4( mix( pow( value.rgb * 0.9478672986 + vec3( 0.0521327014 ), vec3( 2.4 ) ), value.rgb * 0.0773993808, vec3( lessThanEqual( value.rgb, vec3( 0.04045 ) ) ) ), value.a );
}
vec4 sRGBTransferOETF( in vec4 value ) {
	return vec4( mix( pow( value.rgb, vec3( 0.41666 ) ) * 1.055 - vec3( 0.055 ), value.rgb * 12.92, vec3( lessThanEqual( value.rgb, vec3( 0.0031308 ) ) ) ), value.a );
}`,bd=`#ifdef USE_ENVMAP
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
#endif`,Td=`#ifdef USE_ENVMAP
	uniform float envMapIntensity;
	uniform float flipEnvMap;
	uniform mat3 envMapRotation;
	#ifdef ENVMAP_TYPE_CUBE
		uniform samplerCube envMap;
	#else
		uniform sampler2D envMap;
	#endif
	
#endif`,Ad=`#ifdef USE_ENVMAP
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
#endif`,wd=`#ifdef USE_ENVMAP
	#if defined( USE_BUMPMAP ) || defined( USE_NORMALMAP ) || defined( PHONG ) || defined( LAMBERT )
		#define ENV_WORLDPOS
	#endif
	#ifdef ENV_WORLDPOS
		
		varying vec3 vWorldPosition;
	#else
		varying vec3 vReflect;
		uniform float refractionRatio;
	#endif
#endif`,Rd=`#ifdef USE_ENVMAP
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
#endif`,Cd=`#ifdef USE_FOG
	vFogDepth = - mvPosition.z;
#endif`,Pd=`#ifdef USE_FOG
	varying float vFogDepth;
#endif`,Dd=`#ifdef USE_FOG
	#ifdef FOG_EXP2
		float fogFactor = 1.0 - exp( - fogDensity * fogDensity * vFogDepth * vFogDepth );
	#else
		float fogFactor = smoothstep( fogNear, fogFar, vFogDepth );
	#endif
	gl_FragColor.rgb = mix( gl_FragColor.rgb, fogColor, fogFactor );
#endif`,Ld=`#ifdef USE_FOG
	uniform vec3 fogColor;
	varying float vFogDepth;
	#ifdef FOG_EXP2
		uniform float fogDensity;
	#else
		uniform float fogNear;
		uniform float fogFar;
	#endif
#endif`,Id=`#ifdef USE_GRADIENTMAP
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
}`,Ud=`#ifdef USE_LIGHTMAP
	uniform sampler2D lightMap;
	uniform float lightMapIntensity;
#endif`,zd=`LambertMaterial material;
material.diffuseColor = diffuseColor.rgb;
material.specularStrength = specularStrength;`,Nd=`varying vec3 vViewPosition;
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
#define RE_IndirectDiffuse		RE_IndirectDiffuse_Lambert`,Fd=`uniform bool receiveShadow;
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
#endif`,kd=`#ifdef USE_ENVMAP
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
#endif`,Od=`ToonMaterial material;
material.diffuseColor = diffuseColor.rgb;`,Bd=`varying vec3 vViewPosition;
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
#define RE_IndirectDiffuse		RE_IndirectDiffuse_Toon`,Vd=`BlinnPhongMaterial material;
material.diffuseColor = diffuseColor.rgb;
material.specularColor = specular;
material.specularShininess = shininess;
material.specularStrength = specularStrength;`,Hd=`varying vec3 vViewPosition;
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
#define RE_IndirectDiffuse		RE_IndirectDiffuse_BlinnPhong`,Gd=`PhysicalMaterial material;
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
#endif`,jd=`struct PhysicalMaterial {
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
}`,Wd=`
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
#endif`,Xd=`#if defined( RE_IndirectDiffuse )
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
#endif`,qd=`#if defined( RE_IndirectDiffuse )
	RE_IndirectDiffuse( irradiance, geometryPosition, geometryNormal, geometryViewDir, geometryClearcoatNormal, material, reflectedLight );
#endif
#if defined( RE_IndirectSpecular )
	RE_IndirectSpecular( radiance, iblIrradiance, clearcoatRadiance, geometryPosition, geometryNormal, geometryViewDir, geometryClearcoatNormal, material, reflectedLight );
#endif`,Kd=`#if defined( USE_LOGDEPTHBUF )
	gl_FragDepth = vIsPerspective == 0.0 ? gl_FragCoord.z : log2( vFragDepth ) * logDepthBufFC * 0.5;
#endif`,Yd=`#if defined( USE_LOGDEPTHBUF )
	uniform float logDepthBufFC;
	varying float vFragDepth;
	varying float vIsPerspective;
#endif`,$d=`#ifdef USE_LOGDEPTHBUF
	varying float vFragDepth;
	varying float vIsPerspective;
#endif`,Zd=`#ifdef USE_LOGDEPTHBUF
	vFragDepth = 1.0 + gl_Position.w;
	vIsPerspective = float( isPerspectiveMatrix( projectionMatrix ) );
#endif`,Jd=`#ifdef USE_MAP
	vec4 sampledDiffuseColor = texture2D( map, vMapUv );
	#ifdef DECODE_VIDEO_TEXTURE
		sampledDiffuseColor = sRGBTransferEOTF( sampledDiffuseColor );
	#endif
	diffuseColor *= sampledDiffuseColor;
#endif`,Qd=`#ifdef USE_MAP
	uniform sampler2D map;
#endif`,eh=`#if defined( USE_MAP ) || defined( USE_ALPHAMAP )
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
#endif`,th=`#if defined( USE_POINTS_UV )
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
#endif`,nh=`float metalnessFactor = metalness;
#ifdef USE_METALNESSMAP
	vec4 texelMetalness = texture2D( metalnessMap, vMetalnessMapUv );
	metalnessFactor *= texelMetalness.b;
#endif`,ih=`#ifdef USE_METALNESSMAP
	uniform sampler2D metalnessMap;
#endif`,rh=`#ifdef USE_INSTANCING_MORPH
	float morphTargetInfluences[ MORPHTARGETS_COUNT ];
	float morphTargetBaseInfluence = texelFetch( morphTexture, ivec2( 0, gl_InstanceID ), 0 ).r;
	for ( int i = 0; i < MORPHTARGETS_COUNT; i ++ ) {
		morphTargetInfluences[i] =  texelFetch( morphTexture, ivec2( i + 1, gl_InstanceID ), 0 ).r;
	}
#endif`,sh=`#if defined( USE_MORPHCOLORS )
	vColor *= morphTargetBaseInfluence;
	for ( int i = 0; i < MORPHTARGETS_COUNT; i ++ ) {
		#if defined( USE_COLOR_ALPHA )
			if ( morphTargetInfluences[ i ] != 0.0 ) vColor += getMorph( gl_VertexID, i, 2 ) * morphTargetInfluences[ i ];
		#elif defined( USE_COLOR )
			if ( morphTargetInfluences[ i ] != 0.0 ) vColor += getMorph( gl_VertexID, i, 2 ).rgb * morphTargetInfluences[ i ];
		#endif
	}
#endif`,ah=`#ifdef USE_MORPHNORMALS
	objectNormal *= morphTargetBaseInfluence;
	for ( int i = 0; i < MORPHTARGETS_COUNT; i ++ ) {
		if ( morphTargetInfluences[ i ] != 0.0 ) objectNormal += getMorph( gl_VertexID, i, 1 ).xyz * morphTargetInfluences[ i ];
	}
#endif`,oh=`#ifdef USE_MORPHTARGETS
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
#endif`,ch=`#ifdef USE_MORPHTARGETS
	transformed *= morphTargetBaseInfluence;
	for ( int i = 0; i < MORPHTARGETS_COUNT; i ++ ) {
		if ( morphTargetInfluences[ i ] != 0.0 ) transformed += getMorph( gl_VertexID, i, 0 ).xyz * morphTargetInfluences[ i ];
	}
#endif`,lh=`float faceDirection = gl_FrontFacing ? 1.0 : - 1.0;
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
vec3 nonPerturbedNormal = normal;`,uh=`#ifdef USE_NORMALMAP_OBJECTSPACE
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
#endif`,dh=`#ifndef FLAT_SHADED
	varying vec3 vNormal;
	#ifdef USE_TANGENT
		varying vec3 vTangent;
		varying vec3 vBitangent;
	#endif
#endif`,hh=`#ifndef FLAT_SHADED
	varying vec3 vNormal;
	#ifdef USE_TANGENT
		varying vec3 vTangent;
		varying vec3 vBitangent;
	#endif
#endif`,fh=`#ifndef FLAT_SHADED
	vNormal = normalize( transformedNormal );
	#ifdef USE_TANGENT
		vTangent = normalize( transformedTangent );
		vBitangent = normalize( cross( vNormal, vTangent ) * tangent.w );
	#endif
#endif`,ph=`#ifdef USE_NORMALMAP
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
#endif`,mh=`#ifdef USE_CLEARCOAT
	vec3 clearcoatNormal = nonPerturbedNormal;
#endif`,gh=`#ifdef USE_CLEARCOAT_NORMALMAP
	vec3 clearcoatMapN = texture2D( clearcoatNormalMap, vClearcoatNormalMapUv ).xyz * 2.0 - 1.0;
	clearcoatMapN.xy *= clearcoatNormalScale;
	clearcoatNormal = normalize( tbn2 * clearcoatMapN );
#endif`,_h=`#ifdef USE_CLEARCOATMAP
	uniform sampler2D clearcoatMap;
#endif
#ifdef USE_CLEARCOAT_NORMALMAP
	uniform sampler2D clearcoatNormalMap;
	uniform vec2 clearcoatNormalScale;
#endif
#ifdef USE_CLEARCOAT_ROUGHNESSMAP
	uniform sampler2D clearcoatRoughnessMap;
#endif`,vh=`#ifdef USE_IRIDESCENCEMAP
	uniform sampler2D iridescenceMap;
#endif
#ifdef USE_IRIDESCENCE_THICKNESSMAP
	uniform sampler2D iridescenceThicknessMap;
#endif`,xh=`#ifdef OPAQUE
diffuseColor.a = 1.0;
#endif
#ifdef USE_TRANSMISSION
diffuseColor.a *= material.transmissionAlpha;
#endif
gl_FragColor = vec4( outgoingLight, diffuseColor.a );`,Mh=`vec3 packNormalToRGB( const in vec3 normal ) {
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
}`,Sh=`#ifdef PREMULTIPLIED_ALPHA
	gl_FragColor.rgb *= gl_FragColor.a;
#endif`,Eh=`vec4 mvPosition = vec4( transformed, 1.0 );
#ifdef USE_BATCHING
	mvPosition = batchingMatrix * mvPosition;
#endif
#ifdef USE_INSTANCING
	mvPosition = instanceMatrix * mvPosition;
#endif
mvPosition = modelViewMatrix * mvPosition;
gl_Position = projectionMatrix * mvPosition;`,yh=`#ifdef DITHERING
	gl_FragColor.rgb = dithering( gl_FragColor.rgb );
#endif`,bh=`#ifdef DITHERING
	vec3 dithering( vec3 color ) {
		float grid_position = rand( gl_FragCoord.xy );
		vec3 dither_shift_RGB = vec3( 0.25 / 255.0, -0.25 / 255.0, 0.25 / 255.0 );
		dither_shift_RGB = mix( 2.0 * dither_shift_RGB, -2.0 * dither_shift_RGB, grid_position );
		return color + dither_shift_RGB;
	}
#endif`,Th=`float roughnessFactor = roughness;
#ifdef USE_ROUGHNESSMAP
	vec4 texelRoughness = texture2D( roughnessMap, vRoughnessMapUv );
	roughnessFactor *= texelRoughness.g;
#endif`,Ah=`#ifdef USE_ROUGHNESSMAP
	uniform sampler2D roughnessMap;
#endif`,wh=`#if NUM_SPOT_LIGHT_COORDS > 0
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
#endif`,Rh=`#if NUM_SPOT_LIGHT_COORDS > 0
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
#endif`,Ch=`#if ( defined( USE_SHADOWMAP ) && ( NUM_DIR_LIGHT_SHADOWS > 0 || NUM_POINT_LIGHT_SHADOWS > 0 ) ) || ( NUM_SPOT_LIGHT_COORDS > 0 )
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
#endif`,Ph=`float getShadowMask() {
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
}`,Dh=`#ifdef USE_SKINNING
	mat4 boneMatX = getBoneMatrix( skinIndex.x );
	mat4 boneMatY = getBoneMatrix( skinIndex.y );
	mat4 boneMatZ = getBoneMatrix( skinIndex.z );
	mat4 boneMatW = getBoneMatrix( skinIndex.w );
#endif`,Lh=`#ifdef USE_SKINNING
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
#endif`,Ih=`#ifdef USE_SKINNING
	vec4 skinVertex = bindMatrix * vec4( transformed, 1.0 );
	vec4 skinned = vec4( 0.0 );
	skinned += boneMatX * skinVertex * skinWeight.x;
	skinned += boneMatY * skinVertex * skinWeight.y;
	skinned += boneMatZ * skinVertex * skinWeight.z;
	skinned += boneMatW * skinVertex * skinWeight.w;
	transformed = ( bindMatrixInverse * skinned ).xyz;
#endif`,Uh=`#ifdef USE_SKINNING
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
#endif`,zh=`float specularStrength;
#ifdef USE_SPECULARMAP
	vec4 texelSpecular = texture2D( specularMap, vSpecularMapUv );
	specularStrength = texelSpecular.r;
#else
	specularStrength = 1.0;
#endif`,Nh=`#ifdef USE_SPECULARMAP
	uniform sampler2D specularMap;
#endif`,Fh=`#if defined( TONE_MAPPING )
	gl_FragColor.rgb = toneMapping( gl_FragColor.rgb );
#endif`,kh=`#ifndef saturate
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
vec3 CustomToneMapping( vec3 color ) { return color; }`,Oh=`#ifdef USE_TRANSMISSION
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
#endif`,Bh=`#ifdef USE_TRANSMISSION
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
#endif`,Vh=`#if defined( USE_UV ) || defined( USE_ANISOTROPY )
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
#endif`,Hh=`#if defined( USE_UV ) || defined( USE_ANISOTROPY )
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
#endif`,Gh=`#if defined( USE_UV ) || defined( USE_ANISOTROPY )
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
#endif`,jh=`#if defined( USE_ENVMAP ) || defined( DISTANCE ) || defined ( USE_SHADOWMAP ) || defined ( USE_TRANSMISSION ) || NUM_SPOT_LIGHT_COORDS > 0
	vec4 worldPosition = vec4( transformed, 1.0 );
	#ifdef USE_BATCHING
		worldPosition = batchingMatrix * worldPosition;
	#endif
	#ifdef USE_INSTANCING
		worldPosition = instanceMatrix * worldPosition;
	#endif
	worldPosition = modelMatrix * worldPosition;
#endif`;const Wh=`varying vec2 vUv;
uniform mat3 uvTransform;
void main() {
	vUv = ( uvTransform * vec3( uv, 1 ) ).xy;
	gl_Position = vec4( position.xy, 1.0, 1.0 );
}`,Xh=`uniform sampler2D t2D;
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
}`,qh=`varying vec3 vWorldDirection;
#include <common>
void main() {
	vWorldDirection = transformDirection( position, modelMatrix );
	#include <begin_vertex>
	#include <project_vertex>
	gl_Position.z = gl_Position.w;
}`,Kh=`#ifdef ENVMAP_TYPE_CUBE
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
}`,Yh=`varying vec3 vWorldDirection;
#include <common>
void main() {
	vWorldDirection = transformDirection( position, modelMatrix );
	#include <begin_vertex>
	#include <project_vertex>
	gl_Position.z = gl_Position.w;
}`,$h=`uniform samplerCube tCube;
uniform float tFlip;
uniform float opacity;
varying vec3 vWorldDirection;
void main() {
	vec4 texColor = textureCube( tCube, vec3( tFlip * vWorldDirection.x, vWorldDirection.yz ) );
	gl_FragColor = texColor;
	gl_FragColor.a *= opacity;
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
}`,Zh=`#include <common>
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
}`,Jh=`#if DEPTH_PACKING == 3200
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
}`,Qh=`#define DISTANCE
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
}`,ef=`#define DISTANCE
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
}`,tf=`varying vec3 vWorldDirection;
#include <common>
void main() {
	vWorldDirection = transformDirection( position, modelMatrix );
	#include <begin_vertex>
	#include <project_vertex>
}`,nf=`uniform sampler2D tEquirect;
varying vec3 vWorldDirection;
#include <common>
void main() {
	vec3 direction = normalize( vWorldDirection );
	vec2 sampleUV = equirectUv( direction );
	gl_FragColor = texture2D( tEquirect, sampleUV );
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
}`,rf=`uniform float scale;
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
}`,sf=`uniform vec3 diffuse;
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
}`,af=`#include <common>
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
}`,of=`uniform vec3 diffuse;
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
}`,cf=`#define LAMBERT
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
}`,lf=`#define LAMBERT
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
}`,uf=`#define MATCAP
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
}`,df=`#define MATCAP
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
}`,hf=`#define NORMAL
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
}`,ff=`#define NORMAL
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
}`,pf=`#define PHONG
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
}`,mf=`#define PHONG
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
}`,gf=`#define STANDARD
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
}`,_f=`#define STANDARD
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
}`,vf=`#define TOON
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
}`,xf=`#define TOON
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
}`,Mf=`uniform float size;
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
}`,Sf=`uniform vec3 diffuse;
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
}`,Ef=`#include <common>
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
}`,yf=`uniform vec3 color;
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
}`,bf=`uniform float rotation;
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
}`,Tf=`uniform vec3 diffuse;
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
}`,Ge={alphahash_fragment:Xu,alphahash_pars_fragment:qu,alphamap_fragment:Ku,alphamap_pars_fragment:Yu,alphatest_fragment:$u,alphatest_pars_fragment:Zu,aomap_fragment:Ju,aomap_pars_fragment:Qu,batching_pars_vertex:ed,batching_vertex:td,begin_vertex:nd,beginnormal_vertex:id,bsdfs:rd,iridescence_fragment:sd,bumpmap_pars_fragment:ad,clipping_planes_fragment:od,clipping_planes_pars_fragment:cd,clipping_planes_pars_vertex:ld,clipping_planes_vertex:ud,color_fragment:dd,color_pars_fragment:hd,color_pars_vertex:fd,color_vertex:pd,common:md,cube_uv_reflection_fragment:gd,defaultnormal_vertex:_d,displacementmap_pars_vertex:vd,displacementmap_vertex:xd,emissivemap_fragment:Md,emissivemap_pars_fragment:Sd,colorspace_fragment:Ed,colorspace_pars_fragment:yd,envmap_fragment:bd,envmap_common_pars_fragment:Td,envmap_pars_fragment:Ad,envmap_pars_vertex:wd,envmap_physical_pars_fragment:kd,envmap_vertex:Rd,fog_vertex:Cd,fog_pars_vertex:Pd,fog_fragment:Dd,fog_pars_fragment:Ld,gradientmap_pars_fragment:Id,lightmap_pars_fragment:Ud,lights_lambert_fragment:zd,lights_lambert_pars_fragment:Nd,lights_pars_begin:Fd,lights_toon_fragment:Od,lights_toon_pars_fragment:Bd,lights_phong_fragment:Vd,lights_phong_pars_fragment:Hd,lights_physical_fragment:Gd,lights_physical_pars_fragment:jd,lights_fragment_begin:Wd,lights_fragment_maps:Xd,lights_fragment_end:qd,logdepthbuf_fragment:Kd,logdepthbuf_pars_fragment:Yd,logdepthbuf_pars_vertex:$d,logdepthbuf_vertex:Zd,map_fragment:Jd,map_pars_fragment:Qd,map_particle_fragment:eh,map_particle_pars_fragment:th,metalnessmap_fragment:nh,metalnessmap_pars_fragment:ih,morphinstance_vertex:rh,morphcolor_vertex:sh,morphnormal_vertex:ah,morphtarget_pars_vertex:oh,morphtarget_vertex:ch,normal_fragment_begin:lh,normal_fragment_maps:uh,normal_pars_fragment:dh,normal_pars_vertex:hh,normal_vertex:fh,normalmap_pars_fragment:ph,clearcoat_normal_fragment_begin:mh,clearcoat_normal_fragment_maps:gh,clearcoat_pars_fragment:_h,iridescence_pars_fragment:vh,opaque_fragment:xh,packing:Mh,premultiplied_alpha_fragment:Sh,project_vertex:Eh,dithering_fragment:yh,dithering_pars_fragment:bh,roughnessmap_fragment:Th,roughnessmap_pars_fragment:Ah,shadowmap_pars_fragment:wh,shadowmap_pars_vertex:Rh,shadowmap_vertex:Ch,shadowmask_pars_fragment:Ph,skinbase_vertex:Dh,skinning_pars_vertex:Lh,skinning_vertex:Ih,skinnormal_vertex:Uh,specularmap_fragment:zh,specularmap_pars_fragment:Nh,tonemapping_fragment:Fh,tonemapping_pars_fragment:kh,transmission_fragment:Oh,transmission_pars_fragment:Bh,uv_pars_fragment:Vh,uv_pars_vertex:Hh,uv_vertex:Gh,worldpos_vertex:jh,background_vert:Wh,background_frag:Xh,backgroundCube_vert:qh,backgroundCube_frag:Kh,cube_vert:Yh,cube_frag:$h,depth_vert:Zh,depth_frag:Jh,distanceRGBA_vert:Qh,distanceRGBA_frag:ef,equirect_vert:tf,equirect_frag:nf,linedashed_vert:rf,linedashed_frag:sf,meshbasic_vert:af,meshbasic_frag:of,meshlambert_vert:cf,meshlambert_frag:lf,meshmatcap_vert:uf,meshmatcap_frag:df,meshnormal_vert:hf,meshnormal_frag:ff,meshphong_vert:pf,meshphong_frag:mf,meshphysical_vert:gf,meshphysical_frag:_f,meshtoon_vert:vf,meshtoon_frag:xf,points_vert:Mf,points_frag:Sf,shadow_vert:Ef,shadow_frag:yf,sprite_vert:bf,sprite_frag:Tf},de={common:{diffuse:{value:new oe(16777215)},opacity:{value:1},map:{value:null},mapTransform:{value:new Ve},alphaMap:{value:null},alphaMapTransform:{value:new Ve},alphaTest:{value:0}},specularmap:{specularMap:{value:null},specularMapTransform:{value:new Ve}},envmap:{envMap:{value:null},envMapRotation:{value:new Ve},flipEnvMap:{value:-1},reflectivity:{value:1},ior:{value:1.5},refractionRatio:{value:.98}},aomap:{aoMap:{value:null},aoMapIntensity:{value:1},aoMapTransform:{value:new Ve}},lightmap:{lightMap:{value:null},lightMapIntensity:{value:1},lightMapTransform:{value:new Ve}},bumpmap:{bumpMap:{value:null},bumpMapTransform:{value:new Ve},bumpScale:{value:1}},normalmap:{normalMap:{value:null},normalMapTransform:{value:new Ve},normalScale:{value:new We(1,1)}},displacementmap:{displacementMap:{value:null},displacementMapTransform:{value:new Ve},displacementScale:{value:1},displacementBias:{value:0}},emissivemap:{emissiveMap:{value:null},emissiveMapTransform:{value:new Ve}},metalnessmap:{metalnessMap:{value:null},metalnessMapTransform:{value:new Ve}},roughnessmap:{roughnessMap:{value:null},roughnessMapTransform:{value:new Ve}},gradientmap:{gradientMap:{value:null}},fog:{fogDensity:{value:25e-5},fogNear:{value:1},fogFar:{value:2e3},fogColor:{value:new oe(16777215)}},lights:{ambientLightColor:{value:[]},lightProbe:{value:[]},directionalLights:{value:[],properties:{direction:{},color:{}}},directionalLightShadows:{value:[],properties:{shadowIntensity:1,shadowBias:{},shadowNormalBias:{},shadowRadius:{},shadowMapSize:{}}},directionalShadowMap:{value:[]},directionalShadowMatrix:{value:[]},spotLights:{value:[],properties:{color:{},position:{},direction:{},distance:{},coneCos:{},penumbraCos:{},decay:{}}},spotLightShadows:{value:[],properties:{shadowIntensity:1,shadowBias:{},shadowNormalBias:{},shadowRadius:{},shadowMapSize:{}}},spotLightMap:{value:[]},spotShadowMap:{value:[]},spotLightMatrix:{value:[]},pointLights:{value:[],properties:{color:{},position:{},decay:{},distance:{}}},pointLightShadows:{value:[],properties:{shadowIntensity:1,shadowBias:{},shadowNormalBias:{},shadowRadius:{},shadowMapSize:{},shadowCameraNear:{},shadowCameraFar:{}}},pointShadowMap:{value:[]},pointShadowMatrix:{value:[]},hemisphereLights:{value:[],properties:{direction:{},skyColor:{},groundColor:{}}},rectAreaLights:{value:[],properties:{color:{},position:{},width:{},height:{}}},ltc_1:{value:null},ltc_2:{value:null}},points:{diffuse:{value:new oe(16777215)},opacity:{value:1},size:{value:1},scale:{value:1},map:{value:null},alphaMap:{value:null},alphaMapTransform:{value:new Ve},alphaTest:{value:0},uvTransform:{value:new Ve}},sprite:{diffuse:{value:new oe(16777215)},opacity:{value:1},center:{value:new We(.5,.5)},rotation:{value:0},map:{value:null},mapTransform:{value:new Ve},alphaMap:{value:null},alphaMapTransform:{value:new Ve},alphaTest:{value:0}}},$t={basic:{uniforms:Rt([de.common,de.specularmap,de.envmap,de.aomap,de.lightmap,de.fog]),vertexShader:Ge.meshbasic_vert,fragmentShader:Ge.meshbasic_frag},lambert:{uniforms:Rt([de.common,de.specularmap,de.envmap,de.aomap,de.lightmap,de.emissivemap,de.bumpmap,de.normalmap,de.displacementmap,de.fog,de.lights,{emissive:{value:new oe(0)}}]),vertexShader:Ge.meshlambert_vert,fragmentShader:Ge.meshlambert_frag},phong:{uniforms:Rt([de.common,de.specularmap,de.envmap,de.aomap,de.lightmap,de.emissivemap,de.bumpmap,de.normalmap,de.displacementmap,de.fog,de.lights,{emissive:{value:new oe(0)},specular:{value:new oe(1118481)},shininess:{value:30}}]),vertexShader:Ge.meshphong_vert,fragmentShader:Ge.meshphong_frag},standard:{uniforms:Rt([de.common,de.envmap,de.aomap,de.lightmap,de.emissivemap,de.bumpmap,de.normalmap,de.displacementmap,de.roughnessmap,de.metalnessmap,de.fog,de.lights,{emissive:{value:new oe(0)},roughness:{value:1},metalness:{value:0},envMapIntensity:{value:1}}]),vertexShader:Ge.meshphysical_vert,fragmentShader:Ge.meshphysical_frag},toon:{uniforms:Rt([de.common,de.aomap,de.lightmap,de.emissivemap,de.bumpmap,de.normalmap,de.displacementmap,de.gradientmap,de.fog,de.lights,{emissive:{value:new oe(0)}}]),vertexShader:Ge.meshtoon_vert,fragmentShader:Ge.meshtoon_frag},matcap:{uniforms:Rt([de.common,de.bumpmap,de.normalmap,de.displacementmap,de.fog,{matcap:{value:null}}]),vertexShader:Ge.meshmatcap_vert,fragmentShader:Ge.meshmatcap_frag},points:{uniforms:Rt([de.points,de.fog]),vertexShader:Ge.points_vert,fragmentShader:Ge.points_frag},dashed:{uniforms:Rt([de.common,de.fog,{scale:{value:1},dashSize:{value:1},totalSize:{value:2}}]),vertexShader:Ge.linedashed_vert,fragmentShader:Ge.linedashed_frag},depth:{uniforms:Rt([de.common,de.displacementmap]),vertexShader:Ge.depth_vert,fragmentShader:Ge.depth_frag},normal:{uniforms:Rt([de.common,de.bumpmap,de.normalmap,de.displacementmap,{opacity:{value:1}}]),vertexShader:Ge.meshnormal_vert,fragmentShader:Ge.meshnormal_frag},sprite:{uniforms:Rt([de.sprite,de.fog]),vertexShader:Ge.sprite_vert,fragmentShader:Ge.sprite_frag},background:{uniforms:{uvTransform:{value:new Ve},t2D:{value:null},backgroundIntensity:{value:1}},vertexShader:Ge.background_vert,fragmentShader:Ge.background_frag},backgroundCube:{uniforms:{envMap:{value:null},flipEnvMap:{value:-1},backgroundBlurriness:{value:0},backgroundIntensity:{value:1},backgroundRotation:{value:new Ve}},vertexShader:Ge.backgroundCube_vert,fragmentShader:Ge.backgroundCube_frag},cube:{uniforms:{tCube:{value:null},tFlip:{value:-1},opacity:{value:1}},vertexShader:Ge.cube_vert,fragmentShader:Ge.cube_frag},equirect:{uniforms:{tEquirect:{value:null}},vertexShader:Ge.equirect_vert,fragmentShader:Ge.equirect_frag},distanceRGBA:{uniforms:Rt([de.common,de.displacementmap,{referencePosition:{value:new k},nearDistance:{value:1},farDistance:{value:1e3}}]),vertexShader:Ge.distanceRGBA_vert,fragmentShader:Ge.distanceRGBA_frag},shadow:{uniforms:Rt([de.lights,de.fog,{color:{value:new oe(0)},opacity:{value:1}}]),vertexShader:Ge.shadow_vert,fragmentShader:Ge.shadow_frag}};$t.physical={uniforms:Rt([$t.standard.uniforms,{clearcoat:{value:0},clearcoatMap:{value:null},clearcoatMapTransform:{value:new Ve},clearcoatNormalMap:{value:null},clearcoatNormalMapTransform:{value:new Ve},clearcoatNormalScale:{value:new We(1,1)},clearcoatRoughness:{value:0},clearcoatRoughnessMap:{value:null},clearcoatRoughnessMapTransform:{value:new Ve},dispersion:{value:0},iridescence:{value:0},iridescenceMap:{value:null},iridescenceMapTransform:{value:new Ve},iridescenceIOR:{value:1.3},iridescenceThicknessMinimum:{value:100},iridescenceThicknessMaximum:{value:400},iridescenceThicknessMap:{value:null},iridescenceThicknessMapTransform:{value:new Ve},sheen:{value:0},sheenColor:{value:new oe(0)},sheenColorMap:{value:null},sheenColorMapTransform:{value:new Ve},sheenRoughness:{value:1},sheenRoughnessMap:{value:null},sheenRoughnessMapTransform:{value:new Ve},transmission:{value:0},transmissionMap:{value:null},transmissionMapTransform:{value:new Ve},transmissionSamplerSize:{value:new We},transmissionSamplerMap:{value:null},thickness:{value:0},thicknessMap:{value:null},thicknessMapTransform:{value:new Ve},attenuationDistance:{value:0},attenuationColor:{value:new oe(0)},specularColor:{value:new oe(1,1,1)},specularColorMap:{value:null},specularColorMapTransform:{value:new Ve},specularIntensity:{value:1},specularIntensityMap:{value:null},specularIntensityMapTransform:{value:new Ve},anisotropyVector:{value:new We},anisotropyMap:{value:null},anisotropyMapTransform:{value:new Ve}}]),vertexShader:Ge.meshphysical_vert,fragmentShader:Ge.meshphysical_frag};const Dr={r:0,b:0,g:0},On=new xt,Af=new at;function wf(n,e,t,i,r,s,a){const o=new oe(0);let c=s===!0?0:1,l,d,h=null,f=0,m=null;function g(y){let M=y.isScene===!0?y.background:null;return M&&M.isTexture&&(M=(y.backgroundBlurriness>0?t:e).get(M)),M}function _(y){let M=!1;const D=g(y);D===null?u(o,c):D&&D.isColor&&(u(D,1),M=!0);const w=n.xr.getEnvironmentBlendMode();w==="additive"?i.buffers.color.setClear(0,0,0,1,a):w==="alpha-blend"&&i.buffers.color.setClear(0,0,0,0,a),(n.autoClear||M)&&(i.buffers.depth.setTest(!0),i.buffers.depth.setMask(!0),i.buffers.color.setMask(!0),n.clear(n.autoClearColor,n.autoClearDepth,n.autoClearStencil))}function p(y,M){const D=g(M);D&&(D.isCubeTexture||D.mapping===Kr)?(d===void 0&&(d=new Le(new Jt(1,1,1),new Dn({name:"BackgroundCubeMaterial",uniforms:Ui($t.backgroundCube.uniforms),vertexShader:$t.backgroundCube.vertexShader,fragmentShader:$t.backgroundCube.fragmentShader,side:Ct,depthTest:!1,depthWrite:!1,fog:!1})),d.geometry.deleteAttribute("normal"),d.geometry.deleteAttribute("uv"),d.onBeforeRender=function(w,b,C){this.matrixWorld.copyPosition(C.matrixWorld)},Object.defineProperty(d.material,"envMap",{get:function(){return this.uniforms.envMap.value}}),r.update(d)),On.copy(M.backgroundRotation),On.x*=-1,On.y*=-1,On.z*=-1,D.isCubeTexture&&D.isRenderTargetTexture===!1&&(On.y*=-1,On.z*=-1),d.material.uniforms.envMap.value=D,d.material.uniforms.flipEnvMap.value=D.isCubeTexture&&D.isRenderTargetTexture===!1?-1:1,d.material.uniforms.backgroundBlurriness.value=M.backgroundBlurriness,d.material.uniforms.backgroundIntensity.value=M.backgroundIntensity,d.material.uniforms.backgroundRotation.value.setFromMatrix4(Af.makeRotationFromEuler(On)),d.material.toneMapped=Je.getTransfer(D.colorSpace)!==it,(h!==D||f!==D.version||m!==n.toneMapping)&&(d.material.needsUpdate=!0,h=D,f=D.version,m=n.toneMapping),d.layers.enableAll(),y.unshift(d,d.geometry,d.material,0,0,null)):D&&D.isTexture&&(l===void 0&&(l=new Le(new ni(2,2),new Dn({name:"BackgroundMaterial",uniforms:Ui($t.background.uniforms),vertexShader:$t.background.vertexShader,fragmentShader:$t.background.fragmentShader,side:Pn,depthTest:!1,depthWrite:!1,fog:!1})),l.geometry.deleteAttribute("normal"),Object.defineProperty(l.material,"map",{get:function(){return this.uniforms.t2D.value}}),r.update(l)),l.material.uniforms.t2D.value=D,l.material.uniforms.backgroundIntensity.value=M.backgroundIntensity,l.material.toneMapped=Je.getTransfer(D.colorSpace)!==it,D.matrixAutoUpdate===!0&&D.updateMatrix(),l.material.uniforms.uvTransform.value.copy(D.matrix),(h!==D||f!==D.version||m!==n.toneMapping)&&(l.material.needsUpdate=!0,h=D,f=D.version,m=n.toneMapping),l.layers.enableAll(),y.unshift(l,l.geometry,l.material,0,0,null))}function u(y,M){y.getRGB(Dr,qc(n)),i.buffers.color.setClear(Dr.r,Dr.g,Dr.b,M,a)}function E(){d!==void 0&&(d.geometry.dispose(),d.material.dispose(),d=void 0),l!==void 0&&(l.geometry.dispose(),l.material.dispose(),l=void 0)}return{getClearColor:function(){return o},setClearColor:function(y,M=1){o.set(y),c=M,u(o,c)},getClearAlpha:function(){return c},setClearAlpha:function(y){c=y,u(o,c)},render:_,addToRenderList:p,dispose:E}}function Rf(n,e){const t=n.getParameter(n.MAX_VERTEX_ATTRIBS),i={},r=f(null);let s=r,a=!1;function o(x,P,U,A,R){let z=!1;const N=h(A,U,P);s!==N&&(s=N,l(s.object)),z=m(x,A,U,R),z&&g(x,A,U,R),R!==null&&e.update(R,n.ELEMENT_ARRAY_BUFFER),(z||a)&&(a=!1,M(x,P,U,A),R!==null&&n.bindBuffer(n.ELEMENT_ARRAY_BUFFER,e.get(R).buffer))}function c(){return n.createVertexArray()}function l(x){return n.bindVertexArray(x)}function d(x){return n.deleteVertexArray(x)}function h(x,P,U){const A=U.wireframe===!0;let R=i[x.id];R===void 0&&(R={},i[x.id]=R);let z=R[P.id];z===void 0&&(z={},R[P.id]=z);let N=z[A];return N===void 0&&(N=f(c()),z[A]=N),N}function f(x){const P=[],U=[],A=[];for(let R=0;R<t;R++)P[R]=0,U[R]=0,A[R]=0;return{geometry:null,program:null,wireframe:!1,newAttributes:P,enabledAttributes:U,attributeDivisors:A,object:x,attributes:{},index:null}}function m(x,P,U,A){const R=s.attributes,z=P.attributes;let N=0;const O=U.getAttributes();for(const F in O)if(O[F].location>=0){const Z=R[F];let Y=z[F];if(Y===void 0&&(F==="instanceMatrix"&&x.instanceMatrix&&(Y=x.instanceMatrix),F==="instanceColor"&&x.instanceColor&&(Y=x.instanceColor)),Z===void 0||Z.attribute!==Y||Y&&Z.data!==Y.data)return!0;N++}return s.attributesNum!==N||s.index!==A}function g(x,P,U,A){const R={},z=P.attributes;let N=0;const O=U.getAttributes();for(const F in O)if(O[F].location>=0){let Z=z[F];Z===void 0&&(F==="instanceMatrix"&&x.instanceMatrix&&(Z=x.instanceMatrix),F==="instanceColor"&&x.instanceColor&&(Z=x.instanceColor));const Y={};Y.attribute=Z,Z&&Z.data&&(Y.data=Z.data),R[F]=Y,N++}s.attributes=R,s.attributesNum=N,s.index=A}function _(){const x=s.newAttributes;for(let P=0,U=x.length;P<U;P++)x[P]=0}function p(x){u(x,0)}function u(x,P){const U=s.newAttributes,A=s.enabledAttributes,R=s.attributeDivisors;U[x]=1,A[x]===0&&(n.enableVertexAttribArray(x),A[x]=1),R[x]!==P&&(n.vertexAttribDivisor(x,P),R[x]=P)}function E(){const x=s.newAttributes,P=s.enabledAttributes;for(let U=0,A=P.length;U<A;U++)P[U]!==x[U]&&(n.disableVertexAttribArray(U),P[U]=0)}function y(x,P,U,A,R,z,N){N===!0?n.vertexAttribIPointer(x,P,U,R,z):n.vertexAttribPointer(x,P,U,A,R,z)}function M(x,P,U,A){_();const R=A.attributes,z=U.getAttributes(),N=P.defaultAttributeValues;for(const O in z){const F=z[O];if(F.location>=0){let G=R[O];if(G===void 0&&(O==="instanceMatrix"&&x.instanceMatrix&&(G=x.instanceMatrix),O==="instanceColor"&&x.instanceColor&&(G=x.instanceColor)),G!==void 0){const Z=G.normalized,Y=G.itemSize,he=e.get(G);if(he===void 0)continue;const Ie=he.buffer,X=he.type,ee=he.bytesPerElement,ue=X===n.INT||X===n.UNSIGNED_INT||G.gpuType===Ia;if(G.isInterleavedBufferAttribute){const re=G.data,le=re.stride,Pe=G.offset;if(re.isInstancedInterleavedBuffer){for(let me=0;me<F.locationSize;me++)u(F.location+me,re.meshPerAttribute);x.isInstancedMesh!==!0&&A._maxInstanceCount===void 0&&(A._maxInstanceCount=re.meshPerAttribute*re.count)}else for(let me=0;me<F.locationSize;me++)p(F.location+me);n.bindBuffer(n.ARRAY_BUFFER,Ie);for(let me=0;me<F.locationSize;me++)y(F.location+me,Y/F.locationSize,X,Z,le*ee,(Pe+Y/F.locationSize*me)*ee,ue)}else{if(G.isInstancedBufferAttribute){for(let re=0;re<F.locationSize;re++)u(F.location+re,G.meshPerAttribute);x.isInstancedMesh!==!0&&A._maxInstanceCount===void 0&&(A._maxInstanceCount=G.meshPerAttribute*G.count)}else for(let re=0;re<F.locationSize;re++)p(F.location+re);n.bindBuffer(n.ARRAY_BUFFER,Ie);for(let re=0;re<F.locationSize;re++)y(F.location+re,Y/F.locationSize,X,Z,Y*ee,Y/F.locationSize*re*ee,ue)}}else if(N!==void 0){const Z=N[O];if(Z!==void 0)switch(Z.length){case 2:n.vertexAttrib2fv(F.location,Z);break;case 3:n.vertexAttrib3fv(F.location,Z);break;case 4:n.vertexAttrib4fv(F.location,Z);break;default:n.vertexAttrib1fv(F.location,Z)}}}}E()}function D(){C();for(const x in i){const P=i[x];for(const U in P){const A=P[U];for(const R in A)d(A[R].object),delete A[R];delete P[U]}delete i[x]}}function w(x){if(i[x.id]===void 0)return;const P=i[x.id];for(const U in P){const A=P[U];for(const R in A)d(A[R].object),delete A[R];delete P[U]}delete i[x.id]}function b(x){for(const P in i){const U=i[P];if(U[x.id]===void 0)continue;const A=U[x.id];for(const R in A)d(A[R].object),delete A[R];delete U[x.id]}}function C(){v(),a=!0,s!==r&&(s=r,l(s.object))}function v(){r.geometry=null,r.program=null,r.wireframe=!1}return{setup:o,reset:C,resetDefaultState:v,dispose:D,releaseStatesOfGeometry:w,releaseStatesOfProgram:b,initAttributes:_,enableAttribute:p,disableUnusedAttributes:E}}function Cf(n,e,t){let i;function r(l){i=l}function s(l,d){n.drawArrays(i,l,d),t.update(d,i,1)}function a(l,d,h){h!==0&&(n.drawArraysInstanced(i,l,d,h),t.update(d,i,h))}function o(l,d,h){if(h===0)return;e.get("WEBGL_multi_draw").multiDrawArraysWEBGL(i,l,0,d,0,h);let m=0;for(let g=0;g<h;g++)m+=d[g];t.update(m,i,1)}function c(l,d,h,f){if(h===0)return;const m=e.get("WEBGL_multi_draw");if(m===null)for(let g=0;g<l.length;g++)a(l[g],d[g],f[g]);else{m.multiDrawArraysInstancedWEBGL(i,l,0,d,0,f,0,h);let g=0;for(let _=0;_<h;_++)g+=d[_]*f[_];t.update(g,i,1)}}this.setMode=r,this.render=s,this.renderInstances=a,this.renderMultiDraw=o,this.renderMultiDrawInstances=c}function Pf(n,e,t,i){let r;function s(){if(r!==void 0)return r;if(e.has("EXT_texture_filter_anisotropic")===!0){const b=e.get("EXT_texture_filter_anisotropic");r=n.getParameter(b.MAX_TEXTURE_MAX_ANISOTROPY_EXT)}else r=0;return r}function a(b){return!(b!==Gt&&i.convert(b)!==n.getParameter(n.IMPLEMENTATION_COLOR_READ_FORMAT))}function o(b){const C=b===nr&&(e.has("EXT_color_buffer_half_float")||e.has("EXT_color_buffer_float"));return!(b!==pn&&i.convert(b)!==n.getParameter(n.IMPLEMENTATION_COLOR_READ_TYPE)&&b!==dn&&!C)}function c(b){if(b==="highp"){if(n.getShaderPrecisionFormat(n.VERTEX_SHADER,n.HIGH_FLOAT).precision>0&&n.getShaderPrecisionFormat(n.FRAGMENT_SHADER,n.HIGH_FLOAT).precision>0)return"highp";b="mediump"}return b==="mediump"&&n.getShaderPrecisionFormat(n.VERTEX_SHADER,n.MEDIUM_FLOAT).precision>0&&n.getShaderPrecisionFormat(n.FRAGMENT_SHADER,n.MEDIUM_FLOAT).precision>0?"mediump":"lowp"}let l=t.precision!==void 0?t.precision:"highp";const d=c(l);d!==l&&(console.warn("THREE.WebGLRenderer:",l,"not supported, using",d,"instead."),l=d);const h=t.logarithmicDepthBuffer===!0,f=t.reverseDepthBuffer===!0&&e.has("EXT_clip_control"),m=n.getParameter(n.MAX_TEXTURE_IMAGE_UNITS),g=n.getParameter(n.MAX_VERTEX_TEXTURE_IMAGE_UNITS),_=n.getParameter(n.MAX_TEXTURE_SIZE),p=n.getParameter(n.MAX_CUBE_MAP_TEXTURE_SIZE),u=n.getParameter(n.MAX_VERTEX_ATTRIBS),E=n.getParameter(n.MAX_VERTEX_UNIFORM_VECTORS),y=n.getParameter(n.MAX_VARYING_VECTORS),M=n.getParameter(n.MAX_FRAGMENT_UNIFORM_VECTORS),D=g>0,w=n.getParameter(n.MAX_SAMPLES);return{isWebGL2:!0,getMaxAnisotropy:s,getMaxPrecision:c,textureFormatReadable:a,textureTypeReadable:o,precision:l,logarithmicDepthBuffer:h,reverseDepthBuffer:f,maxTextures:m,maxVertexTextures:g,maxTextureSize:_,maxCubemapSize:p,maxAttributes:u,maxVertexUniforms:E,maxVaryings:y,maxFragmentUniforms:M,vertexTextures:D,maxSamples:w}}function Df(n){const e=this;let t=null,i=0,r=!1,s=!1;const a=new Hn,o=new Ve,c={value:null,needsUpdate:!1};this.uniform=c,this.numPlanes=0,this.numIntersection=0,this.init=function(h,f){const m=h.length!==0||f||i!==0||r;return r=f,i=h.length,m},this.beginShadows=function(){s=!0,d(null)},this.endShadows=function(){s=!1},this.setGlobalState=function(h,f){t=d(h,f,0)},this.setState=function(h,f,m){const g=h.clippingPlanes,_=h.clipIntersection,p=h.clipShadows,u=n.get(h);if(!r||g===null||g.length===0||s&&!p)s?d(null):l();else{const E=s?0:i,y=E*4;let M=u.clippingState||null;c.value=M,M=d(g,f,y,m);for(let D=0;D!==y;++D)M[D]=t[D];u.clippingState=M,this.numIntersection=_?this.numPlanes:0,this.numPlanes+=E}};function l(){c.value!==t&&(c.value=t,c.needsUpdate=i>0),e.numPlanes=i,e.numIntersection=0}function d(h,f,m,g){const _=h!==null?h.length:0;let p=null;if(_!==0){if(p=c.value,g!==!0||p===null){const u=m+_*4,E=f.matrixWorldInverse;o.getNormalMatrix(E),(p===null||p.length<u)&&(p=new Float32Array(u));for(let y=0,M=m;y!==_;++y,M+=4)a.copy(h[y]).applyMatrix4(E,o),a.normal.toArray(p,M),p[M+3]=a.constant}c.value=p,c.needsUpdate=!0}return e.numPlanes=_,e.numIntersection=0,p}}function Lf(n){let e=new WeakMap;function t(a,o){return o===qs?a.mapping=Ci:o===Ks&&(a.mapping=Pi),a}function i(a){if(a&&a.isTexture){const o=a.mapping;if(o===qs||o===Ks)if(e.has(a)){const c=e.get(a).texture;return t(c,a.mapping)}else{const c=a.image;if(c&&c.height>0){const l=new Pu(c.height);return l.fromEquirectangularTexture(n,a),e.set(a,l),a.addEventListener("dispose",r),t(l.texture,a.mapping)}else return null}}return a}function r(a){const o=a.target;o.removeEventListener("dispose",r);const c=e.get(o);c!==void 0&&(e.delete(o),c.dispose())}function s(){e=new WeakMap}return{get:i,dispose:s}}const Ei=4,jo=[.125,.215,.35,.446,.526,.582],qn=20,As=new Qc,Wo=new oe;let ws=null,Rs=0,Cs=0,Ps=!1;const Gn=(1+Math.sqrt(5))/2,vi=1/Gn,Xo=[new k(-Gn,vi,0),new k(Gn,vi,0),new k(-vi,0,Gn),new k(vi,0,Gn),new k(0,Gn,-vi),new k(0,Gn,vi),new k(-1,1,-1),new k(1,1,-1),new k(-1,1,1),new k(1,1,1)],If=new k;class Ta{constructor(e){this._renderer=e,this._pingPongRenderTarget=null,this._lodMax=0,this._cubeSize=0,this._lodPlanes=[],this._sizeLods=[],this._sigmas=[],this._blurMaterial=null,this._cubemapMaterial=null,this._equirectMaterial=null,this._compileMaterial(this._blurMaterial)}fromScene(e,t=0,i=.1,r=100,s={}){const{size:a=256,position:o=If}=s;ws=this._renderer.getRenderTarget(),Rs=this._renderer.getActiveCubeFace(),Cs=this._renderer.getActiveMipmapLevel(),Ps=this._renderer.xr.enabled,this._renderer.xr.enabled=!1,this._setSize(a);const c=this._allocateTargets();return c.depthBuffer=!0,this._sceneToCubeUV(e,i,r,c,o),t>0&&this._blur(c,0,0,t),this._applyPMREM(c),this._cleanup(c),c}fromEquirectangular(e,t=null){return this._fromTexture(e,t)}fromCubemap(e,t=null){return this._fromTexture(e,t)}compileCubemapShader(){this._cubemapMaterial===null&&(this._cubemapMaterial=Yo(),this._compileMaterial(this._cubemapMaterial))}compileEquirectangularShader(){this._equirectMaterial===null&&(this._equirectMaterial=Ko(),this._compileMaterial(this._equirectMaterial))}dispose(){this._dispose(),this._cubemapMaterial!==null&&this._cubemapMaterial.dispose(),this._equirectMaterial!==null&&this._equirectMaterial.dispose()}_setSize(e){this._lodMax=Math.floor(Math.log2(e)),this._cubeSize=Math.pow(2,this._lodMax)}_dispose(){this._blurMaterial!==null&&this._blurMaterial.dispose(),this._pingPongRenderTarget!==null&&this._pingPongRenderTarget.dispose();for(let e=0;e<this._lodPlanes.length;e++)this._lodPlanes[e].dispose()}_cleanup(e){this._renderer.setRenderTarget(ws,Rs,Cs),this._renderer.xr.enabled=Ps,e.scissorTest=!1,Lr(e,0,0,e.width,e.height)}_fromTexture(e,t){e.mapping===Ci||e.mapping===Pi?this._setSize(e.image.length===0?16:e.image[0].width||e.image[0].image.width):this._setSize(e.image.width/4),ws=this._renderer.getRenderTarget(),Rs=this._renderer.getActiveCubeFace(),Cs=this._renderer.getActiveMipmapLevel(),Ps=this._renderer.xr.enabled,this._renderer.xr.enabled=!1;const i=t||this._allocateTargets();return this._textureToCubeUV(e,i),this._applyPMREM(i),this._cleanup(i),i}_allocateTargets(){const e=3*Math.max(this._cubeSize,112),t=4*this._cubeSize,i={magFilter:Zt,minFilter:Zt,generateMipmaps:!1,type:nr,format:Gt,colorSpace:Ii,depthBuffer:!1},r=qo(e,t,i);if(this._pingPongRenderTarget===null||this._pingPongRenderTarget.width!==e||this._pingPongRenderTarget.height!==t){this._pingPongRenderTarget!==null&&this._dispose(),this._pingPongRenderTarget=qo(e,t,i);const{_lodMax:s}=this;({sizeLods:this._sizeLods,lodPlanes:this._lodPlanes,sigmas:this._sigmas}=Uf(s)),this._blurMaterial=zf(s,e,t)}return r}_compileMaterial(e){const t=new Le(this._lodPlanes[0],e);this._renderer.compile(t,As)}_sceneToCubeUV(e,t,i,r,s){const c=new Ft(90,1,t,i),l=[1,-1,1,1,1,1],d=[1,1,1,-1,-1,-1],h=this._renderer,f=h.autoClear,m=h.toneMapping;h.getClearColor(Wo),h.toneMapping=Cn,h.autoClear=!1;const g=new Ln({name:"PMREM.Background",side:Ct,depthWrite:!1,depthTest:!1}),_=new Le(new Jt,g);let p=!1;const u=e.background;u?u.isColor&&(g.color.copy(u),e.background=null,p=!0):(g.color.copy(Wo),p=!0);for(let E=0;E<6;E++){const y=E%3;y===0?(c.up.set(0,l[E],0),c.position.set(s.x,s.y,s.z),c.lookAt(s.x+d[E],s.y,s.z)):y===1?(c.up.set(0,0,l[E]),c.position.set(s.x,s.y,s.z),c.lookAt(s.x,s.y+d[E],s.z)):(c.up.set(0,l[E],0),c.position.set(s.x,s.y,s.z),c.lookAt(s.x,s.y,s.z+d[E]));const M=this._cubeSize;Lr(r,y*M,E>2?M:0,M,M),h.setRenderTarget(r),p&&h.render(_,c),h.render(e,c)}_.geometry.dispose(),_.material.dispose(),h.toneMapping=m,h.autoClear=f,e.background=u}_textureToCubeUV(e,t){const i=this._renderer,r=e.mapping===Ci||e.mapping===Pi;r?(this._cubemapMaterial===null&&(this._cubemapMaterial=Yo()),this._cubemapMaterial.uniforms.flipEnvMap.value=e.isRenderTargetTexture===!1?-1:1):this._equirectMaterial===null&&(this._equirectMaterial=Ko());const s=r?this._cubemapMaterial:this._equirectMaterial,a=new Le(this._lodPlanes[0],s),o=s.uniforms;o.envMap.value=e;const c=this._cubeSize;Lr(t,0,0,3*c,2*c),i.setRenderTarget(t),i.render(a,As)}_applyPMREM(e){const t=this._renderer,i=t.autoClear;t.autoClear=!1;const r=this._lodPlanes.length;for(let s=1;s<r;s++){const a=Math.sqrt(this._sigmas[s]*this._sigmas[s]-this._sigmas[s-1]*this._sigmas[s-1]),o=Xo[(r-s-1)%Xo.length];this._blur(e,s-1,s,a,o)}t.autoClear=i}_blur(e,t,i,r,s){const a=this._pingPongRenderTarget;this._halfBlur(e,a,t,i,r,"latitudinal",s),this._halfBlur(a,e,i,i,r,"longitudinal",s)}_halfBlur(e,t,i,r,s,a,o){const c=this._renderer,l=this._blurMaterial;a!=="latitudinal"&&a!=="longitudinal"&&console.error("blur direction must be either latitudinal or longitudinal!");const d=3,h=new Le(this._lodPlanes[r],l),f=l.uniforms,m=this._sizeLods[i]-1,g=isFinite(s)?Math.PI/(2*m):2*Math.PI/(2*qn-1),_=s/g,p=isFinite(s)?1+Math.floor(d*_):qn;p>qn&&console.warn(`sigmaRadians, ${s}, is too large and will clip, as it requested ${p} samples when the maximum is set to ${qn}`);const u=[];let E=0;for(let b=0;b<qn;++b){const C=b/_,v=Math.exp(-C*C/2);u.push(v),b===0?E+=v:b<p&&(E+=2*v)}for(let b=0;b<u.length;b++)u[b]=u[b]/E;f.envMap.value=e.texture,f.samples.value=p,f.weights.value=u,f.latitudinal.value=a==="latitudinal",o&&(f.poleAxis.value=o);const{_lodMax:y}=this;f.dTheta.value=g,f.mipInt.value=y-i;const M=this._sizeLods[r],D=3*M*(r>y-Ei?r-y+Ei:0),w=4*(this._cubeSize-M);Lr(t,D,w,3*M,2*M),c.setRenderTarget(t),c.render(h,As)}}function Uf(n){const e=[],t=[],i=[];let r=n;const s=n-Ei+1+jo.length;for(let a=0;a<s;a++){const o=Math.pow(2,r);t.push(o);let c=1/o;a>n-Ei?c=jo[a-n+Ei-1]:a===0&&(c=0),i.push(c);const l=1/(o-2),d=-l,h=1+l,f=[d,d,h,d,h,h,d,d,h,h,d,h],m=6,g=6,_=3,p=2,u=1,E=new Float32Array(_*g*m),y=new Float32Array(p*g*m),M=new Float32Array(u*g*m);for(let w=0;w<m;w++){const b=w%3*2/3-1,C=w>2?0:-1,v=[b,C,0,b+2/3,C,0,b+2/3,C+1,0,b,C,0,b+2/3,C+1,0,b,C+1,0];E.set(v,_*g*w),y.set(f,p*g*w);const x=[w,w,w,w,w,w];M.set(x,u*g*w)}const D=new Ke;D.setAttribute("position",new Qt(E,_)),D.setAttribute("uv",new Qt(y,p)),D.setAttribute("faceIndex",new Qt(M,u)),e.push(D),r>Ei&&r--}return{lodPlanes:e,sizeLods:t,sigmas:i}}function qo(n,e,t){const i=new ei(n,e,t);return i.texture.mapping=Kr,i.texture.name="PMREM.cubeUv",i.scissorTest=!0,i}function Lr(n,e,t,i,r){n.viewport.set(e,t,i,r),n.scissor.set(e,t,i,r)}function zf(n,e,t){const i=new Float32Array(qn),r=new k(0,1,0);return new Dn({name:"SphericalGaussianBlur",defines:{n:qn,CUBEUV_TEXEL_WIDTH:1/e,CUBEUV_TEXEL_HEIGHT:1/t,CUBEUV_MAX_MIP:`${n}.0`},uniforms:{envMap:{value:null},samples:{value:1},weights:{value:i},latitudinal:{value:!1},dTheta:{value:0},mipInt:{value:0},poleAxis:{value:r}},vertexShader:qa(),fragmentShader:`

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
		`,blending:Rn,depthTest:!1,depthWrite:!1})}function Ko(){return new Dn({name:"EquirectangularToCubeUV",uniforms:{envMap:{value:null}},vertexShader:qa(),fragmentShader:`

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
		`,blending:Rn,depthTest:!1,depthWrite:!1})}function Yo(){return new Dn({name:"CubemapToCubeUV",uniforms:{envMap:{value:null},flipEnvMap:{value:-1}},vertexShader:qa(),fragmentShader:`

			precision mediump float;
			precision mediump int;

			uniform float flipEnvMap;

			varying vec3 vOutputDirection;

			uniform samplerCube envMap;

			void main() {

				gl_FragColor = textureCube( envMap, vec3( flipEnvMap * vOutputDirection.x, vOutputDirection.yz ) );

			}
		`,blending:Rn,depthTest:!1,depthWrite:!1})}function qa(){return`

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
	`}function Nf(n){let e=new WeakMap,t=null;function i(o){if(o&&o.isTexture){const c=o.mapping,l=c===qs||c===Ks,d=c===Ci||c===Pi;if(l||d){let h=e.get(o);const f=h!==void 0?h.texture.pmremVersion:0;if(o.isRenderTargetTexture&&o.pmremVersion!==f)return t===null&&(t=new Ta(n)),h=l?t.fromEquirectangular(o,h):t.fromCubemap(o,h),h.texture.pmremVersion=o.pmremVersion,e.set(o,h),h.texture;if(h!==void 0)return h.texture;{const m=o.image;return l&&m&&m.height>0||d&&m&&r(m)?(t===null&&(t=new Ta(n)),h=l?t.fromEquirectangular(o):t.fromCubemap(o),h.texture.pmremVersion=o.pmremVersion,e.set(o,h),o.addEventListener("dispose",s),h.texture):null}}}return o}function r(o){let c=0;const l=6;for(let d=0;d<l;d++)o[d]!==void 0&&c++;return c===l}function s(o){const c=o.target;c.removeEventListener("dispose",s);const l=e.get(c);l!==void 0&&(e.delete(c),l.dispose())}function a(){e=new WeakMap,t!==null&&(t.dispose(),t=null)}return{get:i,dispose:a}}function Ff(n){const e={};function t(i){if(e[i]!==void 0)return e[i];let r;switch(i){case"WEBGL_depth_texture":r=n.getExtension("WEBGL_depth_texture")||n.getExtension("MOZ_WEBGL_depth_texture")||n.getExtension("WEBKIT_WEBGL_depth_texture");break;case"EXT_texture_filter_anisotropic":r=n.getExtension("EXT_texture_filter_anisotropic")||n.getExtension("MOZ_EXT_texture_filter_anisotropic")||n.getExtension("WEBKIT_EXT_texture_filter_anisotropic");break;case"WEBGL_compressed_texture_s3tc":r=n.getExtension("WEBGL_compressed_texture_s3tc")||n.getExtension("MOZ_WEBGL_compressed_texture_s3tc")||n.getExtension("WEBKIT_WEBGL_compressed_texture_s3tc");break;case"WEBGL_compressed_texture_pvrtc":r=n.getExtension("WEBGL_compressed_texture_pvrtc")||n.getExtension("WEBKIT_WEBGL_compressed_texture_pvrtc");break;default:r=n.getExtension(i)}return e[i]=r,r}return{has:function(i){return t(i)!==null},init:function(){t("EXT_color_buffer_float"),t("WEBGL_clip_cull_distance"),t("OES_texture_float_linear"),t("EXT_color_buffer_half_float"),t("WEBGL_multisampled_render_to_texture"),t("WEBGL_render_shared_exponent")},get:function(i){const r=t(i);return r===null&&Vn("THREE.WebGLRenderer: "+i+" extension not supported."),r}}}function kf(n,e,t,i){const r={},s=new WeakMap;function a(h){const f=h.target;f.index!==null&&e.remove(f.index);for(const g in f.attributes)e.remove(f.attributes[g]);f.removeEventListener("dispose",a),delete r[f.id];const m=s.get(f);m&&(e.remove(m),s.delete(f)),i.releaseStatesOfGeometry(f),f.isInstancedBufferGeometry===!0&&delete f._maxInstanceCount,t.memory.geometries--}function o(h,f){return r[f.id]===!0||(f.addEventListener("dispose",a),r[f.id]=!0,t.memory.geometries++),f}function c(h){const f=h.attributes;for(const m in f)e.update(f[m],n.ARRAY_BUFFER)}function l(h){const f=[],m=h.index,g=h.attributes.position;let _=0;if(m!==null){const E=m.array;_=m.version;for(let y=0,M=E.length;y<M;y+=3){const D=E[y+0],w=E[y+1],b=E[y+2];f.push(D,w,w,b,b,D)}}else if(g!==void 0){const E=g.array;_=g.version;for(let y=0,M=E.length/3-1;y<M;y+=3){const D=y+0,w=y+1,b=y+2;f.push(D,w,w,b,b,D)}}else return;const p=new(Hc(f)?Xc:Wc)(f,1);p.version=_;const u=s.get(h);u&&e.remove(u),s.set(h,p)}function d(h){const f=s.get(h);if(f){const m=h.index;m!==null&&f.version<m.version&&l(h)}else l(h);return s.get(h)}return{get:o,update:c,getWireframeAttribute:d}}function Of(n,e,t){let i;function r(f){i=f}let s,a;function o(f){s=f.type,a=f.bytesPerElement}function c(f,m){n.drawElements(i,m,s,f*a),t.update(m,i,1)}function l(f,m,g){g!==0&&(n.drawElementsInstanced(i,m,s,f*a,g),t.update(m,i,g))}function d(f,m,g){if(g===0)return;e.get("WEBGL_multi_draw").multiDrawElementsWEBGL(i,m,0,s,f,0,g);let p=0;for(let u=0;u<g;u++)p+=m[u];t.update(p,i,1)}function h(f,m,g,_){if(g===0)return;const p=e.get("WEBGL_multi_draw");if(p===null)for(let u=0;u<f.length;u++)l(f[u]/a,m[u],_[u]);else{p.multiDrawElementsInstancedWEBGL(i,m,0,s,f,0,_,0,g);let u=0;for(let E=0;E<g;E++)u+=m[E]*_[E];t.update(u,i,1)}}this.setMode=r,this.setIndex=o,this.render=c,this.renderInstances=l,this.renderMultiDraw=d,this.renderMultiDrawInstances=h}function Bf(n){const e={geometries:0,textures:0},t={frame:0,calls:0,triangles:0,points:0,lines:0};function i(s,a,o){switch(t.calls++,a){case n.TRIANGLES:t.triangles+=o*(s/3);break;case n.LINES:t.lines+=o*(s/2);break;case n.LINE_STRIP:t.lines+=o*(s-1);break;case n.LINE_LOOP:t.lines+=o*s;break;case n.POINTS:t.points+=o*s;break;default:console.error("THREE.WebGLInfo: Unknown draw mode:",a);break}}function r(){t.calls=0,t.triangles=0,t.points=0,t.lines=0}return{memory:e,render:t,programs:null,autoReset:!0,reset:r,update:i}}function Vf(n,e,t){const i=new WeakMap,r=new rt;function s(a,o,c){const l=a.morphTargetInfluences,d=o.morphAttributes.position||o.morphAttributes.normal||o.morphAttributes.color,h=d!==void 0?d.length:0;let f=i.get(o);if(f===void 0||f.count!==h){let v=function(){b.dispose(),i.delete(o),o.removeEventListener("dispose",v)};f!==void 0&&f.texture.dispose();const m=o.morphAttributes.position!==void 0,g=o.morphAttributes.normal!==void 0,_=o.morphAttributes.color!==void 0,p=o.morphAttributes.position||[],u=o.morphAttributes.normal||[],E=o.morphAttributes.color||[];let y=0;m===!0&&(y=1),g===!0&&(y=2),_===!0&&(y=3);let M=o.attributes.position.count*y,D=1;M>e.maxTextureSize&&(D=Math.ceil(M/e.maxTextureSize),M=e.maxTextureSize);const w=new Float32Array(M*D*4*h),b=new Gc(w,M,D,h);b.type=dn,b.needsUpdate=!0;const C=y*4;for(let x=0;x<h;x++){const P=p[x],U=u[x],A=E[x],R=M*D*4*x;for(let z=0;z<P.count;z++){const N=z*C;m===!0&&(r.fromBufferAttribute(P,z),w[R+N+0]=r.x,w[R+N+1]=r.y,w[R+N+2]=r.z,w[R+N+3]=0),g===!0&&(r.fromBufferAttribute(U,z),w[R+N+4]=r.x,w[R+N+5]=r.y,w[R+N+6]=r.z,w[R+N+7]=0),_===!0&&(r.fromBufferAttribute(A,z),w[R+N+8]=r.x,w[R+N+9]=r.y,w[R+N+10]=r.z,w[R+N+11]=A.itemSize===4?r.w:1)}}f={count:h,texture:b,size:new We(M,D)},i.set(o,f),o.addEventListener("dispose",v)}if(a.isInstancedMesh===!0&&a.morphTexture!==null)c.getUniforms().setValue(n,"morphTexture",a.morphTexture,t);else{let m=0;for(let _=0;_<l.length;_++)m+=l[_];const g=o.morphTargetsRelative?1:1-m;c.getUniforms().setValue(n,"morphTargetBaseInfluence",g),c.getUniforms().setValue(n,"morphTargetInfluences",l)}c.getUniforms().setValue(n,"morphTargetsTexture",f.texture,t),c.getUniforms().setValue(n,"morphTargetsTextureSize",f.size)}return{update:s}}function Hf(n,e,t,i){let r=new WeakMap;function s(c){const l=i.render.frame,d=c.geometry,h=e.get(c,d);if(r.get(h)!==l&&(e.update(h),r.set(h,l)),c.isInstancedMesh&&(c.hasEventListener("dispose",o)===!1&&c.addEventListener("dispose",o),r.get(c)!==l&&(t.update(c.instanceMatrix,n.ARRAY_BUFFER),c.instanceColor!==null&&t.update(c.instanceColor,n.ARRAY_BUFFER),r.set(c,l))),c.isSkinnedMesh){const f=c.skeleton;r.get(f)!==l&&(f.update(),r.set(f,l))}return h}function a(){r=new WeakMap}function o(c){const l=c.target;l.removeEventListener("dispose",o),t.remove(l.instanceMatrix),l.instanceColor!==null&&t.remove(l.instanceColor)}return{update:s,dispose:a}}const tl=new At,$o=new Zc(1,1),nl=new Gc,il=new fu,rl=new Yc,Zo=[],Jo=[],Qo=new Float32Array(16),ec=new Float32Array(9),tc=new Float32Array(4);function Oi(n,e,t){const i=n[0];if(i<=0||i>0)return n;const r=e*t;let s=Zo[r];if(s===void 0&&(s=new Float32Array(r),Zo[r]=s),e!==0){i.toArray(s,0);for(let a=1,o=0;a!==e;++a)o+=t,n[a].toArray(s,o)}return s}function gt(n,e){if(n.length!==e.length)return!1;for(let t=0,i=n.length;t<i;t++)if(n[t]!==e[t])return!1;return!0}function _t(n,e){for(let t=0,i=e.length;t<i;t++)n[t]=e[t]}function $r(n,e){let t=Jo[e];t===void 0&&(t=new Int32Array(e),Jo[e]=t);for(let i=0;i!==e;++i)t[i]=n.allocateTextureUnit();return t}function Gf(n,e){const t=this.cache;t[0]!==e&&(n.uniform1f(this.addr,e),t[0]=e)}function jf(n,e){const t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y)&&(n.uniform2f(this.addr,e.x,e.y),t[0]=e.x,t[1]=e.y);else{if(gt(t,e))return;n.uniform2fv(this.addr,e),_t(t,e)}}function Wf(n,e){const t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y||t[2]!==e.z)&&(n.uniform3f(this.addr,e.x,e.y,e.z),t[0]=e.x,t[1]=e.y,t[2]=e.z);else if(e.r!==void 0)(t[0]!==e.r||t[1]!==e.g||t[2]!==e.b)&&(n.uniform3f(this.addr,e.r,e.g,e.b),t[0]=e.r,t[1]=e.g,t[2]=e.b);else{if(gt(t,e))return;n.uniform3fv(this.addr,e),_t(t,e)}}function Xf(n,e){const t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y||t[2]!==e.z||t[3]!==e.w)&&(n.uniform4f(this.addr,e.x,e.y,e.z,e.w),t[0]=e.x,t[1]=e.y,t[2]=e.z,t[3]=e.w);else{if(gt(t,e))return;n.uniform4fv(this.addr,e),_t(t,e)}}function qf(n,e){const t=this.cache,i=e.elements;if(i===void 0){if(gt(t,e))return;n.uniformMatrix2fv(this.addr,!1,e),_t(t,e)}else{if(gt(t,i))return;tc.set(i),n.uniformMatrix2fv(this.addr,!1,tc),_t(t,i)}}function Kf(n,e){const t=this.cache,i=e.elements;if(i===void 0){if(gt(t,e))return;n.uniformMatrix3fv(this.addr,!1,e),_t(t,e)}else{if(gt(t,i))return;ec.set(i),n.uniformMatrix3fv(this.addr,!1,ec),_t(t,i)}}function Yf(n,e){const t=this.cache,i=e.elements;if(i===void 0){if(gt(t,e))return;n.uniformMatrix4fv(this.addr,!1,e),_t(t,e)}else{if(gt(t,i))return;Qo.set(i),n.uniformMatrix4fv(this.addr,!1,Qo),_t(t,i)}}function $f(n,e){const t=this.cache;t[0]!==e&&(n.uniform1i(this.addr,e),t[0]=e)}function Zf(n,e){const t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y)&&(n.uniform2i(this.addr,e.x,e.y),t[0]=e.x,t[1]=e.y);else{if(gt(t,e))return;n.uniform2iv(this.addr,e),_t(t,e)}}function Jf(n,e){const t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y||t[2]!==e.z)&&(n.uniform3i(this.addr,e.x,e.y,e.z),t[0]=e.x,t[1]=e.y,t[2]=e.z);else{if(gt(t,e))return;n.uniform3iv(this.addr,e),_t(t,e)}}function Qf(n,e){const t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y||t[2]!==e.z||t[3]!==e.w)&&(n.uniform4i(this.addr,e.x,e.y,e.z,e.w),t[0]=e.x,t[1]=e.y,t[2]=e.z,t[3]=e.w);else{if(gt(t,e))return;n.uniform4iv(this.addr,e),_t(t,e)}}function ep(n,e){const t=this.cache;t[0]!==e&&(n.uniform1ui(this.addr,e),t[0]=e)}function tp(n,e){const t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y)&&(n.uniform2ui(this.addr,e.x,e.y),t[0]=e.x,t[1]=e.y);else{if(gt(t,e))return;n.uniform2uiv(this.addr,e),_t(t,e)}}function np(n,e){const t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y||t[2]!==e.z)&&(n.uniform3ui(this.addr,e.x,e.y,e.z),t[0]=e.x,t[1]=e.y,t[2]=e.z);else{if(gt(t,e))return;n.uniform3uiv(this.addr,e),_t(t,e)}}function ip(n,e){const t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y||t[2]!==e.z||t[3]!==e.w)&&(n.uniform4ui(this.addr,e.x,e.y,e.z,e.w),t[0]=e.x,t[1]=e.y,t[2]=e.z,t[3]=e.w);else{if(gt(t,e))return;n.uniform4uiv(this.addr,e),_t(t,e)}}function rp(n,e,t){const i=this.cache,r=t.allocateTextureUnit();i[0]!==r&&(n.uniform1i(this.addr,r),i[0]=r);let s;this.type===n.SAMPLER_2D_SHADOW?($o.compareFunction=Vc,s=$o):s=tl,t.setTexture2D(e||s,r)}function sp(n,e,t){const i=this.cache,r=t.allocateTextureUnit();i[0]!==r&&(n.uniform1i(this.addr,r),i[0]=r),t.setTexture3D(e||il,r)}function ap(n,e,t){const i=this.cache,r=t.allocateTextureUnit();i[0]!==r&&(n.uniform1i(this.addr,r),i[0]=r),t.setTextureCube(e||rl,r)}function op(n,e,t){const i=this.cache,r=t.allocateTextureUnit();i[0]!==r&&(n.uniform1i(this.addr,r),i[0]=r),t.setTexture2DArray(e||nl,r)}function cp(n){switch(n){case 5126:return Gf;case 35664:return jf;case 35665:return Wf;case 35666:return Xf;case 35674:return qf;case 35675:return Kf;case 35676:return Yf;case 5124:case 35670:return $f;case 35667:case 35671:return Zf;case 35668:case 35672:return Jf;case 35669:case 35673:return Qf;case 5125:return ep;case 36294:return tp;case 36295:return np;case 36296:return ip;case 35678:case 36198:case 36298:case 36306:case 35682:return rp;case 35679:case 36299:case 36307:return sp;case 35680:case 36300:case 36308:case 36293:return ap;case 36289:case 36303:case 36311:case 36292:return op}}function lp(n,e){n.uniform1fv(this.addr,e)}function up(n,e){const t=Oi(e,this.size,2);n.uniform2fv(this.addr,t)}function dp(n,e){const t=Oi(e,this.size,3);n.uniform3fv(this.addr,t)}function hp(n,e){const t=Oi(e,this.size,4);n.uniform4fv(this.addr,t)}function fp(n,e){const t=Oi(e,this.size,4);n.uniformMatrix2fv(this.addr,!1,t)}function pp(n,e){const t=Oi(e,this.size,9);n.uniformMatrix3fv(this.addr,!1,t)}function mp(n,e){const t=Oi(e,this.size,16);n.uniformMatrix4fv(this.addr,!1,t)}function gp(n,e){n.uniform1iv(this.addr,e)}function _p(n,e){n.uniform2iv(this.addr,e)}function vp(n,e){n.uniform3iv(this.addr,e)}function xp(n,e){n.uniform4iv(this.addr,e)}function Mp(n,e){n.uniform1uiv(this.addr,e)}function Sp(n,e){n.uniform2uiv(this.addr,e)}function Ep(n,e){n.uniform3uiv(this.addr,e)}function yp(n,e){n.uniform4uiv(this.addr,e)}function bp(n,e,t){const i=this.cache,r=e.length,s=$r(t,r);gt(i,s)||(n.uniform1iv(this.addr,s),_t(i,s));for(let a=0;a!==r;++a)t.setTexture2D(e[a]||tl,s[a])}function Tp(n,e,t){const i=this.cache,r=e.length,s=$r(t,r);gt(i,s)||(n.uniform1iv(this.addr,s),_t(i,s));for(let a=0;a!==r;++a)t.setTexture3D(e[a]||il,s[a])}function Ap(n,e,t){const i=this.cache,r=e.length,s=$r(t,r);gt(i,s)||(n.uniform1iv(this.addr,s),_t(i,s));for(let a=0;a!==r;++a)t.setTextureCube(e[a]||rl,s[a])}function wp(n,e,t){const i=this.cache,r=e.length,s=$r(t,r);gt(i,s)||(n.uniform1iv(this.addr,s),_t(i,s));for(let a=0;a!==r;++a)t.setTexture2DArray(e[a]||nl,s[a])}function Rp(n){switch(n){case 5126:return lp;case 35664:return up;case 35665:return dp;case 35666:return hp;case 35674:return fp;case 35675:return pp;case 35676:return mp;case 5124:case 35670:return gp;case 35667:case 35671:return _p;case 35668:case 35672:return vp;case 35669:case 35673:return xp;case 5125:return Mp;case 36294:return Sp;case 36295:return Ep;case 36296:return yp;case 35678:case 36198:case 36298:case 36306:case 35682:return bp;case 35679:case 36299:case 36307:return Tp;case 35680:case 36300:case 36308:case 36293:return Ap;case 36289:case 36303:case 36311:case 36292:return wp}}class Cp{constructor(e,t,i){this.id=e,this.addr=i,this.cache=[],this.type=t.type,this.setValue=cp(t.type)}}class Pp{constructor(e,t,i){this.id=e,this.addr=i,this.cache=[],this.type=t.type,this.size=t.size,this.setValue=Rp(t.type)}}class Dp{constructor(e){this.id=e,this.seq=[],this.map={}}setValue(e,t,i){const r=this.seq;for(let s=0,a=r.length;s!==a;++s){const o=r[s];o.setValue(e,t[o.id],i)}}}const Ds=/(\w+)(\])?(\[|\.)?/g;function nc(n,e){n.seq.push(e),n.map[e.id]=e}function Lp(n,e,t){const i=n.name,r=i.length;for(Ds.lastIndex=0;;){const s=Ds.exec(i),a=Ds.lastIndex;let o=s[1];const c=s[2]==="]",l=s[3];if(c&&(o=o|0),l===void 0||l==="["&&a+2===r){nc(t,l===void 0?new Cp(o,n,e):new Pp(o,n,e));break}else{let h=t.map[o];h===void 0&&(h=new Dp(o),nc(t,h)),t=h}}}class Vr{constructor(e,t){this.seq=[],this.map={};const i=e.getProgramParameter(t,e.ACTIVE_UNIFORMS);for(let r=0;r<i;++r){const s=e.getActiveUniform(t,r),a=e.getUniformLocation(t,s.name);Lp(s,a,this)}}setValue(e,t,i,r){const s=this.map[t];s!==void 0&&s.setValue(e,i,r)}setOptional(e,t,i){const r=t[i];r!==void 0&&this.setValue(e,i,r)}static upload(e,t,i,r){for(let s=0,a=t.length;s!==a;++s){const o=t[s],c=i[o.id];c.needsUpdate!==!1&&o.setValue(e,c.value,r)}}static seqWithValue(e,t){const i=[];for(let r=0,s=e.length;r!==s;++r){const a=e[r];a.id in t&&i.push(a)}return i}}function ic(n,e,t){const i=n.createShader(e);return n.shaderSource(i,t),n.compileShader(i),i}const Ip=37297;let Up=0;function zp(n,e){const t=n.split(`
`),i=[],r=Math.max(e-6,0),s=Math.min(e+6,t.length);for(let a=r;a<s;a++){const o=a+1;i.push(`${o===e?">":" "} ${o}: ${t[a]}`)}return i.join(`
`)}const rc=new Ve;function Np(n){Je._getMatrix(rc,Je.workingColorSpace,n);const e=`mat3( ${rc.elements.map(t=>t.toFixed(4))} )`;switch(Je.getTransfer(n)){case Gr:return[e,"LinearTransferOETF"];case it:return[e,"sRGBTransferOETF"];default:return console.warn("THREE.WebGLProgram: Unsupported color space: ",n),[e,"LinearTransferOETF"]}}function sc(n,e,t){const i=n.getShaderParameter(e,n.COMPILE_STATUS),r=n.getShaderInfoLog(e).trim();if(i&&r==="")return"";const s=/ERROR: 0:(\d+)/.exec(r);if(s){const a=parseInt(s[1]);return t.toUpperCase()+`

`+r+`

`+zp(n.getShaderSource(e),a)}else return r}function Fp(n,e){const t=Np(e);return[`vec4 ${n}( vec4 value ) {`,`	return ${t[1]}( vec4( value.rgb * ${t[0]}, value.a ) );`,"}"].join(`
`)}function kp(n,e){let t;switch(e){case Ol:t="Linear";break;case Bl:t="Reinhard";break;case Vl:t="Cineon";break;case Hl:t="ACESFilmic";break;case jl:t="AgX";break;case Wl:t="Neutral";break;case Gl:t="Custom";break;default:console.warn("THREE.WebGLProgram: Unsupported toneMapping:",e),t="Linear"}return"vec3 "+n+"( vec3 color ) { return "+t+"ToneMapping( color ); }"}const Ir=new k;function Op(){Je.getLuminanceCoefficients(Ir);const n=Ir.x.toFixed(4),e=Ir.y.toFixed(4),t=Ir.z.toFixed(4);return["float luminance( const in vec3 rgb ) {",`	const vec3 weights = vec3( ${n}, ${e}, ${t} );`,"	return dot( weights, rgb );","}"].join(`
`)}function Bp(n){return[n.extensionClipCullDistance?"#extension GL_ANGLE_clip_cull_distance : require":"",n.extensionMultiDraw?"#extension GL_ANGLE_multi_draw : require":""].filter(Yi).join(`
`)}function Vp(n){const e=[];for(const t in n){const i=n[t];i!==!1&&e.push("#define "+t+" "+i)}return e.join(`
`)}function Hp(n,e){const t={},i=n.getProgramParameter(e,n.ACTIVE_ATTRIBUTES);for(let r=0;r<i;r++){const s=n.getActiveAttrib(e,r),a=s.name;let o=1;s.type===n.FLOAT_MAT2&&(o=2),s.type===n.FLOAT_MAT3&&(o=3),s.type===n.FLOAT_MAT4&&(o=4),t[a]={type:s.type,location:n.getAttribLocation(e,a),locationSize:o}}return t}function Yi(n){return n!==""}function ac(n,e){const t=e.numSpotLightShadows+e.numSpotLightMaps-e.numSpotLightShadowsWithMaps;return n.replace(/NUM_DIR_LIGHTS/g,e.numDirLights).replace(/NUM_SPOT_LIGHTS/g,e.numSpotLights).replace(/NUM_SPOT_LIGHT_MAPS/g,e.numSpotLightMaps).replace(/NUM_SPOT_LIGHT_COORDS/g,t).replace(/NUM_RECT_AREA_LIGHTS/g,e.numRectAreaLights).replace(/NUM_POINT_LIGHTS/g,e.numPointLights).replace(/NUM_HEMI_LIGHTS/g,e.numHemiLights).replace(/NUM_DIR_LIGHT_SHADOWS/g,e.numDirLightShadows).replace(/NUM_SPOT_LIGHT_SHADOWS_WITH_MAPS/g,e.numSpotLightShadowsWithMaps).replace(/NUM_SPOT_LIGHT_SHADOWS/g,e.numSpotLightShadows).replace(/NUM_POINT_LIGHT_SHADOWS/g,e.numPointLightShadows)}function oc(n,e){return n.replace(/NUM_CLIPPING_PLANES/g,e.numClippingPlanes).replace(/UNION_CLIPPING_PLANES/g,e.numClippingPlanes-e.numClipIntersection)}const Gp=/^[ \t]*#include +<([\w\d./]+)>/gm;function Aa(n){return n.replace(Gp,Wp)}const jp=new Map;function Wp(n,e){let t=Ge[e];if(t===void 0){const i=jp.get(e);if(i!==void 0)t=Ge[i],console.warn('THREE.WebGLRenderer: Shader chunk "%s" has been deprecated. Use "%s" instead.',e,i);else throw new Error("Can not resolve #include <"+e+">")}return Aa(t)}const Xp=/#pragma unroll_loop_start\s+for\s*\(\s*int\s+i\s*=\s*(\d+)\s*;\s*i\s*<\s*(\d+)\s*;\s*i\s*\+\+\s*\)\s*{([\s\S]+?)}\s+#pragma unroll_loop_end/g;function cc(n){return n.replace(Xp,qp)}function qp(n,e,t,i){let r="";for(let s=parseInt(e);s<parseInt(t);s++)r+=i.replace(/\[\s*i\s*\]/g,"[ "+s+" ]").replace(/UNROLLED_LOOP_INDEX/g,s);return r}function lc(n){let e=`precision ${n.precision} float;
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
#define LOW_PRECISION`),e}function Kp(n){let e="SHADOWMAP_TYPE_BASIC";return n.shadowMapType===wc?e="SHADOWMAP_TYPE_PCF":n.shadowMapType===vl?e="SHADOWMAP_TYPE_PCF_SOFT":n.shadowMapType===ln&&(e="SHADOWMAP_TYPE_VSM"),e}function Yp(n){let e="ENVMAP_TYPE_CUBE";if(n.envMap)switch(n.envMapMode){case Ci:case Pi:e="ENVMAP_TYPE_CUBE";break;case Kr:e="ENVMAP_TYPE_CUBE_UV";break}return e}function $p(n){let e="ENVMAP_MODE_REFLECTION";if(n.envMap)switch(n.envMapMode){case Pi:e="ENVMAP_MODE_REFRACTION";break}return e}function Zp(n){let e="ENVMAP_BLENDING_NONE";if(n.envMap)switch(n.combine){case Rc:e="ENVMAP_BLENDING_MULTIPLY";break;case Fl:e="ENVMAP_BLENDING_MIX";break;case kl:e="ENVMAP_BLENDING_ADD";break}return e}function Jp(n){const e=n.envMapCubeUVHeight;if(e===null)return null;const t=Math.log2(e)-2,i=1/e;return{texelWidth:1/(3*Math.max(Math.pow(2,t),112)),texelHeight:i,maxMip:t}}function Qp(n,e,t,i){const r=n.getContext(),s=t.defines;let a=t.vertexShader,o=t.fragmentShader;const c=Kp(t),l=Yp(t),d=$p(t),h=Zp(t),f=Jp(t),m=Bp(t),g=Vp(s),_=r.createProgram();let p,u,E=t.glslVersion?"#version "+t.glslVersion+`
`:"";t.isRawShaderMaterial?(p=["#define SHADER_TYPE "+t.shaderType,"#define SHADER_NAME "+t.shaderName,g].filter(Yi).join(`
`),p.length>0&&(p+=`
`),u=["#define SHADER_TYPE "+t.shaderType,"#define SHADER_NAME "+t.shaderName,g].filter(Yi).join(`
`),u.length>0&&(u+=`
`)):(p=[lc(t),"#define SHADER_TYPE "+t.shaderType,"#define SHADER_NAME "+t.shaderName,g,t.extensionClipCullDistance?"#define USE_CLIP_DISTANCE":"",t.batching?"#define USE_BATCHING":"",t.batchingColor?"#define USE_BATCHING_COLOR":"",t.instancing?"#define USE_INSTANCING":"",t.instancingColor?"#define USE_INSTANCING_COLOR":"",t.instancingMorph?"#define USE_INSTANCING_MORPH":"",t.useFog&&t.fog?"#define USE_FOG":"",t.useFog&&t.fogExp2?"#define FOG_EXP2":"",t.map?"#define USE_MAP":"",t.envMap?"#define USE_ENVMAP":"",t.envMap?"#define "+d:"",t.lightMap?"#define USE_LIGHTMAP":"",t.aoMap?"#define USE_AOMAP":"",t.bumpMap?"#define USE_BUMPMAP":"",t.normalMap?"#define USE_NORMALMAP":"",t.normalMapObjectSpace?"#define USE_NORMALMAP_OBJECTSPACE":"",t.normalMapTangentSpace?"#define USE_NORMALMAP_TANGENTSPACE":"",t.displacementMap?"#define USE_DISPLACEMENTMAP":"",t.emissiveMap?"#define USE_EMISSIVEMAP":"",t.anisotropy?"#define USE_ANISOTROPY":"",t.anisotropyMap?"#define USE_ANISOTROPYMAP":"",t.clearcoatMap?"#define USE_CLEARCOATMAP":"",t.clearcoatRoughnessMap?"#define USE_CLEARCOAT_ROUGHNESSMAP":"",t.clearcoatNormalMap?"#define USE_CLEARCOAT_NORMALMAP":"",t.iridescenceMap?"#define USE_IRIDESCENCEMAP":"",t.iridescenceThicknessMap?"#define USE_IRIDESCENCE_THICKNESSMAP":"",t.specularMap?"#define USE_SPECULARMAP":"",t.specularColorMap?"#define USE_SPECULAR_COLORMAP":"",t.specularIntensityMap?"#define USE_SPECULAR_INTENSITYMAP":"",t.roughnessMap?"#define USE_ROUGHNESSMAP":"",t.metalnessMap?"#define USE_METALNESSMAP":"",t.alphaMap?"#define USE_ALPHAMAP":"",t.alphaHash?"#define USE_ALPHAHASH":"",t.transmission?"#define USE_TRANSMISSION":"",t.transmissionMap?"#define USE_TRANSMISSIONMAP":"",t.thicknessMap?"#define USE_THICKNESSMAP":"",t.sheenColorMap?"#define USE_SHEEN_COLORMAP":"",t.sheenRoughnessMap?"#define USE_SHEEN_ROUGHNESSMAP":"",t.mapUv?"#define MAP_UV "+t.mapUv:"",t.alphaMapUv?"#define ALPHAMAP_UV "+t.alphaMapUv:"",t.lightMapUv?"#define LIGHTMAP_UV "+t.lightMapUv:"",t.aoMapUv?"#define AOMAP_UV "+t.aoMapUv:"",t.emissiveMapUv?"#define EMISSIVEMAP_UV "+t.emissiveMapUv:"",t.bumpMapUv?"#define BUMPMAP_UV "+t.bumpMapUv:"",t.normalMapUv?"#define NORMALMAP_UV "+t.normalMapUv:"",t.displacementMapUv?"#define DISPLACEMENTMAP_UV "+t.displacementMapUv:"",t.metalnessMapUv?"#define METALNESSMAP_UV "+t.metalnessMapUv:"",t.roughnessMapUv?"#define ROUGHNESSMAP_UV "+t.roughnessMapUv:"",t.anisotropyMapUv?"#define ANISOTROPYMAP_UV "+t.anisotropyMapUv:"",t.clearcoatMapUv?"#define CLEARCOATMAP_UV "+t.clearcoatMapUv:"",t.clearcoatNormalMapUv?"#define CLEARCOAT_NORMALMAP_UV "+t.clearcoatNormalMapUv:"",t.clearcoatRoughnessMapUv?"#define CLEARCOAT_ROUGHNESSMAP_UV "+t.clearcoatRoughnessMapUv:"",t.iridescenceMapUv?"#define IRIDESCENCEMAP_UV "+t.iridescenceMapUv:"",t.iridescenceThicknessMapUv?"#define IRIDESCENCE_THICKNESSMAP_UV "+t.iridescenceThicknessMapUv:"",t.sheenColorMapUv?"#define SHEEN_COLORMAP_UV "+t.sheenColorMapUv:"",t.sheenRoughnessMapUv?"#define SHEEN_ROUGHNESSMAP_UV "+t.sheenRoughnessMapUv:"",t.specularMapUv?"#define SPECULARMAP_UV "+t.specularMapUv:"",t.specularColorMapUv?"#define SPECULAR_COLORMAP_UV "+t.specularColorMapUv:"",t.specularIntensityMapUv?"#define SPECULAR_INTENSITYMAP_UV "+t.specularIntensityMapUv:"",t.transmissionMapUv?"#define TRANSMISSIONMAP_UV "+t.transmissionMapUv:"",t.thicknessMapUv?"#define THICKNESSMAP_UV "+t.thicknessMapUv:"",t.vertexTangents&&t.flatShading===!1?"#define USE_TANGENT":"",t.vertexColors?"#define USE_COLOR":"",t.vertexAlphas?"#define USE_COLOR_ALPHA":"",t.vertexUv1s?"#define USE_UV1":"",t.vertexUv2s?"#define USE_UV2":"",t.vertexUv3s?"#define USE_UV3":"",t.pointsUvs?"#define USE_POINTS_UV":"",t.flatShading?"#define FLAT_SHADED":"",t.skinning?"#define USE_SKINNING":"",t.morphTargets?"#define USE_MORPHTARGETS":"",t.morphNormals&&t.flatShading===!1?"#define USE_MORPHNORMALS":"",t.morphColors?"#define USE_MORPHCOLORS":"",t.morphTargetsCount>0?"#define MORPHTARGETS_TEXTURE_STRIDE "+t.morphTextureStride:"",t.morphTargetsCount>0?"#define MORPHTARGETS_COUNT "+t.morphTargetsCount:"",t.doubleSided?"#define DOUBLE_SIDED":"",t.flipSided?"#define FLIP_SIDED":"",t.shadowMapEnabled?"#define USE_SHADOWMAP":"",t.shadowMapEnabled?"#define "+c:"",t.sizeAttenuation?"#define USE_SIZEATTENUATION":"",t.numLightProbes>0?"#define USE_LIGHT_PROBES":"",t.logarithmicDepthBuffer?"#define USE_LOGDEPTHBUF":"",t.reverseDepthBuffer?"#define USE_REVERSEDEPTHBUF":"","uniform mat4 modelMatrix;","uniform mat4 modelViewMatrix;","uniform mat4 projectionMatrix;","uniform mat4 viewMatrix;","uniform mat3 normalMatrix;","uniform vec3 cameraPosition;","uniform bool isOrthographic;","#ifdef USE_INSTANCING","	attribute mat4 instanceMatrix;","#endif","#ifdef USE_INSTANCING_COLOR","	attribute vec3 instanceColor;","#endif","#ifdef USE_INSTANCING_MORPH","	uniform sampler2D morphTexture;","#endif","attribute vec3 position;","attribute vec3 normal;","attribute vec2 uv;","#ifdef USE_UV1","	attribute vec2 uv1;","#endif","#ifdef USE_UV2","	attribute vec2 uv2;","#endif","#ifdef USE_UV3","	attribute vec2 uv3;","#endif","#ifdef USE_TANGENT","	attribute vec4 tangent;","#endif","#if defined( USE_COLOR_ALPHA )","	attribute vec4 color;","#elif defined( USE_COLOR )","	attribute vec3 color;","#endif","#ifdef USE_SKINNING","	attribute vec4 skinIndex;","	attribute vec4 skinWeight;","#endif",`
`].filter(Yi).join(`
`),u=[lc(t),"#define SHADER_TYPE "+t.shaderType,"#define SHADER_NAME "+t.shaderName,g,t.useFog&&t.fog?"#define USE_FOG":"",t.useFog&&t.fogExp2?"#define FOG_EXP2":"",t.alphaToCoverage?"#define ALPHA_TO_COVERAGE":"",t.map?"#define USE_MAP":"",t.matcap?"#define USE_MATCAP":"",t.envMap?"#define USE_ENVMAP":"",t.envMap?"#define "+l:"",t.envMap?"#define "+d:"",t.envMap?"#define "+h:"",f?"#define CUBEUV_TEXEL_WIDTH "+f.texelWidth:"",f?"#define CUBEUV_TEXEL_HEIGHT "+f.texelHeight:"",f?"#define CUBEUV_MAX_MIP "+f.maxMip+".0":"",t.lightMap?"#define USE_LIGHTMAP":"",t.aoMap?"#define USE_AOMAP":"",t.bumpMap?"#define USE_BUMPMAP":"",t.normalMap?"#define USE_NORMALMAP":"",t.normalMapObjectSpace?"#define USE_NORMALMAP_OBJECTSPACE":"",t.normalMapTangentSpace?"#define USE_NORMALMAP_TANGENTSPACE":"",t.emissiveMap?"#define USE_EMISSIVEMAP":"",t.anisotropy?"#define USE_ANISOTROPY":"",t.anisotropyMap?"#define USE_ANISOTROPYMAP":"",t.clearcoat?"#define USE_CLEARCOAT":"",t.clearcoatMap?"#define USE_CLEARCOATMAP":"",t.clearcoatRoughnessMap?"#define USE_CLEARCOAT_ROUGHNESSMAP":"",t.clearcoatNormalMap?"#define USE_CLEARCOAT_NORMALMAP":"",t.dispersion?"#define USE_DISPERSION":"",t.iridescence?"#define USE_IRIDESCENCE":"",t.iridescenceMap?"#define USE_IRIDESCENCEMAP":"",t.iridescenceThicknessMap?"#define USE_IRIDESCENCE_THICKNESSMAP":"",t.specularMap?"#define USE_SPECULARMAP":"",t.specularColorMap?"#define USE_SPECULAR_COLORMAP":"",t.specularIntensityMap?"#define USE_SPECULAR_INTENSITYMAP":"",t.roughnessMap?"#define USE_ROUGHNESSMAP":"",t.metalnessMap?"#define USE_METALNESSMAP":"",t.alphaMap?"#define USE_ALPHAMAP":"",t.alphaTest?"#define USE_ALPHATEST":"",t.alphaHash?"#define USE_ALPHAHASH":"",t.sheen?"#define USE_SHEEN":"",t.sheenColorMap?"#define USE_SHEEN_COLORMAP":"",t.sheenRoughnessMap?"#define USE_SHEEN_ROUGHNESSMAP":"",t.transmission?"#define USE_TRANSMISSION":"",t.transmissionMap?"#define USE_TRANSMISSIONMAP":"",t.thicknessMap?"#define USE_THICKNESSMAP":"",t.vertexTangents&&t.flatShading===!1?"#define USE_TANGENT":"",t.vertexColors||t.instancingColor||t.batchingColor?"#define USE_COLOR":"",t.vertexAlphas?"#define USE_COLOR_ALPHA":"",t.vertexUv1s?"#define USE_UV1":"",t.vertexUv2s?"#define USE_UV2":"",t.vertexUv3s?"#define USE_UV3":"",t.pointsUvs?"#define USE_POINTS_UV":"",t.gradientMap?"#define USE_GRADIENTMAP":"",t.flatShading?"#define FLAT_SHADED":"",t.doubleSided?"#define DOUBLE_SIDED":"",t.flipSided?"#define FLIP_SIDED":"",t.shadowMapEnabled?"#define USE_SHADOWMAP":"",t.shadowMapEnabled?"#define "+c:"",t.premultipliedAlpha?"#define PREMULTIPLIED_ALPHA":"",t.numLightProbes>0?"#define USE_LIGHT_PROBES":"",t.decodeVideoTexture?"#define DECODE_VIDEO_TEXTURE":"",t.decodeVideoTextureEmissive?"#define DECODE_VIDEO_TEXTURE_EMISSIVE":"",t.logarithmicDepthBuffer?"#define USE_LOGDEPTHBUF":"",t.reverseDepthBuffer?"#define USE_REVERSEDEPTHBUF":"","uniform mat4 viewMatrix;","uniform vec3 cameraPosition;","uniform bool isOrthographic;",t.toneMapping!==Cn?"#define TONE_MAPPING":"",t.toneMapping!==Cn?Ge.tonemapping_pars_fragment:"",t.toneMapping!==Cn?kp("toneMapping",t.toneMapping):"",t.dithering?"#define DITHERING":"",t.opaque?"#define OPAQUE":"",Ge.colorspace_pars_fragment,Fp("linearToOutputTexel",t.outputColorSpace),Op(),t.useDepthPacking?"#define DEPTH_PACKING "+t.depthPacking:"",`
`].filter(Yi).join(`
`)),a=Aa(a),a=ac(a,t),a=oc(a,t),o=Aa(o),o=ac(o,t),o=oc(o,t),a=cc(a),o=cc(o),t.isRawShaderMaterial!==!0&&(E=`#version 300 es
`,p=[m,"#define attribute in","#define varying out","#define texture2D texture"].join(`
`)+`
`+p,u=["#define varying in",t.glslVersion===mo?"":"layout(location = 0) out highp vec4 pc_fragColor;",t.glslVersion===mo?"":"#define gl_FragColor pc_fragColor","#define gl_FragDepthEXT gl_FragDepth","#define texture2D texture","#define textureCube texture","#define texture2DProj textureProj","#define texture2DLodEXT textureLod","#define texture2DProjLodEXT textureProjLod","#define textureCubeLodEXT textureLod","#define texture2DGradEXT textureGrad","#define texture2DProjGradEXT textureProjGrad","#define textureCubeGradEXT textureGrad"].join(`
`)+`
`+u);const y=E+p+a,M=E+u+o,D=ic(r,r.VERTEX_SHADER,y),w=ic(r,r.FRAGMENT_SHADER,M);r.attachShader(_,D),r.attachShader(_,w),t.index0AttributeName!==void 0?r.bindAttribLocation(_,0,t.index0AttributeName):t.morphTargets===!0&&r.bindAttribLocation(_,0,"position"),r.linkProgram(_);function b(P){if(n.debug.checkShaderErrors){const U=r.getProgramInfoLog(_).trim(),A=r.getShaderInfoLog(D).trim(),R=r.getShaderInfoLog(w).trim();let z=!0,N=!0;if(r.getProgramParameter(_,r.LINK_STATUS)===!1)if(z=!1,typeof n.debug.onShaderError=="function")n.debug.onShaderError(r,_,D,w);else{const O=sc(r,D,"vertex"),F=sc(r,w,"fragment");console.error("THREE.WebGLProgram: Shader Error "+r.getError()+" - VALIDATE_STATUS "+r.getProgramParameter(_,r.VALIDATE_STATUS)+`

Material Name: `+P.name+`
Material Type: `+P.type+`

Program Info Log: `+U+`
`+O+`
`+F)}else U!==""?console.warn("THREE.WebGLProgram: Program Info Log:",U):(A===""||R==="")&&(N=!1);N&&(P.diagnostics={runnable:z,programLog:U,vertexShader:{log:A,prefix:p},fragmentShader:{log:R,prefix:u}})}r.deleteShader(D),r.deleteShader(w),C=new Vr(r,_),v=Hp(r,_)}let C;this.getUniforms=function(){return C===void 0&&b(this),C};let v;this.getAttributes=function(){return v===void 0&&b(this),v};let x=t.rendererExtensionParallelShaderCompile===!1;return this.isReady=function(){return x===!1&&(x=r.getProgramParameter(_,Ip)),x},this.destroy=function(){i.releaseStatesOfProgram(this),r.deleteProgram(_),this.program=void 0},this.type=t.shaderType,this.name=t.shaderName,this.id=Up++,this.cacheKey=e,this.usedTimes=1,this.program=_,this.vertexShader=D,this.fragmentShader=w,this}let em=0;class tm{constructor(){this.shaderCache=new Map,this.materialCache=new Map}update(e){const t=e.vertexShader,i=e.fragmentShader,r=this._getShaderStage(t),s=this._getShaderStage(i),a=this._getShaderCacheForMaterial(e);return a.has(r)===!1&&(a.add(r),r.usedTimes++),a.has(s)===!1&&(a.add(s),s.usedTimes++),this}remove(e){const t=this.materialCache.get(e);for(const i of t)i.usedTimes--,i.usedTimes===0&&this.shaderCache.delete(i.code);return this.materialCache.delete(e),this}getVertexShaderID(e){return this._getShaderStage(e.vertexShader).id}getFragmentShaderID(e){return this._getShaderStage(e.fragmentShader).id}dispose(){this.shaderCache.clear(),this.materialCache.clear()}_getShaderCacheForMaterial(e){const t=this.materialCache;let i=t.get(e);return i===void 0&&(i=new Set,t.set(e,i)),i}_getShaderStage(e){const t=this.shaderCache;let i=t.get(e);return i===void 0&&(i=new nm(e),t.set(e,i)),i}}class nm{constructor(e){this.id=em++,this.code=e,this.usedTimes=0}}function im(n,e,t,i,r,s,a){const o=new Va,c=new tm,l=new Set,d=[],h=r.logarithmicDepthBuffer,f=r.vertexTextures;let m=r.precision;const g={MeshDepthMaterial:"depth",MeshDistanceMaterial:"distanceRGBA",MeshNormalMaterial:"normal",MeshBasicMaterial:"basic",MeshLambertMaterial:"lambert",MeshPhongMaterial:"phong",MeshToonMaterial:"toon",MeshStandardMaterial:"physical",MeshPhysicalMaterial:"physical",MeshMatcapMaterial:"matcap",LineBasicMaterial:"basic",LineDashedMaterial:"dashed",PointsMaterial:"points",ShadowMaterial:"shadow",SpriteMaterial:"sprite"};function _(v){return l.add(v),v===0?"uv":`uv${v}`}function p(v,x,P,U,A){const R=U.fog,z=A.geometry,N=v.isMeshStandardMaterial?U.environment:null,O=(v.isMeshStandardMaterial?t:e).get(v.envMap||N),F=O&&O.mapping===Kr?O.image.height:null,G=g[v.type];v.precision!==null&&(m=r.getMaxPrecision(v.precision),m!==v.precision&&console.warn("THREE.WebGLProgram.getParameters:",v.precision,"not supported, using",m,"instead."));const Z=z.morphAttributes.position||z.morphAttributes.normal||z.morphAttributes.color,Y=Z!==void 0?Z.length:0;let he=0;z.morphAttributes.position!==void 0&&(he=1),z.morphAttributes.normal!==void 0&&(he=2),z.morphAttributes.color!==void 0&&(he=3);let Ie,X,ee,ue;if(G){const tt=$t[G];Ie=tt.vertexShader,X=tt.fragmentShader}else Ie=v.vertexShader,X=v.fragmentShader,c.update(v),ee=c.getVertexShaderID(v),ue=c.getFragmentShaderID(v);const re=n.getRenderTarget(),le=n.state.buffers.depth.getReversed(),Pe=A.isInstancedMesh===!0,me=A.isBatchedMesh===!0,te=!!v.map,se=!!v.matcap,K=!!O,I=!!v.aoMap,Ce=!!v.lightMap,Se=!!v.bumpMap,_e=!!v.normalMap,ve=!!v.displacementMap,Ne=!!v.emissiveMap,we=!!v.metalnessMap,L=!!v.roughnessMap,S=v.anisotropy>0,j=v.clearcoat>0,Q=v.dispersion>0,ie=v.iridescence>0,J=v.sheen>0,Re=v.transmission>0,ge=S&&!!v.anisotropyMap,ye=j&&!!v.clearcoatMap,Ye=j&&!!v.clearcoatNormalMap,ce=j&&!!v.clearcoatRoughnessMap,be=ie&&!!v.iridescenceMap,ze=ie&&!!v.iridescenceThicknessMap,Fe=J&&!!v.sheenColorMap,Te=J&&!!v.sheenRoughnessMap,qe=!!v.specularMap,He=!!v.specularColorMap,st=!!v.specularIntensityMap,B=Re&&!!v.transmissionMap,fe=Re&&!!v.thicknessMap,$=!!v.gradientMap,ne=!!v.alphaMap,Me=v.alphaTest>0,xe=!!v.alphaHash,Be=!!v.extensions;let lt=Cn;v.toneMapped&&(re===null||re.isXRRenderTarget===!0)&&(lt=n.toneMapping);const Et={shaderID:G,shaderType:v.type,shaderName:v.name,vertexShader:Ie,fragmentShader:X,defines:v.defines,customVertexShaderID:ee,customFragmentShaderID:ue,isRawShaderMaterial:v.isRawShaderMaterial===!0,glslVersion:v.glslVersion,precision:m,batching:me,batchingColor:me&&A._colorsTexture!==null,instancing:Pe,instancingColor:Pe&&A.instanceColor!==null,instancingMorph:Pe&&A.morphTexture!==null,supportsVertexTextures:f,outputColorSpace:re===null?n.outputColorSpace:re.isXRRenderTarget===!0?re.texture.colorSpace:Ii,alphaToCoverage:!!v.alphaToCoverage,map:te,matcap:se,envMap:K,envMapMode:K&&O.mapping,envMapCubeUVHeight:F,aoMap:I,lightMap:Ce,bumpMap:Se,normalMap:_e,displacementMap:f&&ve,emissiveMap:Ne,normalMapObjectSpace:_e&&v.normalMapType===Yl,normalMapTangentSpace:_e&&v.normalMapType===Bc,metalnessMap:we,roughnessMap:L,anisotropy:S,anisotropyMap:ge,clearcoat:j,clearcoatMap:ye,clearcoatNormalMap:Ye,clearcoatRoughnessMap:ce,dispersion:Q,iridescence:ie,iridescenceMap:be,iridescenceThicknessMap:ze,sheen:J,sheenColorMap:Fe,sheenRoughnessMap:Te,specularMap:qe,specularColorMap:He,specularIntensityMap:st,transmission:Re,transmissionMap:B,thicknessMap:fe,gradientMap:$,opaque:v.transparent===!1&&v.blending===Ti&&v.alphaToCoverage===!1,alphaMap:ne,alphaTest:Me,alphaHash:xe,combine:v.combine,mapUv:te&&_(v.map.channel),aoMapUv:I&&_(v.aoMap.channel),lightMapUv:Ce&&_(v.lightMap.channel),bumpMapUv:Se&&_(v.bumpMap.channel),normalMapUv:_e&&_(v.normalMap.channel),displacementMapUv:ve&&_(v.displacementMap.channel),emissiveMapUv:Ne&&_(v.emissiveMap.channel),metalnessMapUv:we&&_(v.metalnessMap.channel),roughnessMapUv:L&&_(v.roughnessMap.channel),anisotropyMapUv:ge&&_(v.anisotropyMap.channel),clearcoatMapUv:ye&&_(v.clearcoatMap.channel),clearcoatNormalMapUv:Ye&&_(v.clearcoatNormalMap.channel),clearcoatRoughnessMapUv:ce&&_(v.clearcoatRoughnessMap.channel),iridescenceMapUv:be&&_(v.iridescenceMap.channel),iridescenceThicknessMapUv:ze&&_(v.iridescenceThicknessMap.channel),sheenColorMapUv:Fe&&_(v.sheenColorMap.channel),sheenRoughnessMapUv:Te&&_(v.sheenRoughnessMap.channel),specularMapUv:qe&&_(v.specularMap.channel),specularColorMapUv:He&&_(v.specularColorMap.channel),specularIntensityMapUv:st&&_(v.specularIntensityMap.channel),transmissionMapUv:B&&_(v.transmissionMap.channel),thicknessMapUv:fe&&_(v.thicknessMap.channel),alphaMapUv:ne&&_(v.alphaMap.channel),vertexTangents:!!z.attributes.tangent&&(_e||S),vertexColors:v.vertexColors,vertexAlphas:v.vertexColors===!0&&!!z.attributes.color&&z.attributes.color.itemSize===4,pointsUvs:A.isPoints===!0&&!!z.attributes.uv&&(te||ne),fog:!!R,useFog:v.fog===!0,fogExp2:!!R&&R.isFogExp2,flatShading:v.flatShading===!0,sizeAttenuation:v.sizeAttenuation===!0,logarithmicDepthBuffer:h,reverseDepthBuffer:le,skinning:A.isSkinnedMesh===!0,morphTargets:z.morphAttributes.position!==void 0,morphNormals:z.morphAttributes.normal!==void 0,morphColors:z.morphAttributes.color!==void 0,morphTargetsCount:Y,morphTextureStride:he,numDirLights:x.directional.length,numPointLights:x.point.length,numSpotLights:x.spot.length,numSpotLightMaps:x.spotLightMap.length,numRectAreaLights:x.rectArea.length,numHemiLights:x.hemi.length,numDirLightShadows:x.directionalShadowMap.length,numPointLightShadows:x.pointShadowMap.length,numSpotLightShadows:x.spotShadowMap.length,numSpotLightShadowsWithMaps:x.numSpotLightShadowsWithMaps,numLightProbes:x.numLightProbes,numClippingPlanes:a.numPlanes,numClipIntersection:a.numIntersection,dithering:v.dithering,shadowMapEnabled:n.shadowMap.enabled&&P.length>0,shadowMapType:n.shadowMap.type,toneMapping:lt,decodeVideoTexture:te&&v.map.isVideoTexture===!0&&Je.getTransfer(v.map.colorSpace)===it,decodeVideoTextureEmissive:Ne&&v.emissiveMap.isVideoTexture===!0&&Je.getTransfer(v.emissiveMap.colorSpace)===it,premultipliedAlpha:v.premultipliedAlpha,doubleSided:v.side===Tt,flipSided:v.side===Ct,useDepthPacking:v.depthPacking>=0,depthPacking:v.depthPacking||0,index0AttributeName:v.index0AttributeName,extensionClipCullDistance:Be&&v.extensions.clipCullDistance===!0&&i.has("WEBGL_clip_cull_distance"),extensionMultiDraw:(Be&&v.extensions.multiDraw===!0||me)&&i.has("WEBGL_multi_draw"),rendererExtensionParallelShaderCompile:i.has("KHR_parallel_shader_compile"),customProgramCacheKey:v.customProgramCacheKey()};return Et.vertexUv1s=l.has(1),Et.vertexUv2s=l.has(2),Et.vertexUv3s=l.has(3),l.clear(),Et}function u(v){const x=[];if(v.shaderID?x.push(v.shaderID):(x.push(v.customVertexShaderID),x.push(v.customFragmentShaderID)),v.defines!==void 0)for(const P in v.defines)x.push(P),x.push(v.defines[P]);return v.isRawShaderMaterial===!1&&(E(x,v),y(x,v),x.push(n.outputColorSpace)),x.push(v.customProgramCacheKey),x.join()}function E(v,x){v.push(x.precision),v.push(x.outputColorSpace),v.push(x.envMapMode),v.push(x.envMapCubeUVHeight),v.push(x.mapUv),v.push(x.alphaMapUv),v.push(x.lightMapUv),v.push(x.aoMapUv),v.push(x.bumpMapUv),v.push(x.normalMapUv),v.push(x.displacementMapUv),v.push(x.emissiveMapUv),v.push(x.metalnessMapUv),v.push(x.roughnessMapUv),v.push(x.anisotropyMapUv),v.push(x.clearcoatMapUv),v.push(x.clearcoatNormalMapUv),v.push(x.clearcoatRoughnessMapUv),v.push(x.iridescenceMapUv),v.push(x.iridescenceThicknessMapUv),v.push(x.sheenColorMapUv),v.push(x.sheenRoughnessMapUv),v.push(x.specularMapUv),v.push(x.specularColorMapUv),v.push(x.specularIntensityMapUv),v.push(x.transmissionMapUv),v.push(x.thicknessMapUv),v.push(x.combine),v.push(x.fogExp2),v.push(x.sizeAttenuation),v.push(x.morphTargetsCount),v.push(x.morphAttributeCount),v.push(x.numDirLights),v.push(x.numPointLights),v.push(x.numSpotLights),v.push(x.numSpotLightMaps),v.push(x.numHemiLights),v.push(x.numRectAreaLights),v.push(x.numDirLightShadows),v.push(x.numPointLightShadows),v.push(x.numSpotLightShadows),v.push(x.numSpotLightShadowsWithMaps),v.push(x.numLightProbes),v.push(x.shadowMapType),v.push(x.toneMapping),v.push(x.numClippingPlanes),v.push(x.numClipIntersection),v.push(x.depthPacking)}function y(v,x){o.disableAll(),x.supportsVertexTextures&&o.enable(0),x.instancing&&o.enable(1),x.instancingColor&&o.enable(2),x.instancingMorph&&o.enable(3),x.matcap&&o.enable(4),x.envMap&&o.enable(5),x.normalMapObjectSpace&&o.enable(6),x.normalMapTangentSpace&&o.enable(7),x.clearcoat&&o.enable(8),x.iridescence&&o.enable(9),x.alphaTest&&o.enable(10),x.vertexColors&&o.enable(11),x.vertexAlphas&&o.enable(12),x.vertexUv1s&&o.enable(13),x.vertexUv2s&&o.enable(14),x.vertexUv3s&&o.enable(15),x.vertexTangents&&o.enable(16),x.anisotropy&&o.enable(17),x.alphaHash&&o.enable(18),x.batching&&o.enable(19),x.dispersion&&o.enable(20),x.batchingColor&&o.enable(21),v.push(o.mask),o.disableAll(),x.fog&&o.enable(0),x.useFog&&o.enable(1),x.flatShading&&o.enable(2),x.logarithmicDepthBuffer&&o.enable(3),x.reverseDepthBuffer&&o.enable(4),x.skinning&&o.enable(5),x.morphTargets&&o.enable(6),x.morphNormals&&o.enable(7),x.morphColors&&o.enable(8),x.premultipliedAlpha&&o.enable(9),x.shadowMapEnabled&&o.enable(10),x.doubleSided&&o.enable(11),x.flipSided&&o.enable(12),x.useDepthPacking&&o.enable(13),x.dithering&&o.enable(14),x.transmission&&o.enable(15),x.sheen&&o.enable(16),x.opaque&&o.enable(17),x.pointsUvs&&o.enable(18),x.decodeVideoTexture&&o.enable(19),x.decodeVideoTextureEmissive&&o.enable(20),x.alphaToCoverage&&o.enable(21),v.push(o.mask)}function M(v){const x=g[v.type];let P;if(x){const U=$t[x];P=Au.clone(U.uniforms)}else P=v.uniforms;return P}function D(v,x){let P;for(let U=0,A=d.length;U<A;U++){const R=d[U];if(R.cacheKey===x){P=R,++P.usedTimes;break}}return P===void 0&&(P=new Qp(n,x,v,s),d.push(P)),P}function w(v){if(--v.usedTimes===0){const x=d.indexOf(v);d[x]=d[d.length-1],d.pop(),v.destroy()}}function b(v){c.remove(v)}function C(){c.dispose()}return{getParameters:p,getProgramCacheKey:u,getUniforms:M,acquireProgram:D,releaseProgram:w,releaseShaderCache:b,programs:d,dispose:C}}function rm(){let n=new WeakMap;function e(a){return n.has(a)}function t(a){let o=n.get(a);return o===void 0&&(o={},n.set(a,o)),o}function i(a){n.delete(a)}function r(a,o,c){n.get(a)[o]=c}function s(){n=new WeakMap}return{has:e,get:t,remove:i,update:r,dispose:s}}function sm(n,e){return n.groupOrder!==e.groupOrder?n.groupOrder-e.groupOrder:n.renderOrder!==e.renderOrder?n.renderOrder-e.renderOrder:n.material.id!==e.material.id?n.material.id-e.material.id:n.z!==e.z?n.z-e.z:n.id-e.id}function uc(n,e){return n.groupOrder!==e.groupOrder?n.groupOrder-e.groupOrder:n.renderOrder!==e.renderOrder?n.renderOrder-e.renderOrder:n.z!==e.z?e.z-n.z:n.id-e.id}function dc(){const n=[];let e=0;const t=[],i=[],r=[];function s(){e=0,t.length=0,i.length=0,r.length=0}function a(h,f,m,g,_,p){let u=n[e];return u===void 0?(u={id:h.id,object:h,geometry:f,material:m,groupOrder:g,renderOrder:h.renderOrder,z:_,group:p},n[e]=u):(u.id=h.id,u.object=h,u.geometry=f,u.material=m,u.groupOrder=g,u.renderOrder=h.renderOrder,u.z=_,u.group=p),e++,u}function o(h,f,m,g,_,p){const u=a(h,f,m,g,_,p);m.transmission>0?i.push(u):m.transparent===!0?r.push(u):t.push(u)}function c(h,f,m,g,_,p){const u=a(h,f,m,g,_,p);m.transmission>0?i.unshift(u):m.transparent===!0?r.unshift(u):t.unshift(u)}function l(h,f){t.length>1&&t.sort(h||sm),i.length>1&&i.sort(f||uc),r.length>1&&r.sort(f||uc)}function d(){for(let h=e,f=n.length;h<f;h++){const m=n[h];if(m.id===null)break;m.id=null,m.object=null,m.geometry=null,m.material=null,m.group=null}}return{opaque:t,transmissive:i,transparent:r,init:s,push:o,unshift:c,finish:d,sort:l}}function am(){let n=new WeakMap;function e(i,r){const s=n.get(i);let a;return s===void 0?(a=new dc,n.set(i,[a])):r>=s.length?(a=new dc,s.push(a)):a=s[r],a}function t(){n=new WeakMap}return{get:e,dispose:t}}function om(){const n={};return{get:function(e){if(n[e.id]!==void 0)return n[e.id];let t;switch(e.type){case"DirectionalLight":t={direction:new k,color:new oe};break;case"SpotLight":t={position:new k,direction:new k,color:new oe,distance:0,coneCos:0,penumbraCos:0,decay:0};break;case"PointLight":t={position:new k,color:new oe,distance:0,decay:0};break;case"HemisphereLight":t={direction:new k,skyColor:new oe,groundColor:new oe};break;case"RectAreaLight":t={color:new oe,position:new k,halfWidth:new k,halfHeight:new k};break}return n[e.id]=t,t}}}function cm(){const n={};return{get:function(e){if(n[e.id]!==void 0)return n[e.id];let t;switch(e.type){case"DirectionalLight":t={shadowIntensity:1,shadowBias:0,shadowNormalBias:0,shadowRadius:1,shadowMapSize:new We};break;case"SpotLight":t={shadowIntensity:1,shadowBias:0,shadowNormalBias:0,shadowRadius:1,shadowMapSize:new We};break;case"PointLight":t={shadowIntensity:1,shadowBias:0,shadowNormalBias:0,shadowRadius:1,shadowMapSize:new We,shadowCameraNear:1,shadowCameraFar:1e3};break}return n[e.id]=t,t}}}let lm=0;function um(n,e){return(e.castShadow?2:0)-(n.castShadow?2:0)+(e.map?1:0)-(n.map?1:0)}function dm(n){const e=new om,t=cm(),i={version:0,hash:{directionalLength:-1,pointLength:-1,spotLength:-1,rectAreaLength:-1,hemiLength:-1,numDirectionalShadows:-1,numPointShadows:-1,numSpotShadows:-1,numSpotMaps:-1,numLightProbes:-1},ambient:[0,0,0],probe:[],directional:[],directionalShadow:[],directionalShadowMap:[],directionalShadowMatrix:[],spot:[],spotLightMap:[],spotShadow:[],spotShadowMap:[],spotLightMatrix:[],rectArea:[],rectAreaLTC1:null,rectAreaLTC2:null,point:[],pointShadow:[],pointShadowMap:[],pointShadowMatrix:[],hemi:[],numSpotLightShadowsWithMaps:0,numLightProbes:0};for(let l=0;l<9;l++)i.probe.push(new k);const r=new k,s=new at,a=new at;function o(l){let d=0,h=0,f=0;for(let v=0;v<9;v++)i.probe[v].set(0,0,0);let m=0,g=0,_=0,p=0,u=0,E=0,y=0,M=0,D=0,w=0,b=0;l.sort(um);for(let v=0,x=l.length;v<x;v++){const P=l[v],U=P.color,A=P.intensity,R=P.distance,z=P.shadow&&P.shadow.map?P.shadow.map.texture:null;if(P.isAmbientLight)d+=U.r*A,h+=U.g*A,f+=U.b*A;else if(P.isLightProbe){for(let N=0;N<9;N++)i.probe[N].addScaledVector(P.sh.coefficients[N],A);b++}else if(P.isDirectionalLight){const N=e.get(P);if(N.color.copy(P.color).multiplyScalar(P.intensity),P.castShadow){const O=P.shadow,F=t.get(P);F.shadowIntensity=O.intensity,F.shadowBias=O.bias,F.shadowNormalBias=O.normalBias,F.shadowRadius=O.radius,F.shadowMapSize=O.mapSize,i.directionalShadow[m]=F,i.directionalShadowMap[m]=z,i.directionalShadowMatrix[m]=P.shadow.matrix,E++}i.directional[m]=N,m++}else if(P.isSpotLight){const N=e.get(P);N.position.setFromMatrixPosition(P.matrixWorld),N.color.copy(U).multiplyScalar(A),N.distance=R,N.coneCos=Math.cos(P.angle),N.penumbraCos=Math.cos(P.angle*(1-P.penumbra)),N.decay=P.decay,i.spot[_]=N;const O=P.shadow;if(P.map&&(i.spotLightMap[D]=P.map,D++,O.updateMatrices(P),P.castShadow&&w++),i.spotLightMatrix[_]=O.matrix,P.castShadow){const F=t.get(P);F.shadowIntensity=O.intensity,F.shadowBias=O.bias,F.shadowNormalBias=O.normalBias,F.shadowRadius=O.radius,F.shadowMapSize=O.mapSize,i.spotShadow[_]=F,i.spotShadowMap[_]=z,M++}_++}else if(P.isRectAreaLight){const N=e.get(P);N.color.copy(U).multiplyScalar(A),N.halfWidth.set(P.width*.5,0,0),N.halfHeight.set(0,P.height*.5,0),i.rectArea[p]=N,p++}else if(P.isPointLight){const N=e.get(P);if(N.color.copy(P.color).multiplyScalar(P.intensity),N.distance=P.distance,N.decay=P.decay,P.castShadow){const O=P.shadow,F=t.get(P);F.shadowIntensity=O.intensity,F.shadowBias=O.bias,F.shadowNormalBias=O.normalBias,F.shadowRadius=O.radius,F.shadowMapSize=O.mapSize,F.shadowCameraNear=O.camera.near,F.shadowCameraFar=O.camera.far,i.pointShadow[g]=F,i.pointShadowMap[g]=z,i.pointShadowMatrix[g]=P.shadow.matrix,y++}i.point[g]=N,g++}else if(P.isHemisphereLight){const N=e.get(P);N.skyColor.copy(P.color).multiplyScalar(A),N.groundColor.copy(P.groundColor).multiplyScalar(A),i.hemi[u]=N,u++}}p>0&&(n.has("OES_texture_float_linear")===!0?(i.rectAreaLTC1=de.LTC_FLOAT_1,i.rectAreaLTC2=de.LTC_FLOAT_2):(i.rectAreaLTC1=de.LTC_HALF_1,i.rectAreaLTC2=de.LTC_HALF_2)),i.ambient[0]=d,i.ambient[1]=h,i.ambient[2]=f;const C=i.hash;(C.directionalLength!==m||C.pointLength!==g||C.spotLength!==_||C.rectAreaLength!==p||C.hemiLength!==u||C.numDirectionalShadows!==E||C.numPointShadows!==y||C.numSpotShadows!==M||C.numSpotMaps!==D||C.numLightProbes!==b)&&(i.directional.length=m,i.spot.length=_,i.rectArea.length=p,i.point.length=g,i.hemi.length=u,i.directionalShadow.length=E,i.directionalShadowMap.length=E,i.pointShadow.length=y,i.pointShadowMap.length=y,i.spotShadow.length=M,i.spotShadowMap.length=M,i.directionalShadowMatrix.length=E,i.pointShadowMatrix.length=y,i.spotLightMatrix.length=M+D-w,i.spotLightMap.length=D,i.numSpotLightShadowsWithMaps=w,i.numLightProbes=b,C.directionalLength=m,C.pointLength=g,C.spotLength=_,C.rectAreaLength=p,C.hemiLength=u,C.numDirectionalShadows=E,C.numPointShadows=y,C.numSpotShadows=M,C.numSpotMaps=D,C.numLightProbes=b,i.version=lm++)}function c(l,d){let h=0,f=0,m=0,g=0,_=0;const p=d.matrixWorldInverse;for(let u=0,E=l.length;u<E;u++){const y=l[u];if(y.isDirectionalLight){const M=i.directional[h];M.direction.setFromMatrixPosition(y.matrixWorld),r.setFromMatrixPosition(y.target.matrixWorld),M.direction.sub(r),M.direction.transformDirection(p),h++}else if(y.isSpotLight){const M=i.spot[m];M.position.setFromMatrixPosition(y.matrixWorld),M.position.applyMatrix4(p),M.direction.setFromMatrixPosition(y.matrixWorld),r.setFromMatrixPosition(y.target.matrixWorld),M.direction.sub(r),M.direction.transformDirection(p),m++}else if(y.isRectAreaLight){const M=i.rectArea[g];M.position.setFromMatrixPosition(y.matrixWorld),M.position.applyMatrix4(p),a.identity(),s.copy(y.matrixWorld),s.premultiply(p),a.extractRotation(s),M.halfWidth.set(y.width*.5,0,0),M.halfHeight.set(0,y.height*.5,0),M.halfWidth.applyMatrix4(a),M.halfHeight.applyMatrix4(a),g++}else if(y.isPointLight){const M=i.point[f];M.position.setFromMatrixPosition(y.matrixWorld),M.position.applyMatrix4(p),f++}else if(y.isHemisphereLight){const M=i.hemi[_];M.direction.setFromMatrixPosition(y.matrixWorld),M.direction.transformDirection(p),_++}}}return{setup:o,setupView:c,state:i}}function hc(n){const e=new dm(n),t=[],i=[];function r(d){l.camera=d,t.length=0,i.length=0}function s(d){t.push(d)}function a(d){i.push(d)}function o(){e.setup(t)}function c(d){e.setupView(t,d)}const l={lightsArray:t,shadowsArray:i,camera:null,lights:e,transmissionRenderTarget:{}};return{init:r,state:l,setupLights:o,setupLightsView:c,pushLight:s,pushShadow:a}}function hm(n){let e=new WeakMap;function t(r,s=0){const a=e.get(r);let o;return a===void 0?(o=new hc(n),e.set(r,[o])):s>=a.length?(o=new hc(n),a.push(o)):o=a[s],o}function i(){e=new WeakMap}return{get:t,dispose:i}}const fm=`void main() {
	gl_Position = vec4( position, 1.0 );
}`,pm=`uniform sampler2D shadow_pass;
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
}`;function mm(n,e,t){let i=new Ha;const r=new We,s=new We,a=new rt,o=new Nu({depthPacking:Kl}),c=new Fu,l={},d=t.maxTextureSize,h={[Pn]:Ct,[Ct]:Pn,[Tt]:Tt},f=new Dn({defines:{VSM_SAMPLES:8},uniforms:{shadow_pass:{value:null},resolution:{value:new We},radius:{value:4}},vertexShader:fm,fragmentShader:pm}),m=f.clone();m.defines.HORIZONTAL_PASS=1;const g=new Ke;g.setAttribute("position",new Qt(new Float32Array([-1,-1,.5,3,-1,.5,-1,3,.5]),3));const _=new Le(g,f),p=this;this.enabled=!1,this.autoUpdate=!0,this.needsUpdate=!1,this.type=wc;let u=this.type;this.render=function(w,b,C){if(p.enabled===!1||p.autoUpdate===!1&&p.needsUpdate===!1||w.length===0)return;const v=n.getRenderTarget(),x=n.getActiveCubeFace(),P=n.getActiveMipmapLevel(),U=n.state;U.setBlending(Rn),U.buffers.color.setClear(1,1,1,1),U.buffers.depth.setTest(!0),U.setScissorTest(!1);const A=u!==ln&&this.type===ln,R=u===ln&&this.type!==ln;for(let z=0,N=w.length;z<N;z++){const O=w[z],F=O.shadow;if(F===void 0){console.warn("THREE.WebGLShadowMap:",O,"has no shadow.");continue}if(F.autoUpdate===!1&&F.needsUpdate===!1)continue;r.copy(F.mapSize);const G=F.getFrameExtents();if(r.multiply(G),s.copy(F.mapSize),(r.x>d||r.y>d)&&(r.x>d&&(s.x=Math.floor(d/G.x),r.x=s.x*G.x,F.mapSize.x=s.x),r.y>d&&(s.y=Math.floor(d/G.y),r.y=s.y*G.y,F.mapSize.y=s.y)),F.map===null||A===!0||R===!0){const Y=this.type!==ln?{minFilter:kt,magFilter:kt}:{};F.map!==null&&F.map.dispose(),F.map=new ei(r.x,r.y,Y),F.map.texture.name=O.name+".shadowMap",F.camera.updateProjectionMatrix()}n.setRenderTarget(F.map),n.clear();const Z=F.getViewportCount();for(let Y=0;Y<Z;Y++){const he=F.getViewport(Y);a.set(s.x*he.x,s.y*he.y,s.x*he.z,s.y*he.w),U.viewport(a),F.updateMatrices(O,Y),i=F.getFrustum(),M(b,C,F.camera,O,this.type)}F.isPointLightShadow!==!0&&this.type===ln&&E(F,C),F.needsUpdate=!1}u=this.type,p.needsUpdate=!1,n.setRenderTarget(v,x,P)};function E(w,b){const C=e.update(_);f.defines.VSM_SAMPLES!==w.blurSamples&&(f.defines.VSM_SAMPLES=w.blurSamples,m.defines.VSM_SAMPLES=w.blurSamples,f.needsUpdate=!0,m.needsUpdate=!0),w.mapPass===null&&(w.mapPass=new ei(r.x,r.y)),f.uniforms.shadow_pass.value=w.map.texture,f.uniforms.resolution.value=w.mapSize,f.uniforms.radius.value=w.radius,n.setRenderTarget(w.mapPass),n.clear(),n.renderBufferDirect(b,null,C,f,_,null),m.uniforms.shadow_pass.value=w.mapPass.texture,m.uniforms.resolution.value=w.mapSize,m.uniforms.radius.value=w.radius,n.setRenderTarget(w.map),n.clear(),n.renderBufferDirect(b,null,C,m,_,null)}function y(w,b,C,v){let x=null;const P=C.isPointLight===!0?w.customDistanceMaterial:w.customDepthMaterial;if(P!==void 0)x=P;else if(x=C.isPointLight===!0?c:o,n.localClippingEnabled&&b.clipShadows===!0&&Array.isArray(b.clippingPlanes)&&b.clippingPlanes.length!==0||b.displacementMap&&b.displacementScale!==0||b.alphaMap&&b.alphaTest>0||b.map&&b.alphaTest>0){const U=x.uuid,A=b.uuid;let R=l[U];R===void 0&&(R={},l[U]=R);let z=R[A];z===void 0&&(z=x.clone(),R[A]=z,b.addEventListener("dispose",D)),x=z}if(x.visible=b.visible,x.wireframe=b.wireframe,v===ln?x.side=b.shadowSide!==null?b.shadowSide:b.side:x.side=b.shadowSide!==null?b.shadowSide:h[b.side],x.alphaMap=b.alphaMap,x.alphaTest=b.alphaTest,x.map=b.map,x.clipShadows=b.clipShadows,x.clippingPlanes=b.clippingPlanes,x.clipIntersection=b.clipIntersection,x.displacementMap=b.displacementMap,x.displacementScale=b.displacementScale,x.displacementBias=b.displacementBias,x.wireframeLinewidth=b.wireframeLinewidth,x.linewidth=b.linewidth,C.isPointLight===!0&&x.isMeshDistanceMaterial===!0){const U=n.properties.get(x);U.light=C}return x}function M(w,b,C,v,x){if(w.visible===!1)return;if(w.layers.test(b.layers)&&(w.isMesh||w.isLine||w.isPoints)&&(w.castShadow||w.receiveShadow&&x===ln)&&(!w.frustumCulled||i.intersectsObject(w))){w.modelViewMatrix.multiplyMatrices(C.matrixWorldInverse,w.matrixWorld);const A=e.update(w),R=w.material;if(Array.isArray(R)){const z=A.groups;for(let N=0,O=z.length;N<O;N++){const F=z[N],G=R[F.materialIndex];if(G&&G.visible){const Z=y(w,G,v,x);w.onBeforeShadow(n,w,b,C,A,Z,F),n.renderBufferDirect(C,null,A,Z,w,F),w.onAfterShadow(n,w,b,C,A,Z,F)}}}else if(R.visible){const z=y(w,R,v,x);w.onBeforeShadow(n,w,b,C,A,z,null),n.renderBufferDirect(C,null,A,z,w,null),w.onAfterShadow(n,w,b,C,A,z,null)}}const U=w.children;for(let A=0,R=U.length;A<R;A++)M(U[A],b,C,v,x)}function D(w){w.target.removeEventListener("dispose",D);for(const C in l){const v=l[C],x=w.target.uuid;x in v&&(v[x].dispose(),delete v[x])}}}const gm={[Bs]:Vs,[Hs]:Ws,[Gs]:Xs,[Ri]:js,[Vs]:Bs,[Ws]:Hs,[Xs]:Gs,[js]:Ri};function _m(n,e){function t(){let B=!1;const fe=new rt;let $=null;const ne=new rt(0,0,0,0);return{setMask:function(Me){$!==Me&&!B&&(n.colorMask(Me,Me,Me,Me),$=Me)},setLocked:function(Me){B=Me},setClear:function(Me,xe,Be,lt,Et){Et===!0&&(Me*=lt,xe*=lt,Be*=lt),fe.set(Me,xe,Be,lt),ne.equals(fe)===!1&&(n.clearColor(Me,xe,Be,lt),ne.copy(fe))},reset:function(){B=!1,$=null,ne.set(-1,0,0,0)}}}function i(){let B=!1,fe=!1,$=null,ne=null,Me=null;return{setReversed:function(xe){if(fe!==xe){const Be=e.get("EXT_clip_control");fe?Be.clipControlEXT(Be.LOWER_LEFT_EXT,Be.ZERO_TO_ONE_EXT):Be.clipControlEXT(Be.LOWER_LEFT_EXT,Be.NEGATIVE_ONE_TO_ONE_EXT);const lt=Me;Me=null,this.setClear(lt)}fe=xe},getReversed:function(){return fe},setTest:function(xe){xe?re(n.DEPTH_TEST):le(n.DEPTH_TEST)},setMask:function(xe){$!==xe&&!B&&(n.depthMask(xe),$=xe)},setFunc:function(xe){if(fe&&(xe=gm[xe]),ne!==xe){switch(xe){case Bs:n.depthFunc(n.NEVER);break;case Vs:n.depthFunc(n.ALWAYS);break;case Hs:n.depthFunc(n.LESS);break;case Ri:n.depthFunc(n.LEQUAL);break;case Gs:n.depthFunc(n.EQUAL);break;case js:n.depthFunc(n.GEQUAL);break;case Ws:n.depthFunc(n.GREATER);break;case Xs:n.depthFunc(n.NOTEQUAL);break;default:n.depthFunc(n.LEQUAL)}ne=xe}},setLocked:function(xe){B=xe},setClear:function(xe){Me!==xe&&(fe&&(xe=1-xe),n.clearDepth(xe),Me=xe)},reset:function(){B=!1,$=null,ne=null,Me=null,fe=!1}}}function r(){let B=!1,fe=null,$=null,ne=null,Me=null,xe=null,Be=null,lt=null,Et=null;return{setTest:function(tt){B||(tt?re(n.STENCIL_TEST):le(n.STENCIL_TEST))},setMask:function(tt){fe!==tt&&!B&&(n.stencilMask(tt),fe=tt)},setFunc:function(tt,jt,en){($!==tt||ne!==jt||Me!==en)&&(n.stencilFunc(tt,jt,en),$=tt,ne=jt,Me=en)},setOp:function(tt,jt,en){(xe!==tt||Be!==jt||lt!==en)&&(n.stencilOp(tt,jt,en),xe=tt,Be=jt,lt=en)},setLocked:function(tt){B=tt},setClear:function(tt){Et!==tt&&(n.clearStencil(tt),Et=tt)},reset:function(){B=!1,fe=null,$=null,ne=null,Me=null,xe=null,Be=null,lt=null,Et=null}}}const s=new t,a=new i,o=new r,c=new WeakMap,l=new WeakMap;let d={},h={},f=new WeakMap,m=[],g=null,_=!1,p=null,u=null,E=null,y=null,M=null,D=null,w=null,b=new oe(0,0,0),C=0,v=!1,x=null,P=null,U=null,A=null,R=null;const z=n.getParameter(n.MAX_COMBINED_TEXTURE_IMAGE_UNITS);let N=!1,O=0;const F=n.getParameter(n.VERSION);F.indexOf("WebGL")!==-1?(O=parseFloat(/^WebGL (\d)/.exec(F)[1]),N=O>=1):F.indexOf("OpenGL ES")!==-1&&(O=parseFloat(/^OpenGL ES (\d)/.exec(F)[1]),N=O>=2);let G=null,Z={};const Y=n.getParameter(n.SCISSOR_BOX),he=n.getParameter(n.VIEWPORT),Ie=new rt().fromArray(Y),X=new rt().fromArray(he);function ee(B,fe,$,ne){const Me=new Uint8Array(4),xe=n.createTexture();n.bindTexture(B,xe),n.texParameteri(B,n.TEXTURE_MIN_FILTER,n.NEAREST),n.texParameteri(B,n.TEXTURE_MAG_FILTER,n.NEAREST);for(let Be=0;Be<$;Be++)B===n.TEXTURE_3D||B===n.TEXTURE_2D_ARRAY?n.texImage3D(fe,0,n.RGBA,1,1,ne,0,n.RGBA,n.UNSIGNED_BYTE,Me):n.texImage2D(fe+Be,0,n.RGBA,1,1,0,n.RGBA,n.UNSIGNED_BYTE,Me);return xe}const ue={};ue[n.TEXTURE_2D]=ee(n.TEXTURE_2D,n.TEXTURE_2D,1),ue[n.TEXTURE_CUBE_MAP]=ee(n.TEXTURE_CUBE_MAP,n.TEXTURE_CUBE_MAP_POSITIVE_X,6),ue[n.TEXTURE_2D_ARRAY]=ee(n.TEXTURE_2D_ARRAY,n.TEXTURE_2D_ARRAY,1,1),ue[n.TEXTURE_3D]=ee(n.TEXTURE_3D,n.TEXTURE_3D,1,1),s.setClear(0,0,0,1),a.setClear(1),o.setClear(0),re(n.DEPTH_TEST),a.setFunc(Ri),Se(!1),_e(co),re(n.CULL_FACE),I(Rn);function re(B){d[B]!==!0&&(n.enable(B),d[B]=!0)}function le(B){d[B]!==!1&&(n.disable(B),d[B]=!1)}function Pe(B,fe){return h[B]!==fe?(n.bindFramebuffer(B,fe),h[B]=fe,B===n.DRAW_FRAMEBUFFER&&(h[n.FRAMEBUFFER]=fe),B===n.FRAMEBUFFER&&(h[n.DRAW_FRAMEBUFFER]=fe),!0):!1}function me(B,fe){let $=m,ne=!1;if(B){$=f.get(fe),$===void 0&&($=[],f.set(fe,$));const Me=B.textures;if($.length!==Me.length||$[0]!==n.COLOR_ATTACHMENT0){for(let xe=0,Be=Me.length;xe<Be;xe++)$[xe]=n.COLOR_ATTACHMENT0+xe;$.length=Me.length,ne=!0}}else $[0]!==n.BACK&&($[0]=n.BACK,ne=!0);ne&&n.drawBuffers($)}function te(B){return g!==B?(n.useProgram(B),g=B,!0):!1}const se={[Xn]:n.FUNC_ADD,[Ml]:n.FUNC_SUBTRACT,[Sl]:n.FUNC_REVERSE_SUBTRACT};se[El]=n.MIN,se[yl]=n.MAX;const K={[bl]:n.ZERO,[Tl]:n.ONE,[Al]:n.SRC_COLOR,[ks]:n.SRC_ALPHA,[Ll]:n.SRC_ALPHA_SATURATE,[Pl]:n.DST_COLOR,[Rl]:n.DST_ALPHA,[wl]:n.ONE_MINUS_SRC_COLOR,[Os]:n.ONE_MINUS_SRC_ALPHA,[Dl]:n.ONE_MINUS_DST_COLOR,[Cl]:n.ONE_MINUS_DST_ALPHA,[Il]:n.CONSTANT_COLOR,[Ul]:n.ONE_MINUS_CONSTANT_COLOR,[zl]:n.CONSTANT_ALPHA,[Nl]:n.ONE_MINUS_CONSTANT_ALPHA};function I(B,fe,$,ne,Me,xe,Be,lt,Et,tt){if(B===Rn){_===!0&&(le(n.BLEND),_=!1);return}if(_===!1&&(re(n.BLEND),_=!0),B!==xl){if(B!==p||tt!==v){if((u!==Xn||M!==Xn)&&(n.blendEquation(n.FUNC_ADD),u=Xn,M=Xn),tt)switch(B){case Ti:n.blendFuncSeparate(n.ONE,n.ONE_MINUS_SRC_ALPHA,n.ONE,n.ONE_MINUS_SRC_ALPHA);break;case lo:n.blendFunc(n.ONE,n.ONE);break;case uo:n.blendFuncSeparate(n.ZERO,n.ONE_MINUS_SRC_COLOR,n.ZERO,n.ONE);break;case ho:n.blendFuncSeparate(n.ZERO,n.SRC_COLOR,n.ZERO,n.SRC_ALPHA);break;default:console.error("THREE.WebGLState: Invalid blending: ",B);break}else switch(B){case Ti:n.blendFuncSeparate(n.SRC_ALPHA,n.ONE_MINUS_SRC_ALPHA,n.ONE,n.ONE_MINUS_SRC_ALPHA);break;case lo:n.blendFunc(n.SRC_ALPHA,n.ONE);break;case uo:n.blendFuncSeparate(n.ZERO,n.ONE_MINUS_SRC_COLOR,n.ZERO,n.ONE);break;case ho:n.blendFunc(n.ZERO,n.SRC_COLOR);break;default:console.error("THREE.WebGLState: Invalid blending: ",B);break}E=null,y=null,D=null,w=null,b.set(0,0,0),C=0,p=B,v=tt}return}Me=Me||fe,xe=xe||$,Be=Be||ne,(fe!==u||Me!==M)&&(n.blendEquationSeparate(se[fe],se[Me]),u=fe,M=Me),($!==E||ne!==y||xe!==D||Be!==w)&&(n.blendFuncSeparate(K[$],K[ne],K[xe],K[Be]),E=$,y=ne,D=xe,w=Be),(lt.equals(b)===!1||Et!==C)&&(n.blendColor(lt.r,lt.g,lt.b,Et),b.copy(lt),C=Et),p=B,v=!1}function Ce(B,fe){B.side===Tt?le(n.CULL_FACE):re(n.CULL_FACE);let $=B.side===Ct;fe&&($=!$),Se($),B.blending===Ti&&B.transparent===!1?I(Rn):I(B.blending,B.blendEquation,B.blendSrc,B.blendDst,B.blendEquationAlpha,B.blendSrcAlpha,B.blendDstAlpha,B.blendColor,B.blendAlpha,B.premultipliedAlpha),a.setFunc(B.depthFunc),a.setTest(B.depthTest),a.setMask(B.depthWrite),s.setMask(B.colorWrite);const ne=B.stencilWrite;o.setTest(ne),ne&&(o.setMask(B.stencilWriteMask),o.setFunc(B.stencilFunc,B.stencilRef,B.stencilFuncMask),o.setOp(B.stencilFail,B.stencilZFail,B.stencilZPass)),Ne(B.polygonOffset,B.polygonOffsetFactor,B.polygonOffsetUnits),B.alphaToCoverage===!0?re(n.SAMPLE_ALPHA_TO_COVERAGE):le(n.SAMPLE_ALPHA_TO_COVERAGE)}function Se(B){x!==B&&(B?n.frontFace(n.CW):n.frontFace(n.CCW),x=B)}function _e(B){B!==gl?(re(n.CULL_FACE),B!==P&&(B===co?n.cullFace(n.BACK):B===_l?n.cullFace(n.FRONT):n.cullFace(n.FRONT_AND_BACK))):le(n.CULL_FACE),P=B}function ve(B){B!==U&&(N&&n.lineWidth(B),U=B)}function Ne(B,fe,$){B?(re(n.POLYGON_OFFSET_FILL),(A!==fe||R!==$)&&(n.polygonOffset(fe,$),A=fe,R=$)):le(n.POLYGON_OFFSET_FILL)}function we(B){B?re(n.SCISSOR_TEST):le(n.SCISSOR_TEST)}function L(B){B===void 0&&(B=n.TEXTURE0+z-1),G!==B&&(n.activeTexture(B),G=B)}function S(B,fe,$){$===void 0&&(G===null?$=n.TEXTURE0+z-1:$=G);let ne=Z[$];ne===void 0&&(ne={type:void 0,texture:void 0},Z[$]=ne),(ne.type!==B||ne.texture!==fe)&&(G!==$&&(n.activeTexture($),G=$),n.bindTexture(B,fe||ue[B]),ne.type=B,ne.texture=fe)}function j(){const B=Z[G];B!==void 0&&B.type!==void 0&&(n.bindTexture(B.type,null),B.type=void 0,B.texture=void 0)}function Q(){try{n.compressedTexImage2D(...arguments)}catch(B){console.error("THREE.WebGLState:",B)}}function ie(){try{n.compressedTexImage3D(...arguments)}catch(B){console.error("THREE.WebGLState:",B)}}function J(){try{n.texSubImage2D(...arguments)}catch(B){console.error("THREE.WebGLState:",B)}}function Re(){try{n.texSubImage3D(...arguments)}catch(B){console.error("THREE.WebGLState:",B)}}function ge(){try{n.compressedTexSubImage2D(...arguments)}catch(B){console.error("THREE.WebGLState:",B)}}function ye(){try{n.compressedTexSubImage3D(...arguments)}catch(B){console.error("THREE.WebGLState:",B)}}function Ye(){try{n.texStorage2D(...arguments)}catch(B){console.error("THREE.WebGLState:",B)}}function ce(){try{n.texStorage3D(...arguments)}catch(B){console.error("THREE.WebGLState:",B)}}function be(){try{n.texImage2D(...arguments)}catch(B){console.error("THREE.WebGLState:",B)}}function ze(){try{n.texImage3D(...arguments)}catch(B){console.error("THREE.WebGLState:",B)}}function Fe(B){Ie.equals(B)===!1&&(n.scissor(B.x,B.y,B.z,B.w),Ie.copy(B))}function Te(B){X.equals(B)===!1&&(n.viewport(B.x,B.y,B.z,B.w),X.copy(B))}function qe(B,fe){let $=l.get(fe);$===void 0&&($=new WeakMap,l.set(fe,$));let ne=$.get(B);ne===void 0&&(ne=n.getUniformBlockIndex(fe,B.name),$.set(B,ne))}function He(B,fe){const ne=l.get(fe).get(B);c.get(fe)!==ne&&(n.uniformBlockBinding(fe,ne,B.__bindingPointIndex),c.set(fe,ne))}function st(){n.disable(n.BLEND),n.disable(n.CULL_FACE),n.disable(n.DEPTH_TEST),n.disable(n.POLYGON_OFFSET_FILL),n.disable(n.SCISSOR_TEST),n.disable(n.STENCIL_TEST),n.disable(n.SAMPLE_ALPHA_TO_COVERAGE),n.blendEquation(n.FUNC_ADD),n.blendFunc(n.ONE,n.ZERO),n.blendFuncSeparate(n.ONE,n.ZERO,n.ONE,n.ZERO),n.blendColor(0,0,0,0),n.colorMask(!0,!0,!0,!0),n.clearColor(0,0,0,0),n.depthMask(!0),n.depthFunc(n.LESS),a.setReversed(!1),n.clearDepth(1),n.stencilMask(4294967295),n.stencilFunc(n.ALWAYS,0,4294967295),n.stencilOp(n.KEEP,n.KEEP,n.KEEP),n.clearStencil(0),n.cullFace(n.BACK),n.frontFace(n.CCW),n.polygonOffset(0,0),n.activeTexture(n.TEXTURE0),n.bindFramebuffer(n.FRAMEBUFFER,null),n.bindFramebuffer(n.DRAW_FRAMEBUFFER,null),n.bindFramebuffer(n.READ_FRAMEBUFFER,null),n.useProgram(null),n.lineWidth(1),n.scissor(0,0,n.canvas.width,n.canvas.height),n.viewport(0,0,n.canvas.width,n.canvas.height),d={},G=null,Z={},h={},f=new WeakMap,m=[],g=null,_=!1,p=null,u=null,E=null,y=null,M=null,D=null,w=null,b=new oe(0,0,0),C=0,v=!1,x=null,P=null,U=null,A=null,R=null,Ie.set(0,0,n.canvas.width,n.canvas.height),X.set(0,0,n.canvas.width,n.canvas.height),s.reset(),a.reset(),o.reset()}return{buffers:{color:s,depth:a,stencil:o},enable:re,disable:le,bindFramebuffer:Pe,drawBuffers:me,useProgram:te,setBlending:I,setMaterial:Ce,setFlipSided:Se,setCullFace:_e,setLineWidth:ve,setPolygonOffset:Ne,setScissorTest:we,activeTexture:L,bindTexture:S,unbindTexture:j,compressedTexImage2D:Q,compressedTexImage3D:ie,texImage2D:be,texImage3D:ze,updateUBOMapping:qe,uniformBlockBinding:He,texStorage2D:Ye,texStorage3D:ce,texSubImage2D:J,texSubImage3D:Re,compressedTexSubImage2D:ge,compressedTexSubImage3D:ye,scissor:Fe,viewport:Te,reset:st}}function vm(n,e,t,i,r,s,a){const o=e.has("WEBGL_multisampled_render_to_texture")?e.get("WEBGL_multisampled_render_to_texture"):null,c=typeof navigator>"u"?!1:/OculusBrowser/g.test(navigator.userAgent),l=new We,d=new WeakMap;let h;const f=new WeakMap;let m=!1;try{m=typeof OffscreenCanvas<"u"&&new OffscreenCanvas(1,1).getContext("2d")!==null}catch{}function g(L,S){return m?new OffscreenCanvas(L,S):Wr("canvas")}function _(L,S,j){let Q=1;const ie=we(L);if((ie.width>j||ie.height>j)&&(Q=j/Math.max(ie.width,ie.height)),Q<1)if(typeof HTMLImageElement<"u"&&L instanceof HTMLImageElement||typeof HTMLCanvasElement<"u"&&L instanceof HTMLCanvasElement||typeof ImageBitmap<"u"&&L instanceof ImageBitmap||typeof VideoFrame<"u"&&L instanceof VideoFrame){const J=Math.floor(Q*ie.width),Re=Math.floor(Q*ie.height);h===void 0&&(h=g(J,Re));const ge=S?g(J,Re):h;return ge.width=J,ge.height=Re,ge.getContext("2d").drawImage(L,0,0,J,Re),console.warn("THREE.WebGLRenderer: Texture has been resized from ("+ie.width+"x"+ie.height+") to ("+J+"x"+Re+")."),ge}else return"data"in L&&console.warn("THREE.WebGLRenderer: Image in DataTexture is too big ("+ie.width+"x"+ie.height+")."),L;return L}function p(L){return L.generateMipmaps}function u(L){n.generateMipmap(L)}function E(L){return L.isWebGLCubeRenderTarget?n.TEXTURE_CUBE_MAP:L.isWebGL3DRenderTarget?n.TEXTURE_3D:L.isWebGLArrayRenderTarget||L.isCompressedArrayTexture?n.TEXTURE_2D_ARRAY:n.TEXTURE_2D}function y(L,S,j,Q,ie=!1){if(L!==null){if(n[L]!==void 0)return n[L];console.warn("THREE.WebGLRenderer: Attempt to use non-existing WebGL internal format '"+L+"'")}let J=S;if(S===n.RED&&(j===n.FLOAT&&(J=n.R32F),j===n.HALF_FLOAT&&(J=n.R16F),j===n.UNSIGNED_BYTE&&(J=n.R8)),S===n.RED_INTEGER&&(j===n.UNSIGNED_BYTE&&(J=n.R8UI),j===n.UNSIGNED_SHORT&&(J=n.R16UI),j===n.UNSIGNED_INT&&(J=n.R32UI),j===n.BYTE&&(J=n.R8I),j===n.SHORT&&(J=n.R16I),j===n.INT&&(J=n.R32I)),S===n.RG&&(j===n.FLOAT&&(J=n.RG32F),j===n.HALF_FLOAT&&(J=n.RG16F),j===n.UNSIGNED_BYTE&&(J=n.RG8)),S===n.RG_INTEGER&&(j===n.UNSIGNED_BYTE&&(J=n.RG8UI),j===n.UNSIGNED_SHORT&&(J=n.RG16UI),j===n.UNSIGNED_INT&&(J=n.RG32UI),j===n.BYTE&&(J=n.RG8I),j===n.SHORT&&(J=n.RG16I),j===n.INT&&(J=n.RG32I)),S===n.RGB_INTEGER&&(j===n.UNSIGNED_BYTE&&(J=n.RGB8UI),j===n.UNSIGNED_SHORT&&(J=n.RGB16UI),j===n.UNSIGNED_INT&&(J=n.RGB32UI),j===n.BYTE&&(J=n.RGB8I),j===n.SHORT&&(J=n.RGB16I),j===n.INT&&(J=n.RGB32I)),S===n.RGBA_INTEGER&&(j===n.UNSIGNED_BYTE&&(J=n.RGBA8UI),j===n.UNSIGNED_SHORT&&(J=n.RGBA16UI),j===n.UNSIGNED_INT&&(J=n.RGBA32UI),j===n.BYTE&&(J=n.RGBA8I),j===n.SHORT&&(J=n.RGBA16I),j===n.INT&&(J=n.RGBA32I)),S===n.RGB&&j===n.UNSIGNED_INT_5_9_9_9_REV&&(J=n.RGB9_E5),S===n.RGBA){const Re=ie?Gr:Je.getTransfer(Q);j===n.FLOAT&&(J=n.RGBA32F),j===n.HALF_FLOAT&&(J=n.RGBA16F),j===n.UNSIGNED_BYTE&&(J=Re===it?n.SRGB8_ALPHA8:n.RGBA8),j===n.UNSIGNED_SHORT_4_4_4_4&&(J=n.RGBA4),j===n.UNSIGNED_SHORT_5_5_5_1&&(J=n.RGB5_A1)}return(J===n.R16F||J===n.R32F||J===n.RG16F||J===n.RG32F||J===n.RGBA16F||J===n.RGBA32F)&&e.get("EXT_color_buffer_float"),J}function M(L,S){let j;return L?S===null||S===Qn||S===Di?j=n.DEPTH24_STENCIL8:S===dn?j=n.DEPTH32F_STENCIL8:S===Zi&&(j=n.DEPTH24_STENCIL8,console.warn("DepthTexture: 16 bit depth attachment is not supported with stencil. Using 24-bit attachment.")):S===null||S===Qn||S===Di?j=n.DEPTH_COMPONENT24:S===dn?j=n.DEPTH_COMPONENT32F:S===Zi&&(j=n.DEPTH_COMPONENT16),j}function D(L,S){return p(L)===!0||L.isFramebufferTexture&&L.minFilter!==kt&&L.minFilter!==Zt?Math.log2(Math.max(S.width,S.height))+1:L.mipmaps!==void 0&&L.mipmaps.length>0?L.mipmaps.length:L.isCompressedTexture&&Array.isArray(L.image)?S.mipmaps.length:1}function w(L){const S=L.target;S.removeEventListener("dispose",w),C(S),S.isVideoTexture&&d.delete(S)}function b(L){const S=L.target;S.removeEventListener("dispose",b),x(S)}function C(L){const S=i.get(L);if(S.__webglInit===void 0)return;const j=L.source,Q=f.get(j);if(Q){const ie=Q[S.__cacheKey];ie.usedTimes--,ie.usedTimes===0&&v(L),Object.keys(Q).length===0&&f.delete(j)}i.remove(L)}function v(L){const S=i.get(L);n.deleteTexture(S.__webglTexture);const j=L.source,Q=f.get(j);delete Q[S.__cacheKey],a.memory.textures--}function x(L){const S=i.get(L);if(L.depthTexture&&(L.depthTexture.dispose(),i.remove(L.depthTexture)),L.isWebGLCubeRenderTarget)for(let Q=0;Q<6;Q++){if(Array.isArray(S.__webglFramebuffer[Q]))for(let ie=0;ie<S.__webglFramebuffer[Q].length;ie++)n.deleteFramebuffer(S.__webglFramebuffer[Q][ie]);else n.deleteFramebuffer(S.__webglFramebuffer[Q]);S.__webglDepthbuffer&&n.deleteRenderbuffer(S.__webglDepthbuffer[Q])}else{if(Array.isArray(S.__webglFramebuffer))for(let Q=0;Q<S.__webglFramebuffer.length;Q++)n.deleteFramebuffer(S.__webglFramebuffer[Q]);else n.deleteFramebuffer(S.__webglFramebuffer);if(S.__webglDepthbuffer&&n.deleteRenderbuffer(S.__webglDepthbuffer),S.__webglMultisampledFramebuffer&&n.deleteFramebuffer(S.__webglMultisampledFramebuffer),S.__webglColorRenderbuffer)for(let Q=0;Q<S.__webglColorRenderbuffer.length;Q++)S.__webglColorRenderbuffer[Q]&&n.deleteRenderbuffer(S.__webglColorRenderbuffer[Q]);S.__webglDepthRenderbuffer&&n.deleteRenderbuffer(S.__webglDepthRenderbuffer)}const j=L.textures;for(let Q=0,ie=j.length;Q<ie;Q++){const J=i.get(j[Q]);J.__webglTexture&&(n.deleteTexture(J.__webglTexture),a.memory.textures--),i.remove(j[Q])}i.remove(L)}let P=0;function U(){P=0}function A(){const L=P;return L>=r.maxTextures&&console.warn("THREE.WebGLTextures: Trying to use "+L+" texture units while this GPU supports only "+r.maxTextures),P+=1,L}function R(L){const S=[];return S.push(L.wrapS),S.push(L.wrapT),S.push(L.wrapR||0),S.push(L.magFilter),S.push(L.minFilter),S.push(L.anisotropy),S.push(L.internalFormat),S.push(L.format),S.push(L.type),S.push(L.generateMipmaps),S.push(L.premultiplyAlpha),S.push(L.flipY),S.push(L.unpackAlignment),S.push(L.colorSpace),S.join()}function z(L,S){const j=i.get(L);if(L.isVideoTexture&&ve(L),L.isRenderTargetTexture===!1&&L.version>0&&j.__version!==L.version){const Q=L.image;if(Q===null)console.warn("THREE.WebGLRenderer: Texture marked for update but no image data found.");else if(Q.complete===!1)console.warn("THREE.WebGLRenderer: Texture marked for update but image is incomplete");else{X(j,L,S);return}}t.bindTexture(n.TEXTURE_2D,j.__webglTexture,n.TEXTURE0+S)}function N(L,S){const j=i.get(L);if(L.version>0&&j.__version!==L.version){X(j,L,S);return}t.bindTexture(n.TEXTURE_2D_ARRAY,j.__webglTexture,n.TEXTURE0+S)}function O(L,S){const j=i.get(L);if(L.version>0&&j.__version!==L.version){X(j,L,S);return}t.bindTexture(n.TEXTURE_3D,j.__webglTexture,n.TEXTURE0+S)}function F(L,S){const j=i.get(L);if(L.version>0&&j.__version!==L.version){ee(j,L,S);return}t.bindTexture(n.TEXTURE_CUBE_MAP,j.__webglTexture,n.TEXTURE0+S)}const G={[Ys]:n.REPEAT,[Yn]:n.CLAMP_TO_EDGE,[$s]:n.MIRRORED_REPEAT},Z={[kt]:n.NEAREST,[Xl]:n.NEAREST_MIPMAP_NEAREST,[cr]:n.NEAREST_MIPMAP_LINEAR,[Zt]:n.LINEAR,[Qr]:n.LINEAR_MIPMAP_NEAREST,[$n]:n.LINEAR_MIPMAP_LINEAR},Y={[$l]:n.NEVER,[nu]:n.ALWAYS,[Zl]:n.LESS,[Vc]:n.LEQUAL,[Jl]:n.EQUAL,[tu]:n.GEQUAL,[Ql]:n.GREATER,[eu]:n.NOTEQUAL};function he(L,S){if(S.type===dn&&e.has("OES_texture_float_linear")===!1&&(S.magFilter===Zt||S.magFilter===Qr||S.magFilter===cr||S.magFilter===$n||S.minFilter===Zt||S.minFilter===Qr||S.minFilter===cr||S.minFilter===$n)&&console.warn("THREE.WebGLRenderer: Unable to use linear filtering with floating point textures. OES_texture_float_linear not supported on this device."),n.texParameteri(L,n.TEXTURE_WRAP_S,G[S.wrapS]),n.texParameteri(L,n.TEXTURE_WRAP_T,G[S.wrapT]),(L===n.TEXTURE_3D||L===n.TEXTURE_2D_ARRAY)&&n.texParameteri(L,n.TEXTURE_WRAP_R,G[S.wrapR]),n.texParameteri(L,n.TEXTURE_MAG_FILTER,Z[S.magFilter]),n.texParameteri(L,n.TEXTURE_MIN_FILTER,Z[S.minFilter]),S.compareFunction&&(n.texParameteri(L,n.TEXTURE_COMPARE_MODE,n.COMPARE_REF_TO_TEXTURE),n.texParameteri(L,n.TEXTURE_COMPARE_FUNC,Y[S.compareFunction])),e.has("EXT_texture_filter_anisotropic")===!0){if(S.magFilter===kt||S.minFilter!==cr&&S.minFilter!==$n||S.type===dn&&e.has("OES_texture_float_linear")===!1)return;if(S.anisotropy>1||i.get(S).__currentAnisotropy){const j=e.get("EXT_texture_filter_anisotropic");n.texParameterf(L,j.TEXTURE_MAX_ANISOTROPY_EXT,Math.min(S.anisotropy,r.getMaxAnisotropy())),i.get(S).__currentAnisotropy=S.anisotropy}}}function Ie(L,S){let j=!1;L.__webglInit===void 0&&(L.__webglInit=!0,S.addEventListener("dispose",w));const Q=S.source;let ie=f.get(Q);ie===void 0&&(ie={},f.set(Q,ie));const J=R(S);if(J!==L.__cacheKey){ie[J]===void 0&&(ie[J]={texture:n.createTexture(),usedTimes:0},a.memory.textures++,j=!0),ie[J].usedTimes++;const Re=ie[L.__cacheKey];Re!==void 0&&(ie[L.__cacheKey].usedTimes--,Re.usedTimes===0&&v(S)),L.__cacheKey=J,L.__webglTexture=ie[J].texture}return j}function X(L,S,j){let Q=n.TEXTURE_2D;(S.isDataArrayTexture||S.isCompressedArrayTexture)&&(Q=n.TEXTURE_2D_ARRAY),S.isData3DTexture&&(Q=n.TEXTURE_3D);const ie=Ie(L,S),J=S.source;t.bindTexture(Q,L.__webglTexture,n.TEXTURE0+j);const Re=i.get(J);if(J.version!==Re.__version||ie===!0){t.activeTexture(n.TEXTURE0+j);const ge=Je.getPrimaries(Je.workingColorSpace),ye=S.colorSpace===An?null:Je.getPrimaries(S.colorSpace),Ye=S.colorSpace===An||ge===ye?n.NONE:n.BROWSER_DEFAULT_WEBGL;n.pixelStorei(n.UNPACK_FLIP_Y_WEBGL,S.flipY),n.pixelStorei(n.UNPACK_PREMULTIPLY_ALPHA_WEBGL,S.premultiplyAlpha),n.pixelStorei(n.UNPACK_ALIGNMENT,S.unpackAlignment),n.pixelStorei(n.UNPACK_COLORSPACE_CONVERSION_WEBGL,Ye);let ce=_(S.image,!1,r.maxTextureSize);ce=Ne(S,ce);const be=s.convert(S.format,S.colorSpace),ze=s.convert(S.type);let Fe=y(S.internalFormat,be,ze,S.colorSpace,S.isVideoTexture);he(Q,S);let Te;const qe=S.mipmaps,He=S.isVideoTexture!==!0,st=Re.__version===void 0||ie===!0,B=J.dataReady,fe=D(S,ce);if(S.isDepthTexture)Fe=M(S.format===Li,S.type),st&&(He?t.texStorage2D(n.TEXTURE_2D,1,Fe,ce.width,ce.height):t.texImage2D(n.TEXTURE_2D,0,Fe,ce.width,ce.height,0,be,ze,null));else if(S.isDataTexture)if(qe.length>0){He&&st&&t.texStorage2D(n.TEXTURE_2D,fe,Fe,qe[0].width,qe[0].height);for(let $=0,ne=qe.length;$<ne;$++)Te=qe[$],He?B&&t.texSubImage2D(n.TEXTURE_2D,$,0,0,Te.width,Te.height,be,ze,Te.data):t.texImage2D(n.TEXTURE_2D,$,Fe,Te.width,Te.height,0,be,ze,Te.data);S.generateMipmaps=!1}else He?(st&&t.texStorage2D(n.TEXTURE_2D,fe,Fe,ce.width,ce.height),B&&t.texSubImage2D(n.TEXTURE_2D,0,0,0,ce.width,ce.height,be,ze,ce.data)):t.texImage2D(n.TEXTURE_2D,0,Fe,ce.width,ce.height,0,be,ze,ce.data);else if(S.isCompressedTexture)if(S.isCompressedArrayTexture){He&&st&&t.texStorage3D(n.TEXTURE_2D_ARRAY,fe,Fe,qe[0].width,qe[0].height,ce.depth);for(let $=0,ne=qe.length;$<ne;$++)if(Te=qe[$],S.format!==Gt)if(be!==null)if(He){if(B)if(S.layerUpdates.size>0){const Me=Go(Te.width,Te.height,S.format,S.type);for(const xe of S.layerUpdates){const Be=Te.data.subarray(xe*Me/Te.data.BYTES_PER_ELEMENT,(xe+1)*Me/Te.data.BYTES_PER_ELEMENT);t.compressedTexSubImage3D(n.TEXTURE_2D_ARRAY,$,0,0,xe,Te.width,Te.height,1,be,Be)}S.clearLayerUpdates()}else t.compressedTexSubImage3D(n.TEXTURE_2D_ARRAY,$,0,0,0,Te.width,Te.height,ce.depth,be,Te.data)}else t.compressedTexImage3D(n.TEXTURE_2D_ARRAY,$,Fe,Te.width,Te.height,ce.depth,0,Te.data,0,0);else console.warn("THREE.WebGLRenderer: Attempt to load unsupported compressed texture format in .uploadTexture()");else He?B&&t.texSubImage3D(n.TEXTURE_2D_ARRAY,$,0,0,0,Te.width,Te.height,ce.depth,be,ze,Te.data):t.texImage3D(n.TEXTURE_2D_ARRAY,$,Fe,Te.width,Te.height,ce.depth,0,be,ze,Te.data)}else{He&&st&&t.texStorage2D(n.TEXTURE_2D,fe,Fe,qe[0].width,qe[0].height);for(let $=0,ne=qe.length;$<ne;$++)Te=qe[$],S.format!==Gt?be!==null?He?B&&t.compressedTexSubImage2D(n.TEXTURE_2D,$,0,0,Te.width,Te.height,be,Te.data):t.compressedTexImage2D(n.TEXTURE_2D,$,Fe,Te.width,Te.height,0,Te.data):console.warn("THREE.WebGLRenderer: Attempt to load unsupported compressed texture format in .uploadTexture()"):He?B&&t.texSubImage2D(n.TEXTURE_2D,$,0,0,Te.width,Te.height,be,ze,Te.data):t.texImage2D(n.TEXTURE_2D,$,Fe,Te.width,Te.height,0,be,ze,Te.data)}else if(S.isDataArrayTexture)if(He){if(st&&t.texStorage3D(n.TEXTURE_2D_ARRAY,fe,Fe,ce.width,ce.height,ce.depth),B)if(S.layerUpdates.size>0){const $=Go(ce.width,ce.height,S.format,S.type);for(const ne of S.layerUpdates){const Me=ce.data.subarray(ne*$/ce.data.BYTES_PER_ELEMENT,(ne+1)*$/ce.data.BYTES_PER_ELEMENT);t.texSubImage3D(n.TEXTURE_2D_ARRAY,0,0,0,ne,ce.width,ce.height,1,be,ze,Me)}S.clearLayerUpdates()}else t.texSubImage3D(n.TEXTURE_2D_ARRAY,0,0,0,0,ce.width,ce.height,ce.depth,be,ze,ce.data)}else t.texImage3D(n.TEXTURE_2D_ARRAY,0,Fe,ce.width,ce.height,ce.depth,0,be,ze,ce.data);else if(S.isData3DTexture)He?(st&&t.texStorage3D(n.TEXTURE_3D,fe,Fe,ce.width,ce.height,ce.depth),B&&t.texSubImage3D(n.TEXTURE_3D,0,0,0,0,ce.width,ce.height,ce.depth,be,ze,ce.data)):t.texImage3D(n.TEXTURE_3D,0,Fe,ce.width,ce.height,ce.depth,0,be,ze,ce.data);else if(S.isFramebufferTexture){if(st)if(He)t.texStorage2D(n.TEXTURE_2D,fe,Fe,ce.width,ce.height);else{let $=ce.width,ne=ce.height;for(let Me=0;Me<fe;Me++)t.texImage2D(n.TEXTURE_2D,Me,Fe,$,ne,0,be,ze,null),$>>=1,ne>>=1}}else if(qe.length>0){if(He&&st){const $=we(qe[0]);t.texStorage2D(n.TEXTURE_2D,fe,Fe,$.width,$.height)}for(let $=0,ne=qe.length;$<ne;$++)Te=qe[$],He?B&&t.texSubImage2D(n.TEXTURE_2D,$,0,0,be,ze,Te):t.texImage2D(n.TEXTURE_2D,$,Fe,be,ze,Te);S.generateMipmaps=!1}else if(He){if(st){const $=we(ce);t.texStorage2D(n.TEXTURE_2D,fe,Fe,$.width,$.height)}B&&t.texSubImage2D(n.TEXTURE_2D,0,0,0,be,ze,ce)}else t.texImage2D(n.TEXTURE_2D,0,Fe,be,ze,ce);p(S)&&u(Q),Re.__version=J.version,S.onUpdate&&S.onUpdate(S)}L.__version=S.version}function ee(L,S,j){if(S.image.length!==6)return;const Q=Ie(L,S),ie=S.source;t.bindTexture(n.TEXTURE_CUBE_MAP,L.__webglTexture,n.TEXTURE0+j);const J=i.get(ie);if(ie.version!==J.__version||Q===!0){t.activeTexture(n.TEXTURE0+j);const Re=Je.getPrimaries(Je.workingColorSpace),ge=S.colorSpace===An?null:Je.getPrimaries(S.colorSpace),ye=S.colorSpace===An||Re===ge?n.NONE:n.BROWSER_DEFAULT_WEBGL;n.pixelStorei(n.UNPACK_FLIP_Y_WEBGL,S.flipY),n.pixelStorei(n.UNPACK_PREMULTIPLY_ALPHA_WEBGL,S.premultiplyAlpha),n.pixelStorei(n.UNPACK_ALIGNMENT,S.unpackAlignment),n.pixelStorei(n.UNPACK_COLORSPACE_CONVERSION_WEBGL,ye);const Ye=S.isCompressedTexture||S.image[0].isCompressedTexture,ce=S.image[0]&&S.image[0].isDataTexture,be=[];for(let ne=0;ne<6;ne++)!Ye&&!ce?be[ne]=_(S.image[ne],!0,r.maxCubemapSize):be[ne]=ce?S.image[ne].image:S.image[ne],be[ne]=Ne(S,be[ne]);const ze=be[0],Fe=s.convert(S.format,S.colorSpace),Te=s.convert(S.type),qe=y(S.internalFormat,Fe,Te,S.colorSpace),He=S.isVideoTexture!==!0,st=J.__version===void 0||Q===!0,B=ie.dataReady;let fe=D(S,ze);he(n.TEXTURE_CUBE_MAP,S);let $;if(Ye){He&&st&&t.texStorage2D(n.TEXTURE_CUBE_MAP,fe,qe,ze.width,ze.height);for(let ne=0;ne<6;ne++){$=be[ne].mipmaps;for(let Me=0;Me<$.length;Me++){const xe=$[Me];S.format!==Gt?Fe!==null?He?B&&t.compressedTexSubImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+ne,Me,0,0,xe.width,xe.height,Fe,xe.data):t.compressedTexImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+ne,Me,qe,xe.width,xe.height,0,xe.data):console.warn("THREE.WebGLRenderer: Attempt to load unsupported compressed texture format in .setTextureCube()"):He?B&&t.texSubImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+ne,Me,0,0,xe.width,xe.height,Fe,Te,xe.data):t.texImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+ne,Me,qe,xe.width,xe.height,0,Fe,Te,xe.data)}}}else{if($=S.mipmaps,He&&st){$.length>0&&fe++;const ne=we(be[0]);t.texStorage2D(n.TEXTURE_CUBE_MAP,fe,qe,ne.width,ne.height)}for(let ne=0;ne<6;ne++)if(ce){He?B&&t.texSubImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+ne,0,0,0,be[ne].width,be[ne].height,Fe,Te,be[ne].data):t.texImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+ne,0,qe,be[ne].width,be[ne].height,0,Fe,Te,be[ne].data);for(let Me=0;Me<$.length;Me++){const Be=$[Me].image[ne].image;He?B&&t.texSubImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+ne,Me+1,0,0,Be.width,Be.height,Fe,Te,Be.data):t.texImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+ne,Me+1,qe,Be.width,Be.height,0,Fe,Te,Be.data)}}else{He?B&&t.texSubImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+ne,0,0,0,Fe,Te,be[ne]):t.texImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+ne,0,qe,Fe,Te,be[ne]);for(let Me=0;Me<$.length;Me++){const xe=$[Me];He?B&&t.texSubImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+ne,Me+1,0,0,Fe,Te,xe.image[ne]):t.texImage2D(n.TEXTURE_CUBE_MAP_POSITIVE_X+ne,Me+1,qe,Fe,Te,xe.image[ne])}}}p(S)&&u(n.TEXTURE_CUBE_MAP),J.__version=ie.version,S.onUpdate&&S.onUpdate(S)}L.__version=S.version}function ue(L,S,j,Q,ie,J){const Re=s.convert(j.format,j.colorSpace),ge=s.convert(j.type),ye=y(j.internalFormat,Re,ge,j.colorSpace),Ye=i.get(S),ce=i.get(j);if(ce.__renderTarget=S,!Ye.__hasExternalTextures){const be=Math.max(1,S.width>>J),ze=Math.max(1,S.height>>J);ie===n.TEXTURE_3D||ie===n.TEXTURE_2D_ARRAY?t.texImage3D(ie,J,ye,be,ze,S.depth,0,Re,ge,null):t.texImage2D(ie,J,ye,be,ze,0,Re,ge,null)}t.bindFramebuffer(n.FRAMEBUFFER,L),_e(S)?o.framebufferTexture2DMultisampleEXT(n.FRAMEBUFFER,Q,ie,ce.__webglTexture,0,Se(S)):(ie===n.TEXTURE_2D||ie>=n.TEXTURE_CUBE_MAP_POSITIVE_X&&ie<=n.TEXTURE_CUBE_MAP_NEGATIVE_Z)&&n.framebufferTexture2D(n.FRAMEBUFFER,Q,ie,ce.__webglTexture,J),t.bindFramebuffer(n.FRAMEBUFFER,null)}function re(L,S,j){if(n.bindRenderbuffer(n.RENDERBUFFER,L),S.depthBuffer){const Q=S.depthTexture,ie=Q&&Q.isDepthTexture?Q.type:null,J=M(S.stencilBuffer,ie),Re=S.stencilBuffer?n.DEPTH_STENCIL_ATTACHMENT:n.DEPTH_ATTACHMENT,ge=Se(S);_e(S)?o.renderbufferStorageMultisampleEXT(n.RENDERBUFFER,ge,J,S.width,S.height):j?n.renderbufferStorageMultisample(n.RENDERBUFFER,ge,J,S.width,S.height):n.renderbufferStorage(n.RENDERBUFFER,J,S.width,S.height),n.framebufferRenderbuffer(n.FRAMEBUFFER,Re,n.RENDERBUFFER,L)}else{const Q=S.textures;for(let ie=0;ie<Q.length;ie++){const J=Q[ie],Re=s.convert(J.format,J.colorSpace),ge=s.convert(J.type),ye=y(J.internalFormat,Re,ge,J.colorSpace),Ye=Se(S);j&&_e(S)===!1?n.renderbufferStorageMultisample(n.RENDERBUFFER,Ye,ye,S.width,S.height):_e(S)?o.renderbufferStorageMultisampleEXT(n.RENDERBUFFER,Ye,ye,S.width,S.height):n.renderbufferStorage(n.RENDERBUFFER,ye,S.width,S.height)}}n.bindRenderbuffer(n.RENDERBUFFER,null)}function le(L,S){if(S&&S.isWebGLCubeRenderTarget)throw new Error("Depth Texture with cube render targets is not supported");if(t.bindFramebuffer(n.FRAMEBUFFER,L),!(S.depthTexture&&S.depthTexture.isDepthTexture))throw new Error("renderTarget.depthTexture must be an instance of THREE.DepthTexture");const Q=i.get(S.depthTexture);Q.__renderTarget=S,(!Q.__webglTexture||S.depthTexture.image.width!==S.width||S.depthTexture.image.height!==S.height)&&(S.depthTexture.image.width=S.width,S.depthTexture.image.height=S.height,S.depthTexture.needsUpdate=!0),z(S.depthTexture,0);const ie=Q.__webglTexture,J=Se(S);if(S.depthTexture.format===Ai)_e(S)?o.framebufferTexture2DMultisampleEXT(n.FRAMEBUFFER,n.DEPTH_ATTACHMENT,n.TEXTURE_2D,ie,0,J):n.framebufferTexture2D(n.FRAMEBUFFER,n.DEPTH_ATTACHMENT,n.TEXTURE_2D,ie,0);else if(S.depthTexture.format===Li)_e(S)?o.framebufferTexture2DMultisampleEXT(n.FRAMEBUFFER,n.DEPTH_STENCIL_ATTACHMENT,n.TEXTURE_2D,ie,0,J):n.framebufferTexture2D(n.FRAMEBUFFER,n.DEPTH_STENCIL_ATTACHMENT,n.TEXTURE_2D,ie,0);else throw new Error("Unknown depthTexture format")}function Pe(L){const S=i.get(L),j=L.isWebGLCubeRenderTarget===!0;if(S.__boundDepthTexture!==L.depthTexture){const Q=L.depthTexture;if(S.__depthDisposeCallback&&S.__depthDisposeCallback(),Q){const ie=()=>{delete S.__boundDepthTexture,delete S.__depthDisposeCallback,Q.removeEventListener("dispose",ie)};Q.addEventListener("dispose",ie),S.__depthDisposeCallback=ie}S.__boundDepthTexture=Q}if(L.depthTexture&&!S.__autoAllocateDepthBuffer){if(j)throw new Error("target.depthTexture not supported in Cube render targets");le(S.__webglFramebuffer,L)}else if(j){S.__webglDepthbuffer=[];for(let Q=0;Q<6;Q++)if(t.bindFramebuffer(n.FRAMEBUFFER,S.__webglFramebuffer[Q]),S.__webglDepthbuffer[Q]===void 0)S.__webglDepthbuffer[Q]=n.createRenderbuffer(),re(S.__webglDepthbuffer[Q],L,!1);else{const ie=L.stencilBuffer?n.DEPTH_STENCIL_ATTACHMENT:n.DEPTH_ATTACHMENT,J=S.__webglDepthbuffer[Q];n.bindRenderbuffer(n.RENDERBUFFER,J),n.framebufferRenderbuffer(n.FRAMEBUFFER,ie,n.RENDERBUFFER,J)}}else if(t.bindFramebuffer(n.FRAMEBUFFER,S.__webglFramebuffer),S.__webglDepthbuffer===void 0)S.__webglDepthbuffer=n.createRenderbuffer(),re(S.__webglDepthbuffer,L,!1);else{const Q=L.stencilBuffer?n.DEPTH_STENCIL_ATTACHMENT:n.DEPTH_ATTACHMENT,ie=S.__webglDepthbuffer;n.bindRenderbuffer(n.RENDERBUFFER,ie),n.framebufferRenderbuffer(n.FRAMEBUFFER,Q,n.RENDERBUFFER,ie)}t.bindFramebuffer(n.FRAMEBUFFER,null)}function me(L,S,j){const Q=i.get(L);S!==void 0&&ue(Q.__webglFramebuffer,L,L.texture,n.COLOR_ATTACHMENT0,n.TEXTURE_2D,0),j!==void 0&&Pe(L)}function te(L){const S=L.texture,j=i.get(L),Q=i.get(S);L.addEventListener("dispose",b);const ie=L.textures,J=L.isWebGLCubeRenderTarget===!0,Re=ie.length>1;if(Re||(Q.__webglTexture===void 0&&(Q.__webglTexture=n.createTexture()),Q.__version=S.version,a.memory.textures++),J){j.__webglFramebuffer=[];for(let ge=0;ge<6;ge++)if(S.mipmaps&&S.mipmaps.length>0){j.__webglFramebuffer[ge]=[];for(let ye=0;ye<S.mipmaps.length;ye++)j.__webglFramebuffer[ge][ye]=n.createFramebuffer()}else j.__webglFramebuffer[ge]=n.createFramebuffer()}else{if(S.mipmaps&&S.mipmaps.length>0){j.__webglFramebuffer=[];for(let ge=0;ge<S.mipmaps.length;ge++)j.__webglFramebuffer[ge]=n.createFramebuffer()}else j.__webglFramebuffer=n.createFramebuffer();if(Re)for(let ge=0,ye=ie.length;ge<ye;ge++){const Ye=i.get(ie[ge]);Ye.__webglTexture===void 0&&(Ye.__webglTexture=n.createTexture(),a.memory.textures++)}if(L.samples>0&&_e(L)===!1){j.__webglMultisampledFramebuffer=n.createFramebuffer(),j.__webglColorRenderbuffer=[],t.bindFramebuffer(n.FRAMEBUFFER,j.__webglMultisampledFramebuffer);for(let ge=0;ge<ie.length;ge++){const ye=ie[ge];j.__webglColorRenderbuffer[ge]=n.createRenderbuffer(),n.bindRenderbuffer(n.RENDERBUFFER,j.__webglColorRenderbuffer[ge]);const Ye=s.convert(ye.format,ye.colorSpace),ce=s.convert(ye.type),be=y(ye.internalFormat,Ye,ce,ye.colorSpace,L.isXRRenderTarget===!0),ze=Se(L);n.renderbufferStorageMultisample(n.RENDERBUFFER,ze,be,L.width,L.height),n.framebufferRenderbuffer(n.FRAMEBUFFER,n.COLOR_ATTACHMENT0+ge,n.RENDERBUFFER,j.__webglColorRenderbuffer[ge])}n.bindRenderbuffer(n.RENDERBUFFER,null),L.depthBuffer&&(j.__webglDepthRenderbuffer=n.createRenderbuffer(),re(j.__webglDepthRenderbuffer,L,!0)),t.bindFramebuffer(n.FRAMEBUFFER,null)}}if(J){t.bindTexture(n.TEXTURE_CUBE_MAP,Q.__webglTexture),he(n.TEXTURE_CUBE_MAP,S);for(let ge=0;ge<6;ge++)if(S.mipmaps&&S.mipmaps.length>0)for(let ye=0;ye<S.mipmaps.length;ye++)ue(j.__webglFramebuffer[ge][ye],L,S,n.COLOR_ATTACHMENT0,n.TEXTURE_CUBE_MAP_POSITIVE_X+ge,ye);else ue(j.__webglFramebuffer[ge],L,S,n.COLOR_ATTACHMENT0,n.TEXTURE_CUBE_MAP_POSITIVE_X+ge,0);p(S)&&u(n.TEXTURE_CUBE_MAP),t.unbindTexture()}else if(Re){for(let ge=0,ye=ie.length;ge<ye;ge++){const Ye=ie[ge],ce=i.get(Ye);t.bindTexture(n.TEXTURE_2D,ce.__webglTexture),he(n.TEXTURE_2D,Ye),ue(j.__webglFramebuffer,L,Ye,n.COLOR_ATTACHMENT0+ge,n.TEXTURE_2D,0),p(Ye)&&u(n.TEXTURE_2D)}t.unbindTexture()}else{let ge=n.TEXTURE_2D;if((L.isWebGL3DRenderTarget||L.isWebGLArrayRenderTarget)&&(ge=L.isWebGL3DRenderTarget?n.TEXTURE_3D:n.TEXTURE_2D_ARRAY),t.bindTexture(ge,Q.__webglTexture),he(ge,S),S.mipmaps&&S.mipmaps.length>0)for(let ye=0;ye<S.mipmaps.length;ye++)ue(j.__webglFramebuffer[ye],L,S,n.COLOR_ATTACHMENT0,ge,ye);else ue(j.__webglFramebuffer,L,S,n.COLOR_ATTACHMENT0,ge,0);p(S)&&u(ge),t.unbindTexture()}L.depthBuffer&&Pe(L)}function se(L){const S=L.textures;for(let j=0,Q=S.length;j<Q;j++){const ie=S[j];if(p(ie)){const J=E(L),Re=i.get(ie).__webglTexture;t.bindTexture(J,Re),u(J),t.unbindTexture()}}}const K=[],I=[];function Ce(L){if(L.samples>0){if(_e(L)===!1){const S=L.textures,j=L.width,Q=L.height;let ie=n.COLOR_BUFFER_BIT;const J=L.stencilBuffer?n.DEPTH_STENCIL_ATTACHMENT:n.DEPTH_ATTACHMENT,Re=i.get(L),ge=S.length>1;if(ge)for(let ye=0;ye<S.length;ye++)t.bindFramebuffer(n.FRAMEBUFFER,Re.__webglMultisampledFramebuffer),n.framebufferRenderbuffer(n.FRAMEBUFFER,n.COLOR_ATTACHMENT0+ye,n.RENDERBUFFER,null),t.bindFramebuffer(n.FRAMEBUFFER,Re.__webglFramebuffer),n.framebufferTexture2D(n.DRAW_FRAMEBUFFER,n.COLOR_ATTACHMENT0+ye,n.TEXTURE_2D,null,0);t.bindFramebuffer(n.READ_FRAMEBUFFER,Re.__webglMultisampledFramebuffer),t.bindFramebuffer(n.DRAW_FRAMEBUFFER,Re.__webglFramebuffer);for(let ye=0;ye<S.length;ye++){if(L.resolveDepthBuffer&&(L.depthBuffer&&(ie|=n.DEPTH_BUFFER_BIT),L.stencilBuffer&&L.resolveStencilBuffer&&(ie|=n.STENCIL_BUFFER_BIT)),ge){n.framebufferRenderbuffer(n.READ_FRAMEBUFFER,n.COLOR_ATTACHMENT0,n.RENDERBUFFER,Re.__webglColorRenderbuffer[ye]);const Ye=i.get(S[ye]).__webglTexture;n.framebufferTexture2D(n.DRAW_FRAMEBUFFER,n.COLOR_ATTACHMENT0,n.TEXTURE_2D,Ye,0)}n.blitFramebuffer(0,0,j,Q,0,0,j,Q,ie,n.NEAREST),c===!0&&(K.length=0,I.length=0,K.push(n.COLOR_ATTACHMENT0+ye),L.depthBuffer&&L.resolveDepthBuffer===!1&&(K.push(J),I.push(J),n.invalidateFramebuffer(n.DRAW_FRAMEBUFFER,I)),n.invalidateFramebuffer(n.READ_FRAMEBUFFER,K))}if(t.bindFramebuffer(n.READ_FRAMEBUFFER,null),t.bindFramebuffer(n.DRAW_FRAMEBUFFER,null),ge)for(let ye=0;ye<S.length;ye++){t.bindFramebuffer(n.FRAMEBUFFER,Re.__webglMultisampledFramebuffer),n.framebufferRenderbuffer(n.FRAMEBUFFER,n.COLOR_ATTACHMENT0+ye,n.RENDERBUFFER,Re.__webglColorRenderbuffer[ye]);const Ye=i.get(S[ye]).__webglTexture;t.bindFramebuffer(n.FRAMEBUFFER,Re.__webglFramebuffer),n.framebufferTexture2D(n.DRAW_FRAMEBUFFER,n.COLOR_ATTACHMENT0+ye,n.TEXTURE_2D,Ye,0)}t.bindFramebuffer(n.DRAW_FRAMEBUFFER,Re.__webglMultisampledFramebuffer)}else if(L.depthBuffer&&L.resolveDepthBuffer===!1&&c){const S=L.stencilBuffer?n.DEPTH_STENCIL_ATTACHMENT:n.DEPTH_ATTACHMENT;n.invalidateFramebuffer(n.DRAW_FRAMEBUFFER,[S])}}}function Se(L){return Math.min(r.maxSamples,L.samples)}function _e(L){const S=i.get(L);return L.samples>0&&e.has("WEBGL_multisampled_render_to_texture")===!0&&S.__useRenderToTexture!==!1}function ve(L){const S=a.render.frame;d.get(L)!==S&&(d.set(L,S),L.update())}function Ne(L,S){const j=L.colorSpace,Q=L.format,ie=L.type;return L.isCompressedTexture===!0||L.isVideoTexture===!0||j!==Ii&&j!==An&&(Je.getTransfer(j)===it?(Q!==Gt||ie!==pn)&&console.warn("THREE.WebGLTextures: sRGB encoded textures have to use RGBAFormat and UnsignedByteType."):console.error("THREE.WebGLTextures: Unsupported texture color space:",j)),S}function we(L){return typeof HTMLImageElement<"u"&&L instanceof HTMLImageElement?(l.width=L.naturalWidth||L.width,l.height=L.naturalHeight||L.height):typeof VideoFrame<"u"&&L instanceof VideoFrame?(l.width=L.displayWidth,l.height=L.displayHeight):(l.width=L.width,l.height=L.height),l}this.allocateTextureUnit=A,this.resetTextureUnits=U,this.setTexture2D=z,this.setTexture2DArray=N,this.setTexture3D=O,this.setTextureCube=F,this.rebindTextures=me,this.setupRenderTarget=te,this.updateRenderTargetMipmap=se,this.updateMultisampleRenderTarget=Ce,this.setupDepthRenderbuffer=Pe,this.setupFrameBufferTexture=ue,this.useMultisampledRTT=_e}function xm(n,e){function t(i,r=An){let s;const a=Je.getTransfer(r);if(i===pn)return n.UNSIGNED_BYTE;if(i===Ua)return n.UNSIGNED_SHORT_4_4_4_4;if(i===za)return n.UNSIGNED_SHORT_5_5_5_1;if(i===Lc)return n.UNSIGNED_INT_5_9_9_9_REV;if(i===Pc)return n.BYTE;if(i===Dc)return n.SHORT;if(i===Zi)return n.UNSIGNED_SHORT;if(i===Ia)return n.INT;if(i===Qn)return n.UNSIGNED_INT;if(i===dn)return n.FLOAT;if(i===nr)return n.HALF_FLOAT;if(i===Ic)return n.ALPHA;if(i===Uc)return n.RGB;if(i===Gt)return n.RGBA;if(i===zc)return n.LUMINANCE;if(i===Nc)return n.LUMINANCE_ALPHA;if(i===Ai)return n.DEPTH_COMPONENT;if(i===Li)return n.DEPTH_STENCIL;if(i===Fc)return n.RED;if(i===Na)return n.RED_INTEGER;if(i===kc)return n.RG;if(i===Fa)return n.RG_INTEGER;if(i===ka)return n.RGBA_INTEGER;if(i===zr||i===Nr||i===Fr||i===kr)if(a===it)if(s=e.get("WEBGL_compressed_texture_s3tc_srgb"),s!==null){if(i===zr)return s.COMPRESSED_SRGB_S3TC_DXT1_EXT;if(i===Nr)return s.COMPRESSED_SRGB_ALPHA_S3TC_DXT1_EXT;if(i===Fr)return s.COMPRESSED_SRGB_ALPHA_S3TC_DXT3_EXT;if(i===kr)return s.COMPRESSED_SRGB_ALPHA_S3TC_DXT5_EXT}else return null;else if(s=e.get("WEBGL_compressed_texture_s3tc"),s!==null){if(i===zr)return s.COMPRESSED_RGB_S3TC_DXT1_EXT;if(i===Nr)return s.COMPRESSED_RGBA_S3TC_DXT1_EXT;if(i===Fr)return s.COMPRESSED_RGBA_S3TC_DXT3_EXT;if(i===kr)return s.COMPRESSED_RGBA_S3TC_DXT5_EXT}else return null;if(i===Zs||i===Js||i===Qs||i===ea)if(s=e.get("WEBGL_compressed_texture_pvrtc"),s!==null){if(i===Zs)return s.COMPRESSED_RGB_PVRTC_4BPPV1_IMG;if(i===Js)return s.COMPRESSED_RGB_PVRTC_2BPPV1_IMG;if(i===Qs)return s.COMPRESSED_RGBA_PVRTC_4BPPV1_IMG;if(i===ea)return s.COMPRESSED_RGBA_PVRTC_2BPPV1_IMG}else return null;if(i===ta||i===na||i===ia)if(s=e.get("WEBGL_compressed_texture_etc"),s!==null){if(i===ta||i===na)return a===it?s.COMPRESSED_SRGB8_ETC2:s.COMPRESSED_RGB8_ETC2;if(i===ia)return a===it?s.COMPRESSED_SRGB8_ALPHA8_ETC2_EAC:s.COMPRESSED_RGBA8_ETC2_EAC}else return null;if(i===ra||i===sa||i===aa||i===oa||i===ca||i===la||i===ua||i===da||i===ha||i===fa||i===pa||i===ma||i===ga||i===_a)if(s=e.get("WEBGL_compressed_texture_astc"),s!==null){if(i===ra)return a===it?s.COMPRESSED_SRGB8_ALPHA8_ASTC_4x4_KHR:s.COMPRESSED_RGBA_ASTC_4x4_KHR;if(i===sa)return a===it?s.COMPRESSED_SRGB8_ALPHA8_ASTC_5x4_KHR:s.COMPRESSED_RGBA_ASTC_5x4_KHR;if(i===aa)return a===it?s.COMPRESSED_SRGB8_ALPHA8_ASTC_5x5_KHR:s.COMPRESSED_RGBA_ASTC_5x5_KHR;if(i===oa)return a===it?s.COMPRESSED_SRGB8_ALPHA8_ASTC_6x5_KHR:s.COMPRESSED_RGBA_ASTC_6x5_KHR;if(i===ca)return a===it?s.COMPRESSED_SRGB8_ALPHA8_ASTC_6x6_KHR:s.COMPRESSED_RGBA_ASTC_6x6_KHR;if(i===la)return a===it?s.COMPRESSED_SRGB8_ALPHA8_ASTC_8x5_KHR:s.COMPRESSED_RGBA_ASTC_8x5_KHR;if(i===ua)return a===it?s.COMPRESSED_SRGB8_ALPHA8_ASTC_8x6_KHR:s.COMPRESSED_RGBA_ASTC_8x6_KHR;if(i===da)return a===it?s.COMPRESSED_SRGB8_ALPHA8_ASTC_8x8_KHR:s.COMPRESSED_RGBA_ASTC_8x8_KHR;if(i===ha)return a===it?s.COMPRESSED_SRGB8_ALPHA8_ASTC_10x5_KHR:s.COMPRESSED_RGBA_ASTC_10x5_KHR;if(i===fa)return a===it?s.COMPRESSED_SRGB8_ALPHA8_ASTC_10x6_KHR:s.COMPRESSED_RGBA_ASTC_10x6_KHR;if(i===pa)return a===it?s.COMPRESSED_SRGB8_ALPHA8_ASTC_10x8_KHR:s.COMPRESSED_RGBA_ASTC_10x8_KHR;if(i===ma)return a===it?s.COMPRESSED_SRGB8_ALPHA8_ASTC_10x10_KHR:s.COMPRESSED_RGBA_ASTC_10x10_KHR;if(i===ga)return a===it?s.COMPRESSED_SRGB8_ALPHA8_ASTC_12x10_KHR:s.COMPRESSED_RGBA_ASTC_12x10_KHR;if(i===_a)return a===it?s.COMPRESSED_SRGB8_ALPHA8_ASTC_12x12_KHR:s.COMPRESSED_RGBA_ASTC_12x12_KHR}else return null;if(i===Or||i===va||i===xa)if(s=e.get("EXT_texture_compression_bptc"),s!==null){if(i===Or)return a===it?s.COMPRESSED_SRGB_ALPHA_BPTC_UNORM_EXT:s.COMPRESSED_RGBA_BPTC_UNORM_EXT;if(i===va)return s.COMPRESSED_RGB_BPTC_SIGNED_FLOAT_EXT;if(i===xa)return s.COMPRESSED_RGB_BPTC_UNSIGNED_FLOAT_EXT}else return null;if(i===Oc||i===Ma||i===Sa||i===Ea)if(s=e.get("EXT_texture_compression_rgtc"),s!==null){if(i===Or)return s.COMPRESSED_RED_RGTC1_EXT;if(i===Ma)return s.COMPRESSED_SIGNED_RED_RGTC1_EXT;if(i===Sa)return s.COMPRESSED_RED_GREEN_RGTC2_EXT;if(i===Ea)return s.COMPRESSED_SIGNED_RED_GREEN_RGTC2_EXT}else return null;return i===Di?n.UNSIGNED_INT_24_8:n[i]!==void 0?n[i]:null}return{convert:t}}const Mm=`
void main() {

	gl_Position = vec4( position, 1.0 );

}`,Sm=`
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

}`;class Em{constructor(){this.texture=null,this.mesh=null,this.depthNear=0,this.depthFar=0}init(e,t,i){if(this.texture===null){const r=new At,s=e.properties.get(r);s.__webglTexture=t.texture,(t.depthNear!==i.depthNear||t.depthFar!==i.depthFar)&&(this.depthNear=t.depthNear,this.depthFar=t.depthFar),this.texture=r}}getMesh(e){if(this.texture!==null&&this.mesh===null){const t=e.cameras[0].viewport,i=new Dn({vertexShader:Mm,fragmentShader:Sm,uniforms:{depthColor:{value:this.texture},depthWidth:{value:t.z},depthHeight:{value:t.w}}});this.mesh=new Le(new ni(20,20),i)}return this.mesh}reset(){this.texture=null,this.mesh=null}getDepthTexture(){return this.texture}}class ym extends Ni{constructor(e,t){super();const i=this;let r=null,s=1,a=null,o="local-floor",c=1,l=null,d=null,h=null,f=null,m=null,g=null;const _=new Em,p=t.getContextAttributes();let u=null,E=null;const y=[],M=[],D=new We;let w=null;const b=new Ft;b.viewport=new rt;const C=new Ft;C.viewport=new rt;const v=[b,C],x=new Gu;let P=null,U=null;this.cameraAutoUpdate=!0,this.enabled=!1,this.isPresenting=!1,this.getController=function(X){let ee=y[X];return ee===void 0&&(ee=new Ms,y[X]=ee),ee.getTargetRaySpace()},this.getControllerGrip=function(X){let ee=y[X];return ee===void 0&&(ee=new Ms,y[X]=ee),ee.getGripSpace()},this.getHand=function(X){let ee=y[X];return ee===void 0&&(ee=new Ms,y[X]=ee),ee.getHandSpace()};function A(X){const ee=M.indexOf(X.inputSource);if(ee===-1)return;const ue=y[ee];ue!==void 0&&(ue.update(X.inputSource,X.frame,l||a),ue.dispatchEvent({type:X.type,data:X.inputSource}))}function R(){r.removeEventListener("select",A),r.removeEventListener("selectstart",A),r.removeEventListener("selectend",A),r.removeEventListener("squeeze",A),r.removeEventListener("squeezestart",A),r.removeEventListener("squeezeend",A),r.removeEventListener("end",R),r.removeEventListener("inputsourceschange",z);for(let X=0;X<y.length;X++){const ee=M[X];ee!==null&&(M[X]=null,y[X].disconnect(ee))}P=null,U=null,_.reset(),e.setRenderTarget(u),m=null,f=null,h=null,r=null,E=null,Ie.stop(),i.isPresenting=!1,e.setPixelRatio(w),e.setSize(D.width,D.height,!1),i.dispatchEvent({type:"sessionend"})}this.setFramebufferScaleFactor=function(X){s=X,i.isPresenting===!0&&console.warn("THREE.WebXRManager: Cannot change framebuffer scale while presenting.")},this.setReferenceSpaceType=function(X){o=X,i.isPresenting===!0&&console.warn("THREE.WebXRManager: Cannot change reference space type while presenting.")},this.getReferenceSpace=function(){return l||a},this.setReferenceSpace=function(X){l=X},this.getBaseLayer=function(){return f!==null?f:m},this.getBinding=function(){return h},this.getFrame=function(){return g},this.getSession=function(){return r},this.setSession=async function(X){if(r=X,r!==null){if(u=e.getRenderTarget(),r.addEventListener("select",A),r.addEventListener("selectstart",A),r.addEventListener("selectend",A),r.addEventListener("squeeze",A),r.addEventListener("squeezestart",A),r.addEventListener("squeezeend",A),r.addEventListener("end",R),r.addEventListener("inputsourceschange",z),p.xrCompatible!==!0&&await t.makeXRCompatible(),w=e.getPixelRatio(),e.getSize(D),typeof XRWebGLBinding<"u"&&"createProjectionLayer"in XRWebGLBinding.prototype){let ue=null,re=null,le=null;p.depth&&(le=p.stencil?t.DEPTH24_STENCIL8:t.DEPTH_COMPONENT24,ue=p.stencil?Li:Ai,re=p.stencil?Di:Qn);const Pe={colorFormat:t.RGBA8,depthFormat:le,scaleFactor:s};h=new XRWebGLBinding(r,t),f=h.createProjectionLayer(Pe),r.updateRenderState({layers:[f]}),e.setPixelRatio(1),e.setSize(f.textureWidth,f.textureHeight,!1),E=new ei(f.textureWidth,f.textureHeight,{format:Gt,type:pn,depthTexture:new Zc(f.textureWidth,f.textureHeight,re,void 0,void 0,void 0,void 0,void 0,void 0,ue),stencilBuffer:p.stencil,colorSpace:e.outputColorSpace,samples:p.antialias?4:0,resolveDepthBuffer:f.ignoreDepthValues===!1,resolveStencilBuffer:f.ignoreDepthValues===!1})}else{const ue={antialias:p.antialias,alpha:!0,depth:p.depth,stencil:p.stencil,framebufferScaleFactor:s};m=new XRWebGLLayer(r,t,ue),r.updateRenderState({baseLayer:m}),e.setPixelRatio(1),e.setSize(m.framebufferWidth,m.framebufferHeight,!1),E=new ei(m.framebufferWidth,m.framebufferHeight,{format:Gt,type:pn,colorSpace:e.outputColorSpace,stencilBuffer:p.stencil,resolveDepthBuffer:m.ignoreDepthValues===!1,resolveStencilBuffer:m.ignoreDepthValues===!1})}E.isXRRenderTarget=!0,this.setFoveation(c),l=null,a=await r.requestReferenceSpace(o),Ie.setContext(r),Ie.start(),i.isPresenting=!0,i.dispatchEvent({type:"sessionstart"})}},this.getEnvironmentBlendMode=function(){if(r!==null)return r.environmentBlendMode},this.getDepthTexture=function(){return _.getDepthTexture()};function z(X){for(let ee=0;ee<X.removed.length;ee++){const ue=X.removed[ee],re=M.indexOf(ue);re>=0&&(M[re]=null,y[re].disconnect(ue))}for(let ee=0;ee<X.added.length;ee++){const ue=X.added[ee];let re=M.indexOf(ue);if(re===-1){for(let Pe=0;Pe<y.length;Pe++)if(Pe>=M.length){M.push(ue),re=Pe;break}else if(M[Pe]===null){M[Pe]=ue,re=Pe;break}if(re===-1)break}const le=y[re];le&&le.connect(ue)}}const N=new k,O=new k;function F(X,ee,ue){N.setFromMatrixPosition(ee.matrixWorld),O.setFromMatrixPosition(ue.matrixWorld);const re=N.distanceTo(O),le=ee.projectionMatrix.elements,Pe=ue.projectionMatrix.elements,me=le[14]/(le[10]-1),te=le[14]/(le[10]+1),se=(le[9]+1)/le[5],K=(le[9]-1)/le[5],I=(le[8]-1)/le[0],Ce=(Pe[8]+1)/Pe[0],Se=me*I,_e=me*Ce,ve=re/(-I+Ce),Ne=ve*-I;if(ee.matrixWorld.decompose(X.position,X.quaternion,X.scale),X.translateX(Ne),X.translateZ(ve),X.matrixWorld.compose(X.position,X.quaternion,X.scale),X.matrixWorldInverse.copy(X.matrixWorld).invert(),le[10]===-1)X.projectionMatrix.copy(ee.projectionMatrix),X.projectionMatrixInverse.copy(ee.projectionMatrixInverse);else{const we=me+ve,L=te+ve,S=Se-Ne,j=_e+(re-Ne),Q=se*te/L*we,ie=K*te/L*we;X.projectionMatrix.makePerspective(S,j,Q,ie,we,L),X.projectionMatrixInverse.copy(X.projectionMatrix).invert()}}function G(X,ee){ee===null?X.matrixWorld.copy(X.matrix):X.matrixWorld.multiplyMatrices(ee.matrixWorld,X.matrix),X.matrixWorldInverse.copy(X.matrixWorld).invert()}this.updateCamera=function(X){if(r===null)return;let ee=X.near,ue=X.far;_.texture!==null&&(_.depthNear>0&&(ee=_.depthNear),_.depthFar>0&&(ue=_.depthFar)),x.near=C.near=b.near=ee,x.far=C.far=b.far=ue,(P!==x.near||U!==x.far)&&(r.updateRenderState({depthNear:x.near,depthFar:x.far}),P=x.near,U=x.far),b.layers.mask=X.layers.mask|2,C.layers.mask=X.layers.mask|4,x.layers.mask=b.layers.mask|C.layers.mask;const re=X.parent,le=x.cameras;G(x,re);for(let Pe=0;Pe<le.length;Pe++)G(le[Pe],re);le.length===2?F(x,b,C):x.projectionMatrix.copy(b.projectionMatrix),Z(X,x,re)};function Z(X,ee,ue){ue===null?X.matrix.copy(ee.matrixWorld):(X.matrix.copy(ue.matrixWorld),X.matrix.invert(),X.matrix.multiply(ee.matrixWorld)),X.matrix.decompose(X.position,X.quaternion,X.scale),X.updateMatrixWorld(!0),X.projectionMatrix.copy(ee.projectionMatrix),X.projectionMatrixInverse.copy(ee.projectionMatrixInverse),X.isPerspectiveCamera&&(X.fov=ya*2*Math.atan(1/X.projectionMatrix.elements[5]),X.zoom=1)}this.getCamera=function(){return x},this.getFoveation=function(){if(!(f===null&&m===null))return c},this.setFoveation=function(X){c=X,f!==null&&(f.fixedFoveation=X),m!==null&&m.fixedFoveation!==void 0&&(m.fixedFoveation=X)},this.hasDepthSensing=function(){return _.texture!==null},this.getDepthSensingMesh=function(){return _.getMesh(x)};let Y=null;function he(X,ee){if(d=ee.getViewerPose(l||a),g=ee,d!==null){const ue=d.views;m!==null&&(e.setRenderTargetFramebuffer(E,m.framebuffer),e.setRenderTarget(E));let re=!1;ue.length!==x.cameras.length&&(x.cameras.length=0,re=!0);for(let me=0;me<ue.length;me++){const te=ue[me];let se=null;if(m!==null)se=m.getViewport(te);else{const I=h.getViewSubImage(f,te);se=I.viewport,me===0&&(e.setRenderTargetTextures(E,I.colorTexture,f.ignoreDepthValues?void 0:I.depthStencilTexture),e.setRenderTarget(E))}let K=v[me];K===void 0&&(K=new Ft,K.layers.enable(me),K.viewport=new rt,v[me]=K),K.matrix.fromArray(te.transform.matrix),K.matrix.decompose(K.position,K.quaternion,K.scale),K.projectionMatrix.fromArray(te.projectionMatrix),K.projectionMatrixInverse.copy(K.projectionMatrix).invert(),K.viewport.set(se.x,se.y,se.width,se.height),me===0&&(x.matrix.copy(K.matrix),x.matrix.decompose(x.position,x.quaternion,x.scale)),re===!0&&x.cameras.push(K)}const le=r.enabledFeatures;if(le&&le.includes("depth-sensing")&&r.depthUsage=="gpu-optimized"&&h){const me=h.getDepthInformation(ue[0]);me&&me.isValid&&me.texture&&_.init(e,me,r.renderState)}}for(let ue=0;ue<y.length;ue++){const re=M[ue],le=y[ue];re!==null&&le!==void 0&&le.update(re,ee,l||a)}Y&&Y(X,ee),ee.detectedPlanes&&i.dispatchEvent({type:"planesdetected",data:ee}),g=null}const Ie=new el;Ie.setAnimationLoop(he),this.setAnimationLoop=function(X){Y=X},this.dispose=function(){}}}const Bn=new xt,bm=new at;function Tm(n,e){function t(p,u){p.matrixAutoUpdate===!0&&p.updateMatrix(),u.value.copy(p.matrix)}function i(p,u){u.color.getRGB(p.fogColor.value,qc(n)),u.isFog?(p.fogNear.value=u.near,p.fogFar.value=u.far):u.isFogExp2&&(p.fogDensity.value=u.density)}function r(p,u,E,y,M){u.isMeshBasicMaterial||u.isMeshLambertMaterial?s(p,u):u.isMeshToonMaterial?(s(p,u),h(p,u)):u.isMeshPhongMaterial?(s(p,u),d(p,u)):u.isMeshStandardMaterial?(s(p,u),f(p,u),u.isMeshPhysicalMaterial&&m(p,u,M)):u.isMeshMatcapMaterial?(s(p,u),g(p,u)):u.isMeshDepthMaterial?s(p,u):u.isMeshDistanceMaterial?(s(p,u),_(p,u)):u.isMeshNormalMaterial?s(p,u):u.isLineBasicMaterial?(a(p,u),u.isLineDashedMaterial&&o(p,u)):u.isPointsMaterial?c(p,u,E,y):u.isSpriteMaterial?l(p,u):u.isShadowMaterial?(p.color.value.copy(u.color),p.opacity.value=u.opacity):u.isShaderMaterial&&(u.uniformsNeedUpdate=!1)}function s(p,u){p.opacity.value=u.opacity,u.color&&p.diffuse.value.copy(u.color),u.emissive&&p.emissive.value.copy(u.emissive).multiplyScalar(u.emissiveIntensity),u.map&&(p.map.value=u.map,t(u.map,p.mapTransform)),u.alphaMap&&(p.alphaMap.value=u.alphaMap,t(u.alphaMap,p.alphaMapTransform)),u.bumpMap&&(p.bumpMap.value=u.bumpMap,t(u.bumpMap,p.bumpMapTransform),p.bumpScale.value=u.bumpScale,u.side===Ct&&(p.bumpScale.value*=-1)),u.normalMap&&(p.normalMap.value=u.normalMap,t(u.normalMap,p.normalMapTransform),p.normalScale.value.copy(u.normalScale),u.side===Ct&&p.normalScale.value.negate()),u.displacementMap&&(p.displacementMap.value=u.displacementMap,t(u.displacementMap,p.displacementMapTransform),p.displacementScale.value=u.displacementScale,p.displacementBias.value=u.displacementBias),u.emissiveMap&&(p.emissiveMap.value=u.emissiveMap,t(u.emissiveMap,p.emissiveMapTransform)),u.specularMap&&(p.specularMap.value=u.specularMap,t(u.specularMap,p.specularMapTransform)),u.alphaTest>0&&(p.alphaTest.value=u.alphaTest);const E=e.get(u),y=E.envMap,M=E.envMapRotation;y&&(p.envMap.value=y,Bn.copy(M),Bn.x*=-1,Bn.y*=-1,Bn.z*=-1,y.isCubeTexture&&y.isRenderTargetTexture===!1&&(Bn.y*=-1,Bn.z*=-1),p.envMapRotation.value.setFromMatrix4(bm.makeRotationFromEuler(Bn)),p.flipEnvMap.value=y.isCubeTexture&&y.isRenderTargetTexture===!1?-1:1,p.reflectivity.value=u.reflectivity,p.ior.value=u.ior,p.refractionRatio.value=u.refractionRatio),u.lightMap&&(p.lightMap.value=u.lightMap,p.lightMapIntensity.value=u.lightMapIntensity,t(u.lightMap,p.lightMapTransform)),u.aoMap&&(p.aoMap.value=u.aoMap,p.aoMapIntensity.value=u.aoMapIntensity,t(u.aoMap,p.aoMapTransform))}function a(p,u){p.diffuse.value.copy(u.color),p.opacity.value=u.opacity,u.map&&(p.map.value=u.map,t(u.map,p.mapTransform))}function o(p,u){p.dashSize.value=u.dashSize,p.totalSize.value=u.dashSize+u.gapSize,p.scale.value=u.scale}function c(p,u,E,y){p.diffuse.value.copy(u.color),p.opacity.value=u.opacity,p.size.value=u.size*E,p.scale.value=y*.5,u.map&&(p.map.value=u.map,t(u.map,p.uvTransform)),u.alphaMap&&(p.alphaMap.value=u.alphaMap,t(u.alphaMap,p.alphaMapTransform)),u.alphaTest>0&&(p.alphaTest.value=u.alphaTest)}function l(p,u){p.diffuse.value.copy(u.color),p.opacity.value=u.opacity,p.rotation.value=u.rotation,u.map&&(p.map.value=u.map,t(u.map,p.mapTransform)),u.alphaMap&&(p.alphaMap.value=u.alphaMap,t(u.alphaMap,p.alphaMapTransform)),u.alphaTest>0&&(p.alphaTest.value=u.alphaTest)}function d(p,u){p.specular.value.copy(u.specular),p.shininess.value=Math.max(u.shininess,1e-4)}function h(p,u){u.gradientMap&&(p.gradientMap.value=u.gradientMap)}function f(p,u){p.metalness.value=u.metalness,u.metalnessMap&&(p.metalnessMap.value=u.metalnessMap,t(u.metalnessMap,p.metalnessMapTransform)),p.roughness.value=u.roughness,u.roughnessMap&&(p.roughnessMap.value=u.roughnessMap,t(u.roughnessMap,p.roughnessMapTransform)),u.envMap&&(p.envMapIntensity.value=u.envMapIntensity)}function m(p,u,E){p.ior.value=u.ior,u.sheen>0&&(p.sheenColor.value.copy(u.sheenColor).multiplyScalar(u.sheen),p.sheenRoughness.value=u.sheenRoughness,u.sheenColorMap&&(p.sheenColorMap.value=u.sheenColorMap,t(u.sheenColorMap,p.sheenColorMapTransform)),u.sheenRoughnessMap&&(p.sheenRoughnessMap.value=u.sheenRoughnessMap,t(u.sheenRoughnessMap,p.sheenRoughnessMapTransform))),u.clearcoat>0&&(p.clearcoat.value=u.clearcoat,p.clearcoatRoughness.value=u.clearcoatRoughness,u.clearcoatMap&&(p.clearcoatMap.value=u.clearcoatMap,t(u.clearcoatMap,p.clearcoatMapTransform)),u.clearcoatRoughnessMap&&(p.clearcoatRoughnessMap.value=u.clearcoatRoughnessMap,t(u.clearcoatRoughnessMap,p.clearcoatRoughnessMapTransform)),u.clearcoatNormalMap&&(p.clearcoatNormalMap.value=u.clearcoatNormalMap,t(u.clearcoatNormalMap,p.clearcoatNormalMapTransform),p.clearcoatNormalScale.value.copy(u.clearcoatNormalScale),u.side===Ct&&p.clearcoatNormalScale.value.negate())),u.dispersion>0&&(p.dispersion.value=u.dispersion),u.iridescence>0&&(p.iridescence.value=u.iridescence,p.iridescenceIOR.value=u.iridescenceIOR,p.iridescenceThicknessMinimum.value=u.iridescenceThicknessRange[0],p.iridescenceThicknessMaximum.value=u.iridescenceThicknessRange[1],u.iridescenceMap&&(p.iridescenceMap.value=u.iridescenceMap,t(u.iridescenceMap,p.iridescenceMapTransform)),u.iridescenceThicknessMap&&(p.iridescenceThicknessMap.value=u.iridescenceThicknessMap,t(u.iridescenceThicknessMap,p.iridescenceThicknessMapTransform))),u.transmission>0&&(p.transmission.value=u.transmission,p.transmissionSamplerMap.value=E.texture,p.transmissionSamplerSize.value.set(E.width,E.height),u.transmissionMap&&(p.transmissionMap.value=u.transmissionMap,t(u.transmissionMap,p.transmissionMapTransform)),p.thickness.value=u.thickness,u.thicknessMap&&(p.thicknessMap.value=u.thicknessMap,t(u.thicknessMap,p.thicknessMapTransform)),p.attenuationDistance.value=u.attenuationDistance,p.attenuationColor.value.copy(u.attenuationColor)),u.anisotropy>0&&(p.anisotropyVector.value.set(u.anisotropy*Math.cos(u.anisotropyRotation),u.anisotropy*Math.sin(u.anisotropyRotation)),u.anisotropyMap&&(p.anisotropyMap.value=u.anisotropyMap,t(u.anisotropyMap,p.anisotropyMapTransform))),p.specularIntensity.value=u.specularIntensity,p.specularColor.value.copy(u.specularColor),u.specularColorMap&&(p.specularColorMap.value=u.specularColorMap,t(u.specularColorMap,p.specularColorMapTransform)),u.specularIntensityMap&&(p.specularIntensityMap.value=u.specularIntensityMap,t(u.specularIntensityMap,p.specularIntensityMapTransform))}function g(p,u){u.matcap&&(p.matcap.value=u.matcap)}function _(p,u){const E=e.get(u).light;p.referencePosition.value.setFromMatrixPosition(E.matrixWorld),p.nearDistance.value=E.shadow.camera.near,p.farDistance.value=E.shadow.camera.far}return{refreshFogUniforms:i,refreshMaterialUniforms:r}}function Am(n,e,t,i){let r={},s={},a=[];const o=n.getParameter(n.MAX_UNIFORM_BUFFER_BINDINGS);function c(E,y){const M=y.program;i.uniformBlockBinding(E,M)}function l(E,y){let M=r[E.id];M===void 0&&(g(E),M=d(E),r[E.id]=M,E.addEventListener("dispose",p));const D=y.program;i.updateUBOMapping(E,D);const w=e.render.frame;s[E.id]!==w&&(f(E),s[E.id]=w)}function d(E){const y=h();E.__bindingPointIndex=y;const M=n.createBuffer(),D=E.__size,w=E.usage;return n.bindBuffer(n.UNIFORM_BUFFER,M),n.bufferData(n.UNIFORM_BUFFER,D,w),n.bindBuffer(n.UNIFORM_BUFFER,null),n.bindBufferBase(n.UNIFORM_BUFFER,y,M),M}function h(){for(let E=0;E<o;E++)if(a.indexOf(E)===-1)return a.push(E),E;return console.error("THREE.WebGLRenderer: Maximum number of simultaneously usable uniforms groups reached."),0}function f(E){const y=r[E.id],M=E.uniforms,D=E.__cache;n.bindBuffer(n.UNIFORM_BUFFER,y);for(let w=0,b=M.length;w<b;w++){const C=Array.isArray(M[w])?M[w]:[M[w]];for(let v=0,x=C.length;v<x;v++){const P=C[v];if(m(P,w,v,D)===!0){const U=P.__offset,A=Array.isArray(P.value)?P.value:[P.value];let R=0;for(let z=0;z<A.length;z++){const N=A[z],O=_(N);typeof N=="number"||typeof N=="boolean"?(P.__data[0]=N,n.bufferSubData(n.UNIFORM_BUFFER,U+R,P.__data)):N.isMatrix3?(P.__data[0]=N.elements[0],P.__data[1]=N.elements[1],P.__data[2]=N.elements[2],P.__data[3]=0,P.__data[4]=N.elements[3],P.__data[5]=N.elements[4],P.__data[6]=N.elements[5],P.__data[7]=0,P.__data[8]=N.elements[6],P.__data[9]=N.elements[7],P.__data[10]=N.elements[8],P.__data[11]=0):(N.toArray(P.__data,R),R+=O.storage/Float32Array.BYTES_PER_ELEMENT)}n.bufferSubData(n.UNIFORM_BUFFER,U,P.__data)}}}n.bindBuffer(n.UNIFORM_BUFFER,null)}function m(E,y,M,D){const w=E.value,b=y+"_"+M;if(D[b]===void 0)return typeof w=="number"||typeof w=="boolean"?D[b]=w:D[b]=w.clone(),!0;{const C=D[b];if(typeof w=="number"||typeof w=="boolean"){if(C!==w)return D[b]=w,!0}else if(C.equals(w)===!1)return C.copy(w),!0}return!1}function g(E){const y=E.uniforms;let M=0;const D=16;for(let b=0,C=y.length;b<C;b++){const v=Array.isArray(y[b])?y[b]:[y[b]];for(let x=0,P=v.length;x<P;x++){const U=v[x],A=Array.isArray(U.value)?U.value:[U.value];for(let R=0,z=A.length;R<z;R++){const N=A[R],O=_(N),F=M%D,G=F%O.boundary,Z=F+G;M+=G,Z!==0&&D-Z<O.storage&&(M+=D-Z),U.__data=new Float32Array(O.storage/Float32Array.BYTES_PER_ELEMENT),U.__offset=M,M+=O.storage}}}const w=M%D;return w>0&&(M+=D-w),E.__size=M,E.__cache={},this}function _(E){const y={boundary:0,storage:0};return typeof E=="number"||typeof E=="boolean"?(y.boundary=4,y.storage=4):E.isVector2?(y.boundary=8,y.storage=8):E.isVector3||E.isColor?(y.boundary=16,y.storage=12):E.isVector4?(y.boundary=16,y.storage=16):E.isMatrix3?(y.boundary=48,y.storage=48):E.isMatrix4?(y.boundary=64,y.storage=64):E.isTexture?console.warn("THREE.WebGLRenderer: Texture samplers can not be part of an uniforms group."):console.warn("THREE.WebGLRenderer: Unsupported uniform value type.",E),y}function p(E){const y=E.target;y.removeEventListener("dispose",p);const M=a.indexOf(y.__bindingPointIndex);a.splice(M,1),n.deleteBuffer(r[y.id]),delete r[y.id],delete s[y.id]}function u(){for(const E in r)n.deleteBuffer(r[E]);a=[],r={},s={}}return{bind:c,update:l,dispose:u}}class wm{constructor(e={}){const{canvas:t=ru(),context:i=null,depth:r=!0,stencil:s=!1,alpha:a=!1,antialias:o=!1,premultipliedAlpha:c=!0,preserveDrawingBuffer:l=!1,powerPreference:d="default",failIfMajorPerformanceCaveat:h=!1,reverseDepthBuffer:f=!1}=e;this.isWebGLRenderer=!0;let m;if(i!==null){if(typeof WebGLRenderingContext<"u"&&i instanceof WebGLRenderingContext)throw new Error("THREE.WebGLRenderer: WebGL 1 is not supported since r163.");m=i.getContextAttributes().alpha}else m=a;const g=new Uint32Array(4),_=new Int32Array(4);let p=null,u=null;const E=[],y=[];this.domElement=t,this.debug={checkShaderErrors:!0,onShaderError:null},this.autoClear=!0,this.autoClearColor=!0,this.autoClearDepth=!0,this.autoClearStencil=!0,this.sortObjects=!0,this.clippingPlanes=[],this.localClippingEnabled=!1,this._outputColorSpace=Nt,this.toneMapping=Cn,this.toneMappingExposure=1;const M=this;let D=!1,w=0,b=0,C=null,v=-1,x=null;const P=new rt,U=new rt;let A=null;const R=new oe(0);let z=0,N=t.width,O=t.height,F=1,G=null,Z=null;const Y=new rt(0,0,N,O),he=new rt(0,0,N,O);let Ie=!1;const X=new Ha;let ee=!1,ue=!1;this.transmissionResolutionScale=1;const re=new at,le=new at,Pe=new k,me=new rt,te={background:null,fog:null,environment:null,overrideMaterial:null,isScene:!0};let se=!1;function K(){return C===null?F:1}let I=i;function Ce(T,V){return t.getContext(T,V)}try{const T={alpha:!0,depth:r,stencil:s,antialias:o,premultipliedAlpha:c,preserveDrawingBuffer:l,powerPreference:d,failIfMajorPerformanceCaveat:h};if("setAttribute"in t&&t.setAttribute("data-engine",`three.js r${La}`),t.addEventListener("webglcontextlost",ne,!1),t.addEventListener("webglcontextrestored",Me,!1),t.addEventListener("webglcontextcreationerror",xe,!1),I===null){const V="webgl2";if(I=Ce(V,T),I===null)throw Ce(V)?new Error("Error creating WebGL context with your selected attributes."):new Error("Error creating WebGL context.")}}catch(T){throw console.error("THREE.WebGLRenderer: "+T.message),T}let Se,_e,ve,Ne,we,L,S,j,Q,ie,J,Re,ge,ye,Ye,ce,be,ze,Fe,Te,qe,He,st,B;function fe(){Se=new Ff(I),Se.init(),He=new xm(I,Se),_e=new Pf(I,Se,e,He),ve=new _m(I,Se),_e.reverseDepthBuffer&&f&&ve.buffers.depth.setReversed(!0),Ne=new Bf(I),we=new rm,L=new vm(I,Se,ve,we,_e,He,Ne),S=new Lf(M),j=new Nf(M),Q=new Wu(I),st=new Rf(I,Q),ie=new kf(I,Q,Ne,st),J=new Hf(I,ie,Q,Ne),Fe=new Vf(I,_e,L),ce=new Df(we),Re=new im(M,S,j,Se,_e,st,ce),ge=new Tm(M,we),ye=new am,Ye=new hm(Se),ze=new wf(M,S,j,ve,J,m,c),be=new mm(M,J,_e),B=new Am(I,Ne,_e,ve),Te=new Cf(I,Se,Ne),qe=new Of(I,Se,Ne),Ne.programs=Re.programs,M.capabilities=_e,M.extensions=Se,M.properties=we,M.renderLists=ye,M.shadowMap=be,M.state=ve,M.info=Ne}fe();const $=new ym(M,I);this.xr=$,this.getContext=function(){return I},this.getContextAttributes=function(){return I.getContextAttributes()},this.forceContextLoss=function(){const T=Se.get("WEBGL_lose_context");T&&T.loseContext()},this.forceContextRestore=function(){const T=Se.get("WEBGL_lose_context");T&&T.restoreContext()},this.getPixelRatio=function(){return F},this.setPixelRatio=function(T){T!==void 0&&(F=T,this.setSize(N,O,!1))},this.getSize=function(T){return T.set(N,O)},this.setSize=function(T,V,W=!0){if($.isPresenting){console.warn("THREE.WebGLRenderer: Can't change size while VR device is presenting.");return}N=T,O=V,t.width=Math.floor(T*F),t.height=Math.floor(V*F),W===!0&&(t.style.width=T+"px",t.style.height=V+"px"),this.setViewport(0,0,T,V)},this.getDrawingBufferSize=function(T){return T.set(N*F,O*F).floor()},this.setDrawingBufferSize=function(T,V,W){N=T,O=V,F=W,t.width=Math.floor(T*W),t.height=Math.floor(V*W),this.setViewport(0,0,T,V)},this.getCurrentViewport=function(T){return T.copy(P)},this.getViewport=function(T){return T.copy(Y)},this.setViewport=function(T,V,W,q){T.isVector4?Y.set(T.x,T.y,T.z,T.w):Y.set(T,V,W,q),ve.viewport(P.copy(Y).multiplyScalar(F).round())},this.getScissor=function(T){return T.copy(he)},this.setScissor=function(T,V,W,q){T.isVector4?he.set(T.x,T.y,T.z,T.w):he.set(T,V,W,q),ve.scissor(U.copy(he).multiplyScalar(F).round())},this.getScissorTest=function(){return Ie},this.setScissorTest=function(T){ve.setScissorTest(Ie=T)},this.setOpaqueSort=function(T){G=T},this.setTransparentSort=function(T){Z=T},this.getClearColor=function(T){return T.copy(ze.getClearColor())},this.setClearColor=function(){ze.setClearColor(...arguments)},this.getClearAlpha=function(){return ze.getClearAlpha()},this.setClearAlpha=function(){ze.setClearAlpha(...arguments)},this.clear=function(T=!0,V=!0,W=!0){let q=0;if(T){let H=!1;if(C!==null){const ae=C.texture.format;H=ae===ka||ae===Fa||ae===Na}if(H){const ae=C.texture.type,pe=ae===pn||ae===Qn||ae===Zi||ae===Di||ae===Ua||ae===za,Ee=ze.getClearColor(),Ae=ze.getClearAlpha(),ke=Ee.r,Oe=Ee.g,De=Ee.b;pe?(g[0]=ke,g[1]=Oe,g[2]=De,g[3]=Ae,I.clearBufferuiv(I.COLOR,0,g)):(_[0]=ke,_[1]=Oe,_[2]=De,_[3]=Ae,I.clearBufferiv(I.COLOR,0,_))}else q|=I.COLOR_BUFFER_BIT}V&&(q|=I.DEPTH_BUFFER_BIT),W&&(q|=I.STENCIL_BUFFER_BIT,this.state.buffers.stencil.setMask(4294967295)),I.clear(q)},this.clearColor=function(){this.clear(!0,!1,!1)},this.clearDepth=function(){this.clear(!1,!0,!1)},this.clearStencil=function(){this.clear(!1,!1,!0)},this.dispose=function(){t.removeEventListener("webglcontextlost",ne,!1),t.removeEventListener("webglcontextrestored",Me,!1),t.removeEventListener("webglcontextcreationerror",xe,!1),ze.dispose(),ye.dispose(),Ye.dispose(),we.dispose(),S.dispose(),j.dispose(),J.dispose(),st.dispose(),B.dispose(),Re.dispose(),$.dispose(),$.removeEventListener("sessionstart",$a),$.removeEventListener("sessionend",Za),In.stop()};function ne(T){T.preventDefault(),console.log("THREE.WebGLRenderer: Context Lost."),D=!0}function Me(){console.log("THREE.WebGLRenderer: Context Restored."),D=!1;const T=Ne.autoReset,V=be.enabled,W=be.autoUpdate,q=be.needsUpdate,H=be.type;fe(),Ne.autoReset=T,be.enabled=V,be.autoUpdate=W,be.needsUpdate=q,be.type=H}function xe(T){console.error("THREE.WebGLRenderer: A WebGL context could not be created. Reason: ",T.statusMessage)}function Be(T){const V=T.target;V.removeEventListener("dispose",Be),lt(V)}function lt(T){Et(T),we.remove(T)}function Et(T){const V=we.get(T).programs;V!==void 0&&(V.forEach(function(W){Re.releaseProgram(W)}),T.isShaderMaterial&&Re.releaseShaderCache(T))}this.renderBufferDirect=function(T,V,W,q,H,ae){V===null&&(V=te);const pe=H.isMesh&&H.matrixWorld.determinant()<0,Ee=ol(T,V,W,q,H);ve.setMaterial(q,pe);let Ae=W.index,ke=1;if(q.wireframe===!0){if(Ae=ie.getWireframeAttribute(W),Ae===void 0)return;ke=2}const Oe=W.drawRange,De=W.attributes.position;let $e=Oe.start*ke,Qe=(Oe.start+Oe.count)*ke;ae!==null&&($e=Math.max($e,ae.start*ke),Qe=Math.min(Qe,(ae.start+ae.count)*ke)),Ae!==null?($e=Math.max($e,0),Qe=Math.min(Qe,Ae.count)):De!=null&&($e=Math.max($e,0),Qe=Math.min(Qe,De.count));const ht=Qe-$e;if(ht<0||ht===1/0)return;st.setup(H,q,Ee,W,Ae);let ut,Ze=Te;if(Ae!==null&&(ut=Q.get(Ae),Ze=qe,Ze.setIndex(ut)),H.isMesh)q.wireframe===!0?(ve.setLineWidth(q.wireframeLinewidth*K()),Ze.setMode(I.LINES)):Ze.setMode(I.TRIANGLES);else if(H.isLine){let Ue=q.linewidth;Ue===void 0&&(Ue=1),ve.setLineWidth(Ue*K()),H.isLineSegments?Ze.setMode(I.LINES):H.isLineLoop?Ze.setMode(I.LINE_LOOP):Ze.setMode(I.LINE_STRIP)}else H.isPoints?Ze.setMode(I.POINTS):H.isSprite&&Ze.setMode(I.TRIANGLES);if(H.isBatchedMesh)if(H._multiDrawInstances!==null)Vn("THREE.WebGLRenderer: renderMultiDrawInstances has been deprecated and will be removed in r184. Append to renderMultiDraw arguments and use indirection."),Ze.renderMultiDrawInstances(H._multiDrawStarts,H._multiDrawCounts,H._multiDrawCount,H._multiDrawInstances);else if(Se.get("WEBGL_multi_draw"))Ze.renderMultiDraw(H._multiDrawStarts,H._multiDrawCounts,H._multiDrawCount);else{const Ue=H._multiDrawStarts,Mt=H._multiDrawCounts,et=H._multiDrawCount,Wt=Ae?Q.get(Ae).bytesPerElement:1,ii=we.get(q).currentProgram.getUniforms();for(let It=0;It<et;It++)ii.setValue(I,"_gl_DrawID",It),Ze.render(Ue[It]/Wt,Mt[It])}else if(H.isInstancedMesh)Ze.renderInstances($e,ht,H.count);else if(W.isInstancedBufferGeometry){const Ue=W._maxInstanceCount!==void 0?W._maxInstanceCount:1/0,Mt=Math.min(W.instanceCount,Ue);Ze.renderInstances($e,ht,Mt)}else Ze.render($e,ht)};function tt(T,V,W){T.transparent===!0&&T.side===Tt&&T.forceSinglePass===!1?(T.side=Ct,T.needsUpdate=!0,or(T,V,W),T.side=Pn,T.needsUpdate=!0,or(T,V,W),T.side=Tt):or(T,V,W)}this.compile=function(T,V,W=null){W===null&&(W=T),u=Ye.get(W),u.init(V),y.push(u),W.traverseVisible(function(H){H.isLight&&H.layers.test(V.layers)&&(u.pushLight(H),H.castShadow&&u.pushShadow(H))}),T!==W&&T.traverseVisible(function(H){H.isLight&&H.layers.test(V.layers)&&(u.pushLight(H),H.castShadow&&u.pushShadow(H))}),u.setupLights();const q=new Set;return T.traverse(function(H){if(!(H.isMesh||H.isPoints||H.isLine||H.isSprite))return;const ae=H.material;if(ae)if(Array.isArray(ae))for(let pe=0;pe<ae.length;pe++){const Ee=ae[pe];tt(Ee,W,H),q.add(Ee)}else tt(ae,W,H),q.add(ae)}),u=y.pop(),q},this.compileAsync=function(T,V,W=null){const q=this.compile(T,V,W);return new Promise(H=>{function ae(){if(q.forEach(function(pe){we.get(pe).currentProgram.isReady()&&q.delete(pe)}),q.size===0){H(T);return}setTimeout(ae,10)}Se.get("KHR_parallel_shader_compile")!==null?ae():setTimeout(ae,10)})};let jt=null;function en(T){jt&&jt(T)}function $a(){In.stop()}function Za(){In.start()}const In=new el;In.setAnimationLoop(en),typeof self<"u"&&In.setContext(self),this.setAnimationLoop=function(T){jt=T,$.setAnimationLoop(T),T===null?In.stop():In.start()},$.addEventListener("sessionstart",$a),$.addEventListener("sessionend",Za),this.render=function(T,V){if(V!==void 0&&V.isCamera!==!0){console.error("THREE.WebGLRenderer.render: camera is not an instance of THREE.Camera.");return}if(D===!0)return;if(T.matrixWorldAutoUpdate===!0&&T.updateMatrixWorld(),V.parent===null&&V.matrixWorldAutoUpdate===!0&&V.updateMatrixWorld(),$.enabled===!0&&$.isPresenting===!0&&($.cameraAutoUpdate===!0&&$.updateCamera(V),V=$.getCamera()),T.isScene===!0&&T.onBeforeRender(M,T,V,C),u=Ye.get(T,y.length),u.init(V),y.push(u),le.multiplyMatrices(V.projectionMatrix,V.matrixWorldInverse),X.setFromProjectionMatrix(le),ue=this.localClippingEnabled,ee=ce.init(this.clippingPlanes,ue),p=ye.get(T,E.length),p.init(),E.push(p),$.enabled===!0&&$.isPresenting===!0){const ae=M.xr.getDepthSensingMesh();ae!==null&&Zr(ae,V,-1/0,M.sortObjects)}Zr(T,V,0,M.sortObjects),p.finish(),M.sortObjects===!0&&p.sort(G,Z),se=$.enabled===!1||$.isPresenting===!1||$.hasDepthSensing()===!1,se&&ze.addToRenderList(p,T),this.info.render.frame++,ee===!0&&ce.beginShadows();const W=u.state.shadowsArray;be.render(W,T,V),ee===!0&&ce.endShadows(),this.info.autoReset===!0&&this.info.reset();const q=p.opaque,H=p.transmissive;if(u.setupLights(),V.isArrayCamera){const ae=V.cameras;if(H.length>0)for(let pe=0,Ee=ae.length;pe<Ee;pe++){const Ae=ae[pe];Qa(q,H,T,Ae)}se&&ze.render(T);for(let pe=0,Ee=ae.length;pe<Ee;pe++){const Ae=ae[pe];Ja(p,T,Ae,Ae.viewport)}}else H.length>0&&Qa(q,H,T,V),se&&ze.render(T),Ja(p,T,V);C!==null&&b===0&&(L.updateMultisampleRenderTarget(C),L.updateRenderTargetMipmap(C)),T.isScene===!0&&T.onAfterRender(M,T,V),st.resetDefaultState(),v=-1,x=null,y.pop(),y.length>0?(u=y[y.length-1],ee===!0&&ce.setGlobalState(M.clippingPlanes,u.state.camera)):u=null,E.pop(),E.length>0?p=E[E.length-1]:p=null};function Zr(T,V,W,q){if(T.visible===!1)return;if(T.layers.test(V.layers)){if(T.isGroup)W=T.renderOrder;else if(T.isLOD)T.autoUpdate===!0&&T.update(V);else if(T.isLight)u.pushLight(T),T.castShadow&&u.pushShadow(T);else if(T.isSprite){if(!T.frustumCulled||X.intersectsSprite(T)){q&&me.setFromMatrixPosition(T.matrixWorld).applyMatrix4(le);const pe=J.update(T),Ee=T.material;Ee.visible&&p.push(T,pe,Ee,W,me.z,null)}}else if((T.isMesh||T.isLine||T.isPoints)&&(!T.frustumCulled||X.intersectsObject(T))){const pe=J.update(T),Ee=T.material;if(q&&(T.boundingSphere!==void 0?(T.boundingSphere===null&&T.computeBoundingSphere(),me.copy(T.boundingSphere.center)):(pe.boundingSphere===null&&pe.computeBoundingSphere(),me.copy(pe.boundingSphere.center)),me.applyMatrix4(T.matrixWorld).applyMatrix4(le)),Array.isArray(Ee)){const Ae=pe.groups;for(let ke=0,Oe=Ae.length;ke<Oe;ke++){const De=Ae[ke],$e=Ee[De.materialIndex];$e&&$e.visible&&p.push(T,pe,$e,W,me.z,De)}}else Ee.visible&&p.push(T,pe,Ee,W,me.z,null)}}const ae=T.children;for(let pe=0,Ee=ae.length;pe<Ee;pe++)Zr(ae[pe],V,W,q)}function Ja(T,V,W,q){const H=T.opaque,ae=T.transmissive,pe=T.transparent;u.setupLightsView(W),ee===!0&&ce.setGlobalState(M.clippingPlanes,W),q&&ve.viewport(P.copy(q)),H.length>0&&ar(H,V,W),ae.length>0&&ar(ae,V,W),pe.length>0&&ar(pe,V,W),ve.buffers.depth.setTest(!0),ve.buffers.depth.setMask(!0),ve.buffers.color.setMask(!0),ve.setPolygonOffset(!1)}function Qa(T,V,W,q){if((W.isScene===!0?W.overrideMaterial:null)!==null)return;u.state.transmissionRenderTarget[q.id]===void 0&&(u.state.transmissionRenderTarget[q.id]=new ei(1,1,{generateMipmaps:!0,type:Se.has("EXT_color_buffer_half_float")||Se.has("EXT_color_buffer_float")?nr:pn,minFilter:$n,samples:4,stencilBuffer:s,resolveDepthBuffer:!1,resolveStencilBuffer:!1,colorSpace:Je.workingColorSpace}));const ae=u.state.transmissionRenderTarget[q.id],pe=q.viewport||P;ae.setSize(pe.z*M.transmissionResolutionScale,pe.w*M.transmissionResolutionScale);const Ee=M.getRenderTarget();M.setRenderTarget(ae),M.getClearColor(R),z=M.getClearAlpha(),z<1&&M.setClearColor(16777215,.5),M.clear(),se&&ze.render(W);const Ae=M.toneMapping;M.toneMapping=Cn;const ke=q.viewport;if(q.viewport!==void 0&&(q.viewport=void 0),u.setupLightsView(q),ee===!0&&ce.setGlobalState(M.clippingPlanes,q),ar(T,W,q),L.updateMultisampleRenderTarget(ae),L.updateRenderTargetMipmap(ae),Se.has("WEBGL_multisampled_render_to_texture")===!1){let Oe=!1;for(let De=0,$e=V.length;De<$e;De++){const Qe=V[De],ht=Qe.object,ut=Qe.geometry,Ze=Qe.material,Ue=Qe.group;if(Ze.side===Tt&&ht.layers.test(q.layers)){const Mt=Ze.side;Ze.side=Ct,Ze.needsUpdate=!0,eo(ht,W,q,ut,Ze,Ue),Ze.side=Mt,Ze.needsUpdate=!0,Oe=!0}}Oe===!0&&(L.updateMultisampleRenderTarget(ae),L.updateRenderTargetMipmap(ae))}M.setRenderTarget(Ee),M.setClearColor(R,z),ke!==void 0&&(q.viewport=ke),M.toneMapping=Ae}function ar(T,V,W){const q=V.isScene===!0?V.overrideMaterial:null;for(let H=0,ae=T.length;H<ae;H++){const pe=T[H],Ee=pe.object,Ae=pe.geometry,ke=q===null?pe.material:q,Oe=pe.group;Ee.layers.test(W.layers)&&eo(Ee,V,W,Ae,ke,Oe)}}function eo(T,V,W,q,H,ae){T.onBeforeRender(M,V,W,q,H,ae),T.modelViewMatrix.multiplyMatrices(W.matrixWorldInverse,T.matrixWorld),T.normalMatrix.getNormalMatrix(T.modelViewMatrix),H.onBeforeRender(M,V,W,q,T,ae),H.transparent===!0&&H.side===Tt&&H.forceSinglePass===!1?(H.side=Ct,H.needsUpdate=!0,M.renderBufferDirect(W,V,q,H,T,ae),H.side=Pn,H.needsUpdate=!0,M.renderBufferDirect(W,V,q,H,T,ae),H.side=Tt):M.renderBufferDirect(W,V,q,H,T,ae),T.onAfterRender(M,V,W,q,H,ae)}function or(T,V,W){V.isScene!==!0&&(V=te);const q=we.get(T),H=u.state.lights,ae=u.state.shadowsArray,pe=H.state.version,Ee=Re.getParameters(T,H.state,ae,V,W),Ae=Re.getProgramCacheKey(Ee);let ke=q.programs;q.environment=T.isMeshStandardMaterial?V.environment:null,q.fog=V.fog,q.envMap=(T.isMeshStandardMaterial?j:S).get(T.envMap||q.environment),q.envMapRotation=q.environment!==null&&T.envMap===null?V.environmentRotation:T.envMapRotation,ke===void 0&&(T.addEventListener("dispose",Be),ke=new Map,q.programs=ke);let Oe=ke.get(Ae);if(Oe!==void 0){if(q.currentProgram===Oe&&q.lightsStateVersion===pe)return no(T,Ee),Oe}else Ee.uniforms=Re.getUniforms(T),T.onBeforeCompile(Ee,M),Oe=Re.acquireProgram(Ee,Ae),ke.set(Ae,Oe),q.uniforms=Ee.uniforms;const De=q.uniforms;return(!T.isShaderMaterial&&!T.isRawShaderMaterial||T.clipping===!0)&&(De.clippingPlanes=ce.uniform),no(T,Ee),q.needsLights=ll(T),q.lightsStateVersion=pe,q.needsLights&&(De.ambientLightColor.value=H.state.ambient,De.lightProbe.value=H.state.probe,De.directionalLights.value=H.state.directional,De.directionalLightShadows.value=H.state.directionalShadow,De.spotLights.value=H.state.spot,De.spotLightShadows.value=H.state.spotShadow,De.rectAreaLights.value=H.state.rectArea,De.ltc_1.value=H.state.rectAreaLTC1,De.ltc_2.value=H.state.rectAreaLTC2,De.pointLights.value=H.state.point,De.pointLightShadows.value=H.state.pointShadow,De.hemisphereLights.value=H.state.hemi,De.directionalShadowMap.value=H.state.directionalShadowMap,De.directionalShadowMatrix.value=H.state.directionalShadowMatrix,De.spotShadowMap.value=H.state.spotShadowMap,De.spotLightMatrix.value=H.state.spotLightMatrix,De.spotLightMap.value=H.state.spotLightMap,De.pointShadowMap.value=H.state.pointShadowMap,De.pointShadowMatrix.value=H.state.pointShadowMatrix),q.currentProgram=Oe,q.uniformsList=null,Oe}function to(T){if(T.uniformsList===null){const V=T.currentProgram.getUniforms();T.uniformsList=Vr.seqWithValue(V.seq,T.uniforms)}return T.uniformsList}function no(T,V){const W=we.get(T);W.outputColorSpace=V.outputColorSpace,W.batching=V.batching,W.batchingColor=V.batchingColor,W.instancing=V.instancing,W.instancingColor=V.instancingColor,W.instancingMorph=V.instancingMorph,W.skinning=V.skinning,W.morphTargets=V.morphTargets,W.morphNormals=V.morphNormals,W.morphColors=V.morphColors,W.morphTargetsCount=V.morphTargetsCount,W.numClippingPlanes=V.numClippingPlanes,W.numIntersection=V.numClipIntersection,W.vertexAlphas=V.vertexAlphas,W.vertexTangents=V.vertexTangents,W.toneMapping=V.toneMapping}function ol(T,V,W,q,H){V.isScene!==!0&&(V=te),L.resetTextureUnits();const ae=V.fog,pe=q.isMeshStandardMaterial?V.environment:null,Ee=C===null?M.outputColorSpace:C.isXRRenderTarget===!0?C.texture.colorSpace:Ii,Ae=(q.isMeshStandardMaterial?j:S).get(q.envMap||pe),ke=q.vertexColors===!0&&!!W.attributes.color&&W.attributes.color.itemSize===4,Oe=!!W.attributes.tangent&&(!!q.normalMap||q.anisotropy>0),De=!!W.morphAttributes.position,$e=!!W.morphAttributes.normal,Qe=!!W.morphAttributes.color;let ht=Cn;q.toneMapped&&(C===null||C.isXRRenderTarget===!0)&&(ht=M.toneMapping);const ut=W.morphAttributes.position||W.morphAttributes.normal||W.morphAttributes.color,Ze=ut!==void 0?ut.length:0,Ue=we.get(q),Mt=u.state.lights;if(ee===!0&&(ue===!0||T!==x)){const wt=T===x&&q.id===v;ce.setState(q,T,wt)}let et=!1;q.version===Ue.__version?(Ue.needsLights&&Ue.lightsStateVersion!==Mt.state.version||Ue.outputColorSpace!==Ee||H.isBatchedMesh&&Ue.batching===!1||!H.isBatchedMesh&&Ue.batching===!0||H.isBatchedMesh&&Ue.batchingColor===!0&&H.colorTexture===null||H.isBatchedMesh&&Ue.batchingColor===!1&&H.colorTexture!==null||H.isInstancedMesh&&Ue.instancing===!1||!H.isInstancedMesh&&Ue.instancing===!0||H.isSkinnedMesh&&Ue.skinning===!1||!H.isSkinnedMesh&&Ue.skinning===!0||H.isInstancedMesh&&Ue.instancingColor===!0&&H.instanceColor===null||H.isInstancedMesh&&Ue.instancingColor===!1&&H.instanceColor!==null||H.isInstancedMesh&&Ue.instancingMorph===!0&&H.morphTexture===null||H.isInstancedMesh&&Ue.instancingMorph===!1&&H.morphTexture!==null||Ue.envMap!==Ae||q.fog===!0&&Ue.fog!==ae||Ue.numClippingPlanes!==void 0&&(Ue.numClippingPlanes!==ce.numPlanes||Ue.numIntersection!==ce.numIntersection)||Ue.vertexAlphas!==ke||Ue.vertexTangents!==Oe||Ue.morphTargets!==De||Ue.morphNormals!==$e||Ue.morphColors!==Qe||Ue.toneMapping!==ht||Ue.morphTargetsCount!==Ze)&&(et=!0):(et=!0,Ue.__version=q.version);let Wt=Ue.currentProgram;et===!0&&(Wt=or(q,V,H));let ii=!1,It=!1,Bi=!1;const ot=Wt.getUniforms(),Ot=Ue.uniforms;if(ve.useProgram(Wt.program)&&(ii=!0,It=!0,Bi=!0),q.id!==v&&(v=q.id,It=!0),ii||x!==T){ve.buffers.depth.getReversed()?(re.copy(T.projectionMatrix),au(re),ou(re),ot.setValue(I,"projectionMatrix",re)):ot.setValue(I,"projectionMatrix",T.projectionMatrix),ot.setValue(I,"viewMatrix",T.matrixWorldInverse);const Pt=ot.map.cameraPosition;Pt!==void 0&&Pt.setValue(I,Pe.setFromMatrixPosition(T.matrixWorld)),_e.logarithmicDepthBuffer&&ot.setValue(I,"logDepthBufFC",2/(Math.log(T.far+1)/Math.LN2)),(q.isMeshPhongMaterial||q.isMeshToonMaterial||q.isMeshLambertMaterial||q.isMeshBasicMaterial||q.isMeshStandardMaterial||q.isShaderMaterial)&&ot.setValue(I,"isOrthographic",T.isOrthographicCamera===!0),x!==T&&(x=T,It=!0,Bi=!0)}if(H.isSkinnedMesh){ot.setOptional(I,H,"bindMatrix"),ot.setOptional(I,H,"bindMatrixInverse");const wt=H.skeleton;wt&&(wt.boneTexture===null&&wt.computeBoneTexture(),ot.setValue(I,"boneTexture",wt.boneTexture,L))}H.isBatchedMesh&&(ot.setOptional(I,H,"batchingTexture"),ot.setValue(I,"batchingTexture",H._matricesTexture,L),ot.setOptional(I,H,"batchingIdTexture"),ot.setValue(I,"batchingIdTexture",H._indirectTexture,L),ot.setOptional(I,H,"batchingColorTexture"),H._colorsTexture!==null&&ot.setValue(I,"batchingColorTexture",H._colorsTexture,L));const Bt=W.morphAttributes;if((Bt.position!==void 0||Bt.normal!==void 0||Bt.color!==void 0)&&Fe.update(H,W,Wt),(It||Ue.receiveShadow!==H.receiveShadow)&&(Ue.receiveShadow=H.receiveShadow,ot.setValue(I,"receiveShadow",H.receiveShadow)),q.isMeshGouraudMaterial&&q.envMap!==null&&(Ot.envMap.value=Ae,Ot.flipEnvMap.value=Ae.isCubeTexture&&Ae.isRenderTargetTexture===!1?-1:1),q.isMeshStandardMaterial&&q.envMap===null&&V.environment!==null&&(Ot.envMapIntensity.value=V.environmentIntensity),It&&(ot.setValue(I,"toneMappingExposure",M.toneMappingExposure),Ue.needsLights&&cl(Ot,Bi),ae&&q.fog===!0&&ge.refreshFogUniforms(Ot,ae),ge.refreshMaterialUniforms(Ot,q,F,O,u.state.transmissionRenderTarget[T.id]),Vr.upload(I,to(Ue),Ot,L)),q.isShaderMaterial&&q.uniformsNeedUpdate===!0&&(Vr.upload(I,to(Ue),Ot,L),q.uniformsNeedUpdate=!1),q.isSpriteMaterial&&ot.setValue(I,"center",H.center),ot.setValue(I,"modelViewMatrix",H.modelViewMatrix),ot.setValue(I,"normalMatrix",H.normalMatrix),ot.setValue(I,"modelMatrix",H.matrixWorld),q.isShaderMaterial||q.isRawShaderMaterial){const wt=q.uniformsGroups;for(let Pt=0,Jr=wt.length;Pt<Jr;Pt++){const Un=wt[Pt];B.update(Un,Wt),B.bind(Un,Wt)}}return Wt}function cl(T,V){T.ambientLightColor.needsUpdate=V,T.lightProbe.needsUpdate=V,T.directionalLights.needsUpdate=V,T.directionalLightShadows.needsUpdate=V,T.pointLights.needsUpdate=V,T.pointLightShadows.needsUpdate=V,T.spotLights.needsUpdate=V,T.spotLightShadows.needsUpdate=V,T.rectAreaLights.needsUpdate=V,T.hemisphereLights.needsUpdate=V}function ll(T){return T.isMeshLambertMaterial||T.isMeshToonMaterial||T.isMeshPhongMaterial||T.isMeshStandardMaterial||T.isShadowMaterial||T.isShaderMaterial&&T.lights===!0}this.getActiveCubeFace=function(){return w},this.getActiveMipmapLevel=function(){return b},this.getRenderTarget=function(){return C},this.setRenderTargetTextures=function(T,V,W){we.get(T.texture).__webglTexture=V,we.get(T.depthTexture).__webglTexture=W;const q=we.get(T);q.__hasExternalTextures=!0,q.__autoAllocateDepthBuffer=W===void 0,q.__autoAllocateDepthBuffer||Se.has("WEBGL_multisampled_render_to_texture")===!0&&(console.warn("THREE.WebGLRenderer: Render-to-texture extension was disabled because an external texture was provided"),q.__useRenderToTexture=!1)},this.setRenderTargetFramebuffer=function(T,V){const W=we.get(T);W.__webglFramebuffer=V,W.__useDefaultFramebuffer=V===void 0};const ul=I.createFramebuffer();this.setRenderTarget=function(T,V=0,W=0){C=T,w=V,b=W;let q=!0,H=null,ae=!1,pe=!1;if(T){const Ae=we.get(T);if(Ae.__useDefaultFramebuffer!==void 0)ve.bindFramebuffer(I.FRAMEBUFFER,null),q=!1;else if(Ae.__webglFramebuffer===void 0)L.setupRenderTarget(T);else if(Ae.__hasExternalTextures)L.rebindTextures(T,we.get(T.texture).__webglTexture,we.get(T.depthTexture).__webglTexture);else if(T.depthBuffer){const De=T.depthTexture;if(Ae.__boundDepthTexture!==De){if(De!==null&&we.has(De)&&(T.width!==De.image.width||T.height!==De.image.height))throw new Error("WebGLRenderTarget: Attached DepthTexture is initialized to the incorrect size.");L.setupDepthRenderbuffer(T)}}const ke=T.texture;(ke.isData3DTexture||ke.isDataArrayTexture||ke.isCompressedArrayTexture)&&(pe=!0);const Oe=we.get(T).__webglFramebuffer;T.isWebGLCubeRenderTarget?(Array.isArray(Oe[V])?H=Oe[V][W]:H=Oe[V],ae=!0):T.samples>0&&L.useMultisampledRTT(T)===!1?H=we.get(T).__webglMultisampledFramebuffer:Array.isArray(Oe)?H=Oe[W]:H=Oe,P.copy(T.viewport),U.copy(T.scissor),A=T.scissorTest}else P.copy(Y).multiplyScalar(F).floor(),U.copy(he).multiplyScalar(F).floor(),A=Ie;if(W!==0&&(H=ul),ve.bindFramebuffer(I.FRAMEBUFFER,H)&&q&&ve.drawBuffers(T,H),ve.viewport(P),ve.scissor(U),ve.setScissorTest(A),ae){const Ae=we.get(T.texture);I.framebufferTexture2D(I.FRAMEBUFFER,I.COLOR_ATTACHMENT0,I.TEXTURE_CUBE_MAP_POSITIVE_X+V,Ae.__webglTexture,W)}else if(pe){const Ae=we.get(T.texture),ke=V;I.framebufferTextureLayer(I.FRAMEBUFFER,I.COLOR_ATTACHMENT0,Ae.__webglTexture,W,ke)}else if(T!==null&&W!==0){const Ae=we.get(T.texture);I.framebufferTexture2D(I.FRAMEBUFFER,I.COLOR_ATTACHMENT0,I.TEXTURE_2D,Ae.__webglTexture,W)}v=-1},this.readRenderTargetPixels=function(T,V,W,q,H,ae,pe){if(!(T&&T.isWebGLRenderTarget)){console.error("THREE.WebGLRenderer.readRenderTargetPixels: renderTarget is not THREE.WebGLRenderTarget.");return}let Ee=we.get(T).__webglFramebuffer;if(T.isWebGLCubeRenderTarget&&pe!==void 0&&(Ee=Ee[pe]),Ee){ve.bindFramebuffer(I.FRAMEBUFFER,Ee);try{const Ae=T.texture,ke=Ae.format,Oe=Ae.type;if(!_e.textureFormatReadable(ke)){console.error("THREE.WebGLRenderer.readRenderTargetPixels: renderTarget is not in RGBA or implementation defined format.");return}if(!_e.textureTypeReadable(Oe)){console.error("THREE.WebGLRenderer.readRenderTargetPixels: renderTarget is not in UnsignedByteType or implementation defined type.");return}V>=0&&V<=T.width-q&&W>=0&&W<=T.height-H&&I.readPixels(V,W,q,H,He.convert(ke),He.convert(Oe),ae)}finally{const Ae=C!==null?we.get(C).__webglFramebuffer:null;ve.bindFramebuffer(I.FRAMEBUFFER,Ae)}}},this.readRenderTargetPixelsAsync=async function(T,V,W,q,H,ae,pe){if(!(T&&T.isWebGLRenderTarget))throw new Error("THREE.WebGLRenderer.readRenderTargetPixels: renderTarget is not THREE.WebGLRenderTarget.");let Ee=we.get(T).__webglFramebuffer;if(T.isWebGLCubeRenderTarget&&pe!==void 0&&(Ee=Ee[pe]),Ee){const Ae=T.texture,ke=Ae.format,Oe=Ae.type;if(!_e.textureFormatReadable(ke))throw new Error("THREE.WebGLRenderer.readRenderTargetPixelsAsync: renderTarget is not in RGBA or implementation defined format.");if(!_e.textureTypeReadable(Oe))throw new Error("THREE.WebGLRenderer.readRenderTargetPixelsAsync: renderTarget is not in UnsignedByteType or implementation defined type.");if(V>=0&&V<=T.width-q&&W>=0&&W<=T.height-H){ve.bindFramebuffer(I.FRAMEBUFFER,Ee);const De=I.createBuffer();I.bindBuffer(I.PIXEL_PACK_BUFFER,De),I.bufferData(I.PIXEL_PACK_BUFFER,ae.byteLength,I.STREAM_READ),I.readPixels(V,W,q,H,He.convert(ke),He.convert(Oe),0);const $e=C!==null?we.get(C).__webglFramebuffer:null;ve.bindFramebuffer(I.FRAMEBUFFER,$e);const Qe=I.fenceSync(I.SYNC_GPU_COMMANDS_COMPLETE,0);return I.flush(),await su(I,Qe,4),I.bindBuffer(I.PIXEL_PACK_BUFFER,De),I.getBufferSubData(I.PIXEL_PACK_BUFFER,0,ae),I.deleteBuffer(De),I.deleteSync(Qe),ae}else throw new Error("THREE.WebGLRenderer.readRenderTargetPixelsAsync: requested read bounds are out of range.")}},this.copyFramebufferToTexture=function(T,V=null,W=0){T.isTexture!==!0&&(Vn("WebGLRenderer: copyFramebufferToTexture function signature has changed."),V=arguments[0]||null,T=arguments[1]);const q=Math.pow(2,-W),H=Math.floor(T.image.width*q),ae=Math.floor(T.image.height*q),pe=V!==null?V.x:0,Ee=V!==null?V.y:0;L.setTexture2D(T,0),I.copyTexSubImage2D(I.TEXTURE_2D,W,0,0,pe,Ee,H,ae),ve.unbindTexture()};const dl=I.createFramebuffer(),hl=I.createFramebuffer();this.copyTextureToTexture=function(T,V,W=null,q=null,H=0,ae=null){T.isTexture!==!0&&(Vn("WebGLRenderer: copyTextureToTexture function signature has changed."),q=arguments[0]||null,T=arguments[1],V=arguments[2],ae=arguments[3]||0,W=null),ae===null&&(H!==0?(Vn("WebGLRenderer: copyTextureToTexture function signature has changed to support src and dst mipmap levels."),ae=H,H=0):ae=0);let pe,Ee,Ae,ke,Oe,De,$e,Qe,ht;const ut=T.isCompressedTexture?T.mipmaps[ae]:T.image;if(W!==null)pe=W.max.x-W.min.x,Ee=W.max.y-W.min.y,Ae=W.isBox3?W.max.z-W.min.z:1,ke=W.min.x,Oe=W.min.y,De=W.isBox3?W.min.z:0;else{const Bt=Math.pow(2,-H);pe=Math.floor(ut.width*Bt),Ee=Math.floor(ut.height*Bt),T.isDataArrayTexture?Ae=ut.depth:T.isData3DTexture?Ae=Math.floor(ut.depth*Bt):Ae=1,ke=0,Oe=0,De=0}q!==null?($e=q.x,Qe=q.y,ht=q.z):($e=0,Qe=0,ht=0);const Ze=He.convert(V.format),Ue=He.convert(V.type);let Mt;V.isData3DTexture?(L.setTexture3D(V,0),Mt=I.TEXTURE_3D):V.isDataArrayTexture||V.isCompressedArrayTexture?(L.setTexture2DArray(V,0),Mt=I.TEXTURE_2D_ARRAY):(L.setTexture2D(V,0),Mt=I.TEXTURE_2D),I.pixelStorei(I.UNPACK_FLIP_Y_WEBGL,V.flipY),I.pixelStorei(I.UNPACK_PREMULTIPLY_ALPHA_WEBGL,V.premultiplyAlpha),I.pixelStorei(I.UNPACK_ALIGNMENT,V.unpackAlignment);const et=I.getParameter(I.UNPACK_ROW_LENGTH),Wt=I.getParameter(I.UNPACK_IMAGE_HEIGHT),ii=I.getParameter(I.UNPACK_SKIP_PIXELS),It=I.getParameter(I.UNPACK_SKIP_ROWS),Bi=I.getParameter(I.UNPACK_SKIP_IMAGES);I.pixelStorei(I.UNPACK_ROW_LENGTH,ut.width),I.pixelStorei(I.UNPACK_IMAGE_HEIGHT,ut.height),I.pixelStorei(I.UNPACK_SKIP_PIXELS,ke),I.pixelStorei(I.UNPACK_SKIP_ROWS,Oe),I.pixelStorei(I.UNPACK_SKIP_IMAGES,De);const ot=T.isDataArrayTexture||T.isData3DTexture,Ot=V.isDataArrayTexture||V.isData3DTexture;if(T.isDepthTexture){const Bt=we.get(T),wt=we.get(V),Pt=we.get(Bt.__renderTarget),Jr=we.get(wt.__renderTarget);ve.bindFramebuffer(I.READ_FRAMEBUFFER,Pt.__webglFramebuffer),ve.bindFramebuffer(I.DRAW_FRAMEBUFFER,Jr.__webglFramebuffer);for(let Un=0;Un<Ae;Un++)ot&&(I.framebufferTextureLayer(I.READ_FRAMEBUFFER,I.COLOR_ATTACHMENT0,we.get(T).__webglTexture,H,De+Un),I.framebufferTextureLayer(I.DRAW_FRAMEBUFFER,I.COLOR_ATTACHMENT0,we.get(V).__webglTexture,ae,ht+Un)),I.blitFramebuffer(ke,Oe,pe,Ee,$e,Qe,pe,Ee,I.DEPTH_BUFFER_BIT,I.NEAREST);ve.bindFramebuffer(I.READ_FRAMEBUFFER,null),ve.bindFramebuffer(I.DRAW_FRAMEBUFFER,null)}else if(H!==0||T.isRenderTargetTexture||we.has(T)){const Bt=we.get(T),wt=we.get(V);ve.bindFramebuffer(I.READ_FRAMEBUFFER,dl),ve.bindFramebuffer(I.DRAW_FRAMEBUFFER,hl);for(let Pt=0;Pt<Ae;Pt++)ot?I.framebufferTextureLayer(I.READ_FRAMEBUFFER,I.COLOR_ATTACHMENT0,Bt.__webglTexture,H,De+Pt):I.framebufferTexture2D(I.READ_FRAMEBUFFER,I.COLOR_ATTACHMENT0,I.TEXTURE_2D,Bt.__webglTexture,H),Ot?I.framebufferTextureLayer(I.DRAW_FRAMEBUFFER,I.COLOR_ATTACHMENT0,wt.__webglTexture,ae,ht+Pt):I.framebufferTexture2D(I.DRAW_FRAMEBUFFER,I.COLOR_ATTACHMENT0,I.TEXTURE_2D,wt.__webglTexture,ae),H!==0?I.blitFramebuffer(ke,Oe,pe,Ee,$e,Qe,pe,Ee,I.COLOR_BUFFER_BIT,I.NEAREST):Ot?I.copyTexSubImage3D(Mt,ae,$e,Qe,ht+Pt,ke,Oe,pe,Ee):I.copyTexSubImage2D(Mt,ae,$e,Qe,ke,Oe,pe,Ee);ve.bindFramebuffer(I.READ_FRAMEBUFFER,null),ve.bindFramebuffer(I.DRAW_FRAMEBUFFER,null)}else Ot?T.isDataTexture||T.isData3DTexture?I.texSubImage3D(Mt,ae,$e,Qe,ht,pe,Ee,Ae,Ze,Ue,ut.data):V.isCompressedArrayTexture?I.compressedTexSubImage3D(Mt,ae,$e,Qe,ht,pe,Ee,Ae,Ze,ut.data):I.texSubImage3D(Mt,ae,$e,Qe,ht,pe,Ee,Ae,Ze,Ue,ut):T.isDataTexture?I.texSubImage2D(I.TEXTURE_2D,ae,$e,Qe,pe,Ee,Ze,Ue,ut.data):T.isCompressedTexture?I.compressedTexSubImage2D(I.TEXTURE_2D,ae,$e,Qe,ut.width,ut.height,Ze,ut.data):I.texSubImage2D(I.TEXTURE_2D,ae,$e,Qe,pe,Ee,Ze,Ue,ut);I.pixelStorei(I.UNPACK_ROW_LENGTH,et),I.pixelStorei(I.UNPACK_IMAGE_HEIGHT,Wt),I.pixelStorei(I.UNPACK_SKIP_PIXELS,ii),I.pixelStorei(I.UNPACK_SKIP_ROWS,It),I.pixelStorei(I.UNPACK_SKIP_IMAGES,Bi),ae===0&&V.generateMipmaps&&I.generateMipmap(Mt),ve.unbindTexture()},this.copyTextureToTexture3D=function(T,V,W=null,q=null,H=0){return T.isTexture!==!0&&(Vn("WebGLRenderer: copyTextureToTexture3D function signature has changed."),W=arguments[0]||null,q=arguments[1]||null,T=arguments[2],V=arguments[3],H=arguments[4]||0),Vn('WebGLRenderer: copyTextureToTexture3D function has been deprecated. Use "copyTextureToTexture" instead.'),this.copyTextureToTexture(T,V,W,q,H)},this.initRenderTarget=function(T){we.get(T).__webglFramebuffer===void 0&&L.setupRenderTarget(T)},this.initTexture=function(T){T.isCubeTexture?L.setTextureCube(T,0):T.isData3DTexture?L.setTexture3D(T,0):T.isDataArrayTexture||T.isCompressedArrayTexture?L.setTexture2DArray(T,0):L.setTexture2D(T,0),ve.unbindTexture()},this.resetState=function(){w=0,b=0,C=null,ve.reset(),st.reset()},typeof __THREE_DEVTOOLS__<"u"&&__THREE_DEVTOOLS__.dispatchEvent(new CustomEvent("observe",{detail:this}))}get coordinateSystem(){return hn}get outputColorSpace(){return this._outputColorSpace}set outputColorSpace(e){this._outputColorSpace=e;const t=this.getContext();t.drawingBufferColorspace=Je._getDrawingBufferColorSpace(e),t.unpackColorSpace=Je._getUnpackColorSpace()}}const En=1e-6,yi=5e-5,Ls=1e-7;function wa(n,e){return n[0]*e[0]+n[1]*e[1]+n[2]*e[2]}function Ra(n,e){return[n[0]-e[0],n[1]-e[1],n[2]-e[2]]}function Ca(n,e){return[n[1]*e[2]-n[2]*e[1],n[2]*e[0]-n[0]*e[2],n[0]*e[1]-n[1]*e[0]]}function Rm(n){const e=Math.hypot(n[0],n[1],n[2]);return e<1e-12?null:[n[0]/e,n[1]/e,n[2]/e]}function Hr(n,e){const t=n[0]-e[0],i=n[1]-e[1],r=n[2]-e[2];return t*t+i*i+r*r}function Is(n){if(n.length<3)return 0;const e=n[0];let t=0,i=0,r=0;for(let s=1;s+1<n.length;s++){const a=Ra(n[s],e),o=Ra(n[s+1],e),c=Ca(a,o);t+=c[0],i+=c[1],r+=c[2]}return .5*Math.hypot(t,i,r)}function Cm(n,e){const t=[],i=yi*yi;for(const f of n)t.some(m=>Hr(f,m)<=i)||t.push(f);if(t.length<3)return[];let r=0,s=0,a=0;for(const f of t)r+=f[0],s+=f[1],a+=f[2];r/=t.length,s/=t.length,a/=t.length;const o=[r,s,a],c=Math.abs(e[0])<.8?[1,0,0]:[0,1,0],l=Rm(Ca(c,e));if(!l)return[];const d=Ca(e,l),h=t.map(f=>{const m=Ra(f,o),g=wa(m,l),_=wa(m,d);return{tacka:f,ugao:Math.atan2(_,g)}});return h.sort((f,m)=>f.ugao-m.ugao),h.map(f=>f.tacka)}function Pm(n){return[{normala:[1,0,0],grupaId:"__okvir__",oznaka:"",temena:[[n,-n,-n],[n,n,-n],[n,n,n],[n,-n,n]]},{normala:[-1,0,0],grupaId:"__okvir__",oznaka:"",temena:[[-n,-n,n],[-n,n,n],[-n,n,-n],[-n,-n,-n]]},{normala:[0,1,0],grupaId:"__okvir__",oznaka:"",temena:[[-n,n,-n],[-n,n,n],[n,n,n],[n,n,-n]]},{normala:[0,-1,0],grupaId:"__okvir__",oznaka:"",temena:[[-n,-n,n],[-n,-n,-n],[n,-n,-n],[n,-n,n]]},{normala:[0,0,1],grupaId:"__okvir__",oznaka:"",temena:[[-n,-n,n],[n,-n,n],[n,n,n],[-n,n,n]]},{normala:[0,0,-1],grupaId:"__okvir__",oznaka:"",temena:[[n,-n,-n],[-n,-n,-n],[-n,n,-n],[n,n,-n]]}]}function Qi(n){if(n.length===0)return{temena:[],pljosni:[]};let e=1;const t=[];for(let c=0;c<n.length;c++){const l=n[c],d=Math.hypot(l.normala[0],l.normala[1],l.normala[2]);if(d<1e-12)continue;const h=[l.normala[0]/d,l.normala[1]/d,l.normala[2]/d],f=l.d;e=Math.max(e,Math.abs(f)),t.push({normala:h,d:f,grupaId:l.grupaId??`forma-${c}`,oznaka:l.oznaka??""})}let i=Pm(Math.max(12,e*6));for(const c of t){const l=[],d=[];for(const f of i){const m=f.temena.length;if(m<3)continue;const g=f.temena.map(E=>wa(c.normala,E)-c.d),_=[];for(let E=0;E<m;E++){const y=(E+1)%m,M=f.temena[E],D=f.temena[y],w=g[E],b=g[y],C=w<=En,v=b<=En;if(Math.abs(w)<=En*4&&d.push(M),C&&_.push(M),w<-En&&b>En||w>En&&b<-En){const x=w/(w-b),P=[M[0]+(D[0]-M[0])*x,M[1]+(D[1]-M[1])*x,M[2]+(D[2]-M[2])*x];_.push(P),d.push(P)}else!C&&v&&Math.abs(b)<=En&&d.push(D)}const p=[],u=yi*yi;for(const E of _)(p.length===0||Hr(E,p[p.length-1])>u)&&p.push(E);p.length>1&&Hr(p[0],p[p.length-1])<=u&&p.pop(),p.length>=3&&Is(p)>Ls&&l.push({temena:p,normala:f.normala,grupaId:f.grupaId,oznaka:f.oznaka})}const h=Cm(d,c.normala);if(h.length>=3&&Is(h)>Ls&&l.push({temena:h,normala:c.normala,grupaId:c.grupaId,oznaka:c.oznaka}),i=l,i.length===0)break}const r=[],s=[],a=yi*yi;function o(c){for(let l=0;l<r.length;l++)if(Hr(r[l],c)<=a)return l;return r.push([Math.abs(c[0])<1e-10?0:c[0],Math.abs(c[1])<1e-10?0:c[1],Math.abs(c[2])<1e-10?0:c[2]]),r.length-1}for(const c of i){if(c.grupaId==="__okvir__")continue;const l=Is(c.temena);if(l<=Ls)continue;const d=c.temena.map(p=>o(p)),h=[];for(const p of d)(h.length===0||h[h.length-1]!==p)&&h.push(p);if(h.length>1&&h[0]===h[h.length-1]&&h.pop(),h.length<3)continue;let f=0,m=0,g=0;for(const p of h){const u=r[p];f+=u[0],m+=u[1],g+=u[2]}const _=h.length;s.push({indeksiTemena:h,normala:c.normala,centar:[f/_,m/_,g/_],povrsina:l,grupaId:c.grupaId,oznaka:c.oznaka})}return{temena:r,pljosni:s}}function er(n){const e=[];for(const d of n.pljosni)e.includes(d.grupaId)||e.push(d.grupaId);const t=[],i=[],r=[],s=[];for(let d=0;d<e.length;d++){const h=e[d],f=t.length/3;for(let g=0;g<n.pljosni.length;g++){const _=n.pljosni[g];if(_.grupaId!==h)continue;const p=_.indeksiTemena;if(p.length<3)continue;const u=n.temena[p[0]],[E,y,M]=_.normala;for(let D=1;D+1<p.length;D++){const w=n.temena[p[D]],b=n.temena[p[D+1]];t.push(u[0],u[1],u[2],w[0],w[1],w[2],b[0],b[1],b[2]),i.push(E,y,M,E,y,M,E,y,M),r.push(g)}}const m=t.length/3;m>f&&s.push({pocetak:f,broj:m-f,indeksMaterijala:d})}const a=new Ke;a.setAttribute("position",new je(t,3)),a.setAttribute("normal",new je(i,3));for(const d of s)a.addGroup(d.pocetak,d.broj,d.indeksMaterijala);const o=new Set,c=[];for(const d of n.pljosni){const h=d.indeksiTemena;for(let f=0;f<h.length;f++){const m=h[f],g=h[(f+1)%h.length],_=m<g?`${m}-${g}`:`${g}-${m}`;if(o.has(_))continue;o.add(_);const p=n.temena[m],u=n.temena[g];c.push(p[0],p[1],p[2],u[0],u[1],u[2])}}const l=new Ke;return l.setAttribute("position",new je(c,3)),{geometrijaMreze:a,geometrijaIvica:l,mapaTrougaoUPljosan:r,redosledGrupa:e}}const Dm=.5,Lm=.35,Im=.6;function ti(n,e={}){const t=Math.min(Im,Math.max(Lm,e.providnost??Dm));return new zu({color:new oe(n),transparent:!0,opacity:t,depthWrite:!1,side:Tt,roughness:.1,metalness:0,ior:1.56,specularIntensity:1,clearcoat:1,clearcoatRoughness:.06,envMapIntensity:1.1,flatShading:!0})}function zi(n,e){return new oe(n).lerp(new oe(e),.3)}function tr(n,e){return new mt({color:zi(n,e)})}function Um(n,e){return Math.hypot(n.r-e.r,n.g-e.g,n.b-e.b)}function Ka(n,e){const t=new oe(n);let i=new oe(e[0]??n),r=-1;for(const s of e){const a=new oe(s),o=Um(t,a);o>r+1e-6&&(r=o,i=a)}return i}const Pa=64;function zm(n=Pa){const e=new Uint8Array(n*n*4),t=(n-1)/2;for(let i=0;i<n;i++)for(let r=0;r<n;r++){const s=Math.min(1,Math.hypot(r-t,i-t)/t),a=1-s*s*(3-2*s),o=Math.round(255*a*a),c=(i*n+r)*4;e[c]=o,e[c+1]=o,e[c+2]=o,e[c+3]=255}return e}function Nm(n){const e=new Lu(zm(),Pa,Pa,Gt);e.needsUpdate=!0;const t=new Ln({alphaMap:e,transparent:!0,depthWrite:!1,opacity:.2}),i=new Le(new ni(n*2,n*2),t);return i.rotation.x=-Math.PI/2,i.renderOrder=-1,i.name="kontaktna-senka",{mreza:i,osveziBoju(r,s,a){t.color.set(r?a:s),t.opacity=r?.14:.2}}}class Fm extends $c{constructor(){super();const e=new Jt;e.deleteAttribute("uv");const t=new pt({side:Ct}),i=new pt,r=new Bu(16777215,900,28,2);r.position.set(.418,16.199,.3),this.add(r);const s=new Le(e,t);s.position.set(-.757,13.219,.717),s.scale.set(31.713,28.305,28.591),this.add(s);const a=new Le(e,i);a.position.set(-10.906,2.009,1.846),a.rotation.set(0,-.195,0),a.scale.set(2.328,7.905,4.651),this.add(a);const o=new Le(e,i);o.position.set(-5.607,-.754,-.758),o.rotation.set(0,.994,0),o.scale.set(1.97,1.534,3.955),this.add(o);const c=new Le(e,i);c.position.set(6.167,.857,7.803),c.rotation.set(0,.561,0),c.scale.set(3.927,6.285,3.687),this.add(c);const l=new Le(e,i);l.position.set(-2.017,.018,6.124),l.rotation.set(0,.333,0),l.scale.set(2.002,4.566,2.064),this.add(l);const d=new Le(e,i);d.position.set(2.291,-.756,-2.621),d.rotation.set(0,-.286,0),d.scale.set(1.546,1.552,1.496),this.add(d);const h=new Le(e,i);h.position.set(-2.193,-.369,-5.547),h.rotation.set(0,.516,0),h.scale.set(3.875,3.487,2.986),this.add(h);const f=new Le(e,xi(50));f.position.set(-16.116,14.37,8.208),f.scale.set(.1,2.428,2.739),this.add(f);const m=new Le(e,xi(50));m.position.set(-16.109,18.021,-8.207),m.scale.set(.1,2.425,2.751),this.add(m);const g=new Le(e,xi(17));g.position.set(14.904,12.198,-1.832),g.scale.set(.15,4.265,6.331),this.add(g);const _=new Le(e,xi(43));_.position.set(-.462,8.89,14.52),_.scale.set(4.38,5.441,.088),this.add(_);const p=new Le(e,xi(20));p.position.set(3.235,11.486,-12.541),p.scale.set(2.5,2,.1),this.add(p);const u=new Le(e,xi(100));u.position.set(0,20,0),u.scale.set(1,.1,1),this.add(u)}dispose(){const e=new Set;this.traverse(t=>{t.isMesh&&(e.add(t.geometry),e.add(t.material))});for(const t of e)t.dispose()}}function xi(n){const e=new Ln;return e.color.setScalar(n),e}function Mi(n,e,t){return Math.max(e,Math.min(t,n))}class km{stanje;pocetno;minUdaljenost;maksUdaljenost;opcije;vuceMisem=!1;prethodniX=0;prethodniY=0;dodirAktiviran=!1;prethodniDodirX=0;prethodniDodirY=0;prethodniRazmakPrstiju=0;pocetakDodiraX=0;pocetakDodiraY=0;dodirPomeren=!1;cistaci=[];constructor(e){this.opcije=e,this.pocetno={...e.pocetno},this.stanje={...e.pocetno},this.minUdaljenost=e.minUdaljenost??2,this.maksUdaljenost=e.maksUdaljenost??24,this.poveziDogadjaje()}trenutnoStanje(){return{...this.stanje}}rotirajAzimut(e){this.stanje.theta+=e,this.opcije.naPromenu(this.trenutnoStanje())}rotirajElevaciju(e){this.stanje.phi=Mi(this.stanje.phi+e,.15,Math.PI-.15),this.opcije.naPromenu(this.trenutnoStanje())}zumiraj(e){this.stanje.udaljenost=Mi(this.stanje.udaljenost*e,this.minUdaljenost,this.maksUdaljenost),this.opcije.naPromenu(this.trenutnoStanje())}resetuj(){this.stanje={...this.pocetno},this.opcije.naPromenu(this.trenutnoStanje())}postaviAktivacijuDodira(e){this.dodirAktiviran=e,this.opcije.platno.classList.toggle("udzbenik-scena-platno--dodir-aktivan",e),this.opcije.dugmeDodira.hidden=!e,this.opcije.priPromeniAktivacijeDodira?.(e)}poveziDogadjaje(){const{bina:e,platno:t,dugmeDodira:i}=this.opcije,r=g=>{if(g.pointerType!=="touch"&&g.button===0){this.vuceMisem=!0,this.prethodniX=g.clientX,this.prethodniY=g.clientY;try{t.setPointerCapture(g.pointerId)}catch{}}},s=g=>{if(g.pointerType==="touch"||!this.vuceMisem)return;const _=g.clientX-this.prethodniX,p=g.clientY-this.prethodniY;this.prethodniX=g.clientX,this.prethodniY=g.clientY,this.stanje.theta-=_*.008,this.stanje.phi=Mi(this.stanje.phi-p*.008,.15,Math.PI-.15),this.opcije.naPromenu(this.trenutnoStanje())},a=g=>{if(g.pointerType!=="touch"){this.vuceMisem=!1;try{t.hasPointerCapture(g.pointerId)&&t.releasePointerCapture(g.pointerId)}catch{}}},o=g=>{if(!(document.activeElement===e||e.contains(document.activeElement))&&!g.ctrlKey&&!g.metaKey)return;g.preventDefault();const p=g.deltaY>0?1.09:.92;this.zumiraj(p)},c=g=>{if(g.touches.length===2){const _=g.touches[0],p=g.touches[1];this.prethodniDodirX=(_.clientX+p.clientX)/2,this.prethodniDodirY=(_.clientY+p.clientY)/2,this.prethodniRazmakPrstiju=Math.hypot(p.clientX-_.clientX,p.clientY-_.clientY)}else if(g.touches.length===1){const _=g.touches[0];this.pocetakDodiraX=_.clientX,this.pocetakDodiraY=_.clientY,this.prethodniDodirX=_.clientX,this.prethodniDodirY=_.clientY,this.dodirPomeren=!1}},l=g=>{if(g.touches.length===2){g.preventDefault();const _=g.touches[0],p=g.touches[1],u=(_.clientX+p.clientX)/2,E=(_.clientY+p.clientY)/2,y=Math.hypot(p.clientX-_.clientX,p.clientY-_.clientY),M=u-this.prethodniDodirX,D=E-this.prethodniDodirY;if(this.prethodniDodirX=u,this.prethodniDodirY=E,this.stanje.theta-=M*.008,this.stanje.phi=Mi(this.stanje.phi-D*.008,.15,Math.PI-.15),this.prethodniRazmakPrstiju>8&&y>8){const w=this.prethodniRazmakPrstiju/y;this.stanje.udaljenost=Mi(this.stanje.udaljenost*w,this.minUdaljenost,this.maksUdaljenost)}this.prethodniRazmakPrstiju=y,this.dodirPomeren=!0,this.opcije.naPromenu(this.trenutnoStanje())}else if(g.touches.length===1){const _=g.touches[0];if(Math.hypot(_.clientX-this.pocetakDodiraX,_.clientY-this.pocetakDodiraY)>8&&(this.dodirPomeren=!0),this.dodirAktiviran){g.preventDefault();const p=_.clientX-this.prethodniDodirX,u=_.clientY-this.prethodniDodirY;this.prethodniDodirX=_.clientX,this.prethodniDodirY=_.clientY,this.stanje.theta-=p*.009,this.stanje.phi=Mi(this.stanje.phi-u*.009,.15,Math.PI-.15),this.opcije.naPromenu(this.trenutnoStanje())}}},d=g=>{g.touches.length===0&&!this.dodirPomeren&&g.changedTouches.length===1&&this.postaviAktivacijuDodira(!this.dodirAktiviran)},h=()=>{this.postaviAktivacijuDodira(!1)},f=g=>{this.dodirAktiviran&&g.target instanceof Node&&!e.contains(g.target)&&this.postaviAktivacijuDodira(!1)},m=g=>{if(!(g.target instanceof HTMLElement&&g.target!==e&&(g.target.tagName==="BUTTON"||g.target.tagName==="INPUT")))switch(g.key){case"ArrowLeft":g.preventDefault(),this.rotirajAzimut(-.12);break;case"ArrowRight":g.preventDefault(),this.rotirajAzimut(.12);break;case"ArrowUp":g.preventDefault(),this.rotirajElevaciju(-.12);break;case"ArrowDown":g.preventDefault(),this.rotirajElevaciju(.12);break;case"+":case"=":g.preventDefault(),this.zumiraj(.88);break;case"-":case"_":g.preventDefault(),this.zumiraj(1.14);break;case"r":case"R":case"р":case"Р":g.preventDefault(),this.opcije.naReset();break;case" ":g.preventDefault(),this.opcije.naPrekidacPauze();break;case"Escape":this.dodirAktiviran&&(g.preventDefault(),this.postaviAktivacijuDodira(!1));break}};t.addEventListener("pointerdown",r),t.addEventListener("pointermove",s),t.addEventListener("pointerup",a),t.addEventListener("pointercancel",a),t.addEventListener("wheel",o,{passive:!1}),t.addEventListener("touchstart",c,{passive:!0}),t.addEventListener("touchmove",l,{passive:!1}),t.addEventListener("touchend",d),i.addEventListener("click",h),document.addEventListener("touchstart",f,{passive:!0}),e.addEventListener("keydown",m),this.cistaci.push(()=>{t.removeEventListener("pointerdown",r),t.removeEventListener("pointermove",s),t.removeEventListener("pointerup",a),t.removeEventListener("pointercancel",a),t.removeEventListener("wheel",o),t.removeEventListener("touchstart",c),t.removeEventListener("touchmove",l),t.removeEventListener("touchend",d),i.removeEventListener("click",h),document.removeEventListener("touchstart",f),e.removeEventListener("keydown",m)})}raspolazi(){for(const e of this.cistaci)e();this.cistaci.length=0}}let un=null,bi=null,Zn=0,Jn=0,Kn=null;function Om(){if(un)return un;const n=document.createElement("canvas"),e=n.getContext("webgl2",{antialias:!0,alpha:!1,preserveDrawingBuffer:!1})??n.getContext("webgl",{antialias:!0,alpha:!1,preserveDrawingBuffer:!1});if(!e)throw new Error("WebGL контекст није доступан у овом прегледачу.");const t=new wm({canvas:n,context:e,antialias:!0,alpha:!1,powerPreference:"default"});return t.setPixelRatio(1),t.outputColorSpace=Nt,bi=n,un=t,Zn=320,Jn=240,un.setSize(Zn,Jn,!1),un}function Bm(n){if(Kn)return Kn;try{const e=new Ta(n),t=new Fm;Kn=e.fromScene(t,.04).texture,t.dispose(),e.dispose()}catch{Kn=null}return Kn}function f0(){Kn?.dispose(),Kn=null,un&&(un.forceContextLoss(),un.dispose(),un=null,bi=null,Zn=0,Jn=0)}function Lt(n){n.traverse(e=>{const t=e;t.geometry&&typeof t.geometry.dispose=="function"&&t.geometry.dispose();const i=t.material;if(Array.isArray(i))for(const r of i)fc(r);else i&&fc(i)})}function fc(n){for(const e of Object.values(n))e instanceof At&&e.dispose();n.dispose()}function Vm(n,e,t,i){const r=Om(),s=t.platno.getContext("2d");if(!s||!bi)throw new Error("2D контекст платна није доступан.");const a=typeof window<"u"&&typeof window.matchMedia=="function"&&window.matchMedia("(prefers-reduced-motion: reduce)").matches,o=new $c,c=new Ft(42,16/9,.1,100),l=new k(0,0,0),d=new Hu(new oe(1,1,1),.72),h=new Bo(new oe(1,1,1),.95);h.position.set(5,8,6);const f=new Bo(new oe(1,1,1),.38);if(f.position.set(-5,-3,-4),o.add(d,h,f),n.izgled==="kristal"){const K=Bm(r);K&&(o.environment=K,o.environmentIntensity=.85,d.intensity=.32,h.intensity=1.25,h.position.set(4,9,5),f.intensity=0)}const m=[];function g(){for(const K of m)K.osveziBoju(ri.jeTamna(),ri.token("--text-primary"),ri.token("--text-secondary"))}let _=!1;const p=n.pocetnaKamera?.(e)??{theta:.62,phi:1.12,udaljenost:6.2};function u(K){const I=Math.sin(K.phi);c.position.set(l.x+K.udaljenost*I*Math.sin(K.theta),l.y+K.udaljenost*Math.cos(K.phi),l.z+K.udaljenost*I*Math.cos(K.theta)),c.lookAt(l),c.updateMatrixWorld()}u(p);let E=!1,y=!1,M=!0,D=n.imaPodrazumevanuAnimaciju?n.imaPodrazumevanuAnimaciju(e):!0,w=a||!D,b=null,C=null,v=0,x=0,P=Math.max(240,t.bina.clientWidth||600),U=Math.max(180,t.bina.clientHeight||360),A=null;function R(){if(E||y||!bi||!s)return;const K=t.bina.clientWidth,I=t.bina.clientHeight;K>0&&I>0&&(P=K,U=I);const Ce=Math.min(typeof window<"u"&&window.devicePixelRatio||1,2),Se=Math.max(1,Math.round(P*Ce)),_e=Math.max(1,Math.round(U*Ce));(t.platno.width!==Se||t.platno.height!==_e)&&(t.platno.width=Se,t.platno.height=_e),c.aspect=P/Math.max(1,U),c.updateProjectionMatrix();const ve=Math.min(4096,Math.max(Zn,Se)),Ne=Math.min(4096,Math.max(Jn,_e));(ve>Zn||Ne>Jn)&&(Zn=ve,Jn=Ne,r.setSize(Zn,Jn,!1));const we=new oe(ri.token("--bg-card"));r.setViewport(0,0,Se,_e),r.setScissor(0,0,Se,_e),r.setScissorTest(!0),r.setClearColor(we,1),r.clear(!0,!0,!0),r.render(o,c);const L=Math.max(0,bi.height-_e);s.drawImage(bi,0,L,Se,_e,0,0,Se,_e),A?.posleRendera?.()}function z(){E||y||b!==null||C!==null||(C=requestAnimationFrame(()=>{C=null,R()}))}function N(){const K=typeof document<"u"&&document.hidden;return!E&&!y&&D&&!w&&M&&!K}function O(K){if(b=null,!N())return;const I=v>0?Math.min(.05,(K-v)/1e3):.016;v=K,x+=I,A?.azuriraj?.(I,x),R(),N()&&(b=requestAnimationFrame(O))}function F(){t.azurirajDugmePauze(w,D),N()?b===null&&(v=performance.now(),b=requestAnimationFrame(O)):b!==null&&(cancelAnimationFrame(b),b=null)}function G(K){const I=K.clone().project(c),Ce=I.z>=-1&&I.z<=1;return{x:(I.x*.5+.5)*P,y:(-I.y*.5+.5)*U,vidljivo:Ce}}const Z={scena3D:o,kamera:c,platno:t.platno,slojEtiketa:t.slojEtiketa,gornjeKontrole:t.gornjeKontrole,podnozje:t.podnozje,api:i,tema:ri,smanjenPokret:a,zatraziRender:z,korisnikUpravlja:()=>_,dodajKontaktnuSenku:(K,I,Ce,Se=0)=>{const _e=Nm(K);return _e.mreza.position.set(Se,I,0),(Ce??o).add(_e.mreza),m.push(_e),g(),_e.mreza},postaviImaAnimaciju:K=>{D=K,K||(w=!0),F()},prikaziRezervu:K=>{y=!0,F(),t.prikaziRezervu(K)},projektujU2D:G},Y=new km({bina:t.bina,platno:t.platno,dugmeDodira:t.dugmeDodira,pocetno:p,naPromenu:K=>{u(K),z()},naReset:()=>{_=!1,Y.resetuj(),A?.resetuj?.(),R()},naPrekidacPauze:()=>{D&&(w=!w,F())}});A=n.kreiraj(Z,e);const he=()=>{_=!1,Y.resetuj(),A?.resetuj?.(),R()},Ie=()=>{D&&(w=!w,F())},X=()=>{w=!0,F(),A?.korak?A.korak():(x+=.45,A?.azuriraj?.(.45,x)),R()},ee=()=>{_=!0},ue=()=>{ee(),Y.zumiraj(.86)},re=()=>{ee(),Y.zumiraj(1.16)},le=K=>{(K.key.startsWith("Arrow")||K.key==="+"||K.key==="-"||K.key==="=")&&ee()};t.platno.addEventListener("pointerdown",ee),t.platno.addEventListener("wheel",ee,{passive:!0}),t.bina.addEventListener("keydown",le),t.dugmeReset.addEventListener("click",he),t.dugmePauza.addEventListener("click",Ie),t.dugmeKorak.addEventListener("click",X),t.dugmeZumPlus.addEventListener("click",ue),t.dugmeZumMinus.addEventListener("click",re);let Pe=null;typeof ResizeObserver<"u"&&(Pe=new ResizeObserver(K=>{for(const I of K){const Ce=Math.round(I.contentRect.width),Se=Math.round(I.contentRect.height);Ce>0&&Se>0&&(Ce!==P||Se!==U)&&(P=Ce,U=Se,R())}}),Pe.observe(t.bina));let me=null;typeof IntersectionObserver<"u"&&(me=new IntersectionObserver(K=>{for(const I of K)M=I.isIntersecting,F()},{threshold:.05}),me.observe(t.bina));const te=()=>{F(),document.hidden||z()};document.addEventListener("visibilitychange",te);const se=ri.pretplati(K=>{A?.osveziTemu?.(K),g(),R()});return R(),F(),()=>{E||(E=!0,b!==null&&(cancelAnimationFrame(b),b=null),C!==null&&(cancelAnimationFrame(C),C=null),Pe?.disconnect(),me?.disconnect(),document.removeEventListener("visibilitychange",te),se(),t.dugmeReset.removeEventListener("click",he),t.dugmePauza.removeEventListener("click",Ie),t.dugmeKorak.removeEventListener("click",X),t.dugmeZumPlus.removeEventListener("click",ue),t.dugmeZumMinus.removeEventListener("click",re),t.platno.removeEventListener("pointerdown",ee),t.platno.removeEventListener("wheel",ee),t.bina.removeEventListener("keydown",le),Y.raspolazi(),A?.raspolazi?.(),Lt(o),o.clear(),t.slojEtiketa.replaceChildren(),t.gornjeKontrole.replaceChildren(),t.podnozje.replaceChildren())}}const pc={karlsbadski:{zakon:"karlsbadski",naziv:"Карлсбадски близанац",mineral:"ортоклас",sistem:"моноклинични",tipElementa:"osa",opisElementa:"Оса близањења [001] (c-оса), раван срастања (010)",normalaRavniIliOsa:[0,0,1],ugaoRotacijeStepeni:180,izvor:"Klein & Dutrow 2007, str. 235"},spinelov:{zakon:"spinelov",naziv:"Спинелов закон",mineral:"спинел (октаедар)",sistem:"кубни",tipElementa:"ravan",opisElementa:"Раван близањења (111)",normalaRavniIliOsa:[1/Math.sqrt(3),1/Math.sqrt(3),1/Math.sqrt(3)],izvor:"Klein & Dutrow 2007, str. 233"},baveno:{zakon:"baveno",naziv:"Бавено близанац",mineral:"ортоклас",sistem:"моноклинични",tipElementa:"ravan",opisElementa:"Раван близањења (021), моноклинична метрика (β ≈ 116°)",normalaRavniIliOsa:[.31,.7071,.6355],izvor:"Klein & Dutrow 2007, str. 235"},manebah:{zakon:"manebah",naziv:"Манебах близанац",mineral:"ортоклас",sistem:"моноклинични",tipElementa:"ravan",opisElementa:"Раван близањења (001), c* нормала одступа ~26° од c-осе због β ≈ 116°",normalaRavniIliOsa:[.4384,0,.8988],izvor:"Klein & Dutrow 2007, str. 235"},"albitski-polisintetski":{zakon:"albitski-polisintetski",naziv:"Албитски полисинтетски закон",mineral:"албит / плагиоклас",sistem:"триклинични",tipElementa:"ravan",opisElementa:"Раван близањења (010), вишеструке паралелне ламеле",normalaRavniIliOsa:[0,1,0],izvor:"Nesse 2012, str. 280"},japanski:{zakon:"japanski",naziv:"Јапански закон",mineral:"кварц",sistem:"тригонални",tipElementa:"ravan",opisElementa:"Раван близањења (11-22), теоријски угао међу c-осама 84°33′",normalaRavniIliOsa:[.37,.6408,.6726],ugaoOsaStepeni:84.55,izvor:"Frondel 1962, Dana System of Mineralogy Vol. III (a 4,913 c 5,405 Å)",napomena:"Угао 84°33′ је теоријски угао контакта две јединке кварца по (11-22)."},dofinejski:{zakon:"dofinejski",naziv:"Дофинејски закон",mineral:"кварц",sistem:"тригонални",tipElementa:"osa",opisElementa:"Оса близањења [0001] (c-оса), ротација за 180°",normalaRavniIliOsa:[0,0,1],ugaoRotacijeStepeni:180,izvor:"Klein & Dutrow 2007, str. 236"},brazilski:{zakon:"brazilski",naziv:"Бразилски закон",mineral:"кварц",sistem:"тригонални",tipElementa:"ravan",opisElementa:"Раван близањења (11-20), нормала [0,5, √3/2, 0] ≠ [100]",normalaRavniIliOsa:[.5,.866025,0],izvor:"Klein & Dutrow 2007, str. 236; International Tables хексагонска метрика"},"lastin-rep":{zakon:"lastin-rep",naziv:"Ластин реп (близанац гипса)",mineral:"гипс",sistem:"моноклинични",tipElementa:"ravan",opisElementa:"Раван близањења (100)",normalaRavniIliOsa:[1,0,0],izvor:"Klein & Dutrow 2007, str. 235"},"staurolit-90":{zakon:"staurolit-90",naziv:"Крстасти близанац стауролита (90°)",mineral:"стауролит",sistem:"моноклинични / псеудоорторомбични",tipElementa:"ravan",opisElementa:"Раван близањења (031), две јединке под ~90°",normalaRavniIliOsa:[0,.7071,.7071],izvor:"Klein & Dutrow 2007, str. 234"},"staurolit-60":{zakon:"staurolit-60",naziv:"Коси крстасти близанац стауролита (60°)",mineral:"стауролит",sistem:"моноклинични / псеудоорторомбични",tipElementa:"ravan",opisElementa:"Раван близањења (231), две c-осе заклапају ~60° (59°05′)",normalaRavniIliOsa:[.7093,.5038,.4931],ugaoOsaStepeni:59.08,izvor:"Klein & Dutrow 2007, str. 234 (метрика: a 7,87 b 16,62 c 5,66 Å)"},"kolenasti-rutil":{zakon:"kolenasti-rutil",naziv:"Коленасти близанац рутила",mineral:"рутил",sistem:"тетрагонални",tipElementa:"ravan",opisElementa:"Раван близањења (011), прегиб c-оса под 114°30′",normalaRavniIliOsa:[0,.542,.8404],ugaoOsaStepeni:114.5,izvor:"Klein & Dutrow 2007, str. 234 (тетрагонално a 4,59 c 2,96 Å)"},"trilinga-aragonit":{zakon:"trilinga-aragonit",naziv:"Циклички трилинг арагонита",mineral:"арагонит",sistem:"орторомбични",tipElementa:"ravan",opisElementa:"Раван близањења (110), псеудохексагонални склоп",normalaRavniIliOsa:[.707,.707,0],izvor:"Klein & Dutrow 2007, str. 235"},"gvozdeni-krst-pirit":{zakon:"gvozdeni-krst-pirit",naziv:"Гвоздени крст (близанац пирита)",mineral:"пирит",sistem:"кубни (m-3)",tipElementa:"osa",opisElementa:"Оса близањења [001] са прорастањем два пиритоедра",normalaRavniIliOsa:[0,0,1],ugaoRotacijeStepeni:90,izvor:"Klein & Dutrow 2007, str. 234"}};function Hm(n){const e=[];if(n.includes("спинел")||n.includes("октаедар"))for(const r of[1,-1])for(const s of[1,-1])for(const a of[1,-1]){const o=1/Math.sqrt(3);e.push({normala:[r*o,s*o,a*o],d:1})}else if(n.includes("ортоклас"))e.push({normala:[.707,.707,0],d:.9},{normala:[-.707,.707,0],d:.9},{normala:[.707,-.707,0],d:.9},{normala:[-.707,-.707,0],d:.9},{normala:[0,1,0],d:1},{normala:[0,-1,0],d:1},{normala:[0,0,1],d:1.5},{normala:[0,0,-1],d:1.5},{normala:[.5,0,.866],d:1.1},{normala:[-.5,0,-.866],d:1.1});else if(n.includes("кварц")){const r=Math.sqrt(3),s=[[1,0,0],[-1,0,0],[.5,r/2,0],[-.5,r/2,0],[.5,-r/2,0],[-.5,-r/2,0]];for(const l of s)e.push({normala:l,d:.85});const a=51.78*Math.PI/180,o=Math.sin(a),c=Math.cos(a);for(let l=0;l<6;l++){const d=l*60*Math.PI/180;e.push({normala:[o*Math.cos(d),o*Math.sin(d),c],d:1.35}),e.push({normala:[o*Math.cos(d),o*Math.sin(d),-c],d:1.35})}}else if(n.includes("пирит")){const r=[[0,1,2],[1,2,0],[2,0,1]],s=[[1,1],[1,-1],[-1,1],[-1,-1]],a=Math.sqrt(5);for(const o of r)for(const c of s){const l=[0,0,0];l[o[0]]=2*c[0]/a,l[o[1]]=1*c[1]/a,l[o[2]]=0,e.push({normala:[l[0],l[1],l[2]],d:1})}}else e.push({normala:[1,0,0],d:.75},{normala:[-1,0,0],d:.75},{normala:[0,1,0],d:.85},{normala:[0,-1,0],d:.85},{normala:[0,0,1],d:1.6},{normala:[0,0,-1],d:1.6},{normala:[.707,0,.707],d:1.25},{normala:[-.707,0,.707],d:1.25},{normala:[.707,0,-.707],d:1.25},{normala:[-.707,0,-.707],d:1.25});const t=Qi(e),i=er(t);return{mreza:i.geometrijaMreze,ivice:i.geometrijaIvica}}function mc(n){const e=new oe(n.token("--primary")),t=Ka(e,[n.token("--accent"),n.token("--success"),n.token("--info")]);return[e,t]}const Gm={izgled:"kristal",imaPodrazumevanuAnimaciju(n){return(n.animacija??"razdvoji-spoji")!=="nema"},pocetnaKamera(){return{theta:.65,phi:1.15,udaljenost:5.8}},kreiraj(n,e){const t=new nt;n.scena3D.add(t);const i=pc[e.zakon]??pc.karlsbadski,r=Hm(i.mineral),s=r.mreza,[a,o]=mc(n.tema),c=n.tema.token("--text-primary"),l=ti(a),d=ti(o),h=tr(c,a),f=tr(c,o),m=new Le(s,l);m.add(new dt(r.ivice,h));const g=s.clone(),_=r.ivice.clone(),p=new Le(g,d);p.add(new dt(_,f));const u=new k(...i.normalaRavniIliOsa).normalize(),E=new nt;if(E.add(p),i.tipElementa==="osa"){const U=(i.ugaoRotacijeStepeni??180)*Math.PI/180;p.rotateOnAxis(u,U)}else{const U=new at().set(1-2*u.x*u.x,-2*u.x*u.y,-2*u.x*u.z,0,-2*u.y*u.x,1-2*u.y*u.y,-2*u.y*u.z,0,-2*u.z*u.x,-2*u.z*u.y,1-2*u.z*u.z,0,0,0,0,1);g.applyMatrix4(U),_.applyMatrix4(U);const A=g.index;if(A){for(let R=0;R<A.count;R+=3){const z=A.getX(R+1);A.setX(R+1,A.getX(R+2)),A.setX(R+2,z)}A.needsUpdate=!0}g.computeVertexNormals()}t.add(m),t.add(E),s.computeBoundingSphere();const y=s.boundingSphere?.radius??1.5;n.dodajKontaktnuSenku(y*1.7,-y*1.15-.1);const M=new Ln({color:new oe(n.tema.token("--warning")),transparent:!0,opacity:.3,side:Tt,depthWrite:!1}),D=new mt({color:new oe(n.tema.token("--warning")),linewidth:2});let w=null,b=null;if(e.prikazi_element!==!1)if(i.tipElementa==="ravan"){const U=new ni(3.5,3.5);w=new Le(U,M),w.renderOrder=-.5,w.add(new dt(new Ji(U),D)),w.quaternion.setFromUnitVectors(new k(0,0,1),u),t.add(w)}else{const U=new Ke,A=u.clone().multiplyScalar(-2.8),R=u.clone().multiplyScalar(2.8);U.setAttribute("position",new je([A.x,A.y,A.z,R.x,R.y,R.z],3)),b=new $i(U,D),t.add(b)}const C=document.createElement("div");C.className="udzbenik-scena-status",C.textContent=`${i.naziv} (${i.mineral}) • ${i.opisElementa}`,n.podnozje.append(C);const v=e.animacija??"razdvoji-spoji";let x=0;function P(){const[U,A]=mc(n.tema),R=n.tema.token("--text-primary");l.color.copy(U),d.color.copy(A),h.color.copy(zi(R,U)),f.color.copy(zi(R,A)),M.color.set(n.tema.token("--warning")),D.color.set(n.tema.token("--warning"))}return{azuriraj(U){if(x+=U,v==="razdvoji-spoji"){const A=(Math.sin(x*1.5)*.5+.5)*1.1;E.position.copy(u.clone().multiplyScalar(A)),n.korisnikUpravlja()||(t.rotation.y+=U*.25)}else v==="rotacija"&&!n.korisnikUpravlja()&&(t.rotation.y+=U*.45)},korak(){x+=.4;const U=(Math.sin(x*1.5)*.5+.5)*1.1;E.position.copy(u.clone().multiplyScalar(U)),t.rotation.y+=.2},resetuj(){x=0,E.position.set(0,0,0),t.rotation.set(0,0,0)},osveziTemu(){P()},raspolazi(){s.dispose(),p.geometry.dispose(),l.dispose(),d.dispose(),h.dispose(),f.dispose(),M.dispose(),D.dispose(),w&&w.geometry.dispose(),b&&b.geometry.dispose(),Lt(t),C.remove()}}}};class jn extends Error{constructor(e){super(e),this.name="CifGreska"}}function on(n,e){const t=n.trim().replace(/\([0-9]+\)$/,""),i=Number(t);if(!Number.isFinite(i))throw new jn(`Неисправна нумеричка вредност у CIF пољу ${e}: "${n}"`);return i}function Ur(n){const e=[];let t=0;const i=n.length;for(;t<i;){for(;t<i&&/\s/.test(n[t]);)t++;if(t>=i)break;const r=n[t];if(r==="#")break;if(r==="'"||r==='"'){const s=r;t++;let a=t;for(;t<i&&!(n[t]===s&&(t+1>=i||/\s/.test(n[t+1])));)t++;e.push(n.slice(a,t)),t<i&&n[t]===s&&t++}else{const s=t;for(;t<i&&!/\s/.test(n[t]);)t++;e.push(n.slice(s,t))}}return e}function jm(n){if(!n||!n.trim())throw new jn("CIF садржај је празан.");const e=n.split(/\r?\n/);let t="struktura";const i=new Map,r=[];let s=0;for(;s<e.length;){const m=e[s].trim();if(!m||m.startsWith("#")){s++;continue}if(m.toLowerCase().startsWith("data_")){t=m.slice(5).trim()||t,s++;continue}if(m.toLowerCase()==="loop_"){s++;const g=[];for(;s<e.length;){const D=e[s].trim();if(!D||D.startsWith("#")){s++;continue}if(D.startsWith("_")){const w=Ur(D);w[0]&&g.push(w[0].toLowerCase()),s++}else break}const _=g.indexOf("_atom_site_label"),p=g.indexOf("_atom_site_type_symbol"),u=g.indexOf("_atom_site_fract_x"),E=g.indexOf("_atom_site_fract_y"),y=g.indexOf("_atom_site_fract_z"),M=_!==-1&&p!==-1&&u!==-1&&E!==-1&&y!==-1;for(;s<e.length;){const D=e[s].trim();if(!D||D.startsWith("#")){s++;continue}const w=D.toLowerCase();if(D.startsWith("_")||w==="loop_"||w.startsWith("data_")||D.startsWith(";"))break;if(M&&g.length>0){const b=Ur(D);if(b.length<g.length)throw new jn("Непотпун ред у _atom_site табели CIF фајла.");const C=b[_],v=b[p],x=on(b[u],"_atom_site_fract_x"),P=on(b[E],"_atom_site_fract_y"),U=on(b[y],"_atom_site_fract_z");r.push({oznaka:C,simbol:fl(v),fx:x,fy:P,fz:U})}s++}continue}if(m.startsWith("_")){const g=Ur(m);if(g.length>=2&&g[0]&&g[1]!==void 0)i.set(g[0].toLowerCase(),g[1]);else if(g.length===1&&g[0]&&s+1<e.length){const _=Ur(e[s+1].trim());_[0]&&!_[0].startsWith("_")&&_[0].toLowerCase()!=="loop_"&&(i.set(g[0].toLowerCase(),_[0]),s++)}}s++}const a=["_cell_length_a","_cell_length_b","_cell_length_c","_cell_angle_alpha","_cell_angle_beta","_cell_angle_gamma"];for(const m of a)if(!i.has(m))throw new jn(`Недостаје обавезно CIF поље: ${m}`);const o=on(i.get("_cell_length_a"),"_cell_length_a"),c=on(i.get("_cell_length_b"),"_cell_length_b"),l=on(i.get("_cell_length_c"),"_cell_length_c"),d=on(i.get("_cell_angle_alpha"),"_cell_angle_alpha"),h=on(i.get("_cell_angle_beta"),"_cell_angle_beta"),f=on(i.get("_cell_angle_gamma"),"_cell_angle_gamma");if(o<=0||c<=0||l<=0)throw new jn("Димензије јединичне ћелије a, b, c морају бити позитивне.");if(d<=0||d>=180||h<=0||h>=180||f<=0||f>=180||d+h+f>=360)throw new jn("Углови јединичне ћелије α, β, γ нису физички валидни.");if(r.length===0)throw new jn("CIF не садржи ниједан атом у loop_ _atom_site блоку.");return{nazivBloka:t,celija:{a:o,b:c,c:l,alpha:d,beta:h,gamma:f},atomi:r}}function Ya(n){const e=Math.PI/180,t=n.alpha*e,i=n.beta*e,r=n.gamma*e,s=Math.cos(t),a=Math.cos(i),o=Math.cos(r),c=Math.sin(r),l=n.a,d=0,h=n.b*o,f=n.b*c,m=0,g=n.c*a,_=n.c*(s-a*o)/c,p=Math.max(0,n.c*n.c-g*g-_*_),u=Math.sqrt(p);return{va:[l,d,-0],vb:[h,m,-f],vc:[g,u,-_]}}function wn(n,e,t,i){return[n*i.va[0]+e*i.vb[0]+t*i.vc[0],n*i.va[1]+e*i.vb[1]+t*i.vc[1],n*i.va[2]+e*i.vb[2]+t*i.vc[2]]}const Us=[{kljuc:"kubna-P",naziv:"Кубна примитивна (P)",sistem:"Кубни",centriranje:"P",brojCvorova:1,celija:{a:1.8,b:1.8,c:1.8,alpha:90,beta:90,gamma:90},cvoroviFrakcioni:[[0,0,0]]},{kljuc:"kubna-I",naziv:"Кубна просторно центрирана (I)",sistem:"Кубни",centriranje:"I",brojCvorova:2,celija:{a:1.8,b:1.8,c:1.8,alpha:90,beta:90,gamma:90},cvoroviFrakcioni:[[0,0,0],[.5,.5,.5]],primitivniVektori:[[-.5,.5,.5],[.5,-.5,.5],[.5,.5,-.5]]},{kljuc:"kubna-F",naziv:"Кубна површински центрирана (F)",sistem:"Кубни",centriranje:"F",brojCvorova:4,celija:{a:1.8,b:1.8,c:1.8,alpha:90,beta:90,gamma:90},cvoroviFrakcioni:[[0,0,0],[0,.5,.5],[.5,0,.5],[.5,.5,0]],primitivniVektori:[[0,.5,.5],[.5,0,.5],[.5,.5,0]]},{kljuc:"tetragonalna-P",naziv:"Тетрагонална примитивна (P)",sistem:"Тетрагонални",centriranje:"P",brojCvorova:1,celija:{a:1.6,b:1.6,c:2.3,alpha:90,beta:90,gamma:90},cvoroviFrakcioni:[[0,0,0]]},{kljuc:"tetragonalna-I",naziv:"Тетрагонална просторно центрирана (I)",sistem:"Тетрагонални",centriranje:"I",brojCvorova:2,celija:{a:1.6,b:1.6,c:2.3,alpha:90,beta:90,gamma:90},cvoroviFrakcioni:[[0,0,0],[.5,.5,.5]],primitivniVektori:[[-.5,.5,.5],[.5,-.5,.5],[.5,.5,-.5]]},{kljuc:"ortorombicna-P",naziv:"Орторомбична примитивна (P)",sistem:"Орторомбични",centriranje:"P",brojCvorova:1,celija:{a:1.4,b:1.9,c:2.4,alpha:90,beta:90,gamma:90},cvoroviFrakcioni:[[0,0,0]]},{kljuc:"ortorombicna-C",naziv:"Орторомбична базно центрирана (C)",sistem:"Орторомбични",centriranje:"C",brojCvorova:2,celija:{a:1.4,b:1.9,c:2.4,alpha:90,beta:90,gamma:90},cvoroviFrakcioni:[[0,0,0],[.5,.5,0]],primitivniVektori:[[.5,.5,0],[-.5,.5,0],[0,0,1]]},{kljuc:"ortorombicna-I",naziv:"Орторомбична просторно центрирана (I)",sistem:"Орторомбични",centriranje:"I",brojCvorova:2,celija:{a:1.4,b:1.9,c:2.4,alpha:90,beta:90,gamma:90},cvoroviFrakcioni:[[0,0,0],[.5,.5,.5]],primitivniVektori:[[-.5,.5,.5],[.5,-.5,.5],[.5,.5,-.5]]},{kljuc:"ortorombicna-F",naziv:"Орторомбична површински центрирана (F)",sistem:"Орторомбични",centriranje:"F",brojCvorova:4,celija:{a:1.4,b:1.9,c:2.4,alpha:90,beta:90,gamma:90},cvoroviFrakcioni:[[0,0,0],[0,.5,.5],[.5,0,.5],[.5,.5,0]],primitivniVektori:[[0,.5,.5],[.5,0,.5],[.5,.5,0]]},{kljuc:"heksagonalna-P",naziv:"Хексагонална примитивна (P)",sistem:"Хексагонални",centriranje:"P",brojCvorova:1,celija:{a:1.8,b:1.8,c:2.2,alpha:90,beta:90,gamma:120},cvoroviFrakcioni:[[0,0,0]]},{kljuc:"romboedarska-R",naziv:"Ромбоедарска (R, хексагонална поставка)",sistem:"Тригонални",centriranje:"R",brojCvorova:3,celija:{a:1.8,b:1.8,c:2.5,alpha:90,beta:90,gamma:120},cvoroviFrakcioni:[[0,0,0],[2/3,1/3,1/3],[1/3,2/3,2/3]],primitivniVektori:[[2/3,1/3,1/3],[-1/3,1/3,1/3],[-1/3,-2/3,1/3]]},{kljuc:"monoklinicna-P",naziv:"Моноклинична примитивна (P)",sistem:"Моноклинични",centriranje:"P",brojCvorova:1,celija:{a:1.5,b:1.8,c:2.1,alpha:90,beta:110,gamma:90},cvoroviFrakcioni:[[0,0,0]]},{kljuc:"monoklinicna-C",naziv:"Моноклинична базно центрирана (C)",sistem:"Моноклинични",centriranje:"C",brojCvorova:2,celija:{a:1.5,b:1.8,c:2.1,alpha:90,beta:110,gamma:90},cvoroviFrakcioni:[[0,0,0],[.5,.5,0]],primitivniVektori:[[.5,.5,0],[-.5,.5,0],[0,0,1]]},{kljuc:"triklinicna-P",naziv:"Триклинична примитивна (P)",sistem:"Триклинични",centriranje:"P",brojCvorova:1,celija:{a:1.4,b:1.7,c:2.1,alpha:78,beta:108,gamma:102},cvoroviFrakcioni:[[0,0,0]]}],Wm={imaPodrazumevanuAnimaciju(){return!0},pocetnaKamera(){return{theta:.65,phi:1.15,udaljenost:6.8}},kreiraj(n,e){let t=e.resetka==="sve"?"kubna-P":e.resetka;const i=new nt;n.scena3D.add(i);const r=new mn(.08,16,16),s=new pt({color:new oe(n.tema.token("--primary")),roughness:.25,metalness:.2}),a=new pt({color:new oe(n.tema.token("--accent")),roughness:.25,metalness:.2}),o=new mt({color:new oe(n.tema.token("--text-secondary")),linewidth:2}),c=new ku({color:new oe(n.tema.token("--border-color")),dashSize:.15,gapSize:.1}),l=new mt({color:new oe(n.tema.token("--warning")),linewidth:2});function d(p){for(;i.children.length>0;){const U=i.children[0];i.remove(U),Lt(U)}const u=Ya(p.celija),E=new k(...u.va),y=new k(...u.vb),M=new k(...u.vc),w=E.clone().add(y).add(M).multiplyScalar(.5).clone().negate(),b=[[0,0,0],[1,0,0],[1,1,0],[0,1,0],[0,0,1],[1,0,1],[1,1,1],[0,1,1]].map(([U,A,R])=>{const[z,N,O]=wn(U,A,R,u);return new k(z,N,O).add(w)}),C=[[0,1],[1,2],[2,3],[3,0],[4,5],[5,6],[6,7],[7,4],[0,4],[1,5],[2,6],[3,7]],v=[];for(const U of C){const A=b[U[0]],R=b[U[1]];v.push(A.x,A.y,A.z,R.x,R.y,R.z)}const x=new Ke;x.setAttribute("position",new je(v,3)),i.add(new dt(x,o));const P=new Set;for(const[U,A,R]of p.cvoroviFrakcioni)for(let z=0;z<=1;z++)for(let N=0;N<=1;N++)for(let O=0;O<=1;O++){const F=U+z,G=A+N,Z=R+O;if(F>=-1e-4&&F<=1.0001&&G>=-1e-4&&G<=1.0001&&Z>=-1e-4&&Z<=1.0001){const Y=`${F.toFixed(2)},${G.toFixed(2)},${Z.toFixed(2)}`;if(P.has(Y))continue;P.add(Y);const[he,Ie,X]=wn(F,G,Z,u),ee=new k(he,Ie,X).add(w),ue=(z===0||z===1)&&(N===0||N===1)&&(O===0||O===1)&&U===0&&A===0&&R===0,re=new Le(r,ue?s:a);re.position.copy(ee),i.add(re)}}if(e.prikazi_susedne_celije){const U=[];for(const z of[-1,0,1])for(const N of[-1,0,1])for(const O of[-1,0,1]){if(z===0&&N===0&&O===0)continue;const F=E.clone().multiplyScalar(z).add(y.clone().multiplyScalar(N)).add(M.clone().multiplyScalar(O));for(const G of C){const Z=b[G[0]].clone().add(F),Y=b[G[1]].clone().add(F);U.push(Z.x,Z.y,Z.z,Y.x,Y.y,Y.z)}}const A=new Ke;A.setAttribute("position",new je(U,3));const R=new dt(A,c);R.computeLineDistances(),i.add(R)}if(e.prikazi_primitivnu_celiju&&p.primitivniVektori){const U=[],A=b[0],R=p.primitivniVektori.map(([Z,Y,he])=>{const[Ie,X,ee]=wn(Z,Y,he,u);return new k(Ie,X,ee)}),z=R[0],N=R[1],O=R[2],F=[A,A.clone().add(z),A.clone().add(z).add(N),A.clone().add(N),A.clone().add(O),A.clone().add(z).add(O),A.clone().add(z).add(N).add(O),A.clone().add(N).add(O)];for(const Z of C){const Y=F[Z[0]],he=F[Z[1]];U.push(Y.x,Y.y,Y.z,he.x,he.y,he.z)}const G=new Ke;G.setAttribute("position",new je(U,3)),i.add(new dt(G,l))}}const h=document.createElement("div");h.className="udzbenik-scena-status",n.podnozje.append(h);function f(p){h.textContent=`${p.naziv} • Систем: ${p.sistem} • Чворова по конвенционалној ћелији: ${p.brojCvorova}`}if(e.resetka==="sve"){const p=document.createElement("div");p.className="udzbenik-bravais-traka",p.style.display="flex",p.style.flexWrap="wrap",p.style.gap="4px";for(const u of Us){const E=document.createElement("button");E.type="button",E.className="udzbenik-dugme udzbenik-dugme--malo",u.kljuc===t&&E.classList.add("udzbenik-dugme--aktivno"),E.textContent=u.kljuc,E.setAttribute("aria-label",u.naziv),E.addEventListener("click",()=>{t=u.kljuc,p.querySelectorAll("button").forEach(y=>y.classList.remove("udzbenik-dugme--aktivno")),E.classList.add("udzbenik-dugme--aktivno"),d(u),f(u)}),p.append(E)}n.gornjeKontrole.append(p)}const m=Us.find(p=>p.kljuc===t)??Us[0];d(m),f(m);function g(){s.color.set(n.tema.token("--primary")),a.color.set(n.tema.token("--accent")),o.color.set(n.tema.token("--text-secondary")),c.color.set(n.tema.token("--border-color")),l.color.set(n.tema.token("--warning"))}let _=0;return{azuriraj(p){_+=p*.45,i.rotation.y=_},korak(){_+=.25,i.rotation.y=_},resetuj(){_=0,i.rotation.set(0,0,0)},osveziTemu(){g()},raspolazi(){r.dispose(),s.dispose(),a.dispose(),o.dispose(),c.dispose(),l.dispose(),Lt(i),h.remove()}}}};function Xm(n,e){const t=e??56,i=Math.round((180-t)*10)/10;switch(n){case"kubna":return{naziv:"Кубна цепљивост {100}",brojPravaca:"3 правца",uglovi:"90°",podrazumevaniPrimer:"халит, галенит"};case"oktaedarska":return{naziv:"Октаедарска цепљивост {111}",brojPravaca:"4 правца",uglovi:"70,5° и 109,5°",podrazumevaniPrimer:"флуорит, дијамант"};case"dodekaedarska":return{naziv:"Додекаедарска цепљивост {110}",brojPravaca:"6 праваца",uglovi:"60°, 90° и 120°",podrazumevaniPrimer:"сфалерит"};case"romboedarska":return{naziv:"Ромбоедарска цепљивост {101̄1}",brojPravaca:"3 правца",uglovi:"~75° и ~105° (≠ 90°)",podrazumevaniPrimer:"калцит, доломит"};case"bazalna":return{naziv:"Базална (пинакоидална) цепљивост {001}",brojPravaca:"1 правац",uglovi:"паралелне ламеле (0°)",podrazumevaniPrimer:"лискун (мусковит), графит"};case"prizmatska":return{naziv:"Призматска цепљивост {110}",brojPravaca:"2 правца",uglovi:`${t}° и ${i}°`,podrazumevaniPrimer:t>75?"пироксен":"амфибол"};case"nema":return{naziv:"Нема цепљивости (шкољкаст прелом)",brojPravaca:"0 праваца",uglovi:"нема равни цепљивости",podrazumevaniPrimer:"кварц"}}}function Wn(n,e,t,i){const r=Qi(n);if(r.pljosni.length<4||r.temena.length<4)return null;const s=er(r),a=new nt;return a.add(new Le(s.geometrijaMreze,t),new dt(s.geometrijaIvica,i)),{grupa:a,smerRazdvajanja:e}}function cn(n,e,t,i,r){const s=new ni(t,t),a=new Le(s,i),o=new dt(new Ji(s),r),c=new nt;c.add(a,o);const l=new k(...n).normalize();return c.quaternion.setFromUnitVectors(new k(0,0,1),l),c.position.copy(l).multiplyScalar(e),c}function Si(n,e){const t=Math.hypot(n-.35,e-.25),i=.055*Math.sin(t*13.5);return .28*(n*n-.5*e*e)+.18*n+i}function qm(n,e,t,i){if(!n){const h=[{normala:[0,-1,0],d:1.15}];for(let m=0;m<6;m++){const g=m*Math.PI/3,_=Math.cos(g),p=Math.sin(g);h.push({normala:[_,0,p],d:.95}),h.push({normala:[_*.72,.69,p*.72],d:1.28}),h.push({normala:[_*.72,-.69,p*.72],d:1.28})}const f=Wn(h,new k(0,0,0),e,i);return{fragmenti:f?[f]:[]}}const o=12,c=24;function l(h,f){const m=(f%(Math.PI/3)+Math.PI/3)%(Math.PI/3)-Math.PI/6,g=.95*Math.cos(Math.PI/6)/Math.cos(m);return[h*g*Math.cos(f),h*g*Math.sin(f)]}function d(h){const f=[],m=[],g=[],_=h?1.15:-1.15,p=h?1.85:-1.85;for(let D=0;D<o;D++){const w=D/o,b=(D+1)/o;for(let C=0;C<c;C++){const v=C/c*Math.PI*2,x=(C+1)/c*Math.PI*2,[P,U]=l(w,v),[A,R]=l(b,v),[z,N]=l(b,x),[O,F]=l(w,x),G=Si(P,U),Z=Si(A,R),Y=Si(z,N),he=Si(O,F);h?m.push(P,G,U,z,Y,N,A,Z,R,P,G,U,O,he,F,z,Y,N):m.push(P,G,U,A,Z,R,z,Y,N,P,G,U,z,Y,N,O,he,F)}}for(let D=0;D<c;D++){const w=D/c*Math.PI*2,b=(D+1)/c*Math.PI*2,[C,v]=l(1,w),[x,P]=l(1,b),U=Si(C,v),A=Si(x,P);h?(f.push(C,U,v,x,A,P,x,_,P,C,U,v,x,_,P,C,_,v),f.push(C,_,v,x,_,P,0,p,0)):(f.push(C,_,v,x,_,P,x,A,P,C,_,v,x,A,P,C,U,v),f.push(x,_,P,C,_,v,0,p,0)),g.push(C,U,v,x,A,P),g.push(C,_,v,x,_,P),D%(c/6)===0&&(g.push(C,U,v,C,_,v),g.push(C,_,v,0,p,0))}const u=new Ke;u.setAttribute("position",new je(f,3)),u.computeVertexNormals();const E=new Ke;E.setAttribute("position",new je(m,3)),E.computeVertexNormals();const y=new Ke;y.setAttribute("position",new je(g,3));const M=new nt;return M.add(new Le(u,e),new Le(E,t),new dt(y,i)),M}return{fragmenti:[{grupa:d(!0),smerRazdvajanja:new k(.18,.55,.1)},{grupa:d(!1),smerRazdvajanja:new k(-.18,-.55,-.1)}]}}const gc=.4;function _c(n){return Ka(n.token("--primary"),[n.token("--accent"),n.token("--warning"),n.token("--info"),n.token("--success")])}const Km={izgled:"kristal",imaPodrazumevanuAnimaciju(n){return!(n.vrsta==="nema"&&!n.prikazi_prelom)},pocetnaKamera(){return{theta:.68,phi:1.14,udaljenost:5.9}},kreiraj(n,e){const t=e.vrsta,i=e.ugao??56,r=e.prikazi_prelom??!1,s=new nt,a=new nt,o=new nt;s.add(a,o),n.scena3D.add(s);const c=_c(n.tema),l=ti(n.tema.token("--primary"),{providnost:.45}),d=ti(c,{providnost:.6});d.flatShading=!1;const h=tr(n.tema.token("--text-primary"),n.tema.token("--primary")),f=new Ln({color:c.clone(),transparent:!0,opacity:gc,side:Tt,depthWrite:!1}),m=new mt({color:c.clone()}),g=[];function _(){if(t==="kubna"){const b=[-1,1];for(const C of b)for(const v of b)for(const x of b){const P=[{normala:[C,0,0],d:1.05},{normala:[-C,0,0],d:0},{normala:[0,v,0],d:1.05},{normala:[0,-v,0],d:0},{normala:[0,0,x],d:1.05},{normala:[0,0,-x],d:0}],U=Wn(P,new k(C,v,x).normalize().multiplyScalar(.52),l,h);U&&g.push(U)}o.add(cn([1,0,0],0,2.6,f,m),cn([0,1,0],0,2.6,f,m),cn([0,0,1],0,2.6,f,m))}else if(t==="oktaedarska"){const b=io([1,1,1]).map(v=>({normala:v.normala,d:1.08})),C=[[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]];for(let v=0;v<16;v++){const x=[...b],P=new k;for(let A=0;A<4;A++){const R=(v&1<<A)!==0?1:-1,z=C[A];x.push({normala:[z[0]*R,z[1]*R,z[2]*R],d:0}),P.add(new k(z[0]*R,z[1]*R,z[2]*R))}const U=Wn(x,P.lengthSq()>1e-4?P.normalize().multiplyScalar(.52):P,l,h);U&&g.push(U)}for(const v of C)o.add(cn(v,0,2.8,f,m))}else if(t==="dodekaedarska"){const b=io([1,1,0]).map(x=>({normala:x.normala,d:1.12})),C=[[1,1,0],[1,-1,0],[1,0,1],[1,0,-1],[0,1,1],[0,1,-1]];for(const x of C)o.add(cn(x,0,2.7,f,m));const v=[[1,1,0],[1,-1,0],[0,1,1]];for(let x=0;x<8;x++){const P=[...b],U=new k;for(let R=0;R<3;R++){const z=(x&1<<R)!==0?1:-1,N=v[R];P.push({normala:[N[0]*z,N[1]*z,N[2]*z],d:0}),U.add(new k(N[0]*z,N[1]*z,N[2]*z))}const A=Wn(P,U.normalize().multiplyScalar(.5),l,h);A&&g.push(A)}}else if(t==="romboedarska"){const b=[1,.26,.14],C=[.24,1,.22],v=[.18,.26,1],x=[b,C,v],P=[];for(const A of x)P.push({normala:A,d:1}),P.push({normala:[-A[0],-A[1],-A[2]],d:1}),o.add(cn(A,0,2.8,f,m));const U=[-1,1];for(const A of U)for(const R of U)for(const z of U){const N=[...P,{normala:[-b[0]*A,-b[1]*A,-b[2]*A],d:0},{normala:[-C[0]*R,-C[1]*R,-C[2]*R],d:0},{normala:[-v[0]*z,-v[1]*z,-v[2]*z],d:0}],O=new k(b[0]*A+C[0]*R+v[0]*z,b[1]*A+C[1]*R+v[1]*z,b[2]*A+C[2]*R+v[2]*z).normalize().multiplyScalar(.5),F=Wn(N,O,l,h);F&&g.push(F)}}else if(t==="bazalna"){const b=[];for(let P=0;P<6;P++){const U=P*Math.PI/3;b.push({normala:[Math.cos(U),0,Math.sin(U)],d:1.15})}const C=5,v=1.1,x=v/C;for(let P=0;P<C;P++){const U=-v/2+P*x,A=U+x,R=[...b,{normala:[0,1,0],d:A},{normala:[0,-1,0],d:-U}],z=P-(C-1)/2,N=Wn(R,new k(z*.08,z*.28,0),l,h);N&&g.push(N),P>0&&o.add(cn([0,1,0],U,2.7,f,m))}}else if(t==="prizmatska"){const b=i*Math.PI/180*.5,C=[Math.sin(b),0,Math.cos(b)],v=[-Math.sin(b),0,Math.cos(b)],x=[{normala:[0,1,0],d:1.3},{normala:[0,-1,0],d:1.3},{normala:C,d:.9},{normala:[-C[0],0,-C[2]],d:.9},{normala:v,d:.9},{normala:[-v[0],0,-v[2]],d:.9}];o.add(cn(C,0,2.9,f,m),cn(v,0,2.9,f,m));const P=[-1,1];for(const U of P)for(const A of P){const R=[...x,{normala:[-C[0]*U,0,-C[2]*U],d:0},{normala:[-v[0]*A,0,-v[2]*A],d:0}],z=new k(C[0]*U+v[0]*A,0,C[2]*U+v[2]*A).normalize().multiplyScalar(.48),N=Wn(R,z,l,h);N&&g.push(N)}}else{const b=qm(r,l,d,h);g.push(...b.fragmenti)}for(const b of g)a.add(b.grupa)}_();const p=new Fi().setFromObject(a);if(!p.isEmpty()){const b=Math.max(p.max.x-p.min.x,p.max.z-p.min.z);n.dodajKontaktnuSenku(b*.85+.4,p.min.y-.35)}const u=Xm(t,i),E=e.primer||u.podrazumevaniPrimer,y=document.createElement("div");y.className="udzbenik-scena-info-red udzbenik-cepljivost-meta";const M=[[ct("brojPravacaCepljivosti"),u.brojPravaca],[ct("ugloviCepljivosti"),u.uglovi],[ct("primerMinerala"),E]];for(const[b,C]of M){const v=document.createElement("span");v.className="udzbenik-meta-stavka";const x=document.createElement("strong");x.textContent=`${b}: `;const P=document.createElement("span");P.textContent=C,v.append(x,P),y.append(v)}n.podnozje.append(y);let D=n.smanjenPokret?.72:0;function w(){if(t==="nema"&&!r){o.visible=!1;return}let b=0,C=0;if(D<.3)b=D/.3,C=0;else if(D<.72){b=1;const v=(D-.3)/.42;C=v*v*(3-2*v)}else if(D<.85)b=1,C=1;else{const v=(D-.85)/.15;b=1-v,C=1-v*v*(3-2*v)}o.visible=t!=="nema"&&b>.02,o.scale.setScalar(.25+.75*b),f.opacity=gc*b*(1-.45*C);for(const v of g)v.grupa.position.copy(v.smerRazdvajanja).multiplyScalar(C)}return w(),{azuriraj(b){D=(D+b*.17)%1,n.korisnikUpravlja()||(s.rotation.y+=b*.24),w()},korak(){D=(D+.18)%1,w()},resetuj(){s.rotation.set(0,0,0),D=n.smanjenPokret?.72:0,w()},osveziTemu(b){const C=_c(b);l.color.set(b.token("--primary")),d.color.copy(C),h.color.copy(zi(b.token("--text-primary"),b.token("--primary"))),f.color.copy(C),m.color.copy(C)},raspolazi(){Lt(s),l.dispose(),d.dispose(),h.dispose(),f.dispose(),m.dispose()}}}},sl=new Map,Ym=["m-3m","m-3","-43m","432","4/mmm","6/mmm","6/m","-3m","32","mmm","2/m"];for(const n of Ym){let e="kubni";n==="4/mmm"?e="tetragonalni":n==="6/mmm"||n==="6/m"?e="heksagonalni":n==="-3m"||n==="32"?e="trigonalni":n==="mmm"?e="ortorombicni":n==="2/m"&&(e="monoklinicni"),sl.set(n,(t,i)=>Da(t,n,e,i))}const $m=["kubni","tetragonalni","heksagonalni","trigonalni","ortorombicni"];for(const n of $m){const e=Ac(n);sl.set(n,(t,i)=>Da(t,e,n,i))}function Zm(n,e,t,i){const r=t??Ac(e);return Da(n,r,e,i)}const Jm={izgled:"kristal",imaPodrazumevanuAnimaciju(n){return(n.animacija??"prelaz")!=="nema"},pocetnaKamera(){return{theta:.64,phi:1.12,udaljenost:4.8}},kreiraj(n,e){const t=e.animacija??"prelaz",r=e.forme.map((A,R)=>{const z=`forma-${R}`,N=A.naziv||(A.hkl.length===4?`{${A.hkl.join(" ")}}`:pl(A.hkl)),O=Zm(A.hkl,e.sistem,e.klasa,e.celija);return{grupaId:z,oznakaForme:N,baznoD:A.d,hkl:A.hkl,ekvivalentne:O}}),s=new nt;n.scena3D.add(s),n.dodajKontaktnuSenku(1.7,-1.6);const a=tr(n.tema.token("--text-primary"),n.tema.token("--primary")),o=r.map((A,R)=>{const z=ti(n.tema.token("--primary"));return z.name=`mat-forma-${R}`,z});let c=null,l=null,d="";function h(){const A=new oe(n.tema.token("--primary")),R=Ka(A,[n.tema.token("--accent"),n.tema.token("--info"),n.tema.token("--success")]),z=new oe(n.tema.token("--bg-elevated"));for(let N=0;N<o.length;N++){const O=o[N],F=r[N].grupaId,G=r.length>1?N/(r.length-1):0,Z=A.clone().lerp(R,G);N%2===1&&r.length>2&&Z.lerp(z,.22),O.color.copy(Z);const Y=c===F;O.emissive.copy(Y?Z.clone().multiplyScalar(.28):new oe(0,0,0))}a.color.copy(zi(n.tema.token("--text-primary"),A))}h();const f=document.createElement("div");f.className="udzbenik-scena-etiketa udzbenik-scena-etiketa--istaknuta",f.hidden=!0,n.slojEtiketa.append(f);let m=.5,g=n.smanjenPokret?.25:0,_=null;if(r.length>1){const A=document.createElement("label");A.className="udzbenik-klizac-oznaka";const R=document.createElement("span");R.textContent=`${ct("prelazFormi")}: ${r[0].oznakaForme} ↔ ${r[r.length-1].oznakaForme}`,_=document.createElement("input"),_.type="range",_.min="0",_.max="1",_.step="0.01",_.value="0.5",_.className="udzbenik-klizac",_.addEventListener("input",()=>{m=Number(_.value),v(m),n.zatraziRender()}),A.append(R,_),n.gornjeKontrole.append(A)}const p=document.createElement("div");p.className="udzbenik-habitus-forme";const u=new Map;for(const A of r){const R=document.createElement("button");R.type="button",R.className="udzbenik-mohs-cip",R.textContent=A.oznakaForme;const z=()=>{c=A.grupaId;const N=D?.pljosni.find(O=>O.grupaId===A.grupaId);N?(l=new k(...N.centar),d=`${A.oznakaForme} · ${N.oznaka}`):(l=null,d=A.oznakaForme),h(),b(),n.zatraziRender()};R.addEventListener("click",z),R.addEventListener("focus",z),R.addEventListener("blur",()=>{c===A.grupaId&&(c=null,l=null,h(),b(),n.zatraziRender())}),u.set(A.grupaId,R),p.append(R)}const E=document.createElement("span");E.className="udzbenik-habitus-status",p.append(E),n.podnozje.append(p);let y=null,M=null,D=null,w=[];function b(){if(!D)return;const A=D.pljosni.length,R=D.temena.length,z=e.primer?` · ${ct("primerMinerala")}: ${e.primer}`:"",N=d&&c?` · ${d}`:"";E.textContent=`${A} пљосни, ${R} темена${z}${N}`;for(const[O,F]of u.entries()){const G=D.pljosni.some(Z=>Z.grupaId===O);F.classList.toggle("udzbenik-mohs-cip--aktivan",c===O),F.classList.toggle("udzbenik-mohs-cip--prigusen",!G)}}function C(A){const R=r.length;return R<=1?r.map(z=>z.baznoD):r.map((z,N)=>{const O=N/(R-1);let F=1;return A<.5?F=1+(.5-A)*2*O*.95:A>.5&&(F=1+(A-.5)*2*(1-O)*.95),z.baznoD*F})}function v(A){y&&(y.geometry.dispose(),s.remove(y)),M&&(M.geometry.dispose(),s.remove(M));const R=C(A),z=[];for(let Y=0;Y<r.length;Y++){const he=r[Y],Ie=R[Y];for(const X of he.ekvivalentne)z.push({normala:X.normala,d:Ie,grupaId:he.grupaId,oznaka:X.oznaka})}const N=Qi(z);let O=.001;for(const Y of N.temena)O=Math.max(O,Math.hypot(Y[0],Y[1],Y[2]));const F=1.48/O;for(const Y of N.temena)Y[0]*=F,Y[1]*=F,Y[2]*=F;for(const Y of N.pljosni)Y.centar[0]*=F,Y.centar[1]*=F,Y.centar[2]*=F;const G=er(N),Z=G.redosledGrupa.map(Y=>{const he=r.findIndex(Ie=>Ie.grupaId===Y);return o[Math.max(0,he)]});y=new Le(G.geometrijaMreze,Z),M=new dt(G.geometrijaIvica,a),s.add(y,M),D=N,w=G.mapaTrougaoUPljosan,b()}const x=new Xa,P=new We,U=A=>{if(!y||!D)return;const R=n.platno.getBoundingClientRect();if(R.width<=0||R.height<=0)return;P.x=(A.clientX-R.left)/R.width*2-1,P.y=-((A.clientY-R.top)/R.height)*2+1,x.setFromCamera(P,n.kamera);const z=x.intersectObject(y,!1);if(z.length>0&&z[0].faceIndex!==void 0&&z[0].faceIndex!==null){const N=w[z[0].faceIndex],O=N!==void 0?D.pljosni[N]:void 0;if(O){const F=r.find(G=>G.grupaId===O.grupaId);c=O.grupaId,l=new k(...O.centar),d=`${F?.oznakaForme??O.grupaId} · ${O.oznaka}`,h(),b(),n.zatraziRender();return}}c!==null&&A.pointerType==="mouse"&&(c=null,l=null,h(),b(),n.zatraziRender())};return n.platno.addEventListener("pointermove",U),v(m),{azuriraj(A){t==="prelaz"&&r.length>1?(g=(g+A*.14)%1,m=.5-.5*Math.cos(g*Math.PI*2),_&&(_.value=m.toFixed(2)),n.korisnikUpravlja()||(s.rotation.y+=A*.25),v(m)):t==="rotacija"&&!n.korisnikUpravlja()&&(s.rotation.y+=A*.42)},korak(){t==="prelaz"&&r.length>1?(g=(g+.125)%1,m=.5-.5*Math.cos(g*Math.PI*2),_&&(_.value=m.toFixed(2)),v(m)):s.rotation.y+=.35},resetuj(){s.rotation.set(0,0,0),m=.5,g=.25,_&&(_.value="0.5"),c=null,l=null,h(),v(.5)},osveziTemu(){h()},posleRendera(){if(!c||!l){f.hidden=!0;return}s.updateMatrixWorld(!0);const A=l.clone().applyMatrix4(s.matrixWorld),R=n.projektujU2D(A);if(!R.vidljivo){f.hidden=!0;return}f.textContent=d,f.hidden=!1,f.style.transform=`translate(-50%, -120%) translate(${R.x.toFixed(1)}px, ${R.y.toFixed(1)}px)`},raspolazi(){n.platno.removeEventListener("pointermove",U),Lt(s),a.dispose();for(const A of o)A.dispose()}}}},Tn=.8;function Ki(n,e){return n.map(([t,i,r])=>{const s=Math.hypot(t,i,r)||1;return[t/s*e,i/s*e,r/s*e]})}const vc=2/Math.sqrt(3)-1,xc=Math.sqrt(1.5)-1,Mc=Math.SQRT2-1,Sc=Math.sqrt(3)-1,Ec=1,yc={2:{kb:2,nazivOblika:"Линеарни",granicniOdnos:.155,vrhovi:[[0,0,Tn*(1+.155)],[0,0,-Tn*(1+.155)]],trougloviIndeksi:[]},3:{kb:3,nazivOblika:"Троугаони",granicniOdnos:vc,vrhovi:Ki([[1,0,0],[-.5,Math.sqrt(3)/2,0],[-.5,-Math.sqrt(3)/2,0]],Tn*(1+vc)),trougloviIndeksi:[0,1,2]},4:{kb:4,nazivOblika:"Тетраедарски",granicniOdnos:xc,vrhovi:Ki([[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]],Tn*(1+xc)),trougloviIndeksi:[0,1,2,0,3,1,0,2,3,1,3,2]},6:{kb:6,nazivOblika:"Октаедарски",granicniOdnos:Mc,vrhovi:Ki([[1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,1],[0,0,-1]],Tn*(1+Mc)),trougloviIndeksi:[0,2,4,2,1,4,1,3,4,3,0,4,0,5,2,2,5,1,1,5,3,3,5,0]},8:{kb:8,nazivOblika:"Кубични",granicniOdnos:Sc,vrhovi:Ki([[-1,-1,-1],[1,-1,-1],[1,1,-1],[-1,1,-1],[-1,-1,1],[1,-1,1],[1,1,1],[-1,1,1]],Tn*(1+Sc)),trougloviIndeksi:[0,2,1,0,3,2,4,5,6,4,6,7,0,1,5,0,5,4,1,2,6,1,6,5,2,3,7,2,7,6,3,0,4,3,4,7]},12:{kb:12,nazivOblika:"Кубооктаедарски",granicniOdnos:Ec,vrhovi:Ki([[1,1,0],[1,-1,0],[-1,-1,0],[-1,1,0],[1,0,1],[1,0,-1],[-1,0,-1],[-1,0,1],[0,1,1],[0,1,-1],[0,-1,-1],[0,-1,1]],Tn*(1+Ec)),trougloviIndeksi:[0,8,4,1,4,11,2,11,7,3,7,8,0,5,9,1,10,5,2,6,10,3,9,6,0,4,1,0,1,5,2,7,3,2,3,6,8,9,3,8,3,0,11,1,2,11,2,10]}},Qm={izgled:"kristal",imaPodrazumevanuAnimaciju(n){return n.prikazi_odnos_radijusa!==!1},pocetnaKamera(){return{theta:.65,phi:1.18,udaljenost:5.4}},kreiraj(n,e){const t=new nt;n.scena3D.add(t);const i=yc[e.kb]??yc[4],r=Tn,s=r*i.granicniOdnos,a=new mn(s,24,24),o=new pt({color:new oe(n.tema.token("--accent")),roughness:.25,metalness:.2}),c=new Le(a,o);t.add(c);const l=new mn(r,24,24),d=new pt({color:new oe(n.tema.token("--primary")),roughness:.35,metalness:.1,transparent:!0,opacity:.85}),h=new nt;for(const[w,b,C]of i.vrhovi){const v=new Le(l,d);v.position.set(w,b,C),h.add(v)}t.add(h);let f=null,m=null;const g=ti(n.tema.token("--primary"),{providnost:.35}),_=new mt({color:new oe(n.tema.token("--text-secondary")),linewidth:2});if(i.trougloviIndeksi.length>=3){const w=new Ke,b=[];for(const v of i.trougloviIndeksi){const x=i.vrhovi[v];b.push(x[0],x[1],x[2])}w.setAttribute("position",new je(b,3)),w.computeVertexNormals(),f=new Le(w,g),t.add(f);const C=new Ji(w);m=new dt(C,_),t.add(m)}const p=e.katjon||"Katjon",u=e.anjon||"Anjon",E=document.createElement("div");E.className="udzbenik-scena-status",E.textContent=`КБ = ${i.kb} (${i.nazivOblika}) • Гранични однос RA/RX = ${i.granicniOdnos.toFixed(3)} • ${p} / ${u}`,n.podnozje.append(E);let y=0;const M=e.prikazi_odnos_radijusa!==!1;function D(){o.color.set(n.tema.token("--accent")),d.color.set(n.tema.token("--primary")),g.color.set(n.tema.token("--primary")),_.color.set(n.tema.token("--text-secondary"))}return{azuriraj(w){if(y+=w,t.rotation.y=y*.35,M){const b=Math.sin(y*1.8);if(b<-.2){const C=.08*(Math.abs(b)-.2);c.position.set(Math.sin(y*22)*C,Math.cos(y*19)*C,Math.sin(y*25)*C),c.scale.setScalar(.72)}else c.position.set(0,0,0),c.scale.setScalar(1)}},korak(){y+=.3,t.rotation.y+=.2},resetuj(){y=0,c.position.set(0,0,0),c.scale.setScalar(1),t.rotation.set(0,0,0)},osveziTemu(){D()},raspolazi(){a.dispose(),o.dispose(),l.dispose(),d.dispose(),f&&f.geometry.dispose(),m&&m.geometry.dispose(),g.dispose(),_.dispose(),Lt(t),E.remove()}}}},e0={imaPodrazumevanuAnimaciju(){return!1},pocetnaKamera(n){return{theta:.65,phi:1.12,udaljenost:(n.prikaz??"celija")==="supercelija"?8.2:6.2}},kreiraj(n,e){const t=e.prikaz??"celija",i=e.stil??"kugle-stapici",r=e.prikazi_celiju??!0,s=e.oznake_atoma??!0,a=e.poluprecnici??"jonski";let o=!1,c=1.15,l=null,d=-1;const h=new nt,f=new nt,m=new nt,g=new nt;h.add(g,m,f),n.scena3D.add(h);const _=new mt({color:new oe(n.tema.token("--text-secondary"))}),p=new pt({color:new oe(n.tema.token("--text-muted")),roughness:.45,metalness:.15}),u=new Ln({color:new oe(n.tema.token("--accent")),wireframe:!0}),E=new Le(new mn(1,14,12),u);E.visible=!1,h.add(E);const y=document.createElement("div");y.className="udzbenik-scena-etiketa udzbenik-scena-etiketa--atom",y.hidden=!0,n.slojEtiketa.append(y);const M=document.createElement("div");if(M.className="udzbenik-struktura-kontrole",i==="kugle-stapici"){const O=document.createElement("label");O.className="udzbenik-klizac-oznaka";const F=document.createElement("span");F.textContent=`${ct("faktorVeza")}: ×1,15`;const G=document.createElement("input");G.type="range",G.min="0.85",G.max="1.40",G.step="0.05",G.value="1.15",G.className="udzbenik-klizac",G.addEventListener("input",()=>{c=Number(G.value),F.textContent=`${ct("faktorVeza")}: ×${c.toFixed(2).replace(".",",")}`,l&&(A(l),n.zatraziRender())}),O.append(F,G),M.append(O)}const D=document.createElement("span");if(D.className="udzbenik-atom-status",D.setAttribute("aria-live","polite"),s){const O=document.createElement("button");O.type="button",O.className="udzbenik-dugme udzbenik-dugme--malo",O.textContent=ct("sledeciAtom"),O.addEventListener("click",()=>{w.length!==0&&(d=(d+1)%w.length,x(d),n.zatraziRender())}),M.append(O,D)}M.childNodes.length>0&&n.gornjeKontrole.append(M);let w=[],b=null,C=new k,v=1;function x(O){if(O<0||O>=w.length){b=null,E.visible=!1,y.hidden=!0,D.textContent="";return}const F=w[O];b=F.atom;const G=F.mesh.scale.x*1.25;E.position.copy(F.mesh.position),E.scale.setScalar(G),E.visible=!0;const Z=`(${F.atom.fx.toFixed(3)}, ${F.atom.fy.toFixed(3)}, ${F.atom.fz.toFixed(3)})`;y.textContent=`${F.atom.simbol} [${F.atom.oznaka}] ${Z}`,D.textContent=`${F.atom.simbol} (${F.atom.oznaka}): ${Z}`}function P(O){Lt(O),O.clear()}function U(O){n.podnozje.replaceChildren();const F=document.createElement("div");F.className="udzbenik-cpk-legenda",F.setAttribute("aria-label",ct("legendaElemenata"));const G=document.createElement("div");G.className="udzbenik-cpk-stavke";let Z=!1;for(const Ie of O){const X=ro(Ie),ee=so(Ie,a);a==="jonski"&&ee.koriscenaVrsta==="kovalentni"&&(Z=!0);const ue=document.createElement("span");ue.className="udzbenik-cpk-cip";const re=document.createElement("span");re.className="udzbenik-cpk-boja",re.style.backgroundColor=X.bojaHex,re.setAttribute("aria-hidden","true");const le=ee.koriscenaVrsta==="jonski"&&ee.jon?`${X.simbol} (${ee.jon})`:X.simbol,Pe=ee.poluprecnik.toFixed(2).replace(".",","),me=document.createElement("span");me.textContent=`${le} — ${X.naziv} (r = ${Pe} Å)`,ue.append(re,me),G.append(ue)}const Y=document.createElement("p");Y.className="udzbenik-scena-izvor";const he=i==="kugle-stapici"?` · ${ct("detekcijaVezaKovalentniOznaka")}${c.toFixed(2).replace(".",",")}`:"";if(a==="jonski"){const Ie=Z?`${ao.izvor}; ${ct("kovalentnaRezervaOznaka")}: ${oo}`:ao.izvor;Y.textContent=`${ct("poluprecniciJonskiOznaka")} (${ct("izvorPodataka")}: ${Ie})${he}`}else Y.textContent=`${ct("poluprecniciKovalentniOznaka")} (${ct("izvorPodataka")}: ${oo})${he}`;F.append(G,Y),n.podnozje.append(F)}function A(O){P(f),P(m),P(g),w=[];const F=Ya(O.celija),G=t==="supercelija"?2:1,Z=wn(G,G,G,F);C=new k(Z[0]*.5,Z[1]*.5,Z[2]*.5);const Y=Math.max(O.celija.a*G,O.celija.b*G,O.celija.c*G);v=3.6/Math.max(1,Y);const he=[],Ie=new Set,X=[];for(const le of O.atomi){X.includes(le.simbol)||X.push(le.simbol);const Pe=ro(le.simbol),me=so(le.simbol,a),te=(le.fx%1+1)%1,se=(le.fy%1+1)%1,K=(le.fz%1+1)%1,I=te<.001?[0,1]:[0],Ce=se<.001?[0,1]:[0],Se=K<.001?[0,1]:[0];for(let _e=0;_e<G;_e++)for(let ve=0;ve<G;ve++)for(let Ne=0;Ne<G;Ne++)for(const we of I)for(const L of Ce)for(const S of Se){const j=te+_e+we,Q=se+ve+L,ie=K+Ne+S;if(j>G+.001||Q>G+.001||ie>G+.001)continue;const J=`${j.toFixed(3)},${Q.toFixed(3)},${ie.toFixed(3)},${le.simbol}`;if(Ie.has(J))continue;Ie.add(J);const Re=wn(j,Q,ie,F);he.push({oznaka:le.oznaka,simbol:le.simbol,fx:j,fy:Q,fz:ie,pozicija:new k(Re[0],Re[1],Re[2]),poluprecnikPrikaza:me.poluprecnik,kovalentniPoluprecnik:Pe.kovalentniPoluprecnik,bojaHex:Pe.bojaHex})}}const ee=new mn(1,20,16),ue=new Map,re=i==="kugle"?.52:.25;for(const le of he){let Pe=ue.get(le.simbol);Pe||(Pe=new pt({color:new oe(le.bojaHex),roughness:.32,metalness:.1}),ue.set(le.simbol,Pe));const me=new Le(ee,Pe);me.position.copy(le.pozicija).sub(C).multiplyScalar(v);const te=Math.max(.045,le.poluprecnikPrikaza*re*v);me.scale.setScalar(te),f.add(me),w.push({mesh:me,atom:le})}if(i==="kugle-stapici"){const le=new sr(1,1,1,10,1),Pe=new k(0,1,0),me=Math.max(.035,.09*v);for(let te=0;te<he.length;te++){const se=he[te];for(let K=te+1;K<he.length;K++){const I=he[K],Ce=se.pozicija.distanceTo(I.pozicija),Se=(se.kovalentniPoluprecnik+I.kovalentniPoluprecnik)*c;if(Ce>.35&&Ce<=Se){const _e=w[te].mesh.position,Ne=w[K].mesh.position.clone().sub(_e),we=Ne.length();if(we<1e-4)continue;const L=new Le(le,p.clone());L.position.copy(_e).addScaledVector(Ne,.5),L.quaternion.setFromUnitVectors(Pe,Ne.clone().normalize()),L.scale.set(me,we,me),m.add(L)}}}le.dispose()}if(r){const le=[],Pe=[[[0,0,0],[1,0,0]],[[1,0,0],[1,1,0]],[[1,1,0],[0,1,0]],[[0,1,0],[0,0,0]],[[0,0,1],[1,0,1]],[[1,0,1],[1,1,1]],[[1,1,1],[0,1,1]],[[0,1,1],[0,0,1]],[[0,0,0],[0,0,1]],[[1,0,0],[1,0,1]],[[1,1,0],[1,1,1]],[[0,1,0],[0,1,1]]];for(let te=0;te<G;te++)for(let se=0;se<G;se++)for(let K=0;K<G;K++)for(const[I,Ce]of Pe){const Se=wn(I[0]+te,I[1]+se,I[2]+K,F),_e=wn(Ce[0]+te,Ce[1]+se,Ce[2]+K,F),ve=new k(...Se).sub(C).multiplyScalar(v),Ne=new k(..._e).sub(C).multiplyScalar(v);le.push(ve.x,ve.y,ve.z,Ne.x,Ne.y,Ne.z)}const me=new Ke;me.setAttribute("position",new je(le,3)),g.add(new dt(me,_.clone()))}U(X),d=-1,x(-1)}const R=new Xa,z=new We,N=O=>{if(!s||w.length===0)return;const F=n.platno.getBoundingClientRect();if(F.width<=0||F.height<=0)return;z.x=(O.clientX-F.left)/F.width*2-1,z.y=-((O.clientY-F.top)/F.height)*2+1,R.setFromCamera(z,n.kamera);const G=R.intersectObjects(w.map(Z=>Z.mesh),!1);if(G.length>0){const Z=G[0].object,Y=w.findIndex(he=>he.mesh===Z);Y!==d&&(d=Y,x(Y),n.zatraziRender())}else d!==-1&&O.pointerType==="mouse"&&(d=-1,x(-1),n.zatraziRender())};return s&&n.platno.addEventListener("pointermove",N),n.api.ucitajStrukturuCif(e.mineral).then(O=>{o||(l=jm(O),A(l),n.zatraziRender())}).catch(O=>{if(o)return;const F=O instanceof ml&&O.status===404?ct("strukturaNedostupna"):ct("strukturaNedostupna");n.prikaziRezervu(F)}),{resetuj(){d=-1,x(-1)},osveziTemu(O){_.color.set(O.token("--text-secondary")),p.color.set(O.token("--text-muted")),u.color.set(O.token("--accent"));for(const F of g.children){const G=F;G.material instanceof mt&&G.material.color.set(O.token("--text-secondary"))}for(const F of m.children){const G=F;G.material instanceof pt&&G.material.color.set(O.token("--text-muted"))}},posleRendera(){if(!b||d<0){y.hidden=!0;return}const O=w[d];if(!O)return;O.mesh.updateMatrixWorld(!0);const F=O.mesh.position.clone().applyMatrix4(h.matrixWorld),G=n.projektujU2D(F);if(!G.vidljivo){y.hidden=!0;return}y.hidden=!1,y.style.transform=`translate(-50%, -130%) translate(${G.x.toFixed(1)}px, ${G.y.toFixed(1)}px)`},raspolazi(){o=!0,s&&n.platno.removeEventListener("pointermove",N),Lt(h),_.dispose(),p.dispose(),u.dispose()}}}},zs=[{kljuc:"kubni",naziv:"Кубни",kratko:"Кубни",odnosIvica:"a = b = c",odnosUglova:"α = β = γ = 90°",reprezentativniOblik:"коцка",celija:{a:1.15,b:1.15,c:1.15,alpha:90,beta:90,gamma:90}},{kljuc:"tetragonalni",naziv:"Тетрагонални",kratko:"Тетраг.",odnosIvica:"a = b ≠ c",odnosUglova:"α = β = γ = 90°",reprezentativniOblik:"тетрагонална призма",celija:{a:1,b:1,c:1.62,alpha:90,beta:90,gamma:90}},{kljuc:"ortorombicni",naziv:"Орторомбични",kratko:"Орторомб.",odnosIvica:"a ≠ b ≠ c",odnosUglova:"α = β = γ = 90°",reprezentativniOblik:"правоугаона призма („цигла“)",celija:{a:.85,b:1.22,c:1.58,alpha:90,beta:90,gamma:90}},{kljuc:"heksagonalni",naziv:"Хексагонални",kratko:"Хексаг.",odnosIvica:"a = b ≠ c",odnosUglova:"α = β = 90°, γ = 120°",reprezentativniOblik:"хексагонална призма",celija:{a:1.08,b:1.08,c:1.55,alpha:90,beta:90,gamma:120}},{kljuc:"trigonalni",naziv:"Тригонални",kratko:"Тригон.",odnosIvica:"a = b = c (ромбоедарска) / a = b ≠ c (хексагонална)",odnosUglova:"α = β = γ ≠ 90° (ромб.) / α = β = 90°, γ = 120° (хекс.)",reprezentativniOblik:"ромбоедар (у кристалографији се стандардно описује и хексагоналном поставком)",celija:{a:1.18,b:1.18,c:1.18,alpha:75,beta:75,gamma:75}},{kljuc:"monoklinicni",naziv:"Моноклинични",kratko:"Монокл.",odnosIvica:"a ≠ b ≠ c",odnosUglova:"α = γ = 90°, β ≠ 90°",reprezentativniOblik:"кос паралелопипед (β ≠ 90°)",celija:{a:.92,b:1.22,c:1.48,alpha:90,beta:112,gamma:90}},{kljuc:"triklinicni",naziv:"Триклинични",kratko:"Трикл.",odnosIvica:"a ≠ b ≠ c",odnosUglova:"α ≠ β ≠ γ ≠ 90°",reprezentativniOblik:"кос паралелопипед (α, β, γ ≠ 90°)",celija:{a:.88,b:1.18,c:1.46,alpha:78,beta:109,gamma:103}}],t0={a:1.15,b:1.15,c:1.15,alpha:90,beta:90,gamma:90};function n0(n,e,t){const i=Math.max(0,Math.min(1,t));return{a:n.a+(e.a-n.a)*i,b:n.b+(e.b-n.b)*i,c:n.c+(e.c-n.c)*i,alpha:n.alpha+(e.alpha-n.alpha)*i,beta:n.beta+(e.beta-n.beta)*i,gamma:n.gamma+(e.gamma-n.gamma)*i}}function al(n){const e=Ya(n),t=new k(...e.va),i=new k(...e.vb),r=new k(...e.vc),s=t.clone().add(i).add(r).multiplyScalar(.5),a=[],o=[[0,0,0],[1,0,0],[1,1,0],[0,1,0],[0,0,1],[1,0,1],[1,1,1],[0,1,1]];for(const[g,_,p]of o){const u=wn(g,_,p,e);a.push(new k(u[0]-s.x,u[1]-s.y,u[2]-s.z))}const c=[[0,1],[1,2],[2,3],[3,0],[4,5],[5,6],[6,7],[7,4],[0,4],[1,5],[2,6],[3,7]],l=[];for(const[g,_]of c){const p=a[g],u=a[_];l.push(p.x,p.y,p.z,u.x,u.y,u.z)}const d=new Ke;d.setAttribute("position",new je(l,3));const h=[[0,3,2,1],[4,5,6,7],[0,1,5,4],[2,3,7,6],[1,2,6,5],[3,0,4,7]],f=[];for(const[g,_,p,u]of h){const E=a[g],y=a[_],M=a[p],D=a[u];f.push(E.x,E.y,E.z,y.x,y.y,y.z,M.x,M.y,M.z,E.x,E.y,E.z,M.x,M.y,M.z,D.x,D.y,D.z)}const m=new Ke;return m.setAttribute("position",new je(f,3)),m.computeVertexNormals(),{ivice:d,mreza:m,poreklo:a[0],va:t,vb:i,vc:r}}function Ns(n,e,t,i){const r=e.clone().normalize(),s=t.clone().normalize(),a=18,o=[];let c=n.clone();for(let d=0;d<=a;d++){const h=d/a,f=r.clone().multiplyScalar(1-h).addScaledVector(s,h).normalize(),m=n.clone().addScaledVector(f,i);if(d===Math.floor(a/2)&&(c=n.clone().addScaledVector(f,i*1.38)),d>0){const g=(d-1)/a,_=r.clone().multiplyScalar(1-g).addScaledVector(s,g).normalize(),p=n.clone().addScaledVector(_,i);o.push(p.x,p.y,p.z,m.x,m.y,m.z)}}const l=new Ke;return l.setAttribute("position",new je(o,3)),{geometrija:l,sredina:c}}function i0(n,e,t){if(n==="heksagonalni"){const a=.58+.22*t,o=1.35-(1.35-.68)*t,c=[{normala:[0,1,0],d:a},{normala:[0,-1,0],d:a},{normala:[1,0,0],d:.68},{normala:[-1,0,0],d:.68},{normala:[0,0,1],d:.68+.14*t},{normala:[0,0,-1],d:.68+.14*t},{normala:[.5,0,Math.sqrt(3)/2],d:o},{normala:[-.5,0,Math.sqrt(3)/2],d:o},{normala:[.5,0,-Math.sqrt(3)/2],d:o},{normala:[-.5,0,-Math.sqrt(3)/2],d:o}],l=[{normala:[0,1,0],d:a},{normala:[0,-1,0],d:a}];if(t>.85){for(let g=0;g<6;g++){const _=g*Math.PI/3;l.push({normala:[Math.cos(_),0,Math.sin(_)],d:.68})}const f=Qi(l),m=er(f);return{mreza:m.geometrijaMreze,ivice:m.geometrijaIvica}}const d=Qi(c),h=er(d);return{mreza:h.geometrijaMreze,ivice:h.geometrijaIvica}}const i={a:e.a*.92,b:e.b*.92,c:e.c*.92,alpha:e.alpha,beta:e.beta,gamma:e.gamma},r=al(i);return{mreza:r.mreza,ivice:r.ivice}}const r0={izgled:"kristal",imaPodrazumevanuAnimaciju(n){return(n.animacija??"rotacija")!=="nema"},pocetnaKamera(){return{theta:.42,phi:1.15,udaljenost:6.8}},kreiraj(n,e){const t=e.animacija??"rotacija",i=e.prikazi_ose??!0,r=e.prikazi_celiju??!0;let s=e.sistem==="svi"?"heksagonalni":e.sistem;e.sistem==="svi"&&(s="kubni");let a=n.smanjenPokret||t!=="uporedi"?1:0,o=0;const c=new nt,l=new nt,d=new nt;r?(l.position.set(-1.55,-.05,0),d.position.set(1.55,-.05,0)):d.position.set(0,-.05,0),c.add(l,d),n.scena3D.add(c),n.dodajKontaktnuSenku(1.3,-1.02,c,d.position.x);const h=new pt({color:new oe(n.tema.token("--primary")),transparent:!0,opacity:.14,roughness:.45,metalness:.05,side:Tt,depthWrite:!1}),f=new mt({color:new oe(n.tema.token("--text-secondary"))}),m=new mt({color:new oe(n.tema.token("--danger"))}),g=new mt({color:new oe(n.tema.token("--success"))}),_=new mt({color:new oe(n.tema.token("--accent"))}),p=new mt({color:new oe(n.tema.token("--warning"))}),u=ti(n.tema.token("--primary"),{providnost:.55}),E=tr(n.tema.token("--text-primary"),n.tema.token("--primary")),y=["a","b","c","α","β","γ"],M=new Map,D=new Map;if(i&&r)for(const R of y){const z=document.createElement("span");z.className="udzbenik-scena-etiketa",z.textContent=R,n.slojEtiketa.append(z),M.set(R,z),D.set(R,new k)}const w=document.createElement("div");w.className="udzbenik-scena-info-red",n.podnozje.append(w);const b=new Map;if(e.sistem==="svi"){const R=document.createElement("div");R.className="udzbenik-sistemi-traka",R.setAttribute("role","group"),R.setAttribute("aria-label",ct("izaberiKristalniSistem"));for(const z of zs){const N=document.createElement("button");N.type="button",N.className="udzbenik-sistem-kartica",N.dataset.sistem=z.kljuc,N.setAttribute("aria-pressed",String(z.kljuc===s));const O=document.createElement("span");O.className="udzbenik-sistem-kartica-naslov",O.textContent=z.naziv;const F=document.createElement("span");F.className="udzbenik-sistem-kartica-meta",F.textContent=`${z.odnosIvica} · ${z.odnosUglova}`,N.append(O,F),N.addEventListener("click",()=>{s=z.kljuc,a=n.smanjenPokret||t!=="uporedi"?1:0,C(),U(),n.zatraziRender()}),b.set(z.kljuc,N),R.append(N)}n.gornjeKontrole.append(R)}function C(){for(const[R,z]of b.entries()){const N=R===s;z.classList.toggle("udzbenik-sistem-kartica--aktivna",N),z.setAttribute("aria-pressed",String(N))}}function v(){return zs.find(R=>R.kljuc===s)??zs[0]}function x(R){for(const z of R.children){const N=z.geometry;N&&N.dispose()}R.clear()}function P(){if(t!=="uporedi"||s==="kubni"||a>=1)return 1;const R=a%1;if(R<.4){const z=R/.4;return z*z*(3-2*z)}if(R<.72)return 1;if(R<.92){const z=(R-.72)/.2;return 1-z*z*(3-2*z)}return 0}function U(){const R=v(),z=P(),N=n0(t0,R.celija,z);if(x(l),x(d),r){const Y=al(N),he=new Le(Y.mreza,h),Ie=new dt(Y.ivice,f);if(l.add(he,Ie),i){const X=Y.poreklo,ee=X.clone().addScaledVector(Y.va,1.16),ue=X.clone().addScaledVector(Y.vb,1.16),re=X.clone().addScaledVector(Y.vc,1.16),le=new Ke().setFromPoints([X,ee]),Pe=new Ke().setFromPoints([X,ue]),me=new Ke().setFromPoints([X,re]);l.add(new $i(le,m),new $i(Pe,g),new $i(me,_));const te=Ns(X,Y.vb,Y.vc,.36),se=Ns(X,Y.va,Y.vc,.44),K=Ns(X,Y.va,Y.vb,.36);l.add(new dt(te.geometrija,p),new dt(se.geometrija,p),new dt(K.geometrija,p)),D.get("a")?.copy(ee),D.get("b")?.copy(ue),D.get("c")?.copy(re),D.get("α")?.copy(te.sredina),D.get("β")?.copy(se.sredina),D.get("γ")?.copy(K.sredina)}}const O=i0(R.kljuc,N,z);d.add(new Le(O.mreza,u),new dt(O.ivice,E)),w.replaceChildren();const F=document.createElement("strong");F.textContent=`${R.naziv}: `;const G=document.createElement("span"),Z=R.kljuc==="trigonalni"?" • Стандардна кристалографска поставка за тригоналне минерале (кварц, калцит) је хексагонална (a = b ≠ c, γ = 120°).":"";G.textContent=`${R.odnosIvica} · ${R.odnosUglova} — облик: ${R.reprezentativniOblik}${Z}`,w.append(F,G)}function A(){if(!i||!r)return;l.updateMatrixWorld(!0);const R=v();for(const[z,N]of M.entries()){const O=D.get(z);if(!O)continue;const F=O.clone().applyMatrix4(l.matrixWorld),G=n.projektujU2D(F);if(!G.vidljivo){N.hidden=!0;continue}N.hidden=!1,N.style.transform=`translate(-50%, -50%) translate(${G.x.toFixed(1)}px, ${G.y.toFixed(1)}px)`;const Z=z==="c"&&R.celija.c!==R.celija.a||z==="b"&&R.celija.b!==R.celija.a||z==="α"&&R.celija.alpha!==90||z==="β"&&R.celija.beta!==90||z==="γ"&&R.celija.gamma!==90;N.classList.toggle("udzbenik-scena-etiketa--istaknuta",Z)}}return C(),U(),{azuriraj(R){t==="uporedi"?(a=(a+R*.18)%1,n.korisnikUpravlja()||(o+=R*.22,c.rotation.y=Math.sin(o)*.18),U()):t==="rotacija"&&!n.korisnikUpravlja()&&(c.rotation.y+=R*.45)},korak(){t==="uporedi"?(a=(a+.15)%1,o+=.45,c.rotation.y=Math.sin(o)*.18,U()):c.rotation.y+=.35},resetuj(){c.rotation.set(0,0,0),o=0,a=n.smanjenPokret||t!=="uporedi"?1:0,U()},osveziTemu(R){h.color.set(R.token("--primary")),f.color.set(R.token("--text-secondary")),m.color.set(R.token("--danger")),g.color.set(R.token("--success")),_.color.set(R.token("--accent")),p.color.set(R.token("--warning")),u.color.set(R.token("--primary")),E.color.copy(zi(R.token("--text-primary"),R.token("--primary")))},posleRendera(){A()},raspolazi(){Lt(c),h.dispose(),f.dispose(),m.dispose(),g.dispose(),_.dispose(),p.dispose(),u.dispose(),E.dispose()}}}},Yt="Klein, C. & Dutrow, B. (2007), Manual of Mineral Science (23rd ed.), John Wiley & Sons, Table 2.3 (Knoop microhardness HK, kgf/mm²; теренске пробе: нокат ~2,5, бакарни новчић ~3, нож/стакло ~5,5, турпија ~6,5).",yn=[{mohs:1,kljuc:"talk",naziv:"Талк",formula:"Mg₃Si₄O₁₀(OH)₂",apsolutnaKnoop:1,izvor:Yt},{mohs:2,kljuc:"gips",naziv:"Гипс",formula:"CaSO₄·2H₂O",apsolutnaKnoop:32,izvor:Yt},{mohs:3,kljuc:"kalcit",naziv:"Калцит",formula:"CaCO₃",apsolutnaKnoop:135,izvor:Yt},{mohs:4,kljuc:"fluorit",naziv:"Флуорит",formula:"CaF₂",apsolutnaKnoop:163,izvor:Yt},{mohs:5,kljuc:"apatit",naziv:"Апатит",formula:"Ca₅(PO₄)₃(F,Cl,OH)",apsolutnaKnoop:430,izvor:Yt},{mohs:6,kljuc:"ortoklas",naziv:"Ортоклас",formula:"KAlSi₃O₈",apsolutnaKnoop:560,izvor:Yt},{mohs:7,kljuc:"kvarc",naziv:"Кварц",formula:"SiO₂",apsolutnaKnoop:820,izvor:Yt},{mohs:8,kljuc:"topaz",naziv:"Топаз",formula:"Al₂SiO₄(F,OH)₂",apsolutnaKnoop:1340,izvor:Yt},{mohs:9,kljuc:"korund",naziv:"Корунд",formula:"Al₂O₃",apsolutnaKnoop:2100,izvor:Yt},{mohs:10,kljuc:"dijamant",naziv:"Дијамант",formula:"C",apsolutnaKnoop:7e3,izvor:Yt}],s0=[{naziv:"Нокат (~2,5)",mohs:2.5},{naziv:"Бакарни новчић (~3)",mohs:3},{naziv:"Нож / стакло (~5,5)",mohs:5.5},{naziv:"Челична турпија (~6,5)",mohs:6.5}];function bc(n,e){if(!e||e.length===0)return!1;const t=n.kljuc.toLowerCase(),i=n.naziv.toLowerCase();return e.some(r=>{const s=r.trim().toLowerCase();return s===t||s===i})}const a0={imaPodrazumevanuAnimaciju(){return!0},pocetnaKamera(){return{theta:.16,phi:1.18,udaljenost:8.6}},kreiraj(n,e){const t=e.prikazi_apsolutnu??!1,i=e.prikazi_terenske_probe??!0,r=e.istaknuti??[];let s=!1,a=0,o=6,c=5,l=n.smanjenPokret?.65:0;const d=new nt;d.position.set(0,-.35,0),n.scena3D.add(d);const h=-4.05,f=.9,m=-.7,g=2.75,_=new pt({color:new oe(n.tema.token("--bg-elevated")),roughness:.7,metalness:.05}),p=new Le(new Jt(9.6,.14,1.4),_);p.position.set(0,m-.07,-.35),d.add(p);const u=[],E=new mt({color:new oe(n.tema.token("--text-primary"))}),y=new Jt(.66,1,.66),M=new Ji(y);for(let te=0;te<yn.length;te++){const se=yn[te],K=bc(se,r),I=new oe(n.tema.token(K?"--accent":"--primary")),Ce=new pt({color:I,emissive:K?new oe(n.tema.token("--accent")).multiplyScalar(.22):new oe(0,0,0),roughness:.35,metalness:.12}),Se=new Le(y,Ce),_e=new dt(M,E),ve=h+te*f;Se.position.set(ve,m+.5,-.35),_e.position.copy(Se.position),d.add(Se,_e);const Ne=document.createElement("span");Ne.className="udzbenik-scena-etiketa udzbenik-scena-etiketa--mala",K&&Ne.classList.add("udzbenik-scena-etiketa--istaknuta"),Ne.textContent=`${se.mohs}`,n.slojEtiketa.append(Ne),u.push({mineral:se,istaknut:K,mesh:Se,ivice:_e,mat:Ce,etiketaDom:Ne})}const D=new pt({color:new oe(n.tema.token("--warning")),roughness:.4}),w=[];if(i){const te=new sr(.035,.035,.65,8);for(const se of s0){const K=h+(se.mohs-1)*f,I=new Le(te,D);I.position.set(K,m+.32,.18),d.add(I);const Ce=document.createElement("span");Ce.className="udzbenik-scena-etiketa udzbenik-scena-etiketa--proba",Ce.textContent=se.naziv,n.slojEtiketa.append(Ce),w.push({x:K,tekst:se.naziv,dom:Ce,stub:I})}}const b=new nt;b.position.set(0,m-.52,1.35),d.add(b);const C=new pt({color:new oe(n.tema.token("--primary-light")),roughness:.45,metalness:.08}),v=new Le(new Jt(3.4,.24,.92),C),x=new dt(new Ji(v.geometry),E);b.add(v,x);const P=new pt({color:new oe(n.tema.token("--danger")),roughness:.85}),U=new Le(new Jt(1,.05,.11),P);U.position.set(-1.1,.125,0),U.visible=!1,b.add(U);const A=new pt({color:new oe(n.tema.token("--accent")),roughness:.25,metalness:.2}),R=new Le(new Ga(.22,.72,6),A);R.rotation.x=Math.PI,R.rotation.z=-.22,R.position.set(-1.1,.5,0),b.add(R);const z=document.createElement("div");z.className="udzbenik-mohs-kontrole";const N=document.createElement("div");N.className="udzbenik-mohs-dugmad",N.setAttribute("role","group"),N.setAttribute("aria-label",ct("ordinalnaTvrdocaOznaka"));const O=[];for(let te=0;te<yn.length;te++){const se=yn[te],K=document.createElement("button");K.type="button",K.className="udzbenik-mohs-cip",bc(se,r)&&K.classList.add("udzbenik-mohs-cip--istaknut"),K.textContent=`${se.mohs}. ${se.naziv}`,K.addEventListener("click",()=>{Ie(te)}),O.push(K),N.append(K)}z.append(N);const F=document.createElement("div");F.className="udzbenik-mohs-akcije";const G=document.createElement("button");G.type="button",G.className="udzbenik-dugme udzbenik-dugme--malo",G.textContent=ct("zameniMinerale"),G.addEventListener("click",()=>{const te=o;o=c,c=te,l=n.smanjenPokret?.75:0,re(),n.zatraziRender()}),F.append(G);let Z=null;t&&(Z=document.createElement("button"),Z.type="button",Z.className="udzbenik-dugme udzbenik-dugme--malo udzbenik-dugme--preklopnik",Z.setAttribute("role","switch"),Z.setAttribute("aria-checked","false"),Z.textContent=ct("apsolutnaTvrdocaPreklopnik"),Z.addEventListener("click",()=>{s=!s,Z?.setAttribute("aria-checked",String(s)),Z?.classList.toggle("udzbenik-dugme--aktivno",s),n.smanjenPokret&&(a=s?1:0,ee()),re(),n.zatraziRender()}),F.append(Z)),z.append(F),n.gornjeKontrole.append(z);const Y=document.createElement("p");Y.className="udzbenik-scena-info-red",Y.setAttribute("aria-live","polite");const he=document.createElement("p");he.className="udzbenik-scena-izvor",he.textContent=`${ct("izvorPodataka")}: ${Yt}`,n.podnozje.append(Y,he);function Ie(te){te===o?c=te<9?te+1:te-1:(o=te,c=te>0?te-1:1),l=n.smanjenPokret?.75:0,re(),n.zatraziRender()}function X(te,se){const K=te.mohs/10*g,I=Math.max(.08,te.apsolutnaKnoop/7e3*g);return K+(I-K)*se}function ee(){for(let te=0;te<u.length;te++){const se=u[te],K=X(se.mineral,a);se.mesh.scale.y=K,se.mesh.position.y=m+K*.5,se.ivice.scale.y=K,se.ivice.position.copy(se.mesh.position);const I=te===o,Ce=te===c,Se=I?"--accent":Ce?"--warning":se.istaknut?"--accent":"--primary",_e=new oe(n.tema.token(Se));!I&&!Ce&&!se.istaknut&&_e.lerp(new oe(n.tema.token("--bg-elevated")),.25),se.mat.color.copy(_e),se.etiketaDom.textContent=s?`${se.mineral.mohs} (${se.mineral.apsolutnaKnoop})`:`${se.mineral.mohs}`}}function ue(){const te=yn[o],se=yn[c],K=te.mohs>se.mohs,I=Math.min(1,l/.75),Ce=-1.15,_e=Ce+(1.15-Ce)*I;if(R.position.x=_e,R.position.y=K?.44:.5,K&&I>.03){const ve=Math.max(.05,_e-Ce);U.visible=!0,U.scale.x=ve,U.position.x=Ce+ve*.5}else U.visible=!1}function re(){for(let Ce=0;Ce<O.length;Ce++){const Se=O[Ce],_e=Ce===o;Se.classList.toggle("udzbenik-mohs-cip--aktivan",_e),Se.setAttribute("aria-pressed",String(_e))}const te=yn[o],se=yn[c],I=te.mohs>se.mohs?`${ct("probaGrebanja")}: ${te.naziv} (${te.mohs}, HK ${te.apsolutnaKnoop}) је тврђи и оставља бразду на минералу ${se.naziv} (${se.mohs}, HK ${se.apsolutnaKnoop}).`:`${ct("probaGrebanja")}: ${te.naziv} (${te.mohs}, HK ${te.apsolutnaKnoop}) је мекши и НЕ оставља бразду на минералу ${se.naziv} (${se.mohs}, HK ${se.apsolutnaKnoop}).`;Y.textContent=I,ee(),ue()}const le=new Xa,Pe=new We,me=te=>{const se=n.platno.getBoundingClientRect();if(se.width<=0||se.height<=0)return;Pe.x=(te.clientX-se.left)/se.width*2-1,Pe.y=-((te.clientY-se.top)/se.height)*2+1,le.setFromCamera(Pe,n.kamera);const K=le.intersectObjects(u.map(I=>I.mesh),!1);if(K.length>0){const I=K[0].object,Ce=u.findIndex(Se=>Se.mesh===I);Ce!==-1&&Ie(Ce)}};return n.platno.addEventListener("click",me),re(),{azuriraj(te){const se=s?1:0;Math.abs(a-se)>.002?(a+=(se-a)*Math.min(1,te*6),ee()):a!==se&&(a=se,ee()),l=(l+te*.42)%1,ue()},korak(){l=(l+.2)%1,a=s?1:0,ee(),ue()},resetuj(){s=!1,a=0,Z&&(Z.setAttribute("aria-checked","false"),Z.classList.remove("udzbenik-dugme--aktivno")),o=6,c=5,l=n.smanjenPokret?.75:0,re()},osveziTemu(te){_.color.set(te.token("--bg-elevated")),E.color.set(te.token("--text-primary")),D.color.set(te.token("--warning")),C.color.set(te.token("--primary-light")),P.color.set(te.token("--danger")),A.color.set(te.token("--accent")),ee()},posleRendera(){d.updateMatrixWorld(!0);for(const te of u){const se=te.mesh.position.clone().add(new k(0,te.mesh.scale.y*.5+.22,0)).applyMatrix4(d.matrixWorld),K=n.projektujU2D(se);te.etiketaDom.hidden=!K.vidljivo,K.vidljivo&&(te.etiketaDom.style.transform=`translate(-50%, -50%) translate(${K.x.toFixed(1)}px, ${K.y.toFixed(1)}px)`)}for(const te of w){const se=new k(te.x,m-.22,.35).applyMatrix4(d.matrixWorld),K=n.projektujU2D(se);te.dom.hidden=!K.vidljivo,K.vidljivo&&(te.dom.style.transform=`translate(-50%, 0%) translate(${K.x.toFixed(1)}px, ${K.y.toFixed(1)}px)`)}},raspolazi(){n.platno.removeEventListener("click",me),Lt(d),y.dispose(),M.dispose(),_.dispose(),E.dispose(),D.dispose(),C.dispose(),P.dispose(),A.dispose();for(const te of u)te.mat.dispose()}}}};function o0(n,e,t){const i=1/(n*n),r=1/(e*e),s=1/(t*t),a=(i-r)/Math.max(1e-12,r-s),c=2*Math.atan(Math.sqrt(Math.max(0,a)))*180/Math.PI;return c<=90?{dvaV:c,dvaVZ:c,znak:"+",bisektrisaOstra:"Z (γ)"}:{dvaV:180-c,dvaVZ:c,znak:"-",bisektrisaOstra:"X (α)"}}function Tc(n,e,t){const i=Math.hypot(...t),r=i>0?t[0]/i:0,s=i>0?t[1]/i:0,a=i>0?t[2]/i:1;if(n==="izotropna"){const A=e[0]??1.5;return{n1:A,n2:A,delta:0}}if(n==="jednoosna"){const A=e[0]??1.544,R=e[1]??1.553,z=a*a,N=Math.max(0,1-z),O=z/(A*A)+N/(R*R),F=Math.sqrt(1/Math.max(1e-12,O)),G=Math.abs(F-A);return{n1:Math.min(A,F),n2:Math.max(A,F),delta:G}}const o=e[0]??1.52,c=e[1]??1.53,l=e[2]??1.55,d=1/(o*o),h=1/(c*c),f=1/(l*l);let m,g,_,p;if(Math.abs(h-f)>1e-7&&d>=h&&h>=f){const A=o0(o,c,l);m=A.dvaV,g=A.dvaVZ,_=A.znak,p=A.bisektrisaOstra}const u=r*r,E=s*s,y=a*a,M=1,D=-(u*(h+f)+E*(d+f)+y*(d+h)),w=u*h*f+E*d*f+y*d*h,b=Math.max(0,D*D-4*M*w),C=(-D-Math.sqrt(b))/(2*M),v=(-D+Math.sqrt(b))/(2*M),x=Math.sqrt(1/Math.max(1e-12,v)),P=Math.sqrt(1/Math.max(1e-12,C)),U=Math.abs(P-x);return{n1:x,n2:P,delta:U,ugao2V:m,ugao2VZ:g,optickiZnak:_,bisektrisaOstra:p}}const c0={imaPodrazumevanuAnimaciju(){return!0},pocetnaKamera(){return{theta:.72,phi:1.18,udaljenost:5.6}},kreiraj(n,e){const t=new nt;n.scena3D.add(t);const i=e.tip,r=e.n&&e.n.length>0?e.n:i==="izotropna"?[1.5]:i==="jednoosna"?[1.658,1.486]:[1.52,1.53,1.55];let s=1.6,a=1.6,o=1.6;if(i==="jednoosna"){const U=r[0],A=r[1]??r[0];s=1.6,a=1.6,o=1.6*(A>=U?1.35:.72)}else i==="dvoosna"&&(s=1.25,a=1.65,o=2.15);const c=new mn(1,48,36);c.scale(s,a,o);const l=new pt({color:new oe(n.tema.token("--primary")),transparent:!0,opacity:.42,roughness:.25,metalness:.1,side:Tt}),d=new Le(c,l);t.add(d);const h=new mt({color:new oe(n.tema.token("--text-secondary"))}),f=new Ke,m=[-s*1.3,0,0,s*1.3,0,0,0,-a*1.3,0,0,a*1.3,0,0,0,-o*1.3,0,0,o*1.3];f.setAttribute("position",new je(m,3)),t.add(new dt(f,h));const g=new mt({color:new oe(n.tema.token("--accent")),linewidth:3});if(e.prikazi_opticke_ose!==!1){const U=[];if(i==="jednoosna")U.push(0,0,-o*1.45,0,0,o*1.45);else if(i==="dvoosna"){const R=(Tc(i,r,[0,0,1]).ugao2V??50)/2*(Math.PI/180),z=o*1.4,N=z*Math.sin(R),O=z*Math.cos(R);U.push(-N,0,-O,N,0,O),U.push(N,0,-O,-N,0,O)}if(U.length>0){const A=new Ke;A.setAttribute("position",new je(U,3)),t.add(new dt(A,g))}}const _=new nt;t.add(_);const p=new Ln({color:new oe(n.tema.token("--warning")),transparent:!0,opacity:.35,side:Tt}),u=new ja(0,2.2,48),E=new Le(u,p);_.add(E);const y=new mt({color:new oe(n.tema.token("--danger"))}),M=new Ke;M.setAttribute("position",new je([0,0,-2.6,0,0,2.6],3)),_.add(new dt(M,y));const D=document.createElement("div");D.className="udzbenik-scena-status",n.podnozje.append(D);const w=document.createElement("small");w.className="udzbenik-scena-napomena",w.style.display="block",w.textContent="Напомена: Разлике индекса преламања су преувеличане ради јаснијег 3D приказа.",n.podnozje.append(w);let b=.5,C=.3;function v(){_.rotation.set(b,C,0);const U=new k(0,0,1).applyEuler(_.rotation),A=Tc(i,r,[U.x,U.y,U.z]),R=A.delta.toFixed(4),z=e.mineral?` (${e.mineral})`:"",N=A.ugao2V!==void 0?` • 2V = ${A.ugao2V.toFixed(1)}° (${A.optickiZnak}, Bxa = ${A.bisektrisaOstra})`:"";D.textContent=`Тип: ${i}${z} • n'₁ = ${A.n1.toFixed(3)}, n'₂ = ${A.n2.toFixed(3)} • δ = ${R}${N}`}v();function x(){l.color.set(n.tema.token("--primary")),h.color.set(n.tema.token("--text-secondary")),g.color.set(n.tema.token("--accent")),p.color.set(n.tema.token("--warning")),y.color.set(n.tema.token("--danger"))}let P=0;return{azuriraj(U){P+=U*.35,C=Math.sin(P)*1.1,b=Math.cos(P*.7)*.7,v()},korak(){P+=.25,C+=.2,v()},resetuj(){P=0,b=.5,C=.3,v()},osveziTemu(){x()},raspolazi(){c.dispose(),l.dispose(),f.dispose(),h.dispose(),g.dispose(),u.dispose(),p.dispose(),M.dispose(),y.dispose(),Lt(t),D.remove(),w.remove()}}}},Fs={nezo:{klasa:"nezo",naziv:"Незосиликати (изоловани tetraedri)",odnosSiO:"1 : 4 (SiO₄⁴⁻)",zajednickiKiseonici:"0",primeri:"оливин, гранат, циркон"},soro:{klasa:"soro",naziv:"Соросиликати (парови tetraedara)",odnosSiO:"2 : 7 (Si₂O₇⁶⁻)",zajednickiKiseonici:"1",primeri:"епидот, хемиморфит"},"ciklo-3":{klasa:"ciklo-3",naziv:"Циклосиликати (трочлани прстен)",odnosSiO:"1 : 3 (Si₃O₉⁶⁻)",zajednickiKiseonici:"2",primeri:"бенитоит"},"ciklo-6":{klasa:"ciklo-6",naziv:"Циклосиликати (шесточлани прстен)",odnosSiO:"1 : 3 (Si₆O₁₈¹²⁻)",zajednickiKiseonici:"2",primeri:"берил, турмалин"},"ino-jednostruki":{klasa:"ino-jednostruki",naziv:"Иносиликати (једноструки ланци)",odnosSiO:"1 : 3 (Si₂O₆⁴⁻)",zajednickiKiseonici:"2",primeri:"пироксени (диопсид, енстатит)"},"ino-dvostruki":{klasa:"ino-dvostruki",naziv:"Иносиликати (двоструки ланци)",odnosSiO:"4 : 11 (Si₄O₁₁⁶⁻)",zajednickiKiseonici:"2 и 3 (просек 2,5)",primeri:"амфиболи (тремолит, хорнбленда)"},filo:{klasa:"filo",naziv:"Филосиликати (слојевити)",odnosSiO:"2 : 5 (Si₄O₁₀⁴⁻)",zajednickiKiseonici:"3",primeri:"лискуни (мусковит, биотит), талк, каолинит"},tekto:{klasa:"tekto",naziv:"Тектосиликати (просторна мрежа)",odnosSiO:"1 : 2 (SiO₂)",zajednickiKiseonici:"4",primeri:"кварц, фелдспати, зеолити"},sve:{klasa:"sve",naziv:"Преглед свих класа",odnosSiO:"од 1:4 до 1:2",zajednickiKiseonici:"0 до 4",primeri:"полимеризација од незо- до тектосиликата"}};function l0(){const e=.65*Math.SQRT2,t=[0,0,0],i=[-e,.65,0],r=[-e,-.5*.65,Math.sqrt(3)/2*.65],s=[-e,-.5*.65,-(Math.sqrt(3)/2)*.65],a=[e,-.65,0],o=[e,.5*.65,-(Math.sqrt(3)/2)*.65],c=[e,.5*.65,Math.sqrt(3)/2*.65];return{vrhoviLevi:[t,i,r,s],vrhoviDesni:[t,a,o,c],svih7Kiseonika:[t,i,r,s,a,o,c]}}function bn(n,e,t,i,r,s){const a=new nt;a.position.copy(n),a.rotation.copy(e);const o=.55,c=[[o,o,o],[o,-o,-o],[-o,o,-o],[-o,-o,o]];if(s==="tetraedri"||s==="oba"){const l=new Ke,d=[...c[0],...c[1],...c[2],...c[0],...c[3],...c[1],...c[0],...c[2],...c[3],...c[1],...c[3],...c[2]];l.setAttribute("position",new je(d,3)),l.computeVertexNormals();const h=new Le(l,t);a.add(h)}if(s==="kugle"||s==="oba")for(const l of c){const d=new Le(r,i);d.position.set(l[0],l[1],l[2]),a.add(d)}return a}const u0={imaPodrazumevanuAnimaciju(n){return(n.animacija??"rotacija")!=="nema"},pocetnaKamera(){return{theta:.65,phi:1.15,udaljenost:6.2}},kreiraj(n,e){let t=e.klasa==="sve"?"nezo":e.klasa;const i=e.prikaz??"tetraedri",r=new nt;n.scena3D.add(r);const s=new mn(.18,16,16),a=new pt({color:new oe(n.tema.token("--primary")),transparent:!0,opacity:.65,roughness:.25,metalness:.1,side:Tt}),o=new pt({color:new oe(n.tema.token("--accent")),roughness:.25,metalness:.2}),c=document.createElement("div");c.className="udzbenik-scena-status",n.podnozje.append(c);function l(_){for(;r.children.length>0;){const u=r.children[0];r.remove(u),Lt(u)}const p=Fs[_]??Fs.nezo;if(c.textContent=`${p.naziv} • Si:O = ${p.odnosSiO} • Заједнички O: ${p.zajednickiKiseonici} (${p.primeri})`,_==="nezo")r.add(bn(new k(0,0,0),new xt(0,0,0),a,o,s,i));else if(_==="soro"){const{vrhoviLevi:u,vrhoviDesni:E,svih7Kiseonika:y}=l0(),[M,D,w,b]=u,[,C,v,x]=E;if(i==="tetraedri"||i==="oba"){const P=new Ke,U=[...M,...D,...w,...M,...w,...b,...M,...b,...D,...D,...b,...w,...M,...v,...C,...M,...x,...v,...M,...C,...x,...C,...v,...x];P.setAttribute("position",new je(U,3)),P.computeVertexNormals(),r.add(new Le(P,a))}if(i==="kugle"||i==="oba")for(const P of y){const U=new Le(s,o);U.position.set(P[0],P[1],P[2]),r.add(U)}}else if(_==="ciklo-3")for(let u=0;u<3;u++){const E=u*2*Math.PI/3,y=new k(Math.cos(E)*.95,Math.sin(E)*.95,0);r.add(bn(y,new xt(0,0,E),a,o,s,i))}else if(_==="ciklo-6")for(let u=0;u<6;u++){const E=u*2*Math.PI/6,y=new k(Math.cos(E)*1.5,Math.sin(E)*1.5,0);r.add(bn(y,new xt(0,0,E),a,o,s,i))}else if(_==="ino-jednostruki")for(let u=-2;u<=2;u++){const E=u%2===0?0:Math.PI;r.add(bn(new k(u*.9,u%2*.2,0),new xt(0,0,E),a,o,s,i))}else if(_==="ino-dvostruki")for(let u=-2;u<=2;u++){const E=u%2===0?0:Math.PI;r.add(bn(new k(u*.9,.45+u%2*.15,0),new xt(0,0,E),a,o,s,i)),r.add(bn(new k(u*.9,-.45-u%2*.15,0),new xt(0,0,E+Math.PI),a,o,s,i))}else if(_==="filo")for(let u=-1;u<=1;u++)for(let E=-1;E<=1;E++){const y=u*1.4+E%2*.7,M=E*1.2;r.add(bn(new k(y,M,0),new xt(0,0,0),a,o,s,i))}else for(const u of[-.7,.7])for(const E of[-.7,.7])for(const y of[-.7,.7])r.add(bn(new k(u,E,y),new xt(u,E,y),a,o,s,i))}if(e.klasa==="sve"){const _=document.createElement("div");_.className="udzbenik-silikati-traka",_.style.display="flex",_.style.flexWrap="wrap",_.style.gap="4px";const p=["nezo","soro","ciklo-3","ciklo-6","ino-jednostruki","ino-dvostruki","filo","tekto"];for(const u of p){const E=Fs[u],y=document.createElement("button");y.type="button",y.className="udzbenik-dugme udzbenik-dugme--malo",u===t&&y.classList.add("udzbenik-dugme--aktivno"),y.textContent=u,y.setAttribute("aria-label",E.naziv),y.addEventListener("click",()=>{t=u,_.querySelectorAll("button").forEach(M=>M.classList.remove("udzbenik-dugme--aktivno")),y.classList.add("udzbenik-dugme--aktivno"),l(u)}),_.append(y)}n.gornjeKontrole.append(_)}l(t);let d=0;const h=(e.animacija??(e.klasa==="sve"?"polimerizacija":"rotacija"))==="polimerizacija",f=["nezo","soro","ciklo-6","ino-jednostruki","ino-dvostruki","filo","tekto"];let m=0;function g(){a.color.set(n.tema.token("--primary")),o.color.set(n.tema.token("--accent"))}return{azuriraj(_){if(d+=_,r.rotation.y=d*.35,h){const p=Math.floor(d/3)%f.length;if(p!==m){m=p;const u=f[m];l(u)}}},korak(){d+=.3,r.rotation.y+=.2,h&&(m=(m+1)%f.length,l(f[m]))},resetuj(){d=0,r.rotation.set(0,0,0),m=0,l(t)},osveziTemu(){g()},raspolazi(){s.dispose(),a.dispose(),o.dispose(),Lt(r),c.remove()}}}},d0={"kristalni-sistem":r0,"kristalna-struktura":e0,"mohsova-skala":a0,cepljivost:Km,habitus:Jm,"bravaisova-resetka":Wm,"opticka-indikatrisa":c0,blizanac:Gm,"koordinacioni-poliedar":Qm,"silikatna-struktura":u0};function p0(n,e,t){const i=d0[n.scena];return i?Vm(i,n.parametri,e,t):(e.prikaziRezervu("Сцена није подржана у овој верзији мотора."),()=>{})}export{p0 as pokreniScenuPoImenu,f0 as raspolaziDeljenimRendererom};
