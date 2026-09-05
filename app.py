import os
import io
import streamlit as st
import assemblyai as aai
from deep_translator import GoogleTranslator
from streamlit_mic_recorder import mic_recorder

# Configure Page Layout
st.set_page_config(
    page_title="Two-Way Tourist Translator", 
    page_icon="💬", 
    layout="centered"
)

st.title("💬 Two-Way Tourist Translator")
st.caption("Translate local speech to English, then voice your response back.")

# API Key Handling for AssemblyAI
aai_key = os.environ.get("ASSEMBLYAI_API_KEY") or st.sidebar.text_input("AssemblyAI Key", type="password")

if not aai_key:
    st.warning("Please enter your AssemblyAI API key in the sidebar or set the ASSEMBLYAI_API_KEY environment variable.")
    st.stop()

# Set AssemblyAI API Key
aai.settings.api_key = aai_key

# Target Language Selection
target_language = st.sidebar.selectbox(
    "Target Language", 
    ["Japanese", "Spanish", "French", "German", "Chinese", "Italian"]
)

# Language Code Mapping for Translator
LANG_CODES = {
    "Japanese": "ja",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Chinese": "zh-CN",
    "Italian": "it",
    "English": "en"
}

def translate_text(text: str, target_lang: str) -> str:
    """Translates text using the 100% free GoogleTranslator engine."""
    code = LANG_CODES.get(target_lang, "en")
    return GoogleTranslator(source='auto', target=code).translate(text)

# Navigation Tabs
tab1, tab2 = st.tabs(["👂 Listen to Local", "🗣️ Respond to Local"])

# TAB 1: LISTEN TO LOCAL SPEAKER
with tab1:
    st.write(f"### Record Local Speaker ({target_language})")
    audio_local = mic_recorder(
        start_prompt="Record Local",
        stop_prompt="Stop & Translate",
        key="record_local"
    )

    if audio_local:
        with st.spinner("Transcribing with AssemblyAI..."):
            transcriber = aai.Transcriber()
            audio_bytes = io.BytesIO(audio_local['bytes'])
            transcript = transcriber.transcribe(audio_bytes)
            
        if transcript.status == aai.TranscriptStatus.error:
            st.error(f"Transcription Error: {transcript.error}")
        elif transcript.text:
            translation = translate_text(transcript.text, "English")
            
            st.info(f"**What they said ({target_language}):** {transcript.text}")
            st.success(f"**English Translation:** {translation}")
        else:
            st.warning("No speech detected. Please try recording again.")

# TAB 2: RESPOND TO LOCAL SPEAKER
with tab2:
    st.write("### Record Your Response (English)")
    audio_tourist = mic_recorder(
        start_prompt="Record English",
        stop_prompt="Stop & Translate",
        key="record_tourist"
    )

    if audio_tourist:
        with st.spinner("Translating for Local..."):
            transcriber = aai.Transcriber()
            audio_bytes = io.BytesIO(audio_tourist['bytes'])
            transcript = transcriber.transcribe(audio_bytes)
            
        if transcript.status == aai.TranscriptStatus.error:
            st.error(f"Transcription Error: {transcript.error}")
        elif transcript.text:
            foreign_translation = translate_text(transcript.text, target_language)
            
            st.info(f"**You said (English):** {transcript.text}")
            
            # High-visibility visual card to show locals
            st.markdown(f"""
                <div style="background-color: #1E293B; padding: 24px; border-radius: 12px; border: 2px solid #3B82F6; text-align: center; margin-top: 15px;">
                    <h4 style="color: #94A3B8; margin: 0; font-size: 14px; text-transform: uppercase; letter-spacing: 1px;">Show this screen to local:</h4>
                    <h1 style="color: #FFFFFF; margin-top: 12px; font-size: 28px; line-height: 1.3;">{foreign_translation}</h1>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("No speech detected. Please try recording again.")

# 2. Setup & API Keys (Using Streamlit Secrets)
aai.settings.api_key = st.secrets.get("ASSEMBLYAI_API_KEY", "YOUR_LOCAL_FALLBACK_KEY")
aai.settings.http_timeout = 60.0  # Prevents 500/timeout errors

# 3. Helper Functions
def translate_text(text, target_lang):
    try:
        return GoogleTranslator(source='auto', target=target_lang).translate(text)
    except Exception as e:
        return f"Translation error: {str(e)}"



# Tabs, audio recorders, and AssemblyAI call logic go here...
