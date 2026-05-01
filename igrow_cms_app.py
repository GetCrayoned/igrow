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
import base64
import requests
import pandas as pd
import io
from datetime import datetime
from pathlib import Path
import hashlib
import re

# Page configuration
st.set_page_config(
    page_title="BANIG Bible Study",
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

    /* ── Dark Mode Overrides ───────────────────────────────────────── */
    @media (prefers-color-scheme: dark) {

        /* Streamlit root backgrounds */
        .stApp, .main, [data-testid="stAppViewContainer"],
        [data-testid="stHeader"], section.main > div {
            background-color: #1a1917 !important;
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: #26231f !important;
        }

        /* ── Box components ─────────────────────────────────────────── */
        .ice-breaker-box {
            background-color: #2a2520 !important;
            border-left-color: #C9A962 !important;
        }
        .big-idea-box {
            background-color: #26231f !important;
            border-color: #8A7B6A !important;
        }
        .passage-box {
            background-color: #26231f !important;
            border-color: #6F6354 !important;
        }
        .discussion-box {
            background-color: #20202e !important;
            border-color: #6B5B8A !important;
        }
        .proof-box {
            background-color: #26231f !important;
            border-left-color: #8A7B6A !important;
        }
        .yellow-box {
            background-color: #2d2510 !important;
            border-color: #B8860B !important;
        }
        .blue-box {
            background-color: #111827 !important;
            border-color: #2563EB !important;
        }
        .orange-box {
            background-color: #2d1a0d !important;
            border-color: #C2510A !important;
        }
        .green-box {
            background-color: #0d2318 !important;
            border-color: #059669 !important;
        }
        .success-box {
            background-color: #0d2318 !important;
            border-color: #5A8A56 !important;
        }
        .login-box {
            background-color: #2a2520 !important;
            box-shadow: 0 4px 16px rgba(0,0,0,0.5) !important;
        }

        /* ── Text inside boxes in dark mode ────────────────────────── */

        /* Main body text that was hardcoded #252628 (near-black → near-white) */
        .ice-breaker-box p,
        .big-idea-box p,
        .passage-box p,
        .discussion-box p,
        .proof-box p,
        .yellow-box p,
        .blue-box p,
        .orange-box p,
        .green-box p,
        .success-box p {
            color: #e8e3dc !important;
        }

        /* Headings that used the brand brown — lighten it so it's readable */
        .ice-breaker-box h2, .ice-breaker-box h3,
        .big-idea-box h2, .big-idea-box h3,
        .passage-box h2, .passage-box h3,
        .proof-box p:first-child,
        .discussion-box h4 {
            color: #C9A962 !important;
        }

        /* Blue-box headings */
        .blue-box h3, .blue-box h2 {
            color: #93C5FD !important;
        }

        /* Orange-box headings */
        .orange-box h3, .orange-box h2 {
            color: #FDBA74 !important;
        }

        /* Green-box headings */
        .green-box h4, .green-box h2 {
            color: #6EE7B7 !important;
        }

        /* Success-box headings */
        .success-box h3 {
            color: #6EE7B7 !important;
        }

        /* Verse reference grey */
        .passage-box p[style*="6B7280"] {
            color: #9CA3AF !important;
        }

        /* Streamlit generic text */
        .stMarkdown p, .stMarkdown li, label {
            color: #e8e3dc !important;
        }

        /* Section divider accents */
        .section-1 { border-top-color: #8A7B6A !important; }
        .section-2 { border-top-color: #6F6354 !important; }
        .section-3 { border-top-color: #5A8A56 !important; }

        /* Stacked inline styles from Python — catch-all for very dark text */
        [style*="color: #252628"],
        [style*="color:#252628"] {
            color: #e8e3dc !important;
        }
        [style*="color: #1F2937"],
        [style*="color:#1F2937"] {
            color: #D1D5DB !important;
        }
        [style*="color: #1E40AF"],
        [style*="color:#1E40AF"] {
            color: #93C5FD !important;
        }
        [style*="color: #9A3412"],
        [style*="color:#9A3412"] {
            color: #FDBA74 !important;
        }
        [style*="color: #92400E"],
        [style*="color:#92400E"] {
            color: #FCD34D !important;
        }
        [style*="color: #065F46"],
        [style*="color:#065F46"] {
            color: #6EE7B7 !important;
        }
        [style*="color: #6B7280"],
        [style*="color:#6B7280"] {
            color: #9CA3AF !important;
        }
        [style*="color: #6F6354"],
        [style*="color:#6F6354"] {
            color: #C9A962 !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# File paths
CONTENT_FILE = Path("igrow_content.json")
USER_ANSWERS_FILE = Path("igrow_user_answers.json")
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
            
            "enable_icebreaker": True,
            "enable_section1": True,
            "enable_section2": True,
            "enable_section3": True,
            "enable_key_insight": True,
            "enable_action_step": True,
            
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
            "section1_interactive_question": "When have you felt distant from God?",
            "section1_enable_struggles_selector": True,
            "section1_show_content": True,
            "section1_show_question": True,
            "section1_show_key_truth": True,
            "section1_show_interactive": True,
            "section2_title": "Our Shared Responsibility",
            "section2_content": "In our communities, we often find it easy to judge others while excusing ourselves. Ezekiel reminds us that God is impartial, meaning He holds everyone to the same standard of love and justice. As a group, we are called to be like \"watchmen\" who look out for one another's spiritual well-being. This is not about being \"judgy,\" but about caring enough to speak up when we see a friend heading toward a \"dead end.\" Our relationships grow deeper when we create a space where it is safe to admit we are wrong and encourage each other to stay on the right path. We represent God's fairness by being consistent in how we treat people, regardless of their background or status.",
            "section2_question": "How can we make our group a \"safe space\" where it's okay to admit mistakes without feeling judged by others? (Ano yung isang thing na pwede nating gawin para mas maging supportive sa isa't isa?)",
            "section2_key_truth": "True community happens when we're consistent in how we treat everyone, creating space where it's safe to admit mistakes and grow together.",
            "section2_interactive_question": "How can we create a 'safe space'?",
            "section2_enable_safespace_selector": True,
            "section2_show_content": True,
            "section2_show_question": True,
            "section2_show_key_truth": True,
            "section2_show_interactive": True,
            "section3_title": "A Mission of Mercy",
            "section3_content": "The story of the conquest in Joshua and the warnings in Ezekiel show that God intervenes only when evil begins to destroy everything good. Our mission today is to share the \"Good News\" that there is always a way out of toxic cycles and harmful lifestyles. Just as Rahab found safety in the middle of a city facing judgment, God is looking for \"outsiders\" to bring into His family. We are sent to our campuses and offices not to condemn people, but to offer them the same mercy we have received. When we live out this mission, we show the world that God's ultimate goal is not to \"win a war,\" but to save as many people as possible.",
            "section3_question": "Sino yung \"unlikely person\" sa workplace or school mo na feeling mo kailangan ng encouragement or mercy ngayon? (How can you show them God's kindness this week without sounding like you are lecturing them?)",
            "section3_key_truth": "God's ultimate goal isn't to \"win a war\" but to save as many people as possible. When we show mercy, we reveal His true heart.",
            "section3_interactive_question": "Who needs mercy in your circle?",
            "section3_enable_person_input": True,
            "section3_show_content": True,
            "section3_show_question": True,
            "section3_show_key_truth": True,
            "section3_show_interactive": True,
            "key_insight": "It is easy to look at the stories of judgment in the Bible and feel afraid or confused. But when we look closer at Ezekiel 33, we see a God who is actually \"longsuffering\" and incredibly patient. He waits until the very last second, hoping that just one more person will turn around and live. He does not want anyone to perish, and that includes you, your \"difficult\" boss, or your struggling classmate. This reveals that God is both perfectly just and incredibly kind at the same time. You can trust Him with the things you don't understand because His heart is always moved by love.",
            "action_step": "Identify one person this week who seems to be \"struggling with the consequences\" of a bad choice. Instead of joining in the gossip or judging them, offer them a genuine word of encouragement or a small act of kindness to remind them that there is always a path back to hope.",
            "struggles_list": "Felt like a failure\nMade a big mistake\nDrifted from prayer/Bible reading\nHurt someone I care about\nGave in to temptation\nDoubted God's goodness",
            "safespace_list": "Listen without interrupting\nNo gossip rule\nShare our own struggles first\nPray for each other regularly\nCheck in during the week\nCelebrate small wins together"
        }

def push_to_github(json_str: str):
    """Push the JSON string to GitHub via the Contents API.
    Reads config from st.secrets['github'].
    Returns (success: bool, message: str).
    """
    try:
        gh = st.secrets["github"]
        token    = gh["token"]
        repo     = gh["repo"]       # e.g. "YourUsername/your-repo"
        branch   = gh.get("branch", "main")
        filepath = gh.get("filepath", "igrow_content.json")
    except (KeyError, AttributeError) as e:
        return False, f"Missing GitHub secret: {e}. Check .streamlit/secrets.toml."

    api_url = f"https://api.github.com/repos/{repo}/contents/{filepath}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json",
    }

    # Get current file SHA (required for updates)
    sha = None
    get_resp = requests.get(api_url, headers=headers, params={"ref": branch})
    if get_resp.status_code == 200:
        sha = get_resp.json().get("sha")
    elif get_resp.status_code not in (404,):
        return False, f"GitHub GET failed ({get_resp.status_code}): {get_resp.text[:200]}"

    # Encode content as base64
    encoded = base64.b64encode(json_str.encode("utf-8")).decode("utf-8")

    payload = {
        "message": "chore: update igrow_content.json via CMS",
        "content": encoded,
        "branch": branch,
    }
    if sha:
        payload["sha"] = sha

    put_resp = requests.put(api_url, headers=headers, json=payload)
    if put_resp.status_code in (200, 201):
        return True, "Pushed to GitHub successfully."
    else:
        return False, f"GitHub PUT failed ({put_resp.status_code}): {put_resp.text[:300]}"


def save_content(content):
    """Save content to JSON file and push to GitHub."""
    json_str = json.dumps(content, indent=2, ensure_ascii=False)
    with open(CONTENT_FILE, 'w', encoding='utf-8') as f:
        f.write(json_str)
    return push_to_github(json_str)


# ── User answer helpers ───────────────────────────────────────────────────────
def load_user_answers():
    """Load all user answers — tries GitHub first, falls back to local file."""
    try:
        gh = st.secrets["github"]
        token  = gh["token"]
        repo   = gh["repo"]
        branch = gh.get("branch", "main")
        answers_file = gh.get("answers_filepath", "igrow_user_answers.json")
        url = f"https://api.github.com/repos/{repo}/contents/{answers_file}"
        headers = {"Authorization": f"token {token}",
                   "Accept": "application/vnd.github+json"}
        resp = requests.get(url, headers=headers, params={"ref": branch})
        if resp.status_code == 200:
            file_bytes = base64.b64decode(resp.json()["content"])
            return json.loads(file_bytes.decode("utf-8"))
    except Exception:
        pass  # No secrets or network error — fall through to local

    if USER_ANSWERS_FILE.exists():
        with open(USER_ANSWERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_user_answers(data):
    """Persist user answers locally AND push to GitHub."""
    json_str = json.dumps(data, indent=2, ensure_ascii=False)

    # Always write locally (useful for local dev)
    with open(USER_ANSWERS_FILE, "w", encoding="utf-8") as f:
        f.write(json_str)

    # Push to GitHub so data survives Streamlit Cloud restarts
    try:
        gh = st.secrets["github"]
        token  = gh["token"]
        repo   = gh["repo"]
        branch = gh.get("branch", "main")
        answers_file = gh.get("answers_filepath", "igrow_user_answers.json")
        url = f"https://api.github.com/repos/{repo}/contents/{answers_file}"
        headers = {"Authorization": f"token {token}",
                   "Accept": "application/vnd.github+json"}
        sha = None
        get_resp = requests.get(url, headers=headers, params={"ref": branch})
        if get_resp.status_code == 200:
            sha = get_resp.json().get("sha")
        encoded = base64.b64encode(json_str.encode("utf-8")).decode("utf-8")
        payload = {"message": "chore: update igrow_user_answers.json",
                   "content": encoded, "branch": branch}
        if sha:
            payload["sha"] = sha
        requests.put(url, headers=headers, json=payload)
    except Exception:
        pass  # No secrets — silently skip GitHub push


def get_user_answers(username):
    """Return the list of saved answer sessions for a given username."""
    data = load_user_answers()
    return data.get(username.strip().lower(), [])


def save_current_answers(username):
    """Snapshot the current session's answers and append to the user's history."""
    content = st.session_state.content
    session = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "study_topic": content.get("study_topic", ""),
        "section1_question": content.get("section1_question", ""),
        "section1_answer": st.session_state.reflections.get("section1", ""),
        "section2_question": content.get("section2_question", ""),
        "section2_answer": st.session_state.reflections.get("section2", ""),
        "section3_question": content.get("section3_question", ""),
        "section3_answer": st.session_state.reflections.get("section3", ""),
        "unlikely_person": st.session_state.unlikely_person,
        "safe_space_ideas": list(st.session_state.safe_space_ideas),
        "selected_struggles": list(st.session_state.selected_struggles),
        "commitment": st.session_state.action_commitment,
    }
    key = username.strip().lower()
    data = load_user_answers()
    data.setdefault(key, []).append(session)
    save_user_answers(data)


# ── Survey helpers ────────────────────────────────────────────────────────────
SURVEY_FILE = "igrow_survey_responses.xlsx"
SURVEY_COLUMNS = ["Timestamp", "Study Topic", "Name", "Group/Campus",
                  "Satisfaction (1-5)", "What Resonated", "Suggestions"]

def fetch_survey_dataframe():
    """Download existing survey Excel from GitHub. Returns (df, sha)."""
    try:
        gh = st.secrets["github"]
        token = gh["token"]
        repo  = gh["repo"]
        branch = gh.get("branch", "main")
    except (KeyError, AttributeError):
        return pd.DataFrame(columns=SURVEY_COLUMNS), None

    url = f"https://api.github.com/repos/{repo}/contents/{SURVEY_FILE}"
    headers = {"Authorization": f"token {token}",
               "Accept": "application/vnd.github+json"}
    resp = requests.get(url, headers=headers, params={"ref": branch})
    if resp.status_code == 200:
        data = resp.json()
        file_bytes = base64.b64decode(data["content"])
        df = pd.read_excel(io.BytesIO(file_bytes), engine="openpyxl")
        return df, data["sha"]
    return pd.DataFrame(columns=SURVEY_COLUMNS), None


def submit_survey(responses: dict):
    """Append a survey response and push updated Excel to GitHub."""
    df, sha = fetch_survey_dataframe()
    new_row = {
        "Timestamp":        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Study Topic":      st.session_state.content.get("study_topic", ""),
        "Name":             responses.get("name", ""),
        "Group/Campus":     responses.get("group", ""),
        "Satisfaction (1-5)": responses.get("rating", ""),
        "What Resonated":   responses.get("resonated", ""),
        "Suggestions":      responses.get("suggestions", ""),
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    buffer = io.BytesIO()
    df.to_excel(buffer, index=False, engine="openpyxl")
    encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")

    try:
        gh = st.secrets["github"]
        token = gh["token"]
        repo  = gh["repo"]
        branch = gh.get("branch", "main")
    except (KeyError, AttributeError) as e:
        return False, f"Missing secret: {e}"

    url = f"https://api.github.com/repos/{repo}/contents/{SURVEY_FILE}"
    headers = {"Authorization": f"token {token}",
               "Accept": "application/vnd.github+json"}
    payload = {"message": "chore: add survey response",
               "content": encoded, "branch": branch}
    if sha:
        payload["sha"] = sha
    resp = requests.put(url, headers=headers, json=payload)
    return (True, "Submitted!") if resp.status_code in (200, 201) \
        else (False, f"Push failed ({resp.status_code}): {resp.text[:200]}")


# ── Document import (pattern matching) ───────────────────────────────────────
def parse_document_text(text: str) -> dict:
    """
    Parse a plain-text Bible study guide into CMS content fields.
    Expected format (same as I-Grow Google Docs template):
      Line 1: Study Title
      Icebreaker <text>
      Big Idea <text>
      Passage & Key Text <Ref> "<verse>" - <ref>
      <Section heading>\n<body paragraphs>\n<Discussion question?>
      Key Insight <text>
      Action Step <text>
    """
    # Normalise line endings
    lines = [l.strip() for l in text.replace('\r\n', '\n').split('\n')]
    # Remove divider lines
    lines = [l for l in lines if not re.match(r'^[_\-=]{4,}$', l)]
    full = '\n'.join(lines)

    content = {}

    # ── Title ────────────────────────────────────────────────────────────────
    # First non-empty line is the title (may be repeated — take first)
    title_lines = [l for l in lines if l]
    content["study_topic"] = title_lines[0] if title_lines else ""
    content["icebreaker_title"] = content["study_topic"]
    content["main_title"] = "I-Grow Discipleship Guide"
    content["context"] = "Context: Campus and Workplace Small Groups (Philippines)"

    # ── Icebreaker ───────────────────────────────────────────────────────────
    m = re.search(r'Icebreaker\s+(.+?)(?=Big Idea|Passage|\Z)', full, re.S | re.I)
    content["icebreaker_text"] = m.group(1).strip() if m else ""

    # ── Big Idea ─────────────────────────────────────────────────────────────
    m = re.search(r'Big Idea\s+(.+?)(?=Passage|\Z)', full, re.S | re.I)
    content["big_idea"] = m.group(1).strip() if m else ""

    # ── Passage & Key Verse ──────────────────────────────────────────────────
    m = re.search(r'Passage\s*&?\s*Key Text\s+(.+?)(?=\n)', full, re.I)
    if m:
        passage_line = m.group(1).strip()
        # passage ref is before the quoted verse
        ref_match = re.match(r'([^"]+)', passage_line)
        content["passage_name"] = ref_match.group(1).strip() if ref_match else passage_line
    else:
        content["passage_name"] = ""

    verse_match = re.search(r'["\u201c](.+?)["\u201d]\s*[\u2013\-]+\s*(.+?)(?=\n|$)', full)
    if verse_match:
        content["key_verse"]       = verse_match.group(1).strip()
        content["verse_reference"] = verse_match.group(2).strip()
    else:
        content["key_verse"] = content["verse_reference"] = ""

    # ── Sections (detect by heading then collect body + questions) ───────────
    # A section heading is a short line (< 60 chars) not matching known keywords
    SKIP_PATTERN = re.compile(
        r'^(Icebreaker|Big Idea|Passage|Key Insight|Action Step|Finding|One God)',
        re.I)
    # Split body after Passage block
    after_passage = re.split(r'Passage\s*&?\s*Key Text.+?(?=\n\n|\n[A-Z])',
                              full, maxsplit=1, flags=re.S | re.I)
    body = after_passage[-1] if len(after_passage) > 1 else full

    # Split on Key Insight to separate section body from ending
    body_parts = re.split(r'Key Insight', body, maxsplit=1, flags=re.I)
    sections_text = body_parts[0]
    ending_text   = body_parts[1] if len(body_parts) > 1 else ""

    # Find section headings: lines < 55 chars, Title Case or ALL CAPS, no period
    section_blocks = []
    sec_lines = sections_text.split('\n')
    current_heading = None
    current_body = []
    for line in sec_lines:
        if (line and len(line) < 55
                and not SKIP_PATTERN.match(line)
                and not line.endswith('?')
                and re.search(r'[A-Z]', line)
                and not re.match(r'^[a-z]', line)):
            if current_heading is not None:
                section_blocks.append((current_heading, '\n'.join(current_body).strip()))
            current_heading = line
            current_body = []
        elif current_heading:
            current_body.append(line)
    if current_heading:
        section_blocks.append((current_heading, '\n'.join(current_body).strip()))

    section_keys = [
        ("section1_title", "section1_content", "section1_question", "section1_key_truth"),
        ("section2_title", "section2_content", "section2_question", "section2_key_truth"),
        ("section3_title", "section3_content", "section3_question", "section3_key_truth"),
    ]

    for i, (heading, body_text) in enumerate(section_blocks[:3]):
        tk, ck, qk, kk = section_keys[i]
        content[tk] = heading

        # Questions are lines ending with ?
        q_lines = [l for l in body_text.split('\n') if l.strip().endswith('?')]
        content[qk] = ' '.join(q_lines).strip()

        # Content = everything except question lines
        non_q = [l for l in body_text.split('\n')
                 if l.strip() and not l.strip().endswith('?')]
        content[ck] = '\n'.join(non_q).strip()

        # Key truth = last non-question sentence of content
        sentences = re.split(r'(?<=[.!])\s+', content[ck])
        content[kk] = sentences[-1].strip() if sentences else ""

    # Fill missing sections with empty strings
    for i in range(len(section_blocks), 3):
        tk, ck, qk, kk = section_keys[i]
        content[tk] = content[ck] = content[qk] = content[kk] = ""

    # ── Key Insight ──────────────────────────────────────────────────────────
    m = re.search(r'Key Insight\s*\n(.+?)(?=Action Step|\Z)', ending_text, re.S | re.I)
    content["key_insight"] = m.group(1).strip() if m else ""

    # ── Action Step ──────────────────────────────────────────────────────────
    m = re.search(r'Action Step\s*\n(.+?)(?=\Z)', ending_text, re.S | re.I)
    content["action_step"] = m.group(1).strip() if m else ""

    # ── Preserve defaults for toggles and interactive lists ──────────────────
    defaults = {
        "enable_icebreaker": True, "enable_section1": True,
        "enable_section2": True,  "enable_section3": True,
        "enable_key_insight": True, "enable_action_step": True,
        "section1_show_content": True, "section1_show_question": True,
        "section1_show_key_truth": True, "section1_show_interactive": True,
        "section1_interactive_question": "When have you felt this way?",
        "section1_enable_struggles_selector": True,
        "section2_show_content": True, "section2_show_question": True,
        "section2_show_key_truth": True, "section2_show_interactive": True,
        "section2_interactive_question": "How can we support each other?",
        "section2_enable_safespace_selector": True,
        "section3_show_content": True, "section3_show_question": True,
        "section3_show_key_truth": True, "section3_show_interactive": True,
        "section3_interactive_question": "Who needs this in your circle?",
        "section3_enable_person_input": True,
        "struggles_list": "Felt confused or lost\nGoing through a dark season\nSearching for meaning\nFeeling isolated or alone\nDoubting God's presence\nStruggling with purpose",
        "safespace_list": "Listen without interrupting\nPray for each other regularly\nCheck in during the week\nShare our own struggles first\nNo gossip rule\nCelebrate each other's victories",
    }
    for k, v in defaults.items():
        content.setdefault(k, v)

    return content


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

if 'survey_submitted' not in st.session_state:
    st.session_state.survey_submitted = False

if 'import_preview' not in st.session_state:
    st.session_state.import_preview = None

if 'user_logged_in' not in st.session_state:
    st.session_state.user_logged_in = False

if 'current_username' not in st.session_state:
    st.session_state.current_username = ''

if 'show_user_login' not in st.session_state:
    st.session_state.show_user_login = False

if 'show_past_answers' not in st.session_state:
    st.session_state.show_past_answers = False

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

# User login interface
def show_user_login():
    st.markdown("""
    <div class="login-box" style="max-width: 440px; margin: 3rem auto; text-align: center;">
        <span style="font-size: 2.5rem;">📖</span>
        <h2 style="color: #6F6354; margin-top: 0.5rem; margin-bottom: 0.25rem;">Sign In</h2>
        <p style="color: #8A877E; font-size: 0.9rem; margin-bottom: 0;">Enter your name to save and review your answers</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        username = st.text_input(
            "Your Name / Username",
            placeholder="e.g. Maria, JohnD …",
            key="_usr_history_login_input"
        )
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Sign In ✓", use_container_width=True, type="primary", key="_usr_history_signin_confirm"):
                if username.strip():
                    st.session_state.user_logged_in = True
                    st.session_state.current_username = username.strip()
                    st.session_state.show_user_login = False
                    st.rerun()
                else:
                    st.error("Please enter your name.")
        with col_b:
            if st.button("Cancel", use_container_width=True, key="_usr_history_login_cancel"):
                st.session_state.show_user_login = False
                st.rerun()


# Past answers viewer
def show_past_answers():
    """Display the current user's past saved answer sessions."""
    username = st.session_state.current_username
    sessions = get_user_answers(username)

    st.markdown(f"""
    <div class="gradient-header-blue">
        <h2 style="margin-bottom: 0.25rem;">📚 My Past Answers</h2>
        <p style="opacity: 0.9; margin: 0;">Signed in as <strong>{username}</strong></p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("← Back to Study", key="_usr_history_back"):
        st.session_state.show_past_answers = False
        st.rerun()

    if not sessions:
        st.markdown("""
        <div class="info-box" style="text-align: center; padding: 2rem; margin-top: 1.5rem;">
            <p style="font-size: 1.1rem; margin: 0;">No saved answers yet.<br>
            Complete a study and hit <strong>💾 Save My Answers</strong>!</p>
        </div>
        """, unsafe_allow_html=True)
        return

    st.markdown(
        f"<p style='color:#8A877E; margin-bottom:1rem;'>{len(sessions)} session(s) saved</p>",
        unsafe_allow_html=True
    )

    data = load_user_answers()
    key = username.strip().lower()

    # Show newest first
    for orig_idx, session in reversed(list(enumerate(sessions))):
        topic = session.get("study_topic", "Bible Study")
        ts = session.get("timestamp", "")
        label = f"📖  {topic}  •  {ts}"
        is_latest = (orig_idx == len(sessions) - 1)

        with st.expander(label, expanded=is_latest):

            def _qa_row(question, answer):
                if question:
                    st.markdown(f"""
                    <div class="discussion-box" style="margin-bottom:0.5rem;">
                        <p style="color:#6F6354;font-weight:600;font-size:0.82rem;margin-bottom:0.25rem;">QUESTION</p>
                        <p style="color:#252628;font-style:italic;margin-bottom:0;">{question}</p>
                    </div>
                    """, unsafe_allow_html=True)
                if answer:
                    st.markdown(f"""
                    <div class="success-box" style="margin-bottom:1rem;">
                        <p style="color:#065F46;font-weight:600;font-size:0.82rem;margin-bottom:0.25rem;">YOUR ANSWER</p>
                        <p style="color:#252628;margin-bottom:0;">{answer}</p>
                    </div>
                    """, unsafe_allow_html=True)
                elif question:
                    st.markdown(
                        "<p style='color:#9CA3AF;font-size:0.85rem;margin-bottom:1rem;'><em>(No answer recorded)</em></p>",
                        unsafe_allow_html=True
                    )

            _qa_row(session.get("section1_question"), session.get("section1_answer"))
            _qa_row(session.get("section2_question"), session.get("section2_answer"))
            _qa_row(session.get("section3_question"), session.get("section3_answer"))

            if session.get("unlikely_person"):
                st.markdown(f"""
                <div class="proof-box" style="margin-bottom:0.5rem;">
                    <p style="color:#6F6354;font-weight:600;font-size:0.82rem;margin-bottom:0.25rem;">PERSON I IDENTIFIED</p>
                    <p style="color:#252628;margin-bottom:0;">{session['unlikely_person']}</p>
                </div>
                """, unsafe_allow_html=True)

            if session.get("commitment"):
                st.markdown(f"""
                <div class="proof-box" style="border-left-color:#7A9B76;margin-bottom:0.5rem;">
                    <p style="color:#6F6354;font-weight:600;font-size:0.82rem;margin-bottom:0.25rem;">MY COMMITMENT</p>
                    <p style="color:#252628;margin-bottom:0;">{session['commitment']}</p>
                </div>
                """, unsafe_allow_html=True)

            if session.get("selected_struggles"):
                st.markdown(
                    "<p style='font-size:0.82rem;color:#6F6354;font-weight:600;margin-bottom:0.25rem;'>STRUGGLES I IDENTIFIED</p>",
                    unsafe_allow_html=True
                )
                st.markdown("  ".join([f"`{s}`" for s in session["selected_struggles"]]))

            if session.get("safe_space_ideas"):
                st.markdown(
                    "<p style='font-size:0.82rem;color:#6F6354;font-weight:600;margin-top:0.5rem;margin-bottom:0.25rem;'>SAFE SPACE IDEAS I CHOSE</p>",
                    unsafe_allow_html=True
                )
                st.markdown("  ".join([f"`{s}`" for s in session["safe_space_ideas"]]))

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🗑️ Delete this entry", key=f"_usr_history_del_{orig_idx}"):
                data[key].pop(orig_idx)
                save_user_answers(data)
                st.success("Entry deleted.")
                st.rerun()


# Admin content editor
def show_admin_editor():
    with st.sidebar:
        st.title("📝 Admin Content Editor")
        st.markdown("---")
        
        if st.button("💾 Save Changes", use_container_width=True, type="primary"):
            gh_ok, gh_msg = save_content(st.session_state.content)
            if gh_ok:
                st.success("✅ Saved & pushed to GitHub!")
            else:
                st.warning(f"💾 Saved locally. GitHub push failed: {gh_msg}")
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()
        
        st.markdown("---")
        
        # Section Visibility Toggles
        st.subheader("🎛️ Section Visibility")
        st.caption("Toggle sections on/off based on your weekly topic")
        
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            st.session_state.content["enable_icebreaker"] = st.checkbox("Ice Breaker", value=st.session_state.content.get("enable_icebreaker", True), key="enable_icebreaker")
            st.session_state.content["enable_section1"] = st.checkbox("Section 1", value=st.session_state.content.get("enable_section1", True), key="enable_section1")
            st.session_state.content["enable_section2"] = st.checkbox("Section 2", value=st.session_state.content.get("enable_section2", True), key="enable_section2")
        with col_t2:
            st.session_state.content["enable_section3"] = st.checkbox("Section 3", value=st.session_state.content.get("enable_section3", True), key="enable_section3")
            st.session_state.content["enable_key_insight"] = st.checkbox("Key Insight", value=st.session_state.content.get("enable_key_insight", True), key="enable_key_insight")
            st.session_state.content["enable_action_step"] = st.checkbox("Action Step", value=st.session_state.content.get("enable_action_step", True), key="enable_action_step")
        
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
        if st.session_state.content.get("enable_section1", True):
            st.session_state.content["section1_title"] = st.text_input("Section 1 Title", value=st.session_state.content.get("section1_title", ""), key="section1_title")
            
            # Granular toggles for what to show
            st.caption("Show/Hide Elements:")
            col_a, col_b = st.columns(2)
            with col_a:
                st.session_state.content["section1_show_content"] = st.checkbox("Show Content", value=st.session_state.content.get("section1_show_content", True), key="s1_show_content")
                st.session_state.content["section1_show_question"] = st.checkbox("Show Question", value=st.session_state.content.get("section1_show_question", True), key="s1_show_question")
            with col_b:
                st.session_state.content["section1_show_key_truth"] = st.checkbox("Show Key Truth", value=st.session_state.content.get("section1_show_key_truth", True), key="s1_show_truth")
                st.session_state.content["section1_show_interactive"] = st.checkbox("Show Interactive", value=st.session_state.content.get("section1_show_interactive", True), key="s1_show_interactive")
            
            st.session_state.content["section1_content"] = st.text_area("Section 1 Content", value=st.session_state.content.get("section1_content", ""), key="section1_content", height=150)
            st.session_state.content["section1_question"] = st.text_area("Section 1 Discussion Question", value=st.session_state.content.get("section1_question", ""), key="section1_question", height=80)
            st.session_state.content["section1_key_truth"] = st.text_area("Section 1 Key Truth", value=st.session_state.content.get("section1_key_truth", ""), key="section1_key_truth", height=60)
            st.caption("Interactive Elements:")
            st.session_state.content["section1_interactive_question"] = st.text_input("Interactive Question", value=st.session_state.content.get("section1_interactive_question", "When have you felt distant from God?"), key="section1_interactive_question")
            st.session_state.content["section1_enable_struggles_selector"] = st.checkbox("Show struggles selector", value=st.session_state.content.get("section1_enable_struggles_selector", True), key="section1_enable_struggles_selector")
        else:
            st.info("⚠️ Section 1 is disabled. Enable it above to edit.")
        
        st.markdown("---")
        
        # Section 2
        st.subheader("Section 2")
        if st.session_state.content.get("enable_section2", True):
            st.session_state.content["section2_title"] = st.text_input("Section 2 Title", value=st.session_state.content.get("section2_title", ""), key="section2_title")
            
            # Granular toggles
            st.caption("Show/Hide Elements:")
            col_a, col_b = st.columns(2)
            with col_a:
                st.session_state.content["section2_show_content"] = st.checkbox("Show Content", value=st.session_state.content.get("section2_show_content", True), key="s2_show_content")
                st.session_state.content["section2_show_question"] = st.checkbox("Show Question", value=st.session_state.content.get("section2_show_question", True), key="s2_show_question")
            with col_b:
                st.session_state.content["section2_show_key_truth"] = st.checkbox("Show Key Truth", value=st.session_state.content.get("section2_show_key_truth", True), key="s2_show_truth")
                st.session_state.content["section2_show_interactive"] = st.checkbox("Show Interactive", value=st.session_state.content.get("section2_show_interactive", True), key="s2_show_interactive")
            
            st.session_state.content["section2_content"] = st.text_area("Section 2 Content", value=st.session_state.content.get("section2_content", ""), key="section2_content", height=150)
            st.session_state.content["section2_question"] = st.text_area("Section 2 Discussion Question", value=st.session_state.content.get("section2_question", ""), key="section2_question", height=80)
            st.session_state.content["section2_key_truth"] = st.text_area("Section 2 Key Trust", value=st.session_state.content.get("section2_key_truth", ""), key="section2_key_truth", height=60)
            st.caption("Interactive Elements:")
            st.session_state.content["section2_interactive_question"] = st.text_input("Interactive Question", value=st.session_state.content.get("section2_interactive_question", "How can we create a 'safe space'?"), key="section2_interactive_question")
            st.session_state.content["section2_enable_safespace_selector"] = st.checkbox("Show safe space selector", value=st.session_state.content.get("section2_enable_safespace_selector", True), key="section2_enable_safespace_selector")
        else:
            st.info("⚠️ Section 2 is disabled. Enable it above to edit.")
        
        st.markdown("---")
        
        # Section 3
        st.subheader("Section 3")
        if st.session_state.content.get("enable_section3", True):
            st.session_state.content["section3_title"] = st.text_input("Section 3 Title", value=st.session_state.content.get("section3_title", ""), key="section3_title")
            
            # Granular toggles
            st.caption("Show/Hide Elements:")
            col_a, col_b = st.columns(2)
            with col_a:
                st.session_state.content["section3_show_content"] = st.checkbox("Show Content", value=st.session_state.content.get("section3_show_content", True), key="s3_show_content")
                st.session_state.content["section3_show_question"] = st.checkbox("Show Question", value=st.session_state.content.get("section3_show_question", True), key="s3_show_question")
            with col_b:
                st.session_state.content["section3_show_key_truth"] = st.checkbox("Show Key Truth", value=st.session_state.content.get("section3_show_key_truth", True), key="s3_show_truth")
                st.session_state.content["section3_show_interactive"] = st.checkbox("Show Interactive", value=st.session_state.content.get("section3_show_interactive", True), key="s3_show_interactive")
            
            st.session_state.content["section3_content"] = st.text_area("Section 3 Content", value=st.session_state.content.get("section3_content", ""), key="section3_content", height=150)
            st.session_state.content["section3_question"] = st.text_area("Section 3 Discussion Question", value=st.session_state.content.get("section3_question", ""), key="section3_question", height=80)
            st.session_state.content["section3_key_truth"] = st.text_area("Section 3 Key Truth", value=st.session_state.content.get("section3_key_truth", ""), key="section3_key_truth", height=60)
            st.caption("Interactive Elements:")
            st.session_state.content["section3_interactive_question"] = st.text_input("Interactive Question", value=st.session_state.content.get("section3_interactive_question", "Who needs mercy in your circle?"), key="section3_interactive_question")
            st.session_state.content["section3_enable_person_input"] = st.checkbox("Show person input field", value=st.session_state.content.get("section3_enable_person_input", True), key="section3_enable_person_input")
        else:
            st.info("⚠️ Section 3 is disabled. Enable it above to edit.")
        
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

        st.markdown("---")

        # ── Document Import ────────────────────────────────────────────────
        st.subheader("📥 Import New Study Content")
        st.caption("Paste a public Google Docs link OR upload a .txt file to auto-fill all fields.")

        gdoc_url = st.text_input(
            "Google Docs link (must be 'Anyone with link can view')",
            key="gdoc_url_input",
            placeholder="https://docs.google.com/document/d/.../edit"
        )

        uploaded_file = st.file_uploader("Or upload a .txt file", type=["txt"], key="import_file")

        if st.button("🔍 Preview Parsed Content", use_container_width=True):
            raw_text = None
            with st.spinner("Fetching document..."):
                if gdoc_url:
                    doc_id_match = re.search(r'/d/([a-zA-Z0-9_-]+)', gdoc_url)
                    if doc_id_match:
                        export_url = f"https://docs.google.com/document/d/{doc_id_match.group(1)}/export?format=txt"
                        try:
                            r = requests.get(export_url, timeout=10)
                            if r.status_code == 200:
                                raw_text = r.text
                            else:
                                st.error(f"Could not fetch document ({r.status_code}). Make sure it's publicly shared.")
                        except Exception as ex:
                            st.error(f"Error fetching document: {ex}")
                    else:
                        st.error("Could not extract document ID from URL.")
                elif uploaded_file:
                    raw_text = uploaded_file.read().decode("utf-8", errors="ignore")
                else:
                    st.warning("Please paste a Google Docs URL or upload a .txt file.")

            if raw_text:
                parsed = parse_document_text(raw_text)
                st.session_state.import_preview = parsed
                st.success(f"✅ Parsed! Study: **{parsed.get('study_topic', 'Unknown')}**. Review below, then click Apply.")

        if st.session_state.import_preview:
            with st.expander("📋 Preview parsed fields", expanded=False):
                preview = st.session_state.import_preview
                st.write(f"**Topic:** {preview.get('study_topic','')}")
                st.write(f"**Icebreaker:** {preview.get('icebreaker_text','')[:120]}...")
                st.write(f"**Big Idea:** {preview.get('big_idea','')}")
                st.write(f"**Passage:** {preview.get('passage_name','')} | *{preview.get('key_verse','')}*")
                st.write(f"**S1:** {preview.get('section1_title','')}")
                st.write(f"**S2:** {preview.get('section2_title','')}")
                st.write(f"**S3:** {preview.get('section3_title','')}")
                st.write(f"**Key Insight:** {preview.get('key_insight','')[:120]}...")
                st.write(f"**Action Step:** {preview.get('action_step','')}")

            if st.button("✅ Apply to App & Save", use_container_width=True, type="primary"):
                st.session_state.content.update(st.session_state.import_preview)
                gh_ok, gh_msg = save_content(st.session_state.content)
                st.session_state.import_preview = None
                if gh_ok:
                    st.success("✅ Content applied & pushed to GitHub!")
                else:
                    st.warning(f"Applied locally, push failed: {gh_msg}")
                st.rerun()


# ── Satisfaction Survey (visible to all users) ────────────────────────────────
def section_survey():
    st.markdown("---")
    st.markdown("""
    <div class="gradient-header-green">
        <h2 style="margin-bottom:0.25rem;">📋 Share Your Feedback</h2>
        <p style="opacity:0.9; margin:0;">Help us improve this study experience for your group</p>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.get("survey_submitted"):
        st.markdown("""
        <div class="success-box" style="text-align:center; margin-top:1rem;">
            <h3 style="color:#065F46; margin-bottom:0.5rem;">🙏 Thank you for your feedback!</h3>
            <p style="color:#252628;">Your response has been recorded. God bless you this week!</p>
        </div>
        """, unsafe_allow_html=True)
        return

    with st.form("survey_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Your Name", placeholder="Optional")
        with col2:
            group = st.text_input("Small Group / Campus", placeholder="Optional")

        rating = st.radio(
            "Overall Satisfaction ⭐",
            options=[1, 2, 3, 4, 5],
            format_func=lambda x: "⭐" * x,
            horizontal=True,
            index=4
        )
        resonated = st.text_area(
            "What resonated with you most from today's study?",
            height=100,
            placeholder="Share what stood out to you..."
        )
        suggestions = st.text_area(
            "Any suggestions or feedback for us?",
            height=80,
            placeholder="We'd love to hear how we can improve!"
        )

        submitted = st.form_submit_button("Submit Feedback 💬", use_container_width=True)

    if submitted:
        with st.spinner("Saving your response..."):
            ok, msg = submit_survey({
                "name": name,
                "group": group,
                "rating": rating,
                "resonated": resonated,
                "suggestions": suggestions,
            })
        if ok:
            st.session_state.survey_submitted = True
            st.rerun()
        else:
            st.error(f"Could not save your response: {msg}")


# Section 0: Complete Reading Material (Now LAST page - Summary)
def section_0_reading():
    content = st.session_state.content
    
    st.markdown(f"""
    <div class="gradient-header">
        <h1>📖 Complete Study Summary</h1>
        <p style="font-size: 1.2rem; margin-top: 0.5rem; opacity: 0.9;">{content.get('study_topic', '')}</p>
        <p style="font-size: 0.9rem; margin-top: 0.25rem; opacity: 0.75;">A complete reference guide for this week's study</p>
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
    
    # Section 1 - with granular toggles
    if content.get("enable_section1", True):
        st.markdown(f'<div class="section-1"><h2 style="color: #6F6354; margin-bottom: 1rem;">Section 1: {content.get("section1_title", "")}</h2>', unsafe_allow_html=True)
        
        # Content paragraph
        if content.get("section1_show_content", True):
            st.markdown(f'<p style="color: #252628; line-height: 1.6; margin-bottom: 1rem;">{content.get("section1_content", "")}</p>', unsafe_allow_html=True)
        
        # Discussion question
        if content.get("section1_show_question", True):
            st.markdown(f"""
            <div class="discussion-box">
                <p style="color: #6F6354; font-weight: 600; margin-bottom: 0.5rem;">Discussion Question:</p>
                <p style="color: #252628; font-style: italic;">{content.get("section1_question", "")}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Key truth
        if content.get("section1_show_key_truth", True):
            st.markdown(f"""
            <div class="proof-box">
                <p style="color: #6F6354; font-size: 0.9rem; font-weight: 600; margin-bottom: 0.5rem;">KEY TRUTH:</p>
                <p style="color: #252628; font-style: italic;">{content.get("section1_key_truth", "")}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Section 2 - with granular toggles
    if content.get("enable_section2", True):
        st.markdown(f'<div class="section-2"><h2 style="color: #6F6354; margin-bottom: 1rem;">Section 2: {content.get("section2_title", "")}</h2>', unsafe_allow_html=True)
        
        if content.get("section2_show_content", True):
            st.markdown(f'<p style="color: #252628; line-height: 1.6; margin-bottom: 1rem;">{content.get("section2_content", "")}</p>', unsafe_allow_html=True)
        
        if content.get("section2_show_question", True):
            st.markdown(f"""
            <div class="discussion-box">
                <p style="color: #6F6354; font-weight: 600; margin-bottom: 0.5rem;">Discussion Question:</p>
                <p style="color: #252628; font-style: italic;">{content.get("section2_question", "")}</p>
            </div>
            """, unsafe_allow_html=True)
        
        if content.get("section2_show_key_truth", True):
            st.markdown(f"""
            <div class="proof-box">
                <p style="color: #6F6354; font-size: 0.9rem; font-weight: 600; margin-bottom: 0.5rem;">KEY TRUTH:</p>
                <p style="color: #252628; font-style: italic;">{content.get("section2_key_truth", "")}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Section 3 - with granular toggles
    if content.get("enable_section3", True):
        st.markdown(f'<div class="section-3"><h2 style="color: #6F6354; margin-bottom: 1rem;">Section 3: {content.get("section3_title", "")}</h2>', unsafe_allow_html=True)
        
        if content.get("section3_show_content", True):
            st.markdown(f'<p style="color: #252628; line-height: 1.6; margin-bottom: 1rem;">{content.get("section3_content", "")}</p>', unsafe_allow_html=True)
        
        if content.get("section3_show_question", True):
            st.markdown(f"""
            <div class="discussion-box">
                <p style="color: #6F6354; font-weight: 600; margin-bottom: 0.5rem;">Discussion Question:</p>
                <p style="color: #252628; font-style: italic;">{content.get("section3_question", "")}</p>
            </div>
            """, unsafe_allow_html=True)
        
        if content.get("section3_show_key_truth", True):
            st.markdown(f"""
            <div class="proof-box">
                <p style="color: #6F6354; font-size: 0.9rem; font-weight: 600; margin-bottom: 0.5rem;">KEY TRUTH:</p>
                <p style="color: #252628; font-style: italic;">{content.get("section3_key_truth", "")}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
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
    
    # Thank you message at the end
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="success-box" style="text-align: center;">
        <h3 style="color: #065F46; margin-bottom: 1rem;">✨ Thank you for completing this study! ✨</h3>
        <p style="color: #252628; line-height: 1.6;">
            May God bless you as you apply these truths in your life this week.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Satisfaction survey
    section_survey()


# Section 1: Welcome/Intro (First Page)
def section_1_intro():
    content = st.session_state.content
    
    # Add title and context first
    st.markdown(f"""
    <div class="gradient-header">
        <h1>{content.get('main_title', '')}</h1>
        <p style="font-size: 1.2rem; margin-top: 0.5rem; opacity: 0.9;">{content.get('study_topic', '')}</p>
        <p style="font-size: 0.9rem; margin-top: 0.25rem; opacity: 0.75;">{content.get('context', '')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="gradient-header-blue">
        <h2 style="font-size: 2rem; margin-bottom: 0.5rem;">Welcome to Your Interactive Journey</h2>
        <p style="font-size: 1.1rem; opacity: 0.9;">Let's explore together</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Add ice breaker
    st.markdown(f"""
    <div class="ice-breaker-box">
        <h3 style="color: #6F6354; margin-bottom: 1rem;">Ice Breaker: {content.get('icebreaker_title', '')}</h3>
        <p style="color: #252628; line-height: 1.6;">
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
    
    # Content
    if content.get("section1_show_content", True):
        st.markdown(f"""
        <div class="blue-box">
            <h3 style="color: #1E40AF; font-size: 1.5rem; margin-bottom: 1rem;">Section 1: {content.get('section1_title', '')}</h3>
            <p style="color: #252628; line-height: 1.6;">
                {content.get('section1_content', '')}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Interactive selector
    if content.get("section1_show_interactive", True):
        st.markdown(f"""
        <div class="yellow-box">
            <h4 style="color: #92400E; font-size: 1.2rem; margin-bottom: 1rem;">{content.get('section1_interactive_question', 'When have you felt distant from God?')}</h4>
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
    
    # Discussion question
    if content.get("section1_show_question", True):
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
    
    # Key truth
    if content.get("section1_show_key_truth", True):
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
    
    # Content
    if content.get("section2_show_content", True):
        st.markdown(f"""
        <div class="orange-box">
            <h3 style="color: #9A3412; font-size: 1.5rem; margin-bottom: 1rem;">Section 2: {content.get('section2_title', '')}</h3>
            <p style="color: #252628; line-height: 1.6;">
                {content.get('section2_content', '')}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Interactive selector
    if content.get("section2_show_interactive", True):
        st.markdown(f"""
        <div class="green-box">
            <h4 style="color: #065F46; font-size: 1.2rem; margin-bottom: 1rem;">{content.get('section2_interactive_question', 'How can we create a "safe space"?')}</h4>
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
    
    # Discussion question
    if content.get("section2_show_question", True):
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
    
    # Key truth
    if content.get("section2_show_key_truth", True):
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
    
    # Content
    if content.get("section3_show_content", True):
        st.markdown(f"""
        <div class="green-box">
            <h3 style="color: #065F46; font-size: 1.5rem; margin-bottom: 1rem;">Section 3: {content.get('section3_title', '')}</h3>
            <p style="color: #252628; line-height: 1.6;">
                {content.get('section3_content', '')}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Interactive input
    if content.get("section3_show_interactive", True):
        st.markdown(f"""
        <div class="yellow-box">
            <h4 style="color: #92400E; font-size: 1.2rem; margin-bottom: 1rem;">{content.get('section3_interactive_question', 'Who needs mercy in your circle?')}</h4>
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
    
    # Discussion question
    if content.get("section3_show_question", True):
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
    
    # Key truth
    if content.get("section3_show_key_truth", True):
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

    # ── Save My Answers (user login required) ─────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    if st.session_state.get("user_logged_in"):
        if st.session_state.action_commitment:
            if st.button("💾 Save My Answers", use_container_width=True, type="primary", key="_usr_history_save_answers"):
                save_current_answers(st.session_state.current_username)
                st.success(
                    f"✅ Answers saved for **{st.session_state.current_username}**! "
                    "Click **My Past Answers** at the top to review them."
                )
        else:
            st.info("✏️ Write your commitment above to unlock **Save My Answers**.")
    else:
        st.markdown("""
        <div style="background-color:#F5EFE0;border:1px dashed #C9A962;
                    padding:1rem;border-radius:0.5rem;text-align:center;margin-top:0.5rem;">
            <p style="color:#6F6354;margin:0;">💡 <strong>Sign in</strong> at the top of the page
            to save your answers and review them later!</p>
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
    # ── User login / past-answers routing ────────────────────────────────────
    if st.session_state.get("show_past_answers") and st.session_state.get("user_logged_in"):
        show_past_answers()
        return

    if st.session_state.get("show_user_login") and not st.session_state.get("user_logged_in"):
        show_user_login()
        return

    # ── User strip (signed-in) or guest banner ────────────────────────────────
    if st.session_state.get("user_logged_in"):
        uname = st.session_state.current_username
        col_u1, col_u2, col_u3 = st.columns([4, 2, 1])
        with col_u1:
            st.markdown(
                f"<p style='color:#6F6354;font-weight:600;margin:0;padding-top:0.4rem;'>"
                f"👤 Signed in as <strong>{uname}</strong></p>",
                unsafe_allow_html=True
            )
        with col_u2:
            if st.button("📚 My Past Answers", key="_usr_history_view_past", use_container_width=True):
                st.session_state.show_past_answers = True
                st.rerun()
        with col_u3:
            if st.button("Sign Out", key="_usr_history_signout", use_container_width=True):
                st.session_state.user_logged_in = False
                st.session_state.current_username = ''
                st.rerun()
        st.markdown("<hr style='margin:0.4rem 0;border-color:#D0CFC9;'>", unsafe_allow_html=True)
    else:
        col_b1, col_b2 = st.columns([5, 1])
        with col_b1:
            st.markdown(
                "<p style='color:#8A877E;font-size:0.9rem;margin:0;padding-top:0.4rem;'>"
                "💡 Sign in to save your answers and view your study history</p>",
                unsafe_allow_html=True
            )
        with col_b2:
            if st.button("Sign In", key="_usr_history_signin_banner", use_container_width=True):
                st.session_state.show_user_login = True
                st.rerun()
        st.markdown("<hr style='margin:0.4rem 0;border-color:#D0CFC9;'>", unsafe_allow_html=True)

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
    
    # Main content - Restructured order
    sections = [
        {"id": "intro", "title": "Welcome", "func": section_1_intro},
        {"id": "change", "title": "Section 1", "func": section_2_change_of_heart},
        {"id": "responsibility", "title": "Section 2", "func": section_3_shared_responsibility},
        {"id": "mission", "title": "Section 3", "func": section_4_mission_of_mercy},
        {"id": "action", "title": "Your Action Step", "func": section_5_action_step},
        {"id": "reading", "title": "Complete Summary", "func": section_0_reading}
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
import base64
import requests
import pandas as pd
import io
from datetime import datetime
from pathlib import Path
import hashlib
import re

# Page configuration
st.set_page_config(
    page_title="BANIG Bible Study",
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

    /* ── Dark Mode Overrides ───────────────────────────────────────── */
    @media (prefers-color-scheme: dark) {

        /* Streamlit root backgrounds */
        .stApp, .main, [data-testid="stAppViewContainer"],
        [data-testid="stHeader"], section.main > div {
            background-color: #1a1917 !important;
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: #26231f !important;
        }

        /* ── Box components ─────────────────────────────────────────── */
        .ice-breaker-box {
            background-color: #2a2520 !important;
            border-left-color: #C9A962 !important;
        }
        .big-idea-box {
            background-color: #26231f !important;
            border-color: #8A7B6A !important;
        }
        .passage-box {
            background-color: #26231f !important;
            border-color: #6F6354 !important;
        }
        .discussion-box {
            background-color: #20202e !important;
            border-color: #6B5B8A !important;
        }
        .proof-box {
            background-color: #26231f !important;
            border-left-color: #8A7B6A !important;
        }
        .yellow-box {
            background-color: #2d2510 !important;
            border-color: #B8860B !important;
        }
        .blue-box {
            background-color: #111827 !important;
            border-color: #2563EB !important;
        }
        .orange-box {
            background-color: #2d1a0d !important;
            border-color: #C2510A !important;
        }
        .green-box {
            background-color: #0d2318 !important;
            border-color: #059669 !important;
        }
        .success-box {
            background-color: #0d2318 !important;
            border-color: #5A8A56 !important;
        }
        .login-box {
            background-color: #2a2520 !important;
            box-shadow: 0 4px 16px rgba(0,0,0,0.5) !important;
        }

        /* ── Text inside boxes in dark mode ────────────────────────── */

        /* Main body text that was hardcoded #252628 (near-black → near-white) */
        .ice-breaker-box p,
        .big-idea-box p,
        .passage-box p,
        .discussion-box p,
        .proof-box p,
        .yellow-box p,
        .blue-box p,
        .orange-box p,
        .green-box p,
        .success-box p {
            color: #e8e3dc !important;
        }

        /* Headings that used the brand brown — lighten it so it's readable */
        .ice-breaker-box h2, .ice-breaker-box h3,
        .big-idea-box h2, .big-idea-box h3,
        .passage-box h2, .passage-box h3,
        .proof-box p:first-child,
        .discussion-box h4 {
            color: #C9A962 !important;
        }

        /* Blue-box headings */
        .blue-box h3, .blue-box h2 {
            color: #93C5FD !important;
        }

        /* Orange-box headings */
        .orange-box h3, .orange-box h2 {
            color: #FDBA74 !important;
        }

        /* Green-box headings */
        .green-box h4, .green-box h2 {
            color: #6EE7B7 !important;
        }

        /* Success-box headings */
        .success-box h3 {
            color: #6EE7B7 !important;
        }

        /* Verse reference grey */
        .passage-box p[style*="6B7280"] {
            color: #9CA3AF !important;
        }

        /* Streamlit generic text */
        .stMarkdown p, .stMarkdown li, label {
            color: #e8e3dc !important;
        }

        /* Section divider accents */
        .section-1 { border-top-color: #8A7B6A !important; }
        .section-2 { border-top-color: #6F6354 !important; }
        .section-3 { border-top-color: #5A8A56 !important; }

        /* Stacked inline styles from Python — catch-all for very dark text */
        [style*="color: #252628"],
        [style*="color:#252628"] {
            color: #e8e3dc !important;
        }
        [style*="color: #1F2937"],
        [style*="color:#1F2937"] {
            color: #D1D5DB !important;
        }
        [style*="color: #1E40AF"],
        [style*="color:#1E40AF"] {
            color: #93C5FD !important;
        }
        [style*="color: #9A3412"],
        [style*="color:#9A3412"] {
            color: #FDBA74 !important;
        }
        [style*="color: #92400E"],
        [style*="color:#92400E"] {
            color: #FCD34D !important;
        }
        [style*="color: #065F46"],
        [style*="color:#065F46"] {
            color: #6EE7B7 !important;
        }
        [style*="color: #6B7280"],
        [style*="color:#6B7280"] {
            color: #9CA3AF !important;
        }
        [style*="color: #6F6354"],
        [style*="color:#6F6354"] {
            color: #C9A962 !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# File paths
CONTENT_FILE = Path("igrow_content.json")
USER_ANSWERS_FILE = Path("igrow_user_answers.json")
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
            
            "enable_icebreaker": True,
            "enable_section1": True,
            "enable_section2": True,
            "enable_section3": True,
            "enable_key_insight": True,
            "enable_action_step": True,
            
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
            "section1_interactive_question": "When have you felt distant from God?",
            "section1_enable_struggles_selector": True,
            "section1_show_content": True,
            "section1_show_question": True,
            "section1_show_key_truth": True,
            "section1_show_interactive": True,
            "section2_title": "Our Shared Responsibility",
            "section2_content": "In our communities, we often find it easy to judge others while excusing ourselves. Ezekiel reminds us that God is impartial, meaning He holds everyone to the same standard of love and justice. As a group, we are called to be like \"watchmen\" who look out for one another's spiritual well-being. This is not about being \"judgy,\" but about caring enough to speak up when we see a friend heading toward a \"dead end.\" Our relationships grow deeper when we create a space where it is safe to admit we are wrong and encourage each other to stay on the right path. We represent God's fairness by being consistent in how we treat people, regardless of their background or status.",
            "section2_question": "How can we make our group a \"safe space\" where it's okay to admit mistakes without feeling judged by others? (Ano yung isang thing na pwede nating gawin para mas maging supportive sa isa't isa?)",
            "section2_key_truth": "True community happens when we're consistent in how we treat everyone, creating space where it's safe to admit mistakes and grow together.",
            "section2_interactive_question": "How can we create a 'safe space'?",
            "section2_enable_safespace_selector": True,
            "section2_show_content": True,
            "section2_show_question": True,
            "section2_show_key_truth": True,
            "section2_show_interactive": True,
            "section3_title": "A Mission of Mercy",
            "section3_content": "The story of the conquest in Joshua and the warnings in Ezekiel show that God intervenes only when evil begins to destroy everything good. Our mission today is to share the \"Good News\" that there is always a way out of toxic cycles and harmful lifestyles. Just as Rahab found safety in the middle of a city facing judgment, God is looking for \"outsiders\" to bring into His family. We are sent to our campuses and offices not to condemn people, but to offer them the same mercy we have received. When we live out this mission, we show the world that God's ultimate goal is not to \"win a war,\" but to save as many people as possible.",
            "section3_question": "Sino yung \"unlikely person\" sa workplace or school mo na feeling mo kailangan ng encouragement or mercy ngayon? (How can you show them God's kindness this week without sounding like you are lecturing them?)",
            "section3_key_truth": "God's ultimate goal isn't to \"win a war\" but to save as many people as possible. When we show mercy, we reveal His true heart.",
            "section3_interactive_question": "Who needs mercy in your circle?",
            "section3_enable_person_input": True,
            "section3_show_content": True,
            "section3_show_question": True,
            "section3_show_key_truth": True,
            "section3_show_interactive": True,
            "key_insight": "It is easy to look at the stories of judgment in the Bible and feel afraid or confused. But when we look closer at Ezekiel 33, we see a God who is actually \"longsuffering\" and incredibly patient. He waits until the very last second, hoping that just one more person will turn around and live. He does not want anyone to perish, and that includes you, your \"difficult\" boss, or your struggling classmate. This reveals that God is both perfectly just and incredibly kind at the same time. You can trust Him with the things you don't understand because His heart is always moved by love.",
            "action_step": "Identify one person this week who seems to be \"struggling with the consequences\" of a bad choice. Instead of joining in the gossip or judging them, offer them a genuine word of encouragement or a small act of kindness to remind them that there is always a path back to hope.",
            "struggles_list": "Felt like a failure\nMade a big mistake\nDrifted from prayer/Bible reading\nHurt someone I care about\nGave in to temptation\nDoubted God's goodness",
            "safespace_list": "Listen without interrupting\nNo gossip rule\nShare our own struggles first\nPray for each other regularly\nCheck in during the week\nCelebrate small wins together"
        }

def push_to_github(json_str: str):
    """Push the JSON string to GitHub via the Contents API.
    Reads config from st.secrets['github'].
    Returns (success: bool, message: str).
    """
    try:
        gh = st.secrets["github"]
        token    = gh["token"]
        repo     = gh["repo"]       # e.g. "YourUsername/your-repo"
        branch   = gh.get("branch", "main")
        filepath = gh.get("filepath", "igrow_content.json")
    except (KeyError, AttributeError) as e:
        return False, f"Missing GitHub secret: {e}. Check .streamlit/secrets.toml."

    api_url = f"https://api.github.com/repos/{repo}/contents/{filepath}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json",
    }

    # Get current file SHA (required for updates)
    sha = None
    get_resp = requests.get(api_url, headers=headers, params={"ref": branch})
    if get_resp.status_code == 200:
        sha = get_resp.json().get("sha")
    elif get_resp.status_code not in (404,):
        return False, f"GitHub GET failed ({get_resp.status_code}): {get_resp.text[:200]}"

    # Encode content as base64
    encoded = base64.b64encode(json_str.encode("utf-8")).decode("utf-8")

    payload = {
        "message": "chore: update igrow_content.json via CMS",
        "content": encoded,
        "branch": branch,
    }
    if sha:
        payload["sha"] = sha

    put_resp = requests.put(api_url, headers=headers, json=payload)
    if put_resp.status_code in (200, 201):
        return True, "Pushed to GitHub successfully."
    else:
        return False, f"GitHub PUT failed ({put_resp.status_code}): {put_resp.text[:300]}"


def save_content(content):
    """Save content to JSON file and push to GitHub."""
    json_str = json.dumps(content, indent=2, ensure_ascii=False)
    with open(CONTENT_FILE, 'w', encoding='utf-8') as f:
        f.write(json_str)
    return push_to_github(json_str)


# ── User answer helpers ───────────────────────────────────────────────────────
def load_user_answers():
    """Load all user answers from the JSON file."""
    if USER_ANSWERS_FILE.exists():
        with open(USER_ANSWERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def save_user_answers(data):
    """Persist the full user-answers dict to JSON."""
    with open(USER_ANSWERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_user_answers(username):
    """Return the list of saved answer sessions for a given username."""
    data = load_user_answers()
    return data.get(username.strip().lower(), [])


def save_current_answers(username):
    """Snapshot the current session's answers and append to the user's history."""
    content = st.session_state.content
    session = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "study_topic": content.get("study_topic", ""),
        "section1_question": content.get("section1_question", ""),
        "section1_answer": st.session_state.reflections.get("section1", ""),
        "section2_question": content.get("section2_question", ""),
        "section2_answer": st.session_state.reflections.get("section2", ""),
        "section3_question": content.get("section3_question", ""),
        "section3_answer": st.session_state.reflections.get("section3", ""),
        "unlikely_person": st.session_state.unlikely_person,
        "safe_space_ideas": list(st.session_state.safe_space_ideas),
        "selected_struggles": list(st.session_state.selected_struggles),
        "commitment": st.session_state.action_commitment,
    }
    key = username.strip().lower()
    data = load_user_answers()
    data.setdefault(key, []).append(session)
    save_user_answers(data)


# ── Survey helpers ────────────────────────────────────────────────────────────
SURVEY_FILE = "igrow_survey_responses.xlsx"
SURVEY_COLUMNS = ["Timestamp", "Study Topic", "Name", "Group/Campus",
                  "Satisfaction (1-5)", "What Resonated", "Suggestions"]

def fetch_survey_dataframe():
    """Download existing survey Excel from GitHub. Returns (df, sha)."""
    try:
        gh = st.secrets["github"]
        token = gh["token"]
        repo  = gh["repo"]
        branch = gh.get("branch", "main")
    except (KeyError, AttributeError):
        return pd.DataFrame(columns=SURVEY_COLUMNS), None

    url = f"https://api.github.com/repos/{repo}/contents/{SURVEY_FILE}"
    headers = {"Authorization": f"token {token}",
               "Accept": "application/vnd.github+json"}
    resp = requests.get(url, headers=headers, params={"ref": branch})
    if resp.status_code == 200:
        data = resp.json()
        file_bytes = base64.b64decode(data["content"])
        df = pd.read_excel(io.BytesIO(file_bytes), engine="openpyxl")
        return df, data["sha"]
    return pd.DataFrame(columns=SURVEY_COLUMNS), None


def submit_survey(responses: dict):
    """Append a survey response and push updated Excel to GitHub."""
    df, sha = fetch_survey_dataframe()
    new_row = {
        "Timestamp":        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Study Topic":      st.session_state.content.get("study_topic", ""),
        "Name":             responses.get("name", ""),
        "Group/Campus":     responses.get("group", ""),
        "Satisfaction (1-5)": responses.get("rating", ""),
        "What Resonated":   responses.get("resonated", ""),
        "Suggestions":      responses.get("suggestions", ""),
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    buffer = io.BytesIO()
    df.to_excel(buffer, index=False, engine="openpyxl")
    encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")

    try:
        gh = st.secrets["github"]
        token = gh["token"]
        repo  = gh["repo"]
        branch = gh.get("branch", "main")
    except (KeyError, AttributeError) as e:
        return False, f"Missing secret: {e}"

    url = f"https://api.github.com/repos/{repo}/contents/{SURVEY_FILE}"
    headers = {"Authorization": f"token {token}",
               "Accept": "application/vnd.github+json"}
    payload = {"message": "chore: add survey response",
               "content": encoded, "branch": branch}
    if sha:
        payload["sha"] = sha
    resp = requests.put(url, headers=headers, json=payload)
    return (True, "Submitted!") if resp.status_code in (200, 201) \
        else (False, f"Push failed ({resp.status_code}): {resp.text[:200]}")


# ── Document import (pattern matching) ───────────────────────────────────────
def parse_document_text(text: str) -> dict:
    """
    Parse a plain-text Bible study guide into CMS content fields.
    Expected format (same as I-Grow Google Docs template):
      Line 1: Study Title
      Icebreaker <text>
      Big Idea <text>
      Passage & Key Text <Ref> "<verse>" - <ref>
      <Section heading>\n<body paragraphs>\n<Discussion question?>
      Key Insight <text>
      Action Step <text>
    """
    # Normalise line endings
    lines = [l.strip() for l in text.replace('\r\n', '\n').split('\n')]
    # Remove divider lines
    lines = [l for l in lines if not re.match(r'^[_\-=]{4,}$', l)]
    full = '\n'.join(lines)

    content = {}

    # ── Title ────────────────────────────────────────────────────────────────
    # First non-empty line is the title (may be repeated — take first)
    title_lines = [l for l in lines if l]
    content["study_topic"] = title_lines[0] if title_lines else ""
    content["icebreaker_title"] = content["study_topic"]
    content["main_title"] = "I-Grow Discipleship Guide"
    content["context"] = "Context: Campus and Workplace Small Groups (Philippines)"

    # ── Icebreaker ───────────────────────────────────────────────────────────
    m = re.search(r'Icebreaker\s+(.+?)(?=Big Idea|Passage|\Z)', full, re.S | re.I)
    content["icebreaker_text"] = m.group(1).strip() if m else ""

    # ── Big Idea ─────────────────────────────────────────────────────────────
    m = re.search(r'Big Idea\s+(.+?)(?=Passage|\Z)', full, re.S | re.I)
    content["big_idea"] = m.group(1).strip() if m else ""

    # ── Passage & Key Verse ──────────────────────────────────────────────────
    m = re.search(r'Passage\s*&?\s*Key Text\s+(.+?)(?=\n)', full, re.I)
    if m:
        passage_line = m.group(1).strip()
        # passage ref is before the quoted verse
        ref_match = re.match(r'([^"]+)', passage_line)
        content["passage_name"] = ref_match.group(1).strip() if ref_match else passage_line
    else:
        content["passage_name"] = ""

    verse_match = re.search(r'["\u201c](.+?)["\u201d]\s*[\u2013\-]+\s*(.+?)(?=\n|$)', full)
    if verse_match:
        content["key_verse"]       = verse_match.group(1).strip()
        content["verse_reference"] = verse_match.group(2).strip()
    else:
        content["key_verse"] = content["verse_reference"] = ""

    # ── Sections (detect by heading then collect body + questions) ───────────
    # A section heading is a short line (< 60 chars) not matching known keywords
    SKIP_PATTERN = re.compile(
        r'^(Icebreaker|Big Idea|Passage|Key Insight|Action Step|Finding|One God)',
        re.I)
    # Split body after Passage block
    after_passage = re.split(r'Passage\s*&?\s*Key Text.+?(?=\n\n|\n[A-Z])',
                              full, maxsplit=1, flags=re.S | re.I)
    body = after_passage[-1] if len(after_passage) > 1 else full

    # Split on Key Insight to separate section body from ending
    body_parts = re.split(r'Key Insight', body, maxsplit=1, flags=re.I)
    sections_text = body_parts[0]
    ending_text   = body_parts[1] if len(body_parts) > 1 else ""

    # Find section headings: lines < 55 chars, Title Case or ALL CAPS, no period
    section_blocks = []
    sec_lines = sections_text.split('\n')
    current_heading = None
    current_body = []
    for line in sec_lines:
        if (line and len(line) < 55
                and not SKIP_PATTERN.match(line)
                and not line.endswith('?')
                and re.search(r'[A-Z]', line)
                and not re.match(r'^[a-z]', line)):
            if current_heading is not None:
                section_blocks.append((current_heading, '\n'.join(current_body).strip()))
            current_heading = line
            current_body = []
        elif current_heading:
            current_body.append(line)
    if current_heading:
        section_blocks.append((current_heading, '\n'.join(current_body).strip()))

    section_keys = [
        ("section1_title", "section1_content", "section1_question", "section1_key_truth"),
        ("section2_title", "section2_content", "section2_question", "section2_key_truth"),
        ("section3_title", "section3_content", "section3_question", "section3_key_truth"),
    ]

    for i, (heading, body_text) in enumerate(section_blocks[:3]):
        tk, ck, qk, kk = section_keys[i]
        content[tk] = heading

        # Questions are lines ending with ?
        q_lines = [l for l in body_text.split('\n') if l.strip().endswith('?')]
        content[qk] = ' '.join(q_lines).strip()

        # Content = everything except question lines
        non_q = [l for l in body_text.split('\n')
                 if l.strip() and not l.strip().endswith('?')]
        content[ck] = '\n'.join(non_q).strip()

        # Key truth = last non-question sentence of content
        sentences = re.split(r'(?<=[.!])\s+', content[ck])
        content[kk] = sentences[-1].strip() if sentences else ""

    # Fill missing sections with empty strings
    for i in range(len(section_blocks), 3):
        tk, ck, qk, kk = section_keys[i]
        content[tk] = content[ck] = content[qk] = content[kk] = ""

    # ── Key Insight ──────────────────────────────────────────────────────────
    m = re.search(r'Key Insight\s*\n(.+?)(?=Action Step|\Z)', ending_text, re.S | re.I)
    content["key_insight"] = m.group(1).strip() if m else ""

    # ── Action Step ──────────────────────────────────────────────────────────
    m = re.search(r'Action Step\s*\n(.+?)(?=\Z)', ending_text, re.S | re.I)
    content["action_step"] = m.group(1).strip() if m else ""

    # ── Preserve defaults for toggles and interactive lists ──────────────────
    defaults = {
        "enable_icebreaker": True, "enable_section1": True,
        "enable_section2": True,  "enable_section3": True,
        "enable_key_insight": True, "enable_action_step": True,
        "section1_show_content": True, "section1_show_question": True,
        "section1_show_key_truth": True, "section1_show_interactive": True,
        "section1_interactive_question": "When have you felt this way?",
        "section1_enable_struggles_selector": True,
        "section2_show_content": True, "section2_show_question": True,
        "section2_show_key_truth": True, "section2_show_interactive": True,
        "section2_interactive_question": "How can we support each other?",
        "section2_enable_safespace_selector": True,
        "section3_show_content": True, "section3_show_question": True,
        "section3_show_key_truth": True, "section3_show_interactive": True,
        "section3_interactive_question": "Who needs this in your circle?",
        "section3_enable_person_input": True,
        "struggles_list": "Felt confused or lost\nGoing through a dark season\nSearching for meaning\nFeeling isolated or alone\nDoubting God's presence\nStruggling with purpose",
        "safespace_list": "Listen without interrupting\nPray for each other regularly\nCheck in during the week\nShare our own struggles first\nNo gossip rule\nCelebrate each other's victories",
    }
    for k, v in defaults.items():
        content.setdefault(k, v)

    return content


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

if 'survey_submitted' not in st.session_state:
    st.session_state.survey_submitted = False

if 'import_preview' not in st.session_state:
    st.session_state.import_preview = None

if 'user_logged_in' not in st.session_state:
    st.session_state.user_logged_in = False

if 'current_username' not in st.session_state:
    st.session_state.current_username = ''

if 'show_user_login' not in st.session_state:
    st.session_state.show_user_login = False

if 'show_past_answers' not in st.session_state:
    st.session_state.show_past_answers = False

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

# User login interface
def show_user_login():
    st.markdown("""
    <div class="login-box" style="max-width: 440px; margin: 3rem auto; text-align: center;">
        <span style="font-size: 2.5rem;">📖</span>
        <h2 style="color: #6F6354; margin-top: 0.5rem; margin-bottom: 0.25rem;">Sign In</h2>
        <p style="color: #8A877E; font-size: 0.9rem; margin-bottom: 0;">Enter your name to save and review your answers</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        username = st.text_input(
            "Your Name / Username",
            placeholder="e.g. Maria, JohnD …",
            key="_usr_history_login_input"
        )
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Sign In ✓", use_container_width=True, type="primary", key="_usr_history_signin_confirm"):
                if username.strip():
                    st.session_state.user_logged_in = True
                    st.session_state.current_username = username.strip()
                    st.session_state.show_user_login = False
                    st.rerun()
                else:
                    st.error("Please enter your name.")
        with col_b:
            if st.button("Cancel", use_container_width=True, key="_usr_history_login_cancel"):
                st.session_state.show_user_login = False
                st.rerun()


# Past answers viewer
def show_past_answers():
    """Display the current user's past saved answer sessions."""
    username = st.session_state.current_username
    sessions = get_user_answers(username)

    st.markdown(f"""
    <div class="gradient-header-blue">
        <h2 style="margin-bottom: 0.25rem;">📚 My Past Answers</h2>
        <p style="opacity: 0.9; margin: 0;">Signed in as <strong>{username}</strong></p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("← Back to Study", key="_usr_history_back"):
        st.session_state.show_past_answers = False
        st.rerun()

    if not sessions:
        st.markdown("""
        <div class="info-box" style="text-align: center; padding: 2rem; margin-top: 1.5rem;">
            <p style="font-size: 1.1rem; margin: 0;">No saved answers yet.<br>
            Complete a study and hit <strong>💾 Save My Answers</strong>!</p>
        </div>
        """, unsafe_allow_html=True)
        return

    st.markdown(
        f"<p style='color:#8A877E; margin-bottom:1rem;'>{len(sessions)} session(s) saved</p>",
        unsafe_allow_html=True
    )

    data = load_user_answers()
    key = username.strip().lower()

    # Show newest first
    for orig_idx, session in reversed(list(enumerate(sessions))):
        topic = session.get("study_topic", "Bible Study")
        ts = session.get("timestamp", "")
        label = f"📖  {topic}  •  {ts}"
        is_latest = (orig_idx == len(sessions) - 1)

        with st.expander(label, expanded=is_latest):

            def _qa_row(question, answer):
                if question:
                    st.markdown(f"""
                    <div class="discussion-box" style="margin-bottom:0.5rem;">
                        <p style="color:#6F6354;font-weight:600;font-size:0.82rem;margin-bottom:0.25rem;">QUESTION</p>
                        <p style="color:#252628;font-style:italic;margin-bottom:0;">{question}</p>
                    </div>
                    """, unsafe_allow_html=True)
                if answer:
                    st.markdown(f"""
                    <div class="success-box" style="margin-bottom:1rem;">
                        <p style="color:#065F46;font-weight:600;font-size:0.82rem;margin-bottom:0.25rem;">YOUR ANSWER</p>
                        <p style="color:#252628;margin-bottom:0;">{answer}</p>
                    </div>
                    """, unsafe_allow_html=True)
                elif question:
                    st.markdown(
                        "<p style='color:#9CA3AF;font-size:0.85rem;margin-bottom:1rem;'><em>(No answer recorded)</em></p>",
                        unsafe_allow_html=True
                    )

            _qa_row(session.get("section1_question"), session.get("section1_answer"))
            _qa_row(session.get("section2_question"), session.get("section2_answer"))
            _qa_row(session.get("section3_question"), session.get("section3_answer"))

            if session.get("unlikely_person"):
                st.markdown(f"""
                <div class="proof-box" style="margin-bottom:0.5rem;">
                    <p style="color:#6F6354;font-weight:600;font-size:0.82rem;margin-bottom:0.25rem;">PERSON I IDENTIFIED</p>
                    <p style="color:#252628;margin-bottom:0;">{session['unlikely_person']}</p>
                </div>
                """, unsafe_allow_html=True)

            if session.get("commitment"):
                st.markdown(f"""
                <div class="proof-box" style="border-left-color:#7A9B76;margin-bottom:0.5rem;">
                    <p style="color:#6F6354;font-weight:600;font-size:0.82rem;margin-bottom:0.25rem;">MY COMMITMENT</p>
                    <p style="color:#252628;margin-bottom:0;">{session['commitment']}</p>
                </div>
                """, unsafe_allow_html=True)

            if session.get("selected_struggles"):
                st.markdown(
                    "<p style='font-size:0.82rem;color:#6F6354;font-weight:600;margin-bottom:0.25rem;'>STRUGGLES I IDENTIFIED</p>",
                    unsafe_allow_html=True
                )
                st.markdown("  ".join([f"`{s}`" for s in session["selected_struggles"]]))

            if session.get("safe_space_ideas"):
                st.markdown(
                    "<p style='font-size:0.82rem;color:#6F6354;font-weight:600;margin-top:0.5rem;margin-bottom:0.25rem;'>SAFE SPACE IDEAS I CHOSE</p>",
                    unsafe_allow_html=True
                )
                st.markdown("  ".join([f"`{s}`" for s in session["safe_space_ideas"]]))

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🗑️ Delete this entry", key=f"_usr_history_del_{orig_idx}"):
                data[key].pop(orig_idx)
                save_user_answers(data)
                st.success("Entry deleted.")
                st.rerun()


# Admin content editor
def show_admin_editor():
    with st.sidebar:
        st.title("📝 Admin Content Editor")
        st.markdown("---")
        
        if st.button("💾 Save Changes", use_container_width=True, type="primary"):
            gh_ok, gh_msg = save_content(st.session_state.content)
            if gh_ok:
                st.success("✅ Saved & pushed to GitHub!")
            else:
                st.warning(f"💾 Saved locally. GitHub push failed: {gh_msg}")
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()
        
        st.markdown("---")
        
        # Section Visibility Toggles
        st.subheader("🎛️ Section Visibility")
        st.caption("Toggle sections on/off based on your weekly topic")
        
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            st.session_state.content["enable_icebreaker"] = st.checkbox("Ice Breaker", value=st.session_state.content.get("enable_icebreaker", True), key="enable_icebreaker")
            st.session_state.content["enable_section1"] = st.checkbox("Section 1", value=st.session_state.content.get("enable_section1", True), key="enable_section1")
            st.session_state.content["enable_section2"] = st.checkbox("Section 2", value=st.session_state.content.get("enable_section2", True), key="enable_section2")
        with col_t2:
            st.session_state.content["enable_section3"] = st.checkbox("Section 3", value=st.session_state.content.get("enable_section3", True), key="enable_section3")
            st.session_state.content["enable_key_insight"] = st.checkbox("Key Insight", value=st.session_state.content.get("enable_key_insight", True), key="enable_key_insight")
            st.session_state.content["enable_action_step"] = st.checkbox("Action Step", value=st.session_state.content.get("enable_action_step", True), key="enable_action_step")
        
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
        if st.session_state.content.get("enable_section1", True):
            st.session_state.content["section1_title"] = st.text_input("Section 1 Title", value=st.session_state.content.get("section1_title", ""), key="section1_title")
            
            # Granular toggles for what to show
            st.caption("Show/Hide Elements:")
            col_a, col_b = st.columns(2)
            with col_a:
                st.session_state.content["section1_show_content"] = st.checkbox("Show Content", value=st.session_state.content.get("section1_show_content", True), key="s1_show_content")
                st.session_state.content["section1_show_question"] = st.checkbox("Show Question", value=st.session_state.content.get("section1_show_question", True), key="s1_show_question")
            with col_b:
                st.session_state.content["section1_show_key_truth"] = st.checkbox("Show Key Truth", value=st.session_state.content.get("section1_show_key_truth", True), key="s1_show_truth")
                st.session_state.content["section1_show_interactive"] = st.checkbox("Show Interactive", value=st.session_state.content.get("section1_show_interactive", True), key="s1_show_interactive")
            
            st.session_state.content["section1_content"] = st.text_area("Section 1 Content", value=st.session_state.content.get("section1_content", ""), key="section1_content", height=150)
            st.session_state.content["section1_question"] = st.text_area("Section 1 Discussion Question", value=st.session_state.content.get("section1_question", ""), key="section1_question", height=80)
            st.session_state.content["section1_key_truth"] = st.text_area("Section 1 Key Truth", value=st.session_state.content.get("section1_key_truth", ""), key="section1_key_truth", height=60)
            st.caption("Interactive Elements:")
            st.session_state.content["section1_interactive_question"] = st.text_input("Interactive Question", value=st.session_state.content.get("section1_interactive_question", "When have you felt distant from God?"), key="section1_interactive_question")
            st.session_state.content["section1_enable_struggles_selector"] = st.checkbox("Show struggles selector", value=st.session_state.content.get("section1_enable_struggles_selector", True), key="section1_enable_struggles_selector")
        else:
            st.info("⚠️ Section 1 is disabled. Enable it above to edit.")
        
        st.markdown("---")
        
        # Section 2
        st.subheader("Section 2")
        if st.session_state.content.get("enable_section2", True):
            st.session_state.content["section2_title"] = st.text_input("Section 2 Title", value=st.session_state.content.get("section2_title", ""), key="section2_title")
            
            # Granular toggles
            st.caption("Show/Hide Elements:")
            col_a, col_b = st.columns(2)
            with col_a:
                st.session_state.content["section2_show_content"] = st.checkbox("Show Content", value=st.session_state.content.get("section2_show_content", True), key="s2_show_content")
                st.session_state.content["section2_show_question"] = st.checkbox("Show Question", value=st.session_state.content.get("section2_show_question", True), key="s2_show_question")
            with col_b:
                st.session_state.content["section2_show_key_truth"] = st.checkbox("Show Key Truth", value=st.session_state.content.get("section2_show_key_truth", True), key="s2_show_truth")
                st.session_state.content["section2_show_interactive"] = st.checkbox("Show Interactive", value=st.session_state.content.get("section2_show_interactive", True), key="s2_show_interactive")
            
            st.session_state.content["section2_content"] = st.text_area("Section 2 Content", value=st.session_state.content.get("section2_content", ""), key="section2_content", height=150)
            st.session_state.content["section2_question"] = st.text_area("Section 2 Discussion Question", value=st.session_state.content.get("section2_question", ""), key="section2_question", height=80)
            st.session_state.content["section2_key_truth"] = st.text_area("Section 2 Key Trust", value=st.session_state.content.get("section2_key_truth", ""), key="section2_key_truth", height=60)
            st.caption("Interactive Elements:")
            st.session_state.content["section2_interactive_question"] = st.text_input("Interactive Question", value=st.session_state.content.get("section2_interactive_question", "How can we create a 'safe space'?"), key="section2_interactive_question")
            st.session_state.content["section2_enable_safespace_selector"] = st.checkbox("Show safe space selector", value=st.session_state.content.get("section2_enable_safespace_selector", True), key="section2_enable_safespace_selector")
        else:
            st.info("⚠️ Section 2 is disabled. Enable it above to edit.")
        
        st.markdown("---")
        
        # Section 3
        st.subheader("Section 3")
        if st.session_state.content.get("enable_section3", True):
            st.session_state.content["section3_title"] = st.text_input("Section 3 Title", value=st.session_state.content.get("section3_title", ""), key="section3_title")
            
            # Granular toggles
            st.caption("Show/Hide Elements:")
            col_a, col_b = st.columns(2)
            with col_a:
                st.session_state.content["section3_show_content"] = st.checkbox("Show Content", value=st.session_state.content.get("section3_show_content", True), key="s3_show_content")
                st.session_state.content["section3_show_question"] = st.checkbox("Show Question", value=st.session_state.content.get("section3_show_question", True), key="s3_show_question")
            with col_b:
                st.session_state.content["section3_show_key_truth"] = st.checkbox("Show Key Truth", value=st.session_state.content.get("section3_show_key_truth", True), key="s3_show_truth")
                st.session_state.content["section3_show_interactive"] = st.checkbox("Show Interactive", value=st.session_state.content.get("section3_show_interactive", True), key="s3_show_interactive")
            
            st.session_state.content["section3_content"] = st.text_area("Section 3 Content", value=st.session_state.content.get("section3_content", ""), key="section3_content", height=150)
            st.session_state.content["section3_question"] = st.text_area("Section 3 Discussion Question", value=st.session_state.content.get("section3_question", ""), key="section3_question", height=80)
            st.session_state.content["section3_key_truth"] = st.text_area("Section 3 Key Truth", value=st.session_state.content.get("section3_key_truth", ""), key="section3_key_truth", height=60)
            st.caption("Interactive Elements:")
            st.session_state.content["section3_interactive_question"] = st.text_input("Interactive Question", value=st.session_state.content.get("section3_interactive_question", "Who needs mercy in your circle?"), key="section3_interactive_question")
            st.session_state.content["section3_enable_person_input"] = st.checkbox("Show person input field", value=st.session_state.content.get("section3_enable_person_input", True), key="section3_enable_person_input")
        else:
            st.info("⚠️ Section 3 is disabled. Enable it above to edit.")
        
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

        st.markdown("---")

        # ── Document Import ────────────────────────────────────────────────
        st.subheader("📥 Import New Study Content")
        st.caption("Paste a public Google Docs link OR upload a .txt file to auto-fill all fields.")

        gdoc_url = st.text_input(
            "Google Docs link (must be 'Anyone with link can view')",
            key="gdoc_url_input",
            placeholder="https://docs.google.com/document/d/.../edit"
        )

        uploaded_file = st.file_uploader("Or upload a .txt file", type=["txt"], key="import_file")

        if st.button("🔍 Preview Parsed Content", use_container_width=True):
            raw_text = None
            with st.spinner("Fetching document..."):
                if gdoc_url:
                    doc_id_match = re.search(r'/d/([a-zA-Z0-9_-]+)', gdoc_url)
                    if doc_id_match:
                        export_url = f"https://docs.google.com/document/d/{doc_id_match.group(1)}/export?format=txt"
                        try:
                            r = requests.get(export_url, timeout=10)
                            if r.status_code == 200:
                                raw_text = r.text
                            else:
                                st.error(f"Could not fetch document ({r.status_code}). Make sure it's publicly shared.")
                        except Exception as ex:
                            st.error(f"Error fetching document: {ex}")
                    else:
                        st.error("Could not extract document ID from URL.")
                elif uploaded_file:
                    raw_text = uploaded_file.read().decode("utf-8", errors="ignore")
                else:
                    st.warning("Please paste a Google Docs URL or upload a .txt file.")

            if raw_text:
                parsed = parse_document_text(raw_text)
                st.session_state.import_preview = parsed
                st.success(f"✅ Parsed! Study: **{parsed.get('study_topic', 'Unknown')}**. Review below, then click Apply.")

        if st.session_state.import_preview:
            with st.expander("📋 Preview parsed fields", expanded=False):
                preview = st.session_state.import_preview
                st.write(f"**Topic:** {preview.get('study_topic','')}")
                st.write(f"**Icebreaker:** {preview.get('icebreaker_text','')[:120]}...")
                st.write(f"**Big Idea:** {preview.get('big_idea','')}")
                st.write(f"**Passage:** {preview.get('passage_name','')} | *{preview.get('key_verse','')}*")
                st.write(f"**S1:** {preview.get('section1_title','')}")
                st.write(f"**S2:** {preview.get('section2_title','')}")
                st.write(f"**S3:** {preview.get('section3_title','')}")
                st.write(f"**Key Insight:** {preview.get('key_insight','')[:120]}...")
                st.write(f"**Action Step:** {preview.get('action_step','')}")

            if st.button("✅ Apply to App & Save", use_container_width=True, type="primary"):
                st.session_state.content.update(st.session_state.import_preview)
                gh_ok, gh_msg = save_content(st.session_state.content)
                st.session_state.import_preview = None
                if gh_ok:
                    st.success("✅ Content applied & pushed to GitHub!")
                else:
                    st.warning(f"Applied locally, push failed: {gh_msg}")
                st.rerun()


# ── Satisfaction Survey (visible to all users) ────────────────────────────────
def section_survey():
    st.markdown("---")
    st.markdown("""
    <div class="gradient-header-green">
        <h2 style="margin-bottom:0.25rem;">📋 Share Your Feedback</h2>
        <p style="opacity:0.9; margin:0;">Help us improve this study experience for your group</p>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.get("survey_submitted"):
        st.markdown("""
        <div class="success-box" style="text-align:center; margin-top:1rem;">
            <h3 style="color:#065F46; margin-bottom:0.5rem;">🙏 Thank you for your feedback!</h3>
            <p style="color:#252628;">Your response has been recorded. God bless you this week!</p>
        </div>
        """, unsafe_allow_html=True)
        return

    with st.form("survey_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Your Name", placeholder="Optional")
        with col2:
            group = st.text_input("Small Group / Campus", placeholder="Optional")

        rating = st.radio(
            "Overall Satisfaction ⭐",
            options=[1, 2, 3, 4, 5],
            format_func=lambda x: "⭐" * x,
            horizontal=True,
            index=4
        )
        resonated = st.text_area(
            "What resonated with you most from today's study?",
            height=100,
            placeholder="Share what stood out to you..."
        )
        suggestions = st.text_area(
            "Any suggestions or feedback for us?",
            height=80,
            placeholder="We'd love to hear how we can improve!"
        )

        submitted = st.form_submit_button("Submit Feedback 💬", use_container_width=True)

    if submitted:
        with st.spinner("Saving your response..."):
            ok, msg = submit_survey({
                "name": name,
                "group": group,
                "rating": rating,
                "resonated": resonated,
                "suggestions": suggestions,
            })
        if ok:
            st.session_state.survey_submitted = True
            st.rerun()
        else:
            st.error(f"Could not save your response: {msg}")


# Section 0: Complete Reading Material (Now LAST page - Summary)
def section_0_reading():
    content = st.session_state.content
    
    st.markdown(f"""
    <div class="gradient-header">
        <h1>📖 Complete Study Summary</h1>
        <p style="font-size: 1.2rem; margin-top: 0.5rem; opacity: 0.9;">{content.get('study_topic', '')}</p>
        <p style="font-size: 0.9rem; margin-top: 0.25rem; opacity: 0.75;">A complete reference guide for this week's study</p>
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
    
    # Section 1 - with granular toggles
    if content.get("enable_section1", True):
        st.markdown(f'<div class="section-1"><h2 style="color: #6F6354; margin-bottom: 1rem;">Section 1: {content.get("section1_title", "")}</h2>', unsafe_allow_html=True)
        
        # Content paragraph
        if content.get("section1_show_content", True):
            st.markdown(f'<p style="color: #252628; line-height: 1.6; margin-bottom: 1rem;">{content.get("section1_content", "")}</p>', unsafe_allow_html=True)
        
        # Discussion question
        if content.get("section1_show_question", True):
            st.markdown(f"""
            <div class="discussion-box">
                <p style="color: #6F6354; font-weight: 600; margin-bottom: 0.5rem;">Discussion Question:</p>
                <p style="color: #252628; font-style: italic;">{content.get("section1_question", "")}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Key truth
        if content.get("section1_show_key_truth", True):
            st.markdown(f"""
            <div class="proof-box">
                <p style="color: #6F6354; font-size: 0.9rem; font-weight: 600; margin-bottom: 0.5rem;">KEY TRUTH:</p>
                <p style="color: #252628; font-style: italic;">{content.get("section1_key_truth", "")}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Section 2 - with granular toggles
    if content.get("enable_section2", True):
        st.markdown(f'<div class="section-2"><h2 style="color: #6F6354; margin-bottom: 1rem;">Section 2: {content.get("section2_title", "")}</h2>', unsafe_allow_html=True)
        
        if content.get("section2_show_content", True):
            st.markdown(f'<p style="color: #252628; line-height: 1.6; margin-bottom: 1rem;">{content.get("section2_content", "")}</p>', unsafe_allow_html=True)
        
        if content.get("section2_show_question", True):
            st.markdown(f"""
            <div class="discussion-box">
                <p style="color: #6F6354; font-weight: 600; margin-bottom: 0.5rem;">Discussion Question:</p>
                <p style="color: #252628; font-style: italic;">{content.get("section2_question", "")}</p>
            </div>
            """, unsafe_allow_html=True)
        
        if content.get("section2_show_key_truth", True):
            st.markdown(f"""
            <div class="proof-box">
                <p style="color: #6F6354; font-size: 0.9rem; font-weight: 600; margin-bottom: 0.5rem;">KEY TRUTH:</p>
                <p style="color: #252628; font-style: italic;">{content.get("section2_key_truth", "")}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Section 3 - with granular toggles
    if content.get("enable_section3", True):
        st.markdown(f'<div class="section-3"><h2 style="color: #6F6354; margin-bottom: 1rem;">Section 3: {content.get("section3_title", "")}</h2>', unsafe_allow_html=True)
        
        if content.get("section3_show_content", True):
            st.markdown(f'<p style="color: #252628; line-height: 1.6; margin-bottom: 1rem;">{content.get("section3_content", "")}</p>', unsafe_allow_html=True)
        
        if content.get("section3_show_question", True):
            st.markdown(f"""
            <div class="discussion-box">
                <p style="color: #6F6354; font-weight: 600; margin-bottom: 0.5rem;">Discussion Question:</p>
                <p style="color: #252628; font-style: italic;">{content.get("section3_question", "")}</p>
            </div>
            """, unsafe_allow_html=True)
        
        if content.get("section3_show_key_truth", True):
            st.markdown(f"""
            <div class="proof-box">
                <p style="color: #6F6354; font-size: 0.9rem; font-weight: 600; margin-bottom: 0.5rem;">KEY TRUTH:</p>
                <p style="color: #252628; font-style: italic;">{content.get("section3_key_truth", "")}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
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
    
    # Thank you message at the end
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="success-box" style="text-align: center;">
        <h3 style="color: #065F46; margin-bottom: 1rem;">✨ Thank you for completing this study! ✨</h3>
        <p style="color: #252628; line-height: 1.6;">
            May God bless you as you apply these truths in your life this week.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Satisfaction survey
    section_survey()


# Section 1: Welcome/Intro (First Page)
def section_1_intro():
    content = st.session_state.content
    
    # Add title and context first
    st.markdown(f"""
    <div class="gradient-header">
        <h1>{content.get('main_title', '')}</h1>
        <p style="font-size: 1.2rem; margin-top: 0.5rem; opacity: 0.9;">{content.get('study_topic', '')}</p>
        <p style="font-size: 0.9rem; margin-top: 0.25rem; opacity: 0.75;">{content.get('context', '')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="gradient-header-blue">
        <h2 style="font-size: 2rem; margin-bottom: 0.5rem;">Welcome to Your Interactive Journey</h2>
        <p style="font-size: 1.1rem; opacity: 0.9;">Let's explore together</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Add ice breaker
    st.markdown(f"""
    <div class="ice-breaker-box">
        <h3 style="color: #6F6354; margin-bottom: 1rem;">Ice Breaker: {content.get('icebreaker_title', '')}</h3>
        <p style="color: #252628; line-height: 1.6;">
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
    
    # Content
    if content.get("section1_show_content", True):
        st.markdown(f"""
        <div class="blue-box">
            <h3 style="color: #1E40AF; font-size: 1.5rem; margin-bottom: 1rem;">Section 1: {content.get('section1_title', '')}</h3>
            <p style="color: #252628; line-height: 1.6;">
                {content.get('section1_content', '')}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Interactive selector
    if content.get("section1_show_interactive", True):
        st.markdown(f"""
        <div class="yellow-box">
            <h4 style="color: #92400E; font-size: 1.2rem; margin-bottom: 1rem;">{content.get('section1_interactive_question', 'When have you felt distant from God?')}</h4>
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
    
    # Discussion question
    if content.get("section1_show_question", True):
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
    
    # Key truth
    if content.get("section1_show_key_truth", True):
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
    
    # Content
    if content.get("section2_show_content", True):
        st.markdown(f"""
        <div class="orange-box">
            <h3 style="color: #9A3412; font-size: 1.5rem; margin-bottom: 1rem;">Section 2: {content.get('section2_title', '')}</h3>
            <p style="color: #252628; line-height: 1.6;">
                {content.get('section2_content', '')}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Interactive selector
    if content.get("section2_show_interactive", True):
        st.markdown(f"""
        <div class="green-box">
            <h4 style="color: #065F46; font-size: 1.2rem; margin-bottom: 1rem;">{content.get('section2_interactive_question', 'How can we create a "safe space"?')}</h4>
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
    
    # Discussion question
    if content.get("section2_show_question", True):
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
    
    # Key truth
    if content.get("section2_show_key_truth", True):
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
    
    # Content
    if content.get("section3_show_content", True):
        st.markdown(f"""
        <div class="green-box">
            <h3 style="color: #065F46; font-size: 1.5rem; margin-bottom: 1rem;">Section 3: {content.get('section3_title', '')}</h3>
            <p style="color: #252628; line-height: 1.6;">
                {content.get('section3_content', '')}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Interactive input
    if content.get("section3_show_interactive", True):
        st.markdown(f"""
        <div class="yellow-box">
            <h4 style="color: #92400E; font-size: 1.2rem; margin-bottom: 1rem;">{content.get('section3_interactive_question', 'Who needs mercy in your circle?')}</h4>
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
    
    # Discussion question
    if content.get("section3_show_question", True):
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
    
    # Key truth
    if content.get("section3_show_key_truth", True):
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

    # ── Save My Answers (user login required) ─────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    if st.session_state.get("user_logged_in"):
        if st.session_state.action_commitment:
            if st.button("💾 Save My Answers", use_container_width=True, type="primary", key="_usr_history_save_answers"):
                save_current_answers(st.session_state.current_username)
                st.success(
                    f"✅ Answers saved for **{st.session_state.current_username}**! "
                    "Click **My Past Answers** at the top to review them."
                )
        else:
            st.info("✏️ Write your commitment above to unlock **Save My Answers**.")
    else:
        st.markdown("""
        <div style="background-color:#F5EFE0;border:1px dashed #C9A962;
                    padding:1rem;border-radius:0.5rem;text-align:center;margin-top:0.5rem;">
            <p style="color:#6F6354;margin:0;">💡 <strong>Sign in</strong> at the top of the page
            to save your answers and review them later!</p>
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
    # ── User login / past-answers routing ────────────────────────────────────
    if st.session_state.get("show_past_answers") and st.session_state.get("user_logged_in"):
        show_past_answers()
        return

    if st.session_state.get("show_user_login") and not st.session_state.get("user_logged_in"):
        show_user_login()
        return

    # ── User strip (signed-in) or guest banner ────────────────────────────────
    if st.session_state.get("user_logged_in"):
        uname = st.session_state.current_username
        col_u1, col_u2, col_u3 = st.columns([4, 2, 1])
        with col_u1:
            st.markdown(
                f"<p style='color:#6F6354;font-weight:600;margin:0;padding-top:0.4rem;'>"
                f"👤 Signed in as <strong>{uname}</strong></p>",
                unsafe_allow_html=True
            )
        with col_u2:
            if st.button("📚 My Past Answers", key="_usr_history_view_past", use_container_width=True):
                st.session_state.show_past_answers = True
                st.rerun()
        with col_u3:
            if st.button("Sign Out", key="_usr_history_signout", use_container_width=True):
                st.session_state.user_logged_in = False
                st.session_state.current_username = ''
                st.rerun()
        st.markdown("<hr style='margin:0.4rem 0;border-color:#D0CFC9;'>", unsafe_allow_html=True)
    else:
        col_b1, col_b2 = st.columns([5, 1])
        with col_b1:
            st.markdown(
                "<p style='color:#8A877E;font-size:0.9rem;margin:0;padding-top:0.4rem;'>"
                "💡 Sign in to save your answers and view your study history</p>",
                unsafe_allow_html=True
            )
        with col_b2:
            if st.button("Sign In", key="_usr_history_signin_banner", use_container_width=True):
                st.session_state.show_user_login = True
                st.rerun()
        st.markdown("<hr style='margin:0.4rem 0;border-color:#D0CFC9;'>", unsafe_allow_html=True)

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
    
    # Main content - Restructured order
    sections = [
        {"id": "intro", "title": "Welcome", "func": section_1_intro},
        {"id": "change", "title": "Section 1", "func": section_2_change_of_heart},
        {"id": "responsibility", "title": "Section 2", "func": section_3_shared_responsibility},
        {"id": "mission", "title": "Section 3", "func": section_4_mission_of_mercy},
        {"id": "action", "title": "Your Action Step", "func": section_5_action_step},
        {"id": "reading", "title": "Complete Summary", "func": section_0_reading}
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
