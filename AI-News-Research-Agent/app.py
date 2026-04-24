import sys
import os
import json
import time
import streamlit as st
from dotenv import load_dotenv

# Add this line to fix the Streamlit Cloud error:
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# Import our agents
from agents.research_agent import run_research_agent
# Add the current directory to sys.path so Streamlit Cloud can find the 'agents' and 'utils' folders
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our agents
from agents.research_agent import run_research_agent
from agents.filtering_agent import run_filtering_agent
from agents.summarizer_agent import run_summarizer_agent
from agents.analysis_agent import run_analysis_agent
from agents.insight_report_agent import run_insight_report_agent
from tools.catalog_tool import save_to_catalog

load_dotenv()

# ── Auto-load API keys (never shown to user) ──
GROQ_KEY = os.getenv("GROQ_API_KEY", "")
TAVILY_KEY = os.getenv("TAVILY_API_KEY", "")

# ── Page Config ──
st.set_page_config(page_title="AI News Research Agent", page_icon="📰", layout="wide", initial_sidebar_state="expanded")

# ── Premium CSS ──
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

:root {
    --primary: #7c3aed; --primary-light: #a78bfa; --primary-dark: #5b21b6;
    --accent: #06b6d4; --accent-light: #67e8f9;
    --success: #10b981; --warning: #f59e0b; --danger: #ef4444;
    --bg-dark: #0f0a1a; --bg-card: #1a1230; --bg-card-hover: #231a40;
    --text-primary: #f1f0f5; --text-secondary: #a09bb5; --text-muted: #6b6580;
    --border: rgba(124,58,237,0.15); --glow: rgba(124,58,237,0.25);
}

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* Hero Header */
.hero {
    background: linear-gradient(135deg, #7c3aed 0%, #2563eb 50%, #06b6d4 100%);
    padding: 2.5rem 3rem; border-radius: 20px; margin-bottom: 2rem;
    color: white; position: relative; overflow: hidden;
    box-shadow: 0 20px 60px rgba(124,58,237,0.3);
}
.hero::before {
    content: ''; position: absolute; top: -50%; right: -20%; width: 400px; height: 400px;
    background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
    border-radius: 50%;
}
.hero h1 { margin:0; font-size:2.4rem; font-weight:900; letter-spacing:-0.03em; position:relative; }
.hero p { margin:0.5rem 0 0; opacity:0.85; font-size:1rem; font-weight:400; position:relative; }
.hero .badge {
    display:inline-block; background:rgba(255,255,255,0.15); backdrop-filter:blur(10px);
    padding:0.3rem 0.8rem; border-radius:50px; font-size:0.75rem; font-weight:600;
    margin-top:0.8rem; border:1px solid rgba(255,255,255,0.2); position:relative;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f0a1a 0%, #1a1040 50%, #0f0a1a 100%);
}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { color: var(--text-secondary); }

/* Pipeline Steps */
.pipe-step {
    display:flex; align-items:center; gap:0.8rem; padding:0.7rem 1rem;
    border-radius:12px; margin:0.4rem 0; font-size:0.9rem; color:var(--text-secondary);
    transition: all 0.3s ease;
}
.pipe-step .num {
    width:28px; height:28px; border-radius:50%; display:flex; align-items:center; justify-content:center;
    font-weight:700; font-size:0.8rem; border:2px solid var(--border); color:var(--text-muted);
    flex-shrink:0;
}
.pipe-step.active { background:rgba(124,58,237,0.1); border-left:3px solid var(--primary); }
.pipe-step.active .num { background:var(--primary); color:#fff; border-color:var(--primary); }
.pipe-step.done { background:rgba(16,185,129,0.08); border-left:3px solid var(--success); }
.pipe-step.done .num { background:var(--success); color:#fff; border-color:var(--success); }

/* Glow button override */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, var(--primary) 0%, #2563eb 100%) !important;
    border: none !important; font-weight: 700 !important; letter-spacing: 0.02em !important;
    box-shadow: 0 8px 30px rgba(124,58,237,0.35) !important;
    transition: all 0.3s ease !important;
}
.stButton > button[kind="primary"]:hover {
    box-shadow: 0 12px 40px rgba(124,58,237,0.5) !important;
    transform: translateY(-1px) !important;
}

/* Hide streamlit chrome */
#MainMenu {visibility:hidden;} footer {visibility:hidden;} header {visibility:hidden;}
</style>
""", unsafe_allow_html=True)

# ── Hero Header ──
st.markdown("""
<div class="hero">
    <h1>📰 AI News Research Agent</h1>
    <p>A multi-agent system that deeply researches, filters, summarizes, and analyzes any topic you throw at it.</p>
    <span class="badge">✨ Powered by Groq &amp; Tavily Search</span>
</div>
""", unsafe_allow_html=True)

# ── Sidebar ──
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    st.markdown("---")

    model_name = st.selectbox(
        "🧠 Model",
        ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"],
        index=0,
        help="Using the default Groq models configured in your environment.",
    )

    st.markdown("---")
    st.markdown("### 🤖 Agent Pipeline")
    agents_info = [
        ("1", "🔍", "Research Agent"),
        ("2", "🧹", "Filtering Agent"),
        ("3", "📝", "Summarizer Agent"),
        ("4", "📈", "Analysis Agent"),
        ("5", "📰", "Insight / Report Agent"),
    ]
    for num, icon, name in agents_info:
        st.markdown(f'<div class="pipe-step"><span class="num">{num}</span>{icon} {name}</div>', unsafe_allow_html=True)

    st.markdown("---")
    # API status indicator
    if GROQ_KEY and TAVILY_KEY:
        st.success("✅ API keys loaded from environment")
    else:
        missing = []
        if not GROQ_KEY: missing.append("GROQ_API_KEY")
        if not TAVILY_KEY: missing.append("TAVILY_API_KEY")
        st.error(f"❌ Missing in .env: {', '.join(missing)}")

# ── Main Input ──
col1, col2 = st.columns([2, 1])
with col1:
    topic = st.text_input("🎯 Research Topic", value="The state of Quantum Computing in 2024",
        placeholder="e.g., SpaceX Starship updates, AI advancements, Economic outlook...")
with col2:
    depth = st.selectbox("🕵️‍♂️ Research Depth",
        ["Standard", "Deep Dive"], index=0, help="Currently Standard depth is implemented.")

st.markdown("")
run_btn = st.button("🚀 Start Research Pipeline", type="primary", use_container_width=True)

# ── Pipeline Execution ──
if run_btn:
    if not GROQ_KEY or not TAVILY_KEY:
        st.error("⚠️ API keys missing. Add GROQ_API_KEY and TAVILY_API_KEY to your .env file.")
        st.stop()

    research_data = filtered_data = summaries = analysis = final_report = None

    # Step 1
    with st.status("🔍 Research Agent...", expanded=True) as s:
        st.write("Scouring the web for raw articles via Tavily & formatting with Groq...")
        t0 = time.time()
        try:
            research_data = run_research_agent(topic)
            if "error" in research_data:
                raise Exception(research_data["error"])
                
            raw_tavily = research_data.get("raw_data", {}).get("results", [])
            save_to_catalog(raw_tavily, topic)
            grok_formatted = research_data.get("grok_formatted", "")
            
            s.update(label=f"✅ Research Agent ({time.time()-t0:.1f}s)", state="complete")
            st.markdown("### Raw Results Snippet")
            st.markdown(grok_formatted[:500] + "...\n*(truncated)*")
        except Exception as e:
            s.update(label="❌ Research Agent Failed", state="error"); st.error(str(e)); st.stop()

    # Step 2
    with st.status("🧹 Filtering Agent...", expanded=False) as s:
        st.write("Removing duplicates and low-quality sources...")
        t0 = time.time()
        try:
            filtered_data = run_filtering_agent(grok_formatted)
            if not filtered_data or "error" in filtered_data:
                st.warning("Groq failed to return clean JSON, falling back to raw Tavily data.")
                filtered_data = raw_tavily
                
            s.update(label=f"✅ Filtering Agent ({time.time()-t0:.1f}s)", state="complete")
            st.json(filtered_data)
        except Exception as e:
            s.update(label="❌ Filtering Agent Failed", state="error"); st.error(str(e)); st.stop()

    # Step 3
    with st.status("📝 Summarizer Agent...", expanded=False) as s:
        st.write("Condensing the best articles into concise summaries...")
        t0 = time.time()
        try:
            summaries = run_summarizer_agent(filtered_data)
            s.update(label=f"✅ Summarizer Agent ({time.time()-t0:.1f}s)", state="complete")
            st.markdown(summaries)
        except Exception as e:
            s.update(label="❌ Summarizer Agent Failed", state="error"); st.error(str(e)); st.stop()

    # Step 4
    with st.status("📈 Analysis Agent...", expanded=False) as s:
        st.write("Identifying trends, narratives, and contradictions...")
        t0 = time.time()
        try:
            analysis = run_analysis_agent(summaries)
            s.update(label=f"✅ Analysis Agent ({time.time()-t0:.1f}s)", state="complete")
            st.markdown(analysis)
        except Exception as e:
            s.update(label="❌ Analysis Agent Failed", state="error"); st.error(str(e)); st.stop()

    # Step 5
    with st.status("📰 Insight / Report Agent...", expanded=True) as s:
        st.write("Drafting the final comprehensive report...")
        t0 = time.time()
        try:
            final_report = run_insight_report_agent(analysis, summaries)
            s.update(label=f"✅ Report Agent ({time.time()-t0:.1f}s)", state="complete")
            st.markdown("*(Report generated successfully! View below)*")
        except Exception as e:
            s.update(label="❌ Report Agent Failed", state="error"); st.error(str(e)); st.stop()

    # ── Results Dashboard ──
    st.markdown("---")
    st.markdown("## 📊 Research Results Dashboard")

    # Expandable sections
    with st.expander("🔍 Filtered Data & Summaries", expanded=False):
        st.markdown("### Summaries")
        st.markdown(summaries)
        st.markdown("---")
        st.markdown("### Structured Data")
        st.json(filtered_data)

    with st.expander("📈 Deep Analysis", expanded=False):
        st.markdown(analysis)

    with st.expander("📰 Final Comprehensive Report", expanded=True):
        st.markdown(final_report)

    # Download
    st.markdown("---")
    
    d1, d2 = st.columns(2)
    with d1:
        st.download_button("📥 Download Final Report (Markdown)", final_report,
            f"research_report_{topic.replace(' ', '_')}.md", "text/markdown", use_container_width=True)
    with d2:
        # Provide the raw JSON of the filtered data
        json_out = json.dumps(filtered_data, indent=2)
        st.download_button("📥 Download Filtered Articles (JSON)", json_out,
            f"filtered_articles_{topic.replace(' ', '_')}.json", "application/json", use_container_width=True)

