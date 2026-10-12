"""Custom styling and CSS rules for the LegalEase Streamlit interface.

Delivers a premium, futuristic, dark legal-tech SaaS visual identity:
- Dark cinematic background (#070B14) with subtle AI grid and radial glows
- Glassmorphism card surfaces with subtle borders and backdrops
- Electric Blue & Violet accents with cyan highlights
- Modern typography via Inter & JetBrains Mono with serif contrast for legal parchment
- Polished Streamlit input, textarea, selectbox, and button overrides
"""

CUSTOM_CSS = """
<style>
/* ==============================================================================
   1. GLOBAL FONTS & RESET
   ============================================================================== */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,600;0,6..72,700;1,6..72,400&family=Cinzel:wght@600;700&display=swap');

:root {
    --bg-primary: #070B14;
    --bg-secondary: #0B1020;
    --card-bg: rgba(17, 24, 39, 0.72);
    --card-border: rgba(255, 255, 255, 0.08);
    --card-border-hover: rgba(59, 130, 246, 0.35);
    --accent-blue: #2563EB;
    --accent-electric: #3B82F6;
    --accent-violet: #7C3AED;
    --accent-cyan: #06B6D4;
    --accent-cyan-glow: #38BDF8;
    --accent-amber: #F59E0B;
    --text-primary: #F8FAFC;
    --text-secondary: #94A3B8;
    --text-muted: #64748B;
    --radius-sm: 6px;
    --radius-md: 10px;
    --radius-lg: 16px;
    --radius-xl: 20px;
    --transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}

/* Base Body & Container */
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    color: var(--text-primary) !important;
}

[data-testid="stAppViewContainer"] {
    background-color: var(--bg-primary) !important;
    background-image: 
        radial-gradient(circle at 50% 0%, rgba(37, 99, 235, 0.14) 0%, transparent 45%),
        radial-gradient(circle at 90% 85%, rgba(124, 58, 237, 0.09) 0%, transparent 40%),
        radial-gradient(circle at 10% 40%, rgba(6, 182, 212, 0.06) 0%, transparent 35%),
        linear-gradient(rgba(255, 255, 255, 0.018) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255, 255, 255, 0.018) 1px, transparent 1px) !important;
    background-size: 100% 100%, 100% 100%, 100% 100%, 40px 40px, 40px 40px !important;
    background-attachment: fixed !important;
}

/* Top Streamlit Header */
[data-testid="stHeader"] {
    background-color: rgba(7, 11, 20, 0.75) !important;
    backdrop-filter: blur(16px) !important;
    -webkit-backdrop-filter: blur(16px) !important;
    border-bottom: 1px solid var(--card-border) !important;
}

/* Main Content Spacing */
.main .block-container {
    padding-top: 1.2rem !important;
    padding-bottom: 3.5rem !important;
    max-width: 1400px !important;
}

/* Sleek Scrollbar */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}
::-webkit-scrollbar-track {
    background: #070B14;
}
::-webkit-scrollbar-thumb {
    background: #1E293B;
    border-radius: 999px;
}
::-webkit-scrollbar-thumb:hover {
    background: #3B82F6;
}

/* ==============================================================================
   2. TOP NAVIGATION BAR
   ============================================================================== */
.top-nav-container {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: rgba(11, 16, 32, 0.75);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid var(--card-border);
    border-radius: var(--radius-lg);
    padding: 0.75rem 1.4rem;
    margin-bottom: 1.6rem;
    box-shadow: 0 4px 24px -1px rgba(0, 0, 0, 0.35);
}

.nav-brand-group {
    display: flex;
    align-items: center;
    gap: 0.85rem;
}

.nav-brand-logo {
    width: 36px;
    height: 36px;
    border-radius: 9px;
    background: linear-gradient(135deg, rgba(37, 99, 235, 0.3), rgba(124, 58, 237, 0.3));
    border: 1px solid rgba(59, 130, 246, 0.35);
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 0 14px rgba(59, 130, 246, 0.25);
    overflow: hidden;
}

.nav-brand-logo img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.nav-brand-text {
    display: flex;
    flex-direction: column;
}

.nav-brand-name {
    font-size: 1.15rem;
    font-weight: 700;
    letter-spacing: -0.01em;
    color: #F8FAFC;
    line-height: 1.2;
}

.nav-brand-badge {
    font-size: 0.62rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--accent-cyan-glow);
}

.nav-links-group {
    display: flex;
    align-items: center;
    gap: 0.4rem;
}

.nav-item {
    font-size: 0.82rem;
    font-weight: 500;
    color: var(--text-secondary);
    padding: 0.4rem 0.85rem;
    border-radius: var(--radius-sm);
    text-decoration: none;
    transition: var(--transition);
    cursor: default;
    border: 1px solid transparent;
}

.nav-item.active {
    color: #F8FAFC;
    background: rgba(37, 99, 235, 0.15);
    border-color: rgba(59, 130, 246, 0.3);
    box-shadow: 0 0 12px rgba(59, 130, 246, 0.15);
}

.nav-item:hover:not(.active) {
    color: #F8FAFC;
    background: rgba(255, 255, 255, 0.04);
}

.nav-status-pill {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    background: rgba(16, 185, 129, 0.1);
    border: 1px solid rgba(16, 185, 129, 0.25);
    padding: 0.35rem 0.75rem;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 600;
    color: #34D399;
    letter-spacing: 0.04em;
}

.pulse-dot {
    width: 7px;
    height: 7px;
    background-color: #10B981;
    border-radius: 50%;
    box-shadow: 0 0 8px #10B981;
    animation: pulse 2s infinite cubic-bezier(0.4, 0, 0.6, 1);
}

@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.45; transform: scale(0.85); }
}

/* ==============================================================================
   3. HERO SECTION
   ============================================================================== */
.hero-wrapper {
    background: linear-gradient(135deg, rgba(15, 23, 42, 0.6) 0%, rgba(11, 16, 32, 0.8) 100%);
    border: 1px solid var(--card-border);
    border-radius: var(--radius-xl);
    padding: 2.2rem 2.5rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
    box-shadow: 0 12px 36px -8px rgba(0, 0, 0, 0.5);
}

.hero-glow-orb {
    position: absolute;
    top: -50px;
    right: -50px;
    width: 280px;
    height: 280px;
    background: radial-gradient(circle, rgba(59, 130, 246, 0.18) 0%, rgba(124, 58, 237, 0.08) 50%, transparent 70%);
    border-radius: 50%;
    pointer-events: none;
    filter: blur(24px);
}

.hero-meta-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
    background: rgba(37, 99, 235, 0.12);
    border: 1px solid rgba(59, 130, 246, 0.3);
    padding: 0.28rem 0.8rem;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 600;
    color: var(--accent-cyan-glow);
    text-transform: uppercase;
    letter-spacing: 0.09em;
    margin-bottom: 0.9rem;
    box-shadow: 0 0 16px rgba(59, 130, 246, 0.15);
}

.hero-title {
    font-size: 2.45rem !important;
    font-weight: 800 !important;
    letter-spacing: -0.03em !important;
    color: #F8FAFC !important;
    line-height: 1.15 !important;
    margin: 0 0 0.6rem 0 !important;
}

.hero-gradient-text {
    background: linear-gradient(135deg, #60A5FA 0%, #A78BFA 60%, #38BDF8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    font-size: 1.02rem;
    color: var(--text-secondary);
    max-width: 680px;
    line-height: 1.55;
    margin: 0;
}

/* ==============================================================================
   4. WORKSPACE PANELS & CARDS
   ============================================================================== */
.workspace-card {
    background: var(--card-bg);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border: 1px solid var(--card-border);
    border-radius: var(--radius-lg);
    padding: 1.6rem 1.8rem;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    transition: var(--transition);
}

.workspace-card:hover {
    border-color: rgba(255, 255, 255, 0.12);
}

.panel-eyebrow {
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    color: var(--accent-cyan-glow);
    text-transform: uppercase;
    margin-bottom: 0.35rem;
}

.panel-title {
    font-size: 1.35rem !important;
    font-weight: 700 !important;
    color: #F8FAFC !important;
    margin: 0 0 0.35rem 0 !important;
    letter-spacing: -0.01em !important;
}

.panel-desc {
    font-size: 0.85rem;
    color: var(--text-secondary);
    margin-bottom: 1.1rem;
    line-height: 1.45;
}

/* Step Indicator */
.step-indicator-wrap {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    background: rgba(11, 16, 32, 0.6);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: var(--radius-md);
    padding: 0.5rem 0.8rem;
    margin-bottom: 1.3rem;
}

.step-pill {
    font-size: 0.72rem;
    font-weight: 600;
    color: var(--text-muted);
    letter-spacing: 0.06em;
    display: flex;
    align-items: center;
    gap: 0.35rem;
}

.step-pill.active {
    color: var(--accent-cyan-glow);
}

.step-num {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    padding: 0.12rem 0.35rem;
    border-radius: 4px;
    background: rgba(255, 255, 255, 0.06);
}

.step-pill.active .step-num {
    background: rgba(56, 189, 248, 0.2);
    color: #38BDF8;
}

.step-sep {
    color: var(--text-muted);
    font-size: 0.7rem;
    opacity: 0.5;
}

/* Field Microcopy */
.field-microcopy {
    font-size: 0.74rem;
    color: var(--text-muted);
    margin-top: -0.5rem;
    margin-bottom: 0.9rem;
    line-height: 1.3;
}

/* ==============================================================================
   5. STREAMLIT FORM INPUT OVERRIDES
   ============================================================================== */
/* Labels */
[data-testid="stWidgetLabel"] label, [data-testid="stWidgetLabel"] p {
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
    color: #E2E8F0 !important;
    margin-bottom: 0.3rem !important;
}

/* Text Inputs, Textarea, Select, Date Input */
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea,
[data-testid="stDateInput"] input {
    background-color: rgba(11, 16, 32, 0.85) !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: var(--radius-md) !important;
    color: #F8FAFC !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.9rem !important;
    padding: 0.65rem 0.85rem !important;
    transition: var(--transition) !important;
}

[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus,
[data-testid="stDateInput"] input:focus {
    border-color: var(--accent-electric) !important;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.22) !important;
    outline: none !important;
    background-color: rgba(15, 23, 42, 0.95) !important;
}

/* BaseWeb Selectbox */
[data-baseweb="select"] > div {
    background-color: rgba(11, 16, 32, 0.85) !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: var(--radius-md) !important;
    color: #F8FAFC !important;
    transition: var(--transition) !important;
}

[data-baseweb="select"] > div:hover {
    border-color: rgba(255, 255, 255, 0.22) !important;
}

[data-baseweb="popover"], [data-baseweb="menu"] {
    background-color: #0F172A !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: var(--radius-md) !important;
    box-shadow: 0 12px 32px rgba(0, 0, 0, 0.6) !important;
}

[data-baseweb="menu"] [role="option"] {
    color: #E2E8F0 !important;
}

[data-baseweb="menu"] [role="option"][aria-selected="true"] {
    background-color: rgba(37, 99, 235, 0.25) !important;
    color: #93C5FD !important;
}

/* Generate Button - Primary Glow */
[data-testid="stButton"] button[kind="primary"],
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #2563EB 0%, #7C3AED 100%) !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    border-radius: var(--radius-md) !important;
    color: #FFFFFF !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.03em !important;
    padding: 0.75rem 1.4rem !important;
    box-shadow: 0 4px 20px rgba(37, 99, 235, 0.38), 0 0 12px rgba(124, 58, 237, 0.2) !important;
    transition: var(--transition) !important;
}

[data-testid="stButton"] button[kind="primary"]:hover,
.stButton > button[kind="primary"]:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 28px rgba(37, 99, 235, 0.55), 0 0 18px rgba(124, 58, 237, 0.35) !important;
    border-color: rgba(255, 255, 255, 0.35) !important;
}

/* Secondary Buttons */
[data-testid="stButton"] button[kind="secondary"],
.stButton > button:not([kind="primary"]) {
    background: rgba(17, 24, 39, 0.8) !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: var(--radius-md) !important;
    color: #E2E8F0 !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    transition: var(--transition) !important;
}

[data-testid="stButton"] button:not([kind="primary"]):hover {
    background: rgba(30, 41, 59, 0.9) !important;
    border-color: rgba(255, 255, 255, 0.25) !important;
    color: #FFFFFF !important;
    transform: translateY(-1px) !important;
}

/* ==============================================================================
   6. DOCUMENT PREVIEW & DIGITAL PAPER SURFACE
   ============================================================================== */
.preview-header-wrap {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1.1rem;
    padding-bottom: 0.9rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.preview-status-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.28rem 0.75rem;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}

.preview-status-pill.ready {
    background: rgba(56, 189, 248, 0.12);
    border: 1px solid rgba(56, 189, 248, 0.3);
    color: #38BDF8;
}

.preview-status-pill.drafted {
    background: rgba(16, 185, 129, 0.12);
    border: 1px solid rgba(16, 185, 129, 0.3);
    color: #34D399;
}

/* Empty State */
.preview-empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 3.8rem 2rem;
    text-align: center;
    background: rgba(11, 16, 32, 0.4);
    border: 1px dashed rgba(255, 255, 255, 0.12);
    border-radius: var(--radius-lg);
}

.empty-icon-wrap {
    width: 64px;
    height: 64px;
    border-radius: 16px;
    background: rgba(37, 99, 235, 0.1);
    border: 1px solid rgba(59, 130, 246, 0.25);
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 1.2rem;
    box-shadow: 0 0 20px rgba(37, 99, 235, 0.15);
}

.empty-title {
    font-size: 1.15rem !important;
    font-weight: 600 !important;
    color: #F8FAFC !important;
    margin-bottom: 0.45rem !important;
}

.empty-desc {
    font-size: 0.85rem;
    color: var(--text-secondary);
    max-width: 380px;
    line-height: 1.5;
    margin-bottom: 1.5rem;
}

.empty-chips-wrap {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 0.5rem;
}

.empty-chip {
    font-size: 0.72rem;
    color: var(--text-secondary);
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.08);
    padding: 0.25rem 0.65rem;
    border-radius: 999px;
}

/* Document Metadata Bar */
.doc-meta-strip {
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 0.6rem;
    background: rgba(11, 16, 32, 0.6);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: var(--radius-md);
    padding: 0.55rem 0.9rem;
    margin-bottom: 1.2rem;
}

.meta-chip {
    font-size: 0.72rem;
    font-weight: 500;
    color: var(--text-secondary);
    display: flex;
    align-items: center;
    gap: 0.35rem;
}

.meta-chip strong {
    color: #F8FAFC;
    font-weight: 600;
}

/* Warm Ivory Digital Paper */
.legal-parchment {
    background: #FAF9F6 !important;
    border: 1px solid #E2DCD5 !important;
    border-radius: var(--radius-md) !important;
    box-shadow: 0 10px 35px -5px rgba(0, 0, 0, 0.5), inset 0 0 0 1px rgba(255, 255, 255, 0.6) !important;
    padding: 2.8rem 3.2rem !important;
    margin-bottom: 1.4rem !important;
    position: relative !important;
    font-family: 'Newsreader', Georgia, 'Times New Roman', serif !important;
    color: #0F172A !important;
    line-height: 1.75 !important;
}

.legal-ribbon {
    position: absolute;
    top: 16px;
    right: 20px;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.62rem !important;
    font-weight: 700 !important;
    color: #64748B !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
}

.legal-doc-title {
    font-family: 'Cinzel', Georgia, serif !important;
    font-size: 1.55rem !important;
    font-weight: 700 !important;
    text-align: center !important;
    color: #0F172A !important;
    border-bottom: 2px solid #CBD5E1 !important;
    padding-bottom: 0.9rem !important;
    margin-bottom: 1.8rem !important;
    letter-spacing: 0.04em !important;
}

.legal-section-heading {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 700 !important;
    color: #1E3A8A !important;
    margin-top: 1.6rem !important;
    margin-bottom: 0.5rem !important;
    letter-spacing: 0.04em !important;
    text-transform: uppercase !important;
}

.legal-paragraph {
    font-size: 0.95rem !important;
    color: #1E293B !important;
    margin-bottom: 0.9rem !important;
    text-align: justify !important;
}

.legal-bullet {
    font-size: 0.92rem !important;
    color: #1E293B !important;
    margin-left: 1.6rem !important;
    margin-bottom: 0.45rem !important;
}

.legal-signature-line {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.86rem !important;
    color: #0F172A !important;
    margin-top: 0.85rem !important;
    font-weight: 600 !important;
}

.legal-spacer {
    height: 0.85rem !important;
}

.legal-disclaimer-box {
    margin-top: 2rem !important;
    padding: 0.85rem 1rem !important;
    background-color: #F1F5F9 !important;
    border-left: 3px solid #64748B !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.78rem !important;
    color: #475569 !important;
    font-style: italic !important;
}

/* ==============================================================================
   7. EXPORT CONTROLS SECTION
   ============================================================================== */
.export-card-wrap {
    background: rgba(11, 16, 32, 0.7);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: var(--radius-md);
    padding: 1.2rem 1.4rem;
    margin-top: 1.4rem;
}

.export-title {
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--accent-cyan-glow);
    margin-bottom: 0.2rem;
}

.export-subtitle {
    font-size: 0.8rem;
    color: var(--text-muted);
    margin-bottom: 0.9rem;
}

/* Download Button Enhancements */
[data-testid="stDownloadButton"] button {
    background: rgba(15, 23, 42, 0.8) !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: var(--radius-md) !important;
    color: #F8FAFC !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    padding: 0.65rem 1rem !important;
    transition: var(--transition) !important;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.25) !important;
}

[data-testid="stDownloadButton"] button:hover {
    border-color: rgba(56, 189, 248, 0.5) !important;
    background: rgba(30, 41, 59, 0.9) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 16px rgba(56, 189, 248, 0.2) !important;
}

/* Emphasized PDF download button */
.export-pdf-btn [data-testid="stDownloadButton"] button {
    background: linear-gradient(135deg, rgba(37, 99, 235, 0.3) 0%, rgba(124, 58, 237, 0.3) 100%) !important;
    border-color: rgba(96, 165, 250, 0.45) !important;
    box-shadow: 0 0 16px rgba(59, 130, 246, 0.25) !important;
    color: #FFFFFF !important;
}

.export-pdf-btn [data-testid="stDownloadButton"] button:hover {
    border-color: #60A5FA !important;
    box-shadow: 0 0 24px rgba(59, 130, 246, 0.45) !important;
}

/* ==============================================================================
   8. LEGAL SAFETY NOTICE (MUTED AMBER)
   ============================================================================== */
.legal-notice-card {
    display: flex;
    align-items: flex-start;
    gap: 0.85rem;
    background: rgba(245, 158, 11, 0.05);
    border: 1px solid rgba(245, 158, 11, 0.22);
    border-left: 3px solid #F59E0B;
    border-radius: var(--radius-md);
    padding: 0.85rem 1.1rem;
    margin-top: 1.4rem;
}

.notice-icon {
    font-size: 1.1rem;
    line-height: 1.2;
    color: #FBBF24;
}

.notice-title {
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    color: #FBBF24;
    text-transform: uppercase;
    margin-bottom: 0.2rem;
}

.notice-text {
    font-size: 0.78rem;
    color: #D1D5DB;
    line-height: 1.45;
}

/* ==============================================================================
   9. SIDEBAR STYLING
   ============================================================================== */
[data-testid="stSidebar"] {
    background-color: var(--bg-secondary) !important;
    border-right: 1px solid var(--card-border) !important;
}

.sidebar-brand-lockup {
    display: flex;
    align-items: center;
    gap: 0.85rem;
    padding-bottom: 1.2rem;
    margin-bottom: 1.3rem;
    border-bottom: 1px solid var(--card-border);
}

.sidebar-logo-box {
    width: 38px;
    height: 38px;
    border-radius: 9px;
    background: linear-gradient(135deg, rgba(37, 99, 235, 0.3), rgba(124, 58, 237, 0.3));
    border: 1px solid rgba(59, 130, 246, 0.35);
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    box-shadow: 0 0 12px rgba(59, 130, 246, 0.2);
}

.sidebar-brand-name {
    font-size: 1.15rem;
    font-weight: 700;
    color: #F8FAFC;
    line-height: 1.1;
}

.sidebar-brand-sub {
    font-size: 0.6rem;
    font-weight: 600;
    letter-spacing: 0.14em;
    color: var(--accent-cyan-glow);
    text-transform: uppercase;
}

/* Navigation items in sidebar */
.sidebar-nav-group {
    display: flex;
    flex-direction: column;
    gap: 0.35rem;
    margin-bottom: 1.4rem;
}

.sidebar-nav-chip {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    padding: 0.5rem 0.8rem;
    border-radius: var(--radius-sm);
    font-size: 0.82rem;
    font-weight: 500;
    color: var(--text-secondary);
    background: transparent;
    border: 1px solid transparent;
    transition: var(--transition);
}

.sidebar-nav-chip.active {
    background: rgba(37, 99, 235, 0.12);
    border-color: rgba(59, 130, 246, 0.25);
    color: #F8FAFC;
}

.sidebar-nav-chip:hover:not(.active) {
    background: rgba(255, 255, 255, 0.04);
    color: #F8FAFC;
}

/* Status Card */
.sidebar-status-card {
    background: rgba(11, 16, 32, 0.7);
    border: 1px solid var(--card-border);
    border-radius: var(--radius-md);
    padding: 0.85rem 1rem;
    margin-bottom: 1.4rem;
}

.sidebar-card-label {
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 0.6rem;
}

.status-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 0.78rem;
    margin-bottom: 0.4rem;
}

.status-row:last-child {
    margin-bottom: 0;
}

.status-label {
    color: var(--text-secondary);
}

.status-value {
    font-weight: 600;
    color: #F8FAFC;
    display: flex;
    align-items: center;
    gap: 0.35rem;
}

.status-value.connected {
    color: #34D399;
}

.status-value.engine {
    color: #93C5FD;
}

/* Supported Documents Badges */
.doc-chips-container {
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
    margin-bottom: 1.4rem;
}

.doc-chip-badge {
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.08);
    padding: 0.3rem 0.65rem;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 500;
    color: var(--text-secondary);
    transition: var(--transition);
}

.doc-chip-badge:hover {
    border-color: rgba(59, 130, 246, 0.35);
    color: #F8FAFC;
    background: rgba(37, 99, 235, 0.1);
}

/* Sidebar Footer */
.sidebar-footer {
    padding-top: 1.2rem;
    border-top: 1px solid var(--card-border);
    font-size: 0.68rem;
    color: var(--text-muted);
    line-height: 1.4;
}

/* ==============================================================================
   10. AI GENERATION ANIMATED LOADING STATE
   ============================================================================== */
.generating-card {
    background: rgba(15, 23, 42, 0.85);
    border: 1px solid rgba(59, 130, 246, 0.35);
    border-radius: var(--radius-lg);
    padding: 2.2rem 2.5rem;
    margin-top: 1.2rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 0 35px rgba(37, 99, 235, 0.22);
    text-align: center;
}

.generating-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: rgba(37, 99, 235, 0.2);
    border: 1px solid rgba(59, 130, 246, 0.4);
    padding: 0.3rem 0.85rem;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 700;
    color: #60A5FA;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 0.9rem;
}

.generating-title {
    font-size: 1.3rem !important;
    font-weight: 700 !important;
    color: #F8FAFC !important;
    margin-bottom: 1.2rem !important;
}

.generating-bar-container {
    width: 100%;
    height: 4px;
    background: rgba(255, 255, 255, 0.08);
    border-radius: 999px;
    overflow: hidden;
    margin-bottom: 1.4rem;
    position: relative;
}

.generating-bar-progress {
    position: absolute;
    top: 0;
    left: 0;
    height: 100%;
    width: 45%;
    background: linear-gradient(90deg, #3B82F6, #8B5CF6, #06B6D4);
    border-radius: 999px;
    box-shadow: 0 0 12px #38BDF8;
    animation: barScan 1.6s infinite ease-in-out;
}

@keyframes barScan {
    0% { left: -45%; width: 45%; }
    50% { width: 60%; }
    100% { left: 100%; width: 45%; }
}

.generating-steps-grid {
    display: flex;
    justify-content: center;
    gap: 1.5rem;
    flex-wrap: wrap;
}

.generating-step-item {
    font-size: 0.75rem;
    color: var(--text-secondary);
    display: flex;
    align-items: center;
    gap: 0.4rem;
}

.generating-step-item .step-dot {
    width: 6px;
    height: 6px;
    background: #38BDF8;
    border-radius: 50%;
    box-shadow: 0 0 6px #38BDF8;
}

/* Edit Mode Box */
.edit-header-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: rgba(37, 99, 235, 0.1);
    border: 1px solid rgba(59, 130, 246, 0.25);
    border-radius: var(--radius-md);
    padding: 0.6rem 0.9rem;
    margin-bottom: 1rem;
}

.edit-badge {
    font-size: 0.72rem;
    font-weight: 700;
    color: #93C5FD;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

.edit-note {
    font-size: 0.75rem;
    color: var(--text-secondary);
}
</style>
"""


def apply_styles():
    """Apply the custom dark futuristic legal-tech CSS rules to Streamlit."""
    import streamlit as st
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
