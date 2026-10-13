"""Reusable UI layout components for LegalEase Streamlit interface.

Implements the modern, futuristic, dark legal-tech SaaS visual identity:
- Top navigation bar with live status indicator
- Hero section with gradient typography and AI architecture badge
- Compact sidebar with system status, API configuration, and document chips
- Step indicator and field microcopy
- Empty preview state and document metadata chips
- Warm ivory legal parchment display container
- Dedicated export bar with TXT, DOCX, and PDF download buttons
- Subtle legal notice card with muted amber accent
"""

import os
import sys
import base64
import requests
import streamlit as st

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from document_generator.txt_generator import generate_txt
from document_generator.docx_generator import generate_docx
from document_generator.pdf_generator import generate_pdf


@st.cache_data
def get_logo_base64() -> str:
    """Load and cache the application logo as a base64 encoded string."""
    logo_path = os.path.join(BASE_DIR, "assets", "logo.png")
    if os.path.exists(logo_path):
        try:
            with open(logo_path, "rb") as f:
                return base64.b64encode(f.read()).decode("utf-8")
        except Exception:
            return ""
    return ""


def render_top_navigation(backend_url: str):
    """Render the sleek top navigation bar with brand lockup and live status."""
    logo_b64 = get_logo_base64()
    logo_img_tag = (
        f'<img src="data:image/png;base64,{logo_b64}" alt="LegalEase">'
        if logo_b64
        else '<span style="font-size:1.1rem; color:#60A5FA;">⚖</span>'
    )

    # Health check for live badge
    is_healthy = False
    gemini_configured = False
    try:
        r = requests.get(f"{backend_url}/health", timeout=1.5)
        if r.status_code == 200:
            is_healthy = True
            gemini_configured = r.json().get("gemini_configured", False)
    except Exception:
        is_healthy = False

    if is_healthy and gemini_configured:
        status_html = (
            '<div class="nav-status-pill">'
            '<span class="pulse-dot"></span>'
            '<span>SYSTEM OPERATIONAL</span>'
            '</div>'
        )
    elif is_healthy and not gemini_configured:
        status_html = (
            '<div class="nav-status-pill" style="background:rgba(245,158,11,0.12); border-color:rgba(245,158,11,0.3); color:#FBBF24;">'
            '<span style="width:7px; height:7px; background:#FBBF24; border-radius:50%; display:inline-block;"></span>'
            '<span>API KEY REQUIRED</span>'
            '</div>'
        )
    else:
        status_html = (
            '<div class="nav-status-pill" style="background:rgba(239,68,68,0.12); border-color:rgba(239,68,68,0.3); color:#F87171;">'
            '<span style="width:7px; height:7px; background:#EF4444; border-radius:50%; display:inline-block;"></span>'
            '<span>BACKEND OFFLINE</span>'
            '</div>'
        )

    st.markdown(
        f"""
        <div class="top-nav-container">
            <div class="nav-brand-group">
                <div class="nav-brand-logo">
                    {logo_img_tag}
                </div>
                <div class="nav-brand-text">
                    <span class="nav-brand-name">LegalEase</span>
                    <span class="nav-brand-badge">AI LEGAL INTELLIGENCE</span>
                </div>
            </div>
            <div class="nav-links-group">
                <span class="nav-item active">⬡ Workspace</span>
                <span class="nav-item">✧ Templates</span>
                <span class="nav-item">🗎 Documents</span>
                <span class="nav-item">ⓘ How It Works</span>
            </div>
            {status_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_hero():
    """Render the hero section with gradient typography and futuristic badge."""
    st.markdown(
        """
        <div class="hero-wrapper">
            <div class="hero-glow-orb"></div>
            <div class="hero-meta-badge">
                <span style="font-size:0.65rem;">●</span> GEMINI INTELLIGENCE ARCHITECTURE
            </div>
            <h1 class="hero-title">
                Legal documents.<br>
                <span class="hero-gradient-text">Generated intelligently.</span>
            </h1>
            <p class="hero-subtitle">
                Draft professional legal instruments in seconds with AI-powered document intelligence.
                Tailored clauses, standardized terminology, and multi-format export.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar(backend_url: str):
    """Render the redesigned futuristic sidebar with status and API configuration."""
    with st.sidebar:
        logo_b64 = get_logo_base64()
        logo_img_tag = (
            f'<img src="data:image/png;base64,{logo_b64}" alt="LegalEase">'
            if logo_b64
            else '<span style="font-size:1.2rem; color:#60A5FA;">⚖</span>'
        )

        st.markdown(
            f"""
            <div class="sidebar-brand-lockup">
                <div class="sidebar-logo-box">
                    {logo_img_tag}
                </div>
                <div>
                    <div class="sidebar-brand-name">LegalEase</div>
                    <div class="sidebar-brand-sub">AI LEGAL WORKSPACE</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Navigation Links
        st.markdown(
            """
            <div class="sidebar-nav-group">
                <div class="sidebar-nav-chip active">⬡ Workspace</div>
                <div class="sidebar-nav-chip">🗎 Documents</div>
                <div class="sidebar-nav-chip">✧ Templates</div>
                <div class="sidebar-nav-chip">ⓘ How It Works</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # System Status & Gemini Health
        is_connected = False
        gemini_configured = False
        display_model_name = "Gemini Flash Lite"
        try:
            r = requests.get(f"{backend_url}/health", timeout=1.5)
            if r.status_code == 200:
                is_connected = True
                data = r.json()
                gemini_configured = data.get("gemini_configured", False)
                raw_model = data.get("model_name", "")
                if raw_model:
                    display_model_name = raw_model.replace("models/", "").replace("-", " ").title()
        except Exception:
            is_connected = False
            gemini_configured = False

        conn_status_html = (
            '<span class="status-value connected"><span class="pulse-dot"></span> Connected</span>'
            if is_connected
            else '<span class="status-value" style="color:#F87171;">○ Disconnected</span>'
        )

        gemini_status_html = (
            '<span class="status-value connected"><span class="pulse-dot"></span> Configured</span>'
            if gemini_configured
            else '<span class="status-value" style="color:#FBBF24;">○ Not Configured</span>'
        )

        st.markdown(
            f"""
            <div class="sidebar-status-card">
                <div class="sidebar-card-label">SYSTEM STATUS</div>
                <div class="status-row">
                    <span class="status-label">Backend</span>
                    {conn_status_html}
                </div>
                <div class="status-row">
                    <span class="status-label">AI Engine</span>
                    <span class="status-value engine">{display_model_name}</span>
                </div>
                <div class="status-row">
                    <span class="status-label">Gemini API</span>
                    {gemini_status_html}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # API Configuration Status
        st.markdown(
            """
            <div class="sidebar-card-label" style="margin-top:1.2rem; margin-bottom:0.4rem;">API CONFIGURATION</div>
            """,
            unsafe_allow_html=True,
        )

        if gemini_configured:
            st.markdown(
                """
                <div style="background:rgba(16, 185, 129, 0.08); border:1px solid rgba(16, 185, 129, 0.25); border-radius:8px; padding:0.65rem 0.85rem; margin-bottom:0.8rem;">
                    <div style="font-size:0.75rem; font-weight:600; color:#34D399; display:flex; align-items:center; gap:0.4rem;">
                        <span class="pulse-dot"></span> Gemini API: Configured
                    </div>
                    <div style="font-size:0.68rem; color:#94A3B8; margin-top:0.25rem;">
                        Loaded securely via LegalEase/.env
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                """
                <div style="background:rgba(245, 158, 11, 0.08); border:1px solid rgba(245, 158, 11, 0.25); border-radius:8px; padding:0.65rem 0.85rem; margin-bottom:0.8rem;">
                    <div style="font-size:0.75rem; font-weight:600; color:#FBBF24;">
                        ○ Gemini API: Not Configured
                    </div>
                    <div style="font-size:0.68rem; color:#D1D5DB; margin-top:0.25rem; line-height:1.35;">
                        Configure <code>GEMINI_API_KEY</code> in <code>LegalEase/.env</code> to enable generation.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with st.expander("Session Override (Optional)", expanded=False):
            st.caption("Override .env for this session only:")
            key_override = st.text_input(
                "Gemini API Key Override",
                type="password",
                key="sidebar_gemini_key_override",
                placeholder="AIzaSy...",
                help="Optional override. Normal setup loads GEMINI_API_KEY from .env",
                label_visibility="collapsed",
            )

        # Supported Documents Chips
        st.markdown(
            """
            <div class="sidebar-card-label" style="margin-top:1.6rem; margin-bottom:0.6rem;">SUPPORTED DOCUMENTS</div>
            <div class="doc-chips-container">
                <span class="doc-chip-badge">Agreement</span>
                <span class="doc-chip-badge">Contract</span>
                <span class="doc-chip-badge">NDA</span>
                <span class="doc-chip-badge">Lease Agreement</span>
                <span class="doc-chip-badge">Employment Offer Letter</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Sidebar Footer
        st.markdown(
            """
            <div class="sidebar-footer">
                <strong>LegalEase</strong> &bull; AI-Powered Legal Document Generation<br>
                Empowering legal teams & founders with document intelligence.
            </div>
            """,
            unsafe_allow_html=True,
        )

        return key_override.strip() if key_override else None


def render_step_indicator():
    """Render the 3-step configurator indicator."""
    st.markdown(
        """
        <div class="step-indicator-wrap">
            <div class="step-pill active">
                <span class="step-num">01</span> DETAILS
            </div>
            <span class="step-sep">→</span>
            <div class="step-pill active">
                <span class="step-num">02</span> TERMS
            </div>
            <span class="step-sep">→</span>
            <div class="step-pill active">
                <span class="step-num">03</span> GENERATE
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_empty_preview():
    """Render an elegant empty state placeholder when no document is drafted yet."""
    st.markdown(
        """
        <div class="preview-empty-state">
            <div class="empty-icon-wrap">
                <svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="#38BDF8" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                    <polyline points="14 2 14 8 20 8"></polyline>
                    <line x1="16" y1="13" x2="8" y2="13"></line>
                    <line x1="16" y1="17" x2="8" y2="17"></line>
                    <line x1="10" y1="9" x2="8" y2="9"></line>
                </svg>
            </div>
            <h3 class="empty-title">Your legal document will appear here</h3>
            <p class="empty-desc">
                Configure the document details on the left and select <strong>✦ Generate Document</strong> to synthesize structured, enforceable legal clauses.
            </p>
            <div class="empty-chips-wrap">
                <span class="empty-chip">✦ Automated Clauses</span>
                <span class="empty-chip">✦ Terms Table Extraction</span>
                <span class="empty-chip">✦ Multi-Format Export</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_document_metadata(doc_type: str, effective_date: str, content: str):
    """Render metadata chips above the generated document."""
    word_count = len(content.split())
    st.markdown(
        f"""
        <div class="doc-meta-strip">
            <div class="meta-chip">
                <span>Type:</span> <strong>{doc_type}</strong>
            </div>
            <div class="meta-chip">
                <span>Effective:</span> <strong>{effective_date}</strong>
            </div>
            <div class="meta-chip">
                <span>Words:</span> <strong>~{word_count}</strong>
            </div>
            <div class="meta-chip">
                <span style="color:#34D399;">●</span> <strong>Gemini Synthesized</strong>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_generating_indicator():
    """Render a futuristic AI generation progress card while calling the model."""
    st.markdown(
        """
        <div class="generating-card">
            <div class="generating-badge">
                <span style="font-size:0.6rem;">●</span> SYNTHESIZING INSTRUMENT
            </div>
            <h3 class="generating-title">GENERATING LEGAL DOCUMENT</h3>
            <div class="generating-bar-container">
                <div class="generating-bar-progress"></div>
            </div>
            <div class="generating-steps-grid">
                <div class="generating-step-item">
                    <span class="step-dot"></span> Analyzing requirements
                </div>
                <div class="generating-step-item">
                    <span class="step-dot"></span> Structuring clauses
                </div>
                <div class="generating-step-item">
                    <span class="step-dot"></span> Gemini synthesis
                </div>
                <div class="generating-step-item">
                    <span class="step-dot"></span> Formatting document
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_legal_notice():
    """Render the subtle premium amber legal information notice card."""
    st.markdown(
        """
        <div class="legal-notice-card">
            <div class="notice-icon">⚖</div>
            <div>
                <div class="notice-title">LEGAL INFORMATION NOTICE</div>
                <div class="notice-text">
                    LegalEase generates AI-assisted legal content for informational and drafting assistance.
                    Review documents with a licensed legal professional before signing or relying on them.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_download_controls(content: str, doc_type: str):
    """Render dedicated export bar with TXT, DOCX, and emphasized PDF download buttons matching UI design."""
    st.markdown(
        """
        <div style="margin-top: 1.5rem; margin-bottom: 0.8rem;">
            <h3 style="font-size: 1.15rem; font-weight: 700; color: #F8FAFC; display: flex; align-items: center; gap: 0.5rem; margin: 0;">
                <span style="font-size: 1.25rem;">📥</span> Download Document
            </h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)
    safe_name = doc_type.lower().replace(" ", "_")
    export_content = content if content and content.strip() else f"## {doc_type}\n\n[LegalEase AI Document Template]\n\nConfigure document parameters in the Configurator and click 'Generate Document' to generate your customized legal clauses."

    with col1:
        txt_bytes = generate_txt(export_content)
        st.download_button(
            label="📄 Download as .TXT",
            data=txt_bytes,
            file_name=f"{safe_name}.txt",
            mime="text/plain",
            use_container_width=True,
            help="Clean, lightweight UTF-8 plain text file",
        )

    with col2:
        try:
            docx_bytes = generate_docx(export_content, title=doc_type.upper())
            st.download_button(
                label="📝 Download as .DOCX",
                data=docx_bytes,
                file_name=f"{safe_name}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True,
                help="Microsoft Word format with 1-inch margins and Times New Roman styling",
            )
        except Exception as e:
            st.error(f"DOCX preparation failed: {e}")

    with col3:
        try:
            pdf_bytes = generate_pdf(export_content, title=doc_type.upper())
            st.markdown('<div class="export-pdf-btn">', unsafe_allow_html=True)
            st.download_button(
                label="📕 Download as .PDF",
                data=pdf_bytes,
                file_name=f"{safe_name}.pdf",
                mime="application/pdf",
                use_container_width=True,
                help="Printable PDF with header, footer, pagination, and logo styling",
            )
            st.markdown('</div>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"PDF preparation failed: {e}")
