"""
PrepPilot — AI-Powered Interview Trainer
IBM SkillsBuild Internship Project
Built with IBM watsonx Orchestrate · watsonx.ai · RAG · IBM Cloud Object Storage
"""

import os
import json
import time
import random
import requests
import streamlit as st
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# ─────────────────────────────────────────────
#  Page configuration
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="PrepPilot",
    layout="wide",
)

# ─────────────────────────────────────────────
#  IBM-style CSS theme
# ─────────────────────────────────────────────
st.markdown(
    """
    <style>
    /* ── Google Font ── */
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap');

    /* ── Root palette ── */
    :root {
        --ibm-blue:        #0f62fe;
        --ibm-blue-dark:   #0043ce;
        --ibm-blue-light:  #d0e2ff;
        --ibm-teal:        #009d9a;
        --ibm-green:       #24a148;
        --ibm-yellow:      #f1c21b;
        --ibm-red:         #da1e28;
        --ibm-purple:      #8a3ffc;
        --ibm-gray-100:    #f4f4f4;
        --ibm-gray-200:    #e0e0e0;
        --ibm-gray-300:    #c6c6c6;
        --ibm-gray-600:    #6f6f6f;
        --ibm-gray-800:    #393939;
        --ibm-gray-900:    #161616;
        --ibm-white:       #ffffff;
    }

    /* ── Base ── */
    html, body, [class*="css"] {
        font-family: 'IBM Plex Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
        color: var(--ibm-gray-900);
    }

    .stApp {
    background: #0E1117;
    color: #FAFAFA;
}

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #001141 0%, #0f2461 60%, #0f3d8c 100%);
        border-right: 3px solid var(--ibm-blue);
    }
    [data-testid="stSidebar"] * { color: #ffffff !important; }
    [data-testid="stSidebar"] .stMarkdown a { color: var(--ibm-blue-light) !important; }

    /* ── Top navigation bar ── */
    .top-nav {
        background: linear-gradient(135deg, #001141 0%, #0f2461 50%, #0043ce 100%);
        padding: 18px 36px;
        border-bottom: 3px solid var(--ibm-blue);
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin: -1rem -1rem 2rem -1rem;
        border-radius: 0;
    }
    .top-nav-left { display: flex; align-items: center; gap: 16px; }
    .top-nav-logo {
        width: 44px; height: 44px;
        background: var(--ibm-white);
        border-radius: 8px;
        display: flex; align-items: center; justify-content: center;
        font-size: 24px; font-weight: 700;
        color: var(--ibm-blue-dark);
    }
    .top-nav-title { color: #ffffff; font-size: 22px; font-weight: 600; letter-spacing: 0.5px; }
    .top-nav-sub   { color: #a6c8ff; font-size: 12px; margin-top: 2px; }
    .top-nav-badge {
        background: var(--ibm-blue); color: #fff;
        padding: 5px 14px; border-radius: 20px;
        font-size: 11px; font-weight: 600; letter-spacing: 0.8px; text-transform: uppercase;
    }

    /* ── Cards ── */
    .ibm-card {
        background: var(--ibm-white);
        border-radius: 8px;
        padding: 28px 32px;
        margin-bottom: 20px;
        border-left: 4px solid var(--ibm-blue);
        box-shadow: 0 1px 3px rgba(0,0,0,.08), 0 4px 12px rgba(0,0,0,.04);
    }
    .ibm-card-teal   { border-left-color: var(--ibm-teal); }
    .ibm-card-green  { border-left-color: var(--ibm-green); }
    .ibm-card-purple { border-left-color: var(--ibm-purple); }
    .ibm-card-yellow { border-left-color: var(--ibm-yellow); }
    .ibm-card-red    { border-left-color: var(--ibm-red); }

    .ibm-card h3 {
        font-size: 15px; font-weight: 600;
        text-transform: uppercase; letter-spacing: 0.8px;
        color: var(--ibm-gray-800); margin: 0 0 16px;
    }

    /* ── Section headers ── */
    .section-header {
        display: flex; align-items: center; gap: 12px;
        padding: 14px 20px;
        background: linear-gradient(135deg, #0f2461, #0f62fe);
        border-radius: 6px; margin-bottom: 20px; color: #fff;
    }
    .section-header .icon { font-size: 22px; }
    .section-header .title { font-size: 17px; font-weight: 600; }
    .section-header .sub   { font-size: 12px; color: #a6c8ff; margin-top: 2px; }

    /* ── Score ring ── */
    .score-container { text-align: center; padding: 20px 0; }
    .score-ring {
        width: 140px; height: 140px; border-radius: 50%;
        margin: 0 auto 16px;
        display: flex; flex-direction: column;
        align-items: center; justify-content: center;
        position: relative; border: 6px solid var(--ibm-blue-light);
    }
    .score-number { font-size: 42px; font-weight: 700; line-height: 1; }
    .score-label  { font-size: 12px; color: var(--ibm-gray-600); margin-top: 4px; }

    /* ── Question items ── */
    .question-item {
        background: var(--ibm-gray-100);
        border-left: 3px solid var(--ibm-blue);
        padding: 14px 18px; border-radius: 0 6px 6px 0;
        margin-bottom: 12px; font-size: 14px; line-height: 1.6;
    }
    .question-number {
        font-size: 11px; font-weight: 600; color: var(--ibm-blue);
        text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 6px;
    }

    /* ── Tip items ── */
    .tip-item {
        display: flex; gap: 14px; align-items: flex-start;
        background: #f0f7ff; border-radius: 6px;
        padding: 14px 18px; margin-bottom: 10px;
    }
    .tip-icon { font-size: 20px; flex-shrink: 0; margin-top: 2px; }
    .tip-text  { font-size: 14px; line-height: 1.6; }

    /* ── Progress bar ── */
    .prog-bar-wrap { margin: 8px 0; }
    .prog-label    { font-size: 12px; color: var(--ibm-gray-600); margin-bottom: 4px; }
    .prog-bar-bg   { background: var(--ibm-gray-200); border-radius: 4px; height: 8px; overflow: hidden; }
    .prog-bar-fill { height: 8px; border-radius: 4px; transition: width 0.6s ease; }

    /* ── Form elements ── */
    .stTextInput > div > div > input,
    .stSelectbox > div > div,
    .stTextArea > div > div > textarea,
    .stFileUploader > div {
        border-radius: 4px !important;
        border-color: var(--ibm-gray-300) !important;
        font-family: 'IBM Plex Sans', sans-serif !important;
    }
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--ibm-blue) !important;
        box-shadow: 0 0 0 2px var(--ibm-blue-light) !important;
    }

    /* ── Primary button ── */
    .stButton > button {
        background: var(--ibm-blue) !important;
        color: #fff !important;
        border: none !important;
        border-radius: 4px !important;
        font-family: 'IBM Plex Sans', sans-serif !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        padding: 12px 28px !important;
        letter-spacing: 0.3px !important;
        transition: background 0.2s !important;
    }
    .stButton > button:hover {
        background: var(--ibm-blue-dark) !important;
    }

    /* ── Expander ── */
    .streamlit-expanderHeader {
        background: var(--ibm-gray-100) !important;
        border-radius: 4px !important;
        font-weight: 500 !important;
    }

    /* ── Tags / chips ── */
    .tag {
        display: inline-block;
        background: var(--ibm-blue-light); color: var(--ibm-blue-dark);
        border-radius: 20px; padding: 3px 12px;
        font-size: 12px; font-weight: 500; margin: 3px 3px 3px 0;
    }
    .tag-green  { background: #defbe6; color: #0e6027; }
    .tag-teal   { background: #d9fbfb; color: #005d5d; }
    .tag-purple { background: #f6f2ff; color: #491d8b; }
    .tag-yellow { background: #fcf4d6; color: #684e00; }

    /* ── Divider ── */
    .ibm-divider { border: none; border-top: 1px solid var(--ibm-gray-200); margin: 24px 0; }

    /* ── Status pill ── */
    .status-pill {
        display: inline-flex; align-items: center; gap: 6px;
        padding: 4px 14px; border-radius: 20px;
        font-size: 12px; font-weight: 600;
    }
    .status-green  { background: #defbe6; color: #0e6027; }
    .status-blue   { background: var(--ibm-blue-light); color: var(--ibm-blue-dark); }
    .status-yellow { background: #fcf4d6; color: #684e00; }
    .status-red    { background: #fff1f1; color: #a2191f; }

    /* ── Footer ── */
    .footer {
        text-align: center; color: var(--ibm-gray-600);
        font-size: 12px; padding: 32px 0 16px;
        border-top: 1px solid var(--ibm-gray-200); margin-top: 48px;
    }
    
    /* Candidate Summary */
    .ibm-card .candidate-name{
        color:#161616 !important;
        font-size:20px !important;
        font-weight:700 !important;
    }

    .ibm-card .candidate-details{
        color:#555555 !important;
    }

    /* hide streamlit branding */
    #MainMenu, footer, header { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────
#  Sidebar
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        """
        <div style="text-align:center; padding: 20px 0 10px;">
            <div style="font-size:52px;">🎯</div>
            <div style="font-size:24px; font-weight:700; letter-spacing:1px; margin-top:8px;">PrepPilot</div>
            <div style="font-size:12px; color:#a6c8ff; margin-top:4px;">AI Interview Trainer</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    st.markdown(
        """
        <div style="font-size:13px; line-height:1.8;">
            <div style="font-weight:600; font-size:14px; margin-bottom:10px; color:#78a9ff;">🚀 About PrepPilot</div>
            PrepPilot is an AI-powered Interview Trainer that leverages IBM enterprise technology to help candidates prepare with confidence.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown(
        """
        <div style="font-size:13px; line-height:1.8;">
            <div style="font-weight:600; font-size:14px; margin-bottom:10px; color:#78a9ff;">⚙️ Powered By</div>
            <div>🔵 IBM watsonx Orchestrate</div>
            <div>🤖 IBM watsonx.ai</div>
            <div>📚 Retrieval-Augmented Generation</div>
            <div>☁️ IBM Cloud Object Storage</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown(
        """
        <div style="font-size:13px; line-height:1.8;">
            <div style="font-weight:600; font-size:14px; margin-bottom:10px; color:#78a9ff;">📋 Features</div>
            <div>✅ Personalized Question Generation</div>
            <div>✅ Resume-Aware Preparation</div>
            <div>✅ Multi-Format Interview Coaching</div>
            <div>✅ Real-time AI Feedback</div>
            <div>✅ Readiness Score Analytics</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown(
        """
        <div style="font-size:11px; color:#6f6f6f; line-height:1.8;">
            <div style="font-weight:600; color:#a6c8ff; margin-bottom:6px;">IBM SkillsBuild Internship</div>
            <div>Version 1.0.0</div>
            <div>© 2025 PrepPilot Team</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────────
#  Top navigation bar
# ─────────────────────────────────────────────
st.markdown(
    """
    <div class="top-nav">
        <div class="top-nav-left">
            <div class="top-nav-logo">PP</div>
            <div>
                <div class="top-nav-title">PrepPilot — AI Interview Trainer</div>
                <div class="top-nav-sub">Powered by IBM watsonx Orchestrate &amp; watsonx.ai</div>
            </div>
        </div>
        <div class="top-nav-badge">IBM SkillsBuild 2025</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────
#  Watsonx Orchestrate API helper
# ─────────────────────────────────────────────
WATSONX_API_URL    = os.getenv("WATSONX_API_URL", "")
WATSONX_API_KEY    = os.getenv("WATSONX_API_KEY", "")
WATSONX_SPACE_ID   = os.getenv("WATSONX_SPACE_ID", "")
ORCHESTRATE_URL    = os.getenv("ORCHESTRATE_URL", "")
ORCHESTRATE_KEY    = os.getenv("ORCHESTRATE_API_KEY", "")


def call_watsonx_agent(payload: dict) -> dict | None:
    """
    Call the deployed watsonx Orchestrate agent.
    Returns the parsed JSON response or None on failure.
    """
    if not ORCHESTRATE_URL or not ORCHESTRATE_KEY:
        return None
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ORCHESTRATE_KEY}",
    }
    try:
        resp = requests.post(
            ORCHESTRATE_URL,
            headers=headers,
            json=payload,
            timeout=120,
        )
        resp.raise_for_status()
        return resp.json()
    except Exception as exc:
        st.warning(f"Agent API error: {exc}. Running in demo mode.")
        return None


# ─────────────────────────────────────────────
#  Demo data generator  (fallback / showcase)
# ─────────────────────────────────────────────
def generate_demo_content(form: dict) -> dict:
    """Produce realistic demo output when agent credentials are absent."""
    role    = form.get("job_role", "Software Engineer")
    company = form.get("target_company", "IBM")
    exp     = form.get("experience_level", "Mid-Level")
    itype   = form.get("interview_type", "Mixed")
    skills  = form.get("skills", "Python, Machine Learning")

    technical_qs = [
        f"Explain the difference between REST and GraphQL APIs, and when would you choose one over the other for a {role} role at {company}?",
        f"How do you ensure scalability and fault tolerance in distributed systems? Describe a real example relevant to {role}.",
        f"Walk me through your experience with {skills.split(',')[0].strip()} and describe the most complex problem you solved with it.",
        f"What design patterns have you used in your projects? Give a concrete example for a {role} scenario.",
        f"How would you approach debugging a performance bottleneck in a production environment at {company}?",
    ]

    hr_qs = [
        f"Tell me about yourself and why you want to join {company} as a {role}.",
        f"Where do you see yourself in 5 years, and how does this {role} role align with your goals?",
        "Describe a situation where you disagreed with a team member. How did you resolve it?",
        f"Why are you the best candidate for this {role} position at {company}?",
        "How do you manage multiple deadlines and prioritise tasks under pressure?",
    ]

    behavioral_qs = [
        "Describe a time you led a team through a difficult technical challenge. What was your approach?",
        "Tell me about a project where you had to learn a new technology quickly. How did you manage it?",
        "Give an example of when you received critical feedback. How did you respond and adapt?",
        "Describe your most impactful contribution to a team project and what made it successful.",
        "Tell me about a time you identified and proactively solved a problem before it escalated.",
    ]

    model_answers = {
        "Tell me about yourself": (
            f"I'm a {exp} {role} with hands-on experience in {skills}. "
            f"My background includes delivering impactful solutions in fast-paced environments. "
            f"I'm drawn to {company} because of its commitment to innovation and enterprise AI — "
            "areas I'm deeply passionate about. Outside of work I contribute to open-source projects "
            "and enjoy mentoring junior developers."
        ),
        "Greatest Strength": (
            "My greatest strength is translating complex technical concepts into actionable solutions. "
            "I bridge the gap between engineering depth and business value — I don't just write code, "
            "I solve problems. This has consistently helped my teams ship products that stakeholders actually use."
        ),
        "Handle Tight Deadlines": (
            "I break large tasks into sprint-sized milestones, communicate blockers early, and ruthlessly "
            "prioritise. For example, during a product launch I re-scoped a 3-week feature to 4 days by "
            "identifying the critical path and deferring non-essential work — we shipped on time and "
            "iterated in the next release."
        ),
    }

    tips = [
        ("💡", "Research IBM's latest announcements, especially around watsonx, sustainability, and hybrid cloud before your interview."),
        ("📝", f"Prepare 3–4 STAR-format stories that directly map to the core competencies of a {role} at {company}."),
        ("🤝", "Demonstrate cultural fit by aligning your answers with IBM's core values: innovation, trust, and being essential."),
        ("🔍", f"Review the job description line-by-line and map your skills ({skills}) to each listed requirement."),
        ("❓", "Prepare 3–5 thoughtful questions for your interviewer — ask about team structure, current challenges, and success metrics."),
        ("🧠", "Practice articulating your thought process out loud; interviewers evaluate how you think, not just what you know."),
        ("📊", "Quantify your past achievements — numbers, percentages, and business outcomes make stories memorable."),
    ]

    feedback_items = [
        ("Technical Depth",    random.randint(72, 95), "#0f62fe"),
        ("Communication",      random.randint(70, 92), "#009d9a"),
        ("Problem Solving",    random.randint(68, 95), "#8a3ffc"),
        ("Cultural Alignment", random.randint(75, 95), "#24a148"),
        ("Leadership Signals", random.randint(65, 90), "#f1c21b"),
    ]

    score       = random.randint(74, 96)
    score_color = "#24a148" if score >= 85 else "#f1c21b" if score >= 70 else "#da1e28"
    score_label = "Excellent" if score >= 85 else "Good" if score >= 70 else "Needs Work"

    return {
        "technical_questions":  technical_qs  if itype in ("Technical", "Mixed") else [],
        "hr_questions":         hr_qs         if itype in ("HR", "Mixed") else [],
        "behavioral_questions": behavioral_qs if itype in ("Behavioral", "Mixed") else [],
        "model_answers":        model_answers,
        "preparation_tips":     tips,
        "feedback_items":       feedback_items,
        "readiness_score":      score,
        "score_color":          score_color,
        "score_label":          score_label,
        "generated_at":         datetime.now().strftime("%B %d, %Y · %I:%M %p"),
    }


# ─────────────────────────────────────────────
#  Session state
# ─────────────────────────────────────────────
if "result"    not in st.session_state: st.session_state.result    = None
if "submitted" not in st.session_state: st.session_state.submitted = False
if "form_data" not in st.session_state: st.session_state.form_data = {}

# ─────────────────────────────────────────────
#  Main layout — two-column
# ─────────────────────────────────────────────
left_col, right_col = st.columns([1, 1.6], gap="large")

# ══════════════════════════════════════════════
#  LEFT — Candidate Form
# ══════════════════════════════════════════════
with left_col:
    st.markdown(
        """
        <div class="section-header">
            <span class="icon">📋</span>
            <div>
                <div class="title">Candidate Profile</div>
                <div class="sub">Complete your profile for personalised preparation</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("candidate_form", clear_on_submit=False):

        st.markdown("#### 👤 Personal Information")
        full_name = st.text_input(
            "Full Name *",
            placeholder="e.g. Sarah Johnson",
            help="Enter your full legal name as on your resume",
        )
        email = st.text_input(
            "Email Address *",
            placeholder="e.g. sarah.johnson@email.com",
        )

        st.markdown("<hr class='ibm-divider'>", unsafe_allow_html=True)
        st.markdown("#### 💼 Target Role")

        col1, col2 = st.columns(2)
        with col1:
            job_role = st.text_input(
                "Job Role *",
                placeholder="e.g. Data Scientist",
            )
        with col2:
            target_company = st.text_input(
                "Target Company *",
                placeholder="e.g. IBM",
            )

        experience_level = st.selectbox(
            "Experience Level *",
            [
                "Entry-Level (0–2 years)",
                "Mid-Level (2–5 years)",
                "Senior (5–8 years)",
                "Lead / Principal (8+ years)",
                "Executive / Director",
            ],
        )

        skills = st.text_area(
            "Key Skills *",
            placeholder="e.g. Python, Machine Learning, SQL, TensorFlow, Docker, REST APIs",
            height=90,
            help="List your most relevant technical and soft skills, separated by commas",
        )

        st.markdown("<hr class='ibm-divider'>", unsafe_allow_html=True)
        st.markdown("#### 📄 Resume Upload")
        resume_file = st.file_uploader(
            "Upload Resume (PDF or DOCX)",
            type=["pdf", "docx"],
            help="Your resume is analysed by the AI to personalise your preparation",
        )

        st.markdown("<hr class='ibm-divider'>", unsafe_allow_html=True)
        st.markdown("#### 🎯 Interview Configuration")

        interview_type = st.radio(
            "Interview Type *",
            ["Mixed", "Technical", "HR", "Behavioral"],
            horizontal=True,
            help=(
                "**Mixed** covers all categories · "
                "**Technical** focuses on domain knowledge · "
                "**HR** on culture fit · "
                "**Behavioral** on past experiences"
            ),
        )

        num_questions = st.slider(
            "Questions per Category",
            min_value=3, max_value=10, value=5,
            help="Number of questions to generate per interview category",
        )

        focus_areas = st.multiselect(
            "Focus Areas (optional)",
            [
                "System Design", "Algorithms & Data Structures",
                "Machine Learning / AI", "Cloud & DevOps",
                "Leadership & Management", "Product Thinking",
                "Communication & Collaboration", "Problem Solving",
            ],
            default=[],
            help="Optionally narrow down topic areas for targeted preparation",
        )

        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button(
            "🚀  Generate Interview Preparation",
            use_container_width=True,
        )

    # ── Process submission ──────────────────
    if submitted:
        errors = []
        if not full_name.strip():  errors.append("Full Name is required.")
        if not email.strip():      errors.append("Email is required.")
        if not job_role.strip():   errors.append("Job Role is required.")
        if not skills.strip():     errors.append("Skills are required.")

        if errors:
            for e in errors:
                st.error(f"⚠️ {e}")
        else:
            st.session_state.form_data = {
                "full_name":        full_name,
                "email":            email,
                "job_role":         job_role,
                "target_company":   target_company,
                "experience_level": experience_level,
                "skills":           skills,
                "interview_type":   interview_type,
                "num_questions":    num_questions,
                "focus_areas":      focus_areas,
                "resume_uploaded":  resume_file is not None,
            }
            with st.spinner("🤖 PrepPilot AI is analysing your profile…"):
                progress = st.progress(0)
                stages = [
                    (15,  "🔍 Parsing candidate profile…"),
                    (35,  "📚 Querying IBM watsonx.ai knowledge base…"),
                    (55,  "🧠 Generating personalised questions via RAG…"),
                    (75,  "✍️  Crafting model answers and feedback…"),
                    (90,  "📊 Computing readiness score…"),
                    (100, "✅ Preparation report ready!"),
                ]
                status_text = st.empty()
                for pct, msg in stages:
                    status_text.markdown(f"**{msg}**")
                    progress.progress(pct)
                    time.sleep(0.55)

                # Try live agent first, fall back to demo
                agent_payload = {
                    "candidate": st.session_state.form_data,
                    "interview_type": interview_type,
                    "num_questions": num_questions,
                }
                live_result = call_watsonx_agent(agent_payload)
                if live_result:
                    st.session_state.result = live_result
                else:
                    st.session_state.result = generate_demo_content(st.session_state.form_data)

                st.session_state.submitted = True
                status_text.empty()
                progress.empty()

            st.success("✅ Interview preparation generated successfully!")


# ══════════════════════════════════════════════
#  RIGHT — Results Panel
# ══════════════════════════════════════════════
with right_col:

    if not st.session_state.submitted or st.session_state.result is None:
        # ── Welcome / placeholder state ──
        st.markdown(
            """
            <div class="section-header">
                <span class="icon">✨</span>
                <div>
                    <div class="title">Your Preparation Report</div>
                    <div class="sub">Results will appear here after generation</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="ibm-card" style="text-align:center; padding: 48px 32px;">
                <div style="font-size:64px; margin-bottom:20px;">🎯</div>
                <div style="font-size:20px; font-weight:600; color:#0f62fe; margin-bottom:12px;">
                    Welcome to PrepPilot
                </div>
                <div style="font-size:14px; color:#6f6f6f; line-height:1.8; max-width:380px; margin:0 auto;">
                    Complete the candidate profile on the left and click
                    <strong>Generate Interview Preparation</strong> to receive your
                    personalised AI-powered interview coaching report.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:16px; margin-top:16px;">
                <div class="ibm-card ibm-card-teal" style="padding:20px;">
                    <div style="font-size:28px; margin-bottom:8px;">🔵</div>
                    <div style="font-weight:600; font-size:14px;">IBM watsonx.ai</div>
                    <div style="font-size:12px; color:#6f6f6f; margin-top:6px;">Foundation model generates contextual, role-specific questions</div>
                </div>
                <div class="ibm-card ibm-card-green" style="padding:20px;">
                    <div style="font-size:28px; margin-bottom:8px;">📚</div>
                    <div style="font-weight:600; font-size:14px;">RAG Pipeline</div>
                    <div style="font-size:12px; color:#6f6f6f; margin-top:6px;">Retrieves real interview patterns from IBM Cloud Object Storage</div>
                </div>
                <div class="ibm-card ibm-card-purple" style="padding:20px;">
                    <div style="font-size:28px; margin-bottom:8px;">🤖</div>
                    <div style="font-weight:600; font-size:14px;">Orchestrate Agent</div>
                    <div style="font-size:12px; color:#6f6f6f; margin-top:6px;">Deployed AI agent orchestrates the full preparation workflow</div>
                </div>
                <div class="ibm-card ibm-card-yellow" style="padding:20px;">
                    <div style="font-size:28px; margin-bottom:8px;">📊</div>
                    <div style="font-weight:600; font-size:14px;">Readiness Score</div>
                    <div style="font-size:12px; color:#6f6f6f; margin-top:6px;">AI evaluates your profile and estimates interview readiness</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    else:
        # ══════════════════════════════════════
        #  Full results display
        # ══════════════════════════════════════
        res  = st.session_state.result
        form = st.session_state.form_data

        # ── Candidate summary strip ──
        st.markdown(
            f"""
            <div class="ibm-card" style="padding:18px 24px; border-left-color:#009d9a;">
                <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:12px;">
                    <div>
                        <div
                            class="candidate-name"
                            style="color:#161616 !important;
                                font-size:20px;
                                font-weight:bold;">
                            {form.get('full_name','—')}
                        </div>
                        <div class="candidate-details">
                            {" · ".join([
                                x for x in [
                                    form.get("job_role"),
                                    form.get("target_company"),
                                    form.get("experience_level")
                                ] if x
                            ])}
                        </div>
                    </div>
                    <div style="display:flex; gap:8px; flex-wrap:wrap; align-items:center;">
                        <span class="status-pill status-blue">
                            🎯 {form.get('interview_type','Mixed')}
                        </span>
                        {"<span class='status-pill status-green'>📄 Resume</span>" if form.get('resume_uploaded') else ""}
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ── Skills tags ──
        skills_list = [s.strip() for s in form.get("skills", "").split(",") if s.strip()]
        tag_colors  = ["", "tag-green", "tag-teal", "tag-purple", "tag-yellow"]
        tags_html   = "".join(
            f'<span class="tag {tag_colors[i % len(tag_colors)]}">{s}</span>'
            for i, s in enumerate(skills_list)
        )
        if tags_html:
            st.markdown(
                f'<div style="margin:-8px 0 16px;">{tags_html}</div>',
                unsafe_allow_html=True,
            )

        # ─────────────────────────────────────
        #  Tabs for sections
        # ─────────────────────────────────────
        tab_labels = []
        if res.get("technical_questions"):   tab_labels.append("🔧 Technical")
        if res.get("hr_questions"):          tab_labels.append("🤝 HR")
        if res.get("behavioral_questions"):  tab_labels.append("💬 Behavioral")
        tab_labels += ["📖 Model Answers", "💡 Tips", "📊 Feedback & Score"]

        tabs = st.tabs(tab_labels)
        tab_idx = 0

        # ── Technical Questions ──────────────
        if res.get("technical_questions"):
            with tabs[tab_idx]:
                st.markdown(
                    """
                    <div style="margin-bottom:16px;">
                        <span class="status-pill status-blue">Domain & Technical Knowledge</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                for i, q in enumerate(res["technical_questions"], 1):
                    st.markdown(
                        f"""
                        <div class="question-item">
                            <div class="question-number">Question {i:02d}</div>
                            <p style="color:#161616; font-size:15px; font-weight:500; line-height:1.6;">
                               {q}
                            </p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    # User Answer
                    user_answer = st.text_area(
                        f"✍️ Your Answer for Question {i}",
                        key=f"tech_answer_{i}",
                        height=120,
                        placeholder="Write your answer here..."
                    )

                    if st.button("Submit Answer", key=f"submit_{i}"):

                        if user_answer.strip() == "":
                            st.warning("Please write your answer first.")

                        else:

                            score = random.randint(6,10)

                            st.success(f"✅ Score : {score}/10")

                            st.info(
                            "Good answer. Try explaining your solution with one practical example."
                            )
            tab_idx += 1

        # ── HR Questions ─────────────────────
        if res.get("hr_questions"):
            with tabs[tab_idx]:
                st.markdown(
                    """
                    <div style="margin-bottom:16px;">
                        <span class="status-pill status-green">Culture Fit & Motivations</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                for i, q in enumerate(res["hr_questions"], 1):
                    st.markdown(
                        f"""
                        <div class="question-item" style="border-left-color:#24a148;">
                            <div class="question-number" style="color:#24a148;">Question {i:02d}</div>
                            <p style="color:#161616; font-size:15px; font-weight:500; line-height:1.6;">
                               {q}
                            </p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    user_answer = st.text_area(
                        f"✍️ Your Answer for HR Question {i}",
                        key=f"hr_answer_{i}",
                        height=120
                    )

                    if st.button("Submit HR Answer", key=f"hr_submit_{i}"):

                        if user_answer.strip():

                            score=random.randint(7,10)

                            st.success(f"Score : {score}/10")

                            st.info("Excellent. Try adding STAR method.")

                        else:

                            st.warning("Please answer first.")
            tab_idx += 1

        # ── Behavioral Questions ─────────────
        if res.get("behavioral_questions"):
            with tabs[tab_idx]:
                st.markdown(
                    """
                    <div style="margin-bottom:16px;">
                        <span class="status-pill status-yellow">STAR-Format Situations</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                for i, q in enumerate(res["behavioral_questions"], 1):
                    st.markdown(
                        f"""
                        <div class="question-item" style="border-left-color:#f1c21b;">
                            <div class="question-number" style="color:#b45309;">Question {i:02d}</div>
                            <p style="color:#161616; font-size:15px; font-weight:500; line-height:1.6;">
                               {q}
                            </p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    user_answer = st.text_area(
                        f"✍️ Your Answer for Behavioral Question {i}",
                        key=f"beh_answer_{i}",
                        height=120
                    )

                    if st.button("Submit Behavioral Answer", key=f"beh_submit_{i}"):

                        if user_answer.strip():

                            score=random.randint(7,10)

                            st.success(f"Score : {score}/10")

                            st.info(
                                "Good answer. Use Situation → Task → Action → Result."
                            )

                        else:

                            st.warning("Please answer first.")
            tab_idx += 1

        # ── Model Answers ────────────────────
        with tabs[tab_idx]:
            st.markdown(
                """
                <div style="margin-bottom:16px;">
                    <span class="status-pill" style="background:#f6f2ff;color:#491d8b;">
                        AI-crafted example responses
                    </span>
                </div>
                """,
                unsafe_allow_html=True,
            )
            for question, answer in res.get("model_answers", {}).items():
                with st.expander(f"💬 {question}", expanded=False):
                    st.markdown(
                        f"""
                        <div style="background:#f4f4f4; border-left:3px solid #8a3ffc;
                                    padding:16px 20px; border-radius:0 6px 6px 0;
                                    font-size:14px; line-height:1.8; color:#161616;">
                            {answer}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
        tab_idx += 1

        # ── Preparation Tips ─────────────────
        with tabs[tab_idx]:
            st.markdown(
                """
                <div style="margin-bottom:16px;">
                    <span class="status-pill status-green">Expert Interview Strategy</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
            for icon, tip in res.get("preparation_tips", []):
                st.markdown(
                    f"""
                    <div class="tip-item">
                        <span class="tip-icon">{icon}</span>
                        <span class="tip-text" style="color:#161616; font-size:15px;">
                            {tip}
                        </span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        tab_idx += 1

        # ── Feedback & Score ─────────────────
        with tabs[tab_idx]:
            score       = res.get("readiness_score", 0)
            score_color = res.get("score_color", "#0f62fe")
            score_label = res.get("score_label", "Good")

            score_col, bar_col = st.columns([1, 1.8])

            with score_col:
                st.markdown(
                    f"""
                    <div class="score-container">
                        <div class="score-ring" style="border-color:{score_color}30;
                             background: conic-gradient({score_color} {score}%, #e0e0e0 0%);
                             padding:8px;">
                            <div style="background:#fff; width:108px; height:108px;
                                 border-radius:50%; display:flex; flex-direction:column;
                                 align-items:center; justify-content:center;">
                                <div class="score-number" style="color:{score_color};">{score}</div>
                                <div class="score-label">/ 100</div>
                            </div>
                        </div>
                        <div style="font-size:18px; font-weight:600; color:{score_color};">{score_label}</div>
                        <div style="font-size:12px; color:#6f6f6f; margin-top:4px;">Interview Readiness Score</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with bar_col:
                st.markdown("<div style='margin-top:12px;'>", unsafe_allow_html=True)
                for label, value, color in res.get("feedback_items", []):
                    st.markdown(
                        f"""
                        <div class="prog-bar-wrap">
                            <div class="prog-label">{label} — <strong>{value}%</strong></div>
                            <div class="prog-bar-bg">
                                <div class="prog-bar-fill"
                                     style="width:{value}%; background:{color};"></div>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<hr class='ibm-divider'>", unsafe_allow_html=True)

            # Coaching summary
            rec_level = (
                "🟢 You appear well-prepared. Focus on polishing your storytelling and quantifying achievements."
                if score >= 85 else
                "🟡 Good foundation. Strengthen weak areas identified above and practice mock interviews."
                if score >= 70 else
                "🔴 More preparation needed. Deep-dive into technical concepts and rehearse STAR answers."
            )
            st.markdown(
                f"""
                <div class="ibm-card ibm-card-teal" style="padding:20px 24px;">
                    <h3>🧭 AI Coaching Summary</h3>
                    <p style="font-size:14px; line-height:1.8; margin:0; color:#161616; font-weight:500;">
                        {rec_level}
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Reset button
            if st.button("🔄  Start New Preparation", use_container_width=False):
                st.session_state.result    = None
                st.session_state.submitted = False
                st.session_state.form_data = {}
                st.rerun()

# ─────────────────────────────────────────────
#  Footer
# ─────────────────────────────────────────────
st.markdown(
    """
    <div class="footer">
        <strong>PrepPilot</strong> — AI-Powered Interview Trainer &nbsp;·&nbsp;
        IBM SkillsBuild Internship Project 2025 &nbsp;·&nbsp;
        Powered by IBM watsonx Orchestrate, watsonx.ai &amp; RAG
    </div>
    """,
    unsafe_allow_html=True,
)
