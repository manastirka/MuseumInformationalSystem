/**
 * Cinematic Weather Particle System — Navbar Edition
 * Photorealistic effects contained within the top navigation bar.
 */
(function () {
    'use strict';

    function boot() {
        // Тема/приступачност: без декоративних ефеката у високом контрасту и
        // када корисник тражи мање покрета (prefers-reduced-motion).
        if (document.documentElement.getAttribute('data-theme') === 'contrast') {
            console.log('[Weather] Disabled: high-contrast theme');
            return;
        }
        if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
            console.log('[Weather] Disabled: prefers-reduced-motion');
            return;
        }
        if (typeof THREE === 'undefined') { console.warn('[Weather] THREE.js not loaded'); return; }

        var canvas = document.getElementById('weather-canvas');
        if (!canvas) { console.warn('[Weather] No canvas found'); return; }

        var condition = (canvas.dataset.weather || 'none').toLowerCase().trim();

        var navbar = canvas.closest('nav') || canvas.parentElement;
        var isMobile = window.innerWidth < 768;
        var W = navbar ? navbar.offsetWidth : (canvas.clientWidth || window.innerWidth);
        var H = navbar ? navbar.offsetHeight : (canvas.clientHeight || 64);

        if (W < 10 || H < 10) { setTimeout(boot, 200); return; }

        console.log('[Weather] Starting: ' + condition + ' (' + W + 'x' + H + ')');

        canvas.width = W;
        canvas.height = H;

        var renderer;
        try {
            renderer = new THREE.WebGLRenderer({ canvas: canvas, alpha: true, antialias: false, powerPreference: 'low-power' });
        } catch (e) { console.error('[Weather] WebGL failed:', e); return; }

        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        renderer.setSize(W, H, false);

        var camera = new THREE.OrthographicCamera(0, W, 0, H, -100, 100);
        var scene = new THREE.Scene();
        var clock = new THREE.Clock();

        function rand(a, b) { return Math.random() * (b - a) + a; }
        function clamp(v, min, max) { return Math.max(min, Math.min(max, v)); }
        function flowNoise(t, seed) {
            return (
                Math.sin(t * 0.37 + seed) * 0.55 +
                Math.sin(t * 0.91 + seed * 1.7) * 0.3 +
                Math.cos(t * 0.21 + seed * 2.3) * 0.15
            );
        }

        function softDot(size, r, g, b, a) {
            var c = document.createElement('canvas'); c.width = c.height = size;
            var ctx = c.getContext('2d');
            var grad = ctx.createRadialGradient(size/2, size/2, 0, size/2, size/2, size/2);
            grad.addColorStop(0,   'rgba(' + r + ',' + g + ',' + b + ',' + a + ')');
            grad.addColorStop(0.4, 'rgba(' + r + ',' + g + ',' + b + ',' + (a*0.6) + ')');
            grad.addColorStop(1,   'rgba(' + r + ',' + g + ',' + b + ',0)');
            ctx.fillStyle = grad; ctx.fillRect(0, 0, size, size);
            var tex = new THREE.CanvasTexture(c); tex.needsUpdate = true; return tex;
        }

        function bokehDot(size, r, g, b) {
            var c = document.createElement('canvas'); c.width = c.height = size;
            var ctx = c.getContext('2d'); var cx = size/2;
            var grad = ctx.createRadialGradient(cx, cx, size*0.3, cx, cx, cx);
            grad.addColorStop(0,    'rgba(' + r + ',' + g + ',' + b + ',0.05)');
            grad.addColorStop(0.6,  'rgba(' + r + ',' + g + ',' + b + ',0.02)');
            grad.addColorStop(0.82, 'rgba(' + r + ',' + g + ',' + b + ',0.2)');
            grad.addColorStop(0.94, 'rgba(' + r + ',' + g + ',' + b + ',0.08)');
            grad.addColorStop(1,    'rgba(' + r + ',' + g + ',' + b + ',0)');
            ctx.fillStyle = grad; ctx.beginPath(); ctx.arc(cx, cx, cx, 0, Math.PI*2); ctx.fill();
            var tex = new THREE.CanvasTexture(c); tex.needsUpdate = true; return tex;
        }

        function makeLinearTexture(w, h, stops, horizontal) {
            var c = document.createElement('canvas'); c.width = w; c.height = h;
            var ctx = c.getContext('2d');
            var grad = horizontal ? ctx.createLinearGradient(0, 0, w, 0) : ctx.createLinearGradient(0, 0, 0, h);
            for (var i = 0; i < stops.length; i++) grad.addColorStop(stops[i][0], stops[i][1]);
            ctx.fillStyle = grad;
            ctx.fillRect(0, 0, w, h);
            var tex = new THREE.CanvasTexture(c); tex.needsUpdate = true; return tex;
        }

        function cloudDot(size, tint, alpha) {
            var c = document.createElement('canvas'); c.width = c.height = size;
            var ctx = c.getContext('2d');
            var stops = [
                { x: 0.28, y: 0.6, r: 0.18, a: alpha * 0.45 },
                { x: 0.46, y: 0.42, r: 0.26, a: alpha * 0.8 },
                { x: 0.68, y: 0.5, r: 0.23, a: alpha * 0.65 }
            ];
            for (var i = 0; i < stops.length; i++) {
                var s = stops[i];
                var grad = ctx.createRadialGradient(size * s.x, size * s.y, 0, size * s.x, size * s.y, size * s.r);
                grad.addColorStop(0, 'rgba(' + tint[0] + ',' + tint[1] + ',' + tint[2] + ',' + s.a + ')');
                grad.addColorStop(0.7, 'rgba(' + tint[0] + ',' + tint[1] + ',' + tint[2] + ',' + (s.a * 0.35) + ')');
                grad.addColorStop(1, 'rgba(' + tint[0] + ',' + tint[1] + ',' + tint[2] + ',0)');
                ctx.fillStyle = grad;
                ctx.fillRect(0, 0, size, size);
            }
            var tex = new THREE.CanvasTexture(c); tex.needsUpdate = true; return tex;
        }

        function addAtmosphereBand(stops, opacity, z, heightScale, yOffsetScale) {
            var band = new THREE.Mesh(
                new THREE.PlaneGeometry(W, Math.max(H * heightScale, 1)),
                new THREE.MeshBasicMaterial({
                    map: makeLinearTexture(2, 256, stops, false),
                    transparent: true,
                    opacity: opacity,
                    depthWrite: false,
                    depthTest: false
                })
            );
            band.position.set(W / 2, H * yOffsetScale, z || -30);
            scene.add(band);
            return band;
        }

        function addTintOverlay(stops, opacity, z) {
            var overlay = new THREE.Mesh(
                new THREE.PlaneGeometry(Math.max(W, 1), Math.max(H, 1)),
                new THREE.MeshBasicMaterial({
                    map: makeLinearTexture(2, 256, stops, false),
                    transparent: true,
                    opacity: opacity,
                    depthWrite: false,
                    depthTest: false
                })
            );
            overlay.position.set(W / 2, H / 2, z || -40);
            scene.add(overlay);
            return overlay;
        }

        function radialGlow(size, rgba) {
            var c = document.createElement('canvas'); c.width = c.height = size;
            var ctx = c.getContext('2d');
            var cx = size / 2;
            var grad = ctx.createRadialGradient(cx, cx, 0, cx, cx, cx);
            grad.addColorStop(0, rgba[0]);
            grad.addColorStop(0.45, rgba[1]);
            grad.addColorStop(1, rgba[2]);
            ctx.fillStyle = grad;
            ctx.fillRect(0, 0, size, size);
            var tex = new THREE.CanvasTexture(c); tex.needsUpdate = true; return tex;
        }

        function addVignette(opacity, z) {
            var mesh = new THREE.Mesh(
                new THREE.PlaneGeometry(Math.max(W, 1), Math.max(H, 1)),
                new THREE.MeshBasicMaterial({
                    map: radialGlow(256, [
                        'rgba(0,0,0,0)',
                        'rgba(0,0,0,0)',
                        'rgba(0,0,0,0.9)'
                    ]),
                    transparent: true,
                    opacity: opacity,
                    depthWrite: false,
                    depthTest: false
                })
            );
            mesh.position.set(W / 2, H / 2, z || 40);
            scene.add(mesh);
            return mesh;
        }

        function applyNavbarWeatherStyle(name, elapsed) {
            if (!navbar) return;

            var presets = {
                clear: {
                    base: 'linear-gradient(135deg, rgba(38,92,145,0.96), rgba(230,166,84,0.82) 58%, rgba(255,223,159,0.92))',
                    sky: 'linear-gradient(180deg, rgba(255,248,225,0.22), rgba(255,255,255,0.03) 58%, rgba(255,214,135,0.08))',
                    glow: 'radial-gradient(circle at 82% 18%, rgba(255,233,176,0.35), rgba(255,244,214,0.12) 22%, rgba(255,255,255,0) 52%)',
                    shadow: 'rgba(84, 52, 18, 0.24)'
                },
                cloudy: {
                    base: 'linear-gradient(135deg, rgba(74,92,118,0.97), rgba(126,138,158,0.9) 54%, rgba(92,106,128,0.96))',
                    sky: 'linear-gradient(180deg, rgba(228,233,240,0.12), rgba(255,255,255,0.02) 42%, rgba(170,180,194,0.08))',
                    glow: 'radial-gradient(circle at 68% 10%, rgba(236,240,246,0.14), rgba(236,240,246,0.05) 24%, rgba(255,255,255,0) 48%)',
                    shadow: 'rgba(18, 24, 34, 0.24)'
                },
                fog: {
                    base: 'linear-gradient(135deg, rgba(126,138,149,0.95), rgba(188,197,205,0.86) 56%, rgba(150,160,168,0.92))',
                    sky: 'linear-gradient(180deg, rgba(248,250,252,0.16), rgba(255,255,255,0.08) 44%, rgba(222,228,233,0.12))',
                    glow: 'radial-gradient(circle at 50% 20%, rgba(255,255,255,0.18), rgba(255,255,255,0.08) 26%, rgba(255,255,255,0) 56%)',
                    shadow: 'rgba(56, 64, 70, 0.16)'
                },
                rain: {
                    base: 'linear-gradient(135deg, rgba(24,40,69,0.97), rgba(47,82,126,0.9) 46%, rgba(23,49,90,0.96))',
                    sky: 'linear-gradient(180deg, rgba(184,208,242,0.12), rgba(255,255,255,0.02) 44%, rgba(93,123,170,0.1))',
                    glow: 'radial-gradient(circle at 22% 0%, rgba(178,210,255,0.14), rgba(178,210,255,0.06) 18%, rgba(255,255,255,0) 42%)',
                    shadow: 'rgba(6, 12, 24, 0.3)'
                },
                drizzle: {
                    base: 'linear-gradient(135deg, rgba(58,74,96,0.96), rgba(104,122,148,0.88) 52%, rgba(72,88,110,0.94))',
                    sky: 'linear-gradient(180deg, rgba(210,222,240,0.1), rgba(255,255,255,0.03) 45%, rgba(150,168,196,0.08))',
                    glow: 'radial-gradient(circle at 28% 8%, rgba(224,234,248,0.12), rgba(224,234,248,0.04) 24%, rgba(255,255,255,0) 48%)',
                    shadow: 'rgba(14, 18, 26, 0.24)'
                },
                snow: {
                    base: 'linear-gradient(135deg, rgba(78,102,132,0.95), rgba(150,176,205,0.88) 50%, rgba(98,122,149,0.94))',
                    sky: 'linear-gradient(180deg, rgba(247,250,255,0.16), rgba(255,255,255,0.06) 46%, rgba(196,214,235,0.1))',
                    glow: 'radial-gradient(circle at 70% 12%, rgba(245,249,255,0.2), rgba(245,249,255,0.08) 24%, rgba(255,255,255,0) 52%)',
                    shadow: 'rgba(26, 42, 58, 0.18)'
                },
                thunderstorm: {
                    base: 'linear-gradient(135deg, rgba(12,20,38,0.98), rgba(38,52,86,0.92) 44%, rgba(18,24,48,0.98))',
                    sky: 'linear-gradient(180deg, rgba(122,142,186,0.08), rgba(255,255,255,0.01) 38%, rgba(72,88,122,0.1))',
                    glow: 'radial-gradient(circle at 18% 0%, rgba(160,190,255,0.1), rgba(160,190,255,0.04) 18%, rgba(255,255,255,0) 40%)',
                    shadow: 'rgba(2, 4, 10, 0.38)'
                },
                none: {
                    base: 'linear-gradient(135deg, rgba(45,106,79,0.96), rgba(27,67,50,0.94))',
                    sky: 'linear-gradient(180deg, rgba(255,255,255,0.08), rgba(255,255,255,0))',
                    glow: 'radial-gradient(circle at 82% 18%, rgba(255,255,255,0.12), rgba(255,255,255,0) 48%)',
                    shadow: 'rgba(4, 16, 12, 0.22)'
                }
            };

            var preset = presets[name] || presets.none;
            navbar.style.setProperty('--weather-nav-base', preset.base);
            navbar.style.setProperty('--weather-nav-sky', preset.sky);
            navbar.style.setProperty('--weather-nav-shadow', preset.shadow);

            var driftX = 50 + Math.sin(elapsed * 0.03) * 18;
            var driftY = 14 + Math.cos(elapsed * 0.025) * 8;
            var pulse = 0.82 + Math.abs(Math.sin(elapsed * 0.08)) * 0.16;
            var dynamicGlow = preset.glow
                .replace('circle at ', 'circle at ' + driftX.toFixed(1) + '% ' + driftY.toFixed(1) + '%, ');
            navbar.style.setProperty('--weather-nav-glow', dynamicGlow);
            navbar.style.setProperty('--weather-nav-glow-opacity', pulse.toFixed(3));
        }

        // ══════════════════════════════════════════
        // ── SNOW — horizontal drift across navbar ──
        // ══════════════════════════════════════════

        function initSnow() {
            var count = isMobile ? 35 : 80;
            var tex = softDot(64, 255, 255, 255, 1);
            var geo = new THREE.BufferGeometry();
            var pos = new Float32Array(count * 3);
            var sizes = new Float32Array(count);
            var seeds = new Float32Array(count);
            var depth = new Float32Array(count);
            var sway = new Float32Array(count);
            for (var i = 0; i < count; i++) {
                pos[i*3] = rand(0, W); pos[i*3+1] = rand(0, H); pos[i*3+2] = 0;
                depth[i] = rand(0.45, 1.25);
                sizes[i] = rand(1.5, 5.5) * depth[i];
                seeds[i] = rand(0, Math.PI*2);
                sway[i] = rand(8, 22);
            }
            geo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
            var mat = new THREE.PointsMaterial({
                map: tex, size: 6, transparent: true, opacity: 0.8,
                depthWrite: false, blending: THREE.AdditiveBlending, sizeAttenuation: false
            });
            scene.add(new THREE.Points(geo, mat));

            var tint = addTintOverlay([
                [0, 'rgba(205,220,245,0.16)'],
                [0.65, 'rgba(215,228,248,0.08)'],
                [1, 'rgba(255,255,255,0.02)']
            ], 0.7, -34);
            var haze = addAtmosphereBand([
                [0, 'rgba(235,242,255,0.26)'],
                [0.4, 'rgba(235,242,255,0.14)'],
                [1, 'rgba(235,242,255,0)']
            ], 0.65, -25, 1.5, 0.58);
            var vignette = addVignette(0.08, 30);

            // Bokeh layer
            var bCnt = isMobile ? 7 : 14;
            var bGeo = new THREE.BufferGeometry();
            var bPos = new Float32Array(bCnt * 3);
            var bSeeds = new Float32Array(bCnt);
            var bSpeed = new Float32Array(bCnt);
            for (var b = 0; b < bCnt; b++) {
                bPos[b*3] = rand(0, W); bPos[b*3+1] = rand(0, H); bPos[b*3+2] = -10;
                bSeeds[b] = rand(0, Math.PI*2);
                bSpeed[b] = rand(5, 14);
            }
            bGeo.setAttribute('position', new THREE.BufferAttribute(bPos, 3));
            var bMat = new THREE.PointsMaterial({
                map: bokehDot(64, 220, 230, 255), size: isMobile ? 20 : 35,
                transparent: true, opacity: 0.12, depthWrite: false, sizeAttenuation: false
            });
            scene.add(new THREE.Points(bGeo, bMat));

            return {
                update: function (elapsed) {
                    var p = geo.attributes.position.array;
                    for (var i = 0; i < count; i++) {
                        var gust = flowNoise(elapsed * 0.7, seeds[i]);
                        p[i*3] += gust * 0.08 * sway[i] / 10 + 0.1 * depth[i];
                        p[i*3+1] += 0.42 + sizes[i] * 0.18 + Math.cos(elapsed * 0.9 + seeds[i]) * 0.04;
                        if (p[i*3+1] > H + 8) {
                            p[i*3+1] = rand(-12, -2);
                            p[i*3] = rand(-20, W + 20);
                        }
                        if (p[i*3] > W + 16) { p[i*3] = rand(-18, -4); }
                        if (p[i*3] < -24) { p[i*3] = rand(W + 4, W + 18); }
                    }
                    geo.attributes.position.needsUpdate = true;
                    var bp = bGeo.attributes.position.array;
                    for (var b = 0; b < bCnt; b++) {
                        bp[b*3] += bSpeed[b] * 0.04;
                        bp[b*3+1] += 0.15 + Math.sin(elapsed * 0.28 + bSeeds[b]) * 0.16;
                        if (bp[b*3] > W + 20 || bp[b*3+1] > H + 18) {
                            bp[b*3] = rand(-30, -5);
                            bp[b*3+1] = rand(-15, H * 0.55);
                        }
                    }
                    bGeo.attributes.position.needsUpdate = true;
                    mat.opacity = 0.58 + Math.sin(elapsed * 0.23) * 0.05;
                    haze.material.opacity = 0.46 + Math.sin(elapsed * 0.17) * 0.04;
                    tint.material.opacity = 0.64 + Math.abs(flowNoise(elapsed * 0.08, 0.4)) * 0.04;
                    vignette.material.opacity = 0.06 + Math.abs(Math.sin(elapsed * 0.05)) * 0.02;
                }
            };
        }

        // ══════════════════════════════════════════
        // ── RAIN — streaks falling through navbar ──
        // ══════════════════════════════════════════

        function initRain() {
            var fgCount = isMobile ? 30 : 60;
            var bgCount = isMobile ? 20 : 40;

            var dropGeo = new THREE.PlaneGeometry(1, 1);

            // Rain drop texture (short streak for navbar height)
            function makeDropTex(w, h) {
                var c = document.createElement('canvas'); c.width = w; c.height = h;
                var ctx = c.getContext('2d'); var cx = w/2;
                var grad = ctx.createLinearGradient(0, 0, 0, h);
                grad.addColorStop(0,   'rgba(180,210,255,0)');
                grad.addColorStop(0.2, 'rgba(200,225,255,0.4)');
                grad.addColorStop(0.6, 'rgba(215,235,255,0.8)');
                grad.addColorStop(1,   'rgba(240,248,255,1)');
                ctx.fillStyle = grad;
                ctx.fillRect(cx - 1, 0, 2, h);
                var tex = new THREE.CanvasTexture(c); tex.needsUpdate = true; return tex;
            }

            var windAngle = rand(0.05, 0.12);
            var windTarget = windAngle, windTimer = 0;
            var tint = addTintOverlay([
                [0, 'rgba(65,92,135,0.22)'],
                [0.6, 'rgba(80,112,160,0.08)'],
                [1, 'rgba(110,150,210,0.02)']
            ], 0.75, -36);
            var mist = addAtmosphereBand([
                [0, 'rgba(175,205,245,0.22)'],
                [0.45, 'rgba(150,185,235,0.1)'],
                [1, 'rgba(110,145,205,0)']
            ], 0.55, -18, 1.45, 0.56);
            var sheen = new THREE.Mesh(
                new THREE.PlaneGeometry(Math.max(W, 1), Math.max(H * 0.55, 1)),
                new THREE.MeshBasicMaterial({
                    map: makeLinearTexture(2, 256, [
                        [0, 'rgba(210,230,255,0.18)'],
                        [0.55, 'rgba(185,210,245,0.06)'],
                        [1, 'rgba(185,210,245,0)']
                    ], false),
                    transparent: true,
                    opacity: 0.14,
                    depthWrite: false,
                    blending: THREE.AdditiveBlending
                })
            );
            sheen.position.set(W / 2, H * 0.18, -10);
            scene.add(sheen);
            var vignette = addVignette(0.12, 34);

            // ── Foreground ──
            var fgTex = makeDropTex(4, 40);
            var fgMat = new THREE.MeshBasicMaterial({
                map: fgTex, transparent: true, depthWrite: false, depthTest: false,
                opacity: 0.9, blending: THREE.AdditiveBlending,
                color: new THREE.Color(0xc5e0ff), side: THREE.DoubleSide
            });
            var fgGroup = new THREE.Group();
            scene.add(fgGroup);
            var fgDrops = [];

            function resetFg(d, init) {
                d.x = rand(-10, W + 10);
                d.y = init ? rand(-H * 0.5, H) : rand(-H * 0.8, -H * 0.1);
                d.len = rand(H * 0.4, H * 1.2);
                d.w = rand(0.15, 0.3);
                d.speed = rand(180, 320);
                d.alpha = rand(0.5, 1.0);
                d.seed = rand(0, Math.PI * 2);
                d.wobble = rand(0.012, 0.03);
                d.mesh.scale.set(d.w, d.len, 1);
                d.mesh.position.set(d.x, d.y, 0);
            }

            for (var i = 0; i < fgCount; i++) {
                var m = new THREE.Mesh(dropGeo, fgMat.clone());
                m.renderOrder = 2; fgGroup.add(m);
                var d = { mesh: m };
                resetFg(d, true); fgDrops.push(d);
            }

            // ── Background ──
            var bgTex = makeDropTex(3, 30);
            var bgMat = new THREE.MeshBasicMaterial({
                map: bgTex, transparent: true, depthWrite: false, depthTest: false,
                opacity: 0.5, blending: THREE.NormalBlending,
                color: new THREE.Color(0x90b5e5), side: THREE.DoubleSide
            });
            var bgGroup = new THREE.Group();
            bgGroup.position.z = -5;
            scene.add(bgGroup);
            var bgDrops = [];

            function resetBg(d, init) {
                d.x = rand(-10, W + 10);
                d.y = init ? rand(-H * 0.3, H) : rand(-H * 0.6, -H * 0.1);
                d.len = rand(H * 0.3, H * 0.8);
                d.w = rand(0.1, 0.2);
                d.speed = rand(120, 220);
                d.alpha = rand(0.2, 0.45);
                d.seed = rand(0, Math.PI * 2);
                d.wobble = rand(0.006, 0.016);
                d.mesh.scale.set(d.w, d.len, 1);
                d.mesh.position.set(d.x, d.y, 0);
            }

            for (var j = 0; j < bgCount; j++) {
                var bm = new THREE.Mesh(dropGeo, bgMat.clone());
                bm.renderOrder = 1; bgGroup.add(bm);
                var bd = { mesh: bm };
                resetBg(bd, true); bgDrops.push(bd);
            }

            // ── Splash sparks at bottom ──
            var spCnt = isMobile ? 10 : 20;
            var spTex = softDot(32, 220, 235, 255, 0.9);
            var spGeo = new THREE.BufferGeometry();
            var spPos = new Float32Array(spCnt * 3);
            var spAlpha = new Float32Array(spCnt);
            var spSz = new Float32Array(spCnt);
            var spLife = new Float32Array(spCnt);
            var spMax = new Float32Array(spCnt);
            var splQ = [];

            for (var s = 0; s < spCnt; s++) { spLife[s] = 2; spPos[s*3+1] = H; }
            spGeo.setAttribute('position', new THREE.BufferAttribute(spPos, 3));
            spGeo.setAttribute('alpha', new THREE.BufferAttribute(spAlpha, 1));
            spGeo.setAttribute('pSize', new THREE.BufferAttribute(spSz, 1));

            var sVert = 'attribute float alpha;attribute float pSize;uniform float uPR;varying float vA;void main(){vA=alpha;gl_PointSize=pSize*uPR;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.0);}';
            var sFrag = 'uniform sampler2D uTex;varying float vA;void main(){vec4 t=texture2D(uTex,gl_PointCoord);gl_FragColor=vec4(t.rgb,t.a*vA);}';

            var spMat = new THREE.ShaderMaterial({
                uniforms: { uTex: { value: spTex }, uPR: { value: renderer.getPixelRatio() } },
                vertexShader: sVert, fragmentShader: sFrag,
                transparent: true, depthWrite: false, blending: THREE.AdditiveBlending
            });
            scene.add(new THREE.Points(spGeo, spMat));

            function resetSp(i) {
                var sq = splQ.length ? splQ.shift() : { x: rand(0, W) };
                spPos[i*3] = sq.x; spPos[i*3+1] = H - rand(0, 3); spPos[i*3+2] = 0;
                spLife[i] = 0; spMax[i] = rand(0.06, 0.18); spAlpha[i] = 0; spSz[i] = 0;
            }

            return {
                update: function (elapsed, delta) {
                    windTimer -= delta;
                    if (windTimer <= 0) { windTarget = rand(0.03, 0.18); windTimer = rand(1.5, 4); }
                    windAngle += (windTarget - windAngle) * delta * 0.8;
                    var gustField = flowNoise(elapsed * 0.55, 0.7) * 0.015;
                    var tilt = -Math.atan((windAngle + gustField) * 1.2);

                    // Foreground
                    for (var fi = 0; fi < fgDrops.length; fi++) {
                        var f = fgDrops[fi];
                        f.y += f.speed * delta;
                        f.x -= f.speed * (windAngle + gustField + flowNoise(elapsed * 2.1, f.seed) * f.wobble) * delta;
                        f.mesh.position.set(f.x, f.y, 0);
                        f.mesh.rotation.z = tilt + Math.sin(elapsed * 2 + f.seed) * 0.022;
                        var fi1 = Math.min(1, (f.y + H*0.3) / (H*0.4));
                        var fo1 = Math.max(0, 1 - (f.y - H*0.6) / (H*0.4));
                        f.mesh.material.opacity = f.alpha * fi1 * fo1;
                        if (f.y > H + f.len * 0.3) {
                            splQ.push({ x: f.x });
                            resetFg(f, false);
                        }
                    }

                    // Background
                    var bgTilt = -Math.atan(windAngle * 0.8);
                    for (var bi = 0; bi < bgDrops.length; bi++) {
                        var b = bgDrops[bi];
                        b.y += b.speed * delta;
                        b.x -= b.speed * ((windAngle + gustField) * 0.6 + flowNoise(elapsed * 1.2, b.seed) * b.wobble) * delta;
                        b.mesh.position.set(b.x, b.y, 0);
                        b.mesh.rotation.z = bgTilt;
                        var bi1 = Math.min(1, (b.y + H*0.2) / (H*0.3));
                        var bo1 = Math.max(0, 1 - (b.y - H*0.7) / (H*0.3));
                        b.mesh.material.opacity = b.alpha * bi1 * bo1;
                        if (b.y > H + b.len * 0.3) { resetBg(b, false); }
                    }

                    // Splashes
                    for (var si = 0; si < spCnt; si++) {
                        spLife[si] += delta / spMax[si];
                        if (spLife[si] >= 1) { resetSp(si); continue; }
                        var fl = spLife[si] < 0.3 ? spLife[si]/0.3 : 1 - (spLife[si]-0.3)/0.7;
                        spAlpha[si] = fl * 0.7;
                        spSz[si] = 2 + fl * 5;
                    }
                    spGeo.attributes.position.needsUpdate = true;
                    spGeo.attributes.alpha.needsUpdate = true;
                    spGeo.attributes.pSize.needsUpdate = true;
                    mist.material.opacity = 0.48 + Math.min(0.12, Math.abs(windAngle - windTarget) * 1.5);
                    tint.material.opacity = 0.68 + clamp(Math.abs(gustField) * 6, 0, 0.08);
                    sheen.material.opacity = 0.1 + clamp(Math.abs(gustField) * 7, 0, 0.12);
                    vignette.material.opacity = 0.11 + Math.abs(Math.sin(elapsed * 0.1)) * 0.015;
                }
            };
        }

        // ══════════════════════════════════════════
        // ── DRIZZLE — light streaks ──
        // ══════════════════════════════════════════

        function initDrizzle() {
            var count = isMobile ? 25 : 50;
            var geo = new THREE.BufferGeometry();
            var pos = new Float32Array(count * 3);
            var speeds = new Float32Array(count);
            var seeds = new Float32Array(count);
            var lean = new Float32Array(count);
            for (var i = 0; i < count; i++) {
                pos[i*3] = rand(0, W); pos[i*3+1] = rand(-5, H); pos[i*3+2] = 0;
                speeds[i] = rand(60, 130); seeds[i] = rand(0, Math.PI*2); lean[i] = rand(0.015, 0.05);
            }
            geo.setAttribute('position', new THREE.BufferAttribute(pos, 3));

            var tc = document.createElement('canvas'); tc.width = 4; tc.height = 16;
            var tctx = tc.getContext('2d');
            var grad = tctx.createLinearGradient(0, 0, 0, 16);
            grad.addColorStop(0, 'rgba(200,220,255,0)');
            grad.addColorStop(0.4, 'rgba(215,230,255,0.5)');
            grad.addColorStop(1, 'rgba(230,240,255,0.85)');
            tctx.fillStyle = grad; tctx.fillRect(1, 0, 2, 16);
            var tex = new THREE.CanvasTexture(tc); tex.needsUpdate = true;

            var mat = new THREE.PointsMaterial({
                map: tex, size: 10, transparent: true, opacity: 0.65,
                depthWrite: false, sizeAttenuation: false
            });
            scene.add(new THREE.Points(geo, mat));
            var tint = addTintOverlay([
                [0, 'rgba(130,150,180,0.12)'],
                [0.7, 'rgba(170,185,205,0.06)'],
                [1, 'rgba(190,200,215,0.02)']
            ], 0.65, -34);
            var veil = addAtmosphereBand([
                [0, 'rgba(205,220,240,0.2)'],
                [0.55, 'rgba(205,220,240,0.08)'],
                [1, 'rgba(205,220,240,0)']
            ], 0.5, -16, 1.35, 0.58);
            var vignette = addVignette(0.08, 32);

            return {
                update: function (elapsed, delta) {
                    var p = geo.attributes.position.array;
                    for (var i = 0; i < count; i++) {
                        p[i*3+1] += speeds[i] * delta;
                        p[i*3] -= speeds[i] * delta * (lean[i] + flowNoise(elapsed * 0.8, seeds[i]) * 0.004);
                        if (p[i*3+1] > H + 8) { p[i*3+1] = rand(-8, -2); p[i*3] = rand(0, W); }
                    }
                    geo.attributes.position.needsUpdate = true;
                    mat.opacity = 0.5 + Math.sin(elapsed * 0.25) * 0.05;
                    veil.material.opacity = 0.42 + Math.sin(elapsed * 0.18) * 0.04;
                    tint.material.opacity = 0.6 + Math.abs(Math.sin(elapsed * 0.07)) * 0.03;
                    vignette.material.opacity = 0.07 + Math.abs(Math.sin(elapsed * 0.08)) * 0.015;
                }
            };
        }

        // ══════════════════════════════════════════
        // ── CLEAR — gentle dust motes + light ──
        // ══════════════════════════════════════════

        function initClear() {
            var count = isMobile ? 18 : 34;
            var tex = softDot(32, 255, 250, 230, 0.9);
            var geo = new THREE.BufferGeometry();
            var pos = new Float32Array(count * 3);
            var seeds = new Float32Array(count);
            var lift = new Float32Array(count);
            for (var i = 0; i < count; i++) {
                pos[i*3] = rand(0, W); pos[i*3+1] = rand(0, H); pos[i*3+2] = 0;
                seeds[i] = rand(0, Math.PI*2);
                lift[i] = rand(0.6, 1.4);
            }
            geo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
            var mat = new THREE.PointsMaterial({
                map: tex, size: 5, transparent: true, opacity: 0.55,
                depthWrite: false, blending: THREE.AdditiveBlending, sizeAttenuation: false
            });
            scene.add(new THREE.Points(geo, mat));
            var skyTint = addTintOverlay([
                [0, 'rgba(255,222,168,0.08)'],
                [0.5, 'rgba(255,238,205,0.04)'],
                [1, 'rgba(255,255,255,0)']
            ], 0.6, -34);

            // Warm light wash
            var rayGeo = new THREE.PlaneGeometry(W * 0.4, H * 2);
            var rayMat = new THREE.MeshBasicMaterial({
                color: 0xfff4e0, transparent: true, opacity: 0.04,
                depthWrite: false, blending: THREE.AdditiveBlending, side: THREE.DoubleSide
            });
            var ray = new THREE.Mesh(rayGeo, rayMat);
            ray.position.set(W * 0.7, H / 2, -20);
            ray.rotation.z = -0.25;
            scene.add(ray);

            var glow = new THREE.Mesh(
                new THREE.PlaneGeometry(Math.max(W * 0.22, 1), Math.max(H * 1.8, 1)),
                new THREE.MeshBasicMaterial({
                    map: makeLinearTexture(256, 2, [
                        [0, 'rgba(255,235,180,0)'],
                        [0.45, 'rgba(255,240,195,0.22)'],
                        [0.5, 'rgba(255,248,225,0.45)'],
                        [0.55, 'rgba(255,240,195,0.22)'],
                        [1, 'rgba(255,235,180,0)']
                    ], true),
                    transparent: true,
                    opacity: 0.12,
                    depthWrite: false,
                    blending: THREE.AdditiveBlending
                })
            );
            glow.position.set(W * 0.76, H * 0.45, -22);
            glow.rotation.z = -0.3;
            scene.add(glow);
            var vignette = addVignette(0.05, 28);

            return {
                update: function (elapsed) {
                    var pulse = 0.4 + 0.6 * Math.abs(Math.sin(elapsed * 0.6));
                    mat.opacity = pulse * 0.45;
                    mat.size = 3 + pulse * 5;
                    var p = geo.attributes.position.array;
                    for (var i = 0; i < count; i++) {
                        p[i*3] += Math.sin(elapsed * 0.2 + seeds[i]) * 0.12 + 0.03 * lift[i];
                        p[i*3+1] += Math.cos(elapsed * 0.15 + seeds[i]) * 0.04 + 0.02 * lift[i];
                        if (p[i*3] > W + 5) { p[i*3] = rand(-5, 0); p[i*3+1] = rand(0, H); }
                    }
                    geo.attributes.position.needsUpdate = true;
                    ray.material.opacity = 0.03 + Math.sin(elapsed * 0.15) * 0.015;
                    glow.material.opacity = 0.1 + Math.abs(Math.sin(elapsed * 0.2)) * 0.05;
                    skyTint.material.opacity = 0.5 + Math.abs(Math.sin(elapsed * 0.05)) * 0.03;
                    vignette.material.opacity = 0.04 + Math.abs(Math.sin(elapsed * 0.08)) * 0.01;
                }
            };
        }

        // ══════════════════════════════════════════
        // ── CLOUDY — drifting cloud blobs ──
        // ══════════════════════════════════════════

        function initCloudy() {
            var layerCount = isMobile ? 4 : 6;
            var layers = [];
            var tint = addTintOverlay([
                [0, 'rgba(110,125,150,0.12)'],
                [0.55, 'rgba(155,165,185,0.05)'],
                [1, 'rgba(195,200,210,0.02)']
            ], 0.7, -34);
            var canopy = addAtmosphereBand([
                [0, 'rgba(178,188,212,0.3)'],
                [0.45, 'rgba(178,188,212,0.16)'],
                [1, 'rgba(178,188,212,0)']
            ], 0.55, -26, 1.5, 0.58);
            var vignette = addVignette(0.09, 30);

            for (var i = 0; i < layerCount; i++) {
                var tex = cloudDot(192, [218 - i * 5, 223 - i * 5, 236 - i * 3], 0.95 - i * 0.08);
                var mat = new THREE.MeshBasicMaterial({
                    map: tex,
                    transparent: true,
                    opacity: 0.12 + i * 0.015,
                    depthWrite: false,
                    blending: THREE.NormalBlending
                });
                var mesh = new THREE.Mesh(
                    new THREE.PlaneGeometry(W * rand(0.34, 0.52), H * rand(0.95, 1.25)),
                    mat
                );
                mesh.position.set(rand(-W * 0.1, W * 1.05), rand(H * 0.35, H * 0.82), -14 - i);
                layers.push({
                    mesh: mesh,
                    speed: rand(3, 9) + i * 0.6,
                    sway: rand(0.8, 1.8),
                    seed: rand(0, Math.PI * 2)
                });
                scene.add(mesh);
            }

            return {
                update: function (elapsed, delta) {
                    for (var i = 0; i < layers.length; i++) {
                        var layer = layers[i];
                        layer.mesh.position.x += layer.speed * delta;
                        layer.mesh.position.y += flowNoise(elapsed * 0.18, layer.seed) * 0.03 * layer.sway;
                        if (layer.mesh.position.x > W + layer.mesh.scale.x * 40) {
                            layer.mesh.position.x = -W * 0.18;
                            layer.mesh.position.y = rand(H * 0.35, H * 0.82);
                        }
                        layer.mesh.material.opacity = 0.11 + i * 0.02 + Math.sin(elapsed * 0.08 + layer.seed) * 0.015;
                    }
                    canopy.material.opacity = 0.48 + Math.sin(elapsed * 0.1) * 0.04;
                    tint.material.opacity = 0.64 + Math.abs(Math.sin(elapsed * 0.04)) * 0.025;
                    vignette.material.opacity = 0.08 + Math.abs(Math.sin(elapsed * 0.05)) * 0.012;
                }
            };
        }

        // ══════════════════════════════════════════
        // ── FOG — drifting wisps ──
        // ══════════════════════════════════════════

        function initFog() {
            var layerCount = isMobile ? 3 : 5;
            var layers = [];
            var tint = addTintOverlay([
                [0, 'rgba(205,215,225,0.2)'],
                [0.65, 'rgba(220,228,235,0.12)'],
                [1, 'rgba(240,245,250,0.04)']
            ], 0.82, -34);
            var veil = addAtmosphereBand([
                [0, 'rgba(225,232,240,0.4)'],
                [0.55, 'rgba(225,232,240,0.24)'],
                [1, 'rgba(225,232,240,0.04)']
            ], 0.72, -28, 1.6, 0.55);
            var vignette = addVignette(0.05, 30);

            for (var i = 0; i < layerCount; i++) {
                var tex = cloudDot(224, [230, 235, 242], 0.9);
                var mat = new THREE.MeshBasicMaterial({
                    map: tex,
                    transparent: true,
                    opacity: 0.1 + i * 0.03,
                    depthWrite: false
                });
                var mesh = new THREE.Mesh(
                    new THREE.PlaneGeometry(W * rand(0.48, 0.72), H * rand(1.0, 1.35)),
                    mat
                );
                mesh.position.set(rand(-W * 0.12, W * 1.05), rand(H * 0.28, H * 0.8), -15 - i);
                scene.add(mesh);
                layers.push({
                    mesh: mesh,
                    drift: rand(2, 6),
                    bob: rand(0.5, 1.2),
                    seed: rand(0, Math.PI * 2)
                });
            }

            return {
                update: function (elapsed) {
                    for (var i = 0; i < layers.length; i++) {
                        var layer = layers[i];
                        layer.mesh.position.x += layer.drift * 0.12 + flowNoise(elapsed * 0.11, layer.seed) * 0.06;
                        layer.mesh.position.y += Math.cos(elapsed * 0.08 + layer.seed) * 0.05 * layer.bob;
                        if (layer.mesh.position.x > W * 1.12) {
                            layer.mesh.position.x = -W * 0.16;
                            layer.mesh.position.y = rand(H * 0.28, H * 0.8);
                        }
                        layer.mesh.material.opacity = 0.09 + i * 0.025 + Math.sin(elapsed * 0.06 + layer.seed) * 0.012;
                    }
                    veil.material.opacity = 0.62 + Math.sin(elapsed * 0.09) * 0.04;
                    tint.material.opacity = 0.74 + Math.abs(Math.sin(elapsed * 0.05)) * 0.03;
                    vignette.material.opacity = 0.04 + Math.abs(Math.sin(elapsed * 0.04)) * 0.01;
                }
            };
        }

        // ══════════════════════════════════════════
        // ── THUNDERSTORM — rain + flash ──
        // ══════════════════════════════════════════

        function initThunderstorm() {
            var rain = initRain();
            var flashGeo = new THREE.PlaneGeometry(W, H);
            var flashMat = new THREE.MeshBasicMaterial({
                color: 0xe0e8ff, transparent: true, opacity: 0, depthWrite: false
            });
            var flash = new THREE.Mesh(flashGeo, flashMat);
            flash.position.set(W/2, H/2, 50);
            scene.add(flash);
            var tint = addTintOverlay([
                [0, 'rgba(38,48,82,0.3)'],
                [0.6, 'rgba(62,72,110,0.14)'],
                [1, 'rgba(80,98,140,0.04)']
            ], 0.82, -36);
            var stormTint = addAtmosphereBand([
                [0, 'rgba(80,100,145,0.26)'],
                [0.6, 'rgba(80,100,145,0.1)'],
                [1, 'rgba(80,100,145,0)']
            ], 0.7, -12, 1.45, 0.56);
            var vignette = addVignette(0.16, 36);

            var nextFlash = rand(1.5, 4), phase = -1, start = 0;

            return {
                update: function (elapsed, delta) {
                    rain.update(elapsed, delta);
                    if (phase < 0 && elapsed > nextFlash) { phase = 0; start = elapsed; }
                    if (phase >= 0) {
                        var t = elapsed - start;
                        if      (t < 0.05) flashMat.opacity = 0.6;
                        else if (t < 0.1)  flashMat.opacity = 0.02;
                        else if (t < 0.16) flashMat.opacity = 0.4;
                        else if (t < 0.22) flashMat.opacity = 0.1;
                        else { flashMat.opacity = 0; phase = -1; nextFlash = elapsed + rand(2, 6); }
                    }
                    tint.material.opacity = 0.78 - flashMat.opacity * 0.18;
                    stormTint.material.opacity = 0.62 + flashMat.opacity * 0.35;
                    vignette.material.opacity = 0.14 - flashMat.opacity * 0.04;
                }
            };
        }

        // ══════════════════════════════════════════
        // ── LOGO GOLD PARTICLES — diffraction flakes ──
        // ══════════════════════════════════════════

        function initLogoParticles() {
            var logoImg = document.querySelector('.navbar-brand img');
            if (!logoImg) { console.log('[Weather] No logo image found'); return null; }

            var count = isMobile ? 10 : 20;
            var geo = new THREE.BufferGeometry();
            var pos = new Float32Array(count * 3);
            var alphas = new Float32Array(count);
            var sizes = new Float32Array(count);
            var life = new Float32Array(count);
            var maxLife = new Float32Array(count);
            var vx = new Float32Array(count);
            var vy = new Float32Array(count);
            var phase = new Float32Array(count);

            geo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
            geo.setAttribute('alpha', new THREE.BufferAttribute(alphas, 1));
            geo.setAttribute('pSize', new THREE.BufferAttribute(sizes, 1));
            geo.setAttribute('phase', new THREE.BufferAttribute(phase, 1));

            // Diffraction shader: gold → rose → white color shift
            var logoVert = [
                'attribute float alpha;',
                'attribute float pSize;',
                'attribute float phase;',
                'uniform float uPR;',
                'varying float vA;',
                'varying float vPhase;',
                'void main() {',
                '    vA = alpha;',
                '    vPhase = phase;',
                '    gl_PointSize = pSize * uPR;',
                '    gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);',
                '}'
            ].join('\n');

            var logoFrag = [
                'uniform sampler2D uTex;',
                'varying float vA;',
                'varying float vPhase;',
                'void main() {',
                '    vec4 t = texture2D(uTex, gl_PointCoord);',
                '    // Diffraction color shift: gold base with phase-dependent hue',
                '    float p = vPhase;',
                '    vec3 gold  = vec3(0.85, 0.68, 0.20);',
                '    vec3 rose  = vec3(0.92, 0.62, 0.48);',
                '    vec3 white = vec3(1.0, 0.95, 0.85);',
                '    vec3 col;',
                '    if (p < 0.5) {',
                '        col = mix(gold, rose, p * 2.0);',
                '    } else {',
                '        col = mix(rose, white, (p - 0.5) * 2.0);',
                '    }',
                '    gl_FragColor = vec4(col * t.rgb, t.a * vA);',
                '}'
            ].join('\n');

            var flakeTex = softDot(32, 255, 230, 160, 1.0);
            var logoMat = new THREE.ShaderMaterial({
                uniforms: {
                    uTex: { value: flakeTex },
                    uPR: { value: renderer.getPixelRatio() }
                },
                vertexShader: logoVert,
                fragmentShader: logoFrag,
                transparent: true,
                depthWrite: false,
                blending: THREE.AdditiveBlending
            });

            var points = new THREE.Points(geo, logoMat);
            points.renderOrder = 10;
            scene.add(points);

            // Get logo position relative to navbar
            function getLogoPos() {
                var navRect = navbar.getBoundingClientRect();
                var logoRect = logoImg.getBoundingClientRect();
                return {
                    x: logoRect.right - navRect.left,
                    y: logoRect.top - navRect.top + logoRect.height * 0.5
                };
            }

            function resetParticle(i) {
                var lp = getLogoPos();
                pos[i*3]     = lp.x + rand(-3, 5);
                pos[i*3 + 1] = lp.y + rand(-8, 8);
                pos[i*3 + 2] = 0;
                life[i] = 0;
                maxLife[i] = rand(2.5, 5.5);
                vx[i] = rand(20, 70);
                vy[i] = rand(-6, 6);
                alphas[i] = 0;
                sizes[i] = 0;
                phase[i] = rand(0, 1);
            }

            // Stagger initial spawn
            for (var i = 0; i < count; i++) {
                resetParticle(i);
                life[i] = rand(0, maxLife[i]);
            }

            return {
                update: function (elapsed, delta) {
                    for (var i = 0; i < count; i++) {
                        life[i] += delta;
                        var t = life[i] / maxLife[i];
                        if (t >= 1) { resetParticle(i); continue; }

                        // Move: drift right + gentle vertical wave
                        pos[i*3]     += vx[i] * delta;
                        pos[i*3 + 1] += vy[i] * delta + Math.sin(elapsed * 3 + phase[i] * 6.28) * 0.3;

                        // Fade in → hold → fade out
                        var fadeIn  = Math.min(1, t / 0.15);
                        var fadeOut = Math.max(0, 1 - (t - 0.6) / 0.4);
                        alphas[i] = fadeIn * fadeOut * 0.85;

                        // Size pulse
                        sizes[i] = (2 + Math.sin(elapsed * 4 + phase[i] * 6.28) * 1.5 + t * 2) * (isMobile ? 0.7 : 1);

                        // Cycle diffraction color over lifetime
                        phase[i] = (phase[i] + delta * 0.3) % 1;
                    }
                    geo.attributes.position.needsUpdate = true;
                    geo.attributes.alpha.needsUpdate = true;
                    geo.attributes.pSize.needsUpdate = true;
                    geo.attributes.phase.needsUpdate = true;
                }
            };
        }

        // ══════════════════════════════════════════
        // ── Initialize + Animate ──
        // ══════════════════════════════════════════

        var weatherSys = null;
        switch (condition) {
            case 'snow':         weatherSys = initSnow(); break;
            case 'rain':         weatherSys = initRain(); break;
            case 'drizzle':      weatherSys = initDrizzle(); break;
            case 'clear':        weatherSys = initClear(); break;
            case 'cloudy':       weatherSys = initCloudy(); break;
            case 'fog':          weatherSys = initFog(); break;
            case 'thunderstorm': weatherSys = initThunderstorm(); break;
        }

        var logoSys = initLogoParticles();

        if (!weatherSys && !logoSys) return;

        applyNavbarWeatherStyle(condition, 0);

        var paused = false;
        document.addEventListener('visibilitychange', function () {
            paused = document.hidden;
            if (!paused) clock.getDelta();
        });

        function animate() {
            requestAnimationFrame(animate);
            if (paused) return;
            var delta = clock.getDelta();
            var elapsed = clock.getElapsedTime();
            if (delta > 0.1) delta = 0.016;
            applyNavbarWeatherStyle(condition, elapsed);
            if (weatherSys) weatherSys.update(elapsed, delta);
            if (logoSys) logoSys.update(elapsed, delta);
            renderer.render(scene, camera);
        }
        animate();

        window.addEventListener('resize', function () {
            W = navbar ? navbar.offsetWidth : window.innerWidth;
            H = navbar ? navbar.offsetHeight : 64;
            canvas.width = W; canvas.height = H;
            renderer.setSize(W, H, false);
            camera.right = W; camera.bottom = H;
            camera.updateProjectionMatrix();
            isMobile = window.innerWidth < 768;
        });

        console.log('[Weather] Running: ' + condition);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', boot);
    } else {
        boot();
    }
})();
