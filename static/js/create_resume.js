/* ====================================================
   CIT Monster Resume X HirefireAI — Dynamic Layout Preview Engine
   By Abhishek Sahoo | MCA, Cambridge Institute of Technology
   ==================================================== */

let currentTemplate = 'default';

function updatePreview() {
    const name = document.getElementById("name").value || "Abhishek Sahoo";
    const email = document.getElementById("email").value || "abhishek@example.com";
    const phone = document.getElementById("phone").value || "+91 98765 43210";
    const linkedin = document.getElementById("linkedin").value || "linkedin.com/in/abhisheksahoo";
    const education = document.getElementById("education").value || "Cambridge Institute of Technology\nMaster of Computer Applications (MCA) | CGPA: 8.5";
    const experience = document.getElementById("experience").value || "DevOps & Software Engineer Intern at TechCorp\nWorked on Docker, CI/CD pipelines, and FastAPI microservices.";
    const projects = document.getElementById("projects").value || "CIT Monster Resume X HirefireAI\nBuilt a ML-driven resume parser and job finder with FastAPI.";
    const certifications = document.getElementById("certifications").value || "AWS Certified Solutions Architect\nTensorFlow Developer Certificate";

    const resume = document.getElementById("resume");
    if (!resume) return;

    // Render based on active template structure
    if (currentTemplate === 'default') {
        // Monster Cyber (Sleek dark futuristic container)
        resume.style.cssText = "border: 2px solid #a855f7; padding: 25px; border-radius: 20px; background: #0f172a; color: #f8fafc; font-family: 'Courier New', monospace; box-shadow: 0 20px 50px rgba(168, 85, 247, 0.25); min-height: 700px;";
        resume.innerHTML = `
            <div style="font-size: 2.2rem; font-weight: 800; color: #a855f7; border-bottom: 2px dashed #a855f7; padding-bottom: 8px; margin-bottom: 15px;">👾 ${name}</div>
            <div style="display: flex; gap: 15px; font-size: 0.85rem; color: #94a3b8; margin-bottom: 20px;">
                <span>📧 ${email}</span> | <span>📞 ${phone}</span> | <span>🌐 ${linkedin}</span>
            </div>
            <div style="margin-bottom: 15px;">
                <h4 style="color: #38bdf8; font-size: 1rem; border-bottom: 1px solid #334155; margin-bottom: 5px; padding-bottom: 2px;">⚡ EXPERIENCE</h4>
                <p style="white-space: pre-line; line-height: 1.4;">${experience}</p>
            </div>
            <div style="margin-bottom: 15px;">
                <h4 style="color: #38bdf8; font-size: 1rem; border-bottom: 1px solid #334155; margin-bottom: 5px; padding-bottom: 2px;">🛠️ PROJECTS</h4>
                <p style="white-space: pre-line; line-height: 1.4;">${projects}</p>
            </div>
            <div style="margin-bottom: 15px;">
                <h4 style="color: #38bdf8; font-size: 1rem; border-bottom: 1px solid #334155; margin-bottom: 5px; padding-bottom: 2px;">🎓 EDUCATION</h4>
                <p style="white-space: pre-line; line-height: 1.4;">${education}</p>
            </div>
            <div>
                <h4 style="color: #38bdf8; font-size: 1rem; border-bottom: 1px solid #334155; margin-bottom: 5px; padding-bottom: 2px;">🏆 CERTIFICATIONS</h4>
                <p style="white-space: pre-line; line-height: 1.4;">${certifications}</p>
            </div>
        `;
    } else if (currentTemplate === 'classic') {
        // Classic Light (Traditional serif layout, clean black and white, education first)
        resume.style.cssText = "padding: 30px; background: #ffffff; color: #111111; border-radius: 20px; font-family: 'Times New Roman', Times, serif; line-height: 1.5; box-shadow: 0 20px 50px rgba(2, 6, 23, 0.4); min-height: 700px; text-align: left;";
        resume.innerHTML = `
            <div style="text-align: center; font-size: 2.2rem; font-weight: bold; margin-bottom: 5px;">${name}</div>
            <div style="text-align: center; font-size: 0.9rem; margin-bottom: 25px; border-bottom: 1px solid #000; padding-bottom: 10px; color: #333333;">
                ${email} &bull; ${phone} &bull; ${linkedin}
            </div>
            <div style="margin-bottom: 20px;">
                <h3 style="font-size: 1.1rem; font-weight: bold; border-bottom: 1px solid #000; margin-bottom: 8px; color: #111111;">EDUCATION</h3>
                <p style="white-space: pre-line; font-size: 0.95rem; margin-left: 10px;">${education}</p>
            </div>
            <div style="margin-bottom: 20px;">
                <h3 style="font-size: 1.1rem; font-weight: bold; border-bottom: 1px solid #000; margin-bottom: 8px; color: #111111;">PROFESSIONAL EXPERIENCE</h3>
                <p style="white-space: pre-line; font-size: 0.95rem; margin-left: 10px;">${experience}</p>
            </div>
            <div style="margin-bottom: 20px;">
                <h3 style="font-size: 1.1rem; font-weight: bold; border-bottom: 1px solid #000; margin-bottom: 8px; color: #111111;">KEY PROJECTS</h3>
                <p style="white-space: pre-line; font-size: 0.95rem; margin-left: 10px;">${projects}</p>
            </div>
            <div>
                <h3 style="font-size: 1.1rem; font-weight: bold; border-bottom: 1px solid #000; margin-bottom: 8px; color: #111111;">CERTIFICATIONS</h3>
                <p style="white-space: pre-line; font-size: 0.95rem; margin-left: 10px;">${certifications}</p>
            </div>
        `;
    } else if (currentTemplate === 'executive') {
        // Executive Dark (Clean dark minimalist layout with blue primary header block)
        resume.style.cssText = "padding: 0; background: #0f172a; color: #e2e8f0; border-radius: 20px; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; box-shadow: 0 20px 50px rgba(2, 6, 23, 0.4); min-height: 700px; overflow: hidden;";
        resume.innerHTML = `
            <div style="background: #1e3a8a; padding: 30px; text-align: left;">
                <h1 style="font-size: 2.2rem; font-weight: 700; color: #ffffff; margin: 0; letter-spacing: 0.05em;">${name}</h1>
                <p style="font-size: 0.9rem; color: #93c5fd; margin: 5px 0 0 0;">${email} | ${phone} | ${linkedin}</p>
            </div>
            <div style="padding: 25px 30px;">
                <div style="margin-bottom: 20px;">
                    <h3 style="color: #3b82f6; font-size: 1.1rem; font-weight: 600; text-transform: uppercase; margin-bottom: 5px; border-left: 4px solid #3b82f6; padding-left: 10px;">Executive Summary</h3>
                    <p style="white-space: pre-line; font-size: 0.95rem; line-height: 1.5; color: #cbd5e1;">${experience}</p>
                </div>
                <div style="margin-bottom: 20px;">
                    <h3 style="color: #3b82f6; font-size: 1.1rem; font-weight: 600; text-transform: uppercase; margin-bottom: 5px; border-left: 4px solid #3b82f6; padding-left: 10px;">Portfolio Projects</h3>
                    <p style="white-space: pre-line; font-size: 0.95rem; line-height: 1.5; color: #cbd5e1;">${projects}</p>
                </div>
                <div style="margin-bottom: 20px;">
                    <h3 style="color: #3b82f6; font-size: 1.1rem; font-weight: 600; text-transform: uppercase; margin-bottom: 5px; border-left: 4px solid #3b82f6; padding-left: 10px;">Education</h3>
                    <p style="white-space: pre-line; font-size: 0.95rem; line-height: 1.5; color: #cbd5e1;">${education}</p>
                </div>
                <div>
                    <h3 style="color: #3b82f6; font-size: 1.1rem; font-weight: 600; text-transform: uppercase; margin-bottom: 5px; border-left: 4px solid #3b82f6; padding-left: 10px;">Professional Certifications</h3>
                    <p style="white-space: pre-line; font-size: 0.95rem; line-height: 1.5; color: #cbd5e1;">${certifications}</p>
                </div>
            </div>
        `;
    } else if (currentTemplate === 'orange') {
        // Vibrant Orange (Orange themed header, split blocks)
        resume.style.cssText = "padding: 25px; background: #fffcf8; color: #431407; border-radius: 20px; font-family: 'Trebuchet MS', sans-serif; box-shadow: 0 20px 50px rgba(234, 88, 12, 0.15); min-height: 700px;";
        resume.innerHTML = `
            <div style="text-align: left; border-bottom: 4px solid #ea580c; padding-bottom: 10px; margin-bottom: 20px;">
                <h1 style="color: #ea580c; font-size: 2.2rem; font-weight: bold; margin: 0;">${name}</h1>
                <p style="color: #7c2d12; font-size: 0.9rem; margin: 5px 0 0 0;"><strong>Phone:</strong> ${phone} | <strong>Email:</strong> ${email} | <strong>LinkedIn:</strong> ${linkedin}</p>
            </div>
            <div style="display: flex; flex-direction: column; gap: 18px;">
                <div>
                    <h3 style="color: #ea580c; font-size: 1.1rem; text-transform: uppercase; margin-bottom: 6px;">💡 Project Portfolio</h3>
                    <p style="white-space: pre-line; background: #ffedd5; padding: 12px; border-radius: 6px; border-left: 5px solid #ea580c; font-size:0.95rem;">${projects}</p>
                </div>
                <div>
                    <h3 style="color: #ea580c; font-size: 1.1rem; text-transform: uppercase; margin-bottom: 6px;">💼 Experience & History</h3>
                    <p style="white-space: pre-line; background: #ffedd5; padding: 12px; border-radius: 6px; border-left: 5px solid #ea580c; font-size:0.95rem;">${experience}</p>
                </div>
                <div>
                    <h3 style="color: #ea580c; font-size: 1.1rem; text-transform: uppercase; margin-bottom: 6px;">🎓 Education</h3>
                    <p style="white-space: pre-line; background: #ffedd5; padding: 12px; border-radius: 6px; border-left: 5px solid #ea580c; font-size:0.95rem;">${education}</p>
                </div>
                <div>
                    <h3 style="color: #ea580c; font-size: 1.1rem; text-transform: uppercase; margin-bottom: 6px;">🏆 Certifications</h3>
                    <p style="white-space: pre-line; background: #ffedd5; padding: 12px; border-radius: 6px; border-left: 5px solid #ea580c; font-size:0.95rem;">${certifications}</p>
                </div>
            </div>
        `;
    } else if (currentTemplate === 'burgundy') {
        // Elegant Serif (Cream background, burgundy colors, decorative border lines)
        resume.style.cssText = "padding: 30px; background: #fafaf9; color: #1c1917; border-radius: 20px; font-family: Georgia, serif; border: 12px double #78350f; box-shadow: 0 20px 50px rgba(120, 53, 15, 0.2); min-height: 700px;";
        resume.innerHTML = `
            <div style="text-align: center; margin-bottom: 20px;">
                <h1 style="color: #78350f; font-size: 2.2rem; margin: 0; font-family: Georgia, serif; font-weight: normal;">${name}</h1>
                <p style="color: #78716c; font-size: 0.85rem; font-style: italic; margin-top: 5px;">${email} &bull; ${phone} &bull; ${linkedin}</p>
            </div>
            <div style="margin-bottom: 15px;">
                <div style="text-align: center; color: #78350f; font-size: 1rem; font-weight: bold; border-top: 1px solid #78350f; border-bottom: 1px solid #78350f; padding: 3px 0; margin-bottom: 8px; letter-spacing: 0.08em;">ACADEMIC PROFILE</div>
                <p style="white-space: pre-line; font-size: 0.9rem; line-height: 1.4;">${education}</p>
            </div>
            <div style="margin-bottom: 15px;">
                <div style="text-align: center; color: #78350f; font-size: 1rem; font-weight: bold; border-top: 1px solid #78350f; border-bottom: 1px solid #78350f; padding: 3px 0; margin-bottom: 8px; letter-spacing: 0.08em;">WORK EXPERIENCE</div>
                <p style="white-space: pre-line; font-size: 0.9rem; line-height: 1.4;">${experience}</p>
            </div>
            <div style="margin-bottom: 15px;">
                <div style="text-align: center; color: #78350f; font-size: 1rem; font-weight: bold; border-top: 1px solid #78350f; border-bottom: 1px solid #78350f; padding: 3px 0; margin-bottom: 8px; letter-spacing: 0.08em;">DEVELOPMENT & PROJECTS</div>
                <p style="white-space: pre-line; font-size: 0.9rem; line-height: 1.4;">${projects}</p>
            </div>
            <div>
                <div style="text-align: center; color: #78350f; font-size: 1rem; font-weight: bold; border-top: 1px solid #78350f; border-bottom: 1px solid #78350f; padding: 3px 0; margin-bottom: 8px; letter-spacing: 0.08em;">LICENSES & CERTIFICATIONS</div>
                <p style="white-space: pre-line; font-size: 0.9rem; line-height: 1.4;">${certifications}</p>
            </div>
        `;
    } else if (currentTemplate === 'mono') {
        // Modern Tech (Green terminal command theme, top title is terminal banner)
        resume.style.cssText = "padding: 25px; background: #052e16; color: #4ade80; border-radius: 20px; font-family: Consolas, Monaco, monospace; font-size: 0.85rem; border: 2px solid #22c55e; box-shadow: 0 20px 50px rgba(34, 197, 94, 0.2); min-height: 700px;";
        resume.innerHTML = `
            <div style="border-bottom: 1px solid #22c55e; padding-bottom: 10px; margin-bottom: 15px;">
                <p style="margin: 0; color: #86efac;">$ cat abhisheksahoo_profile.sh</p>
                <h1 style="color: #22c55e; font-size: 1.8rem; margin: 5px 0;">NAME="${name}"</h1>
                <p style="margin: 0; color: #a7f3d0;">CONTACT="${email} | ${phone} | ${linkedin}"</p>
            </div>
            <div style="margin-bottom: 12px;">
                <p style="margin: 0; font-weight: bold; color: #a7f3d0;">$ get_experience --full</p>
                <p style="white-space: pre-line; padding-left: 10px; margin-top: 3px;">${experience}</p>
            </div>
            <div style="margin-bottom: 12px;">
                <p style="margin: 0; font-weight: bold; color: #a7f3d0;">$ get_projects --featured</p>
                <p style="white-space: pre-line; padding-left: 10px; margin-top: 3px;">${projects}</p>
            </div>
            <div style="margin-bottom: 12px;">
                <p style="margin: 0; font-weight: bold; color: #a7f3d0;">$ get_education</p>
                <p style="white-space: pre-line; padding-left: 10px; margin-top: 3px;">${education}</p>
            </div>
            <div>
                <p style="margin: 0; font-weight: bold; color: #a7f3d0;">$ get_certifications</p>
                <p style="white-space: pre-line; padding-left: 10px; margin-top: 3px;">${certifications}</p>
            </div>
        `;
    } else if (currentTemplate === 'cyber') {
        // Cyber Neon (Glow Pink / Cyan accents, dark background, border gradient look)
        resume.style.cssText = "padding: 25px; background: #000000; color: #ffffff; border-radius: 20px; font-family: 'Century Gothic', sans-serif; border: 3px solid #ff007f; box-shadow: 0 0 25px #ff007f; min-height: 700px;";
        resume.innerHTML = `
            <div style="text-align: right; border-bottom: 2px solid #00f0ff; padding-bottom: 10px; margin-bottom: 20px;">
                <h1 style="color: #00f0ff; text-shadow: 0 0 5px #00f0ff; font-size: 2.2rem; font-weight: 900; margin: 0; text-transform: uppercase;">${name}</h1>
                <p style="color: #ff007f; font-size: 0.85rem; margin-top: 4px;">[ ${email} || ${phone} || ${linkedin} ]</p>
            </div>
            <div style="margin-bottom: 15px;">
                <div style="color: #ff007f; font-weight: bold; font-size: 0.95rem; margin-bottom: 5px;">&gt; ACTIVE PROJECTS</div>
                <p style="white-space: pre-line; color: #e5e5e5; font-size: 0.9rem; padding-left: 12px; border-left: 2px solid #ff007f;">${projects}</p>
            </div>
            <div style="margin-bottom: 15px;">
                <div style="color: #ff007f; font-weight: bold; font-size: 0.95rem; margin-bottom: 5px;">&gt; EDUCATION TRACK</div>
                <p style="white-space: pre-line; color: #e5e5e5; font-size: 0.9rem; padding-left: 12px; border-left: 2px solid #ff007f;">${education}</p>
            </div>
            <div style="margin-bottom: 15px;">
                <div style="color: #ff007f; font-weight: bold; font-size: 0.95rem; margin-bottom: 5px;">&gt; SERVICE LOGS</div>
                <p style="white-space: pre-line; color: #e5e5e5; font-size: 0.9rem; padding-left: 12px; border-left: 2px solid #ff007f;">${experience}</p>
            </div>
            <div>
                <div style="color: #ff007f; font-weight: bold; font-size: 0.95rem; margin-bottom: 5px;">&gt; DECRYPIONS & CERTIFICATIONS</div>
                <p style="white-space: pre-line; color: #e5e5e5; font-size: 0.9rem; padding-left: 12px; border-left: 2px solid #ff007f;">${certifications}</p>
            </div>
        `;
    } else if (currentTemplate === 'royal') {
        // Royal Blue (Elegant thick blue borders, split layout with sidebar blocks)
        resume.style.cssText = "padding: 30px; background: #ffffff; color: #334155; border-radius: 20px; font-family: Calibri, sans-serif; border-top: 10px solid #1e40af; border-bottom: 10px solid #1e40af; box-shadow: 0 20px 50px rgba(30, 64, 175, 0.2); min-height: 700px;";
        resume.innerHTML = `
            <div style="margin-bottom: 22px;">
                <h1 style="color: #1e40af; font-size: 2.3rem; font-weight: 800; margin: 0;">${name}</h1>
                <p style="color: #64748b; font-size: 0.9rem; margin-top: 4px; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px;">
                    <strong>Email:</strong> ${email} &bull; <strong>Phone:</strong> ${phone} &bull; <strong>LinkedIn:</strong> ${linkedin}
                </p>
            </div>
            <div style="display: flex; flex-direction: column; gap: 15px;">
                <div>
                    <h3 style="color: #1e40af; font-size: 1.1rem; font-weight: bold; text-transform: uppercase; margin-bottom: 4px;">Experience Profile</h3>
                    <div style="padding-left: 10px; border-left: 3px solid #1e40af; font-size: 0.95rem; line-height: 1.4;">${experience}</div>
                </div>
                <div>
                    <h3 style="color: #1e40af; font-size: 1.1rem; font-weight: bold; text-transform: uppercase; margin-bottom: 4px;">Key Innovations</h3>
                    <div style="padding-left: 10px; border-left: 3px solid #1e40af; font-size: 0.95rem; line-height: 1.4;">${projects}</div>
                </div>
                <div>
                    <h3 style="color: #1e40af; font-size: 1.1rem; font-weight: bold; text-transform: uppercase; margin-bottom: 4px;">Education</h3>
                    <div style="padding-left: 10px; border-left: 3px solid #1e40af; font-size: 0.95rem; line-height: 1.4;">${education}</div>
                </div>
                <div>
                    <h3 style="color: #1e40af; font-size: 1.1rem; font-weight: bold; text-transform: uppercase; margin-bottom: 4px;">Certifications</h3>
                    <div style="padding-left: 10px; border-left: 3px solid #1e40af; font-size: 0.95rem; line-height: 1.4;">${certifications}</div>
                </div>
            </div>
        `;
    } else if (currentTemplate === 'split') {
        // Left Sidebar (Clean asymmetric layout, contact details in left column, main sections on right)
        resume.style.cssText = "display: grid; grid-template-columns: 1fr 2fr; background: #ffffff; color: #1e293b; border-radius: 20px; font-family: Arial, sans-serif; box-shadow: 0 20px 50px rgba(2, 6, 23, 0.4); min-height: 700px; overflow: hidden;";
        resume.innerHTML = `
            <!-- Sidebar -->
            <div style="background: #f1f5f9; padding: 25px; border-right: 1px solid #cbd5e1; text-align: left;">
                <div style="font-size: 1.6rem; font-weight: 800; color: #1e3a8a; line-height: 1.2; margin-bottom: 25px;">${name}</div>
                <div style="margin-bottom: 25px;">
                    <h4 style="font-size: 0.8rem; font-weight: bold; color: #64748b; text-transform: uppercase; margin-bottom: 8px;">Contact</h4>
                    <p style="font-size: 0.85rem; margin: 5px 0;">📧 ${email}</p>
                    <p style="font-size: 0.85rem; margin: 5px 0;">📞 ${phone}</p>
                    <p style="font-size: 0.85rem; margin: 5px 0;">🌐 ${linkedin}</p>
                </div>
                <div>
                    <h4 style="font-size: 0.8rem; font-weight: bold; color: #64748b; text-transform: uppercase; margin-bottom: 8px;">Education</h4>
                    <p style="white-space: pre-line; font-size: 0.85rem; line-height: 1.3;">${education}</p>
                </div>
            </div>
            <!-- Main Body -->
            <div style="padding: 30px; text-align: left;">
                <div style="margin-bottom: 25px;">
                    <h3 style="font-size: 1.1rem; font-weight: 800; color: #1e3a8a; border-bottom: 2px solid #cbd5e1; padding-bottom: 4px; margin-bottom: 10px;">Experience</h3>
                    <p style="white-space: pre-line; font-size: 0.9rem; line-height: 1.4; color: #334155;">${experience}</p>
                </div>
                <div style="margin-bottom: 25px;">
                    <h3 style="font-size: 1.1rem; font-weight: 800; color: #1e3a8a; border-bottom: 2px solid #cbd5e1; padding-bottom: 4px; margin-bottom: 10px;">Projects</h3>
                    <p style="white-space: pre-line; font-size: 0.9rem; line-height: 1.4; color: #334155;">${projects}</p>
                </div>
                <div>
                    <h3 style="font-size: 1.1rem; font-weight: 800; color: #1e3a8a; border-bottom: 2px solid #cbd5e1; padding-bottom: 4px; margin-bottom: 10px;">Certifications</h3>
                    <p style="white-space: pre-line; font-size: 0.9rem; line-height: 1.4; color: #334155;">${certifications}</p>
                </div>
            </div>
        `;
    } else if (currentTemplate === 'nightmare') {
        // Red Alert Comic (Bright red styling, comic font, comical notes, custom spacing)
        resume.style.cssText = "padding: 25px; background: #fff1f2; color: #9f1239; border-radius: 20px; font-family: 'Comic Sans MS', cursive; border: 4px dashed #f43f5e; box-shadow: 0 20px 50px rgba(244, 63, 94, 0.2); min-height: 700px;";
        resume.innerHTML = `
            <div style="text-align: center; margin-bottom: 20px;">
                <span style="background: #f43f5e; color: white; padding: 4px 10px; font-weight: bold; border-radius: 4px; font-size: 0.75rem; text-transform: uppercase;">⚠️ WARNING: Flagship Applicant</span>
                <h1 style="color: #e11d48; font-size: 2.2rem; font-weight: bold; margin: 8px 0 0 0; font-family: 'Comic Sans MS', cursive;">${name}</h1>
                <p style="font-size: 0.85rem; margin-top: 5px;">Email: ${email} | Phone: ${phone} | LinkedIn: ${linkedin}</p>
            </div>
            <div style="margin-bottom: 15px;">
                <h3 style="color: #e11d48; border-bottom: 2px solid #f43f5e; font-size: 1rem; font-weight: bold; margin-bottom: 5px; font-family: 'Comic Sans MS', cursive;">💥 EXPERIENCE PROFILE</h3>
                <p style="white-space: pre-line; font-size: 0.9rem; line-height: 1.3;">${experience}</p>
            </div>
            <div style="margin-bottom: 15px;">
                <h3 style="color: #e11d48; border-bottom: 2px solid #f43f5e; font-size: 1rem; font-weight: bold; margin-bottom: 5px; font-family: 'Comic Sans MS', cursive;">🔥 COMPLETED PROJECTS</h3>
                <p style="white-space: pre-line; font-size: 0.9rem; line-height: 1.3;">${projects}</p>
            </div>
            <div style="margin-bottom: 15px;">
                <h3 style="color: #e11d48; border-bottom: 2px solid #f43f5e; font-size: 1rem; font-weight: bold; margin-bottom: 5px; font-family: 'Comic Sans MS', cursive;">🎓 SCHOOLING</h3>
                <p style="white-space: pre-line; font-size: 0.9rem; line-height: 1.3;">${education}</p>
            </div>
            <div>
                <h3 style="color: #e11d48; border-bottom: 2px solid #f43f5e; font-size: 1rem; font-weight: bold; margin-bottom: 5px; font-family: 'Comic Sans MS', cursive;">🏆 SKILLS / CERTIFICATES</h3>
                <p style="white-space: pre-line; font-size: 0.9rem; line-height: 1.3;">${certifications}</p>
            </div>
        `;
    }
}

function downloadPDF() {
    const { jsPDF } = window.jspdf;
    const resume = document.getElementById("resume");
    if (!resume) return;

    html2canvas(resume, { backgroundColor: null, scale: 2 }).then(canvas => {
        let imgData = canvas.toDataURL("image/png");
        let doc = new jsPDF("p", "mm", "a4");

        let imgWidth = 200; 
        let imgHeight = (canvas.height * imgWidth) / canvas.width;
        doc.addImage(imgData, "PNG", 5, 5, imgWidth - 4, imgHeight - 4);
        doc.save("resume.pdf");
    });
}

function selectTemplate(templateName) {
    currentTemplate = templateName;

    // Trigger update to redraw custom structure
    updatePreview();

    // Update active button state
    document.querySelectorAll(".template-btn").forEach(btn => {
        btn.classList.remove("active");
    });
    const activeBtn = document.getElementById(`btn-tmpl-${templateName}`);
    if (activeBtn) activeBtn.classList.add("active");
}

// Initialize preview on DOM load
window.addEventListener("DOMContentLoaded", () => {
    updatePreview();
});