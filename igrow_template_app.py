"""
I-Grow Discipleship Guide - Interactive Streamlit Template
This template allows you to update content weekly for Bible Study sessions
Simply replace the placeholder text in the sidebar to customize each week's material
"""

import streamlit as st
import json
import os

# Configuration
JSON_FILE_PATH = "igrow_content.json"

# Helper functions for JSON management
def load_content_from_json():
    """Load content from JSON file if it exists"""
    if os.path.exists(JSON_FILE_PATH):
        try:
            with open(JSON_FILE_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            st.error(f"Error loading JSON file: {e}")
            return {}
    return {}

def save_content_to_json(content_dict):
    """Save content dictionary to JSON file"""
    try:
        with open(JSON_FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(content_dict, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        st.error(f"Error saving JSON file: {e}")
        return False

def get_content_from_session():
    """Collect all content from session state into a dictionary"""
    return {
        # Toggle states
        "enable_icebreaker": st.session_state.get("enable_icebreaker", True),
        "enable_section1": st.session_state.get("enable_section1", True),
        "enable_section2": st.session_state.get("enable_section2", True),
        "enable_section3": st.session_state.get("enable_section3", True),
        "enable_key_insight": st.session_state.get("enable_key_insight", True),
        "enable_action_step": st.session_state.get("enable_action_step", True),
        
        # Main content
        "main_title": st.session_state.get("main_title", "I-Grow Discipleship Guide"),
        "study_topic": st.session_state.get("study_topic", "Put text here for weekly topic"),
        "context": st.session_state.get("context", "Context: Campus and Workplace Small Groups (Philippines)"),
        "icebreaker_title": st.session_state.get("icebreaker_title", "The \"Fairness\" Debate"),
        "icebreaker_text": st.session_state.get("icebreaker_text", "Put text here for ice breaker question"),
        "big_idea": st.session_state.get("big_idea", "Put text here for the big idea"),
        "passage_name": st.session_state.get("passage_name", "Put text here (e.g., Ezekiel 33)"),
        "key_verse": st.session_state.get("key_verse", "Put text here for the key verse"),
        "verse_reference": st.session_state.get("verse_reference", "Book Chapter:Verse, Version"),
        
        # Section 1
        "section1_title": st.session_state.get("section1_title", "Put text here"),
        "section1_content": st.session_state.get("section1_content", "Put text here for section 1 main content"),
        "section1_question": st.session_state.get("section1_question", "Put text here for discussion question"),
        "section1_key_truth": st.session_state.get("section1_key_truth", "Put text here for key truth"),
        "section1_interactive_question": st.session_state.get("section1_interactive_question", "When have you felt distant from God?"),
        "section1_enable_struggles_selector": st.session_state.get("section1_enable_struggles_selector", True),
        
        # Section 2
        "section2_title": st.session_state.get("section2_title", "Put text here"),
        "section2_content": st.session_state.get("section2_content", "Put text here for section 2 main content"),
        "section2_question": st.session_state.get("section2_question", "Put text here for discussion question"),
        "section2_key_truth": st.session_state.get("section2_key_truth", "Put text here for key truth"),
        "section2_interactive_question": st.session_state.get("section2_interactive_question", "How can we create a 'safe space'?"),
        "section2_enable_safespace_selector": st.session_state.get("section2_enable_safespace_selector", True),
        
        # Section 3
        "section3_title": st.session_state.get("section3_title", "Put text here"),
        "section3_content": st.session_state.get("section3_content", "Put text here for section 3 main content"),
        "section3_question": st.session_state.get("section3_question", "Put text here for discussion question"),
        "section3_key_truth": st.session_state.get("section3_key_truth", "Put text here for key truth"),
        "section3_interactive_question": st.session_state.get("section3_interactive_question", "Who needs mercy in your circle?"),
        "section3_enable_person_input": st.session_state.get("section3_enable_person_input", True),
        
        # Key sections
        "key_insight": st.session_state.get("key_insight", "Put text here for key insight"),
        "action_step": st.session_state.get("action_step", "Put text here for this week's action step"),
        "struggles_list": st.session_state.get("struggles_list", "Felt like a failure\nMade a big mistake\nDrifted from prayer/Bible reading\nHurt someone I care about\nGave in to temptation\nDoubted God's goodness"),
        "safespace_list": st.session_state.get("safespace_list", "Listen without interrupting\nNo gossip rule\nShare our own struggles first\nPray for each other regularly\nCheck in during the week\nCelebrate small wins together")
    }


# Page configuration
st.set_page_config(
    page_title="I-Grow Discipleship Guide Template",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Lighthouse Tagaytay brand colors
st.markdown("""
<style>
    /* Brand Colors */
    :root {
        --primary: #6F6354;
        --background: #D0CFC9;
        --surface: #A2A094;
        --text: #252628;
        --secondary: #8A877E;
        --success: #7A9B76;
        --warning: #C9A962;
        --info: #8B7B9E;
        --cream: #F5EFE0;
        --light-greige: #E8E6E0;
    }
    
    /* Main container */
    .main {
        background-color: var(--background);
    }
    
    /* Headers */
    .gradient-header {
        background: linear-gradient(to right, #6F6354, #8A877E);
        color: white;
        padding: 2rem;
        border-radius: 0.5rem;
        margin-bottom: 1.5rem;
    }
    
    .gradient-header-blue {
        background: linear-gradient(to right, #3B82F6, #9333EA);
        color: white;
        padding: 2rem;
        border-radius: 0.5rem;
        margin-bottom: 1.5rem;
    }
    
    .gradient-header-green {
        background: linear-gradient(to right, #10B981, #3B82F6);
        color: white;
        padding: 2rem;
        border-radius: 0.5rem;
        margin-bottom: 1.5rem;
    }
    
    .gradient-insight {
        background: linear-gradient(to bottom, #7A9B76, #6F6354);
        color: white;
        padding: 2rem;
        border-radius: 0.5rem;
        margin: 1.5rem 0;
    }
    
    /* Boxes */
    .ice-breaker-box {
        background-color: #F5EFE0;
        border-left: 4px solid #C9A962;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    
    .big-idea-box {
        background-color: #E8E6E0;
        border: 2px solid #6F6354;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    
    .passage-box {
        background-color: #D0CFC9;
        border: 2px solid #8A877E;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    
    .discussion-box {
        background-color: #E8E6E0;
        border: 2px solid #8B7B9E;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    
    .proof-box {
        background-color: #D0CFC9;
        border-left: 4px solid #6F6354;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    
    .yellow-box {
        background-color: #FEF3C7;
        border: 2px solid #F59E0B;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    
    .blue-box {
        background-color: #DBEAFE;
        border: 2px solid #3B82F6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    
    .orange-box {
        background-color: #FED7AA;
        border: 2px solid #F97316;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    
    .green-box {
        background-color: #D1FAE5;
        border: 2px solid #10B981;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    
    .success-box {
        background-color: #E8F0E6;
        border: 2px solid #7A9B76;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    
    .info-box {
        background-color: #1E40AF;
        color: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        text-align: center;
    }
    
    /* Section borders */
    .section-1 {
        border-top: 4px solid #6F6354;
        padding-top: 1.5rem;
        margin-top: 1.5rem;
    }
    
    .section-2 {
        border-top: 4px solid #8A877E;
        padding-top: 1.5rem;
        margin-top: 1.5rem;
    }
    
    .section-3 {
        border-top: 4px solid #7A9B76;
        padding-top: 1.5rem;
        margin-top: 1.5rem;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #6F6354;
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 0.5rem;
        font-weight: 600;
        transition: opacity 0.3s;
    }
    
    .stButton > button:hover {
        opacity: 0.9;
        background-color: #6F6354;
    }
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background-color: #6F6354;
    }
    
    /* Card styling for selection */
    .selection-card {
        border: 2px solid #D0CFC9;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: all 0.3s;
    }
    
    .selection-card:hover {
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .selection-card-selected {
        background-color: #7A9B76;
        color: white;
        border: 2px solid #7A9B76;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Scrollable reading section */
    .scrollable-content {
        max-height: 600px;
        overflow-y: auto;
        padding-right: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_section' not in st.session_state:
    st.session_state.current_section = 0

if 'reflections' not in st.session_state:
    st.session_state.reflections = {}

if 'selected_struggles' not in st.session_state:
    st.session_state.selected_struggles = []

if 'safe_space_ideas' not in st.session_state:
    st.session_state.safe_space_ideas = []

if 'unlikely_person' not in st.session_state:
    st.session_state.unlikely_person = ''

if 'action_commitment' not in st.session_state:
    st.session_state.action_commitment = ''

# Load content from JSON on first run
if 'content_loaded' not in st.session_state:
    loaded_content = load_content_from_json()
    # Initialize all content fields from JSON or use defaults
    for key, value in loaded_content.items():
        if key not in st.session_state:
            st.session_state[key] = value
    st.session_state.content_loaded = True

# SIDEBAR - EDITABLE CONTENT
with st.sidebar:
    st.title("📝 Weekly Content Editor")
    st.markdown("---")
    st.info("Update this content each week. Your changes will appear in the main guide.")
    
    # Section Visibility Toggles
    st.subheader("🎛️ Section Visibility")
    st.caption("Toggle sections on/off based on your weekly topic")
    
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        enable_icebreaker = st.checkbox("Ice Breaker", value=True, key="enable_icebreaker")
        enable_section1 = st.checkbox("Section 1", value=True, key="enable_section1")
        enable_section2 = st.checkbox("Section 2", value=True, key="enable_section2")
    with col_t2:
        enable_section3 = st.checkbox("Section 3", value=True, key="enable_section3")
        enable_key_insight = st.checkbox("Key Insight", value=True, key="enable_key_insight")
        enable_action_step = st.checkbox("Action Step", value=True, key="enable_action_step")
    
    st.markdown("---")
    
    # Main Title and Context
    st.subheader("Main Title")
    main_title = st.text_input("Guide Title", value="I-Grow Discipleship Guide", key="main_title")
    study_topic = st.text_area("Topic/Subtitle", value="Put text here for weekly topic", key="study_topic", height=60)
    context = st.text_input("Context", value="Context: Campus and Workplace Small Groups (Philippines)", key="context")
    
    st.markdown("---")
    
    # Ice Breaker
    st.subheader("Ice Breaker")
    icebreaker_title = st.text_input("Ice Breaker Title", value="The \"Fairness\" Debate", key="icebreaker_title")
    icebreaker_text = st.text_area("Ice Breaker Question", value="Put text here for ice breaker question", key="icebreaker_text", height=100)
    
    st.markdown("---")
    
    # Big Idea
    st.subheader("The Big Idea")
    big_idea = st.text_area("Main Message", value="Put text here for the big idea", key="big_idea", height=80)
    
    st.markdown("---")
    
    # Passage & Key Text
    st.subheader("Scripture")
    passage_name = st.text_input("Passage Reference", value="Put text here (e.g., Ezekiel 33)", key="passage_name")
    key_verse = st.text_area("Key Verse", value="Put text here for the key verse", key="key_verse", height=80)
    verse_reference = st.text_input("Verse Reference", value="Book Chapter:Verse, Version", key="verse_reference")
    
    st.markdown("---")
    
    # Section 1
    st.subheader("Section 1")
    if enable_section1:
        section1_title = st.text_input("Section 1 Title", value="Put text here", key="section1_title")
        section1_content = st.text_area("Section 1 Content", value="Put text here for section 1 main content", key="section1_content", height=150)
        section1_question = st.text_area("Section 1 Discussion Question", value="Put text here for discussion question", key="section1_question", height=80)
        section1_key_truth = st.text_area("Section 1 Key Truth", value="Put text here for key truth", key="section1_key_truth", height=60)
        
        st.caption("Interactive Elements:")
        section1_interactive_question = st.text_input("Interactive Question", value="When have you felt distant from God?", key="section1_interactive_question")
        section1_enable_struggles_selector = st.checkbox("Show struggles selector", value=True, key="section1_enable_struggles_selector")
    else:
        st.info("⚠️ Section 1 is disabled. Enable it above to edit.")
    
    st.markdown("---")
    
    # Section 2
    st.subheader("Section 2")
    if enable_section2:
        section2_title = st.text_input("Section 2 Title", value="Put text here", key="section2_title")
        section2_content = st.text_area("Section 2 Content", value="Put text here for section 2 main content", key="section2_content", height=150)
        section2_question = st.text_area("Section 2 Discussion Question", value="Put text here for discussion question", key="section2_question", height=80)
        section2_key_truth = st.text_area("Section 2 Key Truth", value="Put text here for key truth", key="section2_key_truth", height=60)
        
        st.caption("Interactive Elements:")
        section2_interactive_question = st.text_input("Interactive Question", value="How can we create a 'safe space'?", key="section2_interactive_question")
        section2_enable_safespace_selector = st.checkbox("Show safe space selector", value=True, key="section2_enable_safespace_selector")
    else:
        st.info("⚠️ Section 2 is disabled. Enable it above to edit.")
    
    st.markdown("---")
    
    # Section 3
    st.subheader("Section 3")
    if enable_section3:
        section3_title = st.text_input("Section 3 Title", value="Put text here", key="section3_title")
        section3_content = st.text_area("Section 3 Content", value="Put text here for section 3 main content", key="section3_content", height=150)
        section3_question = st.text_area("Section 3 Discussion Question", value="Put text here for discussion question", key="section3_question", height=80)
        section3_key_truth = st.text_area("Section 3 Key Truth", value="Put text here for key truth", key="section3_key_truth", height=60)
        
        st.caption("Interactive Elements:")
        section3_interactive_question = st.text_input("Interactive Question", value="Who needs mercy in your circle?", key="section3_interactive_question")
        section3_enable_person_input = st.checkbox("Show person input field", value=True, key="section3_enable_person_input")
    else:
        st.info("⚠️ Section 3 is disabled. Enable it above to edit.")
    
    st.markdown("---")
    
    # Key Insight
    st.subheader("Key Insight")
    if enable_key_insight:
        key_insight = st.text_area("Key Insight Content", value="Put text here for key insight", key="key_insight", height=150)
    else:
        st.info("⚠️ Key Insight is disabled. Enable it above to edit.")
    
    st.markdown("---")
    
    # Action Step
    st.subheader("Action Step")
    if enable_action_step:
        action_step = st.text_area("Action Step Challenge", value="Put text here for this week's action step", key="action_step", height=100)
    else:
        st.info("⚠️ Action Step is disabled. Enable it above to edit.")
    
    st.markdown("---")
    
    # Interactive Elements (optional customization)
    st.subheader("Section 1: Interactive Options")
    struggles_list = st.text_area(
        "Personal Struggle Options (one per line)", 
        value="Felt like a failure\nMade a big mistake\nDrifted from prayer/Bible reading\nHurt someone I care about\nGave in to temptation\nDoubted God's goodness",
        key="struggles_list",
        height=120
    )
    
    st.subheader("Section 2: Interactive Options")
    safespace_list = st.text_area(
        "Safe Space Ideas (one per line)",
        value="Listen without interrupting\nNo gossip rule\nShare our own struggles first\nPray for each other regularly\nCheck in during the week\nCelebrate small wins together",
        key="safespace_list",
        height=120
    )
    
    st.markdown("---")
    
    # Save Button
    st.subheader("💾 Save Your Changes")
    st.info("Click below to save all your edits to the JSON file. This will update the content permanently.")
    
    if st.button("💾 Save Changes to JSON", key="save_json_btn", use_container_width=True, type="primary"):
        content_to_save = get_content_from_session()
        if save_content_to_json(content_to_save):
            st.success("✅ Content saved successfully to igrow_content.json!")
            st.balloons()
        else:
            st.error("❌ Failed to save content. Please try again.")



# Section 0: Complete Reading Material
def section_0_reading():
    st.markdown(f"""
    <div class="gradient-header">
        <h1>{st.session_state.main_title}</h1>
        <p style="font-size: 1.2rem; margin-top: 0.5rem; opacity: 0.9;">{st.session_state.study_topic}</p>
        <p style="font-size: 0.9rem; margin-top: 0.25rem; opacity: 0.75;">{st.session_state.context}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="scrollable-content">', unsafe_allow_html=True)
    
    # Ice Breaker - only if enabled
    if st.session_state.get("enable_icebreaker", True):
        st.markdown(f"""
        <div class="ice-breaker-box">
            <h2 style="color: #6F6354; margin-bottom: 1rem;">Ice Breaker: {st.session_state.icebreaker_title}</h2>
            <p style="color: #252628; line-height: 1.6;">
                {st.session_state.icebreaker_text}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Big Idea
    st.markdown(f"""
    <div class="big-idea-box">
        <h2 style="color: #6F6354; margin-bottom: 1rem;">The Big Idea</h2>
        <p style="color: #252628; font-weight: 600; line-height: 1.6;">
            {st.session_state.big_idea}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Passage & Key Text
    st.markdown(f"""
    <div class="passage-box">
        <h2 style="color: #6F6354; margin-bottom: 1rem;">Passage & Key Text</h2>
        <p style="color: #252628; font-weight: 600; margin-bottom: 1rem;">Passage: {st.session_state.passage_name}</p>
        <p style="color: #252628; font-style: italic; line-height: 1.6;">
            "{st.session_state.key_verse}"
        </p>
        <p style="color: #6B7280; font-size: 0.9rem; margin-top: 0.5rem;">({st.session_state.verse_reference})</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Section 1 - only if enabled
    if st.session_state.get("enable_section1", True):
        st.markdown(f"""
        <div class="section-1">
            <h2 style="color: #6F6354; margin-bottom: 1rem;">Section 1: {st.session_state.section1_title}</h2>
            <p style="color: #252628; line-height: 1.6; margin-bottom: 1rem;">
                {st.session_state.section1_content}
            </p>
            <div class="discussion-box">
                <p style="color: #6F6354; font-weight: 600; margin-bottom: 0.5rem;">Discussion Question:</p>
                <p style="color: #252628; font-style: italic;">
                    {st.session_state.section1_question}
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Section 2 - only if enabled
    if st.session_state.get("enable_section2", True):
        st.markdown(f"""
        <div class="section-2">
            <h2 style="color: #6F6354; margin-bottom: 1rem;">Section 2: {st.session_state.section2_title}</h2>
            <p style="color: #252628; line-height: 1.6; margin-bottom: 1rem;">
                {st.session_state.section2_content}
            </p>
            <div class="discussion-box">
                <p style="color: #6F6354; font-weight: 600; margin-bottom: 0.5rem;">Discussion Question:</p>
                <p style="color: #252628; font-style: italic;">
                    {st.session_state.section2_question}
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Section 3 - only if enabled
    if st.session_state.get("enable_section3", True):
        st.markdown(f"""
        <div class="section-3">
            <h2 style="color: #6F6354; margin-bottom: 1rem;">Section 3: {st.session_state.section3_title}</h2>
            <p style="color: #252628; line-height: 1.6; margin-bottom: 1rem;">
                {st.session_state.section3_content}
            </p>
            <div class="discussion-box">
                <p style="color: #6F6354; font-weight: 600; margin-bottom: 0.5rem;">Discussion Question:</p>
                <p style="color: #252628; font-style: italic;">
                    {st.session_state.section3_question}
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Key Insight - only if enabled
    if st.session_state.get("enable_key_insight", True):
        st.markdown(f"""
        <div class="gradient-insight">
            <h2 style="margin-bottom: 1rem;">Key Insight</h2>
            <p style="line-height: 1.6;">
                {st.session_state.key_insight}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Action Step - only if enabled
    if st.session_state.get("enable_action_step", True):
        st.markdown(f"""
        <div class="ice-breaker-box">
            <h2 style="color: #6F6354; margin-bottom: 1rem;">Action Step</h2>
            <p style="color: #252628; line-height: 1.6;">
                {st.session_state.action_step}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Call to action
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Ready to make this interactive? Click Next! →", key="start_interactive", use_container_width=True):
            st.session_state.current_section = 1
            st.rerun()


# Section 1: Welcome/Intro
def section_1_intro():
    st.markdown("""
    <div class="gradient-header-blue">
        <h2 style="font-size: 2rem; margin-bottom: 0.5rem;">Welcome to Your Interactive Journey</h2>
        <p style="font-size: 1.1rem; opacity: 0.9;">Let's explore together</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="yellow-box">
        <h3 style="color: #92400E; margin-bottom: 1rem;">Quick Recap: {st.session_state.icebreaker_title}</h3>
        <p style="color: #252628;">
            {st.session_state.icebreaker_text}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="blue-box">
        <h3 style="color: #1E40AF; margin-bottom: 1rem;">The Big Idea</h3>
        <p style="color: #252628; font-size: 1.1rem; line-height: 1.6;">
            {st.session_state.big_idea}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="passage-box" style="border: 2px solid #6B7280;">
        <h3 style="color: #1F2937; margin-bottom: 1rem;">Key Text</h3>
        <p style="color: #252628; font-size: 1.1rem; font-style: italic; line-height: 1.6;">
            "{st.session_state.key_verse}"
        </p>
        <p style="color: #6B7280; font-size: 0.9rem; font-weight: 600; margin-top: 0.5rem;">
            — {st.session_state.verse_reference}
        </p>
    </div>
    """, unsafe_allow_html=True)


# Section 2: A Change of Heart
def section_2_change_of_heart():
    st.markdown(f"""
    <div class="blue-box">
        <h3 style="color: #1E40AF; font-size: 1.5rem; margin-bottom: 1rem;">Section 1: {st.session_state.section1_title}</h3>
        <p style="color: #252628; line-height: 1.6;">
            {st.session_state.section1_content}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="yellow-box">
        <h4 style="color: #92400E; font-size: 1.2rem; margin-bottom: 1rem;">When have you felt distant from God?</h4>
        <p style="color: #252628; margin-bottom: 1rem;">Select all that apply (or add your own):</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Parse struggles from sidebar input
    struggles = [s.strip() for s in st.session_state.struggles_list.split('\n') if s.strip()]
    
    # Create columns for selection
    col1, col2 = st.columns(2)
    
    for idx, struggle in enumerate(struggles):
        with col1 if idx % 2 == 0 else col2:
            is_selected = struggle in st.session_state.selected_struggles
            
            if st.button(
                f"{'✓ ' if is_selected else ''}{struggle}",
                key=f"struggle_{idx}",
                use_container_width=True,
                type="primary" if is_selected else "secondary"
            ):
                if is_selected:
                    st.session_state.selected_struggles.remove(struggle)
                else:
                    st.session_state.selected_struggles.append(struggle)
                st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="discussion-box" style="border-left: 4px solid #8B7B9E;">
        <h4 style="color: #6F6354; font-size: 1.1rem; margin-bottom: 1rem;">Reflect & Respond</h4>
        <p style="color: #252628; font-style: italic; margin-bottom: 1rem;">
            {st.session_state.section1_question}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    reflection = st.text_area(
        "Type your thoughts here...",
        value=st.session_state.reflections.get('section1', ''),
        key="reflection_section1",
        height=120
    )
    st.session_state.reflections['section1'] = reflection
    
    st.markdown(f"""
    <div class="proof-box">
        <p style="color: #6F6354; font-size: 0.9rem; font-weight: 600; margin-bottom: 0.5rem;">KEY TRUTH:</p>
        <p style="color: #252628; font-style: italic;">
            {st.session_state.section1_key_truth}
        </p>
    </div>
    """, unsafe_allow_html=True)


# Section 3: Our Shared Responsibility
def section_3_shared_responsibility():
    st.markdown(f"""
    <div class="orange-box">
        <h3 style="color: #9A3412; font-size: 1.5rem; margin-bottom: 1rem;">Section 2: {st.session_state.section2_title}</h3>
        <p style="color: #252628; line-height: 1.6;">
            {st.session_state.section2_content}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="green-box">
        <h4 style="color: #065F46; font-size: 1.2rem; margin-bottom: 1rem;">How can we create a "safe space"?</h4>
        <p style="color: #252628; margin-bottom: 1rem;">Choose ideas that resonate with you:</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Parse safe space ideas from sidebar input
    quick_ideas = [s.strip() for s in st.session_state.safespace_list.split('\n') if s.strip()]
    
    # Create columns for selection
    col1, col2 = st.columns(2)
    
    for idx, idea in enumerate(quick_ideas):
        with col1 if idx % 2 == 0 else col2:
            is_selected = idea in st.session_state.safe_space_ideas
            
            if st.button(
                f"{'✓ ' if is_selected else ''}{idea}",
                key=f"idea_{idx}",
                use_container_width=True,
                type="primary" if is_selected else "secondary"
            ):
                if is_selected:
                    st.session_state.safe_space_ideas.remove(idea)
                else:
                    st.session_state.safe_space_ideas.append(idea)
                st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="discussion-box" style="border-left: 4px solid #8B7B9E;">
        <h4 style="color: #6F6354; font-size: 1.1rem; margin-bottom: 1rem;">Reflect & Respond</h4>
        <p style="color: #252628; font-style: italic; margin-bottom: 1rem;">
            {st.session_state.section2_question}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    reflection = st.text_area(
        "Share one specific action your group can take...",
        value=st.session_state.reflections.get('section2', ''),
        key="reflection_section2",
        height=120
    )
    st.session_state.reflections['section2'] = reflection
    
    st.markdown(f"""
    <div class="proof-box" style="border-left: 4px solid #8A877E;">
        <p style="color: #6F6354; font-size: 0.9rem; font-weight: 600; margin-bottom: 0.5rem;">KEY TRUTH:</p>
        <p style="color: #252628; font-style: italic;">
            {st.session_state.section2_key_truth}
        </p>
    </div>
    """, unsafe_allow_html=True)


# Section 4: A Mission of Mercy
def section_4_mission_of_mercy():
    st.markdown(f"""
    <div class="green-box">
        <h3 style="color: #065F46; font-size: 1.5rem; margin-bottom: 1rem;">Section 3: {st.session_state.section3_title}</h3>
        <p style="color: #252628; line-height: 1.6;">
            {st.session_state.section3_content}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="yellow-box">
        <h4 style="color: #92400E; font-size: 1.2rem; margin-bottom: 1rem;">Who needs mercy in your circle?</h4>
        <p style="color: #252628; margin-bottom: 1rem;">
            Think of that "unlikely person" - someone others might write off, but who needs 
            encouragement right now.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    unlikely_person = st.text_input(
        "Their name or description",
        value=st.session_state.unlikely_person,
        placeholder="e.g., 'my difficult coworker' or 'the classmate everyone avoids'",
        key="unlikely_person_input"
    )
    st.session_state.unlikely_person = unlikely_person
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="discussion-box" style="border-left: 4px solid #8B7B9E;">
        <h4 style="color: #6F6354; font-size: 1.1rem; margin-bottom: 1rem;">Reflect & Respond</h4>
        <p style="color: #252628; font-style: italic; margin-bottom: 1rem;">
            {st.session_state.section3_question}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    reflection = st.text_area(
        "Be specific: What will you say or do? When will you do it?",
        value=st.session_state.reflections.get('section3', ''),
        key="reflection_section3",
        height=120
    )
    st.session_state.reflections['section3'] = reflection
    
    st.markdown(f"""
    <div class="proof-box" style="border-left: 4px solid #7A9B76;">
        <p style="color: #6F6354; font-size: 0.9rem; font-weight: 600; margin-bottom: 0.5rem;">KEY TRUTH:</p>
        <p style="color: #252628; font-style: italic;">
            {st.session_state.section3_key_truth}
        </p>
    </div>
    """, unsafe_allow_html=True)


# Section 5: Action Step
def section_5_action_step():
    st.markdown(f"""
    <div class="gradient-header-green">
        <h3 style="font-size: 1.8rem; margin-bottom: 1rem;">Key Insight</h3>
        <p style="font-size: 1.1rem; line-height: 1.6;">
            {st.session_state.key_insight}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="yellow-box">
        <h4 style="color: #92400E; font-size: 1.5rem; margin-bottom: 1rem;">This Week's Challenge</h4>
        <p style="color: #252628; font-size: 1.1rem; line-height: 1.6; margin-bottom: 1rem;">
            {st.session_state.action_step}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="success-box">
        <h4 style="color: #065F46; font-size: 1.2rem; margin-bottom: 1rem;">Your Personal Commitment</h4>
    </div>
    """, unsafe_allow_html=True)
    
    # Auto-populate from earlier sections
    if st.session_state.unlikely_person:
        st.markdown(f"""
        <div style="background-color: #D1FAE5; padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem;">
            <p style="color: #065F46; font-size: 0.9rem; font-weight: 600; margin-bottom: 0.25rem;">Person you identified:</p>
            <p style="color: #252628; font-size: 1.1rem; font-weight: 700;">{st.session_state.unlikely_person}</p>
        </div>
        """, unsafe_allow_html=True)
    
    if st.session_state.reflections.get('section3'):
        st.markdown(f"""
        <div style="background-color: #D1FAE5; padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem;">
            <p style="color: #065F46; font-size: 0.9rem; font-weight: 600; margin-bottom: 0.25rem;">Your planned action:</p>
            <p style="color: #252628;">{st.session_state.reflections.get('section3')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<p style='font-weight: 600; color: #252628; margin-bottom: 0.5rem;'>Write your commitment:</p>", unsafe_allow_html=True)
    
    commitment = st.text_area(
        "I commit to... (Be specific: Who? What? When?)",
        value=st.session_state.action_commitment,
        key="action_commitment_input",
        height=120,
        label_visibility="collapsed"
    )
    st.session_state.action_commitment = commitment
    
    if st.session_state.action_commitment:
        st.markdown("""
        <div style="background-color: #7A9B76; color: white; padding: 1rem; border-radius: 0.5rem; margin-top: 1rem;">
            <p style="font-size: 1.1rem; font-weight: 700; margin-bottom: 0.5rem;">✓ Commitment Recorded!</p>
            <p>God is with you as you step out in mercy this week.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        <p style="font-size: 1.2rem; font-weight: 700; margin-bottom: 0.5rem;">Remember:</p>
        <p style="font-size: 1.1rem; line-height: 1.6;">
            Every act of mercy you show reflects God's heart. You're not just being nice - 
            you're showing someone that there's always a path back to hope. 💙
        </p>
    </div>
    """, unsafe_allow_html=True)


# Main app logic
def main():
    sections = [
        {"id": "reading", "title": "Complete Reading", "func": section_0_reading},
        {"id": "intro", "title": "Welcome", "func": section_1_intro},
        {"id": "change", "title": "Section 1", "func": section_2_change_of_heart},
        {"id": "responsibility", "title": "Section 2", "func": section_3_shared_responsibility},
        {"id": "mission", "title": "Section 3", "func": section_4_mission_of_mercy},
        {"id": "action", "title": "Your Action Step", "func": section_5_action_step}
    ]
    
    # Progress bar
    progress = (st.session_state.current_section + 1) / len(sections)
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"<p style='color: #6F6354; font-weight: 600; font-size: 0.9rem;'>Section {st.session_state.current_section + 1} of {len(sections)}</p>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<p style='color: #6F6354; font-weight: 600; font-size: 0.9rem; text-align: right;'>{int(progress * 100)}% Complete</p>", unsafe_allow_html=True)
    
    st.progress(progress)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Render current section
    sections[st.session_state.current_section]["func"]()
    
    # Navigation buttons
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.session_state.current_section > 0:
            if st.button("← Previous", key="prev_btn", use_container_width=True):
                st.session_state.current_section -= 1
                st.rerun()
    
    with col3:
        if st.session_state.current_section < len(sections) - 1:
            if st.button("Next →", key="next_btn", use_container_width=True):
                st.session_state.current_section += 1
                st.rerun()
    
    # Navigation dots
    st.markdown("<br>", unsafe_allow_html=True)
    
    dots_html = '<div style="display: flex; justify-content: center; gap: 0.5rem;">'
    for idx, section in enumerate(sections):
        opacity = "1" if idx == st.session_state.current_section else "0.5"
        color = "#6F6354" if idx == st.session_state.current_section else "#8A877E"
        dots_html += f'<div title="{section["title"]}" style="width: 12px; height: 12px; border-radius: 50%; background-color: {color}; opacity: {opacity}; cursor: pointer;"></div>'
    dots_html += '</div>'
    
    st.markdown(dots_html, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
