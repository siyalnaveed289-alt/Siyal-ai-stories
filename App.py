import streamlit as st
import asyncio
import edge_tts
import os

# Page Config
st.set_page_config(page_title="Ultimate Text-to-Speech", page_icon="🎙️", layout="wide")

st.title("🎙️ AI Text-to-Speech Generator")
st.write("Convert your text into high-quality realistic voice audio.")

# 100% Working & Verified Edge-TTS Voices
VOICE_MAPPING = {
    # --- Urdu & Hindi ---
    "Male 01 - Urdu Pakistan (Asad)": "ur-PK-AsadNeural",
    "Female 01 - Urdu Pakistan (Uzma)": "ur-PK-UzmaNeural",
    "Male 02 - Urdu India (Salman)": "ur-IN-SalmanNeural",
    "Female 02 - Urdu India (Gul)": "ur-IN-GulNeural",
    "Male 03 - Hindi India (Madhur)": "hi-IN-MadhurNeural",
    "Female 03 - Hindi India (Swara)": "hi-IN-SwaraNeural",

    # --- Arabic Voices (Best for Quranic Recitation) ---
    "Male 04 - Arabic Saudi Arabia (Hamed - Best for Quran)": "ar-SA-HamedNeural",
    "Female 04 - Arabic Saudi Arabia (Zariyah)": "ar-SA-ZariyahNeural",
    "Male 05 - Arabic UAE (Hamdan)": "ar-AE-HamdanNeural",
    "Female 05 - Arabic UAE (Fatima)": "ar-AE-FatimaNeural",
    "Male 06 - Arabic Egypt (Shakir)": "ar-EG-ShakirNeural",
    "Female 06 - Arabic Egypt (Salma)": "ar-EG-SalmaNeural",

    # --- English Accent Voices ---
    "Male 07 - English US (Guy - Natural)": "en-US-GuyNeural",
    "Female 07 - English US (Ava - Smooth)": "en-US-AvaNeural",
    "Male 08 - English US (Christopher - Deep)": "en-US-ChristopherNeural",
    "Female 08 - English US (Jenny - Friendly)": "en-US-JennyNeural",
    "Male 09 - English US (Eric - Authoritative)": "en-US-EricNeural",
    "Female 09 - English US (Michelle - Warm)": "en-US-MichelleNeural",
    "Male 10 - English UK (Ryan)": "en-GB-RyanNeural",
    "Female 10 - English UK (Sonia)": "en-GB-SoniaNeural",
    "Male 11 - English Australia (William)": "en-AU-WilliamNeural",
    "Female 11 - English Australia (Natasha)": "en-AU-NatashaNeural",

    # --- Other Major Languages ---
    "Male 12 - French (Henri)": "fr-FR-HenriNeural",
    "Female 12 - French (Denise)": "fr-FR-DeniseNeural",
    "Male 13 - German (Conrad)": "de-DE-ConradNeural",
    "Female 13 - German (Katja)": "de-DE-KatjaNeural",
    "Male 14 - Turkish (Ahmet)": "tr-TR-AhmetNeural",
    "Female 14 - Turkish (Emel)": "tr-TR-EmelNeural",
    "Male 15 - Persian Iran (Farid)": "fa-IR-FaridNeural",
    "Female 15 - Persian Iran (Dilara)": "fa-IR-DilaraNeural"
}

# Core Audio Generation Logic
async def generate_audio(text, voice_id, pitch, rate, output_file="story.mp3"):
    # Detect Arabic Script
    is_arabic_script = any('\u0600' <= char <= '\u06FF' for char in text)
    
    # Automatic Tuning for Quran / Arabic: Slow speed (-20%) for clear pronunciation
    if is_arabic_script and "ar-" in voice_id:
        rate = "-20%"
        pitch = "+0Hz"
        
    communicate = edge_tts.Communicate(text, voice_id, pitch=pitch, rate=rate)
    await communicate.save(output_file)

# Sidebar Options
st.sidebar.header("Voice & Audio Settings")
selected_voice_label = st.sidebar.selectbox("Choose Voice Accent/Character:", list(VOICE_MAPPING.keys()))
voice_id = VOICE_MAPPING[selected_voice_label]

speed = st.sidebar.slider("Speech Speed:", min_value=-50, max_value=50, value=0, step=5)
pitch = st.sidebar.slider("Voice Pitch (Hz):", min_value=-20, max_value=20, value=0, step=2)

speed_str = f"{'+' if speed >= 0 else ''}{speed}%"
pitch_str = f"{'+' if pitch >= 0 else ''}{pitch}Hz"

# Text Input Area
text_input = st.text_area("Enter your script / text here:", height=200, placeholder="Type or paste your content here...")

# Action Button
if st.button("Generate Audio 🎙️"):
    if text_input.strip():
        with st.spinner("Generating high-quality audio..."):
            audio_path = "output.mp3"
            asyncio.run(generate_audio(text_input, voice_id, pitch_str, speed_str, audio_path))
            
            st.success("Audio Generated Successfully!")
            st.audio(audio_path, format="audio/mp3")
            
            with open(audio_path, "rb") as file:
                st.download_button(
                    label="Download MP3 📥",
                    data=file,
                    file_name="generated_voice.mp3",
                    mime="audio/mp3"
                )
    else:
        st.warning("Please enter some text to generate audio.")
    
