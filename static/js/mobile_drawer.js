/* =====================================================================
   Мобилна бочна фиока (#mainDrawer) — понашање изнад Bootstrap offcanvas.
   Bootstrap већ даје: scrim (backdrop), scroll-lock тела, Esc, focus-trap
   и враћање фокуса, aria-modal/role. Овде додајемо:
     • свајп улево за затварање,
     • Back-дугме на Android-у (history state),
     • синхронизацију aria-expanded на хамбургеру,
     • затварање при навигацији (клик на ставку).
   ===================================================================== */
(function () {
    'use strict';

    document.addEventListener('DOMContentLoaded', function () {
        var drawerEl = document.getElementById('mainDrawer');
        var toggleBtn = document.getElementById('drawerToggle');
        if (!drawerEl || !window.bootstrap || !bootstrap.Offcanvas) {
            return;
        }

        var oc = bootstrap.Offcanvas.getOrCreateInstance(drawerEl);
        // Означава да је тренутно отварање гурнуло history state (за уредан back).
        var pushedState = false;

        function isOpen() {
            return drawerEl.classList.contains('show');
        }

        /* ---- aria-expanded + history state ---- */
        drawerEl.addEventListener('show.bs.offcanvas', function () {
            if (toggleBtn) {
                toggleBtn.setAttribute('aria-expanded', 'true');
            }
            // Гурни state само ако већ нисмо у "drawer" стању (нпр. поновно отварање).
            if (!(history.state && history.state.mibDrawer)) {
                history.pushState({ mibDrawer: true }, '');
                pushedState = true;
            }
        });

        drawerEl.addEventListener('hide.bs.offcanvas', function () {
            if (toggleBtn) {
                toggleBtn.setAttribute('aria-expanded', 'false');
            }
        });

        drawerEl.addEventListener('hidden.bs.offcanvas', function () {
            // Ако је фиока затворена неким UI путем (X, scrim, свајп, линк), а
            // history state који смо гурнули још стоји — очисти га без новог отварања.
            if (pushedState && history.state && history.state.mibDrawer) {
                pushedState = false;
                history.back();
            }
        });

        // Back-дугме (Android/десктоп): ако смо у drawer стању и фиока је отворена,
        // затвори је уместо напуштања странице.
        window.addEventListener('popstate', function () {
            pushedState = false;
            if (isOpen()) {
                oc.hide();
            }
        });

        /* ---- Свајп улево за затварање ---- */
        var touchStartX = null;
        var touchStartY = null;
        var swiping = false;

        drawerEl.addEventListener('touchstart', function (e) {
            if (e.touches.length !== 1) { return; }
            touchStartX = e.touches[0].clientX;
            touchStartY = e.touches[0].clientY;
            swiping = false;
        }, { passive: true });

        drawerEl.addEventListener('touchmove', function (e) {
            if (touchStartX === null) { return; }
            var dx = e.touches[0].clientX - touchStartX;
            var dy = e.touches[0].clientY - touchStartY;
            // Претежно хоризонталан гест улево.
            if (!swiping && Math.abs(dx) > 10 && Math.abs(dx) > Math.abs(dy)) {
                swiping = true;
            }
            if (swiping && dx < 0) {
                var shift = Math.max(dx, -drawerEl.offsetWidth);
                drawerEl.style.transform = 'translateX(' + shift + 'px)';
                drawerEl.style.transition = 'none';
            }
        }, { passive: true });

        function resetSwipe() {
            drawerEl.style.transform = '';
            drawerEl.style.transition = '';
            touchStartX = null;
            touchStartY = null;
        }

        drawerEl.addEventListener('touchend', function (e) {
            if (touchStartX === null) { return; }
            var dx = e.changedTouches[0].clientX - touchStartX;
            drawerEl.style.transform = '';
            drawerEl.style.transition = '';
            // Праг: свајп улево преко ~30% ширине → затвори.
            if (swiping && dx < -Math.max(60, drawerEl.offsetWidth * 0.3)) {
                oc.hide();
            }
            resetSwipe();
        }, { passive: true });

        drawerEl.addEventListener('touchcancel', resetSwipe, { passive: true });

        /* ---- Затварање при навигацији (клик на праву ставку) ---- */
        drawerEl.querySelectorAll('a.drawer-link[href]').forEach(function (link) {
            link.addEventListener('click', function () {
                var href = link.getAttribute('href');
                if (href && href !== '#') {
                    oc.hide();
                }
            });
        });

        /* ---- Ако корисник прошири на десктоп док је фиока отворена, затвори је ---- */
        window.addEventListener('resize', function () {
            if (isOpen() && window.innerWidth >= 1200) {
                oc.hide();
            }
        });
    });
})();
