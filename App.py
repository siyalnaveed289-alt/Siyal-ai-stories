import streamlit as st
import asyncio
import edge_tts
import os
import requests

st.set_page_config(page_title="Sial AI Stories", page_icon="🎬", layout="wide")

st.title("🎬 Sial AI Stories")
st.subheader("Multi-Voice Natural Text-to-Speech & AI Story Generator")

app_mode = st.sidebar.radio("Select Mode:", ["1. Custom Text-to-Speech (Apna Text)", "2. Free AI Story Generator"])

# High-Quality Natural Voices Dictionary
VOICES = {
    # --- NATURAL URDU & REGIONAL MALE VOICES ---
    "👨‍💼 Male 01 - Urdu Pakistan (Asad - Natural Standard)": {"id": "ur-PK-AsadNeural", "pitch": "+0Hz", "rate": "+0%"},
    "👨‍🏫 Male 02 - Urdu India (Salman - Soft & Natural)": {"id": "ur-IN-SalmanNeural", "pitch": "+0Hz", "rate": "+0%"},
    "🎙️ Male 03 - Urdu Deep Narrator (Asad Deep Tone)": {"id": "ur-PK-AsadNeural", "pitch": "-3Hz", "rate": "-5%"},
    "⚡ Male 04 - Urdu Energetic Anchor": {"id": "ur-PK-AsadNeural", "pitch": "+0Hz", "rate": "+10%"},
    "📜 Male 05 - Urdu Poetry / Shayari Tone": {"id": "ur-PK-AsadNeural", "pitch": "-2Hz", "rate": "-8%"},
    "🕌 Male 06 - Urdu Islamic Respectful Voice": {"id": "ur-PK-AsadNeural", "pitch": "-1Hz", "rate": "-5%"},
    "🇵🇰 Male 07 - Urdu Leader Style": {"id": "ur-PK-AsadNeural", "pitch": "-2Hz", "rate": "+0%"},
    "👦 Male 08 - Urdu Young Tone": {"id": "ur-IN-SalmanNeural", "pitch": "+2Hz", "rate": "+5%"},
    " Male 09 - Hindi / Urdu (Madhur Natural)": {"id": "hi-IN-MadhurNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Male 10 - Sindhi Pakistan (Nabeel Natural)": {"id": "sd-PK-NabeelNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Male 11 - Saraiki / Shahpuri (Asad Natural)": {"id": "pnb-PK-AsadNeural", "pitch": "+0Hz", "rate": "+0%"},

    # --- NATURAL URDU & REGIONAL FEMALE VOICES ---
    "👩‍💼 Female 01 - Urdu Pakistan (Uzma - Natural Standard)": {"id": "ur-PK-UzmaNeural", "pitch": "+0Hz", "rate": "+0%"},
    "👩‍🏫 Female 02 - Urdu India (Gul - Soft & Melodious)": {"id": "ur-IN-GulNeural", "pitch": "+0Hz", "rate": "+0%"},
    "📖 Female 03 - Urdu Storyteller": {"id": "ur-PK-UzmaNeural", "pitch": "-1Hz", "rate": "-5%"},
    "📻 Female 04 - Urdu Radio RJ Style": {"id": "ur-IN-GulNeural", "pitch": "+1Hz", "rate": "+5%"},
    "👧 Female 05 - Urdu Young Tone": {"id": "ur-PK-UzmaNeural", "pitch": "+3Hz", "rate": "+5%"},
    " Female 06 - Hindi / Urdu (Swara Natural)": {"id": "hi-IN-SwaraNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Female 07 - Sindhi Pakistan (Uzma Natural)": {"id": "sd-PK-UzmaNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Female 08 - Saraiki / Shahpuri (Uzma Natural)": {"id": "pnb-PK-UzmaNeural", "pitch": "+0Hz", "rate": "+0%"},

    # --- ARABIC VOICES ---
    "🕌 Male - Arabic Saudi Arabia (Hamed - Best for Quran)": {"id": "ar-SA-HamedNeural", "pitch": "+0Hz", "rate": "+0%"},
    "🕌 Female - Arabic Saudi Arabia (Zariyah)": {"id": "ar-SA-ZariyahNeural", "pitch": "+0Hz", "rate": "+0%"},
    " Male - Arabic UAE (Hamdan)": {"id": "ar-AE-HamdanNeural", "pitch": "+0Hz", "rate": "+0%"},

    # --- ENGLISH VOICES ---
    " Male - English US (Guy Natural)": {"id": "en-US-GuyNeural", "pitch": "+0Hz", "rate": "+0%"},
    " Female - English US (Jenny Natural)": {"id": "en-US-JennyNeural", "pitch": "+0Hz", "rate": "+0%"},
    " Male - English UK (Ryan)": {"id": "en-GB-RyanNeural", "pitch": "+0Hz", "rate": "+0%"},
    " Female - English UK (Sonia)": {"id": "en-GB-SoniaNeural", "pitch": "+0Hz", "rate": "+0%"}
}

st.write("---")
category_filter = st.radio(
    "Filter Voices Category:", 
    ["All Voices", "Urdu Male Voices", "Urdu Female Voices", "Sindhi & Saraiki", "Arabic / Quran", "English Voices"], 
    horizontal=True
)

if category_filter == "Urdu Male Voices":
    filtered_voices = {k: v for k, v in VOICES.items() if "Male" in k and ("Urdu" in k or "Hindi" in k)}
elif category_filter == "Urdu Female Voices":
    filtered_voices = {k: v for k, v in VOICES.items() if "Female" in k and ("Urdu" in k or "Hindi" in k)}
elif category_filter == "Sindhi & Saraiki":
    filtered_voices = {k: v for k, v in VOICES.items() if "Sindhi" in k or "Saraiki" in k}
elif category_filter == "Arabic / Quran":
    filtered_voices = {k: v for k, v in VOICES.items() if "Arabic" in k}
elif category_filter == "English Voices":
    filtered_voices = {k: v for k, v in VOICES.items() if "English" in k}
else:
    filtered_voices = VOICES

selected_voice_name = st.selectbox("Choose Voice Character:", list(filtered_voices.keys()))
selected_voice_cfg = filtered_voices[selected_voice_name]

# Pitch & Rate Sliders
col_pitch, col_rate = st.columns(2)
with col_pitch:
    pitch_val = st.slider("Fine Pitch Adjustment (Hz):", min_value=-10, max_value=10, value=0, step=1)
with col_rate:
    rate_val = st.slider("Fine Speed Adjustment (%):", min_value=-20, max_value=20, value=0, step=5)

# Calculate final pitch and rate
base_pitch = int(selected_voice_cfg["pitch"].replace("Hz", ""))
base_rate = int(selected_voice_cfg["rate"].replace("%", ""))

final_pitch_num = base_pitch + pitch_val
final_rate_num = base_rate + rate_val

final_pitch = f"{'+' if final_pitch_num >= 0 else ''}{final_pitch_num}Hz"
final_rate = f"{'+' if final_rate_num >= 0 else ''}{final_rate_num}%"

async def generate_audio(text, voice_id, pitch, rate, output_file="story.mp3"):
    # Arabic script detection for clear recitation
    is_arabic_script = any('\u0600' <= char <= '\u06FF' for char in text)
    if is_arabic_script and "ar-" in voice_id:
        rate = "-15%"
        pitch = "+0Hz"
        
    communicate = edge_tts.Communicate(text, voice_id, pitch=pitch, rate=rate)
    await communicate.save(output_file)

# ---------------- MODE 1: CUSTOM TEXT TO SPEECH ----------------
if app_mode == "1. Custom Text-to-Speech (Apna Text)":
    st.write("### 🎙️ Direct Text to Speech")
    user_text = st.text_area(
        "Yahan apna text likhein:", 
        "خوش آمدید! سیال اے آئی اسٹوریز میں اپنا متن درج کریں اور بہترین اور قدرتی آواز حاصل کریں۔"
    )
    
    if st.button("Generate & Speak Audio 🎙️"):
        if user_text.strip():
            with st.spinner("Generating Natural Audio..."):
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
        preset_topic = "Top risk management trading strategies for beginners in Urdu."
    if col_c.button("📜 Urdu Shayari"):
        preset_topic = "زندگی اور جدوجہد پر بہترین اردو شاعری اور گہرے الفاظ۔"
    if col_d.button("😱 Horror Story"):
        preset_topic = "ایک ویران حویلی اور پرراسرار واقعہ۔"

    prompt = st.text_input("Enter Story Topic:", value=preset_topic if preset_topic else "ایک بہادر انسان کی کہانی")
    category = st.selectbox("Story Category:", ["Moral / Islamic / Sabaq Amoz", "Poetry / Shayari", "Action / Adventure", "Funny / Mazahiya", "Mystery / Raaz"])
    api_key = st.text_input("Groq Free API Key (Optional):", type="password")

    if st.button("Generate AI Story 🚀"):
        if prompt.strip():
            with st.spinner("Generating AI Content..."):
                story_text = ""
                
                system_instruction = "You are a respectful Urdu storyteller. Generate engaging content in natural Urdu."
                if "Islamic" in category:
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
                                {"role": "user", "content": f"Write a {category} story in Urdu about: {prompt}."}
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
            
