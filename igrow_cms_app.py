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


# ── Gemini-powered document import ──────────────────────────────────────────────
def fetch_gdoc_text(gdoc_url: str):
    """Export a public Google Doc as plain text. Returns (text, error)."""
    import re
    match = re.search(r'/d/([a-zA-Z0-9_-]+)', gdoc_url)
    if not match:
        return None, "Could not find a document ID in that URL."
    doc_id = match.group(1)
    export_url = f"https://docs.google.com/document/d/{doc_id}/export?format=txt"
    try:
        r = requests.get(export_url, timeout=15)
        if r.status_code == 200:
            return r.text, None
        return None, f"Google returned status {r.status_code}. Make sure the doc is set to 'Anyone with link can view'."
    except Exception as e:
        return None, str(e)


def parse_document_text(raw: str) -> dict:
    """
    Parse a plain-text I-Grow Bible study guide into CMS content fields.

    Supports two Google Docs template formats:

    NEW FORMAT (structured with ## / ### headings):
      ## TOPIC
      Topic Name
      (subtitle in parentheses)
      ## ICEBREAKER
      **"Icebreaker Title"** (duration)
      ...instructions...
      ## BIG IDEA
      ...
      ## PASSAGE & KEY TEXT
      Reference (e.g. Malachi 4:1-3 (ESV))
      "Full passage text..."
      **Key Verse:**
      "Verse text here."
      (Reference, ESV)
      ## THE LESSON
      ### SECTION 1: PERSONAL APPLICATION
      **How This Truth Shapes My Life**
      ...teaching paragraphs...
      **Proof Text:**
      "..." (Reference)
      **DISCUSSION QUESTIONS — Section 1**
      * Open-ended question...
      * Follow-up...
      ### SECTION 2: ...
      ### SECTION 3: ...
      ## KEY INSIGHT
      ...
      ## ACTION STEP
      **This Week: "..."**
      1. Step one
      2. Step two
      ...

    OLD FORMAT (legacy fallback):
      Title / Icebreaker / Big Idea / Passage & Key Text /
      Short heading lines + body / Key Insight / Action Step
    """
    import re

    # ── Normalise ────────────────────────────────────────────────────────────
    lines = [l.rstrip() for l in raw.replace('\r\n', '\n').split('\n')]
    lines = [l for l in lines if not re.match(r'^[_\-=\*]{3,}$', l.strip())]
    text  = '\n'.join(lines)

    def clean(s):
        """Strip markdown bold/italic markers and extra whitespace."""
        s = re.sub(r'\*{1,2}([^*]+)\*{1,2}', r'\1', s)
        return s.strip()

    def between(label_re, stop_re, src=text):
        """Return text between two regex anchors (non-greedy)."""
        m = re.search(label_re + r'\s*\n?(.+?)(?=' + stop_re + r'|\Z)',
                      src, re.S | re.I)
        return m.group(1).strip() if m else ''

    # ════════════════════════════════════════════════════════════════════════
    # Detect format: new format uses ## section markers
    # ════════════════════════════════════════════════════════════════════════
    is_new_format = bool(re.search(r'^##\s+(TOPIC|ICEBREAKER|THE LESSON)', text,
                                   re.MULTILINE | re.IGNORECASE))

    if is_new_format:
        # ── Split into top-level ## sections ────────────────────────────────
        section_map = {}
        current_key = '__preamble__'
        current_buf = []
        for line in lines:
            h2 = re.match(r'^##\s+(.+)', line)
            if h2:
                section_map[current_key] = '\n'.join(current_buf).strip()
                current_key = h2.group(1).strip().upper()
                current_buf = []
            else:
                current_buf.append(line)
        section_map[current_key] = '\n'.join(current_buf).strip()

        def sec(name):
            """Get a top-level section by approximate name."""
            for k, v in section_map.items():
                if name.upper() in k:
                    return v
            return ''

        # ── TOPIC ────────────────────────────────────────────────────────────
        topic_block = sec('TOPIC')
        topic_lines = [l.strip() for l in topic_block.split('\n') if l.strip()]
        # First non-empty line = topic name; subtitle in parentheses on next line
        study_topic = topic_lines[0] if topic_lines else ''
        # Append parenthetical subtitle if present
        if len(topic_lines) > 1 and topic_lines[1].startswith('('):
            study_topic += '\n' + topic_lines[1]

        # ── ICEBREAKER ───────────────────────────────────────────────────────
        ice_block = sec('ICEBREAKER')
        # Title: extract from **"..."** or first quoted text
        ice_title_m = re.search(
            r'\*{1,2}["\u201c](.+?)["\u201d].*?\*{0,2}', ice_block)
        if not ice_title_m:
            ice_title_m = re.search(r'["\u201c](.+?)["\u201d]', ice_block)
        icebreaker_title = ice_title_m.group(1).strip() if ice_title_m else study_topic
        icebreaker_text  = ice_block  # keep full block for display

        # ── BIG IDEA ─────────────────────────────────────────────────────────
        big_idea = sec('BIG IDEA')

        # ── PASSAGE & KEY TEXT ───────────────────────────────────────────────
        passage_block = sec('PASSAGE')
        p_lines = [l.strip() for l in passage_block.split('\n') if l.strip()]
        passage_name = p_lines[0] if p_lines else ''

        # Key Verse label → grab the next quoted block
        kv_m = re.search(
            r'Key Verse[:\s]*\n*["\u201c](.+?)["\u201d]',
            passage_block, re.S | re.I)
        if not kv_m:
            # Fallback: first quoted block in passage section
            kv_m = re.search(r'["\u201c](.+?)["\u201d]', passage_block, re.S)
        key_verse = kv_m.group(1).strip() if kv_m else ''

        # Reference: parenthesised text after the key verse block
        ref_m = re.search(
            r'Key Verse[:\s]*\n*["\u201c].+?["\u201d]\s*\n?\(([^)]+)\)',
            passage_block, re.S | re.I)
        if not ref_m:
            # Fallback: last (Reference ESV) style in passage block
            ref_m = re.search(r'\(([^)]*\bESV\b[^)]*)\)', passage_block, re.I)
        if not ref_m:
            # Old-style dash reference
            ref_m = re.search(
                r'["\u201d]\s*[\u2013\u2014\-]+\s*(.+?)(?:\n|$)', passage_block)
        verse_reference = ref_m.group(1).strip() if ref_m else ''

        # ── THE LESSON → split into ### SECTION blocks ───────────────────────
        lesson_block = sec('THE LESSON')
        sub_sections = re.split(r'###\s+SECTION\s+\d+[:\s]', lesson_block,
                                flags=re.I)
        # sub_sections[0] is text before any SECTION header (ignore)
        lesson_parts = sub_sections[1:4]  # up to 3 sections

        s_titles   = ['', '', '']
        s_subtitles= ['', '', '']
        s_contents = ['', '', '']
        s_questions= ['', '', '']
        s_truths   = ['', '', '']

        for i, part in enumerate(lesson_parts[:3]):
            part_lines = part.split('\n')

            # First non-empty line after the ### header = section label
            # (e.g. "PERSONAL APPLICATION")
            label_line = ''
            for pl in part_lines:
                if pl.strip():
                    label_line = pl.strip()
                    break
            s_titles[i] = label_line

            # Subtitle: **How This Truth Shapes...**
            subtitle_m = re.search(
                r'\*{1,2}How This Truth[^*\n]+\*{0,2}', part, re.I)
            if not subtitle_m:
                # Any **bold** line that isn't a known label
                subtitle_m = re.search(
                    r'^\*{1,2}(?!Proof|DISCUSSION|Key Verse)(.+?)\*{0,2}$',
                    part, re.MULTILINE | re.I)
            s_subtitles[i] = clean(subtitle_m.group(0)) if subtitle_m else ''

            # Proof Text → key_truth
            proof_m = re.search(
                r'Proof Text[:\s]*\n*["\u201c](.+?)["\u201d]',
                part, re.S | re.I)
            s_truths[i] = proof_m.group(1).strip() if proof_m else ''

            # Discussion Questions block (bullet lines under DISCUSSION QUESTIONS)
            dq_m = re.search(
                r'DISCUSSION QUESTIONS[^\n]*\n(.+)',
                part, re.S | re.I)
            if dq_m:
                dq_raw = dq_m.group(1)
                # Grab bullet lines (* text or - text)
                bullets = re.findall(
                    r'^[\*\-•]\s*\*{0,2}(.+?)\*{0,2}$',
                    dq_raw, re.MULTILINE)
                s_questions[i] = ' '.join(b.strip() for b in bullets)

            # Content: teaching paragraphs — exclude sections after Proof Text
            # and the DISCUSSION block
            content_end = re.search(
                r'\*{0,2}Proof Text[:\s]', part, re.I)
            content_part = part[:content_end.start()] if content_end else part

            # Remove the section label line, subtitle, and any remaining **bold**
            # labels; keep normal paragraph text
            content_lines = []
            for cl in content_part.split('\n'):
                cs = cl.strip()
                if not cs:
                    continue
                if cs.upper() == label_line.upper():
                    continue
                if re.match(r'^\*{1,2}[A-Z].*\*{0,2}$', cs):
                    # Looks like a bold label line — skip
                    continue
                content_lines.append(cs)
            s_contents[i] = '\n'.join(content_lines)

        # ── KEY INSIGHT ──────────────────────────────────────────────────────
        key_insight = sec('KEY INSIGHT')

        # ── ACTION STEP ─────────────────────────────────────────────────────
        action_raw = sec('ACTION STEP')
        # Remove the bold title line at the top (e.g. **This Week: "..."**)
        action_lines = [l for l in action_raw.split('\n')
                        if not re.match(r'^\*{1,2}This Week', l.strip(), re.I)]
        action_step = '\n'.join(action_lines).strip()

    else:
        # ════════════════════════════════════════════════════════════════════
        # LEGACY / OLD FORMAT fallback
        # ════════════════════════════════════════════════════════════════════
        non_empty = [l for l in lines if l.strip()]
        study_topic = non_empty[0].strip() if non_empty else ''
        icebreaker_title = study_topic
        icebreaker_text  = between(r'Icebreaker\b', r'Big Idea\b')
        big_idea         = between(r'Big Idea\b', r'Passage\b')

        passage_block = between(r'Passage\s*(?:&|and)?\s*Key Text\b',
                                r'\n[A-Z][^\n]{3,40}\n')
        passage_lines = passage_block.split('\n')
        passage_name  = passage_lines[0].strip() if passage_lines else ''
        verse_m       = re.search(r'["\u201c](.+?)["\u201d]', text)
        key_verse     = verse_m.group(1).strip() if verse_m else ''
        ref_m         = re.search(
            r'["\u201d]\s*[\u2013\u2014\-]+\s*(.+?)(?:\n|$)', text)
        verse_reference = ref_m.group(1).strip() if ref_m else ''

        ki_split    = re.split(r'\bKey Insight\b', text, maxsplit=1, flags=re.I)
        body_text   = ki_split[0]
        ending_text = ki_split[1] if len(ki_split) > 1 else ''

        SKIP = re.compile(
            r'^(Icebreaker|Big Idea|Passage|Key|Action|Finding|\d)', re.I)
        section_blocks = []
        current_h, current_b = None, []
        for line in body_text.split('\n'):
            stripped = line.strip()
            if (stripped
                    and len(stripped) < 60
                    and re.match(r'[A-Z]', stripped)
                    and not stripped.endswith('?')
                    and not stripped.endswith('.')
                    and not SKIP.match(stripped)):
                if current_h is not None:
                    section_blocks.append(
                        (current_h, '\n'.join(current_b).strip()))
                current_h, current_b = stripped, []
            elif current_h:
                current_b.append(line)
        if current_h:
            section_blocks.append((current_h, '\n'.join(current_b).strip()))

        def split_section(block_text):
            q_lines = [l.strip() for l in block_text.split('\n')
                       if l.strip().endswith('?')]
            non_q   = [l for l in block_text.split('\n')
                       if l.strip() and not l.strip().endswith('?')]
            content  = '\n'.join(non_q).strip()
            question = ' '.join(q_lines)
            sentences = re.split(r'(?<=[.!])\s+', content)
            key_truth = sentences[-1].strip() if sentences else ''
            return content, question, key_truth

        s_titles   = ['', '', '']
        s_contents = ['', '', '']
        s_questions= ['', '', '']
        s_truths   = ['', '', '']
        for i, (h, b) in enumerate(section_blocks[:3]):
            s_titles[i] = h
            c, q, t     = split_section(b)
            s_contents[i]  = c
            s_questions[i] = q
            s_truths[i]    = t

        key_insight = between(r'', r'Action Step\b', src=ending_text)
        action_step = between(r'Action Step\b', r'\Z', src=ending_text)

    # ── Assemble & return ────────────────────────────────────────────────────
    return {
        "study_topic":       study_topic,
        "icebreaker_title":  icebreaker_title,
        "icebreaker_text":   icebreaker_text,
        "big_idea":          big_idea,
        "passage_name":      passage_name,
        "key_verse":         key_verse,
        "verse_reference":   verse_reference,
        "section1_title":    s_titles[0],
        "section1_content":  s_contents[0],
        "section1_question": s_questions[0],
        "section1_key_truth":s_truths[0],
        "section2_title":    s_titles[1],
        "section2_content":  s_contents[1],
        "section2_question": s_questions[1],
        "section2_key_truth":s_truths[1],
        "section3_title":    s_titles[2],
        "section3_content":  s_contents[2],
        "section3_question": s_questions[2],
        "section3_key_truth":s_truths[2],
        "key_insight":       key_insight,
        "action_step":       action_step,
    }


def import_with_gemini(raw_text: str):
    """
    Send raw study guide text to Gemini and ask it to return a JSON
    object mapping content to the CMS fields.
    Returns (parsed_dict, error_message).
    """
    try:
        import google.generativeai as genai
        api_key = st.secrets["gemini"]["api_key"]
    except (KeyError, AttributeError):
        return None, "Gemini API key not found. Add [gemini] api_key to Streamlit secrets."
    except ImportError:
        return None, "google-generativeai package not installed."

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.0-flash")

    prompt = f"""
You are a content assistant for a Bible study app. Read the following study guide text and extract its content into a JSON object with EXACTLY these keys:

  study_topic, icebreaker_title, icebreaker_text, big_idea,
  passage_name, key_verse, verse_reference,
  section1_title, section1_content, section1_question, section1_key_truth,
  section2_title, section2_content, section2_question, section2_key_truth,
  section3_title, section3_content, section3_question, section3_key_truth,
  key_insight, action_step

The document may use one of two formats:

NEW FORMAT (## headings):
  ## TOPIC → study_topic (first line = topic name, 2nd line in parentheses = subtitle; include both)
  ## ICEBREAKER → icebreaker_title (quoted title inside **"..."**), icebreaker_text (full block)
  ## BIG IDEA → big_idea
  ## PASSAGE & KEY TEXT → passage_name (first line/reference), key_verse (text after **Key Verse:** label, no quotes), verse_reference (parenthesised reference like "Malachi 4:2, ESV")
  ## THE LESSON → contains ### SECTION 1 / 2 / 3 blocks:
    - section_title = the label after "SECTION N:" (e.g. "PERSONAL APPLICATION")
    - section_content = teaching paragraphs only (stop before **Proof Text:**)
    - section_key_truth = the verse quoted under **Proof Text:** (text only, no reference)
    - section_question = the bullet-point questions under **DISCUSSION QUESTIONS — Section N**
  ## KEY INSIGHT → key_insight
  ## ACTION STEP → action_step (exclude the bold **This Week: "..."** title line)

OLD FORMAT (plain headings):
  - Title line → study_topic, icebreaker_title
  - Icebreaker / Big Idea / Passage & Key Text headings
  - Short capitalized lines = section titles; body text follows
  - Key Insight / Action Step headings

Rules:
- section_content = teaching body paragraphs ONLY (no discussion questions, no proof texts)
- section_question = all discussion/follow-up questions for that section (joined as one string)
- section_key_truth = proof text verse OR last key sentence of the section
- key_verse = verse text only, NO reference citation
- verse_reference = e.g. "Malachi 4:2, ESV"
- Return ONLY valid JSON, no markdown fences, no extra text.

Study guide text:
"""
    prompt += raw_text[:8000]  # stay within token limits

    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        # Strip markdown code fences if Gemini wraps the JSON
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        parsed = json.loads(text)
        return parsed, None
    except json.JSONDecodeError as e:
        return None, f"Gemini returned invalid JSON: {e}"
    except Exception as e:
        return None, f"Gemini API error: {e}"


# ── Survey helpers (JSON-based) ───────────────────────────────────────────────────
# ── Survey helpers (Excel-based) ──────────────────────────────────────────────────
SURVEY_FILE    = "igrow_survey_responses.xlsx"
QUESTIONS_FILE = "igrow_survey_questions.json"

FIXED_COLUMNS = ["Timestamp", "Study Topic", "Name", "Group/Campus"]


def load_survey_questions():
    """Load question definitions from local JSON file."""
    q_path = Path(QUESTIONS_FILE)
    if q_path.exists():
        with open(q_path, 'r', encoding='utf-8') as f:
            return json.load(f).get("questions", [])
    return []


def fetch_survey_excel():
    """Download existing survey Excel from GitHub. Returns (DataFrame, sha, error)."""
    try:
        gh = st.secrets["github"]
        token  = gh["token"]
        repo   = gh["repo"]
        branch = gh.get("branch", "main")
    except (KeyError, AttributeError):
        return None, None, "GitHub secrets not configured"

    url = f"https://api.github.com/repos/{repo}/contents/{SURVEY_FILE}"
    headers = {"Authorization": f"token {token}",
               "Accept": "application/vnd.github+json"}
    resp = requests.get(url, headers=headers, params={"ref": branch})

    if resp.status_code == 404:
        # File doesn't exist yet — first submission
        return None, None, None
    if resp.status_code != 200:
        return None, None, f"GitHub GET failed ({resp.status_code})"

    data = resp.json()
    # GitHub embeds newlines every 60 chars — strip before decoding
    raw_b64 = data["content"].replace("\n", "").replace(" ", "")
    try:
        file_bytes = base64.b64decode(raw_b64)
        df = pd.read_excel(io.BytesIO(file_bytes), engine="openpyxl")
        return df, data["sha"], None
    except Exception as e:
        return None, data.get("sha"), f"Could not read Excel: {e}"


def submit_survey(responses: dict):
    """Append a survey response and push updated Excel to GitHub."""
    questions   = load_survey_questions()
    q_col_names = [q["label"] for q in questions]
    all_columns = ["Timestamp", "Study Topic"] + q_col_names

    df, sha, read_err = fetch_survey_excel()

    if read_err and "Could not read" in read_err:
        # Existing file unreadable — start fresh but warn
        df = pd.DataFrame(columns=all_columns)
    elif df is None:
        df = pd.DataFrame(columns=all_columns)

    # Ensure any new question columns exist
    for col in all_columns:
        if col not in df.columns:
            df[col] = ""

    new_row = {
        "Timestamp":   datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Study Topic": st.session_state.content.get("study_topic", ""),
    }
    for q in questions:
        new_row[q["label"]] = responses.get(q["id"], "")

    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    buffer = io.BytesIO()
    df.to_excel(buffer, index=False, engine="openpyxl")
    buffer.seek(0)
    encoded = base64.b64encode(buffer.read()).decode("utf-8")

    try:
        gh = st.secrets["github"]
        token  = gh["token"]
        repo   = gh["repo"]
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
    if resp.status_code in (200, 201):
        row_count = len(df)
        return True, f"Submitted! ({row_count} total responses in file)"
    return False, f"Push failed ({resp.status_code}): {resp.text[:300]}"



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

if 'pending_import' not in st.session_state:
    st.session_state.pending_import = None

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

        # ── Apply pending import BEFORE any widget is rendered ──────────────
        if st.session_state.pending_import:
            pending = st.session_state.pending_import
            for k, v in pending.items():
                # Update content dict
                st.session_state.content[k] = v
                # Safe to set widget state here — no widgets rendered yet
                st.session_state[k] = v
            gh_ok, gh_msg = save_content(st.session_state.content)
            st.session_state.pending_import = None
            if gh_ok:
                st.success("✅ Import applied & pushed to GitHub!")
            else:
                st.warning(f"Import applied locally. Push failed: {gh_msg}")
        # ─────────────────────────────────────────────────────────

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

        # ── Document Import ──────────────────────────────────────────
        st.subheader("📥 Import New Study Content")
        st.caption("Paste a public Google Docs link to auto-fill all content fields.")

        gdoc_url = st.text_input(
            "Google Docs URL",
            key="gdoc_import_url",
            placeholder="https://docs.google.com/document/d/.../edit"
        )

        # ─ Primary: pattern matching (always available) ─
        col_parse, col_ai = st.columns(2)
        with col_parse:
            parse_clicked = st.button("🔍 Parse Document", use_container_width=True,
                                      key="parse_btn", type="primary")
        # ─ Secondary: Gemini (only if key is configured) ─
        gemini_available = False
        try:
            _ = st.secrets["gemini"]["api_key"]
            gemini_available = True
        except Exception:
            pass
        with col_ai:
            ai_clicked = st.button(
                "🧠 Use Gemini AI" if gemini_available else "🧠 Gemini (key not set)",
                use_container_width=True, key="gemini_btn",
                disabled=not gemini_available
            )

        if parse_clicked or ai_clicked:
            if not gdoc_url:
                st.warning("Please paste a Google Docs URL first.")
            else:
                label = "🧠 Gemini is reading..." if ai_clicked else "🔍 Parsing document..."
                with st.spinner(label):
                    raw, err = fetch_gdoc_text(gdoc_url)
                    if err:
                        st.error(err)
                    else:
                        if ai_clicked:
                            parsed, err2 = import_with_gemini(raw)
                        else:
                            parsed, err2 = parse_document_text(raw), None
                        if err2:
                            st.error(err2)
                        elif parsed:
                            st.session_state.import_preview = parsed
                            st.success(f"✅ Topic detected: **{parsed.get('study_topic', '?')}** — Review & Apply below.")

        if st.session_state.get("import_preview"):
            preview = st.session_state.import_preview
            with st.expander("📋 Preview parsed fields", expanded=True):
                for key, val in preview.items():
                    if val:
                        st.markdown(f"**{key}:** {str(val)[:200]}")

            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("✅ Apply & Save", use_container_width=True,
                             type="primary", key="apply_import_btn"):
                    # Store into pending — applied at top of editor on next rerun
                    # (before widgets render, so widget-state keys can be set safely)
                    st.session_state.pending_import = preview
                    st.session_state.import_preview = None
                    st.rerun()
            with col_b:
                if st.button("❌ Discard", use_container_width=True, key="discard_import_btn"):
                    st.session_state.import_preview = None
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

    questions = load_survey_questions()

    with st.form("survey_form", clear_on_submit=True):
        answers = {}
        i = 0
        while i < len(questions):
            q = questions[i]
            qid    = q.get("id", "")
            label  = q.get("label", qid)
            qtype  = q.get("type", "textarea")
            hint   = q.get("placeholder", "")
            height = q.get("height", 100)
            pair   = q.get("pair_with_next", False)

            # Render two questions side-by-side if pair_with_next is true
            if pair and i + 1 < len(questions):
                q2      = questions[i + 1]
                qid2    = q2.get("id", "")
                label2  = q2.get("label", qid2)
                qtype2  = q2.get("type", "textarea")
                hint2   = q2.get("placeholder", "")
                height2 = q2.get("height", 100)
                col_l, col_r = st.columns(2)
                with col_l:
                    if qtype == "rating":
                        answers[qid] = st.radio(f"{label} ⭐", options=[1,2,3,4,5],
                            format_func=lambda x: "⭐"*x, horizontal=True, index=4, key=f"survey_{qid}")
                    elif qtype == "text_input":
                        answers[qid] = st.text_input(label, placeholder=hint, key=f"survey_{qid}")
                    else:
                        answers[qid] = st.text_area(label, height=height, placeholder=hint, key=f"survey_{qid}")
                with col_r:
                    if qtype2 == "rating":
                        answers[qid2] = st.radio(f"{label2} ⭐", options=[1,2,3,4,5],
                            format_func=lambda x: "⭐"*x, horizontal=True, index=4, key=f"survey_{qid2}")
                    elif qtype2 == "text_input":
                        answers[qid2] = st.text_input(label2, placeholder=hint2, key=f"survey_{qid2}")
                    else:
                        answers[qid2] = st.text_area(label2, height=height2, placeholder=hint2, key=f"survey_{qid2}")
                i += 2
                continue

            # Single full-width question
            if qtype == "rating":
                answers[qid] = st.radio(
                    f"{label} ⭐",
                    options=[1, 2, 3, 4, 5],
                    format_func=lambda x: "⭐" * x,
                    horizontal=True,
                    index=4,
                    key=f"survey_{qid}"
                )
            elif qtype == "text_input":
                answers[qid] = st.text_input(label, placeholder=hint, key=f"survey_{qid}")
            else:
                answers[qid] = st.text_area(label, height=height, placeholder=hint, key=f"survey_{qid}")
            i += 1

        submitted = st.form_submit_button("Submit Feedback 💬", use_container_width=True)

    if submitted:
        with st.spinner("Saving your response..."):
            ok, msg = submit_survey(answers)
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
