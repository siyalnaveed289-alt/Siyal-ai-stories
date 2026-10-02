import streamlit as st
import asyncio
import edge_tts
import os
import requests

st.set_page_config(page_title="Sial AI Stories", page_icon="🎬")

st.title("🎬 Sial AI Stories")
st.subheader("Multi-Voice Text-to-Speech & AI Story Generator")

app_mode = st.sidebar.radio("Select Mode:", ["1. Custom Text-to-Speech (Apna Text)", "2. Free AI Story Generator"])

# Expanded Voices Dictionary including Custom Celebrity & Special Styles
VOICES = {
    # --- SPECIAL & CELEBRITY STYLES (Tone Customizations) ---
    "🕌 Islamic Respectful Voice (Soft & Deep Adab)": {"id": "ur-PK-AsadNeural", "pitch": "-4Hz", "rate": "-10%"},
    "🇵🇰 Imran Khan Style (Deep & Aggressive Male)": {"id": "ur-PK-AsadNeural", "pitch": "-8Hz", "rate": "+5%"},
    "🏏 Babar Azam Style (Calm & Soft Male)": {"id": "ur-PK-AsadNeural", "pitch": "+0Hz", "rate": "-5%"},
    "👔 Nawaz Sharif Style (Elderly Slow Male)": {"id": "ur-PK-AsadNeural", "pitch": "-10Hz", "rate": "-15%"},
    "⚡ Shahbaz Sharif Style (Energetic Fast Male)": {"id": "ur-PK-AsadNeural", "pitch": "-2Hz", "rate": "+20%"},
    "👩‍💼 Maryam Nawaz Style (Confident Female)": {"id": "ur-PK-UzmaNeural", "pitch": "+2Hz", "rate": "+5%"},
    "📜 Famous Poet / Shayari Style (Dramatic Deep Voice)": {"id": "ur-PK-AsadNeural", "pitch": "-6Hz", "rate": "-12%"},

    # --- STANDARD MALE VOICES ---
    "Male 01 - Urdu Standard (Asad)": {"id": "ur-PK-AsadNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Male 02 - English US (Guy - TikTok)": {"id": "en-US-GuyNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Male 03 - English US (Andrew Multilingual)": {"id": "en-US-AndrewMultilingualNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Male 04 - English US (Brian Multilingual)": {"id": "en-US-BrianMultilingualNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Male 05 - English UK (Ryan)": {"id": "en-GB-RyanNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Male 06 - Hindi (Madhur)": {"id": "hi-IN-MadhurNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Male 07 - Arabic UAE (Hamdan)": {"id": "ar-AE-HamdanNeural", "pitch": "+0Hz", "rate": "+0%"},

    # --- STANDARD FEMALE VOICES ---
    "Female 01 - Urdu Standard (Uzma)": {"id": "ur-PK-UzmaNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Female 02 - English US (Jenny - TikTok)": {"id": "en-US-JennyNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Female 03 - English US (Ava Multilingual)": {"id": "en-US-AvaMultilingualNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Female 04 - English UK (Sonia)": {"id": "en-GB-SoniaNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Female 05 - Hindi (Swara)": {"id": "hi-IN-SwaraNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Female 06 - Arabic UAE (Fatima)": {"id": "ar-AE-FatimaNeural", "pitch": "+0Hz", "rate": "+0%"}
}

selected_voice_name = st.selectbox("Choose Voice / Celebrity Style:", list(VOICES.keys()))
selected_voice_cfg = VOICES[selected_voice_name]

# Pitch & Rate Manual Sliders
st.write("---")
st.write("**Fine-tune Voice (Optional Custom Adjustments):**")
col_pitch, col_rate = st.columns(2)
with col_pitch:
    pitch_val = st.slider("Pitch Adjustment (Hz):", min_value=-20, max_value=20, value=0, step=2)
with col_rate:
    rate_val = st.slider("Speed Adjustment (%):", min_value=-30, max_value=30, value=0, step=5)

# Calculate final pitch and rate
base_pitch = int(selected_voice_cfg["pitch"].replace("Hz", ""))
base_rate = int(selected_voice_cfg["rate"].replace("%", ""))

final_pitch_num = base_pitch + pitch_val
final_rate_num = base_rate + rate_val

final_pitch = f"{'+' if final_pitch_num >= 0 else ''}{final_pitch_num}Hz"
final_rate = f"{'+' if final_rate_num >= 0 else ''}{final_rate_num}%"

async def generate_audio(text, voice_id, pitch, rate, output_file="story.mp3"):
    communicate = edge_tts.Communicate(text, voice_id, pitch=pitch, rate=rate)
    await communicate.save(output_file)

# ---------------- MODE 1: CUSTOM TEXT TO SPEECH ----------------
if app_mode == "1. Custom Text-to-Speech (Apna Text)":
    st.write("### 🎙️ Direct Text to Speech")
    user_text = st.text_area(
        "Yahan apna text likhein:", 
        "Welcome! Pick any voice style and hear it speak naturally."
    )
    
    if st.button("Speak Text"):
        if user_text:
            with st.spinner("Generating Audio..."):
                try:
                    if os.path.exists("story.mp3"):
                        os.remove("story.mp3")
                    
                    asyncio.run(generate_audio(user_text, selected_voice_cfg["id"], final_pitch, final_rate, "story.mp3"))
                    
                    if os.path.exists("story.mp3"):
                        st.success("Voice Generated Successfully!")
                        st.audio("story.mp3", format="audio/mp3")
                        
                        with open("story.mp3", "rb") as file:
                            st.download_button(
                                label="📥 Download Voice MP3",
                                data=file,
                                file_name="sial_ai_audio.mp3",
                                mime="audio/mp3"
                            )
                except Exception as e:
                    st.error(f"Audio Error: {e}")
        else:
            st.warning("Please enter text first.")

# ---------------- MODE 2: AI STORY GENERATOR ----------------
else:
    st.write("### 🤖 Free AI Story Generator")
    
    st.write("**Quick Topics (Preset Buttons):**")
    col_a, col_b, col_c, col_d = st.columns(4)
    preset_topic = ""
    if col_a.button("🕌 Islamic Story"):
        preset_topic = "اسلام کی تاریخ کا ایک خوبصورت اور سبق آموز واقعہ، جو نہایت ادب اور احترام کے ساتھ بیان کیا گیا ہے۔"
    if col_b.button("📈 Trading Tip"):
        preset_topic = "Top risk management trading strategies for beginners."
    if col_c.button("📜 Urdu Shayari"):
        preset_topic = "زندگی اور جدوجہد پر بہترین اردو شاعری اور گہرے الفاظ۔"
    if col_d.button("😱 Horror Story"):
        preset_topic = "ایک ویران حویلی اور پرراسرار واقعہ۔"

    prompt = st.text_input("Enter Story Topic:", value=preset_topic if preset_topic else "A Brave Hero")
    category = st.selectbox("Story Category:", ["Moral / Islamic / Sabaq Amoz", "Poetry / Shayari", "Action / Adventure", "Funny / Mazahiya", "Mystery / Raaz"])
    api_key = st.text_input("Groq Free API Key (Optional):", type="password")

    if st.button("Generate AI Story"):
        if prompt:
            with st.spinner("Generating AI Content..."):
                story_text = ""
                
                # System Prompt tweaking for Islamic & Respectful Tone
                system_instruction = "You are a respectful storyteller. Generate engaging content in the same language as input."
                if "Islamic" in category or "🕌" in selected_voice_name:
                    system_instruction = "You are a deeply respectful Islamic storyteller. Use highly respectful, polite, and honorific language (Adab and Ahteram)."

                if api_key:
                    try:
                        headers = {
                            "Authorization": f"Bearer {api_key}",
                            "Content-Type": "application/json"
                        }
                        payload = {
                            "model": "llama3-8b-8192",
                            "messages": [
                                {"role": "system", "content": system_instruction},
                                {"role": "user", "content": f"Write a {category} content about: {prompt}."}
                            ]
                        }
                        res = requests.post("https://api.groq.com/openai/v1/chat/completions", json=payload, headers=headers)
                        if res.status_code == 200:
                            story_text = res.json()["choices"][0]["message"]["content"]
                    except Exception as e:
                        st.error(f"AI API Error: {e}")

                if not story_text:
                    story_text = f"یہ کہانی {prompt} کے بارے میں ہے، جس میں صابر اور نیک عمل کا پیغام دیا گیا ہے۔"

                st.success("Content Generated!")
                st.write("### 📖 Content Text:")
                st.write(story_text)
                
                st.info(f"🎙️ Generating Voice ({selected_voice_name})...")
                try:
                    if os.path.exists("story.mp3"):
                        os.remove("story.mp3")
                    
                    asyncio.run(generate_audio(story_text, selected_voice_cfg["id"], final_pitch, final_rate, "story.mp3"))
                    
                    if os.path.exists("story.mp3"):
                        st.audio("story.mp3", format="audio/mp3")
                        
                        with open("story.mp3", "rb") as file:
                            st.download_button(
                                label="📥 Download Voice MP3",
                                data=file,
                                file_name="sial_ai_story.mp3",
                                mime="audio/mp3"
                            )
                except Exception as e:
                    st.error(f"Audio Error: {e}")
        else:
            st.warning("Please enter a topic first.")

        
        
  
