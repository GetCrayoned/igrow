"""
I-Grow Discipleship Guide - Interactive Streamlit App
Justice and Mercy in the Conquest (The Book of Joshua)
Context: Campus and Workplace Small Groups (Philippines)
"""

import streamlit as st

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


# Section 0: Complete Reading Material
def section_0_reading():
    st.markdown("""
    <div class="gradient-header">
        <h1>I-Grow Discipleship Guide</h1>
        <p style="font-size: 1.2rem; margin-top: 0.5rem; opacity: 0.9;">Justice and Mercy in the Conquest (The Book of Joshua)</p>
        <p style="font-size: 0.9rem; margin-top: 0.25rem; opacity: 0.75;">Context: Campus and Workplace Small Groups (Philippines)</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="scrollable-content">', unsafe_allow_html=True)
    
    # Ice Breaker
    st.markdown("""
    <div class="ice-breaker-box">
        <h2 style="color: #6F6354; margin-bottom: 1rem;">Ice Breaker: The "Fairness" Debate</h2>
        <p style="color: #252628; line-height: 1.6;">
            Think of a time when you were playing a game or working on a group project and someone "cheated" 
            or didn't do their part but still got the same reward as you. How did that make you feel? 
            Share your story in one minute or less.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Big Idea
    st.markdown("""
    <div class="big-idea-box">
        <h2 style="color: #6F6354; margin-bottom: 1rem;">The Big Idea</h2>
        <p style="color: #252628; font-weight: 600; line-height: 1.6;">
            God's heart is always for restoration, and His judgments are not about anger, 
            but about protecting life and providing a way back for everyone.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Passage & Key Text
    st.markdown("""
    <div class="passage-box">
        <h2 style="color: #6F6354; margin-bottom: 1rem;">Passage & Key Text</h2>
        <p style="color: #252628; font-weight: 600; margin-bottom: 1rem;">Passage: Ezekiel 33</p>
        <p style="color: #252628; font-style: italic; line-height: 1.6;">
            "As I live, says the Lord God, I have no pleasure in the death of the wicked, 
            but that the wicked turn from his way and live" (Ezekiel 33:11, ESV).
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Section 1
    st.markdown("""
    <div class="section-1">
        <h2 style="color: #6F6354; margin-bottom: 1rem;">Section 1: A Change of Heart</h2>
        <p style="color: #252628; line-height: 1.6; margin-bottom: 1rem;">
            God is often misunderstood as a strict judge waiting for us to mess up. However, 
            Ezekiel 33:11 shows us a God who actually feels "agony" when people choose a path 
            that leads to destruction. He is like a parent watching a child make a dangerous mistake, 
            pleading for them to "turn back" before they get hurt. This means that my past mistakes 
            do not define my future if I am willing to change direction today. When we turn to Him, 
            His mercy overrides the consequences we originally deserved. This truth changes how I view 
            my own failures because I realize God is cheering for my recovery rather than waiting for 
            my punishment.
        </p>
        <div class="discussion-box">
            <p style="color: #6F6354; font-weight: 600; margin-bottom: 0.5rem;">Discussion Question:</p>
            <p style="color: #252628; font-style: italic;">
                Sa mga moments na feeling mo "fail" ka or lumayo ka kay Lord, how does knowing 
                He takes "no pleasure" in your struggle change your perspective? (Does this make 
                it easier for you to come back to Him?)
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Section 2
    st.markdown("""
    <div class="section-2">
        <h2 style="color: #6F6354; margin-bottom: 1rem;">Section 2: Our Shared Responsibility</h2>
        <p style="color: #252628; line-height: 1.6; margin-bottom: 1rem;">
            In our communities, we often find it easy to judge others while excusing ourselves. 
            Ezekiel reminds us that God is impartial, meaning He holds everyone to the same standard 
            of love and justice. As a group, we are called to be like "watchmen" who look out for 
            one another's spiritual well-being. This is not about being "judgy," but about caring 
            enough to speak up when we see a friend heading toward a "dead end." Our relationships 
            grow deeper when we create a space where it is safe to admit we are wrong and encourage 
            each other to stay on the right path. We represent God's fairness by being consistent 
            in how we treat people, regardless of their background or status.
        </p>
        <div class="discussion-box">
            <p style="color: #6F6354; font-weight: 600; margin-bottom: 0.5rem;">Discussion Question:</p>
            <p style="color: #252628; font-style: italic;">
                How can we make our group a "safe space" where it's okay to admit mistakes without 
                feeling judged by others? (Ano yung isang thing na pwede nating gawin para mas 
                maging supportive sa isa't isa?)
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Section 3
    st.markdown("""
    <div class="section-3">
        <h2 style="color: #6F6354; margin-bottom: 1rem;">Section 3: A Mission of Mercy</h2>
        <p style="color: #252628; line-height: 1.6; margin-bottom: 1rem;">
            The story of the conquest in Joshua and the warnings in Ezekiel show that God intervenes 
            only when evil begins to destroy everything good. Our mission today is to share the 
            "Good News" that there is always a way out of toxic cycles and harmful lifestyles. 
            Just as Rahab found safety in the middle of a city facing judgment, God is looking for 
            "outsiders" to bring into His family. We are sent to our campuses and offices not to 
            condemn people, but to offer them the same mercy we have received. When we live out 
            this mission, we show the world that God's ultimate goal is not to "win a war," but 
            to save as many people as possible.
        </p>
        <div class="discussion-box">
            <p style="color: #6F6354; font-weight: 600; margin-bottom: 0.5rem;">Discussion Question:</p>
            <p style="color: #252628; font-style: italic;">
                Sino yung "unlikely person" sa workplace or school mo na feeling mo kailangan ng 
                encouragement or mercy ngayon? (How can you show them God's kindness this week 
                without sounding like you are lecturing them?)
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Key Insight
    st.markdown("""
    <div class="gradient-insight">
        <h2 style="margin-bottom: 1rem;">Key Insight</h2>
        <p style="line-height: 1.6;">
            It is easy to look at the stories of judgment in the Bible and feel afraid or confused. 
            But when we look closer at Ezekiel 33, we see a God who is actually "longsuffering" 
            and incredibly patient. He waits until the very last second, hoping that just one more 
            person will turn around and live. He does not want anyone to perish, and that includes 
            you, your "difficult" boss, or your struggling classmate. This reveals that God is both 
            perfectly just and incredibly kind at the same time. You can trust Him with the things 
            you don't understand because His heart is always moved by love.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Action Step
    st.markdown("""
    <div class="ice-breaker-box">
        <h2 style="color: #6F6354; margin-bottom: 1rem;">Action Step</h2>
        <p style="color: #252628; line-height: 1.6;">
            Identify one person this week who seems to be "struggling with the consequences" of 
            a bad choice. Instead of joining in the gossip or judging them, offer them a genuine 
            word of encouragement or a small act of kindness to remind them that there is always 
            a path back to hope.
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
        <p style="font-size: 1.1rem; opacity: 0.9;">Let's explore God's heart for justice and mercy together</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="yellow-box">
        <h3 style="color: #92400E; margin-bottom: 1rem;">Quick Recap: The Fairness Debate</h3>
        <p style="color: #252628;">
            We all know the frustration of unfairness - when someone doesn't pull their weight 
            but gets the same reward. That feeling of injustice? It's actually a glimpse into 
            God's character. He cares deeply about fairness AND mercy.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="blue-box">
        <h3 style="color: #1E40AF; margin-bottom: 1rem;">The Big Idea</h3>
        <p style="color: #252628; font-size: 1.1rem; line-height: 1.6;">
            God's heart is always for <span style="background-color: #FEF3C7; color: #92400E; font-weight: 700; padding: 0.25rem 0.5rem; border-radius: 0.25rem;">restoration</span>, 
            and His judgments are not about anger, but about 
            <span style="background-color: #FEF3C7; color: #92400E; font-weight: 700; padding: 0.25rem 0.5rem; border-radius: 0.25rem;">protecting life</span> 
            and providing a 
            <span style="background-color: #FEF3C7; color: #92400E; font-weight: 700; padding: 0.25rem 0.5rem; border-radius: 0.25rem;">way back for everyone</span>.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="passage-box" style="border: 2px solid #6B7280;">
        <h3 style="color: #1F2937; margin-bottom: 1rem;">Key Text</h3>
        <p style="color: #252628; font-size: 1.1rem; font-style: italic; line-height: 1.6;">
            "As I live, says the Lord God, I have no pleasure in the death of the wicked, 
            but that the wicked turn from his way and live"
        </p>
        <p style="color: #6B7280; font-size: 0.9rem; font-weight: 600; margin-top: 0.5rem;">
            — Ezekiel 33:11, ESV
        </p>
    </div>
    """, unsafe_allow_html=True)


# Section 2: A Change of Heart
def section_2_change_of_heart():
    st.markdown("""
    <div class="blue-box">
        <h3 style="color: #1E40AF; font-size: 1.5rem; margin-bottom: 1rem;">Section 1: A Change of Heart</h3>
        <p style="color: #252628; line-height: 1.6;">
            God isn't a strict judge waiting for you to mess up. He feels <strong>agony</strong> 
            when you choose a destructive path - like a parent watching their child make a dangerous 
            mistake. Your past doesn't define your future if you're willing to turn around today.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="yellow-box">
        <h4 style="color: #92400E; font-size: 1.2rem; margin-bottom: 1rem;">When have you felt distant from God?</h4>
        <p style="color: #252628; margin-bottom: 1rem;">Select all that apply (or add your own):</p>
    </div>
    """, unsafe_allow_html=True)
    
    struggles = [
        'Felt like a failure',
        'Made a big mistake',
        'Drifted from prayer/Bible reading',
        'Hurt someone I care about',
        'Gave in to temptation',
        'Doubted God\'s goodness'
    ]
    
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
    
    st.markdown("""
    <div class="discussion-box" style="border-left: 4px solid #8B7B9E;">
        <h4 style="color: #6F6354; font-size: 1.1rem; margin-bottom: 1rem;">Reflect & Respond</h4>
        <p style="color: #252628; font-style: italic; margin-bottom: 1rem;">
            Sa mga moments na feeling mo "fail" ka or lumayo ka kay Lord, how does knowing 
            He takes "no pleasure" in your struggle change your perspective?
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    reflection = st.text_area(
        "Type your thoughts here... (Does this make it easier for you to come back to Him?)",
        value=st.session_state.reflections.get('section1', ''),
        key="reflection_section1",
        height=120
    )
    st.session_state.reflections['section1'] = reflection
    
    st.markdown("""
    <div class="proof-box">
        <p style="color: #6F6354; font-size: 0.9rem; font-weight: 600; margin-bottom: 0.5rem;">KEY TRUTH:</p>
        <p style="color: #252628; font-style: italic;">
            God is cheering for your recovery, not waiting for your punishment. Your past mistakes 
            don't define your future when you turn to Him.
        </p>
    </div>
    """, unsafe_allow_html=True)


# Section 3: Our Shared Responsibility
def section_3_shared_responsibility():
    st.markdown("""
    <div class="orange-box">
        <h3 style="color: #9A3412; font-size: 1.5rem; margin-bottom: 1rem;">Section 2: Our Shared Responsibility</h3>
        <p style="color: #252628; line-height: 1.6;">
            We're called to be "watchmen" for each other - not to judge, but to care enough to 
            speak up when a friend is heading toward a dead end. This creates deeper relationships 
            where it's safe to admit we're wrong.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="green-box">
        <h4 style="color: #065F46; font-size: 1.2rem; margin-bottom: 1rem;">How can we create a "safe space"?</h4>
        <p style="color: #252628; margin-bottom: 1rem;">Choose ideas that resonate with you:</p>
    </div>
    """, unsafe_allow_html=True)
    
    quick_ideas = [
        'Listen without interrupting',
        'No gossip rule',
        'Share our own struggles first',
        'Pray for each other regularly',
        'Check in during the week',
        'Celebrate small wins together'
    ]
    
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
    
    st.markdown("""
    <div class="discussion-box" style="border-left: 4px solid #8B7B9E;">
        <h4 style="color: #6F6354; font-size: 1.1rem; margin-bottom: 1rem;">Reflect & Respond</h4>
        <p style="color: #252628; font-style: italic; margin-bottom: 1rem;">
            Ano yung isang thing na pwede nating gawin para mas maging supportive sa isa't isa?
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
    
    st.markdown("""
    <div class="proof-box" style="border-left: 4px solid #8A877E;">
        <p style="color: #6F6354; font-size: 0.9rem; font-weight: 600; margin-bottom: 0.5rem;">KEY TRUTH:</p>
        <p style="color: #252628; font-style: italic;">
            True community happens when we're consistent in how we treat everyone, creating space 
            where it's safe to admit mistakes and grow together.
        </p>
    </div>
    """, unsafe_allow_html=True)


# Section 4: A Mission of Mercy
def section_4_mission_of_mercy():
    st.markdown("""
    <div class="green-box">
        <h3 style="color: #065F46; font-size: 1.5rem; margin-bottom: 1rem;">Section 3: A Mission of Mercy</h3>
        <p style="color: #252628; line-height: 1.6;">
            Just like Rahab found safety in the middle of judgment, God is looking for "outsiders" 
            to bring into His family. We're sent to our campuses and offices not to condemn, but 
            to offer the same mercy we've received.
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
    
    st.markdown("""
    <div class="discussion-box" style="border-left: 4px solid #8B7B9E;">
        <h4 style="color: #6F6354; font-size: 1.1rem; margin-bottom: 1rem;">Reflect & Respond</h4>
        <p style="color: #252628; font-style: italic; margin-bottom: 1rem;">
            How can you show them God's kindness this week without sounding like you are lecturing them?
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
    
    st.markdown("""
    <div class="proof-box" style="border-left: 4px solid #7A9B76;">
        <p style="color: #6F6354; font-size: 0.9rem; font-weight: 600; margin-bottom: 0.5rem;">KEY TRUTH:</p>
        <p style="color: #252628; font-style: italic;">
            God's ultimate goal isn't to "win a war" but to save as many people as possible. 
            When we show mercy, we reveal His true heart.
        </p>
    </div>
    """, unsafe_allow_html=True)


# Section 5: Action Step
def section_5_action_step():
    st.markdown("""
    <div class="gradient-header-green">
        <h3 style="font-size: 1.8rem; margin-bottom: 1rem;">Key Insight</h3>
        <p style="font-size: 1.1rem; line-height: 1.6;">
            God is "longsuffering" and incredibly patient. He waits until the very last second, 
            hoping just one more person will turn around and live. He doesn't want anyone to perish - 
            including you, your difficult boss, or your struggling classmate. You can trust Him 
            because His heart is always moved by love.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="yellow-box">
        <h4 style="color: #92400E; font-size: 1.5rem; margin-bottom: 1rem;">This Week's Challenge</h4>
        <p style="color: #252628; font-size: 1.1rem; line-height: 1.6; margin-bottom: 1rem;">
            Identify one person who seems to be "struggling with the consequences" of a bad choice. 
            Instead of joining the gossip or judging them, offer a genuine word of encouragement 
            or small act of kindness.
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
        {"id": "change", "title": "A Change of Heart", "func": section_2_change_of_heart},
        {"id": "responsibility", "title": "Our Shared Responsibility", "func": section_3_shared_responsibility},
        {"id": "mission", "title": "A Mission of Mercy", "func": section_4_mission_of_mercy},
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
