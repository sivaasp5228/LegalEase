"""Streamlit frontend web application for LegalEase.

Redesigned into a modern, futuristic, premium AI legal-tech SaaS workspace:
- Top navigation with real-time system operational indicator
- Large hero banner with Gemini 1.5 Pro architecture badge
- Two-column workspace: left configurator panel & right document intelligence preview
- Polished field microcopy, step indicators, and glassmorphism styling
- Human-in-the-loop editing mode with save/cancel protection
- Dedicated export bar with TXT, DOCX, and emphasized PDF downloads
- Muted amber legal information notice
"""

import os
import sys
import datetime
import requests
import streamlit as st
from dotenv import load_dotenv

# Ensure local frontend directory and repository root are in sys.path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))

if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# Local imports as required to preserve exact module import architecture
from styles import apply_styles
from components import (
    render_top_navigation,
    render_hero,
    render_sidebar,
    render_step_indicator,
    render_empty_preview,
    render_document_metadata,
    render_generating_indicator,
    render_legal_notice,
    render_download_controls,
)
from document_generator.html_preview import generate_html_preview

# Load environment configuration from project root .env
ENV_FILE = os.path.join(BASE_DIR, ".env")
load_dotenv(dotenv_path=ENV_FILE, override=True)
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000").rstrip("/")

# Page configuration
st.set_page_config(
    page_title="LegalEase — AI Legal Document Generator",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Apply futuristic dark design system
apply_styles()

# Render Top Navigation Bar & Sidebar
render_top_navigation(backend_url=BACKEND_URL)
api_key_override = render_sidebar(backend_url=BACKEND_URL)

# Render Hero Banner
render_hero()

# Initialize session state variables
if "generated_document" not in st.session_state:
    st.session_state.generated_document = ""
if "active_doc_type" not in st.session_state:
    st.session_state.active_doc_type = "Agreement"
if "active_effective_date" not in st.session_state:
    st.session_state.active_effective_date = str(datetime.date.today())
if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = False
if "edit_buffer" not in st.session_state:
    st.session_state.edit_buffer = ""

# Document Types Catalog
DOCUMENT_TYPES = [
    "Agreement",
    "Contract",
    "NDA",
    "Lease Agreement",
    "Employment Offer Letter",
]

# ==============================================================================
# MAIN TWO-COLUMN WORKSPACE
# ==============================================================================
col_config, col_preview = st.columns([5, 6], gap="large")

# ------------------------------------------------------------------------------
# LEFT PANEL: DOCUMENT CONFIGURATION
# ------------------------------------------------------------------------------
with col_config:
    st.markdown(
        """
        <div class="workspace-card">
            <div class="panel-eyebrow">CONFIGURATOR</div>
            <h2 class="panel-title">CREATE DOCUMENT</h2>
            <div class="panel-desc">Configure the legal instrument you want LegalEase to synthesize.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    render_step_indicator()

    # Inputs Container
    with st.container():
        doc_col, date_col = st.columns([1, 1])

        with doc_col:
            st.markdown('<div style="font-size:0.78rem; font-weight:600; letter-spacing:0.06em; color:#E2E8F0; text-transform:uppercase; margin-bottom:0.2rem;">DOCUMENT TYPE</div>', unsafe_allow_html=True)
            doc_type = st.selectbox(
                "Document Type",
                options=DOCUMENT_TYPES,
                index=0,
                label_visibility="collapsed",
                help="Select the legal instrument classification.",
            )
            st.markdown('<div class="field-microcopy">Choose the agreement you want to generate.</div>', unsafe_allow_html=True)

        with date_col:
            st.markdown('<div style="font-size:0.78rem; font-weight:600; letter-spacing:0.06em; color:#E2E8F0; text-transform:uppercase; margin-bottom:0.2rem;">EFFECTIVE DATE</div>', unsafe_allow_html=True)
            effective_date = st.date_input(
                "Effective Date",
                value=datetime.date.today(),
                format="YYYY/MM/DD",
                label_visibility="collapsed",
                help="The date this legal instrument takes effect.",
            )
            st.markdown('<div class="field-microcopy">The date this instrument takes legal effect.</div>', unsafe_allow_html=True)

        st.markdown('<div style="font-size:0.78rem; font-weight:600; letter-spacing:0.06em; color:#E2E8F0; text-transform:uppercase; margin-bottom:0.2rem;">PARTIES INVOLVED</div>', unsafe_allow_html=True)
        parties = st.text_area(
            "Parties Involved",
            placeholder="E.g., Alpha Tech Solutions LLC (Disclosing Party) and Beta Dynamics Corp (Receiving Party)...",
            height=95,
            label_visibility="collapsed",
            help="Specify entity names, addresses, and signatory roles.",
        )
        st.markdown('<div class="field-microcopy">Identify the individuals or organizations involved.</div>', unsafe_allow_html=True)

        st.markdown('<div style="font-size:0.78rem; font-weight:600; letter-spacing:0.06em; color:#E2E8F0; text-transform:uppercase; margin-bottom:0.2rem;">TERMS & CONDITIONS</div>', unsafe_allow_html=True)
        terms = st.text_area(
            "Terms & Conditions",
            placeholder="E.g., Mutual confidentiality covering source code and proprietary algorithms for 3 years; Net 30 payment terms; Delaware governing law...",
            height=130,
            label_visibility="collapsed",
            help="Specify key covenants, deliverables, compensation, duration, and obligations.",
        )
        st.markdown('<div class="field-microcopy">Add the important conditions, covenants, or operational clauses.</div>', unsafe_allow_html=True)

        # Primary Action Button
        generate_btn = st.button("✦ Generate Document", type="primary", use_container_width=True)

    # Generation Execution Handler
    if generate_btn:
        if not parties.strip():
            st.error("Please provide the parties involved before generating.")
        elif not terms.strip():
            st.error("Please provide the terms and conditions before generating.")
        else:
            with st.container():
                render_generating_indicator()
                payload = {
                    "document_type": doc_type,
                    "parties": parties.strip(),
                    "terms": terms.strip(),
                    "dates": str(effective_date),
                }
                if api_key_override:
                    payload["api_key"] = api_key_override

                try:
                    response = requests.post(
                        f"{BACKEND_URL}/generate",
                        json=payload,
                        timeout=60,
                    )
                    if response.status_code == 200:
                        data = response.json()
                        st.session_state.generated_document = data.get("content", "")
                        st.session_state.active_doc_type = doc_type
                        st.session_state.active_effective_date = str(effective_date)
                        st.session_state.edit_mode = False
                        st.session_state.edit_buffer = st.session_state.generated_document
                        st.rerun()
                    else:
                        error_detail = response.json().get("detail", response.text)
                        st.error(f"Generation failed ({response.status_code}): {error_detail}")
                except requests.exceptions.ConnectionError:
                    st.error(
                        f"Could not connect to FastAPI backend at {BACKEND_URL}. "
                        "Please ensure the backend is running via 'uvicorn app.backend.main:app --reload'."
                    )
                except Exception as ex:
                    st.error(f"An unexpected error occurred: {str(ex)}")

    # Legal Information Notice in configurator column
    render_legal_notice()

# ------------------------------------------------------------------------------
# RIGHT PANEL: DOCUMENT INTELLIGENCE PREVIEW
# ------------------------------------------------------------------------------
with col_preview:
    status_label = "● READY" if not st.session_state.generated_document else "● DRAFT READY"
    status_class = "ready" if not st.session_state.generated_document else "drafted"

    st.markdown(
        f"""
        <div class="preview-header-wrap">
            <div>
                <div class="panel-eyebrow">DOCUMENT INTELLIGENCE</div>
                <h2 class="panel-title" style="margin-bottom:0;">DOCUMENT PREVIEW</h2>
            </div>
            <span class="preview-status-pill {status_class}">{status_label}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not st.session_state.generated_document:
        render_empty_preview()
        render_download_controls(
            content="",
            doc_type=doc_type,
        )
    else:
        # Document Metadata Strip
        render_document_metadata(
            doc_type=st.session_state.active_doc_type,
            effective_date=st.session_state.active_effective_date,
            content=st.session_state.generated_document,
        )

        # Mode Action Switcher (View vs Edit)
        mode_col1, mode_col2 = st.columns([1, 1])
        with mode_col1:
            if not st.session_state.edit_mode:
                if st.button("✎ Edit Document", use_container_width=True):
                    st.session_state.edit_mode = True
                    st.session_state.edit_buffer = st.session_state.generated_document
                    st.rerun()
            else:
                st.caption("Active Mode: Direct Text Editing")

        with mode_col2:
            if st.session_state.edit_mode:
                if st.button("👁 View Formatted Preview", use_container_width=True):
                    st.session_state.edit_mode = False
                    st.rerun()

        # Render Content based on mode
        if st.session_state.edit_mode:
            st.markdown(
                """
                <div class="edit-header-bar">
                    <span class="edit-badge">EDITING DOCUMENT</span>
                    <span class="edit-note">Edit the drafted instrument text below.</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

            edited_text = st.text_area(
                "Document Editor",
                value=st.session_state.edit_buffer,
                height=480,
                label_visibility="collapsed",
                help="Make edits to your legal instrument. Click 'Save Changes' to update downloads.",
            )
            st.session_state.edit_buffer = edited_text

            save_col, cancel_col = st.columns([1, 1])
            with save_col:
                if st.button("✓ Save Changes", type="primary", use_container_width=True):
                    st.session_state.generated_document = st.session_state.edit_buffer
                    st.session_state.edit_mode = False
                    st.success("Changes saved successfully!")
                    st.rerun()
            with cancel_col:
                if st.button("✕ Cancel", use_container_width=True):
                    st.session_state.edit_buffer = st.session_state.generated_document
                    st.session_state.edit_mode = False
                    st.rerun()

        else:
            # Stylized Warm Ivory Legal Parchment Preview
            html_preview = generate_html_preview(st.session_state.generated_document)
            st.markdown(html_preview, unsafe_allow_html=True)

        # Dedicated Export Section
        render_download_controls(
            content=st.session_state.generated_document,
            doc_type=st.session_state.active_doc_type,
        )
