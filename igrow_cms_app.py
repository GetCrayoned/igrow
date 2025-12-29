"""
I-Grow Discipleship Guide - Content Management System
Features:
- Public viewing interface
- Hidden admin login for content editing
- Persistent content storage
- Weekly content updates by authorized users
"""

import streamlit as st
import json
import os
from pathlib import Path
import hashlib

# Page configuration
st.set_page_config(
    page_title="I-Grow Discipleship Guide",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="collapsed"
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
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Scrollable reading section */
    .scrollable-content {
        max-height: 600px;
        overflow-y: auto;
        padding-right: 1rem;
    }
    
    /* Login box */
    .login-box {
        max-width: 400px;
        margin: 2rem auto;
        padding: 2rem;
        background-color: white;
        border-radius: 0.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# File paths
CONTENT_FILE = Path("igrow_content.json")
ADMIN_PASSWORD_HASH = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"  # Default: "password"

# Helper functions
def hash_password(password):
    """Hash a password for storing."""
    return hashlib.sha256(password.encode()).hexdigest()

def load_content():
    """Load content from JSON file."""
    if CONTENT_FILE.exists():
        with open(CONTENT_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        # Return default template content
        return {
            "main_title": "I-Grow Discipleship Guide",
            "study_topic": "Justice and Mercy in the Conquest (The Book of Joshua)",
            "context": "Context: Campus and Workplace Small Groups (Philippines)",
            "icebreaker_title": "The \"Fairness\" Debate",
            "icebreaker_text": "Think of a time when you were playing a game or working on a group project and someone \"cheated\" or didn't do their part but still got the same reward as you. How did that make you feel? Share your story in one minute or less.",
            "big_idea": "God's heart is always for restoration, and His judgments are not about anger, but about protecting life and providing a way back for everyone.",
            "passage_name": "Ezekiel 33",
            "key_verse": "As I live, says the Lord God, I have no pleasure in the death of the wicked, but that the wicked turn from his way and live",
            "verse_reference": "Ezekiel 33:11, ESV",
            "section1_title": "A Change of Heart",
            "section1_content": "God is often misunderstood as a strict judge waiting for us to mess up. However, Ezekiel 33:11 shows us a God who actually feels \"agony\" when people choose a path that leads to destruction. He is like a parent watching a child make a dangerous mistake, pleading for them to \"turn back\" before they get hurt. This means that my past mistakes do not define my future if I am willing to change direction today. When we turn to Him, His mercy overrides the consequences we originally deserved. This truth changes how I view my own failures because I realize God is cheering for my recovery rather than waiting for my punishment.",
            "section1_question": "Sa mga moments na feeling mo \"fail\" ka or lumayo ka kay Lord, how does knowing He takes \"no pleasure\" in your struggle change your perspective? (Does this make it easier for you to come back to Him?)",
            "section1_key_truth": "God is cheering for your recovery, not waiting for your punishment. Your past mistakes don't define your future when you turn to Him.",
            "section2_title": "Our Shared Responsibility",
            "section2_content": "In our communities, we often find it easy to judge others while excusing ourselves. Ezekiel reminds us that God is impartial, meaning He holds everyone to the same standard of love and justice. As a group, we are called to be like \"watchmen\" who look out for one another's spiritual well-being. This is not about being \"judgy,\" but about caring enough to speak up when we see a friend heading toward a \"dead end.\" Our relationships grow deeper when we create a space where it is safe to admit we are wrong and encourage each other to stay on the right path. We represent God's fairness by being consistent in how we treat people, regardless of their background or status.",
            "section2_question": "How can we make our group a \"safe space\" where it's okay to admit mistakes without feeling judged by others? (Ano yung isang thing na pwede nating gawin para mas maging supportive sa isa't isa?)",
            "section2_key_truth": "True community happens when we're consistent in how we treat everyone, creating space where it's safe to admit mistakes and grow together.",
            "section3_title": "A Mission of Mercy",
            "section3_content": "The story of the conquest in Joshua and the warnings in Ezekiel show that God intervenes only when evil begins to destroy everything good. Our mission today is to share the \"Good News\" that there is always a way out of toxic cycles and harmful lifestyles. Just as Rahab found safety in the middle of a city facing judgment, God is looking for \"outsiders\" to bring into His family. We are sent to our campuses and offices not to condemn people, but to offer them the same mercy we have received. When we live out this mission, we show the world that God's ultimate goal is not to \"win a war,\" but to save as many people as possible.",
            "section3_question": "Sino yung \"unlikely person\" sa workplace or school mo na feeling mo kailangan ng encouragement or mercy ngayon? (How can you show them God's kindness this week without sounding like you are lecturing them?)",
            "section3_key_truth": "God's ultimate goal isn't to \"win a war\" but to save as many people as possible. When we show mercy, we reveal His true heart.",
            "key_insight": "It is easy to look at the stories of judgment in the Bible and feel afraid or confused. But when we look closer at Ezekiel 33, we see a God who is actually \"longsuffering\" and incredibly patient. He waits until the very last second, hoping that just one more person will turn around and live. He does not want anyone to perish, and that includes you, your \"difficult\" boss, or your struggling classmate. This reveals that God is both perfectly just and incredibly kind at the same time. You can trust Him with the things you don't understand because His heart is always moved by love.",
            "action_step": "Identify one person this week who seems to be \"struggling with the consequences\" of a bad choice. Instead of joining in the gossip or judging them, offer them a genuine word of encouragement or a small act of kindness to remind them that there is always a path back to hope.",
            "struggles_list": "Felt like a failure\nMade a big mistake\nDrifted from prayer/Bible reading\nHurt someone I care about\nGave in to temptation\nDoubted God's goodness",
            "safespace_list": "Listen without interrupting\nNo gossip rule\nShare our own struggles first\nPray for each other regularly\nCheck in during the week\nCelebrate small wins together"
        }

def save_content(content):
    """Save content to JSON file."""
    with open(CONTENT_FILE, 'w', encoding='utf-8') as f:
        json.dump(content, f, indent=2, ensure_ascii=False)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'show_login' not in st.session_state:
    st.session_state.show_login = False

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

if 'content' not in st.session_state:
    st.session_state.content = load_content()

# Admin login interface
def show_admin_login():
    st.markdown("""
    <div class="login-box">
        <h2 style="color: #6F6354; text-align: center; margin-bottom: 1.5rem;">Admin Login</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        password = st.text_input("Password", type="password", key="admin_password")
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Login", use_container_width=True):
                if hash_password(password) == ADMIN_PASSWORD_HASH:
                    st.session_state.logged_in = True
                    st.session_state.show_login = False
                    st.rerun()
                else:
                    st.error("Incorrect password")
        
        with col_b:
            if st.button("Cancel", use_container_width=True):
                st.session_state.show_login = False
                st.rerun()

# Admin content editor
def show_admin_editor():
    with st.sidebar:
        st.title("📝 Admin Content Editor")
        st.markdown("---")
        
        if st.button("💾 Save Changes", use_container_width=True, type="primary"):
            save_content(st.session_state.content)
            st.success("Content saved successfully!")
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()
        
        st.markdown("---")
        
        # Main Title and Context
        st.subheader("Main Title")
        st.session_state.content["main_title"] = st.text_input("Guide Title", value=st.session_state.content.get("main_title", ""), key="main_title")
        st.session_state.content["study_topic"] = st.text_area("Topic/Subtitle", value=st.session_state.content.get("study_topic", ""), key="study_topic", height=60)
        st.session_state.content["context"] = st.text_input("Context", value=st.session_state.content.get("context", ""), key="context")
        
        st.markdown("---")
        
        # Ice Breaker
        st.subheader("Ice Breaker")
        st.session_state.content["icebreaker_title"] = st.text_input("Ice Breaker Title", value=st.session_state.content.get("icebreaker_title", ""), key="icebreaker_title")
        st.session_state.content["icebreaker_text"] = st.text_area("Ice Breaker Question", value=st.session_state.content.get("icebreaker_text", ""), key="icebreaker_text", height=100)
        
        st.markdown("---")
        
        # Big Idea
        st.subheader("The Big Idea")
        st.session_state.content["big_idea"] = st.text_area("Main Message", value=st.session_state.content.get("big_idea", ""), key="big_idea", height=80)
        
        st.markdown("---")
        
        # Passage & Key Text
        st.subheader("Scripture")
        st.session_state.content["passage_name"] = st.text_input("Passage Reference", value=st.session_state.content.get("passage_name", ""), key="passage_name")
        st.session_state.content["key_verse"] = st.text_area("Key Verse", value=st.session_state.content.get("key_verse", ""), key="key_verse", height=80)
        st.session_state.content["verse_reference"] = st.text_input("Verse Reference", value=st.session_state.content.get("verse_reference", ""), key="verse_reference")
        
        st.markdown("---")
        
        # Section 1
        st.subheader("Section 1")
        st.session_state.content["section1_title"] = st.text_input("Section 1 Title", value=st.session_state.content.get("section1_title", ""), key="section1_title")
        st.session_state.content["section1_content"] = st.text_area("Section 1 Content", value=st.session_state.content.get("section1_content", ""), key="section1_content", height=150)
        st.session_state.content["section1_question"] = st.text_area("Section 1 Discussion Question", value=st.session_state.content.get("section1_question", ""), key="section1_question", height=80)
        st.session_state.content["section1_key_truth"] = st.text_area("Section 1 Key Truth", value=st.session_state.content.get("section1_key_truth", ""), key="section1_key_truth", height=60)
        
        st.markdown("---")
        
        # Section 2
        st.subheader("Section 2")
        st.session_state.content["section2_title"] = st.text_input("Section 2 Title", value=st.session_state.content.get("section2_title", ""), key="section2_title")
        st.session_state.content["section2_content"] = st.text_area("Section 2 Content", value=st.session_state.content.get("section2_content", ""), key="section2_content", height=150)
        st.session_state.content["section2_question"] = st.text_area("Section 2 Discussion Question", value=st.session_state.content.get("section2_question", ""), key="section2_question", height=80)
        st.session_state.content["section2_key_truth"] = st.text_area("Section 2 Key Truth", value=st.session_state.content.get("section2_key_truth", ""), key="section2_key_truth", height=60)
        
        st.markdown("---")
        
        # Section 3
        st.subheader("Section 3")
        st.session_state.content["section3_title"] = st.text_input("Section 3 Title", value=st.session_state.content.get("section3_title", ""), key="section3_title")
        st.session_state.content["section3_content"] = st.text_area("Section 3 Content", value=st.session_state.content.get("section3_content", ""), key="section3_content", height=150)
        st.session_state.content["section3_question"] = st.text_area("Section 3 Discussion Question", value=st.session_state.content.get("section3_question", ""), key="section3_question", height=80)
        st.session_state.content["section3_key_truth"] = st.text_area("Section 3 Key Truth", value=st.session_state.content.get("section3_key_truth", ""), key="section3_key_truth", height=60)
        
        st.markdown("---")
        
        # Key Insight
        st.subheader("Key Insight")
        st.session_state.content["key_insight"] = st.text_area("Key Insight Content", value=st.session_state.content.get("key_insight", ""), key="key_insight", height=150)
        
        st.markdown("---")
        
        # Action Step
        st.subheader("Action Step")
        st.session_state.content["action_step"] = st.text_area("Action Step Challenge", value=st.session_state.content.get("action_step", ""), key="action_step", height=100)
        
        st.markdown("---")
        
        # Interactive Elements
        st.subheader("Section 1: Interactive Options")
        st.session_state.content["struggles_list"] = st.text_area(
            "Personal Struggle Options (one per line)", 
            value=st.session_state.content.get("struggles_list", ""),
            key="struggles_list",
            height=120
        )
        
        st.subheader("Section 2: Interactive Options")
        st.session_state.content["safespace_list"] = st.text_area(
            "Safe Space Ideas (one per line)",
            value=st.session_state.content.get("safespace_list", ""),
            key="safespace_list",
            height=120
        )

# Section 0: Complete Reading Material
def section_0_reading():
    content = st.session_state.content
    
    st.markdown(f"""
    <div class="gradient-header">
        <h1>{content.get('main_title', '')}</h1>
        <p style="font-size: 1.2rem; margin-top: 0.5rem; opacity: 0.9;">{content.get('study_topic', '')}</p>
        <p style="font-size: 0.9rem; margin-top: 0.25rem; opacity: 0.75;">{content.get('context', '')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="scrollable-content">', unsafe_allow_html=True)
    
    # Ice Breaker
    st.markdown(f"""
    <div class="ice-breaker-box">
        <h2 style="color: #6F6354; margin-bottom: 1rem;">Ice Breaker: {content.get('icebreaker_title', '')}</h2>
        <p style="color: #252628; line-height: 1.6;">
            {content.get('icebreaker_text', '')}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Big Idea
    st.markdown(f"""
    <div class="big-idea-box">
        <h2 style="color: #6F6354; margin-bottom: 1rem;">The Big Idea</h2>
        <p style="color: #252628; font-weight: 600; line-height: 1.6;">
            {content.get('big_idea', '')}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Passage & Key Text
    st.markdown(f"""
    <div class="passage-box">
        <h2 style="color: #6F6354; margin-bottom: 1rem;">Passage & Key Text</h2>
        <p style="color: #252628; font-weight: 600; margin-bottom: 1rem;">Passage: {content.get('passage_name', '')}</p>
        <p style="color: #252628; font-style: italic; line-height: 1.6;">
            "{content.get('key_verse', '')}"
        </p>
        <p style="color: #6B7280; font-size: 0.9rem; margin-top: 0.5rem;">({content.get('verse_reference', '')})</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Section 1
    st.markdown(f"""
    <div class="section-1">
        <h2 style="color: #6F6354; margin-bottom: 1rem;">Section 1: {content.get('section1_title', '')}</h2>
        <p style="color: #252628; line-height: 1.6; margin-bottom: 1rem;">
            {content.get('section1_content', '')}
        </p>
        <div class="discussion-box">
            <p style="color: #6F6354; font-weight: 600; margin-bottom: 0.5rem;">Discussion Question:</p>
            <p style="color: #252628; font-style: italic;">
                {content.get('section1_question', '')}
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Section 2
    st.markdown(f"""
    <div class="section-2">
        <h2 style="color: #6F6354; margin-bottom: 1rem;">Section 2: {content.get('section2_title', '')}</h2>
        <p style="color: #252628; line-height: 1.6; margin-bottom: 1rem;">
            {content.get('section2_content', '')}
        </p>
        <div class="discussion-box">
            <p style="color: #6F6354; font-weight: 600; margin-bottom: 0.5rem;">Discussion Question:</p>
            <p style="color: #252628; font-style: italic;">
                {content.get('section2_question', '')}
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Section 3
    st.markdown(f"""
    <div class="section-3">
        <h2 style="color: #6F6354; margin-bottom: 1rem;">Section 3: {content.get('section3_title', '')}</h2>
        <p style="color: #252628; line-height: 1.6; margin-bottom: 1rem;">
            {content.get('section3_content', '')}
        </p>
        <div class="discussion-box">
            <p style="color: #6F6354; font-weight: 600; margin-bottom: 0.5rem;">Discussion Question:</p>
            <p style="color: #252628; font-style: italic;">
                {content.get('section3_question', '')}
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Key Insight
    st.markdown(f"""
    <div class="gradient-insight">
        <h2 style="margin-bottom: 1rem;">Key Insight</h2>
        <p style="line-height: 1.6;">
            {content.get('key_insight', '')}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Action Step
    st.markdown(f"""
    <div class="ice-breaker-box">
        <h2 style="color: #6F6354; margin-bottom: 1rem;">Action Step</h2>
        <p style="color: #252628; line-height: 1.6;">
            {content.get('action_step', '')}
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
    content = st.session_state.content
    
    st.markdown("""
    <div class="gradient-header-blue">
        <h2 style="font-size: 2rem; margin-bottom: 0.5rem;">Welcome to Your Interactive Journey</h2>
        <p style="font-size: 1.1rem; opacity: 0.9;">Let's explore together</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="yellow-box">
        <h3 style="color: #92400E; margin-bottom: 1rem;">Quick Recap: {content.get('icebreaker_title', '')}</h3>
        <p style="color: #252628;">
            {content.get('icebreaker_text', '')}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="blue-box">
        <h3 style="color: #1E40AF; margin-bottom: 1rem;">The Big Idea</h3>
        <p style="color: #252628; font-size: 1.1rem; line-height: 1.6;">
            {content.get('big_idea', '')}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="passage-box" style="border: 2px solid #6B7280;">
        <h3 style="color: #1F2937; margin-bottom: 1rem;">Key Text</h3>
        <p style="color: #252628; font-size: 1.1rem; font-style: italic; line-height: 1.6;">
            "{content.get('key_verse', '')}"
        </p>
        <p style="color: #6B7280; font-size: 0.9rem; font-weight: 600; margin-top: 0.5rem;">
            — {content.get('verse_reference', '')}
        </p>
    </div>
    """, unsafe_allow_html=True)


# Section 2: A Change of Heart
def section_2_change_of_heart():
    content = st.session_state.content
    
    st.markdown(f"""
    <div class="blue-box">
        <h3 style="color: #1E40AF; font-size: 1.5rem; margin-bottom: 1rem;">Section 1: {content.get('section1_title', '')}</h3>
        <p style="color: #252628; line-height: 1.6;">
            {content.get('section1_content', '')}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="yellow-box">
        <h4 style="color: #92400E; font-size: 1.2rem; margin-bottom: 1rem;">When have you felt distant from God?</h4>
        <p style="color: #252628; margin-bottom: 1rem;">Select all that apply (or add your own):</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Parse struggles from content
    struggles = [s.strip() for s in content.get('struggles_list', '').split('\n') if s.strip()]
    
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
            {content.get('section1_question', '')}
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
            {content.get('section1_key_truth', '')}
        </p>
    </div>
    """, unsafe_allow_html=True)


# Section 3: Our Shared Responsibility
def section_3_shared_responsibility():
    content = st.session_state.content
    
    st.markdown(f"""
    <div class="orange-box">
        <h3 style="color: #9A3412; font-size: 1.5rem; margin-bottom: 1rem;">Section 2: {content.get('section2_title', '')}</h3>
        <p style="color: #252628; line-height: 1.6;">
            {content.get('section2_content', '')}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="green-box">
        <h4 style="color: #065F46; font-size: 1.2rem; margin-bottom: 1rem;">How can we create a "safe space"?</h4>
        <p style="color: #252628; margin-bottom: 1rem;">Choose ideas that resonate with you:</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Parse safe space ideas from content
    quick_ideas = [s.strip() for s in content.get('safespace_list', '').split('\n') if s.strip()]
    
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
            {content.get('section2_question', '')}
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
            {content.get('section2_key_truth', '')}
        </p>
    </div>
    """, unsafe_allow_html=True)


# Section 4: A Mission of Mercy
def section_4_mission_of_mercy():
    content = st.session_state.content
    
    st.markdown(f"""
    <div class="green-box">
        <h3 style="color: #065F46; font-size: 1.5rem; margin-bottom: 1rem;">Section 3: {content.get('section3_title', '')}</h3>
        <p style="color: #252628; line-height: 1.6;">
            {content.get('section3_content', '')}
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
            {content.get('section3_question', '')}
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
            {content.get('section3_key_truth', '')}
        </p>
    </div>
    """, unsafe_allow_html=True)


# Section 5: Action Step
def section_5_action_step():
    content = st.session_state.content
    
    st.markdown(f"""
    <div class="gradient-header-green">
        <h3 style="font-size: 1.8rem; margin-bottom: 1rem;">Key Insight</h3>
        <p style="font-size: 1.1rem; line-height: 1.6;">
            {content.get('key_insight', '')}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="yellow-box">
        <h4 style="color: #92400E; font-size: 1.5rem; margin-bottom: 1rem;">This Week's Challenge</h4>
        <p style="color: #252628; font-size: 1.1rem; line-height: 1.6; margin-bottom: 1rem;">
            {content.get('action_step', '')}
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
    # Admin access button (hidden in bottom corner)
    if not st.session_state.logged_in and not st.session_state.show_login:
        # Create a small, subtle button that can be clicked to reveal login
        st.markdown("""
        <div style="position: fixed; bottom: 10px; right: 10px; z-index: 9999;">
            <p style="font-size: 0.7rem; color: #888; opacity: 0.3;">admin</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Check for triple-click on the word "admin" by having a button there
        col1, col2, col3 = st.columns([10, 1, 1])
        with col3:
            if st.button("🔧", key="admin_access", help="Admin Login"):
                st.session_state.show_login = True
                st.rerun()
    
    # Show login if requested
    if st.session_state.show_login and not st.session_state.logged_in:
        show_admin_login()
        return
    
    # Show admin editor if logged in
    if st.session_state.logged_in:
        show_admin_editor()
    
    # Main content
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
