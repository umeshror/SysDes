/* Centralized System Design Scripts */

const pb = document.getElementById('pb');
const pageSections = document.querySelectorAll('.section');
const subItems = document.querySelectorAll('.acc-sub-item[data-sec]');

function showSection(id) {
    if (!pageSections.length) return;
    pageSections.forEach(s => s.classList.remove('active'));
    subItems.forEach(n => n.classList.remove('active'));
    const target = document.getElementById(id);
    if (target) {
        target.classList.add('active');
        const diags = target.querySelectorAll('.mermaid:not([data-processed])');
        if (diags.length && typeof mermaid !== 'undefined') {
            mermaid.run({ nodes: diags });
        }
        const main = document.querySelector('.main');
        if (main) main.scrollTo(0, 0);
    }
    const item = document.querySelector(`.acc-sub-item[data-sec="${id}"]`);
    if (item) item.classList.add('active');
    updateProgress(id);
}

function updateProgress(activeId) {
    if (!pb || !subItems.length) return;
    const ids = Array.from(subItems).map(n => n.dataset.sec);
    const idx = ids.indexOf(activeId);
    const pct = idx >= 0 ? Math.round(((idx + 1) / ids.length) * 100) : 0;
    pb.style.width = pct + '%';
}

subItems.forEach(item => {
    item.addEventListener('click', () => {
        if (item.dataset.sec) showSection(item.dataset.sec);
    });
});

// Deep linking support
window.addEventListener('load', () => {
    const hash = window.location.hash.slice(1);
    if (hash && document.getElementById(hash)) {
        showSection(hash);
    } else if (subItems.length && subItems[0].dataset.sec) {
        showSection(subItems[0].dataset.sec);
    }
});

// Scroll progress and Back to Top
const mainEl = document.querySelector('.main');
const bttBtn = document.getElementById('back-to-top');

if (mainEl && pb) {
    mainEl.addEventListener('scroll', () => {
        const top = mainEl.scrollTop;
        if (bttBtn) bttBtn.classList.toggle('visible', top > 500);

        // Smooth scroll progress
        const scrolled = top + mainEl.clientHeight;
        const total = mainEl.scrollHeight;
        if (total > 0 && !document.querySelector('.section.active')) { // only if not using section switching
            pb.style.width = Math.min(100, Math.round((scrolled / total) * 100)) + '%';
        }
    });
}

if (bttBtn) {
    bttBtn.addEventListener('click', () => {
        if (mainEl) mainEl.scrollTo({ top: 0, behavior: 'smooth' });
        else window.scrollTo({ top: 0, behavior: 'smooth' });
    });
}
