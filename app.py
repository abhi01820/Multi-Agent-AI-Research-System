import streamlit as st
import time
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain
from fpdf import FPDF
import base64

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Abhi's AI Research Lab",
    page_icon="🧬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==========================================
# CUSTOM CSS (Premium Dark Theme & Glassmorphism)
# ==========================================
def inject_custom_css():
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;700;800&display=swap');

            /* Global Background & Font */
            .stApp {
                background: linear-gradient(-45deg, #0f172a, #020617, #1e1b4b, #0f172a);
                background-size: 400% 400%;
                animation: gradientBG 15s ease infinite;
                color: #f8fafc;
                font-family: 'Outfit', sans-serif !important;
            }
            
            /* Apply Font globally */
            * {
                font-family: 'Outfit', sans-serif !important;
            }

            @keyframes gradientBG {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }
            
            /* Hide Sidebar and Streamlit Menu */
            [data-testid="collapsedControl"] { display: none; }
            #MainMenu {visibility: hidden;}
            header {visibility: hidden;}
            footer {visibility: hidden;}

            /* Floating Orbs (Background Decoration) */
            .orb1, .orb2 {
                position: fixed;
                border-radius: 50%;
                filter: blur(100px);
                z-index: -1;
                opacity: 0.5;
            }
            .orb1 {
                top: -10%;
                left: -10%;
                width: 40vw;
                height: 40vw;
                background: rgba(56, 189, 248, 0.3);
                animation: floatOrb 20s infinite alternate;
            }
            .orb2 {
                bottom: -10%;
                right: -10%;
                width: 50vw;
                height: 50vw;
                background: rgba(139, 92, 246, 0.2);
                animation: floatOrb2 25s infinite alternate-reverse;
            }

            @keyframes floatOrb {
                0% { transform: translate(0, 0) scale(1); }
                100% { transform: translate(10vw, 10vh) scale(1.2); }
            }
            @keyframes floatOrb2 {
                0% { transform: translate(0, 0) scale(1); }
                100% { transform: translate(-10vw, -10vh) scale(1.1); }
            }

            /* Hero Typography */
            .hero-title {
                font-size: 4rem;
                font-weight: 800;
                background: linear-gradient(to right, #38bdf8 0%, #8b5cf6 50%, #d946ef 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                text-align: center;
                margin-bottom: 5px;
                animation: fadeInDown 1.2s cubic-bezier(0.2, 0.8, 0.2, 1);
                letter-spacing: -1px;
            }
            .hero-subtitle {
                font-size: 1.3rem;
                color: #94a3b8;
                text-align: center;
                margin-top: 0px;
                margin-bottom: 50px;
                font-weight: 400;
                animation: fadeInUp 1.2s cubic-bezier(0.2, 0.8, 0.2, 1);
            }

            /* Animations */
            @keyframes fadeInDown {
                from { opacity: 0; transform: translateY(-30px); }
                to { opacity: 1; transform: translateY(0); }
            }
            @keyframes fadeInUp {
                from { opacity: 0; transform: translateY(30px); }
                to { opacity: 1; transform: translateY(0); }
            }
            @keyframes pulseGlow {
                0% { box-shadow: 0 0 0 0 rgba(139, 92, 246, 0.4); }
                70% { box-shadow: 0 0 25px 15px rgba(139, 92, 246, 0); }
                100% { box-shadow: 0 0 0 0 rgba(139, 92, 246, 0); }
            }
            @keyframes slideIn {
                from { opacity: 0; transform: translateX(-20px); }
                to { opacity: 1; transform: translateX(0); }
            }

            /* Glassmorphism Cards */
            .glass-card {
                background: rgba(15, 23, 42, 0.6);
                backdrop-filter: blur(20px);
                -webkit-backdrop-filter: blur(20px);
                border-radius: 20px;
                border: 1px solid rgba(255, 255, 255, 0.08);
                padding: 30px;
                margin-top: 30px;
                margin-bottom: 20px;
                box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255,255,255,0.1);
                animation: fadeInUp 1s cubic-bezier(0.2, 0.8, 0.2, 1);
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            }
            .glass-card:hover {
                transform: translateY(-2px);
                box-shadow: 0 15px 50px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255,255,255,0.1);
            }

            /* Input styling */
            .stTextInput > div > div > input {
                background: rgba(255, 255, 255, 0.03) !important;
                border: 1px solid rgba(255, 255, 255, 0.1) !important;
                color: #f8fafc !important;
                border-radius: 16px !important;
                padding: 18px 20px !important;
                font-size: 1.2rem !important;
                transition: all 0.4s cubic-bezier(0.2, 0.8, 0.2, 1);
                box-shadow: inset 0 2px 4px rgba(0,0,0,0.2);
            }
            .stTextInput > div > div > input:focus {
                background: rgba(255, 255, 255, 0.06) !important;
                border-color: #8b5cf6 !important;
                box-shadow: 0 0 20px rgba(139, 92, 246, 0.3), inset 0 2px 4px rgba(0,0,0,0.2) !important;
            }
            .stTextInput > div > div > input::placeholder {
                color: #64748b !important;
            }

            /* Button Styling */
            .stButton > button {
                width: 100%;
                background: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #ec4899 100%) !important;
                color: white !important;
                border: none !important;
                border-radius: 16px !important;
                padding: 14px 28px !important;
                font-weight: 700 !important;
                font-size: 1.2rem !important;
                letter-spacing: 0.5px !important;
                transition: all 0.3s cubic-bezier(0.2, 0.8, 0.2, 1) !important;
                animation: pulseGlow 3s infinite;
                position: relative;
                overflow: hidden;
            }
            .stButton > button::before {
                content: '';
                position: absolute;
                top: 0; left: -100%; width: 100%; height: 100%;
                background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
                transition: left 0.5s ease;
            }
            .stButton > button:hover::before {
                left: 100%;
            }
            .stButton > button:hover {
                transform: translateY(-3px) scale(1.02) !important;
                box-shadow: 0 10px 25px rgba(168, 85, 247, 0.5) !important;
            }

            /* Status Text */
            [data-testid="stStatusWidget"] {
                background: rgba(15, 23, 42, 0.5) !important;
                backdrop-filter: blur(12px) !important;
                border: 1px solid rgba(139, 92, 246, 0.3) !important;
                border-radius: 16px !important;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
            }
            
            /* Expanders */
            [data-testid="stExpander"] {
                background: rgba(255, 255, 255, 0.02) !important;
                border: 1px solid rgba(255, 255, 255, 0.05) !important;
                border-radius: 12px !important;
            }

            /* Download Buttons */
            .download-btn-container .stButton > button {
                background: rgba(255, 255, 255, 0.05) !important;
                border: 1px solid rgba(255, 255, 255, 0.1) !important;
                animation: none;
                font-size: 1rem !important;
                color: #e2e8f0 !important;
            }
            .download-btn-container .stButton > button:hover {
                background: rgba(255, 255, 255, 0.1) !important;
                border-color: #38bdf8 !important;
                box-shadow: 0 5px 15px rgba(56, 189, 248, 0.2) !important;
                transform: translateY(-2px) scale(1) !important;
            }

            /* Footer */
            .custom-footer {
                text-align: center;
                margin-top: 60px;
                padding-bottom: 30px;
                color: #64748b;
                font-size: 1rem;
                font-weight: 500;
            }
            .custom-footer span {
                color: #ec4899;
                display: inline-block;
                animation: pulse 2s infinite;
            }
            @keyframes pulse {
                0% { transform: scale(1); }
                50% { transform: scale(1.2); }
                100% { transform: scale(1); }
            }
        </style>
        
        <!-- Inject Background Orbs -->
        <div class="orb1"></div>
        <div class="orb2"></div>
    """, unsafe_allow_html=True)

# ==========================================
# HELPER FUNCTIONS
# ==========================================
def create_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    encoded_text = text.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 10, txt=encoded_text)
    return pdf.output(dest="S").encode("latin-1")

def stream_report(text):
    """Generator to simulate a typewriter effect for the final report"""
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.02)

# ==========================================
# MAIN APP
# ==========================================
def main():
    inject_custom_css()

    # Hero Section
    st.markdown("<h1 class='hero-title'>Abhi's AI Research Lab</h1>", unsafe_allow_html=True)
    st.markdown("<p class='hero-subtitle'>Experience the Next Generation of Autonomous AI Research</p>", unsafe_allow_html=True)

    # Input Section
    topic = st.text_input("Enter your research topic:", placeholder="e.g., The Future of Quantum Computing in 2030...", label_visibility="collapsed")
    
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        start_btn = st.button("✨ Initialize Research Intelligence")

    if start_btn and topic:
        state = {}
        st.markdown("<br><br>", unsafe_allow_html=True)

        import sys
        import io
        from pipeline import run_research_pipeline
        
        class StreamlitCatcher(io.StringIO):
            def __init__(self, status_widget):
                super().__init__()
                self.status_widget = status_widget
                self.current_step = 0

            def write(self, text):
                sys.__stdout__.write(text)
                sys.__stdout__.flush()
                
                lower_text = text.lower()
                if "step 1" in lower_text:
                    self.status_widget.update(label="🔍 **Abhi's Search Agent** is deeply scanning global networks...", state="running")
                    st.markdown("*Acquiring high-signal intelligence streams...*")
                elif "search result" in lower_text:
                    st.markdown("✅ *Search agent successfully searched the content!*")
                elif "step 2" in lower_text:
                    self.status_widget.update(label="📖 **Abhi's Reader Agent** is analyzing and extracting knowledge...", state="running")
                    st.markdown("*Parsing complex data structures...*")
                elif "scraped content:" in lower_text:
                    st.markdown("✅ *Reader agent successfully scraped the resources!*")
                elif "step 3" in lower_text:
                    self.status_widget.update(label="✍️ **Abhi's Writer Agent** is synthesizing the comprehensive report...", state="running")
                    st.markdown("*Crafting narrative and structuring insights...*")
                elif "final report" in lower_text:
                    st.markdown("✅ *Writer agent successfully generated the report!*")
                elif "step 4" in lower_text:
                    self.status_widget.update(label="🧐 **Abhi's Critic Agent** is performing rigorous quality assurance...", state="running")
                    st.markdown("*Polishing logic and refining accuracy...*")
                elif "critic report" in lower_text:
                    st.markdown("✅ *Critic agent successfully reviewed the content!*")

        with st.status("🚀 **Booting Abhi's AI Pipeline...**", expanded=True) as status:
            catcher = StreamlitCatcher(status)
            old_stdout = sys.stdout
            sys.stdout = catcher
            
            try:
                state = run_research_pipeline(topic)
                status.update(label="✨ Abhi's Research Intelligence has completed its task!", state="complete", expanded=False)
            except Exception as e:
                status.update(label=f"❌ Critical Failure: {str(e)}", state="error")
                st.stop()
            finally:
                sys.stdout = old_stdout

        # ---------------------------------------------------------
        # DISPLAY RESULTS (With Typewriter Effect)
        # ---------------------------------------------------------
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: #38bdf8; margin-bottom: 20px;'>📑 Final Intelligence Report</h2>", unsafe_allow_html=True)
        
        # Simulated Typewriter Effect
        report_container = st.empty()
        # Stream the report for an extraordinary AI feel
        st.write_stream(stream_report(state['report']))
        
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Expandable Sections
        col_exp1, col_exp2 = st.columns(2)
        with col_exp1:
            with st.expander("🛠️ View Critic's Feedback"):
                st.markdown(state["feedback"])
        with col_exp2:
            with st.expander("🌐 View Raw Search Data"):
                st.markdown(state["search_results"])
                st.markdown("---")
                st.markdown(state["scraped_content"])

        # Download Buttons
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='download-btn-container'>", unsafe_allow_html=True)
        dl_col1, dl_col2, dl_col3, dl_col4 = st.columns([1, 2, 2, 1])
        
        with dl_col2:
            st.download_button(
                label="📄 Download Markdown",
                data=state["report"],
                file_name="research_report.md",
                mime="text/markdown",
                use_container_width=True
            )
            
        with dl_col3:
            try:
                pdf_bytes = create_pdf(state["report"])
                st.download_button(
                    label="📕 Download PDF",
                    data=pdf_bytes,
                    file_name="research_report.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            except Exception as e:
                st.error("Could not generate PDF.")
        st.markdown("</div>", unsafe_allow_html=True)

    # Footer
    st.markdown("<div class='custom-footer'>Engineered with by Abhi <span>❤</span> </div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
