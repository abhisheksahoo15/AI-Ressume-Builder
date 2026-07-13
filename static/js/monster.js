/* ====================================================
   CIT Monster Resume X HirefireAI - Main Screen JS
   By Abhishek Sahoo | MCA, Cambridge Institute of Technology
   ==================================================== */

// Sarcastic quotes cycle on the CIT hero.
const sarcasmQuotes = [
    { text: '"College thinks AI means \\"Attendance Issue.\\""', author: '- Attendance office AI' },
    { text: '"The only cloud I learned in college was the weather."', author: '- Cloud computing lab' },
    { text: '"College thinks Python is a snake. That\'s why they never taught us."', author: '- Abhishek Sahoo' },
    { text: '"College gave us theory. Placements asked for receipts."', author: '- CIT survivor' },
    { text: '"Attendance short, confidence full."', author: '- Semester strategy' },
    { text: '"Code works on my laptop. Lab PC took it personally."', author: '- Practical file witness' },
    { text: '"Viva question: explain your project. Me: which part survived?"', author: '- Final year energy' },
    { text: '"Group project taught teamwork, patience, and trust issues."', author: '- Team lead by force' },
    { text: '"Presentation ready. HDMI cable entered villain mode."', author: '- Seminar hall classic' },
    { text: '"Deadline tomorrow, motivation still loading."', author: '- Student operating system' },
    { text: '"DBMS taught normalization. My deadline taught copy-paste."', author: '- Academic balance' },
    { text: '"Software Engineering: 80% UML, 20% hoping the demo works."', author: '- Industry prep' },
    { text: '"Systems are working... leave it lol."', author: '- Practical lab review' },
    { text: '"CGPA is temporary. Debugging trauma is permanent."', author: '- Placement philosopher' }
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

const konamiCode = ['ArrowUp','ArrowUp','ArrowDown','ArrowDown','ArrowLeft','ArrowRight','ArrowLeft','ArrowRight','b','a'];
let konamiIdx = 0;

document.addEventListener('keydown', (e) => {
    if (e.key === konamiCode[konamiIdx]) {
        konamiIdx++;
        if (konamiIdx === konamiCode.length) {
            konamiIdx = 0;

            for (let i = 0; i < 8; i++) {
                setTimeout(() => {
                    const m = document.createElement('div');
                    m.style.cssText = `
                        position: fixed;
                        font-size: ${Math.random() * 42 + 24}px;
                        left: ${Math.random() * 100}vw;
                        top: ${Math.random() * 100}vh;
                        z-index: 99999;
                        pointer-events: none;
                        color: #fdba74;
                        font-family: 'Fredoka One', cursive;
                        animation: konamiMonster 2s ease-out forwards;
                    `;
                    m.textContent = ['AI', 'ATS', 'JOB', 'CV'][Math.floor(Math.random() * 4)];
                    document.body.appendChild(m);
                    setTimeout(() => m.remove(), 2000);
                }, i * 150);
            }

            const ks = document.createElement('style');
            ks.textContent = `
                @keyframes konamiMonster {
                    0% { opacity: 1; transform: scale(0) rotate(0deg); }
                    50% { opacity: 1; transform: scale(1.5) rotate(180deg); }
                    100% { opacity: 0; transform: scale(0.5) rotate(360deg) translateY(-100px); }
                }
            `;
            document.head.appendChild(ks);
        }
    } else {
        konamiIdx = 0;
    }
});

console.log('%cCIT Monster Resume X HirefireAI', 'font-size:24px;color:#7c3aed;font-weight:bold;text-shadow: 0 0 10px #f97316;');
console.log('%cBuilt by Abhishek Sahoo | MCA Dept, Cambridge Institute of Technology, Bangalore', 'font-size:12px;color:#38bdf8;');
console.log('%c"College gave us theory. We built the proof."', 'font-size:11px;color:#f97316;font-style:italic;');
console.log('%cKonami Code for a surprise: up up down down left right left right BA', 'font-size:10px;color:#94a3b8;');
