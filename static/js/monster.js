/* ====================================================
   CIT Monster Resume X HirefireAI - Main Screen JS
   By Abhishek Sahoo | MCA, Cambridge Institute of Technology
   ==================================================== */

// Professional proof points cycle through the landing page hero.
const sarcasmQuotes = [
    { text: 'Make every application reflect your strongest work.', author: 'HireFire AI principle' },
    { text: 'Clarity helps recruiters see the value you bring.', author: 'Career intelligence' },
    { text: 'A focused resume creates momentum for the next step.', author: 'Resume guidance' },
    { text: 'Use evidence, structure, and intention to stand out.', author: 'Professional standard' },
    { text: 'Your experience deserves a clear, confident presentation.', author: 'HireFire AI principle' }
];

let quoteIndex = 0;

function cycleQuote() {
    const textEl = document.getElementById('quoteText');
    const dashEl = document.querySelector('.quote-dash');
    if (!textEl || !dashEl) return;

    textEl.style.opacity = '0';
    textEl.style.transform = 'translateY(10px)';

    setTimeout(() => {
        quoteIndex = (quoteIndex + 1) % sarcasmQuotes.length;
        const q = sarcasmQuotes[quoteIndex];
        textEl.textContent = q.text;
        dashEl.textContent = q.author;
        textEl.style.opacity = '1';
        textEl.style.transform = 'translateY(0)';
    }, 400);
}

setInterval(cycleQuote, 5500);

function triggerReveal() {
    const revealElements = document.querySelectorAll('.reveal');

    if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver(
            (entries) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('visible');
                        observer.unobserve(entry.target);
                    }
                });
            },
            { threshold: 0.12 }
        );
        revealElements.forEach((el) => observer.observe(el));
    } else {
        revealElements.forEach((el) => el.classList.add('visible'));
    }
}

window.addEventListener('DOMContentLoaded', () => {
    triggerReveal();
});

console.log('%cHireFire AI', 'font-size:24px;color:#2563eb;font-weight:bold;');
console.log('%cCareer intelligence platform | Built by Abhishek Sahoo', 'font-size:12px;color:#64748b;');
